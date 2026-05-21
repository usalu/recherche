// ==========================================================================
// stage_4_audit_queries.cypher
// Read-only audit queries for the post-remediation Q1–Q7 + cross-agent
// invariants. The runner runs each block, captures results, writes
// FINAL_REVIEW_PLAN_AUDIT.md.
//
// This file MUST NOT contain any write statements. Default access mode
// must be READ in the runner.
// ==========================================================================

// ==========================================================================
// SECTION A — Headline counts
// ==========================================================================

// A.1 — total nodes / rels
MATCH (n) RETURN 'total_nodes' AS metric, count(n) AS c;
MATCH ()-[r]->() RETURN 'total_rels' AS metric, count(r) AS c;

// A.2 — per-label node counts (descending)
MATCH (n) UNWIND labels(n) AS lbl
RETURN lbl, count(*) AS c ORDER BY c DESC;

// A.3 — per-rel-type counts (descending)
MATCH ()-[r]->()
RETURN type(r) AS rel_type, count(r) AS c ORDER BY c DESC;

// ==========================================================================
// SECTION B — Honest Q1–Q7
// ==========================================================================

// Q1 — Reuse Story (source_curated only — no Repair D promotions)
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
WHERE hbg.evidence_origin = 'source_curated'
RETURN 'Q1_source_curated_only' AS query, count(*) AS row_count;

// Q1 — Reuse Story (topology_synthesized) — what Repair D actually produced
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
WHERE hbg.evidence_origin = 'topology_synthesized'
RETURN 'Q1_topology_synthesized' AS query, count(*) AS row_count;

// Q1 — Reuse Story (combined: source_curated + topology_synthesized)
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe)-[:INTO_RECEIVER]->(receiver),
      (p:Projekt)-[hbg:HAT_BAUTEILGRUPPE]->(bg)
WHERE hbg.evidence_origin IN ['source_curated', 'topology_synthesized']
RETURN 'Q1_combined' AS query, count(*) AS row_count;

// Q1 — Filter by bg_kind='batch' (R5 disambiguation)
MATCH (donor)<-[:FROM_DONOR]-(bg:Bauteilgruppe {bg_kind:'batch'})-[:INTO_RECEIVER]->(receiver)
RETURN 'Q1_bg_kind_batch' AS query, count(DISTINCT bg) AS distinct_bg;

// Q2 — Risk Story (documented only)
MATCH (bg)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
WHERE r.evidence_basis = 'documented'
RETURN 'Q2_documented' AS query, count(*) AS row_count;

// Q2 — Risk Story (era_and_material inference)
MATCH (bg)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
WHERE r.evidence_basis = 'era_and_material'
RETURN 'Q2_era_and_material' AS query, count(*) AS row_count;

// Q2 — Risk Story (material_only inference)
MATCH (bg)-[r:HAS_RISK_POLLUTANT]->(s:Schadstoff)
WHERE r.evidence_basis = 'material_only'
RETURN 'Q2_material_only' AS query, count(*) AS row_count;

// Q2 — all REQUIRES_VERIFICATION_FOR
MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->()
RETURN 'Q2_requires_verification' AS query, count(*) AS row_count;

// Q3 — Comparison (graph-native via :Kennwert from R4)
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'})
RETURN p.id AS projekt, kw.kennwert, kw.wert, kw.wert_text, kw.einheit, kw.bilanzgrenze
ORDER BY p.id;

// Q3 — Count tier-1 projects with reuse_share Kennwert
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[:HAT_KENNWERT]->(kw:Kennwert {category:'reuse_share'})
RETURN 'Q3_tier1_with_reuse_share' AS query, count(DISTINCT p) AS c;

// Q4 — Actor Network (verified BETEILIGT_AN only; no STUB_PROJECT_LINK)
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
WITH a, count(DISTINCT p) AS c WHERE c >= 2
RETURN a.id AS actor_id, a.name AS actor_name, c AS tier1_project_count
ORDER BY c DESC;

// Q4 — Count
MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
WITH a, count(DISTINCT p) AS c WHERE c >= 2
RETURN 'Q4_count' AS query, count(a) AS c;

// Q4 — Including STUB_PROJECT_LINK (the dishonest version, for comparison)
MATCH (a:Akteur)-[:BETEILIGT_AN|STUB_PROJECT_LINK]->(p:Projekt {quality_tier:'tier_1_decision_grade'})
WITH a, count(DISTINCT p) AS c WHERE c >= 2
RETURN 'Q4_with_stubs' AS query, count(a) AS c;

