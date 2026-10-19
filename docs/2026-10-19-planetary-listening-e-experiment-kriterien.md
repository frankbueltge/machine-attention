# Planetary Listening — E-Experiment: Abnahmekriterien (2026-10-19)

**Stufe:** V0, Inkrement 4 — die Kriterien des E-Experiments, committet **bevor** das Fenster
aufgeht. Go für V0: 2026-10-04 (Frank, Wortlaut privat; Ende von
`docs/2026-08-22-planetary-listening-audit.md`). Vorgänger:
`docs/2026-10-16-planetary-listening-v0-inkrement-3.md`.
**Maschinenlesbar:** `planetary/experiment.json` (trägt die Prüfsumme dieses Dokuments;
`verify.py`, `check_planetary_experiment`, scheitert, wenn beide auseinanderlaufen, wenn die
Kriterien nicht vor der ersten Fensternacht datiert sind oder das Fenster kürzer als 14 Nächte
ist). **Zählung:** `python -m practice.planetary.experiment --repo-root .`
(`practice/src/practice/planetary/experiment.py`). **Vorbild:** die Kriterien von The Interval
(`docs/2026-10-14-the-interval-e-experiment-kriterien.md`).

## 0. Bindung

Dieses Dokument bindet mit seinem Commit. Änderungen sind bis zum Tag vor der ersten
Fensternacht erlaubt, also bis **2026-10-20** (datierter Nachtrag mit Begründung,
`experiment.json` und seine Prüfsumme im selben Commit), danach nicht mehr. Die Lesungen vor
dem Fenster (`planetary/readings/2026-10-15.json` bis `2026-10-18.json`, dazu die vom
2026-10-19 und 2026-10-20, sobald der Workflow sie committet) sind **Vor-Fenster-Kontext**:
Sie zählen nicht als E-Evidenz, gehen aber in die Vorher-Seite von B4 ein.

## 1. Das Fenster

