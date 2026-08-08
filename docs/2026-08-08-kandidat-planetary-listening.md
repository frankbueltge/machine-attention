# Kandidat: Planetary Listening

**Status:** Exposé zur Mitnahme in eine eigene Session · 2026-08-08
**Kontext:** Zweitplatzierter Kandidat für Project 001 der machine investigative practice
(gewählt wurde The Foreknown). Atlas-Lücke: Familie „Erkenntnis/Sinne" — kein Werk im
Atlas (494 Einträge) betreibt kontinuierliches maschinelles Zuhören als Untersuchung.

## Einzeiler

Die Maschine hört ununterbrochen die offenen seismischen und Infraschall-Netze der Erde —
und trennt die menschliche Signatur (Sprengungen, Bergbau, Bombardement, Verkehr) vom
Eigenrauschen des Planeten.

## Forschungsfrage

Was hört ein Apparat, der nie schläft, in einem globalen Sensornetz, dem niemand als
Ganzem zuhört — und lässt sich die menschliche Gewalt- und Extraktionssignatur aus dem
planetaren Signal maschinell isolieren, beweisbar und in Echtzeit?

## Maschinen-Überlegenheit

- Tausende Stationen weltweit streamen 24/7; kein Mensch hört auch nur einer zu.
- Ereignisklassifikation (Beben vs. Sprengung) ist etablierte Seismologie — als
  *kontinuierliche öffentliche Praxis* existiert sie nicht.
- Historische Tiefe: Wellenformarchive reichen Jahrzehnte zurück (GEOFON seit 1993) —
  Muster wie „Steinbruch sprengt regelmäßig außerhalb der genehmigten Zeiten" oder
  „Bombardement-Rhythmus einer Region" sind reine machine attention.

## Datenlage (Kurzcheck 2026-08-08, vor Bau volles Go/No-Go-Protokoll)

| Quelle | Status | Notiz |
|---|---|---|
| GEOFON FDSN (GFZ Potsdam) | ✅ live geprüft, HTTP 200, ohne Key | Netz GE: 147 Stationen seit 1993; FDSN-Standard-APIs (station/dataselect) |
| IRIS/EarthScope FDSN | ⚠️ HTTP 307 (Umzug zu EarthScope) | Neue Basis-URL verifizieren; Datenbestand der größte weltweit |
| Weitere FDSN-Knoten (ORFEUS/EIDA, RESIF, INGV …) | zu prüfen | Föderiertes Standardprotokoll — ein Adapter, viele Netze |
| Infraschall (CTBTO IMS) | ⚠️ vermutlich nicht offen | CTBTO-Daten sind zugangsbeschränkt; offene Alternativen (Raspberry-Shake-Netz?) prüfen |
| Ereigniskataloge (EMSC/USGS) | zu prüfen, vermutlich offen | Für Verifikation der eigenen Detektionen |

## Form / Dramaturgie (Bühne-A-kompatibel)

Das klanglichste und sinnlichste der drei Konzepte — festival-nativ:

- **ATTRACT:** Ein Raum, der den Planeten hörbar macht — nicht als Dekor-Sonifikation,
  sondern als laufende, beschriftete Detektion: „03:41:07 UTC — impulsive event,
  quarry-blast signature, Lausitz". Stille ist echt; ein Ausschlag ist echt.
- **ENTER:** Eine Detektion öffnen: Wellenform, Klassifikation, Konfidenz, Station.
- **INVESTIGATE:** Muster über Zeit — der Sprengrhythmus einer Region, das Verstummen
  eines Bergwerks, die Signatur eines Krieges.
- **VERIFY:** Rohwellenform (Originalbytes, gehasht), Klassifikationscode, re-runnable.
- Ästhetik aus der Epistemologie: latency, repetition, signal/noise, Stille als Zustand.

## Alleinstellung & Nachbarschaften (vor Bau prüfen)

- Seismische Sonifikation als Kunst existiert (Einzelwerke, Konzerte) — aber als
  *fertige Stücke*, nicht als laufender investigativer Apparat.
- Wissenschaft detektiert Sprengungen/Bombardements (Studien zu Gaza, Ukraine, Nordkorea)
  — als Paper, nicht als öffentliche kontinuierliche Praxis.
- Zu prüfen: Raspberry-Shake-Community-Visualisierungen, „Global Jukebox"-artige
  Seismo-Streams — vermutlich Dashboards, keine Untersuchung.

## Grenzen / Risiken (ehrlich)

- **Investigativ dünner als die anderen Kandidaten:** Die Detektion ist stark, aber der
  Weg von „Sprengung erkannt" zu „gesellschaftlich relevanter Befund" braucht die
  Kopplung an Register (Genehmigungen, Konzessionen) — zweite Datenschicht nötig.
- Klassifikations-Unsicherheit ist real → als gemessene Unsicherheit ausweisen (Lab-Ethik).
- Datenvolumen: Wellenformen sind groß; Git-als-Archiv trägt nur Detektionen+Ausschnitte,
  nicht Rohstreams (Speicherentscheidung nötig — erste echte Abweichung vom SBTI-Muster).
- Kriegsdetektion berührt laufende Konflikte → Eskalationsregeln (keine operativen
  Echtzeit-Aussagen, die Kriegsparteien nützen könnten; Latenz als Schutzprinzip).

## V0-Skizze (kleinster Slice)

Ein Netz (GEOFON), eine Region (z. B. Lausitzer Tagebaue oder ein Balkan-Steinbrauchfeld),
ein Klassifikator (Beben/Sprengung, publizierte Methode), nächtliche Detektionsliste
committet mit Wellenform-Ausschnitten + Hashes; Bühne zeigt laufende Detektionen + Stille.
E2E-Test: 14 Tage, ≥1 verifizierte Sprengungs-Zeitreihe einer benennbaren Anlage,
Abgleich mit öffentlichen Sprengzeit-Genehmigungen, ehrliche Fehlklassifikations-Quote.

## Offene Fragen für die aufnehmende Session

1. EarthScope-Migration: neue FDSN-Endpunkte + Nutzungsbedingungen.
2. Speichermodell für Wellenformen (Git reicht nicht — Releases? Objektspeicher?).
3. Region der ersten Untersuchung (Kriterium: offene Genehmigungsdaten als Gegenregister).
4. Klassifikator: symbolisch/klassisch (auditierbar, Lab-präferiert) vs. ML — oder beides
   als Gegenmessung.
