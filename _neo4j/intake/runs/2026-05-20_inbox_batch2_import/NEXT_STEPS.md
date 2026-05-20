# Next steps — post batch2 v2 work

**Status (2026-05-20):** 28 JSONL patches + 1 Cypher script written, all dry-run clean. Ready to apply. See [APPLY_ORDER.md](APPLY_ORDER.md).

This doc plans the work *beyond* applying batch2 v2:

- §A — Apply batch2 v2 live (the next concrete action)
- §B — Immediate follow-ups (small patches needed to close known gaps within 1 day of apply)
- §C — Batch3 candidates (next research dossier batch)
- §D — Schema / tooling improvements
- §E — Open questions waiting on user decision

---

## §A — Apply batch2 v2 live

Recommended sequencing (5 stages, each verifiable independently):

### Stage 1 — Cleanup (steps 1-7; 24 ops)
- Phase 1a-1d-2b: deletes, Akteur merges, Circl merge, Projekt→Programm merges
- **Verify after:** count(:Projekt) = 96, count(:Programm) = 20 (17 + 3 new from 1d-2a)
- **Risk:** if step 3 (Rotor merge) produces unwanted dual-labels, revert and consider alternative

### Stage 2 — Shared infrastructure (steps 8-12; 171 ops)
- Phase 2 + 2b + 2c + 3a + 3b: Stadt, Land, Programm, Software, Tool, Norm, Bauwerk + their structural rels + Quellen
- **Verify after:** count(:Stadt) = 76, count(:Bauwerk) = 209, count(:Quelle) +20

### Stage 3 — Projekt promotion (steps 13-14; 68 ops)
- Phase 4a + 4b: promote 8 stubs + create 3 child Projekts + their LIEGT_IN/NUTZT_BAUWERK/TEIL_VON_PROGRAMM/BELEGT_IN
- **Verify after:** every promoted Projekt has node_role='full_projekt'

### Stage 4 — Akteur + Bauteilgruppe content (steps 15-21; 555 ops)
- Phase 5a + 5b + 5c (Cypher) + 6a + 6b + 7a + 7b
- **Verify after:** every new Akteur has HAT_AKTEURROLLE + HAT_AKTEURTYP; every new BG has the 7 mandatory rels + Projekt + Bauwerk + Funktionswechsel

### Stage 5 — Project-level vocab + bridges + cleanup migrations (steps 22-28; 131 ops)
- Phase 8 + 9 + 4c + 4d/4d2 + 4e/4e2
- **Verify after:** full Phase 10 verification block

Take a backup between each stage. If any stage fails, restore from that backup and amend.

---

## §B — Immediate follow-ups (within 1 day of apply)

These are small, well-defined patches that close known gaps.

### B1 — Expand Phase 5c GEHÖRT_ZU
The current Cypher template lists only 2 Person→Org pairs. The full list from [actor_extraction_per_dossier.md §O5](actor_extraction_per_dossier.md) is ~25 pairs. Write the full set:

```cypher
// stefan_perez → perez_schmidlin_bauingenieure (LysP8 / SMS Zürich)
MATCH (p {id:'stefan_perez'}), (o {id:'perez_schmidlin_bauingenieure'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_stefan_perez__GEHÖRT_ZU__perez_schmidlin_bauingenieure',
              r.source = 'batch2_v2_followup_2026-05-21';
// ... 24 more rows
```

**Estimated: 25 GEHÖRT_ZU edges, ~50 lines Cypher. Impact: +25 high-value Person↔Org edges.**

### B2 — External_reference Quellen (PLAN_v2 Phase 3 was case_markdown only)
PLAN_v2 §F16 called for ~30 `external_reference` Quellen per the high-value URLs identified per dossier. Phase 3a only created the 20 `case_markdown` Quellen. Write Phase 3c:

- For each high-value external URL (≥3 dossier references), create `Quelle {quelltyp: "external_reference", url, name, name_full, access_date}`.
- Selected list (~17 Quellen):
  - Circl: dutcharchitects.org/projects/circl-amsterdam (S1), abnamro.com opening release (S3), abnamro PDF report (S4), zuidas dismantling 2025 (S6), icon digital twin (S7)
  - Careno: rotordb.org/projects/careno-becircular (S1), rotordc.com/projects/re-tile (S2)
  - LysP8: zirkular.net/project/lysp8 (S1), swiss-arc.ch (S2), oxara.earth (S4)
  - MedUni: baukarussell.at/2020/09/03 (S2)
  - Stuttgart 210: baunetzwissen.de Jugendtreff (S7), holzbauoffensivebw.de (S5)
  - FCRBE: vb.nweurope.eu Interreg page (S1)
  - REBRIDGE: ke.uni-stuttgart.de/forschung/rebridge (R1)
