# Verifier Agent 09 — Places, Buildings, Projects & Participation

**Database:** `mit-bestand` (READ-ONLY; no graph mutation)
**Date:** 2026-06-06
**Ledger:** [`ledger/agent_09.csv`](../ledger/agent_09.csv) — 2,576 rows (356 nodes + 2,220 relationships)
**Builder (reproducibility):** [`_agent_09_build.py`](../_agent_09_build.py)
**Cross-check sources:** `_neo4j/review/2026-06-06_project_bg_geo_extract/` →
`donor_bauwerke_addresses.json`, `reuse_geo_graph.json`, `akteur_typ_projekt_geo.json`, `sidecar/geo_evidence.jsonl`

---

## 1. Scope & coverage (100 % of shard, no sampling)

| Kind | Element | Planned | Verified |
|---|---|---:|---:|
| Node | `Bauwerk` | 184 | 184 |
| Node | `Projekt` | 83 | 83 |
| Node | `Stadt` | 74 | 74 |
| Node | `Land` | 15 | 15 |
| Rel | `BETEILIGT_AN` | 599 | 599 |
| Rel | `AUS_SPENDER` | 245 | 245 |
| Rel | `IN_EMPFANGSOBJEKT` | 278 | 278 |
| Rel | `HAT_BAUWERK` | 194 | 194 |
| Rel | `NUTZT_BAUWERK` | 1 | 1 |
| Rel | `LIEGT_IN_LAND` | 651 | 651 |
| Rel | `LIEGT_IN_STADT` | 252 | 252 |
| **Total** | | **2,576** | **2,576** |

Counts match the plan and the live graph exactly. Every node-id and relationship element-id in scope appears in exactly one ledger row.

## 2. Method

This is a structural / geo-consistency shard (Cypher-bound + dossier cross-check + selective web), per plan §4 Agent 09:

