# Final Cleanup F1 — Pending graph patches (rau merge + dry-run audit)

**Date:** 2026-06-06 · **Database:** `mit-bestand`  
**Agent:** F1 · **Plan:** [`VERIFICATION_PLAN_7_AGENTS_FINAL_CLEANUP.md`](../VERIFICATION_PLAN_7_AGENTS_FINAL_CLEANUP.md) § Agent F1  
**Ledger:** [`ledger/final_cleanup_f01.csv`](../ledger/final_cleanup_f01.csv) — **10 rows** (1 apply + 4 audit + 5 prune)  
**F4 prune export:** [`ledger/final_cleanup_f01_prune_for_f04.json`](../ledger/final_cleanup_f01_prune_for_f04.json)

## 1. Pre-apply verification

| Check | Result |
|---|---|
| `rau_architects` exists | yes — `:Akteur`, 4 incident rels, `primary_source_url` null |
| Survivor `rau` | `primary_source_url` = https://thomasrau.eu/en/initiatives/rau |
| `rau` vs `thomas_rau` | **distinct** (firm vs person) |
| `madaster` ↔ `rau` edges | **0** (not auto-merged; per REMEDIATION_PLAN escalation) |
| harvestmap VMA | untouched — `re_store_harvestmap_vienna` → `peter_kneidinger` still `evidence_url` null |

## 2. Patch apply

**Patch:** [`patches/post_quality_p06_03.patch.jsonl`](../patches/post_quality_p06_03.patch.jsonl)

```json
{"op": "merge_node", "from": "rau_architects", "to": "rau", "reason": "P6-03 P6-03-RAU-001: PROVEN duplicate firm — RAU Architects on Liander HQ = architectural firm RAU (thomasrau.eu/en/initiatives/rau)"}
```

| Step | Command | Outcome |
|---|---|---|
| Dry-run | `python _scripts/apply_neo4j_review_patch.py --patch …/post_quality_p06_03.patch.jsonl` | `would_merge` 1; expected 2263 nodes / 15063 rels |
| Live apply | `… --confirm "APPLY post_quality_p06_03.patch.jsonl TO mit-bestand"` | **applied**; `dry_run: false` in apply report |

**Apply report:** [`apply_reports/post_quality_p06_03.patch.apply_report.json`](../apply_reports/post_quality_p06_03.patch.apply_report.json)

### Post-apply live counts

| Metric | Before | After (plan) | After (actual) |
|---|---:|---:|---:|
| Nodes | 2,264 | 2,263 | **2,263** |
| Relationships | 15,063 | 15,063 | **15,060** |
| Σ elements | 17,327 | 17,326 | **17,323** |

**Δ rels (−3):** merge redirected 4 outbound rels from `rau_architects`, but 3 were parallel duplicates already present on survivor `rau` (`HAT_AKTEURROLLE` → `ar_entwurf_planung`, `HAT_AKTEURROLLE` → `ar_reuse_zirkularitaetsberatung`, `HAT_AKTEURTYP` → `at_unternehmen`). Only `BETEILIGT_AN` → `p_liander_alliander_hq_duiven` survived as a new live edge (new `elementId`).

**Survivor node:** `rau` — `elementId` `4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:6715`, `aliases` includes `"RAU Architects"`.

## 3. P6 dry-run audit (D6)

Scanned **26** `apply_reports/*.json` files.

| Patch family | Files | `dry_run: true` |
|---|---|---|
| `post_quality_p06_02` | 1 | **no** (`false`) |
| `post_quality_p06_03` | 1 | **no** (was `true` pre-F1; now applied) |
| `post_quality_p06_04` | 1 | **no** (`false`) |
| All other apply reports | 23 | **no** |

**Verdict:** zero `dry_run: true` leftovers in `apply_reports/` — D6 satisfied for this wave.

## 4. F4 prune list (`rau_architects`)

**5 stale rows** in `VERIFICATION_LEDGER_ELEMENT.csv` reference `rau_architects` (plan cited ~14 including historical agent ledgers; canonical element ledger = 5).

| claim_id | kind | stale `element_id` | prune reason |
|---|---|---|---|
| `AKT-node-357` | node | `4:…:5405` | merged node deleted |
| `09-beteiligt_an-0690` | rel | `5:…:1153022659676607773` | redirected → `5:…:1153022659676609083` |
| `EP01-rel-01039` | rel | `5:…:7018962273838307334` | deduped on survivor |
| `EP01-rel-01040` | rel | `5:…:1157527358815606045` | deduped on survivor |
| `EP02-rel-00500` | rel | `5:…:1153024858699863325` | deduped on survivor |

Machine-readable export for Agent **F4** re-merge: [`ledger/final_cleanup_f01_prune_for_f04.json`](../ledger/final_cleanup_f01_prune_for_f04.json).

## 5. Out of scope (confirmed untouched)

- `madaster` ↔ `rau` consolidation — **not** applied (human escalation).
- `re_store_harvestmap_vienna` → `peter_kneidinger` `VERBUNDEN_MIT_AKTEUR` — **not** patched (F3 owner).

## 6. Handoff

- **F4:** prune 5 stale `element_id` keys + re-baseline element count to **17,323** (not 17,326).
- **F5/F6:** use post-F1 headline **2,263 / 15,060** until F7 final proof.
- **F7:** recompute PROVEN% after F4 merge.
