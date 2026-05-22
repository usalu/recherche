# IER-C4 Report — Geo `LIEGT_IN_LAND` / `LIEGT_IN_STADT`

**Agent:** IER-C4  
**Scope:** 362 PARTIAL geo edges (335 `LIEGT_IN_LAND` + 27 `LIEGT_IN_STADT`)  
**Method:** `akteur_typ_projekt_geo.json` primary addresses + donor geo files + imprint `WebFetch` fallback

## Summary

| Metric | Count |
|---|---:|
| Scope rows | 362 |
| Output ledger rows | 362 |
| PARTIAL → PROVEN upgrades | 295 |

### Verdicts

| Verdict | Count |
|---|---:|
| PROVEN | 295 |
| CONTRADICTION | 37 |
| PARTIAL | 25 |
| UNVERIFIABLE | 5 |

### Proposed actions

| Action | Count |
|---|---:|
| KEEP | 259 |
| ESCALATE_HUMAN | 42 |
| ADD_SOURCE | 34 |
| RESOURCE | 18 |
| FIX_PROPERTY | 9 |

## CONTRADICTION rows (skipped — pre-escalated, not in PARTIAL scope)

Five `LIEGT_IN_STADT` edges already carry `CONTRADICTION` from Agent 09. IER-C4 does **not** re-adjudicate them; human patch required per `ledger/provenance_g06.csv`.

| claim_id | from_id | to_id |
|---|---|---|
| 09-lis-0006 | bw_alte_kade_tiel | stadt_utrecht |
| 09-lis-0078 | bw_kerenzerbergtunnel | stadt_zuerich |
| 09-lis-0176 | p_big_dig_building_boston | stadt_boston |
| 09-lis-0190 | p_circular_centre_netherlands_prinsenhof_a_reuse_pilot | stadt_arnhem |
| 09-lis-0204 | p_haus_hos_mehrfamilienhaus_muehlhausen | stadt_leinefelde |

## Notable residual / worst findings

- **09-lil-0002** `2hs` → `land_schweiz`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Deutschland but LIEGT_IN_LAND says Schweiz: Berlin, Germany"
- **09-lil-0023** `angelika_mettke` → `land_deutschland`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Niederlande but LIEGT_IN_LAND says Deutschland: Zwarteweg 1, 8181 PD Heerde, Netherlands"
- **09-lil-0043** `baumab_kassel` → `land_deutschland`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Belgien but LIEGT_IN_LAND says Deutschland: Asse, Halle-Vilvoorde, Vlaams-Brabant, Vlaanderen, België / Belgique / Belgien"
- **09-lil-0070** `circular_construction_lab` → `land_schweiz`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names USA but LIEGT_IN_LAND says Schweiz: United States"
- **09-lil-0075** `circular_structural_design` → `land_niederlande`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Deutschland but LIEGT_IN_LAND says Niederlande: Berlin, Germany"
- **09-lil-0088** `daniel_hoffmann` → `land_schweiz`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Belgien but LIEGT_IN_LAND says Schweiz: Asse, Halle-Vilvoorde, Vlaams-Brabant, Vlaanderen, België / Belgique / Belgien"
- **09-lil-0090** `desso_tarkett` → `land_niederlande`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Schweiz but LIEGT_IN_LAND says Niederlande: Überlandstrasse 129, 8600 Dübendorf, Switzerland"
- **09-lil-0094** `dirk_e_hebel` → `land_schweiz`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Deutschland but LIEGT_IN_LAND says Schweiz: Berlin, Germany"
- **09-lil-0099** `ecovative` → `land_usa`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Schweiz but LIEGT_IN_LAND says USA: Überlandstrasse 129, 8600 Dübendorf, Switzerland"
- **09-lil-0111** `fabian_sauser` → `land_schweiz`: **CONTRADICTION** — project-linked address country != edge land
  - Quote: "address names Belgien but LIEGT_IN_LAND says Schweiz: Asse, Halle-Vilvoorde, Vlaams-Brabant, Vlaanderen, België / Belgique / Belgien"

## Headline

Of **362** PARTIAL geo claims, **295** upgraded to PROVEN (registry address, name_full, or imprint fetch); **37** flagged address-vs-edge mismatches for human review; **25** remain PARTIAL; **5** lack any address or URL.
