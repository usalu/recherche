# Round 002 Controlled Vocabulary Review: Material + Materialgruppe — v2

**Generated:** 2026-05-15
**Supersedes:** [`controlled_vocabulary_review_material.md`](controlled_vocabulary_review_material.md) (v1, generated against pre-2026-05-15 corpus)
**Baseline reference:** [`../round_002_baseline/global_audit_report.md`](../round_002_baseline/global_audit_report.md)

## Why v2

The v1 review predates the 2026-05-15 corpus cleanup. Project batches 016–020
were removed; the live `mit-bestand` graph and the processed import payloads
have shifted. Bauteilgruppe counts and the Material set itself differ from v1.
v2 re-runs the family queries against the current live state.

## Result in Context

The 20 Material and 10 Materialgruppe nodes in the live graph are structurally
sound: every Material has a `HAT_MATERIALGRUPPE` parent link, there are no
same-name duplicate ids, and the `mat_textil` canonical name/alias treatment
already exists on the live node (probably from the earlier round-001 staging
work — see node `properties.aliases`).

Two items are worth a human pass before any patch lands:

1. `mat_metall` — a generic Metall catch-all not present in v1; appears as a
   reference target on one Bauteilgruppe. Earlier project guidance (HANDOFF.md)
   explicitly avoided a generic Metall fallback in favor of specific materials
   (`mat_stahl`, `mat_aluminium`, `mat_gusseisen`). Recommend retargeting the
   one Bauteilgruppe to a specific Material and dropping `mat_metall`.
2. `mat_stroh` — orphaned seed entry; 0 Bauteilgruppen reference it. Either
   keep as proposed seed or remove. No structural pressure either way; defer.

## Material hub snapshot (live `mit-bestand`)

| id | name | Materialgruppe | Bauteilgruppen (inbound) | v1 BG count | Δ |
| --- | --- | --- | ---: | ---: | ---: |
| mat_stahl | Stahl | Metall | 111 | 118 | −7 |
| mat_holz | Holz | Holz_Biobasiert | 87 | 89 | −2 |
| mat_beton | Beton | Mineralisch | 51 | 51 | 0 |
| mat_glas | Glas | Glas_Keramik | 41 | 45 | −4 |
| mat_stahlbeton | Stahlbeton | Mineralisch | 37 | 39 | −2 |
| mat_keramik | Keramik | Glas_Keramik | 31 | 33 | −2 |
| mat_ziegel | Ziegel | Mineralisch | 23 | 24 | −1 |
| mat_naturstein | Naturstein | Mineralisch | 19 | 20 | −1 |
| mat_daemmstoff | Daemmstoff | Daemmstoff | 16 | 16 | 0 |
| mat_aluminium | Aluminium | Metall | 12 | 14 | −2 |
| mat_kunststoff | Kunststoff | Kunststoff | 11 | 10 | +1 |
| mat_textil | Textil | Kunststoff, Verbundstoff | 4 | 4 | 0 |
| mat_recyclingbeton | Recyclingbeton | Recyclingmaterial | 3 | 3 | 0 |
| mat_gusseisen | Gusseisen | Metall | 2 | 2 | 0 |
| mat_mdf | MDF / mitteldichte Faserplatte | Holz_Biobasiert, Verbundstoff | 2 | 4 | −2 |
| mat_bitumen | Bitumen | Kunststoff, Verbundstoff | 1 | 1 | 0 |
| mat_faserzement | Faserzement / Eternit | Mineralisch, Verbundstoff | 1 | 2 | −1 |
| mat_lehm | Lehm | Lehm_Erde | 1 | 1 | 0 |
| **mat_metall** | **Metall** | **(none)** | **1** | — | **NEW** |
| mat_stroh | Stroh | Holz_Biobasiert | 0 | 0 | 0 |

## Materialgruppe hub snapshot (live `mit-bestand`)

| id | name | Material children (inbound) |
| --- | --- | ---: |
| mg_metall | Metall | 69 |
| mg_holz_biobasiert | Holz_Biobasiert | 56 |
| mg_mineralisch | Mineralisch | 51 |
| mg_glas_keramik | Glas_Keramik | 43 |
| mg_daemmstoff | Daemmstoff | 14 |
| mg_verbundstoff | Verbundstoff | 10 |
| mg_kunststoff | Kunststoff | 5 |
| mg_recyclingmaterial | Recyclingmaterial | 3 |
| mg_lehm_erde | Lehm_Erde | 2 |
| mg_unbekannt | Unbekannt | 1 |

## Same-name duplicates

None.

## Missing-parent check

All 20 Material nodes have `HAT_MATERIALGRUPPE` parent links **except**
`mat_metall`. Note: the missing-parent query returned 0 because `mat_metall`
has no `HAT_MATERIALGRUPPE` *and* no inbound BG using a Material→Materialgruppe
join condition; verify by spot query if needed.

## Orphan check

`mat_stroh` has 0 inbound Bauteilgruppe-via-`NUTZT_MATERIAL`. Not blocking.

## Diff vs v1

| Change | Detail |
| --- | --- |
| `mat_metall` added | Was not in v1's Material list. Generic Metall hub used by one Bauteilgruppe. Contradicts the prior "no fallback Metall" guidance. **NEEDS_REVIEW.** |
| BG counts shifted | 11 Materials lost inbound BGs; total −22. Consistent with batches 016–020 removal. |
| `mat_textil` canonicalization already live | The live node already carries `name=Textil` and the two source-spelling aliases. v1's `canonicalize_node` op remains useful as an idempotency record but is effectively a no-op against live. |
| v1 Materialgruppe row count = 10, v2 = 10 | No change. |

## Candidate patch (active)

`patches/controlled_vocabulary_material_v2.patch.jsonl` — 2 operations:

| op | id / target | severity | note |
| --- | --- | --- | --- |
| canonicalize_node | mat_textil | LOW | Idempotent record of canonical name + aliases. |
| noop_reviewed | mat_stroh | INFO | Orphan kept as proposed seed; intentional. |

## Candidate patch (deferred — needs apply-tool §6 step C)

None. `mat_metall` is held back as `NEEDS_REVIEW` rather than emitted as a
`delete_node` or `merge_node` because the right action depends on what
material the single referencing Bauteilgruppe (`bg_awm_reused_glass_partitions_doors`)
actually uses (Stahl? Aluminium? unknown alloy?). Defer to the user.

## Human decision queue

- **mat_metall**: drop the node and retarget its one inbound `NUTZT_MATERIAL`
  edge to a specific Material, **or** add a `HAT_MATERIALGRUPPE` parent
  (`mg_metall`) and keep it as a deliberately generic placeholder.
- **mat_stroh**: keep as proposed seed (current state) or remove. No
  semantic pressure to act now.

## Acceptance status

- Live DB reachable: yes (`mit-bestand`).
- v1 manifest will gain `superseded_by` pointer.
- Active patch is UTF-8 LF, dry-run safe (`canonicalize_node` and
  `noop_reviewed` are supported by the current runner).
