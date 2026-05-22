# Semantic Conflict Audit — Reuse Taxonomy Integration

**Generated:** 2026-06-03 (revised after live-graph connection analysis)
**Scope:** Conflicts between the v9 connection-expansion batches in [\_neo4j/intake/inbox/research/new taxonomy edit/](../../intake/inbox/research/new%20taxonomy%20edit/) and the live `mit-bestand` graph.
**Reference docs:**
- [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md) is now the authoritative source for delete-vs-migrate decisions per edge type (this document gives the high-level semantic resolution; the connection-type audit gives the per-edge policy).
- [CURRENT_SCHEMA_GUIDE.md](../2026-06-01_current_schema_guide/CURRENT_SCHEMA_GUIDE.md) is the live-schema baseline.

**Purpose:** Decide *now*, before any Cypher is staged, where the batches must adapt to the existing schema so we don't create duplicates, parallel vocabularies, or semantic collisions.

The conflicts below are listed in order of blast radius. Each has a **recommended resolution** marked `→` and a **decision-needed** flag where the user's input is required before staging.

---

## C1. `Quelle` collision (label name, two completely different meanings) **— DECIDED: use `:Ressourcenquelle`**

| Side | Meaning | Count | Linked via |
|---|---|---:|---|
| Live `:Quelle` | **Evidence/citation source** — URLs, research docs, PDFs | 5,330 | `BELEGT_IN`, `CITED_FROM_DOSSIER`, `ZITIERT_QUELLE` |
| Batch `Quelle` | **Material origin** — where the physical reused material came from | 350 rows | `HAT_QUELLE` |

User flagged this and proposed renaming batch `Quelle` → `Herkunft`.

**Finding during audit:** the live schema already has a **`:Ressourcenquelle`** vocabulary (16 nodes, **482 existing `HAT_RESSOURCENQUELLE` edges**) that is *semantically identical* to what the batches call `Quelle`. Existing nodes map almost 1:1 to batch buckets:

| Batch `Quelle` canonical | Existing `:Ressourcenquelle` |
|---|---|
| `Externer_Spenderbau` (190) | `rq_donorgebaeude` |
| `Eigener_Bestand` (55) | `rq_baustelle` (+ project context) |
| `Gleicher_Standort` (17) | `rq_baustelle` |
| `Bauteilmarkt_oder_Lager` (19) | `rq_bauteilboerse` / `rq_haendler` / `rq_lager` |
| `Leihgabe_oder_Service` (4) | `rq_borrowed_material_pool` |
| `Restposten_Abfall_Unbekannt` (65) | `rq_construction_waste_stream` / `rq_demolition_waste_stream` / `rq_surplus_stock` / `rq_produktionsueberschuss` / `rq_reclaimed_stock` / `rq_unbekannt` / `rq_unknown_documented_source` |

