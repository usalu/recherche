# Relationship Duplicate Cleanup Package

Date: 2026-06-02

This package operationalizes the safe subset of the duplicate-relationship cleanup identified in [_neo4j/review/2026-06-02_RELATIONSHIP_DUPLICATE_CLEANUP_PLAN.md](../2026-06-02_RELATIONSHIP_DUPLICATE_CLEANUP_PLAN.md).

## Scope

This package separates the cleanup into two classes:

- safe auto-delete relationship overlaps
- review-only overlaps that still carry distinct metadata

## Safe Auto-Delete Set

These three classes are ready for scripted deletion because the canonical edge is semantically stronger and no overlapping edge carries stronger unique metadata:

1. `BELEGT_IN -> OntologyAnchor` when the same endpoints already have `ANCHORED_BY`
2. `NUTZT_BAUWERK` on `Projekt -> Bauwerk` when the same endpoints already have `HAS_BAUWERK`
3. `GEHÖRT_ZU` on `Akteur -> Land` with `rolle = land` when the same endpoints already have `LIEGT_IN_LAND`

Evidence basis from live graph inspection:

- overlapping `BELEGT_IN` edges on `OntologyAnchor` only carry `id`
- overlapping `ANCHORED_BY` edges carry `id` plus `evidence_confidence = unklar`
- overlapping `NUTZT_BAUWERK` edges carry `evidence_confidence = unklar`
- overlapping `HAS_BAUWERK` edges carry `role` plus `evidence_confidence = teilweise_belegt`
- overlapping `GEHÖRT_ZU` actor-country edges carry `evidence_confidence = unklar`
- overlapping `LIEGT_IN_LAND` edges carry `evidence_confidence = teilweise_belegt`

## Review-Only Set

These overlaps should not be bulk-deleted yet:

- `NUTZT_BAUWERK`-only residuals without `HAS_BAUWERK`
- `GEHÖRT_ZU`-only actor-country residuals without `LIEGT_IN_LAND`

Reason:

- 10 `NUTZT_BAUWERK`-only project-building pairs still need explicit `HAS_BAUWERK.role`
- 14 `GEHÖRT_ZU`-only actor-country links still need location review

## Conflict-Resolution Set

These two overlap classes are resolved by explicit migration rules rather than blind delete:

### 4. `STUB_PROJECT_LINK` vs `BETEILIGT_AN`

- Overlap count before resolution: `45`
- Decision rule:
   - keep `STUB_PROJECT_LINK` and delete `BETEILIGT_AN` when the stub itself signals uncertainty via `not_confirmed_project_participation = true` or carries `association_basis`
   - keep `BETEILIGT_AN` and delete `STUB_PROJECT_LINK` only for the small clean residual set where the stub carries neither uncertainty nor association-basis metadata
- Live split:
   - keep `STUB_PROJECT_LINK`: `41`
   - keep `BETEILIGT_AN`: `4`

### 5. `GEHÖRT_ZU` vs `VERBUNDEN_MIT_AKTEUR`

- Overlap count before resolution: `13`
- Decision rule:
   - keep explicit `GEHÖRT_ZU`
   - upgrade `GEHÖRT_ZU.evidence_confidence` from overlapping `VERBUNDEN_MIT_AKTEUR` when the generic edge is stronger
   - delete overlapping `VERBUNDEN_MIT_AKTEUR`

## Files

- `cypher/05_validation_and_review_queries.cypher`
- `cypher/10_safe_delete_belegt_in_ontology_anchor.cypher`
- `cypher/20_safe_delete_nutzt_bauwerk_overlaps.cypher`
- `cypher/30_safe_delete_actor_country_overlaps.cypher`
- `cypher/40_resolve_stub_project_link_beteiligt_an_overlaps.cypher`
- `cypher/50_resolve_gehoert_zu_verbunden_overlaps.cypher`
- `cypher/90_post_cleanup_validation.cypher`

## Recommended Order

