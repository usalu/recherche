# Post-Repair Verification — Re-run of previously failed / residual gates

- **Verifier:** post-repair verification agent
- **Database:** `mit-bestand` on `bolt://localhost:7687` (creds: `E:\recherche\.cursor\mcp.json`)
- **Mode:** read-only (no writes; verified with `read-cypher` semantics and the python `neo4j` driver)
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Timestamp (UTC):** 2026-05-21T07:47:08+00:00
- **Inputs (all 5 repair reports + flags consumed):**
  - `repair_phase1_2_anchor_regression.md` + `PHASE_1_2_REPAIR_DONE.flag`
  - `repair_phase1_5_1_6_residuals.md` + `PHASE_1_5_1_6_REPAIR_DONE.flag`
  - `repair_phase2_5_rechtliche_bedingung.md` + `PHASE_2_5_REPAIR_DONE.flag`
  - `repair_phase4_1_q1.md` + `PHASE_4_1_Q1_REPAIR_DONE.flag`
  - `repair_phase2_7_5_1_panel_tier.md` + `PHASE_2_7_5_1_REPAIR_DONE.flag`
- **Driver script:** `logs/post_repair_verify.py`
- **Raw JSON dump:** `logs/post_repair_verify.json`

## 0. Overall verdict

**OVERALL: PASS** — 28 / 28 gates green across the 5 repaired sections.
All previously failing Final-Verifier gates now pass live, and the Phase 4c
invariants that the repair was required not to disturb are still green.

| Section | Verdict |
|---|---|
| Phase 1.2 — anchor regression closed | **PASS** (5/5) |
| Phase 1.5 / 1.6 — norm + actor residuals closed | **PASS** (5/5) |
| Phase 2.5 — `:RechtlicheBedingung` demoted | **PASS** (5/5) |
| Phase 4.1 + 4c + Q1 — curated/excerpt + Q1 promotion | **PASS** (8/8) |
| Phase 2.7 panel + Phase 5.1 tiering | **PASS** (5/5) |

## 1. Phase 1.2 — Anchor regression closed

Re-running Final Verifier 2's gates 4–7 plus a regression probe.

| # | Gate | Expected | Live | Status |
|---|---|---:|---:|:---:|
| 1 | `:Quelle` with id `q_controlled_vocab_seed` or `q_akteursliste_master_md` | 0 | 0 | PASS |
| 2 | `()-[:BELEGT_IN]->(:OntologyAnchor)` | 0 | 0 | PASS |
| 3 | `count(:OntologyAnchor)` | 2 | 2 | PASS |
| 4 | `()-[:ANCHORED_BY]->(:OntologyAnchor)` in `[690, 730]` | window | 703 | PASS |
| 5 | `()-[:BELEGT_IN]->(n)` where `n.id IN [<anchor ids>]` (regression probe) | 0 | 0 | PASS |

Two anchors visible live: `q_controlled_vocab_seed` and `q_akteursliste_master_md`,
both labelled `:OntologyAnchor` only. The 202 regressed `BELEGT_IN` edges that
Final Verifier 2 found on the surviving anchor are gone; the duplicate `:Quelle`
shell with id `q_akteursliste_master_md` is gone. Phase 1.2 contract restored.

## 2. Phase 1.5 / 1.6 — norm + actor residuals closed

Re-running Final Verifier 3's checks 11, 17, 18 and the supporting counts.

| # | Gate | Expected | Live | Status |
|---|---|---:|---:|:---:|
| 1 | `:Norm {id:'norm_din_18940'}` | 0 | 0 | PASS |
| 2 | `:Akteur {id:'bauburo_in_situ'}` | 0 | 0 | PASS |
| 3 | `:Akteur {id:'Bellastock'}` | 0 | 0 | PASS |
| 4 | Case-insensitive `:Akteur` duplicate ordered pairs | 0 | 0 | PASS |
| 5 | `count(:Akteur)` reasonable | in `[640, 660]` | 648 | PASS |

Canonical replacements observed live: `baubuero_in_situ` (degree 24), `bellastock`
(degree 27), and `norm_din_18940_family` (degree 1). All three residual ids were
merged or remapped into canonical nodes per the repair plan.

## 3. Phase 2.5 — `:RechtlicheBedingung` demoted

Re-running Final Verifier 5's checks 8–14 (label counts only).

| # | Gate | Expected | Live | Status |
|---|---|---:|---:|:---:|
| 1 | `count(:RechtlicheBedingung)` | 0 | 0 | PASS |
| 2 | `count(:Layer)` (already 0; still 0) | 0 | 0 | PASS |
| 3 | `count(:LebenszyklusModul)` (already 0; still 0) | 0 | 0 | PASS |
| 4 | `count(:ZertifizierungBewertungssystem)` (already 0; still 0) | 0 | 0 | PASS |
| 5 | `count(:Tool)` (already 0; still 0) | 0 | 0 | PASS |

