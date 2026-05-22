# Manual remodel candidates (round 3) - NO automatic edges created

These reduce node keys further but require **evidence-based, manual** decisions.
Nothing here was applied. Each item lists the current data and a candidate model.

---

## 1. Quelle URL keys - 5 unique URLs to preserve before keys can be dropped

`source_url` / `source_urls` / `primary_source_url` on `ReuseRule`: 55/60 URL
values already exist on a linked `Quelle` (safe), but these **5 are unique** and
would be lost if the keys were dropped. Each should become a `Quelle` (+ an
evidence-based `BELEGT_IN`/`HAS_SOURCE_LINK` from the rule) **manually**:

| ReuseRule | unique URL |
| --- | --- |
| `rr_ch_stahl` | openbim-knowledgebase.org/.../construction-products-act-baupg/ |
| `rr_fi_beton_hollow_core_slabs` | recreate-project.eu/2025/05/27/.../precast-concrete/ |
| `rr_no_beton_hollow_core_slabs` | standard.no/.../norwegian-standard-for-hollow-core-slabs-for-reuse--ns-3682/ |
| `rr_de_holz` | iom3.org/asset/E62529EE-... |
| `rr_ch_holz` | cirkla.ch/en/publications-outils/projet-innosuisse/ |

Once these 5 are captured, `source_url` / `source_urls` / `primary_source_url`
can be dropped (the rest are redundant). **-3 keys after manual step.**

---

## 2. ReuseRule denormalized payload (free-text arrays)

`ReuseRule` (20 nodes) holds domain lists as **free text**, so they cannot be
auto-linked to existing vocab nodes without manual matching:

| key | example values | candidate target node type / edge |
| --- | --- | --- |
| `key_norms` | "EN 1090-2", "Eurocode 3", "DIN EN 1993" | `Norm` via `REFERENZIERT_NORM` (free text -> Norm id, manual) |
| `required_tests` | "tensile/yield/elongation", "NDT of welds" | `PruefungNachweis` via `HAT_PRUEFUNG` (manual) |
| `pollutant_risks` | "Asbestos fireproofing", "PCB sealants" | `Schadstoff` via `HAS_RISK_POLLUTANT` (manual) |
| `processing_methods` | "Shotblast", "Decoat", "Recertify" | `Aufbereitungsverfahren` via `HAT_AUFBEREITUNG` (manual) |
| `material_id` | `mat_stahl` (clean node id) | `Material` via `NUTZT_MATERIAL` (deterministic, ready) |
| `material` | "Steel", "Concrete" (free text label) | duplicate of `material_id`; drop after edge exists |
| `country_iso` | `GB`, `DE`, `CH` | `Land` via `GILT_IN_LAND` (deterministic, ready) |
| `country_name` | "United Kingdom" | duplicate of `country_iso`; drop after edge |
| `legal_conditions` | free text | `RechtlicheBedingung` (manual) |
| `project_cluster` | cluster label | review - keep as scalar or model as grouping node |

The two **deterministic** ones (`material_id`->Material, `country_iso`->Land) could
be applied immediately on request; the free-text arrays need manual matching.

---

## 3. Land pollutant-regulation years -> Schadstoff edges (recommended, deterministic)

The per-pollutant ban years on `Land` map cleanly to existing `Schadstoff` nodes.
Recommended model: `(Land)-[:REGULIERT {jahr, note}]->(Schadstoff)`, then drop the
year keys. This is a deterministic mapping (not fuzzy) - ready for your approval:

| key | -> Schadstoff | example |
| --- | --- | --- |
| `asbest_verbot_jahr` | `s_asbest` | DE 1993, GB 2000, CH 1990, NO 1980 ... |
| `pcb_verbot_jahr` | `s_pcb` | DE 1989, US 1979, JP 1974 ... |
| `kmf_grenzwert_jahr` | `s_kmf` | DE 1996 |
| `asbest_neshap_year` (+ `asbest_note`) | `s_asbest` | US 1973 (note: no federal ban; NESHAP rules) |

Data present on 13 Land nodes. Applying this removes `asbest_verbot_jahr`,
`pcb_verbot_jahr`, `kmf_grenzwert_jahr`, `asbest_neshap_year`, `asbest_note`
(**-5 keys**) while preserving every year as edge evidence.

`country_iso2` (Land) and `country_short` (Norm) are legitimate ISO/short-name
attributes - **keep**, not remodel.

---

## Potential further reduction (after manual steps)

- Section 1: -3 keys (URL keys)
- Section 2: -8..10 keys (ReuseRule payload, once matched)
- Section 3: -5 keys (Land years)

That would take the in-use node keys from **60** to roughly **45**, still with no
data loss and no unsupported connections.
