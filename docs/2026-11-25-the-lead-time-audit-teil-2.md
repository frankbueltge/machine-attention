# The Lead Time — AUDIT, Teil 2

**Datum:** 2026-11-25 · **Stufe:** AUDIT (Teil 2 von 2, abgeschlossen) · **Exposé:**
`docs/2026-11-23-kandidat-the-lead-time.md` · **Teil 1:** `docs/2026-11-24-the-lead-time-audit-teil-1.md` ·
**Proben:** `leadtime/probes/2026-11-25/manifest.json` (176 konservierte Abrufe, je ein Versuch, kein
Wiederholen, 07:39:45–07:44:26 UTC; dazu 1 nicht konservierter, §5).

**Anlass.** Unverändert seit gestern: alle früheren Kandidaten mit einem nächsten Schritt warten auf ein
Tor des Maintainers (The Interval, Review 2026-11-16; Planetary Listening, Review 2026-11-04; The
Provisional Air, GO 2026-11-17; The Shortage Clock, GO 2026-11-21 und Lizenz 2026-11-20). Teil 2 musste
vor 2026-11-26 ≈ 07:30 UTC laufen, solange die letzte Differenz von Teil 1 (`…20261124073639…`) noch in
der Liste steht (`discovery/AGENDA.md`, The Lead Time, nächster Schritt vom 2026-11-24).

Teil 2 prüft die drei offenen Punkte aus Teil 1 §7: (1) schließt eine Lesung je Tag lückenlos an die
vorige an, (2) trägt das Digitalarchiv des Met Office Stufe, Fenster und Gebiet lesbar, (3) Meteoalarms
Weitergabebedingungen.

## 1. Der Tagestakt, an einer zweiten Lesung bewiesen

Konserviert unter `leadtime/probes/2026-11-25/dwd/`: die Listen `DISTRICT_DWD_DIFF/` und
`DISTRICT_DWD_STAT/` (Stand 07:39 UTC), **alle 158 deutschen Kreis-Differenzen nach
`…20261124073639…`** (von `…20261124074703…` bis `…20261125073057…`, 844 710 B, 123 davon leer mit
22 B) und der jüngste Vollstand **C** = `…20261125073056…STATUS…DISTRICT_DE.zip` (24 Meldungen).

1. **Die Liste überlappt.** Sie reicht heute von `…20261123074253…` bis `…20261125073057…` (316 deutsche
   Differenzen, ≈ 48 h) und enthält `…20261124073639…`, die letzte Datei von Teil 1, noch. Die erste neue
   Datei folgt ihr nach 10,4 min. Über beide Proben zusammen (289 Differenzen,
   2026-11-23 11:30 → 2026-11-25 07:30 UTC) ist der größte Abstand 12,1 min, der Median 10,7 min: **keine
   Lücke**.
2. **Rekonstruktion über die Nacht.** Vollstand B aus Teil 1 (40 Meldungen) plus die 158 neuen
   Differenzen, angewandt mit derselben Regel wie in Teil 1 §3.1 (hinzufügen, Vorgängerin in `references`
   entfernen, `expires` ≤ Dateizeit entfernen), ergibt **genau die 24 Kennungen von C**: 0 fehlend,
   0 zu viel. Die Differenz `…073057…` liegt eine Sekunde nach C und gehört zu ihm.
3. **Ketten.** Alle 5 Verweise von C und alle Verweise der neuen Meldungen lösen sich in den Differenzen
   beider Proben auf (0 offen). Jede Meldung von C steht in einer Differenz.
4. **Was neu sichtbar wurde: Testmeldungen.** Von 68 verschiedenen Meldungen der neuen Differenzen tragen
   **9 `status` `Test`** (Ereignis `TEST-WARNUNG`, 5 `Alert`, 4 `Update`); keine steht in C. Teil 1
   hatte keine. **V0 muss nach `status` = `Actual` filtern**, sonst zählen Testläufe als Warnungen und
   ihre vorzeitigen Enden als Aufhebungen.
