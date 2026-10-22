# The Synthetic Flood — V0, Inkrement 3b: wordlist-v2 und die Regel der abgeleiteten Liste (2026-10-22)

**Stufe:** V0, Inkrement 3b · **Go:** das bedingte GO vom 2026-10-04 (Wortlaut privat), wie in
`docs/2026-10-19-synthetic-flood-v0-inkrement-1.md`. · **Anlass:** Der Fokus wartet — The
Interval liest erst Montag 2026-10-26 wieder; Planetary Listening brauchte heute eine Reparatur
(`docs/2026-10-22-planetary-listening-reparatur-ausfall.md`), die vorging. Kein Abruf heute.

## Gebaut

- **`syntheticflood/wordlists/wordlist-v2.json`** — Nachfolger von `wordlist-v1` (die
  unverändert bleibt). Einzige Änderung: das Kontrollwort `significantly`, ein PubMed-Stoppwort,
  das in allen fünf Basisjahren und in der Kohorte 2026-09 null zählt
  (`syntheticflood/baseline/wordlist-v1.json`; Inkrement 3, Befund 1), fällt; an seine Stelle
  tritt `reduced`, ein Inhaltswort desselben Registers, kein Stoppwort. `fixed` und `pool` Wort
  für Wort übernommen. Getestet gegen die Basis ist `reduced` noch nicht — das ist die erste
  Lesung dieser Liste.
- **Regel `excess-v1`** in `practice/src/practice/syntheticflood/excess.py`, committet bevor für
  irgendeine Kohorte eine abgeleitete Liste berechnet wird: je Wort (außer `rare`) die
  Kleinste-Quadrate-Gerade der Jahresanteile 2018–2022; Erwartung = Gerade an der Lage der
  Kohorte (Jahr = seine Mitte, Monat MM bei YYYY + (MM − 0,5)/12 − 0,5); Verhältnis =
  beobachtet / erwartet. In die Liste eines Monats kommt ein Pool-Wort mit Verhältnis ≥ 2,0 und
  ≥ 50 Abstracts, höchstens 20, höchstes Verhältnis zuerst. Die Kontrollen laufen durch dieselbe
  Rechnung; verlässt eine das Band [1/1,5; 1,5], ist der Monat `control_breach` und seine Liste
  wird berichtet, nicht benutzt. Eine Gerade, die nicht über null bleibt, wird nicht
  extrapoliert (`no_trend`). Tests: `practice/tests/test_syntheticflood_excess.py` (6 Tests,
  ohne Netz), darunter der Fall, für den die Regel da ist: ein Wort, das 2018→2022 schon stieg,
  zählt auf seiner eigenen Geraden keinen Überschuss, wo eine Niveau-Basis ihn als Spur gezählt
  hätte.

## Eine Ehrlichkeitsnotiz

Eine Kohorte nach 2022 ist bereits gelesen: `syntheticflood/readings/2026-09/2026-10-19.json`
(Inkrement 1). Ihre Pool-Zahlen wurden für diese Regel nicht angesehen; die Parameter stammen aus
dem Nachbarn (arXiv:2406.07016, Überschuss gegen eine aus der Basis extrapolierte Linie) und aus
den Schwellen von `baseline-v1` (50 Abstracts, Faktor 1,5). Die Regel ist eine Regel-ID; ändert
sie sich, ist das `excess-v2`, nie eine Änderung dieser.

## Nächste Inkremente

3c. Die fünf Basisjahre und eine Monatskohorte auf `wordlist-v2` lesen (rund 1 000 Anfragen,
    429 als Normalfall), `syntheticflood/baseline/wordlist-v2.json` ableiten, dann die erste
    abgeleitete Liste als Datei, die `verify.py` aus den Lesungen nachrechnet.
4. Erst danach ein monatlicher Workflow.

## Bewusst nicht

Kein Abruf; keine abgeleitete Liste berechnet; `wordlist-v1` und ihre Basis unberührt; keine
Aussage über einen Anteil maschinell geschriebener Sprache; Register B nicht berührt; kein
Workflow; kein Abstract, kein Titel, kein Name.
