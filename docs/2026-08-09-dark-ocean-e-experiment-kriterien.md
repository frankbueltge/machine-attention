# Dark Ocean — E-Experiment: Abnahmekriterien

**Datum:** 2026-08-09 · **Stufe:** 4 des Aufnahme-Pfads (`2026-08-08-projekt-aufnahme.md`)
**Grundlage:** Audit `2026-08-08-dark-ocean-audit.md` (GO mit vier Auflagen), V0-Baubericht
`2026-08-09-dark-ocean-v0.md` · **Status:** committet **vor** Fensterstart — das ist der
Zweck dieses Dokuments, nicht seine Formalie.

## 0. Bindung

Diese Kriterien binden ab der ersten Nacht des Fensters. **Änderungen sind bis dahin
erlaubt** (datierter Nachtrag, mit Begründung); danach nicht mehr. Wer die Latte
verschiebt, während der Ball fliegt, misst nichts — er erzählt nur.

> **Nachtrag angenommen, 2026-08-09 16:3x (Lane-Owner-Entscheidung unter Franks
> Delegation):** Die Kriteriengruppe **N — der notarielle Akt**
> (`2026-08-09-dark-ocean-kriterien-nachtrag-notariat.md`) wird **übernommen** und ist ab
> Nacht 1 Teil dieser Kriterien. Begründung: Der Nachtrag belegt mit Live-Probe, dass A–E
> die *Demonstration* messen (Überlappungszahlen) und den *Anspruch* (den Bewahrungsakt)
> gar nicht — und dass `run.py` ohne Rückblick keine Divergenz je fangen kann, der Akt
> also **strukturell unmessbar** ist. Ein Fenster, das das Falsche misst, sauber
> einzuhalten wäre Formtreue ohne Sinn.
> **Gewählter Weg: Option 1** (N1 wird vor Fensterstart gebaut und verifiziert). Hält der
> Bau die Verifikation heute nicht, gilt **Option 3** — Fenster und Review verschieben
> sich um die Bautage; Option 2 (Nachrüsten im laufenden Fenster) ist ausgeschlossen,
> sie ist genau die bewegliche Latte, gegen die §0 geschrieben ist.
> **Sprachregelung dieser Lane** (Nachtrag §6, entschieden): Arbeitsdokumente im Repo
> bleiben deutsch wie ihre Geschwister; alles, was öffentliche Kopie werden kann —
> README, `darkocean/METHOD.md`, Bühnentexte — ist englisch. Der Nachtrag und das
> Methodenblatt stehen damit korrekt.

## 1. Das Fenster

```
Nacht 1   2026-08-09/10 (Lauf 04:50 UTC am 10.08., Lesung für den 09.08.)
Nacht 14  2026-08-22/23
Review    2026-08-24            (bewusst nach Foreknowns E1-Review ~22.08. — eine Abnahme zugleich)
```

Die beiden bereits gelaufenen Nächte (Lesungen 2026-08-07 und 2026-08-08) **zählen
nicht als E-Evidenz.** Sie entstanden vor diesen Kriterien; sie dienen als
Vor-Fenster-Kontext und als erste Baseline-Anhaltspunkte. Das ist dieselbe Disziplin,
die die Maschine sich in Nacht 1 selbst auferlegt hat, als sie
`sensor-fts-country-coverage` nicht feuern ließ, bevor ihre eigene Baseline stand.

## 2. Drei mögliche Ausgänge, nicht zwei

Der Review entscheidet zwischen:

- **RUNNING · Flagship** — Bühnen-Präsenz, Site-Erzählung, Werk-Eintrag, Methodenblatt.
- **RUNNING · Instrument** — läuft nächtlich weiter, liefert der Praxis zu, **keine
  Bühne**. Kein Trostpreis: state-before-interface ist genau das und darf jahrelang
  „nichts" produzieren.
- **RETIRED** — ehrlich beendet, Records bleiben, Grund committet.

Der Ausgang „Instrument" existiert, weil die Alternative sonst lautet: Bühne erzwingen
oder Projekt töten. Beides wäre gelogen, wenn die Messung trägt und die Form nicht.

## 3. Abnahmekriterien

### A — Betrieb (harte Zahlen, aus den Records nachrechenbar)

