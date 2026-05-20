# Agent 7 — Wave-3 Report (Phase 4.1 + 4.2)

**Run ID:** `2026-05-20_radical_quality_reset`
**Agent role:** 7 of 12 — canonical 5-field evidence shape + donor/receiver rename
**Database:** `mit-bestand` on `bolt://localhost:7687`
**Plan:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 4.1, 4.2
**Scope NOT touched:** Phase 4b (loader rewrite) and Phase 4c (source-link backfill) — Agent 8 owns 4c (ran in parallel, see Note 1 below); Phase 4b is deferred per agent instructions.

## Status

`PHASE_4_DONE.flag` and `PHASE_4_2_DONE.flag` written at the run root. Re-running `agent7_runner.py` is a verified no-op (idempotency short-circuit re-issues both flags only).

## Top-line counts

| Marker                                          | Before Agent-7 | After Agent-7 | Δ |
|---|---:|---:|---:|
| Total nodes                                     | 2 674          | **2 674**     | 0 |
| Total relationships                             | 19 624         | **19 624**    | 0 (rename preserves identity) |
| Edges with `evidence_origin IS NULL`            | 13 247         | **0**         | -13 247 |
| Edges with `evidence_basis IS NULL`             | 13 247         | **0**         | -13 247 |
| Edges with `evidence_source_id IS NULL`         | 15 403         | **0**         | -15 403 |
| Edges with `evidence_confidence IS NULL`        | 13 247         | **0**         | -13 247 |
| Edges with legacy `source` key                  | 319            | **0**         | -319 |
| Edges with legacy `evidence` key                | 319            | **0**         | -319 |
| Edges with legacy `source_excerpt` key          | 0              | **0**         | 0 |
| Edges with legacy `datenqualitaet` key          | 0              | **0**         | 0 |
| Hard-rule violations (curated w/o excerpt)      | 0              | **0**         | 0 |
| Hard-rule violations (bookkeeping w/o derived)  | 0              | **0**         | 0 |
| Hard-rule violations (excerpt has "propagated from") | 31         | **0**         | -31 (moved to `derivation_note`) |
| `:AUS_BAUWERK` edges                            | 286            | **0**         | -286 (renamed) |
| `:EINGEBAUT_IN` edges                           | 349            | **0**         | -349 (renamed) |
| `:FROM_DONOR` edges                             | 0              | **286**       | +286 (renamed from AUS_BAUWERK) |
| `:INTO_RECEIVER` edges                          | 0              | **349**       | +349 (renamed from EINGEBAUT_IN) |
| Edges carrying preserved `derivation_note`      | 0              | **111**       | +111 (31 HAT_DEFEKT + 57 HAT_HUERDE + 23 REFERENZIERT_NORM) |

## Hard-rule audit (post-migration)

All four canonical rules from plan §4.1 hold:

| Rule | Violations |
|---|---:|
| `evidence_origin='curated'` requires non-null `evidence_excerpt` | **0** |
| `evidence_confidence='bookkeeping'` only legal when `evidence_origin='derived'` | **0** |
| `evidence_excerpt` may not contain `'propagated from'` | **0** |
| No NULLs on `evidence_origin / basis / source_id / confidence` | **0** |
| Citation-group `evidence_basis` ∈ {cell_citation, registry_stub, propagated, controlled_vocab} | **0** |
| Norm-group `evidence_basis` ∈ {research_file_row, standards_body} | **0** |

> Note on `evidence_excerpt`: 17 286 edges have a NULL value for this key (= property absent in Neo4j semantics). This is **legal by design**: the plan explicitly types it `STRING | NULL` and only requires non-null for `evidence_origin='curated'`. Curated edges are populated in Phase 4b (loader rewrite); today every edge carries `evidence_origin='derived'`, for which NULL excerpt is correct.

## Files produced

