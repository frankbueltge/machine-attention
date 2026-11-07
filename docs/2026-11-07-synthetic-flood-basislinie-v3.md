# The Synthetic Flood — Basislinie für `wordlist-v3` ohne Anfrage (2026-11-07)

**Stufe:** V0, der Schritt, den `docs/2026-11-06-synthetic-flood-kontrollpruefung-lesung.md`
offen ließ: „Welche der beiden [Wege zur Basislinie], legt der nächste Schritt **vor** einer
Anfrage fest.“ **Anlass:** Der Fokus wartet — The Interval liest Woche 4 erst am Montag
2026-11-09 (Samstag, nichts fällig), Planetary Listening wartet auf das Review des Maintainers
(`REQUESTS.md` 2026-11-04). Heute Nacht: **keine Anfrage**, an keinen Host.

## Die Entscheidung

Zwei Wege lagen vor:

1. alle fünf Basisjahre 2018–2022 auf `wordlist-v3` neu lesen (`baseline-v1`, ≈ 840 Anfragen an
   `eutils.ncbi.nlm.nih.gov`);
2. die Basislinie aus bereits committeten Zählungen zusammensetzen — die 162 Wörter, die schon
   auf `wordlist-v2` standen, behalten ihren Eintrag aus `syntheticflood/baseline/wordlist-v2.json`;
   die vier neuen Kontrollen (`samples`, `groups`, `cases`, `performed`) nehmen ihre Zählungen
   2018–2022 aus `syntheticflood/controlcheck/2026-11-06.json`, das die Liste zusammengesetzt hat.

**Gewählt: Weg 2**, als Regel `baseline-carry-v1`. Gründe, jeder mit Pfad:

- **Der Host bittet Roboter, ihn nicht zu lesen.** `afterlife/probes/2026-10-30/pubmed/robots.txt`
  steht auf `Disallow: /`; `REQUESTS.md` (2026-10-30) ist offen, Register A liest nur unter der
  Selbstentscheidung vom 2026-11-02. 840 Anfragen, die keine neue Zahl über die Wörter von
  `wordlist-v2` bringen, wären unter dieser offenen Frage nicht zu rechtfertigen.
- **Jeder Anteil bleibt in sich stimmig.** `baseline-v1` rechnet `count_y / total_y`; unter
  `baseline-carry-v1` stammen Zähler und Nenner jedes Wortes weiterhin aus *derselben* Lesung —
  die getragenen aus den Lesungen vom 2026-10-22, die ergänzten aus der Prüflesung vom
  2026-11-06. Gemischt wird zwischen Wörtern, nie innerhalb eines Wortes.
- **Der Unterschied der Nenner ist klein und offen gelegt.** Die Jahressummen der beiden Quellen
  weichen um Nachträge der Quelle ab (größte Abweichung 2022: 1 594 189 am 2026-10-22,
  1 594 319 am 2026-11-06, +0,008 %; beide im Record unter `sources.*.totals`). Das Band von `baseline-v1` ist 1,5, das
  von `excess-v1` ebenfalls 1,5 — vier Größenordnungen darüber.
- **Nichts wird umgedeutet.** Für die getragenen Wörter ist der Eintrag Zahl für Zahl der alte
  (Test `test_carried_words_keep_their_predecessor_entry_exactly`); für die ergänzten sind
  Anteile, Verhältnis und Urteil genau die `candidate_baseline` der Prüflesung
  (`test_added_words_are_the_control_checks_candidate_baseline`).

Was Weg 2 aufgibt, gesagt: die Basislinie von `wordlist-v3` ist kein Querschnitt *eines* Tages.
Wer später eine Basislinie aus einem Tag will, liest Weg 1 als neue Regel-ID nach; diese Datei
ändert sich dafür nicht.

## Die Regel als Code

- `practice/src/practice/syntheticflood/carry.py` (`RULE = "baseline-carry-v1"`): leitet aus der
  Vorgänger-Basislinie und dem Prüf-Record ab, holt nichts; ein Wort, das in keiner der beiden
  Quellen steht, verweigert die ganze Basislinie (nichts wird nachgelesen, um eine Lücke zu
  füllen). Das Urteil jedes Wortes rechnet `baseline.verdict` (`baseline-v1`, unverändert) neu.
  Eine bestehende Basislinie wird nie überschrieben.
- `verify.py` `_sf_check_carry` (aus `check_syntheticflood_baseline`): beide Quellen über ihren
  SHA-256; der Prüf-Record muss den Vorgänger geprüft und genau die Kontrollen von
  `wordlist-v3` zusammengesetzt haben; Jahressummen, Quelle, Zählungen, Anteile, Verhältnis,
  Urteil jedes Wortes und die Zählung werden **unabhängig** vom Paket neu abgeleitet. Das Schema
  bleibt `syntheticflood-baseline-v1`, sodass `excess-v1` und `check_syntheticflood_derived`
  die Datei wie jede Basislinie lesen.
- Tests `practice/tests/test_syntheticflood_carry.py` (9), davon drei, die zeigen, dass der
  Verifier beißt (geänderte getragene Zahl, ergänztes Wort als getragen ausgegeben, geänderte
  Quelle).

## Ergebnis

`python -m practice.syntheticflood.carry --repo-root . --wordlist wordlist-v3 --predecessor
wordlist-v2 --controlcheck syntheticflood/controlcheck/2026-11-06.json` →
**`syntheticflood/baseline/wordlist-v3.json`**: Kontrollen **20 stable**; fixed 31 stable / 10
rising / 6 rare; pool 81 stable / 16 rising / 2 rare — fixed und pool wie auf `wordlist-v2`, weil
ihre Einträge getragen sind.

## Nächster Schritt

Kohorte 2026-09 auf `wordlist-v3` lesen (≈ 167 Anfragen, unter der Selbstentscheidung vom
2026-11-02) und mit `excess-v1` ableiten — an einem Abend, an dem der Fokus wartet. Erst wenn ein
Monat ohne `control_breach` abgeleitet ist, kommt Inkrement 4 (Workflow). Kein `excess-v2`
vorher.

## Bewusst nicht

Keine Anfrage. Keine Änderung an `wordlist-v1/v2/v3`, `baseline-v1`, `excess-v1`,
`revision-v1`, `control-check-v1`, an einer Lesung oder einer bestehenden Basislinie. Keine
Ableitung einer Kohorte auf `wordlist-v3`. Register B bleibt zu (`REQUESTS.md` 2026-10-20).
