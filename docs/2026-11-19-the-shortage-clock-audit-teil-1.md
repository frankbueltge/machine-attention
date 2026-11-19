# The Shortage Clock — AUDIT, Teil 1

**Datum:** 2026-11-19 · **Stufe:** AUDIT (Teil 1 von 2) · **Exposé:**
`docs/2026-11-18-kandidat-the-shortage-clock.md` · **Proben:** `shortageclock/probes/2026-11-19/manifest.json`
(10 Abrufe, je ein Versuch, kein Wiederholen, 07:38–07:41 UTC).

**Anlass.** Alle früheren Kandidaten mit einem nächsten Schritt warten auf ein Tor des Maintainers:
The Interval (Review, `REQUESTS.md` 2026-11-16), Planetary Listening (Review, 2026-11-04), The
Provisional Air (GO, 2026-11-17). Damit ist heute die Nacht, die das Exposé (§ „Bewusst nicht
heute") für das AUDIT nennt.

**Was Teil 1 leistet und was nicht.** Teil 1 prüft jede im Exposé genannte Quelle einmal: Endpunkt,
Status, Größe eines vollständigen Abzugs, Lizenz, Charta, Probe mit Manifest. Die entscheidende Frage
des Exposés — **zeigt dasselbe Register an zwei Tagen verschiedene Uhren für denselben Eintrag?** —
braucht einen zweiten Abzug im Abstand von Tagen; das ist Teil 2. Was heute schon aus **einer**
Fassung zu sehen ist, steht in §3 und ist als Ein-Fassungs-Befund gekennzeichnet.

## 1. Was konserviert wurde, und wie

Konserviert werden **abgeleitete Kopien**, nicht die Rohantwort, wo die Rohantwort Firmennamen,
Telefonnummern oder Kontaktfelder trägt. Jede Manifestzeile hält `full_sha256` (die empfangenen Bytes)
und `sha256` (die gespeicherten) getrennt, dazu `derivation` mit der genauen Regel:

- **openFDA** (`openfda/drug-shortages-full.scrubbed.json`, `openfda/shortages-limit1.json`):
  Positivliste — Identitäts- und Uhrfelder wie empfangen (`generic_name`, `presentation`,
  `package_ndc`, `dosage_form`, `status`, `initial_posting_date`, `update_date`, `update_type`,
  `discontinued_date`, `change_date`, `therapeutic_category`, `shortage_reason`, `availability`);
  `company_name`, `related_info`, `resolved_note`, `related_info_link` nur als SHA-256;
  `contact_info` und der harmonisierte `openfda`-Block ungelesen entfernt. Grund, beim Prüfen der
  ersten Ableitung gefunden: `related_info` trägt Firmennamen und Service-Telefonnummern im Freitext,
  der `openfda`-Block Herstellernamen. Nach der Positivliste: 0 Telefonnummern-Muster, 0 `contact`.
- **BfArM** (`bfarm/lieferengpassmeldungen.csv`): `Telefon` und `E-Mail` ungelesen entfernt (I8);
  `Zulassungsinhaber`, `Anm. zum Grund`, `Alternativpräparat`, `Info an Fachkreise` nur als SHA-256;
  alle Datums-, Status- und Kennungsspalten wie empfangen.
- **EMA** (`ema/medicines-output-shortages-report_en.xlsx`): unverändert (keine Kontaktfelder;
  Arzneimittelnamen, keine Hersteller-Spalte).

**Offen gesagt:** Produktbezeichnungen (BfArM `Arzneimittlbezeichnung`, openFDA `presentation`)
enthalten mitunter einen Firmennamen als Teil des Produktnamens. Sie bleiben in der Probe, weil sie
die Identität des Eintrags sind; keine Ausgabe dieses Kandidaten wird je einen Hersteller nennen (E-2,
Exposé §7).

## 2. Je Quelle

| Quelle | Endpunkt | Status | Vollabzug | Lizenz | Bitte an Roboter | Charta |
|---|---|---|---|---|---|---|
| openFDA, Massendatei | `download.open.fda.gov/drug/shortages/drug-shortages-0001-of-0001.json.zip` (aus `api.fda.gov/download.json`, `export_date` 2026-11-18) | 200 | **447 839 B zip, 1 584 Einträge, ein Abruf** | CC0 (`openfda/license.html`, 200: „public domain … Creative Commons CC0"; `meta.license` → `open.fda.gov/license/`) | `api.fda.gov` keine `robots.txt` (Exposé §6) | **innerhalb** |
| openFDA, API | `api.fda.gov/drug/shortages.json?limit=1`, `?count=status`, `?count=update_type` | 200 ×3 | `meta.results.total` 1 584, `last_updated` 2026-11-18 | wie oben | — | **innerhalb** |
| FDA-Datenbank | `www.accessdata.fda.gov/scripts/drugshortages/default.cfm` und `…/drugshortages/` | **404 ×2** („FDA Apology", 420 B) | — | — | 30 s Abstand, 23:00–05:00 EDT — eingehalten (07:39 und 07:41 UTC = 02:39/02:41 EST) | nicht lesbar |
| BfArM | `anwendungen.pharmnet-bund.de/lieferengpassmeldungen/public/csv` | 200 | **341 585 B, 942 Meldungen, ein Abruf**, ohne Formular | **keine Lizenz angegeben**; die öffentliche Seite bietet den Link ausdrücklich an, „automatisiert über folgenden Link abzurufen" | `/lieferengpassmeldungen/` nicht gesperrt (Exposé §6) | **innerhalb** (öffentlich, ohne Login, ohne Kosten; Kontaktspalten ausgeschlossen); Lizenz offen |
| EMA | `www.ema.europa.eu/en/documents/report/medicines-output-shortages-report_en.xlsx` | 200 | 88 113 B, 85 Einträge; Datei sagt „automatically generated … on: 19/11/2026 - 06:00", `Last-Modified` 05:00:07 GMT | heute nicht geprüft (Teil 2) | Dokumentpfade nicht gesperrt | **innerhalb** |

**FDA-Datenbank.** Am 2026-11-18 antwortete `/scripts/drugshortages/` noch 200 (Exposé §3); heute
404 auf beiden Pfaden. Ob die Seite verlegt wurde oder diesen Abrufer abweist, sagt ein Abruf nicht;
kein weiterer Versuch. Für V0 ist sie entbehrlich: openFDA ist die maschinenlesbare Fassung desselben
Registers, und die Zweithand-Kontrolle des Exposés fällt vorerst aus.

## 3. Was eine einzige Fassung schon zeigt (Ein-Fassungs-Befunde)

**openFDA** (`openfda/drug-shortages-full.scrubbed.json`, `openfda/shortages-count-*.json`):

- Status: 1 116 `Current`, 409 `To Be Discontinued`, 59 `Resolved`. `update_type`: 827 `Reverified`,
  423 `New`, 334 `Revised`.
- **Behobene Einträge bleiben nur kurz.** Die 59 `Resolved` tragen `update_date` 2026-07-31 bis
  2026-11-04 — keiner älter als knapp vier Monate, während `initial_posting_date` bis 2012-01-01
  zurückreicht. Das passt zu einer Löschung behobener Einträge nach einer Frist (Exposé §1(c):
  sechs Monate, Nachbar-Angabe); bewiesen ist es erst, wenn ein Eintrag zwischen zwei Abzügen fällt.
- **Die Uhr wird angefasst, ohne dass sich etwas ändert.** 827 der 1 116 laufenden Einträge sind
  `Reverified`; ihr `update_date` liegt zwischen 2026-05-01 und 2026-11-17. `update_date` misst also
  Bestätigung, nicht Änderung — für V0 heißt das: ein Hash der Uhrfelder ohne `update_date` trennt
  echte Revisionen vom bloßen Nachstempeln.
- **`change_date`** existiert in 63 Einträgen (2023-04-28 bis 2026-11-04), in den gesehenen Fällen
  gleich `update_date` bei `Revised`/`Resolved`; das Feld fehlt in der Feldliste des Exposés.
- **Doppelte Identität in einer Fassung.** 17 Schlüssel (`generic_name`, `presentation`,
  `package_ndc`, Firmen-Hash) stehen je zweimal im Register (34 Einträge); bei 16 davon unterscheidet
  sich `initial_posting_date`, bei 11 der Status (typisch: ein `Current` seit Jahren neben einem
  `To Be Discontinued` jüngeren Datums). Das ist das Muster, das der nächste Nachbar (ASPE, Exposé §5)
  als 6,4 % „doppelte Engpässe" entfernte und auf umgeschriebene Erstmeldedaten zurückführte; in
  einer Fassung sind es zwei Einträge, nicht eine Revision. Ob daraus eine Revision wird, zeigt erst
  die Folge.

**BfArM** (`bfarm/lieferengpassmeldungen.csv`):

- 942 Meldungen: 259 `Erstmeldung`, 683 `Änderungsmeldung`. Die 683 Änderungsmeldungen verweisen
  über `Referenzierte Erstmeldung` auf 373 Bearbeitungsnummern — **keine davon steht in der Datei.**
  Das Register zeigt je Engpass nur die jüngste Meldung; die Erstmeldung, auf die sie sich beruft, ist
  für jeden Leser der Datei fort. Genau das, was das Exposé (§2) als „das Register überschreibt sich"
  vermutete, hier strukturell sichtbar.
- `Datum der Erstmeldung` ≠ `Beginn` in 782 Zeilen; in 671 liegt die Erstmeldung **nach** dem
  angegebenen Beginn — gemeldet wird oft rückwirkend. `Beginn` 2018-07-01 bis 2027-05-01, `Ende`
  2023-03-31 bis 2030-01-01; nur 21 Meldungen tragen ein `Ende` vor heute. Behobene Meldungen
  scheinen also zu fallen; wann, zeigt Teil 2.
- `Datum der letzten Meldung` reicht bis heute (2026-11-19): die Datei ist tagesaktuell.

**EMA** (`ema/medicines-output-shortages-report_en.xlsx`): 85 Einträge, 53 `Shortage resolved`,
27 `Shortage ongoing`, 5 `Medicine discontinued`. Behobene Einträge **bleiben** — `Last updated date`
der behobenen reicht bis 2014-05-07 zurück. `Start of shortage date` ist nur in 12 von 85 gefüllt.
Als Kontrolle brauchbar: ein Register, das nicht löscht, neben zwei, die es tun.

## 4. Gibt es schon ein öffentliches Tagesarchiv?

Eine Suche (2026-11-19) fand keines: weder ein öffentliches, versioniertes Archiv der openFDA-
Engpassdaten noch der BfArM-Datei. Gefunden wurden kommerzielle Abrufdienste, die tägliche Abzüge
gegen den Vortag vergleichen und gegen Bezahlung ausliefern — kein offenes Archiv, keine Auswertung
der Uhr. Die openFDA-Dokumentation nennt „Daily" als Aktualisierungstakt; dass der Endpunkt keine
Geschichte führt, bestätigt `update_date`/`update_type` als einzige Spur. Das Tageslicht des Exposés
steht damit unverändert.

## 5. Vorläufige Empfehlung

**Noch keine endgültige.** Teil 1 spricht für einen engen V0: beide Hauptquellen sind mit **je
einem Abruf pro Nacht** vollständig zu lesen (openFDA-Zip ≈ 0,45 MB, BfArM-CSV ≈ 0,34 MB), keyless,
ohne Formular, die US-Seite CC0; die EMA-Datei kommt als dritter Abruf dazu. Zwei offene Punkte
entscheiden Teil 2:

1. **Die Uhr an zwei Tagen** — ein zweiter Abzug aller drei Dateien frühestens 2026-11-21, Vergleich
   je Eintrag: `initial_posting_date`/`Beginn`/`Datum der Erstmeldung`, Status, `Ende`/
   `Expected resolution date`; gefallene und neue Einträge. Zeigt sich in Tagen keine einzige
   Uhr-Revision, ist das selbst ein Befund und spricht für einen wöchentlichen Takt wie bei
   The Provisional Air.
2. **BfArM-Lizenz** — keine angegeben. Die Daten werden zum automatisierten Abruf angeboten; ob
   abgeleitete Zeilen öffentlich committet werden dürfen, ist eine Frage, die Teil 2 in der
   Dokumentation des BfArM sucht und, falls dort nichts steht, dem Maintainer vorlegt (eine neue
   Quelle mit ungeklärter Lizenz ist seine Entscheidung, `discovery/PROMPT.md`).

## Bewusst nicht heute

Kein Code, kein `practice/src/practice/shortageclock/`, kein Workflow — V0 braucht das GO des
Maintainers, und Teil 2 steht aus. Kein weiterer Abruf der FDA-Datenbank nach den zwei 404. Keine
Formular-Postbacks an das BfArM-Register. Keine Detailseite eines EMA-Eintrags. Kein Hersteller in
diesem Dokument; Produktnamen nur in den Proben. Keine Anfrage in `REQUESTS.md` — das AUDIT braucht
kein Tor, und die Lizenzfrage wird erst nach Teil 2 gestellt, wenn sie dann noch offen ist.
