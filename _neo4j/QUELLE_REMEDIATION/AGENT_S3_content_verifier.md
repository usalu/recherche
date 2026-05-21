# Agent S3 — content verifier (double-check every citation)

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.**

You are agent S3 of 6 — the most semantically demanding agent. Your job: **for every citation edge in the graph, fetch the page from S2's body cache, and check whether the cited `evidence_excerpt` actually appears in the page.**

You don't ask whether the URL works (S2 already did). You ask: **does the URL's content actually say what we claim it says?**

This is the **double-check** layer.

---

## §1 Cold-start context

After S2, every `:ExternalLink` has `url_status`, redirect info, and (for reachable HTML/PDF URLs) a body cache file under `shared/url_bodies/`.

Citation edges in `mit-bestand`:
- `:ZITIERT_QUELLE` — `:Quelle` → `:Quelle` (dossier → external URL most commonly). 1,470+ of these.
- `:BELEGT_IN` — any node → `:Quelle`. 4,734 of these. Many point at `:Dossier` not directly at `:ExternalLink`.

Each citation edge that should be verified has `evidence_excerpt` (the cell text from the dossier that grounded the claim). Your job: for each such edge, find the underlying URL (1 or 2 hops away), read the cached body, and check if the excerpt matches.

You do NOT verify edges where:
- `evidence_origin IN ['topology_synthesized','inferred','registry_derived']` — these are not "supposed to be" verbatim from a source page; verifying them is meaningless.
- `evidence_excerpt IS NULL OR empty` — nothing to compare against.
- The underlying URL is dead — tag `target_page_dead` and move on.

---

## §2 Mission

1. **Find every verification target** — citation edges whose endpoint chain reaches a reachable `:ExternalLink` and whose `evidence_origin='source_curated'` and whose `evidence_excerpt` is non-empty.
2. **Load the cached body** for the target URL (S2 cached it; fall back to Wayback snapshot if QD-5 YES and primary URL is dead).
3. **Extract visible text** from the body (HTML or PDF).
4. **Match the excerpt** against the page text using three tiers (§4).
5. **Tag the edge** with `verification_status`, `verification_score`, `verification_method`, `verified_at`.
6. **Emit `:DataIssue`** for `no_text_match` cases so S6 surfaces them.

---

## §3 Schema delta (S3 writes on citation edges)

```
verification_status              // enum:
                                 //   'verbatim_match'         exact substring
                                 //   'paraphrase_match'       fuzzy match ≥ threshold
                                 //   'token_match'            token-overlap match
                                 //   'no_text_match'          page reachable, excerpt not found
                                 //   'target_page_dead'       URL was dead per S2
                                 //   'unsupported_content_type'  e.g. JSON, image
                                 //   'unsupported_javascript_required'  detected JS-only page
                                 //   'cookie_wall_detected'   page returns consent wall
                                 //   'language_mismatch'      excerpt and page in different languages
                                 //   'fetch_error'            S2 cache missing or unreadable
                                 //   'skipped_no_excerpt'     excerpt is null/empty
                                 //   'skipped_non_curated'    origin not 'source_curated'
                                 //   'unchecked'              default before S3 ran
verification_score               // float 0.0–1.0 (1.0 for verbatim; lower for fuzzy)
verification_method              // 'exact' | 'fuzzy_85' | 'token_80' | 'skipped' | 'wayback'
verified_at                      // date
verification_attempts            // int (incremented on retry)
verification_notes               // free-text — for 'no_text_match' include short reason
verification_body_md5            // string (the body md5 from S2 at the time of verification —
                                 //         so we can detect "page changed since last check")
```

---

## §4 The three-tier match algorithm

### §4.1 Pre-processing (both excerpt and page text)

```python
def normalise_text(s):
    s = unicodedata.normalize('NFKC', s)
    s = s.lower()
    s = re.sub(r'\s+', ' ', s)                  # collapse whitespace
    s = re.sub(r'[‘’“”]', '"', s)   # smart quotes → "
    s = re.sub(r'[–—]', '-', s)       # en/em dashes → -
    return s.strip()
```

### §4.2 Tier A — exact substring

```python
if normalised_excerpt in normalised_page_text:
    return ('verbatim_match', 1.0, 'exact')
```

### §4.3 Tier B — fuzzy substring (RapidFuzz)

Per QD-3 threshold = 85.

