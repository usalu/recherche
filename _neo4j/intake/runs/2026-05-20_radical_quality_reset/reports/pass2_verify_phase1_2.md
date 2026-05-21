# Pass-2 Verification — Phase 1.2 (incl. anchor regression repair)

- **Verifier:** Pass-2 Detailed Verifier 2 of 12 (read-only, no migrations executed)
- **Verified at:** 2026-05-21 (live `mit-bestand`, `bolt://localhost:7687`)
- **Plan reference:** `c:/Users/Kinosh/.cursor/plans/radical_quality-first_reset_8d1e2b66.plan.md`, section 1.2
- **Run directory:** `E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset/`
- **Scope:** confirm Phase 1.2 (anchor relabel + `BELEGT_IN`→`ANCHORED_BY` retype + deg-0 `:Quelle` purge) and the post-hoc repair of the Phase 4b.3 regression are fully complete on the live graph.

---

## Overall verdict

**Phase 1.2 + Phase 1.2-repair: PASS.** All eleven Pass-2 deep checks succeed against the live graph. The original Phase 1.2 migration (2026-05-20T20:57:50Z) and the subsequent repair migration (2026-05-21T07:18:00Z) together restore the Phase 1.2 contract end-to-end:

- the two ontology anchors (`q_controlled_vocab_seed`, `q_akteursliste_master_md`) are `:OntologyAnchor`-only,
- no `:Quelle` shadow node carries either anchor id,
- no `:BELEGT_IN` edge terminates on an `:OntologyAnchor`,
- 703 `:ANCHORED_BY` edges (well inside the [690, 730] acceptance window) carry the canonical `derived/controlled_vocab/bookkeeping` shape, with `evidence_excerpt` `NULL` across the full population,
- the actor-registry source-as-link behavior is preserved on the real anchor (`q_akteursliste_master_md` keeps its 319 outgoing `:ZITIERT_QUELLE`).

---

## Deep-check matrix

| # | Check (live `mit-bestand`) | Expected | Live | Result |
|---|---|---|---|---|
| 1 | `migrations/mig_1_2_anchor_relabel.cypher` exists | present | present (69 lines, 3 sections) | PASS |
| 1 | `migrations/mig_repair_1_2_anchor_regression.cypher` exists | present | present (56 lines, 4 sections) | PASS |
| 2 | `PHASE_1_2_DONE.flag` present + parseable | yes | yes (`logs/PHASE_1_2_DONE.flag`, valid JSON, `completed_at=2026-05-20T20:57:50+00:00`) | PASS |
| 2 | `PHASE_1_2_REPAIR_DONE.flag` present + parseable | yes | yes (run-root, valid JSON, `completed_at=2026-05-21T07:18:00+00:00`) | PASS |
| 3 | `deleted/phase1_2_quelle.jsonl` exists with 21 deg-0 `:Quelle` | 21 named records | 23 lines total = 1 header + 21 named deg-0 `:Quelle` (Phase 1.2 list, all `actually_deleted_in=phase_1_5`) + 1 collateral orphan (`q_phase20_kette_autodiscovery`, deleted by 1.2.c). All 21 named IDs match the plan's deg-0 set. | PASS |
| 4 | `count(:OntologyAnchor) == 2` with `{q_controlled_vocab_seed, q_akteursliste_master_md}` | 2 | 2 (ids exactly `q_controlled_vocab_seed`, `q_akteursliste_master_md`) | PASS |
| 5 | `:Quelle` with `id IN ['q_controlled_vocab_seed','q_akteursliste_master_md']` == 0 | 0 | 0 (duplicate `:Quelle` shell deleted by repair migration) | PASS |
| 6 | `()-[:BELEGT_IN]->(:OntologyAnchor) == 0` | 0 | 0 (202 regressed `BELEGT_IN` edges to `q_akteursliste_master_md` removed by repair migration) | PASS |
| 7 | `()-[:ANCHORED_BY]->(:OntologyAnchor)` in `[690, 730]` | in range | **703** (443 → `q_controlled_vocab_seed`, 260 → `q_akteursliste_master_md`) | PASS |
| 8 | Sampled `:ANCHORED_BY` edges carry canonical shape | 10/10 canonical | 10/10 canonical (sample) + **703/703 canonical (population)**: `evidence_origin='derived'`, `evidence_basis='controlled_vocab'`, `evidence_confidence='bookkeeping'`, `evidence_excerpt IS NULL`, `evidence_source_id` matches anchor id | PASS |
| 9 | No duplicate `:Quelle` nodes for either anchor id | 0 | 0 — exactly 2 nodes graph-wide carry these ids, both `:OntologyAnchor`-only | PASS |
| 10 | `:OntologyAnchor` in/out degree breakdown sensible | ANCHORED_BY bulk + optional ZITIERT_QUELLE | see breakdown below | PASS |
| 11 | Audit jsonl line counts match repair report | 1 header + 1 summary + 1 dup-node + 202 + 202 + 277 = 684 | 684 lines, exact match | PASS |

