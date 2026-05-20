# Verify Phase 4.1 (evidence shape) + Phase 4.2 (donor/receiver rename)

Verifier: 10 of 12
Phases: 4.1, 4.2
Run dir: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`
Plan: `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md` §§ 4.1, 4.2
Neo4j database: `mit-bestand` via read-only MCP/driver config from `E:\recherche\.cursor\mcp.json`

## Result

Overall status: **FAIL**

All twelve gates were exercised live against `mit-bestand`. Eleven of twelve pass; one strict-enum gate on `evidence_confidence` fails because 15 `REFERENZIERT_NORM` edges still carry the off-enum value `'mittel'` (legacy from earlier polluted-edge migration; Agent 7 documented the value but did not normalize it).

The Phase 4.2 donor/receiver rename is clean: both legacy types are gone, both new types are at full expected cardinality, and total relationship count is preserved.

## Checks

| # | Check | Expected | Observed | Status |
| ---: | --- | ---: | ---: | --- |
| 1 | `PHASE_4_DONE.flag` exists | yes | yes | PASS |
| 2 | Edges with `evidence_origin IS NULL` | <= 50 | 0 | PASS |
| 3 | `evidence_origin='curated'` AND `evidence_excerpt IS NULL` | 0 | 0 | PASS |
| 4 | `evidence_confidence='bookkeeping'` AND `evidence_origin <> 'derived'` | 0 | 0 | PASS |
| 5 | `evidence_excerpt CONTAINS 'propagated from'` | 0 | 0 | PASS |
| 6 | `evidence_origin` values subset of {curated, inferred, derived} | yes | {derived} | PASS |
| 7 | `evidence_confidence` values subset of {belegt, teilweise_belegt, unklar, inferiert, bookkeeping} | yes | {unklar, bookkeeping, **mittel**} | **FAIL** (15 off-enum edges) |
| 8 | `PHASE_4_2_DONE.flag` exists | yes | yes | PASS |
| 9 | `:AUS_BAUWERK` edge count | 0 | 0 | PASS |
| 10 | `:EINGEBAUT_IN` edge count | 0 | 0 | PASS |
| 11 | `:FROM_DONOR` edge count | >= 280 (~286) | 286 | PASS |
| 12 | `:INTO_RECEIVER` edge count | >= 340 (~349) | 349 | PASS |

## Live evidence_origin distribution

```cypher
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
RETURN DISTINCT r.evidence_origin AS origin, count(r) AS c
ORDER BY origin;
```

| origin | count |
| --- | ---: |
| `derived` | 19 624 |

Observed values are a subset of the allowed enum, so check 6 passes.
Note: no edges carry `'curated'` or `'inferred'` yet — those origins are produced by Phase 4b (loader rewrite) and Phase 3 (era / pollutant inference), neither of which is in Phase 4.1 scope per the plan and per Agent 7's report.

## Live evidence_confidence distribution

```cypher
MATCH ()-[r]->()
WHERE r.evidence_confidence IS NOT NULL
RETURN DISTINCT r.evidence_confidence AS conf, count(r) AS c
ORDER BY conf;
```

| confidence | count |
| --- | ---: |
| `bookkeeping` | 1 021 |
| **`mittel`** | **15** |
| `unklar` | 18 588 |

`'mittel'` is not in the strict enum `{belegt, teilweise_belegt, unklar, inferiert, bookkeeping}` from plan §4.1 (line 156). This is the sole gate failure.

### Root cause of the 15 off-enum edges

All 15 `'mittel'` edges are `REFERENZIERT_NORM` carrying `evidence_origin='derived'`, `evidence_basis='standards_body'`, with project endpoints and Norm targets:

| pattern | edges |
| --- | ---: |
| `(:Projekt)-[:REFERENZIERT_NORM {evidence_confidence:'mittel'}]->(:Norm)` | 15 |

Sample (first 5):

| Projekt | Norm |
| --- | --- |
| `p_55_great_suffolk_street_london` | `norm_din_en_15804` |
| `p_55_great_suffolk_street_london` | `norm_din_en_15978` |
| `p_55_great_suffolk_street_london` | `norm_iso_14040` |
| `p_55_great_suffolk_street_london` | `norm_iso_14044` |
| `p_brent_cross_town_primary_substation_london` | `norm_din_en_15804` |

These edges predate the Phase 4.1 migration (they were already in the graph when Agent 7 started, and Agent 7's report explicitly lists `'mittel'` with count 15 in its "Evidence distribution post-migration" table without remapping it). Agent 7's Phase 4.1 migration `mig_4_1_canonical_evidence.cypher` only normalizes `evidence_basis` enum values (steps 4.1.f / 4.1.g / 4.1.h) and uses `coalesce(r.evidence_confidence, 'unklar' | 'bookkeeping')` for backfill — it never touches non-null confidence values, so `'mittel'` survived unchanged.

Suggested remediation (out of verifier scope): map `'mittel'` → `'teilweise_belegt'` (semantic match: "partly substantiated" via the standards body) in a follow-up Phase 4.1.i step, preserving `derivation_note='former_confidence=mittel'`.

## Phase 4.2 — donor / receiver rename verification

```cypher
MATCH ()-[r:AUS_BAUWERK]->()   RETURN count(r);   //   0
MATCH ()-[r:EINGEBAUT_IN]->()  RETURN count(r);   //   0
MATCH ()-[r:FROM_DONOR]->()    RETURN count(r);   // 286
MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r);   // 349
```

The legacy types are completely retired and the new types match the expected cardinalities exactly (the `~286` / `~349` targets in the brief).
Total graph size is preserved at 2 674 nodes / 19 624 relationships (matches `PHASE_4_DONE.flag` after-block).

## Flag artifacts

| flag | path | bytes |
| --- | --- | ---: |
| `PHASE_4_DONE.flag` | `_neo4j\intake\runs\2026-05-20_radical_quality_reset\PHASE_4_DONE.flag` | 5300 |
| `PHASE_4_2_DONE.flag` | `_neo4j\intake\runs\2026-05-20_radical_quality_reset\PHASE_4_2_DONE.flag` | 5300 |

Both files are valid JSON with matching `before` / `after` blocks (`PHASE_4_DONE.flag.phase = "4.1"`, `PHASE_4_2_DONE.flag.phase = "4.2"`) reporting `rename_status: {FROM_DONOR: 286, INTO_RECEIVER: 349}` and `evidence.{viol_curated_no_excerpt, viol_bk_not_derived, viol_excerpt_propagated, missing_origin} = 0`.

## JSON

```json
{
  "phase": "4.1+4.2",
  "verifier": 10,
  "status": "FAIL",
  "live_graph": {
    "total_nodes": 2674,
    "total_rels": 19624
  },
  "checks": {
    "phase4_done_flag_exists": true,
    "missing_evidence_origin": {
      "expected_max": 50,
      "observed": 0,
      "pass": true
    },
    "viol_curated_no_excerpt": {
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "viol_bookkeeping_not_derived": {
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "viol_excerpt_propagated_from": {
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "evidence_origin_enum": {
      "expected": ["curated", "inferred", "derived"],
      "observed": {"derived": 19624},
      "off_enum_values": [],
      "pass": true
    },
    "evidence_confidence_enum": {
      "expected": ["belegt", "teilweise_belegt", "unklar", "inferiert", "bookkeeping"],
      "observed": {"unklar": 18588, "bookkeeping": 1021, "mittel": 15},
      "off_enum_values": ["mittel"],
      "off_enum_count": 15,
      "off_enum_breakdown_by_rel_type": {"REFERENZIERT_NORM": 15},
      "pass": false
    },
    "phase4_2_done_flag_exists": true,
    "aus_bauwerk_count": {
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "eingebaut_in_count": {
      "expected": 0,
      "observed": 0,
      "pass": true
    },
    "from_donor_count": {
      "expected_min": 280,
      "expected_about": 286,
      "observed": 286,
      "pass": true
    },
    "into_receiver_count": {
      "expected_min": 340,
      "expected_about": 349,
      "observed": 349,
      "pass": true
    }
  },
  "summary": {
    "checks_total": 12,
    "checks_passed": 11,
    "checks_failed": 1,
    "failed_checks": ["evidence_confidence_enum"]
  },
  "notes": [
    "Live verification was read-only via the project-0-recherche Neo4j-Official MCP read-cypher tool against database 'mit-bestand'.",
    "Phase 4.2 rename is clean: AUS_BAUWERK=0, EINGEBAUT_IN=0, FROM_DONOR=286, INTO_RECEIVER=349, total_rels unchanged at 19624.",
    "All four Phase 4.1 hard rules from plan section 4.1 (curated-no-excerpt, bookkeeping-not-derived, propagated-from excerpt, missing-origin) report 0 violations.",
    "evidence_origin distribution is single-valued ('derived' on all 19624 edges); curated and inferred origins are produced by Phase 4b and Phase 3 respectively and are explicitly out of Agent 7 scope.",
    "evidence_confidence enum fails: 15 REFERENZIERT_NORM edges carry 'mittel' which is not in the strict enum {belegt, teilweise_belegt, unklar, inferiert, bookkeeping}.",
    "Agent 7's Phase 4 report itself lists 'mittel' with count 15 in its post-migration distribution, so this is a known unfinished surface left by Phase 4.1 — the canonical migration only normalizes evidence_basis values, never evidence_confidence values.",
    "Suggested follow-up (out of verifier scope): remap 'mittel' -> 'teilweise_belegt' in a Phase 4.1.i step with derivation_note='former_confidence=mittel'."
  ]
}
```
