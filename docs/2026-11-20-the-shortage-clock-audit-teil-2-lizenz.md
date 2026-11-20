# The Shortage Clock — AUDIT, Teil 2, Punkt 2: Lizenz

**Datum:** 2026-11-20 · **Stufe:** AUDIT (Teil 2, Punkt 2 von 2) · **Teil 1:**
`docs/2026-11-19-the-shortage-clock-audit-teil-1.md` · **Proben:** `shortageclock/probes/2026-11-20/manifest.json`
(6 Abrufe, je ein Versuch, kein Wiederholen, 07:39–07:40 UTC).

**Anlass.** Teil 1 ließ zwei Punkte offen (§5): die Uhr an zwei Tagen (frühestens 2026-11-21, ein
Abstand von zwei Tagen zum ersten Abzug) und die Lizenz der BfArM-Datei. Der zweite Punkt braucht
keinen Abstand; er ist der Schritt dieser Nacht. Alle früheren Kandidaten mit einem nächsten Schritt
warten weiter auf ein Tor des Maintainers (`REQUESTS.md` 2026-11-04, 2026-11-16, 2026-11-17).

**Offen gesagt:** Vor den konservierten Abrufen wurden dieselben Seiten (außer der Kopie des
Impressums) einmal mit einem Kommandozeilen-Client gelesen, um die richtigen Adressen zu finden
(dabei: `…/lieferengpassmeldungen/faces/public/index.xhtml` 404, die EMA-Adresse aus der Suche 301
auf die unten genannte). Nichts davon ist aufbewahrt; was hier steht, stützt sich nur auf die Proben.

## 1. Was konserviert wurde

Auszüge statt ganzer Seiten: Die Seiten sind überwiegend Navigation, das BfArM-Impressum nennt
natürliche Personen (I8), die Trefferliste des Registers trägt Produktnamen mit Firmennamen (E-2).
Jede Manifestzeile hält `full_sha256` der empfangenen Bytes und `derivation` mit der genauen Regel.

| Datei | Adresse | Status | Was sie zeigt |
|---|---|---|---|
| `bfarm/pharmnet-robots.txt` | `anwendungen.pharmnet-bund.de/robots.txt` | 200 (402 B, ganz) | `/lieferengpassmeldungen/` nicht gesperrt (wie Exposé §6) |
| `bfarm/meldungen-page-excerpt.txt` | `…/lieferengpassmeldungen/faces/public/meldungen.xhtml` | 200 | Hinweistext und CSV-Satz; **kein Lizenz-, Nutzungs- oder Urheberhinweis, kein Impressum-Link** auf der Seite |
| `bfarm/bfarm-robots.status.json` | `www.bfarm.de/robots.txt` | 404 | keine `robots.txt` |
| `bfarm/bfarm-impressum-copyright-excerpt.txt` | `www.bfarm.de/DE/Service/Impressum/_node.html` | 200 | Abschnitt „Copyright" |
| `bfarm/govdata-search-lieferengpass.json` | Suche „Lieferengpass" im offenen Datenkatalog des Bundes | 200 (ganz) | `count: 0` — der Datensatz ist dort nicht als offene Daten eingetragen |
| `ema/ema-legal-notice-copyright-excerpt.txt` | `www.ema.europa.eu/en/about-us/about-website/legal-notice` | 200 | Abschnitt „copyright and limited reproduction notices" |

## 2. Befund

