# The Declared Network — Exposé

**Datum:** 2026-10-23 · **Stufe:** EXPOSÉ · **Anlass:** Der Fokus wartet. The Interval steht in
seinem Fenster und hat freitags nichts fällig (`interval/experiment.json`, Wochen 2026-10-19 bis
2026-11-09). Seine offene Treiber-Frage wartet auf die Antwort in `REQUESTS.md` (2026-10-22).
Planetary Listening läuft in seinem eigenen Fenster (`planetary/experiment.json`). The Synthetic
Flood wartet auf die Lesung M+2 ab 2026-11-01 (`discovery/AGENDA.md`). Laut
`discovery/PROMPT.md` Schritt 2 darf dann ein neues Exposé pro Woche entstehen. Seit dem
2026-10-04 ist keines entstanden; das Exposé der Synthetic Flood vom 2026-10-16 erneuerte nur
einen alten Kandidaten. Dies ist das Exposé dieser Woche.

Jede Aussage über Endpunkte, Formate, Lizenzen und Raten ist **ungeprüft** und gehört dem AUDIT.
Geprüft ist heute nur, dass die Adressen der Nachbarn unten erreichbar sind: einmaliger
Status-Abruf am 2026-10-23, Ergebnisse in §5. Keine Bytes wurden konserviert, keine
Stationsliste wurde gelesen.

## 1. Die Frage

> Wie lange bleibt eine Wetterstation im amtlichen Register als „in Betrieb" erklärt, nachdem sie
> verstummt ist, und wo auf der Erde wird das Beobachtungsnetz dünner, ohne dass das Register es
> sagt?

