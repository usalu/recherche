// =========================================================================
// Migration 1.6 — Merge 7 verified :Akteur duplicate pairs.
//   apoc.refactor.mergeNodes([canon, dup], {properties:'combine', mergeRels:true})
//   keeps the FIRST node (canon) and moves dup's edges onto it.
//   The merged-in id is appended to the canon's `aliases` list for traceability.
//
// Pairs (canonical id  <-  merge_in id):
//   baubuero_in_situ            <- bauburo_in_situ           (orthographic canon)
//   plp_architecture            <- ak_plp_architecture
//   ZRS_Architekten_Ingenieure  <- zrs_architekten
//   loeliger_strub              <- loeliger_strub_architektur
//   zedfactory_bill_dunster     <- bill_dunster_zedfactory
//   opera                       <- opera_pm
//   bellastock                  <- Bellastock                (case-collision; lowercase wins)
//
// Net effect on :Akteur count: 660 -> 653.
// Reversibility: per-merge journal in ../deleted/phase1_6_merges.jsonl
// captures the merged-in node + its incident edges (pre-merge) so the merge
// can be undone by recreating the dup node and replaying its relationships.
// =========================================================================

// Pattern (parameterised per pair by the Python runner)
// MATCH (canon:Akteur {id: $canonical_id}), (dup:Akteur {id: $merge_id})
// CALL apoc.refactor.mergeNodes([canon, dup], {properties:'combine', mergeRels:true})
//   YIELD node
// SET node.aliases = coalesce(node.aliases, []) + $merge_id
// RETURN node.id AS id, node.aliases AS aliases;
