# Reuse Taxonomy Integration — Final Plan

**Date:** 2026-06-03
**Status:** Finalized. Ready for execution.
**Live graph reference:** [2026-06-03_graph_schema_full_export_mit-bestand](../2026-06-03_graph_schema_full_export_mit-bestand/) — fresh full backup (5,476 nodes / 24,017 rels). `:DataIssue` already cleaned (was 28,729, now 0).

---

## Decisions locked in

| # | Decision | Source |
|---|---|---|
| 1 | Batches are the source of truth for the 5 reuse vocab axes (Methode, Aufbereitungsverfahren, Ressourcenquelle, WiederverwendungsArt, Rueckbauverfahren) and for `:Bauteilgruppe` evidence. | User |
| 2 | Use existing `:Ressourcenquelle` label (no `:Herkunft`). Replace its 16 nodes with 6 new canonical matching batch buckets. | User |
| 3 | Hard-delete 13 `:Methode` originals → replace with 6 new canonical. Migrate 74 non-replaceable upstream edges (`:Akteur`, `:Software`, `:Tool`, `:Norm`). | User |
| 4 | Hard-delete 62 `:Aufbereitungsverfahren` originals → replace with 6 new canonical. Migrate 40 `:ReuseRule` edges + 47 outbound (`TYPISCH_BEI_MATERIAL`, `BELEGT_IN`). | User |
| 5 | `:WiederverwendungsArt` retires entirely. 11 nodes hard-deleted. 604 edges deleted. Constraint dropped. | User |
| 6 | `:Rueckbauverfahren`: keep 4 matching nodes, add 2 new canonical, hard-delete `rv_betonfraesen`. | Analysis |
| 7 | Include Batch 01 markdown (139 rows; K118 + MedUni covered). Total batch rows 2,240. | User |
| 8 | **`:Bauteilgruppe` label scope tightened to `bg_reuse_*` only.** Batches are canonical for that scope. Skip the manual resolver. 273 exact-match BGs stay (same node, batch evidence attached). 29 `needs_review` pairs auto-confirm (live stays, batch evidence attached). 24 batch-only `bg_reuse_*` candidates created as new nodes. **35 `bg_reuse_*` live BGs without a batch match are hard-DELETED** (replaced by batches). **All 35 live `bg_retained_*` / `bg_planned_*` / `bg_dismantled_*` are also hard-DELETED** — they don't semantically belong to `:Bauteilgruppe` (existing buildings, design intent, dismantled components are different research dimensions). **85 batch rows anchoring on non-`bg_reuse_*` BGs are filtered out in Phase 2.** | User (2026-06-03 followups) |
| 9 | No `:*_Legacy` labels anywhere. | User |
| 10 | DataIssue cleanup not needed in this run — already done. | Fresh schema export |

---

## Before vs after — node and edge counts

```
                              BEFORE     →     AFTER     Change
:Methode                          13          6  (all new)        -7
:Aufbereitungsverfahren           62          6  (all new)       -56
:Ressourcenquelle                 16          6  (all new)       -10
:Rueckbauverfahren                 5          6                   +1
:WiederverwendungsArt             11          0  (label retires) -11
:Wiederverwendungsergebnis         -          6  (brand new)      +6
:Wiederverwendungsort              -          6  (brand new)      +6
:Bauteilgruppe                   350        304  (−35 −35 +24)   -46
                                              (35 bg_reuse_ orphans deleted,
                                               35 non-reuse out-of-scope deleted,
                                               24 batch-new bg_reuse_ created)

HAT_METHODE                      654   ≈   ~298  (rerouted/new)
HAT_AUFBEREITUNG                 433   ≈   ~283
HAT_RESSOURCENQUELLE             552   ≈   ~380
HAT_WIEDERVERWENDUNGSART         604   →      0  (rel retires)
HAT_RUECKBAUVERFAHREN            299   ≈   ~136
HAT_ERGEBNIS                       0   →   ~423  (new axis)
HAT_WIEDERVERWENDUNGSORT           0   →   ~367  (new axis)
ANGEWENDET_AUF                     0   →    ~14  (new rel)
TYPISCH_BEI_MATERIAL              22   →    ≤22  (rerouted + dedupe)
BELEGT_IN (from :Aufbereitung)    25   →    ≤25  (rerouted + dedupe)
```

---

## Phase order (final)

