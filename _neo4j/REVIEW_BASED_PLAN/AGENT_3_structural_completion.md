# Agent 3 — Structural completion (R3 + R9)

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.** This brief assumes you have.

You are agent 3 of 5. You add the two structural edges that a first-time graph user expects but the current schema does not have, and you rename the misleading `:ASSOZIIERT_MIT_PROJEKT` type to make actor-stub semantics honest.

---

## §1 Cold-start context

Two important traversals in `mit-bestand` are unnecessarily indirect:

1. **`:Projekt → :Bauwerk` requires multi-hop.** There is no direct edge between a project and the buildings it involves. The current path is `(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR|INTO_RECEIVER]->(:Bauwerk)`. A project with zero Bauteilgruppen has no reachable building, even if the dossier explicitly names buildings. 101 projects, 186 buildings — the 1.84:1 ratio implies most projects involve multiple buildings, but nobody can ask "show me projects involving more than 3 buildings" without 2-hop traversal and deduplication.

2. **`:ReuseRule → :Projekt` requires manual join.** The 20 `:ReuseRule` nodes are connected to `:Land` and `:Material`. To ask "which rules apply to Holbein Gardens?" you must self-join through Holbein's country and materials. The rules are decision-grade content, but the graph treats them as text-on-nodes.

Plus, `:ASSOZIIERT_MIT_PROJEKT` (200 edges) is documented as "registry stub, needs_verification=true" but the type name reads exactly like the verified `:BETEILIGT_AN` edge. 26 % of actor↔project edges are silently mixed in naive queries.

Your job is to add the two missing edges and rename the misleading type.

---

## §2 Mission

### §2.1 Phase R3 — Add the two missing structural edges

- `(:Projekt)-[:HAS_BAUWERK {role: 'donor'|'receiver'}]->(:Bauwerk)` derived from the BG topology.
- `(:ReuseRule)-[:RELEVANT_FOR]->(:Projekt)` derived from country×material match.

Both edges carry `evidence_origin='topology_synthesized'` (they are derived from existing topology). That classification only works after Agent 1's R1 extends the enum.

### §2.2 Phase R9 — Rename `:ASSOZIIERT_MIT_PROJEKT` to `:STUB_PROJECT_LINK`

A `apoc.refactor.rename.type` operation. After the rename, any naive `MATCH (a:Akteur)-[:BETEILIGT_AN]->(:Projekt)` query no longer accidentally includes the stubs. Users who want to include stubs must explicitly write `MATCH (a:Akteur)-[:BETEILIGT_AN|STUB_PROJECT_LINK]->(:Projekt)`.

---

## §3 Dependencies

| Stage | You run | After / before |
|---|---|---|
| Stage 2 | R3 | After: Agent 1 R1 (you write `evidence_origin='topology_synthesized'`); After: Agent 5 R7.a/b (so the 7 orphan projects exist before you wire `:HAS_BAUWERK`). Best to start once both done flags exist. |
| Stage 3 | R9 | After: R3 fully merged. R9 is a single rename, fast. |

You block Agent 1 R8 (R8 seed pass references `:STUB_PROJECT_LINK`) and Orchestrator Stage 4 audit.

---

## §4 Conflict avoidance

You write:
- New `:HAS_BAUWERK` edges (R3.a)
- New `:RELEVANT_FOR` edges (R3.b)
- Renamed `:STUB_PROJECT_LINK` (R9) — was `:ASSOZIIERT_MIT_PROJEKT`

You read:
- `:HAT_BAUTEILGRUPPE`, `:FROM_DONOR`, `:INTO_RECEIVER`
- `:APPLIES_IN`, `:APPLIES_TO`, `:NUTZT_MATERIAL`, `:LIEGT_IN_LAND`
- `:ASSOZIIERT_MIT_PROJEKT` (the rename target)

You MUST NOT:
- Touch any other rel type.
- Modify `:Akteur`, `:Projekt`, `:Bauwerk` node properties.
- Touch evidence properties on edges other than the new ones you create.
- Delete or merge any nodes.

---

## §5 Pre-flight checklist

