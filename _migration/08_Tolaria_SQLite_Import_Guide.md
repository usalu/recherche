# Tolaria / SQLite Import Guide

## Current Migration State

- Staged graph root: `_graph`
- Legacy coverage: `567 / 567` mapped Markdown files covered
- Missing legacy files after migration: `0`
- Confirmed graph edges: `7,923`
- Current review queue: `642`
- Confirmed edge CSV: `_migration/phase6_graph_edges.csv`
- Review queue CSV: `_migration/phase6_label_resolution_review.csv`
- Promoted recurring vocabulary knots: `_migration/phase7_promoted_review_knots.csv`
- Promoted repeated actors: `_migration/phase8_promoted_repeated_actors.csv`
- Actor role vocabulary: `_migration/phase9_actor_roles.csv`
- Hurdle and boundary vocabulary: `_migration/phase10_huerde_abgrenzung_nodes.csv`
- Metric vocabulary gaps: `_migration/phase11_kennwertdefinition_gaps.csv`
- Component-type vocabulary gaps: `_migration/phase12_bauteiltyp_gaps.csv`
- Encoding repair log: `_migration/phase13_encoding_repair.csv`
- Entity counts: `_migration/final_graph_entity_counts.csv`

The old folders were not moved or deleted. `_graph` is the new import-ready staging structure.

## Recommended Import Order

1. Import nodes from `_graph/**/index.md`.
   - Entity = first folder after `_graph`
   - ID = folder name below entity
   - Node metadata = YAML frontmatter
   - Full text = Markdown body

2. Import confirmed edges from `_migration/phase6_graph_edges.csv`.
   - Use only rows from this file for automatic graph edges.
   - Keep `confidence` and `resolution_rule` as edge properties.
   - Keep `raw_label` and `field` for traceability.
   - Important relations now include:
     - `has_bauteiltyp`
     - `uses_material`
     - `has_huerde`
     - `has_bewertungslogik_abgrenzung`
     - `has_pruefung_nachweis`
     - `references_norm`
     - `has_leistungsanforderung`
     - `measures_kennwertdefinition`
     - `involves_akteur`
     - `has_akteurrolle`

3. Import review items from `_migration/phase6_label_resolution_review.csv` into a separate review table.
   - Do not treat these as confirmed edges yet.
   - Review buckets with high value:
     - `akteur`: split multi-actor strings and decide which remaining one-off actors become canonical nodes.
     - `huerde`: decide whether remaining case-specific barriers deserve new hurdle knots.
     - `kennwertdefinition`: decide whether remaining project metrics deserve controlled metrics.
     - `material`: split mixed material labels and decide whether special materials deserve nodes.
     - `pruefung_nachweis`: normalize remaining testing/evidence terms.
     - `norm_or_leistungsanforderung`: separate true standards from performance requirements.
     - `bauteiltyp`: remaining rows are mostly raw materials, special resources, connection hardware, or generic notes; avoid promoting them blindly.

4. Preserve source traceability.
   - Every migrated node contains legacy paths in frontmatter or copied source files under `DATEIEN`.
   - Every generated edge keeps `legacy_path` when available.

## Suggested SQLite Tables

```sql
CREATE TABLE nodes (
  entity TEXT NOT NULL,
  id TEXT NOT NULL,
  title TEXT,
  node_kind TEXT,
  migration_status TEXT,
  markdown_path TEXT NOT NULL,
  markdown_body TEXT,
  frontmatter_json TEXT,
  PRIMARY KEY (entity, id)
);

CREATE TABLE edges (
  source_entity TEXT NOT NULL,
  source_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  target_entity TEXT NOT NULL,
  target_id TEXT NOT NULL,
  field TEXT,
  raw_label TEXT,
  confidence TEXT,
  resolution_rule TEXT,
  legacy_path TEXT
);

CREATE TABLE label_review (
  source_entity TEXT,
  source_id TEXT,
  field TEXT,
  raw_label TEXT,
  suggested_entity TEXT,
  reason TEXT,
  legacy_path TEXT
);
```

## Import Rules

- Treat `phase6_graph_edges.csv` as confirmed machine-generated links.
- Treat `phase6_label_resolution_review.csv` as human-review material.
- Do not merge `akteur_beteiligung` into `akteur` until actor review is done.
- Do not treat `quelle` and `meta` as domain facts; they are preservation/source nodes.
- Do not treat `bewertungslogik_abgrenzung` as a project hurdle. It records scoring/boundary logic, such as "not Direct Reuse" or "future DfD only".
- `bauteilboerse` content is represented as `software_digitaltool` plus platform-related knots (`tooltyp`, `beschaffungsweg`, `ressourcenquelle`) rather than as a standalone domain entity.
- For analysis, center the graph on `reuse_einsatz`, then expand to `fallstudie`, `projekt`, `bauobjekt`, `material`, `bauteiltyp`, `huerde`, `pruefung_nachweis`, `norm`, and `kennwertdefinition`.
- Encoding note: `_migration/repair_phase13_encoding_mojibake.ps1` has already repaired generated mojibake in `_graph`. If older vocabulary scripts are rerun, run the repair script again before import.

## Current Edge Snapshot

- `has_bauteiltyp`: 848
- `uses_material`: 592
- `has_huerde`: 444
- `has_bewertungslogik_abgrenzung`: 151
- `measures_kennwertdefinition`: 612
- `has_pruefung_nachweis`: 48
- `references_norm`: 9
- `has_leistungsanforderung`: 3
- `involves_akteur`: 44
- `has_akteurrolle`: 298

## Next Clean-Up Pass

The next best semantic pass is actor and evidence review:

- Split multi-actor labels.
- Link `akteur_beteiligung` rows to canonical `akteur` nodes.
- Promote one-off but important actors if they are analytically relevant.
- Keep unresolved one-off labels as review rows unless they affect a core reuse chain.
- Then normalize the remaining `huerde`, `kennwertdefinition`, `pruefung_nachweis`, and `norm_or_leistungsanforderung` review buckets.
