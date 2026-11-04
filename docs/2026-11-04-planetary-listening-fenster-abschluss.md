# Planetary Listening — das Fenster ist geschlossen (2026-11-04)

**Stufe:** E-EXPERIMENT, Fenster geschlossen am 2026-11-03 (14 Nächte, Lesungen 2026-10-21 bis
2026-11-03). **Art:** Abschlusszählung aus dem committeten Record, berichtet — keine Entscheidung.
Das Review gehört ab heute dem Maintainer (Kriterien §1, §5). Kriterien:
`docs/2026-10-19-planetary-listening-e-experiment-kriterien.md`, maschinenlesbar
`planetary/experiment.json`. Kein Abruf heute; jede Zahl unten steht in einer committeten Datei.

## Die Zählung

`python -m practice.planetary.experiment --repo-root .` am 2026-11-04 (`closed: true`, Nächte fällig
14 von 14):

| # | Latte | Befund | |
|---|---|---|---|
| A1 | ≥ 13 von 14, nie zwei in Folge fehlend | 13 von 14; fehlend nur 2026-10-21 (Lauf `planetary` #6, GEOFON-Timeout, `docs/2026-10-22-planetary-listening-reparatur-ausfall.md`) | erfüllt |
| A2 | ≤ 1 Ausfallnacht, Ursache im Record | 1: 2026-11-03, Tagesdatei 204 (`planetary/readings/2026-11-03.json`, `station_day.http_status` 204, `outage: true`) | erfüllt |
| A3 | 0 × 429 | 0 | erfüllt |
| A4 | ≤ 400 KB je Nacht | 7,96–46,5 KB (Lesung plus `planetary/snapshots/<date>/`; Höchstwert 2026-10-30) | erfüllt |
| A5 | `verify.py` grün | grün auf diesem Commit (CI-Gate jeder Fensterlesung) | erfüllt |
| B6 | Detektor unverändert | 0 Änderungen (`stalta-v1`, `strong_ratio` 50, ≤ 4 Ausschnitte) | erfüllt |
| C | keine Klasse, keine Person, keine Bühne | Klassenwort-Zählung leer; `export.json` führt Planetary Listening mit `site_route: null` | ohne Verstoß |

**B — berichtet, ohne Latte:**

- **B1 Herausgeber-Attest:** vorhanden in 11 Nächten, fehlend 2026-10-23 und 2026-10-31 (der Index
  endete einen Tag zu früh, §4.1). 2026-10-21 hat keine Lesung.
- **B2 Neu-Einlagerung:** keine Ereignisse in 13 Lesungen.
- **B3/B5 Kalender:** 13 Zeilen (Tage 2026-10-21 bis 2026-11-02). Starke Impulse an sechs Werktagen;
  kein starker Impuls an Wochenenden, Fr 2026-10-30, Do 2026-10-22 und Mo 2026-11-02 (Letzterer ohne
  Tagesdatei, also kein Befund über den Tag). ISC und USGS: 0 Zeilen an jedem Tag.
- **B4 Die Uhr:** **`local`**, Δ = +57,02 min (4 Werktage vorher, 4 nachher). Die ersten starken
  Impulse lagen vor der Umstellung um 07:30–07:39 UTC, danach um 08:27–08:40 UTC (2026-10-26 bis
  10-29). Die vorab notierte Erwartung (`local`, 08:30–08:34 UTC) trifft zu, ohne Latte und ohne
  Aussage über eine Tätigkeit.

Nach §2: **A1–A5 erfüllt · B6 ohne Änderung · B1–B5 berichtet · C ohne Verstoß.** Welcher der drei
Ausgänge aus §5 folgt, entscheidet das Review.

## Für das Review benannt

1. **Die Reparatur im Fenster.** `nightly.py` wurde am 2026-10-22 geändert, damit ein Host ohne Antwort
   als Ausfallnacht geschrieben wird; Detektor, Kriterien und Workflow blieben unberührt. Ohne sie
   wäre ein zweiter Timeout eine zweite fehlende Nacht geworden.
2. **Die letzte Nacht ist die Umkehrung von §4.1.** Am 2026-11-03 um 16:08:05 UTC antwortete
   `dataselect` für den 2026-11-02 mit 204 (0 Byte), während die availability-Zeile eine Sekunde später
   den ganzen Tag attestierte (`Earliest 2026-11-02T00:00`, `Latest 2026-11-03T00:00`, `Updated
   2026-11-03T05:15:51Z`; `planetary/snapshots/2026-11-03/GE.RUE.HHZ/availability-2026-11-02.txt`).
   Bisher fehlte das Attest bei vorhandener Datei; hier fehlt die Datei bei vorhandenem Attest. Ursache
   nicht bewiesen. Kein Nachholen: das wäre ein Abruf außerhalb des Fensters.
3. **Der Workflow läuft spät** (die Lesungen 2026-10-27 bis 2026-11-03 kamen zwischen 14:23 und 18:14 UTC auf main, Commits `c0eb4a2` bis `a8886b0`; geplant 08:10 UTC).
   Das berührt keine Latte (§4.2), ist aber ein Betriebsbefund für RUNNING.

## Bewusst nicht

Keine Entscheidung über den Ausgang · keine Änderung an `nightly.py`, Detektor, Workflow oder Kriterien ·
kein Nachlesen des 2026-11-02 · keine Bühne · kein neuer Abruf.
