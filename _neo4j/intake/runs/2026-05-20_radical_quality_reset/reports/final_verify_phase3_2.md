# Final Verify Phase 3.2 — Pollutant Inference

Verifier: Final Verifier 8 of 12  
Date: 2026-05-21  
Database: `mit-bestand`  
Run directory: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`

## Verdict

PASS — Phase 3.2 pollutant inference is confirmed.

## Artifact Checks

| Check | Expected | Observed | Status |
|---|---:|---:|---|
| `migrations/mig_3_2_pollutant_inference.cypher` exists | present | present | PASS |
| `PHASE_3_2_DONE.flag` exists | present | present | PASS |

## Live Graph Checks

| Query / Check | Expected | Observed | Status |
|---|---:|---:|---|
| `MATCH ()-[r:HAT_SCHADSTOFF]->() RETURN count(r)` | 0 | 0 | PASS |
| `MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r)` | >= 700, target ~803 | 803 | PASS |
| `MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r)` | >= 250, target ~347 | 347 | PASS |

## `HAS_RISK_POLLUTANT` Distribution By Basis

| `evidence_basis` | Count | Status |
|---|---:|---|
| `documented` | 11 | PASS |
| `era_and_material` | 4 | PASS |
| `material_only` | 788 | PASS |

Distribution matches the expected shape: documented edges are present, at least one era-and-material inference exists, and the bulk of inferred edges are material-only.

## Sample Shape Checks

Sampled 3 `HAS_RISK_POLLUTANT` edges:

| Sample | `evidence_origin` | `evidence_basis` | `evidence_source_id` | `evidence_confidence` | Status |
|---:|---|---|---|---|---|
| 1 | `curated` | `documented` | `q_schadstoff_reuse_knowledge_graph_research_md` | `belegt` | PASS |
| 2 | `inferred` | `material_only` | `q_schadstoff_reuse_knowledge_graph_research_md` | `inferiert` | PASS |
| 3 | `inferred` | `material_only` | `q_schadstoff_reuse_knowledge_graph_research_md` | `inferiert` | PASS |

Sampled 3 `REQUIRES_VERIFICATION_FOR` edges:

| Sample | `evidence_origin` | `evidence_basis` | `pollutant_basis` | `evidence_source_id` | `evidence_confidence` | Status |
|---:|---|---|---|---|---|---|
| 1 | `inferred` | `project_rollup` | `material_only` | `q_schadstoff_reuse_knowledge_graph_research_md` | `inferiert` | PASS |
| 2 | `inferred` | `project_rollup` | `material_only` | `q_schadstoff_reuse_knowledge_graph_research_md` | `inferiert` | PASS |
| 3 | `inferred` | `project_rollup` | `material_only` | `q_schadstoff_reuse_knowledge_graph_research_md` | `inferiert` | PASS |

All sampled edges have `evidence_origin` in `{curated, inferred}`, non-null `evidence_source_id`, and accepted `evidence_confidence` values.

## JSON Return

```json
{
  "verifier": "final_verifier_8_of_12",
  "phase": "3.2",
  "phase_name": "pollutant_inference",
  "database": "mit-bestand",
  "status": "pass",
  "checks": {
    "migration_exists": true,
    "phase_flag_present": true,
    "hat_schadstoff_count": 0,
    "has_risk_pollutant_count": 803,
    "has_risk_pollutant_minimum_met": true,
    "has_risk_pollutant_by_basis": {
      "documented": 11,
      "era_and_material": 4,
      "material_only": 788
    },
    "requires_verification_for_count": 347,
    "requires_verification_for_minimum_met": true,
    "has_risk_pollutant_sample_shape_ok": true,
    "requires_verification_for_sample_shape_ok": true
  }
}
```
