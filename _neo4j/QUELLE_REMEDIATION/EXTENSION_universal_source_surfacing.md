# Universal source surfacing — every node, its URL

**Status:** ✅ Complete · **Phase ID:** Q-EXT · **Completed:** 2026-05-22
**Date:** 2026-05-22
**Parent plan:** [QUELLE_REMEDIATION_PLAN.md](../QUELLE_REMEDIATION_PLAN.md) — supersedes S5's narrow scope

> **What this is.** A focused follow-up to S1–S6. Instead of only Projekt/Bauwerk/Akteur carrying `source_urls`, **every domain node** does — Material, Bauteilgruppe, Norm, Schadstoff, Aufbereitungsverfahren, etc. Plus a single-string `primary_source_url` for immediate visibility.

> **What this is NOT.** Not another 6-agent split. One agent (orchestrator), three small Cypher migrations, one runner. Total effort: ~30 minutes.

---

## §1 What the user actually wants

Click any node in Neo4j Browser. See:

```
:Material {id: 'mat_stahl', name: 'Stahl'}
  source_urls:             [8 URLs — broad candidate set; see §3 Q-EXT.B]
  source_count:            8
  confirmed_source_urls:   [2 URLs that actually back this node — see §3 Q-EXT.C v2]
  confirmed_source_count:  2
  confirmation_evidence:   { url_1: ['dossier_grounded:q_resource_rows_copenhagen_md:S3'],
                             url_2: ['content_verified:fuzzy_85:0.87'] }
  primary_source_url:      <first confirmed URL, or NULL>
```

Two arrays: `source_urls` is the broad set (everything reachable through citation chains). `confirmed_source_urls` is the **strict perfect-match set** — only URLs that pass either the dossier-grounding or the content-verification test. Multiple confirmed URLs per node is expected and fine.

No traversal. No dossier indirection. The URLs are right there on the node. The user knows exactly which ones to trust.

For research-folder URLs (the 13 files in `_neo4j/intake/inbox/research/` plus 3k+ files in `_archive/research/`): they cite real standards / papers / regulations, and those URLs must be captured too — not just left in the markdown text. Q-EXT.A scans those folders directly from disk.

---

## §2 Where we are now (post-S6)

| Node label | source_urls? |
|---|:---:|
| `:Projekt` | ✅ (S5) |
| `:Bauwerk` | ✅ (S5) |
| `:Akteur` | ✅ (S5) |
| `:Material` | ❌ |
| `:Bauteilgruppe` | ❌ |
| `:Norm` | ❌ |
| `:Schadstoff` | ❌ |
| `:Aufbereitungsverfahren` | ❌ |
| `:Verbindungstechnik` | ❌ |
| `:PruefungNachweis` | ❌ |
| `:Leistungsanforderung` | ❌ |
| `:ReuseRule` | ❌ |
| `:Programm` | ❌ |
| `:Software` / `:Tool` | ❌ |
| `:Huerde` | ❌ |
| `:Wiederverwendungskette` | ❌ |
| `:Materialdepot` | ❌ |
| `:RechtlicheBedingung` | ❌ |
| `:Zertifizierungssystem` | ❌ |
| `:LCAModule` | ❌ |
| `:Bauteiltyp` | ❌ |
| `:Ressourcenquelle` | ❌ |
| `:Bauproduktstatus` | ❌ |
| ... (28 more domain labels) | ❌ |

Plus: research folder `.md` files have URLs that may not be in `:ExternalLink` yet (S1 only scanned nodes whose `text_content` was populated, which was case_markdown only).

---

## §3 The plan (3 sub-phases, one runner)

### Q-EXT.A — Ingest research folder URLs

Scan the disk for research markdown files:

```
_neo4j/intake/inbox/research/*.md
_archive/research/**/*.md
```

