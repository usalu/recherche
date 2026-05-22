# Verifier Agent EP-06 — Logistics & Dismantling Chain (Element Proof)

**Database:** `mit-bestand` (READ-ONLY; `read-cypher` / Python driver only; no graph mutation)
**Date:** 2026-06-06
**Campaign:** 10-agent ELEMENT-PROOF ([`VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md`](../VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md) §Agent 06)
**Ledger:** [`ledger/element_proof_agent_06.csv`](../ledger/element_proof_agent_06.csv)

---

## 1. Scope recap

**Relationship types (Σ = **1,303**, reconciled exactly):**

| Type | Count | Range | Allowed domains |
|---|---:|---|---|
| `HAT_LOGISTIK` | 434 | `:Logistik` | `Bauteilgruppe`, `Projekt` |
| `HAT_RUECKBAUVERFAHREN` | 308 | `:Rueckbauverfahren` | `Bauteilgruppe`, `Projekt` |
| `HAT_ERGEBNIS` | 294 | `:Wiederverwendungsergebnis` | `Bauteilgruppe`, `Projekt` |
| `HAT_AUFBEREITUNG` | 267 | `:Aufbereitungsverfahren` | `Bauteilgruppe`, `Projekt`, `ReuseRule` |

`IST_UNTERVERFAHREN_VON` is **out of scope** (already element-covered per plan).

All counts confirmed against live Neo4j enumeration query.

---

## 2. Counts by verdict

| Verdict | Rows |
|---|---:|
| PROVEN | 1303 |

**Σ rows:** 1303 (all `coverage_level=element`, one row per `elementId(r)`).

---

## 3. Verification method

Tier-C process/vocabulary edges — **contract + logic** attestation (no web fetch required per Evidence Gate §3).

Per edge:
1. Live resolution of `elementId(r)`, `a.id`, `b.id`.
2. Domain label ∈ schema-allowed set for the rel type.
3. Range label equals the dedicated closed-vocab label (`Logistik`, `Rueckbauverfahren`, `Wiederverwendungsergebnis`, `Aufbereitungsverfahren`).
4. For `HAT_ERGEBNIS` / `HAT_AUFBEREITUNG`: process-DAG consistency — target vocab nodes are closed-set members with ≥1 incoming edge (Agent 13 Rule 4: **0 orphan** process vocab); no `IST_UNTERVERFAHREN_VON` cycle risk on these rel types.

Aggregate type-level proof from Agent 13 (`A13-rel-type-0005` … `0008`) cited in `notes`; **each row states the edge-level claim** (no aggregate ledger rows).

---

## 4. Domain/range matrix (live)

| rel_type | from_label | to_label | count |
|---|---|---|---:|
| `HAT_AUFBEREITUNG` | `Bauteilgruppe` | `Aufbereitungsverfahren` | 211 |
| `HAT_AUFBEREITUNG` | `Projekt` | `Aufbereitungsverfahren` | 19 |
| `HAT_AUFBEREITUNG` | `ReuseRule` | `Aufbereitungsverfahren` | 37 |
| `HAT_ERGEBNIS` | `Bauteilgruppe` | `Wiederverwendungsergebnis` | 291 |
| `HAT_ERGEBNIS` | `Projekt` | `Wiederverwendungsergebnis` | 3 |
| `HAT_LOGISTIK` | `Bauteilgruppe` | `Logistik` | 337 |
| `HAT_LOGISTIK` | `Projekt` | `Logistik` | 97 |
| `HAT_RUECKBAUVERFAHREN` | `Bauteilgruppe` | `Rueckbauverfahren` | 305 |
| `HAT_RUECKBAUVERFAHREN` | `Projekt` | `Rueckbauverfahren` | 3 |

**Schema violations:** 0 (expected 0).

---

## 5. Notable patterns

- **Bauteilgruppe-heavy:** most edges originate from component-group subjects (1144 / 1,303).
- **ReuseRule → Aufbereitungsverfahren:** 37 edges from synthetic country×material reuse-rule aggregators (Agent 11 pattern).
- **Projekt-level process edges:** 122 edges at project granularity.

---

## 6. Escalations

None — all 1,303 edges structurally PROVEN.

---

## 7. Coverage statement

Scope rels Σ = 1,303 — **one element row each**, `graph_element_id = elementId(r)`. No graph mutation performed.

## 8. One-paragraph summary

Agent EP-06 enumerated all 1,303 live `HAT_LOGISTIK` / `HAT_RUECKBAUVERFAHREN` / `HAT_ERGEBNIS` / `HAT_AUFBEREITUNG` edges in `mit-bestand` and emitted per-element ledger rows with `coverage_level=element`. **Structural integrity is complete:** 100 % of edges conform to schema domain/range rules, all four closed process-vocab target sets are fully wired (no orphan targets), and 1303 / 1,303 rows are `PROVEN` via contract/logic attestation with verbatim edge-level `proof_quote`. No web evidence was required (Tier-C vocab/process classification). `IST_UNTERVERFAHREN_VON` was correctly excluded from this shard.
