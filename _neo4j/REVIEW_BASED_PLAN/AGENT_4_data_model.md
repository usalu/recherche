# Agent 4 — Data model: Kennwert (R4)

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.** This brief assumes you have.

You are agent 4 of 5. You own the single most decision-impactful change: lifting the quantitative facts out of JSON-string properties and into a real graph model.

---

## §1 Cold-start context

In `mit-bestand`, every measured quantity lives on `:Projekt` as a list-of-JSON-string property:

- `reuse_share_facts` — reuse percentages, with `{kennwert, wert, einheit, method, bilanzgrenze, source_id, confidence, loader}`
- `co2_facts` — CO₂ savings, same shape
- `cost_facts` — costs, same shape
- `quality_tier_facts` — internal audit fold; NOT a measurement (see §10 D5)

To ask "show all projects with steel reuse share ≥ 30 %", a user must run `apoc.convert.fromJsonList(p.reuse_share_facts)` on every project, then filter the resulting parsed objects. The data lives **inside string-typed properties** — defeating the point of using a graph database.

Worse: each JSON object carries its own `confidence` and `source_id` fields, **duplicating the edge-level evidence model**. Two parallel trust systems for one fact.

Your job: lift the JSON arrays into a proper `:Kennwert` node model with one node per measurement, an explicit `:HAT_KENNWERT` edge, and a single canonical evidence shape on the edge. After that, downstream queries become first-class graph traversals.

---

## §2 Mission

### §2.1 Phase R4 — Lift `*_facts` JSON to `:Kennwert` nodes

Create `:Kennwert` nodes for every entry in the three measurement-style lists (`reuse_share_facts`, `co2_facts`, `cost_facts`). Wire each to its project via `:HAT_KENNWERT`. Move the inner JSON's `confidence` and `source_id` to the **edge** (using R1's `evidence_origin` / `evidence_confidence` enum). After acceptance, the orchestrator decides (D2) whether to strip the JSON-string property mirrors.

`quality_tier_facts` is **out of scope** — it is an internal audit fold, not a measurement. Keep it on `:Projekt`.

---

## §3 Dependencies

| Stage | You run | After / before |
|---|---|---|
| Stage 2 | R4 | After: Agent 1 R1 (you use the R1-extended `evidence_origin` enum on `:HAT_KENNWERT` edges). |

You block:
- Agent 5 R7.c (Section-8 re-extraction creates more `:Kennwert` nodes using your schema).
- Orchestrator's Stage 4 audit (new Q3 query uses `:Kennwert`).

---

## §4 Conflict avoidance

You write:
- New `:Kennwert` nodes.
- New `:HAT_KENNWERT` edges.
- **NOTHING ELSE.** Property strip (R4.b) is deferred to a separate orchestrator-gated migration after Stage 4.

You read:
- `:Projekt.reuse_share_facts`, `:Projekt.co2_facts`, `:Projekt.cost_facts`
- (Optional) `:Quelle.id` to validate the `evidence_source_id` references.

You MUST NOT:
- Touch `quality_tier_facts` (out of scope).
- Strip the JSON-string properties yet.
- Modify existing edges.
- Touch any other label/property.

---

## §5 Pre-flight checklist

```bash
# 1. Verify Agent 1 R1 has landed
ls _neo4j/intake/runs/2026-05-21_review_based_plan/agent_1_evidence_honesty/PHASE_R1_DONE.flag

# 2. Verify expected counts (from FINAL_PASS2_AUDIT.md and Section-8 audit)
#    Total :Projekt with reuse_share_facts: 3
#    Total reuse_share_facts entries: 4
#    Total :Projekt with co2_facts:  ~5–10 (varies)
#    Total :Projekt with cost_facts: ~5–10

# 3. Branch
git switch -c agent4/r4-kennwert

# 4. Peek at sample structure
# MATCH (p:Projekt) WHERE p.reuse_share_facts IS NOT NULL
# RETURN p.id, p.reuse_share_facts LIMIT 5
```

---

## §6 Schema delta