| Phase | What | Touches graph? |
|---|---|---|
| 0 | Snapshot + DB dump (already have [2026-06-03 full export](../2026-06-03_graph_schema_full_export_mit-bestand/)) + pre-deletion scan + relabel `:Projekt`-with-`prog_*` ids | Read + tiny label fix |
| 1 | All decisions locked (done) | No |
| 2 | Normalize batch Markdown: rel aliases (`HAS_METHOD`→`HAT_METHODE`, `HAT_QUELLE`→`HAT_RESSOURCENQUELLE`, etc.), out-of-vocab labels, parser errors | No (Markdown only) |
| 3 | **Skipped** — vocabulary lookup map only (`vocabulary_id_map.csv`); BG resolver not needed | No |
| 4 | Create constraints + 6+6+6 vocab canonical + 6+6 new-axis seed nodes + 2 new `:Rueckbauverfahren` | Add only |
| 5 | Stage Cypher per batch: MERGE Bauteilgruppen (creates 57 new, no-op on 273 existing); attach all evidence edges to BGs/Projekts per `vocabulary_id_map.csv` | Add only |
| 6 | Migrate non-replaceable upstream edges → new canonical; delete old vocab edges + nodes (see Phase 6 detail) | Reroute + Delete |
| 7 | Run [verify_integration.cypher](verify_integration.cypher); all checks pass before sign-off | Read only |

---

## Phase 6 — detailed retirement (final)

Driven by [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md). DataIssue trimming step REMOVED (already done).

| Action | Edges touched | Detail |
|---|---:|---|
| **MIGRATE** `:Akteur/:Software/:Tool/:Norm/:Programm → :Methode` | 74 | Reattach to new canonical with `legacy_methode_id`/`legacy_methode_name` provenance, then delete the old edge |
| **MIGRATE** `:ReuseRule → :Aufbereitungsverfahren` | 40 | Same pattern, `legacy_aufbereitung_*` |
| **MIGRATE + DEDUPE** `:Aufbereitungsverfahren →[TYPISCH_BEI_MATERIAL]→ :Material` | 22 | Reattach to new canonical's outbound; MERGE dedupes |
| **MIGRATE + DEDUPE** `:Aufbereitungsverfahren →[BELEGT_IN]→ :Quelle:ResearchDocument` | 25 | Same |
| **MIGRATE** `:Materialdepot → :Ressourcenquelle` | 1 | Reattach to new canonical |
| **DELETE** `:Bauteilgruppe/:Projekt → :Methode` | 591 | Batches re-supply at row level |
| **DELETE** `:Bauteilgruppe/:Projekt → :Aufbereitungsverfahren` | 433 | Batches re-supply |
| **DELETE** `:Bauteilgruppe/:Projekt → :Ressourcenquelle` | 551 | Batches re-supply |
| **DELETE** `:Bauteilgruppe/:Projekt → :WiederverwendungsArt` | 604 | Axis retires |
| **DELETE** `:Bauteilgruppe → :Rueckbauverfahren` | 299 | Batches re-supply |
| **DELETE** old vocab nodes | 13 + 62 + 16 + 11 + 1 = 103 | After edges resolved, all old `meth_*` + `av_*` + `rq_*` + `wva_*` + `rv_betonfraesen` hard-deleted |
| **DROP** constraint `wiederverwendungsart_id` | — | Axis retired |

Total: ~115 edges migrated, ~2,478 edges deleted, 103 old vocab nodes deleted.

---

## Bauteilgruppe handling — what changed (final)

The batches are canonical on the `bg_reuse_*` axis. Live BGs without a batch slug match get **replaced** by the batch's evidence-backed set; live BGs that are outside batch scope (`bg_retained_*` / `bg_planned_*` / `bg_dismantled_*`) stay untouched.

### Per-bucket disposition (from [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv))

