# Re-Audit der geparkten Kandidaten

**Datum:** 2026-08-22 · **Anlass:** Franks Frage vom 2026-08-22, warum sich in der Praxis
seit zwei Wochen wenig bewegt (Wortlaut privat) · **Stufe:** Vorprüfung vor Stufe 2 (AUDIT)
des Aufnahme-Pfads

**Geprüfte Hypothese:** Am 2026-08-08 wurden fünf Kandidaten als Exposés geschrieben, zwei
gebaut (Dark Ocean V0 am 09.08., Memory Hole V0 am 15.08.). Drei stehen seit dem 08.08.
unverändert auf EXPOSÉ, jeder an genau einem benannten Blocker. Einen Tag später, am
2026-08-09, hat das Haus GCP für Batch-Schritte aktiviert. Die Vermutung lautete: zwei der
drei Blocker sind seither hinfällig, und niemand hat die Parkzettel nachgelesen.

**Ergebnis: in der Sache richtig, in der Begründung falsch.** Ein Blocker ist gefallen —
aber nicht durch GCP, sondern durch die eigene Bauarbeit an Dark Ocean. Ein zweiter ist
durch die Aktivierungs-Unterlagen sogar **härter** geworden. Der dritte steht unverändert.

## 1. Die drei Blocker, wie sie am 2026-08-08 formuliert wurden

- **Planetary Listening** (offene Frage 2): ein Speichermodell für Wellenformen — Git
  reicht nicht, Releases oder Objektspeicher? Dazu die EarthScope-Migration
  (IRIS-Endpunkt antwortete mit HTTP 307) und CTBTO-Infraschall „vermutlich nicht offen".
  Das Exposé schreibt in seinen Risiken selbst, Git-als-Archiv trage „nur
  Detektionen + Ausschnitte, nicht Rohstreams".
- **Synthetic Flood** (offene Frage 1): das Compute-Modell für Common Crawl — Teilkorpora
  lokal gegen AWS-Athena-Kosten, „Kostenrahmen nötig". Dazu Frage 3: Verhältnis zu
  The Consensus, „Kopplung oder strikte Trennung".
