# Planetary Listening — Reparatur im Fenster: ein Host ohne Antwort ist eine Ausfallnacht, keine verlorene (2026-10-22)

**Stufe:** E-EXPERIMENT, Fenster offen seit der Lesung 2026-10-21
(`docs/2026-10-19-planetary-listening-e-experiment-kriterien.md`). **Art:** Reparatur nach
`discovery/PROMPT.md` Schritt 3 — der Defekt ist belegt, die Reparatur schmal.

## Der Defekt

Die erste Fensternacht hat keine Lesung: `planetary/readings/2026-10-21.json` fehlt auf `main`.
Der Workflow-Lauf `planetary` Nr. 6 (geplant, 2026-10-21 13:42–13:52 UTC, Commit `9bed1e7`)
endete mit Exit 1:

    practice.fetch.SourceUnavailable: https://geofon.gfz.de/fdsnws/dataselect/1/query:
    network error: TimeoutError after 4 attempts

Die Ausnahme kam aus `spike._station_day` (`practice/src/practice/planetary/spike.py`) und
verließ `nightly.run` (`practice/src/practice/planetary/nightly.py`) unbehandelt. Der Zweig, den
die Tagesroutine für einen Ausfall hat (`status != 200` → `outage: True`), wird nur bei einer
HTTP-Antwort genommen, nie bei einem Netzfehler. So wurde aus einer Ausfallnacht, die A2 mit
benannter Ursache zählen soll (Kriterien §2, A2: „die Ursache im Record benannt"), eine fehlende
Nacht für A1. Die Zählung `python -m practice.planetary.experiment --repo-root .` nennt zur
Passzeit (2026-10-22, 06:38 UTC) `A1_missing_nights: ["2026-10-21", "2026-10-22"]` — die zweite,
weil der heutige Lauf (Slot 08:10, gelaufen bisher 11:08–13:53 UTC) noch aussteht. Fällt auch
2026-10-22 aus demselben Grund aus, sind zwei Nächte in Folge verloren und A1 gerissen.

## Die Reparatur

`nightly.py`: der Client wird in `_Recording` gehüllt. Wirft ein Abruf `SourceUnavailable`,
antwortet er Status 0 ohne Bytes; die Ursache (der bereits redigierte Text der Ausnahme) wird in
der Ledger-Zeile als `error` geführt und, wenn die Tagesdatei betroffen ist, in
`station_day.cause`. Die Nacht wird geschrieben, registriert, verifiziert und committet wie jede
andere; `experiment.failures` zählt sie als `day file 0`.

Test: `practice/tests/test_planetary_nightly.py`,
`test_a_host_that_times_out_is_a_failed_night_not_a_lost_one` — ein Client, der für dataselect
genau die Ausnahme des Laufs wirft; die Lesung entsteht, mit Ausfall, Ursache, und dem Rest der
Nacht (extent, Kataloge) gelesen.

## Was sich nicht ändert

Auf jeder Nacht, in der jeder Host antwortet, ist die Lesung Byte für Byte dieselbe wie vorher:
`_Recording` reicht durch. Der Detektor (`detect.py`, `stalta-v1`, B6), `spike.py`, die
Zeitgrenzen des Clients (90 s, vier Versuche), der Workflow und die Kriterien bleiben
unverändert. Keine Lesung wird nachgeholt: die Kriterien zählen einen Nachlauf nur am selben
Datum (§1), 2026-10-21 bleibt die eine fehlende Nacht, die A1 erlaubt (≥ 13 von 14). Ein
Nachlauf per `workflow_dispatch` heute ist des Maintainers Klick und wird in `REQUESTS.md`
erbeten, nicht getan.

## Für das Review

Die Reparatur liegt im Fenster. Ausgang „Verlängert" der Kriterien (§5) nennt genau diesen Fall
— „A1 oder A2 knapp verletzt mit benannter, behobener Ursache"; ob die Reparatur im Fenster das
Fenster berührt, entscheidet das Review des Maintainers, nicht dieser Pass.
