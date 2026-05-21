# Agent 5 — Loader hardening (R7)

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.** This brief assumes you have.

You are agent 5 of 5. You own the dossier-side coherence: 7 orphan dossiers without matching projects, 16 dossiers with parallel naming conventions, the missing Section-8 facts extraction, and the dossier-vs-graph schema drift detection.

---

## §1 Cold-start context

The dossier ingestion pipeline (agents 9–11 in `2026-05-20_radical_quality_reset`) left three documented coherence failures, all surfaced in the third layer of the skeptical review:

### §1.1 The 16 dual-naming Quelle pairs

For 16 dossiers, two `:Quelle` nodes coexist:
- `q_<slug>_md` — created by Agent 9 in the new naming convention
- `qu_*_dossier` — left over from an earlier batch loader

Agent 9's report ([agent_9_phase4b1_report.md](../intake/runs/2026-05-20_radical_quality_reset/reports/agent_9_phase4b1_report.md) §"Legacy `qu_*_dossier` case_markdown anchors not touched") explicitly says these 16 were "intentionally NOT touched" — pending reconciliation. ZITIERT_QUELLE chains may be split across the two; users find one anchor and miss the other.

### §1.2 The 7 orphan dossiers

7 dossiers have no matching `:Projekt`:

| Dossier | Suggested resolution |
|---|---|
| `q_circl_pavilion_amsterdam_md` | Create standalone `:Projekt {id:'p_circl_pavilion_amsterdam'}` |
| `q_re_use_hoefe_wien_md` | Create standalone `:Projekt {id:'p_re_use_hoefe_wien'}` |
| `q_berlin_schildow_pilot_house_2_md` | Sibling of `p_berlin_schildow_pilot_house`; create with explicit `:DERIVED_FROM` to sibling |
| `q_eth_circular_construction_programme_md` | Create as `:Programm {id:'p_eth_circular_construction_programme'}` |
| `q_fcrbe_facilitating_circulation_reclaimed_building_elements_md` | Create as `:Programm` |
| `q_rebridge_structural_reuse_md` | Create as `:Programm` |
| `q_refair_bordeaux_md` | Create as `:Programm` (D8 default) |

These are exactly the cross-cutting meta-projects (teaching programmes, EU consortia, platforms) that would have given the graph systemic context.

### §1.3 The Section-8 unevenness

The Section-8 extraction (cost, CO₂, reuse-share facts) ran on each dossier with wildly varying yield. Some dossiers (Stuttgart 210, Circl Pavilion Amsterdam, ETH Circular Construction Programme) show 0 Section-8 facts despite their source text containing explicit numbers ("55–98 % reuse-material share", "5,000 m³ CLT potential", "ca. 1.8 million EUR"). The loader missed those cells.

### §1.4 Dossier-vs-graph schema drift

Dossiers still write retired type names (`AUS_BAUWERK`, `EINGEBAUT_IN`, `LebenszyklusModul`, `Tool`, `ZertifizierungBewertungssystem`). The next ingestion will silently drop these cells unless a translator runs first.

---

## §2 Mission

### §2.1 Phase R7 — Dossier loader hardening, four sub-steps

| Sub-step | What | When |
|---|---|---|
| R7.a | Reconcile the 16 dual-naming `:Quelle` pairs (merge `qu_*` into `q_<slug>_md`) | Stage 1 (parallel-safe) |
| R7.b | Resolve the 7 orphan dossiers (create the 7 missing nodes) | Stage 1 (parallel-safe) |
| R7.c | Re-extract Section-8 facts and emit `:Kennwert` nodes via Agent 4's R4 schema | Stage 2 (after R4) |
| R7.d | Populate `:Quelle.text_content` for `case_markdown` Quellen + dossier-schema drift validator | Stage 2 (parallel-safe with R7.c) |

---

## §3 Dependencies

