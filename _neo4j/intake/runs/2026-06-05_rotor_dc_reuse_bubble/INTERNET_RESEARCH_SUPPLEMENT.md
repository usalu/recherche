# Internet research supplement — gaps vs evidence

**Run:** `2026-06-05_rotor_dc_reuse_bubble`  
**Date:** 2026-06-05  
**Purpose:** Close gaps flagged in [`CENTRALITY_ANALYSIS.md`](CENTRALITY_ANALYSIS.md) with first-party URLs.  
**Register:** [`EVIDENCE_REGISTER_SUPPLEMENT.csv`](EVIDENCE_REGISTER_SUPPLEMENT.csv)

---

## Summary

| Category | Was missing | Research result |
|---|---|---|
| Ecosystem spine | 5 edges + `prog_preuse` | **All unblockable** — first-party quotes on Opalis, PREUSE, Rotor pages |
| Projects | OXY, Caserne, Boardwalk | **3 new `:Projekt` nodes** — Rotor project pages verified |
| rotordc project links | Multi confidence; Recypark; **new OXY link** | Multi → **belegt**; OXY → **belegt** (RotorDC reconversion); Recypark rotordc → still weak |
| Physical hub | Evere 14k m² site | **Unblockable** — rotordc.com + citydev + BMA ERDF call |
| PREUSE partners | Partial roster in graph | Lead partners verified; bulk municipal partners **defer** |
| Donor buildings | CBR, BOMACO, tag list | Homepage/blog evidence exists; bulk import **defer** per dossier caution |

---

## 1. Ecosystem spine — now evidence-ready

### 1.1 `prog_preuse` (missing node)

| Field | Value |
|---|---|
| Proposed `id` | `prog_preuse` |
| Label | `:Programm` |
| Name | PREUSE — Public Responses to Enable the Use of Salvaged building Elements |
| Lead | Rotor (Lead Partner, Belgium) |
| Dates | 22 Nov 2023 – 29 Feb 2028; main implementation Mar 2024 – Nov 2027 |
| Budget | €6M total / €3.6M ERDF (Rotor page); preuse.nweurope.eu cites €6.77M total |
| URLs already in graph | `q_url_150bfa71…` (homepage), `q_url_4a94cddf…` (partners), `q_url_714d4c31…` (Rotor project), `q_url_00fb7425…` (launch news) |

**Quote (belegt):** preuse.nweurope.eu/partners — *"PREUSE is an international project bringing together 9 partners in 4 different countries"*; Rotor listed as **Lead Partner**.

### 1.2 Missing edges — verified quotes

| Edge | Confidence | Primary URL | Quote (≤240 chars) |
|---|---|---|---|
| `opalis` ↔ `rotordc` | **belegt** | https://opalis.eu/en/dealers/rotor-deconstruction | *"Rotor Deconstruction is a co-operative enterprise in Brussels… offshoot of… Rotor… operates as a separate entity since 2016."* |
| `opalis` ↔ `bellastock` | **belegt** | https://opalis.eu/en/about | *"Since 2019, the cooperative Bellastock has joined the project. They updated the section on French salvage dealers…"* |
| `opalis` → FCRBE context | **belegt** | https://opalis.eu/en/about | *"Between 2019 and 2023, the website was further developed within the framework of the FCRBE project."* |
| `opalis` → PREUSE context | **belegt** | https://opalis.eu/en/about | *"Between 2024 and 2027, Opalis is maintained and updated by Rotor and Bellastock as part of… PREUSE."* |
| `Rotor` → `prog_preuse` | **belegt** | https://rotordb.org/en/projects/preuse-interreg-nwe | *"Rotor is leading a new Europe-funded project… PREUSE."* |
| `bellastock` → `prog_preuse` | **belegt** | https://preuse.nweurope.eu/partners | Bellastock listed under **Partners** (France) |
| `rotordc` ↔ `bellastock` | **teilweise_belegt** | indirect only | No direct first-party statement; link via Opalis/PREUSE/FCRBE mesh only |

**Note:** Graph already has `q_chiro_d_itterbeek_dilbeek_s5` → Opalis dealer URL, but **no** `VERBUNDEN_MIT_AKTEUR` edge opalis↔rotordc.

