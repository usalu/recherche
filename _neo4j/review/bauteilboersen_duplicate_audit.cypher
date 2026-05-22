// Bauteilboersen / Materialhubs duplicate audit
//
// Run these sections one by one in Neo4j Browser.
// They are read-only. Do not merge/delete from this file.

// 1) Exact duplicate semantic relationships.
// Same start node, relationship type, and end node.
MATCH (a)-[r]->(b)
WITH a, b, type(r) AS rel_type, collect(r) AS rels
WHERE size(rels) > 1
RETURN a, rel_type, b, size(rels) AS duplicate_count, rels
ORDER BY duplicate_count DESC, rel_type
LIMIT 100;

// 2) Reciprocal actor links.
// These are often display-noise rather than bad data: A->B and B->A encode
// the same undirected association twice.
MATCH (a:Akteur)-[r1:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
MATCH (b)-[r2:VERBUNDEN_MIT_AKTEUR]->(a)
WHERE elementId(a) < elementId(b)
RETURN a, r1, b, r2
ORDER BY coalesce(a.name, a.id), coalesce(b.name, b.id)
LIMIT 100;

// 3) Known duplicate-ish materialhub actors from the current processed scan.
// Review these before merging, because some project-local IDs may carry
// project-specific provenance that should be preserved on relationships.
MATCH (a:Akteur)
WHERE a.id IN [
  "rotordc",
  "a_rotordc",
  "a_rotor_dc",
  "a_cleveland_steel_tubes",
  "a_cleveland_steel_and_tubes"
]
OPTIONAL MATCH (a)-[r]-(n)
RETURN a, collect(DISTINCT type(r) + " " + coalesce(n.id, n.name, elementId(n))) AS neighbourhood
ORDER BY coalesce(a.name, a.id);

// 4) Exact-name actor duplicates.
// This catches exact normalized names, but not spelling variants such as
// Rotor DC vs RotorDC.
MATCH (a:Akteur)
WITH toLower(trim(coalesce(a.name, ""))) AS name_key, collect(a) AS actors
WHERE name_key <> "" AND size(actors) > 1
RETURN name_key, size(actors) AS actor_count, actors
ORDER BY actor_count DESC, name_key
LIMIT 100;
