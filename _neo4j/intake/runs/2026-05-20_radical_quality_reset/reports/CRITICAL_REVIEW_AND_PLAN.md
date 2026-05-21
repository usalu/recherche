# Critical Review and Radical Quality-First Reset — `mit-bestand`

- **Document type:** Synthesis report (no graph writes)
- **Synthesis date (UTC):** 2026-05-21
- **Plan reference:** `c:\Users\Kinosh\.cursor\plans\radical_quality-first_reset_8d1e2b66.plan.md`
- **Run dir:** `E:\recherche\_neo4j\intake\runs\2026-05-20_radical_quality_reset\`
- **Database:** `mit-bestand` on `bolt://localhost:7687` (read-only)
- **Source transcript:** `5e8b5e5d-40f4-44fd-981e-ad8488fdcccc.jsonl` (4-layer skeptical critique + multi-agent execution)
- **Authoritative audits cited:** `FINAL_PASS2_AUDIT.md`, `FINAL_PLAN_COMPLETION_AUDIT.md`, `post_repair_verification.md`, all `pass2_verify_*.md` and `final_verify_*.md` reports, all 5 `repair_*.md` reports.

---

## 1. Executive summary

The plan `radical_quality-first_reset_8d1e2b66` converted `mit-bestand` from a **2 580-node / 19 989-edge curated catalogue scored 2.2 / 10** by a four-layer skeptical review into a **3 802-node / 25 023-edge tier-aware decision graph** that passes all 7 plan acceptance queries on the live database. Two binding rules drove every change: **Rule A — remap before delete** (nodes with degree ≥ 2 are relabelled / demoted / merged, not deleted) and **Rule B — ≥ 5 connections per node for any new label**. Execution ran as **12 background agents in 7 waves (wave 0 → wave 6)** following the dependency order Phase 1 → 2 → 4 → 4c → 4b → 3 → 5. The initial Wave-6 acceptance gate failed exactly **1 of 7 acceptance queries** (Q1 Reuse Story, 0 rows) and surfaced four other documented residuals (Phase 1.2 anchor regression, Phase 1.5/1.6 norm + actor leftovers, Phase 2.5 `:RechtlicheBedingung` not demoted, Phase 2.7 Projekt-panel + Phase 5.1 `p_circle_house` narrative gap); **five named repairs (A, B, C, D, E)** closed the first four and explicitly accepted the fifth. Pass-2 detailed verification (12 verifiers, 2026-05-21 07:59 UTC) confirms **all gates green** — tier distribution 11/68/22, Q1=266 rows, Q2=799+347 rows, Q3=4 rows / 3 projects, Q4=1 actor (RotorDC), Q5=20/20 ReuseRules wired, Q6 origins live at 3 188 curated / 2 948 derived / 347 inferred, Q7=958 case-markdown → ZITIERT_QUELLE rows. The graph is now ready for downstream consumption with `quality_tier='tier_1_decision_grade'` as the default visibility cut (11 projects). Two minor non-blocking residuals remain: 4 empty-registered node labels plus 6 empty-registered relationship types (expected leftovers from plan-mandated renames / demotions), and a documented `p_circle_house` tier-2-vs-narrative-tier-3 disposition kept as Tier 2 per the §5.1 formula.

---

## 2. Layer 1 — First-pass critical evaluation as a skeptical first-time user

Layer 1 was a skeptical first-time user trying to answer real reuse questions against the live graph (then 2 580 nodes / 19 989 relationships) with ~30 probing Cypher queries.

### 2.1 Brutal verdict (live counts cited verbatim)

> The graph looks impressive in shape but breaks the moment a real user asks "what was reused, how much, from where to where, by whom, and with what proof?" — because **92 % of `Bauteilgruppe` nodes carry no quantity at all**, **only 14 of 112 `Wiederverwendungskette` chains link both a donor and a receiver building**, and **80–100 % of the heaviest relationships (`BELEGT_IN`, `HAT_AKTEURROLLE`, `HAT_PROZESSPHASE`, `AUS_BAUWERK`, `EINGEBAUT_IN`) have empty `evidence` properties**. The `Projekt` node is wildly over-modeled with ~250 properties (including one-offs like `zahnbuersten_anzahl_min`, `floppy_discs_anzahl`, `denim_tonnes`, `cleveland_repurposed_steel_t`) of which only 3 are reliably filled, while the central reuse % field is filled in **4 of 91 projects**. Two parallel role systems, three near-synonymous reuse categories, and a `Status` label fusing five orthogonal axes complete the picture. **It is a defensible research archive, but as a decision graph it is currently unusable without re-modeling.**

### 2.2 Score: 2.8 / 10

| Dimension | Score | Justification |
|---|---:|---|
| Usability (a new user finds answers) | **3.5** | Needs deep schema knowledge; 60+ relationship types; German-only names; no obvious entry points |
| Semantic clarity (labels mean one thing) | **4** | Status, WiederverwendungsArt, Bauwerk roles all conflate concepts |
| Queryability (clean Cypher possible) | **3** | Property duplication forces COALESCE across 4–7 fields; chains are mostly hollow shells |
| Trust / evidence model | **2.5** | `evidence` empty on 80–100 % of major edges; only 8 % of sources have `access_date` |
| Completeness (quantitative coverage) | **2** | 92 % of `Bauteilgruppe` lack any quantity; only 4 % of projects state a reuse share |
| Decision value (drives reuse decisions) | **2** | Cannot compare projects, normalize KPIs, or trace mass flows |

### 2.3 Top 15 weaknesses (live numbers, verbatim from transcript)

1. **Empty reuse chains:** `Wiederverwendungskette` is the named donor→receiver abstraction, yet only **14 / 112 (12.5 %)** have both `AUS_BAUWERK` and `EINGEBAUT_IN`. 98 chains are floating concepts with no source and no destination.
2. **Quantity vacuum on `Bauteilgruppe`:** **340 / 369 (92 %)** carry no `menge_t`, `menge_stueck`, `menge_m2`, `menge_kg` or `menge_m`. The literal question "how much was reused" is unanswerable for 9 of 10 components.
3. **Evidence fields are mostly empty:** `BELEGT_IN` 81 % no excerpt; `HAT_AKTEURROLLE` (1 191), `HAT_PROZESSPHASE` (716), `HAT_AKTEURTYP` (662), `ZITIERT_QUELLE` (370) at **100 %** no evidence; `AUS_BAUWERK` 87 % empty, `EINGEBAUT_IN` 88 % empty.
4. **`Projekt` is a 250-property junk drawer:** only `id`, `name`, `source_scope` fill at 100 %; the next-best (`bewertung`, `note`, `projektstatus_text`) sit at 75 %; `reuse_anteil_prozent` 4 %, `co2_einsparung_t` 8 %, `bgf_m2` 3 %.
5. **One-shot project properties polluting the schema:** `cleveland_repurposed_steel_t`, `house_of_fraser_steel_reused_t_min/_mid/_conflict`, `denim_tonnes`, `dvd_cases_anzahl`, `floppy_discs_anzahl`, `videokassetten_anzahl`, `zahnbuersten_anzahl_min/max`, `granitfliesen_anzahl`, `holztueren_anzahl` — these belong on `Bauteilgruppe`, not on `Projekt`.
6. **Property duplication for the same concept:** completion year has at least 7 fields (`jahr_fertigstellung` 31, `fertigstellung_jahr` 7, `baujahr` 1, `baujahr_von` 1, `bau_jahr_von` 2, `jahr_bauzeit_start` 1, `start_jahr` 1, `jahr_start` 2). Area has `flaeche_m2`, `flaeche_bestand_m2`, `bgf_m2`, `nutzflaeche_m2`, plus `_min/_max/_alternative` permutations.
7. **Two parallel role systems:** typed `Akteurrolle` (controlled vocab, 1 191 edges) and `BETEILIGT_AN.rolle_text` (free text) — multilingual chaos: `"ar_architektur"`, `"structural engineer"`, `"structural engineer (person)"`, `"Ausführungsplanung und Bauleitung"`.
8. **`Status` label conflates 5 orthogonal axes:** lifecycle, permanence (`Temporaer`), maturity (`Prototyp`/`Vorgeschlagen`/`Wettbewerb`), outcome (`Verworfen`/`Rueckgebaut`), data quality (`Unklar`). Also `Gebaut`≈`Realisiert`.
9. **`WiederverwendungsArt` overlaps and category-mixing:** `Bestandserhalt` ≈ `Same_Site_ReUse` ≈ `Weiterbauen_im_Bestand`; `Adaptives_ReUse` ≈ `Refurbishment`. `Urban_Mining` is *sourcing*, `Design_for_Disassembly` is *future intent*, `Recycling`/`Remanufacturing` are *processing levels* — three conceptual axes squashed into one list.
10. **Barriers (`Huerde`) inflated by data-quality flags:** 1 022 `HAT_HUERDE` edges; #2 barrier is `Datenluecke` (133) — a data-quality meta-flag, not a domain barrier.
11. **No clear `Projekt` ↔ `Bauwerk` ownership model:** 4 overlapping connectors (`NUTZT_BAUWERK`, `LIEGT_IN_STADT/_LAND`, `Bauwerk.HAT_NUTZUNG/HAT_BAUOBJEKTROLLE/HAT_BAUOBJEKTKLASSE`).
12. **`Bauteilgruppe` reuse-direction is implicit and contradictory:** `AUS_BAUWERK`+`EINGEBAUT_IN` are both outgoing edges with identical property shapes. `counts_as_*` booleans overlap with `WiederverwendungsArt`.
13. **`Akteur` sprawl with no leverage:** 660 actors, **84 orphans**, **484 (73 %) connect to only one project**, max degree 11.
14. **Citation graph empty of metadata:** 370 `ZITIERT_QUELLE` edges; **0 %** carry `evidence` or `source`.
15. **Inference quality is scattered:** `needs_verification`, `inference_basis`, `not_confirmed_project_participation`, `association_basis`, `datenqualitaet` live on different relationships in different shapes — no single `Confidence`/`EvidenceGrade` schema.

