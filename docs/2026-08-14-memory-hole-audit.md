# Memory Hole — Audit (Stufe 2 des Aufnahme-Pfads)

**Datum:** 2026-08-14 (Live-Probes 21:28–21:54 UTC) · **Status:** Audit abgeschlossen,
Empfehlung an Frank — **die Aufnahme selbst bleibt sein Gate**
**Exposé:** `docs/2026-08-08-kandidat-memory-hole.md` · **Muster:** Dark-Ocean-Audit vom
2026-08-08 · **Origin:** Editorial Deadline / The Redaction (frankbueltge.de,
`/redaction`, `pipelines/redaction/`) — läuft unverändert weiter, inklusive der seit
2026-08-14 produktiven zweiten Kammer (World Chamber)

## Einzeiler (aus dem Exposé, bestätigt)

> Was verändert die Macht an ihrer eigenen öffentlichen Vergangenheit?

---

## 1. Die Gretchenfrage zuerst: Abgrenzung im eigenen Haus

Bevor irgendeine Quelle geprüft wird, muss die Frage beantwortet sein, an der dieser
Kandidat scheitern kann: **Was kann Memory Hole, was das Haus nicht schon tut?**

### Was heute läuft

| | Gegenstand | Menge | Form |
|---|---|---|---|
| **Editorial Deadline, Kammer 1** | 32 kuratierte offizielle Seiten (WHO, UN, IPCC, EU-KOM, NASA, NOAA, EPA, CDC, BLS, State Dept, Census, White House, UK Gov, Bundesregierung, IEA) | 32 URLs/Nacht | Wayback-Before/After, Salienz-Ranking, **ein** Tagesexponat |
| **World Chamber, Kammer 2** (seit heute produktiv) | **Presse** — GDELTs Global Difference Graph | 2026-08-13: 776.955 `UNCHANGED_CONTENT`, 135.016 `PAGE_TEXTCHANGE`, 53.724 `PAGE_TITLECHANGE`, 16.610 `HTTP_REDIRECT`; davon **13.454 englische Titeländerungen** | Determinist. Trivialitätsfilter → `reframing` 5.674 / `replaced` 6.525 / `trivial` 790 / `update` 465, Register auf 3 gebunden; dazu die hauseigene, gestichprobte Löschrate (Wilson-CI, 451 separat) |

Belege: `frankbueltge.de/src/data/redaction/world/2026-08-14.json` (Zahlen oben wörtlich
daraus), Trace `world_gdg_titles_20260813_t1786732980`, 246.415.360 Bytes billed;
Code `pipelines/redaction/src/redaction/world/{gdg,triviality,selection,sample,recheck}.py`;
Workflow `.github/workflows/redaction.yml` (05:30 UTC, degradiert ehrlich ohne `GCP_SA_KEY`);
Spec inkl. beider Nachträge `docs/superpowers/specs/2026-08-14-editorial-deadline-world-chamber.md`.

### Was Memory Hole hinzufügen würde — und was davon trägt

| Behauptung des Exposés | Prüfung | Verdikt |
|---|---|---|
| **(a) Skalierung auf institutionelle Seiten** (32 → zehntausende) | Heute live belegt: CDX beantwortet **Domain-/Prefix-Abfragen**. `bundesnetzagentur.de` (`matchType=domain`, 5 Tage): 3.938 Captures über **1.052 verschiedene URLs** in *einer* Abfrage, 30,3 s. `climate.ec.europa.eu/` (`matchType=prefix`, 30 Tage): 4.231 Captures über **2.344 URLs**, 31,8 s. | **Trägt — aber nur in der Domain-Architektur.** Eine größere kuratierte Liste wäre Kammer 1 mit mehr Zeilen. |
| **(b) Semantische Ereignisse statt Wort-Diffs** | Kammer 1 rankt über `salience.score` — das misst *Gewicht von Signalen* (Zahl, Datum, Verpflichtungsverb, Negation, Eigenname), **nicht die Art der Änderung**. Eine Typisierung „Zahl rückwirkend geändert / Versprechen abgeschwächt / Verantwortung verschoben" existiert im Haus nirgends. Die World Chamber typisiert (`triviality.py`), aber über **Titel**, nicht über Fließtext, und über Presse, nicht Institutionen. | **Trägt.** Das ist der eigentliche neue Gegenstand. |
| **(c) Langzeitgedächtnis institutioneller Sprache** | Historische Tiefe ist da: `bafin.de` Startseite 57.164 Captures / 22.201 Digests, `rki.de` 46.808 / 44.037, `esma.europa.eu` 4.413 seit 2010-12-29, `bundesnetzagentur.de` 3.534 seit 2010-06-28. | **Trägt technisch** — ist aber eine Mengen-, keine Art-Erweiterung von (a). |
| **(d) Simultanität über Institutionen** | Rechnerisch geprüft: bei 250–500 kuratierten Seiten und der **gemessenen Kadenz** (7-Tage-Fenster 2026-08-07..15: 0–14 Captures je Seite, 0–7 verschiedene 200-Digests; mehrere Seiten **0 Captures in 7 Tagen**) liegt die nächtliche Änderungsmenge im einstelligen bis niedrig-zweistelligen Bereich. Simultanitäts-Statistik über Institutionen ist damit **nicht führbar**. | **Trägt nur in der Domain-Architektur** (tausende Seiten weniger Institutionen), nicht in der Listen-Architektur. |

### Verdikt der Abgrenzung

**Die Abgrenzung hält — aber nicht in der Form, die das Exposé beschreibt.**

