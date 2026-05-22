# SEMANTIC REVIEW — are the cleanup decisions legit? (critical, evidence-grounded)

Independent, **adversarial** review of the `FINAL_PLAN.md` / `HANDOFF.md` decisions, measured against the
live `mit-bestand` graph on **2026-06-05**. Goal of the cleanup (user-stated): *a clean, clear graph with
**no duplications** and **concrete, connected, non-generic** information.* Verdicts below are graded
**✅ sound · ⚠️ insufficient / inconsistent · ❌ wrong / risky**, every one backed by a measured number.

> **Method.** All claims re-queried live. Baseline: 5 445 nodes · 21 403 rels · 64 in-use labels
> (66 registered) · 85 relationship types. The plan's own counts are accurate; the issues are in
> *scope, consistency and rel-type modelling*, not measurement.

---

## 0. Headline verdict
The plan is **directionally correct and the hard calls (collapse the law layer, retire inferred-regulatory
edges, apply the only sourced overlay) are well-justified.** But measured against *"no duplication / non-
generic"* it is **half a cleanup**: it dedups **labels** thoroughly while almost entirely **ignoring
relationship-type duplication**, and it is **inconsistent about the source model** (absorbs `ExternalLink`
into `Quelle` but keeps three other labels that are *also* 100 % `Quelle`). To meet the user's bar, the
plan needs to be **more aggressive on edges**, not on labels.

---

## 1. The single biggest finding — "generic" must be defined correctly
**Measured: 0 of 21 403 edges carry `source_url` or `evidence_status`.** The *entire* graph's evidence is
node-level (`BELEGT_IN`→`Quelle`); there is **no edge-level evidence anywhere**. So "every regulation edge
sourced" is currently **0 % true**, and the new overlay is genuinely the *only* edge-evidenced layer.
**✅ This strongly validates applying the overlay.**

But it also means a naïve reading of *"non-generic = has a source_url"* would condemn the **whole graph**.
The right definition, which the plan implicitly (but never explicitly) uses:

- **Generic / to-retire** = an edge that *asserts a derived/regulatory claim with no basis* — i.e.
  `evidence_confidence ∈ {inferiert, unklar}` on the **regulation** rel types. Measured: `HAT_HUERDE`
  930/930, `HAS_RISK_POLLUTANT` 658/754, `HAT_PRUEFUNG` 345/465, `HAT_LEISTUNGSANFORDERUNG` 452/452,
  `REQUIRES_VERIFICATION_FOR` 339/339. **These are correctly targeted. ✅**
- **Concrete / keep** = an *observed factual classification* (this component's status, material group,
  process phase). These lack a URL but are ground-truth observations, not inferences.

**⚠️ Action: write this definition into the plan.** Without it, the acceptance checks (T3/T5) and the word
"generic" are ambiguous, and a future agent could wrongly delete factual edges.

---

## 2. DUPLICATION the plan misses — relationship types (the biggest gap)
The plan reduces 64→~46 **labels** but sets **no target for the 85 relationship types** and leaves obvious
rel-type duplicates untouched. For *"no duplications"* this is the headline omission.

| Duplicate / overlapping rel types (measured) | Issue | Recommendation |
|---|---|---|
| `APPLIES_IN` (20) · `APPLIES_TO` (20) · `ANGEWENDET_AUF` (13) · `RELEVANT_FOR` (100) · `REGULIERT` (25) · `GILT_IN_LAND` (172) | 6 overlapping "applies/relevant/regulates" edges, EN+DE mixed | Collapse to a small fixed set: `GILT_IN_LAND` (jurisdiction) + `UNTERLIEGT_REGELWERK` (applicability). Retire the rest. |
| `HAT_DEFEKT` (32) · `HAT_DEFEKT_BEFUND` (25) | two defect edges for one axis | Merge to `HAT_DEFEKT`. |
| `HAT_WIRTSCHAFT` (41) · `HAT_WIRTSCHAFTSASPEKT` (11) | both economy; `Wirtschaft` is being deleted anyway | Delete both with the label. |
| `HAT_BAUPRODUKTSTATUS` (34) · `HAT_TYPISCHEN_BAUPRODUKTSTATUS` (19) | two product-status edges | Fold into the Regelwerk/property migration. |
| `NUTZT_BAUWERK` (27) · `HAS_BAUWERK` (166) | two component/project↔Bauwerk edges | Pick one; merge. |
| `HAS_SOURCE_LINK` (354) | `Quelle`↔`Quelle` pointer; S2 says "keep only as dedup pointer" — but it's also the only thing besides `BELEGT_IN` that the evidence sub-labels use | Verify it isn't a second citation mechanism; otherwise retire. |
| `HAT_TRAGWERKSPRINZIP` (68), `HAT_BAUOBJEKTKLASSE` (224), `HAT_MARKTMODELL` (370), `TEILT_LAYER` (15) | edges of merged-away labels | Must be rewired in the label merges (plan implies, never lists rel-type targets). |

