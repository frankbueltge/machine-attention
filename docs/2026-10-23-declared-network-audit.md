# The Declared Network — AUDIT

**Datum:** 2026-10-23 (zweiter Lauf, ab 22:31 UTC) · **Stufe:** AUDIT · **Exposé:**
`docs/2026-10-23-kandidat-declared-network.md` · **Proben:** `declarednetwork/probes/2026-10-23/`
(Manifest `manifest.json`, 9 Einträge).

**Anlass:** Der Fokus wartet. The Interval hat freitags nichts fällig, seine Treiber-Frage in
`REQUESTS.md` (2026-10-22) ist unbeantwortet. Planetary Listening: die Lesung
`planetary/readings/2026-10-23.json` ist da (Commit `1aec490`). Die Synthetic Flood ist erst ab
2026-11-01 fällig (M+2). Die Bedingung der Agenda — Audit nur, wenn Fokus und laufende Kandidaten
warten — ist erfüllt.

## 1. Was abgefragt wurde

Keine Anfrage mit automatischer Wiederholung, alle mit dem User-Agent der Praxis. Insgesamt 22
Anfragen an drei Hosts: 5 Kopf-Abrufe zur Orientierung, 13 Abrufe mit Antwortkörper, 4 Abrufe des
Probenskripts (die drei `robots.txt` erneut, ein Ausschnitt des Inventars). An OSCAR gingen davon
5: dreimal `robots.txt`, die Stationssuche einmal als Kopf-Abruf und einmal vollständig. Die Tabelle
nennt, was konserviert oder gezählt ist.

| Quelle | Endpunkt | HTTP | Größe | Konserviert |
|---|---|---|---|---|
| OSCAR/Surface | `https://oscar.wmo.int/robots.txt` | 200 | 409 B | ganz |
| OSCAR/Surface | `…/surface/rest/api/search/station?stationClass=synopLand` | 200 | 14 374 478 B, 22 s | **nichts** (nur SHA-256, §2) |
| WDQMS | `https://wdqms.wmo.int/robots.txt` | 404 | 153 B | ganz |
| WDQMS | `…/wdqmsapi/v1/download/nwp/synop/six_hour/availability/?date=2026-10-21&period=00&variable=pressure&centers=COMBINED&baseline=OSCAR` | 200 | 1 800 909 B | erste 64 KiB |
| WDQMS | dasselbe für `date=2023-01-01` | 200 | 1 442 371 B | erste 8 KiB |
| WDQMS | dasselbe für `date=2020-07-06` | 200 | 1 424 002 B | erste 8 KiB |
| NCEI | `https://www.ncei.noaa.gov/robots.txt` | 200 | 254 B | ganz |
| GHCN-Daily | `…/pub/data/ghcn/daily/readme.txt` | 200 | 29 587 B | ganz |
| GHCN-Daily | `…/pub/data/ghcn/daily/ghcnd-inventory.txt` (Range 0–65535) | 206 | 65 536 von 36 396 304 B | ganz (der Ausschnitt) |

Nicht in der Tabelle, weil ohne Befund für die Frage: die WDQMS-Startseite und ihr Skript (daraus
wurde der Download-Pfad gelesen) sowie zwei Download-Versuche mit falschen Parametern (beide 500).
Die Konfigurationsdatei der Startseite enthält ein Zugangstoken eines Kartendienstes. Sie wurde
deshalb nicht konserviert.

## 2. Befunde je Quelle

### OSCAR/Surface — das Register: lesbar, aber es bittet Roboter, nichts zu lesen

- **`robots.txt` sperrt alles:** `User-agent: *` / `Disallow: /`
  (`declarednetwork/probes/2026-10-23/oscar/robots.txt`). Das ist dieselbe Lage wie bei FEWS NET
  (`docs/2026-10-04-kandidat-the-interval.md` §2): Der Betreiber bittet automatisierte Abrufer, die
  Seite nicht zu lesen. Ob das auch für die REST-Schnittstelle gemeint ist, sagt die Datei nicht.
  Die Praxis liest sie als Bitte, bis der Maintainer anders entscheidet.
- **Offenlegung:** Die Suchanfrage ging zweimal hinaus (Kopf-Abruf, dann vollständig), beide Male
  im selben Befehl wie ein Abruf von `robots.txt`, also bevor die Sperre gewogen war. Deshalb ist von ihr nur die Prüfsumme festgehalten (Manifest-Eintrag
  `search-synopLand.json`, `file: null`), keine Bytes. Danach ging an diesen Host nur noch `robots.txt` (für die Probe), keine Anfrage an die Schnittstelle.
- **Was die eine Antwort zeigte** (abgeleitet aus den nicht konservierten Bytes, SHA-256 im
  Manifest; Dritte können es nur mit einem eigenen Abruf nachzählen):
  16 706 Landstationen in einer Antwort (`itemsPerPage` 50 000), keyless. Je Station
  WIGOS-Kennung, `declaredStatus`, `dateEstablished` — und **`assessedStatus`**. Keine Felder für
  Kontaktpersonen in dieser Antwort (I8 hält; die Detailseiten wurden nicht abgefragt).
  Erklärter Status: 14 956 operational, 1 001 closed, 658 silent, 52 unknown, 39 partly.
  **Erklärt operational, bewertet silent: 459.** Erklärt silent, bewertet operational: 95.
  Kein Änderungsdatum, keine Historie des Status.