Eine Memory Hole, die eine größere Watchlist nächtlich diffed, ist ehrlich benannt:
*Editorial Deadline mit mehr URLs*. Dafür gründet man kein Projekt, dafür erweitert man
den Origin. Was Memory Hole zu einer eigenen Untersuchung macht, sind **(b) semantische
Ereignis-Typisierung** und **(d) Simultanität** — und (d) ist ohne (a) in der
Domain-Form statistisch unmöglich.

Daraus folgt die schärfste Auflage dieses Audits (§7, Auflage 1): **V0 baut Domain-Scope
(viele Seiten weniger Institutionen), nicht eine längere Liste.** Wer die Liste
verlängert, hat den Origin erweitert und soll das auch so nennen.

**Umgekehrt gibt es echte Synergie, keinen Konflikt:** die World Chamber hat heute
Nacht genau die Bausteine produktiv gemacht, die Memory Hole braucht — die
Live-Nachprüfung mit Wilson-CI und offen ausgewiesenen `botwall`/`451`-Klassen
(`world/recheck.py`) und den versionierten, determinist. Klassifikator als Methodenkern
(`world/triviality.py`). Memory Hole erbt beides, statt es zu erfinden.

---

## 2. Quellen-Audit (Live-Probes 2026-08-14, 21:28–21:54 UTC, alle ohne Anmeldung)

| Quelle | Probe | Befund |
|---|---|---|
| **Wayback CDX, Einzel-URL, Vollhistorie** | 6 institutionelle Seiten, `fl=timestamp,statuscode,digest&limit=100000` | Alle HTTP 200. BMWE-Dossier Energiewende: **681 Captures / 194 Digests** (2022-03-01 → 2026-07-29), 34,3 s. Bundesnetzagentur-Start: **3.534 / 1.723** (seit 2010-06-28), 15,0 s. ESMA-Start: **4.413 / 1.806** (seit 2010-12-29), 50,8 s. ExxonMobil-Newsroom: **821 / 396** (297 Captures allein 2026), 6,4 s. RKI-Startseite: **46.808 / 44.037**, davon **25.267 × HTTP 404**. BaFin-Start: **57.164 / 22.201**. |
| **Wayback CDX, Einzel-URL, Produktionsform** | Origin-Parameter (`collapse=digest`, `limit=-40`), 10 URLs seriell, 0,6 s Pause | Alle 200, **198,2 s gesamt**, Einzelabfrage **2,3–46,6 s** (Mittel ≈19,2 s). Keine 429. |
| **Wayback CDX, Nebenläufigkeit** | dieselbe Form, 12 URLs, 4 parallel | **117,5 s** (≈9,8 s/URL, Faktor ≈2), **1 × HTTP 504** (`bmuv.de`). Keine 429 — der Dienst drosselt nicht, er ist *langsam und instabil*. |
| **Wayback CDX, Inkrement-Fenster** | 16 URLs über 5 Kategorien, `from=20260807&to=20260815`, 4 parallel | 126,0 s, **3 × HTTP 504 (19 %)** (`bmuv.de`, `oecd.org`, `about.google`). **Kadenz-Befund: 0–14 Captures je Seite in 7 Tagen; 0–7 verschiedene 200-Digests; sechs von sechzehn Seiten 0 Captures.** |
| **Wayback CDX, Domain-/Prefix-Scope** | 4 Institutionen | `bundesnetzagentur.de` (domain, 5 d): **3.938 Captures / 1.052 URLs**, 30,3 s. `climate.ec.europa.eu/` (prefix, 30 d): **4.231 / 2.344**, 31,8 s. `umweltbundesamt.de` (domain, 30 d): **0 Zeilen** — obwohl die Einzel-URL im 7-Tage-Fenster 4 Captures hat. `epa.gov` (domain, **1 Tag**) und `bafin.de` (domain, 30 d): **HTTP 504**. Die Form `climate.ec.europa.eu/*` lieferte 0, die Form mit Schrägstrich 4.231 — **Abfrageform ist hostabhängig und muss je Watchlist-Eintrag erprobt werden.** |
| **Live-Fetch der Originalseiten** | 7 Seiten, eigener UA | BMWE **301 → `bundeswirtschaftsministerium.de`** (Ressort-Umbenennung als Domainwechsel). Bundesnetzagentur/ESMA/ExxonMobil/BaFin: 200 (BaFin per Redirect auf `/DE/home_node.html`). **RKI `/DE/Home/homepage_node.html`: HTTP 404 live.** **bp.com: HTTP 403** (Seite *und* `robots.txt`). |
| **robots.txt** | 7 Hosts | Bundesnetzagentur: `Disallow: /SiteGlobals`. RKI: `Crawl-delay: 30`. BaFin: Standard-GSB-Sperren. ESMA: Drupal-Default. ExxonMobil erlaubt **ausdrücklich** `GPTBot`/`ChatGPT-User`/`OAI-SearchBot`. bp.com: 403 statt robots.txt. |
| **Origin-Code gegen Nicht-Watchlist-Seiten** | `redaction.{cdx,extract,textdiff,prose,salience}` **unverändert** gegen 5 institutionelle Seiten | Siehe Befund 1 und 2 unten — **zwei reproduzierte Falsch-Positiv-Klassen**. |
| **EDGI web-monitoring** | `api.monitoring.envirodatagov.org`, keyless | HTTP 200. **34.999 überwachte Seiten** (`meta.total_results`), Beispielseite `updated_at 2026-08-14T10:00:22Z` — **läuft heute**. Versions-Quelle `source_type: internet_archive`, Bytes gespiegelt auf `edgi-wm-archive.s3.amazonaws.com` mit `body_hash`, älteste Capture 1997-06-19. Tags: `agency:EPA` 44/100, DOI 14, HHS 9, FWS 5, CDC 5, NOAA 5, NIH 4, NASA 4 — **US-Bundesebene**. Kein globaler Änderungs-Feed: `/api/v0/changes` und `/annotations` → 404, `/pages/{uuid}/changes` → Timeout nach 30 s. Scanner-UI `noindex` (Analysten-Werkzeug). Repos aktiv (`web-monitoring-{crawler,ops,processing}` gepusht 2026-08-14). |
| **Internet Archive Save Page Now** | `POST /save` ohne Auth, 21:47:46 Z | **HTTP 401** `{"message":"You need to be logged in to use Save Page Now."}`. Doku: S3-Keys über `archive.org/account/s3.php`, **6 Captures/Minute** authentifiziert, 7 parallele Sessions. → Eskalationsklasse, nicht umgangen. |
| **EU Web Archive** (op.europa.eu) | Übersichtsseite + Archive-It-CDX | Existiert als **Bewahrung** (Publications Office seit 2018, Inhalte seit 1996), nicht als Änderungsmessung. `wayback.archive-it.org/all/timemap/cdx` → **HTTP 403** für unseren UA. API-Zugang **ungeklärt** — offener Punkt, nicht behauptet. |
| **GDG / BigQuery** | **nicht neu geprobt** (Vorgabe) | Im Haus seit 2026-08-14 produktiv bewiesen; Zahlen und Trace siehe §1. |

