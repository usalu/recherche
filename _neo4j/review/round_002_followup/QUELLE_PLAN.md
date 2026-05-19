# Quelle plan — source tracking across the graph

Companion to [NAMING_AND_PROPERTIES_PLAN.md](NAMING_AND_PROPERTIES_PLAN.md). This document handles the **source-coverage** work separately so the naming + property plan stays focused on names and properties.

**Decision basis:** "whatever source is available should be connected." Every node that can be traced to an originating source gets a `BELEGT_IN` edge. Every inferred relationship carries a `r.source` property.

---

## 0. Execution context

**State at plan freeze:** 2 296 nodes / 16 822 relationships on `mit-bestand`. Verify before starting:

```cypher
MATCH (n) WITH count(n) AS nodes
MATCH ()-[r]->() WITH nodes, count(r) AS rels
RETURN nodes, rels;
// Expected: 2296 / 16822.
```

Follows the same standard apply-tool protocol described in [NAMING_AND_PROPERTIES_PLAN.md §0](NAMING_AND_PROPERTIES_PLAN.md): backup → generate patch → dry-run → live apply → verify → update [rollback.md](rollback.md) → commit (3-word subject).

**Scheduling:** runs **after Phase P** of the naming/property plan. Independent of it — can be moved earlier if needed, but Phase O (BG rename) is the riskiest moment, so finishing all naming first reduces context.

---

## 1. The two source channels (recap)

| Channel | Mechanism | Used for |
|---|---|---|
| **1 — Node-level** | `(n)-[:BELEGT_IN]->(:Quelle)` | Case-specific facts (a project, a building, a Bauteilgruppe, an actor) AND vocabulary nodes when an introducing source exists. |
| **2 — Edge-level** | `r.source` property on the relationship | Inferred / propagated edges (Phase G archive scan, Phase I orphan rescue, Round 003 propagation, future similar passes). |

Both stay simple: **no enum split, no source_detail column, no source property on fact nodes**. The principle is "the link itself is the value."

---

## 2. Current coverage (2026-05-19)

### Channel 1 — `BELEGT_IN` coverage per label

**Good (≥ 80 %):**

| Label | Coverage | Avg Quellen/node |
|---|---|---:|
| Projekt | 99/99 (100 %) | 4.0 |
| Bauteilgruppe | 306/306 (100 %) | 1.0 |
| Bauwerk | 196/196 (100 %) | 1.0 |
| Wiederverwendungskette | 63/63 (100 %) | 1.0 |
| Stadt | 62/62 (100 %) | 1.5 |
| Akteur | 565/582 (97 %) | 1.7 |
| Land | 13/16 (81 %) | 5.4 |

**Zero (the gap):**

About 340 controlled-vocabulary nodes carry no `BELEGT_IN` — Defekt, Marktmodell, ZustandsKlasse, Akzeptanz, MatchingQualitaet, Material, Methode, Aufbereitungsverfahren, PruefungNachweis, Schadstoff, BauwerkEra, Bauproduktstatus, LebenszyklusModul, Layer, Wirtschaft, plus the structural-vocab labels Akteurrolle / Akteurtyp / Status / Nutzung / Prozessphase / Bauteiltyp / Materialgruppe / Bauobjektklasse / Bauobjektrolle / WiederverwendungsArt / Funktionswechsel / Bausystem / Bauweise / Tragwerksprinzip / Logistik / BauaufgabeIntervention / Ressourcenquelle / Beschaffungsweg / HuerdeKategorie / Norm (27 of 30) / Huerde / Leistungsanforderung / Programm (15 of 17) / Verbindungstechnik (11 of 12) / Rueckbauverfahren.

### Channel 2 — `r.source` coverage on inferred edges

Already in place for the 482+ inferred edges added across Phases G / I / J / Round 003. No gap.

---

## 3. Quelle node — quelltyp enum

| `quelltyp` value | Count today | What it represents |
|---|---:|---|
| `external_link_from_actor_registry` | 319 | URL cited in the actor registry |
| `case_markdown` | 76 | One per archive case-study `.md` |
| `external_reference` | 51 | URL / publication cited inside an archive case |
| `actor_registry_markdown` | 1 | The `akteursliste_master.md` file itself |
| **`research_markdown`** | 0 → +12 | One per research file under `_neo4j/intake/inbox/research/` (introduced by this plan) |
| **`controlled_vocab_seed`** | 0 → +1 | The contract's `controlled_vocabulary.seed.kg.jsonl` (introduced by this plan) |

After this plan, **6 quelltyp values** total. Enforce as enum at intake.

---

## 4. Phase Q.1 — create research-source Quelle nodes (12)

One Quelle per research markdown file under `_neo4j/intake/inbox/research/`. Each becomes a `BELEGT_IN` target for the vocab nodes that file introduced.

