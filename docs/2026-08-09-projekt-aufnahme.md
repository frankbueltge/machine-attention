# Projekt-Aufnahme: Wie weitere Kandidaten in die Praxis kommen

**Datum:** 2026-08-09 · **Status:** Vorschlag an Frank (sein Gegenvorschlag mit ChatGPT
steht aus; dieses Dokument ist die Vergleichsbasis, kein Beschluss)
**Kandidaten-Backlog:** `docs/2026-08-09-kandidat-planetary-listening.md`,
`docs/2026-08-09-kandidat-synthetic-flood.md` (weitere folgen)

## Grundsatz

Die Praxis ist EINE Maschine mit endlicher Aufmerksamkeit — Projekte sind ihre
Untersuchungen, nicht ihre Filialen. Aufnahme heißt: dieselbe Disziplin, die The Foreknown
durchlaufen hat, kein Sonderweg. Und: **„Baue nicht groß — aber baue offen"** gilt auch
hier — kein Framework für hypothetische Projekte; jede Aufnahme ist ein konkretes Projekt
mit live verifizierten Daten.

## Der Aufnahme-Pfad (fünf Stufen, jede committet)

```
EXPOSÉ → AUDIT → V0 → E-EXPERIMENT → RUNNING        (jederzeit: RETIRED)
```

1. **EXPOSÉ** — Forschungsfrage, Maschinen-Überlegenheit, Datenlage-Kurzcheck, Grenzen,
   V0-Skizze, offene Fragen (Muster: die beiden vorhandenen Kandidaten-Exposés).
2. **AUDIT** — Go/No-Go-Protokoll je Quelle mit Live-Probes (dataset-hub-Methode; Lehre
   aus SBTI: externe Annahmen altern schneller als Architekturen). Endet mit einem
   datierten Audit-Dokument wie `2026-08-09-foreknown-001-audit-und-entwurf.md`.
3. **V0** — kleinster Slice, der nächtlich committete, `verify.py`-geprüfte Records
   erzeugt. Nutzt das Substrat (`practice/`: fetch/preserve/autonomy), erfindet keine
   neue Infrastruktur.
4. **E-EXPERIMENT** — 14 Nächte mit vorab committeten Abnahmekriterien; der Review
   entscheidet über RUNNING (oder ehrliches RETIRED — ein gestorbener Kandidat bleibt
   im Record, wie ein DECLINED am Gate).
5. **RUNNING** — erst jetzt: Bühnen-Präsenz und Site-Erzählung (Werk-Eintrag,
   Methodenblatt). Vorher existiert das Projekt öffentlich nur im Repo.

## Flagship vs. Instrument

Nicht jedes Projekt muss die vier Flagship-Kriterien erfüllen (dringlich · maschinell
überlegen · visuell stark · kontinuierlich lebendig). Zwei Klassen:

- **Flagship** (aktuell: The Foreknown) — trägt die Bühne, erfüllt alle vier.
- **Instrument** (aktuell: state-before-interface) — läuft leise, sammelt, liefert der
  Praxis zu; darf jahrelang „nichts" produzieren. Kein Bühnen-Anspruch, kein
  Produktionsdruck.

Ein Kandidat wird bei Aufnahme klassifiziert; Wechsel ist ein datierter Beschluss.

## Wo ein Projekt wohnt

**Default: im Praxis-Repo** (wie `foreknown/` + `practice.<projekt>`-Paket) — geteiltes
Substrat, EIN Autonomie-Protokoll, EIN Verifikator, EINE Bühne. **Eigenes Repo nur, wenn
die Datenform Git-als-Archiv sprengt** (benannter Fall: Planetary Listening —
Wellenformen; dann hält das Praxis-Repo Registry/Verdikte und verlinkt die Datenheimat).
SBTI bleibt als Sonderfall extern (es war zuerst da).

## Die Rolle der Maschine bei der Aufnahme

Der Discovery-Pass darf ab sofort neben Sensoren und Quellen auch **Projekt-Vorschläge**
liefern (`foreknown/proposals/project-<slug>.json` bzw. künftig `proposals/` auf
Praxis-Ebene): Forschungsfrage, verifizierte Quellen-Probe, Maschinen-Vorteil,
Flagship-/Instrument-Einschätzung — evidenz-zitiert wie alles. Er darf auch die
liegenden Kandidaten-Exposés lesen und konkretisieren (z. B. die offenen Quellenfragen
des Planetary-Listening-Exposés mit Probes beantworten).

**Die Aufnahme selbst bleibt Franks Entscheidung.** Ein neues Projekt heißt neue Kosten,
neue Öffentlichkeit, neuer Scope — das ist ein menschliches Gate im Sinne der Standing
Delegation (E-4/E-6), kein Automatismus. Beleg aus Nacht 1, warum die Rollenteilung
funktioniert: Die Maschine hat die Reaktions-Achse (`sensor-fts-country-coverage`)
selbst vorgeschlagen, bevor ein Mensch sie gebaut hat.

## Sequenzierung (Vorschlag)

**Eine Baustelle zugleich.** Die Maschine kann viele Projekte BETREIBEN, aber wir bauen
nacheinander:

1. **Jetzt:** Foreknown Phase 2 — Reaktions-Achse auf Basis des Maschinen-Proposals,
   dann FEWS NET/IPC (Audit-Stufe), dann E1-Review (~22.08.).
2. **Danach:** nächster Kandidat in den AUDIT — Reihenfolge nach Blocker-Lage, nicht
   nach Vorliebe: Planetary Listening braucht zuerst die Speicherentscheidung
   (Wellenformen ≠ Git), Synthetic Flood zuerst den Compute-Rahmen (Common Crawl).
   Beide Blocker sind in den Exposés benannt; wer seinen Blocker zuerst gelöst hat,
   geht zuerst.
3. **Bühne für mehrere Projekte** (Praxis-Foyer mit „Akten" je Projekt, eigene Form je
   Untersuchung — Feedback-Prinzip „shared machine identity / project-derived form"):
   wird entworfen, WENN das zweite Projekt RUNNING erreicht — nicht vorher. Kein
   Vorrats-Design.

## Bewusst nicht

Kein Multi-Projekt-Framework, keine gemeinsame Ontologie, kein Projekt-Dashboard, keine
Aufnahme ohne Live-Datenprobe, kein Parallel-Bau von zwei V0s, keine Bühnen-Präsenz vor
bestandenem E-Experiment.
