"""Export the complete Bauteilbörse network as a single JSON.

Scope:
  - Layer 1: all Bauteilbörse anchors (Akteurtyp = Materialhub_Bauteilboerse)
  - Layer 2: all 1-hop neighbours in any direction (Akteurtyp, Akteurrolle,
            Geschaeftsmodell, Marktmodell, Methode, Land, Material,
            Bauteiltyp, Quelle, connected Akteur/Software, Projekt,
            Programm, Bauteilgruppe, OntologyAnchor, DataIssue, Tool, etc.)
  - Layer 3: 2-hop neighbours via Projekt/Bauteilgruppe to pull in
            Schadstoff, Huerde, Kennwert, Bauwerk, Stadt,
            WiederverwendungsArt, MatchingQualitaet, Nutzung,
            Ressourcenquelle, Logistik, Beschaffungsweg, Wirtschaft,
            BauaufgabeIntervention, ...

Output format: nodetypes / nodes / edgetypes / edges, with full properties.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
from collections import Counter, defaultdict
from neo4j import GraphDatabase

URI      = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687").strip()
USER     = os.environ.get("NEO4J_USER", "neo4j").strip()
DATABASE = os.environ.get("NEO4J_DATABASE", "mit-bestand").strip()
PWPATH   = Path(".neo4j_password")
OUT      = Path("_neo4j/exports/bauteilboerse_network_2026-06-02.json")


def to_jsonable(v):
    if v is None: return None
    if isinstance(v, (str, int, float, bool)): return v
    if isinstance(v, (list, tuple)): return [to_jsonable(x) for x in v]
    if hasattr(v, "iso_format"): return v.iso_format()
    return str(v)


def main():
    pw = PWPATH.read_text(encoding="utf-8").strip()
    driver = GraphDatabase.driver(URI, auth=(USER, pw))
    nodes_by_eid: dict[str, dict] = {}
    edges_by_eid: dict[str, dict] = {}

    with driver.session(database=DATABASE) as s:
        # ---------- Anchor IDs ----------
        # A Bauteilbörse anchor = actor TYPED as Materialhub_Bauteilboerse.
        # (Previously "any HAT_GESCHAEFTSMODELL holder", which over-counted
        #  directories/SaaS/suppliers that merely carry a business model — see
        #  _neo4j/review/2026-06-04_bauteilboerse_reclass/actor_profiles.md)
        anchor_eids = [r["eid"] for r in s.run(
            "MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(:Akteurtyp {name:'Materialhub_Bauteilboerse'}) "
            "RETURN DISTINCT elementId(a) AS eid")]
        print(f"Anchors: {len(anchor_eids)}")

        # ---------- 1-hop pull (any direction) ----------
        print("Pulling 1-hop direct neighbours and edges...")
        q1 = """
        UNWIND $eids AS eid
        MATCH (a) WHERE elementId(a) = eid
        OPTIONAL MATCH (a)-[r1]->(t1)
        WITH a, collect(DISTINCT {r: r1, n: t1}) AS out_neigh
        OPTIONAL MATCH (s2)-[r2]->(a)
        WITH a, out_neigh, collect(DISTINCT {r: r2, n: s2}) AS in_neigh
        RETURN a AS anchor, out_neigh, in_neigh
        """
        for record in s.run(q1, eids=anchor_eids):
            for n in [record["anchor"]]:
                if n is not None:
                    nid = n.element_id
                    nodes_by_eid[nid] = {
                        "elementId": nid,
                        "labels":    list(n.labels),
                        "properties": {k: to_jsonable(v) for k, v in dict(n).items()},
                    }
            for side, edge_list in (("out", record["out_neigh"]), ("in", record["in_neigh"])):
                for item in edge_list:
                    r = item["r"]; n2 = item["n"]
                    if r is None or n2 is None: continue
                    eid_r = r.element_id
                    edges_by_eid[eid_r] = {
                        "elementId":   eid_r,
                        "type":        r.type,
                        "source":      r.start_node.element_id,
                        "target":      r.end_node.element_id,
                        "properties":  {k: to_jsonable(v) for k, v in dict(r).items()},
                    }
                    nid2 = n2.element_id
                    if nid2 not in nodes_by_eid:
                        nodes_by_eid[nid2] = {
                            "elementId": nid2,
                            "labels": list(n2.labels),
                            "properties": {k: to_jsonable(v) for k, v in dict(n2).items()},
                        }
        print(f"  after 1-hop: {len(nodes_by_eid)} nodes / {len(edges_by_eid)} edges")

        # ---------- 2-hop via Projekt + Bauteilgruppe ----------
        # Picks up Schadstoff, Huerde, Kennwert, Bauwerk, Stadt, etc.
        print("Pulling 2-hop via Projekt / Bauteilgruppe / connected Akteur...")
        q2 = """
        UNWIND $eids AS eid
        MATCH (a) WHERE elementId(a) = eid
        OPTIONAL MATCH (a)-[:BETEILIGT_AN|NUTZT_SOFTWARE|BETRIEBEN_VON|VERBUNDEN_MIT_AKTEUR]->(mid)
        WHERE mid:Projekt OR mid:Programm OR mid:Bauteilgruppe OR mid:Akteur OR mid:Software OR mid:Bauwerk
        OPTIONAL MATCH (mid)-[r3]->(t3)
        RETURN mid, r3, t3 LIMIT 100000
        """
        added_n = added_e = 0
        for record in s.run(q2, eids=anchor_eids):
            for n in (record["mid"], record["t3"]):
                if n is None: continue
                nid = n.element_id
                if nid in nodes_by_eid: continue
                nodes_by_eid[nid] = {
                    "elementId": nid,
                    "labels": list(n.labels),
                    "properties": {k: to_jsonable(v) for k, v in dict(n).items()},
                }
                added_n += 1
            r = record["r3"]
            if r is None: continue
            eid_r = r.element_id
            if eid_r in edges_by_eid: continue
            edges_by_eid[eid_r] = {
                "elementId": eid_r,
                "type": r.type,
                "source": r.start_node.element_id,
                "target": r.end_node.element_id,
                "properties": {k: to_jsonable(v) for k, v in dict(r).items()},
            }
            added_e += 1
        print(f"  +{added_n} nodes / +{added_e} edges (2-hop expansion)")

        # ---------- explicit Schadstoff pickup via Bauwerk / Bauteilgruppe ----------
        # Schadstoff often hangs off Bauwerk or Bauteilgruppe via HAS_RISK_POLLUTANT
        print("Explicit Schadstoff sweep...")
        bauwerk_eids = [n["elementId"] for n in nodes_by_eid.values() if "Bauwerk" in n["labels"]]
        bg_eids      = [n["elementId"] for n in nodes_by_eid.values() if "Bauteilgruppe" in n["labels"]]
        proj_eids    = [n["elementId"] for n in nodes_by_eid.values() if "Projekt" in n["labels"]]
        all_mid_eids = list(set(bauwerk_eids + bg_eids + proj_eids))
        added_n2 = added_e2 = 0
        if all_mid_eids:
            for record in s.run("""
                UNWIND $eids AS eid
                MATCH (mid) WHERE elementId(mid) = eid
                OPTIONAL MATCH (mid)-[r]->(t)
                WHERE t:Schadstoff
                RETURN mid, r, t
            """, eids=all_mid_eids):
                t = record["t"]; r = record["r"]
                if t is None: continue
                nid = t.element_id
                if nid not in nodes_by_eid:
                    nodes_by_eid[nid] = {
                        "elementId": nid, "labels": list(t.labels),
                        "properties": {k: to_jsonable(v) for k, v in dict(t).items()},
                    }
                    added_n2 += 1
                if r is not None and r.element_id not in edges_by_eid:
                    edges_by_eid[r.element_id] = {
                        "elementId": r.element_id, "type": r.type,
                        "source": r.start_node.element_id, "target": r.end_node.element_id,
                        "properties": {k: to_jsonable(v) for k, v in dict(r).items()},
                    }
                    added_e2 += 1
        print(f"  +{added_n2} Schadstoff nodes / +{added_e2} edges")

        # ---------- internal edges between collected nodes ----------
        # We've already pulled outgoing from anchors and 2-hop via Projekt.
        # Now also pull edges *between* already-collected nodes to densify the subgraph.
        print("Densifying: edges between collected nodes...")
        all_eids = list(nodes_by_eid.keys())
        added_e3 = 0
        # Batched to avoid mega-query
        BATCH = 500
        for i in range(0, len(all_eids), BATCH):
            chunk = all_eids[i:i+BATCH]
            for record in s.run("""
                UNWIND $eids AS eid
                MATCH (a) WHERE elementId(a) = eid
                MATCH (a)-[r]->(b)
                WHERE elementId(b) IN $all_eids
                RETURN r LIMIT 200000
            """, eids=chunk, all_eids=all_eids):
                r = record["r"]
                if r is None or r.element_id in edges_by_eid: continue
                edges_by_eid[r.element_id] = {
                    "elementId": r.element_id, "type": r.type,
                    "source": r.start_node.element_id, "target": r.end_node.element_id,
                    "properties": {k: to_jsonable(v) for k, v in dict(r).items()},
                }
                added_e3 += 1
        print(f"  +{added_e3} internal edges (densified)")

    driver.close()

    # ---------- aggregate counts for nodetypes / edgetypes ----------
    nt_counter: Counter = Counter()
    nt_descriptions = {
        "Akteur": "Operator / company (Bauteilbörse anchor or partner)",
        "Software": "Software product node (e.g. Restado)",
        "Geschaeftsmodell": "Business-model archetype (5 clusters)",
        "Marktmodell": "Transaction-type vocabulary",
        "Akteurtyp": "Actor-type vocabulary",
        "Akteurrolle": "Functional-role vocabulary",
        "Methode": "Method vocabulary (urban mining, audit, ...)",
        "Material": "Closed-set material vocabulary (mat_*)",
        "Bauteiltyp": "Closed-set component vocabulary (bt_*)",
        "Land": "Country vocabulary",
        "Stadt": "City vocabulary",
        "Quelle": "Evidence-URL / source node",
        "ExternalLink": "Sub-label of Quelle for web URLs",
        "ResearchDocument": "Sub-label of Quelle for research files",
        "Dossier": "Sub-label of Quelle for dossier files",
        "SectionRef": "Sub-label of Quelle for section references",
        "OntologyAnchor": "Semantic anchor for cross-pass joining",
        "DataIssue": "Quality-issue node (provenance)",
        "Projekt": "Reuse project anchor",
        "Programm": "Programme (e.g. funding scheme)",
        "Bauteilgruppe": "Component group (project-side)",
        "Bauwerk": "Building/structure participating in reuse",
        "Schadstoff": "Pollutant / hazardous-substance vocabulary",
        "Huerde": "Hurdle / barrier vocabulary",
        "Kennwert": "Indicator/KPI vocabulary",
        "WiederverwendungsArt": "Reuse-type vocabulary",
        "MatchingQualitaet": "Match-quality grade",
        "Nutzung": "Use/occupation vocabulary",
        "Ressourcenquelle": "Resource-source vocabulary",
        "Logistik": "Logistic-pattern vocabulary",
        "Beschaffungsweg": "Procurement-route vocabulary",
        "Wirtschaft": "Economic-aspect vocabulary",
        "BauaufgabeIntervention": "Construction-task vocabulary",
        "Tool": "Tooling/equipment vocabulary",
    }
    for n in nodes_by_eid.values():
        for lbl in n["labels"]:
            nt_counter[lbl] += 1

    et_counter: Counter = Counter()
    et_endpoints: dict[str, dict] = defaultdict(lambda: {"from_labels": set(), "to_labels": set()})
    for e in edges_by_eid.values():
        et_counter[e["type"]] += 1
        s_lbls = tuple(nodes_by_eid[e["source"]]["labels"]) if e["source"] in nodes_by_eid else ()
        t_lbls = tuple(nodes_by_eid[e["target"]]["labels"]) if e["target"] in nodes_by_eid else ()
        et_endpoints[e["type"]]["from_labels"].update(s_lbls)
        et_endpoints[e["type"]]["to_labels"].update(t_lbls)

    # ---------- final document ----------
    doc = {
        "metadata": {
            "generated_at_utc": datetime.now(timezone.utc).isoformat(),
            "database": DATABASE,
            "scope": "Bauteilbörse subgraph + all 1-hop neighbours + 2-hop via Projekt/Bauteilgruppe/Bauwerk for Schadstoff/Huerde/Kennwert/etc.",
            "anchor_count": len(anchor_eids),
            "node_count":   len(nodes_by_eid),
            "edge_count":   len(edges_by_eid),
        },
        "nodetypes": [
            {"label": lbl, "count": cnt, "description": nt_descriptions.get(lbl, "")}
            for lbl, cnt in sorted(nt_counter.items(), key=lambda kv: (-kv[1], kv[0]))
        ],
        "edgetypes": [
            {
                "type": t,
                "count": et_counter[t],
                "from_labels": sorted(et_endpoints[t]["from_labels"]),
                "to_labels":   sorted(et_endpoints[t]["to_labels"]),
            }
            for t in sorted(et_counter.keys(), key=lambda k: (-et_counter[k], k))
        ],
        "nodes": sorted(
            list(nodes_by_eid.values()),
            key=lambda n: (n["labels"][0] if n["labels"] else "", n["properties"].get("id") or n["elementId"]),
        ),
        "edges": sorted(
            list(edges_by_eid.values()),
            key=lambda e: (e["type"], e["source"], e["target"]),
        ),
    }

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    size_mb = OUT.stat().st_size / (1024 * 1024)
    print(f"\nWritten {OUT}")
    print(f"  size: {size_mb:.2f} MB")
    print(f"  nodes: {len(nodes_by_eid)}  edges: {len(edges_by_eid)}")
    print(f"  nodetypes: {len(nt_counter)}  edgetypes: {len(et_counter)}")
    print("\nTop nodetypes:")
    for lbl, n in nt_counter.most_common(10):
        print(f"    {lbl:25s} {n}")
    print("Top edgetypes:")
    for t, n in et_counter.most_common(10):
        print(f"    {t:25s} {n}")


if __name__ == "__main__":
    main()
