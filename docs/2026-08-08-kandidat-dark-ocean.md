# Kandidat: Dark Ocean

**Status:** Exposé · 2026-08-08 · **designierter nächster Audit-Kandidat** (Arbeits-Sequenz
im Aufnahme-Dokument) · Quelle: Franks/ChatGPTs Vorschlag, destilliert und mit
Prüf-Vorbehalten versehen
**Origin-Experiment:** [The Ghost Fleet](https://frankbueltge.de/ghost-fleet/) — bleibt
vollständig erhalten und zitierbar; Dark Ocean erweitert seine Frage, ersetzt es nicht.

## Einzeiler

> Ships tell the world where they are. Satellites can see where they actually are.
> The two views do not always agree.

## Forschungsfrage

Nicht „finde illegale Schiffe" (methodisch gefährlich, und ein schlechteres Global
Fishing Watch braucht niemand), sondern: **Wie wird Sichtbarkeit über dem größten
öffentlichen Raum des Planeten technisch hergestellt — und wo widersprechen sich die
Sichtbarkeitsregime?** (deklarierter Ozean: AIS ≠ beobachteter Ozean: SAR/optisch/
Nachtlicht). Fischerei, Schifffahrt, Sanktionen, Schutzgebiete sind mögliche
Investigations, nicht der Gegenstand.

## Warum stark (Flagship-Kriterien)

- **Kontinuierlich lebendig:** Das Meer steht nie still; GFW liefert near-real-time
  Presence und Events (Encounters, Loitering).
- **Maschinell überlegen:** Kein Mensch betrachtet dauerhaft den planetaren Ozean in
  mehreren inkompatiblen Sensorsystemen gleichzeitig — hier ist die Maschinenexistenz
  formal notwendig.
- **Historische Tiefe ab Tag 1:** AIS-Presence bis 2012 zurück, Sentinel-1-Archiv bis
  2014 — die Maschine kann rückwärts laufen, kein leerer Speicher.
- **Ästhetisch:** zwei Ozeane übereinander (deklariert/beobachtet), Abwesenheit als
  Information, „the dark ocean" dazwischen. Sub-Werke denkbar: The Vanishing ·
  Two Oceans · Night Fleet · The Line · **False Darkness** (die Maschine untersucht
  ihre eigenen Fehlzuordnungen — passt exakt zur Lab-Ethik).

## Epistemische Disziplin (aus dem Origin übernommen und verschärft)

Der Kern-Move von Ghost Fleet bleibt bindend: Klassifikationen Dritter (GFW
„intentional disabling") sind modellierte Einschätzungen, keine Schuldbehauptungen.
Dark Ocean publiziert Diskontinuitäten zwischen Sichtbarkeitssystemen — „We know where
its public identity ended. We know something remained visible. We do not yet know
whether they are the same object." Kandidaten sterben ehrlich (False Darkness ist ein
Erfolgs-Endzustand).

## Datenlage (VOR dem Audit zu verifizieren — Research References, keine Verträge)

| Quelle | Annahme | Prüf-Vorbehalt |
|---|---|---|
| GFW APIs (identity, presence seit 2012, events) | frei mit API-Token | Terms für künstlerisch-öffentliche Nachnutzung prüfen; Rate Limits messen |
| GFW SAR vessel detections | **Ausfall seit Anfang Juli 2026** (Pipeline-Umstellung auf neuere Sentinel-1-Satelliten) | Status live prüfen; Plan B: eigener begrenzter Sentinel-1-Pfad |
| Copernicus Sentinel-1 GRD | frei via Data Space APIs, Archiv ab 2014 | Volumen! Szenen sind GB-groß → artifact_ref/Nicht-Git-Speicher wird hier erstmals PFLICHT |
| Hausintern: pipelines/ghost-fleet | läuft produktiv nächtlich | Als Origin-Datenbestand und Adapter-Erfahrung nutzen |

## Blocker vor V0 (benannt)

1. **Speicherentscheidung** (SAR-Kacheln ≠ Git) — erster echter Anwendungsfall des
   `artifact_ref`-Vertrags aus dem Aufnahme-Dokument.
2. **GFW-SAR-Ausfall**: GFW abwarten vs. eigener Detection-Pfad — das Audit
   entscheidet mit Live-Probes, nicht mit Hoffnung.
3. Substrat-Extraktion aus Foreknown (fetch/preserve/autonomy generisch genug für
   Geodaten?) — Dark Ocean ist der designierte Stresstest.

## V0-Skizze (kleinster Slice)

Eine Meeresregion (z. B. ein MPA-Rand oder die Ostsee), AIS-Presence + eine
Satelliten-Detektionsquelle, nächtlicher Abgleich: matched / unmatched / gap-and-return,
als committete Records mit Manifesten; Verdikte nur über Sichtbarkeits-Diskontinuitäten.
E-Experiment 14 Nächte; Abnahme u. a.: ≥1 False-Darkness-Fall ehrlich publiziert.
