# Verifier Agent 05 — Netherlands cluster — Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; no mutations performed)
**Agent:** 05 — Netherlands reuse cluster
**Ledger:** [`ledger/agent_05.csv`](../ledger/agent_05.csv)

## Scope recap

- Relationships tagged `review_run='netherlands_reuse_bubble_2026_06_05'` → **1** edge.
- Cluster nodes: `madaster`, `insert_marketplace`, `new_horizon_urban_mining`, `repurpose`, `superuse_studios_2012architecten`, `madaster_epea`, `city_of_utrecht` → **7** nodes.
- All surviving relationships touching those nodes (both directions), with explicit regression check that the **13 Tier-1 deleted Dutch/Madaster mesh edges** (per `2026-06-06_cross_bubble_extension/EVIDENCE_AUDIT.md`) have **not** resurrected.
- Special checks: `oogstkaart_lineage` (New Horizon→Superuse), Insert↔Madaster partnership, Madaster↔EPEA.

## Counts by verdict

| Verdict | Count |
|---|---:|
| PROVEN | 11 (7 nodes + 3 evidence-backed rels + 1 regression check) |
| MISSING_EVIDENCE | 4 (legacy unsourced `madaster↔rau` / `madaster↔thomas_rau` edges) |
| SCHEMA_VIOLATION | 1 (`repurpose` orphan) |
| **Total ledger rows** | **16** |

Proposed actions: 9× KEEP, 2× ESCALATE_HUMAN (unsourced legacy edges), 2× MERGE_DUPLICATE (bidirectional pairs), 1× ESCALATE_HUMAN (orphan). No DELETE proposed — all surviving evidence-backed edges are genuinely PROVEN.

## Headline finding

**No regression.** Every one of the 13 deleted Dutch/Madaster mesh edges remains absent from the live graph. A targeted `UNWIND` of all 13 endpoint pairs against `VERBUNDEN_MIT_AKTEUR` returned **0 rows**. The earlier purge held.

## The three special-check survivors — all PROVEN (both endpoints named)

1. **`new_horizon_urban_mining → superuse_studios_2012architecten`** (`oogstkaart_lineage`)
   - URL: `superuse-studios.com/publication/oogstkaart-nl-adopted-by-new-horizon/` (HTTP 200).
   - Quote: *"New Horizon will continue the activities of Oogstkaart B.V. as of 2020, with Superuse continuing to provide Oogstkaart's materialisation advice."*
   - The page is Superuse's own publication and names both parties; the lineage claim is exact. ✅

2. **`insert_marketplace → madaster`** (`formal_partnership`)
   - URL: `madaster.com/inspiration/partnership-between-insert-and-madaster/` (HTTP 200).
   - Quote: *"Insert ... and Madaster Services signed a partner agreement, today."*
   - Page is the signed Insert–Madaster partnership announcement (Jan 2019). ✅

3. **`madaster → madaster_epea`** (`platform_family`)
   - URL: `madaster.com/inspiration/epea-and-madaster-simplify-measuring-circularity-within-the-built-environment/` (HTTP 200).
   - Quote: *"EPEA and Madaster have joined forces to provide insight into the circularity of building components and materials"* / *"EPEA has therefore developed a database of materials and products especially for Madaster."*
   - Both endpoints named; data-integration partnership confirmed (Sep 2022). ✅

All 7 cluster nodes were also independently confirmed to exist with their cited attributes (see ledger NL-node-001…007).

## Anomalies / worst findings

1. **`repurpose` is now a fully orphaned node (degree 0).** SCHEMA_VIOLATION. Repurpose is a real Dutch reuse-advisory firm (`repurpose.nl`, "organiseert hergebruik sinds 2012", developer of the **Madopt** marketplace), but every edge it once had was a Tier-1 deleted mesh edge. It is currently disconnected from the graph. → **ESCALATE_HUMAN**: either re-source a real relationship (e.g. `repurpose → madopt`/Madopt platform, which is well-evidenced on repurpose.nl) or `DEPRECATE_NODE`. Also falls under Agent 14's global orphan scan.

2. **Legacy unsourced `madaster ↔ rau` and `madaster ↔ thomas_rau` edges (4 rows).** These untagged `VERBUNDEN_MIT_AKTEUR` edges carry no `evidence_url`/`source_url`. The underlying fact is plausible (Thomas Rau / RAU Architects co-founded the Madaster Foundation), but the edges are unproven on-graph → **MISSING_EVIDENCE / ADD_SOURCE**. The `thomas_rau` node already cites a relevant `madaster.com` article that could anchor a re-source.

3. **Bidirectional duplication.** Both `madaster→rau` **and** `rau→madaster` exist (likewise `madaster↔thomas_rau`). These are reciprocal `VERBUNDEN_MIT_AKTEUR` pairs that the earlier dedup should have collapsed → **MERGE_DUPLICATE** (flag for Agent 14 / Aggregator).

4. **Possible node duplication `rau` vs `thomas_rau`.** Both `:Akteur`, both share `source_urls=[thomasrau.eu/en]`, names "RAU" and "Thomas Rau" — likely the same architect/firm modelled twice. Recommend human review for `MERGE_DUPLICATE`. (Nodes themselves are outside Agent 05's named scope — flagged for the Aggregator / Agent 06/08.)

5. **`madaster_epea` composite naming.** The node name "Madaster / EPEA" conflates two distinct organisations (Madaster platform + EPEA/Drees & Sommer database). The edge `madaster→madaster_epea` is well-evidenced, but the node would be clearer split or renamed to `epea`. Low priority; noted for human review.

## Escalated to human

- `repurpose` orphan → reconnect-with-evidence or deprecate.
- `madaster↔rau` / `madaster↔thomas_rau` unsourced edges → add source or remove; resolve bidirectional duplication; resolve `rau` vs `thomas_rau` node duplication.

## One-paragraph summary

Agent 05 verified 16 claims across the Netherlands cluster: **11 PROVEN** (7 node identities + the 3 special-check survivors, each with a fetched HTTP-200 page naming **both** endpoints + the no-regression check), **4 MISSING_EVIDENCE** (legacy unsourced `madaster↔rau`/`madaster↔thomas_rau` edges, also bidirectionally duplicated), and **1 SCHEMA_VIOLATION**. The single most important finding: **none of the 13 deleted Dutch/Madaster mesh edges have resurrected** — the purge held — and the only structural defect introduced is that **`repurpose` is now an orphan** (its sole edges were all deleted mesh edges), which should be re-sourced or deprecated by a human.
