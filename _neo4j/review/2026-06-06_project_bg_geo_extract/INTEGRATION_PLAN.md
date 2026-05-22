# Geo import integration plan — `mit-bestand`

**Run:** `2026-06-06_project_bg_geo_extract`  
**Source:** [`reuse_geo_graph.json`](reuse_geo_graph.json)

## Property model

| Label | Properties |
|---|---|
| `:Projekt` | `adresse`, `latitude`, `longitude`, `geo_confidence`, `geo_import_run`, `geo_aktualisiert_am_utc`, `metadata_sidecar_key` |
| `:Bauwerk` | same as Projekt |
| `:Stadt` | `latitude`, `longitude`, `geo_import_run`, `geo_aktualisiert_am_utc` |

Evidence detail (status, non-HTTP sources) → [`sidecar/geo_evidence.jsonl`](sidecar/geo_evidence.jsonl).

## Phases

1. `phase1_projekte_geo.patch.jsonl` — 83 receiver sites
2. `phase2_bauwerke_geo.patch.jsonl` — 163 Bauwerke (donor + receiver)
3. `phase3_staedte_geo.patch.jsonl` — 73 city centroids
4. `phase4_new_donor_bauwerke.patch.jsonl` — evidence-gated new donors ([`NEW_DONOR_CANDIDATES.csv`](NEW_DONOR_CANDIDATES.csv))

## Apply

```bash
python _neo4j/review/2026-06-06_project_bg_geo_extract/_pre_apply_check.py
python _neo4j/review/2026-06-06_project_bg_geo_extract/_generate_geo_import_patches.py
python _neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py
python _neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py --commit
```

## Acceptance

- Projekte with `adresse` ≥ 80
- Bauwerke with `adresse` ≥ 160
- Stadt with `latitude` ≥ 70
- Node/rel counts unchanged for phases 1–3
- Phase 4 only when `NEW_DONOR_CANDIDATES.csv` row has `status=accepted`