```bash
# 1. Verify Agent 1 R1 has landed
ls _neo4j/intake/runs/2026-05-21_review_based_plan/agent_1_evidence_honesty/PHASE_R1_DONE.flag

# 2. Verify Agent 5 R7.a/b has landed (7 new projects exist)
ls _neo4j/intake/runs/2026-05-21_review_based_plan/agent_5_loader_hardening/PHASE_R7_DONE.flag
# (or check intermediate flag PHASE_R7_AB_DONE.flag)

# 3. Verify baseline counts
#    :HAT_BAUTEILGRUPPE: 369
#    :FROM_DONOR: 286
#    :INTO_RECEIVER: 349
#    :HAS_BAUWERK: 0 (not yet created)
#    :ReuseRule: 20
#    :APPLIES_IN: 20  :APPLIES_TO: 20
#    :ASSOZIIERT_MIT_PROJEKT: 200

# 4. Branch
git switch -c agent3/r3-r9-structure

# 5. Verify APOC available (for rename.type in R9)
# CALL apoc.help('refactor.rename');
```

---

## §6 Migrations

### §6.1 R3.a — `:Projekt-[:HAS_BAUWERK]->:Bauwerk`

```cypher
// ==========================================================================
// mig_r3_a_has_bauwerk
// Derive direct :Projekt→:Bauwerk edges from the BG donor/receiver topology.
// The `role` property distinguishes donor vs receiver paths.
// If a building is both donor and receiver for the same project, TWO edges
// are created (one per role) so the aggregation is honest.
// ==========================================================================

// R3.a.1 — donor edges
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR]->(b:Bauwerk)
MERGE (p)-[h:HAS_BAUWERK {role: 'donor'}]->(b)
ON CREATE SET h.evidence_origin = 'topology_synthesized',
              h.evidence_basis = 'derived_from_bg_topology',
              h.evidence_confidence = 'teilweise_belegt',
              h.evidence_source_id = 'r3_a_topology',
              h.evidence_excerpt = NULL,
              h.derivation_note = 'Aggregated from (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:FROM_DONOR]->(b).',
              h.migration_origin = 'mig_r3_a_has_bauwerk';

// R3.a.2 — receiver edges
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:INTO_RECEIVER]->(b:Bauwerk)
MERGE (p)-[h:HAS_BAUWERK {role: 'receiver'}]->(b)
ON CREATE SET h.evidence_origin = 'topology_synthesized',
              h.evidence_basis = 'derived_from_bg_topology',
              h.evidence_confidence = 'teilweise_belegt',
              h.evidence_source_id = 'r3_a_topology',
              h.evidence_excerpt = NULL,
              h.derivation_note = 'Aggregated from (p)-[:HAT_BAUTEILGRUPPE]->(bg)-[:INTO_RECEIVER]->(b).',
              h.migration_origin = 'mig_r3_a_has_bauwerk';

// Audits
MATCH ()-[r:HAS_BAUWERK]->() RETURN 'has_bauwerk_total' AS check, count(r) AS c;
MATCH ()-[r:HAS_BAUWERK {role:'donor'}]->() RETURN 'has_bauwerk_donor' AS check, count(r) AS c;
MATCH ()-[r:HAS_BAUWERK {role:'receiver'}]->() RETURN 'has_bauwerk_receiver' AS check, count(r) AS c;

// Sanity: every Projekt with at least one HAT_BAUTEILGRUPPE-→FROM_DONOR path
// must now have at least one HAS_BAUWERK edge.
MATCH (p:Projekt)
WHERE exists{ (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR|INTO_RECEIVER]->(:Bauwerk) }
  AND NOT exists{ (p)-[:HAS_BAUWERK]->() }
RETURN 'projekt_with_bg_paths_no_has_bauwerk' AS check, count(p) AS violations;
```

### §6.2 R3.b — `:ReuseRule-[:RELEVANT_FOR]->:Projekt`

