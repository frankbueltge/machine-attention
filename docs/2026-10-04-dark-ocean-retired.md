# Dark Ocean — RETIRED (2026-10-04)

**Datum:** 2026-10-04 · **Entscheidung:** Frank (Maintainer), Wortlaut privat · **Status:**
RETIRED (Aufnahme-Pfad: „jederzeit: RETIRED“ — ehrlich beendet, Records bleiben, Grund
committet). Letzte Nacht: **2026-10-03**. Am selben Tag wie The Foreknown
(`docs/2026-10-04-foreknown-retired.md`).

## 1. Was Dark Ocean war, und was davon zuletzt lief

Dark Ocean stellte das Hinsehen gegen das Deklarieren: Welche Sentinel-1-Überflüge welche
Ostsee-Kachel abdeckten, gegen das, was das deklarierte Meer über sich sagte. Das E-Experiment
war am 2026-08-22 nicht bestanden (`docs/2026-08-22-dark-ocean-e-review.md`). Weiter lief seither
nur ein Teil davon, als Instrument ohne Bühne: der nächtliche Kontinuitäts-Notar, der den
Copernicus-Katalog fragt, ob er noch sagt, was er gesagt hat.

## 2. Was der Record sagt (nachgezählt aus `darkocean/continuity/*.json`)

- **54 Nächte** Kontinuitäts-Probe (2026-08-11 bis 2026-10-03), **62.737** erneut gefragte
  Katalogzeilen.
- **32 verschiedene Produkte** wichen ab:
  - **14** verschwanden aus dem Katalog (`gone_from_catalog`).
  - **18** änderten nur ihr `modification_date`, ein Metadaten-Zeitstempel. Am Gesehenen
    änderte sich nichts.
- **Korrektur einer veröffentlichten Zahl:** Der Export meldete `darkocean_continuity_divergences`
  als Summe der nächtlichen Fanglisten, zuletzt **614**. Ein Produkt, das verschwunden bleibt,
  wird aber jede Nacht neu gefangen. Gezählt waren also Sichtungen, nicht Abweichungen. Seit
  diesem Commit zählt der Export verschiedene Produkte (32). Das war der offene Vorschlag aus
  PR #49 (damals 12 → 4); PR #46 und #49 sind damit erledigt.

## 3. Warum es endet

Der Maintainer hat entschieden, dass dieses Instrument die Aufmerksamkeit der Praxis nicht
trägt. Dark Ocean hatte keine Bühne. Sein nächtlicher Ertrag war eine Nachprüfzahl, ein
gelegentlich verschwundenes Produkt und ein Zeitstempel. Eine Praxis, die „Aufmerksamkeit“ im
Namen führt, kann sie nicht zweimal ausgeben. Sie gehört jetzt den Projekten, die gebaut werden:
The Interval und Planetary Listening.

## 4. Was sich ändert, was bleibt

- `.github/workflows/darkocean.yml` ist entfernt. Lesung und Kontinuitäts-Probe laufen nicht mehr.
  Der Code unter `practice/src/practice/darkocean/` bleibt als Teil des Records.
- `darkocean/RETIRED.json` ist der Abschluss. Ihn lesen:
  - der Export (Status `retired`),
  - der Stall-Check (`retired`, nicht `STALE`),
  - `verify.py`: keine datierte Nacht nach dem 2026-10-03, für Dark Ocean wie für The Foreknown
    über dieselbe allgemeine Prüfung.
- **Nichts wird gelöscht:** Readings, Kontinuitäts-Probes, Snapshots, Anker, `darkocean/draft/` und
  `METHOD.md` bleiben.
