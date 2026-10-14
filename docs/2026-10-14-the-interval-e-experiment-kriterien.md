# The Interval — E-Experiment: Abnahmekriterien (2026-10-14)

**Stufe:** V0, Inkrement 6 von 6 (`docs/2026-10-04-kandidat-the-interval.md` §6) — die
Kriterien des E-Experiments, committet **bevor** das Fenster aufgeht. Go für V0: 2026-10-04.
**Maschinenlesbar:** `interval/experiment.json` (trägt die Prüfsumme dieses Dokuments;
`verify.py`, `check_interval_experiment`, scheitert, wenn beide auseinanderlaufen).
**Zählung:** `python -m practice.interval.experiment --repo-root .`
(`practice/src/practice/interval/experiment.py`). **Vorbild:** die Kriterien von Memory Hole
(`docs/2026-08-22-memory-hole-e-experiment-kriterien.md`), deren §0 vorführt, was passiert, wenn
Kriterien nach der ersten Nacht kommen. Hier kommen sie davor.

## 0. Bindung

Dieses Dokument bindet mit seinem Commit. Änderungen sind bis zum Tag vor der ersten
Fensterwoche erlaubt (datierter Nachtrag mit Begründung, `experiment.json` und seine
Prüfsumme im selben Commit), danach nicht mehr. Die eine Lesung vor dem Fenster
(`interval/readings/2026-10-13.json`) ist **Vor-Fenster-Kontext**: Sie zählt nicht als
E-Evidenz, dient aber als Ausgangspunkt für B1 und B2.

## 1. Das Fenster

**Vier ISO-Wochen ohne Lücke**, die Mindestlänge aus dem Kandidatendokument §6:

| Woche | Montag (Workflow 04:50 UTC) |
|---|---|
| 1 | 2026-10-19 |
| 2 | 2026-10-26 |
| 3 | 2026-11-02 |
| 4 | 2026-11-09 |

Das Fenster schließt am **2026-11-15**; das Review ist ab dem **2026-11-16** möglich und gehört
dem Maintainer. Eine Woche zählt, wenn in ihr eine Lesung `interval/readings/<date>.json`
committet ist (ein Nachlauf per `workflow_dispatch` innerhalb derselben Woche zählt; die erste
Lesung der Woche ist die zählende) und `verify.py` auf ihr grün ist.

Warum vier und nicht mehr: Die Daten sind monatlich (IPC) und bei abgeschlossenen Episoden
eingefroren (FTS, `docs/2026-10-13-the-interval-v0-inkrement-5.md`). Vier Wochen decken einen
IPC-Monat; was das Instrument über länger sagt, ist die Frage des Reviews, nicht des Fensters.

## 2. Abnahmekriterien

### A — Betrieb (aus den Lesungen gezählt)

| # | Kriterium | Latte |
|---|---|---|
| A1 | committete Lesung in jeder der vier Wochen | **4 von 4**, keine Lücke |
| A2 | Lesungen, in denen IPC `unavailable` ist oder eine geholte Abfrage `unavailable` oder `incomplete` endet | **höchstens 1**, die Ursache im Record benannt |
| A3 | HTTP 429 (HDX oder FTS) in einer Lesung des Fensters | **0** — das Instrument holt höflich oder gar nicht |
| A4 | `verify.py` grün auf jeder Fensterlesung, das Register aus den Snapshots nachgerechnet | ohne Ausnahme (CI-Gate) |
| A5 | keine einzige Anfrage an das FEWS-NET-Data-Warehouse | 0 (Kandidatendokument §2; ein Test hält den Quelltext daran) |

### B — Messung

