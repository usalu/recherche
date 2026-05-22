> ⚠️ **HISTORICAL — superseded by `PLAN_V3.md`** (2026-06-05). v3 keeps v2's cleanup but changes the
> evidence model: **sources → properties (no `Quelle` node), but `Regelwerk` stays a node.** Read v3.

# FINAL PLAN v2 — clean, evidence-first, de-duplicated `mit-bestand`

**Canonical execution plan. Supersedes `FINAL_PLAN.md` (decisions) and the phase list in `HANDOFF.md`.**
Incorporates the live-verified corrections (2026-06-05) and the adversarial `SEMANTIC_REVIEW.md`.
Decisions are locked; **every DB write is gated per phase — nothing commits without explicit go-ahead.**

Priorities (in order): **(1) evidence is a property (node/edge), never a source node · (2) concrete &
connected over generic · (3) no duplication (labels, edges *and* vocabularies) · (4) every added node
type = a controlled vocabulary ≤15, heavily reused · (5) hangs off `Projekt`/`Bauteilgruppe`.**
Aggressive where the data justifies it; never lossy without first re-expressing the fact as a property.

---

## 0. Verified baseline (live `mit-bestand`, 2026-06-05)
- **5 445 nodes · 21 403 relationships · 64 in-use labels (66 registered) · 85 relationship types.**
- **0** edges carry `source_url`/`evidence_status` (all evidence is node-level `BELEGT_IN`→`Quelle`).
- **19 228 / 21 403** edges carry the categorical `evidence_confidence`.
- Overlay **not yet applied**. Mojibake present in node props *and* in reltype names (e.g. `GEHÖRT_ZU`).

### Targets (corrected & principled — updated 2026-06-05 for the property-based evidence model)
| Metric | Now | Target | Note |
|---|---|---|---|
| Nodes | 5 445 | **~2 450** | the entire source-node layer (2 981 `Quelle`, 75 % uncited) is deleted; evidence → properties |
| In-use labels | 64 | **~38** | incl. deleting the 5 evidence labels (`Quelle`/`ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument`); **no `Regelwerk` label added** |
| Relationship types | 85 | **~50** | + rel-type dedup; minus `BELEGT_IN`/`HAS_SOURCE_LINK`/`UNTERLIEGT_REGELWERK`/`GESTUETZT_AUF_REGELWERK` (folded into properties) |
| Edges with `evidence_confidence` | 19 228 | **0** | migrated to numeric `confidence` graph-wide |
| Generic regulation edges | ~2 940 | **0** | retired/replaced by sourced rules |
| Source/evidence stored as **nodes** | 2 981 | **0** | **all** `source_url`/`evidence_status`/standard-citation are **node or edge properties** |
| Added node-type vocabularies > 15 nodes | (Regelwerk 91) | **0** | every added vocab ≤ 15 nodes & heavily reused (see §model) |

### Definition of "generic" (must hold for all acceptance checks)
- **Generic → retire/replace:** an edge asserting a *derived/regulatory* claim with no basis, i.e.
  `evidence_confidence ∈ {inferiert, unklar}` on the **regulation** rel types (`HAT_HUERDE`,
  `HAS_RISK_POLLUTANT`, `HAT_PRUEFUNG`, `HAT_LEISTUNGSANFORDERUNG`, `REQUIRES_VERIFICATION_FOR`).
- **Concrete → keep:** an *observed factual classification* (status, material group, process phase, …).
  Lacking a URL is fine for observations; these are ground truth, not inference. **Never delete these as
  "generic".**

---

## 0b. ⭐ Evidence & vocabulary model (the core correction, locked 2026-06-05)
Two hard rules, both confirmed with the user.

### R1 — Evidence is a PROPERTY, never a node. No source-node layer.
- `source_url`, `source_quote`, `evidence_status`, `confidence`, `accessed_at`, and **the specific
  standard citation** (`rechtsgrundlage` = e.g. "EN 1090", with its URL) live as **properties on the
  node or edge they evidence** — never as a separate node.
- **Delete the entire source-node layer:** `Quelle`(2 981), `ExternalLink`(2 610), `SectionRef`(582),
  `Dossier`(97), `ResearchDocument`(396) — *after* extracting their evidence onto the cited node/edge.
  (Measured: **2 242 / 2 981 `Quelle` are uncited** → they evidence nothing → just dropped.)
- A node cited by several sources (max measured **17**) gets an **array** property `source_urls[]`
  (+ optional `source_titles[]`). Edge evidence stays single-valued per S3 keys.
