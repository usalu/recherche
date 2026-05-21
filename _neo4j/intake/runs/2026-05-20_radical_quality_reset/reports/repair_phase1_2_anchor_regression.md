# Repair Report - Phase 1.2 Anchor Regression

- **Repair agent:** A
- **Database:** `mit-bestand`
- **Migration:** `migrations/mig_repair_1_2_anchor_regression.cypher`
- **Audit:** `logs/repair_phase1_2_anchor_regression_audit.jsonl`
- **Completion flag:** `PHASE_1_2_REPAIR_DONE.flag`

## Problem

Final Verifier 2 found a post-Phase-1.2 regression for `q_akteursliste_master_md`:

- A duplicate `:Quelle {id:'q_akteursliste_master_md'}` shell existed beside the surviving `:OntologyAnchor`.
- 202 `BELEGT_IN` relationships targeted the `:OntologyAnchor`.
- The duplicate `:Quelle` shell also carried 202 duplicate incoming `BELEGT_IN` relationships and 277 outgoing `ZITIERT_QUELLE` relationships already present on the real anchor.

The original Phase 1.2 contract is that ontology anchors are not `:Quelle` nodes and receive anchor bookkeeping via `ANCHORED_BY`, not `BELEGT_IN`.

## Audit

Before graph mutation, `logs/repair_phase1_2_anchor_regression_audit.jsonl` was written with:

- Summary counts before repair.
- The duplicate `:Quelle` node properties and degree.
- All 202 `BELEGT_IN` relationships targeting the `:OntologyAnchor`.
- All 202 duplicate `BELEGT_IN` relationships targeting the duplicate `:Quelle`.
- All 277 duplicate `ZITIERT_QUELLE` relationships from the duplicate shell, including whether the target citation already existed on the real anchor.

## Repair

The migration made four scoped changes:

1. Reused or created canonical `(source)-[:ANCHORED_BY]->(:OntologyAnchor {id:'q_akteursliste_master_md'})` relationships for the 202 regressed anchor-targeting `BELEGT_IN` edges, then removed those `BELEGT_IN` edges.
2. Preserved actor-registry source-as-link behavior by ensuring `ZITIERT_QUELLE` existed from the real `:OntologyAnchor` to each cited actor URL, then removed only the duplicate shell copies.
3. Removed the duplicate shell's incoming `BELEGT_IN` relationships after the real anchor had canonical `ANCHORED_BY` coverage.
4. Deleted the duplicate `:Quelle` shell only after it had no remaining relationships.

199 of the 202 source nodes already had canonical `ANCHORED_BY` relationships from the original Phase 1.2 migration. The repair therefore created only three missing canonical edges and avoided duplicating the 199 existing ones. A final refresh on the shared live graph showed `ANCHORED_BY` at 703 after unrelated graph drift, still within the acceptance range.

## Live Verification

| Gate | Before | After | Status |
|---|---:|---:|---|
| `:Quelle` with controlled-vocab anchor ids | 1 | 0 | PASS |
| `BELEGT_IN` to any `:OntologyAnchor` | 202 | 0 | PASS |
| `OntologyAnchor` count | 2 | 2 | PASS |
| `ANCHORED_BY` to any `:OntologyAnchor` | 702 | 703 | PASS |
| `ANCHORED_BY` to `q_akteursliste_master_md` | 259 | 260 | PASS |
| `BELEGT_IN` to any node with id `q_akteursliste_master_md` | 404 | 0 | PASS |
| `ZITIERT_QUELLE` from real `q_akteursliste_master_md` anchor | 319 | 319 | PASS |
| Non-canonical `ANCHORED_BY` shape to anchors | n/a | 0 | PASS |

Sample repaired or retained `ANCHORED_BY` edges from `werner_sobek_p`, `land_deutschland`, and `land_usa` all have:

- `evidence_origin = 'derived'`
- `evidence_basis = 'controlled_vocab'`
- `evidence_source_id = 'q_akteursliste_master_md'`
- `evidence_confidence = 'bookkeeping'`
- no `BELEGT_IN` relationship remains to the anchor id

## Risk Notes

- The repair intentionally deleted duplicate shell evidence relationships after auditing them because keeping or merging them as `BELEGT_IN` would reintroduce the Phase 1.2 violation.
- `ZITIERT_QUELLE` source-as-link behavior remains on the surviving `:OntologyAnchor`; the count stayed at 319.
- No unrelated source links or evidence relationships were rewritten.
