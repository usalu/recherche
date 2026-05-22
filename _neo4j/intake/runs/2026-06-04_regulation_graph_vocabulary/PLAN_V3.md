# PLAN v3 — canonical, whole-graph, breakability-aware

**Supersedes `FINAL_PLAN.md`, `FINAL_PLAN_V2.md`, `PLAN_V3_RESOLUTION.md` and the HANDOFF phase list.**
Model locked below (incorporates the user decision: **no `Quelle` node**). Every DB write is gated per
phase. Written for the *whole graph*, ordered so nothing breaks.

## 0. The locked model (one rule each)
- **M1 — Sources are PROPERTIES, never a node.** No `Quelle`, `ExternalLink`, `SectionRef`, `Dossier`,
  `ResearchDocument`. A node's sources → `source_urls[]` (+ `source_titles[]`); a single assertion's
  source → `source_url`/`source_quote` on that edge. (User decision — accepts that a source URL may
  repeat across arrays; sources are not heavily relational, so this is acceptable.)
- **M2 — A law/standard IS a node: `Regelwerk` (the 91).** Reused by *pointing*
  (`Nachweisforderung-[:GESTUETZT_AUF_REGELWERK]->Regelwerk-[:GILT_IN_LAND]->Land`); its official page is
  a `source_url` *property on the card*. Kept as a node because it is **heavily reused AND relational**
  (carries jurisdiction) — flattening it would copy one URL up to **84×** and destroy the law↔country
  link. Standards = the one reference catalog that stays a node.
- **M3 — Confidence is numeric** (`confidence` 0–1); the categorical `evidence_confidence` is removed.
- **M4 — "Generic" = an inferred regulatory edge** (`evidence_confidence ∈ {inferiert,unklar}` on the
  regulation rel types). Observed factual classifications (status, material, phase…) are **kept** even
  without a URL — ground truth, not inference. Never delete those as "generic".

> Consistency: "sources are properties; a law is a node that *has* a source property."

---

## 1. Whole-graph map (decisions per layer, not per node)
The 64 labels / 85 rel-types are six layers around two hubs (`Projekt`, `Bauteilgruppe`):

| Layer | Members (examples) | Decision |
|---|---|---|
| **Spine (hubs + structure)** | Projekt, Bauteilgruppe, Bauwerk, Akteur, Programm, Materialdepot; HAT_BAUTEILGRUPPE, HAS_BAUWERK, NUTZT_MATERIAL, HAT_BAUTEILTYP, BETEILIGT_AN, FROM_DONOR, INTO_RECEIVER, LIEGT_IN_LAND/STADT | **KEEP intact.** Everything hangs off this. |
| **Factual attributes** | Material, Materialgruppe, Bauteiltyp, Nutzung, BauwerkEra, Defekt, ZustandsKlasse, Bauweise(+Tragwerksprinzip), Bausystem, Verbindungstechnik, Prozessphase, Rueckbau-/Aufbereitungsverfahren, Methode, Beschaffungsweg(+Marktmodell), Geschaeftsmodell, Akteurtyp/-rolle, Ressourcenquelle, Wiederverwendungsergebnis, Status→prop | **KEEP** (valid without a URL); merge measured duplicates; demote low-info (Status, Layer, Bauteilebene, MatchingQualitaet) to **properties**. |
| **Regulation (evidenced)** | NEW Regulierungsfrage(11), Nachweisforderung(27), **Regelwerk(91, node)** — replaces Norm/RechtlicheBedingung/Bauproduktstatus/Geltungsbereich/Zertifizierungssystem/LCAModule | **One evidenced law layer** replaces the 6 old law-labels. |
| **Domain entities under regulation** | Schadstoff(13), PruefungNachweis(120→deduped methods), Leistungsanforderung(46→~20) | **KEEP + clean** (re-evidence Schadstoff; methods hang under Nachweisforderung). |
| **Evidence/sources** | Quelle + sub-labels (ExternalLink/SectionRef/Dossier/ResearchDocument), BELEGT_IN, HAS_SOURCE_LINK | **DELETE the whole layer → `source_urls[]` properties** (M1). |
| **Noise / scaffolding** | Akzeptanz, OntologyAnchor(+ANCHORED_BY), HuerdeKategorie, Wirtschaft, STUB_PROJECT_LINK, GEHÖRT_ZU, Huerde-regulatory-half, all `inferiert` regulation edges, Wiederverwendungskette(after re-express) | **DELETE** (after re-expressing WVK donor/receiver facts). |

Targets: **5 445→~2 450 nodes · 64→~38 labels · 85→~50 reltypes · 0 duplicated *standard* URLs ·
0 generic regulation edges · 0 `evidence_confidence`.** (Source URLs may repeat in arrays — accepted.)

---

## 2. ⭐ Relations & breakability (think before touching anything)