- `BELEGT_IN` (2 971) and `HAS_SOURCE_LINK` (354) are **retired** — they only existed to point at source
  nodes that no longer exist.

### R2 — Every ADDED node type is a controlled vocabulary ≤ 15, heavily reused, never generic.
- `Regulierungsfrage` **11** (avg 107 edges/node, 0 sparse) ✅ keep as-is.
- `Nachweisforderung` **33 → 27**: keep all **except the 6 with < 4 edges** (`MikrobielleBelastungCheck`,
  `PAKCheck`, `Radonmessung`, `VOC_Emissionsnachweis`, `KMFCheck`, `PCBCheck`) — **fold their edges into
  `nf_schadstoffpruefung`** (the pollutant stays tracked via the `Schadstoff` node), then delete them.
  *(User rule: "keep all, only delete the ones with < 4 edges" — overrides a strict ≤15 here.)*
- `Regelwerk` **91 → ELIMINATED as a node type.** The specific standard is a citation = **evidence**, so
  by R1 it becomes a **property**:
  - on `Nachweisforderung`: `rechtsgrundlagen[]` (standard names) + `rechtsgrundlagen_urls[]`
    (from the 169 `GESTUETZT_AUF_REGELWERK` + 281 `GILT_IN_LAND` overlay edges).
  - on the regulation **edges** (`ERFORDERT_NACHWEIS`/`TRIGGERS_REGULIERUNGSFRAGE`): `rechtsgrundlage`
    + `source_url` where a specific standard backs that specific applicability.
  - **`UNTERLIEGT_REGELWERK`(1 272), `GESTUETZT_AUF_REGELWERK`(169), `GILT_IN_LAND`(overlay 281)** are
    **not created** — their information is folded into the above properties.

### R3 — Rewiring never creates uncontrolled vocabulary or duplicate data (delete-over-migrate).
- If the regulatory meaning of a legacy edge **already exists** from the overlay, **delete the legacy
  edge** — do not rewire it (rewiring would duplicate). Measured redundancy (source already overlay-
  anchored ⇒ delete): `REFERENZIERT_NORM` 43/143 · `HAT_BAUPRODUKTSTATUS` 31/34 ·
  `HAT_ZERTIFIZIERUNG` 12/12 · `HAT_RECHTLICHE_BEDINGUNG` 9/26.
