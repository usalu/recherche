# IER-C1+C2 merged — Never-sourced `:Akteur` recovery report

**Agent:** `IER-C12` · **Generated:** 2026-06-06 23:46 UTC
**Database:** `mit-bestand` (read-only) · **Scope:** 292 rows (IER-C1 174 + IER-C2 118)

## Scope recap

Tier-C `:Akteur` nodes with `verdict=MISSING_EVIDENCE` in canonical ledger, no tier-A URL (`source_urls` / `primary_source_url` null on live graph). Search ladder: official site → imprint/legal → registry (Handelsregister / KBO / etc.) → archive fallback.

## Verdict counts

| Verdict | Count | Share |
|---|---:|---:|
| UNVERIFIABLE | 249 | 85.3% |
| PROVEN | 43 | 14.7% |

## Proposed actions

| Action | Count |
|---|---:|
| RESOURCE | 209 |
| ADD_SOURCE | 43 |
| ESCALATE_HUMAN | 40 |

**PROVEN upgrades:** 43 / 292 (14.7%)

## Ten hardest unresolved (sample)

- `proholz_bw` (proHolz BW): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `verein_re_win` (Verein RE-WIN): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `peabody_trust` (Peabody Trust): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `lcp_circulair` (lcp-circulair): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `donkergroen` (Donkergroen): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `die_kuemmerei` (Die Kümmerei): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `wiener_aufzugmuseum` (Wiener Aufzugmus.): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `koimo_development` (KOIMO Development GmbH): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `die_zusammenarbeiter` (Die Zusammenarbeiter): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found
- `superuse_on_site` (Superuse on Site): **UNVERIFIABLE** — search ladder exhausted; no first-party URL found

## Anomalies

- Persons flagged for ESCALATE_HUMAN: 37
- Search ladder exhausted: 212
- URL cache entries: 4165

## Summary

Processed all **292** never-sourced tier-C actors. **43** upgraded to PROVEN with fetched first-party or registry evidence; remainder mostly UNVERIFIABLE after ladder exhaustion or person-policy ESCALATE.
