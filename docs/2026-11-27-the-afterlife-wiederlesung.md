# The Afterlife — Wiederlesung des Blockers (2026-11-27)

**Art:** Wiederlesung eines geparkten Kandidaten nach `discovery/PROMPT.md` Schritt 2 — kein AUDIT, kein
Exposé. **Warum heute:** jeder Kandidat mit einem Schritt wartet weiter auf ein Tor des Maintainers
(`REQUESTS.md` 2026-11-04, 11-16, 11-17, 11-20, 11-21, 11-25; The Declared Network 10-23), die Synthetic
Flood läuft monatlich (nächster Lauf 2026-12-04), ISO-Woche 48 hat ihr Exposé (The Lead Time, 2026-11-23),
und Compute Ground wurde gestern wiedergelesen (`docs/2026-11-26-compute-ground-wiederlesung.md`). Der
Blocker der Afterlife — `eutils.ncbi.nlm.nih.gov/robots.txt` `Disallow: /` (`docs/2026-10-30-the-afterlife-audit.md`
§3, `REQUESTS.md` 2026-10-30) — ist vier Wochen alt und trägt auch die Selbstentscheidung der Synthetic
Flood vom 2026-11-02, die der Lauf vom 2026-12-04 erbt.

## Was gelesen wurde

Drei Abrufe, je ein Versuch, kein zweiter (`afterlife/probes/2026-11-27/manifest.json`):

1. **`eutils.ncbi.nlm.nih.gov/robots.txt`** — 200, 178 B, `Last-Modified` 2014-06-17,
   **byte-gleich** mit dem Abzug vom 2026-10-30 (SHA-256 `ead5515b…`, beide Dateien unter
   `afterlife/probes/*/pubmed/robots.txt`). `User-agent: *` / `Disallow: /`, Kopfzeile „back-end server
   version - no robots!".
2. **`www.ncbi.nlm.nih.gov/robots.txt`** — 200, 10 819 B, `Last-Modified` 2026-03-17
   (`afterlife/probes/2026-11-27/ncbi-www/robots.txt`; am 2026-10-30 nur als Hash gehalten). Für `*`:
   `Crawl-delay: 5`, `Disallow: /entrez` (der Pfad auf diesem Host, nicht der Schnittstellen-Host),
   `/books/` gesperrt nur mit `?term=` (ein ausdrückliches `Allow: /books/NBK*` steht nur im Block eines
   benannten Agenten, Zeile 237). Gelesen, um zu entscheiden, ob Abruf 3 erlaubt ist — er ist es, weil
   nichts ihn sperrt. **Die Datei beginnt mit derselben Kopfzeile** „back-end server version - no robots!"
   wie die des Schnittstellen-Hosts, trägt darunter aber über 300 Zeilen Regeln.
3. **Die Nutzungsrichtlinien der Schnittstelle** (`www.ncbi.nlm.nih.gov/books/NBK25497/`, das Kapitel
   der Betreiberhilfe, das die Ratenregeln für skriptgesteuerte Abfragen nennt) — 200, 21 381 B, aber die
   Antwort ist eine **Browserprüfseite** (Titel „Checking your browser"), nicht der Text des Betreibers.
   Nur als Hash gehalten (Skriptseite eines Dritten), kein zweiter Versuch, kein Skriptclient — dieselbe
   Grenze wie bei ipcinfo.org (`docs/2026-10-22-the-interval-treiber-quelle-audit.md`) und Meteoalarm
   (`docs/2026-11-25-the-lead-time-audit-teil-2.md` §3).

Kein Abruf an die Schnittstelle selbst, keine Zählung, nichts gesendet, keine Person, kein Konto.

## Befund

- **Der Blocker ist nicht gefallen.** Die Datei auf dem Schnittstellen-Host ist seit 2014 unverändert
  und heute dieselbe wie im AUDIT.
- **Das Gegengewicht ist im Record dünner, als `REQUESTS.md` (2026-10-30) es klingen lässt.** Dort und
  im AUDIT §3 steht, der Betreiber biete den Host „mit eigenen Ratenregeln" an. Belegt im Record ist
  davon nur der Antwortkopf `X-Ratelimit-Limit: 3` (`docs/2026-10-30-the-afterlife-audit.md`, Tabelle,
  Zeile Nachweis A). Der Text der Richtlinien selbst ist in keinem Abzug gehalten und war heute von hier
  aus nicht lesbar. Die Frage an den Maintainer bleibt dieselbe; sie ruht jetzt ausgesprochen auf einem
  Header, nicht auf einem gelesenen Angebot. Und die Selbstbeschreibung der Datei („back-end server
  version"), die das AUDIT als Gegengewicht nannte, trägt weniger als gedacht: dieselbe Kopfzeile steht
  über der vollen Regeldatei des www-Hosts — sie ist Vorlagentext, keine Aussage über die Schnittstelle.
- **Neu und klein:** der www-Host verlangt von jedem Agenten 5 s Abstand. Er ist nicht der Host, den
  Register A der Synthetic Flood liest (`practice/src/practice/syntheticflood/pubmed.py`); für die
  Schnittstelle folgt daraus nichts.

## Was folgt

- The Afterlife bleibt **geparkt**. Wiederlesen, wenn der Maintainer `REQUESTS.md` (2026-10-30)
  beantwortet oder wenn sich die Datei ändert (ihr Hash steht in beiden Manifesten).
- Keine neue Anfrage in `REQUESTS.md`: der Befund ergänzt die offene vom 2026-10-30 (Notiz dort).
- `verify.py` hält jetzt `afterlife/probes/` wie die anderen Probenfamilien (`check_snapshots`);
  Einträge, die nur als Hash gehalten sind (`file: null`), dürfen keine gehaltenen Bytes behaupten.

## Bewusst nicht

Kein Abruf an `eutils.ncbi.nlm.nih.gov` außer `robots.txt`, kein zweiter Versuch an der Browserprüfung,
kein Skriptclient, keine Suche nach einer Kopie der Richtlinien auf fremden Hosts (eine Kopie wäre nicht
die Aussage des Betreibers), keine Änderung an der Synthetic Flood vor ihrem Lauf am 2026-12-04, kein
neues Exposé (Woche 48 hat eines), kein laufendes Instrument berührt.
