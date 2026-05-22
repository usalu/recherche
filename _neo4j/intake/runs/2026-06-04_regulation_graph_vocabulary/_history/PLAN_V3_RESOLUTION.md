# PLAN v3 — resolution of the v2 review issues

Deep analysis of the issues raised in the review, and a concrete plan that resolves them. v3 **keeps
all of v2's good work** (deletions, rel-type dedup, guardrails, generic-definition, WVK re-express,
confidence migration) and **changes one thing**: the evidence/reference *storage model*, because v2's
"everything is a property" creates the very duplication the project exists to remove.

---

## Part A — Deep analysis

### Issue 1 (central) — "evidence = property, never node" duplicates *reused* references
**Root cause:** v2 collapses three different things into one rule:
| Thing | Example | Reused? | Relational? | Correct storage |
|---|---|---|---|---|
| One-off citation of a single assertion | "this edge's claim is backed by URL x, quote y" | no | no | **property** ✅ (v2 right) |
| A reusable **source** | a PDF/page cited by many facts (≤17 measured) | yes | no | **node** (`Quelle`), deduped |
| A named **standard/law** | "EN 1090" (URL + jurisdiction) | **heavily** | **yes** (→Land) | **node** (`Regelwerk`), deduped |

**Measured cost of flattening standards to properties (from the overlay):**
- `UNTERLIEGT_REGELWERK` = **1 272 edges → 57 standards.** As `rechtsgrundlage`+`source_url` edge props,
  the same URL is copied **84×** (ISO 20887), **74×** (EN 13830), **51×** (EU Taxonomy / Level(s) / ESPR).
- `GILT_IN_LAND` = **281 law→country edges** → a flat `jurisdiktion[]` array that **destroys the
  law↔country mapping** (can't tell which of a Nachweis's laws applies in which country).
- Net: ~1 272 duplicated URL copies + lost relation, vs. a normalized **91-node** catalog where each
  URL is stored once and `EN 1090 → Land` stays queryable.

**Why v2's `≤15-node vocabulary` rule misfires here:** it conflates *classification/tagging
vocabularies* (subjective category sets — there, >15 = sprawl/noise) with *reference catalogs* (real
named external entities — `Regelwerk`, `Quelle`, `Material`, `Akteur`). A catalog is as large as reality
and is **already the deduplicated form**; capping it forces denormalization → duplication. The cap is
right for tagging vocabs, wrong for catalogs.

**The resolving principle (one line):** **Normalize what is reused or relational (→ node, stored once);
inline what is one-off (→ property).** This is exactly what minimizes duplication — the #1 goal.

### Issue 2 — the "built & validated overlay" is stale under v2
`build_vocabulary_graph.py` / `apply_to_graph.py` create `Regelwerk` (+ overlay `Quelle`) nodes; v2
forbids both, so the dry-run-clean artifact no longer matches v2 and Phase 2 must be rewritten from
scratch. **Under v3 the overlay is kept (Regelwerk stays a node)** → the validated artifact and audit
survive with only minor edits (numeric confidence; reference cited `Quelle`). **v3 removes this issue.**

### Issue 3 — document drift (≈17 docs, 3 evidence models)
HANDOFF §3 (Quelle-node standard), v2 §0b (all-property), SEMANTIC_PROOF (v1) disagree. Readers hit
contradictions. **Fix:** one canonical plan (this v3) + one executor appendix; everything else marked
`HISTORICAL` in a single index.

### Issue 4 — EN→DE rel-type rename is high-churn / low-value
Renaming core edges (`FROM_DONOR` 245, `HAS_BAUWERK` 166) via create-copy-delete risks regressions for a
cosmetic gain. **Fix:** make naming-normalization an **optional, last, separately-approved** step, not
part of the structural cleanup.

### Issue 5 — Phase 1 is too big (delete ~3 000 nodes + migrate 19 228 edges at once)
**Fix:** split into 1a (source-layer normalization) and 1b (graph-wide `evidence_confidence`→`confidence`),
each gated and reversible.

---

## Part B — The reconciled model (v3)

**Three storage rules (replacing v2 R1/R2):**

- **E1 — One-off evidence → property.** `source_url`, `source_quote`, `confidence` (numeric 0–1),
  `evidence_status` live on the node/edge they back, when the source is specific to that single
  assertion. (= v2 R1, kept.)
- **E2 — Reusable source → `Quelle` node, deduplicated by normalized URL.** Keep **only cited** sources
  (drop the 2 242 uncited); citation = `(fact)-[:BELEGT_IN]->(:Quelle)`. **Collapse** `ExternalLink`/
  `SectionRef`/`Dossier`/`ResearchDocument` into `:Quelle {quelltyp}` (SEMANTIC_REVIEW §3 — one source
  model, fewer labels). A node cited by N sources keeps N `BELEGT_IN` edges (no array duplication).
- **E3 — Named standard/law → `Regelwerk` node, deduplicated** (the existing 91), with
  `GILT_IN_LAND`→`Land` (preserve law↔country) and `Nachweisforderung-[:GESTUETZT_AUF_REGELWERK]->Regelwerk`.
  Anchors reach the law **through the graph** (anchor→Nachweisforderung→Regelwerk), not by copying URLs
  onto 1 272 edges. `rechtsgrundlage` as an *edge property* is used **only** for a net-new standard that
  has no `Regelwerk` node yet (then promote it to a node if it recurs).