**Registrierungs-Disziplin eingehalten:** keine Accounts angelegt, keine Keys erzeugt,
keine fremden Datenbestände gespiegelt (EDGI nur Metadaten-Abfragen). Jede Auth-Pflicht
ist als Befund dokumentiert.

---

## 3. Die sechs Kernbefunde

### 1. Der Origin publiziert heute Falsch-Positive — und Memory Hole würde sie skalieren

Der Origin-Code, unverändert gegen das BMWE-Dossier Energiewende laufen gelassen,
meldet: `kind=removal`, 19 Prosa-Passagen, **270 Tokens entfernt**, Salienz **20**
(Signale: `commitment_verb`, `date`, `named_entity`, `negation`, `number`) — inhaltlich
der Absatz zur Systementwicklungsstrategie und zur Klimaneutralität bis 2045. Ein
Tagesexponat erster Güte.

Nachgeprüft ist es **eine Lüge im Archiv**: Der „danach"-Snapshot vom 2026-05-28
enthält 118.410 Bytes HTML, aus denen die Extraktion acht Tokens gewinnt:

> `Verifying your browser before proceeding... Incident ID: e4841cb0-dxzu-4858-bcd7-154223367ef4`

Die WAF des Ministeriums hat dem Crawler eine Challenge-Seite serviert, und Wayback hat
sie **mit HTTP 200** archiviert. Unser eigener Live-Abruf bekommt dieselbe Seite
(118.413 Bytes, 8 Tokens). Es wurde nichts entfernt; es wurde nichts erfasst.

**Das ist kein Memory-Hole-Problem, das ist ein Origin-Befund von heute Nacht.** Bei 32
handverlesenen, überwiegend WAF-freien Seiten fällt es selten an. Bei deutschen
Bundesseiten (Akamai/Imperva-Schutz) ist es der Normalfall, und bei 1.000+ Seiten wird
es systematisch.

### 2. „Deletion" ist im Origin-Code nicht nachgeprüft — und BaFin beweist es

`cdx.py::_is_dead` wertet **jedes 4xx** der jüngsten Capture als Löschung. Die BaFin-Probe:
jüngste Capture `20260812142910` mit Status **403** → `kind=deletion`. Der Replay liefert
146 Bytes nginx-403; die BaFin ist live und antwortet 200. Zusätzlich bestand der
extrahierte „Vorher"-Text aus dem **Cookie-/Matomo-Hinweis** (69 Tokens) und passierte
mit Salienz **14** das Salienz-Gate, das genau solches Boilerplate abfangen soll.

Zwei Konsequenzen: (a) jede Löschbehauptung braucht eine **Live-Nachprüfung** — der Code
dafür existiert im Haus bereits (`world/recheck.py`: `classify_code`, `wilson`,
`botwall`/`legal_451` als offen ausgewiesene, aus dem Nenner genommene Klassen);
(b) das Salienz-Gate schützt nicht gegen Consent-Banner, weil deren Sprache
(„können", „dürfen", Eigennamen) genau die gewichteten Signale trägt.

### 3. Digest-Rauschen ist gelöst, Seitentyp-Rauschen nicht

Die ExxonMobil-Probe: zwei Captures **acht Sekunden** auseinander, verschiedene Digests,
**identischer extrahierter Text** → 0 entfernte Passagen. Die Text-Diff-Ebene absorbiert
Digest-Churn zuverlässig; das im Exposé benannte „HTML-Rauschen-Kernproblem" ist
tatsächlich gelöst.

Ungelöst ist der Seitentyp. Die ESMA-Probe liefert eine **echte** Entfernung, 76 Tokens:

> „ESMA sets out actions to simplify the retail investor journey … ESMA will focus on three areas …"

Das ist kein Rückzug einer Zusage, das ist ein Teaser, der von der Startseite gerollt
ist. **Startseiten, News-Indizes und Übersichtsseiten sind für dieses Instrument
untauglich** — Memory Hole braucht Inhalts-, Policy- und Fact-Sheet-Seiten. Das ist eine
Methodenanforderung, keine Präferenz.

