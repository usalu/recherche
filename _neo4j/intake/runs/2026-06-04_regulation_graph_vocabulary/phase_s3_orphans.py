# coding: utf-8
"""S3 — merge duplicate actors; delete empty orphan project/programme stubs + unused vocab values."""
import sys
from neo4j import GraphDatabase
RUN="regulation_graph_vocab_2026_06_04"
S=GraphDatabase.driver("bolt://localhost:7687",auth=("neo4j","ENTWERFENMITBESTAND")).session(database="mit-bestand")
commit="--commit" in sys.argv
def cnt(q,**k): return S.run(q,**k).single()[0]

MERGES=[("werner_sobek_p","Werner_Sobek"),("gruner_reuse","gruner_reuse_platform")]  # (loser,keeper)
ORPHAN_DEL=["p_eth_circular_construction_student_reuse","p_rcmi_concular",
            "p_refair_bordeaux_reemploi_platform","p_fcrbe","p_eth_circular_construction_programme"]
VOCAB_DEL=["land_ukraine","land_italien","rq_leihgabe_oder_service","bt_fassadenelement_beton",
           "vt_mechanische_befestigung_unspezifiziert","vt_holzduebel","vt_modulare_fassadenkassette",
           "vt_verleimung","bsys_iw73","ar_brandschutz_barrierefreiheit","ar_stahlbau_fertigung"]

def merge_actor(loser,keeper,do):
    rels=list(S.run("MATCH (l {id:$l})-[r]-(o) RETURN startNode(r).id AS s, endNode(r).id AS e, type(r) AS t, properties(r) AS p",l=loser))
    if do:
        # union source arrays
        S.run("""MATCH (l {id:$l}),(k {id:$k})
                 SET k.source_urls=apoc.coll.toSet(coalesce(k.source_urls,[])+coalesce(l.source_urls,[]))""",l=loser,k=keeper) if False else None
        # manual union (no APOC dependency)
        lk=S.run("MATCH (l {id:$l}),(k {id:$k}) RETURN coalesce(l.source_urls,[]) AS lu, coalesce(k.source_urls,[]) AS ku",l=loser,k=keeper).single()
        union=list(dict.fromkeys(list(lk["ku"])+list(lk["lu"])))
        S.run("MATCH (k {id:$k}) SET k.source_urls=$u",k=keeper,u=union)
        for r in rels:
            other = r["e"] if r["s"]==loser else r["s"]
            if other==keeper: continue
            if r["s"]==loser:
                S.run(f"MATCH (k {{id:$k}}),(o {{id:$o}}) MERGE (k)-[nr:`{r['t']}`]->(o) SET nr+=$p",k=keeper,o=other,p={kk:vv for kk,vv in r['p'].items() if kk!='id'})
            else:
                S.run(f"MATCH (k {{id:$k}}),(o {{id:$o}}) MERGE (o)-[nr:`{r['t']}`]->(k) SET nr+=$p",k=keeper,o=other,p={kk:vv for kk,vv in r['p'].items() if kk!='id'})
        S.run("MATCH (l {id:$l}) DETACH DELETE l",l=loser)
    return len(rels)

print("=== S3 plan ===")
for l,k in MERGES: print(f"  merge {l} -> {k} (redirect {cnt('MATCH (l {id:$l})--() RETURN count(*)',l=l)} edges)")
print(f"  delete {len(ORPHAN_DEL)} orphan project/programme stubs, {len(VOCAB_DEL)} unused vocab values")
if commit:
    for l,k in MERGES: merge_actor(l,k,True)
    S.run("MATCH (n) WHERE n.id IN $ids DETACH DELETE n",ids=ORPHAN_DEL+VOCAB_DEL)
    print("\nCOMMITTED.")
    print("  duplicate actor names left:",cnt("MATCH (a:Akteur) WITH coalesce(a.name,a.id) AS nm,count(*) AS c WHERE c>1 RETURN count(*)"))
    print("  orphan nodes left:",cnt("MATCH (n) WHERE NOT (n)--() RETURN count(n)"))
    print("  totals:",cnt("MATCH (n) RETURN count(n)"),"nodes,",cnt("MATCH ()-[r]->() RETURN count(r)"),"rels")
else:
    print("\nDRY-RUN (no writes).")
S.close()
