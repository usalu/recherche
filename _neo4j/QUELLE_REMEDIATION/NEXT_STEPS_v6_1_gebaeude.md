# Q-EXT v6.1 gebaeude - next steps

**Date:** 2026-05-22  
**State:** v6.1 gebaeude JSONL import executed against `mit-bestand`.

This plan starts from the executed state documented in
[REFACTOR_v6_1_gebaeude_concrete.md](REFACTOR_v6_1_gebaeude_concrete.md).
It keeps the current rule intact: raw dossier targets are reviewable evidence
targets, not automatically merged into semantic graph nodes by name similarity.

---

## Current baseline

Live import result:

| Metric | Count |
|---|---:|
| `:CITED_FROM_DOSSIER` edges from v6.1 gebaeude | 6,150 |
| Distinct `source_url` values | 388 |
| Dossiers touched | 71 |
| `DossierEntityTarget` nodes | 2,591 |
| `EXACT_MATCH_CANDIDATE` review edges | 306 |
| Ambiguous exact candidates | 3 |
| Unresolved raw targets | 2,282 |
| Remaining legacy `:ZITIERT_QUELLE` relationships | 8,229 |

Pre-write backup:
- `_neo4j/review/backups/2026-05-22_pre_qext_v6_1_gebaeude`

Primary artefacts:
- Runner: `_neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_v6_1_gebaeude_runner.py`
- Report: `_neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/reports/qext_v6_1_gebaeude_import_report.md`
- Input triples: `_neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/unfold_all_gebaeude_triples.jsonl`

Known baseline residuals from `_scripts/_gap_survey.py` predate this import.
Do not attribute those existing FAIL rows to v6.1 unless a before/after diff
proves a regression.

---

## Phase 0 - freeze and audit the executed import

Goal: prove the current v6.1 import is stable before any semantic promotion.

Run:

```bash
python _scripts/_gap_survey.py
python -m py_compile _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_v6_1_gebaeude_runner.py
python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_v6_1_gebaeude_runner.py
```

Acceptance checks:

```cypher
MATCH (:DossierEntityTarget)-[r:CITED_FROM_DOSSIER]->(:Dossier)
WHERE r.migration_origin = 'qext_v6_1_gebaeude_unfolder'
RETURN count(r) AS edges,
       count(DISTINCT r.source_url) AS urls,
       count(DISTINCT r.dossier_id) AS dossiers,
       count(DISTINCT r.entity_type + '\u001f' + r.entity_value) AS targets;
```

Expected:
- `edges = 6150`
- `urls = 388`
- `dossiers = 71`
- `targets = 2591`
- no v6.1-created relationship with `r.id IS NULL`
- no v6.1-created node with `source_scope IS NULL`

Deliverable:
- Add a short audit note under `_neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/reports/`.

---

## Phase 1 - review exact candidates, do not auto-merge

Goal: turn the 306 exact candidates into an explicit review queue.

Export review rows:

```cypher
MATCH (t:DossierEntityTarget)-[:EXACT_MATCH_CANDIDATE]->(n)
WHERE t.migration_origin = 'qext_v6_1_gebaeude_unfolder'
RETURN t.id AS target_id,
       t.entity_type AS entity_type,
       t.entity_value AS raw_value,
       labels(n) AS candidate_labels,
       n.id AS candidate_id,
       n.name AS candidate_name
ORDER BY entity_type, raw_value;
```

Decision states:

| Review state | Meaning |
|---|---|
| `accepted_same_entity` | Safe to attach v6.1 citations to the domain node. |
| `rejected_not_same_entity` | Exact text matched, but semantic identity differs. |
| `needs_human_context` | Needs dossier inspection before action. |

Implementation rule:
- Use a separate reviewed patch/import file for accepted links.
- Do not mutate or delete `DossierEntityTarget` nodes; they remain provenance records.
- Accepted links may add `(:DomainNode)-[:CITED_FROM_DOSSIER]->(:Dossier)` edges copied from the target, with `review_status = 'accepted_same_entity'`.

Acceptance:
- Every promoted edge carries `source_url`, `locator`, `dossier_id`, `review_status`, `reviewed_at`, and `reviewed_by`.
- Rejected candidates are queryable, not silently discarded.

---

## Phase 2 - resolve the five zero-triple dossiers

Goal: recover safe citations from the known abbreviation/list-format misses.

Zero-triple dossiers:
- `CRCLR_House_Impact_Hub_Berlin.md`
- `ELYS_Kultur_Gewerbehaus_Basel.md`
- `Europa_Building_Brussels.md`
- `Institut_de_Botanique_ULg_Liege.md`
- `Thoravej_29_Copenhagen.md`

Action:
1. Create a per-dossier alias overlay, for example:

```yaml
crclr_house_impact_hub_berlin:
  CMS: "Circular Material Systems"
```

