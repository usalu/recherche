# Verifier Agent 02 — Belgium / Rotor cluster — Report

**Date:** 2026-06-06
**Database:** `mit-bestand` (READ-ONLY; only `read-cypher` / `get-schema` used)
**Ledger:** [`ledger/agent_02.csv`](../ledger/agent_02.csv) — 49 rows (37 relationships + 12 nodes)

## 1. Scope recap

Authoritative enumeration via `read-cypher`:

- **19** relationships with `r.review_run='rotor_dc_reuse_bubble_2026_06_05'`.
- **3** `cross_bubble_extension_2026_06_06` actor-actor edges touching my actors (`brussels_environment→opalis`, `immobel→rotordc`, `rotordc→whitewood`).
- **15** untagged `VERBUNDEN_MIT_AKTEUR` edges among / adjacent to the core actors (Rotor↔Opalis, Rotor/RotorDC↔staff persons) carrying **no** `evidence_url`.
- **12** `Akteur` nodes: `Rotor`, `rotordc`, `opalis`, `brussels_environment`, `immobel`, `whitewood` + 6 Rotor/RotorDC persons.

**MECE note / overlaps left to their owners (not in my ledger):** the four `*_supplier_listing` edges `reavie|backacia|cycle_up|mineka → opalis` are tagged `france_reuse_bubble_2026_06_05` → **Agent 04**. The endpoint nodes `p_oxy_centre_monnaie`, `p_multi_brussels_reuse_in_multi`, `p_architecture_of_reuse_brussels`, `prog_fcrbe`, `prog_preuse`, `bw_generale_de_banque_brussels` are **Agent 09**'s node scope (their *edges* are verified here). `city_of_utrecht` is NL (**Agent 05**) but its `prog_preuse` edge is `rotor_dc`-tagged → verified here.

## 2. Counts by verdict

| Verdict | Rels | Nodes | Total |
|---|---:|---:|---:|
| PROVEN | 21 | 9 | 30 |
| PARTIAL | 0 | 3 | 3 |
| UNSUPPORTED | 1 | 0 | 1 |
| MISSING_EVIDENCE | 15 | 0 | 15 |
| **Total** | **37** | **12** | **49** |

Proposed actions: `KEEP` 32 · `ADD_SOURCE` 15 · `DELETE` 1 · `RESOURCE` 1.

All web-fetched items returned **HTTP 200**. One cited URL (`rotordb.org/en/about`) is **404** but it is *not* an evidence reference for any edge — only a generic node `source_urls` host whose live pages were otherwise confirmed.

## 3. Special checks (all required by the plan)

- **`colocation_evere`** (`rotordc → Rotor`): **PROVEN**. `rotordb.org/en/projects/rotor-dc-reuse-made-easy` states verbatim *"Rotor's offices are now located literally above RotorDC's stocks of salvaged materials"* and *"in Anderlecht between 2017 and 2022, and in Evere now."*
- **OXY `project_commissioner` (Immobel + Whitewood)**: **PROVEN**. `rotordb.org/en/projects/oxy-centre-monnaie`: *"it was acquired by property developers Whitewood and Immobel."* The OXY news page (`works-oxy-well-underway`) adds *"A collaborative effort with clients Whitewood and Immobel"* and *"reconverted to lighting fixtures by RotorDC"*, which jointly prove the `immobel→rotordc` and `rotordc→whitewood` commissioner/operator edges (both endpoints named on the same project).
- **Opalis funder / maintenance edges vs `opalis.eu/en/about`**: **PROVEN**. The about page proves the Bellastock maintenance partnership (*"Since 2019, the cooperative Bellastock has joined … updated the section on French salvage dealers and keep monitoring this region"*) and the Brussels Environment funding (*"Opalis is maintained and updated by Rotor and Bellastock … Rotor by Brussels Environment as part of the Renolution strategy"*), plus *"The website Opalis was founded by Rotor vzw/asbl."*

## 4. Ten worst findings

