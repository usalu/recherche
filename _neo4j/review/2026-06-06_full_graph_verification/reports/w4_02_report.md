# W4-02 selective unsupported deletes

**Date:** 2026-06-07T12:52:32Z · **Agent:** W4-02 · **Database:** `mit-bestand`
**Scope:** delete_rel ops with no `bg_` / `:Bauteilgruppe` involvement
**Deletes in scope:** 133 · **bg_ skipped (wave total):** 416

## Rel types

| rel_type | count |
|---|---:|
| HAT_BAUTEILTYP | 133 |

## Sample deletes (first 5)

- `btvz_zuerichsee_oberland` —[HAT_BAUTEILTYP]→ `bt_technik`
- `btvz_zuerichsee_oberland` —[HAT_BAUTEILTYP]→ `bt_tuer`
- `cornermat_retrival` —[HAT_BAUTEILTYP]→ `bt_dach`
- `gebruiktebouwmaterialen` —[HAT_BAUTEILTYP]→ `bt_boden`
- `gebruiktebouwmaterialen` —[HAT_BAUTEILTYP]→ `bt_technik`

**Applied to graph:** yes (133 rels deleted via consolidated patch)
