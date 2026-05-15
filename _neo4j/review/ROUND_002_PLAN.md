# Round 002 Plan — Controlled Vocabulary Review

**Date:** 2026-05-15
**Round type:** `VOCAB_REVIEW`
**Status:** **final**
**Authority:** this file supersedes the round-002 rows of
[`_neo4j/neo4j_iterative_review_plan/task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json)
where the two conflict. Conceptual references in
[`00_MASTER_REVIEW_STRATEGY.md`](../neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md),
[`02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md`](../neo4j_iterative_review_plan/plans/02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md),
[`05_PATCH_OUTPUT_CONTRACT.md`](../neo4j_iterative_review_plan/plans/05_PATCH_OUTPUT_CONTRACT.md),
[`06_AGENT_RUNBOOK.md`](../neo4j_iterative_review_plan/plans/06_AGENT_RUNBOOK.md)
still apply — this file overrides their stale specifics.

---

## 1. Purpose

Normalize shared hub nodes so the graph becomes more connected and easier to
query. One controlled-vocabulary family per run. Output is a report + patch
JSONL + manifest per family, never a direct mutation of import payloads.

---

## 2. Repository state this plan is grounded in

The repo was restructured on 2026-05-15. Older planning documents predate it
and refer to paths that are now archived.

### 2.1 Source of truth for graph data

| Concern | Authoritative location |
|---|---|
| Live graph | Neo4j database `mit-bestand` |
| Project import payload | [`_neo4j/processed/projects/records/`](../processed/projects/records/) — 75 `p_*.kg.jsonl`, 18 022 records |
| Vocab seed | [`_neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl`](../processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl) — 385 records |
| Vocab delta (merged) | [`_neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl`](../processed/projects/vocabulary/controlled_terms.merged.kg.jsonl) — 56 records |
| Actor registry | [`_neo4j/processed/actor_registry/actor_registry.canonical.kg.jsonl`](../processed/actor_registry/actor_registry.canonical.kg.jsonl) — 588 nodes, 2 639 unique semantic relationships |
| Actor conflicts | [`_neo4j/processed/actor_registry/conflicts/node_conflicts.jsonl`](../processed/actor_registry/conflicts/node_conflicts.jsonl) |
| Intake contracts | [`_neo4j/contracts/{project_batches_v1_1, actor_registry_v1_2}/`](../contracts/) |
| Archived raw inputs | [`_neo4j/intake/archive/2026-05-15_*`](../intake/archive/) |

**Do not read from the legacy paths.** `_neo4j/batch/` and `_neo4j/new/` are
archived; their content has been superseded by `_neo4j/processed/` and by the
live Neo4j database.

### 2.2 Corpus changes on 2026-05-15

| Subject | Before | After |
|---|---|---|
| Projects | 97 | **75** (`016`–`020` removed; `015` replaced with reviewed v2 set of 5 cases — see [`BATCH_015_020_CLEANUP_2026-05-15.md`](BATCH_015_020_CLEANUP_2026-05-15.md)) |
| Per-batch folders | live | archived under `intake/archive/2026-05-15_project_batches_legacy/` |
| Actor chunks | live | merged into `processed/actor_registry/` |
| Live graph | included 016–020 | cleaned: late-only nodes/relationships removed; replay-only `a_*` duplicates folded to canonical ids |

### 2.3 Artifacts that need re-verification before reuse

These were produced before the restructure:

| Artifact | Status |
|---|---|
| [`round_001/global_audit_report.md`](round_001/global_audit_report.md) (1697 nodes, 14 028 rels, 25 dup ids) | **counts stale** |
| [`round_001/patches/`](round_001/patches/) | partially stale — some node ids no longer exist |
| [`round_001_apply_test/needs_review.patch.jsonl`](round_001_apply_test/needs_review.patch.jsonl) (25 canonicalizations) | **re-verify against current graph** before promoting |
| [`round_002_vocab_material/`](round_002_vocab_material/) | re-query: bauteilgruppe counts changed; `mat_textil` finding likely still stands |
| [`round_002_vocab_stadt_land/`](round_002_vocab_stadt_land/) | re-query **and** regenerate in UTF-8 — current patch has mojibake (`K?nigreich`, `Br?ssel`, `D?nemark`) |
| [`round_003_query_donor_receiver/`](round_003_query_donor_receiver/) | out of scope here |
| [`round_004_donor_receiver/`](round_004_donor_receiver/) | out of scope here |

---

## 3. Corrections to the earlier plan documents

| Issue | Location | Correction |
|---|---|---|
| Round 2 task type | [`task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json) lists `PROJECT_CONTENT_REVIEW` | Round 002 is `VOCAB_REVIEW`. Project content review is round 003. The whole task-queue file is off-by-one and must be regenerated (§6 step E). |
| Family count | `00_MASTER_REVIEW_STRATEGY.md` lists 8 families | The full list is 10 — `02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md` is correct. See §4. |
| Output paths | `02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md` mentions `registry/canonical_nodes.patch.jsonl` | Not used. Output is `patches/controlled_vocabulary_<family>.patch.jsonl` per the existing `round_002_vocab_*/` folders. |
| Input source for vocab review | Older docs imply per-batch `controlled_terms.delta.jsonl` | Use **live Neo4j** + the three processed JSONL files listed in §2.1. |
| Apply-tool capability | `05_PATCH_OUTPUT_CONTRACT.md` lists 13 ops | [`_scripts/apply_neo4j_review_patch.py`](../../_scripts/apply_neo4j_review_patch.py) currently implements only 6: `add_node`, `set_node_properties`, `canonicalize_node`, `set_property`, `add_rel`, `noop_reviewed`. The remaining 7 are added in §6 step C. |
| Reviewer script | [`_scripts/run_neo4j_current_build_review.py`](../../_scripts/run_neo4j_current_build_review.py) | Reads from the archived `_neo4j/batch/` tree (flagged in [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md)). It is **replaced** by a new `run_neo4j_round002_baseline.py` in §6 step A; the old script is left in place with a deprecation note appended to the legacy audit. |

