"""Connect live anchors (Material, Bauteilgruppe, Bauteiltyp, Projekt, Bauwerk) to the new
regulation vocabulary -- WITH EVIDENCE, derived from factual anchor attributes only.

Refined (round 7) so a Bauteilgruppe's connections are accurate, not just "has material X":
  - STRUCTURAL GATING: structural rules (Standsicherheit, EN 1090, Eurocodes, in-situ tests…)
    are applied only to load-bearing components. Uses live `tragend` (True/False); if unknown,
    inferred from Bauteiltyp (Träger/Stütze/Decke… = structural; Fassade/Fenster/Tür/Dämmung/
    Ausbau… = non-structural). A tragend=False façade no longer draws Standsicherheitsnachweis.
  - COMPONENT-SPECIFIC RULES: a Bauteilgruppe/-typ gets the product standard for its TYPE via
    live HAT_BAUTEILTYP + TYPE_BY_RW (Fenster→EN 14351, Fassade→EN 13830, Hohlkörperdecke→EN
    1168, Treppe→DIN 18065, Mauerstein→EN 771, …). This is the "specific Regelwerk per Bauteil".
  - COMPOSITES: groups with >=3 materials / mg_verbundstoff / mat_mehrere are flagged Verbund;
    each material rule is down-weighted (material is only a fraction) and a disassembly/separation
    question (rf_rueckbau via ISO 20887) is added.

Edge types per (anchor, rule): TRIGGERS_REGULIERUNGSFRAGE, ERFORDERT_NACHWEIS, UNTERLIEGT_REGELWERK.
Reads the live graph read-only; writes anchor_edges.csv + anchor_edges.jsonl. No DB writes.
"""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from pathlib import Path

from neo4j import GraphDatabase

from build_vocabulary_graph import REGELWERK, MAT_BY_RW, TYPE_BY_RW, expand_land, RUN

OUT = Path(__file__).resolve().parent
URI, USER, PWD, DB = "bolt://localhost:7687", "neo4j", "ENTWERFENMITBESTAND", "mit-bestand"
RW = {rw["id"]: rw for rw in REGELWERK}

# Project-level rules, split by the project CONTEXT they require (not just jurisdiction):
AUDIT_DECON_RW = {  # need a deconstruction/Rückbau context
    "rw_fr_pemd", "rw_oenorm_b3151", "rw_no_tek17", "rw_be_tracimat_regional", "rw_gewabfv",
    "rw_vob_c_din_18459", "rw_vdi_6210", "rw_eu_cdw_protocol", "rw_din_spec_91484",
    "rw_krwg", "rw_eu_wfd_2008_98",
}
NEWBUILD_ENERGY_RW = {  # need a new-build / renovation (energy-performance) context
    "rw_fr_re2020", "rw_geg", "rw_ch_muken", "rw_sia_380_1", "rw_nl_mpg",
}
BROAD_REUSE_RW = {  # circular-economy / passport / certification frameworks: any reuse project
    "rw_eu_taxonomy", "rw_eu_levels", "rw_espr_dpp", "rw_madaster_grp", "rw_qng_dgnb",
    "rw_iso_20887", "rw_din_spec_91525", "rw_uk_pas2080", "rw_fr_rep_pmcb", "rw_nl_bbl", "rw_dk_br18",
}
PROJEKT_LEVEL_RW = AUDIT_DECON_RW | NEWBUILD_ENERGY_RW | BROAD_REUSE_RW

DECON_INTERVENTIONS = {"bai_rueckbau", "bai_umbau", "bai_sanierung", "bai_umnutzung", "bai_translozierung"}
DECON_PHASES = {"phase_rueckbau", "phase_aufbereitung", "phase_identifikation", "phase_lagerung", "phase_transport"}
BUILD_INTERVENTIONS = {"bai_neubau", "bai_erweiterung", "bai_aufstockung", "bai_wiederaufbau", "bai_umbau", "bai_sanierung"}
PUBLIC_NUTZUNG = {"nut_schule_bildung", "nut_kultur", "nut_gewerbe", "nut_infrastruktur", "nut_sozialbau", "nut_buero"}
# Rules that only apply to load-bearing components:
STRUCTURAL_RW = {
    "rw_cen_ts_1090_201", "rw_en_1090", "rw_en_1090_2_bolts_reuse", "rw_sci_p427", "rw_nta_8713",
    "rw_eurocodes_en_1990_1999", "rw_en_iso_6892", "rw_din_4074_en_14081", "rw_en_408",
    "rw_en_13791_12504", "rw_sia_269", "rw_sia_269_2", "rw_dafstb_rc_beton", "rw_fib_precast_reuse",
    "rw_en_1168", "rw_en_1992_4", "rw_nen_8700", "rw_cen_ts_17440",
}
STRUCT_TYPES = {"bt_traeger", "bt_stuetze", "bt_decke", "bt_hohlkoerperdecke", "bt_fundament",
                "bt_treppe", "bt_mauerstein", "bt_fassadenelement_beton"}
