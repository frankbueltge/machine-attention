# The Synthetic Flood — V0, Inkrement 4: der monatliche Lauf und sein Workflow (2026-11-09)

**Stufe:** V0, Inkrement 4 · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), wie in
`docs/2026-10-19-synthetic-flood-v0-inkrement-1.md` · **Anlass:** Der Fokus wartet — The Interval liest
Woche 4 heute; um 07:37 UTC lag `interval/readings/2026-11-09.json` noch nicht auf main (Wochen 1–3 liefen
10:20, 10:35, 12:54 UTC). Planetary Listening wartet auf das Review des Maintainers (`REQUESTS.md`
2026-11-04). · **Unter:** der Selbstentscheidung vom 2026-11-02 zur `robots.txt` des Hosts
(`docs/2026-11-02-synthetic-flood-v0-lesung-m2.md`; nur Zählanfragen, `tool=machine-attention`, kein
Text). `REQUESTS.md` (2026-10-30) ist weiter offen; widerspricht der Maintainer, wird
`.github/workflows/syntheticflood.yml` entfernt.

## Vorab festgelegt

Der Nächste Schritt vom 2026-11-08 nannte Inkrement 4 erst nach einem Monat ohne `control_breach` —
`syntheticflood/derived/2026-09/2026-11-08.json` ist dieser Monat. Keine Regel wurde geändert:
`wordlist-v3`, `baseline-carry-v1`, `excess-v1`, `revision-v1` sind die committeten.

## Gebaut

- `practice/src/practice/syntheticflood/monthly.py`: an einem Lesedatum D ist jede Monatskohorte ab
  `2026-09` fällig, die bei M+1, M+2 oder M+3 steht und auf `wordlist-v3` bei diesem Abstand noch keine
  Lesung hat. Jede fällige Kohorte wird einmal gelesen (`cohort.read`), bei vollständiger Lesung unter
  `excess-v1` abgeleitet (`derived.build`) und gegen die letzte frühere vollständige Lesung derselben
  Liste revidiert (`revision.build`). Eine Lesung mit fehlenden Zählungen gilt als gelesen und wird nicht
  wiederholt; ein zweiter Lauf im selben Monat stellt keine Anfrage. Jahreskohorten (Basislinie) liest der
  Lauf nie.
- `.github/workflows/syntheticflood.yml`: am 4. jedes Monats, 03:17 UTC, plus `workflow_dispatch`;
  Installieren, Lesen, Registrieren im Anker-Ledger, `verify.py`, Commit — derselbe Handschlag wie
  `planetary.yml` und `interval.yml`.
- Tests `practice/tests/test_syntheticflood_monthly.py` (9): Monatsrechnung über den Jahreswechsel,
  Fälligkeit auf dem committeten Baum, keine Wiederholung, Revision im Folgemonat, unvollständige Lesung
  bleibt ohne Ableitung, Reihenfolge der Workflow-Schritte, und dass der Workflow erst mit einer
  committeten Lesung seines eigenen Befehls zugelassen ist.
- `verify.py` braucht nichts Neues: Lesung, Ableitung und Revision sind Dateien der bestehenden Schemata
  und werden von `check_syntheticflood`, `check_syntheticflood_derived` und
  `check_syntheticflood_revisions` gehalten.

## Die erste Lesung des Befehls

`python -m practice.syntheticflood.monthly --repo-root . --date 2026-11-09` — fällig war genau `2026-10`
bei M+1 (2026-09 hat M+2 auf v3 seit 2026-11-08; 2026-08 liegt vor der ersten Kohorte).

- `syntheticflood/readings/2026-10/2026-11-09.json`: 167 Anfragen, 07:39:51–07:43:10 UTC, **0 × 429**,
  0 fehlend, Gesamt 154 632 Abstracts (`lag_months: 1`, `value: false`).
- `syntheticflood/derived/2026-10/2026-11-09.json` (`excess-v1`, Basislinie
  `syntheticflood/baseline/wordlist-v3.json`): **`control_breach: []`**, Kontrollen 0,7873 (`cases`) bis
  1,4121 (`associated`). 18 abgeleitete Wörter, `offering` 5,22 bis `versatile` 2,10. Gegen 2026-09 bei
  M+2: neu `versatile`, nicht mehr dabei `enduring`, `seamless`, `strategically`.
- Keine Revision: 2026-10 hat keine frühere Lesung.

Das ist eine M+1-Lesung — eine Revision, kein Wert (M+3 ab 2027-01-01). Der Vergleich zweier Kohorten bei
verschiedenen Abständen sagt nichts; er ist hier nur genannt, nicht gelesen.

## Was der Workflow tun wird

Am 2026-12-04: 2026-09 bei M+3 (der erste Wert), 2026-10 bei M+2, 2026-11 bei M+1 — etwa 500 Anfragen,
drei Ableitungen, zwei Revisionen. Danach jeden Monat drei Kohorten.

## Bewusst nicht

Kein `excess-v2`, kein neues Wort, keine Änderung an `cohort.py`, `derived.py`, `revision.py`. Register B
bleibt zu. Keine Bühne. Der Workflow ist kein Anspruch über maschinell geschriebene Texte; die Liste
beschreibt Wörter.
