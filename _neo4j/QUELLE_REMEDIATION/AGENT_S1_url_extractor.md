# Agent S1 — URL extractor

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.**

You are agent S1 of 6. Your job: **discover every URL that appears anywhere in the graph or its source documents, and create a first-class `:Quelle :ExternalLink` node for each unique URL.**

You do NOT verify URLs (S2 does that). You do NOT check content (S3 does that). You DISCOVER.

---

## §1 Cold-start context

- `mit-bestand`: 4,151 nodes / 25,377 relationships at start.
- `:Quelle` nodes (~1,570) currently include some URL-bearing ones (`quelltyp='external_link'` ≈ 264, `quelltyp='external_link_from_actor_registry'` ≈ 314, both with `.url` property already).
- `:Dossier :Quelle` nodes (the 100 dossier markdown files) carry `text_content` with the full dossier markdown including `[label](url)` references and bare URLs.
- ~12 `:ResearchDocument :Quelle` nodes carry similar research markdown with URLs.
- Some edges carry URLs in their `evidence_excerpt` properties (rare; capture them anyway).
- Some non-`:Quelle` nodes may carry URLs in properties (e.g., `Akteur.website`, `Projekt.project_url`); these are FU-9 candidates.

Your job is to consolidate all of these into a single deduplicated `:Quelle :ExternalLink` population.

---

## §2 Mission, in five concrete tasks

1. **Scan dossier text_content** — for every `:Quelle` with `quelltyp IN ['case_markdown','research_markdown']` AND `text_content IS NOT NULL`: parse markdown links `[label](url)` and bare URLs. Emit one `:ExternalLink` per unique normalised URL.
2. **Audit existing URL-bearing Quelle** — for every `:Quelle` with non-null `.url`: normalise the URL; if it doesn't match an `:ExternalLink` already, ensure the node is labelled `:ExternalLink` and stamp `url_origin='pre_existing_quelle'`.
3. **Scan edge `evidence_excerpt`** — for every edge with `evidence_excerpt` containing `http://` or `https://`: extract the URLs; emit `:ExternalLink` and link via `:ZITIERT_QUELLE` from the source endpoint or relevant ancestor.
4. **Scan node properties** — for every node with any property whose name suggests a URL (`url`, `website`, `link`, `homepage`, `project_url`, `source_url`, etc.), capture the URL.
5. **Connect** — every new `:ExternalLink` must be reachable from at least one `:Dossier`, `:ResearchDocument`, `:Akteur`, `:Projekt`, or other discovery context via `:ZITIERT_QUELLE` (or, for node-property URLs, a new edge `:HAS_SOURCE_LINK`).

---

## §3 Schema delta (only what S1 introduces)

### §3.1 New / amended properties on `:Quelle :ExternalLink`

```
url                             // normalised URL (S1.normalise — see §6)
title                           // [label] from markdown, or '' for bare
quelltyp                        // 'external_link'  (kept for back-compat)
url_origin                      // 'dossier_md_link' | 'dossier_bare_url'
                                // | 'pre_existing_quelle' | 'edge_property' | 'node_property'
first_seen_in_dossier           // dossier id (NULL for non-dossier origins)
also_in_dossier                 // list<dossier_id> (for URLs cited by multiple dossiers)
also_in_node                    // list<node_id>    (for URLs found in node properties)
also_in_edge                    // list<edge_internal_id>  (for URLs found in edge excerpts)
extracted_at                    // date
migration_origin                // 'mig_s1_url_extract'
```

### §3.2 New / amended properties on `:ZITIERT_QUELLE`

```
locator                         // 'S1' | 'S7' | 'P1' | 'bare' | 'edge_excerpt' | 'node_prop:<name>'
evidence_excerpt                // ~120 chars surrounding the URL
evidence_source_id              // dossier id, or '<node_label>:<id>' for non-dossier sources
evidence_origin                 // 'source_curated'  (the URL is explicitly cited in source)
evidence_basis                  // 'markdown_link_extraction' | 'bare_url_extraction'
                                // | 'edge_excerpt_extraction' | 'node_property_extraction'
evidence_confidence             // 'belegt'
migration_origin                // 'mig_s1_url_extract'
```

