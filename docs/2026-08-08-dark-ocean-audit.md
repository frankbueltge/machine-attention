# Dark Ocean — Audit (Stufe 2 des Aufnahme-Pfads)

**Datum:** 2026-08-08 (Probes 23:05–23:15 UTC) · **Status:** Audit abgeschlossen,
Empfehlung an Frank — **die Aufnahme selbst bleibt sein Gate**
**Exposé:** `2026-08-08-kandidat-dark-ocean.md` · **Origin:** The Ghost Fleet
(frankbueltge.de, läuft unverändert weiter) · **Muster:** Foreknown-Audit vom 2026-08-08

## Einzeiler (aus dem Exposé, bestätigt)

> Ships tell the world where they are. Satellites can see where they actually are.
> The two views do not always agree.

## Quellen-Audit (Live-Probes 2026-08-08, 23:05–23:15 UTC, alle ohne Anmeldung)

| Quelle | Probe | Befund |
|---|---|---|
| **GFW Gateway API** | `/v3/datasets`, `/v3/vessels/search` ohne Token | HTTP 401 „invalid token" — Token-Pflicht bestätigt (kostenlose Registrierung, aber Login → Charter-Eskalation) |
| **GFW SAR vessel detections** | Plattform-Update-Seite (GFW selbst) | **Offline seit 2026-07-03** (Sentinel-1A-Rentierung riss die Pipeline), angekündigt „mindestens ein Monat" — Stand heute: **fünf Wochen, kein Update, kein Termin.** Exposé-Annahme bestätigt und verschärft |
| **GFW Terms of Use** | öffentliche Terms-Seite | **CC BY-NC** (mehrfach) — Nicht-kommerziell-Klausel auf Karte und Daten |
| **Copernicus Data Space (CDSE), Katalog** | OData `Products` ohne Auth | **HTTP 200, keyless.** Ostsee-Suche liefert GRDH-Szenen von HEUTE 16:53 UTC, Absender **S1D** — die neuen Satelliten liefern öffentlich, während GFWs Ableitung dunkel ist. Szenengrößen gemessen: 1,11–1,78 GB |
| **CDSE, Produkt-Metadaten** | `$top=1` GRDH, Feldliste | Je Szene: **Checksummen (MD5 + BLAKE3) vom Herausgeber selbst**, Footprint-Polygon, `Online`-Flag, **`EvictionDate`** (Szenen rollen aus dem Online-Speicher!), S3Path |
| **CDSE, Download** | zipper `$value` ohne Auth | HTTP 401 „Token not found" — Bytes brauchen (kostenlosen) Copernicus-Account → Eskalation |
| **CDSE, STAC** | `/stac/collections/SENTINEL-1` | 404 (andere Collection-Namen); **OData ist die tragfähige Schnittstelle**, STAC nur mit Namensauflösung |
| **Digitraffic (FIN), AIS live** | `/api/ais/v1/locations` | HTTP 200 **keyless** (einzige Anforderung: gzip-Header). Zum Probezeitpunkt **953 Schiffe live**, Felder mmsi/sog/cog/navStat/… |
| **DMA (DK), AIS-Tagesdumps** | `web.ais.dk/aisdata/`, zwei Proben | **Ausfall zum Probezeitpunkt** (Timeout http und https, 40 s und 15 s). Vermerkt, nicht überbrückt — Nachprobe nötig; wäre die Volumen-/Historienquelle für die Ostsee |
| **NOAA MarineCadastre (US)** | AIS-Handler 2024 Index | HTTP 200 keyless — US-Gewässer, historische Tiefe |
| **EMODnet Human Activities** | WMS GetCapabilities | HTTP 200 keyless, **84 vessel-density-Layer** (EU-Aggregate, monatlich) |
| **EOG VIIRS Boat Detections** | Produktseite | Erreichbar, aber Datei-Downloads hinter Registrierung → Eskalationsklasse (Nachtlicht-Achse: Phase 2) |
| **Hausintern: pipelines/ghost-fleet** | Code-Sichtung | **Produktiver, getesteter GFW-Adapter existiert** (Events API, gap events, Token-Redaktion, Retries) — und das Haus besitzt einen von Frank bewilligten `GFW_TOKEN` (Site-Secret) |

**Registrierungs-Disziplin eingehalten:** keine Accounts angelegt; jede Token-Pflicht
ist als Befund dokumentiert, nicht umgangen.

## Die vier Kernbefunde

### 1. GFWs Ableitung ist dunkel, die Rohbeobachtung fließt

