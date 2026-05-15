# Actor registry processing report

- Input root: `E:/recherche/_neo4j/intake/archive/2026-05-15_actor_registry_seed/raw_tree`
- Canonical chunk files read: **12**
- Node records: **703** → **588** unique node IDs
- Relationship records: **2896** → **2639** unique semantic relationships
- Node content conflicts encountered: **10**

## Merge rules

- Nodes merge by canonical `id`.
- Relationships merge by `(from, type, to, scope)`.
- Chunks are treated as provenance only, not as durable semantic units.

## Node conflicts kept for review

- `p_stuttgart_210`: kept `canonical/actor_registry_021_030/actors_021_030.canonical.kg.jsonl`, also saw `canonical/actor_registry_071_080/actors_071_080.canonical.kg.jsonl`
- `p_umar_unit`: kept `canonical/actor_registry_061_070/actors_061_070.canonical.kg.jsonl`, also saw `canonical/actor_registry_071_080/actors_071_080.canonical.kg.jsonl`
- `p_zinneke_feder_masui4ever_brussels`: kept `canonical/actor_registry_031_040/actors_031_040.canonical.kg.jsonl`, also saw `canonical/actor_registry_071_080/actors_071_080.canonical.kg.jsonl`
- `p_multi_brussels_reuse_in_multi`: kept `canonical/actor_registry_041_050/actors_041_050.canonical.kg.jsonl`, also saw `canonical/actor_registry_071_080/actors_071_080.canonical.kg.jsonl`
- `p_architecture_of_reuse_brussels`: kept `canonical/actor_registry_041_050/actors_041_050.canonical.kg.jsonl`, also saw `canonical/actor_registry_071_080/actors_071_080.canonical.kg.jsonl`
- `p_zinneke_feder_masui4ever_brussels`: kept `canonical/actor_registry_031_040/actors_031_040.canonical.kg.jsonl`, also saw `canonical/actor_registry_081_090/actors_081_090.canonical.kg.jsonl`
- `p_multi_brussels_reuse_in_multi`: kept `canonical/actor_registry_041_050/actors_041_050.canonical.kg.jsonl`, also saw `canonical/actor_registry_081_090/actors_081_090.canonical.kg.jsonl`
- `p_architecture_of_reuse_brussels`: kept `canonical/actor_registry_041_050/actors_041_050.canonical.kg.jsonl`, also saw `canonical/actor_registry_081_090/actors_081_090.canonical.kg.jsonl`
- `p_circle_house`: kept `canonical/actor_registry_011_020/actors_011_020.canonical.kg.jsonl`, also saw `canonical/actor_registry_101_110/actors_101_110.canonical.kg.jsonl`
- `q_akteursliste_master_md`: kept `canonical/actor_registry_011_020/actors_011_020.canonical.kg.jsonl`, also saw `canonical/actor_registry_first10/actors_first10.canonical.kg.jsonl`
