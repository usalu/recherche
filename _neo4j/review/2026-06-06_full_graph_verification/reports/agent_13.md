# Verifier Agent 13 — Process & Requirement Logic Integrity

**Database:** `mit-bestand` (READ-ONLY; only `get-schema` + `read-cypher` used; no graph mutation)
**Date:** 2026-06-06
**Tier:** C — Ontology & structure (internal/structural verification via schema contract + logic rules; no web fetching required)
**Ledger:** [`ledger/agent_13.csv`](../ledger/agent_13.csv)

---

## 1. Scope recap

**Relationship types (Σ = 6,435, reconciled exactly):**

| Type | Count | Type | Count |
|---|---:|---|---:|
| ERFORDERT_NACHWEIS | 1578 | HAT_AUFBEREITUNG | 267 |
| TRIGGERS_REGULIERUNGSFRAGE | 1130 | HAT_RESSOURCENQUELLE | 264 |
| HAT_PROZESSPHASE | 679 | HAT_METHODE | 244 |
| HAT_BESCHAFFUNGSWEG | 592 | HAT_HUERDE | 237 |
| HAT_LOGISTIK | 434 | HAT_INTERVENTION | 144 |
| HAT_RUECKBAUVERFAHREN | 308 | ERFUELLT_NACHWEIS | 118 |
| HAT_ERGEBNIS | 294 | HAT_SCHADSTOFFRISIKO | 100 |
| | | ERFORDERT_SCHADSTOFFPRUEFUNG | 37 |
| | | IST_UNTERVERFAHREN_VON | 9 |

**Nodes:** PruefungNachweis 118, Nachweisforderung 27, Regulierungsfrage 11, Leistungsanforderung 8, plus process vocab (Prozessphase 10, Beschaffungsweg 10, Logistik 10, Rueckbauverfahren 6, Wiederverwendungsergebnis 6, Aufbereitungsverfahren 6, Ressourcenquelle 5, Methode 6, Huerde 11, BauaufgabeIntervention 10).

All planning-time counts confirmed against the live graph.

---

## 2. Counts by verdict

| Verdict | Ledger rows | Underlying elements |
|---|---:|---|
| PROVEN | 24 | 15 rel-type structural classes (6,426 edges) + 9 IST_UNTERVERFAHREN_VON edges + satisfiable-NF group (9 nodes) + PruefungNachweis (118) + Regulierungsfrage (11) + Leistungsanforderung (8) + process vocab (90) |
| CONTRADICTION | 18 | 18 dangling `Nachweisforderung` requirement types (unsatisfiable) |

No SCHEMA_VIOLATION, no wrong-target-label edges, no cycles, no orphan vocabulary, no label contamination.

---

## 3. Logic rules — results

### Rule 1 — Correct target labels & valid domains (PASS)
A single domain/range matrix query over all 16 scope types shows **100 %** of edges conform to the schema range:
- Every `ERFORDERT_NACHWEIS` → `:Nachweisforderung` (1578/1578).
- Every `TRIGGERS_REGULIERUNGSFRAGE` → `:Regulierungsfrage` (1130/1130). No edge points to a non-`Regulierungsfrage` node.
- Every `ERFUELLT_NACHWEIS` runs `:PruefungNachweis` → `:Nachweisforderung` (118/118).
- Every `HAT_*` process edge targets its dedicated vocabulary label; every `ERFORDERT_SCHADSTOFFPRUEFUNG` runs `:Projekt` → `:Schadstoff`.
All source-side domains fall within the schema-allowed sets. **Zero label violations.**

### Rule 2 — `IST_UNTERVERFAHREN_VON` is acyclic (PASS)
All 9 edges enumerated. Self-loop scan and `*2..10` cycle scan both returned **empty**. The relation forms a clean **3-root forest** (a DAG):
- `pr_zerstoerende_pruefung` ← {`pr_bohrkernpruefung_beton`, `pr_zugversuch`}
- `pr_brandschutznachweis` ← `pr_abbrandbemessung`
- `pr_schadstoffpruefung` ← `pr_schadstoffscreening`
- `vt_reversible_fuegung` ← {bolzen-, demontierbarer_schwerlastanker, klemm-, steck-, verschraubung}

Endpoints are always same-label (PruefungNachweis→PruefungNachweis or Verbindungstechnik→Verbindungstechnik), consistent with a taxonomic sub-procedure relation. *(The 5 Verbindungstechnik nodes are vocab owned by Agent 12; the `IST_UNTERVERFAHREN_VON` rel-type is owned here.)*

### Rule 3 — Requirements satisfiable (FAIL — primary finding)
Of the **27** `Nachweisforderung`, only **9** are satisfiable (have ≥1 `ERFUELLT_NACHWEIS` from a `PruefungNachweis`). **18 are dangling**: demanded by `ERFORDERT_NACHWEIS` but with **zero** satisfying proof. The 118 `PruefungNachweis` collapse their `ERFUELLT_NACHWEIS` coverage onto just 9 requirement types.

This is a graph-wide logical-coherence gap, not a label error: the `ERFORDERT_NACHWEIS` edges are individually well-formed (and carry `source_url`, verified by Agent 07), but the compliance graph cannot *close the loop* on 18 requirement types — a reuse process can be told a proof is required yet the graph models no procedure that delivers it.

