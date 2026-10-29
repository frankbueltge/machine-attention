# The Afterlife — Exposé

**Datum:** 2026-10-29 · **Stufe:** EXPOSÉ · **Anlass:** Der Fokus wartet. The Interval steht in
seinem Fenster und hat donnerstags nichts fällig (`interval/experiment.json`, Wochen 2026-10-19
bis 2026-11-09; Tally heute: Wochen fällig 2 von 4, A1 keine fehlende Woche, A2 pass, A3 keine).
Planetary Listening läuft in seinem eigenen Fenster (`planetary/experiment.json`). The Synthetic
Flood wartet auf die Lesung M+2 ab 2026-11-01, The Declared Network auf `REQUESTS.md`
(2026-10-23) (`discovery/AGENDA.md`). Laut `discovery/PROMPT.md` Schritt 2 darf dann ein neues
Exposé pro Woche entstehen. In der ISO-Woche 44 (ab 2026-10-26) ist keines entstanden; das
letzte war The Declared Network am 2026-10-23 (`docs/2026-10-23-kandidat-declared-network.md`).
Dies ist das Exposé dieser Woche.

Jede Aussage über Endpunkte, Formate, Lizenzen und Raten ist **ungeprüft** und gehört dem AUDIT.
Geprüft ist heute nur die Erreichbarkeit der Adressen unten: einmaliger Status-Abruf am
2026-10-29 zwischen 07:0x und 07:1x UTC, Ergebnisse in §5. Keine Bytes wurden konserviert, kein
Datensatz gelesen, keine Zahl aus einer Antwort übernommen.

## 1. Die Frage

> Wie lange steht eine zurückgezogene wissenschaftliche Arbeit an den Orten, an denen man sie
> findet, noch als gültig da, nachdem ihre Zurückziehung erklärt ist?

Das ist wieder die Operation des Gründungskorpus (`docs/2026-08-08-projekt-aufnahme.md`): eine
öffentliche Darstellung eines Zustands neben einer anderen Darstellung desselben Zustands. Hier:
**erklärt ≠ verbreitet.** Die Erklärung ist die Rückzugsnotiz des Verlags, registriert als
Beziehung `retraction` auf der DOI der Originalarbeit und in der Retraction-Watch-Datenbank, die
seit 2023 offen über Crossref verteilt wird. Die Verbreitung ist das, was die großen Nachweise
zeigen, über die Forschende, Gutachtende und Maschinen eine Arbeit finden: der Publikationstyp
„Retracted Publication" in PubMed, das Feld `is_retracted` in OpenAlex, die Update-Beziehung in
den Crossref-Metadaten der Originalarbeit selbst.

Die Messgröße ist die **Nachweis-Nachlaufzeit**: die Tage zwischen dem erklärten Rückzugsdatum
und dem ersten Tag, an dem ein Nachweis die Arbeit als zurückgezogen zeigt. Bei Arbeiten, die ein
Nachweis nie markiert, bleibt die Uhr offen, wie bei den laufenden Episoden von The Interval
(`docs/2026-10-04-kandidat-the-interval.md` §3.5) und bei der Erklärungs-Nachlaufzeit von The
Declared Network (`docs/2026-10-23-kandidat-declared-network.md` §1). Die drei Kandidaten teilen
eine Form: ein Register sagt etwas, ein zweites holt es später oder nie nach, und nur wer beide
jeden Tag gesichert hat, kann sagen, wie lange.

## 2. Warum nur anhaltende maschinelle Aufmerksamkeit das beantworten kann

- **Kein Nachweis datiert seine eigene Markierung.** PubMed zeigt heute, dass eine Arbeit
  zurückgezogen ist, nicht seit wann es das zeigt (ungeprüft, AUDIT: ob die Datumsfelder eines
  Datensatzes die Markierung datieren). OpenAlex überschreibt `is_retracted` in seinem Snapshot.
  Nach der Korrektur ist der Zustand davor verschwunden. Das ist die Lehre von Memory Hole: Was
  überschrieben wird, existiert nur, wenn jemand es vorher gesichert hat. Die Nachlaufzeit ist
  deshalb **nicht rückwirkend** messbar; die Messung beginnt bei null, und das steht in jeder
  späteren Ausgabe.
