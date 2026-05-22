// Resolve explicit membership overlaps.
// Rule:
// - keep GEHÖRT_ZU as the canonical explicit affiliation edge
// - upgrade evidence_confidence from overlapping VERBUNDEN_MIT_AKTEUR when stronger
// - delete the generic actor-to-actor edge

MATCH (a:Akteur)-[g:GEHÖRT_ZU]->(b:Akteur)
MATCH (a)-[v:VERBUNDEN_MIT_AKTEUR]->(b)
SET g.evidence_confidence = CASE
    WHEN coalesce(g.evidence_confidence, '') IN ['', 'unklar']
     AND coalesce(v.evidence_confidence, '') = 'teilweise_belegt'
    THEN 'teilweise_belegt'
    WHEN coalesce(g.evidence_confidence, '') = ''
    THEN v.evidence_confidence
    ELSE g.evidence_confidence
END
DELETE v;