**EN/DE naming inconsistency:** ~12 English rel types (`FROM_DONOR`, `INTO_RECEIVER`, `HAS_BAUWERK`,
`HAS_RISK_POLLUTANT`, `HAS_SOURCE_LINK`, `APPLIES_IN/TO`, `RELEVANT_FOR`, `BUILT_IN_ERA`,
`REQUIRES_VERIFICATION_FOR`, `IST_UNTERVERFAHREN_VON`-style) sit amid ~73 German `HAT_/LIEGT_/NUTZT_`
edges. For a "clean, clear" graph, **normalise rel-type naming to one language** (German, to match the
dominant convention) as part of the rewire. ⚠️

> **Add a rel-type target to the plan:** roughly **85 → ~55** after retirements + dedup + the overlay's
> new types. Today there is no such number, so "clean graph" is unverifiable on the edge side.

---

## 3. SOURCE MODEL — the plan is internally inconsistent (be more aggressive)
**Measured (every node, 0 standalone):** `ExternalLink` 2 610/2 610 · `SectionRef` 582/582 · `Dossier`
97/97 · `ResearchDocument` 396/396 are **all** already co-labelled `:Quelle`. And `SectionRef`/`Dossier`/
`ResearchDocument` participate in **only** `BELEGT_IN` + `HAS_SOURCE_LINK` — i.e. they add **no structural
relationship** a `quelltyp` property couldn't carry.

- The plan **absorbs `ExternalLink`→`Quelle{quelltyp:'external_link'}`** (✅ correct) but **keeps
  `SectionRef`/`Dossier`/`ResearchDocument` as separate labels** — the *identical* pattern. **❌ inconsistent.**
- Per the plan's own S1 ("one source = one `Quelle`, distinguished by `quelltyp`"), these three should
  **also** collapse: `Quelle{quelltyp:'section_ref'|'dossier'|'research_document'}`. That removes **3 more
  labels** (46→43) and unifies the source model for real.
- **Caveat to check first:** if any downstream query relies on `:SectionRef`/`:Dossier` as a label (not a
  property), keep the label but **document why** — otherwise the "unified resource standard" (Section 3 of
  HANDOFF) is violated the moment it ships. **Recommendation: collapse them; it is the aggressive, consistent move the user asked for.**

---

## 4. LABEL decisions — stress-tested
| Decision | Verdict | Evidence |
|---|---|---|
| `ExternalLink`→`Quelle` | ✅ | 2 610/2 610 are already `:Quelle`; pure co-label dedup. |
| `Tool`→`Software` | ✅ | 7/7 `Tool` are already `:Software`. |
| `Norm`/`RechtlicheBedingung`/`Geltungsbereich`/`Zertifizierungssystem`/`LCAModule`→`Regelwerk` | ✅ | All are facets of "a rule/standard"; 0 edge-evidence today; overlay supplies sourced replacement. |
| `Marktmodell`→`Beschaffungsweg` | ✅ | measured 86-BTG overlap; both are procurement axes. |
| `Tragwerksprinzip`→`Bauweise` | ✅ | 4 nodes, 25-Bauwerk overlap. |
| `Bauobjektklasse`→`Nutzung` | ⚠️ | mostly use-values, but check the non-use values (Depot/Infrastruktur) land somewhere, else info loss. |
| `Layer`/`Bauteilebene`/`MatchingQualitaet`→properties | ✅ | low-cardinality attributes, not entities. |
| Keep `SectionRef`/`Dossier`/`ResearchDocument` as labels | ❌ | see §3 — they're `Quelle` sub-types. |
| Keep `HAT_STATUS` axis as-is | ⚠️ | **88 % of 584 edges = 'Realisiert'** (near-constant). Low information; better as a `Bauteilgruppe.status` property than a label+edge axis. |
| Keep all other small vocab labels (Status, Defekt, Prozessphase, Nutzung, Materialgruppe, …) | ✅ | distribution is **meaningful, not spray** (top values 18–46 %, many distinct), so they are concrete classification axes — keep. The "~34 labels" target was wrong precisely because these are legit (see HANDOFF §0). |

---

