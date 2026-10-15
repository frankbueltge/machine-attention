# Planetary Listening — V0, Inkrement 2: die nächtliche T+1-Lesung für GE.RUE (2026-10-15)

**Stufe:** V0, Inkrement 2. Go: 2026-10-04 (Frank, Wortlaut privat). Paarung A
(Rüdersdorf), entschieden vom Spike (`docs/2026-10-14-planetary-listening-v0-inkrement-1.md`).

**Gebaut:** `practice/src/practice/planetary/nightly.py` — liest je Nacht den
**vorigen UTC-Tag** von GE.RUE..HHZ nach dem Speichermodell des Audits (Auflage 2):
Tagesdatei holen, hashen, verwerfen (`committed: false` im Ledger); höchstens vier
record-aligned Ausschnitte starker Impulse (STA/LTA ≥ 50), byteidentische Teilmenge der
Herausgeberbytes. Daneben werden **drei kleine Herausgeberdokumente wörtlich
konserviert** (Audit Befund 2: der Herausgeber beurkundet nichts, aber er datiert seine
Umschreibungen):

| Dokument | Endpunkt | Größe heute |
|---|---|---|
| availability, `show=latestupdate`, gelesener Tag | `geofon.gfz.de/fdsnws/availability/1/query` | 260 B |
| extent, ganze Kanalgeschichte mit `Updated` | `geofon.gfz.de/fdsnws/availability/1/extent` | 912 B |
| WFCatalog-Tagesdokument, `include=sample` | `geofon.gfz.de/eidaws/wfcatalog/1/query` | 702 B |

Kataloge (ISC, USGS) für denselben Tag und dieselbe Box wie im Spike. Tests:
`practice/tests/test_planetary_nightly.py` (ohne Netz; Ausfall wird als Ausfall
geschrieben, nichts erfunden). `verify.py` (`check_planetary_readings`) hält die neuen
Records: Lesung genau einen Tag hinter ihrem Datum, nur auditierte Hosts mit SHA-256,
Netz-DOI, jeder Ausschnitt und jedes Herausgeberdokument manifestiert, die extent- und
availability-Zeilen der Lesung gleich der Neu-Lesung der committeten Bytes, und die
Neu-Einlagerungs-Ereignisse **unabhängig nachgerechnet** (der Verifikator vertraut dem Code
nicht, den er prüft). Die Snapshots liegen unter `planetary/snapshots/<date>/` und sind
damit im Glob des Ankers; der Ledger führt die Nacht als `unstamped`, der Anker-Job
stempelt sie.

## Neu-Einlagerung als Ereignis — die Regel

Ein Segment der extent-Tabelle, das in der vorigen Lesung **schon geschlossen** war und jetzt
ein anderes `Updated` oder `Latest` trägt, ist `segment_rewritten`; verschwindet es,
`segment_gone`; taucht ein Segment auf, das **vor** dem offenen Segment beginnt,
`segment_inserted`. Das offene Segment (das bis zum gelesenen Tag reicht) wächst jede Nacht
durch Anhängen und ist kein Ereignis — heute trägt es `Updated 2026-10-15T05:14:43Z`,
dieselbe Minute wie die availability-Zeile und `producer.created` des WFCatalog. Die erste
Lesung ist eine Basislinie (`baseline: true`), kein Befund. Ereignisse werden verglichen,
nicht vermutet.

## Die erste Lesung — `planetary/readings/2026-10-15.json` (Tag 2026-10-14, Mittwoch)

- Tagesdatei: 200, 11 288 576 B, ein Trace, 8 640 325 Samples, SHA-256 `d8b75e98…`.
- 40 Trigger, **ein starker Impuls: 07:31:34 UTC, STA/LTA 153,05**, Spitzen-RMS 16 052
  gegen Hintergrund 87,5, Dauer 8,25 s. Ausschnitt
  `planetary/snapshots/2026-10-15/GE.RUE.HHZ/20261014T073134.mseed` (13 824 B).
  Das liegt im Band, das der Spike an vier Werktagen der Vorwoche maß (07:30:51–07:33:08);
  ein fünfter Werktag, nicht mehr. Kein Klassenname in irgendeinem Record.
- Herausgeber-Attest: 22 048 Records, 0 Lücken, 0 Überlappungen, 100 % availability,
  Quality D, `sample_rms` 2 360,97.
- extent: fünf Segmente; die vier geschlossenen tragen `Updated` 2022-07-26 (zwei),
  2022-07-28, 2022-10-12 — dieselben Werte wie im Audit vom 2026-08-22. Zwischen Audit und
  heute wurde die Geschichte also nicht umgeschrieben; das ist ein Vergleich zweier Lesungen
  mit 54 Tagen Abstand, nicht eine Behauptung über die Zwischenzeit.
- Kataloge, Box A, derselbe Tag: ISC 204 (null Zeilen), USGS 0 Features.
- Gesamtlast der Nacht im Repo: ≈ 40 KB (Audit-Ziel ≤ 400 KB).

## Bewusst nicht

Kein Workflow heute — der Aufnahme-Pfad lässt ihn erst nach der ersten committeten
V0-Lesung zu; die liegt jetzt vor, der Workflow ist das nächste Inkrement · kein
Fenster, keine Kriterien · kein Backfill zwischen Spike-Woche und heute (10-12, 10-13) ·
GR.KAST nicht nächtlich (Geseke geparkt) · keine Klasse „Sprengung" · kein
Lautstärke-Index (testgesichert) · die `PYTHONPATH`-Verdeckung aus Inkrement 1 nicht
repariert (der Workflow wird `pip install -e ./practice` und `PYTHONPATH=practice/src`
setzen, wie der Lauf heute).

**Nächstes Inkrement:** `.github/workflows/planetary.yml` — täglich nach ~06:00 UTC (die
`Updated`-Zeit des Herausgebers heute: 05:14:43), `python -m practice.planetary.nightly`,
`tools/anchor.py --register`, `verify.py`, Commit. Danach: Akzeptanzkriterien als Datei,
bevor ein Fenster öffnet.
