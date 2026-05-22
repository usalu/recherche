# Bereinigtes Schema für wiederverwendbare Bauteile

## 1. Ziel

Dieses Schema trennt **Bauteil-Identität**, **plattformbezogene Inserate**, **technische Daten**, **Verfügbarkeit**, **Risiken** und **Dokumentation** klar voneinander. Dadurch entstehen keine doppelten oder widersprüchlichen Felder.

**Prinzip:**  
Ein Feld gehört immer dorthin, wo es entsteht:

| Information | Gehört zu |
|---|---|
| Was ist das Bauteil? | `Item` |
| Wo wurde es veröffentlicht? | `Listing` |
| Welche Menge ist aktuell verfügbar? | `AvailabilitySnapshot` |
| Wo liegt es oder woher kommt es? | `Location` / `Provenance` |
| Welche technischen Werte hat es? | `TechnicalAttribute` |
| Welche Risiken bestehen? | `RiskAssessment` |
| Welche Dateien belegen die Angaben? | `DocumentationAsset` |
| Wie gut ist es wiederverwendbar? | `ReuseAssessment` |

---

## 2. Zentrale Entitäten

| Entität | Zweck |
|---|---|
| `Item` | Stabile Identität des Bauteils oder Materials |
| `Listing` | Plattform-spezifisches Inserat, z. B. IBS, useagain, Concular |
| `VariantBatch` | Varianten, Subtypen oder Chargen innerhalb eines Items |
| `Location` | Aktueller Standort, Lagerort, Shop oder Baustelle |
| `Provenance` | Herkunftsgebäude, Projekt, frühere Nutzung |
| `DocumentationAsset` | Fotos, PDFs, CAD, BIM, Prüfberichte, Materialpässe |
| `TechnicalAttribute` | Flexible technische Eigenschaften je Kategorie |
| `AvailabilitySnapshot` | Zeitgestempelter Bestand, Preis, Seitenstatus |
| `RiskAssessment` | Schadstoffe, Zertifikate, strukturelle Unsicherheit |
| `ReuseAssessment` | Wiederverwendungs- und Beschaffungsreife |

---

## 3. Redundanzregeln

| Nicht doppelt speichern | Saubere Lösung |
|---|---|
| `canonical_title` und `original_title` im selben Kontext | `canonical_title` bei `Item`, `original_title` bei `Listing` |
| Preis direkt am Bauteil | Preis immer bei `Listing` oder `AvailabilitySnapshot` |
| Verfügbarkeit direkt am Bauteil | Verfügbarkeit als zeitgestempelter Snapshot |
| Plattformkategorie als eigene Systemkategorie | Rohkategorie bei `Listing`, normalisierte Kategorie bei `Item` |
| Zustand und Wiederverwendungsreife vermischen | Physischer Zustand in `Condition`, strategische Bewertung in `ReuseAssessment` |
| Herkunftsadresse und Lageradresse vermischen | `Provenance` für Ursprungsgebäude, `Location` für aktuellen Standort |
| Technische Spezialfelder als feste Spalten für alle Items | Kategorie-spezifische Werte in `TechnicalAttribute` |

---

## 4. Universelle Felder

### 4.1 `Item`

```text
item_id
canonical_title
component_family
component_type
material_family
primary_material
secondary_materials
newness_type
structural_role
is_batch
parent_item_id
short_description
```

### 4.2 `Listing`

```text
listing_id
item_id
source_platform
source_url
canonical_url
external_listing_id
external_article_number
original_title
platform_category_raw
page_status
data_source_type
first_seen_at
last_seen_at
last_verified_at
data_confidence
```

### 4.3 `VariantBatch`

```text
variant_id
item_id
variant_label
subtype_number
quantity
quantity_unit
length_mm
width_mm
height_mm
thickness_mm
diameter_mm
area_m2
volume_m3
weight_kg_per_unit
total_weight_kg
dimension_notes
```

### 4.4 `Location`

