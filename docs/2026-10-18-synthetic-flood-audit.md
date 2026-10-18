# The Synthetic Flood — Audit (Stufe 2 des Aufnahme-Pfads)

**Datum:** 2026-10-18 · **Stufe:** AUDIT · **Vorgänger:** `docs/2026-10-16-synthetic-flood-expose-achse.md`
(Exposé mit Achse, §7 ist der Prüfauftrag), `docs/2026-08-22-kandidaten-re-audit.md` §3 (die zwei
Blocker) · **Anlass:** Der Fokus wartet — The Interval öffnet sein Fenster am Montag 2026-10-19
(`interval/experiment.json`), es ist nichts fällig (`discovery/AGENDA.md`).

Alle Zahlen unten stammen aus `syntheticflood/probes/2026-10-18/manifest.json` (26 Einträge,
2026-10-18 06:40:58–06:45:40 UTC). Jeder Eintrag trägt URL, HTTP-Status, Bytes, SHA-256, die
Ratengrenz-Header der Antwort, den gesendeten User-Agent und, wo abgeleitet, die abgeleitete Zahl.
Bewahrt sind nur Antworten ohne Texte Dritter; wo eine Antwort Abstracts, Autorennamen oder eine
Policy-Seite trägt, steht im Manifest `"kept": false` — gehasht, gezählt, verworfen.

## Quellen-Audit (Live-Probes 2026-10-18, alle ohne Anmeldung, ohne Schlüssel)

| Quelle | Endpunkt | Status | Größe | Rate ohne Schlüssel | Lizenz / Lage | Charta |
|---|---|---|---|---|---|---|
| PubMed E-utilities | `eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&rettype=count&retmode=json&term=…` | 200 (alle 11) | 77–81 B je Zählung | Header `x-ratelimit-limit: 3` (je Sekunde) | Zählungen sind Fakten; die Abstracts selbst tragen `<CopyrightInformation>` und Autorennamen (`efetch-3-abstracts`, `kept: false`) | **innerhalb**, solange nur Zählungen committet werden |
| OpenAlex | `api.openalex.org/works?per_page=1&select=id&filter=…` | 200 (3), robots 200 | 1,2–1,4 kB | `x-ratelimit-limit: 1000`, `x-ratelimit-remaining` 807 → 808 → 412 binnen Sekunden | Metadaten unter CC0 (Betreiberangabe, ungeprüft in den Bytes) | **innerhalb**, aber das Schlüssellos-Budget ist auf der Austritts-Adresse geteilt — nicht tragfähig |
| Crossref REST | `api.crossref.org/works?rows=0&filter=from-pub-date:…,until-pub-date:…,has-abstract:true` | 200 (2), robots 429 | 191 B | `x-rate-limit-limit: 1`, `x-rate-limit-interval: 1s`, `x-concurrency-limit: 1` | Metadaten als Fakten; Abstracts bleiben beim Verlag | **innerhalb**; der „höfliche" Pool verlangt eine E-Mail-Adresse (Betreiberangabe) — nicht gesendet, weil das eine Person wäre |
| MediaWiki API (en) | `en.wikipedia.org/w/api.php?action=query&list=allcategories&acprefix=Articles+containing+suspected+AI&acprop=size&aclimit=500` | 200 (1), 429 (2) | 4,0 kB | 429 mit `retry-after` 31–37 s auf Folgeanfragen im 5-s-Abstand | Kategorien-Namen und -Größen; keine Seitentitel, keine Benutzernamen angefragt | **innerhalb** |
| Common-Crawl-Index | `index.commoncrawl.org/collinfo.json` | — (Verbindung zurückgesetzt, 2 ×) | — | — | — | **nicht geprüft** |

PubMed, die Zahlen der Probe (ein Monat, eine Lesung — kein Befund, eine Machbarkeit):

