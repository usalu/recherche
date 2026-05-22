# France reuse bubble — connectivity-first import plan

**Run:** `2026-06-05_france_reuse_bubble`  
**Dossier:** `_knowledge/reuse_bubbles/france_reuse_bubble_combined.md`  
**Graph dossier node:** `q_research_france_reuse_bubble_combined_md`  
**Baseline:** `mit-bestand` — [`graph_probe.json`](graph_probe.json)

## Policy: no low-degree nodes

New nodes only if **≥4 edges to bubble seeds**. French marketplace actors **already exist** in graph (`cycle_up`, `backacia`, `mobius_reemploi`, `raedificare`) but are **taxonomy-only isolated** — enrich, do not duplicate.

**Bubble seeds:** `bellastock`, `opalis`, `Rotor`, `prog_fcrbe`, `prog_preuse`, `cstb`.

| Candidate | Seed edges | Verdict |
|---|---:|---|
| `cycle_up`, `backacia`, `mobius_reemploi`, `raedificare` | already in graph | **ENRICH** |
| `association_reavie` | bellastock via Stains project context | **ENRICH** (not new `reavie`) |
| `mineka`, `booster_du_reemploi`, `reavie` | ≤2 each | **SKIP** |
| `p_actlab`, `p_fabrique_du_clos`, demonstrators | ≤1–2 spine links | **SKIP** — sidecar |
| `prog_spirou`, `prog_life_waste2build` | programme nodes | **SKIP** — BELEGT_IN on `cstb`/`mobius` only |

---

## Already in graph — enrich only

| `id` | Role | Gap |
|---|---|---|
| `bellastock` | French hub; opalis/PREUSE/FCRBE linked | No French marketplace VERBUNDEN |
| `opalis` | EU spine (VERBUNDEN 4) | No `backacia` supplier edge |
| `cycle_up` | Marketplace + reconditioning | Isolated |
| `backacia` | Marketplace | Isolated |
| `mobius_reemploi` | SPIROU + IDF reconditioning | Only person edge |
| `raedificare` | Southern platform | Isolated |
| `cstb` | FCRBE participant | No SPIROU/reemploi BELEGT_IN |
| `Rotor`, `prog_*` | NWE bridge | France BELEGT_IN on bellastock |

---

## Target connectivity (post-apply)

| Node | Metric | Before | After |
|---|---|---:|---:|
| `bellastock` | ecosystem `VERBUNDEN` (excl. people) | 1 (`opalis`) | **≥4** |
| `opalis` | ecosystem `VERBUNDEN` | 4 | **≥5** (+ `backacia`) |
| `cycle_up` | spine `VERBUNDEN` | 0 | **≥4** |
| `backacia` | spine `VERBUNDEN` | 0 | **≥3** |
| `mobius_reemploi` | spine `VERBUNDEN` | 0 | **≥2** (+ `cstb`) |
| Stack | bellastock ↔ opalis ↔ backacia ↔ cycle_up ↔ mobius | broken | **connected** |

---

## Phases

1. **Phase 0** — dossier + French quellen  
2. **Phase 1** — EU–France spine + marketplace mesh  
3. **Phase 2** — `association_reavie` ↔ `bellastock` (Île-de-France co-project context)

**Review run:** `france_reuse_bubble_2026_06_05`
