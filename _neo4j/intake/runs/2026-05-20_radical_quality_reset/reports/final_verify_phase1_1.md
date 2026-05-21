# Final Verification — Phase 1.1 (Final Verifier 1 of 12)

- **Phase**: 1.1 — Demote `Wiederverwendungskette` (chains → BG properties)
- **Database**: `mit-bestand` (live, read-only via Neo4j Python driver)
- **Run dir**: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Verifier executed**: 2026-05-21
- **Mode**: Read-only (no writes performed)

## Check Results

| # | Check | Expected | Observed | Result |
|---|-------|----------|----------|--------|
| 1 | `migrations/mig_1_1_demote_chains.cypher` exists | file present | present (3776 bytes) | **PASS** |
| 2 | `PHASE_1_1_DONE.flag` parseable, `ok=true` | ok=true | found in `logs/PHASE_1_1_DONE.flag`, `ok: true` | **PASS** |
| 3 | `deleted/phase1_1_chains.jsonl` has exactly 98 lines | 98 | 98 | **PASS** |
| 4 | `reports/agent_2_phase1_1_report.md` exists | file present | present (7231 bytes) | **PASS** |
| 5 | Live `count(:Wiederverwendungskette)` == 14 | 14 | 14 | **PASS** |
| 6 | Live unwired chains (missing FROM_DONOR or INTO_RECEIVER) == 0 | 0 | 0 | **PASS** |
| 7 | Live `count(r) WHERE r.migration_origin='mig_1_1_demote_chains'` >= 290 | ≥ 290 | 297 | **PASS** |
| 8 | Sample 5 demoted edges: `evidence_source_id` non-null AND (`evidence_basis='demoted_from_kette'` OR `derivation_note CONTAINS 'former_basis=demoted_from_kette'`) | all 5 satisfy | 5/5 satisfy (4 direct `demoted_from_kette`, 1 propagated with matching `former_basis` note) | **PASS** |

## Live Counts (mit-bestand)

```
MATCH (k:Wiederverwendungskette) RETURN count(k)
  -> 14

MATCH (k:Wiederverwendungskette)
WHERE NOT (exists{(k)-[:FROM_DONOR]->()} AND exists{(k)-[:INTO_RECEIVER]->()})
RETURN count(k)
  -> 0

MATCH ()-[r]->() WHERE r.migration_origin='mig_1_1_demote_chains'
RETURN count(r)
  -> 297
```

## Sampled Demoted Edges (5)

| # | reltype | evidence_source_id | evidence_basis | derivation_note |
|---|---------|--------------------|----------------|-----------------|
| 1 | HAT_METHODE  | k_green_house_knoopkazerne_tiel_to_pavilion | demoted_from_kette | — |
| 2 | HAT_METHODE  | k_green_house_knoopkazerne_tiel_to_pavilion | demoted_from_kette | — |
| 3 | HAT_LOGISTIK | k_green_house_knoopkazerne_tiel_to_pavilion | demoted_from_kette | — |
| 4 | HAT_LOGISTIK | k_green_house_knoopkazerne_tiel_to_pavilion | demoted_from_kette | — |
| 5 | HAT_HUERDE   | k_green_house_knoopkazerne_tiel_to_pavilion | propagated         | former_basis=demoted_from_kette |

All 5 sample edges have non-null `evidence_source_id`. Four edges match `evidence_basis='demoted_from_kette'` directly; the fifth is a `propagated` edge whose `derivation_note` contains `former_basis=demoted_from_kette` (acceptable per check 8 disjunction).

## Deviations / Notes

- `PHASE_1_1_DONE.flag` resides in `logs/` rather than the run-dir root. The task statement explicitly allows "anywhere in run dir, root or logs/", so this is compliant.
- Edges count is **297**, which is consistent with the flag (`edges_demoted: 297`) and exceeds the ≥ 290 threshold (the plan target was a soft floor; minor variance is expected since some demoted edges may have been propagated further by downstream phases without losing the migration_origin tag).
- No `Wiederverwendungskette` regression detected: 14 chains remain (the surviving anchored set from the plan), 0 unwired.

## Overall

**PASS — all 8 checks satisfied.** Phase 1.1 is confirmed complete and consistent against `mit-bestand`.