For each file:
1. Match it to an existing `:ResearchDocument :Quelle` (by filename slug → id).
2. If no match, MERGE a new `:Quelle :ResearchDocument`.
3. Extract every Markdown link `[label](url)` and bare `https://…` URL.
4. MERGE `:Quelle :ExternalLink` per unique URL (same normalisation as S1).
5. MERGE `:ZITIERT_QUELLE` edge: ResearchDocument → ExternalLink.

This is "S1 on research folders" — same code, different input.

### Q-EXT.B — Surface source_urls on every domain node

For each **user-facing node label** (denylist below), apply this pattern:

```cypher
MATCH (n:<Label>)
OPTIONAL MATCH path = (n)-[:BELEGT_IN|ZITIERT_QUELLE|HAS_SOURCE_LINK*1..3]->(ext:ExternalLink)
WITH n, collect(DISTINCT ext.url) AS via_chain
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(direct:ExternalLink)
WITH n, via_chain, collect(DISTINCT direct.url) AS direct
WITH n, [u IN (via_chain + direct) WHERE u IS NOT NULL AND u <> ''] AS urls
SET n.source_urls = apoc.coll.toSet(urls),
    n.source_count = size(apoc.coll.toSet(urls)),
    n.source_urls_updated_at = date(),
    n.migration_origin = coalesce(n.migration_origin, '') + ' | mig_qext_b_source_urls';
```

The traversal length `*1..3` covers:
- length 1: `(n)-[:BELEGT_IN]->(:ExternalLink)` direct.
- length 2: `(n)-[:BELEGT_IN]->(:Dossier|:ResearchDocument)-[:ZITIERT_QUELLE]->(:ExternalLink)`.
- length 3: rare; covers (n)→Dossier→ZITIERT_QUELLE→ExternalLink chains through intermediate Quelle.

### Q-EXT.C (v2) — Compute `confirmed_source_urls` per node

> **Revised 2026-05-22 r2.** The previous version picked a single `primary_source_url` by reachability + verification rank. Critique from the user: that picks "any reachable URL", not "URLs that actually back up this specific node". Replaced with **`confirmed_source_urls`** — a multi-URL list where each entry is *confirmed* against the node by one of two independent criteria. Multiple URLs per node are fine and expected.

**The three confirmation criteria** (a URL counts as confirmed if ANY holds):

**C1 — Dossier-grounded (direct).** The URL is cited (`:ZITIERT_QUELLE`) by a `:Dossier` or `:ResearchDocument` that has a direct `:BELEGT_IN` (or `:HAS_SOURCE_LINK`) edge from the node. The node is *explicitly* attached to that dossier, and that dossier *explicitly* cites the URL. Strongest signal — fires for "owning" nodes (Projekt, Bauwerk, Bauteilgruppe).

**C2 — Content-verified.** The `:ZITIERT_QUELLE` edge to this URL has `verification_status IN ['verbatim_match','paraphrase_match','token_match']` (i.e., S3 found the cited excerpt on the page). Independent self-check.

**C3 — Excerpt-mention.** The URL is cited in a dossier whose `:ZITIERT_QUELLE.evidence_excerpt` mentions this node's `.name` (case-insensitive, word-boundary, minimum 4-character match — short names like "AT" or "EU" are skipped to avoid false positives). This handles vocab nodes (`:Material`, `:Norm`, `:Schadstoff`, `:Verbindungstechnik`, …) that are mentioned in dossier text but aren't directly `:BELEGT_IN`. Example: `mat_stahl` (name="Stahl") gets confirmed for any URL whose surrounding-text snippet contains the word "Stahl" near where the URL was extracted.

Schema delta on every domain node:

```
confirmed_source_urls          // list<string> — URLs that meet C1, C2, OR C3
confirmed_source_count         // int
confirmation_evidence          // map<url, list<reason>>
                               //   reasons (prefix : suffix):
                               //     'dossier_grounded:<dossier_id>:<locator>'
                               //     'content_verified:<verification_method>:<score>'
                               //     'excerpt_mention:<dossier_id>:<locator>'
primary_source_url             // first entry of confirmed_source_urls (or NULL if empty)
```

