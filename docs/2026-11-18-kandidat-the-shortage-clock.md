# The Shortage Clock — Exposé

**Datum:** 2026-11-18 · **Stufe:** EXPOSÉ · **Anlass:** Alle Kandidaten mit einem nächsten Schritt
warten auf ein Tor des Maintainers. The Interval: Review angefragt (`REQUESTS.md` 2026-11-16).
Planetary Listening: Review angefragt (`REQUESTS.md` 2026-11-04). The Provisional Air: GO angefragt
(`REQUESTS.md` 2026-11-17). The Synthetic Flood: wartet auf ihren Workflow am 2026-12-04
(`docs/2026-11-09-synthetic-flood-v0-inkrement-4.md`). The Declared Network und The Afterlife:
`REQUESTS.md` 2026-10-23 und 2026-10-30. Laut `discovery/PROMPT.md` Schritt 2 darf dann ein neues
Exposé pro Woche entstehen; das letzte war The Provisional Air am 2026-11-11 (ISO-Woche 46,
`docs/2026-11-11-kandidat-the-provisional-air.md`). Dies ist das Exposé der ISO-Woche 47.

Jede Aussage über Formate, Lizenzen, Raten und das Überschreibverhalten der Quellen ist
**ungeprüft** und gehört dem AUDIT. Geprüft ist heute nur, was §5 und §6 nennen: je Adresse ein
Status-Abruf und die `robots.txt` jedes Hosts, den V0 lesen würde (2026-11-18, 07:5x UTC), sowie
— für §3 — die **Feldnamen** einer openFDA-Antwort mit `limit=1`. Keine Werte übernommen, keine
Bytes konserviert, keine Zahl aus einer Antwort in diesem Dokument.

## 1. Die Frage

> Hält ein öffentliches Arzneimittel-Lieferengpassregister seine eigene Uhr — und wie lange dauert
> ein Engpass, gemessen am Tag, gegen das, was das Register am Ende über ihn sagt?

Behörden führen öffentliche Register der Lieferengpässe: die US-Arzneimittelbehörde (FDA) ihre
Drug-Shortages-Datenbank, in Deutschland das Bundesinstitut für Arzneimittel und Medizinprodukte
(BfArM) seine Lieferengpassmeldungen, auf EU-Ebene die Europäische Arzneimittel-Agentur (EMA) einen
Katalog. Jeder Eintrag trägt eine Uhr: erstmals gemeldet, Status (aktuell / behoben / eingestellt),
zuletzt aktualisiert, erwartetes Ende. Dauer-Statistiken über Engpässe werden aus diesen Feldern
gerechnet — aus der **letzten** Fassung eines Eintrags.

Die Operation des Gründungskorpus (`docs/2026-08-08-projekt-aufnahme.md`), diesmal **das Register
gegen sich selbst**: Was der Eintrag an einem Tag über seinen eigenen Beginn, seinen Status und sein
Ende sagte, neben dem, was er später darüber sagt. Messgrößen:
(a) **Uhr-Revisionen** — ein `initial_posting_date` (bzw. Meldebeginn), das sich nachträglich
verschiebt; ein Status, der von „behoben" zurück auf „aktuell" springt; ein erwartetes Ende, das
weiterwandert; (b) **beobachtete Dauer** — vom ersten Tag, an dem der Eintrag als aktuell stand, bis
zum ersten Tag, an dem er als behoben stand — gegen die Dauer aus der letzten Fassung;
(c) **Verschwinden** — Einträge, die das Register nach der Behebung löscht (bei der FDA nach sechs
Monaten, laut dem Nachbarn in §5, ungeprüft), sodass ein späterer Leser ihre Geschichte nicht mehr sieht.

## 2. Warum nur anhaltende maschinelle Aufmerksamkeit das beantworten kann

- **Das Register überschreibt sich.** Jede Fassung ersetzt die vorige; openFDA gibt nach Kenntnis
  der Feldnamen nur `update_date` und `update_type` der letzten Änderung heraus, keine Geschichte
  (Feldliste §3; dass keine Historie existiert, prüft das AUDIT).
