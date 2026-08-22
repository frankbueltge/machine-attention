# Planetary Listening — Audit (Stufe 2 des Aufnahme-Pfads)

**Datum:** 2026-08-22 (Probes 15:23–15:36 UTC) · **Status:** Audit abgeschlossen,
Empfehlung an Frank — **die Aufnahme selbst bleibt sein Gate**
**Exposé:** `2026-08-08-kandidat-planetary-listening.md` · **Vorprüfung:**
`2026-08-22-kandidaten-re-audit.md` · **Muster:** `2026-08-08-dark-ocean-audit.md`
**Gelernt aus:** `2026-08-22-dark-ocean-e-review.md` §8 (Infrastruktur-Abhängigkeit,
nie-antwortende Quelle, C4)

## Einzeiler — der alte fällt, der neue steht

Der Exposé-Einzeiler versprach Infraschall über CTBTO, „Bombardement" und Echtzeit. Alle
drei Teile sind nach diesem Audit nicht haltbar (Befunde 4, 6, §Ethik). Ersatz, englisch,
als öffentliche Kopie vorgeschlagen:

> **A quarry blasts about once a day. A seismometer on its property has recorded every one
> of them at 100 Hz since 2000. Four public catalogues hold none of it. The machine keeps
> both records, night after night, and publishes the gap.**

Die planetare Rahmung ist damit datiert zurückgezogen: nicht „die Erde", sondern **ein
benannter Ort und eine Uhr**. Das ist kleiner als das Exposé und der einzige Zuschnitt, der
die Beweispflicht trägt.

## Quellen-Audit (Live-Probes 2026-08-22, 15:23–15:36 UTC — **alle ohne Anmeldung**)

