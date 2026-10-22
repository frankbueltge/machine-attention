# The Interval — Audit einer Treiber-Quelle (offener Punkt ohne Gate)

**Datum:** 2026-10-22 (dritter Pass) · **Stufe:** E-EXPERIMENT läuft (Woche 1 gelesen,
`interval/readings/2026-10-19.json`); dieser Schritt ist der offene Punkt ohne Gate aus
`discovery/AGENDA.md`: „alle acht Treiber in `interval/drivers.json` stehen auf `unassigned` — keine
Treiber-Quelle innerhalb der Charter ist bisher gesichert“. · **Bezug:** Kandidatendokument
`docs/2026-10-04-kandidat-the-interval.md` §3 Schritt 5 und §5 Risiko 1; Kriterium **B5**
(`docs/2026-10-14-the-interval-e-experiment-kriterien.md`: berichtet, **keine Latte**).

Alle Zahlen unten stammen aus `interval/probes/2026-10-22/manifest.json` (7 Einträge,
2026-10-22 14:17:06–14:17:38 UTC, je ein Versuch, kein Wiederholen, ehrlicher User-Agent). Jeder
Eintrag trägt URL, HTTP-Status, Bytes, SHA-256 und Abrufzeit. Bei der Weiterleitung der
HDX-Datei auf den Dateispeicher des Betreibers ist nur Host und Pfad bewahrt; die signierte
Abfragezeichenkette der Weiterleitung ist nicht committet.

## 1. Quellen-Audit

| Quelle | Endpunkt | Status | Größe | Lizenz / Lage | Charta |
|---|---|---|---|---|---|
| IPC-Website | `www.ipcinfo.org/robots.txt`, `/llms.txt` | **403** (beide; Antwort ist eine Browser-Prüfseite) | 5,5 kB | — | **nicht erreichbar** für einen schlüssellosen Client; die Analyse-Seiten mit „key drivers“ bleiben ungeprüft, und eine Prüfseite zu umgehen läge außerhalb der Charter |
| ReliefWeb API v2 | `api.reliefweb.int/v2/reports?appname=machine-attention&…` | **403** `"You are not using an approved appname"` | 218 B | — | **außerhalb**: eine genehmigte Kennung ist eine Anmeldung beim Betreiber |
| ReliefWeb robots | `reliefweb.int/robots.txt` | 200 | 2,3 kB | sperrt `/search/`, `/admin/` u. ä. | nur zur Kenntnis |
| HDX CKAN-Suche | `package_search?q="hunger hotspots"` | 200, **0 Treffer** | 294 B | — | kein Datensatz |
| HDX CKAN-Suche | `package_search?q="global report on food crises"` | 200, 2 Treffer | 40 kB | Paket `fsin-grfc`, **CC BY**, Herausgeber Food Security Information Network, Datenstand bis 2025-08-22, geändert 2025-09-16 | **innerhalb** |
| **GRFC-Datenbank** | Paket `fsin-grfc`, Ressource `grfc_afi_database_2016-2025_september_update.xlsx` | **200** | 197 955 B, SHA-256 `44de7226…` (vollständig im Manifest) | CC BY; derselbe Host wie die IPC-Datei von V0, ein Abruf | **innerhalb**: öffentlich, schlüssellos, kostenlos, keine personenbezogenen Daten (Länder × Jahre) |

**Was die GRFC-Datei trägt** (bewahrt unter `interval/probes/2026-10-22/hdx/`): ein Blatt, eine Zeile
je Land × GRFC-Ausgabe × Bezugsjahr 2016–2025, mit Spalten `Primary driver`, `Secondary driver`,
`Tertiary driver` (Werte `Conflict/insecurity`, `Weather extremes`, `Economic shocks`, `N/A`, `None`),
dazu Quelle der Analyse (`IPC`, `HNO`, `FEWS NET`, `IPC and gFSC`) und Analysezeitraum. Der Treiber ist
das Urteil der GRFC-Redaktion über ein Land in einem Jahr, **nicht** über eine Episode; das ist der
Abstand, den jede Zuordnung offenlegen muss.

**Offengelegt:** Für dieses Audit wurden die Zeilen der fünf Episodenländer (AFG, DJI, SDN, SOM, YEM)
ab Bezugsjahr 2020 gelesen. Die Zuordnungsregel unten ist also **nicht blind** geschrieben; sie ist
deshalb so mechanisch wie möglich gehalten (kein Ermessen je Episode), und wer sie prüft, kann sie
gegen die bewahrte Datei nachrechnen. Für die Episode SOM 2026-01 gibt es noch keine Zeile mit
Bezugsjahr 2026; sie bliebe nach jeder Regel `unassigned`. Die Zeile YEM 2023 nennt als Analysequelle
FEWS NET — das ist eine Angabe *in* der GRFC-Datei, kein Abruf bei FEWS NET.

## 2. Empfehlung

**GRFC auf HDX ist die Treiber-Quelle für `interval/drivers.json`** — die einzige der geprüften, die
innerhalb der Charter liegt und maschinenlesbar ist. Vorgeschlagene Regel `drivers-grfc-v1`, die der
nächste Pass als Code mit Tests festschreibt, **bevor** er einen Treiber einträgt:

1. Für eine Episode (Land, t0 = JJJJ-MM) gilt die Zeile mit `ISO Code 3` = Land und
   `Year of reference` = JJJJ; gibt es zwei (Hauptausgabe und Halbjahres-Update „MYU“), die spätere
   Ausgabe. Keine Zeile → `unassigned`.
2. `driver` = der **Primärtreiber**, abgebildet `Conflict/insecurity` → `conflict`,
   `Economic shocks` → `economic`, `Weather extremes` → **neuer Wert `weather`**. `drought` wird nicht
   vergeben: GRFC unterscheidet Dürre nicht von Überschwemmung, und ein Wort, das die Quelle nicht
   sagt, wäre eine Behauptung aus dem Gedächtnis. `mixed` vergibt die Regel nicht; Sekundär- und
   Tertiärtreiber werden wörtlich in einem eigenen Feld mitgeführt, statt sie in ein Etikett zu
   falten. `None`/`N/A` als Primärtreiber → `unassigned`.
3. `source` = Pfad der bewahrten Datei samt SHA-256; `verify.py` rechnet jeden Eintrag aus diesen
   Bytes nach.

Das braucht eine Codeänderung (neuer Wert `weather`, Feld für Sekundärtreiber, Nachrechnung in
`verify.py`) und eine Neuberechnung von `interval/register.json`. Das Register-Gitter, t0, t1 und die
Kriterien A1–A3, B1, B2, B6 berührt es nicht; B5 ist ausdrücklich „berichtet, keine Latte“. Ob ein
Treiber-Eintrag **im Fenster** landen soll oder erst nach dem 2026-11-15, ist eine Frage, die das
Maintainer entscheidet; der Pass legt sie in `REQUESTS.md` vor. Ohne Antwort schreibt er die Regel
als getesteten Code fest und trägt die Treiber erst nach Fensterschluss (2026-11-15) ein.

## 3. Bewusst nicht

- Kein Eintrag in `interval/drivers.json`, kein neues Register, keine Code-Änderung heute.
- Kein zweiter Versuch bei ipcinfo.org oder ReliefWeb, keine Anfrage nach einer ReliefWeb-Kennung
  (das wäre eine Nachricht an Dritte).
- Die zweite GRFC-Datei (`grfc_amn_database_2022-2024.xlsx`, 6,2 MB, Mangelernährung) und die
  älteren Fassungen sind nicht abgerufen.
