"""Check total degree + connection types for surface entities the user
wants to delete. Surface tool_retile (Careno), bw_granby_workshop_liverpool
(Granby donor), surface Akteure, surface Stadt + Methode."""
from __future__ import annotations
import os
from pathlib import Path
from neo4j import GraphDatabase  # type: ignore

PASSWORD = Path(".neo4j_password").read_text(encoding="utf-8").strip().splitlines()[0]
URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687")
DB = os.environ.get("NEO4J_DATABASE", "mit-bestand")

SURFACE_IDS = [
    # Careno surface
    "tool_retile", "brussels_capital_region", "bbri", "meth_wiederverwendungskriterien",
    # Eggshell surface
    "stadt_weil_am_rhein",
    # Granby surface
    "bw_granby_workshop_liverpool", "stadt_liverpool", "assemble", "granby_4_streets_clt",
    "granby_workshop_cic", "will_shannon", "lewis_jones",
    # Circle House surface
    "kasper_guldager_jensen",
    # OBK 27 surface
    "cyril_pressacco", "thibaut_barrault",
    # Up Sticks Dundee (user added 2026-05-31)
    "p_up_sticks_dundee",
]

driver = GraphDatabase.driver(URI, auth=("neo4j", PASSWORD))
with driver.session(database=DB, default_access_mode="READ") as sess:
    for nid in SURFACE_IDS:
        # Total degree + rel-type breakdown + reuse-entity-owner connections (excluding the projects being deleted)
        DELETED = ["p_circle_house","p_obk_27","p_careno_becircular","p_eggshell_pavilion",
                   "p_granby_workshop","p_up_sticks_dundee"]
        rows = list(sess.run(
            """
            MATCH (n {id:$id})-[r]-(other)
            RETURN type(r) AS rt, startNode(r).id = $id AS outbound,
                   labels(other) AS olabs, other.id AS oid, coalesce(other.name,'') AS oname,
                   other.id IN $deleted AS will_be_deleted
            """,
            id=nid, deleted=DELETED,
        ))
        labels = []
        info = sess.run("MATCH (n {id:$id}) RETURN labels(n) AS l, coalesce(n.name,'') AS n", id=nid).single()
        if info:
            labels = list(info["l"])
        print(f"\n== {nid} [{'+'.join(sorted(labels))}] :: {info['n'] if info else '(not found)'} (degree={len(rows)}) ==")
        # Group by direction+rel_type
        connections_after_delete: dict[str, list] = {}
        for r in rows:
            if r["will_be_deleted"]:
                continue  # this edge will disappear with the project anyway
            key = f"{'->' if r['outbound'] else '<-'} {r['rt']}"
            connections_after_delete.setdefault(key, []).append(
                f"{r['oid']} [{'+'.join(sorted(r['olabs']))}]"
            )
        if not connections_after_delete:
            print("  AFTER cascade: 0 remaining edges — safe to delete (will be orphan)")
        else:
            print("  AFTER cascade, remaining edges:")
            for k, v in connections_after_delete.items():
                print(f"    {k:30s} ({len(v)}):")
                for item in v[:5]:
                    print(f"        {item}")
                if len(v) > 5:
                    print(f"        ... +{len(v)-5} more")
driver.close()
