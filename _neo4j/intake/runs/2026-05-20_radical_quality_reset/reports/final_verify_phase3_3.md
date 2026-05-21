# Final Verification — Phase 3.3 ReuseRule

- Verifier: Final Verifier 9 of 12
- Date (UTC): 2026-05-21
- Plan section: 3.3 — Country × material decision shelf
  (`c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`, lines 984–1058)
- Run dir: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- Driver: Neo4j MCP (`project-0-recherche-Neo4j-Official`) → `bolt://localhost:7687`, database **mit-bestand** (read-only)
- Source research file: `_neo4j/intake/inbox/research/circular_construction_reuse_graph_gaps.md`

## Verdict: PASS (9 / 9 checks)

All Phase 3.3 acceptance criteria are met live in `mit-bestand`. No corrective action required.

## Check matrix

| # | Check | Expected | Got | Result |
|---|---|---|---|---|
| 1 | `migrations/mig_3_3_reuse_rules.cypher` exists | present | 6256 bytes, 2026-05-21 00:31 | PASS |
| 2 | `PHASE_3_3_DONE.flag` present | present | 2430 bytes, 2026-05-21 00:37 | PASS |
| 3 | `MATCH (r:ReuseRule) RETURN count(r)` | 20 | 20 | PASS |
| 4 | `(:ReuseRule)-[:APPLIES_IN]->(:Land)` edges | 20 | 20 | PASS |
| 5 | `(:ReuseRule)-[:APPLIES_TO]->(:Material)` edges | 20 | 20 | PASS |
| 6 | `(:ReuseRule)-[:REFERENZIERT_NORM]->(:Norm)` edges | ≥ 60 (target ~93) | 93 | PASS |
| 7 | Sample 3 ReuseRule nodes — all 5 list props non-empty | non-empty on all sampled rules | non-empty on all 20 (key_norms 20/20, legal_conditions 20/20, required_tests 20/20, pollutant_risks 20/20, processing_methods 20/20) | PASS |
| 8 | All 20 `:ReuseRule` have `evidence_origin='inferred'` | 20 / 20 | 20 / 20 | PASS |
| 9 | Decision-support `(:ReuseRule)-[:APPLIES_IN]->(:Land)` AND `-[:APPLIES_TO]->(:Material)` | ≥ 20 | 20 | PASS |

## Live evidence

### Check 3 — node count

```cypher
MATCH (r:ReuseRule) RETURN count(r) AS reuse_rule_total;
// → 20
```

### Check 4 / 5 — wiring counts

```cypher
MATCH (r:ReuseRule)-[:APPLIES_IN]->(:Land)   RETURN count(*);  // → 20
MATCH (r:ReuseRule)-[:APPLIES_TO]->(:Material) RETURN count(*); // → 20
```

### Check 6 — norm wiring

```cypher
MATCH (r:ReuseRule)-[:REFERENZIERT_NORM]->(:Norm) RETURN count(*);  // → 93
```

93 falls inside the plan's 60–120 acceptance band and matches the value
recorded in `PHASE_3_3_DONE.flag.after.referenziert_norm_from_rule = 93`.

### Check 7 — sampled property completeness

Three rules sampled by `r.id` (BE first three):

| id | country_iso | material | key_norms | legal_conditions | required_tests | pollutant_risks | processing_methods |
|---|---|---|---|---|---|---|---|
| `rr_be_beton` | BE | Beton | 6 | 3 | 10 | 6 | 7 |
| `rr_be_holz` | BE | Holz | 4 | 3 | 6 | 5 | 6 |
| `rr_be_naturstein` | BE | Naturstein | 8 | 3 | 7 | 5 | 6 |

All five list properties are non-empty on each sampled node. The same
check broadened across all 20 nodes returned 20 / 20 non-empty for every
required list property:

