# AI-Analyzer → Reclaimed-Material-System: Workflow-Beispiele

## Ziel

Dieses Dokument beschreibt kompakt, wie Daten aus einem AI-Bild-/Text-Analyzer in ein Reclaimed-Material-System gemappt werden.

Grundprinzip:

```text
Input
→ DocumentationAsset speichern
→ RawExtraction erzeugen
→ Normalisieren
→ Klassifizieren
→ Schema-Mapping
→ Validieren
→ Review-Status setzen
→ Datenbank schreiben
→ ReuseAssessment aktualisieren
```

Der AI-Analyzer schreibt nicht direkt finale Wahrheit in die Datenbank. Er erzeugt **belegte Vorschläge** mit Quelle, Konfidenz und Review-Status.

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

## Workflow

### Schritt 1 — Quellen speichern

Jede Datei oder Seite wird als `DocumentationAsset` gespeichert.

```text
asset_type: marketplace_listing
asset_type: image
asset_type: pdf_factsheet
asset_type: cad_file
asset_type: print_pdf
```

### Schritt 2 — Analyzer-Extraktion

```text
Titel: Rippenplatte Stahlbeton / L=6.84m, B=1.495m
Bauteil: strukturelles Deckenelement
Material: Fertigteil-Stahlbeton / Spannbeton
Dimensionen: 6.84m x 1.495m x 48cm
Menge: 188 Stück
CO2 neu: 908 kg/Stk
CO2 Wiederverwendung: -635 kg/Stk
Karbonatisierungstiefe: 21 mm
Druckfestigkeit Beton: 67.4 N/mm2
Elastizitätsmodul Beton: 42.1 bis 50.5 kN/mm2
Dekonstruktionswerkzeug: Diamantsäge
Risiken: Chloride, Korrosion, Feuchtigkeit, Kohlenwasserstoffe, Asbest/PCB ungeklärt
```

### Schritt 3 — Normalisierung

```text
6.84 m → 6840 mm
1.495 m → 1495 mm
48 cm → 480 mm
188 Stk → 188 piece
67.4 N/mm2 → 67.4 MPa
```

### Schritt 4 — Klassifikation

```text
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
data_source_type: technical_inventory
```

### Schritt 5 — Schema-Mapping

#### `Item`

```yaml
canonical_title: Rippenplatte aus Spannbeton
component_family: structure
component_type: slab
material_family: mineral
primary_material: prestressed_concrete
structural_role: load_bearing
newness_type: reclaimed
```

#### `Listing`

```yaml
source_platform: ibs
source_url: https://bauteile-ibs.ch/components/90-rippenplatte-stahlbeton-l684m-b1495m
page_status: live_restricted
data_source_type: technical_inventory
data_confidence: high
```

#### `VariantBatch`

```yaml
quantity: 188
quantity_unit: piece
length_mm: 6840
width_mm: 1495
height_mm: 480
```

#### `TechnicalAttribute`

```yaml
attribute_group: structural_concrete
compressive_strength_mpa: 67.4
carbonation_depth_mm: 21
prestressed: true
connection_type: ribbed_slab_supported_by_beams
cutting_required: true
```

#### `RiskAssessment`

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

#### `EnvironmentalData`

```yaml
co2_new_component_kg: 908
co2_reuse_component_kg: -635
environmental_data_confidence: medium
```

#### `ReuseAssessment`

```yaml
reuse_confidence_score: B_design_ready
recommended_next_action:
  - check_availability
  - request_structural_review
  - request_pollutant_test
```

## Ergebnis

Dieses Szenario erzeugt einen relativ vollständigen Datensatz. Die technischen Daten sind stark, aber Beschaffung, Freigabe und strukturelle Wiederverwendung müssen geprüft werden.

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

## Workflow

### Schritt 1 — Bild als Quelle speichern

```yaml
asset_type: image
file_format: png
extraction_method: ai_visual_ocr
```

### Schritt 2 — Analyzer-Extraktion

```text
Titel: Stahlträger HEB 140 – Länge 2,54m
Artikelnummer: #201605
Zustand: Neu
Bauteil: Stahlträger
Profil: HEB 140
Länge: 2.54 m
Zubehör: Unterlegbleche
Menge: nicht sichtbar
Preis: nicht sichtbar
Standort: nicht sichtbar
```

### Schritt 3 — Normalisierung

```text
2.54 m → 2540 mm
Stahlträger → steel_beam
HEB 140 → profile_type: HEB, section_size: 140
Neu → condition_normalized: new
```

### Schritt 4 — Klassifikation

```text
component_family: structure
component_type: beam
material_family: metal
primary_material: steel
structural_role: load_bearing
```

### Schritt 5 — Schema-Mapping

#### `Item`

```yaml
canonical_title: Stahlträger HEB 140
component_family: structure
component_type: beam
material_family: metal
primary_material: steel
structural_role: load_bearing
newness_type: overstock
```

#### `Listing`

```yaml
external_article_number: "#201605"
original_title: Stahlträger HEB 140 – Länge 2,54m
data_source_type: marketplace_listing
data_confidence: medium
```

#### `VariantBatch`

```yaml
length_mm: 2540
quantity: null
quantity_unit: piece
dimension_notes: HEB 140 profile; exact cross-section should be verified
```

#### `TechnicalAttribute`

