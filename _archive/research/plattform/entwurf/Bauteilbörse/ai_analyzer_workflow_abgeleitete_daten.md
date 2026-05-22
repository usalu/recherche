# AI-Analyzer → Reclaimed-Material-System: Workflow mit abgeleiteten Daten

## Ziel

Dieses Dokument beschreibt, wie ein AI-Bild-/Text-Analyzer Daten aus unterschiedlichen Eingaben in ein Reclaimed-Material-System überführt.

Der wichtigste zusätzliche Schritt ist **Abgeleitete Daten**:  
Dort werden aus den extrahierten Informationen plausible technische, planerische, energetische und logistische Werte berechnet oder geschätzt.

---

## 0. Einheitlicher Ablauf

```text
1. Input erfassen
2. DocumentationAsset speichern
3. RawExtraction erzeugen
4. Normalisieren
5. Abgeleitete Daten berechnen
6. Klassifizieren
7. Schema-Mapping
8. Validieren
9. Review-Status setzen
10. Datenbank schreiben
11. ReuseAssessment aktualisieren
```

**Wichtig:**  
Abgeleitete Daten sind keine verifizierten Fakten. Sie müssen immer mit `source = derived`, `formula`, `confidence` und `review_status` gespeichert werden.

```yaml
derived_value:
  value: 10225.8
  unit: cm2
  source: derived
  formula: length_mm * width_mm
  confidence: medium
  review_status: unverified
```

---

# 1. Szenario A — Projekt mit reichen Daten

## Beispiel

```text
IBS-Bauteilkatalog
Rippenplatte Stahlbeton / L=6.84m, B=1.495m
https://bauteile-ibs.ch/components/90-rippenplatte-stahlbeton-l684m-b1495m
```

## Input-Typen

```text
listing_url
html_listing
images
pdf_factsheet_de
pdf_factsheet_en
dwg_file
print_pdf
```

## 1.1 Raw Extraction

```yaml
title: Rippenplatte Stahlbeton / L=6.84m, B=1.495m
component_raw: Rippenplatte
material_raw: Stahlbeton / Spannbeton
length: 6.84 m
width: 1.495 m
height: 0.48 m
quantity: 188 Stück
co2_new_component_kg: 908
co2_reuse_component_kg: -635
compressive_strength: 67.4 N/mm2
carbonation_depth: 21 mm
deconstruction_method: Diamantsäge
risk_notes:
  - Chloride prüfen
  - Korrosion prüfen
  - Feuchtigkeit prüfen
  - Kohlenwasserstoffe prüfen
  - Asbest/PCB ungeklärt
```

## 1.2 Normalisierung

```yaml
length_mm: 6840
width_mm: 1495
height_mm: 480
quantity_unit: piece
compressive_strength_mpa: 67.4
```

## 1.3 Abgeleitete Daten

### Geometrie und Planung

```yaml
plan_area_per_unit_m2: 10.226
total_plan_area_m2: 1922.5
total_linear_length_m: 1285.9
module_width_m: 1.495
module_length_m: 6.84
probable_design_grid: 1.50m module width
probable_span_direction: length direction, needs verification
```

### Volumen und Gewicht

```yaml
bounding_box_volume_per_unit_m3: 4.908
bounding_box_volume_total_m3: 922.8
max_geometric_mass_per_unit_kg:
  value: 12271
  assumption: reinforced_concrete_density_2500kg_m3
  warning: not actual mass because ribbed slab has voids/ribs
max_geometric_mass_total_t:
  value: 2306.9
  warning: upper-bound only, not for transport planning without actual volume
```

### Tragwerksplanung

```yaml
derived_structural_use:
  - reusable as slab element only after structural verification
  - concrete strength suggests high-strength concrete, but reinforcement/prestress layout controls capacity
  - carbonation depth 21mm indicates durability check needed
  - support condition and cutting damage must be checked
missing_for_structural_calculation:
  - exact cross-section/rib geometry
  - reinforcement layout
  - prestressing data
  - bearing detail
  - crack/spalling map
  - actual self-weight
  - load history
  - deconstruction damage
```

### Umwelt / CO2

```yaml
co2_delta_vs_new_per_unit_kg:
  value: 1543
  formula: 908 - (-635)
co2_delta_vs_new_total_kg:
  value: 290084
  equivalent_tonnes: 290.1
co2_new_total_kg: 170704
co2_reuse_total_kg: -119380
```

### Reuse-Relevanz

```yaml
design_relevance:
  - strong candidate for early design because dimensions and quantity are clear
  - useful for modular floor layouts around 1.495m width
  - high documentation value because PDF/CAD/factsheet exist
reuse_risk:
  - structural approval required
  - pollutant testing required
  - availability/project restriction must be confirmed
```

