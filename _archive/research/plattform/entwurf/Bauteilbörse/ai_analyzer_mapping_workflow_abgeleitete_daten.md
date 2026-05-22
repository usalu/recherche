# AI-Analyzer → Reclaimed-Material-System: Workflow mit abgeleiteten Daten

## Ziel

Dieses Dokument beschreibt, wie Daten aus Bild, Text, PDF oder Prompt in ein Reclaimed-Material-System überführt werden.

Der wichtigste Zusatz ist die Ebene **Abgeleitete Daten**.  
Diese Ebene enthält Informationen, die nicht direkt im Input stehen, aber aus Kontext, Normwissen, Geometrie, Materialtyp und Reuse-Logik abgeleitet werden können.

Wichtig: **Abgeleitete Daten sind keine geprüfte Wahrheit.**  
Sie dienen als Planungs-, Prüf- und Entscheidungsgrundlage und müssen je nach Risiko validiert werden.

---

## Allgemeiner Workflow

```text
1. Input speichern
2. RawExtraction erzeugen
3. Werte normalisieren
4. Bauteil und Material klassifizieren
5. Abgeleitete Daten erzeugen
6. Schema-Mapping ausführen
7. Validierungs- und Review-Regeln anwenden
8. Datenbank schreiben
9. ReuseAssessment aktualisieren
```

---

## Rolle der abgeleiteten Daten

Abgeleitete Daten beantworten Fragen wie:

```text
Welche Rastermaße ergeben sich?
Welche Masse oder Fläche ist ungefähr relevant?
Welche Tragwerksprüfung ist nötig?
Welche Energie-/CO2-Werte könnten relevant sein?
Welche Reuse-Anwendung ist plausibel?
Welche Risiken entstehen aus Material, Alter, Zustand oder fehlenden Nachweisen?
Welche zusätzlichen Daten fehlen für Planung, Statik, Energie oder Beschaffung?
```

Abgeleitete Daten werden gespeichert mit:

```text
derived_value
basis
formula_or_reasoning
confidence
requires_verification
mapped_target
```

---

# 1. Szenario A — Projekt mit reichen Daten

## Beispiel

```text
IBS-Bauteilkatalog
Rippenplatte Stahlbeton / L=6.84m, B=1.495m
https://bauteile-ibs.ch/components/90-rippenplatte-stahlbeton-l684m-b1495m
```

---

## 1.1 Input-Typen

```text
listing_url
html_listing
images
pdf_factsheet_de
pdf_factsheet_en
dwg_file
print_pdf
```

---

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

---

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

---

## 1.4 Klassifikation

```yaml
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
data_source_type: technical_inventory
```

---

## 1.5 Abgeleitete Daten

Diese Daten entstehen aus Geometrie, Materialtyp, Menge und technischen Angaben.

### Geometrie und Modul

```yaml
single_element_plan_area_m2:
  value: 10.23
  basis: 6.84 m * 1.495 m
  confidence: high

total_plan_area_m2:
  value: 1922.45
  basis: 10.23 m2 * 188 Stück
  confidence: high

module_width_m:
  value: 1.495
  design_relevance: geeignet für ca. 1.50-m-Raster
  confidence: high

element_depth_mm:
  value: 480
  design_relevance: relevant für Aufbauhöhe, Anschlüsse, Transporthöhe und Deckenpaket
  confidence: high
```

### Volumen und Masse

```yaml
bounding_volume_per_element_m3:
  value: 4.91
  basis: 6.84 * 1.495 * 0.48
  note: geometrischer Hüllkörper, nicht tatsächliches Betonvolumen
  confidence: high

estimated_solid_mass_upper_bound_t:
  value_range: 11.8-12.3
  basis: bounding_volume * 2400-2500 kg/m3
  note: Obergrenze; Rippenplatte hat wahrscheinlich geringeres reales Volumen
  confidence: medium

logistics_implication:
  value: Kran, Schwertransport und Hebekonzept erforderlich
  basis: Bauteilgröße und geschätzte Masse
  confidence: high
```

