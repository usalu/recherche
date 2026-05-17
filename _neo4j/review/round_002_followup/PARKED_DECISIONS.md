# Parked items awaiting manual decision

**Generated:** 2026-05-17 (after Phase H).

Two lists of nodes that need a per-item judgement call: **delete / promote / keep as stub**. Recommendations are based on degree, name pattern, and what kind of entity the node represents.

When ready: pick a column, batch the decisions, then run a small patch (delete or promote_to_full). I can generate the patch from a CSV of `id,decision` once you've marked them.

---

## A. Stub Projekte (23 items, all `node_role='cross_reference_stub'`)

Sorted by current degree (rich connections at top).

| Rec | ID | Degree | Notes |
|---|---|---:|---|
| **PROMOTE** | `p_stuttgart_210` | 26 | Stuttgart 21 mention shows up across 26 edges — strong signal this is a real, central case. Worth a dedicated archive `.md` so all the cross-references resolve to substance. |
| **PROMOTE** | `p_lysp8_basel` | 23 | High connectivity. Likely the LysBüchel/LYSP-8 Basel reuse pilot — deserves an archive entry. |
| **PROMOTE** | `p_reallabor_be_ware` | 20 | "Reallabor BE-WARE" — Berlin reuse Reallabor program. High connectivity. |
| **KEEP STUB** | `p_schaerenmoosstrasse_zuerich` | 10 | Zürich case; moderately connected. Promote later if archive added. |
| **KEEP STUB** | `p_umar_unit` | 10 | UMAR (Urban Mining and Recycling) NEST unit at Empa — could promote as a unit-scale demonstrator. |
| **RELABEL → Programm** | `p_eth_circular_construction_student_reuse` | 8 | This is a *teaching/research initiative* at ETH, not a building. Should be on a `Programm` or `Initiative` label, not `Projekt`. |
| **RELABEL → Programm** | `p_reuse_in_construction_zhaw` | 8 | ZHAW research programme — same as above. |
| **RELABEL → Programm** | `p_architecture_of_reuse_brussels` | 7 | Pedagogical/research initiative; relabel. |
| **KEEP STUB** | `p_elementa_walkeweg` | 7 | Basel project; archive not added yet. |
| **RELABEL → Programm** | `p_vandkunsten_component_reuse` | 7 | Vandkunsten's reuse R&D track, not a single project. |
| **KEEP STUB** | `p_careno_becircular` | 5 | Belgian Careno/BeCircular case study; keep till archive added. |
| **RELABEL → Programm** | `p_fcrbe` | 5 | FCRBE = Facilitating the Circulation of Reclaimed Building Elements — an Interreg programme, not a building. |
| **KEEP STUB** | `p_meduni_campus_mariannengasse` | 5 | MedUni Vienna campus reuse case; keep till archive. |
| **DELETE** | `p_obk_27` | 5 | "OBK 27" — too cryptic, no source archive, unclear what it refers to. Recommend deletion unless you know the reference. |
| **KEEP STUB** | `p_pavilion_circl_amsterdam` | 5 | Pavilion at Circl Amsterdam — related to ABN AMRO Circl; could merge into `p_circl_abn_amro`. |
| **RELABEL → Plattform** | `p_refair_bordeaux_reemploi_platform` | 5 | This is a platform/tool, not a building project. Could become a Marktmodell instance or Plattform node. |
| **KEEP STUB** | `p_circl_abn_amro` | 4 | Often referenced alongside Circl pavilion; consider merging with `p_pavilion_circl_amsterdam`. |
| **PROMOTE** | `p_granby_workshop` | 3 | Granby 4 Streets / Assemble — actually a well-known Turner-Prize-related project; worth promoting + archive. |
| **RELABEL → Programm** | `p_interreg_nwe_fcrbe` | 3 | Duplicate-ish of `p_fcrbe`; merge or relabel. |
| **RELABEL → Plattform** | `p_rcmi_concular` | 3 | RCMI / Concular platform — same family as `p_refair_*`. |
| **KEEP STUB** | `p_re_use_hoefe` | 3 | "Re-Use Höfe" — Vienna reuse hubs; might be a programme rather than single project. |
| **RELABEL → Programm** | `p_rebridge_structural_reuse_project` | 3 | "ReBridge" R&D project on structural reuse. |
| **RELABEL → Plattform** | `p_reuse_logistics` | 3 | Generic logistics initiative; probably a category, not a Projekt. |

