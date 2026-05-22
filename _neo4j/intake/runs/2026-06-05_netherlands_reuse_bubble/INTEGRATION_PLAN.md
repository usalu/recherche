# Netherlands reuse bubble — connectivity-first import plan

**Run:** `2026-06-05_netherlands_reuse_bubble`  
**Dossier:** `_knowledge/reuse_bubbles/netherlands_reuse_bubble_combined.md`  
**Graph dossier node:** `q_research_netherlands_reuse_bubble_combined_md`  
**Baseline:** `mit-bestand` — [`graph_probe.json`](graph_probe.json)

## Policy: no low-degree nodes

New nodes only if **≥4 edges to bubble seeds**. Existing Dutch actors **enrich only** — do not duplicate `Superuse_Studios` vs `superuse_studios_2012architecten` or `new_horizon` vs `new_horizon_urban_mining`.

**Bubble seeds:** `superuse_studios_2012architecten`, `new_horizon_urban_mining`, `madaster`, `insert_marketplace`, `city_of_utrecht`.

| Candidate | Seed edges | Verdict |
|---|---:|---|
| `superuse_studios_2012architecten`, `new_horizon_urban_mining`, `madaster`, `insert_marketplace` | already in graph | **ENRICH** |
| `repurpose` (+ Madopt platform) | superuse, new_horizon, insert, madaster | **IMPORT** (phase 2) |
| `new_horizon` (duplicate stub) | alias of UM | **SKIP** — use `new_horizon_urban_mining` |
| `cirkelstad`, `platform_cb23` | policy/standards | **SKIP** — BELEGT_IN sidecar only |
| `madopt` as separate node | same org as repurpose | **SKIP** — fold into `repurpose` |
| `p_circl`, `p_de_ceuvel`, demonstrators | ≤2 spine links each | **SKIP** |
| §9–§10 matrix scores | dossier | **sidecar** |

---

## Target connectivity (post-apply)

| Node | Metric | Before | After |
|---|---|---:|---:|
| `superuse_studios_2012architecten` | spine `VERBUNDEN` | 0 | **≥4** |
| `new_horizon_urban_mining` | spine `VERBUNDEN` | 0 | **≥4** |
| `madaster` | Dutch mesh `VERBUNDEN` (excl. concular-only) | 1 (concular) | **≥4** |
| `insert_marketplace` | spine `VERBUNDEN` | 0 | **≥3** |
| Stack | superuse ↔ new_horizon ↔ insert ↔ madaster | broken | **connected** |

---

## Phases

1. **Phase 0** — dossier + Dutch quellen  
2. **Phase 1** — harvest / urban-mining / marketplace / passport mesh  
3. **Phase 2** — `repurpose` (Madopt operator) demand-driven layer  

**Review run:** `netherlands_reuse_bubble_2026_06_05`
