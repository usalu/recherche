# Final Cleanup F6 — Property re-baseline + presentation sync

**Agent:** F6  
**Database:** `mit-bestand` (READ-ONLY)  
**Date:** 2026-06-06  
**Ledger:** [`ledger/final_cleanup_f06.csv`](../ledger/final_cleanup_f06.csv) — **131 rows** (81 node keys + 50 rel keys)

## Scope

1. Live property-key audit vs approved **57/22** manifest (`CLEANUP_APPLY_SUMMARY.md`, phase 8).
2. Sync reuse presentation decks with live graph counts and VMA statistics.
3. Fix stale **78-links** claim (pre-remediation bubble era).
4. Draft `AGENTS.md` §Aktueller Stand updates for F7 closeout (not applied here).

**No graph mutations.** No property cleanup patches.

---

## Live graph headline (read-cypher 2026-06-06)

| Surface | Live | Prior stale refs |
|---|---:|---|
| Nodes | **2,263** | 2,304 (15-agent era) |
| Relationships | **15,060** | 15,457 / 15,486 |
| Σ elements | **17,323** | 17,327 (pre-F1) |

F1 `rau_architects` merge is already reflected (2263 nodes). Rel count −3 vs planning baseline 15,063 — consistent with post-plan edge hygiene; F7 should re-export elementIds.

---

## VMA statistics (reuse deck numbers)

```cypher
MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]-()
RETURN count(r) AS vma_undirected,
       count(CASE WHEN r.review_run IS NOT NULL THEN 1 END) AS vma_tagged,
       count(CASE WHEN r.evidence_confidence = 'belegt' THEN 1 END) AS vma_belegt,
       count(CASE WHEN r.evidence_confidence = 'teilweise_belegt' THEN 1 END) AS vma_teilweise
```

| Metric | Undirected | Directed (`->`) |
|---|---:|---:|
| Tagged (`review_run IS NOT NULL`) | **132** | **66** |
| `belegt` | **114** | **57** |
| `teilweise_belegt` | **18** | **9** |
| Missing `evidence_url` (tagged) | **0** | **0** |

**Stale claim fixed:** decks cited **78** connections from the pre–evidence-audit bubble import. Live directed tagged count is **66** after Tier-1/Tier-2 removals (`EVIDENCE_AUDIT.md`) plus post-quality additions (`agent_06b`, `post_quality_p06_02`, `quality_pass_q05`, `remediation_wave2_r04`).

### Directed connections by `review_run`

| `review_run` | connections |
|---|---:|
| `swiss_reuse_bubble_2026_06_05` | 14 |
| `germany_reuse_bubble_2026_06_05` | 13 |
| `cross_bubble_extension_2026_06_06` | 9 |
| `agent_06b_non_bubble_actor_networks_2026_06_06` | 9 |
| `post_quality_p06_02_2026_06_06` | 9 |
| `france_reuse_bubble_2026_06_05` | 6 |
| `rotor_dc_reuse_bubble_2026_06_05` | 3 |
| `netherlands_reuse_bubble_2026_06_05` | 1 |
| `quality_pass_q05_2026_06_06` | 1 |
| `remediation_wave2_r04_2026_06_06` | 1 |

---

## Presentation decks updated

| File | Changes |
|---|---|
| [`PRESENTATION_REUSE_SYNTHESIS.md`](../../2026-06-06_cross_bubble_extension/PRESENTATION_REUSE_SYNTHESIS.md) | Header stats; Cirkla hub 16→11 partners |
| [`PRESENTATION_REUSE_NETWORKS.md`](../../2026-06-06_cross_bubble_extension/PRESENTATION_REUSE_NETWORKS.md) | 78→66/132/114; bubble table; hub ranking; mechanism breakdown; appendix cheat-sheet; graph 2263/15060; new `review_run` tags |

Speaker convention: **directed** counts for “connections”; **undirected** for evidence totals matching plan SCOPE_CYPHER.

---

## Property-key re-baseline

| Surface | Approved (2026-06-05) | Live | Δ | Agent-14 prior |
|---|---:|---:|---:|---:|
| Node keys | **57** | **81** | **+24** | 83 |
| Rel keys | **22** | **50** | **+28** | 51 |

Ledger verdict histogram:

| Verdict | Node | Rel | Σ |
|---|---:|---:|---:|
| **KEEP** | 56 | 25 | 81 |
| **DOCUMENT_DRIFT** | 22 | 25 | 47 |
| **DEPRECATE** | 3 | 0 | 3 |
| **Total** | 81 | 50 | **131** |

### Intentional drift (DOCUMENT_DRIFT sample)

- **Nodes:** geo intake (`latitude`, `longitude`, `geo_*`, `adresse`, `country_iso2`); entwurfsqualitaet (`entwurfsbeschreibung*`, `entwurfsqualitaet_*`); vocab/intake (`name_de`, `vokabular_version`, `intake_run`, `deprecated_*`); sidecar pointer `metadata_sidecar_key`; intake evidence `primary_source_url`.
- **Rels:** reuse bubbles (`connection_kind`, `dedup_run`, `dedupe_key`, `evidence_excerpt`, …); entwurfsqualitaet (`begruendung`, `belegkonfidenz`, `integration_layer/phase`, `zuordnung_*`, …); dedup metadata (`basis_project_edge_id`, `shared_*_ids`).

### DEPRECATE candidates (no patch this wave)

| Key | Scope | Note |
|---|---|---|
| `land` | node | Redundant scalar vs `LIEGT_IN_LAND` (A14-LAND-001) |
| `review_status` | node | Legacy QA marker |
| `source_scope` | node | Dropped in phase 8; residual occurrences |

---

## AGENTS.md draft (for F7)

Replace §Aktueller Stand graph line with:

> Aktiver Graph-Stand in `mit-bestand`: **2,263 Knoten / 15,060 Relationen** → **17,323 Elemente** (read-cypher 2026-06-06, post-F1 rau merge). Property keys live **81/50** vs approved **57/22** — re-baselined in [`reports/final_cleanup_f06.md`](reports/final_cleanup_f06.md). Reuse presentation VMA backbone: **66 directed / 132 undirected tagged**, **114 belegt**.

PROVEN% and element ledger: **F7 recomputes** after F4 merge.

---

## Acceptance

| Check | Result |
|---|---|
| Ledger row count = 131 | ✅ |
| Presentation decks: no stale “78 links” | ✅ |
| Presentation decks: live graph headline | ✅ |
| READ-ONLY Neo4j | ✅ |
| Property cleanup patches | none (by design) |

---

*Builder script (read-only): [`_f6_build_ledger.py`](../_f6_build_ledger.py)*
