# Agent 3 — Phase 1.2 + 1.3 Report

**Wave 1, Phase 1.2 (Ontology anchors) + Phase 1.3 (Propagated MARKTMODELL)**
**Database:** `mit-bestand`
**Author:** Agent 3 of 12
**Migration completed:** 2026-05-20T20:57:50Z
**Run root:** `E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/`

---

## TL;DR — Counts

| Action | Plan target | Actually applied | Status |
|---|---:|---:|---|
| `:Quelle → :OntologyAnchor` relabel | 2 | 2 | OK |
| `:BELEGT_IN → :ANCHORED_BY` retype | 716 | 716 | OK |
| Hard-delete deg-0 `:Quelle` (Phase 1.2.c) | 21 | 1 | See orchestration note below |
| Flag propagated `HAT_MARKTMODELL` | 319 | 319 | OK |
| Delete `HAT_DOMINANT_MARKTMODELL` | 86 | 86 | OK |
| Delete `HAT_DOMINANT_AKZEPTANZ` | 24 | 24 | OK |

**Net graph delta in this agent's scope:**
- Nodes: 2442 → 2441 (−1)
- Relationships: 19 714 → 19 604 (−110)
- Labels added: `:OntologyAnchor` (× 2)
- Labels removed: `:Quelle` (× 2, on the two anchors)
- Edge types added: `:ANCHORED_BY` (716)
- Edge types removed entirely: `:HAT_DOMINANT_MARKTMODELL`, `:HAT_DOMINANT_AKZEPTANZ`

(The 21 originally-named deg-0 `:Quelle` were already removed by Phase 1.5 before this agent ran; see "Orchestration note" below.)

---

## Pre-flight verification (immediately before this agent's run)

Snapshot (pre-prereqs) was at 2026-05-20T20:42 with `node_count=2580`, `relationship_count=19989`. By the time Agent 3 began executing Phase 1.2 the live graph had already been mutated by Agents 2/4/5/6 (Phases 1.1, 1.4, 1.5, 1.6). Live counts measured immediately before this agent's migration:

```
total_nodes : 2442      (snapshot 2580; −138 from concurrent Wave-1 phases)
total_rels  : 19 714    (snapshot 19 989; −275 from concurrent Wave-1 phases)

# In-scope counts for Phases 1.2 + 1.3 (all matched plan expectations):
anchors_as_quelle                       : 2     (plan: 2)
belegt_in_to_anchors                    : 716   (plan: 716 = 457 + 259)
deg0_quelle                             : 1     (plan: 21 — see note)
hat_marktmodell_with_propagated_excerpt : 319   (plan: 319)
hat_dominant_marktmodell                : 86    (plan: 86)
hat_dominant_akzeptanz                  : 24    (plan: 24)
```

All in-scope counts match the plan exactly (319 / 86 / 24 / 716 / 2). The deg-0 Quelle delta is explained next.

---

## Orchestration note — deg-0 :Quelle accounting

The plan defers all 21 named deg-0 `:Quelle` deletions from section 1.5 to section 1.2.c ("Quelle — 21 to delete (already covered in 1.2)"). In this Wave-1 run, **Agent 5's Phase 1.5 migration ran before Agent 3's Phase 1.2 migration and deleted the 21 named Quelle inside its own surgical-delete batch** (timestamp `2026-05-20T20:52:58Z` per `deleted/phase1_5_nodes.jsonl`). This is a divergence from the plan's "deferred to 1.2" wording, but the resulting state is identical to the plan's intent: those 21 nodes are gone and journalled.

By the time Agent 3 ran Phase 1.2.c only **one** deg-0 `:Quelle` remained — `q_phase20_kette_autodiscovery` — which had become orphaned as **collateral from Phase 1.1's `Wiederverwendungskette` deletion** (Agent 2 deleted the 98 unwired chains that pointed to this node via `BELEGT_IN`). Phase 1.2.c correctly captured and deleted this single residual orphan via the broad `MATCH (q:Quelle) WHERE NOT exists{...}` pattern.

`deleted/phase1_2_quelle.jsonl` records all 22 entries:
- 21 named-and-already-deleted (with cross-reference `actually_deleted_in=phase_1_5`, `preempted_by=agent_5`);
- 1 newly-orphaned (`q_phase20_kette_autodiscovery`, `collateral_cause=phase_1_1_chain_deletion_orphaned_this_node`).

