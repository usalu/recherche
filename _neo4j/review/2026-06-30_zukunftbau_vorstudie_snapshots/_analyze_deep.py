"""Deep analytical pass: topology, fingerprints, co-occurrence, flows, numeric ranges.

Writes deep_analysis_results.json.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

import networkx as nx
from neo4j import GraphDatabase

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

HERE = Path(__file__).resolve().parent


def rows(session, q):
    return [dict(r) for r in session.run(q)]


def describe(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    if not vals:
        return None
    return {
        "n": len(vals),
        "min": round(min(vals), 2),
        "median": round(st.median(vals), 2),
        "max": round(max(vals), 2),
        "mean": round(st.mean(vals), 2),
    }


def main() -> None:
    uri, user, password, database = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    out: dict = {}
    with drv.session(database=database) as s:

        # ---------- 1. Actor network topology ----------
        edges = rows(s, """
            MATCH (a:Akteur)-[:VERBUNDEN_MIT_AKTEUR]-(b:Akteur)
            WITH a, b WHERE a.id < b.id
            OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(la:Land)
            OPTIONAL MATCH (b)-[:LIEGT_IN_LAND]->(lb:Land)
            RETURN a.id AS a, a.name AS an, la.name AS al,
                   b.id AS b, b.name AS bn, lb.name AS bl
        """)
        G = nx.Graph()
        land = {}
        name = {}
        for e in edges:
            G.add_edge(e["a"], e["b"])
            land[e["a"]] = e["al"]; land[e["b"]] = e["bl"]
            name[e["a"]] = e["an"]; name[e["b"]] = e["bn"]
        comps = sorted(nx.connected_components(G), key=len, reverse=True)
        giant = G.subgraph(comps[0]).copy() if comps else nx.Graph()
        btw = nx.betweenness_centrality(G)
        top_btw = sorted(btw.items(), key=lambda kv: kv[1], reverse=True)[:12]
        artic = list(nx.articulation_points(giant)) if giant.number_of_nodes() else []
        deg = dict(G.degree())
        out["topology"] = {
            "nodes": G.number_of_nodes(),
            "edges": G.number_of_edges(),
            "components": len(comps),
            "component_sizes": [len(c) for c in comps[:10]],
            "giant_share": round(len(comps[0]) / G.number_of_nodes(), 3) if comps else 0,
            "giant_density": round(nx.density(giant), 4) if giant.number_of_nodes() else 0,
            "avg_degree": round(sum(deg.values()) / len(deg), 2) if deg else 0,
            "top_betweenness": [
                {"name": name.get(n, n), "land": land.get(n), "betweenness": round(v, 4),
                 "degree": deg.get(n, 0)} for n, v in top_btw],
            "articulation_points": [
                {"name": name.get(n, n), "land": land.get(n), "degree": deg.get(n, 0)}
                for n in sorted(artic, key=lambda n: deg.get(n, 0), reverse=True)[:12]],
            "articulation_count": len(artic),
        }

        # ---------- 2. Cross-border collaboration (actor edges) ----------
        same = cross = unknown = 0
        cross_pairs = defaultdict(int)
        for e in edges:
            al, bl = e["al"], e["bl"]
            if not al or not bl:
                unknown += 1
            elif al == bl:
                same += 1
            else:
                cross += 1
                cross_pairs[tuple(sorted([al, bl]))] += 1
        out["actor_collab_geography"] = {
            "same_country": same, "cross_border": cross, "unknown": unknown,
            "top_cross_pairs": [
                {"laender": list(k), "verbindungen": v}
                for k, v in sorted(cross_pairs.items(), key=lambda kv: kv[1], reverse=True)[:10]],
        }

        # ---------- 3. Swiss bubble deep dive ----------
        ch_nodes = [n for n in G.nodes if land.get(n) == "Schweiz"]
        ch_sub = G.subgraph(ch_nodes).copy()
        ch_deg = dict(ch_sub.degree())
        out["swiss_bubble"] = {
            "akteure_im_netz": len(ch_nodes),
            "interne_kanten": ch_sub.number_of_edges(),
            "dichte": round(nx.density(ch_sub), 4) if ch_sub.number_of_nodes() else 0,
            "top_intern": [
                {"name": name.get(n, n), "intern_grad": d}
                for n, d in sorted(ch_deg.items(), key=lambda kv: kv[1], reverse=True)[:8]],
        }

        # ---------- 4. Component flows: cross-border vs local ----------
        flows = rows(s, """
            MATCH (sp:Bauwerk)<-[:AUS_SPENDER]-(bg:Bauteilgruppe)-[:IN_EMPFANGSOBJEKT]->(emp:Bauwerk)
            OPTIONAL MATCH (sp)-[:LIEGT_IN_LAND]->(spl:Land)
            OPTIONAL MATCH (emp)-[:LIEGT_IN_LAND]->(empl:Land)
            RETURN spl.name AS sp_land, empl.name AS emp_land, count(DISTINCT bg) AS bg
        """)
        f_same = f_cross = f_unknown = 0
        for r in flows:
            if not r["sp_land"] or not r["emp_land"]:
                f_unknown += r["bg"]
            elif r["sp_land"] == r["emp_land"]:
                f_same += r["bg"]
            else:
                f_cross += r["bg"]
        out["flow_geography"] = {
            "lokal_gleiches_land": f_same, "grenzueberschreitend": f_cross,
            "land_unbekannt": f_unknown,
            "detail": sorted(flows, key=lambda r: r["bg"], reverse=True)[:12],
        }
        trans = rows(s, """
            MATCH (k:Kennwert) WHERE toLower(k.kennwert) CONTAINS 'transport'
              AND k.einheit='km' AND k.wert IS NOT NULL
            RETURN k.wert AS wert
        """)
        out["transport_km"] = describe([r["wert"] for r in trans])

        # ---------- 5. Material -> Nachweis fingerprint ----------
        mn = rows(s, """
            MATCH (m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)-[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
            RETURN m.name AS material, nf.name AS nachweis, count(DISTINCT bg) AS bg
        """)
        mat_total = {r["material"]: r["n"] for r in rows(s, """
            MATCH (m:Material)<-[:NUTZT_MATERIAL]-(bg:Bauteilgruppe)
            WHERE (bg)-[:ERFORDERT_NACHWEIS]->()
            RETURN m.name AS material, count(DISTINCT bg) AS n
        """)}
        fp = defaultdict(list)
        for r in mn:
            fp[r["material"]].append((r["nachweis"], r["bg"]))
        fingerprint = {}
        for mat in ["Stahl", "Holz", "Glas", "Stahlbeton", "Beton", "Ziegel"]:
            tot = mat_total.get(mat, 0)
            items = sorted(fp.get(mat, []), key=lambda x: x[1], reverse=True)[:6]
            fingerprint[mat] = {
                "bauteilgruppen_mit_nachweis": tot,
                "top_nachweise": [
                    {"nachweis": nw, "bg": c, "anteil": round(c / tot, 2) if tot else 0}
                    for nw, c in items],
            }
        out["material_nachweis_fingerprint"] = fingerprint

        # ---------- 6. Nachweis co-occurrence bundles ----------
        out["nachweis_cooccurrence"] = rows(s, """
            MATCH (bg:Bauteilgruppe)-[:ERFORDERT_NACHWEIS]->(n1:Nachweisforderung)
            MATCH (bg)-[:ERFORDERT_NACHWEIS]->(n2:Nachweisforderung)
            WHERE n1.name < n2.name
            RETURN n1.name AS a, n2.name AS b, count(DISTINCT bg) AS gemeinsam
            ORDER BY gemeinsam DESC LIMIT 20
        """)

        # ---------- 7. Named Regelwerke (compliance KB seed) ----------
        out["named_regelwerke"] = rows(s, """
            MATCH (law) WHERE any(l IN labels(law) WHERE l ENDS WITH 'recht')
            WITH law, [l IN labels(law) WHERE l ENDS WITH 'recht'][0] AS domaene,
                 count { (law)<-[:GESTUETZT_AUF_REGELWERK]-() } AS incidence
            WHERE incidence > 0
            RETURN coalesce(law.name, law.id) AS regelwerk, domaene, incidence
            ORDER BY incidence DESC LIMIT 25
        """)

        # ---------- 8. Role value-chain ----------
        out["role_frequency"] = rows(s, """
            MATCH (a:Akteur)-[:HAT_AKTEURROLLE]->(r)
            RETURN r.name AS rolle, count(DISTINCT a) AS akteure ORDER BY akteure DESC
        """)
        out["full_stack_actors"] = rows(s, """
            MATCH (a:Akteur)
            WITH a, count { (a)-[:HAT_AKTEURROLLE]->() } AS rollen WHERE rollen >= 4
            RETURN a.name AS name, rollen ORDER BY rollen DESC LIMIT 15
        """)
        out["akteurtyp"] = rows(s, """
            MATCH (a:Akteur)-[:HAT_AKTEURTYP]->(t)
            RETURN t.name AS typ, count(*) AS n ORDER BY n DESC
        """)

        # ---------- 9. Temporal trend ----------
        yr = rows(s, """
            MATCH (p:Projekt) WHERE p.year_completed IS NOT NULL
            RETURN p.year_completed AS jahr, count(*) AS n ORDER BY jahr
        """)
        buckets = defaultdict(int)
        for r in yr:
            try:
                y = int(r["jahr"])
            except Exception:
                continue
            b = "vor 2010" if y < 2010 else ("2010-2014" if y < 2015 else
                ("2015-2019" if y < 2020 else "2020-2024" if y < 2025 else "2025+"))
            buckets[b] += r["n"]
        out["projekt_jahre"] = {"raw": yr, "buckets": dict(buckets)}

        # ---------- 10. Donor building typology ----------
        out["spender_typ"] = rows(s, """
            MATCH (b:Bauwerk)<-[:AUS_SPENDER]-(:Bauteilgruppe)
            WHERE b.bauobjektklasse IS NOT NULL
            RETURN b.bauobjektklasse AS klasse, count(DISTINCT b) AS bauwerke
            ORDER BY bauwerke DESC LIMIT 15
        """)

        # ---------- 11. Numeric performance ranges ----------
        co2_pct = rows(s, """
            MATCH (k:Kennwert)
            WHERE k.einheit='%' AND k.wert IS NOT NULL
              AND (toLower(k.kennwert) CONTAINS 'co2' OR toLower(k.kennwert) CONTAINS 'co₂'
                   OR toLower(k.kennwert) CONTAINS 'reduktion')
            RETURN k.wert AS wert
        """)
        reuse_pct = rows(s, """
            MATCH (k:Kennwert)
            WHERE k.category='reuse_share' AND k.einheit STARTS WITH '%' AND k.wert IS NOT NULL
              AND (toLower(k.kennwert) CONTAINS 'reuse' OR toLower(k.kennwert) CONTAINS 'reused'
                   OR toLower(k.kennwert) CONTAINS 'reclaim' OR toLower(k.kennwert) CONTAINS 'salvage'
                   OR toLower(k.kennwert) CONTAINS 'anteil' OR toLower(k.kennwert) CONTAINS 'réempl'
                   OR toLower(k.kennwert) CONTAINS 'circular')
            RETURN k.wert AS wert
        """)
        co2_t = rows(s, """
            MATCH (k:Kennwert)
            WHERE k.wert IS NOT NULL AND toLower(k.kennwert) STARTS WITH 'co2_einsparung_t'
            RETURN k.wert AS wert
        """)
        cost_eur = rows(s, """
            MATCH (k:Kennwert)
            WHERE k.category='cost' AND k.wert IS NOT NULL AND k.einheit IN ['EUR','€']
            RETURN k.wert AS wert
        """)
        out["performance_ranges"] = {
            "co2_reduktion_prozent": describe([r["wert"] for r in co2_pct]),
            "reuse_anteil_prozent": describe([r["wert"] for r in reuse_pct]),
            "co2_einsparung_tonnen": describe([r["wert"] for r in co2_t]),
            "kosten_eur": describe([r["wert"] for r in cost_eur]),
        }

    drv.close()
    (HERE / "deep_analysis_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    # console summary
    t = out["topology"]
    print(f"TOPOLOGY: {t['nodes']} nodes / {t['edges']} edges, {t['components']} components, "
          f"giant {t['giant_share']*100:.0f}% (density {t['giant_density']}), "
          f"{t['articulation_count']} articulation points")
    print("Top brokers (betweenness):")
    for b in t["top_betweenness"][:8]:
        print(f"   {b['name']} ({b['land']}) btw={b['betweenness']} deg={b['degree']}")
    print("Articulation points:", [a["name"] for a in t["articulation_points"][:8]])
    print("\nActor collab geo:", out["actor_collab_geography"]["same_country"], "same /",
          out["actor_collab_geography"]["cross_border"], "cross")
    print("Top cross pairs:", out["actor_collab_geography"]["top_cross_pairs"][:5])
    print("\nSwiss bubble:", out["swiss_bubble"]["akteure_im_netz"], "actors,",
          out["swiss_bubble"]["interne_kanten"], "internal edges, density",
          out["swiss_bubble"]["dichte"])
    print("\nFlow geo: local", out["flow_geography"]["lokal_gleiches_land"],
          "cross", out["flow_geography"]["grenzueberschreitend"],
          "unknown", out["flow_geography"]["land_unbekannt"])
    print("Transport km:", out["transport_km"])
    print("\nPerformance ranges:")
    for k, v in out["performance_ranges"].items():
        print(f"   {k}: {v}")
    print("\nNachweis co-occurrence top5:", out["nachweis_cooccurrence"][:5])
    print("\nFull-stack actors:", [(a["name"], a["rollen"]) for a in out["full_stack_actors"][:6]])
    print("Projekt buckets:", out["projekt_jahre"]["buckets"])
    print("Spender typ:", out["spender_typ"][:6])
    print("\nNamed Regelwerke top8:", [(r["regelwerk"], r["incidence"]) for r in out["named_regelwerke"][:8]])
    print("\nFingerprint Stahl:", out["material_nachweis_fingerprint"]["Stahl"])
    print("Fingerprint Holz:", out["material_nachweis_fingerprint"]["Holz"])
    print("\nWrote deep_analysis_results.json")


if __name__ == "__main__":
    main()
