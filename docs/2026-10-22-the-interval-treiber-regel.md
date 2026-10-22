# The Interval — Treiber-Regel `drivers-grfc-v1` als Code (offener Punkt ohne Gate)

**Datum:** 2026-10-22 (vierter Pass) · **Stufe:** E-EXPERIMENT läuft (Woche 1 gelesen,
`interval/readings/2026-10-19.json`; nächste Woche Montag 2026-10-26). · **Bezug:** Audit
`docs/2026-10-22-the-interval-treiber-quelle-audit.md` §2 (Empfehlung) und §3; Anfrage in
`REQUESTS.md` (2026-10-22): ohne Antwort schreibt der Pass zuerst die Regel als getesteten Code fest
und trägt Treiber erst nach Fensterschluss (2026-11-15) ein. Bis zu diesem Pass ist keine Antwort
eingegangen; dieser Schritt ist also der, der nicht auf das Gate wartet.

## 1. Was neu ist

- **`practice/src/practice/interval/drivers.py`** — die Regel, wie im Audit §2 vorgeschlagen, ohne
  Abweichung:
  1. Zeile mit `ISO Code 3` = Land und `Year of reference` = Jahr von t0; bei zwei Zeilen die spätere
     Ausgabe (`2025` < `2025 MYU` < `2026`; eine andere Schreibweise der Ausgabe wird abgelehnt, nicht
     geraten). Keine Zeile → `unassigned`.
  2. Label = Primärtreiber: `Conflict/insecurity` → `conflict`, `Economic shocks` → `economic`,
     `Weather extremes` → `weather`. Alles andere (`None`, `N/A`, leer, ein unbekanntes Wort) →
     `unassigned`. `drought` und `mixed` vergibt die Regel nie.
  3. Sekundär- und Tertiärtreiber wörtlich in `secondary` (auch die Schreibvariante
     `Conflict/Insecurity` bleibt, wie sie in der Datei steht); `N/A`, `None`, leer entfallen.
  Die xlsx-Datei wird mit der Standardbibliothek gelesen (erstes Blatt, geteilte und Inline-Strings),
  das Paket bleibt ohne Abhängigkeiten (`practice/pyproject.toml`). Ein Eintrag trägt `rule`,
  `grfc_file`, `source_sha256`, `primary`, `secondary`, `grfc_edition`, `year_of_reference`;
  `source` ist der Dateipfad, wenn ein Treiber vergeben ist, sonst `null`. Aufruf
  `python -m practice.interval.drivers --repo-root . --source <xlsx>` **druckt** die Ableitung für alle
  Episoden von `interval/register.json`; er schreibt nichts.
- **Neuer Wert `weather`** in `DRIVER_VALUES` (`practice/src/practice/interval/register.py`) und
  `IV_DRIVERS` (`verify.py`). `interval/register.json` ändert sich dadurch nicht (alle acht Einträge
  bleiben `unassigned`; `verify.py` grün).
- **`verify.py` `check_interval_drivers`** — für jeden Eintrag in `interval/drivers.json`, der
  `drivers-grfc-v1` nennt: Datei committet, SHA-256 gleich, `source` gleich der Datei, und Label,
  Primär-, Sekundärtreiber, Ausgabe und Jahr aus den Bytes **unabhängig nachgerechnet** (eigener Leser,
  ohne das `practice`-Paket). Ein unbekannter Regelname wird abgelehnt. Einträge ohne `rule` bleiben
  der bisherigen Prüfung in `check_interval` überlassen.
- **Tests** `practice/tests/test_interval_drivers.py` (18): konstruierte Arbeitsmappen (geteilte und
  Inline-Strings), spätere Ausgabe gewinnt, keine Zeile / `None` / `N/A` / unbekannter Primärtreiber →
  `unassigned`, nie `drought` oder `mixed`, unbekannte Ausgabe abgelehnt; die bewahrte GRFC-Datei als
  feste Regression; Gleichheit von Paket- und `verify.py`-Ableitung auf dieser Datei; `verify.py` lehnt
  sieben Arten von Handänderung ab.
- `interval/drivers.json`: nur der `about`-Text nennt den Wert `weather` und die Regel; **kein
  Treiber-Eintrag**.

## 2. Was die Regel auf der bewahrten Datei ergibt (nicht eingetragen)

Auf `interval/probes/2026-10-22/hdx/grfc_afi_database_2016-2025_september_update.xlsx`
(SHA-256 `44de7226…`, vollständig in `interval/probes/2026-10-22/manifest.json`):

| Episode | Label | Ausgabe | Sekundär (wörtlich) |
|---|---|---|---|
| AFG 2021-10 | conflict | 2022 | — |
| AFG 2025-10 | economic | 2025 MYU | Weather extremes, Conflict/insecurity |
| DJI 2023-04 | economic | 2024 | Weather extremes |
| SDN 2023-06 | conflict | 2024 | Economic shocks, Weather extremes |
| SOM 2022-03 | weather | 2023 | — |
| SOM 2024-08 | weather | 2025 | Conflict/insecurity, Economic shocks |
| SOM 2026-01 | unassigned | — | — (keine Zeile mit Bezugsjahr 2026) |
| YEM 2025-06 | economic | 2025 MYU | Conflict/Insecurity, Weather extremes |

Sieben von acht, wie das Audit erwartete. Die Tabelle steht als Regression in den Tests, damit eine
Änderung der Regel sichtbar wird; sie ist **kein** Eintrag. Wie im Audit offengelegt: die Zeilen
waren vor der Regel gelesen, die Regel ist nicht blind — sie ist deshalb mechanisch und unverändert
gegenüber dem Audit-Vorschlag.

## 3. Bewusst nicht

- Kein Eintrag in `interval/drivers.json`, keine Neuberechnung von `interval/register.json`. Die
  Anfrage in `REQUESTS.md` (2026-10-22) bleibt offen; ohne Antwort folgen die Einträge nach dem
  2026-11-15, in einem eigenen, datierten Schritt.
- Kein Abruf heute. Keine neue Fassung der GRFC-Datei, keine zweite GRFC-Datei.
- Kriterien, Fenster, Lese-Workflow und Tally (`practice/src/practice/interval/experiment.py`)
  unberührt; B5 bleibt „berichtet, keine Latte“.
