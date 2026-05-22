# Agent S5 — visibility surfacing

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.**

You are agent S5 of 6. Your job: **denormalise source information onto the user-facing nodes (Projekt, Bauwerk, Akteur) so a single click in Neo4j Browser shows everything that matters.**

The graph traversal is source-of-truth (S1–S3 wrote it). You compute a summary and stamp it on the convenient node for visibility.

---

## §1 Cold-start context

After S1–S3:
- Every `:ExternalLink` has `url_status` and (where reachable) `url_body_cache_path`.
- Every `source_curated` citation edge has `verification_status` and `verification_score`.
- Every node that the user cares about (Projekt, Bauwerk, Akteur) is reachable to one or more `:ExternalLink` via:
  - direct `BELEGT_IN → ExternalLink` (rare)
  - `BELEGT_IN → Dossier → ZITIERT_QUELLE → ExternalLink` (common)
  - `HAS_SOURCE_LINK → ExternalLink` (node-property URLs from S1)

Your job: walk those paths, aggregate, write back a small map of summary properties.

---

## §2 Mission

For every `:Projekt`, `:Bauwerk`, `:Akteur`:

1. Find every reachable `:ExternalLink`.
2. Compute `source_urls` (list of distinct URLs).
3. Compute `source_quality_summary`:
   ```
   {
     n_verbatim:    int,    // verification_status='verbatim_match'
     n_paraphrase:  int,    // 'paraphrase_match' OR 'token_match'
     n_no_match:    int,    // 'no_text_match' OR 'cookie_wall_detected' OR
                            //   'unsupported_javascript_required' OR 'language_mismatch'
     n_dead:        int,    // 'target_page_dead' OR url_status starts with 'dead_'
     n_unchecked:   int     // 'unchecked' OR 'skipped_*'
   }
   ```
4. Compute `source_freshness_summary`:
   ```
   {
     n_reachable:        int,    // url_status='reachable_2xx'
     n_reachable_via_3xx: int,   // url_status='reachable_3xx_to_4xx'
     n_dead:             int,    // url_status starts with 'dead_'
     n_unchecked:        int,    // url_status='unchecked' (should be 0 post-S2)
     n_wayback_fallback: int,    // dead URL but has wayback snapshot
     latest_check_date:  date    // max(url_last_checked_at) across the node's URLs
   }
   ```
5. Compute `source_trust_score` (per QD-7) — single float 0.0–1.0.

---

## §3 The `source_trust_score` formula

```
score(node) = mean over all (node → … → ExternalLink) citation paths of:
              path_score = url_reachability * verification_grade

where:
  url_reachability ∈ {1.0 if reachable_2xx,
                      0.7 if reachable_3xx_to_4xx,
                      0.5 if dead but wayback_snapshot exists,
                      0.0 otherwise}

  verification_grade ∈ {1.0  if verbatim_match,
                        0.85 if paraphrase_match,
                        0.75 if token_match,
                        0.0  if no_text_match,
                        0.5  if target_page_dead (we accept; URL is provably dead),
                        0.4  if unsupported_* (content too hard to verify but URL exists),
                        0.0  if unchecked,
                        verification_score otherwise}
```

A node with 5 verbatim-match citations to reachable URLs → score 1.0.
A node with 5 unchecked citations → score 0.0.
A node with no citations at all → score `NULL` (different from 0.0; means "no sources to score").

---

## §4 Conflict avoidance

You write only on `:Projekt`, `:Bauwerk`, `:Akteur`:
- `source_urls`
- `source_count`
- `source_quality_summary`
- `source_freshness_summary`
- `source_trust_score`
- `source_urls_updated_at`

