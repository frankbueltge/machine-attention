# The Interval — V0, Inkrement 4: das Register (2026-10-12)

**Stufe:** V0, Inkrement 4 von 6 (`docs/2026-10-04-kandidat-the-interval.md` §6). Go: 2026-10-04.

**Gebaut:**
- `practice/src/practice/interval/register.py` — `interval/register.json` als reine Funktion der
  committeten Snapshots und der Liste `interval/drivers.json`; kein Netz, keine Wanduhr. Aufruf:
  `python -m practice.interval.register --repo-root .`
- `verify.py` — `interval/snapshots` wird jetzt wie die anderen Register auf Manifest ↔ Bytes
  geprüft (vorher gar nicht), und `check_interval` rechnet das Register **unabhängig vom
  Paket** (nur Standardbibliothek) aus denselben Snapshots nach. Jede Abweichung einer Episode
  ist ein Loch.
- Tests: `practice/tests/test_interval_register.py` (5, konstruierte Snapshots in einem
  temporären Baum; dazu: das committete Register ist sein eigener Neubau, und `verify.py`
  erkennt ein manipuliertes Register).
- Snapshots: `interval/snapshots/2026-10-12/` — für jeden Beginn die FTS-Abfrage mit der
  Kommaliste aus `boundary_years`, FSC und Ländertotal, 113 Anfragen, kein 429, jede Seitenmenge
  vollständig (letzte Seite ohne `nextLink`). Somalia 2022 FSC liegt schon im Snapshot vom
  2026-10-11 und wurde nicht neu geholt. Größe: 41 MB JSON. Das ist der Preis des Ländertotals
  (rund 14 700 Flüsse); FSC allein wären etwa 5 MB.

**Entscheidungen**
- **Episode = (Land, t0)**, mit den θ, bei denen dieser Monat ein Beginn ist. Somalia 2022-03 und
  2026-01 sowie Jemen 2025-06 sind Beginne bei 5 % und 10 %. Linkszensierte Länder stehen je θ
  daneben, nie als Episode.
- **Je Flussmenge der neueste vollständige Snapshot.** Unvollständig (eine Seite nicht 200, oder
  die letzte Seite hat noch einen `nextLink`) heißt `not_preserved`; nichts wird geschätzt.
- **`as_of` je Flussmenge ist der Monat ihres Snapshot-Tags**, nicht der neueste Snapshot
  überhaupt: Eine offene Uhr läuft nie über das hinaus, was ihr Snapshot sehen konnte.
- **Geld auf Cent, Anteile auf sechs Stellen**, summiert in Fluss-ID-Reihenfolge; so stimmen
  beide Implementierungen Byte für Byte überein.
- **Treiber:** `interval/drivers.json` führt alle acht Episoden als `unassigned`. Für keinen
  Treiber ist bisher eine Quelle gesichert, und ein Treiber aus dem Gedächtnis ist keine
  Beobachtung. Ein Treiber ohne Quelle wird vom Paket abgewiesen und von `verify.py` als Loch
  gemeldet.

**Lesung (jetzt Record: `interval/register.json`, Snapshot-Monat 2026-10).** 8 Episoden, 64
Gitterzellen (k × Achse × Menge), keine offen, keine `not_preserved`.

| Land | t0 | θ | Lücke FSC, geflossen (k=2/3) | Lücke FSC, bekannt (k=2/3) | Total, geflossen (k=2/3) |
|---|---|---|---|---|---|
| AFG | 2021-10 | 10 % | 1 / 1 | 0 / 1 | 1 / 1 |
| AFG | 2025-10 | 5 % | 6 / — | 0 / — | 8 / — |
| DJI | 2023-04 | 5 % | 0 / 0 | Basis null | 0 / — |
| SDN | 2023-06 | 10 % | 0 / 0 | 0 / 0 | 0 / 0 |
| SOM | 2022-03 | 5, 10 % | 2 / 2 | 2 / 2 | 2 / 2 |
| SOM | 2024-08 | 5 % | 7 / 7 | 7 / 7 | 7 / 7 |
| SOM | 2026-01 | 5, 10 % | 1 / 1 | 0 / 0 | 1 / 3 |
| YEM | 2025-06 | 5, 10 % | 10 / 10 | 3 / 10 | 4 / 5 |

„—“: kein Monat im Horizont erreicht k × Basis (`none_in_horizon`). Somalia 2026-01 trägt den
Doppelblock-Vermerk (`blocks` = 2); ihr Horizont endet 2026-12, der Halbzeit-Monat fehlt deshalb.
Die Somalia-2022-Kontrolle aus Inkrement 3 ist bestätigt, jetzt auch am Ländertotal (Lücke 2
auf beiden Achsen).

**Was auffällt, ohne Befund zu sein.** Die Spanne reicht von null bis zehn Monate, wie der
Prototyp des Audits sie für Sudan zeigte. Sudan 2023 hat auf jeder Achse und in jeder Menge
Lücke null: Das Geld stieg schon im Monat des Beginns. Ob ein anderer Treiber das Geld zuerst
bewegte, beantwortet der Treiber-Vermerk, und der ist noch leer. Bei Dschibuti ist die FSC-Basis so klein
(38 Flüsse in drei Jahren), dass „zweifach“ wenig heißt; auf der Kenntnis-Achse ist sie null.
Die gezählten Flüsse liegen beim Total nahe am FTS-eigenen `flowCount` derselben Abfragen
(Probe dieser Nacht, `limit=1`, nicht gesichert): z. B. Jemen 2 676 gegen 2 688, Sudan 2 741
gegen 2 743; beim FSC gleich (Afghanistan 2021: 279 gegen 279). Die Reihe behauptet nicht, das
FTS-Total zu sein.

**Was das nicht ist:** keine Aussage über Geber, Angemessenheit oder Ursache. Acht Episoden mit
leerem Treiber-Vermerk sind ein Instrument, kein Befund. Keine Bühne.

**Nächstes Inkrement (5):** der wöchentliche Workflow `interval.yml` (IPC-Abruf, FTS je Episode,
Register-Neubau, Anker-Registrierung, verify, Commit). Davor ist zu entscheiden, wie die
wöchentliche Lesung mit 41 MB Ländertotal umgeht: neu holen nur, was sich ändern kann (Episoden,
deren Horizont nicht abgeschlossen ist), und abgeschlossene Episoden aus ihrem Snapshot lesen.
Parallel, ohne Gate: Treiber-Quellen innerhalb der Charter suchen (öffentlich, ohne Login), bevor
ein Treiber eingetragen wird.
