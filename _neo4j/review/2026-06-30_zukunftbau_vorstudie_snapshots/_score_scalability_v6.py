"""Reuse-Scalability Index v6 — gates, K1-K14, confidence, archetypes.

Reads v3 dimension scores from project_scalability_scores.json as proxy base.
Verified overrides from verified_enrichment_v6.json (+ verified_enrichment.json metadata).

Writes: project_scalability_scores_v6.json / .csv, _scal_table_v6.md
"""
from __future__ import annotations

import csv
import json
import statistics as st
import sys
from collections import Counter
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

HERE = Path(__file__).resolve().parent

WEIGHTS = {
    "K1": 0.09, "K2": 0.10, "K3": 0.10, "K4": 0.12, "K5": 0.09, "K6": 0.09,
    "K7": 0.07, "K8": 0.07, "K9": 0.08, "K10": 0.06, "K11": 0.05, "K12": 0.04,
    "K13": 0.03, "K14": 0.01,
}
CRITERIA = list(WEIGHTS.keys())
GATES = [f"G{i}" for i in range(1, 7)]

ORGANISATIONAL_MATCHES = ("Grande Halle", "Green House", "Härmälän", "Circl", "CRCLR")


def clamp(x: float, lo: float = 0.0, hi: float = 4.0) -> int:
    return int(max(lo, min(hi, round(x))))


def score_to_raw(score: float | None, default: int = 1) -> int:
    if score is None:
        return default
    return clamp(score / 25.0)


def split_reife_raw(reife: float | None) -> tuple[int, int]:
    if reife is None:
        return 1, 1
    k3 = clamp(reife * 0.6 / 25.0)
    k4 = clamp(reife * 0.4 / 25.0)
    return max(k3, 1), max(k4, 1)


def load_json(name: str) -> dict:
    return json.loads((HERE / name).read_text(encoding="utf-8"))


def match_v6(name: str, entries: list) -> dict | None:
    low = (name or "").lower()
    for e in entries:
        if e["match"].lower() in low:
            return e
    return None


def proxy_criteria(row: dict) -> tuple[dict[str, dict], str]:
    """Derive K1-K14 raw + evidence from v3 dimension scores."""
    bezug = row.get("s_bezug")
    tiefe = row.get("s_tiefe")
    massstab = row.get("s_massstab")
    design = row.get("s_design")
    reife = row.get("s_reife")
    wirkung = row.get("s_wirkung")
    donors = row.get("donors") or 0
    n_tragend = row.get("n_tragend") or 0
    verified = row.get("verified", False)
    name = row.get("name") or ""
    scope = row.get("reuse_scope") or ""

    k3r, k4r = split_reife_raw(reife)
    if n_tragend > 0 and not verified:
        k4r = min(k4r, 1)

    k2r = score_to_raw(bezug, 1 if donors < 2 else 2)
    if donors >= 5:
        k2r = max(k2r, 3)
    elif donors >= 3:
        k2r = max(k2r, 2)

    k10r = score_to_raw(tiefe, 1)
    k9r = score_to_raw(design, 1)
    k14r = score_to_raw(wirkung, 1)
    k6r = clamp(((score_to_raw(bezug, 1) + score_to_raw(reife, 1)) / 2))
    k8r = score_to_raw(massstab, 2)
    k12r = 3 if donors >= 5 else (2 if donors >= 2 else 1)
    k13r = 3 if donors >= 5 else (2 if design and design >= 65 else 1)

    k1r = 2 if row.get("reuse_share") else 1
    k5r = 2 if verified and n_tragend == 0 else 1
    k7r = 2 if any(m in name for m in ORGANISATIONAL_MATCHES) else 1
    k11r = 2

    if scope == "temporary_borrowed":
        k13r = 1
        k7r = min(k7r, 1)

    ev = 2 if verified else 1
    crit = {}
    for k, raw in zip(
        CRITERIA,
        [k1r, k2r, k3r, k4r, k5r, k6r, k7r, k8r, k9r, k10r, k11r, k12r, k13r, k14r],
    ):
        crit[k] = {"raw": raw, "evidence": ev, "provenance": "proxy_v3"}

    profile = "whole_building_project"
    if scope in ("single_gewerk", "interior_fitout"):
        profile = "interior_fitout_reuse"
    elif scope == "structural" or n_tragend > 2:
        profile = "structural_reuse"
    elif scope == "temporary_borrowed":
        profile = "temporary_or_exhibition"

    return crit, profile


