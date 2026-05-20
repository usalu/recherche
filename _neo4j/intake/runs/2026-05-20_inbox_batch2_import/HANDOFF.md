# HANDOFF — batch2 v2 inbox import (2026-05-20)

**Audience:** Any agent (or human) coming to this work fresh.
**Status as of writing:** All 27 phases applied to `mit-bestand`. Graph state **2 580 nodes / 19 989 rels**. Pre-batch2 was 2 298 / 17 035. Net effect: **+282 nodes / +2 954 relationships**.

This document is your entry point. Read it once before touching anything.

---

## 1. What this run was

A single multi-day work block that:

1. **Ingested all 21 dossier files** from `_neo4j/intake/inbox/projects/` (BE/NL, DE/AT/CH, EU consortia, reuse platforms, teaching programmes, UK, plus root batch1.md) into the Neo4j graph `mit-bestand`.
2. **Restructured 6 stub Projekte into Programme** (FCRBE, MAS DFAB, RE-USE Höfe, BE-WARE, REBRIDGE, Stuttgart 210) and stripped the `:Projekt` label off them — they're programmes, not buildings.
3. **Created 61 new Bauteilgruppen** with full vocabulary coverage (BG-level: HAT_BAUTEILEBENE, HAT_STATUS, HAT_RESSOURCENQUELLE, HAT_BAUTEILTYP, HAT_MATERIALGRUPPE, HAT_WIEDERVERWENDUNGSART + 12 optional vocab rels including the new HAT_ZUSTANDSKLASSE and HAT_FUNKTIONSWECHSEL).
4. **Discovered 40 new Wiederverwendungsketten** automatically by querying donor-receiver Bauwerk patterns the graph already implied.
5. **Created/enriched 78 Akteure** (60 truly new + 18 existing enrichments), all with HAT_AKTEURROLLE + HAT_AKTEURTYP + GEHÖRT_ZU links.
6. **Added 8 new vocabulary nodes** where existing taxonomy had gaps (mat_messing, mat_kupfer, mat_holz_clt, mat_pcm_phasenwechsel, norm_sia_416, norm_sia_380_1, ak_oeffentliche_sichtbarkeit_lernort, ak_humanitarian_purpose).
7. **Corpus-wide hygiene**: source_scope is now non-NULL on every node (was missing on ~1 500); all consistency checks return 0.

---

## 2. Quick start — where to look

| Question | File |
|---|---|
| "What's the current graph state?" | [rollback.md](../../review/round_002_followup/rollback.md) — combined-effect table at the top |
| "What patches were applied in what order?" | [APPLY_ORDER.md](APPLY_ORDER.md) (phases 1-28 documented; phases 16, 17, 23-27 added later) |
| "What was originally planned?" | [PLAN_v2.md](PLAN_v2.md) (PLAN.md is the original; v2 is the authoritative version) |
| "What dossier said what?" | [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md) — per-dossier actor/BG/Bauwerk/Quelle inventory |
| "What live data was verified before patches were written?" | [pre_flight_validation.cypher](pre_flight_validation.cypher) + [pre_flight_results.json](pre_flight_results.json) |
| "What errors did we catch and how did we fix them?" | [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) — issue catalog with C1-C15 + O1-O14 + F1-F27 |
| "What new vocabulary nodes did we add and why?" | [NEW_NODE_SUGGESTIONS.md](NEW_NODE_SUGGESTIONS.md) — 8 nodes added in Phase 16 |
| "What's still open?" | [REMAINING_GAPS.md](REMAINING_GAPS.md) |
| "Which scripts to use for what?" | §6 below |
| "How to roll back?" | [rollback.md §Rollback procedure](../../review/round_002_followup/rollback.md) |

---

## 3. Repo navigation