### Tragwerksrelevanz

```yaml
possible_reuse_roles:
  - Deckenplatte
  - Dachplatte
  - Brückenelement nur nach Sonderprüfung
  - Landschafts-/Außenraumelement mit geringerem statischem Anspruch

structural_use_condition:
  value: Nur mit Bestandsstatik, Prüfbericht, Auflagerkonzept und Ingenieurfreigabe
  confidence: high

critical_design_checks:
  - Biegemoment und Querkraft
  - Auflagerdetails
  - Durchstanz-/Randbereiche
  - Transport- und Hebezustand
  - Resttragfähigkeit nach Ausbau
  - Zustand der Vorspannung
  - Chlorid- und Korrosionsrisiko
```

### Umwelt- und Reuse-Relevanz

```yaml
co2_difference_per_element_kg:
  value: 1543
  basis: 908 - (-635)
  note: abhängig von LCA-Methode der Quelle
  confidence: medium

co2_difference_total_kg:
  value: 290084
  basis: 1543 kg * 188 Stück
  confidence: medium

reuse_priority:
  value: hoch
  basis: große Masse, hohe graue Energie, tragende Funktion
  confidence: high
```

### Fehlende Planungsdaten

```yaml
missing_for_design:
  - exakte Bewehrungs- und Vorspanndaten
  - reale Masse pro Element
  - vorhandene Schäden und Risse
  - Auflagerdetails im neuen Projekt
  - Feuerwiderstand im neuen Kontext
  - aktuelle Verfügbarkeit und Zugriffsbeschränkung
  - Transportweg und Kranlasten
```

---

## 1.6 Schema-Mapping

### `Item`

```yaml
canonical_title: Rippenplatte aus Spannbeton
component_family: structure
component_type: slab
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
area_m2: 10.23
total_area_m2: 1922.45
```

### `TechnicalAttribute`

```yaml
attribute_group: structural_concrete
compressive_strength_mpa: 67.4
modulus_elasticity_mpa: 42100-50500
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
co2_difference_per_element_kg: 1543
co2_difference_total_kg: 290084
environmental_data_confidence: medium
```

### `ReuseAssessment`

```yaml
reuse_confidence_score: B_design_ready
recommended_next_action:
  - check_availability
  - request_structural_review
  - request_pollutant_test
  - calculate_transport_and_lifting
```

---

# 2. Szenario B — Wenige Bilder + Beschreibung

## Beispiel

```text
Stahlträger HEB 140 – Länge 2,54m
Artikel-Nr.: #201605
Zustand: Neu
Bauteil: Stahlträger
Beschreibung: Neuer, noch nie verbauter Stahlträger HEB 140,
inkl. Unterlegbleche der Mauerwerks- und Balkenauflager.
```

---

## 2.1 Input-Typen

```text
screenshot
image_gallery
visible_listing_text
```

---

## 2.2 Raw Extraction

```yaml
title: Stahlträger HEB 140 – Länge 2,54m
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

---

## 2.3 Normalisierung

```yaml
length_mm: 2540
component_normalized: steel_beam
profile_type: HEB
section_size: "140"
condition_normalized: new
```

---

## 2.4 Klassifikation

```yaml
component_family: structure
component_type: beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
```

---

## 2.5 Abgeleitete Daten

Diese Daten basieren auf der Angabe `HEB 140` und typischen Profilwerten.  
Sie sind **Vorwerte** und müssen mit Hersteller- oder Normtabelle geprüft werden.

### Profil- und Massenschätzung

```yaml
profile_type:
  value: HEB
  confidence: high

nominal_profile_height_mm:
  value: 140
  confidence: high

nominal_profile_width_mm:
  value: 140
  confidence: high

typical_mass_kg_per_m:
  value_range: 33.7-34.2
  basis: typische HEB-140-Profilmasse
  confidence: medium

estimated_piece_weight_kg:
  value_range: 85.6-86.9
  basis: 2.54 m * 33.7-34.2 kg/m
  confidence: medium
