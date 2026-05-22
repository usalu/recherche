# Bauteilboerse Eingabeinterface - kompakte Kurzfassung

> Entwurfshilfe fuer ein Interface, abgeleitet aus einer archivierten Schema-Datei.
> Nicht kanonische Graph-Wahrheit; vor Import gegen den aktuellen Neo4j-Workflow pruefen.

## Zweck

Nutzer sollen wiederverwendbare Bauteile/Materialien schnell erfassen koennen: Identitaet, Menge, Quelle, Preis/Verfuegbarkeit, Zustand, Risiko, Logistik und Nachweise.

## Formular-Blueprint

| Bereich | Wichtigste Felder | UI-Hinweis |
|---|---|---|
| Bauteil | `canonical_title`, `component_family`, `component_type`, `material_family`, `primary_material`, `secondary_materials`, `newness_type`, `structural_role`, `is_batch`, `short_description` | Kernbereich; Kategorie- und Materialfelder als abhaengige Dropdowns |
| Menge / Masse | `quantity`, `quantity_unit`, `length_mm`, `width_mm`, `height_mm`, `thickness_mm`, `diameter_mm`, `area_m2`, `volume_m3`, `weight_kg_per_unit`, `total_weight_kg`, `dimension_notes` | Zahlenfelder mit Einheit; Varianten als wiederholbarer Block |
| Inserat / Quelle | `source_url`, `canonical_url`, `external_listing_id`, `external_article_number`, `original_title`, `platform_category_raw`, `page_status`, `data_source_type`, `first_seen_at`, `last_seen_at`, `last_verified_at`, `data_confidence` | URLs direkt am Datensatz speichern; Originaltitel behalten |
| Verfuegbarkeit / Preis | `availability_status`, `quantity_available`, `price_amount`, `currency`, `price_unit`, `price_type`, `vat_included`, `minimum_order_quantity`, `available_from`, `available_until`, `pickup_deadline`, `reservation_possible`, `contact_required`, `commercial_only`, `warranty_status`, `availability_notes` | Als zeitbezogenen Schnappschuss behandeln |
| Standort / Herkunft | `location_type`, `name`, `postcode`, `city`, `region`, `country`, `address_visible`, `latitude`, `longitude`, `source_building_name`, `source_project_name`, `source_building_year`, `installation_year`, `original_use`, `original_position`, `owner_or_provider` | Aktuellen Standort und Provenienz getrennt anzeigen |
| Zustand / Risiko | `condition_normalized`, `condition_raw`, `wear_level`, `damage_notes`, `missing_parts`, `cleaned_status`, `tested_status`, `refurbished_status`, `inspection_date`, `inspection_method`, `risk_level`, `hazard_flags`, `pollutant_test_status`, `structural_verification_required`, `fire_certificate_status`, `ce_marking_status`, `engineer_review_status`, `reuse_restrictions`, `risk_notes` | Sichtbar platzieren, da entscheidend fuer Wiederverwendung |
| Logistik | `deconstruction_status`, `demounting_responsibility`, `transport_mode`, `loading_included`, `crane_required`, `forklift_required`, `palletized`, `packaging_status`, `access_constraints`, `logistics_notes`, `deconstruction_window_start`, `deconstruction_window_end` | Rueckbau, Abholung, Transport und Zugang buendeln |
| Dokumente | `asset_type`, `asset_url`, `file_format`, `language`, `title`, `description`, `source_date`, `checked_at`, `asset_confidence` | Wiederholbarer Upload-/Linkblock fuer Fotos, PDFs, CAD, BIM, Pruefberichte |
| Umwelt | `co2_saved_kg`, `embodied_carbon_kgco2e`, `grey_energy_mj`, `avoided_waste_kg`, `reuse_percentage`, `lca_method`, `environmental_data_confidence` | Optionaler Expertenbereich, nur bei vorhandenen Daten anzeigen |

## Technische Zusatzfelder nach Kategorie

