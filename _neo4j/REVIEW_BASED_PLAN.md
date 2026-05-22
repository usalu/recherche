# Review-based remediation plan — `mit-bestand`

**Status:** Draft for user review
**Author:** Claude (Opus 4.7) based on three-layer skeptical review of `mit-bestand`
**Date drafted:** 2026-05-21
**Audience:** Kinan (owner) → future migration agents
**Replaces:** nothing yet — this is proposed alongside [FINAL_PASS2_AUDIT.md](intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md)

> **2026-06-01 advisory (post project reuse-focus cleanup of 2026-05-31):**
> project-level entities are now split across `:Projekt` (86 nodes — built
> reuse projects), `:Programm` (29 nodes — research / funded programmes;
> gained 6 from a 2026-05-31 `:Projekt` strip), `:Tool` / `:Software`
> (reclamation tools), and `:Marktmodell` (component-exchange marketplaces /
> Baubörsen). All counts and gap-audits below that say "projects" are scoped
> to `:Projekt` ONLY. For a holistic view, add a sibling `:Programm` count.
> Cleanup ledger:
> [`_neo4j/review/2026-05-31_project_reuse_focus_cleanup/MANUAL_REVIEW_CHECKPOINT.md`](review/2026-05-31_project_reuse_focus_cleanup/MANUAL_REVIEW_CHECKPOINT.md).

> **How to read this document.**
> §1 is the executive summary. §2 is the pre/post comparison that grounds judgment. §3 is the consolidated finding ledger from the three review layers. §4–§13 are remediation phases (R1 … R10) — each phase is independently reviewable, with its own rationale, acceptance gates, and rollback. §14 lists open decisions that block phases. Read §1 + §2 first; then skim §3; then read whichever phases you want to commit to.

---

## §1 Executive summary

### What this plan addresses

Three layers of review converged on one pattern: **the radical quality reset (2026-05-20) optimized the graph against its own audit gates rather than against the source dossiers**. The audit's "OVERALL: PASS" hides:

- A "Reuse Story" (Q1) that returns 266 rows only because 254 derived edges were relabeled as `curated` with auto-generated excerpts.
- A "Risk Story" (Q2) where 0 of 799 pollutant assertions are documented; all are era×material inference.
- A "Decision Shelf" (Q5/ReuseRule) of 20 nodes that have **no edge to any `:Projekt`** and carry a self-contradicting `inferred` + `belegt` evidence pair.
- A "Comparison" (Q3) over 4 entries in 3 projects, in different units and confidence levels.
- A demotion pattern that converted 5 queryable labels (`Layer`, `LebenszyklusModul`, `RechtlicheBedingung`, `ZertifizierungBewertungssystem`, `Tool`) into stringly-typed properties.
- 33 surgical deletes (Phase 1.5) keyed on degree, not on data quality.
- A "bookkeeping" value mixed into the `evidence_confidence` epistemic enum — silently inflating Q6's "derived" trust bucket by ≈ 24 %.

### What this plan does not address

- New data acquisition (more dossiers, more research files). Volume is not the constraint.
- Frontend / visualization. The graph itself is the focus.
- Performance / scaling. Current graph is tiny (3,802 nodes); not a bottleneck.

### Recommended sequencing

R1 → R2 → R3 → R4 are the **core honesty restoration**. Do them in order; each one is reversible. R5 → R10 are independent improvements that can be done in any order once R1–R4 land.

| Phase | What it does | Effort | Blast radius |
|---|---|:---:|:---:|
| R1 | Split `evidence_origin`; move `bookkeeping` out of confidence enum | M | Medium — relabels ~750 edges |
| R2 | Restore the 5 demoted concepts as queryable nodes | L | Medium — recreates ~36 nodes + ~70 edges |
| R3 | Add the missing structural edges (`:Projekt`→`:Bauwerk`, `:ReuseRule`→`:Projekt`) | M | Small — pure additions |
| R4 | Lift `*_facts` JSON-string properties into a `:Kennwert` node model | L | Small — pure additions + property strip |
| R5 | Disambiguate `:Bauteilgruppe` (batch vs category) | M | Medium — adds sublabel to 369 BGs |
| R6 | Language unification (de/en) | XL | Large — every label/type rename |
| R7 | Dossier loader hardening + the 7 orphans + the 16 dual-naming duplicates | M | Small — clean-up only |
| R8 | Rebuild the curation/audit relationship | M | Small — process change |
| R9 | Actor model: separate verified vs stub edge types | S | Small — type rename of 200 edges |
| R10 | Empty-label / empty-type cleanup with deprecation audit nodes | S | Small — registry-only |

---

## §2 Comparison: pre-reset vs post-reset

Concrete numbers from the audit reports and the round_002_followup documents. These are the facts you can judge against.

### §2.1 Headline counts over time

| Snapshot | Date | Nodes | Rels | Source |
|---|---|---:|---:|---|
| Round 001 audit | 2026-05-14 | 1,697 | 14,028 | [global_audit_report.md](review/round_001/global_audit_report.md) |
| Round 002 followup mid-flight | 2026-05-16 | 2,147 | 15,834 | [reuse_schema_proposals.md](review/round_002_followup/reuse_schema_proposals.md) |
| Batch 2 v2 complete (pre-radical-reset baseline) | 2026-05-20 | **2,580** | **19,989** | [AGENTS.md](../AGENTS.md), [agent_1_snapshot_report.md](intake/runs/2026-05-20_radical_quality_reset/reports/agent_1_snapshot_report.md) |
| Post-radical-reset (current) | 2026-05-21 | **3,802** | **25,023** | [FINAL_PASS2_AUDIT.md](intake/runs/2026-05-20_radical_quality_reset/FINAL_PASS2_AUDIT.md) |

**Net change from pre-radical-reset → post-radical-reset:** +1,222 nodes (+47 %), +5,034 relationships (+25 %). The radical reset *grew* the graph, it didn't shrink it.

### §2.2 What the radical reset actually removed (silent losses)

These were present before the reset and have no equivalent representation in the current graph. Where applicable, the data was preserved in property-form or in `deleted/*.jsonl` journals, but not in queryable graph topology.

| Concept | Pre-reset shape | Post-reset shape | Loss type |
|---|---|---|---|
| `Bauteilgruppe.counts_as_direct_reuse` boolean | true on **206 of 306 BGs** ([reuse_schema_proposals.md §0](review/round_002_followup/reuse_schema_proposals.md)) | **Deleted** (478 props across 314 BGs, Phase 2.1) | hard — not derivable without re-parsing dossiers |
| `Bauteilgruppe.counts_as_*` booleans (5 flags) | properties on most BGs | **Deleted** | hard |
| `BETEILIGT_AN.rolle_text` | 166 per-edge role descriptions | accumulated into per-actor `Akteur.raw_role_evidence` list-of-strings | soft — but per-project role context now requires string parsing |
| `:Layer` nodes + `TEILT_LAYER` edges | 6 nodes + 15 edges | `:Bauteiltyp.brand_layer` enum string | hard — Brand 6-layer cross-comparison no longer a graph step |
| `:LebenszyklusModul` + `BERECHNET_NACH_MODUL` + `METHODENGRUNDLAGE_NORM` | 5 nodes + 16 edges | `:Projekt.lca_module_scope` list mixing canonical + free-text | hard — and list mixes registers (`A1_A3` and `a1_a5` coexist) |
| `:RechtlicheBedingung` + `HAT_RECHTLICHE_BEDINGUNG` + `GILT_IN_LAND` | 9 nodes + 20 edges | `<src>.legal_conditions` list with country bracketed in string | hard — "all legal conditions for DE" now needs `CONTAINS '[…DE…]'` |
| `:ZertifizierungBewertungssystem` + `HAT_ZERTIFIZIERUNG` | 8 nodes + 18 edges | `:Projekt.certifications` list | hard — cross-project certification analysis lost |
| `:Tool` | 8 nodes | relabelled to `:Software {kind:'tool'}` | soft — discriminator works but dossier still uses "Tool" header |
| `:Akteur` low-degree | 6 nodes (`glasfischer_glastec`, `citydev_brussels`, `denkstatt`, `eitel_partner`, `gibbins_architekten`, `zusammenkunft_berlin`) | **Deleted** (Phase 1.5) | hard — real actors deleted by degree-1 heuristic |
| `:Programm` degree-0 | 4 nodes (`prog_bbsm`, `prog_preuse`, `prog_zukunftbau`, `prog_kommunales_programm`) | **Deleted** | hard — real research programmes deleted |
| `:Norm` degree-0 | 2 nodes (`norm_bs_5385_5_2009`, `norm_din_18940`) | **Deleted** | medium |
| `:Quelle` degree-0 dossier stubs | 21 nodes (incl. `qu_stuttgart210_baunetzwissen_s7`, `qu_stuttgart210_holzbauoffensive_s5`) | **Deleted** | medium — dossier-side S-ref names lost |
| `:Status` `status_gebaut` (185 edges) | distinct from `status_realisiert` (398 edges) | merged into `status_realisiert` | hard — "physically built" vs "realized as a project" distinction lost |
| `:Status` `status_wettbewerb` (1 edge) | distinct competition entry | merged into `status_prototyp` | medium |
| `:Akteurrolle` `ar_reuse_beratung` (4 edges) | narrower role | merged into `ar_reuse_zirkularitaetsberatung` (broader) | medium — narrower categorization absorbed into broader |
| `Bauwerk.bauwerkstatus` + `Bauwerk.status_text` | direct properties (15 total) | replaced by `HAT_STATUS` traversal | soft — single-property lookups become 2-hop |

