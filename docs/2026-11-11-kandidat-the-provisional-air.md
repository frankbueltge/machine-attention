# The Provisional Air — Exposé

**Datum:** 2026-11-11 · **Stufe:** EXPOSÉ · **Anlass:** Der Fokus wartet. The Interval hat seine vier
Fensterwochen gelesen und schließt am 2026-11-15 (`interval/experiment.json`; Tally heute mit
`python -m practice.interval.experiment --repo-root .`: A1 keine fehlende Woche, A2 pass, A3 keine,
B1 0, B2 keine Änderung, B6 unverändert, FSC·date·k=2 43/77 gegen 3/7). The Synthetic Flood wartet
auf ihren Workflow am 2026-12-04 (`docs/2026-11-09-synthetic-flood-v0-inkrement-4.md`), Planetary
Listening auf den Review des Maintainers (`REQUESTS.md` 2026-11-04), The Declared Network und The
Afterlife auf `REQUESTS.md` (2026-10-23, 2026-10-30). Laut `discovery/PROMPT.md` Schritt 2 darf dann
ein neues Exposé pro Woche entstehen; in der ISO-Woche 46 ist keines entstanden, das letzte war The
Afterlife am 2026-10-29 (`docs/2026-10-29-kandidat-the-afterlife.md`). Dies ist das Exposé dieser Woche.

Jede Aussage über Formate, Lizenzen, Raten und das Überschreibverhalten der Quellen ist
**ungeprüft** und gehört dem AUDIT. Geprüft ist heute nur, was §5 und §6 nennen: je Adresse ein
Status-Abruf und, neu, die `robots.txt` jedes Hosts, den V0 lesen würde (2026-11-11, 07:3x–07:4x
UTC). Keine Messdaten gelesen, keine Bytes konserviert, keine Zahl aus einer Antwort übernommen.

## 0. Warum diesmal die `robots.txt` schon im Exposé steht

Zwei der drei wartenden Kandidaten sind an derselben Stelle stehen geblieben, und beide erst im
AUDIT: OSCAR/Surface (`declarednetwork/probes/2026-10-23/oscar/robots.txt`) und PubMed
E-utilities (`afterlife/probes/2026-10-30/pubmed/robots.txt`), jeweils `Disallow: /` für jeden
Agenten. Ein Exposé, dessen Hauptquelle Robotern das Lesen verbietet, verbraucht eine Woche und
ein Audit, um an einer Tür zu enden, die man vorher hätte sehen können. Diese Vorprüfung ist ein
Abruf je Host und entscheidet nichts; sie sagt nur, ob ein AUDIT sich lohnt.

## 1. Die Frage

> Wie viel von dem, was der Öffentlichkeit an einem Tag über ihre Luft gesagt wurde, übersteht
> die Validierung — und an welchen Tagen nicht?

Europäische Messnetze liefern Luftqualitätswerte zweimal. Zuerst **vorläufig**, Stunden nach der
Messung, als „up-to-date"-Datenfluss (E2a): aus ihm speisen sich Indexkarten, Warnungen,
Nachrichten des Tages. Dann **validiert**, im Jahr darauf, als E1a — das ist der Wert, an dem
Grenzwertüberschreitungen nach der Luftqualitätsrichtlinie amtlich gezählt werden. Zwischen
beiden liegen Monate; nach Kenntnis der Praxis wird der vorläufige Wert dabei auch vor der
Validierung mehrfach neu geliefert (ungeprüft, AUDIT).

Das ist die Operation des Gründungskorpus (`docs/2026-08-08-projekt-aufnahme.md`): eine
öffentliche Darstellung eines Zustands neben einer späteren Darstellung desselben Zustands.
Diesmal nicht *erklärt ≠ verbreitet* wie bei The Afterlife, sondern **gesagt ≠ festgestellt**:
Die Messgröße ist die **Validierungsdifferenz** je Station × Schadstoff × Tag — und vor allem die
Tage, an denen sie die Seite einer Schwelle wechselt: ein vorläufig gemeldeter
Überschreitungstag, der validiert keiner ist, und einer, den vorläufig niemand sah.

