# The Synthetic Flood — `reduced` in den Jahren 2023–2025: ein Anstieg in Stufen ab 2024 (2026-11-03)

**Stufe:** V0, Schritt nach der M+2-Lesung (`docs/2026-11-02-synthetic-flood-v0-lesung-m2.md`, dort
als nächster Schritt vorgeschlagen: „`reduced` in den Jahreskohorten 2023–2025 lesen (6 Anfragen)").
**Anlass:** Der Fokus wartet — The Interval liest Woche 4 erst am 2026-11-09, Planetary Listening
schließt heute sein Fenster im Workflow. **Host:** `eutils.ncbi.nlm.nih.gov`, unter der
Selbstentscheidung vom 2026-11-02 (`REQUESTS.md` 2026-10-30, weiter offen für Widerspruch): nur
Zählanfragen, kein Text.

## Lesart, festgelegt vor der ersten Anfrage

Verglichen wird der Anteil `reduced[tiab]` an `hasabstract` je Jahr mit dem Basisjahr 2022 (7,901 %,
`syntheticflood/readings/2022/2026-10-22.json`) und der Kohorte 2026-09 bei M+2 (13,735 %,
`syntheticflood/readings/2026-09/2026-11-02.json`):

- **spät** — 2025 ≤ 1,2 × 2022 (≤ 9,48 %): der Anstieg liegt in 2026; Verdacht auf etwas, das nur
  junge Datensätze trifft.
- **früh** — 2023 ≥ 0,9 × 2026-09 (≥ 12,36 %): der Anstieg ist 2023 schon vollzogen.
- **schrittweise** — sonst.

Diese Lesart ist eine Klassifikation dieses einen Befunds, keine neue Regel; `excess-v1`,
`revision-v1`, `baseline-v1` und `wordlist-v2` bleiben unberührt.

## Gelesen

Sechs Zählungen, preserviert mit Manifest unter `syntheticflood/probes/2026-11-03/` (jede Antwort
byte-gleich mit `pubmed.canonical(count)`); 7 Anfragen, 1 × 429 vom Client bis 200 wiederholt,
07:38 UTC.

| Kohorte | `hasabstract` | `reduced` | Anteil | gegen 2022 |
|---|---|---|---|---|
| 2018 (10-22) | 1 186 981 | 96 906 | 8,164 % | 1,033 |
| 2022 (10-22) | 1 594 189 | 125 956 | 7,901 % | 1,000 |
| **2023** | 1 517 501 | 121 227 | **7,989 %** | 1,011 |
| **2024** | 1 559 731 | 135 604 | **8,694 %** | 1,100 |
| **2025** | 1 687 534 | 186 189 | **11,033 %** | 1,396 |
| 2026-09 (M+2) | 172 506 | 23 694 | 13,735 % | 1,738 |

**Klasse: schrittweise.** 2023 liegt auf der Basis (die Basislinie 2018–2022 fällt leicht), der
Anstieg beginnt 2024 (+8,8 % gegen 2023), wird 2025 steil (+26,9 %) und setzt sich zur Kohorte
2026-09 fort (+24,5 %).

## Was daraus folgt — und was nicht

- Die Erklärung „etwas, das nur junge Datensätze trifft" (Zeile 2 der Tabelle von Inkrement 3d) wird
  für `reduced` unwahrscheinlicher: Das ganze Jahr 2025 trägt schon den größten Teil des Anstiegs.
  Bewiesen ist damit kein Grund. Ein Wort, das in Abstracts stetig häufiger wird, ist eine Zählung,
  kein Anteil maschinell geschriebener Sprache — und bei `reduced` kann das genauso Gebrauch in
  einem Fachgebiet sein wie Stil.
- **Für das Instrument:** `reduced` ist als Kontrolle ungeeignet, weil es selbst steigt. Der Bruch
  von `excess-v1` misst also eher die Kontrolle als die Kohorte. Vorschlag, nicht heutiger Schritt:
  `wordlist-v3` mit einer Ersatzkontrolle, die in 2023–2025 nachweislich stabil bleibt — die
  Ersatzkandidaten werden vor jeder Ableitung auf denselben Jahren geprüft, nicht nach ihr gewählt.
  Das ist ein späterer Pass an einem Abend, an dem der Fokus wartet; der Widerspruch des Maintainers
  zu `REQUESTS.md` (2026-10-30) würde ihn erübrigen.
- Die Jahre 2023–2025 sind bislang nicht Teil der Basis (`baseline-v1` liest 2018–2022). Ob alle 47
  festen Wörter ab 2024 so wandern, zeigt dieser Schritt nicht; er las nur `reduced`.

## Bewusst nicht

Keine Änderung an einer Regel, Wortliste, Basis oder früheren Lesung; diese Zählungen sind eine
Sonde, keine Lesung unter `syntheticflood/readings/`. Register B bleibt zu (`REQUESTS.md`
2026-10-20); kein Afterlife-V0; keine weitere Anfrage an den Host heute.