### §2.3 What the radical reset added

| Concept | Pre-reset | Post-reset | Quality |
|---|---|---|---|
| `:ReuseRule` decision shelf | — | 20 nodes, wired to `:Land` + `:Material` | text-on-nodes; no edge to `:Projekt`; inferred+belegt contradiction |
| `:Schadstoff` pollutant model | 5 nodes / 1 edge ([reuse_knowledge_map.md §1](review/round_002_followup/reuse_knowledge_map.md)) | 9 nodes / 799 `HAS_RISK_POLLUTANT` + 347 `REQUIRES_VERIFICATION_FOR` | all inference; 0 documented |
| `:BauwerkEra` inference | — | 6 era nodes / 8 `BUILT_IN_ERA` edges (year→era) | inference only |
| `:Projekt.quality_tier` | — | 11/68/22 across 3 tiers | computed from scalar gates; can be inflated by Repair D promotions |
| `:Quelle` corpus | smaller, mostly dossiers | 1,586 nodes — case_markdown 116, external_link 264, external_link_from_actor_registry, research markdown, S-refs | 5+ subtypes, distinguished only by `quelltyp` property |
| `ANCHORED_BY` bookkeeping edges | — | 703 — for the 2 OntologyAnchor nodes | pollutes Q6 trust counts |
| `evidence_*` cluster | partial | 10 properties enforced by enums | enums passable via string concatenation (Repair D) |
| `*_facts` JSON-string properties | partial | `cost_facts`, `co2_facts`, `reuse_share_facts`, `quality_tier_facts` on `:Projekt` | parallel un-audited trust shape inside the JSON |

### §2.4 Acceptance-query honesty check

These are the seven queries the radical-reset audit holds up as proof of decision-grade-ness. The "honest" column is what the row count means once you discount synthetic data.

| Query | Headline row count | Honest interpretation |
|---|---:|---|
| Q1 Reuse Story | 266 | **254 of 266 promoted from `derived` to `curated` with auto-generated excerpts** (Repair D). Pre-Repair count: 0. |
| Q2 Risk Story | 799 | **0 documented**. 792 are `era_and_material` or `material_only` inference. |
| Q3 Comparison | 4 | 3 distinct projects; units differ; confidences range `belegt`→`unklar`. Not actually comparable. |
| Q4 Actor Network | 1 (RotorDC) | Trivial; doesn't justify a graph. |
| Q5 Decision Support | 20 ReuseRules | Wired to Land+Material; **no edge to Projekt**; carries inferred+belegt contradiction. |
| Q6 Trust Check | 3,188 curated / 2,948 derived / 347 inferred | **Curated is inflated** by ≥ 276 edges (254 Q1 promotion + ~22 unpacked + ~A-A5 synth fills). **Derived is inflated** by 703 ANCHORED_BY bookkeeping. Honest "derived from real evidence" ≈ 2,245. |
| Q7 Source Drill-down | 958 case_markdown→external | Mechanically true; treats Wikipedia-grade external_link the same as dossier-grade evidence. |

### §2.5 Pre-reset's open question — was the older state better?

No, the older state had its own structural problems (round_002_followup [reuse_schema_proposals.md](review/round_002_followup/reuse_schema_proposals.md) frankly admits this):

- "Projekt with `co2_einsparung_t` property: **7 of 99**"
- "Projekt with `bgf_m2` property: **1 of 99**"
- "Projekt with `errichtungsjahr` / `gesamtkosten_eur` / `reuse_anteil_pct`: **0 of 99** for each"
- "Bauteilgruppen WITHOUT any `HAT_PRUEFUNG`: 94 of 306 (≈ 31 %)"

So the pre-reset graph was sparser in quantitative coverage but **more structurally honest** about that sparseness. The radical reset added inference and ReuseRules to mask the sparseness without fixing it. This plan re-anchors on the older, more honest mode.

---

## §3 Finding ledger (the basis for the phases)

33 distinct findings across the three review layers, grouped by the phase that addresses them. Each finding has a stable F-number that the phases reference.

### §3.1 Trust / evidence model (→ R1, R8)

| F# | Finding | Severity |
|---|---|---|
| F1 | Q1's 254 "curated" edges are topology relabels with auto-generated excerpts (Repair D). | **Critical** |
| F23 | `evidence_confidence='bookkeeping'` mixes process-state into an epistemic enum; pollutes Q6. | High |
| F33 | When audits fail, the data is rewritten rather than the source re-curated. | **Critical** |
| F11.a | Repair D step F's "alphabetical priority" rule picked `curated` over `derived` on 22 list-typed edges. | Medium |
| F11.b | Repair D step G silently rewrote 243 `BELEGT_IN` edges from `research_file_row` to `cell_citation`. | Medium |
| F27 | `reuse_share_facts` JSON has its own `confidence` + `source_id` — parallel trust system. | High |
| F22 | Phase 1.2 anchor regression: 202 BELEGT_IN edges were re-created against a duplicate Quelle shell by a downstream agent. | High |

### §3.2 Demoted concepts / lost topology (→ R2)

| F# | Finding | Severity |
|---|---|---|
| F20.a | `:Layer` → property: 6 nodes / 15 edges lost. | Medium |
| F20.b | `:LebenszyklusModul` → list property: 5 nodes / 16 edges lost; list mixes registers. | High |
| F20.c | `:RechtlicheBedingung` → list with country in string brackets. | High |
| F20.d | `:ZertifizierungBewertungssystem` → list property. | Medium |
| F20.e | `:Tool` → `:Software {kind:'tool'}`. | Low |

### §3.3 Missing structural edges (→ R3)

| F# | Finding | Severity |
|---|---|---|
| F26 | No `(:Projekt)-[:HAS_BAUWERK]->(:Bauwerk)` direct edge — Projekt→Bauwerk requires Bauteilgruppe traversal. | **Critical** |
| F8 | `:ReuseRule` has no edge to `:Projekt`. | High |
| F9 | `:ReuseRule` carries `evidence_origin='inferred'` + `evidence_confidence='belegt'` (contradiction) which means rules can never lift a project to tier-1. | High |
| F32 | 7 different actor-to-actor / actor-to-project edge types with overlapping semantics. | Medium |
| F28 | ReuseRule covers 7 countries; tier-1 has projects in France (uncovered). | Medium |

### §3.4 Quantitative facts as JSON strings (→ R4)

| F# | Finding | Severity |
|---|---|---|
| F16 | `reuse_share_facts`, `co2_facts`, `cost_facts`, `quality_tier_facts` all stored as JSON-string properties on `:Projekt`. | **Critical** |
| F30 | `Section-8` (facts) extraction is wildly uneven across dossiers; many show 0 facts despite source-text quantification. | High |

### §3.5 Schema clarity / mental model (→ R5, R6, R10)

