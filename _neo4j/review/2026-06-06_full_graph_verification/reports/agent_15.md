# Agent 15 — Aggregator & Adjudicator Report

**Date:** 2026-06-06 · **Database:** `mit-bestand` · **Mode:** READ-ONLY on Neo4j (no writes, no patches applied).

## Scope recap

Merged the 14 shard ledgers, proved coverage against the live graph, synthesized findings by severity and by
run/type/country, and drafted only the high-confidence non-destructive patch. Live graph confirmed at
**2,304 nodes / 15,457 relationships** (matches plan baseline). Graph id inventory exported read-only via
`default_access_mode="READ"` (`_agent15_export_graph_ids.py`).

## Artifacts written

| File | Purpose |
|---|---|
| `VERIFICATION_LEDGER.csv` | Merged 7,898 rows (17 original cols + `source_agent`, `coverage_level`, `graph_element_id`, `match_status`) |
| `COVERAGE_PROOF.md` | Element vs type-level vs uncovered, with the exact gap ledger and re-dispatch list |
| `CAMPAIGN_REPORT.md` | Verdict/action counts + "where mistakes happened" heatmap |
| `REMEDIATION_PLAN.md` | Grouped actions (DELETE/RELABEL/ADD_SOURCE/MERGE_DUPLICATE/DEPRECATE_NODE/FIX_PROPERTY/ESCALATE_HUMAN) |
| `patches/agent15_add_node_sources.patch.jsonl` | 17 non-destructive `set_node_properties` (dry-run validated) |
| `apply_reports/agent15_add_node_sources.patch.apply_report.{json,md}` | Dry-run proof (17 would_update / 0 errors) |
| `_agent15_work/*.json` | Intermediate: graph inventory, coverage, synthesis, findings, destructive proposals |

## Counts by verdict (7,898 rows)

PROVEN 5,983 · PARTIAL 861 · MISSING_EVIDENCE 786 · SCHEMA_VIOLATION 161 · DEAD_LINK 53 · UNVERIFIABLE 24 ·
CONTRADICTION 23 · UNSUPPORTED 5 · (parse artifact) 2.

## Coverage verdict (honest)

- **Element-level proof:** 6,213/15,457 rels (40.2 %) + 1,097/2,304 nodes (47.6 %).
- **Type/aggregate-level only:** 9,092 rels + 1,040 nodes (Agents 12 & 13 emitted group rows, not per element).
- **Genuine gaps (319):** 152 `VERBUNDEN_MIT_AKTEUR` edges + 167 sourced `Akteur` nodes — never verified.
- **Conclusion:** 100 % element coverage is **NOT** achieved; Definition-of-Done item 1 is unmet pending the R1
  re-dispatch. This is reported, not faked.

## 10 worst findings

1. `circular_berlin → kunst_stoffe_ev` (`VERBUNDEN_MIT_AKTEUR`, **UNSUPPORTED**) — DBU consortium inflated to a tie.
2. `kunst_stoffe_ev → material_mafia` (`VERBUNDEN_MIT_AKTEUR`, **UNSUPPORTED**) — page names only Material Mafia.
3. `rotordc → p_architecture_of_reuse_brussels` (`BETEILIGT_AN`, **UNSUPPORTED**) — page names Rotor, not RotorDC.
4. **18 dangling `Nachweisforderung`** (Agent 13 **CONTRADICTION**) — e.g. `nf_oekobilanz_epd` demanded ×67,
   satisfied ×0; the compliance graph asks for proofs nothing can supply.
5. **152 unverified `VERBUNDEN_MIT_AKTEUR`** (UK steel, Finnish precast, project teams) — the fabrication-prone
   class, entirely outside the campaign so far.
6. **167 sourced `Akteur` nodes** never element-verified (gap between Agents 01–06 and 08).
7. **All 22 `Materialdepot` nodes have 0 sources** (Agent 10) — structural red flag confirmed.
8. **88 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs** (Agent 14) — dedup regression.
9. **431 unsourced `Akteur`** (Agent 08 MISSING_EVIDENCE) — provenance debt long tail.
10. **Property-key drift** — node keys 83 vs approved 57, rel keys 51 vs approved 22; approved-key ledger and
    `AGENTS.md` "Aktueller Stand" need re-baselining.

## Anomalies / data-quality notes on the source ledgers

- Agents 12 & 13 are **aggregate** ledgers (32 / 47 rows) rather than per-element — valid Tier-C method but it
  caps element-level coverage; flagged in `COVERAGE_PROOF.md` §6.
- 2 source rows were column-shifted by an unescaped comma (Agent 13 `A13-node-pn-0001`; Agent 14 `A14-INV` row) →
  surfaced as `(blank)`/`false` verdicts; underlying findings preserved in `notes`.

## Escalated to human

215 ESCALATE_HUMAN rows — chiefly the 18 dangling requirements (logic), all unsourced Materialdepots, 3 orphan
actors + 8 orphan vocab stubs (deprecate-vs-name), the `NUTZT_BAUWERK` singleton normalization, and the
schema-key re-baseline. See `REMEDIATION_PLAN.md` §5/§7.

## One-paragraph summary

The graph is largely proven (5,983 PROVEN; complete element-level coverage of every regulation `source_url` edge,
all geo/participation edges, and the law layer), and fabrication is contained to **3** consortium-inflation edges
with **no** resurrection of the purged 29. The genuine work left is a **319-element coverage gap** (non-bubble
actor networks — same risky class as the original fabrications), **18 dangling compliance requirements**, a large
**provenance debt** (532 missing sources incl. every Materialdepot, 88 bidirectional duplicates, 450 weak geo
URLs), and **per-edge attestation for 9,092 Tier-C edges** if that is required. The single most important next
action is the **R1 re-dispatch** to verify the 152 unverified `VERBUNDEN_MIT_AKTEUR` edges and 167 sourced actors
before the campaign is accepted as complete.