| Quelle | Probe (UTC) | Befund |
|---|---|---|
| **GEOFON** `geofon.gfz.de` station | 15:23:18 · 200 · 118 B · 1,91 s | Netz GE: **147 Stationen seit 1993** — Exposé-Zahl heute unverändert bestätigt. Keyless |
| GEOFON, alter Host `geofon.gfz-potsdam.de` | 15:23:20 · 200 · 5 B | lebt weiter (v1.1.6), kein Redirect nötig |
| **GEOFON dataselect**, GE.RUE BHZ 60 s | 15:24:04 · 200 · `application/vnd.fdsn.mseed` · **2 560 B** · 0,12 s | keyless, Qualitätsflag **D** |
| GEOFON dataselect, GE.RUE HHZ 60 s | 15:24:04 · 200 · **11 264 B** | 100 Hz — das Band, in dem Sprengungen leben |
| GEOFON dataselect, **GE.RUE HHZ 24 h** | 15:24:24 · 200 · **10 768 896 B** (10,27 MiB) · 0,85 s | die gemessene Tageslast, nicht geschätzt |
| GEOFON dataselect, GE.RUE BHZ 24 h | 15:24:25 · 200 · **2 267 136 B** (2,16 MiB) | 4 428 Records × 512 B, STEIM2, alle Quality D |
| Wiederholung derselben 60 s | 15:24:24 · 200 · 2 560 B | **SHA-256 identisch** (`0b4c2aa5…`) |
| **GEOFON availability** `show=latestupdate` | 15:28:53 · 200 · 390 B | pro Kanal-Tag: Quality, SampleRate, Earliest/Latest, **`Updated 2026-08-22T04:54:26Z`** |
| GEOFON availability `extent` (26 Jahre) | 15:28:54 · 200 · 912 B | 5 Segmente, `Restriction OPEN`; Segmente von 2000–2012 tragen **`Updated` 2022-07-26 / 2022-10-12** |
| **EIDA WFCatalog** @ GEOFON, 1 Kanal-Tag | 15:29:38 · 200 · **1 399 B** | Herausgeber-Tagesdokument: `num_gaps`, `num_records` 21 033, `percent_availability` 100, `sample_rms`, Timing-Quality, `producer.created` |
| StationXML GE.RUE `level=channel` / `response` | 15:25:24 / 15:25:23 · 200 · 24 742 B / **654 283 B** | Response-Datei ist der Kalibrierungs-Anker; groß, aber einmalig |
| StationXML GE `level=network` | 15:32:42 · 200 · 427 B | **DOI 10.14470/TR560404** maschinenlesbar → Zitierpflicht erfüllbar |
| **IRIS** `service.iris.edu` ohne Redirect-Folge | 15:25:00 · **307** → `service.earthscope.org` | das HTTP 307 des Exposés ist aufgelöst |
| **EarthScope** station / dataselect | 15:25:11 · 200 · 139 B / **2 560 B** | keyless, IU: 116 Stationen. Trägt |
| **EarthScope fdsnws-event** | 15:25:24 · **410 Gone** | „**This service has been retired as of June 1st 2026**" — verweist auf ISC und USGS |
| **EarthScope fdsnws-availability** | 15:28:56 · **410 Gone** | außer Betrieb „starting Monday, July 27 … for an undetermined period", Grund: Abbau des Seattle-Rechenzentrums |
| **ISC** `isc.ac.uk` fdsnws-event | 15:25:53 · 200 · 6 B | v1.1.0, keyless, **trägt eine `EventType`-Spalte** |
| ISC, Europa-Box, Januar 2026 | 15:26:25 · 200 · 136 482 B · 7,50 s | 1 159 Zeilen: 512 earthquake, 460 *induced or triggered*, **148 mining explosion**, 21 rock burst, 18 explosion |
| ISC, Europa, letzte 3 Tage | 15:26:58 · 200 · 9 491 B | 74 Zeilen, davon 25 mining explosion → **aktuell, nicht 24 Monate im Rückstand** |
| ISC, Oberschlesien, 3 Monate | 15:30:35 · 200 · 99 813 B | **868 Zeilen**, 866 *induced or triggered* (Autor PRU) |
| **ISC, Box um Rüdersdorf (1°×1,2°), 12 Monate** | 15:30:14 · **204 No Content** | **null Zeilen** |
| GEOFON-Eventkatalog, dieselbe Box, 12 Monate | 15:36:08 · **204** | null |
| LMU-Eventkatalog, dieselbe Box, 12 Monate | 15:36:09 · **204** | null |
| USGS ComCat, dieselbe Box, 12 Monate | 15:36:09 · 200 · 327 B | **0 features** |
| **USGS** `eventtype=quarry blast`, 7 Wochen | 15:25:47 · 200 · 218 819 B · 5,34 s | **299 Sprengungen** — ein laufendes, keyless, öffentliches Sprengungsregister … für die USA |
| USGS `quarry blast`, EU-Box, 2 Jahre | 15:26:08 · 200 · 1 061 B | **1 Ereignis** — für Europa existiert es nicht |
| EMSC `seismicportal.eu` event | 15:25:53 · 200 · 27 532 B | keyless, JSON |
| ORFEUS/ODC station · EIDA-Routing | 15:27:00 · 200 · 5 B / 88 B | v1.1.6; Routing GE → `geofon.gfz.de` (ein Adapter, viele Netze — bestätigt) |
| `eida.gfz.de` dataselect · `federator.eida.orfeus-eu.org` | 15:27:00 · 404 · 15:27:18 · **DNS-Fehler** | zwei im Exposé/Umfeld genannte Endpunkte existieren so nicht; ODC-Routing ist der tragfähige Weg |
| RESIF `ws.resif.fr` · INGV `webservices.ingv.it` | 15:27:15 / 15:27:17 · 200 | v1.1.26 / v1.1.64, keyless |
| **BGR** `eida.bgr.de` station GR | 15:29:54 · 200 · 127 B | **199 Stationen seit 1976**, DOI 10.25928/mbx6-hr74 |
| BGR dataselect GR.KAST HHZ 60 s | 15:32:26 · 200 · **7 680 B** | keyless — **aber nur mit `location=--` in Langform**; `loc=*` in Kurzform → 204 |
| **CTBTO** `ctbto.org` (3 Pfade) + `robots.txt` | 15:28:01 · **403** (Cloudflare) | die Website weist *jeden* Maschinenklienten ab, auch `robots.txt`. `vdec.ctbto.org` → 404. **Kein offener Pfad; nicht umgangen** |
| CTBTO indirekt | (aus ISC-Zeilen) | Autor **IDC** (International Data Centre, CTBTO) liefert Zeilen *in* den ISC-Katalog: 9 von 1 159 im Januar-Fenster. **Die Bulletins sickern öffentlich durch, die Daten nicht** |
| **Raspberry Shake** `data.raspberryshake.org` | 15:27:18 · 200 | Netz AM: **27 934 Stationen**, keyless FDSN |
| RS Infraschall-Kanal **HDF**, global | 15:27:30 · 200 · 382 086 B | **851 Stationen, 670 mit offener Epoche** — offener Infraschall existiert |
| RS dataselect AM HDF / EHZ 60 s | 15:27:52 · 200 · **13 824 B** / 9 728 B | keyless, Quality D |
| FDSN-Datenzentren-Register `fdsn.org` | 15:28:35 · 200 · 34 340 B | 32 Datenzentren mit Dienst-URLs — der Panel-Katalog |

