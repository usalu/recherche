// =========================================================================
// Migration 4c.3 — Detach the wrong (Projekt)-[:BELEGT_IN]->(:Quelle)
// edges where the Quelle is a verbatim actor-registry URL.
//
// Rationale (plan §4c.3):
//   Actor-registry URLs are evidence for :Akteur identity / liaison, not
//   for project facts. Folding them onto :Projekt via BELEGT_IN creates
//   ~176 spurious "this project is documented by my own Wikipedia page"
//   edges (Résilience La Ferme des Possibles is the canonical example
//   with 4 such edges all pointing at actor pages).
//
// Contract preserved:
//   - The target :Quelle nodes (quelltyp='external_link_from_actor_registry')
//     remain untouched (319 nodes).
//   - The (Akteur)-[:BELEGT_IN]->(actor_registry Quelle) edges remain
//     untouched (360 edges before/after).
//   - Only the Projekt->Quelle edges are deleted.
//
// Status @ Agent 8 (2026-05-20): 176 edges deleted in a single transaction.
//   Pre-delete forensic snapshot: deleted/phase4c_3_projekt_actor_registry_belegt.jsonl
//   (one JSON line per deleted edge with projekt_id, quelle_id, quelle_url
//   and the full rel_props dict for full reversibility.)
//
// Idempotency: live count after deletion is 0; re-running is a no-op.
// =========================================================================

// --- (Optional) forensic dump BEFORE the delete --------------------------
// MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
// WHERE q.quelltyp = 'external_link_from_actor_registry'
// RETURN p.id AS projekt_id, q.id AS quelle_id, q.url AS quelle_url,
//        properties(r) AS rel_props;

// --- Pre-delete count (must match Agent-8 journal length: 176) ----------
MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
WHERE q.quelltyp = 'external_link_from_actor_registry'
RETURN count(r) AS projekt_belegt_actor_registry_before;

// --- DELETE ---------------------------------------------------------------
MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
WHERE q.quelltyp = 'external_link_from_actor_registry'
DELETE r;

// --- Post-delete acceptance ---------------------------------------------
// (1) Projekt edges must be 0.
MATCH (p:Projekt)-[r:BELEGT_IN]->(q:Quelle)
WHERE q.quelltyp = 'external_link_from_actor_registry'
RETURN count(r) AS must_be_zero;

// (2) Akteur edges must be unchanged (360 in Agent-8 run).
MATCH (a:Akteur)-[r:BELEGT_IN]->(q:Quelle)
WHERE q.quelltyp = 'external_link_from_actor_registry'
RETURN count(r) AS akteur_belegt_actor_registry_after;

// (3) Target :Quelle nodes themselves remain (319 in Agent-8 run).
MATCH (q:Quelle) WHERE q.quelltyp = 'external_link_from_actor_registry'
RETURN count(q) AS actor_registry_quelle_after;
