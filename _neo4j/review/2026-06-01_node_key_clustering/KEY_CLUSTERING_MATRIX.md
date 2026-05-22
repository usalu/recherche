# Node property-key clustering matrix (round 3, mit-bestand)

Goal: reduce the **79 in-use node property keys** as much as possible with **no
data loss** and **no fabricated connections** (any node->node remodeling is left
for manual, evidence-based work).

> Note: the Neo4j browser shows ~**930** property keys, but that is the token
> registry (deleted keys are never garbage-collected). Only 79 are on live nodes.
> Compacting the registry requires a DB dump+reload into a fresh database and is
> tracked separately, not here.

## A. DROP - pure bookkeeping, carries no unique data (13 keys)

Verified they hold no information not already on the graph (e.g. ReuseRule
provenance is on its `BELEGT_IN`/`HAS_SOURCE_LINK` edges):

`evidence_source_id`, `evidence_origin`, `evidence_confidence`, `evidence_basis`,
`source_resolution_status`, `source_count`, `source_url_node_ids`,
`suggested_graph_action`, `source_scope`, `access_date`, `review_run`,
`strict_source_url_cleanup`, `strict_invalid_url_cleanup`.

## B. CLUSTER - synonym keys merged, no data loss (6 keys -> reduction of 6)

- **`title` -> `name`** (`Quelle`): `name = coalesce(name, title)`; where a distinct
  `title` differs from `name` it is appended to `aliases`; then `title` removed.
  (1,830 Quelle had `title` but null `name`; 581 keep title as an alias.)
- **`scope_note`, `short_description`, `definition`, `notes`, `hinweis` -> `beschreibung`**:
  all are free-text descriptions (all STRING). Values concatenated with ` | ` into
  a single `beschreibung`; source keys removed. (collisions, e.g. Programm with
  both `scope_note` + `short_description`, are concatenated - nothing lost.)

## C. KEEP - legitimate distinct fields

- `name_full`: the full/long name, never equal to the short `name` and a deliberate
  2-field design (gap survey enforces `name` <= 25 chars). Folding it into `aliases`
  would be *less* clean, so it stays as its own field.
- `source_file`: provenance file pointer for markdown `Quelle`.
- Domain scalars (`kennwert`, `wert`, `einheit`, `method`, `bilanzgrenze`,
  `alte_funktion`, `neue_funktion`, `reuse_status`, `bg_kind`, `tragend`,
  `year_completed`, `area_m2_gross`, `rank`, `priority`, ...).

## D. REMODEL - MANUAL ONLY, no auto edges (kept intact for now)

These would reduce keys further but require evidence-based, manual matching to
existing node types - **no automatic/fuzzy connection** per the directive. Listed
in `MANUAL_REMODEL_CANDIDATES.md`:

- **`Quelle` URL keys** `source_url`, `source_urls`, `primary_source_url`: 55/60
  ReuseRule URL values are already on a linked `Quelle`, but **5 are unique** -
  dropping would lose them, so kept pending manual handling.
- **`ReuseRule` denormalized payload**: `key_norms`, `required_tests`,
  `pollutant_risks`, `processing_methods` (free-text arrays), `material_id`,
  `material`, `country_iso`, `country_name`, `legal_conditions`, `project_cluster`.
- **`Land` pollutant-regulation years**: `asbest_verbot_jahr`, `pcb_verbot_jahr`,
  `kmf_grenzwert_jahr`, `asbest_neshap_year`, `asbest_note`, `country_iso2`,
  `country_short` (candidate `(Land)-[:REGULIERT {jahr}]->(Schadstoff)`).

## Expected automatic outcome

79 in-use node keys -> **~60** (A: -13, B: -6), zero data loss, zero new edges.
The manual remodel (D) can take it further later under evidence-based review.
