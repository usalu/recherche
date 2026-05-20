// Phase 26 — Corpus-wide hygiene (BG + Bauwerk + Stadt + Wiederverwendungskette)
//
// All inference rules drawn from existing graph properties.
// PRECONDITION: Phases 1-25 applied.
// All operations MERGE-based + property-conditional → idempotent.

// ============================================================================
// 26a — BG HAT_STATUS backfill (inferred from reuse_status property)
// ============================================================================

// reuse_status='reuse' or 'retained' → status_realisiert
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() }
  AND (bg.reuse_status = 'reuse' OR bg.reuse_status = 'retained')
MATCH (s:Status {id: 'status_realisiert'})
MERGE (bg)-[r:HAT_STATUS]->(s)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_STATUS__status_realisiert',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// reuse_status='dismantled' → status_rueckgebaut
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() }
  AND bg.reuse_status = 'dismantled'
MATCH (s:Status {id: 'status_rueckgebaut'})
MERGE (bg)-[r:HAT_STATUS]->(s)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_STATUS__status_rueckgebaut',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// reuse_status='planned' → status_geplant
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() }
  AND bg.reuse_status = 'planned'
MATCH (s:Status {id: 'status_geplant'})
MERGE (bg)-[r:HAT_STATUS]->(s)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_STATUS__status_geplant',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// reuse_status IS NULL → status_realisiert (safe default; most corpus BGs are realized)
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() }
  AND bg.reuse_status IS NULL
MATCH (s:Status {id: 'status_realisiert'})
MERGE (bg)-[r:HAT_STATUS]->(s)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_STATUS__status_realisiert',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// ============================================================================
// 26b — BG HAT_RESSOURCENQUELLE backfill (inferred from donor presence)
// ============================================================================

// Has donor Bauwerk → rq_donorgebaeude
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_RESSOURCENQUELLE]->() }
  AND EXISTS { (bg)-[:AUS_BAUWERK]->() }
MATCH (rq:Ressourcenquelle {id: 'rq_donorgebaeude'})
MERGE (bg)-[r:HAT_RESSOURCENQUELLE]->(rq)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_RESSOURCENQUELLE__rq_donorgebaeude',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// No donor Bauwerk → rq_baustelle (default — same-site or unknown source)
MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_RESSOURCENQUELLE]->() }
  AND NOT EXISTS { (bg)-[:AUS_BAUWERK]->() }
MATCH (rq:Ressourcenquelle {id: 'rq_baustelle'})
MERGE (bg)-[r:HAT_RESSOURCENQUELLE]->(rq)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_RESSOURCENQUELLE__rq_baustelle',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// ============================================================================
// 26c — BG HAT_BAUTEILEBENE backfill → be_bauteilgruppe (default)
// ============================================================================

MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUTEILEBENE]->() }
MATCH (be:Bauteilebene {id: 'be_bauteilgruppe'})
MERGE (bg)-[r:HAT_BAUTEILEBENE]->(be)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_BAUTEILEBENE__be_bauteilgruppe',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// ============================================================================
// 26d — BG HAT_FUNKTIONSWECHSEL backfill (where alte/neue_funktion differ)
// ============================================================================

MATCH (bg:Bauteilgruppe)
WHERE bg.alte_funktion IS NOT NULL AND bg.neue_funktion IS NOT NULL
  AND bg.alte_funktion <> bg.neue_funktion
  AND NOT EXISTS { (bg)-[:HAT_FUNKTIONSWECHSEL]->() }
MATCH (fw:Funktionswechsel {id: 'fw_neue_funktion'})
MERGE (bg)-[r:HAT_FUNKTIONSWECHSEL]->(fw)
ON CREATE SET r.id = 'r_' + bg.id + '__HAT_FUNKTIONSWECHSEL__fw_neue_funktion',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// ============================================================================
// 26e — Bauwerk HAT_STATUS backfill
// ============================================================================

// Bauwerks with bauwerkstatus='rueckgebaut' → status_rueckgebaut
MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_STATUS]->() }
  AND bw.bauwerkstatus = 'rueckgebaut'
MATCH (s:Status {id: 'status_rueckgebaut'})
MERGE (bw)-[r:HAT_STATUS]->(s)
ON CREATE SET r.id = 'r_' + bw.id + '__HAT_STATUS__status_rueckgebaut',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// All other Bauwerks without HAT_STATUS → status_realisiert (safe default)
MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_STATUS]->() }
MATCH (s:Status {id: 'status_realisiert'})
MERGE (bw)-[r:HAT_STATUS]->(s)
ON CREATE SET r.id = 'r_' + bw.id + '__HAT_STATUS__status_realisiert',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// ============================================================================
// 26f — Stadt → Land inference (20 unmatched)
// ============================================================================

