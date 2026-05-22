# Post-IER Verification — W2 Follow-Up Wave (5 Agents)

**Status:** EXECUTING  
**Date:** 2026-06-07  
**Database:** `mit-bestand` (**2,263 nodes / 14,846 rels** post-IER)  
**Prior ledger:** `VERIFICATION_LEDGER_ELEMENT_v3.csv` — **17,109 rows** · **93.31% PROVEN**  
**Runner:** [`_post_ier_w2_wave_run.py`](_post_ier_w2_wave_run.py)

---

## 0. Why W2 exists

POST wave (POST-01…POST-06) drafted patches and partial ledger overlays. Five surfaces remain open:

| Gap | Count (v3 / live) | Owner | W2 action |
|---|---:|---|---|
| Catalogue rels without `evidence_quote` | **1,062** remainder (200 done) | W2-01 | Next **300** @ offset 200; strict Q04 gate |
| `MISSING_EVIDENCE` residual | **215** in v3 | W2-02 | Apply `post_04_missing_evidence.patch.jsonl`; web-search remainder |
| `CONTRADICTION` geo | **42** | W2-03 | Apply `post_03_geo_fixes.patch.jsonl` (human-gated); re-adjudicate remainder |
| `PARTIAL` + VMA weak edges | **334** PARTIAL | W2-04 | Second pass; DELETE/upgrade patches POST-05 missed |
| `SCHEMA_VIOLATION` tier-D | **33** (20 patch ops) | W2-05 | Apply `post_02_schema_violation.patch.jsonl`; merge → v4 |

**Do not apply** `post_01_catalogue_backfill.patch.jsonl` (164/200 UNSUPPORTED under strict gate).

---

## 1. Definition of Done

| # | Criterion |
|---|---|
| **D1** | Each agent emits `ledger/w2_0N.csv` + `reports/w2_0N_report.md`. |
| **D2** | Patches dry-run before apply; graph counts recorded before/after each apply. |
| **D3** | `PROVEN` requires verbatim `proof_quote` (Evidence Gate). |
| **D4** | W2-05 publishes `VERIFICATION_LEDGER_ELEMENT_v4.csv` + `reports/POST_IER_W2_REPORT.md`. |
| **D5** | Apply failures stop that agent and are documented. |

---

## 2. Agent scopes

### W2-01 — Catalogue backfill continuation

- **Scope:** Live `HAT_BAUTEILTYP` / `NUTZT_MATERIAL` where `evidence_quote` empty; **SKIP 200 LIMIT 300**.
- **Method:** Q04 strict gate (same as POST-01); patch only `UPGRADE` with verbatim quote.
- **Outputs:** `ledger/w2_01.csv`, `reports/w2_01_report.md`, `patches/w2_01_catalogue_backfill.patch.jsonl` (dry-run)

### W2-02 — POST-04 apply + MISSING residual

- **Scope:** Apply existing `post_04_missing_evidence.patch.jsonl` (105 node-source ops); then v3 `MISSING_EVIDENCE` rows not upgraded by patch.
- **Method:** Dry-run → apply if clean; HTTP fetch for remainder.
- **Outputs:** `ledger/w2_02.csv`, `reports/w2_02_report.md`, optional `patches/w2_02_missing_evidence.patch.jsonl`

### W2-03 — Geo CONTRADICTION fixes

- **Scope:** Apply `post_03_geo_fixes.patch.jsonl` (56 ops); re-adjudicate remaining `CONTRADICTION` rows.
- **Method:** Dry-run → apply if clean; ledger overlay for unresolved geo.
- **Outputs:** `ledger/w2_03.csv`, `reports/w2_03_report.md`

### W2-04 — PARTIAL + weak VMA edges

- **Scope:** All v3 `PARTIAL` rows; VMA category-inference weak links.
- **Method:** Re-adjudicate; emit `delete_rel` for unsupported VMA; upgrade attempts on live URLs.
- **Outputs:** `ledger/w2_04.csv`, `reports/w2_04_report.md`, `patches/w2_04_partial_vma.patch.jsonl`

### W2-05 — Schema tier-D + aggregator

- **Scope:** Apply `post_02_schema_violation.patch.jsonl` (20 ops); merge W2-01…04 overlays on v3 → v4.
- **Method:** Dry-run → apply if clean; prune stale keys; recompute PROVEN%.
- **Outputs:** `ledger/w2_05.csv`, `VERIFICATION_LEDGER_ELEMENT_v4.csv`, `reports/w2_05_report.md`, `reports/POST_IER_W2_REPORT.md`

---

## 3. Evidence Gate (unchanged)

- Evidence on node/rel properties only.
- No fabricated actor-mesh edges.
- Category similarity ≠ proof.

---

## 4. Execution

```powershell
cd e:\recherche
python _neo4j/review/2026-06-06_full_graph_verification/_post_ier_w2_wave_run.py
```

Patch apply (per agent, after dry-run pass):

```powershell
python _scripts/apply_neo4j_review_patch.py --patch <path>
python _scripts/apply_neo4j_review_patch.py --patch <path> --confirm "APPLY <filename> TO mit-bestand"
```
