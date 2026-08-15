# Memory Hole V0 — Der institutionelle Wortlaut, nachgeprüft (gebaut)

**Datum:** 2026-08-15 (Bau in der Nacht 14./15., Live-Lauf 2026-08-14 23:0x UTC) ·
**Stufe:** V0 des Aufnahme-Pfads · **Klasse:** Instrument ·
**Grundlage:** [`2026-08-14-memory-hole-audit.md`](2026-08-14-memory-hole-audit.md)
(GO mit sieben Auflagen) · **Origin:** Editorial Deadline / The Redaction
(frankbueltge.de, `/redaction`) — läuft unverändert weiter

## Franks Entscheidungen (protokolliert)

Das Go kam in der Nacht zum 2026-08-15, im Wortlaut:

> „[Wortlaut privat]"

Damit sind, wie im Audit zur Entscheidung gestellt:

1. **GO für die V0 in Domain-Scope-Architektur** (Auflage 1). Eine längere
   kuratierte Liste ist ausdrücklich *nicht* dieses Projekt — die wäre eine
   Origin-Erweiterung und gehörte dorthin.
2. **Watchlist-Kategorien A–E wie vorgeschlagen, einschließlich D (Konzerne)** —
   mit der verschärften E-2-Formulierungsdisziplin. Bot-verriegelte Hosts
   (bp.com, 403) kommen als `unverifiable` in den Record, nie als Befund.
3. **Klasse: Instrument.** Keine Bühne, kein Produktionsdruck.
4. **Modellschicht: ja** — harte Nachtgrenze 40 Klassifikationen, Batch-API,
   `estimated: true` an jedem Modell-Verdikt, committeter Token-/Kosten-Trace,
   ehrliche Degradierung beim Anschlag. Regeln zuerst; das Modell sieht nur,
   wovon die Regeln sich enthalten.
5. **SPN-/archive.org-Account: nicht jetzt.** Die V0 committet leere Nächte
   ehrlich (Auflage 6).
6. **Alle sieben Auflagen aus §11 des Audits sind bindend.**

## Was die V0 tut (nächtlich, 02:30 UTC, vollständig keyless)

Für den abgeschlossenen UTC-Tag stellt die Maschine je Institution **eine**
erprobte CDX-Abfrage — `matchType=domain` oder `prefix`, HTML-gefiltert, eine
Zeile je URL — und bekommt damit die Seiten, die das Archiv an diesem Tag
angefasst hat: nicht eine Handvoll kuratierter Adressen, sondern hunderte bis
tausende je Host. Aus dieser Menge zieht sie eine **deterministische Stichprobe**
(`sha256(tag|url)`, aufsteigend), damit die Raten etwas bedeuten und die
Ziehung von jedem nachvollzogen werden kann, der die konservierten Bytes hat.

Für jede gezogene Seite und jede Kontrollseite holt sie die Digest-Historie in
der Produktionsform des Origins (`collapse=digest`, `limit=-40`) und liest
daraus **vier** Klassen:

| Klasse | wann |
|---|---|
| `unchanged` | am Tag kein neuer Digest — die Aufnahme sagte, was schon dastand |
| `changed` | neuer 200-Digest am Tag, **und beide Aufnahmen haben das Gültigkeitsgate passiert** |
| `unverifiable` | Gate gescheitert, Archiv-3xx/5xx, kein Vorher, Fetch-Deckel erreicht, oder ein Löschkandidat, der die Live-Nachprüfung überlebt hat |
| `gone` | 4xx im Archiv **und** live 404/410 |

