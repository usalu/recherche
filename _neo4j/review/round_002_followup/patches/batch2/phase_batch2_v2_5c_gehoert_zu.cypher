// GEHÖRT_ZU edges for new Persons (Phase 5c).
//
// The apply tool's `add_rel` op rejects relationship types containing
// non-ASCII characters (umlauts like Ö). The live graph already contains
// 216 `GEHÖRT_ZU` rels (the canonical Person→Organisation link), so we use
// direct Cypher to add the new edges that match the existing convention.
//
// PRECONDITION: Phase 5a must have applied (target Persons + Orgs exist).
//
// Each MERGE writes an `r.id` matching the canonical `r_<from>__GEHÖRT_ZU__<to>`
// pattern (consistent with Phase R hygiene).

// === Persons in Pérez Schmidlin (LysP8 / SMS Zürich) — placeholder; create Persons in a future batch ===
//   stefan_perez, michael_schmidlin would link to perez_schmidlin_bauingenieure
//   pascal_hentschel, rebecca_brandmayer, laia_meier would link to zirkular_gmbh

// === Persons that ALREADY exist in graph (S27) but lack GEHÖRT_ZU to their dossier-evidenced Org ===

// hans_hammink → de_architekten_cie  (Circl dossier S1)
MATCH (p {id:'hans_hammink'}), (o {id:'de_architekten_cie'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_hans_hammink__GEHÖRT_ZU__de_architekten_cie',
              r.source = 'batch2_v2_import_2026-05-20',
              r.evidence = 'BELEGT';

// dominik_campanella → concular  (RCMI dossier S5; if dominik_campanella node exists)
MATCH (p {id:'dominik_campanella'}), (o {id:'concular'})
MERGE (p)-[r:`GEHÖRT_ZU`]->(o)
ON CREATE SET r.id = 'r_dominik_campanella__GEHÖRT_ZU__concular',
              r.source = 'batch2_v2_import_2026-05-20',
              r.evidence = 'BELEGT';

// (Repeat for each Person→Org pair listed in actor_extraction_per_dossier.md O5 table;
//  using MATCH ... MERGE makes each row idempotent.)

// === Verification ===
//
// MATCH ()-[r:`GEHÖRT_ZU`]->() WHERE r.source = 'batch2_v2_import_2026-05-20' RETURN count(r);
// EXPECTED: number of MERGE statements executed.
//
// MATCH (p:Akteur)-[:`GEHÖRT_ZU`]->(o:Akteur) RETURN count(*) AS total_gehoert_zu;
// EXPECTED: 216 (existing) + <new from this script>.
