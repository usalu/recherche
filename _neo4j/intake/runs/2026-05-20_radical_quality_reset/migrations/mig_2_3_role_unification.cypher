// Phase 2.3 — Single role system (Agent 5, Wave-2)
//   a. Preserve every BETEILIGT_AN.rolle_text string into
//      Akteur.raw_role_evidence (list-of-strings audit column).
//   b. Strip the rolle_text property from BETEILIGT_AN.
//   c. Merge :Akteurrolle{id:'ar_reuse_beratung'} → 'ar_reuse_zirkularitaetsberatung'.
//
// Net: BETEILIGT_AN loses one property; :Akteurrolle 25 → 24 nodes.

// 2.3.a — accumulate rolle_text strings per Akteur (as "<text> @ <target_ref>")
MATCH (a:Akteur)-[r:BETEILIGT_AN]->(t)
WHERE r.rolle_text IS NOT NULL AND trim(r.rolle_text) <> ''
WITH a, trim(r.rolle_text) AS rt,
     coalesce(t.id, t.name, toString(elementId(t))) AS target_ref
WITH a, collect(DISTINCT rt + ' @ ' + target_ref) AS new_entries
WITH a, apoc.coll.toSet(coalesce(a.raw_role_evidence, []) + new_entries) AS combined
SET a.raw_role_evidence = combined
RETURN count(a) AS akteurs_updated,
       sum(size(combined)) AS total_evidence_strings_after;

// 2.3.b — remove rolle_text from BETEILIGT_AN edges
MATCH ()-[r:BETEILIGT_AN]->() WHERE r.rolle_text IS NOT NULL
WITH collect(r) AS rels
UNWIND rels AS r
REMOVE r.rolle_text
RETURN size(rels) AS rolle_text_removed;

// 2.3.c — merge ar_reuse_beratung → ar_reuse_zirkularitaetsberatung
MATCH (canon:Akteurrolle {id:'ar_reuse_zirkularitaetsberatung'}),
      (dup  :Akteurrolle {id:'ar_reuse_beratung'})
WITH canon, dup
CALL apoc.refactor.mergeNodes([canon, dup], {properties:'combine', mergeRels:true}) YIELD node
WITH node
SET node.id = 'ar_reuse_zirkularitaetsberatung',
    node.name = 'Reuse_Zirkularitaetsberatung',
    node.aliases = apoc.coll.toSet(coalesce(node.aliases, []) + ['Reuse_Beratung','ar_reuse_beratung'])
RETURN node.id AS canon_id, node.aliases AS aliases, size(node.aliases) AS alias_count;
