# Final Verify Phase 2.3 + 2.5

Verifier: Final Verifier 5 of 12  
Date: 2026-05-21  
Database: `mit-bestand`  
Run dir: `_neo4j/intake/runs/2026-05-20_radical_quality_reset/`

## Scope

Read-only verification of plan sections:

- `2.3 Two role systems -> one`
- `2.5 Under-used labels -- only Layer and LebenszyklusModul demoted`

Verification used the configured Neo4j driver credentials in `.cursor/mcp.json` and a read-only MCP cross-check. No graph writes were performed.

## Result

Overall status: **FAIL**

Phase 2.3 role cleanup is confirmed. Phase 2.5 demotions are mostly confirmed, but criterion 10 fails because `:RechtlicheBedingung` still has 15 live nodes.

## Phase 2.3 Checks

| # | Check | Expected | Observed | Status |
|---|---|---:|---:|---|
| 1 | `PHASE_2_3_DONE.flag` present | present | `_neo4j/intake/runs/2026-05-20_radical_quality_reset/logs/PHASE_2_3_DONE.flag` | PASS |
| 2 | `BETEILIGT_AN.rolle_text` properties | 0 | 0 | PASS |
| 3 | `Akteur.raw_role_evidence` populated | >= 150 | 155 | PASS |
| 4 | `Akteurrolle` `ar_reuse_beratung` | 0 | 0 | PASS |
| 5 | `Akteurrolle` `ar_reuse_zirkularitaetsberatung` | 1 | 1 | PASS |
| 6 | total `Akteurrolle` nodes | 24 | 24 | PASS |

Phase 2.3 status: **PASS**

## Phase 2.5 Checks

| # | Check | Expected | Observed | Status |
|---|---|---:|---:|---|
| 7 | `PHASE_2_5_DONE.flag` present | present | `_neo4j/intake/runs/2026-05-20_radical_quality_reset/logs/PHASE_2_5_DONE.flag` | PASS |
| 8 | `Layer` nodes | 0 | 0 | PASS |
| 9 | `LebenszyklusModul` nodes | 0 | 0 | PASS |
| 10 | `RechtlicheBedingung` nodes | 0 | 15 | FAIL |
| 11 | `ZertifizierungBewertungssystem` nodes | 0 | 0 | PASS |
| 12 | `Tool` nodes | 0 | 0 | PASS |
| 13 | `Software` nodes | >= 18 | 19 | PASS |
| 14 | all `Software` nodes have `kind` | `count(kind) == count(:Software)` | 19 == 19 | PASS |
| 15 | `Bauteiltyp.brand_layer` populated | >= 10 | 15 | PASS |

Phase 2.5 status: **FAIL**

## Failing Evidence

Live query:

```cypher
MATCH (n:RechtlicheBedingung) RETURN count(n)
```

Observed count: `15`

Remaining `RechtlicheBedingung` node ids:

- `rb_bauordnungsrecht`
- `rb_bauproduktenverordnung_cpr`
- `rb_boulder_deconstruction_ordinance_8366`
- `rb_ce_ukca_marking_reused_steel`
- `rb_denkmalschutz`
- `rb_dibt_zustimmung`
- `rb_eu_taxonomie`
- `rb_gewaehrleistung`
- `rb_grade_ii_listing`
- `rb_kreislaufwirtschaftsgesetz_krwg`
- `rb_materialpass`
- `rb_produkthaftung`
- `rb_schweizer_bauproduktegesetz`
- `rb_vergaberecht`
- `rb_zulassung_im_einzelfall`

## Raw Counts

```json
{
  "database": "mit-bestand",
  "beteiligt_an_rolle_text": 0,
  "akteur_raw_role_evidence": 155,
  "ar_reuse_beratung": 0,
  "ar_reuse_zirkularitaetsberatung": 1,
  "akteurrolle_count": 24,
  "layer_count": 0,
  "lebenszyklusmodul_count": 0,
  "rechtlichebedingung_count": 15,
  "zertifizierungbewertungssystem_count": 0,
  "tool_count": 0,
  "software_count": 19,
  "software_kind_count": 19,
  "software_total_for_kind": 19,
  "bauteiltyp_brand_layer_count": 15
}
```

## JSON Return

```json
{
  "verifier": "Final Verifier 5 of 12",
  "status": "FAIL",
  "database": "mit-bestand",
  "report": "E:\\recherche\\_neo4j\\intake\\runs\\2026-05-20_radical_quality_reset\\reports\\final_verify_phase2_3_5.md",
  "phase_2_3": {
    "status": "PASS",
    "checks": {
      "phase_2_3_done_flag_present": true,
      "beteiligt_an_rolle_text_count": 0,
      "akteur_raw_role_evidence_count": 155,
      "ar_reuse_beratung_count": 0,
      "ar_reuse_zirkularitaetsberatung_count": 1,
      "akteurrolle_count": 24
    }
  },
  "phase_2_5": {
    "status": "FAIL",
    "checks": {
      "phase_2_5_done_flag_present": true,
      "layer_count": 0,
      "lebenszyklusmodul_count": 0,
      "rechtlichebedingung_count": 15,
      "zertifizierungbewertungssystem_count": 0,
      "tool_count": 0,
      "software_count": 19,
      "software_kind_count": 19,
      "software_total_for_kind": 19,
      "bauteiltyp_brand_layer_count": 15
    },
    "failures": [
      {
        "check": "MATCH (n:RechtlicheBedingung) RETURN count(n)",
        "expected": 0,
        "observed": 15
      }
    ]
  }
}
```
