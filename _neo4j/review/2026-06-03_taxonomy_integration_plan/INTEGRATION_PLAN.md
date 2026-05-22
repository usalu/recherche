# Reuse Taxonomy Integration Plan

**Generated:** 2026-06-03
**Source batches:** [\_neo4j/intake/inbox/research/new taxonomy edit/](../../intake/inbox/research/new%20taxonomy%20edit/) (2,240 row-level claims across 79/81 projects)
**Target graph:** `mit-bestand` (39,165 nodes / 80,135 rels)
**Companion docs:**
- [SEMANTIC_CONFLICT_AUDIT.md](SEMANTIC_CONFLICT_AUDIT.md) — every label/rel/ID conflict and its proposed resolution
- [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md) — **authoritative source** on which old-vocab edges DELETE vs MIGRATE (supersedes Phase 6 in earlier drafts)
- [vocab_connection_analysis.txt](vocab_connection_analysis.txt) — raw output of [analyze_old_vocab_connections.py](analyze_old_vocab_connections.py)
- [verify_integration.cypher](verify_integration.cypher) — read-only verification suite (Phase 7)
- Reference: [reuse_taxonomy_short_retirement_prompt_with_scope_v3.md](../../intake/inbox/research/new%20taxonomy%20edit/reuse_taxonomy_short_retirement_prompt_with_scope_v3.md)

---

## Goals

