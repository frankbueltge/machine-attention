# Bühnen-Ehrlichkeit und Momente — der Cold Start verlässt die Bühne, die Praxis gewinnt ihren Momente-Vertrag

**Datum:** 2026-08-09, Nacht · **Status:** umgesetzt · **Anlass:** Franks Review des
Praxis-Stands (extern beraten), plus das eigene Proposal der Maschine
`sensor-cold-start-overdue-drift` aus Discovery-Nacht 1.

## 1. Der Widerspruch

Die Bühne sagte „**100 warnings under watch right now**" und das Ledger „**Open — the
clocks still running**", während nach der Bühnen-eigenen Regel (deterministisch gegen
`run_date`) **99 von 100** offenen Futures ihr angekündigtes Fenster bereits **vor der
ersten Sichtung** hinter sich hatten — Cold-Start-Artefakte, keine Beobachtung. Die
Dossiers sagten das korrekt („an artefact of when observation began"); die Bühne nicht.
Eine Warnung vom August 2025, die diese Maschine erst am 8. August 2026 sah, ist kein
Beleg für Foreknowledge durch diesen Apparat. Die Bühne braucht dieselbe epistemische
Disziplin wie das Dossier.

Bemerkenswert: Die Maschine selbst hatte den ungeteilten Overdue-Flag in ihrer ersten
Discovery-Nacht kritisiert; der Split (`cold_start_overdue` / `drift_overdue`) war
seither Code (`futures.py`, `run.json`) — nur ausgesprochen hat ihn die Bühne nicht.

## 2. Die vier öffentlichen Zustände

Abgeleitet an genau einer Stelle (`stage/generate.py::_overdue_state` gegen `run_date`,
nie Wanduhr), überall nur konsumiert:

| Zustand | Bedeutung |
|---|---|
| **source-open** | Der Herausgeber führt die Warnung noch (Status `OPEN`) — der Schirm über allem. |
| **window-open** | Die angekündigte Zukunft ist noch nicht verstrichen. Nur das ist prospektive Beobachtung. |
| **cold start** | Das Fenster lag bei erster Sichtung bereits in der Vergangenheit — Artefakt des Beobachtungsbeginns, Baseline, kein Befund. |
| **drift** | Das Fenster ist **unter Beobachtung dieser Maschine** verstrichen, die Quelle hält die Warnung offen — der Fall, für den der Flag gebaut wurde. |

Was sich ändert:

- **Stage:** Nur window-open zählt als „under watch"; Cold Start und Drift werden als
  eigene Klauseln benannt („a cold start, not foreknowledge"). Null offene Fenster sind
  ein ehrlicher Zustand mit eigenem Satz — Stille ist erlaubt, Aktivität wird nicht
  erfunden. Featured und Grid zeigen nur prospektive Warnungen.
- **Cold-Start-Uhren ticken nicht mehr.** Eine tickende Uhr inszeniert Gegenwart, die
  der Record nicht behauptet; Cold Starts bekommen eine statische Zeile
  („announced window ended … — before observation began").
- **Ledger:** Die eine „Open"-Sektion wird drei — *Inside the announced window* /
  *Outlived under watch — drift* / *Cold start*, jeweils mit Erklärnote.
- **Dossier-Kicker** unterscheidet „window already past at first sight" von
  „outlived its announced window".
- **Export** (`attention-export/1`, additiv): drei neue Figuren
  `futures_window_open` / `futures_cold_start` / `futures_drift`, nach derselben Regel.

Der Cold Start ist kein Müll: Er bleibt preserved, source-open und ist Baseline- und
Quellen-Diagnostik-Material — er steht nur nicht mehr im Zentrum der Bühne.

## 3. Der Momente-Vertrag (`stage-moments/1`)

Der Substrat-Vertrag `stage_moment` aus `2026-08-08-projekt-aufnahme.md` §5 („Projekte
liefern der gemeinsamen Bühne Momente statt Cards; Code bei Bedarf") wird Code —
**mit einer begründeten Abweichung:** §5 erwartete das zweite Projekt als Auslöser;
der reale erste Konsument ist die gemeinsame Bühne der Praxis selbst
(frankbueltge.de/machine-attention wird vom Manifest zur Situation). Der Bedarf ist da,
nur aus der anderen Richtung.

- **Producer:** `practice/foreknown/moments.py` — deterministisch aus dem committeten
  Register. Ein Moment ist ein reales, datiertes Ereignis unter Beobachtung: Revision
  (mit gemessenem Abstand: „A warning changed 13 hours after it was first preserved."),
  Korrektur des eigenen Registers, Closure, Dissipation, Reappearance, Verdict.
  **Keine Momente sind:** der Gründungs-Import der ersten Nacht und jede Notarisierung,
  deren Fenster bei Erstsichtung schon vorbei war — Baseline, nicht Ereignis.
- **Sammler:** `practice/moments.py` → `moments.json` (Repo-Wurzel, neben
  `export.json`), nächtlich im Sentinel. Getrennt vom Export, absichtlich: der
  Export-Vertrag verspricht „nie einzelne Futures, nie Prosa" — Momente referenzieren
  einzelne Futures und tragen einen Satz. Zwei Verträge, zwei Versprechen.
- **Schema je Moment:** `project · occurred_at · mode · statement · subject · enter ·
  evidence`. Kein `valid_until`: Frische entscheidet der Konsument — eine Uhr statt
  zwei, die sich widersprechen.
- **Zulassung:** `PRODUCERS` erweitern ist eine Aufnahme-Entscheidung, kein Refactor.
  **Dark Ocean dockt frühestens nach dem Review vom 2026-08-24 an** (keine
  Bühnen-Präsenz vor bestandenem E-Experiment); das Instrument nie — kein
  Bühnen-Anspruch ist seine Definition.

## 4. Konsument

Site-seitig: `attention-integrate` spiegelt `moments.json` neben dem Export;
`/machine-attention` wird die Bühne der Praxis (Momente statt Manifest), das Manifest
zieht nach `/machine-attention/about` um. Vertrag dort:
`docs/design/2026-08-09-stage-moments-contract.md` im Site-Repo.