A URL with multiple reasons is *more strongly* confirmed than one with a single reason. The evidence map preserves every reason so the user can spot-check.

`primary_source_url` is kept for backward-compat with the CLI (`find_sources.py`), but is now simply `confirmed_source_urls[0]` rather than a reachability heuristic. **NULL when no URL meets either criterion** — that's the honest signal.

```cypher
// Q-EXT.C v2 — compute confirmed_source_urls (multi-URL) per node.
// Multiple confirmed URLs per node are expected and acceptable.

MATCH (n) WHERE n.source_urls IS NOT NULL AND size(n.source_urls) > 0

// C1 — dossier-grounded URLs: node directly cites a dossier that cites the URL.
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(d)
WHERE (d:Dossier OR d:ResearchDocument)
OPTIONAL MATCH (d)-[zq:ZITIERT_QUELLE]->(ext_c1:ExternalLink)
WITH n,
     collect(DISTINCT {
       url: ext_c1.url,
       reason: 'dossier_grounded:' + d.id + ':' + coalesce(zq.locator, 'bare')
     }) AS c1_hits

// C2 — content-verified URLs: any citation edge to ext has S3 match.
OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK*1..3]->(ext_c2:ExternalLink)
OPTIONAL MATCH (:Dossier)-[zq2:ZITIERT_QUELLE]->(ext_c2)
WHERE zq2.verification_status IN ['verbatim_match','paraphrase_match','token_match']
WITH n, c1_hits,
     collect(DISTINCT {
       url: ext_c2.url,
       reason: 'content_verified:' + coalesce(zq2.verification_method, 'unknown') +
               ':' + toString(coalesce(zq2.verification_score, 0))
     }) AS c2_hits

// Merge — group by URL, collect all reasons
WITH n, [h IN (c1_hits + c2_hits) WHERE h.url IS NOT NULL] AS hits
WITH n, apoc.coll.toSet([h IN hits | h.url]) AS confirmed_urls,
     apoc.map.groupBy(hits, 'url') AS grouped
WITH n, confirmed_urls, grouped,
     apoc.map.fromPairs(
       [u IN confirmed_urls | [u, [g IN coalesce(grouped[u], []) | g.reason]]]
     ) AS evidence

SET n.confirmed_source_urls   = confirmed_urls,
    n.confirmed_source_count  = size(confirmed_urls),
    n.confirmation_evidence   = evidence,
    n.primary_source_url      = CASE WHEN size(confirmed_urls) > 0
                                     THEN confirmed_urls[0] ELSE NULL END,
    n.migration_origin        = coalesce(n.migration_origin, '') +
                                ' | mig_qext_c_v2_confirmed_urls';
```

**Important reading:** `source_urls` (Q-EXT.B) is the *broad candidate set* — every URL reachable from the node by graph traversal. `confirmed_source_urls` (Q-EXT.C v2) is the *strict confirmed set* — only URLs that pass at least one of the two criteria. The two coexist; the user picks which to read.

---

## §4 Which labels get this treatment

**Apply to (denylist approach — everything except these):**

```
:Quelle           // it IS a source; doesn't need a source pointer
:Dossier          // ditto
:ExternalLink     // ditto
:ResearchDocument // ditto
:SectionRef       // ditto
:OntologyAnchor   // bookkeeping
:DataIssue        // internal audit
:DeprecatedType   // internal audit
:GraphVersion     // internal
:Land             // too generic (every project is in a country; URL would be confusing)
:Stadt            // ditto
```

**Everything else gets `source_urls` + `primary_source_url`.** This includes the 28+ domain labels listed in §2.

---

## §5 Migration files

### File 1: `mig_qext_a_research_urls.cypher` (parameterised, driver-side)

Pattern matches Q1 / S1 — same MERGE for `:ExternalLink` and `:ZITIERT_QUELLE`, scanning research markdown files on disk.

