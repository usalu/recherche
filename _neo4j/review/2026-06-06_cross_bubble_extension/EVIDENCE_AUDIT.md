# Evidence Audit — reuse-bubble `VERBUNDEN_MIT_AKTEUR` connections

**Date:** 2026-06-06
**Trigger:** Restado appeared connected to Cirkla / Opalis / Insert / useagain with links
that carried no real evidence. Manual source-checking confirmed a systemic defect.
**Method:** fetched every suspect `evidence_url` and checked whether the page actually
names **both** endpoints of the relationship.

---

## Root cause (why the mistakes happened)

During the **cross-bubble extension** (and the country **mesh/ecosystem** edges), connections
were created from **category similarity** — "both are European reuse marketplaces", "both are
Dutch reuse platforms", "both issue resource passports" — and then a URL that describes **only
one** of the two actors (or a shared directory) was attached as if it were proof.

This violates two rules in `AGENTS.md`:
- Rule 3: *name/category similarity is not sufficient grounds for a link.*
- Evidence rule: *`evidence_url` must support the specific claim on that relationship.*

A co-mention in a directory, or a homepage of one partner, is **not** evidence of a pairwise
relationship between two specific actors.

---

## TIER 1 — REMOVED (16 edges, proven unsupported)

Each URL was fetched; in every case the page does **not** name one of the two endpoints.

| from → to | connection_kind | evidence_url | why wrong |
|---|---|---|---|
| cirkla → software_restado | european_reuse_infrastructure_peer | reuse-rlp.de/fachinformationen | page never mentions restado; only lists cirkla.ch + opalis.eu as links |
| opalis → software_restado | european_reuse_infrastructure_peer | ECESP/opalis | page is about Opalis only; restado not mentioned |
| insert_marketplace → software_restado | european_marketplace_peer | madaster.com/…/insert-and-madaster | page is about Insert↔Madaster; restado not mentioned |
| software_restado → useagain_bauteilclick | european_marketplace_peer | library-of-reuse.ch/pioneers/useagain | page is about useagain only; restado not mentioned |
| city_of_utrecht → madaster | municipal_reuse_pilot_mesh | preuse…/utrecht-reuse-centre | page is about the Utrecht depot; Madaster not mentioned (was mislabeled `belegt`) |
| city_of_utrecht → new_horizon_urban_mining | dutch_reuse_policy_mesh | newhorizon.nl | homepage; Utrecht not mentioned |
| insert_marketplace → new_horizon_urban_mining | dutch_reuse_marketplace_mesh | newhorizon.nl | homepage; Insert not mentioned |
| insert_marketplace → repurpose | dutch_reuse_marketplace_mesh | madopt.nl | page is about Madopt/Repurpose; Insert not mentioned |
| insert_marketplace → superuse_studios_2012architecten | dutch_reuse_marketplace_mesh | insert.nl/…/insert-marktplaats | page is about Insert; Superuse not mentioned |
| madaster → new_horizon_urban_mining | dutch_reuse_data_mesh | circonl.nl/…/new-horizon | page is about New Horizon; Madaster not mentioned |
| madaster → repurpose | dutch_reuse_data_mesh | madopt.nl | page is about Madopt; Madaster not mentioned |
| madaster → superuse_studios_2012architecten | dutch_reuse_data_mesh | superuse…/harvest-collect-re-use | page is about Superuse; Madaster not mentioned |
| new_horizon_urban_mining → repurpose | dutch_reuse_marketplace_mesh | repurpose.nl | homepage; New Horizon not mentioned |
| repurpose → superuse_studios_2012architecten | dutch_reuse_marketplace_mesh | superuse…/harvest-collect-re-use | page is about Superuse; Repurpose not mentioned |
| concular → madaster | ecosystem_peer_resource_passport | madaster.de | homepage; Concular not mentioned |
| concular → madaster_epea | resource_passport_ecosystem | madaster.de | homepage; Concular/EPEA link not mentioned |

**Graph:** 15 486 → **15 470** relationships.

---

## What survived and was re-verified as CORRECT

The legitimate backbone is intact (URL names both endpoints, or is the actor's own
directory/imprint):