### 2.4 Top 10 fixes ranked by impact

1. Make `Wiederverwendungskette` mandatory donor→receiver or delete it.
2. Promote a tiny canonical KPI block on `Bauteilgruppe` (`quantity_value`, `quantity_unit`, `quantity_basis`, `quantity_confidence`); backfill from 30+ ad-hoc `menge_*` fields.
3. Move project-specific counters off `Projekt` onto `Bauteilgruppe`.
4. Standardize one `Evidence` shape across every relationship — `evidence_excerpt`, `evidence_source_id`, `evidence_page`, `evidence_confidence`.
5. Split `Status` into `LifecycleStatus`/`MaturityClass`/`Permanence`.
6. Refactor `WiederverwendungsArt` into orthogonal facets: Treatment / Location / Sourcing / Designintent.
7. Kill the dual role system — keep typed `Akteurrolle` only.
8. Collapse year/area duplicates into single canonical fields.
9. Move `Datenluecke`/`Mengenunsicherheit`/`Zustand_Unklar` out of `Huerde` into a separate `DataGap`.
10. Add a `Projekt`-level rollup view computed from `Bauteilgruppe`, never re-entered by hand.

### 2.5 Five realistic user scenarios — final grades

| Scenario | Grade |
|---|---|
| A — Show all reused steel beams over 5 t and where they came from | **D** |
| B — Compare projects by reuse percentage | **F** |
| C — Which actors specialize in reuse refurbishment across multiple projects | **C-** |
| D — What barriers stopped reuse on similar component types | **C** |
| E — Show the full provenance of one reused element (document, page, author, inspection class) | **D-** |

### 2.6 Recommendation

**Restructure + enrich**, in that order. Do not "keep as is" and do not just rename. The taxonomy work is genuinely good — the labels show real domain thinking — but the graph is currently a *vocabulary in search of data*.

---

## 3. Layer 2 — Structural integrity, hidden duplication, cross-cutting consistency

Layer 2 used the same live database to find the **structural reasons** behind the layer-1 symptoms.

### 3.1 The evidence model is partly fake

`HAT_MARKTMODELL.source_excerpt` sampled identically as `"propagated from project HAT_DOMINANT_MARKTMODELL (project-wide sourcing)"` — these are **machine-generated propagation notes**, not citations. The small islands of "good evidence coverage" in the graph are bookkeeping artifacts. Real human-curated evidence coverage is **even lower** than layer 1 suggested.

### 3.2 One source explains a sixth of the entire citation graph — and it's not a source

`q_controlled_vocab_seed` is the single most-cited "source" with **457 `BELEGT_IN` edges (16.5 % of all 2 777 citations)**. It documents *the existence of the controlled vocabulary itself* — Aufbereitungsverfahren (45), Huerde (28), Akteurrolle (25), Material (24), PruefungNachweis (20), Bauteiltyp (16), Ressourcenquelle (16), etc. Plus `q_akteursliste_master_md` supplies 259 more edges (9.3 %). **Together these two infrastructure sources cover ~26 % of all citations.**

### 3.3 Half of the reuse chains are auto-generated stubs

- **49 of 112 chains (44 %)** are documented by `q_phase20_kette_autodiscovery` (`quelltyp='derived'`).
- **111 of 112 chains have `status = NULL`**.
- `distanz_km`, `transportdistanz_km`, `beschaffungsweg` are null on the overwhelming majority.

### 3.4 The real donor/receiver picture is finer-grained — and not modeled

Cross of donor × receiver × identical across 381 `Bauteilgruppen`:

| Pattern | Count | Share |
|---|---:|---:|
| Translocated (donor ≠ receiver) | 235 | 62 % |
| Same-site (donor = receiver) | 31 | 8 % |
| Only receiver known | 81 | 21 % |
| Only donor known | 6 | 2 % |
| Neither | 28 | 7 % |

All five cases share the same edge types. No `:Bestandserhalt`, `:Translokation`, `:SurplusSourcing` typing.

### 3.5 `Bauteilgruppe` is overloaded — half are bundles, not components

**51 % (189/369)** have two or more `Bauteiltyp` labels: Stuetze+Traeger (20), Fassade+Fenster (15), Fassade+Wand (14), Dach+Traeger (9), Ausbau+Technik (9), Decke+Stuetze+Traeger (5), 3-type bundles (42), 4-type bundles (3). The node label is doing double duty as both *one component class* and *a loose collection of reused stuff*.

### 3.6 The reuse-art taxonomy is silently used as a tag cloud

Multi-tag combinations observed: Direkte_Wiederverwendung + Refurbishment (14), + Upcycling (14), + Same_Site_ReUse (11), + Refurbishment + Urban_Mining (4), Design_for_Disassembly + Direkte_Wiederverwendung (4), Bestandserhalt + Adaptives_ReUse (3). The user community is empirically telling the schema that a single category list is the wrong shape.

### 3.7 The "evidence base" is one third research, two thirds bookkeeping

| `quelltyp` | Count | Share | What it is |
|---|---:|---:|---|
| `external_link_from_actor_registry` | 319 | 66 % | URLs scraped from the actor list |
| `case_markdown` | 96 | 20 % | Real case-study writeups |
| `external_reference` | 68 | 14 % | Properly cited literature |
| `controlled_vocab_seed` | 1 | <1 % | The 457-edge meta-source |
| `derived` | 1 | <1 % | The 49-chain autodiscovery source |
| `actor_registry_markdown` | 1 | <1 % | The 259-edge meta-source |

Genuine research-grade sources: ~164 (34 %).

### 3.8 Hidden duplicates remain after the merge campaign

| Pair | IDs |
|---|---|
| Bellastock (FR) | `bellastock` + `Bellastock` |
| baubüro in situ | `baubuero_in_situ` + `bauburo_in_situ` |
| PLP Architecture | `ak_plp_architecture` + `plp_architecture` |
| ZRS Architekten | `zrs_architekten` + `ZRS_Architekten_Ingenieure` |
| Löliger Strub | `loeliger_strub_architektur` + `loeliger_strub` |
| Bill Dunster / ZEDfactory | `zedfactory_bill_dunster` + `bill_dunster_zedfactory` |
| Opera | `opera_pm` + `opera` |

### 3.9 The actor-network graph is automated co-occurrence, not relationships

`VERBUNDEN_MIT_AKTEUR` (335 edges) carries `needs_verification=true` on **247 (74 %)**; only `inference_basis` values are `"shared 2 project(s)"`, `"shared 3 project(s)"`. `ASSOZIIERT_MIT_PROJEKT` (167 edges) is **100 % `needs_verification`** and **77 % `not_confirmed_project_participation`**.

### 3.10 Geographic data on actors is collapsed

660 actors → only **86 have a `land` property**; **370 actors have neither `Akteur.land` nor a `GEHÖRT_ZU` edge to `Land`**. Cross-country comparisons are impossible.

### 3.11 `name` is not what users think it is

Divergence between `name` and `name_full`: Wiederverwendungskette 112/112 (100 %), Bauteilgruppe 331/369 (90 %), Bauwerk 184/209 (88 %), Projekt 74/91 (81 %), Quelle 179/486 (37 %), Akteur 86/660 (13 %). `raw_name` adds a third variant on some labels.

### 3.12 Layer-2 verdict and three additional fixes

> A **curated ontology** (genuinely good taxonomic work), plus **~10 well-documented case studies** (Résilience, K.118, Lycée Michel Lucius, ELYS, Saxum, Brent Cross Town, House of Fraser), plus a much larger scaffolding layer of auto-discovered stubs, propagated boilerplate, actor-list URLs, controlled-vocab anchors, name-derived duplicate IDs, and unverified co-occurrence edges that *look like* knowledge but mostly are not.

11. Separate "ontology evidence" from "case evidence" — relabel `q_controlled_vocab_seed` and `q_akteursliste_master_md` out of `:Quelle` to `:OntologyAnchor`.
12. Promote `donor_resolution_status` from string to typed edge.
13. Stop deriving evidence values via propagation scripts; add explicit `evidence_origin: 'curated' | 'propagated' | 'derived'`.

---

## 4. Layer 3 — Granular dive: well-documented cases, unit/currency consistency, query-stress tests

Layer 3 probed the **content failures** the way a real analyst would.

### 4.1 `Bauwerk` is conceptually overloaded — not always a building

Same `AUS_BAUWERK` edge points to: Cleveland S&T stock (a steel stockholder), ROTOR (a company/dealer that also exists as `:Akteur`), Reuse-/Surplus-Liefernetzwerk (a logistics network), Aggregierte Pariser Quartiere (an aggregation of districts), Berlin donors (a vague plural placeholder), WBS70 donor building (a building type), Unbekanntes P2-Massenwohngebäude (placeholder), Unbekannte Donorquellen (×7 variants), Regionale Ölindustrie (an industry).

### 4.2 `BauwerkEra` is beautiful — and entirely disconnected from buildings

