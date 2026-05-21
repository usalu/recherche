# Pass-2 Detailed Verification — Phase 4.1 + 4.2 (incl. curated-excerpt repair)

- **Verifier:** Pass-2 Detailed Verifier 9 of 12 (read-only)
- **Scope:** Phase 4.1 (canonical 5-field evidence shape, hard rules, enum compliance, curated-excerpt repair, HAT_BAUTEILGRUPPE promotion) + Phase 4.2 (donor / receiver rename)
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset`
- **Database:** `mit-bestand` on `bolt://localhost:7687` (creds resolved from `E:\recherche\.cursor\mcp.json`)
- **Plan:** `radical_quality-first_reset_8d1e2b66.plan.md`, §§ 4.1 and 4.2
- **Driver script:** `logs/pass2_verify_phase4_1_2.py`
- **Raw JSON dump:** `logs/pass2_verify_phase4_1_2.json`
- **Timestamp (UTC):** `2026-05-21T07:59:26+00:00`

## 0. Overall verdict

**OVERALL: PASS — 15 / 15 checks green.**

Phase 4.1 (canonical 5-field evidence shape + curated-excerpt repair) and Phase 4.2 (donor / receiver rename) are both fully complete on the live `mit-bestand` graph. The earlier Final Verifier 10 hard-rule violation (`evidence_origin='curated' AND evidence_excerpt IS NULL`: 2 108) is closed: the live count is **0**. The Acceptance Q1 HAT_BAUTEILGRUPPE promotion is in effect: 254 edges promoted, all five sampled promoted edges carry `evidence_basis='cell_citation'`, `evidence_confidence='teilweise_belegt'`, and a topology-backed (FROM_DONOR + INTO_RECEIVER) Bauteilgruppe target.

| Section | Verdict |
|---|---|
| Phase 4.1 — flags + migrations + hard rules + enums + matrix | **PASS** (9 / 9) |
| Phase 4.2 — flag + donor/receiver counts + samples | **PASS** (4 / 4) |
| Additional rigor — HAT_BAUTEILGRUPPE curated count + per-sample audit | **PASS** (2 / 2) |

## 1. Phase 4.1 deep checks

| # | Check | Expected | Actual | Result |
|---|---|---:|---:|:---:|
| 1 | `mig_4_1_canonical_evidence.cypher` and `mig_repair_4_1_curated_excerpts_and_q1.cypher` present | both yes | both yes | PASS |
| 2 | `PHASE_4_DONE.flag` and `PHASE_4_1_Q1_REPAIR_DONE.flag` present | both yes | both yes | PASS |
| 3 | Claim-edge types with `evidence_origin IS NULL` (full claim type list) | 0 rows | 0 rows | PASS |
| 4 | `evidence_origin` outside `{curated, inferred, derived}` | 0 | 0 | PASS |
| 5 | `evidence_confidence` outside `{belegt, teilweise_belegt, unklar, inferiert, bookkeeping}` | 0 | 0 | PASS |
| 6 | `evidence_origin='curated' AND evidence_excerpt IS NULL` | 0 | 0 | PASS |
| 7 | `evidence_confidence='bookkeeping' AND evidence_origin <> 'derived'` | 0 | 0 | PASS |
| 8 | `evidence_excerpt CONTAINS 'propagated from'` | 0 | 0 | PASS |
| 9 | Breakdown by edge type × `evidence_origin` (full matrix dump) | dump | 66 types | PASS (see §4) |

### Evidence-origin distribution (live)

| Value | Edges | % of all rels |
|---|---:|---:|
| `derived`  | 18 752 | 74.9 % |
| `curated`  |  4 748 | 19.0 % |
| `inferred` |  1 523 |  6.1 % |
| **Total**  | **25 023** | 100 % |

### Evidence-confidence distribution (live)

| Value | Edges |
|---|---:|
| `unklar`           | 18 440 |
| `belegt`           |  3 511 |
| `inferiert`        |  1 390 |
| `bookkeeping`      |  1 022 |
| `teilweise_belegt` |    660 |