## 1.4 Klassifikation

```yaml
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
newness_type: reclaimed
data_source_type: technical_inventory
```

## 1.5 Schema-Mapping

```yaml
Item:
  canonical_title: Rippenplatte aus Spannbeton
  component_family: structure
  component_type: slab
  material_family: mineral
  primary_material: prestressed_concrete
  structural_role: load_bearing

Listing:
  source_platform: ibs
  source_url: https://bauteile-ibs.ch/components/90-rippenplatte-stahlbeton-l684m-b1495m
  page_status: live_restricted
  data_confidence: high

VariantBatch:
  quantity: 188
  quantity_unit: piece
  length_mm: 6840
  width_mm: 1495
  height_mm: 480

RiskAssessment:
  risk_level: high
  structural_verification_required: true
  pollutant_test_status: partial_test

ReuseAssessment:
  reuse_confidence_score: B_design_ready
  recommended_next_action:
    - check_availability
    - request_structural_review
    - request_pollutant_test
```

---

# 2. Szenario B — Wenige Bilder + Beschreibung

## Beispiel

Screenshot eines Inserats:

```text
Stahlträger HEB 140 – Länge 2,54m
Artikel-Nr.: #201605
Zustand: Neu
Bauteil: Stahlträger
Beschreibung: Neuer, noch nie verbauter Stahlträger HEB 140,
inkl. Unterlegbleche der Mauerwerks- und Balkenauflager.
```

## Input-Typen

```text
screenshot
image_gallery
visible_listing_text
```

## 2.1 Raw Extraction

```yaml
title: Stahlträger HEB 140 – Länge 2,54m
article_number: "#201605"
component_raw: Stahlträger
profile_raw: HEB 140
length: 2.54 m
condition_raw: Neu, noch nie verbaut
included_parts: Unterlegbleche der Mauerwerks- und Balkenauflager
quantity: unknown
price: unknown
location: unknown
```

## 2.2 Normalisierung

```yaml
length_mm: 2540
component_type: beam
profile_type: HEB
section_size: "140"
condition_normalized: new
```

## 2.3 Abgeleitete Daten

### Geometrie und Standardprofil

```yaml
standard_profile_guess:
  profile: HEB 140
  height_mm: 140
  width_mm: 140
  source: derived_from_profile_name
  confidence: medium
  warning: verify with steel table or supplier datasheet
```

### Gewicht und Transport

```yaml
estimated_mass_per_m_kg:
  value: 33.7
  assumption: typical HEB 140 table mass
  confidence: medium
estimated_mass_per_piece_kg:
  value: 85.6
  formula: 2.54m * 33.7kg/m
estimated_steel_volume_m3:
  value: 0.0109
  formula: profile_area_43cm2 * 2.54m
handling_note:
  - likely too heavy for one person
  - possible manual handling with 2-3 people or lifting aid
```

### Tragwerksplanung

```yaml
structural_use:
  - short steel beam or lintel candidate
  - useful for masonry or timber bearing situations
  - bearing plates are relevant for load distribution
missing_for_structural_calculation:
  - steel grade, e.g. S235 or S355
  - exact profile table values
  - support conditions
  - corrosion condition
  - hole/cut/weld modifications
  - fire protection requirement
  - intended span and load case
```

### Plausibilitätswerte, nicht für finale Statik

```yaml
approx_cross_section_area_cm2:
  value: 43.0
  assumption: typical HEB 140 table value
approx_axial_yield_capacity_s235_kN:
  value: 1010
  formula: 4300mm2 * 235N/mm2
  warning: no safety factors, no buckling, not design-ready
approx_axial_yield_capacity_s355_kN:
  value: 1526
  formula: 4300mm2 * 355N/mm2
  warning: no safety factors, no buckling, not design-ready
```

### Energie / CO2

```yaml
co2_calculation_possible:
  formula: estimated_mass_kg * steel_emission_factor_kgco2e_per_kg
  estimated_mass_kg: 85.6
  missing:
    - chosen emission factor
    - reuse transport distance
    - surface treatment effort
```

### Reuse-Relevanz

```yaml
design_relevance:
  - useful for short-span structural reuse
  - profile name gives strong starting point for structural lookup
  - image suggests surface oxidation may exist despite condition "new"
reuse_risk:
  - exact availability unknown
  - price unknown
  - quantity unknown
  - steel grade unknown
  - structural documentation missing
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

## 2.5 Schema-Mapping

```yaml
Item:
  canonical_title: Stahlträger HEB 140
  component_family: structure
  component_type: beam
  material_family: metal
  primary_material: steel
  structural_role: load_bearing
  newness_type: overstock