### File 2: `mig_qext_b_universal_source_urls.cypher`

Single statement, loops over all non-denylisted labels:

```cypher
// Driver loops $labels = ['Material', 'Bauteilgruppe', 'Norm', …]
UNWIND $labels AS lbl
CALL apoc.cypher.run(
  'MATCH (n:`' + lbl + '`) ' +
  'OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(direct:ExternalLink) ' +
  'WITH n, collect(DISTINCT direct.url) AS direct_urls ' +
  'OPTIONAL MATCH (n)-[:BELEGT_IN|HAS_SOURCE_LINK]->(d)-[:ZITIERT_QUELLE]->(ext:ExternalLink) ' +
  'WITH n, direct_urls, collect(DISTINCT ext.url) AS chain_urls ' +
  'WITH n, [u IN (direct_urls + chain_urls) WHERE u IS NOT NULL AND u <> ""] AS all_urls ' +
  'SET n.source_urls = apoc.coll.toSet(all_urls), ' +
  '    n.source_count = size(apoc.coll.toSet(all_urls)), ' +
  '    n.source_urls_updated_at = date(), ' +
  '    n.migration_origin = coalesce(n.migration_origin, "") + " | mig_qext_b_source_urls" ' +
  'RETURN count(n) AS nodes_updated',
  {}
) YIELD value
RETURN lbl, value.nodes_updated;
```

### File 3: `mig_qext_c_primary_source_url.cypher`

The §3 priority logic, run once over every node that has `source_urls`.

---

## §6 Acceptance

### §6.1 Q-EXT.A + Q-EXT.B (broad set — already ran)

| Gate | Cypher | Expected |
|---|---|---|
| Research markdown files all have `:ResearchDocument :Quelle` representation | `MATCH (r:ResearchDocument) RETURN count(r)` | ≥ 201 (post-S4) + any new from disk scan |
| Every non-denylisted domain node has `source_urls` (may be empty) | `MATCH (n:Material) WHERE n.source_urls IS NULL RETURN count(n)` (run per label) | 0 per label |
| Distribution of source_count across all domain labels | informational | shows median, max, label coverage |

### §6.2 Q-EXT.C v2 (confirmed set — new)

| Gate | Cypher | Expected |
|---|---|---|
| Every node with `source_urls` has `confirmed_source_urls` set (may be empty) | `MATCH (n) WHERE n.source_urls IS NOT NULL AND n.confirmed_source_urls IS NULL RETURN count(n)` | 0 |
| `mat_stahl` has confirmed URLs grounded in dossier `q_resource_rows_copenhagen_md` (or similar) | `MATCH (n:Material {id:'mat_stahl'}) RETURN n.confirmed_source_urls, n.confirmation_evidence` | ≥ 1 confirmed URL; evidence references at least one dossier |
| `rr_gb_stahl` has the CEN/TS 1090-201 URL confirmed | `MATCH (n:ReuseRule {id:'rr_gb_stahl'}) RETURN n.confirmed_source_urls` | contains `cen-ts-1090-201-2024` URL |
| `primary_source_url` = head of `confirmed_source_urls` | `MATCH (n) WHERE size(coalesce(n.confirmed_source_urls,[])) > 0 AND n.primary_source_url <> n.confirmed_source_urls[0] RETURN count(n)` | 0 |
| Honest signal: count of nodes where `source_count > 0` BUT `confirmed_source_count = 0` | `MATCH (n) WHERE n.source_count > 0 AND coalesce(n.confirmed_source_count, 0) = 0 RETURN count(n)` | informational — exposes nodes whose URLs are graph-reachable but not specifically dossier-grounded or content-verified |
| Distribution by label | `MATCH (n) UNWIND labels(n) AS lbl RETURN lbl, count(n) AS total, sum(CASE WHEN n.confirmed_source_count > 0 THEN 1 ELSE 0 END) AS with_confirmed ORDER BY with_confirmed DESC` | informational |

