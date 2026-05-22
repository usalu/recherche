# Beispiel: Wie „messy“ Bauteilbörse-Daten ins Schema passen

## Zweck

Dieses Dokument zeigt anhand realistischer, aber vereinfachter Beispiele, wie unterschiedliche Arten von Bauteilbörse- und Reuse-Marktplatzdaten in ein sauberes Schema überführt werden können.

Die Beispiele illustrieren bewusst die typische Unordnung:

- unterschiedliche Plattformlogiken
- fehlende Felder
- widersprüchliche Angaben
- gemischte Einheiten
- alte oder unsichere Verfügbarkeiten
- technische PDFs neben einfachen Shop-Inseraten
- Freitext statt strukturierter Daten
- Mengen, Preise und Zustände mit geringer Verlässlichkeit

---

## 1. Warum die Daten unordentlich sind

| Problem | Beispiel | Lösung im Schema |
|---|---|---|
| Titel enthält mehrere Informationen | „Fenster Holz 120x140, gut, 12 Stk., ab Juli“ | Titel bereinigen, Maße/Menge/Verfügbarkeit separat speichern |
| Menge ist ungenau | „ca. 20 Stück“, „mehrere“, „1 Posten“ | `quantity_available`, `quantity_unit`, `data_confidence` |
| Preis ist nicht eindeutig | „CHF 50/Stk.“, „VB“, „auf Anfrage“ | `price_amount`, `price_unit`, `price_type` |
| Zustand ist Freitext | „gebraucht, aber schön“, „leichte Spuren“ | `condition_raw` + `condition_normalized` |
| Standort ist unklar | „Basel“, „Abholung Baustelle“, „Lager Zürich“ | `Location` mit `location_type` |
| Herkunft und aktueller Ort vermischen sich | „aus Rückbau in Basel, jetzt im Lager“ | `Provenance` + `Location` trennen |
| Technische Daten liegen in PDFs | IBS-artige Factsheets | `DocumentationAsset` + `TechnicalAttribute` |
| Verfügbarkeit ändert sich | Seite live, aber Bestand evtl. alt | `AvailabilitySnapshot` mit `checked_at` |
| Risiken stehen nur in Notizen | „Eternit?“, „KMF vorhanden“ | `RiskAssessment.hazard_flags` |

---

# 2. Beispiel A — IBS-artiges technisches Bauteil

## 2.1 Eingehende Rohdaten

```text
Quelle: IBS Bauteilkatalog
Titel: Rippenplatte Stahlbeton L=5.79m, B=1.495m
Menge: 24 Stk.
CO2 Einsparung: vorhanden
PDFs: DE Factsheet, EN Factsheet
CAD: DWG vorhanden
Bemerkung: Verfügbarkeit möglicherweise projektgebunden
Technik im PDF:
- Spannbeton / Stahlbeton
- Druckfestigkeit 67.4 N/mm²
- Karbonatisierungstiefe 21 mm
- weitere Prüfung empfohlen
- mögliche Schadstoffe/Chloride prüfen
```

## 2.2 Problem

Diese Daten sind technisch reich, aber beschaffungsseitig unsicher.

| Datenart | Qualität |
|---|---|
| Maße | hoch |
| Menge | mittel |
| technische Prüfung | mittel bis hoch |
| Verfügbarkeit | niedrig bis mittel |
| Preis | fehlt |
| Logistik | teilweise unklar |
| Risiko | vorhanden, aber nicht vollständig geprüft |

## 2.3 Normalisierte Struktur