def derive_gates(crit: dict[str, dict], row: dict, profile: str) -> dict[str, int]:
    n_tragend = row.get("n_tragend") or 0
    scope = row.get("reuse_scope") or ""
    cross_project = scope not in ("temporary_borrowed",) and row.get("donors", 0) != 1

    g = {
        "G1": 2 if crit["K1"]["raw"] >= 3 else (1 if crit["K1"]["raw"] >= 2 else 0),
        "G2": 2 if crit["K3"]["raw"] >= 3 else (1 if crit["K3"]["raw"] >= 2 else 0),
        "G3": 2 if crit["K4"]["raw"] >= 3 else (1 if crit["K4"]["raw"] >= 2 else 0),
        "G4": 2 if crit["K5"]["raw"] >= 3 else (1 if crit["K5"]["raw"] >= 2 else 0),
        "G5": 2 if crit["K6"]["raw"] >= 3 else (1 if crit["K6"]["raw"] >= 2 else 0),
        "G6": 2 if crit["K7"]["raw"] >= 3 else (1 if crit["K7"]["raw"] >= 2 else 0),
    }
    if n_tragend > 0 and crit["K4"]["raw"] < 2:
        g["G3"] = min(g["G3"], 1)
        if not row.get("verified"):
            g["G3"] = 0
    if n_tragend > 0 and crit["K5"]["raw"] < 2:
        g["G4"] = min(g["G4"], 1)
    if cross_project and crit["K6"]["raw"] <= 1:
        g["G5"] = 0
    return g


def apply_gate_cap(rsi_brutto: float, gates: dict[str, int], row: dict) -> float:
    n_tragend = row.get("n_tragend") or 0
    zeros = sum(1 for v in gates.values() if v == 0)
    final = rsi_brutto
    if zeros >= 2:
        final = min(final, 39.0)
    elif zeros == 1:
        final = min(final, 59.0)
    if n_tragend > 0 and (gates.get("G3") == 0 or gates.get("G4") == 0):
        final = min(final, 39.0)
    scope = row.get("reuse_scope") or ""
    if scope not in ("temporary_borrowed",) and gates.get("G5") == 0:
        final = min(final, 59.0)
    return round(final, 1)


def compute_rsi(crit: dict[str, dict]) -> float:
    num = sum(WEIGHTS[k] * crit[k]["raw"] * 25 for k in CRITERIA)
    return round(num, 1)


def compute_confidence(crit: dict[str, dict]) -> tuple[float, str]:
    num = sum(WEIGHTS[k] * crit[k]["evidence"] / 3.0 for k in CRITERIA)
    conf = round(num, 2)
    if conf < 0.60:
        cls = "C"
    elif conf < 0.80:
        cls = "B"
    else:
        cls = "A"
    return conf, cls


def einstufung(rsi_final: float) -> str:
    if rsi_final < 40:
        return "Einzelfall / Fallstudie"
    if rsi_final < 60:
        return "Pilot / Reallabor"
    if rsi_final < 75:
        return "bedingt skalierbar"
    if rsi_final < 90:
        return "skalierbar"
    return "systemisch skalierbar"


def archetype_v6(crit: dict[str, dict], row: dict, profile: str) -> str:
    k = {c: crit[c]["raw"] for c in CRITERIA}
    area = row.get("area") or 0
    donors = row.get("donors") or 0

    if k["K2"] >= 3 and k["K3"] >= 3 and k["K6"] >= 3 and k["K12"] >= 3 and k["K13"] >= 3:
        return "Systemischer Aggregator"
    if profile == "material_hub_platform":
        return "Professioneller ReUse-Hub / Plattform"
    if profile == "network_ecosystem":
        return "Netzwerk-/Ökosystem-Enabler"
    if profile == "structural_reuse" and k["K4"] >= 3 and k["K5"] >= 3 and k["K6"] >= 3:
        return "Regulatorisch reifer Struktur-ReUse"
    if k["K9"] == 4:
        return "DfD-Systemreferenz"
    if area >= 5000 and (k["K10"] >= 3 or k["K14"] >= 3 or k["K9"] >= 3):
        return "Großmaßstab-Demonstrator"
    if k["K10"] >= 3 and k["K2"] <= 2:
        return "Tiefen-Pilot"
    if profile == "interior_fitout_reuse":
        return "Innenausbau-/Finish-ReUse"
    if k["K12"] >= 3 and k["K11"] >= 3 and k["K10"] <= 2:
        return "Netzwerk-/Ökosystem-Enabler"
    if area and area < 500:
        return "Klein-Pilot / Reallabor"
    if donors >= 5:
        return "Professioneller ReUse-Hub / Plattform"
    return "Fallstudie"


