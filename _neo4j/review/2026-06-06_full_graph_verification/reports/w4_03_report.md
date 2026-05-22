# W4-03 selective unsupported deletes

**Date:** 2026-06-07T12:52:32Z · **Agent:** W4-03 · **Database:** `mit-bestand`
**Scope:** delete_rel ops with no `bg_` / `:Bauteilgruppe` involvement
**Deletes in scope:** 86 · **bg_ skipped (wave total):** 416

## Rel types

| rel_type | count |
|---|---:|
| NUTZT_MATERIAL | 86 |

## Sample deletes (first 5)

- `archipel_sion_ressourcerie` —[NUTZT_MATERIAL]→ `mat_daemmstoff`
- `archipel_sion_ressourcerie` —[NUTZT_MATERIAL]→ `mat_stahl`
- `batiterre` —[NUTZT_MATERIAL]→ `mat_glas`
- `batiterre` —[NUTZT_MATERIAL]→ `mat_kunststoff`
- `batiterre` —[NUTZT_MATERIAL]→ `mat_ziegel`

**Applied to graph:** yes (86 rels deleted via consolidated patch)
