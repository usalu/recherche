// ===========================================================================
//  mig_5_3_relabel_programme.cypher
//  Phase 5.3 — Relabel 4 registry-stub projects from :Projekt to :Programm.
//
//  Reason (plan section 5.3): these 4 ids read as research programmes /
//  portfolio collections, not as buildings.  All 4 lack HAT_BAUTEILGRUPPE
//  but have degree 8-14 via Hürden / Akteur / Land / Stadt etc.; relabel
//  preserves their topology.
//
//  Kept as :Projekt with quality_tier='tier_3_stub':
//    - p_circle_house  (real Danish prototype, no BG yet)
// ===========================================================================

// ---------------------------------------------------------------------------
//  Relabel the 4 programmes.  Properties:
//    original_label  = 'Projekt'
//    migration_origin = '5_3_relabel_to_programm'
//  These markers make the migration reversible per plan section "Reversibility".
// ---------------------------------------------------------------------------

MATCH (p:Projekt)
WHERE p.id IN [
    'p_reuse_logistics',
    'p_vandkunsten_component_reuse',
    'p_architecture_of_reuse_brussels',
    'p_reuse_in_construction_zhaw'
]
REMOVE p:Projekt
SET   p:Programm,
      p.original_label  = 'Projekt',
      p.migration_origin = '5_3_relabel_to_programm';

// ---------------------------------------------------------------------------
//  Audit: confirm the 4 ids now carry :Programm and not :Projekt, and that
//  p_circle_house remains :Projekt with quality_tier='tier_3_stub'.
// ---------------------------------------------------------------------------

MATCH (n)
WHERE n.id IN [
    'p_reuse_logistics',
    'p_vandkunsten_component_reuse',
    'p_architecture_of_reuse_brussels',
    'p_reuse_in_construction_zhaw',
    'p_circle_house'
]
RETURN n.id AS id, labels(n) AS labels, n.quality_tier AS quality_tier,
       n.migration_origin AS migration_origin, n.original_label AS original_label
ORDER BY id;