```python
from rapidfuzz import fuzz
score = fuzz.partial_ratio(normalised_excerpt, normalised_page_text) / 100.0
if score >= 0.85:
    return ('paraphrase_match', score, 'fuzzy_85')
```

`partial_ratio` slides the excerpt across the page text and reports the best alignment ratio. Robust to small wording differences.

### §4.4 Tier C — token-set overlap

Per QD-4 threshold = 0.80.

```python
STOPWORDS = de_stopwords | en_stopwords    # ~700 entries total

def significant_tokens(s):
    return {t for t in tokenize(s)
            if len(t) >= 3 and t not in STOPWORDS}

excerpt_tokens = significant_tokens(normalised_excerpt)
page_tokens = significant_tokens(normalised_page_text)
overlap = len(excerpt_tokens & page_tokens) / max(1, len(excerpt_tokens))
if overlap >= 0.80:
    return ('token_match', overlap, 'token_80')
```

### §4.5 Fallback — no match

```python
return ('no_text_match', best_score_seen, 'none')
```

The `verification_notes` should include the `best_score_seen` from Tier B and the `overlap` from Tier C for forensic value.

### §4.6 Language detection (per QD-6)

Before running Tiers A–C, detect language of both excerpt and page text using `langdetect` or similar. If they differ:

```python
return ('language_mismatch', 0.0, 'skipped',
        notes=f'excerpt_lang={ex_lang}; page_lang={pg_lang}')
```

---

## §5 Body parsing

### §5.1 HTML

```python
from bs4 import BeautifulSoup

def extract_visible_text(html_bytes):
    soup = BeautifulSoup(html_bytes, 'lxml')
    # Remove script, style, navigation, footer
    for tag in soup(['script', 'style', 'nav', 'footer', 'header', 'noscript']):
        tag.decompose()
    text = soup.get_text(separator=' ', strip=True)
    return text
```

### §5.2 PDF

```python
import pdfplumber

def extract_pdf_text(pdf_bytes):
    text_parts = []
    with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
        for page in pdf.pages:
            t = page.extract_text()
            if t:
                text_parts.append(t)
    return '\n'.join(text_parts)
```

### §5.3 Detect cookie / consent wall (per QD-12)

```python
COOKIE_WALL_MARKERS = [
    'akzeptieren', 'cookie-einstellungen', 'consent management',
    'we use cookies', 'akzeptieren sie cookies', 'datenschutzhinweise'
]

def is_cookie_wall(text, body_length):
    text_lower = text.lower()
    marker_hits = sum(1 for m in COOKIE_WALL_MARKERS if m in text_lower)
    return body_length < 5000 and marker_hits >= 2
```

If detected → `verification_status='cookie_wall_detected'`.

### §5.4 Detect JS-rendered page

```python
def is_js_only(html_bytes, extracted_text):
    if b'window.__NEXT_DATA__' in html_bytes or b'id="__nuxt"' in html_bytes:
        if len(extracted_text) < 500:
            return True
    return False
```

If detected → `verification_status='unsupported_javascript_required'`.

---

## §6 Cypher (parameterised)

Migration file: [migrations/mig_s3_content_verify.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_s3_content_verifier/migrations/mig_s3_content_verify.cypher).

```cypher
// S3.A — write verification results to citation edge
MATCH ()-[r]->() WHERE id(r) = $edge_internal_id
SET r.verification_status   = $verification_status,
    r.verification_score    = $verification_score,
    r.verification_method   = $verification_method,
    r.verified_at           = date(),
    r.verification_attempts = coalesce(r.verification_attempts, 0) + 1,
    r.verification_notes    = $verification_notes,
    r.verification_body_md5 = $verification_body_md5,
    r.migration_origin      = coalesce(r.migration_origin, '') + ' | mig_s3_content_verify';

// S3.B — emit :DataIssue for no_text_match
WITH $verification_status AS status, $edge_internal_id AS eid, $excerpt AS excerpt
WHERE status IN ['no_text_match','target_page_dead','unsupported_content_type',
                 'unsupported_javascript_required','cookie_wall_detected','language_mismatch']
MATCH ()-[r]->() WHERE id(r) = eid
WITH r, status, excerpt
MERGE (i:DataIssue {id: 'di_citation_' + status + '__' + toString(eid)})
ON CREATE SET
  i.kind = CASE status
    WHEN 'no_text_match' THEN 'citation_no_text_match'
    WHEN 'target_page_dead' THEN 'citation_target_page_dead'
    WHEN 'unsupported_content_type' THEN 'citation_unsupported_content_type'
    WHEN 'unsupported_javascript_required' THEN 'citation_unsupported_js'
    WHEN 'cookie_wall_detected' THEN 'citation_cookie_wall'
    WHEN 'language_mismatch' THEN 'citation_language_mismatch'
    ELSE 'citation_unknown_issue' END,
  i.severity = CASE status
    WHEN 'no_text_match' THEN 'high'
    WHEN 'cookie_wall_detected' THEN 'medium'
    ELSE 'medium' END,
  i.ref_label = type(r),
  i.ref_id = toString(id(r)),
  i.rel_type = type(r),
  i.found_at = date(),
  i.found_by = 's3_content_verify',
  i.status = 'open',
  i.resolution_note = 'Excerpt (first 100 chars): ' +
                      substring(coalesce(excerpt,''), 0, 100)
WITH r, i, startNode(r) AS src
MERGE (i)-[:CONCERNS]->(src);
```

