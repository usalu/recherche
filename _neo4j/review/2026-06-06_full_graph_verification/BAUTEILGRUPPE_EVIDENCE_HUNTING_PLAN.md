# Bauteilgruppe Evidence Hunting Plan

**Date:** 2026-06-07 · **Database:** `mit-bestand` · **Mode:** PLAN ONLY (read-only Neo4j; no graph mutations)

**Parent mission:** [`BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md`](BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md)

**Core problem:** `bg_*` slugs encode material + component + project in one token chain, but the web names the same batch in German, French, Dutch, or English — often at material-family or marketplace-category granularity. A literal slug search fails; category co-listing alone must not yield `PROVEN`.

---

## 1. Problem framing

### 1.1 Why `bg_*` is sensitive

| Signal | Count | Implication |
|---|---:|---|
| `:Bauteilgruppe` nodes | **364** | All ids `bg_*`; no `canonical_name`, no `primary_source_url` on nodes |
| Edges touching Bauteilgruppe | **6,684** | **416** W3 `delete_rel` ops skipped (W4) because endpoint is `bg_*` |
| v5 ledger rows involving `bg_*` | **6,684** | **852** `UNSUPPORTED` deferred for this mission |
| Outbound rels without `evidence_url` / `evidence_quote` | **~6,251** | Internet evidence gap is structural, not a handful of outliers |

