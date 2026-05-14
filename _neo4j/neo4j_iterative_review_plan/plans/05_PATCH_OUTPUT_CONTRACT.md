# 05 Patch Output Contract

## Purpose

Patch files are the only correction format produced during iterative review. They are designed for repo agents and MCP importers.

## Patch file naming

```text
patches/
  global_technical.patch.jsonl
  controlled_vocabulary_material.patch.jsonl
  batch_007_content.patch.jsonl
  query_direct_structural_reuse.patch.jsonl
```

## Record format

Each patch record is one JSON object per line.

Required fields:
```json
{"op":"set_node_properties","reason":"why this patch is needed"}
```

## Allowed operations

```text
add_node
add_rel
delete_node
delete_rel
set_node_properties
set_rel_properties
remove_node_properties
remove_rel_properties
merge_node
canonicalize_node
rename_property
move_property
replace_rel_type
```

## Operation examples

```json
{"op":"add_rel","from":"bg_x","type":"HAT_HUERDE","to":"h_technische_freigabe","properties":{},"reason":"documented technical approval hurdle","severity":"MEDIUM"}
{"op":"set_node_properties","id":"p_x","properties":{"flaeche_m2":1412},"reason":"normalize area metric","severity":"LOW"}
{"op":"merge_node","from":"mat_textil_filz","to":"mat_textil","reason":"same material, keep specific term as alias","severity":"MEDIUM"}
{"op":"canonicalize_node","id":"a_rotor","canonical_name":"Rotor","aliases":["ROTOR","Rotor DC"],"reason":"stable actor display name","severity":"LOW"}
```

## Idempotency requirement

Every patch must be safe to apply more than once.

Agents should use:
```cypher
MERGE for nodes
MERGE for relationships
SET += for additive properties
```

## Forbidden patch behavior

Do not:
```text
overwrite canonical names without recording alias
delete source links unless clearly duplicated
delete Quelle nodes
recreate Fallbeispiel
create Kennwert nodes
create Datenqualitaet nodes
```
