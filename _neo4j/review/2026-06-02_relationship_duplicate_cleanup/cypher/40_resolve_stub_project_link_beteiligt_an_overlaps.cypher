// Conflict-aware resolution of STUB_PROJECT_LINK vs BETEILIGT_AN overlaps.
// Rule:
// - keep STUB_PROJECT_LINK when the stub explicitly marks the participation as unconfirmed
//   or carries association-only basis metadata
// - keep BETEILIGT_AN only for clean overlaps where the stub carries neither signal

MATCH (a:Akteur)-[s:STUB_PROJECT_LINK]->(x)
MATCH (a)-[b:BETEILIGT_AN]->(x)
WHERE coalesce(s.not_confirmed_project_participation, false) = true
   OR s.association_basis IS NOT NULL
DELETE b;

MATCH (a:Akteur)-[s:STUB_PROJECT_LINK]->(x)
MATCH (a)-[b:BETEILIGT_AN]->(x)
WHERE coalesce(s.not_confirmed_project_participation, false) = false
  AND s.association_basis IS NULL
SET b.evidence_confidence = CASE
    WHEN coalesce(b.evidence_confidence, '') IN ['', 'unklar']
     AND coalesce(s.evidence_confidence, '') = 'teilweise_belegt'
    THEN 'teilweise_belegt'
    WHEN coalesce(b.evidence_confidence, '') = ''
    THEN s.evidence_confidence
    ELSE b.evidence_confidence
END
DELETE s;