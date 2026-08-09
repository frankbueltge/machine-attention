# Dark Ocean — method sheet

**Standing document** (not a dated note): it describes the register as it currently
runs and is edited when the practice changes. Positioning written 2026-08-09 on
decision D1 of the portfolio audit
(`frankbueltge.de/docs/design/2026-08-09-portfolio-audit.md` §4, §7). Build note:
[`docs/2026-08-09-dark-ocean-v0.md`](../docs/2026-08-09-dark-ocean-v0.md); source audit:
[`docs/2026-08-08-dark-ocean-audit.md`](../docs/2026-08-08-dark-ocean-audit.md).

## 1. The claim

**This register notarizes the act of looking.**

Every night at 04:50 UTC, for the completed UTC day, the machine preserves the
Copernicus Data Space catalogue rows of every Sentinel-1 GRD acquisition over a fixed
Baltic box — **with the publisher's own checksums** (BLAKE3, MD5), the footprint, the
`online` flag and the `EvictionDate` the catalogue states. The scene bytes (1–2 GB per
product, login-walled) are never fetched. The catalogue row is the notarial object,
not the image.

The claim is therefore evidentiary, not maritime: *these are the observation claims
the European archive made about this sea on this day, under the archive's own
checksums, preserved on the day they were made, append-only, keylessly, by a machine
that keeps them independently of whether the archive keeps them.*

**What the eviction premise is worth, measured (2026-08-09).** The design was argued
from `EvictionDate` — the archive's own field for products it intends to drop. Probed
against the live catalogue, that premise is **structural, not observed**: the 42
products of the 2026-08-07 reading all carry `EvictionDate 9999-12-31` and
`online: true`, and re-querying every Baltic S1 GRD product of a day two years earlier
(2024-08-07, 51 products) returns 51 × online, 51 × `9999-12-31`. Copernicus is not
currently evicting this material, and announces no date at which it will. So the
honest framing is not "rows ESA will evict" but: *the publisher guarantees no
durability, the field for withdrawal exists and is part of the archive's design, and
this register does not depend on the publisher's word for either.* If an eviction, an
offline transition or a checksum change ever occurs, this register is positioned to
catch it — and until one does, that positioning is a mechanism, not a result, and is
stated as one.

## 2. What is measured

Against that coverage side stands a **declaration** side: a Digitraffic AIS sample
taken at read time, counted **per bin, never per vessel**. The Baltic box
(9–30 E, 53.5–66 N) is a fixed grid of 1050 half-degree bins — geometric bins, no
coastline mask, so every derivation reproduces from `practice/src/practice/darkocean/region.py`
alone. Per bin, per day: `observed_passes` × `declared_sample`, from which three
categories follow —

| category | reading |
|---|---|
| observed-and-declared | the radar passed, the sample declared traffic |
| observed-silent-in-sample | the radar passed, the sample declared nothing |
| declared-unobserved | traffic declared where no radar passed that day |

These are **statements about the overlap of two committed registers.** They are not
statements about hidden ships. "observed-silent-in-sample" is not a dark vessel: the
AIS sample is one moment, the radar pass is another, and no image was ever examined.

## 3. What is not claimed