## 2. Warum nur anhaltende maschinelle Aufmerksamkeit das beantworten kann

- **Der vorläufige Wert wird überschrieben.** Wenn ein Wert neu geliefert wird, ersetzt die neue
  Lieferung die alte im Download (ungeprüft, AUDIT — die zentrale Prüfung). Was an einem Dienstag
  um 09:00 öffentlich stand, existiert danach nur, wenn jemand es an diesem Dienstag gesichert hat.
  Das ist die Lehre von Memory Hole und der Kern von The State Before the Interface.
- **Die Validierung kommt Monate später.** Wer den Vergleich ziehen will, muss den Tageswert ein
  Jahr lang mit Hash festhalten und dann den validierten danebenlegen. Diese Geduld hat keine
  Person, und die Betreiber haben keinen Grund, ihre eigenen Revisionen zu zählen.
- **Rückwirkend nur zur Hälfte.** Gibt der Download alte E2a-Lieferungen noch heraus, lässt sich
  die Differenz *letzte vorläufige Fassung ↔ validiert* auch rückwirkend messen — dann schrumpft
  das Tageslicht auf die **Zwischenrevisionen** und auf das, was am Tag selbst stand. Das AUDIT
  muss das zuerst klären, und das Ergebnis steht in jeder späteren Ausgabe.
- **Wiederholbarkeit.** Jeder Tageswert wird mit dem SHA-256 der empfangenen Datei festgehalten,
  wie `verify.py` es für die Lesungen von The Interval und der Synthetic Flood tut.

## 3. Datenlage-Kurzcheck (ungeprüft, für das AUDIT)

| Seite | Kandidat-Quelle | Was das AUDIT klären muss |
|---|---|---|
| Vorläufig und validiert | EEA Parquet-Download-API, `eeadmz1-downloads-api-appservice.azurewebsites.net` (Swagger 200; Pfade u. a. `/ParquetFile/urls`, `/DownloadSummary`, `/Pollutant`; Anfragefeld `dataset` als Ganzzahl) | Welcher `dataset`-Wert E2a, welcher E1a ist; ob E2a nach einer Neulieferung die alte Fassung noch herausgibt; Größe eines Tagesabrufs für einen festen Stationssatz; Rate; Lizenz. **Das Anfragefeld `email` wird nie gesetzt** (personenbezogen; die Praxis sendet keine Adresse). |
| Vorläufig, national | Umweltbundesamt Luftdaten-API v3, `luftdaten.umweltbundesamt.de/api/air-data/v3/` (meta 200, 29 B) | Ob die nationale Stunde dieselbe ist, die an die EEA geht; ob sie als Kontrolle taugt (eine zweite Hand für denselben vorläufigen Wert). Nur als Kontrolle, nicht als zweite Hauptquelle. |
| Dokumentation | European Air Quality Portal, Berichtsleitfaden (`eeadata.github.io/AQ.Portal/`, 200) | Definitionen von E2a/E1a, Lieferfristen, ob ein Wert ein Lieferdatum trägt. |

**Rückwirkend:** Die validierte Seite ist es vollständig. Die vorläufige ist es nur, soweit der
Download alte Fassungen behält — siehe §2.

## 4. V0-Skizze (nur Form, keine Festlegung)

Einheit: **Station × Schadstoff × Tag**, verdichtet zu **Land × Schadstoff × Monat**. Ein fester,
vorab committeter Stationssatz (Größenordnung: einige hundert Stationen, PM10 und NO2, weil für
beide Tagesschwellen gelten), jede Nacht der vorläufige Stand der letzten sieben Tage, mit Hash.
Ereignisse: `first_seen`, `revised` (eine vorläufige Fassung ersetzt eine andere), `withdrawn`
(ein vorläufiger Wert verschwindet), später `validated` mit der Differenz und dem Flag
`crossed` (Schwellenseite gewechselt). Die Differenz wird als Verteilung berichtet, nie als
einzelne Zahl. Erst ab dem ersten Validierungsjahrgang nach V0-Beginn gibt es eine Differenz; bis
dahin misst das Instrument nur Zwischenrevisionen. Die Klasse ist vermutlich **Instrument**.

