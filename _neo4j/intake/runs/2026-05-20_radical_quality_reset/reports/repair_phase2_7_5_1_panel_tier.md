# Repair Agent E — Phase 2.7 panel + Phase 5.1 tier residuals

- **Agent:** Repair Agent E (2026-05-21)
- **Database:** `mit-bestand` on `bolt://localhost:7687` (creds: `E:\recherche\.cursor\mcp.json`)
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Inputs reviewed:**
  - `reports/final_verify_phase2_4_7.md` (Final Verifier 6/12)
  - `reports/final_verify_phase5_acceptance.md` (Final Verifier 12/12)
  - `migrations/mig_2_7_panel_cleanup.cypher`
  - `migrations/mig_5_1_quality_tier.cypher`
  - `migrations/mig_5_3_relabel_programme.cypher`
- **Migration created:** `migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher`
- **Runner:** `logs/repair_2_7_5_1_runner.py`
- **Verifier:** `logs/repair_2_7_5_1_verify.py`

## 0. Executive verdict

**STATUS: PASS** (graph_changed = true).

Two residuals reviewed; one repaired in graph, the other documented as a plan-narrative-only discrepancy (no graph change):

1. **Phase 2.7 panel residual (Projekt distinct keys > 25, per-node > 18) — REPAIRED.**
   9 Phase-5.1 audit scalars (`quality_tier_*` excluding `quality_tier` itself) were folded into a single JSON-string property `quality_tier_facts` on every `:Projekt`. The fold is value-preserving and reversible. After the repair:
   - Projekt distinct keys: **30 → 22** (target ≤ 25 ✓)
   - Max per-node keys: **26 → 18** (target ≤ 18 ✓)
   - Sampled 5 Projekt per-node keys: **21–23 → 13–15** (target ≤ 18 ✓)
   - `quality_tier` itself stays directly visible on every node.
2. **Phase 5.1 `p_circle_house` tier residual — DOCUMENTED, NO GRAPH CHANGE.**
   `p_circle_house` remains `:Projekt` with `quality_tier='tier_2_documentation_only'`. This is formula-consistent with plan §5.1 and Final Verifier 12 confirmed it. The task statement here explicitly says *"Do not degrade quality_tier semantics just to satisfy a narrative mismatch unless the plan explicitly requires an override"*. The plan does not write such an override into `mig_5_3_relabel_programme.cypher`. See §3 below for the decision rationale.

## 1. Residual #1 — Projekt panel keys (REPAIRED)

### 1.1 Diagnosis (live before-snapshot)

Live state on 2026-05-21 07:16 UTC, before repair (see `logs/repair_2_7_5_1_runner_before.json`):

```text
:Projekt total:                          101
distinct keys on :Projekt:                30   (target ≤ 25)
max keys on a :Projekt node:              26   (p_crclr_house_impact_hub_berlin; target ≤ 18)
:Projekt with quality_tier_facts:          0
```

The 9 Phase-5.1 audit scalars present on **every** 101 of 101 :Projekt nodes:

| key | type | semantic |
|---|---|---|
| `quality_tier_computed_by`        | STRING  | provenance — name of the migration |
| `quality_tier_has_components`     | BOOL    | sub-criterion: `count(DISTINCT HAT_BAUTEILGRUPPE) >= 3` |
| `quality_tier_has_evidence`       | BOOL    | sub-criterion: `>=3 BELEGT_IN edges with curated evidence` |
| `quality_tier_has_land`           | BOOL    | sub-criterion: `LIEGT_IN_LAND edge present` |
| `quality_tier_has_metric`         | BOOL    | sub-criterion: any of menge / reuse_share_facts / co2_facts |
| `quality_tier_has_year`           | BOOL    | sub-criterion: `year_completed IS NOT NULL` |
| `quality_tier_n_bg`               | INT     | input count: distinct HAT_BAUTEILGRUPPE |
| `quality_tier_n_bg_quantified`    | INT     | input count: BG with non-null quantity |
| `quality_tier_n_curated_evidence` | INT     | input count: BELEGT_IN curated rows |

(`quality_tier` itself — the assigned tier string — is **not** folded; it stays as a top-level panel-visible key per plan §5.1.)

### 1.2 Fold migration

`migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher` runs a single idempotent statement:

```cypher
MATCH (p:Projekt)
WHERE p.quality_tier_computed_by IS NOT NULL
WITH p, apoc.convert.toJson({
        computed_by:        p.quality_tier_computed_by,
        has_components:     p.quality_tier_has_components,
        has_evidence:       p.quality_tier_has_evidence,
        has_land:           p.quality_tier_has_land,
        has_metric:         p.quality_tier_has_metric,
        has_year:           p.quality_tier_has_year,
        n_bg:               p.quality_tier_n_bg,
        n_bg_quantified:    p.quality_tier_n_bg_quantified,
        n_curated_evidence: p.quality_tier_n_curated_evidence,
        repaired_by:        'mig_repair_2_7_5_1_quality_tier_panel',
        repaired_at:        '2026-05-21'
}) AS facts_json
SET p.quality_tier_facts = facts_json
REMOVE p.quality_tier_computed_by,
       p.quality_tier_has_components,
       p.quality_tier_has_evidence,
       p.quality_tier_has_land,
       p.quality_tier_has_metric,
       p.quality_tier_has_year,
       p.quality_tier_n_bg,
       p.quality_tier_n_bg_quantified,
       p.quality_tier_n_curated_evidence;
```

Properties:

- Value-preserving: every scalar value is encoded verbatim inside the JSON object (the cypher driver returns it as a `STRING`, exactly the same shape as `_archive`).
- Idempotent: the `WHERE p.quality_tier_computed_by IS NOT NULL` guard makes a re-run a no-op.
- Reversible: the JSON object is round-trippable with `apoc.convert.fromJsonMap` (cypher snippet in the migration header).

### 1.3 Effect on the live graph (after-snapshot)

After-snapshot (`logs/repair_2_7_5_1_runner_after.json`, `logs/repair_2_7_5_1_verify.json`):

| metric | before | after | target | status |
|---|---:|---:|---:|---|
| `:Projekt` total                                         | 101 | 101 | -    | unchanged |
| `:Projekt` distinct property keys                        | 30  | 22  | ≤ 25 | PASS |
| `:Projekt` max per-node key count                        | 26  | 18  | ≤ 18 | PASS |
| `:Projekt` sample 5 per-node key counts                  | 21,21,21,22,23 | 13,13,13,14,15 | ≤ 18 | PASS |
| `:Projekt` carrying `quality_tier_facts`                 | 0   | 101 | 101  | PASS |
| `:Projekt` carrying any of the 9 legacy scalars          | 101 | 0   | 0    | PASS |
| `:Projekt` carrying `quality_tier`                       | 101 | 101 | 101  | PASS |
| Tier distribution (1 / 2 / 3)                            | 11 / 68 / 22 | 11 / 68 / 22 | 11 / 68 / 22 | PASS |
| Acceptance Q3 rows                                       | 4   | 4   | ≥ 1  | PASS |
| Acceptance Q6 origin categories                          | derived 3205, curated 2939, inferred 342 | derived 3205, curated 2939, inferred 342 | non-zero × 3 | PASS |
| `:Bauteilgruppe` distinct property keys                  | 25  | 25  | ≤ 30 | PASS |

The 5 nodes that now sit at the 17–18-key ceiling all carry the union of canonical panel keys (`id`, `name`, `name_full`, `_archive`, `quality_tier`, `quality_tier_facts`, `source_scope`, `node_role`, `year_completed`, `raw_year_fields`, `area_m2_*`, `bewertung`, `projektstatus_text`, `nutzung_text`, `project_category`, `cost_facts`, `reuse_share_facts`, `co2_facts`) plus 1–2 of the actor-registry seed flags (`actor_registry_loader_seen`, `actor_registry_mentioned`). The post-repair 22 distinct keys on `:Projekt` are:

```text
_archive
actor_registry_loader_seen
actor_registry_mentioned
area_m2_gross
area_m2_range_max
area_m2_range_min
bewertung
co2_facts
cost_facts
id
name
name_full
node_role
nutzung_text
project_category
projektstatus_text
quality_tier
quality_tier_facts
raw_year_fields
reuse_share_facts
source_scope
year_completed
```

