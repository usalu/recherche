# 03 Project Content Review Plan

## Goal

Review project content in small chunks and improve semantic correctness without rewriting entire batches.

## Chunk size

Review exactly **5 projects per run**.

Exceptions:
- A previously generated batch with 6 projects may be reviewed as 6 if the projects are small.
- Very complex projects, such as multi-building reuse chains, may be reviewed alone or in groups of 2–3.

## Project review checklist

For each project, answer:

```text
1. Is the Projekt node the correct root?
2. Is bewertung correct as a scalar on Projekt?
3. Are project-level metrics on Projekt?
4. Are building-level metrics on Bauwerk?
5. Are component-level metrics on Bauteilgruppe?
6. Are donor and receiver Bauwerk nodes correct?
7. Is Bestandserhalt separated from counted direct reuse?
8. Are all Bauteilgruppen meaningful and not too broad?
9. Should any Bauteilgruppe be split?
10. Should any Bauteilgruppe be merged?
11. Are Bauteiltyp relationships useful and controlled?
12. Are Material and Materialgruppe links correct?
13. Are Huerde and HuerdeKategorie links useful?
14. Are PruefungNachweis, Leistungsanforderung and Norm links present when documented?
15. Are Akteurrolle and Akteurtyp modeled as nodes?
16. Are source links to Quelle present?
17. Are raw notes only used when controlled nodes are not sufficient?
```

## Patch action vocabulary

Use only these action keywords in review notes:

```text
KEEP
FIX
ADD
DELETE
MERGE
SPLIT
MOVE_PROPERTY
RETYPE_REL
SOURCE_CHECK
```

## Output files

For each chunk:

```text
project_review_batch_<n>.md
patches/batch_<n>_content.patch.jsonl
patch_manifest.json
```

## Example review note

```text
FIX | p_house_of_fraser_318_oxford_street_tbc_london_reuse_chain
Issue: reused steel quantity has conflicting values but only one scalar exists.
Patch: add steel_menge_t_min and steel_menge_t_max; keep note.
Severity: MEDIUM
```

## Example patch

```json
{"op":"set_node_properties","id":"bg_house_of_fraser_reused_steel","properties":{"menge_t_min":16,"menge_t_max":100,"note":"Conflicting steel reuse quantities in sources"},"reason":"preserve source conflict as scalar range","severity":"MEDIUM"}
```
