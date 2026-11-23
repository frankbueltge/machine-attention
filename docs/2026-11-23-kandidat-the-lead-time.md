# The Lead Time — Exposé

**Datum:** 2026-11-23 · **Stufe:** EXPOSÉ · **Anlass:** Alle Kandidaten mit einem nächsten Schritt
warten auf ein Tor des Maintainers. The Interval: Review angefragt (`REQUESTS.md` 2026-11-16).
Planetary Listening: Review angefragt (`REQUESTS.md` 2026-11-04). The Provisional Air: GO angefragt
(`REQUESTS.md` 2026-11-17). The Shortage Clock: GO angefragt (`REQUESTS.md` 2026-11-21), Lizenzfrage
(`REQUESTS.md` 2026-11-20). The Synthetic Flood: wartet auf ihren Workflow am 2026-12-04
(`docs/2026-11-09-synthetic-flood-v0-inkrement-4.md`). The Declared Network und The Afterlife:
`REQUESTS.md` 2026-10-23 und 2026-10-30. Laut `discovery/PROMPT.md` Schritt 2 darf dann ein neues
Exposé pro Woche entstehen; das letzte war The Shortage Clock am 2026-11-18 (ISO-Woche 47,
`docs/2026-11-18-kandidat-the-shortage-clock.md`). Dies ist das Exposé der ISO-Woche 48.

Jede Aussage über Formate, Lizenzen, Raten und Aufbewahrung der Quellen ist **ungeprüft** und gehört
dem AUDIT. Geprüft ist heute nur, was §6 nennt: die `robots.txt` jedes Hosts, den V0 lesen würde, je
ein Status-Abruf (2026-11-23, ≈ 07:3x UTC) und die **Dateinamen** zweier Verzeichnislisten. Keine
Warnung gelesen, keine Werte übernommen, keine Bytes konserviert.

## 1. Die Frage

> Wie viel Vorwarnung bekam die Öffentlichkeit tatsächlich — und was bleibt von der Geschichte einer
> amtlichen Wetterwarnung, wenn sie abgelaufen ist?

Nationale Wetterdienste geben Warnungen aus: für ein Gebiet, eine Stufe, ein Gültigkeitsfenster.
Eine Warnung lebt: sie wird ausgegeben, hochgestuft, verlängert, verkleinert, aufgehoben. Die
Verifikation, die die Dienste selbst betreiben, fragt, ob das Ereignis eintrat (Trefferquote,
Fehlalarmquote, §5). Sie fragt nicht öffentlich, **wann** die Öffentlichkeit welche Stufe zum ersten
Mal sah.

Die Operation des Gründungskorpus (`docs/2026-08-08-projekt-aufnahme.md`), diesmal die **öffentliche
Warnlage gegen ihre eigene Zeitachse**. Messgrößen je Gebiet × Ereignistyp:
(a) **Vorlauf** — Zeit zwischen der ersten öffentlich sichtbaren Warnung einer Stufe und dem Beginn
ihrer Gültigkeit; (b) **späte Hochstufung** — Anteil der Fälle, in denen die höchste Stufe erst
innerhalb der Gültigkeit erschien; (c) **Lebenslauf** — Zahl der Änderungen (Stufe, Fenster, Gebiet)
bis zur Aufhebung, und Aufhebungen vor Beginn; (d) **was verschwindet** — welcher Teil dieses
Lebenslaufs nach Ablauf in keiner öffentlichen Quelle mehr steht.

## 2. Warum nur anhaltende maschinelle Aufmerksamkeit das beantworten kann

- **Die deutsche Quelle vergisst nach zwei Tagen.** Der Deutsche Wetterdienst (DWD) legt seine
  Warnungen als CAP-Dateien unter `opendata.dwd.de/weather/alerts/cap/` ab; die Verzeichnisliste
  `COMMUNEUNION_DWD_STAT/` begann heute um ≈ 07:3x UTC mit einem Stand von **2026-11-21 07:40:56 UTC**
  (Dateiname `Z_CAP_C_EDZW_20261121074056_…_DE.zip`, 1 711 Verweise in der Liste). Ein rollendes
  Fenster von etwa 48 Stunden, das auch eine Drittdokumentation beschreibt (§5). Wer die
  Warngeschichte eines Sturms in einer Woche rekonstruieren will, findet sie dort nicht mehr.
