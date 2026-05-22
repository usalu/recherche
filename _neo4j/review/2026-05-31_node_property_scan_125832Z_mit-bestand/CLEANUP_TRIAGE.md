# Node property cleanup triage

**Scan:** `2026-05-31_node_property_scan_125832Z_mit-bestand`  
**Database:** `mit-bestand`  
**Mode:** read-only scan, no graph writes

## What was scanned

- 39,550 live nodes / 81,130 live relationships.
- 65 labels with live nodes.
- 266 distinct node property keys.
- 1,157 label/property pairs.
- Full node property export: `nodes_properties.jsonl`.

## Highest-signal cleanup fronts

### 1. Diagnostic/meta-node explosion

`DataIssue` dominates the graph shape:

- 29,061 `DataIssue` nodes.
- 29,061 missing `name`.
- 5,907 missing `source_scope`.
- High-volume properties include `rel_type`, `start_id`, `end_id`, `rel_element_id`, `description`, `severity`, `status`.

First decision: keep these as graph-native review objects, move them out of the semantic graph, or normalize them into a smaller review/audit model.

### 2. Source-node normalization

The source layer is now much larger and more polymorphic than earlier plans assumed:

- 5,343 `Quelle` nodes.
- 5,026 `ExternalLink` nodes.
- 3,571 nodes labeled `Quelle` + `ExternalLink` missing `name`.
- 3,617 nodes labeled `Quelle` + `ExternalLink` missing `source_scope`.
- URL probe/cache properties are duplicated across `Quelle`, `ExternalLink`, `ResearchDocument`, and `SectionRef`.

Likely cleanup: decide whether `ExternalLink` remains a first-class node label or whether URL probe/cache state belongs in a dedicated source/probe node/property subset.

### 3. Legacy path references

There are 5,289 node-property values referencing retired or legacy paths. Main buckets:

- `first_seen_in_research`: 2,386 on `Quelle` + `ExternalLink`.
- `also_in_research`: 2,127 on `Quelle` + `ExternalLink`.
- `source_file`: 281 on `Quelle` + `ResearchDocument` / `Quelle` + `Dossier`.
- `candidate_source_urls`: 224 on `Akteur`, plus smaller counts on `Projekt`, `Bauteilgruppe`, `Programm`, `Bauwerk`, `Kennwert`.

Per AGENTS.md, these must be treated as legacy lineage hints, not authoritative sources.

### 4. Known legacy property keys

Known cleanup candidates from prior hygiene plans still exist:

- `Programm.usage_countries`: 11.
- `Programm.usage_project_count`: 11.
- `Programm.classified_at`: 6.
- `Norm.classified_at`, `Norm.scope`, `Norm.topic`, `Norm.not_yet_referenced_in_corpus`: 5 each.
- `Schadstoff.scope`, `Schadstoff.topic`: 3 each.
- `Leistungsanforderung.classified_at`: 3.
- `Leistungsanforderung.scope`, `Leistungsanforderung.topic`, `Leistungsanforderung.not_yet_referenced_in_corpus`: 2 each.
- `Akteur.akteur_kontext_text`: 1.

These are good candidates for the first low-risk patch, after value review.

### 5. Type drift

23 label/property pairs have mixed types. The most cleanup-relevant:

- `Akteur.source_scope`: mostly string, 5 lists.
- `Norm.source_scope`: mostly string, 1 list.
- `Bauteilgruppe.tragend`: 123 bool, 3 string.
- `Bauteilgruppe.direct_reuse_relevant`: 7 bool, 1 string.
- `Bauteilgruppe.menge_m2` and `Bauteilgruppe.menge_t`: int/float mixed.
- Several URL/list fields mix empty lists and string lists.

Normalize boolean/string drift before semantic cleanup, because it affects query predicates.

### 6. Missing core fields

- `id`: 0 missing.
- `name`: 32,903 missing.
- `source_scope`: 10,128 missing across all nodes.
- `source_scope`: 4,208 missing on source/case-bearing labels.

Do not blindly backfill `name` on every node. `DataIssue`, `Kennwert`, `DeprecatedType`, and combined `Quelle`/`ExternalLink` nodes likely need different naming rules.

## Suggested next patch order

1. Low-risk legacy-key removal/rename patch for the known small-count properties.
2. Type-drift patch for `source_scope`, `tragend`, `direct_reuse_relevant`, and numeric quantity fields.
3. Source-scope backfill rules by label/source-node family, with explicit legacy review status for `_archive` / `research` references.
4. Source-layer model decision: `Quelle` vs `ExternalLink` vs `ResearchDocument` / `SectionRef`.
5. `DataIssue` retention/compaction decision.

Every patch should start with a fresh backup and dry-run through `_scripts/apply_neo4j_review_patch.py`.
