# Archivierter Kanten-Handoff

Stand: 2026-08-14  
Status: **durch `HANDOFF_STRICT_SEMIO_FINAL.md` ersetzt**

Dieser Handoff dokumentiert die ursprüngliche Prüfung von 570
Kantenkandidaten. Er ist kein aktueller Arbeitsauftrag mehr.

## Historischer Kantenstand

- 570/570 Kandidaten wurden geprüft.
- 477 Beziehungen wurden zunächst behalten.
- 93 Beziehungen wurden entfernt.
- 88 schon vorher als `unklar` ausgeschlossene Beziehungen gehörten nicht zu
  diesen 570 Kandidaten.
- Jede positive Entscheidung besitzt Beziehungsart, Richtung, Beschreibung,
  URL und Belegzitat.

## Was sich durch den strengen Knoten-Cleanup geändert hat

Der spätere Research-only-Cleanup entfernte schwache Knoten, führte Dubletten
zusammen und korrigierte Entitätstypen. Deshalb ist die alte Positivliste mit
477 Kanten **nicht** mehr die sichtbare Semio-Kantenmenge.

- aktuelle Semio-Akteurs-/Projektansicht: **619 Knoten / 268 Kanten**
- vollständiger strenger Neo4j-Scope: **628 Knoten / 278 Beziehungen**
- Differenz: **10 freigegebene Beziehungen mit Programmbeteiligung**
- `prune_kanten_final.json` enthält jetzt 98 Paare: die historischen 93 plus
  fünf Rohkanten, die erst durch die korrigierte Umtypisierung von AD VITAM
  MATERIAL und Toulouse Métropole sichtbar wurden und keine freigegebene
  Kantenklassifikation besitzen.

Die fünf zusätzlich ausgeschlossenen Paare sind:

1. Rotor — AD VITAM MATERIAL
2. Envirobat Occitanie — Toulouse Métropole
3. Institut National de l’Économie Circulaire — Toulouse Métropole
4. Recyclo’Bat — Toulouse Métropole
5. Synéthic — Toulouse Métropole

## Neo4j-Status

Die frühere Aussage „Neo4j wurde nicht verändert“ ist nicht mehr aktuell.
Der freigegebene Research-only-Stand wurde am 2026-08-14 in `mit-bestand`
angewendet und unabhängig validiert:

- gesamte Datenbank: **2.910 Knoten / 15.004 Beziehungen**
- strenger Scope: **541 Akteure / 78 Projekte / 9 Programme**
- Fehler: **0**

## Aktuelle Autorität

Für jede Folgearbeit gelten ausschließlich:

- `HANDOFF_STRICT_SEMIO_FINAL.md`
- `kanten_klassifikation.json`
- `prune_kanten_final.json`
- `strict_cleanup_network_audit.json`
- `../../intake/runs/2026-08-14_akteursnetz_strict_cleanup/live_validation.json`

`keep_kanten_final.json` bleibt als historisches Zwischenergebnis erhalten,
darf aber nicht mehr als exakte Semio-Kantenmenge verwendet werden. Die
aktuelle Kantenmenge entsteht fail-closed aus der finalen Kantenklassifikation
und den 619 freigegebenen Akteurs-/Projekt-Endpunkten.

## Reproduzierbare aktuelle Prüfung

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
strict nodes=628 relationships=278 errors=0
```
