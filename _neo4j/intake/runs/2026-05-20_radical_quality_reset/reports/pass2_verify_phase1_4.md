# Pass-2 Detailed Verification — Phase 1.4 (Materialdepot relabel)

Verifier: Pass-2 Detailed Verifier 4 of 12
Scope: Plan §1.4 only
Database: `mit-bestand` (bolt://localhost:7687)
Mode: read-only
Run dir: `_neo4j/intake/runs/2026-05-20_radical_quality_reset`

## Verdict

**PASS** — Phase 1.4 is confirmed fully complete. All 10 deep checks pass. The
relabel preserved every original edge; the 6 apparent degree drops relative to
the plan's pre-Phase-1 snapshot are all `out AUS_BAUWERK → :Wiederverwendungskette`
edges that were correctly removed downstream by **Phase 1.1** chain demote
(not by Phase 1.4).

## Deep checks

| # | Check                                                                             | Expected | Observed | Status |
|---|-----------------------------------------------------------------------------------|---------:|---------:|--------|
| 1 | `migrations/mig_1_4_materialdepot.cypher` present and idempotent                  | yes      | yes      | PASS   |
| 2 | `PHASE_1_4_DONE.flag` parseable                                                   | yes      | yes      | PASS   |
| 3 | Live `count(:Materialdepot)`                                                      | 23       | 23       | PASS   |
| 4 | Live nodes with both `:Materialdepot` AND `:Bauwerk`                              | 0        | 0        | PASS   |
| 5 | Live 23 Materialdepot IDs == plan's 23 IDs (set equality)                         | match    | match    | PASS   |
| 6 | All 23 retained original edges (Phase-1.4 perspective)                            | all      | all      | PASS   |
| 7 | `BETRIEBEN_VON` edges with `evidence_source_id='mig_1_4'`                         | ≥ 3      | 3        | PASS   |
| 8 | `:Materialdepot.era_unknown = true` count (Phase 3.1)                             | 23       | 23       | PASS   |
| 9 | `(:Materialdepot)-[:BUILT_IN_ERA]->()` count                                      | 0        | 0        | PASS   |
| 10| Materialdepot panel/key cleanup (if applicable)                                   | n/a      | see § 10 | PASS   |

## Check 1 — Migration file idempotency

`migrations/mig_1_4_materialdepot.cypher` present (47 lines, two statements).

- **1.4.a relabel**: `MATCH (b:Bauwerk) WHERE b.id IN [...] REMOVE b:Bauwerk SET b:Materialdepot`. Idempotent because after first run no `:Bauwerk` matches the 23 IDs and subsequent runs return `relabelled=0`. `REMOVE`/`SET` are themselves no-ops if the label state already matches.
- **1.4.b wire operator**: `MERGE (d)-[r:BETRIEBEN_VON]->(a)` with `ON CREATE SET` for evidence properties. Pure `MERGE` ensures idempotency; re-execution adds zero new edges.

Header comment also documents the reversibility path (`REMOVE :Materialdepot SET :Bauwerk` + `DELETE r:BETRIEBEN_VON {evidence_source_id:'mig_1_4'}`).

## Check 2 — Flag parseable

`PHASE_1_4_DONE.flag` is well-formed JSON:

```json
{
  "phase": "1.4",
  "completed_at": "2026-05-20T20:52:58+00:00",
  "summary": {
    "phase": "1.4",
    "before_bauwerk": 209,
    "after_bauwerk": 186,
    "before_materialdepot": 0,
    "after_materialdepot": 23,
    "relabelled": 23,
    "betrieben_von_touched": 4,
    "expected_relabelled": 23,
    "elapsed_seconds": 0.289
  }
}
```

Note: `betrieben_von_touched=4` reflects pre-Phase-1.6 state (one duplicate edge
to the case-collided `Bellastock` collapsed during the Phase-1.6 merge, leaving
the canonical 3 edges seen live today).

## Checks 3 & 4 — Materialdepot counts

```cypher
MATCH (m:Materialdepot) RETURN count(m);                    -- 23
MATCH (m:Materialdepot) WHERE m:Bauwerk RETURN count(m);    -- 0
MATCH (m:Materialdepot) RETURN DISTINCT labels(m);          -- [["Materialdepot"]]
```

Every Materialdepot carries exactly the single `Materialdepot` label (no
overload with `Bauwerk` or any other label).

## Check 5 — ID set equality

Live 23 Materialdepot IDs vs the 23 IDs in the plan's §1.4 table:

| # | ID                                                       | In plan | Live `:Materialdepot` |
|--:|----------------------------------------------------------|:-------:|:---------------------:|
| 1 | `bw_crclr_kindl_hall`                                    | ✓       | ✓ |
| 2 | `bw_chiro_itterbeek_reuse_supply_network`                | ✓       | ✓ |
| 3 | `bw_berlin_fitout_donor_sources`                         | ✓       | ✓ |
| 4 | `bw_paris_regional_donor_sources_ferme_du_rail`          | ✓       | ✓ |
| 5 | `bw_paris_material_sources_circular_pavilion`            | ✓       | ✓ |
| 6 | `bw_p2_massenwohnungsbau_donor_unknown`                  | ✓       | ✓ |
| 7 | `bw_unknown_demolition_wood_streams`                     | ✓       | ✓ |
| 8 | `bw_holbein_grosvenor_donor_projects`                    | ✓       | ✓ |
| 9 | `bw_maison_des_canaux_unspecified_donors`                | ✓       | ✓ |
| 10 | `bw_verbiest_lagerhaus_zu_haus_und_atelier`             | ✓       | ✓ |
| 11 | `bw_rotor_reuse_stock_charles_malis`                    | ✓       | ✓ |
| 12 | `bw_messebau_lager_hannover`                            | ✓       | ✓ |
| 13 | `bw_maison_dna_unknown_brick_donor`                     | ✓       | ✓ |
| 14 | `bw_externe_stahl_donor_stockholder`                    | ✓       | ✓ |
| 15 | `bw_unknown_brick_donor_sources_gjg`                    | ✓       | ✓ |
| 16 | `bw_lo_reninge_reuse_brick_source`                      | ✓       | ✓ |
| 17 | `bw_unbekanntes_transformationsgebaeude_kellerwaende`   | ✓       | ✓ |
| 18 | `bw_unbekannte_donor_buildings_zinneke_material_lots`   | ✓       | ✓ |
| 19 | `bw_cleveland_steel_and_tubes_stock`                    | ✓       | ✓ |
| 20 | `bw_wbs70_donor_groeditz`                               | ✓       | ✓ |
| 21 | `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager`| ✓       | ✓ |
| 22 | `bw_donor_gebaudegruppe_resource_rows_mauerwerk`        | ✓       | ✓ |
| 23 | `bw_elys_ehemaliges_getraenkelager_areal`               | ✓       | ✓ |

Set equality holds: |plan ∩ live| = 23, |plan △ live| = 0.

## Check 6 — Edge retention vs. snapshot

The pre-Phase-1.4 pre-state is captured in `snapshot/{nodes,relationships}.jsonl`
(2026-05-20 20:42 UTC, before any radical-reset write hit the graph).
Comparing per-ID incident edges from the snapshot against the live graph for
each of the 23 IDs:

| ID                                                       | Plan deg | Live deg | Δ  | Δ explained by |
|----------------------------------------------------------|:--------:|:--------:|:--:|----------------|
| `bw_crclr_kindl_hall`                                    | 26 | 26 | 0 | — |
| `bw_chiro_itterbeek_reuse_supply_network`                | 21 | 21 | 0 | — |
| `bw_berlin_fitout_donor_sources`                         | 17 | 17 | 0 | — |
| `bw_paris_regional_donor_sources_ferme_du_rail`          | 15 | 15 | 0 | — |
| `bw_paris_material_sources_circular_pavilion`            | 14 | 14 | 0 | — |
| `bw_p2_massenwohnungsbau_donor_unknown`                  | 13 | 13 | 0 | — |
| `bw_holbein_grosvenor_donor_projects`                    | 12 | 13 | +1 | Phase 1.4.b `BETRIEBEN_VON → grosvenor` |
| `bw_unknown_demolition_wood_streams`                     | 12 | 12 | 0 | — |
| `bw_verbiest_lagerhaus_zu_haus_und_atelier`              | 12 | 12 | 0 | — |
| `bw_maison_des_canaux_unspecified_donors`                | 12 | 11 | −1 | Phase 1.1 chain demote (out `AUS_BAUWERK → :Wiederverwendungskette wk_maison_des_canaux_unspecified_donor_to_maison_des_canaux_bestandsgebaeude`) |
| `bw_rotor_reuse_stock_charles_malis`                     | 10 | 11 | +1 | Phase 1.4.b `BETRIEBEN_VON → Rotor` |
| `bw_messebau_lager_hannover`                             | 10 |  9 | −1 | Phase 1.1 chain demote (out `AUS_BAUWERK → :Wiederverwendungskette wk_messebau_lager_hannover_to_recyclinghaus_hannover`) |
| `bw_externe_stahl_donor_stockholder`                     |  9 |  9 | 0 | — |
| `bw_maison_dna_unknown_brick_donor`                      |  9 |  8 | −1 | Phase 1.1 chain demote (out `AUS_BAUWERK → :Wiederverwendungskette wk_maison_dna_unknown_brick_donor_to_maison_dna_receiver`) |
| `bw_unknown_brick_donor_sources_gjg`                     |  8 |  8 | 0 | — |
| `bw_lo_reninge_reuse_brick_source`                       |  8 |  8 | 0 | — |
| `bw_unbekanntes_transformationsgebaeude_kellerwaende`    |  8 |  7 | −1 | Phase 1.1 chain demote (out `AUS_BAUWERK → :Wiederverwendungskette wk_unbekanntes_transformationsgebaeude_to_recrete_footbridge_prototype`) |
| `bw_unbekannte_donor_buildings_zinneke_material_lots`    |  8 |  8 | 0 | — |
| `bw_cleveland_steel_and_tubes_stock`                     |  7 |  6 | −1 | Phase 1.1 chain demote (out `AUS_BAUWERK → :Wiederverwendungskette wk_cleveland_steel_and_tubes_stock_to_55_great_suffolk_street_warehouse`) |
| `bw_wbs70_donor_groeditz`                                |  7 |  6 | −1 | Phase 1.1 chain demote (out `AUS_BAUWERK → :Wiederverwendungskette wk_wbs70_donor_groeditz_to_association_house_groeditz`) |
| `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager` |  5 |  6 | +1 | Phase 1.4.b `BETRIEBEN_VON → bellastock` |
| `bw_donor_gebaudegruppe_resource_rows_mauerwerk`         |  5 |  5 | 0 | — |
| `bw_elys_ehemaliges_getraenkelager_areal`                |  4 |  4 | 0 | — |

**Phase-1.4 attributable changes**: +3 edges (the three `BETRIEBEN_VON`), 0
edges lost. The relabel itself preserved every incident edge.

**6 edges lost downstream by Phase 1.1**: all 6 are outgoing
`(:Materialdepot)-[:AUS_BAUWERK]->(:Wiederverwendungskette)` edges to chains
that Phase 1.1 demoted (the 98 unwired Wiederverwendungskette deleted). The
chain demote correctly cascaded these edge deletions. These do not count as
Phase 1.4 regressions and the snapshot fully accounts for them.

**Edge-type rename (Phase 2.4 reuse-flow split)** also visible in the per-ID
inventory: all inbound `AUS_BAUWERK` from `:Bauteilgruppe`/`:Wiederverwendungskette`
were renamed to `FROM_DONOR`, and inbound `EINGEBAUT_IN` similarly renamed to
`INTO_RECEIVER`. Counts are preserved 1:1 (e.g. crclr_kindl_hall had 2
in-`AUS_BAUWERK` + 6 in-`EINGEBAUT_IN` → live 2 in-`FROM_DONOR` + 6
in-`INTO_RECEIVER`). This is also not a Phase 1.4 issue.

## Check 7 — BETRIEBEN_VON edges from mig_1_4

```cypher
MATCH (m:Materialdepot)-[r:BETRIEBEN_VON]->(a:Akteur)
WHERE r.evidence_source_id = 'mig_1_4'
RETURN m.id, a.id, r.evidence_origin, r.evidence_basis, r.evidence_confidence;
```

Returns 3 rows (≥ 3 ✓):

| Materialdepot                                            | Akteur     | origin    | basis        | confidence |
|----------------------------------------------------------|------------|-----------|--------------|------------|
| `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager` | `bellastock` | derived | name_match | unklar     |
| `bw_holbein_grosvenor_donor_projects`                    | `grosvenor`  | derived | name_match | unklar     |
| `bw_rotor_reuse_stock_charles_malis`                     | `Rotor`      | derived | name_match | unklar     |

All three edges carry the four expected evidence properties exactly as the
plan specifies. The flag's `betrieben_von_touched=4` matches the pre-1.6
state; the Phase 1.6 case-normalise merge of `Bellastock → bellastock` collapsed
one duplicate edge, yielding 3 today (consistent with the agent_4 report).

## Check 8 — era_unknown=true (Phase 3.1)

```cypher
MATCH (m:Materialdepot)
RETURN count(m) AS total,
       sum(CASE WHEN m.era_unknown = true THEN 1 ELSE 0 END) AS era_unknown_true,
       sum(CASE WHEN m.era_unknown IS NULL THEN 1 ELSE 0 END) AS era_unknown_null;
-- total=23, era_unknown_true=23, era_unknown_null=0
```

`PHASE_3_1_DONE.flag` confirms Phase 3.1 ran. All 23 Materialdepots carry the
boolean `era_unknown=true`.

## Check 9 — BUILT_IN_ERA from :Materialdepot

```cypher
MATCH (m:Materialdepot)-[r:BUILT_IN_ERA]->() RETURN count(r);   -- 0
```

Zero `BUILT_IN_ERA` edges originate from any Materialdepot, as expected: depots
are not buildings and have no construction era.

## Check 10 — Panel / property-key cleanup (if applicable)

Phase 1.4 itself did not specify panel cleanup; that was orchestrated by later
phases (2.7 / 5.1 panel-tier work). Current state of the `:Materialdepot`
property panel:

| Property key         | Nodes with key |
|----------------------|---------------:|
| `id`                 | 23 |
| `name`               | 23 |
| `name_full`          | 23 |
| `source_scope`       | 23 |
| `is_material_depot`  | 23 |
| `era_unknown`        | 23 |
| `_archive`           | 16 |
| `nutzung_text`       |  6 |
| `land`               |  1 |
| `flaeche_m2`         |  1 |

10 distinct keys (no chaotic key spread). `_archive` field present on 16/23
nodes (the remainder either had no value to archive or were cleaned in a prior
panel pass). Nothing in this panel inventory contradicts Phase 1.4 completion.

## Per-ID edge type breakdown (live)

For traceability, the type-aggregated edge counts per Materialdepot:

| ID | out edges (type × count) | in edges (type × count) |
|---|---|---|
| `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, BELEGT_IN×1, BETRIEBEN_VON×1 | FROM_DONOR×1 |
| `bw_berlin_fitout_donor_sources` | HAT_BAUOBJEKTKLASSE×2, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, HAT_NUTZUNG×2, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×7, NUTZT_BAUWERK×1 |
| `bw_chiro_itterbeek_reuse_supply_network` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×2, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×13, NUTZT_BAUWERK×1 |
| `bw_cleveland_steel_and_tubes_stock` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, HAT_RESSOURCENQUELLE×1, BELEGT_IN×1 | FROM_DONOR×1 |
| `bw_crclr_kindl_hall` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×3, HAT_TRAGWERKSPRINZIP×1, HAT_BAUWEISE×3, HAT_BAUSYSTEM×2, HAT_STATUS×1, HAT_NUTZUNG×3, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×2, INTO_RECEIVER×6, NUTZT_BAUWERK×1 |
| `bw_donor_gebaudegruppe_resource_rows_mauerwerk` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, BELEGT_IN×1 | FROM_DONOR×1 |
| `bw_elys_ehemaliges_getraenkelager_areal` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, BELEGT_IN×1 | — |
| `bw_externe_stahl_donor_stockholder` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, HAT_NUTZUNG×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_holbein_grosvenor_donor_projects` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_TRAGWERKSPRINZIP×1, HAT_BAUWEISE×1, HAT_BAUSYSTEM×1, HAT_STATUS×1, HAT_NUTZUNG×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1, BETRIEBEN_VON×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_lo_reninge_reuse_brick_source` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_maison_des_canaux_unspecified_donors` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×4, NUTZT_BAUWERK×1 |
| `bw_maison_dna_unknown_brick_donor` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_messebau_lager_hannover` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, HAT_NUTZUNG×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_p2_massenwohnungsbau_donor_unknown` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_TRAGWERKSPRINZIP×1, HAT_BAUWEISE×2, HAT_BAUSYSTEM×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×2, NUTZT_BAUWERK×1 |
| `bw_paris_material_sources_circular_pavilion` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×2, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×6, NUTZT_BAUWERK×1 |
| `bw_paris_regional_donor_sources_ferme_du_rail` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×8, NUTZT_BAUWERK×1 |
| `bw_rotor_reuse_stock_charles_malis` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×2, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1, BETRIEBEN_VON×1 | FROM_DONOR×2, NUTZT_BAUWERK×1 |
| `bw_unbekannte_donor_buildings_zinneke_material_lots` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, BELEGT_IN×1 | FROM_DONOR×4 |
| `bw_unbekanntes_transformationsgebaeude_kellerwaende` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_unknown_brick_donor_sources_gjg` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×1, NUTZT_BAUWERK×1 |
| `bw_unknown_demolition_wood_streams` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_TRAGWERKSPRINZIP×1, HAT_BAUWEISE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, LIEGT_IN_LAND×1, BELEGT_IN×1 | FROM_DONOR×3, NUTZT_BAUWERK×1 |
| `bw_verbiest_lagerhaus_zu_haus_und_atelier` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, BELEGT_IN×1 | FROM_DONOR×1, INTO_RECEIVER×5, NUTZT_BAUWERK×1 |
| `bw_wbs70_donor_groeditz` | HAT_BAUOBJEKTKLASSE×1, HAT_BAUOBJEKTROLLE×1, HAT_STATUS×1, LIEGT_IN_STADT×1, BELEGT_IN×1 | FROM_DONOR×1 |

## Final state

Phase 1.4 is fully confirmed complete:

- Migration file present and idempotent.
- Flag parseable and consistent.
- Exactly the 23 plan-listed `:Bauwerk` placeholders were relabelled to
  `:Materialdepot` with **all original edges preserved**.
- The 3 `BETRIEBEN_VON` edges added by Phase 1.4.b carry the required evidence
  properties.
- Downstream phases (3.1 era_unknown flag, no `BUILT_IN_ERA` edges) leave the
  depots in the state the plan expects.
- The 6 small degree decreases vs. the plan's pre-state table are fully
  attributable to Phase 1.1 chain demote (unwired `:Wiederverwendungskette`
  deletion) and are not a Phase 1.4 regression.