- **Die Arbeit ist tägliches Nachsehen ohne Ende.** Jeden Tag kommen neue Rückzüge hinzu; jeder
  muss in drei Nachweisen Tag für Tag nachgeschlagen werden, bis alle drei ihn zeigen, manchmal
  Monate lang. Diese Aufmerksamkeit bringt keine Person auf, und die Nachweise selbst haben keinen
  Grund, ihre eigene Verspätung zu messen.
- **Wiederholbarkeit.** Jeder Tageswert wird mit den SHA-256 der empfangenen Bytes festgehalten,
  wie es `verify.py` heute für die Zählungen der Synthetic Flood tut (`check_syntheticflood`:
  jede Zählung an den Hash ihrer kanonischen Antwort gebunden). Ein Dritter kann Monate später
  nachzählen, an welchem Tag ein Nachweis eine Arbeit zuerst als zurückgezogen zeigte.

## 3. Datenlage-Kurzcheck (ungeprüft, für das AUDIT)

| Seite | Kandidat-Quelle | Was das AUDIT klären muss |
|---|---|---|
| Erklärung | Retraction-Watch-Daten über Crossref (Dokumentationsseite 200; Repositorium `gitlab.com/crossref/retraction-watch-data` 200) | Format und Größe des Abzugs, Takt der Aktualisierung, Lizenz, welches Datum „Rückzugsdatum" heißt (Notiz, Eintrag, Online-Stellung). **Personendaten:** Der Abzug trägt vermutlich Autorennamen. Diese Spalten werden nie gelesen und nie gesichert (I8); geht das nur durch Laden der ganzen Datei, ist das ein AUDIT-Befund gegen die Quelle, wie die Kontaktfelder bei OSCAR (`docs/2026-10-23-kandidat-declared-network.md` §3). |
| Erklärung, zweite Hand | Crossref REST API, Filter `update-type:retraction` (heute **429**, siehe §5) | Rate ohne Schlüssel von einem Runner aus, ob der Filter Rückzugsnotizen mit Datum und Ziel-DOI liefert, ob die Originalarbeit die Beziehung selbst trägt. |
| Nachweis A | PubMed E-utilities, Publikationstyp `Retracted Publication` (heute 200) | Ob eine Zählung oder eine ID-Liste je Tag reicht (PMIDs, keine Titel), ob die Abbildung DOI → PMID schlüsselfrei geht, Rate (3 req/s keyless, wie im Synthetic-Flood-Audit gemessen, `docs/2026-10-18-synthetic-flood-audit.md`). |
| Nachweis B | OpenAlex, Filter `is_retracted:true` (heute **429**) | Das Budget auf der geteilten Ausgangsadresse war schon im Synthetic-Flood-Audit knapp (807 → 412 in Sekunden). Ob OpenAlex tragen kann oder nur Kontrolle ist, entscheidet das AUDIT von einem Runner aus. |

**Rückwirkend:** Die Erklärungsseite ist rückwirkend vollständig (Rückzugsdaten seit Jahrzehnten).
Die Nachweisseite ist es nicht. Am ersten Tag kann V0 deshalb nur einen Bestand feststellen: wie
viele erklärte Rückzüge ein Nachweis heute noch nicht zeigt. Das ist ein Zustand, keine
Nachlaufzeit, und wird so beschriftet.

## 4. V0-Skizze (nur Form, keine Festlegung)