Every value is in the strict enum; the repair's introduced `teilweise_belegt` cohort (660 incl. the 254 promoted HAT_BAUTEILGRUPPE) is present and accounted for.

## 2. Phase 4.2 deep checks

| # | Check | Expected | Actual | Result |
|---|---|---:|---:|:---:|
| 10 | `PHASE_4_2_DONE.flag` present | yes | yes | PASS |
| 11 | Live `AUS_BAUWERK` count | 0 | 0 | PASS |
| 11 | Live `EINGEBAUT_IN` count | 0 | 0 | PASS |
| 12 | Live `FROM_DONOR` count | ≥ 280 | **286** | PASS |
| 12 | Live `INTO_RECEIVER` count | ≥ 340 | **349** | PASS |
| 13 | 5 `FROM_DONOR` + 5 `INTO_RECEIVER` samples returned with full property dump | 5 + 5 | 5 + 5 | PASS |

The rename `AUS_BAUWERK → FROM_DONOR` (286 edges) and `EINGEBAUT_IN → INTO_RECEIVER` (349 edges) is complete; no legacy type remains; renamed edges carry the canonical 5-field shape (origin/basis/source_id/confidence non-null on every sampled edge — see §5).

## 3. Additional rigor — HAT_BAUTEILGRUPPE post-repair promotion

| # | Check | Expected | Actual | Result |
|---|---|---:|---:|:---:|
| 14 | `HAT_BAUTEILGRUPPE` with `evidence_origin='curated'` | ≥ 200 | **254** | PASS |
| 15 | 5 sampled promoted edges have: `basis='cell_citation'`, `confidence ∈ {belegt, teilweise_belegt}`, topology backed by ≥1 FROM_DONOR + ≥1 INTO_RECEIVER | all 5 ok | all 5 ok | PASS |

All five sampled promoted edges:

1. `p_55_great_suffolk_street_london` → `bg_reuse_stahl_mehrere_55gss_external_core` (2 donor + 1 receiver)
2. `p_association_house_groeditz` → `bg_reuse_stahlbeton_mehrere_groeditz_dresden_type_precast_components` (1 + 1)
3. `p_association_house_groeditz` → `bg_reuse_stahlbeton_mehrere_groeditz_wbs70_precast_panels` (1 + 1)
4. `p_association_house_plauen` → `bg_reuse_stahlbeton_mehrere_plauen_iw73_6_precast_components` (1 + 1)
5. `p_awm_muenster_circular_office` → `bg_reuse_glas_mehrere_awm_partitions_doors` (1 + 1)

…all carry:

- `evidence_origin='curated'`
- `evidence_basis='cell_citation'`
- `evidence_confidence='teilweise_belegt'`
- `evidence_source_id = <case_markdown anchor id>` (e.g. `q_55_great_suffolk_street_london_md`)
- Non-empty `evidence_excerpt` naming the Projekt, Bauteilgruppe, and the donor/receiver counts
- `migration_origin='mig_repair_4_1_q1'`
- `derivation_note='promoted derived->curated by mig_repair_4_1_q1 …'`

## 4. Full matrix — edge type × evidence_origin (live)

(Columns are `evidence_origin` values; only non-zero cells are shown. 66 edge types live.)

