# Planetary Listening — V0, Inkrement 1: der Spike entscheidet die Paarung (2026-10-14)

**Stufe:** V0, Inkrement 1. Go: 2026-10-04 (Frank, Wortlaut privat; Ende von
`docs/2026-08-22-planetary-listening-audit.md`). Auflage 1 des Audits: Detektierbarkeit
wird **vor** dem Fenster gemessen, nicht vorausgesetzt — an zwei Paarungen, mit einem
Detektor, und die Wahl ist selbst ein Befund.

**Gebaut:** `practice/src/practice/planetary/` — `mseed.py` (miniSEED 2 lesen,
STEIM1/STEIM2/INT32 dekodieren, jede STEIM-Record gegen ihr eigenes Xn geprüft;
record-aligned Ausschnitte als Teilmenge der Herausgeberbytes), `detect.py` (Hüllkurve der
ersten Differenzen, STA/LTA, alle Parameter benannt und in jede Lesung geschrieben,
Version `stalta-v1`), `spike.py` (der Lauf). Nur Standardbibliothek. Tests:
`practice/tests/test_planetary_mseed.py`, `test_planetary_detect.py`,
`test_planetary_spike.py`, `test_verify_planetary.py` (ohne Netz).
`verify.py` hält die neuen Records (`check_planetary`): Manifest ↔ Bytes für
`planetary/probes/`, jeder Ausschnitt record-aligned und nur aus dem deklarierten
Theater (GE.RUE, GR.KAST — die Ortsliste liegt im Verifikator, nicht in einer Konfiguration;
Netz AM wird abgewiesen), höchstens vier Ausschnitte je Station-Tag, jede Anfrage nur an
die auditierten Hosts und mit SHA-256, Netz-DOI in jeder Tageszeile.

**Records:** Lesung `planetary/spike/2026-10-14.json` (Detektorparameter, je Station-Tag
Trigger, starke Impulse, Ausschnitte; Katalogabfragen; Anfrage-Ledger mit wörtlicher URL je
Knoten, Status, Größe, SHA-256 der empfangenen Bytes, `committed: false`).
Ausschnitte mit Manifest unter `planetary/probes/2026-10-14/`. Die Deklaration der
Paarung B, wörtlich transkribiert: `planetary/declarations/geseke-2026-10-14.json`.
Speichermodell nach Auflage 2: Tagesdateien werden geholt, gehasht, verworfen.

## Paarung A — Rüdersdorf (GE.RUE..HHZ, 100 Hz, auf dem Werksgelände)

Sieben volle Tage, Montag 2026-10-05 bis Sonntag 2026-10-11, je ~9,4–12,0 MB
(Wochentage größer als das Wochenende: mehr Bewegung, schlechter komprimierbar).
Starke Impulse (STA/LTA ≥ 50), aus der Lesung:

| Tag | starke Impulse (UTC) | Verhältnis | Spitzen-RMS / Hintergrund |
|---|---|---|---|
| Mo 10-05 | 07:33:08 · 11:33:52 | 140 · 1 026 | 20 045 / 100 · 66 350 / 47 |
| Di 10-06 | 07:30:51 | 165 | 18 659 / 89 |
| Mi 10-07 | 07:31:13 | 100 | 17 603 / 152 |
| Do 10-08 | 07:32:32 | 294 | 121 896 / 337 |
| Fr 10-09 | — (stärkster: 18,6) | | |
| Sa 10-10 | — (13,5) | | |
| So 10-11 | — (17,4) | | |

Das ist der Rhythmus, den das Audit für Nacht 14 als Möglichkeit beschrieb, nur schon in
Woche 1: an vier Werktagen ein Impuls zwischen 07:30:51 und 07:33:08 UTC (09:30–09:33
Ortszeit), am Freitag keiner, am Wochenende keiner. Der Abstand zum übrigen Tagesrauschen
liegt im Verhältnis, nicht in der Amplitude: die starken Impulse haben STA/LTA ≥ 99,8, die
übrigen 444 Trigger der Woche ≤ 32,8 — Faktor 3. In der Spitzen-RMS allein trennt es
schlechter (stärkster übriger Trigger 11 787 gegen schwächsten starken 17 603). Die Lesung
führt je Tag die drei stärksten Trigger und alle starken; die vollständige Triggerliste ist
aus dem Ledger reproduzierbar, nicht committet. **Die Katalogseite derselben Woche, dieselbe Box wie im Audit:**
ISC 204 (null Zeilen), USGS 0 Features.

