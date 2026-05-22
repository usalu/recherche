# Bauteilbörsen Graph Integration Report

Date: 2026-05-28

## Applied Patch

Patch:

- `patches/bauteilboersen_integration_graph_only.patch.jsonl`

Apply report:

- `apply_reports/bauteilboersen_integration_graph_only.patch.apply_report.json`
- `apply_reports/bauteilboersen_integration_graph_only.patch.apply_report.md`

Backup before apply:

- `_neo4j/review/backups/2026-05-28_pre_bauteilboersen_integration`

## Scope Applied

Imported the reviewed Bauteilbörsen archive content as graph-first facts only.

Rules followed:

- No long archive section text properties on semantic nodes.
- `BELEGT_IN` uses URL source nodes extracted directly from the `.md` files.
- No new `HAS_DATA_ISSUE`.
- No new `ANCHORED_BY`.
- No new `BETEILIGT_AN`.
- No new `ZITIERT_QUELLE`.
- Network/operator links only to already existing graph actors.
- No new project participation links.

## Graph Delta

Before:

- Nodes: 39,517
- Relationships: 80,675

After:

- Nodes: 39,548
- Relationships: 81,064

Net change:

- +31 nodes
- +389 relationships

## Created Nodes

31 new `Akteur` nodes were created for archive profiles/platforms that did not already have semantic anchors.

Existing semantic anchors were reused for:

- `baukarussell`
- `bauteilboerse_bremen`
- `bauteilladen_winterthur`
- `bauteilnetz_deutschland`
- `gebruiktebouwmaterialen`
- `new_horizon`
- `rotordc`
- `software_restado`
- `concular`
- `salvo_ltd`
- `materialnomaden`

## Created Relationships

Created relationships carrying `review_run = "2026-05-28_bauteilboersen_integration"`:

- `BELEGT_IN`: 136
- `BETRIEBEN_VON`: 3
- `GEHÖRT_ZU`: 34
- `HAT_AKTEURROLLE`: 147
- `HAT_AKTEURTYP`: 35
- `LIEGT_IN_LAND`: 34

The patch also attempted existing-safe relations; 31 were already present and remained unchanged.

## Evidence Verification

All 39 archive profiles were verified after apply.

- Missing direct URL `BELEGT_IN`: 0
- Profiles without country link: 0
- New forbidden relationship types from this run: 0
- New `ZITIERT_QUELLE` from this run: 0

Verification file:

- `post_apply_verification.json`

## Notes

The global gap survey still reports pre-existing broad repository issues, such as nodes missing `source_scope`, relation ids missing, and old Bauteilgruppe gaps. These counts were already present before this Bauteilbörsen integration and were not introduced by this patch.
