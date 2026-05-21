# Pass-2 Verification — Phase 4b.1 + 4b.2 + 4b.3

- Verifier: Pass-2 Detailed Verifier 10 of 12
- Date: 2026-05-21
- Database: `mit-bestand`
- Run directory: `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`
- Mode: read-only live Cypher via Neo4j MCP

## Verdict

PASS — Phase 4b.1, 4b.2, and 4b.3 are complete against the requested acceptance gates.

All three done flags are present. `PHASE_4B_1_DONE.flag` has `acceptance.passed=true`; the 4b.2 and 4b.3 flags are present with completed payloads. Live graph counts meet or exceed every numeric threshold in the verifier brief. Counts differ slightly from the pre-repair reports where later Phase 4.1 repair work legitimately changed evidence shape/counts; all differences are in the passing direction or remain above threshold.

## Inputs Read

- Plan section 4b from `C:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`
- `reports/agent_9_phase4b1_report.md`
- `reports/agent_10_phase4b_report.md`
- `reports/final_verify_phase4b.md`
- `PHASE_4B_1_DONE.flag`, `PHASE_4B_2_DONE.flag`, `PHASE_4B_3_DONE.flag`

## Phase 4b.1 — Dossiers

| # | Gate | Expected | Live / file result | Status |
|---:|---|---:|---:|:---:|
| 1 | `PHASE_4B_1_DONE.flag` with `acceptance.passed=true` | true | true | PASS |
| 2 | `:Quelle {quelltyp:'case_markdown'}` count | observed | 116 | PASS |
| 3 | case_markdown anchors with >=1 `ZITIERT_QUELLE` child | >=85 | 100 | PASS |
| 4 | curated `BELEGT_IN` with non-empty `evidence_excerpt` | >=2500 | 3031 | PASS |
| 5 | distinct `:Projekt` with non-empty `cost_facts` | >=50 | 73 | PASS |
| 6 | sample 5 curated `BELEGT_IN` shape | canonical | 5/5 canonical | PASS |

Sampled dossier-curated `BELEGT_IN` edges all have `evidence_origin='curated'`, `evidence_basis='cell_citation'`, confidence in the accepted enum, and non-empty `evidence_excerpt`.

```json
[
  {
    "start": ["Projekt"], "start_id": "p_association_house_groeditz",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_association_house_groeditz_s0",
    "properties": {
      "_cell_hash": "9e8640b39010",
      "_created_at": "2026-05-20T22:08:09+00:00",
      "_created_by": "agent9_phase4b1",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "teilweise_belegt",
      "evidence_excerpt": "Entität: Fallstudie | Wert: Association house, Gröditz / Gröditz association house | Beziehung zur Fallstudie: Untersuchter Reuse-Fall | Quelle/Beleg: [S0], [S1]",
      "evidence_origin": "curated",
      "evidence_source_id": "q_association_house_groeditz_s0"
    }
  },
  {
    "start": ["Projekt"], "start_id": "p_association_house_groeditz",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_association_house_groeditz_s1",
    "properties": {
      "_cell_hash": "85f25aa9406e",
      "_created_at": "2026-05-20T22:08:09+00:00",
      "_created_by": "agent9_phase4b1",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "unklar",
      "evidence_excerpt": "Bauteil: Außenwand-Fertigteile | Material: Stahlbetonfertigteil | Herkunft: Schule Typ Dresden | alte Funktion: Außenwand | neue Funktion: Wand/Fassade | Menge/Umfang: Teil von 279 | tragend?: wahrscheinlich ja | räumlich?: ja | Hülle?: ja | technisch?: nein | Verbindung: überlappende Fassaden-Fertigteile erwähnt | Leistungsanforderung: Tragfähigkeit, Hülle, Feuchte/Wärme | Hürde: Maß-/Anschlussdetails | Quelle: [S1]",
      "evidence_origin": "curated",
      "evidence_source_id": "q_association_house_groeditz_s1"
    }
  },
  {
    "start": ["Projekt"], "start_id": "p_association_house_groeditz",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_association_house_groeditz_s1",
    "properties": {
      "_cell_hash": "86b4a12079b3",
      "_created_at": "2026-05-20T22:08:09+00:00",
      "_created_by": "agent9_phase4b1",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "unklar",
      "evidence_excerpt": "Bauteil: Deckenelemente | Material: Stahlbetonfertigteil | Herkunft: Schule Typ Dresden | alte Funktion: Decke/Boden | neue Funktion: Decke/Boden | Menge/Umfang: Teil von 279 | tragend?: ja | räumlich?: ja | Hülle?: nein | technisch?: nein | Leistungsanforderung: Tragfähigkeit, Brandschutz | Hürde: Anschluss, Betondeckung | Quelle: [S1]",
      "evidence_origin": "curated",
      "evidence_source_id": "q_association_house_groeditz_s1"
    }
  },
  {
    "start": ["Projekt"], "start_id": "p_association_house_groeditz",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_association_house_groeditz_s1",
    "properties": {
      "_cell_hash": "e9655c102515",
      "_created_at": "2026-05-20T22:08:09+00:00",
      "_created_by": "agent9_phase4b1",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "unklar",
      "evidence_excerpt": "Bauteil: Innenwand-Fertigteile | Material: Stahlbetonfertigteil | Herkunft: Schule Typ Dresden | alte Funktion: Innenwand | neue Funktion: Wand/Trag-/Raumstruktur | Menge/Umfang: Teil von 279 | tragend?: wahrscheinlich ja | räumlich?: ja | Hülle?: nein | technisch?: nein | Verbindung: Ziegelschicht zum Ausgleich erwähnt | Leistungsanforderung: Tragfähigkeit, Brandschutz, Schallschutz | Hürde: Höhenausgleich | Quelle: [S1]",
      "evidence_origin": "curated",
      "evidence_source_id": "q_association_house_groeditz_s1"
    }
  },
  {
    "start": ["Projekt"], "start_id": "p_association_house_groeditz",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_association_house_groeditz_s1",
    "properties": {
      "_cell_hash": "9f78e61b7a47",
      "_created_at": "2026-05-20T22:08:09+00:00",
      "_created_by": "agent9_phase4b1",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "unklar",
      "evidence_excerpt": "Bauteil: Innenwandrahmen | Material: Stahlbetonfertigteil | Herkunft: Schule Typ Dresden | alte Funktion: Wand-/Rahmenelement | neue Funktion: räumlich/tragend | Menge/Umfang: Teil von 279 | tragend?: wahrscheinlich ja | räumlich?: ja | Hülle?: nein | technisch?: nein | Leistungsanforderung: Tragfähigkeit | Hürde: Geometrie | Quelle: [S1]",
      "evidence_origin": "curated",
      "evidence_source_id": "q_association_house_groeditz_s1"
    }
  }
]
```

