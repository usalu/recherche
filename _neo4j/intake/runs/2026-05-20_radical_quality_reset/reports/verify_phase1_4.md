# Verification Phase 1.4 — Materialdepot Relabel

Verifier: 4 of 12  
Mode: read-only Neo4j verification  
Run directory: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`

## Result

PASS — Phase 1.4 Materialdepot relabel is complete and consistent with the plan.

## Evidence

| Check | Expected | Observed | Status |
|---|---:|---:|---|
| `migrations\mig_1_4_materialdepot.cypher` exists | yes | yes | PASS |
| `PHASE_1_4_DONE.flag` exists | yes | yes, run root | PASS |
| `MATCH (m:Materialdepot) RETURN count(m)` | 23 | 23 | PASS |
| `MATCH (m:Materialdepot) WHERE m:Bauwerk RETURN count(m)` | 0 | 0 | PASS |
| `MATCH (b:Bauwerk) RETURN count(b)` | 186 | 186 | PASS |
| `MATCH (m:Materialdepot) WHERE m.is_material_depot=true RETURN count(m)` | 23 | 23 | PASS |
| `BETRIEBEN_VON` edges with `evidence_source_id='mig_1_4'` | >= 3 | 3 | PASS |

## Sampled Plan IDs

| ID | Labels | Degree | Status |
|---|---|---:|---|
| `bw_crclr_kindl_hall` | `Materialdepot` | 26 | PASS |
| `bw_chiro_itterbeek_reuse_supply_network` | `Materialdepot` | 21 | PASS |
| `bw_rotor_reuse_stock_charles_malis` | `Materialdepot` | 11 | PASS |

All three sampled IDs have the `:Materialdepot` label and preserved edge degree >= 4.

## JSON

```json
{
  "phase": "1.4",
  "verifier": "4 of 12",
  "status": "PASS",
  "read_only": true,
  "migration_exists": true,
  "done_flag_exists": true,
  "done_flag_location": "run_root",
  "checks": {
    "materialdepot_count": {
      "query": "MATCH (m:Materialdepot) RETURN count(m)",
      "expected": 23,
      "observed": 23,
      "pass": true
    },
    "materialdepot_with_bauwerk_label_count": {
      "query": "MATCH (m:Materialdepot) WHERE m:Bauwerk RETURN count(m)",
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "bauwerk_count": {
      "query": "MATCH (b:Bauwerk) RETURN count(b)",
      "expected": 186,
      "observed": 186,
      "pass": true
    },
    "materialdepot_is_material_depot_true_count": {
      "query": "MATCH (m:Materialdepot) WHERE m.is_material_depot=true RETURN count(m)",
      "expected": 23,
      "observed": 23,
      "pass": true
    },
    "betrieben_von_mig_1_4_count": {
      "query": "MATCH (m:Materialdepot)-[r:BETRIEBEN_VON]->(a:Akteur) WHERE r.evidence_source_id='mig_1_4' RETURN count(r)",
      "expected_min": 3,
      "observed": 3,
      "pass": true
    }
  },
  "sample_ids": [
    {
      "id": "bw_crclr_kindl_hall",
      "labels": ["Materialdepot"],
      "degree": 26,
      "has_materialdepot_label": true,
      "degree_at_least_4": true,
      "pass": true
    },
    {
      "id": "bw_chiro_itterbeek_reuse_supply_network",
      "labels": ["Materialdepot"],
      "degree": 21,
      "has_materialdepot_label": true,
      "degree_at_least_4": true,
      "pass": true
    },
    {
      "id": "bw_rotor_reuse_stock_charles_malis",
      "labels": ["Materialdepot"],
      "degree": 11,
      "has_materialdepot_label": true,
      "degree_at_least_4": true,
      "pass": true
    }
  ]
}
```
