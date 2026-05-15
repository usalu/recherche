# Round 002 Plan — Controlled Vocabulary Review

**Date:** 2026-05-15
**Round type:** `VOCAB_REVIEW`
**Status of older plan docs:** partially stale — see §3.
**Authority:** this file supersedes the round-002 rows of
[`_neo4j/neo4j_iterative_review_plan/task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json)
where the two conflict. Strategy text in
[`00_MASTER_REVIEW_STRATEGY.md`](../neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md)
remains the conceptual reference.

---

## 1. Purpose

Normalize shared hub nodes so the graph becomes more connected and easier to
query. One controlled-vocabulary family per run. Output is a report + patch
JSONL + manifest per family, never a direct mutation of import payloads.

The high-level rhythm and contracts stay the same as before:

- chunking, severity levels, decision categories →
  [`02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md`](../neo4j_iterative_review_plan/plans/02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md)
- patch operations and idempotency requirements →
  [`05_PATCH_OUTPUT_CONTRACT.md`](../neo4j_iterative_review_plan/plans/05_PATCH_OUTPUT_CONTRACT.md)
- agent input/output expectations →
  [`06_AGENT_RUNBOOK.md`](../neo4j_iterative_review_plan/plans/06_AGENT_RUNBOOK.md)

What this file adds is the *current-repo grounding* those documents lack.

---

## 2. Repository state this plan is grounded in

The repo was restructured on 2026-05-15. The old plan was written before that
restructure and refers to paths that are now archived.

### 2.1 New source of truth for graph data

| Concern | Authoritative location |
|---|---|
| Live graph state | Neo4j database `mit-bestand` (queries below) |
| Reviewable import payload — projects | [`_neo4j/processed/projects/records/`](../processed/projects/records/) (75 `p_*.kg.jsonl`, 18 022 records total) |
| Reviewable import payload — vocab seed | [`_neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl`](../processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl) (385 records) |
| Reviewable import payload — vocab delta | [`_neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl`](../processed/projects/vocabulary/controlled_terms.merged.kg.jsonl) (56 records) |
| Reviewable import payload — actors | [`_neo4j/processed/actor_registry/actor_registry.canonical.kg.jsonl`](../processed/actor_registry/actor_registry.canonical.kg.jsonl) (588 unique node ids, 2 639 unique semantic relationships) |
| Intake contracts | [`_neo4j/contracts/project_batches_v1_1/`](../contracts/project_batches_v1_1/), [`_neo4j/contracts/actor_registry_v1_2/`](../contracts/actor_registry_v1_2/) |
| Archived raw inputs | [`_neo4j/intake/archive/2026-05-15_*`](../intake/archive/) |

**Do not read from the legacy paths.** The old `_neo4j/batch/` per-batch
exports and `_neo4j/new/` actor chunks are archived as inputs only; their
content has been superseded by the merged `_neo4j/processed/` artifacts and
the live Neo4j database.

### 2.2 What changed in the corpus

| Subject | Before 2026-05-15 | After 2026-05-15 |
|---|---|---|
| Projects | 97 | **75** (`batch_016`–`batch_020` removed; thin `batch_015` replaced with reviewed v2 set of 5 cases — see [`BATCH_015_020_CLEANUP_2026-05-15.md`](BATCH_015_020_CLEANUP_2026-05-15.md)) |
| `_neo4j/batch/` tree | live import source | archived under `_neo4j/intake/archive/2026-05-15_project_batches_legacy/` |
| `_neo4j/new/` actor chunks | live source | archived under `_neo4j/intake/archive/2026-05-15_actor_registry_seed/`, merged into `processed/actor_registry/` |
| Project records (per file) | per-batch folders | one file per project under `processed/projects/records/` |
| Live graph | included 016–020 nodes/rels | cleaned: late-only nodes and relationships removed, temp `a_*` duplicates from replay folded back |

### 2.3 What still needs explicit re-baselining

These artifacts were produced **before** the restructure and may now be wrong:

| Artifact | Status after restructure |
|---|---|
| [`round_001/global_audit_report.md`](round_001/global_audit_report.md) (1697 nodes, 14 028 rels, 25 dup ids) | **counts stale** — covered 20 batches; 5 are deleted |
| [`round_001/patches/*.jsonl`](round_001/patches/) | partially stale — some node ids no longer exist in the live graph |
| [`round_001_apply_test/needs_review.patch.jsonl`](round_001_apply_test/needs_review.patch.jsonl) (25 canonicalizations) | **must be re-verified against the current graph** before any is promoted |
| [`round_002_vocab_material/`](round_002_vocab_material/) | needs re-verification: built before 016–020 removal; the `mat_textil` finding likely still stands, but bauteilgruppe counts will have shifted |
| [`round_002_vocab_stadt_land/`](round_002_vocab_stadt_land/) | needs re-verification **and** the patch file contains mojibake (`K?nigreich`, `Br?ssel`, `D?nemark`) — regenerate in UTF-8 |
| [`round_003_query_donor_receiver/`](round_003_query_donor_receiver/) | out of scope here; flagged for the future query review |
| [`round_004_donor_receiver/`](round_004_donor_receiver/) | out of scope; not a freeze round despite the task-queue label |

---

## 3. Corrections to the earlier plan documents

| Issue | Where it appears | Correction |
|---|---|---|
| Round 2 task type | [`task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json) lists `PROJECT_CONTENT_REVIEW` for round_002 | Round 002 is `VOCAB_REVIEW`. Project content review is round 003. The whole task-queue file is off-by-one and should be regenerated. |
| Family count | `00_MASTER_REVIEW_STRATEGY.md` lists 8 families | The full list is 10 — `02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md` is correct. See §4 below. |
| Output paths | `02_CONTROLLED_VOCABULARY_REVIEW_PLAN.md` mentions `registry/canonical_nodes.patch.jsonl` | Not used. Actual output is `patches/controlled_vocabulary_<family>.patch.jsonl` per the existing `round_002_vocab_*/` folders. |
| Input source for vocab review | Older docs imply `_neo4j/batch/<batch>/controlled_terms.delta.jsonl` per batch | Use **live Neo4j** and `_neo4j/processed/projects/vocabulary/{controlled_vocabulary.seed,controlled_terms.merged}.kg.jsonl` + `_neo4j/processed/actor_registry/actor_registry.canonical.kg.jsonl`. The per-batch delta files are now archived and partially deleted. |
| Apply-tool capability | `05_PATCH_OUTPUT_CONTRACT.md` lists 13 operations | [`_scripts/apply_neo4j_review_patch.py`](../../_scripts/apply_neo4j_review_patch.py) only implements 6: `add_node`, `set_node_properties`, `canonicalize_node`, `set_property`, `add_rel`, `noop_reviewed`. **Missing:** `merge_node`, `delete_node`, `delete_rel`, `set_rel_properties`, `remove_node_properties`, `remove_rel_properties`, `rename_property`, `move_property`, `replace_rel_type`. |
| Reviewer script | `_scripts/run_neo4j_current_build_review.py` | Reads from the legacy `_neo4j/batch/` tree (see [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md)). Either update its `choose_current_batches()` to scan `_neo4j/processed/projects/records/` or treat its global-audit re-run as a step that needs a script update first (§6 step A). |

---

## 4. Family list and current status

Run **one family per agent run**. Cap at 100 controlled nodes / 250 patch ops
per family; split alphabetically or by sub-category if a family is larger.

| # | Family | Status | Notes |
|---|---|---|---|
| 1 | Material + Materialgruppe | **needs_reverification** | r002 artifact exists ([review.md](round_002_vocab_material/controlled_vocabulary_review_material.md), 1 LOW canon op for `mat_textil`). Re-query against current graph; bauteilgruppe counts changed. |
| 2 | Bauteiltyp + Bauteilebene | **todo** | — |
| 3 | Huerde + HuerdeKategorie | **todo** | Expected to surface tight parent-category clusters (`hk_umwelt_gesundheit`, etc). |
| 4 | Akteurrolle + Akteurtyp | **todo** | This family is the *vocab* `ar_*` / `at_*` nodes only — **not** the `a_*` actor-organization nodes. The latter belong to the actor registry workstream and were merged in [`actor_registry/merge_report.md`](../processed/actor_registry/merge_report.md). |
| 5 | Bauobjektrolle + Bauobjektklasse | **todo** | Vocab only — `bw_*` Bauwerk nodes are project content (round 003). |
| 6 | Status + WiederverwendungsArt | **todo** | — |
| 7 | Stadt + Land | **needs_reverification + UTF-8 regen** | r002 artifact exists ([review.md](round_002_vocab_stadt_land/controlled_vocabulary_review_stadt_land.md), 5 ops). Existing patch has mojibake; merge_node requires apply-tool extension before live apply. |
| 8 | Norm + PruefungNachweis + Leistungsanforderung | **todo** | `norm_sci_p427` from round_001 needs_review belongs here. |
| 9 | Methode + Rueckbauverfahren + Aufbereitungsverfahren | **todo** | Listed in 02-plan; missing from master strategy text. Include. |
| 10 | ZertifizierungBewertungssystem + Programm + Tool + Software | **todo** | Listed in 02-plan; missing from master strategy text. Include. |

### 4.1 Out-of-scope content nodes that came up in round 001

The round-001 `needs_review.patch.jsonl` lumped 25 canonicalization candidates
together. Only 6 of those are vocab-family nodes; the rest are project content.

| Type | Count | Examples | Where it belongs |
|---|---:|---|---|
| Vocab — Material | 1 | `mat_textil` | family 1 (already captured) |
| Vocab — Land | 4 | `land_belgien`, `land_deutschland`, `land_schweiz`, `land_vereinigtes_koenigreich` | family 7 |
| Vocab — Norm | 1 | `norm_sci_p427` | family 8 |
| Vocab — Stadt | 5 | `stadt_basel`, `stadt_berlin`, `stadt_bruessel`, `stadt_london`, `stadt_winterthur` | family 7 |
| **Content** — Akteur (`a_*`) | 11 | `a_arup`, `a_rotor`, `a_cleveland_steel_tubes`, … | **actor-registry track**, not vocab. Already partially folded by the 2026-05-15 actor-registry merge; re-verify against [`actor_registry/conflicts/node_conflicts.jsonl`](../processed/actor_registry/conflicts/node_conflicts.jsonl). |
| **Content** — Bauwerk (`bw_*`) | 3 | `bw_halle_2_ringberlin`, `bw_lysbuechel_parkhaus_basel`, `bw_tampere_1980s_office_donor` | **round 003** project content review. Some may have been removed with batch 016–020. |

**Rule of thumb for round 002:** if the node id prefix is in this list it is
vocab — otherwise defer.

```
ar_  at_  bok_  bor_  bw_… NO  bauaufgabe_  bauweise_  bausystem_  bteb_
btt_  btz_  fw_  hk_  h_   land_  ls_  lo_  mat_  mg_  meth_  norm_
nutz_  pn_  proz_  rb_   af_  rb_  rq_  rt_  rwa_  sad_  st_   stadt_
sw_  tk_  tw_  vt_   wa_  wi_  zb_
```

(Treat the list as guidance; canonical labels come from
[`_neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl`](../processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl)
and the `VOCAB_LABELS` set in
[`_scripts/run_neo4j_current_build_review.py:38-51`](../../_scripts/run_neo4j_current_build_review.py#L38-L51).)

---

## 5. Per-family runbook

For each family, produce **three artifacts** under
`_neo4j/review/round_002_vocab_<family>/`:

```text
controlled_vocabulary_review_<family>.md     # human-readable findings
patches/controlled_vocabulary_<family>.patch.jsonl
patch_manifest.json
```

### 5.1 Input queries (run against `mit-bestand`)

Adapt the label set per family. Snapshot template:

```cypher
// hub snapshot
MATCH (n:<Label>)
OPTIONAL MATCH (n)<-[r]-(:Bauteilgruppe)
RETURN n.id AS id, n.name AS name, count(DISTINCT r) AS inbound
ORDER BY inbound DESC, name;

// same-name duplicates
MATCH (n:<Label>)
WITH toLower(coalesce(n.name,'')) AS k, collect(n) AS nodes
WHERE size(nodes) > 1
RETURN k, [x IN nodes | x.id] AS ids, size(nodes) AS count;

// same-id property conflicts (cross-check against import payload, not just DB)
// see _neo4j/processed/projects/records/*.kg.jsonl + actor_registry.canonical.kg.jsonl
```

For families that include hierarchy (`Materialgruppe`, `HuerdeKategorie`),
also pull the parent relation type and report missing/wrong parents.

### 5.2 What to look for (unchanged from 02-plan, retained for ease)

```text
same id, different name
same concept, different ids
too-specific term that should be alias
too-generic term that hides useful distinction
term modeled as property but should be node
term modeled as node but should be scalar property
missing parent relationship
```

### 5.3 Allowed patch ops in this round

Round 002 should restrict itself to ops the apply tool already supports
(see §3 apply-tool gap):

```text
canonicalize_node    # primary tool — name + aliases
set_node_properties  # set canonical properties only
add_rel              # only to add parent links (HAT_MATERIALGRUPPE,
                     # HAT_HUERDEKATEGORIE, etc.)
noop_reviewed        # for items checked and deemed clean
```

`merge_node`, `delete_node`, `delete_rel`, `replace_rel_type`,
`set_rel_properties` are **not yet supported by the runner.** Emit them
into a sibling file `patches/controlled_vocabulary_<family>.deferred.jsonl`
with `severity: BLOCKED_ON_APPLY` and reference §6 step C below. Do not let
them stop the rest of the family's deterministic ops.

### 5.4 Severity (from
[`01_GLOBAL_TECHNICAL_AUDIT_PLAN.md`](../neo4j_iterative_review_plan/plans/01_GLOBAL_TECHNICAL_AUDIT_PLAN.md))

```text
BLOCKER  HIGH  MEDIUM  LOW  INFO
```

### 5.5 Human decision categories (from 02-plan)

```text
ACCEPT  REJECT  NEEDS_SOURCE_CHECK  DEFER
```

### 5.6 Per-family manifest skeleton

```json
{
  "review_round": "round_002_vocab_<family>",
  "task_type": "VOCAB_REVIEW",
  "scope": "<family label set>",
  "input_files": [
    "live Neo4j mit-bestand <family> query",
    "_neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl",
    "_neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl"
  ],
  "output_files": [
    "_neo4j/review/round_002_vocab_<family>/controlled_vocabulary_review_<family>.md",
    "_neo4j/review/round_002_vocab_<family>/patches/controlled_vocabulary_<family>.patch.jsonl"
  ],
  "summary": {"patch_operations": 0, "blockers": 0, "high": 0, "medium": 0, "low": 0, "info": 0},
  "apply_order": [],
  "human_review_required": true,
  "requires_apply_tool_support": []
}
```

### 5.7 Encoding rule

All patch and report files **must** be UTF-8 without BOM, LF line endings.
If writing from PowerShell, use `Out-File -Encoding utf8NoBOM` or write
through Python with `open(path, "w", encoding="utf-8", newline="\n")`.
The existing
[`round_002_vocab_stadt_land/patches/controlled_vocabulary_stadt_land.patch.jsonl`](round_002_vocab_stadt_land/patches/controlled_vocabulary_stadt_land.patch.jsonl)
fails this rule and must be regenerated before any apply.

---

## 6. Sequenced execution for the round

Run in this order. Each step is a separate commit.

### Step A — Re-baseline the global audit against the current graph

**Why.** The round-001 audit reflected 20 batches and 1697 nodes; we now
have 15 trusted batches and a different node set. Without a fresh audit
the per-family runs can't trust their "duplicates found" counts.

**How.**

1. Update [`_scripts/run_neo4j_current_build_review.py`](../../_scripts/run_neo4j_current_build_review.py)
   `choose_current_batches()` to read from `_neo4j/processed/projects/records/`
   (one project per file) or skip the batch-walk entirely and pull stats
   straight from Neo4j. Acceptance: the script no longer references
   `_neo4j/batch/` and exits 0 on current state.
2. Write outputs under `_neo4j/review/round_002_baseline/`:
   `global_audit_report.md`, `exports_vs_live_db_diff.md`,
   `patches/global_technical.patch.jsonl` (deterministic fixes only),
   and an updated `needs_review.patch.jsonl` containing only ids that
   still exist in the current graph.
3. Cross-check against [`actor_registry/conflicts/node_conflicts.jsonl`](../processed/actor_registry/conflicts/node_conflicts.jsonl)
   so the actor-registry track doesn't re-surface as round-002 noise.

Out: a fresh baseline that the family runs can quote.

### Step B — Re-verify the two families that were started early

**Why.** Both [`round_002_vocab_material/`](round_002_vocab_material/) and
[`round_002_vocab_stadt_land/`](round_002_vocab_stadt_land/) were generated
before the 2026-05-15 cleanup. Their bauteilgruppe / inbound counts and
their lists of duplicate ids may have shifted.

**How.**

- Material: re-run the snapshot queries (§5.1), regenerate the table in
  the review markdown, regenerate the patch JSONL. Expected: `mat_textil`
  canonicalization still stands; counts and aliases may change.
- Stadt + Land: regenerate the duplicate-name candidates from the current
  graph; regenerate the patch JSONL in UTF-8; route any `merge_node` ops
  to `.deferred.jsonl` until §6 step C lands.
  If a duplicate listed in the prior file no longer appears in the current
  graph, record that explicitly in the review markdown rather than silently
  dropping it.

Mark both folders' manifests with `"superseded_by": "<new file>"` rather
than overwriting in place, so the historical artifact stays auditable.

### Step C — Extend the apply tool with the missing ops

**Why.** A vocab round produces canonicalizations (covered) and genuine
merges (not covered). Without `merge_node` the user cannot collapse
`land_uk` → `land_vereinigtes_koenigreich`, `stadt_brussel` → `stadt_bruessel`,
etc. Without `delete_node` the round-002 cleanup of orphaned terms cannot
land. Without `set_rel_properties` `BELEGT_IN.datenqualitaet` cannot be
edited in place.

**Scope.** Add to [`_scripts/apply_neo4j_review_patch.py`](../../_scripts/apply_neo4j_review_patch.py):

- `merge_node` — relationship-preserving merge using `apoc.refactor.mergeNodes`
  in single-mode (preserve both sides), or a hand-rolled `MATCH` /
  `MERGE` / re-attach pattern if APOC is not available. Must move/union
  properties, union labels, redirect all relationships, then delete the
  duplicate. Idempotent: if the duplicate is gone, no-op.
- `delete_node` — guarded to refuse `Quelle` and `Datenqualitaet`
  per [`05_PATCH_OUTPUT_CONTRACT.md`](../neo4j_iterative_review_plan/plans/05_PATCH_OUTPUT_CONTRACT.md).
- `delete_rel`, `set_rel_properties`, `remove_node_properties`,
  `remove_rel_properties`, `rename_property`, `move_property`,
  `replace_rel_type` — straightforward Cypher; add together so the runner
  matches the patch contract.

**Acceptance.** Dry-run on `round_002_vocab_stadt_land/patches/...`
(regenerated in UTF-8) reports the relationship rewiring counts and
exits 0. Live apply still requires the existing confirmation phrase
`APPLY <patch-file-name> TO mit-bestand`.

### Step D — Run remaining 8 families, one per session

Order:

```
1. Bauteiltyp + Bauteilebene
2. Huerde + HuerdeKategorie
3. Akteurrolle + Akteurtyp
4. Bauobjektrolle + Bauobjektklasse
5. Status + WiederverwendungsArt
6. Norm + PruefungNachweis + Leistungsanforderung
7. Methode + Rueckbauverfahren + Aufbereitungsverfahren
8. ZertifizierungBewertungssystem + Programm + Tool + Software
```

Each family follows §5. Commit message style: three words, e.g.
`Vocab Bauteiltyp Review`.

### Step E — Roll up & hand off to round 003

When all 10 families are accepted:

1. Regenerate the baseline audit one more time (§6 step A repeated).
2. Update [`task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json)
   so round numbers match what was actually executed (round 002 = vocab,
   round 003 = project content, round 004 = query, round 005 = freeze).
