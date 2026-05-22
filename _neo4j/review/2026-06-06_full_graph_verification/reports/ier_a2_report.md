# IER-A2 — Tier A URL-backed relationship evidence recovery

**Date:** 2026-06-06 · **Agent:** `IER-A2`
**Database:** `mit-bestand` (read-only) · **Scope target:** 162
**Ledger:** [`ledger/ier_a2.csv`](../ledger/ier_a2.csv)

## Scope

Non-PROVEN tier-A relationships with HTTP `basis_ref` (excl. IER-A1 actors, IER-B1 dossier BETEILIGT_AN):

| Cluster | rel_types | rows |
|---|---|---:|
| Catalogue | HAT_BAUTEILTYP / NUTZT_MATERIAL | 13 |
| Regulation | TRIGGERS_REGULIERUNGSFRAGE / ERFORDERT_NACHWEIS | 53 |
| VMA | VERBUNDEN_MIT_AKTEUR (URL present) | 20 |
| Schadstoff | HAT_SCHADSTOFFRISIKO / ERFORDERT_SCHADSTOFFPRUEFUNG | 30 |
| Other URL-backed | BETEILIGT_AN, NUTZT_SOFTWARE, BETRIEBEN_VON, … | 46 |
| **Total** | | **162** |

## Method

1. Enumerate 162 rows from `VERIFICATION_LEDGER_ELEMENT.csv` (tier A, rel, non-PROVEN, disjoint filters).
2. `read-cypher` on live graph for endpoint names and on-edge quotes.
3. `WebFetch` ledger `basis_ref` (or live `evidence_url`/`source_url`); URL cache in `_agent_ier_a2_work/`.
4. **Both-endpoint gate:** verbatim `proof_quote` must be supportable from fetched page naming **both** endpoints (relaxed for schadstoff compendia and regulation decree pages).
5. No graph mutations — proposals only.

**Fetches:** 32 unique URLs cached · 33 distinct basis URLs in scope

## Verdict summary

| verdict | count | share |
|---|---:|---:|
| PARTIAL | 58 | 35.8% |
| PROVEN | 51 | 31.5% |
| UNSUPPORTED | 49 | 30.2% |
| DEAD_LINK | 3 | 1.9% |
| UNVERIFIABLE | 1 | 0.6% |

**Upgrades to PROVEN:** 51 (from prior non-PROVEN)

### By relationship type

| rel_type | PROVEN | PARTIAL | other |
|---|---:|---:|---:|
| `BETEILIGT_AN` | 22 | 14 | 2 |
| `BETRIEBEN_VON` | 1 | 0 | 2 |
| `ERFORDERT_NACHWEIS` | 0 | 6 | 19 |
| `ERFORDERT_SCHADSTOFFPRUEFUNG` | 0 | 0 | 8 |
| `HAT_BAUTEILTYP` | 2 | 10 | 0 |
| `HAT_SCHADSTOFFRISIKO` | 0 | 14 | 8 |
| `NUTZT_MATERIAL` | 0 | 1 | 0 |
| `NUTZT_SOFTWARE` | 3 | 0 | 2 |
| `TRIGGERS_REGULIERUNGSFRAGE` | 3 | 13 | 12 |
| `VERBUNDEN_MIT_AKTEUR` | 20 | 0 | 0 |

### Proposed actions

| action | count |
|---|---:|
| DELETE | 49 |
| RELABEL | 47 |
| KEEP | 34 |
| FIX_PROPERTY | 17 |
| RESOURCE | 15 |

## Notable findings (10 worst / gate failures)

