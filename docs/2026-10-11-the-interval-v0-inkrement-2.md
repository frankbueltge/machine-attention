# The Interval — V0, Inkrement 2: Warn-Reihe und Beginn t0 (2026-10-11)

**Stufe:** V0, Inkrement 2 von 6 (`docs/2026-10-04-kandidat-the-interval.md` §6). Go: 2026-10-04.

**Gebaut:** `practice/src/practice/interval/warning.py`, reine Funktionen ohne Netz und ohne
Wanduhr. Tests in `practice/tests/test_interval_warning.py` (12, konstruierte Tabellen), darunter
die chronische Phase-4-Lage, die bei keiner Schwelle einen Beginn auslösen darf. Eingabe ist der
committete Snapshot `interval/snapshots/2026-10-09/ipc/ipc_global_national_long.csv`.

**Entscheidungen (alle aus dem Snapshot belegt)**
- **Nenner ist die Landesbevölkerung, nicht die analysierte Bevölkerung.** Die Spalte
  `Percentage` bezieht sich auf die analysierte Bevölkerung. Teilanalysen läsen sich sonst als
  nationaler Alarm: Sudan, Analyse Januar 2026, zweite Projektion, 21 % von 8,3 Mio. analysierten
  Personen, aber 4 % des Landes (47,5 Mio.). Die Abdeckung wird an jedem Punkt mitgeführt. Gezählt
  wird aus `Number` (Phase 4 + Phase 5); die gerundete Prozentspalte wird nie gelesen.
- **Doppelte Blöcke werden nicht summiert.** Zwei Schlüssel (Land × Analysemonat × Periode)
  tragen im Snapshot zwei Blöcke: Äthiopien Mai 2021 (beide Blöcke mit derselben Phase-5-Zahl
  352 896) und Somalia Januar 2026 (der zweite Block ist eine Beinahe-Kopie, 19 442 155 gegen
  19 442 156). Eine Summe würde doppelt zählen. Behalten wird der Block mit der größten
  analysierten Bevölkerung, und der Punkt trägt `blocks` > 1, damit das Register ihn zeigen kann.
- **W = das Maximum aus erster und zweiter Projektion.** Die aktuelle Lage zählt nicht, denn die
  Frage gilt der *Projektion*. Analysen ohne Projektion (11 von 398 im Snapshot) haben kein W und
  gelten weder als darüber noch als darunter.
- **t0(θ):** eine Analyse mit W ≥ θ nach einem Lauf von Analysen unter θ, der vom ersten Punkt des
  Laufs an mindestens sechs Monate umfasst. Liegt ein Land schon bei seiner ersten Analyse über θ,
  ist es **linkszensiert** und hat keinen Beginn, denn sein Beginn liegt vor 2020-10.

**Lesung zur Kontrolle (nicht committet als Record, das Register kommt mit Inkrement 4):**
50 Länder, 810 Blöcke. θ = 5 %: 6 Beginne, 10 Länder linkszensiert. θ = 10 %: 5 Beginne
(Afghanistan 2021-10, Sudan 2023-06, Somalia 2022-03 und 2026-01, Jemen 2025-06), 5 linkszensiert
(darunter Haiti, das seit der ersten Analyse 2021-09 durchgehend zwischen 10 % und 19 % liegt; das
ist die chronische Gegenprobe in echten Daten). θ = 25 %: kein Beginn, nur Palästina linkszensiert.
Somalia 2026-01 ist zugleich einer der beiden Doppelblock-Punkte. Das Register muss ihn markieren.

**Was das nicht ist:** keine Aussage über Geld, Geber oder Angemessenheit. Die Beginne sind die
linke Uhrhälfte. Die rechte Hälfte (Geld-Reihe und t1) kommt mit Inkrement 3.

**Nächstes Inkrement (3):** Geld-Reihe M und t1, beide Zeitachsen (`date`, `firstReportedDate`),
FSC und Total. Davor ist die Grenzfrage zu klären: FTS behandelt `year=2011,2012,2013` und
`year=2011-2013` verschieden (`docs/2026-10-09-the-interval-v0-inkrement-1.md`).