→ **Decision (revised after live-graph analysis):** keep `:Ressourcenquelle` as the label and `HAT_RESSOURCENQUELLE` as the rel. **Hard-delete all 16 live `rq_*` nodes** and MERGE 6 new canonical with batch-matching ids: `rq_externer_spenderbau`, `rq_eigener_bestand`, `rq_gleicher_standort`, `rq_bauteilmarkt_oder_lager`, `rq_leihgabe_oder_service`, `rq_restposten_abfall_unbekannt`. Live `rq_*` ids don't match batch canonicals, so the cleanest path is delete-and-recreate (consistent with user's "no legacy" rule). Only the 1 `:Materialdepot → :Ressourcenquelle` edge gets migrated; the other 551 inbound from `:Bauteilgruppe`/`:Projekt` are deleted because batches re-supply them. See [CONNECTION_TYPE_AUDIT.md §Ressourcenquelle](CONNECTION_TYPE_AUDIT.md#ressourcenquelle-16--6-new-canonical-with-new-ids).

---

## C2. `Methode` is already a populated controlled vocabulary **— DECIDED: option (a) replace, batches are the source of truth**

| | Live `:Methode` (`HAT_METHODE`, 404 edges) | Batch `Methode` (`NUTZT_METHODE`, 269 rows) |
|---|---|---|
| Node count | 13 | 6 |
| Sample | `meth_urban_mining`, `meth_form_follows_availability`, `meth_design_for_disassembly`, `meth_reuse_assessment` | `Urban_Mining_und_Scouting`, `Verfuegbarkeitsbasiertes_Design`, `Reversibles_Design`, `Bestands_und_ReUse_Assessment` |

The batches use a **coarser** vocabulary (6 buckets) over the **same axis** already covered by 13 fine-grained `meth_*` nodes. The retirement prompt says "do not expand the six-node vocabulary" but the live graph is already richer than six.

→ **Decision:** the batch's 6 buckets are the new canonical. The 13 live `meth_*` are too generic and lack row-level evidence — replace them.

**New canonical nodes to MERGE (id prefix kept as `meth_*` for schema continuity):**

| Batch canonical | New live id | Existing `meth_*` to fold in |
|---|---|---|
| `Urban_Mining_und_Scouting` | `meth_urban_mining_und_scouting` | `meth_urban_mining`, `meth_building_material_scouting` |
| `Bestands_und_ReUse_Assessment` | `meth_bestands_und_reuse_assessment` | `meth_reuse_assessment`, `meth_pre_deconstruction_audit` |
| `Verfuegbarkeitsbasiertes_Design` | `meth_verfuegbarkeitsbasiertes_design` | `meth_form_follows_availability`, `meth_wiederverwendungskriterien` |
| `Reversibles_Design` | `meth_reversibles_design` | `meth_design_for_disassembly`, `meth_reversibilitaet` |
| `Zirkulaere_Beschaffung` | `meth_zirkulaere_beschaffung` | `meth_reuse_ausschreibung`, `meth_zirkulaere_ausschreibung` |
| `Dokumentation_und_Monitoring` | `meth_dokumentation_und_monitoring` | `meth_bauteilkatalogisierung`, `meth_materialinventur`, `meth_abrissmonitoring` |

→ **Delete-with-targeted-migration policy** (revised after live-graph analysis revealed 74 edges from upstream types that batches don't re-supply):

1. MERGE the 6 new canonical nodes with `source_scope = 'controlled_vocab_seed'`.
2. **MIGRATE** the 74 inbound edges from non-replaceable upstreams (`:Akteur` 58, `:Software`/`:Tool` 15, `:Norm` 1) to the new canonical per the map. These reattach with `legacy_methode_id`/`legacy_methode_name` provenance.
3. **DELETE** the 591 inbound edges from `:Bauteilgruppe` (397) and `:Projekt` (194) — batches re-supply these in Phase 5 directly.
4. **Delete or trim DataIssues** that CONCERN the old `meth_*` nodes (per [CONNECTION_TYPE_AUDIT.md §DataIssue policy](CONNECTION_TYPE_AUDIT.md#dataissue-policy-3824-concerns-edges-across-all-5-vocabs)).
5. **Hard-DELETE** all 13 old `meth_*` nodes — no `:Methode_Legacy` survives. The user's "no legacy" rule trumps preserving DataIssue lineage.

→ **Relationship type:** keep `HAT_METHODE`. Do **not** introduce `NUTZT_METHODE` — that would double the axis.

---

## C3. `Rueckbauverfahren` already exists with overlapping vocabulary **— SEMANTIC MERGE**

| | Live `:Rueckbauverfahren` | Batch `Rueckbauverfahren` |
|---|---|---|
| Node count | 5 active (id prefix is `rv_*`, **not** `rbv_*` as the schema doc shows) | 6 canonical + 4 still-aliased |
| Rel | `HAT_RUECKBAUVERFAHREN` (299 edges) ✓ same as batch | same |

→ Mapping table:

| Batch canonical | Existing `rv_*` |
|---|---|
| `Selektiver_Rueckbau` (29) | `rv_selektiver_rueckbau` ✓ |
| `Ausbau_von_Bauteilen` (4) | `rv_ausbau_von_bauteilen` ✓ |
| `Demontage` (38) | `rv_demontage` ✓ |
| `Zerstoerungsarme_Bergung` (48) | `rv_zerstoerungsarme_bergung` ✓ |
| `Schneidender_Rueckbau` (3) | **add new** `rv_schneidender_rueckbau` (also fold `rv_betonfraesen` into it as detail) |
| `Integrierter_Rueckbau_und_Lagerung` (7) | **add new** `rv_integrierter_rueckbau_und_lagerung` |

→ Coverage report calls these still-needing-normalization in batches 07/08: `Sortierung_und_Bergung` (41) → `Zerstoerungsarme_Bergung`; `Dekonstruktion_mit_Inventar` (28) → `Selektiver_Rueckbau`; `Demontage_von_Modulen` (22) → `Demontage`. **Fix in batch Markdown before staging.**

---

## C4. `Aufbereitungsverfahren` has 62 detailed nodes — batches want 6 **— DECIDED: option (a) replace, aggressive cleanup**

| | Live `:Aufbereitungsverfahren` | Batch `Aufbereitungsverfahren` |
|---|---|---|
| Node count | **62 in schema header, 11 active in the round-002 review** (id prefix `av_*`, **not** `auf_*` as the schema doc says — naming drift) | 6 canonical |
| Rel | `HAT_AUFBEREITUNG` (411 edges) ✓ same |  |

→ **Decision:** same aggressive policy as C2. Batch 6 buckets are canonical. Replace.

**New canonical nodes to MERGE (id prefix kept as `av_*`):**

| Batch canonical | New live id | Existing `av_*` to fold in |
|---|---|---|
| `Reinigung_und_Oberflaeche` (34) | `av_reinigung_und_oberflaeche` | `av_reinigung` |
| `Zuschnitt_und_Vereinzelung` (45) | `av_zuschnitt_und_vereinzelung` | `av_zuschnitt`, `av_drahtglasschneiden`, `av_entmoertelung_von_fliesen` |
| `Pruefung_Sortierung_QS` (106) | `av_pruefung_sortierung_qs` | `av_qualitaetssicherung` |
| `Reparatur_und_Refurbishment` (32) | `av_reparatur_und_refurbishment` | `av_reparatur`, `av_rekonditionierung`, `av_leuchten_refurbishment` |
| `Remanufacturing_und_Upcycling` (45) | `av_remanufacturing_und_upcycling` | `av_remanufacturing`, `av_holzaufbereitung` |
| `Verstaerkung_und_Schutz` (6) | `av_verstaerkung_und_schutz` | `av_verstaerkung` |

→ The 62-vs-11 gap (schema doc says 62, round-002 review showed 11 active): the remaining ~51 are likely orphans (zero inbound). They get the same pre-deletion-scan-then-delete-or-relabel policy as C2.

→ **Delete-with-targeted-migration policy:**

1. MERGE the 6 new canonical with `source_scope = 'controlled_vocab_seed'`.
2. **MIGRATE** 40 `:ReuseRule → :Aufbereitungsverfahren` inbound edges to new canonical (preserved provenance).
3. **MIGRATE + DEDUPE** 47 outbound edges: 22 `TYPISCH_BEI_MATERIAL → :Material` and 25 `BELEGT_IN → :Quelle:ResearchDocument`. The MERGE on the new canonical's outbound side dedupes when multiple old `av_*` collapse to one new bucket.
4. **DELETE** 433 inbound edges from `:Bauteilgruppe` (411) and `:Projekt` (22) — batches re-supply.
5. **Delete or trim DataIssues** concerning old `av_*` (per DataIssue policy).
6. **Hard-DELETE** all 33 old `av_*` nodes. No `:Aufbereitungsverfahren_Legacy`.

→ Coverage report still-needing-normalization in batches: `Rekonfiguration_und_Vormontage` (16) → `Remanufacturing_und_Upcycling`; `Zuschnitt_und_Anpassung` (14) → `Zuschnitt_und_Vereinzelung`; `Keine_wesentliche_Aufbereitung` (3) → `Pruefung_Sortierung_QS`. Also fix in Markdown.

---

## C5. `WiederverwendungsArt` is being split across **three** new dimensions **— RETIREMENT**

The retirement prompt's main job. Old `:WiederverwendungsArt` (11 nodes, 425 edges) mixes outcome + method + location into one axis. The new batches split it cleanly. Mapping:

| Old `wva_*` | New target (label / canonical) |
|---|---|
| `wva_direkte_wiederverwendung` | `Wiederverwendungsergebnis: Wiederverwendung_gleiche_Funktion` |
| `wva_adaptives_reuse` | `Wiederverwendungsergebnis: Wiederverwendung_neue_Funktion` |
| `wva_recycling` | `Wiederverwendungsergebnis: Material_Reprocessing` |
| `wva_refurbishment` | `Aufbereitungsverfahren: Reparatur_und_Refurbishment` (axis-shift) |
| `wva_remanufacturing` | `Aufbereitungsverfahren: Remanufacturing_und_Upcycling` (axis-shift) |
| `wva_upcycling` | `Aufbereitungsverfahren: Remanufacturing_und_Upcycling` (axis-shift) |
| `wva_urban_mining` | `Methode: meth_urban_mining` (axis-shift; already in live Methode) |
| `wva_design_for_disassembly` | `Methode: meth_design_for_disassembly` (already in live Methode) |
| `wva_same_site_reuse` | `Wiederverwendungsort: In_situ` / `Im_selben_Gebaeude_versetzt` |
| `wva_bestandserhalt` | `Wiederverwendungsergebnis: Bestandserhalt` |
| `wva_weiterbauen_im_bestand` | `Wiederverwendungsergebnis: Bestandserhalt` |

→ **Revised retirement policy (per user "no legacy"):** the `:WiederverwendungsArt` label retires *entirely*. All 604 inbound edges (425 Bauteilgruppe + 179 Projekt + 0 non-replaceable upstreams) are **deleted** — batches re-supply the meaning on the correct split axes. The ~624 `:DataIssue` `CONCERNS` edges are handled by the DataIssue cleanup policy (delete the issue if its entire CONCERNS set was about retired vocab; trim the edge only if mixed). All 11 `wva_*` nodes are **hard-deleted**. The constraint `wiederverwendungsart_id` is dropped in Phase 6.6.

The mapping table above is now reference-only — it documents what each old `wva_*` *meant* semantically, but no actual migration happens (the batches already classified every project's outcome/method/location into the correct new axis).

---

## C6. New labels to introduce **— SAFE ADDITIONS**

| New label | Why new | Suggested id prefix | Rel from `:Bauteilgruppe` |
|---|---|---|---|
| `:Wiederverwendungsergebnis` | No equivalent axis exists (closest was `:WiederverwendungsArt`, being retired) | `wver_*` | `HAT_ERGEBNIS` |
| `:Wiederverwendungsort` | No equivalent axis exists | `wvo_*` | `HAT_WIEDERVERWENDUNGSORT` |

Both relationship names are new (no collision). Each needs a uniqueness constraint and range index following the existing `<label>_id` convention.

Canonical seed nodes (6 each):

**`:Wiederverwendungsergebnis`**
- `wver_bestandserhalt`, `wver_wv_gleiche_funktion`, `wver_wv_neue_funktion`, `wver_modul_oder_abschnittswv`, `wver_material_reprocessing`, `wver_geplant_oder_gelagert`

**`:Wiederverwendungsort`**
- `wvo_in_situ`, `wvo_im_selben_gebaeude_versetzt`, `wvo_auf_demselben_standort_versetzt`, `wvo_extern_importiert`, `wvo_temporaer_oder_zurueckgegeben`, `wvo_gelagert_oder_unbekannt`

---

## C7. Project ID scheme **— NO CONFLICT (initial reading was wrong)**

Re-verified across all 86 live `:Projekt` nodes in the 2026-06-02 full-network export: every live `:Projekt.id` uses the `p_*` slug, e.g. `p_umar_unit`, `p_bluecity_offices_rotterdam`, `p_k118_kopfbau_halle_118_winterthur`. This matches batch `project_id` exactly.

The earlier "bluecity" sample that suggested a bare-slug convention was a different node type (`:Bauwerk` `bw_bluecity_offices` etc.) — not a Projekt. **No mapping CSV needed.**

→ The one fix needed is in Phase 0.4: relabel 3 nodes that carry `:Projekt` but have `prog_*` ids (`prog_re_use_hoefe`, `prog_reallabor_be_ware`, `prog_stuttgart_210`) → these are mislabeled `:Programm`. Their old-vocab edges then go through the `:Programm → vocab` non-replaceable migration path.

---

## C8. Bauteilgruppe ID conflict — batch slugs ≠ live slugs **— DEDUPE REQUIRED**

The live graph already has component groups for projects covered by batches. Examples from BlueCity / Upcycle Studios alone:

| Live `bg_*` (exists) | Batch `bg_*` (would be created) | Same thing? |
|---|---|---|
| `bg_reuse_beton_wand_bluecity_betonbloecke_trennwaende` | `bg_reuse_beton_innenwand_bluecity_original_concrete_blocks` | **yes** |
| `bg_reuse_stahl_gelaender_bluecity_oelplattform` | `bg_reuse_metall_gelaender_bluecity_oil_platform_balustrades` | **yes** (material drift: metall vs stahl) |
| `bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende` | `bg_reuse_glas_innenwand_bluecity_reused_window_frames` | **yes** (different angle: material vs use) |
| `bg_reuse_glas_fenster_upcycle_studios_copenhagen_doppelverglaste` | `bg_reuse_glas_fenster_upcycle_studios_repurposed_double_glazing` | **yes** |

The coverage report says 79/81 projects already have row-level batch coverage **and** 350 existing `(:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)` edges. Naive MERGE would roughly **double** the Bauteilgruppe table.

→ **Required preflight:** build `bauteilgruppe_id_map.csv` per project via:
- exact slug match
- fuzzy match on `{project, bauteiltyp_token, material_token, descriptor}` with a manual review queue for unclear cases
- the batch `*_candidate` suffix (per open_questions CSV) signals genuinely new groups — flag separately

Without this map, every Bauteilgruppe-anchored row in batches creates a duplicate.

→ Existing graph also has a `bg_kind` property with values `partial_batch`, `batch`, `category` and naming flavors `bg_reuse_*` / `bg_planned_*` / `bg_dismantled_*`. Batches imply only `bg_reuse_*` and `bg_dismantled_*` semantics. Assign `bg_kind` on any new candidate per existing convention.

---

## C9. Relationship-name aliases inside the batches **— NORMALIZE IN MARKDOWN**

Per the coverage report Section 5.B, batches 07/08 still contain pre-v10.1 alias rel-types that must be normalized before staging:

| Raw in batches | Rows | Normalize to |
|---|---:|---|
| `HAS_METHOD` | 55 | `HAT_METHODE` (not `NUTZT_METHODE` — see C2) |
| `HAS_REUSE_RESULT` | 52 | `HAT_ERGEBNIS` |
| `HAS_SOURCE` | 48 | `HAT_RESSOURCENQUELLE` (per C1 recommendation) |
| `HAS_LOCATION` | 47 | `HAT_WIEDERVERWENDUNGSORT` |
| `HAS_PROCESSING` | 42 | `HAT_AUFBEREITUNG` |
| `HAS_DISMANTLING` | 9 | `HAT_RUECKBAUVERFAHREN` |
| `HAS_DECONSTRUCTION` | 1 | `HAT_RUECKBAUVERFAHREN` |

→ Fix in the Markdown source before Cypher staging.

---

## C10. `NUTZT_METHODE` (batch) vs `HAT_METHODE` (live) **— USE LIVE**

Batches use `NUTZT_METHODE`; live graph uses `HAT_METHODE` with a uniqueness constraint already in place (`rel_hat_methode_id`). Adopting `NUTZT_METHODE` would create a parallel rel type.

→ **Use `HAT_METHODE` in all Cypher.** Do not create `NUTZT_METHODE`.

---

## C11. `ANGEWENDET_AUF` (Methode → Bauteilgruppe) **— NEW REL, OK**

Batches introduce `(:Methode)-[:ANGEWENDET_AUF]->(:Bauteilgruppe)` (14 rows). No existing equivalent. Adopt as new rel type with its own uniqueness constraint `rel_angewendet_auf_id`.

---

## C12. Confidence-ladder mismatch **— PROPERTY MAPPING**

| Batch | Live |
|---|---|
| `HIGH` | `belegt` |
| `MEDIUM` | `wahrscheinlich` |
| `LOW` | `unsicher` |

→ Translate during staging. Map every batch `confidence` → schema's `evidence_confidence`. Also populate the required edge properties from the schema guide: `evidence_basis`, `evidence_url` (= batch `evidence_url`), `evidence_quote` (= batch `evidence_summary`, ≤240 chars), `review_run`, `created_at`.

---

## C13. Beschaffungsweg vs Ressourcenquelle (orthogonal axes) **— DO NOT MERGE**

`:Beschaffungsweg` (`bweg_*`) has `bweg_eigenbestand`, `bweg_bauteilboerse`, `bweg_rueckbauprojekt`, `bweg_spende`, `bweg_lager` — superficially overlapping with batch sources, but it's a **different axis**: procurement channel (*how* it was procured), not material origin (*where* it physically came from).

→ Keep separate. Do not route batch `Quelle` rows to `:Beschaffungsweg`. Use `:Ressourcenquelle` per C1.

---

## C14. Two Batch-01 projects had no row-level evidence **— RESOLVED: new Batch-01 markdown delivered**

User uploaded [reuse_taxonomy_v9_connection_expansion_batch_01_markdown_only.md](../../intake/inbox/research/new%20taxonomy%20edit/reuse_taxonomy_v9_connection_expansion_batch_01_markdown_only.md) (2026-06-03 10:08). It contains 139 row-level rows across 10 projects, including K118 Winterthur (17 rows) and MedUni Campus Wien (12 rows).

→ Include Batch 01 in the integration scope. Total batch-row count updates from 2,101 → **2,240**. New per-axis batch counts to add to Phase 7 expectations:

| Relationship | Batch 01 rows | Total batches 01–10 |
|---|---:|---:|
| `HAT_BAUTEILGRUPPE` | 5 | 340 |
| `HAT_ERGEBNIS` | 35 | 423 |
| `HAT_QUELLE` → `HAT_RESSOURCENQUELLE` | 29 | 379 |
| `HAT_WIEDERVERWENDUNGSORT` | 23 | 367 |
| `NUTZT_METHODE` → `HAT_METHODE` | 29 | 298 |
| `HAT_AUFBEREITUNG` | 14 | 283 |
| `HAT_RUECKBAUVERFAHREN` | 4 | 136 |

→ Confidence totals update: HIGH 1618 / MEDIUM 379 / LOW 243.

---

## C15. ID-prefix drift in schema doc vs live data **— REFERENCE FIX**

The [CURRENT_SCHEMA_GUIDE](../2026-06-01_current_schema_guide/CURRENT_SCHEMA_GUIDE.md) lists `Rueckbauverfahren` prefix as `rbv_*` and `Aufbereitungsverfahren` as `auf_*`, but live nodes use **`rv_*`** and **`av_*`**. All Cypher must use the live prefixes; update the schema guide afterward as part of integration cleanup.

---

## Summary: decisions taken (2026-06-03, revised after live-graph analysis)

| Conflict | Choice | Implication |
|---|---|---|
| **C1** | Keep `:Ressourcenquelle` label; **replace** all 16 `rq_*` with 6 new batch-canonical | 482 BG/Projekt edges DELETE, 1 Materialdepot edge MIGRATE, 16 nodes hard-DELETE. |
| **C2** | Hard-delete 13 `meth_*` + replace with 6 new canonical | 591 BG/Projekt edges DELETE, **74 edges from Akteur/Software/Norm MIGRATE**, 13 nodes hard-DELETE. |
| **C4** | Hard-delete 33 `av_*` + replace with 6 new canonical | 433 BG/Projekt edges DELETE, **40 ReuseRule edges MIGRATE**, **47 outbound (TYPISCH_BEI_MATERIAL + BELEGT_IN) MIGRATE+DEDUPE**, 33 nodes hard-DELETE. |
| **C5** | `:WiederverwendungsArt` label **retires entirely** | 604 edges DELETE, 11 nodes hard-DELETE, constraint dropped. |
| **C7** | No project ID conflict — live and batches both use `p_*` | No mapping CSV needed. |
| **C14** | Include Batch 01 | 2,240 total rows; HIGH/MEDIUM/LOW = 1618/379/243. |

**DataIssue cleanup** (~3,824 CONCERNS edges across 5 vocabs):
- DataIssue node whose entire CONCERNS set points at retired vocab → `DETACH DELETE` the DataIssue (~2,500 expected).
- Mixed DataIssue → trim the dangling CONCERNS edges only.

**No `:*_Legacy` labels are created anywhere.** Active vocab axes contain only batch-canonical nodes after Phase 6.

Everything else (C3, C6, C8, C9, C10, C11, C12, C13, C15) has a single clear resolution and does not need a decision.