**Registrierungs-Disziplin eingehalten:** kein Account angelegt, kein Token beschafft, keine
WAF umgangen. **Und der stärkere Befund: es wäre nichts zu beschaffen gewesen** — jede
tragende Quelle dieses Audits antwortete keyless. Anders als bei Dark Ocean gibt es hier
**keine Eskalation, die auf Franks Knopf wartet.**

## Die sechs Kernbefunde

### 1. Speicher, gemessen: der Rohpfad fällt um drei Größenordnungen, der abgeleitete trägt

| Größe | gemessen |
|---|---|
| 1 Kanal-Tag, 100 Hz | 10 768 896 B (10,27 MiB) |
| 1 Kanal-Tag, 20 Hz | 2 267 136 B (2,16 MiB) |
| 60 s, 100 Hz | 11 264 B |
| WFCatalog-Tagesdokument, 1 Kanal | 1 399 B |
| availability-Zeile, 1 Kanal-Tag | ≈ 130 B |
| gzip-Gewinn auf miniSEED | **Faktor 0,868** — STEIM2 ist schon komprimiert, Git holt 13 % |

**Rohpfad, ein Jahr:** 6 Stationen × 1 Vertikalkanal = 61,6 MiB/Nacht → **21,96 GiB/Jahr**
(in Git ≈ 19,1 GiB). 12 Stationen × 3 Komponenten → **131,8 GiB/Jahr**. Ein Panel in der
Größe der Nachbar-Spec (50 × 3) → **549 GiB/Jahr**. Git hält das nicht — nicht knapp,
sondern um den Faktor 40 bis 1 000 daneben.

**Abgeleiteter Pfad + Ausschnitte, ein Jahr:** je Station-Nacht WFCatalog + availability +
Request-/Hash-Zeile ≈ 1,9 KB, plus **maximal vier 60-s-Ausschnitte** à 11 264 B = 45 KB →
47 KB. Sechs Stationen plus eine Lesung ≈ **342 KB/Nacht → ≈ 125 MB/Jahr.**
**Maßstab aus dem eigenen Haus:** Dark Ocean committet heute gemessen ~1,39 MB/Nacht
(Lesung 109 KB + Snapshots 1,28 MB), also ≈ 507 MB/Jahr. **Planetary Listening wäre ein
Viertel davon.** Git hält es, und zwar mit der Disziplin, die die Praxis schon fährt.