Das ist die Operation des Gründungskorpus (`docs/2026-08-08-projekt-aufnahme.md`, Nachtrag
„Founding Corpus"): eine öffentliche Darstellung eines Zustands neben einer anderen, technisch
beobachtbaren Version desselben Zustands. In Ghost Fleet hieß das: deklariert ≠ physisch
sichtbar. Hier heißt es: **deklariert ≠ geliefert.** Das Register ist das Stationsverzeichnis der
WMO (OSCAR/Surface): Station, Status, erklärter Meldeplan. Die Lieferung ist das, was tatsächlich
im internationalen Austausch ankommt. Die Messgröße ist die **Erklärungs-Nachlaufzeit**: die Tage
zwischen dem letzten gelieferten Bericht einer Station und dem Tag, an dem ihr Registereintrag
den Betrieb nicht mehr behauptet. Bei Stationen, die nie aus dem Register fallen, bleibt die Uhr
offen, wie bei den laufenden Episoden von The Interval
(`docs/2026-10-04-kandidat-the-interval.md` §3.5).

Eine zweite Frage hängt an derselben Messung. Sie zeigt eine Verwandtschaft mit The Interval,
ohne dessen Gegenstand zu teilen: Seit 2022 finanziert ein multilateraler Fonds (SOFF) den Ausbau
des Grundnetzes (GBON) in Ländern mit großen Lücken. **Wie lange braucht finanzierte Beobachtung,
bis sie im Austausch ankommt?** The Interval misst die Zeit von der Warnung bis zum Geld. Diese
Frage misst die Zeit vom Geld bis zur Messung. Sie ist für V0 ausdrücklich **nicht** Gegenstand
(§6), steht hier aber, weil sie die Messreihe später trägt, wenn die erste Frage hält.

## 2. Warum nur anhaltende maschinelle Aufmerksamkeit das beantworten kann

- **Schweigen ist in keinem Schnappschuss sichtbar.** Ein Register sagt am Tag X „in Betrieb",
  eine Lieferstatistik sagt am Tag X „nichts angekommen". Ob das ein Ausfall von Stunden ist oder
  der Anfang vom Ende, zeigt erst die Reihe. Dasselbe gilt für die Nachlaufzeit: Man misst sie
  nur, wenn man beide Seiten jeden Tag festgehalten hat, bevor das Register korrigiert wird. Nach
  der Korrektur ist der alte Zustand aus dem Register verschwunden. Das ist die Lehre von Memory
  Hole (`docs/2026-08-15-memory-hole-v0.md`): Was überschrieben wird, existiert nur, wenn jemand
  es vorher gesichert hat.
- **Die Arbeit ist Zählen über Zehntausende Stationen, täglich, ohne Ende.** Das ist
  Aufmerksamkeit, die keine Person aufbringt. Ein Betriebswerkzeug sieht sie nicht vor, denn es
  zeigt, was heute fehlt, nicht seit wann das Register etwas Falsches sagt.
- **Wiederholbarkeit.** Jeder Tageswert wird mit den SHA-256 der empfangenen Bytes festgehalten.
  So kann ein Dritter Monate später nachzählen, wann eine Station verstummte und wann das
  Register es nachtrug. `verify.py` hält heute schon dieselbe Disziplin für Memory Hole und
  Planetary Listening.

## 3. Datenlage-Kurzcheck (ungeprüft, für das AUDIT)

| Seite | Kandidat-Quelle | Was das AUDIT klären muss |
|---|---|---|
| Register | OSCAR/Surface (`oscar.wmo.int/surface/`, Seite 200 am 2026-10-23); eine öffentliche, schlüsselfreie Such- oder Export-Schnittstelle wird vermutet | Endpunkt, Größe eines Vollexports, ob Statusfeld und erklärter Meldeplan maschinenlesbar sind, Lizenz, Rate. **Personendaten:** Stationseinträge können Kontaktpersonen tragen. Diese Felder werden nie gelesen und nie gesichert (I8). Lässt der Export sie nicht weg, ist das ein AUDIT-Befund gegen die Quelle. |
| Lieferung, amtlich | WDQMS (`wdqms.wmo.int`, Seite 200), sechsstündliche Verfügbarkeit je Station aus vier globalen Zentren | ob es einen schlüsselfreien Download gibt (Tages- oder Sechsstundendatei je Variable), wie weit er zurückreicht, Lizenz. Wenn ja, ist das die Lieferseite. |
| Lieferung, unabhängig | GHCN-Daily von NOAA NCEI (Seite 200), Stationsinventar mit erster und letzter Beobachtung und tägliche Aktualisierung | ob das Inventar täglich neu geschrieben wird, Größe, Lizenz (vermutlich gemeinfrei). Kontrolle, nicht Hauptachse: GHCN sammelt auch nachträglich ein, und sein „letzter Tag" ist deshalb revisionsanfällig. Die Revision wäre ein verglichenes Ereignis, wie bei der Synthetic Flood (`docs/2026-10-16-synthetic-flood-expose-achse.md` §3). |

**Rückwirkend:** Ein Teil der Reihe könnte am ersten Tag aus Inventar-Erst- und Letztdaten
rekonstruiert werden. Die Nachlaufzeit des Registers ist **nicht** rückwirkend messbar, weil das
Register seine eigene Historie vermutlich nicht veröffentlicht. Die Messung beginnt dort also bei
null, und das steht so in jeder späteren Ausgabe.

## 4. V0-Skizze (nur Form, keine Festlegung)

Einheit: **Station × Tag**, verdichtet zu **Land × Monat**. Täglich ein Registerabzug, reduziert
auf Stationskennung (WIGOS-ID), Status und erklärten Plan. Dazu je Station die gelieferte Menge
des Vortags. Committet werden nur abgeleitete Zeilen, SHA-256 der Rohantwort und die
Wiederholungsanweisung. Rohantworten werden nur gesichert, wenn ihre Größe in Git trägt; das
klärt das AUDIT, mit der Obergrenze aus Planetary Listening A4 (400 KB je Nacht) als Richtwert.
Ereignisse: `fell_silent` (n Tage ohne Lieferung bei erklärtem Betrieb, n festgelegt vor dem
ersten Abruf), `undeclared` (Register nimmt den Betrieb zurück), `revived`. Die Nachlaufzeit ist
`undeclared − fell_silent`, als Gitter über mehrere n, nie als einzelne Zahl. Die Klasse ist
vermutlich **Instrument**, nicht Flagship: Die Messung kann tragen, ohne eine Bühne zu verlangen.

## 5. Die nächsten Nachbarn, und das Tageslicht

| Nachbar | Was er tut | Tageslicht | Erreichbar 2026-10-23 |
|---|---|---|---|
| [WDQMS](https://wdqms.wmo.int/), das Überwachungswerkzeug der WMO, mit ECMWF seit 2020 ([Ankündigung](https://www.ecmwf.int/node/25208)) | Vergleicht empfangene mit erwarteten Beobachtungen nach dem in OSCAR/Surface erklärten Plan, sechsstündlich, je Station. | **Der nächste Nachbar, und er misst die Lieferseite selbst.** Er ist ein Betriebswerkzeug für das Heute: Die Ampel zeigt, wer jetzt nicht liefert. Er misst nicht, wie lange das Register danach den Betrieb weiter behauptet. Es gibt kein öffentlich verifizierbares, datiertes Archiv beider Seiten (ungeprüft, AUDIT). Die Praxis würde WDQMS lesen, nicht ersetzen. | 200 |
| [OSCAR/Surface](https://oscar.wmo.int/surface/) | Das Register selbst. | Es zeigt den heutigen Stand, nicht wie lange es ihn schon zeigt. | 200 |
| GBON-Lückenanalyse der WMO (Juni 2023) und [SOFF-Fondsbericht 2025](https://mptf.undp.org/sites/default/files/documents/2026-05/soff_fund_report_2025.pdf) | Einmalige Bestandsaufnahme, wie viel des geforderten Grundnetzes geliefert wird; Berichte über finanzierte Länder. | Zeitpunkte, keine Reihe. Die Nachlaufzeit kommt nicht vor. | 200 (Bericht) |
| [IPCC AR6 WG II, Abb. 9.15](https://ipcc.ch/report/ar6/wg2/figures/chapter-9/figure-9-015) nach Carter et al. (2020) | Rückgang der betriebenen Stationen in Afrika seit etwa 1998. | Rückschau über Jahrzehnte mit Jahresauflösung, aus Klimadatensätzen, nicht aus dem Register. | 200 |
| [„Building better weather networks"](https://eos.org/features/building-better-weather-networks), Eos | Bericht über den Schwund afrikanischer Stationen und seine Ursachen, darunter Konflikt. | Erzählung, keine Messreihe. | 200 |
| [GHCN-Daily](https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily) | Klimadatensatz mit Stationsinventar. | Sammelt nachträglich, kennt das Register nicht. Hier ist er Kontrolle (§3). | 200 |

Unter einer früher gefundenen Adresse der WMO-Werkzeugseite (`community.wmo.int/wigos-tools`)
antwortete der Server mit 404, die Seite des Fonds (`www.un-soff.org`) gar nicht. Beide stehen
deshalb nicht in der Tabelle.

## 6. Grenzen, ehrlich

- **Keine Anschuldigung (E-2).** Ein verstummter Sender kann Strom, Leitung, Krieg,
  Geld oder ein Formatwechsel sein. Ein nachlaufendes Register kann schlicht ein Register sein,
  das jemand einmal im Jahr pflegt. Die Praxis misst die Nachlaufzeit und benennt keinen
  Schuldigen. Länder erscheinen als Aggregat. Stationen erscheinen mit ihrer öffentlichen
  WIGOS-ID, Kontaktpersonen nie (I8).
- **„Nicht angekommen" ist nicht „nicht gemessen".** Eine Station kann messen und national
  speichern, ohne international zu liefern. Die Frage handelt vom Austausch, und das steht neben
  jeder Zahl.
- **Formatwechsel** (Umstellung alter Meldeformate) erzeugen Schein-Schweigen. Das AUDIT muss
  zeigen, ob die Lieferseite sie erkennbar macht.
- **Die SOFF-Frage** (§1) ist für V0 ausgeschlossen. Sie verlangt eine Zuordnung von Geld zu
  Stationen, die öffentlich vermutlich nicht maschinenlesbar ist, und sie liegt nahe an einer
  Bewertung von Ländern. Sie wird erst gestellt, wenn die erste Messung hält.

## 7. Was das AUDIT prüfen muss

Für OSCAR/Surface, WDQMS und GHCN-Daily je: exakter Endpunkt, HTTP-Status, Größe eines Tagesabrufs,
Ratengrenze ohne Schlüssel, Lizenz, `robots.txt` und etwaige Bitten an automatisierte Abrufer
(Lehre aus FEWS NET, `docs/2026-10-04-kandidat-the-interval.md` §2), ob innerhalb der
Delegations-Charta (öffentlich, ohne Login, ohne Kosten, ohne personenbezogene Daten), und eine
Probe mit Manifest unter `declarednetwork/probes/<date>/`. Außerdem: ob sich Register und
Lieferung über dieselbe Stationskennung verbinden lassen, und ob das Register irgendwo seine eigene
Änderungshistorie zeigt. Am Ende steht eine Empfehlung. Das GO für V0 ist laut Aufnahme-Pfad das
des Maintainers. Das AUDIT selbst braucht es nicht.

## Bewusst nicht heute

Keine Quelle abgefragt außer einem Status-Abruf je Nachbaradresse. Keine Bytes konserviert, kein
Code, kein Verzeichnis `declarednetwork/`. Keine Schwelle n festgelegt, keine Länderauswahl
getroffen. Die SOFF-Frage nicht gestellt. Der Fokus ist unberührt.