```cypher
// ==========================================================================
// mig_r3_b_reuse_rule_relevant_for
// Wire :ReuseRule to :Projekt via country×material match.
// A rule is RELEVANT_FOR a project if:
//   - the project LIEGT_IN_LAND the rule's APPLIES_IN country, AND
//   - the project has at least one Bauteilgruppe that NUTZT_MATERIAL the
//     rule's APPLIES_TO material.
// ==========================================================================

MATCH (rule:ReuseRule)-[:APPLIES_IN]->(l:Land)<-[:LIEGT_IN_LAND]-(p:Projekt),
      (rule)-[:APPLIES_TO]->(m:Material)
WHERE exists{
  (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
}
MERGE (rule)-[r:RELEVANT_FOR]->(p)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'country_material_match',
              r.evidence_confidence = 'teilweise_belegt',
              r.evidence_source_id = 'r3_b_topology',
              r.evidence_excerpt = NULL,
              r.derivation_note = 'Country×Material match. Country: ' + l.id +
                                  '. Material: ' + m.id + '. Rule: ' + rule.id + '.',
              r.migration_origin = 'mig_r3_b_reuse_rule_relevant_for';

// Audits
MATCH ()-[r:RELEVANT_FOR]->() RETURN 'relevant_for_total' AS check, count(r) AS c;

// Per-rule wiring
MATCH (rule:ReuseRule)
OPTIONAL MATCH (rule)-[r:RELEVANT_FOR]->(:Projekt)
RETURN rule.id AS rule_id, count(r) AS projekt_count
ORDER BY projekt_count DESC, rule_id ASC;

// France exposure check — Ferme du Rail must have ZERO matching rules
// (uncovered country in ReuseRule seed; this is the honest signal)
MATCH (p:Projekt {id:'p_ferme_du_rail_paris'})
OPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p)
RETURN 'ferme_du_rail_rule_count' AS check, count(r) AS c, 0 AS expected_zero;

// UK exposure check — Holbein Gardens must have at least the UK Stahl rule
MATCH (p:Projekt {id:'p_holbein_gardens_london'})
MATCH (rule:ReuseRule)-[r:RELEVANT_FOR]->(p)
RETURN 'holbein_rule_count' AS check, count(r) AS c;
```

### §6.3 R9 — Rename `:ASSOZIIERT_MIT_PROJEKT` → `:STUB_PROJECT_LINK`

Run AFTER R3 is complete and merged.

```cypher
// ==========================================================================
// mig_r9_stub_project_link_rename
// Rename the registry-stub edge type to make its intent visible.
// Uses apoc.refactor.rename.type (identity-preserving, properties intact).
// ==========================================================================

MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
WITH collect(r) AS rels
CALL apoc.refactor.rename.type('ASSOZIIERT_MIT_PROJEKT', 'STUB_PROJECT_LINK', rels)
YIELD batches, total, timeTaken, committedOperations, failedOperations,
      failedBatches, retries, errorMessages
RETURN batches, total, committedOperations, failedOperations;

// Audits
MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN 'old_type_remaining' AS check, count(r) AS violations;
MATCH ()-[r:STUB_PROJECT_LINK]->() RETURN 'new_type_count' AS check, count(r) AS c;

// Confirm every renamed edge retains needs_verification=true property
MATCH ()-[r:STUB_PROJECT_LINK]->()
WHERE r.needs_verification IS NULL OR r.needs_verification = false
RETURN 'stub_without_needs_verification' AS check, count(r) AS violations;
```

---

## §7 Runner script outline

`logs/agent_3_runner.py` should:

1. Run R3.a (write HAS_BAUWERK donor edges).
2. Run R3.b (write RELEVANT_FOR edges).
3. Verify R3 acceptance gates (see §8.1).
4. Write `PHASE_R3_DONE.flag`.
5. Wait for orchestrator merge confirmation.
6. After R3 lands in `orch/integrate-2026-05-21`: pull, run R9.
7. Verify R9 acceptance gates.
8. Write `PHASE_R9_DONE.flag`.

Use the same skeleton as [AGENT_1_evidence_honesty.md](AGENT_1_evidence_honesty.md) §7.

---

## §8 Acceptance gates

### §8.1 R3 acceptance

| Gate | Cypher | Expected |
|---|---|---|
| `:HAS_BAUWERK` total | `MATCH ()-[r:HAS_BAUWERK]->() RETURN count(r)` | ≥ 200 |
| Donor-role count | `MATCH ()-[r:HAS_BAUWERK {role:'donor'}]->() RETURN count(r)` | ≥ 80 |
| Receiver-role count | `MATCH ()-[r:HAS_BAUWERK {role:'receiver'}]->() RETURN count(r)` | ≥ 80 |
| Every project with BG-derived path has `:HAS_BAUWERK` | `MATCH (p:Projekt) WHERE exists{(p)-[:HAT_BAUTEILGRUPPE]->()-[:FROM_DONOR\|INTO_RECEIVER]->(:Bauwerk)} AND NOT exists{(p)-[:HAS_BAUWERK]->()} RETURN count(p)` | 0 |
| `:RELEVANT_FOR` total | `MATCH ()-[r:RELEVANT_FOR]->() RETURN count(r)` | ≥ 5 (could be 20+ given multiple projects per country/material) |
| Holbein Gardens covered | Holbein → ≥ 1 ReuseRule | yes |
| Ferme du Rail uncovered | Ferme du Rail → 0 ReuseRules | yes (the honest signal — France not in seed) |
| Every `:HAS_BAUWERK` carries `evidence_origin='topology_synthesized'` | yes | yes |
| Every `:RELEVANT_FOR` carries `evidence_origin='topology_synthesized'` | yes | yes |