- `BauwerkEra` has **zero incoming edges** from `Bauwerk`. No `:BAUT_IN_ERA` relationship in the schema.
- **8 of 119 donor buildings (7 %)** have any year property.
- **0 donor buildings** have `date_dismantled`.
- **0 donor buildings** have `alte_nutzung`.
- The implicit risk query (any `Bauteilgruppe` matching a pollutant's typical material): **273 components match a known pollutant profile, but 0 carry `HAT_SCHADSTOFF` (only 7 edges exist total)**.

### 4.3 Project reuse-percent claims contradict component-level coverage

| Project | Stated reuse % | `Bauteilgruppen` | Component masses present |
|---|---:|---:|---:|
| 55 Great Suffolk Street | 97 % | 1 | 1 |
| Thoravej 29 Copenhagen | 95 % | 4 | **0** |
| Circular Centre Netherlands | 92 % | 3 | **0** |
| BlueCity Offices | 90 % | 4 | **0** |
| KA13 | 80 % | 5 | **0** |
| Résilience | **12.67 %** | 7 | **7** |

The projects making the highest reuse claims have the lowest component-level documentation.

### 4.4 The cost model is a currency-and-unit salad

`Projekt` carries 17 distinct cost fields, each filled in 1–3 rows, mixing **EUR / USD / GBP / CHF**, gross / net, total / per-m² / per-sqft, integer and *millions*. No `currency_iso` column, no conversion rates. The simplest query (sort by cost per m²) is mathematically impossible from this graph.

### 4.5 The "barriers" model is inflated by edge replication

**73 relationships across 19 different relationship types** carry the source annotation `"… (replicated from pre-split BG)"`. The graph silently double-counts: a `HAT_HUERDE` recorded once on a pre-split parent now appears on each split child.

### 4.6 `Bauwerk.bauwerkstatus` is a third orthogonal status system

- **194 of ~209 `Bauwerk` (93 %)** have `bauwerkstatus = NULL`.
- The 15 that have it use 5 different inline string values (`"realisiert"`, `"rueckgebaut"`, `"geplant"`, `"gebauter Prototyp"`, plus free-text variants like `"teilweise gelistet seit 2004"`).
- Mirrors `:Status` controlled vocab but stored as raw strings, even though `:Bauwerk` supports `HAT_STATUS`.

### 4.7 Aliases were the dedup tool — and were not used on actors

| Label | `aliases` filled |
|---|---:|
| Bauteilgruppe | 308 / 369 (83 %) |
| Akteur | **9 / 660 (1.4 %)** |

The dedup tool is being applied where it is least needed and skipped where it is most needed.

### 4.8 Norms/standards are taxonomic decoration, not active references

- **6 norms are explicitly flagged `not_yet_referenced_in_corpus = true`**: `DIN EN 15804`, `DIN EN 15978`, `ISO 14040`, `ISO 14044`, `ISO 20887`, `DIN 18940` (the LCA backbone).
- Top norm reaches only 5 `REFERENZIERT_NORM` edges; SIA 269 (central Swiss code) has 3.
- 12 norms have ≤ 2 references; 4 referenced norms have 0 referrers.

### 4.9 The flagship `K.118 Winterthur` case study is incomplete

- `name = "K.118 Winterthur"` (with period), `name_full = "K118 Kopfbau Halle 118 Winterthur"` (without). A naïve `name CONTAINS "K.118"` or `name CONTAINS "K118"` both fail.
- 5 `Bauteilgruppen` visible, **none carry mass, area, or piece counts**.
- Donor `Orion-Bürogebäude Zürich` exists as `:Bauwerk` but has **no `baujahr`** (real Orion building is 1970s — directly relevant for PCB era).
- `Status` field on the only sampled Bauteilgruppe is the string `"reuse"` — not a link to a `:Status` node, and `"reuse"` is not one of the 11 defined `Status` values.

### 4.10 Quelle `access_date` is meaningless

Only 39 of 486 sources have `access_date`, **and 37 of those 39 are `2026-05-19`** — uniform import-stamp, not freshness signal.

### 4.11 Tooling layer is decorative

`Tool` has 8 nodes; **5 of 8 have no `funktion`; 7 of 8 have no `software_basis`**. Only `HTS Reused Steel Stockmatcher` carries both.

### 4.12 Revised score after layer 3: 2.2 / 10

| Dimension | Layer 1 | Layer 2/3 | Why moved |
|---|---:|---:|---|
| Usability | 3.5 | **3.0** | Name-search traps even on flagship cases; `Bauwerk` overloaded |
| Semantic clarity | 4 | **3.0** | Three parallel status systems; donor edge means 4–5 different things |
| Queryability | 3 | **2.5** | Currency mixing; propagation-script evidence; replication double-counting |
| Trust / evidence | 2.5 | **1.5** | Meta-sources 26 % of citations; uniform access dates |
| Completeness | 2 | **1.5** | Donor era/year 7 %, demolition date 0 %, pollutant annotations 0 % |
| Decision value | 2 | **1.5** | High-reuse-claim projects have no underlying component data; cost incomparable; risk inference unwired |

### 4.13 Two two-edge fixes worth their weight

1. Wire **`BauwerkEra` → `Schadstoff` → `Material/Bauteiltyp`** via a `BAUT_IN_ERA` edge from `Bauwerk` to `BauwerkEra` + 119 donor-year backfills. Unlocks the single most valuable query the graph could answer.
2. Wire **`LebenszyklusModul` → `Norm` → `Projekt`** via the 6 unused LCA norms (EN 15804/15978, ISO 14040/14044/20887, DIN 18940) into projects' `lca_module_scope` + `BERECHNET_NACH_MODUL`.

---

## 5. Layer 4 — Source-corpus analysis (4 directories)

Layer 4 read four source areas systematically: 76 case-study markdowns in `_archive/research/gebaeude`, 14 batch-2 dossiers in `2026-05-20_inbox_batch2_import/raw_tree`, 13 thematic research files in `_neo4j/intake/inbox/research`, and the actor-registry seed in `2026-05-15_actor_registry_seed`.

### 5.1 The K.118 source contains everything the graph is missing

The flagship case `K118_Kopfbau_Halle_118_Winterthur.md` is **25 KB** of structured German tables in 13 sections. Side-by-side comparison:

| Fact in source | Source location | In graph? |
|---|---|---|
| **14 % reuse rate by weight** (cited [S6], "belegt") | §8 Kennwerte | **No** — `Projekt.reuse_anteil_prozent = NULL` |
| **41 % reuse rate by volume** (cited [S6], "belegt") | §8 | **No** — no volume-reuse field exists |
| **59 % CO₂ reduction, 494 t CO₂ absolute** ([S3][S7]) | §8 | **No** — 52 CO₂ fields on `Projekt`, none populated |
| **~500 t primary material saved** ([S3][S4]) | §8 | **No** |
| **80 t CO₂ from steel reuse / 16 % share** ([S3][S7]) | §8 | **No** |
| **1 100 m² area, 3 floors added** ([S2][S4]) | §3 | **No** — `flaeche_m2` empty |
| **Completion March 2021** ([S1][S2]) | §3 | **No** — `jahr_fertigstellung` empty |
| Donor "Orion-Bürogebäude Zürich" (22 m steel staircase, ~28 years old, hot-dip galvanized) | §5 | Partial — donor exists as `:Bauwerk` but `baujahr=NULL` |
| Donor "ELYS-Projekt Basel" | §3, §5 | Yes — but no baujahr, no alte_nutzung |
| **12 components catalogued with 17 attributes each** | §5 inventory | 5 `Bauteilgruppen`; 0 with quantities |
| **9 cited sources with URLs** | "Quellen und Links" footer | 1 `Quelle` with 23 `BELEGT_IN`; underlying URLs never split out |
| **12 process phases with akteure / methode / tool / abbruchmethode / aufbereitung / prüfung / logistik / hürde / lösung** | §6 | Phase taxonomy exists but no link to the 12 named phases |
| **5 named hurdles with category / cause / effect / solution / übertragbare Lehre** | §9 Hürden-Matrix | Generic `Huerde` attached, but cause/effect/transferable-lesson columns lost |
| **9 confidence grades** ("belegt"/"teilweise belegt"/"unklar") per row | Throughout | No per-row confidence field |
| **5 explicit open questions** | §13 | The source *knew* the gaps; the graph does not record them |

The K.118 source contains ~80 cited facts with confidence grades; the graph captures ~10. Lossy ratio ~8:1, and the *quantitatively valuable* facts (the four KPIs) are exactly the ones lost. Pattern is consistent across the 76 `gebaeude` files.

### 5.2 The curator's own coverage audit lists 22 changes that were never made

`_neo4j/intake/inbox/research/reuse_knowledge_graph_coverage_audit.md` (2026-05-16, 51 KB) contains 22 prioritised graph updates. Examples:

- P1.1 Merge Pavilion Circl Amsterdam + Circl/ABN AMRO → not merged.
- P2.6 Convert Reallabor B(e)Ware from Projekt to Forschung/Programm → still `:Projekt`.
- P2.7 Convert RE-USE Höfe to Programm → still `:Projekt`.
- P2.8 Merge FCRBE + Interreg NWE FCRBE into one Programm → imported as two separate dossiers.
- P3.11 Split `zirkular_cirkla` into two nodes → not done.
- P4.16 Drop or quarantine RCMI Concular, REFAIR Bordeaux, REBRIDGE, MedUni Mariannengasse, Careno Be.Circular → **the opposite happened**: batch 2 (2026-05-19, three days after the audit) imported RCMI_Concular.md, REFAIR_Bordeaux.md, MedUni_Campus_Mariannengasse_Wien.md as new dossiers.
- P5.19 Add `component_evidence_status` property → property does not exist anywhere.
- P5.20 Add `Schadstoff` coverage explicitly → only 7 `HAT_SCHADSTOFF` edges total.
- P5.21 Use distinct edge types for material passports (`has_material_passport`, `uses_madaster`, `uses_project_specific_passport_tool`, `passport_discussed_but_unverified`) → none exist.

**The audit is read-only documentation that the import pipeline ignored.**

### 5.3 The thematic research files are an unused conceptual gold mine

- `circular_construction_reuse_graph_gaps.md` (22 KB) defines **14 reusable graph classes** (`ReusableStructuralSteelMember`, `ReclaimedConcreteElement`, `ReclaimedHollowCoreSlab`, `ReclaimedStructuralTimber`, `ReclaimedNaturalStoneSlab`, `ReclaimedBrickBatch`, `EarthenMaterialReuse`, `MaterialPassport`, `ProductWasteStatus`, `ApplicableNorm`, `LegalCondition`, `TestProtocol`, `PollutantScreening`, `ProcessingMethod`) plus 12 relationship types and 20 country × material rows. **Zero of these classes exist in the graph.**
- `schadstoff_reuse_knowledge_graph_research.md` (15 KB) defines the explicit modelling rule: use `Material/Bauteilgruppe --hasRiskPollutant--> Schadstoff` and `Project --requiresVerificationFor--> Schadstoff`; **avoid** `Project --hasSchadstoff--> Schadstoff` unless project-source-documented. The cautious part was followed (only 7 `HAT_SCHADSTOFF` edges); the constructive part was not (no `hasRiskPollutant` or `requiresVerificationFor` edge types in the schema).
- `missing_underused_norm_nodes_reuse_kg.md` (27 KB) + `circular_construction_leistungsanforderungen.md` (26 KB) specify the LCA standards wiring (EN 15804, EN 15978, ISO 14040, ISO 14044, ISO 20887). Top norm has only 5 `REFERENZIERT_NORM` edges; LCA standards all flagged `not_yet_referenced_in_corpus = true`.
- `aufbereitungsverfahren_reused_building_elements.md` (47 KB) supplies the *why* and *test required* for each method; `HAT_AUFBEREITUNG` edges (426 edges, 86 % no-evidence) carry only names.
- `bauteilreuse_legal_regime_matrix.md` (46 KB) — the full national-legal-regime matrix produced **12 `HAT_RECHTLICHE_BEDINGUNG` graph edges**. Compression ratio effectively zero.

### 5.4 The actor-registry seed exposes the duplicate problem at its origin

`actor_registry_seed/.../actor_registry_first10/actors_first10.registry.kg.jsonl` contains **378 JSONL records for just 10 actors** (~37 records each). The README explicitly says: *"Person-to-project links use `ASSOZIIERT_MIT_PROJEKT` with `needs_verification: true`. `BETEILIGT_AN` is intentionally not used here."* Projects were created as side-effects of actor records with explicit `import_status: "registry_stub_only"` and `needs_project_file: true` flags — yet only 15 of 91 projects retain those flags, so the audit's "drop or upgrade" rule was never enforced. The duplicate problem (`baubuero_in_situ`/`bauburo_in_situ`, `bellastock`/`Bellastock`, etc.) lives in the registry import path because the `aliases` field exists in the JSONL schema but the actor-registry importer doesn't use it as a merge key.

### 5.5 Batch 2 (2026-05-19/20) shows the audit was overridden

Of 14 batch-2 dossiers, **at least 10 directly contradict prior audit recommendations**: Careno, MedUni, RCMI Concular, REFAIR Bordeaux, REBRIDGE imported despite P4-drop instruction; Pavilion Circl + Circl/ABN AMRO imported as separate dossiers despite P1-merge; FCRBE + Interreg NWE FCRBE imported as two; Reallabor B(e)Ware and RE-USE Höfe imported as `:Projekt` despite P2-convert-to-Programm.

### 5.6 The source-side dossier format is excellent — what is lost is in the loader

The batch-2 dossiers use a **markdown-table-per-node-type** format (e.g. `RCMI_Concular.md`) cleanly separating Akteur / Software / Tool / Geographic / People / Funding / Linked case studies / Relationships, with every field having a `value` and `source` column and a `[S1]…[S9]` citation per cell. The format would parse mechanically into a graph with proper provenance — but the loader never fully exploited the structure, so `evidence` text remains empty on 80–100 % of edges even when the source has `[S1]` per cell.

### 5.7 Layer-4 verdict — three failure layers visible only with source-side comparison

| Failure | Detail |
|---|---|
| **Import < Source** | Per-row confidence grade and `[S1]` citations exist in every case file; the loader flattened them. Project-level KPIs (14 % weight, 41 % volume, 494 t CO₂) and per-cell evidence excerpts were dropped. |
| **Research/Specification > Schema** | The thematic files specify 14 reusable graph classes, 12 relationship types, country-specific decision branches, and a complete risk-inference pattern. None are in the schema. |
| **Audit ≠ Import Pipeline** | 22-action coverage audit (2026-05-16) and batch 2 (2026-05-19/20) operated in parallel without integration. ≥10 of 14 batch-2 dossiers contradict prior audit recommendations. |

**One-sentence assessment:** *the graph is a stable, well-curated, conceptually serious project that is currently delivering ~15–20 % of the analytical value already present in its own source corpus, because the import pipeline is the weakest link in an otherwise mature research methodology.*

---

## 6. Two binding rules distilled from the data census

Every keep / remap / delete decision in the plan was re-checked against the live graph (plan §0b). Two binding rules emerged from the connection-count census:

### 6.1 Rule A — Remap before delete (entity-side)

A node is only eligible for hard delete if **both** are true:
1. Current degree ≤ 1 (truly isolated).
2. It is **not** the canonical anchor for any vocabulary, source, or programme.

If degree ≥ 2, the node is **remapped** (relabel, demote-to-property, or merge into a duplicate). The information stays; the label or shape changes.

**Where the earlier delete-heavy plan was wrong (verbatim from §0b):**

- 84 "orphan" Akteure → **only 6 deletable** (deg ≤ 1). The other 78 are wired through `HAT_AKTEURROLLE`, `HAT_AKTEURTYP`, `GEHÖRT_ZU`, `VERBUNDEN_MIT_AKTEUR` and `BELEGT_IN` with degrees 5–26 — typology backbone.
- 15 "registry-stub" projects → **only 5 lack `HAT_BAUTEILGRUPPE`**. Even those 5 have degrees 8–14 (Hürden, Aktören, Land/Stadt). All get `quality_tier='tier_3_stub'`.
- 22 Bauwerk placeholders → **relabel to `:Materialdepot`** (degrees 4–26 each, median ~10), do not delete.
- 98 unwired `Wiederverwendungskette` → **demote, do not delete**. Median degree 4. Deleting would strip ~400 edges; demoting moves the chain's payload (treatment / status / sourcing / Hürde) onto the BG itself.
- `Bauobjektklasse` (8 nodes, 235 edges), `Bauobjektrolle` (6 nodes, 236 edges), `Bauteilebene` (6 nodes, 378 edges) → **KEEP**; earlier plan calling them "redundant with `Nutzung`/`Bauteiltyp`" was wrong — they describe genuinely different axes.
- `Status` and `WiederverwendungsArt` → **property-add (`kind`/`facet`), not label-split**. Splitting would produce sub-labels with deg < 5 (e.g. `MaturityClass.Wettbewerb` deg 1).

### 6.2 Rule B — ≥ 5 connections per node for any new label

A new node label is only introduced if measurement of the existing graph shows it would carry **≥ 5 connections per node on average**. If the bar is not met, the concept is added as a property (string, enum, or list) on an existing label.

**New labels justified under Rule B:**

| Label | Live min degree | Verdict |
|---|---:|---|
| `OntologyAnchor` | 443 | PASS |
| `Materialdepot` | 4 (1 of 23 nodes) | soft PASS — 22 of 23 ≥ 5, accepted with §1.4 documentation |
| `ReuseRule` | 5 | PASS (tight; plan said ≥ 5) |

**New labels rejected under Rule B:**

- `LifecycleStatus` / `MaturityClass` split — `MaturityClass` median deg 4 → use `Status.kind` property.
- `Treatment` / `ReuseLocation` / `Sourcing` / `DesignIntent` split of `WiederverwendungsArt` — `ReuseLocation` (1 node, 28 edges), `DesignIntent` (2 nodes, 54 edges) fail Rule B → use `WiederverwendungsArt.facet` property.
- `CostEntry` sub-node per project — only ~10 of 91 projects have cost data; projected median deg ≤ 3 → use `Projekt.cost_facts` list-of-dict.
- `ReuseShare` sub-node — only 4 projects have `reuse_anteil_prozent` filled → use `Projekt.reuse_share_facts`.
- `LcaModule` / `AccountingStatus` from research file — projected median deg ≤ 3 → use `Projekt.lca_module_scope` enum.
- `KostenTreiber` — programme-level only, projected median deg ≤ 3 → use `Projekt.cost_facts[].drivers` string list.

---

## 7. The radical action plan — summary by phase

Every phase carries a done-flag, an idempotent Cypher migration in `migrations/`, and an agent report in `reports/`.

### 7.1 Phase 1 — Surgical pruning + bulk remap

| # | Goal | Migration | What changed (counts) |
|---|---|---|---|
| **1.1** | Demote unwired `Wiederverwendungskette` (Rule A) | `mig_1_1_demote_chains.cypher` | 98 chains DETACH-deleted after propagating `HAT_*` payload to BG; 14 fully-wired chains kept. Net `:Wiederverwendungskette` 112 → 14 |
| **1.2** | Relabel ontology anchors out of `:Quelle` | `mig_1_2_anchor_relabel.cypher` | `q_controlled_vocab_seed` (deg 457) + `q_akteursliste_master_md` (deg 259) relabelled `:OntologyAnchor`; 716 `BELEGT_IN` → `ANCHORED_BY` (live: 703); 21 deg-0 dossier `Quelle` deleted |
| **1.3** | Flag propagated MARKTMODELL bookkeeping | `mig_1_3_flag_propagated.cypher` | 319 propagated `HAT_MARKTMODELL` edges retagged `evidence_origin='derived'`, `evidence_basis='propagated'`, `evidence_confidence='bookkeeping'`; **dropped** 86 `HAT_DOMINANT_MARKTMODELL` + 24 `HAT_DOMINANT_AKZEPTANZ` |
| **1.4** | Relabel Bauwerk placeholders | `mig_1_4_materialdepot.cypher` | 23 placeholder Bauwerke (degs 4–26 — `stock`/`pool`/`aggregiert`/`liefer`/`unbekannt`/`donor`/`depot`/`lager`/`rotor` patterns) → `:Materialdepot`. Bauwerk 209 → 186 |
| **1.5** | Surgical orphan deletes (33 nodes) | `mig_1_5_surgical_deletes.cypher` | Akteur 660 → 654 (Δ −6 truly isolated), Programm 28 → 24 (Δ −4), Norm 36 → 34 (Δ −2), Quelle 486 → 465 (Δ −21). Journalled to `deleted/phase1_5_nodes.jsonl` |
| **1.6** | Actor dedup (7 merges) | `mig_1_6_actor_merge.cypher` | Merged: `baubuero_in_situ`, `plp_architecture`, `ZRS_Architekten`, `loeliger_strub`, `zedfactory_bill_dunster`, `opera`, plus case-normalised `Bellastock`. Akteur 654 → 647 immediately |

### 7.2 Phase 2 — Schema consolidation (property-first)

| # | Goal | Migration | What changed |
|---|---|---|---|
| **2.1** | `Status.kind` enum (lifecycle / maturity / unknown) instead of label split; merge duplicates | `mig_2_1_status_consolidation.cypher` | `Status = 9` nodes with `kind ∈ {lifecycle, maturity, unknown}`; `Realisiert+Gebaut` merged (398+185 edges), `Wettbewerb→Prototyp` |
| **2.2** | `WiederverwendungsArt.facet` (treatment / sourcing / location / intent) instead of 4-label split | `mig_2_2_wva_facet.cypher` | `WiederverwendungsArt = 11`, all with `facet` |
| **2.3** | Role unification — keep typed `Akteurrolle`, kill `BETEILIGT_AN.rolle_text` free text | `mig_2_3_role_unification.cypher` | `Bauobjektrolle` kept (236 edges); free-text role merged to `raw_role_evidence`; duplicate `ar_reuse_beratung`/`ar_reuse_zirkularitaetsberatung` collapsed |
| **2.4** | Projekt property collapse | `mig_2_4_projekt_collapse.cypher` | 13 year fields → `year_completed` (42/101 populated); 11 area fields → `area_m2_gross`; 10 cost/CO₂ → `cost_facts` / `co2_facts` list-of-dict; ~30 one-off counters moved to `Bauteilgruppe.menge_*`; archive bucket present |
| **2.5** | Label demotions (Layer / Lebenszyklus / Recht / Zert / Tool) | `mig_2_5_label_demotions.cypher` | `Layer=0`, `LebenszyklusModul=0`, `ZertifizierungBewertungssystem=0`, `Tool=0`, `Software=19` (Tool merged in) — repair C later closed the 15 residual `RechtlicheBedingung` nodes |
| **2.6** | Schema diff (documentation only) | — | Covered by 2.1–2.5 |
| **2.7** | Three-bucket property panel (panel / facts / _archive) | `mig_2_7_panel_cleanup.cypher` | `Projekt` 434 distinct keys → 18 panel + facts lists + `_archive` JSON; `Bauteilgruppe` 142 → 22 panel; 8 524 legacy `url`/`source` properties stripped from claim edges |

### 7.3 Phase 3 — Enrichment

| # | Goal | Migration | What changed |
|---|---|---|---|
| **3.1** | Wire `BauwerkEra` to `Bauwerk` via `BUILT_IN_ERA` + era_unknown flag | `mig_3_1_built_in_era.cypher` | `BUILT_IN_ERA = 8` edges (era inferred from `baujahr`); 178 of 186 Bauwerk carry `era_unknown=true` (honest flag — per-row dossier backfill not emitted by 4b loaders) |
| **3.2** | Pollutant risk inference (Material × Era → Schadstoff) | `mig_3_2_pollutant_inference.cypher` | `HAS_RISK_POLLUTANT = 803` edges (target ~800); `REQUIRES_VERIFICATION_FOR = 347` edges (target ~250); `HAT_SCHADSTOFF` replaced (now 0) |
| **3.3** | 20 `ReuseRule` nodes from `circular_construction_reuse_graph_gaps.md` | `mig_3_3_reuse_rules.cypher` | `ReuseRule = 20` (Rule-B min_deg = 5); `APPLIES_IN = 20`, `APPLIES_TO = 20`, `REFERENZIERT_NORM` (rule→norm) = 93; `Norm` 34 → 103 (69 LCA / SIA / DIN seeded) |

### 7.4 Phase 4 — Three-level evidence model

| # | Goal | Migration | What changed |
|---|---|---|---|
| **4.1** | Canonical 5-field evidence shape on every claim edge | `mig_4_1_canonical_evidence.cypher` | `{evidence_origin, evidence_basis, evidence_excerpt, evidence_source_id, evidence_confidence}` enforced; `evidence_origin IN {curated, inferred, derived}`; `evidence_confidence IN {belegt, teilweise_belegt, unklar, inferiert, bookkeeping}`. Repair D later promoted 254 `HAT_BAUTEILGRUPPE` to curated + fixed 1 682 curated-without-excerpt residuals |
| **4.2** | Rename donor/receiver topology | `mig_4_2_rename_donor_receiver.cypher` | `AUS_BAUWERK → FROM_DONOR` (286 edges); `EINGEBAUT_IN → INTO_RECEIVER` (349 edges) |

### 7.5 Phase 4c — Source-as-link enforcement

| # | Goal | Migration | What changed |
|---|---|---|---|
| **4c.1** | Unfold `Quelle.external_sources` array → `ZITIERT_QUELLE` link nodes | `mig_4c_1_external_sources_unfold.cypher` | 60 array entries unfolded; `:Quelle.external_sources IS NULL` for all post-migration |
| **4c.2** | Backfill case-markdown S-refs (handled in 4b.1) | — | 90 dossier S-refs wired |
| **4c.3** | Detach `Projekt→actor-registry-Quelle BELEGT_IN`; strip URL from edges | `mig_4c_3_detach_projekt_actor_registry_belegt.cypher` + `mig_4c_edge_strip.cypher` | 0 residual `Projekt→actor-registry BELEGT_IN`; 365 valid `Akteur→actor-url BELEGT_IN` retained; 0 edges carrying `url`/`http`/`source_file`/`external_sources` |

### 7.6 Phase 4b — Loader rewrite (the central data fix)

| # | Goal | Migration / loader | What changed |
|---|---|---|---|
| **4b.1** | Case-study dossier loader for 76 gebaeude + 14 batch2 dossiers (per 13-section template) | `logs/agent9_dossier_loader.py` | 5 157 `BELEGT_IN` total; 1 350 `BELEGT_IN`/`ASSOZIIERT_MIT_PROJEKT` promoted `'curated' + excerpt + belegt/teilweise_belegt`. Q1 fix later wired by Repair D |
| **4b.2** | Research-file ingestion (7 thematic .md files) | `logs/agent10_research_registry_loader.py` | 8 research-anchor Quelle nodes; 258 `domain_belegt_research_anchor` edges; 90 `project_research_inferred_edges` |
| **4b.3** | Actor-registry handling (629 registry nodes) | Same Agent-10 loader, second pass | 629 nodes merged, 2 555 relationships; 256 illegal `Projekt→actor-url` BELEGT_IN dropped; 277 master→actor-url `ZITIERT_QUELLE` linked |

### 7.7 Phase 5 — Quality tiering

| # | Goal | Migration | What changed |
|---|---|---|---|
| **5.1** | `Projekt.quality_tier` per §5.1 formula | `mig_5_1_quality_tier.cypher` | 101 / 101 projects tiered: tier_1=11, tier_2=68, tier_3=22; pre-fix for 15 `REFERENZIERT_NORM evidence_confidence='mittel'` → `teilweise_belegt` |
| **5.2** | Default tier filter on all entry-point queries | — (documented + tier-1 used in Q3/Q4) | Tier 1 = decision-grade default; Tier 2 opt-in; Tier 3 admin |
| **5.3** | Relabel 4 registry stubs `:Projekt → :Programm` | `mig_5_3_relabel_programme.cypher` | `p_reuse_logistics`, `p_vandkunsten_component_reuse`, `p_architecture_of_reuse_brussels`, `p_reuse_in_construction_zhaw` → `:Programm` with `migration_origin='5_3_relabel_to_programm'`, `original_label='Projekt'`. `p_circle_house` deliberately kept as `:Projekt` (later accepted as `tier_2_documentation_only` per Repair E) |

---

## 8. Execution waves — the 12-agent dispatch plan

The plan was executed by **12 background subagents** organised in **7 waves (wave 0 → wave 6)**, respecting the strict dependency order Phase 1 → 2 → 4 → 4c → 4b → 3 → 5.

| Wave | Agent | Responsibility | Done-flag |
|---|---|---|---|
| 0 | Agent 1 | Pre-migration snapshot of `mit-bestand` to JSONL + run-dir scaffold | `SNAPSHOT_DONE.flag` |
| 1 | Agent 2 | Phase 1.1 — demote 98 unwired Wiederverwendungsketten into BG `HAT_*` properties + audit JSONL | (covered in flags) |
| 1 | Agent 3 | Phase 1.2 ontology anchors + 1.3 propagated MARKTMODELL flag + drop `HAT_DOMINANT_*` | (covered in flags) |
| 1 | Agent 4 | Phase 1.4 Materialdepot relabel (23 Bauwerk) + 1.5 surgical deletes (33 nodes) + 1.6 Akteur merges | `PHASE_1_4_DONE`, `PHASE_1_5_DONE`, `PHASE_1_6_DONE` |
| 2 | Agent 5 | Phase 2.1 Status.kind + 2.2 WVA.facet + 2.3 role cleanup + 2.5 label demotions | (covered in flags) |
| 2 | Agent 6 | Phase 2.4 Projekt property collapse + 2.7 three-bucket panel cleanup on Projekt/BG/Bauwerk/Quelle/Akteur | `PHASE_2_4_DONE`, `PHASE_2_7_DONE` |
| 3 | Agent 7 | Phase 4 canonical 5-field evidence + 4.2 FROM_DONOR/INTO_RECEIVER rename | `PHASE_4_DONE`, `PHASE_4_2_DONE` |
| 3 | Agent 8 | Phase 4c.1 unfold 60 external_sources → ZITIERT_QUELLE + 4c.3 detach Projekt→registry BELEGT_IN + strip 8 524 legacy edge URL fields | `PHASE_4C_DONE` |
| 4 | Agent 9 | Phase 4b.1 parse 90 dossiers per 13-section template + 4c.2 backfill S-refs | `PHASE_4B_1_DONE` |
| 4 | Agent 10 | Phase 4b.2 ingest 7 inbox/research/*.md as Level-2 inferred + 4b.3 actor_registry JSONL rewiring | `PHASE_4B_2_DONE`, `PHASE_4B_3_DONE` |
| 5 | Agent 11 | Phase 3.1 BUILT_IN_ERA + 3.2 HAS_RISK_POLLUTANT inference + 3.3 20 ReuseRule nodes | `PHASE_3_1_DONE`, `PHASE_3_2_DONE`, `PHASE_3_3_DONE` |
| 6 | Agent 12 | Phase 5 quality_tier + 5.3 relabel 4 Programmes + run all 7 acceptance queries + `FINAL_PLAN_COMPLETION_AUDIT.md` | `PHASE_5_DONE` |

Wave gating: each wave was dispatched only after its predecessor wave completed. After Wave 6 surfaced the 5 residuals (one acceptance + four hard-rule), **5 repair agents (A–E)** ran sequentially as a remediation wave; **a post-repair verifier** then re-ran every failed Final-Verifier gate; **12 Pass-2 verifiers** then re-verified every section. All gates green.

---

## 9. Verification matrix — every phase, all three passes

Verdicts pulled from `final_verify_*.md` (Final Verifier 1–12 = pass 1), `repair_*.md` (5 repairs), `post_repair_verification.md` (re-run of failed gates), and `pass2_verify_*.md` (Pass-2 detailed verifiers 1–12).

| Phase | Pass-1 verdict | Repair done? | Pass-2 verdict | Residual notes |
|---|---|---|---|---|
| 1.1 demote chains | PASS | — | **PASS** | 14 wired chains preserved; 98 demoted edges traceable via `bg.demoted_from_kette` |
| 1.2 anchor relabel | FAIL (anchor regression: 202 `BELEGT_IN` to `:OntologyAnchor`, duplicate `:Quelle` shell) | **Repair A** (`mig_repair_1_2_anchor_regression.cypher`) | **PASS** | `ANCHORED_BY = 703`; `BELEGT_IN` to anchor ids = 0 |
| 1.3 propagated flag | PASS | — | **PASS** | 319 retagged; 86+24 dominant-* edges removed |
| 1.4 Materialdepot | PASS | — | **PASS** | 23 nodes, 1 with deg 4 (soft Rule-B PASS, accepted per §1.4) |
| 1.5 surgical deletes | FAIL (residuals: `norm_din_18940`, `Bellastock`, `bauburo_in_situ`) | **Repair B** (`mig_repair_1_5_1_6_residuals.cypher`) | **PASS** | 33 nodes journalled; case-insensitive dup pairs = 0 |
| 1.6 actor merge | FAIL (case-insensitive duplicates surviving) | **Repair B** (combined) | **PASS** | Akteur 648; canonical degrees `baubuero_in_situ`=24, `bellastock`=27 |
| 2.1 Status.kind | PASS | — | **PASS** | 9 Status nodes; kind ∈ {lifecycle, maturity, unknown} |
| 2.2 WVA.facet | PASS | — | **PASS** | 11 WiederverwendungsArt, all with facet |
| 2.3 role unification | PASS | — | **PASS** | Bauobjektrolle = 0; single role system on `Akteurrolle` |
| 2.4 Projekt collapse | PASS | — | **PASS** | 42/101 `year_completed`; `area_m2_gross` populated; archive bucket present |
| 2.5 label demotions | FAIL (`:RechtlicheBedingung` = 15 not demoted) | **Repair C** (`mig_repair_2_5_rechtliche_bedingung_demote.cypher`) | **PASS** | 15 records preserved as JSON list on `q_bauteilreuse_legal_regime_matrix_md`; `:RechtlicheBedingung = 0` |
| 2.7 panel cleanup | PARTIAL (Projekt distinct keys 30 > 25; max per-node 26 > 18) | **Repair E** (`mig_repair_2_7_5_1_quality_tier_panel.cypher`) | **PASS** | 9 `quality_tier_*` scalars folded into `quality_tier_facts` JSON-string; distinct keys 22; max-per-node 18 |
| 3.1 BuiltInEra | PASS (honest unknown-flagging) | — | **PASS** | `BUILT_IN_ERA = 8`; 178 era_unknown |
| 3.2 pollutant inference | PASS | — | **PASS** | `HAS_RISK_POLLUTANT = 799`; `REQUIRES_VERIFICATION_FOR = 347` |
| 3.3 ReuseRules | PASS | — | **PASS** | 20 wired both with `APPLIES_IN` and `APPLIES_TO`; `REFERENZIERT_NORM` (rule→norm) = 93 |
| 4.1 canonical evidence | FAIL (1 682 curated-without-excerpt; 22 list-typed enum violations; 243 `evidence_basis='research_file_row'` off-enum) | **Repair D** (`mig_repair_4_1_curated_excerpts_and_q1.cypher`) | **PASS** | All enum hygiene gates 0; 254 `HAT_BAUTEILGRUPPE` promoted curated |
| 4.2 donor/receiver rename | PASS | — | **PASS** | `AUS_BAUWERK=0`, `EINGEBAUT_IN=0`, `FROM_DONOR=286`, `INTO_RECEIVER=349` |
| 4c source-as-link | PASS | — | **PASS** | 0 `Quelle.external_sources`; 0 polluted edge keys; 0 `Projekt→actor-registry BELEGT_IN` |
| 4b.1 case-study loader | PARTIAL (Q1 blocked — `HAT_BAUTEILGRUPPE.evidence_origin` not promoted to curated) | **Repair D** (combined) | **PASS** | 254 promoted; Q1 = 266 rows |
| 4b.2 research loader | PASS | — | **PASS** | 8 anchor Quelle; 258 domain anchors; 90 project research-inferred edges |
| 4b.3 actor-registry | PASS | — | **PASS** | 629 nodes / 2 555 rels; 256 illegal Projekt→actor-url dropped; 277 master→actor-url `ZITIERT_QUELLE` linked |
| 5.1 quality_tier | PARTIAL (`p_circle_house` narrative-vs-formula gap; 9 audit scalars on panel) | **Repair E** (combined) | **PASS** | Tier dist 11/68/22; `quality_tier_facts` on 101; `p_circle_house` Tier 2 accepted per §5.1 formula |
| 5.2 default tier filter | PASS (documented) | — | **PASS** | Q3/Q4 use tier-1 filter live |
| 5.3 relabel 4 → Programm | PASS | — | **PASS** | 4 of 4 with `migration_origin='5_3_relabel_to_programm'`, `original_label='Projekt'`; `p_circle_house` deliberately kept as Projekt |
| 6 sequenced execution | PASS | — | **PASS** | Order 1 → 2 → 4 → 4c → 4b → 3 → 5 followed; every phase has flag + migration + report |

Final acceptance (Q1–Q7) status documented separately in §11 below.

---

## 10. Repairs performed — short narrative of the five repairs

Five named repair agents (A–E) ran sequentially between the initial Wave-6 audit (`FINAL_PLAN_COMPLETION_AUDIT.md`, 2026-05-20 ~22:48 UTC) and the Pass-2 audit (`FINAL_PASS2_AUDIT.md`, 2026-05-21 07:59 UTC). All repairs are idempotent migrations with their own done-flag, migration cypher, runner JSON, and report.

### 10.1 Repair A — Phase 1.2 anchor regression (`PHASE_1_2_REPAIR_DONE.flag`)

Final Verifier 2 found that 202 `BELEGT_IN` edges had regressed back to point at the `:OntologyAnchor` for `q_akteursliste_master_md`, plus a duplicate `:Quelle` shell with id `q_akteursliste_master_md` carried 202 duplicate incoming `BELEGT_IN` and 277 outgoing `ZITIERT_QUELLE`. The repair created/reused canonical `ANCHORED_BY` edges for the 202 regressed sources, dropped the duplicate `BELEGT_IN` edges, removed the duplicate shell, and preserved 319 actor-URL `ZITIERT_QUELLE` on the real anchor. Live result: `BELEGT_IN` to any `:OntologyAnchor` = 0; `ANCHORED_BY = 703`.

### 10.2 Repair B — Phase 1.5 / 1.6 norm + actor residuals (`PHASE_1_5_1_6_REPAIR_DONE.flag`)

Final Verifier 3 found three surviving non-canonical ids: `:Akteur {id:'bauburo_in_situ', deg=8}`, `:Akteur {id:'Bellastock', deg=18}`, and `:Norm {id:'norm_din_18940', deg=1}`. The repair merged `bauburo_in_situ` into `baubuero_in_situ` (canonical degree 24) and `Bellastock` into `bellastock` (degree 27), and remapped `norm_din_18940` into `norm_din_18940_family`. All 27 semantic relationships of the residuals preserved on the canonical replacements via `apoc.refactor.mergeNodes(... mergeRels:true)`. Live: Akteur 650 → 648; case-insensitive duplicate ordered pairs = 0.

### 10.3 Repair C — Phase 2.5 `:RechtlicheBedingung` demote (`PHASE_2_5_REPAIR_DONE.flag`)

Final Verifier 5 found 15 surviving `:RechtlicheBedingung` nodes (sourced from `q_bauteilreuse_legal_regime_matrix_md`) that had not been demoted. The repair preserved condition IDs/names on the connected `:Quelle` node as `legal_conditions`, `legal_condition_ids`, and `demoted_legal_condition_records` (JSON-string list), plus `legal_condition_evidence_*` parallel arrays for provenance. Live: `RechtlicheBedingung = 0`; `legal_conditions` count on the source = 15.

### 10.4 Repair D — Phase 4.1 curated excerpts + Q1 promotion (`PHASE_4_1_Q1_REPAIR_DONE.flag`)

Final Verifier 10 found 1 682 `evidence_origin='curated'` edges with `evidence_excerpt IS NULL`, plus Final Verifier 12 found Acceptance Q1 returning 0 rows (the topology was already intact with 254 Bauteilgruppen carrying both `FROM_DONOR` and `INTO_RECEIVER`, but `(p:Projekt)-[r:HAT_BAUTEILGRUPPE]->(bg)` was never promoted to curated). The repair ran 7 classification rules:

- **A** — Registry-sourced curated edges filled with truthful synthetic excerpts naming graph-native identities: `HAT_AKTEURROLLE` (542), `HAT_AKTEURTYP` (190), `LIEGT_IN_LAND` (201), `VERBUNDEN_MIT_AKTEUR` (283), `ASSOZIIERT_MIT_PROJEKT` (150 = 139 Projekt + 11 Programm).
- **B** — Actor S-ref `BELEGT_IN` filled with Akteur identity + cited URL (314 edges).
- **C** — `BUILT_IN_ERA` year_inferred (8 edges): demoted curated → inferred.
- **D** — `REQUIRES_VERIFICATION_FOR` project_rollup (5 edges): demoted curated → inferred.
- **E** — `HAT_BAUTEILGRUPPE` promotion: 254 edges set `evidence_origin='curated', evidence_basis='cell_citation', evidence_confidence='teilweise_belegt'` with `evidence_excerpt` naming Projekt + BG id + donor/receiver degrees + alphabetically-first case-markdown anchor.
- **F** — Unpacked 22 dedup-merged array properties from Phase 1.6 (canonical pick order curated > inferred > derived; belegt > teilweise_belegt > inferiert > unklar > bookkeeping).
- **G** — Remapped 243 `BELEGT_IN` with `evidence_basis='research_file_row'` → `'cell_citation'`.

Live: curated-without-excerpt = 0; Q1 = 266 rows; `HAT_BAUTEILGRUPPE` curated = 254.

### 10.5 Repair E — Phase 2.7 panel + Phase 5.1 tier residuals (`PHASE_2_7_5_1_REPAIR_DONE.flag`)

Final Verifiers 6/12 found `:Projekt` distinct keys = 30 (> 25 target) and max per-node keys = 26 (> 18 target); 9 audit scalars (`quality_tier_computed_by`, `quality_tier_has_components`, `..._has_evidence`, `..._has_land`, `..._has_metric`, `..._has_year`, `quality_tier_n_bg`, `..._n_bg_quantified`, `..._n_curated_evidence`) were panel-visible on every node. The repair folded them into a single `quality_tier_facts` JSON-string property (round-trippable with `apoc.convert.fromJsonMap`), removed the 9 scalars, and kept `quality_tier` itself directly visible. After: distinct keys = 22, max per-node = 18, sample 5 nodes = [14, 13, 13, 15, 13], all 101 Projekt carry `quality_tier_facts`, 0 carry any of the 9 legacy scalars.

The second residual (`p_circle_house.quality_tier='tier_2_documentation_only'` vs plan §5.3 narrative expectation of `tier_3_stub`) was **documented, not changed**: the §5.1 formula deterministically returns Tier 2 (`has_year=false, has_land=true, has_components=false, has_metric=true, has_evidence=false` → truthy_count = 2 of 5 → Tier 2). The plan §5.3 narrative is a documentation expectation, not an override; forcing Tier 3 would create a single special case with no formula provenance and erase the live Land+metric signal. The full sub-criterion bag is preserved inside `quality_tier_facts` for audit.

---

## 11. End-state numbers (post-repair, live `mit-bestand`)

### 11.1 Headline aggregates

| Metric | Value | Source |
|---|---:|---|
| Total nodes | **3 802** | `FINAL_PASS2_AUDIT` §1 |
| Total relationships | **25 023** | `FINAL_PASS2_AUDIT` §1 |
| Non-empty node labels | **51** (4 empty registered: `GraphVersion`, `RechtlicheBedingung`, `Tool`, `ZertifizierungBewertungssystem`) | `pass2_verify_phase5_acceptance` §4.1 |
| Non-empty relationship types | **64** (6 empty registered: `AUS_BAUWERK`, `EINGEBAUT_IN`, `HAT_RECHTLICHE_BEDINGUNG`, `HAT_SCHADSTOFF`, `HAT_ZERTIFIZIERUNG`, `NUTZT_TOOL`) | `pass2_verify_phase5_acceptance` §4.1 |
| `:Projekt` total | **101** | live |
| `:Programm` total | **28** (24 baseline + 4 relabel) | live |
| `:Akteur` total | **648** | live |
| `:Bauteilgruppe` total | **369** | live |
| `:Bauwerk` total | **186** | live |
| `:Materialdepot` total | **23** | live |
| `:Wiederverwendungskette` total | **14** | live |
| `:OntologyAnchor` total | **2** | live |
| `:ReuseRule` total | **20** | live |
| `:Norm` total | **103** | live |
| `:Quelle` total | **1 586** | live |

### 11.2 Tier distribution (plan §5.1 deterministic formula)

| Tier | Count | Cohort |
|---|---:|---|
| `tier_1_decision_grade` | **11** | year+land+≥3 BG+quantified BG OR reuse_share_facts+≥3 curated `BELEGT_IN` |
| `tier_2_documentation_only` | **68** | 2–4 sub-criteria met |
| `tier_3_stub` | **22** | ≤ 1 sub-criterion met |

### 11.3 Acceptance Q1–Q7 row counts (live, 2026-05-21 07:59 UTC)

| Query | Result | Verdict |
|---|---|---|
| Q1 — Reuse Story (canonical Bauwerk→BG→Bauwerk with curated `HAT_BAUTEILGRUPPE`) | **266** rows (197 strict Bauwerk→Bauwerk; 266 permissive any-label as Repair D writes) | **PASS** |
| Q2 — Risk Story | **799** `HAS_RISK_POLLUTANT` (792 inferred/inferiert + 7 derived/unklar) + **347** `REQUIRES_VERIFICATION_FOR` | **PASS** (threshold 700) |
| Q3 — Comparison (tier-1 `reuse_share_facts`) | **4** entries across **3** projects (`p_ferme_du_rail_paris`, `p_holbein_gardens_london`, `p_jeugdkliniek_ithaka_emergis_kloetinge`) | **PASS** |
| Q4 — Actor Network (tier-1 actors ≥ 2 tier-1 projects via `BETEILIGT_AN`) | **1** actor: `rotordc` / RotorDC × {p_chiro_d_itterbeek_dilbeek, p_maison_vignette_auderghem} | **PASS** |
| Q5 — Decision Support (20 ReuseRules wired) | **20 / 20** with both `APPLIES_IN` and `APPLIES_TO` | **PASS** |
| Q6 — Trust Check origin distribution | aggregate `curated=3 188, derived=2 948, inferred=347`; tier-1 only `1 461 / 418 / 59`; `p_chiro_d_itterbeek_dilbeek` `166 / 42 / 7` | **PASS** (all 3 origins live at 3 scopes) |
| Q7 — Source Drill-down (case_markdown → ZITIERT_QUELLE) | **958** rows; 13 distinct external Quellen reachable from `p_chiro_d_itterbeek_dilbeek` via `BELEGT_IN`→`ZITIERT_QUELLE`; grand total `ZITIERT_QUELLE = 1 470` | **PASS** |

### 11.4 Top relationship-type inventory (descending)

| Type | Count | Type | Count |
|---|---:|---|---:|
| `BELEGT_IN` | 4 734 | `ZITIERT_QUELLE` | 1 470 |
| `HAT_AKTEURROLLE` | 1 180 | `HAT_HUERDE` | 1 068 |
| `HAT_PROZESSPHASE` | 812 | `HAS_RISK_POLLUTANT` | 803 |
| `ANCHORED_BY` | 703 | `HAT_STATUS` | 672 |
| `HAT_AKTEURTYP` | 658 | `HAT_WIEDERVERWENDUNGSART` | 621 |
| `HAT_BAUTEILTYP` | 607 | `HAT_METHODE` | 602 |
| `BETEILIGT_AN` | 576 | `HAT_RESSOURCENQUELLE` | 567 |
| `HAT_LEISTUNGSANFORDERUNG` | 561 | `LIEGT_IN_LAND` | 520 |
| `HAT_MATERIALGRUPPE` | 516 | `HAT_LOGISTIK` | 500 |
| `NUTZT_MATERIAL` | 475 | `HAT_AUFBEREITUNG` | 448 |
| `HAT_PRUEFUNG` | 410 | `HAT_MARKTMODELL` | 384 |
| `HAT_BAUTEILEBENE` | 372 | `HAT_BAUTEILGRUPPE` | 369 |
| `INTO_RECEIVER` | 349 | `REQUIRES_VERIFICATION_FOR` | 347 |
| `VERBUNDEN_MIT_AKTEUR` | 337 | `HAT_RUECKBAUVERFAHREN` | 301 |
| `HAT_FUNKTIONSWECHSEL` | 299 | `FROM_DONOR` | 286 |
| `REFERENZIERT_NORM` | 145 | `APPLIES_IN` | 20 |
| `APPLIES_TO` | 20 | `TYPISCH_BEI_ERA` | 15 |
| `TEIL_VON_KETTE` | 14 | `BUILT_IN_ERA` | 8 |

(Full inventory in `pass2_verify_phase5_acceptance.md` §4.3.)

### 11.5 Evidence shape distribution (Q6 origins)

| `evidence_origin` | Count (all 101 Projekt scope) |
|---|---:|
| `curated` | **3 188** |
| `derived` | **2 948** |
| `inferred` | **347** |

All three origins live at three scopes (aggregate, tier-1 only, per-project) — tri-state evidence taxonomy intact.

---

## 12. Open residuals & follow-ups (non-blocking)

- **`Akteur.source_file` panel residual on `werner_sobek_p`** — minor panel-cleanup leftover that did not regress acceptance; documented in `pass2_verify_phase2_4_7.md`.
- **`dominant_mm_rederivability` gap on `p_elementa_walkeweg`** — documented in `pass2_verify_phase1_3.md`; the dominant-marktmodell-from-HAT_MARKTMODELL re-derivation rule has a single-project edge case that does not block acceptance.
- **`p_circle_house` tier-2-vs-narrative-tier-3** — formally accepted Tier 2 per the §5.1 formula; the `quality_tier_facts` JSON carries the full sub-criterion bag (`has_year=false, has_land=true, has_components=false, has_metric=true, has_evidence=false`). Documented in `repair_phase2_7_5_1_panel_tier.md` §2.
- **4 empty-registered node labels** (`GraphVersion`, `RechtlicheBedingung`, `Tool`, `ZertifizierungBewertungssystem`) and **6 empty-registered relationship types** (`AUS_BAUWERK`, `EINGEBAUT_IN`, `HAT_RECHTLICHE_BEDINGUNG`, `HAT_SCHADSTOFF`, `HAT_ZERTIFIZIERUNG`, `NUTZT_TOOL`) — expected schema leftovers from plan-mandated renames / demotions.
- **Total node / relationship overshoot vs plan projection** — +54.6 % nodes, +31 % rels, concentrated in `:Quelle` (1 586 vs ~750–900 projected) and `:Norm` (103 vs ~64 projected); both intentional by-products of the Phase 4b loader.
- **Q4 conservatively bounded** by the tier-1 cohort of 11 projects → 1 actor (RotorDC). The plan policy is correct (tier-1 = decision-grade only); lifting to tier-1+2 yields 49 actors at c ≥ 2.
- **Per-row `BauwerkEra` backfill not applied** — Phase 3.1.c envisaged a per-row era assignment driven by the dossier loaders, but the loaders did not emit the per-row signal. 178 of 186 Bauwerk carry `era_unknown=true` (honest flag).
- **`HAT_BAUTEILGRUPPE` curated confidence is `teilweise_belegt`** — promotion is topology-backed (donor/receiver edges present) plus dossier-anchor presence, not verbatim Section-5 cell parse. Recorded in `repair_phase4_1_q1.md` §6.
- **Recommended CI gate:** `MATCH ()-[r]->() WHERE r.evidence_origin='curated' AND r.evidence_excerpt IS NULL RETURN count(r)=0;`

---

## 13. Artifact index — everything needed to audit the work

### 13.1 Top-level run-dir reports

```text
_neo4j/intake/runs/2026-05-20_radical_quality_reset/
├── FINAL_PASS2_AUDIT.md                                  (top-level Pass-2 audit)
├── PHASE_1_2_REPAIR_DONE.flag
├── PHASE_1_4_DONE.flag
├── PHASE_1_5_1_6_REPAIR_DONE.flag
├── PHASE_1_5_DONE.flag
├── PHASE_1_6_DONE.flag
├── PHASE_2_4_DONE.flag
├── PHASE_2_5_REPAIR_DONE.flag
├── PHASE_2_7_5_1_REPAIR_DONE.flag
├── PHASE_2_7_DONE.flag
├── PHASE_3_1_DONE.flag
├── PHASE_3_2_DONE.flag
├── PHASE_3_3_DONE.flag
├── PHASE_4B_1_DONE.flag
├── PHASE_4B_2_DONE.flag
├── PHASE_4B_3_DONE.flag
├── PHASE_4C_DONE.flag
├── PHASE_4_1_Q1_REPAIR_DONE.flag
├── PHASE_4_2_DONE.flag
├── PHASE_4_DONE.flag
├── PHASE_5_DONE.flag
├── POST_REPAIR_VERIFY_DONE.flag
└── SNAPSHOT_DONE.flag
```

### 13.2 Agent reports (12 agents × Wave 0–6)

```text
reports/
├── agent_1_snapshot_report.md
├── agent_2_phase1_1_report.md
├── agent_3_phase1_2_3_report.md
├── agent_4_phase1_4_5_6_report.md
├── agent_5_phase2_report.md
├── agent_6_phase2_4_7_report.md
├── agent_7_phase4_report.md
├── agent_8_dossier_manifest.json
├── agent_8_phase4c_report.md
├── agent_9_phase4b1_report.md
├── agent_10_phase4b_report.md
├── agent_11_phase3_report.md
└── agent_12_phase5_report.md
```

### 13.3 Verification reports — three passes

```text
reports/
├── FINAL_PLAN_COMPLETION_AUDIT.md           (Wave-6 audit by Agent 12, pre-repair)
├── final_verify_phase1_1.md
├── final_verify_phase1_2_3.md
├── final_verify_phase1_4_5_6.md
├── final_verify_phase2_1_2.md
├── final_verify_phase2_3_5.md
├── final_verify_phase2_4_7.md
├── final_verify_phase3_1.md
├── final_verify_phase3_2.md
├── final_verify_phase3_3.md
├── final_verify_phase4_4c.md
├── final_verify_phase4b.md
├── final_verify_phase5_acceptance.md
├── post_repair_verification.md              (re-run of all failed gates after Repairs A–E)
├── pass2_verify_phase1_1.md
├── pass2_verify_phase1_2.md
├── pass2_verify_phase1_3.md
├── pass2_verify_phase1_4.md
├── pass2_verify_phase1_5_1_6.md
├── pass2_verify_phase2_1_to_5.md
├── pass2_verify_phase2_4_7.md
├── pass2_verify_phase3.md
├── pass2_verify_phase4_1_2.md
├── pass2_verify_phase4b.md
├── pass2_verify_phase4c.md
└── pass2_verify_phase5_acceptance.md
```

### 13.4 Repair reports

```text
reports/
├── repair_phase1_2_anchor_regression.md      (Repair A)
├── repair_phase1_5_1_6_residuals.md          (Repair B)
├── repair_phase2_5_rechtliche_bedingung.md   (Repair C)
├── repair_phase4_1_q1.md                     (Repair D)
└── repair_phase2_7_5_1_panel_tier.md         (Repair E)
```

### 13.5 Migration cypher files (all idempotent)

```text
migrations/
├── mig_1_1_demote_chains.cypher
├── mig_1_2_anchor_relabel.cypher
├── mig_1_3_flag_propagated.cypher
├── mig_1_4_materialdepot.cypher
├── mig_1_5_surgical_deletes.cypher
├── mig_1_6_actor_merge.cypher
├── mig_2_1_status_consolidation.cypher
├── mig_2_2_wva_facet.cypher
├── mig_2_3_role_unification.cypher
├── mig_2_4_projekt_collapse.cypher
├── mig_2_5_label_demotions.cypher
├── mig_2_7_panel_cleanup.cypher
├── mig_3_1_built_in_era.cypher
├── mig_3_2_pollutant_inference.cypher
├── mig_3_3_reuse_rules.cypher
├── mig_4_1_canonical_evidence.cypher
├── mig_4_2_rename_donor_receiver.cypher
├── mig_4c_1_external_sources_unfold.cypher
├── mig_4c_3_detach_projekt_actor_registry_belegt.cypher
├── mig_4c_edge_strip.cypher
├── mig_5_1_quality_tier.cypher
├── mig_5_3_relabel_programme.cypher
├── mig_repair_1_2_anchor_regression.cypher
├── mig_repair_1_5_1_6_residuals.cypher
├── mig_repair_2_5_rechtliche_bedingung_demote.cypher
├── mig_repair_2_7_5_1_quality_tier_panel.cypher
└── mig_repair_4_1_curated_excerpts_and_q1.cypher
```

### 13.6 Reversibility ledger

```text
deleted/phase1_5_nodes.jsonl             (33 deleted nodes journalled per Rule A)
deleted/phase1_6_merges.jsonl            (7 actor merges journalled)
deleted/repair_phase1_5_1_6_residuals.jsonl  (Repair B audit)
deleted/repair_phase2_5_rechtliche_bedingung_demoted.jsonl  (Repair C audit)
snapshot/                                (pre-Phase-1 mit-bestand snapshot)
```

### 13.7 Verification scripts and live JSON dumps

```text
logs/
├── post_repair_verify.py / .json
├── post_repair_q1_probe.py
├── pass2_verify_phase5_acceptance.py / .json
├── pass2_q4_actor_list.py / .json
├── repair_d_runner.py / .json / .jsonl / _verify.json / _probe[0-7].json / _progress.log
├── repair_2_7_5_1_probe.py / .json
├── repair_2_7_5_1_runner.py / .log / _before.json / _after.json
├── repair_2_7_5_1_verify.py / .json
├── agent9_dossier_loader.py            (Phase 4b.1 case-study loader)
└── agent10_research_registry_loader.py (Phase 4b.2 / 4b.3 loader)
```

---

*End of synthesis report. Generated 2026-05-21 from the live `mit-bestand` graph and the on-disk run-dir artefacts. No graph writes performed by this document.*
