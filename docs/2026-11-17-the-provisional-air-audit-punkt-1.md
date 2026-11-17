# The Provisional Air — AUDIT, Punkt 1: Neulieferung ändert die Lieferzeit, nicht den Wert

**Datum:** 2026-11-17 · **Stufe:** AUDIT (Punkt 1, Abschluss) · **Teil 1:**
`docs/2026-11-13-the-provisional-air-audit.md` · **Teil 2:** `docs/2026-11-14-the-provisional-air-audit-teil-2.md`
· **Exposé:** `docs/2026-11-11-kandidat-the-provisional-air.md` · **Proben:** 2 Dateien mit Manifest in
`provisionalair/probes/2026-11-17/manifest.json` (Bytes und SHA-256, von `verify.py` `check_snapshots` gehalten).

**Anlass:** Teil 2 legt Punkt 1 auf einen Abend ab 2026-11-16, an dem kein früherer Kandidat einen
fälligen Schritt hat. Am 2026-11-16 ging der Abend an den Fensterschluss von The Interval; heute hat
kein früherer Kandidat etwas fällig (`discovery/AGENDA.md`: The Interval und Planetary Listening warten
auf den Review, `REQUESTS.md` 2026-11-16 und 2026-11-04; die Synthetic Flood auf ihren Workflow am
2026-12-04; The Declared Network und The Afterlife auf `REQUESTS.md` 2026-10-23 und 2026-10-30).

## Abruf

Zwei Abrufe, je ein Versuch, keine Wiederholung, Standardbibliothek, Kennung `machine-attention/0.1`,
keine Anfragefelder; nichts sonst wurde gesendet. Beide 200.

| Datei | vorher (konserviert) | heute |
|---|---|---|
| LU `airquality-p/LU/SPO-LU0101A_00005_103.parquet` | 2026-11-13, 181 133 B, `ETag` `0x8DF4158F7B11228`, `Last-Modified` 07:37:27 UTC, 7 591 Zeilen bis 2026-11-13 07:00 | 185 606 B, `ETag` `0x8DF4476A28621A8`, `Last-Modified` 2026-11-17 06:47:23 UTC, 7 686 Zeilen bis 2026-11-17 06:00 |
| DE `airquality-p/DE/SPO.DE_DEBE010_PM1_dataGroup1.parquet` | 2026-11-14, 221 441 B, `ETag` `0x8DF421D4E7603AC`, `Last-Modified` 07:02:54 UTC, 7 344 Zeilen bis 2026-11-14 23:00 | 222 609 B, `ETag` `0x8DF44787FCEFBC8`, `Last-Modified` 2026-11-17 07:00:44 UTC, 7 416 Zeilen bis 2026-11-17 23:00 |

Gelesen mit einer Wegwerf-Umgebung außerhalb des Baums (wie Teil 2); verglichen wurde Stunde für
Stunde über den Stundenanfang (`Start`), der in beiden Fassungen eindeutig ist. Keine Stunde der
früheren Fassung fehlt in der heutigen (LU 0, DE 0).

## Befund

**Luxemburg** (7 591 gemeinsame Stunden): **0 Werte geändert**, 0 `Validity`, 0 `Verification`
geändert. 24 Stunden haben eine neue `ResultTime`: 23 der 24, die am 2026-11-13 die jüngste
Lieferzeit trugen (2026-11-12 09:00 bis 2026-11-13 07:00, alle 08:25:07; 2026-11-12 08:00 behielt
08:25:07), dazu 2026-11-12 07:00 (06:25:07 → 07:25:07). In der heutigen Fassung trägt fast jede dieser Stunden eine eigene Lieferzeit rund einen Tag nach der Stunde (z. B. 2026-11-12 10:00 →
2026-11-13 10:25:07; 2026-11-13 05:00 → 2026-11-14 05:25:07; sechs Nachtstunden gemeinsam 2026-11-13
23:25:07). Dasselbe Muster zeigen alle Tage ab 2026-11-10 in der heutigen Datei: Luxemburg liefert jede
Stunde rollend am Folgetag neu, und der Batch von 08:25:07 am 2026-11-13 wurde Stunde für Stunde
überschrieben — **mit denselben Werten**.

