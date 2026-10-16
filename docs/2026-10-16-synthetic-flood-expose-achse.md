# The Synthetic Flood — erneuertes Exposé: die Achse

**Datum:** 2026-10-16 (zweiter Pass des Tages) · **Stufe:** EXPOSÉ, erneuert · **Vorgänger:**
`docs/2026-08-08-kandidat-synthetic-flood.md` (Exposé), `docs/2026-08-22-kandidaten-re-audit.md`
§3 (Blocker), Wiederaufnahme 2026-10-04 am Ende des Exposés · **Anlass:** Der Fokus wartet —
The Interval öffnet sein Fenster erst am Montag 2026-10-19 (`interval/experiment.json`),
Planetary Listening wartet auf die erste Lesung seines eigenen Workflows
(`discovery/AGENDA.md`). `discovery/PROMPT.md` Schritt 2 erlaubt dann ein Exposé pro Woche;
dies ist das der Woche.

Dieses Dokument benennt die Achse, die der Re-Audit verlangt, und baut die Frage für den
Takt, den die Hauptzahl hat. Jede Aussage über Endpunkte, Lizenzen, Raten und Größen ist
**ungeprüft** und gehört dem AUDIT. Geprüft ist heute nur, dass die vier unten genannten
Nachbararbeiten unter ihren Adressen erreichbar sind (HTTP 200 auf `arxiv.org/abs/<id>`,
2026-10-16).

## 1. Die Frage, enger als 2026-08-08

> Wie verändert sich, Monat für Monat, der Anteil maschinell mitgeschriebener Sprache in
> zwei öffentlichen Registern, die einander nicht kennen — biomedizinische Abstracts und die
> Selbstmarkierung einer Enzyklopädie — und wie schnell verliert die Messmethode selbst ihre
> Sicht, wenn die Schreibenden die verräterischen Wörter meiden?

Die zweite Hälfte ist neu und ist der Kern. Die „excess vocabulary"-Methode zählt Wörter,
deren Häufigkeit nach 2022 über ihre eigene Vorgeschichte hinausschießt. Sobald diese Wörter
bekannt sind, werden sie gemieden oder ausgetauscht; die Methode sieht dann weniger, ohne
dass weniger maschinell geschrieben wird. Ein einmaliges Paper kann diesen Verfall nicht
sehen, weil es zu einem Zeitpunkt misst. Eine Messreihe, die jeden Monat dieselbe
committete Wortliste **und** eine neu abgeleitete Liste nebeneinander führt, sieht ihn: die
Divergenz der beiden Listen ist die Halbwertszeit der Methode.

## 2. Die Achse — kein GDELT (Blocker 1 des Re-Audits)

**Register A, Fundament: biomedizinische Abstracts über PubMed E-utilities.**
Monatskohorten nach Publikationsdatum; je Kohorte die Häufigkeit einer committeten
Wortliste (Wörter, die in der Basisperiode 2018–2022 stabil waren und danach ausschlagen)
gegen die Basis, und dieselbe Rechnung mit einer jeden Monat neu abgeleiteten Liste.
Committet würden Zählungen, die Liste, die deterministische Anfrage als
Wiederholungsanweisung und SHA-256 der empfangenen Bytes — keine Abstracts, solange das
AUDIT die Lizenzlage der Texte nicht geklärt hat (*referenced, not stored*, wie Dark Ocean V0).
Das ist eine **strukturelle** Messung im Sinne des Exposés: Worthäufigkeiten, kein
Detektor. OpenAlex und Crossref sind Ausweich- und Kontrollquellen; welche trägt, ist eine
AUDIT-Frage.

**Register B, unabhängig: Wikipedias eigene Markierung.** Die Wartungskategorie, in die
Bearbeitende Artikel mit mutmaßlich maschinengeschriebenem Text einsortieren, als tägliche
Zählung über die MediaWiki-API, monatlich verdichtet. Das ist kein Detektor der Praxis,
sondern menschliche Aufmerksamkeit, die maschinell gezählt wird — die Zahl misst, wie viel
Prüfarbeit die Gemeinschaft aufbringt, nicht wie viel Text maschinell ist, und wird so
benannt. Nur Zählungen, keine Seitentitel, keine Benutzernamen (I8, E-2: eine Markierung ist
ein Verdacht, keine Feststellung, und die Praxis macht sie nicht zu einer Liste).

**Common Crawl** bleibt die im Exposé geplante Breitenachse, ist heute aber **nicht** die
Achse: auch über HTTPS bleibt das Volumen eine Compute-Frage, die der Re-Audit offen
gelassen hat. Das AUDIT darf prüfen, ob ein Index-Ausschnitt (`index.commoncrawl.org`) eine
kleine Kontrollprobe trägt; die Monatszahl hängt nicht daran.

**Abgrenzung zu The Consensus:** keine Nachrichtenschicht, keine GDELT-Phrasen, keine
gemeinsame Quelle. Die Dopplung, die der Re-Audit fand, entfällt mit der Achse.

## 3. Der Takt (Blocker 2 des Re-Audits)

Die Hauptzahl ist ein Monatsanteil. Deshalb:

- **Lesung je Monatskohorte, mehrfach.** PubMed indexiert nachlaufend; eine Kohorte M wird
  bei M+1, M+2 und M+3 gelesen, und die Revision zwischen den Lesungen ist ein verglichenes
  Ereignis, kein Fehler (wie die Re-Ingestion bei Planetary Listening,
  `docs/2026-10-15-planetary-listening-v0-inkrement-2.md`). Erst M+3 zählt als Wert.
