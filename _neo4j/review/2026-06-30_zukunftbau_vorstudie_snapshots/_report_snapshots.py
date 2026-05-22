"""Build the 8 core 'Vorstudie' snapshots for the Zukunft-Bau report.

For each snapshot we run a Cypher query, build a networkx graph with display
metadata, export the raw rows + graph as JSON, and render a German-captioned PNG.

Output: report_snapshots/<id>.json and report_snapshots/<id>.png
        report_snapshots/manifest.json
"""

from __future__ import annotations

import json
import math
import sys
from collections import Counter
from pathlib import Path
from typing import Any

import matplotlib

matplotlib.use("Agg")
import matplotlib.patches as mpatches  # noqa: E402
import matplotlib.pyplot as plt  # noqa: E402
import networkx as nx  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

HERE = Path(__file__).resolve().parent
OUT = HERE / "report_snapshots"
OUT.mkdir(exist_ok=True)

plt.rcParams["font.family"] = "DejaVu Sans"

PALETTE = {
    "Akteur": "#4C78A8",
    "Bauteilboerse": "#E45756",
    "Land": "#54A24B",
    "Projekt": "#F58518",
    "Bauteilgruppe": "#72B7B2",
    "Bauwerk": "#9D755D",
    "Spender": "#B279A2",
    "Empfaenger": "#54A24B",
    "Bauteiltyp": "#4C78A8",
    "Material": "#EECA3B",
    "Regulierungsfrage": "#F58518",
    "Nachweisforderung": "#E45756",
    "Regelwerk": "#72B7B2",
    "Huerde": "#E45756",
    "Rechtsdomaene": "#B279A2",
}

BOERSEN_IDS = {
    "concular", "madaster", "bauteilnetz_deutschland", "opalis", "cirkla",
    "software_restado", "restado",
}


def short(text: str | None, n: int = 26) -> str:
    if not text:
        return ""
    text = text.strip()
    return text if len(text) <= n else text[: n - 1] + "…"


def _palette(keys) -> dict[str, str]:
    base = ["#4C78A8", "#F58518", "#54A24B", "#B279A2", "#FF9DA6", "#9D755D",
            "#BAB0AC", "#E45756", "#72B7B2", "#EECA3B", "#1F77B4", "#AEC7E8",
            "#FFBB78", "#98DF8A", "#C5B0D5", "#C49C94", "#17BECF", "#7F7F7F"]
    return {k: base[i % len(base)] for i, k in enumerate(sorted(keys))}


# --------------------------------------------------------------------------- #


def build_a1(session):
    q = """
    MATCH (a:Akteur)-[:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
    OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(la:Land)
    OPTIONAL MATCH (b)-[:LIEGT_IN_LAND]->(lb:Land)
    RETURN a.id AS a_id, coalesce(a.name,a.id) AS a_name, la.name AS a_land,
           b.id AS b_id, coalesce(b.name,b.id) AS b_name, lb.name AS b_land
    """
    rows = [dict(r) for r in session.run(q)]
    G = nx.Graph()
    land_of = {}
    for r in rows:
        land_of[r["a_id"]] = r["a_land"]
        land_of[r["b_id"]] = r["b_land"]
        G.add_node(r["a_id"], name=r["a_name"], land=r["a_land"])
        G.add_node(r["b_id"], name=r["b_name"], land=r["b_land"])
        G.add_edge(r["a_id"], r["b_id"])
    lands = sorted({l for l in land_of.values() if l})
    lp = _palette(lands)
    for n, d in G.nodes(data=True):
        is_b = n in BOERSEN_IDS
        d["group"] = "Bauteilboerse" if is_b else "Akteur"
        d["color"] = "#E45756" if is_b else lp.get(d.get("land"), "#B0B0B0")
        d["label"] = d["name"] if (is_b or G.degree(n) >= 6) else ""
        d["size"] = 90 + 60 * G.degree(n)
    meta = {"layout": "spring",
            "legend": {f"Land: {l}": lp[l] for l in lands} | {"Bauteilbörse (Multiplikator)": "#E45756"},
            "stats": {"akteure": G.number_of_nodes(), "verbindungen": G.number_of_edges(), "laender": len(lands)}}
    return G, meta, rows


