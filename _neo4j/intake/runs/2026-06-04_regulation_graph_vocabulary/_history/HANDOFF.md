# HANDOFF — clean, evidence-first regulation graph (complete execution plan)

Self-contained handoff for the agent/person executing the cleanup of `mit-bestand`. Read this top to
bottom; it references the deeper docs but stands alone. **No DB write happens without a per-phase
go-ahead.** Decisions are locked (`FINAL_PLAN.md`); the plan is semantically proven (`SEMANTIC_PROOF.md`).

> **⭐ Canonical execution plan is now [`FINAL_PLAN_V2.md`](FINAL_PLAN_V2.md)** (live-verified 2026-06-05,
> incorporates `SEMANTIC_REVIEW.md`). It supersedes the phase list below and **changes the evidence model**:
> evidence (incl. the specific standard citation) is a **property on the node/edge**, not a node — the
> whole source-node layer (`Quelle`/`ExternalLink`/`SectionRef`/`Dossier`/`ResearchDocument`, 2 242 of
> them uncited) is **deleted**, and **`Regelwerk` is eliminated as a node type** (standards →
> `rechtsgrundlagen[]` properties). Added vocabularies are ≤15 & heavily reused (`Regulierungsfrage` 11,
> `Nachweisforderung` 27); legacy regulation edges are **deleted-over-migrated** where the overlay already
> covers them. Targets: ~2 450 nodes, ~38 labels, ~50 reltypes. The appendices A–L below remain reference,
> **but Sections 3 (Quelle-node source standard) and the `Regelwerk`-node parts are superseded by
> `FINAL_PLAN_V2.md` §0b.**

---

## 0. Purpose & current state
Turn a 64-label, mostly-unsourced classification graph into a clean, **evidence-first** graph organised
around `Projekt`/`Bauteilgruppe`, with **one unified source model**, **one evidenced regulation layer**,
and **no duplicate axes**. Target: **64 → ~46 labels** (see the label-arithmetic note below — the
long-quoted "~34" is **not reachable** by the enumerated decisions; see the label-arithmetic note), every regulation edge sourced, **~2 940 generic
*regulation* edges** (`HAT_HUERDE`/`HAS_RISK_POLLUTANT`/`HAT_PRUEFUNG`/`HAT_LEISTUNGSANFORDERUNG`/
`REQUIRES_VERIFICATION_FOR`) retired and re-derived from sourced rules.

> **⚠️ Two distinct numbers — do not conflate (verified live 2026-06-05):**
> - **~2 940** generic *regulation* edges are **retired/replaced** (the ones above).
> - **19 228** edges graph-wide carry the categorical property `evidence_confidence` (90 % of all
>   21 403 edges). Removing that *property* (per S4) is a **separate, graph-wide** job, not the same as
>   retiring the 2 940 regulation edges. See S4 for the migration that keeps the 4 634 salvageable
>   (`belegt`/`teilweise_belegt`/`wahrscheinlich`/`abgeleitet…`) signals as numeric `confidence`.

> **Reality-check (live `mit-bestand`, 2026-06-05):** every label/edge count in §B–§D below was
> re-measured and matches. Totals: **5 445 nodes · 21 403 rels · 64 in-use labels (66 registered) ·
> 85 relationship types**. Overlay is **not yet applied** (0 tagged nodes/edges; `Regelwerk`/
> `Regulierungsfrage`/`Nachweisforderung` absent). Mojibake confirmed present. `AGENTS.md`'s
> "Aktueller Stand" (2 580 nodes) is **stale** and should be refreshed in Phase 8.

