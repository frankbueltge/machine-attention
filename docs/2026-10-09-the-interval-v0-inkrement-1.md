# The Interval — V0, Inkrement 1: Quellen und Snapshots (2026-10-09)

**Stufe:** V0, Inkrement 1 von 6 (`docs/2026-10-04-kandidat-the-interval.md` §6). Go: 2026-10-04.

**Gebaut:** `practice/src/practice/interval/sources.py`, Tests in
`practice/tests/test_interval_sources.py` (8, ohne Netz). Erste Bytes unter
`interval/snapshots/2026-10-09/` mit Manifest: IPC national long (403 666 Byte, CC0,
`ipc/ipc_global_national_long.csv`) samt dem CKAN-Record, dazu als Probe der Grenze
Sudan 2024, FSC-gekennzeichnet (`fts/SDN/`, 2 Seiten, vollständig).

**Entscheidungen**
- Kein ETag: der Substrat-Client gibt keine Antwort-Header heraus. Stattdessen übergeht
  `snapshot_ipc` identische Bytes (SHA-256 gegen den neuesten Snapshot) und legt dann
  keinen Tag an. Eine Datei pro Woche, ehrlicher User-Agent.
- Die Ressource wird über den CKAN-Record per Namen aufgelöst, nicht über eine feste ID.

**Neuer Befund für Inkrement 3 (Geld-Reihe):** FTS behandelt `year=2011,2012,2013` und
`year=2011-2013` verschieden (Somalia: 1 912 gegen 13 229 Flüsse, Probe vom 2026-10-09).
Welche Form die „mehrjährige Grenze" der Episode ist, ist vor der Geld-Reihe zu klären;
bis dahin wird die Form unverändert in der gesicherten URL geführt.

**Nächstes Inkrement:** Warn-Reihe und t0 als reine Funktionen (Inkrement 2), mit der
chronischen Phase-4-Lage als Gegenprobe.
