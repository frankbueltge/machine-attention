# Memory Hole — E-Experiment: Abnahmekriterien

**Datum:** 2026-08-22 · **Stufe:** 4 des Aufnahme-Pfads · **Grundlage:** Audit
`2026-08-14-memory-hole-audit.md` (§8 Kriterien, §10 Empfehlung „Instrument", §11 GO mit
sieben Auflagen), V0-Baubericht `2026-08-15-memory-hole-v0.md`, Semantik-Routing
`2026-08-15-semantik-ueber-routine.md`

## 0. Bindung, und warum dieses Dokument sieben Tage zu spät kommt

Das Audit verlangte, die Kriterien **vor der ersten Nacht** zu committen. Memory Hole läuft
seit dem 2026-08-13 nächtlich — acht Lesungen liegen vor, ohne dass ein Fenster erklärt war.
Das wird hier nicht geheilt, sondern abgetrennt: **die acht Nächte 2026-08-13 bis
2026-08-21 zählen nicht als E-Evidenz.** Sie sind Vor-Fenster-Kontext, Betriebsbeleg und
Fehlerquelle — dieselbe Disziplin, die Dark Ocean auf seine zwei Vor-Fenster-Nächte
angewandt hat.

Änderungen an diesem Dokument sind bis Nacht 1 erlaubt (datierter Nachtrag mit Begründung),
danach nicht mehr. Das Fenster öffnet **nicht** mit dem Datum dieses Dokuments, sondern mit
der ersten Nacht nach Erfüllung von §1 — die Öffnung wird als `memoryhole-window-open` im
Autonomie-Log festgehalten, das Review fällt auf Nacht 14 + 1 Tag.

## 1. Drei Bau-Bedingungen vor Nacht 1 (die Dark-Ocean-Lehre)

Das Dark-Ocean-Review vom heutigen Tag hat zwei Fehler dieser Praxis benannt: ein Fenster,
dessen tragendes Kriterium von der eigenen, noch reparaturbedürftigen Infrastruktur
abhängt, misst die Infrastruktur; und ein Kriterium, das eine nicht erreichbare Quelle
voraussetzt, ist ein Versprechen. Beide Fehler drohen hier unmittelbar. Deshalb:

**B-1 — Auflage 5 des GO ist eingelöst.** Die zwei im Audit gefundenen Origin-Bugs
(4xx-Aufnahme als Löschung ohne Nachprüfung; WAF-Challenge-Seite als HTTP 200 archiviert)
werden im Origin behoben, als eigener PR, bevor Memory Hole ein Fenster eröffnet. Offen
seit dem 2026-08-15. Wer ein Instrument über die Vergangenheit anderer betreibt, während
sein eigener Vorläufer nachweislich falsch löscht, misst nichts.

**B-2 — Die Abruf-Zuverlässigkeit ist gebaut und belegt.** In den acht Vor-Fenster-Nächten
lagen die Ausfälle zwischen 1 und 30 je Nacht (überwiegend HTTP 504 der Wayback-Machine),
und **drei Nächte holten null Aufnahme-Paare** (08-16 bis 08-19 teilweise, 08-16 mit 30
Ausfällen und 0 Paaren). Ohne Retry-/Backoff-Disziplin messen alle Ertragskriterien die
Verfügbarkeit eines Fremdarchivs, nicht das Verhalten der Institutionen. Verlangt: Retry
mit Backoff je Anfrage, Ausfälle weiter vollständig im Record, und ein Beweislauf über
drei aufeinanderfolgende Nächte mit **je ≥ 10 validierten Aufnahme-Paaren**.

**B-3 — Der Verdikt-Weg hat einmal funktioniert.** Seit dem 2026-08-15 läuft die
Semantik-Schicht über den nächtlichen Discovery-Pass; bis heute existiert **keine einzige**
Datei unter `memoryhole/verdicts/`. Kriterium 5 (Determinismus gegen Modell) ist ohne sie
strukturell unmessbar. Verlangt: mindestens ein committetes, prüfergrünes Verdikt-File vor
Nacht 1.

