# Apply order — batch2 v2 patches

**All 22 JSONL patches + 1 Cypher script generated and dry-run validated.** Sequence below is the apply order; each patch must be applied before its dependents.

## Pre-apply requirements

1. Take a fresh backup:
   ```
   python _scripts/backup_neo4j_graph.py --out-dir _neo4j/review/backups/batch2_v2_pre_apply
   ```
2. Confirm pre-flight validation is still clean:
   ```
   python _scripts/run_preflight_validation.py --cypher _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_validation.cypher --out _neo4j/intake/runs/2026-05-20_inbox_batch2_import/pre_flight_results_REAPPLY.json
   ```
3. Confirm `_neo4j/intake/runs/2026-05-20_inbox_batch2_import/predelete_snapshot.json` matches current live state for any deleted/merged node.

## Apply sequence

Apply each patch with: `python _scripts/apply_neo4j_review_patch.py --patch <path> --confirm "APPLY <filename> TO mit-bestand"`

| Step | Patch | Records | Operation summary | Depends on |
|---:|---|---:|---|---|
| 1 | phase_batch2_v2_1a_deletes.patch.jsonl | 5 | Delete bizh + dare_gmbh; strip 3 BELEGT_IN rels from p_obk_27 | (baseline) |
| 2 | phase_batch2_v2_1a2_delete_obk27.patch.jsonl | 1 | Delete p_obk_27 | step 1 |
| 3 | phase_batch2_v2_1b_akteur_merges.patch.jsonl | 5 | merge werner_sobek_p→Werner_Sobek; rotor_vzw+rotor_asbl_vzw→Rotor; rotor_dc→rotordc; zirkular_cirkla→zirkular_gmbh | (baseline) |
| 4 | phase_batch2_v2_1c_circl_merge.patch.jsonl | 3 | Pre-set Circl props on canonical; merge p_pavilion_circl_amsterdam→p_circl_abn_amro | (baseline) |
| 5 | phase_batch2_v2_1d_programm_merges.patch.jsonl | 6 | Enrich + merge p_fcrbe→prog_fcrbe, p_interreg_nwe_fcrbe→prog_fcrbe, p_reallabor_be_ware→prog_reallabor_be_ware; add prog_fcrbe→prog_interreg_nwe TEIL_VON_PROGRAMM | (baseline) |
| 6 | phase_batch2_v2_1d2a_programm_adds.patch.jsonl | 3 | Add prog_stuttgart_210, prog_rebridge, prog_re_use_hoefe | (baseline) |
| 7 | phase_batch2_v2_1d2b_programm_merges.patch.jsonl | 3 | Merge p_stuttgart_210, p_rebridge_*, p_re_use_hoefe into new Programmen | step 6 |
| 8 | phase_batch2_v2_2_shared_nodes.patch.jsonl | 36 | 14 Stadt + 3 Land + 8 Programm + 4 Software + 2 Tool + 4 Norm + 1 ZBS | (baseline) |
| 9 | phase_batch2_v2_2b_bauwerks.patch.jsonl | 13 | 13 new Bauwerk nodes (receivers + donors) | step 8 |
| 10 | phase_batch2_v2_2c_bauwerk_rels.patch.jsonl | 61 | Bauwerk → Stadt/Land/Status/Bauobjektrolle/Bauobjektklasse | steps 8, 9 |
| 11 | phase_batch2_v2_3a_quellen_case.patch.jsonl | 20 | 20 case_markdown Quellen (one per dossier; Interreg merges into FCRBE; OBK_27 omitted) | (baseline) |
| 12 | phase_batch2_v2_3b_belegt_in_edges.patch.jsonl | 41 | BELEGT_IN from new Stadt/Land/Bauwerk/Programm to their case Quelle | steps 8, 9, 11 |
| 13 | phase_batch2_v2_4a_projekt_promote.patch.jsonl | 17 | Promote 8 stub Projekte to full_projekt + 3 new child Projekte (Jugendtreff, Eggshell, Up Sticks) | (baseline) |
| 14 | phase_batch2_v2_4b_projekt_rels.patch.jsonl | 51 | BELEGT_IN + LIEGT_IN_* + NUTZT_BAUWERK + TEIL_VON_PROGRAMM + ERHALT_FOERDERUNG_DURCH per project | steps 8, 9, 11, 13 |
| 15 | phase_batch2_v2_5a_new_akteure.patch.jsonl | 30 (26 new + 4 noop) | New Akteur nodes for orgs + a few persons | (baseline) |
| 16 | phase_batch2_v2_5b_akteur_typed_rels.patch.jsonl | 81 (73 new + 8 noop) | HAT_AKTEURROLLE + HAT_AKTEURTYP + BETEILIGT_AN + ERHALT_FOERDERUNG_DURCH | step 15 |
| 17 | phase_batch2_v2_5c_gehoert_zu.cypher | manual | GEHÖRT_ZU Person→Org rels (apply tool umlaut limitation — direct Cypher) | step 15 |
| 18 | phase_batch2_v2_6a_bg_addnodes.patch.jsonl | 42 | 42 new Bauteilgruppen with required properties (alte_funktion / neue_funktion for FW cases) | (baseline) |
| 19 | phase_batch2_v2_6b_bg_rels.patch.jsonl | 384 | BG vocab + project + Bauwerk + Funktionswechsel rels (HAT_BAUTEILEBENE, HAT_STATUS, HAT_RESSOURCENQUELLE, HAT_BAUTEILTYP, HAT_MATERIALGRUPPE, HAT_WIEDERVERWENDUNGSART, BELEGT_IN, HAT_BAUTEILGRUPPE, EINGEBAUT_IN, AUS_BAUWERK, HAT_MATCHINGQUALITAET) | steps 8, 9, 11, 13, 18 |
| 20 | phase_batch2_v2_7a_ketten_addnodes.patch.jsonl | 9 | 9 Wiederverwendungsketten (wk_* prefix per Z C10 override) | (baseline) |
| 21 | phase_batch2_v2_7b_kette_rels.patch.jsonl | 25 | TEIL_VON_KETTE + AUS_BAUWERK/EINGEBAUT_IN to ketten | steps 9, 18, 20 |
| 22 | phase_batch2_v2_8_project_vocab.patch.jsonl | 73 | Project-level vocab edges (Plan 1 Phase 8 restored: HAT_INTERVENTION, HAT_NUTZUNG, HAT_METHODE, HAT_DOMINANT_*, NUTZT_SOFTWARE, NUTZT_TOOL, HAT_ZERTIFIZIERUNG, REFERENZIERT_NORM) | step 8, 13 |
| 23 | phase_batch2_v2_9_bridges.patch.jsonl | 23 | Cross-project bridges (Rotor + RotorDC + TU Delft + Zirkular + Assemble + BauKarussell + Concular + La Fab + Persons-to-programmes) | steps 13, 15 |
| **24** | **phase_batch2_v2_4c_eth_merge.patch.jsonl** | **1** | **MERGE p_eth_circular_construction_student_reuse → prog_mas_dfab (aliases UNION; 8 rels redirected)** | **step 8 (prog_mas_dfab) + step 14 (children attached)** |
| **25** | **phase_batch2_v2_4d_rcmi_strip.patch.jsonl** | **5** | **Strip BELEGT_IN x2 + ASSOZIIERT x1 from p_rcmi_concular; re-route Dominik → tool_rcmi + concular** | **step 8 (tool_rcmi)** |
| **26** | **phase_batch2_v2_4d2_rcmi_delete.patch.jsonl** | **1** | **Delete p_rcmi_concular** | **step 25** |
| **27** | **phase_batch2_v2_4e_refair_strip.patch.jsonl** | **8** | **Strip BELEGT_IN x3 + ASSOZIIERT x2 from p_refair_bordeaux_reemploi_platform; re-route Orianne + Tiphaine → la_fab + La Fab NUTZT_BAUWERK depot** | **step 15 (la_fabrique...)** |
| **28** | **phase_batch2_v2_4e2_refair_delete.patch.jsonl** | **1** | **Delete p_refair_bordeaux_reemploi_platform** | **step 27** |
| **29** | **phase_batch2_v2_10_huerde_wirtschaft.patch.jsonl** | **72** | **Project-level HAT_HUERDE + HAT_WIRTSCHAFT + HAT_DOMINANT_AKZEPTANZ (CORRECTIONS O7 cont.)** | **steps 13, 24** |
| **30** | **phase_batch2_v2_11_bg_vocab.patch.jsonl** | **357** | **BG-level optional vocab: HAT_BESCHAFFUNGSWEG, HAT_VERBINDUNGSTECHNIK, HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG, HAT_LOGISTIK, HAT_PRUEFUNG, HAT_DEFEKT, HAT_ZUSTANDSKLASSE, HAT_BAUPRODUKTSTATUS, HAT_LEISTUNGSANFORDERUNG, HAT_SCHADSTOFF, HAT_MARKTMODELL, NUTZT_MATERIAL** | **step 18** |
| **31** | **phase_batch2_v2_12a_deferred_bg_addnodes.patch.jsonl** | **19** | **19 deferred Bauteilgruppen (Circl extended, MedUni, BE-WARE TULIUM, RE_USE Höfe, Ingersheim secondary, Granby first house + bespoke)** | (baseline) |
| **32** | **phase_batch2_v2_12b_deferred_bg_rels.patch.jsonl** | **236** | **Mandatory 7 rels + Project + Bauwerk links + optional vocab for 19 deferred BGs** | **steps 8, 9, 11, 13, 31** |
| **33** | **phase_batch2_v2_13a_more_actors_addnodes.patch.jsonl** | **67 (60 new + 7 noop)** | **~60 truly new Akteure (UMAR suppliers, ELEMENTA team, SMS team, LysP8 + Zirkular team, MedUni Persons, Stuttgart 210 + Ingersheim Persons + funders, Granby CIC, Circl additional, RE-USE Höfe Persons, Urban Bricolage core, REFAIR Persons, RCMI Persons, FCRBE partners)** | (baseline) |
| **34** | **phase_batch2_v2_13b_more_actors_rels.patch.jsonl** | **201** | **HAT_AKTEURROLLE + HAT_AKTEURTYP + BETEILIGT_AN for all new actors** | **step 33** |
| **35** | **phase_batch2_v2_14_external_quellen.patch.jsonl** | **17** | **17 external_reference Quellen for high-value source URLs (Circl × 5, Careno × 2, LysP8 × 3, MedUni × 1, Stuttgart 210 × 2, FCRBE × 1, REBRIDGE × 1, Granby × 2)** | (baseline) |
| **36** | **phase_batch2_v2_15_gehoert_zu_full.cypher** | **manual** | **~38 GEHÖRT_ZU Person→Org edges via direct Cypher (apply-tool umlaut limit)** | **steps 15, 33** |

