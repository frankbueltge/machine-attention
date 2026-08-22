# Dark Ocean — E-Experiment: Review

**Datum:** 2026-08-22 · **Stufe:** 4 des Aufnahme-Pfads · **Grundlage:** Abnahmekriterien
`2026-08-09-dark-ocean-e-experiment-kriterien.md` (geschlossen seit Nacht 1)
**Ausgang: NICHT BESTANDEN.** Die Bühnen-Ambition endet mit diesem Dokument; die
nächtliche Kontinuitäts-Probe läuft als Instrument weiter (Franks Entscheidung vom
2026-08-22, Wortlaut privat).

## 0. Warum dieses Review zwei Tage früher steht als geplant

Der Fahrplan nannte den **24.08.** Dieses Review ist am **22.08.** geschrieben, weil das
tragende Kriterium B3 **arithmetisch abgeschlossen** ist: es verlangt ≥ 12 Nächte mit
Sample innerhalb ±90 min um 04:50 UTC, und mehr als **10** sind im Fenster nicht mehr
erreichbar — unabhängig davon, was in der letzten Nacht passiert. Der Befund selbst ist
nicht neu: er steht seit dem 2026-08-14 im Autonomie-Log (`stale-stage-rescue`,
`window_arithmetic`).

Was das Vorziehen **nicht** ist: ein Abbruch. Nacht 14 läuft und committet wie geplant
(Lauf 04:50 UTC am 23.08., Lesung für den 22.08.); es wird nichts mitten im Fenster
abgeschaltet und nichts nachträglich aus dem Record entfernt. Die Latte wird nicht
verschoben — sie wird abgerechnet, während der Ball noch fliegt, weil sein Aufschlagpunkt
schon feststeht.

## 1. A — Betrieb

| # | Verlangt | Nachgerechnet | Urteil |
|---|---|---|---|
| A1 | ≥ 12 von 14 Nächten vollständig committet | **11 committet** (Lesungen 08-11 … 08-21), **12 mit Nacht 14** | erfüllt genau an der Latte, null Reserve |
| A2 | jede fehlende Nacht mit benannter Ursache | Nächte **08-09 und 08-10** verloren an den Anchor-Deadlock (`verify` verlangte den Manifest-Eintrag, den nur der Anchor-Job nach dem Merge setzen konnte); Ursache, Reparatur und „kein Backfill" stehen im Log vom 2026-08-12 | **erfüllt** |
| A3 | `verify.py` grün auf jeder committeten Nacht | CI-Gate, grün auf allen 13 Lesungen (11 im Fenster) | **erfüllt** |
| A4 | 0 € | 0,00 € über alle Läufe, keyless-Pfad hielt, keine Eskalation aktiviert | **erfüllt** |

## 2. B — Trägt die Messung?

| # | Verlangt | Nachgerechnet | Urteil |
|---|---|---|---|
| B1 | Deklarations-Hülle committet, Kennzahl innerhalb der Hülle | Hülle steht je Nacht (`cells_declared_sample`); die Innen-Hülle-Zahlen (`cells_observed_and_declared_sample`, `cells_declared_unobserved_today`) stehen neben der Außen-Zahl | **erfüllt** |
| B2 | Baseline über das Fenster: Median und Streuung | siehe §3 — hiermit committet | **erfüllt** |
| B3 | ≥ 12 Nächte Sample innerhalb ±90 min um 04:50 UTC | **9 committet** (08-12, 08-14 … 08-21), **10 mit Nacht 14**. 08-11 wurde um 22:09 gezogen, 08-13 um 21:00 — beide nach einer Reparatur per Dispatch, beide auf dem Record | **NICHT ERFÜLLT — max. 10 von 12** |
| B4 | ≥ 1 Ausreißer erklärt oder als offene Frage committet | siehe §3, als offene Frage committet | **erfüllt** |

