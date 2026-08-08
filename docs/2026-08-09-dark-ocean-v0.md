# Dark Ocean V0 — Coverage vs Declaration (gebaut)

**Datum:** 2026-08-09 (kurz nach UTC-Mitternacht; Franks GO kam in der Nacht
08./09.) · **Stufe:** V0 des Aufnahme-Pfads · **Grundlage:**
`2026-08-08-dark-ocean-audit.md` (GO mit vier Auflagen)

## Franks Entscheidungen (protokolliert, autonomy/log.jsonl)

1. **GO für die V0** „Coverage vs Declaration" ✓
2. **Region Ostsee** bestätigt ✓
3. **Eskalation a (Copernicus-Account)** bewilligt — wird aktiv, sobald das
   Secret existiert; die V0 braucht es nicht
4. **Eskalation b (GFW-Token-Zweitnutzung)** bewilligt — dito; ausschließlich
   für NC-markierte Vergleichsschichten, nie im CC0-Rückgrat

## Was die V0 tut (nächtlich, 04:50 UTC, vollständig keyless)

Die Maschine beurkundet **den Akt des Hinschauens gegen den Akt des
Sich-Erklärens**: Für den abgeschlossenen UTC-Tag D konserviert sie die
CDSE-Katalogzeilen aller Sentinel-1-GRD-Aufnahmen über der Ostsee-Box
(9–30 E, 53,5–66 N; 0,5°-Bins) — mit den **Checksummen des Herausgebers**
(BLAKE3/MD5), Footprints und `EvictionDate`; die Szenen-Bytes (1–2 GB,
login-pflichtig) werden nie geholt, die Katalogzeile ist der notarielle
Gegenstand. Dagegen: ein Digitraffic-AIS-Sample zum Lesezeitpunkt — als
Zählungen je Bin, **nie mit Schiffsidentitäten** (der Prüfer erzwingt das:
ein `mmsi` in einem abgeleiteten Record ist ein Verifikationsfehler).
Die DMA-Tagesdumps (Momenten-Achse) werden nächtlich **geprobt, nicht
geholt** — drei Ausfälle am 08.08.; die Rückkehr der Quelle wird damit im
Record sichtbar, und der Momenten-Adapter ist der protokollierte nächste
Schritt für die erste Nacht, in der sie antwortet.

Kategorien je Bin: `observed_passes` × `declared_sample` → daraus
observed-and-declared / observed-silent-in-sample / declared-unobserved —
ausdrücklich Aussagen über die Überlappung zweier committeter Register,
nie über versteckte Schiffe.

## Erste Lesung (2026-08-07, gerechnet 2026-08-08 23:57 UTC)

- **84 Katalogprodukte = 42 Aufnahmen** (das SAFE/COG-Paar des Katalogs,
  sichtbar dedupliziert, beide Zahlen im Record)
- Getragen von **S1C (23) und S1D (19)** — kein einziges S1A-Produkt: der
  Generationswechsel, an dem GFWs Ableitung seit fünf Wochen hängt, ist in
  den Rohdaten vollzogen
- **563 von 1050 Bins** an einem Tag radar-überflogen (54 %)
- Deklarierte Achse: **937 Schiffe in der Region** (Sample 23:57 UTC,
  154 Bins); dichtester Überlapp im Schärengebiet vor Turku
  (E22.0_N60.0: 2 Überflüge, 46 deklarierte Schiffe)
- DMA: outage, protokolliert. 0 Quellen-Failures.
- `verify.py` rechnet die Lesung vollständig aus den konservierten Bytes
  nach (Zweitimplementierung inkl. eigener Gitter- und Polygon-Mathematik).

## Substrat-Stresstest (Auflage 4) — Befund

`Snapshot`/`preserve`/`autonomy` trugen **unverändert**. Einziger nötiger
Eingriff ins Substrat: `Client.fetch` akzeptiert jetzt additive Header
(Digitraffic erzwingt gzip; der Adapter dekomprimiert selbst und
konserviert das Dokument). Noch **nicht** gestresst: GB-Skala (kommt erst
mit DMA-Dumps bzw. V1-Szenen) — offen vermerkt, nicht behauptet.

## GCP-Notiz (Franks Direktive aus derselben Nacht)

Frank will das GCP-Potential aller Projekte geprüft sehen. Für Dark Ocean
gibt es einen konkreten Kandidaten: **Sentinel-1 liegt in Earth Engine**
(und Teile in BigQuery/Public Datasets) — das könnte den V1-Detektionspfad
(Szenen-Prozessierung) tragen, statt GB-Downloads auf Actions-Runnern.
Zu AUDITIEREN (Lizenz! Earth Engine ist für Nichtkommerzielles frei, aber
mit eigenen Terms; Nachprüfbarkeits-Ethik: jeder GCP-Schritt braucht
Trace), nicht heute zu bauen. Gehört in die Portfolio-/GCP-Session.

## Bewusst nicht (V0)

Keine Detektion · keine Szenen-Bytes · keine Schiffsidentitäten · keine
Bühnen-/Site-Präsenz (erst nach E-Experiment, Aufnahme-Pfad Stufe 5) ·
keine E-Experiment-Kriterien um 2 Uhr nachts — die werden **vor** Start
des 14-Nächte-Laufs in eigener Session committet (Stufe-4-Pflicht).

## Nächste Schritte

1. Nächte akkumulieren; DMA-Rückkehr im Record beobachten → dann
   Momenten-Adapter (der echte GB-Stresstest).
2. E-Experiment-Kriterien committen, dann 14-Nächte-Lauf.
3. Eskalations-Secrets, sobald Frank sie hinterlegt: Copernicus-Account
   (V1-Detektion), `GFW_TOKEN` (NC-Vergleichsschichten).
4. GCP-Audit für den V1-Pfad in der Portfolio-Session.