### §3.3 New edge type (for node-property URLs)

When the URL came from a non-Quelle node's property (e.g., `Akteur.website`):

```
(node)-[:HAS_SOURCE_LINK {
  property_name,                // 'website' | 'project_url' | …
  evidence_origin: 'source_curated',
  evidence_basis: 'node_property_extraction',
  migration_origin: 'mig_s1_url_extract'
}]->(:ExternalLink)
```

---

## §4 Conflict avoidance

You write:
- New `:Quelle :ExternalLink` nodes (idempotent MERGE on URL hash).
- New `:ZITIERT_QUELLE` edges (idempotent MERGE).
- New `:HAS_SOURCE_LINK` edges (idempotent MERGE).
- The `also_in_*` arrays on `:ExternalLink`.

You MUST NOT:
- Touch `url_status`, `url_http_code`, redirect-chain — those are S2's.
- Touch `verification_status` — that's S3's.
- Touch secondary labels `:Dossier`, `:ResearchDocument`, `:SectionRef` — those are S4's (you can READ `quelltyp` though).
- Touch `:Dossier.text_content` (you READ it; S4 strips it).
- Touch `source_urls` on Projekt/Bauwerk/Akteur — that's S5's.

---

## §5 Pre-flight

```bash
# 1. Verify Stage 4 baseline
ls _neo4j/FINAL_REVIEW_PLAN_AUDIT.md

# 2. Check expected starting counts
# MATCH (q:Quelle {quelltyp:'case_markdown'}) WHERE q.text_content IS NOT NULL
#   RETURN count(q);   -- expect 95
# MATCH (q:Quelle {quelltyp:'external_link'}) RETURN count(q);   -- expect ~264
# MATCH (q:Quelle {quelltyp:'external_link_from_actor_registry'}) RETURN count(q);   -- expect ~314

# 3. Branch
git switch -c agent_s1/url-extract

# 4. Connect creds
python -c "from _scripts.neo4j_env import resolve_connection; print(resolve_connection())"
```

---

## §6 URL normalisation (canonical algorithm)

Every URL extracted goes through this pipeline before MERGE:

```python
def normalise_url(raw: str) -> str:
    parsed = urlparse(raw.strip())
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    # Drop default ports
    if (scheme == "https" and netloc.endswith(":443")) or (scheme == "http" and netloc.endswith(":80")):
        netloc = netloc.rsplit(":", 1)[0]
    path = parsed.path.rstrip("/") or "/"
    # Strip tracking params
    query_pairs = [
        (k, v) for k, v in parse_qsl(parsed.query)
        if k.lower() not in UTM_PARAMS    # utm_*, fbclid, gclid, mc_cid, mc_eid, _ga
    ]
    query = urlencode(sorted(query_pairs))    # alphabetise for stable hashing
    return urlunparse((scheme, netloc, path, parsed.params, query, ""))    # drop fragment
```

Hash: `md5(normalised_url).hexdigest()` → used as `:ExternalLink.id` suffix.

---

## §7 Cypher (parameterised template)

Migration file: [migrations/mig_s1_url_extract.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_s1_url_extractor/migrations/mig_s1_url_extract.cypher).

