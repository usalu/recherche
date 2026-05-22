# Post-IER Verification — W3 Follow-Up Wave (10 Agents)

**Status:** EXECUTING  
**Date:** 2026-06-07  
**Database:** `mit-bestand` (**2,263 nodes / 14,819 rels** post-W2)  
**Prior ledger:** `VERIFICATION_LEDGER_ELEMENT_v4.csv` — **17,081 rows** · **91.72% PROVEN**  
**Runner:** [`_post_ier_w3_wave_run.py`](_post_ier_w3_wave_run.py)

---

## 0. Why W3 exists

W2 closed schema/geo applies and re-adjudicated catalogue offset 200–500 (0 upgrades under strict gate). Seven surfaces remain:

| Gap | Count (v4 / live) | Owner | W3 action |
|---|---:|---|---|
| Catalogue rels without `evidence_quote` | **~762** remainder (500 done) | W3-01…04 | Four batches @ offsets 500, 690, 880, 1070; strict Q04 gate |
| `VERBUNDEN_MIT_AKTEUR` weak on graph | **122** live | W3-05 | Live scan; web proof or DELETE draft |
| `MISSING_EVIDENCE` residual | **215** | W3-06, W3-07 | Web search ladder split a–m / n–z |
| `PARTIAL` residual | **331** | W3-08 | Fetch upgrade or DELETE draft |
| `CONTRADICTION` geo | **14** | W3-09 | Human-merge proposals |
| `SCHEMA_VIOLATION` tier-D | **33** | W3-09 | Deprecation proposals |
| `UNVERIFIABLE` persons | subset of **357** | W3-09 | Deprecation / escalate |

**Do not apply** `post_01_catalogue_backfill.patch.jsonl` or W2 catalogue patches without strict-gate upgrades.

---

## 1. Definition of Done

| # | Criterion |
|---|---|
| **D1** | Each agent emits `ledger/w3_0N.csv` + `reports/w3_0N_report.md`. |
| **D2** | Patches dry-run before apply; graph counts recorded before/after each apply. |
| **D3** | `PROVEN` requires verbatim `proof_quote` / `evidence_quote` (Evidence Gate). |
| **D4** | W3-10 publishes `VERIFICATION_LEDGER_ELEMENT_v5.csv` + `reports/POST_IER_W3_REPORT.md`. |
| **D5** | DELETE patches drafted only — not applied without explicit report note. |
| **D6** | Auto-apply only `set_rel_properties` / `set_node_properties` when dry-run is clean. |

---

## 2. Agent scopes

### W3-01 — Catalogue backfill (offset 500–689)

- **Scope:** Live `HAT_BAUTEILTYP` / `NUTZT_MATERIAL` where `evidence_quote` empty; **SKIP 500 LIMIT 190**.
- **Method:** Fetch `source_url` / actor URLs; Q04 strict gate; upgrade patch on verbatim quote.
- **Outputs:** `ledger/w3_01.csv`, `reports/w3_01_report.md`, `patches/w3_01_catalogue_backfill.patch.jsonl`

### W3-02 — Catalogue (offset 690–879)

- Same method; **SKIP 690 LIMIT 190**.
- **Outputs:** `ledger/w3_02.csv`, `reports/w3_02_report.md`, `patches/w3_02_catalogue_backfill.patch.jsonl`

### W3-03 — Catalogue (offset 880–1069)

- **SKIP 880 LIMIT 190**.
- **Outputs:** `ledger/w3_03.csv`, `reports/w3_03_report.md`, `patches/w3_03_catalogue_backfill.patch.jsonl`

### W3-04 — Catalogue (offset 1070–end)

- **SKIP 1070 LIMIT 500** (~192 remainder).
- **Outputs:** `ledger/w3_04.csv`, `reports/w3_04_report.md`, `patches/w3_04_catalogue_backfill.patch.jsonl`

### W3-05 — VMA weak edges (live graph)

- **Scope:** All live `VERBUNDEN_MIT_AKTEUR` missing `evidence_quote` and `evidence_url`.
- **Method:** Q05 actor-org gate; pairwise web proof; DELETE draft if gate fails.
- **Outputs:** `ledger/w3_05.csv`, `reports/w3_05_report.md`, `patches/w3_05_vma.patch.jsonl`

### W3-06 — MISSING_EVIDENCE rows a–m

- **Scope:** v4 `MISSING_EVIDENCE` where `element_id` first alpha char ∈ [a–m].
- **Method:** Web search ladder (basis_ref, notes domains, candidate hints).
- **Outputs:** `ledger/w3_06.csv`, `reports/w3_06_report.md`, `patches/w3_06_missing_evidence.patch.jsonl`

### W3-07 — MISSING_EVIDENCE rows n–z

- Same method for first alpha char ∈ [n–z].
- **Outputs:** `ledger/w3_07.csv`, `reports/w3_07_report.md`, `patches/w3_07_missing_evidence.patch.jsonl`

### W3-08 — PARTIAL residual

- **Scope:** All v4 `PARTIAL` rows (331).
- **Method:** Re-fetch basis URLs; upgrade if verbatim quote; DELETE draft for unsupported VMA inference.
- **Outputs:** `ledger/w3_08.csv`, `reports/w3_08_report.md`, `patches/w3_08_partial.patch.jsonl`

### W3-09 — CONTRADICTION + SCHEMA + UNVERIFIABLE persons

- **Scope:** 14 CONTRADICTION + 33 SCHEMA_VIOLATION + UNVERIFIABLE where `element_id` starts with `p_`.
- **Method:** Human-merge / deprecation proposals; no auto-delete.
- **Outputs:** `ledger/w3_09.csv`, `reports/w3_09_report.md`, `patches/w3_09_tier_d.patch.jsonl` (draft only)

### W3-10 — Aggregator

- **Scope:** Merge W3-01…09 overlays on v4 → v5; consolidate patches; campaign report.
- **Outputs:** `ledger/w3_10.csv`, `VERIFICATION_LEDGER_ELEMENT_v5.csv`, `reports/w3_10_report.md`, `reports/POST_IER_W3_REPORT.md`

---

## 3. Evidence Gate (unchanged)

- Evidence on node/rel properties only.
- Actor edges need both endpoints named on page.
- No category inference for VMA.
- Catalogue: classification token must appear verbatim in quote.

---

## 4. Execution

```powershell
cd e:\recherche
python _neo4j/review/2026-06-06_full_graph_verification/_post_ier_w3_wave_run.py
```

Patch apply policy:

```powershell
# Dry-run all patches
python _scripts/apply_neo4j_review_patch.py --patch <path>

# Auto-apply upgrades only (runner handles filtering)
python _scripts/apply_neo4j_review_patch.py --patch <path> --confirm "APPLY <filename> TO mit-bestand"
```

DELETE ops are **never** auto-applied in W3.