---

## §7 Runner outline

```python
def run_s3():
    # Find all edges to verify
    targets = session.run("""
        MATCH (src)-[r]->(target)
        WHERE r.evidence_origin = 'source_curated'
          AND r.evidence_excerpt IS NOT NULL
          AND r.evidence_excerpt <> ''
          AND (r.verification_status IS NULL OR r.verification_status = 'unchecked')
        OPTIONAL MATCH (target)-[:ZITIERT_QUELLE]->(ext1:ExternalLink)
        WITH src, r, target,
             CASE
               WHEN target:ExternalLink THEN target
               WHEN ext1 IS NOT NULL THEN ext1
               ELSE NULL END AS url_node
        RETURN id(r) AS edge_id, type(r) AS edge_type,
               r.evidence_excerpt AS excerpt,
               url_node.id AS ext_id,
               url_node.url AS url,
               url_node.url_status AS url_status,
               url_node.url_body_cache_path AS cache_path,
               url_node.url_content_type AS content_type,
               url_node.url_wayback_snapshot AS wayback_url
    """)

    for t in targets:
        if t['url_status'] is None or t['url_status'].startswith('dead_'):
            # Citation points at a dead URL — tag and continue
            session.run(S3_A, edge_internal_id=t['edge_id'],
                        verification_status='target_page_dead',
                        verification_score=0.0,
                        verification_method='skipped',
                        verification_notes=f"url_status={t['url_status']}",
                        ...)
            continue

        if not t['cache_path']:
            session.run(S3_A, edge_internal_id=t['edge_id'],
                        verification_status='fetch_error',
                        ...)
            continue

        body = read_cached_body(t['cache_path'])
        if 'pdf' in (t['content_type'] or ''):
            page_text = extract_pdf_text(body)
        elif 'html' in (t['content_type'] or ''):
            page_text = extract_visible_text(body)
        else:
            session.run(S3_A, edge_internal_id=t['edge_id'],
                        verification_status='unsupported_content_type',
                        ...)
            continue

        # Cookie wall / JS-only detection
        if is_cookie_wall(page_text, len(body)):
            session.run(S3_A, edge_internal_id=t['edge_id'],
                        verification_status='cookie_wall_detected',
                        verification_score=0.0,
                        verification_method='skipped', ...)
            continue
        if is_js_only(body, page_text):
            session.run(S3_A, edge_internal_id=t['edge_id'],
                        verification_status='unsupported_javascript_required', ...)
            continue

        # Language check
        ex_lang = detect_language(t['excerpt'])
        pg_lang = detect_language(page_text[:5000])
        if ex_lang and pg_lang and ex_lang != pg_lang:
            session.run(S3_A, edge_internal_id=t['edge_id'],
                        verification_status='language_mismatch',
                        verification_notes=f'excerpt_lang={ex_lang}; page_lang={pg_lang}',
                        ...)
            continue

        # Three-tier match
        status, score, method, notes = three_tier_match(t['excerpt'], page_text)

        session.run(S3_A, edge_internal_id=t['edge_id'],
                    verification_status=status,
                    verification_score=score,
                    verification_method=method,
                    verification_notes=notes,
                    verification_body_md5=md5_of(body), ...)
        session.run(S3_B, edge_internal_id=t['edge_id'], excerpt=t['excerpt'],
                    verification_status=status)
        write_jsonl(verification_log, {...})

    session.run(audits)
```

