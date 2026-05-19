"""One-shot audit script: scan the live graph for quality/improvement opportunities.

Reports findings against the conventions established in NAMING_AND_PROPERTIES_PLAN.md.
"""
from neo4j import GraphDatabase
from _scripts.neo4j_env import resolve_connection


def main() -> None:
    uri, user, password, db = resolve_connection()
    d = GraphDatabase.driver(uri, auth=(user, password))

    checks = [
        ("1a. Nodes missing id",
         "MATCH (n) WHERE n.id IS NULL RETURN labels(n)[0] AS lbl, count(*) AS c"),
        ("1b. Nodes missing name",
         "MATCH (n) WHERE n.name IS NULL AND n.id IS NOT NULL RETURN labels(n)[0] AS lbl, count(*) AS c ORDER BY c DESC"),
        ("1c. Nodes with name > 25 chars",
         "MATCH (n) WHERE n.name IS NOT NULL AND size(n.name) > 25 RETURN labels(n)[0] AS lbl, count(*) AS c ORDER BY c DESC"),
        ("1d. name_full = name (redundant per Q3)",
         "MATCH (n) WHERE n.name_full = n.name RETURN labels(n)[0] AS lbl, count(*) AS c"),

        ("2a. BG primary_material_id=mat_mehrere but actually has <2 materials",
         """MATCH (bg:Bauteilgruppe)
            OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material)
            WITH bg, count(m) AS c
            WHERE bg.primary_material_id = 'mat_mehrere' AND c < 2
            RETURN bg.id AS id, c"""),
        ("2b. BG primary_material_id specific but has multiple mats",
         """MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->(m:Material)
            WITH bg, count(DISTINCT m) AS c
            WHERE NOT bg.primary_material_id IN ['mat_mehrere','mat_unbekannt'] AND c > 1
            RETURN bg.id AS id, bg.primary_material_id AS pmat, c LIMIT 15"""),
        ("2c. BG with mismatched primary_bauteiltyp_id",
         """MATCH (bg:Bauteilgruppe)
            OPTIONAL MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
            WITH bg, collect(bt.id) AS bts
            WHERE (bg.primary_bauteiltyp_id = 'bt_mehrere' AND size(bts) < 2)
               OR (NOT bg.primary_bauteiltyp_id IN ['bt_mehrere','bt_unbekannt'] AND size(bts) > 1 AND NOT bg.primary_bauteiltyp_id IN bts)
            RETURN bg.id AS id, bg.primary_bauteiltyp_id AS pbt, bts LIMIT 15"""),
        ("2d. BG missing primary_material_id",
         "MATCH (bg:Bauteilgruppe) WHERE bg.primary_material_id IS NULL RETURN bg.id LIMIT 5"),
        ("2e. BG missing reuse_status",
         "MATCH (bg:Bauteilgruppe) WHERE bg.reuse_status IS NULL RETURN bg.id LIMIT 5"),
        ("2f. BG id not matching schema",
         """MATCH (bg:Bauteilgruppe) WHERE NOT bg.id STARTS WITH 'bg_reuse_'
            AND NOT bg.id STARTS WITH 'bg_retained_'
            AND NOT bg.id STARTS WITH 'bg_planned_'
            AND NOT bg.id STARTS WITH 'bg_dismantled_'
            RETURN bg.id"""),

        ("3a. Case-specific nodes missing BELEGT_IN",
         """MATCH (n) WHERE any(l IN labels(n) WHERE l IN ['Projekt','Bauteilgruppe','Bauwerk','Wiederverwendungskette','Stadt'])
            AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) }
            RETURN labels(n)[0] AS lbl, count(*) AS c"""),
        ("3b. Inferred BG rels missing r.source",
         """MATCH (bg:Bauteilgruppe)-[r:HAT_DEFEKT|HAT_MARKTMODELL]->()
            WHERE r.source IS NULL RETURN type(r) AS rt, count(r) AS c"""),

        ("4a. Nodes with 0 rels",
         "MATCH (n) WHERE NOT (n)-[]-() RETURN labels(n)[0] AS lbl, n.id AS id LIMIT 20"),
        ("4b. BGs with NUTZT_MATERIAL but missing HAT_MATERIALGRUPPE",
         """MATCH (bg:Bauteilgruppe)-[:NUTZT_MATERIAL]->()
            WITH bg WHERE NOT (bg)-[:HAT_MATERIALGRUPPE]->()
            RETURN bg.id AS id, bg.primary_material_id AS pmat LIMIT 15"""),

        ("5a. Rels with missing r.id (top labels)",
         "MATCH ()-[r]->() WHERE r.id IS NULL RETURN type(r) AS rt, count(r) AS c ORDER BY c DESC LIMIT 8"),
        ("5b. Duplicate r.id",
         "MATCH ()-[r]->() WHERE r.id IS NOT NULL WITH r.id AS rid, count(*) AS c WHERE c > 1 RETURN rid, c LIMIT 5"),

        ("6. Akteur stars_ignored leak",
         "MATCH (a:Akteur) WHERE a.stars_ignored IS NOT NULL RETURN count(a) AS c"),

        ("7a. Quelle without name", "MATCH (q:Quelle) WHERE q.name IS NULL RETURN count(q) AS c"),
        ("7b. Quelle still with old titel", "MATCH (q:Quelle) WHERE q.titel IS NOT NULL RETURN count(q) AS c"),
        ("7c. Quelltyp values out of canonical enum",
         """MATCH (q:Quelle) WHERE NOT q.quelltyp IN
            ['external_link_from_actor_registry','case_markdown','external_reference','actor_registry_markdown']
            AND q.quelltyp IS NOT NULL RETURN q.quelltyp AS qt, count(*) AS c"""),

        ("8. Land sovereign nodes still missing country_iso2",
         """MATCH (l:Land) WHERE l.country_iso2 IS NULL AND NOT l.id IN ['land_eu','land_eea','land_international']
            RETURN l.id"""),

        ("9. BGs missing aliases",
         "MATCH (bg:Bauteilgruppe) WHERE bg.aliases IS NULL OR size(bg.aliases) = 0 RETURN bg.id"),

        ("10. BG name collisions",
         """MATCH (bg:Bauteilgruppe) WITH bg.name AS nm, collect(bg.id) AS ids WHERE size(ids) > 1
            RETURN nm, ids LIMIT 10"""),

        ("11a. Projekt missing bewertung", "MATCH (p:Projekt) WHERE p.bewertung IS NULL RETURN count(p) AS c"),
        ("11b. Projekt missing source_scope", "MATCH (p:Projekt) WHERE p.source_scope IS NULL RETURN count(p) AS c"),
        ("11c. Projekt missing node_role", "MATCH (p:Projekt) WHERE p.node_role IS NULL RETURN count(p) AS c"),

        ("12. retained BGs with HAT_WIEDERVERWENDUNGSART=direkte (possibly wrong)",
         """MATCH (bg:Bauteilgruppe {reuse_status:'retained'})-[:HAT_WIEDERVERWENDUNGSART]->(w {id:'wva_direkte_wiederverwendung'})
            RETURN count(bg) AS c"""),

        ("13. People's Pavilion HAT_MATERIALGRUPPE coverage",
         """MATCH (bg) WHERE 'bg_peoples_pavilion_borrowed_facade_elements' IN bg.aliases
            OPTIONAL MATCH (bg)-[:HAT_MATERIALGRUPPE]->(g)
            RETURN bg.id AS id, collect(g.id) AS groups"""),

        ("14. Træ windturbine Materialgruppe",
         """MATCH (bg) WHERE 'bg_trae_high_rise_aarhus_windturbinenfluegel_als_sonnenschutz' IN bg.aliases
            OPTIONAL MATCH (bg)-[:HAT_MATERIALGRUPPE]->(g)
            RETURN bg.id AS id, collect(g.id) AS groups"""),

        ("15. Total counts",
         "MATCH (n) WITH count(n) AS nodes MATCH ()-[r]->() RETURN nodes, count(r) AS rels"),

        ("16. Bauteilgruppe property population (out of 308)",
         """MATCH (bg:Bauteilgruppe) RETURN
            count(CASE WHEN bg.name IS NOT NULL THEN 1 END) AS has_name,
            count(CASE WHEN bg.name_full IS NOT NULL THEN 1 END) AS has_nf,
            count(CASE WHEN bg.aliases IS NOT NULL THEN 1 END) AS has_aliases,
            count(CASE WHEN bg.raw_name IS NOT NULL THEN 1 END) AS has_raw,
            count(CASE WHEN bg.counts_as_direct_reuse IS NOT NULL THEN 1 END) AS has_cadr,
            count(CASE WHEN bg.alte_funktion IS NOT NULL THEN 1 END) AS has_af,
            count(CASE WHEN bg.neue_funktion IS NOT NULL THEN 1 END) AS has_nfn"""),
    ]

    with d.session(database=db) as s:
        for label, q in checks:
            print(f"═══ {label}")
            rows = list(s.run(q))
            if not rows:
                print("   ✓ (empty)")
            else:
                for r in rows[:20]:
                    print(f"   {dict(r)}")
            print()

    d.close()


if __name__ == "__main__":
    main()