### 1.3 Duplicate Rotor↔opalis edges

Live graph has **two** `VERBUNDEN_MIT_AKTEUR` edges (`r_opalis__…__Rotor` and `r_Rotor__…__opalis`). Integration should **enrich, not duplicate**.

---

## 2. Projects — new nodes verified

| Proposed `id` | Rotor project URL | Role | rotordc involvement |
|---|---|---|---|
| `p_oxy_centre_monnaie` | https://rotordb.org/en/projects/oxy-centre-monnaie | Rotor design assistance 2020–2025; 4–6% reuse target; 89% retention | **Yes** — https://rotordb.org/en/news/works-oxy-well-underway: *"300 running meters of original aluminium facade profiles which will be reconverted to lighting fixtures by RotorDC"* |
| `p_caserne_tresignies_south_wing` | https://rotordb.org/en/projects/caserne-tresignies-south-wing | Rotor inventories, dismantling tests, specs, monitoring (2022–2026) | **No** on Rotor page; press names **Retrival** as dismantling operator — do not attribute dismantling to rotordc |
| `p_boardwalk_reclaimed_tropical_hardwood` | https://rotordb.org/en/projects/boardwalk-reclaimed-tropical-hardwood | Rotor design assistance; 300 m² azobé boardwalk, Minerve Edegem | **No** — material via Van Hameren Houthandel; corroboration: https://www.minerve.info/nieuws/vlonder/ |

**Commissioners (already in graph):** `whitewood`, `immobel` — OXY news links them to Rotor reuse work (same pattern as Multi).

### 2.1 Confidence upgrades on existing projects

