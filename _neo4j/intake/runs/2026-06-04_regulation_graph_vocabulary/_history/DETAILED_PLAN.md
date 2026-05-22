> ▶ **`HANDOFF.md` is the authoritative execution doc.** It adds a foundational **Phase 1 — Source-model
> unification** (the unified resource standard) and renumbers the phases below accordingly, plus the
> final review (Phase 8). This file holds the per-phase operational detail.

# DETAILED execution plan — clean evidence-first regulation graph

Granular companion to `FINAL_PLAN.md` (decisions) — exact operations, evidence handling, acceptance
checks, and rollback per phase. Huerde = **B-clean** (evidenced barrier vocab).

**Global conventions**
- Every created node: `source_scope='regulation_graph_vocab_2026_06_04'`. Every created/modified edge:
  `review_run='regulation_graph_vocab_2026_06_04'`, plus `evidence_status`, `source_url`,
  `source_quote`, `confidence`, `created_at_utc`.
- Every phase: (1) **snapshot** the nodes/edges it will modify/delete (extend `_snapshot_predelete.py`)
  → `phaseN_before.json`; (2) run idempotent `MERGE`/`SET`/`DELETE`; (3) run **acceptance queries**;
  (4) write `phaseN_report.json`. DB writes only after explicit go-ahead per phase.
- Reuse existing tooling: `backup_neo4j_graph.py`, `_snapshot_predelete.py`, `audit_edges.py`,
  `apply_to_graph.py`, `_gap_survey.py`, `connect_anchors_to_vocab.py`, `rewire_map.py`.

---

## Phase 0 — Backup & encoding normalization
**Goal:** safety net + fix mojibake (`K�nstliche`→`Künstliche`, `Pr�fung`→`Prüfung`, `�-Zeichen`).
**Steps**
1. `python _scripts/backup_neo4j_graph.py` → timestamped full dump.
2. Scan: `MATCH (n) WHERE any(k IN keys(n) WHERE n[k] CONTAINS '�') RETURN labels(n)[0], count(*)`.
3. Re-decode affected string props (UTF-8-mis-read-as-Latin1 → correct). Script `phase0_fix_encoding.py`,
   dry-run first (print before/after), then `--commit`.
**Acceptance:** count of props containing `�` = 0; node/edge totals unchanged; spot-check 20 names.
**Rollback:** restore backup.

## Phase 1 — Apply the evidenced overlay
**Goal:** add the new sourced law layer + anchor connections (already built & dry-run clean).
**Steps**
1. `python apply_to_graph.py` (dry-run) → must report all references resolve.
2. `python apply_to_graph.py --commit` → MERGE 135 vocab nodes (11 rf / 33 nf / 91 rw),
   601 backbone edges, 3 729 anchor edges; all tagged.
**Acceptance:**
- `MATCH (n {source_scope:$run}) RETURN count(n)` = 135; tagged edges = 4 330.
- `python audit_edges.py` → 0 problems (jurisdiction, structural, target-type, confidence).
- Every `Regelwerk`/anchor edge has non-null `source_url`.
**Rollback:** `MATCH ()-[r {review_run:$run}]->() DELETE r; MATCH (n {source_scope:$run}) DETACH DELETE n;`

## Phase 2 — Regulation collapse (6 labels → Regelwerk)
**Goal:** one evidenced law layer. Uses `rewire_map.csv`.
**Steps**
1. **Rewire to Regelwerk** — for each old edge, create the evidenced replacement, carrying the target
   Regelwerk's url/quote:
   - `(x)-[:REFERENZIERT_NORM]->(:Norm)` → `(x)-[:UNTERLIEGT_REGELWERK]->(rw)` per `NORM_TO_RW`.
   - `(x)-[:HAT_RECHTLICHE_BEDINGUNG]->(:RechtlicheBedingung)` → Regelwerk/Frage per `RB_TO`.
   - `(x)-[:HAT_BAUPRODUKTSTATUS]->(:Bauproduktstatus)` → Regelwerk per `BPS_TO_RW`.
2. **Bauproduktstatus status-enums:** for `bestand_no_status / project_specific / unbekannt`, set a
   `produktstatus` **property** on the source Bauteilgruppe; then drop those 3 nodes.
3. **Merge cert/LCA/scope:** `Zertifizierungssystem`→Regelwerk (DGNB/QNG/BREEAM), `LCAModule`→Regelwerk
   (EN 15804); `Geltungsbereich` → drop (covered by `GILT_IN_LAND`).
4. **Snapshot + delete labels:** `Norm`, `RechtlicheBedingung`, route-`Bauproduktstatus`,
   `Geltungsbereich`, `Zertifizierungssystem`, `LCAModule` nodes + their now-orphan edges.
**Acceptance:**
- `MATCH (:Norm) RETURN count(*)` = 0; same for RechtlicheBedingung/Geltungsbereich.
- Every project/BTG that had `REFERENZIERT_NORM` now has ≥1 `UNTERLIEGT_REGELWERK`.
- Gap nodes (`crow_cur`, `swiss_baupg`, `sia_500`) logged to `phase2_gaps.json` (not silently dropped).
**Rollback:** restore `phase2_before.json` + delete phase-2 `review_run` edges.

