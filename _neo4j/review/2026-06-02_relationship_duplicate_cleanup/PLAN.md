# Relationship duplicate cleanup plan

**Date:** 2026-06-02  
**Database:** `mit-bestand`  
**Source of truth:** live Neo4j graph, not `_archive/research/` or old `_database` material.

## 1. Baseline

Live baseline from `_scripts/_gap_survey.py` and direct Neo4j queries:

| Check | Result |
|---|---:|
| Total nodes | 5,476 |
| Total relationships | 25,104 |
| Distinct relationship types | 77 |
| Exact parallel duplicates, same start/type/end | 0 |
| Relationships with `r.id IS NULL` | 127 |

The duplicate problem is therefore not exact parallel relationships. It is semantic overlap: same start node, same end node, different relationship type.

Current gap survey failures to keep in scope:

| Gap | Count |
|---|---:|
| `r.id NULL` | 127 |
| Case-specific nodes missing `BELEGT_IN` | 4 |
| `Bauteilgruppe` missing `HAT_MATERIALGRUPPE` | 1 |
| `Bauteilgruppe` missing `HAT_WIEDERVERWENDUNGSART` | 2 |

These are not all duplicate-cleanup tasks, but they must be acceptance gates so the cleanup does not hide existing regressions.

## 2. Duplicate classes found

### A. `HAS_BAUWERK` + `NUTZT_BAUWERK`

Live finding:

| Pattern | Count |
|---|---:|
| Same `(:Projekt)->(:Bauwerk)` pair has both types | 139 |
| `HAS_BAUWERK` total | 166 |
| `NUTZT_BAUWERK` total | 166 |
| Overlap where `HAS_BAUWERK.role = 'donor'` | 71 |
| Overlap where `HAS_BAUWERK.role = 'receiver'` | 68 |
| `HAS_BAUWERK` without matching `NUTZT_BAUWERK` | 27 |
| `NUTZT_BAUWERK` without matching `HAS_BAUWERK` | 10 |

Observed property pattern:

- `HAS_BAUWERK` carries `role: donor|receiver` and usually `evidence_confidence: teilweise_belegt`.
- `NUTZT_BAUWERK` usually only carries `id` and `evidence_confidence: unklar`.
- Several donor Bauwerke are also linked by `NUTZT_BAUWERK`, which makes the old relation semantically ambiguous.

Proposed canonical rule:

Use `HAS_BAUWERK` as the canonical project-to-building topology edge, because it preserves donor/receiver role. Treat `NUTZT_BAUWERK` as legacy/older project building relation.

Cleanup action:

1. For every duplicate pair with both `HAS_BAUWERK` and `NUTZT_BAUWERK`, keep `HAS_BAUWERK`.
2. Before deleting `NUTZT_BAUWERK`, copy any non-duplicate useful properties into audit fields on `HAS_BAUWERK`, for example `legacy_nutzt_bauwerk_rel_id`, `legacy_nutzt_bauwerk_props`, `relationship_cleanup_run`.
3. For the 10 `NUTZT_BAUWERK`-only pairs, create `HAS_BAUWERK` only after role classification:
   - if target Bauwerk is the receiving/current project building, set `role: 'receiver'`;
   - if target Bauwerk is donor/source, set `role: 'donor'`;
   - if role cannot be inferred from existing graph context, send to review queue.
4. Update diagnostics and downstream queries that currently require `Projekt-[:NUTZT_BAUWERK]->Bauwerk` so they check `HAS_BAUWERK {role:'receiver'}` or any `HAS_BAUWERK` depending on intent.

Do not delete all `NUTZT_BAUWERK` until `_scripts/_gap_survey.py` and query/export scripts are updated, otherwise the cleanup would create an artificial "Projekt missing NUTZT_BAUWERK" regression.

### B. `GEHÖRT_ZU` + `LIEGT_IN_LAND`

Live finding:

| Pattern | Count |
|---|---:|
| Same source/target has both `GEHÖRT_ZU` and `LIEGT_IN_LAND` to `:Land` | 196 |
| Overlap from `:Akteur` to `:Land` | 195 |
| Overlap from `:Software` to `:Land` | 1 |
| `GEHÖRT_ZU` to `:Land` without matching `LIEGT_IN_LAND` | 14 |
| `LIEGT_IN_LAND` without matching `GEHÖRT_ZU` | 451 |

Observed property pattern:

- `GEHÖRT_ZU` duplicates have `rolle: 'land'` and mostly `evidence_confidence: unklar`.
- `LIEGT_IN_LAND` is the current explicit geography relation. The Bauteilbörse schema already marks `GEHÖRT_ZU -> :Land` as legacy and says to prefer `LIEGT_IN_LAND`.

