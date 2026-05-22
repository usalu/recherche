# Evidence URL Location Audit

**Date:** 2026-06-06  
**Database:** `mit-bestand`  
**Purpose:** locate where URL evidence currently lives after the evidence/property cleanups, before launching the full proof campaign.

## Immediate correction

The live graph does **not** have only 72 evidence-bearing relationships. That was an undercount caused by checking only the newer reuse-bubble property names:

- `evidence_url` / `evidence_quote` / `evidence_confidence`

The older canonical property model still uses:

- `source_url` / `source_quote` / `confidence`

Current live counts:

| Surface | Count |
|---|---:|
| Relationships total | 15,457 |
| Relationships with `source_url` | 3,691 |
| Relationships with `evidence_url` | 72 |
| Relationships with either URL field | 3,763 |
| Nodes total | 2,304 |
| Nodes with `source_urls` | 544 |
| Nodes with `primary_source_url` | 54 |
| Nodes with singleton `source_url` | 13 |
| Nodes with `source_titles` | 1,001 |

So much more evidence is still present in the graph than the narrow `evidence_url` scan suggested.

## Where evidence is hiding

### 1. Live Neo4j relationship properties

Main live relationship evidence is under `source_url`, not `evidence_url`.

`source_url` is concentrated in the regulation / process layer:

| Relationship type | `source_url` rels |
|---|---:|
| `ERFORDERT_NACHWEIS` | 1,578 |
| `TRIGGERS_REGULIERUNGSFRAGE` | 1,130 |
| `GILT_IN_LAND` | 281 |
| `HAT_HUERDE` | 237 |
| `GESTUETZT_AUF_REGELWERK` | 167 |
| `ERFUELLT_NACHWEIS` | 118 |
| `HAT_SCHADSTOFFRISIKO` | 100 |
| `ERFORDERT_SCHADSTOFFPRUEFUNG` | 37 |
| `TYPISCH_BEI_MATERIAL` | 18 |
| `TYPISCH_BEI_ERA` | 15 |
| `TYPISCH_BEI_BAUTEILTYP` | 10 |

Reuse-bubble and cross-bubble edges use `evidence_url` instead. There is no overlap: relationships do not currently carry both `source_url` and `evidence_url`.

### 2. Live Neo4j node properties

Node evidence is mostly under:

- `source_urls` on 544 nodes.
- `primary_source_url` on 54 nodes.
- singleton `source_url` on 13 nodes.
- `source_titles` on 1,001 nodes, mostly UI/provenance titles rather than proof URLs.

Important implication: verification agents must query **all** of these fields, not just `primary_source_url`.

### 3. Reuse-bubble cleanup artifacts

`_neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/`

Important files:

- `CLEANUP_SUMMARY.md`
- `audit_report.json`
- `evidence_property_audit.json`
- `evidence_property_fix_report.json`
- `patches/bubble_node_source_urls.patch.jsonl`
- `patches/bubble_hub_node_urls.patch.jsonl`
- `patches/bubble_url_corrections.patch.jsonl`
- apply reports for those patches

This cleanup removed `:Quelle` URL nodes and `BELEGT_IN` edges, but states that URLs were merged onto node/relationship properties. `audit_report.json` still contains the former `q_url_*` and named source URLs, including Cirkla, Zirkular, Restado, Opalis, etc.

### 4. Old `ZITIERT_QUELLE` trace run

`_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/`

Important files:

- `reports/zitiert_quelle_trace_report.md`
- `reports/zitiert_quelle_trace_report.json`
- `reports/strict_source_url_binding_cleanup.json`
- `reports/strict_invalid_url_cleanup.json`
- `logs/zitiert_quelle_edge_inventory.jsonl`
- `logs/zitiert_quelle_resolution_ledger.jsonl`
- `logs/information_source_url_ledger.jsonl`
- `logs/source_url_unresolved_review.jsonl`
- `logs/strict_candidate_source_url_review.jsonl`
- `logs/strict_invalid_source_url_review.jsonl`

Key historical numbers from the reports:

- 8,229 legacy `:ZITIERT_QUELLE` rows were resolved/deleted.
- 12,841 trusted relationship URL bindings remained after invalid cleanup at that stage.
- 3,693 candidate relationship URL sets were demoted because they were too broad.
- 1,765 nodes had candidate source sets needing review.
- 1,809 nodes were marked as lacking trusted source URL.

These logs are the main place to recover older candidate/trusted source bindings that are not visible as current `evidence_url`.

### 5. Property cleanup sidecar

`_neo4j/review/2026-06-05_post_migration_property_cleanup/sidecar/`

Important files:

- `entity_metadata.jsonl`
- `manifest.json`
- `qa/needs_source_url_review.csv`

The sidecar contains 615 relationship metadata rows and 607 node metadata rows. It does **not** generally hold trusted URL evidence for the first sampled rows; many rows preserve review metadata such as `review_status: needs_source_url_review` while `source_url` remained null. But the QA file is important: it lists 353 relationship claims that explicitly still need source URL review.

