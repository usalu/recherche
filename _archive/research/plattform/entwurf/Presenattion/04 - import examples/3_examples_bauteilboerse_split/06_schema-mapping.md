# Schema-Mapping

## 1. Rippenplatte / Spannbeton

### 1.6 Schema-Mapping

#### Item

```yaml
canonical_title: Rippenplatte aus Spannbeton
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
newness_type: reclaimed
```

#### VariantBatch

```yaml
quantity: 188
quantity_unit: piece
length_mm: 6840
width_mm: 1495
height_mm: 480
area_m2: 10.23
total_area_m2: 1922.45
```

#### RiskAssessment

```yaml
risk_level: high
hazard_flags:
  - chlorides
  - corrosion
  - moisture_damage
  - hydrocarbons
  - unknown_pollutants
structural_verification_required: true
pollutant_test_status: partial_test
```

---

## 2. Stahlträger HEB 140

### 2.6 Schema-Mapping

#### Item

```yaml
canonical_title: Stahlträger HEB 140
component_family: structure
component_type: beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
```

#### TechnicalAttribute

```yaml
attribute_group: metal_steel
profile_type: HEB
section_size: "140"
nominal_profile_height_mm: 140
nominal_profile_width_mm: 140
typical_mass_kg_per_m: 33.7-34.2
typical_elastic_modulus_mpa: 210000
accessory_list: Unterlegbleche für Mauerwerks- und Balkenauflager
```

---

## 3. Historische Holzbalken aus Altbausanierung

### 3.6 Schema-Mapping

#### Item

```yaml
canonical_title: Historische Holzbalken aus Altbausanierung
component_family: structure
component_type: beam
material_family: timber_biobased
primary_material: solid_timber
newness_type: reclaimed
structural_role: unknown_or_potentially_load_bearing
short_description: Alte, trockene Holzbalken mit rustikaler Oberfläche und teilweise fränkischer Kerbe.
```

#### VariantBatch

```yaml
quantity: 10
quantity_unit: piece
length_min_mm: 1000
length_max_mm: 6000
width_min_mm: 180
width_max_mm: 220
height_min_mm: 180
height_max_mm: 220
estimated_total_volume_typical_m3: 1.4
dimension_notes: Querschnitte variieren; Einzelmaße je Balken erforderlich.
```

#### TechnicalAttribute

```yaml
attribute_group: timber
estimated_age_years: 160
wood_species: unknown
solid_or_engineered: solid_timber
surface_finish: raw_untreated
moisture_condition: very_dry
joinery_detail: two-sided_franconian_notch_partial
```
