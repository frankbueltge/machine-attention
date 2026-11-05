# The Synthetic Flood — Regel `control-check-v1`: welche Kontrolle trägt nach 2022? (2026-11-05)

**Stufe:** V0, Schritt nach dem Befund vom 2026-11-03 (`docs/2026-11-03-synthetic-flood-reduced-jahre.md`,
dort vorgeschlagen: „`wordlist-v3` mit einer Ersatzkontrolle, die in 2023–2025 nachweislich stabil
bleibt — die Ersatzkandidaten werden vor jeder Ableitung auf denselben Jahren geprüft, nicht nach ihr
gewählt"). **Anlass:** Der Fokus wartet — The Interval liest Woche 4 erst am Montag 2026-11-09
(`discovery/AGENDA.md`), Planetary Listening wartet auf das Review des Maintainers (`REQUESTS.md`
2026-11-04). **Keine Anfrage an irgendeinen Host heute.**

## Warum eine Regel vor der Lesung

`reduced` war auf 2018–2022 stabil (Verhältnis 1,0338, `syntheticflood/baseline/wordlist-v2.json`)
und stieg danach (2024 und 2025, Sonde `syntheticflood/probes/2026-11-03/`). Damit ist keine der
übrigen 19 Kontrollen für die Jahre nach 2022 bewiesen — sie wurden nie dort gelesen. Ein bloßer
Tausch von `reduced` gegen ein anderes Wort würde dieselbe Lücke wiederholen. Deshalb prüft der
nächste Schritt **alle** Kontrollen und eine fest benannte Kandidatenliste auf 2023–2025, und die
Prüfung samt Zusammensetzung von `wordlist-v3` ist heute als Code festgelegt, bevor eine einzige
dieser Zählungen existiert.

## Die Regel (`practice/src/practice/syntheticflood/controlcheck.py`)

- Je Wort: Linie der Anteile 2018–2022 (wie `excess-v1`), extrapoliert auf 2023, 2024, 2025;
  Verhältnis beobachtet/erwartet.
- **Bestanden**, wenn das Wort in `baseline-v1` `stable` ist, in jedem Prüfjahr ≥ 50 Abstracts zählt
  und jedes Verhältnis in **[1/1,2; 1,2]** liegt.
- **Warum 1,2 und nicht 1,5:** Auf den festgeschriebenen Zählungen liegt `reduced` bei 1,0247 /
  1,1266 / 1,4445 (2023 / 24 / 25) — mit dem Band von `excess-v1` (1,5) hätte es in jedem Prüfjahr
  bestanden und trotzdem die Kohorte 2026-09 gebrochen (1,821). Ein Prüfband gleich dem
  Nutzungsband hätte das Wort durchgelassen, das den Bruch verursacht. Der Test
  `test_the_committed_reduced_counts_fail_the_check_but_pass_the_use_band` rechnet das aus den
  committeten Bytes nach.
- **Zusammensetzung:** die bestehenden Kontrollen, die bestehen, in ihrer Reihenfolge, ohne
  `reduced`; dann die Kandidaten, die bestehen, in festgelegter Reihenfolge, bis wieder 20 erreicht
  sind. Bestehen insgesamt weniger als 15, entsteht kein `wordlist-v3` — das wird berichtet, nicht
  repariert.
- **Kandidaten**, gewählt vor jeder ihrer Zählungen: `samples`, `groups`, `cases`, `performed`,
  `total`, `age` — Inhaltswörter desselben Registers, auf keiner Liste von `wordlist-v2`, keines auf
  der veröffentlichten Stoppwortliste von PubMed (der Fehler von `significantly`,
  `docs/2026-10-21-synthetic-flood-v0-inkrement-3.md`). Ein Kandidat braucht wie jede Kontrolle
  einen `baseline-v1`-Eintrag; seine fünf Basisjahre werden mit den Prüfjahren gelesen.

## Offen gelegt

- Die Verhältnisse der 19 übrigen Kontrollen in der Kohorte 2026-09 sind bereits im Record
  (0,676 `effect` bis 1,394 `associated`, `syntheticflood/derived/2026-09/2026-11-02.json`). Das Band
  wurde allein an `reduced` begründet, nicht an diesen Werten abgestimmt; dass einzelne Kontrollen
  daran scheitern können (`effect` liegt 2026-09 schon unter 1/1,2), ist gewollt und wird der Befund
  der Lesung sein.
- Die Regel entscheidet über Kontrollen, nicht über maschinell geschriebene Sprache. Ein Wort, das
  besteht, ist ein über 2018–2025 auf seiner Linie bleibender Zähler — mehr nicht.

## Nächster Schritt

Eine Lesung auf `eutils.ncbi.nlm.nih.gov`, nur Zählanfragen, an einem Abend, an dem der Fokus wartet:
19 Kontrollen × 2023–2025 (57), 6 Kandidaten × 2018–2025 (48), 8 Jahressummen — **≈ 113 Anfragen**.
Sie fällt unter die Selbstentscheidung vom 2026-11-02 (`REQUESTS.md` 2026-10-30, weiter offen für
Widerspruch; ein Widerspruch beendet Register A und erübrigt diesen Schritt). Erst danach:
`wordlist-v3` nach `compose`, gehalten von `verify.py`; kein `excess-v2`, kein Workflow vorher.

## Bewusst nicht

Keine Anfrage, keine Änderung an `wordlist-v1/v2`, `baseline-v1`, `excess-v1`, `revision-v1` oder
einer Lesung. Register B bleibt zu (`REQUESTS.md` 2026-10-20). Kein Eintrag in `verify.py` heute:
die Regel erzeugt noch keinen Record; sie wird gehalten, sobald ihre erste Prüfung committet ist.
