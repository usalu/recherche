# Remediation Wave 2 — Agent R01 (Materialdepots)

**Database:** `mit-bestand` (2296 nodes / 15338 rels baseline)
**Date:** 2026-06-06
**Ledger:** [`ledger/remediation_r01.csv`](../ledger/remediation_r01.csv) — 22 claim rows
**Patch (PROVEN only):** [`patches/remediation_r01_materialdepot_sources.patch.jsonl`](../patches/remediation_r01_materialdepot_sources.patch.jsonl) — 5 ops
**Method:** Evidence Gate — live `read-cypher` enumeration of all `:Materialdepot` nodes with zero `primary_source_url` / `source_urls`; `WebFetch` for official or first-party URLs; PROVEN requires verbatim quote naming the depot.

## 1. Scope recap

| Work-set | Cypher | Count |
|---|---|---|
| Unsourced `Materialdepot` nodes | `MATCH (n:Materialdepot) WHERE coalesce(n.primary_source_url,'') = '' AND size(coalesce(n.source_urls,[])) = 0 RETURN n` | **22** |

All 22 match Agent 10's finding (graph-wide 0/22 sourced). No other `Materialdepot` nodes exist outside this set.

## 2. Verdict summary

| Verdict | Count | Proposed action |
|---|---:|---|
| PROVEN | 5 | ADD_SOURCE (patch drafted) |
| MISSING_EVIDENCE | 17 | ESCALATE_HUMAN |
| **Total** | **22** | |

| Outcome | Count |
|---|---:|
| Patch ops (`set_node_properties`) | 5 |
| Human escalation (placeholders / aggregates / unknowns) | 17 |

## 3. PROVEN — sources added (patch)

| Node id | name_full (trunc.) | basis_ref | proof quote (verbatim excerpt) |
|---|---|---|---|
| `bw_bellastock_ville_des_terres_l_ile_saint_denis_lager` | Bellastock Ville des Terres / L'Île-Saint-Denis Lager | construction21.org (Résilience case study) | *"Briques en terre crue BTC réemployées … vendues par Bellastock, issues de la Ville des Terres"* |
| `bw_cleveland_steel_and_tubes_stock` | Cleveland Steel and Tubes reclaimed stock | cleveland-steel.com | *"84,000 tonnes of material held at our 100-acre facility in North Yorkshire, UK"* |
| `bw_crclr_kindl_hall` | Ehemalige Lager-/Fassladehalle Kindl-Areal / CRCLR House | buildingsocialecology.org | *"The existing warehouse is being extended"* (former Kindl brewery, Berlin) |
| `bw_elys_ehemaliges_getraenkelager_areal` | Ehemaliges Getränkelager / Dachaufbauten ELYS-Areal | elys-basel.ch | *"Aluminium-Trapezblech von einem ehemaligen Getränkelager im Quartier"* |
| `bw_verbiest_lagerhaus_zu_haus_und_atelier` | Verbiest Lagerhaus zu Haus und Atelier | ica-wb.be (Inventaires W-B) | *"transform a large warehouse (1000 m2) into a single-family house … and a shared art studio"* |

## 4. ESCALATE_HUMAN — no patch (17 nodes)

These nodes are **modelling placeholders** (names contain *Unbekannt* / *Aggregierte* / *unknown*) or **abstract donor pools** with no findable discrete depot URL. Per Agent 10 and re-check here: no official page names the node as a depot → `MISSING_EVIDENCE` + `ESCALATE_HUMAN`.

| Node id | Reason |
|---|---|
| `bw_berlin_fitout_donor_sources` | Aggregated Berlin donor sources (Boros/Berghain etc.) |
| `bw_chiro_itterbeek_reuse_supply_network` | Supply-network abstraction, not a depot |
| `bw_donor_gebaudegruppe_resource_rows_mauerwerk` | Donor building-group aggregate |
| `bw_externe_stahl_donor_stockholder` | Aggregate; likely duplicate of Cleveland stock node |
| `bw_holbein_grosvenor_donor_projects` | Grosvenor portfolio aggregate |
| `bw_lo_reninge_reuse_brick_source` | Explicit unknown brick source |
| `bw_maison_des_canaux_unspecified_donors` | Explicit unknown sources |
| `bw_maison_dna_unknown_brick_donor` | Explicit unknown brick donor |
| `bw_messebau_lager_hannover` | Generic trade-fair storage; unverifiable |
| `bw_p2_massenwohnungsbau_donor_unknown` | Explicit unknown P2 donor building |
| `bw_paris_material_sources_circular_pavilion` | Aggregated Paris sources |
| `bw_paris_regional_donor_sources_ferme_du_rail` | Aggregated Paris/regional sources |
| `bw_unbekannte_donor_buildings_zinneke_material_lots` | Explicit unknown Zinneke lots |
| `bw_unbekanntes_transformationsgebaeude_kellerwaende` | Explicit unknown transformation building |
| `bw_unknown_brick_donor_sources_gjg` | Explicit unknown brick donors |
| `bw_unknown_demolition_wood_streams` | Explicit unknown demolition-wood streams |
| `bw_wbs70_donor_groeditz` | WBS70 donor building; needs dossier-level verification |

**Recommended human actions:** deprecate or relabel placeholder nodes; merge `bw_externe_stahl_donor_stockholder` into `bw_cleveland_steel_and_tubes_stock` if intended duplicate; split aggregates into project-specific donor edges where dossiers allow.

## 5. Apply status

Dry-run and live apply executed via `_scripts/apply_neo4j_review_patch.py` (see `apply_reports/remediation_r01_materialdepot_sources.patch.apply_report.md`).

Post-apply expectation: **5/22** `Materialdepot` nodes sourced; **17** remain unsourced pending structural cleanup.

## 6. Fetch notes

- `bellastock.com/projets/resilience/` — timeout; used Construction21 case study (lists Bellastock as réemploi AMO; BTC from Ville des Terres) plus Build Green ActLab article as secondary URL on patch.
- `circularmaterialsystems.com`, `asbp.org.uk/55-great-suffolk-street` — timeout (not needed for final 5 PROVEN set).
- `agwa.be` project pages — 404 from fetch tool; Verbiest proven via ICA W-B official inventory + WBA project page as secondary.