---

## 4. Vocab vs content boundary

The seed file
[`controlled_vocabulary.seed.kg.jsonl`](../processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl)
and the project records pin down which prefixes are vocab and which are
content. **Round 002 touches only the vocab rows.**

### 4.1 Vocab labels and id prefixes (round-002 scope)

| Label | Prefix | Source |
|---|---|---|
| Akteurrolle | `ar_` | seed |
| Akteurtyp | `at_` | seed |
| Aufbereitungsverfahren | `av_` | seed |
| BauaufgabeIntervention | `bai_` | seed |
| Bauobjektklasse | `bok_` | seed |
| Bauobjektrolle | `bor_` | seed |
| Bausystem | `bsys_` | seed |
| Bauteilebene | `be_` | seed |
| Bauteiltyp | `bt_` | seed |
| Bauweise | `bauw_` | seed |
| Beschaffungsweg | `bweg_` | seed |
| Funktionswechsel | `fw_` | seed |
| Huerde | `h_` | seed |
| HuerdeKategorie | `hk_` | seed |
| Land | `land_` | seed + merged |
| Leistungsanforderung | `la_` | seed |
| Logistik | `log_` | seed |
| Material | `mat_` | seed |
| Materialgruppe | `mg_` | seed |
| Methode | `meth_` | seed |
| Norm | `norm_` | seed + project records |
| Nutzung | `nut_` | seed |
| Programm | `prog_` | seed |
| Prozessphase | `phase_` | seed |
| PruefungNachweis | `pr_` | seed |
| RechtlicheBedingung | `rb_` | seed + project records |
| Ressourcenquelle | `rq_` | seed |
| Rueckbauverfahren | `rv_` | seed |
| Schadstoff | `s_` | seed |
| Software | `software_` | merged |
| Stadt | `stadt_` | project records |
| Status | `status_` | seed |
| Tool | `tool_` | merged |
| Tragwerksprinzip | `tp_` | seed |
| Verbindungstechnik | `vt_` | seed + project records |
| WiederverwendungsArt | `wva_` | seed |
| Wirtschaft | `wi_` | seed |
| ZertifizierungBewertungssystem | `zbs_` | seed |

