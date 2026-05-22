# Merge guidance

Use only rows where:

- `recommended_action` is `ADD_OR_KEEP`, and
- `import_safe_without_manual_review` is `yes`, and
- `target_id` does not start with `LOOKUP_REQUIRED`.

Rows with `THIRD_PARTY_*`, `DIRECT_FIRST_PARTY_SEARCH`, or `LOOKUP_REQUIRED_*` are still evidence/leads, but review them manually if your import policy requires fetched first-party line references.

For process/proof/dismantling rows, first run the Cypher lookup requested in the original brief to map the textual candidate to an existing graph ID.
