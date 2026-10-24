# The Synthetic Flood — V0, Inkrement 3d: die Revisionsregel, vor der zweiten Lesung festgelegt (2026-10-24)

**Stufe:** V0, Inkrement 3d · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), wie in
`docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`. · **Anlass:** Der Fokus wartet — The Interval
liest erst Montag 2026-10-26 (Samstag, nichts fällig); Planetary Listening läuft im Fenster, die Nacht
2026-10-24 ist zur Passzeit (06:37 UTC) noch nicht fällig (Slot 08:10 UTC); The Declared Network wartet
auf `REQUESTS.md` (2026-10-23). `memoryhole/readings/2026-10-22.json` trägt 0 Enthaltungen — kein
Urteil fällig. Eine neue Exposé ist diese Woche schon geöffnet (The Declared Network, 2026-10-23).

## Warum jetzt

Die erste abgeleitete Liste von 2026-09 ist `control_breach`
(`syntheticflood/derived/2026-09/2026-10-22.json`: `reduced` beobachtet 13,78 %, erwartet 7,54 %,
Verhältnis 1,8272). Inkrement 3c nennt drei mögliche Ursachen, keine bewiesen: die Mischung der Kohorte
bei M+1, eine Änderung der Suche, oder Gebrauch
(`docs/2026-10-22-synthetic-flood-v0-inkrement-3c.md`). Der nächste Schritt ist die zweite Lesung bei
M+2 ab 2026-11-01. Damit sie nicht nachträglich gedeutet wird, steht **heute**, vor ihr, fest, wie sie
mit der ersten verglichen wird und was jedes Ergebnis bedeutet.

## Gebaut

- **Regel `revision-v1`** — `practice/src/practice/syntheticflood/revision.py` (rein in `compare`,
  holt nichts): für jedes Wort, das in beiden Lesungen einer Kohorte steht,
  `drift = (später / Gesamt später) / (früher / Gesamt früher)`, vier Stellen; unter 50 Abstracts in
  der früheren Lesung `thin` (berichtet, nicht beurteilt); außerhalb [1/1,1, 1,1] `moved`, sonst
  `held`. Datei `syntheticflood/revisions/<kohorte>/<früher>_<später>.json`, beide Lesungen mit
  SHA-256, Abstand in Monaten und Wortliste genannt.
- **`verify.py` → `check_syntheticflood_revisions`** rechnet jeden Drift, die Gesamtzahlen und die
  `moved`-Liste unabhängig aus den genannten Lesungen nach und hält die Parameter unter ihrer ID fest.
- **Tests:** `practice/tests/test_syntheticflood_revision.py` (6, ohne Netz; jede Prüfung mit einem
  Test, der sie bricht: geänderter Drift, Regel unter ihrer ID geändert, Lesung nach der Revision
  geändert, falsche Reihenfolge, Basisjahr).

## Die erste Revision: 2026-09, gelesen am 2026-10-19 und am 2026-10-22

`syntheticflood/revisions/2026-09/2026-10-19_2026-10-22.json` — beide Lesungen bei M+1, drei Tage
auseinander, `wordlist-v1` gegen `wordlist-v2` (165 gemeinsame Wörter). Gesamt 165 555 → 165 995
(+0,27 %). 137 Wörter beurteilt, **alle `held`**, Drift 0,9844 (`showcase`) bis 1,0336
(`noteworthy`); 28 `thin`. Kein Fetch heute.

**Grenze:** `reduced` steht nur in `wordlist-v2` — diese Revision sagt über das Bruchwort nichts. Sie
zeigt nur, dass drei Tage Nachindexierung bei M+1 die Anteile der übrigen Wörter um höchstens 3,4 %
bewegt haben.

## Vorab festgelegt: wie die Lesung bei M+2 gelesen wird

Ab 2026-11-01: Kohorte 2026-09 auf `wordlist-v2` lesen (≈ 168 Anfragen), daraus die abgeleitete Liste
(`excess-v1`, unverändert) und die Revision `2026-10-22_<M+2-Datum>` (`revision-v1`). Die Erwartung
von `reduced` hängt nur an der Basis und bleibt 7,54 %; der Bruch fällt deshalb **nur**, wenn sein
Drift unter 1,5 / 1,8272 = **0,8209** liegt — also nur, wenn `reduced` `moved` ist. Ein `held`
`reduced` mit gefallenem Bruch ist arithmetisch ausgeschlossen.

| `reduced` bei M+2 | Bruch | Lesart, festgelegt vor der Lesung | Was folgt |
|---|---|---|---|
| Drift ≤ 0,8209 | fällt | Der Bruch von M+1 war Mischung der Kohorte. | Die M+2-Liste gilt, wenn keine andere Kontrolle bricht; Workflow (Inkrement 4) nach der Agenda-Regel. Künftig wird erst ab M+2 abgeleitet — als neue Regel, nicht als Änderung von `excess-v1`. |
| Drift `held` | hält | Mischung bei M+1 ist für `reduced` ausgeschlossen. Eine Suchänderung seit der Basis ist schon jetzt unwahrscheinlich: Basis und Kohorte wurden am selben Tag gelesen (2026-10-22). Offen bleibt Gebrauch — oder ein Unterschied, der nur junge Datensätze trifft. | Vorschlag, nicht Schritt: `reduced` in den Jahreskohorten 2023–2025 lesen (6 Anfragen), um einen stetigen Anstieg von einer Stufe zu unterscheiden. Keine `wordlist-v3` vor diesem Befund. |
| Drift `moved`, > 0,8209 | hält | Die Kohorte revidiert noch, der Bruch steht trotzdem. Keine Ursache entschieden. | Lesung bei M+3 (ab 2026-12-01), dieselbe Regel. |

Bricht bei M+2 eine weitere Kontrolle, wird sie berichtet und nach derselben Tabelle gelesen. Ein Wort
mit Drift ist eine Zählung, kein Text und kein Anteil maschinell geschriebener Sprache.

## Bewusst nicht

Keine Anfrage an PubMed heute (die Revision rechnet aus committeten Lesungen); keine Änderung an
`excess-v1`, `wordlist-v2` oder einer Lesung; Register B bleibt zu (`REQUESTS.md` 2026-10-20 offen);
kein Workflow.
