# Bauteilbörsen Integration Plan

Date: 2026-05-28

## Scope

Checked all 39 legacy profiles in `_archive/research/bauteilboerse/` against the live Neo4j graph. The archive is treated as reviewed legacy input, not as canonical truth. Neo4j remains the source of truth; integration must preserve legacy provenance and review status.

Generated audit artifacts:

- `content_inventory.json` - full parsed content for every section in every profile.
- `content_inventory.csv` - compact sortable inventory.
- `ACTION_MATRIX.md` - per-profile action matrix.
- `existing_semantic_node_context.json` - live graph context for already matched semantic nodes.
- `CONTENT_COVERAGE.md` - explicit coverage check for frontmatter, title, all sections, URLs, and footer note.
- `FINAL_GRAPH_PREVIEW.md` - visual target graph preview before import.

## Double-Check Result

- Profiles checked: 39/39.
- Required sections present: 39/39.
- Live source containers already exist: 39/39 as `q_research_*_md`.
- Profiles without URLs: 0/39.
- Candidate country nodes all exist for concrete countries.
- `region_europa` appears only as service scope in Loopfront and Restado; do not create a fake `Land` node for Europe.
- Existing vocabulary is sufficient: `at_materialhub_bauteilboerse` and all needed `Akteurrolle` ids exist.
- 38/39 profiles contain uncertainty markers, mainly in `Geschäftsmodell`, `Ökologische Bewertung`, `Daten je Bauteil`, `Qualität / Prüfung`, or `Logistik / Lagerung`.
- Structural content coverage is complete: 39/39 files have `type: Bauteilbörse`, matching H1 title, all 17 required sections, at least one URL, and the footer warning note.

## Live Graph Fit

Current semantic action split:

- 29 profiles: create new materialhub actor.
- 6 profiles: update existing materialhub actor.
- 1 profile: reconcile existing network context.
- 2 profiles: create platform node and link to existing operator.
- 1 profile: link existing software node to existing operator.

Existing materialhub actor matches:

- `baukarussell`
- `bauteilboerse_bremen`
- `bauteilladen_winterthur`
- `gebruiktebouwmaterialen`
- `new_horizon` for Oogstkaart / New Horizon
- `rotordc`

Existing non-direct or partial matches:

- `bauteilnetz_deutschland` exists as network actor and should keep that context.
- `software_restado` exists as `Software`; `concular` exists as the operator actor.
- `salvo_ltd` exists as operator for SalvoWEB.
- `materialnomaden` exists as operator context for re:store / HarvestMAP Vienna.

Existing nodes needing completion before the new batch is considered complete:

- `bauteilboerse_bremen`: missing `BELEGT_IN` to the profile source container.
- `bauteilladen_winterthur`: missing country relation.
- `gebruiktebouwmaterialen`: missing country relation.
- `salvo_ltd`: missing country relation and `BELEGT_IN`.
- `software_restado`: missing country/service-scope modeling via operator relation.

## Target Graph Shape

Use existing graph vocabulary only.

Graph-first rule:

- Do not copy archive sections into long text properties on semantic nodes.
- Import only content that can be linked to existing graph content as nodes and relationships.
- Keep only minimal node identity/provenance properties such as `id`, `name`, `aliases`, `source_scope`, `review_run`, and `review_status`.
- If a section cannot be mapped to existing graph content without inventing weak nodes or storing prose blobs, do not import that section semantically in this batch.
- The raw archive file and existing `q_research_*_md` source container remain the provenance record for dropped/non-graphable prose.

For each accepted profile:

- Create or update one semantic platform/actor anchor.
- For `Akteur` anchors, attach `HAT_AKTEURTYP -> at_materialhub_bauteilboerse` when the profile describes a materialhub, marketplace, Bauteilbörse, or reuse-material platform.
- For non-actor anchors such as `software_restado`, keep the node's existing label and connect it to its operator; actor type and roles belong on the operator actor.
- For `Akteur` anchors, attach `HAT_AKTEURROLLE` from the candidate roles in `content_inventory.json`.
- Attach concrete country with `LIEGT_IN_LAND`.
- Do not store broader service scope such as DACH, Nordics, or Europe as text. Model it only if a suitable graph node already exists; otherwise drop it from the semantic import.
- Link distinct platforms to operators with `BETRIEBEN_VON`.
- Use `BELEGT_IN` from semantic nodes to their `q_research_*_md` source containers.
- Link source URL nodes through `HAS_SOURCE_LINK` or existing source-container linkage; do not reintroduce `ZITIERT_QUELLE`.
- Use `DataIssue` / `HAS_DATA_ISSUE` only for uncertainty that affects an accepted graph fact, not for every vague sentence.

Use `review_status = "reviewed_legacy_profile_needs_url_fact_check"` for imported archive-derived graph facts unless the URLs are checked in the same batch.

## Content Graph Disposition

Every archive content class is checked, but not every class should become graph content. The import should preserve graphable facts and deliberately drop prose/evaluations that cannot be linked cleanly to existing vocabulary.