No detection. No scene bytes. No vessel identities — an `mmsi` in a derived record is
a **verification failure**, enforced by `verify.py`, because small fishing vessels are
person-adjacent. No legality claims, no attribution of intent. Third-party
classifications (e.g. GFW's "intentional disabling") would be carried, if ever, as
labelled model estimates, never as findings of this register.

## 4. Nearest neighbours, and where the daylight is

The measurement of maritime reality is **well occupied**, and this sheet says so
first. Strongest neighbours, in order:

- **[Global Fishing Watch — SAR vessel detections](https://globalfishingwatch.org/platform-update/2024-may-data-download-portal-new-dataset-released-featuring-vessel-detections-from-sentinel-1-sar/)**
  ([Paolo et al. 2024, *Nature*](https://www.nature.com/articles/s41586-023-06825-8)) —
  publishes Sentinel-1 detections since 2017 *including image-footprint polygons and
  overpass rasters*, plus whether each detection broadcast AIS. Both sides of this
  register's overlap exist there as a maintained public dataset — and GFW goes
  further, to detection.
- **[Skylight (Ai2)](https://support.skylight.global/en_US/satellite-radar)** — free,
  near-real-time, full S1/S2 EEZ coverage, 18 months of public history, open-sourced
  detection models, daily dark-vessel flags.
- **[ESA's own Sentinel-1 observation scenario / acquisition plans](https://sentinels.copernicus.eu/copernicus/sentinel-1/acquisition-plans)** —
  the publisher already publishes "the act of looking" as *plans*, archived to 2015.
  This register preserves what was actually catalogued, with checksums, after the fact.
- **[Welch et al. 2022, "Hot spots of unseen fishing vessels"](https://pmc.ncbi.nlm.nih.gov/articles/PMC9629714/)**
  ([code](https://github.com/GlobalFishingWatch/AIS-disabling-high-seas)) — the
  canonical academic AIS-gap register, explicitly conditioned on observability: the
  closest existing "declared vs. observable" epistemics, for AIS reception rather than
  SAR coverage.
- **[SkyTruth Cerulean](https://skytruth.org/cerulean)** — continuous public register
  derived from S1 GRD, free map, API, published methods.
- **[FormerLab shadow-fleet-tracker-light](https://github.com/FormerLab/shadow-fleet-tracker-light)** —
  open-source Baltic shadow-fleet tracking, watchlist- and identity-based: the exact
  opposite design choice to identity-free bin counts.
- **[HELCOM AIS density maps](https://metadata.helcom.fi/geonetwork/srv/api/records/2558244b-0cea-46e9-8053-af6ef5d01853)** —
  the institutional Baltic declared register (AIS since 2005), annual, no coverage side.
- **[OpenTimestamps × Internet Archive](https://petertodd.org/2017/carbon-dating-the-internet-archive-with-opentimestamps)** —
  precedent for notarizing an archive's hashes at scale; not findably applied to an
  Earth-observation catalogue.

**The daylight**, stated narrowly on purpose: nobody found doing this preserves *the
publisher's own checksummed catalogue claims* as a daily, keyless, append-only record,
with a second independent implementation recomputing every figure, and with detection
deliberately refused. Every operational neighbour jumps to detections or identities;
the refusal is the position.

**A gap in that daylight, as the register stands today.** The nightly run writes the
day it just read and never looks back — `run.py` reads no earlier reading. So the
register cannot currently show the one thing its claim rests on: that something it
held has since changed or gone. The catalogue supports the look-back keylessly (a
`Products(<id>)` query returns the current `online`, `EvictionDate` and
`ModificationDate`; verified 2026-08-09), so this is a missing step, not a missing
possibility. Until it exists, the notarial act is asserted rather than demonstrated —
which is why it belongs in the acceptance criteria (§7).

**And the honest converse:** read as a dark-ship instrument, this register is a
degraded subset of what GFW already publishes, and it loses. The per-bin overlap
counts are a demonstration of what two registers can jointly say — not a maritime
finding. If the notarial act is not the headline, the work has no case.

## 5. Sources, licences, failures

| source | what is taken | licence / notice |
|---|---|---|
| [Copernicus Data Space](https://catalogue.dataspace.copernicus.eu) OData catalogue | S1 GRD catalogue rows: name, platform, times, footprint, BLAKE3/MD5, `EvictionDate`, `online` | Copernicus data, free and open; derived records carry the notice, never a bare CC0 claim |
| [Digitraffic](https://meri.digitraffic.fi) AIS locations (Fintraffic) | positions at read time, reduced to per-bin counts before anything is written | Fintraffic open data, CC BY 4.0 — attribution travels with the derived records |
| Danish Maritime Authority daily AIS dumps | the moment axis — **probed nightly, not yet fetched** | probed only; the source's return becomes visible in the record |

**Failures are recorded, never bridged.** The DMA outage of 2026-08-08 stands in the
record as an outage; a source that stops answering makes the register smaller and says
so. `http_status` and `retrieved_at` are preserved per file in each day's manifest.

**Compute footprint.** Keyless HTTP only: two documents per night (~0.5 MB), no scene
bytes, no cloud service, a few seconds of a GitHub Actions runner. Nothing in the V0
path runs on Google Cloud.

## 6. Verification

Each night writes a `manifest.json` with the SHA-256 of every preserved document, and
`verify.py` — a **second implementation**, with its own grid and polygon mathematics —
recomputes the reading from the preserved bytes alone. A figure that only the pipeline
can produce is treated as unverified. The identity ban is a verification rule, not a
convention.

Anchoring the daily manifests to Bitcoin via OpenTimestamps is examined in
[`docs/2026-08-09-opentimestamps-examination.md`](../docs/2026-08-09-opentimestamps-examination.md)
(decision D2) — a git history proves order, not time.

## 7. What this means for the E-experiment criteria

The criteria for the 14-night run must measure **the notarial act**, because that is
where the claim lives. Concretely, the register's own success terms are things like:
did the run catch catalogue rows that later went offline or were evicted; did the
publisher's checksums stay stable for products that stayed online, and was any change
caught; did the second implementation reproduce every published figure; were outages
recorded rather than bridged. Rising or falling vessel counts are **not** success
terms — a quiet Baltic is a quiet record, not a failed night.

The criteria committed on 2026-08-09
([`docs/2026-08-09-dark-ocean-e-experiment-kriterien.md`](../docs/2026-08-09-dark-ocean-e-experiment-kriterien.md))
measure operations, the overlap statistics, stage-worthiness, honesty and the charter —
thoroughly, but they contain no criterion about the notarial act. The addendum
[`docs/2026-08-09-dark-ocean-kriterien-nachtrag-notariat.md`](../docs/2026-08-09-dark-ocean-kriterien-nachtrag-notariat.md)
proposes that gap closed under the criteria document's own §0 (changes allowed, dated,
until the window opens). It is a proposal, not a change: the criteria bind as
committed until Frank decides.

## 8. V1, in advance

The detection path (V1) enters occupied territory knowingly and needs a **different**
USP than this one — the refusal that gives V0 its position is precisely what V1 gives
up. If V1 runs on Earth Engine, it inherits a documented reproducibility trade-off:
an Earth Engine computation is not third-party re-runnable the way a committed query
string is, provenance is self-assembled from committed script, hash, task id and
parameters, and the trade-off is stated openly rather than glossed
(`frankbueltge.de/docs/design/2026-08-09-gcp-activation.md` §4). Earth Engine use
stays on the noncommercial tier at zero cost; if a step would cost real money, work
stops.