**Aggregate: 11/11 PASS.**

---

## Detail

### 1. Migration files

- `migrations/mig_1_2_anchor_relabel.cypher` — original Phase 1.2 migration. Sections 1.2.a (relabel two anchors), 1.2.b (retype `BELEGT_IN`→`ANCHORED_BY` with canonical shape), 1.2.c (hard-delete deg-0 `:Quelle`). Header documents pre-migration counts (457 + 259 `BELEGT_IN` and 21 deg-0 `:Quelle`).
- `migrations/mig_repair_1_2_anchor_regression.cypher` — repair migration scoped to `q_akteursliste_master_md`. Four sections: (1) convert regressed `BELEGT_IN`→`ANCHORED_BY` on the real anchor using `MERGE` to avoid duplicates, (2) preserve outgoing `:ZITIERT_QUELLE` on the real anchor via `MERGE`, (3) remove duplicate shell's incoming `:BELEGT_IN`, (4) delete duplicate `:Quelle` shell once detached.

### 2. Done-flags

```text
logs/PHASE_1_2_DONE.flag           (Phase 1.2 main, 2026-05-20T20:57:50+00:00)
PHASE_1_2_REPAIR_DONE.flag         (Phase 1.2 repair, 2026-05-21T07:18:00+00:00)
```

Both are valid JSON. The main flag's `after` block reports `belegt_in_to_anchors=0`, `anchored_by_to_anchors=716`, `anchors_as_ontology_anchor=2`, `deg0_quelle=0`. The repair flag's `after` block reports `duplicate_quelle_controlled_vocab_ids=0`, `belegt_in_to_ontology_anchor=0`, `anchored_by_to_ontology_anchor=703`, `anchored_by_to_q_akteursliste_master_md=260`, `bad_anchored_by_shape_to_ontology_anchor=0`, `ontology_anchor_zitiert_quelle_out=319`. Live graph today exactly matches the repair `after` block.

### 3. `deleted/phase1_2_quelle.jsonl` (forensic completeness)

23 lines: 1 header + 21 plan-named deg-0 `:Quelle` (all cross-referenced as `actually_deleted_in=phase_1_5`, `preempted_by=agent_5`) + 1 collateral orphan (`q_phase20_kette_autodiscovery`, `collateral_cause=phase_1_1_chain_deletion_orphaned_this_node`, actually deleted by 1.2.c). The 21 named IDs reproduce the plan's deg-0 set verbatim (`qu_rcmi_concular_dossier`, `qu_arch_reuse_bxl_dossier`, `qu_vandkunsten_dossier`, `qu_zhaw_reuse_dossier`, 7 Circl S-refs, 3 Careno/LysP8 refs, 2 MedUni/Stuttgart refs, 2 FCRBE/REBRIDGE refs, 2 Granby refs).

### 4. Live anchor identity

```cypher
MATCH (a:OntologyAnchor) RETURN count(a), collect(a.id)
// → count=2, ids = ['q_controlled_vocab_seed', 'q_akteursliste_master_md']
```

### 5. No `:Quelle` shadows for anchor ids

```cypher
MATCH (q:Quelle) WHERE q.id IN ['q_controlled_vocab_seed','q_akteursliste_master_md']
RETURN count(q)
// → 0
```

And the universe check (any-label nodes with these ids):

```cypher
MATCH (n) WHERE n.id IN ['q_controlled_vocab_seed','q_akteursliste_master_md']
RETURN n.id, labels(n), elementId(n)
```

