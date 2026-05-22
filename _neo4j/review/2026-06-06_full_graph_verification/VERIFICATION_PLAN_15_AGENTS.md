# Full-Graph Verification — 15-Agent Proof Campaign

**Status:** PLAN (ready to execute)
**Date:** 2026-06-06
**Database:** `mit-bestand`
**Graph snapshot at planning time:** **2 304 nodes / 15 457 relationships / 54 active labels / 50 active relationship types**
**Trigger:** The evidence audit (`_neo4j/review/2026-06-06_cross_bubble_extension/EVIDENCE_AUDIT.md`) found **29 fabricated relationships** — links built from category similarity with `evidence_url`s that did not name both endpoints. We will now prove **every** node and **every** relationship in the graph, or flag it.

**Evidence-location audit (2026-06-06):** [`EVIDENCE_URL_LOCATION_AUDIT.md`](EVIDENCE_URL_LOCATION_AUDIT.md) — the graph uses **two** relationship evidence shapes (`source_url` vs `evidence_url`); off-graph recovery ledgers are listed there.

---

## 0. Definition of "prove"

A claim is **PROVEN** only when an agent has produced, in writing, the *specific basis* for it:

- **External claim** (anything carrying `evidence_url` **or** `source_url` on relationships; `primary_source_url` / `source_urls` / singleton `source_url` on nodes): the agent fetched the URL, recorded the **HTTP status**, and quoted a **verbatim snippet** from the live page that supports the *exact* assertion. For a relationship, the snippet must reference **both endpoints** (or be the directory/imprint of one endpoint that explicitly lists the other). For a node, the snippet must establish the entity's existence and the cited attributes.
- **Internal/structural claim** (taxonomy, process, schema): the agent verified it against the **ontology contract**, the **source dossier** in `intake/inbox/…`, and **logical-consistency rules** (no contradictions, valid vocabulary target, valid endpoints, no orphan). "Plausible" is **not** proven.

Anything not provable is assigned a non-PROVEN verdict (see §3) and routed to remediation. **No verdict may be "SUPPORTED" without a fetched snippet or an explicit dossier/contract citation.**

---

## 1. Hard constraints (read these first)

1. **Agents are READ-ONLY on Neo4j.** Verifier agents may call only `read-cypher` (+ `get-schema`) and `WebFetch`/`WebSearch`, and may write only their own report files under this folder. **No agent may run `write-cypher`, mutate the graph, or apply a patch.** All mutations happen later, once, through the existing gated tool `_scripts/apply_neo4j_review_patch.py` (dry-run → human `--confirm` → apply), driven by the Aggregator's remediation set.
2. **Evidence lives on graph properties** (per `AGENTS.md`): reuse-bubble rels use `evidence_url`/`evidence_quote`/`evidence_confidence`; regulation/process rels use `source_url`/`source_quote`/`confidence`; nodes use `primary_source_url` and/or `source_urls`. Agents must **not** invent sidecar nodes or `BELEGT_IN`/`q_url_*` artifacts. Off-graph ledgers (`finalest.evidence.json`, trace logs, sidecars) are **recovery references only** — not proof until re-fetched and bound to a graph claim.
3. **MECE coverage is mandatory.** Every node id and every relationship id is owned by **exactly one** verifier agent (Agents 01–13). Agent 14 is a deliberate *global* meta-layer (overlap allowed). The Aggregator (15) must prove 100 % coverage with zero gaps before the campaign is accepted.
4. **Anti-hallucination for the verifiers themselves** (§3.3) — the irony is the point: a verification campaign that hallucinates is worse than none.
5. **Determinism:** every agent enumerates its work-set with the exact Cypher in its spec and processes the full enumerated list — no sampling unless the spec says so.

---

## 2. The three verification tiers

| Tier | What | Volume | Method | Risk |
|---|---|---|---|---|
| **A — Web evidence** | Rels with `evidence_url` (72, reuse bubbles) **+** rels with `source_url` (3,691, regulation/process) **+** nodes with `source_urls`/`primary_source_url` (544/54) | large, high-stakes | Fetch URL, confirm claim, quote verbatim; bubble actor edges need both endpoints | **HIGHEST** for bubble actor edges; regulation layer is volume-heavy but mostly law-to-requirement |
| **B — Entity & provenance** | Sourced + unsourced entities (Akteur 697, Bauwerk 184, Projekt 83, Materialdepot 22, Software 20, Programm 31, law nodes ~190) and their factual links (BETEILIGT_AN, AUS_SPENDER, GESTUETZT_AUF_REGELWERK, GILT_IN_LAND, geo) | medium | Existence + attribute proof; dossier trace; geo cross-check | HIGH — unsourced actors & zero-source Materialdepot are red flags |
| **C — Ontology & structure** | Taxonomic classification edges, process/requirement edges, schema, hygiene | ~13 600 edges + vocab nodes | Contract conformance, vocabulary validity, logic, hygiene scans | MEDIUM — mechanical but must be exhaustive |

