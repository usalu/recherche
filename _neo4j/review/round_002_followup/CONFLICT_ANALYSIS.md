# Conflict analysis — NAMING_AND_PROPERTIES_PLAN.md

Detailed pre-flight check before adopting the naming + property plan. Every finding is grounded in a live-graph query or apply-tool code review.

**Verdict:** the plan is sound in principle but needs **four amendments** before execution. Detailed list in section F.

---

## A. No conflicts — safe to proceed

### A1. All six new properties are unused
Queried every node for `name_full`, `primary_material_id`, `primary_bauteiltyp_id`, `reuse_status`, `bg_slug`, `country_iso2`. **Zero existing usage.** Adding them is a clean introduction.

### A2. No existing ids use `__` separator
Queried `MATCH (n) WHERE n.id CONTAINS '__'`. Zero hits. The proposed `bg_<projslug>__<status>_…` schema is collision-free at the id-syntax level. (The `__` separator is currently only used in relationship ids `r_<from>__<TYPE>__<to>`, which the apply tool's `rewrite_id_outbound` function recognises.)

### A3. Norm short names are unique
Took the first 2 tokens of every Norm `name` (e.g. "EN 206", "DIN 4074", "CEN/TS 1090-201:2024") — **all 30 short names unique.** The proposed Norm shortening is safe.

### A4. Akteur aliases format is consistent
Existing `aliases` on Akteur are arrays of strings:
```
imd_raadgevende_ingenieurs    IMd Raadgevende Ingenieurs    aliases=['IMd raadgevende ingenieurs']
cleveland_steel_tubes          Cleveland Steel & Tubes        aliases=['Cleveland Steel and Tubes']
rotor_dc                       Rotor DC                       aliases=['Rotor Deconstruction / RotorDC']
```
Adding old BG ids as aliases on renamed BGs is structurally consistent.

### A5. BG ids are not referenced in archive `.md` files
Searched 76 archive case-study files for `bg_*` substrings. **Zero hits.** Renaming BGs does not invalidate any archive documentation.

### A6. No `bg_*` substrings in relationship `source_excerpt` properties
Queried every rel with `source_excerpt` for `bg_*` patterns. **Zero hits.** The Phase G archive-scan source excerpts are textual quotations, not graph references.

### A7. No stub Bauteilgruppen
All 306 BGs belong to full Projekte (none of the 23 stub Projekte own a BG). The rename touches no stub state.

---

## B. Confirmed conflicts — plan needs amendment

### B1. ⚠️ CRITICAL — `canonicalize_node` does NOT rename ids

Code review of `_scripts/apply_neo4j_review_patch.py:767–775`:

```python
if op == "canonicalize_node":
    after = planned["after"]["properties"]
    session.run(
        "MATCH (n {id: $id}) SET n.name = $name, n.aliases = $aliases",
        id=record["id"], name=after.get("name"), aliases=after.get("aliases", []),
    ).consume()
    return
```

It only sets `name` and `aliases` — **the node id stays.** My earlier plan to use `canonicalize_node` for the 306-row BG rename is wrong.

**Correct workflow:** use `merge_node` (`apply_neo4j_review_patch.py:777–868`), which has working rel-id rewriting (`rewrite_id_outbound` at lines 788–793). For each BG:
1. `add_node` with the **new** id + all new properties (name short, name_full, reuse_status, primary_material_id, primary_bauteiltyp_id)
2. `merge_node` from **old** id to **new** id — redirects all rels, rewrites `r.id` properties on outgoing rels, copies remaining old properties (raw_name, alte_funktion, neue_funktion, counts_as_direct_reuse), then deletes the old node.

**Op-count impact:** Phase O goes from 306 ops to **612 ops** (2 per BG).

### B2. Multi-axis collisions on BG id — discriminator is mandatory in 15+ cases

Queried for BGs sharing the same `(project, material, bauteiltyp)` tuple. Found **15 collision groups**, examples:

| Project | Material | Bauteiltyp | Colliding BGs |
|---|---|---|---|
| `p_association_house_groeditz` | mat_stahlbeton | bt_decke | `bg_groeditz_dresden_type_precast_components`, `bg_groeditz_wbs70_precast_panels` |
| `p_big_dig_house_lexington_massachusetts` | mat_stahl | bt_traeger | `bg_big_dig_house_stahltraeger_stahlstuetzen`, `bg_big_dig_house_ramp_pier_roadway_components` |
| `p_christ_pavilion_volkenroda` | mat_beton | bt_wand | `bg_christ_pavilion_complete_ensemble`, `bg_christ_pavilion_fair_faced_concrete_parts` |
| `p_chiro_d_itterbeek_dilbeek` | mat_daemmstoff | bt_daemmung | `bg_chiro_surplus_floor_wall_insulation`, `bg_chiro_surplus_ceiling_insulation` |

**Plan amendment:** the discriminator slot becomes **required** when (project, material, bauteiltyp) already collides for another BG in the same project. Algorithm needs a uniqueness check during rename-table generation.

### B3. Multi-material BGs — `primary_material_id` policy needed

Material count per BG:

| # materials | # BGs | % |
|---:|---:|---:|
| 0 | 5 | 1.6 % |
| 1 | 188 | 61.4 % |
| 2 | 82 | 26.8 % |
| 3 | 27 | 8.8 % |
| 4 | 3 | 1.0 % |
| 5 | 1 | 0.3 % |

**113 BGs (37 %) have ≥ 2 materials.** Three policy options for `primary_material_id`:

- **Option A** — `mehrere` for all 113. Honest, loses information, makes 37 % of BGs less discoverable.
- **Option B** — pick the alphabetically-first id. Deterministic, but arbitrary; might pick `mat_aluminium` over `mat_stahl` even when steel is the structural primary.
- **Option C** — pick based on a manual review for each multi-material BG. Highest quality but laborious.

**Recommendation:** **Option A + manual override** — start with `mehrere`, allow per-BG override in the rename table for the 30 BGs where a clear primary exists (the 3+ material cases). Easier to dry-run.

### B4. Multi-bauteiltyp BGs — same problem, more common

Bauteiltyp count per BG:

| # bauteiltypen | # BGs | % |
|---:|---:|---:|
| 1 | 117 | 38.2 % |
| 2 | 143 | 46.7 % |
| 3 | 43 | 14.1 % |
| 4 | 3 | 1.0 % |

**189 BGs (62 %) have ≥ 2 Bauteiltypen.** Same policy needed for `primary_bauteiltyp_id`. **Recommendation:** Option A + manual override.

### B5. BGs with 0 materials (5 outliers)

```
bg_charles_malis_rotor_luminaires                            "ROTOR-Leuchten"
bg_chiro_luminaires                                          "Leuchten"
bg_circular_pavilion_reused_lights                           "Vier grosse Leuchten aus oeffentlichem Bestand"
bg_peoples_pavilion_borrowed_facade_elements                 "Geliehene Fassadenelemente"
bg_trae_high_rise_aarhus_windturbinenfluegel_als_sonnenschutz "Windturbinenflügel als Sonnenschutz"
```

These are reused fixtures/elements where the material is unknown or non-standard (wind-turbine blades, luminaires). **Plan amendment:** introduce `mat_unbekannt` for these 5, or omit the material slot in the new id (`bg_charles_malis__reuse_<bauteiltyp>_rotor_luminaires`).

### B6. Projekt short-name collision

Heuristic shortening (`first token + city`) detects one collision:
```
'Association house' → ['p_association_house_groeditz', 'p_association_house_plauen']
```

Both are German "Vereinshaus" precast-panel reuse projects but with different cities. **Plan amendment:** the short-name rule must include city as the disambiguator when the project name leads with a generic noun:
- `p_association_house_groeditz` → `Vereinshaus Gröditz` (not "Association house")
- `p_association_house_plauen` → `Vereinshaus Plauen`

The `Big Dig Building Boston` / `Big Dig House Lexington` pair is *not* a collision because the city is already part of the project's distinguishing token (`Building Boston` vs `House Lexington`).

### B7. Quelle property landscape — actually three-state, not two

| State | Count | Action |
|---:|---:|---|
| both `name` + `titel` (values equal) | 1 | drop `titel`, keep `name` |
| `name` only | 127 | leave `name`; check if ≤ 25 chars; if not, set `name_full = name`, derive new short name |
| `titel` only | 319 | `titel → name_full`, derive new short `name` |
| neither | 0 | — |

The 127 "name only" Quelle nodes still need a length check — if their `name` is currently long (likely yes for archive-scan-derived nodes), they need the same short-name derivation as the 319. Plan needs to address this.

### B8. Norm `usage_project_count` etc. — small data loss but derivable

The 16 Norm nodes carrying `usage_project_count`, `usage_countries`, `usage_project_ids` hold real values:
```
norm_sia_schweiz       count=2 countries=['Schweiz']
norm_crow_cur_4_2023   count=2 countries=['Niederlande','Finnland']
norm_sci_p427          count=2 countries=['Vereinigtes Königreich']
```
But these are **derivable** via Cypher:
```cypher
MATCH (n:Norm {id: 'norm_sia_schweiz'})<-[:REFERENZIERT_NORM]-(bg:Bauteilgruppe)
       <-[:HAT_BAUTEILGRUPPE]-(p:Projekt)
RETURN count(DISTINCT p), collect(DISTINCT p.id);
```
Safe to drop. The cached values just stop being maintained; queries always return fresh counts.

### B9. Akteur `stars_ignored` — 85 nodes hold value `'True'` (string)

All 85 carry the same value. No information lost on drop.

### B10. Existing aliases on Projekt + Land must not be overwritten

- **Projekt** has aliases on 2 nodes: `p_lysp8_basel` (`['LYSP8']`) and `p_eth_circular_construction_student_reuse` (`['ETH Circular Construction student reuse project']`).
- **Land** has aliases on 1 node: `land_daenemark` (`['Daenemark']`).

**Plan amendment:** any patch op that touches `aliases` must use *append* semantics, not overwrite. The apply tool's `set_node_properties` overwrites — so for these 3 nodes, the patch must explicitly include the existing aliases plus any new ones in the new aliases array.

---

## C. Cross-reference risks

### C1. 873 references to `bg_*` in historical patch JSONLs

Historical patches under `_neo4j/review/round_002_followup/patches/*.jsonl` reference BG ids 873 times. **These patches are already applied** — they're audit documentation now. No re-application planned.

**Mitigation:** preserve every old BG id in the renamed node's `aliases` array. This way `MATCH (bg:Bauteilgruppe {aliases: ['bg_villa_welpeloo_enschede_stahltraeger_aus_paternoster_textilmaschine']}) RETURN bg` still resolves to the renamed node, and the audit trail in the patch files stays human-readable.

### C2. 7 882 rels FROM Bauteilgruppe with `r.id` starting `r_bg_`

Every outgoing rel from a BG has a relationship id of form `r_<bg_id>__<TYPE>__<to_id>`. Renaming a BG would invalidate all 7 882 of these ids — except `merge_node` rewrites them automatically via `rewrite_id_outbound`:

```python
def rewrite_id_outbound(rel_id, rel_type):
    needle = f"r_{from_id}__{rel_type}__"
    if not rel_id.startswith(needle): return None
    return f"r_{to_id}__{rel_type}__" + rel_id[len(needle):]
```

**Verified safe** — the merge tool handles this. No additional plan action needed.

### C3. 2 references to `bg_*` in .cypher files

The 2 references are in `VERIFICATION_QUERIES.cypher` and `EXPLORATION_QUERIES.cypher`. Both files filter by Material / Project / Country ids — never by hard-coded BG ids. **Safe.** Spot-checked.

### C4. Round 003 propagation rels carry `r.source = 'round_003_material_propagation'`

Those rels (33 HAT_DEFEKT at BG level + 321 HAT_MARKTMODELL at BG level) have rel ids `r_<bg_id>__HAT_*__<vocab_id>`. Same as C2 — `merge_node` rewrites them correctly.

### C5. Archive markdown files

Searched all 76 archive .md files for `bg_*` substrings: **zero hits.** No archive-side documentation needs updating after the rename.

---

## D. Phase ordering — recommended sequence

Original plan: L → M → N → O → P. Findings tweak this:

| Phase | What | Why this order |
|---|---|---|
| **L1–L5** | property hygiene (drop stray intake props, normalize Quelle, add country_iso2) | get to a clean property baseline first so subsequent dry-runs aren't noisy |
| **M** | short `name` + `name_full` on long-named vocab labels | low-risk, isolated property writes |
| **N** | short `name` + `name_full` on Projekt / Bauwerk / Wiederverwendungskette | same low-risk pattern |
| **O.a** | `add_node` for all 306 new BGs with new ids + new properties | Phase O is split — creates new shells first |
| **O.b** | `merge_node` for all 306 old→new pairs | redirects rels with `rewrite_id_outbound`, deletes old nodes |
| **P** | backfill optional properties (counts_as_direct_reuse, alte/neue_funktion) | runs against the new, clean state |

**Why split Phase O:** in case anything goes wrong between O.a and O.b, the old BGs are still intact. The new BGs are isolated until merged. Both phases get their own backup.

**Suggested smaller intermediate step:** after Phase L, take a graph diff to confirm the property hygiene didn't drop anything load-bearing. The verification queries should all still pass.

---

## E. Data-integrity verification

### E1. `merge_node` preserves old BG properties

Code review confirms `merge_node` step 4 (line 859–865):
```python
# 4. Set merged properties on target (canonical wins; id stays).
after_props = dict(planned["after"]["properties"])
after_props["id"] = to_id
session.run("MATCH (t {id: $to_id}) SET t += $props", ...)
```

`after_props` is the planner-computed union of source + target. So the old BG's `raw_name`, `alte_funktion`, `neue_funktion`, `counts_as_direct_reuse`, etc. survive the merge.

### E2. Rel id format consistency

Before merge: `r_<old_bg_id>__NUTZT_MATERIAL__mat_stahl`
After merge: `r_<new_bg_id>__NUTZT_MATERIAL__mat_stahl`

Format stays the same. The relationship pattern matching in all existing Cypher continues to work.

### E3. Uniqueness constraints

If the graph has a uniqueness constraint on `Bauteilgruppe.id` (it probably does — see `_neo4j/contracts/project_batches_v1_1/cypher/constraints.cypher`):
- During Phase O.a, new ids must not already exist (the rename table must be collision-free)
- During Phase O.b, when `merge_node` deletes the old node, the old id becomes free — no constraint violation

If there's also a uniqueness constraint on relationship ids (Neo4j 5+):
- `rewrite_id_outbound` produces ids of form `r_<new_bg_id>__TYPE__<to_id>` which are guaranteed unique (different `from` part)
- But `rewrite_id_inbound` for inbound rels keeps the rel id as `r_<x>__TYPE__<new_bg_id>` — also unique

---

## F. Required plan amendments

Adopt these before executing:

1. **Phase O split** — `add_node` (Phase O.a, 306 ops) then `merge_node` (Phase O.b, 306 ops). Two separate patches with backup between. Total Phase O ops = 612, not 306.

2. **Discriminator becomes required** when (project, material, bauteiltyp) already collides within a project. Rename-table generator must include a uniqueness check; if `bg_<proj>__<status>_<mat>_<bt>` would collide with an already-emitted id, append the existing BG's "what makes it special" tail (donor source, position, sub-component).

3. **Primary-material / Primary-bauteiltyp policy** for the 113 + 189 multi-axis BGs:
   - 0 materials → `mat_unbekannt` (introduce as new Material node) OR omit the slot in the new id
   - 1 material → that material
   - 2+ materials → `mehrere` by default; allow per-BG manual override in the rename table
   - Same for bauteiltyp

4. **Preserve old BG ids as aliases** on each renamed BG. The `add_node` op for the new BG must include `aliases: ['<old_bg_id>']` so the historical 873 references in patch JSONLs can still be resolved via `MATCH (bg:Bauteilgruppe) WHERE '<old_id>' IN bg.aliases`.

5. **Quelle handling — three groups, not two:**
   - 1 node with both `name`+`titel` (same value) → drop `titel`, no other change
   - 319 with `titel` only → `rename_property` `titel → name_full`, derive new short `name`
   - 127 with `name` only → length check; if `name > 25 chars`, set `name_full = name`, derive new short `name`; if already ≤ 25 chars, no change

6. **Aliases append, never overwrite** — any `set_node_properties` patch op that touches `aliases` on `p_lysp8_basel`, `p_eth_circular_construction_student_reuse`, `land_daenemark`, the 4 Akteure with existing aliases, or any other already-aliased node must pre-fetch the existing array and emit `aliases = [<existing>, <new>]`.

7. **Projekt short-name disambiguation rule:** when the project name leads with a generic noun (`Association house`, `Pilot house`, `Maison`, etc.) AND another project shares that same prefix, the city / country / year token is mandatory in the short name. Currently only `p_association_house_groeditz` vs `p_association_house_plauen` matches this — but apply the rule defensively for all projects whose first 2 tokens collide.

---

## G. Risk summary

| Risk | Severity | Mitigation |
|---|---|---|
| `canonicalize_node` won't rename ids | **HIGH** — silently no-op | Use `merge_node`; split Phase O into O.a + O.b |
| 15+ BG id collisions on (project, mat, bt) tuple | **MEDIUM** — patch would fail uniqueness | Discriminator-required check in rename-table generator |
| Multi-material/-bauteiltyp BGs lose information via `mehrere` | LOW | Manual override option for the 30 most-multi cases |
| Historical 873 BG-id references in patch files become stale | LOW | Preserve old ids in `aliases`; audit traceable |
| 5 BGs with 0 materials don't fit the new id schema | LOW | Use `mat_unbekannt` or omit slot |
| Projekt short-name collisions (currently 1 confirmed) | LOW | City-required rule for generic-noun leads |
| Quelle property cleanup more complex than 2-state | LOW | 3-state handling in plan (B7) |
| Existing `aliases` on 7 nodes get overwritten | MEDIUM — data loss | `aliases` always uses append semantics |
| Uniqueness constraints during Phase O.a window | LOW | New ids are by construction collision-free vs existing |
| `usage_project_count` etc. drop on Norm loses cached counts | LOW | Derivable via Cypher; document the query |

---

## Next step

Compute the 306-row BG rename table with these amendments baked in. The table is a CSV / markdown sheet with columns:

| old_id | new_id | proposed short `name` | `name_full` | `reuse_status` | `primary_material_id` | `primary_bauteiltyp_id` | discriminator | aliases (= [old_id]) | manual override? |
|---|---|---|---|---|---|---|---|---|---|

For each of the ~30 multi-axis BGs and the 5 zero-material outliers, the "manual override?" column flags the row for your manual review before patch generation.