| F# | Finding | Severity |
|---|---|---|
| F6 | `:Bauteilgruppe` is both batch-instance and category-roll-up; no marker distinguishes them. | High |
| F4 | Bilingual schema: German + English mixed at label and rel-type level, no rule. | Medium |
| F7 | 4 empty-registered labels + 6 empty-registered rel types pollute discovery. | Low |
| F19 | `GEHÖRT_ZU` vs `VERBUNDEN_MIT_AKTEUR` overlap with no boundary rule. | Medium |
| F15 | 22 sub-10-node vocab labels; many of them coarser than the dossiers they ingest from. | Medium |
| F25 | `BETEILIGT_AN.rolle_text` stripped to `Akteur.raw_role_evidence` list — per-project role context now requires string parsing. | High |
| F24 | `status_gebaut` merged into `status_realisiert` — physically-built vs realized-as-project distinction lost. | Medium |
| F31 | `:MatchingQualitaet` is dark vocabulary — 9 nodes, 187 edges, no semantic glossary. | Low |
| F29 | `lca_module_scope` list mixes canonical enums with free-text legacy values. | Medium |

### §3.6 Ingestion pipeline (→ R7)

| F# | Finding | Severity |
|---|---|---|
| F12 | 16 dossiers have parallel `q_<slug>_md` AND legacy `qu_*_dossier` Quelle anchors; not reconciled. | High |
| F13 | 7 dossiers have no matching `:Projekt` — orphan citations from the meta-projects (ETH, FCRBE, REBRIDGE, REFAIR, Circl Pavilion Amsterdam, Berlin Schildow 2, RE_USE Höfe Wien). | High |
| F18 | Dossiers still use retired type names (`AUS_BAUWERK`, `EINGEBAUT_IN`, `LebenszyklusModul`, `Tool`, `ZertifizierungBewertungssystem`). Next ingestion will silently drop these cells. | High |

### §3.7 Actor model (→ R9)

| F# | Finding | Severity |
|---|---|---|
| F14 | 200 `ASSOZIIERT_MIT_PROJEKT` edges (26 % of actor↔project) are unverified registry stubs; naive `BETEILIGT_AN|ASSOZIIERT_MIT_PROJEKT` queries silently mix them in. | High |
| F21 | Phase 1.5 deleted 6 actors and 4 programmes by degree alone, not by data quality. Real research programmes (`prog_preuse`, `prog_zukunftbau`) were dropped. | High |

### §3.8 Source / Quelle model (→ part of R7)

| F# | Finding | Severity |
|---|---|---|
| F17 | `:Quelle` hides 5+ subtypes via `quelltyp` property. No subtype labels. | Medium |
| F5 | `BELEGT_IN` (4,734 edges) is overloaded — joins many node kinds to many Quelle kinds with no semantic shape. | Medium |

---

## §4 R1 — Restore honesty of the evidence model

**Addresses:** F1, F11.a/b, F23, F27, F33
**Effort:** Medium · **Risk:** Medium (touches ~750 edges, but all backed by current Repair-D / Phase-1.2 audit logs)
**Idempotent:** yes

### §4.1 Rationale

The current `evidence_origin ∈ {curated, inferred, derived}` enum is overloaded: `curated` means both "human read a source cell" and "Repair D auto-generated this from graph topology". The current `evidence_confidence` enum is contaminated by the process-state value `bookkeeping`. The current model cannot tell you which of the 3,188 "curated" edges are actually grounded in source text and which are synthesis artefacts.

### §4.2 Schema delta

Add new values to `evidence_origin`:

```
evidence_origin ∈ {
  source_curated,        // verbatim cell from a source document
  topology_synthesized,  // generated by Repair D / Repair A et al. from existing graph topology
  registry_derived,      // lineage from a master registry row; evidence requires the concrete row link, not q_akteursliste_master_md itself
  inferred,              // from a rule (era×material, year→era)
  external_unfolded      // from a citation array via mig_4c_1
}
```

Add a new boolean property on edges (default false):

```
is_bookkeeping: bool
```

Remove the `bookkeeping` enum value from `evidence_confidence`:

```
evidence_confidence ∈ {belegt, teilweise_belegt, unklar, inferiert}
```

(`bookkeeping` edges keep the actual epistemic value if any — typically `unklar` — but are tagged with `is_bookkeeping=true`.)

### §4.3 Migration steps (Cypher sketch)

```cypher
// R1.a — Reclassify Repair D promoted edges (254 HAT_BAUTEILGRUPPE)
MATCH ()-[r]->()
WHERE r.migration_origin CONTAINS 'mig_repair_4_1_q1'
SET r.evidence_origin = 'topology_synthesized';

// R1.b — Reclassify Repair D registry-context fills (A1-A5)
MATCH ()-[r]->()
WHERE r.migration_origin CONTAINS 'mig_repair_4_1_excerpts'
SET r.evidence_origin = 'registry_derived';

// R1.c — Reclassify Repair D unpacked merge artefacts (22 edges)
MATCH ()-[r]->()
WHERE r.migration_origin CONTAINS 'mig_repair_4_1_unpack'
SET r.evidence_origin = 'topology_synthesized';

// R1.d — external_unfolded from mig_4c_1
MATCH ()-[r:ZITIERT_QUELLE]->()
WHERE r.evidence_basis = 'external_sources_array'
SET r.evidence_origin = 'external_unfolded';

// R1.e — All other 'curated' becomes 'source_curated'
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
SET r.evidence_origin = 'source_curated';

// R1.f — Move bookkeeping out of confidence enum
MATCH ()-[r]->()
WHERE r.evidence_confidence = 'bookkeeping'
SET r.is_bookkeeping = true,
    r.evidence_confidence = 'unklar';

// R1.g — Reclassify ReuseRule contradictory inferred+belegt
MATCH (rule:ReuseRule)-[r:APPLIES_IN|APPLIES_TO|REFERENZIERT_NORM]->()
WHERE r.evidence_origin = 'inferred' AND r.evidence_confidence = 'belegt'
SET r.evidence_confidence = 'teilweise_belegt',
    r.derivation_note = coalesce(r.derivation_note, '') +
      ' | R1: inferred+belegt is a contradiction; downgraded to teilweise_belegt';
```

### §4.4 Acceptance gates

| Gate | Pass condition |
|---|---|
| Q1 rerun under new enum | Rows with `evidence_origin='source_curated'` must be **0** (because none of the 254 were source-curated). The audit reports the new number honestly. |
| Q6 rerun | Add a fifth bucket — `topology_synthesized` and `external_unfolded` shown separately. `derived` excludes `is_bookkeeping=true`. |
| ReuseRule rule integrity | No edge has `origin='inferred' AND confidence='belegt'`. |
| Bookkeeping flag | `MATCH ()-[r]->() WHERE r.evidence_confidence='bookkeeping' RETURN count(r)` → **0** |
| Bookkeeping flag accounted | `MATCH ()-[r {is_bookkeeping:true}]->() RETURN count(r)` ≈ 703 |
| No evidence-origin-enum violations | Every edge with non-null `evidence_origin` is in the new 5-value enum. |

### §4.5 Rollback

Single Cypher to revert:

```cypher
MATCH ()-[r]->()
WHERE r.evidence_origin IN ['source_curated', 'topology_synthesized', 'registry_derived', 'external_unfolded']
SET r.evidence_origin = CASE r.evidence_origin
    WHEN 'source_curated' THEN 'curated'
    WHEN 'topology_synthesized' THEN 'curated'  // accepts the lie back
    WHEN 'registry_derived' THEN 'curated'
    WHEN 'external_unfolded' THEN 'derived'
END;

MATCH ()-[r]->()
WHERE r.is_bookkeeping = true
SET r.evidence_confidence = 'bookkeeping'
REMOVE r.is_bookkeeping;
```

### §4.6 Risks / open questions

- Q1's row count under the honest classification will drop to 0 unless the dossier-side cells are actually parsed. R1 alone doesn't fix Q1; it just stops lying about it. R8 is the follow-up that *fixes* Q1.
- The `derivation_note` chains will grow further. Acceptable; they remain the forensic trail.
- Open question: should `registry_derived` keep `confidence='belegt'`? The actor master file is human-maintained lineage, but the file itself is not source truth. Actor identity can be belegt only when tied to the concrete link in that actor row; project participation needs its own concrete URL. **Decision needed (D1).**

---