5. **Form der Nacht, nur `Actual` (59 Meldungen: 35 `Alert`, 24 `Update`).** 9 Vorgängerinnen mit
   mehreren Nachfolgerinnen (bis 3), 0 Zusammenführungen; von 24 Übergängen verkleinern 19 das Gebiet,
   0 vergrößern es; **8 vorzeitige Enden** (`Update` mit `expires` = `sent`), 0 `Cancel`. `onset` −
   `sent` der Wurzeln 0 bis 6,3 h, 11 mit 0. Wieder alle `severity` `Minor` (Nebel, Frost, Glätte, Böen):
   **keine Hochstufung in zwei Nächten** — die Messgröße (b) bleibt am deutschen Material ungeprüft. Kein
   Wert, keine Verteilung: zwei Novembernächte.

**Antwort auf Teil 1 §7.1:** Eine Lesung je Tag genügt, jetzt an zwei Lesungen gezeigt, nicht nur aus
einer Liste geschlossen. Aufwand der Nacht: 161 konservierte Abrufe an `opendata.dwd.de`, 1,8 MB (davon 0,57 MB die zwei Listen). Reserve: eine
ausgefallene Lesung lässt sich am Folgetag nachholen, zwei nicht.

## 2. Das Met-Office-Archiv: maschinenlesbarer als gedacht

