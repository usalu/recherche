# Quality Pass Q02 — Materialdepot placeholders (EP-09 / R01 residuals)

**Agent:** Q02 · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Inputs:** [`ledger/element_proof_agent_09.csv`](../ledger/element_proof_agent_09.csv) (EP09-n-0001…0017), [`ledger/remediation_r01.csv`](../ledger/remediation_r01.csv) (R01-N-002…022)
**Ledger:** [`ledger/quality_pass_q02.csv`](../ledger/quality_pass_q02.csv)
**Patch:** [`patches/quality_pass_q02_deprecate.patch.jsonl`](../patches/quality_pass_q02_deprecate.patch.jsonl)
**Apply report:** [`apply_reports/quality_pass_q02_deprecate.patch.apply_report.md`](../apply_reports/quality_pass_q02_deprecate.patch.apply_report.md)

## 1. Scope

17 unsourced `:Materialdepot` nodes remaining after R01 sourced 5 discrete depots. All 17 were `MISSING_EVIDENCE` / `ESCALATE_HUMAN` in EP-09 and R01 — aggregate labels, explicit *Unbekannt* placeholders, or network abstractions with no findable primary depot URL.

| Pre-pass | Post-pass |
|---|---:|
| 22 Materialdepot nodes (5 sourced / 17 unsourced) | **5 Materialdepot nodes (5/5 sourced)** |
| 2281 nodes / 15289 rels | **2264 nodes / 15171 rels** |

## 2. Verdict summary

| Proposed action | Count | Rationale |
|---|---:|---|
| **DEPRECATE_NODE** (delete) | 16 | No discrete depot; placeholder modelling only |
| **DEPRECATE_NODE** (merge) | 1 | Cleveland aggregate duplicate of R01-sourced node |
| **ADD_SOURCE** | 0 | None of the 17 qualify — all are non-discrete |
| **Edge redirect** | 2 | Cleveland merge + WBS70 → school donor Bauwerk |

## 3. Per-node decisions

| Node id | Action | Redirect / notes |
|---|---|---|
| `bw_berlin_fitout_donor_sources` | DEPRECATE | Aggregate (Boros/Berghain/other sites) |
| `bw_chiro_itterbeek_reuse_supply_network` | DEPRECATE | Supply-network abstraction |
| `bw_donor_gebaudegruppe_resource_rows_mauerwerk` | DEPRECATE | Donor building-group aggregate |
| `bw_externe_stahl_donor_stockholder` | **MERGE →** `bw_cleveland_steel_and_tubes_stock` | R01 PROVEN at cleveland-steel.com; redirects `bg_stahl_traeger_timber_square` AUS_SPENDER + `p_timber_square_london` HAT_BAUWERK |
| `bw_holbein_grosvenor_donor_projects` | DEPRECATE | Grosvenor portfolio aggregate |
| `bw_lo_reninge_reuse_brick_source` | DEPRECATE | Explicit unknown brick source |
| `bw_maison_des_canaux_unspecified_donors` | DEPRECATE | Explicit unknown sources |
| `bw_maison_dna_unknown_brick_donor` | DEPRECATE | Explicit unknown brick donor |
| `bw_messebau_lager_hannover` | DEPRECATE | Generic label; Cityförster PDF cites trade-fair boards from demolition projects, not a named depot |
| `bw_p2_massenwohnungsbau_donor_unknown` | DEPRECATE | Explicit unknown P2 donor building |
| `bw_paris_material_sources_circular_pavilion` | DEPRECATE | Paris aggregate |
| `bw_paris_regional_donor_sources_ferme_du_rail` | DEPRECATE | Paris/regional aggregate; Bellastock is one of many sources — no safe blanket redirect |
| `bw_unbekannte_donor_buildings_zinneke_material_lots` | DEPRECATE | Explicit unknown Zinneke lots |
| `bw_unbekanntes_transformationsgebaeude_kellerwaende` | DEPRECATE | Explicit unknown transformation building |
| `bw_unknown_brick_donor_sources_gjg` | DEPRECATE | Explicit unknown brick donors (GJG) |
| `bw_unknown_demolition_wood_streams` | DEPRECATE | Explicit unknown demolition-wood streams |
| `bw_wbs70_donor_groeditz` | DEPRECATE + redirect | `bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` AUS_SPENDER → `bw_school_type_dresden_donor` (existing donor Bauwerk; parallel to Dresden-type BG) |

## 4. Patch operations (applied)

| Op | Count | Detail |
|---|---:|---|
| `merge_node` | 1 | `bw_externe_stahl_donor_stockholder` → `bw_cleveland_steel_and_tubes_stock` |
| `add_rel` | 1 | WBS70 BG → `bw_school_type_dresden_donor` AUS_SPENDER |
| `delete_node` | 16 | All remaining placeholders |

Dry-run and live apply executed via `_scripts/apply_neo4j_review_patch.py`.

## 5. Post-apply verification

```cypher
MATCH (n:Materialdepot)
RETURN count(n) AS total,
       sum(CASE WHEN coalesce(n.primary_source_url,'') <> ''
                 OR size(coalesce(n.source_urls,[])) > 0
            THEN 1 ELSE 0 END) AS sourced
-- → total: 5, sourced: 5
```

Redirects confirmed live:
- `p_timber_square_london` HAT_BAUWERK → `bw_cleveland_steel_and_tubes_stock`
- `bg_stahlbeton_mehrere_groeditz_wbs70_precast_panels` AUS_SPENDER → `bw_school_type_dresden_donor`

## 6. Residual gaps (intentional)

Deleting placeholder depots removes **59** `AUS_SPENDER` edges and **13** `HAT_BAUWERK` project→depot links where no discrete depot could be named. These donor provenance gaps should be re-wired only when dossier-level evidence names a specific donor building or depot — not by re-introducing aggregate Materialdepot stubs.

**Highest-value future work:** split Paris / Berlin / Chiro aggregates into project-specific donor Bauwerk nodes when intake dossiers permit.
