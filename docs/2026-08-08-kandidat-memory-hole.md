# Kandidat: Memory Hole

**Status:** Exposé · 2026-08-08 · zweiter in der Arbeits-Sequenz (nach Dark Ocean)
**Origin-Experiment:** [Editorial Deadline](https://frankbueltge.de/redaction/) — läuft
täglich weiter; beobachtet derzeit 32 offizielle Seiten mit Before/After-Wayback-Evidenz
und hält explizit fest, dass Veränderung nicht automatisch Vertuschung bedeutet.

## Einzeiler

> Was verändert die Macht an ihrer eigenen öffentlichen Vergangenheit?

## Sprung vom Origin zur Investigation

Heute: `32 URLs → diff → deleted words`. Die Linie skaliert auf zehntausende
institutionelle Seiten (Behörden, Ministerien, Regulierer, Konzerne, internationale
Institutionen) und hebt die Analyse von Wort-Diffs auf **semantische Ereignisse**:
Zahl rückwirkend geändert · Versprechen über Revisionen abgeschwächt · Verantwortung
verschoben · dieselbe Formulierung simultan auf vielen Seiten entfernt · historischer
Claim umgeschrieben. Daraus entsteht ein Langzeitgedächtnis institutioneller Sprache —
und maschinelle Anomalie-Entdeckung darüber.

## Ästhetische Operation

Die Maschine zeigt nicht das Archiv — **sie komponiert mit dem, was daraus
verschwindet.** Eine Oberfläche aus gelöschter Sprache; Corrections überschreiben
sichtbar statt zu löschen. Zehn-Sekunden-Einstieg trägt sofort („A public page lost
4,562 words. SHOW ME WHAT DISAPPEARED").

## Maschinen-Überlegenheit

Zehntausende Seiten über Jahre diffen, semantisch klassifizieren, Simultanität über
Institutionen erkennen — reine machine attention. Wayback liefert historische Tiefe ab
Tag 1 (im SBTI-Kontext live gemessen: >2.000 Fassungen je Schlüsselseite).

## Datenlage / Vorbehalte (vor Audit prüfen)

- Wayback CDX + Live-Fetches: frei, hausintern erprobt (`pipelines/redaction/cdx.py`,
  Salience-Filter gegen HTML-Rauschen — das Kernproblem ist gelöst vorhanden).
- EDGI web-monitoring (Open Source) als Prior Art und ggf. Werkzeug — Abgrenzung
  dokumentieren: EDGI überwacht, Memory Hole untersucht und komponiert.
- Semantische Diffs brauchen ein Modell → Trace-Pflicht, Konfidenz ausgewiesen;
  strukturelle Diffs bleiben das deterministische Fundament.
- E-2 bleibt scharf: „Institution X vertuscht" ist keine Ausgabe; publiziert werden
  dokumentierte Änderungen mit Bytes.

## Blocker

Watchlist-Kuration (wessen Gedächtnis? — redaktionelle Entscheidung mit Frank);
Modell-Kosten der semantischen Schicht; Abgrenzung zur laufenden Redaction (Origin
läuft weiter, Memory Hole zitiert es).
