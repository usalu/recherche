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

- 809 sichtbare Knoten
- 452 belegte Kanten
- davon Bestand: 618 Knoten / 262 Kanten
- davon Erweiterung: 191 Knoten / 190 Kanten
  - 121 neue Akteure
  - 70 neue Projekte
- entfernt: AT:K004 und NL:K019
- alle übrigen acht kritischen Bestandskanten präzisiert und behalten
- jede sichtbare Kante besitzt ein freigegebenes Beziehungsprofil

## Erweiterung um 71 Projekte

- falsche Norsk-Folkemuseum-Kante entfernen
- Norsk Folkemuseum mit TradLab TRE verbinden
- Brukspecialisten–Borås nicht aufnehmen: Lieferrolle nicht eindeutig belegt
- CONIX behalten und Rotor-Quelle verwenden
- Liljewall-Kante an der Peab-Etappe Ekebäckshöjd entfernen
- `La Caserne de Reuilly` als Projektname verwenden
- unbelegte BTU-Kante Hohenmölsen entfernen
- unbelegte Cleveland-Kante entfernen
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
wurde auf Wunsch nicht ausgeführt. Git und Ticket wurden ebenfalls nicht
verwendet.