```json
{
  "item": {
    "item_id": "item-ibs-001",
    "canonical_title": "Rippenplatte aus Spannbeton",
    "component_family": "structure",
    "component_type": "slab",
    "material_family": "mineral",
    "primary_material": "prestressed_concrete",
    "structural_role": "load_bearing",
    "is_batch": true
  },
  "listing": {
    "listing_id": "listing-ibs-001",
    "item_id": "item-ibs-001",
    "source_platform": "ibs",
    "source_url": "https://example.org/ibs/rippenplatte-579",
    "original_title": "Rippenplatte Stahlbeton L=5.79m, B=1.495m",
    "page_status": "live_restricted",
    "data_source_type": "technical_inventory",
    "data_confidence": "medium"
  },
  "variant_batch": {
    "variant_id": "variant-ibs-001",
    "item_id": "item-ibs-001",
    "variant_label": "L=5.79m, B=1.495m",
    "quantity": 24,
    "quantity_unit": "piece",
    "length_mm": 5790,
    "width_mm": 1495,
    "height_mm": 480
  },
  "availability_snapshot": {
    "snapshot_id": "snap-ibs-001",
    "listing_id": "listing-ibs-001",
    "checked_at": "2026-06-14",
    "availability_status": "project_restricted",
    "quantity_available": 24,
    "quantity_unit": "piece",
    "price_type": "unknown",
    "contact_required": true
  },
  "technical_attributes": [
    {
      "attribute_group": "structural_concrete",
      "attribute_name": "compressive_strength",
      "value_number": 67.4,
      "unit": "MPa",
      "confidence": "medium",
      "source_asset_id": "asset-ibs-pdf-001"
    },
    {
      "attribute_group": "structural_concrete",
      "attribute_name": "carbonation_depth",
      "value_number": 21,
      "unit": "mm",
      "confidence": "medium",
      "source_asset_id": "asset-ibs-pdf-001"
    }
  ],
  "risk_assessment": {
    "risk_id": "risk-ibs-001",
    "item_id": "item-ibs-001",
    "risk_level": "medium",
    "hazard_flags": ["chlorides", "hydrocarbons", "structural_uncertainty"],
    "pollutant_test_status": "partial_test",
    "structural_verification_required": true,
    "risk_notes": "Technische Prüfung vorhanden, aber Wiederverwendung erfordert weitere projektspezifische Nachweise."
  },
  "reuse_assessment": {
    "assessment_id": "reuse-ibs-001",
    "item_id": "item-ibs-001",
    "reuse_confidence_score": "B_design_ready",
    "recommended_next_action": "check_availability"
  }
}
```

## 2.4 Erkenntnis

IBS-artige Daten eignen sich gut für **Planung und technische Vorprüfung**, aber weniger gut für sofortige Beschaffung.

---

# 3. Beispiel B — Klassisches lokales Bauteilbörse-Inserat

## 3.1 Eingehende Rohdaten

```text
Quelle: lokale Bauteilbörse
Titel: Alte Holztüren, verschiedene Grössen
Beschreibung:
10-15 Stück, meist gut erhalten, teilweise mit Rahmen.
Masse bitte vor Ort prüfen.
Preis: 40 CHF / Stück, bei Abnahme aller Türen günstiger.
Standort: Lager Basel
Zustand: gebraucht, schöne Patina, einzelne Kratzer
Fotos: 3 Fotos
Abholung: selbst organisieren
```

## 3.2 Problem

Das Inserat ist marktnah, aber technisch ungenau.

| Datenart | Qualität |
|---|---|
| Menge | ungenau |
| Maße | fehlen |
| Preis | vorhanden, aber verhandelbar |
| Zustand | Freitext |
| Fotos | vorhanden |
| Dokumente | fehlen |
| Risiko | unbekannt |

## 3.3 Normalisierte Struktur

