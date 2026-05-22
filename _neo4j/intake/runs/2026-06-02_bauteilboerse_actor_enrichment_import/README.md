# Bauteilbörse Actor Enrichment Edges Import (2026-06-02)

Continuation of [2026-06-01_project_part_actor_import_all/](../2026-06-01_project_part_actor_import_all/).
The prior run imported the 91 `BETEILIGT_AN` edges (`project_part_actor_edge_enrichment_existing_node_types_2026_06_01` slice).
This run imports the remaining web-evidenced enrichment slices from the same source JSON.

## Source

`_neo4j/intake/inbox/research/bauteilboerse_network_2026-06-01_project_part_actor_edges.json`

Three slices are *not yet imported*:

| `enrichment_run` | Edges | All have real URL? |
|---|---:|---|
| `actor_edge_enrichment_existing_types_2026_06_01` | 215 | 215/215 |
| `actor_edge_enrichment_deep_existing_types_2026_06_01` | 102 | 102/102 |
| `edge_enrichment_deeper_existing_node_types_2026_06_01` | 226 | 66/226 (rest have `internal:` placeholder) |

## Selection rule

Per user direction "import whatever is provided with an evidence ... not duplicating or cluttering":

- Include if `evidence_url` is present **and** does not start with `internal:`.
- Result: **383 edges** = 215 + 102 + 66.
- Skipped: 160 `internal:`-only `Projekt`-shortcut edges from the `_deeper_` slice. Those duplicate two-hop paths already
  reachable via `Projekt → Bauteilgruppe → Bauteiltyp / Material` and are not Bauteilbörse-specific.

## Schema guardrails (enforced at runtime, not just JSON-time)

Two cardinality-1 edge types need DB-level checks before MERGE:

| Edge | Schema cardinality | Risk in this batch |
|---|---|---|
| `HAT_MARKTMODELL` | 1 per actor | `enviromate` would receive a 2nd `HAT_MARKTMODELL` (`mm_spende`) |
| `LIEGT_IN_LAND` | 1 per actor | `software_opalis` would receive 3 (`land_belgien`, `land_frankreich`, `land_niederlande`) |

For every row, the importer:

1. Verifies `(source.id, target.id)` exist in DB.
2. For `HAT_MARKTMODELL` / `LIEGT_IN_LAND`: skips if the source already has an edge of that type to a *different* target.
3. For all other types: skips if a relationship of the same `type` between the same `src` and `tgt` already exists with a different `id` (parallel-edge prevention).
4. Otherwise `MERGE`-es by relationship `id`.

Skipped rows are written to `SKIPPED.csv` with a reason.

## What the importer writes (per imported edge)

```
evidence_basis              = row.evidence_basis        (source text justifying the edge)
evidence_url                = row.evidence_url          (operator URL — singular per row)
evidence_confidence         = 'abgeleitet'              (overridden, see below)
import_original_evidence_confidence
                            = row.evidence_confidence   (belegt | abgeleitet | abgeleitet_belegt | abgeleitet_aus_bestehender_bauteilgruppe)
scope_note                  = row.scope_note            (when present)
via_bauteilgruppe_id        = row.via_bauteilgruppe_id  (only present on _deeper_ slice rows)
enrichment_run              = row.enrichment_run        (the originating slice id)
import_source_file          = 'bauteilboerse_network_2026-06-01_project_part_actor_edges.json'
import_source_slice         = row.enrichment_run
review_run                  = 'bauteilboerse_actor_enrichment_import_2026_06_02'
import_decision             = 'import_all_for_now'
review_status               = 'needs_source_url_review'
source_resolution_status    = 'needs_source_url_review'
source_status               = 'candidate'
source_status_reason        = 'candidate_url_needs_fact_review'
candidate_source_urls       = [row.evidence_url]
candidate_source_basis      = 'bauteilboerse_actor_enrichment_import_2026_06_02'
created_at_utc              = row.created_at_utc  (only on first create)
```

`evidence_confidence` is normalised to `abgeleitet` even when the row says `belegt`. The original value is preserved in
`import_original_evidence_confidence`. This is the same policy the prior import used: imported facts stay
`needs_source_url_review` until a human confirms the URL really substantiates the claim.

## Post-import schema check

After import, the script re-runs the Bauteilbörse schema check on every Akteur/Software/Tool that was touched
(same check used in [`_fix_post_patch.py`](../../inbox/research/_fix_post_patch.py)). Any actor that drops below the
required-edge thresholds is printed.

## Run

```powershell
python _neo4j/intake/runs/2026-06-02_bauteilboerse_actor_enrichment_import/_run_import_actor_enrichment_edges.py
```

Connection defaults match the prior run (`neo4j://127.0.0.1:7687`, db `mit-bestand`, password from `.neo4j_password`).

## Files

- `_run_import_actor_enrichment_edges.py` — importer.
- `SKIPPED.csv` — written by the importer; one row per skipped edge with reason.
- `run.log` — captured stdout from the importer.

## Rollback

```cypher
MATCH ()-[r {review_run:'bauteilboerse_actor_enrichment_import_2026_06_02'}]->()
DELETE r;
```
