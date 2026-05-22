# Relationship Duplicate Cleanup Plan

Date: 2026-06-02

Scope: live Neo4j graph analyzed via read-only MCP Cypher. No write operations were executed.

## Executive Summary

- There are no duplicate relationships of the same type on the same start and end nodes.
- The cleanup problem is mainly parallel relationship types stored on the same node pair.
- Three high-confidence cleanup targets exist:
  - `HAS_BAUWERK` and `NUTZT_BAUWERK`
  - `GEHÖRT_ZU` and `LIEGT_IN_LAND` for `Akteur -> Land`
  - `ANCHORED_BY` and `BELEGT_IN` for `* -> OntologyAnchor`
- Two medium-confidence transitional duplicates exist:
  - `STUB_PROJECT_LINK` and `BETEILIGT_AN`
  - `GEHÖRT_ZU` and `VERBUNDEN_MIT_AKTEUR` for explicit person or organization membership
- One low-confidence overlap exists but should not be bulk-cleaned:
  - `FROM_DONOR` and `INTO_RECEIVER`

## Findings

### 1. `HAS_BAUWERK` vs `NUTZT_BAUWERK`

- `HAS_BAUWERK`: 166 edges total
- `NUTZT_BAUWERK`: 166 edges total
- Exact overlap on identical `Projekt -> Bauwerk` pairs: 139
- `HAS_BAUWERK` only: 27
- `NUTZT_BAUWERK` only: 10
- `HAS_BAUWERK.role` distribution:
  - `donor`: 98
  - `receiver`: 68
- All 27 `HAS_BAUWERK`-only edges are `role = donor`.

Interpretation:

- `HAS_BAUWERK` is the stronger model because it already carries the project-side role (`donor` or `receiver`).
- `NUTZT_BAUWERK` is a role-free convenience edge and is redundant for 139 pairs.
- The 10 `NUTZT_BAUWERK`-only cases should not be deleted blindly; they need role assignment before migration.

Recommendation:

- Make `HAS_BAUWERK` the canonical stored relationship for `Projekt -> Bauwerk`.
- Treat `NUTZT_BAUWERK` as a derived compatibility edge only, or remove it entirely.

### 2. `GEHÖRT_ZU` vs `LIEGT_IN_LAND`

- `GEHÖRT_ZU`: 250 edges total
- `Akteur -> Land` subset of `GEHÖRT_ZU`: 209 edges, all with `rolle = land`
- Exact overlap with `LIEGT_IN_LAND` on identical `Akteur -> Land` pairs: 195
- `GEHÖRT_ZU`-only `Akteur -> Land`: 14 edges across 13 actors
- `GEHÖRT_ZU` also has 40 `Akteur -> Akteur` membership-style edges

Interpretation:

- For actor geography, `LIEGT_IN_LAND` is the more precise type.
- `GEHÖRT_ZU` should be reserved for membership, hierarchy, or organizational belonging, not geography.
- The 14 `GEHÖRT_ZU`-only actor-country links need review before conversion. At least one actor is linked to more than one country, so these are not safe for automatic migration to location.

Recommendation:

- Make `LIEGT_IN_LAND` canonical for geographic actor-country links.
- Keep `GEHÖRT_ZU` for actor-to-actor membership and hierarchy.
- Review the 14 actor-country residuals individually before converting or deleting them.

### 3. `ANCHORED_BY` vs `BELEGT_IN` on `OntologyAnchor`

- `ANCHORED_BY`: 695 edges total
- `ANCHORED_BY` overlapping `BELEGT_IN` to the same `OntologyAnchor`: 695
- `BELEGT_IN` to `OntologyAnchor` without `ANCHORED_BY`: 0
- `ANCHORED_BY` without `BELEGT_IN` to the same `OntologyAnchor`: 0

Interpretation:

- For `* -> OntologyAnchor`, the graph stores two complete topological copies.
- `BELEGT_IN` is still valid elsewhere in the graph for provenance-style links, but using it against `OntologyAnchor` collapses semantic and provenance layers.
- Property inspection shows the overlap is safe to collapse: overlapping `BELEGT_IN` edges carry only `id`, while overlapping `ANCHORED_BY` edges carry `id` plus `evidence_confidence = unklar`.