### 2.1 Load-bearing — must survive every phase untouched
`Projekt–HAT_BAUTEILGRUPPE→Bauteilgruppe`, `–HAS_BAUWERK→Bauwerk`, `Bauteilgruppe–NUTZT_MATERIAL→Material`,
`–HAT_BAUTEILTYP→Bauteiltyp`, `Akteur–BETEILIGT_AN→Projekt`, `FROM_DONOR`/`INTO_RECEIVER`,
`LIEGT_IN_LAND/STADT`, and the new `anchor→Nachweisforderung→Regelwerk→Land`. **No phase deletes/renames
these.** T1 asserts their counts unchanged.

### 2.2 Blast-radius of each operation (a node delete also removes all its edges)
| Operation | Removes | Breakability | Safety rule |
|---|---|---|---|
| **Delete source layer** (Quelle+4 sublabels, BELEGT_IN 2 971, HAS_SOURCE_LINK 354) | all node provenance | **HIGH** — Dossier aggregates sources for Akteur(429)/BTG(287)/Bauwerk(188)/Kennwert(162); lost if deleted before copy | **extract `source_urls[]` onto every cited node first; verify ≥ pre-delete; then DETACH DELETE.** Snapshot first. |
| Drop uncited Quelle (2 242) | nothing (in-degree 0) | LOW | verify in-degree 0 |
| Delete OntologyAnchor/Akzeptanz | ANCHORED_BY 609 / nothing | LOW | scaffolding/orphan |
| Retire `inferiert` regulation edges (HAT_HUERDE 930, HAS_RISK_POLLUTANT 754, HAT_PRUEFUNG 465, HAT_LEISTUNGSANFORDERUNG 452) | edges only (nodes kept) | LOW–MED | build sourced replacement **first** |
| Merge label A→B (Marktmodell→Beschaffungsweg, Tragwerksprinzip→Bauweise, Bauobjektklasse→Nutzung, Tool→Software) | A's edges if not redirected | MED | **redirect edges→B, verify, then delete A** |
| Demote to property (Status, Layer, Bauteilebene, MatchingQualitaet) | edge after copy | MED | **copy value→property, verify, then delete edge** |
| Legacy regulation collapse (Norm/RechtlicheBedingung/…) | old edges+labels | MED | delete where overlay covers (a); else **migrate to a Regelwerk node** (b) — never a `Norm`/`GAP_*` node |
| **Delete Wiederverwendungskette (14)** | TEIL_VON_KETTE 14 + the only donor/receiver link for 14 BTG | **HIGH** — unique sourced facts lost | **re-express as direct FROM_DONOR/INTO_RECEIVER (with source prop) first** |
| Confidence migration (19 228 edges) | a property | MED (scale) | own gated step; reviewed mapping; reversible |
| EN→DE rename of spine edges (FROM_DONOR 245, HAS_BAUWERK 166) | create+copy+delete on spine | **HIGH** | **optional, last, separately approved — recommend skip** |

### 2.3 Ordering constraints (wrong order breaks things)
1. Backup → 2. Encoding fix (before name matching) → 3. **Extract sources to properties before deleting
the source layer** → 4. **Apply overlay before retiring legacy/`inferiert` regulation edges** →
5. **Schadstoff era+material spine before retiring HAS_RISK_POLLUTANT** → 6. **`ERFUELLT_NACHWEIS` before
retiring HAT_PRUEFUNG** (65/120 methods hang only off it) → 7. **Re-express WVK before deleting it** →
8. **Redirect merged-label edges before deleting the label** → 9. Rel-type dedup after label merges →
10. Verify last.

### 2.4 Standing safety rules (every phase)
Dry-run → review → commit · snapshot-before-delete (`phaseN_before.json`) · tag (`review_run`/
`source_scope`) · idempotent `MERGE` · per-phase rollback + Phase-0 full backup · **never delete before
the unique info is re-expressed and verified.**

---

