# Manual Review Checkpoint — 2026-05-31 Project Reuse-Focus Cleanup
**Updated 2026-05-31 after user instructions to cascade-delete Careno, Eggshell, Granby + merge B4.**

**Nothing has been applied to Neo4j.** This is a dry-run artefact bundle for
human review. After review, follow the apply order in
[CONFLICT_ANALYSIS.md](CONFLICT_ANALYSIS.md) §D.

## Bundle contents

| File | Purpose |
|---|---|
| `schema_snapshot.json` | Live label / rel-type / status enum whitelist |
| `candidates.yaml` | Named candidate list |
| `resolution.jsonl` | Resolver output |
| `evidence.jsonl` | Reuse-evidence pull |
| `status_inventory.json` | Distinct status values per label |
| `duplicate_clusters.json` | Auto-detected name collisions |
| `cascade_targets.json` | **NEW.** Exclusive aux-node targets per delete project (Bauteilgruppe + DataIssue + Kennwert + Dossier) |
| `decision_table.csv` | **PRIMARY REVIEW DOC.** 27 rows |
| `projects.phaseA.patch.jsonl` | **91 ops**: 90 delete_node (cascade + projects) + 1 set_property (LYSP8 rename) |
| `projects.phaseB.patch.jsonl` | **8 merge_node ops** (was 7 — added B4 ETH Circular Construction student → prog_mas_dfab) |
| `projects.phaseA.delete_targets.txt` | 90 ids needing pre-delete snapshot |
| `projects.phaseB.merge_targets.txt` | 8 ids needing pre-merge snapshot |
| `projects.phaseC_strip_projekt.cypher` | REMOVE :Projekt on **6 canonicals** (added prog_mas_dfab) |
| `dependency_fixes/` | R1 query audit + R4/R5 doc advisories |
| `REGRESSION_AUDIT.md` | R1–R5 status |
| `CONFLICT_ANALYSIS.md` | Pre-flight checks |

## Net mutations proposed (after 2026-05-31 user update)

### Delete + cascade (5 projects, 90 nodes total)
Each project AND its project-exclusive auxiliary nodes (Bauteilgruppe,
DataIssue, Kennwert, project-scoped Dossier) are deleted together:

| Project | Cascade aux count | Surface (NOT cascaded) |
|---|---|---|
| `p_circle_house` | 12 (1 Kennwert + 11 DataIssue) | 1 Akteur (`kasper_guldager_jensen`) |
| `p_obk_27` | 6 (1 Dossier `q_obk_27_md` + 5 DataIssue) | 2 Akteure (`cyril_pressacco`, `thibaut_barrault`) |
| `p_careno_becircular` | 29 (3 Bauteilgruppe + 26 DataIssue) | 4: `tool_retile`, `brussels_capital_region`, `meth_wiederverwendungskriterien`, `bbri` |
| `p_eggshell_pavilion` | 11 (1 Bauteilgruppe + 10 DataIssue) | 1: `stadt_weil_am_rhein` |
| `p_granby_workshop` (override) | 27 (4 Bauteilgruppe + 22 DataIssue + 1 Dossier) | 7: 5 Akteure + 1 Bauwerk + 1 Stadt |

**Surface notes (NOT auto-deleted):** real-world entities — Akteure, Bauwerke,
Städte, vocab Methoden, Tools — even when they currently only connect to one
project. These are entities in their own right.

### Merge (8 ops)
- `p_interreg_nwe_fcrbe` → `prog_fcrbe`
- `p_re_use_hoefe` → `prog_re_use_hoefe`
- `p_rebridge_structural_reuse_project` → `prog_rebridge`
- `p_stuttgart_210` → `prog_stuttgart_210`
- `p_reallabor_be_ware` → `prog_reallabor_be_ware`
- `p_reallabor_b_e_ware` → `prog_reallabor_be_ware`
- `p_pavilion_circl_amsterdam` → `p_circl_abn_amro`
- **`p_eth_circular_construction_student_reuse_project` → `prog_mas_dfab`** (B4, user decision 2026-05-31)