## §5 R2 — Restore the 5 demoted concepts as queryable nodes

**Addresses:** F20.a–F20.e
**Effort:** Large · **Risk:** Medium (recreates ~36 nodes + ~70 edges)
**Idempotent:** yes

### §5.1 Rationale

Phase 2.5 of the radical reset collapsed 5 label families to string/list properties. Every collapse cited "underused" as justification, but in every case the data is queryably richer when it lives as a graph rather than a property. The corpus has only 9 RechtlicheBedingung nodes — that is the *content* of the data, not a reason to delete the label.

### §5.2 What to restore

For each demoted concept, restore as a node, **keep the property as a deprecated mirror** for one cycle, and re-create the edges from the property values.

| Demoted concept | Property to read | Node label to restore | Edge to restore |
|---|---|---|---|
| Layer | `:Bauteiltyp.brand_layer` | `:Layer {id, name, brand_position}` | `(:Bauteiltyp)-[:TEILT_LAYER]->(:Layer)` |
| LebenszyklusModul | `:Projekt.lca_module_scope` (list) | `:LCAModule {id, name, en15978_code}` | `(:Projekt)-[:BERECHNET_NACH_MODUL]->(:LCAModule)` |
| RechtlicheBedingung | `<src>.legal_conditions` (list with country brackets) | `:RechtlicheBedingung {id, name}` | `(<src>)-[:HAT_RECHTLICHE_BEDINGUNG]->(:RechtlicheBedingung)` + `(:RechtlicheBedingung)-[:GILT_IN_LAND]->(:Land)` |
| Zertifizierung | `:Projekt.certifications` (list) | `:Zertifizierungssystem {id, name, scheme_kind}` (cleaner name than the old `:ZertifizierungBewertungssystem`) | `(:Projekt)-[:HAT_ZERTIFIZIERUNG]->(:Zertifizierungssystem)` |
| Tool | `:Software {kind:'tool'}` | keep `:Software` label; add `:Tool` as **secondary** label (Neo4j supports multiple labels) | no edge change needed |

### §5.3 Migration steps

For LCAModule (representative):

```cypher
// R2.b.1 — Normalise the list (drop free-text values, uppercase enums)
MATCH (p:Projekt)
WHERE p.lca_module_scope IS NOT NULL
WITH p,
     [x IN p.lca_module_scope WHERE
        toUpper(x) IN ['A1_A3','A1_A5','A4_A5','B','C1_C4','D']
      | toUpper(x)] AS canonical,
     [x IN p.lca_module_scope WHERE NOT
        toUpper(x) IN ['A1_A3','A1_A5','A4_A5','B','C1_C4','D']] AS free_text
SET p.lca_module_scope = canonical,
    p.lca_module_legacy = free_text;

// R2.b.2 — Recreate :LCAModule nodes (5 max)
UNWIND ['A1_A3','A1_A5','A4_A5','B','C1_C4','D'] AS code
MERGE (lcm:LCAModule {id: 'lcm_' + toLower(replace(code,'_',''))})
ON CREATE SET lcm.name = code,
              lcm.en15978_code = code,
              lcm.source_scope = 'r2_restore';

// R2.b.3 — Recreate edges
MATCH (p:Projekt) WHERE p.lca_module_scope IS NOT NULL
UNWIND p.lca_module_scope AS code
MATCH (lcm:LCAModule {en15978_code: code})
MERGE (p)-[r:BERECHNET_NACH_MODUL]->(lcm)
ON CREATE SET r.evidence_origin = 'source_curated',
              r.evidence_basis = 'cell_citation',
              r.evidence_source_id = 'r2_lca_restore',
              r.evidence_confidence = 'teilweise_belegt',
              r.migration_origin = 'r2_lca_restore';
```

Pattern is the same for the other four. Critical detail: for `:RechtlicheBedingung`, the country has to be parsed out of the bracketed string (`'<name> [DE,BE]'` → name, [DE,BE]). Use a deterministic parser; reject any string that doesn't match the bracket pattern and journal it.

### §5.4 Acceptance gates

