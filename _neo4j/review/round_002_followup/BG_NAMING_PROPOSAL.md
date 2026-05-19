# Bauteilgruppe naming convention — proposal

After analyzing all 306 `Bauteilgruppe` nodes (their `id`, `name`, `raw_name`, `alte_funktion`, `neue_funktion`, materials, Bauteiltypen, and project links), the current naming is **freeform and inconsistent**. This document proposes a tighter, machine-parseable convention plus a migration path.

## What the data shows now

| Property | Coverage |
|---|---:|
| `name` (human-readable) | 306/306 (100 %) |
| `raw_name` (verbatim source label) | 219/306 (72 %) |
| `alte_funktion` | 287/306 (94 %) |
| `neue_funktion` | 287/306 (94 %) |
| `counts_as_direct_reuse` | 266/306 (87 %) |
| Project link via HAT_BAUTEILGRUPPE | 306/306 |
| Material link via NUTZT_MATERIAL | 301/306 (98 %) |
| Bauteiltyp link via HAT_BAUTEILTYP | 306/306 |

### Issues found

1. **Inconsistent project prefix.** Of 306 ids, only 105 use ≥ 2 tokens of the project slug. 160 use just 1 token, 33 use an ad-hoc abbreviation (`alliander`, `botanique`, `green`, `groeditz`, `ithaka`, `awm`, `bedzed`, `ccn`, `hof`, `musef` …), 21 don't match at all.
2. **Mixed languages.** 146 ids use English component descriptors (`reused_steel_external_core`), 48 use German (`stahltraeger_stuetzen_rahmen`), 111 use proper nouns / project names only, 1 is mixed.
3. **Reuse-status tokens are scattered.** Currently in use: `reused` (41), `retained` (16), `reclaimed` (7), `geplante` (2), plus singletons `wiederverwendeter`, `wiederverwendete`, `restored`, `demontables`, `preused`. Most ids (≈ 70 %) have no explicit status token.
4. **Material/Bauteiltyp encoding is redundantly inconsistent.** 66 / 306 ids include the material name; 240 don't. Same for Bauteiltyp.
5. **Token repeats within one id.** 7 ids repeat a project token (`bg_verbiest_karreveld_brussels_verbiest_dach_und_terrassenfliesen` — "verbiest" twice).
6. **Length varies from 16 to 82 chars** (avg 37). Several ids are unwieldy because they jam project + donor + material + descriptor into one string.

## Proposed convention

```
bg_<project-slug>__<reuse-status>_<material>_<bauteiltyp>_<discriminator?>
```

Anatomy:

| Slot | Purpose | Vocabulary |
|---|---|---|
| `bg_` | entity prefix (already universal) | fixed |
| `<project-slug>` | short canonical slug of the owning Projekt — **≤ 3 tokens**, stored on `Projekt.bg_slug` for stability | per project |
| `__` | **double underscore** — project / BG boundary, allows trivial split-parsing | fixed |
| `<reuse-status>` | how this BG counts toward direct reuse | **4 controlled values:** `reuse`, `retained`, `planned`, `dismantled` |
| `<material>` | primary material short form (matches `mat_*` suffix) | `stahl`, `holz`, `beton`, `stahlbeton`, `glas`, `keramik`, `ziegel`, `naturstein`, `daemmstoff`, `aluminium`, `kunststoff`, `mdf`, `recyclingbeton`, `mehrere` |
| `<bauteiltyp>` | primary Bauteiltyp short form (matches `bt_*` suffix) | `fassade`, `wand`, `traeger`, `decke`, `ausbau`, `boden`, `stuetze`, `technik`, `fenster`, `dach`, `tuer`, `daemmung`, `gelaender`, `treppe`, `fundament`, `mehrere` |
| `<discriminator>` | optional — disambiguates multiple BGs that would otherwise share the same id within one project. Usually donor source or location. Free-form, ≤ 4 tokens. | free |

### Concrete examples — before vs. after