## Phase 4b.2 — Research

| # | Gate | Expected | Live / file result | Status |
|---:|---|---:|---:|:---:|
| 7 | `PHASE_4B_2_DONE.flag` present | true | true | PASS |
| 8 | `:Quelle {quelltyp:'research_markdown'}` | >=7 | 8 | PASS |
| 9 | `BELEGT_IN` with `evidence_origin='inferred'` anchored to research markdown | >=200 | 243 | PASS |
| 10 | research_markdown anchors with `ZITIERT_QUELLE` children | >=5 | 6 | PASS |
| 11 | sample 3 inferred `BELEGT_IN` shape | canonical | 3/3 canonical | PASS |

The inferred count is now 243 rather than the earlier 258 because post-repair work remapped/cleaned some evidence-basis classifications. The acceptance threshold is still exceeded by 43.

```json
[
  {
    "start": ["Aufbereitungsverfahren"], "start_id": "av_aluminium_oberflaechenbehandlung",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_aufbereitungsverfahren_reused_building_elements_md",
    "properties": {
      "derivation_note": "former_basis=research_file_row->cell_citation via mig_repair_4_1 (BELEGT_IN belongs to citation-group enum, not norm-group)",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "inferiert",
      "evidence_origin": "inferred",
      "evidence_source_id": "q_aufbereitungsverfahren_reused_building_elements_md",
      "id": "r_av_aluminium_oberflaechenbehandlung__BELEGT_IN__q_aufbereitungsverfahren_reused_building_elements_md",
      "migration_origin": "mig_repair_4_1_basis_norm_group"
    }
  },
  {
    "start": ["Aufbereitungsverfahren"], "start_id": "av_aluminium_reinigung_entdichtung",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_aufbereitungsverfahren_reused_building_elements_md",
    "properties": {
      "derivation_note": "former_basis=research_file_row->cell_citation via mig_repair_4_1 (BELEGT_IN belongs to citation-group enum, not norm-group)",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "inferiert",
      "evidence_origin": "inferred",
      "evidence_source_id": "q_aufbereitungsverfahren_reused_building_elements_md",
      "id": "r_av_aluminium_reinigung_entdichtung__BELEGT_IN__q_aufbereitungsverfahren_reused_building_elements_md",
      "migration_origin": "mig_repair_4_1_basis_norm_group"
    }
  },
  {
    "start": ["Aufbereitungsverfahren"], "start_id": "av_aluminium_zuschnitt_bohrung",
    "type": "BELEGT_IN", "end": ["Quelle"], "end_id": "q_aufbereitungsverfahren_reused_building_elements_md",
    "properties": {
      "derivation_note": "former_basis=research_file_row->cell_citation via mig_repair_4_1 (BELEGT_IN belongs to citation-group enum, not norm-group)",
      "evidence_basis": "cell_citation",
      "evidence_confidence": "inferiert",
      "evidence_origin": "inferred",
      "evidence_source_id": "q_aufbereitungsverfahren_reused_building_elements_md",
      "id": "r_av_aluminium_zuschnitt_bohrung__BELEGT_IN__q_aufbereitungsverfahren_reused_building_elements_md",
      "migration_origin": "mig_repair_4_1_basis_norm_group"
    }
  }
]
```