---

## §8 Acceptance gates

| Gate | Cypher | Expected |
|---|---|---|
| Every source_curated citation edge has `verification_status` | `MATCH ()-[r]->() WHERE r.evidence_origin='source_curated' AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> '' AND (r.verification_status IS NULL OR r.verification_status='unchecked') RETURN count(r)` | 0 |
| Verification status distribution | `MATCH ()-[r]->() WHERE r.verification_method IS NOT NULL RETURN r.verification_status, count(r)` | populated; verbatim+paraphrase+token expected to be ≥ 50 % of attempted |
| `verification_score` ∈ [0, 1] | `MATCH ()-[r]->() WHERE r.verification_score IS NOT NULL AND (r.verification_score < 0 OR r.verification_score > 1) RETURN count(r)` | 0 |
| `:DataIssue` for no_text_match populated | `MATCH (i:DataIssue {kind:'citation_no_text_match'}) RETURN count(i)` | ≥ 0 (will likely be > 0; that's the honest signal) |
| No verification body_md5 mismatch with S2 | `MATCH (e:ExternalLink)<-[:ZITIERT_QUELLE]-(:Dossier)-[bel:BELEGT_IN]-() WHERE bel.verification_body_md5 IS NOT NULL AND bel.verification_body_md5 <> e.url_body_md5 RETURN count(bel)` | 0 (or page changed mid-run; investigate) |
| Stuttgart 210 — at least one verbatim_match | `MATCH (:Projekt {id:'p_stuttgart_210'})-[bel:BELEGT_IN]->(d:Dossier)-[z:ZITIERT_QUELLE]->(e:ExternalLink) WHERE z.verification_status='verbatim_match' RETURN count(z)` | ≥ 1 |

---

## §9 Rollback

```cypher
MATCH ()-[r]->()
WHERE r.migration_origin CONTAINS 'mig_s3_content_verify'
REMOVE r.verification_status, r.verification_score, r.verification_method,
       r.verified_at, r.verification_attempts, r.verification_notes,
       r.verification_body_md5;

MATCH (i:DataIssue) WHERE i.found_by = 's3_content_verify' DETACH DELETE i;
```

---

## §10 Risks specific to S3

| Risk | Mitigation |
|---|---|
| HTML body parsing strips important content (e.g., text inside `<noscript>`) | Re-test with a known good page; tune the BeautifulSoup selector. |
| PDF extraction returns garbage on scanned PDFs | Detect "few words, high page count" → tag `unsupported_pdf_scanned`. |
| Fuzzy threshold 85 is too lenient → false positives | Per-edge `verification_score` exposed; user can re-filter at query time. |
| Verbatim match found in nav/footer chrome (not main content) | BeautifulSoup pre-processing removes nav/footer; double-check with manual inspection on a sample. |
| Same page has the excerpt buried in a quote from a different source — false positive | Acceptable for now; treat as `paraphrase_match` (lower score). Real fix: extract `<main>` only. |
| Page is paywalled → returns short summary | Likely caught as `cookie_wall_detected` or `no_text_match`. Document. |
| German excerpts with umlauts vs page using ae/oe/ue normalisation | The normalise_text() collapses Unicode NFKC; both should compare equal. |

---

## §11 Handoff

When S3 completes:

1. Write `agent_s3_content_verifier/PHASE_S3_DONE.flag` with verification distribution.
2. Push branch + open PR.
3. Append HANDOFF_LOG row: verbatim count, paraphrase count, no_match count, dead_page count, skip counts.
4. PR body should highlight the top-10 projects with the most `no_text_match` citations — these are the most-in-question facts in the graph.

S5 reads:
- `verification_status` on every citation edge (folds into `source_quality_summary`).
- `verification_score` (folds into `source_trust_score`).

---

## §12 Tunables to expose for re-runs

Edges marked `no_text_match` could be re-tried after parameter tweaks. The runner should support:

- `--threshold-fuzzy 80` (override QD-3 default 85)
- `--threshold-token 0.7` (override QD-4 default 0.8)
- `--retry-only no_text_match` (re-verify only edges that failed previously)
- `--re-verify-since 30` (re-verify edges last checked > 30 days ago)

This makes the verification round iterative — the user can ease thresholds, re-run, and see which edges flip from `no_text_match` to `token_match`.

---

**End of AGENT_S3_content_verifier.md.**