1. Land new evidence-backed taxonomy (`Wiederverwendungsergebnis`, `Wiederverwendungsort`, batch-level outcome/origin/location/method/Rückbau/Aufbereitung mappings) onto the live graph.
2. Follow existing schema conventions exactly — id prefixes, edge property contract, uniqueness constraints, label-agnostic anchor MATCH.
3. **Zero duplicates** at the `:Projekt`, `:Bauteilgruppe`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Ressourcenquelle` levels.
4. **Hard-delete** all legacy vocab nodes. **No `:*_Legacy` labels** remain after integration. The graph's vocab axes contain only batch-canonical nodes.
5. **Targeted migration** for the small set of upstream edges that batches don't re-supply (Akteur/Software/Norm/ReuseRule/Materialdepot/Programm — 115 edges total) — these are reattached to the new canonical so nothing breaks.
6. Every step rollback-able via `review_run` tag.
7. End-to-end verifiable by a read-only Cypher test suite that can be re-run any time.

---

## Phase 0 — Pre-flight (read-only)

**P0.1 Snapshot the current graph.**
Export to `_neo4j/review/2026-06-03_taxonomy_integration_plan/snapshot_pre_integration/`:
- full node + rel counts by label / type
- all `:WiederverwendungsArt`, `:Ressourcenquelle`, `:Methode`, `:Rueckbauverfahren`, `:Aufbereitungsverfahren`, `:Wiederverwendungskette` nodes with **all** properties and **all** incoming/outgoing rels
- all `(:Bauteilgruppe)-[r]->(*)` from the affected vocabs
- all `:Projekt` ids and names

**P0.2 Backup the active database.** Standard Neo4j dump to `_neo4j/review/backups/2026-06-03_pre_taxonomy_integration.dump`.

**P0.3 Pre-deletion scan** for every node about to be touched (all 13 `meth_*` + 33 `av_*` + 16 `rq_*` + 11 `wva_*` + 5 `rv_*` = 78 nodes). Run the scan in [CONNECTION_TYPE_AUDIT.md §"Updated Phase 0 pre-flight scan list"](CONNECTION_TYPE_AUDIT.md) and dump to `pre_deletion_scan.json`. Use this scan to drive the Phase 6 reattachment Cypher precisely — each (old_id, upstream_label) tuple gets exactly the right MIGRATE recipe.

**P0.4 Detect mislabeled `:Projekt` nodes** with `prog_*` ids:
```cypher
MATCH (p:Projekt) WHERE p.id STARTS WITH 'prog_' RETURN p.id, p.name, labels(p);
```
For each: add `:Programm` label, remove `:Projekt`. Their old-vocab edges then fall under the `:Programm → vocab` migration path.

**Exit criteria:** all four artifacts written; counts logged; no script has modified the graph yet.

---

## Phase 1 — Decisions  **[COMPLETE — 2026-06-03]**

All four open questions resolved (see §"Decisions taken" at end of this doc). Headline:
- C1 → use existing `:Ressourcenquelle`
- C2 → option (a): replace 13 live `meth_*` with 6 new canonical (batches are source of truth)
- C4 → option (a): replace ~62 live `av_*` with 6 new canonical (aggressive)
- C14 → include Batch 01 (new markdown file delivered)

---

## Phase 2 — Markdown normalization (no graph change)

Touch only the batch Markdown files in [\_neo4j/intake/inbox/research/new taxonomy edit/](../../intake/inbox/research/new%20taxonomy%20edit/). All fixes are local-string substitutions per the coverage report.

**P2.1 Normalize relationship aliases** in batches 07/08 (per [SEMANTIC_CONFLICT_AUDIT.md §C9](SEMANTIC_CONFLICT_AUDIT.md#c9-relationship-name-aliases-inside-the-batches--normalize-in-markdown)) and across all batches:
`HAS_METHOD` → `HAT_METHODE`, `HAS_REUSE_RESULT` → `HAT_ERGEBNIS`, `HAS_SOURCE` → `HAT_RESSOURCENQUELLE`, `HAS_LOCATION` → `HAT_WIEDERVERWENDUNGSORT`, `HAS_PROCESSING` → `HAT_AUFBEREITUNG`, `HAS_DISMANTLING|HAS_DECONSTRUCTION` → `HAT_RUECKBAUVERFAHREN`, `NUTZT_METHODE` → `HAT_METHODE`, `HAT_QUELLE` → `HAT_RESSOURCENQUELLE`.

**P2.2 Normalize target labels** to the canonical six per axis (per coverage report §5.C and audit C3, C4): rewrite `Lokal_oder_Regional_importiert` → `Extern_importiert`, `Sortierung_und_Bergung` → `Zerstoerungsarme_Bergung`, `Demontage_von_Modulen` → `Demontage`, `Rekonfiguration_und_Vormontage` → `Remanufacturing_und_Upcycling`, `Zuschnitt_und_Anpassung` → `Zuschnitt_und_Vereinzelung`, `Keine_wesentliche_Aufbereitung` → `Pruefung_Sortierung_QS`, `Auf_demselben_Areal` → `Auf_demselben_Standort_versetzt`, `Lager_und_Bauteilboerse` → `Bauteilmarkt_oder_Lager`, `Baustellenrest_oder_Ueberproduktion` → `Restposten_Abfall_Unbekannt`, `Nicht_bestimmbar` → `Restposten_Abfall_Unbekannt`, `Design_for_Disassembly` → `Reversibles_Design`, `Dekonstruktion_mit_Inventar` → `Selektiver_Rueckbau` (Rückbau) / `Dokumentation_und_Monitoring` (Methode).

**P2.3 Fix the 6 parser-error / malformed cells** flagged in coverage report (HTML URLs in target columns, etc.) — manual edit.

**P2.4** Apply P2.1–P2.3 normalization to the new [Batch 01 markdown](../../intake/inbox/research/new%20taxonomy%20edit/reuse_taxonomy_v9_connection_expansion_batch_01_markdown_only.md) too (139 rows). The legacy [batch_01.csv](../../intake/inbox/research/new%20taxonomy%20edit/reuse_taxonomy_v9_connection_expansion_batch_01.csv) and [open_questions.csv](../../intake/inbox/research/new%20taxonomy%20edit/reuse_taxonomy_v9_connection_expansion_batch_01_open_questions.csv) are now superseded and should be marked `superseded_by_batch_01_markdown_only` (move to `_archive/` subfolder, do not delete).

**P2.5 Filter out non-`bg_reuse_*` rows** per [FINAL_PLAN.md decision #8](FINAL_PLAN.md#decisions-locked-in). Move all rows that anchor on `bg_retained_*` / `bg_planned_*` / `bg_dismantled_*` / `bg_candidate_*` BGs (~85 rows, 4.9% of total) into `_filtered_non_reuse_bgs.md` for transparency. Do not delete; keep them as historical record outside the import set.

Affected batches per filter check: every batch that mentions ELEMENTA, LysP8, Circl planned/dismantled, Elys/Grande Halle/Botanique retained, MedUni Mariannengasse retained, Melkinlaituri candidate, etc.

**Exit criteria:** running the coverage-report script over the normalized + filtered batches reports **0** raw-alias rows, **0** out-of-vocab target labels, and **0** rows anchoring on non-`bg_reuse_*` BGs. Total parsed row count drops from 2,240 to **~2,155** (1,734 in network export sample minus 85 filtered = baseline shift consistent with full set).

---

## Phase 3 — Build the resolver tables (no graph change)

**P3.1 ~~Project ID map — NO LONGER NEEDED~~**. Live `:Projekt.id` already uses `p_*` slugs that match batches exactly.

**P3.2 ~~Manual resolver — SKIPPED~~** per [FINAL_PLAN.md decision #8](FINAL_PLAN.md#decisions-locked-in). The resolver CSV is consulted programmatically. Phase 5 applies these rules:

- `action = auto_confirm` with `bg_reuse_*` slug (~251 rows) → MERGE into existing live BG, attach batch evidence
- `action = auto_confirm` with non-reuse slug (22 rows) → **SKIP** (live + batch rows dropped in Phase 6 / Phase 2)
- `action = needs_review` (29 rows, all `bg_reuse_*`) → **auto-confirm by policy** — MERGE into existing live BG, attach batch evidence
- `action = no_batch_equiv` (48 rows) → split by prefix:
  - if `bg_reuse_*` (35 rows) → **DELETE live BG** in Phase 6.4b
  - if non-reuse (13 rows) → **DELETE live BG** in Phase 6.4c
- `action = new_candidate` (28 rows):
  - if `bg_reuse_*` (24 rows) → MERGE as new `:Bauteilgruppe` node with `bg_kind = 'partial_batch'`
  - if non-reuse / `bg_candidate_*` (4 rows) → SKIP

**P3.2 [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv)** — `batch_bg_id, live_bg_id_or_NEW, match_method (exact|fuzzy|new_candidate), confidence, decision`. Generated by:
- exact `bg_*` slug match
- fuzzy match per `{live_projekt_id, bauteiltyp_token, material_token, descriptor_overlap_ratio}` with a configurable similarity threshold
- batches `*_candidate` suffix → always `NEW`

Manual review queue for fuzzy < 0.85 or any row hitting two live targets. Expected size ~700 rows (2,101 batch rows × 1 bg per row, deduped).

**P3.3 [vocabulary_id_map.csv](vocabulary_id_map.csv)** — Canonical lookups:
- batch `Wiederverwendungsergebnis` token → new `wver_*` id (6 canonical)
- batch `Wiederverwendungsort` token → new `wvo_*` id (6 canonical)
- batch `Quelle` token → new `rq_*` id (6 new canonical replacing the 16 live `rq_*`)
- batch `Methode` token → new `meth_*` id (6 new canonical)
- batch `Rueckbauverfahren` token → existing `rv_*` (4 reused) + 2 new
- batch `Aufbereitungsverfahren` token → new `av_*` id (6 new canonical)
- **legacy → new collapse map** (used by Phase 6 migration of non-replaceable upstreams):
  - `wva_*` (11) → does NOT collapse anywhere; the WiederverwendungsArt axis retires entirely. Their inbound edges are deleted (per [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md)), no migration target.
  - `meth_*` (13) → 6 new canonical per the C2 table
  - `av_*` (33) → 6 new canonical per the C4 table
  - `rq_*` (16) → 6 new canonical per the C1 table
  - `rv_betonfraesen` → `rv_schneidender_rueckbau` (1 entry; other 4 `rv_*` ids are unchanged)

**Exit criteria:** all three CSVs reviewed and signed off. Any row marked `manual_review_needed = TRUE` is resolved before Phase 4.

---

## Phase 4 — Schema additions (Cypher, idempotent, single run-tag)

Run tag: `review_run = 'taxonomy_integration_2026_06_03'`

**P4.1 New label constraints & indexes.**

```cypher
CREATE CONSTRAINT wiederverwendungsergebnis_id IF NOT EXISTS
  FOR (n:Wiederverwendungsergebnis) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT wiederverwendungsort_id IF NOT EXISTS
  FOR (n:Wiederverwendungsort) REQUIRE n.id IS UNIQUE;