### Rename (1 op)
- `p_lysp8.name = "LysP8 — LysBüchelStrasse 8 Reuse Pilot Basel"`

### Strip `:Projekt` (Phase C, 6 canonicals)
- `prog_fcrbe`, `prog_re_use_hoefe`, `prog_rebridge`, `prog_stuttgart_210`,
  `prog_reallabor_be_ware`, **`prog_mas_dfab`** (added for B4)

## Explicit user overrides (2026-05-31)

### O1. Granby Workshop — graph evidence overridden
Graph showed `NUTZT_BAUWERK=1, HAT_BAUTEILGRUPPE=4, HAT_METHODE=1` (reclaimed
proof = true). User instruction takes precedence: remove with cascade.
**Surface for review:** the donor `bw_granby_workshop_liverpool` (Bauwerk) is
NOT cascaded — it's an exclusive real-world building. Decide separately whether
to delete it.

### O2. Careno — open decision B3 resolved
Closed with "remove completely + cascade related aux".

### O3. Eggshell Pavilion — open decision B1 resolved
Closed with "remove completely + cascade related aux".

### O4. ETH Circular Construction student — open decision B4 resolved
Closed with "merge into `prog_mas_dfab`".

## Open decisions still pending

### U1. Up Sticks Dundee ETH MAS DFAB 2019 (`p_up_sticks_dundee`)
Marginal evidence (HAT_BAUTEILGRUPPE+METHODE+INTERVENTION+TEIL_VON_PROGRAMM,
REQUIRES_VERIFICATION_FOR=5, no donor/receiver/wva/nutzt). Same shape as
Eggshell. Currently `noop_reviewed`.

> **Question:** apply the same Eggshell treatment (delete + cascade) given
> the parallel shape? Or keep for now?

### U2. MedUni Campus Mariannengasse — no anchor entity
No `:Projekt`/`:Bauwerk` exists. Currently `absent_from_graph`. Decide whether
to create a donor `:Bauwerk` stub or accept the absence.

### U3. Surface entities — keep or delete?
For each delete cascade, the following exclusive real-world entities are NOT
cascaded by default:
- `kasper_guldager_jensen` (Circle House Akteur)
- `cyril_pressacco`, `thibaut_barrault` (OBK 27 Akteure)
- `tool_retile`, `brussels_capital_region`, `meth_wiederverwendungskriterien`, `bbri` (Careno)
- `stadt_weil_am_rhein` (Eggshell — Vitra/Werl Weil am Rhein city)
- `bw_granby_workshop_liverpool`, `stadt_liverpool`, `lewis_jones`, `will_shannon`, `granby_workshop_cic`, `granby_4_streets_clt`, `assemble` (Granby)

> **Question:** any of these should also be removed (e.g. Granby's
> `bw_granby_workshop_liverpool` Bauwerk if the donor building is no longer
> in scope)?

## Required amendment before Phase C
**C1.** Resolve the 16 production-tier hard-coded `MATCH (p:Projekt)` queries
in `dependency_fixes/hard_coded_projekt_query_audit.csv` (dashboard +
gap-audit + page-gen + image-pipeline). Phase C strips `:Projekt` from 6
canonicals; queries that count `:Projekt` will silently undercount.

## Required before Phase A
**A1.** Pre-apply snapshot via [_scripts/_snapshot_predelete.py](../../../_scripts/_snapshot_predelete.py)
of ALL 90 ids in `projects.phaseA.delete_targets.txt`. Without it, the 90
deletes are unrecoverable from this bundle alone.

## No-action zone (out of scope)
- Applying any patch.
- Editing legacy research / news inbox files.
- Reclassifying any node whose target label isn't in `schema_snapshot.json`.
- Touching `:Akteur`, `:Quelle`, source-level cleanup (covered by 2026-05-28 runs).