**Was gegenüber dem VERIFY-Versprechen verloren geht — und was nicht.** Bewiesen, nicht
behauptet: die 60-s-Datei liegt **byteidentisch und 512-Byte-record-aligned im Tagesfile**
(Offset 1 035 776). Ein Ausschnitt ist also **keine Ableitung, sondern eine Teilmenge der
Originalbytes des Herausgebers** — VERIFY hält für jede Behauptung, die die Maschine
aufstellt. Verloren gehen 99,72 % der Sekunden (86 160 von 86 400 je Station-Tag): **die
Nicht-Detektionen.** Ein Dritter kann die Falsch-Negativ-Quote nicht aus dem Archiv
nachrechnen, nur durch Neu-Abruf beim Herausgeber. Das ist der ehrliche Preis, und er ist
zulässig, weil das Archiv das Beste behält, was es geben kann: (a) die Originalbytes jeder
Behauptung, (b) das **Herausgeber-Attest über den Rest** (WFCatalog: 21 033 Records,
100 % availability, 0 Lücken, RMS, Timing-Quality), (c) die wörtliche Wiederhol-Anweisung.
Aufs Methodenblatt, nicht wegformuliert: *VERIFY covers what the machine says it heard, not
what it says it did not hear.*

**Nebenfolge für den Aufnahme-Pfad:** dessen Regel „eigenes Repo nur, wenn die Datenform
Git sprengt" nennt Planetary Listening als **den** Beispielfall. Der Fall ist damit
gemessen erledigt: **Default Praxis-Repo**, ein Substrat, ein Verifikator, eine Bühne.

### 2. Provenienz: der Herausgeber beurkundet nichts — aber er datiert seine Umschreibungen

Die dataselect-Antwort trägt **keine Checksumme, kein ETag, kein Last-Modified**, nur
`Transfer-Encoding: chunked` und ein `Content-Disposition`. Das ist die harte Gegenseite zu
CDSE, das je Szene BLAKE3 **und** MD5 selbst beurkundet. Ehrlich benannt: **hier hashen wir
selbst, oder niemand hasht.**

Was der Herausgeber dafür liefert, ist besser als erwartet:
- **Determinismus hält im Kleinen:** dieselbe Anfrage, zweimal, SHA-256 identisch.
- **Qualitätsrevisionen sind nicht das Risiko:** alle 4 428 Records des Tages und alle fünf
  Segmente der 26-jährigen Historie tragen Quality **D**. GEOFON befördert nicht nach Q/M.
- **Das Risiko ist Neu-Einlagerung, und sie ist sichtbar:** `availability/1/extent` zeigt für
  GE.RUE HHZ Segmente der Jahre 2000–2012 mit `Updated` **2022-07-26 / 2022-07-28 /
  2022-10-12**. Das Archiv wurde zehn bis zweiundzwanzig Jahre nach der Aufnahme
  umgeschrieben — und sagt es. `show=latestupdate` committen macht daraus ein
  **detektierbares Ereignis**; genau die Form der Dark-Ocean-Kontinuitätssonde, also das
  eine Bauteil dieses Hauses, das sein E-Experiment überlebt hat.
- **Die Wiederhol-Anweisung ist nicht portabel:** GEOFON antwortet auf Kurzform-Parameter mit
  `loc=--`; BGR gab auf `loc=*` in Kurzform 204 und erst auf `location=--` in Langform 200.
  Committet wird darum die **wörtliche URL je Knoten**, nicht eine kanonische FDSN-Query.

### 3. Der Nachbar im eigenen Haus: die Trennung ist schreibbar

„The Seismic Quiet" (Lab-Spec 2026-08-14, nicht beauftragt) und dieser Kandidat teilen die
Netze und nichts sonst:

| | The Seismic Quiet (Lab) | Planetary Listening (Praxis) |
|---|---|---|
| Gegenstand | der **Untergrund** — anthropogenes Rauschen | der **Vordergrund** — einzelne Impulse |
| Größe | Index in % der eigenen Wochentags-Baseline, 4–14 Hz PSD | eine datierte Zeile: Ort, Uhrzeit, Klasse |
| Panel | ~50 Stationen, global, städtenah | **eine** Anlage, eine Station darauf |
| Operation | Normalisierung gegen sich selbst | **Join gegen ein deklariertes Register** |
| Fällt aus, wenn | die Stille nie kommt | die Register nie widersprechen |

