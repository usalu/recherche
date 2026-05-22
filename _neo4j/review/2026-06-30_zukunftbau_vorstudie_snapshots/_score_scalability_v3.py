"""Reuse-Scalability Index v3 (RSI) — design-aware, literature-anchored, verified.

Second-dive revision. Changes vs v2:
  * NEW dedicated design dimension "Zirkuläres Design / Transformationskapazität",
    grounded in Durmisevic (Independence x Exchangeability), the DGBC/Alba-Concepts
    Disassembly-Potential method (connection type, accessibility, independence,
    product-edge geometry) and Brand's shearing layers. Operationalised from the
    graph's connection types (reversible vs cast/welded), deconstruction method,
    functional-change (exchangeability), construction method (prefab) and standardisation.
  * Reuse depth now scope-adjusted (whole_building vs single-gewerk) to stop a
    97%-steel-only figure outscoring an 80%-whole-building one.
  * Weights rebalanced and justified via the Multi-Level Perspective (niche->regime):
    sourcing (market infrastructure) and design (replicable niche technology) are the
    two binding levers; evidence/legitimation weighted up.

Six dimensions (weights):
  1. Bezug & Reverse-Logistik            .22  (reverse-logistics; MLP market infra; SNM)
  2. Wiederverwendungstiefe & -umfang    .16  (Level(s) 2.2/2.4; MCI; Küpfer; scope-adjusted)
  3. Maßstab                             .10  (beyond-pilots; BCR feasibility)
  4. Zirkuläres Design / TC              .22  (Durmisevic TC; DGBC DP; ISO 20887; Brand)
  5. Informationsreife & Nachweis        .18  (SNM legitimation; info-gap; Madaster; RVI)
  6. Umweltwirkungs-Nachweis             .12  (Level(s) 1.2 GWP; landscape decarbonisation)

Verified enrichment (verified_enrichment.json) overrides graph values incl. design_quality.
Writes: project_scalability_scores.json / .csv, _scal_table.md
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
    "bezug": 0.22,
    "tiefe": 0.16,
    "massstab": 0.10,
    "design": 0.22,
    "reife": 0.18,
    "wirkung": 0.12,
}
AREA_MIN, AREA_MAX = 50.0, 80000.0
SCOPE_FACTOR = {
    "whole_building": 1.0, "structural": 1.0, "facade": 0.8,
    "single_gewerk": 0.75, "temporary_borrowed": 0.9, None: 0.9,
}
REVERSIBLE = ("reversibel", "reversible", "verschraub", "klemm", "bolzen", "steck",
              "demontier", "schraub", "stahlverbinder", "stahlrahmen")
IRREVERSIBLE = ("verschweiss", "vermoertel", "mauerwerk_ausgleich", "geklebt", "kleb", "guss")
REUSE_INCL = ("reuse", "reused", "reclaim", "salvage", "anteil", "circular", "réempl",
              "biosourc", "recycl", "ombruk", "gjenbruk", "wiederverw")
REUSE_EXCL = ("pv", "strom", "prize", "electric", "award", "operational")


def rows(session, q):
    return [dict(r) for r in session.run(q)]


def clamp(x, lo=0.0, hi=100.0):
    return max(lo, min(hi, x))


def score_bezug(donors, n_beschaffung):
    if not donors:
        return None
    base = 20.0 + 30.0 * math.log2(donors)
    if n_beschaffung and n_beschaffung >= 3:
        base += 10
    elif n_beschaffung and n_beschaffung >= 2:
        base += 5
    return round(clamp(base), 1)


def score_tiefe(share, scope, tragend, n_bg):
    if share is not None:
        return round(clamp(share * SCOPE_FACTOR.get(scope, 0.9)), 1)
    proxy = []
    if tragend and tragend > 0:
        proxy.append(55.0)                       # structural reuse is deep by nature
    if n_bg:
        proxy.append(min(50.0, n_bg / 10.0 * 50.0))
    return round(max(proxy), 1) if proxy else None


def score_massstab(area):
    if not area:
        return None
    return round(clamp((math.log10(area) - math.log10(AREA_MIN)) /
                       (math.log10(AREA_MAX) - math.log10(AREA_MIN)) * 100), 1)


def score_design(rev, tot, has_nondestruct, has_rueckbau, has_exch, prefab,
                 n_levels, n_btyp, verified_dq):
    if verified_dq is not None:
        return float(verified_dq)                # expert-verified DP/adaptability anchor
    d, signal = 0.0, False
    if tot and tot > 0:
        d += (rev / tot) * 35.0                  # DGBC connection-type / Durmisevic exchangeability
        signal = True
    if has_nondestruct:
        d += 20; signal = True                   # non-destructive deconstruction
    elif has_rueckbau:
        d += 10; signal = True
    if has_exch:
        d += 15; signal = True                   # functional change demonstrated (exchangeability)
    if prefab:
        d += 15; signal = True                   # prefab/dry assembly -> separable (Brand layers)
    if n_levels and n_levels >= 2:
        d += 8; signal = True                    # engages multiple building layers
    if n_btyp and n_btyp >= 5:
        d += 7; signal = True
    elif n_btyp and n_btyp >= 2:
        d += 4; signal = True
    # graph-derived design is capped at 90; 90+ ("reference-grade") requires
    # documented zero-damage evidence via the verified layer (design_quality).
    return round(clamp(d, hi=90.0), 1) if signal else None


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
        ev += 15
    return float(min(100, ev))


def score_wirkung(co2_pct, co2_t):
    w = None
    if co2_pct is not None:
        w = clamp(co2_pct * 1.25)
    if co2_t is not None:
        w = max(w or 0.0, 55.0)
    return round(w, 1) if w is not None else None


def archetype(area, share, donors, design, co2_pct):
    if design is not None and design >= 92:
        return "DfD-Referenz (Design-Vorbild)"
    if donors and donors >= 5:
        return "Aggregator – skalierbares Bezugsmodell"
    if area and area >= 5000 and ((share is not None and share >= 40)
                                  or (design is not None and design >= 70)
                                  or (co2_pct is not None and co2_pct >= 25)):
        return "Großmaßstab-Demonstrator"
    if share is not None and share >= 75 and (not donors or donors <= 1):
        return "Tiefen-Pilot (hohe Quote, schmale Quelle)"
    if design is not None and design >= 65:
        return "System-Pilot (reproduzierbare Bauweise)"
    if area and area < 500:
        return "Klein-Pilot / Reallabor"
    return "Fallstudie (teil-dokumentiert)"


def load_enrichment():
    return json.loads((HERE / "verified_enrichment.json").read_text(encoding="utf-8"))["entries"]


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
                   p.year_completed AS jahr, p.area_m2_gross AS area, p.bauobjektklasse AS klasse,
                   (p.zertifizierungssysteme IS NOT NULL) AS zert,
                   (p.lca_modules IS NOT NULL) AS lca,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe) } AS n_bg,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe)
                           WHERE toLower(toString(b.tragend)) IN ['true','ja','yes','1'] } AS n_tragend,
                   count { (p)-[:HAT_KENNWERT]->(:Kennwert) } AS n_kw,
                   count { (p)-[:ERFORDERT_NACHWEIS]->() } AS n_nw,
                   count { (p)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_ZUSTANDSKLASSE]->() } AS n_zust
        """)

        def cmap(q):
            return {r["id"]: r["n"] for r in rows(s, q)}

        donors = cmap("""MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:AUS_SPENDER]->(b)
                         WHERE b:Bauwerk OR b:Materialdepot RETURN p.id AS id, count(DISTINCT b) AS n""")
        beschaffung = cmap("""MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_BESCHAFFUNGSWEG]->(w:Beschaffungsweg)
                              RETURN p.id AS id, count(DISTINCT w) AS n""")
        btyp = cmap("""MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_BAUTEILTYP]->(t:Bauteiltyp)
                       RETURN p.id AS id, count(DISTINCT t) AS n""")

        # connection reversibility per project
        conn = rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_VERBINDUNGSTECHNIK]->(v:Verbindungstechnik)
            RETURN p.id AS id, toLower(coalesce(v.name,v.id)) AS vt, count(*) AS n
        """)
        rev_cnt, tot_cnt = {}, {}
        for r in conn:
            tot_cnt[r["id"]] = tot_cnt.get(r["id"], 0) + r["n"]
            vt = r["vt"]
            if any(x in vt for x in REVERSIBLE):
                rev_cnt[r["id"]] = rev_cnt.get(r["id"], 0) + r["n"]

        nondestruct = {r["id"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->(x:Rueckbauverfahren)
            WHERE toLower(coalesce(x.name,x.id)) CONTAINS 'zerstoerungsarme'
               OR toLower(coalesce(x.name,x.id)) CONTAINS 'demontage'
            RETURN DISTINCT p.id AS id""")}
        has_rueckbau = {r["id"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_RUECKBAUVERFAHREN]->()
            RETURN DISTINCT p.id AS id""")}
        has_exch = {r["id"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe)
            WHERE any(x IN b.funktionswechsel WHERE x IN ['Neue_Funktion','Konstruktive_Funktion'])
            RETURN DISTINCT p.id AS id""")}
        prefab = {r["id"] for r in rows(s, """
            MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(:Bauteilgruppe)-[:HAT_BAUWEISE]->(w:Bauweise)
            WHERE toLower(coalesce(w.name,w.id)) IN ['fertigteilbauweise','stahlbauweise','holzbauweise','hybridbauweise']
            RETURN DISTINCT p.id AS id""")}
        levels = cmap("""MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe)
                         WHERE b.bauteilebene IS NOT NULL
                         UNWIND b.bauteilebene AS lv
                         RETURN p.id AS id, count(DISTINCT lv) AS n""")

        ksh = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.category='reuse_share' AND k.wert IS NOT NULL AND coalesce(k.einheit,'') STARTS WITH '%'
            RETURN p.id AS id, k.kennwert AS name, k.wert AS wert""")
        share = {}
        for r in ksh:
            nm = (r["name"] or "").lower()
            if any(x in nm for x in REUSE_EXCL) or not any(x in nm for x in REUSE_INCL):
                continue
            share[r["id"]] = max(share.get(r["id"], 0.0), float(r["wert"]))

        co2 = rows(s, """
            MATCH (p:Projekt)-[:HAT_KENNWERT]->(k:Kennwert)
            WHERE k.category='co2_saving' AND k.wert IS NOT NULL
            RETURN p.id AS id, k.kennwert AS name, k.wert AS wert, coalesce(k.einheit,'') AS einheit""")
        co2_pct, co2_t = {}, {}
        for r in co2:
            nm, unit, val = (r["name"] or "").lower(), (r["einheit"] or "").lower(), float(r["wert"])
            if ("%" in unit or "prozent" in nm or "pct" in nm or ("reduktion" in nm and val <= 100)) and val <= 100:
                co2_pct[r["id"]] = max(co2_pct.get(r["id"], 0.0), val)
            elif unit.startswith("t") or "einsparung_t" in nm:
                co2_t[r["id"]] = max(co2_t.get(r["id"], 0.0), val)
    drv.close()

    entries = load_enrichment()
    results = []
    for r in base:
        pid = r["id"]
        prov = {}
        try:
            area = float(r["area"]) if r["area"] is not None else None
        except Exception:
            area = None
        try:
            yr = int(r["jahr"]) if r["jahr"] is not None else None
        except Exception:
            yr = None
        klasse = r["klasse"][0] if isinstance(r["klasse"], list) and r["klasse"] else r["klasse"]
        for f in ("area", "donors", "reuse_share", "co2_pct", "co2_t", "design", "scope"):
            prov[f] = "graph"

        d = donors.get(pid, 0)
        sh = share.get(pid)
        cpct = co2_pct.get(pid)
        ct = co2_t.get(pid)
        scope = None
        vdq = None

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
            if "reuse_scope" in enr:
                scope = enr["reuse_scope"]; prov["scope"] = "verified"
            if "design_quality" in enr:
                vdq = enr["design_quality"]; prov["design"] = "verified"

        sub = {
            "bezug": score_bezug(d, beschaffung.get(pid, 0)),
            "tiefe": score_tiefe(sh, scope, r["n_tragend"], r["n_bg"]),
            "massstab": score_massstab(area),
            "design": score_design(rev_cnt.get(pid, 0), tot_cnt.get(pid, 0),
                                   pid in nondestruct, pid in has_rueckbau, pid in has_exch,
                                   pid in prefab, levels.get(pid, 0), btyp.get(pid, 0), vdq),
            "reife": score_reife(r["n_kw"], r["lca"], r["zert"], r["n_nw"], r["n_zust"] > 0),
            "wirkung": score_wirkung(cpct, ct),
        }
        num = sum(WEIGHTS[k] * v for k, v in sub.items() if v is not None)
        den = sum(WEIGHTS[k] for k, v in sub.items() if v is not None)
        rsi = round(num / den, 1) if den else 0.0

        results.append({
            "id": pid, "name": r["name"], "land": r["land"], "jahr": yr, "area": area,
            "klasse": klasse, "n_bg": r["n_bg"], "n_tragend": r["n_tragend"], "donors": d,
            "reuse_share": sh, "reuse_scope": scope, "co2_pct": cpct, "co2_t": ct,
            "s_bezug": sub["bezug"], "s_tiefe": sub["tiefe"], "s_massstab": sub["massstab"],
            "s_design": sub["design"], "s_reife": sub["reife"], "s_wirkung": sub["wirkung"],
            "RSI": rsi, "confidence": round(den, 2), "dims": sum(1 for v in sub.values() if v is not None),
            "archetyp": archetype(area, sh, d, sub["design"], cpct),
            "provenance": prov, "verified": bool(enr), "sources": enr_sources,
        })

    results.sort(key=lambda x: (x["RSI"], x["confidence"]), reverse=True)
    for i, r in enumerate(results, 1):
        r["rang"] = i

    (HERE / "project_scalability_scores.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = ["rang", "name", "land", "jahr", "area", "n_bg", "n_tragend", "donors", "reuse_share",
            "reuse_scope", "co2_pct", "co2_t", "s_bezug", "s_tiefe", "s_massstab", "s_design",
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
             "Maßstab | **Design** | Reife | Wirkung | **RSI** | Konf. | Archetyp |",
             "|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|"]
    for r in results:
        nm = r["name"] if len(r["name"]) <= 30 else r["name"][:29] + "…"
        vflag = " ✓" if r["verified"] else ""
        lines.append(
            f"| {r['rang']} | {nm}{vflag} | {r['land'] or '—'} | {fmt(r['jahr'])} | {fmt(r['area'])} | "
            f"{r['donors'] or '—'} | {fmt(r['reuse_share'])} | {fmt(r['s_bezug'])} | {fmt(r['s_tiefe'])} | "
            f"{fmt(r['s_massstab'])} | {fmt(r['s_design'])} | {fmt(r['s_reife'])} | {fmt(r['s_wirkung'])} | "
            f"**{fmt(r['RSI'])}** | {fmt(r['confidence'])} | {r['archetyp']} |")
    (HERE / "_scal_table.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    arche = Counter(r["archetyp"] for r in results)
    print(f"Projekte: {len(results)}  |  verifiziert: {sum(r['verified'] for r in results)}")
    print(f"RSI Median {st.median([r['RSI'] for r in results]):.1f}  "
          f"Max {max(r['RSI'] for r in results):.1f}  Min {min(r['RSI'] for r in results):.1f}")
    print(f"Design-Score vorhanden: {sum(1 for r in results if r['s_design'] is not None)}/{len(results)}")
    print("Archetypen:")
    for a, n in arche.most_common():
        print(f"   {n:>3}  {a}")
    print("\nTop 15:")
    for r in results[:15]:
        print(f"  {r['rang']:>2} {r['name'][:34]:34} RSI {r['RSI']:>5} (k{r['confidence']:.2f}) "
              f"D={r['s_design']} [{r['archetyp']}]")


if __name__ == "__main__":
    main()
