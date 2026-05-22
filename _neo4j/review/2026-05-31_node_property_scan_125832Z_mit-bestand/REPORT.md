# Node property scan

**Created UTC:** 2026-05-31T12:58:50.145291+00:00
**Database:** `mit-bestand`
**Connection:** `bolt://localhost:7687` as `neo4j`
**Graph counts:** 39550 nodes / 81130 relationships

## Outputs

| File | Purpose |
|---|---|
| `nodes_properties.jsonl` | Every node with labels, id/name, property keys, and full property bag. |
| `property_inventory.csv` | Per-label property coverage, types, samples, and flags. |
| `property_key_summary.csv` | Graph-wide property-key frequency and label distribution. |
| `node_property_issues.jsonl` / `.csv` | Review queue for cleanup candidates. |
| `label_summary.csv` | Labels, node counts, and property-key sets. |
| `value_samples.json` | Long text, type drift, and known legacy key slices. |

## Headline counts

- Labels: 65
- Distinct node property keys: 266
- Label/property pairs: 1157
- Issue rows: 62219
- Missing `id`: 0
- Missing `name`: 32903
- Missing `source_scope` on any label: 10128
- Missing `source_scope` on case/source-bearing labels: 4208
- Label/property type drift pairs: 23
- Known legacy label/property pairs: 14

## Issue categories

| Category | Count |
|---|---:|
| `missing_name` | 32903 |
| `missing_source_scope` | 10128 |
| `blank_list_property` | 5621 |
| `legacy_path_reference` | 5289 |
| `missing_source_scope_case_label` | 4208 |
| `long_text_property` | 3512 |
| `url_in_non_url_property` | 471 |
| `known_legacy_property` | 64 |
| `property_type_drift` | 23 |

## Severity

| Severity | Count |
|---|---:|
| `high` | 9497 |
| `low` | 9133 |
| `medium` | 43589 |

## Largest labels

| Label | Nodes | Distinct props |
|---|---:|---:|
| `DataIssue` | 29061 | 31 |
| `Quelle` | 5343 | 86 |
| `ExternalLink` | 5026 | 61 |
| `DossierEntityTarget` | 2591 | 14 |
| `Akteur` | 679 | 40 |
| `SectionRef` | 641 | 41 |
| `ResearchDocument` | 403 | 59 |
| `Bauteilgruppe` | 369 | 40 |
| `Kennwert` | 258 | 34 |
| `Bauwerk` | 186 | 27 |
| `PruefungNachweis` | 120 | 22 |
| `Norm` | 103 | 34 |
| `Projekt` | 101 | 46 |
| `Dossier` | 100 | 35 |
| `Stadt` | 76 | 4 |
| `Aufbereitungsverfahren` | 62 | 16 |
| `Leistungsanforderung` | 46 | 21 |
| `Programm` | 29 | 68 |
| `Huerde` | 28 | 9 |
| `Material` | 26 | 22 |
| `Akteurrolle` | 24 | 7 |
| `Bauteiltyp` | 23 | 19 |
| `Materialdepot` | 23 | 22 |
| `ReuseRule` | 20 | 36 |
| `Software` | 19 | 20 |

## Most common property keys

| Property | Nodes | Labels | Flags |
|---|---:|---:|---|
| `id` | 39550 | 65 | core |
| `migration_origin` | 35118 | 62 |  |
| `source_scope` | 29422 | 64 | core; provenance_key |
| `kind` | 29102 | 5 |  |
| `severity` | 29061 | 1 |  |
| `status` | 28151 | 3 |  |
| `review_status` | 27884 | 27 |  |
| `source_trace_migration` | 26793 | 19 | provenance_key |
| `evidence_origin` | 24684 | 12 | provenance_key |
| `evidence_source_id` | 24588 | 9 | provenance_key |
| `created_at` | 23356 | 3 |  |
| `description` | 23154 | 1 |  |
| `rel_type` | 22297 | 1 |  |
| `end_id` | 21046 | 1 |  |
| `start_id` | 21046 | 1 |  |
| `rel_element_id` | 21043 | 1 |  |
| `ref_id` | 6969 | 1 |  |
| `name` | 6647 | 62 | core |
| `url` | 5655 | 5 | provenance_key |
| `candidate_source_count` | 5458 | 22 | provenance_key |
| `quelltyp` | 5345 | 6 |  |
| `extracted_at` | 5026 | 4 |  |
| `url_origin` | 5026 | 4 | provenance_key |
| `found_at` | 4986 | 1 |  |
| `found_by` | 4986 | 1 |  |

## Read this before cleanup

- This scan is read-only and does not decide semantic merges.
- `known_legacy_review` means the key has appeared in old cleanup plans or legacy imports; inspect value samples before removal.
- `possible_quelle_denormalization` is a review cue only. Actual provenance should remain traceable through `Quelle`, `BELEGT_IN`, and relationship provenance.
- Any patch should be generated separately, dry-run with `_scripts/apply_neo4j_review_patch.py`, backed up first, and reviewed by label/key slice.