Der Leser unterscheidet sie an den Einzeilern: *„How loud is humanity today, and where did
it fall silent?"* gegen *„Who blasted, when, and which record admits it?"* Ein Thermometer
gegen eine Anwesenheitsliste. **Als Auflage:** Planetary Listening publiziert **keinen
Lautstärke-Index** — täte es das, kollabieren die zwei. Und weil beide dieselbe Fetch-Schicht
brauchen: **die Praxis-`practice/`-Schicht ist die Implementierung**; würde das Lab die Spec
je beauftragen, konsumiert sie diese oder wird abgelehnt. (Kostenlose Gegenleistung an das
Lab: der EIDA-WFCatalog liefert bereits herausgeberseitig ein tägliches `sample_rms` je
Kanal — breitbandig, nicht bandbegrenzt, also nicht der Index, aber ein näherer Nachbar als
die Spec-Nachbarliste kennt.)

### 4. Infraschall: CTBTO ist zu, offener Infraschall ist trotzdem da

CTBTO antwortet einem Maschinenklienten mit 403 — auf jeden Pfad, auch auf `robots.txt`. Es
gibt also nicht nur keinen Datenzugang, sondern **keinen maschinenlesbaren Weg, die
Bedingungen zu lesen.** Der Befund wird notiert, nicht umgangen. Indirekt ist die
Organisation trotzdem öffentlich: **IDC-autorisierte Zeilen stehen im ISC-Katalog** (9 von
1 159 im Januar-Fenster). Die Bulletins sickern durch, die Wellenformen nicht.
Der Einzeiler musste dennoch nicht auf Infraschall verzichten — **670 Raspberry-Boom-HDF-
Stationen mit offener Epoche** liefern keyless Infraschall (13 824 B je 60 s). Für V0 wird
diese Achse **bewusst nicht** gebaut (eine Achse, nicht zwei — Lehre aus Dark Ocean, wo die
zweite Achse in 13 von 13 Nächten nie ankam).

### 5. Die investigative Tiefe kommt nicht aus einem nationalen Register — sie kommt aus dem Regime-Kontrast

Gegenargument 2 der Vorprüfung stimmt in der Prämisse und irrt im Schluss. Geprüft: In
Deutschland ist gewerbliches Sprengen weitgehend **anzeige-, nicht genehmigungspflichtig**,
und wo eine BImSchG-Anlagengenehmigung das Sprengen einschließt, entfällt auch die Anzeige.
Ein zentrales, maschinenlesbares Sprengregister existiert nicht — Compute Grounds Blocker,
im Kleinen, bestätigt.

Aber der Gegenpart muss kein Register sein. **Betreiber deklarieren selbst, und zwar
vorwärtsgerichtet:** Heidelberg Materials publiziert für Geseke einen Sprengkalender mit
konkreten Terminen je Steinbruch und dem Fenster „in der Regel zwischen 10:00 und 12:00
Uhr", rund zehn Termine im Monat über drei Brüche, mit Vorbehalt für Wetter und Betrieb. Das
ist **stärker** als eine Genehmigungsdatenbank: eine eigene, öffentliche, datierte Behauptung
über die Zukunft — genau das, was die Maschine prüfen kann.

Und die Tiefe liegt im Kontrast der Regime, vierfach gemessen: Oberschlesien **868 Zeilen in
drei Monaten**, Rüdersdorf **null Zeilen in zwölf Monaten bei ISC, GEOFON, LMU und USGS** —
während dort täglich gesprengt wird und eine GEOFON-Station mit 100 Hz auf dem Werksgelände
steht. Derselbe Gegenstand, dieselbe Zeit, ein Grenzverlauf.
**E-2-Grenze mitgeschrieben:** Das ist **kein Vorwurf**. Internationale Kataloge schließen
Industriesprengungen durch Magnitudenschwelle und Verfahren *planmäßig* aus; nationale
Dienste erkennen und verwerfen sie. Gegenstand ist die **Bauart der Auslassung**, nicht ein
Verschweigen. Genau so bleibt es die Hausoperation (Regime gegen Regime) und keine Anklage.