// Q5 — Decision Support (graph-native :RELEVANT_FOR from R3)
MATCH ()-[r:RELEVANT_FOR]->()
RETURN 'Q5_relevant_for_total' AS query, count(r) AS c;

// Q5 — Per-rule coverage
MATCH (rule:ReuseRule)
OPTIONAL MATCH (rule)-[r:RELEVANT_FOR]->(:Projekt)
RETURN rule.id AS rule_id, rule.country_iso AS country, rule.material AS material,
       count(r) AS projekt_count
ORDER BY projekt_count DESC, rule.id;

// Q5 — France exposure (Ferme du Rail must be uncovered)
MATCH (p:Projekt {id:'p_ferme_du_rail_paris'})
OPTIONAL MATCH (:ReuseRule)-[r:RELEVANT_FOR]->(p)
RETURN 'Q5_ferme_du_rail_rules' AS query, count(r) AS c;

// Q5 — UK exposure (Holbein Gardens must be covered)
MATCH (p:Projekt {id:'p_holbein_gardens_london'})
OPTIONAL MATCH (rule:ReuseRule)-[r:RELEVANT_FOR]->(p)
RETURN 'Q5_holbein_rules' AS query, count(r) AS c;

// Q6 — Trust check, 5-bucket distribution
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
RETURN r.evidence_origin AS origin, count(*) AS c ORDER BY c DESC;

// Q6 — Per-Projekt (aggregate over 101 :Projekt)
MATCH (p:Projekt)-[r]-()
WHERE r.evidence_origin IS NOT NULL
RETURN r.evidence_origin AS origin, count(*) AS c ORDER BY c DESC;

// Q6 — Tier-1 only (the decision cohort)
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})-[r]-()
WHERE r.evidence_origin IS NOT NULL
RETURN r.evidence_origin AS origin, count(*) AS c ORDER BY c DESC;

// Q6 — Bookkeeping segregation
MATCH ()-[r {is_bookkeeping:true}]->()
RETURN 'Q6_bookkeeping_count' AS query, count(r) AS c;

// Q7 — Source drill-down (case_markdown → external)
MATCH (qmd:Quelle {quelltyp:'case_markdown'})-[:ZITIERT_QUELLE]->(ext:Quelle)
RETURN 'Q7_case_md_external' AS query, count(*) AS c;

// Q7 — case_markdown with text_content available (from R7.d)
MATCH (qmd:Quelle {quelltyp:'case_markdown'})
WHERE qmd.text_content IS NOT NULL
RETURN 'Q7_case_md_with_text_content' AS query, count(qmd) AS c;

// ==========================================================================
// SECTION C — Cross-agent invariants
// ==========================================================================

// C.1 — every evidence_origin in new enum
MATCH ()-[r]->()
WHERE r.evidence_origin IS NOT NULL
  AND NOT r.evidence_origin IN ['source_curated','topology_synthesized','registry_derived','inferred','external_unfolded']
RETURN 'C1_origin_enum_violation' AS rule, count(r) AS violations;

// C.2 — no edge retains old 'curated' value
MATCH ()-[r]->()
WHERE r.evidence_origin = 'curated'
RETURN 'C2_old_curated_remaining' AS rule, count(r) AS violations;

// C.3 — no edge retains 'bookkeeping' in confidence enum
MATCH ()-[r]->()
WHERE r.evidence_confidence = 'bookkeeping'
RETURN 'C3_bookkeeping_in_confidence' AS rule, count(r) AS violations;

// C.4 — every source_curated has a non-null excerpt
MATCH ()-[r]->()
WHERE r.evidence_origin = 'source_curated'
  AND (r.evidence_excerpt IS NULL OR r.evidence_excerpt = '')
RETURN 'C4_source_curated_no_excerpt' AS rule, count(r) AS violations;

// C.5 — every :Bauteilgruppe has bg_kind
MATCH (bg:Bauteilgruppe) WHERE bg.bg_kind IS NULL
RETURN 'C5_bg_without_kind' AS rule, count(bg) AS violations;