### Rule 4 — No dangling/contradicting structures elsewhere (PASS)
- All **11** `Regulierungsfrage` are triggered (≥14 incoming `TRIGGERS_REGULIERUNGSFRAGE`) and each emits ≥3 `ERFORDERT_NACHWEIS` — no orphan questions, no dead-end questions.
- All **8** `Leistungsanforderung` have a `maps_to_nachweisforderung` pointer that resolves to a real `Nachweisforderung` and equals their own `ERFORDERT_NACHWEIS` target.
- All **118** `PruefungNachweis` are connected (0 isolated, 0 without fulfillment).
- All `Nachweisforderung` have demands > 0 (no unused requirement node).
- Every process-vocab node receives ≥1 incoming edge (no orphan vocab); no node in scope carries a second label.

---

## 4. Ten worst findings

The worst-class findings are the 18 unsatisfiable requirements, ranked by demand pressure (number of `ERFORDERT_NACHWEIS` edges left unsatisfiable):

| # | Nachweisforderung | Demands | Fulfillments | Verdict |
|---|---|---:|---:|---|
| 1 | `nf_oekobilanz_epd` (OekobilanzEPD) | 67 | 0 | CONTRADICTION |
| 2 | `nf_materialpass_ressourcenpass` | 54 | 0 | CONTRADICTION |
| 3 | `nf_bauteilidentifikation` | 50 | 0 | CONTRADICTION |
| 4 | `nf_befestigungsnachweis` | 48 | 0 | CONTRADICTION |
| 5 | `nf_schadstoffkataster_erkundung` | 39 | 0 | CONTRADICTION |
| 6 | `nf_dauerhaftigkeit_restlebensdauer` | 35 | 0 | CONTRADICTION |
| 7 | `nf_holzschutzmittel_check` | 29 | 0 | CONTRADICTION |
| 8 | `nf_bauphysiknachweis` | 28 | 0 | CONTRADICTION |
| 9 | `nf_genehmigungs_oder_zustimmungsbedarf` | 27 | 0 | CONTRADICTION |
| 10 | `nf_rc_gesteinskoernung_eignung` | 25 | 0 | CONTRADICTION |

Remaining 8 (also CONTRADICTION): `nf_barrierefreiheit_nachweis` (18), `nf_absturzsicherung` (14), `nf_asbest_check` (10), `nf_elektrosicherheitsnachweis` (7), `nf_hygiene_und_reinigungsnachweis` (7), `nf_schwermetall_oder_bleifarbe_check` (6), `nf_formaldehyd_oder_emissionsnachweis` (5), `nf_mineralische_ersatzbaustoff_guete` (4).

**Notable near-miss:** `pr_schadstoffscreening` exists as a `PruefungNachweis` (sub-procedure of `pr_schadstoffpruefung`) yet `nf_asbest_check`, `nf_holzschutzmittel_check`, `nf_schwermetall_oder_bleifarbe_check` and `nf_formaldehyd_oder_emissionsnachweis` remain unfulfilled — a pollutant-screening procedure is present but not wired to satisfy these pollutant requirements.

---

## 5. Escalations to human (`ESCALATE_HUMAN`)

The 18 dangling `Nachweisforderung` are escalated, not deleted. The `ERFORDERT_NACHWEIS` demand edges are sourced and structurally valid, so the correct remediation is **coverage**, not removal. Options for a human/aggregator:
1. Add `ERFUELLT_NACHWEIS` edges from existing/new `PruefungNachweis` nodes that genuinely satisfy these requirements (e.g. connect `pr_schadstoffscreening` to the pollutant requirements; add EPD / material-passport / identification procedures).
2. Or, if a requirement is intentionally "informational only" with no verifying procedure in scope, mark it as such in the contract so the satisfiability rule can exempt it.

No automatic patch is proposed: closing these loops is a modelling decision, not a mechanical fix.

---

## 6. Coverage statement

Scope rels Σ = 6,435 (16 types) — all verified for target-label/domain conformance; 9 `IST_UNTERVERFAHREN_VON` individually proven acyclic. Scope nodes (PruefungNachweis 118, Nachweisforderung 27, Regulierungsfrage 11, Leistungsanforderung 8, process vocab 90) — all verified. **No graph mutation performed.**

## 7. One-paragraph summary

Agent 13 verified the reuse-process & compliance subgraph (6,435 relationships across 16 types + 254 process/requirement nodes) entirely by schema-contract and logic rules, read-only. **Structural integrity is excellent**: 100 % of edges carry the correct target label and a valid source domain, `IST_UNTERVERFAHREN_VON` is a clean acyclic 3-root forest, all `Regulierungsfrage`/`Leistungsanforderung`/`PruefungNachweis` are well-connected, and there are no orphan or multi-label vocabulary nodes. **The single material finding** is a satisfiability gap: 18 of 27 `Nachweisforderung` requirement types are demanded (some by 30–67 edges) but cannot be satisfied by any `PruefungNachweis` via `ERFUELLT_NACHWEIS` — the proof layer only closes the loop on 9 requirement types. These 18 are flagged `CONTRADICTION` → `ESCALATE_HUMAN` for coverage remediation rather than deletion.
