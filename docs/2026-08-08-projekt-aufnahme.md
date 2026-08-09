# Projekt-Aufnahme: Wie weitere Kandidaten in die Praxis kommen

**Datum:** 2026-08-08 · **Status:** Vorschlag an Frank (sein Gegenvorschlag mit ChatGPT
steht aus; dieses Dokument ist die Vergleichsbasis, kein Beschluss)
**Kandidaten-Backlog:** `docs/2026-08-08-kandidat-planetary-listening.md`,
`docs/2026-08-08-kandidat-synthetic-flood.md` (weitere folgen)

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

> **Nachtrag 2026-08-09 (Frank, vor dem Dark-Ocean-Fenster):** Der Review am Ende des
> E-Experiments kennt **drei** Ausgänge, nicht zwei — RUNNING · Flagship (Bühne),
> RUNNING · Instrument (läuft leise weiter, keine Bühne), RETIRED. Anlass und Wortlaut:
> `2026-08-09-dark-ocean-e-experiment-kriterien.md` §2. Grund: Trägt die Messung, aber
> nicht die Form, wären beide Zwei-Wege-Antworten gelogen — Bühne erzwingen oder ein
> funktionierendes Instrument töten. Gilt ab sofort für alle Kandidaten.

1. **EXPOSÉ** — Forschungsfrage, Maschinen-Überlegenheit, Datenlage-Kurzcheck, Grenzen,
   V0-Skizze, offene Fragen (Muster: die beiden vorhandenen Kandidaten-Exposés).
2. **AUDIT** — Go/No-Go-Protokoll je Quelle mit Live-Probes (dataset-hub-Methode; Lehre
   aus SBTI: externe Annahmen altern schneller als Architekturen). Endet mit einem
   datierten Audit-Dokument wie `2026-08-08-foreknown-001-audit-und-entwurf.md`.
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

---

## Nachtrag (2026-08-08, abends): Synthese mit Franks ChatGPT-Dokumenten

Frank hat drei Dokumente aus seinem ChatGPT-Strang eingebracht. Chronologie: Die beiden
älteren (Dark Ocean als 001; Founding-Corpus-Tabelle 001–004) entstanden BEVOR ChatGPT
The Foreknown kannte — sie beantworten dieselbe Flagship-Frage parallel; das jüngste
Dokument kennt Foreknown/Repo/Bühne und bestätigt Foreknown als 001. Beschluss:

### Übernommen

1. **Founding Corpus.** Die Praxis startet nicht bei null: Das Lab besitzt ein
   proto-investigatives Werkcorpus mit einer gemeinsamen Operation — *Differenzen
   zwischen öffentlichen Darstellungen eines Zustands und anderen technisch
   beobachtbaren Versionen desselben Zustands* („multiple regimes of visibility"):
   Ghost Fleet (deklariert ≠ physisch sichtbar), Consensus (unabhängig erscheinend ≠
   gemeinsamer Ursprung), Editorial Deadline (heutige Aussage ≠ eigene Aktenlage),
   Two Meters / The Floor / One Tap (legitime Messregime ≠ einander).
2. **Origin-Experiment-Muster statt Portierung.** Ein neues Projekt WÄCHST aus einem
   Lab-Experiment; das Original bleibt vollständig erhalten, zitierbar, unter seiner
   URL, und wird künftig als „ORIGIN" ausgewiesen. Nichts wird still umetikettiert.
   Field-/Studio-Werke (Two Meters, The Floor, One Tap) behalten ihre
   Ecology-Provenienz und werden nur als externe Precursors referenziert.
3. **Founding sensibility, keine Verfassung.** discrepancy · absence · duplication ·
   rewriting · measurement boundaries · visibility · provenance · physical trace
   werden die ersten Discovery-Operatoren — ausdrücklich Startsensibilität, kein
   Oberthema. Der Erfolgsfall bleibt ein Projekt, das niemand von uns vorgeschlagen
   hat („006-Punkt").
4. **Werk-Tiefe vor neuen Quellen.** The Foreknown wird als vollständiges Werk gebaut
   (Reaktions-Achse nach Maschinen-Proposal `sensor-fts-country-coverage`, dann
   ENTER → INVESTIGATE → VERIFY), BEVOR neue Quellen oder Projekte starten. FEWS/IPC
   rückt nach hinten.
5. **Substrat-Verträge auf Papier, Code bei Bedarf:** `artifact_ref` (Origin,
   Abrufzeit, Hash, media_type, storage_uri — damit Git nicht unbemerkt
   Universalmedium wird) und `stage_moment` (Projekte liefern der gemeinsamen Bühne
   Momente statt Cards). Implementiert, wenn das ZWEITE Projekt sie real braucht;
   die Substrat-Extraktion aus Foreknown ist der Stresstest, nicht der Vorrat.
6. **Die harte Lehre aus One Tap** (zurückgezogen nach unzureichenden Inszenierungen,
   Recherche blieb): *Gute Evidence ergibt nicht automatisch ein gutes digitales
   Werk.* Abnahme-Maßstab für jede künftige Projekt-Form.
7. **SBTI-Bühnenlabel** perspektivisch: „EARLY INSTRUMENT — STILL RUNNING".

### Angepasst (Widerspruch, begründet)

- **The Foreknown bleibt 001** — Franks Session-Entscheidung, vom jüngsten Dokument
  bestätigt; die Dark-Ocean-als-001-Dokumente sind der ältere Parallel-Strang.
- **Keine Vorab-Nummern.** Beide älteren Dokumente vergeben 001–004 vor jedem Audit —
  das Roadmap-vor-Realität-Muster, das die Korrektur beerdigt hat. Arbeits-Sequenz ja,
  Nummer erst bei RUNNING.
- **Chorus vs. Synthetic Flood:** dieselbe Linie (Sprache in Maschinen-Skalierung,
  Origin: The Consensus). Schwerpunkt entscheidet das Audit — EIN Projekt, keine
  Doppelarchitektur.

### Arbeits-Sequenz der Audits

```
JETZT   Foreknown als vollständiges Werk
DANN    Dark-Ocean-Linie    (Origin: The Ghost Fleet; Substrat-Stresstest Geodaten;
                             Exposé: docs/2026-08-08-kandidat-dark-ocean.md)
DANN    Memory-Hole-Linie   (Origin: Editorial Deadline; Text/Zeit; zweiter Stresstest;
                             Exposé: docs/2026-08-08-kandidat-memory-hole.md)
DANN    Wahl: Chorus/Synthetic-Flood-Linie oder Planetary Listening
SPÄTER  Compute-Ground-Linie (Precursors extern: Two Meters, The Floor, One Tap;
                             Exposé: docs/2026-08-08-kandidat-compute-ground.md)
```

Jede Stufe durchläuft den Aufnahme-Pfad oben; Origins beschleunigen Audits, ersetzen
sie nicht.