- **Compute Ground:** EU-Reporting-DB ungeprüft, nationale Genehmigungsregister
  fragmentiert und teils nicht maschinenlesbar („der ehrliche Hauptblocker") — und
  ausdrücklich die **Form**-Frage: kein Start ohne Form-These, nicht nur Evidenz
  (One-Tap-Lehre).

## 2. Was seit dem 2026-08-09 tatsächlich erlaubt ist

GCP darf **nur in Batch-Schritten der Pipelines** vorkommen, nie zur Laufzeit der Site;
Git bleibt das Archiv. Aktiviert sind **G1 BigQuery-GDELT** (live geprüft am 09.08.,
30,4 MB billed ≈ 0,003 % des monatlichen Freikontingents, 0 €) und **G5 Earth Engine
Sentinel-1** unter Null-Kosten-Vorbehalt und ausdrücklich **nur für den
Dark-Ocean-V1-Pfad**. Bedingungen je Schritt: Trace committen (Query, Job-ID, bytes
billed — zur Laufzeit erfasst, weil die Job-Historie nach 180 Tagen verfällt),
Lizenz-Notice der Quelle, Kostendisziplin mit Richtwert 10 €/Monat, Ausfälle vermerkt wie
bei jeder Quelle. Nicht aktiviert: G2/G3, G4/G6. §3 der Aktivierung nennt machine
attention ausdrücklich als vorgesehene Nutznießerin — die Erlaubnis gilt hier also.

Der G1-Pfad ist kein Papier: die Weltkammer von `/redaction` fährt ihn seit dem 2026-08-14
nächtlich mit ~20–26 MB billed und committeten Job-Traces. (Nebenbefund derselben
Krankheit wie die Parkzettel: der Kandidaten-Index des Labs sagt noch „awaits
`GCP_SA_KEY`", während die Tagesrekorde ab 14.08. `gdg.available: true` samt Traces
zeigen. Currency-Drift, eine Zeile Arbeit.)

## 3. Urteil je Kandidat

### Planetary Listening — Blocker **gefallen**, aber nicht durch GCP

GCP löst hier nichts: seismische Wellenformen kommen in der Aktivierungs-Karte nicht vor,
Earth Engine ist Raster und Dark Ocean V1 gewidmet. Gefallen ist der Blocker durch eigene
Bauarbeit **nach** dem 08.08.:

1. **Dark Ocean V0 (09.08.)** hat das Muster bewiesen: Szenen von 1,1–1,8 GB werden nie
   geholt; committet werden Katalogzeile, Herausgeber-Checksumme, Footprint, Zeit —
   *referenced, not stored*, keyless, prüfergezwungen, nächtlich. Die Wellenform-Frage hat
   exakt dieselbe Form.
2. **Der Aufnahme-Pfad** erlaubt seit dem 08.08. ein eigenes Repo, wenn die Datenform Git
   sprengt — benannter Beispielfall: Planetary Listening. Der Parkzettel stand gegen eine
   Regel, die ihn schon durchgelassen hätte.
3. Das Lab hat die Speicherfrage inzwischen ausgeschrieben (Spec „The Seismic Quiet",
   2026-08-14): immutables Tages-JSON aus abgeleiteten Werten, Stations-Metadaten und
   Netz-Zitat je Record, offengelegte Lücken, Baseline-Neustart bei Metadatenwechsel.

Das committete nächtliche Artefakt wäre demnach: Detektionsliste (Zeit, Station, Klasse,
Konfidenz), der **deterministische FDSN-Request** als Wiederholungsanweisung, SHA-256 der
empfangenen Bytes, und ein Wellenform-**Ausschnitt** um jede Detektion (Sekunden, ein
Kanal — Kilobytes, git-fähig). Treu zum Exposé? Weitgehend ja, es wollte selbst nur
„Detektionen + Ausschnitte". Ein reines Metriken-Archiv wäre **nicht** treu: VERIFY
versprach Originalbytes. Ehrliche Restschwäche: FDSN-Bytes sind nicht stabilitätsgarantiert
(Qualitätsrevisionen), und der Herausgeber beurkundet — anders als CDSE — nichts. Das ist
kein Defekt, sondern genau die Divergenz-Frage, für die die Kontinuitäts-Sonde schon läuft.

**Erste ehrliche Nachtzahl:** „Station X, 03:41:07 UTC, impulsives Ereignis,
Sprengsignatur, Konfidenz mittel." **Nacht 14:** ein Kalender — der Sprengrhythmus einer
benennbaren Anlage, und die Brüche darin. Ein Ort und eine Uhr, keine Überlappungsquote.
Nach dem Dark-Ocean-Review vom heutigen Tag ist genau das das Gegenmittel gegen C4.

### Synthetic Flood — Blocker **unberührt, faktisch verschärft**

Common Crawl liegt auf AWS S3; die Aktivierung autorisiert kein AWS-Budget und keinen
GCP-Ersatz. Schwerer: **§6.4 des Portfolio-Audits vom 2026-08-09 ist ein verifiziertes
Negativ für genau diese Klasse** — BREATHE eingefroren seit 2020-06-25,
`pmc_open_access_commercial` nur eine Teilmenge; für Korpusfragen bringt BigQuery wenig.
Der eine Teil, den G1 heute sofort trüge (Publikationsfrequenz-Anomalien,
Quellenkonzentration in GKG), ist der Teil, der mit The Consensus kollidiert, dessen
Längsschnitt-Baseline seit dem 09.08. auf demselben Pfad läuft: Duplikation, keine neue
Linie. Dazu die C4-Falle: die Kopfzahl ist eine Anteilsquote, und die Drift ist im Exposé
monatlich getaktet — ein 14-Nächte-Fenster kann die Hauptgröße nicht messen.
**Kein AUDIT, bis eine Nicht-GDELT-Achse benannt ist.**

### Compute Ground — Blocker **unberührt**

Kein Cloud-Dienst macht ein Genehmigungsregister maschinenlesbar, und keiner liefert eine
Form-These. G5 ist Dark Ocean V1 gewidmet, die Satellitenachse also auch nicht frei.
Nachtzahl heute: eine jahresaktuelle Differenz, die sich vierzehn Nächte lang nicht bewegt.

## 4. Was AUDIT verlangt (Stufe 2)

Muster ist das Dark-Ocean-Audit vom 2026-08-08: Go/No-Go je Quelle mit Live-Probes und
bezifferten Befunden, **Registrierungs-Disziplin** (keine Accounts angelegt — jede
Token-Pflicht wird als Befund dokumentiert, nicht umgangen), Lizenz-Architektur vor dem
Bau, Eskalationen als getrennte Ein-Klick-Entscheidungen, Ethik-Grenzen,
Flagship-oder-Instrument-Einschätzung, V0-Empfehlung mit Form-Vorbehalt, ein „Bewusst
nicht"-Abschnitt. Ausdrücklich **nicht**: V0 bauen, Bytes konservieren, Detektion
prototypisieren, Site anfassen. Die Aufnahme selbst bleibt Franks Gate. Der Drei-Wege-
Ausgang (Flagship · Instrument · RETIRED) gilt seit dem 09.08. für alle Kandidaten.

## 5. Empfehlung

**Planetary Listening ins AUDIT** — ein Audit kostet nichts, baut nichts und legt keinen
Account an. Die V0-Entscheidung gehört dahinter, nicht davor.

**Gegenargumente gegen die eigene Empfehlung, faires Gewicht:**

1. Das Lab hat mit „The Seismic Quiet" (2026-08-14) einen **hauseigenen Nachbarn** auf
   denselben FDSN-Netzen. Die USP-Pflicht verlangt, die Trennung (Lautstärke-Index gegen
   diskrete Ereignisdetektion) **vor** dem Audit zu schreiben, sonst entsteht ein zweites
   Lab-Instrument unter anderem Dach.
2. Das Exposé nennt sich selbst „investigativ dünner": der Weg von „Sprengung erkannt" zu
   einem gesellschaftlichen Befund braucht ein Genehmigungsregister — Compute Grounds
   Blocker im Kleinen.
3. Die Infraschall-Hälfte des Einzeilers fällt am Audit vermutlich weg (CTBTO). Der
   Einzeiler muss vorher umgeschrieben werden; das ist eine Form-, keine Datenfrage.
4. Ereignisdetektion in Kriegsgebieten kollidiert mit E-2 und braucht Latenz als
   Schutzprinzip — schriftlich, vor V0.

**Für die anderen zwei ist die Antwort „noch nicht", und sie bleibt datiert stehen:**
Synthetic Flood mit dem verifizierten Negativ §6.4 plus der Consensus-Duplikation,
Compute Ground unverändert bis zu einer Form-These. Was am 2026-08-08 als „wer seinen
Blocker zuerst löst, geht zuerst" formuliert wurde, hat damit einen Sieger — er hat seinen
Blocker nur nicht selbst gelöst, sondern von Dark Ocean geschenkt bekommen.
