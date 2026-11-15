# The Provisional Air — AUDIT, Punkt 1: Vergleichsregel und Vorher-Zeilen, vor dem Abruf festgelegt

**Datum:** 2026-11-15 · **Stufe:** AUDIT (Punkt 1, Vorbereitung; kein Abruf) · **Teil 1:**
`docs/2026-11-13-the-provisional-air-audit.md` §6 · **Teil 2:** `docs/2026-11-14-the-provisional-air-audit-teil-2.md`
· **Vorher-Zeilen:** `provisionalair/point1/2026-11-15-vorher.json`

**Anlass:** Kein früherer Kandidat hat heute einen fälligen Schritt (`discovery/AGENDA.md`): The Interval
schließt sein Fenster heute, die Review-Bitte schreibt der Lauf vom 2026-11-16; Planetary Listening wartet auf
den Review (`REQUESTS.md` 2026-11-04), die Synthetic Flood auf ihren Workflow am 2026-12-04, The Declared
Network und The Afterlife auf `REQUESTS.md` (2026-10-23, 2026-10-30). Ein neues Exposé ist in dieser Woche
schon geöffnet (2026-11-11). Punkt 1 selbst ist an „ab 2026-11-16" gebunden (Teil 1 §6) und wird heute
**nicht** abgerufen. Heute wird festgelegt, *womit* sein Ergebnis verglichen und *wie* es gelesen wird —
bevor die neue Datei da ist, damit die Lesung nicht an ihr ausgerichtet werden kann (dieselbe Ordnung
wie bei der Synthetic Flood, `docs/2026-10-24-synthetic-flood-v0-inkrement-3d.md`).

## 1. Die Vorher-Seite, aus den konservierten Bytes

`provisionalair/point1/2026-11-15-vorher.json` hält je Reihe die Zeilen des Vergleichsfensters, gelesen
aus den hash-gebundenen Dateien (Wegwerf-Umgebung außerhalb des Baums, keine neue Abhängigkeit der Praxis):

| Reihe | Quelle | SHA-256 | Fenster (Stundenbeginn) | Zeilen | davon −999 |
|---|---|---|---|---|---|
| LU0101A PM10 | `provisionalair/probes/2026-11-13/blob/e2a-SPO-LU0101A_00005_103.parquet` | `efc15b4d…bfa9` | 2026-11-12 00:00 – 2026-11-13 07:00 | 32 | 0 |
| DEBE010 PM10 | `provisionalair/probes/2026-11-14/blob/e2a-SPO.DE_DEBE010_PM1_dataGroup1.parquet` | `3ff0b3b1…1e6d` | 2026-11-12 00:00 – 2026-11-14 23:00 | 72 | 17 |

Jede Zeile: `start`, `value` (Dezimalzahl als Text, ohne Rundung), `validity`, `verification`,
`result_time`, `observation_log`. Die Hashes stehen voll in der Datei und gleichen denen der Manifeste.

**Was die Vorher-Zeilen schon zeigen (aus den Bytes gelesen, Mechanismus gefolgert):** In der
luxemburgischen Datei tragen die 32 Stunden vier Lieferzeiten — 11-12 00:00–04:00 `23:25:07` vom 11-12,
05:00 `05:25:07`, 06:00–07:00 `06:25:07`, und **die 24 Stunden 11-12 08:00 bis 11-13 07:00 alle
`08:25:07` vom 11-13**. Die letzte Lieferung hat also genau die vorangehenden 24 Stunden neu
geschrieben; jede frühere Lieferung ist dort zu sehen, wo keine spätere sie überdeckt hat. Gelesen als
Regel: *jede Lieferung ersetzt die letzten 24 Stunden* — dann wird eine luxemburgische Stunde am ersten
Tag bis zu vierundzwanzigmal überschrieben, nicht einmal. Bewiesen ist das nicht (eine Datei, ein
Zeitpunkt); es macht Punkt 1 schärfer, denn der Abruf ab 2026-11-16 sieht nur die letzte dieser Fassungen.
Die deutsche Datei zeigt dagegen den Tagestakt aus Teil 2 (11-12 alle `11-13 23:45:40`, 11-13 und 11-14
alle `11-14 07:45:45`).

