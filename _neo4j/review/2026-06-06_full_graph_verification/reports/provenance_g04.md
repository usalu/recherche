# Git Provenance — Agent G4 (UNVERIFIABLE rows)

**Generated:** 2026-06-06T18:34:31Z  
**Ledger:** [`ledger/provenance_g04.csv`](../ledger/provenance_g04.csv)  
**Input:** `VERIFICATION_LEDGER_ELEMENT.csv` — **102** `UNVERIFIABLE` rows

## Executive summary

Almost all UNVERIFIABLE rows (**89/102**) are **sourced `:Akteur` nodes** that Agent 06b
deferred under a **volume cap** (`DEFERRED: not re-fetched`). Their `source_urls` were **not**
written by Agent 06b or Agent 08 — they were denormalized earlier by **Q4 `mig_q4_surface_urls`**
(2026-05-21) from `BELEGT_IN → :Quelle/ExternalLink` URLs originating in the **2026-05-15 actor
registry** import of `_archive/research/person/akteursliste_master.md`.

**Agent 08** accounts for **9** UNVERIFIABLE rows: unsourced-actor triage of **miscast** entities
(private clients, aggregate ReCreate clusters, generic volunteer groups). None of the four residual
actors appear in Agent 08's scope because they already carried `source_urls`.

**Agent 10** accounts for **4** UNVERIFIABLE rows (software/program/reallab fetch timeouts).

The **four F3/F4 residual actors** (`anja_rosen`, `annabelle_von_reutern`, `gxn`, `jan_haerens`)
share one systemic pattern: **registry-curated affiliation URLs** (tool/org/project pages) were
surfaced as `source_urls` but fail the **strict person-naming Evidence Gate** on re-fetch.

## Counts

| Shard | UNVERIFIABLE rows |
|---|---:|
| `06b` | 89 |
| `08` | 9 |
| `10` | 4 |

| Root-cause bucket | Count |
|---|---:|
| 06b_volume_cap_deferred | 85 |
| miscast_private_anonymised | 5 |
| f04_strict_gate_residual | 4 |
| fetch_timeout_or_deferred | 2 |
| miscast_aggregate_cluster | 2 |
| miscast_generic_group | 2 |
| software_program_source_weak | 2 |

## Timeline: when `source_urls` were set

| Date | Run / commit | What happened |
|---|---|---|
| 2026-05-15 | `13c165fd` actor_registry_seed | Actors + `q_actor_*` ExternalLink nodes from `akteursliste_master.md`; URLs live on Quelle nodes via `BELEGT_IN`, not yet on `:Akteur`. |
| 2026-05-21 | `d37e5240` Q4 Source Hunting | `mig_q4_surface_urls.cypher` §Q4.C copies `BELEGT_IN → ExternalLink.url` onto `:Akteur.source_urls` (`migration_origin=mig_q4_surface_urls`). |
| 2026-05-23 | `bd62286a` trace_zitiert | URL binding cleanup; broadens/trims `source_urls` on some labels — actor registry URLs largely stable. |
| 2026-06-05 | property cleanup 4b/5b | `source_urls` preserved (404 nodes unchanged per cleanup summary); Quelle nodes later dropped in reuse-bubble cleanup. |
| 2026-06-06 | Agent **06b** | Audited **sourced** actors (218 gap nodes); **89** marked UNVERIFIABLE without re-fetch (volume cap). **`agent06b_add_node_sources`** added URLs to **42** previously-unsourced actors only — **not** the four residuals. |
| 2026-06-06 | Agent **08** | Scoped to **477 unsourced** actors (`source_urls IS NULL`). Residual four **excluded** (already sourced). Nine miscast unsourced actors → UNVERIFIABLE. |
| 2026-06-06 | Agent **15** patch | `agent15_add_node_sources` — **17** Agent-08-PROVEN hubs; separate from 06b patch. |
| 2026-06-06 | F3/F4 | Re-adjudicated 18+8+1 Scope-B items; four actors remain UNVERIFIABLE under strict graph-URL gate. |

## 06b vs Agent 08 — import boundary

| Path | Scope | Effect on `source_urls` | UNVERIFIABLE in G4 |
|---|---|---|---:|
| **06b verification** | `:Akteur` in 06b gap set with existing `source_urls` | Read-only audit; deferred fetch → UNVERIFIABLE | **89** |
| **06b patch** (`agent06b_add_node_sources`) | 42 actors **without** URLs that 06b proved live | `set_node_properties` writes `primary_source_url` + `source_urls` | **0** (patch targets were unsourced) |
| **08 triage** (`ledger/agent_08.csv`) | 477 actors **without** `source_urls` | Proposals only (`ADD_SOURCE` / `ESCALATE_HUMAN`); no graph write in 08 | **9** (miscast only) |
| **15 patch** (`agent15_add_node_sources`) | 17 Agent-08-PROVEN hubs | Graph write for high-confidence unsourced hubs | **0** |

