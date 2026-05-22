# Global Source Evidence Similar-Issues Report

Date: 2026-05-28  
Database: `mit-bestand`  
Purpose: scan for source-evidence problems similar to the actor/Bauteilboersen cleanup.

## Files

- Scan: `_neo4j/review/global_source_evidence_issue_scan.json`
- Focus scan: `_neo4j/review/global_source_evidence_issue_scan_focus.json`
- Cleanup patch: `_neo4j/review/anchor_source_evidence_cleanup.patch.jsonl`
- Post-check: `_neo4j/review/global_source_evidence_issue_scan_post_anchor_cleanup.json`
- Backup: `_neo4j/review/backups/2026-05-28_pre_anchor_source_evidence_cleanup`

## What Was Found

The main actor evidence patterns are now clean:

| Check | Result |
|---|---:|
| Remaining `evidence_terms` on relationships | 0 |
| Duplicate actor-country paths using both `LIEGT_IN_LAND` and `GEHÖRT_ZU` | 0 |
| Unmarked suspicious actor-role auto-classification candidates | 0 |
| Unmarked relationships with `evidence_source_id` but no resolvable `Quelle.url` | 0 after cleanup |

The one clear similar issue was `ANCHORED_BY`.

Before cleanup:

| Relationship type | Problem | Count |
|---|---|---:|
| `ANCHORED_BY` | used internal anchor source ids like `q_controlled_vocab_seed` / `q_akteursliste_master_md` without a `source_resolution_status` | 703 |

These are bookkeeping/ontology-anchor links, not external proof for factual claims.

## What Was Fixed

Applied `_neo4j/review/anchor_source_evidence_cleanup.patch.jsonl`.

Graph size stayed unchanged:

| Before | After |
|---:|---:|
| 39,548 nodes / 81,031 relationships | 39,548 nodes / 81,031 relationships |

All 703 `ANCHORED_BY` links now carry:

- `review_status = "needs_source_url_review"`
- `source_resolution_status = "bookkeeping_anchor_internal_source_not_claim_evidence"`
- `source_role = "ontology_anchor_bookkeeping"`
- `evidence_quality = "internal_anchor_not_claim_evidence"`

This prevents internal anchor links from being read as external claim evidence.

## Remaining Non-Problem Source-URL Cases

These relationship types have `source_url` but no `source_status`, which is acceptable because they already declare a bookkeeping role:

| Relationship type | Count | Existing `source_role` |
|---|---:|---|
| `CITED_FROM_DOSSIER` | 6,150 | `lineage_only` |
| `CONCERNS` | 3,456 with URL props | `audit_only` |
| `HAS_SOURCE_LINK` | 20 | `source_inventory` |

So I did not change these into evidence facts.

## Still Outside This Fix

The broader graph still has normal gap-survey issues unrelated to this evidence cleanup, for example missing `source_scope` on older nodes, missing relationship ids, and some Bauteilgruppe classification gaps. Those should be handled as separate structural cleanup tasks, not mixed into source-evidence remediation.

## Deeper Scan: Confidence Contradictions

After the first cleanup, I scanned for relationships that still claimed strong evidence while also needing source review.

New files:

- Deeper scan: `_neo4j/review/global_source_evidence_deeper_scan.json`
- Contradiction scan: `_neo4j/review/global_source_status_contradiction_scan.json`
- Fix candidates: `_neo4j/review/global_source_evidence_fix_candidates.json`
- Cleanup Cypher: `_neo4j/review/belegt_confidence_conflict_cleanup.cypher`
- Post-check: `_neo4j/review/global_source_evidence_deeper_scan_post_confidence_cleanup.json`
- Backup: `_neo4j/review/backups/2026-05-28_pre_belegt_confidence_conflict_cleanup`

The scan found 172 relationships where:

- `evidence_confidence = "belegt"`
- `source_status` was not `exact`
- and the relationship still had `needs_source_url_review` or another review-needed source status.

These were misleading because a relationship cannot honestly be treated as strongly evidenced while its source binding is still missing or only candidate-level.

I updated those 172 relationships:

- `previous_evidence_confidence = "belegt"`
- `evidence_confidence = "unklar"`
- `evidence_confidence_status = "downgraded_pending_exact_source_url_review"`

No relationships or nodes were deleted.

| Relationship type | Downgraded |
|---|---:|
| `HAT_PRUEFUNG` | 51 |
| `HAT_KENNWERT` | 25 |
| `HAT_AUFBEREITUNG` | 22 |
| `TEILT_LAYER` | 15 |
| `BELEGT_IN` | 14 |
| `HAT_ZERTIFIZIERUNG` | 12 |
| `METHODENGRUNDLAGE_NORM` | 8 |
| `VERBUNDEN_MIT_AKTEUR` | 6 |
| `HAT_AKTEURROLLE` | 6 |
| `GILT_IN_LAND` | 5 |
| `HAS_RISK_POLLUTANT` | 4 |
| `HAT_AKTEURTYP` | 3 |
| `HAT_VERBINDUNGSTECHNIK` | 1 |

Post-check:

| Check | Result |
|---|---:|
| Remaining `belegt` + review-needed + non-exact source contradictions | 0 |
| `source_status = exact` without URL | 0 |
| Unmarked unresolved `evidence_source_id` relationships | 0 |
| Missing-URL `Quelle` nodes without review marker | 0 |

