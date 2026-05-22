# AI-Analyzer → Reclaimed-Material-System: Workflow-Beispiele

## Ziel

Dieses Dokument beschreibt kompakt, wie Daten aus einem AI-Bild-/Text-Analyzer in ein Reclaimed-Material-System gemappt werden.

Der Analyzer erzeugt nicht direkt finale Wahrheit, sondern **belegte Vorschläge** mit Quelle, Konfidenz und Review-Status.

```text
Input
→ DocumentationAsset speichern
→ RawExtraction erzeugen
→ Normalisieren
→ Klassifizieren
→ Abgeleitete Daten erzeugen
→ Schema-Mapping
→ Validieren
→ Review-Status setzen
→ Datenbank schreiben
→ ReuseAssessment aktualisieren
```

---

## Grundregel für „Abgeleitete Daten“

**Abgeleitete Daten** sind Informationen, die nicht explizit im Input stehen, aber aus Kontext, Bauteiltyp, Material, Marktlogik oder Bauwissen plausibel geschlossen werden können.

Sie dürfen nie als verifizierte Fakten gespeichert werden.

Jedes abgeleitete Feld braucht:

```text
derived: true
confidence: low | medium | high
reasoning_source: image_context | text_context | material_logic | category_rule | market_pattern
review_required: true | false
```

Beispiel:

```yaml
field: structural_verification_required
value: true
derived: true
confidence: high
reasoning_source: category_rule
review_required: true
```

---

# 1. Szenario A: Projekt mit reichen Daten

## Beispiel

IBS-Bauteilkatalog:

```text
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

## Schritt 1 — Quellen speichern

```yaml
documentation_assets:
  - asset_type: marketplace_listing
  - asset_type: image
  - asset_type: pdf_factsheet
  - asset_type: cad_file
  - asset_type: print_pdf
```

## Schritt 2 — RawExtraction

```yaml
title_raw: Rippenplatte Stahlbeton / L=6.84m, B=1.495m
component_raw: Rippenplatte
material_raw: Stahlbeton / Spannbeton
length_raw: 6.84 m
width_raw: 1.495 m
height_raw: 48 cm
quantity_raw: 188 Stück
co2_new_raw: 908 kg/Stk
co2_reuse_raw: -635 kg/Stk
carbonation_depth_raw: 21 mm
compressive_strength_raw: 67.4 N/mm2
deconstruction_tool_raw: Diamantsäge
risk_raw:
  - Chloride
  - Korrosion
  - Feuchtigkeit
  - Kohlenwasserstoffe
  - Asbest/PCB ungeklärt
```

## Schritt 3 — Normalisierung

```yaml
length_mm: 6840
width_mm: 1495
height_mm: 480
quantity: 188
quantity_unit: piece
compressive_strength_mpa: 67.4
```

## Schritt 4 — Klassifikation

```yaml
component_family: structure
component_type: slab
component_subtype: ribbed_slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
newness_type: reclaimed
data_source_type: technical_inventory
```

## Schritt 5 — Abgeleitete Daten

Diese Daten werden aus Bauteiltyp, Material, Quelle und Kontext abgeleitet. Sie sind **nicht automatisch verifiziert**.

```yaml
derived_data:
  likely_use_cases:
    value:
      - reuse_as_structural_floor_slab
      - reuse_as_non_structural_platform_or_landscape_element
      - reuse_as_heavy_precast_component
    confidence: medium
    reasoning_source: category_rule
    review_required: true

  procurement_complexity:
    value: high
    confidence: high
    reasoning_source: material_logic
    reason: Tragendes Betonfertigteil mit hohem Gewicht, Rückbau- und Transportaufwand.
    review_required: true

  handling_requirements:
    value:
      - crane_likely_required
      - heavy_transport_required
      - lifting_plan_required
      - storage_on_hard_surface_required
    confidence: medium
    reasoning_source: material_logic
    review_required: true

  verification_needs:
    value:
      - structural_engineer_review
      - pollutant_testing
      - connection_detail_review
      - crack_and_spalling_inspection
      - lifting_point_assessment
    confidence: high
    reasoning_source: category_rule
    review_required: true

  likely_missing_data:
    value:
      - final_availability_confirmation
      - reservation_status
      - exact_pickup_window
      - transport_cost
      - reuse_design_load_case
      - legal_release_for_third_party_use
    confidence: high
    reasoning_source: source_context
    review_required: true

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

  suggested_market_segment:
    value:
      - architects_with_reuse_project
      - structural_engineers
      - public_or_large_scale_reuse_projects
      - landscape_or_infrastructure_reuse
    confidence: medium
    reasoning_source: market_pattern
    review_required: false

  expected_data_quality:
    value: technically_rich_but_procurement_uncertain
    confidence: high
    reasoning_source: source_context
    review_required: false
