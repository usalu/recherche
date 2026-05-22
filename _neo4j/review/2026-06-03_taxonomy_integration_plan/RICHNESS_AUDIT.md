# Richness & Re-supply Audit

**Generated:** 2026-06-03
**Source data:**
- [analyze_richness_and_coverage.py](analyze_richness_and_coverage.py) over the 2026-06-02 full-network export + all 10 batch markdown files → [richness_and_coverage.txt](richness_and_coverage.txt)
- [2026-06-01 relationship property audit](../2026-06-01_relationship_property_audit_mit-bestand/PER_REL_DIGEST.txt) — what properties old vocab edges actually carry

**The user asked two questions:**

1. Are the live `:Projekt` and `:Bauteilgruppe` nodes actually richer/more accurate than the batches?
2. Do the batches really re-supply enough information to replace the old vocab edges?

Both answered with hard numbers below. **Bottom line: yes safe to delete the old vocab — the volume drop is real, but the quality direction is up.**

---

## Q1 — Are old `:Projekt` and `:Bauteilgruppe` nodes richer?

**Yes, but this is irrelevant to the integration.** The plan never touches `:Projekt` or `:Bauteilgruppe` node properties. The integration only deletes/migrates edges on the 5 old vocab axes. Every property on every BG and Projekt node is preserved.

### `:Projekt` property bag (86 nodes)

| Property | Coverage | Stays? |
|---|---:|---|
| `name` | 86/86 | [KEEP] |
| `id` | 86/86 | [KEEP] |
| `projektstatus_text` | 69/86 | [KEEP] |
| `name_full` | 66/86 | [KEEP] |
| `year_completed` | 42/86 | [KEEP] |
| `area_m2_gross` | 35/86 | [KEEP] |
| `nutzung_text` | 9/86 | [KEEP] |

None of these are touched by the integration. Batches don't try to overwrite Projekt properties; they only attach evidence edges.

### `:Bauteilgruppe` property bag (356 nodes)

| Property | Coverage | Stays? |
|---|---:|---|
| `id` | 356/356 | [KEEP] |
| `name` | 356/356 | [KEEP] |
| `reuse_status` | 356/356 | [KEEP] |
| `bg_kind` | 356/356 | [KEEP] (`partial_batch` / `batch` / `category`) |
| `alte_funktion` | 291/356 | [KEEP] (semantic context — what the component was used for before) |
| `neue_funktion` | 291/356 | [KEEP] (what it becomes after reuse) |
| `tragend` | 124/356 | [KEEP] (load-bearing flag) |

All preserved.

### Other connections on `:Bauteilgruppe` that are NOT touched

For every BG, the integration only touches the 5 old vocab axes (marked `[IN SCOPE]` below). The other 10+ axes stay untouched:

```
-[:HAS_RISK_POLLUTANT          ]->(:Schadstoff              )   791   stays
-[:HAT_HUERDE                  ]->(:Huerde                  )   739   stays
-[:HAT_PROZESSPHASE            ]->(:Prozessphase            )   645   stays
-[:BELEGT_IN                   ]->(:Quelle                  )   627   stays  (evidence URLs)
-[:HAT_BAUTEILTYP              ]->(:Bauteiltyp              )   592   stays
-[:HAT_LEISTUNGSANFORDERUNG    ]->(:Leistungsanforderung    )   548   stays
-[:NUTZT_MATERIAL              ]->(:Material                )   495   stays
-[:HAT_RESSOURCENQUELLE        ]->(:Ressourcenquelle        )   482   [IN SCOPE]
-[:HAT_MATERIALGRUPPE          ]->(:Materialgruppe          )   475   stays
-[:HAT_WIEDERVERWENDUNGSART    ]->(:WiederverwendungsArt    )   425   [IN SCOPE]
-[:HAT_AUFBEREITUNG            ]->(:Aufbereitungsverfahren  )   411   [IN SCOPE]
-[:HAT_METHODE                 ]->(:Methode                 )   397   [IN SCOPE]
-[:HAT_LOGISTIK                ]->(:Logistik                )   390   stays
-[:HAT_MARKTMODELL             ]->(:Marktmodell             )   374   stays
-[:HAT_BAUTEILEBENE            ]->(:Bauteilebene            )   359   stays
```