| Bucket | Live BGs | Batch BGs | Action |
|---|---:|---:|---|
| Exact slug match, both `bg_reuse_*` | ~251 | ~251 | **KEEP live node**, batch rows MERGE evidence on top |
| Exact slug match, non-reuse prefix (retained/planned/dismantled) | 22 | 22 | **DELETE live node** + **DROP batch rows** — out of `:Bauteilgruppe` semantic scope |
| `needs_review` pairs `bg_reuse_*` (algorithm 0.35–0.65) | 29 | 29 | **Auto-confirm** — KEEP live node, batch rows MERGE evidence. Skipping review per user instruction. |
| `no_batch_equiv` `bg_reuse_*` | 35 | — | **DELETE live node** and its edges (replaced by batches' canonical set). |
| `no_batch_equiv` non-reuse prefix | 13 | — | **DELETE live node** — out of `:Bauteilgruppe` semantic scope. |
| `new_candidate` `bg_reuse_*` | — | 24 | **CREATE** as new `:Bauteilgruppe` node with `bg_kind = partial_batch` |
| `new_candidate` non-reuse prefix + `bg_candidate_*` | — | 4 | **SKIP** — out of `:Bauteilgruppe` semantic scope |

### Net BG count

```
Before                          350
+ batch-only bg_reuse_ created  +24
− bg_reuse_ orphans deleted     −35
− non-reuse (retained/planned/dismantled) deleted   −35
= After                         304   (all bg_reuse_*)
```

### Batch row filter

Phase 2 (Markdown normalization) filters out **85 batch rows (4.9% of 1,734)** that anchor on non-`bg_reuse_*` BGs. These rows would otherwise create evidence edges to nodes we're deleting. Move filtered rows to `_filtered_non_reuse_bgs.md` for transparency; do not delete from history.

Examples of dropped batch findings:
- ELEMENTA Brettstapel laminated-timber ceiling design intent (`bg_planned_*`)
- LysP8 Design-for-Disassembly timber frame (`bg_planned_*`)
- Circl Tarkett C2C planned floor (`bg_planned_*`)
- Elys / Grande Halle / Botanique retained concrete structures (`bg_retained_*`)
- Circl dismantled larch structure (`bg_dismantled_*`)
- MedUni Mariannengasse retained Art Nouveau ceiling (`bg_retained_*`)

These are real findings dropped because they aren't `:Bauteilgruppe` semantically — they're a different research dimension (existing building stock, design intent, dismantled components).

### What gets lost when we delete 70 BGs total (35 reuse orphans + 35 non-reuse)

Per BG, on average:
- Property bag: `reuse_status`, `bg_kind`, `alte_funktion`, `neue_funktion`, `tragend`, name
- Outbound edges (counted across all 70): roughly 70-100 `NUTZT_MATERIAL`, 70-100 `HAT_BAUTEILTYP`, 70-100 `HAT_MATERIALGRUPPE`, plus Schadstoff/Huerde/Prozessphase/Leistungsanforderung/Logistik/Marktmodell/Bauteilebene
- Evidence URLs (`BELEGT_IN → :Quelle`): ~3 per BG = ~210 total
- `(:Projekt)-[:HAT_BAUTEILGRUPPE]->` anchor: 70 edges
- 85 batch rows that would have created new evidence on the non-reuse BGs

Total: roughly **600–800 non-vocab edges + 70 property bags + 85 batch findings** removed.

User's rationale (decision #8): the batches are better-quality evidence than the auto-tagged controlled-vocab placeholders that live on these orphan BGs (per [RICHNESS_AUDIT.md](RICHNESS_AUDIT.md), 91-100% of those non-vocab edges are `topology_synthesized` with `evidence_confidence: unklar`). The non-reuse BGs additionally don't belong semantically to `:Bauteilgruppe`. The trade-off is consistent with the same "batches replace placeholders, clean semantic scope" logic that retires the 5 vocab axes.

**Alternative if data preservation matters more:** relabel the 35 non-reuse live BGs to dedicated labels (`:Bestand` / `:GeplantesBauteil` / `:Dekonstruktion`) instead of deleting. Preserves all 600+ non-vocab edges and the 85 batch findings. Not the current plan; flag if you want to switch.

### Slug-drift redirection (informal)

Some of the 35 orphan deletions are the live side of a slug-drift pair where the batch side ends up in `new_candidate`. E.g. BlueCity:
- Delete: `bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende` (live, generic slug)
- Create: `bg_reuse_glas_innenwand_bluecity_reused_window_frames` (batch, evidence-backed)

The new batch node carries the same physical-component meaning but with proper material/bauteiltyp typing and `belegt`-tier source. The replacement is exactly what "batches replace old" means in practice.

The Phase 3.2 resolver artifacts ([bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv), [bauteilgruppe_resolver_review.md](bauteilgruppe_resolver_review.md), [RESOLVER_USAGE.md](RESOLVER_USAGE.md)) are preserved for future cleanup; not required for execution.

---

## What we lose / gain

### Lose
- 2,459 old vocab edges with `evidence_origin: topology_synthesized` and `evidence_confidence: unklar` (per [RICHNESS_AUDIT.md](RICHNESS_AUDIT.md)). These were placeholders flagged `needs_source_url_review`; not curated knowledge.
- 11 `:WiederverwendungsArt` nodes (replaced by `:Wiederverwendungsergebnis` + `:Wiederverwendungsort` + `:Methode` split).
- 13 `:Methode` originals (folded into 6 new canonical, upstream edges preserved).
- 62 `:Aufbereitungsverfahren` originals (folded into 6 new canonical).
- 16 `:Ressourcenquelle` originals (replaced with 6 new canonical).

### Keep (unchanged)
- All 86 `:Projekt` nodes and properties.
- All 350 live `:Bauteilgruppe` nodes — full property bag (`reuse_status`, `bg_kind`, `alte_funktion`, `neue_funktion`, `tragend`), all evidence URLs (`BELEGT_IN`), all non-vocab edges (HAT_BAUTEILTYP, NUTZT_MATERIAL, HAT_MATERIALGRUPPE, HAT_SCHADSTOFF, HAT_HUERDE, HAT_PROZESSPHASE, HAT_LEISTUNGSANFORDERUNG, HAT_LOGISTIK, HAT_MARKTMODELL, HAT_BAUTEILEBENE, INTO_RECEIVER, FROM_DONOR, etc.).
- All `:Akteur`, `:Software`, `:Tool`, `:Norm`, `:ReuseRule`, `:Materialdepot`, `:Programm` upstream connections to the vocab axes (rerouted to new canonical, provenance preserved).

### Gain
- ~2,240 evidence-backed batch rows materialized as new edges, each carrying `evidence_url`, `evidence_quote`, `evidence_confidence ∈ {belegt, wahrscheinlich, unsicher}`.
- New `:Wiederverwendungsergebnis` axis (6 canonical) — replaces the outcome dimension of the retired `:WiederverwendungsArt`.
- New `:Wiederverwendungsort` axis (6 canonical) — replaces the location dimension.
- New `ANGEWENDET_AUF` relationship for `:Methode → :Bauteilgruppe` (~14 edges).
- ~57 new `:Bauteilgruppe` nodes covering components the live graph didn't have (e.g. K118's Orion-donor granite facade and external stair, Ferme du Rail's textile sun-shading, etc.).

### Net evidence-confidence shift
Before: ~2,459 edges at `unklar` confidence (placeholders).
After: ~1,997 edges at `belegt`/`wahrscheinlich` + ~243 at `unsicher`. **From ~0 evidence-backed to ~2,000.**

---

## Rollback

- Phase 4 + 5 (additive) → rollback by `MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]-() DELETE r` + delete new seed nodes
- Phase 6 (destructive) → only path back is restore from [2026-06-03 full backup](../2026-06-03_graph_schema_full_export_mit-bestand/live_graph.backup.jsonl)
- Procedure: do not start Phase 6 until Phase 5 verifies green AND the Phase 0 backup is confirmed restorable on a clone.

---

## All companion docs (current status)

| Doc | Status |
|---|---|
| [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md) | Updated to reflect skip-resolver decision |
| [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md) | Authoritative for Phase 6 edge actions (unchanged; still accurate) |
| [SEMANTIC_CONFLICT_AUDIT.md](SEMANTIC_CONFLICT_AUDIT.md) | Decisions table reflects final state |
| [RICHNESS_AUDIT.md](RICHNESS_AUDIT.md) | Evidence that old vocab edges are mostly placeholders — unchanged |
| [BAUTEILGRUPPE_COMPARISON.md](BAUTEILGRUPPE_COMPARISON.md) | Updated: marks resolver as deferred / informational |
| [RESOLVER_USAGE.md](RESOLVER_USAGE.md) | Marked as optional / informational — not blocking |
| [WHATS_HAPPENING.md](WHATS_HAPPENING.md) | Plain-language summary updated |
| [verify_integration.cypher](verify_integration.cypher) | DataIssue checks dropped; slug-duplicate cost surfaced as info |

---

## Next step

When you're ready, the implementation order is:

1. **Phase 0.4**: detect `:Projekt` nodes with `prog_*` ids (3 expected) and relabel to `:Programm`. Trivial Cypher.
2. **Phase 2**: normalize batch Markdown (alias rel-types and out-of-vocab labels) per [INTEGRATION_PLAN.md §P2.1–P2.3](INTEGRATION_PLAN.md).
3. **Phase 3.3**: build [vocabulary_id_map.csv](vocabulary_id_map.csv) — small lookup (one row per old `wva_*`/`meth_*`/`av_*`/`rq_*` → new canonical).
4. **Phase 4 + 5 + 6**: generate and stage Cypher per [INTEGRATION_PLAN.md](INTEGRATION_PLAN.md). Roughly one Cypher file per batch + one Phase 6 cleanup file.
5. **Phase 7**: [verify_integration.cypher](verify_integration.cypher).

Want me to start Phase 0.4 (relabel `prog_*` projects) and Phase 2 (Markdown normalization) — both safe, non-destructive — to keep momentum?