## Phase 4b.3 — Actor Registry

| # | Gate | Expected | Live / file result | Status |
|---:|---|---:|---:|:---:|
| 12 | `PHASE_4B_3_DONE.flag` present | true | true | PASS |
| 13 | `HAT_AKTEURROLLE` in curated/belegt shape | >=500 | 548 | PASS |
| 14a | `ASSOZIIERT_MIT_PROJEKT` with `evidence_basis='registry_stub'` | >=100 | 200 | PASS |
| 14b | `ASSOZIIERT_MIT_PROJEKT` curated/teilweise_belegt registry_stub | >=100 | 142 | PASS |
| 15 | `Projekt -[:BELEGT_IN]-> actor_url Quelle` | 0 | 0 | PASS |
| 16a | `Akteur -[:BELEGT_IN]-> actor_url` canonical curated shape | >=300 | 318 | PASS |
| 16b | canonical actor-url edges with non-empty excerpt | same as 16a | 318 / 318 | PASS |
| 17 | curated actor-registry claim edges with null/empty `evidence_excerpt` | 0 | 0 | PASS |

For gate 17, the checked acceptance scope is curated actor-registry claim edges (`source_scope='actor_registry' AND evidence_origin='curated'`). Live count: 1691 curated actor-registry claim edges, 0 with null/empty `evidence_excerpt`. A broader diagnostic over all `source_scope='actor_registry'` relationships also finds 529 derived/source-link relationships with null excerpts; those are not curated claim edges and are allowed by the Phase 4.1 invariant.

## Live Cypher Summary

```json
{
  "phase_4b_1": {
    "flag_present": true,
    "acceptance_passed": true,
    "case_markdown_total": 116,
    "case_markdown_with_zitiert_child": 100,
    "curated_belegt_with_excerpt": 3031,
    "projekt_with_cost_facts": 73,
    "sample_5_curated_belegt_in_shape_ok": true
  },
  "phase_4b_2": {
    "flag_present": true,
    "research_markdown_total": 8,
    "inferred_belegt_to_research_markdown": 243,
    "research_markdown_with_zitiert_child": 6,
    "sample_3_inferred_belegt_in_shape_ok": true
  },
  "phase_4b_3": {
    "flag_present": true,
    "hat_akteurrolle_curated_belegt": 548,
    "assoziiert_registry_stub_total": 200,
    "assoziiert_registry_stub_curated_teilweise": 142,
    "projekt_belegt_actor_url": 0,
    "akteur_belegt_actor_url_canonical": 318,
    "akteur_belegt_actor_url_canonical_with_excerpt": 318,
    "curated_actor_registry_edges": 1691,
    "curated_actor_registry_null_excerpt": 0,
    "derived_actor_registry_edges": 529,
    "derived_actor_registry_null_excerpt": 529
  }
}
```

## JSON Verdict

```json
{
  "verifier": "pass2_detailed_verifier_10_of_12",
  "phase": "4b",
  "database": "mit-bestand",
  "run_dir": "E:/recherche/_neo4j/intake/runs/2026-05-20_radical_quality_reset",
  "status": "pass",
  "complete": true,
  "checks_passed": 17,
  "checks_failed": 0,
  "notes": [
    "All requested numeric thresholds pass live.",
    "Phase 4b.2 inferred research BELEGT_IN count is 243 after post-repair evidence-basis cleanup, still above the >=200 threshold.",
    "Actor-registry null-excerpt gate is evaluated on curated actor-registry claim edges; broader derived/source-link registry relationships are reported separately and remain outside the curated-excerpt invariant."
  ]
}
```