### 6. Die USA haben es, Europa nicht — und das ist die USP-Antwort

USGS ComCat führt `eventtype=quarry blast` als laufende Kategorie: **299 Ereignisse in
sieben Wochen**, keyless, maschinenlesbar. Die Detektion ist also nicht neu und die
Publikation auch nicht — für die USA. Für eine EU-Box liefert dieselbe Abfrage über zwei
Jahre **ein** Ereignis. Nächste Nachbarn, benannt: **USGS ComCat** (US-Register,
behördlich); **ISC** mit `mining explosion`/`explosion`/`rock burst` (europäisch, aber als
Aggregat nationaler Beiträge und, wie gemessen, mit weißen Flecken statt Flächendeckung);
**NORSAR/Nature 2023** (Ukraine, 1 200+ Explosionen — Paper, keine laufende Praxis);
**Seismica 2024, Oslo** (Bau- und Steinbruchsprengungen mit Low-Cost-Sensoren und Deep
Learning — Paper); **Lecocq 2020/SeismoRMS** (Rauschen, nicht Ereignisse);
**Raspberry-Shake-StationView** (Anzeige, kein Register).
**Daylight, eng formuliert:** Niemand gefunden, der **eine benannte Anlage gegen ihre eigene
öffentliche Deklaration und gegen die öffentlichen Kataloge stellt, nächtlich, keyless,
append-only, mit Originalbyte-Ausschnitten je Behauptung.** Die Detektion ist Stand der
Technik; der **Join gegen zwei Register** ist die Position.

## Der C4-Test: erste Nachtzahl, und Nacht 14

**Nacht 1, ehrlich:** „GE.RUE, 2026-08-2x, drei impulsive Ereignisse über Schwelle,
Sprengsignatur, Konfidenz mittel; 12:07:14 UTC das stärkste. Öffentliche Kataloge zu diesem
Ort und Tag: null Zeilen (ISC 204, GEOFON 204, LMU 204, USGS 0)."

**Nacht 14 als Journal:** ein **Kalender einer benannten Anlage** — vierzehn Zeilen, je eine
Uhrzeit oder ein Strich, daneben die Spalte „im Register: nein". Die zwingende Zeile ist
nicht eine Quote, sondern ein **Rhythmus und sein Bruch**: an elf Werktagen ein Impuls
zwischen 12:00 und 12:30, an zwei Tagen keiner, an einem Sonntag einer. Ort, Uhr, Kalender —
**keine Überlappungsquote.** Damit ist C4 adressiert, nicht umgangen: die Kopfzahl ist eine
Null **im Register eines Anderen**, gemessen gegen ein Nicht-Null im eigenen. Das ist
kategorial anders als „zwei Register überlappen sich zu X %", weil eine Seite der Rechnung
die Maschine selbst herstellt.

**Der ehrliche Restrisiko-Satz, vor dem Fenster:** Ist die Detektierbarkeit schlecht oder die
Anlage still (Ferien, Umstellung auf Reißen statt Sprengen — für Rüdersdorf berichtet), ist
Nacht 14 ein **leerer Kalender**, und dann ist das Werk ein Instrument. Deshalb Auflage 1:
Die Detektierbarkeit wird **vor** dem Fenster gemessen, nicht vorausgesetzt (E-Review §8.2:
eine Bedingung, die eine unerreichbare Quelle voraussetzt, ist ein Versprechen).

## Ethik — E-2 und die Verweigerung

Die Kriegsachse ist attraktiv und genau deshalb gefährlich: die NORSAR-Arbeit wird
ausdrücklich als mögliche Evidenz für Völkerrechtsverstöße gerahmt. Schriftlich, als
V0-Bedingung:

1. **Deklariertes Theater.** Der Charter nennt Industrieanlagen in EU-Staaten im Frieden.
   Konflikt- und Militärachsen sind nicht gebaut und **nicht per Konfiguration
   einschaltbar** — die Ortsliste liegt im Verifikator, nicht im Config.