| # | Kriterium |
|---|---|
| A1 | **≥ 12 von 14 Nächten** mit vollständig committeter Lesung (beide Achsen, `failures` explizit) |
| A2 | Jede fehlende Nacht hat eine **benannte Ursache** in `autonomy/log.jsonl` — keine stillen Lücken |
| A3 | `verify.py` **grün auf jeder committeten Nacht**, aus den konservierten Bytes nachgerechnet (CI-Gate, keine Nachsicht) |
| A4 | **0 € Kosten**, keyless-Pfad hält. Wird eine Eskalation aktiv (Copernicus/GFW), wird das Fenster **annotiert, nicht entwertet** — aber der Vorher/Nachher-Schnitt steht im Record |

### B — Die Messung trägt

| # | Kriterium |
|---|---|
| B1 | **Deklarations-Hülle committet:** die Bins, in denen der Behörden-Feed im Fenster je ≥ 1 Schiff meldete. Die Kennzahl wird **innerhalb** dieser Hülle berichtet; außerhalb wird getrennt berichtet und **nie „Stille" genannt** (Begründung: §5.2) |
| B2 | **Baseline committet:** Median und Streuung über das Fenster für Aufnahmen, beobachtete Bins, deklarierte Schiffe und die Diskrepanzrate innerhalb der Hülle |
| B3 | **Sample-Stunde diszipliniert:** `declared_sample_at` in ≥ 12 Nächten innerhalb ±90 min der Fahrplanzeit; jede Abweichung steht im Record und fließt nicht in B2 ein (Begründung: §5.1) |
| B4 | **Mindestens ein Ausreißer** außerhalb der Streuung ist entweder aus committeten Records erklärt (Satellitengeometrie, Sample-Stunde, Feed-Ausfall) **oder als offene Frage committet.** Unerklärt bleiben darf er; unerwähnt nicht |

### C — Werkfähigkeit (die One-Tap-Latte)

| # | Kriterium |
|---|---|
| C1 | Aus den Records des Fensters lässt sich **ein Bühnen-Moment** bauen, der die Zehn-Sekunden-Regel der Bühne erfüllt: ein einfacher Satz, ein echtes Phänomen, eine Handlung |
| C2 | Die Figur dieses Moments ist **aus den Records abgeleitet, nicht komponiert** — sie zeigt einen Systemzustand, keine Illustration |
| C3 | **Gebaut, nicht behauptet:** dem Review liegt ein echter Entwurf bei (statische Seite oder Figur). Genau hier ist One Tap gestorben — an der Inszenierung, nicht an der Evidenz. Ein Versprechen auf eine spätere Form zählt nicht |
| C4 | **Negativ formuliert, damit es beißt:** Wenn der einzige wahre Satz nach 14 Nächten lautet „zwei Register überlappen sich zu etwa X %", ist das eine **Instrumentenanzeige, kein Bühnen-Moment** → Ausgang Instrument |

### D — Ehrlichkeit

| # | Kriterium |
|---|---|
| D1 | **≥ 1 publiziertes Negativ:** ein durchgetragener Quellenausfall, eine von der Maschine selbst korrigierte Zuordnung, oder ein beziffertes Eingeständnis zur eigenen Messgrenze |
| D2 | **Die Artefakt-Schranke ist Pflicht** (Begründung: §5.3). Eine von drei Formen: (a) DMA kehrt zurück → Momenten-Achse; (b) die Maschine begrenzt das Artefakt anders (z. B. zweite Stichprobe innerhalb derselben Nacht); (c) sie schreibt in jede Lesung, dass ihre Stille-Zahl an dieser Stelle **unbegrenzt** ist. Was nicht zulässig ist: eine unqualifizierte Stille-Zahl |

### E — Charter und Ethik (Ausschlusskriterien, keine Punkte)

| # | Kriterium |
|---|---|
| E1 | **Null MMSI, null Schiffsnamen** in abgeleiteten Records über 14 Nächte. Ein einziger Fall ist **Abbruch**, kein Befund — der Prüfer erzwingt es bereits, hier steht es als Bedingung |
| E2 | Kein „illegal", kein „dark ship", keine Schuldzuweisung in committeten Records oder im Entwurf. Publiziert werden Diskontinuitäten zwischen Sichtbarkeitsregimen |
| E3 | Lizenz-Rückgrat hält: kein NC-Material (GFW) in CC0-Ausgaben |

