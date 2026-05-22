# Cross-bubble extension — reuse network mesh (2026-06-06)

Research pass after the five country bubbles (`swiss`, `germany`, `france`, `netherlands`, `rotor_dc`) and the Quelle/evidence cleanup. Goal: **bridge isolated bubble subgraphs** with evidence-backed edges on node/rel properties only.

**Graph before:** 2 304 nodes / 15 527 rels (`mit-bestand`).

## Diagnosis

| Hub pair | Shortest path (pre-patch) | Gap |
|---|---|---|
| `insert_marketplace` ↔ `madaster` | 1 hop | Exists; confidence **teilweise_belegt** — upgrade to formal partnership |
| `madaster` ↔ `madaster_epea` | 2 hops via `ar_forschung_dokumentation` | Missing direct platform-family link |
| `concular` ↔ `restado` | disconnected (`restado` id absent) | Canonical node is `software_restado`; only legacy `BETRIEBEN_VON`, no bubble evidence |
| `software_restado` ↔ `opalis` | 2 hops | No direct European reuse-platform bridge |
| `opalis` ↔ `prog_preuse` | disconnected | Opalis maintained under PREUSE (2024–2027) but not linked |
| `Rotor` ↔ `opalis` | 1 hop | OK |
| `city_of_utrecht` ↔ `prog_preuse` | 1 hop | OK (NL ↔ BE programme bridge) |
| `cirkla` ↔ `concular` | 2 hops via role node | No direct CH ↔ DE marketplace bridge |

**Not imported (deferred):** duplicate `restado` Akteur id — use existing `software_restado` from Bauteilbörsen integration.

## Patch scope (`cross_bubble_extension.patch.jsonl`)

### Upgrades
1. `insert_marketplace` ↔ `madaster` → **belegt** (Madaster–Insert partner agreement, Jan 2019).

### New edges (belegt)
2. `madaster` ↔ `madaster_epea` — same international platform; EPEA database integration.
3. `concular` ↔ `software_restado` — restado is a Concular GmbH brand (Impressum).
4. `opalis` → `prog_preuse` `BETEILIGT_AN` — Opalis maintained under Interreg PREUSE 2024–2027.

### New edges (teilweise_belegt)
5. `software_restado` ↔ `opalis` — European reuse platform peers (ReUse RLP platform listing + ECESP).
6. `software_restado` ↔ `insert_marketplace` — European marketplace peers (passport ↔ marketplace layer).
7. `cirkla` ↔ `software_restado` — Swiss umbrella ↔ German marketplace peer (ReUse RLP platform listing).

### Node enrichment
8. `software_restado` — `primary_source_url` → `https://restado.de/ueber-restado/`.

## Deferred (no patch)

| Item | Reason |
|---|---|
| `city_of_utrecht` ↔ `insert_marketplace` | No first-party co-project URL; connected indirectly via `madaster` |
| `rotordc` ↔ `bellastock` direct | No first-party org link (Rotor/DC deferred) |
| Bulk FCRBE pilot `:Projekt` nodes | Registry exists; selective import only |
| `overall_stiftung` as `:Akteur` | Swiss deferred — useagain owner cited but no dedicated profile node |

## Evidence sources

See [`EVIDENCE_REGISTER.csv`](EVIDENCE_REGISTER.csv).

## Apply (both phases)

```powershell
python _neo4j/review/2026-06-06_cross_bubble_extension/apply_cross_bubble_both.py
python _neo4j/review/2026-06-06_cross_bubble_extension/apply_cross_bubble_both.py --commit
```

Or individually:

```powershell
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_cross_bubble_extension/patches/cross_bubble_extension.patch.jsonl --confirm "APPLY cross_bubble_extension.patch.jsonl TO mit-bestand"
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_cross_bubble_extension/patches/cross_bubble_extension_phase2.patch.jsonl --confirm "APPLY cross_bubble_extension_phase2.patch.jsonl TO mit-bestand"
```

Post-apply: re-run `_probe_cross_bubble.py` and verify `concular`–`software_restado` path length 1.

## Phase 2 — applied (`cross_bubble_extension_phase2.patch.jsonl`)

Swiss hub enrichment, Germany HdM consortium completion, Rotor-DC commissioner links, CH↔DE marketplace bridge.

| Change | Confidence |
|---|---|
| `sumami` ↔ `cirkla` / `eth_zuerich` / `circular_hub_zurich` | belegt |
| `kunst_stoffe_ev` ↔ `material_mafia` / `circular_berlin` | belegt |
| `rotordc` ↔ `whitewood` / `immobel` | belegt |
| `brussels_environment` ↔ `opalis` | belegt |
| `useagain_bauteilclick` ↔ `software_restado` | teilweise_belegt |
| `city_of_utrecht` ↔ `madaster` upgrade (PREUSE Utrecht) | belegt |

**Graph after phase 2:** 2 304 nodes / **15 556** rels (+29 total).