Coverage observed at planning time (corrected 2026-06-06):

- Relationships with `evidence_url` only: **72** (`review_run`-tagged reuse bubbles: swiss 21, rotor_dc 19, germany 13, cross_bubble_extension 12, france 6, netherlands 1).
- Relationships with `source_url`: **3,691** (mainly `ERFORDERT_NACHWEIS` 1578, `TRIGGERS_REGULIERUNGSFRAGE` 1130, `GILT_IN_LAND` 281, `HAT_HUERDE` 237, `GESTUETZT_AUF_REGELWERK` 167, …).
- Relationships with either URL field: **3,763** (no rel carries both).
- Nodes with `source_urls`: **544**; `primary_source_url`: **54**; singleton `source_url`: **13**; `source_titles`: **1,001** (titles, not proof).
- Off-graph recovery queues: `needs_source_url_review.csv` (353 rels), `strict_candidate_source_url_review.jsonl` (3,693 demoted candidate sets — **do not auto-trust**).

---

## 3. The Evidence Gate (shared protocol for every agent)

### 3.1 Per-item procedure
For each work item (a node or a relationship):

1. **Read the claim** from the graph (endpoints, type, all properties).
2. **Locate the basis:**
   - external → take rel `evidence_url` or `source_url`; node `source_urls` / `primary_source_url` / `source_url`;
   - internal → take the relevant dossier path (`intake/inbox/<run>/…`) and the ontology contract (`_neo4j/contracts/`).
3. **Test it:**
   - external → `WebFetch` the URL. If timeout, retry once; if still unreachable, try `WebSearch` for a cached/alternate copy. Record final HTTP/fetch status.
   - confirm the page contains support for the **specific** claim. For relationships, the support must connect **both endpoints**; mere co-listing in a directory counts **only** if that directory is one endpoint's own curated listing of the other.
4. **Quote** the exact supporting sentence(s) (`proof_quote`, verbatim, ≤ 300 chars).
5. **Assign a verdict** (§3.2) and a **proposed action** (§3.4).
6. **Append one row** to the agent's ledger shard (§5.1).

