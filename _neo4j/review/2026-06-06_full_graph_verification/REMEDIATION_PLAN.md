# Remediation Plan — Full-Graph Verification Campaign

**Agent:** 15 (Aggregator) · **Date:** 2026-06-06 · **Database:** `mit-bestand`
**Source:** `VERIFICATION_LEDGER.csv` (8,284 rows incl. Agent 06b) · **Status:** partial apply (see §9).

> **Apply discipline (unchanged):** every mutation goes through the gated tool
> `_scripts/apply_neo4j_review_patch.py` → **dry-run** → human `--confirm "APPLY <patch> TO mit-bestand"`.
> The only artifact pre-built here is the **non-destructive** node-source patch (§3). All destructive groups
> (DELETE, MERGE_DUPLICATE, DEPRECATE_NODE) are listed for a **human-built** gated patch.

Action totals across the merged ledger: KEEP 6,374 · ADD_SOURCE 636 · RESOURCE 450 · ESCALATE_HUMAN 215 ·
MERGE_DUPLICATE 132 · RELABEL 70 · FIX_PROPERTY 16 · DELETE 3.

---

## 1. DELETE (destructive — 3 edges, human-gated)

High-confidence UNSUPPORTED edges (consortium/category inference, evidence URL never names both endpoints):

| from → to | type | basis of removal | source agent |
|---|---|---|---|
| `rotordc → p_architecture_of_reuse_brussels` | `BETEILIGT_AN` | page names only *Rotor*, not *RotorDC*; no actor named | 02 |
| `circular_berlin → kunst_stoffe_ev` | `VERBUNDEN_MIT_AKTEUR` | DBU "Reallabor" consortium ≠ pairwise tie; page never names both | 06 |
| `kunst_stoffe_ev → material_mafia` | `VERBUNDEN_MIT_AKTEUR` | page names Material Mafia, **not** Kunst-Stoffe | 06 |

→ Build `delete_unsupported.patch.jsonl` (`{"op":"delete_rel","from":…,"type":…,"to":…,"reason":…}`) exactly like the
audited `unsupported_edges_removal.patch.jsonl`. **Not auto-generated here** (destructive). Full list:
`_agent15_work/destructive_proposals.json`.

## 2. RELABEL / RESOURCE (downgrade or re-source — non-deletion, 520 items)

- **RELABEL (70):** mostly Agent 09 (63) — `BETEILIGT_AN`/geo edges whose evidence supports a weaker claim;
  downgrade `confidence`/`connection_kind` rather than assert. Also 03 (3), 01 (2), 10 (2).
- **RESOURCE (450):** find a correct URL. Agent 09 (367) weak/placeholder geo evidence (`processed`, `archive`),
  Agent 07 (63) dead/paywalled regulation links, plus 10/03/01/02/14. Includes Agent 14's
  **353-row `needs_source_url_review` backlog** (HAT_BAUTEILTYP 142, NUTZT_MATERIAL 103, BETEILIGT_AN 63 …).

→ These are property edits (`set_rel_properties`) but **require a freshly fetched correct URL first**; do not
auto-patch. Route RESOURCE batches back to the Tier-A web agents.

## 3. ADD_SOURCE (non-destructive — patch drafted for the high-confidence subset)

636 ADD_SOURCE proposals total (525 MISSING_EVIDENCE candidates, 93 PARTIAL, 17 PROVEN, 1 UNVERIFIABLE).

- ✅ **Applied:** `patches/agent15_add_node_sources.patch.jsonl` — **17 `set_node_properties`** (Agent 08 PROVEN).
  Live apply 2026-06-06: **17 updated / 0 errors**
  (`apply_reports/agent15_add_node_sources.patch.apply_report.md`).
- ✅ **Applied:** `patches/agent06b_add_node_sources.patch.jsonl` — **42 `set_node_properties`** (Agent 06b PROVEN).
  Live apply 2026-06-06: **42 updated / 0 errors**
  (`apply_reports/agent06b_add_node_sources.patch.apply_report.md`).
- ⏸ **Deferred (619):** the remaining ADD_SOURCE rows are *candidate* URLs (MISSING_EVIDENCE/PARTIAL) — not yet
  fetched-and-confirmed at endpoint level. Each needs a confirming fetch before it can be written. **Do not
  auto-trust** (AGENTS.md rule + the demoted-candidate caveat in the evidence audit).

**Top priority within ADD_SOURCE:** the **22 `Materialdepot` nodes with 0 sources** (Agent 10). Per the
Definition-of-Done each must gain a source or be `ESCALATE_HUMAN`.

## 4. MERGE_DUPLICATE (destructive — 132 items, human-gated)

- **88 bidirectional `VERBUNDEN_MIT_AKTEUR` pairs** (Agent 14) — both `a→b` and `b→a` exist (dedup regression).
  Collapse to one canonical direction. e.g. `eth_zuerich↔fabio_gramazio`, `madaster↔rau`, `Rotor↔opalis`,
  `gruner_ag↔gruner_reuse_platform`.
  - ✅ **Applied (wave-1):** `merge_duplicate_edges_remaining.patch.jsonl` — **23 `delete_rel`** reverse legs
    (`apply_reports/merge_duplicate_edges_remaining.patch.apply_report.md`).
  - ✅ **Applied (06b):** `agent06b_merge_duplicate_reverse.patch.jsonl` — **63 `delete_rel`** reverse legs.
  - ⏸ **2 pairs remain** (`madaster↔rau`, `madaster↔thomas_rau`) — escalated pending RAU identity decision.