- Then add BELEGT_IN edges from specific BGs/Akteure to the relevant external_reference Quelle (much richer per-claim sourcing).

**Estimated: ~17 Quelle add_nodes + ~80 BELEGT_IN edges. Impact: per-claim provenance traceable.**

### B3 — Fill in the ~19 deferred Bauteilgruppen
PLAN_v2 §VI.4 deferred ~19 BGs from the original 61-target. The patches now cover 42; the remaining are:

- **Circl extended (8 BGs)**: window-frame floor PCM concrete tiles, restored ABN AMRO furniture, leased lifts (mm_leasing), leased lighting (mm_leasing), Tarkett C2C iQ One floor, remountable façade (Donkergroen + De Groot & Visser), façade aluminium sections, roof terrace planting, greenery harvest
- **MedUni extended (3 BGs)**: bike workshop, heavy shelves, fluorescent tubes (hazardous removal)
- **BE-WARE TULIUM (4 BGs)**: timber-and-clay deck systems, flying foundation specifics, secured reallab inventory (78 elements), pilot fitout
- **RE_USE Höfe (2 BGs)**: Windows for Ukraine batch, Höfe yard logistics
- **Ingersheim secondary (1 BG)**: CLT offcuts for secondary elements
- **Granby (1 BG)**: bespoke waste-stream mixes

**Estimated: ~19 add_nodes + ~230 vocab rels (~7 per BG via the existing generator script). Impact: complete dossier-evidenced BG coverage.**

### B4 — Add fine-grained NUTZT_MATERIAL edges
Phase 6b wrote HAT_MATERIALGRUPPE (coarse) for each BG. The graph has 19 Material nodes and 134 existing NUTZT_MATERIAL rels (per S8 + rollback.md R-3). For each new BG that has a clear primary material, add `NUTZT_MATERIAL → mat_*`:

| BG | mat_* target |
|---|---|
| bg_dismantled_holz_mehrere_circl_larch_structure | mat_holz_larche (or mat_holz) |
| bg_reuse_holz_boden_circl_window_frame_floor | mat_holz |
| bg_reuse_metall_tuer_umar_wabbes_handles | mat_messing |
| bg_reuse_glas_keramik_fassade_umar_magna_glass | mat_recyclingglas |
| ... ~40 more |

**Estimated: ~40 NUTZT_MATERIAL rels. Impact: unlocks `MATCH (bg)-[:NUTZT_MATERIAL]->(m)<-[:TYPISCH_BEI_MATERIAL]-(pr)` recommendation query (rollback.md L810).**

### B5 — Address dual-label `:Programm:Projekt` semantics (user decision)
5 nodes now have both labels (prog_fcrbe, prog_reallabor_be_ware, prog_stuttgart_210, prog_rebridge, prog_re_use_hoefe). Decision: keep dual-labels or strip Projekt label? See user discussion above.

If stripping: write a Cypher script:
```cypher
MATCH (n:Programm:Projekt) WHERE n.id IN [
  'prog_fcrbe', 'prog_reallabor_be_ware',
  'prog_stuttgart_210', 'prog_rebridge', 'prog_re_use_hoefe'
] REMOVE n:Projekt;
```

**Impact: count(:Projekt) drops by 5 → 91; queries against `:Projekt {id:'p_fcrbe'}` start returning empty (good or bad depending on use case).**

### B6 — Extend Akteure to cover dossier-named Persons not yet in graph
Phase 5a created 26 new Akteur nodes. Several dossier-named Persons remain unrepresented:
- `mario_monotti`, `roger_keller`, `ana_olalquiaga` (ELEMENTA team)
- `pascal_hentschel`, `rebecca_brandmayer`, `laia_meier` (Zirkular team, LysP8)
- `dominik_campanella`, `julius_schaeufele`, `lenard_da_costa_kurek` (Concular CEO/Geschäftsführer/RCMI co-author)
- `michelle_schneider_zhaw`, `felix_dillmann` (RE-USE Höfe authors)
- `markus_meissner`, `thomas_romm` (BauKarussell, MedUni)
- ... ~25 more

**Estimated: ~25 Akteur add_nodes + ~75 typed rels + ~20 GEHÖRT_ZU. Impact: complete dossier-actor coverage.**