- **Der nächste Nachbar musste raten, wo Tagesbeobachtung gemessen hätte.** Die Analyse für das
  US-Gesundheitsministerium (ASPE, §5) rekonstruierte Statusverläufe 2018–2023 aus **39**
  Webarchiv-Fassungen der FDA-Exceldatei (2019-12-29 bis 2023-12-21) — im Mittel eine Fassung alle
  gut fünf Wochen. Sie berichtet, dass in 6,4 % der Fälle ein zweiter Engpass für ein Produkt
  erschien, das schon in einem laufenden stand, „möglicherweise wegen leichter Abweichungen im
  angegebenen Erstmeldedatum, als Meldungen aktualisiert wurden" — und entfernte diese Fälle. Ob
  das Register sein Erstmeldedatum umschreibt, ist dort eine Vermutung; eine tägliche, gehashte
  Lesung macht es zu einer Zählung.
- **Gelöschtes verschwindet.** Was nach der Behebung aus dem Register fällt, ist für jeden späteren
  Leser fort; nur wer an jedem Tag las, hat es.
- **Wiederholbarkeit.** Jede Fassung mit dem SHA-256 der empfangenen Antwort, wie `verify.py` es
  für The Interval hält.

## 3. Datenlage-Kurzcheck (ungeprüft, für das AUDIT)

| Seite | Kandidat-Quelle | Was das AUDIT klären muss |
|---|---|---|
| USA, maschinenlesbar | openFDA `api.fda.gov/drug/shortages.json` (200, keyless; `meta`: `disclaimer`, `terms`, `license`, `last_updated`, `results`; Ergebnisfelder: `company_name`, `contact_info`, `discontinued_date`, `dosage_form`, `generic_name`, `initial_posting_date`, `openfda`, `package_ndc`, `presentation`, `related_info`, `status`, `therapeutic_category`, `update_date`, `update_type`) | Takt von `last_updated`; ob ein ganzer Abzug ohne Schlüssel in die Rate passt; Lizenz aus `meta.license`; ob behobene Einträge im Endpunkt bleiben oder fallen. **`contact_info` wird nie gelesen oder gespeichert** (kann Personen nennen, I8). |
| USA, Quelle des Betreibers | FDA Drug Shortages Database, `www.accessdata.fda.gov/scripts/drugshortages/` (200) | Ob die Seite dieselbe Uhr zeigt wie openFDA (Kontrolle, zweite Hand); ob die Exceldatei, die der Nachbar las, noch erscheint. |
| Deutschland | BfArM Lieferengpassmeldungen, `anwendungen.pharmnet-bund.de/lieferengpassmeldungen/faces/public/meldungen.xhtml` (200) | Ob ein Export ohne Formular-Postback erreichbar ist; Felder (Meldedatum, Beginn, voraussichtliches Ende, Status); Lizenz; ob behobene Meldungen stehen bleiben. Hier fallen nach öffentlicher Darstellung weit mehr Meldungen an als bei der FDA — der Kandidat braucht diese zweite Seite, sonst misst er zu wenig (§7). |
| EU | EMA-Katalog, `www.ema.europa.eu/en/documents/report/medicines-output-shortages-report_en.xlsx` (200, xlsx); die gleichnamige `.json` antwortet 404 | Takt der Datei; ob sie Fassungen datiert; Lizenz. Kontrolle, nicht Hauptquelle: zentral zugelassene Arzneimittel, wenige Einträge (ungeprüft). |

**Rückwirkend:** nur in Archivfassungen Dritter, und so grob, wie §2 zeigt. Das Tageslicht beginnt
mit der ersten Lesung.

## 4. V0-Skizze (nur Form, keine Festlegung)

Einheit: **Eintrag × Tag** (FDA: Wirkstoff × Darreichung bzw. Paket-NDC; BfArM: Meldung). Jede Nacht
der ganze öffentliche Stand beider Register, gehasht; committet werden abgeleitete Zeilen, nicht die
Rohantwort, sofern sie zu groß ist. Ereignisse: `first_seen`, `status_changed` (mit Richtung;
`reopened` für behoben → aktuell), `clock_revised` (ein Datumsfeld über den Beginn ändert sich),
`end_moved` (erwartetes Ende verschoben), `vanished`. Berichtet als Verteilung je Register und
Monat, nie je Hersteller. Die Klasse ist vermutlich **Instrument**; ein E-Experiment von 14 Nächten
kann nur Lesbarkeit und Ereignisrate prüfen, keine Dauern.