def build_a2(session):
    q = """
    MATCH (a:Akteur)-[:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
    OPTIONAL MATCH (a)-[:LIEGT_IN_LAND]->(la:Land)
    OPTIONAL MATCH (b)-[:LIEGT_IN_LAND]->(lb:Land)
    RETURN a.id AS a_id, coalesce(a.name,a.id) AS a_name, la.name AS a_land,
           b.id AS b_id, coalesce(b.name,b.id) AS b_name, lb.name AS b_land
    """
    rows = [dict(r) for r in session.run(q)]
    full = nx.Graph()
    name_of, land_of = {}, {}
    for r in rows:
        name_of[r["a_id"]] = r["a_name"]; name_of[r["b_id"]] = r["b_name"]
        land_of[r["a_id"]] = r["a_land"]; land_of[r["b_id"]] = r["b_land"]
        full.add_edge(r["a_id"], r["b_id"])
    deg = dict(full.degree())
    top = [n for n, _ in sorted(deg.items(), key=lambda x: -x[1])[:12]]
    topset = set(top)
    keep = set(top)
    for h in top:
        keep.update(full.neighbors(h))
    G = full.subgraph(keep).copy()
    lands = sorted({land_of.get(n) for n in G.nodes() if land_of.get(n)})
    lp = _palette(lands)
    for n, d in G.nodes(data=True):
        is_b = n in BOERSEN_IDS
        is_hub = n in topset
        d["name"] = name_of.get(n, n); d["land"] = land_of.get(n)
        d["group"] = "Bauteilboerse" if is_b else "Akteur"
        d["color"] = "#E45756" if is_b else lp.get(d["land"], "#B0B0B0")
        d["label"] = d["name"] if (is_hub or is_b) else ""
        d["size"] = 120 + 60 * deg[n]
    ranking = [{"akteur": name_of.get(n, n), "grad": deg[n], "boerse": n in BOERSEN_IDS} for n in top]
    meta = {"layout": "spring_wide",
            "legend": {f"Land: {l}": lp[l] for l in lands} | {"Bauteilbörse (Multiplikator)": "#E45756"},
            "stats": {"top_akteure": len(top), "knoten_im_teilnetz": G.number_of_nodes(), "ranking": ranking}}
    return G, meta, rows


def build_a3(session):
    q = """
    MATCH (a:Akteur)-[:LIEGT_IN_LAND]->(land:Land)
    RETURN a.id AS a_id, coalesce(a.name,a.id) AS a_name, land.name AS land
    """
    rows = [dict(r) for r in session.run(q)]
    counts = Counter(r["land"] for r in rows)
    G = nx.Graph()
    lands = sorted(counts)
    lp = _palette(lands)
    for land in lands:
        G.add_node(f"LAND::{land}", group="Land", label=f"{land}\n({counts[land]})",
                   color="#54A24B", size=600 + 120 * counts[land], is_land=True)
    for r in rows:
        nid = r["a_id"]; is_b = nid in BOERSEN_IDS
        G.add_node(nid, group="Bauteilboerse" if is_b else "Akteur",
                   label=r["a_name"] if is_b else "",
                   color="#E45756" if is_b else lp.get(r["land"], "#B0B0B0"),
                   size=170 if is_b else 28, is_land=False)
        G.add_edge(f"LAND::{r['land']}", nid)
    meta = {"layout": "radial_country",
            "legend": {"Land (Größe = Anzahl Akteure)": "#54A24B", "Bauteilbörse / Multiplikator": "#E45756", "Akteur": "#B0B0B0"},
            "stats": {"akteure": len({r["a_id"] for r in rows}), "laender": len(lands), "verteilung": dict(counts.most_common())}}
    return G, meta, rows