**Deutschland** (7 344 gemeinsame Stunden): 48 Stunden mit neuer `ResultTime` — 2026-11-13 00–23 h
(07:45:45 → 2026-11-14 23:45:40) und 2026-11-14 00–23 h (07:45:45 → 2026-11-15 23:45:40), also der in
Teil 2 beschriebene Takt „am Ende des Folgetags". Von diesen 48 waren 31 schon Werte (`Validity` 1):
**0 geändert**. Die übrigen 17 (2026-11-14 07:00–23:00) waren Platzhalter (−999, `Validity` −1) und
sind jetzt Werte (7.63 bis 17.31 µg/m³, `Validity` 1). Das ist Erstlieferung, keine Änderung. Neu:
Die heutige Datei trägt 87 Platzhalter, die Zukunft von 2026-11-17 07:00 an eingeschlossen.

**Zusammen: 55 Stunden mit Wert wurden zwischen zwei Fassungen neu geliefert, 0 davon mit anderem
Wert.** Gemessen ist das an zwei Messstellen, einem Schadstoff, einer Neulieferung je Stunde — keine
Aussage über die Monatsneulieferung Luxemburgs oder die Quartalsneulieferung Deutschlands (Teil 1 §1,
Teil 2 Punkt 3), die diese beiden Abrufe nicht erfassen.

**Nebenbefund aus den konservierten Dateien, kein neuer Abruf:** In der deutschen Datei tragen Januar
bis März (2 160 Stunden, die am 2026-05-08 als Quartal neu gelieferten) `Verification` 2, alle übrigen
Monate 3; in der luxemburgischen alle 3 (Teil-2-Datei und heutige gleich). Zwischen „nicht verifiziert"
und dem validierten E1a liegt bei Deutschland also eine Zwischenstufe; ob deren Neulieferung Werte
änderte, ist im Download nicht mehr zu sehen — die frühere Fassung ist getilgt (Teil 2).

## Endgültige Empfehlung

Teil 2 hat festgelegt, was aus diesem Punkt folgt: „ändert sie nur die `ResultTime`, schrumpft der
Kandidat auf den Sprung zur Validierung, und das wäre zu sagen." **Das ist hiermit gesagt.** Die
tägliche Neulieferung ist in dieser Probe ein Umstempeln, kein Umschreiben; nächtliches Festhalten
gewinnt dort nichts, was ein einziger späterer Abruf nicht auch hätte.

Was bleibt, ist der Kern des Exposés: Der vorläufige Wert eines Jahres verschwindet aus dieser Quelle,
sobald das validierte Jahr erscheint (Teil 1: E2a beginnt 2026-01-01, E1a hält 2024–2025). Wer 2026
vorläufig gegen validiert vergleichen will, muss die vorläufige Seite **jetzt** festhalten; der
Vergleich wird erst mit der E1a-Lieferung für 2026 möglich (für 2025 kam sie im Herbst 2026, LU-E1a
`Last-Modified` 2026-10-20, `provisionalair/probes/2026-11-13/manifest.json`). Dazu kommen die
Zwischenstufen (Monat LU, Quartal DE mit `Verification` 2), deren Wertwechsel nur ein Festhalten vor der
Neulieferung zeigt.

**Empfehlung: GO für ein enges V0, enger als in Teil 2** — wenige Messstellen in zwei Ländern, PM10;
**nicht nächtlich, sondern wöchentlich**, und nur bei geändertem `ETag`; committet werden abgeleitete
Zeilen (Stunde, Wert, `Validity`, `Verification`, `ResultTime`, Hash der Quelldatei), nicht die Dateien;
−999 nie als Wert; Platzhalter nie als Fassung. Der Wochentakt reicht, weil die tägliche Neulieferung den
Wert nicht ändert (oben) und die Monats- und Quartalsneulieferungen Wochen auseinanderliegen. Die
Tagesschwellen bleiben an Richtlinie (EU) 2024/2881 gebunden (Teil 1 §3), die Zeitzone ist vor dem
ersten Zählen aus der Dokumentation zu belegen (Teil 2 Punkt 3). **Offen zu sagen:** Das Ergebnis, für
das das Instrument gebaut würde — der Sprung zur Validierung für 2026 — liegt rund ein Jahr entfernt; ein
E-Experiment vorher kann nur die Treue der Festhaltung prüfen (Abdeckung, kein Verlust einer Fassung vor
der Neulieferung), nicht den Befund. Ob ein Instrument mit so langem Weg zum Befund in die Praxis passt,
ist die Frage des GO.

Bitte um das GO: `REQUESTS.md` (2026-11-17).

## Bewusst nicht heute

Kein dritter Abruf, keine weitere Messstelle, kein E1a-Abruf, kein UBA, kein OpenAQ. Kein Code unter
`practice/`, kein Stationssatz, keine Schwelle. Das GO für V0 bleibt dem Maintainer.