This matches the plan §2.7 panel (18 enumerated keys) plus 3 actor-registry seed flags carried in by Phase 4b.3 (`actor_registry_loader_seen`, `actor_registry_mentioned`, `project_category`) and the new fold key `quality_tier_facts`. The 3 actor-registry flags are documented in `agent_12_phase5_report.md` and are an additive Phase 4b residual rather than a Phase 2.7 regression.

### 1.4 Phase 5.1 semantic preservation

The fold preserves every Phase 5.1 derivation input verbatim. Example for one Tier 1 node (`p_k118_kopfbau_halle_118_winterthur`) and one Tier 2 node (`p_circle_house`), reconstructed from `quality_tier_facts`:

```text
p_k118 / has_year=true, has_land=true, has_components=true,
         has_metric=true, has_evidence=true
         (matches tier_1_decision_grade per §5.1 formula)

p_circle_house / has_year=false, has_land=true,
                 has_components=false, has_metric=true,
                 has_evidence=false
                 (matches tier_2_documentation_only per §5.1 formula)
```

`quality_tier` itself is unchanged on every node (read from the runner before/after snapshots), and the tier distribution `tier_1=11, tier_2=68, tier_3=22` is identical to the Final Verifier 12 reading.

## 2. Residual #2 — `p_circle_house` Tier 2 vs narrative Tier 3 (NO GRAPH CHANGE)

### 2.1 Live state

```text
id:            p_circle_house
labels:        [:Projekt]
quality_tier:  tier_2_documentation_only
has_year:      false
has_land:      true
has_components: false
has_metric:    true   (driven by reuse_share_facts / co2_facts presence)
has_evidence:  false
truthy count:  2 of 5
```

### 2.2 Plan reading

The plan has two statements about `p_circle_house`:

- §5.1 — *executable* formula: tier_2 iff `2 ≤ truthy_count < 5`; tier_3 iff `truthy_count ≤ 1`. With truthy_count=2, the formula deterministically returns `tier_2_documentation_only`.
- §5.3 — *narrative*: "Kept as `:Projekt` with `quality_tier='tier_3_stub'`". This sentence describes an *expectation* for p_circle_house's classification, but `mig_5_3_relabel_programme.cypher` does not implement it — the migration only relabels the 4 other ids; it never overrides any tier.

Final Verifier 12 already classified this as a **plan-narrative discrepancy** (plan §5.3 expectation vs plan §5.1 executable formula), not an implementation defect.

### 2.3 Decision: keep Tier 2

The repair task explicitly says:

> Do not degrade quality_tier semantics just to satisfy a narrative mismatch unless the plan explicitly requires an override.

Forcing `p_circle_house.quality_tier='tier_3_stub'` would:

1. Be inconsistent with the §5.1 formula that produced every other tier value on the graph (every other Projekt's tier is the deterministic output of the same formula; overriding one node would create a single special case with no formula provenance).
2. Erase the live signal that the node has 2 of 5 sub-criteria (it has a Land and a metric — a genuine Tier 2 signal — even though it has no curated evidence and no components).
3. Require either editing `mig_5_3_relabel_programme.cypher` after the fact (rewriting history) or adding a new override migration with no plan-instruction backing.

The plan §5.3 narrative is therefore better fixed in documentation than in graph state. `quality_tier_facts` now carries the full sub-criterion bag for `p_circle_house` (`has_year=false, has_land=true, has_components=false, has_metric=true, has_evidence=false`), so anyone reading the project sees both the tier and the audit trail in one panel-visible JSON object.

If a future plan rev wants Tier 3 for this id, the correct path is:

```cypher
MATCH (p:Projekt {id:'p_circle_house'})
SET p.quality_tier = 'tier_3_stub',
    p.quality_tier_override = 'plan_5_3_narrative_override';
```

…in a new migration with explicit plan citation. This repair does not preempt that.

## 3. Acceptance queries — re-check after the repair

| Q | live result after repair | verdict |
|---|---|---|
| Q3 | `MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) UNWIND p.reuse_share_facts AS rs RETURN count(*)` = **4** rows | PASS (unchanged) |
| Q6 | aggregate: derived=3205, curated=2939, inferred=342 | PASS (unchanged) |

(Q1, Q2, Q4, Q5, Q7 are not affected by this repair as they do not read any `quality_tier_*` key other than `quality_tier` itself.)

## 4. Files written by this repair

```text
migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher
logs/repair_2_7_5_1_probe.py
logs/repair_2_7_5_1_probe.json
logs/repair_2_7_5_1_runner.py
logs/repair_2_7_5_1_runner.log
logs/repair_2_7_5_1_runner_before.json
logs/repair_2_7_5_1_runner_after.json
logs/repair_2_7_5_1_verify.py
logs/repair_2_7_5_1_verify.json
reports/repair_phase2_7_5_1_panel_tier.md   (this file)
PHASE_2_7_5_1_REPAIR_DONE.flag
```

## 5. Risks

| risk | likelihood | impact | mitigation |
|---|---|---|---|
| Future code reads the 9 removed scalars by their old names | low | low | replaced by `quality_tier_facts` JSON; reversal cypher shown in migration header; `_archive` JSON pattern already established |
| Re-running `mig_5_1_quality_tier.cypher` resurrects the 9 scalars | medium | low | this repair migration is idempotent and can simply be re-run; re-run is a no-op once applied |
| Consumers expect `quality_tier_facts` as a Cypher map, not a JSON string | low | low | matches the `_archive` precedent on the same label; decode with `apoc.convert.fromJsonMap(p.quality_tier_facts)`; documented in migration header |
| Tier 2/3 narrative mismatch for `p_circle_house` confuses readers | low | low | documented in §2 above and inside `quality_tier_facts` per-node |

## 6. JSON return (summary)

```json
{
  "status": "PASS",
  "graph_changed": true,
  "before": {
    "projekt_distinct_keys": 30,
    "max_per_node_keys": 26,
    "sample_5_per_node_keys": [21, 21, 21, 22, 23],
    "quality_tier_facts_present": 0,
    "tier_distribution": {"tier_1_decision_grade": 11, "tier_2_documentation_only": 68, "tier_3_stub": 22}
  },
  "after": {
    "projekt_distinct_keys": 22,
    "max_per_node_keys": 18,
    "sample_5_per_node_keys": [14, 13, 13, 15, 13],
    "quality_tier_facts_present": 101,
    "legacy_scalars_present_total": 0,
    "tier_distribution": {"tier_1_decision_grade": 11, "tier_2_documentation_only": 68, "tier_3_stub": 22}
  },
  "p_circle_house": {
    "decision": "KEEP_TIER_2",
    "rationale": "plan §5.1 formula is deterministic; plan §5.3 narrative is a documentation expectation, not an override; full sub-criterion bag is preserved inside quality_tier_facts",
    "labels": ["Projekt"],
    "quality_tier": "tier_2_documentation_only",
    "truthy_count": 2,
    "sub_criteria": {
      "has_year": false,
      "has_land": true,
      "has_components": false,
      "has_metric": true,
      "has_evidence": false
    }
  },
  "acceptance_queries_after_repair": {
    "Q3": {"rows": 4, "verdict": "PASS"},
    "Q6": {"origins": ["derived", "curated", "inferred"], "verdict": "PASS"}
  },
  "files_written": [
    "migrations/mig_repair_2_7_5_1_quality_tier_panel.cypher",
    "logs/repair_2_7_5_1_probe.py",
    "logs/repair_2_7_5_1_probe.json",
    "logs/repair_2_7_5_1_runner.py",
    "logs/repair_2_7_5_1_runner.log",
    "logs/repair_2_7_5_1_runner_before.json",
    "logs/repair_2_7_5_1_runner_after.json",
    "logs/repair_2_7_5_1_verify.py",
    "logs/repair_2_7_5_1_verify.json",
    "reports/repair_phase2_7_5_1_panel_tier.md",
    "PHASE_2_7_5_1_REPAIR_DONE.flag"
  ],
  "risks": [
    "future code reading old 9 scalars (mitigated: quality_tier_facts JSON; reversal documented)",
    "re-running mig_5_1 resurrects the 9 scalars (mitigated: repair migration is idempotent; just re-run)",
    "downstream consumers expecting a Cypher map (mitigated: same precedent as _archive STRING; decode helper documented)",
    "p_circle_house tier-2-vs-narrative-3 confusion (mitigated: documented above and inside quality_tier_facts)"
  ]
}
```