CREATE CONSTRAINT rel_hat_ergebnis_id IF NOT EXISTS
  FOR ()-[r:HAT_ERGEBNIS]-() REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT rel_hat_wiederverwendungsort_id IF NOT EXISTS
  FOR ()-[r:HAT_WIEDERVERWENDUNGSORT]-() REQUIRE r.id IS UNIQUE;
CREATE CONSTRAINT rel_angewendet_auf_id IF NOT EXISTS
  FOR ()-[r:ANGEWENDET_AUF]-() REQUIRE r.id IS UNIQUE;
```

(If C1 = `:Herkunft`: add `herkunft_id`, `rel_hat_herkunft_id` constraints too.)

**P4.2 Seed the 6 new `:Wiederverwendungsergebnis` nodes** + 6 new `:Wiederverwendungsort` nodes, all with `source_scope = 'controlled_vocab_seed'`.

**P4.3 MERGE 6 new canonical `:Methode` nodes**:
`meth_urban_mining_und_scouting`, `meth_bestands_und_reuse_assessment`, `meth_verfuegbarkeitsbasiertes_design`, `meth_reversibles_design`, `meth_zirkulaere_beschaffung`, `meth_dokumentation_und_monitoring`.

**P4.4 MERGE 6 new canonical `:Aufbereitungsverfahren` nodes**:
`av_reinigung_und_oberflaeche`, `av_zuschnitt_und_vereinzelung`, `av_pruefung_sortierung_qs`, `av_reparatur_und_refurbishment`, `av_remanufacturing_und_upcycling`, `av_verstaerkung_und_schutz`.

**P4.5 MERGE 6 new canonical `:Ressourcenquelle` nodes**:
`rq_externer_spenderbau`, `rq_eigener_bestand`, `rq_gleicher_standort`, `rq_bauteilmarkt_oder_lager`, `rq_leihgabe_oder_service`, `rq_restposten_abfall_unbekannt`.

**P4.6 MERGE the 2 new `:Rueckbauverfahren` nodes**: `rv_schneidender_rueckbau`, `rv_integrierter_rueckbau_und_lagerung`. (Existing `rv_selektiver_rueckbau`, `rv_ausbau_von_bauteilen`, `rv_demontage`, `rv_zerstoerungsarme_bergung` remain — their ids already match batch canonicals.)

**Exit criteria:** [verify_integration.cypher](verify_integration.cypher) §1 (schema-additions block) returns all green.

---

## Phase 5 — Stage batches as Cypher (dry-run + apply)

For each batch row, emit one idempotent `MERGE` per the schema-guide MERGE pattern. Use `MATCH (a {id: ...})` (label-agnostic) and resolve every id through the Phase 3 maps.

**P5.1 Generate** [\_neo4j/review/2026-06-03_taxonomy_integration_plan/staging/](staging/) Cypher files, one per batch (02–10 plus the conditional batch-01-fixup). Each file is wrapped in `:USE mit-bestand;` and the apply log goes to `staging/apply_reports/`.

Every relationship MERGE follows the schema-guide property contract:

```cypher
MATCH (bg {id: $live_bg_id}), (t {id: $live_target_id})
MERGE (bg)-[r:HAT_ERGEBNIS]->(t)
ON CREATE SET r.id                  = $row_uuid,
              r.evidence_basis      = 'taxonomy_integration_2026_06_03',
              r.evidence_confidence = $mapped_confidence,  // HIGH→belegt etc.
              r.evidence_url        = $batch_evidence_url,
              r.evidence_quote      = left($batch_evidence_summary, 240),
              r.review_run          = 'taxonomy_integration_2026_06_03',
              r.created_at          = datetime(),
              r.batch_id            = $batch_id,
              r.batch_edge_id       = $batch_edge_id;  // e.g. 'v10B-001'