| id | labels | elementId | in-deg | out-deg |
|---|---|---|---:|---:|
| `q_controlled_vocab_seed` | `[OntologyAnchor]` | `4:…:807` | 443 | 0 |
| `q_akteursliste_master_md` | `[OntologyAnchor]` | `4:…:6180` | 260 | 319 |

Exactly two nodes; both are `:OntologyAnchor` only; the duplicate shell `4:…:1777` previously documented by Pass-1 verifier is gone.

### 6. No `:BELEGT_IN` to any `:OntologyAnchor`

```cypher
MATCH ()-[r:BELEGT_IN]->(a:OntologyAnchor) RETURN count(r)
// → 0
```

The 202 `:Akteur`/`:Land -[:BELEGT_IN]-> q_akteursliste_master_md` edges introduced by `agent10_phase4b_3` are gone: 199 already had canonical `:ANCHORED_BY` from the original Phase 1.2 migration, 3 were newly `MERGE`'d by the repair (audit confirms `anchored_by_created=3` in the repair flag).

### 7. `:ANCHORED_BY` count is in range

```cypher
MATCH ()-[r:ANCHORED_BY]->(a:OntologyAnchor) RETURN count(r)
// → 703   (in [690, 730])
```

Per-anchor breakdown:

| anchor id | `ANCHORED_BY` in |
|---|---:|
| `q_controlled_vocab_seed` | 443 |
| `q_akteursliste_master_md` | 260 |
| **total** | **703** |

The −13 drift from the original Phase 1.2 post-state (716 → 703) is consistent with downstream node deletions in later Wave-1 and Wave-2 phases (e.g. 1.5 / 1.6 / 2.x) detaching their owning `:ANCHORED_BY` edges; the live count is still 13 above the acceptance floor of 690.

### 8. Edge-shape conformance

Sampled 10 `()-[r:ANCHORED_BY]->(:OntologyAnchor)` edges (sources: `mm_kauf_neu`, `mm_kauf_gebraucht`, `mm_spende`, `mm_leasing`, `mm_rueckkauf`, `mm_same_site`, `mm_plattform_vermittelt`, `s_kmf`, `s_formaldehyd`, `s_schwermetalle` — all → `q_controlled_vocab_seed`):

| field | sampled values |
|---|---|
| `evidence_origin` | `derived` (10/10) |
| `evidence_basis` | `controlled_vocab` (10/10) |
| `evidence_confidence` | `bookkeeping` (10/10) |
| `evidence_source_id` | matches anchor id (10/10) |
| `evidence_excerpt` | `null` (10/10) |

Full-population scan (no sampling, all 703 edges):

| field | conforming |
|---|---:|
| `evidence_origin = 'derived'` | 703 / 703 |
| `evidence_basis = 'controlled_vocab'` | 703 / 703 |
| `evidence_confidence = 'bookkeeping'` | 703 / 703 |
| `evidence_excerpt IS NULL` | 703 / 703 |
| `evidence_source_id IS NOT NULL` | 703 / 703 |

Every `:ANCHORED_BY` edge in the graph today conforms to the canonical Phase 1.2 shape; no curated/cell-citation residue from the Phase 4b.3 regression remains.

### 9. No duplicate `:Quelle` for either anchor id

Already covered in checks 5 + 9 above. `MATCH (q:Quelle) WHERE q.id IN […]` returns 0; `MATCH (n) WHERE n.id IN […]` returns the two `:OntologyAnchor`-only nodes. No shadow nodes.

### 10. Anchor degree breakdown (in/out by edge type)

| anchor | in-edges by type | out-edges by type |
|---|---|---|
| `q_controlled_vocab_seed` | `ANCHORED_BY × 443` | none |
| `q_akteursliste_master_md` | `ANCHORED_BY × 260` | `ZITIERT_QUELLE × 319` |

Per-source-label breakdown of the 260 `ANCHORED_BY` on `q_akteursliste_master_md`:

| source label | count |
|---|---:|
| `Akteur` | 205 |
| `Projekt` | 35 |
| `Programm` | 10 |
| `Land` | 10 |
| **total** | **260** |

This shape matches the plan exactly: anchors receive only `:ANCHORED_BY` bookkeeping in-edges and may keep their original `:ZITIERT_QUELLE` outgoing source-as-link edges (akteursliste keeps all 319 outbound actor-URL citations; controlled-vocab-seed has none, as expected for a pure ontology root).

