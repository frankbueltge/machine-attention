# The Interval — Woche 3: eine geschlossene Uhr öffnet sich wieder (2026-11-03)

**Stufe:** E-EXPERIMENT, Fenster läuft (Woche 3 von 4, ISO-Woche 45). **Art:** Befund aus dem
committeten Record, berichtet — kein Eingriff ins Instrument, keine Änderung an Kriterien, Register
oder Lesung. Kriterien: `docs/2026-10-14-the-interval-e-experiment-kriterien.md`.

## Was gelesen wurde

- `interval/readings/2026-11-02.json` (Commit `91f4202`, Workflow 12:54 UTC): 8 Episoden, 29 Anfragen,
  0 × 429, IPC `unchanged`, 12 Abfragen eingefroren, 4 geholt (`autonomy/log.jsonl`, Zeile
  `interval-reading` vom 2026-11-02).
- Tally `python -m practice.interval.experiment --repo-root .`: Wochen fällig 3 von 4, A1 keine
  fehlende Woche, A2 bestanden, A3 keine, B1 0 Bewegungen, B2 keine Änderung (8 Episoden in allen
  drei Lesungen), B6 unverändert (FSC·date·k=2: 43/77 Placebo gegen 3/7 Beginne).

## B4, Wochen 2–3

Verglichen wurde `interval/register.json` zwischen Commit `3a71f48` (Lesung 2026-10-26) und `91f4202`
(Lesung 2026-11-02), Zelle für Zelle. Geändert haben sich nur die vier offenen Abfragen (AFG 2025-10
und SOM 2026-01, je FSC und Total), und jede nur mit neuen Seiten unter
`interval/snapshots/2026-11-02/fts/` und neuen Hashes: **kein B4-Verstoß.**

| Abfrage | Flüsse | gezählt |
|---|---|---|
| AFG 2025-10 FSC | 356 → 357 | 284 → 285 |
| AFG 2025-10 Total | 2 975 → 2 981 | 2 296 → **2 287** |
| SOM 2026-01 FSC | 279 → 280 | 185 → 186 |
| SOM 2026-01 Total | 1 533 → 1 541 | 1 065 → 1 076 |

`as_of` aller vier Abfragen rückt von 2026-10 auf 2026-11.

## Der Befund: AFG 2025-10, Total · `date` · k=2

Diese Zelle stand in den Registern der Lesungen 2026-10-19 und 2026-10-26 auf `closed`, t1 2026-06,
Lücke 8 Monate. Seit der Lesung 2026-11-02 steht sie auf **`none_in_horizon`** (der Horizont endet
2026-09, `as_of` 2026-11 liegt dahinter). Die Basis ist unverändert (Median 126 139 403,5 USD,
Schwelle 2 × = 252,28 Mio.). Nachgerechnet aus den committeten Seiten mit
`practice.interval.money` (`parse_flows`, `money_series`), Achse `date`:

- Monat 2026-06: **269,2 Mio. → 233,0 Mio. USD** — unter die Schwelle. Alle anderen Monate des
  Horizonts bleiben, bis auf 2026-08 (85,4 → 84,4) und 2026-09 (65,4 → 65,1), gleich.
- Neun gezahlte Flüsse (Ids 358637, 358875, 359267, 359415, 361939, 361940, 361943, 361945, 361946)
  tragen in einer neuen `versionId` als `date` den Monat **2026-10 statt 2026-06**; ihr
  `firstReportedDate` bleibt 2026-05. Summe ≈ 20,8 Mio. USD, jetzt außerhalb des Horizonts.
- Zehn Zusagen (`commitment`, Ids 390613–390622; neun mit `date` 2026-06, eine 2026-09) und zwei
  weitere (401113, 401114, 2026-09) sind in der neuen Lesung nicht mehr gelistet. Die neun
  Juni-Zusagen summieren ≈ 15,5 Mio. USD. Einige liegen betragsnah an gezahlten Flüssen derselben
  Liste (z. B. 390616 5 264 830 neben 359415 5 259 990) — ob die Quelle Zusagen durch Zahlungen
  ersetzt hat, zeigt der Record nicht; es bleibt eine Beobachtung.

Die Achse `firstReportedDate` derselben Zelle bleibt `closed` bei 2025-10 (k=2) — sie sieht die
Umdatierung nicht, weil das Meldedatum der Flüsse nicht wandert.

## Was das heißt — und was nicht

- **Kriterien:** kein Verstoß. B1 gilt eingefrorenen Abfragen; diese ist offen bis zu einem Snapshot
  nach 2026-12 (Kriterien §3). B4 verlangt, dass eine offene Zelle sich nur mit neuem Snapshot
  ändert — so war es. B2 zählt Episoden, nicht Zellen.
- **Messung:** Eine Uhr, die das Register als geschlossen führte, hat die Quelle eine Woche später
  wieder geöffnet, weil Zahlungen umdatiert wurden. Genau dafür friert das Instrument erst nach der
  Gnadenfrist ein und führt zwei Zeitachsen; der Fall ist der erste im Fenster, an dem die `date`-
  Achse sich als revisionsanfällig zeigt, die Melde-Achse nicht. Ein einzelner Fall, kein Muster.
- Keine Zuschreibung (E-2): Die Umdatierung ist eine Revision der Quelle, nicht das Versäumnis eines
  Gebers, einer Agentur oder einer Regierung.

## Bewusst nicht

Keine Änderung an `money.py`, `register.json`, den Kriterien oder einer Lesung; keine Abfrage an FTS
aus diesem Container. Der Fall geht als berichteter Befund ins Review ab 2026-11-16.
