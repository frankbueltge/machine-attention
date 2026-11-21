# The Shortage Clock — AUDIT, Teil 2, Punkt 1: die Uhr an zwei Tagen

**Datum:** 2026-11-21 · **Stufe:** AUDIT (Teil 2, Punkt 1 von 2 — damit ist das AUDIT abgeschlossen) ·
**Teil 1:** `docs/2026-11-19-the-shortage-clock-audit-teil-1.md` · **Punkt 2 (Lizenz):**
`docs/2026-11-20-the-shortage-clock-audit-teil-2-lizenz.md` · **Proben:**
`shortageclock/probes/2026-11-21/manifest.json` (4 Abrufe, 07:39–07:40 UTC) · **Vergleich:**
`shortageclock/comparisons/2026-11-19_2026-11-21.json`.

**Anlass.** Teil 1 (§5, Punkt 1) setzte einen zweiten Abzug aller drei Dateien frühestens auf
2026-11-21. Alle früheren Kandidaten mit einem nächsten Schritt warten weiter auf ein Tor des
Maintainers (`REQUESTS.md` 2026-11-04, 2026-11-16, 2026-11-17, 2026-11-20).

**Offen gesagt — drei Läufe statt einem.** Das Abrufskript lief dreimal. Lauf 1 (07:3x UTC) und
Lauf 2 (07:39:26 UTC) brachen jeweils nach drei Abrufen ab (openFDA-Index, openFDA-Zip, BfArM-CSV),
weil die BfArM-Antwort sich nicht als UTF-8 dekodieren ließ und das Skript dafür keinen Rückfall
hatte; beim zweiten Mal griff eine Korrektur nicht, die ich für angewandt hielt. Aus beiden Läufen
ist nichts aufbewahrt (das Verzeichnis wurde vor Lauf 3 gelöscht). Lauf 3 (ab 07:39:53 UTC) ist der
konservierte. Insgesamt also **10 Abrufe, davon je 3 an openFDA-Index, openFDA-Zip und BfArM, 1 an
EMA**, statt 4. Kein Abruf wurde wegen einer Fehlantwort der Quelle wiederholt; alle Antworten waren
200. **Befund dabei:** die BfArM-Datei kommt heute als Windows-1252, nicht als UTF-8 (`encoding` in
`bfarm/lieferengpassmeldungen.status.json`); Teil 1 vermerkt „decoded utf-8". Ob die Quelle die
Kodierung gewechselt hat oder Teil 1 ungenau vermerkt ist, lässt sich nicht prüfen — die Rohbytes
von 2026-11-19 sind nicht aufbewahrt, nur ihr Hash. Für V0 heißt das: Kodierung erkennen, nicht
annehmen.

## 1. Was konserviert wurde, und wie

- **openFDA:** Index-Auszug (`export_date` jetzt 2026-11-20) und die Massendatei, abgeleitet nach
  **derselben Positivliste wie am 2026-11-19** (Manifest `derivation`, wortgleich). Die Firmen-Hashes
  sind zwischen den Tagen vergleichbar: 1 556 Identitätsschlüssel stimmen überein.
- **BfArM:** wegen `REQUESTS.md` (2026-11-20, offen) **keine Zeile, keine Bearbeitungsnummer, kein
  Produktname** — konserviert sind nur Status, Kodierung, Zeilenzahl und `full_sha256` der Antwort.
  Der Vergleich wurde im Speicher gegen die abgeleitete CSV vom 2026-11-19 gerechnet und ist nur als
  Zählung festgehalten. Die Rohbytes lagen während des Laufs in einem flüchtigen Arbeitsverzeichnis
  außerhalb des Repositoriums; `Telefon` und `E-Mail` wurden vor dem Zählen ungelesen entfernt.
- **EMA:** die Datei unverändert (Erlaubnis zur Weiterverwendung mit Quellenangabe, Punkt 2):
  „Output automatically generated from content on www.ema.europa.eu" — European Medicines Agency.

## 2. Befunde, je Quelle (zwei Fassungen, zwei Tage)

### openFDA (Export 2026-11-18 gegen 2026-11-20)

- 1 584 → 1 581 Einträge. Gepaart über `generic_name`, `package_ndc`, Firmen-Hash: **1 576 gepaart,
  8 gefallen, 5 neu.**
- **Keine Uhr wurde umgeschrieben:** in keinem gepaarten Eintrag änderte sich `initial_posting_date`,
  `status`, `discontinued_date` oder `change_date`; kein gefallener Eintrag kehrte unter neuem
  Erstmeldedatum zurück (`vanished_and_new_share_key: 0`).
- **Nachstempeln ist der Normalfall:** 308 Einträge änderten nur `update_date`/`update_type`; 40
  änderten Inhalt (`availability` 33, `shortage_reason` 31, `presentation` 5); 1 228 blieben gleich.
- **`presentation` wird an Ort und Stelle umgeschrieben** — drei Einträge desselben Wirkstoffs mit
  Erstmeldung 2018-03-23 wurden am 2026-11-20 `Revised`, und nur der Text der Darreichung änderte
  sich. Mein erster Schlüssel enthielt `presentation` und zählte sie als „gefallen + neu"; der
  Schlüssel ohne `presentation` ist der richtige. Für V0: die Identität ist NDC + Firma, nicht der
  Produkttext.
- **Die 8 gefallenen Einträge** sind alle `To Be Discontinued`, `update_type` `New`, und tragen alle
  dasselbe Erstmeldedatum **2025-11-19** — sie fielen am Jahrestag. Eine einfache Ein-Jahres-Frist
  ist es nicht: `To Be Discontinued`-Einträge mit Erstmeldung 2023-04-28 stehen in beiden Fassungen.
  Ursache nicht bewiesen; ein Kandidat für die Folge, nicht für einen Schluss. Keiner der 8 ging über
  `Resolved` — er war am einen Tag da und am nächsten für jeden Leser fort.
