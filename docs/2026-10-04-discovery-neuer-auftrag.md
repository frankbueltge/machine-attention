# Der Discovery-Pass baut — neuer Auftrag (2026-10-04)

**Datum:** 2026-10-04 · **Entscheidung:** Frank (Maintainer), Wortlaut privat · **Ersetzt:**
den Auftrag in `discovery/PROMPT.md` vom 2026-08-08 (zuletzt ergänzt 2026-08-15)

## Anlass

Der Discovery-Pass war, wie sein Prompt ihn definierte, die Wartung **eines** Instruments. Er
las jede Nacht `foreknown/registry.json`, schrieb Differenz-Beobachtungen über diesen Record,
schlug Sensoren dafür vor und reparierte dessen Code. Daraus wurden in 44 Läufen
45 Beobachtungen und 11 Sensoren, alle über The Foreknown, und sorgfältig gemacht. Die letzten
vier fanden einen VTEC-Jahresfehler, der eine Warnung doppelt zählt, eine Sensor-Klasse, in
der seit 39 Nächten genau ein Fall steckt, und zweimal Feinarbeit an der Verifikation.

In derselben Zeit bewegte sich kein neues Projekt. Das letzte Konzeptdokument ist vom
2026-08-22. Planetary Listening ist seit diesem Tag fertig auditiert und wartet auf ein Go,
nach dem niemand mehr gefragt hat. Synthetic Flood und Compute Ground liegen seit dem
2026-08-08 an ihren Blockern. Frank hatte erwartet, dass der nächtliche Pass die Praxis
weiterentwickelt. Der Prompt hatte ihm das nie aufgetragen.

## Der neue Auftrag (`discovery/PROMPT.md`)

Jede Nacht, in dieser Reihenfolge:

1. **Den Fokus-Kandidaten einen echten Schritt weiterbringen**, entlang EXPOSÉ → AUDIT → V0 →
   E-EXPERIMENT. Ein Schritt ist etwas Committetes, das vorher nicht da war: ein Exposé mit
   benannten Nachbarn, ein Live-Probe mit Manifest, ein getestetes V0-Inkrement, die
   Abnahmekriterien vor dem Fenster.
2. **Die Liste lebendig halten.** `discovery/AGENDA.md` führt der Pass selbst. Wartet der
   Fokus an einem Gate oder Blocker, darf er höchstens ein neues Exposé pro Woche eröffnen und
   geparkte Kandidaten neu lesen, wenn ihr Blocker gefallen sein könnte.
3. **Reparaturen, eng.** Nur wo der Record einen Defekt an einem laufenden Instrument
   beweist (Dark Ocean, Memory Hole, Anker), und nie statt Schritt 1.
4. **Memory-Hole-Urteile** wie bisher, wörtlich übernommen, weil `verify.py` ihr Format
   prüft.

**Die Gates bleiben bei Frank**, so wie der Aufnahme-Pfad sie setzt: das Go für V0, das
Review nach dem E-Experiment und jede Bühnenpräsenz. Neu ist nur, dass der Pass an einem Gate
nicht mehr stehen bleibt. Er schreibt die Anfrage in zwei Sätzen in `REQUESTS.md` und geht zum
nächsten Schritt, der nicht darauf wartet.

**Was unverändert dem Maintainer bleibt:** Geld, personenbezogene Daten, alles, was das Haus
verlässt, Quellen außerhalb der Delegations-Charter und die öffentlichen Behauptungen der
Praxis darüber, was sie bewiesen hat. „Nothing sends itself.“

**Ausdrücklich verboten:** The Foreknown wieder anzuwerfen. Der Notar ist RETIRED
(`docs/2026-10-04-foreknown-retired.md`), und `verify.py` lässt keine Nacht nach dem
2026-10-03 zu.

## Fokus zum Start

**The Interval** (`docs/2026-10-04-kandidat-the-interval.md`): Die Frage des Foreknown wird an
die Uhr verlegt, auf der Reaktion messbar ist. Das sind langsame Ernährungskrisen, gemessen
als Projektion gegen Finanzierung. Das AUDIT hat das Haus am 2026-10-04 gemacht, das Go für V0
hat Frank am selben Tag gegeben. Der Pass baut V0 in nächtlichen Inkrementen.

## Was der Pass kostet

Er läuft weiter als Cloud-Routine in Franks Claude-Oberfläche und zieht damit aus demselben
Nutzungskontingent wie die übrigen Routinen des Hauses. Ein Bau-Auftrag braucht pro Nacht
mehr als eine Lesung. Ist das Wochenlimit erreicht, fällt die Nacht aus. Das ist zulässig: Die
Agenda hält fest, wo es weitergeht.
