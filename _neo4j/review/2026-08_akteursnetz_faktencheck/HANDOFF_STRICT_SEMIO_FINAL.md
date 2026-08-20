# Finaler Handoff: lokales LaTeX-Akteursnetz

## Verbindlicher Endstand 20.08.2026

Dieser Abschnitt ersetzt **alle später im Dokument genannten Zahlen,
Laufzeitklassen und Arbeitsaufträge**. Die folgenden älteren Abschnitte bleiben
nur als Verlauf erhalten.

- Lokales LaTeX-Netz: **809 sichtbare Knoten / 452 sichtbare Kanten / 11 Länder**.
- Bereinigte Basis: **618 Knoten / 262 Kanten**.
- Geprüfte Erweiterung: **191 Knoten / 190 Kanten**.
  Davon **121 Akteure und 70 Projekte**.
- Entfernt: **AT:K004** und **NL:K019**, weil die konkrete Beziehung nicht
  belegt ist. Die vier Endknoten bleiben sichtbar.
- Aus der Erweiterung wurden vier falsche oder unbelegte Kanten entfernt;
  Brukspecialisten–Borås wurde wegen unklarer Lieferrolle nicht ergänzt.
- Norsk Folkemuseum wurde mit **TradLab TRE** statt mit dem Spenderprojekt
  Nedre Sem verbunden.
- Jede verbleibende Kante besitzt Belegzitat, URL, Beschreibung und ein
  freigegebenes `Beziehungsprofil`.
- Hauptklassen: **Projektübergreifend** und **Vorhabenspezifisch**.
- Verteilung: 39 institutionell, 7 strategisch, 5 operativ, 389 Vorhaben,
  8 Leistungen, 4 Ereignisse.
- Die Tabellenspalte heißt `Beziehungsprofil`; `Beziehungsdauer` entfällt.
- Neo4j wurde nicht beschrieben.
- `E:/semio` wurde nicht verändert oder synchronisiert.
- Git und Ticket wurden auf Nutzerwunsch nicht verwendet.
- Angewendete Erweiterung:
  `beziehungsprofil_review/erweiterung_final/akteursnetz_erweiterung_final.json`.
- Abschlussbericht: `E:/recherche/AKTEURSNETZ_ERWEITERUNG_ABSCHLUSS.md`.
- Fertiges Tabellenfragment:
  `E:/recherche/_neo4j/netz/figs/frag_tables_grid.tex`.
- Fertiges Graphfragment:
  `E:/recherche/_neo4j/netz/figs/frag_abb_netz.tex`.
- Visuell geprüfte Forschungsbericht-QA:
  `E:/recherche/output/pdf/akteursnetz_beziehungsprofil_qa.pdf`.

Beziehungs- und Erweiterungstests bestehen. Der vollständige Testlauf hat nur
den unabhängigen, bereits vorhandenen Logo-Sicherheitsabstandstest als offenen
Fehler. Die 31-seitige QA-PDF wurde vollständig visuell geprüft.

Für eine spätere Veröffentlichung nach `E:/semio` ist ein eigener Auftrag
erforderlich. Diese Übergabe führt weder Synchronisierung noch Ticketarbeit
vorweg.

---

## Historischer Verlauf – nicht als aktueller Auftrag verwenden

Stand: 2026-08-14  
Status: fachlich abgeschlossen, in `mit-bestand` angewendet und validiert

## Verbindlicher Endstand

- Vollständig entschiedene EIDs: **859 von 859**
- `keep`: **628**
- `prune`: **227**
- `merge`: **4**
- strenger Neo4j-Bestand: **628 Knoten**
  - **541 Akteure**
  - **78 realisierte Referenzprojekte**
  - **9 Programme**
- Semio-Akteurs-/Projektansicht: **619 Knoten und 268 belegte Kanten**
- vollständiger strenger Neo4j-Scope: **628 Knoten und 278 belegte Beziehungen**
- unplatzierte EIDs: **0**
- Validator-, Typ-, Join- und Kantenfehler: **0**

Neo4j ist jetzt auf denselben freigegebenen Research-only-Stand gebracht. Alle
technischen Joins laufen über stabile `eid`-Werte. Alte `LAND:tid`-Werte sind
nur Prüfbezeichnungen.

## Programme: nicht als Akteure rendern

Diese neun Einträge gehören ausschließlich in den separaten Programmblock:

1. `BE:F01` — BAMB (Buildings as Material Banks)
2. `BE:S02` — Preuse
3. `CH:F10` — Urban Bricolage
4. `DE:F02` — Circular Material Systems
5. `DE:F10` — ReCreate project consortium
6. `DE:P4` — CIRCOFIN (Circular Construction Finance)
7. `FI:F03` — ReCreate Finnish cluster
8. `FR:F02` — FCRBE (Facilitating the Circulation of Reclaimed Building Elements)
9. `FR:O03` — Métabolisme Urbain

Programme erhöhen weder die Akteurs- noch die Projektzahlen. Die zehn
freigegebenen Beziehungen mit Programmbeteiligung bleiben im vollständigen
Neo4j-Scope erhalten, werden aber nicht als Akteurskanten gerendert.

## Kanonische Artefakte

