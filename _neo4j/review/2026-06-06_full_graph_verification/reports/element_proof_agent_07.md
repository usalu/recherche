# Verifier Agent EP-07 — Methods, design & outcome vocabulary — Element Proof Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; `read-cypher` / driver read session only)
**Ledger:** [`ledger/element_proof_agent_07.csv`](../ledger/element_proof_agent_07.csv) — **1159** relationship rows (`coverage_level=element`)

## 1. Scope recap

Authoritative enumeration via scope Cypher (9 rel types):

| rel_type | count |
|---|---:|
| `HAT_RESSOURCENQUELLE` | 264 |
| `HAT_METHODE` | 241 |
| `HAT_INTERVENTION` | 144 |
| `HAT_BAUWEISE` | 124 |
| `HAT_VERBINDUNGSTECHNIK` | 110 |
| `HAT_ENTWURFSMETHODIK` | 79 |
| `HAT_ARCHITEKTURERGEBNIS` | 79 |
| `HAT_BAUSYSTEM` | 61 |
| `HAT_DEFEKT` | 57 |
| **Total** | **1159** |

## 2. Counts by verdict

| Verdict | Count |
|---|---:|
| PROVEN | 1159 |

Proposed actions: `KEEP` 1159.

## 3. Special checks

- **DEPRECATED Entwurfsmethodik / Architekturergebnis isolation:** Live graph has **16** `:DEPRECATED` nodes (8 `Entwurfsmethodik`, 8 `Architekturergebnis`). **0** in-scope edges target a `:DEPRECATED` node (`deprecated_target_edges=0`). **PASS**.
- **HAT_ENTWURFSMETHODIK / HAT_ARCHITEKTURERGEBNIS:** All 79+79 edges target active (non-deprecated) vocab nodes; domain 100% `:Projekt`.
- **HAT_DEFEKT / HAT_BAUSYSTEM:** Domains include `:Bauteilgruppe` (32/37 edges) plus valid reuse-process domains (`Projekt`, `Bauwerk`, `Materialdepot`) per Agent 12 aggregate proof.
- **HAT_METHODE:** 241 edges; domain `:Akteur` 144, `:Projekt` 80, `:Bauteilgruppe` 13, `:Software` 4 — all contract-valid.

## 4. Schema violations

None. All 1,159 edges pass domain/range contract checks.

## 5. Anomalies / notes

- Tier-C vocab/process shard: `basis_type=contract`; no `evidence_url` on these rel types — structural proof via endpoint labels and controlled vocabulary (not web fetch).
- Prior aggregate rows `A12-rel-agg-0010` … `A12-rel-agg-0016` superseded by this per-element ledger for Agent 10 merge.
- English-named active replacements (`ae_patchwork_envelope`, `em_design_for_disassembly`, …) carry all live `HAT_ENTWURFSMETHODIK` / `HAT_ARCHITEKTURERGEBNIS` edges; German legacy nodes remain isolated.

## 6. Items escalated to human

None — all edges structurally valid.

## 7. One-paragraph summary

Agent EP-07 emitted **1159** element-level ledger rows for methods/design/outcome vocabulary edges (`HAT_RESSOURCENQUELLE` through `HAT_DEFEKT`). Verdicts: **1159 PROVEN**, **0 SCHEMA_VIOLATION**. The mandatory DEPRECATED-node isolation check passes: zero in-scope edges reach the 16 deprecated `Entwurfsmethodik`/`Architekturergebnis` nodes. All edges satisfy contract domain/range rules; proposed action **KEEP** throughout.
