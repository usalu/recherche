# Variant B — Typed law-node taxonomy (draft for re-import)

**Status:** applied (Option 1, 11 labels) — committed 2026-06-05 via `phaseB_reimport_typed_laws.py --commit`.  
**Source of truth for the 91 standards:** `build_vocabulary_graph.py` / `vocab_nodes.jsonl`.  
**Current live graph:** Variant A (laws as `rechtsgrundlagen[]` on `Nachweisforderung`).  
**Import script:** `phaseB_reimport_typed_laws.py` (dry-run → explicit go-ahead → `--commit`).

## Pre-flight review (2026-06-05)

All safety checks passed against live `mit-bestand`:

| Check | Result |
|---|---|
| Live baseline | 2 182 nodes / 14 670 rels / 11 RF / 27 NF |
| Overlay NF targets after fold | 27/27 exist in graph |
| Overlay Land targets | 9/9 exist (0 missing) |
| `rechtsgrundlagen[]` ↔ GESTUETZT parity | 167/167 pairs match (0 gaps) |
| Duplicate GESTUETZT after NF fold | 2 raw rows → deduped to 167 unique edges |
| Duplicate GILT_IN_LAND | 0 (281 unique) |
| ERFORDERT_NACHWEIS overlay vs live | 88/88 unchanged |
| TRIGGERS_REGULIERUNGSFRAGE | not touched by Phase B |
| `:Regelwerk` / existing GESTUETZT / GILT_IN_LAND | all 0 (safe to import) |

**Corrected edge counts:** 167 `GESTUETZT_AUF_REGELWERK` (not 169 — two pollutant-check NF
ids fold into `nf_schadstoffpruefung` and dedupe), plus 281 `GILT_IN_LAND`.

---

## 1. Recommendation

Use **11 typed law labels**, one per `Regulierungsfrage`. This is the cleanest alignment with the
existing question layer and keeps every label ≤ 27 nodes (well under the ≤15 *reuse* target per
vocabulary — note these are reference standards, not spray nodes).

An optional **7-label consolidation** is listed in §3 if you prefer fewer browse buckets.

**Multi-label rule (required):** 48 / 91 standards span more than one domain. Each gets **all
applicable `:…recht` labels** derived from its `rf[]` links in `build_vocabulary_graph.py`. Primary
navigation uses labels; `rechtsbereiche[]` property mirrors them for array queries.

---

## 2. Eleven-label taxonomy (recommended)

| Neo4j label | Maps from Regulierungsfrage | Standards (count) | Example nodes |
|---|---|---:|---|
| `:ReuseDokumentationsrecht` | `rf_reusedokumentationfrage` | 18 | `rw_din_spec_91484`, `rw_madaster_grp` |
| `:RueckbauUndAbbruchrecht` | `rf_rueckbau_und_bauteilernte_frage` | 16 | `rw_vdi_6210`, `rw_krwg`, `rw_vob_c_din_18459` |
| `:Bauproduktrecht` | `rf_bauproduktstatus_frage` | 23 | `rw_eu_cpr_2024_3110`, `rw_en_1090`, `rw_dibt_zie_abz` |
| `:Tragwerksrecht` | `rf_tragwerkssicherheit_frage` | 26 | `rw_eurocodes_en_1990_1999`, `rw_sci_p427`, `rw_nta_8713` |
| `:Brandschutzrecht` | `rf_brandschutz_frage` | 8 | `rw_din_en_13501`, `rw_vkf_bsv`, `rw_uk_adb` |
| `:Bauphysikrecht` | `rf_bauphysik_frage` | 10 | `rw_geg`, `rw_sia_380_1`, `rw_fr_re2020` |
| `:Schadstoffrecht` | `rf_schadstoff_frage` | 17 | `rw_trgs_519`, `rw_trgs_521`, `rw_gefstoffv` |
| `:HygieneElektroFunktionsrecht` | `rf_hygiene_elektro_funktion_frage` | 4 | `rw_dguv_v3_vde`, `rw_vdi_6023_6022` |
| `:Genehmigungsrecht` | `rf_genehmigungs_frage` | 7 | `rw_mbo_lbo`, `rw_denkmalschutz` |
| `:Haftungsrecht` | `rf_haftung_gewaehrleistung_frage` | 3 | `rw_prodhaftg_bgb`, `rw_fr_rep_pmcb` |
| `:UmweltUndOekobilanzrecht` | `rf_umweltvertraeglichkeit_oekobilanz_frage` | 13 | `rw_en_15804_15978`, `rw_eu_taxonomy`, `rw_qng_dgnb` |

