"""Drill into one Projekt end-to-end to design the detail page."""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parents[1]
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402


def heading(t: str) -> None:
    print()
    print("=" * 72)
    print(t)
    print("=" * 72)


def main(pid: str = "p_jeugdkliniek_ithaka") -> None:
    uri, user, pw, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pw))
    with driver.session(database=db) as s:

        heading(f"[A] Node properties — {pid}")
        r = s.run("MATCH (p:Projekt {id:$pid}) RETURN p", pid=pid).single()
        if not r:
            print(f"Project '{pid}' not found.")
            return
        node = dict(r["p"])
        for k in sorted(node):
            v = node[k]
            sv = str(v)
            print(f"  {k:>35s}: {sv[:80]}{'…' if len(sv) > 80 else ''}")

        heading("[B] Country / city / programme / intervention / reuse-type / status")
        for label, q in [
            ("LIEGT_IN_LAND", "MATCH (p:Projekt {id:$pid})-[:LIEGT_IN_LAND]->(n) RETURN n.name AS x"),
            ("LIEGT_IN_STADT", "MATCH (p:Projekt {id:$pid})-[:LIEGT_IN_STADT]->(n) RETURN n.name AS x"),
            ("TEIL_VON_PROGRAMM", "MATCH (p:Projekt {id:$pid})-[:TEIL_VON_PROGRAMM]->(n) RETURN n.name AS x"),
            ("HAT_INTERVENTION", "MATCH (p:Projekt {id:$pid})-[:HAT_INTERVENTION]->(n) RETURN n.name AS x"),
            ("HAT_WIEDERVERWENDUNGSART", "MATCH (p:Projekt {id:$pid})-[:HAT_WIEDERVERWENDUNGSART]->(n) RETURN n.name AS x"),
            ("HAT_STATUS", "MATCH (p:Projekt {id:$pid})-[:HAT_STATUS]->(n) RETURN n.name AS x"),
            ("HAT_NUTZUNG", "MATCH (p:Projekt {id:$pid})-[:HAT_NUTZUNG]->(n) RETURN n.name AS x"),
            ("HAT_METHODE", "MATCH (p:Projekt {id:$pid})-[:HAT_METHODE]->(n) RETURN n.name AS x"),
            ("NUTZT_BAUWERK", "MATCH (p:Projekt {id:$pid})-[:NUTZT_BAUWERK]->(n) RETURN n.name AS x, n.id AS i"),
            ("HAT_HUERDE", "MATCH (p:Projekt {id:$pid})-[:HAT_HUERDE]->(n) RETURN n.name AS x"),
        ]:
            rows = s.run(q, pid=pid).data()
            vals = ", ".join(str(r.get("x") or r.get("i") or "") for r in rows)
            print(f"  {label:>25s}: {vals or '<none>'}")

        heading("[C] Bauteilgruppe — the reused components")
        rows = s.run(
            "MATCH (p:Projekt {id:$pid})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(m:Material) "
            "OPTIONAL MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp) "
            "OPTIONAL MATCH (bg)-[:HAT_STATUS]->(st:Status) "
            "OPTIONAL MATCH (bg)-[:HAT_WIEDERVERWENDUNGSART]->(w:WiederverwendungsArt) "
            "OPTIONAL MATCH (bg)-[:FROM_DONOR]->(d:Bauwerk) "
            "RETURN bg.id AS id, bg.name AS name, "
            "  collect(DISTINCT m.name) AS materials, "
            "  collect(DISTINCT bt.name) AS bauteiltypen, "
            "  collect(DISTINCT st.name) AS statuses, "
            "  collect(DISTINCT w.name) AS reuse_types, "
            "  collect(DISTINCT d.name) AS donors",
            pid=pid,
        ).data()
        for x in rows:
            print(f"  • {x['name'][:55]:<55s}")
            print(f"      mat={x['materials']} | type={x['bauteiltypen']}")
            print(f"      status={x['statuses']} | reuse={x['reuse_types']}")
            print(f"      donor(s)={x['donors']}")

        heading("[D] Actor ecosystem")
        rows = s.run(
            "MATCH (p:Projekt {id:$pid})<-[:BETEILIGT_AN]-(a:Akteur) "
            "OPTIONAL MATCH (a)-[:HAT_AKTEURROLLE]->(r:Akteurrolle) "
            "OPTIONAL MATCH (a)-[:HAT_AKTEURTYP]->(t:Akteurtyp) "
            "RETURN a.name AS actor, collect(DISTINCT r.name) AS roles, "
            "       collect(DISTINCT t.name) AS types "
            "ORDER BY actor",
            pid=pid,
        ).data()
        for x in rows:
            print(f"  • {x['actor'][:35]:<35s} | roles={x['roles']} | types={x['types']}")

        heading("[E] Kennwert (KPIs)")
        rows = s.run(
            "MATCH (p:Projekt {id:$pid})-[:HAT_KENNWERT]->(k:Kennwert) "
            "OPTIONAL MATCH (k)-[:BERECHNET_NACH_MODUL]->(m:LCAModule) "
            "RETURN k.kennwert AS metric, k.wert AS value, k.einheit AS unit, "
            "       k.method AS method, m.name AS lca_module",
            pid=pid,
        ).data()
        for x in rows:
            print(f"  • {str(x['metric'])[:35]:<35s} = {str(x['value'])[:20]:<20s} {str(x.get('unit') or ''):<10s} | method: {str(x['method'])[:40]}")
            if x.get("lca_module"):
                print(f"      LCA: {x['lca_module']}")

        heading("[F] Source evidence")
        rows = s.run(
            "MATCH (p:Projekt {id:$pid})-[:BELEGT_IN]->(q:Quelle) "
            "OPTIONAL MATCH (q)-[:HAS_SOURCE_LINK]->(el:ExternalLink) "
            "RETURN q.id AS qid, q.name AS qname, "
            "       collect(DISTINCT el.url)[..3] AS urls LIMIT 25",
            pid=pid,
        ).data()
        print(f"BELEGT_IN Quelle (max 25): {len(rows)} rows")
        for x in rows:
            urls = x.get("urls") or []
            url_short = urls[0][:60] if urls else "<no url>"
            print(f"  • {str(x['qname'])[:35]:<35s} → {url_short}")

        rows = s.run(
            "MATCH (p:Projekt {id:$pid})-[:BELEGT_IN]->(d:Dossier) "
            "RETURN d.id AS did, d.name AS dname",
            pid=pid,
        ).data()
        print(f"\nBELEGT_IN Dossier: {len(rows)} rows")
        for x in rows:
            print(f"  • {x.get('dname') or x.get('did')}")

        heading("[G] Data quality concerns")
        r = s.run(
            "MATCH (p:Projekt {id:$pid})-[:CONCERNS]-(di:DataIssue) "
            "RETURN di.severity AS sev, di.status AS st, count(*) AS n "
            "ORDER BY n DESC",
            pid=pid,
        ).data()
        for x in r:
            print(f"  sev={x['sev']:<10s} status={x['st']:<10s}: {x['n']}")


if __name__ == "__main__":
    pid = sys.argv[1] if len(sys.argv) > 1 else "p_jeugdkliniek_ithaka"
    main(pid)
