# Phase 38 Final Manual Decision Readiness

## Status

All 27 manual-review nodes now have preparation material.

No final manual decisions have been written.

```text
manual decision template: 27 TODO
validation issues: 0
remaining edge-proposal work: 0
remaining content-proposal work: 0
```

## Decision Template

Use this file only in the final decision pass:

```text
_migration/25_manual_review_decision_template.csv
```

## Proposal Packages

### First Batch

Highest-impact broad/wrong-level nodes:

```text
_migration/28_material_metall_edge_review_decisions.csv
_migration/29_huerde_performance_nachweis_edge_review_decisions.csv
_migration/30_bauteiltyp_tragstruktur_edge_review_decisions.csv
_migration/31_bauteiltyp_bauwerksteil_edge_review_decisions.csv
_migration/32_huerde_logistikproblem_edge_review_decisions.csv
```

Summary:

```text
_migration/33_First_Manual_Batch_Decision_Summary.md
```

### Second Batch

Component-scope review nodes:

```text
_migration/34_second_manual_batch_edge_proposals.csv
_migration/34_Second_Manual_Batch_Proposals.md
```

### Third Batch

Remaining edge-impact nodes:

```text
_migration/36_third_manual_batch_edge_proposals.csv
_migration/36_Third_Manual_Batch_Proposals.md
```

### Content-Only Batch

Nodes with no held edges, but semantic cleanup needed:

```text
_migration/37_content_only_review_proposals.csv
_migration/37_Content_Only_Review_Proposals.md
```

## Tracking

Preparation status:

```text
_migration/35_manual_review_preparation_status.csv
_migration/35_Manual_Review_Preparation_Status.md
```

Decision validation:

```text
_migration/27_Manual_Decision_Validation_Report.md
```

## Final Decision Rule

Only after reviewing the proposal packages should rows in `_migration/25_manual_review_decision_template.csv` be changed from `TODO` to:

```text
approve_move
approve_split
merge_into_existing
keep_review
delete_from_final
```

After final decisions are entered, run:

```text
_migration/validate_phase27_manual_decisions.ps1
```

Then apply approved decisions in a separate migration step.