---

## §C — Batch3 candidates

After batch2 v2 + B1-B6 are applied, the next research dossier batch should target gaps that emerged during this work:

### C1 — `KEEP STUB` decisions from PARKED_DECISIONS that batch2 didn't touch
Per PARKED_DECISIONS list, 9 Projekt stubs were KEEP STUB:
- p_pavilion_circl_amsterdam ← already MERGED in batch2 ✓
- p_circl_abn_amro ← already PROMOTED ✓
- p_careno_becircular ← already PROMOTED ✓
- p_meduni_campus_mariannengasse ← already PROMOTED ✓
- p_schaerenmoosstrasse_zuerich ← already PROMOTED ✓
- p_umar_unit ← already PROMOTED ✓
- p_elementa_walkeweg ← already PROMOTED ✓

So all of these are handled. The remaining KEEP STUBs (per PARKED_DECISIONS for stub Akteure) are:
- `glasfischer_glastec`, `heinrich_boell_stiftung`, `koimo_development`, `mehr_als_wohnen`, `stiftung_habitat`, `citydev_brussels`, `denkstatt`, `edith_maryon_stift`, `eitel_partner`, `gibbins_architekten`, `kunst_stoffe_ev`, `zusammenkunft_berlin`

These remain orphans (degree 0-1). Batch3 should research and link them to relevant projects.

### C2 — Dossier follow-up batches (rounds 3+)
The current dossiers are mostly DACH + EU + UK. Underrepresented regions:
- France (only REFAIR Bordeaux dossier)
- Iberia (none — REBRIDGE has Coimbra partner but no Iberian project dossier)
- Eastern Europe (none — Ukraine added as Land but no project dossier)
- US / Canada
- Asia (Kamikatsu existing but only as Stadt — no dossier)

### C3 — Vocabulary expansion
Several gaps surfaced:
- **Material nodes**: live graph has 19; many BGs need finer-grained materials than the Materialgruppe coarse categories. Specifically `mat_messing` (brass — Wabbes handles), `mat_recyclingglas` (Magna), `mat_holz_larche` (Circl larch), `mat_holz_clt` (Stuttgart 210), `mat_textil` (Circl jeans/clothing).
- **`bt_belag` is absent** (S10) — either create as new Bauteiltyp or accept `bt_boden` as canonical for floor finishes.
- **`norm_sia_*`**: SIA 261, 269, 500 created in batch2. SIA 380/1 (energy), SIA 269/3 (timber existing structures), etc. may be needed.
- **`Region` label**: doesn't exist. Brussels-Capital Region, Nouvelle-Aquitaine, etc. forced into Akteur or Stadt today. Consider introducing.

### C4 — Wiederverwendungsketten expansion
batch2 added 9 ketten. Many more chains are documented in batch1 archive but unmodeled:
- K.118 → various receivers (existing in graph but ketten not all wired)
- Resource Rows brick modules
- Mauerwerk reuse chains in Belgium
- Stahl-Offcuts reuse chains

### C5 — Per-BG NUTZT_MATERIAL backfill (corpus-wide)
Per rollback.md R-3, 134 existing BGs already have NUTZT_MATERIAL. The other ~170 don't. A bulk backfill script (similar to phase R) would add NUTZT_MATERIAL where the Materialgruppe → Material mapping is unambiguous.

### C6 — `external_reference` Quelle backfill (corpus-wide)
NAMING_AND_PROPERTIES_PLAN §Q deferred this. After B2 adds the high-value batch2 ones, a corpus-wide pass would add the rest.

---

## §D — Schema / tooling improvements

### D1 — Patch tool: support unicode in rel types
The apply tool's regex `^[A-Za-z_][A-Za-z0-9_]*$` rejects `GEHÖRT_ZU`. Two options:
- **Tighter**: keep the regex; rename live `GEHÖRT_ZU` → `GEHOERT_ZU` (one-time rel-type rename, 216 rels affected). Then all future GEHÖRT_ZU writes go through the apply tool.
- **Looser**: relax regex to `^[A-Za-z_À-ſ][A-Za-z0-9_À-ſ]*$` (allow Latin Extended). Less disruption, but `r.id` strings with umlauts may cause issues downstream.

Recommend **option D1a (rename)**: cleaner long-term. Write a `phase_r2.py` script that does `MATCH ()-[r:GEHÖRT_ZU]->() CALL apoc.refactor.setType(r, 'GEHOERT_ZU') YIELD ...`. Then update all consuming queries.