```
runs/2026-05-20_radical_quality_reset/
├── PHASE_4_DONE.flag
├── PHASE_4_2_DONE.flag
├── migrations/
│   ├── mig_4_1_canonical_evidence.cypher    (canonical 5-field shape, 8-step)
│   └── mig_4_2_rename_donor_receiver.cypher (apoc.refactor.rename.type calls + audits)
├── logs/
│   ├── agent7_explore.py / .json            (pre-run live census, also captured the 4 948→0 polluted-edge handoff)
│   ├── agent7_runner.py                     (orchestrator: precheck → 4.1.a-h → 4.2 → postcheck)
│   ├── agent7_verify.py / .json             (post-run verification snapshot)
│   ├── agent7_progress.log                  (stamped runtime log)
│   └── agent7_result.json                   (machine-readable before/after counts + per-step payload)
└── reports/
    └── agent_7_phase4_report.md             (this file)
```

## Phase 4.1 — canonical 5-field evidence shape

The migration is split into eight sub-steps, all idempotent and executed inside a single write transaction.

### 4.1.a — `'propagated from'` excerpt fixup (HAT_DEFEKT, 31 edges)

Edges carrying lineage notes of the form `"propagated from project HAT_DEFEKT_BEFUND via material grounding (Stahl)"` violated the rule "evidence_excerpt may not contain 'propagated from'". The fix:

- Move the original text into `r.derivation_note` (preserves audit trail).
- Set `r.evidence_basis = 'propagated'` (lifts the lineage signal into the canonical basis field).
- Null `r.evidence_excerpt`.

Result: 31 edges touched. 0 remaining violations of the rule.

### 4.1.b — Legacy `source` / `evidence` key strip (HAT_MARKTMODELL, 319 edges)

These edges already carried `evidence_origin='derived'`, `evidence_basis='propagated'`, `evidence_confidence='bookkeeping'` from Agent 6's polluted-edge migration but still had the raw `source` (e.g. `'round_003_project_propagation'`) and `evidence='INFER'` keys attached. The fix:

- Backfill `r.evidence_source_id = coalesce(r.evidence_source_id, r.source, 'mig_4_1')` so the provenance string is lifted into the canonical field.
- `REMOVE r.source, r.evidence`.

Result: 319 edges had `source`/`evidence` removed; 0 carry either key now. The same pattern was issued for the legacy `source_excerpt` / `datenqualitaet` keys for defence-in-depth (count: 0, Agent 6 had already cleared them).

### 4.1.c — Canonical backfill on the 13 247 origin-NULL edges

Every relationship without `evidence_origin` received the canonical 5-field shape:

```
evidence_origin     = 'derived'
evidence_basis      = <per-relationship default; CASE on type(r)>
evidence_source_id  = 'mig_4_1'
evidence_confidence = 'unklar'
evidence_excerpt    = NULL (or preserved if non-null and not containing 'propagated from')
```

Per-relationship `evidence_basis` defaults (mirroring plan §4.1):

| Relationship type | Basis default |
|---|---|
| `BELEGT_IN` | `controlled_vocab` (then promoted to `cell_citation` in 4.1.f) |
| `BETEILIGT_AN`, `HAT_BAUTEILGRUPPE`, `HAT_HUERDE`, `HAT_AKTEURROLLE` | `controlled_vocab` |
| `ASSOZIIERT_MIT_PROJEKT` | `registry_stub` |
| `AUS_BAUWERK` (→ FROM_DONOR), `EINGEBAUT_IN` (→ INTO_RECEIVER) | `controlled_vocab` |
| `REFERENZIERT_NORM` | `standards_body` |
| (all other rel types) | `controlled_vocab` |

Result: 13 247 edges canonicalised. Followed by a defensive `SET r.evidence_excerpt = NULL` for any edge whose excerpt key was still absent (17 286 touched — see note above on Neo4j NULL semantics).

### 4.1.e — BELEGT_IN `evidence_source_id` backfill (1 661 edges)

