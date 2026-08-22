# The Foreknown — E1: Review

**Datum:** 2026-08-22 · **Grundlage:** E1-Kriterien in
`2026-08-08-foreknown-001-audit-und-entwurf.md` §„E1 — erstes E2E-Experiment (14 Nächte)"
**Ausgang: NICHT BESTANDEN — zwei von vier Kriterien offen.** Beide Lücken sind gebaut,
nicht gemessen worden: eine dritte Quelle fehlt, und die Reaktions-Achse ist nie in einen
Auflösungs-Record eingeflossen. Das Projekt läuft weiter; E1 wird unter geschlossenen
Kriterien wiederholt (§6).

## 1. Nachgerechnet aus den committeten Records

| # | Verlangt | Nachgerechnet | Urteil |
|---|---|---|---|
| E1.1 | ≥ 20 beurkundete announced_futures aus **≥ 3 Quellen**, je mit Bytes + Hash + Abrufzeit | **112 Zukünfte** — aber aus **2 Quellen**: GDACS (108), NHC current-storms (4). Bytes/Hash/Abrufzeit vollständig, je Nacht im Manifest | **nicht erfüllt** (Menge weit über der Latte, Quellenzahl darunter) |
| E1.2 | ≥ 1 vollständiger Zyklus Warnung → Auflösung **mit Geld- und Aufmerksamkeits-Zeitreihe** | 15 Auflösungen, davon 13 mit `cold_start: true`. **Kein einziger Auflösungs-Record trägt Geld oder Aufmerksamkeit** — obwohl beides seit 13 Nächten je Zukunft vorliegt (FTS-Plan-Bedarf/-Finanzierung, GDELT-Artikel gegen 28-Tage-Baseline) | **nicht erfüllt** — Datenlücke null, Join-Lücke total |
| E1.3 | Bühne live mit echten Countdowns; Provenienz-Verifikator grün; Autonomie-Trace vollständig inkl. Discovery-Kosten | Bühne live und nächtlich neu gebaut, byte-stabil; `verify.py` grün auf jeder Nacht; 75 Trace-Einträge, Kosten je Schritt, 17 Discovery-Pässe | **erfüllt** |
| E1.4 | Ehrlichkeits-Kriterium: ≥ 1 NOT_ARRIVED oder REVISED sichtbar publiziert | Publiziert ist mehr als das Minimum: **0 von 15 Auflösungen materialisiert** (`MATERIALIZED_AS_ALERT` = 0), 13× `EPISODE_ENDED`, 2× `NO_ALERT_MATCH`; 29 Zukünfte mit revidierter Historie, eine mit 13 Revisionen; die epistemische Aufteilung des Registers (93 cold start, 3 offenes Fenster, 1 Drift) steht auf der Bühne | **erfüllt** |

## 2. Betrieb, den die Kriterien nicht abgefragt haben

13 Nächte auf dem Record (08-08 … 08-22); **08-10 und 08-11 fehlen**, verloren an
denselben Anchor-Deadlock, der Dark Ocean zwei Nächte gekostet hat — Ursache im Log,
kein Backfill. 0,00 € über alle Läufe. 21 datierte Selbstbeobachtungen der Maschine
(`foreknown/proposals/obs-*`), 9 Sensor-Vorschläge, einer davon heute selbst befördert.

## 3. Der eigentliche Befund: das Register ist zu 96 % ein Archiv, kein Wachdienst

Von 97 quelloffenen Zukünften stehen **93 im cold start** — sie waren schon angekündigt,
bevor die Maschine hinsah. Wirklich unter Beobachtung entstanden sind **4** (3 offene
Fenster, 1 Drift). Von 15 Auflösungen betrafen **2** eine Zukunft, die von der Ankündigung
an beobachtet wurde.

Das ist keine Schwäche der Messung, sondern ihr ehrlichster Satz — und die Bühne sagt ihn
seit dem 2026-08-09 selbst. Aber es erklärt, warum 14 Nächte sich nach außen wie Stillstand
anfühlen: Die Maschine hat vor allem einen Bestand beurkundet und dann gewartet. Ein
14-Nächte-Fenster ist für Katastrophen-Ankündigungen mit Wochen- bis Monatshorizont zu
kurz, um viele Zyklen zu schließen; das nächste Fenster muss deshalb nicht länger sein,
sondern **die Zyklen zählen, die es tatsächlich schließen kann** (§6).

