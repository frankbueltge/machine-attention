# The Interval — Woche 4: eine zweite Uhr öffnet sich, ohne neue Version (2026-11-10)

**Stufe:** E-EXPERIMENT, Fenster läuft (Woche 4 von 4, ISO-Woche 46; das Fenster schließt
2026-11-15). **Art:** Befund aus dem committeten Record, berichtet — kein Eingriff ins Instrument,
keine Änderung an Kriterien, Register oder Lesung. Kriterien:
`docs/2026-10-14-the-interval-e-experiment-kriterien.md`.

## Was gelesen wurde

- `interval/readings/2026-11-09.json` (Commit `bd9c933`, Workflow 13:26 UTC): 8 Episoden,
  30 Anfragen, 0 × 429, IPC `preserved` (neuer Snapshot), 12 Abfragen eingefroren, 4 geholt
  (`autonomy/log.jsonl`, Zeile `interval-reading` vom 2026-11-09).
- Tally `python -m practice.interval.experiment --repo-root .`: Wochen fällig 4 von 4, A1 keine
  fehlende Woche, A2 bestanden, A3 keine, B1 0 Bewegungen, B2 keine Änderung (8 Episoden in allen
  vier Lesungen), B6 unverändert (FSC·date·k=2: 43/77 Placebo gegen 3/7 Beginne). `closed: false`
  nur, weil der Kalender das Fenster erst am 2026-11-15 schließt; eine fünfte Lesung ist nicht fällig.

## IPC: der erste neue Snapshot im Fenster

`ipc_global_national_long.csv` wechselt von `interval/snapshots/2026-10-19/ipc/` (sha256
`ec85a04b…`) auf `interval/snapshots/2026-11-09/ipc/` (sha256 `ca943df0…`). Der Unterschied sind
42 angefügte Zeilen, keine gelöschte oder geänderte: drei neue Analysen (COD Sep 2026, LBN Sep 2026,
UGA Aug 2026, je `current` und `first projection`). Keine davon erzeugt eine Episode — B2 bleibt bei
8. Die eingefrorenen Abfragen bleiben unberührt (B1 0).

## B4, Wochen 3–4

Verglichen wurde `interval/register.json` zwischen Commit `91f4202` (Lesung 2026-11-02) und
`bd9c933` (Lesung 2026-11-09), Zelle für Zelle. Geändert haben sich nur die vier offenen Abfragen
(AFG 2025-10 und SOM 2026-01, je FSC und Total), jede mit neuen Seiten unter
`interval/snapshots/2026-11-09/fts/` und neuen Hashes, dazu `ipc_snapshot`/`ipc_sha256`:
**kein B4-Verstoß.**

| Abfrage | Flüsse | gezählt | Zellen geändert |
|---|---|---|---|
| AFG 2025-10 FSC | 357 → 353 | 285 → 283 | date k=2 `closed` → `none_in_horizon`; Halbmonate, Basis firstReportedDate |
| AFG 2025-10 Total | 2 981 → 3 020 | 2 287 → 2 283 | keine |
| SOM 2026-01 FSC | 280 → 282 | 186 → 188 | Basis date 2 696 555,5 → 1 699 450 USD, Lücke bleibt 1 |
| SOM 2026-01 Total | 1 541 → 1 545 | 1 076 → 1 080 | keine |

## Der Befund: AFG 2025-10, FSC · `date` · k=2

Die Zelle stand in den Lesungen 2026-10-19 bis 2026-11-02 auf `closed`, t1 2026-04, Lücke 6 Monate.
Seit 2026-11-09 steht sie auf **`none_in_horizon`** (Horizont endet 2026-09, `as_of` 2026-11). Die
Basis ist unverändert (32 091 886 USD, Schwelle 2 × = 64,18 Mio.). Nachgerechnet mit
`practice.interval.money` (`parse_flows`, `money_series`) aus den committeten Seiten:

- Monat 2026-04: **69,24 → 35,80 Mio. USD** — unter die Schwelle. Sonst ändert sich im Horizont nur
  2025-08 (3,15 → 3,08, ein entfallener Fluss).
- Die Ursache ist ein einziger Fluss, Id **385472** (`flowType` `Parked`, `paid`, `incoming`,
  `date` 2026-04-15), Seite `…/AFG/fsc-2024_2025_2026-p002.json` in beiden Snapshots:
  `amountUSD` **64 642 725 → 31 200 076**, `childFlowIds` von einem auf sechs Kinder
  (383505 → 383505, 405911, 384086, 384087, 384499, 406463), `updatedAt` 2026-10-23 → 2026-11-09 —
  **`versionId` bleibt 1.** Keines der sechs Kinder steht in den AFG-Listen der Lesung.
- Derselbe Fluss 385472 steht auch in der SOM-FSC-Liste (`…/SOM/fsc-2025_2026-p00*.json`) und
  senkt dort 2026-04 von 68,90 auf 35,46 Mio.; SOMs Zelle bleibt geschlossen (t1 2026-02, Lücke 1),
  weil ihre Antwort vor April liegt. Die SOM-Basis fällt, weil Fluss 356708 (2025-08, 2,88 Mio.)
  nicht mehr gelistet ist.

Die Achse `firstReportedDate` derselben AFG-Zelle bleibt `closed` bei Lücke 0 (k=2); auch ihr April
fällt (67,74 → 34,29), doch ihre Antwort liegt früher.

## Was das heißt — und was nicht

- **Kriterien:** kein Verstoß. Die Abfrage ist offen bis zu einem Snapshot nach 2026-12 (Kriterien
  §3); B4 verlangt den neuen Snapshot, er liegt vor.
- **Messung:** Zweite geschlossene Uhr im Fenster, die die Quelle wieder öffnet (die erste: AFG
  Total·date·k=2, `docs/2026-11-03-the-interval-woche-3.md`). Diesmal ist der Weg ein anderer: kein
  Umdatieren, sondern ein geparkter Betrag, der beim Weiterleiten an Kinder schrumpft, **ohne dass
  die Version steigt**. `parse_flows` hält je Id die höchste `versionId`; innerhalb einer Lesung ist
  das hier ohne Folge (der Fluss steht einmal), über Lesungen hinweg zeigt es: die Version ist kein
  verlässlicher Marker einer Revision, `updatedAt` und die Bytes sind es. Dass ein geparkter Fluss in
  zwei Länderlisten zählt, ist im Instrument so festgelegt (`money.py`, Docstring: „Every flow type
  counts, parked and pass-through included“); ob das doppelt zählt, was nur einmal floss, zeigt der
  Record nicht. Beides geht als Frage ins Review, nicht als Reparatur.
- Keine Zuschreibung (E-2): Die Änderung ist eine Buchung der Quelle, nicht das Versäumnis eines
  Gebers, einer Agentur oder einer Regierung.

## Bewusst nicht

Keine Änderung an `money.py`, `register.json`, den Kriterien oder einer Lesung; keine Abfrage an FTS
oder IPC aus diesem Container. Mit dieser Lesung sind die vier Fensterwochen gelesen; die Nacht nach
2026-11-15 schreibt die Review-Bitte in `REQUESTS.md`, das Review ab 2026-11-16 ist das des
Maintainers.