| Stage | You run | After / before |
|---|---|---|
| Stage 1 | R7.a, R7.b | After: orchestrator baseline snapshot. Parallel-safe. **Blocks Agent 3 R3** (R3 needs the 7 new projects to exist before `:HAS_BAUWERK` aggregation runs). |
| Stage 2 | R7.c | After: Agent 4 R4 (you use R4's `:Kennwert` schema). |
| Stage 2 | R7.d | After: orchestrator baseline. Parallel with R7.c. |

You block:
- Agent 3 R3 (R7.a/b must finish first).
- Agent 1 R8 (R7.d's drift detection feeds R8's `:DataIssue` seed).

---

## §4 Conflict avoidance

You write:
- New `:Projekt` and `:Programm` nodes (7 total in R7.b).
- Merge of `qu_*_dossier` into `q_<slug>_md` via `apoc.refactor.mergeNodes` (R7.a) — this DELETES the `qu_*` shell after migrating edges.
- New `:Kennwert` nodes + `:HAT_KENNWERT` edges (R7.c) — using Agent 4's schema.
- New `:Quelle.text_content` property on `case_markdown` Quellen (R7.d).
- New `:DataIssue` nodes for dossier-schema drift findings (R7.d).

You read:
- All `:Quelle` nodes with `quelltyp='case_markdown'`.
- Dossier `.md` files under `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/` and `_archive/research/gebaeude/`.
- Agent 4's `:Kennwert` schema (when R7.c runs).

You MUST NOT:
- Modify any other Projekt's properties.
- Touch existing evidence properties on edges (Agent 1's domain).
- Restore demoted labels (Agent 2's domain).
- Add `:HAS_BAUWERK` edges (Agent 3's domain).

---

## §5 Pre-flight checklist

```bash
# 1. Verify baseline
ls _neo4j/intake/runs/2026-05-21_review_based_plan/baseline_snapshot/

# 2. Verify the 16 dual-naming pairs exist (from agent_9 report)
# MATCH (q1:Quelle), (q2:Quelle)
# WHERE q1.id STARTS WITH 'qu_' AND q1.id ENDS WITH '_dossier'
#   AND q2.id STARTS WITH 'q_' AND q2.id ENDS WITH '_md'
#   AND substring(q1.id, 3, size(q1.id)-11) =
#       substring(q2.id, 2, size(q2.id)-5)
# RETURN q1.id, q2.id LIMIT 20

# 3. Verify the 7 orphan dossiers exist as Quelle but no matching Projekt
# MATCH (q:Quelle {quelltyp:'case_markdown'})
# WHERE NOT exists{
#   MATCH (p:Projekt)-[:BELEGT_IN]->(q)
# }
# RETURN q.id

# 4. Branch
git switch -c agent5/r7-loader
```

---

## §6 Migrations

### §6.1 R7.a — Merge dual-naming `:Quelle` pairs

```cypher
// ==========================================================================
// mig_r7_a_dual_naming_merge
// For each pair (q_old=qu_*_dossier, q_new=q_<slug>_md):
//   - move all edges from q_old to q_new (apoc.refactor.mergeNodes)
//   - add q_old.id to q_new.aliases
//   - delete q_old shell
// Pre-condition: 16 pairs (per agent_9 report).
// ==========================================================================

// Runner provides $pairs parameter with the 16 matched pairs.
UNWIND $pairs AS pair
MATCH (q_old:Quelle {id: pair.old_id}),
      (q_new:Quelle {id: pair.new_id})
CALL apoc.refactor.mergeNodes([q_new, q_old], {
  properties: 'discard',  // keep q_new properties; q_old's are alias-recorded below
  mergeRels: true
}) YIELD node
SET node.aliases = apoc.coll.toSet(coalesce(node.aliases, []) + [pair.old_id]),
    node.migration_origin = coalesce(node.migration_origin, '') + ' | mig_r7_a_dual_naming_merge'
RETURN node.id AS canonical_id, node.aliases AS aliases;

// Audits
MATCH (q:Quelle) WHERE q.id STARTS WITH 'qu_' AND q.id ENDS WITH '_dossier'
RETURN 'qu_dossier_remaining' AS check, count(q) AS violations;

MATCH (q:Quelle) WHERE q.aliases IS NOT NULL AND any(a IN q.aliases WHERE a STARTS WITH 'qu_')
RETURN 'q_md_with_qu_alias' AS check, count(q) AS c;
```

### §6.2 R7.b — Create the 7 orphan node targets

```cypher
// ==========================================================================
// mig_r7_b_resolve_orphan_dossiers
// Create the 7 missing :Projekt / :Programm nodes so dossier citations land.
// ==========================================================================

UNWIND [
  {target_label:'Projekt',  id:'p_circl_pavilion_amsterdam',
   name:'Circl Pavilion Amsterdam',  dossier_quelle:'q_circl_pavilion_amsterdam_md'},
  {target_label:'Projekt',  id:'p_re_use_hoefe_wien',
   name:'Re-Use Höfe Wien',          dossier_quelle:'q_re_use_hoefe_wien_md'},
  {target_label:'Projekt',  id:'p_berlin_schildow_pilot_house_2',
   name:'Berlin Schildow Pilot House 2', dossier_quelle:'q_berlin_schildow_pilot_house_2_md',
   sibling_of:'p_berlin_schildow_pilot_house'},
  {target_label:'Programm', id:'p_eth_circular_construction_programme',
   name:'ETH Circular Construction Programme',
   dossier_quelle:'q_eth_circular_construction_programme_md'},
  {target_label:'Programm', id:'p_fcrbe_facilitating_circulation_reclaimed_building_elements',
   name:'FCRBE — Facilitating Circulation of Reclaimed Building Elements',
   dossier_quelle:'q_fcrbe_facilitating_circulation_reclaimed_building_elements_md'},
  {target_label:'Programm', id:'p_rebridge_structural_reuse',
   name:'REBRIDGE Structural Reuse',
   dossier_quelle:'q_rebridge_structural_reuse_md'},
  {target_label:'Programm', id:'p_refair_bordeaux',
   name:'REFAIR Bordeaux',
   dossier_quelle:'q_refair_bordeaux_md'}
] AS row
CALL apoc.create.node([row.target_label], {
  id: row.id,
  name: row.name,
  source_scope: 'r7_b_orphan_resolution',
  migration_origin: 'mig_r7_b_resolve_orphan_dossiers',
  needs_dossier_extraction: true,
  evidence_origin: 'source_curated',
  evidence_basis: 'dossier_anchored',
  evidence_confidence: 'belegt'
}) YIELD node
WITH row, node
MATCH (q:Quelle {id: row.dossier_quelle})
MERGE (node)-[r:BELEGT_IN]->(q)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = q.id,
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r7_b_resolve_orphan_dossiers'
WITH row, node
WHERE row.sibling_of IS NOT NULL
MATCH (sibling) WHERE sibling.id = row.sibling_of
MERGE (node)-[s:DERIVED_FROM]->(sibling)
ON CREATE SET s.evidence_origin = 'source_curated',
              s.evidence_basis = 'sibling_dossier_relation',
              s.evidence_confidence = 'teilweise_belegt',
              s.evidence_excerpt = 'Berlin Schildow Pilot House 2 is the second pilot in the same programme as ' + row.sibling_of + '.',
              s.migration_origin = 'mig_r7_b_resolve_orphan_dossiers';

// Audits
MATCH (n) WHERE n.id IN [
  'p_circl_pavilion_amsterdam',
  'p_re_use_hoefe_wien',
  'p_berlin_schildow_pilot_house_2',
  'p_eth_circular_construction_programme',
  'p_fcrbe_facilitating_circulation_reclaimed_building_elements',
  'p_rebridge_structural_reuse',
  'p_refair_bordeaux'
]
RETURN 'orphan_resolution_count' AS check, count(n) AS c;

// Confirm orphan dossiers now have a project
MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE NOT exists{
  MATCH (n)-[:BELEGT_IN]->(q) WHERE n:Projekt OR n:Programm
}
RETURN 'case_markdown_still_orphan' AS check, count(q) AS violations;
```

### §6.3 R7.c — Section-8 re-extraction → `:Kennwert`

Runs AFTER Agent 4 R4 lands. Driver-side Python script:

1. For each `:Quelle {quelltyp:'case_markdown'}`, locate the original dossier `.md` file via `q.source_file` or `q.aliases`.
2. Parse the dossier's "Economy / Wirtschaft" section, "co2 / CO₂" tables, "reuse_share / Wiederverwendungsanteil" rows.
3. For each numerical cell with units (`(\d+(?:\.\d+)?(?:-\d+(?:\.\d+)?)?)\s*(%|t|kg|m2|m3|EUR|€|m)`), emit a `:Kennwert` MERGE:

```python
# Pseudocode — runner side
for dossier_path, projekt_id, quelle_id in dossier_projekt_pairs:
    text = Path(dossier_path).read_text(encoding='utf-8')
    facts = extract_section8_facts(text)   # regex + heuristics
    for i, fact in enumerate(facts):
        cypher = '''
        MATCH (p:Projekt {id: $projekt_id})
        MERGE (kw:Kennwert {id: $kw_id})
        ON CREATE SET kw.category = $category,
                      kw.kennwert = $kennwert,
                      kw.wert = $wert,
                      kw.wert_text = $wert_text,
                      kw.wert_min = $wert_min,
                      kw.wert_max = $wert_max,
                      kw.einheit = $einheit,
                      kw.method = $method,
                      kw.bilanzgrenze = $bilanzgrenze,
                      kw.loader = 'r7_c_section8_extractor',
                      kw.source_id = $quelle_id,
                      kw.source_scope = 'r7_c_section8_reextract',
                      kw.migration_origin = 'mig_r7_c_section8_kennwert'
        MERGE (p)-[r:HAT_KENNWERT]->(kw)
        ON CREATE SET r.evidence_origin = 'source_curated',
                      r.evidence_basis = 'cell_citation',
                      r.evidence_confidence = $confidence,
                      r.evidence_source_id = $quelle_id,
                      r.evidence_excerpt = $excerpt,
                      r.migration_origin = 'mig_r7_c_section8_kennwert'
        '''
        session.run(cypher, projekt_id=projekt_id, kw_id=..., ...)
```

Confidence rules:
- Cell has explicit unit + single number → `belegt`.
- Cell has a range or "ca." / "approx." → `teilweise_belegt`.
- Cell carries phrases like "unknown", "TBD" → skip (do NOT create a `:Kennwert`).

### §6.4 R7.d — `Quelle.text_content` + drift validator

```cypher
// ==========================================================================
// mig_r7_d_quelle_text_content + drift validator
// For case_markdown :Quelle, store the full markdown text on the node
// (gated by D9=yes). This unlocks Agent 9 R9.b's text-matching stub-promotion.
// ==========================================================================

// Runner side: read each dossier .md and SET q.text_content.
// Cypher pattern (per dossier):
MATCH (q:Quelle {id: $quelle_id, quelltyp: 'case_markdown'})
SET q.text_content = $full_markdown_text,
    q.text_content_loaded_at = date(),
    q.migration_origin = coalesce(q.migration_origin, '') + ' | mig_r7_d_text_content';

// Audits
MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE q.text_content IS NULL
RETURN 'case_markdown_without_text' AS check, count(q) AS c;

MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE q.text_content IS NOT NULL
RETURN 'case_markdown_with_text' AS check, count(q) AS c;
```

**Drift validator** — a separate Python script `_scripts/validate_dossier_schema.py`:

```python
# Pseudocode
RETIRED_LABELS = {
    'LebenszyklusModul', 'ZertifizierungBewertungssystem',
    'Tool', 'RechtlicheBedingung', 'Layer',
    'AUS_BAUWERK', 'EINGEBAUT_IN', 'HAT_SCHADSTOFF'
}

drift_findings = []
for dossier_path in dossier_paths:
    text = Path(dossier_path).read_text(encoding='utf-8')
    for term in RETIRED_LABELS:
        if term in text:
            drift_findings.append((dossier_path, term))

# Emit :DataIssue nodes for each drift finding
for dossier_path, term in drift_findings:
    session.run('''
        MERGE (i:DataIssue {id: 'di_dossier_drift__' + $term + '__' + $dossier_slug})
        ON CREATE SET
          i.kind = 'dossier_uses_retired_type',
          i.severity = 'medium',
          i.ref_label = 'Dossier',
          i.ref_id = $dossier_path,
          i.found_at = date(),
          i.found_by = 'r7_d_drift_validator',
          i.status = 'open',
          i.resolution_note = $note
    ''', term=term, dossier_slug=..., dossier_path=dossier_path,
       note=f'Dossier still references retired type "{term}". Translate to new name in next ingestion.')
```

This script should also be wired into the next pre-flight (gate any future ingestion with `python _scripts/validate_dossier_schema.py`).

---

## §7 Runner script outline

`logs/agent_5_runner.py` runs the four sub-steps in order, with a clean abort if any stage fails:

```python
def main():
    # Stage 1
    run_r7_a()  # merge dual naming
    run_r7_b()  # resolve 7 orphans
    write_flag('PHASE_R7_AB_DONE.flag')

    # Wait for Agent 4 R4 done flag
    while not Path('../agent_4_data_model/PHASE_R4_DONE.flag').exists():
        print('Waiting for Agent 4 R4...')
        sleep(60)

    # Stage 2
    run_r7_c()  # Section-8 → Kennwert
    run_r7_d()  # text_content + drift validator
    write_flag('PHASE_R7_DONE.flag')

if __name__ == '__main__':
    main()
```

---

## §8 Acceptance gates

### §8.1 R7.a acceptance

| Gate | Expected |
|---|---|
| `qu_*_dossier` nodes remaining | 0 |
| `q_<slug>_md` with `qu_*_dossier` in `aliases` | ≥ 16 |
| Total `:Quelle` count | (pre-baseline) − 16 |

### §8.2 R7.b acceptance

| Gate | Expected |
|---|---|
| 7 new nodes exist | 4 `:Programm` + 3 `:Projekt` (`p_circl_pavilion_amsterdam`, `p_re_use_hoefe_wien`, `p_berlin_schildow_pilot_house_2`) |
| Each carries `needs_dossier_extraction=true` | yes |
| Each has `BELEGT_IN → corresponding Quelle` | yes |
| `p_berlin_schildow_pilot_house_2 → DERIVED_FROM → p_berlin_schildow_pilot_house` | yes |
| `case_markdown :Quelle` without `Projekt|Programm` BELEGT_IN | 0 (was 7) |

### §8.3 R7.c acceptance

| Gate | Expected |
|---|---|
| `:Kennwert` nodes from R7.c | ≥ 20 (Section-8 extraction across 100 dossiers should yield ≥ 20 verifiable facts) |
| Stuttgart 210 now has ≥ 2 `:Kennwert` (was 0) | yes |
| Circl Pavilion Amsterdam now has ≥ 1 `:Kennwert` (was 0) | yes |
| Every R7.c `:Kennwert` carries `loader='r7_c_section8_extractor'` | yes |

### §8.4 R7.d acceptance

| Gate | Expected |
|---|---|
| `case_markdown :Quelle` with `text_content` populated | 116 |
| `:DataIssue {kind:'dossier_uses_retired_type'}` | 0 if no drift found, otherwise list with severity=medium |
| `_scripts/validate_dossier_schema.py` exits 0 on clean dossiers | yes |

---

## §9 Rollback

### §9.1 R7.a rollback

Recreate `qu_*_dossier` from journal (each merge produced an entry in `logs/agent_5_r7a_audit.jsonl` with the deleted node's properties + incident edges). Replay the JSONL.

### §9.2 R7.b rollback

```cypher
MATCH (n) WHERE n.migration_origin = 'mig_r7_b_resolve_orphan_dossiers'
DETACH DELETE n;
```

### §9.3 R7.c rollback

```cypher
MATCH (kw:Kennwert) WHERE kw.migration_origin = 'mig_r7_c_section8_kennwert'
DETACH DELETE kw;
```

### §9.4 R7.d rollback

```cypher
MATCH (q:Quelle) WHERE q.text_content_loaded_at IS NOT NULL
REMOVE q.text_content, q.text_content_loaded_at;

MATCH (i:DataIssue {kind: 'dossier_uses_retired_type'}) DETACH DELETE i;
```

---

## §10 Open decisions affecting your phase

- **D8** (`refair_bordeaux` classification): Default `:Programm`. REFAIR is a research consortium output, not a market actor. If you want to instead use `:Marktmodell`, note it in the report.
- **D9** (`Quelle.text_content`): YES — populate for `case_markdown` Quelle. This unlocks Agent 1 R8's residual flagging and future text-matching curation.

---

## §11 Handoff

When R7.a/b are complete:

1. Push `agent5/r7-loader` to remote with R7.a/b commits.
2. Update [HANDOFF_LOG.md](HANDOFF_LOG.md): `| <date> | agent_5 | R7.a+b complete (16 merged, 7 resolved) | <PR> | PASS |`.
3. **Critical: Notify Agent 3** — R3 can now run. Tag in handoff log.

When R7.c/d are complete (after R4 merge):

4. Push R7.c/d commits.
5. Update handoff log.

---

## §12 Report contents

Standard template plus:

- The 16 merged pairs (table: old_id, new_id, edges_transferred).
- The 7 resolved orphans (table: dossier, target_label, target_id).
- Section-8 facts added per project (counts and sample excerpts).
- Drift findings (number of dossiers with retired-type references, per type).
- `Quelle.text_content` population stats.

---

**End of AGENT_5_loader_hardening.md.**
