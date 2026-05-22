"""Phase L: extract denormalized ReuseRule/Land payload into edges (reuse existing nodes).

Principles:
  - Reuse existing target nodes; create a new node ONLY when clearly necessary.
  - Map only high-confidence (clear-evidence) equivalences; everything unmatched
    is preserved as a residual array (no data loss).
  - No edge is created without an explicit keyword rule below.

Modes:
  (default)            dry-run: prints summary + writes MAPPING_PREVIEW.md
  --confirm "PHASE_L TO mit-bestand"   live apply
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

PREVIEW_PATH = Path(
    "_neo4j/review/2026-06-01_node_key_clustering/MAPPING_PREVIEW.md"
)

# --- New Schadstoff nodes (recurring, real contaminants with no existing home) ---
NEW_SCHADSTOFF = {
    "s_schimmel": "Schimmel / mikrobielle Kontamination",
    "s_chlorid": "Chloride",
    "s_mineraloel": "Mineraloel-/Oelkontamination",
    "s_salze": "Salze (bauschaedlich)",
}

# --- Keyword -> existing/new node id. A token may match several (set union). ---
POLLUTANT_KW = [
    ("asbest", "s_asbest"),
    ("pcb", "s_pcb"),
    ("pah", "s_pak"), ("tar", "s_pak"),
    ("lead", "s_bleifarbe"),
    ("chromate", "s_schwermetalle"), ("cadmium", "s_schwermetalle"),
    ("heavy metal", "s_schwermetalle"), ("galvanic", "s_schwermetalle"),
    ("creosote", "s_holzschutzmittel"), ("pcp", "s_holzschutzmittel"),
    ("lindane", "s_holzschutzmittel"), ("cca", "s_holzschutzmittel"),
    ("preservative", "s_holzschutzmittel"),
    ("formaldehyde", "s_formaldehyd"),
    ("mold", "s_schimmel"),
    ("chloride", "s_chlorid"),
    ("oil", "s_mineraloel"),
    ("salt", "s_salze"),
]

TEST_KW = [
    ("moisture", "pn_feuchtemessung"),
    ("carbonation", "pn_karbonatisierung"),
    ("chloride", "pn_chlorid"),
    ("petrograph", "pn_petrografie"),
    ("weldab", "pn_schweissbarkeit"),
    ("corrosion", "pn_rostgrad"),
    ("reinforcement", "pn_bewehrungsscan"), ("cover scan", "pn_bewehrungsscan"),
    ("cover", "pn_bewehrungsscan"),
    ("water absorption", "pn_wasseraufnahme"),
    ("slip", "pn_rutschhemmung"),
    ("tensile", "pn_zugversuch"), ("yield", "pn_zugversuch"), ("elongation", "pn_zugversuch"),
    ("charpy", "pn_kerbschlag"),
    ("crack", "pn_risskartierung"),
    ("fire", "pr_brandschutznachweis"),
    ("load test", "pr_statische_nachweisfuehrung"), ("load path", "pr_statische_nachweisfuehrung"),
    ("bending", "pr_statische_nachweisfuehrung"), ("shear", "pr_statische_nachweisfuehrung"),
    ("capacity", "pr_statische_nachweisfuehrung"),
    ("provenance", "pr_dokumentenpruefung_bestand"), ("drawings", "pr_dokumentenpruefung_bestand"),
    ("documentation", "pr_dokumentenpruefung_bestand"), ("document like new", "pr_dokumentenpruefung_bestand"),
    ("visual", "pn_sichtpruefung"),
    ("ndt", "pr_zerstoerungsfreie_pruefung"),
    ("cores", "pn_bohrkern_druckfestigkeit"),
    ("rebound", "pn_rueckprallhammer"),
    ("upv", "pn_ultraschall"),
    ("geometr", "pr_geometrische_vermessung"), ("dimension", "pr_geometrische_vermessung"),
    ("decay", "pn_faeulnis_sichtpruefung"), ("insect", "pn_faeulnis_sichtpruefung"),
    ("biological attack", "pn_faeulnis_sichtpruefung"),
    ("strength grading", "pr_festigkeitssortierung_holz"), ("grade", "pr_festigkeitssortierung_holz"),
    ("mechanical", "pr_materialpruefung"),
    ("density", "pn_dichte"),
    ("strand", "pn_spannlitzenlage"),
    ("anchor", "pn_ankerpruefung"),
    ("flexural", "pn_biegezug"),
    ("compressive strength", "pn_druckfestigkeit"),
]

METHOD_KW = [
    ("de-nail", "av_entnageln"), ("denail", "av_entnageln"), ("nailing", "av_entnageln"),
    ("clean", "av_reinigung"),
    ("shotblast", "av_sandstrahlen"), ("blasting", "av_sandstrahlen"), ("sandblast", "av_sandstrahlen"),
    ("planing", "av_hobeln"), ("plane", "av_hobeln"),
    ("trim", "av_zuschnitt"), ("cut", "av_zuschnitt"), ("saw", "av_zuschnitt"),
    ("drying", "av_holz_trocknung_feuchtekonditionierung"),
    ("sort", "av_materialsortierung_chargenbildung"), ("classif", "av_materialsortierung_chargenbildung"),
    ("batch", "av_materialsortierung_chargenbildung"),
    ("repair", "av_reparatur"),
    ("recoat", "av_korrosionsschutz_beschichten"), ("coating renewal", "av_korrosionsschutz_beschichten"),
    ("decoat", "av_beschichtung_entfernen"), ("coating removal", "av_beschichtung_entfernen"),
    ("mortar removal", "av_moertelentfernung_ziegel"),
    ("crush", "av_lehm_sieben_mischen"), ("sieve", "av_lehm_sieben_mischen"),
    ("rehydrate", "av_lehm_sieben_mischen"), ("reform", "av_lehm_sieben_mischen"),
    ("regrad", "av_holz_festigkeitssortierung"),
    ("recondition", "av_rekonditionierung"),
    ("remanufact", "av_remanufacturing"), ("re-fabrication", "av_remanufacturing"),
    ("dismantl", "av_zerlegung_vereinzelung"), ("deconstruct", "av_zerlegung_vereinzelung"),
    ("salvage", "av_zerlegung_vereinzelung"),
    ("surface prepar", "av_oberflaechenbehandlung"), ("surface protection", "av_oberflaechenbehandlung"),
    ("surface refinish", "av_oberflaechenbehandlung"), ("refinish", "av_oberflaechenbehandlung"),
]

LEGAL_KW = [
    ("cpr", "rb_bauproduktenverordnung_cpr"),
    ("baupg", "rb_schweizer_bauproduktegesetz"),
    ("krwg", "rb_kreislaufwirtschaftsgesetz_krwg"),
    ("dibt", "rb_dibt_zustimmung"),
    ("ukca", "rb_ukca_marking_reused_steel"),
    ("ce marking", "rb_ce_marking_reused_steel"),
    ("passport", "rb_materialpass"), ("materialpass", "rb_materialpass"),
    ("denkmal", "rb_denkmalschutz"), ("heritage", "rb_denkmalschutz"),
    ("listing", "rb_grade_ii_listing"),
]

# array -> (keyword table, relationship type)
ARRAYS = {
    "pollutant_risks": (POLLUTANT_KW, "HAS_RISK_POLLUTANT"),
    "required_tests": (TEST_KW, "HAT_PRUEFUNG"),
    "processing_methods": (METHOD_KW, "HAT_AUFBEREITUNG"),
    "legal_conditions": (LEGAL_KW, "HAT_RECHTLICHE_BEDINGUNG"),
}

# Land pollutant-year keys -> Schadstoff id
LAND_YEAR_MAP = {
    "asbest_verbot_jahr": "s_asbest",
    "pcb_verbot_jahr": "s_pcb",
    "kmf_grenzwert_jahr": "s_kmf",
    "asbest_neshap_year": "s_asbest",
}
LAND_DROP_KEYS = list(LAND_YEAR_MAP.keys()) + ["asbest_note"]
RR_DROP_KEYS = ["material_id", "material", "country_iso", "country_name", "key_norms"]


def match(token: str, table):
    low = token.lower()
    return sorted({tid for kw, tid in table if kw in low})


def compute(rr_rows):
    edges = {rel: [] for _, rel in ARRAYS.values()}
    edges["REFERENZIERT_NORM"] = [{"rule": "rr_de_lehm", "tid": "norm_din_18940_family"}]
    residual = {}  # rule -> {array: [unmatched]}
    preview = {arr: {} for arr in ARRAYS}  # array -> token -> targets
    for row in rr_rows:
        rid = row["id"]
        residual[rid] = {}
        for arr, (table, rel) in ARRAYS.items():
            toks = row.get(arr) or []
            res = []
            for t in toks:
                targets = match(t, table)
                preview[arr].setdefault(t, targets)
                if targets:
                    for tid in targets:
                        edges[rel].append({"rule": rid, "tid": tid})
                else:
                    res.append(t)
            residual[rid][arr] = res
    # dedup edges
    for rel in edges:
        seen, dd = set(), []
        for e in edges[rel]:
            k = (e["rule"], e["tid"])
            if k not in seen:
                seen.add(k)
                dd.append(e)
        edges[rel] = dd
    return edges, residual, preview


def compute_land(land_rows):
    out = []
    for l in land_rows:
        for key, sid in LAND_YEAR_MAP.items():
            yr = l.get(key)
            if yr is not None:
                out.append({"land": l["id"], "sid": sid, "jahr": yr, "basis": key,
                            "note": l.get("asbest_note") if key == "asbest_neshap_year" else None})
    return out


def write_preview(preview, residual, edges, land_edges):
    lines = ["# Phase L mapping preview (review before apply)\n"]
    for arr in ARRAYS:
        rel = ARRAYS[arr][1]
        toks = preview[arr]
        matched = {t: v for t, v in toks.items() if v}
        unmatched = sorted(t for t, v in toks.items() if not v)
        lines.append(f"\n## {arr} -> {rel}  ({len(matched)} tokens mapped, {len(unmatched)} residual)\n")
        for t in sorted(matched):
            lines.append(f"- `{t}` -> {', '.join(matched[t])}")
        if unmatched:
            lines.append(f"\n**Residual (kept as-is, no edge):** {'; '.join(unmatched)}")
    lines.append("\n## Edge totals to MERGE\n")
    for rel, es in edges.items():
        lines.append(f"- {rel}: {len(es)}")
    lines.append(f"- REGULIERT (Land->Schadstoff): {len(land_edges)}")
    lines.append(f"\n## New Schadstoff nodes: {', '.join(NEW_SCHADSTOFF)}\n")
    PREVIEW_PATH.parent.mkdir(parents=True, exist_ok=True)
    PREVIEW_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser()
    ap.add_argument("--confirm", default=None)
    args = ap.parse_args()

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    expected = f"PHASE_L TO {database}"
    live = args.confirm == expected
    if args.confirm and not live:
        raise SystemExit(f"Confirm must equal: {expected!r}")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            rr = [dict(r) for r in session.run(
                "MATCH (r:ReuseRule) RETURN r.id AS id, r.pollutant_risks AS pollutant_risks, "
                "r.required_tests AS required_tests, r.processing_methods AS processing_methods, "
                "r.legal_conditions AS legal_conditions")]
            land = [dict(r) for r in session.run(
                "MATCH (l:Land) RETURN l.id AS id, l.asbest_verbot_jahr AS asbest_verbot_jahr, "
                "l.pcb_verbot_jahr AS pcb_verbot_jahr, l.kmf_grenzwert_jahr AS kmf_grenzwert_jahr, "
                "l.asbest_neshap_year AS asbest_neshap_year, l.asbest_note AS asbest_note")]

            edges, residual, preview = compute(rr)
            land_edges = compute_land(land)
            write_preview(preview, residual, edges, land_edges)

            summary = {
                "mode": "live" if live else "dry-run",
                "edge_counts": {rel: len(es) for rel, es in edges.items()},
                "reguliert_edges": len(land_edges),
                "new_schadstoff": list(NEW_SCHADSTOFF),
                "residual_token_total": sum(len(v) for r in residual.values() for v in r.values()),
            }

            if live:
                # 1. new Schadstoff
                session.run(
                    "UNWIND $rows AS row MERGE (s:Schadstoff {id: row.id}) "
                    "ON CREATE SET s.name = row.name",
                    rows=[{"id": k, "name": v} for k, v in NEW_SCHADSTOFF.items()],
                ).consume()
                # 2. array edges (+ the one norm edge)
                rel_label = {
                    "HAS_RISK_POLLUTANT": "Schadstoff", "HAT_PRUEFUNG": "PruefungNachweis",
                    "HAT_AUFBEREITUNG": "Aufbereitungsverfahren",
                    "HAT_RECHTLICHE_BEDINGUNG": "RechtlicheBedingung", "REFERENZIERT_NORM": "Norm",
                }
                for rel, es in edges.items():
                    if not es:
                        continue
                    session.run(
                        f"UNWIND $rows AS row MATCH (r:ReuseRule {{id: row.rule}}) "
                        f"MATCH (t:`{rel_label[rel]}` {{id: row.tid}}) MERGE (r)-[:`{rel}`]->(t)",
                        rows=es,
                    ).consume()
                # 3. residual arrays
                session.run(
                    "UNWIND $rows AS row MATCH (r:ReuseRule {id: row.id}) "
                    "SET r.pollutant_risks = row.pr, r.required_tests = row.rt, "
                    "r.processing_methods = row.pm, r.legal_conditions = row.lc",
                    rows=[{"id": rid, "pr": d["pollutant_risks"], "rt": d["required_tests"],
                           "pm": d["processing_methods"], "lc": d["legal_conditions"]}
                          for rid, d in residual.items()],
                ).consume()
                # remove now-empty residual arrays + fully-captured keys
                for arr in list(ARRAYS) :
                    session.run(f"MATCH (r:ReuseRule) WHERE r.`{arr}` = [] REMOVE r.`{arr}`").consume()
                session.run(
                    "MATCH (r:ReuseRule) REMOVE " + ", ".join(f"r.`{k}`" for k in RR_DROP_KEYS)
                ).consume()
                # 4. Land REGULIERT + drop year keys
                session.run(
                    "UNWIND $rows AS row MATCH (l:Land {id: row.land}) MATCH (s:Schadstoff {id: row.sid}) "
                    "MERGE (l)-[rel:REGULIERT]->(s) SET rel.jahr = row.jahr, rel.basis = row.basis, "
                    "rel.note = row.note",
                    rows=land_edges,
                ).consume()
                session.run(
                    "MATCH (l:Land) REMOVE " + ", ".join(f"l.`{k}`" for k in LAND_DROP_KEYS)
                ).consume()
                summary["applied"] = True

            print(json.dumps(summary, indent=2))
    finally:
        driver.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