- **IER-A2-0002** `heyne_tillett_steel` → `tool_hts_stockmatcher` (NUTZT_SOFTWARE): **DEAD_LINK** — prior_verdict=PARTIAL; prior_claim=A10-R-028; fetch_error=<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate ve
- **IER-A2-0003** `p_timber_square_london` → `tool_hts_stockmatcher` (NUTZT_SOFTWARE): **DEAD_LINK** — prior_verdict=PARTIAL; prior_claim=A10-R-045; fetch_error=<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate ve
- **IER-A2-0010** `tool_hts_stockmatcher` → `heyne_tillett_steel` (BETRIEBEN_VON): **DEAD_LINK** — prior_verdict=PARTIAL; prior_claim=A10-R-096; fetch_error=<urlopen error [SSL: CERTIFICATE_VERIFY_FAILED] certificate ve
- **IER-A2-0028** `rr_de_ziegel` → `s_bleifarbe` (HAT_SCHADSTOFFRISIKO): **UNSUPPORTED** — schadstoff gate fail; from=no to=no
  - quote: "PAK, Asbest, KMF: Grenzwerte für Schadstoffbelastungen Schriftenreihe Band 1: Asbest in bauchemischen Produkten Band 2: Emissionen aus Bauprodukten Band 3: PCB, Chlorparaffine, Rad…"
- **IER-A2-0029** `p_big_dig_building_boston` → `s_schwermetalle` (ERFORDERT_SCHADSTOFFPRUEFUNG): **UNSUPPORTED** — schadstoff gate fail; from=no to=no
  - quote: "PAK, Asbest, KMF: Grenzwerte für Schadstoffbelastungen Schriftenreihe Band 1: Asbest in bauchemischen Produkten Band 2: Emissionen aus Bauprodukten Band 3: PCB, Chlorparaffine, Rad…"
- **IER-A2-0030** `p_maison_vignette_auderghem` → `s_bleifarbe` (ERFORDERT_SCHADSTOFFPRUEFUNG): **UNSUPPORTED** — schadstoff gate fail; from=no to=no
  - quote: "PAK, Asbest, KMF: Grenzwerte für Schadstoffbelastungen Schriftenreihe Band 1: Asbest in bauchemischen Produkten Band 2: Emissionen aus Bauprodukten Band 3: PCB, Chlorparaffine, Rad…"
- **IER-A2-0038** `p_biopartner_5_leiden_oegstgeest` → `nf_genehmigungs_oder_zustimmungsbedarf` (ERFORDERT_NACHWEIS): **UNSUPPORTED** — regulation gate fail; from=no to=no
  - quote: "The Environment Buildings Decree of the Netherlands (Besluit bouwwerken leefomgeving, Bbl) - Climate Change Laws of the World Skip to content This document Everything Home / Search…"
- **IER-A2-0039** `p_bluecity_offices_rotterdam` → `nf_genehmigungs_oder_zustimmungsbedarf` (ERFORDERT_NACHWEIS): **UNSUPPORTED** — regulation gate fail; from=no to=no
  - quote: "The Environment Buildings Decree of the Netherlands (Besluit bouwwerken leefomgeving, Bbl) - Climate Change Laws of the World Skip to content This document Everything Home / Search…"
- **IER-A2-0040** `p_jeugdkliniek_ithaka_emergis_kloetinge` → `nf_genehmigungs_oder_zustimmungsbedarf` (ERFORDERT_NACHWEIS): **UNSUPPORTED** — regulation gate fail; from=no to=no
  - quote: "The Environment Buildings Decree of the Netherlands (Besluit bouwwerken leefomgeving, Bbl) - Climate Change Laws of the World Skip to content This document Everything Home / Search…"
- **IER-A2-0041** `p_liander_alliander_hq_duiven` → `nf_genehmigungs_oder_zustimmungsbedarf` (ERFORDERT_NACHWEIS): **UNSUPPORTED** — regulation gate fail; from=no to=no
  - quote: "The Environment Buildings Decree of the Netherlands (Besluit bouwwerken leefomgeving, Bbl) - Climate Change Laws of the World Skip to content This document Everything Home / Search…"

## Summary

Processed **162/162** tier-A URL-backed relationships. **51** upgraded to PROVEN under both-endpoint gate. **58** remain PARTIAL (single-endpoint or weak catalogue/regulation tie). **52** UNSUPPORTED/DEAD_LINK routed to DELETE/RESOURCE.