```cypher
// S1.A — MERGE :ExternalLink
MERGE (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
ON CREATE SET
  ext.url = $url,
  ext.title = $title,
  ext.quelltyp = 'external_link',
  ext.url_origin = $url_origin,
  ext.first_seen_in_dossier = $source_id,
  ext.extracted_at = date(),
  ext.evidence_origin = 'source_curated',
  ext.evidence_basis = $evidence_basis,
  ext.evidence_confidence = 'belegt',
  ext.evidence_source_id = $source_id,
  ext.migration_origin = 'mig_s1_url_extract'
ON MATCH SET
  ext.also_in_dossier = apoc.coll.toSet(
    coalesce(ext.also_in_dossier, []) +
    CASE WHEN $url_origin IN ['dossier_md_link','dossier_bare_url']
         THEN [$source_id] ELSE [] END
  ),
  ext.also_in_node = apoc.coll.toSet(
    coalesce(ext.also_in_node, []) +
    CASE WHEN $url_origin = 'node_property' THEN [$source_id] ELSE [] END
  ),
  ext.also_in_edge = apoc.coll.toSet(
    coalesce(ext.also_in_edge, []) +
    CASE WHEN $url_origin = 'edge_property' THEN [$source_id] ELSE [] END
  );

// S1.B — Link to source (dossier or research document)
// Used when source is a :Quelle (case_markdown or research_markdown)
MATCH (source:Quelle {id: $source_id})
MATCH (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
MERGE (source)-[z:ZITIERT_QUELLE]->(ext)
ON CREATE SET
  z.locator = $locator,
  z.evidence_origin = 'source_curated',
  z.evidence_basis = $evidence_basis,
  z.evidence_source_id = $source_id,
  z.evidence_confidence = 'belegt',
  z.evidence_excerpt = $surrounding_text,
  z.migration_origin = 'mig_s1_url_extract';

// S1.C — Link from non-Quelle node via :HAS_SOURCE_LINK
// Used when URL was found in a property of a Projekt / Akteur / etc.
MATCH (source) WHERE source.id = $source_id AND NOT source:Quelle
MATCH (ext:Quelle:ExternalLink {id: 'q_url_' + $url_hash})
MERGE (source)-[h:HAS_SOURCE_LINK]->(ext)
ON CREATE SET
  h.property_name = $property_name,
  h.evidence_origin = 'source_curated',
  h.evidence_basis = 'node_property_extraction',
  h.evidence_source_id = source.id,
  h.evidence_confidence = 'belegt',
  h.migration_origin = 'mig_s1_url_extract';
```

---

## §8 Runner skeleton (`logs/agent_s1_runner.py`)

```python
def run_s1():
    # Stage 1: scan :Dossier and :ResearchDocument text_content (markdown links + bare URLs)
    candidates = session.run(
        "MATCH (q:Quelle) WHERE q.quelltyp IN ['case_markdown','research_markdown'] "
        "  AND q.text_content IS NOT NULL "
        "RETURN q.id, q.text_content, q.quelltyp"
    )
    for cand in candidates:
        records = extract_md_links(cand) + extract_bare_urls(cand)
        for rec in records:
            session.run(S1_A, **rec)
            session.run(S1_B, **rec)

    # Stage 2: scan existing :Quelle with .url already set
    existing = session.run(
        "MATCH (q:Quelle) WHERE q.url IS NOT NULL AND q.url <> '' "
        "RETURN q.id, q.url, q.name AS title, q.quelltyp"
    )
    for q in existing:
        norm = normalise_url(q['url'])
        # MERGE :ExternalLink secondary label + url_origin='pre_existing_quelle'
        session.run(S1_A_for_existing, url=norm, url_hash=md5(norm), ...)

    # Stage 3: scan edges with URL-bearing evidence_excerpt
    edge_urls = session.run(
        "MATCH ()-[r]->() WHERE r.evidence_excerpt =~ '.*https?://.*' "
        "RETURN id(r) AS rid, type(r) AS rtype, r.evidence_excerpt AS excerpt"
    )
    for e in edge_urls:
        for url in extract_urls_from(e['excerpt']):
            # MERGE :ExternalLink + record in ext.also_in_edge
            ...

    # Stage 4: scan node properties (Akteur.website, Projekt.project_url, etc.)
    url_property_names = ['url', 'website', 'link', 'homepage',
                          'project_url', 'source_url', 'official_url']
    for prop in url_property_names:
        nodes = session.run(
            f"MATCH (n) WHERE n.{prop} IS NOT NULL AND n.{prop} =~ '^https?://.*' "
            f"RETURN n.id AS nid, labels(n) AS lbls, n.{prop} AS url"
        )
        for n in nodes:
            norm = normalise_url(n['url'])
            session.run(S1_A_for_node_prop, ...)
            session.run(S1_C, source_id=n['nid'], property_name=prop, ...)

    # Audits
    ...
```