Recommendation:

- Make `ANCHORED_BY` the canonical semantic anchor edge.
- Restrict `BELEGT_IN` to evidence or provenance targets such as documents, links, or source objects.
- Before deleting `BELEGT_IN` on `OntologyAnchor`, verify whether any evidence fields on those edges must be preserved elsewhere.

### 4. `STUB_PROJECT_LINK` vs `BETEILIGT_AN`

- `STUB_PROJECT_LINK`: 169 edges total
- Overlap with `BETEILIGT_AN`: 45
  - to `Projekt`: 28
  - to `Programm`: 17
- Remaining `STUB_PROJECT_LINK` without explicit participation edge: 124

Interpretation:

- These are not simple duplicates. They are trust conflicts between an explicit participation edge and a stub edge that often says participation is not confirmed.
- 41 of the 45 overlapping stub edges carry extra stub-only metadata beyond `id` and `evidence_confidence`, most often `not_confirmed_project_participation` and sometimes `association_basis`.
- Only 4 overlap cases are clean redundant stubs without those uncertainty signals.

Recommendation:

- Resolve by rule, not by one-sided bulk delete:
  - keep `STUB_PROJECT_LINK` and delete `BETEILIGT_AN` when the stub marks participation as unconfirmed or carries association-only basis metadata;
  - keep `BETEILIGT_AN` and delete `STUB_PROJECT_LINK` only for the 4 clean redundant stub cases.
- This rule has been executed on the live graph:
  - `41` overlapping `BETEILIGT_AN` edges deleted
  - `4` overlapping `STUB_PROJECT_LINK` edges deleted
  - `4` kept `BETEILIGT_AN` edges upgraded to `evidence_confidence = teilweise_belegt`
  - remaining `STUB_PROJECT_LINK` + `BETEILIGT_AN` overlap: `0`

### 5. `GEHÖRT_ZU` vs `VERBUNDEN_MIT_AKTEUR`

- `GEHÖRT_ZU` `Akteur -> Akteur`: 40
- Exact overlap with `VERBUNDEN_MIT_AKTEUR`: 13

Interpretation:

- The overlap cases look like explicit membership or affiliation pairs, for example person to office or person to institution.
- `GEHÖRT_ZU` is the stronger explicit relation.
- `VERBUNDEN_MIT_AKTEUR` appears to be a looser inferred relation and should not win over an explicit membership edge.
- 8 of the 13 overlapping `VERBUNDEN_MIT_AKTEUR` edges carry `connection_kind = context_affiliation_from_actor_list`.
- 9 of the 13 overlapping generic edges carried stronger `evidence_confidence = teilweise_belegt` than the explicit `GEHÖRT_ZU` edge.

Recommendation:

- Keep `GEHÖRT_ZU` as canonical, upgrade its `evidence_confidence` when the overlapping generic edge is stronger, then delete the redundant `VERBUNDEN_MIT_AKTEUR` edge.
- This rule has been executed on the live graph:
  - `13` overlapping `VERBUNDEN_MIT_AKTEUR` edges deleted
  - `9` `GEHÖRT_ZU` edges now carry `evidence_confidence = teilweise_belegt`
  - remaining `GEHÖRT_ZU` + `VERBUNDEN_MIT_AKTEUR` overlap: `0`

### 6. `FROM_DONOR` vs `INTO_RECEIVER`

- `FROM_DONOR`: 284 edges total
- `INTO_RECEIVER`: 345 edges total
- Exact overlap: 28

Interpretation:

- Sample rows show mostly retained or self-context cases where the same `Bauteilgruppe` is modeled as both coming from and ending in the same building context.
- This is not a safe bulk-duplicate class.

Recommendation:

- Do not auto-clean this pair.
- Review only if you want to distinguish retained-in-place semantics from donor or receiver flow semantics.

## Canonical Relationship Rules

Use these as the cleanup target state:

- `Projekt -> Bauwerk`: `HAS_BAUWERK` is canonical.
- `Akteur -> Land`: `LIEGT_IN_LAND` is canonical.
- `Akteur -> Akteur` membership or affiliation: `GEHÖRT_ZU` is canonical.
- `* -> OntologyAnchor`: `ANCHORED_BY` is canonical.
- `Akteur -> Projekt|Programm`: `BETEILIGT_AN` is canonical.
- `STUB_PROJECT_LINK` remains only as unresolved intake residue.