**Total: 1869 ops + 1 Cypher script (~38 GEHÖRT_ZU MERGEs).**

### Insertion notes for steps 29-36

- Steps 29-30 (Phases 10-11) add project-level + BG-level optional vocab. These are pure rel additions, no new nodes. Can run any time after steps 8, 13, 18.
- Steps 31-32 (Phase 12) add the 19 deferred BGs + their full rel set. Step 32 depends on step 31 (BGs created) plus prior shared infrastructure.
- Steps 33-34 (Phase 13) add ~60 more Akteure (UMAR/ELEMENTA/SMS/LysP8/MedUni/etc.) + typed rels. The 7 noop_existing in step 33 are actors S27 confirmed already exist (e.g., `gemeinde_ingersheim` may have a near-name match).
- Step 35 (Phase 14) is independent — 17 standalone Quelle nodes. Can run early.
- Step 36 (Phase 15) is the direct-Cypher GEHÖRT_ZU expansion; depends on Phases 5a + 13a having created the target Persons + Orgs.

**Updated total: ~1870 ops across 36 JSONL patches + 1 Cypher script.**

### Insertion notes

- Steps 24-28 close the "3 missing migrations" gap (ETH parent stub, RCMI, REFAIR). After step 28 applied, `count(:Projekt)` drops by 3 (to 96 net) and the 3 orphan stubs are gone.
- Steps 24-28 must run AFTER their prerequisites:
  - Step 24 needs `prog_mas_dfab` (step 8).
  - Steps 25-26 need `tool_rcmi` + `concular` (steps 8, 15).
  - Steps 27-28 need `la_fabrique_de_bordeaux_metropole` + `software_refair` + `bw_base_du_reemploi_merignac` (steps 8, 9, 15).
