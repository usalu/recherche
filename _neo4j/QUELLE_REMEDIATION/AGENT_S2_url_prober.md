# Agent S2 — URL prober (chase every link)

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.**

You are agent S2 of 6. Your job: **for every `:ExternalLink.url` in the graph, find out if it's actually reachable, where it redirects, and what it serves.** You also cache the body so S3 can verify content without re-fetching.

This is the **chase** layer. S3 is the **double-check** layer that depends on you.

---

## §1 Cold-start context

After S1, the graph has every URL that any agent ever mentioned, deduplicated and normalised. Most of them are German/EU government, university, or industry sites — generally polite hosts but some rate-limit aggressively. Some URLs are 10+ years old (papers, PDF reports) and may be dead.

Your job: probe each one (HTTP request), record what comes back, cache the body, and on dead links, ask the Wayback Machine.

You do NOT make value judgements about the content. S3 does that.

---

## §2 Mission

1. **Probe every `:ExternalLink`** — for each URL with `url_status IS NULL OR url_status = 'unchecked' OR url_last_checked_at < (today - 30 days)`.
2. **Capture the full picture** — status code, redirect chain, final URL, content-type, body size, `Last-Modified` header.
3. **Cache the body** under `shared/url_bodies/` for S3 to consume (skip if > 5 MB; skip if content-type not text/* or application/pdf).
4. **Fallback to Wayback** for dead URLs (4xx, 5xx, DNS failures). If Wayback has a snapshot, store the snapshot URL and timestamp.
5. **Be a good citizen** — rate-limit per host, respect robots.txt, identify in User-Agent, honour 429 backoff.
6. **Emit `:DataIssue`** for dead URLs so S6 can surface them in the audit.

---

## §3 Schema delta (what S2 writes on `:ExternalLink`)

```
url_status                  // enum:
                            //   'reachable_2xx'           - 200/204/...
                            //   'reachable_3xx_to_4xx'    - redirected and target was 4xx
                            //   'dead_4xx'                - 4xx final
                            //   'dead_5xx'                - 5xx final
                            //   'timeout'                 - request timeout
                            //   'dns_failure'             - DNS resolution failed
                            //   'tls_failure'             - SSL/TLS handshake failed
                            //   'unsupported_scheme'      - mailto:, ftp:, etc.
                            //   'blocked_by_robots'       - robots.txt disallow (QD-2)
                            //   'unchecked'               - default, before probe
url_http_code               // int (or NULL on network failure)
url_final_url               // string (after redirect chain; may equal url)
url_redirect_chain          // list<string> (intermediates between url and final_url)
url_content_type            // 'text/html' | 'application/pdf' | …
url_content_length_bytes    // int (from Content-Length header or measured body length)
url_last_modified_header    // string (raw header value)
url_server_header           // string
url_response_headers        // map (full headers dump, useful for forensics)
url_last_checked_at         // date
url_probe_attempts          // int (incremented on retry)
url_probe_duration_ms       // int (single-probe duration)
url_user_agent              // string (UA used)

// Wayback fallback (only if primary URL is dead and we asked archive.org)
url_wayback_snapshot        // string (archive.org URL of the closest snapshot)
url_wayback_timestamp       // string ('20221015143200' style)
url_wayback_attempted       // bool

// Body cache
url_body_cache_path         // string (relative path under shared/url_bodies/)
url_body_cache_format       // 'html' | 'pdf' | 'binary' | 'too_large_skipped' | 'wrong_type_skipped'
url_body_md5                // string

migration_origin            // 'mig_s2_url_probe'
```

---

## §4 Conflict avoidance

You write: only `url_*` properties on `:ExternalLink`. You also write `:DataIssue` for dead URLs.

You DO NOT touch:
- `verification_status` (S3 only)
- `source_*` on Projekt/Bauwerk/Akteur (S5)
- secondary labels (S4)
- existing citation edges' properties

You READ:
- `:ExternalLink.url` (the only thing you probe)

---

## §5 Pre-flight

```bash
# 1. S1 done flag
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s1_url_extractor/PHASE_S1_DONE.flag

# 2. Expected target count
# MATCH (e:ExternalLink) RETURN count(e);   -- expect ~600–1,500 after S1

# 3. Body cache directory
mkdir -p _neo4j/intake/runs/2026-05-21_quelle_remediation/shared/url_bodies

# 4. Branch
git switch -c agent_s2/url-probe

# 5. Required Python libraries
# pip install httpx tenacity beautifulsoup4 (for the runner)
# Confirm:
python -c "import httpx, tenacity, bs4; print('ok')"
```

---

## §6 HTTP probe protocol (the careful version)

For each `:ExternalLink` to probe:

### §6.1 Pre-checks

1. **Scheme check.** If scheme not in `{'http', 'https'}` → set `url_status='unsupported_scheme'`, write `:DataIssue {kind:'url_unsupported_scheme'}`, skip.
2. **robots.txt check.** Per QD-2: fetch `https://<host>/robots.txt` (cached per-host for the run). If `Disallow` applies to the path for our User-Agent → set `url_status='blocked_by_robots'`, skip body fetch.

### §6.2 Probe (HEAD then GET fallback)

```python
USER_AGENT = (
    "mit-bestand-source-prober/1.0 (research-graph; "
    "contact: kinan.sarak@gmail.com)"          # per QD-8
)

@retry(stop=stop_after_attempt(3),
       wait=wait_exponential(min=1, max=10),
       retry=retry_if_exception_type((httpx.TimeoutException, httpx.ConnectError)))
def probe(url):
    with httpx.Client(
        follow_redirects=False,                # we follow manually to capture chain
        timeout=httpx.Timeout(connect=10.0, read=20.0),
        headers={'User-Agent': USER_AGENT, 'Accept': 'text/html,application/pdf,*/*;q=0.8'},
    ) as client:
        redirect_chain = []
        current = url
        for hop in range(6):                   # max 5 redirects + 1 final
            try:
                resp = client.head(current)
            except Exception:
                resp = client.get(current)     # some servers reject HEAD
            if 300 <= resp.status_code < 400 and 'location' in resp.headers:
                redirect_chain.append(current)
                current = httpx.URL(resp.headers['location'], base=current)
                continue
            break
        return {'final_url': str(current), 'redirect_chain': redirect_chain,
                'status_code': resp.status_code, 'headers': dict(resp.headers)}