```

### Vorbemessungswerte

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

estimated_bending_only_uniform_load_s235_kn_per_m:
  value_approx: 63
  basis: einfach gelagerter Träger, L=2.54 m, nur Biegung, ohne Stabilitäts-/Sicherheitsnachweise
  confidence: low
  verification_required: true
```

### Design- und Reuse-Relevanz

```yaml
possible_reuse_roles:
  - kurzer Stahlträger
  - Sturz
  - Unterzug für kleine Spannweite
  - sekundäres Tragwerk
  - Möbel-/Innenausbau mit industriellem Look

design_advantage:
  value: neue, unverbaute Ware mit klarer Profilbezeichnung
  confidence: high

logistics_implication:
  value: Einzelträger vermutlich mit 2 Personen oder Hebehilfe bewegbar; sichere Hebeprüfung empfohlen
  basis: geschätztes Gewicht ca. 86 kg
  confidence: medium
```

### Fehlende Planungsdaten

```yaml
missing_for_design:
  - Stahlgüte
  - exakte Profilnorm und Hersteller
  - Menge
  - Preis
  - Standort
  - Korrosionszustand trotz Neuware
  - Nachweis für Tragwerksverwendung
  - Auflagerlängen
  - Verbindungskonzept
  - Brandschutzanforderung
```

---

## 2.6 Schema-Mapping

### `Item`

```yaml
canonical_title: Stahlträger HEB 140
component_family: structure
component_type: beam
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
estimated_piece_weight_kg: 85.6-86.9
quantity: null
quantity_unit: piece
dimension_notes: HEB 140 profile; exact profile table should be verified
```

### `TechnicalAttribute`

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

---

## 3.1 Input-Typen

```text
user_prompt
free_text_description
no_images
no_url
no_documents
```

---

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

---

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

---

## 3.4 Klassifikation

```yaml
component_family: structure
component_type: beam
material_family: timber_biobased
primary_material: solid_timber
structural_role: unknown_or_potentially_load_bearing
newness_type: reclaimed
```

---

## 3.5 Abgeleitete Daten

Diese Daten basieren nur auf Freitext.  
Konfidenz ist niedriger als bei URL/PDF/Bilddaten.

### Geometrie und Mengen

```yaml
quantity_total:
  value: 10
  confidence: high

cross_section_min_mm:
  value: 180 x 180
  confidence: high

cross_section_common_range_mm:
  value: 180x180 bis 200x220
  confidence: medium

cross_section_max_mm:
  value: 220 x 220
  confidence: high

length_range_mm:
  value: 1000-6000
  confidence: high

estimated_volume_per_piece_min_m3:
  value: 0.032
  basis: 0.18 * 0.18 * 1.0
  confidence: medium

estimated_volume_per_piece_max_m3:
  value: 0.290
  basis: 0.22 * 0.22 * 6.0
  confidence: medium

estimated_total_volume_typical_m3:
  value_approx: 1.4
  basis: 10 Stück * 0.20 * 0.20 * 3.5 m angenommene Durchschnittslänge
  confidence: low
```

### Masse und Handling

```yaml
assumed_dry_timber_density_kg_m3:
  value_range: 450-650
  confidence: medium

estimated_total_weight_typical_kg:
  value_range: 630-910
  basis: 1.4 m3 * 450-650 kg/m3
  confidence: low

estimated_weight_single_6m_beam_kg:
  value_range: 97-189
  basis: 6 m * Querschnitt 180x180 bis 220x220 mm * 500-650 kg/m3
  confidence: low

handling_note:
  value: einzelne kurze Balken vermutlich manuell bewegbar; lange Balken nicht sicher alleine tragbar
  confidence: medium
```

### Tragwerksrelevanz