```json
{
  "item": {
    "item_id": "item-door-001",
    "canonical_title": "Gebrauchte Holztüren gemischter Größen",
    "component_family": "interior_fitout",
    "component_type": "interior_door",
    "material_family": "timber_biobased",
    "primary_material": "solid_timber",
    "structural_role": "non_load_bearing",
    "is_batch": true
  },
  "listing": {
    "listing_id": "listing-door-001",
    "item_id": "item-door-001",
    "source_platform": "bauteilboerse_local",
    "source_url": "https://example.org/tueren-altbestand",
    "original_title": "Alte Holztüren, verschiedene Grössen",
    "platform_category_raw": "Türen / Fenster",
    "page_status": "live",
    "data_source_type": "marketplace_listing",
    "data_confidence": "medium"
  },
  "variant_batch": {
    "variant_id": "variant-door-001",
    "item_id": "item-door-001",
    "variant_label": "gemischte Größen",
    "quantity": 10,
    "quantity_unit": "piece",
    "dimension_notes": "Inserat nennt 10-15 Stück; Maße müssen vor Ort geprüft werden."
  },
  "location": {
    "location_id": "loc-door-001",
    "location_type": "stored_in_warehouse",
    "name": "Lager Basel",
    "city": "Basel",
    "country": "CH",
    "address_visible": false
  },
  "availability_snapshot": {
    "snapshot_id": "snap-door-001",
    "listing_id": "listing-door-001",
    "checked_at": "2026-06-14",
    "availability_status": "available",
    "quantity_available": 10,
    "quantity_unit": "piece",
    "price_amount": 40,
    "currency": "CHF",
    "price_unit": "piece",
    "price_type": "negotiable",
    "minimum_order_quantity": 1,
    "contact_required": true
  },
  "condition": {
    "condition_id": "cond-door-001",
    "item_id": "item-door-001",
    "condition_raw": "gebraucht, schöne Patina, einzelne Kratzer",
    "condition_normalized": "used_light_wear",
    "wear_level": "medium",
    "damage_notes": "Einzelne Kratzer; Rahmen nur teilweise vorhanden.",
    "tested_status": "not_tested"
  },
  "logistics": {
    "logistics_id": "log-door-001",
    "listing_id": "listing-door-001",
    "deconstruction_status": "stored_in_warehouse",
    "demounting_responsibility": "not_applicable",
    "transport_mode": "pickup_only",
    "loading_included": false,
    "logistics_notes": "Abholung muss selbst organisiert werden."
  },
  "documentation_assets": [
    {
      "asset_id": "asset-door-photo-001",
      "item_id": "item-door-001",
      "listing_id": "listing-door-001",
      "asset_type": "photo",
      "file_format": "jpg",
      "title": "Inseratsfoto 1",
      "asset_confidence": "medium"
    }
  ],
  "reuse_assessment": {
    "assessment_id": "reuse-door-001",
    "item_id": "item-door-001",
    "reuse_confidence_score": "A_procurement_ready",
    "recommended_next_action": "visit_site"
  }
}
```

## 3.4 Erkenntnis

Lokale Bauteilbörsen liefern oft gute **Beschaffungsdaten**, aber schwache **technische Daten**.

---

# 4. Beispiel C — Strukturierter Schweizer Marktplatz

## 4.1 Eingehende Rohdaten

```text
Quelle: Schweizer Reuse-Marktplatz
Titel: Radiator weiss
Kategorie: Gebäudetechnik > Wärmeabgabe
eBKP-H: vorhanden
Artikel-Nr.: 26-000-000175
Preis: CHF 25 / Stück
Menge verfügbar: 8 Stück
Zustand: geprüft, gebraucht
Ort: Zürich
Lieferung: Abholung oder Lieferung nach Absprache
Zahlung: Online / Rechnung
PDF: Artikelblatt
```

## 4.2 Problem

Die Daten sind relativ strukturiert, aber stark plattformspezifisch.

| Datenart | Qualität |
|---|---|
| Klassifikation | hoch |
| Preis | hoch |
| Menge | hoch |
| Zustand | mittel |
| technische Leistung | fehlt oder gering |
| Logistik | mittel |
| Dokumentation | einfaches Artikelblatt |

## 4.3 Normalisierte Struktur

```json
{
  "item": {
    "item_id": "item-radiator-001",
    "canonical_title": "Gebrauchter weißer Radiator",
    "component_family": "building_services",
    "component_type": "radiator",
    "material_family": "metal",
    "primary_material": "steel",
    "structural_role": "non_load_bearing",
    "is_batch": true
  },
  "listing": {
    "listing_id": "listing-radiator-001",
    "item_id": "item-radiator-001",
    "source_platform": "useagain_like",
    "source_url": "https://example.org/useagain/radiator",
    "external_article_number": "26-000-000175",
    "original_title": "Radiator weiss",
    "platform_category_raw": "Gebäudetechnik > Wärmeabgabe",
    "page_status": "live",
    "data_source_type": "marketplace_listing",
    "data_confidence": "high"
  },
  "availability_snapshot": {
    "snapshot_id": "snap-radiator-001",
    "listing_id": "listing-radiator-001",
    "checked_at": "2026-06-14",
    "availability_status": "available",
    "quantity_available": 8,
    "quantity_unit": "piece",
    "price_amount": 25,
    "currency": "CHF",
    "price_unit": "piece",
    "price_type": "fixed",
    "contact_required": false
  },
  "condition": {
    "condition_id": "cond-radiator-001",
    "item_id": "item-radiator-001",
    "condition_raw": "geprüft, gebraucht",
    "condition_normalized": "used_good",
    "tested_status": "tested",
    "inspection_method": "platform_check"
  },
  "logistics": {
    "logistics_id": "log-radiator-001",
    "listing_id": "listing-radiator-001",
    "transport_mode": "delivery_available",
    "logistics_notes": "Abholung oder Lieferung nach Absprache."
  },
  "documentation_assets": [
    {
      "asset_id": "asset-radiator-pdf-001",
      "item_id": "item-radiator-001",
      "listing_id": "listing-radiator-001",
      "asset_type": "pdf_factsheet",
      "file_format": "pdf",
      "title": "Artikelblatt",
      "asset_confidence": "medium"
    }
  ],
  "reuse_assessment": {
    "assessment_id": "reuse-radiator-001",
    "item_id": "item-radiator-001",
    "reuse_confidence_score": "A_procurement_ready",
    "recommended_next_action": "reserve_item"
  }
}
```

