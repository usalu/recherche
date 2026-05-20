// =========================================================================
// Migration 1.4 — Relabel 23 overloaded :Bauwerk placeholders to :Materialdepot
// Wire BETRIEBEN_VON edges to matching operator :Akteur.
// Reversibility: nodes.jsonl in snapshot/ holds the pre-state. Re-add :Bauwerk
// and REMOVE :Materialdepot + DELETE the new BETRIEBEN_VON edges to rollback.
// =========================================================================

// --- 1.4.a Relabel
MATCH (b:Bauwerk)
WHERE b.id IN [
  'bw_crclr_kindl_hall',
  'bw_chiro_itterbeek_reuse_supply_network',
  'bw_berlin_fitout_donor_sources',
  'bw_paris_regional_donor_sources_ferme_du_rail',
  'bw_paris_material_sources_circular_pavilion',
  'bw_p2_massenwohnungsbau_donor_unknown',
  'bw_unknown_demolition_wood_streams',
  'bw_holbein_grosvenor_donor_projects',
  'bw_maison_des_canaux_unspecified_donors',
  'bw_verbiest_lagerhaus_zu_haus_und_atelier',
  'bw_rotor_reuse_stock_charles_malis',
  'bw_messebau_lager_hannover',
  'bw_maison_dna_unknown_brick_donor',
  'bw_externe_stahl_donor_stockholder',
  'bw_unknown_brick_donor_sources_gjg',
  'bw_lo_reninge_reuse_brick_source',
  'bw_unbekanntes_transformationsgebaeude_kellerwaende',
  'bw_unbekannte_donor_buildings_zinneke_material_lots',
  'bw_cleveland_steel_and_tubes_stock',
  'bw_wbs70_donor_groeditz',
  'bw_bellastock_ville_des_terres_l_ile_saint_denis_lager',
  'bw_donor_gebaudegruppe_resource_rows_mauerwerk',
  'bw_elys_ehemaliges_getraenkelager_areal'
]
REMOVE b:Bauwerk SET b:Materialdepot
RETURN count(b) AS relabelled;

// --- 1.4.b Wire to operator Akteur where IDs match
MATCH (d:Materialdepot), (a:Akteur)
WHERE d.id CONTAINS toLower(a.id) OR d.id CONTAINS toLower(replace(a.name,' ','_'))
MERGE (d)-[r:BETRIEBEN_VON]->(a)
ON CREATE SET r.evidence_origin    = 'derived',
              r.evidence_basis     = 'name_match',
              r.evidence_source_id = 'mig_1_4',
              r.evidence_confidence= 'unklar'
RETURN count(r) AS betrieben_von_edges;