Substrat: Lesen und Sichern wie The Interval (`practice/src/practice/interval/`); ein Parquet-Leser
wäre neu und muss zeigen, dass er ohne zusätzliche Abhängigkeit auskommt oder sie rechtfertigt.

## 5. Die nächsten Nachbarn, und das Tageslicht

| Nachbar | Was er tut | Tageslicht | Erreichbar 2026-11-11 |
|---|---|---|---|
| [ETC/ATNI-Bericht 11/2020](https://www.eionet.europa.eu/etcs/etc-atni/products/etc-atni-reports/etc-atni-report-11-2020-european-air-quality-interim-mapping-under-etc-atni-evaluation-of-aq-mapping-using-utd-measurement-and-cams-forecast-modelling-data-an-approach-for-more-timely-european-aq-annual-maps) ([Zenodo](https://zenodo.org/records/6368242)) | Baut Jahreskarten aus vorläufigen Daten und prüft sie gegen die validierten. | **Der nächste Nachbar.** Er vergleicht Jahreskennzahlen auf Karten, einmal je Jahrgang; er vergleicht weder Tage noch Zwischenfassungen, und er hält nicht fest, was an einem Tag öffentlich stand. | 200 / 200 |
| [ETC HE-Bericht 4/2022](https://www.eionet.europa.eu/etcs/etc-he/products/etc-he-products/etc-he-reports/etc-he-report-2022-4-interim-european-air-quality-maps-for-2021-pm10-no2-and-ozone-spatial-estimates-based-on-non-validated-utd-data) | Vorläufige Jahreskarten 2021 aus nicht validierten Daten. | Dieselbe Richtung, dieselbe Auflösung (Jahr, Karte). Die Tagesgranularität und die Schwellenwechsel fehlen. | 200 |
| [Europäischer Luftqualitätsindex](https://airindex.eea.europa.eu/AQI/index.html) | Zeigt stündlich den vorläufigen Stand. | Er ist die Seite *gesagt* selbst. Er zeigt nicht, was er gestern zeigte, und nicht, was davon validiert bleibt. | 200 |
| [OpenAQ](https://openaq.org/) ([Dokumentation](https://docs.openaq.org/)) | Sammelt vorläufige Messwerte vieler Netze und hält sie historisch vor. | **Der Nachbar, der am meisten Tageslicht nehmen kann.** Behält er die zuerst gesehene Fassung, existiert ein Teil des „Vorher" schon. Ob er Neulieferungen überschreibt, ob er Fassungen datiert und ob er gegen E1a vergleicht, muss das AUDIT an seiner Dokumentation prüfen, nicht an seiner Schnittstelle (die einen Schlüssel verlangt, nach Kenntnis der Praxis — ungeprüft). | 200 / 200 |
| [Copernicus Atmosphere Monitoring Service](https://atmosphere.copernicus.eu/) | Nutzt vorläufige Messungen für Analyse und Vorhersage. | Ein Verbraucher des vorläufigen Werts, kein Prüfer. Zeigt, wie weit der vorläufige Wert wirkt, bevor er validiert ist. | 200 |
| [Luftqualitätsrichtlinie 2008/50/EG](https://eur-lex.europa.eu/eli/dir/2008/50/oj) | Legt die Tagesschwellen und das Zählen der Überschreitungstage fest. | Regel, nicht Verlauf. Sie zählt am validierten Wert; der öffentliche Tag läuft am vorläufigen. | 202 |

## 6. Vorprüfung der Roboter-Regeln (je Host ein Abruf)

| Host | `robots.txt` | Bedeutung für V0 |
|---|---|---|
| `eeadmz1-downloads-api-appservice.azurewebsites.net` | 404, keine Datei | Keine Bitte an Roboter. Die Hauptquelle steht offen, soweit das ein Abruf sagen kann. |
| `eeadmz1-downloads-webapp.azurewebsites.net` | 403 (auch die Startseite) | Die Web-Oberfläche des Downloads; V0 braucht sie nicht. |
| `luftdaten.umweltbundesamt.de` | 200; sperrt Verwaltungs-, Such- und Anmeldepfade, nicht `/api/` | Die Kontrolle steht offen. |
| `www.eea.europa.eu` | 200; `Disallow: /api` | Gilt für diesen Host, nicht für den Download-Host; V0 liest `www.eea.europa.eu/api` nicht. Das AUDIT hält die Abgrenzung schriftlich fest. |
| `discomap.eea.europa.eu` | 404 | — |

Damit fällt dieser Kandidat nicht an der Tür, an der The Declared Network und The Afterlife
stehen. Bewiesen ist damit nichts über Lizenz und Rate.

## 7. Grenzen, ehrlich

- **Keine Anschuldigung (E-2).** Dass ein vorläufiger Wert sich ändert, ist der Zweck der
  Validierung, kein Fehler. Gemessen wird, wie viel sich ändert und an welchen Tagen es die
  öffentliche Aussage umkehrt; kein Messnetz wird als Einzelner bewertet, nur Länder als Aggregat.
- **Keine Personen (I8).** Stationen, Schadstoffe, Werte. Keine Kontaktfelder der Netzbetreiber;
  das Anfragefeld `email` bleibt leer.
- **Lange Uhr.** Die erste Validierungsdifferenz entsteht frühestens mit dem Jahrgang, den V0
  vorläufig gelesen hat — also nicht vor 2027/2028. Bis dahin berichtet das Instrument nur
  Zwischenrevisionen, und das steht neben jeder Ausgabe. Ein E-Experiment über 14 Nächte kann nur
  diese Hälfte prüfen.
- **Nähe zu The Interval.** Auch dort wird eine erste öffentliche Darstellung gegen eine spätere
  gelesen (Projektion gegen Finanzierung). Die Bauform ist verwandt, der Gegenstand nicht; das
  AUDIT sagt, wie viel Code geteilt werden kann.
- **Wenn OpenAQ die erste Fassung schon hält,** bleibt als Tageslicht nur die Datierung der
  Zwischenrevisionen und der Hash-gebundene Vergleich mit E1a. Reicht das nicht, endet der
  Kandidat im AUDIT, und das ist ein gültiges Ende.

## 8. Was das AUDIT prüfen muss

Für den EEA-Download und die UBA-Luftdaten je: exakter Endpunkt, HTTP-Status, Größe eines
Tagesabrufs für einen festen Stationssatz, Rate ohne Schlüssel, Lizenz, Bitten an automatisierte
Abrufer, ob innerhalb der Delegations-Charta (öffentlich, ohne Login, ohne Kosten, ohne
personenbezogene Daten), und eine Probe mit Manifest unter `provisionalair/probes/<date>/`.
Zuerst und entscheidend: **ob eine E2a-Neulieferung die alte Fassung im Download ersetzt** (zwei
Abrufe desselben Tages im Abstand von Tagen, Hash-Vergleich) — ohne Überschreiben ist der Kandidat
zur Hälfte rückwirkend und das Exposé muss das sagen. Außerdem: welche `dataset`-Ganzzahl welchem
Datenfluss entspricht; ob Werte ein Liefer- oder Validierungsdatum tragen; was OpenAQ laut seiner
Dokumentation mit Neulieferungen tut. Am Ende steht eine Empfehlung. Das GO für V0 ist laut
Aufnahme-Pfad das des Maintainers; das AUDIT braucht es nicht.

## Bewusst nicht heute

Keine Messdaten abgefragt, kein Parquet geladen, kein zweiter Versuch, keine Bytes konserviert,
kein Code, kein Verzeichnis `provisionalair/`. Kein Stationssatz, kein Schadstoff, keine Schwelle
festgelegt. Der Fokus ist unberührt. Ob ein vierter wartender Kandidat der Praxis dient oder sie
zerstreut, ist offen; dieser hier ist der erste, der die Roboter-Vorprüfung vor dem AUDIT besteht,
und das AUDIT kommt erst, wenn kein früherer Kandidat einen fälligen Schritt hat.