**14 Nächte ohne Lücke**, die Länge, die das Audit nennt (Offene Entscheidung 1:
„14-Nächte-Fenster danach"). Eine Nacht ist ein Lesungsdatum; gelesen wird jeweils der
UTC-Tag davor.

| | Lesung | gelesener Tag |
|---|---|---|
| erste Nacht | 2026-10-21 | Di 2026-10-20 |
| letzte Nacht | 2026-11-03 | Mo 2026-11-02 |

Das Fenster schließt am **2026-11-03**; das Review ist ab dem **2026-11-04** möglich und gehört
dem Maintainer. Die erste Nacht liegt zwei Tage hinter diesem Commit, damit die Kriterien auf
`main` stehen, bevor die erste Fensterlesung entsteht. Eine Nacht zählt, wenn
`planetary/readings/<date>.json` committet ist (der Workflow läuft täglich; ein Nachlauf per
`workflow_dispatch` am selben Datum zählt) und `verify.py` auf ihr grün ist.

## 2. Abnahmekriterien

### A — Betrieb (aus den Lesungen gezählt)

| # | Kriterium | Latte |
|---|---|---|
| A1 | committete Lesung je Nacht | **mindestens 13 von 14**, nie zwei Nächte in Folge fehlend |
| A2 | Nächte, in denen die Tagesdatei (`station_day.outage` oder Status ≠ 200), die extent-Tabelle oder ein Katalog (Status nicht 200/204) ausfällt | **höchstens 1**, die Ursache im Record benannt |
| A3 | HTTP 429 von irgendeinem Host in einer Fensterlesung | **0** |
| A4 | was eine Nacht ins Repo legt: Snapshots unter `planetary/snapshots/<date>/` plus die Lesung | **≤ 400 KB** je Nacht (Audit, Auflage 2); vor dem Fenster gemessen 7,9–25,2 KB |
| A5 | `verify.py` grün auf jeder Fensterlesung: nur auditierte Hosts, deklariertes Theater (GE.RUE), höchstens vier record-aligned Ausschnitte, Neu-Einlagerung unabhängig nachgerechnet | ohne Ausnahme (CI-Gate) |

### B — Messung

| # | Kriterium | Latte |
|---|---|---|
| B1 | **Herausgeber-Attest.** Nächte, in denen availability-Zeile und WFCatalog-Tagesdokument für den gelesenen Tag ankamen | berichtet, **keine Latte** (siehe §4.1) |
| B2 | **Neu-Einlagerung.** Ereignisse `segment_rewritten`, `segment_gone`, `segment_inserted` | berichtet, jedes mit seinen extent-Zeilen; eine Abweichung zwischen Lesung und Nachrechnung des Verifikators ist ein Verstoß (A5) |
| B3 | **Der Kalender.** Je gelesenem Tag die starken Impulse (STA/LTA ≥ 50) mit UTC-Einsatz und Verhältnis, oder ein Strich | berichtet, 14 Zeilen |
| B4 | **Die Uhr.** Siehe §3 | berichtet, **keine Latte** — ein Befund, keine Abnahme |
| B5 | **Das andere Register.** Je Kalenderzeile die Zeilen von ISC und USGS für denselben Tag und dieselbe Box | berichtet |
| B6 | **Der Detektor steht still.** `detector` = `stalta-v1` mit den Parametern in `experiment.json`, `strong_ratio` 50, höchstens 4 Ausschnitte, in jeder Fensterlesung | **0 Änderungen** |

### C — Ethik und Charter (Ausschluss, keine Punkte)

Keine Klasse in einem Record: weder „Sprengung" noch blast, explosion oder quarry außerhalb
des wörtlichen Anfrage-Ledgers (die Zählung sucht danach). Kein Lautstärke-Index. Keine
natürliche Person, keine AM-Station (I8; Audit, Ethik 4). Keine Zuschreibung (E-2): Eine
Zeile sagt Impuls, Zeit, Station, und ob ein Register einen Eintrag hat — nie wer, nie
„ungenehmigt", nie „verschwiegen". Die Auslassung der Kataloge ist ihre Bauart, kein
Versäumnis (Audit, Befund 5). Bis zum Review keine Bühne: Planetary Listening steht auf der
Site mit keiner Seite, keiner Figur, keiner Zahl.

**Bestanden = A1–A5 erfüllt · B6 ohne Änderung · B1–B5 berichtet · C ohne Verstoß.**

## 3. B4 — die Uhr, vorab festgelegt

Deutschland verlässt die Sommerzeit am **Sonntag, 2026-10-25** (03:00 MESZ → 02:00 MEZ). Die
starken Impulse der Vor-Fenster-Werktage lagen zwischen 07:30:51 und 07:33:08 UTC
(Spike-Woche, `planetary/spike/2026-10-14.json`) und um 07:31:34 und 07:31:49 UTC
(`planetary/readings/2026-10-15.json`, `2026-10-16.json`), also bei 09:30–09:33 MESZ.

Die Regel, bevor ein Tag nach der Umstellung gelesen ist:

- Gezählt wird je **Werktag** (Mo–Fr) der **erste** starke Impuls des Tages, aus allen
  committeten Lesungen, die vor dem Fenster eingeschlossen.
- Vorher-Seite: gelesene Tage vor 2026-10-25; Nachher-Seite: ab 2026-10-25.
- Δ = Median(nachher) − Median(vorher) in Minuten UTC.
- **`local`**, wenn |Δ − 60| ≤ 10: der Impuls folgt der Ortsuhr. **`utc`**, wenn |Δ| ≤ 10:
  er folgt einer Uhr, die die Umstellung nicht kennt. Sonst **`neither`**. Hat eine Seite
  weniger als zwei Tage: **`undetermined`**.

Die Spike-Woche bleibt außerhalb der Zählung (andere Datei, anderer Lauf); sie ist der
Grund für die Erwartung, nicht ihr Beleg. Die Erwartung, notiert: `local`, Einsätze um
08:30–08:34 UTC ab Montag 2026-10-26. Das wäre eine Aussage, die keine einzelne Nacht machen
kann und kein Katalog führt: dass die Maschine an einem Ort, an dem kein Register etwas
verzeichnet, die Uhr eines Betriebs hört. Es bleibt eine Aussage über eine Uhr, nicht über
eine Tätigkeit, und sie nennt niemanden.

## 4. Bekannte Konfundierer — vor Fensterstart benannt

1. **Der Herausgeber-Index hinkt.** Auf den zwei Läufen des Workflows (2026-10-17 um 11:08,
   2026-10-18 um 11:39 UTC) antworteten availability und WFCatalog für den gelesenen Tag mit
   204. Die committete extent-Tabelle zeigt warum: Am 2026-10-17 endete das offene Segment
   noch bei 2026-10-16T00:00 (`Updated 2026-10-16T05:00:57Z`), am 2026-10-18 bei
   2026-10-17T00:00 (`Updated 2026-10-18T03:29:39Z`) — beide Male einen Tag vor dem Ende des
   gelesenen Tages (`planetary/snapshots/2026-10-17/GE.RUE.HHZ/extent.txt`, `2026-10-18/…`).
   Die Tagesdatei kam trotzdem vollständig (Status 200, ein Trace). Das Attest über den Rest
   des Tages fehlt dann; VERIFY hält weiter für jede Behauptung, nicht für das Schweigen. B1
   zählt es, ohne Latte, weil es der Herausgeber ist, nicht das Instrument. Ein Nachholen des
   Attests für den Vortag ist eine Codeänderung und würde das Fenster ändern; sie wird nicht
   im Fenster gemacht.
2. **Der Workflow läuft spät.** Geplant 06:40 UTC, gelaufen 11:08 und 11:39 UTC. Das berührt
   A1 nicht (das Datum zählt, nicht die Uhrzeit) und die Lesung nicht (gelesen wird der
   abgeschlossene Vortag).
3. **Ferien und Betriebsruhe.** Ein leerer Werktag ist eine Zeile mit Strich, kein Fehler.
   Freitags und am Wochenende war in der Spike-Woche kein starker Impuls; 2026-10-16 (Fr)
   und 2026-10-17 (Sa) ebenso.
4. **Ein starker Impuls ist kein Ereignis einer Klasse.** Der Montagsimpuls der Spike-Woche
   um 11:33:52 UTC passt in keinen Rhythmus; B4 zählt nur den ersten starken Impuls je
   Werktag, damit ein solcher Ausreißer den Median nicht trägt.
5. **Kataloge haben Nachlauf.** ISC und USGS werden am Folgetag abgefragt; ein später
   nachgetragener Katalogeintrag erscheint im Fenster nicht. Benannte Grenze; B5 berichtet,
   was am Lesetag stand.

## 5. Drei mögliche Ausgänge (die Entscheidung ist des Maintainers)

- **RUNNING · Instrument** — A und B6 ohne Verstoß: die nächtliche Lesung bleibt, der Kalender
  wird fortgeschrieben; eine Bühne ist eine eigene Entscheidung. Die Flagship-Bedingungen des
  Audits (a)–(d) prüft dieses Fenster nicht.
- **Verlängert** — A1 oder A2 knapp verletzt mit benannter, behobener Ursache: ein neues
  Fenster, mit neuen, vorher committeten Kriterien.
- **RETIRED** — B6 oder C verletzt, oder A1 gerissen ohne benannte Ursache.

## Bewusst nicht

Kein neuer Abruf heute; jede Zahl oben steht in einer committeten Datei · keine Änderung an
`nightly.py` vor dem Fenster (auch nicht für §4.1) · kein Backfill (2026-10-12, 2026-10-13) ·
GR.KAST nicht nächtlich (Geseke geparkt) · keine Klasse, kein Lautstärke-Index · keine Bühne.
