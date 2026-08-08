# Kandidat: The Synthetic Flood

**Status:** Exposé zur Mitnahme in eine eigene Session · 2026-08-08
**Kontext:** Drittplatzierter Kandidat für Project 001 der machine investigative practice
(gewählt wurde The Foreknown). Atlas-Lücke: Feld 12 „Sprache & Generativität" ist mit
24 von 494 Werken dünn besetzt — und kein Werk *vermisst* die synthetische Flut, alle
*benutzen* Generativität.

## Einzeiler

Eine Maschine vermisst kontinuierlich, wie viel der öffentlichen Sprache von Maschinen
geschrieben wird — KI, die KI beim Fluten der Öffentlichkeit zusieht, mit der eigenen
Unzuverlässigkeit als Teil der Messung.

## Forschungsfrage

Lässt sich die Maschinisierung der öffentlichen Sprache — Nachrichten, Behördentexte,
Produktrezensionen, Wissenschafts-Abstracts — als kontinuierliche, nachprüfbare Messreihe
führen, wenn der Messapparat selbst aus derselben Technologie besteht, die er vermisst?

## Warum das konzeptuell heiß ist

- „Dead Internet" ist Volksmythos ohne Messung; seriöse Zahlen sind Einzelstudien.
- Die Selbstbezüglichkeit ist keine Schwäche, sondern der Kern: Das Lab-Prinzip „wo das
  Modell selbst der Gegenstand ist, wird seine Unzuverlässigkeit Teil der Messung" wird
  hier zum ganzen Werk. Detektions-Unsicherheit wird nicht versteckt, sondern ist die
  zentrale ausgestellte Größe — mit Konfidenzbändern, Nullhypothesen, Negativkontrollen.
- Politisch dringlich: Epistemische Verschmutzung ist DAS Infrastrukturproblem der
  Öffentlichkeit; die EU diskutiert Kennzeichnungspflichten (AI Act Art. 50 blieb
  im Digital Omnibus unangetastet — Transparenzpflichten kommen).

## Maschinen-Überlegenheit

- Millionen Seiten lesen, in Dutzenden Sprachen, jede Woche neu — nur maschinell möglich.
- Längsschnitt: dieselben Domains/Korpora über Jahre — Driftmessung statt Momentaufnahme.
- Robuste Teilmessungen, die NICHT auf wackliger KI-Text-Detektion beruhen:
  Duplikations-/Ähnlichkeitsnetzwerke, Übersetzungsschleifen, Templating-Signaturen,
  Publikationsfrequenz-Anomalien (ein „Lokalblatt", das 400 Artikel/Tag publiziert),
  Autoren-Entropie. Die harte Detektion („ist dieser Text KI?") bleibt als ausgewiesen
  unsichere Schicht obenauf.

## Datenlage (Kurzcheck 2026-08-08)

| Quelle | Status | Notiz |
|---|---|---|
| Common Crawl | ✅ live geprüft: Index CC-MAIN-2026-30 (Juli 2026) | Milliarden Seiten, CDX-API + WARC-Bytes, frei; historische Crawls seit 2008 → Längsschnitt ab Tag 1 |
| GDELT | ✅ (im Lab produktiv, Consensus/Newspool) | Nachrichtenschicht; Überlappung mit The Consensus beachten |
| Wikipedia/Wikidata Dumps | offen, zu prüfen | Kontrollkorpus mit Editier-Provenienz |
| OpenAlex/Crossref | offen, zu prüfen | Wissenschafts-Abstracts (LLM-Marker-Studien existieren als Vorbild) |
| Detektions-Benchmarks | zu prüfen | Für die ehrliche Kalibrierung der unsicheren Schicht |

## Form / Dramaturgie (Bühne-A-kompatibel)

- **ATTRACT:** Eine Sprachfläche, die vor den Augen kippt — echte Textströme, in denen
  die maschinell-verdächtigen Passagen langsam ausbleichen oder sich verdoppeln.
  Kernzahl des Tages: „Von X gelesenen Seiten trugen Y die Signatur der Maschine —
  Konfidenz: niedrig/mittel/hoch."
- **ENTER:** Ein Duplikationsnetz öffnen: derselbe Text in 40 Gewändern über 12 Domains.
- **INVESTIGATE:** Drift über Jahre (Common-Crawl-Längsschnitt), Sprachen im Vergleich,
  die Übersetzungsschleifen.
- **VERIFY:** WARC-Bytes, Hashes, Methoden, Konfidenz-Kalibrierung, Negativkontrollen.
- Ästhetik aus der Epistemologie: repetition, uncertainty, accumulation — Unsicherheit
  als sichtbarer Raum, nicht als Fußnote.

## Alleinstellung & Nachbarschaften (vor Bau prüfen)

- NewsGuard trackt „AI-generated news sites" — kommerziell, Listen, keine offene Messung.
- Originality.ai/GPTZero publizieren Marketing-Studien — keine Provenienz, kein Archiv.
- Akademische Einzelstudien (arXiv: „synthetic text prevalence", Übersetzungsschleifen-
  Paper) — Momentaufnahmen, keine laufende öffentliche Messreihe.
- **Abgrenzung im eigenen Haus:** The Consensus misst orchestrierte Gleichförmigkeit in
  Nachrichten (GDELT-Phrasen). The Synthetic Flood misst Maschinisierung der Sprache
  breiter (Web, Behörden, Wissenschaft, Rezensionen) und führt die Detektions-
  unsicherheit als Hauptgröße. Kopplung möglich, Verwechslung vermeiden.

## Grenzen / Risiken (ehrlich)

- **KI-Text-Detektion ist unzuverlässig** — deshalb Architektur in zwei Schichten:
  robuste strukturelle Messungen (Duplikation, Frequenz, Netzwerke) als Fundament,
  Detektion nur als ausgewiesen unsichere Schätzschicht. Wenn die Unsicherheit die
  Messung frisst, ist DAS der publizierte Befund.
- Rechenkosten: Common-Crawl-Läufe brauchen echtes Compute (Athena/lokale Verarbeitung
  von Teilkorpora) — Kostenrahmen nötig.
- Keine Domain-Prangerlisten ohne wasserdichte Evidenz (E-2): publiziert werden
  Verteilungen, Netzwerke, Fallstudien mit Originalbytes.

## V0-Skizze (kleinster Slice)

Ein Korpus-Ausschnitt (z. B. deutschsprachige „Lokalnachrichten"-Domains aus Common
Crawl), zwei robuste Messgrößen (Duplikationsnetz + Publikationsfrequenz-Anomalien),
eine unsichere Schicht (Detektor mit publizierter Kalibrierung), monatliche Messreihe
committet. E2E: ein Duplikationsnetz mit ≥10 Domains, vollständig belegt mit
WARC-Bytes, plus ehrliche Konfidenzrechnung.

## Offene Fragen für die aufnehmende Session

1. Compute-Modell für Common Crawl (Teilkorpora lokal vs. AWS-Athena-Kosten).
2. Detektor-Wahl + Kalibrierungsprotokoll (welche Negativkontrollen?).
3. Verhältnis zu The Consensus (Kopplung oder strikte Trennung?).
4. Sprachen der ersten Messreihe (DE-Start wie skizziert, oder EN wegen Korpusgröße?).
