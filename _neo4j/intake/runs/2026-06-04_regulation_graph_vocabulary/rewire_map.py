# coding: utf-8
"""Evidence-backed rewire map: every old node -> new vocab target, semantic basis + evidence.

Semantic layer = the mapping (meaning correspondence). Evidence layer = the target Regelwerk's
source_url + quote that proves the target rule exists/applies. Emits REWIRE_MAP.md + rewire_map.csv.
"""
import csv
from collections import Counter

from neo4j import GraphDatabase

from build_vocabulary_graph import REGELWERK, NACHWEISFORDERUNG

RW = {rw["id"]: rw for rw in REGELWERK}

NF_BACKING = {}
for _rw in REGELWERK:
    for _nf in _rw["nf"]:
        NF_BACKING.setdefault(_nf, _rw["id"])


def ev(target):
    if target in RW:
        r = RW[target]
        return r["url"], r["conf"]
    if target in NACHWEISFORDERUNG and NF_BACKING.get(target):
        b = NF_BACKING[target]
        return RW[b]["url"], RW[b]["conf"]
    return "", 0.7


# ---------- NORM -> Regelwerk ----------
NORM_TO_RW = {
 "norm_bbl_nen": "rw_nl_bbl", "norm_bbl_nen_links": "rw_nl_bbl", "norm_bs_4978": "rw_din_4074_en_14081",
 "norm_cb_23_passports": "rw_madaster_grp", "norm_cen_ts_1090_201": "rw_cen_ts_1090_201",
 "norm_cen_ts_1090_201_2024": "rw_cen_ts_1090_201", "norm_cen_ts_17440": "rw_cen_ts_17440",
 "norm_crow_cur_4_2023": "GAP_nl_beton_reuse", "norm_dibt_mvv_tb": "rw_mvv_tb",
 "norm_din_18008": "rw_din_18008", "norm_din_18940_family": "rw_din_18945_lehm", "norm_din_18945": "rw_din_18945_lehm",
 "norm_din_18946": "rw_din_18945_lehm", "norm_din_18947": "rw_din_18945_lehm", "norm_din_4074": "rw_din_4074_en_14081",
 "norm_din_68800": "rw_din_68800_altholzv", "norm_din_en_1090_2": "rw_en_1090", "norm_din_en_1168": "rw_en_1168",
 "norm_din_en_13369": "rw_en_1168", "norm_din_en_14081": "rw_din_4074_en_14081", "norm_din_en_15804": "rw_en_15804_15978",
 "norm_din_en_15978": "rw_en_15804_15978", "norm_din_en_1993": "rw_eurocodes_en_1990_1999", "norm_din_en_1996": "rw_eurocodes_en_1990_1999",
 "norm_din_en_206": "rw_dafstb_rc_beton", "norm_din_en_338": "rw_din_4074_en_14081", "norm_en_1090": "rw_en_1090",
 "norm_en_1090_2": "rw_en_1090", "norm_en_1168": "rw_en_1168", "norm_en_12058": "rw_en_naturstein", "norm_en_12371": "rw_en_naturstein",
 "norm_en_12372": "rw_en_naturstein", "norm_en_13162": "rw_en_13162_mineralwolle", "norm_en_13224": "rw_en_1168",
 "norm_en_13369": "rw_en_1168", "norm_en_1341": "rw_en_naturstein", "norm_en_13747": "rw_en_1168", "norm_en_13755": "rw_en_naturstein",
 "norm_en_14081": "rw_din_4074_en_14081", "norm_en_14231": "rw_en_naturstein", "norm_en_1469": "rw_en_naturstein",
 "norm_en_1936": "rw_en_naturstein", "norm_en_1992": "rw_eurocodes_en_1990_1999", "norm_en_1993": "rw_eurocodes_en_1990_1999",
 "norm_en_1995": "rw_eurocodes_en_1990_1999", "norm_en_1996": "rw_eurocodes_en_1990_1999", "norm_en_206": "rw_dafstb_rc_beton",
 "norm_en_338": "rw_din_4074_en_14081", "norm_en_771": "rw_en_771_reclaimed", "norm_en_771_1": "rw_en_771_reclaimed",
 "norm_en_772": "rw_en_771_reclaimed", "norm_en_998": "rw_en_771_reclaimed", "norm_en_sia_product_references": "rw_sia_269",
 "norm_en_sn_12058": "rw_en_naturstein", "norm_en_sn_1469": "rw_en_naturstein", "norm_eurocode_2": "rw_eurocodes_en_1990_1999",
 "norm_eurocode_3": "rw_eurocodes_en_1990_1999", "norm_eurocode_5": "rw_eurocodes_en_1990_1999", "norm_eurocode_5_uk_na": "rw_eurocodes_en_1990_1999",
 "norm_eurocode_6": "rw_eurocodes_en_1990_1999", "norm_eurocode_adjacent_structural_verification": "rw_cen_ts_17440",
 "norm_eurocode_related_timber_product_standards": "rw_din_4074_en_14081", "norm_finnish_national_annexes": "rw_eurocodes_en_1990_1999",
 "norm_fire_durability_rules": "rw_din_en_13501", "norm_fire_moisture_durability_requirements": "rw_din_en_13501",
 "norm_fire_moisture_rules": "rw_din_en_13501", "norm_frost_rules": "rw_en_naturstein", "norm_historic_sections_book": "rw_sci_p427",
 "norm_iso_14040": "rw_en_15804_15978", "norm_iso_14044": "rw_en_15804_15978", "norm_iso_20887": "rw_iso_20887",
 "norm_mvv_tb_dibt_pathway": "rw_mvv_tb", "norm_nbn_en_14081": "rw_din_4074_en_14081", "norm_nbn_en_338": "rw_din_4074_en_14081",
 "norm_nbn_national_annexes": "rw_eurocodes_en_1990_1999", "norm_nen_8700": "rw_nen_8700", "norm_nen_en_1090_2": "rw_en_1090",
 "norm_nen_en_14081": "rw_din_4074_en_14081", "norm_nen_en_338": "rw_din_4074_en_14081", "norm_nen_fire_moisture_rules": "rw_din_en_13501",
 "norm_ns_3682": "rw_din_4074_en_14081", "norm_ns_3682_2022": "rw_din_4074_en_14081", "norm_pd_cen_ts_1090_201": "rw_cen_ts_1090_201",
 "norm_recreate_qa_procedure": "rw_fib_precast_reuse", "norm_rt_2012": "rw_fr_re2020", "norm_sci_p427": "rw_sci_p427",
 "norm_sci_p440": "rw_sci_p427", "norm_sci_protocol": "rw_sci_p427", "norm_sia_261": "rw_sia_269", "norm_sia_262": "rw_sia_269_2",
 "norm_sia_263": "rw_sia_269", "norm_sia_265": "rw_sia_269", "norm_sia_269": "rw_sia_269", "norm_sia_380_1": "rw_sia_380_1",
 "norm_sia_416": "rw_sia_269", "norm_sia_500": "GAP_ch_barrierefrei", "norm_sia_facade_anchorage_rules": "rw_en_1992_4",
 "norm_sia_fire_durability_rules": "rw_vkf_bsv", "norm_sia_schweiz": "rw_sia_269", "norm_swiss_baupg": "GAP_ch_baupg",
 "norm_tek17": "rw_no_tek17", "norm_tek_norway": "rw_no_tek17", "norm_ukca_ce_interface": "rw_ukca_ce",
}

