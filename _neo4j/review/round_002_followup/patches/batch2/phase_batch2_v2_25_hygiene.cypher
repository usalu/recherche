// Phase 25 — Bucket D hygiene (corpus-wide consistency)
//
// Three operations:
//   25a — Create q_controlled_vocab_seed Quelle node + BELEGT_IN from all
//          ~379 unsourced controlled-vocabulary nodes.
//   25b — source_scope backfill via id-pattern rules.
//   25c — case-specific case-scope cleanup.
//
// All operations idempotent (MERGE-based + SET only-where-null).

// ============================================================================
// 25a — Vocab seed Quelle + BELEGT_IN backfill
// ============================================================================

MERGE (q:Quelle {id: 'q_controlled_vocab_seed'})
ON CREATE SET q.name = 'Controlled-vocab seed',
              q.name_full = 'Controlled vocabulary seed source — definitional taxonomy file (controlled_vocabulary.seed.kg.jsonl)',
              q.quelltyp = 'controlled_vocab_seed',
              q.source_file = '_neo4j/intake/controlled_vocabulary.seed.kg.jsonl',
              q.source_scope = 'controlled_vocab_seed',
              q.access_date = '2026-05-20';

// Link all unsourced controlled-vocab nodes to it
MATCH (n) WHERE NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) }
  AND any(l IN labels(n) WHERE l IN [
    'Akteurrolle','Akteurtyp','Aufbereitungsverfahren','BauaufgabeIntervention',
    'Bauobjektklasse','Bauobjektrolle','Bauproduktstatus','Bausystem','Bauteilebene',
    'Bauteiltyp','Bauweise','BauwerkEra','Beschaffungsweg','Defekt','Funktionswechsel',
    'Huerde','HuerdeKategorie','Layer','LebenszyklusModul','Leistungsanforderung',
    'Logistik','Marktmodell','MatchingQualitaet','Material','Materialgruppe','Methode',
    'Nutzung','PruefungNachweis','Prozessphase','Ressourcenquelle','Rueckbauverfahren',
    'Schadstoff','Status','Tragwerksprinzip','Verbindungstechnik','WiederverwendungsArt',
    'ZustandsKlasse','Wirtschaft','Akzeptanz'
  ])
WITH n
MATCH (q:Quelle {id: 'q_controlled_vocab_seed'})
MERGE (n)-[r:BELEGT_IN]->(q)
ON CREATE SET r.id = 'r_' + n.id + '__BELEGT_IN__q_controlled_vocab_seed',
              r.source = 'batch2_v2_phase25_2026-05-20',
              r.evidence = 'BELEGT';

// ============================================================================
// 25b — source_scope backfill via id-pattern rules (only where null)
// ============================================================================

// Quelle nodes by id prefix
MATCH (q:Quelle) WHERE q.source_scope IS NULL AND q.id STARTS WITH 'q_actor_'
SET q.source_scope = 'actor_registry';

MATCH (q:Quelle) WHERE q.source_scope IS NULL AND q.id ENDS WITH '_md'
SET q.source_scope = 'case_markdown';

MATCH (q:Quelle) WHERE q.source_scope IS NULL AND q.id STARTS WITH 'q_akteursliste'
SET q.source_scope = 'actor_registry_markdown';

MATCH (q:Quelle) WHERE q.source_scope IS NULL
SET q.source_scope = 'external_reference';

// Akteure missing source_scope → actor_registry (most came from CSV import)
MATCH (a:Akteur) WHERE a.source_scope IS NULL
SET a.source_scope = 'actor_registry';

// All controlled-vocab nodes → controlled_vocab_seed
MATCH (n) WHERE n.source_scope IS NULL
  AND any(l IN labels(n) WHERE l IN [
    'Akteurrolle','Akteurtyp','Aufbereitungsverfahren','BauaufgabeIntervention',
    'Bauobjektklasse','Bauobjektrolle','Bauproduktstatus','Bausystem','Bauteilebene',
    'Bauteiltyp','Bauweise','BauwerkEra','Beschaffungsweg','Defekt','Funktionswechsel',
    'Huerde','HuerdeKategorie','Layer','LebenszyklusModul','Leistungsanforderung',
    'Logistik','Marktmodell','MatchingQualitaet','Material','Materialgruppe','Methode',
    'Nutzung','PruefungNachweis','Prozessphase','Ressourcenquelle','Rueckbauverfahren',
    'Schadstoff','Status','Tragwerksprinzip','Verbindungstechnik','WiederverwendungsArt',
    'ZustandsKlasse','Wirtschaft','Akzeptanz','Norm','ZertifizierungBewertungssystem',
    'Software','Tool','Programm','Land','Stadt'
  ])
SET n.source_scope = 'controlled_vocab_seed';

// 25c — Case-specific case-scope cleanup
// All remaining nodes (Projekt, Bauwerk, Bauteilgruppe, Wiederverwendungskette)
// without source_scope likely came from archive scans
MATCH (n) WHERE n.source_scope IS NULL
  AND any(l IN labels(n) WHERE l IN ['Projekt','Bauwerk','Bauteilgruppe','Wiederverwendungskette','Datenqualitaet','Tag'])
SET n.source_scope = 'archive_scan';

// Final fallback: anything else missing → 'derived'
MATCH (n) WHERE n.source_scope IS NULL
SET n.source_scope = 'derived';

// ============================================================================
// Verification
// ============================================================================
// MATCH (n) WHERE n.source_scope IS NULL RETURN count(n);
// EXPECTED: 0.
//
// MATCH (n) RETURN n.source_scope AS s, count(n) AS c ORDER BY c DESC;
// EXPECTED: case_markdown (~235), actor_registry (~500), controlled_vocab_seed (~500),
//           archive_scan (~600), external_reference (~50), derived (~40), etc.
//
// MATCH (n)-[:BELEGT_IN]->(q:Quelle {id: 'q_controlled_vocab_seed'}) RETURN count(n);
// EXPECTED: ~379.