If a query for round 002 turns up an id whose prefix is **not** in this
table, it is content and must be deferred.

### 4.2 Content labels (out of scope for round 002)

| Label | Prefix | Route |
|---|---|---|
| Akteur | `a_` | actor-registry track (use [`conflicts/node_conflicts.jsonl`](../processed/actor_registry/conflicts/node_conflicts.jsonl)) |
| Bauteilgruppe | `bg_` | round 003 |
| Bauwerk | `bw_` | round 003 |
| Projekt | `p_` | round 003 |
| Quelle | `q_` | round 003 |
| Wiederverwendungskette | `wk_` | round 003 |

### 4.3 Where round-001's `needs_review` items land

| Type | Count | Route |
|---|---:|---|
| `mat_textil` | 1 | family 1 (already drafted) |
| `land_*` | 4 | family 7 |
| `norm_sci_p427` | 1 | family 8 |
| `stadt_*` | 5 | family 7 |
| `a_*` | 11 | **actor-registry track**, not family 4 |
| `bw_*` | 3 | **round 003**, not family 5 |

---

## 5. Family list, order, and status

Run **one family per agent run**. Cap at 100 controlled nodes / 250 patch ops
per family; split alphabetically if a family is larger.

| # | Family | Status |
|---|---|---|
| 1 | Material + Materialgruppe | **needs_reverification** (existing artifact under [`round_002_vocab_material/`](round_002_vocab_material/)) |
| 2 | Stadt + Land | **needs_reverification + UTF-8 regen** (existing artifact under [`round_002_vocab_stadt_land/`](round_002_vocab_stadt_land/)) |
| 3 | Bauteiltyp + Bauteilebene | todo |
| 4 | Huerde + HuerdeKategorie | todo |
| 5 | Akteurrolle + Akteurtyp | todo |
| 6 | Bauobjektrolle + Bauobjektklasse | todo |
| 7 | Status + WiederverwendungsArt | todo |
| 8 | Norm + PruefungNachweis + Leistungsanforderung | todo |
| 9 | Methode + Rueckbauverfahren + Aufbereitungsverfahren | todo |
| 10 | ZertifizierungBewertungssystem + Programm + Tool + Software | todo |

Families 1 and 2 are first because their artifacts already exist and need
re-baselining anyway; the remaining families run in the order shown.

---

## 6. Sequenced execution

Each step is a separate commit. Three-word commit subject style
(`Round 002 Plan`, `Baseline Vocab Audit`, `Material Vocab Reverify`, …).

### Step A — Re-baseline the global audit (replaces legacy reviewer)

**Why.** The round-001 audit reflects 20 batches and 1 697 nodes; we now
have 75 projects and a different node set. Without a fresh baseline no
family run can trust its duplicate counts.

**How.**

1. Add `_scripts/run_neo4j_round002_baseline.py`. Inputs:
   - the live Neo4j `mit-bestand` database (via `neo4j_env.resolve_connection()`);
   - `_neo4j/processed/projects/records/p_*.kg.jsonl`;
   - `_neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl`;
   - `_neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl`;
   - `_neo4j/processed/actor_registry/actor_registry.canonical.kg.jsonl`.
   It must reuse the schema enums loaded from
   `_neo4j/batch/contract/schemas/kg_jsonl_record_schema.json`
   (or the equivalent `_neo4j/contracts/project_batches_v1_1/schemas/`
   copy if available) and the vocab-label set in
   [`run_neo4j_current_build_review.py:38-51`](../../_scripts/run_neo4j_current_build_review.py#L38-L51).
2. Outputs under `_neo4j/review/round_002_baseline/`:
   ```text
   global_audit_report.md
   exports_vs_live_db_diff.md
   patch_manifest.json
   patches/global_technical.patch.jsonl   # deterministic fixes only
   needs_review.patch.jsonl               # only ids that still exist in the live graph
   ```
3. Append a deprecation note to [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md):
   `_scripts/run_neo4j_current_build_review.py` is superseded by
   `run_neo4j_round002_baseline.py`. Do not delete the old file; it is the
   reproducible record of the pre-cleanup audit.

**Acceptance.**

- The new script reads no path under `_neo4j/batch/` or `_neo4j/new/`.
- It exits 0 against the current graph.
- The report's totals match the live graph (no missing endpoints,
  `forbidden_nodes = 0`, no `Fallbeispiel`, no `Kennwert`).
