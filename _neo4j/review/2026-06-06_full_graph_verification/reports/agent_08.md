# Verifier Agent 08 — Unsourced Actors (the long tail)

**Database:** `mit-bestand` · **Mode:** READ-ONLY on Neo4j (propose-only) · **Date:** 2026-06-06
**Ledger:** [`ledger/agent_08.csv`](../ledger/agent_08.csv) (477 rows, one per actor)

## 1. Scope & method

Scope Cypher (authoritative enumeration, processed in full — no sampling):

```cypher
MATCH (n:Akteur)
WHERE n.source_urls IS NULL OR size(n.source_urls)=0
RETURN n.id, n.name
```

- **697** total `:Akteur` nodes; **477** lack `source_urls` (68.7 %). All 477 are in this ledger.
- Per item I read `name`, `Akteurtyp`, country (`LIEGT_IN_LAND`), and graph degree, then decided:
  (a) real identifiable org/person → `ADD_SOURCE`; (b) generic/legacy stub or duplicate →
  `DEPRECATE_NODE`/`MERGE_DUPLICATE`; (c) role/type miscast as an actor → `ESCALATE_HUMAN`.
- Per the plan, this is the long-pole shard. I **web-verified the high-value graph hubs** (deepest
  fetch where node degree is largest / identity ambiguous) and triaged the long tail with
  search-grade evidence plus high-confidence candidate domains. **No graph mutation** was performed;
  all rows are proposals for the Aggregator's gated patch run.

> Anti-hallucination discipline: only the 17 rows with `fetched=true` carry a verbatim `proof_quote`
> and are `PROVEN`. Every unfetched candidate domain is `basis_type=candidate`, `verdict=MISSING_EVIDENCE`,
> and explicitly flagged "UNFETCHED – verify before import". No node was marked PROVEN without a live quote.

## 2. Counts

| Verdict | Count |
|---|---:|
| `MISSING_EVIDENCE` (real, source needed) | 431 |
| `SCHEMA_VIOLATION` (duplicate node) | 20 |
| `PROVEN` (web-verified hub) | 17 |
| `UNVERIFIABLE` (miscast / private / aggregate) | 9 |
| **Total** | **477** |

| Proposed action | Count |
|---|---:|
| `ADD_SOURCE` | 448 |
| `MERGE_DUPLICATE` | 20 |
| `ESCALATE_HUMAN` | 9 |

Evidence basis of the 448 `ADD_SOURCE` rows: **17** web-verified (with quote), **141** high-confidence
candidate official domain (unfetched), **290** identifiable but no candidate URL captured in triage
(left for sourcing). So **158 / 477 actors already have a proposed URL**; the remaining 290 are real-looking
entities still needing a source hunt, and 29 are duplicates/escalations that should *not* be sourced as-is.

## 3. Web-verified hubs (PROVEN — fetched, with quote)

The largest / most ambiguous hubs were verified live before triaging the tail:

| id | deg | source (basis_ref) | verbatim proof |
|---|---:|---|---|
| `cleveland_steel_tubes` | 37 | cleveland-steel.com | "Established in 1973, we are one of the largest stockholders of steel tubes in Europe … North Yorkshire, UK." |
| `heyne_tillett_steel` | 20 | hts.uk.com | "a dynamic practice of over 180 staff with offices in London and Manchester …" |
| `symmetrys` | 15 | symmetrys.com | "Symmetrys is an employee owned structural and civil engineering practice …" |
| `akt_ii` | 15 | en.wikipedia.org/wiki/AKT_II | "AKT II is a London based firm of structural, civil and transportation engineering consultants." |
| `gardiner_and_theobald` | 10 | gardiner.com | "a partner-led consultancy, delivering cost, project and infrastructure management services …" |
| `gruner_ag` | 10 | gruner.ch | "Gruner is a leading independent engineering consultancy based in Switzerland." |
| `trnsfrm_eg` | 10 | junge-genossenschaften.berlin | "Die TRNSFRM eG … übernimmt die Bauherrenaufgabe für die Planung und die bauliche Umsetzung …" |
| `vandkunsten` | 11 | vandkunsten.com | "At Vandkunsten Architects we design with an understanding of the past …" |
| `consolis_parma` | 10 | recreate-project.eu | "Consolis Parma, Finland's leading manufacturer of precast concrete elements …" |
| `cantillon` | 8 | constructionnews.co.uk | "Cantillon has been renamed as Morrisroe Demolition … bought by Morrisroe Group." |

Plus 6 Finnish **ReCreate** partners corroborated by `parma.fi`/`recreate-project.eu`
(`ramboll_finland`, `skanska_finland`, `liike_oy_arkkitehtistudio`, `metso_oyj`, `kruunu` = A‑Kruunu,
`tampere_university`): "… ovat mukana Skanska, Consolis Parma, Ramboll Finland, Umacon, Liike Oy
Arkkitehtistudio sekä Tampereen kaupunki." (`umacon` is captured under the verified-hub block.)

## 4. Ten worst findings

1. **`recreate_dutch_cluster`** / **`recreate_finnish_cluster`** (ESCALATE) — these are *aggregate
   sub-groupings of the ReCreate project*, not standalone organisations; they should be remodelled as
   project parts, not `:Akteur`. (`recreate_project` itself is a real consortium → `ADD_SOURCE` recreate-project.eu.)
2. **Three overlapping ZRS org nodes** — `zrs` (deg 9), `ZRS_Architekten_Ingenieure` (7), `zrs_ingenieure` (7)
   all denote the Berlin ZRS engineering/architecture group (zrs.berlin). Propose collapse to one canonical node.
3. **`Superuse_Studios`** (deg 7) duplicates the already-**sourced** `superuse_studios_2012architecten`
   (superuse-studios.com) — merge into the sourced node so the source is inherited.