```

### §6.3 Body fetch (only if 2xx and content-type allowed)

If `status_code` in 200..299 AND `content-type` in `{'text/html', 'text/plain', 'application/pdf', 'application/xhtml+xml'}`:

```python
resp = client.get(final_url, headers={'User-Agent': USER_AGENT})
content_length = len(resp.content)
if content_length > 5 * 1024 * 1024:           # QD-11
    return {'cache': 'too_large_skipped'}
ext = 'pdf' if 'pdf' in content_type else 'html'
body_md5 = md5(resp.content).hexdigest()
cache_path = f"shared/url_bodies/{url_hash}.{ext}"
if content_length > 100 * 1024:                # gzip files > 100 KB
    Path(cache_path + '.gz').write_bytes(gzip.compress(resp.content))
    cache_path += '.gz'
else:
    Path(cache_path).write_bytes(resp.content)
```

### §6.4 Wayback fallback for dead URLs (per QD-1, QD-5)

If `status_code` ≥ 400 OR network error:

```python
wayback = httpx.get(
    "https://archive.org/wayback/available",
    params={'url': original_url}
)
data = wayback.json()
snap = data.get('archived_snapshots', {}).get('closest')
if snap and snap.get('available'):
    return {'wayback_url': snap['url'], 'wayback_timestamp': snap['timestamp']}
```

Per QD-1, also proactively submit the **live** URL to Wayback to preserve it:

```python
httpx.get(f"https://web.archive.org/save/{quote(original_url)}",
          timeout=30.0)                        # fire and forget
