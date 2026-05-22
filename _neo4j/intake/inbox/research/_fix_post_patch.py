"""Fix 8 schema_check failures left after the 580-edge JSON back-sync."""
from pathlib import Path
from neo4j import GraphDatabase
import hashlib

pw = Path('.neo4j_password').read_text(encoding='utf-8').strip()
d = GraphDatabase.driver('neo4j://127.0.0.1:7687', auth=('neo4j', pw))
TAG = 'json_back_sync_fix_2026_06_02'


def md5(s): return hashlib.md5(s.encode()).hexdigest()


with d.session(database='mit-bestand') as s:
    print('=== enviromate Marktmodell check (before fix) ===')
    for r in s.run("""MATCH (a {id:'enviromate'})-[r:HAT_MARKTMODELL]->(m)
        RETURN m.id AS mm, r.evidence_basis AS basis, r.review_run AS run, elementId(r) AS reid"""):
        print(f"  {dict(r)}")

    print()
    print('=== STEP 1: universal roles (label-agnostic) ===')
    failing = ['software_ecotool', 'software_opalis', 'software_qflow', 'tool_qflow',
               'software_concular', 'tool_hts_stockmatcher', 'opalis', 'harvestmap']
    for aid in failing:
        for rid in ['ar_materialbroker', 'ar_materiallieferung_markt', 'ar_software_digitalisierung']:
            c = s.run("""MATCH (a {id:$aid}), (r:Akteurrolle {id:$rid})
                MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
                ON CREATE SET rel.evidence_basis='universal_bauteilboerse_role', rel.review_run=$tag""",
                aid=aid, rid=rid, tag=TAG).consume().counters
            if c.relationships_created:
                print(f'  + {aid:30s} -> {rid}')

    print()
    print('=== STEP 2: cluster fingerprints (label-agnostic) ===')
    fingerprint_role = {
        'gm_shop_eigenstock': ['ar_materialbroker'],
        'gm_marketplace_vermittlung': ['ar_materialbroker', 'ar_software_digitalisierung'],
        'gm_dienstleistung_urban_mining': [
            'ar_rueckbau_bauteilernte_logistik', 'ar_aufbereitung_refurbishment',
            'ar_materiallieferung_markt', 'ar_reuse_zirkularitaetsberatung'],
        'gm_saas_inventar_plattform': ['ar_software_digitalisierung', 'ar_forschung_dokumentation'],
        'gm_netzwerk_aggregator': ['ar_bildung_wissenstransfer', 'ar_forschung_dokumentation', 'ar_materialbroker'],
    }
    fingerprint_meth = {
        'gm_dienstleistung_urban_mining': ['meth_urban_mining', 'meth_pre_deconstruction_audit', 'meth_bauteilkatalogisierung'],
        'gm_saas_inventar_plattform': ['meth_materialinventur', 'meth_bauteilkatalogisierung', 'meth_abrissmonitoring'],
    }
    for aid in failing:
        gms = [r['gid'] for r in s.run("MATCH (a {id:$aid})-[:HAT_GESCHAEFTSMODELL]->(g) RETURN g.id AS gid", aid=aid)]
        for gid in gms:
            for rid in fingerprint_role.get(gid, []):
                c = s.run("""MATCH (a {id:$aid}), (r:Akteurrolle {id:$rid})
                    MERGE (a)-[rel:HAT_AKTEURROLLE]->(r)
                    ON CREATE SET rel.evidence_basis='gm_fingerprint', rel.review_run=$tag""",
                    aid=aid, rid=rid, tag=TAG).consume().counters
                if c.relationships_created:
                    print(f'  + {aid:30s} -> {rid} (via {gid})')
            for mid in fingerprint_meth.get(gid, []):
                c = s.run("""MATCH (a {id:$aid}), (m:Methode {id:$mid})
                    MERGE (a)-[rel:HAT_METHODE]->(m)
                    ON CREATE SET rel.evidence_basis='gm_fingerprint', rel.review_run=$tag""",
                    aid=aid, mid=mid, tag=TAG).consume().counters
                if c.relationships_created:
                    print(f'  + {aid:30s} -> {mid} (via {gid})')

    print()
    print('=== STEP 3: missing land / Marktmodell ===')
    fixes = [
        ('software_ecotool', 'LIEGT_IN_LAND', 'land_deutschland', 'Land'),
        ('software_ecotool', 'HAT_MARKTMODELL', 'mm_plattform_vermittelt', 'Marktmodell'),
        ('software_qflow',   'HAT_MARKTMODELL', 'mm_plattform_vermittelt', 'Marktmodell'),
        ('tool_qflow',       'HAT_MARKTMODELL', 'mm_plattform_vermittelt', 'Marktmodell'),
        ('tool_hts_stockmatcher', 'HAT_MARKTMODELL', 'mm_plattform_vermittelt', 'Marktmodell'),
    ]
    for aid, rel, tid, tlbl in fixes:
        c = s.run(f"""MATCH (a {{id:$aid}}), (t:{tlbl} {{id:$tid}})
            MERGE (a)-[r:`{rel}`]->(t)
            ON CREATE SET r.evidence_basis='audit_post_patch', r.review_run=$tag""",
            aid=aid, tid=tid, tag=TAG).consume().counters
        print(f'  + {aid:30s} -[{rel}]-> {tid}: r+={c.relationships_created}')

    print()
    print('=== STEP 4: canonical evidence URLs ===')
    urls = [
        ('opalis', 'https://opalis.eu/'),
        ('opalis', 'https://opalis.eu/en/about'),
        ('software_concular', 'https://concular.de/restado/'),
        ('software_concular', 'https://restado.de/'),
        ('software_ecotool', 'https://concular.de/ecotool/'),
        ('software_ecotool', 'https://www.concular.de/'),
        ('software_qflow', 'https://qflow.io/'),
        ('software_qflow', 'https://qflow.io/about/'),
        ('tool_qflow', 'https://qflow.io/'),
        ('tool_qflow', 'https://qflow.io/about/'),
        ('tool_hts_stockmatcher', 'https://www.heynetillettsteel.com/research/'),
        ('tool_hts_stockmatcher', 'https://www.heynetillettsteel.com/'),
        ('software_opalis', 'https://opalis.eu/'),
        ('software_opalis', 'https://opalis.eu/en/about'),
    ]
    for aid, url in urls:
        qid = f'q_url_{md5(url)}'
        c = s.run("""MATCH (a {id:$aid})
            MERGE (q:Quelle:ExternalLink {id:$qid})
              ON CREATE SET q.url=$url, q.quelltyp='external_link', q.review_run=$tag
              ON MATCH SET q.url=coalesce(q.url, $url), q.quelltyp=coalesce(q.quelltyp,'external_link')
            MERGE (a)-[r:BELEGT_IN]->(q)
              ON CREATE SET r.evidence_basis='audit_post_patch', r.review_run=$tag""",
            aid=aid, qid=qid, url=url, tag=TAG).consume().counters
        if c.relationships_created:
            print(f'  + {aid:30s} BELEGT_IN -> {url}')

    print()
    print('=== STEP 5: enviromate duplicate MM resolution ===')
    rows = list(s.run("""MATCH (a {id:'enviromate'})-[r:HAT_MARKTMODELL]->(m)
        RETURN m.id AS mm, r.evidence_basis AS basis, elementId(r) AS reid"""))
    for r in rows: print(f"  {dict(r)}")
    if len(rows) > 1:
        for r in rows:
            if r['mm'] != 'mm_plattform_vermittelt':
                s.run("MATCH ()-[r]->() WHERE elementId(r)=$reid DELETE r", reid=r['reid'])
                print(f"  removed {r['mm']} (kept mm_plattform_vermittelt)")

    # ----- FINAL CHECK -----
    print()
    print('=== FINAL schema_check ===')
    rows = list(s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        WITH DISTINCT a
        OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t) WITH a, count(t) AS n_typ
        OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l) WITH a, n_typ, count(l) AS n_land
        OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m) WITH a, n_typ, n_land, count(m) AS n_mm
        OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g) WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
        OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r) WITH a, n_typ, n_land, n_mm, n_gm, count(r) AS n_roles
        OPTIONAL MATCH (a)-[:BELEGT_IN]->(q) WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_ev
        RETURN a.id AS id, labels(a) AS lbls, n_typ, n_land, n_mm, n_gm, n_roles, n_ev"""))
    ok = 0; fails = []
    for r in rows:
        d_ = dict(r); is_soft = bool({'Software', 'Tool'} & set(d_['lbls']))
        valid = ((d_['n_typ'] >= 1 or is_soft) and d_['n_land'] >= 1 and d_['n_mm'] == 1 and
                 d_['n_gm'] >= 1 and d_['n_roles'] >= 3 and d_['n_ev'] >= 2)
        if valid: ok += 1
        else: fails.append(d_)
    print(f'{ok}/{len(rows)} PASS')
    for f in fails:
        print(f"  [FAIL] {f['id']:35s} typ={f['n_typ']} land={f['n_land']} mm={f['n_mm']} gm={f['n_gm']} roles={f['n_roles']} ev={f['n_ev']}")

d.close()
