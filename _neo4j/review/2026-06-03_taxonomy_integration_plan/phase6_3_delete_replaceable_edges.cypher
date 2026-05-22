// =====================================================================
// Phase 6.3 — Delete replaceable upstream edges
//
// Every (:Bauteilgruppe|:Projekt)-[HAT_METHODE|HAT_AUFBEREITUNG|
//   HAT_RESSOURCENQUELLE|HAT_RUECKBAUVERFAHREN|HAT_WIEDERVERWENDUNGSART]->
//   (old vocab) edge is being deleted because the batches re-supply
// these connections (Phase 5 has already MERGEd the evidence-backed
// replacements on the SAME source nodes pointing to the NEW canonical).
//
// Per CONNECTION_TYPE_AUDIT.md totals:
//   HAT_METHODE       Bauteilgruppe→ 397 + Projekt→ 194 = 591
//   HAT_AUFBEREITUNG  411 + 22  = 433
//   HAT_RESSOURCENQUELLE 482 + 69 = 551
//   HAT_WIEDERVERWENDUNGSART 425 + 179 = 604
//   HAT_RUECKBAUVERFAHREN 299 + 0   = 299
//   ──────────────────────────
//   TOTAL ≈ 2,478 edges
//
// Notice we delete by checking the TARGET node has an OLD id (i.e. not
// one of the 6 new canonical ids). This ensures we don't accidentally
// drop a Phase-5 evidence edge that points at the new canonical.
//
// Run AFTER Phase 6.1 + 6.2 have reattached non-replaceable upstreams.
// =====================================================================

// New canonical id lists — anything NOT in these is "old vocab"
:param new_meth_ids => ['meth_urban_mining_und_scouting','meth_bestands_und_reuse_assessment',
                         'meth_verfuegbarkeitsbasiertes_design','meth_reversibles_design',
                         'meth_zirkulaere_beschaffung','meth_dokumentation_und_monitoring'];
:param new_aufb_ids => ['av_reinigung_und_oberflaeche','av_zuschnitt_und_vereinzelung',
                         'av_pruefung_sortierung_qs','av_reparatur_und_refurbishment',
                         'av_remanufacturing_und_upcycling','av_verstaerkung_und_schutz'];
:param new_rq_ids   => ['rq_externer_spenderbau','rq_eigener_bestand','rq_gleicher_standort',
                         'rq_bauteilmarkt_oder_lager','rq_leihgabe_oder_service',
                         'rq_restposten_abfall_unbekannt'];
:param new_rv_ids   => ['rv_selektiver_rueckbau','rv_ausbau_von_bauteilen','rv_demontage',
                         'rv_zerstoerungsarme_bergung','rv_schneidender_rueckbau',
                         'rv_integrierter_rueckbau_und_lagerung'];


// ---------- §1. HAT_METHODE ----------

MATCH (src)-[r:HAT_METHODE]->(meth_old:Methode)
WHERE (src:Bauteilgruppe OR src:Projekt)
  AND NOT meth_old.id IN $new_meth_ids
DELETE r;


// ---------- §2. HAT_AUFBEREITUNG ----------

MATCH (src)-[r:HAT_AUFBEREITUNG]->(av_old:Aufbereitungsverfahren)
WHERE (src:Bauteilgruppe OR src:Projekt)
  AND NOT av_old.id IN $new_aufb_ids
DELETE r;


// ---------- §3. HAT_RESSOURCENQUELLE ----------

MATCH (src)-[r:HAT_RESSOURCENQUELLE]->(rq_old:Ressourcenquelle)
WHERE (src:Bauteilgruppe OR src:Projekt)
  AND NOT rq_old.id IN $new_rq_ids
DELETE r;


// ---------- §4. HAT_WIEDERVERWENDUNGSART — entire axis retires ----------

MATCH (src)-[r:HAT_WIEDERVERWENDUNGSART]->()
WHERE (src:Bauteilgruppe OR src:Projekt)
DELETE r;
// Note: this drops every WVA edge regardless of target (the axis is gone)


// ---------- §5. HAT_RUECKBAUVERFAHREN (only rv_betonfraesen-targeting edges) ----------

MATCH (src)-[r:HAT_RUECKBAUVERFAHREN]->(rv_old:Rueckbauverfahren)
WHERE (src:Bauteilgruppe OR src:Projekt)
  AND NOT rv_old.id IN $new_rv_ids
DELETE r;
// In practice only rv_betonfraesen-targeting edges match.


// ---------- §6. Post-checks ----------

// 6.1 No remaining BG/Projekt → old-meth edges
MATCH (src)-[r:HAT_METHODE]->(meth_old:Methode)
WHERE (src:Bauteilgruppe OR src:Projekt) AND NOT meth_old.id IN $new_meth_ids
RETURN 'FAIL' AS status, 'HAT_METHODE leftover' AS where_, count(r) AS n;
// expected: 0

MATCH (src)-[r:HAT_AUFBEREITUNG]->(av_old:Aufbereitungsverfahren)
WHERE (src:Bauteilgruppe OR src:Projekt) AND NOT av_old.id IN $new_aufb_ids
RETURN 'FAIL' AS status, 'HAT_AUFBEREITUNG leftover' AS where_, count(r) AS n;
// expected: 0

MATCH (src)-[r:HAT_RESSOURCENQUELLE]->(rq_old:Ressourcenquelle)
WHERE (src:Bauteilgruppe OR src:Projekt) AND NOT rq_old.id IN $new_rq_ids
RETURN 'FAIL' AS status, 'HAT_RESSOURCENQUELLE leftover' AS where_, count(r) AS n;
// expected: 0

MATCH ()-[r:HAT_WIEDERVERWENDUNGSART]->()
RETURN 'FAIL' AS status, 'HAT_WIEDERVERWENDUNGSART axis still has edges' AS where_, count(r) AS n;
// expected: 0

MATCH (src)-[r:HAT_RUECKBAUVERFAHREN]->(rv_old:Rueckbauverfahren)
WHERE (src:Bauteilgruppe OR src:Projekt) AND NOT rv_old.id IN $new_rv_ids
RETURN 'FAIL' AS status, 'HAT_RUECKBAUVERFAHREN leftover' AS where_, count(r) AS n;
// expected: 0


// ---------- Note ----------
// After this phase, the old vocab nodes themselves still exist but have
// zero (or near-zero) inbound edges. Phase 6.5 hard-deletes them.
// DataIssue.CONCERNS edges that pointed at them are already 0 per the
// 2026-06-03 fresh export.