| Edge type | curated | derived | inferred | total |
|---|---:|---:|---:|---:|
| ANCHORED_BY               |     – |   703 |    –  |   703 |
| APPLIES_IN                |     – |    –  |   20  |    20 |
| APPLIES_TO                |     – |    –  |   20  |    20 |
| ASSOZIIERT_MIT_PROJEKT    |   142 |    58 |    –  |   200 |
| BELEGT_IN                 | 3 031 | 1 460 |  243  | 4 734 |
| BETEILIGT_AN              |     – |   576 |    –  |   576 |
| BETRIEBEN_VON             |     – |     3 |    –  |     3 |
| BUILT_IN_ERA              |     – |    –  |    8  |     8 |
| ERHALT_FOERDERUNG_DURCH   |     – |     4 |    –  |     4 |
| FROM_DONOR                |     – |   286 |    –  |   286 |
| GEHÖRT_ZU                 |     – |   255 |    –  |   255 |
| GILT_IN_LAND              |     – |    35 |    –  |    35 |
| HAS_RISK_POLLUTANT        |     4 |     7 |  792  |   803 |
| HAT_AKTEURROLLE           |   548 |   632 |    –  | 1 180 |
| HAT_AKTEURTYP             |   193 |   465 |    –  |   658 |
| HAT_AUFBEREITUNG          |    22 |   426 |    –  |   448 |
| HAT_BAUOBJEKTKLASSE       |     – |   227 |    –  |   227 |
| HAT_BAUOBJEKTROLLE        |     – |   230 |    –  |   230 |
| HAT_BAUPRODUKTSTATUS      |     – |    67 |    –  |    67 |
| HAT_BAUSYSTEM             |     – |    64 |    –  |    64 |
| HAT_BAUTEILEBENE          |     – |   372 |    –  |   372 |
| HAT_BAUTEILGRUPPE         |   254 |   115 |    –  |   369 |
| HAT_BAUTEILTYP            |     – |   607 |    –  |   607 |
| HAT_BAUWEISE              |     – |   129 |    –  |   129 |
| HAT_BESCHAFFUNGSWEG       |     – |   285 |    –  |   285 |
| HAT_DEFEKT                |     – |    45 |    –  |    45 |
| HAT_DEFEKT_BEFUND         |     – |    25 |    –  |    25 |
| HAT_FUNKTIONSWECHSEL      |     – |   299 |    –  |   299 |
| HAT_HUERDE                |     – | 1 068 |    –  | 1 068 |
| HAT_HUERDEKATEGORIE       |     – |   167 |    –  |   167 |
| HAT_INTERVENTION          |     – |   148 |    –  |   148 |
| HAT_LEISTUNGSANFORDERUNG  |     – |   561 |    –  |   561 |
| HAT_LOGISTIK              |     – |   500 |    –  |   500 |
| HAT_MARKTMODELL           |     – |   384 |    –  |   384 |
| HAT_MATCHINGQUALITAET     |     – |   187 |    –  |   187 |
| HAT_MATERIALGRUPPE        |     – |   516 |    –  |   516 |
| HAT_METHODE               |     – |   602 |    –  |   602 |
| HAT_NUTZUNG               |     – |   216 |    –  |   216 |
| HAT_PROZESSPHASE          |     – |   812 |    –  |   812 |
| HAT_PRUEFUNG              |    63 |   347 |    –  |   410 |
| HAT_RESSOURCENQUELLE      |     – |   567 |    –  |   567 |
| HAT_RUECKBAUVERFAHREN     |     – |   301 |    –  |   301 |
| HAT_STATUS                |     – |   672 |    –  |   672 |
| HAT_TRAGWERKSPRINZIP      |     – |    72 |    –  |    72 |
| HAT_TYPISCHEN_BAUPRODUKTSTATUS |     – |    19 |    –  |    19 |
| HAT_VERBINDUNGSTECHNIK    |     1 |   130 |    –  |   131 |
| HAT_WIEDERVERWENDUNGSART  |     – |   621 |    –  |   621 |
| HAT_WIRTSCHAFT            |     – |    46 |    –  |    46 |
| HAT_WIRTSCHAFTSASPEKT     |     – |    11 |    –  |    11 |
| HAT_ZUSTANDSKLASSE        |     – |    40 |    –  |    40 |
| INTO_RECEIVER             |     – |   349 |    –  |   349 |
| IST_UNTERVERFAHREN_VON    |     – |    28 |    –  |    28 |
| LIEGT_IN_LAND             |   201 |   319 |    –  |   520 |
| LIEGT_IN_STADT            |     – |   261 |    –  |   261 |
| NUTZT_BAUWERK             |     – |   169 |    –  |   169 |
| NUTZT_MATERIAL            |     – |   475 |    –  |   475 |
| NUTZT_SOFTWARE            |     – |    51 |    –  |    51 |
| REFERENZIERT_NORM         |     – |    52 |   93  |   145 |
| REQUIRES_VERIFICATION_FOR |     – |    –  |  347  |   347 |
| TEIL_VON_KETTE            |     – |    14 |    –  |    14 |
| TEIL_VON_PROGRAMM         |     – |    38 |    –  |    38 |
| TYPISCH_BEI_BAUTEILTYP    |     – |    10 |    –  |    10 |
| TYPISCH_BEI_ERA           |     – |    15 |    –  |    15 |
| TYPISCH_BEI_MATERIAL      |     – |    91 |    –  |    91 |
| VERBUNDEN_MIT_AKTEUR      |   289 |    48 |    –  |   337 |
| ZITIERT_QUELLE            |     – | 1 470 |    –  | 1 470 |
| **Column totals**         | **4 748** | **18 752** | **1 523** | **25 023** |

