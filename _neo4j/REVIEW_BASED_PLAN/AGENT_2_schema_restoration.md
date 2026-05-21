# Agent 2 — Schema restoration (R2 + R10)

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.** This brief assumes you have.

You are agent 2 of 5. You restore 5 concepts that the radical-quality-reset (Phase 2.5) collapsed from label-shape into stringly-typed property lists, and then clean up the now-empty registry slots.

---

## §1 Cold-start context

In Phase 2.5 of the radical_quality_reset run, the migration `mig_2_5_label_demotions.cypher` collapsed 5 labels into properties:

| Original label | Demoted to | Live nodes after demote |
|---|---|---|
| `:Layer` (6 nodes) | `:Bauteiltyp.brand_layer` enum string | 0 |
| `:LebenszyklusModul` (5 nodes) | `:Projekt.lca_module_scope` list-of-strings | 0 |
| `:RechtlicheBedingung` (9 nodes) | `<src>.legal_conditions` list with country in brackets | 0 |
| `:ZertifizierungBewertungssystem` (8 nodes) | `:Projekt.certifications` list | 0 |
| `:Tool` (8 nodes) | `:Software {kind:'tool'}` | 0 (relabelled) |

Each collapse lost queryability: "show me all projects sharing a BREEAM certification" went from a clean graph traversal to a list-contains string match. The country edge `(:RechtlicheBedingung)-[:GILT_IN_LAND]->(:Land)` became a substring `[DE,BE]` inside a string. The deleted nodes' original properties are preserved in `_neo4j/intake/runs/2026-05-20_radical_quality_reset/deleted/phase2_5_demoted_nodes.jsonl` and `phase2_5_tool_relabels.jsonl`.

Your job is to reverse that collapse: re-create the nodes, re-create the edges, parse the country brackets out of the strings, and prepare the registry-cleanup audit nodes for the labels/rel-types that genuinely should remain retired.

---

## §2 Mission

### §2.1 Phase R2 — Restore 5 demoted concepts as queryable nodes

For each collapsed concept, restore it as a node, recreate the edges from the property values, and **keep the property as a deprecated mirror** for one ingestion cycle. After Stage 4 acceptance and a successful new dossier batch, the orchestrator may delete the property mirrors (decision D2).

**Tool note:** Instead of restoring `:Tool` as a separate label (which would re-create the artificial split), add `:Tool` as a **secondary label** on the existing `:Software` nodes that carry `kind='tool'`. Neo4j supports multiple labels per node.

### §2.2 Phase R10 — Deprecated-type audit nodes

After R2 lands, audit which labels/rel types remain empty. For each, create a `:DeprecatedType` node that records the rename history. This makes the deprecation queryable — a future user sees both "what's gone" and "where to look instead".

---

## §3 Dependencies

| Stage | You run | After / before |
|---|---|---|
| Stage 2 | R2 | After: orchestrator's baseline snapshot. Stage 1 is parallel-safe; you may start R2 prep then. Best to start R2 main execution after Agent 1 R1 to avoid touching old-enum values. |
| Stage 3 | R10 | After: R2 fully landed. R10 reads the post-R2 empty-label list. |

You do not block any other agent. Orchestrator's Stage 4 audit reads your output.

---

## §4 Conflict avoidance

You write:
- New `:Layer`, `:LCAModule`, `:RechtlicheBedingung`, `:Zertifizierungssystem` nodes
- New `:Tool` secondary label on `:Software {kind:'tool'}` nodes
- New `:TEILT_LAYER`, `:BERECHNET_NACH_MODUL`, `:HAT_RECHTLICHE_BEDINGUNG`, `:HAT_ZERTIFIZIERUNG`, `:GILT_IN_LAND` edges
- New `:DeprecatedType` nodes (R10)

You read:
- `Bauteiltyp.brand_layer`
- `Projekt.lca_module_scope`, `Projekt.lca_module_legacy`
- `<src>.legal_conditions` (on `:Projekt`, `:Bauteilgruppe`, `:Bauwerk`)
- `Projekt.certifications`
- `Software.kind`
- `deleted/phase2_5_demoted_nodes.jsonl` (preserved Properties)
- `deleted/phase2_5_tool_relabels.jsonl`