This is the *exact* end state the plan describes; the only departure is which agent journal logs which node.

---

## Phase 1.2 — execution detail

### 1.2.a — relabel anchors (`:Quelle` → `:OntologyAnchor`)

```cypher
MATCH (q:Quelle)
WHERE q.id IN ['q_controlled_vocab_seed', 'q_akteursliste_master_md']
REMOVE q:Quelle SET q:OntologyAnchor
```

| anchor id | new labels |
|---|---|
| `q_controlled_vocab_seed` | `[OntologyAnchor]` |
| `q_akteursliste_master_md` | `[OntologyAnchor]` |

Counter summary: `labels_added=2`, `labels_removed=2`.

### 1.2.b — retype 716 `:BELEGT_IN` to `:ANCHORED_BY`

```cypher
MATCH (n)-[r:BELEGT_IN]->(a:OntologyAnchor)
CREATE (n)-[r2:ANCHORED_BY]->(a)
SET r2 = {
    evidence_origin:     'derived',
    evidence_basis:      'controlled_vocab',
    evidence_excerpt:    NULL,
    evidence_source_id:  a.id,
    evidence_confidence: 'bookkeeping'
}
DELETE r
```

| anchor id | `ANCHORED_BY` in-edges | evidence_origin | evidence_basis | evidence_confidence |
|---|---:|---|---|---|
| `q_controlled_vocab_seed` | 457 | `derived` | `controlled_vocab` | `bookkeeping` |
| `q_akteursliste_master_md` | 259 | `derived` | `controlled_vocab` | `bookkeeping` |
| **total** | **716** | | | |

Counter summary: `relationships_created=716`, `relationships_deleted=716`, `properties_set=2864` (= 716 × 4 non-NULL properties).

The original `:BELEGT_IN` edge properties (`id`, `source`, `evidence`, `datenqualitaet`, `source_scope`) are intentionally dropped per the plan's `SET r2 = shape` semantics; the snapshot at `snapshot/relationships.jsonl` and this migration file preserve the audit trail.