```
:Kennwert {
  id: 'kw_<projekt>_<category>_<i>',   // deterministic, idempotent
  category: enum {reuse_share, co2_saving, cost, …},  // discriminator (D4=yes)
  kennwert: <free text — what the metric measures, e.g. 'Stahl_Wiederverwendungsanteil'>,
  wert: <float when single value> | NULL,
  wert_text: <string when non-numeric or range>,
  wert_min: <float>,           // when wert is a range
  wert_max: <float>,
  einheit: <string enum: percent, t_co2, eur, m2, m3, m, kg, t, eur_per_m2, …>,
  method: <free text — measurement methodology>,
  bilanzgrenze: <enum: A1_A3, A1_A5, A4_A5, B, C1_C4, D, lifecycle, full_scope, partial, NULL>,
  loader: <string — which loader/migration created this>,
  source_id: <string — original Quelle id referenced by the JSON>
}

(:Projekt)-[:HAT_KENNWERT]->(:Kennwert)
  evidence_origin     (R1-extended enum)
  evidence_basis      ('cell_citation' typical)
  evidence_confidence (R1-cleaned: belegt | teilweise_belegt | unklar | inferiert)
  evidence_source_id  (Quelle id from inner JSON)
  evidence_excerpt    (optional — if loader captured original text)
  migration_origin    ('mig_r4_kennwert')
```

**On `:Kennwert.category` discriminator (D4):** Yes — add `category` enum on the node. Indexable, query-friendly, and prevents the JSON-shape ambiguity from leaking into the new model.

**On range values:** If the source has "30–40 %" (Jeugdkliniek), set `wert_min=30`, `wert_max=40`, `wert=NULL`, `wert_text='30-40 %'`. The mid-point can be derived in queries; do not synthesize it here.

---

## §7 Migration

### §7.1 R4.a — Lift `reuse_share_facts`

```cypher
// ==========================================================================
// mig_r4_a_lift_reuse_share_facts
// Each JSON entry becomes one :Kennwert node + :HAT_KENNWERT edge.
// Idempotent: id is deterministic from (projekt, category, entry_index).
// ==========================================================================

MATCH (p:Projekt)
WHERE p.reuse_share_facts IS NOT NULL AND size(p.reuse_share_facts) > 0
UNWIND range(0, size(p.reuse_share_facts)-1) AS i
WITH p, i, apoc.convert.fromJsonMap(p.reuse_share_facts[i]) AS fact
WITH p, i, fact,
     'kw_' + p.id + '_reuse_share_' + toString(i) AS new_id,
     // Parse wert: scalar vs range
     CASE
       WHEN fact.wert IS NULL THEN NULL
       WHEN toString(fact.wert) CONTAINS '-' AND NOT toString(fact.wert) STARTS WITH '-'
         THEN NULL  // range — set wert_min/max below
       ELSE toFloat(toString(fact.wert))
     END AS wert_scalar,
     CASE
       WHEN toString(fact.wert) CONTAINS '-' AND NOT toString(fact.wert) STARTS WITH '-'
         THEN toFloat(split(toString(fact.wert), '-')[0])
       ELSE NULL
     END AS wert_min,
     CASE
       WHEN toString(fact.wert) CONTAINS '-' AND NOT toString(fact.wert) STARTS WITH '-'
         THEN toFloat(split(toString(fact.wert), '-')[1])
       ELSE NULL
     END AS wert_max
MERGE (kw:Kennwert {id: new_id})
ON CREATE SET kw.category = 'reuse_share',
              kw.kennwert = fact.kennwert,
              kw.wert = wert_scalar,
              kw.wert_text = toString(fact.wert),
              kw.wert_min = wert_min,
              kw.wert_max = wert_max,
              kw.einheit = coalesce(fact.einheit, '%'),
              kw.method = fact.method,
              kw.bilanzgrenze = fact.bilanzgrenze,
              kw.loader = coalesce(fact.loader, 'unknown'),
              kw.source_id = fact.source_id,
              kw.migration_origin = 'mig_r4_a_lift_reuse_share_facts',
              kw.source_scope = 'r4_a_reuse_share'
MERGE (p)-[r:HAT_KENNWERT]->(kw)
ON CREATE SET r.evidence_origin = CASE
                WHEN fact.confidence = 'belegt' THEN 'source_curated'
                WHEN fact.confidence = 'teilweise_belegt' THEN 'source_curated'
                WHEN fact.confidence = 'unklar' THEN 'derived'
                WHEN fact.confidence = 'inferiert' THEN 'inferred'
                ELSE 'derived' END,
              r.evidence_basis = 'cell_citation',
              r.evidence_confidence = coalesce(fact.confidence, 'unklar'),
              r.evidence_source_id = fact.source_id,
              r.evidence_excerpt = NULL,
              r.migration_origin = 'mig_r4_a_lift_reuse_share_facts';
```

### §7.2 R4.b — Lift `co2_facts`

