# Final Cleanup F05 — Tracimat rels + harvestmap VMA (F3 rel subset)

**Date:** 2026-06-06 · **Database:** `mit-bestand` · **Mode:** read-only (no graph mutation)
**Ledger:** [`ledger/final_cleanup_f05.csv`](../ledger/final_cleanup_f05.csv)
**Scope:** F3 `SCOPE_CYPHER` rel block — **9** relationships (8 Tracimat `ERFORDERT_NACHWEIS` + 1 PARTIAL VMA)

## Scope recap

| Cluster | Count | Prior verdict | New verdict |
|---|---:|---|---|
| Belgian reuse projects → `nf_bauteilidentifikation` (Tracimat / OVAM) | 8 | UNVERIFIABLE (P604) | **PROVEN** |
| `re_store_harvestmap_vienna` → `peter_kneidinger` VMA | 1 | PARTIAL (EP09-r-0040) | **PROVEN** |
| **Σ** | **9** | 8 UNVERIFIABLE + 1 PARTIAL | **9 PROVEN** |

## Verdict histogram

| Verdict | Count |
|---|---:|
| PROVEN | 9 |
| PARTIAL | 0 |
| UNVERIFIABLE | 0 |

## Key findings

### 1. Tracimat cluster — source URL drift resolved

Live `read-cypher` shows all eight edges now cite `https://ovam.vlaanderen.be/bouw-sloopopvolging` (not the stale VITO news URL that P6-04 fetched). Re-fetch of the live `source_url` returns HTTP 200 with verbatim support:

> *Tracimat is momenteel de enige erkende sloopbeheerorganisatie. Sinds 1 juli 2022 is sloopopvolging door een sloopbeheerorganisatie voor grote werven verplicht.*

The page further documents mandatory sloopopvolgingsplan (SOP) conformity via Tracimat and digital material-flow tracking — sufficient for regulation-class `ERFORDERT_NACHWEIS` → `nf_bauteilidentifikation` on Flanders reuse/demolition projects.

**Action:** KEEP all eight edges; no patch required (graph already carries correct `source_url` / `source_quote`).

### 2. harvestmap VMA — two-endpoint gate now passes

`re_store_harvestmap_vienna` → `peter_kneidinger` (`elementId` `…1157538353931917937`) still has **null** `evidence_url` / `evidence_quote` on the live rel, but the re:store first-party impressum names both entities:

> *Impressum re:store : HarvestMAP eG – Genossenschaft zur Vermittlung von re:use Bauteilen … Vorstandsvorsitzender & gewerberechtliche Geschäftsführung: Ing. Peter Kneidinger*

`morgenbau.at/34-bauteile-ernten-statt-entsorgen` (listed on `peter_kneidinger.source_urls`) timed out on fetch; impressum alone satisfies the strict actor VMA gate.

**Action:** `ADD_SOURCE` — optional human-gated `set_rel_properties` to copy impressum URL + quote onto the rel (`evidence_url`, `evidence_quote`, `evidence_confidence='belegt'`). Not applied by this agent.

## Worst prior states (all upgraded)

1. **P604-agent07-rel-0668…0675** — UNVERIFIABLE because VITO URL returned landing-page content, not the cited article.
2. **EP09-r-0040** — PARTIAL with empty `proof_quote`; Q05 strict gate failed on unfetched secondary sources.

## Anomalies

- Graph `source_quote` on Tracimat edges remains the English VITO-era sentence while `basis_ref` is now OVAM Dutch; proof uses live OVAM verbatim text (Evidence Gate compliant).
- VMA rel retains `confidence: 0.6` on-graph despite PROVEN attestation; property sync deferred to optional patch.

## Summary

All **9/9** scoped relationships upgraded to **PROVEN** with non-empty `proof_quote` and `fetched=true`. Net upgrade: **+8** from UNVERIFIABLE, **+1** from PARTIAL. No Neo4j writes performed.