```

## Schritt 6 — Schema-Mapping

### `Item`

```yaml
canonical_title: Rippenplatte aus Spannbeton
component_family: structure
component_type: slab
component_subtype: ribbed_slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
newness_type: reclaimed
```

### `Listing`

```yaml
source_platform: ibs
source_url: https://bauteile-ibs.ch/components/90-rippenplatte-stahlbeton-l684m-b1495m
page_status: live_restricted
data_source_type: technical_inventory
data_confidence: high
```

### `VariantBatch`

```yaml
quantity: 188
quantity_unit: piece
length_mm: 6840
width_mm: 1495
height_mm: 480
```

### `TechnicalAttribute`

```yaml
attribute_group: structural_concrete
compressive_strength_mpa: 67.4
carbonation_depth_mm: 21
prestressed: true
cutting_required: true
```

### `RiskAssessment`

```yaml
risk_level: high
hazard_flags:
  - chlorides
  - corrosion
  - moisture_damage
  - hydrocarbons
  - unknown_pollutants
  - structural_uncertainty
structural_verification_required: true
pollutant_test_status: partial_test
```

### `EnvironmentalData`

```yaml
co2_new_component_kg: 908
co2_reuse_component_kg: -635
environmental_data_confidence: medium
```

### `ReuseAssessment`

```yaml
reuse_confidence_score: B_design_ready
recommended_next_action:
  - check_availability
  - request_structural_review
  - request_pollutant_test
```

---

# 2. Szenario B: Wenige Bilder + Beschreibung

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

## Schritt 1 — Quellen speichern

```yaml
documentation_assets:
  - asset_type: image
    file_format: png
    extraction_method: ai_visual_ocr
```

## Schritt 2 — RawExtraction

```yaml
title_raw: Stahlträger HEB 140 – Länge 2,54m
article_number_raw: "#201605"
condition_raw: Neu
component_raw: Stahlträger
profile_raw: HEB 140
length_raw: 2.54 m
accessories_raw: Unterlegbleche
quantity_raw: not_visible
price_raw: not_visible
location_raw: not_visible
```

## Schritt 3 — Normalisierung

```yaml
length_mm: 2540
component_type: beam
profile_type: HEB
section_size: "140"
condition_normalized: new
```

## Schritt 4 — Klassifikation

```yaml
component_family: structure
component_type: beam
component_subtype: steel_beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
data_source_type: marketplace_listing
```

## Schritt 5 — Abgeleitete Daten

```yaml
derived_data:
  likely_use_cases:
    value:
      - small_structural_beam
      - lintel_or_support_beam
      - renovation_support_element
      - secondary_steel_structure
    confidence: medium
    reasoning_source: component_profile
    review_required: true

  procurement_complexity:
    value: medium
    confidence: medium
    reasoning_source: material_logic
    reason: Stahlträger ist kleiner als große Betonfertigteile, aber statisch relevant.
    review_required: true

  handling_requirements:
    value:
      - two_person_or_machine_handling_likely
      - corrosion_check_required
      - storage_dry_recommended
      - transport_by_van_or_small_truck_possible
    confidence: medium
    reasoning_source: image_context
    review_required: true

  likely_missing_data:
    value:
      - quantity_available
      - price
      - seller_contact
      - pickup_location
      - steel_grade
      - exact_weight
      - certificates_or_material_spec
      - full_listing_url
    confidence: high
    reasoning_source: visible_listing_gap
    review_required: true

  verification_needs:
    value:
      - measure_actual_length
      - verify_profile_HEB_140
      - check_steel_grade
      - check_corrosion_or_storage_marks
      - structural_engineer_review_if_load_bearing
    confidence: high
    reasoning_source: category_rule
    review_required: true

  possible_condition_interpretation:
    value: new_old_stock_or_overstock
    confidence: medium
    reasoning_source: text_context
    reason: Text says new and never installed, but visible surface oxidation/storage marks may exist.
    review_required: true

  reuse_barriers:
    value:
      - missing_steel_grade
      - missing_quantity
      - missing_price
      - structural_liability
      - unknown_storage_history
    confidence: medium
    reasoning_source: marketplace_pattern
    review_required: true

  expected_data_quality:
    value: visually_supported_but_commercially_incomplete
    confidence: high
    reasoning_source: input_type
    review_required: false
