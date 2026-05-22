# Verifier Agent EP-05 — Process Phase & Procurement (Element Proof)

**Database:** `mit-bestand` (READ-ONLY; `read-cypher` / Python driver only; no graph mutation)
**Date:** 2026-06-06
**Campaign:** 10-agent ELEMENT-PROOF ([`VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md`](../VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md) §Agent 05)
**Ledger:** [`ledger/element_proof_agent_05.csv`](../ledger/element_proof_agent_05.csv)

---

## 1. Scope recap

**Relationship types (Σ = **1,270**, reconciled exactly):**

| Type | Count | Range | Allowed domains |
|---|---:|---|---|
| `HAT_PROZESSPHASE` | 679 | `:Prozessphase` | `Bauteilgruppe`, `Projekt` |
| `HAT_BESCHAFFUNGSWEG` | 591 | `:Beschaffungsweg` | `Bauteilgruppe`, `Projekt`, `Akteur`, `Software` |

Live graph: `HAT_PROZESSPHASE` domains are exclusively `Bauteilgruppe` (567) + `Projekt` (112); `HAT_BESCHAFFUNGSWEG` adds `Akteur` (57) and `Software` (6). No `evidence_url` / `source_url` on any in-scope rel.

---

## 2. Counts by verdict

| Verdict | Rows |
|---|---:|
| PROVEN | 1270 |

**Σ rows:** 1270 (all `coverage_level=element`, one row per `elementId(r)`).

---

## 3. Verification method

Tier-C process/vocabulary edges — **contract + logic** attestation (Evidence Gate §3; no web fetch).

Per edge:
1. Live resolution of `elementId(r)`, `a.id`, `b.id`, endpoint labels.
2. Domain label ∈ schema-allowed set for the rel type.
3. Range label equals closed vocab (`Prozessphase` / `Beschaffungsweg`); target id prefix `phase_` / `bweg_`.
4. **Phase ordering (soft):** subjects with multiple `HAT_PROZESSPHASE` edges checked against canonical reuse lifecycle (Identifikation → Planung → Rueckbau → Transport → Lagerung → Aufbereitung → Pruefung → Wiedereinbau → Dokumentation → Betrieb); 192 multi-phase subjects, no per-edge SCHEMA_VIOLATION from ordering.
5. **Orphan vocab (Agent 13 Rule 4):** all 10 `:Prozessphase` and all 10 `:Beschaffungsweg` nodes receive ≥1 incoming edge — **0 orphans**.

Aggregate type-level proof from Agent 13 (`A13-rel-type-0003`, `A13-rel-type-0004`) cited in `notes`; each row states the edge-level claim.

---

## 4. Domain/range matrix (live)

| rel_type | from_label | to_label | count |
|---|---|---|---:|
| `HAT_BESCHAFFUNGSWEG` | `Akteur` | `Beschaffungsweg` | 57 |
| `HAT_BESCHAFFUNGSWEG` | `Bauteilgruppe` | `Beschaffungsweg` | 468 |
| `HAT_BESCHAFFUNGSWEG` | `Projekt` | `Beschaffungsweg` | 60 |
| `HAT_BESCHAFFUNGSWEG` | `Software` | `Beschaffungsweg` | 6 |
| `HAT_PROZESSPHASE` | `Bauteilgruppe` | `Prozessphase` | 567 |
| `HAT_PROZESSPHASE` | `Projekt` | `Prozessphase` | 112 |

**Schema violations:** 0 (expected 0).

---

## 5. Notable patterns

- **Bauteilgruppe-heavy process phases:** 567 / 679 `HAT_PROZESSPHASE` edges from component groups.
- **Akteur procurement paths:** 57 edges model marketplace/platform sourcing at actor granularity (Bauteilboerse operators).
- **Extended Beschaffungsweg vocab (live, not in seed file):** `bweg_lager`, `bweg_leihmodell`.

---

## 6. Escalations

None — all 1,270 edges structurally PROVEN.

---

## 7. Coverage statement

Scope rels Σ = 1,270 — **one element row each**, `graph_element_id = elementId(r)`. No graph mutation performed.

## 8. One-paragraph summary

Agent EP-05 enumerated all 1,270 live `HAT_PROZESSPHASE` (679) and `HAT_BESCHAFFUNGSWEG` (591) edges in `mit-bestand` and emitted per-element ledger rows with `coverage_level=element`. **Structural integrity is complete:** 100 % of edges conform to schema domain/range rules, all process-phase and procurement vocab targets are wired (0 orphan nodes), and 1270 / 1,270 rows are `PROVEN` via contract/logic attestation with verbatim edge-level `proof_quote`. No web evidence was required (Tier-C vocab/process classification). Phase ordering was cross-checked against the reuse lifecycle template; no aggregate-only verdicts were used.