def build_b1(session):
    q = """
    MATCH (p:Projekt {id:'p_k118_kopfbau_halle_118_winterthur'})-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe)
    WHERE bg.alte_funktion IS NOT NULL
    OPTIONAL MATCH (bg)-[:AUS_SPENDER]->(sp:Bauwerk)
    OPTIONAL MATCH (bg)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
    OPTIONAL MATCH (bg)-[:NUTZT_MATERIAL]->(mat:Material)
    RETURN p.id AS p_id, coalesce(p.name,p.id) AS p_name,
           bg.id AS bg_id, coalesce(bg.name,bg.id) AS bg_name,
           bg.tragend AS tragend, sp.id AS sp_id, coalesce(sp.name,sp.id) AS sp_name,
           bt.name AS bauteiltyp, mat.name AS material
    """
    rows = [dict(r) for r in session.run(q)]
    G = nx.DiGraph()
    p_id = rows[0]["p_id"] if rows else "p_k118"
    p_name = rows[0]["p_name"] if rows else "K.118 Winterthur"
    G.add_node(p_id, group="Projekt", label=p_name, color=PALETTE["Projekt"], size=1700)
    for r in rows:
        bg = r["bg_id"]; lbl = short(r["bg_name"], 30)
        if r["tragend"]:
            lbl += " ⚙"
        G.add_node(bg, group="Bauteilgruppe", label=lbl, color=PALETTE["Bauteilgruppe"], size=750)
        G.add_edge(p_id, bg, rel="HAT_BAUTEILGRUPPE")
        if r["sp_id"]:
            G.add_node(r["sp_id"], group="Spender", label=short(r["sp_name"], 28), color=PALETTE["Spender"], size=520)
            G.add_edge(r["sp_id"], bg, rel="AUS_SPENDER")
        if r["bauteiltyp"]:
            tid = f"BT::{r['bauteiltyp']}"
            G.add_node(tid, group="Bauteiltyp", label=r["bauteiltyp"], color=PALETTE["Bauteiltyp"], size=400)
            G.add_edge(bg, tid, rel="HAT_BAUTEILTYP")
        if r["material"]:
            mid = f"MAT::{r['material']}"
            G.add_node(mid, group="Material", label=r["material"], color=PALETTE["Material"], size=400)
            G.add_edge(bg, mid, rel="NUTZT_MATERIAL")
    meta = {"layout": "spring",
            "legend": {"Projekt (Empfänger)": PALETTE["Projekt"], "Bauteilgruppe (⚙ = tragend)": PALETTE["Bauteilgruppe"],
                       "Spenderbauwerk": PALETTE["Spender"], "Bauteiltyp": PALETTE["Bauteiltyp"], "Material": PALETTE["Material"]},
            "stats": {"bauteilgruppen": len({r["bg_id"] for r in rows})}}
    return G, meta, rows


def build_b2(session):
    q = """
    MATCH (sp:Bauwerk)<-[:AUS_SPENDER]-(bg:Bauteilgruppe)-[:IN_EMPFANGSOBJEKT]->(emp:Bauwerk)
    OPTIONAL MATCH (sp)-[:LIEGT_IN_LAND]->(spl:Land)
    OPTIONAL MATCH (emp)-[:LIEGT_IN_LAND]->(empl:Land)
    RETURN sp.id AS sp_id, coalesce(sp.name,sp.id) AS sp_name, spl.name AS sp_land,
           emp.id AS emp_id, coalesce(emp.name,emp.id) AS emp_name, empl.name AS emp_land
    """
    rows = [dict(r) for r in session.run(q)]
    pair_count: Counter = Counter(); cross = {}; names = {}; lands = {}
    for r in rows:
        names[r["sp_id"]] = r["sp_name"]; names[r["emp_id"]] = r["emp_name"]
        lands[r["sp_id"]] = r["sp_land"]; lands[r["emp_id"]] = r["emp_land"]
        key = (r["sp_id"], r["emp_id"]); pair_count[key] += 1
        cross[key] = bool(r["sp_land"] and r["emp_land"] and r["sp_land"] != r["emp_land"])
    G = nx.DiGraph(); deg_in: Counter = Counter(); deg_out: Counter = Counter()
    cross_nodes = set()
    for (sp, emp) in pair_count:
        deg_out[sp] += 1; deg_in[emp] += 1
        if cross[(sp, emp)]:
            cross_nodes.add(sp); cross_nodes.add(emp)
    for nid, name in names.items():
        is_emp = deg_in[nid] >= deg_out[nid] and deg_in[nid] > 0
        tot = deg_in[nid] + deg_out[nid]
        show = tot >= 3 or nid in cross_nodes
        G.add_node(nid, group="Empfaenger" if is_emp else "Spender",
                   label=short(name, 22) if show else "", land=lands.get(nid),
                   color=PALETTE["Empfaenger"] if is_emp else PALETTE["Spender"], size=200 + 130 * tot)
    for (sp, emp), n in pair_count.items():
        G.add_edge(sp, emp, weight=n, cross=cross[(sp, emp)])
    meta = {"layout": "spring",
            "legend": {"Spenderbauwerk": PALETTE["Spender"], "Empfängerbauwerk": PALETTE["Empfaenger"], "länderübergreifender Fluss": "#D62728"},
            "stats": {"flussbeziehungen": len(pair_count), "bauteilgruppen_im_fluss": len(rows), "laenderuebergreifend": sum(1 for v in cross.values() if v)},
            "edge_cross_highlight": True}
    return G, meta, rows