```yaml
possible_reuse_roles:
  - dekorative Balken
  - sichtbare Innenausbau-Elemente
  - Möbelbau
  - nichttragende Pergola-/Ausbauteile
  - tragende Nutzung nur nach Holzsortierung und statischer Prüfung

structural_use_condition:
  value: Tragende Wiederverwendung nur nach Festigkeitssortierung, Feuchteprüfung, Schädlingsprüfung und Ingenieurfreigabe
  confidence: high

critical_design_checks:
  - Holzart bestimmen
  - Querschnitt je Stück messen
  - Risse und Kerben bewerten
  - Insekten- und Pilzbefall prüfen
  - Resttragfähigkeit prüfen
  - frühere Verbindungslöcher und Kerben bewerten
  - Brandschutz im neuen Kontext prüfen
```

### Historische und gestalterische Reuse-Relevanz

```yaml
design_value:
  value: hoch für sichtbare, historische und rustikale Anwendungen
  basis: 160 Jahre, roh, gesägt/geschlagen, fränkische Kerbe
  confidence: high

surface_character:
  value: roh, handwerklich, historisch, rustikal
  confidence: high

recommended_design_use:
  - sichtbare Balkenlage
  - Wand-/Deckenakzent
  - Möbel und Regale
  - Gastronomie-/Retail-Innenausbau
  - reversible Einbauten
```

### Energie- und CO2-Relevanz

```yaml
biogenic_carbon_storage_estimate_kg_co2:
  value_range: 1150-1670
  basis: geschätzte typische Masse 630-910 kg * ca. 1.83 kg CO2 biogen pro kg trockenes Holz
  confidence: low

reuse_priority:
  value: mittel bis hoch
  basis: historisches Material, trocken, vermutlich geringer Aufbereitungsaufwand, gestalterischer Wert
  confidence: medium
```

### Fehlende Planungsdaten

```yaml
missing_for_design:
  - Fotos je Balken
  - Einzelmaße je Stück
  - Holzart
  - Feuchtegehalt
  - Schädlingsbefall
  - Pilzbefall
  - Rissbild
  - genaue Preislogik und Währung
  - Standort
  - Verfügbarkeitstermin
  - Nachweis für tragende Nutzung
```

---

## 3.6 Schema-Mapping

### `Item`

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
estimated_total_volume_typical_m3: 1.4
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

| Szenario | Datenlage | Abgeleitete Daten möglich | Hauptnutzen | Score |
|---|---|---|---|---|
| A: Reiche Projektdaten | URL + PDF + Bilder + CAD | Hoch | Entwurfsplanung, Vorstatik, CO2, Logistik | `B_design_ready` |
| B: Screenshot + Beschreibung | Bild + sichtbarer Text | Mittel | Voridentifikation, Profilgewicht, Prüfbedarf | `C_investigation_only` |
| C: Nur Prompt | Freitext | Niedrig bis mittel | Mengenabschätzung, Designpotenzial, fehlende Daten | `C_investigation_only` |

---

# 5. Review-Regeln

Ein menschliches Review ist erforderlich, wenn:

```text
confidence < 0.75
structural_role = load_bearing
price_unit = unknown
quantity_available = unknown
source_url fehlt
Abmessungen nur geschätzt sind
Stahlgüte / Holzart / Betondaten fehlen
hazard_flags unknown_pollutants oder structural_uncertainty enthalten
image/text/pdf sich widersprechen
```

---

# 6. Speichern der abgeleiteten Daten

Abgeleitete Daten sollten nicht unmarkiert in finale Felder geschrieben werden.  
Sie werden als eigene Datensätze gespeichert:

```yaml
derived_data:
  item_id: item-001
  derived_field: estimated_piece_weight_kg
  value: 86.9
  unit: kg
  basis: "HEB 140 typical mass 34.2 kg/m * 2.54 m"
  confidence: medium
  requires_verification: true
  mapped_target: TechnicalAttribute
```

---

# 7. Wichtigste Design-Regel

Der Analyzer liefert drei Ebenen:

```text
1. Extrahierte Daten = direkt gesehen oder gelesen
2. Abgeleitete Daten = logisch berechnet oder kontextuell geschätzt
3. Verifizierte Daten = geprüft und freigegeben
```

Nur Ebene 3 darf für finale Beschaffung, Statik oder Ausführung verwendet werden.