```

**P5.2 Dry-run** on `:USE mit-bestand-dryrun;` (clone). Capture `EXPLAIN`/`PROFILE` for the largest batch. Verify `verify_integration.cypher` §2 (stage-time invariants) returns green on the clone.

**P5.3 Apply** to live `mit-bestand`. Each batch is one transaction; if any constraint violation, abort and roll back via `MATCH ()-[r {review_run:'taxonomy_integration_2026_06_03'}]-() DELETE r;` (also for nodes created in this run).

**Exit criteria:** all batches applied; per-batch row counts match expected (parsed batch rows = created+merged rels per axis ± known dedupes).

---

## Phase 6 — Old-vocab retirement (delete-with-targeted-migration)

Driven entirely by [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md). No `:*_Legacy` labels are created. Every old node ends Phase 6 either hard-deleted or — in the special case of the 4 matching `rv_*` ids — re-used as the new canonical.

**P6.1 Migrate non-replaceable upstream edges (115 total).** For each old-vocab node and each inbound edge whose source label is NOT `:Bauteilgruppe`, NOT `:Projekt`, NOT `:DataIssue`:

```cypher
// Template (instantiated per vocab axis from vocabulary_id_map.csv)
MATCH (upstream)-[r_old:HAT_METHODE]->(meth_old:Methode)
WHERE NOT upstream:Bauteilgruppe AND NOT upstream:Projekt AND NOT upstream:DataIssue
MATCH (meth_new:Methode {id: $new_id_for[meth_old.id]})
MERGE (upstream)-[r_new:HAT_METHODE]->(meth_new)
ON CREATE SET r_new = properties(r_old),
              r_new.legacy_methode_id   = meth_old.id,
              r_new.legacy_methode_name = meth_old.name,
              r_new.review_run          = 'taxonomy_integration_2026_06_03',
              r_new.migrated_at         = datetime();
