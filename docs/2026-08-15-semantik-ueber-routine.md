# Memory Hole: Semantik-Schicht über den Routine-Kanal

**Datum:** 2026-08-15 · **Entscheidung:** Frank · **Status:** in Kraft

## Die Entscheidung

Die semantische Schicht des Memory-Hole-Instruments läuft **nicht** über einen
eigenen API-Schlüssel, sondern über denselben Kanal wie alle Modell-Arbeit der
Praxis: den nächtlichen Discovery-Pass, der seit 2026-08-08 als Cloud-Routine
in Franks Claude-Oberfläche lebt. Franks Begründung (Wortlaut privat,
sinngemäß): Alle Modell-Arbeit des Hauses lief bisher als Routine und war
damit in seiner eigenen Oberfläche im Überblick — ein Kanal, eine Übersicht,
keine zweite Abrechnung. Die Schwärzungs-Regel derselben Nacht
(„redact: no verbatim personal messages in the decision record") gilt hier
von der ersten Fassung an.

Die V0 hatte die Schicht als Batch-API-Modul mit eigenem Schlüssel gebaut
(`practice/src/practice/memoryhole/model.py`, der Kostenrahmen stammt aus dem
Audit §5). Das Modul bleibt bestehen und meldet ehrlich „off: no key
configured" — es ist der Fallback, falls das Haus je auf den API-Kanal
wechselt. Der gelebte Pfad ist ab heute:

## Der Pfad

1. Der nächtliche Lauf (02:30 UTC) schreibt die Lesung mit den Enthaltungen
   der Regel-Schicht (`entries[].abstentions`) — unverändert.
2. Der Discovery-Pass (Routine, später in der Nacht) klassifiziert bis zu
   **40** Enthaltungen, salienzstärkste zuerst, und liefert
   `memoryhole/verdicts/<datum>.json` über seinen normalen PR-Weg
   (Pflicht 5 in `discovery/PROMPT.md`).
3. `verify.py::check_memoryhole_verdicts` hält jede Verdikt-Datei an den
   Vertrag: nur Verweise auf tatsächlich enthaltene Passagen
   (`before_sha256`), nur die committeten Ereignistypen (plus
   `none_of_these`), Deckel eingehalten, Modell-ID benannt, `estimated: true`
   an Datei und jedem einzelnen Verdikt.

## Was sich NICHT ändert

- Die Regel-Schicht entscheidet zuerst; Verdikte entstehen nur bei Enthaltung.
- Lesungen werden nie nachträglich editiert — Verdikte sind Annotation,
  nicht Korrektur.
- Jedes Modell-Verdikt bleibt Schätzung und ist so markiert; keine Bühne,
  kein Methodenblatt zitiert es je als Feststellung.
- Audit-Auflage 4 (Deckel, Trace, ehrliche Degradierung) gilt unverändert —
  nur der Transport wechselt: Franks Plan statt API-Rechnung, sichtbar in
  seiner eigenen Oberfläche.

## Offen benannt

Der Discovery-Pass läuft auf dem Modell der Routine (zuletzt Sonnet), nicht
auf dem im Audit kalkulierten Haiku — die Kostenrechnung des Audits ist damit
gegenstandslos, der Verbrauch geht im Routine-Kontingent auf. Die Modell-ID
im Verdikt und im Autonomie-Log bleibt die Offenlegung.