## 2. Das Fenster

Vierzehn Nächte, gerechnet ab der ersten Nacht nach §1. Eine Nacht zählt, wenn sie eine
committete Lesung hat (auch eine leere) und `verify.py` auf ihr grün ist.

## 3. Abnahmekriterien

### A — Betrieb

| # | Kriterium |
|---|---|
| A1 | ≥ 12 von 14 Nächten mit committeter Lesung, `failures` explizit |
| A2 | ≥ 12 von 14 Nächten mit **≥ 10 validierten Aufnahme-Paaren** (die Latte, die B-2 vorher belegt) |
| A3 | jede fehlende Nacht mit benannter Ursache im Autonomie-Log — keine stillen Lücken |
| A4 | `verify.py` grün auf jeder committeten Nacht (CI-Gate) |
| A5 | Kosten: 0 € eigener Schlüssel; die Modell-Kosten des Discovery-Passes ausgewiesen, gegen die Obergrenze, mit Nächten am Deckel (Audit-Kriterium 7) |

### B — Die Kriterien des Audits, Schwellen unverändert übernommen

| # | Kriterium (Audit §8) | Latte |
|---|---|---|
| B1 | **Falsch-Positiv-Rate** — publizierte Ereignisse auf der Kontrollgruppe E (20 Seiten) | **0.** Jedes Ereignis dort ist ein Verfahrensfehler |
| B2 | **Gültigkeitsgate** — Anteil `unverifiable` je Kategorie berichtet; null publizierte Records, die auf Challenge-, Consent- oder Bot-Wall-Seiten beruhen | 0 solcher Records |
| B3 | **Ertrag** — Nächte mit ≥ 1 validiertem semantischem Ereignis | **≥ 4 von 14** |
| B4 | **Löschbehauptungen** — wie viele 4xx-Kandidaten überleben die Live-Nachprüfung; die Zahl misst zugleich die heutige Größe des Origin-Bugs | Zahl berichtet, Disclosure-Klassen getrennt |
| B5 | **Determinismus gegen Modell** — Übereinstimmung von Regel- und Modellschicht auf der Schnittmenge; **kein Ereignistyp allein aus dem Modell** | 0 modell-only Ereignistypen |
| B6 | **Simultanität** (die eigentliche Hypothese) — siehe §4 | vorab registriert, Null-Befund publizierbar |
| B7 | **Laufzeit und Ausfälle** — nächtliche Laufzeit, 504-Quote, Nächte mit unvollständigem Erfassungslauf | berichtet |
| B8 | **Substrat** — was in `practice/` gebrochen ist, als Befund | berichtet |

### C — Ethik und Charter (Ausschluss, keine Punkte)

Kein Personenbezug in abgeleiteten Records; keine Schuldzuweisung an namentliche Personen;
publiziert werden Änderungen an institutionellen Texten, nie Motive. Kein Record, der auf
einer Seite beruht, die das Gültigkeitsgate nicht passiert hat. Simultanität wird bis zur
Entscheidung über B6 **nirgends** behauptet — weder auf der Site noch im Methodenblatt
(Auflage 7).

**Bestanden = A vollständig · B1, B2, B5 ohne Verstoß · B3 erfüllt · B4, B7, B8 berichtet ·
C ohne Verstoß.** B6 entscheidet über die Form, nicht über die Existenz.

## 4. Die vorab registrierte Simultanitäts-Schwelle (B6)

**Hypothese:** Innerhalb der 14 Nächte verschwindet **dieselbe Formulierung** von ≥ 3
Seiten aus ≥ 2 Institutionen.

Vorab festgelegt, damit später nichts hineingelesen werden kann:

- **„Formulierung"** = eine normalisierte Passage von ≥ 8 Token (Kleinschreibung,
  Whitespace kollabiert, Satzzeichen entfernt), die in der Vor-Aufnahme vorhanden und in
  der Nach-Aufnahme nicht mehr vorhanden ist.
