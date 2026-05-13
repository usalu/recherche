"""
Deep-dive into the actual content of projects from batches 015-019.
Queries Neo4j for every project and its connected graph.
"""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, '_scripts')
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

uri, user, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, pw))

def q(cypher, **params):
    with driver.session(database=db) as s:
        return list(s.run(cypher, **params))

BATCH_PROJECTS = {
    15: ['p_55_great_suffolk_street_london','p_association_house_groeditz','p_association_house_plauen','p_awm_muenster_circular_office','p_bedzed_london_hackbridge'],
    16: ['p_bestandshalle_crclr_house','p_elementa_walkeweg_basel','p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal','p_hobelwerk_haus_d_oberwinterthur','p_lysp8_basel_lysbuechelareal'],
    17: ['p_boell_lab_berlin','p_crclr_house_berlin_overview','p_da_vinci_business_district_evere','p_lysbuechel_parkhaus_basel','p_reusebox_heilbronn'],
    18: ['p_be_ware_reallabor_berlin','p_bizh_reallabor_berlin','p_kindl_areal_berlin','p_opalis_plattformfall'],
    19: ['p_areal_walkeweg_nord_basel','p_haus_der_materialisierung_berlin','p_kunst_stoffe_berlin','p_preuse_interreg_nwe'],
}

SEP  = '=' * 70
SEP2 = '-' * 70