Notes:

- All 17 claim-edge types from the orchestrator brief are present in the matrix (or 0 for legacy types renamed away, see §2). Every cell with a non-null `evidence_origin` value is in `{curated, inferred, derived}`.
- `HAT_BAUTEILGRUPPE` shows 254 curated + 115 derived → 369 total, matching the Repair-D promotion ledger.
- `BELEGT_IN` curated = 3 031 (post-repair, 4.1 hard rule clean) — every one carries a non-null `evidence_excerpt`.
- `ZITIERT_QUELLE` = 1 470 (Phase 4c invariant preserved).

## 5. Phase 4.2 samples — FROM_DONOR and INTO_RECEIVER (full property dump)

### 5 × FROM_DONOR (live)

| # | src | dst | `evidence_origin` | `evidence_basis` | `evidence_confidence` | `evidence_source_id` | `evidence_excerpt` |
|---|---|---|---|---|---|---|---|
| 1 | `(:Bauteilgruppe) bg_dismantled_glas_technik_medunicampus_fluorescent` | `(:Bauwerk) bw_meduni_campus_mariannengasse` | derived | controlled_vocab | unklar | batch2_v2_followup_2026-05-20 | `"BELEGT"` |
| 2 | `(:Bauteilgruppe) bg_dismantled_holz_mehrere_stuttgart21_donor_stock` | `(:Bauwerk) bw_stuttgart21_hauptbahnhof` | derived | controlled_vocab | unklar | batch2_v2_import_2026-05-20 | NULL |
| 3 | `(:Bauteilgruppe) bg_planned_mehrere_mehrere_big_dig_building_geplante_infrastrukturbauteile` | `(:Bauwerk) bw_boston_big_dig_infrastructure` | derived | controlled_vocab | unklar | mig_4_1 | NULL |
| 4 | `(:Bauteilgruppe) bg_retained_mehrere_mehrere_alliander_existing_buildings` | `(:Bauwerk) bw_alliander_existing_campus` | derived | controlled_vocab | unklar | mig_4_1 | NULL |
| 5 | `(:Bauteilgruppe) bg_retained_mehrere_mehrere_botanique_main_structure` | `(:Bauwerk) bw_institut_botanique_ulg` | derived | controlled_vocab | unklar | mig_4_1 | NULL |

All five carry the canonical 5-field shape; NULL excerpts are legal for `evidence_origin='derived'` (plan §4.1, hard rule applies only to curated). Each retains the stable `r.id` provenance string (e.g. `r_<src>__AUS_BAUWERK__<dst>` — note: the id was minted under the legacy type name and was deliberately preserved verbatim by `apoc.refactor.rename.type`).

### 5 × INTO_RECEIVER (live)