```
e:/recherche/
├── _neo4j/
│   ├── README.md                    # Workspace overview (start here for the broader convention)
│   ├── contracts/                   # Input contracts / schemas (legacy reference)
│   ├── processed/                   # Cleaned import payloads from previous workflows
│   ├── intake/
│   │   ├── README.md                # Intake adapter docs
│   │   ├── inbox/projects/          # Raw drops (THIS RUN'S 21 dossiers still here — see §5)
│   │   ├── archive/                 # Preserved raw packages after processing
│   │   └── runs/
│   │       ├── 2026-05-19_inbox_projects_import/  # Earlier abandoned run (Plan 1)
│   │       └── 2026-05-20_inbox_batch2_import/    # THIS RUN — read HANDOFF here
│   │           ├── HANDOFF.md                    # ← you are here
│   │           ├── CLEANUP_PLAN.md
│   │           ├── REMAINING_GAPS.md
│   │           ├── PLAN.md (superseded)
│   │           ├── PLAN_v2.md                    # authoritative plan
│   │           ├── NEXT_STEPS.md (superseded)
│   │           ├── NEXT_STEPS_v2.md (superseded)
│   │           ├── APPLY_ORDER.md
│   │           ├── CORRECTIONS_2026-05-20.md
│   │           ├── NEW_NODE_SUGGESTIONS.md
│   │           ├── actor_extraction_per_dossier.md
│   │           ├── pre_flight_validation.cypher
│   │           ├── pre_flight_results.json
│   │           ├── apply_log.jsonl               # per-patch apply outcomes
│   │           ├── predelete_snapshot.json       # pre-Phase-1 snapshots
│   │           ├── predelete_snapshot_round2.json # pre-Phase-4c snapshots
│   │           └── predelete_snapshot_round3.json # pre-Phase-17 snapshots
│   └── review/
│       ├── backups/batch2_v2_pre_apply/      # full graph backup before applying any patch
│       └── round_002_followup/
│           ├── rollback.md                   # MASTER ledger (Phase A-R + batch2 v2 + 18-27)
│           ├── NAMING_AND_PROPERTIES_PLAN.md # naming conventions (Phase L-P era)
│           ├── PARKED_DECISIONS.md           # stub-Projekt + stub-Akteur disposition decisions
│           ├── STUB_AKTEUR_DECISIONS.md      # explicit per-Akteur decisions
│           ├── stub_research/GRAPH_SCHEMA.md # comprehensive node-label + rel-type reference
│           ├── patches/batch2/               # 50 patch files (all applied)
│           └── apply_reports/                # per-patch JSON+md apply reports
└── _scripts/
    ├── apply_neo4j_review_patch.py           # apply tool (modified during batch2 v2 — accepts Unicode rel types)
    ├── backup_neo4j_graph.py                 # logical JSONL backup
    ├── restore_neo4j_graph_backup.py         # restore from JSONL backup
    ├── neo4j_env.py                          # shared connection settings
    ├── _apply_batch2_v2_all.py               # orchestrator for the 34 sequenced patches
    ├── _run_cypher_file.py                   # multi-statement Cypher runner
    ├── _snapshot_predelete.py                # pre-delete safety snapshotter
    ├── _gap_survey.py                        # exhaustive gap survey
    ├── _generate_phase*.py                   # per-phase generator scripts (kept for reproducibility)
    ├── run_preflight_validation.py           # pre_flight_validation.cypher executor
    └── ...                                   # older non-batch2 scripts
```

---

## 4. Conceptual model — what's a Projekt, Programm, Bauwerk, etc.

The graph uses a German-language taxonomy. Future agents must respect these distinctions:

| Label | What it represents | NOT |
|---|---|---|
| `Projekt` | A specific reuse mission tied to a building or building component process. Has location (LIEGT_IN_STADT), receiver/donor Bauwerk(s), participants (BETEILIGT_AN). | NOT abstract programmes, organisations, or marketplaces. |
| `Programm` | A funding/research/teaching programme that hosts one or many Projekte. May span years and countries. | Doesn't get LIEGT_IN_STADT (too coarse-grained); rarely has BGs directly. |
| `Bauwerk` | A specific building or structure (donor, receiver, depot, storage). Has HAT_STATUS, HAT_BAUOBJEKTROLLE, HAT_BAUOBJEKTKLASSE, address. | Not an organisation; not an abstract concept. |
| `Bauteilgruppe` | A batch of reused components within a project. Carries the rich vocabulary (15+ rel types). | One BG per material/component class per project per phase. |
| `Akteur` | Person OR organisation involved in a project. Akteurtyp distinguishes (at_person / at_unternehmen / at_forschung_lehre / etc.). | Not a building, programme, or marketplace per se. |
| `Wiederverwendungskette` | An end-to-end reuse chain: donor Bauwerk → BG(s) → receiver Bauwerk. | Not a project. |
| `Quelle` | A bibliographic source. Either case_markdown (a dossier file) or external_reference (a URL) or actor_registry (CSV row) or controlled_vocab_seed (taxonomy file). | Not a project, building, or person. |

