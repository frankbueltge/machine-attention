# The Lead Time — AUDIT, Teil 1

**Datum:** 2026-11-24 · **Stufe:** AUDIT (Teil 1 von 2) · **Exposé:**
`docs/2026-11-23-kandidat-the-lead-time.md` · **Proben:** `leadtime/probes/2026-11-24/manifest.json`
(144 konservierte Abrufe, je ein Versuch, kein Wiederholen, 07:38:24–07:40:59 UTC; dazu 5 nicht
konservierte, §6).

**Anlass.** Alle früheren Kandidaten mit einem nächsten Schritt warten auf ein Tor des Maintainers:
The Interval (Review, `REQUESTS.md` 2026-11-16), Planetary Listening (Review, 2026-11-04), The
Provisional Air (GO, 2026-11-17), The Shortage Clock (GO, 2026-11-21; Lizenz, 2026-11-20). Keine
dieser Anfragen ist beantwortet. Damit ist heute die Nacht, die das Exposé (§ „Bewusst nicht heute")
für das AUDIT nennt.

**Was Teil 1 leistet und was nicht.** Teil 1 beantwortet die entscheidende Frage des Exposés (§8):
**trägt die CAP-Kette des DWD den Lebenslauf einer Warnung aus zwei Ständen im Abstand einiger
Stunden ohne Lücke, und genügt `_DIFF`?** Dazu je Quelle Endpunkt, Status, Größe, Takt, Lizenz,
Charta. Offen für Teil 2: ob eine Lesung je Tag über **zwei** Tage lückenlos anschließt, das
Digitalarchiv des Met Office selbst, und Meteoalarms Weitergabebedingungen.

## 1. Was konserviert wurde, und wie

Unter `leadtime/probes/2026-11-24/`:

- **`dwd/`** — die Verzeichnisliste `…/alerts/cap/`, die Listen `DISTRICT_DWD_STAT/` und
  `DISTRICT_DWD_DIFF/` (Stand 07:38 UTC), `README.txt` und `LIESMICH.txt` des Servers, die Wurzel-
  und `weather/`-Liste; **zwei Vollstände** `stat/` (Kreisebene, deutsch): **A** =
  `…20261124003727…DISTRICT_DE.zip` (650 247 B), **B** = `…20261124073639…DISTRICT_DE.zip`
  (673 484 B) — 7 h 0 min auseinander; und **alle 131 deutschen Differenzdateien** `diff/` von
  2026-11-23 11:30:59 bis 2026-11-24 07:36:39 UTC lückenlos laut Liste (1 079 868 B, 103 davon leer
  mit 22 B). Alle unverändert: die CAP-Dateien nennen keine Personen; `sender` ist die
  Funktionsadresse des Dienstes, `senderName`/`contact` sein Name (I8 unberührt).
- **`meteoalarm/`** — der Feed Luxemburg (`feed-luxembourg.xml`, 989 B, unverändert) und ein
  Textauszug der Feed-Startseite (Lizenzzeile; Markup, Skripte, Sitzungstoken und Kontaktadresse
  entfernt, `derivation` im Manifest).
- **`metoffice/`** — `robots.txt` und ein Textauszug der Archivseite des NSWWS (Navigation entfernt,
  Kontaktadresse durch Platzhalter ersetzt).

Jede Manifestzeile hält `full_sha256` (empfangene Bytes) und `sha256` (gespeicherte) getrennt;
`verify.py` hält `leadtime/probes/` ab heute wie die Proben der anderen Kandidaten
(`check_snapshots`, beide Richtungen).

## 2. Je Quelle

| Quelle | Endpunkt | Status | Größe / Takt | Lizenz | Bitte an Roboter | Charta |
|---|---|---|---|---|---|---|
| DWD, Kreisebene, Vollstand | `opendata.dwd.de/weather/alerts/cap/DISTRICT_DWD_STAT/` | 200 | 335 deutsche Stände in der Liste (ältester 2026-11-22 07:43:13 UTC → ≈ 48 h), Abstand Median 10,25 min, max. 11,1 min; ≈ 650–675 KB je Stand, 195,5 MB je Fenster | Server: „free of charge", „without registration", Nutzungsbedingungen **nur auf `www.dwd.de`** (`README.txt`, `LIESMICH.txt`); in jeder Warnung `eventCode LICENSE` „© GeoBasis-DE / BKG 2021 (Daten modifiziert)" (Geometrie) | `opendata.dwd.de` keine `robots.txt` (Exposé §6); `www.dwd.de` `Disallow: /` | **innerhalb** (öffentlich, ohne Login, ohne Kosten, keine Personendaten); Nutzungsbedingungen ungelesen (§5) |
| DWD, Kreisebene, Differenz | `…/DISTRICT_DWD_DIFF/` | 200 | 335 deutsche Dateien in ≈ 48 h, **2,67 MB je Fenster**; leere Differenz 22 B | wie oben | wie oben | **innerhalb** |
| DWD, weitere Familien | `COMMUNEUNION_{CELLS,DWD}_{STAT,DIFF}`, `DISTRICT_EVENT_*` (13 Einträge in `cap-index.html`) | 200 | nicht geladen | wie oben | wie oben | — |
| Meteoalarm | `feeds.meteoalarm.org/feeds/meteoalarm-legacy-atom-luxembourg` | 200 | 989 B, **0 Einträge** um 07:40 UTC | Feed-`rights`: „terms equivalent to CC BY 4.0, with additional requirements for redistributing outlined in our Terms and Conditions"; Startseite: „MeteoAlarm License (CC BY 4.0)" | keine Sperre (Exposé §6) | **innerhalb**; Weitergabebedingungen ungelesen (Teil 2) |
| Met Office, NSWWS-Archiv | `www.metoffice.gov.uk/research/library-and-archive/publications/national-severe-weather-warning-service` | 200 | Erläuterungsseite | Archiv selbst nicht geprüft | `robots.txt` sperrt `/public/data/`, `/lib/` u. a., nicht `/research/` | Seite **innerhalb**; Archiv: Teil 2 |

## 3. Die entscheidende Frage: trägt die Kette den Lebenslauf?

Gelesen mit der Standardbibliothek (`zipfile`, `xml.etree`), Felder `identifier`, `msgType`,
`references`, `sent`, `event`, `severity`, `onset`, `expires`, `areaDesc`. Ergebnis aus den
konservierten Dateien:

1. **Differenzen rekonstruieren den Vollstand exakt.** A (30 Meldungen: 22 `Alert`, 8 `Update`)
   plus die 120 Differenzen nach A, angewandt mit einer Regel — Meldung hinzufügen, jede in
   `references` genannte Vorgängerin entfernen, jede Meldung mit `expires` ≤ Dateizeit entfernen —
   ergibt **genau die 40 Kennungen von B** (31 `Alert`, 9 `Update`): 0 fehlend, 0 zu viel.
2. **Jede Meldung aus A und B steht in einer Differenz.** Über alle 131 Differenzen 62 verschiedene
   Meldungen (39 `Alert`, 23 `Update`); die Vereinigung mit A und B bleibt 62.
3. **Keine Kette bricht.** Allein aus A und B sind von B's 9 Verweisen nur 3 auflösbar: 6 `Update`s
   verweisen auf Vorgängerinnen, die vor A schon ersetzt waren und deshalb in **keinem** Vollstand
   mehr stehen. Mit den Differenzen ab 2026-11-23 11:30 UTC (aus dem 48-Stunden-Fenster
   nachgeladen) sind **alle** Verweise von B aufgelöst; Kettenlängen 1 (31×), 2 (5×), 3 (3×), 4 (1×).
   Fünf Verweise der frühesten Differenzen zeigen vor 11:30 UTC und wurden nicht verfolgt.
4. **Der Lebenslauf ist ein Baum, keine Kette.** 9 Meldungen haben mehr als eine Nachfolgerin
   (bis zu 3); 17 von 18 sichtbaren Übergängen **verkleinern das Gebiet** (eine `Alert` mit 97
   Kreisen zerfällt in `Update`s mit 41, 45, 11 Kreisen). Keine Zusammenführung (0 Meldungen mit
   mehr als einem Verweis).
5. **Aufhebung ist ein `Update`, kein `Cancel`.** 0 Meldungen mit `msgType` `Cancel`; **7 `Update`s
   setzen `expires` = `sent`** — die Warnung endet vorzeitig (Beispiel: Glätte, Vorgängerin bis
   10:00 MEZ, beendet 07:48 MEZ). Diese Meldung verschwindet **sofort** aus dem Vollstand: B kennt
   sie nicht, nur die Differenz `…20261124064759…` hält sie. **Ein Leser nur der Vollstände sähe
   vorzeitige Enden nie.**
6. **Vorlauf, eine Nacht, nur als Form.** Für die 39 Wurzel-`Alert`s liegt `onset` − `sent` zwischen
   0 und 7,5 h; 15 haben `onset` = `sent`. Alle 62 Meldungen sind `severity` `Minor` (Frost, Glätte,
   Nebel, leichter Schneefall, Böen) — **eine Hochstufung kam in diesem Ausschnitt nicht vor**, die
   Messgröße (b) ist heute nicht prüfbar. Kein Wert, keine Verteilung.

**Antwort auf §8 des Exposés:** Ja — mit `_DIFF`, nicht mit `_STAT`. Und anders als das Exposé
fürchtete, braucht V0 **keinen Takt unter einem Tag**: jede Differenz bleibt ≈ 48 h in der Liste,
also holt eine Lesung je Tag alle Differenzen seit der letzten (≈ 170 Abrufe, ≈ 1,3 MB je Tag),
mit einem Tag Reserve für eine ausgefallene Lesung. Das ist aus **einer** Liste geschlossen; Teil 2
prüft es an einer zweiten Lesung (§7).

## 4. Die Nachbarschaft, geprüft

- **Met Office.** Die Archivseite sagt: Warnungen seit März 2011, **jede Aktualisierung als eigene
  Datei mit demselben Kenncode** und eigener Ausgabezeit im Namen (Beispiel der Seite:
  `NSWWS_cb7ef0b6-…_20250101_1112_Y_Sn`, dann `…_20250102_1106_Y_SnIc`, `…_20250105_0351_Y_SnIc`),
  als **PDF**, das laufende Jahr monatlich nachkatalogisiert. Für das Vereinigte Königreich hält also
  ein öffentlicher Ort den Lebenslauf schon — in Bildform, nicht maschinenlesbar, mit Wochen
  Verzögerung. Wie das Exposé vorsah: **UK wird Kontrolle, nicht Lücke.** Ob die PDFs Stufe, Fenster
  und Gebiet lesbar tragen, ist Teil 2.
- **Meteoalarm.** Der Luxemburg-Feed war um 07:40 UTC leer: er zeigt den aktuellen Stand, keine
  abgelaufenen Warnungen (ein Feed, ein Zeitpunkt — Hinweis, kein Beweis). Eine Geschichte hält er
  nicht sichtbar; für Deutschland ist er gegenüber dem DWD ohnehin Zweithand.
- **Ein öffentliches Kettenarchiv der DWD-Warnungen** wurde nicht gefunden; das Exposé (§5) nannte
  nur Werkzeuge, die innerhalb des 48-Stunden-Fensters lesen. Das Tageslicht steht.

## 5. Lizenz — die offene Frage

`README.txt` des Servers verweist auf `www.dwd.de/EN/service/legal_notice/legal_notice_node.html`,
`LIESMICH.txt` auf `www.dwd.de/copyright`. Dieser Host bittet alle Roboter mit `Disallow: /`
(Exposé §6); das AUDIT liest ihn **nicht**, wie bei OSCAR und den E-utilities, und legt die Frage
dem Maintainer vor. Was ungelesen bleibt: ob die Nutzungsbedingungen das Committen abgeleiteter
Zeilen und das Konservieren der Rohdateien mit Quellenangabe erlauben. Die Geometrie trägt in jeder
Datei den BKG-Vermerk; V0 würde Polygone nicht committen, nur Kreisnamen. Der Server speichert nach
eigener Angabe die IP-Adresse des Abrufers bis zu 7 Tage — eine Angabe über diesen Abrufer, keine
Personendaten Dritter.

## 6. Abrufe, offen gezählt

149 Abrufe an `opendata.dwd.de`, `feeds.meteoalarm.org`, `www.metoffice.gov.uk`, alle 200, keiner
wiederholt. **144 konserviert** (Manifest). **5 nicht konserviert** (`not_kept` im Manifest): vor dem
Probenskript las ein erkundender Aufruf `…/cap/`, `COMMUNEUNION_DWD_STAT/`, `COMMUNEUNION_DWD_DIFF/`,
`DISTRICT_DWD_STAT/`, `DISTRICT_DWD_DIFF/` (nur Dateinamen, Größen, Zeiten), um den Ausschnitt zu
wählen; `…/cap/` und die beiden `DISTRICT_*`-Listen wurden im Skript erneut geholt und konserviert.
Die Differenzen vor A (86 Dateien) wurden in einem zweiten Lauf nachgeladen, nachdem die erste
Auswertung sechs unaufgelöste Verweise fand — offen gesagt: der Ausschnitt wuchs nach dem ersten
Blick. Kein Abruf von `www.dwd.de`. Nichts gesendet.

## 7. Empfehlung

**V0 ist innerhalb der Charta möglich und schmal**, sobald zwei Dinge geklärt sind:

1. **Teil 2 (ohne Tor):** eine zweite Lesung, frühestens 2026-11-25, die alle deutschen
   Kreis-Differenzen seit `…20261124073639…` holt und zeigt, dass sie lückenlos an diese Probe
   anschließen (Zeitstempel der Liste, Kette, Rekonstruktion eines dann aktuellen Vollstands) — der
   Beweis für den Tagestakt. Dazu je ein Ordner des Met-Office-Digitalarchivs (Lesbarkeit der PDFs)
   und Meteoalarms Weitergabebedingungen, soweit ohne Sperre lesbar.
2. **Die Lizenzfrage (Maintainer):** die Nutzungsbedingungen stehen nur hinter einer
   Roboter-Sperre; sie zu lesen oder zu entscheiden, ist nicht Sache dieses Passes.

**Form, wenn das GO kommt:** täglich einmal (nicht mehrmals) alle `DISTRICT_DWD_DIFF/…_DE.zip` seit
der letzten Lesung; jede Datei gehasht; committet werden abgeleitete Zeilen je Meldung
(`identifier`, `msgType`, `references`, `sent`, `event`, `severity`, `onset`, `expires`, Kreisnamen
— keine Polygone, kein Freitext, kein `sender`/`contact`); `verify.py` rekonstruiert je Lesung den
letzten Vollstand aus den Differenzen und vergleicht ihn mit einem einmal täglich mitgeholten
`_STAT`. Gemessen: Vorlauf der Wurzel, Hochstufungen entlang des Baums, Gebietsverkleinerungen,
vorzeitige Enden — als Verteilung, nie als Urteil über eine Warnung (E-2).

Das GO für V0 ist laut Aufnahme-Pfad das des Maintainers; es wird erst nach Teil 2 angefragt, damit
die Anfrage den Tagestakt bewiesen enthält.

## Bewusst nicht heute

Kein Code, kein Workflow, keine Lesung im Sinn eines Instruments; kein `www.dwd.de`; keine
Polygone ausgewertet; die Familien `COMMUNEUNION_*` und `DISTRICT_EVENT_*` nicht geladen; der
deutsche Meteoalarm-Feed (8,9 MB) nicht erneut geholt. Keine Anfrage in `REQUESTS.md` — die
Lizenzfrage geht zusammen mit der GO-Anfrage nach Teil 2 hinein.
