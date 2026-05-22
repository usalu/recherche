"""Project-level analysis with a reuse-scalability lens.

Writes scalability_results.json.
"""
from __future__ import annotations

import json
import statistics as st
import sys
from collections import defaultdict
from pathlib import Path

from neo4j import GraphDatabase

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

HERE = Path(__file__).resolve().parent


def rows(session, q, **p):
    return [dict(r) for r in session.run(q, **p)]


def desc(vals):
    vals = [v for v in vals if isinstance(v, (int, float))]
    if not vals:
        return None
    return {"n": len(vals), "min": round(min(vals), 1), "median": round(st.median(vals), 1),
            "max": round(max(vals), 1)}


REUSE_INCL = ("reuse", "reused", "reclaim", "salvage", "anteil", "circular", "réempl",
              "biosourc", "recycl")
REUSE_EXCL = ("pv", "strom", "prize", "electric", "award")


def main() -> None:
    uri, user, password, database = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    with drv.session(database=database) as s:

        base = rows(s, """
            MATCH (p:Projekt)
            OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(land:Land)
            RETURN p.id AS id, coalesce(p.name,p.id) AS name, land.name AS land,
                   p.year_completed AS jahr, p.area_m2_gross AS area,
                   p.bauobjektklasse AS klasse, p.nutzung_text AS nutzung,
                   p.zertifizierungssysteme AS zert, p.lca_modules AS lca,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) } AS n_bg,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(:Bauwerk) } AS bg_mit_spender
        """)
        # distinct donor buildings per project
        donors = rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(b:Bauwerk)
            RETURN p.id AS id, count(DISTINCT b) AS donors
        """)
        donor_map = {r["id"]: r["donors"] for r in donors}
        # reuse share kennwerte per project
        ksh = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.category='reuse_share' AND k.wert IS NOT NULL AND k.einheit STARTS WITH '%'
            RETURN p.id AS id, k.kennwert AS name, k.wert AS wert
        """)
        share_map: dict[str, float] = {}
        for r in ksh:
            nm = (r["name"] or "").lower()
            if any(x in nm for x in REUSE_EXCL):
                continue
            if not any(x in nm for x in REUSE_INCL):
                continue
            share_map[r["id"]] = max(share_map.get(r["id"], 0), float(r["wert"]))
        # co2 reduction pct per project
        kco2 = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.wert IS NOT NULL AND k.einheit='%'
              AND (toLower(k.kennwert) CONTAINS 'co2' OR toLower(k.kennwert) CONTAINS 'co₂'
                   OR toLower(k.kennwert) CONTAINS 'reduktion')
            RETURN p.id AS id, k.wert AS wert
        """)
        co2_map: dict[str, float] = {}
        for r in kco2:
            co2_map[r["id"]] = max(co2_map.get(r["id"], 0), float(r["wert"]))

        proj = []
        for r in base:
            pid = r["id"]
            area = None
            try:
                area = float(r["area"]) if r["area"] is not None else None
            except Exception:
                area = None
            yr = None
            try:
                yr = int(r["jahr"]) if r["jahr"] is not None else None
            except Exception:
                yr = None
            proj.append({
                "id": pid, "name": r["name"], "land": r["land"], "jahr": yr, "area": area,
                "klasse": (r["klasse"][0] if isinstance(r["klasse"], list) and r["klasse"] else r["klasse"]),
                "n_bg": r["n_bg"], "donors": donor_map.get(pid, 0),
                "reuse_share": share_map.get(pid), "co2_red": co2_map.get(pid),
                "zert": bool(r["zert"]), "lca": bool(r["lca"]),
            })

    drv.close()

    out: dict = {}
    out["n_projects"] = len(proj)

    # --- Size profile ---
    areas = [p["area"] for p in proj if p["area"]]
    out["area_stats"] = desc(areas)
    size_buckets = defaultdict(int)
    def sbucket(a):
        if a is None:
            return "ohne Angabe"
        if a < 500:
            return "<500 (Pilot/Pavillon)"
        if a < 2000:
            return "500–2.000 (Klein-/Mittelbau)"
        if a < 10000:
            return "2.000–10.000 (Großbau)"
        return ">10.000 (Groß/Campus)"
    for p in proj:
        size_buckets[sbucket(p["area"])] += 1
    out["size_buckets"] = dict(size_buckets)

    # --- Reuse depth (share) profile ---
    shares = [p["reuse_share"] for p in proj if p["reuse_share"] is not None]
    out["reuse_share_stats"] = desc(shares)
    share_buckets = defaultdict(int)
    for v in shares:
        b = "sehr hoch ≥75%" if v >= 75 else ("hoch 50–75%" if v >= 50 else
            ("mittel 25–50%" if v >= 25 else "niedrig <25%"))
        share_buckets[b] += 1
    out["reuse_share_buckets"] = dict(share_buckets)

    # --- Depth vs size (the scalability question) ---
    depth_by_size = defaultdict(list)
    for p in proj:
        if p["area"] and p["reuse_share"] is not None:
            depth_by_size[sbucket(p["area"])].append(p["reuse_share"])
    out["reuse_depth_by_size"] = {
        k: {"n": len(v), "median_reuse_share": round(st.median(v), 1),
            "max": round(max(v), 1)} for k, v in depth_by_size.items()}
    out["size_vs_share_pairs"] = [
        {"name": p["name"], "land": p["land"], "area": p["area"],
         "reuse_share": p["reuse_share"], "n_bg": p["n_bg"], "donors": p["donors"]}
        for p in proj if p["area"] and p["reuse_share"] is not None]

    # --- Sourcing model: donors per project ---
    dvals = [p["donors"] for p in proj if p["bg_mit_spender" if False else "donors"] is not None]
    donors_all = [p["donors"] for p in proj]
    with_donor = [d for d in donors_all if d > 0]
    out["sourcing"] = {
        "projekte_mit_spender": len(with_donor),
        "donors_stats": desc(with_donor),
        "single_donor": sum(1 for d in with_donor if d == 1),
        "few_2_3": sum(1 for d in with_donor if 2 <= d <= 3),
        "many_4plus": sum(1 for d in with_donor if d >= 4),
        "top_aggregators": sorted(
            [{"name": p["name"], "land": p["land"], "donors": p["donors"], "n_bg": p["n_bg"],
              "area": p["area"], "reuse_share": p["reuse_share"]} for p in proj if p["donors"] > 0],
            key=lambda x: x["donors"], reverse=True)[:10],
    }

    # --- Component breadth vs size ---
    out["breadth_vs_size"] = {}
    bb = defaultdict(list)
    for p in proj:
        bb[sbucket(p["area"])].append(p["n_bg"])
    for k, v in bb.items():
        out["breadth_vs_size"][k] = {"n": len(v), "median_bauteilgruppen": round(st.median(v), 1)}

    # --- Temporal scaling ---
    def ybucket(y):
        if y is None:
            return None
        return ("≤2014" if y <= 2014 else "2015–2019" if y <= 2019 else
                "2020–2024" if y <= 2024 else "2025+")
    tb = defaultdict(lambda: {"count": 0, "areas": [], "shares": [], "donors": []})
    for p in proj:
        b = ybucket(p["jahr"])
        if not b:
            continue
        tb[b]["count"] += 1
        if p["area"]:
            tb[b]["areas"].append(p["area"])
        if p["reuse_share"] is not None:
            tb[b]["shares"].append(p["reuse_share"])
        if p["donors"]:
            tb[b]["donors"].append(p["donors"])
    out["temporal"] = {
        k: {"projekte": v["count"],
            "median_area": round(st.median(v["areas"]), 0) if v["areas"] else None,
            "median_reuse_share": round(st.median(v["shares"]), 1) if v["shares"] else None,
            "median_donors": round(st.median(v["donors"]), 1) if v["donors"] else None}
        for k, v in sorted(tb.items())}

    # --- Typology of recipient projects ---
    kl = defaultdict(int)
    for p in proj:
        if p["klasse"]:
            kl[p["klasse"]] += 1
    out["klasse"] = dict(sorted(kl.items(), key=lambda kv: kv[1], reverse=True))

    # --- Existence proof: large AND high-reuse projects ---
    out["scalable_examples"] = sorted(
        [{"name": p["name"], "land": p["land"], "area": p["area"], "reuse_share": p["reuse_share"],
          "n_bg": p["n_bg"], "donors": p["donors"], "co2_red": p["co2_red"]}
         for p in proj if p["area"] and p["area"] >= 2000 and p["reuse_share"] is not None
         and p["reuse_share"] >= 50],
        key=lambda x: x["area"], reverse=True)

    # --- Maturity signals ---
    out["maturity"] = {
        "mit_zertifizierung": sum(1 for p in proj if p["zert"]),
        "mit_lca_modules": sum(1 for p in proj if p["lca"]),
        "mit_reuse_share_wert": len(shares),
        "mit_flaeche": len(areas),
    }

    (HERE / "scalability_results.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")

    print("Projekte:", out["n_projects"])
    print("Fläche:", out["area_stats"])
    print("Größenklassen:", out["size_buckets"])
    print("Reuse-Anteil:", out["reuse_share_stats"], out["reuse_share_buckets"])
    print("\nReuse-Tiefe nach Größe:")
    for k, v in out["reuse_depth_by_size"].items():
        print("  ", k, v)
    print("\nSourcing:", {k: out["sourcing"][k] for k in
          ["projekte_mit_spender", "donors_stats", "single_donor", "few_2_3", "many_4plus"]})
    print("Top-Aggregatoren:")
    for a in out["sourcing"]["top_aggregators"][:6]:
        print("  ", a)
    print("\nBreite nach Größe:", out["breadth_vs_size"])
    print("\nTemporal:")
    for k, v in out["temporal"].items():
        print("  ", k, v)
    print("\nGebäudeklasse:", out["klasse"])
    print("\nSkalierbare Beispiele (>=2000 m² & >=50% reuse):")
    for e in out["scalable_examples"]:
        print("  ", e)
    print("\nReife:", out["maturity"])
    print("\nWrote scalability_results.json")


if __name__ == "__main__":
    main()