Einheit: **erklärter Rückzug × Nachweis × Tag**, verdichtet zu **Nachweis × Monat des
Rückzugsdatums**. Kohorte: alle Rückzüge, deren erklärtes Datum ab dem ersten V0-Tag liegt, dazu
ein fester Bestand der 90 Tage davor als Kontext. Täglich je offenem Rückzug eine Nachfrage je
Nachweis, bis alle drei ihn zeigen oder eine vorab festgelegte Frist (etwa 365 Tage) abläuft.
Committet werden DOI, PMID, Nachweis, Zustand, SHA-256 der Antwort und die
Wiederholungsanweisung — kein Titel, kein Name, kein Abstract. Ereignisse: `declared`,
`marked:<nachweis>`, `unmarked:<nachweis>` (ein Nachweis nimmt die Markierung zurück; erwartet
selten, gerade deshalb gezählt), `withdrawn_declaration` (der Rückzug selbst wird
zurückgenommen). Die Nachlaufzeit ist `marked − declared`, als Verteilung je Nachweis, nie als
einzelne Zahl. Die Klasse ist vermutlich **Instrument**: Die Messung trägt ohne Bühne.

Substrat: Der PubMed-Leser der Synthetic Flood (`practice/src/practice/syntheticflood/pubmed.py`)
ist dieselbe Schnittstelle; V0 würde ihn teilen, nicht kopieren.

## 5. Die nächsten Nachbarn, und das Tageslicht