Proposed canonical rule:

Use `LIEGT_IN_LAND` for all country links. Reserve `GEHÖRT_ZU` for non-geographic legacy semantics until those are separately reviewed.

Cleanup action:

1. For the 196 duplicate pairs, keep `LIEGT_IN_LAND`.
2. Archive each deleted `GEHÖRT_ZU` relationship with `elementId`, `id`, properties, source id, target id, and run id in a JSONL ledger.
3. For the 14 `GEHÖRT_ZU -> :Land` only pairs, create matching `LIEGT_IN_LAND` first, preserving `evidence_confidence` and adding `migrated_from_rel_type: 'GEHÖRT_ZU'`; then archive/delete the legacy edge.
4. Do not touch the 40 `GEHÖRT_ZU` actor-to-actor edges in this pass.

### C. `BELEGT_IN` + `ANCHORED_BY`

Live finding:

| Pattern | Count |
|---|---:|
| Same source and same `:OntologyAnchor` has both `BELEGT_IN` and `ANCHORED_BY` | 695 |

Observed property pattern:

- `BELEGT_IN` often has only deterministic `id`.
- `ANCHORED_BY` often adds `evidence_confidence: unklar`.
- Targets are `:OntologyAnchor`, not normal source documents.

Risk:

This looks like a large technical duplicate class, but `ANCHORED_BY` may be an internal ontology anchoring construct rather than evidence. Do not auto-delete until consumers and schema intent are checked.

Cleanup action:

1. Inventory consumers that query `ANCHORED_BY` or `BELEGT_IN` to `:OntologyAnchor`.
2. Decide whether `OntologyAnchor` should use only `ANCHORED_BY` and real evidence should use only `BELEGT_IN`, or whether both are intentionally dual-purpose.
3. If one relation is retired, migrate the weaker relation into archived provenance fields and delete only after query/export tests pass.

### D. `STUB_PROJECT_LINK` + `BETEILIGT_AN`

Live finding:

| Pattern | Count |
|---|---:|
| Same `(:Akteur)->(:Projekt|:Programm)` pair has both types | 45 |

Observed property pattern:

- `STUB_PROJECT_LINK` often has `not_confirmed_project_participation: true`.
- `BETEILIGT_AN` often has `evidence_confidence: unklar`.

Risk:

This is not a safe duplicate. It is a trust-state conflict: one edge says "association only / not confirmed participation", the other asserts participation.

Cleanup action:

1. Generate a review queue for all 45 pairs.
2. If no project-file or external source confirms participation, keep `STUB_PROJECT_LINK` and delete/demote `BETEILIGT_AN`.
3. If participation is confirmed, keep `BETEILIGT_AN` and delete `STUB_PROJECT_LINK`, preserving `association_basis` in provenance.
4. Record decision per pair with `review_status`, reviewer/run id, and evidence source.

### E. `FROM_DONOR` + `INTO_RECEIVER`

Live finding:

| Pattern | Count |
|---|---:|
| Same `(:Bauteilgruppe)->(:Bauwerk|:Materialdepot)` pair has both types | 31 |

Risk:

This may be either a true modeling error or a legitimate "retained in same building" situation. It is unsafe to collapse automatically.

Cleanup action:

1. Split candidates by `Bauteilgruppe.id` prefix and target role:
   - `bg_retained_*` may legitimately be both source and receiver;
   - `bg_reuse_*` with same donor and receiver likely needs correction;
   - `:Materialdepot` targets need separate treatment because they may represent source depots rather than buildings.
2. For each candidate, inspect project context and `HAS_BAUWERK.role`.
3. Keep both only when the retained/component-in-place interpretation is explicit.
4. Otherwise retain the correct directional edge and archive the wrong one.

### F. Other smaller overlap classes

| Pattern | Count | Initial action |
|---|---:|---|
| `BELEGT_IN` + `HAS_SOURCE_LINK` on `ReuseRule->Quelle` | 20 | likely standardize to `BELEGT_IN`, but inspect rule consumers first |
| `GEHÖRT_ZU` + `VERBUNDEN_MIT_AKTEUR` on `Akteur->Akteur` | 13 | review, not automatic |
| `GEHÖRT_ZU` + `BETEILIGT_AN` on `Akteur->Akteur` | 7 | review, likely old fold noise |
| `HAS_RISK_POLLUTANT` + `REQUIRES_VERIFICATION_FOR` on `Projekt->Schadstoff` | 3 | probably different semantics; keep until pollutant schema is reviewed |

## 3. Execution phases

### Phase 0. Backup and ledger setup