- **44 node/entity duplicates** (Agent 08 ×20, 10 ×11, 03 ×6, 01 ×5, 05 ×2) — e.g. `software_qflow`↔`qualisflow`.
  - ✅ **Applied (wave-1):** `merge_duplicate_nodes_high_confidence.patch.jsonl` — **8 `merge_node`**
    (`apply_reports/merge_duplicate_nodes_high_confidence.patch.apply_report.md`).
  - ✅ **Applied (R03, 2026-06-06):** `remediation_r03_merge_nodes.patch.jsonl` — **11 `merge_node`**
  (ZRS triple→`zrs_ingenieure`, IEMB composite→`iemb_tu_berlin`, EPFL SXL, Albert & Co, BTU Cottbus, Claus Asam,
  Archipel zéro, Pirmin Jung AG, Tampere University ×2). Live apply: **2295→2284 nodes / 15340→15312 rels**
  (`apply_reports/remediation_r03_merge_nodes.patch.apply_report.md`; report `reports/remediation_r03.md`).
  - ⏸ **17 deferred** from R03 ledger (9 ESCALATE_HUMAN — Paris STP, BIM triple, `prog_recreate_local`, `rau`↔`rau_architects`;
    4 REJECT — `herve_joel_biele`, Oogstkaart vs HarvestMAP; 2 REFERENCE_R04 — `harvestmap`, `rau`↔`thomas_rau`;
    2 KEEP hierarchy — `iemb_tu_berlin`≠`tu_berlin`, `structural_xploration_lab_epfl`≠`epfl`).

→ Remaining edge dedup: human-gate any new `merge_duplicate_edges.patch.jsonl` for the 2 `madaster` pairs.
Node dupes: **never auto-merge on name similarity** (AGENTS.md rule 3); R03 merges required org URL / legal entity /
institute proof (`ledger/remediation_r03.csv`).

## 5. DEPRECATE_NODE (candidates — human decision)

No shard emitted the literal `DEPRECATE_NODE` action, but these are deprecation candidates:

- ✅ **3 orphan `Akteur` connected (R05, 2026-06-06):** `c33_circular_construction_catalyst`→`land_schweiz`,
  `circular_economy_switzerland`→`land_schweiz`, `repurpose`→`land_niederlande` via `LIEGT_IN_LAND`;
  `repurpose.land` scalar dropped. Deprecation **not** applied.
- **8 orphan vocab stubs** (Agent 12, 0 incoming edges, `name==id`): `bt_fassadenelement`,
  `bt_fassadenmodul_mauerwerk`, `bt_glasscheibe`, `bt_hohlkoerperdecke`, `bt_mauerstein`, `bt_verglasung`,
  `mat_drahtglas`, `mat_spannbeton` → either give a curated name (FIX_PROPERTY) or DEPRECATE; they overlap
  curated nodes (`bt_fassade`, `bt_fenster`, `mat_glas`, `mat_beton`).

→ ESCALATE_HUMAN to choose name-vs-deprecate; then a gated `delete_node`/`set_node_properties` patch.

## 6. FIX_PROPERTY (schema cleanup — 16 items)

- Agent 14: `nutzung_role`→`role` and `bauwerk_role`→`role` on the OXY/Rotor donor edges; drop stray
  `additional_marktmodelle` (`enviromate`), `needs_evidence_urls`/`evidence_urls_target` (`mobius_reemploi`);
  drop redundant scalar `land` on 6 actors (verify `LIEGT_IN_LAND` edge exists first).
  - ✅ **Applied (R05):** `remediation_r05_fix_property.patch.jsonl` — **1 `remove_node_properties`**
    (`repurpose.land`); 8× `noop_reviewed` (vocab names already live).
  - ✅ **Applied (R05):** `remediation_r05_connect_orphans.patch.jsonl` — **3 `add_rel` `LIEGT_IN_LAND`**.
- Agent 12 (8), 09 (2), 10 (1): vocab name backfills / property corrections.
- **Schema re-baselining (Agent 14 DRIFT):** node property keys **83 vs approved 57**, rel keys **51 vs approved 22**.
  Most additions are legitimate June intakes (geo `latitude/longitude/geo_*`, `entwurfsqualitaet_*`, vocab
  `name_de/literature_ref/intake_run`). **Action: re-baseline the approved-key ledger + AGENTS.md "Aktueller
  Stand"** — this is documentation drift, not corruption.

## 7. ESCALATE_HUMAN (215 items — judgment required)