```cypher
// Same pattern; category='co2_saving'; default einheit='t_co2'
MATCH (p:Projekt)
WHERE p.co2_facts IS NOT NULL AND size(p.co2_facts) > 0
UNWIND range(0, size(p.co2_facts)-1) AS i
WITH p, i, apoc.convert.fromJsonMap(p.co2_facts[i]) AS fact
WITH p, i, fact,
     'kw_' + p.id + '_co2_saving_' + toString(i) AS new_id,
     CASE WHEN fact.wert IS NOT NULL THEN toFloat(toString(fact.wert)) ELSE NULL END AS wert_scalar
MERGE (kw:Kennwert {id: new_id})
ON CREATE SET kw.category = 'co2_saving',
              kw.kennwert = fact.kennwert,
              kw.wert = wert_scalar,
              kw.wert_text = toString(fact.wert),
              kw.einheit = coalesce(fact.einheit, 't_co2'),
              kw.method = fact.method,
              kw.bilanzgrenze = fact.bilanzgrenze,
              kw.loader = coalesce(fact.loader, 'unknown'),
              kw.source_id = fact.source_id,
              kw.migration_origin = 'mig_r4_b_lift_co2_facts',
              kw.source_scope = 'r4_b_co2_saving'
MERGE (p)-[r:HAT_KENNWERT]->(kw)
ON CREATE SET r.evidence_origin = CASE fact.confidence
                WHEN 'belegt' THEN 'source_curated'
                WHEN 'teilweise_belegt' THEN 'source_curated'
                WHEN 'unklar' THEN 'derived'
                WHEN 'inferiert' THEN 'inferred'
                ELSE 'derived' END,
              r.evidence_basis = 'cell_citation',
              r.evidence_confidence = coalesce(fact.confidence, 'unklar'),
              r.evidence_source_id = fact.source_id,
              r.migration_origin = 'mig_r4_b_lift_co2_facts';
```

### §7.3 R4.c — Lift `cost_facts`

```cypher
// Same pattern; category='cost'; default einheit varies per fact.einheit
MATCH (p:Projekt)
WHERE p.cost_facts IS NOT NULL AND size(p.cost_facts) > 0
UNWIND range(0, size(p.cost_facts)-1) AS i
WITH p, i, apoc.convert.fromJsonMap(p.cost_facts[i]) AS fact
WITH p, i, fact,
     'kw_' + p.id + '_cost_' + toString(i) AS new_id,
     CASE WHEN fact.wert IS NOT NULL THEN toFloat(toString(fact.wert)) ELSE NULL END AS wert_scalar
MERGE (kw:Kennwert {id: new_id})
ON CREATE SET kw.category = 'cost',
              kw.kennwert = coalesce(fact.kennwert, fact.basis),  // legacy entries use 'basis'
              kw.wert = wert_scalar,
              kw.wert_text = toString(fact.wert),
              kw.einheit = coalesce(fact.einheit, fact.unit, 'EUR'),
              kw.method = fact.method,
              kw.bilanzgrenze = fact.bilanzgrenze,
              kw.loader = coalesce(fact.loader, 'unknown'),
              kw.source_id = fact.source_id,
              kw.migration_origin = 'mig_r4_c_lift_cost_facts',
              kw.source_scope = 'r4_c_cost'
MERGE (p)-[r:HAT_KENNWERT]->(kw)
ON CREATE SET r.evidence_origin = CASE fact.confidence
                WHEN 'belegt' THEN 'source_curated'
                WHEN 'teilweise_belegt' THEN 'source_curated'
                WHEN 'unklar' THEN 'derived'
                WHEN 'inferiert' THEN 'inferred'
                ELSE 'derived' END,
              r.evidence_basis = 'cell_citation',
              r.evidence_confidence = coalesce(fact.confidence, 'unklar'),
              r.evidence_source_id = fact.source_id,
              r.migration_origin = 'mig_r4_c_lift_cost_facts';
```

### §7.4 Audits (run last)