| Kategorie | Nur die wichtigsten Zusatzfelder anzeigen |
|---|---|
| Beton / tragend | `concrete_type`, `precast_or_cast_in_situ`, `prestressed`, `reinforcement_type`, `compressive_strength_mpa`, `load_capacity_known`, `connection_type`, `crack_condition`, `spalling_condition` |
| Holz | `wood_species`, `solid_or_engineered`, `strength_class`, `moisture_content_percent`, `treatment_type`, `insect_damage`, `fungal_damage`, `reuse_as_structural_allowed` |
| Metall / Stahl | `metal_type`, `steel_grade`, `profile_type`, `section_size`, `corrosion_level`, `coating_type`, `galvanized`, `load_capacity_known` |
| Fenster / Glas / Fassade | `frame_material`, `glazing_type`, `number_of_panes`, `u_value_w_m2k`, `g_value`, `sound_reduction_db`, `fire_rating`, `opening_type`, `seal_condition`, `glass_damage` |
| Tueren | `door_type`, `leaf_material`, `frame_included`, `hardware_included`, `fire_rating`, `sound_rating_db`, `security_class`, `swing_direction`, `lock_included`, `key_available` |
| Ausbauoberflaechen | `finish_material`, `format_size_mm`, `thickness_mm`, `coverage_area_m2`, `adhesive_residue`, `cleaning_required`, `color_variation`, `batch_consistency` |
| Sanitaer / Kueche / Einbauten | `fixture_type`, `manufacturer`, `model`, `material`, `color`, `fittings_included`, `tested_for_leaks`, `hygiene_condition` |
| Gebaeudetechnik | `mep_category`, `manufacturer`, `model`, `power_rating`, `voltage`, `capacity`, `energy_label`, `commissioning_year`, `tested_operational`, `certification_status` |
| Schuettgut / Restmaterial | `material_grade`, `grain_size`, `packaging_unit`, `batch_weight_kg`, `contamination_level`, `storage_condition`, `waste_code`, `recycling_route` |

## Zentrale Dropdowns

| Feld | Werte |
|---|---|
| `component_family` | `structure`, `envelope`, `interior_fitout`, `building_services`, `site_external`, `bulk_material` |
| `material_family` | `mineral`, `timber_biobased`, `metal`, `glass`, `polymer`, `composite`, `mixed_unknown` |
| `availability_status` | `available`, `available_soon`, `reserved`, `sold`, `out_of_stock`, `on_request`, `unknown` |
| `condition_normalized` | `new`, `new_old_stock`, `like_new`, `used_good`, `used_light_wear`, `used_heavy_wear`, `damaged_repairable`, `untested`, `unknown` |
| `risk_level` | `low`, `medium`, `high`, `critical`, `unknown` |
| `hazard_flags` | `asbestos`, `pcb`, `pah`, `lead_paint`, `chlorides`, `mold`, `corrosion`, `moisture_damage`, `structural_uncertainty`, `missing_certification`, `none_known`, `unknown_pollutants` |
| `deconstruction_status` | `still_installed`, `dismantling_planned`, `being_dismantled`, `dismantled`, `stored_on_site`, `stored_in_warehouse`, `in_shop`, `unknown` |
| `transport_mode` | `pickup_only`, `delivery_available`, `shipping_available`, `freight_required`, `local_delivery_only`, `self_organized`, `unknown` |
| `price_type` | `fixed`, `negotiable`, `price_on_request`, `auction`, `free`, `donation`, `unknown` |
| `quantity_unit` | `piece`, `lot`, `set`, `pair`, `linear_m`, `m2`, `m3`, `kg`, `tonne`, `pallet`, `package`, `roll`, `unknown` |

## Interface-Regeln

- Tabs oder Schritte: Bauteil, Menge, Quelle, Verfuegbarkeit, Standort, Zustand/Risiko, Logistik, Dokumente, Umwelt.
- Nur Kernfelder zu Beginn verpflichtend machen; unvollstaendige Entwuerfe erlauben.
- Abhaengige Dropdowns nutzen: `component_family` -> `component_type`, `material_family` -> `primary_material`, `component_type` -> technische Felder.
- Interne IDs nicht manuell abfragen, ausser bei strukturiertem Import.
- Rohtext neben normalisierten Feldern behalten, damit Originalformulierungen nicht verloren gehen.
- Unsicherheit mit `unknown` erfassen statt mit leerem Freitext.