Listing:
  external_article_number: "#201605"
  original_title: Stahlträger HEB 140 – Länge 2,54m
  data_source_type: marketplace_listing
  data_confidence: medium

VariantBatch:
  length_mm: 2540
  quantity: null
  quantity_unit: piece
  dimension_notes: HEB 140 profile; exact cross-section should be verified

RiskAssessment:
  risk_level: medium
  hazard_flags:
    - structural_uncertainty
    - missing_certification
  structural_verification_required: true

ReuseAssessment:
  reuse_confidence_score: C_investigation_only
  recommended_next_action:
    - request_full_listing_url
    - check_availability
    - request_price
    - request_stock_quantity
    - request_steel_grade
    - request_structural_review
```

---

# 3. Szenario C — Nur Prompt / Textbeschreibung

## Beispiel-Prompt

```text
Alte Holzbalken aus laufender Altbausanierung, ca. 160 Jahre alt, 10 Stück.
Querschnitt meistens 18x18 bis 20x22 cm, maximal 22x22 cm.
Länge ca. 1 bis 6 Meter.
Teilweise mit zweiseitiger fränkischer Kerbe, sehr trocken und kann alleine getragen werden.
Gebraucht, roh und unbehandelt, Oberfläche gesägt und geschlagen.
Historisch, sehr gut erhalten, rustikaler Look.
Höhe und Breite ca. 180–220 mm.
Preis je nach Länge: 20.
```

## Input-Typen

```text
user_prompt
free_text_description
no_images
no_url
no_documents
```

## 3.1 Raw Extraction

```yaml
component_raw: alte Holzbalken
source_context: laufende Altbausanierung
estimated_age: ca. 160 Jahre
quantity: 10 Stück
cross_section_range: 18x18 bis 20x22 cm
max_cross_section: 22x22 cm
length_range: 1 bis 6 m
special_feature: teilweise zweiseitige fränkische Kerbe
condition_raw: gebraucht, roh, unbehandelt, sehr trocken, sehr gut erhalten
surface: gesägt und geschlagen
look: historisch, rustikal
price_raw: 20, je nach Länge
```

## 3.2 Normalisierung

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
price_amount: 20
currency: unknown
price_unit: unknown
```

## 3.3 Abgeleitete Daten

### Geometrie und Mengen

```yaml
total_linear_length_min_m: 10.0
total_linear_length_max_m: 60.0
total_linear_length_mid_estimate_m: 35.0

cross_section_area_min_m2:
  value: 0.0324
  formula: 0.18m * 0.18m
cross_section_area_max_m2:
  value: 0.0484
  formula: 0.22m * 0.22m
cross_section_area_mid_estimate_m2:
  value: 0.0400
  formula: 0.20m * 0.20m
```

### Volumen und Gewicht

```yaml
timber_volume_min_m3:
  value: 0.324
  formula: 10m total length * 0.0324m2
timber_volume_max_m3:
  value: 2.904
  formula: 60m total length * 0.0484m2
timber_volume_mid_estimate_m3:
  value: 1.400
  formula: 35m total length * 0.04m2

estimated_weight_per_m_min_kg:
  value: 14.6
  assumption: density 450kg/m3, section 18x18cm
estimated_weight_per_m_max_kg:
  value: 31.5
  assumption: density 650kg/m3, section 22x22cm
estimated_weight_per_m_mid_kg:
  value: 22.0
  assumption: density 550kg/m3, section 20x20cm

estimated_total_weight_min_kg: 146
estimated_total_weight_max_kg: 1888
estimated_total_weight_mid_kg: 770
```

### Tragwerksplanung

```yaml
structural_reuse_potential:
  - possible as visible secondary beams or decorative structural elements
  - primary load-bearing reuse only after grading and engineer review
  - fränkische Kerben reduce effective section and must be measured
  - age and dryness are positive for stability but not enough for structural approval
missing_for_structural_calculation:
  - wood species
  - strength class
  - moisture content
  - exact dimensions per beam
  - exact length per beam
  - notch geometry and position
  - insect damage
  - fungal damage
  - cracks and checks
  - previous load history
```

### Preislogik

```yaml
price_interpretation_uncertain:
  raw_price: 20
  possible_price_per_piece_total:
    value: 200
    formula: 10 pieces * 20
  possible_price_per_linear_meter_range:
    min_value: 200
    max_value: 1200
    formula: 10-60 linear meters * 20
  possible_price_per_linear_meter_mid:
    value: 700
    formula: 35 linear meters * 20
  missing:
    - currency
    - unit, piece or linear meter
    - whether price varies by exact length
```

