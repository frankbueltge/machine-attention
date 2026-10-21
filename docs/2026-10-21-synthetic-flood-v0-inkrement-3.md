# The Synthetic Flood — V0, Inkrement 3: die Basis 2018–2022 und der Stabilitätstest (2026-10-21)

**Stufe:** V0, Inkrement 3 · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), wie in
`docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`. · **Anlass:** Der Fokus wartet — The Interval
liest erst am Montag 2026-10-26 wieder (Tally ohne Lücke, B6 unverändert), Planetary Listening
erwartet seine erste Fensterlesung 2026-10-21 aus dem Workflow (08:10 UTC, zur Passzeit noch nicht
fällig). Die Frage nach einem Runner für Register B (`REQUESTS.md`, 2026-10-20) blieb über diesen
Pass unbeantwortet: Register B bleibt zu, Register A geht vor.

## Gebaut

- **Jahreskohorten:** `pubmed.cohort_term("2019")` ergibt `hasabstract AND 2019[dp]`; eine
  Jahreskohorte endet im Dezember, ihr Abstand wird von dort gezählt
  (`practice/src/practice/syntheticflood/cohort.py`, `lag`). Die Lesungen liegen wie jede
  Kohorte unter `syntheticflood/readings/<YYYY>/<datum>.json`, alle als `retrospective` markiert,
  keine als `value`. `verify.py` (`_sf_url`, `check_syntheticflood`) baut die Jahresanfrage
  unabhängig nach.
- **Die Regel, vor der ersten Basisanfrage geschrieben:** `baseline-v1` in
  `practice/src/practice/syntheticflood/baseline.py` — je Wort der Anteil an jeder Jahreskohorte
  2018–2022; `rare`, wenn ein Basisjahr weniger als 50 Abstracts zählt; `stable`, wenn der größte
  Jahresanteil höchstens das 1,5-Fache des kleinsten ist; sonst `drifting-rising` oder
  `drifting-falling` nach Richtung vom ersten zum letzten Jahr. Die Datei wurde geschrieben, bevor
  die erste Jahresanfrage lief (erste Anfrage 06:38:51 UTC, `autonomy/log.jsonl`); eine andere Regel
  ist eine neue Regel-ID, nie eine Änderung dieser.
- **Das Ergebnis als abgeleitete Datei:** `syntheticflood/baseline/wordlist-v1.json` — nennt die
  fünf Lesungen mit SHA-256, die Nenner, je Wort Zahlen, Anteile, Verhältnis und Urteil.
  `verify.py` → `check_syntheticflood_baseline` rechnet alles unabhängig aus den Lesungen nach, hält
  die Regelparameter unter ihrer ID fest und verlangt die jeweils neueste Lesung je Jahr.
  Tests: `practice/tests/test_syntheticflood_baseline.py` (8 Tests, ohne Netz; jede Regel des
  Verifikators mit einem Test, der sie bricht).

## Die Lesungen

Fünf Jahreskohorten, je 166 Wörter plus Nenner, 06:38:51–06:57:50 UTC, 839 Anfragen, 0 fehlend.
**4 × 429** (je eine in 2018, 2019, 2021, 2022), jede vom Client nach Wartezeit wiederholt und
dann mit 200 beantwortet — bei 1,2 s Abstand, also unter den 3/s ohne Schlüssel. Wie bei Register B
liegt die Grenze vermutlich an der geteilten Ausgangsadresse (nicht bewiesen); ein späterer
Workflow muss 429 als normalen Fall zählen, nicht als Ausfall.

Nenner (`hasabstract`, Publikationsjahr): 2018 1 186 982 · 2019 1 248 393 · 2020 1 434 646 ·
2021 1 582 705 · 2022 1 594 195.

| Liste | stable | drifting-rising | rare |
|---|---|---|---|
| fixed (47) | 31 | 10 | 6 |
| controls (20) | 19 | 0 | 1 |
| pool (99) | 81 | 16 | 2 |

## Befunde — Eigenschaften der Methode, keine Aussage über maschinelle Sprache

1. **Ein Kontrollwort ist tot.** `significantly` zählt in allen fünf Jahren 0 — und ebenso in
   der Lesung `syntheticflood/readings/2026-09/2026-10-19.json`. PubMed führt es als Stoppwort;
   die `[tiab]`-Suche findet es nie. Eine Negativkontrolle, die immer 0 zeigt, kontrolliert
   nichts. `wordlist-v1` bleibt unverändert (sie ist unveränderlich); das Wort fällt erst mit
   `wordlist-v2`.
2. **Zehn `fixed`-Wörter stiegen schon vor 2023.** `delve` verdoppelt sich 2018→2022 fast
   (0,0084 % → 0,0206 %, Verhältnis 2,45), `leveraging` (0,106 % → 0,226 %), die
   `showcase`-Familie, `garnered`, `nuanced`, `unveiling`, `elucidates`. Ein Überschuss gegen das
   **Niveau** der Basis würde diesen Vorlauf als maschinelle Spur zählen. Daraus folgt für die
   abgeleitete Liste: Überschuss gegen den **Trend** der Basis (wie der Nachbar, arXiv:2406.07016,
   der aus 2021–2022 extrapoliert), nicht gegen ihren Mittelwert. Das ist die Regel des nächsten
   Inkrements, heute nicht festgelegt.
3. **Sechs `fixed`-Wörter sind zu selten, um geprüft zu werden** (`boasts`, `delved`, `delves`,
   `delving`, `tapestry`, `unwavering`: in mindestens einem Basisjahr unter 50). Für sie gibt es
   keinen Basisanteil, gegen den ein späterer Anstieg gemessen werden könnte, ohne dass Rauschen
   ihn trägt.
4. **Die Kontrollen halten.** 19 der 20 Kontrollen sind stabil (Verhältnis 1,02–1,17); `patients`
   liegt bei 28,7–30,8 %.

## Nächste Inkremente

3b. `wordlist-v2`: `significantly` ersetzt durch ein stabiles, zählbares Kontrollwort; die
    Regel der abgeleiteten Liste (Überschuss gegen den Basistrend, aus dem Pool) als committete
    Regel-ID, bevor eine Kohorte nach 2022 gelesen wird.
4. Erst danach ein monatlicher Workflow (M−1, M−2, M−3).

## Bewusst nicht

Kein Wort gestrichen und keine Liste überschrieben; keine Kohorte nach 2022 gelesen (die Regel
für den Überschuss steht noch nicht); keine Aussage über einen Anteil maschinell geschriebener
Sprache; Register B nicht berührt; kein Workflow; kein Abstract, kein Titel, kein Name.