def build_b3(session):
    q = """
    MATCH (bg:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp)
    MATCH (bg)-[:NUTZT_MATERIAL]->(mat:Material)
    RETURN bt.name AS typ, mat.name AS material, count(DISTINCT bg) AS n
    """
    rows = [dict(r) for r in session.run(q)]
    G = nx.Graph(); typ_tot: Counter = Counter(); mat_tot: Counter = Counter()
    for r in rows:
        typ_tot[r["typ"]] += r["n"]; mat_tot[r["material"]] += r["n"]
    for t, tot in typ_tot.items():
        G.add_node(f"T::{t}", group="Bauteiltyp", label=t, color=PALETTE["Bauteiltyp"], size=260 + 35 * tot, bipartite=0)
    for m, tot in mat_tot.items():
        G.add_node(f"M::{m}", group="Material", label=m, color=PALETTE["Material"], size=260 + 35 * tot, bipartite=1)
    for r in rows:
        G.add_edge(f"T::{r['typ']}", f"M::{r['material']}", weight=r["n"])
    meta = {"layout": "bipartite",
            "legend": {"Bauteiltyp": PALETTE["Bauteiltyp"], "Material": PALETTE["Material"]},
            "stats": {"bauteiltypen": len(typ_tot), "materialien": len(mat_tot), "kanten": len(rows)}}
    return G, meta, rows


def build_c1(session):
    q = """
    MATCH (law)-[:GILT_IN_LAND]->(land:Land)
    UNWIND [l IN labels(law) WHERE l ENDS WITH 'recht'] AS domain
    RETURN land.name AS land, domain AS domain, count(*) AS n
    """
    rows = [dict(r) for r in session.run(q)]
    G = nx.Graph(); land_tot: Counter = Counter(); dom_tot: Counter = Counter()
    for r in rows:
        land_tot[r["land"]] += r["n"]; dom_tot[r["domain"]] += r["n"]
    for land, tot in land_tot.items():
        G.add_node(f"L::{land}", group="Land", label=f"{land} ({tot})", color=PALETTE["Land"], size=350 + 50 * tot, bipartite=0)
    for dom, tot in dom_tot.items():
        G.add_node(f"D::{dom}", group="Rechtsdomaene", label=dom, color=PALETTE["Rechtsdomaene"], size=350 + 40 * tot, bipartite=1)
    for r in rows:
        G.add_edge(f"L::{r['land']}", f"D::{r['domain']}", weight=r["n"])
    meta = {"layout": "bipartite",
            "legend": {"Land": PALETTE["Land"], "Rechtsdomäne": PALETTE["Rechtsdomaene"]},
            "stats": {"laender": len(land_tot), "rechtsdomaenen": len(dom_tot), "normknoten_kanten": sum(r["n"] for r in rows)}}
    return G, meta, rows


