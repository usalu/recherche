// Bauteilboersen / Materialhubs: cleaned country + actor graph
//
// Paste into Neo4j Browser and use Graph view.
// This is intentionally stricter than the broad scan:
// - uses canonical actor-registry hubs only (`source_scope = actor_registry_context`)
// - adds Bauteilnetz Deutschland as network context
// - uses directed actor links from the hub/network to avoid reciprocal double edges
// - returns paths, so Neo4j renders a graph

MATCH p =
  (root:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
WHERE coalesce(root.source_scope, "") = "actor_registry_context"
RETURN p

UNION

MATCH p =
  (root:Akteur)-[:`GEHÖRT_ZU`|LIEGT_IN_LAND]->(:Land)
WHERE root.id = "bauteilnetz_deutschland"
   OR (
     coalesce(root.source_scope, "") = "actor_registry_context"
     AND EXISTS {
       MATCH (root)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     }
   )
RETURN p

UNION

MATCH p =
  (root:Akteur)-[:HAT_AKTEURROLLE]->(:Akteurrolle)
WHERE root.id = "bauteilnetz_deutschland"
   OR (
     coalesce(root.source_scope, "") = "actor_registry_context"
     AND EXISTS {
       MATCH (root)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     }
   )
RETURN p

UNION

MATCH p =
  (root:Akteur)-[:VERBUNDEN_MIT_AKTEUR]->(:Akteur)
WHERE root.id = "bauteilnetz_deutschland"
   OR (
     coalesce(root.source_scope, "") = "actor_registry_context"
     AND EXISTS {
       MATCH (root)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     }
   )
RETURN p

UNION

MATCH p =
  (:Akteur {id: "bauteilnetz_deutschland"})-[:HAT_AKTEURTYP]->(:Akteurtyp)
RETURN p;