```

## Schritt 6 — Schema-Mapping

### `Item`

```yaml
canonical_title: Stahlträger HEB 140
component_family: structure
component_type: beam
component_subtype: steel_beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
```

### `Listing`

```yaml
external_article_number: "#201605"
original_title: Stahlträger HEB 140 – Länge 2,54m
data_source_type: marketplace_listing
data_confidence: medium
```

### `VariantBatch`

```yaml
length_mm: 2540
quantity: null
quantity_unit: piece
dimension_notes: HEB 140 profile; exact cross-section and steel grade should be verified.
```

### `TechnicalAttribute`

```yaml
attribute_group: metal_steel
profile_type: HEB
section_size: "140"
accessory_list: Unterlegbleche für Mauerwerks- und Balkenauflager
```

### `Condition`

```yaml
condition_raw: Neu, noch nie verbaut
condition_normalized: new
inspection_method: ai_visual_ocr
```

### `RiskAssessment`

```yaml
risk_level: medium
hazard_flags:
  - structural_uncertainty
  - missing_certification
structural_verification_required: true
pollutant_test_status: unknown
```

### `ReuseAssessment`

```yaml
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

# 3. Szenario C: Nur Prompt / Textbeschreibung

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

## Schritt 1 — Quelle speichern

```yaml
documentation_assets:
  - asset_type: manual_entry
    data_source_type: user_prompt
    extraction_method: text_parser
```

## Schritt 2 — RawExtraction

```yaml
component_raw: alte Holzbalken
origin_raw: laufende Altbausanierung
age_raw: ca. 160 Jahre
quantity_raw: 10 Stück
section_raw: 18x18 bis 20x22 cm, maximal 22x22 cm
length_raw: 1 bis 6 m
special_feature_raw: zweiseitige fränkische Kerbe
moisture_raw: sehr trocken
condition_raw: gebraucht, sehr gut erhalten
surface_raw: roh, unbehandelt, gesägt und geschlagen
style_raw: historisch, rustikal
price_raw: 20 je nach Länge
```

## Schritt 3 — Normalisierung

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

## Schritt 4 — Klassifikation

```yaml
component_family: structure
component_type: beam
component_subtype: timber_beam
material_family: timber_biobased
primary_material: solid_timber
structural_role: unknown_or_potentially_load_bearing
newness_type: reclaimed
data_source_type: user_prompt
```

## Schritt 5 — Abgeleitete Daten

```yaml
derived_data:
  likely_use_cases:
    value:
      - decorative_exposed_beam
      - interior_feature
      - furniture_or_joinery
      - non_structural_reuse
      - structural_reuse_only_after_engineering_review
    confidence: high
    reasoning_source: text_context
    review_required: true

  likely_market_appeal:
    value: high_for_historic_rustic_design
    confidence: medium
    reasoning_source: market_pattern
    reason: Historic age, rustic look and untreated surface are desirable for interior reuse.
    review_required: false

  procurement_complexity:
    value: low_to_medium
    confidence: medium
    reasoning_source: text_context
    reason: Text says the beams can be carried by one person, but lengths vary up to 6 m.
    review_required: true

  handling_requirements:
    value:
      - manual_handling_possible_for_shorter_pieces
      - long_pieces_need_two_people_or_vehicle
      - dry_storage_required
      - protect_from_moisture
      - individual_labeling_recommended
    confidence: medium
    reasoning_source: material_logic
    review_required: true

  likely_missing_data:
    value:
      - photos
      - exact_dimensions_per_beam
      - wood_species
      - location
      - price_currency
      - price_unit
      - insect_damage_status
      - fungal_damage_status
      - load_history
      - nails_or_metal_contamination
    confidence: high
    reasoning_source: prompt_gap
    review_required: true

  verification_needs:
    value:
      - request_photos
      - measure_each_piece
      - inspect_for_insects
      - inspect_for_fungal_damage
      - check_cracks_and_splitting
      - check_metal_fasteners
      - clarify_if_structural_reuse_is_intended
    confidence: high
    reasoning_source: category_rule
    review_required: true

  possible_condition_interpretation:
    value: used_good_but_unverified
    confidence: medium
    reasoning_source: user_description
    reason: User describes very good condition, but there are no images or inspection data.
    review_required: true

  reuse_barriers:
    value:
      - unknown_wood_species
      - no_visual_evidence
      - no_precise_piece_schedule
      - biological_damage_unknown
      - structural_certification_missing
      - unclear_price_unit
    confidence: high
    reasoning_source: prompt_gap
    review_required: true

  suggested_data_collection_template:
    value:
      - beam_id
      - length_mm
      - width_mm
      - height_mm
      - weight_or_carryability
      - notch_present
      - crack_level
      - insect_holes
      - moisture_condition
      - nails_or_metal_present
      - photo_each_side
    confidence: high
    reasoning_source: category_rule
    review_required: false

  expected_data_quality:
    value: conceptually_rich_but_unverified
    confidence: high
    reasoning_source: input_type
    review_required: false
```