| Current id | Project | Material | Bauteiltyp | Proposed id |
|---|---|---|---|---|
| `bg_k118_kopfbau_halle_118_winterthur_stahltraeger_aus_elys_basel`* | K.118 Winterthur | Stahl | Träger | `bg_k118__reuse_stahl_traeger_aus_elys_basel` |
| `bg_55gss_reused_steel_external_core` | 55 Great Suffolk St | Stahl | Stütze/Träger | `bg_55_great_suffolk__reuse_stahl_traeger_external_core` |
| `bg_alliander_common_roof_atrium` | Liander Alliander | Glas+Holz+Stahl | Dach/Fassade | `bg_alliander__retained_mehrere_dach_atrium` |
| `bg_alliander_material_passport_inventory` | Liander Alliander | (digital) | (none) | `bg_alliander__planned_mehrere_technik_material_passport` |
| `bg_bedzed_reused_structural_steel` | BedZED | Stahl | Träger | `bg_bedzed__reuse_stahl_traeger` |
| `bg_bedzed_reused_timber_wall_studs` | BedZED | Holz | Wand | `bg_bedzed__reuse_holz_wand_studs` |
| `bg_resource_rows_ziegelfassadenmodule_mauerwerksausschnitte`* | Resource Rows | Ziegel | Fassade | `bg_resource_rows__reuse_ziegel_fassade_module` |
| `bg_villa_welpeloo_enschede_stahltraeger_aus_paternoster_textilmaschine` (70 chars) | Villa Welpeloo | Stahl | Träger | `bg_villa_welpeloo__reuse_stahl_traeger_paternoster_textilmaschine` (61 chars) |
| `bg_zinneke_feder_masui4ever_brussels_eichenparkett_und_azobe_terrassendielen` (76 chars) | Zinneke Brussels | Holz | Boden | `bg_zinneke__reuse_holz_boden_eichenparkett_azobe` (47 chars) |
| `bg_grande_halle_doors_fire_doors` (token repeat) | Grande Halle Colombelles | Holz | Tür | `bg_grande_halle__reuse_holz_tuer_fire_rated` |
| `bg_verbiest_karreveld_brussels_karreveld_modulares_innenwandsystem` (token repeat) | Verbiest Karreveld | Mehrere | Wand | `bg_verbiest__reuse_mehrere_wand_modulares_innenwandsystem` |
| `bg_bestandsfundamente_und_erste_geschosse_blackfriars` (no clear project prefix) | Roots in the Sky / Blackfriars | Beton | Fundament | `bg_blackfriars__retained_beton_fundament_erste_geschosse` |
| `bg_geplante_stahltrager_stahlprofile_roots` (mixes "geplante" + project at end) | Roots in the Sky | Stahl | Träger | `bg_roots__planned_stahl_traeger_stahlprofile` |

*Hypothetical — those exact ids don't exist as one string today, but the example shows the equivalent transformation.

### Why this convention works

