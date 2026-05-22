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
→ Abgeleitete Daten erzeugen
→ Schema-Mapping
→ Validieren
→ Review-Status setzen
→ Datenbank schreiben
→ ReuseAssessment aktualisieren
```

Der AI-Analyzer schreibt nicht direkt finale Wahrheit in die Datenbank. Er erzeugt **belegte Vorschläge** mit Quelle, Konfidenz und Review-Status.

Wichtig: **Abgeleitete Daten** sind keine geprüften Fakten. Sie sind Vorplanungsannahmen, die aus Kontext, Geometrie, Materialtyp und typischen Planungslogiken entstehen. Sie müssen mit Konfidenz, Quelle und Review-Status gespeichert werden.

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

### Schritt 5 — Abgeleitete Daten

Diese Daten werden für Entwurf, Vorplanung, statische Vordimensionierung, Logistik und LCA abgeleitet.

#### Design / Entwurf

```yaml
module_width_mm: 1495
module_length_mm: 6840
gross_area_per_unit_m2: 10.23
potential_total_gross_area_m2: 1923.24
likely_design_use:
  - wiederverwendbares Deckenelement
  - Dach-/Plattenelement nach Prüfung
  - serielles Rasterelement für modulare Planung
design_constraints:
  - große Bauteiltiefe von 480 mm beeinflusst Geschosshöhen
  - Einbaurichtung wahrscheinlich einachsig spannend
  - Ausschnitte und Bohrungen nicht ohne Nachweis annehmen
  - Auflager- und Anschlussdetails sind entwurfsbestimmend
confidence: medium
```

#### Vorplanung Statik

```yaml
preliminary_static_assumptions:
  span_direction: entlang der Länge, zu prüfen
  support_logic: Auflagerung auf Unterzügen oder Linienauflagern, zu prüfen
  structural_system: einachsig tragende Rippen-/Spannbetonplatte, zu prüfen
required_checks:
  - Biegung
  - Querkraft
  - Auflagerpressung
  - Resttragfähigkeit der Vorspannung
  - Rissbild und Abplatzungen
  - Chlorid-/Korrosionsrisiko
  - Brandschutz
  - Anschluss an neues Tragwerk
not_safe_for_final_calculation_until:
  - Statikerfreigabe
  - Prüfbericht vollständig
  - Bewehrungs-/Vorspanndaten geprüft
  - Bauteilzustand pro Element dokumentiert
confidence: medium
```

#### Energie / LCA / Wiederverwendung

```yaml
co2_new_per_m2_kg: 88.8
co2_reuse_per_m2_kg: -62.1
potential_co2_difference_per_m2_kg: 150.9
potential_total_co2_difference_kg: 290084
lca_notes:
  - Werte sind aus den angegebenen Stückwerten abgeleitet
  - Transport, Lagerung, Zuschnitt und neue Anschlüsse separat bilanzieren
  - tatsächliche Materialmenge kann wegen Rippengeometrie vom Bruttovolumen abweichen
confidence: medium
```

#### Logistik / Rückbau

```yaml
handling_assumptions:
  - Kran- oder schweres Hebegerät wahrscheinlich erforderlich
  - Transport als großformatiges Fertigteil
  - Schutz gegen Kantenschäden und Rissbildung erforderlich
  - Rückbau mit Diamantsäge deutet auf nicht vollständig reversible Verbindung hin
missing_logistics_data:
  - Gewicht pro Einheit
  - Hebepunkte
  - Stapelbarkeit
  - Transportrestriktionen
  - Lagerzustand
confidence: medium
```

### Schritt 6 — Schema-Mapping

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

### Schritt 5 — Abgeleitete Daten

Diese Daten entstehen aus Profiltyp, Länge, Zustand und sichtbarem Kontext.

#### Design / Entwurf

```yaml
likely_design_use:
  - kurzer Stahlträger
  - Sturz über Öffnung
  - sekundärer Träger
  - Auflager- oder Verstärkungselement
useful_design_features:
  - HEB-Profil ist kompakt und gut für kurze Spannweiten
  - Unterlegbleche können für Mauerwerks- oder Holzauflager relevant sein
  - Länge 2540 mm ist geeignet für kleine Öffnungen oder lokale Verstärkungen
