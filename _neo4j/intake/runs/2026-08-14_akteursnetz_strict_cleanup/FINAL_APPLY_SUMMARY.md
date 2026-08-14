# Finaler Neo4j-Anwendungsbericht: Akteursnetz Research-only Cleanup

Stand: 2026-08-14  
Datenbank: `mit-bestand`  
Ergebnis: **erfolgreich angewendet und unabhängig validiert**

## Ergebnis

| Kennzahl | Vorher | Nachher |
|---|---:|---:|
| gesamte Knoten | 2.670 | 2.910 |
| gesamte Beziehungen | 14.948 | 15.004 |
| strenge Akteure | — | 541 |
| strenge Projekte | — | 78 |
| strenge Programme | — | 9 |
| strenge Knoten gesamt | — | 628 |
| strenge Beziehungen gesamt | — | 278 |
| Semio-Knoten ohne Programme | — | 619 |
| Semio-Kanten ohne Programmkanten | — | 268 |

Der Live-Validator meldet `errors: []` und `success: true`.

## Durchgeführte Änderungen

- 160 bereits vorhandene Quellknoten wurden gemäß Review entfernt oder
  zusammengeführt; darin enthalten sind zwei live vorhandene Merge-Quellen.
- 307 geprüfte Overlay-Entitäten wurden neu angelegt.
- FCRBE und Preuse wurden mit ihren vorhandenen Programm-EIDs abgeglichen,
  statt doppelt angelegt zu werden.
- 69 freigegebene Prune-Einträge existierten nie im Live-Graphen und mussten
  daher nicht gelöscht werden.
- Namen, Entitätstypen, Länder, Rollen, Relevanz und Evidenz wurden auf die
  freigegebenen `eid`-basierten Review-Daten normalisiert.
- Die Beziehungen im strengen Scope wurden vollständig ersetzt und auf exakt
  278 freigegebene, belegte Beziehungen gesetzt.
- Keine Sidecar-Quellenknoten wurden angelegt. Evidenz liegt ausschließlich
  auf Knoten- und Beziehungsproperties.

## Typ- und Kategorieabgleich

- Ferry-Dusika-Stadion Rückbau ist ein Projekt.
- AD VITAM MATERIAL und Toulouse Métropole sind Akteure, keine Projekte.
- Preuse ist ein Programm, kein Akteur.
- Der Renderer wurde auf dieselben Typen gebracht; fünf dadurch sichtbar
  gewordene, nicht freigegebene Rohkanten werden explizit ausgeschlossen.

## Sicherungen und Wiederherstellung

Vollständige Sicherung des Ausgangsstands:

`E:/recherche/_neo4j/intake/runs/2026-08-14_akteursnetz_strict_cleanup/backup_pre_apply`

Bestätigungsphrase:

`RESTORE mit-bestand FROM backup_pre_apply`

Zusätzliche Sicherung unmittelbar vor der abschließenden Typreparatur:

`E:/recherche/_neo4j/intake/runs/2026-08-14_akteursnetz_strict_cleanup/backup_post_apply_pre_repair`

Der erste Schreibversuch scheiterte vor dem Commit an einer kollidierenden
Beziehungs-ID und wurde vollständig zurückgerollt. Die spätere Typreparatur
wurde erst nach der zweiten vollständigen Sicherung ausgeführt.

## Verifikation

Erfolgreich geprüft wurden:

- Verbindung mit `mit-bestand`: 2.910 Knoten / 15.004 Beziehungen
- 859/859 Review-Entscheidungen, Cross-Review vollständig
- exakt 628 strenge Knoten: 541 Akteure, 78 Projekte, 9 Programme
- exakt 278 strenge Beziehungen
- exakt 619 Semio-Knoten und 268 Semio-Kanten
- keine fehlenden oder zusätzlichen EIDs
- keine geprunten Live-EIDs und keine Merge-Quellen
- exakte Namen, Typen, Länder, Rollen und Relevanz
- vollständige Rollen- und Kantenbelege
- exakte Figuren-/Tabellen-Kantenparität

Maschinenlesbarer Nachweis: `live_validation.json`  
Reproduzierbarer Validator: `validate_live_cleanup.py`  
Idempotentes Anwendungsskript: `apply_strict_akteursnetz_cleanup.py`

## Nächster Schritt

Die Datenbankarbeit ist abgeschlossen. Als separater Schritt werden die drei
finalen LaTeX-Fragmente in Semio übernommen, der Bericht einmal gebaut und
alle Länder- und Programmblöcke visuell geprüft. Dafür gilt der Handoff:

`../../../review/2026-08_akteursnetz_faktencheck/HANDOFF_STRICT_SEMIO_FINAL.md`
