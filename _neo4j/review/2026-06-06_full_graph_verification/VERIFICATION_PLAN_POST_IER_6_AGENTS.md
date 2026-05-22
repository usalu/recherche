# Post-IER Verification — 6-Agent Follow-Up Wave (POST-01…POST-06)

**Status:** EXECUTING  
**Date:** 2026-06-07  
**Database:** `mit-bestand` (post-IER apply: **2,263 nodes / 14,846 rels**)  
**Prior ledger:** `VERIFICATION_LEDGER_ELEMENT_v2.csv` — **17,109 rows** · **93.74% PROVEN**  
**IER apply:** `ier_evidence_recovery.patch.jsonl` (184 ops) + `ier_evidence_recovery_deletes.patch.jsonl` (214 rel deletes, human-approved)

---

## 0. Why this wave exists

Internet Evidence Recovery (IER) applied evidence upgrades and pruned 214 unsupported catalogue/actor-mesh edges. The element ledger `v2` still reflects pre-delete graph keys for 214 relationships and leaves four attestation debt surfaces:

| Gap | Live / ledger count | Owner |
|---|---:|---|
| Catalogue rels without `evidence_quote` | **1,262** (`HAT_BAUTEILTYP` 732 + `NUTZT_MATERIAL` 530) | POST-01 |
| `SCHEMA_VIOLATION` tier-D (`prog_*` category nodes + `TEIL_VON_PROGRAMM`) | **33** (25 prog-related) | POST-02 |
| `CONTRADICTION` geo (address vs Stadt/Land) | **42** | POST-03 |
| `MISSING_EVIDENCE` residual | **323** | POST-04 |
| `PARTIAL` residual | **316** | POST-05 |
| Weak `PROVEN` (domain parking, IER false positives) | **~6+** | POST-06 |

POST-06 merges shard overlays → `VERIFICATION_LEDGER_ELEMENT_v3.csv` and `POST_IER_CAMPAIGN_REPORT.md`.

---

## 1. Definition of Done

| # | Criterion |
|---|---|
| **D1** | Each agent emits `ledger/post_0N.csv` + `reports/post_0N_report.md`. |
| **D2** | Destructive patches are **dry-run only** except where human already approved (IER deletes — done pre-wave). |
| **D3** | `PROVEN` requires verbatim `proof_quote` (Evidence Gate). |
| **D4** | POST-06 ledger covers **only live** graph elements (stale IER-deleted rel rows pruned). |
| **D5** | `VERIFICATION_LEDGER_ELEMENT_v3.csv` + recomputed PROVEN% published. |

---

## 2. Agent scopes (disjoint)

### POST-01 — Catalogue quote backfill

- **Scope:** Live `HAT_BAUTEILTYP` / `NUTZT_MATERIAL` where `coalesce(r.evidence_quote,'') = ''`.
- **Batch:** 200 rels per run (representative sample); document remainder.
- **Method:** Reuse Q04 token/quote gate; fetch actor `source_urls` / enrichment dossiers; propose `set_rel_properties` patch (dry-run).
- **Outputs:** `ledger/post_01.csv`, `reports/post_01_report.md`, `patches/post_01_catalogue_backfill.patch.jsonl`

### POST-02 — SCHEMA_VIOLATION tier-D

- **Scope:** All 33 `SCHEMA_VIOLATION` rows; focus `prog_*` generic Programme nodes + `TEIL_VON_PROGRAMM` edges.
- **Method:** `DEPRECATE_NODE` / `delete_rel` proposals; no live apply.
- **Outputs:** `ledger/post_02.csv`, `reports/post_02_report.md`, `patches/post_02_schema_violation_deletes.patch.jsonl`

### POST-03 — CONTRADICTION geo

- **Scope:** 42 `CONTRADICTION` rows (LIEGT_IN_STADT / LIEGT_IN_LAND mismatches).
- **Method:** Propose `delete_rel` + `add_rel` to correct Stadt/Land from notes; `ESCALATE_HUMAN` where ambiguous.
- **Outputs:** `ledger/post_03.csv`, `reports/post_03_report.md`, `patches/post_03_geo_fixes.patch.jsonl`

### POST-04 — MISSING_EVIDENCE recovery

- **Scope:** 323 `MISSING_EVIDENCE` rows from v2.
- **Method:** HTTP fetch `basis_ref` / noted candidate URLs; upgrade to PROVEN only on verbatim quote.
- **Outputs:** `ledger/post_04.csv`, `reports/post_04_report.md`, `patches/post_04_missing_evidence.patch.jsonl`

### POST-05 — PARTIAL residual

- **Scope:** 316 `PARTIAL` rows.
- **Method:** Re-adjudicate: dangling `nf_*` → KEEP PARTIAL; weak VMA → DELETE proposal; live URL → upgrade attempt.
- **Outputs:** `ledger/post_05.csv`, `reports/post_05_report.md`, `patches/post_05_partial.patch.jsonl`

### POST-06 — Weak PROVEN audit + aggregator

- **Scope:** Domain-parking proofs (`embuild`, `franck`, etc.); merge POST-01…05 overlays on v2; prune stale keys.
- **Outputs:** `ledger/post_06.csv`, `VERIFICATION_LEDGER_ELEMENT_v3.csv`, `reports/post_06_report.md`, `reports/POST_IER_CAMPAIGN_REPORT.md`

---

## 3. Evidence Gate (unchanged)

- Evidence lives on node/rel properties only (`evidence_url`, `evidence_quote`, `source_urls`, …).
- No fabricated actor-mesh edges.
- Category similarity ≠ proof.

---

## 4. Execution

```powershell
cd e:\recherche
python _neo4j/review/2026-06-06_full_graph_verification/_post_ier_wave_run.py
```

Runner: [`_post_ier_wave_run.py`](_post_ier_wave_run.py)