### 4. Das Feld ist US-seitig besetzt — und außerhalb der USA praktisch leer

**EDGI ist kein historisches Prior Art, sondern ein laufender Konkurrent:** 34.999
überwachte Seiten, heute aktualisiert, öffentlich lesbare API ohne Schlüssel, Bytes
gespiegelt, Versionen bis 1997, dazu der **Federal Environmental Web Tracker** —
öffentlich, durchsuchbar, wöchentlich aktualisiert. Daneben Sunlights **Web Integrity
Project** (seit 2018) und **Gov404**, **Tracking Gov Info** (UMN), `govinfowatch.net`.
Größenordnung des Gegenstands dort: seit Januar 2025 **über 8.000** entfernte oder
substanziell geänderte Bundesseiten (CDC über 3.000, Census ~3.000).

Die Recherche fand **kein Äquivalent** für die deutsche Bundesebene, **keines** für
EU-Regulierer (das EU Web Archive bewahrt, es misst nicht) und **keines** für Konzerne.
Der Konzern-Fall ist dabei nachweislich relevant und unbesetzt: Google hat seine
Netto-Null-Zusage von der Nachhaltigkeitsseite entfernt (National Observer, 2025-09-04),
BP und Shell haben Zusagen abgeschwächt — dokumentiert **journalistisch, per
Wayback-Handarbeit, im Einzelfall**. Der Net Zero Tracker verfolgt *Zusagen*, nicht
deren *Verschwinden*.

**Konsequenz für die USP-Pflicht:** Die Daylight liegt in **Jurisdiktion (DE/EU/Konzerne)
+ Form (typisierte Ereignisse als tägliches Register)**, nicht in der Fähigkeit. EDGIs
technische Tiefe ist heute größer als das, was eine V0 leisten wird — das gehört so ins
Methodenblatt. Eine Ausweitung auf US-Bundesumwelt-/Gesundheitsseiten wäre Duplikat und
ist ausgeschlossen (Ausnahme: eine kleine US-Stichprobe als *Kalibrierung gegen EDGI*,
ausdrücklich als solche deklariert).

### 5. Die Kadenz ist die eigentliche physikalische Grenze

Über sieben Tage (2026-08-07..15) bekamen die geprobten institutionellen Seiten **0 bis
14 Captures**, mit **0 bis 7** verschiedenen 200-Digests; sechs von sechzehn Seiten
**null**. Wayback crawlt diese Seiten wöchentlich bis nie.

Ein „nächtliches" Instrument auf passiver Wayback-Basis ist nächtlich **im Protokoll**,
nicht in der Auflösung. Drei ehrliche Wege: (a) die Kadenz benennen und das Nichts als
Messwert committen; (b) **Save Page Now** — eigene Captures im öffentlichen Archiv, 6/min
authentifiziert → 360/h, für 300 Seiten ≈50 min/Nacht, kostet einen kostenlosen
archive.org-Account (Franks Klick); (c) eigene Live-Captures ins Repo — funktioniert,
verlagert aber die Provenienz vom Dritt-Archiv ins eigene Haus und schwächt genau die
Beweiskraft, die den Origin trägt. **Empfehlung: (a) für V0, (b) als Eskalation, (c) nicht.**

### 6. Die Infrastruktur ist langsam und flattert — das muss ins Budget

Kein einziges 429 in ~60 Abfragen; dafür Latenzen von **1,3 s bis 60 s** und eine
504-Quote von **19 %** bei Nebenläufigkeit 4. Hochgerechnet: 300 Einzel-URLs seriell
≈100 min, bei Nebenläufigkeit 4 ≈50 min; die Domain-Architektur ersetzt das durch
wenige Abfragen à 30 s — plus die Snapshot-Abrufe der geänderten Seiten (gemessen
3,5–11,9 s für zwei Snapshots). Der Retry-Pfad in `cdx.py` (drei Versuche, 1/2/4 s)
ist notwendig und ausreichend; das nächtliche Zeitbudget ist mit **1–3 h** anzusetzen,
nicht mit Minuten.

---

## 4. Watchlist-Vorschlag: „wessen Gedächtnis?"

Die redaktionelle Entscheidung liegt bei Frank. Vorschlag, begründet, kuratierbar,
Größenordnung V0: **250–350 Seiten plus 20 Kontrollseiten** — in der Domain-Architektur
verteilt auf **wenige Institutionen mit vielen Seiten**, nicht viele Institutionen mit
je einer Seite.

