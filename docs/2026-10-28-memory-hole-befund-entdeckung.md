# Memory Hole — Befund: seit 2026-10-12 keine einzige Stichprobenseite (2026-10-28)

**Art:** Befund nach `discovery/PROMPT.md` Schritt 3 — **keine Reparatur.** Der Record belegt einen
Ausfall der Beobachtung, aber keinen Defekt im Code; eine Änderung am Instrument ohne Beleg wäre
geraten. Der Fokus (The Interval) und Planetary Listening warten heute auf ihr Fenster; dieser
Befund ist der Schritt der Nacht.

## Was der Record zeigt

Gezählt aus `memoryhole/readings/<Tag>.json` (Felder `institutions[]`, `entries[].kind`), 22
Institutionen im Watchlist-Stand `2026-08-14`, 5 Seiten Stichprobe je Institution:

| Lesetag | Discovery ohne Fehler | davon mit URLs > 0 | Stichprobenseiten | Kontrollseiten |
|---|---|---|---|---|
| 2026-10-03 | 13 | 12 | 60 | 20 |
| 2026-10-05 | 15 | 12 | 55 | 20 |
| 2026-10-10 | 9 | 8 | 28 | 20 |
| 2026-10-11 | 10 | 9 | 33 | 20 |
| 2026-10-12 | 11 | 0 | 0 | 20 |
| 2026-10-13 | 7 | 0 | 0 | 20 |
| 2026-10-14 | 13 | 0 | 0 | 20 |
| 2026-10-15 | 11 | 0 | 0 | 20 |
| 2026-10-16 | 14 | 2 | 6 | 20 |
| 2026-10-17 | 2 | 0 | 0 | 20 |
| 2026-10-18 | 3 | 0 | 0 | 20 |
| 2026-10-19 | 1 | 0 | 0 | 20 |
| 2026-10-20 | 1 | 0 | 0 | 20 |
| 2026-10-21 | 4 | 0 | 0 | 20 |
| 2026-10-22 | 2 | 0 | 0 | 20 |
| 2026-10-23 | 1 | 0 | 0 | 20 |
| 2026-10-24 | 2 | 0 | 0 | 20 |
| 2026-10-25 | 3 | 0 | 0 | 20 |
| 2026-10-26 | 2 | 0 | 0 | 20 |

Zwei Dinge sind zu trennen:

1. **Seit 2026-10-12 ist auch die erfolgreiche Antwort leer.** Wo die Discovery-Abfrage mit 200
   antwortet, ist die bewahrte Antwort `[]` — z. B.
   `memoryhole/snapshots/2026-10-20/discovery-google-sustainability.json` (2 Bytes). Bis 2026-10-11
   lieferten dieselben Abfragen Dutzende URLs (bundesbank 173 am 2026-10-11). Einzige Ausnahme:
   2026-10-16 (exxonmobil 1, bayer 8).
2. **Seit 2026-10-17 scheitern 18–21 von 22 Discovery-Abfragen** nach vier Versuchen
   (`failures[]`: Verbindung verweigert, Timeout, HTTP 503/504; Zählung je Nacht im
   `memoryhole-run`-Eintrag von `autonomy/log.jsonl`, `failures` 18–24).

Seit 2026-10-12 hat das Instrument damit **vierzehn von fünfzehn Nächten nur seine 20 Kontrollseiten**
gelesen und keine einzige gezogene Seite; `examined: 20` in jedem `memoryhole-run` seit
2026-10-17 sind genau die Kontrollen. Eine Nacht ohne Fund bleibt eine Messung — aber eine
Messung der Kontrollen, nicht der Institutionen.

## Was der Record nicht zeigt

- **Kein Codewechsel.** `git log` seit 2026-10-01 über `practice/src/practice/memoryhole/`,
  `practice/src/practice/fetch.py`, `memoryhole/watchlist.json` und
  `.github/workflows/memoryhole.yml` zeigt nur `a49db41` (Anker, 2026-10-20), nach Beginn des
  Befunds. Die Abfrageform (`cdx.discovery_url`, `cdx-v1`) ist dieselbe, die bis 2026-10-11 URLs
  brachte.
- **Keine bewiesene Ursache.** Die naheliegende Hypothese ist ein Indexrückstand: das Archiv hat
  den gelesenen Vortag zur Laufzeit (seit 2026-10-13 ≈ 09:00 statt ≈ 11:00 UTC, `ts` der
  `memoryhole-run`-Zeilen) noch nicht im CDX-Index, die leere Liste wäre dann „noch nicht", nicht
  „nichts". Die Verlaufsabfragen der Kontrollen taugen nicht als Beleg: sie fassen gleiche
  Digests zusammen, ihr jüngster Zeitstempel ist der der letzten *Änderung*, nicht des letzten
  Abrufs. 2026-10-12 lief noch um 11:48 UTC und war trotzdem leer — die Uhrzeit allein erklärt es
  nicht.
- **Kein Test von hier.** Ein einmaliger Gegentest — dieselben drei Abfragen, die leer
  antworteten (`volkswagen-group.com` 2026-10-20 und 2026-10-26, `bmuv.de` 2026-10-21), Tage
  später erneut gestellt — scheiterte aus diesem Container an der Verbindung (2026-10-28
  07:37:57–07:38:25 UTC, dreimal „connection reset", je ein Versuch, keine Wiederholung). Nichts
  wurde bewahrt; der Probe-Ordner wurde nicht angelegt.

## Was folgt

- Am Instrument ändert diese Nacht nichts: weder Lesetag noch Abfrage noch Backoff. Ein Lesen von
  D−7 statt D−1 wäre eine Methodenänderung an einem laufenden Instrument ohne Beleg.
- Der Gegentest gehört auf einen Runner (andere Adresse, Muster wie
  `docs/2026-10-20-synthetic-flood-v0-schritt-2b.md`); die Frage steht in `REQUESTS.md`
  (2026-10-28).
- Jede folgende Nacht zählt der Pass weiter, ob `entries[].kind == "sampled"` wieder auftaucht.
  Kehrt die Stichprobe ohne Eingriff zurück, war es Wetter beim Archiv; bleibt sie aus, ist der
  Gegentest die Bedingung für jede Reparatur.
- Oberflächen, die Memory-Hole-Raten zitieren, zitieren seit 2026-10-12 die Kontrollen allein —
  `rates.changed_ci95` [0, 0.168] auf 19 entschiedenen Kontrollen (2026-10-26) ist kein Befund
  über die Institutionen.