def main() -> None:
    v3_rows = json.loads((HERE / "project_scalability_scores.json").read_text(encoding="utf-8"))
    v6_enr = load_json("verified_enrichment_v6.json")["entries"]
    base_enr = load_json("verified_enrichment.json")["entries"]

    results = []
    for row in v3_rows:
        v6 = match_v6(row["name"], v6_enr)
        base = match_v6(row["name"], base_enr)

        if v6 and "criteria" in v6:
            crit = {
                k: {
                    "raw": v6["criteria"][k]["raw"],
                    "evidence": v6["criteria"][k]["evidence"],
                    "provenance": "verified_v6",
                }
                for k in CRITERIA
            }
            profile = v6.get("profile", "whole_building_project")
            gates = dict(v6.get("gates", {}))
            verified = True
        else:
            crit, profile = proxy_criteria(row)
            gates = derive_gates(crit, row, profile)
            verified = bool(row.get("verified"))

        rsi_brutto = compute_rsi(crit)
        rsi_final = apply_gate_cap(rsi_brutto, gates, row)
        conf, conf_cls = compute_confidence(crit)
        arch = archetype_v6(crit, row, profile)
        einst = einstufung(rsi_final)

        out = {
            "id": row["id"],
            "name": row["name"],
            "land": row.get("land"),
            "jahr": row.get("jahr"),
            "area": row.get("area"),
            "donors": row.get("donors"),
            "reuse_share": row.get("reuse_share"),
            "reuse_scope": row.get("reuse_scope"),
            "n_tragend": row.get("n_tragend"),
            "profile": profile,
            "gates": gates,
            "RSI_brutto": rsi_brutto,
            "RSI_final": rsi_final,
            "RSI_v3_historical": row.get("RSI"),
            "confidence": conf,
            "confidence_class": conf_cls,
            "einstufung": einst,
            "archetyp": arch,
            "verified": verified,
            "sources": row.get("sources") or (base or {}).get("sources", []),
        }
        for k in CRITERIA:
            out[f"{k}_raw"] = crit[k]["raw"]
            out[f"{k}_norm"] = crit[k]["raw"] * 25
            out[f"{k}_evidence"] = crit[k]["evidence"]
            out[f"{k}_prov"] = crit[k]["provenance"]
        results.append(out)

    results.sort(key=lambda x: (x["RSI_final"], x["confidence"]), reverse=True)
    for i, r in enumerate(results, 1):
        r["rang"] = i

    (HERE / "project_scalability_scores_v6.json").write_text(
        json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")

    cols = ["rang", "name", "land", "RSI_final", "RSI_brutto", "RSI_v3_historical",
            "confidence", "confidence_class", "einstufung", "archetyp", "profile", "verified"]
    cols += [f"{k}_raw" for k in CRITERIA]
    cols += [f"G{i}" for i in range(1, 7)]
    with (HERE / "project_scalability_scores_v6.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in results:
            flat = dict(r)
            for g in GATES:
                flat[g] = r["gates"].get(g)
            w.writerow(flat)

    lines = [
        "| # | Projekt | Land | RSI final | RSI brutto | Konf. | Klasse | Einstufung | Archetyp | K2 | K3 | K4 | K9 |",
        "|---:|---|---|---:|---:|---:|---|---|---|---:|---:|---:|---:|",
    ]
    for r in results:
        nm = r["name"] if len(r["name"]) <= 28 else r["name"][:27] + "…"
        vf = " ✓" if r["verified"] else ""
        lines.append(
            f"| {r['rang']} | {nm}{vf} | {r['land'] or '—'} | **{r['RSI_final']}** | {r['RSI_brutto']} | "
            f"{r['confidence']} | {r['confidence_class']} | {r['einstufung']} | {r['archetyp']} | "
            f"{r['K2_raw']} | {r['K3_raw']} | {r['K4_raw']} | {r['K9_raw']} |"
        )
    (HERE / "_scal_table_v6.md").write_text("\n".join(lines) + "\n", encoding="utf-8")

    med = st.median([r["RSI_final"] for r in results])
    arch = Counter(r["archetyp"] for r in results)
    agg = sum(1 for r in results if r["K2_raw"] >= 3)
    gate0 = sum(1 for r in results if any(r["gates"][g] == 0 for g in GATES))

    summary = {
        "version": "v6",
        "n_projects": len(results),
        "n_verified": sum(1 for r in results if r["verified"]),
        "median_rsi_final": round(med, 1),
        "max_rsi_final": max(r["RSI_final"] for r in results),
        "min_rsi_final": min(r["RSI_final"] for r in results),
        "k2_ge_3": agg,
        "projects_with_gate_zero": gate0,
        "archetypes": dict(arch.most_common()),
        "confidence_classes": dict(Counter(r["confidence_class"] for r in results)),
    }
    (HERE / "scalability_v6_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"Projekte: {len(results)} | verifiziert: {summary['n_verified']}")
    print(f"RSI final Median {med:.1f} | Max {summary['max_rsi_final']} | Min {summary['min_rsi_final']}")
    print(f"K2≥3 (Versorgung): {agg} | mind. ein Gate=0: {gate0}")
    print("Archetypen:", arch.most_common(5))
    print("\nTop 10:")
    for r in results[:10]:
        print(f"  {r['rang']:>2} {r['name'][:36]:36} final {r['RSI_final']:>5} "
              f"(k{r['confidence']:.2f}) [{r['archetyp']}]")


if __name__ == "__main__":
    main()
