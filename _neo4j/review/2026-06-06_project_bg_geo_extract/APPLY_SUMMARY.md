# Geo import apply summary — `mit-bestand`

**Run:** `2026-06-06_project_bg_geo_extract`  
**Applied:** 2026-06-05 (UTC)  
**Database:** `mit-bestand`

## Phases applied

| Phase | Records | Result |
|---|---:|---|
| phase1_projekte_geo | 83 | 83 Projekt nodes updated |
| phase2_bauwerke_geo | 163 | 163 Bauwerk nodes updated |
| phase3_staedte_geo | 73 | 73 Stadt centroids |
| phase4_new_donor_bauwerke | 0 | skipped (no `status=accepted` in NEW_DONOR_CANDIDATES.csv) |

## Graph integrity

| Metric | Before | After |
|---|---:|---:|
| Nodes | 2 304 | 2 304 |
| Relationships | 15 527 | 15 527 |

No structural changes (property-only import).

## Coverage after apply

| Check | Count |
|---|---:|
| `:Projekt` with `adresse` | 83 |
| `:Bauwerk` with `adresse` | 163 |
| `:Stadt` with `latitude` | 73 |
| `:Projekt` with `geo_confidence = low` | 8 |

Low-confidence projects: `p_association_house_groeditz`, `p_berlin_schildow_pilot_house`, `p_big_dig_building_boston`, `p_broethen_twin_house_hoyerswerda`, `p_gjg_house_gentbrugge`, `p_haus_hos_mehrfamilienhaus_muehlhausen`, `p_juch_areal_recyclingzentrum_zuerich`, `p_mehrow_pilot_house`.

## Sample chain verification (SUPERLOCAL)

- Donor `bw_hochhausflat_ursulastraat`: Ursulastraat, Bleijerheide, 6464 Kerkrade (50.8530, 6.0666)
- Receiver `p_superlocal_expogebouw_bleijerheide`: Voorterstraat, Bleijerheide, 6462 Kerkrade (50.8534, 6.0618)

## Deferred

- **Phase 4 new donors:** see [`NEW_DONOR_CANDIDATES.csv`](NEW_DONOR_CANDIDATES.csv) — 2 rejected, 2 pending (RE-WIN multi-warehouse, TULIUM orphan BG).
- **Baseline note:** live graph is 2 304 / 15 527 (post-regulation intakes); differs from FINAL_AUDIT 2 273 / 15 118.
- **Stadt:** 1 of 74 geocoded cities not in graph (`staedte_geocoded.json` has 74; 73 applied).

## Artifacts

- Rollback snapshot: [`geo_import_before.json`](geo_import_before.json) (empty — first geo import)
- Sidecar evidence: [`sidecar/geo_evidence.jsonl`](sidecar/geo_evidence.jsonl) (246 rows)
- Apply reports: [`apply_reports/`](apply_reports/)
- Machine report: [`apply_summary.json`](apply_summary.json)

## Rebuild / re-apply

```bash
python _neo4j/review/2026-06-06_project_bg_geo_extract/_pre_apply_check.py
python _neo4j/review/2026-06-06_project_bg_geo_extract/_generate_geo_import_patches.py
python _neo4j/review/2026-06-06_project_bg_geo_extract/apply_geo_import.py --commit
```