- **Längsschnitt ab Tag eins.** Die Basisperiode 2018–2022 und die Monate seither sind
  heute lesbar; V0 könnte die Reihe rückwirkend aufbauen, die Messung beginnt also nicht bei
  null. Rückwirkende Werte werden als solche markiert und nicht als Vorhersage gewertet.
- **Abnahmefenster in Monaten.** Ein E-Experiment für diesen Kandidaten misst über
  mindestens sechs aufeinanderfolgende Kohorten mit je drei Lesungen, nicht über vierzehn
  Nächte. Das ist ein Hinweis an die spätere Kriterien-Datei, keine Festlegung.

## 4. Warum nur anhaltende Maschinenaufmerksamkeit das beantworten kann

Die Frage verlangt drei Dinge zugleich, die keine Einzelstudie leistet: dieselbe Methode
jeden Monat unverändert anwenden (sonst ist Drift nicht von Methodenwechsel zu trennen), sie
**zugleich** jeden Monat neu ableiten (sonst bleibt der Verfall unsichtbar), und jede Lesung
mit ihren Bytes so festhalten, dass ein Dritter sie Monate später wiederholen und die
Revisionen nachzählen kann. Die Arbeit ist Zählen über Millionen Datensätze, monatlich,
ohne Ende — Aufmerksamkeit, die eine Person nicht aufbringt und ein Paper nicht vorsieht.

## 5. Die nächsten Nachbarn, und das Tageslicht

| Nachbar | Was er tut | Tageslicht |
|---|---|---|
| Kobak et al., „Delving into LLM-assisted writing in biomedical publications through excess vocabulary", [arXiv:2406.07016](https://arxiv.org/abs/2406.07016) | Die Methode selbst: Überschuss-Vokabular in PubMed-Abstracts 2010–2024. | Ein Zeitpunkt, eine Liste. Hier: Methode als Nachbar, nicht als Kopie — monatlich, mit zweiter, neu abgeleiteter Liste und dem Verfall als Größe. |
| Liang et al., „Mapping the Increasing Use of LLMs in Scientific Papers", [arXiv:2404.01268](https://arxiv.org/abs/2404.01268) | Verteilungsschätzung des maschinell veränderten Anteils über Preprint- und Journal-Korpora. | Modellbasierte Schätzung über einen festen Zeitraum, kein laufendes öffentliches Archiv. |
| Liang et al., „The Widespread Adoption of Large Language Model-Assisted Writing Across Society", [arXiv:2502.09747](https://arxiv.org/abs/2502.09747) | Dieselbe Schätzung über Beschwerden, Pressemitteilungen, Stellenanzeigen, UN-Texte. | Breite statt Dauer; die Reihe endet mit dem Paper. |
| Brooks, Eggert, Peskoff, „The Rise of AI-Generated Content in Wikipedia", [arXiv:2410.08044](https://arxiv.org/abs/2410.08044) | Detektoren auf neu angelegten Artikeln. | Detektor statt Selbstmarkierung; Register B zählt die menschliche Markierung, nicht ein Detektorurteil. |
| Kommerzielle Tracker und Marketing-Studien (Exposé 2026-08-08, Abschnitt Nachbarschaften) | Listen und Einzelzahlen. | Keine Provenienz, kein Archiv, keine Wiederholbarkeit. |
| Die Gemeinschaftsinitiative auf Wikipedia, die maschinengeschriebenen Text aufspürt und markiert | Die Arbeit, die Register B zählt. | Sie markiert; die Praxis zählt nur, monatlich und datiert, und macht keine Liste daraus. |

## 6. Grenzen, ehrlich

- Überschuss-Vokabular misst **Spuren**, nicht Urheberschaft. Ein Anstieg kann Mode sein;
  die Basisperiode und Kontrollwörter (stabile Funktionswörter) sind die Negativkontrolle,
  die das AUDIT festlegen muss.
- Register B misst Markierungsarbeit; ihr Anstieg kann mehr Prüfende statt mehr
  maschinellen Text bedeuten. Das steht neben jeder Zahl.
- Englischsprachiger Bias in Register A. Eine zweite Sprache ist eine spätere Frage.
- Die Detektionsschicht des Exposés (Schätzschicht obenauf) ist hier bewusst nicht
  enthalten; sie kann später als ausgewiesen unsichere Schicht dazukommen.

## 7. Was das AUDIT prüfen muss

Für PubMed E-utilities, OpenAlex, Crossref, die MediaWiki-API und den Common-Crawl-Index je:
exakter Endpunkt, HTTP-Status, Größe einer Monatsanfrage, Ratengrenze ohne Schlüssel, Lizenz
der Metadaten **und** der Abstract-Texte, ob innerhalb der Delegations-Charta (öffentlich,
ohne Login, ohne Kosten, ohne personenbezogene Daten), und eine Probe mit Manifest unter
`syntheticflood/probes/<date>/`. Außerdem: ob die Kategorie in Register B einen stabilen
Namen und eine abfragbare Größe hat, und ob ihre Historie rückwirkend lesbar ist. Endet in
einer Empfehlung; das GO für V0 ist laut Wiederaufnahme vom 2026-10-04 erteilt, **sofern** das
AUDIT beide Blocker ausräumt.

## Bewusst nicht heute

Keine Quelle abgefragt außer den vier Paper-Adressen; keine Bytes konserviert; kein Code;
kein Detektor; keine Wortliste festgelegt. Common Crawl nicht als Achse genommen.