**Das Gültigkeitsgate ist das eigentlich Neue** und die Existenzberechtigung des
Projekts gegenüber dem Origin. Eine Aufnahme zählt nur als Seite, wenn
(a) Status 200, (b) der extrahierte Haupttext eine Mindestlänge erreicht,
(c) kein Challenge-/Interstitial-Fingerabdruck darin steht („Verifying your
browser", „Incident ID", „Attention Required", „Just a moment", „Checking your
browser", „Ray ID" … — versionierte Konstante), (d) der Text nicht überwiegend
Consent-Boilerplate ist und genug Sätze trägt, die der Prosa-Filter als Prosa
erkennt. Alles andere ist `unverifiable`: **gezählt, ausgewiesen, nie gediffed.**
Die Befunde 1 und 2 des Audits — eine WAF-Challenge, die das Archiv mit HTTP 200
gespeichert hat und die der Origin als 270-Token-Entfernung mit Salienz 20
publizierte; ein nginx-403, das er als Löschung publizierte — sind genau das,
was hier nicht mehr passieren kann.

Was durch das Gate kommt, wird deterministisch gediffed
(`textdiff` → `prose` → `salience`, aus dem Origin geerbt) und **typisiert**:

`number_revised` · `date_shifted` · `negation_flipped` · `commitment_removed` ·
`attribution_removed`

Fünf Operationen **am Text**, keine Absichten. „Institution X vertuscht" ist
keine Ausgabe dieses Instruments und kann keine werden (E-2). Wo die Regeln sich
enthalten, entsteht eine `abstention` — und nur die sieht die Modellschicht.

**I8 ist strukturell gelöst, nicht durch Vorsatz:** jede Passage, die eine
Zuschreibung an eine Person oder ein Amt trägt, geht als SHA-256 in den Record,
nie als Text. Ein Name in einer Registerzeile ist damit konstruktionsbedingt
unmöglich — und `verify.py` prüft das nach.

**Jede Löschbehauptung wird live nachgeprüft**, mit den Offenlegungsklassen und
dem Wilson-CI aus `world/recheck.py`: `botwall` (401/403/429), `server_error`
und `unreachable` fallen aus dem Nenner und werden als Zahl ausgewiesen; 451
steht getrennt. Erst danach darf das Wort „gone" im Record stehen.

## Die Watchlist — live erprobt, nicht konfiguriert (Auflage 1)

`memoryhole/watchlist.json`, gebaut aus **live gelaufenen Probes in der Nacht
14./15. August**. Je Eintrag stehen die versuchte Strategie, das Ergebnis, die
Latenz und der Fehler im Record; ein Host wird nicht konfiguriert, er wird
ausprobiert.

| Kat. | Institution | Strategie | Abfrageziel | Probe: URLs/Tag | Latenz | Vorher gescheitert |
|---|---|---|---|---|---|---|
| A | Bundesministerium für Wirtschaft und Energie | `domain` | `bundeswirtschaftsministerium.de` | 228 | 6.4 s | — |
| A | Bundesministerium für Gesundheit | `domain` | `bundesgesundheitsministerium.de` | 170 | 7.3 s | — |
| A | Bundesministerium für Umwelt, Naturschutz, nukleare Sicherheit und Verbraucherschutz | `domain` | `bmuv.de` | 25 | 2.9 s | — |
| A | Robert Koch-Institut | `prefix` | `rki.de/` | 368 | 55.1 s | `domain` HTTP 504 |
| A | Umweltbundesamt | `domain` | `umweltbundesamt.de` | 329 | 46.5 s | — |
| A | Statistisches Bundesamt | `prefix` | `destatis.de/` | 1440 | 49.9 s | `domain` HTTP 504 |
| B | European Commission, DG Climate Action | `domain` | `climate.ec.europa.eu` | 415 | 5.5 s | — |
| B | European Securities and Markets Authority | `domain` | `esma.europa.eu` | 28 | 56.3 s | — |
| B | European Banking Authority | `prefix` | `eba.europa.eu/regulation-and-policy/` | 3 | 12.6 s | `domain` HTTP 504; `prefix` HTTP 504 |
| B | European Insurance and Occupational Pensions Authority | `domain` | `eiopa.europa.eu` | 12 | 15.2 s | — |
| B | European Medicines Agency | `prefix` | `ema.europa.eu/` | 563 | 59.5 s | `domain` HTTP 504 |
| B | EU Agency for the Cooperation of Energy Regulators | `domain` | `acer.europa.eu` | 30 | 39.8 s | — |
| C | Bundesnetzagentur | `domain` | `bundesnetzagentur.de` | 402 | 15.4 s | — |
| C | Bundesanstalt für Finanzdienstleistungsaufsicht | `prefix` | `bafin.de/DE/` | 16 | 57.5 s | `domain` HTTP 504; `prefix` HTTP 504 |
| C | Deutsche Bundesbank | `domain` | `bundesbank.de` | 156 | 25.2 s | — |
| D | Google (sustainability) | `domain` | `sustainability.google` | 33 | 5.1 s | — |
| D | ExxonMobil (corporate) | `domain` | `corporate.exxonmobil.com` | 489 | 32.4 s | — |
| D | Shell | `domain` | `shell.com` | 1804 | 17.2 s | — |
| D | Volkswagen Group | `domain` | `volkswagen-group.com` | 109 | 2.3 s | — |
| D | BASF | `domain` | `basf.com` | 311 | 49.4 s | — |
| D | Bayer | `domain` | `bayer.com` | 28 | 21.0 s | — |
| D | BP | `prefix` | `bp.com/` | 104 | 21.7 s | `domain` HTTP 504 |