```

Rate-limit Wayback to 3 req/min/host.

### §6.5 Rate-limiting (per QD-10)

- Maximum 1 req/sec/host (sliding window).
- Maximum 30 req/min globally.
- On HTTP 429 or 503-with-Retry-After: honour the header, double the wait on each retry.
- Total wall-clock budget for a full S2 run: 60 min for ~1,000 URLs.

---

## §7 Cypher (parameterised)

Migration file: [migrations/mig_s2_url_probe.cypher](../intake/runs/2026-05-21_quelle_remediation/agent_s2_url_prober/migrations/mig_s2_url_probe.cypher).

```cypher
// S2.A — write probe results to :ExternalLink
MATCH (ext:ExternalLink {id: $external_link_id})
SET ext.url_status             = $url_status,
    ext.url_http_code          = $url_http_code,
    ext.url_final_url          = $url_final_url,
    ext.url_redirect_chain     = $url_redirect_chain,
    ext.url_content_type       = $url_content_type,
    ext.url_content_length_bytes = $url_content_length_bytes,
    ext.url_last_modified_header = $url_last_modified_header,
    ext.url_server_header      = $url_server_header,
    ext.url_response_headers   = $url_response_headers,
    ext.url_last_checked_at    = date(),
    ext.url_probe_attempts     = coalesce(ext.url_probe_attempts, 0) + 1,
    ext.url_probe_duration_ms  = $url_probe_duration_ms,
    ext.url_user_agent         = $url_user_agent,
    ext.url_body_cache_path    = $url_body_cache_path,
    ext.url_body_cache_format  = $url_body_cache_format,
    ext.url_body_md5           = $url_body_md5,
    ext.url_wayback_snapshot   = $url_wayback_snapshot,
    ext.url_wayback_timestamp  = $url_wayback_timestamp,
    ext.url_wayback_attempted  = $url_wayback_attempted,
    ext.migration_origin = coalesce(ext.migration_origin, '') + ' | mig_s2_url_probe';

// S2.B — emit :DataIssue for dead URLs
WITH $url_status AS status, $url AS url, $external_link_id AS eid
WHERE status IN ['dead_4xx','dead_5xx','timeout','dns_failure','tls_failure','blocked_by_robots']
MATCH (ext:ExternalLink {id: eid})
MERGE (i:DataIssue {id: 'di_url_' + status + '__' + eid})
ON CREATE SET
  i.kind = CASE status
    WHEN 'dead_4xx' THEN 'url_unreachable_4xx'
    WHEN 'dead_5xx' THEN 'url_unreachable_5xx'
    WHEN 'timeout' THEN 'url_timeout'
    WHEN 'dns_failure' THEN 'url_dns_failure'
    WHEN 'tls_failure' THEN 'url_tls_failure'
    WHEN 'blocked_by_robots' THEN 'url_blocked_by_robots'
    ELSE 'url_unknown_status' END,
  i.severity = CASE status
    WHEN 'dead_4xx' THEN 'medium'
    WHEN 'dead_5xx' THEN 'medium'
    WHEN 'dns_failure' THEN 'medium'
    ELSE 'low' END,
  i.ref_label = 'ExternalLink',
  i.ref_id = eid,
  i.found_at = date(),
  i.found_by = 's2_url_probe',
  i.status = 'open',
  i.resolution_note = 'URL not reachable (' + status + '). Wayback fallback: ' +
                      coalesce($url_wayback_snapshot, 'unavailable')
MERGE (i)-[:CONCERNS]->(ext);
```

---

## §8 Runner skeleton

```python
def run_s2():
    targets = session.run(
        "MATCH (e:ExternalLink) "
        "WHERE e.url_status IS NULL OR e.url_status = 'unchecked' "
        "  OR (e.url_last_checked_at IS NOT NULL "
        "      AND duration.inDays(date(e.url_last_checked_at), date()).days > 30) "
        "RETURN e.id AS id, e.url AS url"
    )

    rate_limiter = HostRateLimiter(rps=1.0, global_rpm=30)
    robots_cache = {}

    for t in targets:
        if not allowed_by_robots(t['url'], robots_cache):
            session.run(S2_A, url_status='blocked_by_robots',
                        external_link_id=t['id'], ...)
            continue

        rate_limiter.wait(host_of(t['url']))
        result = probe(t['url'])
        body_info = maybe_cache_body(result)
        wayback_info = wayback_fallback_if_dead(result, t['url'])
        proactively_archive_if_alive(t['url'])

        session.run(S2_A, external_link_id=t['id'], **flatten(result, body_info, wayback_info))
        session.run(S2_B, external_link_id=t['id'], url=t['url'], **flatten(result))
        write_jsonl(probe_log, {...})

    session.run(audits)
