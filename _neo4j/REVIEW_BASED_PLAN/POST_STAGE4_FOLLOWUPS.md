# Post-Stage-4 follow-ups

> Migrations and decisions the remediation defers to a future round. **Do not run any of these until Stage 4 PASSes** — they all depend on Stage 4's honest counts as input.

---

## §1 — FU-1 — Tier-1 honest recompute

### Why

The current `:Projekt.quality_tier='tier_1_decision_grade'` cohort is 11 projects, but the gating Cypher (in [mig_5_1_quality_tier.cypher](../intake/runs/2026-05-20_radical_quality_reset/migrations/mig_5_1_quality_tier.cypher)) treats Repair D's auto-promoted edges as `curated`. After R1's reclassification to `source_curated` / `topology_synthesized`, the honest gate counts only `source_curated` evidence. The tier-1 cohort is expected to drop to 3–5 projects.

This is the **headline success metric** of the whole remediation.

### Migration

```cypher
// mig_fu1_tier1_honest_recompute.cypher
//
// Recompute :Projekt.quality_tier using R1's source_curated-only gate.
// Save the legacy tier in .quality_tier_pre_fu1 for forensic comparison.
// Update .quality_tier_facts (the JSON-string fold from Phase 5.1) to
// reflect the new sub-counts.

MATCH (p:Projekt)
OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WITH p,
     count(DISTINCT bg) AS n_bg,
     sum(CASE WHEN bg.menge_t      IS NOT NULL
                OR bg.menge_stueck IS NOT NULL
                OR bg.menge_m2     IS NOT NULL
                OR bg.menge_kg     IS NOT NULL
                OR bg.menge_m      IS NOT NULL
              THEN 1 ELSE 0 END) AS n_bg_quantified
OPTIONAL MATCH (p)-[bel:BELEGT_IN]->()
WITH p, n_bg, n_bg_quantified,
     // HONEST gate: source_curated ONLY (drops Repair D promotions and registry fills)
     sum(CASE WHEN bel.evidence_origin = 'source_curated'
                AND bel.evidence_excerpt IS NOT NULL
                AND bel.evidence_confidence IN ['belegt','teilweise_belegt']
              THEN 1 ELSE 0 END) AS n_source_curated_evidence
// Optionally also count :HAT_KENNWERT (R4) as quantification — a Kennwert
// IS evidence of quantification when the edge is source_curated.
OPTIONAL MATCH (p)-[kw_edge:HAT_KENNWERT]->()
WITH p, n_bg, n_bg_quantified, n_source_curated_evidence,
     sum(CASE WHEN kw_edge.evidence_origin = 'source_curated' THEN 1 ELSE 0 END) AS n_kennwert_curated
WITH p, n_bg, n_bg_quantified, n_source_curated_evidence, n_kennwert_curated,
     (p.year_completed IS NOT NULL) AS has_year,
     exists{(p)-[:LIEGT_IN_LAND]->()} AS has_land,
     (n_bg >= 3) AS has_components,
     (n_bg_quantified >= 1
          OR n_kennwert_curated >= 1
          OR size(coalesce(p.reuse_share_facts, [])) >= 1
          OR size(coalesce(p.co2_facts, [])) >= 1) AS has_metric,
     (n_source_curated_evidence >= 3) AS has_evidence
SET p.quality_tier_pre_fu1 = coalesce(p.quality_tier_pre_fu1, p.quality_tier),
    p.quality_tier = CASE
        WHEN has_year AND has_land AND has_components AND has_metric AND has_evidence
            THEN 'tier_1_decision_grade'
        WHEN (toInteger(has_year)
              + toInteger(has_land)
              + toInteger(has_components)
              + toInteger(has_metric)
              + toInteger(has_evidence)) >= 2
            THEN 'tier_2_documentation_only'
        ELSE 'tier_3_stub'
    END,
    p.quality_tier_n_source_curated_evidence = n_source_curated_evidence,
    p.quality_tier_n_kennwert_curated = n_kennwert_curated,
    p.quality_tier_recomputed_by = 'mig_fu1_tier1_honest_recompute',
    p.quality_tier_recomputed_at = date();

// Distribution after recompute
MATCH (p:Projekt) RETURN p.quality_tier AS tier, count(p) AS c ORDER BY tier;

// Projects that dropped tier
MATCH (p:Projekt)
WHERE p.quality_tier_pre_fu1 = 'tier_1_decision_grade'
  AND p.quality_tier <> 'tier_1_decision_grade'
RETURN p.id AS demoted, p.quality_tier_pre_fu1 AS was, p.quality_tier AS now;
```

### Acceptance

| Gate | Expected |
|---|---|
| `:Projekt.quality_tier_pre_fu1` set on all 101 | yes |
| New tier-1 cohort ≤ legacy tier-1 cohort | yes (expected: ≤ 5) |
| Audit lists demoted projects | non-empty |

