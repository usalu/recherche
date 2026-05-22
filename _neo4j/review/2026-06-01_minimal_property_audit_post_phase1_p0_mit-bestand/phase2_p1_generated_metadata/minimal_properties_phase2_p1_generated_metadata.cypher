// Phase 2 P1 generated/import/cache/debug property cleanup.
// Generated for review; backup before applying.
// Generated UTC: 2026-06-01T07:07:52.803787+00:00

// P1.1: node Akteur._archive (122) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.2: node Akteur.actor_registry_loader_seen (187) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.3: node Akteur.candidate_source_status (553) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.4: node Akteur.candidate_source_urls (553) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.5: node Akteur.migration_origin (638) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.6: node Akteur.raw_role_evidence (150) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`raw_role_evidence` IS NOT NULL
REMOVE n.`raw_role_evidence`;

// P1.7: node Akteur.repaired_at (2) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`repaired_at` IS NOT NULL
REMOVE n.`repaired_at`;

// P1.8: node Akteur.source_trace_migrated_at (638) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.9: node Akteur.source_trace_migration (638) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.10: node Akteur.source_urls_updated_at (638) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.11: node Akteur.strict_candidate_url_array_cleanup_at (216) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.12: node Akteur.strict_invalid_url_cleanup_at (134) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.13: node Akteur.strict_source_url_cleanup_at (553) - generated/import/cache/debug metadata
MATCH (n:`Akteur`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.14: node Akteurrolle.migration_origin (24) - generated/import/cache/debug metadata
MATCH (n:`Akteurrolle`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.15: node Akteurrolle.source_urls_updated_at (24) - generated/import/cache/debug metadata
MATCH (n:`Akteurrolle`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.16: node Akteurtyp.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`Akteurtyp`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.17: node Akteurtyp.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`Akteurtyp`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.18: node Akzeptanz.migration_origin (7) - generated/import/cache/debug metadata
MATCH (n:`Akzeptanz`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.19: node Akzeptanz.source_urls_updated_at (7) - generated/import/cache/debug metadata
MATCH (n:`Akzeptanz`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.20: node Aufbereitungsverfahren.candidate_source_status (52) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.21: node Aufbereitungsverfahren.candidate_source_urls (52) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.22: node Aufbereitungsverfahren.created_by (17) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.23: node Aufbereitungsverfahren.last_seen_by (52) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.24: node Aufbereitungsverfahren.migration_origin (62) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.25: node Aufbereitungsverfahren.source_urls_updated_at (62) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.26: node Aufbereitungsverfahren.strict_source_url_cleanup_at (62) - generated/import/cache/debug metadata
MATCH (n:`Aufbereitungsverfahren`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.27: node BauaufgabeIntervention.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`BauaufgabeIntervention`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.28: node BauaufgabeIntervention.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`BauaufgabeIntervention`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.29: node Bauobjektklasse.migration_origin (8) - generated/import/cache/debug metadata
MATCH (n:`Bauobjektklasse`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.30: node Bauobjektklasse.source_urls_updated_at (8) - generated/import/cache/debug metadata
MATCH (n:`Bauobjektklasse`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.31: node Bauobjektrolle.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`Bauobjektrolle`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.32: node Bauobjektrolle.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`Bauobjektrolle`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.33: node Bauproduktstatus.migration_origin (15) - generated/import/cache/debug metadata
MATCH (n:`Bauproduktstatus`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.34: node Bauproduktstatus.source_urls_updated_at (15) - generated/import/cache/debug metadata
MATCH (n:`Bauproduktstatus`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.35: node Bausystem.migration_origin (9) - generated/import/cache/debug metadata
MATCH (n:`Bausystem`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.36: node Bausystem.source_urls_updated_at (9) - generated/import/cache/debug metadata
MATCH (n:`Bausystem`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.37: node Bauteilebene.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`Bauteilebene`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.38: node Bauteilebene.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`Bauteilebene`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.39: node Bauteilgruppe._archive (304) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.40: node Bauteilgruppe.candidate_source_status (304) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.41: node Bauteilgruppe.candidate_source_urls (304) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.42: node Bauteilgruppe.migration_origin (356) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.43: node Bauteilgruppe.source_trace_migrated_at (304) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.44: node Bauteilgruppe.source_trace_migration (304) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.45: node Bauteilgruppe.source_urls_updated_at (356) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.46: node Bauteilgruppe.strict_candidate_url_array_cleanup_at (160) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.47: node Bauteilgruppe.strict_source_url_cleanup_at (356) - generated/import/cache/debug metadata
MATCH (n:`Bauteilgruppe`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.48: node Bauteiltyp.candidate_source_status (8) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.49: node Bauteiltyp.candidate_source_urls (8) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.50: node Bauteiltyp.created_by (7) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.51: node Bauteiltyp.last_seen_by (8) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.52: node Bauteiltyp.migration_origin (23) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.53: node Bauteiltyp.source_trace_migrated_at (23) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.54: node Bauteiltyp.source_trace_migration (23) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.55: node Bauteiltyp.source_urls_updated_at (23) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.56: node Bauteiltyp.strict_source_url_cleanup_at (8) - generated/import/cache/debug metadata
MATCH (n:`Bauteiltyp`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.57: node Bauweise.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`Bauweise`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.58: node Bauweise.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`Bauweise`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.59: node Bauwerk._archive (83) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.60: node Bauwerk.candidate_source_status (172) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.61: node Bauwerk.candidate_source_urls (172) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.62: node Bauwerk.migration_origin (184) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.63: node Bauwerk.source_trace_migrated_at (172) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.64: node Bauwerk.source_trace_migration (172) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.65: node Bauwerk.source_urls_updated_at (184) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.66: node Bauwerk.strict_candidate_url_array_cleanup_at (90) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.67: node Bauwerk.strict_source_url_cleanup_at (184) - generated/import/cache/debug metadata
MATCH (n:`Bauwerk`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.68: node BauwerkEra.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`BauwerkEra`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.69: node BauwerkEra.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`BauwerkEra`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.70: node Beschaffungsweg.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`Beschaffungsweg`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.71: node Beschaffungsweg.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`Beschaffungsweg`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.72: node DataIssue.created_at (22846) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`created_at` IS NOT NULL
REMOVE n.`created_at`;

// P1.73: node DataIssue.detected_at (911) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`detected_at` IS NOT NULL
REMOVE n.`detected_at`;

// P1.74: node DataIssue.found_at (4972) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`found_at` IS NOT NULL
REMOVE n.`found_at`;

// P1.75: node DataIssue.found_by (4972) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`found_by` IS NOT NULL
REMOVE n.`found_by`;

// P1.76: node DataIssue.migration_origin (24436) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.77: node DataIssue.ref_label (4972) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`ref_label` IS NOT NULL
REMOVE n.`ref_label`;

// P1.78: node DataIssue.ref_labels (2084) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`ref_labels` IS NOT NULL
REMOVE n.`ref_labels`;

// P1.79: node DataIssue.resolution_note (4972) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`resolution_note` IS NOT NULL
REMOVE n.`resolution_note`;

// P1.80: node DataIssue.source_trace_migration (22846) - generated/import/cache/debug metadata
MATCH (n:`DataIssue`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.81: node Defekt.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`Defekt`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.82: node Defekt.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`Defekt`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.83: node DeprecatedType.deprecated_at (13) - generated/import/cache/debug metadata
MATCH (n:`DeprecatedType`)
WHERE n.`deprecated_at` IS NOT NULL
REMOVE n.`deprecated_at`;

// P1.84: node DeprecatedType.migration_origin (13) - generated/import/cache/debug metadata
MATCH (n:`DeprecatedType`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.85: node Dossier._archive (78) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.86: node Dossier._created_at (22) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`_created_at` IS NOT NULL
REMOVE n.`_created_at`;

// P1.87: node Dossier._created_by (22) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`_created_by` IS NOT NULL
REMOVE n.`_created_by`;

// P1.88: node Dossier.candidate_source_status (76) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.89: node Dossier.candidate_source_urls (76) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.90: node Dossier.migration_origin (97) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.91: node Dossier.source_trace_migrated_at (97) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.92: node Dossier.source_trace_migration (97) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.93: node Dossier.strict_candidate_url_array_cleanup_at (40) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.94: node Dossier.strict_invalid_url_cleanup_at (70) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.95: node Dossier.strict_source_url_cleanup_at (95) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.96: node Dossier.text_content_loaded_at (92) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`text_content_loaded_at` IS NOT NULL
REMOVE n.`text_content_loaded_at`;

// P1.97: node Dossier.text_content_retry_attempted_at (5) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`text_content_retry_attempted_at` IS NOT NULL
REMOVE n.`text_content_retry_attempted_at`;

// P1.98: node Dossier.text_content_stripped_at (97) - generated/import/cache/debug metadata
MATCH (n:`Dossier`)
WHERE n.`text_content_stripped_at` IS NOT NULL
REMOVE n.`text_content_stripped_at`;

// P1.99: node DossierEntityTarget.migration_origin (2591) - generated/import/cache/debug metadata
MATCH (n:`DossierEntityTarget`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.100: node DossierEntityTarget.unfolding_origin (2591) - generated/import/cache/debug metadata
MATCH (n:`DossierEntityTarget`)
WHERE n.`unfolding_origin` IS NOT NULL
REMOVE n.`unfolding_origin`;

// P1.101: node ExternalLink._archive (625) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.102: node ExternalLink._created_at (622) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`_created_at` IS NOT NULL
REMOVE n.`_created_at`;

// P1.103: node ExternalLink._created_by (622) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`_created_by` IS NOT NULL
REMOVE n.`_created_by`;

// P1.104: node ExternalLink.actor_registry_loader_seen (277) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.105: node ExternalLink.also_in_dossier (930) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`also_in_dossier` IS NOT NULL
REMOVE n.`also_in_dossier`;

// P1.106: node ExternalLink.also_in_edge (930) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`also_in_edge` IS NOT NULL
REMOVE n.`also_in_edge`;

// P1.107: node ExternalLink.also_in_node (930) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`also_in_node` IS NOT NULL
REMOVE n.`also_in_node`;

// P1.108: node ExternalLink.also_in_research (2127) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`also_in_research` IS NOT NULL
REMOVE n.`also_in_research`;

// P1.109: node ExternalLink.created_by (193) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.110: node ExternalLink.extracted_at (5017) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`extracted_at` IS NOT NULL
REMOVE n.`extracted_at`;

// P1.111: node ExternalLink.first_seen_in_dossier (597) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`first_seen_in_dossier` IS NOT NULL
REMOVE n.`first_seen_in_dossier`;

// P1.112: node ExternalLink.first_seen_in_research (2386) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`first_seen_in_research` IS NOT NULL
REMOVE n.`first_seen_in_research`;

// P1.113: node ExternalLink.last_seen_by (193) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.114: node ExternalLink.migration_origin (5017) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.115: node ExternalLink.source_trace_migrated_at (1601) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.116: node ExternalLink.source_trace_migration (1601) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.117: node ExternalLink.strict_invalid_url_cleanup_at (30) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.118: node ExternalLink.strict_node_url_array_cleanup_at (32) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`strict_node_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_node_url_array_cleanup_at`;

// P1.119: node ExternalLink.strict_source_url_cleanup_at (30) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.120: node ExternalLink.url_body_cache_format (1946) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_body_cache_format` IS NOT NULL
REMOVE n.`url_body_cache_format`;

// P1.121: node ExternalLink.url_body_cache_path (1896) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_body_cache_path` IS NOT NULL
REMOVE n.`url_body_cache_path`;

// P1.122: node ExternalLink.url_body_md5 (1896) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_body_md5` IS NOT NULL
REMOVE n.`url_body_md5`;

// P1.123: node ExternalLink.url_last_checked_at (2631) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_last_checked_at` IS NOT NULL
REMOVE n.`url_last_checked_at`;

// P1.124: node ExternalLink.url_last_modified_header (471) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_last_modified_header` IS NOT NULL
REMOVE n.`url_last_modified_header`;

// P1.125: node ExternalLink.url_probe_attempts (2631) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_probe_attempts` IS NOT NULL
REMOVE n.`url_probe_attempts`;

// P1.126: node ExternalLink.url_probe_duration_ms (2631) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_probe_duration_ms` IS NOT NULL
REMOVE n.`url_probe_duration_ms`;

// P1.127: node ExternalLink.url_response_headers (2560) - generated/import/cache/debug metadata
MATCH (n:`ExternalLink`)
WHERE n.`url_response_headers` IS NOT NULL
REMOVE n.`url_response_headers`;

// P1.128: node Funktionswechsel.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`Funktionswechsel`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.129: node Funktionswechsel.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`Funktionswechsel`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.130: node Geltungsbereich.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`Geltungsbereich`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.131: node Huerde.migration_origin (28) - generated/import/cache/debug metadata
MATCH (n:`Huerde`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.132: node Huerde.source_trace_migrated_at (28) - generated/import/cache/debug metadata
MATCH (n:`Huerde`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.133: node Huerde.source_trace_migration (28) - generated/import/cache/debug metadata
MATCH (n:`Huerde`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.134: node Huerde.source_urls_updated_at (28) - generated/import/cache/debug metadata
MATCH (n:`Huerde`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.135: node HuerdeKategorie.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`HuerdeKategorie`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.136: node HuerdeKategorie.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`HuerdeKategorie`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.137: node Kennwert.candidate_source_status (162) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.138: node Kennwert.candidate_source_urls (162) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.139: node Kennwert.loader (255) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`loader` IS NOT NULL
REMOVE n.`loader`;

// P1.140: node Kennwert.migration_origin (255) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.141: node Kennwert.raw_property (255) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`raw_property` IS NOT NULL
REMOVE n.`raw_property`;

// P1.142: node Kennwert.source_trace_migrated_at (255) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.143: node Kennwert.source_trace_migration (255) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.144: node Kennwert.source_urls_updated_at (255) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.145: node Kennwert.strict_candidate_url_array_cleanup_at (88) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.146: node Kennwert.strict_invalid_url_cleanup_at (52) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.147: node Kennwert.strict_source_url_cleanup_at (214) - generated/import/cache/debug metadata
MATCH (n:`Kennwert`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.148: node LCAModule.migration_origin (5) - generated/import/cache/debug metadata
MATCH (n:`LCAModule`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.149: node LCAModule.source_urls_updated_at (5) - generated/import/cache/debug metadata
MATCH (n:`LCAModule`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.150: node Land.actor_registry_loader_seen (10) - generated/import/cache/debug metadata
MATCH (n:`Land`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.151: node Layer.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`Layer`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.152: node Layer.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`Layer`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.153: node Leistungsanforderung.candidate_source_status (41) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.154: node Leistungsanforderung.candidate_source_urls (41) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.155: node Leistungsanforderung.created_by (34) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.156: node Leistungsanforderung.last_seen_by (41) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.157: node Leistungsanforderung.migration_origin (46) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.158: node Leistungsanforderung.source_urls_updated_at (46) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.159: node Leistungsanforderung.strict_source_url_cleanup_at (46) - generated/import/cache/debug metadata
MATCH (n:`Leistungsanforderung`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.160: node Logistik.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`Logistik`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.161: node Logistik.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`Logistik`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.162: node Marktmodell.migration_origin (11) - generated/import/cache/debug metadata
MATCH (n:`Marktmodell`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.163: node Marktmodell.source_urls_updated_at (11) - generated/import/cache/debug metadata
MATCH (n:`Marktmodell`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.164: node MatchingQualitaet.migration_origin (9) - generated/import/cache/debug metadata
MATCH (n:`MatchingQualitaet`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.165: node MatchingQualitaet.source_urls_updated_at (9) - generated/import/cache/debug metadata
MATCH (n:`MatchingQualitaet`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.166: node Material.candidate_source_status (10) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.167: node Material.candidate_source_urls (10) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.168: node Material.created_by (2) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.169: node Material.last_seen_by (8) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.170: node Material.migration_origin (26) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.171: node Material.source_trace_migrated_at (26) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.172: node Material.source_trace_migration (26) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.173: node Material.source_urls_updated_at (26) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.174: node Material.strict_source_url_cleanup_at (10) - generated/import/cache/debug metadata
MATCH (n:`Material`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.175: node Materialdepot._archive (15) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.176: node Materialdepot.candidate_source_status (22) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.177: node Materialdepot.candidate_source_urls (22) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.178: node Materialdepot.migration_origin (22) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.179: node Materialdepot.source_urls_updated_at (22) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.180: node Materialdepot.strict_candidate_url_array_cleanup_at (10) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.181: node Materialdepot.strict_source_url_cleanup_at (22) - generated/import/cache/debug metadata
MATCH (n:`Materialdepot`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.182: node Materialgruppe.migration_origin (11) - generated/import/cache/debug metadata
MATCH (n:`Materialgruppe`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.183: node Materialgruppe.source_urls_updated_at (11) - generated/import/cache/debug metadata
MATCH (n:`Materialgruppe`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.184: node Methode.migration_origin (13) - generated/import/cache/debug metadata
MATCH (n:`Methode`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.185: node Methode.source_trace_migrated_at (13) - generated/import/cache/debug metadata
MATCH (n:`Methode`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.186: node Methode.source_trace_migration (13) - generated/import/cache/debug metadata
MATCH (n:`Methode`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.187: node Methode.source_urls_updated_at (13) - generated/import/cache/debug metadata
MATCH (n:`Methode`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.188: node Norm.candidate_source_status (78) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.189: node Norm.candidate_source_urls (78) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.190: node Norm.migration_origin (103) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.191: node Norm.repaired_at (1) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`repaired_at` IS NOT NULL
REMOVE n.`repaired_at`;

// P1.192: node Norm.source_trace_migrated_at (103) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.193: node Norm.source_trace_migration (103) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.194: node Norm.source_urls_updated_at (103) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.195: node Norm.strict_candidate_url_array_cleanup_at (1) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.196: node Norm.strict_source_url_cleanup_at (78) - generated/import/cache/debug metadata
MATCH (n:`Norm`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.197: node Nutzung.migration_origin (9) - generated/import/cache/debug metadata
MATCH (n:`Nutzung`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.198: node Nutzung.source_urls_updated_at (9) - generated/import/cache/debug metadata
MATCH (n:`Nutzung`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.199: node OntologyAnchor.actor_registry_loader_seen (1) - generated/import/cache/debug metadata
MATCH (n:`OntologyAnchor`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.200: node OntologyAnchor.source_trace_migrated_at (1) - generated/import/cache/debug metadata
MATCH (n:`OntologyAnchor`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.201: node OntologyAnchor.source_trace_migration (1) - generated/import/cache/debug metadata
MATCH (n:`OntologyAnchor`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.202: node Programm._archive (4) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.203: node Programm.actor_registry_loader_seen (10) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.204: node Programm.candidate_source_status (13) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.205: node Programm.candidate_source_urls (13) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.206: node Programm.migration_origin (29) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.207: node Programm.source_trace_migrated_at (13) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.208: node Programm.source_trace_migration (13) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.209: node Programm.source_urls_updated_at (29) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.210: node Programm.strict_candidate_url_array_cleanup_at (2) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.211: node Programm.strict_invalid_url_cleanup_at (6) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.212: node Programm.strict_source_url_cleanup_at (29) - generated/import/cache/debug metadata
MATCH (n:`Programm`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.213: node Projekt._archive (80) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.214: node Projekt.actor_registry_loader_seen (37) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.215: node Projekt.candidate_source_status (85) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.216: node Projekt.candidate_source_urls (85) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.217: node Projekt.migration_origin (86) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.218: node Projekt.raw_year_fields (52) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`raw_year_fields` IS NOT NULL
REMOVE n.`raw_year_fields`;

// P1.219: node Projekt.source_trace_migrated_at (85) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.220: node Projekt.source_trace_migration (85) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.221: node Projekt.source_urls_updated_at (86) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.222: node Projekt.strict_candidate_url_array_cleanup_at (39) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.223: node Projekt.strict_invalid_url_cleanup_at (33) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.224: node Projekt.strict_source_url_cleanup_at (86) - generated/import/cache/debug metadata
MATCH (n:`Projekt`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.225: node Prozessphase.migration_origin (10) - generated/import/cache/debug metadata
MATCH (n:`Prozessphase`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.226: node Prozessphase.source_urls_updated_at (10) - generated/import/cache/debug metadata
MATCH (n:`Prozessphase`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.227: node PruefungNachweis.candidate_source_status (113) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.228: node PruefungNachweis.candidate_source_urls (113) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.229: node PruefungNachweis.created_by (100) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.230: node PruefungNachweis.last_seen_by (113) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.231: node PruefungNachweis.migration_origin (120) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.232: node PruefungNachweis.source_urls_updated_at (120) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.233: node PruefungNachweis.strict_invalid_url_cleanup_at (5) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.234: node PruefungNachweis.strict_source_url_cleanup_at (120) - generated/import/cache/debug metadata
MATCH (n:`PruefungNachweis`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.235: node Quelle._archive (703) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.236: node Quelle._created_at (651) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`_created_at` IS NOT NULL
REMOVE n.`_created_at`;

// P1.237: node Quelle._created_by (651) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`_created_by` IS NOT NULL
REMOVE n.`_created_by`;

// P1.238: node Quelle.actor_registry_loader_seen (277) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`actor_registry_loader_seen` IS NOT NULL
REMOVE n.`actor_registry_loader_seen`;

// P1.239: node Quelle.also_in_dossier (930) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`also_in_dossier` IS NOT NULL
REMOVE n.`also_in_dossier`;

// P1.240: node Quelle.also_in_edge (930) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`also_in_edge` IS NOT NULL
REMOVE n.`also_in_edge`;

// P1.241: node Quelle.also_in_node (930) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`also_in_node` IS NOT NULL
REMOVE n.`also_in_node`;

// P1.242: node Quelle.also_in_research (2127) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`also_in_research` IS NOT NULL
REMOVE n.`also_in_research`;

// P1.243: node Quelle.candidate_source_status (78) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.244: node Quelle.candidate_source_urls (78) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.245: node Quelle.created_at (201) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`created_at` IS NOT NULL
REMOVE n.`created_at`;

// P1.246: node Quelle.created_by (201) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.247: node Quelle.extracted_at (5017) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`extracted_at` IS NOT NULL
REMOVE n.`extracted_at`;

// P1.248: node Quelle.first_seen_in_dossier (597) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`first_seen_in_dossier` IS NOT NULL
REMOVE n.`first_seen_in_dossier`;

// P1.249: node Quelle.first_seen_in_research (2386) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`first_seen_in_research` IS NOT NULL
REMOVE n.`first_seen_in_research`;

// P1.250: node Quelle.last_seen_by (201) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.251: node Quelle.legal_condition_demoted_at (1) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`legal_condition_demoted_at` IS NOT NULL
REMOVE n.`legal_condition_demoted_at`;

// P1.252: node Quelle.migration_origin (5330) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.253: node Quelle.source_trace_migrated_at (1914) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.254: node Quelle.source_trace_migration (1914) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.255: node Quelle.strict_candidate_url_array_cleanup_at (40) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.256: node Quelle.strict_invalid_url_cleanup_at (100) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.257: node Quelle.strict_node_url_array_cleanup_at (39) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`strict_node_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_node_url_array_cleanup_at`;

// P1.258: node Quelle.strict_source_url_cleanup_at (264) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.259: node Quelle.text_content_loaded_at (92) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`text_content_loaded_at` IS NOT NULL
REMOVE n.`text_content_loaded_at`;

// P1.260: node Quelle.text_content_retry_attempted_at (5) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`text_content_retry_attempted_at` IS NOT NULL
REMOVE n.`text_content_retry_attempted_at`;

// P1.261: node Quelle.text_content_stripped_at (97) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`text_content_stripped_at` IS NOT NULL
REMOVE n.`text_content_stripped_at`;

// P1.262: node Quelle.url_body_cache_format (1946) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_body_cache_format` IS NOT NULL
REMOVE n.`url_body_cache_format`;

// P1.263: node Quelle.url_body_cache_path (1896) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_body_cache_path` IS NOT NULL
REMOVE n.`url_body_cache_path`;

// P1.264: node Quelle.url_body_md5 (1896) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_body_md5` IS NOT NULL
REMOVE n.`url_body_md5`;

// P1.265: node Quelle.url_last_checked_at (2631) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_last_checked_at` IS NOT NULL
REMOVE n.`url_last_checked_at`;

// P1.266: node Quelle.url_last_modified_header (471) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_last_modified_header` IS NOT NULL
REMOVE n.`url_last_modified_header`;

// P1.267: node Quelle.url_probe_attempts (2631) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_probe_attempts` IS NOT NULL
REMOVE n.`url_probe_attempts`;

// P1.268: node Quelle.url_probe_duration_ms (2631) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_probe_duration_ms` IS NOT NULL
REMOVE n.`url_probe_duration_ms`;

// P1.269: node Quelle.url_response_headers (2560) - generated/import/cache/debug metadata
MATCH (n:`Quelle`)
WHERE n.`url_response_headers` IS NOT NULL
REMOVE n.`url_response_headers`;

// P1.270: node RechtlicheBedingung.migration_origin (16) - generated/import/cache/debug metadata
MATCH (n:`RechtlicheBedingung`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.271: node RechtlicheBedingung.source_urls_updated_at (14) - generated/import/cache/debug metadata
MATCH (n:`RechtlicheBedingung`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.272: node RechtlicheBedingung.strict_source_url_cleanup_at (16) - generated/import/cache/debug metadata
MATCH (n:`RechtlicheBedingung`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.273: node ResearchDocument.candidate_source_status (2) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.274: node ResearchDocument.candidate_source_urls (2) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.275: node ResearchDocument.created_at (201) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`created_at` IS NOT NULL
REMOVE n.`created_at`;

// P1.276: node ResearchDocument.created_by (201) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.277: node ResearchDocument.extracted_at (193) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`extracted_at` IS NOT NULL
REMOVE n.`extracted_at`;

// P1.278: node ResearchDocument.last_seen_by (201) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.279: node ResearchDocument.legal_condition_demoted_at (1) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`legal_condition_demoted_at` IS NOT NULL
REMOVE n.`legal_condition_demoted_at`;

// P1.280: node ResearchDocument.migration_origin (402) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.281: node ResearchDocument.source_trace_migrated_at (402) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.282: node ResearchDocument.source_trace_migration (402) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.283: node ResearchDocument.strict_invalid_url_cleanup_at (30) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.284: node ResearchDocument.strict_source_url_cleanup_at (169) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.285: node ResearchDocument.url_body_cache_format (162) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_body_cache_format` IS NOT NULL
REMOVE n.`url_body_cache_format`;

// P1.286: node ResearchDocument.url_body_cache_path (148) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_body_cache_path` IS NOT NULL
REMOVE n.`url_body_cache_path`;

// P1.287: node ResearchDocument.url_body_md5 (148) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_body_md5` IS NOT NULL
REMOVE n.`url_body_md5`;

// P1.288: node ResearchDocument.url_last_checked_at (193) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_last_checked_at` IS NOT NULL
REMOVE n.`url_last_checked_at`;

// P1.289: node ResearchDocument.url_last_modified_header (73) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_last_modified_header` IS NOT NULL
REMOVE n.`url_last_modified_header`;

// P1.290: node ResearchDocument.url_probe_attempts (193) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_probe_attempts` IS NOT NULL
REMOVE n.`url_probe_attempts`;

// P1.291: node ResearchDocument.url_probe_duration_ms (193) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_probe_duration_ms` IS NOT NULL
REMOVE n.`url_probe_duration_ms`;

// P1.292: node ResearchDocument.url_response_headers (193) - generated/import/cache/debug metadata
MATCH (n:`ResearchDocument`)
WHERE n.`url_response_headers` IS NOT NULL
REMOVE n.`url_response_headers`;

// P1.293: node Ressourcenquelle.migration_origin (16) - generated/import/cache/debug metadata
MATCH (n:`Ressourcenquelle`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.294: node Ressourcenquelle.source_urls_updated_at (16) - generated/import/cache/debug metadata
MATCH (n:`Ressourcenquelle`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.295: node ReuseRule.candidate_source_status (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.296: node ReuseRule.candidate_source_urls (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.297: node ReuseRule.migration_origin (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.298: node ReuseRule.source_trace_migrated_at (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.299: node ReuseRule.source_trace_migration (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.300: node ReuseRule.source_urls_updated_at (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.301: node ReuseRule.strict_invalid_url_cleanup_at (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_invalid_url_cleanup_at`;

// P1.302: node ReuseRule.strict_source_url_cleanup_at (20) - generated/import/cache/debug metadata
MATCH (n:`ReuseRule`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.303: node Rueckbauverfahren.migration_origin (5) - generated/import/cache/debug metadata
MATCH (n:`Rueckbauverfahren`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.304: node Rueckbauverfahren.source_urls_updated_at (5) - generated/import/cache/debug metadata
MATCH (n:`Rueckbauverfahren`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.305: node Schadstoff.created_by (1) - generated/import/cache/debug metadata
MATCH (n:`Schadstoff`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.306: node Schadstoff.last_seen_by (9) - generated/import/cache/debug metadata
MATCH (n:`Schadstoff`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.307: node Schadstoff.migration_origin (9) - generated/import/cache/debug metadata
MATCH (n:`Schadstoff`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.308: node Schadstoff.source_urls_updated_at (9) - generated/import/cache/debug metadata
MATCH (n:`Schadstoff`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.309: node SectionRef._archive (46) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`_archive` IS NOT NULL
REMOVE n.`_archive`;

// P1.310: node SectionRef._created_at (584) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`_created_at` IS NOT NULL
REMOVE n.`_created_at`;

// P1.311: node SectionRef._created_by (584) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`_created_by` IS NOT NULL
REMOVE n.`_created_by`;

// P1.312: node SectionRef.extracted_at (629) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`extracted_at` IS NOT NULL
REMOVE n.`extracted_at`;

// P1.313: node SectionRef.migration_origin (636) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.314: node SectionRef.source_trace_migrated_at (636) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`source_trace_migrated_at` IS NOT NULL
REMOVE n.`source_trace_migrated_at`;

// P1.315: node SectionRef.source_trace_migration (636) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`source_trace_migration` IS NOT NULL
REMOVE n.`source_trace_migration`;

// P1.316: node SectionRef.strict_node_url_array_cleanup_at (7) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`strict_node_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_node_url_array_cleanup_at`;

// P1.317: node SectionRef.url_body_cache_format (491) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_body_cache_format` IS NOT NULL
REMOVE n.`url_body_cache_format`;

// P1.318: node SectionRef.url_body_cache_path (484) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_body_cache_path` IS NOT NULL
REMOVE n.`url_body_cache_path`;

// P1.319: node SectionRef.url_body_md5 (484) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_body_md5` IS NOT NULL
REMOVE n.`url_body_md5`;

// P1.320: node SectionRef.url_last_checked_at (629) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_last_checked_at` IS NOT NULL
REMOVE n.`url_last_checked_at`;

// P1.321: node SectionRef.url_last_modified_header (97) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_last_modified_header` IS NOT NULL
REMOVE n.`url_last_modified_header`;

// P1.322: node SectionRef.url_probe_attempts (629) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_probe_attempts` IS NOT NULL
REMOVE n.`url_probe_attempts`;

// P1.323: node SectionRef.url_probe_duration_ms (629) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_probe_duration_ms` IS NOT NULL
REMOVE n.`url_probe_duration_ms`;

// P1.324: node SectionRef.url_response_headers (623) - generated/import/cache/debug metadata
MATCH (n:`SectionRef`)
WHERE n.`url_response_headers` IS NOT NULL
REMOVE n.`url_response_headers`;

// P1.325: node Software.candidate_source_status (10) - generated/import/cache/debug metadata
MATCH (n:`Software`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.326: node Software.candidate_source_urls (10) - generated/import/cache/debug metadata
MATCH (n:`Software`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.327: node Software.migration_origin (18) - generated/import/cache/debug metadata
MATCH (n:`Software`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.328: node Software.source_urls_updated_at (18) - generated/import/cache/debug metadata
MATCH (n:`Software`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.329: node Software.strict_candidate_url_array_cleanup_at (4) - generated/import/cache/debug metadata
MATCH (n:`Software`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.330: node Software.strict_source_url_cleanup_at (18) - generated/import/cache/debug metadata
MATCH (n:`Software`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.331: node Status.migration_origin (9) - generated/import/cache/debug metadata
MATCH (n:`Status`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.332: node Status.source_urls_updated_at (9) - generated/import/cache/debug metadata
MATCH (n:`Status`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.333: node Tool.candidate_source_status (4) - generated/import/cache/debug metadata
MATCH (n:`Tool`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.334: node Tool.candidate_source_urls (4) - generated/import/cache/debug metadata
MATCH (n:`Tool`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.335: node Tool.migration_origin (7) - generated/import/cache/debug metadata
MATCH (n:`Tool`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.336: node Tool.source_urls_updated_at (7) - generated/import/cache/debug metadata
MATCH (n:`Tool`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.337: node Tool.strict_candidate_url_array_cleanup_at (3) - generated/import/cache/debug metadata
MATCH (n:`Tool`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.338: node Tool.strict_source_url_cleanup_at (7) - generated/import/cache/debug metadata
MATCH (n:`Tool`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.339: node Tragwerksprinzip.migration_origin (4) - generated/import/cache/debug metadata
MATCH (n:`Tragwerksprinzip`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.340: node Tragwerksprinzip.source_urls_updated_at (4) - generated/import/cache/debug metadata
MATCH (n:`Tragwerksprinzip`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.341: node Verbindungstechnik.candidate_source_status (3) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.342: node Verbindungstechnik.candidate_source_urls (3) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.343: node Verbindungstechnik.created_by (3) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`created_by` IS NOT NULL
REMOVE n.`created_by`;

// P1.344: node Verbindungstechnik.last_seen_by (10) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`last_seen_by` IS NOT NULL
REMOVE n.`last_seen_by`;

// P1.345: node Verbindungstechnik.migration_origin (15) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.346: node Verbindungstechnik.source_urls_updated_at (15) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.347: node Verbindungstechnik.strict_candidate_url_array_cleanup_at (1) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.348: node Verbindungstechnik.strict_source_url_cleanup_at (15) - generated/import/cache/debug metadata
MATCH (n:`Verbindungstechnik`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.349: node WiederverwendungsArt.migration_origin (11) - generated/import/cache/debug metadata
MATCH (n:`WiederverwendungsArt`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.350: node WiederverwendungsArt.source_urls_updated_at (11) - generated/import/cache/debug metadata
MATCH (n:`WiederverwendungsArt`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.351: node Wiederverwendungskette.candidate_source_status (14) - generated/import/cache/debug metadata
MATCH (n:`Wiederverwendungskette`)
WHERE n.`candidate_source_status` IS NOT NULL
REMOVE n.`candidate_source_status`;

// P1.352: node Wiederverwendungskette.candidate_source_urls (14) - generated/import/cache/debug metadata
MATCH (n:`Wiederverwendungskette`)
WHERE n.`candidate_source_urls` IS NOT NULL
REMOVE n.`candidate_source_urls`;

// P1.353: node Wiederverwendungskette.migration_origin (14) - generated/import/cache/debug metadata
MATCH (n:`Wiederverwendungskette`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.354: node Wiederverwendungskette.source_urls_updated_at (14) - generated/import/cache/debug metadata
MATCH (n:`Wiederverwendungskette`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.355: node Wiederverwendungskette.strict_candidate_url_array_cleanup_at (4) - generated/import/cache/debug metadata
MATCH (n:`Wiederverwendungskette`)
WHERE n.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE n.`strict_candidate_url_array_cleanup_at`;

// P1.356: node Wiederverwendungskette.strict_source_url_cleanup_at (14) - generated/import/cache/debug metadata
MATCH (n:`Wiederverwendungskette`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.357: node Wirtschaft.migration_origin (12) - generated/import/cache/debug metadata
MATCH (n:`Wirtschaft`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.358: node Wirtschaft.source_urls_updated_at (12) - generated/import/cache/debug metadata
MATCH (n:`Wirtschaft`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.359: node Zertifizierungssystem.migration_origin (8) - generated/import/cache/debug metadata
MATCH (n:`Zertifizierungssystem`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.360: node Zertifizierungssystem.source_urls_updated_at (8) - generated/import/cache/debug metadata
MATCH (n:`Zertifizierungssystem`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.361: node Zertifizierungssystem.strict_source_url_cleanup_at (8) - generated/import/cache/debug metadata
MATCH (n:`Zertifizierungssystem`)
WHERE n.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE n.`strict_source_url_cleanup_at`;

// P1.362: node ZustandsKlasse.migration_origin (6) - generated/import/cache/debug metadata
MATCH (n:`ZustandsKlasse`)
WHERE n.`migration_origin` IS NOT NULL
REMOVE n.`migration_origin`;

// P1.363: node ZustandsKlasse.source_urls_updated_at (6) - generated/import/cache/debug metadata
MATCH (n:`ZustandsKlasse`)
WHERE n.`source_urls_updated_at` IS NOT NULL
REMOVE n.`source_urls_updated_at`;

// P1.364: relationship ANCHORED_BY.candidate_source_basis (252) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.365: relationship ANCHORED_BY.candidate_source_url_node_ids (252) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.366: relationship ANCHORED_BY.candidate_source_urls (252) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.367: relationship ANCHORED_BY.source_status_corrected_at (695) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`source_status_corrected_at` IS NOT NULL
REMOVE r.`source_status_corrected_at`;

// P1.368: relationship ANCHORED_BY.source_trace_migrated_at (695) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.369: relationship ANCHORED_BY.source_trace_migration (695) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.370: relationship ANCHORED_BY.strict_source_url_cleanup_at (252) - generated/import/cache/debug metadata
MATCH ()-[r:`ANCHORED_BY`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.371: relationship APPLIES_IN.candidate_source_basis (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.372: relationship APPLIES_IN.candidate_source_url_node_ids (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.373: relationship APPLIES_IN.candidate_source_urls (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.374: relationship APPLIES_IN.source_status_normalized_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.375: relationship APPLIES_IN.source_trace_migrated_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.376: relationship APPLIES_IN.source_trace_migration (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.377: relationship APPLIES_IN.strict_source_url_cleanup_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_IN`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.378: relationship APPLIES_TO.candidate_source_basis (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.379: relationship APPLIES_TO.candidate_source_url_node_ids (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.380: relationship APPLIES_TO.candidate_source_urls (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.381: relationship APPLIES_TO.source_status_normalized_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.382: relationship APPLIES_TO.source_trace_migrated_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.383: relationship APPLIES_TO.source_trace_migration (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.384: relationship APPLIES_TO.strict_source_url_cleanup_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`APPLIES_TO`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.385: relationship BELEGT_IN._cell_hash (2713) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`_cell_hash` IS NOT NULL
REMOVE r.`_cell_hash`;

// P1.386: relationship BELEGT_IN._created_at (2713) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`_created_at` IS NOT NULL
REMOVE r.`_created_at`;

// P1.387: relationship BELEGT_IN._created_by (2713) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`_created_by` IS NOT NULL
REMOVE r.`_created_by`;

// P1.388: relationship BELEGT_IN.candidate_source_basis (1424) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.389: relationship BELEGT_IN.candidate_source_url_node_ids (1424) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.390: relationship BELEGT_IN.candidate_source_urls (1424) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.391: relationship BELEGT_IN.migration_origin (3303) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.392: relationship BELEGT_IN.source_status_normalized_at (4730) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.393: relationship BELEGT_IN.source_trace_migrated_at (4730) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.394: relationship BELEGT_IN.source_trace_migration (4730) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.395: relationship BELEGT_IN.source_url_last_checked_at (3143) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`source_url_last_checked_at` IS NOT NULL
REMOVE r.`source_url_last_checked_at`;

// P1.396: relationship BELEGT_IN.strict_candidate_url_array_cleanup_at (644) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE r.`strict_candidate_url_array_cleanup_at`;

// P1.397: relationship BELEGT_IN.strict_invalid_url_cleanup_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_invalid_url_cleanup_at`;

// P1.398: relationship BELEGT_IN.strict_source_url_cleanup_at (1424) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.399: relationship BELEGT_IN.verified_at (2713) - generated/import/cache/debug metadata
MATCH ()-[r:`BELEGT_IN`]->()
WHERE r.`verified_at` IS NOT NULL
REMOVE r.`verified_at`;

// P1.400: relationship BERECHNET_NACH_MODUL.migration_origin (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BERECHNET_NACH_MODUL`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.401: relationship BERECHNET_NACH_MODUL.source_status_normalized_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BERECHNET_NACH_MODUL`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.402: relationship BERECHNET_NACH_MODUL.source_trace_migrated_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BERECHNET_NACH_MODUL`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.403: relationship BERECHNET_NACH_MODUL.source_trace_migration (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BERECHNET_NACH_MODUL`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.404: relationship BETEILIGT_AN.source_status_normalized_at (561) - generated/import/cache/debug metadata
MATCH ()-[r:`BETEILIGT_AN`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.405: relationship BETEILIGT_AN.source_trace_migrated_at (561) - generated/import/cache/debug metadata
MATCH ()-[r:`BETEILIGT_AN`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.406: relationship BETEILIGT_AN.source_trace_migration (561) - generated/import/cache/debug metadata
MATCH ()-[r:`BETEILIGT_AN`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.407: relationship BETRIEBEN_VON.source_status_normalized_at (2) - generated/import/cache/debug metadata
MATCH ()-[r:`BETRIEBEN_VON`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.408: relationship BETRIEBEN_VON.source_trace_migrated_at (2) - generated/import/cache/debug metadata
MATCH ()-[r:`BETRIEBEN_VON`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.409: relationship BETRIEBEN_VON.source_trace_migration (2) - generated/import/cache/debug metadata
MATCH ()-[r:`BETRIEBEN_VON`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.410: relationship BUILT_IN_ERA.migration_origin (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BUILT_IN_ERA`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.411: relationship BUILT_IN_ERA.source_status_normalized_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BUILT_IN_ERA`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.412: relationship BUILT_IN_ERA.source_trace_migrated_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BUILT_IN_ERA`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.413: relationship BUILT_IN_ERA.source_trace_migration (8) - generated/import/cache/debug metadata
MATCH ()-[r:`BUILT_IN_ERA`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.414: relationship CITED_FROM_DOSSIER.migration_origin (6104) - generated/import/cache/debug metadata
MATCH ()-[r:`CITED_FROM_DOSSIER`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.415: relationship CITED_FROM_DOSSIER.source_status_corrected_at (6104) - generated/import/cache/debug metadata
MATCH ()-[r:`CITED_FROM_DOSSIER`]->()
WHERE r.`source_status_corrected_at` IS NOT NULL
REMOVE r.`source_status_corrected_at`;

// P1.416: relationship CITED_FROM_DOSSIER.source_url_last_checked_at (3457) - generated/import/cache/debug metadata
MATCH ()-[r:`CITED_FROM_DOSSIER`]->()
WHERE r.`source_url_last_checked_at` IS NOT NULL
REMOVE r.`source_url_last_checked_at`;

// P1.417: relationship CITED_FROM_DOSSIER.unfolding_origin (6104) - generated/import/cache/debug metadata
MATCH ()-[r:`CITED_FROM_DOSSIER`]->()
WHERE r.`unfolding_origin` IS NOT NULL
REMOVE r.`unfolding_origin`;

// P1.418: relationship CONCERNS.migration_origin (43431) - generated/import/cache/debug metadata
MATCH ()-[r:`CONCERNS`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.419: relationship CONCERNS.source_status_corrected_at (3520) - generated/import/cache/debug metadata
MATCH ()-[r:`CONCERNS`]->()
WHERE r.`source_status_corrected_at` IS NOT NULL
REMOVE r.`source_status_corrected_at`;

// P1.420: relationship CONCERNS.source_trace_migrated_at (3520) - generated/import/cache/debug metadata
MATCH ()-[r:`CONCERNS`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.421: relationship CONCERNS.source_trace_migration (3520) - generated/import/cache/debug metadata
MATCH ()-[r:`CONCERNS`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.422: relationship CONCERNS.source_url_last_checked_at (3456) - generated/import/cache/debug metadata
MATCH ()-[r:`CONCERNS`]->()
WHERE r.`source_url_last_checked_at` IS NOT NULL
REMOVE r.`source_url_last_checked_at`;

// P1.423: relationship CONCERNS.strict_invalid_url_cleanup_at (64) - generated/import/cache/debug metadata
MATCH ()-[r:`CONCERNS`]->()
WHERE r.`strict_invalid_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_invalid_url_cleanup_at`;

// P1.424: relationship ERHALT_FOERDERUNG_DURCH.source_status_normalized_at (3) - generated/import/cache/debug metadata
MATCH ()-[r:`ERHALT_FOERDERUNG_DURCH`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.425: relationship ERHALT_FOERDERUNG_DURCH.source_trace_migrated_at (3) - generated/import/cache/debug metadata
MATCH ()-[r:`ERHALT_FOERDERUNG_DURCH`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.426: relationship ERHALT_FOERDERUNG_DURCH.source_trace_migration (3) - generated/import/cache/debug metadata
MATCH ()-[r:`ERHALT_FOERDERUNG_DURCH`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.427: relationship EXACT_MATCH_CANDIDATE.migration_origin (305) - generated/import/cache/debug metadata
MATCH ()-[r:`EXACT_MATCH_CANDIDATE`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.428: relationship EXACT_MATCH_CANDIDATE.unfolding_origin (305) - generated/import/cache/debug metadata
MATCH ()-[r:`EXACT_MATCH_CANDIDATE`]->()
WHERE r.`unfolding_origin` IS NOT NULL
REMOVE r.`unfolding_origin`;

// P1.429: relationship FROM_DONOR.source_status_normalized_at (284) - generated/import/cache/debug metadata
MATCH ()-[r:`FROM_DONOR`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.430: relationship FROM_DONOR.source_trace_migrated_at (284) - generated/import/cache/debug metadata
MATCH ()-[r:`FROM_DONOR`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.431: relationship FROM_DONOR.source_trace_migration (284) - generated/import/cache/debug metadata
MATCH ()-[r:`FROM_DONOR`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.432: relationship GEHÖRT_ZU.source_status_normalized_at (249) - generated/import/cache/debug metadata
MATCH ()-[r:`GEHÖRT_ZU`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.433: relationship GEHÖRT_ZU.source_trace_migrated_at (249) - generated/import/cache/debug metadata
MATCH ()-[r:`GEHÖRT_ZU`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.434: relationship GEHÖRT_ZU.source_trace_migration (249) - generated/import/cache/debug metadata
MATCH ()-[r:`GEHÖRT_ZU`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.435: relationship GILT_IN_LAND.migration_origin (42) - generated/import/cache/debug metadata
MATCH ()-[r:`GILT_IN_LAND`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.436: relationship GILT_IN_LAND.source_status_normalized_at (160) - generated/import/cache/debug metadata
MATCH ()-[r:`GILT_IN_LAND`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.437: relationship GILT_IN_LAND.source_trace_migrated_at (160) - generated/import/cache/debug metadata
MATCH ()-[r:`GILT_IN_LAND`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.438: relationship GILT_IN_LAND.source_trace_migration (160) - generated/import/cache/debug metadata
MATCH ()-[r:`GILT_IN_LAND`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.439: relationship HAS_BAUWERK.migration_origin (183) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_BAUWERK`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.440: relationship HAS_BAUWERK.source_status_normalized_at (183) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_BAUWERK`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.441: relationship HAS_BAUWERK.source_trace_migrated_at (183) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_BAUWERK`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.442: relationship HAS_BAUWERK.source_trace_migration (183) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_BAUWERK`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.443: relationship HAS_RISK_POLLUTANT.migration_origin (4) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_RISK_POLLUTANT`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.444: relationship HAS_RISK_POLLUTANT.source_status_normalized_at (795) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_RISK_POLLUTANT`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.445: relationship HAS_RISK_POLLUTANT.source_trace_migrated_at (795) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_RISK_POLLUTANT`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.446: relationship HAS_RISK_POLLUTANT.source_trace_migration (795) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_RISK_POLLUTANT`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.447: relationship HAS_RISK_POLLUTANT.verified_at (4) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_RISK_POLLUTANT`]->()
WHERE r.`verified_at` IS NOT NULL
REMOVE r.`verified_at`;

// P1.448: relationship HAS_SOURCE_LINK.migration_origin (20) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_SOURCE_LINK`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.449: relationship HAS_SOURCE_LINK.source_status_corrected_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_SOURCE_LINK`]->()
WHERE r.`source_status_corrected_at` IS NOT NULL
REMOVE r.`source_status_corrected_at`;

// P1.450: relationship HAS_SOURCE_LINK.source_trace_migrated_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_SOURCE_LINK`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.451: relationship HAS_SOURCE_LINK.source_trace_migration (20) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_SOURCE_LINK`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.452: relationship HAS_SOURCE_LINK.source_url_last_checked_at (20) - generated/import/cache/debug metadata
MATCH ()-[r:`HAS_SOURCE_LINK`]->()
WHERE r.`source_url_last_checked_at` IS NOT NULL
REMOVE r.`source_url_last_checked_at`;

// P1.453: relationship HAT_AKTEURROLLE.candidate_source_basis (535) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.454: relationship HAT_AKTEURROLLE.candidate_source_url_node_ids (535) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.455: relationship HAT_AKTEURROLLE.candidate_source_urls (535) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.456: relationship HAT_AKTEURROLLE.migration_origin (535) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.457: relationship HAT_AKTEURROLLE.source_status_normalized_at (1162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.458: relationship HAT_AKTEURROLLE.source_trace_migrated_at (1162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.459: relationship HAT_AKTEURROLLE.source_trace_migration (1162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.460: relationship HAT_AKTEURROLLE.strict_source_url_cleanup_at (535) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.461: relationship HAT_AKTEURTYP.candidate_source_basis (188) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.462: relationship HAT_AKTEURTYP.candidate_source_url_node_ids (188) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.463: relationship HAT_AKTEURTYP.candidate_source_urls (188) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.464: relationship HAT_AKTEURTYP.migration_origin (188) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.465: relationship HAT_AKTEURTYP.source_status_normalized_at (648) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.466: relationship HAT_AKTEURTYP.source_trace_migrated_at (648) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.467: relationship HAT_AKTEURTYP.source_trace_migration (648) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.468: relationship HAT_AKTEURTYP.strict_source_url_cleanup_at (188) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.469: relationship HAT_AUFBEREITUNG.candidate_source_basis (22) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.470: relationship HAT_AUFBEREITUNG.candidate_source_url_node_ids (22) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.471: relationship HAT_AUFBEREITUNG.candidate_source_urls (22) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.472: relationship HAT_AUFBEREITUNG.migration_origin (22) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.473: relationship HAT_AUFBEREITUNG.source_status_normalized_at (433) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.474: relationship HAT_AUFBEREITUNG.source_trace_migrated_at (433) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.475: relationship HAT_AUFBEREITUNG.source_trace_migration (433) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.476: relationship HAT_AUFBEREITUNG.strict_source_url_cleanup_at (22) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.477: relationship HAT_AUFBEREITUNG.verified_at (22) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_AUFBEREITUNG`]->()
WHERE r.`verified_at` IS NOT NULL
REMOVE r.`verified_at`;

// P1.478: relationship HAT_BAUOBJEKTKLASSE.source_status_normalized_at (224) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUOBJEKTKLASSE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.479: relationship HAT_BAUOBJEKTKLASSE.source_trace_migrated_at (224) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUOBJEKTKLASSE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.480: relationship HAT_BAUOBJEKTKLASSE.source_trace_migration (224) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUOBJEKTKLASSE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.481: relationship HAT_BAUOBJEKTROLLE.source_status_normalized_at (225) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUOBJEKTROLLE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.482: relationship HAT_BAUOBJEKTROLLE.source_trace_migrated_at (225) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUOBJEKTROLLE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.483: relationship HAT_BAUOBJEKTROLLE.source_trace_migration (225) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUOBJEKTROLLE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.484: relationship HAT_BAUPRODUKTSTATUS.source_status_normalized_at (65) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUPRODUKTSTATUS`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.485: relationship HAT_BAUPRODUKTSTATUS.source_trace_migrated_at (65) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUPRODUKTSTATUS`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.486: relationship HAT_BAUPRODUKTSTATUS.source_trace_migration (65) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUPRODUKTSTATUS`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.487: relationship HAT_BAUSYSTEM.source_status_normalized_at (64) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUSYSTEM`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.488: relationship HAT_BAUSYSTEM.source_trace_migrated_at (64) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUSYSTEM`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.489: relationship HAT_BAUSYSTEM.source_trace_migration (64) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUSYSTEM`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.490: relationship HAT_BAUTEILEBENE.source_status_normalized_at (359) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILEBENE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.491: relationship HAT_BAUTEILEBENE.source_trace_migrated_at (359) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILEBENE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.492: relationship HAT_BAUTEILEBENE.source_trace_migration (359) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILEBENE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.493: relationship HAT_BAUTEILGRUPPE.candidate_source_basis (246) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.494: relationship HAT_BAUTEILGRUPPE.candidate_source_url_node_ids (246) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.495: relationship HAT_BAUTEILGRUPPE.candidate_source_urls (246) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.496: relationship HAT_BAUTEILGRUPPE.migration_origin (252) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.497: relationship HAT_BAUTEILGRUPPE.source_status_normalized_at (356) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.498: relationship HAT_BAUTEILGRUPPE.source_trace_migrated_at (356) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.499: relationship HAT_BAUTEILGRUPPE.source_trace_migration (356) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.500: relationship HAT_BAUTEILGRUPPE.strict_candidate_url_array_cleanup_at (130) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE r.`strict_candidate_url_array_cleanup_at`;

// P1.501: relationship HAT_BAUTEILGRUPPE.strict_source_url_cleanup_at (246) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILGRUPPE`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.502: relationship HAT_BAUTEILTYP.source_status_normalized_at (593) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILTYP`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.503: relationship HAT_BAUTEILTYP.source_trace_migrated_at (593) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILTYP`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.504: relationship HAT_BAUTEILTYP.source_trace_migration (593) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUTEILTYP`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.505: relationship HAT_BAUWEISE.source_status_normalized_at (128) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUWEISE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.506: relationship HAT_BAUWEISE.source_trace_migrated_at (128) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUWEISE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.507: relationship HAT_BAUWEISE.source_trace_migration (128) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BAUWEISE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.508: relationship HAT_BESCHAFFUNGSWEG.source_status_normalized_at (274) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BESCHAFFUNGSWEG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.509: relationship HAT_BESCHAFFUNGSWEG.source_trace_migrated_at (274) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BESCHAFFUNGSWEG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.510: relationship HAT_BESCHAFFUNGSWEG.source_trace_migration (274) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_BESCHAFFUNGSWEG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.511: relationship HAT_DEFEKT.source_status_normalized_at (42) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_DEFEKT`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.512: relationship HAT_DEFEKT.source_trace_migrated_at (42) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_DEFEKT`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.513: relationship HAT_DEFEKT.source_trace_migration (42) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_DEFEKT`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.514: relationship HAT_DEFEKT_BEFUND.source_status_normalized_at (25) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_DEFEKT_BEFUND`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.515: relationship HAT_DEFEKT_BEFUND.source_trace_migrated_at (25) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_DEFEKT_BEFUND`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.516: relationship HAT_DEFEKT_BEFUND.source_trace_migration (25) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_DEFEKT_BEFUND`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.517: relationship HAT_FUNKTIONSWECHSEL.source_status_normalized_at (293) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_FUNKTIONSWECHSEL`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.518: relationship HAT_FUNKTIONSWECHSEL.source_trace_migrated_at (293) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_FUNKTIONSWECHSEL`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.519: relationship HAT_FUNKTIONSWECHSEL.source_trace_migration (293) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_FUNKTIONSWECHSEL`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.520: relationship HAT_GELTUNGSBEREICH.migration_origin (15) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_GELTUNGSBEREICH`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.521: relationship HAT_HUERDE.demoted_at (57) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDE`]->()
WHERE r.`demoted_at` IS NOT NULL
REMOVE r.`demoted_at`;

// P1.522: relationship HAT_HUERDE.migration_origin (57) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDE`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.523: relationship HAT_HUERDE.source_status_normalized_at (1044) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.524: relationship HAT_HUERDE.source_trace_migrated_at (1044) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.525: relationship HAT_HUERDE.source_trace_migration (1044) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.526: relationship HAT_HUERDEKATEGORIE.source_status_normalized_at (167) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDEKATEGORIE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.527: relationship HAT_HUERDEKATEGORIE.source_trace_migrated_at (167) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDEKATEGORIE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.528: relationship HAT_HUERDEKATEGORIE.source_trace_migration (167) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_HUERDEKATEGORIE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.529: relationship HAT_INTERVENTION.source_status_normalized_at (144) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_INTERVENTION`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.530: relationship HAT_INTERVENTION.source_trace_migrated_at (144) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_INTERVENTION`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.531: relationship HAT_INTERVENTION.source_trace_migration (144) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_INTERVENTION`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.532: relationship HAT_KENNWERT.candidate_source_basis (162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.533: relationship HAT_KENNWERT.candidate_source_url_node_ids (162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.534: relationship HAT_KENNWERT.candidate_source_urls (162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.535: relationship HAT_KENNWERT.migration_origin (255) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.536: relationship HAT_KENNWERT.source_status_normalized_at (255) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.537: relationship HAT_KENNWERT.source_trace_migrated_at (255) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.538: relationship HAT_KENNWERT.source_trace_migration (255) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.539: relationship HAT_KENNWERT.strict_candidate_url_array_cleanup_at (88) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`strict_candidate_url_array_cleanup_at` IS NOT NULL
REMOVE r.`strict_candidate_url_array_cleanup_at`;

// P1.540: relationship HAT_KENNWERT.strict_source_url_cleanup_at (162) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.541: relationship HAT_LEISTUNGSANFORDERUNG.source_status_normalized_at (549) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LEISTUNGSANFORDERUNG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.542: relationship HAT_LEISTUNGSANFORDERUNG.source_trace_migrated_at (549) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LEISTUNGSANFORDERUNG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.543: relationship HAT_LEISTUNGSANFORDERUNG.source_trace_migration (549) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LEISTUNGSANFORDERUNG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.544: relationship HAT_LOGISTIK.demoted_at (58) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LOGISTIK`]->()
WHERE r.`demoted_at` IS NOT NULL
REMOVE r.`demoted_at`;

// P1.545: relationship HAT_LOGISTIK.migration_origin (58) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LOGISTIK`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.546: relationship HAT_LOGISTIK.source_status_normalized_at (494) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LOGISTIK`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.547: relationship HAT_LOGISTIK.source_trace_migrated_at (494) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LOGISTIK`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.548: relationship HAT_LOGISTIK.source_trace_migration (494) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_LOGISTIK`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.549: relationship HAT_MARKTMODELL.source_status_normalized_at (374) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MARKTMODELL`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.550: relationship HAT_MARKTMODELL.source_trace_migrated_at (374) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MARKTMODELL`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.551: relationship HAT_MARKTMODELL.source_trace_migration (374) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MARKTMODELL`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.552: relationship HAT_MATCHINGQUALITAET.source_status_normalized_at (182) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MATCHINGQUALITAET`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.553: relationship HAT_MATCHINGQUALITAET.source_trace_migrated_at (182) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MATCHINGQUALITAET`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.554: relationship HAT_MATCHINGQUALITAET.source_trace_migration (182) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MATCHINGQUALITAET`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.555: relationship HAT_MATERIALGRUPPE.source_status_normalized_at (503) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MATERIALGRUPPE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.556: relationship HAT_MATERIALGRUPPE.source_trace_migrated_at (503) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MATERIALGRUPPE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.557: relationship HAT_MATERIALGRUPPE.source_trace_migration (503) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_MATERIALGRUPPE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.558: relationship HAT_METHODE.demoted_at (63) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_METHODE`]->()
WHERE r.`demoted_at` IS NOT NULL
REMOVE r.`demoted_at`;

// P1.559: relationship HAT_METHODE.migration_origin (63) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_METHODE`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.560: relationship HAT_METHODE.source_status_normalized_at (595) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_METHODE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.561: relationship HAT_METHODE.source_trace_migrated_at (595) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_METHODE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.562: relationship HAT_METHODE.source_trace_migration (595) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_METHODE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.563: relationship HAT_NUTZUNG.source_status_normalized_at (214) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_NUTZUNG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.564: relationship HAT_NUTZUNG.source_trace_migrated_at (214) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_NUTZUNG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.565: relationship HAT_NUTZUNG.source_trace_migration (214) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_NUTZUNG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.566: relationship HAT_PROZESSPHASE.demoted_at (119) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PROZESSPHASE`]->()
WHERE r.`demoted_at` IS NOT NULL
REMOVE r.`demoted_at`;

// P1.567: relationship HAT_PROZESSPHASE.migration_origin (119) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PROZESSPHASE`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.568: relationship HAT_PROZESSPHASE.source_status_normalized_at (812) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PROZESSPHASE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.569: relationship HAT_PROZESSPHASE.source_trace_migrated_at (812) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PROZESSPHASE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.570: relationship HAT_PROZESSPHASE.source_trace_migration (812) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PROZESSPHASE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.571: relationship HAT_PRUEFUNG.candidate_source_basis (51) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.572: relationship HAT_PRUEFUNG.candidate_source_url_node_ids (51) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.573: relationship HAT_PRUEFUNG.candidate_source_urls (51) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.574: relationship HAT_PRUEFUNG.migration_origin (63) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.575: relationship HAT_PRUEFUNG.source_status_normalized_at (408) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.576: relationship HAT_PRUEFUNG.source_trace_migrated_at (408) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.577: relationship HAT_PRUEFUNG.source_trace_migration (408) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.578: relationship HAT_PRUEFUNG.strict_source_url_cleanup_at (51) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.579: relationship HAT_PRUEFUNG.verified_at (63) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_PRUEFUNG`]->()
WHERE r.`verified_at` IS NOT NULL
REMOVE r.`verified_at`;

// P1.580: relationship HAT_RECHTLICHE_BEDINGUNG.migration_origin (15) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RECHTLICHE_BEDINGUNG`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.581: relationship HAT_RECHTLICHE_BEDINGUNG.source_status_normalized_at (15) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RECHTLICHE_BEDINGUNG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.582: relationship HAT_RECHTLICHE_BEDINGUNG.source_trace_migrated_at (15) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RECHTLICHE_BEDINGUNG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.583: relationship HAT_RECHTLICHE_BEDINGUNG.source_trace_migration (15) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RECHTLICHE_BEDINGUNG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.584: relationship HAT_RESSOURCENQUELLE.source_status_normalized_at (552) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RESSOURCENQUELLE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.585: relationship HAT_RESSOURCENQUELLE.source_trace_migrated_at (552) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RESSOURCENQUELLE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.586: relationship HAT_RESSOURCENQUELLE.source_trace_migration (552) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RESSOURCENQUELLE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.587: relationship HAT_RUECKBAUVERFAHREN.source_status_normalized_at (299) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RUECKBAUVERFAHREN`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.588: relationship HAT_RUECKBAUVERFAHREN.source_trace_migrated_at (299) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RUECKBAUVERFAHREN`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.589: relationship HAT_RUECKBAUVERFAHREN.source_trace_migration (299) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_RUECKBAUVERFAHREN`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.590: relationship HAT_STATUS.source_status_normalized_at (655) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_STATUS`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.591: relationship HAT_STATUS.source_trace_migrated_at (655) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_STATUS`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.592: relationship HAT_STATUS.source_trace_migration (655) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_STATUS`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.593: relationship HAT_TRAGWERKSPRINZIP.source_status_normalized_at (71) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_TRAGWERKSPRINZIP`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.594: relationship HAT_TRAGWERKSPRINZIP.source_trace_migrated_at (71) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_TRAGWERKSPRINZIP`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.595: relationship HAT_TRAGWERKSPRINZIP.source_trace_migration (71) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_TRAGWERKSPRINZIP`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.596: relationship HAT_TYPISCHEN_BAUPRODUKTSTATUS.source_status_normalized_at (19) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_TYPISCHEN_BAUPRODUKTSTATUS`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.597: relationship HAT_TYPISCHEN_BAUPRODUKTSTATUS.source_trace_migrated_at (19) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_TYPISCHEN_BAUPRODUKTSTATUS`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.598: relationship HAT_TYPISCHEN_BAUPRODUKTSTATUS.source_trace_migration (19) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_TYPISCHEN_BAUPRODUKTSTATUS`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.599: relationship HAT_VERBINDUNGSTECHNIK.candidate_source_basis (1) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.600: relationship HAT_VERBINDUNGSTECHNIK.candidate_source_url_node_ids (1) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.601: relationship HAT_VERBINDUNGSTECHNIK.candidate_source_urls (1) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.602: relationship HAT_VERBINDUNGSTECHNIK.migration_origin (1) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.603: relationship HAT_VERBINDUNGSTECHNIK.source_status_normalized_at (128) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.604: relationship HAT_VERBINDUNGSTECHNIK.source_trace_migrated_at (128) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.605: relationship HAT_VERBINDUNGSTECHNIK.source_trace_migration (128) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.606: relationship HAT_VERBINDUNGSTECHNIK.strict_source_url_cleanup_at (1) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.607: relationship HAT_VERBINDUNGSTECHNIK.verified_at (1) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_VERBINDUNGSTECHNIK`]->()
WHERE r.`verified_at` IS NOT NULL
REMOVE r.`verified_at`;

// P1.608: relationship HAT_WIEDERVERWENDUNGSART.source_status_normalized_at (604) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIEDERVERWENDUNGSART`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.609: relationship HAT_WIEDERVERWENDUNGSART.source_trace_migrated_at (604) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIEDERVERWENDUNGSART`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.610: relationship HAT_WIEDERVERWENDUNGSART.source_trace_migration (604) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIEDERVERWENDUNGSART`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.611: relationship HAT_WIRTSCHAFT.source_status_normalized_at (41) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIRTSCHAFT`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.612: relationship HAT_WIRTSCHAFT.source_trace_migrated_at (41) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIRTSCHAFT`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.613: relationship HAT_WIRTSCHAFT.source_trace_migration (41) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIRTSCHAFT`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.614: relationship HAT_WIRTSCHAFTSASPEKT.source_status_normalized_at (11) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIRTSCHAFTSASPEKT`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.615: relationship HAT_WIRTSCHAFTSASPEKT.source_trace_migrated_at (11) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIRTSCHAFTSASPEKT`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.616: relationship HAT_WIRTSCHAFTSASPEKT.source_trace_migration (11) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_WIRTSCHAFTSASPEKT`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.617: relationship HAT_ZERTIFIZIERUNG.migration_origin (12) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZERTIFIZIERUNG`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.618: relationship HAT_ZERTIFIZIERUNG.source_status_normalized_at (12) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZERTIFIZIERUNG`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.619: relationship HAT_ZERTIFIZIERUNG.source_trace_migrated_at (12) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZERTIFIZIERUNG`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.620: relationship HAT_ZERTIFIZIERUNG.source_trace_migration (12) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZERTIFIZIERUNG`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.621: relationship HAT_ZERTIFIZIERUNG.verified_at (12) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZERTIFIZIERUNG`]->()
WHERE r.`verified_at` IS NOT NULL
REMOVE r.`verified_at`;

// P1.622: relationship HAT_ZUSTANDSKLASSE.source_status_normalized_at (36) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZUSTANDSKLASSE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.623: relationship HAT_ZUSTANDSKLASSE.source_trace_migrated_at (36) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZUSTANDSKLASSE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.624: relationship HAT_ZUSTANDSKLASSE.source_trace_migration (36) - generated/import/cache/debug metadata
MATCH ()-[r:`HAT_ZUSTANDSKLASSE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.625: relationship INTO_RECEIVER.source_status_normalized_at (345) - generated/import/cache/debug metadata
MATCH ()-[r:`INTO_RECEIVER`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.626: relationship INTO_RECEIVER.source_trace_migrated_at (345) - generated/import/cache/debug metadata
MATCH ()-[r:`INTO_RECEIVER`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.627: relationship INTO_RECEIVER.source_trace_migration (345) - generated/import/cache/debug metadata
MATCH ()-[r:`INTO_RECEIVER`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.628: relationship IST_UNTERVERFAHREN_VON.source_status_normalized_at (28) - generated/import/cache/debug metadata
MATCH ()-[r:`IST_UNTERVERFAHREN_VON`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.629: relationship IST_UNTERVERFAHREN_VON.source_trace_migrated_at (28) - generated/import/cache/debug metadata
MATCH ()-[r:`IST_UNTERVERFAHREN_VON`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.630: relationship IST_UNTERVERFAHREN_VON.source_trace_migration (28) - generated/import/cache/debug metadata
MATCH ()-[r:`IST_UNTERVERFAHREN_VON`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.631: relationship LIEGT_IN_LAND.candidate_source_basis (196) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.632: relationship LIEGT_IN_LAND.candidate_source_url_node_ids (196) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.633: relationship LIEGT_IN_LAND.candidate_source_urls (196) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.634: relationship LIEGT_IN_LAND.migration_origin (196) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.635: relationship LIEGT_IN_LAND.source_status_normalized_at (504) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.636: relationship LIEGT_IN_LAND.source_trace_migrated_at (504) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.637: relationship LIEGT_IN_LAND.source_trace_migration (504) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.638: relationship LIEGT_IN_LAND.strict_source_url_cleanup_at (196) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_LAND`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.639: relationship LIEGT_IN_STADT.source_status_normalized_at (252) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_STADT`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.640: relationship LIEGT_IN_STADT.source_trace_migrated_at (252) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_STADT`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.641: relationship LIEGT_IN_STADT.source_trace_migration (252) - generated/import/cache/debug metadata
MATCH ()-[r:`LIEGT_IN_STADT`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.642: relationship METHODENGRUNDLAGE_NORM.migration_origin (8) - generated/import/cache/debug metadata
MATCH ()-[r:`METHODENGRUNDLAGE_NORM`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.643: relationship METHODENGRUNDLAGE_NORM.source_status_normalized_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`METHODENGRUNDLAGE_NORM`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.644: relationship METHODENGRUNDLAGE_NORM.source_trace_migrated_at (8) - generated/import/cache/debug metadata
MATCH ()-[r:`METHODENGRUNDLAGE_NORM`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.645: relationship METHODENGRUNDLAGE_NORM.source_trace_migration (8) - generated/import/cache/debug metadata
MATCH ()-[r:`METHODENGRUNDLAGE_NORM`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.646: relationship NUTZT_BAUWERK.source_status_normalized_at (166) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_BAUWERK`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.647: relationship NUTZT_BAUWERK.source_trace_migrated_at (166) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_BAUWERK`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.648: relationship NUTZT_BAUWERK.source_trace_migration (166) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_BAUWERK`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.649: relationship NUTZT_MATERIAL.source_status_normalized_at (468) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_MATERIAL`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.650: relationship NUTZT_MATERIAL.source_trace_migrated_at (468) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_MATERIAL`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.651: relationship NUTZT_MATERIAL.source_trace_migration (468) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_MATERIAL`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.652: relationship NUTZT_SOFTWARE.source_status_normalized_at (50) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_SOFTWARE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.653: relationship NUTZT_SOFTWARE.source_trace_migrated_at (50) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_SOFTWARE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.654: relationship NUTZT_SOFTWARE.source_trace_migration (50) - generated/import/cache/debug metadata
MATCH ()-[r:`NUTZT_SOFTWARE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.655: relationship REFERENZIERT_NORM._derived_from_lzm (15) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`_derived_from_lzm` IS NOT NULL
REMOVE r.`_derived_from_lzm`;

// P1.656: relationship REFERENZIERT_NORM.candidate_source_basis (93) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.657: relationship REFERENZIERT_NORM.candidate_source_url_node_ids (93) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.658: relationship REFERENZIERT_NORM.candidate_source_urls (93) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.659: relationship REFERENZIERT_NORM.source_status_normalized_at (145) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.660: relationship REFERENZIERT_NORM.source_trace_migrated_at (145) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.661: relationship REFERENZIERT_NORM.source_trace_migration (145) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.662: relationship REFERENZIERT_NORM.strict_source_url_cleanup_at (93) - generated/import/cache/debug metadata
MATCH ()-[r:`REFERENZIERT_NORM`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.663: relationship RELEVANT_FOR.migration_origin (100) - generated/import/cache/debug metadata
MATCH ()-[r:`RELEVANT_FOR`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.664: relationship RELEVANT_FOR.source_status_normalized_at (100) - generated/import/cache/debug metadata
MATCH ()-[r:`RELEVANT_FOR`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.665: relationship RELEVANT_FOR.source_trace_migrated_at (100) - generated/import/cache/debug metadata
MATCH ()-[r:`RELEVANT_FOR`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.666: relationship RELEVANT_FOR.source_trace_migration (100) - generated/import/cache/debug metadata
MATCH ()-[r:`RELEVANT_FOR`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.667: relationship REQUIRES_VERIFICATION_FOR.migration_origin (4) - generated/import/cache/debug metadata
MATCH ()-[r:`REQUIRES_VERIFICATION_FOR`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.668: relationship REQUIRES_VERIFICATION_FOR.source_status_normalized_at (339) - generated/import/cache/debug metadata
MATCH ()-[r:`REQUIRES_VERIFICATION_FOR`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.669: relationship REQUIRES_VERIFICATION_FOR.source_trace_migrated_at (339) - generated/import/cache/debug metadata
MATCH ()-[r:`REQUIRES_VERIFICATION_FOR`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.670: relationship REQUIRES_VERIFICATION_FOR.source_trace_migration (339) - generated/import/cache/debug metadata
MATCH ()-[r:`REQUIRES_VERIFICATION_FOR`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.671: relationship STUB_PROJECT_LINK.candidate_source_basis (133) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.672: relationship STUB_PROJECT_LINK.candidate_source_url_node_ids (133) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.673: relationship STUB_PROJECT_LINK.candidate_source_urls (133) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.674: relationship STUB_PROJECT_LINK.migration_origin (133) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.675: relationship STUB_PROJECT_LINK.source_status_normalized_at (169) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.676: relationship STUB_PROJECT_LINK.source_trace_migrated_at (169) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.677: relationship STUB_PROJECT_LINK.source_trace_migration (169) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.678: relationship STUB_PROJECT_LINK.strict_source_url_cleanup_at (133) - generated/import/cache/debug metadata
MATCH ()-[r:`STUB_PROJECT_LINK`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;

// P1.679: relationship TEILT_LAYER.migration_origin (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TEILT_LAYER`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.680: relationship TEILT_LAYER.source_status_normalized_at (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TEILT_LAYER`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.681: relationship TEILT_LAYER.source_trace_migrated_at (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TEILT_LAYER`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.682: relationship TEILT_LAYER.source_trace_migration (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TEILT_LAYER`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.683: relationship TEIL_VON_KETTE.source_status_normalized_at (14) - generated/import/cache/debug metadata
MATCH ()-[r:`TEIL_VON_KETTE`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.684: relationship TEIL_VON_KETTE.source_trace_migrated_at (14) - generated/import/cache/debug metadata
MATCH ()-[r:`TEIL_VON_KETTE`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.685: relationship TEIL_VON_KETTE.source_trace_migration (14) - generated/import/cache/debug metadata
MATCH ()-[r:`TEIL_VON_KETTE`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.686: relationship TEIL_VON_PROGRAMM.source_status_normalized_at (35) - generated/import/cache/debug metadata
MATCH ()-[r:`TEIL_VON_PROGRAMM`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.687: relationship TEIL_VON_PROGRAMM.source_trace_migrated_at (35) - generated/import/cache/debug metadata
MATCH ()-[r:`TEIL_VON_PROGRAMM`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.688: relationship TEIL_VON_PROGRAMM.source_trace_migration (35) - generated/import/cache/debug metadata
MATCH ()-[r:`TEIL_VON_PROGRAMM`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.689: relationship TYPISCH_BEI_BAUTEILTYP.source_status_normalized_at (10) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_BAUTEILTYP`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.690: relationship TYPISCH_BEI_BAUTEILTYP.source_trace_migrated_at (10) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_BAUTEILTYP`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.691: relationship TYPISCH_BEI_BAUTEILTYP.source_trace_migration (10) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_BAUTEILTYP`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.692: relationship TYPISCH_BEI_ERA.source_status_normalized_at (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_ERA`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.693: relationship TYPISCH_BEI_ERA.source_trace_migrated_at (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_ERA`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.694: relationship TYPISCH_BEI_ERA.source_trace_migration (15) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_ERA`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.695: relationship TYPISCH_BEI_MATERIAL.source_status_normalized_at (91) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_MATERIAL`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.696: relationship TYPISCH_BEI_MATERIAL.source_trace_migrated_at (91) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_MATERIAL`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.697: relationship TYPISCH_BEI_MATERIAL.source_trace_migration (91) - generated/import/cache/debug metadata
MATCH ()-[r:`TYPISCH_BEI_MATERIAL`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.698: relationship VERBUNDEN_MIT_AKTEUR.candidate_source_basis (250) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`candidate_source_basis` IS NOT NULL
REMOVE r.`candidate_source_basis`;

// P1.699: relationship VERBUNDEN_MIT_AKTEUR.candidate_source_url_node_ids (250) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`candidate_source_url_node_ids` IS NOT NULL
REMOVE r.`candidate_source_url_node_ids`;

// P1.700: relationship VERBUNDEN_MIT_AKTEUR.candidate_source_urls (250) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`candidate_source_urls` IS NOT NULL
REMOVE r.`candidate_source_urls`;

// P1.701: relationship VERBUNDEN_MIT_AKTEUR.cleanup_bauteilboersen_bidirectional_dedup_at (27) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`cleanup_bauteilboersen_bidirectional_dedup_at` IS NOT NULL
REMOVE r.`cleanup_bauteilboersen_bidirectional_dedup_at`;

// P1.702: relationship VERBUNDEN_MIT_AKTEUR.migration_origin (250) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`migration_origin` IS NOT NULL
REMOVE r.`migration_origin`;

// P1.703: relationship VERBUNDEN_MIT_AKTEUR.source_status_normalized_at (298) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`source_status_normalized_at` IS NOT NULL
REMOVE r.`source_status_normalized_at`;

// P1.704: relationship VERBUNDEN_MIT_AKTEUR.source_trace_migrated_at (298) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`source_trace_migrated_at` IS NOT NULL
REMOVE r.`source_trace_migrated_at`;

// P1.705: relationship VERBUNDEN_MIT_AKTEUR.source_trace_migration (298) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`source_trace_migration` IS NOT NULL
REMOVE r.`source_trace_migration`;

// P1.706: relationship VERBUNDEN_MIT_AKTEUR.strict_source_url_cleanup_at (250) - generated/import/cache/debug metadata
MATCH ()-[r:`VERBUNDEN_MIT_AKTEUR`]->()
WHERE r.`strict_source_url_cleanup_at` IS NOT NULL
REMOVE r.`strict_source_url_cleanup_at`;