1. Run the read-only queries in `cypher/05_validation_and_review_queries.cypher` in Neo4j Browser or via MCP `read-cypher`.
2. Execute the three safe delete scripts in order.
3. Re-run `cypher/90_post_cleanup_validation.cypher` in Browser or via MCP `read-cypher`.
4. Review the residual rows from `cypher/05_validation_and_review_queries.cypher` before touching stub or generic-actor overlaps.

## Running the Write Scripts

The repo already contains a Cypher file runner:

```powershell
python _scripts/_run_cypher_file.py --cypher _neo4j/review/2026-06-02_relationship_duplicate_cleanup/cypher/10_safe_delete_belegt_in_ontology_anchor.cypher
python _scripts/_run_cypher_file.py --cypher _neo4j/review/2026-06-02_relationship_duplicate_cleanup/cypher/20_safe_delete_nutzt_bauwerk_overlaps.cypher
python _scripts/_run_cypher_file.py --cypher _neo4j/review/2026-06-02_relationship_duplicate_cleanup/cypher/30_safe_delete_actor_country_overlaps.cypher
```

`_scripts/_run_cypher_file.py` now reports delete counters, so successful runs will show `rels_deleted=...`.

## Expected Delete Counts


If a run produces different counts, stop and re-run the validation queries before continuing.# Relationship Duplicate Cleanup Package

## Live Execution Result

Executed on 2026-06-02 against the live `mit-bestand` graph.

- `10_safe_delete_belegt_in_ontology_anchor.cypher`: `rels_deleted=695`
- `20_safe_delete_nutzt_bauwerk_overlaps.cypher`: `rels_deleted=139`
- `30_safe_delete_actor_country_overlaps.cypher`: `rels_deleted=195`
- `40_resolve_stub_project_link_beteiligt_an_overlaps.cypher`: `rels_deleted=45`, split as `41` deleted `BETEILIGT_AN`, `4` deleted `STUB_PROJECT_LINK`, `4` confidence upgrades on kept `BETEILIGT_AN`
- `50_resolve_gehoert_zu_verbunden_overlaps.cypher`: `rels_deleted=13`, with `9` effective confidence upgrades on kept `GEHÖRT_ZU`
- Total relationships deleted by the safe cleanup set: `1029`
- Total relationships deleted after overlap conflict resolution: `1087`

Post-cleanup validation:

- overlapping `BELEGT_IN -> OntologyAnchor`: `0`
- overlapping `Projekt -> Bauwerk` `NUTZT_BAUWERK` + `HAS_BAUWERK`: `0`
- overlapping `Akteur -> Land` `GEHÖRT_ZU` + `LIEGT_IN_LAND`: `0`
- overlapping `STUB_PROJECT_LINK` + `BETEILIGT_AN`: `0`
- overlapping `GEHÖRT_ZU` + `VERBUNDEN_MIT_AKTEUR`: `0`
- total relationships after cleanup: `24017`

Residual review sets intentionally left in place:

- `NUTZT_BAUWERK`-only `Projekt -> Bauwerk`: `10`
- `GEHÖRT_ZU`-only `Akteur -> Land`: `14`
- remaining `GEHÖRT_ZU` topology: `40` `Akteur -> Akteur`, `14` `Akteur -> Land`, `1` `Software -> Land`
- remaining `NUTZT_BAUWERK` topology: `10` `Projekt -> Bauwerk`, `16` `Projekt -> Materialdepot`, `1` `Akteur -> Bauwerk`
- remaining `STUB_PROJECT_LINK`: `165`
- remaining `BETEILIGT_AN`: `611`
- remaining `VERBUNDEN_MIT_AKTEUR`: `289`

Post-cleanup diagnostic note:

- `_scripts/_gap_survey.py` was updated from legacy `NUTZT_BAUWERK` to canonical `HAS_BAUWERK`.
- The artificial `Projekt missing NUTZT_BAUWERK` regression is gone.
- Remaining failing survey checks after cleanup are unrelated open items:
   - `r.id NULL = 127`
   - `Case-specific nodes missing BELEGT_IN = 4`
   - `BG missing HAT_MATERIALGRUPPE = 1`
   - `BG missing HAT_WIEDERVERWENDUNGSART = 2`

