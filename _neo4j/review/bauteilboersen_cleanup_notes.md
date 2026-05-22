# Bauteilboersen cleanup notes

Date: 2026-05-28

## What was cleaned now

`bauteilboersen_country_actor_graph.cypher` was tightened for graph display:

- only canonical actor-registry materialhub nodes are used (`source_scope = actor_registry_context`);
- `bauteilnetz_deutschland` is included explicitly as network context;
- `VERBUNDEN_MIT_AKTEUR` is matched only outbound from the hub/network, avoiding reciprocal display duplicates;
- the query returns `p` paths, so Neo4j Browser renders an actual graph.

## Duplicate classes found in processed data

### 1. Display duplicates

The previous graph query used undirected `VERBUNDEN_MIT_AKTEUR` plus a separate `bauteilnetz_deutschland` section. That showed both directions of reciprocal actor links, for example:

- `bauteilboerse_bremen -> bauteilnetz_deutschland`
- `bauteilnetz_deutschland -> bauteilboerse_bremen`

These are not necessarily wrong graph facts, but they make the visual graph noisy.

### 2. Reciprocal actor links

Many `VERBUNDEN_MIT_AKTEUR` pairs exist in both directions. This appears intentional in the actor-registry import style, but for visualization it should usually be treated as one undirected association.

Use `_neo4j/review/bauteilboersen_duplicate_audit.cypher` section 2 to inspect them.

### 3. Exact repeated semantic relationships

The processed scan found repeated `(start, type, end)` triples, especially from seed/vocabulary and project-local generated records, for example:

- `mat_stahl -> HAT_MATERIALGRUPPE -> mg_metall`
- `stadt_london -> LIEGT_IN_LAND -> land_vereinigtes_koenigreich`
- `a_cleveland_steel_tubes -> HAT_AKTEURTYP -> at_materialhub_bauteilboerse`

These should be deduplicated only after checking whether duplicate rels carry different provenance that needs to be preserved.

### 4. Duplicate-ish materialhub actor identities

High-priority review candidates:

| Candidate IDs | Reading |
|---|---|
| `rotordc`, `a_rotordc`, `a_rotor_dc` | likely same actor, but project-local IDs carry project provenance |
| `a_cleveland_steel_tubes`, `a_cleveland_steel_and_tubes` | likely same actor spelling variant |

Suggested merge targets, pending review:

| Merge into | Merge from |
|---|---|
| `rotordc` | `a_rotordc`, `a_rotor_dc` |
| `a_cleveland_steel_tubes` | `a_cleveland_steel_and_tubes` |

Do not merge by name similarity alone. Preserve source/project provenance from merged nodes and relationships.

## Next safe cleanup order

1. Run `_neo4j/review/bauteilboersen_duplicate_audit.cypher` read-only.
2. Confirm the exact duplicate rels where all duplicate rel properties are equivalent or safely unionable.
3. For actor merges, move/merge relationships first, union aliases/provenance, then retire the old node IDs.
4. Add/import id-mapping so future project-local imports resolve `a_rotordc` and `a_rotor_dc` to `rotordc`.