```cypher
// ==========================================================================
// R4 audits — every count below MUST satisfy expectations
// ==========================================================================

// Total :Kennwert per category
MATCH (kw:Kennwert) RETURN kw.category AS category, count(kw) AS c ORDER BY c DESC;

// Every :Kennwert has at least one incoming :HAT_KENNWERT
MATCH (kw:Kennwert) WHERE NOT exists{()-[:HAT_KENNWERT]->(kw)}
RETURN 'kennwert_orphan' AS check, count(kw) AS violations;

// Every :Projekt with reuse_share_facts has matching :Kennwert nodes
MATCH (p:Projekt) WHERE p.reuse_share_facts IS NOT NULL AND size(p.reuse_share_facts) > 0
OPTIONAL MATCH (p)-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'})
WITH p, count(kw) AS kw_count, size(p.reuse_share_facts) AS expected
WHERE kw_count <> expected
RETURN 'reuse_share_count_mismatch' AS check, count(p) AS violations;

// Every :HAT_KENNWERT carries evidence_origin in R1-extended enum
MATCH ()-[r:HAT_KENNWERT]->()
WHERE NOT r.evidence_origin IN ['source_curated','topology_synthesized','registry_derived','inferred','external_unfolded']
RETURN 'hat_kennwert_origin_enum_violation' AS check, count(r) AS violations;

// Sample query: Q3 rewrite under new model
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert)
WHERE kw.category = 'reuse_share'
RETURN p.id AS projekt, kw.kennwert, kw.wert, kw.wert_text, kw.einheit, kw.bilanzgrenze
ORDER BY p.id, kw.kennwert;
```

---

## §8 Acceptance gates

| Gate | Expected |
|---|---|
| `:Kennwert` total | ≥ 12 (Section-8 sums across all dossiers; R7.c will add more) |
| `:Kennwert {category:'reuse_share'}` | ≥ 4 (matches current `reuse_share_facts` entries) |
| `:Kennwert {category:'co2_saving'}` | ≥ 5 (per pre-reset audit: 7 projects had `co2_einsparung_t`) |
| `:Kennwert {category:'cost'}` | ≥ 5 |
| Every `:Kennwert` has at least one `:HAT_KENNWERT` incoming | 100 % |
| Every `:Projekt.reuse_share_facts` array entry has a matching `:Kennwert` | 100 % |
| Every `:HAT_KENNWERT.evidence_origin` in R1-extended enum | 100 % |
| Q3 honest rerun: `MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'}) RETURN p, kw` returns ≥ 3 projects (Holbein, Jeugdkliniek, Ferme du Rail) | yes |
| Holbein 34 % steel reuse: `MATCH (:Projekt {id:'p_holbein_gardens_london'})-[:HAT_KENNWERT]->(kw:Kennwert) WHERE kw.kennwert CONTAINS 'steel' RETURN kw.wert` returns 34 | yes |
| Range parse works: Jeugdkliniek 30–40 has `wert_min=30, wert_max=40` | yes |

---

## §9 Rollback

```cypher
MATCH (kw:Kennwert) WHERE kw.migration_origin STARTS WITH 'mig_r4_'
DETACH DELETE kw;
```

The JSON-string properties on `:Projekt` are untouched, so this is a clean rollback.

---

## §10 Open decisions affecting your phase

- **D4** (`:Kennwert.category` enum): YES — add the discriminator. The Cypher above includes it.
- **D5** (lift `quality_tier_facts`): NO — it's an internal audit fold, not a measurement. Keep as JSON-string on `:Projekt`.

If you encounter a fact entry that does not parse cleanly (malformed JSON, missing required fields), record it as a residual:

```cypher
MERGE (i:DataIssue {id: 'di_r4_unparseable__' + <p.id> + '_' + <category> + '_' + <i>})
SET i.kind = 'r4_kennwert_unparseable_entry',
    i.severity = 'medium',
    i.ref_label = 'Projekt',
    i.ref_id = <p.id>,
    i.found_at = date(),
    i.found_by = 'agent_4_r4_residual',
    i.status = 'open',
    i.resolution_note = 'Fact JSON did not parse cleanly. Original: ' + <original_string>;
```

---

## §11 Handoff

When R4 is complete:

1. Verify all acceptance gates green.
2. Push `agent4/r4-kennwert` to remote.
3. Update [HANDOFF_LOG.md](HANDOFF_LOG.md): `| <date> | agent_4 | R4 complete (Kennwert: X reuse_share + Y co2_saving + Z cost) | <PR> | PASS |`.

Critical: Agent 5 R7.c uses your schema. Confirm in the handoff log that R7.c can proceed.

---

## §12 Report contents

Standard template plus:

- `:Kennwert` count by category (table).
- For each of the 11 tier-1 projects, list every `:Kennwert` reachable (this becomes the new Q3 evidence base).
- Any residual `:DataIssue` nodes you created.
- Confirmation that JSON-string properties are untouched (the strip is deferred to a post-Stage-4 migration).

---

**End of AGENT_4_data_model.md.**