## Cleanup Plan

### Phase 1. Export review sets before mutation

Export these candidate sets to CSV or JSON before any writes:

- 10 `NUTZT_BAUWERK`-only pairs
- 14 `GEHÖRT_ZU`-only `Akteur -> Land` pairs
- 695 `BELEGT_IN -> OntologyAnchor` pairs
- 45 overlapping `STUB_PROJECT_LINK` pairs
- 13 overlapping `GEHÖRT_ZU` and `VERBUNDEN_MIT_AKTEUR` pairs

### Phase 2. Repair missing canonical edges

- Review the 10 `NUTZT_BAUWERK`-only project-building pairs and create missing `HAS_BAUWERK` edges with explicit `role`.
- Review the 14 `GEHÖRT_ZU`-only actor-country pairs and create `LIEGT_IN_LAND` only where the semantics are truly geographic.
- If `BELEGT_IN` on `OntologyAnchor` carries evidence fields you still need, migrate those fields to a proper provenance structure before deletion.

### Phase 3. Delete redundant overlapping edges

After Phase 2 review and migration:

- Delete 139 overlapping `NUTZT_BAUWERK` edges where the same `HAS_BAUWERK` already exists.
- Delete 195 overlapping `GEHÖRT_ZU` actor-country edges where the same `LIEGT_IN_LAND` already exists.
- Delete 695 `BELEGT_IN` edges whose target is `OntologyAnchor` if `ANCHORED_BY` remains canonical.
- Resolve the 45 overlapping `STUB_PROJECT_LINK` cases with the trust-aware split rule described above.
- Resolve the 13 overlapping `GEHÖRT_ZU` and `VERBUNDEN_MIT_AKTEUR` cases by keeping explicit membership and upgrading confidence where supported.

### Phase 4. Add guard queries to the import QA

Add read-only QA checks that fail the intake if any of the following are non-zero:

- `Projekt -> Bauwerk` pairs carrying both `HAS_BAUWERK` and `NUTZT_BAUWERK`
- `Akteur -> Land` pairs carrying both `GEHÖRT_ZU` and `LIEGT_IN_LAND`
- `* -> OntologyAnchor` pairs carrying both `ANCHORED_BY` and `BELEGT_IN`
- `Akteur -> Projekt|Programm` pairs carrying both `STUB_PROJECT_LINK` and `BETEILIGT_AN`

## Suggested QA Queries

```cypher
MATCH (p:Projekt)-[:HAS_BAUWERK]->(b:Bauwerk)
WHERE EXISTS { MATCH (p)-[:NUTZT_BAUWERK]->(b) }
RETURN count(*) AS overlappingProjectBauwerkPairs;
```

```cypher
MATCH (a:Akteur)-[:GEHÖRT_ZU]->(l:Land)
WHERE EXISTS { MATCH (a)-[:LIEGT_IN_LAND]->(l) }
RETURN count(*) AS overlappingActorCountryPairs;
```

```cypher
MATCH (n)-[:ANCHORED_BY]->(a:OntologyAnchor)
WHERE EXISTS { MATCH (n)-[:BELEGT_IN]->(a) }
RETURN count(*) AS overlappingAnchorPairs;
```

```cypher
MATCH (a:Akteur)-[:STUB_PROJECT_LINK]->(x)
WHERE EXISTS { MATCH (a)-[:BETEILIGT_AN]->(x) }
RETURN count(*) AS overlappingStubParticipationPairs;
```

## Priority Order

1. `ANCHORED_BY` vs `BELEGT_IN` on `OntologyAnchor`
2. `HAS_BAUWERK` vs `NUTZT_BAUWERK`
3. `GEHÖRT_ZU` vs `LIEGT_IN_LAND`
4. `STUB_PROJECT_LINK` vs `BETEILIGT_AN`
5. `GEHÖRT_ZU` vs `VERBUNDEN_MIT_AKTEUR`
6. `FROM_DONOR` vs `INTO_RECEIVER` review only