- Recommended insertion point: **after step 23 (Phase 9 bridges)**, as the final cleanup before verification.

After each step, verify with:
- Patch-specific verification block from PLAN_v2 Phase 10
- Append result to `_neo4j/review/round_002_followup/rollback.md`

## Final verification

After all 23 steps, run:

```cypher
// 1. Final state
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;
// EXPECTED: ~2495 nodes / ~18800 rels after all 36 patches (delta: +197 nodes, +1765 rels)
// Nodes: +135 batch2 v2 (steps 1-28) + 19 deferred BGs (step 31) + 60 more Akteure (step 33) - 3 orphan stubs = +211 raw, but the 5 ":Programm:Projekt" dual-labels count once each (no node growth) → ~+197 net
// count(:Projekt) net: -3 (orphans) + 3 new children + 5 dual-labels still counted - 2 pure-Projekt merges (pavilion, interreg) - 1 OBK = 99 + 2 = ~101 or 96 depending on label-count interpretation (per discussion in B5)
// count(:Programm) net: +11 → 28

// 2. No fabricated rel types
MATCH ()-[r]->() WHERE type(r) IN ['HAT_SOFTWARE','HAT_TOOL','HAT_NORM',
  'HAT_BAUAUFGABE','HAT_AKZEPTANZ','HAT_AUFBEREITUNGSVERFAHREN',
  'HAT_PRUEFUNG_NACHWEIS','LIEFERT_MATERIAL_AUS','VERBUNDEN_MIT','LIEGT_IN']
RETURN type(r), count(*);
// EXPECTED: 0 rows

// 3. r.id integrity
MATCH ()-[r]->() WHERE r.id IS NULL
   OR r.id <> 'r_' + startNode(r).id + '__' + type(r) + '__' + endNode(r).id
RETURN type(r), count(*);
// EXPECTED: 0 rows

// 4. Deleted nodes confirmed
MATCH (n) WHERE n.id IN [
  'p_obk_27','bizh','dare_gmbh','rotor_vzw','rotor_asbl_vzw',
  'werner_sobek_p','rotor_dc','zirkular_cirkla',
  'p_pavilion_circl_amsterdam','p_fcrbe','p_interreg_nwe_fcrbe',
  'p_reallabor_be_ware','p_stuttgart_210','p_rebridge_structural_reuse_project',
  'p_re_use_hoefe'
] RETURN n.id;
// EXPECTED: 0 rows (all consumed by merges or deletes)

// 5. New nodes exist
MATCH (n) WHERE n.id IN [
  'bw_circl_pavilion_amsterdam','bw_umar_unit_duebendorf','bw_ubs_altstetten',
  'prog_be_circular','prog_nest_empa','tool_retile','software_llmnt',
  'wk_stuttgart21_clt_to_ingersheim','wk_wabbes_handles_to_umar',
  'bg_reuse_metall_tuer_umar_wabbes_handles','p_jugendtreff_ingersheim'
] RETURN n.id, labels(n);
// EXPECTED: 11 rows

// 6. Funktionswechsel hub got new incoming edges
MATCH (bg:Bauteilgruppe)-[:HAT_MATCHINGQUALITAET]->(mq:MatchingQualitaet {id:'mq_spec_zweckaenderung'})
WHERE bg.source_scope = 'case_markdown'
RETURN count(bg) AS new_funktionswechsel_bgs;
// EXPECTED: ~7

// 7. New Programm nodes have typed properties
MATCH (p:Programm) WHERE p.id IN ['prog_rebridge','prog_fcrbe','prog_be_circular','prog_mas_dfab','prog_stuttgart_210']
RETURN p.id, p.start_year, p.end_year, p.status, p.eu_funding_programme;

// 8. Every new Akteur has HAT_AKTEURROLLE + HAT_AKTEURTYP
MATCH (a:Akteur) WHERE a.source_scope = 'case_markdown'
  AND NOT EXISTS { (a)-[:HAT_AKTEURROLLE]->() }
RETURN a.id LIMIT 10;
// EXPECTED: 0 rows
```

## Rollback procedure

If any step fails or produces unwanted results:

1. Note the failed step number.
2. Restore from `_neo4j/review/backups/batch2_v2_pre_apply/`:
   ```
   python _scripts/restore_neo4j_graph_backup.py --backup-dir _neo4j/review/backups/batch2_v2_pre_apply
   ```
3. Investigate failure, amend the patch, re-validate, re-run from step 1.

## Notes

- **Phase 5c (GEHÖRT_ZU)** uses direct Cypher because the apply tool's regex (`^[A-Za-z_][A-Za-z0-9_]*$`) rejects relationship types containing umlauts. The live graph has 216 existing GEHÖRT_ZU rels — these are added by direct MERGE.
- Several `noop_existing` results in dry-runs are intentional — the apply tool's idempotency safely no-ops when nodes/rels already exist.
- `missing_endpoint` in dry-runs is expected for ops that depend on prior phases creating their target nodes. Live apply with sequential phase order resolves these.
- `phase_batch2_v2_5c_gehoert_zu.cypher` is a starter template — extend with additional Person→Org pairs as the patch generator's Phase 5b emits new Persons (the file lists only hans_hammink and dominik_campanella; add per actor_extraction_per_dossier.md O5 table).