### Summary of recommendations

- **PROMOTE (4):** p_stuttgart_210, p_lysp8_basel, p_reallabor_be_ware, p_granby_workshop — write dedicated archive `.md` files
- **RELABEL → Programm / Plattform (9):** Move out of `Projekt` label
- **KEEP STUB (9):** Defer to round 003 or later archive expansion
- **DELETE (1):** p_obk_27 (cryptic, no evidence)
- **MERGE candidate (1):** p_pavilion_circl_amsterdam → p_circl_abn_amro

---

## B. Stub Akteure (16 items, degree 0 or 1)

| Rec | ID | Degree | Notes |
|---|---|---:|---|
| **DELETE** | `bizh` | 0 | Unknown abbreviation; no connections; no source scope. |
| **KEEP** | `glasfischer_glastec` | 0 | Real company (glass technology). Probably orphaned because no project lists them. Could absorb in round 003. |
| **KEEP** | `heinrich_boell_stiftung` | 0 | Heinrich-Böll-Stiftung — real foundation. Useful as policy/grant reference even at degree 0. |
| **KEEP** | `koimo_development` | 0 | Real Berlin developer; orphaned because no project tags them yet. |
| **KEEP** | `mehr_als_wohnen` | 0 | Genossenschaft "Mehr als wohnen" Zürich — real Bauherr. Round 003 will tag. |
| **KEEP** | `stiftung_habitat` | 0 | Stiftung Habitat — Basel housing foundation. Real entity. |
| **KEEP** | `citydev_brussels` | 1 | Brussels public developer; minimal connection. |
| **DELETE** | `dare_gmbh` | 1 | Unclear which firm; no source scope. |
| **KEEP** | `denkstatt` | 1 | Sustainability consultancy (AT). Real. |
| **KEEP** | `edith_maryon_stift` | 1 | Stiftung Edith Maryon (CH) — well-known reuse foundation. |
| **KEEP** | `eitel_partner` | 1 | Architecture firm. |
| **KEEP** | `gibbins_architekten` | 1 | Architecture firm (CH). |
| **KEEP** | `kunst_stoffe_ev` | 1 | Kunst-Stoffe e.V. Berlin — known reuse association. |
| **MERGE** | `rotor_vzw` | 1 | Rotor cooperative — probably duplicate of `rotor` or `rotor_deconstruction`. Verify and merge. |
| **MERGE** | `zirkular_cirkla` | 1 | Cirkla / Zirkular — probably duplicate of `zirkular` (Basel reuse planner). Verify and merge. |
| **MERGE** | `zusammenkunft_berlin` | 1 | Likely duplicate of an existing collective; check `zusammenkunft`. |

### Summary

- **DELETE (2):** bizh, dare_gmbh — too cryptic
- **MERGE (3):** rotor_vzw, zirkular_cirkla, zusammenkunft_berlin → existing canonical entries
- **KEEP (11):** All real entities; will be tagged naturally as round 003 surfaces them in project archives

---

## Suggested next step

If you accept these recommendations, I can generate one patch:
- 4 promote ops (write archive `.md` + flip `node_role` to `full_projekt`)
- 9 relabel ops (`Projekt` → `Programm` or `Plattform`) — needs decision on whether to keep `Projekt` label as well
- 1 merge op (p_pavilion_circl_amsterdam → p_circl_abn_amro)
- 1 delete op (p_obk_27)
- 3 akteur-merge ops (rotor_vzw, zirkular_cirkla, zusammenkunft_berlin)
- 2 akteur-delete ops (bizh, dare_gmbh)

Plus the 11 "KEEP" akteure and 9 "KEEP STUB" projekte stay; they'll be addressed during round 003.

Mark up this file with your decisions (or just say "accept all recs") and I'll cut the patch.