```text
location_id
location_type
name
address_visible
postcode
city
region
country
latitude
longitude
```

### 4.5 `Provenance`

```text
provenance_id
item_id
source_building_name
source_project_name
source_building_year
installation_year
original_use
original_position
owner_or_provider
```

### 4.6 `AvailabilitySnapshot`

```text
snapshot_id
listing_id
checked_at
availability_status
quantity_available
quantity_unit
price_amount
currency
price_unit
price_type
vat_included
minimum_order_quantity
available_from
available_until
pickup_deadline
deconstruction_window_start
deconstruction_window_end
cart_available
reservation_possible
contact_required
commercial_only
warranty_status
availability_notes
```

### 4.7 `Condition`

```text
condition_id
item_id
condition_raw
condition_normalized
wear_level
damage_notes
missing_parts
cleaned_status
tested_status
refurbished_status
inspection_date
inspection_method
```

### 4.8 `RiskAssessment`

```text
risk_id
item_id
risk_level
hazard_flags
pollutant_test_status
structural_verification_required
fire_certificate_status
ce_marking_status
engineer_review_status
reuse_restrictions
risk_notes
```

### 4.9 `Logistics`

```text
logistics_id
listing_id
deconstruction_status
demounting_responsibility
transport_mode
loading_included
crane_required
forklift_required
palletized
packaging_status
access_constraints
logistics_notes
```

### 4.10 `DocumentationAsset`

```text
asset_id
item_id
listing_id
asset_type
asset_url
file_format
language
title
description
source_date
checked_at
asset_confidence
```

### 4.11 `EnvironmentalData`

```text
environmental_id
item_id
co2_saved_kg
embodied_carbon_kgco2e
grey_energy_mj
avoided_waste_kg
reuse_percentage
lca_method
environmental_data_confidence
```

### 4.12 `ReuseAssessment`

```text
assessment_id
item_id
reuse_confidence_score
procurement_readiness
design_readiness
technical_readiness
recommended_next_action
assessment_notes
assessed_at
```

---

## 5. Kategoriespezifische Attributpakete

Kategoriespezifische Felder werden nicht als feste Spalten in `Item` gespeichert, sondern als flexible `TechnicalAttribute`-Einträge.

### Struktur von `TechnicalAttribute`

```text
attribute_id
item_id
attribute_group
attribute_name
value_number
value_text
value_boolean
unit
source_asset_id
confidence
verified_at
```

### 5.1 Tragende Betonbauteile

```text
concrete_type
precast_or_cast_in_situ
prestressed
reinforcement_type
compressive_strength_mpa
modulus_elasticity_mpa
carbonation_depth_mm
chloride_content
concrete_cover_mm
load_capacity_known
original_static_system
connection_type
cutting_required
lifting_points_known
crack_condition
spalling_condition
```

### 5.2 Holz

```text
wood_species
solid_or_engineered
strength_class
moisture_content_percent
treatment_type
surface_finish
nail_screw_contamination
insect_damage
fungal_damage
reuse_as_structural_allowed
planing_required
de_nailing_required
```

### 5.3 Metall / Stahl

```text
metal_type
steel_grade
profile_type
section_size
corrosion_level
coating_type
galvanized
welded_connections
bolted_connections
load_capacity_known
fire_protection_coating
```

### 5.4 Fenster / Glas / Fassade

```text
frame_material
glazing_type
number_of_panes
u_value_w_m2k
g_value
sound_reduction_db
fire_rating
opening_type
shading_included
hardware_included
seal_condition
glass_damage
installation_frame_included
```

### 5.5 Türen

```text
door_type
leaf_material
frame_included
hardware_included
fire_rating
sound_rating_db
security_class
swing_direction
surface_finish
lock_included
key_available
```

### 5.6 Ausbauoberflächen

```text
finish_material
format_size_mm
thickness_mm
coverage_area_m2
surface_finish
adhesive_residue
cleaning_required
reinstallation_method
color_variation
batch_consistency
```