**Bestanden = A vollständig · B vollständig · D vollständig · E ohne Verstoß.**
**C entscheidet dann nur noch zwischen Flagship und Instrument** — nicht über Leben und
Tod des Projekts.

## 4. Was dieses E-Experiment nicht entscheidet

Den V1-Detektionspfad · die Earth-Engine-Frage (konditionales GO liegt, gehört in eigene
Sessions) · eine Regionsänderung · Bühnen-Präsenz vor dem Review · die Momenten-Achse als
Feature (sie ist hier Schranke, nicht Ziel).

## 5. Bekannte Konfundierer — vor Fensterstart benannt

### 5.1 Die Sample-Stunde ist gewandert

Lesung 2026-08-07 wurde um **23:57 UTC** gezogen, Lesung 2026-08-08 um **05:36 UTC** —
sechs Stunden Unterschied, weil die erste Nacht ein Handlauf war und danach der Fahrplan
(04:50 UTC) griff. Ostsee-Verkehr ist tageszeitabhängig; ohne feste Stunde mischt jeder
Nacht-über-Nacht-Vergleich Signal mit Tagesgang. Daher B3.

### 5.2 Die deklarierte Achse sieht nicht, was das Radar sieht

Die Radar-Box ist die ganze Ostsee (9–30 E, 53,5–66 N, 1050 Bins). Die deklarierte Achse
ist **eine Behörde mit Empfängerreichweite vor finnischer Küste** — in beiden
Vor-Fenster-Nächten meldete sie in 154 bzw. 160 Bins. Die Kopfzahl
„observed_silent_in_sample" (459 bzw. 557 Bins) misst deshalb heute überwiegend
**Empfänger-Geografie, nicht Auskunftsverhalten.** Die Lesung sagt das bereits ehrlich in
ihren Notizen; für die Abnahme reicht Ehrlichkeit im Kleingedruckten nicht — die Kennzahl
selbst muss innerhalb der Hülle stehen. Daher B1.

### 5.3 Ohne Momenten-Achse ist „Stille" ein Augenblick

Die deklarierte Achse ist eine **Momentaufnahme**; ein Schiff zehn Minuten vorher oder
nachher erscheint als Stille. Das ist die V0-Form von False Darkness — nicht die Maschine
findet versteckte Schiffe, sondern ihre eigene Abtastung erzeugt Löcher. Solange die
DMA-Tagesdumps ausfallen (drei Proben am 08.08., weiter `outage: URLError`), ist die
Schranke unbekannt. Daher D2.

### 5.4 Bins sind keine Wasserflächen

Halbgrad-Bins über einer Bounding-Box enthalten Land. Steht in den Notizen, bleibt
stehen: eine Seemaske wäre eine Interpretation, die V0 sich nicht anmaßt — aber die
Kopfzahlen dürfen sich nicht auf sie stützen, ohne es zu sagen.

## 6. Wie der Review rechnet

A und B werden **aus den committeten Lesungen nachgerechnet** — ohne frischen Abruf; wenn
eine Zahl das nicht hergibt, ist sie keine Abnahmezahl. E ist Prüfer-Ausgabe. C und D
sind menschlich lesbare Urteile mit beigelegtem Entwurf; sie werden als Text committet,
nicht als Score. Kein Aggregatwert, hier so wenig wie im Autonomie-Protokoll.

## 7. Franks Entscheidungen (2026-08-09, vor Fensterstart — damit gebunden)

1. **Die C-Latte bleibt hart:** ein *gebauter* Entwurf ist Pflicht (C3), keine
   Formskizze. Die teuerste Variante, und die einzige, die die One-Tap-Lehre ernst
   nimmt.
2. **Der Drei-Wege-Ausgang gilt** (§2) — Flagship · Instrument · RETIRED. Damit
   entscheidet C über die Form, nicht über die Existenz; das ist eine datierte
   Erweiterung des Aufnahme-Pfads, der nur RUNNING/RETIRED kannte, und gilt ab jetzt
   auch für künftige Kandidaten.
3. **Die zwei Vor-Fenster-Nächte zählen nicht mit** (§1) — mein Vorschlag, nicht
   widersprochen; steht damit.

Ab der ersten Nacht des Fensters ist dieses Dokument geschlossen. Was danach noch
auffällt, wird Befund des Reviews, nicht Änderung der Kriterien.