Bauteilgruppe is the **reuse batch** layer: each node is a project-specific material/component bundle (often with quantity, donor city, or marketplace sourcing). Edges fan out to catalogue vocab (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`), process axes, regulation triggers, spatial links, and taxonomy. Many v5 `PROVEN` rows are **contract/logic** attestations from the element-proof campaign — not verbatim web quotes on the relationship. The hunting mission must upgrade **internet-evidence** quality without re-introducing category-inference false positives (the failure mode remediated in W3/W4 and Q04).

### 1.2 The naming challenge (live graph examples)

Slugs are stable ids; `name` is a display alias; dossiers and marketplaces use a third wording. Agents must reconcile all three **without merging nodes on string similarity** (`AGENTS.md` rule 3).

| `bg_*` id | Graph `name` | Dossier / intake alias | Likely web variants (not literal slug) |
|---|---|---|---|
| `bg_keramik_mehrere_maison_vignette_terracotta_floor_tiles` | 13,5 m² wiederverwendete… | **13,5 m² wiederverwendete Terrakotta-Bodenfliesen** (`p_maison_vignette_auderghem.kg.jsonl`) | FR: *carrelage*, *revêtement de sol*, *terre cuite*; EN: *terracotta floor tiles*, *reclaimed ceramic flooring*; marketplace: *zellige*, *glazed terracotta tile* (Rotor DC shop lexicon) |
| `bg_stahl_gelaender_verbiest_charleroi` | Geländer aus Charleroi | Geländer / steel railing batch from Charleroi donor | FR: *garde-corps*, *rambarde*; EN: *steel railing*, *balustrade*; partial: *métallerie* (too broad) |
| `bg_glas_mehrere_awm_partitions_doors` | Glass partitions and… | Glass partitions and doors (AWM office) | DE: *Glaswände*, *Trennwände*; FR: *cloisons vitrées*, *châssis*; EN: *glass partitions*, *internal glazing* |
| `bg_stahlbeton_mehrere_haus_hos_floor_elements` | Stahlbeton-Deckenelemente | Hollow-core / precast floor slabs (Haus HOS) | DE: *Deckenelemente*, *Hohldiele*; FR: *plancher*, *dalles*; EN: *precast floor elements*, *hollow core slabs* |
| `bg_ziegel_fassade_maison_vignette_reused_facing_bricks` | bg_reuse_ziegel_fassade… (display drift) | 3.000 wiederverwendete Ziegel / facing bricks | FR: *briques de parement*, *brique en terre cuite*; EN: *reclaimed facing bricks*, *cladding brick*; BE press: *Maison Vignette* + *briques récupérées* |

**Takeaway:** `mehrere` in the slug means *batch / multiple units*, not a searchable token. Project anchors (`maison_vignette`, `verbiest_charleroi`, `haus_hos`) must appear in quotes or listing context; material tokens (`keramik`, `terracotta`, `stahl`) and component tokens (`boden`, `gelaender`, `floor_tiles`) must match via **alias sets**, not substring of the full slug.

### 1.3 W4 exclusion recap

- **416** edges: W3 proposed `delete_rel` but skipped because `from` or `to` is `bg_*`.
- **852** v5 `UNSUPPORTED` rows: retained for alias-aware hunting; **no auto-delete** without mission sign-off and human review of high-impact regulation/spatial edges.

---

## 2. Naming normalization ladder

### 2.1 Slug decomposition (`bg_*` → structured tokens)

Parse id after stripping prefix `bg_`:

```
bg_{material}_{component_or_mehrere}_{project_anchor...}_{detail_tokens...}
```

| Segment | Role | Examples | Search use |
|---|---|---|---|
| **material** | Primary material family | `keramik`, `stahl`, `ziegel`, `stahlbeton`, `glas`, `holz`, `mehrere`* | Maps to `mat_*` aliases; `mehrere` → read material from `name` or linked `NUTZT_MATERIAL` |
| **component** | Bauteiltyp hint (if not `mehrere`) | `boden`, `wand`, `fassade`, `gelaender`, `dach`, `technik` | Maps to `bt_*` aliases |
| **quantity hint** | Often in `name`, not slug | `13,5 m²`, `3.000`, `mehrere` | Use in quote validation when dossier gives m²/count |
| **project anchor** | Tail tokens tied to `p_*` | `maison_vignette`, `verbiest_charleroi`, `awm`, `haus_hos` | **Required** for PROVEN on project-specific claims |
| **detail_tokens** | Product English in slug | `terracotta_floor_tiles`, `partitions_doors`, `reused_facing_bricks` | Split on `_`; drop stopwords (`reused`, `candidate`, `external`) |

\*When segment 2 is `mehrere`, segment 1 is still material; component comes from segment 4+ (`terracotta_floor_tiles` → boden + keramik).

**Implementation:** `scripts/bg_slug_decompose.py` (recommended) — output JSON per node:

```json
{
  "bg_id": "bg_keramik_mehrere_maison_vignette_terracotta_floor_tiles",
  "material_token": "keramik",
  "component_tokens": ["boden", "floor", "tiles", "terracotta"],
  "project_anchor": "maison_vignette",
  "projekt_id": "p_maison_vignette_auderghem",
  "quantity_hint": "13.5 m2"
}
```

Join with `(p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg)` for `projekt_id`, `projekt.name`, and geo URLs from `akteur_typ_projekt_geo.json` / `reuse_geo_graph.json`.

### 2.2 Search alias sets (DE / FR / NL / EN)

Seed from:

1. `controlled_vocabulary.seed.kg.jsonl` (`mat_*`, `bt_*` names)
2. `EXTRA_TOKENS` in [`_agent_q04_catalogue_edges.py`](_agent_q04_catalogue_edges.py) (lines 68–100)
3. Bauteilbörse enrichment raw strings (`*.enrichment.json`, `FINAL_EVIDENCE_LEDGER_ALL_ROWS.csv` `raw material` / `raw component` columns)
4. Per-`bg_*` dossier `raw_name` / `name` from project batch JSONL (`intake/archive/.../p_*.kg.jsonl`)

**Material families (starter table — extend from corpus):**

| Graph token | DE | FR | NL | EN |
|---|---|---|---|---|
| keramik | Keramik, Fliesen, Feinsteinzeug, Terrakotta | céramique, carrelage, faïence, terre cuite | tegel, keramiek | ceramic, tile, terracotta, faience |
| ziegel | Ziegel, Klinker, Backstein | brique, terre cuite | baksteen, steen | brick, facing brick, clay brick |
| stahl | Stahl, Metall, Eisen | acier, métal | staal | steel, metal |
| glas | Glas, Verglasung | verre, vitrage | glas | glass, glazing |
| holz | Holz, Holzbau, Brett | bois, panneau | hout | wood, timber, panel |
| stahlbeton | Stahlbeton, Beton, Decke | béton armé, dalle | beton, gewapend | reinforced concrete, precast |
| naturstein | Naturstein, Stein | pierre naturelle | natuursteen | natural stone |
| daemmstoff | Dämmstoff, Isolierung | isolant, laine | isolatie | insulation |

**Component families (starter table):**

| Graph token | DE | FR | NL | EN |
|---|---|---|---|---|
| boden | Boden, Bodenbelag, Estrich | sol, revêtement de sol | vloer | floor, flooring |
| wand | Wand, Wandbekleidung | mur, parement, cloison | wand | wall, wall cladding |
| fassade | Fassade, Fassadenplatte | façade, bardage | gevel | facade, cladding |
| gelaender | Geländer, Brüstung | garde-corps, rambarde | leuning | railing, balustrade |
| dach | Dach, Dachziegel | toiture, tuile | dak, dakpan | roof, roof tile |
| fenster | Fenster | fenêtre, châssis | raam | window |
| technik | Sanitär, Technik, Installation | sanitaire, plomberie | sanitair | sanitary, MEP |
| decke | Decke, Deckenelement | plafond, plancher, dalle | plafond, vloerplaat | ceiling, slab |

**Project anchor aliases:** derive from `p_*.name`, city tokens (`auderghem`, `charleroi`, `brussels`), building names (`Maison Vignette`, `Verbiest`, `Haus HOS`), and `linked_projekt_name` in `akteur_typ_projekt_geo.json`.

### 2.3 `name` property vs slug vs dossier titles

| Source | Priority | Use |
|---|---|---|
| Dossier `name` / `raw_name` in `p_*.kg.jsonl` | **Highest** for quote matching | Often richest German/French wording |
| Node `bg.name` | Display alias | May be truncated (`…`); never sole anchor |
| Slug tokens | Stable decomposition | Alias generation, not literal search |
| Marketplace listing title | Per-listing PROVEN | Must pair with project or listing id when index page is shared |

Never change `bg_*` id based on a better web string. Record matched aliases in `notes` + `evidence_basis`.

### 2.4 Trigram / token overlap scoring (candidate quotes)

Normalize text: NFKD, strip accents, lower case, collapse whitespace (reuse `norm_text()` from Q04).

**Token hit:** word-boundary match, min length 4 (except FR/NL 3-char tokens in allowlist: `sol`, `mur`, `bois`, `dak`).

**Scores (per candidate sentence or ≤300 char quote):**

| Feature | Weight | Threshold |
|---|---|---|
| Project anchor hit (name, city, or `p_*` title) | +4 | **Required** for PROVEN on bg_-anchored edges |
| Component family hit (any `bt_*` alias) | +3 | ≥1 required |
| Material family hit (any `mat_*` alias) | +2 | ≥1 required for `NUTZT_MATERIAL` / material-taxonomy edges |
| Quantity hint match (m², count) | +2 | Bonus; not required |
| Listing title token overlap | +3 | Required when URL is marketplace **index** |
| Slug token literal match | +1 | Low weight — slug tokens often absent on web |

**Verdict mapping:**

| Score | Project anchor? | Component? | Verdict |
|---|---|---|---|
| ≥8 | yes | yes | `PROVEN` candidate (still needs verbatim quote + pairwise rule) |
| 5–7 | yes | partial / family only | `PARTIAL` |
| ≥5 | no | yes | `PARTIAL` at best — **not** PROVEN |
| <5 | — | — | `UNSUPPORTED` |

**Trigram fallback** (when token lists fail on inflected FR): `SequenceMatcher` on normalized quote vs best alias phrase; accept if ratio **≥ 0.72** on strings ≥12 chars **and** project anchor still present.

**False-positive guard:** If page lists ≥8 unrelated component types in one block (category nav, footer sitemap) without naming the project or listing → cap score at 4 → `UNSUPPORTED`.

---

## 3. Source hierarchy (search ladder per mission BG-M1…M5)

For each mission, search **in order**; stop early only when PROVEN gate is satisfied. Record `basis_type` and highest tier used.

### BG-M1 — Catalogue edges (`HAT_BAUTEILTYP`, `NUTZT_MATERIAL`) · ~855 edges

| Tier | Sources | PROVEN | PARTIAL | UNSUPPORTED |
|---|---|---|---|---|
| **Primary** | Project dossier markdown in `intake/inbox/` / `intake/archive/.../p_*.kg.jsonl`; project page URL from `reuse_geo_graph.json` / `akteur_typ_projekt_geo.json` (`source_url` on linked projekt); **per-product** marketplace URL if `BETEILIGT_AN` or enrichment names this `bg_*` | Quote names **project or bg display** AND **component/material family** (via alias) AND target vocab (`bt_*` / `mat_*`) | Page names material family on project page but not exact vocab node | Category page lists component among many without project/listing anchor |
| **Secondary** | Bauteilbörse `*.enrichment.json`, `FINAL_EVIDENCE_LEDGER_ALL_ROWS.csv`; press/architect pages (Opalis, FCRBE sheets); PDF factsheets | Same as primary with third-party project article | Actor shop mentions material but not this project | Shop homepage category only (Rotor `/shop` brick+floor+sanitary list) |
| **Tertiary** | `archive.org` snapshot of dead project URL; image `SCREENSHOT_NOTES.md` under `intake/inbox/BAUTEILBÖRSE IMAGES/` | Only if caption names project + component | Caption material only | OCR noise / generic "Bauteile" |

### BG-M2 — Process axis (`HAT_PROZESSPHASE`, `HAT_BESCHAFFUNGSWEG`, `HAT_LOGISTIK`) · ~1,372 edges

| Tier | Sources | PROVEN | PARTIAL | UNSUPPORTED |
|---|---|---|---|---|
| **Primary** | Project dossier describing procurement (Bauteilbörse), logistics, phasing; contract clause in `_neo4j/contracts/project_batches_v1_1` **plus** dossier sentence naming the component batch | Dossier links **this bg batch** to process term (e.g. *über Rotor DC bezogen*, *Materialmatching*) | Generic project reuse narrative without naming component family | Contract-only with no dossier mention of batch |
| **Secondary** | Marketplace FAQ / process pages **when** listing URL is batch-specific | Listing states procurement channel for **that product** | Platform generic "how to buy" | Platform index |
| **Tertiary** | Tender / award PDFs mentioning salvaged component | Named project + component | Project-only | Generic circular economy text |

### BG-M3 — Regulation triggers (`ERFORDERT_NACHWEIS`, `TRIGGERS_REGULIERUNGSFRAGE`) · ~1,677 edges

| Tier | Sources | PROVEN | PARTIAL | UNSUPPORTED |
|---|---|---|---|---|
| **Primary** | Law/regulation node `source_url` (graph); official legal text naming material class or doc requirement | Legal text supports requirement for **material/component class** of this bg | Law supports general building doc, not material-specific | Inference from bg material without legal cite |
| **Secondary** | Agency guidance PDF (UBA, Bruxelles Environnement) citing project **as example** | Guideline names project + material | Guideline material class only | |
| **Tertiary** | Academic / case-study citing regulation in context of project | Named project + regulation + material | Regulation + material, no project | |

**Note:** Many edges are structurally valid; evidence may live on law nodes. Hunting still records bg_-specific **application** quote where dossier ties batch to requirement.

### BG-M4 — Spatial / donor (`AUS_SPENDER`, `IN_EMPFANGSOBJEKT`, inbound `HAT_BAUTEILGRUPPE`) · ~840 edges

| Tier | Sources | PROVEN | PARTIAL | UNSUPPORTED |
|---|---|---|---|---|
| **Primary** | `reuse_geo_graph.json` donor/receiver `source_url`; dossier donor building name; `akteur_typ_projekt_geo.json` | Quote names **donor city/building** AND **component** AND receiver project | Donor city + project, component family weak | Geo proximity only |
| **Secondary** | Local press ("materials from Charleroi"); demolition permit | All three anchors | Two of three | City name only |
| **Tertiary** | Map captions, photo essays | Visual + caption text naming batch | Image with no caption | |

### BG-M5 — Material taxonomy (`HAT_MATERIALGRUPPE`, `HAT_RUECKBAUVERFAHREN`, `HAT_AUFBEREITUNG`) · ~891 edges

| Tier | Sources | PROVEN | PARTIAL | UNSUPPORTED |
|---|---|---|---|---|
| **Primary** | Dossier demounting/prep method for batch; `controlled_vocabulary.seed.kg.jsonl` + dossier crosswalk | Dossier names bg batch + taxonomy target | Dossier names material + generic prep | Material-only → taxonomy edge |
| **Secondary** | Marketplace condition notes (cleaned, sorted, tested) on **listing** | Listing-specific | Shop "we test materials" boilerplate | |
| **Tertiary** | Manufacturer reclaim guides | Material + process | Material only | |

### Cross-mission verdict contract

- **`PROVEN`:** Verbatim `proof_quote` (≤300 chars); `fetched=true`; score ≥8 with project anchor; `evidence_basis=bg_hunt_alias_match`; both endpoints satisfied per §4 step 5.
- **`PARTIAL`:** Real quote but weaker claim (family match, third-party, missing quantity); `proposed_action` ∈ {`KEEP`, `RELABEL`, `DOWNGRADE`} — not patch-upgrade to PROVEN.
- **`UNSUPPORTED`:** Research attempted (≥3 query variants, ≥2 tiers); no qualifying quote → retain for W4-style review; `proposed_action` = `KEEP_DEFERRED` or `ESCALATE_HUMAN` (not auto-`DELETE` on bg_).

---

## 4. Multi-wording proof protocol

Step-by-step for hunting agents BG-H1…H5.

### Step 1 — Extract anchor tokens

Per edge row `(bg_id, rel_type, to_id)`:

1. Run slug decomposition (§2.1).
2. Load `bg.name`, linked `p_*` id/name, donor/receiver from `reuse_geo_graph.json`.
3. Load dossier lines from matching `p_*.kg.jsonl` node entry (search `bg_` or legacy id).
4. Load marketplace actor: `BETEILIGT_AN` partners + `akteur_typ_projekt_geo.json` URLs.
5. Build alias sets: `project_aliases[]`, `material_aliases[]`, `component_aliases[]`, `target_aliases[]` (from `to_id` vocab name + `EXTRA_TOKENS`).

### Step 2 — Generate 5–10 search queries per edge

Do **not** search the full slug. Template mix:

1. `{projekt_name} {material_alias} {component_alias}` (DE)
2. `{projekt_name} {FR material} {FR component}` (e.g. *Maison Vignette carrelage terre cuite*)
3. `{donor_city} {component_alias} {material_alias}` (spatial missions)
4. `{marketplace_actor} {component_alias} {project_city}`
5. `{listing_title_fragment}` from enrichment if present
6. `site:{domain} {project_anchor} {component_alias}`
7. `{projekt_name} wiederverwendet {component_alias}`
8. `{english_project_name} reclaimed {english_material} {english_component}`
9. Archive: `site:web.archive.org {primary_url}`
10. PDF: `{projekt_name} filetype:pdf {material_alias}`

### Step 3 — Fetch candidate pages

- `WebFetch` primary URLs first (project page, listing URL on rel if any, geo `source_url`).
- Cache by URL across edges in the same project (Maison Vignette: one fetch serves many `bg_*`).
- Rate limit: **≤1 req/s** per host, **≤30 req/min** global; backoff on 429.
- Retry once on timeout; then `WebSearch` for alternate URL.

### Step 4 — Score quotes

A candidate quote must mention:

- **(A)** project OR listing title OR donor building/city tied to this batch, **AND**
- **(B)** component family (not generic *Bauteile*, *matériaux de réemploi*, *building components* alone)

Use §2.4 scoring. Extract best verbatim sentence (`extract_verbatim_sentence` pattern from Q04).

Set `evidence_basis` = `bg_hunt_alias_match` and `notes` = JSON snippet:

```json
{"matched_aliases": ["carrelage", "Maison Vignette", "terre cuite"], "score": 9, "tier": "primary"}
```

### Step 5 — Pairwise rule for relationships

| rel pattern | Requirement |
|---|---|
| `bg_* → bt_*` / `mat_*` | Quote ties **this batch** (or unambiguous project+component phrase) to the classification |
| `bg_* → process/reg vocab` | Quote ties **batch or project** to process term; contract alone = logic-PROVEN (already in ledger) — hunting adds `evidence_url` if external |
| `bg_* → spatial node` | Quote names donor/receiver **and** component |
| `Akteur → bg_*` (`BETEILIGT_AN`) | Actor's **own** listing or project page names component; not actor index |
| `p_* → bg_*` (`HAT_BAUTEILGRUPPE`) | Project dossier or official project page lists component batch |

### Step 6 — Ledger / patch fields

Proposed rel properties on upgrade (for aggregator patch batch, not applied by hunters):

- `evidence_url`
- `evidence_quote`
- `evidence_confidence` ∈ {`high`, `medium`, `low`}
- `evidence_basis` = `bg_hunt_alias_match`
- `review_run` = `bg_hunt_2026_06_07`

---

## 5. Agent execution plan (5 hunters + 1 aggregator)

### 5.1 Fleet overview

| Agent | Mission | Scope filter (disjoint) | ~edges | Ledger shard |
|---|---|---|---:|---|
| **BG-H1** | BG-M1 | `rel_type ∈ {HAT_BAUTEILTYP, NUTZT_MATERIAL}` ∧ (`from_id` starts with `bg_` OR `to_id` starts with `bg_`) | 855 | `ledger/bg_hunt_h1.csv` |
| **BG-H2** | BG-M2 | `rel_type ∈ {HAT_PROZESSPHASE, HAT_BESCHAFFUNGSWEG, HAT_LOGISTIK}` ∧ bg endpoint | 1,372 | `ledger/bg_hunt_h2.csv` |
| **BG-H3** | BG-M3 | `rel_type ∈ {ERFORDERT_NACHWEIS, TRIGGERS_REGULIERUNGSFRAGE}` ∧ bg endpoint | 1,677 | `ledger/bg_hunt_h3.csv` |
| **BG-H4** | BG-M4 | `rel_type ∈ {AUS_SPENDER, IN_EMPFANGSOBJEKT}` ∨ (`rel_type=HAT_BAUTEILGRUPPE` ∧ `to_id` starts with `bg_`) | 840 | `ledger/bg_hunt_h4.csv` |
| **BG-H5** | BG-M5 | `rel_type ∈ {HAT_MATERIALGRUPPE, HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG}` ∧ bg endpoint | 891 | `ledger/bg_hunt_h5.csv` |
| **BG-H6** | Aggregator | Merge H1–H5, dedupe URL cache stats, emit patches | — | `ledger/bg_hunt_merged.csv`, `patches/bg_hunt_upgrades.patch.jsonl` |

**Disjointness:** Each live `element_id` appears in exactly one hunter shard (partition by `rel_type` first; if multi-label conflict, assign to lowest mission number).

**Batch sizes:** Process in project clusters — sort by `projekt_id`, batches of **40–60 edges** sharing fetch cache. Target **~120–180 edges/agent/day** with manual WebFetch.

**Scope enumeration Cypher (per agent — replace `REL_TYPES`):**

```cypher
MATCH (bg:Bauteilgruppe)-[r]->(t)
WHERE type(r) IN $REL_TYPES
RETURN elementId(r) AS element_id, bg.id AS from_id, t.id AS to_id,
       type(r) AS rel_type, bg.name AS bg_name
ORDER BY from_id, rel_type
```

For inbound `HAT_BAUTEILGRUPPE` (BG-H4 only):

```cypher
MATCH (p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
RETURN elementId(r) AS element_id, p.id AS from_id, bg.id AS to_id,
       type(r) AS rel_type, bg.name AS bg_name
ORDER BY from_id
```

### 5.2 BG-H6 aggregator duties

1. Concatenate `bg_hunt_h1.csv` … `bg_hunt_h5.csv`; verify row count = 5,635 hunted edges (subset of 6,684; remaining 1,049 are other rel types deferred to phase 2).
2. Dedupe proposed `set_rel_properties` by `element_id`; prefer highest score.
3. Emit `reports/bg_hunt_summary.md`: verdict deltas, top 20 alias wins, top 20 false-positive near-misses.
4. Emit `patches/bg_hunt_upgrades.patch.jsonl` — **proposal only**; human apply after spot-check.
5. Update v5 ledger columns `verdict_after`, `evidence_basis` (see §7).

### 5.3 Prompt templates

Base template: [`AGENT_PROMPT_TEMPLATE.md`](AGENT_PROMPT_TEMPLATE.md). Replace placeholders per agent.

#### BG-H1 prompt (catalogue)

```
You are **BG-H1** (Bauteilgruppe catalogue hunter). READ-ONLY Neo4j.

Read:
- BAUTEILGRUPPE_EVIDENCE_HUNTING_PLAN.md §2–§4
- BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md

Scope: HAT_BAUTEILTYP, NUTZT_MATERIAL edges with bg_* endpoint.
Enumerate via read-cypher (REL_TYPES = ['HAT_BAUTEILTYP','NUTZT_MATERIAL']).

For each edge:
1. Decompose bg_* slug; load project + dossier aliases.
2. Generate 5–10 multilingual queries (NOT literal slug).
3. Fetch primary project URL + marketplace listing if linked.
4. Score quote: project anchor AND component/material family (§2.4).
5. NEVER PROVEN on category co-listing alone (§6).

evidence_basis must be `bg_hunt_alias_match` when upgrading.
Write ledger/bg_hunt_h1.csv incrementally.

{{SCOPE_CYPHER from §5.1}}
```

#### BG-H2 prompt (process axis)

```
You are **BG-H2** (process axis hunter). Scope: HAT_PROZESSPHASE, HAT_BESCHAFFUNGSWEG, HAT_LOGISTIK.

Prioritize dossier sentences tying THIS component batch to procurement/logistics/phasing.
Marketplace process pages count only when listing-specific.

If only contract supports edge and dossier silent: verdict stays logic-PROVEN; note `no_external_upgrade`.
```

#### BG-H3 prompt (regulation)

```
You are **BG-H3** (regulation hunter). Scope: ERFORDERT_NACHWEIS, TRIGGERS_REGULIERUNGSFRAGE.

Fetch law node source_url from graph. Quote must support material/component class for bg batch.
Dossier may tie batch to requirement — prefer primary legal text + dossier cross-cite.
```

#### BG-H4 prompt (spatial / donor)

```
You are **BG-H4** (spatial hunter). Scope: AUS_SPENDER, IN_EMPFANGSOBJEKT, inbound HAT_BAUTEILGRUPPE.

Use reuse_geo_graph.json + akteur_typ_projekt_geo.json for donor/receiver URLs.
Quote must name donor city/building AND component AND receiver project where claim is directional.
```

#### BG-H5 prompt (material taxonomy)

```
You are **BG-H5** (taxonomy hunter). Scope: HAT_MATERIALGRUPPE, HAT_RUECKBAUVERFAHREN, HAT_AUFBEREITUNG.

Require batch-specific prep/demount wording; material-only match → PARTIAL max.
```

#### BG-H6 prompt (aggregator)

```
You are **BG-H6** (aggregator). Read-only merge of bg_hunt_h1..h5 ledgers.

Validate: no duplicate element_id; every PROVEN has proof_quote + matched_aliases in notes.
Flag rows with score <8 for human review. Emit patch JSONL and summary report.
Do NOT apply patches.
```

---

## 6. Anti-patterns (explicit bans)

| Ban | Example | Correct action |
|---|---|---|
| **Category co-listing** | Rotor `/shop` lists Brick, Floor, Sanitary, Roof… | `UNSUPPORTED` for `bg_keramik_*` unless quote names project/listing |
| **Shared marketplace index** | `restado.de/baustoff/fliesen-22/` category with 50 tiles | Need product URL + title match; index alone → `PARTIAL` at best |
| **Material-only, no project** | "terracotta tile" on shop with no Maison Vignette | `PARTIAL` or `UNSUPPORTED` — not PROVEN for project-specific bg |
| **Generic reuse vocabulary** | "circular economy", "réemploi de matériaux" | Ignore — no component family |
| **Slug literal search** | Googling `bg_keramik_mehrere_maison_vignette_terracotta_floor_tiles` | Use decomposition + aliases |
| **Cross-batch transfer** | Proof for `bg_keramik_boden_verbiest_charleroi` applied to `bg_naturstein_wand_verbiest_charleroi` | One quote → one `element_id` only |
| **Actor homepage = component proof** | `batiterre.be` shop category lists Carrelage, Faïence | Does not prove Verbiest batch edge |
| **Third-party laundry list** | Press article listing "fenêtres, portes, carrelage" for a platform | `PARTIAL` unless project named |
| **Merge on name similarity** | "Fliesen" ≈ "carrelage" ⇒ merge bg nodes | Aliases for matching only; never merge |
| **Logic-PROVEN override** | Existing contract PROVEN → add fake web quote | Hunter may add URL; must not downgrade logic proofs without contradiction |

---

## 7. Tooling recommendations

### 7.1 Scripts (proposed paths under this review folder)

| Script | Purpose |
|---|---|
| `_neo4j/review/2026-06-06_full_graph_verification/bg_hunt_build_alias_table.py` | Export all 364 `bg_*` → alias JSONL from slug + dossier + vocab |
| `_neo4j/review/2026-06-06_full_graph_verification/bg_hunt_build_shards.py` | Emit disjoint CSV scopes per BG-H1…H5 from live graph + v5 ledger |
| `_neo4j/review/2026-06-06_full_graph_verification/bg_hunt_quote_scorer.py` | Score fetched HTML/text; stub below |
| `_neo4j/review/2026-06-06_full_graph_verification/bg_hunt_aggregate.py` | BG-H6 merge + patch proposal |

**Inputs:** `reuse_geo_graph.json`, `akteur_typ_projekt_geo.json`, `intake/archive/.../p_*.kg.jsonl`, `bauteilboersen_*.enrichment.json`, `controlled_vocabulary.seed.kg.jsonl`.

### 7.2 Quote scorer stub

Path: `bg_hunt_quote_scorer.py` (minimal; extend Q04 helpers):

```python
"""Score a candidate quote against bg_hunt alias sets. See BAUTEILGRUPPE_EVIDENCE_HUNTING_PLAN §2.4."""

from difflib import SequenceMatcher

def score_quote(quote: str, project_aliases: list[str], component_aliases: list[str],
                material_aliases: list[str], *, require_project: bool = True) -> dict:
    q = norm_text(quote)
    pa = sum(4 for a in project_aliases if token_hit(a, q))
    ca = sum(3 for a in component_aliases if token_hit(a, q))
    ma = sum(2 for a in material_aliases if token_hit(a, q))
    total = pa + ca + ma
    if require_project and pa == 0:
        total = min(total, 4)
    return {"score": total, "project_hit": pa > 0, "component_hit": ca > 0,
            "material_hit": ma > 0, "proven_eligible": total >= 8 and pa > 0 and ca > 0}
```

Reuse `norm_text`, `token_hit`, `is_valid_quote`, `extract_verbatim_sentence` from [`_agent_q04_catalogue_edges.py`](_agent_q04_catalogue_edges.py).

### 7.3 Ledger column extensions

Extend hunter shard CSV beyond [`VERIFICATION_LEDGER.schema.csv`](VERIFICATION_LEDGER.schema.csv):

| Column | Description |
|---|---|
| `verdict_before` | From v5 ledger |
| `verdict_after` | Hunter result |
| `evidence_basis` | `bg_hunt_alias_match` \| `logic` \| `dossier` \| empty |
| `matched_aliases` | Semicolon-separated tokens that fired |
| `alias_score` | Numeric §2.4 score |
| `project_anchor_hit` | `true` / `false` |
| `component_family_hit` | `true` / `false` |
| `search_tier` | `primary` \| `secondary` \| `tertiary` |
| `queries_tried` | Count of distinct queries |
| `graph_element_id` | `elementId(r)` for patch join |

BG-H6 writes merged file compatible with existing element ledger merge scripts (`verdict` → `verdict_after` on upgrade rows only).

---

## 8. Success metrics

### 8.1 Baseline (v5 ledger, 2026-06-07)

| Metric | Value |
|---|---:|
| bg_* edge rows | 6,684 |
| PROVEN | 5,768 (86.3%) — mostly logic/contract |
| UNSUPPORTED | **852** (12.7%) — **primary hunting target** |
| PARTIAL | 56 |
| MISSING_EVIDENCE | 8 |
| Outbound rels missing `evidence_url` | ~6,251 |

### 8.2 Targets (post BG-H1…H6)

| Metric | Target |
|---|---|
| UNSUPPORTED reduction | **≥40%** of 852 → ≤510 remaining (≥342 upgraded or reclassified) |
| New external `evidence_url` on bg_ rels | **≥250** high-confidence upgrades |
| PROVEN lift (internet-backed) | **+15 pp** on hunted 5,635-edge subset for rows that were logic-PROVEN without quote |
| Max false PROVEN rate | **≤2%** on spot-check sample (n≥50) — if exceeded, halt patch apply |
| PARTIAL acceptance | ≤**8%** of hunted edges; must have documented alias gap |

### 8.3 Human ESCALATE queue criteria

Route to `ESCALATE_HUMAN` when any of:

1. `alias_score` 7–8 with high graph impact (`ERFORDERT_NACHWEIS`, `AUS_SPENDER`, inbound `HAT_BAUTEILGRUPPE`).
2. Conflicting quotes across sources (dossier vs marketplace).
3. `bg.name` display drift (raw slug in name field) — e.g. `bg_reuse_ziegel_fassade_*`.
4. Donor = `unknown_donors` pool with only regional geo.
5. Candidate PROVEN would be first external evidence for regulation edge affecting ≥5 bg batches.
6. Marketplace listing in Dutch/French with ambiguous component (sanitary vs ceramic).
7. W4-skipped delete candidate — hunter found weak evidence; needs mission sign-off.

### 8.4 Done criteria (campaign close)

- [ ] All 5 hunter ledgers complete (no empty `verdict_after`).
- [ ] BG-H6 summary + patch JSONL reviewed.
- [ ] Spot-check 50 PROVEN upgrades — ≤1 false positive.
- [ ] `BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md` updated with post-hunt counts.
- [ ] No graph mutations until human approves patch batch.

---

## References

| Artifact | Path |
|---|---|
| Mission plan | [`BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md`](BAUTEILGRUPPE_EVIDENCE_MISSION_PLAN.md) |
| Geo / project URLs | [`../2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json`](../2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json), `reuse_geo_graph.json` |
| v5 ledger (bg rows) | [`VERIFICATION_LEDGER_ELEMENT_v5.csv`](VERIFICATION_LEDGER_ELEMENT_v5.csv) |
| Q04 strict gate / tokens | [`_agent_q04_catalogue_edges.py`](_agent_q04_catalogue_edges.py) |
| Agent prompt base | [`AGENT_PROMPT_TEMPLATE.md`](AGENT_PROMPT_TEMPLATE.md) |
| Evidence rules | [`AGENTS.md`](../../../AGENTS.md) |
| Dossier example | `intake/archive/.../batch_009/p_maison_vignette_auderghem.kg.jsonl` |
| Bauteilbörse enrichment | `intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results/*.enrichment.json` |
| W4 deferral | [`VERIFICATION_PLAN_W4_SELECTIVE_DELETE_4_AGENTS.md`](VERIFICATION_PLAN_W4_SELECTIVE_DELETE_4_AGENTS.md) (if present) |

---

*Plan authored 2026-06-07. Neo4j queries used read-only `read-cypher` on `mit-bestand`.*
