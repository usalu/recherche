# Reuse bubble evidence cleanup — graph-only properties

**Date:** 2026-06-06  
**Database:** `mit-bestand`

## Policy

Evidence and URLs are stored **only** on entity node and relationship properties. Intake runs must not create extra `:Quelle` nodes for external URLs or dossiers.

## Graph changes (committed)

| Metric | Before | After | Delta |
|---|---:|---:|---:|
| Nodes | 2 432 | 2 304 | **−128** |
| Relationships | 15 622 | 15 527 | **−95** |

Removed from all five reuse-bubble `review_run` tags:

- **128** `:Quelle` nodes (ExternalLink + ResearchDocument intake mirrors)
- **95** `BELEGT_IN` edges to those quellen
- Pointer properties on bubble rels: `evidence_source_id`, `secondary_evidence_source_ids`, `archive_source_id`, `metadata_sidecar_key`, `evidence_claim_ids`

URLs merged onto entity nodes as `primary_source_url` + `source_urls` where `BELEGT_IN` had carried them.

## Patch normalization (all 5 runs)

- `patches/phase0_sources_and_dossier.patch.jsonl` → **emptied** (backups: `*.bak`)
- All other patches: `BELEGT_IN` → `set_node_properties`; rel props cleaned
- Regenerate tool: `_scripts/normalize_bubble_evidence_patches.py`

## Affected review runs

- `swiss_reuse_bubble_2026_06_05`
- `germany_reuse_bubble_2026_06_05`
- `france_reuse_bubble_2026_06_05`
- `netherlands_reuse_bubble_2026_06_05`
- `rotor_dc_reuse_bubble_2026_06_05`

## Verify

```cypher
MATCH (q:Quelle) WHERE q.review_run IN [
  'swiss_reuse_bubble_2026_06_05',
  'germany_reuse_bubble_2026_06_05',
  'france_reuse_bubble_2026_06_05',
  'netherlands_reuse_bubble_2026_06_05',
  'rotor_dc_reuse_bubble_2026_06_05'
] RETURN count(q);  // expect 0

MATCH ()-[r]->()
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN r.evidence_url, r.evidence_quote, r.evidence_confidence
LIMIT 5;
```

## Evidence on properties (2026-06-06 follow-up)

- **46** entity nodes received `primary_source_url` + `source_urls` from former `BELEGT_IN` anchors
- **8** hub actors (pre-existing, mesh-only) received homepage URLs
- All bubble rels: `evidence_url`, `evidence_quote`, `evidence_confidence`, `evidence_basis` — **0** pointer props remaining
- Patches synced: phase1c-deleted weak edges removed from phase1 patch files; `evidence_source_id` stripped from phase1c

Tool: `apply_evidence_property_fix.py --commit`

## Re-run cleanup

```bash
python _neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/apply_quelle_cleanup.py --commit
python _neo4j/review/2026-06-06_reuse_bubble_quelle_cleanup/apply_evidence_property_fix.py --commit
```