| Source | Count | Theme |
|---|---:|---|
| 09 | 96 | geo/participation ambiguities, possible contradictions |
| 10 | 56 | software/depot/programme identity uncertain; all Materialdepots unsourced |
| 01 | 23 | CH actor/edge judgment calls |
| 13 | 11 | **dangling `Nachweisforderung`** — add `ERFUELLT_NACHWEIS` coverage or downgrade the requirement |
| 08 | 9 | unverifiable/paywalled actors |
| 14 | 6 | orphans, singleton reltype, key drift re-baseline |
| 05, 12, 03 | 8 | NL mesh checks, vocab stubs, DE judgment |

- ✅ **Applied (R02):** `remediation_r02_erfuellt_nachweis.patch.jsonl` — **10 `add_rel` `ERFUELLT_NACHWEIS`**
  covering **7** high-confidence dangling `Nachweisforderung` types (Agent 13). Live apply 2026-06-06:
  **10 created / 0 errors**, rel total **15,330 → 15,340**
  (`apply_reports/remediation_r02_erfuellt_nachweis.patch.apply_report.md`). **11** dangling requirements
  remain (5 need new `PruefungNachweis`, 6 medium-confidence only). See `reports/remediation_r02.md`.

## 8. COVERAGE re-dispatch (precondition for Definition-of-Done)

- ✅ **R1 — Agent 06b (non-bubble actor networks):** **complete** (`ledger/agent_06b.csv`, 386 claims).
  True gap was **218 edges + 168 nodes**. **0/218 edges had on-graph evidence** at audit.
- ✅ **R1b — Agent 15b merge:** **complete** (`_agent15b_aggregate.py` → `VERIFICATION_LEDGER.csv` 8,284 rows).
- **06b remediation patches:**
  - ✅ **Applied:** `agent06b_relabel_connection_kind.patch.jsonl` — **12 `set_rel_properties`**
    (`consortium_co_membership` downgrades). Live apply 2026-06-06: **12 updated / 0 errors**
    (`apply_reports/agent06b_relabel_connection_kind.patch.apply_report.md`).
  - ⏸ **Human gate:** `agent06b_delete_self_loop.patch.jsonl` — 1 `delete_rel`
  - ⏸ **Human gate:** `agent06b_merge_duplicate_reverse.patch.jsonl` — 63 `delete_rel` reverse legs
- **R2/R3 (optional):** re-run Agents 12 & 13 in per-edge enumerate mode if element-level attestation is required
  for the 9,092 Tier-C edges / 1,040 vocab+process nodes.

## 9. Suggested apply order

**Wave 1 (campaign, 2026-06-06)**

1. ✅ `agent15_add_node_sources.patch.jsonl` — **applied** (17 node sources).
2. ✅ `agent06b_add_node_sources.patch.jsonl` — **applied** (42 node sources).
3. ✅ `agent06b_relabel_connection_kind.patch.jsonl` — **applied** (12 connection_kind downgrades).
4. ✅ `agent06b_delete_self_loop.patch.jsonl` + `agent06b_merge_duplicate_reverse.patch.jsonl` +
   `delete_unsupported.patch.jsonl` — **applied** (1 + 63 + 3 `delete_rel`).
5. ✅ `fix_property.patch.jsonl` + `merge_duplicate_edges_remaining.patch.jsonl` +
   `merge_duplicate_nodes_high_confidence.patch.jsonl` — **applied** (16 ops + 23 + 8 dedup).

**Wave 2 — R01–R07 (2026-06-06)**

6. ✅ `remediation_r01_materialdepot_sources.patch.jsonl` — **applied** (5 `set_node_properties`; 17 depots deferred).
7. ✅ `remediation_r04_madaster_rau_harvestmap.patch.jsonl` — **applied** (7 ops; 2296→2295 / 15338→15327).
8. ✅ `remediation_r06_regulation_urls.patch.jsonl` — **applied** (63 `set_rel_properties`; property-only).
9. ✅ `remediation_r05_connect_orphans.patch.jsonl` + `remediation_r05_fix_property.patch.jsonl` — **applied**
   (3 `LIEGT_IN_LAND`, 1 `land` drop; deprecations deferred).
10. ✅ `remediation_r02_erfuellt_nachweis.patch.jsonl` — **applied** (10 `ERFUELLT_NACHWEIS`; +10 rels).
11. ✅ `remediation_r03_merge_nodes.patch.jsonl` — **applied** (11 `merge_node`; 2295→**2284** / 15340→**15312**).
12. ✅ `remediation_r07_add_rel_sources.patch.jsonl` — **applied** (137 `set_rel_properties`; 0 errors;
    graph unchanged at **2284 / 15312**).

**Outstanding**

13. Human-gate R03-deferred node dupes (17) + R04 `rau`↔`rau_architects` + founder-edge semantics.
14. FIX_PROPERTY patch (role renames, remaining stray-key drops beyond R05).
15. R07 residual **171 RESOURCE** + **6 MISSING_EVIDENCE**; R01 **17** Materialdepots; R02 **11** dangling NF.
16. ESCALATE_HUMAN review (geo/participation, vocab-stub deprecations, key re-baseline).
17. Re-run Agent 14 hygiene; see [`WAVE2_SUMMARY.md`](WAVE2_SUMMARY.md).

`AGENTS.md` "Aktueller Stand" updated to **2 284 nodes / 15 312 rels** (2026-06-06 post-R07).