## 4.4 Erkenntnis

Strukturierte Marktplätze sind gut für **Bestand, Preis, Kategorie und Beschaffung**, aber oft weniger tief bei technischen Nachweisen.

---

# 5. Beispiel D — Professionelles B2B-Inserat

## 5.1 Eingehende Rohdaten

```text
Quelle: professioneller B2B-Reuse-Shop
Titel: Fensteranlage 5.000 x 1.395 mm, ESG, U-Wert 0.7
Preis: auf Anfrage
Menge: 14 Stück
Verfügbarkeit: Rückbau Q3, Abholung in Tranchen
B2B only
Zustand: geprüft
Technik:
- Aluminiumrahmen
- 3-fach Verglasung
- U-Wert 0.7 W/m²K
- Sonnenschutz teilweise enthalten
Garantie: eingeschränkt / nach Vereinbarung
```

## 5.2 Problem

Hier sind Beschaffung, Zeitfenster und Technik stark, aber oft mit juristischen Einschränkungen.

| Datenart | Qualität |
|---|---|
| technische Produktdaten | hoch |
| Preis | fehlt / Anfrage |
| Verfügbarkeit | gut, aber zeitgebunden |
| Logistik | wichtig und komplex |
| rechtliche Bedingungen | relevant |
| Risiko | eher Zertifikate/Haftung als Schadstoffe |

## 5.3 Normalisierte Struktur

```json
{
  "item": {
    "item_id": "item-window-001",
    "canonical_title": "Aluminium-Fensteranlage mit Dreifachverglasung",
    "component_family": "envelope",
    "component_type": "window",
    "material_family": "composite",
    "primary_material": "aluminium_glass",
    "structural_role": "non_load_bearing",
    "is_batch": true
  },
  "listing": {
    "listing_id": "listing-window-001",
    "item_id": "item-window-001",
    "source_platform": "concular_like",
    "source_url": "https://example.org/concular/window",
    "original_title": "Fensteranlage 5.000 mm x 1.395 mm ESG U-Wert 0.7",
    "page_status": "live",
    "data_source_type": "marketplace_listing",
    "data_confidence": "high"
  },
  "variant_batch": {
    "variant_id": "variant-window-001",
    "item_id": "item-window-001",
    "quantity": 14,
    "quantity_unit": "piece",
    "width_mm": 5000,
    "height_mm": 1395
  },
  "availability_snapshot": {
    "snapshot_id": "snap-window-001",
    "listing_id": "listing-window-001",
    "checked_at": "2026-06-14",
    "availability_status": "available_soon",
    "quantity_available": 14,
    "quantity_unit": "piece",
    "price_type": "price_on_request",
    "commercial_only": true,
    "available_from": "2026-09-01",
    "deconstruction_window_start": "2026-07-01",
    "deconstruction_window_end": "2026-09-30",
    "contact_required": true,
    "warranty_status": "limited_warranty"
  },
  "technical_attributes": [
    {
      "attribute_group": "window_facade",
      "attribute_name": "frame_material",
      "value_text": "aluminium",
      "confidence": "high"
    },
    {
      "attribute_group": "window_facade",
      "attribute_name": "glazing_type",
      "value_text": "triple_glazing",
      "confidence": "high"
    },
    {
      "attribute_group": "window_facade",
      "attribute_name": "u_value",
      "value_number": 0.7,
      "unit": "W/m2K",
      "confidence": "high"
    },
    {
      "attribute_group": "window_facade",
      "attribute_name": "shading_included",
      "value_boolean": true,
      "confidence": "medium"
    }
  ],
  "logistics": {
    "logistics_id": "log-window-001",
    "listing_id": "listing-window-001",
    "deconstruction_status": "dismantling_planned",
    "demounting_responsibility": "reuse_contractor",
    "transport_mode": "freight_required",
    "logistics_notes": "Abholung in Tranchen während Rückbauzeitfenster."
  },
  "risk_assessment": {
    "risk_id": "risk-window-001",
    "item_id": "item-window-001",
    "risk_level": "medium",
    "hazard_flags": ["missing_certification"],
    "fire_certificate_status": "unknown",
    "ce_marking_status": "unknown",
    "risk_notes": "Technische Leistungswerte vorhanden, aber Zertifikats- und Haftungsstatus für neue Anwendung prüfen."
  },
  "reuse_assessment": {
    "assessment_id": "reuse-window-001",
    "item_id": "item-window-001",
    "reuse_confidence_score": "B_design_ready",
    "recommended_next_action": "contact_seller"
  }
}
```