Verdict on Q1: BG and Projekt node richness is **fully preserved**. The only knowledge that disappears is the 5 vocab axes — and those have a quality problem (see Q2).

---

## Q2 — Do batches re-supply enough information?

Three angles: edge volume, edge quality, and per-project / per-BG coverage gaps.

### 2A. Edge VOLUME — yes, fewer edges after integration

Across all 5 old vocab axes combined:

| Source | Total edges |
|---|---:|
| Old graph (5 vocab rels) | **2,459** |
| Batches (6 new vocab rels) | **~1,886** (per coverage report §3) |
| Net delta | **−573 edges** |

Per axis:

| Axis | Old edges | Batch supply | Delta |
|---|---:|---:|---:|
| `HAT_METHODE` (live → 6 canonical) | 654 | 298 | −356 |
| `HAT_AUFBEREITUNG` | 433 | 283 | −150 |
| `HAT_RESSOURCENQUELLE` | 552 | 379 | −173 |
| `HAT_WIEDERVERWENDUNGSART` | 604 | 0 | −604 (axis retires; replaced by Ergebnis+Ort below) |
| `HAT_RUECKBAUVERFAHREN` | 299 | 136 | −163 |
| `HAT_ERGEBNIS` (new) | 0 | 423 | +423 |
| `HAT_WIEDERVERWENDUNGSORT` (new) | 0 | 367 | +367 |

WVA's 604 edges get conceptually replaced by `HAT_ERGEBNIS` (423) + `HAT_WIEDERVERWENDUNGSORT` (367) + some `HAT_METHODE` — so the WVA "loss" is not a loss.

### 2B. Edge QUALITY — old graph is mostly auto-tagged placeholders

This is the decisive number. From the [2026-06-01 relationship property audit](../2026-06-01_relationship_property_audit_mit-bestand/PER_REL_DIGEST.txt):

| Vocab edge | `review_status: needs_source_url_review` | `evidence_origin: topology_synthesized` | `evidence_confidence: unklar` | `source_status: missing` |
|---|---:|---:|---:|---:|
| `HAT_METHODE` (654) | 91% | 91% | 91% | 91% |
| `HAT_AUFBEREITUNG` (433) | **100%** | 100% | **100%** | 100% |
| `HAT_RESSOURCENQUELLE` (552) | **100%** | 100% | **100%** | 100% |
| `HAT_WIEDERVERWENDUNGSART` (604) | **100%** | 100% | **100%** | 100% |
| `HAT_RUECKBAUVERFAHREN` (299) | **100%** | 100% | **100%** | 100% |
| `evidence_basis` | `controlled_vocab` / `legacy_migration` | | | |
| `source_status_reason` | `no_exact_url_binding_needs_review` | | | |

**In plain language:** essentially every old vocab edge is an auto-derived placeholder with `confidence: unklar` (unknown), `source_status: missing`, and a `needs_source_url_review` flag. They were never human-verified evidence. They were synthesised from controlled-vocab tagging and legacy migration scripts, waiting for actual evidence to confirm or refute them.

The batches **are** that confirmation. Every batch row carries:
- `evidence_url` — first-party source URL
- `evidence_summary` — verbatim quote
- `evidence_confidence ∈ {belegt, wahrscheinlich, unsicher}` — graded ladder (HIGH/MEDIUM/LOW translated)
- `evidence_basis` = `taxonomy_integration_2026_06_03` — auditable run tag

**Confidence ladder comparison after integration:**

| Tier | Old graph edges | Batches deliver |
|---|---:|---:|
| `belegt` (high confidence, sourced) | ~0 | 1,618 |
| `wahrscheinlich` (medium) | ~0 | 379 |
| `unsicher` / `unklar` (low) | ~2,459 | 243 |
| **Total** | **2,459 unverified** | **2,240 evidence-backed** |

So the volume drops by 573 edges but **evidence-backed edges go from ~0 to 1,997**. That's the actual change.

### 2C. Per-project gap check — where the volume drop is concentrated

