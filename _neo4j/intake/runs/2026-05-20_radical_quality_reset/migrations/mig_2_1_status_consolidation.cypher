// Phase 2.1 — Status consolidation (Agent 5, Wave-2)
//   a. Add `kind` ∈ {lifecycle, maturity, unknown} on every :Status node.
//   b. Merge :Status{id:'status_gebaut'} → :Status{id:'status_realisiert'}.
//   c. Merge :Status{id:'status_wettbewerb'} → :Status{id:'status_prototyp'}.
//   d. Remove redundant :Bauwerk.bauwerkstatus / :Bauwerk.status_text props
//      (encoded already on HAT_STATUS edges).
//   e. Remove redundant :Bauteilgruppe.counts_as_* booleans (encoded already
//      on HAT_WIEDERVERWENDUNGSART edges).
//
// Net: :Status 11 → 9 nodes; HAT_STATUS edges preserved (~686).

// 2.1.a.1 — lifecycle kind (4 nodes pre-merge, 3 post-merge once Gebaut is folded)
MATCH (s:Status)
WHERE s.id IN ['status_geplant','status_in_bau','status_realisiert','status_rueckgebaut','status_gebaut']
SET s.kind = 'lifecycle'
RETURN count(s) AS lifecycle_set;

// 2.1.a.2 — maturity kind (4 nodes pre-merge, 3 post-merge once Wettbewerb is folded)
MATCH (s:Status)
WHERE s.id IN ['status_prototyp','status_vorgeschlagen','status_verworfen','status_temporaer','status_wettbewerb']
SET s.kind = 'maturity'
RETURN count(s) AS maturity_set;

// 2.1.a.3 — unknown kind
MATCH (s:Status) WHERE s.id = 'status_unklar'
SET s.kind = 'unknown'
RETURN count(s) AS unknown_set;

// 2.1.b — merge Gebaut → Realisiert (dup-into-canon; mergeRels:true dedupes HAT_STATUS to identical sources)
MATCH (canon:Status {id:'status_realisiert'}), (dup:Status {id:'status_gebaut'})
WITH canon, dup
CALL apoc.refactor.mergeNodes([canon, dup], {properties:'combine', mergeRels:true}) YIELD node
WITH node
SET node.id = 'status_realisiert',
    node.name = 'Realisiert',
    node.kind = 'lifecycle',
    node.aliases = apoc.coll.toSet(coalesce(node.aliases, []) + ['Gebaut','status_gebaut'])
RETURN node.id AS canon_id, node.aliases AS aliases, size(node.aliases) AS alias_count;

// 2.1.c — merge Wettbewerb → Prototyp
MATCH (canon:Status {id:'status_prototyp'}), (dup:Status {id:'status_wettbewerb'})
WITH canon, dup
CALL apoc.refactor.mergeNodes([canon, dup], {properties:'combine', mergeRels:true}) YIELD node
WITH node
SET node.id = 'status_prototyp',
    node.name = 'Prototyp',
    node.kind = 'maturity',
    node.aliases = apoc.coll.toSet(coalesce(node.aliases, []) + ['Wettbewerb','status_wettbewerb'])
RETURN node.id AS canon_id, node.aliases AS aliases, size(node.aliases) AS alias_count;

// 2.1.d — remove redundant Bauwerk status property duplicates
MATCH (b:Bauwerk)
WHERE b.bauwerkstatus IS NOT NULL OR b.status_text IS NOT NULL
WITH collect(b) AS bauwerks
UNWIND bauwerks AS b
REMOVE b.bauwerkstatus, b.status_text
RETURN size(bauwerks) AS bauwerk_props_cleared;

// 2.1.e — remove redundant Bauteilgruppe counts_as_* property duplicates
MATCH (bg:Bauteilgruppe)
WHERE bg.counts_as_direct_reuse    IS NOT NULL
   OR bg.counts_as_bestandserhalt  IS NOT NULL
   OR bg.counts_as_recycling       IS NOT NULL
   OR bg.counts_as_remanufacturing IS NOT NULL
   OR bg.counts_as_surplus         IS NOT NULL
WITH collect(bg) AS bgs
UNWIND bgs AS bg
REMOVE bg.counts_as_direct_reuse,
       bg.counts_as_bestandserhalt,
       bg.counts_as_recycling,
       bg.counts_as_remanufacturing,
       bg.counts_as_surplus
RETURN size(bgs) AS bg_counts_props_cleared;
