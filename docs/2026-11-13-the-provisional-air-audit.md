# The Provisional Air — AUDIT, Teil 1

**Datum:** 2026-11-13 · **Stufe:** AUDIT (Teil 1 von 2) · **Exposé:**
`docs/2026-11-11-kandidat-the-provisional-air.md` · **Proben:** 18 Abrufe, jeder mit Manifest in
`provisionalair/probes/2026-11-13/manifest.json` (Bytes und SHA-256, von `verify.py` gehalten).

**Anlass:** Kein früherer Kandidat hat heute einen fälligen Schritt (`discovery/AGENDA.md`): The
Interval schließt sein Fenster am 2026-11-15 und hat diese Woche nichts zu lesen; Planetary Listening
wartet auf den Review (`REQUESTS.md` 2026-11-04); die Synthetic Flood auf ihren Workflow am
2026-12-04; The Declared Network und The Afterlife auf `REQUESTS.md` (2026-10-23, 2026-10-30).

Jeder Abruf: ein Versuch, keine Wiederholung, Standardbibliothek, Kennung
`machine-attention/0.1`. **Das Anfragefeld `email` wurde nie gesetzt**; das Probe-Skript bricht ab,
wenn es im Anfragekörper steht. Keine Kontaktfelder, keine Personen (I8). Zum Lesen der beiden
Parquet-Dateien diente eine Wegwerf-Umgebung außerhalb des Baums; die Praxis hat keine neue
Abhängigkeit.

## 1. Die entscheidende Frage: ersetzt eine Neulieferung die alte Fassung?

**Ja — und das lässt sich schon an einem einzigen Abruf zeigen, nicht erst an zweien.**

Die vorläufige Datei einer Messstelle
(`provisionalair/probes/2026-11-13/blob/e2a-SPO-LU0101A_00005_103.parquet`, 181 133 B, PM10, eine
Station in Luxemburg) hat **7 591 Zeilen und 7 591 verschiedene Stundenanfänge**
(2026-01-01 01:00 bis 2026-11-13 07:00): jede Stunde genau eine Zeile. Jede Zeile trägt
`ResultTime` — den Zeitpunkt der Lieferung, aus der sie stammt (1 758 verschiedene Werte, ebenso
viele `FkObservationLog`). Die Datei war beim Abruf zwei Minuten alt (`Last-Modified` 07:37:27 UTC,
Abruf 07:39:01 UTC, Manifest-Header): sie wird als Ganzes neu geschrieben.

Verzögerung `ResultTime − End` je Monat (Zeilen gesamt / davon unter 6 h):

| Monat | Zeilen | < 6 h | Auffällig |
|---|---|---|---|
| 2026-01 | 743 | 728 | — |
| 2026-02 | 672 | 659 | — |
| 2026-03 | 744 | 628 | — |
| 2026-04 | 720 | 28 | — |
| 2026-05 | 744 | 0 | — |
| 2026-06 | 720 | 24 | — |
| 2026-07 | 744 | 0 | alle 744 Stunden mit `ResultTime` 2026-08-05 |
| 2026-08 | 744 | 0 | — |
| 2026-09 | 720 | 0 | alle 720 mit `ResultTime` 2026-10-07 |
| 2026-10 | 744 | 0 | alle 744 mit `ResultTime` 2026-11-04 |
| 2026-11 | 296 | 6 | 156 Stunden um 11-08 mit `ResultTime` 2026-11-10 |

Die letzten Stunden (heute 02:00–07:00) stehen mit weniger als 6 h Verzögerung in der Datei — das
ist der Wert, den der Tag sieht. Die Monate Juli bis Oktober dagegen tragen je **eine einzige
Lieferzeit Anfang des Folgemonats**: ganze Monate wurden neu geliefert, und da jede Stunde nur eine
Zeile hat, steht die frühere Fassung nicht mehr im Download. Ob und wie stark sich die Werte dabei
geändert haben, sagt die Datei nicht — genau das ist, was nur ein nächtliches Festhalten sehen kann.
Nicht bewiesen ist, dass jede dieser Stunden vorher schon einmal geliefert war; das zeigt Teil 2
(§6), indem er die heute frischen Stunden nach einer Neulieferung wieder liest.

