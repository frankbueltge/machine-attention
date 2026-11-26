# Compute Ground — Wiederlesung des Blockers (2026-11-26)

**Art:** Wiederlesung eines geparkten Kandidaten nach `discovery/PROMPT.md` Schritt 2 — kein AUDIT, kein
Exposé. **Warum heute:** jeder Kandidat mit einem Schritt wartet auf ein Tor des Maintainers (The Interval
und Planetary Listening auf die Durchsicht, `REQUESTS.md` 2026-11-16 und 2026-11-04; The Provisional Air,
The Shortage Clock und The Lead Time auf ein GO, 2026-11-17, 2026-11-21, 2026-11-25; The Declared Network
und The Afterlife auf ihre `robots.txt`-Fragen), die Synthetic Flood läuft monatlich (nächster Lauf
2026-12-04), und ISO-Woche 48 hat ihr Exposé schon (The Lead Time, 2026-11-23). Der älteste ungeprüfte
Blocker im Record ist der von Compute Ground: „EU-DB-Zugang ungeprüft" (`docs/2026-08-08-kandidat-compute-ground.md`,
Abschnitt Blocker; bestätigt „unberührt" in `docs/2026-08-22-kandidaten-re-audit.md` §3).

## Was gelesen wurde

1. **Die Themenseite der Kommission** zur Energieeffizienz von Rechenzentren
   (`energy.ec.europa.eu/…/energy-performance-data-centres_en`), einmal gelesen, nicht konserviert
   (eine Textseite ohne Daten). Sie verlinkt (a) die Meldeplattform der europäischen Datenbank
   (`policy-reporting-platform.ec.europa.eu`), die nach ihrem eigenen Text Daten „collects and publishes",
   (b) ein **öffentliches Dashboard „presenting the aggregated data foreseen in the directive"**,
   monatlich aktualisiert, (c) nur PDFs: Benutzerhandbuch und Meldeleitfaden (2025-09-03), FAQ (2026-09-17),
   Kontaktstellenliste (2026-03-11), eine Analyse der Meldeperiode 2024 (Juli 2025); der Bericht zur
   Periode 2025 ist „under preparation". Keine Datendatei, kein Export, kein Zeilenformat je Rechenzentrum.
2. **Eine Websuche** (ein Aufruf) nach der Veröffentlichung: der Bericht COM(2026) 500 vom 2026-09-21
   wertet die Meldungen 2024 aus; ein Entwurf einer delegierten Verordnung sieht ein **Nachhaltigkeitslabel
   je meldendem Rechenzentrum** vor, das die Datenbank selbst erzeugt, erstmals ab **2027-08-15**;
   Konsultation bis 2026-12-14. Eine öffentliche Veröffentlichung von Werten je Rechenzentrum wurde nicht
   gefunden.
3. **Das Dashboard selbst**, ein Abruf (`computeground/probes/2026-11-26/manifest.json`):
   `link.europa.eu/q7x39t` → 307 → `dashboard.tech.ec.europa.eu/qs_digit_dashboard_mt/public/sense/app/…`,
   200, 7 624 B. Die Antwort ist die **Hülle einer Skriptanwendung** (Titel und Ladebildschirm, kein Wert;
   `computeground/probes/2026-11-26/dashboard-shell.html`). Ohne Skriptclient liefert sie nichts; ein
   Skriptclient oder die interne Abfrageschnittstelle der Anwendung wurde bewusst nicht versucht.
4. **`robots.txt`** beider Hosts (Meldeplattform, Dashboard): je 403 — die Antwort ist die
   Sperrseite der **Netzrichtlinie dieses Containers** (`policy_denied`), nicht des Hosts. Nicht
   beurteilt; im Manifest unter `not_kept`.

Im Ganzen 5 Abrufe an Hosts der Kommission (Themenseite 1, Dashboard 2 — Kurzlink und Ziel —, `robots.txt`
2), dazu eine Websuche. Nichts gesendet, kein Konto, keine Person, kein Betreiber genannt.

## Befund

- **Der EU-Teil des Blockers ist nicht mehr „ungeprüft", aber nicht gefallen.** Die Datenbank
  veröffentlicht heute **nur Aggregate**, und nur in einer Skriptanwendung; die Seite bietet keinen
  Download. Für die Frage des Exposés — wo sich die Messregime *je Ort* widersprechen — tragen Aggregate
  nichts, und eine Skriptanwendung ist für diesen Pass keine Quelle (dieselbe Grenze wie bei Meteoalarm,
  `docs/2026-11-25-the-lead-time-audit-teil-2.md` §3).
- **Der Blocker hat jetzt ein Datum.** Werden die Labels ab 2027-08-15 je Rechenzentrum öffentlich, gibt es
  zum ersten Mal ein offizielles, standortbezogenes Register, das man gegen Firmenangaben und Netzdaten
  halten könnte — die tragende Quelle, die das Exposé suchte. Ob die Labels öffentlich und maschinenlesbar
  werden, entscheidet der endgültige Rechtsakt (geplant zweites Quartal 2027), nicht der Entwurf.
- **Die Form-These fehlt unverändert** (Re-Audit §3). Sie ist der zweite Teil des Blockers und durch keine
  Quelle zu lösen; sie bleibt die Bedingung jedes Starts.

## Was folgt

- Compute Ground bleibt **geparkt**. Wiederlesen, wenn der endgültige Rechtsakt zum Label veröffentlicht
  ist (frühestens zweites Quartal 2027), sonst am 2027-08-15.
- Keine Anfrage in `REQUESTS.md`: nichts wird gebraucht, was der Pass nicht selbst hat.

## Bewusst nicht

Kein Skriptclient, keine Abfrage der internen Schnittstelle des Dashboards, kein Konto auf der
Meldeplattform (sie ist für meldende Betreiber), kein PDF konserviert, kein neues Exposé (Woche 48 hat
eines), keine Änderung an einem laufenden Instrument.
