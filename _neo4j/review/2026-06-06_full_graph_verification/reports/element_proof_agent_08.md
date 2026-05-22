# Verifier Agent EP-08 — Element-Level Vocab & Process Nodes

**Database:** `mit-bestand` (READ-ONLY; `read-cypher` only)
**Date:** 2026-06-06
**Tier:** C — ontology / structure (contract + logic; no web fetch)
**Ledger:** [`ledger/element_proof_agent_08.csv`](../ledger/element_proof_agent_08.csv)
**Plan:** [`VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md`](../VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md) §Agent 08

---

## 1. Scope recap

**Nodes enumerated:** **1066** (live `SCOPE_CYPHER`; plan target was 1,040 at gap-inventory time — delta reconciled below)

| Primary label | Count |
|---|---:|
| `Bauteilgruppe` | 364 |
| `Kennwert` | 255 |
| `PruefungNachweis` | 118 |
| `Nachweisforderung` | 27 |
| `Material` | 26 |
| `Akteurrolle` | 22 |
| `Bauteiltyp` | 22 |
| `Architekturergebnis` | 16 |
| `Entwurfsmethodik` | 16 |
| `Schadstoff` | 13 |
| `Huerde` | 11 |
| `Materialgruppe` | 11 |
| `Regulierungsfrage` | 11 |
| `Verbindungstechnik` | 11 |
| `Akteurtyp` | 10 |
| `BauaufgabeIntervention` | 10 |
| `Beschaffungsweg` | 10 |
| `Defekt` | 10 |
| `Logistik` | 10 |
| `Prozessphase` | 10 |
| `Nutzung` | 9 |
| `Bausystem` | 8 |
| `Leistungsanforderung` | 8 |
| `Aufbereitungsverfahren` | 6 |
| `Bauweise` | 6 |
| `Bauobjektrolle` | 6 |
| `BauwerkEra` | 6 |
| `Methode` | 6 |
| `Rueckbauverfahren` | 6 |
| `Wiederverwendungsergebnis` | 6 |
| `ZustandsKlasse` | 6 |
| `Geschaeftsmodell` | 5 |
| `Ressourcenquelle` | 5 |

**Relationships:** 0 (node-only shard)

---

## 2. Counts by verdict

| Verdict | Rows |
|---|---:|
| CONTRADICTION | 11 |
| PROVEN | 1047 |
| SCHEMA_VIOLATION | 8 |

| Proposed action | Rows |
|---|---:|
| KEEP | 1047 |
| ESCALATE_HUMAN | 11 |
| DEPRECATE_NODE | 8 |

---

## 3. Special checks

### PruefungNachweis (118)
All **118** nodes have ≥1 outgoing `ERFUELLT_NACHWEIS` (0 isolated, 0 without fulfillment). **PASS.**

### Nachweisforderung / R02 dangling
Of **27** `Nachweisforderung` nodes, **11** remain unsatisfiable (demands>0, fulfillments=0) after Wave-2 R02 patch (+10 `ERFUELLT_NACHWEIS`). These are `CONTRADICTION` → `ESCALATE_HUMAN` (coverage gap, not invalid requirements).

### DEPRECATED isolation (16)
All **16** `:DEPRECATED` nodes (8 `Architekturergebnis` + 8 `Entwurfsmethodik` German legacy) have **degree 0**. **PASS.**

### Vocab stubs (`name==id` / orphan)
R05 applied human-readable names to the 8 Agent-12 stubs (`bt_fassadenelement`, …). All **8** still have **0 incoming** classification edges (outgoing reg edges only) → `SCHEMA_VIOLATION` / `DEPRECATE_NODE`.

---

## 4. Ten worst findings

| # | Node id | Label | Verdict | Action | Proof |
|---|---|---|---|---|---|
| 1 | `nf_barrierefreiheit_nachweis` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=18 fulfillments=0; R02 residual dangling requirement |
| 2 | `nf_befestigungsnachweis` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=48 fulfillments=0; R02 residual dangling requirement |
| 3 | `nf_dauerhaftigkeit_restlebensdauer` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=35 fulfillments=0; R02 residual dangling requirement |
| 4 | `nf_elektrosicherheitsnachweis` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=7 fulfillments=0; R02 residual dangling requirement |
| 5 | `nf_genehmigungs_oder_zustimmungsbedarf` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=27 fulfillments=0; R02 residual dangling requirement |
| 6 | `nf_hygiene_und_reinigungsnachweis` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=7 fulfillments=0; R02 residual dangling requirement |
| 7 | `nf_materialpass_ressourcenpass` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=54 fulfillments=0; R02 residual dangling requirement |
| 8 | `nf_mineralische_ersatzbaustoff_guete` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=4 fulfillments=0; R02 residual dangling requirement |
| 9 | `nf_oekobilanz_epd` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=67 fulfillments=0; R02 residual dangling requirement |
| 10 | `nf_rc_gesteinskoernung_eignung` | Nachweisforderung | CONTRADICTION | ESCALATE_HUMAN | demands=25 fulfillments=0; R02 residual dangling requirement |

---

## 5. Count reconciliation (1,040 plan vs 1066 live)

The §2.3 gap inventory counted nodes lacking a prior `coverage_level=element` ledger row. Live enumeration of `SCOPE_CYPHER` returns **1066** nodes — the agent proves **every** vocab/process node in scope (not only the historical gap subset). Agent 10 dedupes against retained prior element rows.

---

## 6. Summary

Agent EP-08 emitted **1066** element-level node rows (`coverage_level=element`). **1047** nodes are structurally proven (identity, label legality, wiring or allowed isolation). **11** dangling `Nachweisforderung` types remain post-R02. **8** `SCHEMA_VIOLATION` rows (mostly orphan vocab stubs). No graph mutation performed.