**Rückwirkend:** Die vorläufige Datei beginnt am 2026-01-01. Die validierte Datei derselben
Messstelle (`…/blob/e1a-SPO-LU0101A_00005_103.parquet`, 240 798 B, 17 544 Stunden 2024-01-01 bis
2026-01-01, `Verification` 1, `ResultTime` 2025-09-04 und 2026-09-11, `Last-Modified` 2026-10-20)
deckt 2024 und 2025. **Die vorläufigen Werte von 2025 sind aus diesem Download verschwunden,
seit 2025 validiert ist.** Damit ist die vorläufige Seite eines validierten Jahres hier nicht mehr
lesbar, auch nicht in ihrer letzten Fassung: Der Kandidat ist an dieser Quelle **nicht** zur Hälfte
rückwirkend. Das Tageslicht des Exposés (§2) bleibt — gegen diese Quelle. Gegen OpenAQ siehe §4.

## 2. Die Quelle, Endpunkt für Endpunkt

| Abruf | Endpunkt | Status | Größe | Befund |
|---|---|---|---|---|
| Version | `GET …azurewebsites.net/Version` | 200 | 7 B | `Raster1` |
| Schadstoffe | `GET /Pollutant` | 200 | 71 014 B | 648 Einträge; PM10 = `…/pollutant/5`, NO2 = `…/pollutant/8` |
| Umfang | `POST /DownloadSummary`, LU, PM10, `dataset` 1 | 200 | 26 B | 5 Dateien |
| Umfang | dasselbe, `dataset` 2 (Tag 2026-11-10 und 2024-11-10) | 200 | 27 B je | 15 Dateien beide Male — der Datumsfilter wirkt auf die Dateiauswahl nicht |
| Adressen | `POST /ParquetFile/urls`, `dataset` 1 | 200 | 508 B | 5 Dateien im Container `airquality-p` |
| Adressen | dasselbe, `dataset` 2 | 200 | 834 B | 8 Dateien im Container `airquality-p-e1a` |
| Datei E2a | `GET eeadmz1batchservice02.blob.core.windows.net/airquality-p/LU/SPO-LU0101A_00005_103.parquet` | 200 | 181 133 B | siehe §1 |
| Datei E1a | `GET …/airquality-p-e1a/LU/SPO-LU0101A_00005_103.parquet` | 200 | 240 798 B | siehe §1 |
| Roboter | `GET …blob.core.windows.net/robots.txt` | 400 | 226 B | `OutOfRangeInput` — der Speicher kennt keine Datei dieses Namens; keine Bitte an Roboter |

**`dataset` 1 = E2a (vorläufig), `dataset` 2 = E1a (validiert)** — belegt durch die Container der
zurückgegebenen Adressen, nicht durch Dokumentation (die Swagger-Beschreibung
`…/swagger/v1/swagger.json` nennt das Feld nur als Ganzzahl). Die Dateien liegen je Messstelle und
Schadstoff vor, jahresweise kumulativ; ein Tagesabruf ist also kein Tagesausschnitt, sondern die
ganze Jahresdatei. Spalten beider Fassungen gleich: `Samplingpoint, Pollutant, Start, End, Value,
Unit, AggType, Validity, Verification, ResultTime, DataCapture, FkObservationLog`. Die
Speicherantwort trägt `ETag` und `Last-Modified` — eine Nacht kann also mit einem Kopfabruf je Datei
sehen, ob sich etwas geändert hat, und nur dann die Datei holen.

**Rate:** 18 Abrufe in sechs Minuten, kein 429, keine Ratenkopfzeilen. Eine dokumentierte Grenze
wurde nicht gefunden. **Lizenz:** an keinem der Endpunkte und auf keiner der gelesenen
Portalseiten genannt (`…/docs/download-data.html`, `…/docs/legal-aspects.html`: nur die
Rechtsakte). Die Lizenz bleibt offen für Teil 2 (EEA-Datenkatalog).

**Charta:** öffentlich, ohne Anmeldung, ohne Schlüssel, ohne Kosten; keine personenbezogenen
Daten in den Dateien (Messstelle, Stunde, Wert). Das freiwillige Feld `email` bleibt leer.