### 6. Project / geo evidence sidecar

`_neo4j/review/2026-06-06_project_bg_geo_extract/sidecar/geo_evidence.jsonl`

This stores geo/address evidence for projects and buildings. Many rows contain useful `source_url` values, but some use placeholders like `processed`, `archive`, `processed+archive`, or empty strings. Those are not proof URLs and need review before being treated as evidence.

### 7. Bauteilbörsen final verified evidence package

`_neo4j/intake/inbox/research/bauteilboersen_finalest_verified_reuse_evidence_2026-05-31/`

Important files:

- `README.md`
- `csv/FINAL_IMPORT_SAFE_MATERIAL_BAUTEILTYP_CLAIMS.csv`
- `csv/FINAL_ACTOR_STATUS_AND_COVERAGE.csv`
- `csv/FINAL_EVIDENCE_LEDGER_ALL_ROWS.csv`
- `json_per_actor/*.finalest.evidence.json`

This is a high-quality strict evidence package: 39 actors, 150 strict import-safe rows, 235 review-only rows, and no actor with zero captured evidence. Example: `software_restado.finalest.evidence.json` contains direct product-detail URLs and quotes for `HAT_BAUTEILTYP` / `NUTZT_MATERIAL` claims.

### 8. Bauteilbörsen enrichment packages

Important directories:

- `_neo4j/intake/inbox/research/bauteilboersen_deep_enrichment_results/`
- `_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/`
- `_neo4j/intake/inbox/research/bauteilboersen_evidence_continuation_3_2026-05-31/`

These contain many `*.enrichment.json` and `*.enrichment_delta.json` files with `sources_visited`, `evidence_urls`, `evidence_quote`, and status fields. They are not automatically graph-safe, but they are the main raw evidence reservoirs for actor/material/component claims.

### 9. Country reuse bubble evidence dossiers

Important files under `_neo4j/intake/runs/2026-06-05_*_reuse_bubble/`:

- `EVIDENCE_REGISTER.csv`
- `EVIDENCE_REGISTER_SUPPLEMENT.csv`
- `EVIDENCE_DEEP_RESEARCH.md`
- `EVIDENCE_DEEP_DIVE.md`
- `INTERNET_RESEARCH_SUPPLEMENT.md`
- `DEFERRED_NO_EVIDENCE.md`
- `patches/phase1c_evidence_hardening.patch.jsonl`
- `patches/*.bak`

These often contain stronger evidence than the final graph edge does, plus explicit warnings about weak/overclaimed edges. Germany's `EVIDENCE_DEEP_RESEARCH.md` is especially important because it already identified some weak inferred edges before the later cross-bubble audit.

### 10. Git history

Git history around evidence fields exists in commits:

- `d37e5240` — Source Hunting
- `e9d7f605` — Source check
- `28cf3919` — Source check 2
- `6f183784` — Source check 3
- `bd62286a` — source check 4
- `f9cf1a8c` — updates
- `4ad31276`, `7da6d3ec`, `323cd19b`, `ed1d81d9`

Searches with `git log -Ssource_url -- _neo4j` and `git log -Sevidence_url -- _neo4j` show evidence-field churn in these commits. A deleted-file pathspec check for evidence/source/url/quelle-named files found no obvious deleted evidence files under `_neo4j`; the evidence appears to have been remodeled, not removed from git.

## Consequences for the 15-agent verification plan

The plan must be amended before execution:

1. Agent evidence queries must treat `source_url`, `evidence_url`, node `source_urls`, node `primary_source_url`, and node singleton `source_url` as evidence-bearing fields.
2. The high-risk web-evidence surface is not ~72 relationships; it is at least **3,763 URL-bearing relationships** plus **544 source-url nodes**.
3. The 3,691 `source_url` relationships are mostly regulation/process claims and need a different verification protocol from the 72 reuse-bubble `evidence_url` edges.
4. The 3,693 demoted candidate URL sets from the old trace run must not be trusted automatically. They are a recovery queue only.
5. `needs_source_url_review.csv` and `strict_candidate_source_url_review.jsonl` should become explicit work queues for missing/weak evidence.

## Priority recovery order

1. **Normalize live graph evidence inventory**: export all current URL-bearing nodes/rels across all URL fields.
2. **Reconcile with old trace ledgers**: match current `rel.id` or `(type, from_id, to_id)` to the 2026-05-23 trusted/candidate ledgers.
3. **Recover strict bauteilboersen evidence** from `finalest.evidence.json` and strict CSVs for actor/material/component claims.
4. **Use country-bubble evidence registers** to fill missing node `source_urls` and relationship `evidence_url` where already verified.
5. **Use sidecars only as review queues** unless they contain real URL + quote fields.
6. **Do not import candidate URL sets** without fresh endpoint-level verification.