2. **Keine Echtzeit für Sensibles.** Industrieachse: nächtlich, T+1 (kein Kombattant
   profitiert von der Sprengzeit eines Steinbruchs). Jede Achse, die einen Konflikt oder
   ein militarisiertes Objekt berührt: **nicht gebaut**; würde sie je gebaut, dann mit
   Latenz ≥ 30 Tage, Ortsauflösung ≥ 0,5°, Zeitauflösung ≥ 1 Tag und menschlichem
   Freigabe-Gate.
3. **Keine Zuschreibung (E-2).** Publizierte Zeile: Signal der Klasse X, Zeit T, Station S;
   Register R enthält / enthält keinen Eintrag. **Nie** wer, nie „illegal", nie
   „ungenehmigt". Das Betreiber-Fenster wird als **Behauptung** zitiert, nicht als Recht.
4. **Keine Personen.** Raspberry-Shake-Stationen stehen in Privatwohnungen; ihre Koordinaten
   sind personennah. Für V0: AM bleibt draußen; käme es je hinein, dann als markierte zweite
   Stufe mit auf 0,1° gerundeten Koordinaten — **vom Verifikator erzwungen**, wie das
   MMSI-Verbot bei Dark Ocean.
5. **Die Verweigerung wird publiziert**, wie im Dark-Ocean-Methodenblatt.

**Was das kostet, ohne Beschönigung:** Es nimmt dem Exposé sein stärkstes Material — den
Bombardement-Rhythmus. Übrig bleibt eine Steinbruch-Anwesenheitsliste, und das ist weniger
dringlich; das muss hier stehen und nicht kleingeredet werden. Der methodische Trost ist
echt, kein Trostpreis: **ein Konflikt hat kein deklariertes Register.** Der Join, der die
ganze Methode ist, hätte dort nichts zu joinen. E-2 und die Methode sagen dasselbe.

## Flagship oder Instrument?

Die vier Kriterien, ehrlich abgehakt: **kontinuierlich lebendig** — ja, gemessen (100 Hz,
100 % availability gestern, 26 Jahre Historie an einer Station). **Maschinell überlegen** —
ja für das ununterbrochene Zuhören und den nächtlichen Join; **nein** für die Detektion, die
Standard-Seismologie und in den USA behördliche Routine ist. **Sinnlich stark** —
potenziell das stärkste aller Kandidaten (echter Schall, echte Stille, ein Kalender, der
sich füllt), aber unbewiesen; die One-Tap-Lehre gilt. **Dringlich** — die schwächste Karte;
der Befund ist epistemisch, kein öffentlicher Notstand.

**Urteil: Instrument, mit benanntem Weg zum Flagship.** Flagship wäre es, wenn vier Dinge
wahr würden: (a) die Maschine hört an einer benannten Anlage ≥ 80 % der deklarierten Termine
— der Kalender füllt sich wirklich; (b) mindestens **eine undeklarierte Zeile** übersteht die
eigene Nachprüfung — eine Zeile, die in keinem Register steht; (c) die Form trägt als Klang
und Stille, geprüft an einem gebauten Entwurf wie Dark Oceans C3; (d) ein **zweiter Ort in
einem zweiten Meldegime**, damit der Befund über Regime spricht und nicht über einen
Steinbruch. Dark Ocean hat im Audit Flagship behauptet und an C4 verloren; dieses Audit
verzichtet vorab. Das ist die angewandte Lehre.

## Go/No-Go

**GO für V0 „One Quarry, Two Records" — mit Auflagen:**

1. **Spike vor dem Fenster (2 Tage, kein Commit-Zwang):** Detektierbarkeit an zwei
   Paarungen messen — (A) **Rüdersdorf**: GE.RUE auf dem Werksgelände, ~1 Sprengung/Tag
   berichtet (unbelegt, die Maschine misst es), Deklarationsseite = die vier öffentlichen
   Kataloge, gemessen null; (B) **Geseke**: publizierter Betreiber-Sprengkalender, nächste
   offene Station GR.KAST in ~49 km plus drei AM-Stationen. Die Paarung wird **gewählt, nicht
   angenommen** — und die Wahl ist selbst ein Befund.
