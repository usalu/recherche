# Round 002 Controlled Vocabulary Review: Material + Materialgruppe

## Result In Context

Round 001 left material vocabulary structurally importable. No live Material nodes share the same lowercase display name. The actionable issue is semantic/canonical: `mat_textil` has accumulated source spelling variants and should remain a review candidate, not an automatic live patch.

## Material Hub Snapshot

| id | name | groups | Bauteilgruppen |
| --- | --- | --- | --- |
| mat_stahl | Stahl | Metall | 118 |
| mat_holz | Holz | Holz_Biobasiert | 89 |
| mat_beton | Beton | Mineralisch | 51 |
| mat_glas | Glas | Glas_Keramik | 45 |
| mat_stahlbeton | Stahlbeton | Mineralisch | 39 |
| mat_keramik | Keramik | Glas_Keramik | 33 |
| mat_ziegel | Ziegel | Mineralisch | 24 |
| mat_naturstein | Naturstein | Mineralisch | 20 |
| mat_daemmstoff | Daemmstoff | Daemmstoff | 16 |
| mat_aluminium | Aluminium | Metall | 14 |
| mat_kunststoff | Kunststoff | Kunststoff | 10 |
| mat_mdf | MDF / mitteldichte Faserplatte | Holz_Biobasiert, Verbundstoff | 4 |
| mat_textil | Textil / Filz / textile Fasern | Kunststoff, Verbundstoff | 4 |
| mat_recyclingbeton | Recyclingbeton | Recyclingmaterial | 3 |
| mat_faserzement | Faserzement / Eternit | Mineralisch, Verbundstoff | 2 |
| mat_gusseisen | Gusseisen | Metall | 2 |
| mat_bitumen | Bitumen | Kunststoff, Verbundstoff | 1 |
| mat_lehm | Lehm | Lehm_Erde | 1 |
| mat_stroh | Stroh | Holz_Biobasiert | 0 |

## Candidate Patch

- `controlled_vocabulary_material.patch.jsonl` contains 1 LOW `canonicalize_node` candidate for `mat_textil`.
- No merge or delete operation is proposed in this round.