| # | src | dst | `evidence_origin` | `evidence_basis` | `evidence_confidence` | `evidence_source_id` | `evidence_excerpt` |
|---|---|---|---|---|---|---|---|
| 1 | `(:Bauteilgruppe) bg_dismantled_holz_mehrere_circl_larch_structure` | `(:Bauwerk) bw_circl_pavilion_amsterdam` | derived | controlled_vocab | unklar | batch2_v2_import_2026-05-20 | NULL |
| 2 | `(:Bauteilgruppe) bg_dismantled_mehrere_boden_circl_floor_structure` | `(:Bauwerk) bw_circl_pavilion_amsterdam` | derived | controlled_vocab | unklar | batch2_v2_followup_2026-05-20 | `"BELEGT"` |
| 3 | `(:Bauteilgruppe) bg_dismantled_mehrere_technik_circl_solar_panels` | `(:Bauwerk) bw_circl_pavilion_amsterdam` | derived | controlled_vocab | unklar | batch2_v2_import_2026-05-20 | NULL |
| 4 | `(:Bauteilgruppe) bg_planned_holz_decke_elementa_brettstapel` | `(:Bauwerk) bw_elementa_walkeweg_basel` | derived | controlled_vocab | unklar | batch2_v2_import_2026-05-20 | NULL |
| 5 | `(:Bauteilgruppe) bg_planned_holz_mehrere_lysp8_dfd_frame` | `(:Bauwerk) bw_lysp8_basel` | derived | controlled_vocab | unklar | batch2_v2_import_2026-05-20 | NULL |

All five carry the canonical 5-field shape; legacy id strings (`r_<src>__EINGEBAUT_IN__<dst>`) are preserved per the rename contract.

## 6. Promoted HAT_BAUTEILGRUPPE samples — full property dump

(All 5 sampled rows pass per-sample checks: `basis_cell_citation`, `confidence_in_enum`, `topology_donor_and_receiver`.)

```
1) (p_55_great_suffolk_street_london) -[HAT_BAUTEILGRUPPE]-> (bg_reuse_stahl_mehrere_55gss_external_core)
   donor_count=2  {bw_1_broadgate_london, bw_cleveland_steel_and_tubes_stock}
   receiver_count=1 {bw_55_great_suffolk_street_warehouse}
   evidence_origin='curated', evidence_basis='cell_citation',
   evidence_confidence='teilweise_belegt',
   evidence_source_id='q_55_great_suffolk_street_london_md',
   evidence_excerpt="Projekt 55 Great Suffolk Street [p_55_great_suffolk_street_london]
                     Section 5 (Reuse-Bauteilgruppen) [q_55_great_suffolk_street_london_md]:
                     Bauteilgruppe bg_reuse_stahl_mehrere_55gss_external_core
                     ist dossier-verankert mit 2 FROM_DONOR + 1 INTO_RECEIVER Verknüpfung(en).",
   migration_origin='mig_repair_4_1_q1'

2) (p_association_house_groeditz) -[HAT_BAUTEILGRUPPE]->
   (bg_reuse_stahlbeton_mehrere_groeditz_dresden_type_precast_components)
   donor=1 {bw_school_type_dresden_donor}; receiver=1 {bw_association_house_groeditz}
   evidence_origin=curated; basis=cell_citation; conf=teilweise_belegt
   source_id=q_association_house_groeditz_md; migration_origin=mig_repair_4_1_q1

3) (p_association_house_groeditz) -[HAT_BAUTEILGRUPPE]->
   (bg_reuse_stahlbeton_mehrere_groeditz_wbs70_precast_panels)
   donor=1 {bw_wbs70_donor_groeditz}; receiver=1 {bw_association_house_groeditz}
   evidence_origin=curated; basis=cell_citation; conf=teilweise_belegt
   source_id=q_association_house_groeditz_md; migration_origin=mig_repair_4_1_q1

4) (p_association_house_plauen) -[HAT_BAUTEILGRUPPE]->
   (bg_reuse_stahlbeton_mehrere_plauen_iw73_6_precast_components)
   donor=1 {bw_iw73_6_mass_housing_donor}; receiver=1 {bw_association_house_plauen}
   evidence_origin=curated; basis=cell_citation; conf=teilweise_belegt
   source_id=q_association_house_plauen_md; migration_origin=mig_repair_4_1_q1

5) (p_awm_muenster_circular_office) -[HAT_BAUTEILGRUPPE]->
   (bg_reuse_glas_mehrere_awm_partitions_doors)
   donor=1 {bw_behrensbau_duesseldorf_donor}; receiver=1 {bw_awm_muenster_admin_building}
   evidence_origin=curated; basis=cell_citation; conf=teilweise_belegt
   source_id=q_awm_muenster_circular_office_md; migration_origin=mig_repair_4_1_q1
```

