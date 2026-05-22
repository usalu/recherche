# Agent S2 URL Probe Report

- Completed at UTC: `2026-05-22T07:02:16+00:00`
- ExternalLink nodes covered: `2640`
- Distinct URLs covered: `1030`
- Probe log lines: `1432` (append-only; includes interrupted/resumed probe attempts)
- Body cache size: `122683283` bytes (`117.0 MB`)
- Body cache files: `1659`
- Cache evicted files: `0`
- Proactive Wayback archive enabled: `false`
- Wayback fallbacks found on dead URLs: `148`

## Acceptance Gates

- Unchecked ExternalLinks: `0`
- Reachable 2xx ExternalLinks: `1955` (`74.1%` of ExternalLink nodes)
- Dead URLs with Wayback snapshot: `148`
- Reachable HTML without cache: `0`
- Missing expected S2 DataIssue: `0`
- Stale S2 DataIssue after cleanup: `0`

## Final URL Status Distribution

- `reachable_2xx`: 1955
- `dead_4xx`: 336
- `dns_failure`: 231
- `blocked_by_robots`: 79
- `timeout`: 11
- `dead_5xx`: 10
- `tls_failure`: 10
- `reachable_3xx_to_4xx`: 8

## S2 DataIssues

- `url_unreachable_4xx`: 336
- `url_dns_failure`: 231
- `url_blocked_by_robots`: 79
- `url_timeout`: 11
- `url_unreachable_5xx`: 10
- `url_tls_failure`: 10

## Top Problematic Hosts

- `www.construction21.org`: 21 (`dead_4xx`: 21)
- `www.sciencedirect.com`: 20 (`dead_4xx`: 11, `blocked_by_robots`: 9)
- `www.baunetzwissen.de`: 17 (`dead_4xx`: 17)
- `www.researchgate.net`: 17 (`dead_4xx`: 14, `blocked_by_robots`: 3)
- `www.bellastock.com`: 14 (`dead_4xx`: 9, `blocked_by_robots`: 5)
- `vb.nweurope.eu`: 12 (`blocked_by_robots`: 12)
- `www.agwa.be`: 12 (`dead_4xx`: 12)
- `bouldercolorado.gov`: 10 (`dead_4xx`: 10)
- `swiss-architects.com`: 10 (`dead_4xx`: 10)
- `discovery.ucl.ac.uk`: 9 (`dead_4xx`: 6, `blocked_by_robots`: 3)

## Notes

The run was interrupted and resumed. Two probe runners briefly overlapped; writes were idempotent on `:ExternalLink`, and stale/mismatched S2 `:DataIssue` nodes were cleaned after the final pass. The JSONL remains append-only for forensics, so it contains more lines than distinct URLs.