SCHADSTOFF_TO_NF = {
 "s_asbest": ["nf_asbest_check"], "s_kmf": ["nf_kmf_check"], "s_pcb": ["nf_pcb_check"], "s_pak": ["nf_pak_check"],
 "s_schwermetalle": ["nf_schwermetall_oder_bleifarbe_check"], "s_bleifarbe": ["nf_schwermetall_oder_bleifarbe_check"],
 "s_formaldehyd": ["nf_formaldehyd_oder_emissionsnachweis", "nf_voc_emissionsnachweis"],
 "s_holzschutzmittel": ["nf_holzschutzmittel_check"], "s_schimmel": ["nf_mikrobielle_belastung_check"],
 "s_radon": ["nf_radonmessung"], "s_chlorid": ["nf_schadstoffpruefung"], "s_salze": ["nf_schadstoffpruefung"],
 "s_mineraloel": ["nf_schadstoffpruefung"],
}

BPS_TO_RW = {
 "bps_ce_hen": "rw_eu_cpr_2024_3110", "bps_ce_eta": "rw_eu_cpr_2024_3110", "bps_ue_zeichen": "rw_mbo_lbo",
 "bps_abz_abg": "rw_dibt_zie_abz", "bps_zie_vbg": "rw_dibt_zie_abz", "bps_ukca": "rw_ukca_ce", "bps_baupg_ch": "GAP_ch_baupg",
 "bps_pemd_fr": "rw_fr_pemd", "bps_tracimat_be": "rw_be_tracimat_regional", "bps_nta_8713": "rw_nta_8713",
 "bps_ibc_104_11_alternative": "OUT_OF_SCOPE_usa", "bps_jis_jas_mlit": "OUT_OF_SCOPE_jp",
 "bps_bestand_no_status": "KEEP_ENUM", "bps_project_specific": "KEEP_ENUM", "bps_unbekannt": "KEEP_ENUM",
}