1. **`rotordc → p_architecture_of_reuse_brussels` (BETEILIGT_AN) — UNSUPPORTED → DELETE.** The only fabrication in the shard. evidence_url `architecture-reuse-brussels` names **only Rotor** ("involved in three of the featured projects: Zinneke, Multi and Recypark"). There is **no RotorDC**, no "Olivia Noël", and no "BMA launch" anywhere on the page. The asserted quote is invented; RotorDC was attached by category inference — exactly the failure mode under remediation.
2. **`brussels_environment → prog_fcrbe` (BETEILIGT_AN) — PROVEN but mis-sourced → RESOURCE.** The cited `evidence_url` (`opalis.eu/en/about`) does **not** connect Brussels Environment to FCRBE. The claim is nonetheless true: the FCRBE pilot-operations page lists *"Other pilot operations by … Brussels Environment."* Fix the `evidence_url` to `rotordb.org/en/projects/12-fcrbe-pilot-operations`.
3–6. **Bidirectional `VERBUNDEN_MIT_AKTEUR` pairs (no evidence) → flag for Agent 14 dedup + ADD_SOURCE.** `Rotor↔opalis` (rel-0023/0024), `maarten_gielen↔opalis` (rel-0025/0026), `lionel_devlieger↔Rotor` (rel-0028/0032), `maarten_gielen↔Rotor` (rel-0029/0033), `tristan_boniver↔Rotor` (rel-0031/0037) all exist in both directions. The earlier dedup should have collapsed these; they are parallel/bidirectional and carry no `evidence_url`.
7. **`Rotor↔opalis` carries no edge evidence** though the founder fact is on `opalis.eu/en/about` ("founded by Rotor vzw/asbl"). ADD_SOURCE.
8. **Rotor/RotorDC ↔ person edges (11) all lack `evidence_url`.** Affiliations are real for Billiet (OXY/Multi/Careno), Ghyoot (FCRBE/PREUSE/Zinneke) and Paulet (Careno), but the edges themselves are unsourced → ADD_SOURCE; not deletions.
9. **`maarten_gielen`, `lionel_devlieger`, `tristan_boniver` nodes — PARTIAL.** Documented Rotor co-founders, cited in node `source_urls`, but none was named on a page I fetched this run; could not produce a verbatim naming quote. Low risk, KEEP, but not strictly PROVEN.
10. **`immobel` node `primary_source_url` (`immobelgroup.com`) not fetched.** Identity is corroborated by the OXY page ("property developers Whitewood and Immobel"), so verdict PROVEN, but the node's own primary source was not independently loaded this run.

## 5. Anomalies / notes

- **No dead/unsupported evidence links among the 22 sourced edges** except finding #1. The rotor_dc bubble is otherwise exceptionally clean: every reuse-bubble `evidence_url` resolved to a first-party Rotor / RotorDC / Opalis / PREUSE page that named the relevant endpoints.
- The `p_multi → bw_generale_de_banque` HAT_BAUWERK figures (66 t granite / 230 t finishes) match `opalis.eu/fr/projets/ancien-siege-de-la-generale-de-banque` exactly, and the reuse-in-Multi link is corroborated on the Multi project page.
- `rotordb.org/en/about` returns **404**; the live Rotor site uses `rotordb.org/en` as its homepage. Node `source_urls` pointing at `/en/about` (if any elsewhere) would dead-link, but none in my scope relied on it.

## 6. Items escalated to human

None requiring escalation. All non-PROVEN items have a clear mechanical remediation: **1 DELETE** (rel-0016), **1 RESOURCE** (rel-0008), **15 ADD_SOURCE** (unsourced actor/person edges), and the bidirectional-pair flags routed to **Agent 14**.

## 7. One-paragraph summary

Agent 02 processed **49 claims** (37 rels + 12 nodes) for the Belgium / Rotor cluster, fetching 13 distinct live pages (all HTTP 200; `rotordb.org/en/about` 404 but non-evidential). Verdicts: **30 PROVEN, 3 PARTIAL, 1 UNSUPPORTED, 15 MISSING_EVIDENCE**. All three special checks — `colocation_evere`, the OXY commissioners (Immobel + Whitewood with RotorDC as operator), and the Opalis funder/maintenance edges via `opalis.eu/en/about` — are **PROVEN** on first-party pages. The single most important finding is the lone fabrication **`rotordc → p_architecture_of_reuse_brussels`**: its evidence page names only Rotor (not RotorDC) and contains neither the asserted "Olivia Noël" nor any "BMA launch" — recommend **DELETE**. The 15 MISSING_EVIDENCE rows are unsourced (but largely real) actor/person affiliation edges needing `ADD_SOURCE`, several of them bidirectional pairs to hand to Agent 14.