## Schritt 6 — Schema-Mapping

### `Item`

```yaml
canonical_title: Historische Holzbalken aus Altbausanierung
component_family: structure
component_type: beam
component_subtype: timber_beam
material_family: timber_biobased
primary_material: solid_timber
newness_type: reclaimed
structural_role: unknown_or_potentially_load_bearing
short_description: Alte, trockene Holzbalken mit rustikaler Oberfläche und teilweise fränkischer Kerbe.
```

### `VariantBatch`

```yaml
quantity: 10
quantity_unit: piece
length_min_mm: 1000
length_max_mm: 6000
width_min_mm: 180
width_max_mm: 220
height_min_mm: 180
height_max_mm: 220
dimension_notes: Querschnitte variieren; Einzelmaße je Balken erforderlich.
```

### `TechnicalAttribute`

```yaml
attribute_group: timber
estimated_age_years: 160
wood_species: unknown
solid_or_engineered: solid_timber
surface_finish: raw_untreated
moisture_condition: very_dry
joinery_detail: two-sided_franconian_notch_partial
```

### `Condition`

```yaml
condition_raw: gebraucht, roh, unbehandelt, sehr trocken, sehr gut erhalten
condition_normalized: used_good
wear_level: used_light_wear
inspection_method: user_description
```

### `AvailabilitySnapshot`

```yaml
availability_status: on_request
quantity_available: 10
quantity_unit: piece
price_amount: 20
currency: unknown
price_unit: unknown
price_type: unclear
```

### `RiskAssessment`

```yaml
risk_level: medium
hazard_flags:
  - biological_damage_unknown
  - structural_uncertainty
  - missing_certification
pollutant_test_status: not_tested
structural_verification_required: true
```

### `ReuseAssessment`

```yaml
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

# 4. Vergleich der Szenarien

| Szenario | Datenlage | Extrahierte Daten | Abgeleitete Daten | Hauptlücken | Score |
|---|---|---|---|---|---|
| A: Reiche Projektdaten | URL + PDF + Bilder + CAD | Sehr stark | Logistik, Prüfbedarf, Marktsegment, Wiederverwendungsbarrieren | Live-Verfügbarkeit, finale Freigabe | `B_design_ready` |
| B: Screenshot + Beschreibung | Bild + sichtbarer Text | Mittel | Einsatzmöglichkeiten, fehlende Felder, Handling, Prüfbedarf | Preis, Menge, Standort, Link, Stahlgüte | `C_investigation_only` |
| C: Nur Prompt | Freitext | Niedrig bis mittel | Marktattraktivität, Risiken, Datenerhebungsvorlage, Prüfbedarf | Fotos, Belege, Einzelmaße, Standort, Holzart | `C_investigation_only` |

---

# 5. Einheitlicher Mapping-Prozess

```text
1. Input speichern
2. RawExtraction erzeugen
3. Werte normalisieren
4. Bauteil und Material klassifizieren
5. Abgeleitete Daten erzeugen
6. Universelle Felder mappen
7. Kategorie-Attributpaket aktivieren
8. Fehlende Felder markieren
9. Risiko- und Review-Regeln ausführen
10. ReuseAssessment berechnen
11. In Datenbank schreiben
```

---

# 6. Review-Regeln

Ein menschliches Review ist erforderlich, wenn:

```text
confidence < 0.75
derived = true und risk_level >= medium
structural_role = load_bearing
price_unit = unknown
quantity_available = unknown
hazard_flags enthält unknown_pollutants
dimensions sind geschätzt
source_url fehlt
image/text widersprechen sich
```

---

# 7. Wichtigste Design-Regel

Der Analyzer erzeugt **evidence-backed suggestions**:

```text
value
source_asset_id
extraction_method
confidence_score
derived
reasoning_source
verified_status
mapped_schema_field
```

So bleibt das System nachvollziehbar, prüfbar und sicher für wiederverwendbare Bauteile.
