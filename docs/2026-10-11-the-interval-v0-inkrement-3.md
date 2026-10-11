# The Interval — V0, Inkrement 3: Geld-Reihe M und Antwort t1 (2026-10-11)

**Stufe:** V0, Inkrement 3 von 6 (`docs/2026-10-04-kandidat-the-interval.md` §6). Go: 2026-10-04.

**Gebaut:** `practice/src/practice/interval/money.py`, reine Funktionen ohne Netz und ohne Wanduhr.
Tests in `practice/tests/test_interval_money.py` (13, konstruierte Flüsse, dazu eine Prüfung am
committeten Sudan-Snapshot). `sources.fts_url` verweigert jetzt eine Jahresspanne (Test angepasst
in `practice/tests/test_interval_sources.py`).

**Die Grenzfrage ist entschieden, durch eine Probe** (`interval/snapshots/2026-10-11/fts/SOM/probe-boundary-*.json`,
je eine Seite mit `limit=1`, Manifest daneben). Somalia:

| Abfrage | Flüsse | Eingang (FTS-eigenes Total) |
|---|---|---|
| `year=2011` / `2012` / `2013` | 805 / 622 / 584 | $1 356M / $927M / $723M |
| `year=2011,2012,2013` | 1 912 | $2 798M |
| `year=2011-2013` | 13 246 | $18 801M |
| ohne `year` | 13 246 | $18 801M |

Die Spanne ist **kein Filter**: FTS übergeht sie und liefert alle Jahre. Die Kommaliste ist die
mehrjährige Grenze; sie hat 99 Flüsse weniger als die drei Einzeljahre zusammen, weil ein Fluss
über mehrere Jahre nur einmal erscheint. Daraus: Die Grenze einer Episode ist immer eine
Kommaliste, und eine Spanne wird schon beim Bau der URL abgelehnt. Die 13 229 der Probe vom
2026-10-09 passen zu derselben ungefilterten Menge, zwei Tage älter (nicht nachgeprüft: jene
Probe ist nicht gesichert).

**Entscheidungen**
- **Fenster:** zwölf Monate vor t0 (Basis) bis elf Monate danach (Horizont). Die Jahre dieses
  Fensters sind die Grenze (`boundary_years`, für t0 = 2022-03: `2021,2022,2023`).
- **Gezählt** wird, was eingehend über die Grenze geht (`boundary` incoming), Status paid oder
  commitment, jede Flussart, auch Parked und Pass through. Genau das zählt FTS in seinem eigenen
  `flowCount`: Sudan 2024 FSC 175 von 175 (Snapshot 2026-10-09), Somalia 2021–23 FSC 407 von 407
  (Snapshot 2026-10-11). Die Summen liegen nahe, aber nicht gleich: $801,4M gegen $803,2M und
  $2 358,8M gegen $2 347,5M. Die Reihe behauptet nicht, das FTS-Total zu sein.
- Ein Fluss, der zweimal erscheint, zählt einmal, mit der höchsten `versionId`.
- **Zwei Zeitachsen:** `date` (geflossen) und `firstReportedDate` (bekannt). Monate ohne Fluss
  sind null, nicht fehlend.
- **t1(k):** der erste Monat ab t0 mit M ≥ k × Median der zwölf Monate davor, bis zum Horizont und
  nie über `as_of` (Monat des neuesten Snapshots) hinaus. Status `closed`, `open` (mit offener Uhr
  in Monaten gegen `as_of`), `none_in_horizon` oder `baseline_zero`: Ein Median von null hat kein
  t1, denn „überhaupt Geld" ist keine Antwort. Der Halbzeit-Monat wird nur bei vollständigem
  Horizont angegeben.
- FSC gegen Total ist keine Eigenschaft der Funktion, sondern der Flussmenge, die man ihr gibt.
  Das Register (Inkrement 4) führt beide Mengen nebeneinander.

**Lesung zur Kontrolle (nicht als Record, das Register kommt mit Inkrement 4):** Somalia, Beginn
2022-03 bei θ = 10 % (Inkrement 2), FSC, Grenze `2021,2022,2023`, Snapshot
`interval/snapshots/2026-10-11/fts/SOM/fsc-2021_2022_2023-p00{1,2,3}.json` (3 Seiten, vollständig).
Basis-Median $40,8M (geflossen) und $24,8M (bekannt). t1 = 2022-05 auf beiden Achsen und für
k = 2 wie k = 3: **Lücke zwei Monate.** Die Hälfte des Zwölfmonatsgelds war im Juni 2022 geflossen
und erst im August öffentlich bekannt. Die Ländertotal-Gegenprobe ist noch nicht gesichert.

**Was das nicht ist:** keine Aussage über Geber, Angemessenheit oder Ursache. Eine Kontrolle
an einer Episode ist kein Befund.

**Nächstes Inkrement (4):** das Register `interval/register.json` (Episoden × Gitter, FSC und
Total, Doppelblock-Vermerk `blocks` > 1, Treiber-Vermerk aus `interval/drivers.json`) und die
Erweiterung von `verify.py`, die es aus den Snapshots nachrechnet. Dafür braucht es pro Beginn
zwei FTS-Abfragen (FSC und Total) mit der Kommaliste aus `boundary_years`.