- **concular → software_restado** (`marketplace_brand_operator`) — restado imprint: "restado ist eine Marke der Concular GmbH". ✅
- **bauteilboerse_hannover → software_restado** (`marketplace_listing`) — real restado profile page. ✅
- **insert_marketplace → madaster** (`formal_partnership`) — the Madaster page is precisely the signed Insert–Madaster partnership. ✅
- **madaster → madaster_epea** (`platform_family`) — Madaster/EPEA article. ✅
- **new_horizon_urban_mining → superuse_studios_2012architecten** (`oogstkaart_lineage`) — Superuse article documenting Oogstkaart sold to New Horizon. ✅
- **brussels_environment → opalis** (`programme_funder_platform`) — Opalis/about: "Rotor by Brussels Environment as part of the Renolution strategy". ✅
- **immobel/whitewood → rotordc** (`project_commissioner`) — Rotor OXY Centre Monnaie project page. ✅
- **eth_zuerich → sumami**, **cirkla → sumami**, **circular_hub_zurich → sumami** — each named on the cited page. ✅
- Opalis **supplier_listing** edges (backacia/cycle_up/mineka/reavie → opalis) — each is that dealer's own Opalis listing. ✅

---

## TIER 2 — VERIFIED (13 edges; every cited URL fetched/searched)

Each `evidence_url` was fetched (or, for the paywalled Le Moniteur article, retrieved via
search). **None of the pages name both endpoints.** All 13 fail the evidence test.

| from → to | connection_kind | verified finding | verdict |
|---|---|---|---|
| cirkla → c33_circular_construction_catalyst | coordination_ecosystem | C33 page describes C33 only; **no Cirkla** | unsupported |
| cirkla → circular_hub_zurich | coordination_ecosystem | Circular Hub page; **no Cirkla** | unsupported |
| cirkla → circular_economy_switzerland | coordination_ecosystem | CES page; **no Cirkla** (grep: 0 hits) | unsupported |
| cirkla → zirkular | ecosystem_practice_triangle | K.118 page; **no Cirkla**. Real link exists only via shared planner Benjamin Poignon (also Cirkla committee) | unsupported by URL — *salvageable via re-source* |
| bauteilboerse_bremen → concular | digital_physical_exchange_layer | ECESP restado page; names **neither** Bremen nor Concular | unsupported |
| bellastock → mobius_reemploi | french_reuse_ecosystem | CSTB page names **Mobius** (SPIROU partner of CSTB) but **not Bellastock** | unsupported (borrowed the legit cstb→mobius source) |
| association_reavie → bellastock | opalis_directory_mesh | RéaVie's Opalis profile page; **no Bellastock** | unsupported (co-listing only) |
| backacia → bellastock | opalis_directory_mesh | Bellastock Opalis-France page would not load (3 timeouts); same co-listing pattern | unverifiable / presumed unsupported |
| bellastock → cycle_up | opalis_directory_mesh | Le Moniteur article profiles **Bellastock alone** (partners: ADEME/CSTB/FCRBE); **no Cycle Up** | unsupported |
| backacia → mineka | opalis_directory_peer | Backacia's Opalis profile; **no Mineka** | unsupported (co-listing only) |
| backacia → cycle_up | opalis_directory_peer | ADEME study (general FCRBE/Opalis directory); no pairwise link | unsupported |
| bellastock → mineka | opalis_directory_peer | Le Moniteur article profiles **Bellastock alone**; **no Mineka** | unsupported |
| cycle_up → mineka | opalis_directory_peer | Cycle Up's Opalis profile; **no Mineka** | unsupported (co-listing only) |

**Note:** the "co-listed in Opalis" facts are real, but they belong on each dealer's
`supplier_listing → opalis` edge (which already exists and is verified), not as invented
pairwise dealer-to-dealer partnerships. `cirkla → zirkular` is the one case with a real
underlying relationship (shared planner Benjamin Poignon), but the cited K.118 URL does not
evidence it — it would need re-sourcing if kept.

---

## Knock-on effect

The presentation decks (`PRESENTATION_REUSE_NETWORKS.md`,
`PRESENTATION_REUSE_SYNTHESIS.md`) cite some now-deleted edges — notably the cross-border
path `useagain → restado → opalis → bellastock → cstb`, which relied on the deleted
restado↔opalis and restado↔useagain edges. Those slides must be re-checked before reuse.