def build_c2(session):
    # One reused steel beam group -> question -> proof -> law DOMAIN (aggregated) -> country
    q = """
    MATCH (bg:Bauteilgruppe {id:'bg_stahl_mehrere_k118_structure'})
    MATCH (bg)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf:Regulierungsfrage)
    OPTIONAL MATCH (rf)-[:ERFORDERT_NACHWEIS]->(nf:Nachweisforderung)
    OPTIONAL MATCH (nf)-[:GESTUETZT_AUF_REGELWERK]->(law)
          WHERE any(l IN labels(law) WHERE l ENDS WITH 'recht')
    OPTIONAL MATCH (law)-[:GILT_IN_LAND]->(land:Land)
          WHERE land.name = 'Schweiz'
    RETURN coalesce(bg.name,bg.id) AS bg_name, rf.name AS rf, nf.name AS nf,
           [l IN labels(law) WHERE l ENDS WITH 'recht'][0] AS law_domain, land.name AS land
    """
    rows = [dict(r) for r in session.run(q)]
    G = nx.DiGraph()
    bg_name = rows[0]["bg_name"] if rows else "Stahlträger K.118"
    G.add_node("BG", group="Bauteilgruppe", label=short(bg_name, 24), color=PALETTE["Bauteilgruppe"], size=1500, tier=0)
    dom_count: Counter = Counter()
    for r in rows:
        if not r["rf"]:
            continue
        rf = f"RF::{r['rf']}"
        G.add_node(rf, group="Regulierungsfrage", label=short(r["rf"], 22), color=PALETTE["Regulierungsfrage"], size=760, tier=1)
        G.add_edge("BG", rf, rel="TRIGGERS")
        if r["nf"]:
            nf = f"NF::{r['nf']}"
            G.add_node(nf, group="Nachweisforderung", label=short(r["nf"], 22), color=PALETTE["Nachweisforderung"], size=640, tier=2)
            G.add_edge(rf, nf, rel="ERFORDERT_NACHWEIS")
            if r["law_domain"]:
                dm = f"DM::{r['law_domain']}"
                dom_count[r["law_domain"]] += 1
                G.add_node(dm, group="Regelwerk", label=r["law_domain"], color=PALETTE["Regelwerk"], size=620, tier=3)
                G.add_edge(nf, dm, rel="GESTUETZT_AUF")
                if r["land"]:
                    ld = f"LD::{r['land']}"
                    G.add_node(ld, group="Land", label=r["land"], color=PALETTE["Land"], size=820, tier=4)
                    G.add_edge(dm, ld, rel="GILT_IN_LAND")
    meta = {"layout": "multipartite",
            "legend": {"Bauteilgruppe": PALETTE["Bauteilgruppe"], "Regulierungsfrage": PALETTE["Regulierungsfrage"],
                       "Nachweisforderung": PALETTE["Nachweisforderung"], "Rechtsdomäne / Regelwerk": PALETTE["Regelwerk"], "Land": PALETTE["Land"]},
            "stats": {"regulierungsfragen": sum(1 for n in G if n.startswith("RF::")),
                      "nachweisforderungen": sum(1 for n in G if n.startswith("NF::")),
                      "rechtsdomaenen": sum(1 for n in G if n.startswith("DM::"))}}
    return G, meta, rows


def build_d1(session):
    q = """
    MATCH (h:Huerde)<-[:HAT_HUERDE]-(x)
    RETURN h.id AS hid, coalesce(h.name,h.id) AS huerde, count(*) AS incidence,
           labels(x)[0] AS quelle
    """
    raw = [dict(r) for r in session.run(q)]
    inc: Counter = Counter(); name_of = {}; per_src = {}
    for r in raw:
        inc[r["hid"]] += r["incidence"]; name_of[r["hid"]] = r["huerde"]
        per_src.setdefault(r["hid"], Counter())[r["quelle"]] += r["incidence"]
    # co-occurrence via shared projects
    cooc = session.run("""
        MATCH (h1:Huerde)<-[:HAT_HUERDE]-(x)-[:HAT_HUERDE]->(h2:Huerde)
        WHERE h1.id < h2.id
        RETURN h1.id AS a, h2.id AS b, count(DISTINCT x) AS w
    """)
    G = nx.Graph()
    for hid, n in inc.items():
        G.add_node(hid, group="Huerde", label=f"{short(name_of[hid], 24)}\n[{n}]",
                   color=PALETTE["Huerde"], size=300 + 42 * n)
    edges = []
    for r in cooc:
        d = dict(r)
        if d["a"] in G and d["b"] in G and d["w"] >= 5:
            G.add_edge(d["a"], d["b"], weight=d["w"]); edges.append(d)
    ranked = sorted(inc.items(), key=lambda x: -x[1])
    # order nodes by incidence so circular layout places them by rank
    G2 = nx.Graph()
    for hid, _n in ranked:
        G2.add_node(hid, **G.nodes[hid])
    G2.add_edges_from(G.edges(data=True))
    G = G2
    meta = {"layout": "circular",
            "legend": {"Hürde (Größe / [n] = Häufigkeit)": PALETTE["Huerde"], "Kante = gemeinsames Auftreten (≥5)": "#C2C7CC"},
            "stats": {"huerden": len(inc),
                      "top": [{"huerde": name_of[h], "vorkommen": n} for h, n in ranked[:8]]}}
    return G, meta, {"incidence": raw, "cooccurrence": edges}


# --------------------------------------------------------------------------- #


