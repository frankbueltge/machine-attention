# The Synthetic Flood — V0, Kohorte 2026-09 auf `wordlist-v3`: die erste Ableitung ohne Bruch (2026-11-08)

**Stufe:** V0, Schritt nach `baseline-carry-v1` (`docs/2026-11-07-synthetic-flood-basislinie-v3.md`) ·
**Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), wie in
`docs/2026-10-19-synthetic-flood-v0-inkrement-1.md` · **Anlass:** Der Fokus wartet — The Interval
liest Woche 4 erst am Montag 2026-11-09 (heute Sonntag, nichts fällig), Planetary Listening wartet auf
das Review des Maintainers (`REQUESTS.md` 2026-11-04). · **Unter:** der Selbstentscheidung vom
2026-11-02 zur `robots.txt` des Hosts (`docs/2026-11-02-synthetic-flood-v0-lesung-m2.md`; nur
Zählanfragen, `tool=machine-attention`, unter 3 Anfragen pro Sekunde, kein Text). `REQUESTS.md`
(2026-10-30) ist weiter offen.

## Vorab festgelegt

Was die Lesung bedeutet, stand vor der ersten Anfrage fest: Der Nächste Schritt vom 2026-11-07 nennt
sie und sagt, Inkrement 4 (Workflow) komme erst, wenn ein Monat ohne `control_breach` abgeleitet ist.
Keine Regel wurde für heute geändert: `wordlist-v3`, `baseline-carry-v1`, `excess-v1`,
`revision-v1` sind die committeten.

## Gelesen

`syntheticflood/readings/2026-09/2026-11-08.json` — Kohorte 2026-09 bei M+2 (`lag_months: 2`,
`value: false`) auf `wordlist-v3` (SHA-256 `9a1e1890…`), 167 Anfragen,
07:38:12–07:41:31 UTC, **0 × 429**, 0 fehlend, 166 Wörter. Gesamt 173 495 Abstracts (172 506 am
2026-11-02, +0,57 %).

## Abgeleitet (Regel `excess-v1`, unverändert)

`syntheticflood/derived/2026-09/2026-11-08.json`, Basislinie `syntheticflood/baseline/wordlist-v3.json`:

- **`control_breach: []`** — alle 20 Kontrollen innerhalb [1/1,5; 1,5]: Spanne **0,8211**
  (`patients`) bis **1,3953** (`associated`). Die vier neuen Kontrollen `samples` 0,9100,
  `groups` 0,8880, `cases` 0,8534, `performed` 0,8825.
- **Abgeleitete Liste, 20 Wörter** (Verhältnis beobachtet/erwartet, Abstracts): `offering` 5,40
  (4 477), `aligns` 4,84, `transformative` 4,57, `delineates` 4,50, `advancing` 3,99,
  `substantially` 3,66, `enhances` 3,37, `leverages` 3,16, `substantial` 3,15, `align` 2,91,
  `thereby` 2,78, `amplify` 2,60, `robust` 2,42, `strategically` 2,37, `profoundly` 2,28, `elevated`
  2,21, `navigating` 2,17, `synergy` 2,14, `enduring` 2,13, `seamless` 2,12.
- Gegen die Liste vom 2026-11-02 (`wordlist-v2`, damals `control_breach`) ein Wort anders:
  `enduring` (2,1334) statt `versatile` (2,1008) — beide an der Grenze von Rang 20; die
  Pool-Basislinie ist auf v2 und v3 dieselbe (`baseline-carry-v1`), der Tausch kommt aus den
  Zählungen der Woche.

## Revision (Regel `revision-v1`, unverändert)

`syntheticflood/revisions/2026-09/2026-11-02_2026-11-08.json` über die 162 Wörter, die beide
Lesungen teilen (die Revisionsregel vergleicht je Liste und Wort; die vier neuen Kontrollen fehlen
der früheren Lesung, `reduced`, `effect`, `levels`, `observed` der späteren): Gesamt +0,57 %,
134 `held` (Drift 0,9761 `intriguing` bis 1,0244 `revolutionizing`), 28 `thin`, **0 `moved`**.

## Wie es zu lesen ist

1. **Zum ersten Mal leitet ein Monat ohne Bruch ab.** Das ist die vorab gesetzte Bedingung für
   Inkrement 4. Es ist **keine** Aussage darüber, wie viel Sprache maschinell geschrieben ist: Ein
   Wort mit Verhältnis über 2 ist eine Zählung gegen eine Linie, kein Anteil.
2. **Konstruktion, offengelegt:** Die Kontrollen von `wordlist-v3` wurden ausgewählt, weil sie
   2023, 2024 und 2025 nahe ihrer Linie blieben (`control-check-v1`,
   `syntheticflood/controlcheck/2026-11-06.json`). Die Kohorte 2026-09 war an dieser Auswahl nicht
   beteiligt — sie ist für die Kontrollen außerhalb der Stichprobe. Dass sie hält, ist darum ein
   Befund, nicht nur ein Echo der Auswahl; die Kontrollen am Rand (`patients` 0,82, `associated`
   1,40) liegen enger am Band als der Rest.
3. **Noch kein Wert.** Nach dem Exposé zählt eine Kohorte erst bei M+3 (`VALUE_LAG = 3` in
   `practice/src/practice/syntheticflood/cohort.py`); für 2026-09 ist das ab 2026-12-01.
4. Die Revision bestätigt die Woche: zwischen M+2-Lesungen bewegt sich kein Wort.

## Nächster Schritt

Inkrement 4, wie vorab festgelegt: ein Workflow, der jede Kohorte bei M+1, M+2 und M+3 einmal liest
und mit `excess-v1` ableitet — gebaut, getestet, mit Regeln und Wortliste festgeschrieben, an einem
Abend, an dem der Fokus wartet. Er erbt die Selbstentscheidung zur `robots.txt` und fällt mit ihr:
widerspricht der Maintainer (`REQUESTS.md` 2026-10-30), wird er entfernt, bevor er ein zweites Mal
läuft. Register B bleibt zu (`REQUESTS.md` 2026-10-20). Kein `excess-v2`, kein `wordlist-v4`.

## Bewusst nicht

Keine Änderung an einer Regel, Wortliste, Basislinie oder früheren Lesung. Kein Workflow heute.
Keine zweite Lesung, keine Jahreskohorte, keine weitere Anfrage an den Host nach den 167. Nichts auf
der Bühne.