| # | Kriterium | Latte |
|---|---|---|
| B1 | **Eingefroren bleibt eingefroren.** Eine Abfrage, die in einer Lesung (die Vor-Fenster-Lesung eingeschlossen) `frozen` war, ist in jeder späteren `frozen`, auf demselben Basis-Tag | **0 Verstöße.** Ein Verstoß heißt: Abgeschlossene Episoden bewegen sich, und das Gitter misst die Pipeline |
| B2 | **Episoden-Wechsel** zwischen den Lesungen (neue Beginne, verschwundene Beginne durch IPC-Revision) | berichtet, jede Änderung mit der IPC-Zeile, die sie trägt |
| B3 | **Gitter vollständig.** Jede Episode des Registers trägt alle Zellen θ × k × Zeitachse × FSC/Total, oder ihre Lücke ist als Status benannt (`incomplete`, offen) | 0 stumme Lücken |
| B4 | **Offene Uhren** zählen gegen den Snapshot, nie gegen die Wanduhr: ändert sich eine offene Zelle zwischen zwei Lesungen, dann nur mit einem neuen Snapshot | berichtet; ein Sprung ohne neuen Snapshot ist ein Verstoß |
| B5 | **Treiber-Vermerke** mit Quelle innerhalb der Charter | berichtet, **keine Latte** — heute stehen alle acht auf `unassigned` (`interval/drivers.json`) |

### C — Ethik und Charter (Ausschluss, keine Punkte)

Keine natürliche Person in einem Record (I8). Keine Schuldzuweisung (E-2): Die Lücke t1 − t0
wird gemessen und mit ihrem Gitter gezeigt, nie einem Geber, einer Agentur oder einer Regierung
als Versäumnis zugeschrieben. Nur öffentliche, schlüsselfreie Quellen. Bis zum Review keine
Bühne: The Interval steht auf der Site nirgends.

**Bestanden = A1–A5 erfüllt · B1, B3, B4 ohne Verstoß · B2, B5 berichtet · C ohne Verstoß.**

## 3. Was das Fenster voraussichtlich zeigt — vorab notiert

Aus der Vor-Fenster-Lesung vom 2026-10-13: 8 Episoden, 16 Abfragen, davon 12 eingefroren. Offen
sind Afghanistan 2025-10 (eingefroren ab einem Snapshot nach 2026-12) und Somalia 2026-01 (nach
2027-03). Erwartung: Das Fenster friert nichts Neues ein, holt jede Woche vier Abfragen, und
B1 läuft auf zwölf eingefrorenen Abfragen leer, wenn die Pipeline hält. Das ist der Sinn von
B1: Ein Instrument, dessen abgeschlossene Episoden still bleiben, misst die Welt und nicht sich.

Eine Änderung der IPC-Tabelle ist im Fenster wahrscheinlich (zuletzt am 2026-10-13: Gambia und
Nigeria, März 2026). Ein neuer Beginn kommt ohne Basis und wird voll geholt; das ist B2s Fall
und kein Fehler.

## 4. Bekannte Konfundierer — vor Fensterstart benannt

1. **Bevölkerung 0.** Die Nigeria-Zeilen vom März 2026 tragen als Gesamtbevölkerung 0 und
   ergeben keinen Anteil (`warning.py`); ein solches Land kann keinen Beginn haben, solange die
   Quelle nicht nachträgt. Ein Nachtrag erscheint in B2 als neuer Beginn, nicht als Krise.
2. **Nachmeldungen bei FTS.** Die drei Monate Karenz (`GRACE_MONTHS`) fangen sie auf der
   `date`-Achse ab; was danach an einer abgeschlossenen Episode geändert wird, verfolgt V0
   nicht. Benannte Grenze.
3. **FSC-Kennzeichnung** trägt erst ab etwa 2020 (Kandidatendokument §2); das Ländertotal ist
   die Gegenprobe und kein Ersatz.
4. **HDX-`robots.txt`** sperrt `*.csv` für Crawler; V0 holt eine Datei pro Woche, mit ETag und
   ehrlichem User-Agent. A3 hält das.
5. **Treiber fehlen.** Ohne Treiber ist das Register eine Lückenmessung ohne Erklärung. Das
   Fenster prüft das Instrument, nicht die Erklärung.

## 5. Drei mögliche Ausgänge (die Entscheidung ist des Maintainers)

- **RUNNING · Instrument** — A und B ohne Verstoß: wöchentliche Lesung bleibt, Register wird
  fortgeschrieben; eine Bühne ist eine eigene Entscheidung.
- **Verlängert** — A2 oder B4 knapp verletzt mit benannter, behobener Ursache: ein neues Fenster,
  mit neuen, vorher committeten Kriterien.
- **RETIRED** — B1 oder C verletzt, oder A1 gerissen ohne benannte Ursache.
