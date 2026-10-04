# The Interval — Exposé, Audit und V0-Plan (2026-10-04)

**Datum:** 2026-10-04 · **Stufe:** AUDIT abgeschlossen, **V0 freigegeben** (Franks Go vom
2026-10-04, Wortlaut privat, auf die hier benannten Quellen) · **Baut:** der Discovery-Pass,
nächtlich in Inkrementen (`docs/2026-10-04-discovery-neuer-auftrag.md`) · **Herkunft:** die
Frage von The Foreknown (`docs/2026-10-04-foreknown-retired.md` §4)

## 1. Die Frage

Wie lange braucht humanitäres Geld, um einer **projizierten** Ernährungskrise zu folgen?
Gemessen ab dem Monat, in dem für ein Land erstmals ein relevanter Bevölkerungsanteil in
**IPC Phase 4 (Emergency) oder schlimmer** projiziert wird, bis zu dem Monat, in dem das Geld
messbar ansteigt. Für jede Episode, für jedes Land, fortlaufend neu berechnet aus committeten
Snapshots.

Das ist die Frage von The Foreknown, gestellt an eine Uhr, auf der sie eine Antwort hat.
Projektionen erscheinen Monate vor dem Höhepunkt, und Finanzierung bewegt sich in Monaten. Die
Lücke zwischen beidem ist der bekannteste Vorwurf an das humanitäre System: Somalia 2011,
Hungersnot erklärt am 20. Juli, gewarnt seit dem Herbst davor. Der Prototyp unten misst dort
sechs Monate.

**Warum nur ausdauernde maschinelle Aufmerksamkeit das leistet:** Die Daten liegen öffentlich,
aber nirgends nebeneinander, nirgends mit ihrer Zeitachse und nirgends fortgeschrieben. Eine
Maschine kann für jedes Land jede Woche dieselbe Rechnung neu machen. Sie kann laufende Episoden
offen halten („Phase 4+ projiziert seit N Monaten, kein Anstieg“) und den Datenbestand sichern,
bevor er verschwindet. Für FEWS NET ist das gerade eine reale Gefahr.

## 2. Audit der Quellen (Live-Probes 2026-10-03, vollständige Notizen im Session-Protokoll)

| Quelle | Zugang | Lizenz | Urteil |
|---|---|---|---|
| **OCHA FTS** `api.hpc.tools/v1/public/fts/flow?countryISO3=…&year=…` | schlüsselfrei, Seiten à 200 über `nextLink` (Somalia 2011: 805 Flüsse, 1,5 MB) | Attribution | **in Charter**, Geld-Achse |
| FTS-Filter `&filterBy=destinationGlobalClusterCode:FSC` | funktioniert | | verlässlich erst **ab ca. 2020**: Sudan 2024 trifft das FTS-eigene Total ($801M zu $795M), Somalia 2017 nicht ($90M zu $341M) |
| **IPC auf HDX** `global-acute-food-insecurity-country-data` (`ipc_global_national_long.csv`, 402 KB; `ipc_global_area_long.csv`, 33 MB) | schlüsselfrei, CKAN-Download | **CC0** | **in Charter**, Warn-Achse. Bevölkerung je Phase für aktuelle Lage, erste und zweite Projektion, Landesebene **ab 2020-10**, 50 Länder |
| FEWS NET Data Warehouse `fdw.fews.net/api/ipcphase/` | schlüsselfrei, technisch gut | eigene Policy, Attribution, keine implizite Billigung | **nicht benutzen.** `robots.txt` sperrt alles, `llms.txt` bittet ausdrücklich, auch nicht für KI-Abrufe zu crawlen, und verweist auf Partnerzugang auf Anfrage |
| FEWS NET Shapefile-Pakete `shapefiles.fews.net/HFIC/…` | öffentlich zum Download, von `robots.txt` nicht gesperrt | wie oben | in Charter, aber nur für eine spätere Rückschau vor 2020 (GIS-Verschnitt nötig) |
| IPC-API `api.ipcinfo.org` | **401, Schlüssel nötig** | | **außerhalb der Charter** |
| HDX HAPI | **403, App-Kennung aus E-Mail nötig** | | außerhalb, und nicht nötig |

**Offengelegt:** Bevor die `llms.txt` von FEWS NET gelesen war, hat die Audit-Recherche rund 35
Anfragen an das Data Warehouse geschickt, zwei davon mit dem dort ausdrücklich unerwünschten
`ordering`-Parameter, dazu eine abgebrochene tiefe Paginierung. Danach kam keine Anfrage mehr.
Der Pass schickt keine.

**HDX und robots.txt:** HDX sperrt `/api/` und `*.csv` für Crawler (Crawl-Delay 10) und
dokumentiert zugleich die programmatische CKAN-Nutzung. V0 holt deshalb **eine** Datei **pro
Woche**, mit ehrlichem User-Agent und ETag. Die Daten ändern sich monatlich; ein täglicher Abruf
brächte nichts.

