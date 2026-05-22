# Germany reuse bubble — connectivity-first import plan

**Run:** `2026-06-05_germany_reuse_bubble`  
**Dossier:** `_knowledge/reuse_bubbles/germany_reuse_bubble_v1.md`  
**Graph dossier node:** `q_research_germany_reuse_bubble_v1_md`  
**Baseline:** `mit-bestand` — [`graph_probe.json`](graph_probe.json) (2026-06-06)

## Policy: no low-degree nodes

New `:Akteur` / `:Projekt` / `:Tool` nodes only if they add **≥4 edges to bubble seeds**, or close a broken tier-1 spine gap.

**Bubble seeds:** `concular`, `software_restado`, `circular_structural_design`, `bauteilboerse_bremen`, `madaster`, `madaster_epea`, `tu_berlin`.

| Candidate | Seed edges | Verdict |
|---|---:|---|
| **`bauteilboerse_hannover`** | concular, software_restado, bauteilboerse_bremen, circular_structural_design (teilweise) | **IMPORT** |
| **`haus_der_materialisierung`** | tu_berlin, bauteilboerse_bremen, bauteilboerse_hannover, madaster (Berlin practice cluster teilweise) | **IMPORT** |
| `material_mafia` | hdM only (~1) | **SKIP** — sidecar |
| `circular_berlin` | Berlin NGO; no spine density | **SKIP** |
| `p_berlin_txl` | concular (~1), madaster teilweise | **SKIP** |
| `p_rathaus_korbach` | UMI/madaster indirect (~1) | **SKIP** |
| Concular project cases (ICE, Leipzig, Forum, …) | ≤1 each | **SKIP** — sidecar |
| `tool_din_spec_91484` / `91525` | 2–3 seeds each | **SKIP new node** — BELEGT_IN enrich on concular + CDS |

---

## Already in graph — enrich only

| `id` | Role | Phase |
|---|---|---|
| `concular` | Digital/market spine; thin ecosystem VERBUNDEN (1 person) | 1, 2 |
| `software_restado` | Marketplace layer; BETRIEBEN_VON concular | 1 |
| `circular_structural_design` | Engineering/PDA partner | 1 |
| `bauteilboerse_bremen` | Physical depot; isolated | 1, 2 |
| `madaster`, `madaster_epea` | Passport/data layer | 1 |
| `tu_berlin` | HdM research anchor | 2b |
| `tool_rcmi`, `dominik_campanella` | RCMI cluster | no change |

**Do not duplicate:** `software_restado` ↔ `concular` BETRIEBEN/NUTZT_SOFTWARE mesh — enrich only.

---

## Target connectivity (post-apply)

| Node | Metric | Before | After |
|---|---|---:|---:|
| `concular` | ecosystem `VERBUNDEN` (excl. people) | 0 | **≥4** |
| `bauteilboerse_bremen` | `VERBUNDEN` to spine | 0 | **≥2** |
| `software_restado` | `BELEGT_IN` | 0 | **≥2** |
| Stack | concular ↔ restado ↔ bremen ↔ hannover ↔ CDS | broken | **connected** |

---

## Phased patches

### Phase 0 — sources + dossier (~22 quellen)

### Phase 1 — concular ecosystem spine

- `concular` BELEGT_IN (homepage, urban-mining, ECESP)
- `concular` ↔ `circular_structural_design` `VERBUNDEN` (Green-AI Hub)
- `concular` ↔ `madaster`, `madaster_epea` `VERBUNDEN` (Heidelberg/Huthmacher portfolio)
- `concular` ↔ `bauteilboerse_bremen` `VERBUNDEN` (DE marketplace layer)
- `software_restado` BELEGT_IN (ECESP, über-restado)
- `bauteilboerse_bremen` BELEGT_IN ×3
- `circular_structural_design` BELEGT_IN
- `madaster` BELEGT_IN madaster.de

### Phase 2 — `bauteilboerse_hannover`

**One new node:** `bauteilboerse_hannover`

### Phase 2b — `haus_der_materialisierung`

**One new node:** `haus_der_materialisierung` — links `tu_berlin`, peer Bauteilbörsen, Berlin practice context

---

## Apply order

```
phase0 → phase1 → phase2 → phase2b
```

**New nodes: 2.** Off-graph: §7–§8 interpretive matrix, Concular-only quantities, material_mafia as separate node.

See [`DEFERRED_NO_EVIDENCE.md`](DEFERRED_NO_EVIDENCE.md).