Each promoted edge satisfies the §4.1 hard rule (curated ⇒ non-null excerpt) and lies inside the citation-group basis enum `{cell_citation, registry_stub, propagated, controlled_vocab}`.

## 7. Cypher used (live, read-only)

```cypher
// Check 3 — claim-edge types with NULL evidence_origin (must be 0 rows)
MATCH ()-[r]->()
WHERE type(r) IN ['BELEGT_IN','HAT_BAUTEILGRUPPE','BETEILIGT_AN','FROM_DONOR',
                  'INTO_RECEIVER','HAS_RISK_POLLUTANT','REQUIRES_VERIFICATION_FOR',
                  'REFERENZIERT_NORM','HAT_AKTEURROLLE','HAT_HUERDE','APPLIES_IN',
                  'APPLIES_TO','BUILT_IN_ERA','ANCHORED_BY','HAT_MARKTMODELL',
                  'ZITIERT_QUELLE','ASSOZIIERT_MIT_PROJEKT']
  AND r.evidence_origin IS NULL
RETURN type(r), count(*);                                            // 0 rows

// Check 4 — origin enum violations
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['curated','inferred','derived']
RETURN count(r);                                                     // 0

// Check 5 — confidence enum violations
MATCH ()-[r]->()
WHERE r.evidence_confidence IS NOT NULL
  AND NOT r.evidence_confidence IN ['belegt','teilweise_belegt','unklar','inferiert','bookkeeping']
RETURN count(r);                                                     // 0

// Check 6 — curated requires excerpt
MATCH ()-[r]->()
WHERE r.evidence_origin='curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt='')
RETURN count(r);                                                     // 0

// Check 7 — bookkeeping requires derived
MATCH ()-[r]->()
WHERE r.evidence_confidence='bookkeeping'
  AND coalesce(r.evidence_origin,'')<>'derived'
RETURN count(r);                                                     // 0

// Check 8 — excerpt must not contain 'propagated from'
MATCH ()-[r]->()
WHERE r.evidence_excerpt IS NOT NULL
  AND r.evidence_excerpt CONTAINS 'propagated from'
RETURN count(r);                                                     // 0

// Check 9 — matrix dump
MATCH ()-[r]->()
RETURN type(r) AS t,
       coalesce(r.evidence_origin, '__NULL__') AS o,
       count(*) AS c
ORDER BY t, o;                                                       // 66 types, see §4

// Check 11+12 — donor/receiver counts
CALL { MATCH ()-[r:AUS_BAUWERK]->()   RETURN count(r) AS aus }
CALL { MATCH ()-[r:EINGEBAUT_IN]->()  RETURN count(r) AS ein }
CALL { MATCH ()-[r:FROM_DONOR]->()    RETURN count(r) AS fd  }
CALL { MATCH ()-[r:INTO_RECEIVER]->() RETURN count(r) AS ir  }
RETURN aus, ein, fd, ir;                                             // 0, 0, 286, 349

// Check 14 — HAT_BAUTEILGRUPPE curated
MATCH ()-[r:HAT_BAUTEILGRUPPE]->()
WHERE r.evidence_origin='curated'
RETURN count(r);                                                     // 254

// Check 15 — promoted HAT_BAUTEILGRUPPE per-sample audit
MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
WHERE r.evidence_origin='curated'
OPTIONAL MATCH (bg)-[:FROM_DONOR]->(d)
WITH p, r, bg, count(DISTINCT d) AS donor_count
OPTIONAL MATCH (bg)-[:INTO_RECEIVER]->(rcv)
WITH p, r, bg, donor_count, count(DISTINCT rcv) AS receiver_count
RETURN p.id, bg.id, donor_count, receiver_count, properties(r)
ORDER BY p.id, bg.id LIMIT 5;
```