### 5.7 Sanitär / Küche / Einbauten

```text
fixture_type
manufacturer
model
material
color
fittings_included
water_connection_status
electrical_connection_status
tested_for_leaks
hygiene_condition
```

### 5.8 Gebäudetechnik

```text
mep_category
manufacturer
model
power_rating
voltage
capacity
energy_label
commissioning_year
maintenance_records_available
tested_operational
certification_status
```

### 5.9 Schüttgut / Restmaterial

```text
material_grade
grain_size
packaging_unit
batch_weight_kg
contamination_level
new_or_recycled
storage_condition
waste_code
recycling_route
```

---

## 6. Bauteil-Taxonomie

```text
component_family
├── structure
│   ├── slab
│   ├── beam
│   ├── column
│   ├── wall_element
│   ├── stair_element
│   └── foundation_element
├── envelope
│   ├── window
│   ├── exterior_door
│   ├── facade_panel
│   ├── roof_element
│   ├── insulation
│   ├── waterproofing
│   └── shading
├── interior_fitout
│   ├── interior_door
│   ├── partition
│   ├── flooring
│   ├── wall_finish
│   ├── ceiling_finish
│   ├── built_in_furniture
│   └── hardware
├── building_services
│   ├── radiator
│   ├── ventilation_unit
│   ├── duct
│   ├── pipe
│   ├── cable_tray
│   ├── lighting
│   ├── electrical_fixture
│   ├── sanitary_fixture
│   └── kitchen_fixture
├── site_external
│   ├── paving
│   ├── kerbstone
│   ├── fence
│   ├── railing
│   └── street_furniture
└── bulk_material
    ├── brick
    ├── tile
    ├── stone
    ├── aggregate
    ├── recycled_concrete
    ├── timber_offcut
    ├── metal_scrap
    └── mixed_lot
```

---

## 7. Material-Taxonomie

```text
material_family
├── mineral
│   ├── concrete
│   │   ├── reinforced_concrete
│   │   ├── prestressed_concrete
│   │   ├── precast_concrete
│   │   └── recycled_concrete
│   ├── brick_ceramic
│   ├── natural_stone
│   ├── artificial_stone
│   ├── gypsum
│   └── mineral_insulation
├── timber_biobased
│   ├── solid_timber
│   ├── glulam
│   ├── clt
│   ├── plywood
│   ├── osb
│   ├── mdf_particleboard
│   └── cork_fibreboard
├── metal
│   ├── steel
│   ├── stainless_steel
│   ├── aluminium
│   ├── copper
│   ├── brass_bronze
│   └── zinc_galvanized
├── glass
│   ├── single_glazing
│   ├── double_glazing
│   ├── triple_glazing
│   ├── safety_glass
│   ├── fire_rated_glass
│   └── glass_block
├── polymer
│   ├── pvc
│   ├── pe
│   ├── pp
│   ├── epdm
│   ├── polycarbonate
│   └── acrylic
├── composite
│   ├── aluminium_composite_panel
│   ├── fibre_cement
│   ├── wood_plastic_composite
│   ├── sandwich_panel
│   └── laminate
└── mixed_unknown
    ├── mixed_lot
    ├── unknown_material
    └── requires_assessment
```

---

## 8. Kontrollierte Vokabulare

### `source_platform`

```text
ibs
useagain
salza
concular
restado
bauteilboerse_basel
bauteilboerse_bremen
bauteilladen_winterthur
bauteilnetz_deutschland
materialnomaden
baukarussell
cirkla
madaster
other
```

### `page_status`

```text
live
live_restricted
archived
redirected
not_found
requires_login
unknown
```

### `data_source_type`

```text
marketplace_listing
technical_inventory
pre_demolition_audit
physical_store_catalogue
auction_listing
intake_form
pdf_factsheet
cad_file
bim_model
material_passport
test_report
manual_entry
```

### `availability_status`

