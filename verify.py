#!/usr/bin/env python3
"""Walk the provenance chain backwards and fail on any hole (invariant I1).

Checks: snapshot manifests ↔ bytes (SHA-256, both directions), registry
history anchored in manifested snapshots, announced_at immutability rules,
autonomy protocol coverage, and the stage as a byte-identical deterministic
rebuild of the committed records. Stdlib only.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import sys
import tempfile
from pathlib import Path

VALID_STATUS = {"OPEN", "CLOSED_BY_SOURCE", "DISSIPATED"}
VALID_EVENTS = {"NOTARIZED", "REVISED", "REAPPEARED", "CLOSED_BY_SOURCE",
                "DISSIPATED"}
VALID_VERDICTS = {"EPISODE_ENDED", "MATERIALIZED_AS_ALERT", "NO_ALERT_MATCH"}
MANIFEST_KEYS = ("file", "url", "retrieved_at", "http_status", "sha256")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def check(root: Path) -> list[str]:
    problems: list[str] = []
    registry_files: dict[str, dict] = {}

    snap_base = root / "foreknown" / "snapshots"
    day_dirs = sorted(d for d in snap_base.iterdir() if d.is_dir()) \
        if snap_base.exists() else []
    for day_dir in day_dirs:
        manifest_path = day_dir / "manifest.json"
        if not manifest_path.exists():
            problems.append(f"{day_dir.name}: missing manifest.json")
            continue
        manifest = load(manifest_path)
        listed = set()
        for entry in manifest.get("entries", []):
            missing = [k for k in MANIFEST_KEYS if k not in entry]
            if missing:
                problems.append(f"{manifest_path}: entry missing {missing}")
                continue
            target = root / entry["file"]
            listed.add(entry["file"])
            if not target.exists():
                problems.append(f"{entry['file']}: listed but missing")
            elif sha256_file(target) != entry["sha256"]:
                problems.append(f"{entry['file']}: bytes do not match manifest sha256")
            else:
                registry_files[entry["file"]] = entry
        if not (day_dir / "run.json").exists():
            problems.append(f"{day_dir.name}: missing run.json")
        for file in day_dir.rglob("*"):
            if file.is_file() and file.name not in ("manifest.json", "run.json"):
                rel = file.relative_to(root).as_posix()
                if rel not in listed:
                    problems.append(f"{rel}: preserved but not manifested")

    registry = load(root / "foreknown" / "registry.json") \
        if (root / "foreknown" / "registry.json").exists() else {"futures": {}}
    for fid, future in sorted(registry["futures"].items()):
        if future.get("status") not in VALID_STATUS:
            problems.append(f"{fid}: illegal status {future.get('status')!r}")
        history = future.get("history", [])
        if not history:
            problems.append(f"{fid}: empty history")
            continue
        if history[0].get("event") != "NOTARIZED":
            problems.append(f"{fid}: history does not begin with NOTARIZED")
        if not future.get("announced_at"):
            problems.append(f"{fid}: missing announced_at")
        elif history[0].get("ts") != future["announced_at"]:
            problems.append(f"{fid}: announced_at diverges from notarization event")
        for event in history:
            if event.get("event") not in VALID_EVENTS:
                problems.append(f"{fid}: unknown history event {event.get('event')!r}")
            anchor = event.get("snapshot")
            if anchor and anchor not in registry_files:
                problems.append(f"{fid}: history anchor {anchor} not manifested")

    for res_file in sorted(root.glob("foreknown/resolutions/*.json")):
        resolution = load(res_file)
        fid = resolution.get("future", res_file.stem)
        future = registry["futures"].get(fid)
        if future is None:
            problems.append(f"resolution {fid}: unknown future")
            continue
        if future.get("status") == "OPEN":
            problems.append(f"resolution {fid}: future is still OPEN")
        if resolution.get("verdict") not in VALID_VERDICTS:
            problems.append(f"resolution {fid}: illegal verdict "
                            f"{resolution.get('verdict')!r}")
        if not resolution.get("resolved_at"):
            problems.append(f"resolution {fid}: missing resolved_at")
        if not isinstance(resolution.get("measured"), dict):
            problems.append(f"resolution {fid}: measured is not a record")
        for anchor in resolution.get("evidence", []):
            if anchor not in registry_files:
                problems.append(f"resolution {fid}: evidence {anchor} "
                                "not manifested")

    log_path = root / "autonomy" / "log.jsonl"
    run_dates = {load(p)["date"] for p in root.glob("foreknown/snapshots/*/run.json")}
    logged = set()
    if log_path.exists():
        for i, line in enumerate(log_path.read_text(encoding="utf-8").splitlines(), 1):
            try:
                entry = json.loads(line)
            except json.JSONDecodeError:
                problems.append(f"autonomy log line {i}: unparseable")
                continue
            if entry.get("step") == "foreknown-notary-run":
                logged.add(entry.get("detail", {}).get("date"))
    for missing_date in sorted(run_dates - logged):
        problems.append(f"run {missing_date} has no autonomy protocol entry")

    generator = root / "stage" / "generate.py"
    public = root / "public"
    if generator.exists():
        spec = importlib.util.spec_from_file_location("stagegen", generator)
        stagegen = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(stagegen)
        with tempfile.TemporaryDirectory() as tmp:
            fresh = stagegen.build(root, Path(tmp) / "public")
            fresh_files = {p.relative_to(fresh).as_posix(): p.read_bytes()
                           for p in fresh.rglob("*") if p.is_file()}
            public_files = {p.relative_to(public).as_posix(): p.read_bytes()
                            for p in public.rglob("*") if p.is_file()} \
                if public.exists() else {}
            if not public_files:
                problems.append("public/ missing — stage not generated")
            elif fresh_files != public_files:
                diff = sorted(set(fresh_files) ^ set(public_files)) or sorted(
                    k for k in fresh_files if fresh_files[k] != public_files.get(k))
                problems.append("public/ is not a deterministic rebuild "
                                f"(differs: {diff[:5]})")
    return problems


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo-root", default=".", type=Path)
    args = parser.parse_args(argv)
    problems = check(args.repo_root.resolve())
    if problems:
        print(f"provenance chain has {len(problems)} hole(s):")
        for problem in problems:
            print(f"  - {problem}")
        return 1
    print("provenance chain intact")
    return 0


if __name__ == "__main__":
    sys.exit(main())