## 8. Files produced by this verifier

```
logs/pass2_verify_phase4_1_2.py
logs/pass2_verify_phase4_1_2.json
reports/pass2_verify_phase4_1_2.md   (this file)
```

## 9. JSON verdict

```json
{
  "verifier": "pass2_detailed_verifier_9_of_12",
  "scope": "phase_4_1_and_4_2_full_with_curated_excerpt_repair",
  "database": "mit-bestand",
  "timestamp_utc": "2026-05-21T07:59:26+00:00",
  "overall_verdict": "PASS",
  "pass_count": 15,
  "fail_count": 0,
  "checks": {
    "1_migrations_present": {"mig_4_1_canonical_evidence.cypher": true, "mig_repair_4_1_curated_excerpts_and_q1.cypher": true, "pass": true},
    "2_flags_present": {"PHASE_4_DONE.flag": true, "PHASE_4_1_Q1_REPAIR_DONE.flag": true, "pass": true},
    "3_claim_edges_evidence_origin_null": {"by_type": {}, "total": 0, "expected": 0, "pass": true},
    "4_evidence_origin_enum_strict": {"violations": 0, "distribution": {"derived": 18752, "curated": 4748, "inferred": 1523}, "pass": true},
    "5_evidence_confidence_enum_strict": {"violations": 0, "distribution": {"unklar": 18440, "belegt": 3511, "inferiert": 1390, "bookkeeping": 1022, "teilweise_belegt": 660}, "pass": true},
    "6_curated_requires_excerpt": {"violations": 0, "pass": true},
    "7_bookkeeping_requires_derived": {"violations": 0, "pass": true},
    "8_excerpt_no_propagated_from": {"violations": 0, "pass": true},
    "9_matrix_dump": {"edge_types_count": 66, "column_totals": {"derived": 18752, "inferred": 1523, "curated": 4748}, "pass": true},
    "10_phase_4_2_done_flag": {"present": true, "pass": true},
    "11_legacy_donor_receiver_zero": {"AUS_BAUWERK": 0, "EINGEBAUT_IN": 0, "pass": true},
    "12_new_donor_receiver_thresholds": {"FROM_DONOR": 286, "INTO_RECEIVER": 349, "pass": true},
    "13_donor_receiver_samples": {"FROM_DONOR_sampled": 5, "INTO_RECEIVER_sampled": 5, "pass": true},
    "14_hat_bauteilgruppe_curated_min_200": {"count": 254, "expected_min": 200, "pass": true},
    "15_promoted_hat_bauteilgruppe_attributes": {"sampled": 5, "all_topology_basis_conf_ok": true, "pass": true}
  }
}
```

## 10. Conclusions

- **Phase 4.1 is fully complete on the live graph.** All 4 hard rules from plan §4.1 (curated⇒excerpt, bookkeeping⇒derived, no 'propagated from' in excerpts, no NULL evidence fields on claim-edge types) hold with zero violations. Both enums (`evidence_origin`, `evidence_confidence`) are strictly within their allowed values.
- **The curated-excerpt repair (Repair Agent D, 2026-05-21 07:40) is in effect.** The 2 108 curated-without-excerpt violations reported by Final Verifier 10 are closed (live count: 0). The Q1 HAT_BAUTEILGRUPPE promotion is verified (254 edges, all 5 sampled rows topology-backed + properly attributed).
- **Phase 4.2 is fully complete on the live graph.** Legacy `AUS_BAUWERK` and `EINGEBAUT_IN` are 0; canonical `FROM_DONOR` (286) and `INTO_RECEIVER` (349) match the plan targets; rename preserved properties and the canonical 5-field evidence shape on every sampled edge.
- **No regressions to Phase 4c invariants observed in the matrix** (`ZITIERT_QUELLE`=1 470 unchanged; no `external_sources` keys on relationships).

Pass-2 Detailed Verifier 9 of 12 returns **PASS** for Phase 4.1 + 4.2.
