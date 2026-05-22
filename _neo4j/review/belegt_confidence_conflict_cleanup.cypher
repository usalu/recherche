// 2026-05-28
// Downgrade misleading "belegt" confidence where source binding is not exact
// and the relationship already requires source URL / exact-claim review.
//
// This preserves the original confidence in previous_evidence_confidence.

MATCH ()-[r]->()
WHERE r.evidence_confidence = "belegt"
  AND coalesce(r.source_role, "") = ""
  AND (
    coalesce(r.source_resolution_status, "") CONTAINS "review"
    OR coalesce(r.review_status, "") CONTAINS "review"
  )
  AND coalesce(r.source_status, "") <> "exact"
SET r.previous_evidence_confidence = coalesce(r.previous_evidence_confidence, r.evidence_confidence),
    r.evidence_confidence = "unklar",
    r.evidence_confidence_status = "downgraded_pending_exact_source_url_review",
    r.evidence_quality = coalesce(r.evidence_quality, "source_binding_not_exact"),
    r.evidence_note = coalesce(
      r.evidence_note,
      "Former evidence_confidence=belegt was downgraded because source_status is not exact and the relationship still needs source URL / exact-claim review."
    ),
    r.evidence_cleanup_run = "2026-05-28_belegt_confidence_conflict_cleanup"
RETURN count(r) AS updated_relationships;