```text
available
available_soon
reserved
partially_available
sold
out_of_stock
expired
stale_listing
project_restricted
on_request
unknown
```

### `condition_normalized`

```text
new
new_old_stock
like_new
used_good
used_light_wear
used_heavy_wear
damaged_repairable
damaged_not_ready
untested
unknown
```

### `risk_level`

```text
low
medium
high
critical
unknown
```

### `hazard_flags`

```text
asbestos
pcb
pah
lead_paint
kmf_mineral_wool
chlorides
hydrocarbons
mold
corrosion
moisture_damage
fire_damage
biological_damage
structural_uncertainty
missing_certification
unknown_pollutants
none_known
```

### `deconstruction_status`

```text
still_installed
dismantling_planned
being_dismantled
dismantled
stored_on_site
stored_in_warehouse
in_shop
unknown
```

### `demounting_responsibility`

```text
buyer
seller
platform
demolition_contractor
reuse_contractor
self_demount
not_applicable
unknown
```

### `transport_mode`

```text
pickup_only
delivery_available
shipping_available
freight_required
local_delivery_only
self_organized
unknown
```

### `price_type`

```text
fixed
negotiable
price_on_request
auction
free
donation
included_in_service
unknown
```

### `quantity_unit`

```text
piece
lot
set
pair
linear_m
m2
m3
kg
tonne
pallet
package
roll
unknown
```

### `reuse_confidence_score`

```text
A_procurement_ready
B_design_ready
C_investigation_only
D_stale_or_risky
```

| Score | Bedeutung |
|---|---|
| `A_procurement_ready` | Bestand, Preis, Standort, Zustand, Logistik und Bedingungen sind klar |
| `B_design_ready` | Maße, Menge, Fotos/Zeichnungen und technisches Potenzial sind klar; Beschaffung oder Prüfung noch offen |
| `C_investigation_only` | Interessantes Material, aber Preis, Bestand, Zustand, Tests oder Logistik fehlen |
| `D_stale_or_risky` | Alte Anzeige, unsichere Verfügbarkeit, Schadstoffrisiko oder fehlende Prüfdaten |

### `recommended_next_action`

```text
contact_seller
reserve_item
request_photos
request_drawings
request_test_report
request_pollutant_test
request_structural_review
check_availability
visit_site
estimate_transport
archive_listing
reject_item
```

---

## 9. Minimale Datenbankstruktur

```text
items
listings
variant_batches
locations
provenance
availability_snapshots
conditions
risk_assessments
logistics
documentation_assets
environmental_data
reuse_assessments
technical_attributes
controlled_vocabularies
```

### Pflichtfelder für Version 1

```text
item_id
canonical_title
component_family
component_type
material_family
primary_material
structural_role
listing_id
source_platform
source_url
page_status
availability_status
quantity_available
quantity_unit
price_amount
currency
condition_normalized
risk_level
hazard_flags
reuse_confidence_score
last_verified_at
```

---

## 10. Beispiel

```json
{
  "item": {
    "item_id": "item-001",
    "canonical_title": "Rippenplatte aus Spannbeton",
    "component_family": "structure",
    "component_type": "slab",
    "material_family": "mineral",
    "primary_material": "prestressed_concrete",
    "structural_role": "load_bearing"
  },
  "listing": {
    "listing_id": "listing-001",
    "source_platform": "ibs",
    "source_url": "https://example.com/component/001",
    "page_status": "live_restricted"
  },
  "availability_snapshot": {
    "checked_at": "2026-06-14",
    "availability_status": "project_restricted",
    "quantity_available": 24,
    "quantity_unit": "piece"
  },
  "technical_attribute": {
    "attribute_group": "structural_concrete",
    "attribute_name": "compressive_strength",
    "value_number": 67.4,
    "unit": "MPa",
    "confidence": "medium"
  },
  "reuse_assessment": {
    "reuse_confidence_score": "B_design_ready",
    "recommended_next_action": "check_availability"
  }
}
```