3. Move the round 001 `needs_review` content nodes (`a_*`, `bw_*`) into
   round 003's queue.

---

## 7. Done definition for round 002

Round 002 is complete when all of the following hold:

- [ ] One review markdown + patch JSONL + manifest exists for each of
      the 10 families in §4.
- [ ] Each manifest's `summary` counters match its patch file.
- [ ] No patch file contains mojibake; every file is UTF-8 LF.
- [ ] All `canonicalize_node` and `add_rel` operations are dry-run clean
      against `mit-bestand`.
- [ ] All `merge_node` / `delete_node` / `replace_rel_type` operations
      live in `.deferred.jsonl` siblings until apply-tool §6 step C lands,
      after which they too are dry-run clean.
- [ ] The round-002 baseline audit reports the same node and relationship
      totals as the live `mit-bestand` (no missing endpoints,
      `forbidden_nodes = 0`, no `Fallbeispiel` / `Kennwert`).
- [ ] [`task_queue.recommended.json`](../neo4j_iterative_review_plan/task_queue.recommended.json)
      has been corrected.
- [ ] A final commit summarizes accepted/deferred counts per family.

---

## 8. Open questions for the user

These would unblock or sharpen the next steps. None of them have to be
answered before §6 step A starts.

1. Should `merge_node` use APOC (`apoc.refactor.mergeNodes`) or a
   hand-rolled MERGE flow? APOC is shorter; hand-rolled has no plugin
   dependency.