You MUST NOT:
- Delete the property mirrors yet (D2 says: defer to a separate run).
- Mutate any `evidence_origin` on existing edges (Agent 1's job).
- Touch `:Quelle` or dossier files (Agent 5's job).
- Touch `:Projekt.*_facts` JSON (Agent 4's job).

---

## §5 Pre-flight checklist

```bash
# 1. Verify deleted journals exist
ls _neo4j/intake/runs/2026-05-20_radical_quality_reset/deleted/phase2_5_*.jsonl

# 2. Verify baseline counts (from FINAL_PASS2_AUDIT.md §4.2)
#    :Layer: 0    :LebenszyklusModul: 0    :RechtlicheBedingung: 0
#    :ZertifizierungBewertungssystem: 0
#    :Bauteiltyp: 23 (15 with brand_layer)
#    :Projekt: 101 (some with lca_module_scope, certifications)
#    :Software: 19 (8 with kind='tool')

# 3. Read the property mirrors to confirm data is present
# Sample query:
# MATCH (p:Projekt) WHERE p.certifications IS NOT NULL RETURN p.id, p.certifications

# 4. Verify Agent 1's R1 has landed (or coordinate timing)
ls _neo4j/intake/runs/2026-05-21_review_based_plan/agent_1_evidence_honesty/PHASE_R1_DONE.flag

# 5. Branch from baseline
git switch -c agent2/r2-r10-restore
```

---

## §6 Migrations

### §6.1 R2.a — Restore `:Layer`

```cypher
// ==========================================================================
// mig_r2_a_restore_layer
// Restore :Layer nodes from Bauteiltyp.brand_layer property.
// Recreate TEILT_LAYER edges.
// Pre-condition: deleted/phase2_5_demoted_nodes.jsonl contains 6 :Layer records.
// ==========================================================================

// R2.a.1 — Create :Layer nodes (Brand 6-layer model: site, structure, skin,
//          services, space_plan, stuff; site is project-level so usually unused at BT level)
UNWIND [
  {id:'layer_site',       name:'Site',       brand_position: 1},
  {id:'layer_structure',  name:'Structure',  brand_position: 2},
  {id:'layer_skin',       name:'Skin',       brand_position: 3},
  {id:'layer_services',   name:'Services',   brand_position: 4},
  {id:'layer_space_plan', name:'Space Plan', brand_position: 5},
  {id:'layer_stuff',      name:'Stuff',      brand_position: 6}
] AS row
MERGE (l:Layer {id: row.id})
ON CREATE SET l.name = row.name,
              l.brand_position = row.brand_position,
              l.evidence_origin = 'source_curated',
              l.evidence_basis = 'controlled_vocab',
              l.evidence_source_id = 'q_brand_how_buildings_learn',
              l.evidence_confidence = 'belegt',
              l.source_scope = 'r2_a_layer_restore',
              l.migration_origin = 'mig_r2_a_restore_layer';

// R2.a.2 — Recreate TEILT_LAYER edges from Bauteiltyp.brand_layer
MATCH (bt:Bauteiltyp) WHERE bt.brand_layer IS NOT NULL
MATCH (l:Layer {id: 'layer_' + toLower(replace(bt.brand_layer,' ','_'))})
MERGE (bt)-[r:TEILT_LAYER]->(l)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'controlled_vocab',
              r.evidence_source_id = 'r2_a_layer_restore',
              r.evidence_confidence = 'belegt',
              r.migration_origin = 'mig_r2_a_restore_layer';

// Audits
MATCH (l:Layer) RETURN 'layer_count' AS check, count(l) AS c;
MATCH ()-[r:TEILT_LAYER]->() RETURN 'teilt_layer_count' AS check, count(r) AS c;
MATCH (bt:Bauteiltyp) WHERE bt.brand_layer IS NOT NULL
  AND NOT exists{(bt)-[:TEILT_LAYER]->(:Layer)}
RETURN 'bauteiltyp_with_brand_layer_no_edge' AS check, count(bt) AS violations;
```

### §6.2 R2.b — Restore `:LCAModule`

```cypher
// ==========================================================================
// mig_r2_b_restore_lca_module
// Restore :LCAModule nodes from Projekt.lca_module_scope list.
// Free-text legacy values (a1_a5, unclear, 50y_lifecycle) are moved to
// .lca_module_legacy for transparency.
// ==========================================================================

// R2.b.1 — Normalise: split canonical from legacy
MATCH (p:Projekt)
WHERE p.lca_module_scope IS NOT NULL AND size(p.lca_module_scope) > 0
WITH p,
     [x IN p.lca_module_scope WHERE
        toUpper(x) IN ['A1_A3','A1_A5','A4_A5','B','C1_C4','D']
      | toUpper(x)] AS canonical,
     [x IN p.lca_module_scope WHERE NOT
        toUpper(x) IN ['A1_A3','A1_A5','A4_A5','B','C1_C4','D']] AS free_text
SET p.lca_module_scope = canonical,
    p.lca_module_legacy = free_text;

// R2.b.2 — Create :LCAModule nodes (6 canonical EN 15978 modules)
UNWIND [
  {id:'lcm_a1_a3',  code:'A1_A3',  name:'Product Stage (A1-A3)'},
  {id:'lcm_a1_a5',  code:'A1_A5',  name:'Product + Construction (A1-A5)'},
  {id:'lcm_a4_a5',  code:'A4_A5',  name:'Construction Stage (A4-A5)'},
  {id:'lcm_b',      code:'B',      name:'Use Stage (B1-B7)'},
  {id:'lcm_c1_c4',  code:'C1_C4',  name:'End-of-Life Stage (C1-C4)'},
  {id:'lcm_d',      code:'D',      name:'Beyond System Boundary (D)'}
] AS row
MERGE (lcm:LCAModule {id: row.id})
ON CREATE SET lcm.name = row.name,
              lcm.en15978_code = row.code,
              lcm.evidence_origin = 'source_curated',
              lcm.evidence_basis = 'controlled_vocab',
              lcm.evidence_source_id = 'q_en_15978_lifecycle_modules',
              lcm.evidence_confidence = 'belegt',
              lcm.source_scope = 'r2_b_lca_restore',
              lcm.migration_origin = 'mig_r2_b_restore_lca_module';

// R2.b.3 — Recreate BERECHNET_NACH_MODUL edges
MATCH (p:Projekt) WHERE p.lca_module_scope IS NOT NULL
UNWIND p.lca_module_scope AS code
MATCH (lcm:LCAModule {en15978_code: code})
MERGE (p)-[r:BERECHNET_NACH_MODUL]->(lcm)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_b_lca_restore',
              r.evidence_confidence = 'teilweise_belegt',
              r.migration_origin = 'mig_r2_b_restore_lca_module';

// Audits
MATCH (lcm:LCAModule) RETURN 'lca_module_count' AS check, count(lcm) AS c;
MATCH ()-[r:BERECHNET_NACH_MODUL]->() RETURN 'berechnet_nach_modul_count' AS check, count(r) AS c;
MATCH (p:Projekt)
WHERE p.lca_module_scope IS NOT NULL AND size(p.lca_module_scope) > 0
  AND NOT exists{(p)-[:BERECHNET_NACH_MODUL]->(:LCAModule)}
RETURN 'projekt_with_scope_no_edge' AS check, count(p) AS violations;
```

### §6.3 R2.c — Restore `:RechtlicheBedingung` (with country parse)

```cypher
// ==========================================================================
// mig_r2_c_restore_legal_conditions
// Parse <src>.legal_conditions strings of form "<name> [DE,BE]" or "<name>"
// Recreate :RechtlicheBedingung + HAT_RECHTLICHE_BEDINGUNG + GILT_IN_LAND
// ==========================================================================

// R2.c.1 — Read deleted journal to recover original node properties
// (Run from runner Python — load deleted/phase2_5_demoted_nodes.jsonl,
//  filter to records where labels==['RechtlicheBedingung'], MERGE nodes
//  with original id and properties)

// Pattern (runner-driven):
// UNWIND $rb_rows AS row
// MERGE (rb:RechtlicheBedingung {id: row.id})
// ON CREATE SET rb.name = row.name,
//               rb.scope_note = row.scope_note,
//               rb.is_universal = row.is_universal,
//               rb.diversion_requirement_percent = row.diversion_requirement_percent,
//               rb.note = row.note,
//               rb.evidence_origin = 'source_curated',
//               rb.evidence_basis = 'controlled_vocab',
//               rb.evidence_source_id = 'r2_c_restored_from_phase2_5_journal',
//               rb.evidence_confidence = 'belegt',
//               rb.source_scope = 'r2_c_legal_restore',
//               rb.migration_origin = 'mig_r2_c_restore_legal_conditions';

// R2.c.2 — Parse legal_conditions strings on every source node
//          Pattern: "<rb_name> [DE,BE]"  or  "<rb_name>"
MATCH (src)
WHERE src.legal_conditions IS NOT NULL AND size(src.legal_conditions) > 0
UNWIND src.legal_conditions AS lc_string
WITH src, lc_string,
     CASE WHEN lc_string CONTAINS '['
          THEN trim(split(lc_string, '[')[0])
          ELSE trim(lc_string) END AS rb_name_raw,
     CASE WHEN lc_string CONTAINS '['
          THEN split(replace(replace(split(lc_string, '[')[1], ']', ''), ' ', ''), ',')
          ELSE [] END AS country_isos
WITH src, lc_string, rb_name_raw, country_isos,
     // map raw name to id slug (lowercase + underscores)
     'rb_' + replace(replace(toLower(rb_name_raw), ' ', '_'), '/', '_') AS rb_id
// Match the RechtlicheBedingung node restored in R2.c.1 (by id or name)
OPTIONAL MATCH (rb:RechtlicheBedingung) WHERE rb.id = rb_id OR rb.name = rb_name_raw
WITH src, lc_string, rb, country_isos
WHERE rb IS NOT NULL
MERGE (src)-[h:HAT_RECHTLICHE_BEDINGUNG]->(rb)
ON CREATE SET h.evidence_origin = 'source_curated',
              h.evidence_basis = 'cell_citation',
              h.evidence_source_id = 'r2_c_restored_from_string',
              h.evidence_confidence = 'teilweise_belegt',
              h.evidence_excerpt = 'Restored from .legal_conditions: ' + lc_string,
              h.migration_origin = 'mig_r2_c_restore_legal_conditions'
WITH rb, country_isos
UNWIND country_isos AS iso
MATCH (l:Land) WHERE l.country_iso = iso OR toUpper(coalesce(l.iso, '')) = iso
MERGE (rb)-[g:GILT_IN_LAND]->(l)
ON CREATE SET g.evidence_origin = 'source_curated',
              g.evidence_basis = 'cell_citation',
              g.evidence_source_id = 'r2_c_restored_from_string_brackets',
              g.evidence_confidence = 'teilweise_belegt',
              g.migration_origin = 'mig_r2_c_restore_legal_conditions';

// Audits
MATCH (rb:RechtlicheBedingung) RETURN 'rb_count' AS check, count(rb) AS c;
MATCH ()-[r:HAT_RECHTLICHE_BEDINGUNG]->() RETURN 'hat_rb_count' AS check, count(r) AS c;
MATCH (:RechtlicheBedingung)-[r:GILT_IN_LAND]->(:Land) RETURN 'rb_gilt_in_land_count' AS check, count(r) AS c;
// Unparseable strings (no RB matched)
MATCH (src) WHERE src.legal_conditions IS NOT NULL AND size(src.legal_conditions) > 0
WITH src, [s IN src.legal_conditions WHERE NOT exists{
    MATCH (rb:RechtlicheBedingung) WHERE rb.name CONTAINS substring(s, 0, 10)  // fuzzy
}] AS unmatched
WHERE size(unmatched) > 0
RETURN 'legal_conditions_unparsed' AS check, src.id AS source_id, unmatched LIMIT 20;
```

### §6.4 R2.d — Restore `:Zertifizierungssystem`

```cypher
// ==========================================================================
// mig_r2_d_restore_certifications
// Parse Projekt.certifications list and recreate node + edge.
// New label name: :Zertifizierungssystem (cleaner than the old
// :ZertifizierungBewertungssystem; preserved as alias)
// ==========================================================================

// R2.d.1 — Create canonical certification nodes
UNWIND [
  {id:'cert_breeam',           name:'BREEAM',                   scheme_kind:'multi_criteria'},
  {id:'cert_leed',             name:'LEED',                     scheme_kind:'multi_criteria'},
  {id:'cert_dgnb',             name:'DGNB',                     scheme_kind:'multi_criteria'},
  {id:'cert_well',             name:'WELL',                     scheme_kind:'health_wellness'},
  {id:'cert_nabers',           name:'NABERS',                   scheme_kind:'operational_energy'},
  {id:'cert_paris_proof',      name:'Paris Proof',              scheme_kind:'carbon_target'},
  {id:'cert_nordic_swan',      name:'Nordic Swan Ecolabel',     scheme_kind:'ecolabel'},
  {id:'cert_ecotool',          name:'EcoTool',                  scheme_kind:'methodology_tool'}
] AS row
MERGE (z:Zertifizierungssystem {id: row.id})
ON CREATE SET z.name = row.name,
              z.scheme_kind = row.scheme_kind,
              z.aliases = ['ZertifizierungBewertungssystem'],
              z.evidence_origin = 'source_curated',
              z.evidence_basis = 'controlled_vocab',
              z.evidence_source_id = 'r2_d_cert_restore',
              z.evidence_confidence = 'belegt',
              z.source_scope = 'r2_d_cert_restore',
              z.migration_origin = 'mig_r2_d_restore_certifications';

// R2.d.2 — Recreate HAT_ZERTIFIZIERUNG edges
MATCH (p:Projekt) WHERE p.certifications IS NOT NULL
UNWIND p.certifications AS cert_name
WITH p, cert_name, trim(cert_name) AS cert_clean
MATCH (z:Zertifizierungssystem)
WHERE z.name = cert_clean
   OR cert_clean CONTAINS z.name
   OR z.name CONTAINS cert_clean
MERGE (p)-[r:HAT_ZERTIFIZIERUNG]->(z)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_d_cert_restore',
              r.evidence_confidence = 'belegt',
              r.evidence_excerpt = 'Restored from Projekt.certifications: ' + cert_name,
              r.migration_origin = 'mig_r2_d_restore_certifications';

// Audits
MATCH (z:Zertifizierungssystem) RETURN 'cert_count' AS check, count(z) AS c;
MATCH ()-[r:HAT_ZERTIFIZIERUNG]->() RETURN 'hat_zert_count' AS check, count(r) AS c;
MATCH (p:Projekt) WHERE p.certifications IS NOT NULL
  AND NOT exists{(p)-[:HAT_ZERTIFIZIERUNG]->()}
RETURN 'projekt_with_certs_no_edge' AS check, count(p) AS violations;
```

### §6.5 R2.e — Restore `:Tool` as secondary label

```cypher
// ==========================================================================
// mig_r2_e_restore_tool_label
// Add :Tool as a secondary label on :Software nodes with kind='tool'.
// Preserves :Software primary label so existing queries still work.
// ==========================================================================

MATCH (s:Software {kind: 'tool'})
SET s:Tool,
    s.migration_origin = coalesce(s.migration_origin, '') + ' | mig_r2_e_tool_secondary_label';

// Audits
MATCH (t:Tool) RETURN 'tool_count' AS check, count(t) AS c;
MATCH (t:Tool) WHERE NOT 'Software' IN labels(t) RETURN 'tool_without_software' AS check, count(t) AS violations;
MATCH (s:Software {kind:'tool'}) WHERE NOT 'Tool' IN labels(s)
RETURN 'software_tool_kind_without_tool_label' AS check, count(s) AS violations;
```

### §6.6 R10 — `:DeprecatedType` audit nodes

Run AFTER R2 is complete.

```cypher
// ==========================================================================
// mig_r10_deprecated_type_seed
// Record old-name → new-name mapping for retired labels/rel types.
// ==========================================================================

UNWIND [
  {kind:'label',    old:'GraphVersion',                        new:'(none — dropped)',           reason:'Experimental versioning label; never populated.'},
  {kind:'label',    old:'ZertifizierungBewertungssystem',      new:'Zertifizierungssystem',      reason:'Renamed in R2.d for brevity; old name preserved as alias on new nodes.'},
  {kind:'rel_type', old:'AUS_BAUWERK',                         new:'FROM_DONOR',                 reason:'Phase 4.2 rename.'},
  {kind:'rel_type', old:'EINGEBAUT_IN',                        new:'INTO_RECEIVER',              reason:'Phase 4.2 rename.'},
  {kind:'rel_type', old:'HAT_SCHADSTOFF',                      new:'HAS_RISK_POLLUTANT',         reason:'Phase 3.2 split into HAS_RISK_POLLUTANT + REQUIRES_VERIFICATION_FOR.'},
  {kind:'rel_type', old:'NUTZT_TOOL',                          new:'NUTZT_SOFTWARE',             reason:'Phase 2.5.e Tool relabel.'},
  {kind:'rel_type', old:'ASSOZIIERT_MIT_PROJEKT',              new:'STUB_PROJECT_LINK',          reason:'Renamed in R9 for honest stub semantics.'},
  {kind:'rel_type', old:'TEILT_LAYER',                         new:'(restored in R2.a)',         reason:'Restored from brand_layer property.'},
  {kind:'rel_type', old:'BERECHNET_NACH_MODUL',                new:'(restored in R2.b)',         reason:'Restored from lca_module_scope property.'},
  {kind:'rel_type', old:'HAT_RECHTLICHE_BEDINGUNG',            new:'(restored in R2.c)',         reason:'Restored from legal_conditions string.'},
  {kind:'rel_type', old:'GILT_IN_LAND',                        new:'(restored in R2.c via bracketed country)',         reason:'Restored from legal_conditions bracket parse.'},
  {kind:'rel_type', old:'HAT_ZERTIFIZIERUNG',                  new:'(restored in R2.d)',         reason:'Restored from certifications property.'}
] AS row
MERGE (d:DeprecatedType {id: 'dep_' + row.kind + '__' + replace(row.old, '_', '__')})
ON CREATE SET
  d.kind = row.kind,
  d.old_name = row.old,
  d.new_name = row.new,
  d.deprecated_at = date(),
  d.deprecated_by = 'mig_r10_deprecated_type_seed',
  d.reason = row.reason,
  d.evidence_origin = 'source_curated',
  d.evidence_basis = 'audit_record',
  d.evidence_confidence = 'belegt',
  d.migration_origin = 'mig_r10_deprecated_type_seed';

// Audits
MATCH (d:DeprecatedType) RETURN 'deprecated_type_count' AS check, count(d) AS c;
MATCH (d:DeprecatedType) RETURN d.kind, count(d) AS c;
```

---

## §7 Runner script outline

`logs/agent_2_runner.py` should:

1. Read `deleted/phase2_5_demoted_nodes.jsonl` and `deleted/phase2_5_tool_relabels.jsonl`.
2. Filter records by label (`RechtlicheBedingung`, `ZertifizierungBewertungssystem`, `Layer`, `LebenszyklusModul`, `Tool`).
3. Run R2.a → R2.b → R2.c (with rb_rows parameter from journal) → R2.d → R2.e in sequence.
4. After verifying R2 acceptance, run R10.
5. Write done flags `PHASE_R2_DONE.flag` and `PHASE_R10_DONE.flag`.

See [AGENT_1_evidence_honesty.md](AGENT_1_evidence_honesty.md) §7 for runner pattern.

---

## §8 Acceptance gates

### §8.1 R2 acceptance

| Gate | Expected |
|---|---|
| `:Layer` count | 6 (the Brand 6-layer model) |
| `TEILT_LAYER` count | ≥ 15 (one per Bauteiltyp with brand_layer) |
| `:LCAModule` count | 6 (A1_A3, A1_A5, A4_A5, B, C1_C4, D) |
| `BERECHNET_NACH_MODUL` count | ≥ 15 (preserved from pre-demote) |
| `:RechtlicheBedingung` count | ≥ 9 (the pre-demote nodes) |
| `HAT_RECHTLICHE_BEDINGUNG` count | ≥ 12 |
| `(:RechtlicheBedingung)-[:GILT_IN_LAND]->(:Land)` count | ≥ 5 |
| `:Zertifizierungssystem` count | ≥ 6 (BREEAM, LEED, DGNB, WELL, NABERS, Paris Proof, …) |
| `HAT_ZERTIFIZIERUNG` count | ≥ 12 |
| `:Tool` (secondary label) count | 8 (matches `:Software {kind:'tool'}`) |
| `:Tool` nodes all also `:Software` | 100 % |
| Every restored edge has `migration_origin` set | 100 % |

### §8.2 R10 acceptance

| Gate | Expected |
|---|---|
| `:DeprecatedType` count | ≥ 12 |
| Distinct `kind` values | `{'label','rel_type'}` |
| All entries reference real history | manual inspection: every `old` name appears in some prior migration |

---

## §9 Rollback

### §9.1 R2 rollback

```cypher
// R2 rollback — delete restored nodes; property mirrors are still present
MATCH (l:Layer) DETACH DELETE l;
MATCH (lcm:LCAModule) DETACH DELETE lcm;
MATCH (rb:RechtlicheBedingung) WHERE rb.migration_origin CONTAINS 'mig_r2_c' DETACH DELETE rb;
MATCH (z:Zertifizierungssystem) WHERE z.migration_origin CONTAINS 'mig_r2_d' DETACH DELETE z;
MATCH (t:Tool) WHERE 'Software' IN labels(t) REMOVE t:Tool;
```

### §9.2 R10 rollback

```cypher
MATCH (d:DeprecatedType) WHERE d.migration_origin = 'mig_r10_deprecated_type_seed' DETACH DELETE d;
```

---

## §10 Open decisions affecting your phase

- **D2** (delete mirrors after R2 lands): Do NOT delete `Bauteiltyp.brand_layer`, `Projekt.lca_module_scope`, `<src>.legal_conditions`, `Projekt.certifications`, or `Software.kind` in this phase. Defer to a follow-up after Stage 4 confirms downstream queries use the nodes.

If you encounter a property-mirror entry that you cannot parse back into a node (e.g., a legal_conditions string in an unexpected format), record it as a residual:

```cypher
MERGE (i:DataIssue {id: 'di_r2_unparsed__' + <src.id> + '__' + <hash>})
SET i.kind = 'r2_unparseable_property_mirror',
    i.severity = 'medium',
    ...
```

(This `:DataIssue` will be unified with Agent 1's R8 seed pass.)

---

## §11 Handoff

When R2 is complete:

1. Verify all R2 acceptance gates green.
2. Push `agent2/r2-r10-restore` to remote.
3. Update [HANDOFF_LOG.md](HANDOFF_LOG.md): `| <date> | agent_2 | R2 complete (X Layer, Y LCAModule, Z RB, W Cert restored) | <PR> | PASS |`.

After orchestrator merges R2 to `orch/integrate-2026-05-21`:

4. Pull and run R10 on the integrated branch.
5. Verify R10 acceptance.
6. Push R10 commit.
7. Update handoff log.

---

## §12 Report contents (your `reports/agent_2_report.md`)

Standard template (ORCHESTRATION §6.6) plus:

- Before/after node counts per restored label.
- Before/after edge counts per restored rel type.
- List of unparseable property-mirror entries (with proposed fix).
- Comparison: pre-Phase-2.5 counts (from `deleted/phase2_5_demoted_nodes.jsonl`) vs post-R2 counts. Confirm round-trip lossless except where R2 deliberately consolidated (e.g., `:Zertifizierungssystem` renamed).

---

**End of AGENT_2_schema_restoration.md.**
