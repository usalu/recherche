# Remediation R03 — Deferred Node Duplicates (Wave 2)

**Agent:** R03 · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Input:** REMEDIATION_PLAN §4 (36 deferred node dupes after wave-1 8 merges)
**Ledger:** [`ledger/remediation_r03.csv`](../ledger/remediation_r03.csv) — 36 pair reviews
**Patch:** [`patches/remediation_r03_merge_nodes.patch.jsonl`](../patches/remediation_r03_merge_nodes.patch.jsonl) — 11 `merge_node` (airtight only)

## Executive summary

Of the **36 deferred** node-duplicate pairs from §4, **11** pass the strict identity gate (same org URL / legal entity / institute ID / EN–FR alias / org+person composite collapse). **11** are rejected or escalated (generic BIM concepts, Paris public-body hierarchy, Joel+Hervé Biele brothers, sub-pilot programme labels). **8** were already resolved in wave-1 (`merge_duplicate_nodes_high_confidence`). **4** are cross-referenced to Agent R04 (RAU identity split; `harvestmap` → `re_store_harvestmap_vienna`).

**Apply discipline:** ✅ **Live apply 2026-06-06** — 11/11 `merge_node`, 2295→2284 nodes, 15340→15312 rels
(`apply_reports/remediation_r03_merge_nodes.patch.apply_report.md`). R04 `harvestmap` merge remains in the R04 patch (separate gated apply).

## Method

1. `read-cypher` on all candidate node ids — properties, degree, incident rel types.
2. Pairwise comparison against ledger notes (Agent 08 AKT-node-*, Agent 10 A10-N-*).
3. `WebFetch` / web search for `primary_source_url`, `source_urls`, and official domains.
4. **Never merge on name similarity alone** — require org URL, legal entity, or institute GND/homepage proof.

## Verdict summary

| Outcome | Count | Examples |
|---|---:|---|
| **PATCH_READY** (`merge_node`) | 11 | ZRS triple (×2 merges), IEMB/Tampere/Archipel composites, Albert & Co, Pirmin Jung AG, EPFL SXL |
| **ESCALATE_HUMAN** | 9 | Paris STP / Pavillon, BIM triple, `prog_recreate_local`, `rau`↔`rau_architects` |
| **REJECT merge** (keep separate) | 4 | `herve_joel_biele`, BIM pairs, Oogstkaart vs HarvestMAP |
| **REFERENCE_R04** | 2 | `harvestmap`, `rau`↔`thomas_rau` |
| **RESOLVED wave-1** | 8 | Superuse, CITYFOERSTER, Artelia, Greisch, Graber Pulver, Fabrix, Lendager, Qflow |
| **KEEP hierarchy** | 2 | `iemb_tu_berlin`≠`tu_berlin`, `structural_xploration_lab_epfl`≠`epfl` |

## Cluster findings

### ZRS triple (PROVEN — patch)

| Node | deg | Sources | Verdict |
|---|---:|---|---|
| `ZRS_Architekten_Ingenieure` | 7 | none | merge → `zrs_ingenieure` |
| `zrs` | 7 | none | merge → `zrs_ingenieure` |
| `zrs_ingenieure` | 7 | `source_titles` (CRCLR projects) | **canonical** |

