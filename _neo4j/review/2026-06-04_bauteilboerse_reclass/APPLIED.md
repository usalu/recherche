# Applied — Bauteilbörse reclassification

- **When:** 2026-06-04 (UTC ~21:08)
- **DB:** `mit-bestand` (only populated DB; default `neo4j` is empty)
- **Script:** `_scripts/migrate_bauteilboerse_reclass_2026-06-04.py`
- **Before-state dump (rollback):** `before_state_2026-06-04T210811Z.json`
- **Compliance:** existing taxonomy values only; **no new taxonomy nodes, no new property keys**.

## Akteurtyp results
| id | before | after |
|---|---|---|
| opalis | Software_Tool_Anbieter | **NGO_Verband_Netzwerk** |
| reuse_and_trade | (none) | **Unternehmen** |
| mobius_reemploi | Materialhub_Bauteilboerse | **Unternehmen** |
| madaster | Software_Tool_Anbieter | **+Unternehmen** |
| new_horizon_urban_mining | Materialhub_Bauteilboerse | **Unternehmen** (dup of new_horizon) |
| loopfront | (none) | **Software_Tool_Anbieter** |
| syphon_ag_bauteilboerse_biel_bruegg | Materialhub_Bauteilboerse | **Unternehmen** (liquidiert 2024-08-26) |
| cleveland_steel_tubes | Materialhub_Bauteilboerse, Unternehmen | **Unternehmen** |
| material_reuse_portal | (none) | **Software_Tool_Anbieter** |
| salvo_ltd | Materialhub_Bauteilboerse | **NGO_Verband_Netzwerk, Organisation** |
| materialnomaden | Materialhub_Bauteilboerse | **Unternehmen** |
| la_fabrique_de_bordeaux_metropole | Oeffentliche_Institution | (no change) |
| new_horizon | Unternehmen | (no change) |
| heyne_tillett_steel | Unternehmen | (no change; HTS Stockmatcher stays a Tool) |

## Geschaeftsmodell / Marktmodell
- opalis: removed Marktmodell `Plattform-Kauf` (directory, non-transactional)
- salvo_ltd: removed `Multi-Vendor-Marktplatz` + `Plattform-Kauf` (those belong to SalvoWEB)
- madaster: +`SaaS-Inventarplattform`
- loopfront: +`SaaS-Inventarplattform`
- material_reuse_portal: +`Netzwerk / Aggregator / Redistribution`
- reuse_and_trade: +`Multi-Vendor-Marktplatz` +`Plattform-Kauf` (general B2B marketplace)

## Verification
- Materialhub_Bauteilboerse-typed actors: **55 → 49**
- None of the 13 remain typed Bauteilbörse.
- **SalvoWEB unchanged** — still `Materialhub_Bauteilboerse` + `Multi-Vendor-Marktplatz` + `Plattform-Kauf` (the real exchange; `BETRIEBEN_VON` Salvo Ltd).
- Export anchor logic updated in `_neo4j/exports/_export_bauteilboerse_network.py`:
  `HAT_GESCHAEFTSMODELL holders` → `Akteurtyp = Materialhub_Bauteilboerse`.

## Not done (deliberately out of strict scope)
- `Akteurrolle` noise (`Materialbroker / Reuse-Marketplace-Betreiber` on non-marketplace actors) left untouched — per-actor nuance; needs its own pass.
- `new_horizon_urban_mining` duplicate reclassified but **not merged** into `new_horizon` (merge = node deletion, conflicts with "nodes stay").
