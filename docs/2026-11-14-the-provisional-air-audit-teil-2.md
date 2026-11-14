# The Provisional Air — AUDIT, Teil 2 (Punkte 2–4)

**Datum:** 2026-11-14 · **Stufe:** AUDIT (Teil 2, ohne Punkt 1) · **Teil 1:**
`docs/2026-11-13-the-provisional-air-audit.md` · **Exposé:** `docs/2026-11-11-kandidat-the-provisional-air.md`
· **Proben:** 12 Dateien mit Manifest in `provisionalair/probes/2026-11-14/manifest.json` (Bytes und
SHA-256, von `verify.py` `check_snapshots` gehalten).

**Anlass:** Kein früherer Kandidat hat heute einen fälligen Schritt (`discovery/AGENDA.md`): The
Interval schließt sein Fenster morgen und hat heute (Samstag) nichts zu lesen; Planetary Listening
wartet auf den Review (`REQUESTS.md` 2026-11-04), die Synthetic Flood auf ihren Workflow am
2026-12-04, The Declared Network und The Afterlife auf `REQUESTS.md` (2026-10-23, 2026-10-30).
Teil 1 §6 bindet nur Punkt 1 (Wiederholungsabruf derselben Datei) an „ab 2026-11-16"; die Punkte 2–4
haben kein Datum und werden heute genommen. Punkt 1 bleibt für einen Abend ab 2026-11-16.

Jeder Abruf: ein Versuch, keine Wiederholung, Standardbibliothek, Kennung `machine-attention/0.1`;
das Anfragefeld `email` wurde nie gesetzt (das Skript bricht ab, wenn es im Anfragekörper steht).
Zum Lesen der Parquet-Datei diente eine Wegwerf-Umgebung außerhalb des Baums; die Praxis hat keine
neue Abhängigkeit.

**Offengelegt — vor den Proben gesendet und nicht konserviert:** fünf Statusabrufe (OpenAQ-Archiv,
EEA-Katalog, UBA-Meta, EEA-Version, OpenAQ-Doku; nur Statuscode und Größe gelesen), zwei
Listenabrufe des OpenAQ-Archivs (dieselben, die konserviert unter `openaq/list-root.xml` und
`openaq/list-records.xml` liegen), eine Katalogsuche (POST, 200 — sie nannte die beiden unten
konservierten Datensätze), zwei Abrufe der UBA-`robots.txt`, ein Stationsabruf bei UBA, der nach
30 s ohne Bytes abbrach. Der zweite Stationsabruf (57 s, 200) ist konserviert, aber ohne Kopfzeilen
(`uba/stations-airquality.json`, im Manifest als Befehlszeilen-Client vermerkt). Die konservierte
Wiederholung der Katalogsuche antwortete **400** mit leerem Körper (`catalogue/search-e1a-e2a.json`)
— vermutlich fehlte die `Accept`-Kopfzeile des ersten Versuchs; nicht wiederholt.

## Punkt 4 — Lizenz: CC BY 4.0

`robots.txt` des Katalogs: `User-agent: * / Allow: /` (`catalogue/robots.txt`).

| Datensatz | Datei | Lizenzangabe |
|---|---|---|
| `fe809728-9cec-41c0-a9be-3a8f04600974` „Air Quality download service for verified and Up To Date data, 2013-now" | `catalogue/record-fe809728-….xml` | „License CC-BY 4.0 (https://creativecommons.org/licenses/by/4.0/). Copyright holder: European Environment Agency (EEA)." |
| `0eed9a67-0018-4a9b-9925-f4a10d333428` „Air Quality e-Reporting: Air quality time series (E1a & E2a data sets)" | `catalogue/record-0eed9a67-….xml` | „No limitations to public access"; „License CC-BY 4.0 … Copyright holder: European Commission." |

Der erste Datensatz beschreibt genau den Dienst, den Teil 1 abgerufen hat. **Die Quelle liegt in der
Charta** (öffentlich, ohne Schlüssel, ohne Kosten, keine Personendaten) und ist unter CC BY 4.0
weiterverwendbar; V0 müsste die EEA als Quelle nennen. Die beiden Datensätze nennen verschiedene
Rechteinhaber (EEA, Europäische Kommission) — für die Namensnennung beide.

## Punkt 3 — UBA-Kontrolle: dieselben Stunden, dieselben Werte; und eine zweite Form des Überschreibens

