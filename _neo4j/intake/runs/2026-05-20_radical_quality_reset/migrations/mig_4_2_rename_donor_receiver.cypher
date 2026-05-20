// =====================================================================
// mig_4_2 — Phase 4.2: rename donor/receiver relationship types
//
//   AUS_BAUWERK   → FROM_DONOR
//   EINGEBAUT_IN  → INTO_RECEIVER
//
// Uses apoc.refactor.rename.type which preserves identity, properties,
// and start/end nodes — this is a TYPE rename, not an alias.
//
// APOC presence verified at runtime by the runner (procedure
// 'apoc.refactor.rename.type' enumerated in agent7_explore.json).
//
// Idempotency: rename is a no-op when the old type is absent.
// =====================================================================

// 4_2.a — AUS_BAUWERK → FROM_DONOR (286 edges at run time)
MATCH ()-[r:AUS_BAUWERK]->()
WITH collect(r) AS rels
CALL apoc.refactor.rename.type('AUS_BAUWERK', 'FROM_DONOR', rels)
YIELD batches, total, timeTaken, committedOperations, failedOperations,
      failedBatches, retries, errorMessages
RETURN 'AUS_BAUWERK→FROM_DONOR' AS step,
       batches, total, committedOperations, failedOperations,
       failedBatches, retries, timeTaken, errorMessages;

// 4_2.b — EINGEBAUT_IN → INTO_RECEIVER (349 edges at run time)
MATCH ()-[r:EINGEBAUT_IN]->()
WITH collect(r) AS rels
CALL apoc.refactor.rename.type('EINGEBAUT_IN', 'INTO_RECEIVER', rels)
YIELD batches, total, timeTaken, committedOperations, failedOperations,
      failedBatches, retries, errorMessages
RETURN 'EINGEBAUT_IN→INTO_RECEIVER' AS step,
       batches, total, committedOperations, failedOperations,
       failedBatches, retries, timeTaken, errorMessages;

// 4_2.c — Post-rename audits — must satisfy:
//          AUS_BAUWERK   = 0
//          EINGEBAUT_IN  = 0
//          FROM_DONOR    = 286 (pre-rename AUS_BAUWERK count)
//          INTO_RECEIVER = 349 (pre-rename EINGEBAUT_IN count)
MATCH ()-[r:AUS_BAUWERK]->()
RETURN 'AUS_BAUWERK_remaining' AS check, count(r) AS c;

MATCH ()-[r:EINGEBAUT_IN]->()
RETURN 'EINGEBAUT_IN_remaining' AS check, count(r) AS c;

MATCH ()-[r:FROM_DONOR]->()
RETURN 'FROM_DONOR_count' AS check, count(r) AS c;

MATCH ()-[r:INTO_RECEIVER]->()
RETURN 'INTO_RECEIVER_count' AS check, count(r) AS c;