// C.6 — no :Bauteilgruppe tagged 'category' has a donor/receiver edge
MATCH (bg:Bauteilgruppe {bg_kind:'category'})
WHERE exists{(bg)-[:FROM_DONOR]->()} OR exists{(bg)-[:INTO_RECEIVER]->()}
RETURN 'C6_category_with_topology' AS rule, count(bg) AS violations;

// C.7 — every :Projekt with HAT_BAUTEILGRUPPE→BG→Bauwerk has :HAS_BAUWERK
MATCH (p:Projekt)
WHERE exists{(p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:FROM_DONOR|INTO_RECEIVER]->(:Bauwerk)}
  AND NOT exists{(p)-[:HAS_BAUWERK]->()}
RETURN 'C7_missing_has_bauwerk' AS rule, count(p) AS violations;

// C.8 — :ASSOZIIERT_MIT_PROJEKT renamed to :STUB_PROJECT_LINK
MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
RETURN 'C8_old_rel_type_remaining' AS rule, count(r) AS violations;

// C.9 — every Kennwert has at least one HAT_KENNWERT incoming
MATCH (kw:Kennwert) WHERE NOT exists{()-[:HAT_KENNWERT]->(kw)}
RETURN 'C9_kennwert_orphan' AS rule, count(kw) AS violations;

// C.10 — every :Quelle case_markdown has text_content (R7.d)
MATCH (q:Quelle {quelltyp:'case_markdown'})
WHERE q.text_content IS NULL
RETURN 'C10_case_md_without_text' AS rule, count(q) AS c;

// C.11 — restored labels are populated
MATCH (n:Layer) RETURN 'C11_layer_count' AS check, count(n) AS c;
MATCH (n:LCAModule) RETURN 'C11_lca_module_count' AS check, count(n) AS c;
MATCH (n:RechtlicheBedingung) RETURN 'C11_rb_count' AS check, count(n) AS c;
MATCH (n:Zertifizierungssystem) RETURN 'C11_cert_count' AS check, count(n) AS c;
MATCH (n:Tool) WHERE 'Software' IN labels(n) RETURN 'C11_tool_secondary_count' AS check, count(n) AS c;
MATCH (n:DeprecatedType) RETURN 'C11_deprecated_type_count' AS check, count(n) AS c;
MATCH (n:DataIssue) RETURN 'C11_data_issue_count' AS check, count(n) AS c;

// ==========================================================================
// SECTION D — Decision-grade cohort recomputation
// ==========================================================================

// D.1 — tier-1 count under the OLD gate (source_curated OR topology_synthesized)
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
RETURN 'D1_tier1_legacy' AS query, count(p) AS c;

// D.2 — tier-1 count under the NEW honest gate (source_curated only)
// A project is honestly tier-1 if it has ≥ 3 source_curated BELEGT_IN edges
// AND the other tier criteria still hold.
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
OPTIONAL MATCH (p)-[bel:BELEGT_IN]->()
WITH p, sum(CASE WHEN bel.evidence_origin = 'source_curated'
                   AND bel.evidence_excerpt IS NOT NULL
                   AND bel.evidence_confidence IN ['belegt','teilweise_belegt']
                 THEN 1 ELSE 0 END) AS source_curated_evidence_count
WHERE source_curated_evidence_count >= 3
RETURN 'D2_tier1_honest_count' AS query, count(p) AS c;

// D.3 — projects that would drop tier under honest gate
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
OPTIONAL MATCH (p)-[bel:BELEGT_IN]->()
WITH p, sum(CASE WHEN bel.evidence_origin = 'source_curated'
                   AND bel.evidence_excerpt IS NOT NULL
                   AND bel.evidence_confidence IN ['belegt','teilweise_belegt']
                 THEN 1 ELSE 0 END) AS sc_count
WHERE sc_count < 3
RETURN p.id AS projekt_id, sc_count AS source_curated_evidence;

// ==========================================================================
// SECTION E — :DataIssue summary
// ==========================================================================

MATCH (i:DataIssue) RETURN 'E1_data_issue_total' AS query, count(i) AS c;
MATCH (i:DataIssue) RETURN i.kind AS kind, count(i) AS c ORDER BY c DESC;
MATCH (i:DataIssue) RETURN i.severity AS severity, count(i) AS c ORDER BY i.severity;
MATCH (i:DataIssue)-[:CONCERNS]->(p:Projekt)
RETURN p.id AS projekt, count(i) AS issue_count
ORDER BY issue_count DESC LIMIT 10;