**Critical decision recorded during batch2 v2 (B1):** Programmes and Projekte are distinct. The 6 dual-labelled `:Programm:Projekt` nodes that emerged from merge operations had their `:Projekt` label stripped in Phase 23. From now on, only nodes with the literal `:Projekt` label and `node_role='full_projekt'` are "real" projects.

---

## 5. Status of `_neo4j/intake/inbox/projects/`

**STILL THERE, not yet archived.** Per the convention in [`_neo4j/intake/README.md`](../../README.md):

> After processing, move the untouched raw package into `archive/<run-id>/` and keep the generated reports in `runs/<run-id>/`.

All 21 dossier files in `_neo4j/intake/inbox/projects/` were processed in this run. They should be moved to:

```
_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
```

See [CLEANUP_PLAN.md §1](CLEANUP_PLAN.md) for the exact moves.

---

## 6. Tooling — which script does what

### Applied during batch2 v2 (durable, reusable)

| Script | Purpose |
|---|---|
| [`_scripts/apply_neo4j_review_patch.py`](../../../../_scripts/apply_neo4j_review_patch.py) | The canonical patch applier. Supports add_node / set_node_properties / canonicalize_node / set_property / add_rel / merge_node / delete_node / delete_rel / set_rel_properties / remove_node_properties / remove_rel_properties / rename_property / move_property / replace_rel_type. **Modified during batch2 v2**: `rel_type_safe()` regex now accepts Unicode rel types (so GEHÖRT_ZU works in merge redirects). |
| [`_scripts/backup_neo4j_graph.py`](../../../../_scripts/backup_neo4j_graph.py) | Full logical JSONL backup of the database. Run before any destructive phase. |
| [`_scripts/restore_neo4j_graph_backup.py`](../../../../_scripts/restore_neo4j_graph_backup.py) | Restore from a JSONL backup. |
| [`_scripts/neo4j_env.py`](../../../../_scripts/neo4j_env.py) | Shared connection settings (reads `.cursor/mcp.json`). |

### New scripts written for batch2 v2

| Script | Purpose | Status |
|---|---|---|
| [`_scripts/_apply_batch2_v2_all.py`](../../../../_scripts/_apply_batch2_v2_all.py) | Orchestrator that runs N patches in sequence with correct `--confirm` phrases. Handles Windows console UTF-8. | **Keep — reusable for batch3** |
| [`_scripts/_run_cypher_file.py`](../../../../_scripts/_run_cypher_file.py) | Run a multi-statement `.cypher` file (split on `;`, skip `//` comments). | **Keep — reusable** |
| [`_scripts/_snapshot_predelete.py`](../../../../_scripts/_snapshot_predelete.py) | Snapshot rels + properties of any set of node ids before delete/merge. | **Keep — safety tool** |
| [`_scripts/_gap_survey.py`](../../../../_scripts/_gap_survey.py) | Exhaustive consistency-check survey. Returns counts that should be 0. | **Keep — diagnostic** |
| [`_scripts/run_preflight_validation.py`](../../../../_scripts/run_preflight_validation.py) | Executes `pre_flight_validation.cypher` block-by-block; emits JSON. | **Keep — diagnostic** |
| [`_scripts/_generate_phase*.py`](../../../../_scripts/) (10 files) | One-shot generators that produced each Phase N's JSONL patch from compact spec tables. | **Keep for reproducibility — historic record of how each phase was built** |
| [`_scripts/_probe_schema.py`](../../../../_scripts/_probe_schema.py) | Quick rel-type probe between specific label pairs. | **Keep — small diagnostic** |
| [`_scripts/_test_graph_queries.py`](../../../../_scripts/_test_graph_queries.py) | Block-by-block Cypher test runner. | **Keep — diagnostic** |