**Größe für V0:** Luxemburg hat 5 vorläufige PM10-Dateien (Umfang 0 MB laut `DownloadSummary`,
gerundet). Bei rund 180 KB je Messstelle und Jahr bis November wären einige hundert Messstellen ×
zwei Schadstoffe pro Nacht zweistellige Megabyte — **zu groß zum Committen**. V0 müsste die
Dateien nur bei geändertem `ETag` holen und **abgeleitete Zeilen** festhalten (Stunde, Wert,
`ResultTime`, Hash der Quelldatei), wie The Declared Network es für WDQMS vorschlug.

## 3. Nebenbefund: die Richtlinie wechselt

Die Portalseite „Legal aspects" (`…/docs/legal-aspects.html`) nennt Richtlinie 2008/50/EG als
**aufgehoben mit Wirkung vom 12. Dezember 2026**; an ihre Stelle tritt Richtlinie (EU) 2024/2881.
Die Tagesschwellen, an denen V0 die Seitenwechsel zählen würde, sind also an die neue Richtlinie zu
binden, mit Datum. Das Exposé nennt nur 2008/50/EG; das ist hiermit korrigiert.

## 4. Der stärkste Nachbar: OpenAQ

Die Dokumentationsseite des öffentlichen Archivs (`…/openaq/aws-about.html`, `robots.txt`
`Allow: /`) sagt wörtlich: *„Files are written 72 hours after the end of day … Files may be
retroactively patched if data are missing due to fetching error or from historical data scrape."*
Die FAQ (`…/openaq/faq.html`) sagt zu Fassungen nichts. Gelesen: OpenAQ hält **eine** Fassung je
Stunde, etwa drei Tage nach dem Tag, ohne dokumentierte Versionsgeschichte, und kann sie
nachträglich ersetzen. Wenn OpenAQ die europäischen Stationen aus dieser Quelle bezieht, liegt dort
für vergangene Jahre ein Wert „Tag + 3" vor der Monatsneulieferung — **das würde einen Teil der
rückwirkenden Hälfte zurückbringen**, die §1 der EEA-Quelle abspricht. Nicht geprüft: welche
Quelle OpenAQ für Luxemburg und Deutschland nutzt, und ob die Archivdatei eines vergangenen Tages
die frühe oder die neu gelieferte Fassung trägt. Das ist die zweite entscheidende Prüfung, und sie
gehört an das öffentliche Archiv, nicht an die Schnittstelle (die einen Schlüssel verlangt).

## 5. Nicht geprüft heute

Die nationale Kontrolle (Umweltbundesamt, Luftdaten-API v3) — Teil 2. Die Lizenz. Ein fester
Stationssatz. NO2. Ob `Validity` −1 (20 Zeilen) bei der Neulieferung wechselt.

## 6. Teil 2 — was ihn abschließt

1. **Wiederholungsabruf derselben Datei** an einem Abend ab 2026-11-16 (ein Abruf): Tragen die heute
   frischen Stunden 2026-11-13 02:00–07:00 dann eine spätere `ResultTime`, und hat sich ein Wert
   geändert? Der Vergleich ist allein aus den beiden konservierten Dateien zu führen; die heutige
   Datei ist hash-gebunden.
2. **OpenAQ-Archiv:** eine Tagesdatei 2025 einer Luxemburger Station gegen dieselben Stunden in
   E1a — trägt OpenAQ die frühe oder die neue Fassung, und woher?
3. **UBA-Kontrolle:** eine Stunde einer deutschen Station bei UBA und in E2a.
4. **Lizenz** aus dem EEA-Datenkatalog.

Danach die Empfehlung. Sie ist heute noch nicht fällig: Fiele OpenAQ als „Vorher" aus, wäre die
Empfehlung GO für ein enges V0; hielte OpenAQ die frühe Fassung, schrumpfte das Tageslicht auf die
Zwischenrevisionen der ersten drei Tage — und das wäre zu sagen.

## Bewusst nicht heute

Kein zweiter Abruf einer Datei, kein Stationssatz, kein Code unter `practice/`, keine Schwelle
festgelegt. Kein Abruf von `www.eea.europa.eu/api` (dort `Disallow: /api`, Exposé §6). Keine
OpenAQ-Schnittstelle. Das GO für V0 bleibt dem Maintainer.