## Phase 3 — Schadstoff re-evidence (REFINED per `SEMANTIC_PROOF.md` P3)
**Goal:** keep the 13 substances, re-derive pollutant risk from **sourced** rules, drop the `inferiert`
spray **without losing any signal we can't reproduce**.
> Proof found two holes: (3.1) 5 pollutants — `s_radon`, `s_schimmel`, `s_chlorid`, `s_salze`,
> `s_mineraloel` — have no era/material rule (they're exposure/condition-based); (3.2) era-derivation
> reaches only 38/228 BTG. So derive via era **and** material, route the 5 via condition/location, and
> never delete a link we can't replace.
**Steps**
1. **Cite the rules:** set `source_url`/`quote` on `TYPISCH_BEI_ERA` **and** `TYPISCH_BEI_MATERIAL`
   from `POLLUTANT_ERA_EVIDENCE.md` (LfU Arbeitshilfe, TRGS 519/521, REACH, StrlSchG).
2. **Build the sourced spine via BOTH paths:**
   - `Bauwerk(era) → Schadstoff` (era-typical: asbest, pcb, pak, kmf, holzschutz, bleifarbe…).
   - `Material → Schadstoff` (material-typical: schwermetalle/metal, formaldehyd/MDF…) — covers the
     ~283 material-known BTG that lack era data.
   - then `→ Nachweisforderung(*Check) → Regelwerk` for each.
3. **Condition/location pollutants (the 5):** re-route, do NOT delete blindly —
   `s_radon → Land/Standort + StrlSchG` (`basis='location'`); `s_schimmel → Defekt(Feuchte) + UBA`
   (`basis='condition'`); `s_chlorid/s_salze/s_mineraloel → Defekt/exposure + VDI 6202` (`basis='condition'`).
4. **Name** `s_radon`.
5. **Retire `HAS_RISK_POLLUTANT` (754) + `REQUIRES_VERIFICATION_FOR` (339) ONLY where a sourced
   replacement now exists.** Any component-pollutant link with no era/material/condition basis →
   tag `screening_unverified` and **report for an explicit drop/keep decision** (no silent loss).
**Acceptance:** all 13 `Schadstoff` reachable by a *sourced* path (era/material/location/condition);
`HAS_RISK_POLLUTANT` remaining = only the `screening_unverified` set (reported, count in `phase3_report.json`);
0 silent losses; 13 substances intact.
**Rollback:** restore `phase3_before.json`.

## Phase 4 — PruefungNachweis dedup + Leistungsanforderung consolidate
**Goal:** clean controlled vocab; retire generic assignment edges.
**Steps**
1. **PruefungNachweis dedup:** detect `pn_*`/`pr_*` twins (`zugversuch`, `sichtpruefung`,
   `schadstoffanalyse`…); MERGE to the named canonical, redirect any edges, delete the duplicate;
   give names to bare `pn_*` ids (map table `phase4_pruefung_dedup.csv`, reviewed first).
2. **Link methods:** `(pn)-[:ERFUELLT_NACHWEIS]->(nf)` per the keyword map in `rewire_map.py`.
3. **Snapshot + retire** generic `HAT_PRUEFUNG` (465) — replaced by overlay `ERFORDERT_NACHWEIS`.
4. **Leistungsanforderung consolidate:** merge fire cluster (`brandschutz/brandverhalten/feuerwiderstand/
   f90/r90/rei90`→`la_feuerwiderstand`) and thermal/acoustic clusters → ~20 canonical; redirect edges;
   retire generic `HAT_LEISTUNGSANFORDERUNG`; keep concrete ones linked to the matching Nachweis.
**Acceptance:** 0 `pn_/pr_` duplicate pairs; 0 nameless PruefungNachweis; `HAT_PRUEFUNG`=0;
Leistungsanforderung ≤ ~22; every method has `ERFUELLT_NACHWEIS`.
**Rollback:** restore `phase4_before.json`.

## Phase 5 — Huerde **B-clean** (evidenced barrier vocabulary) + Tier-F deletions
**Goal:** turn the least-evidenced label into a small sourced "Reuse-Hemmnis" vocab; remove orphans.
**5.1 Controlled barrier vocabulary (keep 11, add `category` from Rakhshan 2020)**
| Huerde node | Rakhshan category | connect to | basis |
|---|---|---|---|
| h_heterogenitaet_chargen, h_unkonventionelles_material | Technical/Quality | **Bauteilgruppe** | material_derived |
| h_akzeptanzproblem | Social/Perception | Projekt | taxonomy/case |
| h_mengenunsicherheit, h_verfuegbarkeitsproblem | Market/Supply | Projekt | taxonomy/case |
| h_terminunsicherheit, h_entwurfsbindung | Organisational | Projekt | taxonomy/case |
| h_fehlende_lagerflaeche, h_witterung_feuchte | Logistics | Projekt | taxonomy/case |
| h_aufbereitungsaufwand | Economic | Projekt | taxonomy/case |
| h_ausschreibungsproblem | Regulatory/Procurement | Projekt (+`rw_zirkulaere_vergabe`) | case |

**5.2 Evidence sources:** add `Quelle` for Rakhshan et al. (2020) systematic review
(https://pmc.ncbi.nlm.nih.gov/articles/PMC7472835/) + FCRBE; these back the vocabulary.
**5.3 Reconnect (script `phase5_huerde_reconnect.py`):**
- **Material-derived → Bauteilgruppe:** concrete/composite BTG → `h_heterogenitaet_chargen`
  (concrete service-life/heterogeneity), composite → quality/separation; `basis='material_derived'`,
  cite Rakhshan + concrete-reuse study. Steel deliberately few (literature).
- **Project barriers → Projekt:** for projects **with a real source** (33–86 via `BELEGT_IN`/`Dossier`),
  a per-project extraction pass reads the case text and attaches only the documented barriers
  (`basis='case_documented'`, `source_url`=project source). For the rest, attach the dominant taxonomy
  barriers (perception/risk/market) `basis='taxonomy_derived'`, cite Rakhshan.
**5.4 Delete:** the ~13 regulatory Huerde + `HuerdeKategorie` + **all 930 old `inferiert` `HAT_HUERDE`**
(snapshot first). New evidenced `HAT_HUERDE` edges carry `source_url`+`basis`.
**5.5 Tier-F deletions (snapshot each):** `Akzeptanz` (+edges), `OntologyAnchor`+`ANCHORED_BY`,
`STUB_PROJECT_LINK`, `GEHÖRT_ZU`, `Wirtschaft`, `MatchingQualitaet`→3 BTG/Projekt properties
(`match_geo`,`match_spec`,`match_temporal`).
**Acceptance:** `Huerde`=11, each with `category` + only evidenced edges (every `HAT_HUERDE` has
`source_url`+`basis`); 0 `inferiert` HAT_HUERDE; `Akzeptanz`/`OntologyAnchor`/`MatchingQualitaet`=0.
**Rollback:** restore `phase5_before.json`.

## Phase 6 — Consolidate duplicate axes
**Steps (each: redirect edges → set property/merge node → delete old; snapshot first)**
1. `Marktmodell` → `Beschaffungsweg` (merge equivalent values; redirect `HAT_MARKTMODELL`→`HAT_BESCHAFFUNGSWEG`).
2. `Wiederverwendungsort`, `Funktionswechsel` → BTG **properties** (`wv_ort`, `funktionswechsel`); delete labels.
3. `Tragwerksprinzip` → `Bauweise` (map 4 values); `Bauobjektklasse` non-use values → `Nutzung`, delete rest.
4. `Layer` → `Bauteiltyp.layer` property; `Bauteilebene` → `Bauteilgruppe.ebene` property.
5. `ExternalLink` → unify under `Quelle` (add `:Quelle` label / `quelltyp='external_link'`); `Tool`→`Software`.
**Acceptance:** merged labels count = 0; redirected edge counts preserved (no orphans); properties present.
**Rollback:** restore `phase6_before.json`.

## Phase 7 — Final audit & handoff
**Steps**
1. `python audit_edges.py` (extended to whole graph) + `python _scripts/_gap_survey.py`.
2. Label inventory + evidence-coverage recount.
3. Write `FINAL_AUDIT_REPORT.md`; update `AGENTS.md` / `HANDOFF.md` with the new node count.
**Acceptance (target clean state):**
- **~34 labels** (from 62).
- **0** `inferiert`/`unklar` regulation edges remaining; **every** regulation edge has `source_url`.
- One law layer (`Regelwerk`); `Norm`/`RechtlicheBedingung`/`Geltungsbereich`/`Zertifizierungssystem`/
  `LCAModule` gone.
- `Huerde`=11 evidenced; orphans (`Akzeptanz`,`OntologyAnchor`) gone; no duplicate axes.
- All consistency/gap checks return 0.

---

## Effort / sequencing notes
- Phases 1–4, 6 are mostly **scripted & ready** (overlay, rewire_map, audit exist). Phase 0 (encoding)
  and Phase 5 (Huerde per-project extraction) need **new small scripts + one research/extraction pass**.
- Phase 5's `case_documented` extraction is the only research-heavy step; `taxonomy_derived` is the
  v1 fallback so Phase 5 isn't blocked on it.
- Recommended first delivery: **Phase 0 + Phase 1** (backup + encoding + apply validated overlay),
  re-audit, then proceed phase-by-phase with a go-ahead each.

## Open items before execution
- Confirm start with **Phase 0 + 1**.
- For Phase 5 `case_documented`: confirm I should do the per-project barrier extraction pass (reads the
  ~33–86 project sources), or ship `taxonomy_derived` first and upgrade later.
