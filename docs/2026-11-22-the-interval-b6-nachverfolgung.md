# The Interval — B6 nachverfolgt: welche Placebo-Zelle sich bewegte, und warum (2026-11-22)

**Stufe:** E-EXPERIMENT geschlossen, Review beim Maintainer (`REQUESTS.md`, 2026-11-16). **Art:**
Nachverfolgung aus dem committeten Record, berichtet — kein Abruf, kein Eingriff ins Instrument,
keine Änderung an Kriterien, Register, Lesungen oder Treibern. Sie schließt die offene Stelle des
Fensterabschlusses (`docs/2026-11-16-the-interval-fenster-abschluss.md`: „welcher Monat hinzukam,
ist heute nicht nachverfolgt").

## Ergebnis in einem Satz

Die Zelle total·`firstReportedDate`·k=2 stieg von 35/77 auf 36/77 **mit der Lesung von Woche 1**
(2026-10-19), nicht in den Wochen 3–4, wie der Abschluss vermutete: der Placebo-Monat AFG 2025-06
schloss statt mit Abstand 4 nun mit Abstand 1, weil ein am Lesetag neu angelegter Fluss ein
Erstmeldedatum von vor fünfzehn Monaten trägt.

## Wie nachverfolgt wurde

`base_rate` aus `practice/src/practice/interval/experiment.py`, unverändert, auf jedem committeten
Stand von `interval/register.json` (je ein Arbeitsbaum, nur gelesen):

| Commit | Stand | total·firstReportedDate·k=2 | alle anderen sieben Zellen |
|---|---|---|---|
| `16a0dcf` | 2026-10-13 (Grundlage des Nachtrags 2026-10-17) | 35/77 gegen 4/7 | wie im Nachtrag |
| `a1a13ae` | Woche 1, 2026-10-19 | **36/77** gegen 4/7 | unverändert |
| `3a71f48`, `91f4202`, `bd9c933` | Wochen 2–4 | 36/77 gegen 4/7 | unverändert |
| `3c26d8c`, `f4ec544` | 2026-11-16 (Treiber; Lesung nach dem Fenster) | 36/77 gegen 4/7 | unverändert |

Zwischen `16a0dcf` und `a1a13ae` ändern sich auf dieser Achse genau zwei Placebo-Monate, beide in
der Episode AFG 2025-10 (Total, Seiten `interval/snapshots/2026-10-13/fts/AFG/total-2024_2025_2026-p0*.json`
gegen `interval/snapshots/2026-10-19/fts/AFG/…`, je 15 Seiten):

- **Placebo t0 2025-06** (Grundwert 85,28 M USD, Schwelle 170,57 M): t1 2025-10 / Abstand 4 →
  t1 **2025-07 / Abstand 1**. Juli 2025 stieg auf dieser Achse von 168,96 auf 172,39 M (+3,42 M) —
  damit zählt der Monat als kurze Antwort (B6_MAX_GAP 1). Das ist die eine hinzugekommene Zelle.
- **Placebo t0 2025-11** (Grundwert 124,90 M, Schwelle 249,79 M): `closed` / Abstand 7 →
  `none_in_horizon`. Juni 2026 fiel von 253,53 auf 245,68 M. Für B6 ohne Wirkung (Abstand 7 war
  nie kurz).

Die Beginne (4/7) bewegen sich nicht.

## Die beiden Mechanismen

**1. Ein neuer Fluss mit rückdatiertem Erstmeldedatum.** Fluss `403006` fehlt in den Seiten vom
2026-10-13 und steht in `interval/snapshots/2026-10-19/fts/AFG/total-2024_2025_2026-p015.json`:
`createdAt` **2026-10-19T10:03:09Z** — siebzehn Minuten vor der Lesung von Woche 1 (Commit
`a1a13ae`, 10:20 UTC) —, `paid`, 3 421 714 USD, `firstReportedDate` **2025-07-02**, `date`
2025-08-27, `parentFlowId` 359180. Er übernimmt Erstmelde- und Flussdatum seiner Elternzusage
`359180` (`commitment`, `firstReportedDate` 2025-07-02), deren Betrag im selben Zug von 0 auf
−540 USD ging und die `403006` als zweites Kind aufnahm — bei unverändertem `versionId` 1
(`updatedAt` 2026-10-19T10:03:09Z). Doppelt gezählt wird nichts: die Zusage trägt keinen Betrag.

**2. Ein bestehender Fluss, an Ort und Stelle umgeschrieben.** Fluss `396456` (`createdAt`
2026-07-22) stand am 2026-10-13 mit 8 075 370 USD, `firstReportedDate` 2026-06-29; am 2026-10-19
mit 1 342 282 USD, `firstReportedDate` und `date` **2026-10-19** — `versionId` bleibt 1,
nur `updatedAt` rückt (2026-10-19T09:57:13Z). Zwei weitere Juni-Flüsse (`396488`, `396491`)
stiegen mit `versionId` 2 leicht. Das ist der Mechanismus von Woche 4 (Fluss 385472,
`docs/2026-11-10-the-interval-woche-4.md`), hier auf der zweiten Achse.

Beide Stände bleiben bis zur Lesung vom 2026-11-16 so (`interval/snapshots/2026-11-16/fts/AFG/…`).

## Was das für das Review heißt (berichtet, keine Bewertung)

- Der Bericht von Woche 3 (`docs/2026-11-03-the-interval-woche-3.md`) hielt fest, die
  `firstReportedDate`-Achse bleibe für AFG 2025-10 bei 2025-10 geschlossen. Das stimmt, aber die
  Achse ist aber kein Erscheinungsdatum: ein Fluss, der erst im Oktober 2026 im Register auftaucht,
  zählt für Juli 2025, und ein Erstmeldedatum kann ohne neue Version um vier Monate wandern. Wer
  die Achse als „wann wusste die Welt davon" liest, liest mehr, als sie trägt.
- Die Grundrate B6 wird aus dem jeweils aktuellen Register gerechnet und bewegt sich daher mit den
  Rückschreibungen der Quelle; der Nachtrag hat das nicht festgehalten. Eine gegen das Register vom
  Tag des Nachtrags eingefrorene Grundrate wäre eine Frage für das Review, nicht für diese Nacht.
- Ein eigenes `createdAt` je Fluss liegt in jeder bewahrten Seite. Ob eine dritte Achse
  „erstmals im Register gesehen" (aus den Snapshots, nicht aus der Quelle) künftig mitgezählt
  wird, ist eine Änderung am Instrument und bleibt dem Maintainer.

## Bewusst nicht

Kein Abruf; `practice/`, `verify.py`, `interval/experiment.json`, `interval/register.json` und die
früheren Dokumente unverändert — auch die Vermutung im Fensterabschluss bleibt stehen und wird
hier korrigiert. Keine natürliche Person, keine Organisation als Geberin benannt.