Note: `:ZITIERT_QUELLE` edges incident to `q_akteursliste_master_md` (the registry's own outbound citations) were left untouched — they are not bookkeeping and remain semantically correct on the new `:OntologyAnchor`.

### 1.2.c — hard-delete remaining deg-0 `:Quelle`

```cypher
MATCH (q:Quelle)
WHERE NOT exists { (q)<-[]-() } AND NOT exists { (q)-[]->() }
WITH q, q.id AS deleted_id
DELETE q
```

| deleted id | reason |
|---|---|
| `q_phase20_kette_autodiscovery` | Phase-1.1 collateral (its only `:BELEGT_IN` back-references were on the 98 deleted `:Wiederverwendungskette` chains) |

Counter summary: `nodes_deleted=1`.

---

## Phase 1.3 — execution detail

### 1.3.a — flag 319 propagated `HAT_MARKTMODELL` edges

```cypher
MATCH ()-[r:HAT_MARKTMODELL]->()
WHERE r.source_excerpt CONTAINS 'propagated'
WITH r, r.source_excerpt AS original_excerpt
SET r.evidence_origin         = 'derived',
    r.evidence_basis          = 'propagated',
    r.evidence_excerpt        = NULL,
    r.evidence_confidence     = 'bookkeeping',
    r.original_source_excerpt = original_excerpt
REMOVE r.source_excerpt
```

Post-state:

| filter | count |
|---|---:|
| `HAT_MARKTMODELL` total | 384 |
| `HAT_MARKTMODELL` with `evidence_basis='propagated'` | 319 |
| `HAT_MARKTMODELL` with `original_source_excerpt` set | 319 |
| `HAT_MARKTMODELL` still carrying `source_excerpt` | 0 |
| `HAT_MARKTMODELL` untouched (real excerpts) | 65 |

Counter summary: `properties_set=1595`.

The sole literal template string observed across all 319 edges was:
```
"propagated from project HAT_DOMINANT_MARKTMODELL (project-wide sourcing)"
```
This is preserved verbatim under `original_source_excerpt` on every flagged edge for future reverse-engineering.

### 1.3.b — delete 86 `HAT_DOMINANT_MARKTMODELL` edges

```cypher
MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->() DELETE r
```

Counter summary: `relationships_deleted=86`. Post-count of the type: 0.

### 1.3.c — delete 24 `HAT_DOMINANT_AKZEPTANZ` edges

```cypher
MATCH ()-[r:HAT_DOMINANT_AKZEPTANZ]->() DELETE r
```

Counter summary: `relationships_deleted=24`. Post-count of the type: 0.

---

## Post-migration assertions (all PASSED)

```
anchors_as_quelle                        == 0     OK
anchors_as_ontology_anchor               == 2     OK
belegt_in_to_anchors                     == 0     OK
anchored_by_to_anchors                   == 716   OK
deg0_quelle                              == 0     OK
hat_marktmodell_with_propagated_excerpt  == 0     OK
hat_marktmodell_with_propagated_basis    == 319   OK
hat_dominant_marktmodell                 == 0     OK
hat_dominant_akzeptanz                   == 0     OK
total_nodes (before − 1)                 == 2441  OK
total_rels  (before − 110)               == 19604 OK
```

---

## Deliverables

| Path | Purpose |
|---|---|
| `migrations/mig_1_2_anchor_relabel.cypher` | Authoritative Phase 1.2 Cypher (1.2.a + 1.2.b + 1.2.c) |
| `migrations/mig_1_3_flag_propagated.cypher` | Authoritative Phase 1.3 Cypher (1.3.a + 1.3.b + 1.3.c) |
| `logs/migrate_helper_p1_2_3.py` | Python runner — parses + executes the two .cypher files inside transactional write sessions against `mit-bestand`; emits structured per-statement results |
| `logs/phase1_2_3_progress.log` | Stamped per-statement execution log |
| `logs/phase1_2_3_result.json` | JSON of before/after counts + per-statement counters and returns |
| `logs/PHASE_1_2_DONE.flag` | Wave-1 done flag for Phase 1.2 |
| `logs/PHASE_1_3_DONE.flag` | Wave-1 done flag for Phase 1.3 |
| `deleted/phase1_2_quelle.jsonl` | 22 forensic records: 21 named-already-preempted + 1 new orphan actually deleted by 1.2.c |
| `reports/agent_3_phase1_2_3_report.md` | (this file) |

---

## Recovery / rollback notes

- **Phase 1.2.a is fully reversible** — `:OntologyAnchor` → `:Quelle` is a one-line `REMOVE … SET …` swap (the 2 ids are well known).
- **Phase 1.2.b is reversible from `snapshot/relationships.jsonl`** — every original `:BELEGT_IN` property tuple is recorded there. The new `:ANCHORED_BY` edges can be deleted and the originals re-played 1:1.
- **Phase 1.2.c is reversible from `snapshot/nodes.jsonl`** plus `deleted/phase1_2_quelle.jsonl` for the 1 node Agent 3 actually deleted. The 21 1.5-preempted nodes are recoverable from `deleted/phase1_5_nodes.jsonl`.
- **Phase 1.3.a is reversible inside the DB** — `r.original_source_excerpt` holds the literal template string; a single Cypher swap moves it back to `r.source_excerpt` and clears the canonical evidence fields.
- **Phase 1.3.b / 1.3.c are reversible from `snapshot/relationships.jsonl`** — the 110 deleted edges (and their properties) are recorded there.

---

## Boundaries respected

- Did **NOT** run Phase 1.1, 1.4, 1.5, or 1.6 (those were owned by other Wave-1 agents).
- Did **NOT** modify any node outside the two named ontology anchors and the one orphan Quelle.
- Did **NOT** modify any edge type outside `:BELEGT_IN` (only on the two anchors), `:HAT_MARKTMODELL` (only the 319 propagated subset), `:HAT_DOMINANT_MARKTMODELL`, and `:HAT_DOMINANT_AKZEPTANZ`.
- Did **NOT** introduce new label or edge-type combinations beyond those explicitly specified in the plan (`:OntologyAnchor`, `:ANCHORED_BY`).

---

## Final returned counts (for orchestrator)

```json
{
  "phase_1_2": {
    "quelle_to_ontology_anchor": 2,
    "belegt_in_to_anchored_by":   716,
    "deg0_quelle_deleted":         1,
    "deg0_quelle_preempted_by_1_5": 21
  },
  "phase_1_3": {
    "hat_marktmodell_flagged":         319,
    "hat_dominant_marktmodell_deleted": 86,
    "hat_dominant_akzeptanz_deleted":   24
  },
  "graph_delta": { "nodes": -1, "relationships": -110 },
  "graph_after": { "nodes": 2441, "relationships": 19604 }
}
```
