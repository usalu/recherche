# IER-A1 — Tier A actors with URL (internet evidence recovery)

**Date:** 2026-06-06 · **Agent:** IER-A1
**Database:** `mit-bestand` (read-only) · **Review run:** `ier_a1_2026_06_06`
**Ledger:** [`ledger/ier_a1.csv`](../ledger/ier_a1.csv)
**Patch (dry-run):** [`patches/ier_a1_fix_node_sources.patch.jsonl`](../patches/ier_a1_fix_node_sources.patch.jsonl)

## Scope

Non-PROVEN `:Akteur` nodes where `basis_ref` starts with `http` OR `basis_type ∈ {web,candidate}`;
tier-D rows (`UNVERIFIABLE`, `SCHEMA_VIOLATION`, `CONTRADICTION`) excluded per §3 disjointness.

| Metric | Value |
|---|---:|
| Scope rows | **165** |
| Processed | **165** |
| Unique URLs | 155 |
| Cache entries (this run) | 258 |

## Method

1. Load shard from `VERIFICATION_LEDGER_ELEMENT.csv` (165 tier-A actors).
2. `read-cypher` for live `name`, `source_urls`, `primary_source_url`.
3. `WebFetch` each `basis_ref` (reuse R07 cache; retry once on timeout).
4. **Entity gate:** verbatim `proof_quote` must name organisation/person — not sector tagline only.
5. Homepage alone sufficient for **existence** (IER-A1 special check); VMA edges out of scope.

## Verdict summary

| verdict | count | share |
|---|---:|---:|
| `PROVEN` | 129 | 78.2% |
| `PARTIAL` | 18 | 10.9% |
| `DEAD_LINK` | 13 | 7.9% |
| `UNVERIFIABLE` | 5 | 3.0% |

**Upgraded to PROVEN:** 129 (78.2% of shard)

### Proposed actions

| action | count |
|---|---:|
| `KEEP` | 129 |
| `RESOURCE` | 36 |

**Dry-run patch ops:** 129 `set_node_properties` (not applied).

## Ten weakest findings

| element_id | verdict | http | note |
|---|---|---|---|
| `archipel_zero` | DEAD_LINK | — | fetch failed: <urlopen error [Errno 11001] getaddrinfo failed> |
| `circular_construction_lab` | DEAD_LINK | — | fetch failed: <urlopen error [Errno 11001] getaddrinfo failed> |
| `circular_engineering_for_architecture_eth` | DEAD_LINK | — | fetch failed: <urlopen error [Errno 11001] getaddrinfo failed> |
| `city_of_helsinki` | DEAD_LINK | — | fetch failed: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify |
| `immobilien_basel_stadt` | DEAD_LINK | — | fetch failed: <urlopen error [WinError 10060] A connection attempt failed becaus |
| `london_borough_of_barnet` | DEAD_LINK | — | fetch failed: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify |
| `noaarchitecten` | DEAD_LINK | — | fetch failed: <urlopen error [Errno 11001] getaddrinfo failed> |
| `normandie_amenagement` | DEAD_LINK | — | fetch failed: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify |
| `oxara_ag` | DEAD_LINK | — | fetch failed: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify |
| `philippe_samyn_and_partners` | DEAD_LINK | — | fetch failed: <urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate verify |

## Summary

Processed **165/165** tier-A `:Akteur` rows. **129** upgraded to `PROVEN` via live URL fetch naming the entity; **18** remain `PARTIAL` (page loads but entity not named); **13** `DEAD_LINK`. Graph unchanged (read-only wave).
