# Connectivity recheck — internet + graph crosswalk

**Date:** 2026-06-05  
**Question:** Are there any **other** nodes besides `prog_preuse` and `p_oxy_centre_monnaie` that pass the ≥4-edge gate to **bubble seeds**?

**Bubble seeds (scoring baseline):** `Rotor`, `rotordc`, `opalis`, `bellastock`, `prog_fcrbe`, plus tightly coupled existing projects `p_multi_brussels_reuse_in_multi`, `p_recypark_demets_anderlecht`, `p_architecture_of_reuse_brussels`.

---

## Method

1. Second-pass web search: AMOP, Architecture of Reuse, SAU/Usquare, CCRI/FCRBE/PREUSE, Whitewood cluster, brussels_environment funding layer.
2. Crosswalk against `2026-06-03` export + live centrality report.
3. Score each **candidate new node** by count of **new** edges to bubble seeds (not taxonomy, not quellen).

---

## Verdict: still only 2 new nodes

| Candidate | New edges to bubble seeds | Evidence | Decision |
|---|---:|---|---|
| **`prog_preuse`** | 4+ (Rotor, bellastock, opalis context, city_of_utrecht; bridges FCRBE) | W01–W04, W28–W30 | **IMPORT** |
| **`p_oxy_centre_monnaie`** | 4 (Rotor, rotordc, whitewood, immobel) | W07–W08, W36–W37 | **IMPORT** |
| `p_amop_mission` | 2 (Rotor, brussels_environment) | [AMOP Mission](https://www.rotordb.org/en/projects/amop-mission) | **SKIP** — authorities (citydev, Beliris, …) mostly absent from graph |
| `p_sau_caserne` / Usquare | 1 (Rotor) | [SAU Caserne](https://www.rotordb.org/en/projects/sau-caserne) | **SKIP** |
| `p_caserne_tresignies_south_wing` | 1 (Rotor) | W09 | **SKIP** |
| `p_boardwalk_*` | 1 (Rotor) | W10–W11 | **SKIP** |
| `bw_rotordc_evere_*` | 2 (rotordc, Rotor) | W14–W16 | **SKIP** |
| `citydev_brussels` | 1–2 (Rotor via AMOP; FCRBE Greenbizz indirect) | AMOP list, FCRBE Greenbizz II pilot | **SKIP** |
| `la_fabrique_des_quartiers` | 1 (prog_preuse) | W31–W32 | **SKIP** |
| Donor `:Bauwerk` (CBR, Borgerstein, …) | 1 each (rotordc) | W24–W26, W38, W43 | **SKIP** |
| `city_of_mechelen`, `city_of_lorient`, LIST | 1 each (prog_preuse) | W32 | **SKIP** |

---

## High-value finds that are **not** new nodes

These already exist in the graph but were underused in the first plan. Import as **edge enrichments only**.

### 1. `p_architecture_of_reuse_brussels` (`:Programm`) — meta-hub

**Already in graph.** Rotor and rotordc already have `BETEILIGT_AN` (unklar).

| Fact | Source |
|---|---|
| BMA publication featuring **14 Brussels reuse projects** | [rotordb.org/…/architecture-reuse-brussels](https://rotordb.org/en/projects/architecture-reuse-brussels) |
| Rotor explicitly on **Zinneke, Multi, Recypark** | same |
| rotordc participant at BMA launch (Olivia Noel) | [bma.brussels/…](https://bma.brussels/en/the-architecture-of-reuse-in-brussels/) |

**Action:** Phase 1b — upgrade `Rotor` + `rotordc` → `p_architecture_of_reuse_brussels` to **belegt**; `BELEGT_IN` BMA URL. No new node.

Connects narrative across `p_multi`, `p_recypark_demets_anderlecht`, `p_zinneke_feder_masui4ever_brussels` (all exist) without inter-project edges.

### 2. `brussels_environment` — policy/funder hub (existing)

| Fact | Source |
|---|---|
| FCRBE partner (edge exists, unklar) | export + [FCRBE page](https://rotordb.org/en/projects/interreg-nwe-fcrbe) |
| Funds Rotor's PREUSE/Opalis share via **Renolution** | [opalis.eu/en/about](https://opalis.eu/en/about) |
| Commissioned **AMOP** reuse support (12 pilots, 2020–2021) | [AMOP Mission](https://www.rotordb.org/en/projects/amop-mission) |
| Commissioner for **Georges Henri playground** rotordc salvage | W38 |

**Action:** Phase 1 — `brussels_environment` → `prog_preuse` `BETEILIGT_AN` (partner/funder role); enrich FCRBE edge to belegt; optional `VERBUNDEN`/`supports` enrichment to `opalis` via sidecar (no new opalis–programme rel type unless schema allows).

**Bubble-seed edges added:** prog_preuse, prog_fcrbe, opalis (context), Rotor (AMOP) = **4 enrichments, 0 new nodes**.

### 3. Whitewood / Immobel / CONIX cluster (existing)

| Actor | Already connected | OXY/Multi evidence |
|---|---|---|
| `whitewood` | `p_multi` BETEILIGT (unklar) | W07, W37 — Multi + OXY commissioner |
| `immobel` | `p_multi` BETEILIGT (unklar) | W07 |
| `conix_rdbm` | `p_multi` BETEILIGT (unklar) | W12, Multi project page |

**Action:** Covered by Phase 2 (OXY) + Phase 3 (Multi upgrades). No new commissioner nodes.

### 4. `p_recypark_demets_anderlecht` + `51n4e` (existing)

Recypark already has **6+ actor** `BETEILIGT_AN` edges (51N4E, Bruxelles-Propreté, Witteveen&Bos, …). Rotor participation is belegt (W18); **rotordc** remains deferred (W19).

**Action:** Optional Phase 3b — upgrade `Rotor` → `p_recypark` to **belegt** only. Not a new node.

### 5. Colocation Rotor / rotordc (edge enrichment)

[Rotor DC: reuse made easy](https://www.rotordb.org/en/projects/rotor-dc-reuse-made-easy): *"Rotor's offices are now located literally above RotorDC's stocks"*; shared Evere journey.

**Action:** Enrich existing `rotordc`↔`Rotor` `VERBUNDEN_MIT_AKTEUR` to **belegt** (W45/W50). No Evere `:Bauwerk` node.

### 6. FCRBE ↔ rotordc (edge only, teilweise)

FCRBE Paris Dance Center pilot: **Supplier: Rotor Déconstruction** (W35). Links operational layer to `prog_fcrbe` without new node.

---

## Candidates explicitly ruled out after recheck

| Candidate | Why it looked promising | Why it still fails |
|---|---|---|
| AMOP mission | 12 Brussels pilots, citydev listed | Only 2 bubble-seed endpoints in graph; rest are absent actors |
| SAU / Usquare | 40k m², citydev/ULB/VUB | ULB/VUB/SAU not in graph; 1 seed (Rotor) |
| Evere site | 14k m², ERDF, citydev | 2 seeds (rotordc, Rotor); physical node low ROI |
| Architecture of Reuse | Links 3 projects | **Already `p_architecture_of_reuse_brussels`** — enrich, don't create |
| CCRI / KARMA visit | Names FCRBE + PREUSE | Event corroboration only; no new graph entity |

---

## Updated import plan delta

Add to [`INTEGRATION_PLAN.md`](INTEGRATION_PLAN.md) Phase 1:

| Addition | Type |
|---|---|
| `brussels_environment` → `prog_preuse` | new edge |
| `brussels_environment` → `prog_fcrbe` upgrade | enrich |
| `Rotor` + `rotordc` → `p_architecture_of_reuse_brussels` upgrade | enrich |
| `rotordc` ↔ `Rotor` VERBUNDEN upgrade | enrich |
| Optional `Rotor` → `p_recypark` upgrade | enrich |

**New node count unchanged: 2.**

---

## New evidence rows (recheck)

| ID | URL | Use |
|---|---|---|
| W48 | https://rotordb.org/en/projects/architecture-reuse-brussels | p_architecture_of_reuse_brussels upgrade |
| W49 | https://www.rotordb.org/en/projects/amop-mission | brussels_environment ↔ Rotor context (sidecar; no AMOP node) |
| W50 | https://www.rotordb.org/en/projects/rotor-dc-reuse-made-easy | rotordc↔Rotor colocation enrich |
| W51 | https://circular-cities-and-regions.ec.europa.eu/news/ccri-pilot-flanders-visits-rotor-learn-about-construction-material-reuse | FCRBE/PREUSE corroboration (sidecar) |