| Gate | Pass condition |
|---|---|
| Layer node count | ≥ 5 (the Brand layers: structure / skin / services / space_plan / stuff; `site` is project-level not BT-level) |
| LCAModule node count | 5 (A1_A3, A1_A5, A4_A5, B, C1_C4, D) |
| RechtlicheBedingung restored | ≥ 9 nodes (the original count) |
| Zertifizierungssystem restored | ≥ 6 nodes (BREEAM, WELL, NABERS, Paris_Proof, DGNB, Nordic Swan; LEED if orphaned in deleted/*.jsonl) |
| Property mirrors retained | `.lca_module_scope`, `.certifications`, `.legal_conditions` all still present on source nodes |
| No information loss | For every project p, the set of `:LCAModule` reachable equals the canonical part of `p.lca_module_scope` |

### §5.5 Rollback

Drop the new labels and delete the recreated nodes — properties were preserved.

### §5.6 Open questions

- Open question (D2): Do we **delete** the mirror properties after R2 stabilises, or keep them indefinitely as "denormalized convenience"? Recommendation: delete after one batch of new ingestion confirms the node form is loader-ready.

---

## §6 R3 — Add the missing structural edges

**Addresses:** F26, F8, F9 (partially via R1), F28, F32 (partially)
**Effort:** Medium · **Risk:** Small (pure additions)
**Idempotent:** yes

### §6.1 Rationale

Three structural edges are missing that a first-time user expects:

1. `(:Projekt)-[:HAS_BAUWERK]->(:Bauwerk)` — currently routed indirectly via `:Bauteilgruppe`.
2. `(:ReuseRule)-[:RELEVANT_FOR]->(:Projekt)` — currently a manual join through `:Land` + `:Material`.
3. `(:Bauteilgruppe)-[:DERIVED_FROM]->(:Bauteilgruppe)` (optional, for reuse-chain semantics that `:Wiederverwendungskette` half-models). **Decision needed (D3).**

### §6.2 Migration steps

```cypher
// R3.a — :Projekt-[:HAS_BAUWERK]->:Bauwerk
//        Derived from the Bauteilgruppe → donor/receiver topology.
//        donor_or_receiver property distinguishes the role.
MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:FROM_DONOR]->(b:Bauwerk)
MERGE (p)-[h:HAS_BAUWERK {role: 'donor'}]->(b)
ON CREATE SET h.evidence_origin = 'topology_synthesized',
              h.evidence_basis = 'derived_from_bg_topology',
              h.evidence_confidence = 'teilweise_belegt',
              h.migration_origin = 'r3_a_has_bauwerk';

MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(b:Bauwerk)
MERGE (p)-[h:HAS_BAUWERK {role: 'receiver'}]->(b)
ON CREATE SET h.evidence_origin = 'topology_synthesized',
              h.evidence_basis = 'derived_from_bg_topology',
              h.evidence_confidence = 'teilweise_belegt',
              h.migration_origin = 'r3_a_has_bauwerk';

// R3.b — :ReuseRule-[:RELEVANT_FOR]->:Projekt
//        Match on Land + any-of-Material via the BG NUTZT_MATERIAL chain.
MATCH (rule:ReuseRule)-[:APPLIES_IN]->(l:Land)<-[:LIEGT_IN_LAND]-(p:Projekt),
      (rule)-[:APPLIES_TO]->(m:Material)
WHERE exists{
  (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m)
}
MERGE (rule)-[r:RELEVANT_FOR]->(p)
ON CREATE SET r.evidence_origin = 'topology_synthesized',
              r.evidence_basis = 'country_material_match',
              r.evidence_confidence = 'teilweise_belegt',
              r.migration_origin = 'r3_b_reuserule_relevant_for';
```

### §6.3 Acceptance gates

| Gate | Pass condition |
|---|---|
| `:HAS_BAUWERK` count | ≥ 200 (≥ FROM_DONOR + INTO_RECEIVER distinct (p, b) tuples) |
| Every `:Projekt` with ≥ 1 BG has ≥ 1 `:HAS_BAUWERK` | Yes |
| `:ReuseRule->:Projekt` for Holbein Gardens | Returns rule_1 (UK/Stahl) |
| `:ReuseRule->:Projekt` for Ferme du Rail | Returns zero (FR is uncovered — exposes F28 cleanly) |
| Honest answer for "France not covered" | Visible at the schema level, not buried in research file |

### §6.4 Rollback

Delete edges by `migration_origin`:

```cypher
MATCH ()-[r]->()
WHERE r.migration_origin STARTS WITH 'r3_'
DELETE r;
```

### §6.5 Open questions

- D3: Add `:Bauteilgruppe-[:DERIVED_FROM]->:Bauteilgruppe` for cross-project chains? Only meaningful if multi-hop reuse chains actually exist in the data. 14 `:Wiederverwendungskette` nodes suggest yes-but-sparse. Recommendation: defer to a separate R3.5 once R3 is in place.

---

## §7 R4 — Lift `*_facts` JSON-string properties into a `:Kennwert` node model

**Addresses:** F16, F27 (parallel trust), F30 (visibility)
**Effort:** Large · **Risk:** Small (pure additions, then property strip)
**Idempotent:** yes

### §7.1 Rationale

`cost_facts`, `co2_facts`, `reuse_share_facts`, `quality_tier_facts` are arrays of JSON-strings on `:Projekt`. Their contents — verified reuse share, CO₂ savings, costs — are exactly the decision-relevant numbers the graph is supposed to support. Burying them as `apoc.convert.fromJsonList`-required strings defeats the point of a graph.

### §7.2 Schema delta

```
:Kennwert {
  id: 'kw_<projekt>_<kennwert>_<i>',
  kennwert: <name string>,
  wert: <float or text>,
  wert_min: float,
  wert_max: float,
  einheit: <enum: percent, t_co2, eur, m2, m3, …>,
  method: <free-text>,
  bilanzgrenze: <enum: A1_A3, A1_A5, A4_A5, B, C, D, lifecycle, …>
}

(:Projekt)-[:HAT_KENNWERT]->(:Kennwert)
  evidence_origin, evidence_basis, evidence_confidence, evidence_source_id, evidence_excerpt
```

Three subtypes of `kennwert` field: `reuse_share`, `co2_saving`, `cost`. Use the `kennwert` string as discriminator rather than 3 separate labels — keeps the model simple, indexable, and additive for new metric kinds.

### §7.3 Migration steps

```cypher
// R4.a — Parse reuse_share_facts JSON arrays into nodes
MATCH (p:Projekt)
WHERE size(coalesce(p.reuse_share_facts, [])) > 0
UNWIND apoc.convert.fromJsonList(p.reuse_share_facts) AS fact
WITH p, fact,
     'kw_' + p.id + '_reuse_share_' + apoc.text.random(6) AS new_id
MERGE (kw:Kennwert {id: new_id})
SET kw.kennwert = fact.kennwert,
    kw.wert = fact.wert,
    kw.einheit = coalesce(fact.einheit, '%'),
    kw.method = fact.method,
    kw.bilanzgrenze = fact.bilanzgrenze,
    kw.migration_origin = 'r4_a_reuse_share'
MERGE (p)-[r:HAT_KENNWERT]->(kw)
ON CREATE SET r.evidence_origin = CASE
                WHEN fact.confidence = 'belegt' THEN 'source_curated'
                WHEN fact.confidence = 'teilweise_belegt' THEN 'source_curated'
                WHEN fact.confidence = 'unklar' THEN 'derived'
                ELSE 'inferred' END,
              r.evidence_basis = 'cell_citation',
              r.evidence_confidence = coalesce(fact.confidence, 'unklar'),
              r.evidence_source_id = fact.source_id,
              r.migration_origin = 'r4_a_reuse_share';

// (analogous for cost_facts and co2_facts)

// R4.b — Strip the JSON-string properties only after acceptance gates pass
//        (defer to a separate run; see Rollback)
```

### §7.4 Acceptance gates

| Gate | Pass condition |
|---|---|
| `:Kennwert` count | ≥ 4 (Q3 has 4 reuse_share entries; cost/co2 add more) |
| Every JSON entry in `reuse_share_facts` has a `:Kennwert` node | 1:1 |
| `evidence_confidence` on `HAT_KENNWERT` matches inner JSON `confidence` | 1:1 |
| `evidence_source_id` populated for ≥ 80 % of `:Kennwert` | yes (only "unknown source" entries lack it) |
| New Q3 query (using `:Kennwert`) | `MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert) WHERE kw.kennwert CONTAINS 'reuse' RETURN p, kw` — returns ≥ 3 projects |

### §7.5 Rollback

Two stages:

- Before R4.b (property strip): drop `:Kennwert` nodes via `migration_origin='r4_*'`. Properties unchanged.
- After R4.b: reverse-serialize. Each `:Kennwert` becomes a JSON object via `apoc.convert.toJson`; collected per `:Projekt`; reassigned to the original property. The migration must journal the original JSON-strings byte-by-byte before R4.b runs.

### §7.6 Open questions

- D4: Should `:Kennwert` carry a `category` enum (`reuse_share`, `cost`, `co2_saving`, `quality_tier`, `dimension`) for explicit typing, or stay discriminated only by the `kennwert` string?
- D5: Should `quality_tier_facts` (the per-project sub-score fold from Phase 5) also be lifted? It's not a *measurement*, it's an internal audit fold. Recommendation: keep on `:Projekt` as a debug property, do not lift.

---

## §8 R5 — Disambiguate `:Bauteilgruppe` (batch vs category)

**Addresses:** F6, partially F25 (per-project role-text)
**Effort:** Medium · **Risk:** Medium (tags 369 BGs)
**Idempotent:** yes

### §8.1 Rationale

A `:Bauteilgruppe` like `bg_stuttgart_21_clt_formwork_elements` is clearly a **batch** ("the 12 specific CLT elements salvaged from Stuttgart 21"). Other BGs are **categories** ("structural steel" — a roll-up of that material in a project, with no donor edge). The schema doesn't mark this. Aggregation queries (total quantity, donor density, reuse-chain length) silently mix the two and produce meaningless aggregates.

### §8.2 Schema delta

Add a property `bg_kind ∈ {batch, category}` to every `:Bauteilgruppe`.

- `batch` if the BG has `FROM_DONOR` OR `INTO_RECEIVER` edge (concrete reuse event).
- `category` if neither edge exists (vocabulary-level roll-up).

Optionally also add a Neo4j secondary label `:BauteilgruppeBatch` or `:BauteilgruppeCategory` for fast type-filtered MATCH. **Decision needed (D6).**

### §8.3 Migration steps

```cypher
MATCH (bg:Bauteilgruppe)
WITH bg, exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()} AS is_batch
SET bg.bg_kind = CASE WHEN is_batch THEN 'batch' ELSE 'category' END,
    bg.migration_origin = coalesce(bg.migration_origin,'') + ' | r5_bg_disambiguation';

// Optional secondary label (if D6 = yes):
MATCH (bg:Bauteilgruppe {bg_kind: 'batch'})
SET bg:BauteilgruppeBatch;
MATCH (bg:Bauteilgruppe {bg_kind: 'category'})
SET bg:BauteilgruppeCategory;
```

### §8.4 Acceptance gates

| Gate | Pass condition |
|---|---|
| All 369 BGs have `bg_kind` | yes |
| `batch` count ≥ 254 | yes (the BGs Repair D's Q1 query found) |
| `category` count = 369 − batch | matches |
| Aggregation queries now type-safe | `MATCH (bg:Bauteilgruppe {bg_kind:'batch'}) RETURN sum(coalesce(bg.menge_t, 0))` returns a meaningful number |

### §8.5 Rollback

`REMOVE bg.bg_kind`. Optionally drop secondary labels.

---

## §9 R6 — Schema language unification

**Addresses:** F4
**Effort:** Extra Large · **Risk:** Large (touches every label, every rel type, every property name)
**Idempotent:** depends on direction
**Status:** **Decision-blocked.** See §14 D7.

### §9.1 Rationale

The schema mixes German and English at every level. A user must know that `HAT_BAUTEILGRUPPE` is the same kind of edge as `HAS_RISK_POLLUTANT`, that `:Bauwerk` is a building and `:Projekt` is a project, that `:Schadstoff` is a pollutant and `:Akteur` is an actor. There is no rule for which language a new concept should be in. Half of the radical-reset additions are English (`FROM_DONOR`, `INTO_RECEIVER`, `BUILT_IN_ERA`, `ReuseRule`); the legacy core is German.

### §9.2 Two viable directions (mutually exclusive)

**Direction A: All English**
- All labels Latinized: `Akteur` → `Actor`, `Bauwerk` → `Building`, `Bauteilgruppe` → `ComponentBatch`, `Projekt` → `Project`, `Quelle` → `Source`, `Norm` → `Standard`, `Schadstoff` → `Pollutant`, `Land` → `Country`, etc.
- All rel types Latinized: `HAT_BAUTEILGRUPPE` → `HAS_COMPONENT_BATCH`, `BETEILIGT_AN` → `PARTICIPATES_IN`, `LIEGT_IN_LAND` → `LOCATED_IN_COUNTRY`, etc.
- Property names Latinized.
- Pros: matches the EU research literature lingua franca; international audience-friendly; aligns with the new (English) acceptance-query types.
- Cons: severs continuity with the source dossiers, which are German-tabular; loader must add translation layer.

**Direction B: All German**
- New types renamed back: `FROM_DONOR` → `AUS_BAUWERK`, `INTO_RECEIVER` → `EINGEBAUT_IN`, `HAS_RISK_POLLUTANT` → `HAT_SCHADSTOFFRISIKO`, `REQUIRES_VERIFICATION_FOR` → `ERFORDERT_PRUEFUNG_FUER`, `BUILT_IN_ERA` → `ERRICHTET_IN_EPOCHE`, `ReuseRule` → `WiederverwendungsRegel`, etc.
- Pros: matches the dossier source language; restores the pre-reset vocabulary; loader is direct.
- Cons: international consumer-friendliness drops; literature alignment drops.

### §9.3 Migration steps (sketch for Direction A)

```cypher
// R6.a — Use apoc.refactor.rename.type for every rel type
CALL apoc.refactor.rename.type('HAT_BAUTEILGRUPPE', 'HAS_COMPONENT_BATCH')
YIELD batches, total RETURN total;
// (repeat for ~30 rel types)

// R6.b — Use apoc.refactor.rename.label for every label
CALL apoc.refactor.rename.label('Bauteilgruppe', 'ComponentBatch')
YIELD batches, total RETURN total;
// (repeat for ~25 labels)

// R6.c — Rename properties (per-node iteration)
MATCH (n) WHERE n.einheit IS NOT NULL
SET n.unit = n.einheit REMOVE n.einheit;
// etc.
```

### §9.4 Acceptance gates

| Gate | Pass condition |
|---|---|
| All labels in one language | yes |
| All rel types in one language | yes |
| All property names in one language | yes |
| All Cypher queries in `_neo4j/review/round_002_followup/` updated | yes |
| All dossier loaders updated to translate dossier-language to schema-language | yes |
| Acceptance Q1–Q7 still PASS (under their new query forms) | yes |

### §9.5 Rollback

Reverse-rename every label, type, property. Apply the reverse mapping. Apoc rename is reversible.

### §9.6 Open questions

- **D7:** Which direction? Recommendation: **Direction A (English)** because (a) ReuseRule is already English, (b) the EU literature is, (c) the international audience for reuse research is larger. But the dossier translation cost is real. Defer until Kinan signals.

---

## §10 R7 — Dossier loader hardening

**Addresses:** F12 (dual naming), F13 (7 orphans), F18 (schema drift in dossier text), F30 (Section-8 unevenness)
**Effort:** Medium · **Risk:** Small (loader-side; pure additions or controlled deletes)
**Idempotent:** yes

### §10.1 Rationale

The dossier ingestion pipeline (agent 9, agent 10, etc.) has three documented coherence failures: 16 dossiers have parallel q_<slug>_md AND legacy qu_*_dossier Quelle anchors; 7 dossiers couldn't resolve to a `:Projekt`; Section-8 extraction misses most quantitative cells; the dossiers still write retired type names that the next loader will silently drop.

### §10.2 Tasks

**R7.a — Reconcile dual-naming Quelle anchors**

For the 16 dossier slugs with both `q_<slug>_md` and `qu_<slug>_dossier`:
- `MATCH (q_old:Quelle {id: 'qu_<slug>_dossier'})` and `(q_new:Quelle {id: 'q_<slug>_md'})`
- Move all incoming/outgoing edges from `q_old` to `q_new` via `apoc.refactor.mergeNodes`.
- Add `q_old.id` to `q_new.aliases`.
- Detach delete `q_old`.

**R7.b — Resolve the 7 orphan dossiers**

The 7 dossiers that have no matching `:Projekt`:
1. `q_eth_circular_construction_programme_md` → already relabelled to `:Programm`; create the missing `:Programm` node and re-route the citations.
2. `q_fcrbe_facilitating_circulation_reclaimed_building_elements_md` → already a `:Programm` candidate; create.
3. `q_rebridge_structural_reuse_md` → meta-project; create as `:Programm`.
4. `q_refair_bordeaux_md` → reuse platform; create as `:Programm` or `:Marktmodell` (decision needed, D8).
5. `q_circl_pavilion_amsterdam_md` → standalone project; create `:Projekt` with `p_circl_pavilion_amsterdam`.
6. `q_re_use_hoefe_wien_md` → standalone project; create `:Projekt` with `p_re_use_hoefe_wien`.
7. `q_berlin_schildow_pilot_house_2_md` → sibling of `p_berlin_schildow_pilot_house`; create with explicit relation to sibling.

**R7.c — Section-8 re-extraction**

For each dossier with `section8_facts=0` in the agent_9 report:
- Re-parse the dossier's "Economy", "Wirtschaft", "co2", "reuse_share", "cost" sections.
- Identify quantitative cells (numbers with units, ranges, percentages).
- Emit `:Kennwert` nodes (using R4's schema) with `evidence_origin='source_curated'` only when the cell has a clear numerical + unit + source.

This is the work that should have been Repair D's actual job.

**R7.d — Dossier-schema drift detection**

Add a pre-flight validation script `_scripts/validate_dossier_schema.py`:
- For each dossier `.md` file, extract column headers and relation-table labels.
- Cross-check against the live graph schema.
- Emit warnings for retired labels (`LebenszyklusModul`, `ZertifizierungBewertungssystem`, `Tool`, `AUS_BAUWERK`, `EINGEBAUT_IN`).
- Block the next ingestion if drift is unresolved.

### §10.3 Acceptance gates

| Gate | Pass condition |
|---|---|
| `qu_*_dossier` Quelle node count | 0 (all merged into `q_<slug>_md` siblings) |
| 7 unmatched dossiers resolved | each has either a `:Projekt` or `:Programm` matching its dossier identity |
| Section-8 re-extraction surfaces ≥ 5 new `:Kennwert` per high-content dossier | yes (Stuttgart 210, Circl Pavilion Amsterdam, et al. each have ≥ 5 verifiable numbers in their dossier text) |
| `_scripts/validate_dossier_schema.py` exits clean on the current 116 dossiers | yes (after dossier-side updates) |

### §10.4 Rollback

Per-dossier journal in `runs/<date>/r7_journal/<dossier>.jsonl` capturing the pre-merge state. Replayable.

---

## §11 R8 — Rebuild the curation/audit relationship

**Addresses:** F33 (audit-driven rewrites), F1 (Repair D's actual fix), partially F30
**Effort:** Medium · **Risk:** Small (process change)
**Idempotent:** yes (process is)

### §11.1 Rationale

The Repair-D-and-friends pattern shows that this graph's failure mode is to satisfy audit gates by rewriting data rather than by re-curating. The right architecture is to record audit failures as queryable graph artefacts and to fix them via targeted curation, not via blanket reclassifications.

### §11.2 Schema delta

```
:DataIssue {
  id, kind, severity, ref_label, ref_id,
  found_at, found_by,
  status: ∈ {open, in_review, resolved, won't_fix, false_positive},
  resolution_note
}

(:DataIssue)-[:CONCERNS]->(<any node>)
(:DataIssue)-[:CONCERNS_EDGE_BETWEEN {rel_type, rel_internal_id}]->(<any node>)  
   // for edge-targeted issues, attach to one endpoint with the other recorded as property
```

### §11.3 Initial population

```cypher
// Issue 1: every Repair-D-promoted edge is an open issue
MATCH ()-[r]->()
WHERE r.evidence_origin = 'topology_synthesized'
  AND r.migration_origin CONTAINS 'mig_repair_4_1_q1'
WITH r, startNode(r) AS s, endNode(r) AS t
MERGE (i:DataIssue {id: 'di_q1_promotion_' + type(r) + '_' + coalesce(s.id, toString(elementId(s))) + '_' + coalesce(t.id, toString(elementId(t)))})
SET i.kind = 'topology_synthesis_curation_missing',
    i.severity = 'high',
    i.ref_label = type(r),
    i.ref_id = r.id,
    i.found_at = '2026-05-21',
    i.found_by = 'r8_audit_seed',
    i.status = 'open',
    i.resolution_note = 'Promoted from derived to curated by Repair D without source-cell parse. Requires dossier re-read.'
MERGE (i)-[c:CONCERNS]->(s);

// Issue 2: every HAS_RISK_POLLUTANT with origin=inferred is an issue
MATCH ()-[r:HAS_RISK_POLLUTANT]->()
WHERE r.evidence_origin = 'inferred'
  AND r.evidence_basis IN ['era_and_material', 'material_only']
WITH r, startNode(r) AS bg, endNode(r) AS s
MERGE (i:DataIssue {id: 'di_pollutant_inference_' + bg.id + '_' + s.id})
SET i.kind = 'pollutant_inference_not_documented',
    i.severity = 'medium',
    i.found_at = '2026-05-21',
    i.found_by = 'r8_audit_seed',
    i.status = 'open',
    i.resolution_note = 'Inferred from era × material lookup. No source-cell citation; requires dossier verification.'
MERGE (i)-[c:CONCERNS]->(bg);

// Issue 3: 7 orphan dossiers (will be resolved by R7)
// Issue 4: 200 needs_verification=true ASSOZIIERT_MIT_PROJEKT edges (resolved by R9)
// ...
```

### §11.4 Audit policy change

| Old policy | New policy |
|---|---|
| Audit finds N violations → migration rewrites N records to pass | Audit finds N violations → migration creates N `:DataIssue` nodes; live graph remains as-is |
| Verifier 10 finds 2,108 curated-without-excerpt edges → Repair D fills excerpts | Verifier records 2,108 issues; resolution is per-edge re-curation against source |
| Tier-1 gate requires ≥ 3 curated evidence edges → promote derived to curated | Tier-1 gate counts only `evidence_origin='source_curated'`; tier-1 cohort drops; that drop is the honest signal |

### §11.5 Acceptance gates

| Gate | Pass condition |
|---|---|
| `:DataIssue` count | ≥ 1,000 (every Repair-D edge + every inferred-pollutant + every needs_verification) |
| Issue density per `:Projekt` queryable | `MATCH (i:DataIssue)-[:CONCERNS]->(p:Projekt) RETURN p.id, count(i)` returns meaningful distribution |
| `quality_tier` recomputed under R8 policy | tier-1 cohort drops (likely to 3–5 projects); that's the honest signal |
| No new migration writes `evidence_origin='source_curated'` without a verbatim excerpt | enforced at gate level |

### §11.6 Rollback

Detach-delete all `:DataIssue` nodes. Policy change cannot be rolled back without explicit decision; it's a workflow.

---

## §12 R9 — Actor model: separate verified from stub

**Addresses:** F14 (26 % stubs silently mixed), partially F21
**Effort:** Small · **Risk:** Small (renames 200 edges)
**Idempotent:** yes

### §12.1 Rationale

`ASSOZIIERT_MIT_PROJEKT` is documented as a registry stub edge (with `needs_verification=true`) but its name reads as if it were a real participation edge. The 200 edges of this type silently mix into actor-network queries. The fix is to either rename the type or split it.

### §12.2 Migration steps

```cypher
// R9.a — Rename ASSOZIIERT_MIT_PROJEKT to STUB_PROJECT_LINK to make intent visible
MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
WITH collect(r) AS rels
CALL apoc.refactor.rename.type('ASSOZIIERT_MIT_PROJEKT', 'STUB_PROJECT_LINK', rels)
YIELD total RETURN total;

// R9.b — Resolve stubs by promoting where dossier confirms
//        (per-actor, per-project; manual curation queue from R8)
MATCH (a:Akteur)-[r:STUB_PROJECT_LINK]->(p:Projekt)
WHERE exists{
  (p)-[:BELEGT_IN]->(q:Quelle {quelltyp:'case_markdown'})
  WHERE q.text_content CONTAINS a.name  // requires text_content property on Quelle
}
// promote to BETEILIGT_AN
CREATE (a)-[r2:BETEILIGT_AN]->(p)
SET r2 = properties(r),
    r2.needs_verification = false,
    r2.promoted_by = 'r9_stub_promotion',
    r2.evidence_origin = 'source_curated'
DELETE r;
```

R9.b's text-match requires `:Quelle.text_content` to be populated. **Decision needed (D9).**

### §12.3 Acceptance gates

| Gate | Pass condition |
|---|---|
| `ASSOZIIERT_MIT_PROJEKT` count | 0 |
| `STUB_PROJECT_LINK` count | ≤ 200 (minus the ones R9.b promoted) |
| Q4 rerun under new types | New honest count; likely still small, but the filter is now explicit |

### §12.4 Rollback

Reverse rename: `apoc.refactor.rename.type('STUB_PROJECT_LINK', 'ASSOZIIERT_MIT_PROJEKT', rels)`.

---

## §13 R10 — Empty-label / empty-type cleanup with deprecation audit nodes

**Addresses:** F7, partially F18 (dossier drift)
**Effort:** Small · **Risk:** Small (registry-only)
**Idempotent:** yes

### §13.1 Rationale

`:GraphVersion`, `:RechtlicheBedingung`, `:Tool`, `:ZertifizierungBewertungssystem` are registered labels with 0 nodes. `AUS_BAUWERK`, `EINGEBAUT_IN`, `HAT_RECHTLICHE_BEDINGUNG`, `HAT_SCHADSTOFF`, `HAT_ZERTIFIZIERUNG`, `NUTZT_TOOL` are registered rel types with 0 edges. A first-time user querying these gets "no data" with no hint they were renamed.

After R2 restores some of these as nodes, this phase cleans up the leftovers.

### §13.2 Schema delta

```
:DeprecatedType {
  id: 'dep_<old_name>',
  kind: 'label' | 'rel_type',
  old_name: string,
  new_name: string,
  deprecated_at: date,
  deprecated_by: migration_id,
  reason: string
}
```

### §13.3 Migration steps

```cypher
// R10.a — After R2 restores RechtlicheBedingung, ZertifizierungBewertungssystem,
//         Tool, those labels are no longer empty. The remaining empties:
//         GraphVersion (was experimental), and the 6 empty rel types.

UNWIND [
  {kind:'label',    old:'GraphVersion',                new:'(none — drop)',         reason:'Experimental versioning label, never populated'},
  {kind:'rel_type', old:'AUS_BAUWERK',                 new:'FROM_DONOR',            reason:'Phase 4.2 rename'},
  {kind:'rel_type', old:'EINGEBAUT_IN',                new:'INTO_RECEIVER',         reason:'Phase 4.2 rename'},
  {kind:'rel_type', old:'HAT_SCHADSTOFF',              new:'HAS_RISK_POLLUTANT',    reason:'Phase 3.2 split + rename'},
  {kind:'rel_type', old:'HAT_RECHTLICHE_BEDINGUNG',    new:'(restored by R2.c)',    reason:'Demoted in 2.5, restored by R2.c'},
  {kind:'rel_type', old:'HAT_ZERTIFIZIERUNG',          new:'(restored by R2.d)',    reason:'Demoted in 2.5, restored by R2.d'},
  {kind:'rel_type', old:'NUTZT_TOOL',                  new:'NUTZT_SOFTWARE',        reason:'Phase 2.5.e'}
] AS row
MERGE (d:DeprecatedType {id: 'dep_' + replace(row.old, '_', '__')})
SET d.kind = row.kind,
    d.old_name = row.old,
    d.new_name = row.new,
    d.deprecated_at = date(),
    d.deprecated_by = 'r10_a_deprecation_seed',
    d.reason = row.reason;
```

The labels themselves can be dropped from the registry once no other Cypher script references them (Neo4j retains label registration as long as the registry mentions them; deleting the last node doesn't unregister).

### §13.4 Acceptance gates

| Gate | Pass condition |
|---|---|
| `:DeprecatedType` count | ≥ 7 (cover every empty-registered label/type) |
| Discoverability: `MATCH (d:DeprecatedType) RETURN d.old_name, d.new_name` | returns a clean lookup table |
| Empty labels other than the documented ones | 0 |

### §13.5 Rollback

`MATCH (d:DeprecatedType) DETACH DELETE d;`

---

## §14 Open decisions (block specific phases)

These decisions are mine to recommend but yours to make. The phases referencing them cannot proceed without resolution.

| ID | Decision | Default recommendation | Blocks |
|---|---|---|---|
| D1 | Keep `evidence_confidence='belegt'` on registry-derived edges, or downgrade to `teilweise_belegt`? | Downgrade unless the exact actor-row link is copied onto the fact. `akteursliste_master.md` itself is lineage, not evidence. | R1 |
| D2 | After R2 lands, delete the mirror properties (`lca_module_scope`, `certifications`, `legal_conditions`) or keep them? | Delete after one ingestion cycle confirms the loader writes nodes, not properties. | R2 follow-up |
| D3 | Add `:Bauteilgruppe-[:DERIVED_FROM]->:Bauteilgruppe` for cross-project chains in R3? | Defer to R3.5; current data is too sparse to motivate. | R3 |
| D4 | Add `:Kennwert.category` enum, or discriminate only by `kennwert` string? | Add explicit enum. Better for indexing. | R4 |
| D5 | Lift `quality_tier_facts` to `:Kennwert` too? | No; it's an internal audit fold, not a measurement. | R4 |
| D6 | Use secondary labels `:BauteilgruppeBatch` / `:BauteilgruppeCategory`, or only `bg_kind` property? | Property only. Secondary labels add registry noise without query benefit at this scale. | R5 |
| D7 | Schema language: English (Direction A) or German (Direction B)? | English. Aligns with ReuseRule, with the EU literature, and with an international audience. | R6 |
| D8 | Classify `q_refair_bordeaux_md` as `:Programm` or `:Marktmodell`? | `:Programm`. REFAIR is a research consortium output, not a market actor. | R7.b |
| D9 | Add `Quelle.text_content` (full markdown text) to support text-matching curation in R9.b? | Yes for `case_markdown` Quelle. Allows automated stub→participant promotion based on dossier text. | R9.b |
| D10 | Does R8's audit policy change apply retrospectively (re-tier under source_curated only)? | Yes. The honest tier-1 cohort is the goal. Expect 3–5 projects, not 11. | R8 |

---

## §15 Sequencing and parallelism

```
        R1 (evidence honesty)
         │
         ▼
        R2 (restore demoted labels)   ◄── independent of R1; can run in parallel
         │
         ▼
        R3 (structural edges) ◄────── independent of R1/R2
         │
         ▼
        R4 (Kennwert)        ◄────── depends on R1 (for evidence_origin)
         │
         ▼
        R5 (BG disambiguation) ◄──── independent, can run anytime after baseline
         │
        R6 (language unification) ◄─ run last; touches everything
         │
        R7 (loader hardening) ◄───── independent, but R7.c uses R4's :Kennwert schema
         │
        R8 (audit relationship) ◄─── enables honest re-tiering; depends on R1
         │
        R9 (actor model) ◄────────── independent
         │
        R10 (deprecated cleanup) ◄── run after R2 (which restores some empties)
```

**Recommended order:** R1 → R3 → R5 → R10 (the four small ones); then R2 → R4 → R7; then R8 → R9; then R6 last (language). Each can be a single commit, each is rollback-able, total ≈ 10 commits.

---

## §16 What success looks like

After all 10 phases:

| Question | Expected new answer |
|---|---|
| "Which projects have human-curated reuse evidence?" | The honest count — likely 3–7 projects, **not** 266 rows. Tier-1 cohort shrinks accordingly. |
| "Which buildings does Stuttgart 210 involve?" | One-hop traversal via `:HAS_BAUWERK`. |
| "Which rules apply to Holbein Gardens?" | One-hop via `:ReuseRule-[:RELEVANT_FOR]->(:Projekt)`. |
| "Show me reuse share across tier-1 projects, sortable by %" | `MATCH (p:Projekt)-[:HAT_KENNWERT]->(kw:Kennwert {kennwert:'reuse_share'}) RETURN p, kw.wert ORDER BY kw.wert DESC` — pure graph. |
| "What pollutant evidence is documented (not inferred) for project X?" | `MATCH (p)-[:REQUIRES_VERIFICATION_FOR]->(:Schadstoff) WHERE r.evidence_origin='source_curated'` — likely zero, and that's the honest signal. |
| "What data quality issues concern this Bauteilgruppe?" | `MATCH (i:DataIssue)-[:CONCERNS]->(bg:Bauteilgruppe {id:'…'}) RETURN i` |
| "Which actors are verified vs stub for this project?" | `MATCH (a:Akteur)-[r:BETEILIGT_AN|STUB_PROJECT_LINK]->(:Projekt {id:'…'}) RETURN type(r), a` — type makes it explicit. |
| "Which BG is a batch and which is a category?" | `MATCH (bg:Bauteilgruppe) RETURN bg.bg_kind, count(bg)` |

The graph will likely **look worse** by raw audit-PASS counts after these phases. That's the point. The current numbers are right because the rules are bent to fit them. The post-R1–R10 numbers will be right because the data is what it is.

---

## §17 Risks and what could go wrong

| Risk | Mitigation |
|---|---|
| R1 breaks downstream queries that filter `evidence_origin='curated'`. | Inventory all such queries (in `_neo4j/review/round_002_followup/*.cypher` etc.); update to `IN ['source_curated','registry_derived']` where appropriate. |
| R2 re-creates nodes that the original Phase 2.5 had a good reason to delete. | Read each deletion's deleted/*.jsonl journal; if the reason was "data was wrong", do not restore as a node — record as `:DataIssue` instead. |
| R3's `:HAS_BAUWERK` edge double-counts when a building is both donor and receiver. | The `role` property distinguishes; aggregations must `DISTINCT` on (p, b). |
| R4's strip of `*_facts` JSON properties (R4.b) loses information if the JSON had keys not covered by `:Kennwert`. | Journal every JSON-string byte-by-byte before strip; reversible. |
| R6 language unification is incompatible with existing loaders. | Defer R6 until R7's loader hardening lands; R7 includes the dossier-side translation layer. |
| R7's text-matching for stub-promotion has false positives (`a.name='Rotor'` matches Rotor-the-band). | Use full-name matching with word boundaries; manual review queue for borderline cases (the R8 `:DataIssue` flow). |
| R8 changes tier-1 count visibly; users may panic. | Communicate the change loudly; document that the previous count was an artefact of Repair D. |

---

## §18 What this plan deliberately does NOT do

- Does not delete the radical-quality-reset migrations. They remain in git history; the reset's deletions remain in `deleted/*.jsonl` journals. R2 reads those journals.
- Does not change the `mit-bestand` database name or location.
- Does not propose a new graph database or rewrite the schema from scratch. All changes are incremental.
- Does not propose new visualization or BI tooling. Graph-only.
- Does not address the 4-empty-labels by aggressively dropping them from the Neo4j label registry (which would require admin commands and is not always possible without DB restart).
- Does not propose changes to `_scripts/apply_neo4j_review_patch.py` beyond what R2/R3 need. The applier is its own concern.

---

## §19 Review checkpoint

Once you've read this:

1. Tell me which of D1–D10 you want to decide now.
2. Tell me which phases to **drop** (you may decide R6 is too risky, or R8 too philosophical).
3. Tell me which phases to **reorder** (e.g., if you'd rather do R7 first because new dossiers are coming).
4. Tell me what's **missing** from this plan that the three layers should have flagged.

I'll then produce a phase-by-phase execution plan in the format of the existing radical_quality_reset plans — one phase per file under `_neo4j/intake/runs/<run-id>/plans/` — with full Cypher, runner scripts, and acceptance gates ready to hand off to a migration agent.

---

**End of REVIEW_BASED_PLAN.md — 2026-05-21 draft.**