**Daraus folgt der Zeitraum von V0: 2020-10 bis heute.** Ab dann gibt es beide Achsen sauber:
IPC auf Landesebene und eine Food-Security-Kennzeichnung in FTS, die trägt. Somalia 2011 und 2017
liegen davor. Sie sind die bekannten Fälle, aber nicht der Gegenstand von V0. Eine Rückschau
über die FEWS-NET-Shapefiles oder über Partnerzugang ist eine spätere Entscheidung (§7).

## 3. Die Messung (V0)

Einheit: **Land × Episode.** Alle Eingaben sind committete Snapshots; `verify.py` rechnet alles
nach.

1. **Warn-Reihe W(Land, Analyse):** Anteil der Bevölkerung in Phase 4+ in der ersten und der
   zweiten Projektion, datiert auf den Analysemonat (`Date of analysis`). Dazu ein Merker, ob
   irgendwo Phase 5 projiziert ist.
2. **Beginn t0(θ):** die erste Analyse mit W ≥ θ nach mindestens sechs Monaten darunter, mit
   θ ∈ {5 %, 10 %, 25 %}. Ohne Schwelle hieße „irgendwo Phase 4“ in chronischen Lagen nichts.
3. **Geld-Reihe M(Land, Monat):** FTS eingehend, Status paid oder commitment, ohne Pledges.
   Abgefragt über die mehrjährige Grenze der Episode, nicht über ein Einzeljahr, weil sich die
   Buchungssemantik sonst verschiebt (Somalia Januar 2011: $150M im Einjahres-, $62M im
   Dreijahresfenster). Die Reihe wird zweimal geführt: nach `date` (wann das Geld floss) und
   nach `firstReportedDate` (wann es öffentlich bekannt war; teils Jahre später). Hauptreihe ist
   FSC-gekennzeichnet, Gegenprobe ist das Ländertotal.
4. **Antwort t1(k):** der erste Monat ab t0 mit M ≥ k × Median der zwölf Monate vor t0,
   k ∈ {2, 3}. Beschreibend dazu: der Monat, in dem die Hälfte des Zwölfmonatsgelds nach t0
   eingegangen ist. **Lücke = t1 − t0.**
5. **Ausgabe:** eine Zeile pro Episode mit dem **ganzen Sensitivitätsgitter** (θ × k ×
   Zeitachse × FSC/Total), nie eine einzelne Zahl. Jede Episode bekommt einen
   **Treiber-Vermerk** (Dürre, Konflikt, Wirtschaft, gemischt), mit Quelle. Laufende Episoden
   führen eine offene Uhr in Monaten, deterministisch gegen den letzten Snapshot und nie gegen
   die Wanduhr.

**Prototyp (Audit, Landestotals, FEWS-NET-Einheiten, nur zur Machbarkeit, nicht
committet):** Somalia 2011: 6 Monate. Somalia 2017: 1 Monat. Somalia 2022: 3–7 Monate. Sudan
2023–24: **0–10 Monate**, je nach Schwelle und Zeitachse, weil das Geld mit dem Krieg kam. Diese
Spanne ist der Grund für Gitter, Treiber-Vermerk und FSC-Hauptreihe.

## 4. Nachbarn und Daylight

- **Maxwell, Day & Hailey (2023)**, „Do Famine Declarations Really Lead to Increased Funding?“,
  Tufts FIC — https://fic.tufts.edu/wp-content/uploads/Famine-declarations-and-warnings_6-8.pdf.
  Der nächste Nachbar: 16 Hungersnot-Designationen 2011–2022, FTS vier Monate davor und danach.
  Das Ergebnis lautet „mixed“, Somalia 2011 ein Einzelfall. *Daylight:* Uhrstart bei der ersten
  Emergency-Projektion statt bei der Hungersnot-Designation, eine Lücke statt eines festen
  ±4-Monats-Fensters, fortgeschrieben statt einmalig, mit veröffentlichten Daten.
- **Hillbruner & Moloney (2012)**, „When early warning is not enough“ —
  https://fews.net/sites/default/files/documents/reports/Global_food_security_early_warning.pdf ·
  **Bailey (2013)**, „Managing Famine Risk“, Chatham House. *Daylight:* Beide stellen FTS und
  Warnungen für **einen** Fall nebeneinander, statisch.
- **„A Dangerous Delay“ (2012)** und **„Dangerous Delay 2“ (2022)**, Oxfam/Save the Children —
  erzählende Berichte ohne Datensatz.
- **Financing Flows and Food Crises** (FSIN, jährlich) — Jahressummen, keine Zeit innerhalb des
  Jahres.
