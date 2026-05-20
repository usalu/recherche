// Phase 2.2 — :WiederverwendungsArt facet property (Agent 5, Wave-2)
//   Adds `facet` ∈ {treatment, sourcing, location, intent} to each of the
//   11 :WiederverwendungsArt nodes. Mapping per plan §2.2.

// 2.2.a — treatment (5 nodes)
MATCH (n:WiederverwendungsArt)
WHERE n.id IN ['wva_direkte_wiederverwendung','wva_upcycling','wva_recycling',
               'wva_refurbishment','wva_remanufacturing']
SET n.facet = 'treatment'
RETURN count(n) AS treatment_set;

// 2.2.b — sourcing (3 nodes)
MATCH (n:WiederverwendungsArt)
WHERE n.id IN ['wva_bestandserhalt','wva_urban_mining','wva_weiterbauen_im_bestand']
SET n.facet = 'sourcing'
RETURN count(n) AS sourcing_set;

// 2.2.c — location (1 node)
MATCH (n:WiederverwendungsArt) WHERE n.id = 'wva_same_site_reuse'
SET n.facet = 'location'
RETURN count(n) AS location_set;

// 2.2.d — intent (2 nodes)
MATCH (n:WiederverwendungsArt)
WHERE n.id IN ['wva_design_for_disassembly','wva_adaptives_reuse']
SET n.facet = 'intent'
RETURN count(n) AS intent_set;

// 2.2.e — verify zero unfaceted
MATCH (n:WiederverwendungsArt) WHERE n.facet IS NULL
RETURN collect(n.id) AS missing_facet, count(n) AS missing_count;
