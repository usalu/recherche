# Next steps — post batch2 v2 + Phase 16/17 (2026-05-20 evening)

**Current state:** 2 538 nodes / 18 651 rels in `mit-bestand`. Batch2 v2 + Phase 16 (new vocab) + Phase 17 (Zirkular dedup) all applied successfully. See [rollback.md §Phase batch2 v2](../../review/round_002_followup/rollback.md) for the audit trail.

**Survey findings drove this plan.** A quick live-graph audit surfaced 5 categories of post-apply gaps that should be closed before moving to batch3. They're ordered by priority + effort.

---

## §A — Immediate cleanups (small, this-session-feasible) — Phase 18

These are bugs/omissions in batch2 v2 work, not new content. ~30 patch ops total.

### A1 — `node_role` cleanup on 11 dual-labelled `:Programm:Projekt` nodes
**Issue:** When a Programm absorbed a Projekt stub via merge_node, the merged node inherited `node_role='cross_reference_stub'` from the source. The 11 dual-labelled nodes (`prog_fcrbe`, `prog_mas_dfab`, `prog_re_use_hoefe`, `prog_reallabor_be_ware`, `prog_rebridge`, `prog_stuttgart_210`, plus the 5 Projekt-side promotions whose `node_role` may not have stuck) still report `node_role='cross_reference_stub'`. Should be `full_projekt` or removed entirely (Programm doesn't need node_role).

**Fix:** Phase 18a — `set_node_properties` on each, set `node_role='full_projekt'` (or `remove_node_properties` if Programm-only).

**Estimated:** 11 set_node_properties ops.

### A2 — BETEILIGT_AN backfill for 22 deg-0/1 Akteure
**Issue:** Several Akteure created in Phase 5/13 got `HAT_AKTEURROLLE` + `HAT_AKTEURTYP` but no `BETEILIGT_AN` to a Projekt. Affected:

- `drz_demontage_recycling`, `die_kuemmerei`, `wiener_aufzugmuseum` → `p_meduni_campus_mariannengasse`
- `icon_real_estate`, `victory_group` → `p_circl_abn_amro`
- `la_fabrique_de_bordeaux_metropole` → previously REFAIR Projekt was deleted; should it link to a substitute? Options: link to existing Projekts where La Fab operates as `ar_materialbroker`; or accept orphan-without-project (it's a platform operator). Decision needed.
- `university_of_fribourg` → `p_reuse_logistics` (parent project) + `prog_urban_bricolage`
- `kanton_basel_stadt` → `p_elementa_walkeweg` (already added via funder rel — verify or add)
- `brussels_capital_region` → `p_careno_becircular` via `ERHALT_FOERDERUNG_DURCH` (already added in Phase 5b)
- `proholz_bw`, `ed_zueblin_ag` → `prog_stuttgart_210` (re-verify; Phase 5b may have missed some)
- `bbri` → `p_careno_becircular` (added in Phase 5b, verify)

**Fix:** Phase 18b — add_rel BETEILIGT_AN edges with `rolle_text`. ~10-12 missing edges.

### A3 — KEEP-STUB Akteure orphan reduction
**Issue:** 12 KEEP-STUB Akteure remain degree 0 or 1 per PARKED_DECISIONS recommendation: glasfischer_glastec, heinrich_boell_stiftung, koimo_development, mehr_als_wohnen, stiftung_habitat, citydev_brussels, denkstatt, edith_maryon_stift, eitel_partner, gibbins_architekten, kunst_stoffe_ev, zusammenkunft_berlin.

**Some are linkable from dossier evidence:**
- `mehr_als_wohnen` → LysP8 dossier mentions "Zurich housing estate" kitchens — Mehr als Wohnen Zürich is a likely donor. Add `BETEILIGT_AN → p_lysp8_basel` with rolle_text="kitchen donor (Zurich housing estate)".
- `stiftung_habitat` → LysP8 already named as client; verify edge exists, add if missing.
- `eitel_partner` → LysP8 already named as construction manager; verify.
- `kunst_stoffe_ev` → Berlin reuse association; could link to `prog_reallabor_be_ware`.

**Fix:** Phase 18c — 4-6 connectivity edges from dossier evidence.

### A4 — Werner_Sobek alias preservation check
**Issue:** Phase 1b merged `werner_sobek_p → Werner_Sobek`. The apply tool should have UNIONed aliases, but `werner_sobek_p` had no `aliases` property before. Verify Werner_Sobek now has `aliases` including the historical id slug.

**Fix:** Phase 18d — `canonicalize_node Werner_Sobek` with aliases=["werner_sobek_p", "Werner Sobek (canonical pre-merge)"].

### A5 — q_actor_* Quelle stragglers
**Issue:** When `p_obk_27`, `p_rcmi_concular`, `p_refair_bordeaux_reemploi_platform` were deleted, their `q_actor_*_01/02/03` Quellen lost the project context but remain linked to the Akteure. These Quellen titles still reference the deleted projects (e.g., "Pavilion Circl Amsterdam", "FCRBE"). Stale but harmless.

**Fix:** Phase 18e — optional `set_node_properties` on the affected Quellen to drop the stale project name from their `name`/`titel`. Or leave as-is. **Recommendation:** leave as-is; they're still valid bibliographic citations.

---

## §B — Phase 19: BG enrichment for the remaining ~50 BGs (Phase 6 + 11 didn't fully cover)

### B1 — Existing-corpus BGs missing optional vocab
**Issue:** Phase 11 added optional vocab (HAT_BESCHAFFUNGSWEG / HAT_VERBINDUNGSTECHNIK / etc.) to 42 of the 61 batch2 BGs, but the deferred 19 from Phase 12 got their own optional vocab via Phase 12b. The other ~300 pre-existing BGs in the graph have varying degrees of vocab coverage.

**Survey query** to scope this:
```cypher
MATCH (bg:Bauteilgruppe) WHERE bg.source_scope <> 'case_markdown' OR bg.source_scope IS NULL
WITH bg, [(bg)-[r]->() | type(r)] AS rels
RETURN bg.id, size(rels) AS vocab_count, rels
ORDER BY vocab_count ASC LIMIT 20;
```
Run this; identify BGs with vocab_count < 5 (i.e., missing most optional vocab). Then research-and-fill per dossier in a follow-up batch.

**Effort:** Hard to estimate without running the survey. Likely **batch3 candidate** (research time per BG).

### B2 — `counts_as_*` property backfill
**Issue:** Phase P (2026-05-19) backfilled `counts_as_direct_reuse` on 5 Projekte but the property is missing on ~40 BGs (per Phase P review). The new batch2 v2 BGs were created with `reuse_status` but not `counts_as_*`.

**Fix:** Derive `counts_as_direct_reuse = (reuse_status = 'reuse')` etc. Phase 19b — bulk `set_node_properties`.

**Estimated:** ~60 set_node_properties ops.

### B3 — `alte_funktion` / `neue_funktion` consistency
**Issue:** Phase 6a set these properties for the 7 Funktionswechsel BGs. Other BGs may benefit from explicit alte/neue function annotations even when no FW happens (alte=neue is informative).

**Fix:** Phase 19c — bulk fill where dossier evidence is clear; skip where ambiguous.

---

## §C — Phase 20: Cross-Bauwerk reuse chain discovery + Wiederverwendungskette wiring

### C1 — Implicit donor→receiver links between Bauwerks
**Goal:** Many batch2 BGs have `AUS_BAUWERK` (donor) and `EINGEBAUT_IN` (receiver). The implicit chain Bauwerk→BG→Bauwerk should be captured at the Bauwerk level as new Wiederverwendungskette nodes where it isn't already.

**Survey:**
```cypher
MATCH (donor:Bauwerk)<-[:AUS_BAUWERK]-(bg:Bauteilgruppe)-[:EINGEBAUT_IN]->(receiver:Bauwerk)
WHERE donor <> receiver
  AND NOT EXISTS { (bg)-[:TEIL_VON_KETTE]->(:Wiederverwendungskette) }
RETURN donor.id, receiver.id, count(bg) AS bg_count;
```
For every donor-receiver pair with no kette, create one.

**Effort:** ~5-15 new ketten depending on survey. **Phase 20a** generator script.

### C2 — Multi-BG ketten expansion
**Goal:** Existing ketten typically have 1-3 BGs. Extend with the full BG list per chain.

For example, `wk_circl_larch_dismantling_chain` currently has 1 BG (`bg_dismantled_holz_mehrere_circl_larch_structure`). The dossier evidence supports adding more dismantled Circl BGs as part of the same chain.

**Effort:** ~20 additional `TEIL_VON_KETTE` edges. **Phase 20b**.

---

## §D — Phase 21: New dossier batch (batch3 candidates)

These need fresh research outside the current inbox.

### D1 — Fill in `Architecture of Reuse Brussels` actor list
The Projekt stayed as `cross_reference_stub` per dossier "identified_programme: no". Per [actor_extraction_per_dossier.md §15-§17](actor_extraction_per_dossier.md), Rotor + RotorDC + CONIX RDBM + 3 named Persons should still be linked.

**Effort:** ~6 BETEILIGT_AN edges. Could be added inline; not strictly batch3.

### D2 — `Vandkunsten` + `ZHAW Reuse in Construction`
Same pattern: keep as Projekt; tag dossier-named actors. ~10 edges total.

### D3 — OBK_27 follow-up: Oberkampf Paris dossier
The OBK_27 stub was deleted in Phase 1a-2 (negative finding). But the dossier's leading candidate is *Oberkampf social housing in massive stone (Paris)* by Barrault Pressacco. `cyril_pressacco` and `thibaut_barrault` are now orphaned Akteure.

**Research needed:** verify Oberkampf project details, then create a proper `p_oberkampf_paris` Projekt + Bauwerk + actor links. **Batch3.**

### D4 — Stuttgart 210 reallabs 2-5
Phase 4a created `p_jugendtreff_ingersheim` as the first pilot. The HTWG dossier says "78 elements secured for four/five reallabs" — only the first is built. Future reallabs (Reallab 2 = Pavillon Ingersheim 2; Reallab 3-5 = TBD) need their own child Projekts as evidence emerges. **Batch3+.**

### D5 — FCRBE's 37 pilot operations cataloging
The FCRBE dossier mentions 37 pilot operations across NWE. Need to check whether these already exist in the graph (many are documented in `_archive/research/`) and add `TEIL_VON_PROGRAMM → prog_fcrbe` for those that don't.

**Effort:** ~37 TEIL_VON_PROGRAMM edges (one per pilot). **Batch3 research** + edge generation.

### D6 — Regional gaps
- **France**: only REFAIR + REBRIDGE (partner) so far. Add: dossiers for Bellastock-led projects, La Fab Bordeaux pilot buildings, French Réemploi case studies.
- **Iberia**: no Iberian projects yet. REBRIDGE has Coimbra partner.
- **Eastern Europe**: Ukraine added as Land but no project dossier yet.
- **US / Canada**: only Ecovative supplier so far.
- **Asia**: stadt_kamikatsu (Japan) exists with no dossier.

**Batch3+** research priorities.

---

## §E — Phase 22: Schema / tooling improvements (low-priority polish)

### E1 — Tooling: `remove_label` op in apply tool
**Need:** Strip `:Projekt` label from the 6 dual-labelled `:Programm:Projekt` nodes (`prog_fcrbe`, `prog_mas_dfab`, etc.) if you want strict semantic clarity. Decision pending per [NEXT_STEPS.md §B5](NEXT_STEPS.md).

**Effort:** Tool extension (~20 lines Python) + 1 patch op per node.

### E2 — Tooling: relax `--confirm` to support batch mode
Currently each patch needs its own `APPLY <filename> TO mit-bestand`. The orchestrator [`_apply_batch2_v2_all.py`](../../../_scripts/_apply_batch2_v2_all.py) handles this but it's verbose. Consider `--confirm-all` flag for orchestrators.

### E3 — Rename `GEHÖRT_ZU` → `GEHOERT_ZU` corpus-wide
**Rationale:** 255 GEHÖRT_ZU rels live. The apply tool's regex was patched in this session to allow Unicode, but downstream tools (frontends, exports) may still struggle. ASCII-only would be cleaner long-term.

**Cost:** One-time rename of 255 rels via Cypher. ~2 hours including verification.

**Decision:** Defer unless a frontend or export pipeline complains.

### E4 — `HAT_FUNKTIONSWECHSEL` rel type
**Status:** Phase 16 NEW_NODE_SUGGESTIONS §H1 flagged this for verification. The 6 `fw_*` nodes exist in the graph but nothing points to them. Likely the original taxonomy author intended a `HAT_FUNKTIONSWECHSEL` rel type that was never wired.

**Verify:**
```cypher
MATCH ()-[r]->(:Funktionswechsel) RETURN type(r), count(*);
```
Expected: 0 rows (no rel type points to Funktionswechsel currently).

**Fix:** Either drop the 6 fw_* nodes (orphans), or wire them via a new `HAT_FUNKTIONSWECHSEL` rel from BGs that have alte_funktion/neue_funktion set.

**Effort:** ~7 add_rel ops (one per Funktionswechsel BG from Phase 6a/12a, targeting `fw_neue_funktion` or `fw_konstruktive_funktion`).

### E5 — `Region` label introduction (deferred per NEW_NODE_SUGGESTIONS §F)
Revisit when ≥10 region-level entities accumulate. Currently 2 (Brussels-Capital Region as Akteur; Nouvelle-Aquitaine unused).

### E6 — `bt_belag` decision (deferred per NEW_NODE_SUGGESTIONS §G)
Currently all "Belag" slots use `bt_boden`. Add a `belag_oder_tragend` property on BG to disambiguate if needed.

---

## §F — Phase 23: Corpus-wide consistency passes (Phase R-style)

### F1 — Re-run r.id integrity check
Phase R (2026-05-19) cleaned up 2 523 stale r.id strings. New batch2 v2 rels may have introduced fresh staleness, especially from `merge_node` operations.

**Verify:**
```cypher
MATCH ()-[r]->() WHERE r.id IS NULL
   OR r.id <> 'r_' + startNode(r).id + '__' + type(r) + '__' + endNode(r).id
RETURN type(r), count(*) ORDER BY count(*) DESC;
```
Expected: 0 rows. If non-zero, re-run `_scripts/_apply_phase_r_full.py` (or equivalent).

### F2 — Source-scope completeness
**Verify:**
```cypher
MATCH (n) WHERE n.source_scope IS NULL AND any(l IN labels(n) WHERE l IN ['Projekt','Bauteilgruppe','Bauwerk','Wiederverwendungskette','Stadt','Akteur','Quelle','Programm']) RETURN labels(n), count(n);
```
Identify nodes still without source_scope; backfill where origin is known.

### F3 — Quelle name length compliance
Per NAMING_AND_PROPERTIES_PLAN, Quelle names should be ≤25 chars. Check:
```cypher
MATCH (q:Quelle) WHERE size(q.name) > 25 RETURN q.id, q.name, size(q.name);
```
Fix offenders via `set_node_properties`.

### F4 — `aliases` UNION verification
**Verify** that the 7 nodes with aliases (per NAMING_AND_PROPERTIES_PLAN §0) still have their pre-existing aliases AND the new ones added in batch2 v2:
- `imd_raadgevende_ingenieurs`, `cleveland_steel_tubes`, `rotor_dc` (deleted; verify aliases on `rotordc`), `duncan_baker_brown`, `land_daenemark`, `p_lysp8_basel`, `p_eth_circular_construction_student_reuse` (deleted; verify aliases on `prog_mas_dfab`).

---

## §G — Suggested execution sequence

| Step | Phase | What | Effort | Risk |
|---:|---|---|---|---|
| 1 | A1-A5 | Immediate cleanup (node_role, BETEILIGT_AN gaps, KEEP-STUB orphan linking, alias verify) | ~30 patch ops | Low |
| 2 | F1-F4 | Phase R-style consistency (r.id, source_scope, aliases) | Survey + fixes | Low |
| 3 | B1-B3 | BG enrichment for pre-existing corpus BGs missing optional vocab | Research-heavy | Medium |
| 4 | C1-C2 | Cross-Bauwerk Wiederverwendungskette discovery + multi-BG expansion | ~20-30 add_rel + ~10 add_node | Medium |
| 5 | D1-D2 | Quick wins: tag existing actors to Architecture-of-Reuse-BXL / Vandkunsten / ZHAW stubs | ~16 BETEILIGT_AN edges | Low |
| 6 | E4 | HAT_FUNKTIONSWECHSEL rel type — verify + introduce | ~7 add_rel | Low |
| 7 | E1 / E3 | Optional: strip Projekt label from dual-labels; GEHÖRT_ZU rename | Schema decisions | High visibility |
| 8 | D3-D6 | batch3 research dossiers (OBK_27 / Oberkampf, Stuttgart 210 reallabs, FCRBE pilots, regional gaps) | Multi-session research | High value |

---

## §H — Suggested next concrete action

**Option α** (recommended): Do **§A immediate cleanups** (Phase 18) live. Small (~30 ops), low risk, closes verified gaps. Could be a single `phase_batch2_v2_18.patch.jsonl`.

**Option β**: Do **§E4 HAT_FUNKTIONSWECHSEL** investigation + introduction. Cheap connectivity win for the 7 Funktionswechsel BGs.

**Option γ**: Do **§F consistency passes** first to ensure batch2 v2 didn't introduce any hygiene drift before piling on more work.

**Option δ**: Move straight to **batch3 research** (§D) — most value but requires fresh dossier research time outside this session.

---

## §I — Open questions still pending user decision

| # | Question | Status |
|---|---|---|
| E1 (from NEXT_STEPS) | Strip Projekt label from `:Programm:Projekt` dual-labels? | Pending |
| E3 | Rename GEHÖRT_ZU → GEHOERT_ZU corpus-wide? | Pending |
| E5 | Introduce `Region` label? | Defer until ≥10 entities |
| E6 | Introduce `bt_belag`? | Defer; bt_boden works |
| New | Do A5 (Quelle name cleanup) or leave stale-but-functional? | Leave (recommended) |
| New | A1: node_role on dual-labels = `full_projekt` or remove the property entirely? | Recommendation: `full_projekt` (preserves backward queries) |
| New | A2: `la_fabrique_de_bordeaux_metropole` BETEILIGT_AN target? REFAIR Projekt was deleted; should it link to a substitute project? | Likely accept "operator-without-project" status; the connectivity is via Software + Bauwerk + Persons |

---

## §J — Estimated final state if §A+§F+§D1-D2+§E4 all applied

| | Now | After §A | After §F | After §D1-D2 | After §E4 | Final |
|---|---:|---:|---:|---:|---:|---:|
| Nodes | 2 538 | 2 538 | 2 538 | 2 538 | 2 538 | **2 538** |
| Rels | 18 651 | ~18 685 | ~18 685 (cleanup) | ~18 701 | ~18 708 | **~18 708** |

Modest connectivity gain (~57 edges) but full hygiene + dossier coverage.

The bigger jumps come from batch3 (§D3-D6) which requires research outside this session.

---

**End of NEXT_STEPS_v2.md.**

Cross-references: [rollback.md §Phase batch2 v2](../../review/round_002_followup/rollback.md), [NEXT_STEPS.md](NEXT_STEPS.md) (the pre-apply plan, now mostly obsolete), [APPLY_ORDER.md](APPLY_ORDER.md), [NEW_NODE_SUGGESTIONS.md](NEW_NODE_SUGGESTIONS.md).