Weg (alle Abrufe 200; die Seiten als Linklisten konserviert, `metoffice/*.links.txt`): Bibliotheksseite →
`digital.nmla.metoffice.gov.uk/SO_c66eb279-…/` („National Severe Weather Warning Service", Rechte:
**„Available under Open Government Licence"**, `collection.links.txt`) → Ordner „Next Generation NSWWS"
(Jahre 2018–2026) → 2025 → 202501 → 20250101. Beide Hosts (`digital.nmla.metoffice.gov.uk`,
`metoffice.access.preservica.com`) sperren in `robots.txt` nur `/wp-admin/`.

1. **Jahresmetadaten als Tabelle.** Der Jahresordner 2025 hält neben den Monaten ein Objekt
   `NSWWS_Metadata_2025` — eine Arbeitsmappe mit einer Zeile **je Datei, also je Aktualisierung**:
   Kennung (Code, Ausgabezeit, Farbe, Element im Namen), ursprüngliches Ausgabedatum, Farbe, Element,
   Regionen. Konserviert als CSV der 422 Datenzeilen (`metoffice/nswws-metadata-2025.csv`; Hinweisblatt,
   Kontaktzeilen und Bilder weggelassen, `full_sha256` der Mappe im Manifest). Gezählt: **239 Warnungen,
   422 Dateien, 128 mit Aktualisierungen** (bis 6 Dateien); Farben 376 Gelb, 43 Orange, 3 Rot. Von 183
   Übergängen zwischen aufeinanderfolgenden Dateien einer Warnung: **2 Hochstufungen**, 0 Herabstufungen,
   181 gleich; Regionen 26 enger, 29 weiter, 113 gleich, 15 verschoben. Farbe im Namen und in der Spalte
   stimmen in allen 422 Zeilen überein.
2. **Das PDF trägt Fenster und Ausgabezeit als Text.** Eine Datei geladen
   (`…cb7ef0b6-…_20250101_1112_Y_Sn`, 4 Seiten, 302 724 B; konserviert als Textschicht,
   `metoffice/NSWWS_cb7ef0b6-…_Y_Sn.txt`, Telefon und Adresse des Wetterdesks ersetzt): „Yellow warning
   Snow", „Between 12:00 Sat 4 Jan 2025 and 09:00 Mon 6 Jan 2025", „Issued at 11:12 Wed 1 Jan, 2025",
   Regionen und Behörden auf Seite 3–4. **Vorlauf dieser einen Warnung: 72 h 48 min** — eine Größenordnung
   über dem deutschen Kreismaterial (≤ 7,5 h), was eher die Art der Warnung (nationale Vorwarnung gegen
   Kreiswarnung) als einen Unterschied der Dienste zeigt.
3. **Was das heißt.** Für das Vereinigte Königreich ist der Lebenslauf öffentlich, OGL-lizenziert und zum
   Teil maschinenlesbar: Hochstufung und Gebietsänderung schon aus der Tabelle, der Vorlauf erst aus dem
   PDF (Textschicht; die Standardbibliothek liest kein PDF, V0 bräuchte dafür eine Abhängigkeit oder
   liest nur die Tabelle). Das Jahr wird nachträglich und monatlich katalogisiert (Teil 1 §4): die
   Kontrolle läuft Wochen hinterher. **UK bleibt Kontrolle; jetzt eine, die zählbar ist** — und die
   einzige Quelle in diesem AUDIT, an der Hochstufungen überhaupt vorkamen.

## 3. Meteoalarm: Bedingungen nicht lesbar

`meteoalarm.org` ist eine Skriptanwendung (ohne Skript nur der Hinweis, sie brauche JavaScript;
`meteoalarm/home.excerpt.txt`), `robots.txt` dort 404. Weder die Feed-Startseite
(`meteoalarm/feeds-root.links.txt`) noch das API-Portal (`meteoalarm/api-root.excerpt.txt`) verlinken
Nutzungsbedingungen; beide nur CC BY 4.0. Die „additional requirements for redistributing" (Teil 1 §2)
bleiben **ungelesen**. Da Meteoalarm für Deutschland Zweithand ist und das Exposé es nur als
Querverweis führt, braucht V0 es nicht: **Meteoalarm bleibt aus V0 heraus**.

## 4. Empfehlung — AUDIT abgeschlossen

**V0 ist innerhalb der Charta möglich, schmal und täglich**, in der Form von Teil 1 §7, mit zwei
Änderungen aus heute: Filter `status` = `Actual`; das Met-Office-Archiv als jährlich bzw. monatlich
gelesene Kontrolle aus der Metadatentabelle (OGL, Quellenangabe), PDFs höchstens als Stichprobe.

Offen und **nicht Sache dieses Passes**: die Nutzungsbedingungen des DWD stehen nur auf `www.dwd.de`
hinter `Disallow: /` (Teil 1 §5) — ob abgeleitete Zeilen (Kennung, Typ, Verweise, Zeiten, Ereignis,
Stufe, Kreisnamen) committet und Rohdateien konserviert werden dürfen. Dazu und zum GO die Anfrage in
`REQUESTS.md` (2026-11-25). Bis zur Antwort: kein Code, keine weitere Lesung; die beiden Proben bleiben,
was sie sind.

Ein Wort zur Grenze des Befunds: zwei Novembernächte mit nur `Minor`-Meldungen. Ob die Frage des Exposés
— wie viel Vorwarnung tatsächlich gegeben wurde, und wie oft spät hochgestuft wird — am deutschen
Material Antworten trägt, zeigt erst ein Winter mit Unwettern. Das spricht für einen langen Lauf, nicht
gegen V0; ein E-Experiment, das Hochstufungen zählen soll, braucht eine Mindestzahl, die vorher
festgelegt wird.

## 5. Abrufe, offen gezählt

177 Abrufe: 162 an `opendata.dwd.de` (2 Listen, 158 Differenzen, 1 Vollstand, dazu der nicht
konservierte), 11 an die Met-Office-Hosts (`www.metoffice.gov.uk` 1, `digital.nmla.metoffice.gov.uk` 4,
`metoffice.access.preservica.com` 6), 4 an Meteoalarm (`meteoalarm.org` 2, `feeds.meteoalarm.org` 1,
`api.meteoalarm.org` 1). Alle 200 außer `meteoalarm.org/robots.txt` (404). **176 konserviert**
(Manifest; HTML-Seiten als Link- oder Textauszug, `derivation` je Zeile). **1 nicht konserviert**
(`not_kept`): eine Erreichbarkeitsprüfung der Differenzliste vor dem Skript (nur Status und Größe), die
Liste danach im Skript erneut geholt. Die Bibliotheksseite und die Feed-Startseite wurden nur geholt, um
Links zu finden; der Pfad durch das Archiv wurde Schritt für Schritt gewählt, nicht vorher festgelegt.
Kein Abruf von `www.dwd.de`. Nichts gesendet.

## Bewusst nicht heute

Kein Code, kein Workflow, keine Änderung an `verify.py` (es hält `leadtime/probes/` seit gestern). Keine
Familie außer `DISTRICT_*_DE`; keine Polygone; keine weiteren PDFs; die Tabellen anderer Jahre nicht
geladen; kein Versuch, Meteoalarm mit einem Skriptclient zu lesen.