## 2. Der Abruf (ab 2026-11-16, nicht heute)

Dieselben zwei Adressen wie in den Manifesten, je **ein** Versuch, keine Wiederholung, Standardbibliothek,
Kennung `machine-attention/0.1`, das Anfragefeld `email` nie gesetzt; konserviert unter
`provisionalair/probes/<Datum>/blob/` mit Manifest. Frühestens nach der deutschen Lieferung des
2026-11-15 (`23:45` UTC+1, gefolgert = 22:45 UTC), also im Lauf vom 2026-11-16 oder später. Scheitert ein
Abruf (kein 200), bleibt Punkt 1 für diese Reihe offen, ein Versuch an einem späteren Abend.

## 3. Regel `compare-v1` — je Stunde des Fensters

Verglichen wird je Reihe die Vorher-Zeile *b* mit der Nachher-Zeile *a* gleichen `start`. Werte werden als
Dezimalzahl exakt verglichen (keine Toleranz, keine Rundung); −999 ist nie ein Wert.

| Klasse | Bedingung (in dieser Reihenfolge) |
|---|---|
| `missing_after` | keine Zeile *a* |
| `filled` | *b* −999, *a* nicht −999 |
| `withdrawn` | *b* nicht −999, *a* −999 |
| `changed` | beide nicht −999, Wert verschieden — berichtet mit *a* − *b* und ob sich der auf ganze µg/m³ gerundete Wert ändert (die UBA-Kopie, Teil 2 Punkt 3) |
| `flag_changed` | Wert gleich, `validity` oder `verification` verschieden |
| `redelivered` | Wert, `validity`, `verification` gleich, `result_time` später |
| `same` | alles gleich, auch `result_time` |

Dazu je Kalendertag (Stundenbeschriftung) das Mittel der Stunden mit Wert ≠ −999 und `validity` > 0, vorher
und nachher, und die Zahl dieser Stunden. **Keine Schwelle wird angewandt** — die Werte liegen bei 5–24 µg/m³,
und ein Audit zählt keine Überschreitungen; die Bindung an Richtlinie (EU) 2024/2881 (Teil 1 §3) bleibt V0.

## 4. Lesung, festgelegt vor dem Abruf

| Ergebnis (über beide Reihen) | Bedeutung | Folge |
|---|---|---|
| mindestens ein `changed` oder `withdrawn` | ein gezeigter vorläufiger Wert hat die Neulieferung nicht überlebt | Empfehlung **endgültig GO für ein enges V0** (Teil 2), Bitte in `REQUESTS.md` |
| kein `changed`/`withdrawn`, mindestens ein `redelivered` oder `flag_changed` | die frühen Neulieferungen ersetzen die Lieferzeit, nicht den Wert — für diese Stunden | Empfehlung **GO, enger**: das Tageslicht liegt dann im Sprung zur Validierung (E1a) und in den Monats-/Quartalsneulieferungen, nicht in den ersten Tagen; das wird in der Bitte gesagt |
| nur `same` und `filled` | keine Neulieferung der Vorher-Stunden beobachtet — widerspräche für DEBE010 dem Tagestakt aus Teil 2 | berichtet, keine Empfehlung daraus; ein weiterer Abruf frühestens eine Woche später |
| `missing_after` | Zeilen verschwunden | eigener Befund, berichtet; zählt nicht als Wertänderung, bis geklärt |

Ein Ergebnis aus zwei Reihen und einem Zeitpunkt beweist keinen Anteil; es entscheidet nur, *welche*
Empfehlung geschrieben wird. Für Luxemburg kann der Abruf die Zwischenfassungen des ersten Tages (§1) nicht
sehen — nur die letzte gegen die vom 2026-11-13 07:39 UTC.

## Bewusst nicht heute

Kein Abruf, keine Statusabfrage, kein Code unter `practice/`, kein Stationssatz, keine Schwelle. Die Regel
oben ändert sich nach dem Abruf nicht; eine Änderung wäre eine neue Version mit Datum. Das GO für V0 bleibt
dem Maintainer.
