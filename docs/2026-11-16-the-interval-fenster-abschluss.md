# The Interval — das Fenster ist geschlossen, die Treiber sind eingetragen (2026-11-16)

**Stufe:** E-EXPERIMENT, Fenster geschlossen am 2026-11-15 (vier ISO-Wochen, Lesungen 2026-10-19,
10-26, 11-02, 11-09). **Art:** Abschlusszählung aus dem committeten Record, berichtet — keine
Entscheidung; das Review gehört ab heute dem Maintainer (Kriterien §1, §5). Dazu ein datierter
Schritt, der auf nichts wartet: die Treiber-Einträge nach Regel `drivers-grfc-v1`, wie in
`REQUESTS.md` (2026-10-22) für die Zeit nach dem Fenster angekündigt. Kriterien:
`docs/2026-10-14-the-interval-e-experiment-kriterien.md`, Nachtrag
`docs/2026-10-17-the-interval-e-experiment-nachtrag.md`, maschinenlesbar `interval/experiment.json`.
Kein Abruf heute; jede Zahl unten steht in einer committeten Datei.

## 1. Die Zählung

`python -m practice.interval.experiment --repo-root .` am 2026-11-16, vor dem Treiber-Schritt
(`closed: true`, Wochen fällig 4 von 4, Episoden je Lesung 8 / 8 / 8 / 8):

| # | Latte | Befund | |
|---|---|---|---|
| A1 | 4 von 4 Wochen | 4 von 4, `A1_missing_weeks: []` (Lesungen `interval/readings/2026-10-19.json`, `2026-10-26.json`, `2026-11-02.json`, `2026-11-09.json`) | erfüllt |
| A2 | ≤ 1 Lesung mit Ausfall | 0 (`A2_readings_with_failures: {}`) | erfüllt |
| A3 | 0 × 429 | 0 (`A3_http_429: []`) | erfüllt |
| A4 | `verify.py` grün auf jeder Fensterlesung | grün (CI-Gate jeder Lesung; heute grün auf diesem Commit) | erfüllt |
| A5 | 0 Anfragen an das FEWS-NET-Data-Warehouse | 0 (`test_sources_never_name_the_fews_net_warehouse`, `practice/tests/test_interval_experiment.py`) | erfüllt |
| B1 | eingefroren bleibt eingefroren | 0 Bewegungen (`B1_frozen_moves: []`) | ohne Verstoß |
| B3 | Gitter vollständig | das Register wird von `verify.py` (`check_interval`) aus den Snapshots nachgerechnet; keine stumme Lücke gemeldet | ohne Verstoß |
| B4 | offene Zelle ändert sich nur mit neuem Snapshot | Wochen 1–2, 2–3, 3–4 je geprüft: nur die vier offenen Abfragen und der IPC-Zeiger änderten sich, jeweils mit neuem Snapshot (`discovery/AGENDA.md` 2026-10-27, `docs/2026-11-03-the-interval-woche-3.md`, `docs/2026-11-10-the-interval-woche-4.md`) | ohne Verstoß |
| C | keine Person, keine Schuldzuweisung, keine Bühne | **verfehlt per Entscheidung** — die Website-Sperre wurde am 2026-10-29 aufgehoben (`docs/2026-10-29-sperre-aufgehoben.md`); die Kriterien bleiben, C zählt als verfehlt. Personen und Schuldzuweisungen: heute nicht gesondert durchsucht; die vier Wochendokumente nennen keine | verfehlt (Verweis) |

**B — berichtet, ohne Latte:**

- **B2 Episoden-Wechsel:** keine (`B2_episode_changes: []`). Ein neuer IPC-Snapshot im Fenster
  (`interval/snapshots/2026-11-09/ipc/`, 42 angefügte Zeilen COD/LBN/UGA) erzeugte keinen Beginn.
- **B5 Treiber:** im Fenster alle acht `unassigned`; ab heute sieben eingetragen (§2).
- **B6 Grundrate:** FSC·date·k=2 43/77 Placebo gegen 3/7 Beginne, wie im Nachtrag. Sieben der acht
  Zellen stehen wie in der Nachtrags-Tabelle; **total·firstReportedDate·k=2 zählt heute 36/77 statt
  35/77** (Beginne 4/7 unverändert). Die Grundrate wird aus dem aktuellen Register gerechnet, und die
  offenen AFG-Abfragen haben sich im Fenster bewegt (Wochen 3 und 4); welcher Monat hinzukam, ist
  heute nicht nachverfolgt.

