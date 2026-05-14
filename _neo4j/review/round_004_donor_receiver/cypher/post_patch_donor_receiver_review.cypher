// Post-patch donor/receiver completeness review
// A Bauteilgruppe is considered donor-resolved if it has an exact AUS_BAUWERK edge,
// a HAT_RESSOURCENQUELLE edge, or a terminal donor_resolution_status.

MATCH (bg:Bauteilgruppe)
WHERE coalesce(bg.direct_reuse, true) = true
WITH bg,
     EXISTS { (bg)-[:AUS_BAUWERK]->(:Bauwerk) } AS hasDonorBuilding,
     EXISTS { (bg)-[:HAT_RESSOURCENQUELLE]->(:Ressourcenquelle) } AS hasResourceSource
WHERE NOT hasDonorBuilding
  AND NOT hasResourceSource
  AND coalesce(bg.donor_resolution_status,'') NOT IN ['not_applicable_retention','planned_not_built','unknown']
RETURN bg.id AS bg_id, bg.name AS bg_name, bg.donor_resolution_status AS status
ORDER BY bg_id;

// Missing receiver check remains stricter: every direct-reuse Bauteilgruppe should still have a receiver Bauwerk,
// unless receiver_resolution_status marks it as deferred/unknown.
MATCH (bg:Bauteilgruppe)
WHERE coalesce(bg.direct_reuse, true) = true
  AND NOT EXISTS { (bg)-[:EINGEBAUT_IN]->(:Bauwerk) }
  AND coalesce(bg.receiver_resolution_status,'') NOT IN ['unknown','not_applicable_retention','planned_not_built']
RETURN bg.id AS bg_id, bg.name AS bg_name, bg.receiver_resolution_status AS status
ORDER BY bg_id;
