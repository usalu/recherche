# Verifier Agent EP-04 — Material groups, Kennwert, era links — Element Proof Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; `read-cypher` / driver read session only)
**Ledger:** [`ledger/element_proof_agent_04.csv`](../ledger/element_proof_agent_04.csv) — **1104** relationship rows (`coverage_level=element`)

## 1. Scope recap

Authoritative enumeration (6 rel types):

| rel_type | live | this ledger |
|---|---:|---:|
| `HAT_MATERIALGRUPPE` | 403 | 403 |
| `HAT_BAUTEILGRUPPE` | 364 | 364 |
| `HAT_KENNWERT` | 255 | 255 |
| `TYPISCH_BEI_MATERIAL` | 74 | 56 |
| `HAT_ZUSTANDSKLASSE` | 18 | 18 |
| `GEBAUT_IN_ERA` | 8 | 8 |
| **Total** | **1122** | **1104** |

- Excluded **18** `TYPISCH_BEI_MATERIAL` Schadstoff edges already element-covered in `VERIFICATION_LEDGER.csv` (Agent 07 web proof).

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
| PROVEN | 1104 |

Proposed actions: `KEEP` 1104.

## 3. Special checks

- **Kennwert `name=null`:** All 255 `HAT_KENNWERT` targets have `kennwert` and/or `wert` populated; `name=null` is by design.
- **HAT_BAUTEILGRUPPE:** 364 instance edges (360 `Projekt` + 4 `Programm` → `Bauteilgruppe`); not duplicate vocab nodes.
- **TYPISCH_BEI_MATERIAL gap shard:** 56 edges (Aufbereitungsverfahren 18, Defekt 14, PruefungNachweis 12, ZustandsKlasse 12); 18 Schadstoff edges retained from prior ledger.
- **HAT_ZUSTANDSKLASSE / GEBAUT_IN_ERA:** 18 + 8 edges; domain/range 100% valid.

## 4. Schema violations

None. All 1,104 edges pass domain/range contract checks.

## 5. Anomalies / notes

- Tier-C / instance shard: `basis_type=contract` or `logic`; no `evidence_url` on these rel types.
- Prior aggregate rows `A12-rel-agg-0005/0006/0007/0017/0018/0021` superseded by this per-element ledger for Agent 10 merge.

## 6. Items escalated to human

None.

## 7. One-paragraph summary

Agent EP-04 emitted **1104** element-level ledger rows for material-group, Kennwert, era, and typical-material links. Verdicts: **1104 PROVEN**, **0 SCHEMA_VIOLATION**. All edges satisfy contract domain/range rules; Kennwert instances verified via `kennwert`/`wert`/`einheit` despite `name=null`. Eighteen Schadstoff `TYPISCH_BEI_MATERIAL` edges excluded as already element-proven by Agent 07.