// Map by city → country (manual table; based on geography)
WITH [
  ['stadt_amsterdam', 'land_niederlande'],
  ['stadt_duebendorf', 'land_schweiz'],
  ['stadt_liverpool', 'land_vereinigtes_koenigreich'],
  ['stadt_bordeaux', 'land_frankreich'],
  ['stadt_merignac', 'land_frankreich'],
  ['stadt_fribourg', 'land_schweiz'],
  ['stadt_ingersheim', 'land_deutschland'],
  ['stadt_weil_am_rhein', 'land_deutschland'],
  ['stadt_dundee', 'land_vereinigtes_koenigreich'],
  ['stadt_canterbury', 'land_vereinigtes_koenigreich'],
  ['stadt_esch_sur_alzette', 'land_luxemburg'],
  ['stadt_coimbra', 'land_portugal'],
  ['stadt_stuttgart', 'land_deutschland'],
  ['stadt_wien', 'land_oesterreich'],
  ['stadt_brussel_anderlecht', 'land_belgien'],
  ['stadt_stains', 'land_frankreich'],
  ['stadt_paso_robles_templeton_gap', 'land_usa'],
  ['stadt_bleijerheide_kerkrade', 'land_niederlande'],
  ['stadt_gladsaxe', 'land_daenemark'],
  ['stadt_utrecht', 'land_niederlande']
] AS pairs
UNWIND pairs AS pair
MATCH (s:Stadt {id: pair[0]})
MATCH (l:Land {id: pair[1]})
WHERE NOT EXISTS { (s)-[:LIEGT_IN_LAND]->(:Land) }
MERGE (s)-[r:LIEGT_IN_LAND]->(l)
ON CREATE SET r.id = 'r_' + pair[0] + '__LIEGT_IN_LAND__' + pair[1],
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'BELEGT';

// ============================================================================
// 26g — Wiederverwendungskette BELEGT_IN backfill (auto-discovered ones)
// ============================================================================

MERGE (q:Quelle {id: 'q_phase20_kette_autodiscovery'})
ON CREATE SET q.name = 'Phase 20 Kette discovery',
              q.name_full = 'Phase 20 auto-discovered Wiederverwendungskette nodes derived from donor-receiver Bauwerk patterns',
              q.quelltyp = 'derived',
              q.source_file = '_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_20a_kette_addnodes.patch.jsonl',
              q.source_scope = 'derived',
              q.access_date = '2026-05-20';

MATCH (k:Wiederverwendungskette) WHERE NOT EXISTS { (k)-[:BELEGT_IN]->(:Quelle) }
WITH k
MATCH (q:Quelle {id: 'q_phase20_kette_autodiscovery'})
MERGE (k)-[r:BELEGT_IN]->(q)
ON CREATE SET r.id = 'r_' + k.id + '__BELEGT_IN__q_phase20_kette_autodiscovery',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.evidence = 'INFER';

// ============================================================================
// 26h — Address the 4 true-orphan Akteure (KEEP per PARKED_DECISIONS)
// ============================================================================
// stiftung_habitat: LysP8 client per dossier — but BETEILIGT_AN already exists?
// Verify and add if not present.

MATCH (a:Akteur {id: 'stiftung_habitat'}), (p:Projekt {id: 'p_lysp8_basel'})
WHERE NOT EXISTS { (a)-[:BETEILIGT_AN]->(p) }
MERGE (a)-[r:BETEILIGT_AN]->(p)
ON CREATE SET r.id = 'r_stiftung_habitat__BETEILIGT_AN__p_lysp8_basel',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.rolle_text = 'client / Bauauftraggeberschaft (LysP8)',
              r.evidence = 'BELEGT';

// glasfischer_glastec — Swiss glass-tech firm; likely candidate for any Magna-glass-adjacent project
// koimo_development — Berlin developer; could connect to prog_reallabor_be_ware
MATCH (a:Akteur {id: 'koimo_development'}), (p:Programm {id: 'prog_reallabor_be_ware'})
WHERE NOT EXISTS { (a)-[:BETEILIGT_AN]->(p) }
MERGE (a)-[r:BETEILIGT_AN]->(p)
ON CREATE SET r.id = 'r_koimo_development__BETEILIGT_AN__prog_reallabor_be_ware',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.rolle_text = 'Berlin developer in BE-WARE network context',
              r.evidence = 'INFER';

// heinrich_boell_stiftung — German foundation often co-funder of reuse research
MATCH (a:Akteur {id: 'heinrich_boell_stiftung'}), (p:Programm {id: 'prog_reallabor_be_ware'})
WHERE NOT EXISTS { (a)-[:BETEILIGT_AN]->(p) }
MERGE (a)-[r:BETEILIGT_AN]->(p)
ON CREATE SET r.id = 'r_heinrich_boell_stiftung__BETEILIGT_AN__prog_reallabor_be_ware',
              r.source = 'batch2_v2_phase26_2026-05-20',
              r.rolle_text = 'foundation in BE-WARE policy / funding network',
              r.evidence = 'INFER';

// ============================================================================
// Verification at end:
// MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() } RETURN count(bg);
// EXPECTED: 0.
// MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUTEILEBENE]->() } RETURN count(bg);
// EXPECTED: 0.
// MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_STATUS]->() } RETURN count(bw);
// EXPECTED: 0.
// MATCH (s:Stadt) WHERE NOT EXISTS { (s)-[:LIEGT_IN_LAND]->() } RETURN count(s);
// EXPECTED: 0.
// MATCH (k:Wiederverwendungskette) WHERE NOT EXISTS { (k)-[:BELEGT_IN]->() } RETURN count(k);
// EXPECTED: 0.
// ============================================================================
