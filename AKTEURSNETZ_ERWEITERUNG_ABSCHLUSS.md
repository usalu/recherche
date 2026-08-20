# Abschluss: lokales LaTeX-Akteursnetz

Stand: 20.08.2026  
Status: **fachlich abgeschlossen und visuell geprüft**

## Ergebnis

- 809 sichtbare Knoten
- 452 belegte Kanten
- 11 Länder
- 191 neue Knoten
  - 121 Akteure
  - 70 Projekte
- 190 neue Kanten
- isolierte Knoten bleiben sichtbar
- jede sichtbare Kante mit Beschreibung, Quelle und Beziehungsprofil
- alle neuen Beschreibungen höchstens 60 Zeichen

## Beziehungsprofil

- `Projektübergreifend`: mehrere Projekte oder institutionelle Bindung
- `Vorhabenspezifisch`: ein Projekt, ein Auftrag oder ein Ereignis

Gesamtverteilung:

- Projektübergreifend / institutionell: 39
- Projektübergreifend / strategisch: 7
- Projektübergreifend / operativ: 5
- Vorhabenspezifisch / Vorhaben: 389
- Vorhabenspezifisch / Leistung: 8
- Vorhabenspezifisch / Ereignis: 4

## Entfernt oder nicht aufgenommen

Bestand:

- AT:K004 – konkrete DRZ-Aufgabe nicht belegt
- NL:K019 – bilaterale Beziehung nicht belegt

Erweiterung:

- Norsk Folkemuseum – Nedre Sem Låve – falsches Zielprojekt
- Liljewall – Ekebäckshöjd – Quelle betrifft eine andere Etappe
- BTU – Reihenhäuser Hohenmölsen – keine Beteiligung belegt
- Cleveland-Kandidat – exakte Akteursidentität nicht belegt
- Brukspecialisten – Borås – genaue Lieferrolle nicht belegt

## Korrigiert

- Norsk Folkemuseum mit TradLab TRE verbunden
- CONIX-Beziehung mit Rotor-Beleg gesichert
- Projekt in `La Caserne de Reuilly` umbenannt
- zwei BAM-Bezeichnungen zu `BAM Bouw en Techniek` zusammengeführt
- Dura-Vermeer-Varianten getrennt gelassen
- IMd und Van Rossum getrennt gelassen

## Prüfung

- Graph und Tabelle: identische 452 Kanten
- alle 31 PDF-Seiten visuell geprüft
- Beziehungstests: bestanden
- ein unabhängiger, bereits bestehender Logo-Sicherheitsabstandstest bleibt offen

## Dateien

- Daten: `_neo4j/review/2026-08_akteursnetz_faktencheck/beziehungsprofil_review/erweiterung_final/akteursnetz_erweiterung_final.json`
- Knotentabelle: `_neo4j/review/2026-08_akteursnetz_faktencheck/beziehungsprofil_review/erweiterung_final/erweiterung_klassifikation.json`
- Kantentabelle: `_neo4j/review/2026-08_akteursnetz_faktencheck/beziehungsprofil_review/erweiterung_final/erweiterung_kanten.json`
- Audit: `_neo4j/review/2026-08_akteursnetz_faktencheck/beziehungsprofil_review/erweiterung_final/ERWEITERUNG_FINAL_AUDIT.md`
- LaTeX-Tabelle: `_neo4j/netz/figs/frag_tables_grid.tex`
- LaTeX-Graph: `_neo4j/netz/figs/frag_abb_netz.tex`
- PDF: `output/pdf/akteursnetz_beziehungsprofil_qa.pdf`

## Bewusst nicht ausgeführt

- kein Neo4j-Schreibzugriff
- keine Änderung oder Synchronisierung in `E:\semio`
- kein Git
- kein Ticket
