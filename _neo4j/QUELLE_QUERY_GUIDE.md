# How to find where a fact in `mit-bestand` came from

Authoritative guide after the 2026-05-23 source trace migration and the
2026-05-28 source-status normalization.

## 30-second mental model

The old source hop is gone:

```cypher
MATCH ()-[r:ZITIERT_QUELLE]->()
RETURN count(r);  // 0
```

Fact/claim relationships now carry a small source state directly:

```text
source_status = exact | candidate | missing | derived
```

Use `source_url` as fact proof only when `source_status = 'exact'` and the relationship is tied to a concrete URL endpoint or a single resolved source. Broad document-level URL sets are not evidence for a specific fact. They live in `candidate_source_urls` with `source_status = 'candidate'` and require review before promotion. Lineage/audit/bookkeeping relationships such as `CITED_FROM_DOSSIER`, `CONCERNS`, `ANCHORED_BY`, or `HAS_SOURCE_LINK` may carry URLs as context or inventory, but they must not carry `source_status`. Malformed/truncated URL strings are not exposed as trusted or candidate URLs; they are kept only in `invalid_source_url` / `invalid_candidate_source_urls` for cleanup.

`:ExternalLink`, `:SectionRef`, and `:UrlMetadata` nodes may still exist as URL metadata, but normal source lookup must not depend on a `:ZITIERT_QUELLE` traversal.

## Query 1 - just give me the URLs for this thing

```cypher
MATCH (n {id: 'p_holbein_gardens_london'})
RETURN n.primary_source_url AS primary,
       n.source_urls AS source_url_inventory,
       n.source_count AS inventory_n,
       n.candidate_source_urls AS candidate_urls,
       n.candidate_source_count AS candidate_n;
```

This is the fast browser/card query. Node-level URLs are inventory/visibility, not proof for every fact attached to the node.

## Query 2 - show relationship-level source context

```cypher
MATCH (n {id: 'p_holbein_gardens_london'})-[r]-(other)
WHERE r.source_status = 'exact'
  AND r.source_url IS NOT NULL
  AND coalesce(r.source_role, 'fact') = 'fact'
RETURN DISTINCT r.source_url AS url,
       type(r) AS rel_type,
       other.id AS context_id,
       labels(other) AS context_labels,
       r.source_status AS source_status,
       r.locator AS locator,
       r.evidence_source_id AS evidence_source_id,
       r.evidence_excerpt AS excerpt,
       r.source_resolution_status AS source_resolution_status
ORDER BY rel_type, context_id, url;
```

This is the replacement for the old `BELEGT_IN -> Dossier -> ZITIERT_QUELLE -> ExternalLink` query.

## Query 3 - which facts cite this URL directly?

```cypher
MATCH (a)-[r]-(b)
WHERE r.source_status = 'exact'
  AND r.source_url = 'https://www.baunetzwissen.de/...'
  AND coalesce(r.source_role, 'fact') = 'fact'
RETURN type(r) AS rel_type,
       labels(a) AS a_labels,
       a.id AS a_id,
       labels(b) AS b_labels,
       b.id AS b_id,
       r.locator AS locator
ORDER BY rel_type, a_id, b_id;
```

Use this to find facts, not just source documents, attached to a trusted URL.

## Query 4 - which nodes share this source?

```cypher
MATCH (n)
WHERE 'https://standards.iteh.ai/...' IN coalesce(n.source_urls, [])
   OR n.source_url = 'https://standards.iteh.ai/...'
RETURN labels(n) AS labels, n.id AS id, n.name AS name
ORDER BY labels, id;
```

## Query 5 - unresolved source review queue

```cypher
MATCH (a)-[r]->(b)
WHERE r.source_status IN ['candidate', 'missing']
RETURN type(r) AS rel_type,
       a.id AS start_id,
       b.id AS end_id,
       r.source_status AS source_status,
       r.evidence_source_id AS evidence_source_id,
       r.evidence_origin AS evidence_origin,
       r.evidence_basis AS evidence_basis
ORDER BY rel_type, start_id, end_id
LIMIT 200;
```