### Design / Atmosphäre / Reuse

```yaml
design_relevance:
  - high visual reuse value
  - suitable for rustic interiors, visible beams, furniture, cladding, non-structural installations
  - historic character is a design asset
  - raw untreated surface allows flexible finishing
reuse_risk:
  - no images
  - no location
  - no exact dimensions per piece
  - no wood species
  - biological damage unknown
  - structural classification unknown
```

### Energie / CO2

```yaml
co2_calculation_possible:
  formula: estimated_timber_volume_m3 * timber_emission_or_storage_factor
  usable_volume_range_m3: "0.324–2.904"
  midpoint_volume_m3: 1.400
  missing:
    - wood species
    - density confirmation
    - LCA factor
    - transport distance
    - reconditioning effort
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

## 3.5 Schema-Mapping

```yaml
Item:
  canonical_title: Historische Holzbalken aus Altbausanierung
  component_family: structure
  component_type: beam
  material_family: timber_biobased
  primary_material: solid_timber
  newness_type: reclaimed
  structural_role: unknown_or_potentially_load_bearing

VariantBatch:
  quantity: 10
  quantity_unit: piece
  length_min_mm: 1000
  length_max_mm: 6000
  width_min_mm: 180
  width_max_mm: 220
  height_min_mm: 180
  height_max_mm: 220

TechnicalAttribute:
  attribute_group: timber
  estimated_age_years: 160
  wood_species: unknown
  solid_or_engineered: solid_timber
  surface_finish: raw_untreated
  moisture_condition: very_dry
  joinery_detail: two-sided_franconian_notch_partial

AvailabilitySnapshot:
  availability_status: on_request
  quantity_available: 10
  price_amount: 20
  currency: unknown
  price_unit: unknown

RiskAssessment:
  risk_level: medium
  hazard_flags:
    - biological_damage_unknown
    - structural_uncertainty
    - missing_certification
  structural_verification_required: true

ReuseAssessment:
  reuse_confidence_score: C_investigation_only
  recommended_next_action:
    - request_photos
    - request_exact_dimensions_per_piece
    - request_location
    - clarify_price_unit
    - request_wood_species
    - inspect_for_insect_damage
    - inspect_for_fungal_damage
```

---

# 4. Vergleich

| Szenario | Datenlage | Abgeleitete Datenqualität | Hauptnutzen | Hauptrisiko | Score |
|---|---|---|---|---|---|
| A: Reiche Projektdaten | URL + PDF + Bilder + CAD | Hoch | Planung, Vorbemessung, CO2, Mengen | Verfügbarkeit, Statik, Schadstoffe | `B_design_ready` |
| B: Screenshot + Text | Bild + sichtbarer Text | Mittel | Profil, Gewicht, kurzer Bauteil-Check | Stahlgüte, Preis, Menge fehlen | `C_investigation_only` |
| C: Nur Prompt | Freitext | Niedrig bis mittel | Mengen-/Volumen-/Preis-Szenarien | Keine Belege, Holzqualität unbekannt | `C_investigation_only` |

---

# 5. Review-Regeln für abgeleitete Daten

Ein menschliches Review ist erforderlich, wenn:

```text
confidence < 0.75
structural_role = load_bearing
value_source = derived and used_for_structural_calculation = true
price_unit = unknown
quantity_available = unknown
dimensions are estimated or given as range
hazard_flags contains unknown_pollutants
source_url is missing
image and text contradict each other
standard table values are assumed but not verified
```

---

# 6. Speicherung abgeleiteter Daten

Abgeleitete Daten sollten nicht normale Rohdaten überschreiben.  
Sie werden als eigene Felder oder `TechnicalAttribute` mit Herkunft gespeichert.

```yaml
derived_data_record:
  item_id: item-001
  field_name: estimated_mass_per_piece_kg
  value: 85.6
  unit: kg
  formula: length_m * estimated_mass_per_m
  source: derived
  based_on:
    - length_mm
    - profile_type
  confidence: medium
  verified_status: unverified
  usable_for_design: preliminary_only
```

---

# 7. Wichtigste Design-Regel

Der Analyzer erzeugt:

```text
Beobachtete Daten
+ normalisierte Daten
+ abgeleitete Daten
+ Unsicherheit
+ Review-Bedarf
```

Nicht:

```text
finale Statik
finale Energie-/CO2-Bilanz
finale Beschaffungsentscheidung
```

Für Reuse ist der wichtigste Mehrwert nicht nur „was ist vorhanden“, sondern:

```text
Was kann man daraus planerisch ableiten?
Was fehlt für die Nutzung?
Wie riskant ist die Annahme?
Welche nächste Prüfung ist nötig?
```
