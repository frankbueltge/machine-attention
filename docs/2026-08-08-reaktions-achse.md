# Die Reaktions-Achse — was sich bewegte, während die Uhr lief

**Datum:** 2026-08-08 (UTC) · **Status:** gebaut, nächtlich laufend
**Projekt:** 001 The Foreknown · **Roadmap-Punkt 2** aus
`2026-08-08-projekt-aufnahme.md` („Werk-Tiefe vor neuen Quellen")

## Herkunft: die Maschine war zuerst da

Der erste Discovery-Pass (Nacht 1, PR #1) hat aus eigenem Antrieb drei Sensor-Proposals
geliefert. Eines davon, `sensor-fts-country-coverage`, beschreibt exakt die Reaktions-Achse:
ein mechanischer iso3-Abgleich der offenen Warnungen gegen die konservierten
OCHA-Response-Pläne — **inklusive der ausdrücklichen Weigerung, daraus ein Urteil über
Finanzierungs-Angemessenheit zu machen.** Die Maschine hat die Achse vorgeschlagen, bevor
ein Mensch sie gebaut hat; dieser Bau setzt auf ihrem Text auf, nicht neben ihm.

Definition, Testregel und Falsifikation des Proposals sind **unverändert übernommen** und
so implementiert, wie sie dastehen. Was hinzukommt (Geldbeträge, Aufmerksamkeitsvolumen),
liegt als Erweiterung um den Kern herum und ist im Record als solche benannt.

## Quellen-Audit (Live-Probes 2026-08-08, UTC-Abend)

| Quelle | Endpoint | Befund |
|---|---|---|
| **OCHA FTS — Bedarf** | `api.hpc.tools/v1/public/plan/year/2026` | bereits nächtlich konserviert (35 Pläne, `locations[].iso3`, `revisedRequirements`) — die Achse liest die Bytes des Notariats zurück, statt dasselbe Dokument zweimal zu holen |
| **OCHA FTS — Geld** | `…/fts/flow?year=2026&groupby=plan` | HTTP 200, **65 KB, ein Request für alle Pläne**. `report3` (destination) geprüft gegen die Einzelplan-Abfrage: planid=1498 → 84.257.438 in beiden; `report2` liefert 82.346.102 — report3 ist die Reihe, die FTS selbst publiziert |
| **GDELT — Aufmerksamkeit** | `data.gdeltproject.org/events/YYYYMMDD.export.CSV.zip` | HTTP 200, **6,4 MB/Tag, ein Request/Tag**, 102.018 Zeilen, 58 Spalten, 222 Länder. Nicht die DOC-2.0-API (drosselt mit klebrigen IP-Blocks, Hausbeleg: `frankbueltge.de/pipelines/newspool`, 2026-08-04/05) |
| **GDELT — Ländercodes** | `gdeltproject.org/data/lookups/FIPS.country.txt` | HTTP 200, 274 Codes — die Herausgeber-eigene Liste, gegen die der Crosswalk geprüft wird |
| FTS-Einzelflüsse (`?planid=X`) | 281 KB/Plan | **bewusst nicht gebaut:** eine rückwirkende Funding-Kurve aus Flow-Daten wären ~7 MB/Nacht. Der Befund ist notiert, die Kurve verschoben |

## Was gebaut wurde

```
foreknown/reaction/
  iso3-fips.json              der Crosswalk (75 Einträge) — handgeschrieben,
                              gegen die Herausgeber-Liste geprüft, mit Fundstelle
  snapshots/<datum>/          fts-funding-2026.json + fips-country.txt + manifest
  attention/<datum>.json      ein Tag Weltaufmerksamkeit je Land (222 Länder)
  readings/<datum>.json       die nächtliche Lesung: je offener Zukunft Geld + Aufmerksamkeit
```

**Geld.** Je angekündigter Zukunft: welche OCHA-Pläne 2026 mindestens eines ihrer Länder
listen (`has_fts_plan_match` — das Feld der Maschine, unverändert), deren Plan-IDs, deren
Jahresbedarf und deren von FTS gemeldeter Finanzierungsstand. Die Felder heißen
`plan_requirements_usd` und `plan_funded_usd`, weil die Zahlen **den Plänen gehören, nicht
dem Ereignis** — ein Plan, der ein Land listet, bringt seinen ganzen Jahresappell mit.

**Aufmerksamkeit.** Je Zukunft die Artikel-Erwähnungen des Tages aus ihren Ländern, ihr
Anteil an der Welt (`share_per_10k`) und ihr Verhältnis zum eigenen 28-Tage-Median
(`ratio_to_baseline`). Rückwirkend gerechnet: **60 Tage sind nachgeladen** (2026-06-09 bis
2026-08-07), also existiert der Basiswert ab der ersten Nacht statt erst in einem Monat.
Öffentliche Historie zu laden ist kein Backfill im Sinne des Invariants — rückdatiert wird
kein einziger eigener Eintrag (Korrektur-Dokument §1).

**Provenienz ohne Datenhalde.** Die GDELT-Tagesdateien werden **nicht** im Repo abgelegt
(6,4 MB/Tag). Jeder Tages-Record trägt url, SHA-256 der gelesenen Bytes, Länge und
Abrufzeit: Die Datei ist nach Veröffentlichung unveränderlich, also ist die Ableitung
nachrechenbar — und ein nicht mehr passender Hash wäre kein toter Link, sondern der Befund.
Das ist der erste reale Fall des `artifact_ref`-Vertrags aus der Projekt-Aufnahme (§5),
lokal gelöst, nicht als Framework vorgebaut.

## Der Crosswalk — und was er gefunden hat

GDACS liefert iso3, GDELT verortet nach FIPS 10-4. Der Übersetzer ist das einzige
handgeschriebene Glied der Kette und deshalb belegt: jeder FIPS-Code steht in der
Herausgeber-Liste, keine zwei iso3 zeigen auf denselben Code, und der Name, den GDELT dem
Code gibt, steht daneben — ein falscher Eintrag ist ohne Nachschlagen sichtbar. `verify.py`
prüft das gegen die konservierte Liste, nicht gegen sich selbst.

**Fundstelle, im Record vermerkt:** GDELT führt FIPS `LO` bis heute als *„Czechoslovakia"* —
ein Staat, den es seit 1992 nicht mehr gibt. Die Daten unter `LO` sind slowakisch (Probe
2026-08-07: „Slovak Republic", „Bratislava, Bratislavsky Kraj"), FIPS 10-4 weist `LO` der
Slowakei zu; die Zuordnung SVK→LO stimmt, das Etikett des Instruments ist veraltet. Nicht
stillschweigend korrigiert, sondern notiert.

Nur die 75 Länder, die bisher in der Registry vorkamen, sind übersetzt. Ein iso3 ohne
Eintrag erscheint in jeder Lesung als `unmapped_iso3` — eine Lücke steht im Record, statt
sich als „null Aufmerksamkeit" zu tarnen.

## Was die Zahlen nicht sind

In jeder Lesung als `notes` mitgeschrieben, nicht als Fußnote nachgereicht:

1. Plan-Bedarf und Plan-Finanzierung sind **Jahreszahlen der Pläne für alle ihre Länder** —
   nicht dem Ereignis zurechenbar, keine Aussage über Angemessenheit, Bedarf oder
   Verantwortung.
2. `articles` summiert GDELTs NumArticles über die Ereignisse eines Landes: ein
   **Volumen-Proxy**, keine Zahl unterschiedlicher Artikel.
3. **Aufmerksamkeit wird für das Land gemessen, nicht für die Gefahr.** Ein Landesvolumen
   bewegt sich aus vielen Gründen gleichzeitig; diese Achse kann sie nicht trennen. (Der
   höchste Wert der ersten Lesung — Thailand, 11,0× — ist genau deshalb keine Aussage über
   die thailändische Flut.) Themen-spezifische Aufmerksamkeit über die GKG-Themes wäre der
   nächste Schritt und ist bewusst nicht gebaut.
4. Ein Land ohne passenden Plan ist eine Tatsache über zwei Register, kein Befund über die
   Welt.

## Verifikation

`verify.py` nimmt die Lesung nicht beim Wort, sondern **rechnet sie aus den konservierten
Bytes nach** — bewusst als zweite Implementierung, denn ein Prüfer, der den geprüften Code
aufruft, beweist nur, dass Code mit sich selbst übereinstimmt: Plan-Treffer, Plan-Summen,
Artikelzahlen, Weltanteil, Median und Verhältnis, dazu Crosswalk gegen Herausgeber-Liste und
die Identität `world == Σ Länder + unlocated` je Aufmerksamkeitstag. Der Basiszeitraum steht
als Datumsliste in der Lesung, damit später nachgeladene Tage eine alte Lesung nicht
unrechenbar machen. Tests: 27 grün, davon 11 neu.

## Beförderung — und zwei ehrliche Nicht-Beförderungen

- **`sensor-fts-country-coverage` → STANDING.** Er misst ab jetzt jede Nacht und committet
  seinen Wert. **Das Feuern bleibt DEFERRED:** Das Proposal weigert sich, Schwellen aus einer
  einzigen Stichprobe zu setzen, und diese Weigerung steht im Code — die Lesung zählt die
  Nächte und schärft den Sensor selbst in der dritten. Die Bedingung der Maschine wird
  erzwungen, nicht erinnert.
- **`sensor-cold-start-overdue-drift` → IMPLEMENTED, nicht befördert.** Der Split ist gebaut
  (`futures.py: overdue_kind`), aber das Proposal verlangt für die Beförderung mindestens
  einen real beobachteten `drift_overdue`-Fall. Heute gibt es keinen und kann es keinen
  geben: Alle 100 überfälligen Warnungen sind Kaltstart per Konstruktion. Code jetzt,
  Beförderung wenn der Beleg da ist.
- **`sensor-forecast-kind-gap` → bleibt PROPOSED.** Er verlangt 14 Nächte. Dies ist Nacht 1.

## Erste Messwerte (Lesung 2026-08-08)

- 100 offene Alert-Episoden, **37 mit Plan-Treffer (37 %)** — erster Basiswert der Serie.
- 60 Aufmerksamkeitstage konserviert, 222 Länder je Tag, 1.134.791 Artikel-Erwähnungen am
  2026-08-07 (davon 90.310 ohne Verortung, separat geführt).
- Spannweite `ratio_to_baseline` über die 100 offenen Warnungen: 0,41× (Erdbeben Afghanistan)
  bis 11,0× (Flut Thailand) — beides Landeswerte, siehe Grenze 3.
- Bühne: die Featured-Karte trägt **einen** Satz („Meanwhile, …"), kein Dashboard.

## Bewusst nicht gebaut

Keine Funding-Kurve aus Einzelflüssen · keine themenspezifische Aufmerksamkeit (GKG) · keine
Wirksamkeits- oder Angemessenheits-Kennzahl · keine Länder-Rankings · keine eigene Prognose ·
kein Reaktions-Dashboard auf der Bühne.
