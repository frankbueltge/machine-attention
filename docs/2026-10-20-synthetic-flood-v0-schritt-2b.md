# The Synthetic Flood — V0, Schritt 2b: die gepaarte Probe (2026-10-20, zweiter Pass)

**Stufe:** V0, zwischen Inkrement 2 und 3 · **Anlass:** der nächste Schritt aus
`docs/2026-10-20-synthetic-flood-v0-inkrement-2.md` §2b — der Fokus wartet (The Interval:
Woche 1 gelesen, `interval/readings/2026-10-19.json`; Planetary Listening: erste Fensterlesung
am 2026-10-21).

## Was getan wurde — genau zwei Anfragen

| Zeit (UTC) | Client | Ergebnis | bewahrt |
|---|---|---|---|
| 09:40:58 | Standardbibliothek, die Kopfzeilen des Lesers (`User-Agent` des Audits, `Accept: application/json`), ein Versuch | 429, `retry-after: 1`, 274 B | `syntheticflood/probes/2026-10-20/mediawiki/allcategories-ai-reader-0940.txt` |
| 09:46:26 | Kommandozeilen-Client (HTTP/2), derselbe `User-Agent`, `Accept: */*`, ein Versuch, 328 s später | 429, `retry-after: 33`, `x-envoy-ratelimited: true`, 274 B | `syntheticflood/probes/2026-10-20/mediawiki/allcategories-ai-cli-0946.txt` |

Beide Einträge stehen mit SHA-256 und den Antwort-Kopfzeilen im Manifest
`syntheticflood/probes/2026-10-20/manifest.json` neben der Probe vom Morgen. Der Text beider
Antworten ist bis auf die Anfrage-ID derselbe wie am Morgen und im Audit
(`syntheticflood/probes/2026-10-18/mediawiki/categoryinfo.txt`). Keine weitere Anfrage; keine
zweite Lesung für 2026-10-20 (eine Lesung wird nie überschrieben).

## Befund

Drei Stunden später als die Lesung des Morgens und mit beiden Clients: **429**. Damit ist die
Vermutung des Morgens — eine Unterscheidung nach Client — **nicht belegt**; der Leser wird nicht
geändert. Die eine 200 des Morgens (Kommandozeilen-Client, ~06:38, nicht bewahrt) ist die Ausnahme,
nicht die Regel. Was die Kopfzeilen zeigen: die Ablehnung kommt von der Ratenbegrenzung am Rand des
Betreibers (`x-envoy-ratelimited: true`), nicht von der API selbst. Naheliegend, **nicht bewiesen**:
das Kontingent hängt an der Austritts-Adresse dieses Containers, die geteilt ist — dasselbe Muster
wie beim OpenAlex-Budget im Audit (`docs/2026-10-18-synthetic-flood-audit.md`, 807 → 412 in Sekunden).
Acht Anfragen an diesen Endpunkt am 2026-10-20 aus diesem Container (sechs am Morgen, zwei jetzt), eine davon 200.

## Was daraus folgt

- Register B ist aus diesem Container nicht verlässlich lesbar. Ein Umbau des Lesers (andere
  Kopfzeilen, mehr Wartezeit) würde am Befund vorbei raten; die Richtlinie des Betreibers verlangt
  einen kontaktfähigen `User-Agent`, und den trägt der Leser schon.
- Die Regel aus Inkrement 2 bleibt: kein Workflow für Register B, solange der Leser nicht einmal 200
  gelesen hat. Ein Runner hätte eine andere Austritts-Adresse — ob ein **einmaliger, von Hand
  gestarteter** Lauf des Lesers auf einem Runner den Unterschied belegen darf, ist eine Frage an den
  Maintainer und steht in `REQUESTS.md`; ein Workflow-Lauf ist ein Klick am Repository, kein Akt
  dieses Passes.
- Der nächste Schritt, der auf nichts wartet: Inkrement 3, die Basis 2018–2022 für Register A
  (PubMed, Zählungen), und die Stabilitätsprüfung jedes `fixed`-Worts.

## Bewusst nicht

Keine Wiederholung nach `retry-after`; kein Kontakt zum Betreiber (die Adresse in der Antwort ist
ein Senden und bleibt beim Maintainer); die Client-Adresse aus den Antwort-Kopfzeilen nicht bewahrt;
keine Seitentitel, keine Benutzernamen.
