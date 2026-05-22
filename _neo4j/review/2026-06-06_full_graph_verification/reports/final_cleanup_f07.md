# Final Cleanup F07 — Property-key re-baseline + AGENTS.md draft

**Date:** 2026-06-06T18:20:42.613269+00:00 · **Database:** `mit-bestand`
**Mode:** READ-ONLY Neo4j (`read-cypher` only; no property cleanup patches)
**Ledger:** [`ledger/final_cleanup_f07.csv`](../ledger/final_cleanup_f07.csv) — **131 rows**
**Reference manifest:** [`CLEANUP_APPLY_SUMMARY.md`](../../2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md) (approved **57/22**)

## Live export (read-cypher)

| Surface | Approved (2026-06-05 phase8) | Live now | Δ |
|---|---:|---:|---:|
| Node property keys | **57** | **81** | **+24** |
| Rel property keys | **22** | **50** | **+28** |
| Graph nodes | — | **2,263** | post-F1 (`rau_architects` merged) |
| Graph rels | — | **15,060** | |

Agent-14 scan (15-agent era) reported **83/51** distinct keys; live is now **81/50** (−2 node / −1 rel) after Q01 stray-key fixes and graph edits — F07 re-baselines against the canonical **57/22** manifest, not the Agent-14 snapshot.

## Classification histogram

| classification | node | rel | Σ |
|---|---:|---:|---:|
| KEEP | 57 | 22 | 79 |
| DOCUMENT_DRIFT | 19 | 26 | 45 |
| DEPRECATE | 5 | 2 | 7 |
| **Σ keys** | **81** | **50** | **131** |

## Drift buckets (intentional vs legacy)

| drift_bucket | Count | Action |
|---|---:|---|
| approved_phase8 | 79 | No patch; remains canonical baseline |
| intentional_post_p6 | 45 | Document in schema manifest; do **not** auto-drop |
| legacy_residual | 7 | Candidate for future property patch (human-gated) |

### Notable DOCUMENT_DRIFT clusters

- **Geo intake:** `latitude`, `longitude`, `adresse`, `geo_*` (6 node keys)
- **Entwurfsqualität:** `entwurfsbeschreibung*`, `entwurfsqualitaet_*` + 11 rel keys (`begruendung`, `zuordnung_*`, …)
- **Reuse bubbles / VMA:** `evidence_*`, `connection_kind`, `dedup_run`, `review_run`, `dossier_section`, …
- **Sidecar pointers:** `metadata_sidecar_key` on nodes (741) and rels (505) — legacy cleanup 4b/5b scope per `AGENTS.md`
- **P6 evidence:** `primary_source_url` on nodes (re-introduced after phase5 drop)

### DEPRECATE residuals (7 keys, no F07 patch)

| scope | key | occ | rationale |
|---|---|---:|---|
| node | `land` | 5 | redundant Akteur scalar; canonical pattern is LIEGT_IN_LAND (A14-LAND-001) |
| node | `review_run` | 22 | node-level run tag; bubble tagging lives on relationships |
| node | `review_status` | 17 | legacy QA key; offloaded in property cleanup 4b |
| node | `short_description` | 1 | singleton stray key (1 node) |
| node | `source_scope` | 22 | obsolete since 2026-06-01; target drop from PROPERTY_CLEANUP_PLAN |
| rel | `review_status` | 69 | legacy QA; phase 4b target was 0 remaining |
| rel | `source_scope` | 69 | legacy scope tag; phase 4b/5b offload |

## SCOPE_CYPHER (repro)

```cypher
MATCH (n) UNWIND keys(n) AS k RETURN DISTINCT k AS key, 'node' AS scope ORDER BY key
```

```cypher
MATCH ()-[r]->() UNWIND keys(r) AS k RETURN DISTINCT k AS key, 'rel' AS scope ORDER BY key
```

## AGENTS.md §Aktueller Stand — draft block

> **Not applied to `AGENTS.md` by F07** — F10 applies final counts after F09 ledger merge. Insert/replace when PROVEN% and element row count are final.

```
## Aktueller Stand (2026-06-06) — F07 draft (pending F10 closeout)

Der Regulation-Graph-Vocabulary-Cleanup (Plan:
[`PLAN_V3.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/PLAN_V3.md))
ist bis Phase 8 + **Phase B (Variant B, 11 typed law labels)** angewendet, danach Abschluss-OP S1–S5
([`LAST_SURGERY_REPORT.md`](_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/LAST_SURGERY_REPORT.md)):
alle Schadstoff-/Regelungskanten belegt, 30 Bauteilgruppen verbunden, Dubletten/Waisen bereinigt.
Aktiver Graph-Stand in `mit-bestand`: **2,263 Knoten / 15,060 Relationen** (nach Final-Cleanup F1 `rau` merge;
Element-Ledger + PROVEN% werden von F10 nach F09-Re-Merge finalisiert — Platzhalter bis dahin).
Vor Final Cleanup (P6-06): 2 264 / 15 063 — **89,27 % PROVEN** auf 17 327 Zeilen —
[`POST_QUALITY_CAMPAIGN_REPORT.md`](_neo4j/review/2026-06-06_full_graph_verification/POST_QUALITY_CAMPAIGN_REPORT.md).
Property-Cleanup 2026-06-05: **57 Knoten-Property-Keys** (war 107), **22 Rel-Property-Keys** (war 63) —
[`CLEANUP_APPLY_SUMMARY.md`](_neo4j/review/2026-06-05_post_migration_property_cleanup/CLEANUP_APPLY_SUMMARY.md);
**live property-key drift dokumentiert (F07): 81 node / 50 rel** vs approved 57/22
(45 intentional drift, 7 legacy residuals) —
[`reports/final_cleanup_f07.md`](_neo4j/review/2026-06-06_full_graph_verification/reports/final_cleanup_f07.md).
Agent-14-Historie 83/51 → **81/50 live** (Q01 stray-key fixes + keine Property-Patches in F07).
```

## Acceptance

- [x] Row count = **131** (81 node + 50 rel live keys)
- [x] READ-ONLY Neo4j (no `write-cypher`, no property patches)
- [x] Each live key classified `KEEP` | `DOCUMENT_DRIFT` | `DEPRECATE`
- [x] Approved manifest cross-walk documents **57/22 → 81/50** drift
- [ ] `AGENTS.md` commit deferred to F10 closeout
