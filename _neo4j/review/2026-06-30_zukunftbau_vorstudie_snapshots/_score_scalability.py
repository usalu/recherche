"""Per-project Reuse-Scalability Index (SKI).

Documented, reproducible scoring system applied to every project.
Writes: project_scalability_scores.json / .csv and _scal_table.md (ranked table).
"""
from __future__ import annotations

import csv
import json
import math
import statistics as st
import sys
from collections import Counter
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

# ---- Scoring configuration (the documented "system") ----
WEIGHTS = {           # relative importance of each scalability dimension
    "bezug": 0.30,    # sourcing model — the identified bottleneck (§3.3)
    "tiefe": 0.20,    # reuse depth (share)
    "massstab": 0.20, # absolute scale (area)
    "umfang": 0.15,   # component volume
    "reife": 0.15,    # evidence / documentation maturity
}
AREA_MIN, AREA_MAX = 50.0, 80000.0   # log-normalization bounds for scale
BG_FULL = 15.0                        # n_bauteilgruppen giving full volume score
DONOR_SCORE = {1: 20, 2: 50, 3: 75}  # >=4 -> 100

REUSE_INCL = ("reuse", "reused", "reclaim", "salvage", "anteil", "circular", "réempl",
              "biosourc", "recycl")
REUSE_EXCL = ("pv", "strom", "prize", "electric", "award")


def rows(session, q):
    return [dict(r) for r in session.run(q)]


def clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


def score_scale(area):
    if not area:
        return None
    return round(clamp((math.log10(area) - math.log10(AREA_MIN)) /
                       (math.log10(AREA_MAX) - math.log10(AREA_MIN)) * 100), 1)


def score_bezug(donors):
    if not donors:
        return None
    return float(DONOR_SCORE.get(donors, 100))


def score_reife(n_kennwerte, has_lca, has_zert, n_nachweise):
    ev = 0
    if n_kennwerte > 0:
        ev += 40
    if has_lca:
        ev += 20
    if has_zert:
        ev += 20
    if n_nachweise > 0:
        ev += 20
    return float(min(100, ev))


def archetype(area, share, donors, ski):
    if donors and donors >= 3:
        return "Aggregator (skalierbares Bezugsmodell)"
    if area and area >= 2000 and share is not None and share >= 50:
        return "Großmaßstab-Demonstrator"
    if share is not None and share >= 75:
        return "Tiefen-Pilot (hohe Quote, Einzelquelle)"
    if area and area < 500:
        return "Klein-Pilot"
    return "Fallstudie (teil-dokumentiert)"