### §8.2 R9 acceptance

| Gate | Cypher | Expected |
|---|---|---|
| Old type gone | `MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->() RETURN count(r)` | 0 |
| New type count | `MATCH ()-[r:STUB_PROJECT_LINK]->() RETURN count(r)` | 200 |
| `needs_verification` preserved | `MATCH ()-[r:STUB_PROJECT_LINK]->() WHERE r.needs_verification IS NULL OR r.needs_verification=false RETURN count(r)` | 0 |
| Sample edge property check | `MATCH ()-[r:STUB_PROJECT_LINK]->() RETURN r LIMIT 1` | shows all old properties intact |

---

## §9 Rollback

### §9.1 R3 rollback

```cypher
MATCH ()-[r:HAS_BAUWERK]->() WHERE r.migration_origin = 'mig_r3_a_has_bauwerk' DELETE r;
MATCH ()-[r:RELEVANT_FOR]->() WHERE r.migration_origin = 'mig_r3_b_reuse_rule_relevant_for' DELETE r;
```

### §9.2 R9 rollback

```cypher
MATCH ()-[r:STUB_PROJECT_LINK]->()
WITH collect(r) AS rels
CALL apoc.refactor.rename.type('STUB_PROJECT_LINK', 'ASSOZIIERT_MIT_PROJEKT', rels)
YIELD total RETURN total;
```

---

## §10 Open decisions affecting your phase

- **D3** (Bauteilgruppe `:DERIVED_FROM` chain edges): **Defer.** Current data is too sparse to motivate adding a third reuse-chain edge type (we already have `TEIL_VON_KETTE` on `:Wiederverwendungskette`). Note this in your report.

If you encounter a project that has `BELEGT_IN→case_markdown` but no BG path to any Bauwerk (so R3.a creates no edge for it), record the situation as a residual `:DataIssue` (the R8 seed pass will pick this up via its `dossier_section8_missing` kind or you can add a new kind `projekt_no_building_path`):

```cypher
MATCH (p:Projekt)
WHERE exists{(p)-[:BELEGT_IN]->(:Quelle {quelltyp:'case_markdown'})}
  AND NOT exists{(p)-[:HAS_BAUWERK]->()}
WITH p
MERGE (i:DataIssue {id: 'di_projekt_no_building_path__' + p.id})
ON CREATE SET i.kind = 'projekt_no_building_path',
              i.severity = 'medium',
              i.ref_label = 'Projekt',
              i.ref_id = p.id,
              i.found_at = date(),
              i.found_by = 'agent_3_r3_residual',
              i.status = 'open',
              i.resolution_note = 'Project has dossier anchor but no Bauteilgruppe→Bauwerk topology; check ingestion.'
MERGE (i)-[:CONCERNS]->(p);
```

(This bypasses Agent 1 R8's seed pass for issues you observe directly. Coordinate with Agent 1 to avoid duplicate `:DataIssue` ids — use a distinct `found_by` value.)

---

## §11 Handoff

After R3:

1. Push `agent3/r3-r9-structure` to remote with R3 commits.
2. Update [HANDOFF_LOG.md](HANDOFF_LOG.md): `| <date> | agent_3 | R3 complete (HAS_BAUWERK: X, RELEVANT_FOR: Y) | <PR> | PASS |`.
3. Wait for orchestrator merge.

After R9:

4. Run R9 on integrated branch.
5. Verify acceptance.
6. Push R9 commit.
7. Update log.

---

## §12 Report contents

Standard template plus:

- `:HAS_BAUWERK` distribution: donor vs receiver counts per `:Projekt` (top 20).
- `:RELEVANT_FOR` per rule: list each rule with its target project count.
- Confirmation that France-based projects are uncovered (the honest exposure).
- Old vs new `:ASSOZIIERT_MIT_PROJEKT` / `:STUB_PROJECT_LINK` count.
- Any residual `:DataIssue` nodes you created.

---

**End of AGENT_3_structural_completion.md.**
