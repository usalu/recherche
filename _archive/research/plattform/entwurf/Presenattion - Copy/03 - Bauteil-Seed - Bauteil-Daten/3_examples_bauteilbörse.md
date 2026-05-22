

---

## Overview

| Case | Component | Source Type | Material | Reuse / Newness Type | Main Value | Main Review Need |
|---|---|---|---|---|---|---|
| 1 | Rippenplatte aus Spannbeton | Listing, datasheets, images, DWG, PDF | Prestressed concrete | Reclaimed | Known quantity, dimensions, and technical properties | Structural liability, pollutants, deconstruction/cutting damage |
| 2 | Stahlträger HEB 140 | Screenshot, image gallery, visible listing text | Steel | Overstock | Standardized profile and predictable reference values | Verification of grade, exact condition, and structural parameters |
| 3 | Historische Holzbalken aus Altbausanierung | User prompt, free-text description | Solid timber | Reclaimed | High historical and design value | Wood species, dimensions per piece, pests, moisture, structural verification |

---




# 1. Rippenplatte / Spannbeton

## 1.1 Input-Typen

```yaml
input_types:
  - listing_url
  - html_listing
  - images
  - pdf_factsheet_de
  - pdf_factsheet_en
  - dwg_file
  - print_pdf
```

## 1.2 Raw Extraction

```yaml
title: Rippenplatte Stahlbeton / L=6.84m, B=1.495m
component_raw: strukturelles Deckenelement
material_raw: Fertigteil-Stahlbeton / Spannbeton
dimensions_raw: 6.84m x 1.495m x 48cm
quantity: 188 Stück
co2_new_per_piece: 908 kg/Stk
co2_reuse_per_piece: -635 kg/Stk
carbonation_depth: 21 mm
concrete_compressive_strength: 67.4 N/mm2
concrete_elastic_modulus: 42.1 bis 50.5 kN/mm2
deconstruction_tool: Diamantsäge
risk_notes:
  - Chloride
  - Korrosion
  - Feuchtigkeit
  - Kohlenwasserstoffe
  - Asbest/PCB ungeklärt
```

## 1.3 Normalisierung

```yaml
length_mm: 6840
width_mm: 1495
height_mm: 480
quantity: 188
quantity_unit: piece
compressive_strength_mpa: 67.4
modulus_elasticity_mpa: 42100-50500
```

## 1.4 Klassifikation

```yaml
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
data_source_type: technical_inventory
```

## 1.5 Abgeleitete Daten

```yaml
bounding_volume_per_element_m3:
  value: 4.91
  basis: 6.84 * 1.495 * 0.48
  note: geometrischer Hüllkörper, nicht tatsächliches Betonvolumen
  confidence: high
```

```yaml
possible_reuse_roles:
  - Deckenplatte
  - Dachplatte
  - Brückenelement nur nach Sonderprüfung
  - Landschafts-/Außenraumelement mit geringerem statischem Anspruch
```

```yaml
reuse_barriers:
  value:
    - structural_liability
    - pollutant_uncertainty
    - high_logistics_cost
    - dimensional_inflexibility
    - cutting_or_deconstruction_damage
  confidence: high
  reasoning_source: material_logic
  review_required: true
```

## 1.6 Schema-Mapping

### Item

```yaml
canonical_title: Rippenplatte aus Spannbeton
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
newness_type: reclaimed
```

### VariantBatch

```yaml
quantity: 188
quantity_unit: piece
length_mm: 6840
width_mm: 1495
height_mm: 480
area_m2: 10.23
total_area_m2: 1922.45
```

### RiskAssessment

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

# 2. Stahlträger HEB 140

## 2.1 Input-Typen

```yaml
input_types:
  - screenshot
  - image_gallery
  - visible_listing_text
```

## 2.2 Raw Extraction

```yaml
title: Stahlträger HEB 140 - Länge 2,54m
article_number: "#201605"
condition_raw: Neu
component_raw: Stahlträger
profile_raw: HEB 140
length: 2.54 m
included_parts: Unterlegbleche
quantity: nicht sichtbar
price: nicht sichtbar
location: nicht sichtbar
```