**Total unique law nodes:** 91 (same ids as today’s `rw_*`; labels are additive).

---

## 3. Optional seven-label consolidation

Merge closely coupled domains only where browse UX benefits:

| Consolidated label | Absorbs | Unique standards |
|---|---|---:|
| `:Bauproduktrecht` | (unchanged) | 23 |
| `:Tragwerksrecht` | (unchanged) | 26 |
| `:Schadstoffrecht` | (unchanged) | 17 |
| `:BauphysikUndBrandschutzrecht` | Bauphysik + Brandschutz | 15 |
| `:RueckbauUndReuseDokumentationsrecht` | Rueckbau + Reuse-Doku | 25 |
| `:GenehmigungsHaftungsUndFunktionsrecht` | Genehmigung + Haftung + Hygiene/Elektro | 13 |
| `:UmweltUndOekobilanzrecht` | (unchanged) | 13 |

Use this only if 11 browser tabs feels too fine-grained. **Re-import mapping should still store the
fine-grained domain in `rechtsbereiche[]`** even when using consolidated labels.

---

## 4. Node schema (each law node)

```json
{
  "id": "rw_sci_p427",
  "name": "SCI P427",
  "source_url": "https://steel-sci.com/assets/downloads/steel-reuse-protocol-v06.pdf",
  "source_quote": "Reclaimed steelwork can be CE marked per BS EN 1090; …",
  "evidence_status": "rule_documented",
  "confidence": 0.9,
  "rechtsbereiche": ["Tragwerksrecht", "Bauproduktrecht"],
  "source_scope": "regulation_graph_vocab_2026_06_04",
  "review_run": "variant_b_reimport"
}
```

**Labels (11-label mode):** `:Tragwerksrecht:Bauproduktrecht` (multi-label on 48 nodes).

---

## 5. Edge schema (restored from overlay, not from Variant A properties)

| Edge | From → To | Count (overlay) | Notes |
|---|---|---:|---|
| `GESTUETZT_AUF_REGELWERK` | `Nachweisforderung` → law node | 167 | replaces `rechtsgrundlagen[]` entries (169 raw, 2 deduped after NF fold) |
| `GILT_IN_LAND` | law node → `Land` | 281 | jurisdiction; was folded into `jurisdiktion[]` in A |
| `ERFORDERT_NACHWEIS` | `Regulierungsfrage` → `Nachweisforderung` | 94 | unchanged |
| `TRIGGERS_REGULIERUNGSFRAGE` | case anchors → `Regulierungsfrage` | (existing) | unchanged |
| `BETRIFFT_MATERIAL` | law node → `Material` | 39 | optional component routing |
| `BETRIFFT_BAUTEILTYP` | law node → `Bauteiltyp` | 18 | optional component routing |

**Dropped Nachweisforderung remap (same as Phase 2):** 6 sparse NF (`nf_kmf_check`, …) fold into
`nf_schadstoffpruefung`; their `GESTUETZT_AUF_REGELWERK` edges target the surviving NF.

---

## 6. Multi-domain standards (48) — label assignment rule

```
FOR each rw IN REGELWERK:
  labels(rw) = { RF_TO_LABEL[rf] for rf in rw.rf[] }
```

Examples:

| id | name | labels |
|---|---|---|
| `rw_cen_ts_1090_201` | CEN/TS 1090-201:2024 | `:Tragwerksrecht` `:Bauproduktrecht` |
| `rw_eu_cpr_2024_3110` | EU CPR 2024/3110 | `:Bauproduktrecht` `:ReuseDokumentationsrecht` |
| `rw_din_4102` | DIN 4102/4108/4109 | `:Brandschutzrecht` `:Bauphysikrecht` |
| `rw_dk_br18` | Denmark BR18 | `:Bauproduktrecht` `:Brandschutzrecht` `:UmweltUndOekobilanzrecht` |
| `rw_lfu_schadstoff_arbeitshilfe` | LfU Arbeitshilfe | `:Schadstoffrecht` `:RueckbauUndAbbruchrecht` |