Substrat: Lesen und Sichern wie The Interval (`practice/src/practice/interval/`), der xlsx-Leser
aus `practice/src/practice/interval/drivers.py` (stdlib) für die EMA-Datei.

## 5. Die nächsten Nachbarn, und das Tageslicht

| Nachbar | Was er tut | Tageslicht | Erreichbar 2026-11-18 |
|---|---|---|---|
| [ASPE, „Analysis of Drug Shortages, 2018–2023"](https://aspe.hhs.gov/reports/drug-shortages-2018-2023) ([Bookshelf](https://www.ncbi.nlm.nih.gov/books/NBK611681)) | Rekonstruiert Statusverläufe und Dauern je 9-stelligem NDC aus 39 Webarchiv-Fassungen der FDA-Datei. | **Der nächste Nachbar, und er nimmt die Dauer-Frage zum Teil.** Er misst rückwirkend, grob (≈ fünf Wochen Abstand) und muss Uhr-Revisionen als Rauschen entfernen. Das Tageslicht ist genau dieses Rauschen: wie oft das Register seine Uhr umschreibt, und was das mit der Dauer macht. Ein Bericht, kein laufendes Register. | Suchauszug 2026-11-18; Seiten nicht abgerufen |
| [„Comparative Analysis of Drug Shortages in the US and Germany (2016–2023)"](https://doi.org/10.1017/jme.2024.105) | Vergleicht Wirkstoffe, Dauern und Zyklen aus ASHP- und BfArM-Daten. | Liest die letzte Fassung beider Seiten; keine Revisionen, kein Tag. Nimmt den Ländervergleich, den V0 deshalb nicht als Frage führt. | Suchauszug; nicht abgerufen |
| [„National and transnational drug shortages … Europe and the USA" (BMC 2022)](https://doi.org/10.1186/s12913-022-08309-3) | Vergleicht neun Monate öffentlicher Register in fünf Ländern. | Querschnitt, nicht Verlauf. | Suchauszug; nicht abgerufen |
| [ASHP-Engpassstatistik](https://www.ashp.org/drug-shortages/shortage-resources/drug-shortages-statistics) | Quartalszählungen aktiver und neuer Engpässe aus der eigenen, nicht offen lizenzierten Liste. | Eigene Liste, Quartalsauflösung; keine Uhr des Behördenregisters. | 403 (`robots.txt` 200) |
| [FDA, Drug Shortages Report to Congress CY 2025](https://www.fda.gov/media/193637/download?attachment) | Jahreszählungen aus der internen Datenbank. | Die eigene Jahresbilanz des Registers; zeigt nicht, wie oft es sich umschrieb. | Suchauszug; nicht abgerufen |
| [OECD, Analyse nationaler Engpass-Monitoringsysteme (2022)](https://www.oecd.org/content/dam/oecd/en/topics/policy-issues/pharmaceuticals-and-medical-technologies/suppl-mat-1-oecd-analysis-of-national-shortage-monitoring-systems-2022.pdf) | Inventar der Register, Aktualisierungstakt, Löschregeln. | Beschreibt die Uhren, liest sie nicht. Nützlich für das AUDIT (Löschfristen). | Suchauszug; nicht abgerufen |

Ob jemand das openFDA-Register bereits täglich archiviert und die Fassungen veröffentlicht, ist
heute nicht geprüft und die erste Frage des AUDIT an die Nachbarschaft; findet sich ein solches
Archiv, schrumpft das Tageslicht auf seine Auswertung.

## 6. Vorprüfung der Roboter-Regeln (je Host ein Abruf)

| Host | `robots.txt` | Bedeutung für V0 |
|---|---|---|
| `api.fda.gov` | 404, keine Datei | Keine Bitte an Roboter. Die Hauptquelle der US-Seite steht offen, soweit ein Abruf das sagen kann. |
| `open.fda.gov` | 403 (Dokumentationsseite selbst 200) | Dokumentation, nicht Datenquelle; das AUDIT liest sie einmal. |
| `www.accessdata.fda.gov` | 200; `/scripts/drugshortages/` nicht gesperrt; für alle Crawler „Hit-rate: 30", „Visiting-hours: 23:00EDT-05:00EDT" | Nicht-Standard-Felder, aber eine Bitte. Liest V0 diesen Host, dann höchstens einmal je Nacht, innerhalb dieser Stunden, 30 s Abstand. Das AUDIT hält das schriftlich fest. |
| `anwendungen.pharmnet-bund.de` | 200; `/lieferengpassmeldungen/` nicht gesperrt (gesperrt u. a. `/amgui/`, `/register/`, `/websearch/`) | Die deutsche Seite steht offen. |
| `www.ema.europa.eu` | 200; Dokumentpfade nicht gesperrt, `Allow: /*/documents/report/*.json$` | Die EU-Kontrolle steht offen. |
| `www.bfarm.de` | 404 (Fehlerseite) | Nur Erläuterungsseiten; V0 braucht den Host nicht. |

Damit fällt auch dieser Kandidat nicht an der Tür von OSCAR und E-utilities. Lizenz und Rate sind
damit nicht bewiesen.

## 7. Grenzen, ehrlich

- **Keine Anschuldigung (E-2).** Ein Engpass ist kein Vergehen, eine Datumskorrektur kein Fehler.
  Gemessen wird das Register, nicht die Hersteller: kein Hersteller wird als Einzelner ausgewiesen,
  `company_name` geht nur in einen Hash zur Identität des Eintrags ein, nie in eine Ausgabe.
- **Keine Personen (I8).** `contact_info` und jedes Kontaktfeld der deutschen Meldungen werden nicht
  gelesen. Keine Patientendaten existieren in diesen Quellen.
- **Wenige Ereignisse auf der US-Seite.** Der Bericht an den Kongress zählt für 2025 nur sehr wenige
  neue Engpässe (§5, Auszug). Statusübergänge laufender Einträge und Uhr-Revisionen sind die
  Ereignisse, nicht neue Engpässe; ob sie häufig genug sind, sagt erst eine Folge von Lesungen.
  Darum braucht der Kandidat die deutsche Seite.
- **Nähe zu The Interval und The Provisional Air.** Dieselbe Bauform (frühe Darstellung gegen
  spätere); hier liegt beides im selben Register. Das AUDIT sagt, wie viel Code geteilt wird.
- **Wenn ein öffentliches Tagesarchiv existiert,** endet der Kandidat womöglich im AUDIT; das ist ein
  gültiges Ende.

## 8. Was das AUDIT prüfen muss

Für openFDA, die FDA-Datenbank, das BfArM-Register und die EMA-Datei je: exakter Endpunkt,
HTTP-Status, Größe eines vollständigen Abzugs, Rate ohne Schlüssel, Lizenz, Bitten an
automatisierte Abrufer, ob innerhalb der Delegations-Charta (öffentlich, ohne Login, ohne Kosten,
ohne personenbezogene Daten — Kontaktfelder ausgeschlossen), und eine Probe mit Manifest unter
`shortageclock/probes/<date>/`. Zuerst und entscheidend: **ob dasselbe Register an zwei Tagen
verschiedene Uhren für denselben Eintrag zeigt** (zwei Abrufe im Abstand von Tagen, Vergleich der
Datumsfelder) und ob behobene Einträge stehen bleiben. Dazu: ob ein öffentliches Tagesarchiv schon
existiert. Am Ende steht eine Empfehlung. Das GO für V0 ist laut Aufnahme-Pfad das des Maintainers;
das AUDIT braucht es nicht.

## Bewusst nicht heute

Keine Einträge gelesen, keine Werte übernommen (nur Feldnamen einer Antwort mit `limit=1`), keine
Bytes konserviert, kein Code, kein Verzeichnis `shortageclock/`. Kein Formular-Postback an das
BfArM-Register, kein Abruf der Exceldatei über ihren Status hinaus. Der Fokus ist unberührt. Das
AUDIT kommt erst, wenn kein früherer Kandidat einen fälligen Schritt hat; vor ihm steht in der
Reihe The Provisional Air, falls ihr GO kommt.
