# Planetary Listening — V0, Inkrement 3: der tägliche Workflow (2026-10-16)

**Stufe:** V0, Inkrement 3. Go: 2026-10-04 (Frank, Wortlaut privat). Paarung A
(Rüdersdorf). Vorgänger: `docs/2026-10-15-planetary-listening-v0-inkrement-2.md`.

**Gebaut:** `.github/workflows/planetary.yml` — täglich 06:40 UTC und von Hand
auslösbar: `pip install -e ./practice`, `python -m practice.planetary.nightly --repo-root .`,
`tools/anchor.py --register`, `verify.py`, `tools/commit-and-push.sh` mit
„planetary: reading of <gelesener Tag>". Test:
`practice/tests/test_planetary_workflow.py` — die Schritte in dieser Reihenfolge, und der
Zeitpunkt liegt mindestens 30 Minuten nach dem `Updated` des Herausgebers in **jeder**
committeten Lesung (wird der Herausgeber später, schlägt der Test an, nicht die Nacht).

Der Aufnahme-Pfad lässt einen Workflow erst zu, wenn V0 eine committete Lesung erzeugt hat.
Es sind jetzt zwei, beide mit demselben Befehl, den der Workflow ausführt — die zweite heute,
lokal, aus dem installierten Paket ohne `PYTHONPATH` (`pip install -e` genügt; die
Verdeckung aus Inkrement 1 betrifft nur Läufe ohne Installation).

## Warum 06:40

Das `Updated` der availability-Zeile für den gelesenen Tag war 05:14:43
(`planetary/readings/2026-10-15.json`) und 05:00:57 (`planetary/readings/2026-10-16.json`).
06:40 lässt rund 85 Minuten Abstand und liegt hinter dem Anker-Job (06:20): das Manifest der
Nacht wird als `unstamped` registriert und am nächsten Morgen gestempelt, wie bei
Memory Hole, deren Lauf vom 2026-10-15 erst 09:24 UTC endete (`autonomy/log.jsonl`).
Einen halben Tag früher gestempelt zu sein ist weniger wert als einen vollständigen Tag zu
lesen.

## Die zweite Lesung — `planetary/readings/2026-10-16.json` (Tag 2026-10-15, Donnerstag)

- Tagesdatei: 200, ein Trace, 8 640 730 Samples, Anfrage-SHA-256 `0ff8b5d8…`.
- 8 Trigger, **ein starker Impuls: 07:31:49 UTC, STA/LTA 106,13**, Spitzen-RMS 12 436 gegen
  Hintergrund 93,8, Dauer 8,0 s. Ausschnitt
  `planetary/snapshots/2026-10-16/GE.RUE.HHZ/20261015T073149.mseed` (13 824 B). Er liegt im
  Band der Spike-Woche (07:30:51–07:33:08) und 15 Sekunden nach dem Impuls des Vortags; ein
  sechster Werktag, nicht mehr. Kein Klassenname.
- Herausgeber-Attest: 22 168 Records, 0 Lücken, 0 Überlappungen, 100 % availability,
  Quality D, `sample_rms` 2 369,20.
- **Erste verglichene Neu-Einlagerung:** `compared_with` = Lesung vom 2026-10-15,
  **0 Ereignisse**. Die vier geschlossenen extent-Segmente tragen dieselben `Updated`
  (2022-07-26 zweimal, 2022-07-28, 2022-10-12); nur das offene Segment wuchs bis
  2026-10-16T00:00 (`Updated 2026-10-16T05:00:57Z`). Ein Vergleich zweier Lesungen mit einem
  Tag Abstand, keine Aussage über das Archiv darüber hinaus.
- Kataloge, Box A, derselbe Tag: ISC 204, USGS 200 mit 0 Features.
- Last der Nacht: ≈ 17 KB Snapshots plus Lesung.

## Bewusst nicht

Kein Eintrag in `practice/src/practice/staleness.py` heute — der Registry-Stall-Wächter soll
`planetary/readings` erst führen, wenn der Workflow einmal selbst committet hat; sonst meldet
er eine Lücke, die nur das Warten auf den ersten Lauf ist · keine Akzeptanzkriterien, kein
Fenster (das nächste Inkrement) · kein Backfill (10-12, 10-13) · GR.KAST nicht nächtlich ·
keine Klasse „Sprengung" · kein Lautstärke-Index.

**Nächstes:** nach dem ersten Lauf des Workflows `planetary/readings` in den
Registry-Stall-Wächter; dann die Akzeptanzkriterien als committete Datei, bevor ein Fenster
öffnet.
