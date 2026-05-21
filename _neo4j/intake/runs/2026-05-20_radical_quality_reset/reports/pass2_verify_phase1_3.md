# Pass-2 Detailed Verification — Phase 1.3 (Propagated MARKTMODELL + dominant-edge removal)

- **Verifier:** Pass-2 Detailed Verifier 3 of 12 (read-only, no migrations executed)
- **Verified at:** 2026-05-21 (live `mit-bestand`, bolt://localhost:7687)
- **Plan reference:** `c:/Users/Kinosh/.cursor/plans/radical_quality-first_reset_8d1e2b66.plan.md`, section 1.3
- **Run directory:** `E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/`
- **Prior verifiers consulted:** `reports/agent_3_phase1_2_3_report.md`, `reports/final_verify_phase1_2_3.md`

---

## Overall verdict — **PASS (with one documented derivability caveat)**

Phase 1.3 is fully complete and intact:

- The migration script exists and is idempotent.
- The done-flag is parseable and matches the live post-state.
- The two old aggregation edge types (`HAT_DOMINANT_MARKTMODELL`, `HAT_DOMINANT_AKZEPTANZ`) are gone — both from edges and from the database type registry (`db.relationshipTypes()` no longer lists them).
- All 319 propagated `HAT_MARKTMODELL` edges carry the canonical `derived/propagated/bookkeeping` shape with `original_source_excerpt` preserved verbatim and `source_excerpt` removed.
- All 384 original `(Bauteilgruppe, Marktmodell)` pairs from the pre-Phase-1 snapshot are still present 1:1 in the live graph (Δ pairs = 0).
- 85 of the 86 deleted `HAT_DOMINANT_MARKTMODELL` projekt→mm claims are still re-derivable through `(Projekt)-[:HAT_BAUTEILGRUPPE]->(BG)-[:HAT_MARKTMODELL]->(MM)`.

**One caveat (not a Phase 1.3 execution defect):** the projekt→mm pair `p_elementa_walkeweg → mm_plattform_vermittelt` is no longer reachable through the BG path because that project's 4 Bauteilgruppen never carried any `HAT_MARKTMODELL` edge — neither in the snapshot nor today. The plan's re-derivability claim therefore fails for exactly 1 of 86 dominant-MM claims. Phase 1.3 was executed exactly as the plan specifies; this is a plan-side derivability gap, not a Phase 1.3 mis-execution.

A separate, plan-acknowledged loss exists for the 24 `HAT_DOMINANT_AKZEPTANZ` claims: there were 0 plain `HAT_AKZEPTANZ` edges in the snapshot and 0 today, so all akzeptanz aggregation information was deleted by Phase 1.3.c with no surviving fan-in. The migration header comment ("re-derivable from surviving HAT_AKZEPTANZ edges") is therefore inaccurate for AKZEPTANZ. Again, plan-side, not execution-side.

---

## Deep checks

### Check 1 — `migrations/mig_1_3_flag_propagated.cypher` present and idempotent — **PASS**

Path: `E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/migrations/mig_1_3_flag_propagated.cypher` (3 072 bytes, `2026-05-20T22:53` mtime). Three labelled sections matching the plan verbatim:

- **1.3.a** — `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.source_excerpt CONTAINS 'propagated'` → sets `evidence_origin='derived'`, `evidence_basis='propagated'`, `evidence_excerpt=NULL`, `evidence_confidence='bookkeeping'`, captures `original_source_excerpt` via `WITH … AS original_excerpt` (guards against ordering issues), then `REMOVE r.source_excerpt`.
- **1.3.b** — `MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->() DELETE r`.
- **1.3.c** — `MATCH ()-[r:HAT_DOMINANT_AKZEPTANZ]->() DELETE r`.

**Idempotency** (each statement is naturally re-runnable):

| stmt | re-run effect on live graph | why idempotent |
| --- | --- | --- |
| 1.3.a | matches 0 rows (the `WHERE r.source_excerpt CONTAINS 'propagated'` filter is empty because `source_excerpt` was REMOVEd) | filter excludes already-processed edges |
| 1.3.b | matches 0 rows (relationship type no longer exists in the database) | no edges of that type to delete |
| 1.3.c | matches 0 rows (relationship type no longer exists in the database) | no edges of that type to delete |

Re-running the file today would yield three statements each returning `count = 0` with zero side-effects — confirmed idempotent.

### Check 2 — `PHASE_1_3_DONE.flag` parseable — **PASS**

Path: `logs/PHASE_1_3_DONE.flag` (Agent 3 placed all 1.2/1.3 done-flags under `logs/`; consistent with `final_verify_phase1_2_3.md` gate 10). Valid JSON, fields:

```json
{
  "phase": "1.3",
  "completed_at": "2026-05-20T20:57:50+00:00",
  "before": {
    "hat_marktmodell_with_propagated_excerpt": 319,
    "hat_marktmodell_with_propagated_basis": 0,
    "hat_dominant_marktmodell": 86,
    "hat_dominant_akzeptanz": 24
  },
  "after": {
    "hat_marktmodell_with_propagated_excerpt": 0,
    "hat_marktmodell_with_propagated_basis": 319,
    "hat_dominant_marktmodell": 0,
    "hat_dominant_akzeptanz": 0
  }
}
```

The four Phase 1.3 in-scope counts in `after` (0 / 319 / 0 / 0) match the live measurements taken today exactly.

### Check 3 — `()-[:HAT_DOMINANT_MARKTMODELL]->()` == 0 — **PASS** (live = 0)

Cypher: `MATCH ()-[r:HAT_DOMINANT_MARKTMODELL]->() RETURN count(r)` → `0`.
Additional sanity: `CALL db.relationshipTypes() WHERE relationshipType STARTS WITH 'HAT_DOMINANT'` returns the empty set — the type itself has been retired from the database.

### Check 4 — `()-[:HAT_DOMINANT_AKZEPTANZ]->()` == 0 — **PASS** (live = 0)

Same as Check 3 — both count and type-registry are empty.

### Check 5 — `()-[:HAT_MARKTMODELL]->()` WHERE `evidence_basis='propagated'` in [310, 330] — **PASS** (live = exact 319)

Cypher: `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.evidence_basis='propagated' RETURN count(r)` → `319` (window: 310 ≤ 319 ≤ 330; matches the plan's pre-migration count exactly; matches `PHASE_1_3_DONE.flag.after.hat_marktmodell_with_propagated_basis` exactly).

### Check 6 — `()-[:HAT_MARKTMODELL]->()` WHERE `source_excerpt CONTAINS 'propagated'` == 0 — **PASS** (live = 0)

Cypher: `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.source_excerpt CONTAINS 'propagated' RETURN count(r)` → `0`. The literal template string `"propagated from project HAT_DOMINANT_MARKTMODELL (project-wide sourcing)"` has been excised from every `source_excerpt` slot and lives only in `original_source_excerpt` (see Check 7).

### Check 7 — Sample 10 propagated `HAT_MARKTMODELL` edges — **PASS** (10/10 canonical)

Sample (first 10 returned by the bare match):

| src_id | dst_id | evidence_origin | evidence_basis | evidence_confidence | source_excerpt | original_source_excerpt |
| --- | --- | --- | --- | --- | --- | --- |
| `bg_reuse_stahl_mehrere_55gss_external_core` | `mm_spende` | `derived` | `propagated` | `bookkeeping` | null | "propagated from project HAT_DOMINANT_MARKTMODELL (project-wide sourcing)" |
| `bg_reuse_mehrere_mehrere_alliander_common_roof_atrium` | `mm_spende` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_reuse_mehrere_mehrere_alliander_common_roof_atrium` | `mm_plattform_vermittelt` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_reuse_mehrere_mehrere_alliander_common_roof_atrium` | `mm_take_back_service` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_reuse_mehrere_ausbau_alliander_material_passport_inventory` | `mm_spende` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_reuse_mehrere_ausbau_alliander_material_passport_inventory` | `mm_plattform_vermittelt` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_reuse_mehrere_ausbau_alliander_material_passport_inventory` | `mm_take_back_service` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_retained_mehrere_mehrere_alliander_existing_buildings` | `mm_spende` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_retained_mehrere_mehrere_alliander_existing_buildings` | `mm_plattform_vermittelt` | `derived` | `propagated` | `bookkeeping` | null | same |
| `bg_retained_mehrere_mehrere_alliander_existing_buildings` | `mm_take_back_service` | `derived` | `propagated` | `bookkeeping` | null | same |

Full-population check (not just sample): `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.evidence_basis='propagated' AND (r.original_source_excerpt IS NULL OR r.original_source_excerpt='' OR r.source_excerpt IS NOT NULL OR r.evidence_origin <> 'derived' OR r.evidence_confidence <> 'bookkeeping') RETURN count(r)` → `0`. **All 319 propagated edges carry the canonical Phase-1.3 shape.**

### Check 8 — Non-propagated `HAT_MARKTMODELL` count + provenance distribution — **PASS** (with documented downstream reshape)

Cypher: `MATCH ()-[r:HAT_MARKTMODELL]->() WHERE r.evidence_basis<>'propagated' RETURN count(r)` → `65`. Distribution (single bucket — uniformity is itself notable):

| evidence_origin | evidence_basis | evidence_confidence | count |
| --- | --- | --- | ---: |
| `derived` | `legacy_migration` | `unklar` | 65 |

**Note about the 65:** The task description anticipated these would still look like "original belegt edges" with `curated/cell_citation/belegt` shape. They no longer do — every one of them now carries `derived/legacy_migration/unklar`. This is **not** a Phase 1.3 regression. Phase 1.3 explicitly left these 65 untouched (Agent 3's report records `"HAT_MARKTMODELL untouched (real excerpts) | 65"`). The reshape to `legacy_migration/unklar` was applied later by **Phase 4.1** (`mig_4_1_canonical_evidence.cypher`, ~22 KB, executed by Agent 7 around `2026-05-20T23:39`) as part of the cross-graph canonical-evidence normalisation.

Two sampled non-propagated edges (random pick across the 65):

| src_id → dst_id | provenance | evidence_excerpt | evidence_source_id |
| --- | --- | --- | --- |
| `bg_reuse_stahl_gelaender_verbiest_charleroi → mm_same_site` | `derived / legacy_migration / unklar` | null | `archive:Verbiest_Karreveld_Brussels.md (replicated from pre-split BG)` |
| `bg_reuse_holz_fassade_botanique → mm_same_site` | `derived / legacy_migration / unklar` | `"BELEGT"` | `Same-site reuse (donor=receiver Bauwerk); no market transaction` |

So Phase 1.3's contract — "65 edges left to retain their real evidence" — was honoured at the moment Phase 1.3 ran, even though Phase 4.1 has since reshaped their evidence properties.

### Check 9 — No Projekt lost market-model evidence in the Phase 1.3 transition — **PASS (with 1 caveat)**

Methodology: diffed `snapshot/relationships.jsonl` (pre-Phase-1, taken `2026-05-20T20:42Z`, 19 989 rels) against the live `mit-bestand` today on two axes:

(a) **Topology of the 319 propagated `HAT_MARKTMODELL` edges** — the edges Phase 1.3.a re-shaped:

| measure | snapshot | live | Δ |
| --- | ---: | ---: | ---: |
| distinct `(BG, MM)` pairs over all `HAT_MARKTMODELL` | 384 | 384 | 0 |
| distinct `(BG, MM)` pairs where source_excerpt was "propagated" (snapshot) / evidence_basis='propagated' (live) | 319 | 319 | 0 |
| snapshot-propagated pairs missing from live | — | — | **0** |
| snapshot-propagated pairs not flagged `propagated` in live | — | — | **0** |
| live pairs absent from snapshot | — | — | 0 |
| live-propagated pairs absent from snapshot-propagated | — | — | 0 |

**Conclusion (a):** Phase 1.3.a preserved 100 % of the BG→MM topology and re-flagged exactly the right 319 edges.

(b) **Re-derivability of the 86 deleted dominant projekt→mm claims** — the edges Phase 1.3.b deleted:

For each of the 86 `(Projekt, Marktmodell)` pairs from `HAT_DOMINANT_MARKTMODELL` in the snapshot, checked whether `(Projekt)-[:HAT_BAUTEILGRUPPE]->(BG)-[:HAT_MARKTMODELL]->(MM)` still reaches the same MM today.

| outcome | count |
| --- | ---: |
| projekt still exists, mm still exists, ≥1 reaching BG | **85 / 86** |
| projekt still exists, mm still exists, 0 reaching BG | **1 / 86** |

The single un-derivable claim:

| projekt_id | mm_id | projekt BGs in live | snapshot BGs with `HAT_MARKTMODELL` |
| --- | --- | ---: | --- |
| `p_elementa_walkeweg` | `mm_plattform_vermittelt` | 4 (`bg_planned_holz_decke_elementa_brettstapel`, `bg_reuse_mineralisch_wand_elementa_baufeld_d`, `bg_planned_lehm_erde_wand_elementa_clay`, `bg_reuse_mineralisch_stuetze_elementa_baufeld_c`) | 0 (none of the 4 ever had a `HAT_MARKTMODELL` edge) |

**Root cause:** in the snapshot, all four BGs of `p_elementa_walkeweg` carried zero `HAT_MARKTMODELL` edges; the only `Projekt→mm_plattform_vermittelt` assertion came directly from the now-deleted `HAT_DOMINANT_MARKTMODELL`. The plan's re-derivability assumption holds for 85 of 86 cases but fails for this one because the underlying fan-in was never written.

This is a **known plan-side blind spot, not a Phase 1.3 execution defect**. Phase 1.3 did exactly what section 1.3 specifies; the loss is the cost the plan explicitly accepted when it asserted re-derivability "by count".

(c) **Parallel observation for HAT_DOMINANT_AKZEPTANZ:** the snapshot contains zero plain `HAT_AKZEPTANZ` edges (only the 24 dominant variants), and the live graph still contains zero `HAT_AKZEPTANZ` edges (`CALL db.relationshipTypes() WHERE relationshipType CONTAINS 'AKZEPTANZ'` returns the empty set). So Phase 1.3.c removed all 24 akzeptanz claims with no possibility of re-derivation. Plan-acknowledged; out of scope for "market-model" evidence loss but worth recording.

### Check 10 — No edge has both old `HAT_DOMINANT_*` label and new `evidence_basis` — **PASS** (trivially)

Both `HAT_DOMINANT_MARKTMODELL` and `HAT_DOMINANT_AKZEPTANZ` no longer exist as relationship types in `mit-bestand` (`db.relationshipTypes()` returns no matches for either name). Therefore no surviving edge in the graph can carry an `HAT_DOMINANT_*` type at all, regardless of its `evidence_basis` value. Sanity satisfied without further filtering.

---

## Counts (compact form)

```text
hat_marktmodell_total                                  : 384
hat_marktmodell_with_evidence_basis_propagated         : 319
hat_marktmodell_with_evidence_basis_not_propagated     : 65    (all derived/legacy_migration/unklar — reshaped by Phase 4.1)
hat_marktmodell_with_source_excerpt_contains_propagated: 0
hat_marktmodell_propagated_with_canonical_shape        : 319/319 (zero deviations)

hat_dominant_marktmodell                               : 0
hat_dominant_akzeptanz                                 : 0
db.relationshipTypes matching 'HAT_DOMINANT*'          : []   (type retired)
db.relationshipTypes matching '*AKZEPTANZ*'            : []   (no surviving akzeptanz edges in any form)

snapshot_hat_marktmodell_total                         : 384
snapshot_hat_dominant_marktmodell                      : 86
snapshot_hat_dominant_akzeptanz                        : 24
snapshot_hat_marktmodell_propagated_via_source_excerpt : 319

snapshot_BG_MM_pairs_total                             : 384
live_BG_MM_pairs_total                                 : 384
pairs_lost_in_transition                               : 0
pairs_gained_in_transition                             : 0

dominant_projekt_mm_claims_in_snapshot                 : 86
dominant_projekt_mm_claims_rederivable_via_BG_today    : 85
dominant_projekt_mm_claims_NOT_rederivable             : 1     (p_elementa_walkeweg -> mm_plattform_vermittelt; underlying fan-in never existed)
```

---

## Files touched by this verifier

- **Created:** `reports/pass2_verify_phase1_3.md` (this file).
- **Migrations executed:** none (read-only).
- **Database writes:** none (read-only).
- **Temporary working files (outside repo):**
  - `C:/Users/Kinosh/AppData/Local/Temp/snapshot_pairs.json` — set of 384 `(BG, MM)` pairs + 319 propagated subset, extracted from `snapshot/relationships.jsonl` for diff use.
  - `C:/Users/Kinosh/AppData/Local/Temp/dominant_pairs.json` — 86 `(Projekt, MM)` + 24 `(Projekt, Akz)` pairs from snapshot, used for derivability check.
  - `C:/Users/Kinosh/AppData/Local/Temp/projekt_mm_claims.json` — flat list of the 86 dominant Projekt→MM claims for the live re-derivability query.