```

---

## §9 Acceptance gates

| Gate | Cypher | Expected |
|---|---|---|
| Every `:ExternalLink` has `url_status` set (not unchecked) | `MATCH (e:ExternalLink) WHERE e.url_status IS NULL OR e.url_status='unchecked' RETURN count(e)` | 0 |
| Reachable URLs (2xx) count | `MATCH (e:ExternalLink {url_status:'reachable_2xx'}) RETURN count(e)` | ≥ 60 % of total |
| Dead URLs that got a Wayback snapshot | `MATCH (e:ExternalLink) WHERE e.url_status STARTS WITH 'dead_' AND e.url_wayback_snapshot IS NOT NULL RETURN count(e)` | ≥ 0 (informational) |
| Body cache for HTML URLs reachable | `MATCH (e:ExternalLink) WHERE e.url_status='reachable_2xx' AND e.url_content_type STARTS WITH 'text/html' AND e.url_body_cache_path IS NULL RETURN count(e)` | 0 (every reachable html cached) |
| `:DataIssue` count for url_unreachable_* | `MATCH (i:DataIssue) WHERE i.found_by='s2_url_probe' RETURN i.kind, count(i)` | non-empty if any URLs dead |
| Probe log written | `agent_s2_url_prober/logs/url_probe_results.jsonl` exists | yes |
| Body cache directory size | `du -sh shared/url_bodies/` | ≤ 2 GB |

---

## §10 Rollback

```cypher
MATCH (e:ExternalLink)
REMOVE e.url_status, e.url_http_code, e.url_final_url, e.url_redirect_chain,
       e.url_content_type, e.url_content_length_bytes, e.url_last_modified_header,
       e.url_server_header, e.url_response_headers, e.url_last_checked_at,
       e.url_probe_attempts, e.url_probe_duration_ms, e.url_user_agent,
       e.url_body_cache_path, e.url_body_cache_format, e.url_body_md5,
       e.url_wayback_snapshot, e.url_wayback_timestamp, e.url_wayback_attempted;

MATCH (i:DataIssue) WHERE i.found_by = 's2_url_probe' DETACH DELETE i;

// Optionally: rm -rf shared/url_bodies/
```

---

## §11 Risks specific to S2

| Risk | Mitigation |
|---|---|
| Host bans us after rate-limit miss | Per-host sliding window; honour 429; on persistent block tag `url_status='blocked_by_host'` (use `dead_4xx` if 4xx) |
| robots.txt fetched slowly per host | Cache for the run lifetime (in-memory dict) |
| Some hosts return 200 + HTML error page (soft-404) | Tag `url_status='reachable_2xx'` honestly; S3 will detect the content mismatch |
| PDF body parse-out is heavy for S2 | S2 only caches the body bytes; S3 does the parsing |
| Body cache fills disk | Hard cap at 2 GB; eject by LRU; tag affected ExternalLinks with `url_body_cache_format='evicted'` |
| Wayback Machine itself is slow / rate-limited | Use a smaller pool for Wayback (1 rps); on Wayback timeout, skip and continue |
| URL contains credentials (`user:pass@`) | Strip credentials before probing; log a `:DataIssue {kind:'url_with_credentials'}` |

---

## §12 Handoff

When S2 completes:

1. Write `agent_s2_url_prober/PHASE_S2_DONE.flag` with counts.
2. Push branch + open PR.
3. Append row to [HANDOFF_LOG.md](HANDOFF_LOG.md) with key metrics: total probed, `reachable_2xx` count, `dead_*` count, Wayback fallbacks count, body cache size.
4. PR body should include the top-10 problematic hosts (most 4xx/5xx returns).

S3 reads:
- `:ExternalLink.url_status` (skip dead pages; tag `verification_status='target_page_dead'` for their citation edges)
- `:ExternalLink.url_body_cache_path` (the cached body — its primary input)
- `:ExternalLink.url_wayback_snapshot` (optional secondary input if QD-5 YES)

---

## §13 Recommended ordering inside S2

- Process `:ExternalLink` in chunks of 50.
- Within each chunk: probe in parallel (4 workers), each respecting rate limits.
- Persist progress to JSONL after every chunk so a crash doesn't lose work.
- Resume capability: skip any URL whose `url_last_checked_at` is today.

---

**End of AGENT_S2_url_prober.md.**