### 3.2 Verdict taxonomy
- `PROVEN` — live source (or contract+dossier) explicitly supports the exact claim, both endpoints named.
- `PARTIAL` — source supports a weaker/narrower version (e.g. co-membership but not the asserted partnership). Must be relabeled/downgraded.
- `UNSUPPORTED` — source does not support the claim (page doesn't name an endpoint; category inference). **Delete or re-source.**
- `DEAD_LINK` — URL returns 4xx/5xx or is gone. Re-source required.
- `UNVERIFIABLE` — paywalled/login/robot-blocked; could not be confirmed either way. **Never counts as PROVEN.**
- `MISSING_EVIDENCE` — claim that *should* carry a source has none.
- `CONTRADICTION` — claim conflicts with another graph claim or the contract.
- `SCHEMA_VIOLATION` — forbidden property, illegal label/type, orphan, duplicate, deprecated wiring.

### 3.3 Anti-hallucination rules for verifiers
- A `PROVEN`/`PARTIAL` verdict **requires** a non-empty `proof_quote` copied from fetched content (external) or an exact dossier line + contract clause (internal). No quote ⇒ cannot be PROVEN.
- Never infer a relationship from "both are the same kind of thing", shared sector, shared country, or co-appearance in a list that neither party curates. That is the exact failure mode being remediated.
- Record `fetched: true/false` and `http_status`. If `fetched:false`, max verdict is `UNVERIFIABLE`/`DEAD_LINK`.
- Do not edit the graph. Do not propose merges based on name similarity (`AGENTS.md` rule 3).

### 3.4 Proposed-action vocabulary (consumed by the Aggregator)
`KEEP` · `DELETE` · `RESOURCE` (find a correct URL) · `RELABEL` (downgrade `connection_kind`/confidence) · `ADD_SOURCE` · `MERGE_DUPLICATE` · `DEPRECATE_NODE` · `FIX_PROPERTY` · `ESCALATE_HUMAN`.

---

## 4. The 15-agent fleet

> Each agent's **Scope Cypher** is the authoritative enumeration of its work-set. Counts are planning-time estimates.

### Band 1 — Tier A web-evidence (regional shards) — Agents 01–07

**Agent 01 — Switzerland reuse cluster**
- **Mission:** prove every CH actor/platform node and every `swiss_reuse_bubble` relationship.
- **Scope (rels):** `MATCH (a)-[r]->(b) WHERE r.review_run='swiss_reuse_bubble_2026_06_05' RETURN r` (21) **plus** all `VERBUNDEN_MIT_AKTEUR` where both endpoints are CH (cirkla, useagain, sumami, materiuum, salza, reuzi, gruner_reuse_platform, baubuero_in_situ, zirkular, bauteilladen_winterthur, wick, bauteilboerse_basel_overall, circular_hub_zurich, c33…).
- **Scope (nodes):** those CH `Akteur`/`Software`/`Materialdepot` nodes + their `source_urls`.
- **Method:** Evidence Gate on every `evidence_url`; for each node, confirm `source_urls[0]` establishes the entity. Re-check the Cirkla directory listings (each must be cirkla.ch's own `/annuaire/experts/<x>` page actually showing `<x>`).
- **Est. items:** ~40.

**Agent 02 — Belgium / Rotor cluster**
- **Scope:** `review_run='rotor_dc_reuse_bubble_2026_06_05'` (19) + Rotor/RotorDC/Opalis/Brussels Environment/Immobel/Whitewood actor-actor edges + their nodes (Rotor, rotordc, opalis, brussels_environment, immobel, whitewood…).
- **Special checks:** `colocation_evere`, `project_commissioner` on the OXY project (confirm rotordb.org names Immobel + Whitewood); Opalis funder/maintenance edges against opalis.eu/about.
- **Est. items:** ~30.

**Agent 03 — Germany cluster**
- **Scope:** `review_run='germany_reuse_bubble_2026_06_05'` (13) + Concular/restado/bauteilbörsen/HdM/Material-Mafia/Kunst-Stoffe/Circular-Berlin/TU-Berlin/Madaster-DE edges + nodes.
- **Special checks:** Concular↔restado brand fact (restado imprint); bauteilnetz peer page lists both Bremen & Hannover; HdM consortium edges against hausdermaterialisierung.org / tu.berlin HdM page.
- **Est. items:** ~30.

**Agent 04 — France cluster**
- **Scope:** `review_run='france_reuse_bubble_2026_06_05'` (6) + Bellastock/Cycle Up/Backacia/Mineka/Opalis-FR/RéaVie/Mobius/CSTB edges + nodes.
- **Special checks:** every Opalis `supplier_listing` must be that dealer's own `opalis.eu/fr/fournisseurs/<x>` page; SPIROU consortium (CSTB↔Mobius) against cstb.fr; REPAR (Bellastock↔CSTB/ADEME).
- **Est. items:** ~25.

**Agent 05 — Netherlands cluster**
- **Scope:** `review_run='netherlands_reuse_bubble_2026_06_05'` (1) + Madaster/Insert/New Horizon/Repurpose/Superuse/Madaster-EPEA/Utrecht nodes & surviving edges.
- **Special checks:** confirm the surviving `oogstkaart_lineage` (Superuse→New Horizon) snippet on superuse-studios.com; Insert↔Madaster partnership; Madaster↔EPEA. **Confirm none of the deleted mesh edges resurrect.**
- **Est. items:** ~20.

**Agent 06 — Cross-border / pan-European edges (HIGHEST SCRUTINY)**
- **Mission:** re-verify **every** relationship whose two endpoints belong to *different* country clusters — the exact class where all fabrications occurred — even ones that survived earlier passes.
- **Scope:** `MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)` where the inferred country of `a` ≠ country of `b`, OR `r.review_run='cross_bubble_extension_2026_06_06'`.
- **Method:** strict Evidence Gate; additionally assert the surviving set contains **no** `*_peer`, `*_mesh`, `*_ecosystem`, `european_*` `connection_kind` (those were purged — flag any reappearance as regression).
- **Est. items:** ~15.

**Agent 07 — Regulation/process `source_url` relationships**
- **Scope:** every relationship with `source_url` and **no** `review_run` (the 3,691 regulation/process edges). Primary types: `ERFORDERT_NACHWEIS`, `TRIGGERS_REGULIERUNGSFRAGE`, `GILT_IN_LAND`, `HAT_HUERDE`, `GESTUETZT_AUF_REGELWERK`, `ERFUELLT_NACHWEIS`, `HAT_SCHADSTOFFRISIKO`, `ERFORDERT_SCHADSTOFFPRUEFUNG`, `TYPISCH_BEI_*`.
- **Method:** Evidence Gate on `source_url`+`source_quote`; for law→requirement edges, verify the cited page supports the **specific** legal instrument and requirement (not merely the topic). Cross-check against typed law node `source_url`/`source_quote` where present. Flag dead links; reconcile with `2026-05-23_trace_zitiert_quelle_to_urls` trusted ledgers only as a recovery hint, never as auto-PROVEN.
- **Est. items:** ~3,691 (batch by reltype; dedupe URLs across rels).

### Band 2 — Tier B entity & provenance — Agents 08–11

**Agent 08 — Unsourced actors (the long tail)**
- **Mission:** every `Akteur` lacking `source_urls` (~477 of 697).
- **Scope:** `MATCH (n:Akteur) WHERE n.source_urls IS NULL OR size(n.source_urls)=0 RETURN n.id`.
- **Method:** for each, decide: (a) is it a real, identifiable organisation? `WebSearch` for an official site; if found → `ADD_SOURCE`. (b) Is it a generic/legacy stub or duplicate? → `DEPRECATE_NODE`/`MERGE_DUPLICATE`. (c) Is it actually a role/type miscast as an actor? → `ESCALATE_HUMAN`.
- **Output emphasis:** ranked list of unverifiable actors; do **not** delete — propose only.
- **Est. items:** ~477 (largest shard; mostly `WebSearch`, batched).

**Agent 09 — Places, buildings, projects & participation**
- **Mission:** prove the physical/temporal spine.
- **Scope (nodes):** `Bauwerk` (184), `Projekt` (83), `Stadt` (74), `Land` (15).
- **Scope (rels):** `BETEILIGT_AN` (599), `AUS_SPENDER` (245), `IN_EMPFANGSOBJEKT` (278), `HAT_BAUWERK` (194), `NUTZT_BAUWERK` (1), `LIEGT_IN_LAND` (651), `LIEGT_IN_STADT` (252).
- **Method:** cross-check against the already-extracted geo files (`_neo4j/review/2026-06-06_project_bg_geo_extract/donor_bauwerke_addresses.json`, `reuse_geo_graph.json`, `akteur_typ_projekt_geo.json`): every Bauwerk address resolves to its `Stadt`/`Land`; every donor→project (`AUS_SPENDER`/`IN_EMPFANGSOBJEKT`) is internally consistent; `BETEILIGT_AN` (actor↔project) is corroborated by the project's source where one exists. Flag geo contradictions (city not in stated country, etc.).
- **Est. items:** ~2 220 edges + 356 nodes (consistency checks, selective web).

**Agent 10 — Platforms, depots, programmes, software**
- **Mission:** `Software` (20), `Tool` (1), `Materialdepot` (22, **0 sources** — top red flag), `Programm` (31).
- **Scope:** these nodes + `NUTZT_SOFTWARE` (54), `TEIL_VON_PROGRAMM` (35), `BETRIEBEN_VON` (9), `ERHALT_FOERDERUNG_DURCH` (3).
- **Method:** confirm each platform/tool/depot/programme is a real, named entity with a findable source; every `Materialdepot` must get `ADD_SOURCE` or `ESCALATE_HUMAN` (none has one today). Verify `BETRIEBEN_VON` operator facts against the operator's site.
- **Est. items:** ~74 nodes + ~100 edges.

**Agent 11 — Regulation / legal layer (nodes + structural edges)**
- **Mission:** every typed law node exists and its structural applicability edges are coherent. **URL fetching for `source_url` rels is Agent 07's job** — Agent 11 checks node identity, label taxonomy, and edge logic only.
- **Scope (nodes):** all typed `*recht` labels + `ReuseRule` (20).
- **Scope (rels):** `GESTUETZT_AUF_REGELWERK` (167), `GILT_IN_LAND` (281) — structural/country checks; defer live URL proof to Agent 07 ledger merge.
- **Method:** confirm each instrument is a **real** law/standard/regulation; confirm `GILT_IN_LAND` country attribution is correct. Cross-check `FINAL_AUDIT_REPORT.md` / `VARIANT_B_TAXONOMY.md`.
- **Est. items:** ~165 nodes + 448 edges (structural; web proof merged from Agent 07).

### Band 3 — Tier C ontology & structure — Agents 12–14

**Agent 12 — Controlled-vocabulary & classification integrity**
- **Mission:** every taxonomic classification edge points to a valid, non-duplicate vocabulary node.
- **Scope (rels):** `HAT_AKTEURROLLE` (1493), `HAT_BAUTEILTYP` (871), `HAT_AKTEURTYP` (700), `NUTZT_MATERIAL` (633), `HAT_MATERIALGRUPPE` (403), `HAT_BAUTEILGRUPPE` (364), `HAT_KENNWERT` (255), `HAT_NUTZUNG` (235), `HAT_BAUOBJEKTROLLE` (225), `HAT_BAUWEISE` (124), `HAT_VERBINDUNGSTECHNIK` (110), `HAT_GESCHAEFTSMODELL` (98), `HAT_ENTWURFSMETHODIK` (79), `HAT_ARCHITEKTURERGEBNIS` (79), `HAT_BAUSYSTEM` (61), `HAT_DEFEKT` (57), `HAT_ZUSTANDSKLASSE` (18), `TYPISCH_BEI_MATERIAL` (74), `TYPISCH_BEI_ERA` (15), `TYPISCH_BEI_BAUTEILTYP` (10), `GEBAUT_IN_ERA` (8).
- **Scope (nodes):** all vocabulary labels (Bauteilgruppe, Bauteiltyp, Material, Materialgruppe, Kennwert, Akteurrolle, Akteurtyp, Nutzung, Bauobjektrolle, Bauweise, Bausystem, Verbindungstechnik, Geschaeftsmodell, Entwurfsmethodik, Architekturergebnis, Defekt, ZustandsKlasse, BauwerkEra, Schadstoff, …).
- **Method:** (no web) check every edge's target is in the legal vocabulary for that edge type (contract in `_neo4j/contracts/`); detect near-duplicate vocab nodes (case/spelling) → `MERGE_DUPLICATE`; detect classification edges to free-text/orphan nodes; verify domain/range (e.g. only `Akteur` may have `HAT_AKTEURROLLE`).
- **Est. items:** ~6 900 edges + ~600 nodes (programmatic).

**Agent 13 — Process & requirement logic integrity**
- **Mission:** the reuse-process and compliance graph is logically coherent.
- **Scope (rels):** `ERFORDERT_NACHWEIS` (1578), `TRIGGERS_REGULIERUNGSFRAGE` (1130), `HAT_PROZESSPHASE` (679), `HAT_BESCHAFFUNGSWEG` (592), `HAT_LOGISTIK` (434), `HAT_RUECKBAUVERFAHREN` (308), `HAT_ERGEBNIS` (294), `HAT_AUFBEREITUNG` (267), `HAT_RESSOURCENQUELLE` (264), `HAT_METHODE` (244), `HAT_HUERDE` (237), `HAT_INTERVENTION` (144), `ERFUELLT_NACHWEIS` (118), `HAT_SCHADSTOFFRISIKO` (100), `ERFORDERT_SCHADSTOFFPRUEFUNG` (37), `IST_UNTERVERFAHREN_VON` (9).
- **Scope (nodes):** `PruefungNachweis` (118), `Nachweisforderung` (27), `Leistungsanforderung` (8), `Regulierungsfrage` (11), process vocab.
- **Method:** logic rules — every `Nachweisforderung` reached by `ERFORDERT_NACHWEIS` should be satisfiable by some `ERFUELLT_NACHWEIS`/`PruefungNachweis`; no `TRIGGERS_REGULIERUNGSFRAGE` to a non-`Regulierungsfrage`; `IST_UNTERVERFAHREN_VON` forms a DAG (no cycles); phase/method assignments are domain-valid. Flag dangling requirements & contradictions.
- **Est. items:** ~6 900 edges + ~165 nodes.

**Agent 14 — Global hygiene & schema conformance (meta-layer)**
- **Mission:** graph-wide invariants, independent of the per-shard work.
- **Checks (whole graph):**
  1. **Orphans:** nodes with no relationships (esp. non-vocab).
  2. **Duplicates:** nodes sharing normalized `id`/name; parallel edges (same type+endpoints); bidirectional `VERBUNDEN_MIT_AKTEUR` pairs (the earlier dedup must hold).
  3. **DEPRECATED (16):** must not be wired into active subgraphs; confirm isolation.
  4. **Forbidden properties** (per `AGENTS.md`): no `BELEGT_IN`, `q_url_*`, `evidence_source_id`, `archive_source_id`, `evidence_claim_ids`; `metadata_sidecar_key` only within legacy cleanup scope.
  5. **Property-key schema:** node keys ⊆ approved 57; rel keys ⊆ approved 22 (`CLEANUP_APPLY_SUMMARY.md`).
  6. **ID & label legality:** every node has a unique `id`; labels ⊆ 54 active; rel types ⊆ 50 active.
  7. **Evidence schema:** every `review_run` rel has `evidence_url`+`evidence_confidence`; every `source_url` rel has `source_quote` or `confidence`; no rel has both URL fields; confidence values valid.
  8. **Recovery backlog:** emit counts for rels in `needs_source_url_review.csv` still lacking `source_url`/`evidence_url` on graph.
- **Method:** pure Cypher scans; emit a violations ledger.
- **Est. items:** ~15 invariant queries over the full graph.

### Band 4 — Adjudication — Agent 15

**Agent 15 — Aggregator & Adjudicator (runs last)**
- **Inputs:** the 14 ledger shards.
- **Tasks:**
  1. **Coverage proof:** union all processed node-ids and rel-ids; assert it equals the full graph (2 304 nodes / 15 457 rels). List any gaps → re-dispatch.
  2. **Merge & dedupe** findings; reconcile overlaps (Agent 14 vs shard verdicts).
  3. **Rank by severity:** `UNSUPPORTED`/`CONTRADICTION`/`SCHEMA_VIOLATION` > `DEAD_LINK`/`MISSING_EVIDENCE` > `PARTIAL`/`UNVERIFIABLE`.
  4. **Emit the master `VERIFICATION_LEDGER.csv`** (one row per claim) and **`REMEDIATION_PLAN.md`**.
  5. **Generate remediation patches** (`*.patch.jsonl`) grouped by action: `delete_rel`, `set_rel_properties` (relabel/downgrade), `set_node_properties` (add source), node deprecation — **for human dry-run/approval only**, exactly like the audit's `unsupported_edges_removal.patch.jsonl`.
  6. **Write `CAMPAIGN_REPORT.md`**: counts by verdict, "where mistakes happened" heatmap by `review_run`/relationship-type/country, and the residual unverifiable set.

---

## 5. Output artifacts (uniform, machine-mergeable)

### 5.1 Per-agent ledger shard — `ledger/agent_<NN>.csv`
Columns (see `VERIFICATION_LEDGER.schema.csv`):
`claim_id, claim_kind(node|rel), element_id, from_id, to_id, rel_type/label, asserted_claim, basis_type(web|dossier|contract|logic), basis_ref(url/path), fetched(bool), http_status, verdict, confidence, proof_quote, proposed_action, agent_id, notes`

### 5.2 Per-agent narrative — `reports/agent_<NN>.md`
Scope recap, counts by verdict, the 10 worst findings with quotes, anomalies, and any items escalated to human.

### 5.3 Aggregator outputs
`VERIFICATION_LEDGER.csv` · `REMEDIATION_PLAN.md` · `CAMPAIGN_REPORT.md` · `patches/*.patch.jsonl` · `COVERAGE_PROOF.md`.

Folder layout:
```
_neo4j/review/2026-06-06_full_graph_verification/
  VERIFICATION_PLAN_15_AGENTS.md     (this file)
  AGENT_PROMPT_TEMPLATE.md
  VERIFICATION_LEDGER.schema.csv
  ledger/        agent_01.csv … agent_14.csv
  reports/       agent_01.md  … agent_15.md
  patches/       *.patch.jsonl  (Aggregator-generated, human-applied)
  VERIFICATION_LEDGER.csv  REMEDIATION_PLAN.md  CAMPAIGN_REPORT.md  COVERAGE_PROOF.md
```

---

## 6. MECE partition — proof of total coverage

### 6.1 Relationship types → owning agent (all 50 types, Σ = 15 457)
| Agent | Relationship types | ≈ rels |
|---|---|---|
| 01–06 | `VERBUNDEN_MIT_AKTEUR` (341, split by country/cross-border) | 341 |
| 07 | legacy `evidence_url`-bearing rels not in a 2026-06 run | (subset, tagged) |
| 09 | `BETEILIGT_AN` 599, `AUS_SPENDER` 245, `IN_EMPFANGSOBJEKT` 278, `HAT_BAUWERK` 194, `NUTZT_BAUWERK` 1, `LIEGT_IN_LAND` 651, `LIEGT_IN_STADT` 252 | 2 220 |
| 10 | `NUTZT_SOFTWARE` 54, `TEIL_VON_PROGRAMM` 35, `BETRIEBEN_VON` 9, `ERHALT_FOERDERUNG_DURCH` 3 | 101 |
| 11 | `GESTUETZT_AUF_REGELWERK` 167, `GILT_IN_LAND` 281 | 448 |
| 12 | `HAT_AKTEURROLLE` 1493, `HAT_BAUTEILTYP` 871, `HAT_AKTEURTYP` 700, `NUTZT_MATERIAL` 633, `HAT_MATERIALGRUPPE` 403, `HAT_BAUTEILGRUPPE` 364, `HAT_KENNWERT` 255, `HAT_NUTZUNG` 235, `HAT_BAUOBJEKTROLLE` 225, `HAT_BAUWEISE` 124, `HAT_VERBINDUNGSTECHNIK` 110, `HAT_GESCHAEFTSMODELL` 98, `HAT_ENTWURFSMETHODIK` 79, `HAT_ARCHITEKTURERGEBNIS` 79, `HAT_BAUSYSTEM` 61, `HAT_DEFEKT` 57, `HAT_ZUSTANDSKLASSE` 18, `TYPISCH_BEI_MATERIAL` 74, `TYPISCH_BEI_ERA` 15, `TYPISCH_BEI_BAUTEILTYP` 10, `GEBAUT_IN_ERA` 8 | 6 912 |
| 13 | `ERFORDERT_NACHWEIS` 1578, `TRIGGERS_REGULIERUNGSFRAGE` 1130, `HAT_PROZESSPHASE` 679, `HAT_BESCHAFFUNGSWEG` 592, `HAT_LOGISTIK` 434, `HAT_RUECKBAUVERFAHREN` 308, `HAT_ERGEBNIS` 294, `HAT_AUFBEREITUNG` 267, `HAT_RESSOURCENQUELLE` 264, `HAT_METHODE` 244, `HAT_HUERDE` 237, `HAT_INTERVENTION` 144, `ERFUELLT_NACHWEIS` 118, `HAT_SCHADSTOFFRISIKO` 100, `ERFORDERT_SCHADSTOFFPRUEFUNG` 37, `IST_UNTERVERFAHREN_VON` 9 | 6 435 |
| 14 | (meta — scans all, owns none exclusively) | — |

Σ ≈ 341 + 2 220 + 101 + 448 + 6 912 + 6 435 = **15 457** ✔ (the ~72 evidence-bearing `BETEILIGT_AN`/`HAT_BAUWERK`/`VERBUNDEN` are *also* web-checked by Agents 01–07 but counted once under their structural owner; the Aggregator dedups by `element_id`).

### 6.2 Node labels → owning agent (primary owner; Σ over primary labels = 2 304)
- Agents 01–06: sourced `Akteur` by country; **08:** unsourced `Akteur`. (697 total)
- 09: `Bauwerk` 184, `Projekt` 83, `Stadt` 74, `Land` 15.
- 10: `Software` 20, `Tool` 1, `Materialdepot` 22, `Programm` 31.
- 11: all law labels + `ReuseRule` (~210).
- 12: all controlled-vocabulary labels (Bauteilgruppe 364, Kennwert 255, … Schadstoff 13).
- 13: `PruefungNachweis` 118, `Nachweisforderung` 27, `Leistungsanforderung` 8, `Regulierungsfrage` 11, process vocab.
- 14: `DEPRECATED` 16 (isolation check).

The Aggregator runs `COVERAGE_PROOF.md`: `MATCH (n) RETURN n.id` minus union(processed node ids) must be **∅**; same for relationship ids.

---

## 7. Orchestration

### 7.1 Launch model
- 15 subagents via the `Task` tool, **`run_in_background: true`**, **non-readonly** (verifiers need `WebFetch` + Neo4j `read-cypher`; readonly mode disables internet/MCP). Their write-discipline is enforced by prompt + the §1 constraints, not by mode.
- **Wave 1 (parallel):** Agents 01–14 (independent shards; no inter-agent dependency; all read-only on the DB so zero write contention).
- **Wave 2:** Agent 15 starts only after 01–14 have written their `ledger/agent_<NN>.csv`.
- Each agent receives the **same** `AGENT_PROMPT_TEMPLATE.md` with its `{{AGENT_ID}}`, `{{SCOPE_CYPHER}}`, `{{SPECIAL_CHECKS}}`, `{{OUTPUT_PATHS}}` filled in.

### 7.2 Throughput & politeness
- Web-heavy agents (01–08, 10, 11) must cap concurrency, dedupe URLs (cache by URL across items), retry-once on timeout, and back off on 429. Reuse one fetched page for all claims citing it.
- Structural agents (09, 12, 13, 14) are Cypher-bound — fast, minimal web.
- Agent 08 (≈477 actors) is the long pole; it may `WebSearch` in batches and is allowed to mark low-value legacy stubs `ESCALATE_HUMAN` rather than exhaustively searching.

### 7.3 Failure handling
- If an agent crashes/stops mid-shard, it must have written incremental ledger rows; re-dispatch resumes from the last `claim_id`.
- Aggregator's coverage gap list drives any re-runs.

---

## 8. Remediation workflow (after the campaign)

1. Aggregator emits `patches/*.patch.jsonl` (grouped: `delete_unsupported`, `relabel_partial`, `add_missing_sources`, `fix_schema`, `deprecate_nodes`).
2. **Dry-run** each: `python _scripts/apply_neo4j_review_patch.py --patch <p> --database mit-bestand --report-dir apply_reports` → review `would_*` counts.
3. **Human approves**, then apply with `--confirm "APPLY <p> TO mit-bestand"`.
4. Re-run Agent 14 (hygiene) + the affected shard to confirm the fix and no regressions.
5. Update `AGENTS.md` "Aktueller Stand" counts and append a campaign entry.

This mirrors exactly the audited removal of the 29 fabricated edges (`unsupported_edges_removal.patch.jsonl`, `unsupported_edges_tier2_removal.patch.jsonl`).

---

## 9. Acceptance criteria (Definition of Done)

- [ ] **100 % coverage**: every node id and rel id appears in exactly one shard ledger (Agent 14/meta excluded); `COVERAGE_PROOF.md` shows ∅ gaps.
- [ ] Every Tier-A item (all `evidence_url` + all `source_url` rels + all sourced nodes) has `fetched=true` (or a justified `DEAD_LINK`/`UNVERIFIABLE`) and a `verdict`.
- [ ] **Zero `UNSUPPORTED` claims remain** post-remediation; zero `SCHEMA_VIOLATION`; zero forbidden properties.
- [ ] Every surviving `review_run` relationship is `PROVEN` or `PARTIAL`-then-relabeled with a verbatim `proof_quote`.
- [ ] `Materialdepot` nodes either gain a source or are `ESCALATE_HUMAN`/deprecated.
- [ ] `CAMPAIGN_REPORT.md` delivers the "why & where mistakes happened" breakdown by run/type/country.
- [ ] No graph mutation occurred except via dry-run-then-`--confirm` patches.

---

## 10. Risks & mitigations
| Risk | Mitigation |
|---|---|
| Verifier agents hallucinate "PROVEN" | §3.3 hard rule: no `proof_quote` ⇒ not provable; record `fetched`/`http_status`. |
| Paywalled/blocked sources (e.g. Le Moniteur) | `UNVERIFIABLE` verdict, never PROVEN; route to human. |
| Coverage gaps / double-counting | Aggregator coverage proof + dedupe by `element_id`. |
| Accidental graph writes | Agents read-only; all writes via gated patch tool with human `--confirm`. |
| 477-actor long tail stalls campaign | Agent 08 allowed to escalate legacy stubs instead of exhaustive search. |
| Rate limiting | URL cache, retry-once, back-off, shared-page reuse. |

---

## 11. Effort estimate (planning)
| Band | Agents | Dominant cost | Rough load |
|---|---|---|---|
| A web evidence | 01–07 | ~4k URL-bearing rels (deduped by URL) + 544 sourced nodes | bubble actor edges: hand-quality; regulation: batched |
| B entity/provenance | 08–11 | ~550 web searches + geo cross-check | medium-high |
| C structure | 12–14 | ~13 600 edges via Cypher | high volume, mechanical |
| Adjudication | 15 | merge + patches | low |

**Net:** the **highest-risk** surface is the 72 reuse-bubble `evidence_url` actor edges (hand-quality). The **largest** surface is 3,691 regulation `source_url` rels (Agent 07, URL-deduped batches). Tier C is mechanical. Off-graph ledgers are recovery hints only — see `EVIDENCE_URL_LOCATION_AUDIT.md`.