1. Create backup under `_neo4j/review/backups/2026-06-02_pre_relationship_duplicate_cleanup`.
2. Create run directory under `_neo4j/intake/runs/2026-06-02_relationship_duplicate_cleanup`.
3. Write:
   - `pre_counts.json`
   - `duplicate_candidates.json`
   - `deleted_relationships.jsonl`
   - `manual_review_queue.jsonl`

### Phase 1. Safe geography canonicalization

Scope:

- `GEHÖRT_ZU -> :Land` only.
- Either duplicate with `LIEGT_IN_LAND` or migratable land-only legacy edge.

Acceptance:

- `MATCH (a)-[:GEHÖRT_ZU]->(l:Land) WHERE EXISTS { (a)-[:LIEGT_IN_LAND]->(l) } RETURN count(*)` returns `0`.
- `MATCH (a)-[:GEHÖRT_ZU]->(:Land) RETURN count(*)` returns `0`, unless a deliberate exception list is created.
- Existing `LIEGT_IN_LAND` country coverage does not decrease.

### Phase 2. Project/building canonicalization

Scope:

- `(:Projekt)-[:HAS_BAUWERK|NUTZT_BAUWERK]->(:Bauwerk)`.

Acceptance:

- `MATCH (p:Projekt)-[:HAS_BAUWERK]->(bw:Bauwerk) MATCH (p)-[:NUTZT_BAUWERK]->(bw) RETURN count(*)` returns `0`.
- All former duplicate `NUTZT_BAUWERK` data is present either on the kept `HAS_BAUWERK` edge or in the ledger.
- The 10 `NUTZT_BAUWERK`-only pairs are either converted to `HAS_BAUWERK` with reviewed `role` or listed in `manual_review_queue.jsonl`.
- `_scripts/_gap_survey.py` is updated before deleting `NUTZT_BAUWERK` if it remains a diagnostic dependency.

### Phase 3. Trust-conflict review queues

Scope:

- `STUB_PROJECT_LINK` + `BETEILIGT_AN`
- `FROM_DONOR` + `INTO_RECEIVER`
- actor-to-actor `GEHÖRT_ZU` overlaps

Acceptance:

- No automatic deletes in this phase.
- Every candidate has a review record with proposed action, evidence status, and reviewer decision slot.

### Phase 4. Technical relation ID repair

Scope:

- 127 relationships with missing `r.id`.

Acceptance:

- `MATCH ()-[r]->() WHERE r.id IS NULL RETURN count(r)` returns `0`.
- Deterministic ids do not collide.
- Run `_scripts/_gap_survey.py` after repair.

### Phase 5. Optional ontology-anchor cleanup

Scope:

- `BELEGT_IN` + `ANCHORED_BY` on `:OntologyAnchor`.

Acceptance:

- Only after confirming schema intent and downstream consumers.
- Either relation pair is documented as intentionally dual, or one relation is retired with a migration ledger.

## 4. Suggested Cypher probes

Duplicate class inventory:

```cypher
MATCH (a)-[r]->(b)
WITH a, b, collect(DISTINCT type(r)) AS ts, count(r) AS rels
WHERE size(ts) > 1
RETURN labels(a) AS from_labels, a.id AS from_id, a.name AS from_name,
       labels(b) AS to_labels, b.id AS to_id, b.name AS to_name,
       ts, rels
ORDER BY size(ts) DESC, from_id, to_id;
```

Safe land duplicate gate:

```cypher
MATCH (a)-[g:GEHÖRT_ZU]->(l:Land)
WHERE EXISTS { (a)-[:LIEGT_IN_LAND]->(l) }
RETURN count(g) AS duplicate_gehoert_land;
```

Project/building duplicate gate:

```cypher
MATCH (p:Projekt)-[h:HAS_BAUWERK]->(bw:Bauwerk)
MATCH (p)-[n:NUTZT_BAUWERK]->(bw)
RETURN count(*) AS duplicate_project_bauwerk_pairs,
       count { WHERE h.role = 'donor' } AS donor_pairs,
       count { WHERE h.role = 'receiver' } AS receiver_pairs;
```

Relationship id gate:

```cypher
MATCH ()-[r]->()
WHERE r.id IS NULL
RETURN type(r) AS rel_type, count(r) AS missing_id_count
ORDER BY missing_id_count DESC;
```

## 5. Do not do

- Do not merge nodes based on name similarity.
- Do not use `_archive/research/` as authority for cleanup decisions.
- Do not delete `STUB_PROJECT_LINK`, `FROM_DONOR`, `INTO_RECEIVER`, or actor-to-actor `GEHÖRT_ZU` automatically.
- Do not remove `NUTZT_BAUWERK` until diagnostics and export/query consumers have been updated or explicitly accepted.