### Typical workflow for a future agent

1. **Reading the graph:** `python _scripts/_gap_survey.py` — quick health check.
2. **Designing a new patch batch:** run `python _scripts/run_preflight_validation.py --cypher <file>.cypher --out <results>.json` against your queries first, write the patch, then dry-run with `python _scripts/apply_neo4j_review_patch.py --patch <file>.patch.jsonl` (without `--confirm`).
3. **Applying live:** add `--confirm "APPLY <filename> TO mit-bestand"` to the same command.
4. **Before destructive ops:** `python _scripts/_snapshot_predelete.py --ids "x,y,z" --out <snapshot>.json`.
5. **Multi-statement Cypher:** `python _scripts/_run_cypher_file.py --cypher <file>.cypher`.

---

## 7. Decisions log (D1-D16 + B1-B4 from batch2 v2)

Recorded for context. Future agents should treat these as binding unless they have an explicit reason to revisit.

### Pre-batch2 decisions (from PLAN_v2.md)

| # | Decision | Rationale |
|---|---|---|
| D1 | Circl canonical = `p_circl_abn_amro` (Pavilion merged in) | PARKED_DECISIONS line 47 + dossier evidence consolidated on canonical |
| D2 | `Plattform` label dropped | RCMI/REFAIR dossiers explicitly reject Plattform classification |
| D3 | 4 dossier-unverified Programms stay as Projekt | Dossiers say `identified_programme: no` (Architecture of Reuse BXL, Vandkunsten, ZHAW, Reuse Logistics) |
| D4 | ETH stub merged into `prog_mas_dfab` | Verified Programm; ETH parent stub absorbed |
| D5 | Reuse Logistics stays Projekt; new parent `prog_urban_bricolage` | SNSF subproject |
| D6 | UMAR + ELEMENTA brought in scope from batch 1.md | Original Plan 2 had only Schärenmoosstrasse |
| D7 | RE_USE Höfe drops "Wien" from name | Dossier explicit "Vienna location unverified" |
| D8 | `wk_*` prefix for new ketten | Live live state had 44 with `wk_*` vs 19 `k_*` |
| D9 | `norm_*` prefix preserved | Existing 30 Norm nodes all `norm_*` |
| D10 | Werner Sobek canonical = `Werner_Sobek` | Higher-degree node wins |
| D11 | Rotor canonical = `Rotor` | Higher-degree node wins |
| D12 | Zirkular canonical = `zirkular` | Higher-degree node wins |
| D13 | RotorDC canonical = `rotordc` | Higher-degree node wins |
| D14 | `bw_ubs_altstetten` (not bw_ubs_datacenter_altstetten) | Match Plan 1's shorter id |
| D15 | 8 new vocab nodes (Phase 16) | NEW_NODE_SUGGESTIONS — existing vocab insufficient |
| D16 | 3 multi-value placeholders (mg/bt/mat_mehrere) | NAMING_AND_PROPERTIES_PLAN convention |

### Post-apply user decisions (B1-B4 from this session)

| # | Decision | Effect |
|---|---|---|
| B1 | Strip `:Projekt` label from 6 dual-label `:Programm:Projekt` nodes | Phase 23 applied; 6 nodes now `:Programm` only |
| B2 | Keep German characters (umlauts) in rel type names | No GEHÖRT_ZU → GEHOERT_ZU rename |
| B3 | Organisations operating software/marketplaces don't need to be tied to a Projekt | Accept `la_fabrique_de_bordeaux_metropole` etc. as orphan-without-project; "platform operators" is a valid status |
| B4 | Leave `planned`-status `counts_as_*` blank | Phase 19 already skipped these |

### Definition of "what is a Projekt" (B3 expanded)

