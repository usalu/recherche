# Stub-Projekt research workflow

**Goal:** turn the 23 remaining `cross_reference_stub` Projekt nodes into full case studies, using external ChatGPT/perplexity research. Each batch document below covers ≤ 5 projects in a single category.

## Workflow per batch

For each project in a batch:

1. **Hand the batch document to ChatGPT** (or similar). It contains the schema, the concrete example, and a per-project research checklist.
2. **ChatGPT produces two files:**
   - `_archive/research/gebaeude/<ProjectName>.md` — narrative case study, same template as the existing 76 archive files.
   - `_neo4j/intake/inbox/stub_promotion/<pid>.kg.jsonl` — JSONL records matching the contract in [`_neo4j/contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json`](../../../contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json).
3. **You review** the two files, fix any errors, then trigger a small import patch that:
   - Drops `node_role: cross_reference_stub` from the Projekt
   - Adds `node_role: full_projekt`, `promoted_at`, `promoted_reason`
   - Loads the new JSONL records (idempotent — existing rels stay)

## Reference example

The single best concrete example is **K.118 / Kopfbau Halle 118, Winterthur**:
- Archive markdown: [`_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md`](../../../../_archive/research/gebaeude/K118_Kopfbau_Halle_118_Winterthur.md) — see in particular Sections 2 (ENTITÄTEN-MAPPING), 5 (BAUTEIL-INVENTAR), 6 (PROZESS UND LOGISTIK), 7 (TECHNIK, LEISTUNG, NORMEN), 8 (KENNWERTE).
- JSONL chunk pattern: [`_neo4j/intake/archive/2026-05-15_project_batches_legacy/raw_tree/neo4j_batch_001_exports/batches/batch_001/p_berlin_schildow_pilot_house.kg.jsonl`](../../../intake/archive/2026-05-15_project_batches_legacy/raw_tree/neo4j_batch_001_exports/batches/batch_001/p_berlin_schildow_pilot_house.kg.jsonl) — shows full node + rel pattern for a small project.
- Contract: [`_neo4j/contracts/project_batches_v1_1/`](../../../contracts/project_batches_v1_1/) — README, schema, controlled vocab seed.

## Schema (what each project file must produce)

Every project chunk emits **nodes** (one of these labels — see [schema enum](../../../contracts/project_batches_v1_1/schemas/kg_jsonl_record_schema.json)):

`Projekt`, `Bauwerk`, `Bauteilgruppe`, `Akteur`, `Quelle`, `Wiederverwendungskette`, `Stadt`, `Land`, plus references to controlled vocabularies for `Material`, `Bauteiltyp`, `Bauteilebene`, `Bauobjektklasse`, `Bauobjektrolle`, `Akteurrolle`, `Akteurtyp`, `WiederverwendungsArt`, `Status`, `Nutzung`, `Prozessphase`, `PruefungNachweis`, `Leistungsanforderung`, `Norm`, `Aufbereitungsverfahren`, `Rueckbauverfahren`, `Beschaffungsweg`, `Ressourcenquelle`, `Logistik`, `Methode`, `Verbindungstechnik`, `RechtlicheBedingung`, `Schadstoff`, `Wirtschaft`, `ZertifizierungBewertungssystem`, `Tragwerksprinzip`, `Bauweise`, `Bausystem`, `Funktionswechsel`, `BauaufgabeIntervention`, `Programm`, `Software`, `Tool`, `BauwerkEra`, `Bauproduktstatus`, `LebenszyklusModul`, `Layer`, `Marktmodell`, `Defekt`, `MatchingQualitaet`, `ZustandsKlasse`, `Akzeptanz`.

The full relationship-type enum is also in the schema — 67 types in active use.

## ID convention

| Node type | Prefix | Example |
|---|---|---|
| Projekt | `p_` | `p_k118_kopfbau_halle_118_winterthur` |
| Bauwerk | `bw_` | `bw_winterthur_industriehalle_118` |
| Bauteilgruppe | `bg_` | `bg_k118_stahltraeger_aus_elys_basel` |
| Akteur | (slug only) | `baubuero_in_situ`, `stiftung_abendrot` |
| Quelle | `q_` | `q_k118_archive_md` |
| Stadt | `stadt_` | `stadt_winterthur` |
| Land | `land_` | `land_schweiz` |