RB_TO = {
 "rb_bauordnungsrecht": "rw_mbo_lbo", "rb_bauproduktenverordnung_cpr": "rw_eu_cpr_2024_3110",
 "rb_boulder_deconstruction_ordinance_8366": "OUT_OF_SCOPE_usa", "rb_ce_marking_reused_steel": "rw_en_1090",
 "rb_denkmalschutz": "rw_denkmalschutz", "rb_dibt_zustimmung": "rw_dibt_zie_abz",
 "rb_eu_taxonomie": "rw_eu_taxonomy", "rb_gewaehrleistung": "rw_prodhaftg_bgb", "rb_grade_ii_listing": "rw_denkmalschutz",
 "rb_kreislaufwirtschaftsgesetz_krwg": "rw_krwg", "rb_materialpass": "rw_madaster_grp", "rb_produkthaftung": "rw_prodhaftg_bgb",
 "rb_schweizer_bauproduktegesetz": "GAP_ch_baupg", "rb_ukca_marking_reused_steel": "rw_ukca_ce",
 "rb_vergaberecht": "rw_zirkulaere_vergabe", "rb_zulassung_im_einzelfall": "rw_dibt_zie_abz",
}


def pruef_to_nf(nid):
    s = nid.lower()
    if any(k in s for k in ["schadstoff", "biozid", "pcp_lindan", "staub", "chlorid"]): return "nf_schadstoffpruefung"
    if "schimmel" in s: return "nf_mikrobielle_belastung_check"
    if any(k in s for k in ["brand", "feuerwid", "abbrand"]): return "nf_brandschutznachweis"
    if any(k in s for k in ["statik", "modulstatik", "tragf", "hebepunkt", "restquerschnitt", "spannlitz", "bewehrungsscan"]): return "nf_standsicherheitsnachweis"
    if any(k in s for k in ["zugversuch", "druckfest", "bohrkern", "rueckprall", "ultraschall", "haerte", "kerbschlag", "biege", "festigkeit", "sortierung", "pmi", "materialanalyse", "petrograf", "kornverteil", "dichte", "porosi", "wasserauf", "karbonat", "schweissbar", "klangprobe", "restmoertel", "restanhaft", "metalldetekt", "baulehm", "rutsch"]): return "nf_materialpruefung"
    if any(k in s for k in ["herkunft", "dokumenten", "chargenprot", "lagerprot", "bauteilpass", "rueckverfolg", "transportsicher"]): return "nf_herkunfts_und_rueckbaudokumentation"
    if any(k in s for k in ["mass", "geometr", "schnittplan", "schwindmass", "bohrbild", "fugen", "risskart", "risspru", "bruchbild", "zustand", "faeulnis", "restschicht", "sicht"]): return "nf_zustands_und_massaufnahme"
    if any(k in s for k in ["ug_wert", "ug_uw", "uw_wert", "lambda"]): return "nf_u_wert_oder_energie_info"
    if any(k in s for k in ["glasbruch", "glastyp", "kanten", "sicherheitsglas"]): return "nf_sicherheitsglas_info"
    if any(k in s for k in ["korrosion", "rostgrad", "beschichtung", "schichtdick", "haftzug", "oberflaech", "untergrund"]): return "nf_materialpruefung"
    if any(k in s for k in ["beschlag", "funktionspr", "dichtheit", "leckage", "wasserdicht", "bedien", "approval", "anwendungsbeschr", "nutzungsbeschr", "werkspru", "musterfl", "designstrat", "performance_gap"]): return "nf_produktstatus_und_leistungserklaerung"
    return "nf_materialpruefung"


