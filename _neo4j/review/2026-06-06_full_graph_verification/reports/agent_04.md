# Verifier Agent 04 — France reuse cluster

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; only `read-cypher` + `WebFetch` used)
**Ledger:** [`ledger/agent_04.csv`](../ledger/agent_04.csv)

## 1. Scope recap

Authoritative enumeration (Cypher run against the live graph):

- **Relationships:** `MATCH (a)-[r]->(b) WHERE r.review_run='france_reuse_bubble_2026_06_05' RETURN r` → **6 relationships** (all `VERBUNDEN_MIT_AKTEUR`).
- **Nodes:** the 8 French-cluster actors named in the mission — `bellastock, cycle_up, backacia, mineka, opalis, association_reavie, mobius_reemploi, cstb` → **8 `Akteur` nodes**.

Total work-set: **14 claims** (6 rels + 8 nodes). Every item was processed; no sampling.

The 6 France-run edges are exactly:

| from | to | connection_kind | evidence_url |
|---|---|---|---|
| association_reavie | opalis | supplier_listing | opalis.eu/fr/fournisseurs/reavie |
| backacia | opalis | supplier_listing | opalis.eu/fr/fournisseurs/backacia |
| cycle_up | opalis | supplier_listing | opalis.eu/fr/fournisseurs/cycle |
| mineka | opalis | supplier_listing | opalis.eu/fr/fournisseurs/mineka |
| bellastock | cstb | research_programme (REPAR) | experimentationsurbaines.ademe.fr/.../programmes-repar-1-et-2 |
| cstb | mobius_reemploi | spirou_consortium | cstb.fr/.../accompagner-developpement-reemploi |

## 2. Counts by verdict

| Verdict | Rels | Nodes | Total |
|---|---:|---:|---:|
| PROVEN | 6 | 8 | **14** |
| PARTIAL | 0 | 0 | 0 |
| UNSUPPORTED | 0 | 0 | 0 |
| DEAD_LINK | 0 | 0 | 0 |
| UNVERIFIABLE | 0 | 0 | 0 |
| MISSING_EVIDENCE | 0 | 0 | 0 |
| CONTRADICTION | 0 | 0 | 0 |
| SCHEMA_VIOLATION | 0 | 0 | 0 |

**All 14 claims are PROVEN. Proposed action for every item: KEEP.** No remediation required for this shard.

Every external item has `fetched=true` and `http_status=200`. No paywalled URL was the sole basis for any verdict (see §5).

## 3. Special-check results (mission-mandated)

1. **Opalis `supplier_listing` edges must be dealer→Opalis and on Opalis's own page.** ✅ All four (`reavie, backacia, cycle_up, mineka`) point **dealer → opalis**, and each `evidence_url` is Opalis's own curated directory page `opalis.eu/fr/fournisseurs/<x>` that is branded "`<dealer> | Opalis`" and describes that exact dealer. This is one endpoint's (Opalis's) own curated listing of the other — the only permitted form of directory co-listing under §3.1. No reversed-direction or non-Opalis listing edge found.
2. **SPIROU consortium CSTB ↔ Mobius.** ✅ `cstb.fr` (CSTB's own offer page) explicitly names "**le projet de recherche SPIROU … co-financé par l'ADEME, le CSTB et ses partenaires Mobius réemploi**". Both endpoints named on the source. PROVEN.
3. **REPAR Bellastock / CSTB / ADEME.** ✅ Present as `bellastock → cstb`. The ADEME page (also Bellastock's `primary_source_url`) states "**REPAR … piloté par Bellastock en partenariat avec l'ADEME et le CSTB**". Both endpoints named. PROVEN. (ADEME is named in the quote but is not a graph endpoint of this edge — no fabricated ADEME edge in the France run.)

## 4. Worst findings

There are **no** UNSUPPORTED / PARTIAL / DEAD_LINK / CONTRADICTION findings in this shard. The France reuse cluster is the cleanest possible result: every edge is backed by a live page that names both endpoints, and every node resolves to a live official site or authoritative directory entry. This stands in contrast to the cross-bubble fabrications that triggered the campaign — the France-run edges were built from real directory listings and named research consortia, not category inference.

## 5. Anomalies & notes for the Aggregator

- **Paywall in node source list (not blocking):** `bellastock.source_urls` includes `https://www.lemoniteur.fr/article/missionnaires-du-circulaire.2133509` (Le Moniteur, paywalled → would be UNVERIFIABLE if relied upon). The Bellastock node verdict does **not** depend on it; the ADEME `primary_source_url` is sufficient. No action needed, but flag if any other agent cites this Le Moniteur URL as proof.
- **Adjacent edges touching my actors that are owned by other shards (excluded from my ledger to preserve MECE):**
  - `bellastock → opalis` (`programme_maintenance_partner`) and `opalis → rotordc` (`directory_dealer`) and `opalis ↔ Rotor` — `review_run = rotor_dc_reuse_bubble_2026_06_05` → **Agent 02**.
  - `brussels_environment → opalis` (`programme_funder_platform`) — `review_run = cross_bubble_extension_2026_06_06` → **Agent 06**.
  - Person/affiliation edges with no `review_run` and no evidence: `bellastock→hugo_topalov`, `bellastock→sarah_westerfeld` (and `sarah_westerfeld→bellastock`), `frederic_denise→bellastock`, `mobius_reemploi→noe_basch`, `opalis→maarten_gielen` (and `maarten_gielen→opalis`). These carry `evidence_url=null` / `evidence_quote=null`. They are out of my scope (individuals, not the 8 actors' inter-org edges), but I flag them as **MISSING_EVIDENCE candidates** for the owning agent (likely Agent 08). Note `noe_basch` is corroborated as a Mobius founder on mobius-reemploi.fr, and `maarten_gielen` is the known Rotor co-founder — so several of these person edges are plausibly real but currently unsourced on-graph.
- **No SCHEMA_VIOLATION:** all 6 France-run rels carry `evidence_url` + `evidence_quote` + `evidence_confidence='belegt'`; none carries `source_url` as well (no dual-URL violation). All 8 nodes use `source_urls` / `primary_source_url` correctly; no forbidden `BELEGT_IN` / `q_url_*` artifacts seen on these elements.
- **No ESCALATE_HUMAN items.**

## 6. One-paragraph summary

Agent 04 processed all 14 France-cluster claims (6 `france_reuse_bubble_2026_06_05` relationships + 8 actor nodes). **Verdict: 14/14 PROVEN, 0 issues, KEEP all.** Every Opalis `supplier_listing` edge is the correct dealer→Opalis direction and is backed by Opalis's own `/fr/fournisseurs/<x>` directory page; the SPIROU (CSTB↔Mobius) and REPAR (Bellastock↔CSTB) consortium edges are each confirmed by a live source naming both endpoints; all eight actor nodes resolve to live official sites or authoritative directory entries. The single most important finding is the **absence** of fabrication in this shard — the France run is fully evidence-backed — with the only follow-up being a handful of **out-of-scope, unsourced person/affiliation edges** touching these actors that the relevant agent (08) should review, and one paywalled Le Moniteur URL on the Bellastock node that must never be treated as proof.
