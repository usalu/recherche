# Rotor DC reuse bubble — connectivity-first import plan

**Run:** `2026-06-05_rotor_dc_reuse_bubble`  
**Dossier:** `_knowledge/reuse_bubbles/rotor_dc_reuse_bubble_v2.md`  
**Graph dossier node:** `q_research_rotor_dc_reuse_bubble_v2_md` (to create Phase 0)  
**Evidence:** [`EVIDENCE_REGISTER_SUPPLEMENT.csv`](EVIDENCE_REGISTER_SUPPLEMENT.csv) (W01–W51), [`EVIDENCE_DEEP_DIVE.md`](EVIDENCE_DEEP_DIVE.md), [`CONNECTIVITY_RECHECK.md`](CONNECTIVITY_RECHECK.md)  
**Baseline:** `mit-bestand` — [`centrality_report.json`](centrality_report.json) (2026-06-05)

## Policy: no low-degree nodes

**New `:Akteur` / `:Projekt` / `:Programm` / `:Bauwerk` nodes only if they are expected to add ≥4 edges to existing bubble seeds** (actors + programmes already in graph), or close a broken tier-1 spine gap.

**Recheck (2026-06-05):** Internet + graph crosswalk — see [`CONNECTIVITY_RECHECK.md`](CONNECTIVITY_RECHECK.md). **No additional new nodes** pass the gate. Several **existing** nodes warrant enrichment: `p_architecture_of_reuse_brussels`, `brussels_environment`, Whitewood cluster.

| Candidate | Expected new edges to existing seeds | Verdict |
|---|---:|---|
| **`prog_preuse`** | Rotor, bellastock, city_of_utrecht, opalis↔bellastock context, stack to prog_fcrbe | **IMPORT** |
| **`p_oxy_centre_monnaie`** | Rotor, rotordc, whitewood, immobel (+ Multi narrative) | **IMPORT** |
| `bw_rotordc_evere_da_vinci_site` | rotordc, Rotor only (~2) | **SKIP** |
| `p_caserne_tresignies_south_wing` | Rotor only (~1; partners not in graph) | **SKIP** |
| `p_boardwalk_reclaimed_tropical_hardwood` | Rotor only (~1) | **SKIP** |
| `la_fabrique_des_quartiers` | prog_preuse only (~1) | **SKIP** |
| Donor `:Bauwerk` (CBR, Borgerstein, CCN, Georges Henri) | rotordc only (~1 each) | **SKIP** — evidence stays in sidecar |
| `bw_generale_de_banque_brussels` | **already exists** | **edges only** (Phase 3) |

---

## Evidence contract (every patch op)

| Property | Value |
|---|---|
| `evidence_basis` | `rotor_dc_reuse_bubble_v2_2026_06_05` or URL-specific id (e.g. `opalis_dealer_rotordc`) |
| `evidence_confidence` | `belegt` \| `teilweise_belegt` — no `abgeleitet` as graph fact |
| `evidence_source_id` | `:Quelle` id |
| `evidence_url` | First-party URL |
| `evidence_quote` | ≤240 chars |
| `review_run` | `rotor_dc_reuse_bubble_2026_06_05` |
| `review_status` | `evidence_backed_pending_apply` |

**Off-graph:** §13 matrix, interpretive labels — [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md).

---

## Already in graph — enrich only

| `id` | Role | Phase |
|---|---|---|
| `Rotor` | Hub (VERBUNDEN 7, BETEILIGT 6) | 1, 2, 3 |
| `rotordc` | Operational (55 rels; thin ecosystem VERBUNDEN 4) | 1, 2, 3 |
| `opalis` | Directory (VERBUNDEN 2 — **main gap**) | 1 |
| `bellastock` | FCRBE partner; isolated from opalis/rotordc | 1 |
| `prog_fcrbe` | 13 inbound BETEILIGT_AN | 1 enrich |
| `p_multi_brussels_reuse_in_multi` | Rotor + rotordc BETEILIGT (unklar) | 3 upgrade |
| `p_recypark_demets_anderlecht` | Rotor only | no rotordc edge |
| `bw_generale_de_banque_brussels` | Donor for Multi granite | 3 material path |
| `whitewood`, `immobel` | Multi/OXY commissioners | 2 |
| `city_of_utrecht` | FCRBE partner → add PREUSE | 1 |
| `brussels_environment` | FCRBE partner; Opalis/PREUSE funder; AMOP commissioner | 1 enrich + **PREUSE edge** |
| `p_architecture_of_reuse_brussels` | BMA programme; links Multi/Recypark/Zinneke narrative | 1b upgrade Rotor+rotordc |
| `maarten_gielen` | Bridges Rotor/rotordc/opalis | no change |