visual_notes:
  - sichtbare Lager-/Flugrostspuren möglich, obwohl Zustand als neu angegeben ist
  - Oberfläche vor Beschichtung prüfen
confidence: medium
```

#### Vorplanung Statik

```yaml
preliminary_static_assumptions:
  profile_family: HEB
  nominal_profile_size: 140
  length_mm: 2540
  approximate_mass_kg: 85
  mass_basis: typischer HEB-140-Wert ca. 33–34 kg/m, muss mit Profiltabelle geprüft werden
required_profile_table_values:
  - steel_grade
  - cross_section_area
  - Iy
  - Iz
  - Wel_y
  - Wpl_y
  - torsional_values
required_checks:
  - Stahlgüte S235/S355 klären
  - Biegung
  - Querkraft
  - Durchbiegung
  - Biegedrillknicken
  - Auflagerlänge
  - Schraub-/Schweißanschlüsse
not_safe_for_final_calculation_until:
  - Stahlgüte bekannt
  - Profiltabelle bestätigt
  - Zustand und Korrosion geprüft
  - Auflager und Lastannahmen bekannt
confidence: low_to_medium
```

#### Energie / LCA / Wiederverwendung

```yaml
lca_mass_input_kg: 85
lca_formula: Masse × Emissionsfaktor für Primärstahl oder Recyclingstahl
reuse_relevance:
  - wenn tatsächlich unverbauter Überbestand, keine Rückbauemissionen
  - Wiederverwendung kann Neuproduktion eines Stahlträgers vermeiden
  - Oberflächenreinigung oder Beschichtung separat bilanzieren
missing_lca_data:
  - exaktes Gewicht
  - Stahlgüte
  - Transportdistanz
  - notwendige Nachbehandlung
confidence: low_to_medium
```

#### Logistik / Beschaffung

```yaml
handling_assumptions:
  - ca. 85 kg, daher eher zwei Personen oder Hebehilfe
  - kurze Länge erleichtert Transport
  - Kanten- und Korrosionsschutz bei Lagerung relevant
missing_procurement_data:
  - Preis
  - Menge
  - Standort
  - Verkäuferkontakt
  - Liefer-/Abholbedingungen
  - Zertifikate oder Lieferschein
confidence: medium
```

### Schritt 6 — Schema-Mapping

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

### Schritt 5 — Abgeleitete Daten

Diese Daten werden aus Freitext, Alter, Geometrie und Materiallogik abgeleitet.

#### Design / Entwurf

```yaml
likely_design_use:
  - sichtbare historische Balken
  - Innenausbau mit rustikalem Charakter
  - dekorative Träger
  - Möbelbau oder Einbauten
  - sekundäre Konstruktion nach Prüfung
design_value:
  - hoher gestalterischer Wert durch Alter, Patina und Kerben
  - roh/unbehandelte Oberfläche geeignet für sichtbare Wiederverwendung
  - variable Längen ermöglichen Sortierung nach Entwurfsraster
design_constraints:
  - jedes Stück muss einzeln vermessen werden
  - Kerben und alte Bearbeitungsspuren reduzieren nutzbaren Querschnitt
  - Toleranzen und Verformungen einplanen
  - Oberfläche kann splittern oder Nachbearbeitung benötigen
confidence: medium
```

#### Vorplanung Statik

```yaml
preliminary_geometry:
  quantity: 10
  length_range_mm: 1000-6000
  section_min_mm: 180x180
  section_max_mm: 220x220
  cross_section_area_range_m2: 0.0324-0.0484
  volume_per_piece_range_m3: 0.0324-0.2904
  total_batch_volume_range_m3: 0.324-2.904
structural_assumptions:
  structural_use_possible_only_after_grading: true
  kerbs_reduce_effective_section: true
  old_timber_strength_unknown: true
required_checks:
  - Holzart bestimmen
  - Feuchte messen
  - Insektenbefall prüfen
  - Pilzbefall prüfen
  - Risse und Verdrehung dokumentieren
  - Kerben statisch bewerten
  - Festigkeitsklasse oder Sortierklasse festlegen
  - Tragfähigkeit und Durchbiegung pro Einzelbalken prüfen