> **✅ Label-arithmetic — the real target is ~46, NOT ~34 (researched & locked 2026-06-05).** The
> enumerated decisions remove **21** in-use labels (Akzeptanz, Bauobjektklasse, Bauproduktstatus,
> Bauteilebene, ExternalLink, Funktionswechsel, Geltungsbereich, HuerdeKategorie, LCAModule, Layer,
> Marktmodell, MatchingQualitaet, Norm, OntologyAnchor, RechtlicheBedingung, Tool, Tragwerksprinzip,
> Wiederverwendungsort, **Wiederverwendungskette**, Wirtschaft, Zertifizierungssystem) and add **3**
> (Regulierungsfrage, Nachweisforderung, Regelwerk): `64 − 21 + 3 = 46`.
> **Why not 34?** The 13-label gap was researched against live node counts: the remaining small labels
> (5–10 nodes each — `Status`, `Defekt`, `ZustandsKlasse`, `BauwerkEra`, `Methode`, `Prozessphase`,
> `Beschaffungsweg`, …) are **distinct controlled-vocabulary axes**, each a separate semantic slot that
> T7 (orthogonality) explicitly protects. The plan already demoted the genuinely-redundant ones to
> properties (Layer, Bauteilebene, MatchingQualitaet, Bauproduktstatus-enums) and merged the
> measured-overlap duplicates (Marktmodell, Tragwerksprinzip, …). Forcing 13 more merges would have to
> either **collapse orthogonal axes (violating T7)** or demote useful query axes to properties for no
> analytical gain. **~46 is therefore the correct, principled target; the long-quoted "~34" was an
> unsupported earlier estimate.**
> **Previously-unaddressed labels (now resolved):**
> - `Wiederverwendungskette` (**14 nodes**) — donor→component→receiver reuse chains
>   (`FROM_DONOR`/`INTO_RECEIVER`→Bauwerk, `TEIL_VON_KETTE`→Bauteilgruppe, `BELEGT_IN`→Quelle).
>   **DELETE** (user decision 2026-06-05). Snapshot first; removing the 14 nodes drops their 56 edges
>   and retires only `TEIL_VON_KETTE` (14, exclusive to WVK). **`FROM_DONOR` (245) and `INTO_RECEIVER`
>   (278) are NOT retired** — they are core `Bauteilgruppe`→`Bauwerk` donor/receiver edges used graph-wide.
>   ⚠️ These 14 chains are the **only** donor→receiver link for their 14 component groups (0 of them have
>   a direct BTG `FROM_DONOR`/`INTO_RECEIVER`), and all 14 are sourced — so deleting the label loses
>   unique sourced facts unless first re-expressed as direct BTG edges (see SEMANTIC_REVIEW). Handled in
>   Phase 6 (Tier-F deletions). It **is** counted in the 21 removals above.
> - `GraphVersion` (0 nodes) and `ZertifizierungBewertungssystem` (0 nodes) — **empty registered
>   labels** (the 8 cert systems actually live under `Zertifizierungssystem` as `zbs_*` ids). They
>   inflate `db.labels()` from 64→66; clear them from the registry (or note they're harmless empties).

Built & validated already (in this run folder): the overlay (`vocab_nodes.jsonl`, `vocab_edges.csv` —
11 Regulierungsfrage / 33 Nachweisforderung / 91 Regelwerk; 601 backbone + 3 729 anchor edges),
`rewire_map.csv` (341 old nodes mapped), `audit_edges.py` (0 problems), `apply_to_graph.py`
(dry-run clean).

## 1. Prerequisites & environment
- Neo4j `mit-bestand` at `bolt://localhost:7687` (creds in `.cursor/mcp.json`; helper
  `_scripts/neo4j_env.py`). MCP is read-only; write scripts use the bolt driver directly.
- Python deps: `requirements-neo4j.txt` (neo4j driver).
- Tools to reuse: `backup_neo4j_graph.py`, `_snapshot_predelete.py`, `restore_neo4j_graph_backup.py`,
  `_gap_survey.py`, and in this folder: `build_vocabulary_graph.py`, `connect_anchors_to_vocab.py`,
  `apply_to_graph.py`, `audit_edges.py`, `rewire_map.py`.

## 2. Global conventions (apply in EVERY phase)
1. **Dry-run → review → commit.** Every write script runs read-only first and prints before/after.
2. **Tagging.** New nodes: `source_scope='regulation_graph_vocab_2026_06_04'`. New/modified edges:
   `review_run='regulation_graph_vocab_2026_06_04'`.
3. **Snapshot before delete.** Each phase writes `phaseN_before.json` (nodes/edges it will remove) via
   `_snapshot_predelete.py`, and `phaseN_report.json` (counts, acceptance results) after.
4. **Idempotent.** `MERGE` on `id`; re-running a phase is a no-op.
5. **Rollback.** Per-phase: restore `phaseN_before.json` + `MATCH ()-[r {review_run:$run}]->() DELETE r`.
   Catastrophic: `restore_neo4j_graph_backup.py` (Phase 0 backup).

---

## 3. ⭐ THE UNIFIED RESOURCE (SOURCE / EVIDENCE) STANDARD — always the same way
The graph today cites sources **six different ways** (`Quelle`+`BELEGT_IN`, `ExternalLink`, edge
`source_url`, `HAS_SOURCE_LINK`, `ANCHORED_BY`→seed, node `url`/`source_urls` props). **This is the
core thing to unify.** From now on, exactly **two mechanisms, each with one form:**

### S1 — One source node: `Quelle`
- Every real source = **one** `:Quelle` node, **deduplicated by normalized URL** (lowercase host,
  strip trailing slash/utm). `ExternalLink` is absorbed → `:Quelle {quelltyp:'external_link'}`.
- Required props: `id`, `url` (http(s); or `internal:<key>` for non-web), `titel`, `quelltyp`,
  optional `herausgeber`, `zugriff_datum`.
- `quelltyp:'seed'` marks definitional/seed sources (e.g. controlled-vocab seed) — **not counted as
  evidence** (prevents pseudo-evidence).

### S2 — Node provenance: `(x)-[:BELEGT_IN]->(:Quelle)` — the ONLY node-level citation
- Retire as source mechanisms: `ANCHORED_BY`/`OntologyAnchor` (delete), node `url`/`source_urls`/
  `primary_source_url` *used as evidence* (migrate to a linked `Quelle`), `HAS_SOURCE_LINK` (keep only
  as a `Quelle`→`Quelle` dedup/relation pointer, not as a node's evidence).

### S3 — Edge evidence: a FIXED property set on the edge (the overlay pattern), always these keys
`evidence_status` ∈ {`rule_documented`,`rule_derived`,`case_documented`,`comparative`,
`screening_unverified`} · `source_url` · `source_quote` · `confidence` (float 0–1) · `basis`
(optional: material_derived/era/jurisdiction/…) · `applicability_reason` · `review_run` ·
`created_at_utc`.
- **Cross-link rule:** every distinct edge `source_url` MUST exist as a `Quelle` node, so the edge
  evidence and the source catalogue stay consistent (one source, one node, reused everywhere).

### S4 — One confidence scale (graph-wide migration — 19 228 edges, not ~2 700)
Numeric `confidence` 0–1 only. **Retire the categorical `evidence_confidence`** across the **whole
graph** — it sits on **19 228 of 21 403 edges** (measured), with 8 values:
`unklar` 13 259 · `teilweise_belegt` 2 309 · `belegt` 1 479 · `inferiert` 1 192 · `abgeleitet` 452 ·
`wahrscheinlich` 238 · `abgeleitet_aus_bestehender_bauteilgruppe` 156 · `unsicher` 143.
- **Do not blanket-delete** — 4 634 edges (`belegt`/`teilweise_belegt`/`wahrscheinlich`/`abgeleitet*`)
  carry real signal. Map categorical → numeric `confidence`, then drop the categorical property:
  `belegt→0.9 · teilweise_belegt→0.6 · wahrscheinlich→0.5 · abgeleitet*→0.4 · inferiert→0.25 ·
  unsicher→0.2 · unklar→null` (no fabricated confidence for `unklar`).
- **`evidence_status` is NOT added here.** On the factual layer set only numeric `confidence`. Keep
  `evidence_status` (+ mandatory `source_url`) exclusively on the evidence/regulation layer (S3), so the
  T3 invariant "`evidence_status` ⇒ `source_url`" never breaks.
- The ~2 940 generic *regulation* edges are a **subset** that gets retired/replaced in later phases; this
  S4 migration handles the *remaining* ~16 000 factual-layer edges that no phase otherwise touches.

### S5 — Acceptance for the standard (checked in Phase 1 and again in review)
- 0 nodes carry an http URL *as a source property* without a corresponding `Quelle`+`BELEGT_IN`.
- 0 `ANCHORED_BY` edges; `ExternalLink` label count = 0 (merged into `Quelle`).
- 0 edges with `evidence_confidence` **graph-wide** (achieved by the S4 migration in Phase 1, not just
  the regulation-edge retirements); every evidence-bearing edge uses the S3 key set.
- `Quelle` deduplicated: no two `Quelle` share a normalized URL.

---

## 4. Locked decisions (summary; full rationale in FINAL_PLAN.md / GRAPH_BLUEPRINT_DATA.md)
- **Apply** the evidenced overlay (Regulierungsfrage/Nachweisforderung/Regelwerk + anchor edges).
- **Collapse** Norm + RechtlicheBedingung + Bauproduktstatus + Geltungsbereich + Zertifizierungssystem
  + LCAModule → **one `Regelwerk`** layer.
- **Keep + re-evidence** Schadstoff (era **and** material rules + condition routing), PruefungNachweis
  (dedup `pn_/pr_`, link via `ERFUELLT_NACHWEIS`), Leistungsanforderung (consolidate ~46→~20).
- **Huerde = B-clean**: keep ~11 market barriers as an evidenced "Reuse-Hemmnis" vocab (Rakhshan
  taxonomy), delete the regulatory half + the 930 `inferiert` edges.
- **Consolidate** Marktmodell→Beschaffungsweg, reuse-event 4→2 (+properties), Tragwerksprinzip→Bauweise,
  Bauobjektklasse→Nutzung, Layer/Bauteilebene→properties, Tool→Software.
- **Delete** Akzeptanz, OntologyAnchor, STUB_PROJECT_LINK, GEHÖRT_ZU, Wirtschaft, MatchingQualitaet→properties.

---

## 5. Phased execution
Each phase: **goal · steps · acceptance (queries must pass) · rollback.** Run in order; stop for
go-ahead after each.

> **Note on phase numbering:** this HANDOFF uses a **9-phase** sequence (0–8) and **supersedes** the
> 8-phase table in `FINAL_PLAN.md` (0–7). The decisions are identical; HANDOFF splits out a dedicated
> **Phase 1 = source-model unification** (foundational) and a dedicated **Phase 8 = final review**.
> Where the two disagree on numbering, **HANDOFF wins** — `FINAL_PLAN.md` is the decision rationale, not
> the execution order.

### Phase 0 — Backup & encoding normalization
- Steps: full `backup_neo4j_graph.py`; then `phase0_fix_encoding.py` re-decodes mojibake (`�`) in all
  string props (dry-run → commit).
- Acceptance (array-safe — the naïve `toString(n[k])` form **crashes** with `CypherTypeError` on
  `StringArray` props such as `source_urls`):

```cypher
MATCH (n)
WHERE any(k IN keys(n) WHERE
  any(v IN (CASE WHEN n[k] IS :: LIST<ANY> THEN n[k] ELSE [n[k]] END)
      WHERE v IS :: STRING AND v CONTAINS '\uFFFD'))
RETURN count(n) AS c   // must be 0
```

  total node/edge counts unchanged. (Note: mojibake also exists in some *relationship-type names*, e.g.
  the corrupt `GEHÖRT_ZU` — those are slated for deletion, not re-decoding, since type names can't be
  edited in place.)
- Rollback: restore backup.

### Phase 1 — Source-model unification (Section 3) — FOUNDATIONAL
- Steps: merge `ExternalLink`→`Quelle` (2 610 nodes, all with url); dedup `Quelle` by normalized URL
  (redirect `BELEGT_IN`); migrate node url-as-source props → linked `Quelle` (**scope is small —
  only `ReuseRule`×20 + `OntologyAnchor`×1 carry a url-as-source prop without `BELEGT_IN`**, measured);
  delete `OntologyAnchor` (2 nodes) + `ANCHORED_BY` (**609 edges**); flag `quelltyp:'seed'` on the 313
  url-less `Quelle`; **run the S4 graph-wide migration**: map `evidence_confidence` → numeric
  `confidence` on all 19 228 edges per the S4 table, then drop the categorical property.
- Acceptance: the four S5 checks pass (incl. the **graph-wide** `evidence_confidence = 0`).
- Rollback: `phase1_before.json` + backup.

### Phase 2 — Apply the evidenced overlay (conforms to the standard)
- Steps: `apply_to_graph.py --commit`; **materialize each Regelwerk `source_url` as a `Quelle` +
  `BELEGT_IN`** (so S3 cross-link holds).
- Acceptance: 135 tagged nodes, 4 330 tagged edges; `audit_edges.py` 0 problems; every regulation edge
  has `source_url` AND a matching `Quelle`.
- Rollback: `review_run` delete.

### Phase 3 — Regulation collapse (6 → Regelwerk)
- Steps: rewire `REFERENZIERT_NORM`/`HAT_RECHTLICHE_BEDINGUNG`/`HAT_BAUPRODUKTSTATUS` →
  `UNTERLIEGT_REGELWERK` (via `rewire_map.csv`); Bauproduktstatus enums → BTG property; merge
  Zertifizierungssystem/LCAModule → Regelwerk; drop Geltungsbereich; snapshot+delete the old labels;
  log the 8 gaps to `phase3_gaps.json`.
- Acceptance: `Norm`/`RechtlicheBedingung`/`Geltungsbereich`/`Zertifizierungssystem`/`LCAModule` = 0
  nodes; every former `REFERENZIERT_NORM` source now has `UNTERLIEGT_REGELWERK`; gaps logged.
- Rollback: `phase3_before.json`.

### Phase 4 — Schadstoff re-evidence (REFINED per SEMANTIC_PROOF.md — no silent loss)
- Steps: cite `TYPISCH_BEI_ERA` **and** `TYPISCH_BEI_MATERIAL` (LfU/TRGS/REACH); build sourced spine via
  **both era and material**; route the 5 condition pollutants (`s_radon`→Standort/StrlSchG,
  `s_schimmel/chlorid/salze/mineraloel`→Defekt/exposure/VDI 6202); name `s_radon`; retire
  `HAS_RISK_POLLUTANT`/`REQUIRES_VERIFICATION_FOR` **only where a sourced replacement exists**; tag the
  rest `screening_unverified` and **report for an explicit drop/keep decision**.
- Acceptance: all 13 Schadstoff reachable by a sourced path; remaining `HAS_RISK_POLLUTANT` = only the
  reported `screening_unverified` set; 0 silent losses.
- Rollback: `phase4_before.json`.

### Phase 5 — PruefungNachweis dedup + Leistungsanforderung consolidate
- Steps: merge `pn_/pr_` twins + name bare ids (`phase5_pruefung_dedup.csv`, reviewed); add
  `(pn)-[:ERFUELLT_NACHWEIS]->(nf)` **(load-bearing — must precede retiring HAT_PRUEFUNG)**; retire
  `HAT_PRUEFUNG`; consolidate Leistungsanforderung clusters (~46→~20) + retire `HAT_LEISTUNGSANFORDERUNG`.
- Acceptance: 0 `pn_/pr_` dup pairs; 0 nameless PruefungNachweis; every method has `ERFUELLT_NACHWEIS`;
  `HAT_PRUEFUNG`=0; Leistungsanforderung ≤ ~22.
- Rollback: `phase5_before.json`.

### Phase 6 — Huerde B-clean + Tier-F deletions
- Steps (detail in `HUERDE_RESEARCH.md`): keep 11 barriers + `category` (Rakhshan); add Rakhshan/FCRBE
  `Quelle`; reconnect technical→Bauteilgruppe (material_derived), market→Projekt (case_documented where
  a project source exists, else taxonomy_derived); delete regulatory Huerde + `HuerdeKategorie` + all
  930 `inferiert` `HAT_HUERDE`; delete Akzeptanz, OntologyAnchor(if not in P1), STUB_PROJECT_LINK,
  GEHÖRT_ZU, Wirtschaft, **Wiederverwendungskette (14 nodes + 56 edges; snapshot first — retires only
  `TEIL_VON_KETTE`; `FROM_DONOR`/`INTO_RECEIVER` stay, they are core BTG→Bauwerk edges)**;
  MatchingQualitaet→3 properties.
- Acceptance: `Huerde`=11, each with `category`; every `HAT_HUERDE` has `source_url`+`basis`; 0
  `inferiert` HAT_HUERDE; Akzeptanz/OntologyAnchor/MatchingQualitaet/Wiederverwendungskette=0.
- Rollback: `phase6_before.json`.

### Phase 7 — Consolidate duplicate axes
- Steps: Marktmodell→Beschaffungsweg; Wiederverwendungsort/Funktionswechsel→BTG properties;
  Tragwerksprinzip→Bauweise; Bauobjektklasse→Nutzung; Layer→Bauteiltyp prop; Bauteilebene→BTG prop;
  Tool→Software. (Snapshot each; redirect edges before delete.)
- Acceptance: merged labels = 0 nodes; redirected edge counts preserved (no orphans); properties present.
- Rollback: `phase7_before.json`.

---

## 6. ⭐ Phase 8 — FINAL REVIEW & VERIFICATION (prove the targets are reached)
Run all checks; every one must pass. Write `FINAL_AUDIT_REPORT.md` + update `AGENTS.md`/`HANDOFF.md`.

**T1 — Label count.** `MATCH (n) UNWIND labels(n) AS l RETURN count(DISTINCT l)` ≈ **46** (was 64
in-use / 66 registered). The 21 deleted labels — Norm, RechtlicheBedingung, Bauproduktstatus,
Geltungsbereich, Zertifizierungssystem, LCAModule, Akzeptanz, OntologyAnchor, HuerdeKategorie,
Wirtschaft, MatchingQualitaet, Tragwerksprinzip, Bauobjektklasse, Layer, Bauteilebene, ExternalLink,
Tool, Marktmodell, Wiederverwendungsort, Funktionswechsel, **Wiederverwendungskette** — all return
**0**. Target locked at **~46** (see §0 label-arithmetic; ~34 was unsupported and would break T7
orthogonality).

**T2 — One law layer.** `Regelwerk` present & evidenced; the 6 collapsed labels = 0.

**T3 — Evidence everywhere it should be (the priority).**
- `MATCH ()-[r]->() WHERE r.evidence_status IS NOT NULL AND r.source_url IS NULL RETURN count(r)` = 0.
- `MATCH ()-[r]->() WHERE r.evidence_confidence IS NOT NULL RETURN count(r)` = 0 (categorical gone).
- Every `UNTERLIEGT_REGELWERK`/`ERFORDERT_NACHWEIS`/`TRIGGERS_REGULIERUNGSFRAGE` has `source_url`.

**T4 — Unified resource (the important part).** All four S5 checks pass:
- `MATCH (n:ExternalLink) RETURN count(n)` = 0; `MATCH ()-[r:ANCHORED_BY]->() RETURN count(r)` = 0.
- No two `Quelle` share a normalized URL.
- Every edge `source_url` has a matching `Quelle` node.
- 0 nodes use a url property *as evidence* without `BELEGT_IN`.

**T5 — No generic spray left.** `HAS_RISK_POLLUTANT`/`HAT_PRUEFUNG`/`HAT_LEISTUNGSANFORDERUNG` = 0
(or only the reported `screening_unverified` Schadstoff set, with the user's recorded decision).

**T6 — Connectivity priority.** Every kept analytical label connects (≤2 hops) to `Projekt` or
`Bauteilgruppe`; 0 orphan nodes: `MATCH (n) WHERE NOT (n)--() RETURN labels(n)[0], count(*)` → only
intentional isolates, if any.

**T7 — No duplicate axis.** Manual: the kept ~46 labels each map to a distinct semantic slot
(law / proof / method / question / pollutant / requirement / physical / condition / process / market /
actor / geo / evidence). No two overlap.

**T8 — Integrity & consistency.** `audit_edges.py` 0 problems; `_gap_survey.py` 0 mandatory gaps;
node/edge totals reconcile against the sum of phase reports.

**Sign-off:** all T1–T8 green → migration complete. Any red → roll back the offending phase, fix, re-run.

---

## 7. Document index (read order)
`HANDOFF.md` (this) → `FINAL_PLAN.md` (decisions) → `SEMANTIC_REVIEW.md` (adversarial review of the
decisions, live-verified 2026-06-05 — rel-type dedup, source-model consistency, generic-definition) →
`DETAILED_PLAN.md` (per-phase ops) →
`SEMANTIC_PROOF.md` (why it's sound + Phase-4/Schadstoff fix) → `GRAPH_BLUEPRINT_DATA.md` (per-label
data) → `STATE_REVIEW.md` (overview) → topical: `AUDIT_7_LABELS_DEEP.md`, `RESCUE_VERDICT.md`,
`POLLUTANT_ERA_EVIDENCE.md`, `HUERDE_RESEARCH.md`, `REWIRE_REVIEW.md`, `DECISIONS_EXPLAINED.md`,
`EVIDENCE_REGELWERK.md`, `GRAPH_CRITICAL_AUDIT.md`.

## 8. Risks & handling
- **Silent information loss** → snapshots + `screening_unverified` reporting (Phase 4) + acceptance T3/T5.
- **Source dedup over-merging** → dedup only on *exact normalized URL*; review the merge list first.
- **Irreversibility** → Phase 0 full backup + per-phase snapshots; commit only after dry-run review.
- **`ERFUELLT_NACHWEIS` ordering** → must run before retiring `HAT_PRUEFUNG` (Phase 5).

## 9. Where to start
Confirm **Phase 0 + 1** (backup + encoding + **source unification**). I run one phase, post its
`phaseN_report.json` + acceptance results, and wait for go-ahead before the next. Open item for Phase 4:
do the per-project `case_documented` extraction now, or ship `taxonomy_derived` first.

---

# APPENDICES — full context & findings (so a fresh agent needs nothing else)

## A. Mission origin & journey
- Trigger: `_neo4j/intake/inbox/research/reuse_regulation_graph_replacement_prompt_short.md` — replace
  weak/generic regulation vocabulary with an evidence-backed one.
- Domain: **building-component reuse** (donor/receiver buildings, reclaimed components, the regulations,
  proofs and standards that govern reuse across DE/AT/CH/NL/BE/FR/DK/NO/UK + EU).
- We then (a) web-researched a new evidenced vocabulary, (b) connected it to live anchors, (c) audited,
  (d) critically reviewed the whole graph, (e) proved the cleanup plan semantically. This handoff is the result.

## B. Baseline graph facts (mit-bestand, measured — re-verified 2026-06-05)
- **5 445 nodes · 21 403 relationships · 64 labels · 85 relationship types.**
- Hubs: `Projekt` 86, `Bauteilgruppe` 364, `Bauwerk` 184, `Akteur` 689. Sources: `Quelle` 2 981,
  `ExternalLink` 2 610. Target after cleanup: **~46 labels** (corrected from the earlier "~34"; see §0).

## C. THE central finding — evidence vs. generic tagging
- The analytical graph is **almost entirely unsourced**. Edge-level evidence by rel type: `HAT_HUERDE`
  930 → **0%**, `HAS_RISK_POLLUTANT` 754 → 0%, `HAT_PROZESSPHASE` 679 → 0%, `HAT_STATUS` 584 → 0%,
  `HAT_PRUEFUNG` 465 → 0%, `HAT_LEISTUNGSANFORDERUNG` 452 → 0%, `REFERENZIERT_NORM` 143 → 0%.
- The edges carry a **categorical `evidence_confidence`** that *admits* it's not evidence:
  `HAS_RISK_POLLUTANT`=`inferiert` (650), `HAT_LEISTUNGSANFORDERUNG`=`unklar` (all 452),
  `REQUIRES_VERIFICATION_FOR`=`material_only` (331/339). **0** of the 7 regulation labels reach a real
  http source.
- **Full `evidence_confidence` footprint (measured): 19 228 / 21 403 edges (90 %)** — far beyond the
  regulation layer: `unklar` 13 259 · `teilweise_belegt` 2 309 · `belegt` 1 479 · `inferiert` 1 192 ·
  `abgeleitet` 452 · `wahrscheinlich` 238 · `abgeleitet_aus_bestehender_bauteilgruppe` 156 ·
  `unsicher` 143. This is why S4 is a **graph-wide** migration, distinct from retiring the ~2 940
  generic regulation edges.
- Real http evidence exists in only ~9 labels: `Quelle` 2737, `ExternalLink` 2610, `SectionRef` 575,
  `Akteur` 197, `ResearchDocument` 187, `Dossier` 69, `Kennwert` 52, `Projekt` 33, `ReuseRule` 20.
- **Pseudo-evidence trap:** Schadstoff/Norm `BELEGT_IN` point to a *seed* `Quelle` with no http url —
  looks sourced, isn't. (Hence the `quelltyp:'seed'` flag in the source standard.)
- ⇒ The new overlay is the **only** fully-evidenced layer; the cleanup re-derives the rest from sourced rules.

## D. Per-label disposition (all, with the data that decided it)
`n`=nodes, `→P`/`→BTG`=reached from Projekt/Bauteilgruppe, `httpEv`=real-sourced nodes.
**KEEP-ENTITY/EVIDENCE:** Quelle(2981/2737), ExternalLink(2610→merge to Quelle), SectionRef(582/575),
Dossier(97/69), ResearchDocument(396/187), Kennwert(255/52), ReuseRule(20/20), Akteur(689/197),
Projekt, Bauteilgruppe, Bauwerk, Programm, Materialdepot, Software(+Tool merge), Land, Stadt.
**KEEP-FACTUAL ATTRIBUTE:** Material, Materialgruppe, Bauteiltyp, Nutzung, BauwerkEra, Status,
BauaufgabeIntervention, Defekt, ZustandsKlasse, Verbindungstechnik, Bauobjektrolle, Bauweise(+absorb
Tragwerksprinzip), Bausystem, Prozessphase, Rueckbauverfahren, Aufbereitungsverfahren, Methode,
Ressourcenquelle, Wiederverwendungsergebnis, Logistik, Beschaffungsweg(+absorb Marktmodell),
Geschaeftsmodell, Akteurtyp, Akteurrolle.
**REGULATION (new, keep):** Regulierungsfrage(11), Nachweisforderung(33), Regelwerk(91).
**REGULATION (old → delete/replace):** Norm(103→Regelwerk), RechtlicheBedingung(16→Regelwerk/Frage),
Bauproduktstatus(15→Regelwerk+3 enums→property), Geltungsbereich(6→delete), Zertifizierungssystem(8→Regelwerk),
LCAModule(5→Regelwerk).
**ENTITY UNDER REG (keep+clean):** Schadstoff(13), PruefungNachweis(120 dedup), Leistungsanforderung(46→~20).
**RESTRUCTURE→property:** Layer(→Bauteiltyp), Bauteilebene(→BTG), Wiederverwendungsort, Funktionswechsel,
MatchingQualitaet(→Geo/Spec/Temporal), Bauproduktstatus enums.
**DELETE:** Akzeptanz(7, orphan), OntologyAnchor(2 nodes, scaffolding)+ANCHORED_BY(609 edges),
HuerdeKategorie(10), Wirtschaft(12, mixed), **STUB_PROJECT_LINK (165 — a *relationship type*, not a
label)**, **GEHÖRT_ZU (a corrupt *relationship type*, not a label)**,
**Wiederverwendungskette(14, +56 edges; retires only `TEIL_VON_KETTE`; `FROM_DONOR`/`INTO_RECEIVER` stay)
— user-decided delete 2026-06-05**.
**Huerde(28):** B-clean (keep 11 market barriers, evidenced; delete 13 regulatory + 930 inferiert edges).
**Measured overlaps justifying merges:** Marktmodell∩Beschaffungsweg=86 BTG; 245 BTG carry ≥3 of the 4
reuse-event labels; Tragwerksprinzip 4 nodes / 25 Bauwerk overlap.

## E. The new regulation vocabulary (built, evidenced — see EVIDENCE_REGELWERK.md for URLs+quotes)
- **11 Regulierungsfrage:** Reusedokumentation, RückbauUndBauteilernte, Bauproduktstatus, Tragwerkssicherheit,
  Brandschutz, Bauphysik, Schadstoff, HygieneElektroFunktion, Genehmigung, HaftungGewährleistung,
  UmweltverträglichkeitÖkobilanz.
- **33 Nachweisforderung** (proofs): Bauteilidentifikation, Herkunftsdok., ZustandsUndMassaufnahme,
  Standsicherheit, Materialprüfung, Brandschutznachweis, Bauphysiknachweis, Schadstoffprüfung,
  Produktstatus/Leistungserklärung, Genehmigungsbedarf, Befestigung, Elektrosicherheit, Hygiene,
  Formaldehyd/Emission, AsbestCheck, KMFCheck, PCBCheck, PAKCheck, Schwermetall/Bleifarbe,
  HolzschutzmittelCheck, SicherheitsglasInfo, U-Wert/Energie, Dauerhaftigkeit/Restlebensdauer,
  Schadstoffkataster, OekobilanzEPD, Materialpass, MineralErsatzbaustoff, RC-Gesteinskörnung, Radonmessung,
  VOC-Emission, MikrobielleBelastung, Barrierefreiheit, Absturzsicherung.
- **91 Regelwerke** by domain (each with source_url): Reuse/Rückbau & Abfall (DIN SPEC 91484/91525,
  VDI 6210, KrWG, GewAbfV, EU WFD/CDW, ISO 20887, ÖNORM B 3151, FR PEMD/REP, NO TEK17, BE Tracimat,
  FCRBE, VOB/C 18459); Tragwerk & Prüfung (CEN/TS 1090-201, SCI P427, NTA 8713, EN 1090(+bolts),
  Eurocodes, EN ISO 6892, DIN 4074/EN 14081, EN 408, EN 13791/12504, SIA 269/269-2, DAfStb R-Beton,
  fib, EN 1168, EN 1992-4, NEN 8700, EN 771, Naturstein-EN, CEN/TS 17440, DIN 18945 Lehm, EN 13162);
  Bauproduktstatus & Bauteilnormen (EU CPR 2024/3110 & 305/2011, DIBt ZiE, MVV TB, MBO/LBO, UKCA,
  EN 14351, EN 13830, DIN 18065, ESPR/DPP); Schadstoff (TRGS 519/521/524, GefStoffV, REACH, POP,
  VDI 6202, PCB-RL, DIN 68800/AltholzV, AgBB, VDI 3492, UBA-Schimmel, StrlSchG, EBV, **LfU Arbeitshilfe**);
  Brandschutz (DIN EN 13501, DIN 4102, VKF, UK ADB, OIB, DIN 18008); Bauphysik/Ökobilanz (GEG, SIA 380/1,
  SIA 2032, MuKEn, FR RE2020, NL MPG, UK PAS 2080, EN 15804/15978, EU Taxonomy, EU Level(s), Madaster,
  QNG/DGNB, Glas-IGU); Genehmigung/Recht/Funktion (Dutch Bbl, DK BR18, ProdHaftG, DGUV V3, VDI 6023/6022,
  DIN 18040, Denkmalschutz, Zirkuläre Vergabe).
- **8 live-graph links:** rw_nta_8713↔bps_nta_8713, rw_eu_taxonomy↔rb_eu_taxonomie, rw_strlschg_radon↔s_radon,
  rw_uba_schimmelleitfaden↔s_schimmel, rw_nen_8700↔norm_nen_8700; rw_oenorm_b3151→actor baukarussell;
  rw_fcrbe→actors rotordc/salvoweb/bellastock.

## F. Rewire mapping (full table: rewire_map.csv; 341 old nodes, 333 mapped, 8 gaps)
- Norm 103 → Regelwerk (deduped: EN1090 ×5→rw_en_1090, Eurocodes ×8→rw_eurocodes…; full dict in `rewire_map.py`).
- Bauproduktstatus: CE→CPR, ZiE→DIBt, UKCA→UKCA, NTA8713→nta_8713, PEMD→fr_pemd, Tracimat→tracimat;
  3 enums→property; US IBC / JP JIS → delete.
- RechtlicheBedingung: EU_Taxonomie→eu_taxonomy, KrWG→krwg, Produkthaftung/Gewährleistung→prodhaftg,
  Denkmalschutz→denkmalschutz, Vergaberecht→zirkulaere_vergabe, CE/UKCA→en_1090/ukca.
- **8 gaps to log (Phase 3):** Swiss BauPG (×2 nodes), CROW-CUR 4 (NL concrete reuse), SIA 500 (CH
  accessibility), + 3 out-of-scope US/JP (delete).

## G. Pollutant × era × component matrix (for Phase 4 — sourced; full in POLLUTANT_ERA_EVIDENCE.md)
| Schadstoff | window | components | era nodes | derivable? |
|---|---|---|---|---|
| Asbest | 1950–95 (Verbot '93) | Spritzasbest, Asbestzement, Putze, Fugen, Floor-Flex | nachkrieg, 1970-90, 1990-2000 | era+material+bt |
| KMF | <1996/2000 | Dämmung | 1970-90, 1990-2000 | era+material |
| PCB | 1955–75 (Verbot '78/'89) | Fugendichtmassen (Skelett/Plattenbau), Wandfarben | nachkrieg, 1970-90 | era+material+bt |
| PAK/Teer | bis ~1970er | Teerpappe, Parkett-Schwarzkleber, Gussasphalt | vor1900, 1900-45, nachkrieg | era+material+bt |
| Holzschutz (PCP/Lindan) | bis 1989 | behandeltes Holz | nachkrieg, 1970-90 | era+material |
| Bleifarbe | überw. <1960 | Anstriche | vor1900, 1900-45, nachkrieg | era+material+bt |
| Formaldehyd | ab 1960er | Spanplatten, MDF | nachkrieg, 1970-90, post2000 | era+material |
| Schwermetalle | nutzungsabh. | Beschichtungen, Laborbauten | — | **material only** |
| **Radon** | geologie | Baugrund-Kontakt | — | **location (StrlSchG), NOT era** |
| **Schimmel** | feuchte | feuchtegeschädigt | — | **condition (Defekt), NOT era** |
| **Chlorid/Salze/Mineralöl** | exposure | — | — | **condition/exposure, NOT era** |
Sources: LfU Bayern Arbeitshilfe (`rw_lfu_schadstoff_arbeitshilfe`), TRGS 519/521, REACH, StrlSchG, polludoc, allum.
**Coverage caution (proof):** only 38/228 affected BTG have a Bauwerk-era → derive via era **and**
material; the 5 condition pollutants need condition/location routing; no silent deletion.

## H. Huerde B-clean (for Phase 6 — full in HUERDE_RESEARCH.md)
Taxonomy: **Rakhshan, Morel, Alaka & Charef (2020), Waste Management & Research — 6 categories/23 sub**
(https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/). Keep 11, tag `category`, connect:
- **Technical → Bauteilgruppe (material_derived):** h_heterogenitaet_chargen, h_unkonventionelles_material
  (concrete→service-life/heterogeneity; composite→separation; **steel→few** per literature).
- **Market/Organisational/Perception → Projekt:** h_akzeptanzproblem, h_mengenunsicherheit,
  h_verfuegbarkeitsproblem, h_terminunsicherheit, h_entwurfsbindung, h_fehlende_lagerflaeche,
  h_witterung_feuchte, h_aufbereitungsaufwand, h_ausschreibungsproblem (→ also rw_zirkulaere_vergabe).
- Evidence basis: `case_documented` (project source) where available, else `taxonomy_derived` (Rakhshan).
- Delete the 13 regulatory Huerde + all 930 `inferiert` `HAT_HUERDE`.

## I. How the overlay derives anchor connections (methodology — connect_anchors_to_vocab.py)
Edges are derived from **factual live attributes**, never from Huerde/Norm:
- Material: `Regelwerk-[:BETRIFFT_MATERIAL]->Material`. Bauteilgruppe: live `NUTZT_MATERIAL`,
  **structurally gated by `tragend`** (load-bearing only gets Standsicherheit/EN1090/etc.; façade/Fenster/
  Dämmung excluded), **composite-aware** (≥3 materials/Verbund → down-weight material rules + add
  disassembly), **jurisdiction-gated** (national rules only in the component's project country).
- Bauteiltyp: own product standard via `BETRIFFT_BAUTEILTYP` (Fenster→EN14351, Fassade→EN13830,
  Mauerstein→EN771, Technik→DGUV/VDI…), no material bleed.
- Projekt: `LIEGT_IN_LAND` × **context** — demolition/audit rules need a Rückbau/Umbau/Sanierung
  `HAT_INTERVENTION` or Rückbau/Aufbereitung `HAT_PROZESSPHASE`; energy/LCA rules need build context;
  circular frameworks broad; Schadstoff via `HAS_BAUWERK`-era; DIN 18040 for public `HAT_NUTZUNG`.
- Bauwerk: `BauwerkEra` + `TYPISCH_BEI_ERA` → Schadstoff. Confidence graded by chain (×0.95 group,
  ×0.9 component, ×0.82 era), composite ×0.78. Audit: 0 mismatches.

## J. Semantic proof — what was validated & the holes fixed (full: SEMANTIC_PROOF.md)
- PASS: rewire completeness (333/341), meaning preservation, consolidation-equivalence (measured),
  orthogonality, integrity (dry-run resolves all).
- **2 holes found & fixed in Phase 4:** (3.1) 5 condition pollutants not era/material-derivable → route
  via condition/location; (3.2) era-derivation covers only 38/228 BTG → derive via era **and** material;
  retire generic edges **only where a sourced replacement exists**, else flag `screening_unverified`.
- **Load-bearing ordering:** add `ERFUELLT_NACHWEIS` (method→Nachweis) **before** retiring `HAT_PRUEFUNG`
  (65/120 methods are reachable only via `HAT_PRUEFUNG`).

## K. Scripts (in this run folder unless noted) — purpose · run · in/out
- `build_vocabulary_graph.py` — defines the vocabulary (REGELWERK/MAT_BY_RW/TYPE_BY_RW…); emits
  `vocab_nodes.jsonl` + `vocab_edges.csv`. Re-run after any vocab edit. `python build_vocabulary_graph.py`.
- `connect_anchors_to_vocab.py` — reads live graph (read-only), derives `anchor_edges.csv` (gating in §I).
- `rewire_map.py` — old→new mapping; emits `rewire_map.csv`. `make_rewire_review.py` → `REWIRE_REVIEW.md`.
- `apply_to_graph.py` — **the importer.** Dry-run default (validates all refs); `--commit` writes overlay
  (nodes + vocab_edges + anchor_edges), tagged. Rollback cypher in its header.
- `audit_edges.py` — integrity/jurisdiction/structural/confidence audit. Must return 0 before/after each phase.
- `inspect_connections.py` → `DRY_RUN_DETAIL.md` (per-anchor evidence view).
- Repo tools: `_scripts/backup_neo4j_graph.py`, `_snapshot_predelete.py`, `restore_neo4j_graph_backup.py`,
  `_gap_survey.py`, `neo4j_env.py`.
- **To build (new):** `phase0_fix_encoding.py`, `phase1_source_unify.py`, `phase5_pruefung_dedup.py`,
  `phase6_huerde_reconnect.py`, plus per-phase rewire/delete runners (idempotent, tagged, snapshot-first).

## L. Environment gotchas (save time)
- Bash tool **cwd resets between calls** → use absolute paths or `cd` each call. Prefer the PowerShell/
  Bash tool with the repo path.
- Neo4j 5 Cypher: `RETURN count(x) AS c` (the `AS` is **required**; bare alias errors).
- Mojibake: many names are Latin-1/UTF-8 corrupted (`�`) — Phase 0 fixes; don't match names on raw bytes.
- MCP Neo4j is **read-only**; writes go through the bolt driver in scripts. Password in `.cursor/mcp.json`.
- Whole-graph audit/critical findings for the *non-regulation* labels: `GRAPH_CRITICAL_AUDIT.md` (deferred).
