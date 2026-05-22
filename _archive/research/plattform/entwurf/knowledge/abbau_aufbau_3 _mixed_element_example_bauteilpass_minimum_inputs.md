# Minimum Inputs Collected from Mixed Element Bauteilpass Example

**Source document:** `_archive/research/plattform/entwurf/knowledge/3 abbau_aufbau_mixed_element_example_bauteilpass.md`  
**Extraction date:** 2026-06-10  
**Status:** legacy-derived reference extraction, not canonical Neo4j truth and not an import payload.

This document collects every `Minimum Input` block from the source document into one place.
Repeated or similar fields are intentionally kept under their original source sections.
No semantic merge, normalization, or Neo4j import decision is made here.

---

## 1.4 Minimum Input for This Example

Source line: 104

```yaml
minimum_input:
  component_id: AA_MIX_001
  component_typology: mixed_slab_beam_column_slice
  material_kind: reinforced_concrete

  base_geometry_reference: representations/AA_MIX_001/base.glb

  source_context:
    source_project: Abbau Aufbau
    source_building: donor-building-001
    original_level: 1OG
    original_function: slab_beam_column_zone

  pool_context:
    kit_id: kit-abbau-aufbau-pool-001
    current_storage_location: storage-yard-01
    storage_position: MIX-A-01

  project_defaults:
    density_reinforced_concrete_kg_m3: 2400
    lambda_reinforced_concrete_W_mK: 2.3
    transport_factor_kgco2e_per_tkm: 0.05
    new_precast_concrete_reference_kgco2e_per_t: 171.7
    default_transport_distance_km: 40

  optional_evidence:
    concrete_test_report: null
    reinforcement_scan: partial
    damage_photos: available
    fire_document: null
    lca_dataset: generic_reference_only
```

---

## 0. Header / Quick Summary

Source line: 571

```yaml
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
base_geometry_reference: representations/AA_MIX_001/base.glb
current_storage_location: storage-yard-01
```

---

## 1. Semio Binding

Source line: 648

```yaml
kit_id: kit-abbau-aufbau-pool-001
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

---

## 2. Identity + Traceability

Source line: 737

```yaml
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
source_project: Abbau Aufbau
source_building_id: donor-building-001
original_level: 1OG
original_function: slab_beam_column_zone
```

---

## 3. Pool Availability

Source line: 811

```yaml
component_id: AA_MIX_001
stock_rule: individual_component
design_graph_access: true
storage_location: storage-yard-01
```

---

## 4. Classification

Source line: 877

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

---

## 5. Geometry Overview

Source line: 969

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

---

## 6. Geometry Representations

Source line: 1042

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

---

## 7. Physical Geometry

Source line: 1120

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
```

---

## 8. Structural Geometry

Source line: 1197

```yaml
component_typology: mixed_slab_beam_column_slice
base_geometry_reference: representations/AA_MIX_001/base.glb
original_function: slab_beam_column_zone
```

---

## 9. Energy / Envelope Geometry

Source line: 1285

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
intended_exposure_context: unknown
```

---

## 10. Semantic / Architectural Geometry

Source line: 1358

```yaml
component_typology: mixed_slab_beam_column_slice
source_context:
  original_function: slab_beam_column_zone
target_use_context: unknown
```

---

## 11. Openings + Penetrations

Source line: 1435

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
```

---

## 12. Surface + Edge Condition

Source line: 1496

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
damage_photos: available
```

---

## 13. Damage Records

Source line: 1565

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
damage_photos: available
```

---

## 14. Concrete Evidence

Source line: 1636

```yaml
material_kind: reinforced_concrete
concrete_test_report: null
```

---

## 15. Reinforcement Evidence

Source line: 1707

```yaml
component_typology: mixed_slab_beam_column_slice
reinforcement_scan: partial
```

---

## 16. Durability + Restnutzungsdauer

Source line: 1779

```yaml
material_kind: reinforced_concrete
storage_context: outdoor_storage_with_weather_protection_unknown
condition_status: partial
```

---

## 17. Structural Data

Source line: 1850

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
base_geometry_reference: representations/AA_MIX_001/base.glb
original_function: slab_beam_column_zone
```

---

## 18. Connector / Interface Data

Source line: 1944

```yaml
component_typology: mixed_slab_beam_column_slice
project_connector_library: abbau_aufbau_connection_families
```

---

## 19. Bohrzonen / No-Drill Zones

Source line: 2049

```yaml
component_typology: mixed_slab_beam_column_slice
rebar_scan: partial
project_drilling_defaults: available
```

---

## 20. Fire Data

Source line: 2119

```yaml
material_kind: reinforced_concrete
component_typology: mixed_slab_beam_column_slice
fire_document: null
```

---

## 21. Building Physics Data

Source line: 2188

```yaml
material_kind: reinforced_concrete
component_typology: mixed_slab_beam_column_slice
exposure_context: unknown
project_thermal_defaults:
  lambda_reinforced_concrete_W_mK: 2.3
```

---

## 22. Acoustic Data

Source line: 2256

```yaml
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
```

---

## 23. TGA / Services Data

Source line: 2315

```yaml
base_geometry_reference: representations/AA_MIX_001/base.glb
component_typology: mixed_slab_beam_column_slice
service_context: unknown
```

---

## 24. Logistics Data

Source line: 2392

```yaml
component_typology: mixed_slab_beam_column_slice
base_geometry_reference: representations/AA_MIX_001/base.glb
material_kind: reinforced_concrete
storage_location: storage-yard-01
```

---

## 25. Transport Data

Source line: 2476

```yaml
storage_location: storage-yard-01
target_site_location: rebuild-site-01
transport_distance_km: 40
project_transport_factor_kgco2e_per_tkm: 0.05
```

---

## 26. LCA / Oekobilanz Data

Source line: 2546

```yaml
material_kind: reinforced_concrete
component_typology: mixed_slab_beam_column_slice
project_lca_defaults:
  transport_factor_kgco2e_per_tkm: 0.05
  new_precast_concrete_reference_kgco2e_per_t: 171.7
transport_distance_km: 40
```

---

## 27. Documentation

Source line: 2634

```yaml
component_id: AA_MIX_001
file_references:
  base_geometry: available
  damage_photos: available
  rebar_scan: partial
```

---

## 28. Evidence Completeness

Source line: 2711

```yaml
component_id: AA_MIX_001
component_typology: mixed_slab_beam_column_slice
material_kind: reinforced_concrete
base_geometry_reference: representations/AA_MIX_001/base.glb
```

---

## 29. Pool-Level Warnings

Source line: 2786

```yaml
generated_geometry: complete
evidence_status:
  concrete: missing
  rebar: partial
  damage: partial
  fire: missing
  lca: precheck_only
```

---

## 30. Rule-Checker Readiness

Source line: 2856

```yaml
generated_representations: complete
system_evidence_status: partial
project_rule_library: abbau_aufbau
```