2. **Speichermodell festgeschrieben, nicht nachträglich:** derived + record-aligned
   Originalbyte-Ausschnitte, Obergrenze je Station-Nacht committet (Vorschlag: 4 × 60 s),
   WFCatalog- und availability-Zeile inkl. `Updated` je Kanal-Tag, wörtliche Request-URL je
   Knoten, SHA-256 der empfangenen Bytes. Ziel ≤ 400 KB/Nacht.
3. **Lizenz-Architektur vor dem Bau:** GEOFONs Archiv mischt **CC BY 4.0, CC BY-SA 4.0 und
   CC BY-ND 4.0**. ND und SA können nicht in CC0-Ableitungen fließen. Panel ist
   **lizenzgefiltert**: nur CC BY 4.0 (GE ist CC BY 4.0, DOI 10.14470/TR560404; GR trägt DOI
   10.25928/mbx6-hr74). Netz-DOI und Lizenz stehen **in jedem Record**; die Lizenz ist nicht
   maschinenlesbar abrufbar und wird darum je Netz kuratiert und datiert.
4. **Keine Abhängigkeit von EarthScope-Infrastruktur** (E-Review §8.1): event und
   availability dort sind 410 Gone. Ereignisabgleich läuft über **ISC + USGS** (beide heute
   200), Verfügbarkeit über **GEOFON/BGR availability + WFCatalog**. EarthScope darf
   Wellenformen liefern, aber kein Kriterium tragen.
5. **Kein Lautstärke-Index** (Trennung zum Hausnachbarn, Befund 3) — testgesichert.
6. **Ethik-Auflagen 1–5** oben, im Verifikator, nicht im Wording.
7. **Substrat-Stresstest ist Teil des Auftrags:** `fetch/preserve/autonomy` gegen Binärdaten
   (miniSEED) statt JSON — was bricht, wird als Substrat-Befund committet.

**Kein V0-Bau ohne Franks ausdrückliches Go** — Aufnahme ist das menschliche Gate (E-4/E-6).
Dieses Audit endet hier.

## Offene Entscheidungen (Frank) — keine davon ist ein Account

1. **Go für V0 „One Quarry, Two Records"?** (14-Nächte-Fenster danach, 0 €, keyless)
2. **Paarung:** Rüdersdorf (bestes Hören, null Deklaration) oder Geseke (beste Deklaration,
   unbewiesenes Hören) — oder Spike entscheidet (Empfehlung).
3. **Raspberry-Shake-Stationen überhaupt zulassen?** (Personennähe; Empfehlung: nein für V0)
4. **Wohnort bestätigen: Praxis-Repo** — der im Aufnahme-Pfad genannte Eigen-Repo-Fall ist
   durch Befund 1 gegenstandslos.

## Bewusst nicht (in diesem Audit / in V0)

Kein Account angelegt, kein Token beschafft, **keine CTBTO-WAF umgangen** · keine Detektion
prototypisiert, kein Klassifikator gewählt · keine Bytes konserviert (alle Probes sind hier
beziffert; Konservierung beginnt mit V0) · keine Site-/Bühnenänderung (Öffentlichkeit erst
ab RUNNING) · **kein Rohstream-Archiv** (gemessen: 22–549 GiB/Jahr) · **keine
Infraschall-Achse** in V0 (670 offene HDF-Stationen existieren — bewusst zurückgestellt,
eine Achse statt zweier) · **keine ML-Klassifikation** in V0 (symbolische Schwellen und
publizierte Diskriminanten, auditierbar) · **keine Konflikt- oder Militärachse**, auch nicht
hinter einem Flag · kein Lautstärke-Index · kein zweiter Ort, bevor der erste gemessen ist ·
kein Backfill.
