// ==========================================================================
// mig_r9_stub_project_link_rename
// Rename registry-stub project links to make their status explicit.
// Uses APOC refactor; run only after R3 is integrated.
// ==========================================================================

MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
WITH collect(r) AS rels
CALL apoc.refactor.rename.type('ASSOZIIERT_MIT_PROJEKT', 'STUB_PROJECT_LINK', rels)
YIELD batches, total, timeTaken, committedOperations, failedOperations,
      failedBatches, retries, errorMessages
RETURN batches, total, timeTaken, committedOperations, failedOperations,
       failedBatches, retries, errorMessages;

// Audits
MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
RETURN 'old_type_remaining' AS check, count(r) AS violations;

MATCH ()-[r:STUB_PROJECT_LINK]->()
RETURN 'new_type_count' AS check, count(r) AS c;

MATCH ()-[r:STUB_PROJECT_LINK]->()
WHERE r.needs_verification IS NULL OR r.needs_verification = false
RETURN 'stub_without_needs_verification' AS check, count(r) AS violations;