**Kontrollgruppe (E): 20 Seiten** — Kontakt-, Impressums-,
Datenschutz-, Barrierefreiheits-, Sitemap- und Rechtstexte quer über A–D, jede
einzeln mit der Einzel-URL-Historienabfrage geprobt. Sie sind keine Beigabe: an
ihnen misst das E-Experiment die Falsch-Positiv-Rate des Verfahrens (Bar: 0).
Ausgewählt wurden sie nicht geraten, sondern **aus den Discovery-Antworten der
Institutionen geerntet** und dann einzeln nachgeprüft — was in der Liste steht,
hat das Archiv nachweislich gesehen.

**Ausgeschlossen:** die 32 Seiten der Kammer 1 des Origins, namentlich im
Watchlist-File (`excluded.urls`) — der Origin behält sie unangetastet, Memory
Hole doppelt keine davon; ein Test hält das fest, und `verify.py` prüft es je
Nacht nach. Ebenso ausgeschlossen: US-Bundesumwelt- und -gesundheitsseiten
(EDGI-Duplikat, Audit-Befund 4).

## Erste Lesung (UTC-Tag 2026-08-13, gerechnet 2026-08-15 00:02 UTC)

Ein echter Lauf, keine Simulation. Laufzeit **61 Minuten** (23:01 → 00:02 UTC)
— das Audit budgetiert 1–3 Stunden je Nacht, und genau da liegt es.

**Erfassung.** 22 Institutionen gefragt, **20 haben geantwortet**; ESMA und EMA
endeten nach vier Versuchen in HTTP 504 und stehen als `failures` im Record.
Zwei weitere (EBA, EIOPA) antworteten mit **null Zeilen** — das ist kein
Fehler, sondern die Kadenz: das Archiv hat diese Hosts an diesem Tag nicht
angefasst. Insgesamt hat das Archiv an einem einzigen Tag **2.150 Seiten**
dieser Institutionen berührt; allein `shell.com` 1.468, `bundesnetzagentur.de`
225, `destatis.de` 182. Kammer 1 des Origins sieht 32 Seiten pro Nacht.

**Geprüft: 98 Seiten** (78 gezogene + 20 Kontrollseiten).

| Klasse | Zahl | Anteil |
|---|---|---|
| `unchanged` | 15 | |
| `changed` | 3 | Änderungsrate **16,7 %**, CI₉₅ [5,8 %; 39,2 %] über 18 entschiedene |
| `unverifiable` | 73 | **74,5 %**, CI₉₅ [65,1 %; 82,1 %] |
| `gone` | 7 | |

**Der Befund der Nacht ist die Löschprüfung — und er beziffert Audit-Befund 2.**
24 Seiten trugen im Archiv ein 4xx, waren also nach der **Logik des Origins**
Löschungen. Die Live-Nachprüfung sagt:

| Live-Antwort | Zahl | |
|---|---|---|
| **404 — wirklich weg** | **7** | RKI (3), Umweltbundesamt (2), Bundesbank (1), Bayer (1) |
| **200 — die Seite lebt** | **13** | BaFin (3), Destatis (5), RKI (2), BMWE (2), Destatis-Sitemap (1) |
| **403 — Bot-Wall** | 4 | ausschließlich `bp.com`, aus dem Nenner genommen |

Löschrate **35 %**, CI₉₅ [18,1 %; 56,7 %] über 20 entschiedene Kandidaten.

**Das heißt: 13 von 24 Löschbehauptungen — 54 % — wären falsch gewesen.** Die
BaFin-Beobachtung des Audits war kein Einzelfall, sondern ein Muster: das
Internet Archive hat für deutsche Bundes- und Aufsichtsseiten systematisch 403
gespeichert, wo live eine funktionierende Seite steht. Auflage 3 ist damit
nicht nur erfüllt, sondern in einer Nacht als notwendig belegt. Und `bp.com`
verhielt sich exakt wie vorhergesagt: vier Kandidaten, viermal `botwall`,
viermal aus dem Nenner — kein einziger Befund über einen Konzern, der uns
nicht antwortet.

**Das Gate hat laut gearbeitet.** Von 39 geholten Aufnahme-Paaren überlebten
nur 3 beide Prüfungen. Gründe: `not_prose` 58×, `too_short` 5×, dazu
Archiv-3xx (15×) und fehlendes Vorher (4×). Das ist keine schöne Zahl, und sie
ist ehrlich zwei Dinge zugleich: das Instrument wirft Nicht-Seiten hinaus, wie
es soll — **und** die grobe Standardbibliotheks-Extraktion produziert bei
Übersichts- und Indexseiten Navigationshalden, die zu Recht durchfallen. Die
Trennung dieser beiden Anteile ist die erste Aufgabe des E-Experiments.

**Semantisch war die Nacht leer.** 3 geänderte Seiten, **0 typisierte
Ereignisse**, 1 Enthaltung (eine VW-Geschäftsberichtsseite, Salienz 7). Das ist
ein Messwert, kein Ausfall — und genau der Fall, für den Auflage 6 die
Record-Pflicht vorschreibt: die Nacht ist geschrieben.

**Kontrollgruppe: 15 `unchanged`, 5 `unverifiable`, 0 Ereignisse.** Die
Falsch-Positiv-Bar des E-Experiments (0 Ereignisse auf E) hält in Nacht eins.

**Modellschicht:** `off: no key configured`, Kosten 0,00 USD. Genau die
Degradierung, die Auflage 4 verlangt.

**Deckel:** 39 von 40 erlaubten Aufnahme-Paaren geholt — die Nacht ist ohne
Deckel-Anschlag durchgelaufen, aber um Haaresbreite.

**Konserviert:** 197 Dateien, **8,0 MB** — davon 7,0 MB die 78 archivierten
HTML-Seiten, der Rest CDX-Antworten und Manifest. `verify.py` rechnet die
gesamte Lesung daraus nach (Stichprobenziehung, Gate, Diff, Ereignisse,
Klassen, Raten) und findet **keine Lücke**.

## Was das Audit vorhergesagt hat — und was die Probes wirklich zeigten

Die Probes liefen in der Produktionsform der Abfrage, also mit demselben Code,
den die Nacht benutzt (`cdx.discovery_url` bzw. `cdx.history_url`); nur das
Fenster war weiter (7 Tage statt 1), damit ein Host bei der gemessenen Kadenz
überhaupt eine Chance hat, Zeilen zu zeigen.