- **Konsequenz für das Tageslicht:** Das Register stellt Erklärung und Bewertung schon selbst
  nebeneinander. Die Gegenüberstellung *heute* ist also kein Beitrag der Praxis. Übrig bleibt nur
  die **Zeit**: seit wann der Widerspruch steht und wann die Erklärung nachzieht. Das Register
  zeigt sie nicht. Genau das war die Frage des Exposés (§1), sie wird enger, nicht falsch.

### WDQMS — die Lieferseite: offen, und sie reicht bis 2020 zurück

- Keine `robots.txt` (404), kein Schlüssel, kein Login, CSV mit
  `name, wigosid, country code, in OSCAR, …, #received, #expected, default schedule, …, date, center`.
- **Archiv:** Dieselbe Abfrage antwortet für 2026-10-21, 2023-01-01 und 2020-07-06 mit 200 und
  vollen Dateien. Das Skript der Seite nennt 2020-07-06 als frühestes Datum. Damit ist die
  **Lieferseite rückwirkend über sechs Jahre lesbar.** Das Exposé (§3) hatte nur Inventardaten als
  Rückschau vermutet.
- **Größe:** 1,4–1,8 MB je Sechsstundenfenster und Variable, also rund 7 MB am Tag für eine
  Variable. Das trägt Git nicht. V0 könnte nur abgeleitete Zeilen und die SHA-256 der Antwort
  committen, wie im Exposé §4 vorgesehen. Für eine Rückschau wären es rund 8 800 Abrufe
  (6 Jahre × 4 Fenster); das ist eine Frage der Rate, die heute nicht geprüft wurde.
- **Verbindung:** Von 13 486 Stationen der Datei vom 2026-10-21 00 UTC tragen 11 542 eine
  WIGOS-Kennung, die auch in der OSCAR-Antwort steht. 12 057 Zeilen sind `in OSCAR = True`.
  Die Verbindung über dieselbe Kennung trägt.
- **Ein Fenster ist kein Schweigen:** In diesem einen Fenster haben 1 920 erklärt operationale
  Stationen nichts geliefert. Das sagt noch nichts. Erst die Reihe über Tage macht daraus
  `fell_silent` (Exposé §2).
- **Lizenz:** Am Endpunkt nicht genannt (keine Kopfzeile, kein Text in der Datei). Die
  Datenpolitik der WMO wurde heute nicht abgefragt. Offen, vor V0 zu klären.

### GHCN-Daily — die Kontrolle: zu grob für Tage

- `robots.txt` sperrt `/data*` und `/orders*`, nicht `/pub/` — der Pfad ist erlaubt.
- `ghcnd-inventory.txt`: 36 396 304 B, `Last-Modified` 2026-10-14 (Manifest-Notiz), also **nicht
  täglich** neu geschrieben. Das Format kennt nur `FIRSTYEAR`/`LASTYEAR` (`ghcnd-readme.txt`
  Abschnitt VII). Für eine Nachlaufzeit in Tagen ist das Inventar zu grob. Taggenau wären nur die
  Stationsdateien, also ein Abruf je Station. Das ist für eine Kontrolle zu teuer.
- Eine Lizenzzeile steht im Readme nicht. Nicht weiter geprüft.

## 3. Charta

| Quelle | Öffentlich | Ohne Login | Ohne Kosten | Ohne Personendaten | Bitte an Roboter | In der Charta |
|---|---|---|---|---|---|---|
| OSCAR/Surface | ja | ja | ja | in der Suchantwort ja | **`Disallow: /`** | **nein, bis der Maintainer entscheidet** |
| WDQMS | ja | ja | ja | ja (Stationsnamen sind Ortsnamen) | keine | ja; Lizenz offen |
| GHCN-Daily | ja | ja | ja | ja | `/pub/` erlaubt | ja; als Kontrolle zu grob |

## 4. Empfehlung

1. **Kein V0, solange die Registerseite gesperrt ist.** Die Frage des Exposés braucht das
   Register: Die Nachlaufzeit ist `undeclared − fell_silent`, und `undeclared` steht nur in OSCAR.
   WDQMS trägt zwar `in OSCAR` und den erklärten Plan (`#expected`), nicht aber den erklärten
   Status. Ohne Register misst man nur Schweigen, nicht dessen Erklärung.
2. **Die Entscheidung über OSCAR gehört dem Maintainer** — eine Anfrage beim Betreiber oder die
   Lesart, dass `robots.txt` die REST-Schnittstelle nicht meint. Beides ist nicht Sache dieses
   Laufs. Die Frage steht in `REQUESTS.md` (2026-10-23).
3. **Die Lieferseite ist bereit.** Fällt die Sperre, kann V0 mit einem täglichen Registerabzug
   und den vier WDQMS-Fenstern des Vortags beginnen. Die Rückschau 2020–2026 hätte dann nur eine
   Seite: Die Register-Uhr beginnt am ersten Abruftag bei null (Exposé §3, bestätigt: keine
   Historie in der Antwort).
4. **GHCN-Daily fällt als Kontrolle aus.** Eine zweite Lieferquelle bleibt offen; das ist kein
   Blocker.
5. Bis zur Antwort ist der Kandidat **geparkt** mit dem Blocker „OSCAR `robots.txt`
   `Disallow: /`". Der Lauf liest OSCAR erst wieder, wenn der Maintainer es sagt.

## Bewusst nicht

Keine zweite Anfrage an OSCAR, keine Detailseite einer Station (dort stünden Kontaktpersonen),
keine Rate-Messung an WDQMS, keine Rückschau-Abrufe, kein Code, kein `verify.py`-Check (das ist
V0), keine Schwelle n, keine Länderzahlen. Der Fokus ist unberührt.
