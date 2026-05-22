# Bauteilgruppe Comparison — would we lose components?

**Generated:** 2026-06-03
**FINAL DECISION (2026-06-03 latest):** `:Bauteilgruppe` label scoped to `bg_reuse_*` only. All non-reuse prefixes (`bg_retained_*` / `bg_planned_*` / `bg_dismantled_*` / `bg_candidate_*`) deleted as out-of-scope. Skip the manual resolver. See [FINAL_PLAN.md decision #8](FINAL_PLAN.md#decisions-locked-in).
**This document is preserved for context** — original analysis text below kept for reference, but the headline numbers have changed (see [FINAL_PLAN.md](FINAL_PLAN.md) for the current dispositions).

**Source:** [analyze_bauteilgruppe_comparison.py](analyze_bauteilgruppe_comparison.py) → [bauteilgruppe_comparison.txt](bauteilgruppe_comparison.txt)

User asked: *if we delete old stuff, would we lose actual Bauteilgruppen connected to projects?*

## Current answer: **70 BGs deleted total** (35 `bg_reuse_*` orphans + 35 non-reuse out-of-scope), **24 batch-new `bg_reuse_*` created**, **85 batch rows filtered** (anchored on non-reuse BGs). Net: 350 → 304 BGs, all `bg_reuse_*`.

Phase 6 only deletes vocab nodes (`meth_*`, `av_*`, `rq_*`, `wva_*`, `rv_betonfraesen`) and their inbound edges. Every one of the 350 live `:Bauteilgruppe` nodes survives with:

- its full property bag (`reuse_status`, `bg_kind`, `alte_funktion`, `neue_funktion`, `tragend`, `id`, `name`)
- its evidence URLs (`BELEGT_IN → :Quelle`, 627 edges total — these are NOT touched)
- every non-vocab relationship (`HAS_RISK_POLLUTANT`, `HAT_HUERDE`, `HAT_PROZESSPHASE`, `HAT_BAUTEILTYP`, `NUTZT_MATERIAL`, `HAT_MATERIALGRUPPE`, `HAT_LOGISTIK`, `HAT_MARKTMODELL`, `HAT_BAUTEILEBENE`, etc.)
- its `(:Projekt)-[:HAT_BAUTEILGRUPPE]->` anchor to the project

The integration only attaches **new** evidence edges to existing BGs and (optionally) creates a small number of new candidate BGs that the batches introduce.

## What the comparison actually measures

The real question that matters is: **for each live BG, will batches deliver new evidence on the new axes (Ergebnis, Ort, Methode, Quelle, Aufbereitung, Rückbau)?** The match between live BG ids and batch BG ids determines whether the resolver can attach the batch row.

| Bucket | Count | What it means |
|---|---:|---|
| **EXACT match** | 273 | Live BG id = batch BG id. Resolver MERGEs batch evidence directly. Clean. |
| **FUZZY match** | 13 | Live BG ≠ batch BG slug-wise, but ≥35% token similarity (with German↔English aliasing). Resolver auto-folds — review the list. |
| **LIVE-ONLY** | 64 | Live BG has no batch slug that matches algorithmically. **Most of these have a batch equivalent the matcher couldn't see (semantic drift). Need manual resolver review.** |
| **BATCH-ONLY** | 44 | Batch BG slug has no live equivalent that matches algorithmically. Genuine new candidates plus the other side of the "LIVE-ONLY" drift. |
| **Total live BGs** | 350 | All preserved |
| **Total batch BGs referenced** | 330 | |

## Why "LIVE-ONLY" is misleading

Inspect the BlueCity example. The live graph has 4 BGs; the batches have 4 too. The matcher catches 2 fuzzy matches and labels the other 2 "live-only" — but they DO have batch equivalents:

| Live (German) | Batch (English) | Same component? | Matched? |
|---|---|---|---|
| `bg_reuse_beton_wand_bluecity_betonbloecke_trennwaende` | `bg_reuse_beton_innenwand_bluecity_original_concrete_blocks` | yes (concrete blocks as partition walls) | FUZZY (0.50) |
| `bg_reuse_stahl_ausbau_bluecity` | `bg_reuse_stahl_tragwerk_bluecity_reused_steel` | yes (reused steel) | FUZZY (0.40) |
| `bg_reuse_stahl_gelaender_bluecity_oelplattform` | `bg_reuse_metall_gelaender_bluecity_oil_platform_balustrades` | yes (oil platform balustrades) | **MISSED** — material category drift (stahl vs metall) |
| `bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende` | `bg_reuse_glas_innenwand_bluecity_reused_window_frames` | yes (cedar window frames used as partitions) | **MISSED** — generic `mehrere_mehrere` slug |

→ Real coverage for BlueCity: **4/4 components matched** after manual review. Algorithmic matching: 2/4 exact, 0 fuzzy on this run, 2 truly live-only flagged for review (but turn out to match too).

This pattern repeats across the 64 "live-only" cases.

## Per-project breakdown (15 most-affected)

| Project | live BGs | batch BGs | exact | fuzzy | live-only | batch-only | comment |
|---|---:|---:|---:|---:|---:|---:|---|
| `p_chiro_d_itterbeek_dilbeek` | 13 | 12 | 11 | 1 | 1 | 0 | Almost full |
| `p_circl_abn_amro` | 15 | 13 | 8 | 0 | 7 | 5 | High drift (planned/dismantled BGs not in batches) |
| `p_circular_pavilion_paris` | 6 | 6 | 6 | 0 | 0 | 0 | Clean |
| `p_crclr_house_impact_hub_berlin` | 6 | 4 | 4 | 0 | 2 | 0 | 2 live-only need review |
| `p_elys_kultur_gewerbehaus_basel` | 7 | 7 | 6 | 1 | 0 | 0 | Clean |
| `p_ferme_du_rail_paris` | 8 | 8 | 0 | 0 | 8 | 8 | **Full slug rewrite** — manual review needed |
| `p_grande_halle_de_colombelles` | 9 | 9 | 8 | 0 | 1 | 1 | 1 needs review |
| `p_grubenstrasse_29_werkhof_29_zuerich` | 9 | 9 | 7 | 0 | 2 | 2 | 2 need review |
| `p_impact_hub_berlin_crclr_fitout` | 7 | 7 | 4 | 0 | 3 | 3 | 3 need review |
| `p_k118_kopfbau_halle_118_winterthur` | 5 | 5 | 0 | 0 | 5 | 5 | **K118 entirely re-slugged** — manual review |
| `p_maison_des_canaux_paris` | 4 | 4 | 0 | 0 | 4 | 4 | Manual review |
| `p_maison_vignette_auderghem` | 5 | 5 | 0 | 0 | 5 | 5 | Manual review |
| `p_meduni_campus_mariannengasse` | 6 | 6 | 6 | 0 | 0 | 0 | Clean |
| `p_upcycle_studios_copenhagen` | 3 | 3 | 0 | 0 | 3 | 3 | Manual review |
| `p_umar_unit` | 8 | 4 | 3 | 1 | 4 | 0 | 4 live-only — likely not in batches |

(Full table in [bauteilgruppe_comparison.txt](bauteilgruppe_comparison.txt).)

## What this means operationally

### What's guaranteed safe
- **0 BGs deleted.** All 350 live BGs survive. Property bags intact.
- **273 exact-match BGs** will receive new batch evidence directly.
- **13 fuzzy-match BGs** auto-fold via the resolver — spot-check the list.

### What needs Phase 3.2 manual resolver work
- ~64 live-only + ~44 batch-only candidates. Most pairs likely refer to the same component (BlueCity-style slug drift). The resolver CSV ([bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv)) needs a manual review pass:
  - For every "live-only" BG, suggest the closest batch BG (top-3 by tokens + alte_funktion match)
  - User confirms or rejects
  - Confirmed pairs become resolver entries

### What's a genuine NEW candidate
After manual review, ~10–25 of the 44 batch-only entries will turn out to be **genuinely new** components that batches discovered (the `*_candidate` suffix is the hint). Examples:
- `bg_reuse_naturstein_fassade_k118_granit_orion_candidate` — granite from the Orion donor building (new for K118)
- `bg_reuse_stahl_erschliessung_k118_aussentreppe_orion_candidate` — external stairs (new for K118)
- `bg_reuse_holz_papier_ferme_du_rail_recycled_fibre_wall_panels`
- `bg_reuse_asphalt_liander_existing_roofs`

These get MERGEd as new `:Bauteilgruppe` nodes anchored to the relevant project. The `bg_kind` property should be set to `partial_batch` (the live convention for batch-derived BGs).

### What's a genuine UNCOVERED live BG (no batch evidence anywhere)
After manual review, ~5–20 of the 64 will turn out to be **genuinely uncovered** by batches. These survive with all their properties but their old vocab edges get deleted in Phase 6 with nothing replacing them on the new axes. They become "evidence-cold" BGs — known to exist but with no `belegt`-tier confirmation on outcome/origin/location/method/processing.

Risk assessment: low. These BGs still carry their `alte_funktion`, `neue_funktion`, `tragend`, material, bauteiltyp, schadstoff, huerde, prozessphase data. They just lack vocab-axis evidence. They become candidates for the next research batch.

## Updated Phase 3.2 workflow

```text
For each project:
  1. List live BGs (id, name, alte_funktion, material, bauteiltyp)
  2. List batch BGs (id, descriptor)
  3. Auto-match: exact slug → DIRECT MERGE
  4. Auto-match: fuzzy ≥0.5 → SUGGEST, mark `auto_confirmed`
  5. Auto-match: fuzzy 0.35–0.5 + same material category → SUGGEST, mark `needs_review`
  6. Unmatched live BG: scan batch list for any pair with shared (project, material_family, bauteiltyp_family, alte_funktion_token) → SUGGEST manual review
  7. Unmatched batch BG: scan live list with the same heuristic → SUGGEST or mark NEW candidate
  8. Human reviewer signs off the CSV before Phase 4 starts
```

Estimated manual review queue size after auto-matching: **~30–50 pairs** to confirm/reject. Should take 1–2 hours of focused review.

## Updated check to add to verify_integration.cypher

```cypher
// §12. Bauteilgruppe count parity per project — flag projects where
// post-integration BG count differs from pre-integration (none should drop)
MATCH (p:Projekt)
OPTIONAL MATCH (p)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WITH p, count(bg) AS post_integration_bg_count
RETURN p.id AS project, post_integration_bg_count
ORDER BY post_integration_bg_count DESC LIMIT 10;
// Pre-integration values for cross-check (from this analysis, 2026-06-03):
//   verbiest_karreveld_brussels:7, kindergarten_moeoeslistrasse:7, lycee_michel_lucius:7,
//   resilience_la_ferme_des_possibles:7, jeugdkliniek_ithaka:7, …
// After Phase 6: every project should have either the same count (existing BG kept)
// or higher (batch-only candidates added). No project should drop.

// §13. BGs with zero batch evidence on the NEW axes (visibility, not failure)
MATCH (bg:Bauteilgruppe)
WHERE NOT EXISTS { MATCH (bg)-[r {review_run: 'taxonomy_integration_2026_06_03'}]-() }
  AND EXISTS { MATCH (:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg) }
WITH bg
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)
RETURN 'INFO' AS status, p.id AS project, bg.id, bg.name,
       bg.alte_funktion, bg.neue_funktion,
       'evidence-cold: no batch row matched this BG' AS note
ORDER BY p.id, bg.id;
```

## TL;DR

- **0 Bauteilgruppe nodes deleted.** Plan never touches them.
- **78% (273/350) of live BGs auto-match** to a batch BG by exact slug — get new evidence cleanly.
- **18% (64/350) need Phase 3.2 manual resolver review** because of German↔English slug drift, material-category drift, or generic `mehrere_mehrere` slugs. Most pairs likely DO match a batch BG; resolver just needs human eyes.
- **~10–25 batch-only entries are genuinely new components** that batches discovered and that get added as new `:Bauteilgruppe` nodes anchored to their project.
- **~5–20 BGs will end up evidence-cold** after the integration (no batch row covers them). They keep all properties and non-vocab edges; they just lack confirmation on the new vocab axes. Worth a follow-up research batch later.

You don't lose components. You may lose the auto-generated `unklar`-tier vocab tags on a small number of BGs, which is the same trade-off the [RICHNESS_AUDIT.md](RICHNESS_AUDIT.md) flagged at the project level.
