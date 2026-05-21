# Final Verification — Phase 4.1 + 4.2 + 4c

- **Verifier:** Final Verifier 10 of 12 (read-only)
- **Run dir:** `_neo4j/intake/runs/2026-05-20_radical_quality_reset/`
- **Database:** `mit-bestand` (driver creds: `.cursor/mcp.json`)
- **Timestamp (UTC+2):** 2026-05-21 09:05
- **Plan sections:** 4 (incl. 4.1, 4.2) and 4c in `radical_quality-first_reset_8d1e2b66.plan.md`

## Verdict

**OVERALL: FAIL (1 of 16 checks)** — 15 checks PASS, 1 hard-rule violation (check #5).

The violation is a Phase 4.1 hard rule (`evidence_origin='curated'` requires non-null `evidence_excerpt`) that was clean in the Phase 4.1 "after" snapshot (recorded `viol_curated_no_excerpt: 0` at 2026-05-20 23:41) but was **regressed by Phase 4b loader runs** (2026-05-21 00:00–00:08) which inserted 2 108 curated edges without `evidence_excerpt`, predominantly from the actor-registry source (`q_akteursliste_master_md`).

## Phase 4.1 — Canonical evidence shape on every claim edge

| # | Check | Expected | Actual | Result |
|---|-------|---------:|-------:|:------:|
| 1 | `PHASE_4_DONE.flag` present | yes | yes (2026-05-20 23:41) | PASS |
| 2 | Claim-edge types with `evidence_origin IS NULL` | 0 rows | 0 rows | PASS |
| 3 | `evidence_origin` outside `{curated, inferred, derived}` | 0 | 0 | PASS |
| 4 | `evidence_confidence` outside `{belegt, teilweise_belegt, unklar, inferiert, bookkeeping}` | 0 | 0 | PASS |
| 5 | `evidence_origin='curated' AND evidence_excerpt IS NULL` | 0 | **2 108** | **FAIL** |
| 6 | `evidence_confidence='bookkeeping' AND evidence_origin <> 'derived'` | 0 | 0 | PASS |
| 7 | `evidence_excerpt CONTAINS 'propagated from'` | 0 | 0 | PASS |

### Check #5 breakdown (the regression)

Live distribution of the 2 108 curated edges that violate the "curated requires excerpt" hard rule (plan §4.1 line 1091):

| `type(r)` | `evidence_basis` | `evidence_source_id` | count |
|---|---|---|---:|
| `BELEGT_IN` | `cell_citation` | `q_akteursliste_master_md` | 404 |
| `BELEGT_IN` | `cell_citation` | actor S-refs (`q_actor_*_NN`) | 318 |
| `HAT_AKTEURROLLE` | `controlled_vocab` | `q_akteursliste_master_md` | 548 |
| `VERBUNDEN_MIT_AKTEUR` | `controlled_vocab` | `q_akteursliste_master_md` | 289 |
| `LIEGT_IN_LAND` | `controlled_vocab` | `q_akteursliste_master_md` | 201 |
| `HAT_AKTEURTYP` | `controlled_vocab` | `q_akteursliste_master_md` | 193 |
| `ASSOZIIERT_MIT_PROJEKT` | `registry_stub` | `q_akteursliste_master_md` | 142 |
| `BUILT_IN_ERA` | `year_inferred` | `bauwerk.baujahr_property` | 8 |
| `REQUIRES_VERIFICATION_FOR` | `project_rollup` | `q_schadstoff_reuse_knowledge_graph_research_md` | 5 |
| **Total** | | | **2 108** |

Total curated edges live: 4 911; with excerpt: 2 803; without excerpt: 2 108 (42.9 % of all curated edges).

Notes:

- Phase 4.1 "after" snapshot in `PHASE_4_DONE.flag` recorded `viol_curated_no_excerpt: 0`. The flag was created at 2026-05-20 23:41 — **before** the Phase 4b loader runs (2026-05-21 00:00 → 00:08) that re-ingested the actor-registry corpus and re-created these edges as `evidence_origin='curated'` without filling `evidence_excerpt`. The hard rule documented in the plan is unconditional: `evidence_origin='curated'` MUST have a non-null `evidence_excerpt`.
- The `BUILT_IN_ERA` cases with `basis='year_inferred'` and `evidence_source_id='bauwerk.baujahr_property'` are additionally semantically suspect (year-inferred edges should normally carry `evidence_origin='inferred'`, not `'curated'`), but that is outside the scope of this check.
- The earlier-wave verifier-10 finding (15 edges with `evidence_confidence='mittel'`) is **closed**: count is now 0.

## Phase 4.2 — Donor / receiver rename

| # | Check | Expected | Actual | Result |
|---|-------|---------:|-------:|:------:|
| 8 | `PHASE_4_2_DONE.flag` present | yes | yes (2026-05-20 23:41) | PASS |
| 9 | Live `AUS_BAUWERK` count | 0 | 0 | PASS |
| 9 | Live `EINGEBAUT_IN` count | 0 | 0 | PASS |
| 10 | Live `FROM_DONOR` count | ≥ 280 (target ~286) | 286 | PASS |
| 10 | Live `INTO_RECEIVER` count | ≥ 340 (target ~349) | 349 | PASS |

The rename `(:Bauteilgruppe)-[:AUS_BAUWERK]->` → `FROM_DONOR` and `EINGEBAUT_IN` → `INTO_RECEIVER` is complete; no legacy edge types remain.

## Phase 4c — Source-as-link model

| # | Check | Expected | Actual | Result |
|---|-------|---------:|-------:|:------:|
| 11 | `PHASE_4C_DONE.flag` present | yes | yes (2026-05-20 23:36) | PASS |
| 12 | `:Quelle` nodes with non-null `external_sources` | 0 | 0 | PASS |
| 13 | Relationships carrying any of `url` / `http` / `source_file` / `external_sources` keys | 0 | 0 | PASS |
| 14 | `(:Projekt)-[:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})` | 0 | 0 | PASS |
| 15 | `(:Akteur)-[:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})` | ≥ 300 | 365 | PASS |
| 16 | `()-[:ZITIERT_QUELLE]->()` total | ≥ 1 500 (target ~1 747) | 1 747 | PASS |

All Phase 4c invariants hold. The Phase 4c done-flag recorded `akteur_belegt_actor_registry: 360`; live is 365 (delta +5 from later Phase 4b registry top-up — still consistent with the ≥ 300 acceptance bound).

## Cypher used (live, read-only)

```cypher
// Check 2
MATCH ()-[r]->()
WHERE type(r) IN ['BELEGT_IN','HAT_BAUTEILGRUPPE','BETEILIGT_AN','FROM_DONOR',
                  'INTO_RECEIVER','HAS_RISK_POLLUTANT','REQUIRES_VERIFICATION_FOR',
                  'REFERENZIERT_NORM','HAT_AKTEURROLLE','HAT_HUERDE','APPLIES_IN',
                  'APPLIES_TO','BUILT_IN_ERA','ANCHORED_BY','HAT_MARKTMODELL',
                  'ZITIERT_QUELLE','ASSOZIIERT_MIT_PROJEKT']
  AND r.evidence_origin IS NULL
RETURN type(r), count(*);                                        // 0 rows

// Check 3
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['curated','inferred','derived']
RETURN count(r);                                                 // 0

// Check 4
MATCH ()-[r]->()
WHERE r.evidence_confidence IS NOT NULL
  AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
RETURN count(r);                                                 // 0

// Check 5 (FAIL)
MATCH ()-[r]->()
WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NULL
RETURN count(r);                                                 // 2108

// Check 6
MATCH ()-[r]->()
WHERE r.evidence_confidence='bookkeeping'
  AND coalesce(r.evidence_origin,'')<>'derived'
RETURN count(r);                                                 // 0

// Check 7
MATCH ()-[r]->()
WHERE r.evidence_excerpt IS NOT NULL
  AND r.evidence_excerpt CONTAINS 'propagated from'
RETURN count(r);                                                 // 0

// Check 9 + 10
CALL { MATCH ()-[r:AUS_BAUWERK]->() RETURN count(r) AS aus_bauwerk }
CALL { MATCH ()-[r:EINGEBAUT_IN]->() RETURN count(r) AS eingebaut_in }
CALL { MATCH ()-[r:FROM_DONOR]->() RETURN count(r) AS from_donor }
CALL { MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r) AS into_receiver }
RETURN aus_bauwerk, eingebaut_in, from_donor, into_receiver;     // 0,0,286,349

// Check 12
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q); // 0

// Check 13
MATCH ()-[r]->()
WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad
WHERE size(bad) > 0
RETURN count(r);                                                 // 0

// Check 14
MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r);                                                 // 0

// Check 15
MATCH (:Akteur)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r);                                                 // 365

// Check 16
MATCH ()-[r:ZITIERT_QUELLE]->() RETURN count(r);                 // 1747
```

## Recommended remediation (out of scope for this read-only verifier)

To restore the Phase 4.1 hard-rule invariant violated by Phase 4b's registry loader:

1. **Re-parse `q_akteursliste_master_md`** and fill `evidence_excerpt` from the registry JSONL row text (role name, actor type, country code, project association cell) for the 1 920 `q_akteursliste_master_md`-sourced edges in the table above.
2. **Re-parse actor S-ref dossiers** (`q_actor_*_NN`) and fill `evidence_excerpt` from the JSONL row that carries the cited URL for the 318 `BELEGT_IN` edges.
3. **Re-classify `BUILT_IN_ERA` `year_inferred` edges**: change `evidence_origin` from `'curated'` to `'inferred'` (these are derived from `Bauwerk.baujahr`, not from a curated cell), or fill `evidence_excerpt` with the year value.
4. **Fill the 5 `REQUIRES_VERIFICATION_FOR` project-rollup edges** with the verbatim text from `q_schadstoff_reuse_knowledge_graph_research_md` that triggered them.
5. Add a Phase-4.1 hard-constraint check to CI: `MATCH ()-[r]->() WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NULL RETURN count(r) = 0` so future loader changes cannot silently regress this invariant.