Rel IDs follow `r_<from_id>__<TYPE>__<to_id>`.

## Controlled vocab — reuse, don't redefine

The most-used existing IDs (ChatGPT should reuse these instead of inventing new ones):

**Materials:** `mat_stahl`, `mat_holz`, `mat_beton`, `mat_stahlbeton`, `mat_glas`, `mat_naturstein`, `mat_aluminium`, `mat_ziegel`, `mat_mdf`, `mat_lehm`, `mat_stroh`.

**Bauteiltyp:** `bt_traeger`, `bt_stuetze`, `bt_wand`, `bt_decke`, `bt_dach`, `bt_fenster`, `bt_tuer`, `bt_fassade`, `bt_treppe`, `bt_fundament`, `bt_belag_boden`.

**Akteurrolle:** `ar_architektur`, `ar_tragwerksplanung`, `ar_bauherr_auftraggeber`, `ar_bauausfuehrung`, `ar_rueckbau_demontage`, `ar_aufbereitung_refurbishment`, `ar_reuse_beratung`, `ar_forschung_dokumentation`, `ar_materiallieferant`, `ar_oeffentliche_hand`, `ar_brandschutz_barrierefreiheit`, `ar_fassade`, `ar_tga_gebaeudetechnik`.

**Akteurtyp:** `at_person`, `at_organisation`, `at_unternehmen`, `at_oeffentliche_institution`, `at_forschung_lehre`, `at_ngo_netzwerk`, `at_verband_kammer`, `at_materialhub_bauteilboerse`, `at_foerdergeber_programmtraeger`.

**Land:** `land_schweiz`, `land_deutschland`, `land_oesterreich`, `land_belgien`, `land_niederlande`, `land_frankreich`, `land_vereinigtes_koenigreich`, `land_daenemark`, `land_finnland`, `land_norwegen`, `land_luxemburg`, `land_usa`, `land_japan`, `land_international`.

**WiederverwendungsArt:** `wva_direkte_wiederverwendung`, `wva_aufbereitung_und_wiederverwendung`, `wva_zweckaenderung`, `wva_recycling`.

**Status:** `status_realisiert`, `status_in_planung`, `status_studie`, `status_pilot`.

**Methode (existing 13):** `meth_form_follows_availability`, `meth_reuse_assessment`, `meth_bauteilkatalogisierung`, `meth_building_material_scouting`, `meth_design_for_disassembly`, `meth_reversibilitaet`, `meth_materialinventur`, `meth_reuse_ausschreibung`, `meth_pre_deconstruction_audit`, `meth_urban_mining`, `meth_wiederverwendungskriterien`, `meth_abrissmonitoring`, `meth_zirkulaere_ausschreibung`.

Full vocab seed: [`controlled_vocabulary.seed.kg.jsonl`](../../../contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl) (385 entries).

## Where stub Projekte come from

All 23 stubs were created during the actor-registry seed: an `ASSOZIIERT_MIT_PROJEKT` edge from one or more Akteur nodes pointed at a project name that had no archive file. The project node was created as a placeholder. We now want to replace each placeholder with a real, sourced case study.

The Akteure already attached to each stub are listed in each batch document under "Existing actor links" so ChatGPT doesn't lose those references.

## Batch index

| # | Batch | Projects | Decision |
|---|---|---:|---|
| 1 | [Swiss pilots](batch_01_swiss_pilots.md) | 3 | Promote to full Projekt |
| 2 | [DE/AT large urban](batch_02_de_at_large.md) | 5 | Promote to full Projekt |
| 3 | [BE/NL case study buildings](batch_03_be_nl_buildings.md) | 3 | Promote (+ 1 merge candidate) |
| 4 | [UK + unclear](batch_04_uk_unclear.md) | 2 | Promote (or delete obk_27 if unidentifiable) |
| 5 | [Teaching/research programs](batch_05_teaching_programs.md) | 4 | Relabel `Projekt` → `Programm` after research |
| 6 | [EU-funded consortia](batch_06_eu_consortia.md) | 4 | Relabel `Projekt` → `Programm` after research |
| 7 | [Reuse platforms / tools](batch_07_reuse_platforms.md) | 2 | Relabel `Projekt` → `Plattform` or `Tool` after research |

Total: 23 stubs.