| Audit-Warnung | Befund 14./15.08. |
|---|---|
| `umweltbundesamt.de` liefert im Domain-Scope **0 Zeilen** | **Nicht reproduziert.** Die tages-skopierte Produktionsform antwortet mit 329 URLs in 46,5 s. Die Falle war die Abfrageform (30-Tage-Fenster ohne `collapse=urlkey`), nicht der Host. |
| `bafin.de` Domain-Scope **504** | **Reproduziert** — und zusätzlich scheitert auch `prefix` auf dem nackten Host. Die vom Audit empfohlene **Prefix-Partitionierung** trägt: `bafin.de/DE/` antwortet mit 16 URLs. |
| `bmuv.de` in zwei Proben 504 | **Nicht reproduziert:** 25 URLs in 2,9 s. |
| `epa.gov` selbst für einen Tag 504 | nicht erneut geprobt — der Host ist als EDGI-Duplikat ohnehin ausgeschlossen. |
| `bp.com` antwortet 403 auf Seite *und* robots.txt | Der **Live**-Zugriff bleibt die Frage; die **CDX**-Abfrage geht (104 URLs über `bp.com/`). Genau die Trennung, die das Instrument braucht: das Archiv ist zugänglich, der Live-Recheck wird `botwall` sagen und aus dem Nenner fallen. |
| 19 % 504-Quote | Bei serieller Abfrage gemessen: **6 von 24 Erstversuchen** (25 %) endeten in 504, alle nach genau 60 s Timeout. Vier davon waren mit der zweiten Strategie zu retten, zwei erst mit Partitionierung. **Kein einziges 429** in ~70 Abfragen — der Dienst drosselt nicht, er ist langsam und unzuverlässig. |
| Domain-Scope liefert tausende URLs je Abfrage | Bestätigt und in einem Punkt übertroffen: `shell.com` 1.804, `destatis.de/` 1.440, `ema.europa.eu/` 563, `corporate.exxonmobil.com` 489 — **an einem einzigen Tag**. Zum Vergleich: Kammer 1 des Origins beobachtet 32 Seiten pro Nacht. |

## Substrat-Stresstest (der Zweck, nicht der Unfall)

- **`fetch.Client` musste einmal nachgeben.** Die Backoff-Leiter (30/60/120 s)
  war gegen knappe, kostbare JSON-APIs gebaut, wo Warten billiger ist als
  Abgewiesenwerden. Ein langsames, flatterndes Massenarchiv ist der
  umgekehrte Fall: bei 25 % 504 verbringt diese Leiter die Nacht mit Warten.
  Die Leiter ist jetzt ein Konstruktor-Argument; Memory Hole übergibt
  5/15/30 s. Das ist der einzige nötige Eingriff ins Substrat.
- **`Snapshot`/`preserve`/`autonomy` trugen unverändert** — aber unter einer
  anderen Last als bisher: eine Nacht schreibt ein Discovery-File je
  Institution, ein Historien-File je geprüfter Seite und zwei
  HTML-Momentaufnahmen je geänderter Seite. Das sind Hunderte kleiner Dateien
  pro Nacht statt einer Handvoll großer — die erste Snapshot-Familie dieses
  Hauses, bei der die Datei*anzahl* die interessante Größe ist, nicht die
  Byte-Zahl.
- **Der ehrlichste Befund betrifft den Prüfer.** `verify.py` musste zum ersten
  Mal keine Arithmetik zweitimplementieren, sondern eine **Heuristik** — die
  Textextraktion, das Gate, den Satz-Diff, die Ereignisregeln. Das ging nur,
  weil die Pipeline selbst standardbibliotheks-rein ist. Wäre `trafilatura`
  im Spiel, könnte der Prüfer die Lesung nicht mehr nachrechnen, sondern
  müsste ihr glauben. Der Verzicht auf die bessere Extraktion ist also keine
  Bequemlichkeit, sondern der Preis der Nachprüfbarkeit — und er wird unten
  bei den Grenzen bezahlt.

## Abweichungen von der Audit-Skizze — benannt, nicht versteckt

1. **22 Institutionen statt der skizzierten 12–18.** Alle 22 haben eine
   Live-Probe bestanden; einen erprobten Host wieder hinauszuwerfen, nur um
   eine Zahl aus einer Skizze zu treffen, wäre Willkür gewesen. Kosten: eine
   längere Nacht.
