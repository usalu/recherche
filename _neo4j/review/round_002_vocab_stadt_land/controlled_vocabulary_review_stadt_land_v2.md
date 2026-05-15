# Round 002 Controlled Vocabulary Review: Stadt + Land — v2

**Generated:** 2026-05-15
**Supersedes:** [`controlled_vocabulary_review_stadt_land.md`](controlled_vocabulary_review_stadt_land.md) (v1, generated against pre-2026-05-15 corpus; patch file also had mojibake — see [`patches/controlled_vocabulary_stadt_land.patch.jsonl`](patches/controlled_vocabulary_stadt_land.patch.jsonl))
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Why v2

Three reasons:

1. The v1 patch file is **mojibake** (`Vereinigtes K?nigreich`, `D?nemark`,
   `Br?ssel`) because it was written through a non-UTF-8 codepage. It cannot
   be applied as-is even after the apply tool gains `merge_node`.
2. The corpus shifted: batches 016–020 are gone from the live graph, so v1's
   counts are stale.
3. The v1 patch proposed merging `stadt_brussel` → `stadt_bruessel`, but
   `stadt_brussel` no longer exists in the live graph. The merge is a no-op
   against live and should be dropped.

## Result in Context

The live `mit-bestand` graph has 16 `Land` nodes and 62 `Stadt` nodes. Three
genuine `Land` duplicate clusters remain; no `Stadt` duplicate clusters do.

Three nodes referenced by the v1 patch are confirmed safe to merge once the
apply tool supports `merge_node` (plan §6 step C):

- `land_vereinigtes_konigreich` → `land_vereinigtes_koenigreich`
- `land_united_kingdom` → `land_vereinigtes_koenigreich`
- `land_danemark` → `land_daenemark`

One v1 patch op (`stadt_brussel` → `stadt_bruessel`) is **dropped from v2**:
the source node is not present in the current live graph.

## Land hub snapshot (live `mit-bestand`)

| id | name | aliases | inbound | merge_target |
| --- | --- | --- | ---: | --- |
| land_deutschland | Deutschland | — | 120 | — |
| land_schweiz | Schweiz | — | 88 | — |
| land_niederlande | Niederlande | — | 61 | — |
| land_belgien | Belgien | — | 57 | — |
| land_frankreich | Frankreich | — | 35 | — |
| land_vereinigtes_koenigreich | Vereinigtes Königreich | Vereinigtes Koenigreich | 33 | (canonical) |
| land_usa | USA | — | 16 | — |
| land_finnland | Finnland | — | 15 | — |
| land_daenemark | Dänemark | — | 12 | (canonical) |
| land_oesterreich | Österreich | — | 11 | — |
| land_danemark | Dänemark | — | 6 | → land_daenemark |
| land_luxemburg | Luxemburg | — | 6 | — |
| land_japan | Japan | — | 5 | — |
| land_norwegen | Norwegen | — | 5 | — |
| land_vereinigtes_konigreich | Vereinigtes Königreich | — | 5 | → land_vereinigtes_koenigreich |
| land_united_kingdom | United Kingdom | — | 1 | → land_vereinigtes_koenigreich |

## Stadt hub snapshot (top 25 by inbound, live `mit-bestand`)

| id | name | inbound |
| --- | --- | ---: |
| stadt_london | London | 24 |
| stadt_berlin | Berlin | 16 |
| stadt_zuerich | Zürich | 13 |
| stadt_bruessel | Brüssel | 9 |
| stadt_paris | Paris | 9 |
| stadt_hannover | Hannover | 7 |
| stadt_tampere | Tampere | 7 |
| stadt_luxembourg_limpertsberg | Luxembourg-Limpertsberg | 5 |
| stadt_auderghem_brussels | Auderghem / Brüssel | 4 |
| stadt_basel | Basel | 4 |
| stadt_boston | Boston | 4 |
| stadt_hastings | Hastings | 4 |
| stadt_kamikatsu | Kamikatsu, Tokushima Prefecture | 4 |
| stadt_kopenhagen | Kopenhagen | 4 |
| stadt_lo_reninge | Lo-Reninge | 4 |
| stadt_muenchen | München | 4 |
| stadt_oslo | Oslo | 4 |
| stadt_utrecht | Utrecht | 4 |
| stadt_asse | Asse | 3 |
| stadt_bleijerheide_kerkrade | Bleijerheide / Kerkrade | 3 |
| stadt_boulder_colorado | Boulder, Colorado | 3 |
| stadt_colombelles | Colombelles | 3 |
| stadt_dilbeek | Dilbeek / Itterbeek | 3 |
| stadt_duiven | Duiven | 3 |
| stadt_gentbrugge | Gentbrugge / Ghent | 3 |

