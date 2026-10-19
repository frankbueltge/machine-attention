# The Synthetic Flood — V0, Inkrement 1: die Wortliste und die erste Kohorte (2026-10-19)

**Stufe:** V0, Inkrement 1 · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), die
Bedingung erfüllt laut `docs/2026-10-18-synthetic-flood-audit.md`; die Lesart steht seit
2026-10-18 in `REQUESTS.md` und blieb über den nächsten Pass unbeantwortet, also gilt die
stehende Regel (`REQUESTS.md`, Kopf). · **Anlass:** Der Fokus wartet — The Interval hat die
Lesung der ersten Fensterwoche (`interval/readings/2026-10-19.json`, Tally A1 ohne Lücke),
Planetary Listening hat seine Kriterien seit dem Morgen (`planetary/experiment.json`).

## Gebaut

- **Die Wortliste als unveränderliche Versionsdatei:** `syntheticflood/wordlists/wordlist-v1.json` —
  47 Wörter `fixed` (die committete Liste, jeden Monat unverändert gezählt), 20 `controls`
  (stabile Inhaltswörter, die Negativkontrolle), 99 `pool` (der Kandidatenpool, aus dem die
  monatlich neu abgeleitete Liste gezogen wird; Audit Befund 2, Weg a). Exakte PubMed-`[tiab]`-
  Terme, nur Kleinbuchstaben a–z, die drei Listen disjunkt. Eine geänderte Liste ist eine neue
  Datei; diese ändert sich nie (der Verifikator hält ihren SHA-256 gegen jede Lesung).
  **Ehrlich:** die Auswahl ist die des Passes, angelehnt an die Stilwörter des Nachbarn
  (arXiv:2406.07016), nicht aus dessen Tabellen kopiert und noch **nicht** gegen die Basis
  2018–2022 geprüft. Diese Prüfung ist ein späteres Inkrement und darf Wörter streichen — als
  `wordlist-v2`, nie durch Überschreiben.
- **Der Leser:** `practice/src/practice/syntheticflood/` — `pubmed.py` (die deterministische
  `esearch`-Zählanfrage, byte-gleich mit den Probe-URLs des Audits; die kanonische Antwortform),
  `wordlist.py` (Laden und Prüfen), `cohort.py` (eine Kohorte, jedes Wort, nur Zahlen). Aufruf:
  `python -m practice.syntheticflood.cohort --repo-root . --cohort 2026-09`.
- **Keine Bytes, trotzdem prüfbar:** Alle sieben Zählantworten der Audit-Probe sind byte-gleich
  mit `{"header":{"type":"esearch","version":"0.3"},"esearchresult":{"count":"N"}}` plus
  Zeilenende (`practice/tests/test_syntheticflood.py::test_probe_answers_are_canonical`). Die Lesung
  speichert daher Anfrage, Zahl und SHA-256 der empfangenen Bytes; `verify.py` baut die Bytes aus
  der Zahl nach und prüft den Hash. Eine Antwort in anderer Form wird als Bytes mit Manifest unter
  `syntheticflood/snapshots/` bewahrt — der Leser entscheidet das je Antwort.
- **`verify.py` → `check_syntheticflood`** (und `check_snapshots` für `syntheticflood/snapshots`):
  Pfad = Kohorte/Lesedatum; Abstand in Monaten, `value` nur bei M+3, `retrospective` ab M+4;
  nur der auditierte Host; die Wortliste unverändert; jedes Wort in Reihenfolge gezählt; jede
  Anfrage neu gebaut und verglichen; jede Zahl an ihren Hash gebunden; kein Feld außerhalb der
  Zählfelder (ein Feld wie `abstract` fällt durch). Jede Regel hat einen Test, der sie bricht
  (`practice/tests/test_syntheticflood.py`, 16 Tests, ohne Netz).

## Die erste Lesung

`syntheticflood/readings/2026-09/2026-10-19.json` — Kohorte 2026-09 bei M+1, 167 Anfragen
(18:13:53–18:17:12 UTC), 0 × 429, 0 fehlend, keine Bytes bewahrt (alle Antworten kanonisch).

| | Zahl | Anteil an der Kohorte |
|---|---|---|
| Kohorte (`hasabstract`, 2026/09[dp]) | 165 555 | |
| `delve` | 27 | 0,016 % |
| `intricate` | 420 | 0,254 % |
| `meticulous` | 210 | 0,127 % |
| `pivotal` | 1 893 | 1,143 % |
| `underscores` | 1 915 | 1,157 % |
| Kontrolle `patients` | 44 539 | 26,903 % |

**Schon eine Revision, noch kein Befund:** dieselbe Kohortenanfrage zählte im Audit am
2026-10-18 165 058 Abstracts (`syntheticflood/probes/2026-10-18/manifest.json`, `cohort-2026-09`),
heute 165 555 — +497 an einem Tag. Genau deshalb zählt erst M+3 als Wert (Exposé §3). `delve`
steht bei 27 wie im Audit. Ohne Basis 2018–2022 ist keine dieser Zahlen ein Überschuss; die
Tabelle ist eine Machbarkeit, keine Aussage.

## Nächste Inkremente

2. Register B: eine tägliche `allcategories`-Anfrage mit Kontakt-User-Agent (nur Größen der
   datierten Unterkategorien), Leser und Verifikator.
3. Die Basis: dieselbe Wortliste über die Kohorten 2018–2022 (rückwirkend markiert), die
   Prüfung jedes `fixed`-Worts auf Stabilität, die Regel für die abgeleitete Liste.
4. Ein Workflow erst danach — monatlich die Kohorten M−1, M−2, M−3.

## Bewusst nicht

Kein Abstract, kein Titel, kein Name angefragt oder gespeichert; keine E-Mail-Adresse an NCBI;
OpenAlex, Crossref und Wikipedia heute nicht berührt; kein Workflow; keine Aussage über Anteile
maschinell geschriebener Sprache.

## Reparatur am Rand (Planetary Listening)

`practice/tests/test_planetary_workflow.py::test_schedule_follows_every_observed_publisher_update`
war auf `main` rot: die Lesung `planetary/readings/2026-10-19.json` trägt `Updated
2026-10-19T06:22:02Z`, der Slot 06:40 UTC lag damit innerhalb der 30-Minuten-Marge. Der Slot in
`.github/workflows/planetary.yml` steht jetzt auf 08:10 UTC — vor dem Fenster (erste Lesung
2026-10-21), und die Kriterien zählen das Datum einer Lesung, nicht ihre Uhrzeit
(`docs/2026-10-19-planetary-listening-e-experiment-kriterien.md` §4, Punkt 2). Der Detektor
und `nightly.py` sind unberührt (B6).