2. **Stichprobe statt „alle entdeckten Seiten".** Der Domain-Scope liefert
   3 bis 1.804 URLs je Host und Tag; jede einzelne davon zurückzulesen kostet
   eine eigene CDX-Abfrage à 2–60 s und ist in einer Nacht physikalisch
   unmöglich. Die V0 zieht deshalb je Institution **5 Seiten deterministisch
   pseudo-zufällig** (`sha256(tag|url)`). Das ist dieselbe Methode, mit der
   die World Chamber des Origins ihre Löschrate misst — Stichprobe plus
   Nachprüfung plus Wilson-CI — und der Grund, warum die Raten dieser Lesung
   überhaupt etwas bedeuten. Der Preis steht im Record: gemessen wird „unter
   den Seiten, die das Archiv an diesem Tag angefasst hat", nicht „unter allen
   Seiten der Institution".
3. **Die Extraktion nutzt `trafilatura` nicht** (Begründung oben beim Prüfer).
   Der Origin behält seine; hier ist der stdlib-Pfad der Extraktor.
4. **Die Modellschicht spricht rohes HTTP statt des Hersteller-SDK.** Das
   Substrat ist abhängigkeitsfrei; eine Nacht, die sich eine Abhängigkeit
   einhandelt, um eine *optionale* Schicht zu erreichen, wäre der schlechtere
   Tausch. Der Batch-Pfad (POST → Poll → Results, Kosten mit
   Batch-Rabatt) ist gegen eine simulierte Schnittstelle getestet.
5. **Der nächtliche Fetch-Deckel taucht als `unverifiable`-Grund auf**
   (`over_nightly_fetch_cap`), statt Seiten still fallenzulassen. Er hat in
   dieser Nacht nicht gegriffen, aber er steht im Record, wo er greifen würde.
6. **Die erste Lesung gilt dem 2026-08-13, nicht dem 2026-08-14.** Zum
   Bauzeitpunkt war der 14. UTC noch nicht abgeschlossen (23:0x UTC). Eine
   Lesung, die einen laufenden Tag als abgeschlossenen führt, wäre genau die
   kleine Lüge, gegen die dieses Haus gebaut ist.
   Der nächtliche Workflow holt den 14. um 02:30 UTC von selbst nach.

## Ehrliche Grenzen

- **Auflösung ≠ Kadenz.** Wayback crawlt institutionelle Seiten wöchentlich bis
  nie. „Nächtlich" ist die Protokoll-, nicht die Beobachtungsfrequenz — solange
  SPN nicht eskaliert wird (Franks getrennte Ein-Klick-Entscheidung).
- **Die Extraktion ist gröber als die des Origins.** Sie zieht Navigations- und
  Consent-Reste mit; genau dagegen stehen Gate und Prosa-Filter, und genau
  deshalb ist ein Teil der `unverifiable`-Quote hausgemacht, nicht fremd
  verursacht.
- **„Entfernt" ≠ „geschwärzt".** Ein Teaser, der von einer Übersichtsseite
  rollt, ist eine echte Entfernung und trotzdem Redaktionsalltag. Die
  Seitentyp-Frage (Audit-Befund 3) ist in der V0 nur teilweise gelöst: das Gate
  wirft Nicht-Seiten hinaus, aber es unterscheidet keine Inhaltsseite von einem
  News-Index.
- **EDGI ist technisch heute tiefer.** 34.999 Seiten, gespiegelte Bytes,
  Versionen ab 1997. Memory Hole gewinnt über Jurisdiktion (DE/EU/Konzerne) und
  Form (typisierte Ereignisse als tägliches Register), nicht über Fähigkeit.
  Das gehört so ins Methodenblatt, nicht kleingeredet.
- **Die Simultanitäts-These ist unbewiesen** und ist auch kein V0-Versprechen
  (Auflage 7). Sie ist E-Experiment-Hypothese, sonst nichts.