Date: 2026-06-02

This package turns the live duplicate analysis into executable cleanup steps.

Source analysis:

- `_neo4j/review/2026-06-02_RELATIONSHIP_DUPLICATE_CLEANUP_PLAN.md`

## Scope

This package separates the graph into:

- safe auto-delete duplicates
- review-only residuals that still need semantic decisions

## Safe auto-delete classes

### 1. `BELEGT_IN -> OntologyAnchor`

- Delete only when the same source node already has `ANCHORED_BY` to the same `OntologyAnchor`.
- Live graph finding: 695 overlapping pairs.
- Safety note: overlapping `BELEGT_IN` edges carry only `id`; overlapping `ANCHORED_BY` edges already carry `id` and `evidence_confidence`.

### 2. `NUTZT_BAUWERK` on `Projekt -> Bauwerk`

- Delete only when the same `Projekt -> Bauwerk` pair already has `HAS_BAUWERK`.
- Live graph finding: 139 overlapping pairs.
- Safety note: overlapping `NUTZT_BAUWERK` has `evidence_confidence = unklar`; overlapping `HAS_BAUWERK` already carries stronger semantics plus `role`.
- Important limit: the graph also has `NUTZT_BAUWERK` on `Projekt -> Materialdepot` and one `Akteur -> Bauwerk` edge. This package does not touch those cases.

### 3. `GEHÖRT_ZU` on `Akteur -> Land`

- Delete only when `rolle = 'land'` and the same actor already has `LIEGT_IN_LAND` to the same country.
- Live graph finding: 195 overlapping pairs.
- Safety note: overlapping `GEHÖRT_ZU` has weaker confidence than overlapping `LIEGT_IN_LAND`.
- Important limit: `LIEGT_IN_LAND` is used by other labels too, and `GEHÖRT_ZU` is still needed for `Akteur -> Akteur` membership.

## Review-only classes

These remain out of the auto-delete scripts because they still carry distinct review metadata or weaker semantics that should be inspected first:

- 10 `NUTZT_BAUWERK`-only `Projekt -> Bauwerk` pairs
- 14 `GEHÖRT_ZU`-only `Akteur -> Land` pairs
- overlapping `STUB_PROJECT_LINK` and `BETEILIGT_AN` pairs
- overlapping `GEHÖRT_ZU` and `VERBUNDEN_MIT_AKTEUR` actor membership pairs

## Suggested execution order

1. Inspect `cypher/01_precheck_duplicate_cleanup.cypher` in Neo4j Browser or via MCP read-cypher.
2. Inspect `cypher/02_review_only_residuals.cypher` and confirm no residuals need migration first.
3. Run the safe delete scripts in this order:
   - `cypher/10_delete_overlapping_belegt_in_ontology_anchor.cypher`
   - `cypher/20_delete_overlapping_nutzt_bauwerk_project_bauwerk.cypher`
   - `cypher/30_delete_overlapping_gehoert_zu_land_actor_country.cypher`
4. Run `cypher/90_postcheck_duplicate_cleanup.cypher`.

## Runner

The repo already includes `_scripts/_run_cypher_file.py` for executing write `.cypher` files against the live database.

Example commands:

```powershell
python _scripts/_run_cypher_file.py --cypher _neo4j/review/2026-06-02_relationship_duplicate_cleanup/cypher/10_delete_overlapping_belegt_in_ontology_anchor.cypher
python _scripts/_run_cypher_file.py --cypher _neo4j/review/2026-06-02_relationship_duplicate_cleanup/cypher/20_delete_overlapping_nutzt_bauwerk_project_bauwerk.cypher
python _scripts/_run_cypher_file.py --cypher _neo4j/review/2026-06-02_relationship_duplicate_cleanup/cypher/30_delete_overlapping_gehoert_zu_land_actor_country.cypher
```

The runner now reports delete counters, so each script execution should show `rels_deleted=<expected_count>`.