| Kohorte (`[dp]`, `hasabstract`) | alle | `delve[tiab]` | Anteil |
|---|---|---|---|
| 2019-03 | 131 704 | 15 | 0,011 % |
| 2024-03 | 161 199 | 330 | 0,205 % |
| 2026-09 | 165 058 | 27 | 0,016 % |

Kontrolle `patients[tiab]` 2024-03: 46 679. OpenAlex mit `abstract.search:delve` (der Betreiber
stemmt, also eine andere Messung): 301 (2019-03), 6 559 von 528 481 (2024-03). Crossref mit
`has-abstract:true`: 126 820 (2019-03), 287 695 (2024-03).

Register B, die Kategorie: Der Container heißt **„Articles containing suspected AI-generated texts"**
(versteckt, 0 Seiten, nur Unterkategorien) und hat **datierte Monats-Unterkategorien**
„… from <Monat Jahr>", Mai 2025 bis Oktober 2026 (`mediawiki/allcategories-ai.json`; Oktober 2026:
3 504 Seiten, September 2026: 812, Juli 2026: 872, Mai 2025: 1). Daneben eine kleine Schwester für
Quellen („… AI-generated sources", 13 Unterkategorien, zusammen 98 Seiten). Eine Anfrage liefert
alles, ohne Fortsetzung (`continue` fehlt).

## Die fünf Kernbefunde

### 1. Register A trägt ohne einen einzigen gespeicherten Text

Die Methode des Nachbarn (Kobak et al., Exposé §5) braucht Worthäufigkeiten je Kohorte, nicht
Abstracts. `esearch` mit `rettype=count` liefert genau das: eine Zahl je Wort und Monat, 77–81 Bytes,
bei 3 Anfragen je Sekunde. Eine committete Liste von 100 Wörtern plus Kontrollwörtern, drei Lesungen
je Kohorte (M+1, M+2, M+3), ist ein paar hundert Anfragen im Monat — Minuten, nicht Stunden. Was
gespeichert würde: die Anfrage als Wiederholungsanweisung, die Zählung, SHA-256 der Antwort. Die
Abstracts selbst tragen Verlagsrechte und Personennamen (`efetch-3-abstracts`: beides vorhanden) und
werden nie committet. *Referenced, not stored* hält.

### 2. Die zweite, neu abgeleitete Liste ist die eigentliche AUDIT-Frage — und sie hat eine Grenze

Zählungen beantworten nur Wörter, die man fragt. Eine jeden Monat neu abgeleitete Liste braucht einen
Kandidatenpool. Zwei Wege, beide innerhalb der Charta: (a) ein committeter Pool von einigen tausend
Wörtern, jeden Monat gezählt (bei 3/s rund 15 Minuten je Kohorte), die neue Liste ist die
Teilmenge mit dem größten Überschuss gegen 2018–2022; (b) eine kleine, flüchtige Stichprobe von
Abstracts je Monat (`efetch`, gehasht und verworfen wie die Tagesdatei bei Planetary Listening), aus
der Kandidaten gewonnen und dann nur noch gezählt werden. (a) ist sauberer und sieht nichts außerhalb
des Pools; (b) sieht neue Wörter, hält aber Texte Dritter kurz im Speicher. Empfehlung: (a) für V0,
der Pool selbst committet und versioniert; (b) bleibt eine spätere, ausgewiesene Erweiterung.

### 3. Der Verfall ist in einer einzigen Probe schon sichtbar — darf aber noch nichts heißen

`delve` fällt von 0,205 % (2024-03) auf 0,016 % (2026-09), fast zurück auf 2019 (0,011 %). Das ist
genau die Bewegung, die das Exposé die Halbwertszeit der Methode nennt. Es ist **kein Befund**: ein
Wort, eine Lesung, und 2026-09 ist eine junge Kohorte, die PubMed noch nachträgt (`einfo`
`lastupdate` 2026/10/18 00:00). Es zeigt nur, dass die Frage messbar ist und dass der Takt aus dem
Exposé §3 (M+3 zählt) nötig ist.

### 4. Register B ist rückwirkend lesbar — als stehender Rückstand, nicht als Zufluss

Die datierten Unterkategorien zählen Artikel nach dem Monat, in dem die Markierung gesetzt wurde,
**solange sie steht**. Eine entfernte Markierung verschwindet aus ihrem Monat. Die Rückschau ist also
der heutige Rückstand nach Markierungsmonat, nicht die Zahl der Markierungen je Monat; erst die
tägliche Lesung ab V0 sieht Zufluss und Abbau getrennt. So wird es benannt. Seitentitel werden nie
angefragt (I8, E-2).

### 5. Die Raten sind die eigentliche Betriebsfrage

OpenAlex' Schlüssellos-Budget (1 000) fiel binnen Sekunden von 807 auf 412 — andere teilen die
Austritts-Adresse; ein Schlüssel verlangt ein Konto, liegt also außerhalb der Charta. Wikimedia
antwortete auf jede zweite Anfrage im 5-s-Abstand mit 429. Die Antwort mit Kontakt-User-Agent
(`machine-attention/0.1 (https://github.com/frankbueltge/machine-attention; …)`, im Manifest je
Eintrag vermerkt) kam durch; die Richtlinie des Betreibers, auf die der 429-Text verweist (`mediawiki/categoryinfo.txt`), verlangt eine Kontaktangabe, die URL des
öffentlichen Repositorys ist eine, ohne Person. Für V0 heißt das: Register B macht **eine** Anfrage
am Tag, mit diesem User-Agent; Register A trägt allein auf PubMed; OpenAlex und Crossref sind
Kontrollen für den Nenner, keine tragenden Quellen.

## Die zwei Blocker des Re-Audits

1. **Dopplung mit The Consensus (GDELT):** ausgeräumt. Keine der fünf Quellen ist eine
   Nachrichtenschicht.
2. **Takt der Hauptzahl:** ausgeräumt auf der Ebene der Quellen. Monatskohorten sind nach
   Publikationsdatum zählbar, jede Lesung kostet Sekunden, die Revision zwischen M+1 und M+3 ist
   mit derselben Anfrage wiederholbar. Belegt wird sie erst durch die zweite Lesung derselben
   Kohorte — das ist V0, nicht dieses Audit.

## Empfehlung

**GO für V0, eng.** Register A über PubMed-Zählungen (committete Wortliste und committeter
Kandidatenpool, keine Texte), Register B über eine tägliche `allcategories`-Anfrage (nur Größen der
datierten Unterkategorien). OpenAlex und Crossref nur als Nenner-Kontrolle. Common Crawl wird in V0
nicht berührt. Das GO des Maintainers ist laut Wiederaufnahme vom 2026-10-04 für den Fall erteilt,
dass das AUDIT beide Blocker ausräumt; dieses Dokument sagt, dass es das tut, und stellt die
Bewertung trotzdem in `REQUESTS.md`, weil die Reihenfolge der Kandidaten seine ist.

V0, Inkrement 1, wäre: der Kandidatenpool und die committete Liste als Datei, ein Leser für eine
Kohorte, und die erste Lesung von 2026-09 (M+1). Nicht vor Planetary Listening Inkrement 4.

## Bewusst nicht

- Keine Abstracts committet, keine Autorennamen, keine Seitentitel, keine Benutzernamen.
- Keine E-Mail-Adresse an Crossref oder NCBI gesendet (beide bieten das an; es wäre eine Person).
- Kein Konto, kein Schlüssel bei OpenAlex.
- Common Crawl nicht beurteilt: Der Index war aus diesem Container zweimal nicht erreichbar
  (Verbindung zurückgesetzt, `commoncrawl`-Einträge im Manifest ohne Status). Das ist eine
  Aussage über den Container, nicht über die Quelle; sie ist nicht die Achse.
- Keine Wortliste festgelegt — das ist V0.