- **Kim (2025)**, AAEA-Poster zu Afghanistan — ein Land, kausale Schätzung, nicht fortgeschrieben.
- **HDX HAPI** stellt IPC und FTS nebeneinander, rechnet aber keine Lücke.
- **Anticipatory Action** (CERF, Start Network, Anticipation Hub) — Mechanismen und Volumina,
  kein systemweites Lückenregister.

**Urteil:** Nichts Gleichartiges gefunden. Die Frage selbst ist gestellt worden. Der Beitrag ist
das Instrument: öffentlich, nachrechenbar, je Episode, mit der Trennung von geflossen und bekannt,
mit dem ganzen Gitter und mit offenen Uhren. **The Interval behauptet keinen neuen Befund über
Geber.** Es macht die Zeit sichtbar und prüfbar. Wie The Foreknown fällt es keine Urteile über
Angemessenheit oder Verantwortung.

## 5. Risiken

1. **Zuordnung** — das Scheitern des Foreknown. Ländergeld reagiert auf Krieg, Vertreibung und
   Seuchen. *Gegenmittel:* FSC-Hauptreihe (ab 2020 tragfähig), Treiber-Vermerk, Gitter, und eine
   Episode, deren Lücke vom Treiber dominiert ist, wird so ausgewiesen statt gemittelt.
2. **Schwellen-Empfindlichkeit:** Das Ergebnis kann Maxwell et al.s „mixed“ reproduzieren. Das
   wäre ein ehrlicher Befund, kein Scheitern des Instruments.
3. **Kenntniszeit ist rückwirkend nicht exakt:** FTS wird nachträglich revidiert, Planwerte haben
   keine Revisionsgeschichte, IPC datiert auf den Analysemonat, nicht auf die Veröffentlichung.
   Exakt ist nur, was ab dem ersten Snapshot gesichert ist. Für alles davor sagt der Record das.
4. **Wortwahl:** IPC ist nicht FEWS NET. Keine implizite Billigung, keine Logos.

## 6. V0-Plan — Inkremente für den Discovery-Pass

Jedes Inkrement ist eine Nacht, getestet, der Baum bleibt grün.

1. **Quellen:** Module `practice/src/practice/interval/` mit dem HDX-IPC-Abruf (eine Datei, ETag,
   ehrlicher User-Agent) und dem FTS-Abruf (`nextLink`-Paginierung, mehrjährige Grenze). Bytes
   gesichert unter `interval/snapshots/<date>/` mit Manifest, über das vorhandene
   `practice.preserve`. Tests mit Fixtures, kein Netz im Test.
2. **Warn-Reihe und t0** als reine Funktionen, Tests mit konstruierten Reihen, darunter eine
   chronische Phase-4-Lage, die keinen Beginn auslösen darf.
3. **Geld-Reihe und t1**: beide Zeitachsen, FSC und Total, Grenzsemantik. Tests, darunter der
   Fall Januar 2011 (Einjahres- gegen Mehrjahresfenster).
4. **Register** `interval/register.json`: Episoden × Gitter plus Treiber-Vermerk (anfangs aus
   einer handgepflegten, zitierten Liste `interval/drivers.json`). Dazu eine Erweiterung von
   `verify.py`, die das Register aus den Snapshots nachrechnet und bei Abweichung scheitert.
5. **Workflow** `interval.yml`, **wöchentlich** (die Daten sind monatlich). Er läuft wie die
   anderen Register: Anker-Registrierung, verify, Commit. Erst ab hier gibt es Nächte.
6. **E-Experiment:** Der Pass schreibt die Abnahmekriterien als Datei, **bevor** das Fenster
   aufgeht, mindestens vier wöchentliche Lesungen ohne Lücke. Das Review danach und jede Bühne
   bleiben bei Frank. Bis dahin hat The Interval auf der Site keine Bühne.

## 7. Entscheidungen, die bei Frank liegen

- **Entschieden 2026-10-04: keine Anfrage bei FEWS NET** (Frank, Wortlaut privat). The Interval
  bleibt bei IPC/HDX und FTS. Die Rückschau vor 2020 bleibt offen.
- *(vorher gefragt)* **Partnerzugang bei FEWS NET anfragen?** Das würde die Rückschau 2011–2020 sauber öffnen,
  darunter Somalia 2011 und 2017, und den Bestand sichern, falls FEWS NET eingestellt wird. Eine
  Anfrage ist eine Mail an reale Empfänger, also Franks Knopf. Ein Partner-Entitlement wäre
  außerdem eine Zugangsberechtigung, und die Charter müsste das ausdrücklich zulassen.
- **Rückschau über die öffentlichen Shapefiles** (ab 2009, GIS-Verschnitt, nur abgeleitete Tabellen
  plus Hashes im Repo) — machbar ohne Anfrage, aber erst nach V0 sinnvoll.