> "Projects are related to a mission of building with Reuse whether planning, research, or engineering, etc. What is NOT a project is Baubörse, software or organisation."

This is the operational rule for future agents:

- **Projekt = mission with construction outcome** (planning, research-pilot-with-built-output, design study, etc.)
- **NOT Projekt:**
  - Marketplace operators (Baubörse, Bauteilbörse Basel) → Akteur
  - Software / digital platforms (REFAIR, RCMI, Concular) → Software or Tool
  - Pure organisations without a single project → Akteur
  - Research programmes / teaching tracks → Programm
  - Funding instruments → Programm

---

## 8. Schema invariants now enforced

Every check below should return 0. Future patch batches must preserve these.

```cypher
// Hygiene
MATCH (n) WHERE n.source_scope IS NULL RETURN count(n); // EXPECTED: 0
MATCH ()-[r]->() WHERE r.id IS NULL RETURN count(r);     // EXPECTED: 0

// Case-specific nodes must have BELEGT_IN
MATCH (n) WHERE any(l IN labels(n) WHERE l IN ['Projekt','Bauteilgruppe','Bauwerk','Wiederverwendungskette','Stadt'])
  AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) } RETURN count(n); // EXPECTED: 0

// Bauteilgruppe mandatory rels
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUTEILEBENE]->() } RETURN count(bg);     // EXPECTED: 0
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() } RETURN count(bg);            // EXPECTED: 0
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_RESSOURCENQUELLE]->() } RETURN count(bg);  // EXPECTED: 0
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUTEILTYP]->() } RETURN count(bg);        // EXPECTED: 0
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_MATERIALGRUPPE]->() } RETURN count(bg);    // EXPECTED: 0
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_WIEDERVERWENDUNGSART]->() } RETURN count(bg); // EXPECTED: 0

// Bauwerk mandatory rels
MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_STATUS]->() } RETURN count(bw); // EXPECTED: 0

// Stadt → Land
MATCH (s:Stadt) WHERE NOT EXISTS { (s)-[:LIEGT_IN_LAND]->() } RETURN count(s); // EXPECTED: 0

// Wiederverwendungskette → Quelle
MATCH (k:Wiederverwendungskette) WHERE NOT EXISTS { (k)-[:BELEGT_IN]->() } RETURN count(k); // EXPECTED: 0

// Funktionswechsel rule: alte ≠ neue ⇒ HAT_FUNKTIONSWECHSEL must exist
MATCH (bg:Bauteilgruppe) WHERE bg.alte_funktion IS NOT NULL AND bg.neue_funktion IS NOT NULL
  AND bg.alte_funktion <> bg.neue_funktion AND NOT EXISTS { (bg)-[:HAT_FUNKTIONSWECHSEL]->() }
RETURN count(bg); // EXPECTED: 0

// No fabricated rel types
MATCH ()-[r]->() WHERE type(r) IN ['HAT_SOFTWARE','HAT_TOOL','HAT_NORM','LIEFERT_MATERIAL_AUS','VERBUNDEN_MIT','LIEGT_IN']
RETURN count(r); // EXPECTED: 0

// No dual :Programm:Projekt labels (per B1 decision)
MATCH (n:Programm:Projekt) RETURN count(n); // EXPECTED: 0
```

`python _scripts/_gap_survey.py` runs these and a dozen more.

---

## 9. Tooling gotchas future agents will hit

### 9.1 — Apply tool's `--confirm` phrase

Every live mutation requires `--confirm "APPLY <filename> TO mit-bestand"` where `<filename>` is the basename of the patch file. The orchestrator [`_apply_batch2_v2_all.py`](../../../../_scripts/_apply_batch2_v2_all.py) handles this automatically.

### 9.2 — Planner evaluates against initial state, not post-prior-op state

The patch planner does NOT re-plan ops as previous ops in the same patch execute. So if you have:

```jsonl
{"op": "add_node", "id": "foo", ...}
{"op": "add_rel", "from": "foo", "to": "bar", ...}
```

The second op will **fail at plan time** with `missing_endpoint` because `foo` doesn't exist yet at plan time. Split into two patches if you need dependent ops.

