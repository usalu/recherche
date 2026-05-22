# Regulation graph vocabulary — run index

**Run:** `regulation_graph_vocab_2026_06_04` · **Status: COMPLETE** (migration + finishing surgery applied
to live `mit-bestand`, 2026-06-05). This folder holds the plan, evidence, scripts and reports.

## Outcome (live graph now)
Evidence-first regulation layer on `mit-bestand`: **2 255 nodes · 15 235 rels · 51 labels · 48 reltypes.**
Sources are node/edge **properties** (no `Quelle` node); each standard is **one typed law node**
(`Tragwerksrecht`/`Schadstoffrecht`/… — domain-labelled, jurisdiction preserved); every regulation/
pollutant edge is sourced; generic `inferiert`/`unklar` edges retired. See `LAST_SURGERY_REPORT.md`.

## Canonical documents (read these)
- **`PLAN_V3.md`** — the canonical plan & locked model (sources=property, law=node).
- **`FINAL_AUDIT_REPORT.md`** — migration result (phases 0–8 + typed-law Variant B).
- **`LAST_SURGERY_REPORT.md`** — finishing pass (S1–S5): sourced the last 137 pollutant edges,
  connected 30 components, merged duplicates, deleted orphans; all acceptance gates green.
- **`VARIANT_B_TAXONOMY.md`** — the typed `…recht` law-label taxonomy.
- **`SEMANTIC_REVIEW.md`** — adversarial review that drove the final model.
- **`GRAPH_BLUEPRINT_DATA.md`** — per-label data + dispositions.

## Evidence & research (the sourced facts)
- `EVIDENCE_REGELWERK.md` — the researched standards with URLs+quotes.
- `POLLUTANT_ERA_EVIDENCE.md` — pollutant × era × component sourced matrix.
- `HUERDE_RESEARCH.md` — reuse-barrier taxonomy (Rakhshan 2020).
- `REWIRE_REVIEW.md` — old→new node mapping. `EXPLORER_QUERIES.md` — handy Cypher.

## Executable artifacts (reversible; dry-run→commit, tagged `review_run=…`)
- Migration: `phase0…phase8`, `phaseB_*` (+ `*_report.json` / `*_before.json` snapshots).
- Finishing surgery: `phase_s1_schadstoff_source.py`, `phase_s2_connect.py`, `phase_s3_orphans.py`.
- Build/connect/audit: `build_vocabulary_graph.py`, `connect_anchors_to_vocab.py`, `apply_to_graph.py`,
  `audit_edges.py`, `inspect_connections.py`, `rewire_map.py`, data `*.csv`/`*.jsonl`.
- Rollback: backup `_neo4j/review/backups/20260605T152248Z-mit-bestand` (pre-surgery) or restore phase snapshots.

## `_history/`
Superseded planning & intermediate-analysis docs (PLAN v1/v2, blueprints, proofs, audits) kept for the
decision trail. Not current — see the canonical list above.
