// ==========================================================================
// mig_q4_surface_urls.cypher
//
// Phase Q4 — Surface source URLs at the node level for visibility in Neo4j
// Browser. Three target labels: :Projekt, :Bauwerk, :Akteur.
//
// Each node gets:
//   source_urls           list<string>   distinct URLs traceable from the node
//   source_count          int            length of source_urls
//   source_urls_updated_at date           when this denormalisation last ran
//
// This is purely DENORMALISED for ergonomics. The graph traversal (Q9 in the
// plan / §9.1 of the plan) remains source-of-truth. Re-run this migration
// whenever new dossiers or URLs are added.
//
// Idempotent. Reversible (REMOVE the three properties).
//
// Plan ref:   _neo4j/QUELLE_REMEDIATION_PLAN.md §5 Q4
// ==========================================================================

// ---------- Q4.A — :Projekt source_urls -----------------------------------
// Two paths to a URL from a Projekt:
//   1. (p)-[:BELEGT_IN]->(:Dossier)-[:ZITIERT_QUELLE]->(:ExternalLink)
//   2. (p)-[:BELEGT_IN]->(:ExternalLink)  (rare, but possible)
MATCH (p:Projekt)
OPTIONAL MATCH (p)-[:BELEGT_IN]->(:Dossier)-[:ZITIERT_QUELLE]->(via_d:ExternalLink)
WITH p, collect(DISTINCT via_d.url) AS via_dossier_urls
OPTIONAL MATCH (p)-[:BELEGT_IN]->(direct:ExternalLink)
WITH p, via_dossier_urls, collect(DISTINCT direct.url) AS direct_urls
WITH p,
     apoc.coll.toSet(
       [u IN (via_dossier_urls + direct_urls) WHERE u IS NOT NULL AND u <> '' | u]
     ) AS all_urls
SET p.source_urls = all_urls,
    p.source_count = size(all_urls),
    p.source_urls_updated_at = date(),
    p.migration_origin = coalesce(p.migration_origin, '') +
        CASE WHEN p.migration_origin IS NULL OR p.migration_origin = ''
             THEN 'mig_q4_surface_urls'
             ELSE ' | mig_q4_surface_urls' END;

// ---------- Q4.B — :Bauwerk source_urls -----------------------------------
// Two paths:
//   1. Inherited from any :Projekt that HAS_BAUWERK to this Bauwerk
//      (using the freshly computed p.source_urls)
//   2. Direct (b)-[:BELEGT_IN]->(:Dossier)-[:ZITIERT_QUELLE]->(:ExternalLink)
MATCH (b:Bauwerk)
OPTIONAL MATCH (b)<-[:HAS_BAUWERK]-(p:Projekt)
WITH b, collect(DISTINCT p.source_urls) AS via_projects
OPTIONAL MATCH (b)-[:BELEGT_IN]->(:Dossier)-[:ZITIERT_QUELLE]->(via_d:ExternalLink)
WITH b, via_projects, collect(DISTINCT via_d.url) AS direct_via_dossier
OPTIONAL MATCH (b)-[:BELEGT_IN]->(direct:ExternalLink)
WITH b, via_projects, direct_via_dossier, collect(DISTINCT direct.url) AS direct_urls
WITH b,
     apoc.coll.flatten(via_projects) + direct_via_dossier + direct_urls AS combined
WITH b,
     apoc.coll.toSet(
       [u IN combined WHERE u IS NOT NULL AND u <> '' | u]
     ) AS all_urls
SET b.source_urls = all_urls,
    b.source_count = size(all_urls),
    b.source_urls_updated_at = date(),
    b.migration_origin = coalesce(b.migration_origin, '') +
        CASE WHEN b.migration_origin IS NULL OR b.migration_origin = ''
             THEN 'mig_q4_surface_urls'
             ELSE ' | mig_q4_surface_urls' END;

// ---------- Q4.C — :Akteur source_urls ------------------------------------
// Actors mostly have direct BELEGT_IN to actor-registry URLs.
MATCH (a:Akteur)
OPTIONAL MATCH (a)-[:BELEGT_IN]->(ext:ExternalLink)
WITH a, collect(DISTINCT ext.url) AS direct_urls
OPTIONAL MATCH (a)-[:BELEGT_IN]->(:Dossier)-[:ZITIERT_QUELLE]->(via_d:ExternalLink)
WITH a, direct_urls, collect(DISTINCT via_d.url) AS dossier_urls
WITH a,
     apoc.coll.toSet(
       [u IN (direct_urls + dossier_urls) WHERE u IS NOT NULL AND u <> '' | u]
     ) AS all_urls
SET a.source_urls = all_urls,
    a.source_count = size(all_urls),
    a.source_urls_updated_at = date(),
    a.migration_origin = coalesce(a.migration_origin, '') +
        CASE WHEN a.migration_origin IS NULL OR a.migration_origin = ''
             THEN 'mig_q4_surface_urls'
             ELSE ' | mig_q4_surface_urls' END;

// ==========================================================================
// Audits
// ==========================================================================

// A1 — Every :Projekt has source_urls (may be empty for orphan projects)
MATCH (p:Projekt) WHERE p.source_urls IS NULL
RETURN 'q4_a1_projekt_without_source_urls' AS rule, count(p) AS violations;

// A2 — Distribution: how many Projekt have at least one URL
MATCH (p:Projekt) WHERE size(coalesce(p.source_urls, [])) > 0
RETURN 'q4_a2_projekt_with_url' AS check, count(p) AS c;

// A3 — Spot-check Stuttgart 210
MATCH (p:Projekt {id:'p_stuttgart_210'})
RETURN 'q4_a3_stuttgart_210' AS check,
       p.source_count AS count, p.source_urls AS urls;

// A4 — Spot-check Holbein Gardens
MATCH (p:Projekt {id:'p_holbein_gardens_london'})
RETURN 'q4_a4_holbein_gardens' AS check,
       p.source_count AS count, p.source_urls AS urls;

// A5 — Bauwerk coverage
MATCH (b:Bauwerk) WHERE size(coalesce(b.source_urls, [])) > 0
RETURN 'q4_a5_bauwerk_with_url' AS check, count(b) AS c;

// A6 — Akteur coverage
MATCH (a:Akteur) WHERE size(coalesce(a.source_urls, [])) > 0
RETURN 'q4_a6_akteur_with_url' AS check, count(a) AS c;

// A7 — Flag Projekt with > 50 URLs (might be too-many-sources :DataIssue)
MATCH (p:Projekt) WHERE p.source_count > 50
RETURN 'q4_a7_projekt_with_excessive_sources' AS check,
       p.id AS projekt, p.source_count AS n;

// A8 — Top-10 Projekt by source_count
MATCH (p:Projekt) WHERE p.source_count > 0
RETURN 'q4_a8_top_sources' AS check, p.id AS projekt, p.source_count AS n
ORDER BY p.source_count DESC LIMIT 10;

// A9 — Average source_count across all Projekt that have at least one URL
MATCH (p:Projekt) WHERE p.source_count > 0
RETURN 'q4_a9_avg_sources_when_present' AS check,
       avg(p.source_count) AS avg_sources,
       min(p.source_count) AS min_sources,
       max(p.source_count) AS max_sources,
       count(p) AS projekt_with_sources;
