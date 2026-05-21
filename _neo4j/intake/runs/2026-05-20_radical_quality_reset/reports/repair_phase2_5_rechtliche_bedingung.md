# Repair Phase 2.5: RechtlicheBedingung Demotion

Date: 2026-05-21  
Database: `mit-bestand`  
Repair agent: C  
Failure fixed: Final verifier 5 observed 15 live `:RechtlicheBedingung` nodes; expected 0.

## Summary

The 15 remaining `:RechtlicheBedingung` nodes were later source-level legal-regime records from `q_bauteilreuse_legal_regime_matrix_md`. They had `BELEGT_IN` evidence edges to that source and no live `HAT_RECHTLICHE_BEDINGUNG` edges to project/domain nodes at inspection time.

The repair follows the Phase 2.5 property-first demotion pattern:

- preserved condition IDs/names on the connected `Quelle` node in `legal_conditions`, `legal_condition_ids`, and `demoted_legal_condition_ids`;
- preserved provenance/evidence metadata in `legal_condition_evidence_source_ids`, `legal_condition_evidence_basis`, `legal_condition_evidence_origin`, `legal_condition_evidence_confidence`, `legal_condition_source_edge_ids`, and `demoted_legal_condition_records`;
- included a generic transfer step for any remaining `HAT_RECHTLICHE_BEDINGUNG` domain edges, which updated 0 nodes because none existed at runtime;
- deleted the 15 demoted label nodes with `DETACH DELETE`.

No new node label was created.

## Files Written

- `_neo4j/intake/runs/2026-05-20_radical_quality_reset/migrations/mig_repair_2_5_rechtliche_bedingung_demote.cypher`
- `_neo4j/intake/runs/2026-05-20_radical_quality_reset/deleted/repair_phase2_5_rechtliche_bedingung_demoted.jsonl`
- `_neo4j/intake/runs/2026-05-20_radical_quality_reset/PHASE_2_5_REPAIR_DONE.flag`
- `_neo4j/intake/runs/2026-05-20_radical_quality_reset/reports/repair_phase2_5_rechtliche_bedingung.md`

## Execution Result

Migration statement results:

- source node updated: `q_bauteilreuse_legal_regime_matrix_md`
- legal conditions preserved on source node: 15
- domain nodes updated through `HAT_RECHTLICHE_BEDINGUNG`: 0
- `:RechtlicheBedingung` nodes deleted: 15

Runtime notices:

- Neo4j emitted APOC deprecation warnings for `apoc.coll.toSet`; this matches prior migration style and did not block execution.

## Verification

Before repair:

```json
{
  "rechtlichebedingung_count": 15,
  "layer_count": 0,
  "lebenszyklusmodul_count": 0,
  "zertifizierungbewertungssystem_count": 0,
  "tool_count": 0,
  "software_count": 19,
  "software_kind_count": 19,
  "software_total_for_kind": 19,
  "bauteiltyp_brand_layer_count": 15
}
```

After repair:

```json
{
  "rechtlichebedingung_count": 0,
  "layer_count": 0,
  "lebenszyklusmodul_count": 0,
  "zertifizierungbewertungssystem_count": 0,
  "tool_count": 0,
  "software_count": 19,
  "software_kind_count": 19,
  "software_total_for_kind": 19,
  "bauteiltyp_brand_layer_count": 15
}
```

Queryable legal-condition preservation on `q_bauteilreuse_legal_regime_matrix_md`:

```json
{
  "legal_conditions_count": 15,
  "legal_condition_ids_count": 15,
  "demoted_records_count": 15,
  "evidence_source_ids": ["q_bauteilreuse_legal_regime_matrix_md"]
}
```

The preserved `legal_condition_ids` are:

```json
[
  "rb_bauordnungsrecht",
  "rb_bauproduktenverordnung_cpr",
  "rb_boulder_deconstruction_ordinance_8366",
  "rb_ce_ukca_marking_reused_steel",
  "rb_denkmalschutz",
  "rb_dibt_zustimmung",
  "rb_eu_taxonomie",
  "rb_gewaehrleistung",
  "rb_grade_ii_listing",
  "rb_kreislaufwirtschaftsgesetz_krwg",
  "rb_materialpass",
  "rb_produkthaftung",
  "rb_schweizer_bauproduktegesetz",
  "rb_vergaberecht",
  "rb_zulassung_im_einzelfall"
]
```

## Risks

- These records are source/country-level metadata, not project-level facts. The source file explicitly says project-level edges require project evidence, so the repair preserved them on the connected `Quelle` rather than inventing project/domain relationships.
- `demoted_legal_condition_records` stores compact JSON strings because Neo4j node properties cannot store maps; structured queryability is provided by the parallel list properties.