DELETE r_old;
```

Run for: `:Akteur|:Software|:Software:Tool|:Norm|:Programm → :Methode` (74 edges), `:ReuseRule → :Aufbereitungsverfahren` (40 edges), `:Materialdepot → :Ressourcenquelle` (1 edge). `:WiederverwendungsArt` and `:Rueckbauverfahren` have no non-replaceable upstreams (skip).

**P6.2 Migrate outbound edges from `:Aufbereitungsverfahren` (47 edges).** The 22 `TYPISCH_BEI_MATERIAL → :Material` and 25 `BELEGT_IN → :Quelle:ResearchDocument` edges live on the *outbound* side of old `av_*`. MERGE dedupes when multiple old `av_*` collapse to one new canonical:

```cypher
MATCH (av_old:Aufbereitungsverfahren)-[r_old:TYPISCH_BEI_MATERIAL]->(mat:Material)
MATCH (av_new:Aufbereitungsverfahren {id: $new_id_for[av_old.id]})
MERGE (av_new)-[r_new:TYPISCH_BEI_MATERIAL]->(mat)
ON CREATE SET r_new = properties(r_old),
              r_new.legacy_aufbereitung_id   = av_old.id,
              r_new.legacy_aufbereitung_name = av_old.name,
              r_new.review_run               = 'taxonomy_integration_2026_06_03';
DELETE r_old;
```

Same template for `BELEGT_IN`.

**P6.3 Delete replaceable upstream edges.** For each old vocab axis, delete all inbound edges from `:Bauteilgruppe` and `:Projekt` (the batches re-supplied these in Phase 5):

```cypher
MATCH (src)-[r:HAT_METHODE]->(meth_old:Methode)
WHERE (src:Bauteilgruppe OR src:Projekt)
  AND NOT meth_old.id IN [<6 new canonical ids>]
DELETE r;
```

Run for each of: `HAT_METHODE`, `HAT_AUFBEREITUNG`, `HAT_RESSOURCENQUELLE`, `HAT_WIEDERVERWENDUNGSART`, `HAT_RUECKBAUVERFAHREN`. Expected deletion counts (from [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md)): 397+194 + 411+22 + 482+69 + 425+179 + 299+0 = **2,478 edges**.

**P6.4 ~~DataIssue cleanup — NOT NEEDED~~.** The 2026-06-03 full schema export confirms `:DataIssue` count is now **0** (was 28,729 in the 06-01 baseline). Previous integration rounds already cleaned them. No CONCERNS-edge handling required.

**P6.4b Delete `bg_reuse_*` orphan Bauteilgruppen** per [FINAL_PLAN.md decision #8](FINAL_PLAN.md#decisions-locked-in). 35 live `bg_reuse_*` BGs that have no batch slug match (`action = no_batch_equiv`) — replaced by the batches' evidence-backed set.

```cypher
LOAD CSV WITH HEADERS FROM 'file:///bauteilgruppe_id_map.csv' AS row
WITH row WHERE row.action = 'no_batch_equiv' AND row.live_bg_id STARTS WITH 'bg_reuse_'
MATCH (bg:Bauteilgruppe {id: row.live_bg_id})
DETACH DELETE bg;
```

**P6.4c Delete all non-`bg_reuse_*` Bauteilgruppen** per [FINAL_PLAN.md decision #8](FINAL_PLAN.md#decisions-locked-in). 35 live `bg_retained_*` + `bg_planned_*` + `bg_dismantled_*` BGs (any action — they don't semantically belong to `:Bauteilgruppe` regardless of batch coverage).

```cypher
MATCH (bg:Bauteilgruppe)
WHERE bg.id STARTS WITH 'bg_retained_'
   OR bg.id STARTS WITH 'bg_planned_'
   OR bg.id STARTS WITH 'bg_dismantled_'
   OR bg.id STARTS WITH 'bg_candidate_'
