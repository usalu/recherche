# 01 Global Technical Audit Plan

## Scope

Run against all existing repo exports:

```text
neo4j_exports/batches/batch_*/
neo4j_exports/vocabulary/
neo4j_exports/registry/
```

This does not require the original markdown files.

## Chunk size

Run on **all batches at once**. This is a mechanical check and should not be split by project unless it fails due to memory.

## Checks

Agent must check:

```text
1. JSONL syntax for every .kg.jsonl and patch candidate.
2. JSON schema compliance for every node/rel record.
3. Manifest schema compliance.
4. Duplicate node ids with conflicting labels.
5. Duplicate node ids with conflicting canonical properties.
6. Duplicate relationship ids with conflicting endpoints/type.
7. Missing relationship endpoints.
8. Unexpected labels.
9. Unexpected relationship types.
10. Any Fallbeispiel nodes.
11. Any Kennwert nodes.
12. Any BELEGT_IN relationship without datenqualitaet = "Belegt".
13. Any non-seed emitted node with fewer than 2 incident relationships.
14. Any Projekt without BELEGT_IN.
15. Any Projekt without HAT_BAUTEILGRUPPE or NUTZT_BAUWERK.
16. Any Bauteilgruppe without BELEGT_IN.
17. Any Bauteilgruppe without HAT_BAUTEILTYP.
18. Any Bauteilgruppe without NUTZT_MATERIAL or HAT_BAUTEILEBENE.
```

## Output files

```text
global_audit_report.md
patches/global_technical.patch.jsonl
patch_manifest.json
```

## Severity levels

```text
BLOCKER  = import would fail or graph integrity breaks
HIGH     = import works but graph semantics are wrong
MEDIUM   = query quality is reduced
LOW      = naming, alias, formatting, or readability improvement
INFO     = observation only
```

## Patch only deterministic fixes

Examples:
```json
{"op":"delete_node","id":"fall_x","reason":"Fallbeispiel is forbidden","severity":"HIGH"}
{"op":"set_rel_properties","id":"r_x","properties":{"datenqualitaet":"Belegt"},"reason":"BELEGT_IN must carry source evidence quality","severity":"HIGH"}
{"op":"add_rel","from":"p_x","type":"BELEGT_IN","to":"q_x","properties":{"datenqualitaet":"Belegt"},"reason":"Projekt missing source link","severity":"BLOCKER"}
```

If a fix needs human interpretation, write it in the report as `NEEDS_REVIEW`.