---

## 7. Full standard → label mapping (11-label mode)

### ReuseDokumentationsrecht (18)
- `rw_be_tracimat_regional`, `rw_denkmalschutz`, `rw_din_spec_91484`, `rw_din_spec_91525`
- `rw_eu_cdw_protocol`, `rw_eu_cpr_2024_3110`, `rw_eu_taxonomy`, `rw_eu_wfd_2008_98`
- `rw_fcrbe_reuse_toolkit`, `rw_fr_pemd`, `rw_iso_20887`, `rw_istructe_reuse`, `rw_krwg`
- `rw_madaster_grp`, `rw_naturstein_reuse`, `rw_nl_bbl`, `rw_qng_dgnb`, `rw_zirkulaere_vergabe`

### RueckbauUndAbbruchrecht (16)
- `rw_be_tracimat_regional`, `rw_din_spec_91484`, `rw_din_spec_91525`, `rw_eu_cdw_protocol`
- `rw_eu_wfd_2008_98`, `rw_fcrbe_reuse_toolkit`, `rw_fr_pemd`, `rw_fr_rep_pmcb`, `rw_gewabfv`
- `rw_iso_20887`, `rw_krwg`, `rw_lfu_schadstoff_arbeitshilfe`, `rw_no_tek17`, `rw_oenorm_b3151`
- `rw_vdi_6210`, `rw_vob_c_din_18459`

### Bauproduktrecht (23)
- `rw_cen_ts_1090_201`, `rw_dibt_zie_abz`, `rw_din_18945_lehm`, `rw_dk_br18`, `rw_en_1090`
- `rw_en_1090_2_bolts_reuse`, `rw_en_1168`, `rw_en_13162_mineralwolle`, `rw_en_13830`, `rw_en_14351`
- `rw_en_771_reclaimed`, `rw_en_naturstein`, `rw_espr_dpp`, `rw_eu_cpr_2024_3110`, `rw_eu_cpr_305_2011`
- `rw_glas_reuse_igu`, `rw_mbo_lbo`, `rw_mvv_tb`, `rw_nl_bbl`, `rw_no_tek17`, `rw_nta_8713`
- `rw_sci_p427`, `rw_ukca_ce`

### Tragwerksrecht (26)
- `rw_cen_ts_1090_201`, `rw_cen_ts_17440`, `rw_dafstb_rc_beton`, `rw_din_18008`, `rw_din_18945_lehm`
- `rw_din_4074_en_14081`, `rw_en_1090`, `rw_en_1090_2_bolts_reuse`, `rw_en_1168`, `rw_en_13791_12504`
- `rw_en_1992_4`, `rw_en_408`, `rw_en_771_reclaimed`, `rw_en_iso_6892`, `rw_en_naturstein`
- `rw_eurocodes_en_1990_1999`, `rw_fib_precast_reuse`, `rw_istructe_reuse`, `rw_mvv_tb`
- `rw_naturstein_reuse`, `rw_nen_8700`, `rw_nta_8713`, `rw_sci_p427`, `rw_sia_269`, `rw_sia_269_2`
- `rw_uk_adb`

### Brandschutzrecht (8)
- `rw_din_4102`, `rw_din_en_13501`, `rw_dk_br18`, `rw_en_13830`, `rw_mvv_tb`, `rw_oib_richtlinien`
- `rw_uk_adb`, `rw_vkf_bsv`

### Bauphysikrecht (10)
- `rw_ch_muken`, `rw_din_4102`, `rw_en_13162_mineralwolle`, `rw_en_13830`, `rw_en_14351`
- `rw_fr_re2020`, `rw_geg`, `rw_glas_reuse_igu`, `rw_oib_richtlinien`, `rw_sia_380_1`

### Schadstoffrecht (17)
- `rw_agbb_voc`, `rw_din_68800_altholzv`, `rw_ebv`, `rw_eu_cdw_protocol`, `rw_gefstoffv`
- `rw_lfu_schadstoff_arbeitshilfe`, `rw_oenorm_b3151`, `rw_pcb_richtlinie`, `rw_pop_2019_1021`
- `rw_reach_annex_xvii`, `rw_strlschg_radon`, `rw_trgs_519`, `rw_trgs_521`, `rw_trgs_524`
- `rw_uba_schimmelleitfaden`, `rw_vdi_3492`, `rw_vdi_6202`