NONSTRUCT_TYPES = {"bt_fassade", "bt_fassadenelement", "bt_fassadenmodul_mauerwerk", "bt_fenster",
                   "bt_tuer", "bt_verglasung", "bt_glasscheibe", "bt_daemmung", "bt_ausbau",
                   "bt_boden", "bt_gelaender", "bt_technik"}
ERA_POLLUTANT = {"era_vor_1900", "era_1900_1945", "era_nachkrieg_1945_1970", "era_1970_1990", "era_1990_2000"}


def mat_rules():
    idx = defaultdict(list)
    for rw in REGELWERK:
        for m in MAT_BY_RW.get(rw["id"], []):
            idx[m].append(rw)
    return idx


def type_rules():
    idx = defaultdict(list)
    for rw_id, types in TYPE_BY_RW.items():
        for t in types:
            idx[t].append(RW[rw_id])
    return idx


def structural_relevance(tragend, types):
    if tragend is True:
        return "yes"
    if tragend is False:
        return "no"
    types = set(types or [])
    if types & STRUCT_TYPES:
        return "yes"
    if types and types <= NONSTRUCT_TYPES:
        return "no"
    return "unknown"


def main():
    MR, TR = mat_rules(), type_rules()
    drv = GraphDatabase.driver(URI, auth=(USER, PWD))
    raw = []  # (from_id, label, edge_type, to_id, rw_id, url, quote, reason, conf)

    def emit(anchor_id, label, factor, reason, rw, skip_struct=False, struct_unknown=False):
        if skip_struct and rw["id"] in STRUCTURAL_RW:
            return
        f = factor
        r = reason
        if struct_unknown and rw["id"] in STRUCTURAL_RW:
            f *= 0.85
            r += " [tragend unbekannt -> strukturelle Relevanz zu pruefen]"
        c = round(rw["conf"] * f, 2)
        for rf in rw["rf"]:
            raw.append((anchor_id, label, "TRIGGERS_REGULIERUNGSFRAGE", rf, rw["id"], rw["url"], rw["quote"], r, c))
        for nf in rw["nf"]:
            raw.append((anchor_id, label, "ERFORDERT_NACHWEIS", nf, rw["id"], rw["url"], rw["quote"], r, c))
        raw.append((anchor_id, label, "UNTERLIEGT_REGELWERK", rw["id"], rw["id"], rw["url"], rw["quote"], r, c))

    def juris_gate(rw, comp_lands):
        """National rules apply only in their jurisdiction. Returns (ok, note)."""
        if "EU" in rw["land"]:
            return True, ""
        rule_lands = set(expand_land(rw["land"]))
        if not comp_lands:
            return True, " [Projekt-Land unbekannt -> Geltung zu pruefen]"
        if comp_lands & rule_lands:
            return True, ""
        return False, ""  # national rule, component is elsewhere -> not the governing law

    with drv.session(database=DB) as s:
        live_mats = {r["id"] for r in s.run("MATCH (m:Material) RETURN m.id AS id")}
        # component country via its project(s) -- for jurisdiction gating of material/type rules
        bg_land = defaultdict(set)
        for r in s.run("MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(b:Bauteilgruppe) "
                       "OPTIONAL MATCH (p)-[:LIEGT_IN_LAND]->(l:Land) "
                       "OPTIONAL MATCH (p)-[:LIEGT_IN_STADT]->(:Stadt)-[:LIEGT_IN_LAND]->(l2:Land) "
                       "RETURN b.id AS b, collect(DISTINCT l.id)+collect(DISTINCT l2.id) AS lands"):
            bg_land[r["b"]] |= {x for x in r["lands"] if x}

        # 1. Material (direct, no structural gating -- material rules are intrinsic)
        for mat, rules in MR.items():
            if mat in live_mats:
                for rw in rules:
                    emit(mat, "Material", 1.0, f"Material '{mat}' wird durch {rw['id']} ({rw['name']}) geregelt", rw)

        # 2. Bauteilgruppe: materials (gated) + composite + component-type rules
        recs = s.run(
            "MATCH (b:Bauteilgruppe) "
            "OPTIONAL MATCH (b)-[:NUTZT_MATERIAL]->(m:Material) "
            "OPTIONAL MATCH (b)-[:HAT_BAUTEILTYP]->(bt:Bauteiltyp) "
            "OPTIONAL MATCH (b)-[:HAT_MATERIALGRUPPE]->(mg:Materialgruppe) "
            "RETURN b.id AS bg, b.tragend AS tragend, collect(DISTINCT m.id) AS mats, "
            "collect(DISTINCT bt.id) AS types, collect(DISTINCT mg.id) AS mgs")
        for r in recs:
            bg, mats, types, mgs = r["bg"], [m for m in r["mats"] if m], [t for t in r["types"] if t], r["mgs"]
            tragend = r["tragend"] if isinstance(r["tragend"], bool) else None
            rel = structural_relevance(tragend, types)
            skip_struct = rel == "no"
            unknown = rel == "unknown"
            composite = len(mats) >= 3 or "mat_mehrere" in mats or any(g in ("mg_verbundstoff", "mg_mehrere") for g in mgs if g)
            comp_lands = bg_land.get(bg, set())
            # 2a. material rules (structural ones gated by tragend; national rules gated by country)
            for mat in mats:
                for rw in MR.get(mat, []):
                    ok, jnote = juris_gate(rw, comp_lands)
                    if not ok:
                        continue
                    base = 0.95 * (0.78 if composite else 1.0)
                    reason = f"Bauteilgruppe nutzt Material '{mat}' (live NUTZT_MATERIAL); {rw['id']} regelt '{mat}'"
                    if composite:
                        reason += " [Verbundbauteil: Material nur Teilfraktion]"
                    emit(bg, "Bauteilgruppe", base, reason + jnote, rw, skip_struct=skip_struct, struct_unknown=unknown)
            # 2b. component-type product standards (national ones gated by country)
            for t in types:
                for rw in TR.get(t, []):
                    ok, jnote = juris_gate(rw, comp_lands)
                    if not ok:
                        continue
                    emit(bg, "Bauteilgruppe", 0.97,
                         f"Bauteilgruppe ist Bauteiltyp '{t}' (live HAT_BAUTEILTYP); {rw['id']} ist die Produktnorm dafuer" + jnote, rw)
            # 2c. composite -> disassembly/separation question (ISO 20887)
            if composite:
                emit(bg, "Bauteilgruppe", 0.8,
                     f"Verbundbauteil ({len(mats)} Materialien) -> Trennbarkeit/Rueckbau erforderlich", RW["rw_iso_20887"])

        # 3. Bauteiltyp: ONLY its genuine component product standard(s). No material-via-parent
        #    bleed (a window-group bundling brick must not give the window EN 771).
        for r in s.run("MATCH (bt:Bauteiltyp) RETURN bt.id AS bt"):
            bt = r["bt"]
            for rw in TR.get(bt, []):
                emit(bt, "Bauteiltyp", 0.95, f"Bauteiltyp '{bt}': {rw['id']} ist die Produktnorm fuer diesen Bauteiltyp", rw)

        # 4. Projekt: jurisdiction AND context (intervention / phase / nutzung / Bauwerk-era)
        proj_land = defaultdict(set)
        for q in ("MATCH (p:Projekt)-[:LIEGT_IN_LAND]->(l:Land) RETURN p.id AS p, l.id AS l",
                  "MATCH (p:Projekt)-[:LIEGT_IN_STADT]->(:Stadt)-[:LIEGT_IN_LAND]->(l:Land) RETURN p.id AS p, l.id AS l"):
            for r in s.run(q):
                proj_land[r["p"]].add(r["l"])

        def ctx(rel, tgt):
            d = defaultdict(set)
            for r in s.run(f"MATCH (p:Projekt)-[:{rel}]->(x:{tgt}) RETURN p.id AS p, x.id AS x"):
                d[r["p"]].add(r["x"])
            return d
        p_interv, p_phase, p_nutz = ctx("HAT_INTERVENTION", "BauaufgabeIntervention"), ctx("HAT_PROZESSPHASE", "Prozessphase"), ctx("HAT_NUTZUNG", "Nutzung")
        p_era = defaultdict(set)
        for r in s.run("MATCH (p:Projekt)-[:HAS_BAUWERK]->(:Bauwerk)-[]->(e:BauwerkEra) RETURN p.id AS p, e.id AS e"):
            p_era[r["p"]].add(r["e"])

        for p, lands in proj_land.items():
            interv, phase, nutz = p_interv.get(p, set()), p_phase.get(p, set()), p_nutz.get(p, set())
            has_decon = bool(interv & DECON_INTERVENTIONS or phase & DECON_PHASES)
            has_build = bool(interv & BUILD_INTERVENTIONS)
            interv_known = bool(interv or phase)
            for rw_id in PROJEKT_LEVEL_RW:
                rw = RW[rw_id]
                hit = lands & set(expand_land(rw["land"]))
                if not hit:
                    continue
                if rw_id in AUDIT_DECON_RW:
                    if has_decon:
                        fac, note, ctxt = 1.0, "", f"Rückbau-/Bestandskontext ({sorted(interv & DECON_INTERVENTIONS or phase & DECON_PHASES)})"
                    elif not interv_known:
                        fac, note, ctxt = 0.8, " [Intervention unbekannt -> Rückbaukontext zu pruefen]", "Kontext unbekannt"
                    else:
                        continue  # explicit non-deconstruction (e.g. reiner Neubau) -> skip
                elif rw_id in NEWBUILD_ENERGY_RW:
                    if has_build:
                        fac, note, ctxt = 1.0, "", f"Neubau-/Umbaukontext ({sorted(interv & BUILD_INTERVENTIONS)})"
                    elif not interv_known:
                        fac, note, ctxt = 0.8, " [Intervention unbekannt]", "Kontext unbekannt"
                    else:
                        continue
                else:  # BROAD_REUSE_RW
                    fac, note, ctxt = 1.0, "", "Reuse-Projekt"
                emit(p, "Projekt", fac,
                     f"Projekt in {sorted(hit)}; {ctxt}; {rw['id']} gilt{note}", rw)

            # Schadstoff only when deconstructing an existing building of a pollutant-era
            eras = p_era.get(p, set()) & ERA_POLLUTANT
            if has_decon and eras and (lands & set(expand_land(RW["rw_gefstoffv"]["land"]))):
                emit(p, "Projekt", 0.8,
                     f"Rückbau/Sanierung eines Bauwerks der Era {sorted(eras)} (live HAS_BAUWERK) -> Schadstoffermittlung", RW["rw_gefstoffv"])
            # Accessibility only for public-use new-build/renovation (DE)
            if has_build and (nutz & PUBLIC_NUTZUNG) and (lands & set(expand_land(RW["rw_din_18040"]["land"]))):
                emit(p, "Projekt", 0.75,
                     f"Öffentliche Nutzung {sorted(nutz & PUBLIC_NUTZUNG)} + Neubau/Umbau -> Barrierefreiheit", RW["rw_din_18040"])

        # 5. Bauwerk via era -> Schadstoff
        gef = RW["rw_gefstoffv"]
        for r in s.run("MATCH (bw:Bauwerk)-[]->(e:BauwerkEra) RETURN bw.id AS bw, collect(DISTINCT e.id) AS eras"):
            eras = [e for e in r["eras"] if e in ERA_POLLUTANT]
            if eras:
                emit(r["bw"], "Bauwerk", 0.82, f"Bauwerk-Era {eras} -> typische Schadstoffe (graph TYPISCH_BEI_ERA)", gef)
    drv.close()

    best, support = {}, defaultdict(set)
    for e in raw:
        key = (e[0], e[2], e[3])
        support[key].add(e[4])
        if key not in best or e[8] > best[key][8]:
            best[key] = e

    cols = ["from_node_id", "from_label", "edge_type", "to_node_id", "evidence_status",
            "source_url", "source_quote", "applicability_reason", "support_rules", "confidence", "review_run"]
    rows = [[e[0], e[1], e[2], e[3], "rule_derived", e[5], e[6], e[7], len(support[key]), e[8], RUN]
            for key, e in best.items()]
    rows.sort(key=lambda r: (r[1], r[2], r[0], r[3]))

    with (OUT / "anchor_edges.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh); w.writerow(cols); w.writerows(rows)
    with (OUT / "anchor_edges.jsonl").open("w", encoding="utf-8") as fh:
        for row in rows:
            fh.write(json.dumps(dict(zip(cols, row)), ensure_ascii=False) + "\n")

    from collections import Counter
    print(f"anchor edges (deduped): {len(rows)}")
    print(f"  by edge_type: {dict(Counter(r[2] for r in rows))}")
    print(f"  by anchor label: {dict(Counter(r[1] for r in rows))}")
    print(f"  distinct anchors: {len({r[0] for r in rows})}")


if __name__ == "__main__":
    main()
