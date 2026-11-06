# The Synthetic Flood — Prüflesung `control-check-v1` und `wordlist-v3` (2026-11-06)

**Stufe:** V0, der Schritt, den `docs/2026-11-05-synthetic-flood-kontrollpruefung.md` festgelegt hat
(„Eine Lesung auf `eutils.ncbi.nlm.nih.gov`, nur Zählanfragen … ≈ 113 Anfragen“). **Anlass:** Der
Fokus wartet — The Interval liest Woche 4 erst am Montag 2026-11-09, Planetary Listening wartet auf
das Review des Maintainers (`REQUESTS.md` 2026-11-04). Die Lesung fällt unter die
Selbstentscheidung vom 2026-11-02 (`REQUESTS.md` 2026-10-30, weiter offen für Widerspruch).

## Was gelesen wurde

`python -m practice.syntheticflood.controlread --repo-root . --date 2026-11-06`
(`practice/src/practice/syntheticflood/controlread.py`), 07:38:57–07:41:47 UTC:
8 Jahressummen 2018–2025, 19 Kontrollen × 2023–2025 (ohne `reduced`), 6 Kandidaten × 2018–2025 —
**113 Zeilen, 114 Anfragen, 1 × 429** (vom Client zu 200 wiederholt), **0 fehlend**. Jede Antwort war
das kanonische Zähldokument; gespeichert sind Anfrage, Zahl und SHA-256, keine Bytes, kein Text.
Record: `syntheticflood/controlcheck/2026-11-06.json`.

## Befund

Regel und Band unverändert (1,2; ≥ 50 Abstracts; Linie 2018–2022 aus
`syntheticflood/baseline/wordlist-v2.json`, für die Kandidaten aus den heutigen Basisjahren):

| | Wörter | Verhältnis 2023 / 2024 / 2025 |
|---|---|---|
| **gefallen** | `effect` | 0,9858 / 0,9193 / **0,8029** |
| | `levels` | 1,0216 / 1,1436 / **1,2254** |
| | `observed` | 1,0345 / 1,1671 / **1,2549** |
| **gestrichen** (Regel) | `reduced` | — (Befund 2026-11-03) |
| **bestanden** | 16 übrige Kontrollen | 0,8416 (`outcome` 2025) bis 1,0882 (`clinical` 2025) |
| **Kandidaten** | `samples`, `groups`, `cases`, `performed`, `total`, `age` | alle sechs `stable` auf 2018–2022 (1,0221–1,1572) und bestanden |

`compose` ergibt 16 behaltene + 4 ergänzte (`samples`, `groups`, `cases`, `performed`) = **20**;
`total` und `age` bestehen, werden aber nicht gebraucht (Ziel erreicht). Daraus
**`syntheticflood/wordlists/wordlist-v3.json`**: `fixed` und `pool` Wort für Wort aus `wordlist-v2`,
`wordlist-v1/v2` unberührt.

Gelesen, nicht gedeutet: `effect` fällt, `levels` und `observed` steigen nach 2022 wie `reduced` —
alle drei bleiben auf 2018–2022 stabil, gehen erst danach von ihrer Linie. Einige bestandene Wörter
neigen sich innerhalb des Bandes (`outcome` 0,84, `performed` 0,84, `total` 0,86, `patients` 0,90 in
2025). Die Prüfung sagt über Kontrollen etwas, nicht über maschinell geschriebene Sprache.

## Offen gelegt: ein Fehler der ersten Auswertung, vor dem Commit behoben

Die erste Auswertung des Laufs legte die Jahressumme unter dem Schlüssel `"total"` ab — und `total`
ist selbst ein Kandidatenwort. Dessen Zählung überschrieb die Summe; alle 19 Kontrollen fielen mit
Verhältnissen um 6,5, kein `wordlist-v3` entstand. Die Zeilen (Anfragen, Zahlen, Hashes) waren
richtig; falsch war nur die Ableitung. Behoben: die Summe steht unter `None`
(`counts_from_rows`), die Auswertung wurde **aus den gespeicherten Zeilen neu gerechnet, ohne eine
weitere Anfrage**. Die Zeile des Laufs in `autonomy/log.jsonl` (07:41:47) trägt noch die falsche
Auswertung; die Korrekturzeile danach verweist auf sie. Test:
`test_the_word_total_is_never_the_cohort_total`.

Die Basisjahressummen von heute weichen von denen des 2026-10-22 minimal ab (2020: 1 434 703 statt
1 434 647; Nachträge der Quelle). Kontrollen nutzen die committete Linie, Kandidaten die heutige —
so wie die Regel es vorsieht.

## Gehalten

`verify.py` `check_syntheticflood_controlcheck`: jede Zeile folgt dem Leseplan der Regel und ist an
den SHA-256 ihrer Antwort gebunden; jede Prüfung, die Kandidaten-Basislinie und die
Zusammensetzung werden **unabhängig** von `controlcheck.py` neu abgeleitet; der Nachfolger
`wordlist-v3` muss genau die Zusammensetzung tragen. Tests
`practice/tests/test_syntheticflood_controlread.py` (9), davon drei, die zeigen, dass der Verifier
beißt.

## Nächster Schritt

Kohorte 2026-09 auf `wordlist-v3` lesen (≈ 167 Anfragen) — erst dafür braucht `wordlist-v3` eine
Basislinie: die fünf Basisjahre auf der neuen Liste (`baseline-v1`, ≈ 840 Anfragen) oder, sparsamer,
nur die vier neuen Kontrollen (deren Basisjahre liegen heute schon vor). Welche der beiden, legt der
nächste Schritt **vor** einer Anfrage fest. Kein `excess-v2`, kein Workflow vorher. An einem Abend,
an dem der Fokus wartet.

## Bewusst nicht

Keine Änderung an `wordlist-v1/v2`, `baseline-v1`, `excess-v1`, `revision-v1`, `control-check-v1`
oder an einer Lesung. Keine Ableitung einer Kohorte auf `wordlist-v3`. Register B bleibt zu
(`REQUESTS.md` 2026-10-20).