**Do not duplicate:** `r_opalis__VERBUNDEN_MIT_AKTEUR__Rotor` + `r_Rotor__VERBUNDEN_MIT_AKTEUR__opalis` — enrich one, `delete_rel` duplicate if apply script supports safe dedup.

---

## Target connectivity (post-apply)

| Node | Metric | Before | After (target) |
|---|---|---:|---:|
| `opalis` | `VERBUNDEN_MIT_AKTEUR` degree | 2 | **≥4** (Rotor, rotordc, bellastock, maarten_gielen) |
| `rotordc` | ecosystem VERBUNDEN (excl. Chiro BG) | 4 | **≥5** (+ opalis) |
| `bellastock` | edges to spine actors | 1 (prog_fcrbe) | **≥3** (+ opalis, prog_preuse) |
| `prog_preuse` | inbound `BETEILIGT_AN` | 0 (missing) | **≥3** (Rotor, bellastock, city_of_utrecht) |
| Stack | rotordc↔opalis↔Rotor↔prog_fcrbe↔prog_preuse | broken | **connected** |

Chiro-project Bauteilgruppen (23× `BETEILIGT_AN`) are **out of scope** for this bubble import.

---

## Phased patches

### Phase 0 — `patches/phase0_sources_and_dossier.patch.jsonl`

Minimal quellen for phases 1–3 only (~15 URLs, not full W01–W47 dump):

- `q_research_rotor_dc_reuse_bubble_v2_md`
- Existing: `q_url_150bfa71…`, `q_url_4a94cddf…`, `q_url_714d4c31…`, `q_chiro_…_s5` (opalis dealer)
- New ExternalLink: opalis `/en/about`, rotordb OXY project + works-oxy news, rotordb multi-de-brouckere, opalis Generale project, preuse launch blog, FCRBE interreg page (if no `q_url_*` yet)

---

### Phase 1 — `patches/phase1_ecosystem_spine.patch.jsonl`

**One new node:** `prog_preuse` (`:Programm`).

| Op | Endpoints | Evidence | Conf. |
|---|---|---|---|
| `upsert_node` | `prog_preuse` | W01, W03 | belegt |
| `add_rel` / upgrade | `Rotor` → `prog_preuse` `BETEILIGT_AN` | W03, W28 | belegt |
| `add_rel` / upgrade | `bellastock` → `prog_preuse` `BETEILIGT_AN` | W02 | belegt |
| `add_rel` | `city_of_utrecht` → `prog_preuse` `BETEILIGT_AN` | W30 | belegt |
| `add_rel` | `opalis` ↔ `rotordc` `VERBUNDEN_MIT_AKTEUR` | W05 | belegt |
| `add_rel` | `opalis` ↔ `bellastock` `VERBUNDEN_MIT_AKTEUR` | W04, W42b | belegt |
| `enrich_rel` | `Rotor` → `prog_fcrbe` `BETEILIGT_AN` | W33 | unklar → **belegt** |
| `enrich_node` | `opalis` — programme context props / `BELEGT_IN` | W04, W06, W40 | belegt |
| `enrich_rel` | `brussels_environment` → `prog_preuse` `BETEILIGT_AN` | W04c, W49 context | belegt |
| `enrich_rel` | `brussels_environment` → `prog_fcrbe` confidence upgrade | FCRBE partners page | unklar → **belegt** |
| `enrich_rel` | `rotordc` ↔ `Rotor` `VERBUNDEN_MIT_AKTEUR` | W50 colocation Evere | teilweise → **belegt** |

**Optional same phase (edge-only, no new node):** `rotordc` → `prog_fcrbe` `teilweise_belegt` via W35 (FCRBE Paris pilot supplier) — only if programme participation edges are used for `:Programm`; otherwise sidecar-only.

**Explicitly not in Phase 1:** LIST, Mechelen, Lorient, La Fabrique, Evere site, donor Bauwerke, **AMOP mission node** (only 2 seed links — W49).

### Phase 1b — `patches/phase1b_publication_hub.patch.jsonl` (existing node)

| Op | Endpoints | Evidence | Conf. |
|---|---|---|---|
| `enrich_rel` | `Rotor` → `p_architecture_of_reuse_brussels` `BETEILIGT_AN` | W48 — featured Zinneke, Multi, Recypark | → **belegt** |
| `enrich_rel` | `rotordc` → `p_architecture_of_reuse_brussels` `BETEILIGT_AN` | W48 + BMA launch (rotordc participant) | → **belegt** |
| `BELEGT_IN` | programme + BMA PDF URL | W48 | belegt |

No inter-project edges between Multi/Recypark/Zinneke — publication hub stays on existing `:Programm` node.

---

### Phase 2 — `patches/phase2_oxy_hub.patch.jsonl`

**One new node:** `p_oxy_centre_monnaie` (`:Projekt`).