- **Aggregatoren zeigen die Gegenwart.** Meteoalarm, der europäische Sammelpunkt nationaler
  Warnungen, liefert je Land einen aktuellen Feed (§3); ob er eine Geschichte hält, prüft das AUDIT.
- **Die Verifikation ist die des Ausgebers.** Sie misst Warnung gegen Ereignis, intern, und
  veröffentlicht Jahreszahlen (§5). Den Lebenslauf der Warnung, so wie die Öffentlichkeit ihn sah,
  hält niemand fest, der nicht jeden Tag mehrmals las.
- **Wiederholbarkeit.** Jeder gelesene Stand mit dem SHA-256 der empfangenen Datei, wie `verify.py`
  es für The Interval hält.

## 3. Datenlage-Kurzcheck (ungeprüft, für das AUDIT)

| Seite | Kandidat-Quelle | Was das AUDIT klären muss |
|---|---|---|
| Deutschland, Hauptquelle | DWD CAP, `opendata.dwd.de/weather/alerts/cap/` (200; Unterverzeichnisse `COMMUNEUNION_*`, `DISTRICT_*` je `_STAT` und `_DIFF`) | Takt der Stände (Dateinamen deuten auf einige Minuten); Größe eines Stands; ob `_DIFF` den Lebenslauf billiger trägt als `_STAT`; Lizenz (Nutzungsbedingungen des Open-Data-Servers); ob CAP-Felder `msgType` (`Alert`/`Update`/`Cancel`), `references`, `onset`, `sent` den Lebenslauf ohne Rekonstruktion tragen. |
| Europa, Aggregator | Meteoalarm, `feeds.meteoalarm.org/api/v1/warnings/feeds-germany` (200, **8 942 466 B** in einem Abruf) | Lizenz und Weitergabebedingungen (eine Seite „terms and conditions" existiert laut einer Drittliste, nicht gelesen); ob der Feed abgelaufene Warnungen hält; Takt; ob V0 statt Deutschland ein zweites Land braucht, dessen nationaler Dienst keinen offenen Feed hat. Die Größe spricht gegen mehrmals täglich. |
| Vereinigtes Königreich, Kontrolle | Met Office National Severe Weather Warning Service (Archiv seit März 2011 in der Bibliothek, eine „NSWWS Open Licence" existiert laut Suchauszug) | Ob das Archiv maschinenlesbar ist und Änderungen innerhalb einer Warnung hält; ob es den Lebenslauf schon zeigt — dann Kontrolle für die Methode. |
| Deutschland, Hitze | `opendata.dwd.de/climate_environment/health/historical_alerts/heat_warnings/` (200; Beschreibung nennt 2005–2019 laut Suchauszug) | Ob ein historischer Datensatz endgültige Warnungen oder Lebensläufe hält; zeigt, dass der DWD Archive veröffentlichen kann. |

**Rückwirkend:** für Deutschland nur das rollende 48-Stunden-Fenster. Das Tageslicht beginnt mit der
ersten Lesung.

## 4. V0-Skizze (nur Form, keine Festlegung)

Einheit: **Warnung × Stand** (CAP-`identifier`, über `references` zu einer Kette verbunden). Mehrmals
täglich (Takt aus dem AUDIT, sodass keine Kette zwischen zwei Lesungen beginnt und endet) die
`_DIFF`- oder `_STAT`-Dateien des DWD, gehasht; committet werden abgeleitete Zeilen je Kette:
`first_seen`, `level_changed` (mit Richtung), `window_changed`, `area_changed`, `cancelled`,
`expired`. Berichtet als Verteilung von Vorlauf und Änderungen je Ereignistyp, Stufe und Monat — nie
als Urteil über eine einzelne Warnung. Die Klasse ist vermutlich **Instrument**; ein E-Experiment von
14 Nächten kann Vollständigkeit der Ketten und Lesbarkeit prüfen, eine Wintersturmsaison erst die
Verteilung.

Substrat: Lesen und Sichern wie The Interval (`practice/src/practice/interval/`), Zip und XML aus der
Standardbibliothek. Anders als bei den bisherigen Kandidaten ist der Takt **unter einem Tag** — die
nächtliche Bauform der Praxis reicht nicht; das AUDIT sagt, ob ein Workflow mehrmals täglich im
Rahmen bleibt.

## 5. Die nächsten Nachbarn, und das Tageslicht

| Nachbar | Was er tut | Tageslicht | Erreichbar 2026-11-23 |
|---|---|---|---|
| [Iowa Environmental Mesonet, VTEC-Archiv](https://mesonet.agron.iastate.edu/info/datasets/vtec.html) | Archiviert alle Warnungen des US-Wetterdienstes mit Ausgabe- und Ablaufzeit, Tornado- und Gewitterwarnungen seit 1986, die meisten Typen seit 2005/2008; Shapefiles und API. | **Der Beweis, dass es geht, und er nimmt die USA ganz.** Für die USA existiert der Lebenslauf öffentlich; die Frage wird darum für Europa gestellt, wo kein solches Archiv gefunden wurde. Methodische Warnung des Archivs selbst: Ausgabezeit und Beginn sind nicht dasselbe — genau Messgröße (a). | Suchauszug; nicht abgerufen |
| [MeteoSchweiz, „Die Qualität unserer Unwetterwarnungen"](https://www.meteoschweiz.admin.ch/ueber-uns/meteoschweiz-blog/de/2026/04/diequalitaetunsererunwetterwarnungen2025.html) | Jährliche Treffer- und Fehlalarmquote ab Stufe 3 gegen vereinbarte Ziele (≥ 85 % / ≤ 30 %). | Ereignis gegen Warnung, eigene Daten, Jahreswert. Kein Vorlauf, kein Lebenslauf, keine Rohdaten. | Suchauszug; nicht abgerufen |
| DWD-Warnverifikation ([Göber, DACH 2010](https://meetingorganizer.copernicus.org/DACH2010/DACH2010-207.pdf); [ASR 2016](https://asr.copernicus.org/articles/13/113/2016/asr-13-113-2016.pdf)) | Methoden der internen Verifikation, Böenwarnungen. | Intern, aus dem vollständigen Archiv des Ausgebers; nicht wiederholbar von außen. | Suchauszug; nicht abgerufen |
| [wetterdienst (Python-Bibliothek)](https://wetterdienst.readthedocs.io/en/latest/data/provider/dwd/alerts/index.html) | Holt DWD-Warnungen zu einem vergangenen Zeitpunkt — nur innerhalb des 48-Stunden-Fensters. | Ein Werkzeug, kein Archiv; bestätigt das Fenster (Drittangabe). | Suchauszug; nicht abgerufen |
| [Met Office, NSWWS-Archiv](https://metoffice.gov.uk/research/library-and-archive/publications/national-severe-weather-warning-service) | Warnungen seit März 2011 in der Bibliothek. | Möglicherweise der europäische Nachbar, der den Lebenslauf schon hält; das AUDIT prüft, ob Änderungen innerhalb einer Warnung sichtbar sind. Findet es sie, wird UK Kontrolle, nicht Lücke. | Suchauszug; nicht abgerufen |
| [DWD, historische Hitzewarnungen](https://opendatao.dwd.de/climate_environment/health/historical_alerts/heat_warnings/Description_historical_heat_alerts.pdf) | Ein historischer Datensatz für einen Warntyp (2005–2019 laut Auszug). | Endgültige Warnungen eines Typs, abgeschlossen; nicht der laufende Lebenslauf aller Typen. | Verzeichnis 200 (nur Dateinamen) |

Ob jemand die DWD- oder Meteoalarm-Feeds bereits dauerhaft und öffentlich archiviert, ist heute
nicht geprüft und die erste Frage des AUDIT an die Nachbarschaft.

## 6. Vorprüfung der Roboter-Regeln (je Host ein Abruf)

| Host | `robots.txt` | Bedeutung für V0 |
|---|---|---|
| `opendata.dwd.de` | 404, keine Datei | Keine Bitte an Roboter; der Server ist für automatisierte Abrufe gebaut. |
| `feeds.meteoalarm.org` | 200; nur Kommentare, `Disallow: /` auskommentiert | Keine Sperre. |
| `meteoalarm.org`, `www.meteoalarm.org` | 404 | Nur Erläuterungsseiten. |
| `www.dwd.de` | 200; `User-agent: *` → `Disallow: /`, `Crawl-delay: 10` | **Gesperrt.** V0 braucht den Host nicht (Daten liegen auf `opendata.dwd.de`); Nutzungsbedingungen, die nur dort stehen, liest das AUDIT nicht maschinell, sondern legt die Frage dem Maintainer vor, wie bei OSCAR und E-utilities. |

Abrufe heute, alle mit einem generischen Agenten: fünf `robots.txt` (Tabelle), drei Status-Abrufe
(`…/cap/`, `…/historical_alerts/`, Meteoalarm-Feed Deutschland — dessen Bytes verworfen), danach die
Verzeichnislisten `…/cap/`, `…/historical_alerts/` und `…/cap/COMMUNEUNION_DWD_STAT/` je zweimal
(ein Skript listete und zählte in zwei Aufrufen; nur Dateinamen gelesen). Vierzehn Abrufe, nichts
gesendet, nichts konserviert.

## 7. Grenzen, ehrlich

- **Keine Anschuldigung (E-2).** Ein kurzer Vorlauf ist kein Fehler: konvektive Ereignisse sind nicht
  Tage voraus warnbar, und eine aufgehobene Warnung kann richtig gewesen sein. Gemessen wird, was die
  Öffentlichkeit sah, nicht ob der Dienst richtig lag. Keine Ausgabe bewertet eine einzelne Warnung.
- **Keine Personen (I8).** Warnungen nennen Gebiete, keine Personen. CAP-Felder wie `sender` oder
  `contact` werden nicht gespeichert.
- **Kein Ereignisvergleich in V0.** Ob das Ereignis eintrat, ist die Frage der Verifikation des
  Dienstes; sie mit Stationsdaten nachzubauen, wäre ein zweiter Kandidat.
- **Takt unter einem Tag.** Eine Kette, die zwischen zwei Lesungen beginnt und endet, fehlt; das
  rollende Fenster dämpft das, solange je 48 Stunden mindestens eine Lesung gelingt.
- **Saison.** Wintersturm, Glätte und Tauwetter jetzt, Gewitter erst ab Frühjahr; eine Verteilung
  braucht ein Jahr.
- **Nähe zu The Shortage Clock und The Interval.** Dieselbe Bauform (frühe Darstellung gegen spätere);
  hier ist der Gegenstand aber flüchtig im Stundenmaß und die Quelle löscht von selbst.
- **Wenn ein öffentliches Archiv der Ketten existiert** (Met Office, Meteoalarm), schrumpft das
  Tageslicht auf seine Auswertung; das ist ein gültiges Ende im AUDIT.

## 8. Was das AUDIT prüfen muss

Für die DWD-CAP-Verzeichnisse, den Meteoalarm-Feed und das Met-Office-Archiv je: exakter Endpunkt,
HTTP-Status, Größe eines Stands, Takt, Rate ohne Schlüssel, Lizenz, Bitten an automatisierte
Abrufer, ob innerhalb der Delegations-Charta, und eine Probe mit Manifest unter
`leadtime/probes/<date>/`. Zuerst und entscheidend: **ob die CAP-Kette (`msgType`, `references`)
den Lebenslauf einer Warnung aus zwei Ständen im Abstand einiger Stunden ohne Lücke trägt**, und ob
`_DIFF` dafür genügt. Dazu: die Nutzungsbedingungen des DWD-Open-Data-Servers, soweit sie ohne
`www.dwd.de` lesbar sind, und ob irgendwo ein öffentliches europäisches Kettenarchiv existiert. Am
Ende steht eine Empfehlung. Das GO für V0 ist laut Aufnahme-Pfad das des Maintainers; das AUDIT
braucht es nicht.

## Bewusst nicht heute

Keine Warnung gelesen, keine CAP-Datei geladen, keine Bytes konserviert, kein Code, kein Verzeichnis
`leadtime/`. Kein Abruf von `www.dwd.de` über seine `robots.txt` hinaus. Der Fokus ist unberührt.
Das AUDIT kommt erst, wenn kein früherer Kandidat einen fälligen Schritt hat; vor ihm stehen The
Provisional Air und The Shortage Clock, falls ihr GO kommt.