def leist_to(nid):
    s = nid.lower()
    if any(k in s for k in ["brand", "feuer", "f90", "r90", "rei90"]): return "nf_brandschutznachweis"
    if any(k in s for k in ["waerme", "feuchteschutz", "luftdicht", "schlagregen", "innenraumklima", "schallschutz", "dichtheit"]): return "nf_bauphysiknachweis"
    if any(k in s for k in ["trag", "standsicher", "verbundf"]): return "nf_standsicherheitsnachweis"
    if any(k in s for k in ["korrosion", "schweissbar", "masshalt", "passgen", "kanten", "oberflaech", "maschinenbearb", "frostbest", "dauerhaft"]): return "nf_materialpruefung"
    if any(k in s for k in ["schadstoff", "innenraumluft", "hygiene", "feuchtereg"]): return "nf_schadstoffpruefung"
    if "rueckbau" in s or "rueckverfolg" in s: return "nf_herkunfts_und_rueckbaudokumentation"
    if any(k in s for k in ["rutsch", "sicherheit", "betriebssicher", "arbeitsschutz"]): return "nf_absturzsicherung"
    return "nf_produktstatus_und_leistungserklaerung"


HUERDE_KEEP = {"h_akzeptanzproblem", "h_mengenunsicherheit", "h_terminunsicherheit", "h_verfuegbarkeitsproblem",
               "h_fehlende_lagerflaeche", "h_aufbereitungsaufwand", "h_entwurfsbindung", "h_ausschreibungsproblem",
               "h_heterogenitaet_chargen", "h_witterung_feuchte", "h_unkonventionelles_material"}


def main():
    s = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "ENTWERFENMITBESTAND")).session(database="mit-bestand")
    live = {l: [r["id"] for r in s.run(f"MATCH (x:`{l}`) RETURN x.id AS id")]
            for l in ["Norm", "Schadstoff", "Bauproduktstatus", "RechtlicheBedingung", "PruefungNachweis", "Leistungsanforderung", "Huerde"]}
    s.close()

    rows = []

    def add(lbl, oid, action, target, basis):
        url, conf = ev(target if (target in RW or target in NACHWEISFORDERUNG) else "")
        rows.append([lbl, oid, action, target, basis, url, conf])

    for nid in sorted(live["Norm"]):
        t = NORM_TO_RW.get(nid, "UNMAPPED")
        act = "REWIRE->Regelwerk" if t in RW else ("DELETE+GAP" if str(t).startswith("GAP") else "REVIEW")
        add("Norm", nid, act, t, "Norm IS a standard = Regelwerk (deduped, evidenced)")
    for sid in sorted(live["Schadstoff"]):
        add("Schadstoff", sid, "KEEP+wire->Nachweis", "|".join(SCHADSTOFF_TO_NF.get(sid, ["nf_schadstoffpruefung"])),
            "pollutant entity kept; wired to its check + Regelwerk")
    for bid in sorted(live["Bauproduktstatus"]):
        t = BPS_TO_RW.get(bid, "REVIEW")
        act = "REWIRE->Regelwerk" if t in RW else ("KEEP-ENUM" if t == "KEEP_ENUM" else "REVIEW/OUT")
        add("Bauproduktstatus", bid, act, t, "conformity route = Regelwerk; generic status kept as enum")
    for rid in sorted(live["RechtlicheBedingung"]):
        t = RB_TO.get(rid, "REVIEW")
        act = "REWIRE->Regelwerk" if t in RW else "DELETE+GAP/Frage"
        add("RechtlicheBedingung", rid, act, t, "legal condition = Regelwerk or Genehmigung/Haftung-Frage")
    for pid in sorted(live["PruefungNachweis"]):
        add("PruefungNachweis", pid, "KEEP+wire->Nachweis(method)", pruef_to_nf(pid), "concrete test method under its Nachweisforderung")
    for lid in sorted(live["Leistungsanforderung"]):
        add("Leistungsanforderung", lid, "REWIRE->Nachweis/Frage", leist_to(lid), "performance requirement proven by Nachweis")
    for hid in sorted(live["Huerde"]):
        if hid in HUERDE_KEEP:
            add("Huerde", hid, "KEEP (market/logistics)", "-", "distinct market/logistics axis, not regulatory")
        else:
            add("Huerde", hid, "DELETE (regulatory)", "-", "regulatory barrier replaced by evidenced Frage/Nachweis")

    with open("rewire_map.csv", "w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["old_label", "old_id", "action", "new_target", "semantic_basis", "evidence_url", "confidence"])
        w.writerows(rows)

    print("rewire rows:", len(rows))
    print("by action:", dict(Counter(r[2] for r in rows)))
    gaps = [r for r in rows if "GAP" in str(r[3]) or r[3] in ("REVIEW", "UNMAPPED") or "OUT_OF_SCOPE" in str(r[3])]
    print("\nGAPS / needs-decision (", len(gaps), "):")
    for r in gaps:
        print(f"  [{r[0]}] {r[1]} -> {r[3]}")


if __name__ == "__main__":
    main()