2. After §6 step B, should the original
   `round_002_vocab_material/` and `round_002_vocab_stadt_land/` files
   be retained as-is with a `superseded_by` pointer, or overwritten in
   place with the new versions and only kept in git history?
3. The legacy `_scripts/run_neo4j_current_build_review.py` — update in
   place for the new `_neo4j/processed/` layout, or replace with a new
   `run_neo4j_round002_baseline.py` and retire the old one with a deprecation
   note in [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md)?
4. For the 11 `a_*` actor canonicalizations from round 001: confirm they
   should be handled inside the actor-registry track (using
   [`processed/actor_registry/conflicts/node_conflicts.jsonl`](../processed/actor_registry/conflicts/node_conflicts.jsonl))
   and **not** mixed into family 4 (`Akteurrolle + Akteurtyp`)?

---

## 9. Pointers

- Schema and model assumptions: [`00_MASTER_REVIEW_STRATEGY.md`](../neo4j_iterative_review_plan/plans/00_MASTER_REVIEW_STRATEGY.md) §"Frozen model assumptions"
- Patch contract reminders: [`05_PATCH_OUTPUT_CONTRACT.md`](../neo4j_iterative_review_plan/plans/05_PATCH_OUTPUT_CONTRACT.md)
- Seed vocabulary inventory: [`controlled_vocabulary.seed.kg.jsonl`](../processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl)
- Live-graph batch cleanup record: [`BATCH_015_020_CLEANUP_2026-05-15.md`](BATCH_015_020_CLEANUP_2026-05-15.md)
- Legacy reading guide: [`LEGACY_LINEAGE_AUDIT.md`](LEGACY_LINEAGE_AUDIT.md)
