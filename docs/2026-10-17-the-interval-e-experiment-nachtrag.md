# The Interval — E-Experiment: Nachtrag zu den Abnahmekriterien (2026-10-17)

**Bezug:** `docs/2026-10-14-the-interval-e-experiment-kriterien.md` §0 — Änderungen sind bis zum
Tag vor der ersten Fensterwoche (2026-10-19) als datierter Nachtrag mit Begründung erlaubt,
`interval/experiment.json` und seine Prüfsummen im selben Commit. Dies ist dieser Nachtrag; er
bindet mit seinem Commit, wie das Hauptdokument. Das Hauptdokument bleibt unverändert (seine
Prüfsumme in `experiment.json` ebenso); dieser Nachtrag steht unter `addenda` mit eigener
Prüfsumme, und `verify.py` (`check_interval_experiment`) scheitert, wenn er nach dem
Fensterbeginn datiert ist oder sich ohne seine Prüfsumme ändert.

**Anlass:** der Eintrag des Hauses in `REQUESTS.md` vom 2026-10-17 („three things worth
knowing“), ein Angebot, kein Auftrag. Alle drei Punkte sind hier beantwortet.

## 1. B6 — Basisrate (neu, berichtet, keine Latte)

**Befund des Hauses, nachgerechnet.** Die Regel t1(k) schließt an Placebo-Beginnen — jedem
anderen Monat des Beginnjahres — etwa so oft binnen eines Monats wie an den echten Beginnen.
Der Pass hat das mit der eigenen Zählung (`base_rate` in
`practice/src/practice/interval/experiment.py`) aus dem committeten Register
(`interval/register.json`, Stand 2026-10-13, `as_of` 2026-10) nachgerechnet; die Zahlen stimmen
Zelle für Zelle mit der Tabelle des Hauses überein:

| Zelle | Placebo, Lücke ≤ 1 | echte Beginne, Lücke ≤ 1 |
|---|---|---|
| FSC · date · k=2 | 43 von 77 | 3 von 7 |
| FSC · date · k=3 | 31 von 77 | 3 von 7 |
| FSC · firstReportedDate · k=2 | 37 von 77 | 3 von 7 |
| FSC · firstReportedDate · k=3 | 29 von 77 | 2 von 7 |
| Total · date · k=2 | 30 von 77 | 3 von 7 |
| Total · date · k=3 | 21 von 77 | 2 von 7 |
| Total · firstReportedDate · k=2 | 35 von 77 | 4 von 7 |
| Total · firstReportedDate · k=3 | 27 von 77 | 3 von 7 |

**Was B6 ist.** Für jede Episode, deren Fenster drei Jahre umspannt (sieben von acht; Somalia
2026-01 hat kein volles Beginnjahr in seiner Grenze und fällt aus beiden Spalten), wird dieselbe
Regel — dieselben Seiten, dieselbe Grundlinie von zwölf Monaten, derselbe Horizont, dasselbe
`as_of` — an jedem Monat des Beginnjahres gerechnet; der echte Beginn ist keine Placebo-Stelle.
Gezählt wird je Zelle (Set × Zeitachse × k), wie oft die Lücke geschlossen und ≤ 1 Monat ist,
bei Placebo und bei den echten Beginnen. Die Zählung liest nur committete Seiten, holt nichts und
kann A3 nicht berühren.

**Wie B6 berichtet wird.** Der Workflow baut das Register jeden Montag neu und committet es mit
der Lesung; `python -m practice.interval.experiment --repo-root .` gibt B6 neben A1–A3, B1, B2
aus. Der Montags-Pass vermerkt B6 in `discovery/AGENDA.md`. Die Tabelle oben ist der
Vor-Fenster-Wert, wie die Lesung vom 2026-10-13 Vor-Fenster-Kontext ist.

**Was B6 nicht ist.** Keine Latte, kein Teil von „Bestanden“: Die Formel in §2 des
Hauptdokuments bleibt wörtlich. Die Placebo-Monate stammen aus den Krisenjahren selbst; B6 ist
eine Basisrate *innerhalb* von Krisenjahren, nicht über ruhige Jahre. Sieben Beginne sind wenige.
B6 zeigt nicht, dass die Lücke den Auszahlungskalender misst; es zeigt, dass eine kurze Lücke am
Beginn, für sich gelesen, noch keine Antwort belegt. Damit erhält die Grenze, die §4.5 schon
nennt („eine Lückenmessung ohne Erklärung“), eine zweite, gemessene Seite: Das Review ab dem
2026-11-16 kann nun beurteilen, ob das Instrument läuft, **und** gegen welche Basisrate seine
zentrale Zahl zu lesen ist. Was daraus folgt, ist des Maintainers Urteil.

## 2. C — was „keine Bühne“ heißt (Klarstellung)

Der Satz in §2 C, „Bis zum Review keine Bühne: The Interval steht auf der Site nirgends“, war
wörtlich schon bei seinem Commit verletzt: Die Site nennt The Interval an drei Stellen
(`src/data/werke.ts`, `src/pages/werke/attention.astro`,
`src/pages/machine-attention/about.astro` im Repository der Site) als die Frage, die von The
Foreknown herüberkam — nach der Entscheidung vom 2026-10-04, zehn Tage vor den Kriterien. Gemeint
war eine Bühne, nicht ein Name. Der Satz gilt ab diesem Nachtrag so:

> Bis zum Review keine Bühne: keine Seite, keine Figur, keine Zahl und keine Daten von The
> Interval auf der Site. Die Nennung als aktuelle Frage dieser Praxis ist keine Bühne.

Die drei bestehenden Nennungen verletzen C damit nicht; das Haus muss nichts abnehmen. Eine Zahl
aus `interval/` auf der Site vor dem Review bliebe ein Verstoß.

## 3. Der Workflow vor Woche 1 — ein Probelauf außerhalb des Records

`interval.yml` ist noch nie gelaufen. Der Pass kann keinen Workflow auslösen, und eine committete
Probelesung vor Montag wäre eine zweite Vor-Fenster-Lesung, die §0 nicht vorsieht. Deshalb kein
committeter Probelauf. Stattdessen hat der Pass am 2026-10-17 den Lesungsschritt des Workflows
(`python -m practice.interval.weekly --repo-root .`, danach `tools/anchor.py --register` und
`verify.py`) in einer Wegwerf-Kopie des Baums ausgeführt; nichts davon ist committet:

- Lesung geschrieben: IPC neu bewahrt (die Bytes der Tabelle haben sich seit 2026-10-13
  geändert), 4 Abfragen geholt und `preserved` (Afghanistan 2025-10 und Somalia 2026-01, je FSC
  und Total), 12 eingefroren, 8 Episoden, 29 Anfragen, **0 × HTTP 429**.
- `verify.py` grün auf der Kopie; die Zählung: keine Ausfälle, keine Bewegung eingefrorener
  Abfragen, kein Episodenwechsel.

Was der Probelauf **nicht** prüft: den Workflow selbst — Checkout, Installation auf dem Runner,
den Push über `tools/commit-and-push.sh`. Diese Strecke bleibt bis Montag 04:50 UTC ungeprüft.
A1 lässt einen Nachlauf per `workflow_dispatch` in derselben Woche zählen; scheitert der erste
Lauf, ist das der Weg, und die Ursache gehört in den Record (A2).

## 4. Was sich nicht ändert

Fenster, Wochen, A1–A5, B1–B5, die Bestanden-Formel, §3–§5 des Hauptdokuments. Die einzige
Vor-Fenster-Lesung bleibt `interval/readings/2026-10-13.json`.