GFW SAR ist seit fünf Wochen offline ohne Termin — aber der CDSE-Katalog zeigt
S1D-Szenen von heute über der Ostsee, öffentlich und keyless durchsuchbar. **Der
beobachtete Ozean wird weiter beobachtet; nur das abgeleitete Sichtbarkeitsprodukt
fehlt.** Das ist selbst schon eine Dark-Ocean-Beobachtung erster Güte — und es
verschiebt den Plan B des Exposés (eigener begrenzter Sentinel-1-Pfad) von „Notlösung"
zu „ernsthafte Architektur-Option". Ehrliches Gegengewicht bleibt: eigene Detektion
ist echte Bildverarbeitung mit Qualitätsrisiko — „ein schlechteres GFW braucht
niemand" (Exposé). Die V0-Empfehlung unten umgeht diese Falle.

### 2. Lizenz-Kollision: GFW ist CC BY-NC, die Lab-Linie ist offen

Seit 2026-07-26 gilt für alle Lab-Repos: Code Apache 2.0, Werke CC BY 4.0, **Daten
und Ableitungen CC0**. Aus CC-BY-NC-Material lassen sich keine CC0-Ableitungen
ziehen. Copernicus-Daten dagegen sind EU-offen inklusive kommerzieller Nutzung
(Attribution), die AIS-Behördenquellen (FIN/DK/US) und EMODnet sind Public-Sector-
offen. **Konsequenz für die Architektur:** Das Rückgrat der abgeleiteten Records
muss auf Copernicus + Behörden-AIS stehen; GFW-Schichten sind nur als klar
NC-markierte Vergleichsebene zulässig und fließen nie in CC0-Ausgaben ein. (Muster
existiert im Haus: die /seed-Ausnahme dokumentiert bereits eine abweichende
Lizenzspur.)

### 3. Die GFW-Eskalation ist kleiner als gedacht

Das Origin-Experiment läuft produktiv gegen die GFW-API — mit Token, den Frank für
ghost-fleet bereits bewilligt hat, und einem Adapter, dessen Muster (Bearer,
Redaktion, Retries) direkt übernehmbar ist. Die Charter-Frage schrumpft von „Account
anlegen?" auf: **denselben Token als Secret auch in machine-attention hinterlegen?**
Ein Ein-Klick-Gate für Frank — keine neue Externbeziehung. (Der Token liegt korrekt
nur als GitHub-Secret; lokal existiert keine Kopie.)

### 4. artifact_ref trägt — sogar issuer-seitig

Der erste echte Anwendungsfall des Vertrags aus dem Aufnahme-Dokument ist gelöst
skizzierbar: Szenen (1–2 GB) kommen nie ins Git. Der CDSE-Katalog liefert je Szene
**Herausgeber-Checksummen (BLAKE3/MD5), Footprint und Zeiten** — das
referenced-not-stored-Muster der Reaktions-Achse (GDELT) trägt hier stärker, weil
nicht einmal wir hashen müssen: der Aussteller beurkundet selbst. **Pflicht dabei:**
die Katalogzeile am Tag der Beobachtung konservieren, denn `EvictionDate` zeigt,
dass Szenen aus dem Online-Bestand rollen — der Katalog ist selbst ein flüchtiges
Sichtbarkeitsregime (auch das ein Dark-Ocean-Motiv).

## Charter-Lage zusammengefasst

- **Heute keyless möglich:** deklarierte Achse Ostsee (Digitraffic live; DMA-Dumps
  nach Nachprobe; NOAA-Historie US; EMODnet-Aggregate EU) **und** die beurkundeten
  Beobachtungsakte (CDSE-Katalog: wann/wo wurde Radar geschaut, mit Checksummen).
- **Eskalation nötig (je ein Frank-Klick):** (a) Copernicus-Account für Szenen-Bytes
  (→ Detektionspfad, V1), (b) GFW-Token-Zweitnutzung (→ NC-markierte
  Vergleichsschichten), (c) EOG-Registrierung (Nachtlicht, Phase 2).

## V0-Empfehlung: „Coverage vs. Declaration" — vollständig im Charter

Kleinster Slice, ohne einen einzigen Account: **Die Maschine beurkundet den Akt des
Hinschauens gegen den Akt des Sich-Erklärens.** Ostsee als Region. Nächtlich:

1. CDSE-Katalogzeilen der letzten 24 h über der Region konservieren (Footprints,
   Zeiten, Checksummen — Bytes referenced-not-stored),
