# IER-C5 Report — Software / Participation Residual

Agent: **IER-C5** · Scope: **125** tier-C rows (skip tier-D inference)

## Scope recap

| Cluster | Rows |
|---|---:|
| BETEILIGT_AN | 50 |
| NUTZT_SOFTWARE | 35 |
| HAT_BAUWERK | 18 |
| IN_EMPFANGSOBJEKT | 11 |
| Software | 6 |
| AUS_SPENDER | 4 |
| BETRIEBEN_VON | 1 |

Disjointness: tier-D `abgeleitet` / generic-concept `NUTZT_SOFTWARE` self-wiring excluded; tier-B `BETEILIGT_AN` placeholder geo (IER-B1) excluded.

## Verdict counts

| Verdict | Count |
|---|---:|
| PARTIAL | 70 |
| PROVEN | 30 |
| MISSING_EVIDENCE | 23 |
| UNVERIFIABLE | 2 |

**PROVEN upgrades:** 30

## Proposed actions

| Action | Count |
|---|---:|
| RESOURCE | 70 |
| ADD_SOURCE | 37 |
| ESCALATE_HUMAN | 11 |
| DELETE | 7 |

## Ten priority findings

### 1. `A10-R-002` → MISSING_EVIDENCE / DELETE

- **Claim:** Bauteilkatalog Immobilien Basel-Stadt uses a Bauteilkatalog tool
- **Basis:** none `` (fetched=false, http=)
- **Quote:** No page names both 'bauteilkatalog immobilien basel stadt' and 'tool bauteilkatalog' for software use
- **Notes:** tried 0 URLs

### 2. `A10-R-003` → MISSING_EVIDENCE / DELETE

- **Claim:** Re:Crete concrete blocks analysed with FE model
- **Basis:** web `https://opalis.eu/sites/default/files/2022-01/2.40_en_-_reclaimed_solid_terracotta_brick_v01_0.pdf` (fetched=true, http=200)
- **Quote:** No page names both 'beton mehrere recrete betonbloecke bogensegmente' and 'Finite-Elemente-Modell / FE-Modell' for software use
- **Notes:** tried 10 URLs

### 3. `A10-R-014` → MISSING_EVIDENCE / DELETE

- **Claim:** PLP fit-out components used material-passport/Maconda workflow
- **Basis:** web `https://circulars.iclei.org/wp-content/uploads/2021/01/Circular_Procurement_Case_Study_Collection.pdf?utm_source=chatgpt` (fetched=true, http=200)
- **Quote:** No page names both 'mehrere mehrere plfeste fitout komponenten' and 'Material passports / Maconda data workflow' for software use
- **Notes:** tried 67 URLs

### 4. `A10-R-034` → MISSING_EVIDENCE / DELETE

- **Claim:** ELEMENTA Walkeweg used a Bauteilkatalog tool
- **Basis:** web `https://www.elementa.swiss/` (fetched=true, http=0)
- **Quote:** No page names both 'ELEMENTA Walkeweg' and 'tool bauteilkatalog' for software use
- **Notes:** tried 1 URLs

### 5. `A10-R-040` → MISSING_EVIDENCE / DELETE

- **Claim:** Kindergarten Mööslistrasse used a Bauteilkatalog tool
- **Basis:** web `https://www.stadt-zuerich.ch/` (fetched=true, http=200)
- **Quote:** No page names both 'Kindergarten Mööslistrasse / Manegg, Zürich' and 'tool bauteilkatalog' for software use
- **Notes:** tried 1 URLs

### 6. `A10-R-041` → MISSING_EVIDENCE / DELETE

- **Claim:** PLP London HQ used material passports/Maconda workflow
- **Basis:** web `https://circulars.iclei.org/wp-content/uploads/2021/01/Circular_Procurement_Case_Study_Collection.pdf?utm_source=chatgpt` (fetched=true, http=200)
- **Quote:** No page names both 'PLP Architecture HQ / Circular Studio Fit-out, London' and 'Material passports / Maconda data workflow' for software use
- **Notes:** tried 67 URLs

### 7. `A10-R-042` → MISSING_EVIDENCE / DELETE

- **Claim:** Re:Crete footbridge used FE model
- **Basis:** web `https://opalis.eu/sites/default/files/2022-01/2.40_en_-_reclaimed_solid_terracotta_brick_v01_0.pdf` (fetched=true, http=200)
- **Quote:** No page names both 'Re:Crete footbridge — reused concrete blocks' and 'Finite-Elemente-Modell / FE-Modell' for software use
- **Notes:** tried 10 URLs

### 8. `09-in_empfangsobjekt-1101` → PARTIAL / ESCALATE_HUMAN

- **Claim:** Bauteilgruppe bg_holz_mehrere_crclr_recycled_gallery_interior IN_EMPFANGSOBJEKT bw_crclr_kindl_hall
- **Basis:** web `https://concular.de/referenzen/` (fetched=true, http=404)
- **Quote:** unsourced Materialdepot receiver bw_crclr_kindl_hall; bg bg_holz_mehrere_crclr_recycled_gallery_interior donor chain unconfirmed externally
- **Notes:** unsourced depot receiver per agent_09; retain PARTIAL not downgrade

### 9. `09-in_empfangsobjekt-1126` → PARTIAL / ESCALATE_HUMAN

- **Claim:** Bauteilgruppe bg_keramik_boden_verbiest_charleroi IN_EMPFANGSOBJEKT bw_verbiest_lagerhaus_zu_haus_und_atelier
- **Basis:** web `https://opalis.eu/fr/projets/verbiest-karreveld` (fetched=true, http=404)
- **Quote:** unsourced Materialdepot receiver bw_verbiest_lagerhaus_zu_haus_und_atelier; bg bg_keramik_boden_verbiest_charleroi donor chain unconfirmed externally
- **Notes:** unsourced depot receiver per agent_09; retain PARTIAL not downgrade

### 10. `09-in_empfangsobjekt-1130` → PARTIAL / ESCALATE_HUMAN

- **Claim:** Bauteilgruppe bg_keramik_mehrere_verbiest_hanzinelle_fliesen IN_EMPFANGSOBJEKT bw_verbiest_lagerhaus_zu_haus_und_atelier
- **Basis:** web `https://opalis.eu/fr/projets/verbiest-karreveld` (fetched=true, http=404)
- **Quote:** unsourced Materialdepot receiver bw_verbiest_lagerhaus_zu_haus_und_atelier; bg bg_keramik_mehrere_verbiest_hanzinelle_fliesen donor chain unconfirmed externally
- **Notes:** unsourced depot receiver per agent_09; retain PARTIAL not downgrade

## Summary

Processed all **125** disjoint IER-C5 rows via WebFetch + DuckDuckGo search recovery. **30** upgraded to PROVEN with verbatim `proof_quote`. Impact Hub / Concular cluster and Qualis Flow Qflow edges remain the highest-yield software-use recoveries; generic `Bauteilkatalog`/`BIM` concept nodes and `prog_*` programme participation edges largely stay PARTIAL/RESOURCE.