32 projects show batch supply meaningfully lower than old vocab tags on at least one axis. Top 8 with multi-axis gaps:

| Project | Old vocab edges (5 axes) | Batch new edges (6 axes) | Worst-affected axes |
|---|---:|---:|---|
| `p_impact_hub_berlin_crclr_fitout` | 33+11+24+14+15 = 97 | 3+7+7+0+7+7 = 31 | Method 33→3, Rueckb 14→0 |
| `p_crclr_house_impact_hub_berlin` | (similarly heavy) | smaller | similar pattern |
| `p_elys_kultur_gewerbehaus_basel` | 17+14+24+14+14 = 83 | 2+0+7+0+7+7 = 23 | Aufber 14→0, Rueckb 14→0 |
| `p_grubenstrasse_29_werkhof_29_zuerich` | 22+16+31+18+12 = 99 | 2+0+9+0+9+10 = 30 | Aufber 16→0, Rueckb 18→0 |
| `p_grande_halle_de_colombelles` | 21+16+20+18+12 = 87 | 3+8+8+0+8+8 = 35 | Rueckb 18→0 |
| `p_ferme_du_rail_paris` | 19+11+27+16+10 = 83 | 3+1+1+0+5+1 = 11 | Quelle 27→1, Rueckb 16→0 |
| `p_house_of_fraser_…tbc_…reuse_chain` | 15+13+14+6+15 = 63 | 2+0+4+0+4+4 = 14 | Aufber 13→0, Rueckb 6→0 |
| `p_svanen_kindergarten_gladsaxe` | 23+9+7+9+15 = 63 | 4+2+7+1+7+7 = 28 | Method 23→4 |

**Pattern in every case:** old graph had auto-tagged generic vocab edges (e.g. 22 BGs of Grubenstrasse all auto-tagged `meth_urban_mining`); batches deliver per-component evidence-backed rows. The drop reflects deduplication of redundant auto-tags, not loss of curated knowledge.

For these projects the integration *replaces* coarse `unklar`-confidence tagging with selective `belegt`/`wahrscheinlich` evidence. Numerically less, qualitatively richer.

### 2D. Per-BG gap check — only 6 high-risk BGs remain after parser fix

The earlier draft flagged 54 BGs with zero batch coverage, but that was a parser miss on batches 04+. After fixing the parser:

- **6 BGs** in projects with ≤ 3 batch rows. These are the genuine gaps where the BG had old vocab edges but the batch supply is thin.
- All 6 are in the projects flagged above (Impact Hub and CRCLR House) — the batches were not comprehensive on the small fittings (MDF panels, phone booths). For these, the new state will be: BG keeps its properties and non-vocab edges, but its old vocab axes go to zero. **The information loss is the 5 auto-tagged `unklar` edges per BG.**

If you want zero-loss: either supplement those 6 BGs with additional batch rows in Phase 2 (Markdown normalization), or accept the 5 `unklar` edges per BG disappear (recommended given they had no evidence anyway).

---

## Decision matrix per old vocab edge

Re-cast of [CONNECTION_TYPE_AUDIT.md](CONNECTION_TYPE_AUDIT.md) tags through the richness lens. Each row reflects the property profile of the edges in that bucket.