def main() -> None:
    uri, user, password, database = resolve_connection()
    drv = GraphDatabase.driver(uri, auth=(user, password))
    with drv.session(database=database) as s:
        base = rows(s, """
            MATCH (p:Projekt)
            OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(land:Land)
            RETURN p.id AS id, coalesce(p.name_full, p.name, p.id) AS name, land.name AS land,
                   p.year_completed AS jahr, p.area_m2_gross AS area,
                   p.bauobjektklasse AS klasse,
                   (p.zertifizierungssysteme IS NOT NULL) AS zert,
                   (p.lca_modules IS NOT NULL) AS lca,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) } AS n_bg,
                   count { (p)-[:HAT_KENNWERT]->(:Kennwert) } AS n_kw,
                   count { (p)-[:ERFORDERT_NACHWEIS]->() } AS n_nw
        """)
        donors = {r["id"]: r["d"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(b:Bauwerk)
            RETURN p.id AS id, count(DISTINCT b) AS d
        """)}
        ksh = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.category='reuse_share' AND k.wert IS NOT NULL AND k.einheit STARTS WITH '%'
            RETURN p.id AS id, k.kennwert AS name, k.wert AS wert
        """)
        share = {}
        for r in ksh:
            nm = (r["name"] or "").lower()
            if any(x in nm for x in REUSE_EXCL) or not any(x in nm for x in REUSE_INCL):
                continue
            share[r["id"]] = max(share.get(r["id"], 0.0), float(r["wert"]))
    drv.close()

    results = []
    for r in base:
        pid = r["id"]
        try:
            area = float(r["area"]) if r["area"] is not None else None
        except Exception:
            area = None
        try:
            yr = int(r["jahr"]) if r["jahr"] is not None else None
        except Exception:
            yr = None
        klasse = r["klasse"][0] if isinstance(r["klasse"], list) and r["klasse"] else r["klasse"]
        d = donors.get(pid, 0)
        sh = share.get(pid)

        sub = {
            "bezug": score_bezug(d),
            "tiefe": round(clamp(sh), 1) if sh is not None else None,
            "massstab": score_scale(area),
            "umfang": round(min(100.0, r["n_bg"] / BG_FULL * 100), 1),
            "reife": score_reife(r["n_kw"], r["lca"], r["zert"], r["n_nw"]),
        }
        num = sum(WEIGHTS[k] * v for k, v in sub.items() if v is not None)
        den = sum(WEIGHTS[k] for k, v in sub.items() if v is not None)
        ski = round(num / den, 1) if den else 0.0
        ndims = sum(1 for v in sub.values() if v is not None)
        results.append({
            "id": pid, "name": r["name"], "land": r["land"], "jahr": yr,
            "area": area, "klasse": klasse, "n_bg": r["n_bg"], "donors": d,
            "reuse_share": sh, "n_kennwerte": r["n_kw"], "n_nachweise": r["n_nw"],
            "s_bezug": sub["bezug"], "s_tiefe": sub["tiefe"], "s_massstab": sub["massstab"],
            "s_umfang": sub["umfang"], "s_reife": sub["reife"],
            "SKI": ski, "dims": ndims,
            "archetyp": archetype(area, sh, d, ski),
        })

    results.sort(key=lambda x: x["SKI"], reverse=True)
    for i, r in enumerate(results, 1):
        r["rang"] = i

    (HERE / "project_scalability_scores.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = ["rang", "name", "land", "jahr", "area", "n_bg", "donors", "reuse_share",
            "n_kennwerte", "n_nachweise", "s_bezug", "s_tiefe", "s_massstab", "s_umfang",
            "s_reife", "SKI", "dims", "archetyp"]
    with (HERE / "project_scalability_scores.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)

    # markdown ranked table
    def fmt(v, suff=""):
        if v is None:
            return "—"
        if isinstance(v, float):
            return (f"{v:.0f}" if v == int(v) else f"{v:.1f}") + suff
        return str(v) + suff
    lines = ["| # | Projekt | Land | Jahr | Fläche m² | BTGr | Spender | Reuse% | "
             "Bezug | Tiefe | Maßstab | Umfang | Reife | **SKI** | Archetyp |",
             "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in results:
        nm = r["name"] if len(r["name"]) <= 34 else r["name"][:33] + "…"
        lines.append(
            f"| {r['rang']} | {nm} | {r['land'] or '—'} | {fmt(r['jahr'])} | "
            f"{fmt(r['area'])} | {r['n_bg']} | {r['donors'] or '—'} | {fmt(r['reuse_share'])} | "
            f"{fmt(r['s_bezug'])} | {fmt(r['s_tiefe'])} | {fmt(r['s_massstab'])} | "
            f"{fmt(r['s_umfang'])} | {fmt(r['s_reife'])} | **{fmt(r['SKI'])}** | {r['archetyp']} |")
    arche = Counter(r["archetyp"] for r in results)
    (HERE / "_scal_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"Projekte bewertet: {len(results)}")
    print(f"SKI Median: {st.median([r['SKI'] for r in results]):.1f}, "
          f"Max: {max(r['SKI'] for r in results):.1f}, Min: {min(r['SKI'] for r in results):.1f}")
    print("Archetypen:")
    for a, n in arche.most_common():
        print(f"   {n:>3}  {a}")
    print("\nTop 12:")
    for r in results[:12]:
        print(f"  {r['rang']:>2} {r['name'][:38]:38} SKI {r['SKI']:>5}  "
              f"[{r['archetyp']}]  bezug={r['s_bezug']} tiefe={r['s_tiefe']} "
              f"massstab={r['s_massstab']} umfang={r['s_umfang']} reife={r['s_reife']}")
    print("\nWrote project_scalability_scores.json/.csv and _scal_table.md")


if __name__ == "__main__":
    main()