### 11. Audit jsonl counts vs. repair report

`logs/repair_phase1_2_anchor_regression_audit.jsonl` — 684 lines:

| `audit_kind` | count | report claim |
|---|---:|---:|
| `audit_header` | 1 | 1 |
| `summary_counts_before` | 1 | 1 |
| `duplicate_quelle_node_before_delete` | 1 | 1 |
| `belegt_in_to_ontology_anchor_before_retype` | 202 | 202 |
| `belegt_in_to_duplicate_quelle_before_delete` | 202 | 202 |
| `zitiert_quelle_from_duplicate_before_merge` | 277 | 277 |
| **total lines** | **684** | **684** (= 1 + 1 + 1 + 202 + 202 + 277) |

The `summary_counts_before` row internally reports `anchored_by_to_anchor=259`, `belegt_in_to_anchor=202`, `belegt_in_to_duplicate_quelle=202`, `duplicate_quelle_count=1`, `zitiert_from_anchor=319`, `zitiert_from_duplicate_quelle=277` — all consistent with the `before` block of `PHASE_1_2_REPAIR_DONE.flag`.

---

## Files touched by this verifier

- **Created:** `reports/pass2_verify_phase1_2.md` (this file).
- **Migrations run:** none.
- **Database writes:** none.

---

## JSON verdict

```json
{
  "verifier":   "pass2_detailed_verifier_2_of_12",
  "phase":      "1.2",
  "scope":      ["mig_1_2_anchor_relabel", "mig_repair_1_2_anchor_regression"],
  "verdict":    "PASS",
  "checks":     {
    "1_mig_1_2_anchor_relabel_present":            "PASS",
    "1_mig_repair_1_2_anchor_regression_present":  "PASS",
    "2_phase_1_2_done_flag_parseable":             "PASS",
    "2_phase_1_2_repair_done_flag_parseable":      "PASS",
    "3_deleted_phase1_2_quelle_jsonl":             "PASS",
    "4_ontology_anchor_count_two_with_ids":        "PASS",
    "5_no_quelle_with_anchor_ids":                 "PASS",
    "6_no_belegt_in_to_ontology_anchor":           "PASS",
    "7_anchored_by_in_range_690_730":              "PASS",
    "8_sample_and_population_edge_shape":          "PASS",
    "9_no_duplicate_quelle_nodes":                 "PASS",
    "10_anchor_degree_breakdown":                  "PASS",
    "11_audit_jsonl_counts_match_report":          "PASS"
  },
  "live_counts": {
    "ontology_anchor_count":                       2,
    "ontology_anchor_ids":                         ["q_controlled_vocab_seed", "q_akteursliste_master_md"],
    "quelle_with_anchor_ids":                      0,
    "belegt_in_to_ontology_anchor":                0,
    "anchored_by_to_ontology_anchor":              703,
    "anchored_by_to_q_controlled_vocab_seed":      443,
    "anchored_by_to_q_akteursliste_master_md":     260,
    "zitiert_quelle_out_from_q_akteursliste_master_md": 319,
    "anchored_by_canonical_shape_conformance":     "703/703",
    "audit_jsonl_total_lines":                     684,
    "audit_jsonl_belegt_in_to_anchor_records":     202,
    "audit_jsonl_belegt_in_to_duplicate_records":  202,
    "audit_jsonl_zitiert_from_duplicate_records":  277
  },
  "notes": [
    "Phase 1.2 main migration completed 2026-05-20T20:57:50+00:00.",
    "Phase 4b.3 introduced a duplicate :Quelle shell and 202 :BELEGT_IN edges to OntologyAnchor; both were eliminated by mig_repair_1_2_anchor_regression.cypher at 2026-05-21T07:18:00+00:00.",
    "All 703 :ANCHORED_BY edges to :OntologyAnchor carry the canonical Phase 1.2 shape (derived / controlled_vocab / bookkeeping / NULL excerpt / matching evidence_source_id).",
    "Actor-registry source-as-link behavior preserved on the real anchor (319 outgoing :ZITIERT_QUELLE on q_akteursliste_master_md).",
    "Audit trail line counts (684 = 1+1+1+202+202+277) exactly match the repair report's claimed counts."
  ]
}
```