## 3. Phases (ordered by §2.3; each gated, reversible)
| # | Phase | Core action | Risk | Depends on |
|---|---|---|---|---|
| 0 | Backup + encoding | full backup; fix mojibake in props (array-safe) | LOW | — |
| 1a | **Sources → properties** | extract `BELEGT_IN`+Dossier aggregation → `source_urls[]`/`source_titles[]` on cited nodes; verify; `DETACH DELETE` Quelle+4 sublabels+BELEGT_IN+HAS_SOURCE_LINK; delete OntologyAnchor+ANCHORED_BY | HIGH | 0 |
| 1b | Confidence migration | `evidence_confidence`→numeric `confidence` graph-wide; drop categorical | MED | 0 |
| 2 | Apply overlay | create **Regelwerk(91)**+Regulierungsfrage(11)+Nachweisforderung(27) + backbone + anchor edges; evidence as **properties** (numeric confidence); **no source nodes** | LOW (additive) | 1a |
| 3 | Legacy regulation collapse | delete-over-migrate; net-new → a **Regelwerk node**; delete the 6 old labels | MED | 2 |
| 4 | Schadstoff re-evidence | enrich existing TYPISCH_BEI_ERA+MATERIAL; era+material spine; condition routing; retire HAS_RISK_POLLUTANT/REQUIRES_VERIFICATION_FOR where replaced; rest→`screening_unverified` | MED | 2 |
| 5 | Pruefung + Leistung | dedup pn_/pr_; add ERFUELLT_NACHWEIS; retire HAT_PRUEFUNG/HAT_LEISTUNGSANFORDERUNG | MED | 2 |
| 6 | Huerde B-clean + WVK re-express + Tier-F | 11 evidenced barriers (sources as props); re-express WVK→FROM/INTO then delete; delete Akzeptanz/STUB/GEHÖRT_ZU/Wirtschaft/MatchingQualitaet→props | MED–HIGH | 1a, 2 |
| 7 | Consolidate attribute axes | Marktmodell→Beschaffungsweg, Tragwerksprinzip→Bauweise, Bauobjektklasse→Nutzung; demote Status/Layer/Bauteilebene→props; Tool→Software | MED | — |
| 8 | Rel-type dedup | collapse applicability sprawl (APPLIES_*/ANGEWENDET_AUF/RELEVANT_FOR/REGULIERT), merge HAT_DEFEKT(_BEFUND), reconcile NUTZT_BAUWERK/HAS_BAUWERK; target ~50. **EN→DE rename optional/last** | MED (HIGH if rename) | 7 |
| 9 | Verification | T1–T9 | — | all |

(Exact per-phase ops + acceptance queries: `DETAILED_PLAN.md` / `FINAL_PLAN_V2.md` §2, **with the v3
change applied: sources→properties (no Quelle), Regelwerk stays a node.**)

---

## 4. Verification (Phase 9 — every check green = done)
- **T1 Spine intact:** counts of HAT_BAUTEILGRUPPE, HAS_BAUWERK, NUTZT_MATERIAL, HAT_BAUTEILTYP,
  BETEILIGT_AN, FROM_DONOR, INTO_RECEIVER **unchanged** vs Phase-0 baseline.
- **T2 Sources are properties:** `Quelle`/`ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument`=0;
  `BELEGT_IN`/`HAS_SOURCE_LINK`/`ANCHORED_BY`=0; **every formerly-cited node now has `source_urls`**
  (0 evidence lost vs P1 snapshot).
- **T3 No standard duplication:** `Regelwerk` deduped (no two share id/normalized-URL); **0 standard URL
  stored as a property where a Regelwerk node exists** (anchors point, not copy); Regulierungsfrage=11,
  Nachweisforderung=27.
- **T4 One law layer:** Norm/RechtlicheBedingung/Geltungsbereich/Zertifizierungssystem/LCAModule/
  Bauproduktstatus=0.
- **T5 Confidence:** 0 edges with `evidence_confidence`; evidence-bearing edges have numeric `confidence`;
  edges with `evidence_status` have `source_url`.
- **T6 No generic spray:** HAT_HUERDE/HAS_RISK_POLLUTANT/HAT_PRUEFUNG/HAT_LEISTUNGSANFORDERUNG=0 (or only
  the reported `screening_unverified` set).
- **T7 No data loss:** WVK's 14 BTG now have direct sourced FROM_DONOR/INTO_RECEIVER; phase snapshots reconcile.
- **T8 No duplicate edges / self-loops:** parallel `(a)-[t]->(b)` count>1 = 0; 0 regulation self-loops.
- **T9 Counts & integrity:** ~38 labels, ~50 reltypes, ~2 450 nodes; every kept label ≤2 hops from
  Projekt/Bauteilgruppe; `audit_edges.py` 0; `_gap_survey.py` 0.

---

## 5. Smart calls already made (don't re-litigate)
- Keep the meaningful small vocabularies (Defekt, Prozessphase, Nutzung, …) — distinct axes, not
  duplication. Target ~38, **not** the mythical 34.
- The win is **no duplication + everything sourced-or-factual**, not the smallest possible graph.
- Spine edges need no URL — they're observed structure, not inference.

## 6. Decisions — LOCKED (2026-06-05)
1. **`Regelwerk` stays a node** (M2). ✅
2. **Sources → properties, no `Quelle`** (M1). ✅
3. **EN→DE rel rename — SKIPPED** (drop Phase 8's rename sub-step; structural rel-type dedup still runs). ✅
4. **Phase 4/6 — do the per-project `case_documented` extraction now** (read each project's saved sources
   to record the pollutants/barriers it actually documents; `taxonomy_derived` only as fallback). ✅

Execution: v3 is canonical (v1/v2 marked historical). Per-phase, dry-run → show → commit, pausing for
go-ahead before each destructive step. Starting at **P0** (backup + encoding), then **P1a** after its
dry-run is reviewed.
