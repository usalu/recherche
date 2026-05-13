# Agent notes — batch_007

Import after the global `controlled_vocabulary.seed.kg.jsonl` and before/with this batch's `controlled_terms.delta.jsonl`.

Important modeling notes:

- `Institut de Botanique de l’ULg` is modeled as a comparison case with only the partially documented reclaimed timber facade counted as direct reuse.
- `Jeugdkliniek Ithaka / Emergis` separates donor components from RWS Terneuzen from the retained Emergis Bestand in Kloetinge.
- `Juch-Areal Recyclingzentrum` is intentionally marked as planned/watchlist; it contains planned direct reuse of the Hagenholz hall structure and Kerenzerberg tunnel plates.
- `K.118` is a high-confidence main case with reused steel structure from ELYS Basel, reused external stair, and additional envelope/interior component groups.
- `KA13` is a high-confidence main case with donor hollow-core slabs and reused steel; retained existing structure is explicitly not counted as direct reuse.

Do not convert scalar metrics into `Kennwert` nodes. Do not create `Fallbeispiel` nodes. `BELEGT_IN.datenqualitaet` is always `Belegt`.
