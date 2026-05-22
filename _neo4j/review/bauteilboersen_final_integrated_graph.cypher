// Final Bauteilb?rsen integrated graph visualization query
// Run this in Neo4j Browser after the integration patch is applied.
// It returns the semantic anchors, countries, actor types, roles, operators, and source containers.

WITH [
  "articonnex",
  "backacia",
  "baticycle",
  "batiterre",
  "batrecup",
  "baukarussell",
  "bauteilboerse_bremen",
  "bauteilladen_winterthur",
  "bauteilnetz_deutschland",
  "building_spares_market",
  "concular",
  "cornermat_retrival",
  "cycle_up",
  "cycle_zero",
  "enviromate",
  "gebruiktebouwmaterialen",
  "genbyg",
  "globechain",
  "insert_marketplace",
  "loopfront",
  "material_index",
  "material_reuse_portal",
  "materialenbank_leuven_atelier_circuler",
  "materialnomaden",
  "materialrest24",
  "new_horizon",
  "r_place",
  "raedificare",
  "re_store_harvestmap_vienna",
  "reempro",
  "resource_marktplaats",
  "reuse_and_trade",
  "rotordc",
  "salvo_ltd",
  "salvoweb",
  "salza",
  "skop_marketplace",
  "software_restado",
  "surplus_building_and_plumbing_materials",
  "sustainability_yard",
  "useagain_bauteilclick",
  "warp_it"
] AS anchorIds
MATCH (n)
WHERE n.id IN anchorIds
OPTIONAL MATCH p_country = (n)-[:LIEGT_IN_LAND|GILT_IN_LAND]->(:Land)
OPTIONAL MATCH p_type = (n)-[:HAT_AKTEURTYP]->(:Akteurtyp)
OPTIONAL MATCH p_role = (n)-[:HAT_AKTEURROLLE]->(:Akteurrolle)
OPTIONAL MATCH p_operator = (n)-[:BETRIEBEN_VON]->(:Akteur)
OPTIONAL MATCH p_source = (n)-[:BELEGT_IN]->(:Quelle)
RETURN p_country, p_type, p_role, p_operator, p_source;
