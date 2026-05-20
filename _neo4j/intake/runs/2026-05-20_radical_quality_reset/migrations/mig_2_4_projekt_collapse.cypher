// =========================================================================
// Migration 2.4 — :Projekt property collapse
//   - year fields  → year_completed + raw_year_fields (JSON string)
//   - area fields  → area_m2_gross / area_m2_range_min/max / area_sqft_min/max
//   - cost fields  → cost_facts (list of JSON strings)
//   - co2 fields   → co2_facts (list of JSON strings)
//   - reuse fields → reuse_share_facts (list of JSON strings)
//   - one-off counters → matching :Bauteilgruppe.menge_stueck per name pattern
//
// Original sparse keys are REMOVED from :Projekt after they have been
// preserved into raw_year_fields / *_facts. Phase 2.7 then archives any
// remaining non-panel keys into ._archive.
//
// Reversibility: snapshot/nodes.jsonl (taken Wave-1 start) carries the
// pre-migration property tuple for every :Projekt; replay restores 1:1.
// =========================================================================

// --- 2.4.a Year coalesce + raw_year_fields
// (executed per-node by agent6_runner.py with bound parameters;
//  this canonical form documents the contract)
//
// PRIORITY: jahr_fertigstellung > fertigstellung_jahr > jahr_eroeffnung
//           > jahr > baujahr
//
// MATCH (p:Projekt)
// WITH p,
//   [k IN $YEAR_KEYS WHERE p[k] IS NOT NULL] AS present_year_keys,
//   coalesce(p.jahr_fertigstellung, p.fertigstellung_jahr,
//            p.jahr_eroeffnung, p.jahr, p.baujahr) AS year_completed
// WITH p, present_year_keys, year_completed,
//   apoc.convert.toJson(apoc.map.fromPairs([k IN present_year_keys | [k, p[k]]])) AS raw_json
// SET p.year_completed   = year_completed,
//     p.raw_year_fields  = raw_json
// WITH p, present_year_keys
// CALL apoc.create.removeProperties(p, present_year_keys) YIELD node
// RETURN count(node);

// --- 2.4.b Area coalesce
//
// MATCH (p:Projekt)
// WITH p,
//   coalesce(p.flaeche_m2, p.bgf_m2, p.nutzflaeche_m2) AS area_gross,
//   p.flaeche_m2_min  AS area_min,
//   p.flaeche_m2_max  AS area_max,
//   p.flaeche_sqft_min AS sqft_min,
//   p.flaeche_sqft_max AS sqft_max
// WITH p, area_gross, area_min, area_max, sqft_min, sqft_max,
//   [k IN $AREA_KEYS WHERE p[k] IS NOT NULL] AS present_area_keys
// SET p.area_m2_gross      = area_gross,
//     p.area_m2_range_min  = area_min,
//     p.area_m2_range_max  = area_max,
//     p.area_sqft_min      = sqft_min,
//     p.area_sqft_max      = sqft_max
// WITH p, present_area_keys
// CALL apoc.create.removeProperties(p, present_area_keys) YIELD node
// RETURN count(node);

// --- 2.4.c Cost / CO2 / Reuse fact-lists (list of JSON strings)
//
// Pattern (per node, per fact group):
//
// WITH p,
//   [k IN $COST_KEYS WHERE p[k] IS NOT NULL] AS present_cost_keys
// WITH p, present_cost_keys,
//   [k IN present_cost_keys |
//     apoc.convert.toJson({
//       basis: k,
//       value: p[k],
//       unit: CASE k
//         WHEN 'baukosten_eur' THEN 'EUR'
//         WHEN 'kosten_eur'    THEN 'EUR'
//         WHEN 'kostenreduktion_prozent' THEN '%'
//         ELSE null END,
//       source_id: null
//     })
//   ] AS facts
// SET p.cost_facts = facts
// WITH p, present_cost_keys
// CALL apoc.create.removeProperties(p, present_cost_keys) YIELD node
// RETURN count(node);
//
// (analogous for co2_facts ($CO2_KEYS) and reuse_share_facts ($REUSE_KEYS))

// --- 2.4.d Counters → :Bauteilgruppe.menge_stueck
//
// Pattern per (counter_key, bg_name_substring):
//
// MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
// WHERE p[$counter_key] IS NOT NULL
//   AND toLower(coalesce(bg.name,'')) CONTAINS $bg_substring
// WITH p, bg, p[$counter_key] AS cnt
// SET bg.menge_stueck = coalesce(bg.menge_stueck, cnt),
//     bg.menge_source = coalesce(bg.menge_source, 'projekt_counter_migration_mig_2_4'),
//     bg.menge_original_key = coalesce(bg.menge_original_key, $counter_key)
// RETURN p.id, bg.id, cnt;
//
// After all known mappings applied, the counter properties that were
// successfully migrated are removed from :Projekt by the Python runner
// (idempotent: counters that did NOT name-match a BG are left in place
// and will be archived by Phase 2.7 into ._archive).

// --- 2.4.e Sanity checks (read-only)
// MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL RETURN count(p);
// MATCH (p:Projekt) WHERE p.area_m2_gross IS NOT NULL RETURN count(p);
// MATCH (p:Projekt) WHERE size(coalesce(p.cost_facts,[])) > 0 RETURN count(p);
// MATCH (p:Projekt) WHERE size(coalesce(p.co2_facts,[])) > 0 RETURN count(p);
// MATCH (p:Projekt) WHERE size(coalesce(p.reuse_share_facts,[])) > 0 RETURN count(p);
// MATCH (bg:Bauteilgruppe) WHERE bg.menge_source = 'projekt_counter_migration_mig_2_4' RETURN count(bg);