| Zweck | Datei |
|---|---|
| Akteure und Projekte | `klassifikation_actor_project_final.json` |
| Programme | `programme_strict_final.json` |
| Entfernungen | `prune_strict_final.json` |
| Dubletten-Weiterleitungen | `merge_redirects_strict.json` |
| Namen-, Typ- und Länderkorrekturen | `report_overrides_strict.json` |
| Entscheidungsprovenienz | `prune_strict_provenance.json` |
| Kantenklassifikation | `kanten_klassifikation.json` |
| verworfene Kanten | `prune_kanten_final.json` |
| Netzabschluss | `strict_cleanup_network_audit.json` |
| lesbarer Netzabschluss | `STRICT_CLEANUP_NETWORK_AUDIT.md` |
| Neo4j-Anwendungsbericht | `../../intake/runs/2026-08-14_akteursnetz_strict_cleanup/FINAL_APPLY_SUMMARY.md` |
| Live-Validierung | `../../intake/runs/2026-08-14_akteursnetz_strict_cleanup/live_validation.json` |

Die ursprünglichen Resultatstabellen, `prune_faktencheck_final.json` und die
eingefrorenen Ausgangsdateien bleiben unverändert.

## Neo4j-Anwendung

Zieldatenbank: `mit-bestand`

- vor dem Lauf: **2.670 Knoten / 14.948 Beziehungen**
- nach dem Lauf: **2.910 Knoten / 15.004 Beziehungen**
- 160 vorhandene, freigegeben entfernte Quellknoten gelöscht oder gemergt
- 307 research-geprüfte Overlay-Entitäten neu angelegt
- FCRBE und Preuse mit ihren bereits vorhandenen Programm-EIDs abgeglichen
- Rollen, Länder, Namen, Typen, Relevanz und Evidenz normalisiert
- der strenge Scope auf exakt **278** freigegebene Beziehungen gesetzt

Vollständige Sicherung vor der Anwendung:

`E:/recherche/_neo4j/intake/runs/2026-08-14_akteursnetz_strict_cleanup/backup_pre_apply`

Wiederherstellungsphrase:

`RESTORE mit-bestand FROM backup_pre_apply`

Zusätzliche Sicherung vor der abschließenden Typreparatur:

`E:/recherche/_neo4j/intake/runs/2026-08-14_akteursnetz_strict_cleanup/backup_post_apply_pre_repair`

## Historischer Fragmentstand vom 14.08.2026 – ersetzt

- `E:/recherche/_neo4j/netz/figs/frag_abb_netz.tex`
- `E:/recherche/_neo4j/netz/figs/frag_tables_grid.tex`
- `E:/recherche/_neo4j/netz/figs/frag_programme.tex`

Diese Dateien enthielten damals 540 Akteure, 78 Projekte und 264 Kanten. Diese
Zahlen und die damalige Spalte `Beziehungsdauer` sind ersetzt. Maßgeblich ist
nur der Endstand am Anfang dieses Dokuments.

## Historischer Semio-Auftrag – nicht ausführen

Die folgende Liste dokumentiert den damaligen Ablauf. Sie ist kein aktueller
Auftrag und enthält ersetzte Zahlen.

1. Zuerst `E:/semio/AGENTS.md` lesen.
2. Das vorgeschriebene Semio-Ticket öffnen oder wiedereröffnen; ohne Ticket
   keine Semio-Datei ändern.
3. Bestehende Nutzeränderungen in `semio-graph.sty` und `semio-tree.sty`
   erhalten.
4. Die drei finalen Fragmente in die bestehenden Berichtziele übernehmen:
   - `frag_abb_netz.tex` → `anhang/akteursnetz-figuren.tex`
   - `frag_tables_grid.tex` → `anhang/akteursnetz-tabellen.tex`
   - `frag_programme.tex` → `anhang/akteursnetz-programme.tex`
5. Berichtszahlen auf **618 Knoten, 264 Kanten, 9 Programme** setzen.
6. Den Forschungsbericht über die vorgesehene Launch-/Nx-Struktur bauen
   (`📦build🏚️mitbestand📕forschungsbericht` bzw. dessen Nx-Ziel).
7. Alle elf Länderblöcke, den Programmblock, Tabellenumbrüche, Quellenlisten
   und beide Style-Dateien visuell prüfen.
8. Das Ticket mit Build- und Sichtprüfungsnachweis schließen.

## Historische Abnahmebedingungen

- Resource Rows und Circl erscheinen jeweils nur einmal.
- Keine dänischen Einträge stehen im deutschen Länderblock.
- Kein Programm erscheint als Akteur oder Projekt.
- Kein geprunter oder zusammengeführter Quell-EID wird gerendert.
- Keine Fallback-Rolle und kein Fallback-Standardsatz wird ausgegeben.
- Jede sichtbare Rolle, jedes Projekt und jede Kante besitzt konkrete
  Reuse-Evidenz.
- Semio zeigte exakt dieselben freigegebenen Typen, Laufzeiten und Kanten wie
  die geprüfte LaTeX-Klassifikation.

## Historische reproduzierbare Prüfung

```text
cd E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck
python strict_review/validate_strict_review.py
python strict_review/audit_final_network.py

cd E:/recherche/_neo4j/intake/runs/2026-08-14_akteursnetz_strict_cleanup
python validate_live_cleanup.py
```

Erwartet:

```text
records=859 errors=0 cross_review_complete=True
nodes=619 edges=268 errors=0
strict nodes=628 actors=541 projects=78 programmes=9 relationships=278 errors=0
```

## Historische Schlussregel

Diese frühere Schlussregel ist durch den Abschnitt `Verbindlicher Endstand
20.08.2026` ersetzt.
