# The Foreknown — RETIRED (2026-10-04)

**Datum:** 2026-10-04 · **Entscheidung:** Frank (Maintainer), Wortlaut privat · **Status:**
RETIRED — das Wort, das der Aufnahme-Pfad für ein ehrliches Ende vorab festgelegt hat
(`docs/2026-08-08-projekt-aufnahme.md`: „jederzeit: RETIRED“ — ehrlich beendet, Records
bleiben, Grund committet). Letzte Nacht des Notars: **2026-10-03**.

## 1. Die Frage, und warum der Notar sie nicht beantworten konnte

The Foreknown sollte festhalten, was wann angekündigt war, und die Lücke zwischen Warnung
und Reaktion messen, solange die Uhr noch läuft. Fünfzig Nächte Record zeigen, dass das mit
diesem Instrument nicht ging. Drei Gründe, jeder aus den committeten Daten nachzählbar:

1. **Die falsche Uhr.** Von 757 angekündigten Zukünften stammen **622 vom US National
   Weather Service** (seit 2026-08-23 die dritte Quelle), 115 von GDACS, 20 vom NHC. Der
   NWS kündigt lokale Flut-, Frost- und Sturmlagen Stunden bis Tage vorher an. Eine
   institutionelle Reaktion, die sich in Geld oder Aufmerksamkeit messen ließe, gibt es auf
   dieser Zeitskala nicht. Die Bühne stellte zuletzt eine Frostwarnung in Wisconsin unter den
   Satz, niemand könne später sagen, es habe keiner gewusst.
2. **Urteile ohne Gehalt.** Von 614 gemessenen Auflösungen lauten **595
   `EPISODE_ENDED`**, die Warnung lief an ihrer Quelle aus. 18 lauten `NO_ALERT_MATCH`,
   **eine einzige** `MATERIALIZED_AS_ALERT`. Was über „die Quelle hat losgelassen“
   hinausgeht, kam in fünfzig Nächten einmal vor.
3. **Reaktion ohne Zuordnung.** Die Reaktionsachse (OCHA FTS, GDELT) lag an 599
   Auflösungen an. Ihre eigenen, mitgeschriebenen Grenzen sagen, warum sie nichts tragen
   kann: Die Summen sind Jahrespläne ganzer Länder, „none of it was raised for this hazard“.
   Aufmerksamkeit ist Länder-Aufmerksamkeit, keine Gefahren-Aufmerksamkeit. Für die
   US-Warnungen, die Mehrheit, existiert kein UN-Plan.

Schon die E1-Prüfung vom 2026-08-22 war nicht bestanden. Von 97 quelloffenen Zukünften
standen damals 93 fest, bevor die Maschine hinsah (`docs/2026-08-22-foreknown-e1-review.md`).
Der Plan war, mit einer dritten Quelle und dem Reaktions-Join nachzubessern. Beides wurde
gebaut. An den drei Gründen oben hat es nichts geändert.

**Was funktioniert hat:** das Beurkunden selbst. Die Bytes sind gesichert, gehasht,
verankert, deterministisch nachgebaut, und `verify.py` hält die Kette. Der Discovery-Pass hat
44-mal das Instrument gelesen und Fehler darin gefunden, die er selbst reparierte. Acht
Sensoren hat er befördert. Die Maschine war sorgfältig. Die Frage war an die falsche Uhr
gestellt.

## 2. Was sich ändert

- **Der Notar läuft nicht mehr.** `.github/workflows/sentinel.yml` ruft
  `practice.foreknown.run` nicht mehr auf. Der Workflow erzeugt weiter Export und Momente für
  die Seite, denn Dark Ocean und Memory Hole laufen weiter und hängen daran.
- **`foreknown/RETIRED.json`** ist der maschinenlesbare Abschluss. Ihn lesen:
  - die Bühne (`stage/generate.py`: Archivzustand ohne „Right now“, ohne tickende Uhren und
    ohne Countdown, alle Zahlen aus dem Record),
  - der Export (Status `retired`, keine „under watch“-Zahlen mehr),
  - die Momente (ein letzter Moment `retirement`),
  - der Stall-Check (ein stillgelegtes Register ist `retired`, nicht `STALE`; die
    Falsifikationsklausel des Sensors hatte diese Ausnahme vorhergesehen),
  - `verify.py` (keine Nacht nach `last_night`).
- **Der Discovery-Pass** bekommt einen neuen Auftrag
  (`docs/2026-10-04-discovery-neuer-auftrag.md`). Er wartet nicht mehr The Foreknown,
  sondern treibt neue Projekte durch den Aufnahme-Pfad. Den stillgelegten Notar darf er nicht
  „reparieren“.

## 3. Was bleibt

Nichts wird gelöscht und nichts zurückgebaut. Registry, Snapshots, Auflösungen,
Reaktions-Lesungen, Vorschläge und Anker bleiben, wie sie in der letzten Nacht standen. Die
Bühne unter frankbueltge.de/attention bleibt als Archiv erreichbar, mit jedem Dossier. 149
Zukünfte standen in der letzten Nacht an ihrer Quelle offen. Sie bleiben so stehen und
bekommen kein nachträgliches Urteil.

## 4. Was aus der Frage wird

Die Frage nach der Lücke zwischen Warnung und Reaktion bleibt richtig. Sie gehört nur an eine
Uhr, auf der Reaktion messbar ist: langsame Ernährungskrisen. Dort werden Projektionen
(FEWS NET, IPC) Monate vorher veröffentlicht, und das Geld (OCHA FTS) kommt messbar später
oder nicht. Der Kandidat dafür steht in `docs/2026-10-04-kandidat-the-interval.md`.