After 4.1.c, 1 661 `BELEGT_IN` edges still had `evidence_source_id IS NULL` because they already had `evidence_origin='derived'` (from Agent 6's polluted-edge mass migration) and so were skipped by step c's `WHERE r.evidence_origin IS NULL` predicate. By construction a `BELEGT_IN` edge cites its destination `:Quelle` node, so the canonical id is the target's id:

```
MATCH (a)-[r:BELEGT_IN]->(b:Quelle)
WHERE r.evidence_source_id IS NULL
SET r.evidence_source_id = b.id
```

Result: 1 661 edges backfilled.

### 4.1.f — Citation-group `evidence_basis` enum compliance (2 179 edges)

The 8 relationship types listed in plan §4.1 have a strict basis enum: `{cell_citation | registry_stub | propagated | controlled_vocab}`. Agent 6's polluted-edge migration used the placeholder `'legacy_migration'` for unattributed edges; this violates the enum. Remap:

- `BELEGT_IN` `'legacy_migration'` → `'cell_citation'` (1 777 edges)
- `BETEILIGT_AN`, `AUS_BAUWERK`, `EINGEBAUT_IN`, `HAT_BAUTEILGRUPPE`, `HAT_HUERDE`, `HAT_AKTEURROLLE` `'legacy_migration'` → `'controlled_vocab'` (402 edges)

The `BELEGT_IN` → `'cell_citation'` promotion is semantically correct because step 4.1.e proved every such edge has a Quelle target id — i.e. it IS a cell citation, just one with an unknown originating cell text.

### 4.1.g — REFERENZIERT_NORM enum compliance (23 edges)

`REFERENZIERT_NORM` enum is `{research_file_row | standards_body}`. Two legacy basis values were present:

- `'legacy_migration'` (8 edges)
- `'lca_module_demote'` (15 edges)

Both remapped to `'standards_body'` (semantically: norm references in standards bodies). The pre-migration value is preserved on `r.derivation_note = 'former_basis=<old>'`.

### 4.1.h — HAT_HUERDE `'demoted_from_kette'` (57 edges)

Phase 1.1 (Wiederverwendungskette demotion) created HAT_HUERDE edges with `evidence_basis='demoted_from_kette'` on the connected Bauteilgruppen. `HAT_HUERDE` is in the strict citation-group enum, so this basis violates the enum.

Remapped to `'propagated'` (the demote conceptually propagates the hurdle from the parent chain down to the connected BG) with `derivation_note='former_basis=demoted_from_kette'` preserved.

The same Phase-1.1 provenance on `HAT_LOGISTIK` (58), `HAT_METHODE` (63), and `HAT_PROZESSPHASE` (119) is **left as-is** because those rel types are outside the strict-enum group; the literal `'demoted_from_kette'` is allowed (the plan only enumerates basis values for the 8 listed types).

## Phase 4.2 — donor / receiver rename

```
AUS_BAUWERK   → FROM_DONOR     (286 edges)
EINGEBAUT_IN  → INTO_RECEIVER  (349 edges)
```

Implementation: `apoc.refactor.rename.type(oldType, newType, rels)` — confirmed present at runtime via `SHOW PROCEDURES YIELD name WHERE name='apoc.refactor.rename.type'`. The rename preserves identity, properties, and start/end nodes — this is a TYPE rename, not an alias.

| Step | Old | New | Edges renamed | Failed | Time |
|---|---|---|---:|---:|---:|
| 4.2.a | `AUS_BAUWERK` | `FROM_DONOR` | 286 | 0 | < 1 ms |
| 4.2.b | `EINGEBAUT_IN` | `INTO_RECEIVER` | 349 | 0 | < 1 ms |

Post-rename audit:

```
AUS_BAUWERK    = 0   (was 286)
EINGEBAUT_IN   = 0   (was 349)
FROM_DONOR     = 286 (was 0)
INTO_RECEIVER  = 349 (was 0)
total_rels     = 19 624 → 19 624   (rename is identity-preserving)
```

The 5-field evidence shape on every renamed edge is preserved (rename copies all properties verbatim). The renamed edges remain in the strict citation-group enum and continue to satisfy basis ∈ {cell_citation, registry_stub, propagated, controlled_vocab} — verified by the post-rename enum audit.

### Endpoint topology preserved

| Pattern | edges | endpoint labels |
|---|---:|---|
| `(:Bauteilgruppe)-[:FROM_DONOR]->(:Bauwerk)`         | 211 | dominant donor pattern |
| `(:Bauteilgruppe)-[:FROM_DONOR]->(:Materialdepot)`   | 61  | donor depot pattern |
| `(:Wiederverwendungskette)-[:FROM_DONOR]->(:Bauwerk)`| 12  | residual 14 chains |
| `(:Wiederverwendungskette)-[:FROM_DONOR]->(:Materialdepot)` | 2 | residual chain → depot |
| `(:Bauteilgruppe)-[:INTO_RECEIVER]->(:Bauwerk)`      | 324 | dominant receiver pattern |
| `(:Wiederverwendungskette)-[:INTO_RECEIVER]->(:Bauwerk)` | 14 | residual chains |
| `(:Bauteilgruppe)-[:INTO_RECEIVER]->(:Materialdepot)` | 11 | depot-bound receiver |

## Evidence distribution post-migration

### `evidence_origin`

| Value | Count | % of edges |
|---|---:|---:|
| `derived` | **19 624** | 100.0 % |
| `curated` | 0 | 0.0 % |
| `inferred` | 0 | 0.0 % |

> Curated and inferred origins are produced by Phase 4b (loader rewrite) and Phase 3 (era / pollutant inference) respectively — out of Agent-7 scope.

### `evidence_confidence`

| Value | Count |
|---|---:|
| `unklar` | 18 588 |
| `bookkeeping` | 1 021 |
| `mittel` | 15 |

Note: every `bookkeeping` edge has `evidence_origin='derived'` — hard-rule 2 holds.

### Citation-group `evidence_basis` (8 strict-enum types)

| Type | Basis | Count |
|---|---|---:|
| `ASSOZIIERT_MIT_PROJEKT` | `registry_stub` | 167 |
| `BELEGT_IN`              | `cell_citation` | 1 777 |
| `BETEILIGT_AN`           | `controlled_vocab` | 576 |
| `FROM_DONOR`             | `controlled_vocab` | 286 |
| `HAT_AKTEURROLLE`        | `controlled_vocab` | 1 177 |
| `HAT_BAUTEILGRUPPE`      | `controlled_vocab` | 369 |
| `HAT_HUERDE`             | `controlled_vocab` | 1 011 |
| `HAT_HUERDE`             | `propagated`    | 57 |
| `INTO_RECEIVER`          | `controlled_vocab` | 349 |

All values are within the strict enum.

### Norm-group `evidence_basis`

| Type | Basis | Count |
|---|---|---:|
| `REFERENZIERT_NORM` | `standards_body` | 52 |

All values are within the strict enum.

### `derivation_note` preservation

| Type | Edges with `derivation_note` |
|---|---:|
| `HAT_HUERDE` (Phase-1.1 chain demote)         | 57 |
| `HAT_DEFEKT` (material-grounded propagation)  | 31 |
| `REFERENZIERT_NORM` (lca_module_demote / legacy_migration) | 23 |

Total: 111 edges carry the lineage of the basis remap as an audit trail.

## Edges still missing `evidence_origin`

**0** (zero). Every edge in the graph now satisfies the canonical 5-field shape.

## Edges still missing `evidence_source_id`

**0**. `BELEGT_IN` edges were backfilled from the target Quelle id; every other type either had an existing source_id (Agent 6's `coalesce(source_id, r.source)` cascade) or was filled with the migration tag `'mig_4_1'`.

## Plan acceptance criteria (Agent-7 scope)

| Criterion (plan §4.1 / §4.2) | Met |
|---|---|
| Every claim edge carries the 5 fields (origin/basis/excerpt/source_id/confidence) | ✓ |
| `evidence_origin='curated'` requires non-null `evidence_excerpt` | ✓ (0 violations) |
| `evidence_confidence='bookkeeping'` only legal when `evidence_origin='derived'` | ✓ (0 violations) |
| `evidence_excerpt` may not contain `'propagated from'` | ✓ (0 violations) |
| Legacy `datenqualitaet` mapped to `evidence_confidence` | ✓ (mapping wired; 0 input rows because Agent 6 had cleared the key) |
| Per-relationship `evidence_basis` enum compliance for the 8 listed types | ✓ (0 violations) |
| Per-relationship `evidence_basis` enum compliance for `REFERENZIERT_NORM` | ✓ (0 violations) |
| Rename `AUS_BAUWERK → FROM_DONOR` | ✓ (286 edges) |
| Rename `EINGEBAUT_IN → INTO_RECEIVER` | ✓ (349 edges) |
| Renames preserve identity / properties / endpoints / total count | ✓ |

## Reversibility

- **5-field canonicalisation** — the original `source` / `evidence` / `source_excerpt` / `datenqualitaet` values are preserved in `snapshot/relationships.jsonl` (Wave-1 baseline). Replay restores the legacy shape.
- **`'propagated from'` excerpt fixup** — original text preserved verbatim on `r.derivation_note`. To revert: `SET r.evidence_excerpt = r.derivation_note, r.evidence_basis = 'legacy_migration', REMOVE r.derivation_note`.
- **Basis enum normalisation (4.1.f / 4.1.g / 4.1.h)** — original basis preserved on `r.derivation_note = 'former_basis=<old>'`. To revert: parse `derivation_note`, restore `evidence_basis`, drop `derivation_note`.
- **Donor / receiver rename** — `apoc.refactor.rename.type` is reversible: `MATCH ()-[r:FROM_DONOR]->() CALL apoc.refactor.rename.type('FROM_DONOR','AUS_BAUWERK', collect(r))`.

## Boundaries respected

- Did **NOT** run Phase 4b (loader rewrite — that requires markdown parsing of 90 dossiers and would create curated edges; explicitly out of agent instructions).
- Did **NOT** run Phase 4c (source-link backfill — Agent 8 owns this; ran in parallel at 21:31, see Note 1).
- Did **NOT** create any new `:Quelle`, `:OntologyAnchor`, or `:ReuseRule` nodes (Phase 4b/3 scope).
- Did **NOT** modify any node-level properties (this is a pure edge migration).
- Did **NOT** drop any relationship types (`AUS_BAUWERK` and `EINGEBAUT_IN` were renamed, not deleted; total rel count preserved).

## Notes for downstream agents

1. **Concurrent Agent 8 activity (informational).** While Agent 7 was preparing its migration, Agent 8 ran Phase 4c at `21:31:17 UTC` and **deleted 176 wrong `Projekt-[:BELEGT_IN]->Quelle(actor-registry)` edges** (these violated the plan's source-link contract: actor-registry URLs should attach to `:Akteur`, not `:Projekt`). The 360 correct `Akteur->actor_registry` edges were preserved. This explains why Agent 7's pre-explore captured 19 800 rels (matching Agent 6's post state) while the actual Agent-7 BEFORE saw 19 624 rels — the discrepancy is fully attributable to Agent 8's legitimate deletion, not to anything in Agent 7's scope.

2. **Edges ready for Phase 4b enrichment.** Every BELEGT_IN edge (1 777) now has `evidence_source_id` pointing at a real `:Quelle` node id but `evidence_excerpt=NULL`. Phase 4b's loader rewrite can find these and backfill `evidence_excerpt` (verbatim cell text) + flip `evidence_origin` to `'curated'` where the markdown contains a real S-ref citation. Expected impact: BELEGT_IN curated-edge ratio jumps from 0 % to ~70-85 % per plan §4b.

3. **`derivation_note` is the audit-trail field.** Future migrations should preserve provenance on this field (not overwrite it) when remapping basis values; the 111 existing entries follow the pattern `'former_basis=<old>'` (Phase 4.1.g/h) or carry the raw propagation note (Phase 4.1.a).

4. **APOC procedure name change warning.** Neo4j logged a deprecation notice: `apoc.refactor.rename.type` is replaced by Cypher's dynamic types (`CREATE (from)-[newRel:$(newType)]->(to) SET newRel = properties(oldRel) DELETE oldRel`). The current APOC procedure still works in this runtime; future renames should prefer the dynamic-type syntax once Neo4j 6+ is in production.

5. **Phase 3 readiness.** Agent 7's exit state satisfies all preconditions for Phase 3 (era / pollutant / decision-shelf inference): every edge has a canonical evidence shape, the donor/receiver topology is unambiguous (`FROM_DONOR` vs `INTO_RECEIVER`), and the strict-enum basis values give Phase 3 a clean substrate to introduce `'era_and_material'`, `'material_only'`, `'era_only'`, and `'documented'` basis values on the new `:HAS_RISK_POLLUTANT` / `:REQUIRES_VERIFICATION_FOR` edges it creates.

Agent 7 stops here.
