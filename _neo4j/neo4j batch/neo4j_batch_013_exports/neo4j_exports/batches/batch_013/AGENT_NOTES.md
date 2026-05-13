# Agent notes — batch_013

Import order recommended:
1. `controlled_vocabulary.seed.kg.jsonl`
2. `controlled_terms.delta.jsonl`
3. all `p_*.kg.jsonl` project chunks from this batch

Use node id as MERGE key. Relationship id is stable and can be used as MERGE key for relationships.

This batch contains two new controlled certification nodes:
- `zbs_nordic_swan_ecolabel`
- `zbs_nabers`

Source files processed:
- Superlocal_Expogebouw_Bleijerheide.md
- Svanen_Kindergarten_Gladsaxe.md
- The_Green_House_Utrecht.md
- Thoravej_29_Copenhagen.md
- Timber_Square_London.md