## 5.4 Erkenntnis

Professionelle B2B-Daten sind häufig gut strukturiert, aber stärker abhängig von **Zeitfenstern, Verträgen und Haftung**.

---

# 6. Beispiel E — Restmaterial / Überbestand

## 6.1 Eingehende Rohdaten

```text
Quelle: Restmaterial-Marktplatz
Titel: Dämmplatten EPS, Restposten
Menge: 12 Pakete, ca. 96 m²
Preis: 9.50 EUR / m² zzgl. MwSt.
Zustand: neu, Lagerware
Lieferung: möglich, Kosten separat
Standort: München
Kategorie: Dämmung
```

## 6.2 Problem

Es handelt sich nicht um Rückbauware, sondern um Überbestand. Das ist trotzdem relevant, muss aber anders klassifiziert werden.

| Datenart | Qualität |
|---|---|
| Preis | hoch |
| Menge | hoch |
| Zustand | hoch |
| Herkunft | keine Rückbau-Herkunft |
| Umweltwert | indirekt |
| Risiko | gering bis mittel |

## 6.3 Normalisierte Struktur

```json
{
  "item": {
    "item_id": "item-eps-001",
    "canonical_title": "EPS-Dämmplatten als Restposten",
    "component_family": "envelope",
    "component_type": "insulation",
    "material_family": "polymer",
    "primary_material": "eps",
    "newness_type": "overstock",
    "structural_role": "non_load_bearing",
    "is_batch": true
  },
  "listing": {
    "listing_id": "listing-eps-001",
    "item_id": "item-eps-001",
    "source_platform": "restmaterial_like",
    "source_url": "https://example.org/restmaterial/eps",
    "original_title": "Dämmplatten EPS, Restposten",
    "platform_category_raw": "Dämmung",
    "page_status": "live",
    "data_source_type": "marketplace_listing",
    "data_confidence": "high"
  },
  "variant_batch": {
    "variant_id": "variant-eps-001",
    "item_id": "item-eps-001",
    "quantity": 12,
    "quantity_unit": "package",
    "area_m2": 96,
    "dimension_notes": "12 Pakete entsprechen laut Inserat ca. 96 m²."
  },
  "availability_snapshot": {
    "snapshot_id": "snap-eps-001",
    "listing_id": "listing-eps-001",
    "checked_at": "2026-06-14",
    "availability_status": "available",
    "quantity_available": 96,
    "quantity_unit": "m2",
    "price_amount": 9.5,
    "currency": "EUR",
    "price_unit": "m2",
    "price_type": "fixed",
    "vat_included": false,
    "commercial_only": true
  },
  "condition": {
    "condition_id": "cond-eps-001",
    "item_id": "item-eps-001",
    "condition_raw": "neu, Lagerware",
    "condition_normalized": "new_old_stock",
    "tested_status": "not_required"
  },
  "logistics": {
    "logistics_id": "log-eps-001",
    "listing_id": "listing-eps-001",
    "deconstruction_status": "stored_in_warehouse",
    "transport_mode": "delivery_available",
    "logistics_notes": "Lieferkosten separat."
  },
  "reuse_assessment": {
    "assessment_id": "reuse-eps-001",
    "item_id": "item-eps-001",
    "reuse_confidence_score": "A_procurement_ready",
    "recommended_next_action": "reserve_item"
  }
}
```