- **Machine parseable.** `split('__', 1)` gives `(project_slug, component_id)`. `component_id.split('_', 3)` gives `(status, material, bauteiltyp, discriminator)`.
- **Self-documenting at a glance.** Even without reading any property, the id says: which project, what reuse status, what material, what component type.
- **Shorter on average.** Estimated new avg ≈ 32 chars (currently 37). The genuinely long ids — those carrying donor specifics — stay readable because the structured part is compact.
- **Consistent language.** Reuse-status in English (matches the rest of the schema's enum vocabulary). Material + Bauteiltyp short forms in German (match the controlled-vocab seed). Discriminator stays in the source language.
- **Encodes information already required.** Material + Bauteiltyp already exist as relationships on every BG. Putting the short form in the id makes the id mirror the strongest two facts about the BG.

## Companion property changes

Add three new properties to every BG to make the convention robust:

| Property | Type | Source | Note |
|---|---|---|---|
| `reuse_status` | enum string | one of `reuse / retained / planned / dismantled` | Already implicit in `name` / `alte_funktion`; just promote to a typed field. |
| `primary_material_id` | string | first / dominant material from existing `NUTZT_MATERIAL` rels | Lets you filter without a traversal. |
| `primary_bauteiltyp_id` | string | first / dominant Bauteiltyp from existing `HAT_BAUTEILTYP` rels | Same. |

Existing properties stay as-is:
- `name` — keep human-readable (German or English ok)
- `raw_name` — keep verbatim source label
- `alte_funktion`, `neue_funktion` — keep (and backfill the 19 missing ones)
- `counts_as_direct_reuse` — keep (and backfill the 40 missing ones)

The `id` becomes the **structured handle**; `name` stays the freeform descriptor.

## Stable project-slug table (the ≤ 3-token "bg_slug")

I'd add a `Projekt.bg_slug` property holding the short canonical slug for each project. Examples:

| Project (current id) | Proposed bg_slug |
|---|---|
| `p_k118_kopfbau_halle_118_winterthur` | `k118` |
| `p_55_great_suffolk_street_london` | `55_great_suffolk` |
| `p_resource_rows_copenhagen` | `resource_rows` |
| `p_liander_alliander_hq_duiven` | `alliander` |
| `p_villa_welpeloo_enschede` | `villa_welpeloo` |
| `p_zinneke_feder_masui4ever_brussels` | `zinneke` |
| `p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain` | `house_of_fraser` |
| `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot` | `ccn_prinsenhof` |
| `p_roots_in_the_sky_blackfriars_crown_court` | `roots_blackfriars` |
| `p_kindergarten_moeoeslistrasse_manegg_zuerich` | `manegg_kiga` |
| `p_eth_circular_construction_student_reuse` | `eth_cea` |

A naming-control list once written becomes the source of truth — every new BG references it.

## Migration mechanics

The renaming is an id-change which means every relationship referencing the BG also needs updating. The apply tool's `canonicalize_node` op handles this:

```jsonl
{"op": "canonicalize_node", "id": "bg_villa_welpeloo_enschede_stahltraeger_aus_paternoster_textilmaschine",
 "canonical_name": "bg_villa_welpeloo__reuse_stahl_traeger_paternoster_textilmaschine",
 "aliases": ["bg_villa_welpeloo_enschede_stahltraeger_aus_paternoster_textilmaschine"],
 "reason": "BG renaming convention v2", "severity": "LOW"}
```

For all 306 BGs this is one patch with 306 records. Recommended sequence:

1. **Generate `Projekt.bg_slug` for all 76 (or all 99 incl. stubs) projects.** Manual review of the slug list first (≤ 3 tokens, no collisions).
2. **Compute proposed BG id** for each of the 306 BGs using the algorithm above:
   - status from existing reuse-status token in the current id (defaults `reuse` if missing)
   - material from `primary_material_id` (or `mehrere` if > 1 with no clear primary)
   - bauteiltyp from `primary_bauteiltyp_id` (or `mehrere`)
   - discriminator from the residue of the current id after stripping project tokens + status + material + bauteiltyp tokens
3. **Review the 306-row rename table manually** — there will be ~10-20 ambiguous cases (which is "primary" material when a BG has 3?).
4. **Generate the canonicalize_node patch** and apply with the standard backup + dry-run + live-apply protocol.
5. **Add the three new properties** (`reuse_status`, `primary_material_id`, `primary_bauteiltyp_id`) in the same patch.

Expected impact: 306 node renames + 0 new nodes + new properties on 306 BGs. All existing relationships keep working (canonicalize_node redirects them).

## What I'd skip

- **Don't try to fully translate names to one language.** The `name` property can stay multilingual — German for German projects, English for UK / Dutch / Danish projects, French for French projects. The id is the structured handle; the name is human-readable.
- **Don't pre-encode Akteur slugs in BG ids.** Actors change; the project link is enough.
- **Don't introduce a separate `BauteilgruppeTyp` taxonomy** on top of the existing `Bauteiltyp` + `Material` combination — the two existing vocabularies are sufficient.

## Open questions before executing

1. Is `bg_slug` the right property name on Projekt, or should it be `slug_short` / `canonical_slug` (more general for cross-referencing all child nodes)?
2. For BGs that span multiple buildings / multiple donor sources, should the discriminator combine them (`paternoster_textilmaschine_und_grover_warehouse`) or pick one canonical donor?
3. Should `reuse_status` be derived only from the name, or do we want to introduce a fifth value (`mehrere` / `gemischt`) for BGs that combine retained + reused parts?

If you accept this proposal in principle, I can compute the full 306-row rename table and a draft `bg_slug` value for each project as the next step — that gives you something concrete to mark up before any rename runs.