```cypher
MATCH (r:ReuseRule)
WITH r,
     size(r.key_norms)          AS kn,
     size(r.legal_conditions)   AS lc,
     size(r.required_tests)     AS rt,
     size(r.pollutant_risks)    AS pr,
     size(r.processing_methods) AS pm
RETURN count(r) AS rules_total,
       sum(CASE WHEN kn>0 THEN 1 ELSE 0 END) AS key_norms_nonempty,
       sum(CASE WHEN lc>0 THEN 1 ELSE 0 END) AS legal_conditions_nonempty,
       sum(CASE WHEN rt>0 THEN 1 ELSE 0 END) AS required_tests_nonempty,
       sum(CASE WHEN pr>0 THEN 1 ELSE 0 END) AS pollutant_risks_nonempty,
       sum(CASE WHEN pm>0 THEN 1 ELSE 0 END) AS processing_methods_nonempty;
// → rules_total=20, all five *_nonempty counters = 20
```

### Check 8 — evidence origin uniform

```cypher
MATCH (rule:ReuseRule)
RETURN rule.evidence_origin AS evidence_origin, count(*) AS n;
// → [{evidence_origin: 'inferred', n: 20}]
```

All 20 `:ReuseRule` nodes also carry `evidence_basis='research_file_row'`,
`evidence_source_id='q_circular_construction_reuse_graph_gaps_md'`, and
`evidence_confidence='belegt'`, matching the plan spec
(lines 1033–1036).

### Check 9 — decision-support wiring

```cypher
MATCH (rule:ReuseRule)-[:APPLIES_IN]->(l:Land),
      (rule)-[:APPLIES_TO]->(m:Material)
RETURN count(rule) AS wired_rules;  // → 20
```

Spot-check of the plan's named decision query (line 1056) now hits the
graph because the `:Land` nodes carry `country_iso` (note: the property
is `country_iso`, not the abbreviated `iso` used in the plan snippet):

```cypher
MATCH (rule:ReuseRule)-[:APPLIES_IN]->(:Land {country_iso:'DE'}),
      (rule)-[:APPLIES_TO]->(:Material {name:'Stahl'})
RETURN rule.id, size(rule.key_norms) AS n_norms,
       size(rule.required_tests) AS n_tests,
       size(rule.pollutant_risks) AS n_pollutants,
       size(rule.processing_methods) AS n_processing,
       rule.evidence_source_id;
// → rr_de_stahl with n_norms=4, n_tests=7, n_pollutants=5, n_processing=5,
//   evidence_source_id='q_circular_construction_reuse_graph_gaps_md'
```

## Coverage map (20 / 20 rows)

The 20 `:ReuseRule` ids cover every row of the plan's 1–20 table:

- P1_Critical (11 rows): `rr_gb_stahl`, `rr_be_stahl`, `rr_de_stahl`,
  `rr_nl_stahl`, `rr_ch_stahl`, `rr_be_beton`, `rr_nl_beton`,
  `rr_de_beton`, `rr_ch_beton`, `rr_fi_beton_hollow_core_slabs`,
  `rr_no_beton_hollow_core_slabs`.
- P2_High (9 rows): `rr_de_holz`, `rr_nl_holz`, `rr_be_holz`,
  `rr_ch_holz`, `rr_be_naturstein`, `rr_ch_naturstein`, `rr_gb_holz`,
  `rr_de_ziegel`, `rr_de_lehm`.

Country ISO codes used: `GB`, `BE`, `DE`, `NL`, `CH`, `FI`, `NO`
(7 distinct), matching the migration's `3_3.pre` block (lines 40–50 of
`mig_3_3_reuse_rules.cypher`).

## Plan ↔ runtime notes (no failures, informational)

- The plan example query on line 1056 uses `{iso:'DE'}` whereas the
  actual property set by `mig_3_3_reuse_rules.cypher` is
  `country_iso='DE'`. The decision query still works with the correct
  property name. The Phase 3.3 acceptance check #9 (which does not
  filter by ISO at all) passes regardless.
- 69 new `:Norm` nodes were minted from `key_norms` strings that were
  not yet in the graph (recorded in `PHASE_3_3_DONE.flag.after.new_norm_nodes_reuse_rule_seed=69`).
  This was anticipated by the plan (lines 1052–1053).
- Per the plan's Rule B (≥5 connections per node for new labels),
  `:ReuseRule` reports minimum degree 5, median 7, mean 6.65 — well
  above the threshold.

## Conclusion

Phase 3.3 is confirmed complete and stable on `mit-bestand`. All nine
read-only checks pass. No write actions were taken during this
verification.