2. Extend `test_gebaeude_unfolder.py` to load the overlay.
3. Re-run `unfold_all_gebaeude.py`.
4. Compare new totals against the current 6,150-edge baseline.
5. Import only the delta, preserving the same `CITED_FROM_DOSSIER` contract.

Acceptance:
- Alias entries are explicit and reviewed.
- Any still-unresolved reference remains visible in summary output.
- No abbreviation is globally inferred across dossiers.

---

## Phase 3 - build the unresolved-target review queue

Goal: make the 2,282 unresolved raw targets useful without fuzzy merging.

Prioritise by edge volume:

```cypher
MATCH (t:DossierEntityTarget)-[r:CITED_FROM_DOSSIER]->(:Dossier)
WHERE t.review_status = 'unresolved_no_exact_match'
RETURN t.entity_type AS entity_type,
       t.entity_value AS raw_value,
       count(r) AS citations,
       count(DISTINCT r.dossier_id) AS dossiers
ORDER BY citations DESC, dossiers DESC
LIMIT 200;
```

Recommended review order:
1. High-volume `People`, `Projekt`, `Gebaeude`, `Bauteil`, `Material`.
2. Controlled-vocabulary-like rows (`kennwert`, `huerde`, `prozessphase`, `thema`) that may be row claims rather than entities.
3. Long comma-separated actor lists, which should be split only after manual review.

Deliverable:
- `_neo4j/review/qext_v6_1_gebaeude_target_review.queue.jsonl`

Each queue row should include:
- target id
- raw value
- entity type
- citation count
- sample dossier locators
- proposed action
- review status

---

## Phase 4 - update user-facing source queries

Goal: make `:CITED_FROM_DOSSIER.source_url` visible in normal lookup scripts and docs.

Update candidates:
- `_scripts/find_sources.py`
- `_neo4j/QUELLE_QUERY_GUIDE.md`
- any S5 visibility runner that still reads only `BELEGT_IN -> Dossier -> ZITIERT_QUELLE`

New source traversal should include:

```cypher
MATCH (n)-[c:CITED_FROM_DOSSIER]->(d:Dossier)
WHERE c.source_url IS NOT NULL
RETURN n.id, d.id, c.locator, c.source_url;
```

Acceptance:
- Looking up a v6.1 target or accepted domain node shows direct edge URLs.
- Legacy `:ZITIERT_QUELLE` paths still work until the broader v6.C migration is executed.

---

## Phase 5 - decide and stage `kill_zitiert_quelle`

Goal: prepare, but not casually run, the broader v6.C migration.

Current boundary:
- v6.1 imported gebaeude row citations.
- It did not remove `:ZITIERT_QUELLE`.
- `:ZITIERT_QUELLE` still has 8,229 relationships across dossier, research, external-link, section-ref, actor, and ontology paths.

Required before execution:
1. Classify all `:ZITIERT_QUELLE` start/end label pairs.
2. Decide which are safe to convert to direct edge properties.
3. Write a dry-run report with counts by path type.
4. Back up the graph.
5. Execute in a separate migration with rollback.

Do not run a global delete until non-gebaeude source chains have a tested replacement.

---

## Phase 6 - provenance taxonomy for accepted domain nodes

Goal: stamp accepted edges and nodes with the v6 taxonomy without overwriting older evidence.

For accepted domain-node citations:
- `unfolding_kind = 'dossier_row'`
- `unfolding_origin = <dossier_id>/<locator>`
- `migration_origin` appends the review migration id

For raw `DossierEntityTarget` nodes:
- keep `source_scope = 'dossier_entity_target'`
- keep `review_status`
- do not pretend unresolved targets are canonical semantic nodes

Acceptance:
- Accepted citation edges are one-hop source evidence.
- Raw targets remain available for audit and rollback.

---

## Phase 7 - final sign-off gates

Run after each phase:

```bash
python _scripts/_gap_survey.py
```

Core v6.1 gates:

```cypher
MATCH (:DossierEntityTarget)-[r:CITED_FROM_DOSSIER]->(:Dossier)
WHERE r.migration_origin = 'qext_v6_1_gebaeude_unfolder'
RETURN count(r) AS edges;
```

Expected: `6150` until alias-delta work is intentionally imported.

```cypher
MATCH ()-[r:CITED_FROM_DOSSIER]->()
WHERE r.source_url IS NULL OR r.locator IS NULL OR r.dossier_id IS NULL
RETURN count(r) AS bad_edges;
```

Expected: `0`.

```cypher
MATCH (t:DossierEntityTarget)
WHERE t.migration_origin = 'qext_v6_1_gebaeude_unfolder'
  AND t.review_status IS NULL
RETURN count(t) AS missing_review_status;
```

Expected: `0`.

Final deliverable:
- a short report with before/after counts, changed files, and residuals.

