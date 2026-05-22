# W4 Selective Unsupported Delete — 4-Agent Plan

**Status:** EXECUTED  
**Date:** 2026-06-07T12:52:32Z  
**Database:** `mit-bestand`  
**Prior ledger:** `VERIFICATION_LEDGER_ELEMENT_v5.csv`  
**Consolidated patch:** `patches/w4_selective_unsupported_deletes.patch.jsonl`

---

## 0. Filter rule (Bauteilgruppe exclusion)

**INCLUDE** `delete_rel` when neither endpoint is `bg_*` or `:Bauteilgruppe`.  
**EXCLUDE** all catalogue / material / VMA edges touching Bauteilgruppe — deferred to `BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md`.

| Source | Total delete_rel | bg_ skipped | Eligible |
|---|---:|---:|---:|
| W3-01…05 patches | 636 | 416 | 220 |
| v5 UNSUPPORTED sweep (extra) | 28 | — | 28 |
| **Consolidated patch** | — | — | **248** |

---

## 1. Agents

| Agent | Scope | Deletes | Ledger | Report |
|---|---|---:|---|---|
| **W4-01** | VMA `VERBUNDEN_MIT_AKTEUR` unsupported (no bg_) | 29 | `ledger/w4_01.csv` | `reports/w4_01_report.md` |
| **W4-02** | Catalogue `HAT_BAUTEILTYP` (p_*, marketplace → bt_*, no bg_) | 133 | `ledger/w4_02.csv` | `reports/w4_02_report.md` |
| **W4-03** | `NUTZT_MATERIAL` + v5 UNSUPPORTED sweep + v6 aggregator | 86 | `ledger/w4_03.csv` | `reports/w4_03_report.md` |
| **W4-BG** | **Plan only** — all edges touching `:Bauteilgruppe` | 0 | — | `BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md` |

---

## 2. Execution

```powershell
python _neo4j/review/2026-06-06_full_graph_verification/_w4_orchestrate.py
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/w4_selective_unsupported_deletes.patch.jsonl
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/w4_selective_unsupported_deletes.patch.jsonl --confirm "APPLY w4_selective_unsupported_deletes.patch.jsonl TO mit-bestand"
```

W4-03 emits `VERIFICATION_LEDGER_ELEMENT_v6.csv` and `reports/W4_CLEANUP_REPORT.md`.

---

## 3. Definition of Done

- [x] Consolidated patch built with bg_ exclusion documented
- [x] Dry-run clean on `mit-bestand`
- [x] Live apply (`delete_rel` only, no node deletes)
- [x] Before/after rel counts recorded
- [x] v6 ledger + PROVEN% recomputed
- [x] Bauteilgruppe mission plan (read-only audit)
