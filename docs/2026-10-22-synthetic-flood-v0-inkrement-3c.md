# The Synthetic Flood — V0, Inkrement 3c: Basis auf wordlist-v2 und die erste abgeleitete Liste (2026-10-22, zweiter Pass)

**Stufe:** V0, Inkrement 3c · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), wie in
`docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`. · **Anlass:** Der Fokus wartet — The Interval
liest erst Montag 2026-10-26 (Tally unverändert); Planetary Listening wartet auf den Lauf des
Tages (Workflow `planetary`, zuletzt gegen 13:30 UTC gestartet; zur Passzeit 12:16 UTC noch nicht
gelaufen, die Bitte um `workflow_dispatch` steht seit dem Morgen in `REQUESTS.md`).
`memoryhole/readings/2026-10-21.json` trägt 0 Enthaltungen — kein Urteil fällig.

## Gebaut

- **Die Lesungen** (`wordlist-v2`, Lesedatum 2026-10-22, 12:16:59–12:40:59 UTC, 1 010 Anfragen,
  8 × 429, jede vom Client wiederholt und dann mit 200 beantwortet, 0 fehlend):
  `syntheticflood/readings/{2018,2019,2020,2021,2022}/2026-10-22.json` und
  `syntheticflood/readings/2026-09/2026-10-22.json` (Kohorte 2026-09 bei M+1, 165 995 Abstracts —
  165 555 am 2026-10-19, die Nachindexierung läuft weiter). Die `wordlist-v1`-Lesungen und ihre
  Basis bleiben unberührt; `verify.py` wählt die neueste Lesung je Jahr **je Liste**.
- **`syntheticflood/baseline/wordlist-v2.json`** — Regel `baseline-v1`, unverändert:
  Kontrollen 20 stabil · fixed 31 stabil / 10 steigend / 6 selten · Pool 81 / 16 / 2. Das neue
  Kontrollwort `reduced` ist in der Basis stabil (Anteil 8,16 % → 7,90 %, Verhältnis 1,034).
- **Die abgeleitete Liste als Datei:** `practice/src/practice/syntheticflood/derived.py` schreibt
  `syntheticflood/derived/<kohorte>/<lesedatum>.json` aus der Kohortenlesung und der Basis
  derselben Liste, beide mit SHA-256 genannt, Regel `excess-v1` (`excess.py`, unverändert und
  weiterhin rein). `verify.py` → `check_syntheticflood_derived` rechnet jede Erwartung, jedes
  Verhältnis, den Kontrollbruch und die Liste unabhängig nach (eigene Kleinste-Quadrate-Rechnung,
  nicht das Paketmodul) und hält die Regelparameter unter ihrer ID fest. Tests:
  `practice/tests/test_syntheticflood_derived.py` (7 Tests, ohne Netz; jede Prüfung mit einem
  Test, der sie bricht).

## Das Ergebnis: Kontrollbruch

`syntheticflood/derived/2026-09/2026-10-22.json` ist **`control_breach: ["reduced"]`** — die
Liste wird nach der Regel berichtet, nicht benutzt. `reduced` zählt in 2026-09 22 877 von
165 995 Abstracts (13,8 %), seine Basisgerade erwartet rund 7,5 %: Verhältnis 1,827, außerhalb
[1/1,5; 1,5]. Die übrigen 19 Kontrollen liegen bei 0,678 (`effect`) bis 1,399 (`associated`),
also im Band, zwei davon nah am Rand.

Was das heißt, ist nicht bewiesen. Möglich sind (a) eine Eigenheit der Kohorte bei M+1 — früh
indexierte Datensätze sind nicht dieselbe Mischung wie die spätere volle Kohorte; (b) eine
Änderung der Suche selbst zwischen 2022 und 2026, die das Wort anders trifft; (c) ein echter
Wandel im Gebrauch. Die Regel unterscheidet das nicht und soll es nicht: Sie hält den Monat an.
Der Test kommt mit der Lesung bei M+2 (November) und M+3 (Dezember, der Wert der Kohorte). Die
Regel wird für dieses Ergebnis nicht geändert; eine andere Kontrolle wäre `wordlist-v3`, eine
andere Schwelle `excess-v2`, beides erst nach einer zweiten Lesung und mit Begründung aus ihr.

Die 20 Wörter, die die Regel ohne den Bruch gelistet hätte (Verhältnis 2,09–5,41), stehen in der
Datei; sie sind keine Aussage. Auffällig unter den `fixed`-Wörtern, die nie in die Liste kommen:
`underscoring` 16,5, `underscores` 10,1, `underscore` 7,5 — gegen ihre eigene Basisgerade, nicht
gegen ein Niveau.

## Nächste Inkremente

4. Monatlicher Workflow erst, wenn ein Monat ohne Kontrollbruch abgeleitet ist — oder der
   Maintainer anders entscheidet. Bis dahin liest der Pass 2026-09 bei M+2 (ab 2026-11-01) von
   Hand und leitet erneut ab; die Lesung 2026-10-22 bleibt stehen.

## Bewusst nicht

Keine Regel und keine Wortliste geändert; keine Kohorte außer 2026-09 nach 2022 gelesen; keine
Aussage über einen Anteil maschinell geschriebener Sprache; Register B nicht berührt (die
Runner-Frage in `REQUESTS.md`, 2026-10-20, bleibt offen); kein Workflow; kein Abstract, kein
Titel, kein Name.
