# Entscheidungen Akteursnetz

Stand: 20.08.2026

## Freigegeben

- Spalte: `Beziehungsprofil`
- Hauptklassen: `Projektübergreifend` und `Vorhabenspezifisch`
- `Beziehungsdauer` entfällt.
- Falsche oder nicht konkret belegte Kanten werden entfernt.
- Jede sichtbare Kante braucht Beschreibung, Belegzitat und mindestens eine URL.
- Isolierte Knoten bleiben sichtbar.

## Aktueller LaTeX-Bestand

- 618 sichtbare Knoten
- 262 belegte Kanten
- entfernt: AT:K004 und NL:K019
- alle übrigen acht kritischen Bestandskanten präzisiert und behalten
- jede sichtbare Kante besitzt ein freigegebenes Beziehungsprofil

## Erweiterung um 71 Projekte

- falsche Norsk-Folkemuseum-Kante entfernen
- Norsk Folkemuseum mit TradLab TRE verbinden
- Brukspecialisten mit Borås nya tingsrätt verbinden
- CONIX behalten und Rotor-Quelle verwenden
- Liljewall-Kante an der Peab-Etappe Ekebäckshöjd entfernen
- `La Caserne de Reuilly` als Projektname verwenden
- unbelegte BTU-Kante Hohenmölsen entfernen
- beide BAM-Namen zu `BAM Bouw en Techniek` zusammenführen
- Dura Vermeer und Dura Vermeer Bouw Zuid getrennt lassen
- IMd und Van Rossum getrennt lassen

## Verbindliche Dateien

- Vollständige Entscheidungsliste:
  `_neo4j/review/2026-08_akteursnetz_faktencheck/beziehungsprofil_review/ENTSCHEIDUNGSLISTE_KOMPAKT.md`
- Erweiterungskorrekturen:
  `_neo4j/review/2026-08_akteursnetz_faktencheck/beziehungsprofil_review/ERWEITERUNG_KORREKTUREN_FREIGEGEBEN.json`
- Ergebnis aktuelle Kanten:
  `_neo4j/review/2026-08_akteursnetz_faktencheck/BEZIEHUNGSPROFIL_FINAL.md`
- Visuelle Kontrolle:
  `output/pdf/akteursnetz_beziehungsprofil_qa.pdf`

Neo4j wurde nicht geändert. Die Synchronisierung in den Forschungsbericht
muss im Semio-Ticket mit dem bestehenden Nx-/Launch-Ablauf erfolgen.
