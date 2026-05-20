# Batch2 v2 phase generator scripts

One-shot generators that produced the JSONL patches for the 2026-05-20 batch2 v2 import.

**Don't delete.** They are the receipt for how each phase's patch was built. If you need to:

- Re-derive a patch from its spec → run the matching generator
- Audit a phase's logic → read the script
- Build a similar phase for a future batch → fork the script

## Script → patch mapping

| Generator | Produces | Notes |
|---|---|---|
| `_generate_phase6_bg_rels.py` | `phase_batch2_v2_6b_bg_rels.patch.jsonl` | BG mandatory + optional rels |
| `_generate_phase8_project_vocab.py` | `phase_batch2_v2_8_project_vocab.patch.jsonl` | Projekt-level vocab links |
| `_generate_phase10_huerde_wirtschaft.py` | `phase_batch2_v2_10_huerde_wirtschaft.patch.jsonl` | Hürde-Wirtschaft links |
| `_generate_phase11_bg_vocab.py` | `phase_batch2_v2_11_bg_vocab.patch.jsonl` | BG optional vocab (42 BGs) |
| `_generate_phase12_deferred_bgs.py` | `phase_batch2_v2_12a_*` + `12b_*` | Deferred 19 BGs (split patch) |
| `_generate_phase13_more_actors.py` | `phase_batch2_v2_13a_*` + `13b_*` | Round-2 Akteur enrichments |
| `_generate_phase19_counts_as.py` | `phase_batch2_v2_19_counts_as.patch.jsonl` | `counts_as_*` property derivation |
| `_generate_phase20_ketten.py` | `phase_batch2_v2_20a_kette_addnodes.patch.jsonl` + `20b_kette_rels.patch.jsonl` | Auto-discovered Wiederverwendungsketten |
| `_generate_phase24_autodiscovery.py` | `phase_batch2_v2_24_autodiscovery.patch.jsonl` | VERBUNDEN_MIT_AKTEUR pairs from shared-project participation |

See [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md` §6](../../_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md) for the full tooling guide.

## Re-running a generator

Each generator writes its patch under `_neo4j/review/round_002_followup/patches/batch2/`. Running it overwrites the existing patch — only do this if you want to regenerate the patch file (e.g., after fixing a spec table inline in the generator).

```bash
python _scripts/batch2_v2_generators/_generate_phase6_bg_rels.py
```

The applied patches are byte-frozen in `_neo4j/review/round_002_followup/patches/batch2/` and have already been applied to the live database. Regenerating won't change live state; it only refreshes the JSONL file on disk.