| # | Kategorie | Beispiel-Hosts | Umfang | Begründung / Warnung |
|---|---|---|---|---|
| **A** | **Deutsche Bundesebene** | `bundeswirtschaftsministerium.de`, `bundesgesundheitsministerium.de`, `bmuv.de`, `rki.de`, `umweltbundesamt.de`, `destatis.de` | 80–120 | Weltweit unbesetzt; Sprach- und Rechtsnähe des Hauses. **Warnung:** WAF-Challenges (BMWE, Befund 1), `bmuv.de` in zwei Proben 504, `umweltbundesamt.de` liefert im Domain-Scope 0 Zeilen — je Host erproben. RKI beweist mit 25.267 archivierten 404 und einer heute toten Startseite, dass hier real gelöscht wird. |
| **B** | **EU-Regulierer und Kommission** | `climate.ec.europa.eu`, `esma.europa.eu`, `eba.europa.eu`, `eiopa.europa.eu`, `ema.europa.eu`, `acer.europa.eu` | 80–120 | Prefix-Scope **bewiesen** (climate.ec.europa.eu: 2.344 URLs in einer Abfrage). Zweitquelle EU Web Archive offen. Regulierer publizieren Fristen, Schwellen, Zahlen — genau das Material der Ereignistypen. |
| **C** | **Deutsche Regulierer/Aufsicht** | `bundesnetzagentur.de`, `bafin.de`, `bundesbank.de` | 40–60 | Domain-Scope bei Bundesnetzagentur **bewiesen** (1.052 URLs), bei BaFin **504** → dort Prefix-Partitionierung. |
| **D** | **Konzerne mit öffentlichen Selbstverpflichtungen** | `sustainability.google`, `corporate.exxonmobil.com`, `shell.com`, `volkswagen-group.com`, `basf.com`, `bayer.com` | 40–60 | **Die größte Daylight-Lücke** (Befund 4). **Warnung:** Bot-Walls — `bp.com` antwortet unserem Client mit 403 auf Seite *und* robots.txt; solche Hosts kommen als `unverifiable` in den Record, nicht als Löschung. Politisch die exponierteste Kategorie: E-2 gilt hier am schärfsten. |
| **E** | **Kontrollgruppe (Pflicht, kein Beiwerk)** | ~20 Seiten ohne Verpflichtungscharakter: Kontaktseiten, Impressen, statische Rechtstexte, quer über A–D | 20 | Misst die **Falsch-Positiv-Rate des Instruments an sich**. Jedes Ereignis auf einer Kontrollseite ist per Konstruktion ein Fehler des Verfahrens. Ohne diese Gruppe ist die E-Experiment-Bedingung in §8 nicht messbar. |

**Ausgeschlossen:** US-Bundesumwelt- und -gesundheitsseiten (EDGI-Duplikat, Befund 4) und
alles, was Kammer 1 bereits beobachtet (WHO, UN, IPCC, NASA, NOAA, EPA, CDC, BLS,
State Dept, Census, White House, UK Gov, IEA, Bundesregierung-Klimaschutz) — der Origin
behält seine 32 Seiten unangetastet, Memory Hole doppelt keine davon.

**Optional, deklariert:** ~20 EDGI-überwachte US-Seiten als **Kalibrierungsstichprobe** —
misst unsere Ereignistypisierung gegen einen fremden, laufenden Bestand. Das ist
Nachprüfbarkeit, nicht Duplikat.

---

## 5. Kostenrahmen der semantischen Schicht

Deterministische strukturelle Diffs bleiben das kostenlose Fundament. Die semantische
Schicht ist optional und gestuft. Preise recherchiert am 2026-08-14 über die
Claude-API-Referenz des Hauses:

- **Claude Haiku 4.5** (`claude-haiku-4-5`), Default für diese Aufgabe: **1,00 $ / 1 Mio.
  Input-Token**, **5,00 $ / 1 Mio. Output-Token**, Kontextfenster 200 K.
- **Batch-API: 50 % Rabatt** auf alle Token (Latenz bis 24 h — für einen nächtlichen
  Lauf irrelevant, also Pflicht).
- **Prompt-Caching greift hier nicht:** Der minimal cachefähige Präfix liegt bei Haiku 4.5
  bei **4.096 Token**; ein Klassifikations-Systemprompt von ~600 Token bleibt darunter und
  cacht **still** nicht. Das gehört genannt, damit niemand Cache-Ersparnis einplant.

**Mengengerüst aus den Proben** (nicht geschätzt, hergeleitet): 300 Seiten × gemessene
0–7 geänderte 200-Digests je Woche ≈ 20–25 geänderte Captures/Nacht; davon überleben
nach Text-Diff und Prosa-Filter erfahrungsgemäß 30–50 % (ExxonMobil-Befund: Digest ≠
Text) → **≈7–12 Klassifikationen/Nacht**. Planungsansatz großzügig: **30/Nacht**.

| Szenario | Klassifikationen/Nacht | Token je Klassifikation | Kosten/Nacht | Kosten/Monat | Mit Batch (−50 %) |
|---|---|---|---|---|---|
| **V0, realistisch** | 30 | 2.000 in / 300 out | 0,105 $ | ≈3,15 $ | **≈1,60 $ ≈ 1,50 €** |
| V0, Spitzennacht | 60 | 3.000 in / 400 out | 0,30 $ | — | — |
| **Stress (Domain-Scope, 500+ Seiten)** | 100 | 6.000 in / 800 out | 1,00 $ | ≈30 $ | ≈15 $ |