### Run after

Stage 4 PASS (so the demotion is visible in `FINAL_REVIEW_PLAN_AUDIT.md`'s "Decision-grade cohort" section).

---

## §2 — FU-2 — Close 6 remaining orphan dossiers

### Why

Agent 5 R7.b's brief called for 7 orphan dossiers to be resolved with new `:Projekt` / `:Programm` nodes. Only 1 (`p_eth_circular_construction_programme`) was created. The remaining 6 are still orphans:

- `q_circl_pavilion_amsterdam_md` → expected `:Projekt p_circl_pavilion_amsterdam`
- `q_re_use_hoefe_wien_md` → expected `:Projekt p_re_use_hoefe_wien`
- `q_berlin_schildow_pilot_house_2_md` → expected `:Projekt p_berlin_schildow_pilot_house_2` (sibling of `p_berlin_schildow_pilot_house`)
- `q_fcrbe_facilitating_circulation_reclaimed_building_elements_md` → expected `:Programm`
- `q_rebridge_structural_reuse_md` → expected `:Programm`
- `q_refair_bordeaux_md` → expected `:Programm` (per D8 default)

### Investigation first

Before recreating, check whether each orphan dossier already has a `:Projekt` with a different id:

```cypher
// For each orphan, look for a Projekt whose name or slug roughly matches
UNWIND [
  'circl_pavilion_amsterdam',
  're_use_hoefe_wien',
  'berlin_schildow_pilot_house_2',
  'fcrbe',
  'rebridge',
  'refair'
] AS slug
MATCH (p:Projekt)
WHERE toLower(p.id) CONTAINS slug
   OR toLower(coalesce(p.name, '')) CONTAINS replace(slug, '_', ' ')
RETURN slug, p.id, p.name;
```

Only create new nodes for orphans that genuinely don't exist.

### Migration

Use the same pattern as Agent 5's [R7.b](AGENT_5_loader_hardening.md#62-r7b--create-the-7-orphan-node-targets) but scoped to the 6 still-missing slugs. Reuse the Cypher block from `AGENT_5_loader_hardening.md §6.2`.

### Acceptance

| Gate | Expected |
|---|---|
| `case_markdown :Quelle` without matching `:Projekt`/`:Programm` BELEGT_IN | 0 |
| 6 new nodes created (or fewer if some matched existing) | yes |
| Each new node has `needs_dossier_extraction=true` | yes |

### Run after

R3 (so that any new `:Projekt` is picked up by R3's `:HAS_BAUWERK` derivation — though new orphan projects have no BG paths yet, this is forward-compat).

---

## §3 — FU-3 — R7.c.v2 — Section-8 re-extraction for R8-flagged projects

### Why

R7.c was deferred (OD-2). Agent 1's R8 seed pass creates `:DataIssue {kind:'dossier_section8_missing'}` for every `:Projekt` that has a `case_markdown` Quelle but no `:Kennwert`. Those are the candidates for re-extraction.

### Migration approach

Driver-side Python script:

1. `MATCH (i:DataIssue {kind:'dossier_section8_missing'})-[:CONCERNS]->(p:Projekt)` → get the project list.
2. For each, find its `case_markdown` Quelle (now carries `.text_content` from R7.d).
3. Run the Section-8 regex extractor (number + unit patterns) on `q.text_content`.
4. For each match, MERGE a `:Kennwert` + `:HAT_KENNWERT` using Agent 4's R4 schema.
5. Mark the `:DataIssue` as `status='resolved'` if any `:Kennwert` was emitted.

### Acceptance

| Gate | Expected |
|---|---|
| `:DataIssue {kind:'dossier_section8_missing', status:'open'}` count | drops to 0 or near-0 |
| New `:Kennwert {migration_origin:'mig_fu3_section8_v2'}` count | ≥ 1 per resolved project |
| No duplicate `:Kennwert` (idempotent on re-run) | yes |

### Run after

R8 (so the `:DataIssue` set is populated).

---

## §4 — FU-4 — Strip `*_facts` JSON-string property mirrors (D2)

### Why

After R4 lifted the JSON-string facts into `:Kennwert` nodes, the original `:Projekt.reuse_share_facts`, `.co2_facts`, `.cost_facts` properties remain as a deprecated mirror (per D2: defer the strip until one ingestion cycle confirms the node form is loader-ready).

### When this becomes safe

- All existing dossier loaders have been updated to write `:Kennwert` (not JSON-string lists).
- The drift validator (R7.d) catches any retired-property reference in new dossiers.
- One new batch import has succeeded against the new model.

### Migration

```cypher
// mig_fu4_strip_facts_mirrors.cypher
//
// Strip Projekt.{reuse_share_facts, co2_facts, cost_facts} once :Kennwert is
// loader-ready. Each strip is journalled to deleted/fu4_<projekt>_<facts>.jsonl
// for reversibility.

// Driver-side: journal first, then strip.

MATCH (p:Projekt)
WHERE p.reuse_share_facts IS NOT NULL
   OR p.co2_facts IS NOT NULL
   OR p.cost_facts IS NOT NULL
REMOVE p.reuse_share_facts, p.co2_facts, p.cost_facts;
```

### Acceptance

| Gate | Expected |
|---|---|
| `:Projekt` with `reuse_share_facts` | 0 |
| `:Projekt` with `co2_facts` | 0 |
| `:Projekt` with `cost_facts` | 0 |
| `:Kennwert` total | unchanged (≥ 258) |

### Run after

At least one new ingestion cycle confirms `:Kennwert` is the canonical write path.

---

## §5 — FU-5 — R6 schema language unification (deferred D7)

### Why

The schema is half-Anglicized. New types (`FROM_DONOR`, `INTO_RECEIVER`, `HAS_RISK_POLLUTANT`, `BUILT_IN_ERA`, `ReuseRule`, `:HAS_BAUWERK`, `:RELEVANT_FOR`, `:STUB_PROJECT_LINK`, `:DataIssue`, `:DeprecatedType`, `:Kennwert`, `:LCAModule`, `:Zertifizierungssystem`) are English. Legacy types (`HAT_BAUTEILGRUPPE`, `BETEILIGT_AN`, `LIEGT_IN_LAND`, `:Bauwerk`, `:Bauteilgruppe`, `:Akteur`, `:Projekt`, `:Quelle`, `:Norm`, `:Schadstoff`, `:Land`, `:Stadt`) are German.

### Choice

D7 default: **Direction A (all English)**. Aligns with the international research literature.

### Migration

Big single migration using `apoc.refactor.rename.type` and `apoc.refactor.rename.label` for every German type/label. Property names also Anglicised.

Effort: Extra Large. Touches every query in every existing script. Requires updating all dossier loaders, all helper scripts, all documentation.

### Acceptance

| Gate | Expected |
|---|---|
| Every label in English | yes |
| Every rel type in English | yes |
| Every property name in English | yes |
| Acceptance Q1–Q7 (new form) PASS | yes |
| Dossier loaders updated to translate dossier-German → schema-English | yes |

### Risk mitigation

This is a one-shot rename. Once committed, it's hard to revert without re-running everything. Recommend a separate branch with full audit before merging. Pause one full week between R6 author and R6 merge to give downstream users time to react.

### Run after

Stage 4 PASS + post-Stage-4 cleanup (FU-1, FU-4) complete + at least one new dossier ingestion succeeds.

---

## §6 — FU-6 — Drift validator as a pre-flight gate

### Why

R7.d's drift validator detected 59 dossier-vs-schema drift issues (dossier text still uses retired type names like `LebenszyklusModul`, `ZertifizierungBewertungssystem`, `EINGEBAUT_IN`). Currently these are recorded as `:DataIssue` after ingestion. Better: block the ingestion if drift exists.

### Action

Make `_scripts/validate_dossier_schema.py` a hard pre-flight gate. Update `_neo4j/intake/README.md` to require its successful exit before any loader runs.

Add the script as the first step in the next ingestion run.

### Acceptance

| Gate | Expected |
|---|---|
| Pre-flight returns exit 0 on all dossiers in the next inbox batch | yes |
| Any new drift finding blocks ingestion | yes |
| `:DataIssue {kind:'dossier_uses_retired_type', status:'open'}` count | trends to 0 over batches |

### Run after

Stage 4 PASS + dossier authors notified of the new gate.

---

## §7 — Dependency between follow-ups

```
                Stage 4 PASS
                     │
            ┌────────┼────────┐
            ▼        ▼        ▼
          FU-1     FU-2     FU-3  ◄── needs R8 done (already prerequisite for Stage 4)
                                   │
                                   ▼
                                  FU-4
                                   │
                                   ▼
                                  FU-5 (R6)
                                   │
                                   ▼
                                  FU-6
```

FU-1, FU-2, FU-3 are independent and can run in parallel. FU-4 follows them. FU-5 is the heaviest and should be last.

---

## §8 — Tracking

After Stage 4, each follow-up should:

1. Get its own short brief in this directory (e.g., `FU_1_TIER1_RECOMPUTE.md`).
2. Be assigned to a single agent (or the orchestrator).
3. Have its own done flag (`PHASE_FU_1_DONE.flag`, etc.).
4. Update [STATUS.md](STATUS.md)'s "Known open follow-ups" table.

`:DataIssue {kind:'open_followup'}` nodes can also track them at the graph level if desired.

---

**End of POST_STAGE4_FOLLOWUPS.md.**
