# Minimal properties Phase 1 P0 patch

**Generated UTC:** 2026-06-01T00:04:02.423580+00:00
**Database:** `mit-bestand`

## Outputs

- Patch: `_neo4j\review\2026-06-01_minimal_property_audit_mit-bestand\phase1_p0\minimal_properties_phase1_p0.patch.jsonl`
- Unaddressed rel Cypher: `_neo4j\review\2026-06-01_minimal_property_audit_mit-bestand\phase1_p0\minimal_properties_phase1_unaddressed_relationships.cypher`
- Summary: `_neo4j\review\2026-06-01_minimal_property_audit_mit-bestand\phase1_p0\minimal_properties_phase1_summary.json`

## Counts

- Patch records: 8012
- Node patch records: 5376
- Relationship patch records: 2636
- Node property removals: 5422
- Relationship property removals via JSONL patch: 2636
- Relationship property removals parked as Cypher: 97

## Unaddressed relationship rows

| Type | Property | Count |
|---|---|---:|
| `HAT_AKTEURROLLE` | `scope` | 7 |
| `HAT_AKTEURTYP` | `scope` | 2 |
| `HAT_KENNWERT` | `candidate_source_count` | 88 |

## Apply protocol

1. Backup `mit-bestand`.
2. Dry-run the JSONL patch.
3. Apply the JSONL patch only if dry-run reports zero errors.
4. Review the Cypher file separately; it handles rels without `r.id`.
5. Rerun `_scripts/_gap_survey.py` and the minimal-property audit.