**Proof:** [zrs.berlin/en/office](https://www.zrs.berlin/en/office/) — *"ZRS Architekten Ingenieure … two firms ZRS Architekten GvA mbH and ZRS Ingenieure GmbH"*. Contact page names Christof Ziegert and Uwe Seiler (matching graph `VERBUNDEN_MIT_AKTEUR` on stub `zrs`).

### IEMB / TU Berlin composites (PROVEN — patch)

| From | To | Proof |
|---|---|---|
| `ak_tu_berlin_iemb` | `iemb_tu_berlin` | DNB GND [2129400-8](https://portal.dnb.de/opacPresentation?cqlMode=true&query=idn%3D007761945): *IEMB an der TU Berlin* |
| `claus_asam_iemb` | `claus_asam` | [iemb.de publication](https://d-nb.info/1003144454/34): *Dipl.-Ing. Claus Asam, asam@iemb.de* |

Person nodes `claus_asam`, institute `iemb_tu_berlin`, and parent `tu_berlin` **remain separate** after composite collapse.

### Tampere / ReCreate composites (PROVEN — patch)

| From | To | Proof |
|---|---|---|
| `tampere_university_recreate` | `tampere_university` | [recreate-project.eu](https://recreate-project.eu): Tampere University researchers throughout |
| `tampere_university_satu_huuhka` | `tampere_university` | Same; `satu_huuhka` person node retained (sourced) |

### Archipel Zéro composite (PROVEN — patch)

`frederic_denise_archipel_zero` → `archipel_zero`. Person `frederic_denise` already carries `archipelzero.com` project URLs; composite stub absorbed into firm node.

### Albert & Compagnie (PROVEN — patch)

`albert_et_compagnie` → `albert_and_co`. [albert-et-compagnie.com](https://www.albert-et-compagnie.com) displays **ALBERT & Co** — EN/FR trade-name alias, not two firms.

### Pirmin Jung (PROVEN — patch)

`pirmin_jung_schweiz` → `pirmin_jung_schweiz_ag`. UID **CHE-108.393.904**, [pirminjung.ch](https://www.pirminjung.ch/ueber-uns/organisation).

### EPFL SXL (PROVEN — patch)

`ak_epfl_structural_xploration_lab` → `structural_xploration_lab_epfl`. [epfl.ch/labs/sxl](https://www.epfl.ch/labs/sxl/team/) — Structural Xploration Lab; `corentin_fivet` VERBUNDEN edge matches.

### BTU Cottbus / Mettke (PROVEN — patch)

`btu_cottbus_angelika_mettke` → `btu_cottbus`. `angelika_mettke` person node stays (ReCreate-sourced).

---

### Hervé / Joel Biele (REJECT merge)

**Ledger:** AKT-node-218 proposed `herve_joel_biele` → `herve_biele_conclus`.

**Proof:** [Spiegel International](https://www.spiegel.de/international/recycling-architectural-disasters-a-communist-block-house-renaissance-a-367335.html) — *"Joel Biele's brother Herve"* at Conclus. Graph composite intentionally names **both brothers**; merging into `herve_biele_conclus` (Hervé-only) drops Joel.

**Action:** KEEP all three nodes; human may split composite or add `VERBUNDEN_MIT_AKTEUR` to Conclus.

### Ville de Paris cluster (ESCALATE)

| Node | Role on `p_circular_pavilion_paris` |
|---|---|
| `services_techniques_ville_de_paris` | technical services / execution |
| `ville_de_paris` | client / public authority |
| `ville_de_paris_pavillon_arsenal` | architecture centre |

No fetched URL proves these are interchangeable legal entities. **Do not merge** STP into `ville_de_paris` (Agent 08 already flagged lower confidence).

### Generic BIM / Bauteilkatalog (ESCALATE — not entities)

`software_bim`, `tool_bauteilkatalog`, `tool_bim_bauteilkatalog` — unsourced generic concepts with spurious bidirectional `NUTZT_SOFTWARE` self-wiring (Agent 10). **Not merge candidates**; relabel to vocabulary or delete self-edges in a separate pass.

### HarvestMAP / Oogstkaart / RAU (see R04)

| Pair | R03 verdict | Owner |
|---|---|---|
| `harvestmap` → `re_store_harvestmap_vienna` | PROVEN | **R04 patch** (materialnomaden.at/about) |
| `tool_oogstkaart_harvest_map` vs `harvestmap` | CONTRADICTION — keep separate | R03 |
| `rau` vs `thomas_rau` | CONTRADICTION — firm vs person | **R04** |

Superuse [Oogstkaart press release](https://superuse-studios.com/projects/oogstkaart/) confirms NL Oogstkaart ≠ AT HarvestMAP Vienna.

## Patch (11 merges — dry-run passed)

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r03_merge_nodes.patch.jsonl
```

Live apply (human gate):

```bash
python _scripts/apply_neo4j_review_patch.py \
  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r03_merge_nodes.patch.jsonl \
  --confirm "APPLY remediation_r03_merge_nodes.patch.jsonl TO mit-bestand"
```

### Post-apply expectations (dry-run 2026-06-06)

| Metric | Before | After (expected) |
|---|---:|---:|
| Nodes | 2295 | **2284** (−11) |
| Rels | 15327 | 15327 (redirected) |

Dry-run report: [`apply_reports/remediation_r03_merge_nodes.patch.apply_report.md`](../apply_reports/remediation_r03_merge_nodes.patch.apply_report.md)

Canonical survivors: `zrs_ingenieure`, `structural_xploration_lab_epfl`, `iemb_tu_berlin`, `albert_and_co`, `btu_cottbus`, `claus_asam`, `archipel_zero`, `pirmin_jung_schweiz_ag`, `tampere_university`.

## Deferred to human (not in R03 patch)

1. **Paris:** `services_techniques_ville_de_paris`, `ville_de_paris_pavillon_arsenal` identity vs `ville_de_paris`
2. **Biele brothers:** split or relink `herve_joel_biele`
3. **BIM triple:** deprecate/relabel generic `Software` nodes
4. **`prog_recreate_local`:** merge into `prog_recreate` vs keep as sub-pilot label
5. **`rau` vs `rau_architects`:** firm duplicate review (R04-escalate-001)

Generated 2026-06-06 (Remediation Wave 2, Agent R03).