not_safe_for_final_calculation_until:
  - Einzelmaße vorliegen
  - Holzart und Festigkeit bekannt sind
  - Schäden und Kerben bewertet sind
confidence: low_to_medium
```

#### Energie / LCA / Wiederverwendung

```yaml
lca_volume_input_m3: 0.324-2.904
lca_formula: Holzvolumen × Rohdichte × Emissions- oder Speicherfaktor
reuse_relevance:
  - vermeidet neues Bauholz oder dekoratives Altholz
  - biogener Kohlenstoff kann bilanziell relevant sein
  - sehr trockener Zustand reduziert Trocknungsaufwand
additional_lca_inputs_needed:
  - Holzart
  - Rohdichte
  - tatsächliches Volumen pro Balken
  - Transportdistanz
  - Nachbearbeitung wie Hobeln, Sägen, Bürsten oder Schädlingsbehandlung
confidence: low
```

#### Logistik / Beschaffung

```yaml
handling_assumptions:
  - einzelne kurze Stücke wahrscheinlich manuell tragbar
  - lange Stücke bis 6 m benötigen zwei Personen oder Transporthilfe
  - trockene, alte Oberfläche braucht Schutz bei Transport und Lagerung
price_interpretation:
  price_amount: 20
  price_unit: unknown
  possible_price_units:
    - per_piece
    - per_linear_meter
    - depending_on_length
missing_procurement_data:
  - Standort
  - Fotos
  - exakte Maße je Balken
  - Preislogik
  - Währung
  - Abholzeitraum
  - Demontagezustand
confidence: low_to_medium
```

### Schritt 6 — Schema-Mapping

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

| Szenario | Datenlage | Automatisch erfassbar | Wichtigste abgeleitete Daten | Hauptlücken | Score |
|---|---|---|---|---|---|
| A: Reiche Projektdaten | URL + PDF + Bilder + CAD | Sehr viel | Raster, Fläche, CO2/m², Vorstatik-Risiken, Rückbauannahmen | Live-Verfügbarkeit, finale Statik, Freigabe | `B_design_ready` |
| B: Screenshot + Beschreibung | Bild + sichtbarer Text | Mittel | Profiltyp, Vorstatik-Checkliste, ungefähres Gewicht, LCA-Masseninput | Preis, Menge, Standort, Link, Nachweise | `C_investigation_only` |
| C: Nur Prompt | Freitext | Wenig bis mittel | Volumenbereich, Designpotenzial, Prüfbedarf, LCA-Formel | Fotos, Einzelmaße, Holzart, Preislogik, Zustand | `C_investigation_only` |

---

# 5. Einheitlicher Mapping-Prozess

```text
1. Input speichern
2. RawExtraction erzeugen
3. Werte normalisieren
4. Bauteil und Material klassifizieren
5. Abgeleitete Daten berechnen oder schätzen
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
structural_role = load_bearing
price_unit = unknown
quantity_available = unknown
hazard_flags enthält unknown_pollutants
dimensions sind nur geschätzt
source_url fehlt
image/text widersprechen sich
abgeleitete_daten werden für Statik oder LCA verwendet
```

---

# 7. Speicherung von abgeleiteten Daten

Abgeleitete Daten sollten separat von extrahierten Daten gespeichert werden.

```yaml
derived_data:
  field_name: gross_area_per_unit_m2
  value: 10.23
  method: length_mm * width_mm
  source_fields:
    - length_mm
    - width_mm
  confidence: medium
  usable_for:
    - design
    - lca_precalculation
  verified_status: unverified
```

Empfohlene Kategorien:

```text
design_derivation
structural_precheck
lca_precheck
logistics_precheck
risk_precheck
procurement_precheck
```

---

# 8. Wichtigste Design-Regel

Der Analyzer erzeugt keine finalen Wahrheiten, sondern **evidence-backed suggestions**:

```text
value
source_asset_id
extraction_method
confidence_score
verified_status
mapped_schema_field
derivation_method
usable_for
```

So bleibt das System nachvollziehbar, prüfbar und sicher für wiederverwendbare Bauteile.