for batch_num, project_ids in BATCH_PROJECTS.items():
    print(f'\n{SEP}')
    print(f'  BATCH {batch_num:03d}  ({len(project_ids)} projects)')
    print(SEP)

    for pid in project_ids:
        # ── Project node ──────────────────────────────────────────────────
        rows = q('MATCH (p:Projekt {id:$id}) RETURN p', id=pid)
        if not rows:
            print(f'\n  [{pid}]  *** NOT IN DATABASE ***')
            continue

        p = dict(rows[0]['p'])
        print(f'\n  {SEP2}')
        name   = p.get('name', pid)
        bew    = p.get('bewertung', '?')
        status = p.get('projektstatus_text', '?')
        stadt  = p.get('stadt', '')
        land   = p.get('land', '')
        flaeche = p.get('flaeche_m2', '')
        jahr   = p.get('jahr_fertigstellung', p.get('fertigstellung_jahr', ''))
        note   = p.get('note', '')
        print(f'  {name}')
        print(f'  id={pid}  bew={bew}  status={status}')
        if flaeche: print(f'  Flaeche: {flaeche} m²')
        if jahr:    print(f'  Fertigstellung: {jahr}')
        if note:    print(f'  Note: {note[:200]}')

        # ── Location ──────────────────────────────────────────────────────
        loc = q('''
            MATCH (p:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)-[:EINGEBAUT_IN]->(bw:Bauwerk)-[:LIEGT_IN_STADT]->(s:Stadt)-[:LIEGT_IN_LAND]->(l:Land)
            RETURN DISTINCT s.name AS stadt, l.name AS land LIMIT 3
        ''', id=pid)
        if not loc:
            loc = q('''
                MATCH (p:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(bg)-[:EINGEBAUT_IN]->(bw:Bauwerk)-[:LIEGT_IN_STADT]->(s:Stadt)
                RETURN DISTINCT s.name AS stadt, null AS land LIMIT 3
            ''', id=pid)
        if loc:
            places = ', '.join(f"{r['stadt']}" + (f" ({r['land']})" if r.get('land') else '') for r in loc)
            print(f'  Ort: {places}')

        # ── Actors ────────────────────────────────────────────────────────
        actors = q('''
            MATCH (a:Akteur)-[:BETEILIGT_AN]->(p:Projekt {id:$id})
            OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(ar:Akteurrolle)
            OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(at:Akteurtyp)
            RETURN a.name AS name, collect(DISTINCT ar.name) AS rollen, at.name AS typ
            ORDER BY a.name
        ''', id=pid)
        if actors:
            print(f'  Akteure ({len(actors)}):')
            for a in actors:
                rollen = ', '.join(r for r in a['rollen'] if r)
                print(f'    • {a["name"]:<40}  [{rollen}]')

        # ── Bauteilgruppen ────────────────────────────────────────────────
        bgs = q('''
            MATCH (p:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
            OPTIONAL MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
            OPTIONAL MATCH (bg)-[:HAT_WIEDERVERWENDUNGSART]->(wva:WiederverwendungsArt)
            OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(mat:Material)
            OPTIONAL MATCH (bg)-[:EINGEBAUT_IN]->(bw:Bauwerk)
            OPTIONAL MATCH (bg)-[:AUS_BAUWERK]->(donor:Bauwerk)
            OPTIONAL MATCH (bg)-[:HAT_STATUS]->(st:Status)
            RETURN bg.name AS name,
                   collect(DISTINCT bt.name)  AS typen,
                   collect(DISTINCT wva.name) AS wva,
                   collect(DISTINCT mat.name) AS materialien,
                   bw.name  AS eingebaut_in,
                   donor.name AS aus_bauwerk,
                   st.name  AS status
            ORDER BY bg.name
        ''', id=pid)
        if bgs:
            print(f'  Bauteilgruppen ({len(bgs)}):')
            for bg in bgs:
                typen = ', '.join(t for t in bg['typen'] if t)
                wva   = ', '.join(w for w in bg['wva'] if w)
                mats  = ', '.join(m for m in bg['materialien'] if m)
                donor = f'  aus: {bg["aus_bauwerk"]}' if bg.get('aus_bauwerk') else ''
                einb  = f'  →: {bg["eingebaut_in"]}'  if bg.get('eingebaut_in')  else ''
                stat  = f'  [{bg["status"]}]'          if bg.get('status')        else ''
                print(f'    • {bg["name"]:<45} {typen}')
                if wva:   print(f'      Reuse-Art: {wva}')
                if mats:  print(f'      Material:  {mats}')
                if donor or einb: print(f'     {donor}{einb}{stat}')
        else:
            print(f'  Bauteilgruppen: keine')

        # ── Hürden ────────────────────────────────────────────────────────
        hurden = q('''
            MATCH (p:Projekt {id:$id})-[:HAT_HUERDE]->(h:Huerde)
            OPTIONAL MATCH (h)-[:HAT_HUERDEKATEGORIE]->(hk:HuerdeKategorie)
            RETURN h.name AS name, hk.name AS kat
            ORDER BY h.name LIMIT 8
        ''', id=pid)
        if hurden:
            print(f'  Hürden ({len(hurden)}):')
            for h in hurden:
                kat = f' [{h["kat"]}]' if h.get('kat') else ''
                print(f'    • {h["name"]}{kat}')

        # ── Quellen ───────────────────────────────────────────────────────
        quellen = q('''
            MATCH (n)-[:BELEGT_IN]->(q:Quelle)
            WHERE (n:Projekt AND n.id=$id)
               OR (:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(n)
            RETURN DISTINCT q.name AS qname, q.quelltyp AS typ
            ORDER BY qname LIMIT 6
        ''', id=pid)
        if quellen:
            print(f'  Quellen: {", ".join(q["qname"] for q in quellen)}')

        # ── Reuse-Kette ───────────────────────────────────────────────────
        kette = q('''
            MATCH (p:Projekt {id:$id})-[:HAT_BAUTEILGRUPPE]->(bg)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette)
            RETURN DISTINCT k.name AS name LIMIT 5
        ''', id=pid)
        if kette:
            print(f'  Reuse-Ketten: {", ".join(r["name"] for r in kette)}')

        # ── Programm ─────────────────────────────────────────────────────
        prog = q('''
            MATCH (p:Projekt {id:$id})-[:TEIL_VON_PROGRAMM]->(pr:Programm)
            RETURN pr.name AS name
        ''', id=pid)
        if prog:
            print(f'  Programm: {", ".join(r["name"] for r in prog)}')

print(f'\n{SEP}')
driver.close()