This bit us in Phases 1d-2a/2b, 4c, 6b. The orchestrator handles it by running each patch separately.

### 9.3 — `delete_node` refuses if BELEGT_IN edges attached

Safety guard in the apply tool. To delete a node:
1. First emit `delete_rel` for each BELEGT_IN edge to a Quelle.
2. Then emit `delete_node` in a SECOND patch (because of §9.2).

See Phases 1a + 1a-2 for the pattern.

### 9.4 — `merge_node` UNIONS labels (doesn't replace)

If you merge `(x:Projekt)` into `(y:Programm)`, the result is `(y:Programm:Projekt)`. If you want strict label-replacement, use direct Cypher with `REMOVE n:Projekt` afterward (see Phase 23).

### 9.5 — `merge_node` rewrites `r.id` outbound from source

The apply tool rewrites `r_<from>__<TYPE>__<x>` patterns automatically for outgoing rels. For incoming rels it MERGE-deduplicates. See `apply_neo4j_review_patch.py:777-820`.

### 9.6 — Unicode rel types in apply tool

The regex was tightened from ASCII-only to allow Unicode word characters (so `GEHÖRT_ZU` works in merge_node). If you ever roll the apply tool back, you'll need to patch this again — see `apply_neo4j_review_patch.py:134-138`.

### 9.7 — Windows console + UTF-8

If you `print()` text with non-ASCII characters on a Windows console with default cp1252 encoding, Python crashes. Set `sys.stdout.reconfigure(encoding='utf-8')` at the top of every script that prints German/French names. The orchestrator and survey scripts do this.

---

## 10. The 4 KEEP-STUB Akteure that remain orphans (deg ≤ 1)

Per `PARKED_DECISIONS.md` these are intentionally kept until natural references emerge:

| Akteur | Why kept |
|---|---|
| `glasfischer_glastec` | Swiss/German glass-tech company; real entity; no dossier evidence yet |
| `heinrich_boell_stiftung` | German foundation; linked in Phase 18 to BE-WARE programme (now deg 2) |
| `koimo_development` | Berlin developer; linked in Phase 18 to BE-WARE (now deg 2) |
| `mehr_als_wohnen` | Zurich coop Bauherr; linked in Phase 18 to LysP8 as inferred kitchen donor (now deg 2) |

These are not bugs — they're parking spots until evidence arrives.

---

## 11. Backups

| Backup | When | Path | Still valid as rollback target? |
|---|---|---|---|
| Pre-batch2 v2 full | 2026-05-20 morning | `_neo4j/review/backups/batch2_v2_pre_apply/` | **YES** — restores to 2 298 / 17 035 |
| Older Phase A-R backups | 2026-05-15-19 | `_neo4j/review/backups/phase_*_pre_apply/` | yes for their respective phases |

To restore the pre-batch2 state:
```bash
python _scripts/restore_neo4j_graph_backup.py --backup-dir _neo4j/review/backups/batch2_v2_pre_apply
```

---

## 12. What's NOT in this run

- **Dossiers under `_neo4j/intake/archive/`** — those are LEGACY archives from 2026-05-15. This run's inbox is still in `_neo4j/intake/inbox/projects/` and needs to be archived (see CLEANUP_PLAN.md).
- **No new dossier research was done during batch2 v2.** Every fact in the graph derived from the 21 inbox dossiers OR from pattern-discovery against the existing graph (Phase 20, Phase 24, Phase 26).
- **The `_archive/research/` folder is LEGACY**. Per `AGENTS.md`, it must not be silently consumed as canonical.

---

## 13. Read these next

1. [REMAINING_GAPS.md](REMAINING_GAPS.md) — what's still open + suggested next batch
2. [CLEANUP_PLAN.md](CLEANUP_PLAN.md) — repo housekeeping after batch2 v2
3. [rollback.md](../../review/round_002_followup/rollback.md) — full ledger of every applied phase

If you're picking up this work cold: run `python _scripts/_gap_survey.py` first to see live state, then read these three documents in order.

---

**End of HANDOFF.md.** Updated 2026-05-20.