## 4. Zwei Lücken, ein Befund über uns

Beide offenen Kriterien sind **Bau**-Lücken, keine Erkenntnis-Lücken:

- **Dritte Quelle:** GDACS und NHC waren am 08.08. live geprüft; eine dritte wurde
  vertagt (ReliefWeb bis zur Registrierungsfrage, GloFAS/IPC als Phase 2) und danach
  nie wieder aufgenommen. Es fehlte kein Zugang, es fehlte eine Session.
- **Reaktions-Join:** `foreknown/reaction/readings/*.json` trägt seit 13 Nächten je
  Zukunft `money` (FTS-Plan, Bedarf/Finanzierung, USD) und `attention` (GDELT-Artikel,
  Baseline-Median, Ratio) — 112 Aufmerksamkeits-Tage bis zurück zum 2026-06-09. Der
  Auflösungs-Record kennt das nicht: er misst `episode_days`, `revisions`, `severity_path`.
  Die Zeitreihe, die E1 verlangt, liegt vollständig auf der Platte und ist nie an die
  Auflösung gehängt worden.

Nebenbefund, der öffentlich werden sollte: von 95 laufenden Alarm-Episoden haben nur
**42 überhaupt einen Finanzierungsplan-Treffer** (Match-Rate 0,44). Das ist eine
Gegenmessungs-Zahl, nicht eine Betriebszahl.

## 5. Eine Asymmetrie, die benannt gehört

Der Aufnahme-Pfad verlangt: keine Bühnen-Präsenz vor bestandenem E-Experiment. The
Foreknown hat seit dem 08.08. eine öffentliche Route (`/attention`), ohne bestandenes E1 —
Dark Ocean hat 14 Nächte lang keine bekommen. Der Grund ist historisch: die Regel wurde am
2026-08-09 für Kandidaten *nach* Projekt 001 formuliert, während Bühne und Projekt 001
zusammen entstanden sind. Das ist eine datierte Bestandsausnahme, keine Gleichbehandlung.
Sie wird hier festgehalten, damit sie nicht als Regel missverstanden wird; ein drittes
Projekt kann sich nicht darauf berufen.

## 6. Was jetzt gilt

1. **The Foreknown bleibt `running`.** Nicht weil E1 bestanden wäre, sondern weil E1.3 und
   E1.4 tragen und die zwei offenen Kriterien nichts über den Gegenstand aussagen, nur über
   unsere Bauliste.
2. **E1 wird wiederholt — mit geschlossenen Kriterien vor Fensterstart**, nach dem Muster,
   das Dark Ocean erzwungen hat (`2026-08-09-…-e-experiment-kriterien.md` §0). Die Lehre
   dieses Reviews wandert direkt hinein: **kein Kriterium, das eine noch nicht gebaute
   Quelle oder einen noch nicht gebauten Join voraussetzt.** Erst bauen, dann Fenster
   öffnen.
3. **Reihenfolge, verbindlich:** (a) dritte Quelle live geprüft, gebaut, verifiziert;
   (b) Auflösungs-Record trägt Geld- und Aufmerksamkeits-Zeitreihe aus committeten
   Snapshots, deterministisch, ohne frischen Abruf; (c) danach Kriterien committen; (d)
   dann Fenster.
4. **Das nächste Fenster zählt geschlossene Zyklen, nicht Nächte.** Vorschlag für die
   Kriterien: ≥ 3 Auflösungen von Zukünften, die **unter Beobachtung** angekündigt wurden
   (cold_start = false), jede mit Geld- und Aufmerksamkeits-Zeitreihe — statt „14 Nächte
   und mindestens einer". Der Kalender ist dann Nebensache; entscheidend ist, dass die
   Maschine einen Zyklus wirklich von vorn bis hinten gesehen hat.
