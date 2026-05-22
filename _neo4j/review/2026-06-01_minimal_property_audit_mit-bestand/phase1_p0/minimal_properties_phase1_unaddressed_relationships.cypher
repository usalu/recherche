// Phase 1 P0 relationship-property cleanup for rels without r.id.
// Generated for review only; apply after backup if accepted.
// Generated UTC: 2026-06-01T00:04:02.420573+00:00

// 7 relationships: HAT_AKTEURROLLE.scope
MATCH ()-[r:`HAT_AKTEURROLLE`]->()
WHERE r.`scope` IS NOT NULL
REMOVE r.`scope`;

// 2 relationships: HAT_AKTEURTYP.scope
MATCH ()-[r:`HAT_AKTEURTYP`]->()
WHERE r.`scope` IS NOT NULL
REMOVE r.`scope`;

// 88 relationships: HAT_KENNWERT.candidate_source_count
MATCH ()-[r:`HAT_KENNWERT`]->()
WHERE r.`candidate_source_count` IS NOT NULL
REMOVE r.`candidate_source_count`;