## 6.4 Erkenntnis

Restmaterialien sind oft beschaffungsbereit, aber sie gehören nicht in dieselbe Kategorie wie rückgebaute Bauteile: `newness_type = overstock`.

---

# 7. Beispiel F — Projekt-Pipeline / Rückbauchance

## 7.1 Eingehende Rohdaten

```text
Quelle: regionale Reuse-Plattform
Projekt: Bürogebäude Zürich West
Zeitraum Rückbau: Winter 2026
Mögliche Bauteile:
- Doppelböden
- Leuchten
- Glaswände
- Türen
Noch keine Einzelpreise
Noch keine exakten Mengen
Kontakt für Bauteilaufnahme
```

## 7.2 Problem

Das ist kein konkretes Produkt, sondern eine zukünftige Gelegenheit.

| Datenart | Qualität |
|---|---|
| Projekt / Ort | mittel bis hoch |
| Bauteilgruppen | grob |
| konkrete Artikel | fehlen |
| Preise | fehlen |
| Mengen | fehlen |
| Zeitpunkt | grob vorhanden |
| Nutzen | gut für Früherkennung |

## 7.3 Normalisierte Struktur

```json
{
  "item": {
    "item_id": "item-pipeline-001",
    "canonical_title": "Potenzielle Bauteile aus Bürogebäude Zürich West",
    "component_family": "mixed_lot",
    "component_type": "mixed_lot",
    "material_family": "mixed_unknown",
    "primary_material": "requires_assessment",
    "newness_type": "still_installed",
    "is_batch": true
  },
  "listing": {
    "listing_id": "listing-pipeline-001",
    "item_id": "item-pipeline-001",
    "source_platform": "salza_like",
    "source_url": "https://example.org/project/zurich-west",
    "original_title": "Rückbau Bürogebäude Zürich West",
    "page_status": "live",
    "data_source_type": "pre_demolition_audit",
    "data_confidence": "low"
  },
  "provenance": {
    "provenance_id": "prov-pipeline-001",
    "item_id": "item-pipeline-001",
    "source_project_name": "Bürogebäude Zürich West",
    "original_use": "office"
  },
  "availability_snapshot": {
    "snapshot_id": "snap-pipeline-001",
    "listing_id": "listing-pipeline-001",
    "checked_at": "2026-06-14",
    "availability_status": "available_soon",
    "price_type": "unknown",
    "deconstruction_window_start": "2026-12-01",
    "deconstruction_window_end": "2027-02-28",
    "contact_required": true,
    "availability_notes": "Noch keine geprüften Einzelbauteile; Bauteilaufnahme erforderlich."
  },
  "technical_attributes": [
    {
      "attribute_group": "pipeline",
      "attribute_name": "potential_component_groups",
      "value_text": "raised_floor, lighting, glass_partition, interior_door",
      "confidence": "low"
    }
  ],
  "reuse_assessment": {
    "assessment_id": "reuse-pipeline-001",
    "item_id": "item-pipeline-001",
    "reuse_confidence_score": "C_investigation_only",
    "recommended_next_action": "visit_site"
  }
}
```

## 7.4 Erkenntnis

Pipeline-Daten sind schlecht für Einkauf, aber gut für **frühe Planung, Matching und Bauteilaufnahme**.

---

# 8. Vergleich der Datentypen

| Datentyp | Typische Quelle | Stärken | Schwächen | Passender Score |
|---|---|---|---|---|
| Technischer Bauteilkatalog | IBS-artig | Maße, PDFs, Prüfwerte, CAD | Verfügbarkeit/Preis unsicher | `B_design_ready` |
| Lokale Bauteilbörse | Basel/Bremen/Laden | Preis, Abholung, Fotos | Maße/Tests oft ungenau | `A` bis `C` |
| Strukturierter CH-Marktplatz | useagain-artig | Kategorie, Preis, Menge, Ort | wenig tiefe Technik | `A_procurement_ready` |
| Professioneller B2B-Shop | Concular-artig | Technik, Zeitfenster, Menge | Preis/Vertrag oft auf Anfrage | `B_design_ready` |
| Restmaterial-Marktplatz | Restado-artig | Preis, Lagerware, Lieferung | keine Rückbau-Herkunft | `A_procurement_ready` |
| Projekt-Pipeline | Salza-artig | frühe Gelegenheit | kaum Artikeldaten | `C_investigation_only` |

