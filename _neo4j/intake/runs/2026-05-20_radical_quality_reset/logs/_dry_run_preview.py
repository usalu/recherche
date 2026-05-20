"""Read-only dry-run preview of phase 1.1 demote query."""
import sys
sys.path.insert(0, r"E:/recherche/_scripts")
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

DEMOTABLE_TYPES = (
    "HAT_STATUS",
    "HAT_WIEDERVERWENDUNGSART",
    "HAT_HUERDE",
    "HAT_LOGISTIK",
    "HAT_PROZESSPHASE",
    "HAT_METHODE",
)

uri, user, pw, _ = resolve_connection()
drv = GraphDatabase.driver(uri, auth=(user, pw))
with drv.session(database="mit-bestand") as s:
    print("=== fan-out of bg x payload across unwired chains ===")
    rows = list(
        s.run(
            "MATCH (bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette) "
            "WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}) "
            "MATCH (k)-[r]->(target) "
            "WHERE type(r) IN $types "
            "RETURN type(r) AS t, count(*) AS n ORDER BY n DESC",
            types=list(DEMOTABLE_TYPES),
        )
    )
    total = 0
    for r in rows:
        print(f"  {r['t']}: {r['n']}")
        total += r['n']
    print(f"  TOTAL fan-out (pre-merge): {total}")

    print()
    print("=== distinct (bg, type, target) tuples (post-merge upper bound) ===")
    r = s.run(
        "MATCH (bg:Bauteilgruppe)-[:TEIL_VON_KETTE]->(k:Wiederverwendungskette) "
        "WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}) "
        "MATCH (k)-[r]->(target) "
        "WHERE type(r) IN $types "
        "RETURN count(DISTINCT [id(bg), type(r), id(target)]) AS distinct_combos, "
        "       count(DISTINCT [id(bg), type(r), id(target), k.id]) AS distinct_with_source",
        types=list(DEMOTABLE_TYPES),
    ).single()
    print(f"  distinct (bg, type, target): {r['distinct_combos']}")
    print(f"  distinct (bg, type, target, source_id): {r['distinct_with_source']}")

    print()
    print("=== sample 5 unwired chains and their payload ===")
    rows = list(
        s.run(
            "MATCH (k:Wiederverwendungskette) "
            "WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}) "
            "OPTIONAL MATCH (k)-[r]->(t) WHERE type(r) IN $types "
            "WITH k, collect(type(r)+'->'+coalesce(t.id, t.name, '?')) AS payload "
            "RETURN k.id AS chain_id, payload "
            "ORDER BY size(payload) DESC LIMIT 5",
            types=list(DEMOTABLE_TYPES),
        )
    )
    for r in rows:
        print(f"  {r['chain_id']}: {r['payload']}")

    print()
    print("=== unwired chains: incoming AUS_BAUWERK/EINGEBAUT_IN counts ===")
    r = s.run(
        "MATCH (k:Wiederverwendungskette) "
        "WHERE NOT (exists{(k)-[:AUS_BAUWERK]->()} AND exists{(k)-[:EINGEBAUT_IN]->()}) "
        "OPTIONAL MATCH (s_ab)-[:AUS_BAUWERK]->(k) "
        "WITH k, count(DISTINCT s_ab) AS in_ab "
        "OPTIONAL MATCH (s_ei)-[:EINGEBAUT_IN]->(k) "
        "RETURN sum(in_ab) AS in_ab_total, count(DISTINCT s_ei) AS in_ei_distinct"
    ).single()
    print(f"  incoming AUS_BAUWERK total: {r['in_ab_total']}")
    print(f"  incoming EINGEBAUT_IN distinct sources: {r['in_ei_distinct']}")
drv.close()