These rows are honest residuals: the graph has provenance text or a legacy run id, but no concrete URL can be assigned automatically without source review.

Candidate URL sets are visible separately:

```cypher
MATCH (a)-[r]->(b)
WHERE r.candidate_source_urls IS NOT NULL
RETURN type(r) AS rel_type,
       a.id AS start_id,
       b.id AS end_id,
       r.evidence_source_id AS evidence_source_id,
       r.candidate_source_urls AS candidate_urls
LIMIT 50;
```

## What's where

| If you want | Look at |
|---|---|
| Node URL inventory / clickable visibility | `n.source_urls`, `n.primary_source_url` |
| Candidate URLs needing review | `n.candidate_source_urls`, `r.candidate_source_urls` |
| Invalid/truncated URL strings | `invalid_source_url`, `invalid_candidate_source_urls` |
| URL for a specific relationship | `r.source_url` |
| Minimal source state for a fact relationship | `r.source_status` |
| Context/inventory, not fact proof | `r.source_role = 'lineage_only'`, `audit_only`, `ontology_anchor`, or `source_inventory` |
| Row locator / section locator | `r.locator` |
| Original source id | `r.evidence_source_id` |
| Evidence text | `r.evidence_excerpt` |
| URL reachability/cache metadata | matching `:ExternalLink` / `:UrlMetadata` node by `.url` |
| Unresolved URL provenance | `r.source_resolution_status = 'needs_source_url_review'` and related `:DataIssue` |

## Helper script

```bash
python _scripts/find_sources.py p_holbein_gardens_london
python _scripts/find_sources.py p_holbein_gardens_london --full
```

`--full` now separates exact fact sources, candidate review leads, and node URL inventory. It does not use `:ZITIERT_QUELLE`.

## Current migration artefacts

- Run report: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/zitiert_quelle_trace_report.md`
- Strict binding cleanup: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_source_url_binding_cleanup.json`
- Invalid URL cleanup: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_invalid_url_cleanup.json`
- Node URL array cleanup: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_node_url_array_cleanup.json`
- Candidate URL cleanup: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/reports/strict_candidate_url_array_cleanup.json`
- Legacy edge ledger: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/zitiert_quelle_resolution_ledger.jsonl`
- Information edge ledger: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/information_source_url_ledger.jsonl`
- Review queue: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/source_url_unresolved_review.jsonl`
- Candidate URL review queue: `_neo4j/intake/runs/2026-05-23_trace_zitiert_quelle_to_urls/logs/strict_candidate_source_url_review.jsonl`
- Backup: `_neo4j/review/backups/2026-05-23_pre_trace_zitiert_quelle_to_urls`
- Source-status normalization: `_neo4j/intake/runs/2026-05-28_source_status_normalization/reports/source_status_normalization_report.md`
- Source-status correction: `_neo4j/intake/runs/2026-05-28_source_status_correction/reports/source_status_correction_report.md`
- Source-status scope addendum: `_neo4j/intake/runs/2026-05-28_source_status_correction/reports/source_status_scope_addendum_report.md`
- Backup before source-status normalization: `_neo4j/review/backups/2026-05-28_pre_source_status_normalization`

## What does not exist anymore

- `:ZITIERT_QUELLE` relationships in the live graph.
- `:Quelle.text_content` on dossiers.
- Source lookup that requires archived markdown as a canonical path.

## When to refresh visibility

After future imports, write `source_status = 'exact'` and `source_url` only when the fact-to-URL binding is exact. If the importer only knows the source document's URL list, write `source_status = 'candidate'`, `candidate_source_urls`, and `source_resolution_status = 'needs_source_url_review'`. For lineage/audit/bookkeeping/source-inventory relationships, keep URLs as context and set `source_role` instead of `source_status`. Do not recreate `:ZITIERT_QUELLE`.