- Die 5 neuen: alle `To Be Discontinued`, `New`, Erstmeldung 2026-11-18 bis 2026-11-20.

### BfArM (CSV 2026-11-19 gegen 2026-11-21) — nur Zählungen

- 942 → 942 Zeilen, 546 → 542 Meldungen (Bearbeitungsnummern), 928 → 928 PZN.
- **Eine Meldung wird nie geändert, sie wird ersetzt.** Alle 523 Meldungen, die in beiden Fassungen
  stehen, sind in jedem Datums-, Status- und Grundfeld gleich. 23 Meldungen fielen, 19 kamen neu.
- **15 der 23 gefallenen haben einen Nachfolger** in der neuen Fassung: eine neue Änderungsmeldung,
  die dieselbe Erstmeldung zitiert (11) oder die gefallene Meldung selbst als Erstmeldung zitiert (4).
  Zwischen Vorgänger und Nachfolger: **in 12 von 15 rückte `Ende` nach hinten** (nie nach vorn), in
  1 wurde `Beginn` umgeschrieben, in 3 änderte sich kein Uhrfeld. Wer die Datei nur heute liest, sieht
  das alte erwartete Ende nicht mehr — und auch nicht, dass es eines gab.
- 8 gefallene Meldungen ohne Nachfolger; von allen 23 gefallenen lag das `Ende` bei 14 vor heute.
- Weiterhin steht **keine** zitierte Erstmeldung selbst in der Datei (0 von allen zitierten, beide
  Fassungen) — der Befund aus Teil 1 hält in der zweiten Fassung.
- Neue Meldungen: 4 neue Erstmeldungen, 15 Änderungsmeldungen (siehe oben).

### EMA (Datei vom 19/11/2026 06:00 gegen 21/11/2026 06:00)

- 85 → 86 Einträge (Schlüssel: `Shortage URL`), 1 neu (`Shortage ongoing`), **0 gefallen, 0 Felder
  geändert** in den 85 gemeinsamen. Die Kontrolle ist ruhig: ein Register, das nicht löscht und in
  zwei Tagen nichts umschrieb.

## 3. Was das für die Frage des Exposés heißt

Die Frage war, ob ein Register die eigene Uhr umschreibt und ob die tägliche Beobachtung eine andere
Dauer sieht als die letzte Fassung. Zwei Tage beantworten sie nicht, aber sie trennen die Quellen:

- **BfArM** schreibt die Uhr um, und zwar strukturell: das erwartete Ende wird verschoben, indem die
  Meldung durch eine neue ersetzt wird; die alte ist danach für jeden Leser fort. 12 Verschiebungen
  in zwei Tagen bei rund 540 Meldungen. Das ist genau das, was nur ein täglicher Leser festhalten
  kann — ein wöchentlicher sähe von zwei Ersetzungen in einer Woche nur die letzte.
- **openFDA** schreibt in zwei Tagen keine Erstmeldung und keinen Status um, stempelt aber
  massenhaft nach und lässt Einträge ohne `Resolved` verschwinden. Die Revisionen des Erstmeldedatums,
  die der nächste Nachbar (ASPE) vermutete, sind in zwei Tagen nicht zu sehen; ob sie über Wochen
  auftauchen, ist die Frage, die V0 stellen würde.
- **EMA** bleibt die Kontrolle.

## 4. Empfehlung

**GO für einen engen V0, täglich.** Begründung: (a) beide US/EU-Quellen sind mit je einem Abruf pro
Nacht vollständig zu lesen (openFDA-Zip ≈ 0,44 MB plus Index, EMA ≈ 0,09 MB), keyless, innerhalb der
Charta (CC0; Weiterverwendung mit Quellenangabe); (b) das Wegfallen und Ersetzen geschieht von Tag
zu Tag, also ist der tägliche Takt der kleinste, der die Spur hält; (c) die Positivliste und die
Hash-Regel sind in zwei Läufen erprobt und zwischen Tagen vergleichbar.

**Zuschnitt:** openFDA und EMA als Register mit abgeleiteten Zeilen (Positivliste wie in den Proben;
Identität `generic_name` + `package_ndc` + Firmen-Hash; Kodierung erkannt, nicht angenommen); je
Nacht ein Vergleich gegen die Vornacht mit den Klassen dieses Dokuments (gepaart unverändert /
nachgestempelt / Inhalt / Uhr; gefallen; neu). **BfArM** hängt an `REQUESTS.md` (2026-11-20): ohne
Antwort nur Zählungen und Hashes je Nacht — das erkennt, *dass* sich etwas ändert, aber nicht, *in
welche Richtung* das Ende rückt; die Richtung braucht die Zeilen. Kein Hersteller in einer Ausgabe
(E-2), keine Kontaktfelder (I8), keine Bühne.

Die GO-Bitte steht in `REQUESTS.md` (2026-11-21). V0 beginnt erst mit dem GO.

## Bewusst nicht heute

Kein Code unter `practice/src/practice/shortageclock/`, kein Workflow — V0 braucht das GO. Keine
BfArM-Zeile, keine Bearbeitungsnummer im Repositorium. Keine Detailseite eines EMA-Eintrags, kein
Abruf der FDA-Datenbank (404 an beiden Pfaden am 2026-11-19). Keine Ursache für die 8 gefallenen
openFDA-Einträge behauptet. Kein Hersteller in diesem Dokument.