---

# 9. Datenqualität pro Quelle

| Quelle | Technische Tiefe | Beschaffungsreife | Logistikdaten | Risikoangaben | Preisangaben |
|---|---:|---:|---:|---:|---:|
| IBS-artig | hoch | niedrig-mittel | mittel | mittel-hoch | niedrig |
| Lokale Bauteilbörse | niedrig-mittel | mittel-hoch | mittel | niedrig | mittel |
| useagain-artig | mittel | hoch | mittel | niedrig-mittel | hoch |
| Concular-artig | hoch | mittel | hoch | mittel | mittel |
| Restmaterial-Marktplatz | niedrig-mittel | hoch | mittel | niedrig | hoch |
| Pipeline-Plattform | niedrig | niedrig | niedrig-mittel | niedrig | niedrig |

---

# 10. Wichtige Designentscheidung

Nicht jede Quelle erzeugt sofort ein vollständiges `Item`.

Manchmal entsteht zuerst nur ein schwacher Datensatz:

```text
Pipeline-Hinweis
→ grobes Item / mixed_lot
→ Bauteilaufnahme
→ einzelne Items
→ technische Attribute
→ Verfügbarkeitssnapshots
→ ReuseAssessment
```

Beispiel:

```text
„Rückbau Bürogebäude Zürich West“
```

wird später zu:

```text
item-101: 34 Leuchten
item-102: 18 Glastrennwände
item-103: 42 Doppelbodenplatten
item-104: 12 Innentüren
```

---

# 11. Mapping-Regeln

## 11.1 Titelbereinigung

```text
Raw:
"Fenster Holz 120x140, 8 Stk., gut, ab Juli"

Mapping:
canonical_title → "Gebrauchte Holzfenster"
component_type → window
primary_material → timber
quantity_available → 8
quantity_unit → piece
width_mm → 1200
height_mm → 1400
condition_normalized → used_good
available_from → Juli
```

## 11.2 Preisbereinigung

```text
Raw:
"CHF 50/Stk. VB"

Mapping:
price_amount → 50
currency → CHF
price_unit → piece
price_type → negotiable
```

## 11.3 Mengenbereinigung

```text
Raw:
"10-15 Stück"

Mapping:
quantity_available → 10
quantity_unit → piece
data_confidence → medium
dimension_notes / availability_notes → "Quelle nennt 10-15 Stück."
```

## 11.4 Zustandbereinigung

```text
Raw:
"gebraucht, schöne Patina, einzelne Kratzer"

Mapping:
condition_raw → "gebraucht, schöne Patina, einzelne Kratzer"
condition_normalized → used_light_wear
damage_notes → "Einzelne Kratzer"
```

## 11.5 Unsichere Schadstoffe

```text
Raw:
"Eternit? Muss geprüft werden."

Mapping:
hazard_flags → ["asbestos", "unknown_pollutants"]
pollutant_test_status → not_tested
risk_level → high
recommended_next_action → request_pollutant_test
```

---

# 12. Minimaler Import-Workflow

```text
1. Raw Listing speichern
2. Titel, Kategorie, Material und Menge extrahieren
3. Item oder VariantBatch erzeugen
4. Listing mit Quelle verbinden
5. AvailabilitySnapshot anlegen
6. Condition normalisieren
7. Risiken und offene Fragen erfassen
8. Dokumente/Fotos anhängen
9. ReuseAssessment berechnen
10. Bei späterem Check neuen AvailabilitySnapshot speichern
```

---

# 13. Fazit

Die Unordnung der Bauteilbörse-Daten ist kein Fehler, sondern ein Merkmal des Feldes.

Ein gutes System muss daher drei Dinge gleichzeitig können:

1. **Unvollständige Daten aufnehmen**
2. **Daten sauber normalisieren**
3. **Unsicherheit sichtbar machen**

Das vorgeschlagene Schema trennt stabile Bauteilinformationen von zeitabhängigen Marktplatzdaten, technischen Attributen, Risiken und Dokumentationsquellen.
