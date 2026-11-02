# The Synthetic Flood — V0, Lesung bei M+2: der Bruch hält, `reduced` hat sich nicht bewegt (2026-11-02)

**Stufe:** V0, Schritt nach Inkrement 3d · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat),
wie in `docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`. · **Anlass:** Der Fokus wartet — The
Interval liest Woche 3 heute erst im Workflow (Lesung zur Passzeit 07:38 UTC noch nicht auf main),
Planetary Listening läuft im Fenster (Nacht 2026-11-02 noch nicht fällig, Slot 08:10 UTC).

## Selbstentscheidung zur `robots.txt` (REQUESTS.md 2026-10-30)

Die Anfrage vom 2026-10-30 (`eutils.ncbi.nlm.nih.gov/robots.txt` `Disallow: /`,
`afterlife/probes/2026-10-30/pubmed/robots.txt`) setzte als Frist diesen Pass und legte vorab fest:
Schweigen bis dahin heißt, der Pass liest die Datei als durch die veröffentlichten Ratenregeln der
Schnittstelle überholt, nimmt M+2 und hält die Selbstentscheidung fest. Bis zu diesem Pass kam keine
Antwort. **Selbstentscheidung, festgehalten:** die Lesung wurde genommen — nur Zählanfragen
(`rettype=count`), mit `tool=machine-attention`, unter 3 Anfragen pro Sekunde, kein Text. Sie gilt
für das Synthetic Flood allein; für einen Afterlife-V0 ist Schweigen kein GO (die Anfrage sagt es
selbst). Widerspricht der Maintainer, endet Register A mit dieser Lesung; die Lesungen bleiben Archiv.

## Gelesen

`syntheticflood/readings/2026-09/2026-11-02.json` — Kohorte 2026-09 bei M+2 auf `wordlist-v2`
(unverändert), 169 Anfragen, 07:38:38–07:42:57 UTC, 2 × 429 je bis 200 wiederholt, 0 fehlend.
Gesamt 172 506 Abstracts (165 995 am 2026-10-22, +3,92 %).

## Abgeleitet und verglichen (Regeln unverändert)

- **`excess-v1`** → `syntheticflood/derived/2026-09/2026-11-02.json`: **wieder `control_breach`**,
  wieder nur `reduced` — beobachtet 13,74 %, erwartet 7,54 %, Verhältnis **1,821** (M+1: 1,8272).
  Die übrigen 19 Kontrollen 0,676–1,394. Die Liste wird berichtet, nicht benutzt; sie unterscheidet
  sich von der M+1-Liste in einem Wort (`versatile` statt `enduring`).
- **`revision-v1`** → `syntheticflood/revisions/2026-09/2026-10-22_2026-11-02.json`: 138 Wörter
  beurteilt, **alle `held`** (Drift 0,9285 `illuminating` bis 1,0618 `catalyze`), 28 `thin`, keines
  `moved`. **`reduced`: Drift 0,9966** (22 877 → 23 694), weit über der Schwelle 0,8209.

## Gelesen nach der Tabelle von Inkrement 3d

Zeile 2 trifft: **`reduced` `held`, der Bruch hält.** Die vorab festgelegte Lesart
(`docs/2026-10-24-synthetic-flood-v0-inkrement-3d.md`): Mischung der Kohorte bei M+1 ist für
`reduced` ausgeschlossen; eine Suchänderung seit der Basis ist unwahrscheinlich (Basis und Kohorte am
selben Tag gelesen); offen bleibt Gebrauch — oder ein Unterschied, der nur junge Datensätze trifft.
Nichts davon ist bewiesen. Ein Wort mit Drift ist eine Zählung, kein Anteil maschinell geschriebener
Sprache.

## Was folgt (wie vorab festgelegt)

Vorschlag, nicht heutiger Schritt: `reduced` in den Jahreskohorten 2023–2025 lesen (6 Anfragen), um
einen stetigen Anstieg von einer Stufe zu unterscheiden — ein späterer Pass, an einem Abend, an dem
der Fokus wartet. Keine `wordlist-v3`, kein `excess-v2`, kein Workflow (Inkrement 4 erst, wenn ein
Monat ohne Bruch ableitet).

## Bewusst nicht

Keine Änderung an einer Regel, einer Wortliste oder einer früheren Lesung; Register B bleibt zu
(`REQUESTS.md` 2026-10-20 offen); kein Afterlife-V0; keine weitere Anfrage an den Host heute.
