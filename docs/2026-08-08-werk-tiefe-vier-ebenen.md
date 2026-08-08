# Werk-Tiefe: die vier Ebenen von The Foreknown

**Datum:** 2026-08-08 (spät UTC; lokal bereits 09.08. — das Notariat datiert nach UTC)
**Status:** gebaut · **Roadmap:** Punkt „Werk-Tiefe vor neuen Quellen"
(`2026-08-08-projekt-aufnahme.md` §4) · **Vorgabe:** ATTRACT → ENTER →
INVESTIGATE → VERIFY aus dem Korrektur-Dokument („Public dramaturgy ist Teil
des Kernsystems")

## Der Grundsatz

**Depth on demand — Evidence ist unendlich, Aufmerksamkeit nicht.** Die Bühne
bleibt der Zehn-Sekunden-Raum; wer tiefer will, bekommt je Klick genau eine
Ebene mehr. Alle vier Ebenen sind statische, deterministische Ableitungen aus
denselben committeten Records — dadurch prüft `verify.py` sie automatisch mit
(Byte-Vergleich des kompletten Rebuilds), und die Ausstellungs-Regel „keine
Sackgassen" ist ein **Test** (`test_no_page_has_a_dead_end`), kein Vorsatz.

## Die Ebenen

| Ebene | Datei | Inhalt |
|---|---|---|
| ATTRACT | `index.html` | unverändert die Zehn-Sekunden-Bühne; Featured-Karte und Grid-Karten verlinken jetzt in die Dossiers, das Ledger-Band auf das volle Register |
| ENTER | `future/<id>.html` (je Zukunft, auch geschlossene) | das Leben der Warnung als Spur: NOTARIZED → REVISED (von → nach je Feld) → CLOSED/DISSIPATED → Verdikt, **jedes Ereignis mit Evidenz-Anker** auf den konservierten Snapshot; Kaltstart- und Overdue-Ehrlichkeit in Klartext; die Reaktion mit Plan-**Namen** und den Grenzen im Fließtext; Provenienz-Fuß mit Record-id und Quelle |
| INVESTIGATE | `ledger.html` | die Nächte als Tabelle, das offene Register nach Gefahr gruppiert (inkl. Spalte „2026 plan" = der stehende Sensor der Maschine, Zeile für Zeile), Geschlossene mit Verdikt, und **„What the machine itself has noticed"**: Observations und Sensor-Proposals im Volltext mit Status und Beförderungs-Begründung |
| VERIFY | `verify.html` | „Nothing here asks to be believed": die Kette in Klartext, die drei Kommandos, konservierte Bytes mit SHA-256 (neueste 14 Nächte, Kappung offen deklariert), die referenzierten-nicht-gespeicherten GDELT-Bytes mit Hash-Argument, der Crosswalk als „the one hand-authored link", das Autonomie-Protokoll |

## Entscheidungen

1. **Kein Interaktions-Apparat.** Ledger ohne Filter/Suche — 100 Zeilen sind
   scanbar, und die Nüchternheit der Bühne setzt sich fort. Wird das Register
   vierstellig, ist das eine neue Entwurfsfrage, nicht ein fehlendes Feature.
2. **Volle amtliche Namen als H1.** Die 28-Länder-Dürre ergibt eine
   monumentale Überschrift — gewollt: der notarisierte Name der Warnung in
   voller Länge ist die Bühnen-Sprache („monumental true statements"), nur
   der Browser-`<title>` wird gekürzt.
3. **Statusfarben bleiben tabu.** Orange/Rot erscheinen als Text (die Worte
   der Quelle), Verdikte neutral; die einzige Signalfarbe bleibt das
   Bühnen-Bernstein für Uhren/Marker — Identität, keine Wertung.
4. **Kappung mit Offenlegung.** VERIFY zeigt die neuesten 14 Nächte bzw. 10
   Aufmerksamkeitstage und sagt jeweils dazu, wie viele es insgesamt sind und
   dass das Repo das vollständige Archiv ist — keine stille Trunkierung.
5. **Die Maschine ist auf der INVESTIGATE-Ebene Autorin.** Ihre Proposals
   stehen im Volltext mit Status-Badge (STANDING/IMPLEMENTED/PROPOSED) und
   der jeweiligen Beförderungs- bzw. Nicht-Beförderungs-Begründung — die
   Rollenteilung (Maschine schlägt vor, Beförderung ist ein begründeter
   Commit) wird öffentlich lesbar statt nur im Repo.

## Abnahme gegen die One-Tap-Lehre

„Gute Evidence ergibt nicht automatisch ein gutes digitales Werk." Prüfung:
jede Ebene beginnt mit einem Klartext-Satz (Zehn-Sekunden-Regel gilt auf
jeder Tiefe), jede Zahl bleibt ein echter Systemzustand, jede Grenze steht
neben ihrer Zahl statt in einer Fußnote, und der tiefste Punkt des Werks ist
keine „About"-Seite, sondern die Kette selbst („This page is the bottom of
the work"). Der Weg ATTRACT→VERIFY ist in drei Klicks begehbar und in beide
Richtungen verlinkt.

## Nebenbefund (an den Discovery-Pass, nicht heute)

Die Ledger-Tabelle macht sichtbar, dass zahlreiche Erdbeben-Fenster 2025
enden — GDACS führt Episoden von über einem Jahr Alter als aktiv. Zusammen
mit obs-2026-08-08-2 (Erdbeben-Fenster sind strukturell instantan) Material
für eine künftige Differenz-Beobachtung; ledger.html ist ab jetzt Teil des
Nachtzustands, den der Pass liest.

## Bewusst nicht gebaut

Filter-/Such-UI · Reaktions-Zeitreihen je Dossier (erst wenn mehrere Lesungen
existieren) · QR-Handoff/Kiosk-Modus (Ausstellungs-Paket, eigener Schritt) ·
Attract-Loop über die Tiefen · jede Form von Dashboard.