| Edge / fact | Was | Now | Source |
|---|---|---|---|
| `Rotor` / `rotordc` `BETEILIGT_AN` `p_multi_brussels_reuse_in_multi` | unklar / teilweise | **belegt** | https://rotordb.org/en/projects/multi-de-brouckere-tower — *"Flamed granite flooring, salvaged by Rotor DC from the Generale de Banque…"*; corroborated https://www.triodos.be/fr/articles/2025/multi-une-reconversion-pionniere-exemplaire-rotor-construction-circulaire |
| `rotordc` `BETEILIGT_AN` `p_recypark_demets_anderlecht` | missing | **still defer** | Rotor/51N4E/RIBA name **Rotor** as salvage consultant; rotordc blog post is inspiration-only (https://rotordc.com/blog/inspiration-4/recypark-in-anderlecht-brussels-101) |

---

## 3. Physical hub — Evere / Da Vinci site

| Proposed `id` | Label | Evidence |
|---|---|---|
| `bw_rotordc_evere_da_vinci_site` | `:Bauwerk` or `:Standort` | 14 000 m²; Avenue de Bâle 3, 1140 Evere; Da Vinci business district, citydev.brussels |

| Source | Quote |
|---|---|
| https://rotordc.com/about-us | *"14,000 m² site in the Da Vinci business district of citydev.brussels"* |
| https://rotordc.com/contact | *"Our site is located in Da Vinci business park by citydev.brussels"* |
| https://bma.brussels/en/rotor-en/ | ERDF Circular Hub; client RTRDC; Avenue de Bâle 3, 1140 Evere; budget €2.9M works |
| https://www.brusiness.brussels/rotor-dc-pionier-in-hergebruik-von-bouwmaterialen/ | Long-term lease/erfpacht from CityDev.brussels (secondary corroboration) |

**Edges:** `rotordc` + `Rotor` → site (`LIEGT_IN` / `VERBUNDEN` / `BETEILIGT_AN` per schema convention); optional `citydev_brussels` as `:Akteur` (URL `q_url_ca958507…` already in graph).

---

## 4. PREUSE partner roster (selective)

Verified on https://preuse.nweurope.eu/partners:

| Partner | Graph status | Import? |
|---|---|---|
| Rotor | `Rotor` ✓ | lead — `BETEILIGT_AN` upgrade |
| Bellastock | `bellastock` ✓ | yes |
| LIST | check `list` / `luxembourg_institute` | defer until id match |
| Stad Mechelen | no dedicated node seen | defer |
| La Fabrique des Quartiers | `la_fabrique_de_bordeaux_metropole` — **wrong entity?** | verify before edge |
| Municipality of Wiltz | defer | |
| Greater Paris Metropolis | defer | |
| City of Lorient | defer | |
| City of Utrecht | `city_of_utrecht` ✓ (FCRBE already) | `BETEILIGT_AN` prog_preuse after node exists |
| Neighborhood Production | defer | |

**Pilot operations** (preuse.nweurope.eu/pilot-operations): Lorient, La Fabrique des Quartiers (Roubaix), Utrecht — defer project nodes until pilot pages fetched per site.

---

## 5. Tier-2 actors (optional)

| Actor | Evidence | Recommendation |
|---|---|---|
| Atelier 4/5 | https://opalis.eu/en/about; https://rotordb.org/en/projects/plateforme-reemploi | Optional `VERBUNDEN_MIT_AKTEUR` opalis↔atelier; low priority |
| citydev.brussels | rotordc.com, brusiness | Optional `:Akteur` for urban-development context |
| Van Hameren Houthandel | Boardwalk + Minerve page | Supplier for boardwalk only; not bubble spine |
| Retrival | DH Caserne article | Caserne dismantling operator; **not** rotordc |

---

## 6. Donor-building network — partial URLs found

Homepage https://rotordc.com/ still lists: Générale de Banque, CBR, BOMACO, Emery & Cie, Sonian Wood Coop, Bomarbre.  
Blog https://rotordc.com/blog/salvaging-by-rotordc-3/ — Borgerstein, CCN, Durobor, PointCulture, etc.

**Recommendation:** Import **only** donors with explicit material statements and cross-links to existing graph nodes:

| Building | Graph id | Unblock? |
|---|---|---|
| Générale de Banque HQ | `bw_generale_de_banque_brussels` ✓ | **Yes** — link to Multi + rotordc via S18/Triodos |
| CBR Building | create `bw_cbr_building_brussels` | teilweise — homepage listing only |
| Others from §9 tag list | — | **Defer** — dossier §9 caution unchanged |

---

## 7. New URLs to add to quelle register

See `EVIDENCE_REGISTER_SUPPLEMENT.csv`. Notable **not yet in graph**:

- https://rotordb.org/en/projects/oxy-centre-monnaie
- https://rotordb.org/en/news/works-oxy-well-underway
- https://rotordb.org/en/projects/caserne-tresignies-south-wing
- https://rotordb.org/en/projects/boardwalk-reclaimed-tropical-hardwood
- https://opalis.eu/en/about (may need canonical `q_url_*` if absent)
- https://opalis.eu/en/documentation (FCRBE booklets)
- https://www.triodos.be/fr/articles/2025/multi-une-reconversion-pionniere-exemplaire-rotor-construction-circulaire
- https://bma.brussels/en/rotor-en/
- https://www.minerve.info/nieuws/vlonder/
- https://rotordb.org/en/projects/plateforme-reemploi

---

## 8. Still deferred (unchanged)

| Item | Reason |
|---|---|
| §13 matrix scores | Analytical, not measurements |
| Bulk blog-tag buildings (AG Campus, WTC, …) | Tag index ≠ per-case proof (dossier §9) |
| `rotordc` `BETEILIGT_AN` Recypark | Only Rotor named on project pages; rotordc blog is non-participation |
| Full PREUSE 9-partner mesh | Municipal partners need per-site verification |
| `rotordc` ↔ `bellastock` direct edge | No first-party direct link |
| FCRBE capitalisation partners bulk (LIST, TU Delft) | Already partial on prog_fcrbe; PREUSE overlap needs dedup review |
| Kanal Museum, SAU Caserne, Permeke | Rotor projects list only — no detail import without page fetch |

Full defer list: [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md).

---

## 9. Recommended patch priority (post-research)

1. **Phase 0:** Research dossier node + supplement URL quellen  
2. **Phase 1:** `prog_preuse` node; ecosystem `VERBUNDEN`/`BETEILIGT_AN` spine (7 edges)  
3. **Phase 2:** `p_oxy_centre_monnaie`, `p_caserne_tresignies_south_wing`, `p_boardwalk_…`; Rotor/rotordc/OXY/Multi upgrades  
4. **Phase 3:** `bw_rotordc_evere_da_vinci_site`; Generale de Banque → Multi material path  
