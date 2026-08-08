# The Foreknown — Project 001: Quellen-Audit & V0-Entwurf

**Datum:** 2026-08-09 · **Status:** Entwurf nach Franks Zuschlag („lass the foreknown nehmen")
**Einordnung:** Project 001 der machine investigative practice (Korrektur-Dokument
2026-08-08). Bühne: Prototyp A. SBTI läuft parallel als Hintergrund-Observatorium weiter.
**Ablage-Hinweis:** Dieses Dokument zieht um, sobald die Praxis ihr eigenes Repo hat.

## Einzeiler

> An observatory of announced futures. Die Maschine beurkundet, was wann wissbar war —
> und vermisst die Lücke zwischen Warnung und Reaktion, während die Uhr noch läuft.

Der konzeptuelle Kern: **Provenienz auf die Zukunft angewandt.** Jede Warnung wird im
Moment ihrer Ausgabe konserviert und gehasht (append-only, kein Backfill) — das Archiv
beweist Vorherwissen, bevor das Ereignis eintritt. Das generalisiert den stärksten Zug
aus SBTI („das Vorher-Bild sichern") zur Signatur der Praxis. Atlas-Lücke: Feld 9
(Zeit & Archiv, 46 Werke) schaut ausschließlich rückwärts; kein Werk im Atlas (494)
arbeitet mit Antizipation.

## Quellen-Audit (Live-Probes 2026-08-08/09)

| Quelle | Rolle | Status | Befund |
|---|---|---|---|
| **GDACS** (EU/UN) | Katastrophen-Alerts, alle Typen | ✅ live, kein Key | Event-API HTTP 200, 142 KB aktive Orange/Rot-Alerts; strukturiert (eventtype, alertlevel, fromdate) |
| **NOAA NHC** | Zyklon-Advisories (Atlantik/Pazifik) | ✅ live, kein Key | CurrentStorms.json HTTP 200 — aktuell leer (0 Stürme): ehrlicher Ruhezustand, API trägt |
| **ECMWF Open Data** | Wetter-/Extremvorhersagen (Rohdaten) | ✅ live, kein Key | data.ecmwf.int HTTP 200; offen seit 2022, CC BY 4.0 — die Notariats-Quelle für Wetter-Zukünfte |
| **OCHA FTS/HPC** | Geldströme + Response-Pläne | ✅ live, kein Key | flow-API HTTP 200; 35 Pläne 2026 mit Metadaten — die „was bewegte sich"-Achse |
| **FEWS NET** | Hungersnot-Frühwarnung (IPC-Phasen, Projektionen) | ⚠️ live, aber ungefiltert riesig | HTTP 200, Endpoint lieferte 1,84 GB Gesamtbestand — enorme historische Tiefe; Filter-/Paginierungs-Parameter vor Bau klären |
| **ReliefWeb v2** | Lagebilder/Ereignis-Verifikation | ⚠️ HTTP 403 | v1 stillgelegt, v2 verlangt registrierte appname — Registrierung oder Verzicht (GDACS deckt Verifikation teilweise) |
| **GDELT** | Aufmerksamkeits-Achse | ✅ hausintern produktiv | Consensus/Newspool-Pipelines nutzen die Rohdateien bereits |
| GloFAS/EFAS (Copernicus) | Flutvorhersagen | zu prüfen | CDS-Registrierung + Key (frei); Phase 2 |
| IPC direkt / EM-DAT | Projektionen / Ausgänge | zu prüfen | Key- bzw. registrierungspflichtig; Phase 2 |

**Ereignisdichte bestätigt:** GDACS führt permanent aktive Alerts; FEWS projiziert
Monate voraus; ECMWF publiziert mehrmals täglich. Es gibt keine „0 investigations"-Wochen
— die Welt kündigt ununterbrochen Zukünfte an.

## V0-Entwurf — offen gebaut (Lehre aus der SBTI-Korrektur)

### Die Grundeinheit: die angekündigte Zukunft

```
announced_future {
  what / where / severity          — aus der Quelle, strukturiert wo möglich
  announced_at (UTC)               — Abrufzeit = Beurkundungszeit
  expected_window                  — wann die Zukunft fällig ist
  source + preserved bytes + hash  — I1, unverändert aus dem Substrat
  status: OPEN → ARRIVED | NOT_ARRIVED | REVISED | EXPIRED_UNRESOLVED
}
```

`NOT_ARRIVED` ist kein Fehler, sondern gemessene Vorhersage-Güte (Terminal-State-Logik
aus dem Substrat). `REVISED` — eine still herabgestufte oder verschobene Warnung — ist
ein eigenes Signal erster Klasse.

### Der Kreislauf

1. **Notariat (mehrquellig ab Tag 1 — nicht wieder ein Ein-Quellen-Korridor):**
   GDACS + NHC + ECMWF(-Ausschnitt) + FEWS-Projektionen nächtlich abrufen, Bytes hashen,
   announced_futures extrahieren (deterministisch bei strukturierten Quellen; LLM-gestützt
   mit Primärbytes-Bindung bei Prosa — Modell/Kosten im Autonomie-Trace).
2. **Die Uhren laufen:** Offene Zukünfte als Countdown-Register; täglich dazu die
   Reaktions-Achsen konserviert: FTS-Geldstände, GDELT-Aufmerksamkeitsvolumen.
3. **Auflösung:** Fenster abgelaufen → Abgleich (GDACS-Events, später EM-DAT):
   eingetreten? Vorlaufzeit? Was bewegte sich zwischen Warnung und Ereignis?
4. **Discovery-Pass (die Intelligenz-Schicht der Praxis):** nächtlich, budgetiert,
   über der Akkumulation — darf neue Warnquellen und neue Differenzarten VORSCHLAGEN
   (z. B. „Funding stagniert während Countdown < 30 Tage", „Warnung wurde still
   revidiert") als committete sensor proposals. Delegation-Charter §1 gilt: Aufnahme
   offener, key-/kosten-/personenfreier Quellen ist delegiert.

### Bühne (aus Prototyp A)

Die Stage zeigt Foreknown als erstes lebendes Material: laufende Countdowns realer
angekündigter Zukünfte, das Beurkundungs-Ledger, die Ruhe ehrlich („No storm is
announced tonight"). Exhibition Mode von Anfang an (Attract-Loop, Distanz-Lesbarkeit,
QR-Handoff). Jede Zahl ein echter Systemzustand.

### Ethik-Grenzen (konstitutiv, nicht nachträglich)

- Gegenstand ist das **Warnsystem und die institutionelle Zeit — nie die Opfer.**
  Keine Bilder von Leid, keine Personen, keine Ortsauflösung unterhalb administrativer
  Ebenen.
- **Keine Schuld-Claims** (E-2): publiziert werden Zeitpunkte, Beträge, Volumina,
  Differenzen. „Wer versagt hat" ist keine Ausgabe dieser Maschine.
- **Wir prognostizieren nicht selbst.** Beurkundet werden DEREN Vorhersagen; die
  Maschine fügt keine eigenen Risikoschätzungen hinzu. (Grenze gegen Katastrophen-Orakel.)
- Nüchternheit als Register — die Uhren sind dramatisch genug.

### E1 — erstes E2E-Experiment (14 Nächte)

- ≥ 20 beurkundete announced_futures aus ≥ 3 Quellen, alle mit Bytes+Hash+Abrufzeit.
- ≥ 1 vollständiger Zyklus Warnung → Auflösung mit Geld- und Aufmerksamkeits-Zeitreihe.
- Bühne live mit echten Countdowns; Provenienz-Verifikator grün; Autonomie-Trace
  vollständig (inkl. Discovery-Pass-Kosten).
- Ehrlichkeits-Kriterium: mindestens ein NOT_ARRIVED oder REVISED sichtbar publiziert.

### Bewusst nicht gebaut (V0)

Eigene Vorhersagemodelle · Wirksamkeits-Scores für Hilfsorganisationen · Länder-Rankings ·
Opfer-Darstellungen · ReliefWeb-Abhängigkeit (bis Registrierung geklärt) ·
GloFAS/IPC-direkt (Phase 2) · Integration in die Research Ecology.

## Offene Entscheidungen (Frank)

1. **Heimat:** eigenes Repo `the-foreknown` + Praxis-Repo für die Stage — oder erst die
   Praxis benennen? (Repo-Anlage braucht wie gehabt deinen Knopf.)
2. **Name der Praxis** (weiter offen; die Stage trägt bisher „machine attention").
3. **Discovery-Budget** pro Nacht (Vorschlag: Abo-Token, hartes Limit, Trace-Pflicht).
4. **Stage-Deployment:** GitHub Pages wie SBTI, oder direkt auf frankbueltge.de?