- **Country check** (`LIEGT_IN_LAND`): country derived from the node's address (English/native country token in the trailing segment), or, for `Stadt`, from real-world geography of the city, or from a linked `Stadt`→`Land`. Compared to the edge's `Land`.
- **City check** (`LIEGT_IN_STADT`): the node address must name the linked `Stadt` (with an exonym table: Brussels↔Brüssel, København/Copenhagen↔Kopenhagen, Vienna↔Wien, Den Bosch↔'s-Hertogenbosch, Liège↔Lüttich, Søborg↔Gladsaxe, Luxembourg↔Limpertsberg). If the address instead names a **different city that already exists as its own `Stadt` node**, that is a `CONTRADICTION`.
- **Donor/receiver chain** (`AUS_SPENDER`, `IN_EMPFANGSOBJEKT`, `HAT_BAUWERK`): the `(Bauteilgruppe → Bauwerk)` donor link and `(Projekt → Bauwerk)` link are confirmed against the donor/receiver chain in `reuse_geo_graph.json` and `donor_bauwerke_addresses.json`.
- **Participation** (`BETEILIGT_AN` actor→project): corroborated by the project's `source_url` recorded in `akteur_typ_projekt_geo.json` (all 474 actor→project links present there).
- **URL-evidence classification:** every node/edge source was classed **real** (`http(s)://…`) vs **placeholder** (`processed`, `archive`, `processed+archive`, `processed+web`, `Council of the EU`, empty, …). Placeholders are **not** proof and are routed to `RESOURCE`.
- **Live web (8 fetches, all HTTP 200):** the highest-value cross-border edges were re-fetched to anchor genuine `fetched=true` PROVEN rows (rotordc.com, zirkular.net, rotordb.org, opalis.eu). `dossier`/`logic` rows record `fetched=false` honestly.

## 3. Verdict totals

| Verdict | Count |
|---|---:|
| PROVEN | 1,645 |
| PARTIAL | 751 |
| MISSING_EVIDENCE | 175 |
| CONTRADICTION | 5 |

Proposed actions: `KEEP` 2,048 · `RESOURCE` 367 · `ESCALATE_HUMAN` 96 · `RELABEL` 63 · `FIX_PROPERTY` 2.
Basis: `dossier` 1,372 · `logic` 1,185 · `web` 19 (8 live-fetched + 11 carrying `evidence_url`).

### By type
| Type | PROVEN | PARTIAL | MISSING | CONTRA |
|---|---:|---:|---:|---:|
| `Land` | 15 | – | – | – |
| `Stadt` | 73 | 1 | – | – |
| `Projekt` | 63 | – | 20 | – |
| `Bauwerk` | 79 | – | 105 | – |
| `LIEGT_IN_LAND` | 309 | 342 | – | 0 |
| `LIEGT_IN_STADT` | 206 | 41 | – | 5 |
| `AUS_SPENDER` | 191 | 54 | – | – |
| `IN_EMPFANGSOBJEKT` | 267 | 11 | – | – |
| `HAT_BAUWERK` | 157 | 37 | – | – |
| `NUTZT_BAUWERK` | 1 | – | – | – |
| `BETEILIGT_AN` | 284 | 265 | 50 | – |

## 4. Geo-consistency result

- **Country (`LIEGT_IN_LAND`): no contradictions.** All 309 edges whose node carries an address or whose source is a city resolve to the asserted `Land`. The 342 `PARTIAL` are organisational nodes (331 `Akteur` + `Software`/`Programm`/`Materialdepot` + ~20 address-less `Bauwerke`) that carry **no address and no `land` property** — their home country cannot be confirmed from the geo files and was left honestly unconfirmed (verdict `PARTIAL`, action `KEEP`), not asserted.
- **City (`LIEGT_IN_STADT`): 5 contradictions** (below). 206 confirmed (incl. exonyms); 41 `PARTIAL` are benign native-name/district variants.
- **City↔country cross-check:** zero cases where a node's city sits in a different country than its `LIEGT_IN_LAND`.
- **All 74 `Stadt`→`Land` canonical pairs are geographically correct** (London→UK, Basel→Schweiz, Paris→Frankreich, Amsterdam→Niederlande, …).

## 5. The 10 worst findings

**5 city contradictions (`CONTRADICTION` / `ESCALATE_HUMAN`):**

1. `bw_alte_kade_tiel` → `stadt_utrecht`, but address is **"Alte Kade, Tiel, Netherlands"**. Tiel (Gelderland) ≠ Utrecht. *(09-lis-0006)*
2. `bw_kerenzerbergtunnel` → `stadt_zuerich`, but address is **"Kerenzerberg tunnel area, Glarus, Switzerland"**. Glarus ≠ Zürich. *(09-lis-0078)*
3. `p_big_dig_building_boston` → `stadt_boston`, but address is **"…Cambridge, MA 02140, USA"**. A `stadt_cambridge_ma` node already exists; the building sits in Cambridge, not Boston. *(09-lis-0176)*
4. `p_circular_centre_netherlands_prinsenhof_a_reuse_pilot` → `stadt_arnhem`, but address is **"Zwarteweg 1, 8181 PD Heerde, Netherlands"**. A `stadt_heerde` node exists. *(09-lis-0190)*
5. `p_haus_hos_mehrfamilienhaus_muehlhausen` → `stadt_leinefelde`, but address is **"Mühlhausen, 99974, Germany"**. The project *also* (correctly) links to `stadt_muehlhausen_thueringen`; the Leinefelde edge is a **donor-site city leaking onto the receiver project** (`bw_leinefelde_plattenbau_donor` is its concrete donor). *(09-lis-0204)*

**5 systemic evidence weaknesses (`MISSING_EVIDENCE` / `RESOURCE` & `ESCALATE_HUMAN`):**

6. **66 of 184 `Bauwerke` rest on placeholder geo sources** (`processed`, `archive`, `archive:<file>.md`, `processed+web`) — no real URL. e.g. `bw_kerenzerbergtunnel` (`processed`), `bw_altes_projekt_in_hanzinelle` (`archive:Verbiest_Karreveld_Brussels.md`).
7. **39 `Bauwerke` have neither address nor any source** (e.g. `bw_alliander_existing_campus`, `bw_alliander_hq_duiven`, `bw_base_du_reemploi_merignac`).
8. **20 `Projekte` lack a real geo source** (6 placeholder, 14 empty), including well-known sites whose address is on file but unsourced: `p_circl_abn_amro`, `p_europa_building_brussels`, `p_thoravej_29_copenhagen`, `p_elys_kultur_gewerbehaus_basel`, `p_ka13_kristian_augusts_gate_13_oslo`, `p_umar_unit`.
9. **63 `BETEILIGT_AN` actor→Bauteilgruppe edges are inferred, not evidenced** (`connection_kind = reuse_supply_or_material_hub_candidate` / `planning_actor_component_involvement`). These are shared-material/"candidate" inferences — the same class as the 29 fabricated edges already removed — verdict `PARTIAL`, action `RELABEL` (keep only as explicit candidates, never as proven participation).
10. **81 donor/receiver edges terminate on unsourced `Materialdepot` nodes** (54 `AUS_SPENDER`, 16 `HAT_BAUWERK`, 11 `IN_EMPFANGSOBJEKT`). `Materialdepot` has **0 sourced nodes** graph-wide → cross-reference Agent 10; verdict `PARTIAL`, action `ESCALATE_HUMAN`.

## 6. Strongest PROVEN anchors (live-fetched, HTTP 200, both endpoints on page)

- `NUTZT_BAUWERK` `rotordc`→`bw_generale_de_banque_brussels` — *"over 230 tonnes of finishing materials were salvaged … This project kick-started Rotor DC"* (rotordc.com).
- `BETEILIGT_AN` `baubuero_in_situ`/`zirkular`→`p_k118_kopfbau_halle_118_winterthur` — *"the projects K.118 in Winterthur and ELYS in Basel … the trigger for the foundation of Zirkular … architecture: baubüro in situ"* (zirkular.net).
- `BETEILIGT_AN` `immobel`/`whitewood`/`Rotor`→`p_oxy_centre_monnaie` — *"acquired by property developers Whitewood and Immobel … Rotor was asked to join the project team"* (rotordb.org).
- `BETEILIGT_AN` `opalis`/`brussels_environment`→`prog_preuse` — *"Opalis is maintained and updated by Rotor and Bellastock … for the PREUSE-project … Rotor by Brussels Environment as part of the Renolution strategy"* (opalis.eu/en/about).

## 7. Escalated to human (96 `ESCALATE_HUMAN`)

- **5 city contradictions** (§5.1–5.5) — re-point `LIEGT_IN_STADT` to the correct existing `Stadt` (or drop the donor-city leak on `p_haus_hos…`).
- **10 structurally unusual `BETEILIGT_AN` targets**: 9 `Akteur`→`Akteur` and 1 `Akteur`→`Software` with no evidence — verify the modelling (participation usually targets `Projekt`/`Programm`).
- **81 `Materialdepot`-endpoint donor/receiver edges** — depend on Agent 10's unsourced-depot remediation.

## 8. Property hygiene (within scope)

- `land_liechtenstein` is missing `country_iso2` → `FIX_PROPERTY` (existence otherwise PROVEN).
- `stadt_paso_robles_templeton_gap` is the only `Stadt` without `latitude`/`longitude` → `FIX_PROPERTY`.
- No forbidden properties, no orphans, and no parallel duplicates observed among the in-scope nodes/edges (full graph-wide hygiene is Agent 14's remit).

## 9. Limits / honesty notes

- 2,568 rows are `fetched=false`: the geo spine was proved by **dossier corroboration + logic** (the loaded geo extract files are this shard's authorised dossier, per plan §3.1 internal-claim rule), and only 8 high-value web claims were live-fetched. No row is marked `PROVEN` on web basis without a `fetched=true` snippet.
- `Akteur`-home-country (`LIEGT_IN_LAND`, 331 edges) was deliberately left `PARTIAL`: the only addresses available for actors in the geo files are **project-derived** (where the actor worked), which cannot validate an actor's seat without risking false contradictions. These need a seat-level source (Agent 08 territory).
- The 11 `BETEILIGT_AN`/`HAT_BAUWERK` edges that carry an `evidence_url` I did not re-fetch are kept at their on-file status with `fetched=false`; full re-fetch of those overlaps Agents 02/06 and should be merged there.

## 10. One-paragraph summary

The physical/temporal spine is **structurally sound**: all 356 places/buildings/projects exist, all 74 city→country pairs are geographically correct, and there are **no country-level contradictions** across 651 `LIEGT_IN_LAND` edges. The real problems are (a) **5 city mis-links** where a building/project is attached to the wrong (but already-modelled) `Stadt` — most tellingly a donor city (`Leinefelde`, `Heerde`) leaking onto a receiver project — and (b) a large **evidence-quality gap on the donor side**: 66 `Bauwerke` and 6 projects rest on `processed`/`archive` placeholder "sources" rather than real URLs, 39 donor `Bauwerke` have no source at all, 63 actor→component participation edges are unproven shared-material inferences, and 81 donor/receiver edges hang off unsourced `Materialdepot` nodes. **Single most important finding:** the geo extract's `source_url` field silently mixes real URLs with placeholder tokens (`processed`, `archive`, `processed+web`), so any downstream consumer treating that column as provenance will over-state evidence for ~half of all donor buildings — these must be `RESOURCE`-d before the geo layer is presented as sourced.