### HygieneElektroFunktionsrecht (4)
- `rw_dguv_v3_vde`, `rw_din_18040`, `rw_din_18065`, `rw_vdi_6023_6022`

### Genehmigungsrecht (7)
- `rw_denkmalschutz`, `rw_dibt_zie_abz`, `rw_din_18065`, `rw_mbo_lbo`, `rw_nl_bbl`
- `rw_oib_richtlinien`, `rw_zirkulaere_vergabe`

### Haftungsrecht (3)
- `rw_fr_rep_pmcb`, `rw_prodhaftg_bgb`, `rw_vob_c_din_18459`

### UmweltUndOekobilanzrecht (13)
- `rw_dafstb_rc_beton`, `rw_dk_br18`, `rw_ebv`, `rw_en_15804_15978`, `rw_espr_dpp`, `rw_eu_levels`
- `rw_eu_taxonomy`, `rw_fr_re2020`, `rw_madaster_grp`, `rw_nl_mpg`, `rw_qng_dgnb`, `rw_sia_2032`
- `rw_uk_pas2080`

---

## 8. Concrete graph slice (Holbein steel — Variant B)

```
(bg_stahl_mehrere_holbein_structural:Bauteilgruppe)
  -[:TRIGGERS_REGULIERUNGSFRAGE]-> (rf_tragwerkssicherheit_frage:Regulierungsfrage)
  -[:TRIGGERS_REGULIERUNGSFRAGE]-> (rf_schadstoff_frage:Regulierungsfrage)

(rf_tragwerkssicherheit_frage)-[:ERFORDERT_NACHWEIS]->(nf_standsicherheitsnachweis:Nachweisforderung)
  -[:GESTUETZT_AUF_REGELWERK]-> (rw_eurocodes_en_1990_1999:Tragwerksrecht)
  -[:GESTUETZT_AUF_REGELWERK]-> (rw_sci_p427:Tragwerksrecht:Bauproduktrecht)
  -[:GESTUETZT_AUF_REGELWERK]-> (rw_cen_ts_1090_201:Tragwerksrecht:Bauproduktrecht)

(rw_sci_p427)-[:GILT_IN_LAND]-> (land_vereinigtes_koenigreich:Land)
(rw_eurocodes_en_1990_1999)-[:GILT_IN_LAND]-> (land_deutschland:Land)
```

Query:

```cypher
MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_holbein_structural'})
      -[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage {id:'rf_tragwerkssicherheit_frage'})
      -[:ERFORDERT_NACHWEIS]->(nf)-[:GESTUETZT_AUF_REGELWERK]->(rw)
RETURN labels(rw) AS rechtstyp, rw.name, rw.source_url
```

---

## 9. Migration from Variant A (high level)

1. Snapshot (`phaseB_before.json`).
2. Import 91 law nodes from `vocab_nodes.jsonl` with typed labels + evidence props.
3. Create 169 `GESTUETZT_AUF_REGELWERK` + 281 `GILT_IN_LAND` from `vocab_edges.csv`.
4. **Keep** `rechtsgrundlagen[]` on NF as denormalized cache **or** remove after verify (recommend:
   keep read-only mirror `legacy_rechtsgrundlagen_from_variant_a[]` one release, then drop).
5. Acceptance: every entry in current `nf.rechtsgrundlagen[]` has a matching `GESTUETZT_AUF` edge;
   no duplicate `(nf,rw)` pairs; 91 nodes / 0 `:Regelwerk` label.

**Graph size after B:** ~2182 + 91 = **~2273 nodes**, +450 overlay edges (gestützt + gilt_in_land).

---

## 10. Locked decisions (Option 1)

| Question | Decision |
|---|---|
| Label granularity | **11-label** (1:1 with Regulierungsfrage) |
| Multi-label | **Yes** — 48 cross-domain standards |
| Denormalized arrays on NF | Archive to `legacy_*_from_variant_a[]`, remove active arrays after import |
| Component edges | **Deferred** — `BETRIFFT_MATERIAL` / `BETRIFFT_BAUTEILTYP` not in Phase B |
| Unchanged layers | `TRIGGERS_REGULIERUNGSFRAGE` (1 100), `ERFORDERT_NACHWEIS` (1 483) |
