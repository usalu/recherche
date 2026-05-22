"""Reuse-Scalability Index v2 (RSI) — literature-anchored, with verified enrichment.

Six dimensions, each mapped to an established reuse/circularity framework:

  1. Bezug & Reverse-Logistik (w .25) -> reverse-logistics / market-scaling literature
     (Reuse Market Dynamics 2024; BCR-Feasibility business+organisational domain).
  2. Wiederverwendungstiefe        (w .20) -> Level(s) 2.2/2.4; EMF-MCI; Küpfer et al. reuse rate.
  3. Maßstab (absolute Größe)       (w .15) -> "moving beyond pilots" (BCR feasibility).
  4. Technische Reproduzierbarkeit/DfD (w .15) -> ISO 20887 (standardisation, independence,
     simplicity, ease of access); Küpfer construction-complexity criterion.
  5. Informationsreife & Nachweis   (w .15) -> Reuse Market Dynamics "information gap";
     Madaster material passports; RVI technical dimension (compliance/residual value).
  6. Umweltwirkungs-Nachweis        (w .10) -> Level(s) 1.2 GWP (module D); embodied-carbon lit.

Verified external values (verified_enrichment.json) override graph values for benchmark
projects; every field carries provenance ('verified' | 'graph').

Writes: project_scalability_scores.json / .csv and _scal_table.md
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

WEIGHTS = {
    "bezug": 0.25,
    "tiefe": 0.20,
    "massstab": 0.15,
    "technik": 0.15,
    "reife": 0.15,
    "wirkung": 0.10,
}
AREA_MIN, AREA_MAX = 50.0, 80000.0

REUSE_INCL = ("reuse", "reused", "reclaim", "salvage", "anteil", "circular", "réempl",
              "biosourc", "recycl", "ombruk", "gjenbruk", "wiederverw")
REUSE_EXCL = ("pv", "strom", "prize", "electric", "award", "operational")


def rows(session, q):
    return [dict(r) for r in session.run(q)]


def clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


# ---- dimension scoring rules (documented) ----
def score_bezug(donors, n_beschaffung):
    if not donors:
        return None
    base = 20.0 + 30.0 * math.log2(donors)          # 1->20, 2->50, 4->80, 8->110, 25->~159
    if n_beschaffung and n_beschaffung >= 3:
        base += 10                                   # diverse market procurement = repeatable
    elif n_beschaffung and n_beschaffung >= 2:
        base += 5
    return round(clamp(base), 1)


def score_tiefe(share):
    return round(clamp(share), 1) if share is not None else None


def score_massstab(area):
    if not area:
        return None
    return round(clamp((math.log10(area) - math.log10(AREA_MIN)) /
                       (math.log10(AREA_MAX) - math.log10(AREA_MIN)) * 100), 1)


def score_technik(n_bg, n_tragend, has_reversible, n_bauteiltyp, dfd_flag):
    t = 0.0
    if n_tragend and n_tragend > 0:
        t += 30                                      # structural reuse: hardest, highest value
    if dfd_flag or has_reversible:
        t += 25                                      # reversible joints / deconstruction method
    t += min(25.0, (n_bg / 10.0) * 25.0)             # systemic breadth of element groups
    if n_bauteiltyp and n_bauteiltyp >= 5:
        t += 20                                      # documented, transferable type catalogue
    elif n_bauteiltyp and n_bauteiltyp >= 2:
        t += 10
    return round(clamp(t), 1) if (n_bg or n_tragend or n_bauteiltyp) else None


def score_reife(n_kw, has_lca, has_zert, n_nw, has_zustand):
    ev = 0
    if n_kw > 0:
        ev += 30
    if has_lca:
        ev += 20
    if has_zert:
        ev += 15
    if n_nw > 0:
        ev += 20
    if has_zustand:
        ev += 15                                     # condition class = residual value / QA info
    return float(min(100, ev))


def score_wirkung(co2_pct, co2_t):
    w = None
    if co2_pct is not None:
        w = clamp(co2_pct * 1.25)                    # 80% GHG cut -> 100; 60%->75; 30%->37.5
    if co2_t is not None:
        w = max(w or 0.0, 55.0)                      # quantified tonnes proof present
    return round(w, 1) if w is not None else None


def archetype(area, share, donors, technik, co2_pct):
    if donors and donors >= 5:
        return "Aggregator – skalierbares Bezugsmodell"
    if area and area >= 5000 and ((share is not None and share >= 40)
                                  or (technik is not None and technik >= 60)
                                  or (co2_pct is not None and co2_pct >= 25)):
        return "Großmaßstab-Demonstrator"
    if share is not None and share >= 75 and (not donors or donors <= 1):
        return "Tiefen-Pilot (hohe Quote, schmale Quelle)"
    if technik is not None and technik >= 70:
        return "DfD-/System-Pilot (reproduzierbare Bauweise)"
    if area and area < 500:
        return "Klein-Pilot / Reallabor"
    return "Fallstudie (teil-dokumentiert)"


def load_enrichment():
    data = json.loads((HERE / "verified_enrichment.json").read_text(encoding="utf-8"))
    return data["entries"]


def match_enrichment(name, entries):
    low = (name or "").lower()
    for e in entries:
        if e["match"].lower() in low:
            return e
    return None


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
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe)
                           WHERE toLower(toString(b.tragend)) IN ['true','ja','yes','1'] } AS n_tragend,
                   count { (p)-[:HAT_KENNWERT]->(:Kennwert) } AS n_kw,
                   count { (p)-[:ERFORDERT_NACHWEIS]->() } AS n_nw,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_ZUSTANDSKLASSE]->() } AS n_zust,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_VERBINDUNGSTECHNIK]->() } AS n_vt,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->() } AS n_rb,
                   count { (p)-[:HAT_RUECKBAUVERFAHREN]->() } AS n_rb_p
        """)
        donors = {r["id"]: r["d"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(b)
            WHERE b:Bauwerk OR b:Materialdepot
            RETURN p.id AS id, count(DISTINCT b) AS d
        """)}
        beschaffung = {r["id"]: r["n"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(w:Beschaffungsweg)
            RETURN p.id AS id, count(DISTINCT w) AS n
        """)}
        btyp = {r["id"]: r["n"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(t:Bauteiltyp)
            RETURN p.id AS id, count(DISTINCT t) AS n
        """)}
        ksh = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.category='reuse_share' AND k.wert IS NOT NULL AND coalesce(k.einheit,'') STARTS WITH '%'
            RETURN p.id AS id, k.kennwert AS name, k.wert AS wert
        """)
        share = {}
        for r in ksh:
            nm = (r["name"] or "").lower()
            if any(x in nm for x in REUSE_EXCL) or not any(x in nm for x in REUSE_INCL):
                continue
            share[r["id"]] = max(share.get(r["id"], 0.0), float(r["wert"]))

        co2 = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.category='co2_saving' AND k.wert IS NOT NULL
            RETURN p.id AS id, k.kennwert AS name, k.wert AS wert, coalesce(k.einheit,'') AS einheit
        """)
        co2_pct, co2_t = {}, {}
        for r in co2:
            nm = (r["name"] or "").lower()
            unit = (r["einheit"] or "").lower()
            val = float(r["wert"])
            is_pct = "%" in unit or "prozent" in nm or "pct" in nm or "reduktion" in nm and val <= 100
            is_ton = unit in ("t", "tco2", "t co2e", "tonnen") or "einsparung_t" in nm or unit.startswith("t")
            if is_pct and val <= 100:
                co2_pct[r["id"]] = max(co2_pct.get(r["id"], 0.0), val)
            elif is_ton:
                co2_t[r["id"]] = max(co2_t.get(r["id"], 0.0), val)
    drv.close()

    entries = load_enrichment()
    results = []
    for r in base:
        pid = r["id"]
        prov = {}

        def g(field, graph_val):
            prov[field] = "graph"
            return graph_val

        area = None
        try:
            area = float(r["area"]) if r["area"] is not None else None
        except Exception:
            area = None
        area = g("area", area)
        try:
            yr = int(r["jahr"]) if r["jahr"] is not None else None
        except Exception:
            yr = None
        klasse = r["klasse"][0] if isinstance(r["klasse"], list) and r["klasse"] else r["klasse"]

        d = g("donors", donors.get(pid, 0))
        nb = beschaffung.get(pid, 0)
        sh = g("reuse_share", share.get(pid))
        cpct = g("co2_pct", co2_pct.get(pid))
        ct = g("co2_t", co2_t.get(pid))
        dfd_flag = False
        prov["dfd"] = "graph"
        has_reversible = (r["n_vt"] > 0) or (r["n_rb"] > 0) or (r["n_rb_p"] > 0)

        # ---- apply verified enrichment overrides ----
        enr = match_enrichment(r["name"], entries)
        enr_sources = []
        if enr:
            enr_sources = enr.get("sources", [])
            if "donors" in enr:
                d = enr["donors"]; prov["donors"] = "verified"
            if "reuse_share" in enr:
                sh = enr["reuse_share"]; prov["reuse_share"] = "verified"
            if "area_m2_gross" in enr:
                area = enr["area_m2_gross"]; prov["area"] = "verified"
            if "co2_reduktion_pct" in enr:
                cpct = enr["co2_reduktion_pct"]; prov["co2_pct"] = "verified"
            if "co2_einsparung_t" in enr:
                ct = enr["co2_einsparung_t"]; prov["co2_t"] = "verified"
            if "dfd" in enr:
                dfd_flag = bool(enr["dfd"]); prov["dfd"] = "verified"

        sub = {
            "bezug": score_bezug(d, nb),
            "tiefe": score_tiefe(sh),
            "massstab": score_massstab(area),
            "technik": score_technik(r["n_bg"], r["n_tragend"], has_reversible or dfd_flag,
                                     btyp.get(pid, 0), dfd_flag),
            "reife": score_reife(r["n_kw"], r["lca"], r["zert"], r["n_nw"], r["n_zust"] > 0),
            "wirkung": score_wirkung(cpct, ct),
        }
        num = sum(WEIGHTS[k] * v for k, v in sub.items() if v is not None)
        den = sum(WEIGHTS[k] for k, v in sub.items() if v is not None)
        rsi = round(num / den, 1) if den else 0.0
        conf = round(den, 2)                          # data-completeness (sum of present weights)
        ndims = sum(1 for v in sub.values() if v is not None)

        results.append({
            "id": pid, "name": r["name"], "land": r["land"], "jahr": yr,
            "area": area, "klasse": klasse, "n_bg": r["n_bg"], "n_tragend": r["n_tragend"],
            "donors": d, "n_beschaffung": nb, "n_bauteiltyp": btyp.get(pid, 0),
            "reuse_share": sh, "co2_pct": cpct, "co2_t": ct,
            "n_kennwerte": r["n_kw"], "n_nachweise": r["n_nw"],
            "s_bezug": sub["bezug"], "s_tiefe": sub["tiefe"], "s_massstab": sub["massstab"],
            "s_technik": sub["technik"], "s_reife": sub["reife"], "s_wirkung": sub["wirkung"],
            "RSI": rsi, "confidence": conf, "dims": ndims,
            "archetyp": archetype(area, sh, d, sub["technik"], cpct),
            "provenance": prov, "verified": bool(enr), "sources": enr_sources,
        })

    results.sort(key=lambda x: (x["RSI"], x["confidence"]), reverse=True)
    for i, r in enumerate(results, 1):
        r["rang"] = i

    (HERE / "project_scalability_scores.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = ["rang", "name", "land", "jahr", "area", "n_bg", "n_tragend", "donors",
            "n_beschaffung", "n_bauteiltyp", "reuse_share", "co2_pct", "co2_t",
            "n_kennwerte", "n_nachweise", "s_bezug", "s_tiefe", "s_massstab", "s_technik",
            "s_reife", "s_wirkung", "RSI", "confidence", "dims", "verified", "archetyp"]
    with (HERE / "project_scalability_scores.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)

    def fmt(v, suff=""):
        if v is None:
            return "—"
        if isinstance(v, float):
            return (f"{v:.0f}" if v == int(v) else f"{v:.1f}") + suff
        return str(v) + suff

    lines = ["| # | Projekt | Land | Jahr | Fläche m² | Spend. | Reuse% | Bezug | Tiefe | "
             "Maßstab | Technik | Reife | Wirkung | **RSI** | Konf. | Archetyp |",
             "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in results:
        nm = r["name"] if len(r["name"]) <= 32 else r["name"][:31] + "…"
        vflag = " ✓" if r["verified"] else ""
        lines.append(
            f"| {r['rang']} | {nm}{vflag} | {r['land'] or '—'} | {fmt(r['jahr'])} | "
            f"{fmt(r['area'])} | {r['donors'] or '—'} | {fmt(r['reuse_share'])} | "
            f"{fmt(r['s_bezug'])} | {fmt(r['s_tiefe'])} | {fmt(r['s_massstab'])} | "
            f"{fmt(r['s_technik'])} | {fmt(r['s_reife'])} | {fmt(r['s_wirkung'])} | "
            f"**{fmt(r['RSI'])}** | {fmt(r['confidence'])} | {r['archetyp']} |")
    (HERE / "_scal_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    arche = Counter(r["archetyp"] for r in results)
    print(f"Projekte bewertet: {len(results)}  |  verifiziert angereichert: {sum(r['verified'] for r in results)}")
    print(f"RSI Median: {st.median([r['RSI'] for r in results]):.1f}  "
          f"Max: {max(r['RSI'] for r in results):.1f}  Min: {min(r['RSI'] for r in results):.1f}")
    print("Archetypen:")
    for a, n in arche.most_common():
        print(f"   {n:>3}  {a}")
    print("\nTop 15:")
    for r in results[:15]:
        print(f"  {r['rang']:>2} {r['name'][:36]:36} RSI {r['RSI']:>5} (konf {r['confidence']:.2f}) "
              f"[{r['archetyp']}]")
    print("\nWrote project_scalability_scores.json/.csv and _scal_table.md")


if __name__ == "__main__":
    main()