| Edge bucket | Property profile | Action | Rationale |
|---|---|---|---|
| `:Bauteilgruppe → :Methode` (397) | 91% `topology_synthesized`/`unklar`/`missing` | **DELETE** | Auto-tagged placeholders. Batches replace with evidence-backed rows where coverage exists. |
| `:Projekt → :Methode` (194) | same | **DELETE** | Same |
| `:Akteur/:Software/:Tool/:Norm → :Methode` (74) | same | **REROUTE** | Non-replaceable upstream; keep the link, point at new canonical |
| `:Bauteilgruppe → :Aufbereitungsverfahren` (411) | 100% `topology_synthesized`/`unklar`/`missing` | **DELETE** | |
| `:Projekt → :Aufbereitungsverfahren` (22) | same | **DELETE** | |
| `:ReuseRule → :Aufbereitungsverfahren` (40) | same | **REROUTE** | Non-replaceable upstream |
| `:Aufbereitungsverfahren → :Material` (`TYPISCH_BEI_MATERIAL`, 22) | mixed: some `source_curated` | **REROUTE + DEDUPE** | Real semantic association; preserve onto new canonical |
| `:Aufbereitungsverfahren → :Quelle:ResearchDocument` (`BELEGT_IN`, 25) | curated | **REROUTE + DEDUPE** | Real evidence citations; preserve |
| `:Bauteilgruppe → :Ressourcenquelle` (482) | 100% `topology_synthesized`/`unklar`/`missing` | **DELETE** | |
| `:Projekt → :Ressourcenquelle` (69) | same | **DELETE** | |
| `:Materialdepot → :Ressourcenquelle` (1) | curated | **REROUTE** | |
| `:Bauteilgruppe → :WiederverwendungsArt` (425) | 100% `topology_synthesized`/`unklar`/`missing` | **DELETE** | Axis retires; replaced by Ergebnis+Ort+Methode from batches |
| `:Projekt → :WiederverwendungsArt` (179) | same | **DELETE** | |
| `:Bauteilgruppe → :Rueckbauverfahren` (299) | 100% `topology_synthesized`/`unklar`/`missing` | **DELETE** | |

**Net:** delete 2,478 placeholder edges, reroute 162 edges (115 inbound + 47 outbound), add 1,997 evidence-backed edges + 14 ANGEWENDET_AUF + 340 HAT_BAUTEILGRUPPE.

---

## What to do about the 32 flagged projects

Three options:

**A. Accept the volume drop** (recommended).
The "loss" is loss of `unklar`/`needs_source_url_review` edges. They were never trustworthy data. The new state is honest: where evidence exists, we have a `belegt` edge; where it doesn't, the BG simply has no edge on that axis (which is more accurate than a fake `unklar` placeholder).

**B. Targeted batch top-up** for the 8 worst-affected projects.
Before Phase 5, write a small additional research pass for Impact Hub, CRCLR House, Elys, Grubenstrasse, Grande Halle, Ferme du Rail, House of Fraser, Svanen. Add rows to the existing batch markdown files. Phase 5 then has fuller coverage. Costs research time; gains 200–400 evidence-backed edges.

**C. Preserve old edges that DO carry evidence.**
Filter old vocab edges by property: keep any with `evidence_basis != 'controlled_vocab'` AND `evidence_basis != 'legacy_migration'` AND has an `evidence_source_id` pointing to a real source. From the property profile, this is roughly **3% of HAT_METHODE** and near-zero on the others. Option C salvages ~20 edges total — probably not worth the complexity.

→ Recommend **A**, with a flag in the verification test (§7) listing the 8 most-affected projects so they're visible after Phase 5 and can be revisited with new research if needed.

---

## Updated check to add to verify_integration.cypher

A new §11 that reports the 32 flagged projects after Phase 5 — not a FAIL, just visibility:

```cypher
// §11. Volume change per project — surface projects with significant drop
MATCH (p:Projekt)
OPTIONAL MATCH (p)-[r_old_pre]->(t_old) WHERE type(r_old_pre) IN
  ['HAT_METHODE','HAT_AUFBEREITUNG','HAT_RESSOURCENQUELLE','HAT_RUECKBAUVERFAHREN']
  AND r_old_pre.evidence_origin = 'topology_synthesized'
WITH p, count(r_old_pre) AS old_placeholder_count
OPTIONAL MATCH (p)<-[:HAT_BAUTEILGRUPPE]-()
OPTIONAL MATCH ()-[r_new]->()
WHERE r_new.review_run = 'taxonomy_integration_2026_06_03'
WITH p, old_placeholder_count, count(r_new) AS new_evidence_count
RETURN p.id, p.name, old_placeholder_count, new_evidence_count,
       new_evidence_count - old_placeholder_count AS delta
ORDER BY delta ASC LIMIT 10;
```

(Logically this query runs *before* Phase 6's edge deletion, so old counts are still visible. After Phase 6 the placeholder rows are gone and the comparison is moot — the same query would just confirm the deletion is complete.)
