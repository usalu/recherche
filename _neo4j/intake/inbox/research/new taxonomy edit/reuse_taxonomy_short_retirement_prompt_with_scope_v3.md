# Short Integration Prompt v3 — Context-Aware Replacement of Old Generic Taxonomy

Generated: 2026-06-03

## Work context

This is **integration work**, not new evidence research and not blind cleanup.

The goal is to replace the old generic reuse-taxonomy layer in the live graph with the new evidence-backed taxonomy from the approved Markdown batches.

The **new Markdown evidence batches are the source of truth**. They contain the current mappings for:

- projects,
- component groups,
- reuse outcomes,
- source,
- reuse location,
- methods,
- Rückbauverfahren,
- Aufbereitungsverfahren.

The old graph is **not** the source of truth for taxonomy meaning. It is legacy context. It may still contain useful attached notes, aliases, quantities, provenance, relationships, or metadata that were not visible in the partial graph JSON used during this work.

The agent must scan the live graph before deleting old nodes or relationships. The scan is **not** to re-litigate the new evidence batches. The scan is only to prevent destructive results: orphaned nodes, lost context, broken relationships, or hidden dependencies.

## Main rule

Use the new Markdown batches and cleaned taxonomy as authoritative.

Old generic taxonomy connections should be removed from the active graph when they duplicate, conflict with, or are replaced by the new evidence-backed mappings.

Before deletion:

1. scan what is connected to old nodes and edges;
2. reconnect useful context to the correct new taxonomy node/edge;
3. move unclear extra context to review/staging;
4. log anything unresolved;
5. only then retire/delete the old generic connection from the active graph.

## Source-of-truth order

1. Approved Markdown evidence batches.
2. Cleaned six-node taxonomy vocabulary.
3. Existing live graph IDs for `Projekt` and `Bauteilgruppe`.
4. Old taxonomy nodes/edges only as legacy context to scan and retire.

Do **not** treat old generic taxonomy edges as equal to the new evidence-backed batch mappings.

## Active target taxonomy

The active graph should use only this cleaned taxonomy structure:

```cypher
(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)

(:Bauteilgruppe)-[:HAT_ERGEBNIS]->(:Wiederverwendungsergebnis)
(:Bauteilgruppe)-[:HAT_QUELLE]->(:Quelle)
(:Bauteilgruppe)-[:HAT_WIEDERVERWENDUNGSORT]->(:Wiederverwendungsort)
(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren)
(:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)

(:Projekt)-[:NUTZT_METHODE]->(:Methode)
(:Methode)-[:ANGEWENDET_AUF]->(:Bauteilgruppe)
```

## Old content to replace and retire

### 1. Old `WiederverwendungsArt`

Remove old active edges:

```cypher
(:Bauteilgruppe)-[:HAT_WIEDERVERWENDUNGSART]->(:WiederverwendungsArt)
```

Replace their meaning with the new semantic dimensions:

```text
HAT_ERGEBNIS
HAT_QUELLE
HAT_WIEDERVERWENDUNGSORT
NUTZT_METHODE
ANGEWENDET_AUF
HAT_AUFBEREITUNG
```

Old `WiederverwendungsArt` nodes should be deleted or archived after their attached context has been scanned and reconnected.

### 2. Old generic `Rueckbauverfahren`

Replace old generic Rückbau edges with the new evidence-backed batch rows:

```cypher
(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(:Rueckbauverfahren)
```

The new batch mappings are authoritative. Do not manually re-litigate them if project/component matching is clear and batch evidence is present.

Old generic Rückbau nodes and edges should be removed from the active taxonomy after scan/reconnection, especially where they duplicate the new six-node Rückbau vocabulary.

### 3. Old generic `Aufbereitungsverfahren`

`Aufbereitungsverfahren` is also part of the same cleanup.

The cleaned taxonomy keeps `Aufbereitungsverfahren`, but only as the capped six-node controlled vocabulary from the cleaned taxonomy.

Old detailed, duplicate, or generic processing nodes/edges must be scanned and then replaced with the new evidence-backed batch mappings:

```cypher
(:Bauteilgruppe)-[:HAT_AUFBEREITUNG]->(:Aufbereitungsverfahren)
```

Old processing nodes such as detailed cleaning, cutting, refurbishment, remanufacturing, surface treatment, sorting, testing, coating, or repair variants should not remain as parallel active taxonomy nodes if they duplicate the new canonical processing categories.

Their useful detail should be preserved as edge metadata, for example:

```text
legacy_processing_detail
evidence_summary
evidence_phrase
source_file
old_node_id
old_node_name
```

The active `Aufbereitungsverfahren` vocabulary should be limited to the cleaned six nodes:

```text
Reinigung_und_Oberflaeche
Zuschnitt_und_Vereinzelung
Pruefung_Sortierung_QS
Reparatur_und_Refurbishment
Remanufacturing_und_Upcycling
Verstaerkung_und_Schutz
```

## Required pre-deletion scan

Before deleting or detaching any old `WiederverwendungsArt`, `Rueckbauverfahren`, or `Aufbereitungsverfahren` node/edge, scan:

- all incoming and outgoing relationships;
- all node and relationship properties;
- connected projects and component groups;
- notes, aliases, quantities, provenance, timestamps, labels, and user-added metadata;
- links to actors, sources, documents, locations, materials, or technical evidence;
- anything not represented in the new batches.

Minimum scan pattern:

```cypher
MATCH (old)
WHERE old:WiederverwendungsArt
   OR old:Rueckbauverfahren
   OR old:Aufbereitungsverfahren
OPTIONAL MATCH (old)-[r]-()
RETURN labels(old) AS labels,
       old.id AS old_id,
       old.name AS old_name,
       properties(old) AS old_node_properties,
       type(r) AS relationship_type,
       properties(r) AS relationship_properties,
       startNode(r).id AS start_id,
       endNode(r).id AS end_id;
```

Also scan old active edges:

```cypher
MATCH (bg:Bauteilgruppe)-[r:HAT_WIEDERVERWENDUNGSART|HAT_RUECKBAUVERFAHREN|HAT_AUFBEREITUNG]->(old)
RETURN bg.id AS bauteilgruppe_id,
       bg.name AS bauteilgruppe,
       type(r) AS old_relationship,
       labels(old) AS old_target_labels,
       old.id AS old_target_id,
       old.name AS old_target_name,
       properties(r) AS old_edge_properties;
```

## Reconnection rule

If old removed content has useful attached context, reconnect it to the new semantic equivalent.

Examples:

```text
old reuse type / outcome context        -> Wiederverwendungsergebnis
old source context                      -> Quelle
old reuse-location context              -> Wiederverwendungsort
old method/design/procurement context   -> Methode
old deconstruction context              -> Rueckbauverfahren
old cleaning/cutting/testing/repair context -> Aufbereitungsverfahren
```

If the semantic target is clear, reconnect directly.

If the semantic target is unclear, move the context to `REVIEW_LEGACY_CONTEXT` or an equivalent staging/report artifact.

Do not keep unclear old taxonomy edges in the cleaned active graph.

## Deletion / retirement policy

After scanning and reconnecting:

1. remove old `HAT_WIEDERVERWENDUNGSART` edges from the active graph;
2. archive/delete old `WiederverwendungsArt` nodes when no unique context remains;
3. replace old generic `HAT_RUECKBAUVERFAHREN` edges with new evidence-backed Rückbau rows;
4. archive/delete old generic `Rueckbauverfahren` nodes when replaced;
5. replace old generic `HAT_AUFBEREITUNG` edges with new evidence-backed Aufbereitung rows;
6. archive/delete old duplicate/detailed `Aufbereitungsverfahren` nodes when their useful detail has been preserved;
7. move unmatched or unclear old taxonomy context to review/staging, not the active taxonomy.

## Hard safety rules

- Do not delete before scanning.
- Do not preserve duplicate old taxonomy edges in the active graph when new batch mappings exist.
- Do not silently drop old attached context.
- Do not question or downgrade new batch mappings unless there is a clear project/component mismatch.
- Do not keep old detailed processing nodes as active taxonomy nodes if their meaning is covered by the six canonical `Aufbereitungsverfahren`.
- Do not modify project or component identity nodes unless explicitly required.
- Do not expand the six-node taxonomy vocabulary.

## Desired final state

The active graph should contain the cleaned taxonomy only.

Old `WiederverwendungsArt`, old generic `Rueckbauverfahren`, and old generic/detailed `Aufbereitungsverfahren` should no longer duplicate the new evidence-backed mappings.

All useful old context should either be:

1. reconnected to the new semantic equivalent,
2. preserved as metadata on the new edge,
3. archived in a legacy layer,
4. or listed in a review report.

The result should be context-aware, semantic-aware, non-destructive, and aligned with the new evidence-backed Markdown batches.