DETACH DELETE bg;
```

Phase 0.3 pre-deletion scan must include both lists. Combined expected loss: ~600-800 non-vocab edges + 70 property bags + 85 batch rows filtered in Phase 2.5.

**P6.5 Hard-delete old vocab nodes.** After P6.1–P6.4, every old `meth_*` / `av_*` / `rq_*` / `wva_*` / `rv_betonfraesen` should have zero remaining edges (verify with a sanity check first):

```cypher
// Sanity check: anything left attached?
MATCH (n) WHERE (n:Methode OR n:Aufbereitungsverfahren OR n:Ressourcenquelle
                 OR n:WiederverwendungsArt OR n:Rueckbauverfahren)
  AND NOT n.id IN [<all 24 new canonical ids>]
  AND (n)-[]-()
RETURN labels(n), n.id, count{(n)-[]-()} AS still_attached;
// expected: 0 rows. If non-zero, abort and investigate.

// Hard delete
MATCH (n) WHERE (n:Methode OR n:Aufbereitungsverfahren OR n:Ressourcenquelle
                 OR n:WiederverwendungsArt OR n:Rueckbauverfahren)
  AND NOT n.id IN [<all 24 new canonical ids>]
DELETE n;
```

`<all 24 new canonical ids>` = the 6 new `meth_*` + 6 new `av_*` + 6 new `rq_*` + 6 `rv_*` (4 kept + 2 new). Plus optionally the new `:Wiederverwendungsergebnis` and `:Wiederverwendungsort` (which carry their own labels and won't match this query anyway).

**P6.6 Drop `:WiederverwendungsArt` label entirely.** After P6.5 there should be zero nodes carrying this label. As an additional hygiene step, drop any leftover constraint:

```cypher
MATCH (n:WiederverwendungsArt) RETURN count(n);  // expected: 0
DROP CONSTRAINT wiederverwendungsart_id IF EXISTS;
```

**Exit criteria:**
- Zero nodes carry `:WiederverwendungsArt`.
- Active `:Methode`, `:Aufbereitungsverfahren`, `:Ressourcenquelle` each contain exactly 6 canonical nodes with the new ids.
- `:Rueckbauverfahren` contains exactly 6 nodes.
- No `:*_Legacy` labels anywhere.
- Every migrated edge carries `legacy_*_id`/`legacy_*_name` provenance + `review_run`.
- DataIssue cleanup logged with before/after counts.

---

## Phase 7 — Verification

Run [verify_integration.cypher](verify_integration.cypher). It is read-only and re-runnable. All checks must return `OK` (or zero rows for "find duplicates" queries) before sign-off.

The verification suite is documented inline in that file but covers:
- §1: schema-additions block (new constraints / new seed nodes present, correct counts)
- §2: stage-time invariants (no orphaned Bauteilgruppe, no duplicate `:Projekt`, no duplicate `:Bauteilgruppe`)
- §3: row-count parity (live edge counts per axis ≈ batch row counts; per coverage report Section 3)
- §4: id-prefix purity (every node carries the convention-correct prefix; no `p_*` `:Projekt`, no `bg_*_candidate` left as active)
- §5: legacy retirement (zero active `HAT_WIEDERVERWENDUNGSART`, no orphan-from-collapse)
- §6: edge-property contract (every Phase 5 / Phase 6 rel carries `review_run`, `evidence_basis`, `evidence_confidence`, `created_at`)
- §7: coverage parity (every project with batch coverage has ≥1 new-axis edge; the two C14 projects either covered or in `pending_row_level_evidence` set)
- §8: rollback rehearsal — dry-run delete of the run-tag and re-count

**Exit criteria:** verify_integration.cypher returns no FAIL rows. Sign-off recorded in `INTEGRATION_SIGNOFF.md`.

---

## Rollback

Phase 6 is destructive (nodes are hard-deleted). Edge-level rollback within this run is possible for Phase 5, but for Phase 6 the only safe restore is the Phase 0.2 database dump.

```cypher
// Phase 5 edges (created in this run) — rollback-able
MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]-() DELETE r;
// Phase 4 seed nodes — rollback-able while no other edges anchor them
MATCH (n) WHERE n.review_run = 'taxonomy_integration_2026_06_03'
  AND (n:Wiederverwendungsergebnis OR n:Wiederverwendungsort
       OR n:Methode OR n:Aufbereitungsverfahren OR n:Ressourcenquelle
       OR n:Rueckbauverfahren)
  AND NOT (n)-[]-()
