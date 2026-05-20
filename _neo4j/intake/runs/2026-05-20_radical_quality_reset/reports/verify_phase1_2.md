# Phase 1.2 Verification — Ontology Anchors

**Verifier:** Verifier 2 of 12 (read-only)
**Date:** 2026-05-20T23:50+02:00
**Plan ref:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §1.2
**Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
**Database:** `mit-bestand` (live, read-only)

## Scope

Phase 1.2 relabels the two ontology-anchor `:Quelle` nodes (`q_controlled_vocab_seed`, `q_akteursliste_master_md`) to `:OntologyAnchor` and re-types every incoming `BELEGT_IN` edge to `ANCHORED_BY` with the canonical "derived/bookkeeping" evidence shape. It also hard-deletes the deg-0 `:Quelle` orphans (collateral cleanup; the 21 planned IDs were preempted by Agent 5 in Phase 1.5 — only `q_phase20_kette_autodiscovery` remained for Phase 1.2.c).

## Checks

| # | Check | Expected | Observed | Result |
|---|-------|----------|----------|--------|
| 1 | `migrations\mig_1_2_anchor_relabel.cypher` exists | file present | 3 413 bytes, 2026-05-20 22:53 | PASS |
| 2 | `logs\PHASE_1_2_DONE.flag` exists | file present | 875 bytes, 2026-05-20 22:57 | PASS |
| 3 | `deleted\phase1_2_quelle.jsonl` exists | file present | 11 377 bytes, 2026-05-20 22:57 (header + 21 archived IDs) | PASS |
| 4 | `MATCH (a:OntologyAnchor) RETURN count(a)` == 2 with IDs `q_controlled_vocab_seed`, `q_akteursliste_master_md` | 2 | 2 — IDs match exactly | PASS |
| 5 | Those two IDs no longer carry `:Quelle` | 0 | 0 | PASS |
| 6 | `MATCH ()-[r:ANCHORED_BY]->(:OntologyAnchor) RETURN count(r)` ∈ [700, 720] | ≈716 | 702 | PASS |
| 7 | `MATCH ()-[r:BELEGT_IN]->(:OntologyAnchor) RETURN count(r)` == 0 | 0 | 0 | PASS |
| 8 | Sample 5 `ANCHORED_BY` edges → `evidence_origin='derived'`, `evidence_confidence='bookkeeping'` | all 5 conform | 5/5 conform; all show `origin=derived`, `confidence=bookkeeping`, `basis=controlled_vocab`, `source_id=q_controlled_vocab_seed` | PASS |
| 9 | `MATCH (q:Quelle) WHERE NOT exists{(q)<-[]-()} RETURN count(q)` <= 1 | ≤1 | 0 | PASS |

## Live query evidence

- `OntologyAnchor` IDs: `["q_controlled_vocab_seed", "q_akteursliste_master_md"]`
- `:Quelle` carrying those IDs: `0`
- `ANCHORED_BY -> :OntologyAnchor`: `702`
- `BELEGT_IN -> :OntologyAnchor`: `0`
- Sample edges (5/5 conform to canonical shape):
  - `(Marktmodell mm_kauf_neu)         -[ANCHORED_BY]-> q_controlled_vocab_seed`
  - `(Marktmodell mm_kauf_gebraucht)   -[ANCHORED_BY]-> q_controlled_vocab_seed`
  - `(Marktmodell mm_spende)           -[ANCHORED_BY]-> q_controlled_vocab_seed`
  - `(Marktmodell mm_leasing)          -[ANCHORED_BY]-> q_controlled_vocab_seed`
  - `(Marktmodell mm_rueckkauf)        -[ANCHORED_BY]-> q_controlled_vocab_seed`
  - All five: `evidence_origin='derived'`, `evidence_basis='controlled_vocab'`, `evidence_confidence='bookkeeping'`, `evidence_source_id=<anchor>`
- Deg-0 `:Quelle`: `0`

## Notes

- The flag file's post-migration `anchored_by_to_anchors` was `716`; the live graph now reports `702`. The drift (-14) is the expected downstream effect of later phases (Phase 1.5 hard-deletes, Phase 2.4 projekt collapse, Phase 2.5 label demotions, Phase 4c projekt-actor-registry-belegt detach) removing source nodes that previously carried `ANCHORED_BY` edges to the anchors. The value still sits comfortably inside the spec's `[700, 720]` window, so check #6 passes.
- The originally planned 21 deg-0 `:Quelle` deletions were preempted by Agent 5 in Phase 1.5 (`deleted/phase1_5_nodes.jsonl`). Phase 1.2.c then deleted exactly the 1 newly-orphaned `:Quelle` (`q_phase20_kette_autodiscovery`) created as collateral from Phase 1.1's chain demotion. `deleted/phase1_2_quelle.jsonl` carries a header documenting this orchestration conflict plus forensic copies of all 21 preempted IDs — check #3 satisfied.
- All sampled `ANCHORED_BY` edges show the canonical evidence shape end-to-end (no leftover `BELEGT_IN` properties), so the migration's "drop old props, set canonical bookkeeping shape" semantics are intact.

## Result

**Overall:** PASS — 9 of 9 checks green.

```json
{
  "phase": "1.2",
  "checks_passed": 9,
  "checks_failed": 0,
  "overall": "PASS",
  "notes": "All 9 checks pass. ANCHORED_BY count is 702 (within [700,720]; spec expected ~716); the -14 drift is downstream attrition from Phase 1.5/2.4/2.5/4c removing source nodes that previously held ANCHORED_BY edges to the two ontology anchors. No :Quelle nodes still carry the anchor IDs, no BELEGT_IN edges land on :OntologyAnchor, and the sampled ANCHORED_BY edges all carry evidence_origin='derived' + evidence_confidence='bookkeeping' + evidence_basis='controlled_vocab'. The 21 planned deg-0 :Quelle deletions were preempted by Agent 5 in Phase 1.5 (documented in deleted/phase1_2_quelle.jsonl header); Phase 1.2.c removed the 1 newly-orphaned :Quelle from Phase 1.1 collateral."
}
```
