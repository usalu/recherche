# Bauteilbörsen evidence continuation 3 — final correction/extension pass

Date: 2026-05-31

This package is **additive/corrective**. It does not overwrite the previous ZIPs. It focuses on material and Bauteiltyp claims and intentionally separates rejected/non-importable evidence.

## Files

- `csv/evidence_added_corrected_continuation_3.csv` — 95 evidence rows.
- `csv/rejected_do_not_import_continuation_3.csv` — 15 rows that should **not** be imported as claims.
- `csv/source_register_continuation_3.csv` — source URL register with retrieval notes and line/search references.
- `csv/per_anchor_delta_summary_continuation_3.csv` — anchor-level coverage summary.
- `csv/process_pruefung_rueckbau_candidates_need_cypher_lookup.csv` — process/proof/dismantling candidates where the exact live graph ID must be looked up.
- `json_delta/*.enrichment_delta.json` — one JSON delta per touched anchor.
- `CHANGES_AND_DECISIONS.md` — concise explanation of what changed and what remains unsafe.

## Reliability rules used in this pass

1. **No material ID was imported from component-only wording** unless the material word itself appeared (`Bois`, `PVC`, `Verre`, `fonte`, `céramique`, etc.).
2. `Carrelage`, `Fliesen`, or `tiles` were treated as **Bauteiltyp evidence** but not as `mat_keramik` unless the source explicitly said ceramic/céramique/Keramik.
3. Generic `metal/Metall/Metaal` was **not** mapped to `mat_stahl`.
4. Search-result extracts and third-party sources are clearly marked. They are useful for leads, but are not always import-safe without manual review.
5. Pruefung/Aufbereitung/Rueckbau candidates are recorded as `LOOKUP_REQUIRED_*` when the graph node ID was not available in this environment.