- Legacy edges that carry **net-new** regulation (source not yet overlay-anchored) are preserved **as a
  property** (`rechtsgrundlage` + `source_url` on the source's regulation edge / node) — **never** by
  creating a `Norm`/`Regelwerk`/`GAP_*` node.
- **Pattern to hunt graph-wide:** any "(thing)-[legacy]->(concept-node)" where a controlled-vocab node or
  the overlay already expresses the same topic ⇒ collapse to the controlled node / property, delete the
  rest. (Applies to `REFERENZIERT_NORM`, `HAT_RECHTLICHE_BEDINGUNG`, `HAT_BAUPRODUKTSTATUS`,
  `HAT_TYPISCHEN_BAUPRODUKTSTATUS`, `HAT_GELTUNGSBEREICH`, `HAT_ZERTIFIZIERUNG`, `REGULIERT`,
  `METHODENGRUNDLAGE_NORM`.)

---

## 1. Global conventions (every phase)
1. **Dry-run → review → commit.** Each write script runs read-only first and prints before/after.
2. **Tag** new nodes `source_scope='regulation_graph_vocab_2026_06_04'`; new/modified edges
   `review_run='regulation_graph_vocab_2026_06_04'`.
3. **Snapshot before delete** (`phaseN_before.json`) via `_snapshot_predelete.py`; write `phaseN_report.json` after.
4. **Idempotent** (`MERGE` on `id`); re-running a phase is a no-op.
5. **Rollback** per phase: restore `phaseN_before.json` + `MATCH ()-[r {review_run:$run}]->() DELETE r`.
   Catastrophic: `restore_neo4j_graph_backup.py` (Phase 0 backup).
6. Neo4j 5 Cypher: `RETURN count(x) AS c` (the `AS` is required). MCP is read-only; writes use the bolt
   driver (`_scripts/neo4j_env.py`).

---

## 2. Phases (run in order; stop for go-ahead after each)

### Phase 0 — Backup & encoding normalization
- **Do:** full `backup_neo4j_graph.py`; `phase0_fix_encoding.py` re-decodes mojibake (`�`) in all string
  *properties* (dry-run → commit). Corrupt *reltype names* (e.g. `GEHÖRT_ZU`) are handled by deletion in
  Phase 6, not re-decoded (type names can't be edited in place).
- **Accept (array-safe):**

```cypher
MATCH (n)
WHERE any(k IN keys(n) WHERE
  any(v IN (CASE WHEN n[k] IS :: LIST<ANY> THEN n[k] ELSE [n[k]] END)
      WHERE v IS :: STRING AND v CONTAINS '\uFFFD'))
RETURN count(n) AS c   // must be 0
```

  + node/edge totals unchanged. **Rollback:** restore backup.

### Phase 1 — Evidence → properties; delete the source-node layer (FOUNDATIONAL, per R1)
- **Do:**
  1. **Extract evidence onto each cited node.** For every `(x)-[:BELEGT_IN]->(q:Quelle)` (and the
     `Quelle` sub-labels), collect `q.url`/`q.name`/`q.title`/`q.accessed_at_utc` into arrays on `x`:
     `x.source_urls += q.url` (dedup), `x.source_titles += coalesce(q.title,q.name)`. Multi-source nodes
     (up to 17) → arrays. (Edges that should carry the source instead of the node — e.g. a `Kennwert`'s
     measurement source — set `r.source_url` per S3 keys.)
  1b. **Preserve URL-less internal provenance (Phase 1b).** ~315 deleted `Quelle` were pointers to
     internal research/case markdown (no web URL, so not `source_urls`). Re-express their `name` as a
     `legacy_internal_provenance_docs[]` array on each cited node (2 069 citations → 1 584 nodes, e.g.
     `Plattenpalast_Berlin.md`). No source nodes restored; trail kept under the property-only model.
     **Importance:** this property is deliberately subordinate to `source_urls` — it marks internal/
     legacy document pointers, not citable web sources; consumers must always prefer `source_urls`.
     Implemented by `phase1b_restore_provenance_docs.py` (snapshot-sourced, idempotent).
  2. **Delete the entire source-node layer:** after extraction, `DETACH DELETE` all `Quelle`(2 981)
     incl. co-labels `ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument`; this also removes
     `BELEGT_IN`(2 971) and `HAS_SOURCE_LINK`(354). Uncited `Quelle` (2 242) carry no evidence → just go.
  3. Delete `OntologyAnchor`(2) + `ANCHORED_BY`(609) (scaffolding).
  4. Migrate the remaining node url-as-source props to `source_urls[]` (`ReuseRule`×20 + `OntologyAnchor`×1)
     before their owners are touched.
  5. **S4 graph-wide confidence migration (19 228 edges):** map `evidence_confidence`→numeric `confidence`
     (`belegt→0.9 · teilweise_belegt→0.6 · wahrscheinlich→0.5 · abgeleitet*→0.4 · inferiert→0.25 ·
     unsicher→0.2 · unklar→null`), then drop the categorical property. `evidence_status`+`source_url` are
     set **only** on evidence-bearing edges (S3); the factual layer gets numeric `confidence` only.
- **🛑 No-data-loss guard:** the extraction (step 1) must run and be verified **before** the delete
  (step 2). Snapshot every `Quelle` + `BELEGT_IN` to `phase1_before.json` first.
- **Accept:**
  - `MATCH (n:Quelle) RETURN count(n)`=0; same for `ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument`.
  - `MATCH ()-[r:BELEGT_IN|HAS_SOURCE_LINK|ANCHORED_BY]->() RETURN count(r)`=0.
  - **0 lost evidence:** every node that had ≥1 `BELEGT_IN` (snapshot) now has a non-empty `source_urls`
    (or an edge `source_url`); count(distinct extracted urls) ≥ count(distinct pre-delete cited urls).
  - `MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL RETURN count(r)`=0.
  - `source_urls` arrays contain no duplicates. **Rollback:** restore `phase1_before.json` + backup.
  - **Provenance kept (low-priority):** `MATCH (n) WHERE size(coalesce(n.legacy_internal_provenance_docs,[]))>0
    RETURN count(n)`=1 584 (URL-less internal docs preserved as a subordinate property, not lost).

### Phase 2 — Apply the evidenced overlay (no `Regelwerk` nodes; standards as properties)
- **Do:** modify `apply_to_graph.py` to the property-based model, then `--commit`:
  1. Create **only** `Regulierungsfrage`(11) + `Nachweisforderung`(27) nodes (drop the 6 `<4`-edge
     Nachweisforderung; fold their anchor edges into `nf_schadstoffpruefung` via `MERGE`). **No
     `Regelwerk` nodes, no `Quelle` nodes.**
  2. Create the structural regulation edges only: `TRIGGERS_REGULIERUNGSFRAGE` (anchor→rf),
     `ERFORDERT_NACHWEIS` (anchor→nf and rf→nf). Tagged, with S3 evidence keys (`source_url`,
     `evidence_status`, `confidence`) **as edge properties**.
  3. **Fold the 91 standards into properties (R2):** from `GESTUETZT_AUF_REGELWERK`(169) + `GILT_IN_LAND`
     (281), set on each `Nachweisforderung`: `rechtsgrundlagen[]` (standard names),
     `rechtsgrundlagen_urls[]`, `jurisdiktion[]`. Do **not** create `UNTERLIEGT_REGELWERK`/
     `GESTUETZT_AUF_REGELWERK`/`GILT_IN_LAND` edges.
  4. Keep the pollutant hierarchy as edges among the surviving `Nachweisforderung`
     (specific check → `nf_schadstoffpruefung`) where the check survived (`AsbestCheck` etc. ≥4 edges).
- **Accept:** `MATCH (n:Regulierungsfrage) RETURN count(n)`=11; `MATCH (n:Nachweisforderung) RETURN
  count(n)`=27; `MATCH (n:Regelwerk) RETURN count(n)`=0; `MATCH (n:Quelle) RETURN count(n)`=0;
  every regulation edge has `source_url` **as a property** (no source node); every `Nachweisforderung`
  with a known standard has non-empty `rechtsgrundlagen_urls`; `audit_edges.py` 0 problems.
  **Rollback:** `review_run` delete + `source_scope` node delete.

### Phase 3 — Retire the legacy regulation layer (delete-over-migrate, per R3)
Because `Regelwerk` is **not** a node type (R2) and the overlay already carries the regulation semantics,
Phase 3 is **mostly deletion**, not rewiring. For each legacy edge type decide per source node:
- **(a) source already overlay-anchored ⇒ DELETE the legacy edge** (semantics duplicated by the overlay).
- **(b) source NOT yet overlay-anchored ⇒ preserve as a PROPERTY** — set `rechtsgrundlage` (the old
  standard's name) + `source_url` on that source's existing/`MERGE`d `ERFORDERT_NACHWEIS` (or, if none,
  on the node as `rechtsgrundlagen[]`). **Never create a `Norm`/`Regelwerk`/`GAP_*` node.**
- **Do (measured split):**
  - `REFERENZIERT_NORM`(143): **43 delete (a)** · 100 → property (b). `HAT_RECHTLICHE_BEDINGUNG`(26):
    9 delete · 17 → property. `HAT_BAUPRODUKTSTATUS`(34): **31 delete** · 3 → BTG property +
    enum→property. `HAT_ZERTIFIZIERUNG`(12): **12 delete** (fully redundant). `HAT_GELTUNGSBEREICH`(15),
    `HAT_TYPISCHEN_BAUPRODUKTSTATUS`(19), `REGULIERT`(25), `METHODENGRUNDLAGE_NORM`(8): evaluate per (a)/(b),
    default → property where it names a real standard, else delete.
  - Then **delete the now-orphan legacy nodes/labels**: `Norm`(103), `RechtlicheBedingung`(16),
    `Bauproduktstatus`(15), `Geltungsbereich`(6), `Zertifizierungssystem`(8), `LCAModule`(5).
  - The 8 `GAP_*` standards (e.g. CROW-CUR 4) → `phase3_gaps.json` only.
- **🛑 Guardrails (verified 2026-06-05):**
  - **G3.1 No node creation, ever.** No `Norm`/`Regelwerk`/`GAP_*`/`Quelle` node is created in this phase.
    *Accept:* label counts for the 6 legacy labels = 0 **and** `Regelwerk`=0 **and** `Quelle`=0;
    `MATCH (n) WHERE n.id STARTS WITH 'GAP_' RETURN count(n)`=0.
  - **G3.2 Delete-over-migrate is the default.** ~95 legacy edges from overlay-anchored sources are
    **deleted, not migrated** (REFERENZIERT_NORM 43, HAT_BAUPRODUKTSTATUS 31, HAT_ZERTIFIZIERUNG 12,
    HAT_RECHTLICHE_BEDINGUNG 9). *Accept:* 0 legacy regulation edges remain (`REFERENZIERT_NORM`/
    `HAT_RECHTLICHE_BEDINGUNG`/`HAT_BAUPRODUKTSTATUS`/`HAT_TYPISCHEN_BAUPRODUKTSTATUS`/
    `HAT_GELTUNGSBEREICH`/`HAT_ZERTIFIZIERUNG`/`REGULIERT`/`METHODENGRUNDLAGE_NORM` = 0).
  - **G3.3 Net-new info preserved as property, deduped.** Every (b) standard ends up in exactly one place
    (`rechtsgrundlage` on the edge, or one entry in `rechtsgrundlagen[]` on the node). *Accept:* no
    `rechtsgrundlagen[]` array has duplicates; 0 standards silently dropped (count (b) inputs = count
    properties written + logged gaps).
  - **G3.4 No self-loops, no duplicate property edges.** `Norm`→`Norm` cross-refs (incl. the 2
    `sci_p427`↔`p440`) become **one** `rechtsgrundlagen` entry on the relevant Nachweisforderung, **not**
    an edge. *Accept:* 0 self-loops on any regulation edge.
- **Accept (summary):** the 6 legacy labels = 0; all 8 legacy regulation rel types = 0; net-new standards
  live as deduped properties; 0 nodes created; gaps logged. **Rollback:** `phase3_before.json`.

### Phase 4 — Schadstoff re-evidence (no silent loss)
- **Do:** cite `TYPISCH_BEI_ERA`(15) **and** `TYPISCH_BEI_MATERIAL`(74) (LfU/TRGS/REACH); build sourced
  spine via era **and** material (covers the 38/228 era-only gap); route the 5 condition pollutants
  (`s_radon`→Standort/StrlSchG, `s_schimmel/chlorid/salze/mineraloel`→Defekt/exposure/VDI 6202); name
  `s_radon`. Retire `HAS_RISK_POLLUTANT`(754)/`REQUIRES_VERIFICATION_FOR`(339) **only where a sourced
  replacement exists**; tag the rest `screening_unverified` and **report for explicit drop/keep**.
- **🛑 Anti-duplication / evidence guardrails (verified 2026-06-05):**
  - **G4.1 Enrich the existing `TYPISCH_BEI_*`, don't duplicate them.** The 15 `TYPISCH_BEI_ERA` + 74
    `TYPISCH_BEI_MATERIAL` + 10 `TYPISCH_BEI_BAUTEILTYP` already exist and are **all unsourced** (0/99
    have `source_url`). Phase 4 must **`MATCH` the existing edge and `SET` evidence**
    (`source_url`/`evidence_status`/`confidence`), **not** create a parallel sourced edge beside an
    unsourced one. New era/material links use `MERGE` on the `(source,Schadstoff)` pair.
    *Accept:* `MATCH (a)-[r:TYPISCH_BEI_ERA|TYPISCH_BEI_MATERIAL|TYPISCH_BEI_BAUTEILTYP]->(b) WITH
    a,b,type(r) AS t,count(r) AS c WHERE c>1 RETURN count(*)`=0.
  - **G4.2 Don't re-create the overlay's Schadstoff routing.** The overlay already links Schadstoff into
    the regulation layer (`TRIGGERS_REGULIERUNGSFRAGE`/`ERFORDERT_NACHWEIS`; the backing standard lives as
    a `rechtsgrundlagen[]` property on the `Nachweisforderung`). Phase 4 must `MERGE` (reuse), never add a
    second copy, and append standards to the array (deduped), not as new nodes/edges.
    *Accept:* `MATCH (a)-[r:ERFORDERT_NACHWEIS]->(b) WITH a,b,count(r) AS c WHERE c>1 RETURN count(*)`=0.
  - **G4.3 Clear evidence on every kept edge.** Every Schadstoff-spine edge that is **kept** carries a
    `source_url`; the unsourced remainder is tagged `screening_unverified` **and listed in
    `phase4_screening_report.json`** for an explicit drop/keep. No kept edge is silently unsourced.
    *Accept:* `MATCH (a)-[r:TYPISCH_BEI_ERA|TYPISCH_BEI_MATERIAL]->(s:Schadstoff) WHERE r.source_url IS
    NULL AND coalesce(r.evidence_status,'') <> 'screening_unverified' RETURN count(r)`=0.
- **Accept:** all 13 Schadstoff reachable by a **sourced** path; remaining `HAS_RISK_POLLUTANT` = only the
  reported `screening_unverified` set; 0 silent losses; 0 duplicate `TYPISCH_BEI_*`/`ERFORDERT_NACHWEIS`
  pairs. **Rollback:** `phase4_before.json`.

### Phase 5 — PruefungNachweis dedup + Leistungsanforderung consolidate
- **Do:** merge `pn_/pr_` twins + name bare ids (reviewed `phase5_pruefung_dedup.csv`); add
  `(pn)-[:ERFUELLT_NACHWEIS]->(nf)` **before** retiring `HAT_PRUEFUNG`(465) (load-bearing: 65/120 methods
  reachable only via `HAT_PRUEFUNG`); consolidate Leistungsanforderung ~46→~20 + retire
  `HAT_LEISTUNGSANFORDERUNG`(452).
- **Accept:** 0 `pn_/pr_` dup pairs; 0 nameless PruefungNachweis; every method has `ERFUELLT_NACHWEIS`;
  `HAT_PRUEFUNG`=0; Leistungsanforderung ≤ ~22. **Rollback:** `phase5_before.json`.

### Phase 6 — Huerde B-clean, reuse-chain re-express, Tier-F deletions
- **Do:**
  - Huerde: keep 11 barriers + `category` (Rakhshan); add Rakhshan/FCRBE source as `source_urls[]`
    **properties** on the Huerde nodes (no source node); reconnect technical→Bauteilgruppe
    (material_derived), market→Projekt (case_documented else taxonomy_derived); delete 13 regulatory
    Huerde + `HuerdeKategorie`(10) + all 930 `inferiert` `HAT_HUERDE`.
  - **`Wiederverwendungskette`(14): re-express, then delete (no data loss).** First write the donor/
    receiver facts as direct `(:Bauteilgruppe)-[:FROM_DONOR]->(:Bauwerk)` / `-[:INTO_RECEIVER]->` carrying
    the chain's source as the edge property `source_url` (taken from the WVK's `source_urls` set in
    Phase 1; these BTG have no such edge today). Then delete the 14 nodes; this retires only
    `TEIL_VON_KETTE`(14). **`FROM_DONOR`(245)/`INTO_RECEIVER`(278) stay** (core edges).
  - Delete `Akzeptanz`(7), `OntologyAnchor`(if not in P1), `STUB_PROJECT_LINK`(165 *edges*),
    `GEHÖRT_ZU`(55 *edges, corrupt*), `Wirtschaft`(12)+`HAT_WIRTSCHAFT`(41)+`HAT_WIRTSCHAFTSASPEKT`(11);
    `MatchingQualitaet`→3 BTG properties (Geo/Spec/Temporal)+retire `HAT_MATCHINGQUALITAET`(182).
- **Accept:** `Huerde`=11 each with `category`; every kept `HAT_HUERDE` has `source_url`+`basis`; 0
  `inferiert` `HAT_HUERDE`; `Akzeptanz`/`OntologyAnchor`/`MatchingQualitaet`/`Wiederverwendungskette`/
  `Wirtschaft`=0; the 14 BTG now have direct sourced `FROM_DONOR`/`INTO_RECEIVER`. **Rollback:** `phase6_before.json`.

### Phase 7 — Consolidate duplicate axes + low-info demotions
- **Do:** `Marktmodell`→`Beschaffungsweg` (rewire `HAT_MARKTMODELL`(370)→`HAT_BESCHAFFUNGSWEG`);
  `Tragwerksprinzip`→`Bauweise` (rewire `HAT_TRAGWERKSPRINZIP`(68)); `Bauobjektklasse`→`Nutzung`
  (keep non-use values); `Layer`→Bauteiltyp prop (`TEILT_LAYER`15); `Bauteilebene`→BTG prop
  (`HAT_BAUTEILEBENE`289); `Wiederverwendungsort`/`Funktionswechsel`→BTG props; `Tool`→`Software`.
  **`HAT_STATUS`→`Bauteilgruppe.status` property** (88 % single-valued; low-info axis) + delete `Status`
  label + `HAT_STATUS`(584). (Snapshot each; redirect edges before delete.)
- **Accept:** merged labels = 0 nodes; redirected edge counts preserved (no orphans); properties present;
  `Status`=0, `HAT_STATUS`=0. **Rollback:** `phase7_before.json`.

### Phase 8 — Relationship-type dedup & naming normalization (NEW)
- **Do:**
  - Collapse the applicability sprawl → keep `GILT_IN_LAND` (jurisdiction) + `ERFORDERT_NACHWEIS`/
    `TRIGGERS_REGULIERUNGSFRAGE` (the regulation structure); rewire/retire `APPLIES_IN`(20),
    `APPLIES_TO`(20), `ANGEWENDET_AUF`(13), `RELEVANT_FOR`(100), `REGULIERT`(25, if not already in P3).
    (`BELEGT_IN`/`HAS_SOURCE_LINK`/`UNTERLIEGT_REGELWERK`/`GESTUETZT_AUF_REGELWERK` are already gone from
    Phases 1–3.)
  - Merge `HAT_DEFEKT_BEFUND`(25)→`HAT_DEFEKT`(32); reconcile `NUTZT_BAUWERK`(27)↔`HAS_BAUWERK`(166)→one.
  - **Normalize reltype naming to German** (rename the EN types: `HAS_BAUWERK`, `HAS_RISK_POLLUTANT`,
    `HAS_SOURCE_LINK`, `FROM_DONOR`, `INTO_RECEIVER`, `BUILT_IN_ERA`, `REQUIRES_VERIFICATION_FOR`,
    `RELEVANT_FOR`, `APPLIES_*`) where the type survives. (Rename = create new + copy props + delete old,
    tagged + snapshot.)
- **Accept:** `APPLIES_IN`/`APPLIES_TO`/`ANGEWENDET_AUF`/`RELEVANT_FOR`/`HAT_DEFEKT_BEFUND`=0; total reltype
  count ≤ **~50**; no orphaned edges. **Rollback:** `phase8_before.json`.

### Phase 9 — Final review & verification
Run all; every check green = done. Write `FINAL_AUDIT_REPORT.md`; refresh `AGENTS.md` (its 2 580-node
"Aktueller Stand" is stale) + `HANDOFF.md`.
- **T1 labels** `MATCH (n) UNWIND labels(n) AS l RETURN count(DISTINCT l) AS c` ≈ **38**; the 26 removed
  labels = 0 (the 21 from HANDOFF + `Status` + the 5 evidence labels `Quelle`/`ExternalLink`/`SectionRef`/
  `Dossier`/`ResearchDocument`); only `Regulierungsfrage`+`Nachweisforderung` added (no `Regelwerk`).
- **T2 reltypes** `CALL db.relationshipTypes() YIELD relationshipType RETURN count(*) AS c` ≤ **~50**;
  the retired types (applicability sprawl, `HAT_HUERDE`, `HAS_RISK_POLLUTANT`, `HAT_PRUEFUNG`,
  `HAT_LEISTUNGSANFORDERUNG`, `HAT_MARKTMODELL`, `TEIL_VON_KETTE`, …) = 0.
- **T3 evidence is property-only** `MATCH (n:Quelle) RETURN count(n)`=0 and `ExternalLink`/`SectionRef`/
  `Dossier`/`ResearchDocument`=0; `MATCH ()-[r:BELEGT_IN|HAS_SOURCE_LINK]->() RETURN count(r)`=0;
  every node that had a source now carries `source_urls` (or an edge `source_url`); 0 evidence lost vs the
  Phase-1 snapshot.
- **T4 regulation layer is two tight vocabularies + properties** `Regelwerk`=0 nodes; the 6 legacy labels
  =0; `Regulierungsfrage`=11 and `Nachweisforderung`=27; every `Nachweisforderung` that names a standard
  has a non-empty `rechtsgrundlagen_urls`; 0 legacy regulation rel types remain.
- **T5 evidence integrity** `MATCH ()-[r]->() WHERE r.evidence_status IS NOT NULL AND r.source_url IS NULL
  RETURN count(r)`=0; `MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL RETURN count(r)`=0.
- **T6 no generic spray** `HAS_RISK_POLLUTANT`/`HAT_PRUEFUNG`/`HAT_LEISTUNGSANFORDERUNG`=0 (or only the
  reported `screening_unverified` set, with the recorded decision).
- **T7 connectivity** every kept analytical label connects ≤2 hops to `Projekt` or `Bauteilgruppe`; only
  intentional isolates remain.
- **T8 no duplicate axis / no duplicate edge.** (a) Each kept label = one distinct semantic slot and each
  kept reltype = one distinct relation (manual sign-off, aided by the `SEMANTIC_REVIEW.md` table).
  (b) **No parallel duplicate edges** — baseline is **0** today, so this must stay 0:
  `MATCH (a)-[r]->(b) WITH a,b,type(r) AS t,count(*) AS c WHERE c>1 RETURN t,count(*) ORDER BY count(*) DESC`
  → empty. (c) **No self-loops on regulation edges:**
  `MATCH (a)-[r:ERFORDERT_NACHWEIS|TRIGGERS_REGULIERUNGSFRAGE]->(b) WHERE a=b RETURN count(r)`=0.
- **T9b controlled vocabulary** every **added** node label has ≤15 nodes (`Regulierungsfrage` 11,
  `Nachweisforderung` 27 — exception recorded: user rule "delete <4 edges" kept 27) and **0 sparse
  vocab nodes** below the reuse floor (`Nachweisforderung` with <4 edges = 0).
- **T9 integrity** `audit_edges.py` 0 problems; `_gap_survey.py` 0 mandatory gaps; totals reconcile
  against the sum of phase reports.

**Sign-off:** T1–T9 green → migration complete. Any red → roll back the offending phase, fix, re-run.

---

## 3. Changes vs the previous plan (what v2 adds)
1. **⭐ Evidence is a property, not a node (R1).** The whole source-node layer is deleted
   (`Quelle`/`ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument`, with 2 242 uncited `Quelle` simply
   dropped); `source_url`/`source_urls[]`/`evidence_status` live on the cited node or edge. `BELEGT_IN`/
   `HAS_SOURCE_LINK` retired. (~5 445 → ~2 450 nodes.)
2. **⭐ `Regelwerk` eliminated as a node type (R2).** 91 named standards become **edge/Nachweisforderung
   properties** (`rechtsgrundlagen[]` + URLs). Every *added* node vocabulary is now ≤15 & heavily reused:
   `Regulierungsfrage` 11, `Nachweisforderung` 27 (dropped the 6 with <4 edges).
3. **⭐ Delete-over-migrate (R3).** Legacy regulation edges whose meaning the overlay already carries are
   **deleted, not rewired** (measured: REFERENZIERT_NORM 43, HAT_BAUPRODUKTSTATUS 31, HAT_ZERTIFIZIERUNG
   12, HAT_RECHTLICHE_BEDINGUNG 9); net-new ones become deduped properties — **no node is ever created**.
4. **Edge-side dedup** — Phase 8 (rel-type collapse + EN→DE naming), target **85→~50**.
5. **Graph-wide `evidence_confidence` migration** (19 228 edges) with a numeric mapping that keeps the
   4 634 salvageable signals.
6. **`Wiederverwendungskette` deleted *without data loss*** — donor/receiver facts re-expressed as direct
   `source_url`-carrying edges first.
7. **`HAT_STATUS`→property** (88 % single-valued).
8. **Written definition of "generic"** so no observed fact is wrongly deleted; **corrected baseline**
   (64 labels / 85 reltypes / 5 445 nodes; 0 edge-level sources today); **array-safe Phase-0 query**.
9. **Anti-duplication guardrails** for Phase 3 (G3.1–G3.4: no node creation, delete-over-migrate, deduped
   properties, no self-loops) and Phase 4 (G4.1–G4.3: enrich existing `TYPISCH_BEI_*`, reuse overlay
   routing, clear evidence on every kept edge). T8 asserts **0 parallel duplicate edges** (baseline 0) and
   **0 regulation self-loops**; T9b asserts the **≤15 controlled-vocabulary** rule.

## 4. Document map
`FINAL_PLAN_v2.md` (this — canonical) · `SEMANTIC_REVIEW.md` (why these changes) · `HANDOFF.md` (executor
detail + appendices A–L) · `FINAL_PLAN.md` (original decisions, superseded) · `DETAILED_PLAN.md` ·
`SEMANTIC_PROOF.md` · `GRAPH_BLUEPRINT_DATA.md` · `REWIRE_REVIEW.md` · `HUERDE_RESEARCH.md` ·
`POLLUTANT_ERA_EVIDENCE.md` · `EVIDENCE_REGELWERK.md`.

## 5. Where to start
Approve **Phase 0 + 1** (backup + encoding + full source unification incl. the 3 sub-label collapses + the
graph-wide confidence migration). I run one phase, post its `phaseN_report.json` + acceptance results, and
wait for go-ahead before the next. Open Phase-4 item: per-project `case_documented` extraction now, or ship
`taxonomy_derived` first.