**Vocabulary governance (replacing v2's flat ≤15):**
- **Tagging vocabularies** (subjective categories): `Regulierungsfrage` (11), `Nachweisforderung` (→27,
  drop <4-edge), Huerde categories, … — keep small & heavily reused (the ≤~15 spirit). ✅
- **Reference catalogs** (real named entities): `Regelwerk` (91), `Quelle` (cited), `Material`, `Akteur`,
  … — **no cap**; deduplication *is* the cleanliness criterion (one node per real thing).

**Everything else from v2 is adopted unchanged:** the precise "generic" definition; retiring the
inferred-regulatory edges; delete-over-migrate for legacy regulation edges **(but migrate net-new to a
`Regelwerk` node, not a property)**; rel-type dedup + target; WVK re-express-then-delete; HAT_STATUS→
property; Tier-F deletions; all guardrails (G3.x/G4.x) and acceptance gates (T-series).

---

## Part C — Phase plan (v3 = v2 phases, with the model change applied)

| Phase | v3 action (Δ from v2 in **bold**) |
|---|---|
| **0** Backup & encoding | unchanged (full backup; fix mojibake in props; array-safe accept query). |
| **1a** Source-layer normalization | drop 2 242 **uncited** `Quelle`; **collapse `ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument` → `:Quelle{quelltyp}`** (keep cited as nodes); dedup `Quelle` by URL; **keep `BELEGT_IN` as the citation edge**; delete `OntologyAnchor`+`ANCHORED_BY`; retire `HAS_SOURCE_LINK` (or keep only as Quelle-dedup pointer). **(No source→property flattening; no array duplication.)** |
| **1b** Confidence migration | `evidence_confidence`→numeric `confidence` graph-wide (v2 mapping), drop categorical. Gated separately from 1a. |
| **2** Apply overlay | **keep `build/apply` ~as-is: create `Regelwerk`(91)+`Regulierungsfrage`(11)+`Nachweisforderung`(27, drop <4) nodes + the backbone edges incl. `GILT_IN_LAND`/`GESTUETZT_AUF_REGELWERK`/`UNTERLIEGT_REGELWERK`.** Only edits: numeric `confidence`; cite reused sources via `BELEGT_IN`→existing `Quelle`. (Validated overlay survives.) |
| **3** Legacy regulation collapse | delete-over-migrate (v2 R3) **but net-new standards become a `Regelwerk` node** (`MERGE` on id), never a property/`Norm`/`GAP_*`. Delete the 6 legacy labels. |
| **4** Schadstoff re-evidence | unchanged (era+material, condition routing, no silent loss, G4.x guardrails). |
| **5** Pruefung dedup + Leistung consolidate | unchanged (`ERFUELLT_NACHWEIS` before retiring `HAT_PRUEFUNG`). |
| **6** Huerde B-clean + WVK re-express + Tier-F | unchanged; Huerde sources as `BELEGT_IN`→`Quelle` (not array). |
| **7** Consolidate axes | unchanged (Marktmodell→Beschaffungsweg, Tragwerksprinzip→Bauweise, Bauobjektklasse→Nutzung, Layer/Bauteilebene/MatchingQualitaet→props, HAT_STATUS→prop). |
| **8** Rel-type dedup | unchanged structurally (collapse applicability sprawl, merge HAT_DEFEKT(_BEFUND), NUTZT_BAUWERK/HAS_BAUWERK; target 85→~50). **EN→DE rename = optional, separately approved, last.** |
| **9** Final review | v2 T-series **minus the "Regelwerk=0 / Quelle=0" gates**; **plus**: cited `Quelle` retained (0 lost evidence vs snapshot), `Regelwerk` is a deduped catalog (no duplicate standard ids), no URL stored >1× as a property where a node exists. |

## Part D — Revised targets (v3)
| Metric | Now | v2 target | **v3 target** | why v3 |
|---|---|---|---|---|
| Nodes | 5 445 | ~2 450 | **~2 700** | keep ~739 cited `Quelle` + 91 `Regelwerk` as deduped nodes (drop 2 242 uncited) |
| Labels | 64 | ~38 | **~40** | source sub-labels collapse to `Quelle`; `Regelwerk` stays (+) |
| Reltypes | 85 | ~50 | **~50** | same dedup; keep `BELEGT_IN`/`GILT_IN_LAND`/`GESTUETZT_AUF_REGELWERK` |
| `evidence_confidence` edges | 19 228 | 0 | **0** | same migration |
| Generic regulation edges | ~2 940 | 0 | **0** | same |
| Duplicated standard/source URLs | — | **~1 272 (as props)** | **0 (normalized as nodes)** | the core fix |

## Part E — Decisions for you (the one real fork)
1. **Adopt v3's reconciled model** (Regelwerk + cited Quelle as deduped nodes; one-off evidence as
   property)? — **Recommended**; it's the lower-duplication, less-rework, fidelity-preserving option.
   *Or* keep v2's all-property model knowingly accepting the ~1 272 duplicated URLs + lost law↔country
   relation (valid only if you specifically want the simpler shape over the no-duplication goal).
2. **Collapse `SectionRef`/`Dossier`/`ResearchDocument` → `Quelle{quelltyp}`?** Recommended yes (consistent),
   unless a downstream query needs those labels — then document why.
3. **EN→DE rel-type rename:** do it (last, optional) or skip? Recommend **skip/defer** (churn vs value).

On approval I will: (1) collapse the docs to **this v3 as canonical** + mark the rest historical;
(2) make the small overlay-script edits (numeric confidence, Quelle reuse) and re-run the dry-run/audit;
(3) start Phase 0 + 1a.