**Was das nicht ist:** keine Klassifikation. Ein Impuls ist ein Impuls; dass es
Sprengungen sind, ist die naheliegende Lesart, nicht die Messung (Detektor-Docstring;
Audit „keine ML-Klassifikation", E-2). Der Montagsimpuls um 11:33:52 ist der stärkste
der Woche und passt nicht in den Rhythmus — er bleibt als Zeile stehen, ungedeutet.

## Paarung B — Geseke (GR.KAST..HHZ, ~49 km), gegen die Betreiber-Deklaration

**Befund 1, vor jeder Seismik: die Deklaration steht still.** Die öffentliche Seite des
Betreibers, gelesen am 2026-10-14, nennt zehn Termine vom 2025-07-28 bis 2025-08-28 und
keinen späteren — die letzte vorwärtsgerichtete Behauptung ist **412 Tage alt**. Das Audit
nannte den Kalender „stärker als eine Genehmigungsdatenbank", weil er eine datierte
Behauptung über die Zukunft ist. Heute ist er eine Behauptung über die Vergangenheit. Ob der
Betreiber aufgehört hat zu deklarieren, zu sprengen oder die Seite zu pflegen, sagt die
Seite nicht, und diese Datei behauptet es nicht.

**Befund 2: das Hören ist an dieser Entfernung nicht bewiesen.** Gemessen an den zehn
deklarierten Tagen und zehn Kontroll-Werktagen derselben Spanne, im deklarierten Fenster
10:00–12:00 Ortszeit (08:00–10:00 UTC), stärkster Impuls je Tag:

| | Median STA/LTA | Spanne | starke Impulse (≥ 50) |
|---|---|---|---|
| deklarierte Tage (10) | 22,0 | 8,2–88,7 | 1 (2025-08-28, 88,7) |
| Kontrolltage (10) | 16,6 | 10,5–288,1 | 2 (2025-08-05, 288,1; 2025-08-19, 51,3) |

Der stärkste Impuls der zwanzig Fenster liegt an einem **nicht** deklarierten Tag. Mit
diesem Detektor trennt GR.KAST deklarierte von nicht deklarierten Tagen nicht. Das
schließt nicht aus, dass ein bandbegrenzter oder Array-Ansatz es könnte; es schließt aus,
das für V0 vorauszusetzen. Kataloge derselben Spanne: ISC 204, USGS 0.

## Entscheidung (Auflage 1 des Audits; die Wahl liegt nach Franks Go beim Spike)

**Paarung A: Rüdersdorf.** Sie hört — vier von vier Werktagsimpulsen mit
Verhältnis ≥ 100, eine Woche lang regelmäßig — und ihre Gegenseite ist gemessen leer.
Paarung B fällt doppelt: eine Deklaration ohne Termin seit 412 Tagen und ein Hören, das
deklarierte Tage nicht von anderen trennt. Damit wird der Werk-Einzeiler aus dem Audit
gestützt, nicht verschoben: *eine Anlage, eine Station darauf, vier öffentliche Kataloge,
die nichts führen.*

**Der Preis, benannt:** Ohne Paarung B fehlt die Betreiber-Deklaration als zweites
Register; der Join läuft in V0 nur gegen die öffentlichen Kataloge. Flagship-Bedingung (d)
des Audits (zweiter Ort, zweites Meldegime) bleibt offen. Geseke ist **geparkt, nicht
verworfen**: fällt die Deklaration wieder vorwärts aus (neuer Termin auf der Seite), wird
das Hören erneut gemessen.

## Substrat-Befunde (Auflage 7)

- `fetch.Client` trägt Binärdaten ohne Änderung (eigener `Accept`-Header je Aufruf);
  ein 204 kommt als Status, nicht als Ausnahme.
- `preserve.Snapshot` trägt Binärausschnitte ohne Änderung.
- Ein Stolperstein: Vom Repo-Wurzelverzeichnis aus verdeckt der Ordner `practice/` das
  installierte Paket (Namespace-Package). `python -m practice.planetary.spike` braucht
  dort `PYTHONPATH=practice/src`. Nicht repariert — es betrifft jeden Modulaufruf von der
  Wurzel und gehört nicht in dieses Inkrement.
- BGR liefert in einem Vier-Stunden-Fenster überlappende Records (2025-08-01: drei
  Traces); `spike.analyse` entfernt doppelte Trigger gleicher Einsatzzeit. Es wird nichts
  interpoliert.

## Bewusst nicht

Kein Fenster, keine Kriterien, kein Workflow (erst nach der ersten committeten
V0-Lesung) · kein Backfill über die Spike-Tage hinaus · keine Klasse „Sprengung" in
irgendeinem Record · keine Infraschall-Achse, keine AM-Stationen · kein Lautstärke-Index
(testgesichert) · die Betreiberseite nicht als Ganzes konserviert (Kontaktzeilen;
transkribiert sind die zehn Zeilen und der Fenstersatz, mit SHA-256 der gelesenen Seite).

**Nächstes Inkrement:** die nächtliche Lesung für GE.RUE (T+1, ein Tag, Ausschnitte nach
Speichermodell) plus `availability`-Zeile mit `Updated` und WFCatalog-Tagesdokument
(Audit Befund 2: Neu-Einlagerung als detektierbares Ereignis).