- The 25 round-001 `needs_review` items are filtered down to only those
  whose ids still exist in the current graph, and each is annotated with
  which family or content track it belongs to per §4.

### Step B — Re-verify families 1 and 2

**Why.** Existing artifacts predate the 2026-05-15 cleanup.

**How.** For each of [`round_002_vocab_material/`](round_002_vocab_material/)
and [`round_002_vocab_stadt_land/`](round_002_vocab_stadt_land/):

1. Keep the existing files in place. Do not edit them. Set their
   `patch_manifest.json` `superseded_by` pointer to the new v2 file.
2. Create sibling v2 files in the same folder:
   ```text
   controlled_vocabulary_review_<family>_v2.md
   patches/controlled_vocabulary_<family>_v2.patch.jsonl
   patch_manifest_v2.json
   ```
3. v2 files use the queries in §7.1 against the current graph and obey §7.7
   (UTF-8 LF). Any `merge_node` op goes into a sibling
   `patches/controlled_vocabulary_<family>_v2.deferred.jsonl` until §6 step C
   lands; the active patch contains only ops the runner supports today.
4. v2 report records the diff vs v1: items dropped, items added, count
   changes.

**Acceptance.** v2 manifest's counters match its patch file; v2 patch is
UTF-8 LF; dry-run against `mit-bestand` is clean.

### Step C — Extend the apply tool with the missing ops

**Why.** Genuine duplicates (`land_uk` → `land_vereinigtes_koenigreich`,
`stadt_brussel` → `stadt_bruessel`, etc.) cannot be applied without
`merge_node`. The remaining contract ops are needed for parent-link
corrections, datenqualitaet edits, and the eventual round-003 work.

**Decision.** Hand-rolled implementation, no APOC dependency. APOC is not
currently used anywhere under `_scripts/`; adding a plugin requirement for
one feature would be a step backward.

**Scope.** Add to [`_scripts/apply_neo4j_review_patch.py`](../../_scripts/apply_neo4j_review_patch.py):

- `merge_node` — relationship-preserving merge. Algorithm: locate both
  nodes by id; for every incoming relationship of the duplicate, `MERGE`
  an equivalent one onto the canonical (preserving type, properties,
  direction); same for outgoing; union labels; union properties (canonical
  wins on conflict; loser's display becomes alias unless the patch supplies
  one); delete duplicate. Idempotent: if the duplicate is gone, no-op and
  report `noop_missing_source`.
- `delete_node` — refuses `Quelle`, `Datenqualitaet`, and any node with
  `BELEGT_IN` evidence still attached, per
  [`05_PATCH_OUTPUT_CONTRACT.md`](../neo4j_iterative_review_plan/plans/05_PATCH_OUTPUT_CONTRACT.md).
- `delete_rel`, `set_rel_properties`, `remove_node_properties`,
  `remove_rel_properties`, `rename_property`, `move_property`,
  `replace_rel_type` — straightforward Cypher; add together to keep the
  runner aligned with the contract.

**Acceptance.**

- Dry-run on the round_002_vocab_stadt_land v2 patch (after UTF-8 regen,
  §6 step B) reports the relationship-rewiring counts and exits 0.
- Live apply still requires the existing confirmation phrase
  `APPLY <patch-file-name> TO mit-bestand`.
- A short usage note for the new ops is appended to the script's docstring.

### Step D — Run remaining families 3–10

Each family follows §7. One agent run per family. Order: §5 rows 3–10
top-to-bottom. Commits: three-word subject (`Bauteiltyp Vocab Review`,
`Huerde Vocab Review`, …).

### Step E — Roll up

