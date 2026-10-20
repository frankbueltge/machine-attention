# The Synthetic Flood — V0, Inkrement 2: Register B, die datierten Kategoriegrößen (2026-10-20)

**Stufe:** V0, Inkrement 2 · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), die Lesart
seit 2026-10-18 in `REQUESTS.md`, unwidersprochen · **Anlass:** Der Fokus wartet — The Interval
liest im Fenster wöchentlich (`interval/readings/2026-10-19.json`), Planetary Listening hat seine
Kriterien seit 2026-10-19 und die erste Fensterlesung erst am 2026-10-21.

## Gebaut

- **`practice/src/practice/syntheticflood/wikipedia.py`** — die eine Anfrage, byte-gleich mit der
  Audit-Probe (`syntheticflood/probes/2026-10-18/manifest.json`, `allcategories-ai`), mit dem
  Kontakt-User-Agent des Audits (Repository-URL, keine Person), und der Parser: Container und
  datierte Monate „… from <Monat Jahr>" je Familie (`texts`, `sources`), Monatsschlüssel
  `YYYY-MM`; was nicht passt, bleibt mit Name und Größe unter `unmatched`, nichts wird verworfen;
  eine Fortsetzung (`continue`) wird vermerkt (`complete: false`), nie verfolgt — eine Anfrage am Tag.
- **`practice/src/practice/syntheticflood/categories.py`** — der Leser:
  `python -m practice.syntheticflood.categories --repo-root .` schreibt
  `syntheticflood/categories/<Datum>.json` und bewahrt die Antwort (rund 4 KB) als Bytes mit
  Manifest unter `syntheticflood/snapshots/<Datum>-categories/`. Ein Ausfall wird als Ausfall
  gelesen (I4): Status, Fehler, Zahl der Anfragen und der 429, keine Größen.
- **`verify.py` → `check_syntheticflood_categories`**: nur die auditierte Anfrage; kein Feld außer
  Kategorienamen und -größen (ein Feld wie `pages` mit Seitentiteln fällt durch); Größen nur mit
  bewahrten Bytes, und diese unter dem eigenen Datum manifestiert; jede Zahl aus den Bytes
  **unabhängig neu abgeleitet** (eigener Parser im Verifikator, nicht der des Lesers) und verglichen.
- **Tests:** `practice/tests/test_syntheticflood_categories.py`, 11 Tests ohne Netz. Der Parser
  reproduziert die Audit-Tabelle aus der bewahrten Probe (Oktober 2026: 3 504, Mai 2025: 1, 18
  datierte Monate, der Container zählt genau diese 18), Leser und Verifikator leiten dasselbe ab,
  und jede Regel hat einen Test, der sie bricht.

## Die erste Lesung: ein Ausfall, ehrlich gelesen

`syntheticflood/categories/2026-10-20.json` — 06:39:19–06:42:51 UTC, 4 Anfragen, **4 × 429**
(Leiter 0/30/60/120 s), keine Größen. Was davor und danach geschah, gehört in den Befund:

| Zeit (UTC) | Client | Ergebnis | bewahrt |
|---|---|---|---|
| ~06:38 | Kommandozeilen-Client, derselbe User-Agent, eine Anfrage (Erreichbarkeit) | 200, 4 013 B | nein — nur Erreichbarkeit, nicht als Lesung gezählt |
| 06:39–06:42 | der Leser (Standardbibliothek), User-Agent + `Accept: application/json` | 4 × 429 | nein (Ausfall, I4); Lesung vermerkt ihn |
| 06:43:57 | dieselbe Bibliothek, dieselben Kopfzeilen, ein Versuch | 429, `retry-after: 2`, 274 B | ja: `syntheticflood/probes/2026-10-20/` |

Der Text der 429-Antwort ist derselbe wie im Audit (`syntheticflood/probes/2026-10-18/mediawiki/categoryinfo.txt`):
„too many requests", Verweis auf die Ratenrichtlinie des Betreibers. Sechs Anfragen an den Betreiber
in sechs Minuten — mehr nicht; der Pass hat danach aufgehört.

**Was das heißt, und was nicht.** Die Ablehnung hielt über 3,5 Minuten und über eine `retry-after`
von 2 s hinweg an, während eine Minute zuvor ein anderer Client mit demselben User-Agent durchkam.
Ein kurzes Ratenfenster erklärt das schlecht; eine Unterscheidung nach Client liegt näher. **Bewiesen
ist das nicht** — zwei Clients, je ein Zeitpunkt, und das Audit sah 429 schon bei Anfragen im
5-Sekunden-Abstand. Der Leser wird deshalb heute nicht umgebaut: der Grund ist nicht bekannt, und ein
Umbau auf Verdacht wäre Raten am Betreiber vorbei.

## Nächste Schritte

2b. **Eine gepaarte Probe, nicht mehr:** in der nächsten Nacht, die Register B anfasst, zuerst eine
   einzige Anfrage des Lesers zu einer anderen Stunde; nur wenn sie wieder 429 erhält, eine einzige
   Anfrage des Kommandozeilen-Clients im Abstand von mindestens fünf Minuten, beide bewahrt. Erst ein
   belegter Unterschied ändert den Leser — und nur so, wie die Richtlinie des Betreibers es beschreibt.
   Ein Workflow für Register B gibt es nicht, solange der Leser nicht einmal 200 gelesen hat; ein
   Runner hat ohnehin eine andere Austritts-Adresse.
3. Die Basis 2018–2022 für Register A (rückwirkend markiert), die Stabilitätsprüfung jedes `fixed`-Worts.
4. Workflows erst danach.

## Bewusst nicht

Keine Seitentitel, keine Benutzernamen angefragt oder gespeichert; die Antwort trägt nur
Kategorienamen und -größen. Keine Fortsetzung verfolgt. Keine zweite Lesung für 2026-10-20 (eine
Lesung wird nie überschrieben). Kein Kontakt zum Betreiber — das wäre ein Senden und bleibt beim
Maintainer. Register A heute nicht gelesen (die nächste Kohortenlesung ist M+2 im November).