**Der Regelbetrieb liegt bei ein bis zwei Euro im Monat — die Kostendisziplin des Hauses
(Richtwert 10 €/Monat) ist mühelos eingehalten. Die Gefahr ist nicht der Preis, sondern
die Skalendrift:** das Stress-Szenario reißt den Richtwert. Deshalb Auflage 4: **harte
nächtliche Obergrenze** (Vorschlag 40 Klassifikationen), Batch-API, committeter
Token-/Kosten-Trace je Nacht, und ehrliche Degradierung beim Anschlagen der Grenze
(„n Kandidaten unklassifiziert, Grenze erreicht") statt stillem Abschneiden.

**Trace-Pflicht** wie bei jedem KI-Schritt des Hauses: Modell-ID, Prompt-Version,
Verfahren offengelegt; jedes Modell-Verdikt trägt `estimated: true` und wird nie als
Feststellung geführt. Der Record steht auch ohne die semantische Schicht.

---

## 6. V0-Skizze: „Der institutionelle Wortlaut, nachgeprüft"

Kleinster Slice, der nächtlich committete, `verify.py`-prüfbare Records erzeugt —
im Praxis-Substrat, ohne einen einzigen Account.

**Nächtlich, für den abgeschlossenen UTC-Tag:**

1. **Erfassen (Domain-Scope).** Je Institution eine CDX-Abfrage in erprobter Form
   (`matchType=domain` oder `prefix` mit Host+Schrägstrich, `from`/`to` = Vortag), Antwort
   **als Bytes konserviert** in `memoryhole/snapshots/<tag>/` mit Manifest — nach dem
   Dark-Ocean-Muster (`darkocean/snapshots/<tag>/manifest.json`, 3,3 MB für sechs Tage;
   Textkorpora sind kleiner als Geodaten, Git-als-Archiv trägt).
2. **Seiten-Gültigkeitsgate (das eigentlich Neue).** Eine Capture zählt nur als Seite, wenn
   (a) `statuscode == 200`, (b) extrahierter Haupttext ≥ Mindestlänge, (c) **kein
   Challenge-/Interstitial-Fingerabdruck** („Verifying your browser", „Incident ID",
   „Attention Required", „Just a moment"), (d) nicht überwiegend Consent-/Nav-Boilerplate.
   Alles andere → Klasse `unverifiable`, **gezählt und ausgewiesen, nie gediffed**.
   Befunde 1 und 2 sind die Existenzberechtigung dieses Schritts.
3. **Deterministisch diffen.** `textdiff.removed` → `prose.keep_prose` → `salience.score`,
   unverändert aus dem Origin.
4. **Ereignisse typisieren — determinist. zuerst.** Regelbasierter, versionierter
   Klassifikator nach dem Muster von `world/triviality.py`:
   `number_revised` (Zahlpaare vorher/nachher), `date_shifted`, `commitment_removed`
   (das Signal `commitment_verb` existiert in `salience.py` bereits), `negation_flipped`,
   `attribution_removed`. **Die Modell-Schicht läuft nur dort, wo die Regeln sich
   enthalten** — gedeckelt, im Batch, als Schätzung markiert.
5. **Löschungen live nachprüfen.** Jede 4xx-Capture geht durch `recheck.py`-Logik
   (`classify_code`, `wilson`, `botwall`/`legal_451` außerhalb des Nenners), bevor das
   Wort „gone" im Record erscheint.
6. **Committen.** `memoryhole/readings/<tag>.json`: je Eintrag
   `unchanged | changed | unverifiable | gone`, dazu die typisierten Ereignisse, dazu die
   Raten mit Wilson-CI, dazu der Kosten-/Token-Trace. **Auch eine Nacht ohne Fund wird
   geschrieben** — „nichts geschehen" ist ein Messwert (Befund 5).
7. **`verify.py::check_memoryhole`.** Jede Lesung wird aus den konservierten Bytes
   nachgerechnet — exakt wie `check_darkocean` und `check_reaction`.

**Code-Erbe, explizit benannt:**

| Übernommen aus | Was | Änderung |
|---|---|---|
| `redaction/cdx.py` | `captures`, `snapshot_url`, `permalink`, Retry, `_redacted` | **`classify` wird korrigiert**: 4xx ist Löschungs-*Kandidat*, nicht Löschung (Befund 2) |
| `redaction/salience.py` | `WEIGHTS`, Signalregexe, versionierte Bewertung — symbolisch, kein LLM | unverändert; ergänzt um das Gültigkeitsgate davor |
| `redaction/{textdiff,prose,extract}.py` | Satz-Diff, Prosa-Filter, trafilatura-Extraktion mit stdlib-Fallback | unverändert |
| `redaction/world/recheck.py` | `classify_code`, `wilson`, Offenlegungsklassen, 451-Titel nur als SHA-256 | direkt anwendbar |
| `redaction/world/triviality.py` | versionierter, determinist. Klassifikator als **Methodenkern-Muster** | Vorbild, nicht Kopie (Titel → Fließtext) |
| `practice/` | `fetch.Client` (1,2 s Mindestabstand, Backoff, Redaktion), `preserve.{sha256,Snapshot,write_json}`, `autonomy.append` | unverändert — das ist der Substrat-Stresstest |

**Der Substrat-Stresstest ist Zweck, nicht Unfall:** `practice/fetch` und `preserve`
sind gegen JSON-APIs gewachsen; hier treffen sie auf HTML-Korpora, Extraktions-Heuristik
und Snapshot-Familien mit hunderten Dateien pro Nacht. Was bricht, wird als
Substrat-Befund committet.

---

## 7. Ethik-Grenzen (verschärft gegenüber dem Origin)

- **E-2 bleibt scharf.** „Institution X vertuscht" ist keine Ausgabe. Publiziert werden
  dokumentierte Änderungen mit Bytes, Zeitstempeln und zwei Klicks Nachprüfbarkeit. Die
  Ereignistypen (`commitment_removed`, `number_revised`) benennen **Operationen am Text**,
  keine Absichten. Die Konzern-Kategorie D ist hier am exponiertesten und bekommt die
  Formulierungsdisziplin ausdrücklich ins Methodenblatt.
- **I8, natürliche Personen — hier nicht trivial.** „Verantwortung verschoben" heißt
  praktisch oft: ein Name oder eine Rollenzuschreibung ist verschwunden. Regel: der Name
  bleibt in den konservierten Bytes als Beweis, wird aber **nicht zum Gegenstand des
  Records**; typisiert wird das Ereignis (`attribution_removed`), nicht die Person.
  Keine Personen-Ranglisten, keine Namen in Registerzeilen.
- **Unsicherheit wird gezeigt, nicht versteckt.** `unverifiable` (Bot-Wall,
  WAF-Challenge, Serverfehler) ist eine **veröffentlichte Zahl**, keine Lücke. Genau so
  hält es die World Chamber mit `botwall` und `451`.
- **Kein Backfill.** Wie im ganzen Haus: keine rückdatierten Records, keine nachträglich
  „reparierten" Nächte. Korrekturen überschreiben sichtbar.

---

## 8. Was das E-Experiment messen müsste (vorab committete Kriterien)

Vierzehn Nächte. Die Kriterien werden **vor** der ersten Nacht committet; ein Null-Ergebnis
ist ein Ergebnis.

1. **Falsch-Positiv-Rate.** Anzahl publizierter Ereignisse auf der Kontrollgruppe E.
   **Bar: 0.** Jedes Ereignis dort ist ein Verfahrensfehler.
2. **Gültigkeitsgate.** Anteil `unverifiable` je Kategorie, und: **null** publizierte
   Records, die auf Challenge-, Consent- oder Bot-Wall-Seiten beruhen (Befunde 1/2).
3. **Ertrag.** Nächte mit ≥1 validiertem semantischem Ereignis. Vorschlag Bar: **≥4 von 14**.
   Darunter ist es kein tägliches Instrument, sondern ein Langzeit-Sammler — dann
   ehrlich als Instrument mit Wochenkadenz führen oder RETIRED.
4. **Löschbehauptungen.** Wie viele 4xx-Kandidaten überleben die Live-Nachprüfung? Diese
   Zahl misst zugleich, wie groß der Origin-Bug (Befund 2) heute wirklich ist.
5. **Determinismus gegen Modell.** Übereinstimmung der Regelschicht mit der Modellschicht
   auf der Schnittmenge. **Kein Ereignistyp darf allein aus dem Modell stammen** — sonst ist
   der Record ein Orakel.
6. **Simultanität (die eigentliche Hypothese).** Verschwindet innerhalb der 14 Nächte
   dieselbe Formulierung von ≥3 Seiten aus ≥2 Institutionen? Schwelle vorab registriert;
   **ein Null-Befund ist publizierbar** und entscheidet über (d) aus §1.
7. **Kosten.** Tatsächliche €/Nacht gegen die Obergrenze; Nächte mit Deckel-Anschlag.
8. **Laufzeit und Ausfälle.** Nächtliche Laufzeit, 504-Quote, Nächte mit
   unvollständigem Erfassungslauf.
9. **Substrat.** Was in `practice/` gebrochen ist — als Befund, nicht als Panne.

---

## 9. Ehrliche Grenzen dieses Kandidaten

- **Auflösung ≠ Kadenz.** Wayback crawlt institutionelle Seiten wöchentlich bis nie
  (0–14 Captures/7 Tage, sechs von sechzehn Seiten null). „Nächtlich" ist die Protokoll-,
  nicht die Beobachtungsfrequenz — solange SPN nicht eskaliert wird.
- **Die Infrastruktur ist unzuverlässig.** 19 % 504 bei Nebenläufigkeit 4; Domain-Scope
  scheitert an großen Hosts (`epa.gov` selbst für einen Tag: 504) und ist in der
  Abfrageform hostabhängig (`umweltbundesamt.de` domain: 0 Zeilen trotz vorhandener
  Captures). Jeder Watchlist-Eintrag braucht eine erprobte Abfragestrategie — das ist
  Kuratierungsarbeit, keine Konfiguration.
- **Extraktion bleibt Heuristik.** trafilatura zieht Consent-Banner, Teaser und
  Navigationsreste mit; Salienz filtert sie nicht zuverlässig heraus (BaFin: Cookie-Text,
  Salienz 14).
- **„Entfernt" ≠ „geschwärzt".** ESMA zeigt eine echte Entfernung, die nur ein rotierender
  Teaser ist. Ohne Seitentyp-Disziplin misst das Instrument Redaktionsalltag.
- **EDGI ist technisch heute tiefer.** 34.999 Seiten, gespiegelte Bytes, Versionen ab 1997,
  öffentlicher Tracker. Memory Hole gewinnt über Jurisdiktion und Form, nicht über
  Fähigkeit — und das gehört so ins Methodenblatt, nicht kleingeredet.
- **Die Simultanitäts-These ist unbewiesen** und kann am Ende der 14 Nächte schlicht
  falsch sein. Dann bleibt ein solides Instrument, kein Flagship.
- **Die Abgrenzung ist dünn, wenn V0 die Architektur verfehlt.** In der Listen-Form ist
  Memory Hole der Origin mit mehr Zeilen. Das ist die realistischste Art, wie dieses
  Projekt scheitert.

---

## 10. Flagship oder Instrument?

Die vier Flagship-Kriterien, geprüft:

| Kriterium | Befund |
|---|---|
| dringlich | ✅ — RKI-Startseite heute 404, 25.267 archivierte 404; >8.000 US-Bundesseiten seit 2025; Google entfernt Netto-Null-Zusage |
| maschinell überlegen | ✅ — 2.344 URLs je Abfrage, Jahre über Jahrzehnte diffen, Simultanität erkennen: formal notwendig maschinell |
| historisch tief | ✅ — 2010+ je Seite, 3.534–57.164 Captures |
| **kontinuierlich lebendig** | ⚠️ — **das ist die Schwachstelle.** Die gemessene Kadenz erzeugt Nächte ohne Fund. Ohne SPN ist tägliche Bühnenpräsenz nicht ehrlich zu bespielen. |
| ästhetisch stark | ✅ — „eine Oberfläche aus gelöschter Sprache" trägt; Corrections überschreiben sichtbar |

**Empfehlung: Instrument**, mit Beförderungsoption zum Flagship, wenn das E-Experiment
Kriterium 6 (Simultanität) *und* Kriterium 3 (Ertrag ≥4/14) besteht. Dagegen spricht auch
die Hauslage: The Foreknown hält die Bühne, Dark Ocean ist der Flagship-Kandidat; ein
zweiter wäre ein Scope-Problem, kein Gewinn.

---

## 11. Go/No-Go

**GO für eine V0 „Der institutionelle Wortlaut, nachgeprüft" — mit sieben Auflagen.**
Ausdrücklich **kein** GO für die V0, die das Exposé beschreibt (größere Watchlist,
gleicher Diff): die wäre eine Origin-Erweiterung und gehört dann auch dorthin.

1. **Domain-Scope statt längerer Liste.** Die Architekturentscheidung wird im V0-Design
   festgeschrieben, nicht nachträglich. Je Institution eine erprobte Abfragestrategie
   (`domain` / `prefix` / Einzel-URL-Fallback), dokumentiert mit dem Probe-Ergebnis, das
   sie rechtfertigt. Ohne diese Auflage fällt die Abgrenzung aus §1 in sich zusammen.
2. **Seiten-Gültigkeitsgate vor dem ersten Diff.** Kein Record verlässt die Pipeline,
   bevor Challenge-, Consent- und Bot-Wall-Seiten als `unverifiable` abgefangen sind. Die
   Falsch-Positiv-Rate auf der Kontrollgruppe wird als Zahl committet. Belege: Befunde 1/2.
3. **Live-Nachprüfung jeder Löschbehauptung**, mit den Offenlegungsklassen und dem
   Wilson-CI aus `world/recheck.py`. „gone" ist eine geprüfte Aussage, keine CDX-Zeile.
4. **Semantik gestuft und gedeckelt.** Regelschicht zuerst; Modellschicht nur bei
   Enthaltung der Regeln, im Batch, mit harter Nachtgrenze (Vorschlag 40), committetem
   Token-/Kosten-Trace, `estimated: true` an jedem Modell-Verdikt und ehrlicher
   Degradierung beim Anschlag.
5. **Der Origin bleibt unangetastet — und bekommt etwas zurück.** Keine Watchlist-Migration,
   kein Fork. Die zwei heute Nacht gefundenen Fehler (4xx-Löschung ohne Nachprüfung;
   WAF-Challenge als 200 archiviert) werden **im Origin** als eigener PR gefixt, bevor
   Memory Hole sie erbt. Das ist die Gegenleistung dieses Audits ans Haus.
6. **Kadenz-Ehrlichkeit.** Jede Nacht schreibt einen Record, auch den leeren. Die
   SPN-Eskalation ist eine getrennte Ein-Klick-Entscheidung Franks; die V0 wartet nicht
   auf sie.
7. **Simultanität ist E-Experiment-Hypothese, kein V0-Versprechen.** Weder Site noch
   Methodenblatt behaupten sie, bevor Kriterium 6 aus §8 entschieden ist.

**Kein V0-Bau ohne Franks ausdrückliches Go** — Aufnahme ist das menschliche Gate
(E-4/E-6). Dieses Audit endet hier.

---

## 12. Offene Entscheidungen (Frank)

1. **Go für V0 in der Domain-Scope-Form?** (Listen-Form wäre eine Origin-Erweiterung —
   auch ein zulässiges, billigeres Ergebnis.)
2. **Watchlist:** Kategorien A–E wie vorgeschlagen? Insbesondere: **Konzerne (D) ja oder
   nein** — größte Daylight-Lücke, größte Exposition, meiste Bot-Walls.
3. **Eskalation:** kostenlosen **archive.org-Account für Save Page Now** anlegen
   (6 Captures/min → eigene Captures im *öffentlichen* Archiv, Provenienz bleibt beim
   Dritten)? Ohne ihn bleibt die Auflösung bei „wöchentlich bis nie".
4. **Semantische Schicht:** Modell-Calls ja/nein — und wenn ja, welche Nachtgrenze?
   (Vorschlag 40 → ≈1,50 €/Monat mit Batch.)
5. **Klasse:** **Instrument** (Empfehlung) oder Flagship-Kandidat?
6. **Origin-Fix vorziehen?** Die zwei Bugs aus Befunden 1/2 betreffen die 32 heute
   laufenden Seiten — Fix sofort, unabhängig von der Memory-Hole-Entscheidung?

---

## 13. Bewusst nicht (in diesem Audit)

Keine Accounts angelegt (SPN-401 dokumentiert, nicht umgangen) · keine Keys erzeugt ·
kein Code geschrieben und nichts committet · keine Watchlist festgeschrieben ·
GDG/BigQuery nicht neu geprobt (Hausbeleg zitiert) · keine EDGI-Daten gespiegelt (nur
Metadaten-Abfragen) · keine Modell-Calls für dieses Audit (die Kostenrechnung ist
hergeleitet, nicht erprobt) · keine Site- oder Bühnen-Änderung (Öffentlichkeit erst ab
RUNNING) · EU-Web-Archive-API als offene Frage stehen gelassen statt behauptet.