You DO NOT touch:
- Anything S2 wrote on `:ExternalLink`.
- Anything S3 wrote on citation edges.
- Anything S4 wrote (secondary labels).
- `:DataIssue` (you raise some but don't modify existing ones — `excessive_sources_on_node`).

---

## §5 Migrations

Migration file: [migrations/mig_s5_visibility.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_s5_visibility/migrations/mig_s5_visibility.cypher).

```cypher
// ==========================================================================
// S5.A — :Projekt surfacing
// ==========================================================================

MATCH (p:Projekt)
OPTIONAL MATCH (p)-[bel1:BELEGT_IN]->(d:Dossier)-[z:ZITIERT_QUELLE]->(ext1:ExternalLink)
WITH p, collect(DISTINCT {url: ext1.url, ext: ext1, zq: z}) AS via_dossier
OPTIONAL MATCH (p)-[bel2:BELEGT_IN]->(direct:ExternalLink)
WITH p, via_dossier, collect(DISTINCT {url: direct.url, ext: direct, zq: bel2}) AS via_direct
OPTIONAL MATCH (p)-[hsl:HAS_SOURCE_LINK]->(hsl_ext:ExternalLink)
WITH p, via_dossier, via_direct, collect(DISTINCT {url: hsl_ext.url, ext: hsl_ext, zq: hsl}) AS via_hsl

WITH p, via_dossier + via_direct + via_hsl AS all_paths
WITH p, [path IN all_paths WHERE path.url IS NOT NULL AND path.url <> ''] AS paths

WITH p, paths,
     apoc.coll.toSet([path IN paths | path.url]) AS unique_urls

// Reachability counts
WITH p, paths, unique_urls,
     size([path IN paths WHERE path.ext.url_status = 'reachable_2xx']) AS n_reach,
     size([path IN paths WHERE path.ext.url_status = 'reachable_3xx_to_4xx']) AS n_reach_3xx,
     size([path IN paths WHERE path.ext.url_status STARTS WITH 'dead_']) AS n_dead,
     size([path IN paths WHERE path.ext.url_status IS NULL
                              OR path.ext.url_status = 'unchecked']) AS n_unchecked_url,
     size([path IN paths WHERE path.ext.url_status STARTS WITH 'dead_'
                              AND path.ext.url_wayback_snapshot IS NOT NULL]) AS n_wayback

// Verification counts
WITH p, paths, unique_urls, n_reach, n_reach_3xx, n_dead, n_unchecked_url, n_wayback,
     size([path IN paths WHERE path.zq.verification_status = 'verbatim_match']) AS n_verbatim,
     size([path IN paths WHERE path.zq.verification_status IN ['paraphrase_match','token_match']]) AS n_para,
     size([path IN paths WHERE path.zq.verification_status IN
                                ['no_text_match','cookie_wall_detected',
                                 'unsupported_javascript_required','language_mismatch']]) AS n_nomatch,
     size([path IN paths WHERE path.zq.verification_status = 'target_page_dead']) AS n_v_dead,
     size([path IN paths WHERE path.zq.verification_status IS NULL
                              OR path.zq.verification_status = 'unchecked'
                              OR path.zq.verification_status STARTS WITH 'skipped_']) AS n_v_unchecked

// Latest check
WITH p, paths, unique_urls,
     n_reach, n_reach_3xx, n_dead, n_unchecked_url, n_wayback,
     n_verbatim, n_para, n_nomatch, n_v_dead, n_v_unchecked,
     reduce(latest = NULL, path IN paths |
       CASE WHEN path.ext.url_last_checked_at IS NULL THEN latest
            WHEN latest IS NULL OR path.ext.url_last_checked_at > latest
                 THEN path.ext.url_last_checked_at
            ELSE latest END) AS latest_check

// trust score
WITH p, paths, unique_urls,
     n_reach, n_reach_3xx, n_dead, n_unchecked_url, n_wayback,
     n_verbatim, n_para, n_nomatch, n_v_dead, n_v_unchecked, latest_check,
     CASE WHEN size(paths) = 0 THEN NULL
          ELSE reduce(s = 0.0, path IN paths |
            s + (CASE path.ext.url_status
                   WHEN 'reachable_2xx' THEN 1.0
                   WHEN 'reachable_3xx_to_4xx' THEN 0.7
                   ELSE CASE WHEN path.ext.url_status STARTS WITH 'dead_'
                                  AND path.ext.url_wayback_snapshot IS NOT NULL
                             THEN 0.5
                             ELSE 0.0 END
                 END) *
                (CASE path.zq.verification_status
                   WHEN 'verbatim_match' THEN 1.0
                   WHEN 'paraphrase_match' THEN 0.85
                   WHEN 'token_match' THEN 0.75
                   WHEN 'target_page_dead' THEN 0.5
                   WHEN 'no_text_match' THEN 0.0
                   WHEN 'cookie_wall_detected' THEN 0.0
                   WHEN 'unsupported_javascript_required' THEN 0.4
                   WHEN 'language_mismatch' THEN 0.0
                   ELSE coalesce(path.zq.verification_score, 0.0) END)
          ) / size(paths) END AS trust_score

SET p.source_urls = unique_urls,
    p.source_count = size(unique_urls),
    p.source_quality_summary = {
      n_verbatim: n_verbatim, n_paraphrase: n_para, n_no_match: n_nomatch,
      n_dead: n_v_dead, n_unchecked: n_v_unchecked
    },
    p.source_freshness_summary = {
      n_reachable: n_reach, n_reachable_via_3xx: n_reach_3xx,
      n_dead: n_dead, n_unchecked: n_unchecked_url,
      n_wayback_fallback: n_wayback,
      latest_check_date: toString(latest_check)
    },
    p.source_trust_score = trust_score,
    p.source_urls_updated_at = date(),
    p.migration_origin = coalesce(p.migration_origin, '') + ' | mig_s5_visibility';

// ==========================================================================
// S5.B — :Bauwerk surfacing (similar; inherits from Projekt via :HAS_BAUWERK)
// ==========================================================================
// (analogous block — omitted for brevity; runner authors based on Projekt template)

// ==========================================================================
// S5.C — :Akteur surfacing
// ==========================================================================
// (analogous block)

// ==========================================================================
// S5.D — :DataIssue for nodes with > 50 URLs (per QD-?)
// ==========================================================================
MATCH (n) WHERE n.source_count > 50
MERGE (i:DataIssue {id: 'di_excessive_sources__' + n.id})
ON CREATE SET
  i.kind = 'excessive_sources_on_node',
  i.severity = 'low',
  i.ref_label = labels(n)[0],
  i.ref_id = n.id,
  i.found_at = date(),
  i.found_by = 's5_visibility',
  i.status = 'open',
  i.resolution_note = 'Node has ' + toString(n.source_count) +
                      ' source URLs. Consider whether all are warranted.'
MERGE (i)-[:CONCERNS]->(n);
```

---

## §6 Acceptance gates

| Gate | Cypher | Expected |
|---|---|---|
| Every `:Projekt` has `source_urls` (may be empty list) | `MATCH (p:Projekt) WHERE p.source_urls IS NULL RETURN count(p)` | 0 |
| Every `:Projekt` has `source_quality_summary` | `MATCH (p:Projekt) WHERE p.source_quality_summary IS NULL RETURN count(p)` | 0 |
| Every `:Projekt` has `source_freshness_summary` | as above | 0 |
| Spot-check Stuttgart 210 | `MATCH (p:Projekt {id:'p_stuttgart_210'}) RETURN p.source_count, p.source_trust_score, p.source_quality_summary` | source_count ≥ 5; trust_score ≥ 0.4 (likely ≥ 0.7 if S3 worked) |
| Spot-check Holbein Gardens | as above | source_count ≥ 7 |
| `:Bauwerk` with `source_urls` | `MATCH (b:Bauwerk) WHERE b.source_urls IS NOT NULL RETURN count(b)` | ≥ 100 (of 186 — those reachable from a Projekt) |
| `:Akteur` with `source_urls` | `MATCH (a:Akteur) WHERE a.source_urls IS NOT NULL RETURN count(a)` | ≥ 300 |
| Tier-1 projects with `source_trust_score ≥ 0.7` | `MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'}) WHERE p.source_trust_score >= 0.7 RETURN count(p)` | ≥ 5 (informational; honest signal) |
| Projects with `> 50` URLs (DataIssue) | `MATCH (i:DataIssue {kind:'excessive_sources_on_node'}) RETURN count(i)` | ≤ 5 (usually 0) |

---

## §7 Rollback

```cypher
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_s5_visibility'
REMOVE n.source_urls, n.source_count,
       n.source_quality_summary, n.source_freshness_summary,
       n.source_trust_score, n.source_urls_updated_at;

MATCH (i:DataIssue) WHERE i.found_by = 's5_visibility' DETACH DELETE i;
```

---

## §8 Risks

| Risk | Mitigation |
|---|---|
| The aggregation Cypher is heavy on a 5,500-node graph | Add indexes on `Projekt.id`, `ExternalLink.url`. The whole pass should complete in < 60 s. |
| A Projekt has hundreds of citation paths (e.g. very-cited research programme) | The reduce-loop scales linearly. Cap output URLs at 100 for browser sanity (`source_urls` truncated, full list still queryable via traversal). |
| The trust score for a Projekt with 1 verbatim + 1 no_match → average 0.5, may misrepresent | Acceptable; the summary map shows the components honestly. |
| `latest_check_date` returns NULL when no URL probed | Fall back to "—" string. Future S2 reruns populate it. |
| Re-running S5 stamps `migration_origin` repeatedly | The coalesce pattern appends ` | mig_s5_visibility` each run — accept, OR dedupe with `apoc.text.regreplace`. |

---

## §9 Handoff

When S5 completes:

1. Write `agent_s5_visibility/PHASE_S5_DONE.flag`.
2. HANDOFF_LOG row: avg source_trust_score across Projekt, count of trust=NULL projects (no sources), top-10 by trust, bottom-10 by trust.
3. S6 reads everything you wrote.

---

## §10 What the user sees post-S5 (the deliverable)

In Neo4j Browser, clicking `p_stuttgart_210`:

```
source_urls:              [https://www.stuttgart210.de/, …]   (7 items)
source_count:             7
source_quality_summary:   {n_verbatim: 4, n_paraphrase: 2, n_no_match: 1, n_dead: 0, n_unchecked: 0}
source_freshness_summary: {n_reachable: 7, n_dead: 0, n_unchecked: 0, latest_check_date: '2026-05-21'}
source_trust_score:       0.86
source_urls_updated_at:   2026-05-21
```

That's the whole point of this remediation. **Visible. Honest. One click.**

---

**End of AGENT_S5_visibility.md.**