Damit ist **B unvollständig.** Die Abnahmeregel lautet: bestanden = A **und** B **und** D
vollständig, E ohne Verstoß. Sie ist nicht erfüllt.

## 3. Die Baseline des Fensters (B2) und ihr Ausreißer (B4)

Elf committete Nächte, aus den konservierten Records nachgerechnet, ohne frischen Abruf:

| Größe | Median | Min | Max | σ |
|---|---|---|---|---|
| Aufnahmen (Sentinel-1) | 41 | 33 | 46 | 4,1 |
| beobachtete Bins | 579 | 549 | 723 | 61,2 |
| deklarierte Bins (Hülle) | 158 | 119 | 228 | 36,9 |
| deklarierte Schiffe | 1064 | 868 | 1427 | 199,9 |
| Diskrepanzrate **innerhalb** der Hülle | 51,5 % | 29,5 % | 66,1 % | 12,9 |

**Der Ausreißer, als offene Frage committet:** Die Innen-Hülle-Rate schwankt um ±19
Prozentpunkte (29,5 % am 08-12 gegen 66,1 % am 08-15) — bei einer Radar-Achse, deren
Aufnahmezahl im gleichen Fenster nur zwischen 33 und 46 wandert. Die zwei
außerplanmäßigen Abendproben (08-11, 08-13) liegen dabei *nicht* an den Rändern der
Verteilung, sondern mitten drin, während die höchsten Werte auf planmäßig gezogene Nächte
fallen. Die naheliegende Erklärung — der Tagesgang der Ostsee-Schifffahrt — ist damit
gerade **nicht** belegt. Was die Streuung erzeugt, ist aus elf Nächten nicht entscheidbar:
Satellitengeometrie (welche Bahnstreifen fielen auf welche Hülle), Empfängerreichweite und
Tageszeit sind in dieser Form konfundiert und wurden vom V0 nie getrennt. Das bleibt eine
offene Frage, keine Erklärung.

## 4. C — Werkfähigkeit

C3 ist eingelöst: `darkocean/draft/index.html` existiert als gebauter Entwurf, ein Satz,
eine Figur, ein Journal, das nach unten wächst. Genau das, was das Kriterium verlangte —
und genau deshalb ist die Antwort belastbar.

Was der Entwurf nach elf Nächten zeigt: **0 Divergenzen in 3.571 Nachfragen** an den
Katalog (11 Nächte, von 122 bis 523 nachgefragten Produkten je Nacht). Der Katalog hat sich
nie widersprochen. Das ist ein Ergebnis, und N3 nennt es zurecht eines — aber es ist genau
der Zustand, für den C4 negativ formuliert wurde: „zwei Register überlappen sich zu etwa
X %" ist eine **Instrumentenanzeige, kein Bühnen-Moment.** Alle Zeilen des Journals sind
gleich, und sie werden erst an dem Tag zwingend, an dem sich eine ändert. Der Entwurf hat
die Frage nicht beantwortet, sondern entscheidbar gemacht; das war seine Aufgabe.

## 5. D — Ehrlichkeit

- **D1 erfüllt, mehrfach:** zwei verlorene Nächte ohne Backfill auf dem Record; der
  Durchhalte-Befund, dass die zweite Achse nie ankam; die eigene, im Log berechnete
  Feststellung, dass B3 nicht mehr erreichbar ist — geschrieben, bevor jemand von außen
  danach fragte.