The 15 demoted `:RechtlicheBedingung` records are now property-encoded on
`q_bauteilreuse_legal_regime_matrix_md` per the repair report (not reverified
here because the post-repair check only owns label-count gates).

## 4. Phase 4.1 + 4c invariants + Acceptance Q1

Re-running Final Verifier 10's hard-rule checks (2–7) and 4c invariants (12–14),
plus the Acceptance Q1 row-count required by the repair report.

| # | Gate | Expected | Live | Status |
|---|---|---:|---:|:---:|
| 1 | `evidence_origin='curated' AND evidence_excerpt IS NULL` | 0 | 0 | PASS |
| 2 | `evidence_origin` outside `{curated, inferred, derived}` | 0 | 0 | PASS |
| 3 | `evidence_confidence` outside `{belegt, teilweise_belegt, unklar, inferiert, bookkeeping}` | 0 | 0 | PASS |
| 4 | `evidence_confidence='bookkeeping' AND evidence_origin <> 'derived'` | 0 | 0 | PASS |
| 5 | `:Quelle.external_sources IS NOT NULL` | 0 | 0 | PASS |
| 6 | Relationships carrying any of `url` / `http` / `source_file` / `external_sources` | 0 | 0 | PASS |
| 7 | `(:Projekt)-[:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})` | 0 | 0 | PASS |
| 8 | Acceptance Q1 canonical Reuse-Story rows | ≥ 1 | **266** | PASS |

Supporting counts:

- `evidence_basis IN ['research_file_row']` violations on `:BELEGT_IN`: 0
  (243 remap from Repair D applied).
- `:HAT_BAUTEILGRUPPE` with `evidence_origin='curated'`: 254 (Q1 promotion live).
- `Q1` strict-`Bauwerk-to-Bauwerk` variant: 197 rows (donor/receiver can be
  other labels — keeping the canonical permissive variant matches Repair D and
  plan §Q1).
- `:ZITIERT_QUELLE` total: 1 470 (matches Repair D's reported "unchanged" value).

## 5. Phase 2.7 panel cleanup + Phase 5.1 tiering

Re-running Final Verifier 6's checks 8/9 (Projekt distinct keys, sample per-node
keys), plus Final Verifier 12's Phase 5 gates and the `p_circle_house` residual.

| # | Gate | Expected | Live | Status |
|---|---|---:|---:|:---:|
| 1 | `:Projekt` distinct property keys | ≤ 25 | **22** | PASS |
| 2 | Sampled 5 `:Projekt` per-node key counts | ≤ 18 each | `[14, 13, 13, 15, 13]` | PASS |
| 3 | All `:Projekt` carry `quality_tier` | `total == with_tier` | 101 == 101 | PASS |
| 4 | Tier distribution | tier_1 ≥ 8, tier_2 ≥ 50, tier_3 ≥ 10 | 11 / 68 / 22 | PASS |
| 5 | `p_circle_house` tier (per repair report) | `:Projekt`, `tier_2_documentation_only` | `:Projekt`, `tier_2_documentation_only` | PASS |

Supporting counts confirming the fold migration:

- `:Projekt` carrying `quality_tier_facts` (JSON-string fold): **101**.
- `:Projekt` carrying any of the 9 legacy `quality_tier_*` scalars: **0**.
- `:Projekt` max per-node key count: **18** (was 26 before the repair).

`p_circle_house` is documented in `repair_phase2_7_5_1_panel_tier.md` §2 as
`tier_2_documentation_only` — the formula-consistent §5.1 output (2 of 5
sub-criteria met). The repair task explicitly accepted that as the correct live
state; this verifier honours that and treats the §5.3 narrative-vs-formula gap
as documentation, not graph state.

## 6. Cypher run (read-only)

All queries are read-only and use the live `mit-bestand` database. Exact
statements are encoded in `logs/post_repair_verify.py`. Highlights:

```cypher
// 1.2 anchor regression
MATCH (q:Quelle) WHERE q.id IN ['q_controlled_vocab_seed','q_akteursliste_master_md']
RETURN count(q);                                                    // 0
MATCH ()-[r:BELEGT_IN]->(:OntologyAnchor) RETURN count(r);          // 0
MATCH (a:OntologyAnchor) RETURN count(a);                           // 2
MATCH ()-[r:ANCHORED_BY]->(:OntologyAnchor) RETURN count(r);        // 703

// 1.5 / 1.6 residuals
MATCH (n:Norm {id:'norm_din_18940'}) RETURN count(n);               // 0
MATCH (a:Akteur {id:'bauburo_in_situ'}) RETURN count(a);            // 0
MATCH (a:Akteur {id:'Bellastock'}) RETURN count(a);                 // 0
MATCH (a1:Akteur),(a2:Akteur)
WHERE a1.id<>a2.id AND toLower(a1.id)=toLower(a2.id)
RETURN count(*);                                                    // 0
MATCH (a:Akteur) RETURN count(a);                                   // 648

// 2.5 RechtlicheBedingung
MATCH (n:RechtlicheBedingung) RETURN count(n);                      // 0

// 4.1 hard rule + 4c invariants
MATCH ()-[r]->() WHERE r.evidence_origin='curated'
  AND r.evidence_excerpt IS NULL RETURN count(r);                   // 0
MATCH ()-[r]->() WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['curated','inferred','derived']
RETURN count(r);                                                    // 0
MATCH ()-[r]->() WHERE r.evidence_confidence='bookkeeping'
  AND coalesce(r.evidence_origin,'')<>'derived' RETURN count(r);    // 0
MATCH (q:Quelle) WHERE q.external_sources IS NOT NULL RETURN count(q); // 0
MATCH ()-[r]->()
WITH r, [k IN keys(r) WHERE k IN ['url','http','source_file','external_sources']] AS bad
WHERE size(bad) > 0 RETURN count(r);                                // 0
MATCH (:Projekt)-[r:BELEGT_IN]->(:Quelle {quelltyp:'external_link_from_actor_registry'})
RETURN count(r);                                                    // 0

// Q1 canonical
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(rec),
      (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)
WHERE r.evidence_origin='curated' RETURN count(*);                  // 266

// 2.7 panel + 5.1 tier
MATCH (p:Projekt) UNWIND keys(p) AS k RETURN count(DISTINCT k);     // 22
MATCH (p:Projekt) WITH size(keys(p)) AS n RETURN max(n);            // 18
MATCH (p:Projekt) RETURN p.quality_tier, count(p);                  // 11/68/22
MATCH (p {id:'p_circle_house'})
RETURN labels(p), p.quality_tier;                                   // [Projekt], tier_2
```

## 7. Files written by this verifier

```text
logs/post_repair_verify.py
logs/post_repair_verify.json
logs/post_repair_q1_probe.py
reports/post_repair_verification.md   (this file)
POST_REPAIR_VERIFY_DONE.flag
```

## 8. JSON summary

```json
{
  "verifier": "post_repair_verification",
  "database": "mit-bestand",
  "timestamp_utc": "2026-05-21T07:47:08+00:00",
  "overall_verdict": "PASS",
  "section_passes": {
    "phase_1_2": true,
    "phase_1_5_1_6": true,
    "phase_2_5": true,
    "phase_4_1_and_4c_and_q1": true,
    "phase_2_7_and_5_1": true
  },
  "phase_1_2": {
    "quelle_with_anchor_ids": 0,
    "belegt_in_to_ontology_anchor": 0,
    "ontology_anchor_count": 2,
    "anchored_by_count": 703,
    "belegt_in_to_anchor_ids_via_id": 0
  },
  "phase_1_5_1_6": {
    "norm_din_18940_remaining": 0,
    "bauburo_in_situ_remaining": 0,
    "Bellastock_remaining": 0,
    "case_insensitive_actor_dup_ordered_pairs": 0,
    "akteur_count": 648
  },
  "phase_2_5": {
    "rechtlichebedingung_count": 0,
    "layer_count": 0,
    "lebenszyklusmodul_count": 0,
    "zertifizierungbewertungssystem_count": 0,
    "tool_count": 0
  },
  "phase_4_1_and_4c_and_q1": {
    "curated_without_excerpt": 0,
    "origin_enum_violations": 0,
    "confidence_enum_violations": 0,
    "bookkeeping_not_derived": 0,
    "citation_basis_enum_violations_belegt_in": 0,
    "quelle_external_sources_nonnull": 0,
    "rel_polluted_keys": 0,
    "projekt_actor_registry_belegt_in": 0,
    "q1_canonical_rows": 266,
    "q1_bauwerk_only_rows": 197,
    "hat_bauteilgruppe_curated": 254,
    "zitiert_quelle_total": 1470
  },
  "phase_2_7_and_5_1": {
    "projekt_total": 101,
    "projekt_distinct_keys": 22,
    "projekt_max_keys_per_node": 18,
    "projekt_sample_5_keys": [14, 13, 13, 15, 13],
    "projekt_with_quality_tier_facts": 101,
    "projekt_with_legacy_scalars": 0,
    "projekt_with_quality_tier": 101,
    "tier_distribution": {
      "tier_1_decision_grade": 11,
      "tier_2_documentation_only": 68,
      "tier_3_stub": 22
    },
    "p_circle_house": {
      "labels": ["Projekt"],
      "quality_tier": "tier_2_documentation_only",
      "documented_in_repair_report": true
    }
  },
  "remaining_failures": []
}
```

## 9. Remaining failures

None. All five repaired sections are green against the live `mit-bestand`
graph, and Phase 4c invariants (no `:Quelle.external_sources`, no polluted
rel-key set, no `(:Projekt)-[:BELEGT_IN]->actor-url`) still hold.