Station Berlin Wedding (`DEBE010`, UBA-ID 121 laut `uba/stations-airquality.json`), PM10,
Stundenmittel (`component=1&scope=2`), 2026-11-13 00:00–12:00 (`uba/measures-121-pm10-2026-11-13.json`,
1 059 B) gegen die vorläufige Datei derselben Messstelle
(`blob/e2a-SPO.DE_DEBE010_PM1_dataGroup1.parquet`, 221 441 B, `Last-Modified` 2026-11-14 07:02:54 UTC,
Abruf 07:40:51 UTC; Adresse aus `eea/urls-DE-PM10-ds1.csv`).

| Stunde (Beginn) | UBA | E2a |
|---|---|---|
| 00 | 12 | 12.47 |
| 01 | 11 | 10.54 |
| 02 | 9 | 9.25 |
| 03 | 8 | 7.73 |
| 04 | 7 | 6.78 |
| 05 | 6 | 5.50 |
| 06 | 5 | 5.23 |
| 07 | 6 | 5.66 |
| 08 | 7 | 6.57 |
| 09 | 8 | 8.09 |
| 10 | 8 | 8.34 |
| 11 | 10 | 9.56 |

**12 von 12 Stunden stimmen auf ganze µg/m³ gerundet überein, bei gleicher Stundenbeschriftung.**
UBA gibt ganze Zahlen aus, E2a zwei Nachkommastellen; UBA ist also eine zweite, gröbere Kopie
derselben vorläufigen Seite, kein unabhängiges Messsystem. Für V0 heißt das: UBA taugt als
Plausibilitätskontrolle der Stundenzuordnung, nicht als „Vorher". Ob UBA seine Werte selbst
überschreibt, zeigt ein Abruf nicht.

**Zeitachse (gefolgert, nicht bewiesen):** Die jüngste `ResultTime` der Datei ist 07:45:45, ihr
`Last-Modified` 07:02:54 UTC. Eine Lieferung kann nicht nach dem Schreiben der Datei liegen; liest man
`ResultTime` und die Stundenbeschriftung als UTC+1, passt es (06:45:45 UTC). Die UBA-Stunden, die
UBA in MEZ angibt, decken sich mit den E2a-Stunden gleicher Beschriftung. V0 müsste die Zeitzone
aus der Dokumentation belegen, bevor es Tage gegen Tagesschwellen zählt.

**Was die deutsche Datei über das Überschreiben zeigt** (7 344 Zeilen, 7 344 verschiedene
Stundenanfänge, 2026-01-01 00:00 bis 2026-11-14 23:00, 2 146 verschiedene `ResultTime`):

- **Jeder Tag wird am Folgetag neu geliefert.** Alle 24 Stunden von 11-10 tragen `ResultTime`
  2026-11-11 23:45:36, alle von 11-11 tragen 11-12 23:45:39, alle von 11-12 tragen 11-13 23:45:40;
  die Stunden von 11-13 und 11-14 tragen 11-14 07:45:45. Die Vormittagsstunden eines Tages sind also
  spätestens am Ende des Folgetags durch eine neue Lieferung ersetzt, und weil jede Stunde nur eine
  Zeile hat, steht die frühere Fassung nicht mehr im Download. Ob sich der **Wert** dabei ändert, zeigt
  ein Abruf nicht — das ist Punkt 1, und für Deutschland ist er nach dieser Datei schon nach einem Tag
  beantwortbar, nicht erst nach einer Monatsneulieferung.
- **Ein Quartal in einem Zug neu geliefert:** Januar bis März (2 160 Stunden) tragen alle
  `ResultTime` 2026-05-08. Luxemburg liefert monatlich neu (Teil 1 §1), Deutschland hier einmal für
  drei Monate — der Takt der Neulieferung ist eine Eigenschaft der Meldestelle, nicht der EEA.
- **Platzhalter für die Zukunft:** Die Stunden 2026-11-14 07:00 bis 23:00 stehen schon in der Datei,
  mit `Value` −999 und `Validity` −1. Die 20 Zeilen mit `Validity` −1 der luxemburgischen Datei von
  gestern sind dagegen verstreute Lücken (2026-01-07 bis 2026-09-02, alle −999), keine Zukunft.
  V0 darf −999 nie als Wert lesen.