### D2 — Apply tool: support `remove_label` op
Currently the apply tool can union labels (via merge_node) but can't strip one. Add a `remove_label` op:
```jsonl
{"op": "remove_label", "id": "prog_fcrbe", "label": "Projekt", "reason": "...", "severity": "LOW"}
```
This would handle Option B5 cleanly via the standard patch workflow.

### D3 — Apply tool: support dependent-op planning
Current planner evaluates all ops against the initial state, so an add_node + merge_node pair must be split into two patches. A flag `--sequential-planning` would re-plan each op against the post-prior-op state, enabling single-file patches with dependencies.

### D4 — Validation tool: add per-patch precondition Cypher
The apply tool already supports `--confirm "APPLY <file> TO <db>"`. Add `--precondition <file.cypher>` that runs read-only Cypher and asserts results match expectations before apply.

### D5 — `r.id` integrity guard
Phase R hygiene revealed 2523 stale r.id strings post-merge. Apply tool could optionally re-write r.id on every operation that changes endpoints, eliminating the need for periodic Phase R cleanup.

---

## §E — Open questions waiting on user decision

| # | Question | Recommendation |
|---|---|---|
| E1 | Zirkular dedup: `zirkular` (deg 24) vs `zirkular_gmbh` (deg 10) coexist post-batch2 1b. Merge? | Yes — merge `zirkular_gmbh → zirkular` (higher degree wins per same logic as Z10 Rotor decision). Defer to batch3 unless urgent. |
| E2 | Keep `:Programm:Projekt` dual-label or strip? | Pragmatic: keep. Strip only if a query author explicitly asks. |
| E3 | RE_USE Höfe "Wien" — kept as alias, but the dossier is explicit it's not actually Vienna. Should we also remove the `prog_re_use_hoefe → stadt_wien` LIEGT_IN_STADT if any? | Verify no such edge exists (none created in batch2). If found later, remove. |
| E4 | OBK_27 dossier — should we research the actual Barrault Pressacco project (Oberkampf social housing, Paris)? It's the only candidate per the dossier. | Yes, in batch3. Currently the cyril_pressacco + thibaut_barrault Akteure are orphaned from any project. |
| E5 | Werner Sobek merge direction — done (werner_sobek_p → Werner_Sobek per user). Should we also unify with potential other Sobek-related ids in the corpus? | Check S29-style query for all "Sobek" matches after batch2 applied; merge if duplicates found. |
| E6 | Region label: introduce as new schema label, or keep regions as Akteur (current) / Stadt (current Brussels-Capital Region mapping)? | Schema decision; defer to batch3 planning. |
| E7 | Should "research/teaching programmes that are dossier-unverified" (Architecture of Reuse BXL, Vandkunsten, ZHAW) be researched further to verify? | Yes, in batch3. They're the only stubs without verified Programm anchor. |

---

## §F — Suggested deliverables for batch3

If you proceed with batch3, the suggested artifacts (mirroring batch2 v2's structure):

1. **`pre_flight_validation_batch3.cypher`** — same shape as batch2, with section S* updated for new ids batch3 will touch.
2. **`CORRECTIONS_2026-MM-DD.md`** — issue + remediation catalog.
3. **`actor_extraction_per_dossier_batch3.md`** — extracted per-dossier actor inventory.
4. **`PLAN_v3.md`** — 10-phase plan covering: stub cleanups (B1-B6 from this doc) + new dossiers (C1-C2) + vocab expansion (C3).
5. **`APPLY_ORDER_v3.md`** — apply sequence.
6. **`patches/batch3/`** — JSONL patches.

Lessons from batch2 v2 to encode in PLAN_v3:
- Always run pre-flight validation before patch generation.
- Split add_node + merge_node into separate patches (planner limitation).
- Strip BELEGT_IN rels before delete_node (apply tool safety guard).
- Use `merge_node` (with label union) for relabel operations; document the dual-label outcome.
- Use direct Cypher for rel types containing non-ASCII characters (apply tool regex limitation, until D1 fixes it).
- Generator scripts (Python emitting JSONL) for repetitive patches (Phases 6b, 8) save substantial time.

---

**End of NEXT_STEPS.md.**

Cross-references: [APPLY_ORDER.md](APPLY_ORDER.md), [PLAN_v2.md](PLAN_v2.md), [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md), [actor_extraction_per_dossier.md](actor_extraction_per_dossier.md).