| Archive content | Planned graph treatment |
|---|---|
| YAML frontmatter `type` | Link to `Akteurtyp` via `HAT_AKTEURTYP`; no text property. |
| H1 title | Use as `name` / alias on the semantic anchor only. |
| `Kurzbeschreibung` | Extract only graphable facts already covered by country, actor type, roles, operator, platform/software/depot nodes. Drop residual prose. |
| `Land / Region` | Link concrete countries with `LIEGT_IN_LAND`. Drop broad scopes such as DACH/Nordics/Europe unless an approved region node exists. |
| `Betreiber` | Create/link `Akteur` nodes and `BETRIEBEN_VON` where the operator is explicit. If operator is unclear, do not create an operator node; optionally attach `HAS_DATA_ISSUE`. |
| `Zielgruppe` | Drop for this batch unless an existing controlled target-audience node is found; do not encode as text. |
| `Plattformtyp` | Map to `Akteurtyp`, `Software`, `Tool`, `Materialdepot`, `Marktmodell`, or `Akteurrolle` only when unambiguous. Drop residual wording. |
| `Bauteilkategorien` | Link to existing `Bauteilgruppe` / `Materialgruppe` nodes only when the category maps cleanly. Drop broad shop-category prose. |
| `Art der Wiederverwendung` | Link to existing `WiederverwendungsArt` via `HAT_WIEDERVERWENDUNGSART` when unambiguous. Drop residual wording. |
| `Funktionen` | Map to roles, `Software`/`Tool`, `Materialdepot`, `HAT_MARKTMODELL`, or `HAT_LOGISTIK` only when graphable. Drop feature prose. |
| `Daten je Bauteil` | Drop unless it maps to an existing data/quality/matching node. Do not store product-data descriptions as text. |
| `Qualität / Prüfung` | Link to existing `PruefungNachweis`, `ZustandsKlasse`, or `DataIssue` only when explicit. Drop vague checks like "details vary by product". |
| `Logistik / Lagerung` | Link to existing `Logistik` or create/link `Materialdepot` only when explicit. Drop uncertain delivery/collection prose. |
| `Geschäftsmodell` | Link to existing `Marktmodell` / `Wirtschaft` nodes only when unambiguous. Drop fee/revenue prose if no controlled node exists. |
| `Ökologische Bewertung` | Link only quantitative `Kennwert`, certification, or explicit assessment nodes if present. Drop generic ecological benefit statements. |
| `Stärken` | Drop; evaluative prose is not graph content. |
| `Schwächen / Hemmnisse` | Link to existing `Huerde` / `HuerdeKategorie` or `DataIssue` only when graphable. Drop residual prose. |
| `Relevanz für zirkuläres Bauen` | Use only to justify existing type/role links. Drop residual summary prose. |
| `Quellen und Links` | Link existing `Quelle` / `ExternalLink` nodes through `BELEGT_IN` / `HAS_SOURCE_LINK`; no URL arrays on semantic nodes. |
| Footer `Hinweis` | Drop from semantic graph import; it is a generic caution retained only in the raw source container. |

## Batch Plan

1. Preflight

Run `_scripts/_gap_survey.py`, create a graph backup, and freeze the inventory artifacts in this run directory.

2. Source container normalization

Confirm all 39 `q_research_*_md` source containers have `source_file`, `source_url_node_ids`, `review_status`, and `source_resolution_status`. Add missing profile-to-source `BELEGT_IN` relationships for existing semantic nodes.

3. Existing node completion

Update the six existing materialhub actors with missing countries, aliases, graphable role/type links, source links, and direct `BELEGT_IN`. Keep DossierEntityTarget nodes out of the materialhub visualization unless explicitly needed.

4. Partial-node reconciliation

For Bauteilnetz Deutschland, keep `at_ngo_verband_netzwerk` and add materialhub/network context only with a review note.

For Restado, keep `software_restado` as `Software`, add `BETRIEBEN_VON -> concular`, and include it in the Bauteilbörsen graph through the software/operator path rather than forcing a duplicate actor.

5. New semantic nodes

Create the 29 missing materialhub actors from the action matrix. Each new node gets only graphable links: country, actor type, roles, operator/platform links where explicit, source URL links, and `BELEGT_IN`. Do not add section text properties.

6. Distinct platform/operator nodes

Create platform nodes for SalvoWEB and re:store / HarvestMAP Vienna, then link them to `salvo_ltd` and `materialnomaden` with `BETRIEBEN_VON`.

7. Validation

Required checks after dry run and after apply:

- `python _scripts/_gap_survey.py` shows no new regressions.
- 39/39 archive profiles resolve to at least one semantic graph anchor.
- 39/39 semantic anchors have `BELEGT_IN` to their profile source container.
- 39/39 semantic anchors have concrete country links where a concrete country exists in the profile.
- Every imported archive fact is represented as a node/relationship, not as a long text property.
- Every non-imported content class has an explicit "drop" disposition in the content graph disposition table.
- No duplicate reciprocal `VERBUNDEN_MIT_AKTEUR` pairs are introduced.
- No new `ZITIERT_QUELLE` relationships are introduced.
- The Bauteilbörsen graph query returns actors/platforms, countries, roles, operators, and source containers.

## Import Patch Shape

Prepare one dry-run patch JSONL first:

- `add_node` only for semantic anchors, operators, source-supporting nodes, or controlled graph targets that already fit the vocabulary.
- `set_node_properties` only for minimal identity/provenance fields; no copied archive-section prose.
- `add_rel` for `HAT_AKTEURTYP`, `HAT_AKTEURROLLE`, `LIEGT_IN_LAND`, `BETRIEBEN_VON`, `BELEGT_IN`, `HAS_SOURCE_LINK`, and any other existing controlled relation used by the graph disposition table.
- Stable relationship ids in the form `r_<from>__<TYPE>__<to>`.
- Every operation carries `source_scope = "bauteilboerse_legacy_review"` and `review_run = "2026-05-28_bauteilboersen_integration_plan"`.

Only apply after dry-run diff review and backup.