- Lücken: August 528 von 744 Stunden, September 648 von 720.

## Punkt 2 — OpenAQ-Archiv: innerhalb der Charta nicht zu schließen

Das öffentliche Archiv antwortet ohne Schlüssel (`openaq/list-root.xml`, `list-records.xml`,
`list-csvgz-page1.xml`): ein Pfad `records/csv.gz/locationid=<n>/`, je Listenseite 1 000 Präfixe
(`IsTruncated true`), Kennungen bis über 1 066 094. **Das Archiv kennt keine Namen und keine
Stationscodes**; welche Kennung `LU0101A` oder `DEBE010` ist, sagt nur die Schnittstelle, und die
verlangt einen Schlüssel, der an das Konto einer Person gebunden ist — außerhalb der Charta (Teil 1 §4).
Den Archivbaum Seite für Seite und Datei für Datei nach Namen abzusuchen hieße hunderte Abrufe
für eine Zuordnung; das ist **bewusst nicht** getan.

Was sich ohne die Zuordnung sagen lässt, folgt aus Punkt 3 und Teil 1, nicht aus OpenAQ selbst:
OpenAQ schreibt eine Tagesdatei 72 Stunden nach dem Tag und kann sie nachträglich ersetzen (Teil 1
§4, `provisionalair/probes/2026-11-13/openaq/aws-about.html`). Die EEA-Datei ersetzt einen Tag schon
am Folgetag (oben). Hält OpenAQ für europäische Stationen eine Fassung, dann **eine aus den ersten
drei Tagen** — weder sicher die erste, noch die der Monats- oder Quartalsneulieferung, noch die
validierte. Das Tageslicht des Kandidaten gegen OpenAQ läge damit in den späten Neulieferungen und
im Sprung zur Validierung, nicht im ersten Tag. **Nicht bewiesen**, weil die Quelle, aus der OpenAQ
Luxemburg und Deutschland bezieht, ungeprüft bleibt.

## Empfehlung — vorläufig, bis Punkt 1

Die Quelle trägt ein V0: öffentlich, schlüssellos, CC BY 4.0, kein 429 in 30 konservierten Abrufen über zwei Tage,
eine Datei je Messstelle und Schadstoff mit `ETag`, jede Stunde genau eine Zeile mit ihrer
Lieferzeit, und Neulieferungen, die die frühere Fassung tilgen — Tag für Tag (Deutschland), Monat für
Monat (Luxemburg), Quartal auf einmal (Deutschland, Januar–März). Was nur nächtliches Festhalten
sehen kann, ist der Wertwechsel zwischen diesen Fassungen. **Vorläufige Empfehlung: GO für ein enges
V0** — wenige Messstellen in zwei Ländern, PM10, nur bei geändertem `ETag` holen, abgeleitete Zeilen
(Stunde, Wert, `Validity`, `ResultTime`, Hash der Quelldatei) committen, nicht die Dateien;
−999 nie als Wert; Tagesschwellen an Richtlinie (EU) 2024/2881 gebunden (Teil 1 §3). Die Empfehlung
wird erst endgültig, wenn Punkt 1 zeigt, ob eine Neulieferung **Werte** ändert; ändert sie nur die
`ResultTime`, schrumpft der Kandidat auf den Sprung zur Validierung, und das wäre zu sagen.

**Nächster Schritt:** Punkt 1 an einem Abend ab 2026-11-16 — dieselbe luxemburgische Datei einmal
und, neu wegen des Befunds oben, dieselbe Berliner Datei einmal: Haben die heute frischen Stunden
(LU 2026-11-13 02:00–07:00; DE 2026-11-13 00:00–23:00 und 2026-11-14 00:00–06:00) eine spätere
`ResultTime`, und hat sich ein Wert geändert? Zwei Abrufe, Vergleich allein aus den konservierten
Dateien. Danach die endgültige Empfehlung und die Bitte um das GO in `REQUESTS.md`.

## Bewusst nicht heute

Kein Wiederholungsabruf der Dateien von gestern (Punkt 1 ist an 2026-11-16 gebunden). Kein Absuchen
des OpenAQ-Archivs nach Namen, keine OpenAQ-Schnittstelle, kein Schlüssel. Kein Code unter
`practice/`, kein Stationssatz, keine Schwelle. Das GO für V0 bleibt dem Maintainer.