**Key distinction:** 06b and 08 are **complementary shards** — 06b audited actors that *already had*
registry-derived URLs; 08 hunted actors that *lacked* URLs. The four residuals sit entirely in the
06b/F4 path, not the 08 unsourced tail.

## Four residual actors (deep trace)

### `anja_rosen`

- **Graph `source_urls`:** `https://urban-mining-index.de`
- **Origin chain:** akteursliste_master.md → actor_registry (actor_registry_061_070) → BELEGT_IN q_actor_* → mig_q4_surface_urls (2026-05-21) → graph source_urls
- **06b patch:** false · **08 unsourced scope:** false
- **Detail:** Registry chunk `actor_registry_061_070`; `q_actor_anja_rosen_01` → `https://urban-mining-index.de/`. Akteursliste cites UMI **tool** page, not a person bio. Q4 copied URL to `source_urls`. 06b deferred; F4 fetch: homepage names UMI methodology only — **no 'Anja Rosen' string**.

### `annabelle_von_reutern`

- **Graph `source_urls`:** `https://www.tomas-architecture.com|https://concular.de`
- **Origin chain:** akteursliste_master.md → actor_registry (actor_registry_091_100) → BELEGT_IN q_actor_* → mig_q4_surface_urls (2026-05-21) → graph source_urls
- **06b patch:** false · **08 unsourced scope:** false
- **Detail:** Registry chunk `actor_registry_091_100`; URLs from `q_actor_annabelle_von_reutern_01/02` (TOMAS + Concular org homepages). F4: `concular.de` loads but **does not name** actor; `tomas-architecture.com` timeout. Affiliation URLs ≠ person attestation.

### `gxn`

- **Graph `source_urls`:** `https://gxn.3xn.com/wp-content/uploads/sites/4/2019/02/CircleHouse_ENG_2018.pdf`
- **Origin chain:** akteursliste_master.md → actor_registry (actor_registry_101_110) → BELEGT_IN q_actor_* → mig_q4_surface_urls (2026-05-21) → graph source_urls
- **06b patch:** false · **08 unsourced scope:** false
- **Detail:** Registry chunk `actor_registry_101_110`; stub org node (`source_scope=actor_registry_context`). URL inherited via `r_gxn__BELEGT_IN__q_actor_kasper_guldager_jensen_01` (Circle House PDF from Kasper Guldager Jensen row). Q4 surfaced PDF URL on `gxn`. F4: PDF fetch timeout; gxn.3xn.com cookie wall — no verbatim quote under strict gate.

### `jan_haerens`

- **Graph `source_urls`:** `https://rotordb.org/en/projects/zinneke-feder-masui4ever|https://www.vai.be/en/buildings/cultuurinfrastructuur/zinneke|https://vb.nweurope.eu/projects/project-search/fcrbe-facilitating-the-circulation-of-reclaimed-building-elements-in-northwestern-europe/news/on-site-visit-the-zinneke`
- **Origin chain:** akteursliste_master.md → actor_registry (actor_registry_031_040) → BELEGT_IN q_actor_* → mig_q4_surface_urls (2026-05-21) → graph source_urls
- **06b patch:** false · **08 unsourced scope:** false
- **Detail:** Registry chunk `actor_registry_031_040`; three `q_actor_jan_haerens_*` Zinneke/project URLs. F4: `rotordb.org` Zinneke page credits **Renaud Haerlingen**, not Jan Haerens; `vai.be` / FCRBE news omit Jan. Off-graph attestation exists but is **not on graph `source_urls`**.

## Systemic root cause

1. **Q4 denormalization without person-level validation** — `mig_q4_surface_urls` treats any
   `BELEGT_IN → ExternalLink` as authoritative for `:Akteur`, including org/tool/project pages
   from a curated markdown table.
2. **06b volume cap** — sourced actors were classified UNVERIFIABLE without HTTP re-proof,
   blocking automatic upgrade even when URLs are first-party for the *affiliation*, not the *person*.
3. **Evidence Gate mismatch** — registry stars/links encode **reuse relevance**, not biographical
   proof; F3/F4 strict gate correctly refuses PROVEN but leaves rows permanently UNVERIFIABLE
   until graph URLs are replaced with person-naming sources.

## Recommendations

1. **Residual four:** add person-naming URLs to graph (`source_urls`) before re-running F3 — e.g.
   bibliographic sources for Rosen, TOMAS team page for von Reutern, gxn.3xn.com about page for GXN,
   ouest.be / Brussels Architecture Prize for Haerens — then re-fetch.
2. **Bulk 06b deferred (85 actors):** batch spot-fetch pass; many are org-homepage URLs that may
   PROVEN for organisations but stay UNVERIFIABLE for *person* nodes — split person vs org gate.
3. **Agent 08 miscast (9):** do not ADD_SOURCE; remodel as project parts or drop private stubs.
4. **Provenance guard:** new intakes should set `primary_source_url` only from URLs that name the
   entity; keep affiliation URLs on `VERBUNDEN_MIT_AKTEUR` edges with `evidence_url`.

---

*Builder:* `_build_provenance_g04.py` · rows: **102**