## 5. `Wiederverwendungskette` deletion — re-examined (user said delete)
**Measured:** 14 nodes, **all sourced** (`BELEGT_IN`→`Quelle`), modelling donor→component→receiver chains.
Crucially: **0 of the 14 member `Bauteilgruppe` have a direct `FROM_DONOR`/`INTO_RECEIVER` edge** — so the
chain node is their *only* donor↔receiver link. Deleting the label therefore **loses unique, sourced reuse
facts** (not redundant data, as I first assumed). `FROM_DONOR` (245) / `INTO_RECEIVER` (278) themselves stay
(core BTG→Bauwerk edges); only `TEIL_VON_KETTE` (14) retires.

- **Verdict: ⚠️ lossy.** The delete is fine *if* the donor/receiver facts are first re-expressed as direct
  `(:Bauteilgruppe)-[:FROM_DONOR]->(:Bauwerk)` / `-[:INTO_RECEIVER]->` edges carrying the source, **then**
  the `Wiederverwendungskette` node is dropped. That honours the user's "delete the label" decision while
  keeping the 14 sourced reuse cases — exactly the "concrete, connected, non-generic" data the cleanup is
  supposed to *protect*. Recommend doing the re-expression in Phase 6 before the delete.

---

## 6. The new overlay (Regelwerk 91 / Nachweisforderung 33 / Regulierungsfrage 11)
- **Duplication: none meaningful. ✅** The 91 Regelwerke are distinct named standards (DIN/EN/ISO/…),
  already deduped in `rewire_map` (EN1090 ×5→1, etc.).
- **Granularity: ⚠️ watch the pollutant proofs.** Among the 33 `Nachweisforderung` there is one general
  `Schadstoffpruefung` **plus** ~11 specific checks (`AsbestCheck`, `KMFCheck`, `PCBCheck`, `PAKCheck`,
  `HolzschutzmittelCheck`, `Radonmessung`, `VOC_Emissionsnachweis`, `MikrobielleBelastungCheck`,
  `Formaldehyd…`, `Schwermetall/Bleifarbe`, `Schadstoffkataster`). These are legitimately distinct proof
  obligations (each maps to a specific TRGS/REACH/StrlSchG rule), but flat siblings invite confusion.
  **Recommend a parent→child link** (`Schadstoffpruefung`→specific checks) rather than 12 flat peers, so
  the proof layer reads as a hierarchy, not a duplicate set.
- Otherwise the overlay is the one fully-sourced, audited (0 problems) layer — apply it. ✅

---

## 7. What "aggressive but correct" looks like (recommended additions to the plan)
1. **Define generic precisely** (§1) and put it in T3/T5 so no factual edge is mistakenly deleted.
2. **Add a relationship-type cleanup phase** (§2): collapse the applicability sprawl
   (`APPLIES_IN/APPLIES_TO/ANGEWENDET_AUF/RELEVANT_FOR/REGULIERT`), merge `HAT_DEFEKT(_BEFUND)`,
   `NUTZT_BAUWERK`/`HAS_BAUWERK`, kill the `Wirtschaft` edges, and **set a rel-type target (~85→~55)**.
3. **Normalise rel-type naming to German** during the rewire (kill the EN/DE split).
4. **Collapse `SectionRef`/`Dossier`/`ResearchDocument` into `Quelle{quelltyp}`** (§3) for a truly unified
   source model — 3 more labels gone (→~43, or ~40 with the rel-type/status moves).
5. **Demote `HAT_STATUS` to a property** (§4) — 88 % single-valued, low information as an axis.
6. **Re-express the 14 reuse chains as direct sourced BTG→Bauwerk edges before deleting WVK** (§5).
7. Leave the meaningful small vocab labels alone — chasing "~34" by merging them would *create*
   semantic muddle, the opposite of the goal.

**Net effect if adopted:** labels 64 → **~40** (not the mythical 34, but principled), rel types
85 → **~55**, one source model, one law layer, edge-level evidence only where it's real, and the genuine
generic spray (inferred-regulatory edges) gone — while every *observed fact* is preserved. That is "clean,
clear, de-duplicated, concrete" without throwing away real data.

---

## 8. Decisions I'd reverse or change
- **❌ Keep-as-label for `SectionRef`/`Dossier`/`ResearchDocument`** → collapse to `Quelle{quelltyp}`.
- **⚠️ `Wiederverwendungskette` hard delete** → re-express donor/receiver edges first, then delete.
- **⚠️ Silent keep of `HAT_STATUS` axis** → demote to property.
- **⚠️ No rel-type plan** → add one; it's half the duplication problem.
Everything else in `FINAL_PLAN.md` survives the adversarial pass. The plan is sound at the label level and
on the regulation collapse; it just stops short of the edge-level and source-model consistency the
"no-duplication / non-generic" goal demands.