- **„Dieselbe"** = identische normalisierte Passage. Keine Ähnlichkeitsschwelle, kein
  Embedding-Vergleich — beides wäre ein Freiheitsgrad, den niemand nachrechnen kann.
- **„Verschwindet"** = ein Ereignis der Klassen `commitment_removed`,
  `attribution_removed` oder `negation_flipped` auf dieser Passage, oder ihr Wegfall in
  einer Aufnahme, die das Gültigkeitsgate passiert hat.
- **Zählung:** ≥ 3 verschiedene URLs, ≥ 2 verschiedene Institutionen, innerhalb der 14
  Nächte, Institutionen der Kontrollgruppe E ausgeschlossen.
- **Ein Null-Befund ist ein Befund** und wird publiziert: „In 14 Nächten über 22
  Institutionen verschwand keine Formulierung gleichzeitig an mehreren Stellen."

## 5. Was dieses Fenster voraussichtlich ergibt — vorab notiert

Aus den acht Vor-Fenster-Nächten: **eine** Nacht mit typisierten Ereignissen (2026-08-21,
`date_shifted` 1, `number_revised` 1), sieben Nächte mit null. Geradlinig fortgeschrieben
landet der Ertrag bei ~2 von 14 und **reißt die Latte B3 (≥ 4)**.

Diese Erwartung wird hier festgehalten, **und die Latte bleibt trotzdem, wo das Audit sie
hingelegt hat.** Eine Schwelle im Wissen um die Daten nach unten zu korrigieren, ist genau
die bewegliche Latte, an der Dark Ocean heute gescheitert ist — dort war sie
unverschiebbar, hier wäre sie es nicht, und gerade deshalb muss sie stehen. Der Ausgang,
den das Audit für diesen Fall vorgesehen hat, ist ausdrücklich kein Scheitern:
**Instrument mit Wochenkadenz** — jede Nacht sammeln, wöchentlich berichten — oder RETIRED.
Ein Instrument, das viermal im Jahr etwas findet, ist ehrlicher als ein Tagesinstrument,
das täglich nichts findet und trotzdem täglich spricht.

## 6. Drei mögliche Ausgänge

- **RUNNING · Flagship** — nur wenn **B3 und B6** bestehen (Audit §10). Bühne, Werk-Eintrag,
  Methodenblatt.
- **RUNNING · Instrument** — der vom Audit empfohlene Normalfall; Kadenz (täglich oder
  wöchentlich) entscheidet der Ertrag.
- **RETIRED** — wenn A reißt oder B1/B2/B5/C verletzt sind: dann misst das Instrument nicht,
  was es behauptet.

## 7. Bekannte Konfundierer — vor Fensterstart benannt

1. **Die Kadenz des Fremdarchivs ist die Obergrenze.** Wayback liefert je Seite 0–14
   Aufnahmen pro Woche, teils null. Was die Maschine nicht sieht, hat nicht stattgefunden —
   für sie. Jede Ertragszahl ist eine Aussage über Archiv *und* Institution.
2. **Seitentyp-Churn.** Rotierende Teaser auf Startseiten und News-Indizes erzeugen echte
   Entfernungen ohne institutionelle Bedeutung (ESMA-Fall im Audit). Der Salienz-Filter
   dämpft das, hebt es nicht auf.
3. **Das Feld ist außerhalb DE/EU besetzt** (EDGI, 34.999 Seiten, tiefer gebaut). Der
   Unterschied dieses Instruments ist der Zuschnitt (DE/EU/Konzern) und die Typisierung —
   nicht die Idee. Steht so im Methodenblatt, bevor irgendetwas behauptet wird.
4. **19 % HTTP 504 bei Nebenläufigkeit 4**, Latenzen 1,3–60 s, keine 429er: Unzuverlässigkeit
   ist die Fehlerform, nicht Throttling. Genau dagegen steht B-2.
