# The Interval — V0, Inkrement 5: die wöchentliche Lesung (2026-10-13)

**Stufe:** V0, Inkrement 5 von 6 (`docs/2026-10-04-kandidat-the-interval.md` §6). Go: 2026-10-04.
Mit diesem Inkrement hat The Interval Nächte: einen Workflow und seine erste committete Lesung.

**Gebaut:**
- `practice/src/practice/interval/weekly.py` — eine Lesung = ein Record
  `interval/readings/<date>.json`, dazu die Snapshots, die sie ausgelöst hat, und das neu gebaute
  Register. Aufruf: `python -m practice.interval.weekly --repo-root .`
- `.github/workflows/interval.yml` — montags 04:50 UTC (der Platz, den Dark Ocean bis zu seiner
  Stilllegung hatte): Lesung, Anker-Registrierung, verify, Commit über `tools/commit-and-push.sh`.
- `register.py` — die Beginn-Suche als eigene Funktion `read_onsets` (dieselbe Rechnung, jetzt von
  Register und Lesung geteilt); `newest_fts` nimmt optional `before`, damit eine Entscheidung nur
  auf Snapshot-Tagen vor der Lesung beruht.
- `verify.py` — `check_interval_readings`: rechnet für jede Lesung jede Entscheidung (holen oder
  eingefroren) unabhängig aus den Snapshot-Tagen vor ihrem Datum nach, prüft, dass die Abfragen
  genau Episoden × Mengen des genannten IPC-Snapshots sind, und dass jede genannte Seiten-Prüfsumme
  die des Manifests (gesichert) oder der Basis (unverändert) ist.
- Tests: `practice/tests/test_interval_weekly.py` (4, konstruierter Baum, falscher Client, kein
  Netz; darunter: eine gefälschte Entscheidung wird von `verify.py` erkannt).

**Entscheidung: wie die Woche 41 MB nicht neu holt.**
- Eine Abfrage (Episode × Menge) ist **eingefroren**, sobald ein vollständiger Seitensatz von einem
  Snapshot-Tag existiert, dessen Monat mehr als **drei Monate** (`GRACE_MONTHS`) nach dem letzten
  Fenstermonat liegt. Sie wird dann aus diesem Snapshot gelesen und nicht mehr geholt. Die drei
  Monate fangen Nachmeldungen auf der `date`-Achse ab; was FTS danach noch an einer abgeschlossenen
  Episode ändert, verfolgt V0 nicht. Das ist die benannte Grenze, kein stilles Weglassen.
- Jede andere Abfrage wird vollständig geholt. Sind die Seiten-Prüfsummen gleich denen des
  neuesten vollständigen Satzes, heißt das `unchanged`, und nichts wird ein zweites Mal gesichert.
  Ein unvollständiger Satz wird gesichert (`incomplete`), damit der Fehler im Record steht.
- Folge für `as_of`: Bei `unchanged` bleibt das Register beim Snapshot-Tag der Basis. Eine offene
  Uhr zählt bis zu dem Monat, den ein gesicherter Snapshot sehen konnte; die Lesung belegt
  daneben, dass FTS an diesem Tag dieselben Bytes lieferte.
- IPC wird wie bisher nur bei geänderten Bytes gesichert (`sources.snapshot_ipc`).

**Erste Lesung (Record: `interval/readings/2026-10-13.json`).** 29 Anfragen, kein 429.
- IPC: **geändert** gegenüber dem Snapshot vom 2026-10-09, gesichert unter
  `interval/snapshots/2026-10-13/ipc/`. 49 neue Zeilen: Analysen vom März 2026 für Gambia und
  Nigeria. Die Nigeria-Zeilen tragen als Gesamtbevölkerung **0**; sie ergeben keinen Anteil und sind
  für die Beginn-Regel unsichtbar (`warning.py`, Anteil nur bei Bevölkerung > 0). Das ist
  festzuhalten: Ein Land mit fehlender Bevölkerungszahl kann in diesem Instrument keinen Beginn
  haben, solange die Quelle sie nicht nachträgt.
- Episoden: weiter 8, dieselben wie am 2026-10-12. Eingefroren: 12 von 16 Abfragen. Geholt:
  Afghanistan 2025-10 (FSC unverändert; Total 15 Seiten, **3 neue Flüsse**, gesichert, 6 MB) und
  Somalia 2026-01 (FSC und Total unverändert).
- Register: keine Gitterzelle hat sich geändert; nur Afghanistan 2025-10 Total liest jetzt aus dem
  Snapshot vom 2026-10-13 (2 903 statt 2 900 Flüsse, 2 252 gezählt).

**Was wöchentlich anfällt:** solange Afghanistan 2025-10 (eingefroren ab einem Snapshot nach
2026-12) und Somalia 2026-01 (nach 2027-03) offen sind, bis zu rund 10 MB pro Woche, wenn FTS sich
bewegt; nichts, wenn nicht. Neue Beginne aus einer neuen IPC-Tabelle kommen ohne Basis und werden
voll geholt.

**Was das nicht ist:** kein Befund, keine Bühne, kein Treiber. `interval/drivers.json` bleibt bei
acht `unassigned`.

**Nächstes Inkrement (6):** die Abnahmekriterien des E-Experiments als committete Datei, **bevor**
das Fenster aufgeht (mindestens vier wöchentliche Lesungen ohne Lücke). Das Review danach bleibt
beim Maintainer. Ohne Gate parallel: eine Treiber-Quelle innerhalb der Charter.