---

## §7 What the user sees afterwards

### In Browser

Click `mat_stahl`:

```
:Material
  id:                  mat_stahl
  name:                Stahl
  primary_source_url:  https://standards.iteh.ai/catalog/standards/cen/.../cen-ts-1090-201-2024
  source_urls:         [6 URLs — full list]
  source_count:        6
  source_urls_updated_at: 2026-05-22
```

Click `norm_sci_p440`:

```
:Norm
  id:                  norm_sci_p440
  name:                SCI P440 Reuse of Structural Steel
  primary_source_url:  https://steel-sci.com/publication/.../P440
  source_urls:         [2 URLs]
  source_count:        2
```

Click any `:Schadstoff`, any `:Verbindungstechnik`, etc. — same shape.

### From CLI

The existing `_scripts/find_sources.py` already works on any node id. After Q-EXT, every node id returns a non-empty result.

---

## §8 Risks and edge cases

| Risk | Mitigation |
|---|---|
| Some domain nodes have NO citation path (e.g. controlled-vocab `:Bauteiltyp` not cited anywhere) | `source_urls = []`, `primary_source_url = NULL`. Acceptable — emit `:DataIssue {kind:'node_no_source_url'}` if you want to track. |
| Hot labels (`:Bauteilgruppe` with 369 nodes) get heavy Cypher | Acceptable in one-shot; apoc.cypher.run paginates. |
| URL extracted from research file points to PDF / dead URL | Tagged by S2 already (`url_status`). Same logic applies. |
| Some node's primary_source_url is a dead URL | Acceptable — `source_urls` array shows all candidates; user can pick another. |

---

## §9 Rollback

```cypher
MATCH (n) WHERE n.migration_origin CONTAINS 'mig_qext_b_source_urls'
REMOVE n.source_urls, n.source_count, n.source_urls_updated_at;

MATCH (n) WHERE n.primary_source_url IS NOT NULL
  AND n.migration_origin CONTAINS 'mig_qext_c_primary_source_url'
REMOVE n.primary_source_url;

// Q-EXT.A research URL nodes
MATCH (e:ExternalLink) WHERE e.migration_origin = 'mig_qext_a_research_urls'
DETACH DELETE e;
```

---

## §10 Open decisions (small)

| ID | Question | Default |
|---|---|---|
| QE-1 | Include `:Land` / `:Stadt` in the surfacing? | NO — too generic. |
| QE-2 | Emit a `:DataIssue` for domain nodes with `source_urls = []`? | YES — kind: `node_no_source_url`, severity: low. Becomes the next-ingestion backlog. |
| QE-3 | Compute `source_trust_score` for non-Projekt/Bauwerk/Akteur labels too? | NO for now — adds noise. The S2/S3 verification status is still queryable per URL via the existing chain. |
| QE-4 | When picking `primary_source_url`, should we prefer the URL from the node's OWN dossier over an inherited one? | YES (default in §3 priority list). |

---

## §11 How to run

```bash
# Step 1 — research folders
python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/qext_runner.py research

# Step 2 — universal source_urls
python ... qext_runner.py surface

# Step 3 — primary_source_url
python ... qext_runner.py primary

# Or all in one
python ... qext_runner.py all
```

Each step writes `PHASE_QEXT_<X>_DONE.flag`. Re-runnable idempotently.

---

## §12 What success looks like (one paragraph)

After Q-EXT runs: open Neo4j Browser, click any `:Material`, `:Norm`, `:Bauteilgruppe`, `:Schadstoff`, `:Aufbereitungsverfahren`, `:Verbindungstechnik`, `:ReuseRule`, `:Bauteiltyp`, or any other domain node. See `primary_source_url` immediately in the property panel — a single clickable URL telling the user where this fact came from. See `source_urls` array for the full list. **No traversal. No Quelle nodes. No dossiers in the way.**

---

**End of EXTENSION_universal_source_surfacing.md.**
