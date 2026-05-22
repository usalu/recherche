# Bauteilgruppe Resolver — usage guide

**STATUS (2026-06-03 followup):** Optional / informational. Final plan ([FINAL_PLAN.md decision #8](FINAL_PLAN.md#decisions-locked-in)) skips the manual resolver — batch BG slugs are canonical, slug-drift duplicates are an accepted cost.

This guide is preserved for two reasons:
1. If you change your mind later and want to do the dedupe, this is the tooling.
2. After Phase 5 lands, a future research/cleanup pass can use this to dedupe the ~25-50 slug-drift duplicates.

Original purpose: map every live `:Bauteilgruppe` slug to its matching batch BG slug so the batches can MERGE their evidence rows onto the existing nodes instead of creating duplicates.

## Files

- [build_bauteilgruppe_resolver.py](build_bauteilgruppe_resolver.py) — generates the map (read-only on graph)
- [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv) — the actual map (edit this)
- [bauteilgruppe_resolver_review.md](bauteilgruppe_resolver_review.md) — human-readable review queue, grouped by project

Re-run `python build_bauteilgruppe_resolver.py` any time the batch Markdown changes or after manual edits invalidate something.

## What the matcher does

For each project, it pairs live BGs to batch BGs using:

1. **exact id match** → `auto_confirm`
2. **rich token comparison** with:
   - bilingual aliasing (German ↔ English: `beton ↔ concrete`, `wand ↔ wall`, `fensterrahmen ↔ window`, `aussentreppe ↔ stair`, etc.)
   - material family bonus (`stahl + metall + aluminium + steel` all in the same metal family → +0.10)
   - bauteiltyp family bonus (`gelaender + balustrade + railing` same family → +0.10)
   - cross-`reuse_status` penalty (don't pair `bg_retained_*` with `bg_reuse_*`: −0.20)
3. **enriched signal** from BG properties:
   - live: `id + name + alte_funktion + neue_funktion`
   - batch: `id + detail + evidence_phrase + canonical_target + evidence_summary`
4. **greedy assignment** highest-scoring pair first, both sides exclusive

## Current numbers (regenerate by running the script)

```
Live BGs total          : 350
Batch BGs total         : 330
auto_confirm (exact)    : 273  (78.0%)
needs_review            :  29  (paired with mid-confidence guess)
no_batch_equiv          :  48  (live BG with no plausible batch match)
new_candidate           :  28  (batch BG with no live equivalent)
```

302 BGs paired automatically (86%). You review ~105 entries (29 needs_review + 48 evidence-cold live + 28 new candidates).

## How to review

Open [bauteilgruppe_resolver_review.md](bauteilgruppe_resolver_review.md). Each project block looks like this:

```
### p_bluecity_offices_rotterdam

| kind         | live                                | batch                                       | score | live alte_funktion | live neue_funktion | batch detail |
| weak_guess   | bg_reuse_stahl_gelaender_bluecity…  | bg_reuse_metall_gelaender_bluecity_oil_…    | 0.31  | Offshore-/Balustradenbauteil | unbekannte räumliche Einbauteile | Balustrades from a decommissioned oil platform … |
| weak_guess   | bg_reuse_beton_wand_bluecity_…      | bg_reuse_beton_innenwand_bluecity_original_concrete_blocks | 0.21 | Bestands-/Baumaterial | Trennwände | Concrete blocks from the original water-park structure … |
| weak_guess   | bg_reuse_stahl_ausbau_bluecity      | bg_reuse_stahl_tragwerk_bluecity_reused_steel | 0.14 | unbekannt | unbekannte feste Bauteile im Büroausbau | Reused steel is named as the second material input … |
| no_batch_equiv | bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende | _(none)_ | - | Außenfenster | Trennwände und innere Fassade … |   |
| new_candidate  | _(none)_                          | bg_reuse_glas_innenwand_bluecity_reused_window_frames | - |   |   | Reused window frames are described as the most important … |
```

Decision rules per row:

- **`auto_confirm`** — already in the CSV with the right mapping. Skip unless you want to spot-check.
- **`needs_review`** (score ≥ 0.35) — the algorithm is fairly confident. Read both sides, default to **confirm** unless they clearly describe different components.
- **`weak_guess`** (score 0.10–0.35) — read carefully. The two sides share *some* signal but the score is low.
- **`no_batch_equiv`** (live, no batch match) — the live BG has no batch row covering it. Two sub-cases:
  - genuine gap → leave as-is. The BG keeps its properties + non-vocab edges; just no new evidence on the new axes.
  - missed match → look at the other "no_batch_equiv" / "new_candidate" rows in the same project block. If you spot a pair, edit the CSV (see below).
- **`new_candidate`** (batch, no live match) — the batch introduces a component not in the live graph. Two sub-cases:
  - genuinely new → leave as-is. Phase 4 will MERGE it as a new `:Bauteilgruppe` node anchored to the project (set `bg_kind = partial_batch`).
  - missed match → pair with a live BG, see below.

### How to override a pair

Open [bauteilgruppe_id_map.csv](bauteilgruppe_id_map.csv) in a spreadsheet or text editor. Each row has columns:

```
project_id, live_bg_id, batch_bg_id, score, action, reason, live_alte_funktion, live_neue_funktion, batch_detail
```

Edit `action` to one of:

- **`confirm`** — accept the proposed pair (works for any kind including weak_guess)
- **`reject`** — reject the proposed pair. Use when a `needs_review`/`weak_guess` row is wrong. Set `action = reject`, leave the rest. Both sides become unmatched (live → `no_batch_equiv`, batch → `new_candidate`).
- **`merge_to:bg_X`** — override the algorithm. Use when you spot a better pair in the same project block.
  Example: in BlueCity, edit the row for `bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende` and set `action = merge_to:bg_reuse_glas_innenwand_bluecity_reused_window_frames`. This also auto-rejects the `new_candidate` row for the batch BG.

Re-run the script after manual edits; it preserves your `confirm`/`reject`/`merge_to:` decisions and only re-derives the auto-suggestions.

## Estimated review time

| Effort | Quick (just `auto_confirm` spot-check) | Full review |
|---|---|---|
| Time | 15 min | 1–2 hours |
| Quality | catches obvious mis-pairs | catches all the German↔English drift cases |

## After review, what happens

Phase 4 reads the final CSV and only acts on rows with `action ∈ {auto_confirm, confirm, merge_to:bg_X}`. Rejected pairs become independent (live stays evidence-cold; batch becomes a new node).

The Cypher driver for Phase 4/5 (to be written) loads this CSV as its single source of truth for "which live BG receives which batch row".

## What's safe even if you skip the review entirely

If you run Phase 4–6 with only the 273 `auto_confirm` entries:

- 273 BGs (78%) get new batch evidence — clean
- 77 live BGs stay evidence-cold on the new axes — but they keep all their properties, non-vocab edges, evidence URLs, project anchor. No data lost.
- ~28 batch BGs that look new but actually map to a live BG get duplicated. **This is the only real risk of skipping review.** You'd end up with two `:Bauteilgruppe` nodes representing the same physical component (e.g. BlueCity's red cedar window frames as a live BG AND as a new batch-derived BG).

→ For the cleanest graph, review the 29 needs_review + 28 new_candidate entries (~57 rows). The 48 no_batch_equiv entries can be skipped — they only become candidates for a future research pass.

## Next steps after the CSV is signed off

1. Mark the CSV as final: write `_signed_off = true` in a sidecar file or just commit it.
2. Phase 4 (constraints, new canonical seed nodes) can run.
3. Phase 5 (stage batch Cypher) reads the CSV; Phase 6 (retire old vocab) doesn't depend on it.