DELETE n;
```

**Phase 6 rollback** = full restore from `_neo4j/review/backups/2026-06-03_pre_taxonomy_integration.dump` via `neo4j-admin database load`. This is by design: the user wants no legacy nodes, so we don't leave a soft-archive that would clutter the active graph.

Therefore: **do not start Phase 6 until Phase 5 verifies green and the Phase 0.2 dump is confirmed restorable on a clone.**

---

## Decisions taken (2026-06-03)

| Conflict | Choice | Rationale |
|---|---|---|
| **C1** Material origin | Keep `:Ressourcenquelle` label; **replace all 16 `rq_*` nodes** with 6 new batch-canonical | Connection-type audit confirmed semantic equivalence but the live ids don't match batch canonicals. Per user "no legacy stuff": delete 16, create 6 new with batch names. Migrate only the 1 `:Materialdepot → :Ressourcenquelle` edge. |
| **C2** `:Methode` collapse | **Hard delete 13 + replace with 6 new canonical** | User: "old ones should be deleted because they are too generic and they lack of evidence". 591 Bauteilgruppe/Projekt→Methode edges deleted (batches re-supply); 74 edges from non-replaceable upstreams (Akteur, Software, Tool, Norm) MIGRATED to new canonical. |
| **C4** `:Aufbereitungsverfahren` collapse | **Hard delete 33 + replace with 6 new canonical** | User: "aggressive". 433 Bauteilgruppe/Projekt edges deleted; 40 `:ReuseRule → Aufbereitung` MIGRATED; 47 outbound (`TYPISCH_BEI_MATERIAL`, `BELEGT_IN`) MIGRATED + deduped onto new canonical. |
| **C14** Batch 01 | Include — markdown delivered 2026-06-03 10:08 | New row-level Batch 01 (139 rows, 10 projects including K118 + MedUni) supersedes summary. Legacy `.csv` files moved to `_archive/`. |
| **P3.1** Project ID map | **Not needed** | Live `:Projekt.id` already uses `p_*` slug matching batch IDs (verified across all 86 live projects). |
| **`:WiederverwendungsArt`** | **Label retires entirely** | 604 edges deleted (no migration anywhere — axis fully replaced by the new triple Ergebnis/Methode/Ort). 11 nodes hard-deleted. Constraint dropped in P6.6. |
| **`:Rueckbauverfahren`** | Keep 4 matching ids; add 2 new; delete `rv_betonfraesen` | 4 existing ids already match batch canonicals — no need to replace nodes. Only edge churn. |
| **DataIssue cleanup** | **Delete or trim** per P6.4 | DataIssues about retired vocab are themselves obsolete after integration. DataIssues whose entire CONCERNS set targets retired nodes → DETACH DELETE. Mixed DataIssues → trim dangling edges only. |
| **`:Projekt` with `prog_*` id** | Relabel to `:Programm` in P0.4 | Data-quality fix found by audit. Their old-vocab edges then go through the `:Programm → vocab` migration path. |