The full list is 62 entries — the remainder are all distinct cities with
inbound ≥ 1.

## Same-name duplicates (live `mit-bestand`)

| label | name_key | ids | count |
| --- | --- | --- | ---: |
| Land | vereinigtes königreich | `land_vereinigtes_koenigreich`, `land_vereinigtes_konigreich` | 2 |
| Land | dänemark | `land_danemark`, `land_daenemark` | 2 |
| Stadt | — | none | — |

(`land_united_kingdom` is a third concept-duplicate that doesn't share the
exact name string but means the same country; it's included as a merge target
in the deferred patch below.)

## Orphan check

No orphans for `Stadt` or `Land`.

## Diff vs v1

| Change | Detail |
| --- | --- |
| Encoding fixed | All `Vereinigtes Königreich`, `Dänemark`, `Brüssel` rendered correctly in UTF-8 LF. |
| `stadt_brussel` → `stadt_bruessel` merge dropped | Source node not present in live graph. |
| New target: `land_united_kingdom` | Distinct id with name "United Kingdom" (1 inbound) — adds a third merge into `land_vereinigtes_koenigreich`. Was already in v1 as `land_uk`; the id appears renamed in the cleanup. |
| `land_uk` not found | v1 referenced `land_uk` (now `land_united_kingdom`). v2 uses the live id. |
| Canonicalize `land_daenemark` alias | v1 had a mojibake canonicalize op; v2 records the correct `aliases: ["Daenemark"]` after merging `land_danemark` into it. |
| Counts shifted | All `Land` inbound counts grew (more BG/Projekt references after the live cleanup wiring). |

## Candidate patch (active)

`patches/controlled_vocabulary_stadt_land_v2.patch.jsonl` — 1 operation:

| op | id / target | severity | note |
| --- | --- | --- | --- |
| canonicalize_node | land_vereinigtes_koenigreich | LOW | Records canonical name "Vereinigtes Königreich" with aliases `["Vereinigtes Koenigreich","United Kingdom"]` so the merge sources are preserved as aliases on the survivor. |

Note: the `canonicalize_node` for `land_daenemark` (adding "Daenemark" as an
alias) is held until after `land_danemark` merges in — applying the alias on
the canonical first is also safe but creates a fictitious alias if the merge
is later rejected. Defer it to the same step as the merge.

## Candidate patch (deferred — needs apply-tool §6 step C)

`patches/controlled_vocabulary_stadt_land_v2.deferred.jsonl` — 4 operations:

| op | from | to | severity | why deferred |
| --- | --- | --- | --- | --- |
| merge_node | land_vereinigtes_konigreich | land_vereinigtes_koenigreich | MEDIUM | merge_node not yet supported by runner |
| merge_node | land_united_kingdom | land_vereinigtes_koenigreich | MEDIUM | merge_node not yet supported by runner |
| merge_node | land_danemark | land_daenemark | MEDIUM | merge_node not yet supported by runner |
| canonicalize_node | land_daenemark | — | LOW | Hold for atomic apply alongside the merge; ensures alias `Daenemark` is added only when the merge actually rewires the 6 inbound LIEGT_IN_LAND rels. |

## Human decision queue

None for round 002 — all four deferred ops are deterministic once `merge_node`
is implemented. The `stadt_*` cluster (Brüssel, Molenbeek, Auderghem,
Anderlecht) was inspected: these are *different* sub-municipalities and must
**not** be merged.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- v1 manifest will gain `superseded_by` pointer.
- Active patch is UTF-8 LF and dry-run safe.
- Deferred patch is UTF-8 LF; will become dry-run safe once §6 step C lands.