| Research file | Quelle id | quelltyp |
|---|---|---|
| `bauteilreuse_legal_regime_matrix.md` | `q_research_bauteilreuse_legal_regime` | `research_markdown` |
| `connection_techniques_bauteilreuse.md` | `q_research_connection_techniques` | `research_markdown` |
| `circular_construction_economics_kg.md` | `q_research_circular_economics` | `research_markdown` |
| `circular_construction_leistungsanforderungen.md` | `q_research_leistungsanforderungen` | `research_markdown` |
| `circular_construction_reuse_graph_gaps.md` | `q_research_reuse_graph_gaps` | `research_markdown` |
| `schadstoff_reuse_knowledge_graph_research.md` | `q_research_schadstoff_kg` | `research_markdown` |
| `energy_climate_reuse_research.md` | `q_research_energy_climate` | `research_markdown` |
| `aufbereitungsverfahren_reused_building_elements.md` | `q_research_aufbereitungsverfahren` | `research_markdown` |
| `missing_underused_norm_nodes_reuse_kg.md` | `q_research_norm_nodes` | `research_markdown` |
| `reuse_knowledge_graph_coverage_audit.md` | `q_research_coverage_audit` | `research_markdown` |
| `testing_verification_bauteilreuse_kg.md` | `q_research_testing_verification` | `research_markdown` |
| `graph_patch_validation.md` | `q_research_patch_validation` | `research_markdown` |

Each Quelle node carries: `id`, `name` (short), `name_full` (= original research filename), `quelltyp`, `source_file` (path to the file).

**Op:** 12 × `add_node`.

---

## 5. Phase Q.2 — link conceptual-vocab nodes to research Quellen (≈ 160 edges)

Each conceptual-vocab node gets a `BELEGT_IN` edge to the research file that introduced it.

| Research Quelle | Targets |
|---|---|
| `q_research_bauteilreuse_legal_regime` | 15 Bauproduktstatus + 5 Akzeptanz |
| `q_research_connection_techniques` | 12 Verbindungstechnik |
| `q_research_circular_economics` | 12 Wirtschaft + 11 Marktmodell |
| `q_research_reuse_graph_gaps` | 10 Defekt + 9 MatchingQualitaet + 6 ZustandsKlasse |
| `q_research_schadstoff_kg` | 8 Schadstoff + 6 BauwerkEra |
| `q_research_aufbereitungsverfahren` | 45 Aufbereitungsverfahren + 5 Rueckbauverfahren |
| `q_research_norm_nodes` | 27 currently-source-less Norms |
| `q_research_energy_climate` | 5 LebenszyklusModul + 6 Layer |
| `q_research_leistungsanforderungen` | 12 Leistungsanforderung |

≈ 162 `add_rel` ops.

---

## 6. Phase Q.3 — link structural-vocab nodes to controlled-vocab seed (≈ 190 edges)

Structural typology nodes (Akteurrolle, Akteurtyp, Status, Nutzung, Prozessphase, Bauteiltyp, Materialgruppe, Bauobjektklasse, Bauobjektrolle, WiederverwendungsArt, Funktionswechsel, Bausystem, Bauweise, Tragwerksprinzip, Logistik, BauaufgabeIntervention, Ressourcenquelle, Beschaffungsweg, HuerdeKategorie, Methode, PruefungNachweis, Huerde) trace to the contract's `controlled_vocabulary.seed.kg.jsonl`. Attach all of them to one Quelle.

| Quelle id | quelltyp | Targets |
|---|---|---|
| `q_controlled_vocab_seed` | `controlled_vocab_seed` | ~190 structural-vocab nodes across ~22 labels |

**Ops:** 1 × `add_node` + ~190 × `add_rel`.

Per the user's decision ("whatever source is available should be connected"), structural typology DOES get its single seed-source. This is the decision that elevates Phase Q from optional to mandatory.

---

## 7. Phase Q.4 — case-specific gap backfill (≈ 20 edges)

### 17 source-less Akteure

Most likely actor-registry entries that lack a URL — attach the registry markdown (`q_akteursliste_master` Quelle, already exists) as Quelle. Investigation per actor; if no plausible source exists, leave as-is and document.

### 3 source-less Lands

The supranational scope-pseudo nodes:
- `land_eu` — Europäische Union (Geltungsbereich)
- `land_eea` — Europäischer Wirtschaftsraum (EU+EEA)
- `land_international` — International (ISO/IEC Geltungsbereich)

These are meta-nodes, not real countries. Two options:
- Attach a `q_controlled_vocab_seed` link (treats them as part of the structural vocab) — simpler
- Leave un-sourced, document as "scope pseudo-nodes don't need Quelle" — also defensible

**Recommendation:** attach to `q_controlled_vocab_seed`. Keeps coverage uniform.

≈ 20 `add_rel` ops.

---

## 8. Phase Q.5 — Quelle property cleanup (during Phase L hygiene)

Note: this part overlaps with NAMING_AND_PROPERTIES_PLAN.md Phase L (Group B). It is **scheduled there**, executed before this Quelle plan starts, and listed here only for context:

- 319 nodes: `titel → name_full`, derive short `name`
- 127 nodes: length-check on existing `name`; promote if > 25 chars
- 1 node: drop redundant `titel` (= name)
- Unify `filename` (5) + `dateiname` (1) → `source_file`

After Phase L, every Quelle has `name` + (optionally) `name_full` + clean `quelltyp` + `source_file`.

---

## 9. Phase Q.6 — Quelle short-name strategy (hybrid)

For the ~440 Quellen needing `name` ≤ 25 chars (executed as part of Phase L):

| Quelle subset | Strategy | Example |
|---|---|---|
| `external_link_from_actor_registry` (319) | id-suffix → take last 1–2 id tokens | `q_villa_welpeloo_enschede_s3` → `Welpeloo S3` |
| `case_markdown` (76) | id-suffix (already the project slug, just clean it up) | `q_k118_kopfbau_halle_118_winterthur_md` → `K.118 md` |
| `external_reference` (51) | author + year if parseable from `name_full`; id-suffix otherwise | `[S3] Steukers, Ghyoot, Devlieger…` → `Steukers 2025` |
| (anything missed) | Fallback: truncate `name_full` to 24 chars + `…` | "Steukers, Ghyoot, Devliege…" |

Hybrid keeps automation high and readability decent. Marginal cases get truncation — acceptable for ≤ 5 % of nodes.

---

## 10. Verification queries (run after Phase Q completes)

```cypher
// Q-1: every node must have at least one BELEGT_IN edge (except Quelle itself)
MATCH (n) WHERE NOT 'Quelle' IN labels(n)
  AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) }
RETURN labels(n)[0] AS label, count(*) AS n_uncovered
ORDER BY n_uncovered DESC;
// Expected after Phase Q: 0 rows (or only orphan/stub nodes that should be cleaned up).
```

```cypher
// Q-2: every inferred rel must carry r.source
MATCH ()-[r]->()
WHERE type(r) IN [
  'HAT_DEFEKT_BEFUND','HAT_MATCHINGQUALITAET','HAT_DOMINANT_MARKTMODELL',
  'HAT_DOMINANT_AKZEPTANZ','HAT_WIRTSCHAFT','HAT_DEFEKT','HAT_MARKTMODELL'
] AND r.source IS NULL
RETURN type(r) AS rel_type, count(*) AS missing_source
ORDER BY missing_source DESC;
// Expected: 0 rows (or only the ~34 pre-Round-003 HAT_MARKTMODELL edges that predate the convention).
```

```cypher
// Q-3: every Quelle node has the required core (name + quelltyp + at least one citer)
MATCH (q:Quelle)
OPTIONAL MATCH (q)<-[r:BELEGT_IN]-()
WITH q, count(r) AS citers
RETURN q.id, q.name, q.quelltyp, citers
ORDER BY citers ASC LIMIT 30;
// Expected: every Quelle has name AND quelltyp; uncited Quellen are rare and can be reviewed.
```

```cypher
// Q-4: the quelltyp enum holds exactly the 6 expected values
MATCH (q:Quelle) RETURN DISTINCT q.quelltyp ORDER BY q.quelltyp;
// Expected: 6 rows — external_link_from_actor_registry, case_markdown,
//   external_reference, actor_registry_markdown, research_markdown,
//   controlled_vocab_seed.
```

---

## 11. Estimated totals + sequencing

| Sub-phase | Ops | Patch |
|---|---:|---|
| Q.1 — create 12 research Quellen | 12 add_node | `phase_q1.patch.jsonl` |
| Q.2 — link conceptual vocab → research | ≈ 162 add_rel | `phase_q2.patch.jsonl` |
| Q.3 — link structural vocab → seed Quelle | 1 add_node + ≈ 190 add_rel | `phase_q3.patch.jsonl` |
| Q.4 — case-specific backfill | ≈ 20 add_rel | `phase_q4.patch.jsonl` |

**Q.5 + Q.6 (Quelle property cleanup + short-name)** are executed under Phase L of the naming plan — not part of this document's execution surface.

**Total Phase Q here: ≈ 385 ops across 4 small patches.** Each follows the standard backup → patch → dry-run → live-apply protocol.

---

## 12. After Phase Q completes — coverage targets

| Label group | Target | After Phase Q |
|---|---|---|
| Case-specific (Projekt / Bauwerk / Bauteilgruppe / Wiederverwendungskette / Stadt / Akteur / Land) | ≥ 95 % BELEGT_IN | ≥ 99 % |
| Conceptual vocab (Defekt / MatchingQualitaet / etc.) | 100 % BELEGT_IN | 100 % |
| Structural typology (Akteurrolle / Status / Nutzung / etc.) | 100 % BELEGT_IN | 100 % |
| Inferred edges (HAT_DEFEKT_BEFUND etc.) | 100 % r.source | 100 % |

Every node and every inferred relationship is sourceable. Phase Q completes the source-coverage promise of the graph.