- **Die Modellschicht hat noch nie mit der echten API gesprochen.** Im Repo
  existiert kein `ANTHROPIC_API_KEY` (geprüft: nur `CLAUDE_CODE_OAUTH_TOKEN`
  ist hinterlegt). Der Batch-Pfad — POST, Poll, Results, Deckel, Kosten mit
  Batch-Rabatt — ist gegen eine **simulierte** Schnittstelle getestet und
  degradiert nachweislich ehrlich. Was er noch nicht bewiesen hat: dass er
  gegen die echte Schnittstelle sauber durchläuft. Das steht so im Record und
  wird nicht als „läuft" verkauft.
- **Git-als-Archiv kostet hier 8 MB pro Nacht** — 197 Dateien, davon 7 MB
  archiviertes HTML. Das sind hochgerechnet ~240 MB im Monat und ~2,9 GB im
  Jahr; die Dark-Ocean-Familie liegt bei 3,3 MB für sechs Tage. Das ist die
  offene Spannung dieser V0: **volle Nachprüfbarkeit verlangt die Quell-Bytes,
  und die Quell-Bytes sind groß.** Naheliegende Auswege (gzip konservieren;
  nur den extrahierten Text statt des HTML halten) sind nicht kostenlos — der
  zweite nähme dem Prüfer genau das, was er nachrechnen soll. Entscheidung
  gehört ins E-Experiment, nicht in eine Nacht um zwei Uhr.
- **Die `unverifiable`-Quote von 74,5 % ist nicht sauber aufgeteilt.** Sie
  enthält beides: berechtigte Zurückweisungen (Nicht-Seiten, Archiv-3xx,
  Bot-Walls) und hausgemachte (die grobe Extraktion, die aus Übersichtsseiten
  Navigationshalden macht). Wie viel wovon, weiß diese Nacht nicht — das ist
  die erste Frage, die das E-Experiment beantworten muss.
- **Die Stichprobe ist nach Konstruktion verzerrt** — zugunsten von Seiten,
  die das Archiv an diesem Tag angefasst hat. Das ist die Aufmerksamkeit des
  Archivs, nicht die der Institution, und der Record sagt das: gemessen wird
  „unter den Seiten, die das Archiv an diesem Tag berührt hat".

## Bewusst nicht

Keine Accounts angelegt · keine Schlüssel erzeugt · keine fremden Datenbestände
gespiegelt · **keine Bühnen- oder Site-Präsenz** (Öffentlichkeit erst ab
bestandenem E-Experiment, Aufnahme-Pfad Stufe 5) · kein Backfill vergangener
Nächte · keine Watchlist-Migration aus dem Origin · keine
E-Experiment-Kriterien nebenbei (die werden **vor** dem 14-Nächte-Lauf in
eigener Sitzung committet, Stufe-4-Pflicht).

## Nächste Schritte

1. **Origin-Fix (Auflage 5, die Gegenleistung ans Haus):** die beiden Fehler,
   die dieses Audit gefunden hat — 4xx als Löschung ohne Nachprüfung; die
   WAF-Challenge als 200 archiviert und als Entfernung publiziert — gehören als
   eigener PR in `frankbueltge.de/pipelines/redaction/`, bevor Memory Hole
   Nächte sammelt. Sie betreffen die 32 heute laufenden Seiten.
2. **E-Experiment-Kriterien committen** (§8 des Audits: Falsch-Positiv-Rate auf
   E, Gate-Quote, Ertrag ≥4/14, Löschbehauptungen, Determinismus gegen Modell,
   Simultanität, Kosten, Laufzeit, Substrat), dann 14 Nächte.
3. **Modellschicht scharf schalten**, sobald Frank einen `ANTHROPIC_API_KEY` als
   Repo-Secret hinterlegt — der Workflow liest ihn bereits, die Nacht läuft ohne
   ihn weiter.
4. **SPN-Eskalation** bleibt Franks getrennte Entscheidung; die V0 wartet nicht
   auf sie.