| Op | Endpoints | Evidence | Conf. |
|---|---|---|---|
| `upsert_node` | `p_oxy_centre_monnaie` | W07 | belegt |
| `add_rel` | `Rotor` → `p_oxy` `BETEILIGT_AN` | W07 | belegt |
| `add_rel` | `rotordc` → `p_oxy` `BETEILIGT_AN` | W08 | belegt |
| `add_rel` | `whitewood` → `p_oxy` `BETEILIGT_AN` | W07, W37 | belegt |
| `add_rel` | `immobel` → `p_oxy` `BETEILIGT_AN` | W07 | belegt |
| `BELEGT_IN` | project + actors | W07, W08, W37 | belegt |

Links OXY into existing **Whitewood/Immobel/Multi** commissioner cluster without new commissioner nodes.

---

### Phase 3 — `patches/phase3_material_path_upgrades.patch.jsonl`

**Zero new nodes** — edges + confidence upgrades on existing ids.

| Op | Endpoints | Evidence | Conf. |
|---|---|---|---|
| `enrich_rel` | `rotordc` + `Rotor` → `p_multi` `BETEILIGT_AN` | W12, W13 | → **belegt** |
| `add_rel` | `rotordc` → `bw_generale_de_banque_brussels` (salvage/source) | W21, W23 | belegt |
| `add_rel` | `bw_generale_de_banque_brussels` → `p_multi` (material supply) | W12 | belegt |
| `BELEGT_IN` | rotordc, Multi, Generale | W05b, W21 | belegt |

Use relation types already in graph for donor flows (`FROM_DONOR` / `AUS_BAUWERK` / `VERBUNDEN` — match live schema from Multi/Generale neighbourhood before apply).

---

## Patch volume estimate

| Phase | New nodes | New/upgrade rels (approx.) |
|---|---:|---:|
| 0 | 1 dossier + ~10 quellen | ~10 |
| 1 | **1** (`prog_preuse`) | **~10–11** |
| 1b | **0** | **~3** |
| 2 | **1** (`p_oxy_centre_monnaie`) | **~5–6** |
| 3 | **0** | **~4–6** |
| **Total** | **2** | **~32–36** |

---

## Pre-apply checklist

1. Live baseline: node/rel counts vs `FINAL_AUDIT_REPORT.md`.
2. Confirm `prog_preuse`, `p_oxy_centre_monnaie` absent.
3. Confirm `city_of_utrecht`, `whitewood`, `immobel`, `bw_generale_de_banque_brussels` present.
4. Dry-run each phase; **no `missing_endpoint`** across ordered apply.
5. Post-apply: re-run [`_graph_centrality_check.py`](_graph_centrality_check.py) → `connectivity_report.json`.

## Apply order

```
phase0 → phase1 → phase1b → phase2 → phase3
```

Sequential only — Phase 1 must exist before Phase 2 OXY (optional `review_run` tag on all new rels).

---

## Sidecar (recommended, not blocking apply)

Mirror Swiss pattern when building patches:

- `sidecar/claims.jsonl` — atomic claims from W01–W47 subset used in phases 1–3
- `sidecar/edge_evidence.jsonl` — claim_id ↔ rel id
- Donor-building claims (Borgerstein, CBR, …) → **sidecar only** until a donor links ≥2 existing seeds

---

## Skipped despite evidence (connectivity gate)

| Item | Evidence | Why skipped |
|---|---|---|
| Caserne, Boardwalk, Recypark rotordc | W09, W10, W19 | ≤1 spine connection each |
| Evere 14k m² site | W14–W16 | 2 actor links only |
| PREUSE partners (LIST, Mechelen, Lorient, La Fabrique) | W29–W32 | 1 programme edge each |
| Atelier 4/5, citydev, Van Hameren | W17, W20, W11 | peripheral |
| FCRBE 37-pilot project nodes | W34 | bulk; no spine density |

Full defer list: [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md).

---

## Cypher — post-apply bubble view

```cypher
UNWIND [
  'Rotor','rotordc','opalis','bellastock',
  'prog_fcrbe','prog_preuse',
  'p_multi_brussels_reuse_in_multi','p_oxy_centre_monnaie',
  'bw_generale_de_banque_brussels',
  'whitewood','immobel','city_of_utrecht'
] AS sid
MATCH (n {id: sid})
OPTIONAL MATCH (n)-[r]-(m)
WHERE m.id IN [
  'Rotor','rotordc','opalis','bellastock',
  'prog_fcrbe','prog_preuse',
  'p_multi_brussels_reuse_in_multi','p_oxy_centre_monnaie',
  'bw_generale_de_banque_brussels',
  'whitewood','immobel','city_of_utrecht'
]
RETURN n, r, m
```

Filter `r.review_run = 'rotor_dc_reuse_bubble_2026_06_05'` for strict import-only view.