Nach §2: **A1–A5 erfüllt · B1, B3, B4 ohne Verstoß · B2, B5 berichtet · C verfehlt per Entscheidung
vom 2026-10-29.** Welcher Ausgang aus §5 folgt, entscheidet das Review.

## 2. Treiber eingetragen — Regel `drivers-grfc-v1`, unverändert

`REQUESTS.md` (2026-10-22) blieb unbeantwortet; die dort angekündigte Folge tritt ein: die Regel war
seit dem 2026-10-22 getesteter Code (`practice/src/practice/interval/drivers.py`,
`docs/2026-10-22-the-interval-treiber-regel.md`), die Einträge folgen nach dem Fenster in einem
eigenen Schritt. Quelle: die im Audit bewahrte Datei
`interval/probes/2026-10-22/hdx/grfc_afi_database_2016-2025_september_update.xlsx` (SHA-256
`44de7226…`), kein neuer Abruf. Geschrieben mit
`python -m practice.interval.drivers --repo-root . --source <Datei>` nach `interval/drivers.json`,
dann `python -m practice.interval.register --repo-root .`.

| Episode | Treiber | Ausgabe | Sekundär (wörtlich) |
|---|---|---|---|
| AFG 2021-10 | conflict | 2022 | — |
| AFG 2025-10 | economic | 2025 MYU | Weather extremes, Conflict/insecurity |
| DJI 2023-04 | economic | 2024 | Weather extremes |
| SDN 2023-06 | conflict | 2024 | Economic shocks, Weather extremes |
| SOM 2022-03 | weather | 2023 | — |
| SOM 2024-08 | weather | 2025 | Conflict/insecurity, Economic shocks |
| SOM 2026-01 | unassigned | — | — (keine Zeile mit Bezugsjahr 2026) |
| YEM 2025-06 | economic | 2025 MYU | Conflict/Insecurity, Weather extremes |

Identisch mit der Regressionstabelle vom 2026-10-22. `interval/register.json` ändert sich nur in den
sieben `driver`-Feldern; alle Geld-Zellen, Hashes und der IPC-Zeiger bleiben gleich (Feld für Feld
verglichen vor und nach der Neuberechnung). `verify.py` `check_interval_drivers` rechnet jeden
Eintrag unabhängig aus den Bytes nach. Offengelegt wie im Audit: die Zeilen waren vor der Regel
gelesen, die Regel ist nicht blind. Ein Treiber ist die Angabe der Quelle zum Bezugsjahr, keine
Erklärung der Lücke und keine Zuschreibung (E-2).

## 3. Für das Review benannt

1. **Zwei wieder geöffnete Uhren, zwei Mechanismen.** AFG 2025-10 total·date·k=2 (Woche 3:
   Umdatierung durch die Quelle in neuen Versionen) und FSC·date·k=2 (Woche 4: ein geparkter Fluss
   schrumpft beim Weiterleiten, `versionId` bleibt 1). Kein Kriterium verletzt — beide Abfragen sind
   offen —, aber eine „geschlossene“ Antwort einer offenen Episode ist vorläufig.
2. **Ein geparkter Fluss zählt in zwei Länderlisten** (Fluss 385472, AFG und SOM). So festgelegt in
   `money.py`; ob das doppelt zählt, was einmal floss, zeigt der Record nicht.
3. **B6:** eine kurze Lücke am Beginn hebt sich in keiner Zelle deutlich von der Placebo-Rate ab
   (z. B. 43/77 gegen 3/7). Das Instrument läuft; was seine zentrale Zahl bedeutet, bleibt offen.
4. **C** zählt als verfehlt per Entscheidung des Maintainers, nicht durch einen Fund.

## Bewusst nicht

Keine Entscheidung über den Ausgang · keine Änderung an Kriterien, `money.py`, Workflow oder einer
Lesung · keine neue GRFC-Fassung, kein Abruf · keine Bühne · der wöchentliche Workflow liest weiter,
bis das Review entscheidet.
