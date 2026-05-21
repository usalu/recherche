// =========================================================================
// Repair migration — Phase 1.5 / 1.6 residuals
// Database: mit-bestand
//
// Fixes final verifier 3 blocking residuals:
//   - norm_din_18940 remained as a live :Norm
//   - bauburo_in_situ remained as a live :Akteur
//   - Bellastock remained as a live :Akteur
//
// Policy:
//   - actor residuals have useful live connections and are merged into the
//     Phase 1.6 canonical nodes with relationships preserved.
//   - norm_din_18940 now has one useful ReuseRule connection, so the old
//     target id is retired by merging into a replacement family node rather
//     than detach-deleting the connected node.
// =========================================================================

// --- 1.6 residual actor: baubuero_in_situ <- bauburo_in_situ
MATCH (canon:Akteur {id: 'baubuero_in_situ'}), (dup:Akteur {id: 'bauburo_in_situ'})
WITH canon, dup,
     apoc.coll.toSet([x IN coalesce(canon.aliases, []) + coalesce(dup.aliases, []) + [dup.id, dup.name] WHERE x IS NOT NULL]) AS aliases
CALL apoc.refactor.mergeNodes([canon, dup], {properties: 'combine', mergeRels: true})
  YIELD node
SET node.id = 'baubuero_in_situ',
    node.name = 'baubüro in situ',
    node.aliases = apoc.coll.toSet(aliases + coalesce(node.aliases, [])),
    node.repair_phase = '1.5_1.6_residuals',
    node.repaired_at = datetime()
RETURN node.id AS repaired_actor, node.aliases AS aliases;

// --- 1.6 residual actor: bellastock <- Bellastock
MATCH (canon:Akteur {id: 'bellastock'}), (dup:Akteur {id: 'Bellastock'})
WITH canon, dup,
     apoc.coll.toSet([x IN coalesce(canon.aliases, []) + coalesce(dup.aliases, []) + [dup.id, dup.name] WHERE x IS NOT NULL]) AS aliases
CALL apoc.refactor.mergeNodes([canon, dup], {properties: 'combine', mergeRels: true})
  YIELD node
SET node.id = 'bellastock',
    node.name = 'Bellastock',
    node.aliases = apoc.coll.toSet(aliases + coalesce(node.aliases, [])),
    node.repair_phase = '1.5_1.6_residuals',
    node.repaired_at = datetime()
RETURN node.id AS repaired_actor, node.aliases AS aliases;

// --- 1.5 residual norm: remap old deletion target to retained family node
MATCH (old:Norm {id: 'norm_din_18940'})
MERGE (canon:Norm {id: 'norm_din_18940_family'})
ON CREATE SET
  canon.name = 'DIN 18940 family',
  canon.name_full = 'DIN 18940/18945/18946/18947 family',
  canon.source_scope = 'repair_phase_1_5_1_6',
  canon.evidence_origin = 'repair_remap',
  canon.evidence_basis = 'reuse_rule_key_norm_family',
  canon.evidence_confidence = 'belegt'
WITH canon, old,
     apoc.coll.toSet([x IN coalesce(canon.aliases, []) + coalesce(old.aliases, []) + [old.id, old.name, old.name_full] WHERE x IS NOT NULL]) AS aliases
CALL apoc.refactor.mergeNodes([canon, old], {properties: 'combine', mergeRels: true})
  YIELD node
SET node.id = 'norm_din_18940_family',
    node.name = 'DIN 18940 family',
    node.name_full = 'DIN 18940/18945/18946/18947 family',
    node.aliases = apoc.coll.toSet(aliases + coalesce(node.aliases, [])),
    node.repair_phase = '1.5_1.6_residuals',
    node.repaired_at = datetime()
RETURN node.id AS repaired_norm, node.aliases AS aliases;