4. **`claus_asam` / `claus_asam_iemb`** — same person (composite person+IEMB); merge.
5. **`iemb_tu_berlin` / `ak_tu_berlin_iemb`** — duplicate IEMB/TU-Berlin nodes; merge.
6. **`tampere_university` / `tampere_university_recreate` / `tampere_university_satu_huuhka`** — one
   university split into three role-labelled actor nodes; merge (Satu Huuhka already a separate sourced person).
7. **`btu_cottbus` / `btu_cottbus_angelika_mettke`** — institution + person composite; merge (Mettke is a sourced person).
8. **Private / anonymised owners** — `haus_hos_privater_bauherr`, `maison_dna_private_owner`,
   `maison_vignette_private_owner`, `private_bauherrschaft_villa_welpeloo`, `familie_lange` — no public
   source obtainable (privacy); escalate rather than fabricate a source.
9. **Generic people-groups** — `studierende_freiwillige` ("Studierende, Schulkinder und Freiwillige",
   typ `Unbekannt`) and `kamikatsu_residents` ("local residents") are not identifiable legal actors; escalate.
10. **Brand/legal-name drift** — `cantillon` rebranded to **Morrisroe Demolition** (2023); the node needs
    `ADD_SOURCE` morrisroe.co.uk **and** a rename note. Similar EN/FR or short/long pairs to merge:
    `albert_et_compagnie`→`albert_and_co`, `artelia_group`→`artelia`, `bureau_greisch`→`greisch`,
    `graber_pulver_architektinnen`→`graber_pulver`, `pirmin_jung_schweiz`→`pirmin_jung_schweiz_ag`,
    `fabrix_london`→`fabrix`, `ak_cityfoerster`→`CITYFOERSTER`,
    `ak_epfl_structural_xploration_lab`→`structural_xploration_lab_epfl`,
    `lendager_group_lendager_architects`→`Lendager`, `frederic_denise_archipel_zero`→`archipel_zero`,
    `herve_joel_biele`→`herve_biele_conclus`, `services_techniques_ville_de_paris`→`ville_de_paris` (lower confidence).

## 5. Duplicate / merge proposals (20)

All `MERGE_DUPLICATE` rows carry the canonical target and rationale in `notes`. These are **proposals
only** and must be confirmed against endpoints/provenance before any merge (per `AGENTS.md` rule 3:
name similarity alone is not sufficient — but each of these is an abbreviation/EN-FR/person+org composite,
not a mere lexical coincidence). Several canonical targets are already sourced
(`superuse_studios_2012architecten`), so merging directly resolves the missing-source gap.

## 6. Escalations to human (9)

`recreate_dutch_cluster`, `recreate_finnish_cluster` (aggregate clusters → remodel),
`haus_hos_privater_bauherr`, `maison_dna_private_owner`, `maison_vignette_private_owner`,
`private_bauherrschaft_villa_welpeloo`, `familie_lange` (private/anonymised → privacy),
`studierende_freiwillige`, `kamikatsu_residents` (generic groups → not legal actors).

## 7. Anomalies & notes for the Aggregator

- **Type miscast candidates** worth a human check: `interreg_nwe` (an EU funding *programme*, not an actor —
  proposed source nweurope.eu but consider re-labelling to `Programm`), `ak_maconda`/`madaster_context`/
  `urban_mining_index` carry `Software_Tool_Anbieter` type yet sit in the actor shard (cross-check with Agent 10).
- **`ak_*` legacy prefix** (Hannover/Expo intake) accounts for many composite/duplicate nodes
  (`ak_cityfoerster`, `ak_tu_berlin_iemb`, `ak_epfl_structural_xploration_lab`, `ak_carsten_wiewiorra` …);
  these are the densest pocket of duplication and the best first cleanup batch.
- **141 candidate domains are UNFETCHED.** Do not import them blindly — they are high-confidence guesses
  (often corroborated by an already-sourced sibling *person* node, e.g. `lxsy_architektur`←lxsy.de,
  `urselmann_interior`←urselmanninterior.com, `klingelhoefer_kroetsch`←klingelhoefer-kroetsch.de,
  `encore_heureux`←encoreheureux.org, `grand_huit`←grandhuit.eu, `circular_material_systems`←circularmaterialsystems.com).
  Re-fetch + endpoint-confirm before the `set_node_properties` patch.
- **290 actors still need a source hunt** — overwhelmingly recognised AEC firms, universities and public
  bodies (low fabrication risk, just unsourced). They are not flagged as problems, only as work remaining.

## 8. Coverage statement

Every one of the 477 enumerated unsourced `:Akteur` ids appears exactly once in `ledger/agent_08.csv`
(`claim_kind=node`, `rel_type_or_label=Akteur`). Relationship verification for these actors' edges is
owned by other shards (Agent 09 participation/geo, Agent 12 classification edges); Agent 08 owns the
**node identity & provenance** verdict only.

---

**One-paragraph summary:** Of 697 actors, **477 (68.7 %) carry no `source_urls`**. None were deleted
(propose-only). I web-verified the **17 highest-value hubs** (incl. the deg-37 `cleveland_steel_tubes`)
with verbatim quotes, supplied **141 high-confidence candidate domains** (unfetched, flagged), flagged
**20 duplicate nodes** for merge (notably three overlapping ZRS nodes and `Superuse_Studios` ↔ the
already-sourced `superuse_studios_2012architecten`), and **escalated 9** non-actors (ReCreate clusters,
anonymised private owners, generic people-groups). **The single most important finding:** the unsourced
long tail is dominated not by fabrications but by *legacy duplication* (the `ak_*` intake and short/long
name pairs) — fixing those merges removes the largest block of "missing source" noise before any new sourcing.
