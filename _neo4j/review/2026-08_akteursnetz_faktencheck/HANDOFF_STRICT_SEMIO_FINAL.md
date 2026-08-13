# Finaler Handoff: Strict Research-only Cleanup → Semio

Stand: 2026-08-13  
Status: fachlich abgeschlossen, freigegeben und maschinell validiert

## Verbindlicher Endstand

- Vollständig entschiedene EIDs: **859 von 859**
- `keep`: **628**
- davon Akteure und realisierte Referenzprojekte: **620**
- davon separat geführte Programme: **8**
- `prune`: **227**
- `merge`: **4**
- finale Akteurs-/Projektansicht: **620 Knoten, 268 belegte Kanten**
- unplatzierte EIDs: **0**
- Validator- und Netzfehler: **0**

Neo4j wurde nicht verändert. Alle Korrekturen sind report-spezifisch und über
`eid` nachvollziehbar. Alte `LAND:tid`-Werte sind nur Prüfbezeichnungen und
dürfen nicht als technischer Join-Schlüssel verwendet werden.

## Programme: nicht als Akteure rendern

Diese acht Einträge gehören ausschließlich in einen separaten Programmblock:

1. `BE:F01` — BAMB (Buildings as Material Banks)
2. `CH:F10` — Urban Bricolage
3. `DE:F02` — Circular Material Systems
4. `DE:F10` — ReCreate project consortium
5. `DE:P4` — CIRCOFIN (Circular Construction Finance)
6. `FI:F03` — ReCreate Finnish cluster
7. `FR:F02` — FCRBE (Facilitating the Circulation of Reclaimed Building Elements)
8. `FR:O03` — Métabolisme Urbain

Sie sind bereits aus den Akteursdiagrammen und Akteurstabellen ausgeschlossen.
Die ersten sieben wurden in der letzten Freigabe umtypisiert; `FR:O03` war
bereits als Programm korrigiert.

## Kanonische Eingaben für Semio

| Zweck | Datei |
|---|---|
| Akteure und Projekte | `klassifikation_actor_project_final.json` |
| separater Programmblock | `programme_strict_final.json` |
| report-spezifische Entfernungen | `prune_strict_final.json` |
| Dubletten-Weiterleitungen | `merge_redirects_strict.json` |
| Namen-, Typ- und Länderkorrekturen | `report_overrides_strict.json` |
| vollständige Entscheidungsprovenienz | `prune_strict_provenance.json` |
| maschineller Netzabschluss | `strict_cleanup_network_audit.json` |
| lesbarer Netzabschluss | `STRICT_CLEANUP_NETWORK_AUDIT.md` |

Die ursprünglichen Resultatstabellen, `prune_faktencheck_final.json` und die
eingefrorenen Ausgangsdateien bleiben unverändert.

## Bereits neu erzeugte LaTeX-Fragmente

- `E:/recherche/_neo4j/netz/figs/frag_abb_netz.tex`
- `E:/recherche/_neo4j/netz/figs/frag_tables_grid.tex`

Beide Fragmente enthalten ausschließlich die 620 freigegebenen Akteure und
Projekte. Nicht klassifizierte Legacy-Knoten werden fail-closed ausgeschlossen.

## Auftrag für den nächsten Agenten

1. Zuerst `E:/semio/AGENTS.md` lesen.
2. Über das verpflichtende Repo-MCP `repo://goals` lesen und ein passendes
   Ticket öffnen oder wiedereröffnen. Ohne Repo-Ticket keine Semio-Datei ändern.
3. Bestehende Nutzeränderungen in
   `E:/semio/print/tex/semio-graph.sty` und
   `E:/semio/print/tex/semio-tree.sty` erhalten.
4. Die beiden finalen Fragmente in die bestehenden Semio-Ziele übernehmen:
   - `frag_abb_netz.tex` →
     `E:/semio/mit-bestand/bericht/zwischenbericht/anhang/akteursnetz-figuren.tex`
   - `frag_tables_grid.tex` →
     `E:/semio/mit-bestand/bericht/zwischenbericht/anhang/akteursnetz-tabellen.tex`
5. Aus `programme_strict_final.json` im bestehenden Bericht einen klar getrennten
   Programmblock erzeugen. Programme dürfen weder Akteurszahlen noch
   Länder-Akteursrollen erhöhen.
6. Veraltete Berichtszahlen durch den Endstand ersetzen: **620 Knoten,
   268 Kanten, 8 separate Programme**.
7. Den vorhandenen Zwischenbericht-Build über die im Repository vorgesehene
   Launch-/Nx-Struktur einmal ausführen; keine parallelen Builds starten.
8. Alle elf Länderblöcke, den Programmblock, Tabellenumbrüche, Quellenlisten
   und die beiden geänderten Style-Dateien visuell prüfen.
9. Das Repo-Ticket mit Build- und Sichtprüfungsnachweis schließen.

## Harte Abnahmebedingungen

- Resource Rows und Circl erscheinen jeweils nur einmal.
- Keine dänischen Einträge stehen im deutschen Länderblock.
- Kein Programm erscheint als Akteur oder Projekt.
- Kein geprunter oder zusammengeführter Quell-EID wird gezeichnet.
- Keine Fallback-Rolle und kein Fallback-Standardsatz wird ausgegeben.
- Keine Rolle stammt nur aus Partnerliste, Mitgliedschaft, allgemeiner
  Nachhaltigkeit oder Recycling.
- Jede sichtbare Rolle und jedes sichtbare Projekt besitzt konkrete
  Reuse-Evidenz.
- Neo4j bleibt unverändert.

## Reproduzierbare Research-Prüfung

Aus `E:/recherche/_neo4j/review/2026-08_akteursnetz_faktencheck/strict_review`:

```text
python validate_strict_review.py
python audit_final_network.py
```

Erwartet:

```text
records=859 errors=0 cross_review_complete=True
nodes=620 edges=268 errors=0
```

Die Fragmente werden aus `E:/recherche/_neo4j/netz` reproduziert:

```text
python -m netz.cli abb
python -m netz.cli tables-grid
```

## Schlussregel

Für Semio gelten nur dieser Handoff und die oben genannten `*_strict_*`- bzw.
`*_final`-Artefakte. Frühere Handoffs mit **859 Knoten / 570 Kanten** beschreiben
den Stand vor dem harten Research-only-Cleanup und sind nicht mehr renderfähig.
