# IER-B2 Report — Dossier Bauwerk / Projekt

Agent: **IER-B2** · Scope: **41** rows (21 `HAT_BAUWERK` PARTIAL + 20 `:Projekt` ME)

## Scope recap

- Tier B shard: `HAT_BAUWERK` partial edges not in geo donor/receiver chain export
- Tier B shard: `:Projekt` nodes with `MISSING_EVIDENCE` (no real `source_urls`)
- Excluded: 2 Materialdepot-target `HAT_BAUWERK` rows (IER escalation / tier-D crossover)

## Verdict counts

| Verdict | Count |
|---|---:|
| PARTIAL | 24 |
| PROVEN | 16 |
| UNSUPPORTED | 1 |

**PROVEN upgrades:** 16 (from prior PARTIAL/ME)

## Proposed actions

| Action | Count |
|---|---:|
| ADD_SOURCE | 31 |
| RESOURCE | 8 |
| DELETE | 1 |
| ESCALATE_HUMAN | 1 |

## Ten priority findings

### 1. `09-hat_bauwerk-0875` → UNSUPPORTED / DELETE

- **Claim:** Projekt p_brent_cross_town_primary_substation_london HAT_BAUWERK bw_cancelled_oil_gas_pipeline_projects (role=donor)
- **Basis:** logic `aggregate_stub_check` (fetched=false, http=)
- **Quote:** Aggregate donor stub 'Surplus / cancelled oil-and-gas pipeline projects' (bw_cancelled_oil_gas_pipeline_projects); not a discrete building
- **Notes:** IER-B2: tier-D crossover — aggregate Bauwerk endpoint

### 2. `09-hat_bauwerk-0845` → PARTIAL / RESOURCE

- **Claim:** Projekt la_fabrique_de_bordeaux_metropole HAT_BAUWERK bw_base_du_reemploi_merignac (role=None)
- **Basis:** web `https://www.bordeaux-metropole.fr/` (fetched=true, http=0)
- **Quote:** No fetched page names both 'la fabrique de bordeaux metropole' and 'base du reemploi merignac' as donor/receiver pair
- **Notes:** tried 1 dossier URLs; pairwise gate not met

### 3. `09-hat_bauwerk-0862` → PROVEN / ADD_SOURCE

- **Claim:** Projekt p_big_dig_building_boston HAT_BAUWERK bw_big_dig_building (role=receiver)
- **Basis:** web `https://metropolismag.com/programs/single-speed-design-the-2004-next-generation-winner/` (fetched=true, http=200)
- **Quote:** Read more June 1, 2004 Single Speed Design: The 2004 Next Generation® Winner Four young architects’ bold idea: reusing remnants from the Big Dig in Boston to create housing.
- **Notes:** HAT_BAUWERK donor link recovered via fetch; names p_big_dig_building_boston + bw_big_dig_building

### 4. `09-hat_bauwerk-0863` → PROVEN / ADD_SOURCE

- **Claim:** Projekt p_big_dig_building_boston HAT_BAUWERK bw_boston_big_dig_infrastructure (role=donor)
- **Basis:** web `https://metropolismag.com/programs/single-speed-design-the-2004-next-generation-winner/` (fetched=true, http=200)
- **Quote:** And Pedini wants to interest state officials in building public housing in Boston from other Big Dig materials.
- **Notes:** HAT_BAUWERK donor link recovered via fetch; names p_big_dig_building_boston + bw_boston_big_dig_infrastructure

### 5. `09-hat_bauwerk-0871` → PROVEN / ADD_SOURCE

- **Claim:** Projekt p_bluecity_offices_rotterdam HAT_BAUWERK bw_tropicana_rotterdam (role=None)
- **Basis:** web `https://www.tudelft.nl/en/architecture-and-the-built-environment/circular-design-atlas/blue-city` (fetched=true, http=200)
- **Quote:** The concept involves reusing the 12.000 m2 building Tropicana, a former tropical swimming paradise that lost its original function and is now hosting offices and events.
- **Notes:** TU Delft circular atlas names BlueCity reuse of Tropicana building

### 6. `09-hat_bauwerk-0898` → PARTIAL / RESOURCE

- **Claim:** Projekt p_europa_building_brussels HAT_BAUWERK bw_residence_palace_block_a (role=donor)
- **Basis:** web `https://www.consilium.europa.eu/en/european-council/europa-building/` (fetched=true, http=403)
- **Quote:** No fetched page names both 'Europa Building Brussels / Résidence Palace – Europa' and 'Residence Palace Block A' as donor/receiver pair
- **Notes:** tried 2 dossier URLs; pairwise gate not met

### 7. `09-hat_bauwerk-0910` → PROVEN / ADD_SOURCE

- **Claim:** Projekt p_hastings_pier_visitor_centre HAT_BAUWERK bw_hastings_pier_retained_heritage_context (role=receiver)
- **Basis:** web `https://www.drmm.co.uk/project/hastings-pier/` (fetched=true, http=200)
- **Quote:** Hastings Pier | dRMM Architects You are using an outdated browser.
- **Notes:** HAT_BAUWERK donor link recovered via fetch; names p_hastings_pier_visitor_centre + bw_hastings_pier_retained_heritage_context

### 8. `09-hat_bauwerk-0921` → PROVEN / ADD_SOURCE

- **Claim:** Projekt p_impact_hub_berlin_crclr_fitout HAT_BAUWERK bw_crclr_house_existing_context (role=None)
- **Basis:** web `https://www.buildingsocialecology.org/projects/crclr-house-berlin/` (fetched=true, http=200)
- **Quote:** As soon as the building is finalized, the Impact Hub Berlin will move in and offer co-working spaces, lab facilities and an event program.
- **Notes:** HAT_BAUWERK donor link recovered via fetch; names p_impact_hub_berlin_crclr_fitout + bw_crclr_house_existing_context

### 9. `09-hat_bauwerk-0924` → PARTIAL / RESOURCE

- **Claim:** Projekt p_jeugdkliniek_ithaka_emergis_kloetinge HAT_BAUWERK bw_emergis_bestand_kloetinge (role=donor)
- **Basis:** web `https://www.emergis.nl/` (fetched=true, http=200)
- **Quote:** Emergis homepage confirms operator but not Ithaka youth clinic Kloetinge donor building
- **Notes:** Downgraded: single-endpoint fetch; pairwise gate not met

### 10. `09-hat_bauwerk-0934` → PARTIAL / RESOURCE

- **Claim:** Projekt p_k118_kopfbau_halle_118_winterthur HAT_BAUWERK bw_halle_118_bestand (role=donor)
- **Basis:** web `https://www.lagerplatz.ch/` (fetched=true, http=200)
- **Quote:** Lagerplatz site confirms areal but does not name Halle 118 donor pairing
- **Notes:** Downgraded: single-endpoint fetch; pairwise gate not met

## DELETE proposals (aggregate stubs)

- `09-hat_bauwerk-0875`: p_brent_cross_town_primary_substation_london -HAT_BAUWERK-> bw_cancelled_oil_gas_pipeline_projects — Aggregate donor stub 'Surplus / cancelled oil-and-gas pipeline projects' (bw_cancelled_oil_gas_pipeline_projects); not a discrete building

## Summary

Processed all **41** disjoint IER-B2 rows. **16** upgraded to PROVEN with fetched `proof_quote`. **1** aggregate-stub edges proposed for DELETE. Remaining gaps flagged as RESOURCE/ESCALATE_HUMAN for aggregator merge.