def layout_for(G, meta):
    kind = meta["layout"]
    if kind == "multipartite":
        return nx.multipartite_layout(G, subset_key="tier", align="vertical")
    if kind == "bipartite":
        top = [n for n, d in G.nodes(data=True) if d.get("bipartite") == 0]
        return nx.bipartite_layout(G, top, align="vertical", scale=2.4)
    if kind == "radial_country":
        lands = [n for n, d in G.nodes(data=True) if d.get("is_land")]
        pos = nx.spring_layout(G, k=0.18, iterations=80, seed=7)
        for i, l in enumerate(sorted(lands)):
            ang = 2 * math.pi * i / max(1, len(lands))
            pos[l] = (math.cos(ang) * 1.18, math.sin(ang) * 1.18)
        return pos
    if kind == "circular":
        return nx.circular_layout(G, scale=1.7)
    if kind == "spring_wide":
        return nx.spring_layout(G, k=0.9, iterations=220, seed=5)
    k = 0.6 / max(1, G.number_of_nodes()) ** 0.5 + 0.25
    return nx.spring_layout(G, k=k, iterations=150, seed=11)


def render(G, meta, title, caption, path):
    pos = layout_for(G, meta)
    fig, ax = plt.subplots(figsize=(15, 10.5))
    node_colors = [d.get("color", "#888888") for _, d in G.nodes(data=True)]
    node_sizes = [d.get("size", 200) for _, d in G.nodes(data=True)]
    if isinstance(G, nx.DiGraph):
        if meta.get("edge_cross_highlight"):
            normal = [(u, v) for u, v, d in G.edges(data=True) if not d.get("cross")]
            crossed = [(u, v) for u, v, d in G.edges(data=True) if d.get("cross")]
            nx.draw_networkx_edges(G, pos, edgelist=normal, ax=ax, edge_color="#BBBBBB", arrows=True,
                                   arrowsize=10, width=1.0, alpha=0.6, connectionstyle="arc3,rad=0.06")
            nx.draw_networkx_edges(G, pos, edgelist=crossed, ax=ax, edge_color="#D62728", arrows=True,
                                   arrowsize=15, width=2.6, alpha=0.95, connectionstyle="arc3,rad=0.06")
        else:
            widths = [0.7 + 0.5 * G[u][v].get("weight", 1) for u, v in G.edges()]
            nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#9AA0A6", arrows=True, arrowsize=11,
                                   width=widths, alpha=0.7, connectionstyle="arc3,rad=0.05")
    else:
        widths = [0.5 + 0.45 * G[u][v].get("weight", 1) for u, v in G.edges()]
        nx.draw_networkx_edges(G, pos, ax=ax, edge_color="#C2C7CC", width=widths, alpha=0.55)
    nx.draw_networkx_nodes(G, pos, ax=ax, node_color=node_colors, node_size=node_sizes,
                           edgecolors="white", linewidths=0.8)
    labels = {n: d["label"] for n, d in G.nodes(data=True) if d.get("label")}
    nx.draw_networkx_labels(G, pos, labels=labels, ax=ax, font_size=8.0, font_color="#1A1A1A")
    handles = [mpatches.Patch(color=c, label=k) for k, c in meta["legend"].items()]
    ax.legend(handles=handles, loc="upper left", fontsize=8.5, frameon=True, framealpha=0.9, title="Legende")
    ax.set_title(title, fontsize=15, fontweight="bold", loc="left")
    ax.text(0.0, -0.04, caption, transform=ax.transAxes, fontsize=9.0, color="#444444", va="top", wrap=True)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def graph_to_json(G):
    return {"directed": isinstance(G, nx.DiGraph),
            "nodes": [{"id": n, **dict(d)} for n, d in G.nodes(data=True)],
            "edges": [{"source": u, "target": v, **dict(d)} for u, v, d in G.edges(data=True)]}