When all 10 families are accepted:

1. Re-run the baseline (§6 step A) one final time and commit a snapshot
   under `_neo4j/review/round_002_baseline/final/`.
2. Regenerate [`task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json)
   so round numbers reflect what was executed (round 002 = vocab,
   round 003 = project content, round 004 = query, round 005 = freeze).
3. Append a one-line `## Round 002 family runs` summary to
   [`00_MASTER_REVIEW_STRATEGY.md`](../neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md)
   with a link to this plan.
4. Move the 11 `a_*` round-001 canonicalizations into the actor-registry
   track (cross-reference `conflicts/node_conflicts.jsonl`) and the 3
   `bw_*` items into the round-003 queue.

---

## 7. Per-family runbook

For each family produce **three artifacts** under
`_neo4j/review/round_002_vocab_<family>/`:

```text
controlled_vocabulary_review_<family>.md     # human-readable findings
patches/controlled_vocabulary_<family>.patch.jsonl
patch_manifest.json
```

Plus, if any blocked ops exist (`merge_node` etc.):
`patches/controlled_vocabulary_<family>.deferred.jsonl`.

### 7.1 Input queries (run against `mit-bestand`)

Adapt per family. Template (`<Label>` = one row from §4.1, `<Prefix>` = its prefix):

```cypher
// hub snapshot
MATCH (n:<Label>)
WHERE n.id STARTS WITH '<Prefix>'
OPTIONAL MATCH (n)<-[r]-(x)
RETURN n.id AS id, n.name AS name,
       count(DISTINCT r) AS inbound,
       collect(DISTINCT labels(x)[0])[..5] AS sample_in_labels
ORDER BY inbound DESC, name;

// same-name duplicates
MATCH (n:<Label>)
WITH toLower(coalesce(n.name,'')) AS k, collect(n) AS nodes
WHERE size(nodes) > 1
RETURN k, [x IN nodes | x.id] AS ids, size(nodes) AS count;

// orphaned vocab (no inbound link from a content node)
MATCH (n:<Label>) WHERE NOT (n)<-[]-()
RETURN n.id, n.name;

// missing parent (for Materialgruppe / HuerdeKategorie / etc.)
MATCH (child:<ChildLabel>) WHERE NOT (child)-[:<ParentRel>]->(:<ParentLabel>)
RETURN child.id, child.name;
```

### 7.2 What to look for

```text
same id, different name
same concept, different ids
too-specific term that should be alias
too-generic term that hides useful distinction
term modeled as property but should be node
term modeled as node but should be scalar property
missing parent relationship
```

### 7.3 Allowed patch ops in round 002

Active patch JSONL (`patches/controlled_vocabulary_<family>.patch.jsonl`)
restricts itself to ops the runner supports **before** §6 step C lands:

```text
canonicalize_node    # primary tool — name + aliases
set_node_properties  # set canonical properties only
add_rel              # only to add parent links
                     # (HAT_MATERIALGRUPPE, HAT_HUERDEKATEGORIE, …)
noop_reviewed        # for items checked and deemed clean
```

After §6 step C lands, all 13 contract ops are available and the deferred
sibling files can be merged into the active patch.

### 7.4 Deferred sibling file

`patches/controlled_vocabulary_<family>.deferred.jsonl` holds ops that
need the extended runner: `merge_node`, `delete_node`, `delete_rel`,
`set_rel_properties`, `remove_node_properties`, `remove_rel_properties`,
`rename_property`, `move_property`, `replace_rel_type`. Each record
includes `"severity": "BLOCKED_ON_APPLY"` and a `"why_deferred"` field
referencing §6 step C.

### 7.5 Severity

```text
BLOCKER  HIGH  MEDIUM  LOW  INFO
```

### 7.6 Human decision categories

```text
ACCEPT  REJECT  NEEDS_SOURCE_CHECK  DEFER
```

### 7.7 Encoding rule

All review markdown and patch JSONL **must** be UTF-8 without BOM, LF line
endings. From PowerShell: `Out-File -Encoding utf8NoBOM`. From Python:
`open(path, "w", encoding="utf-8", newline="\n")`. The existing
[`round_002_vocab_stadt_land/patches/controlled_vocabulary_stadt_land.patch.jsonl`](round_002_vocab_stadt_land/patches/controlled_vocabulary_stadt_land.patch.jsonl)
fails this rule and is regenerated in §6 step B as `_v2`.

### 7.8 Manifest skeleton

```json
{
  "review_round": "round_002_vocab_<family>",
  "task_type": "VOCAB_REVIEW",
  "scope": "<family label set>",
  "input_files": [
    "live Neo4j mit-bestand <family> query",
    "_neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl",
    "_neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl",
    "_neo4j/review/round_002_baseline/global_audit_report.md"
  ],
  "output_files": [
    "_neo4j/review/round_002_vocab_<family>/controlled_vocabulary_review_<family>.md",
    "_neo4j/review/round_002_vocab_<family>/patches/controlled_vocabulary_<family>.patch.jsonl"
  ],
  "summary": {"patch_operations": 0, "blockers": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
  "deferred_operations": 0,
  "apply_order": [],
  "human_review_required": true,
  "requires_apply_tool_support": []
}
```

### 7.9 Example operations

```json
{"op":"canonicalize_node","id":"mat_textil","canonical_name":"Textil","aliases":["Textil / textile Fasern","Textil / Filz / textile Fasern"],"reason":"normalize textile material names","severity":"LOW"}
{"op":"add_rel","from":"h_schadstoffbelastung","type":"HAT_HUERDEKATEGORIE","to":"hk_umwelt_gesundheit","properties":{},"reason":"hurdle requires parent category","severity":"MEDIUM"}
{"op":"merge_node","from":"land_uk","to":"land_vereinigtes_koenigreich","reason":"duplicate country term","severity":"MEDIUM","why_deferred":"merge_node not yet supported by apply runner; see ROUND_002_PLAN §6 step C"}
```

---

## 8. Done definition

Round 002 is complete when **all** of the following hold:

- [ ] §6 step A baseline exists under `_neo4j/review/round_002_baseline/`
      and its audit numbers match the live graph.
- [ ] Each of the 10 families in §5 has a review markdown, an active patch
      JSONL, an (optional) deferred patch JSONL, and a manifest under
      `_neo4j/review/round_002_vocab_<family>/`.
- [ ] Families 1 and 2 carry both v1 and v2 artifacts; the v1 manifest's
      `superseded_by` field points at the v2 file.
- [ ] Every manifest's `summary` counters match its patch file.
- [ ] No file contains mojibake; every file is UTF-8 LF.
- [ ] Every active patch is dry-run clean against `mit-bestand`.
- [ ] Apply runner has been extended (§6 step C) and the deferred patches
      are dry-run clean as well.
- [ ] [`task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json)
      has been regenerated to reflect actual round numbering.
- [ ] Round-001 content items (`a_*`, `bw_*`) have been moved into the
      actor-registry track and the round-003 queue.
- [ ] [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md) carries the
      `run_neo4j_current_build_review.py` deprecation note.
- [ ] [`00_MASTER_REVIEW_STRATEGY.md`](../neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md)
      has the one-line round-002 summary linking back here.

---

## 9. Kickoff

Start with §6 step A. Commit subject: `Baseline Vocab Audit`. After that
lands, work through §6 steps B → C → D → E in order. Each step is
self-contained and produces commit-sized work.

---

## 10. Pointers

- Frozen graph-model assumptions: [`00_MASTER_REVIEW_STRATEGY.md`](../neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md) §"Frozen model assumptions"
- Patch contract: [`05_PATCH_OUTPUT_CONTRACT.md`](../neo4j_iterative_review_plan/plans/05_PATCH_OUTPUT_CONTRACT.md)
- Seed vocabulary: [`controlled_vocabulary.seed.kg.jsonl`](../processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl)
- Batch-cleanup record: [`BATCH_015_020_CLEANUP_2026-05-15.md`](BATCH_015_020_CLEANUP_2026-05-15.md)
- Legacy reading guide: [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md)