2. AIS-Lage derselben Stunden konservieren (Digitraffic; DMA wenn wieder erreichbar),
3. abgleichen als committete Records: **welche Seefläche wurde radar-beobachtet,
   was deklarierte sich dort im Beobachtungsmoment** — Zählungen je Zelle/Zeitfenster,
   `matched-moment / unobserved-declaration / observed-silence` als Kategorien über
   Regime, nicht über Schiffe.

Das ist die Signatur der Praxis (Provenienz auf den Beobachtungsakt angewandt),
deterministisch, verify-bar — und es produziert genau die Vorratsliste an
„Momenten", die ein späterer Detektionspfad (V1, hinter Eskalation a) einlösen kann.
**Ehrlicher Vorbehalt (One-Tap-Lehre):** Ob Coverage-vs-Declaration allein werkfähig
ist, entscheidet erst das E-Experiment — das Audit behauptet die Form nicht, es
belegt nur, dass der Slice messbar, ehrlich und im Charter baubar ist.

## Ethik-Grenzen (verschärft gegenüber dem Origin)

Keine natürlichen Personen — für V0 heißt das konkret: **keine MMSI, keine
Schiffsnamen in öffentlichen Records**, nur Aggregate je Zelle/Zeitfenster (kleine
Fischereifahrzeuge sind personennah). Keine „illegal"-Claims, keine
Schuldzuweisungen (E-2): publiziert werden Diskontinuitäten zwischen
Sichtbarkeitsregimen. Klassifikationen Dritter (GFW „intentional disabling") bleiben
als modellierte Einschätzungen gekennzeichnet. False Darkness — die Maschine
untersucht ihre eigenen Fehlzuordnungen — bleibt Erfolgs-Endzustand.

## Flagship oder Instrument?

Die vier Flagship-Kriterien halten der Prüfung stand (kontinuierlich: 953 Schiffe
live um 23:11 UTC, drei Ostsee-Szenen allein heute; maschinell überlegen: formal
notwendig; historisch tief: AIS 2012+, S1 2014+; ästhetisch: zwei Ozeane
übereinander). **Empfehlung: Flagship-Kandidat** — aber The Foreknown bleibt die
Bühne mindestens bis zum E1-Review (~22.08.); Dark Ocean existiert bis nach dem
E-Experiment öffentlich nur im Repo (Aufnahme-Pfad, Stufe 5).

## Go/No-Go

**GO für V0 „Coverage vs. Declaration" — mit Auflagen:**

1. Lizenz-Architektur wie Befund 2 (Copernicus/Behörden-Rückgrat CC0-fähig, GFW nur
   NC-markiert) wird im V0-Design festgeschrieben, nicht nachträglich.
2. Die zwei Eskalationen (Copernicus-Account, GFW-Token-Zweitnutzung) werden Frank
   als getrennte Ein-Klick-Entscheidungen vorgelegt; die V0 wartet auf keine davon.
3. DMA-Nachprobe vor V0-Baubeginn (Ausfall zum Probezeitpunkt ist vermerkt); fällt
   DMA dauerhaft aus, trägt Digitraffic die V0 allein — kleinerer Ausschnitt, ehrlich
   benannt.
4. Substrat-Stresstest ist Teil des V0-Auftrags: fetch/preserve/autonomy aus
   `practice/` gegen Geodaten führen; was bricht, wird als Substrat-Befund
   committet (der Stresstest ist der Zweck, nicht der Unfall).

**Kein V0-Bau ohne Franks ausdrückliches Go** — Aufnahme ist das menschliche Gate
(E-4/E-6). Dieses Audit endet hier.

## Offene Entscheidungen (Frank)

1. **Go für V0 „Coverage vs. Declaration"?** (Ostsee, keyless, ~14-Nächte-E-Experiment
   danach)
2. Eskalation a: kostenlosen **Copernicus-Account** anlegen (Detektionspfad V1)?
3. Eskalation b: **GFW_TOKEN auch in machine-attention** hinterlegen
   (NC-Vergleichsschichten + Origin-Datenkontinuität)?
4. Region bestätigen: **Ostsee** (Datenlage stark, Hausnähe) oder MPA-Rand?

## Bewusst nicht (in diesem Audit)

Keine Accounts angelegt · keine Detektion prototypisiert · keine Bytes konserviert
(Probes sind im Dokument beziffert; Konservierung beginnt mit V0) · keine
Bühnen-/Site-Änderung (Aufnahme-Pfad: Öffentlichkeit erst ab RUNNING) · FEWS/IPC
weiter zurückgestellt.