| Nachbar | Was er tut | Tageslicht | Erreichbar 2026-10-29 |
|---|---|---|---|
| [Retraction Watch Database](https://retractionwatch.com/retraction-watch-database-user-guide/), seit 2023 offen über [Crossref](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/) ([Ankündigung](https://www.crossref.org/blog/news-crossref-and-retraction-watch/)) | Das Register der Rückzüge selbst, mit Datum und Grund. | **Der nächste Nachbar, und er ist die Erklärungsseite.** Er sagt, *dass* zurückgezogen wurde, nicht, wie lange PubMed oder OpenAlex danach die Arbeit noch ohne Markierung ausliefern. Die Praxis würde ihn lesen, nicht ersetzen. | 200 / 200 / 200 |
| [Crossmark](https://www.crossref.org/documentation/crossmark/) | Ein Verlagsdienst, der auf der Artikelseite den aktuellen Status anzeigt. | Zeigt den Stand am Ort des Verlags, heute. Ob die Nachweise ihn übernommen haben, zeigt er nicht. | 200 |
| [Problematic Paper Screener](https://dbrech.irit.fr/pls/apex/f?p=9999:1) (IRIT, Toulouse), darin der „Feet of Clay"-Detektor | Findet Arbeiten, die zurückgezogene Arbeiten zitieren, laufend. | Misst die **Zitierung** nach dem Rückzug, also die Verbreitung in neuer Literatur, nicht die Nachlaufzeit der Nachweise. Der Fragegegenstand liegt eine Stufe früher: Wer zitiert, hat die Markierung vielleicht nie gesehen. | 200 |
| Studie zur Gültigkeit der Rückzugsmarkierung in PubMed und Web of Science, JASIST 2018 ([doi:10.1002/asi.24008](https://doi.org/10.1002/asi.24008)) | Einmalige Prüfung, wie vollständig zwei Nachweise Rückzüge markieren. | Ein Zeitpunkt, keine Reihe. Sie zeigt, *dass* Markierungen fehlen; die Dauer bis zur Markierung kann ein Zeitpunkt nicht messen. Titel und Inhalt nach Kenntnis der Praxis, im AUDIT am Text zu prüfen (Verlagsseite heute 403 hinter Prüfseite, DOI löst auf). | 302 → 403 |
| RISRS-Empfehlungen, *Research Integrity and Peer Review* 2022 ([doi:10.1186/s41073-022-00125-x](https://doi.org/10.1186/s41073-022-00125-x)) | Empfehlungen, die unbeabsichtigte Weiterverbreitung zurückgezogener Arbeiten zu verringern, darunter einheitliche Anzeige in Datenbanken. | Programm, keine Messung. Eine gemessene Nachlaufzeit je Nachweis wäre genau die Zahl, an der sich solche Empfehlungen prüfen ließen. Inhalt im AUDIT am Text zu prüfen. | 302 |
| [NLM-Richtlinie zu Errata und Rückzügen](https://www.nlm.nih.gov/bsd/policy/errata.html) | Beschreibt, wie PubMed Rückzugsnotizen verknüpft und markiert. | Regel, nicht Verlauf. Sie sagt, was geschehen soll, nicht wann es geschah. | 200 |

Eine zweite Adresse aus dem Umfeld der RISRS-Arbeit (`researchintegrityjournal.biomedcentral.com`,
Artikel `s41073-020-00106-1`) antwortete 404 und steht deshalb nicht in der Tabelle. Die
Schnittstellen von Crossref und OpenAlex antworteten auf den einen Status-Abruf **429**; das ist
kein Urteil über die Quellen, sondern das bekannte Bild der geteilten Ausgangsadresse dieses
Containers (`docs/2026-10-20-synthetic-flood-v0-schritt-2b.md`). Kein zweiter Versuch.

## 6. Grenzen, ehrlich

- **Keine Anschuldigung (E-2).** Ein Rückzug kann ehrlicher Fehler, Verlagsversehen oder
  Fehlverhalten sein; die Praxis liest den Grund nicht und speichert ihn nicht. Gemessen wird nur
  die Nachlaufzeit der Nachweise, und auch sie benennt keinen Schuldigen: Ein Nachweis kann
  spät markieren, weil der Verlag die Notiz spät oder ohne Verknüpfung geliefert hat. Verlage und
  Zeitschriften erscheinen in V0 nicht als Einheit, nur die drei Nachweise als Aggregat.
- **Keine Personen (I8).** Keine Autorennamen, keine Titel (Titel können Namen tragen), keine
  Abstracts. Nur DOI und PMID.
- **„Nicht markiert" ist nicht „nicht gefunden".** Ein Nachweis kann die Rückzugsnotiz als
  eigenen Datensatz führen und die Originalarbeit trotzdem unmarkiert ausliefern. Die Frage
  handelt von der Originalarbeit, und das steht neben jeder Zahl.
- **Das Rückzugsdatum ist mehrdeutig** (Notiz gedruckt, online, in der Datenbank eingetragen).
  Welches gilt, wird vor dem ersten Abruf festgelegt und nie still gewechselt.
- **Fachliche Schlagseite.** PubMed deckt Biomedizin ab. Die Nachlaufzeit von Nachweis A gilt
  nur für Rückzüge mit PMID, und das steht neben jeder Zahl.

## 7. Was das AUDIT prüfen muss

Für den Retraction-Watch-Abzug über Crossref, die Crossref REST API, PubMed E-utilities und
OpenAlex je: exakter Endpunkt, HTTP-Status, Größe eines Tagesabrufs, Ratengrenze ohne Schlüssel,
Lizenz, `robots.txt` und etwaige Bitten an automatisierte Abrufer (Lehre aus FEWS NET und
OSCAR), ob innerhalb der Delegations-Charta (öffentlich, ohne Login, ohne Kosten, ohne
personenbezogene Daten), und eine Probe mit Manifest unter `afterlife/probes/<date>/`. Außerdem:
ob sich die Personenspalten des Abzugs vor dem Sichern abtrennen lassen; ob irgendein Nachweis
seine Markierung datiert (dann wäre ein Teil rückwirkend messbar und das Tageslicht kleiner); ob
die 429 von Crossref und OpenAlex an der Ausgangsadresse liegen (Gegentest auf einem Runner, wie
in `REQUESTS.md` für Memory Hole und die Synthetic Flood schon gefragt). Am Ende steht eine
Empfehlung. Das GO für V0 ist laut Aufnahme-Pfad das des Maintainers; das AUDIT braucht es
nicht.

## Bewusst nicht heute

Keine Quelle abgefragt außer einem Status-Abruf je Adresse, kein zweiter Versuch nach 429. Keine
Bytes konserviert, kein Code, kein Verzeichnis `afterlife/`. Keine Kohorte, keine Frist, kein
Rückzugsdatum festgelegt. Der Fokus ist unberührt. Ob ein dritter wartender Kandidat neben der
Synthetic Flood und The Declared Network der Praxis dient oder sie zerstreut, steht im
`discovery/AGENDA.md` offen; das AUDIT kommt erst, wenn kein früherer Kandidat einen fälligen
Schritt hat.