---

## §9 Acceptance gates

| Gate | Cypher | Expected |
|---|---|---|
| Every `:ExternalLink` has non-null `.url` | `MATCH (e:ExternalLink) WHERE e.url IS NULL RETURN count(e)` | 0 |
| Every new `:ExternalLink` has `url_origin` | `MATCH (e:ExternalLink) WHERE e.migration_origin CONTAINS 'mig_s1' AND e.url_origin IS NULL RETURN count(e)` | 0 |
| Every `:ExternalLink` created by S1 has at least one incoming citation edge | `MATCH (e:ExternalLink) WHERE e.migration_origin CONTAINS 'mig_s1' AND NOT exists{(:Quelle\|()-[:ZITIERT_QUELLE\|HAS_SOURCE_LINK]->(e)} RETURN count(e)` | 0 |
| Distinct URLs after dedup | `MATCH (e:ExternalLink) RETURN count(DISTINCT e.url)` | ≥ 500 (estimate; varies) |
| Stuttgart 210 has ≥ 7 URLs | `MATCH (:Dossier {id:'q_stuttgart_210_md'})-[:ZITIERT_QUELLE]->(e:ExternalLink) RETURN count(DISTINCT e)` | ≥ 7 |
| No URL contains `utm_` (normalisation working) | `MATCH (e:ExternalLink) WHERE e.url CONTAINS 'utm_' RETURN count(e)` | 0 |
| No URL ends with `/` (trailing slash normalised) | `MATCH (e:ExternalLink) WHERE e.url ENDS WITH '/' AND size(e.url) > 12 RETURN count(e)` | 0 |
| URL origins distribution | `MATCH (e:ExternalLink) RETURN e.url_origin, count(e)` | non-empty in 3+ of 5 categories |

---

## §10 Rollback

```cypher
// Drop S1-created edges first
MATCH ()-[r:ZITIERT_QUELLE]->() WHERE r.migration_origin = 'mig_s1_url_extract' DELETE r;
MATCH ()-[r:HAS_SOURCE_LINK]->() WHERE r.migration_origin = 'mig_s1_url_extract' DELETE r;

// Drop S1-created nodes (ExternalLink that don't pre-date S1)
MATCH (e:ExternalLink) WHERE e.migration_origin = 'mig_s1_url_extract' DETACH DELETE e;

// Strip the also_in_* arrays from pre-existing :ExternalLink
MATCH (e:ExternalLink) WHERE e.url_origin = 'pre_existing_quelle'
REMOVE e.also_in_dossier, e.also_in_node, e.also_in_edge;
```

---

## §11 Handoff

When S1 completes:

1. Write `agent_s1_url_extractor/PHASE_S1_DONE.flag`.
2. Push branch + open PR.
3. Append row to [HANDOFF_LOG.md](HANDOFF_LOG.md) with key metrics: URLs extracted by origin, total `:ExternalLink` count, top-10 dossiers by URL count.
4. Notify in PR body: "**S2 may now run** (URL probe phase)."

S2 reads:
- `:ExternalLink` set (it probes every one).
- `url_origin` (informational; S2 doesn't filter on it).

---

## §12 Open questions (record in your report)

- Some `evidence_excerpt` strings contain truncated URLs (`https://www.example.com/page/very/long...`). Decision: skip if URL has trailing `…` or `...` or `[truncated]`. Document the skip count.
- For node-property URLs, do we keep the `:HAS_SOURCE_LINK` edge type OR fold into `:ZITIERT_QUELLE`? Recommend: separate type for semantic clarity ("this is a node property, not a dossier citation").
- 5 dossiers without `text_content` are skipped silently; S4 owns resolving them.

---

**End of AGENT_S1_url_extractor.md.**
