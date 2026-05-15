# Neo4j intake

New raw packages go into `inbox/` unchanged.

```text
inbox/
  projects/
  actor_registry/
```

After processing, move the untouched raw package into `archive/<run-id>/` and keep the generated reports in `runs/<run-id>/`.

## Current adapters

| Adapter | Expected input |
|---|---|
| `projects` | old project-batch export layout containing `p_*.kg.jsonl` files |
| `actor-registry` | actor-registry tree containing canonical chunk files |

## Example commands

```text
python _scripts/process_neo4j_intake.py projects --input-root <raw-tree> --output-root _neo4j/processed/projects
python _scripts/process_neo4j_intake.py actor-registry --input-root <raw-tree> --output-root _neo4j/processed/actor_registry
```

## After processing

Inspect the merge report and provenance first. If the run is approved:

```text
python _scripts/import_jsonl_to_neo4j.py _neo4j/processed/projects/vocabulary/controlled_vocabulary.seed.kg.jsonl
python _scripts/import_jsonl_to_neo4j.py _neo4j/processed/projects/vocabulary/controlled_terms.merged.kg.jsonl
python _scripts/import_jsonl_to_neo4j.py _neo4j/processed/projects/records/*.kg.jsonl

python _scripts/import_jsonl_to_neo4j.py _neo4j/processed/actor_registry/actor_registry.canonical.kg.jsonl
```

## Rule

Processing creates **reviewable import payloads**, not a replacement source of truth. Neo4j remains authoritative.
