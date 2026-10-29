# Die Website-Sperre der Prüffenster ist aufgehoben (2026-10-29)

**Entscheidung des Maintainers, 2026-10-29 (Wortlaut privat).** Anlass: Die Einstiegsseite
frankbueltge.de/machine-attention zeigte seit dem Ende von The Foreknown (2026-10-04) nur noch
Projektnamen, obwohl die Praxis jede Nacht misst. Ein Text-Logbuch der Nächte wurde als Ersatz
verworfen; gewollt sind Figuren der Experimente, wie überall sonst auf der Site.

## Was gilt ab heute

- **The Interval** und **Planetary Listening** dürfen während ihrer Fenster auf der Website
  erscheinen: Figuren, Zahlen und Daten aus den committeten Records.
- Die Kriterien selbst werden **nicht** umgeschrieben (`interval/experiment.json`,
  `planetary/experiment.json` und ihre Dokumente bleiben mit ihren Hashes stehen). Bei der Prüfung
  (Planetary ab 2026-11-04, Interval ab 2026-11-16) gilt **Kriterium C als verfehlt**, mit Verweis
  auf dieses Dokument. Der Rest der Kriterien wird wie vorgesehen gezählt; ob ein Projekt trotz C
  aufgenommen wird, ist die Entscheidung der Prüfung.
- Die Zeilen der Figuren liefert `views.json` (`practice/src/practice/views.py`, Vertrag
  `attention-views/1`), berechnet mit dem eigenen Code der Projekte aus committeten Bytes und vom
  Sentinel neben `export.json` gebaut. Die Site spiegelt die Datei und zeichnet daraus.