- **D2 in der Sache erfüllt, im Wortlaut nicht:** DMA hat in **13 von 13 Nächten** nicht
  geantwortet (`moment_axis.state: idle`, `dma_probe.state: outage: URLError`); Form (a)
  war unerreichbar, Form (b) wurde nicht gebaut. Die Lesungen sagen ehrlich, dass die
  deklarierte Achse eine Momentaufnahme einer Empfängerreichweite ist und dass „observed
  silent" eine Aussage über zwei Register ist, nie über versteckte Schiffe. Sie sagen
  **nirgends explizit, dass die Stille-Zahl an dieser Stelle unbegrenzt ist** — das
  verlangte Form (c) wortwörtlich. Als Review-Befund festgehalten, nicht als Freispruch.
  (Nebenbei korrigiert dieses Review eine Untertreibung des Kriterien-Dokuments: §5.3
  sprach von „drei Proben am 08.08."; es sind 13 Nächte durchgehender Ausfall.)

## 6. E — Charter und Ethik

Kein Verstoß. Null MMSI, null Schiffsnamen in abgeleiteten Records über alle Nächte
(vom Prüfer erzwungen, nicht nur behauptet); kein „illegal", kein „dark ship", keine
Schuldzuweisung; Lizenz-Rückgrat hielt, kein NC-Material in CC0-Ausgaben.

## 7. Ausgang und Begründung

**Dark Ocean als Projekt mit Bühnen-Ambition: beendet.** Nicht bestanden, weil B
unvollständig ist. Zwei Dinge trennen sauber:

1. **Der zufällige Teil:** Nächte 08-09 und 08-10 fielen einem Deadlock der eigenen
   Maschinerie zum Opfer; zwei Reparatur-Läufe verschoben zwei Sample-Stunden um Stunden.
   Ohne diesen Defekt wäre B3 erreichbar gewesen. Das ist Pech plus ein Bug — kein Urteil
   über den Gegenstand.
2. **Der strukturelle Teil, der schwerer wiegt:** Die zweite Achse ist nie angekommen.
   Ohne per-Moment-deklarierte Quelle bleibt die Kopfzahl eine Aussage über
   Empfängergeografie und Abtastzeitpunkt, und die stärkste wahre Behauptung nach 14
   Nächten lautet „zwei Register überlappen sich, und eines widerspricht sich nie". Das
   ist ein Instrument. Ein zweites Fenster hätte daran nichts geändert — es hätte dieselbe
   Zahl mit besserer Sample-Disziplin produziert.

**Was weiterläuft:** die Kontinuitäts-Probe (`practice.darkocean.continuity`, nächtlich in
`darkocean.yml`) — keyless, 0 €, jede Nacht eine Frage an ein öffentliches Archiv, ob es
noch sagt, was es gesagt hat. Sie läuft als **Instrument** ohne Bühne, mit derselben
Erlaubnis wie The State Before the Interface: jahrelang nichts zu finden ist ein zulässiges
Ergebnis. Ihre zwei Zahlen gehen in den Export, damit die Null sichtbar ist und nicht
stillschweigend als „läuft" erscheint.

**Was nicht weiterläuft:** die Bühnen-Erzählung, der Werk-Eintrag, der Anspruch „Coverage
vs Declaration". Der Entwurf bleibt unter `darkocean/draft/` liegen, `noindex`, als
datiertes Artefakt des Fensters. Kein Rückbau, kein Löschen — die Records bleiben, wie sie
sind.

## 8. Was dieses Review für künftige Kandidaten festhält

1. **Ein Fenster, dessen tragendes Kriterium von der eigenen Infrastruktur abhängt, misst
   die Infrastruktur.** B3 war eine Disziplin-Latte, aber gehalten wurde sie von einem
   Workflow, der zu Fensterbeginn noch reparaturbedürftig war. Künftige Kriterien nennen
   ausdrücklich, welche Läufe sie voraussetzen — und ob die Latte einen Reparatur-Lauf
   verzeiht.
2. **Ein Kriterium, das eine noch nicht erreichbare Quelle voraussetzt, ist ein
   Versprechen, kein Kriterium.** D2 hing an einer Quelle, die seit dem 08.08. ausfällt.
   Eine solche Bedingung gehört vor den Fensterstart, als Bau- oder Ausschlussfrage.
3. **Der Drei-Wege-Ausgang hat gehalten** — er hat verhindert, dass eine ehrliche
   Nullmessung entweder zur erzwungenen Bühne oder zum toten Projekt werden musste. Er
   bleibt in Kraft.