## 2.3 Normalisierung

```yaml
length_mm: 2540
component_normalized: steel_beam
profile_type: HEB
section_size: "140"
condition_normalized: new
```

## 2.4 Klassifikation

```yaml
component_family: structure
component_type: beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
```

## 2.5 Abgeleitete Daten

```yaml
typical_mass_kg_per_m:
  value_range: 33.7-34.2
  basis: typische HEB-140-Profilmasse
  confidence: medium

estimated_piece_weight_kg:
  value_range: 85.6-86.9
  basis: 2.54 m * 33.7-34.2 kg/m
  confidence: medium
```

```yaml
typical_steel_density_kg_m3:
  value: 7850
  confidence: high

typical_elastic_modulus_mpa:
  value: 210000
  confidence: high

possible_steel_grades:
  - S235
  - S275
  - S355

estimated_elastic_bending_resistance_s235_knm:
  value_approx: 51
  basis: typischer elastischer Widerstandsmomentwert HEB 140 * 235 MPa
  confidence: low
  verification_required: true
```

## 2.6 Schema-Mapping

### Item

```yaml
canonical_title: Stahlträger HEB 140
component_family: structure
component_type: beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
```

### TechnicalAttribute

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

# 3. Historische Holzbalken aus Altbausanierung

## 3.1 Input-Typen

```yaml
input_types:
  - user_prompt
  - free_text_description
  - no_images
  - no_url
  - no_documents
```

## 3.2 Raw Extraction

```yaml
component_raw: alte Holzbalken
source_context: laufende Altbausanierung
estimated_age: ca. 160 Jahre
quantity: 10 Stück
cross_section_range: meist 18x18 bis 20x22 cm
max_cross_section: 22x22 cm
length_range: ca. 1 bis 6 m
special_feature: teilweise zweiseitige fränkische Kerbe
condition_raw: sehr trocken, sehr gut erhalten
surface: roh, unbehandelt, gesägt und geschlagen
look: historisch, rustikal
price_raw: 20, Einheit/Währung unklar
```

## 3.3 Normalisierung

```yaml
quantity: 10
quantity_unit: piece
length_min_mm: 1000
length_max_mm: 6000
width_min_mm: 180
width_max_mm: 220
height_min_mm: 180
height_max_mm: 220
estimated_age_years: 160
```

## 3.4 Klassifikation

```yaml
component_family: structure
component_type: beam
material_family: timber_biobased
primary_material: solid_timber
structural_role: unknown_or_potentially_load_bearing
newness_type: reclaimed
```

## 3.5 Abgeleitete Daten

```yaml
assumed_dry_timber_density_kg_m3:
  value_range: 450-650
  confidence: medium

estimated_total_weight_typical_kg:
  value_range: 630-910
  basis: 1.4 m3 * 450-650 kg/m3
  confidence: low
```

```yaml
structural_use_condition:
  value: Tragende Wiederverwendung nur nach Festigkeitssortierung, Feuchteprüfung, Schädlingsprüfung und Ingenieurfreigabe
  confidence: high
```

```yaml
design_value:
  value: hoch für sichtbare, historische und rustikale Anwendungen
  basis: 160 Jahre, roh, gesägt/geschlagen, fränkische Kerbe
  confidence: high
```

```yaml
critical_design_checks:
  - Holzart bestimmen
  - Querschnitt je Stück messen
  - Risse und Kerben bewerten
  - Insekten- und Pilzbefall prüfen
  - Resttragfähigkeit prüfen
  - frühere Verbindungslöcher und Kerben bewerten
  - Brandschutz im neuen Kontext prüfen
```

## 3.6 Schema-Mapping

### Item

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

### VariantBatch

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

### TechnicalAttribute

```yaml
attribute_group: timber
estimated_age_years: 160
wood_species: unknown
solid_or_engineered: solid_timber
surface_finish: raw_untreated
moisture_condition: very_dry
joinery_detail: two-sided_franconian_notch_partial
```