```yaml
attribute_group: metal_steel
profile_type: HEB
section_size: "140"
accessory_list: Unterlegbleche für Mauerwerks- und Balkenauflager
```

#### `Condition`

```yaml
condition_raw: Neu, noch nie verbaut
condition_normalized: new
inspection_method: ai_visual_ocr
```

#### `RiskAssessment`

```yaml
risk_level: medium
hazard_flags:
  - structural_uncertainty
structural_verification_required: true
pollutant_test_status: unknown
```

#### `ReuseAssessment`

```yaml
reuse_confidence_score: C_investigation_only
recommended_next_action:
  - request_full_listing_url
  - check_availability
  - request_price
  - request_stock_quantity
  - request_structural_review
```

## Ergebnis

Dieses Szenario erzeugt einen brauchbaren Vor-Datensatz. Identität und Geometrie sind teilweise klar, aber Preis, Menge, Standort, Verfügbarkeit und technische Nachweise fehlen.

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

## Workflow

### Schritt 1 — Prompt als Quelle speichern

```yaml
asset_type: manual_entry
data_source_type: user_prompt
extraction_method: text_parser
```

### Schritt 2 — Analyzer-Extraktion

```text
Bauteil: alte Holzbalken
Herkunft: laufende Altbausanierung
Alter: ca. 160 Jahre
Menge: 10 Stück
Querschnitt: meist 18x18 bis 20x22 cm
Maximaler Querschnitt: 22x22 cm
Länge: ca. 1 bis 6 m
Besonderheit: teilweise zweiseitige fränkische Kerbe
Zustand: sehr trocken, sehr gut erhalten
Oberfläche: roh, unbehandelt, gesägt und geschlagen
Look: historisch, rustikal
Preis: 20, Einheit/Währung unklar
```

### Schritt 3 — Normalisierung

```text
10 Stück → 10 piece
18 cm → 180 mm
20 cm → 200 mm
22 cm → 220 mm
1 m → 1000 mm
6 m → 6000 mm
160 Jahre alt → estimated_age_years: 160
```

### Schritt 4 — Klassifikation

```text
component_family: structure
component_type: beam
material_family: timber_biobased
primary_material: solid_timber
structural_role: unknown_or_potentially_load_bearing
newness_type: reclaimed
```

### Schritt 5 — Schema-Mapping

#### `Item`

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

#### `VariantBatch`

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

#### `TechnicalAttribute`

```yaml
attribute_group: timber
estimated_age_years: 160
wood_species: unknown
solid_or_engineered: solid_timber
surface_finish: raw_untreated
moisture_condition: very_dry
joinery_detail: two-sided_franconian_notch_partial
```

#### `Condition`

```yaml
condition_raw: gebraucht, roh, unbehandelt, sehr trocken, sehr gut erhalten
condition_normalized: used_good
wear_level: used_light_wear
inspection_method: user_description
```

#### `AvailabilitySnapshot`

```yaml
availability_status: on_request
quantity_available: 10
quantity_unit: piece
price_amount: 20
currency: unknown
price_unit: unknown
price_type: unclear
```

#### `RiskAssessment`

```yaml
risk_level: medium
hazard_flags:
  - biological_damage_unknown
  - structural_uncertainty
  - missing_certification
pollutant_test_status: not_tested
structural_verification_required: true
```

#### `ReuseAssessment`

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

## Ergebnis

Dieses Szenario erzeugt nur einen Entwurfsdatensatz. Die Beschreibung ist nützlich, aber Fotos, exakte Maße, Holzart, Standort, Preislogik und Zustand müssen verifiziert werden.

---

# 4. Vergleich der drei Szenarien

| Szenario | Datenlage | Automatisch erfassbar | Hauptlücken | Score |
|---|---|---|---|---|
| A: Reiche Projektdaten | URL + PDF + Bilder + CAD | Sehr viel | Live-Verfügbarkeit, rechtliche Freigabe, finale Prüfung | `B_design_ready` |
| B: Screenshot + Beschreibung | Bild + sichtbarer Text | Mittel | Preis, Menge, Standort, Link, Nachweise | `C_investigation_only` |
| C: Nur Prompt | Freitext | Wenig bis mittel | Fotos, Belege, Maße pro Stück, Standort, Preis, Materialprüfung | `C_investigation_only` |

---

# 5. Einheitlicher Mapping-Prozess

```text
1. Input speichern
2. RawExtraction erzeugen
3. Werte normalisieren
4. Bauteil und Material klassifizieren
5. Universelle Felder mappen
6. Kategorie-Attributpaket aktivieren
7. Fehlende Felder markieren
8. Risiko- und Review-Regeln ausführen
9. ReuseAssessment berechnen
10. In Datenbank schreiben
```

---

# 6. Review-Regeln

Ein menschliches Review ist erforderlich, wenn:

```text
confidence < 0.75
structural_role = load_bearing
price_unit = unknown
quantity_available = unknown
hazard_flags enthält unknown_pollutants
dimensions sind nur geschätzt
source_url fehlt
image/text widersprechen sich
```

---

# 7. Wichtigste Design-Regel

Der Analyzer erzeugt keine finalen Wahrheiten, sondern **evidence-backed suggestions**:

```text
value
source_asset_id
extraction_method
confidence_score
verified_status
mapped_schema_field
```

So bleibt das System nachvollziehbar, prüfbar und sicher für wiederverwendbare Bauteile.
