# The Afterlife — AUDIT

**Datum:** 2026-10-30 · **Stufe:** AUDIT · **Exposé:** `docs/2026-10-29-kandidat-the-afterlife.md`
· **Proben:** `afterlife/probes/2026-10-30/manifest.json` (17 Anfragen, 07:38–07:4x UTC, je ein
Versuch, keine Wiederholung).

**Anlass.** Der Fokus wartet: The Interval hat freitags nichts fällig (Tally: Wochen fällig 2 von 4,
A1 keine fehlende Woche, A2 pass, A3 keine, B2 keine Änderung, 8 Episoden in beiden Wochen). Die
Synthetic Flood hat ihren nächsten Schritt erst ab 2026-11-01 (M+2), The Declared Network wartet auf
`REQUESTS.md` (2026-10-23). Damit ist die Bedingung aus `discovery/AGENDA.md` erfüllt, unter der das
AUDIT der Afterlife laufen darf.

## 1. Ergebnis je Quelle

| Seite | Endpunkt | Status | Größe | Rate / Grenze | Lizenz | `robots.txt` | Charta |
|---|---|---|---|---|---|---|---|
| Erklärung | `api.crossref.org/works?filter=update-type:retraction,from-created-date:…,until-created-date:…&select=DOI,created,update-to` | 200 (3), **429** (1) | Zählung 188 B; 100 Notizen 36 020 B | `x-rate-limit-limit: 1`, `x-rate-limit-interval: 1s`, `x-concurrency-limit: 1`; die vierte Anfrage, 1,5 s nach der dritten, bekam 429 (geteilte Ausgangsadresse) | an der Schnittstelle nicht angegeben | **404** (keine Datei, also kein Verbot) | **innerhalb** — mit `select` trägt die Antwort keine Namen |
| Erklärung, Abzug | Retraction-Watch-CSV, `gitlab.com/crossref/retraction-watch-data` (Repositorium mit `README.md` und `retraction_watch.csv`) | 200 (3, Projekt-API) | nicht geladen | — | an der Dokumentation nicht angegeben | **`Disallow: /api/v*` und `Disallow: /*/raw`** für jeden Agenten | **außerhalb für V0**: die Datei ist nur ganz zu laden und trägt nach dem Exposé Autorenspalten (I8); drei API-Anfragen gingen vor dem Lesen von `robots.txt` hinaus und sind nur als Hash gehalten |
| Nachweis A | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="retracted publication"[pt]` | 200 (2) | 205 B / 326 B | `X-Ratelimit-Limit: 3` | — | **`Disallow: /` für jeden Agenten** (`afterlife/probes/2026-10-30/pubmed/robots.txt`, Last-Modified 2014-06-17, Kopfzeile „back-end server version - no robots!"); `www.ncbi.nlm.nih.gov/robots.txt` sperrt `/entrez/eutils` für mehrere benannte Agenten, für `*` `/entrez` (Hash im Manifest) | **offen — Frage an den Maintainer** (§3) |
| Nachweis B | `api.openalex.org/works?filter=is_retracted:true&select=…` | **429** | 802 B | Tagesbudget der Ausgangsadresse aufgebraucht, `Retry-After: 58869`, `X-RateLimit-Remaining: 0` | — | `Allow: /` | erreichbar nur mit eigenem Schlüssel, den der Betreiber gegen die E-Mail-Adresse einer Person ausgibt (Antworttext) — **außerhalb** |
| Dokumentation | `www.crossref.org/documentation/retrieve-metadata/retraction-watch/` | 200 | 70 908 B (Hash) | — | — | — | gelesen, nicht gesichert |

## 2. Was die Bytes zeigen

- **Die Erklärungsseite ist schlüsselfrei lesbar.** Notizen mit `created` zwischen 2026-10-01 und
  2026-10-29: **426** (`afterlife/probes/2026-10-30/crossref/retraction-notices-count-2026-10.json`).
  In den ersten 100 (`…/retraction-notices-sources-2026-10.json`) stehen 103 Beziehungen vom Typ
  `retraction`, alle mit `source: publisher`; keine mit `source: retraction-watch`, obwohl die
  Dokumentation diesen Wert nennt. Wo die Retraction-Watch-Einträge in der Schnittstelle sitzen
  (an der Originalarbeit statt an einer Notiz?), ist offen; eine Kohorte nur aus Verlagsnotizen
  wäre schmaler als das Register.
- **Das Datum der Erklärung.** `update-to[].updated` liegt bei 85 von 103 Beziehungen am selben Tag
  wie `created` der Notiz, bei 16 einen Tag davor; zwei Ausreißer liegen 137 und 452 Tage davor. Ein Kandidat für das eine
  Rückzugsdatum, das das Exposé (§6) vor dem ersten Abruf festlegen will: `created` der Notiz in
  Crossref. Nicht festgelegt heute.
- **Crossref ist zugleich ein Nachweis.** Die Originalarbeit `10.3389/fmicb.2025.1738181` trägt
  `updated-by` mit der Rückzugsnotiz und `indexed` 2026-10-20T18:40 UTC, am Tag der Notiz
  (`…/original-updated-by-2.json`). Für Verlagsnotizen ist die Crossref-Nachlaufzeit damit
  vermutlich nahe null — das Tageslicht liegt bei den anderen Nachweisen, nicht hier.
- **PubMed markiert in der Masse:** 35 366 Datensätze mit Publikationstyp „Retracted Publication"
  (`…/pubmed/retracted-publication-count.json`). Der Typ der Notiz selbst wurde mit der falschen
  Schreibweise gefragt (0 Treffer, `…/retraction-notice-count.json`) und nicht wiederholt.
- **Datiert ein Nachweis seine Markierung?** Nicht geprüft: dafür wären weitere Anfragen an
  E-utilities nötig gewesen, und die stehen unter §3. Bleibt offen.

## 3. Der Befund, der über alles andere entscheidet

`eutils.ncbi.nlm.nih.gov/robots.txt` lautet `User-agent: *` / `Disallow: /`. Das ist die Lage von
FEWS NET (`docs/2026-10-04-kandidat-the-interval.md` §2) und OSCAR
(`docs/2026-10-23-declared-network-audit.md`). Zwei Zählungen gingen im selben Durchgang hinaus
wie das Lesen der Datei, bevor sie gewogen war; sie tragen keine Personendaten und sind
mit diesem Hinweis im Manifest gehalten. Danach ging keine Anfrage mehr an E-utilities.

**Das betrifft nicht nur diesen Kandidaten.** Register A der Synthetic Flood liest denselben Host
(`practice/src/practice/syntheticflood/pubmed.py`). Ihr AUDIT hat die Datei am 2026-10-18 mit 200
gelesen (`syntheticflood/probes/2026-10-18/manifest.json`), ohne sie im Dokument zu wägen
(`docs/2026-10-18-synthetic-flood-audit.md`, Zeilen zu PubMed). Dagegen steht, dass E-utilities
eine Programmierschnittstelle ist, die der Betreiber mit eigenen Ratenregeln für skriptgesteuerte
Abfragen anbietet (3 Anfragen/s ohne Schlüssel, im Header bestätigt) und dass die Datei aus dem
Jahr 2014 stammt und sich als „back-end server version" bezeichnet. Ob das Angebot der
Schnittstelle die Datei überwiegt, entscheidet nicht der Pass: Bei OSCAR hat er dieselbe Frage dem
Maintainer gegeben, und er gibt sie ihm auch hier.

## 4. Empfehlung

**Kein V0 wie skizziert.** Von den drei Nachweisen ist OpenAlex von hier aus nicht tragfähig
(Budget, Schlüssel nur gegen eine Personenadresse), Crossref markiert die Originalarbeit
vermutlich am Tag der Notiz, und PubMed, der Nachweis mit dem größten Tageslicht, hängt an der
Frage von §3. Ein V0 nur aus Crossref würde ein Register gegen sich selbst messen. Die Afterlife
wird **auf dem Ergebnis geparkt**, mit einer Bedingung zur Wiederaufnahme: Liest der Maintainer
die E-utilities-Datei als nicht bindend für die Schnittstelle, ist ein schmales V0 möglich —
Kohorte aus Crossref-Notizen ab dem ersten V0-Tag, ein täglicher PubMed-Abgleich je offener DOI,
OpenAlex nur als Kontrolle, sobald es von einem Runner aus antwortet. Das GO dafür wäre dann
seins.

**Für die Synthetic Flood** hält der Pass die Lesung M+2 an (fällig ab 2026-11-01), bis die Frage
beantwortet ist oder bis zum Pass am 2026-11-02 Schweigen herrscht. Nach der stehenden Regel in
`REQUESTS.md` heißt Schweigen dann: Der Pass liest die Datei wie die Betreiberregeln der
Schnittstelle, nimmt die Lesung M+2 auf und vermerkt die Selbstentscheidung. Für die Afterlife
gilt Schweigen nicht als GO für V0; das GO bleibt nach dem Aufnahme-Pfad das des Maintainers.

## Bewusst nicht heute

Kein zweiter Versuch nach 429 (Crossref einmal, OpenAlex einmal). Keine weitere Anfrage an
E-utilities nach dem Lesen von `robots.txt`, keine an die GitLab-API oder an den CSV-Pfad. Keine
Anfrage nach einem Schlüssel, keine E-Mail-Adresse gesendet. Keine Namen, keine Titel gesichert:
alle gehaltenen Crossref-Antworten tragen nur DOI, Datum und Beziehung. Kein Code, keine Kohorte,
kein Rückzugsdatum festgelegt. The Interval und Planetary Listening sind unberührt.