**BfArM.** Das Impressum des BfArM sagt wörtlich (`bfarm/bfarm-impressum-copyright-excerpt.txt`):
„Das Copyright für Texte und Bilder liegt, soweit nicht anders vermerkt, beim BfArM. Die im
Internetangebot zur Verfügung gestellten Texte, Textteile, Grafiken, Tabellen oder Bildmaterialien
dürfen ohne vorherige Zustimmung des BfArM nicht vervielfältigt, verbreitet oder ausgestellt werden."
Die Registerseite selbst, auf einem anderen Host, nennt keinerlei Bedingungen; sie bietet die CSV
„automatisiert über folgenden Link abzurufen" an und sagt, die Einstellung erfolge „unter der
alleinigen Verantwortung der jeweiligen Zulassungsinhaber" (`bfarm/meldungen-page-excerpt.txt`).
Im offenen Datenkatalog des Bundes steht der Datensatz nicht (`count: 0`), also auch unter keiner
Datenlizenz.

Lesart, nicht bewiesen: Der Abruf ist erlaubt und erwünscht; ob das Committen abgeleiteter Zeilen
(Kennung, Daten, Status) in ein öffentliches Repository eine Vervielfältigung oder Verbreitung im
Sinne des Impressums ist, ob das Impressum von `www.bfarm.de` die Datei auf
`anwendungen.pharmnet-bund.de` überhaupt erfasst, und ob gemeldete Tatsachen und Daten dort
überhaupt gemeint sind, kann diese Nacht nicht entscheiden. Ein ausdrücklicher Vorbehalt der
Zustimmung steht im Raum — damit ist es eine Quelle mit ungeklärter Lizenz, und die Entscheidung ist
die des Maintainers (`discovery/PROMPT.md`). Die Probe vom 2026-11-19 (`bfarm/lieferengpassmeldungen.csv`,
abgeleitete Kopie) bleibt, wie sie ist; sie wird nicht erweitert, bis er entschieden hat.

**EMA.** Wiederverwendung für nicht-kommerzielle und kommerzielle Zwecke erlaubt, „provided that
EMA is always acknowledged as the source of the material. Such acknowledgement must be included in
each copy of the material"; ausgenommen sind Inhalte Dritter (`ema/ema-legal-notice-copyright-excerpt.txt`).
Die Engpassliste ist ein von EMA erzeugter Bericht (Teil 1 §2), also kein Inhalt Dritter. **Innerhalb
der Charta**, mit Quellenangabe in jeder Kopie — ein V0 schriebe sie in jede Datei, die Zeilen der EMA
trägt.

**openFDA.** Unverändert CC0 (Teil 1, `shortageclock/probes/2026-11-19/openfda/license.html`).

**Nebenbefund, nicht verfolgt:** Die Registerseite nennt in der Grundansicht 553 gefundene
Lieferengpässe; die CSV vom Vortag trug 942 Meldungen (Teil 1 §3). Ob die Seite vorfiltert (etwa
ohne Löschmeldungen) oder die CSV mehr enthält, ist eine Frage für Teil 2, Punkt 1.

## 3. Was daraus für die Empfehlung folgt

Zwei der drei Register (openFDA CC0, EMA mit Quellenangabe) sind lizenzrechtlich innerhalb der Charta;
openFDA ist die Hauptquelle mit der meisten Masse. Das BfArM-Register, das das Exposé (§7) als zweite
Seite für nötig hielt, ist es nicht ohne die Entscheidung des Maintainers. Vorgelegt in `REQUESTS.md`
(2026-11-20). Bis dahin plant Teil 2, Punkt 1 (ab 2026-11-21) den Vergleich der Uhren für openFDA und
EMA wie vorgesehen; für das BfArM wird ein zweiter Abzug nur gelesen und **als Zählung** festgehalten
(Meldungen, Kennungen gefallen/neu, Uhrfelder geändert — als Zahlen und Hashes, keine neuen Zeilen),
bis die Antwort da ist. Die endgültige Empfehlung folgt nach Punkt 1.

## Bewusst nicht heute

Kein zweiter Abzug der drei Dateien (Abstand: frühestens 2026-11-21). Keine Anfrage an das BfArM —
etwas zu senden ist die Sache des Maintainers. Kein Code, kein Workflow (V0 braucht sein GO). Kein
Hersteller und kein Produktname in diesem Dokument.