SNAPSHOTS: list[dict[str, Any]] = [
    {"id": "A1_akteurskonstellation", "builder": build_a1,
     "title": "A1 · Akteurs-Konstellation der Wiederverwendung (alle Länder)",
     "caption": ("Verbundene Akteure (VERBUNDEN_MIT_AKTEUR), eingefärbt nach Land. Rot = Bauteilbörsen/"
                 "Multiplikatoren. Das Feld ist ein real vernetztes, aber lose koordiniertes Ökosystem – "
                 "die integrierende Plattform ist die fehlende Schicht.")},
    {"id": "A2_hubs_bruecken", "builder": build_a2,
     "title": "A2 · Hubs & Brücken – die zentralen Multiplikatoren",
     "caption": ("Teilnetz der am stärksten vernetzten Akteure (höchster Grad). Identifiziert konkrete "
                 "Transfer-/Anbindungspartner i. S. der Auflage b (Concular, Madaster, bauteilnetz, Cirkla, Opalis).")},
    {"id": "A3_akteure_nach_land", "builder": build_a3,
     "title": "A3 · Akteure nach Land",
     "caption": ("Geografische Verteilung der Akteure (LIEGT_IN_LAND). Knotengröße der Länder = Anzahl Akteure. "
                 "Beleg für die internationale Reichweite, die eine offene Plattform adressiert.")},
    {"id": "B1_bauteilgruppen_k118", "builder": build_b1,
     "title": "B1 · Semantische Bauteil-Repräsentation am Beispiel K.118 Winterthur",
     "caption": ("Bauteilgruppen des Projekts K.118 mit Spenderbauwerk, Bauteiltyp, Material und Tragend-Flag (⚙). "
                 "Beleg, dass Komponenten mit genau jenen Metadatenfeldern semantisch erfasst werden können, die "
                 "die Plattform-Schnittstelle benötigt.")},
    {"id": "B2_spender_empfaenger", "builder": build_b2,
     "title": "B2 · Spender → Empfänger – reale Bauteil-Flüsse (Urban Mining)",
     "caption": ("Bauwerk-zu-Bauwerk-Flüsse über wiederverwendete Bauteilgruppen (AUS_SPENDER → IN_EMPFANGSOBJEKT). "
                 "Rote Kanten = länderübergreifende Flüsse. Beleg für die Herkunfts-/Verbleib-Provenienz, die der Katalog tragen muss.")},
    {"id": "B3_bauteiltyp_material", "builder": build_b3,
     "title": "B3 · Bauteiltyp ↔ Material – das Komponenten-Vokabular",
     "caption": ("Bipartite Kopplung von Bauteiltyp und Material (Kantenstärke = Anzahl Bauteilgruppen). "
                 "Dieses Vokabular bildet die Grundlage für Filterung und KI-gestützte Vorschläge.")},
    {"id": "C1_normen_nach_land", "builder": build_c1,
     "title": "C1 · Normen-/Rechtslandschaft nach Land",
     "caption": ("Welche Rechtsdomänen sind je Land dokumentiert (Regelwerk GILT_IN_LAND, Kantenstärke = Anzahl Normknoten). "
                 "Der länderspezifische Rahmen, den die Nachweis-Funktionen (Tragwerk, Ökobilanz) respektieren müssen.")},
    {"id": "C2_regelkette", "builder": build_c2,
     "title": "C2 · Nachweis-Kette: Bauteil → Frage → Nachweis → Regelwerk → Land",
     "caption": ("Semantische Kette für einen wiederverwendeten Stahlträger (K.118, Schweiz); Regelwerke zur Lesbarkeit "
                 "nach Rechtsdomäne aggregiert. Genau die Verknüpfung von Metadaten und Nachweisanforderungen, nach der Forschungsfrage 6.1 fragt.")},
    {"id": "D1_huerden", "builder": build_d1,
     "title": "D1 · Wiederverwendungs-Hürden (empirisch)",
     "caption": ("Dokumentierte Hürden; Knotengröße/[Zahl] = Häufigkeit der Nennung in Projekten und Bauteilgruppen, "
                 "Kanten = gemeinsames Auftreten. Empirische Grundlage für die Problemstellung (§4.1/4.2) und die Interview-Leitfäden (§6.2).")},
]


def main():
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    manifest = []
    with driver.session(database=database) as session:
        for snap in SNAPSHOTS:
            sid = snap["id"]
            print(f"--- {sid} ---")
            G, meta, rows = snap["builder"](session)
            render(G, meta, snap["title"], snap["caption"], OUT / f"{sid}.png")
            payload = {"id": sid, "title": snap["title"], "caption": snap["caption"],
                       "stats": meta["stats"], "graph": graph_to_json(G), "rows": rows}
            (OUT / f"{sid}.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
            manifest.append({"id": sid, "title": snap["title"], "png": f"{sid}.png", "json": f"{sid}.json",
                             "nodes": G.number_of_nodes(), "edges": G.number_of_edges(), "stats": meta["stats"]})
            print(f"    nodes={G.number_of_nodes()} edges={G.number_of_edges()} stats={meta['stats']}")
    (OUT / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    driver.close()
    print(f"\nWrote {len(manifest)} snapshots to {OUT}")


if __name__ == "__main__":
    main()
