"""Full audit of Bauteilbörse subgraph - find gaps, inconsistencies, improper info."""
from pathlib import Path
from neo4j import GraphDatabase

pw = Path('.neo4j_password').read_text(encoding='utf-8').strip()
d = GraphDatabase.driver('neo4j://127.0.0.1:7687', auth=('neo4j', pw))


def section(title):
    print()
    print('=' * 80)
    print(title)
    print('=' * 80)


with d.session(database='mit-bestand') as s:
    # ----- BASELINE -----
    section('BASELINE: How many Bauteilbörse anchors exist?')
    q = """
    MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
    RETURN count(DISTINCT a) AS n
    """
    n = s.run(q).single()['n']
    print(f'  Anchors with HAT_GESCHAEFTSMODELL: {n}')

    n2 = s.run("MATCH (a)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'}) RETURN count(a) AS n").single()['n']
    print(f'  Actors with at_materialhub_bauteilboerse: {n2}')

    # ----- FLAG 1: GM/MM conflicts -----
    section('FLAG 1: GM vs MM logic conflicts')
    q = """
    MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)
    WITH a, collect(DISTINCT g.id) AS gms
    MATCH (a)-[:HAT_MARKTMODELL]->(m)
    WITH a, gms, m.id AS mm
    RETURN a.id AS id, gms, mm
    ORDER BY id
    """
    rows = list(s.run(q))
    conflicts = []
    for r in rows:
        gms = set(r['gms']); mm = r['mm']
        # Pure shop with mm_plattform_vermittelt = unusual (should be mm_kauf_gebraucht)
        if gms == {'gm_shop_eigenstock'} and mm == 'mm_plattform_vermittelt':
            conflicts.append((r['id'], 'pure shop but plattform_vermittelt', gms, mm))
        # Pure marketplace with mm_kauf_gebraucht = unusual
        if gms == {'gm_marketplace_vermittlung'} and mm == 'mm_kauf_gebraucht':
            conflicts.append((r['id'], 'pure marketplace but kauf_gebraucht', gms, mm))
        # Network/aggregator with mm_kauf_gebraucht = wrong
        if gms == {'gm_netzwerk_aggregator'} and mm == 'mm_kauf_gebraucht':
            conflicts.append((r['id'], 'network/aggregator but kauf_gebraucht', gms, mm))
    print(f'  {len(conflicts)} conflicts:')
    for c in conflicts:
        print(f'  - {c[0]:50s} {c[1]} (gms={c[2]} mm={c[3]})')

    # ----- FLAG 2: schema completeness -----
    section('FLAG 2: schema_check failures (every anchor)')
    q = """
    MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
    WITH DISTINCT a
    OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp)        WITH a, count(t) AS n_typ
    OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(l:Land)             WITH a, n_typ, count(l) AS n_land
    OPTIONAL MATCH (a)-[:HAT_MARKTMODELL]->(m:Marktmodell)    WITH a, n_typ, n_land, count(m) AS n_mm
    OPTIONAL MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)           WITH a, n_typ, n_land, n_mm, count(g) AS n_gm
    OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle)    WITH a, n_typ, n_land, n_mm, n_gm, count(r) AS n_roles
    OPTIONAL MATCH (a)-[:BELEGT_IN]->(q:Quelle)               WITH a, n_typ, n_land, n_mm, n_gm, n_roles, count(q) AS n_ev
    OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(mm:Material)       WITH a, n_typ, n_land, n_mm, n_gm, n_roles, n_ev, count(mm) AS n_mat
    OPTIONAL MATCH (a)-[:HAT_BAUTEILTYP]->(bb:Bauteiltyp)     WITH a, n_typ, n_land, n_mm, n_gm, n_roles, n_ev, n_mat, count(bb) AS n_bt
    RETURN a.id AS id, labels(a) AS lbls, n_typ, n_land, n_mm, n_gm, n_roles, n_ev, n_mat, n_bt
    ORDER BY id
    """
    rows = list(s.run(q))
    fails = []
    for r in rows:
        issues = []
        # software_restado is :Software, exempt from n_typ requirement
        is_software = 'Software' in r['lbls']
        if not is_software and r['n_typ'] < 1: issues.append(f"typ={r['n_typ']}")
        if r['n_land'] != 1: issues.append(f"land={r['n_land']}")
        if r['n_mm'] != 1: issues.append(f"mm={r['n_mm']}")
        if r['n_gm'] < 1: issues.append(f"gm={r['n_gm']}")
        if r['n_roles'] < 3: issues.append(f"roles={r['n_roles']}<3")
        if r['n_ev'] < 2: issues.append(f"ev={r['n_ev']}<2")
        if issues:
            fails.append((r['id'], issues, r['lbls']))
    print(f'  {len(fails)} anchors failing schema_check:')
    for f in fails:
        print(f'  - {f[0]:50s} {f[2]}  issues: {",".join(f[1])}')

    # ----- FLAG 3: Material/Bauteiltyp coverage gaps -----
    section('FLAG 3: anchors with NO Material AND NO Bauteiltyp')
    q = """
    MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
    WITH DISTINCT a
    OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(m)
    WITH a, count(m) AS n_mat
    OPTIONAL MATCH (a)-[:HAT_BAUTEILTYP]->(b)
    WITH a, n_mat, count(b) AS n_bt
    WHERE n_mat = 0 AND n_bt = 0
    RETURN a.id AS id, n_mat, n_bt
    ORDER BY id
    """
    rows = list(s.run(q))
    print(f'  {len(rows)} anchors with no Material AND no Bauteiltyp:')
    for r in rows: print(f'  - {dict(r)}')

    # ----- FLAG 4: rich-bt-no-mat or rich-mat-no-bt -----
    section('FLAG 4: imbalanced coverage')
    q = """
    MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
    WITH DISTINCT a
    OPTIONAL MATCH (a)-[:NUTZT_MATERIAL]->(m) WITH a, count(m) AS n_mat
    OPTIONAL MATCH (a)-[:HAT_BAUTEILTYP]->(b) WITH a, n_mat, count(b) AS n_bt
    WHERE (n_bt >= 5 AND n_mat = 0) OR (n_mat >= 4 AND n_bt = 0)
    RETURN a.id AS id, n_mat, n_bt
    ORDER BY n_mat+n_bt DESC
    """
    rows = list(s.run(q))
    print(f'  {len(rows)} anchors with imbalanced coverage:')
    for r in rows: print(f'  - {dict(r)}')

    # ----- FLAG 5: at_materialhub without HAT_GESCHAEFTSMODELL -----
    section('FLAG 5: at_materialhub_bauteilboerse actors WITHOUT HAT_GESCHAEFTSMODELL (un-classified)')
    rows = list(s.run("""
        MATCH (a)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
        WHERE NOT (a)-[:HAT_GESCHAEFTSMODELL]->()
        RETURN a.id AS id, labels(a) AS lbls
        ORDER BY id
    """))
    print(f'  {len(rows)} actors:')
    for r in rows: print(f'  - {dict(r)["id"]:50s} lbls={dict(r)["lbls"]}')

    # ----- FLAG 6: HAT_GESCHAEFTSMODELL without proper Akteurtyp -----
    section('FLAG 6: anchors with HAT_GESCHAEFTSMODELL but NOT at_materialhub_bauteilboerse')
    rows = list(s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        WHERE NOT (a)-[:HAT_AKTEURTYP]->(:Akteurtyp {id:'at_materialhub_bauteilboerse'})
        RETURN a.id AS id, labels(a) AS lbls
        ORDER BY id
    """))
    print(f'  {len(rows)} (expected: software_restado + bauteilnetz_deutschland):')
    for r in rows: print(f'  - {dict(r)["id"]:50s} lbls={dict(r)["lbls"]}')

    # ----- FLAG 7: distributions -----
    section('FLAG 7: Marktmodell distribution among anchors')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        MATCH (a)-[:HAT_MARKTMODELL]->(m)
        RETURN m.id, count(DISTINCT a) AS n ORDER BY n DESC
    """):
        print(f'  {dict(r)}')

    section('FLAG 8: Geschäftsmodell distribution')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->(g)
        RETURN g.id, count(DISTINCT a) AS n ORDER BY n DESC
    """):
        print(f'  {dict(r)}')

    section('FLAG 9: Country distribution')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        MATCH (a)-[:LIEGT_IN_LAND]->(l)
        RETURN l.id, count(DISTINCT a) AS n ORDER BY n DESC
    """):
        print(f'  {dict(r)}')

    section('FLAG 10: Akteurrolle universal-coverage check')
    universal = ['ar_materialbroker','ar_materiallieferung_markt','ar_software_digitalisierung']
    for rid in universal:
        rows = list(s.run("""
            MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
            WHERE NOT (a)-[:HAT_AKTEURROLLE]->(:Akteurrolle {id:$rid})
            RETURN a.id AS id ORDER BY id
        """, rid=rid))
        if rows:
            print(f'  {rid}: missing on {len(rows)} anchors')
            for r in rows: print(f'     - {dict(r)["id"]}')
        else:
            print(f'  {rid}: present on all anchors')

    section('FLAG 11: BELEGT_IN under-coverage (anchors with <2 evidence URLs)')
    rows = list(s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        WITH DISTINCT a
        OPTIONAL MATCH (a)-[:BELEGT_IN]->(q)
        WITH a.id AS id, count(q) AS n
        WHERE n < 2
        RETURN id, n
    """))
    print(f'  {len(rows)} anchors:')
    for r in rows: print(f'  - {dict(r)}')

    section('FLAG 12: Operator chain (BETRIEBEN_VON)')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        MATCH (a)-[:BETRIEBEN_VON]->(op)
        RETURN a.id AS actor, op.id AS operator
        ORDER BY actor
    """):
        print(f'  {dict(r)}')

    section('FLAG 13: VERBUNDEN_MIT_AKTEUR among anchors')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        MATCH (a)-[:VERBUNDEN_MIT_AKTEUR]->(b)
        WHERE (b)-[:HAT_GESCHAEFTSMODELL]->() OR b.id IN ['bauteilnetz_deutschland']
        RETURN a.id AS a, b.id AS b
        ORDER BY a, b
    """):
        print(f'  {dict(r)}')

    section('FLAG 14: Methode leakage (urban-mining methods on non-urban-mining anchors)')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        WHERE NOT (a)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_dienstleistung_urban_mining'})
              AND NOT (a)-[:HAT_GESCHAEFTSMODELL]->(:Geschaeftsmodell {id:'gm_saas_inventar_plattform'})
        MATCH (a)-[:HAT_METHODE]->(m)
        RETURN a.id AS actor, collect(DISTINCT m.id) AS methods
        ORDER BY actor
    """):
        print(f'  {dict(r)}')

    section('FLAG 15: Akteurtyp inventory of anchors (look for unexpected types)')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t)
        WITH a.id AS id, collect(DISTINCT t.id) AS types
        WHERE size([x IN types WHERE NOT x IN ['at_materialhub_bauteilboerse','at_software_tool_anbieter','at_unternehmen','at_ngo_verband_netzwerk','at_organisation']])>0 OR size(types)>2
        RETURN id, types ORDER BY id
    """):
        print(f'  {dict(r)}')

    section('FLAG 16: Material distribution per anchor (top of histogram)')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        MATCH (a)-[:NUTZT_MATERIAL]->(m)
        RETURN m.id, count(DISTINCT a) AS n ORDER BY n DESC
    """):
        print(f'  {dict(r)}')

    section('FLAG 17: Bauteiltyp distribution per anchor')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        MATCH (a)-[:HAT_BAUTEILTYP]->(b)
        RETURN b.id, count(DISTINCT a) AS n ORDER BY n DESC
    """):
        print(f'  {dict(r)}')

    section('FLAG 18: Materials untouched by any Bauteilbörse')
    for r in s.run("""
        MATCH (m:Material) WHERE m.id STARTS WITH 'mat_'
        AND NOT (m)<-[:NUTZT_MATERIAL]-(:Akteur)-[:HAT_GESCHAEFTSMODELL]->()
        RETURN m.id ORDER BY m.id
    """):
        print(f'  {dict(r)["m.id"]}')

    section('FLAG 19: Bauteiltypen untouched by any Bauteilbörse')
    for r in s.run("""
        MATCH (b:Bauteiltyp) WHERE b.id STARTS WITH 'bt_'
        AND NOT (b)<-[:HAT_BAUTEILTYP]-(:Akteur)-[:HAT_GESCHAEFTSMODELL]->()
        RETURN b.id ORDER BY b.id
    """):
        print(f'  {dict(r)["b.id"]}')

    section('FLAG 20: Property-level checks on Akteur nodes')
    for r in s.run("""
        MATCH (a)-[:HAT_GESCHAEFTSMODELL]->()
        WITH a WHERE a.name IS NULL OR a.source_scope IS NULL
        RETURN a.id AS id, a.name AS name, a.source_scope AS scope
        ORDER BY id
    """):
        print(f'  {dict(r)}')

d.close()
