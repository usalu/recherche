#!/usr/bin/env python3
"""Generate Neo4j batch JSONL files for fallstudie batches 015-020 (27 new cases)."""
import json
from pathlib import Path

BASE = Path(r"e:\recherche\_neo4j\neo4j batch")


# ─── helpers ──────────────────────────────────────────────────────────────────

def n(id, labels, **props):
    if isinstance(labels, str):
        labels = [labels]
    return {"record_type": "node", "id": id, "labels": labels, "properties": {"id": id, **props}}

def r(from_id, rel_type, to_id, **props):
    return {"record_type": "rel",
            "id": f"r_{from_id}__{rel_type}__{to_id}",
            "from": from_id, "type": rel_type, "to": to_id,
            "properties": props}

def belegt(node_id, quelle_id):
    return r(node_id, "BELEGT_IN", quelle_id, datenqualitaet="Belegt")

def write_batch(batch_num, files_dict):
    d = BASE / f"neo4j_batch_{batch_num:03d}_exports" / "neo4j_exports" / "batches" / f"batch_{batch_num:03d}"
    d.mkdir(parents=True, exist_ok=True)
    for fname, lines in files_dict.items():
        with open(d / fname, "w", encoding="utf-8") as f:
            for obj in lines:
                f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        print(f"  {fname}  ({len(lines)} lines)")

# ─── shared city/country nodes (MERGE-safe – already in DB for known ones) ────

def ort_nodes(stadt_id, stadt_name, land_id, land_name, q):
    nodes = [
        n(stadt_id, "Stadt", name=stadt_name),
        n(land_id,  "Land",  name=land_name),
    ]
    rels = [
        belegt(stadt_id, q), belegt(land_id, q),
        r(stadt_id, "LIEGT_IN_LAND", land_id),
    ]
    return nodes, rels

def projekt_base(pid, title, bw, jahr=None, **extra):
    props = dict(name=title)
    if jahr:
        props["jahr"] = jahr
    props.update(extra)
    return n(pid, "Projekt", **props)

def akteur(a_id, name, rollen, typ, pid, q):
    nd = n(a_id, "Akteur", name=name)
    rels = [belegt(a_id, q)]
    for ro in rollen:
        rels.append(r(a_id, "HAT_AKTEURROLLE", ro))
    rels.append(r(a_id, "HAT_AKTEURTYP", typ))
    rels.append(r(a_id, "BETEILIGT_AN", pid))
    return nd, rels

def bauteilgruppe(bg_id, name, counts, donor_bw, recv_bw, pid, q,
                  types=(), ebene="be_bauteilgruppe", mats=(), wvas=(),
                  status="status_realisiert", aufbereitung=(), rueckbau=(),
                  pruefung=(), la=(), tp=(), bauweise=(), bausystem=(), fw=(),
                  huerde=(), **props):
    nd = n(bg_id, "Bauteilgruppe",
           name=name, counts_as_direct_reuse=counts, **props)
    rels = [belegt(bg_id, q),
            r(pid, "HAT_BAUTEILGRUPPE", bg_id)]
    if donor_bw:
        rels.append(r(bg_id, "AUS_BAUWERK", donor_bw))
    if recv_bw:
        rels.append(r(bg_id, "EINGEBAUT_IN", recv_bw))
    for bt in types:
        rels.append(r(bg_id, "HAT_BAUTEILTYP", bt))
    rels.append(r(bg_id, "HAT_BAUTEILEBENE", ebene))
    for m in mats:
        rels.append(r(bg_id, "NUTZT_MATERIAL", m))
    for w in wvas:
        rels.append(r(bg_id, "HAT_WIEDERVERWENDUNGSART", w))
    rels.append(r(bg_id, "HAT_STATUS", status))
    for av in aufbereitung:
        rels.append(r(bg_id, "HAT_AUFBEREITUNG", av))
    for rv in rueckbau:
        rels.append(r(bg_id, "HAT_RUECKBAUVERFAHREN", rv))
    for pr in pruefung:
        rels.append(r(bg_id, "HAT_PRUEFUNG", pr))
    for l in la:
        rels.append(r(bg_id, "HAT_LEISTUNGSANFORDERUNG", l))
    for t in tp:
        rels.append(r(bg_id, "HAT_TRAGWERKSPRINZIP", t))
    for bw in bauweise:
        rels.append(r(bg_id, "HAT_BAUWEISE", bw))
    for bs in bausystem:
        rels.append(r(bg_id, "HAT_BAUSYSTEM", bs))
    for f in fw:
        rels.append(r(bg_id, "HAT_FUNKTIONSWECHSEL", f))
    for h in huerde:
        rels.append(r(bg_id, "HAT_HUERDE", h))
    return nd, rels

def bauwerk(bw_id, name, bok, bor, stadt_id, land_id, status, nutzungen, q, note=None):
    props = dict(name=name)
    if note:
        props["note"] = note
    nd = n(bw_id, "Bauwerk", **props)
    rels = [belegt(bw_id, q),
            r(bw_id, "HAT_BAUOBJEKTKLASSE", bok),
            r(bw_id, "HAT_BAUOBJEKTROLLE", bor),
            r(bw_id, "LIEGT_IN_STADT", stadt_id),
            r(bw_id, "LIEGT_IN_LAND", land_id),
            r(bw_id, "HAT_STATUS", status)]
    for nu in nutzungen:
        rels.append(r(bw_id, "HAT_NUTZUNG", nu))
    return nd, rels


# ══════════════════════════════════════════════════════════════════════════════
# BATCH 015
# Cases: 55_Great_Suffolk_Street, Association_Groeditz, Association_Plauen,
#        BedZED_London_Hackbridge, AWM_Muenster_Circular_Office
# Delta: bsys_iw73
# ══════════════════════════════════════════════════════════════════════════════

def case_55_great_suffolk_street():
    q  = "q_55_great_suffolk_street_london_md"
    pid = "p_55_great_suffolk_street_london"
    bwr = "bw_55_great_suffolk_street"
    bwd = "bw_1_broadgate_london"
    bg1 = "bg_55gsf_structural_steel"
    lines = []

    # Quelle
    lines.append(n(q, "Quelle", name="55_Great_Suffolk_Street_London.md", quelltyp="case_markdown"))

    # Ort
    on, or_ = ort_nodes("stadt_london", "London", "land_uk", "United Kingdom", q)
    lines += on

    # Projekt
    lines.append(projekt_base(pid, "55 Great Suffolk Street London",
                               bwr, jahr=2022, bewertung=4,
                               projektstatus_text="gebaut 2022",
                               co2_saving_t=50,
                               reuse_menge_t=20.35))
    # Bauwerke
    bw_r, bwr_rels = bauwerk(bwr, "55 Great Suffolk Street – Victorian Warehouse",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_london", "land_uk", "status_gebaut",
                              ["nut_buero"], q,
                              note="Grade II listed Victorian warehouse; refurb + new external steel core")
    lines.append(bw_r)
    bw_d, bwd_rels = bauwerk(bwd, "1 Broadgate London (demolished)",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_london", "land_uk", "status_rueckgebaut",
                              ["nut_buero"], q)
    lines.append(bw_d)

    # Bauteilgruppe
    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Wiedergewonnene Stahlprofile (Tragwerk)", True,
        bwd, bwr, pid, q,
        types=["bt_stuetze", "bt_traeger"],
        mats=["mat_stahl"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung", "av_zuschnitt"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_materialpruefung", "pr_schweissbarkeitspruefung"],
        la=["la_tragfaehigkeit"],
        tp=["tp_skeletttragwerk"],
        bauweise=["bauw_stahlbauweise"],
        fw=["fw_gleiche_funktion"],
        huerde=["h_technische_freigabe", "h_verfuegbarkeitsproblem"],
        anzahl_t=20.35
    )
    lines.append(bg_nd)

    # Akteure
    akteure_data = [
        ("a_hawkins_brown",   "Hawkins\\Brown",          ["ar_architektur"],                  "at_unternehmen"),
        ("a_symmetrys",       "Symmetrys",               ["ar_tragwerksplanung"],              "at_unternehmen"),
        ("a_cleveland_steel", "Cleveland Steel & Tubes",  ["ar_materiallieferant"],             "at_unternehmen"),
        ("a_fabrix",          "Fabrix",                  ["ar_bauherr_auftraggeber"],          "at_unternehmen"),
    ]
    akteur_nodes, akteur_rels = [], []
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        akteur_nodes.append(nd)
        akteur_rels += rl

    lines += akteur_nodes

    # All rels
    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_london"),
        r(pid, "LIEGT_IN_LAND", "land_uk"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_sanierung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_building_material_scouting"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "NUTZT_BAUWERK", bwr),
        r(pid, "NUTZT_BAUWERK", bwd),
        r(pid, "REFERENZIERT_NORM", "norm_en_1090"),
    ]
    lines += bwr_rels + bwd_rels + bg_rels + akteur_rels
    return lines


def case_association_groeditz():
    q   = "q_association_house_groeditz_md"
    pid = "p_association_house_groeditz"
    bwr = "bw_association_house_groeditz"
    bwd1 = "bw_dresden_schule_donor"
    bwd2 = "bw_wbs70_source_groeditz"
    bg1 = "bg_groeditz_dresden_precast"
    bg2 = "bg_groeditz_wbs70_elements"
    lines = []

    lines.append(n(q, "Quelle", name="Association_house_Groeditz.md", quelltyp="case_markdown"))

    on, or_ = ort_nodes("stadt_groeditz", "Gröditz", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Association House Gröditz", bwr,
                               jahr=2007, bewertung=4,
                               projektstatus_text="gebaut 2007",
                               reuse_anzahl_teile=438,
                               transportdistanz_km=2.5))

    bw_r, bwr_rels = bauwerk(bwr, "Vereinshaus Gröditz",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_groeditz", "land_deutschland",
                              "status_gebaut", ["nut_wohnen"], q)
    bw_d1, bwd1_rels = bauwerk(bwd1, "Dresdner Schule (Spender)",
                                "bok_gebaeude", "bor_donorobjekt",
                                "stadt_groeditz", "land_deutschland",
                                "status_rueckgebaut", ["nut_schule_bildung"], q)
    bw_d2, bwd2_rels = bauwerk(bwd2, "WBS70 Plattenbau (Spender Gröditz)",
                                "bok_gebaeude", "bor_donorobjekt",
                                "stadt_groeditz", "land_deutschland",
                                "status_rueckgebaut", ["nut_wohnen"], q)
    lines += [bw_r, bw_d1, bw_d2]

    bg1_nd, bg1_rels = bauteilgruppe(
        bg1, "Betonfertigteile aus Dresdner Schule (279 Teile)", True,
        bwd1, bwr, pid, q,
        types=["bt_wand", "bt_decke"], mats=["mat_stahlbeton"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_zustandsbewertung"],
        la=["la_tragfaehigkeit"],
        bauweise=["bauw_fertigteilbauweise"],
        bausystem=["bsys_betonfertigteil_system"],
        anzahl=279
    )
    bg2_nd, bg2_rels = bauteilgruppe(
        bg2, "WBS70-Plattenbauteile (159 Teile)", True,
        bwd2, bwr, pid, q,
        types=["bt_wand", "bt_decke"], mats=["mat_stahlbeton"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau"],
        pruefung=["pr_zustandsbewertung"],
        la=["la_tragfaehigkeit"],
        bauweise=["bauw_fertigteilbauweise"],
        bausystem=["bsys_plattenbau"],
        anzahl=159
    )
    lines += [bg1_nd, bg2_nd]

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_groeditz"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_form_follows_availability"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_LOGISTIK", "log_transportdistanz"),
        r(pid, "NUTZT_BAUWERK", bwr),
        r(pid, "NUTZT_BAUWERK", bwd1),
        r(pid, "NUTZT_BAUWERK", bwd2),
        r(pid, "TEIL_VON_PROGRAMM", "prog_pilotprojekt"),
    ]
    lines += bwr_rels + bwd1_rels + bwd2_rels + bg1_rels + bg2_rels
    return lines


def case_association_plauen():
    q   = "q_association_house_plauen_md"
    pid = "p_association_house_plauen"
    bwr = "bw_association_house_plauen"
    bwd = "bw_iw73_plattenbau_plauen_donor"
    bg1 = "bg_plauen_iw73_betonfertigteile"
    lines = []

    lines.append(n(q, "Quelle", name="Association_house_Plauen.md", quelltyp="case_markdown"))

    on, or_ = ort_nodes("stadt_plauen", "Plauen", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Association House Plauen", bwr,
                               jahr=2007, bewertung=4,
                               projektstatus_text="gebaut 2007",
                               reuse_anzahl_teile=189,
                               transportdistanz_km=7))

    bw_r, bwr_rels = bauwerk(bwr, "Vereinshaus Plauen",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_plauen", "land_deutschland",
                              "status_gebaut", ["nut_wohnen"], q)
    bw_d, bwd_rels = bauwerk(bwd, "IW73/6-Plattenbau (Spender Plauen)",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_plauen", "land_deutschland",
                              "status_rueckgebaut", ["nut_wohnen"], q,
                              note="IW73/6 Plattenbausystem DDR; 145 Deckenplatten + 19 Außenwände + 14 Innenwände + 11 Kellerwände")
    lines += [bw_r, bw_d]

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "IW73/6-Betonfertigteile (189 Teile)", True,
        bwd, bwr, pid, q,
        types=["bt_decke", "bt_wand"], mats=["mat_stahlbeton"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_zustandsbewertung", "pr_materialpruefung"],
        la=["la_tragfaehigkeit", "la_brandschutz"],
        bauweise=["bauw_fertigteilbauweise"],
        bausystem=["bsys_iw73"],
        anzahl=189,
        deckenplatten=145, aussenwaende=19, innenwaende=14, kellerwaende=11
    )
    lines.append(bg_nd)

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_plauen"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_form_follows_availability"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_LOGISTIK", "log_transportdistanz"),
        r(pid, "NUTZT_BAUWERK", bwr),
        r(pid, "NUTZT_BAUWERK", bwd),
        r(pid, "TEIL_VON_PROGRAMM", "prog_pilotprojekt"),
    ]
    lines += bwr_rels + bwd_rels + bg_rels
    return lines


def case_bedzed():
    q   = "q_bedzed_london_hackbridge_md"
    pid = "p_bedzed_london_hackbridge"
    bwr = "bw_bedzed_housing_hackbridge"
    bg1 = "bg_bedzed_structural_steel"
    bg2 = "bg_bedzed_timber_studs"
    bg3 = "bg_bedzed_misc_reuse"
    lines = []

    lines.append(n(q, "Quelle", name="BedZED_London_Hackbridge.md", quelltyp="case_markdown"))

    on, or_ = ort_nodes("stadt_hackbridge", "Hackbridge / Wallington",
                         "land_uk", "United Kingdom", q)
    lines += on

    lines.append(projekt_base(pid, "BedZED – Beddington Zero Energy Development", bwr,
                               jahr=2002, bewertung=4,
                               projektstatus_text="gebaut 2000–2002",
                               reuse_stahl_t=98,
                               reuse_gesamt_t=3404,
                               reuse_anteil_prozent=15))

    bw_r, bwr_rels = bauwerk(bwr, "BedZED Wohn- und Bürokomplex Hackbridge",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_hackbridge", "land_uk",
                              "status_gebaut", ["nut_wohnen", "nut_buero", "nut_mischnutzung"], q,
                              note="82 Wohnungen + Büro; Peabody Trust; 3.404t Recycling-/Reusematerial (15%)")
    lines.append(bw_r)

    bg1_nd, bg1_rels = bauteilgruppe(
        bg1, "Wiedergewonnene Stahlträger (98t, 95% des Tragwerkstahls)", True,
        None, bwr, pid, q,
        types=["bt_traeger", "bt_stuetze"], mats=["mat_stahl"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung", "av_verstaerkung"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_sichtpruefung", "pr_geometrische_vermessung"],
        la=["la_tragfaehigkeit"],
        tp=["tp_skeletttragwerk"],
        bauweise=["bauw_stahlbauweise"],
        fw=["fw_gleiche_funktion"],
        huerde=["h_verfuegbarkeitsproblem"],
        menge_t=98, anteil_prozent=95
    )
    bg2_nd, bg2_rels = bauteilgruppe(
        bg2, "Wiedergewonnene Nadelholzständer (54 km)", True,
        None, bwr, pid, q,
        types=["bt_wand"], mats=["mat_holz"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau"],
        pruefung=["pr_sichtpruefung"],
        la=["la_tragfaehigkeit"],
        fw=["fw_gleiche_funktion"],
        laenge_km=54
    )
    bg3_nd, bg3_rels = bauteilgruppe(
        bg3, "Diverses Reuse-Material (Türen, Bordsteine, Steinplatten, Geländerrohre)", True,
        None, bwr, pid, q,
        types=["bt_tuer", "bt_boden", "bt_gelaender"], mats=["mat_naturstein", "mat_stahl"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_ausbau_von_bauteilen"],
        fw=["fw_neue_funktion", "fw_gleiche_funktion"],
    )
    lines += [bg1_nd, bg2_nd, bg3_nd]

    akteure_data = [
        ("a_bill_dunster_zedfactory", "Bill Dunster / ZEDfactory",
         ["ar_architektur"], "at_unternehmen"),
        ("a_bioregional",            "BioRegional",
         ["ar_forschung_dokumentation", "ar_reuse_beratung"], "at_ngo_netzwerk"),
        ("a_peabody_trust",          "Peabody Trust",
         ["ar_bauherr_auftraggeber"], "at_unternehmen"),
        ("a_arup",                   "Arup",
         ["ar_tragwerksplanung"], "at_unternehmen"),
    ]
    akteur_nodes, akteur_rels = [], []
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        akteur_nodes.append(nd)
        akteur_rels += rl
    lines += akteur_nodes

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_hackbridge"),
        r(pid, "LIEGT_IN_LAND", "land_uk"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "HAT_METHODE", "meth_building_material_scouting"),
        r(pid, "HAT_METHODE", "meth_urban_mining"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_LOGISTIK", "log_lokale_wiederverwendung"),
        r(pid, "HAT_LOGISTIK", "log_transportdistanz"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg1_rels + bg2_rels + bg3_rels + akteur_rels
    return lines


def case_awm_muenster():
    q   = "q_awm_muenster_circular_office_md"
    pid = "p_awm_muenster_circular_office"
    bwr = "bw_awm_muenster_office"
    bwd = "bw_behrensbau_duesseldorf"
    bg1 = "bg_awm_glastrennwaende"
    bg2 = "bg_awm_kabelkanaele_upcycling"
    lines = []

    lines.append(n(q, "Quelle", name="AWM_Muenster_Circular_Office.md", quelltyp="case_markdown"))

    on, or_ = ort_nodes("stadt_muenster", "Münster", "land_deutschland", "Deutschland", q)
    lines += on
    on2, or2 = ort_nodes("stadt_duesseldorf", "Düsseldorf", "land_deutschland", "Deutschland", q)
    lines += on2

    lines.append(projekt_base(pid, "AWM Münster Circular Office", bwr,
                               jahr=2022, bewertung=3,
                               projektstatus_text="gebaut ~2022",
                               reuse_menge_t=6.9,
                               co2_saving_t=13.32,
                               co2_reduction_prozent=82))

    bw_r, bwr_rels = bauwerk(bwr, "AWM Münster Bürofitout Rösnertstraße",
                              "bok_innenausbau", "bor_empfaengerobjekt",
                              "stadt_muenster", "land_deutschland",
                              "status_gebaut", ["nut_buero"], q,
                              note="~250m² interior fit-out; 6.9t reclaimed; 82% CO2 reduction")
    bw_d, bwd_rels = bauwerk(bwd, "Behrensbau Düsseldorf (Spender)",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_duesseldorf", "land_deutschland",
                              "status_rueckgebaut", ["nut_buero"], q)
    lines += [bw_r, bw_d]

    bg1_nd, bg1_rels = bauteilgruppe(
        bg1, "Glastrennwände + WC-Wände aus Behrensbau Düsseldorf", True,
        bwd, bwr, pid, q,
        types=["bt_wand", "bt_fassade"], mats=["mat_glas"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung", "av_zuschnitt"],
        rueckbau=["rv_demontage"],
        pruefung=["pr_sichtpruefung"],
        fw=["fw_gleiche_funktion"],
    )
    bg2_nd, bg2_rels = bauteilgruppe(
        bg2, "Kabelkanäle als Regalböden und Leuchten (Upcycling)", True,
        None, bwr, pid, q,
        types=["bt_ausbau", "bt_technik"], mats=["mat_stahl"],
        wvas=["wva_direkte_wiederverwendung", "wva_upcycling"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_ausbau_von_bauteilen"],
        fw=["fw_neue_funktion"],
    )
    lines += [bg1_nd, bg2_nd]

    nd_c, rl_c = akteur("a_concular", "Concular",
                         ["ar_reuse_beratung"], "at_unternehmen", pid, q)
    lines.append(nd_c)

    lines += or_ + or2
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_muenster"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_fit_out"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_upcycling"),
        r(pid, "HAT_METHODE", "meth_building_material_scouting"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_digitale_plattform"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_LOGISTIK", "log_materialmatching"),
        r(pid, "NUTZT_BAUWERK", bwr),
        r(pid, "NUTZT_BAUWERK", bwd),
    ]
    lines += bwr_rels + bwd_rels + bg1_rels + bg2_rels + rl_c
    return lines


# ══════════════════════════════════════════════════════════════════════════════
# BATCH 016
# Cases: LysP8, ELYS_detailed, ELEMENTA, Bestandshalle_CRCLR, Hobelwerk_Haus_D
# ══════════════════════════════════════════════════════════════════════════════

def case_lysp8_basel():
    q   = "q_lysp8_basel_lysbuechelareal_md"
    pid = "p_lysp8_basel_lysbuechelareal"
    bwr = "bw_lysp8_basel"
    lines = []

    lines.append(n(q, "Quelle", name="LysP8_Basel_Lysbuechelareal.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_basel", "Basel", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid, "LysP8 Basel Lysbuechelareal", bwr,
                               jahr=2025, bewertung=4,
                               projektstatus_text="gebaut 2025",
                               co2_saving_t=250))

    bw_r, bwr_rels = bauwerk(bwr, "LysP8 – Langhaus + Punkthaus Basel",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_gebaut", ["nut_wohnen", "nut_gewerbe"], q,
                              note="27 Wohnungen (günstig) + Gewerbe EG; ~30 Bauteilgruppen Reuse")
    lines.append(bw_r)

    bgs = [
        ("bg_lysp8_faserzement_fassade", "Faserzement-Fassadenplatten (Reuse)", True,
         ["bt_fassade"], ["mat_faserzement"], ["fw_gleiche_funktion"]),
        ("bg_lysp8_fensterlaeden",       "Fensterläden Metall aus Zürcher Siedlung", True,
         ["bt_fassade"], ["mat_aluminium"], ["fw_gleiche_funktion"]),
        ("bg_lysp8_dachziegel_fassade",  "Dachziegel als Fassadenverkleidung", True,
         ["bt_fassade", "bt_dach"], ["mat_keramik"], ["fw_neue_funktion"]),
        ("bg_lysp8_brettschichtholz",    "Brettschichtholz-Deckenelemente (~400m²) aus Formel-E-Pavillon", True,
         ["bt_decke"], ["mat_holz"], ["fw_gleiche_funktion"]),
        ("bg_lysp8_kuechen",             "~30 Küchenzeilen (Reuse)", True,
         ["bt_ausbau"], ["mat_holz", "mat_stahl"], ["fw_gleiche_funktion"]),
        ("bg_lysp8_sanitaer",            "WC-Becken, Armaturen, Sanitärkeramik", True,
         ["bt_ausbau", "bt_technik"], ["mat_keramik"], ["fw_gleiche_funktion"]),
    ]
    for bg_id, name, cdr, types, mats, fw in bgs:
        bg_nd, bg_rels = bauteilgruppe(
            bg_id, name, cdr, None, bwr, pid, q,
            types=types, mats=mats,
            wvas=["wva_direkte_wiederverwendung"],
            aufbereitung=["av_reinigung"], fw=fw,
            rueckbau=["rv_ausbau_von_bauteilen"],
        )
        lines.append(bg_nd)
        lines += bg_rels

    akteure_data = [
        ("a_stiftung_habitat",     "Stiftung Habitat",           ["ar_bauherr_auftraggeber"],   "at_organisation"),
        ("a_loeliger_strub",       "Loeliger Strub Architektur", ["ar_architektur"],            "at_unternehmen"),
        ("a_zirkular_cirkla",      "Zirkular / Cirkla",          ["ar_reuse_beratung"],         "at_unternehmen"),
        ("a_eitel_partner",        "Eitel & Partner",            ["ar_tragwerksplanung"],       "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_basel"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "HAT_METHODE", "meth_form_follows_availability"),
        r(pid, "HAT_METHODE", "meth_building_material_scouting"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_digitale_plattform"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_lager"),
        r(pid, "HAT_LOGISTIK", "log_lagerung"),
        r(pid, "HAT_LOGISTIK", "log_materialmatching"),
        r(pid, "HAT_BAUWEISE", "bauw_holzbauweise"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_elys_lysbuechelareal():
    q   = "q_elys_kultur_und_gewerbehaus_basel_lysbuechelareal_md"
    pid = "p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal"
    bwr = "bw_elys_lysp_kultur_gewerbehaus"
    lines = []

    lines.append(n(q, "Quelle", name="ELYS_Kultur_und_Gewerbehaus_Basel_Lysbuechelareal.md",
                   quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_basel", "Basel", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid,
                               "ELYS Kultur- und Gewerbehaus Basel Lysbuechelareal (detaillierte Fallstudie)",
                               bwr, bewertung=4,
                               projektstatus_text="gebaut",
                               note="Detaillierte Version; Umbau ehemaliges Coop-Verteilzentrum/Großbäckerei 1980er"))

    bw_r, bwr_rels = bauwerk(bwr, "ELYS Kultur- und Gewerbehaus Basel",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_gebaut", ["nut_gewerbe", "nut_kultur"], q,
                              note="Umbau ehem. Coop-Verteilzentrum/Großbäckerei; Neue Fassade ~1000m²")
    lines.append(bw_r)

    bgs = [
        ("bg_elys_fenster_fassade",    "~200 verschiedene Fenster als Fassade (Lagerware/Fehlbestellungen)", True,
         ["bt_fenster", "bt_fassade"], ["mat_glas", "mat_aluminium"]),
        ("bg_elys_rueckbauholz_glulam","~150m³ Rückbauholz als neue Leimbinder", True,
         ["bt_traeger", "bt_dach"], ["mat_holz"]),
        ("bg_elys_trapezblech",        "Trapezbleche aus ehem. Coop-Weinlager (beige)", True,
         ["bt_fassade", "bt_dach"], ["mat_stahl"]),
        ("bg_elys_bestehende_fassade", "Bestehende grüne Trapezblechfassade teilweise erhalten", True,
         ["bt_fassade"], ["mat_stahl"]),
    ]
    for bg_id, name, cdr, types, mats in bgs:
        bg_nd, bg_rels = bauteilgruppe(
            bg_id, name, cdr, None, bwr, pid, q,
            types=types, mats=mats,
            wvas=["wva_direkte_wiederverwendung"],
            aufbereitung=["av_reinigung"],
            rueckbau=["rv_ausbau_von_bauteilen"],
        )
        lines.append(bg_nd)
        lines += bg_rels

    akteure_data = [
        ("a_bauburo_in_situ",         "baubüro in situ",             ["ar_architektur"],         "at_unternehmen"),
        ("a_zirkular_cirkla",         "Zirkular / Cirkla",           ["ar_reuse_beratung"],      "at_unternehmen"),
        ("a_immobilien_basel_stadt",  "Immobilien Basel-Stadt",      ["ar_bauherr_auftraggeber"],"at_oeffentliche_institution"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_basel"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_umbau"),
        r(pid, "HAT_INTERVENTION", "bai_umnutzung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_adaptives_reuse"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "HAT_METHODE", "meth_form_follows_availability"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_lager"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_lager"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_elementa():
    q   = "q_elementa_walkeweg_basel_md"
    pid = "p_elementa_walkeweg_basel"
    bwr = "bw_elementa_walkeweg_c_d"
    bwd = "bw_lysbuechel_parkhaus_basel"
    bg1 = "bg_elementa_beton_traeger_decken"
    lines = []

    lines.append(n(q, "Quelle", name="ELEMENTA.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_basel", "Basel", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid, "ELEMENTA Walkeweg Basel C+D", bwr,
                               bewertung=3,
                               projektstatus_text="Wettbewerb gewonnen; Planung",
                               transportdistanz_km=6))

    bw_r, bwr_rels = bauwerk(bwr, "ELEMENTA Wohngebäude Walkeweg C+D",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_geplant", ["nut_wohnen"], q,
                              note="Neubau mit wiedergewonnenen Betonfertigteilen aus Lysbuechel-Parkhaus")
    bw_d, bwd_rels = bauwerk(bwd, "Lysbuechel Parkhaus Basel (Spender)",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_rueckgebaut", ["nut_infrastruktur"], q)
    lines += [bw_r, bw_d]

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Betonfertigteile Parkhaus (Träger + Deckenplatten)", True,
        bwd, bwr, pid, q,
        types=["bt_decke", "bt_traeger"], mats=["mat_stahlbeton"],
        wvas=["wva_direkte_wiederverwendung", "wva_urban_mining"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_materialpruefung", "pr_zustandsbewertung"],
        la=["la_tragfaehigkeit"],
        bauweise=["bauw_fertigteilbauweise"],
        bausystem=["bsys_betonfertigteil_system"],
        status="status_geplant",
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_parabase",                "PARABASE Architekten",        ["ar_architektur"],          "at_unternehmen"),
        ("a_immobilien_basel_stadt",  "Immobilien Basel-Stadt",      ["ar_bauherr_auftraggeber"], "at_oeffentliche_institution"),
        ("a_zirkular_cirkla",         "Zirkular / Cirkla",           ["ar_reuse_beratung"],       "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_basel"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_geplant"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "HAT_METHODE", "meth_zirkulaere_ausschreibung"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "HAT_METHODE", "meth_urban_mining"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_ausschreibung"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_LOGISTIK", "log_transportdistanz"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_wettbewerb"),
        r(pid, "NUTZT_BAUWERK", bwr),
        r(pid, "NUTZT_BAUWERK", bwd),
    ]
    lines += bwr_rels + bwd_rels + bg_rels
    return lines


def case_bestandshalle_crclr():
    q   = "q_bestandshalle_crclr_house_md"
    pid = "p_bestandshalle_crclr_house"
    bwr = "bw_bestandshalle_crclr_kindl_areal"
    lines = []

    lines.append(n(q, "Quelle", name="Bestandshalle_CRCLR_House.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Bestandshalle CRCLR House Berlin-Neukölln", bwr,
                               bewertung=3,
                               projektstatus_text="gebaut",
                               note="Industriehalle 1872, Kindl-Areal; Umbau + Holzaufstockung"))

    bw_r, bwr_rels = bauwerk(bwr, "Bestandshalle CRCLR House – Kindl-Areal Neukölln",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_gebaut", ["nut_gewerbe", "nut_kultur"], q,
                              note="Ehemalige Industriehalle 1872; Umbau mit Holzaufstockung")
    lines.append(bw_r)

    bgs = [
        ("bg_crclr_tueren",            "Türen + Schiebetüren aus ehem. Impact Hub Berlin", True,
         ["bt_tuer"], ["mat_holz", "mat_stahl"], ["fw_gleiche_funktion"]),
        ("bg_crclr_mdf_schwarz",       "Schwarzes MDF aus Berliner Club",                  True,
         ["bt_ausbau", "bt_boden"], ["mat_mdf"],  ["fw_neue_funktion"]),
        ("bg_crclr_stahl_treppen",     "Stahlbauteile Hallendach als Treppenwangen",       True,
         ["bt_treppe", "bt_traeger"], ["mat_stahl"], ["fw_neue_funktion"]),
    ]
    for bg_id, name, cdr, types, mats, fw in bgs:
        bg_nd, bg_rels = bauteilgruppe(
            bg_id, name, cdr, None, bwr, pid, q,
            types=types, mats=mats,
            wvas=["wva_direkte_wiederverwendung"],
            aufbereitung=["av_reinigung"],
            rueckbau=["rv_demontage"],
            fw=fw,
        )
        lines.append(bg_nd)
        lines += bg_rels

    akteure_data = [
        ("a_trnsfrm_eg",    "TRNSFRM eG",               ["ar_bauherr_auftraggeber"],  "at_organisation"),
        ("a_lxsy_architektur","LXSY Architektur",        ["ar_architektur"],           "at_unternehmen"),
        ("a_zrs_architekten","ZRS Architekten Ingenieure",["ar_tragwerksplanung"],      "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_umbau"),
        r(pid, "HAT_INTERVENTION", "bai_aufstockung"),
        r(pid, "HAT_INTERVENTION", "bai_umnutzung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_adaptives_reuse"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_weiterbauen_im_bestand"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_informelles_netzwerk"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_hobelwerk_haus_d():
    q   = "q_hobelwerk_haus_d_oberwinterthur_md"
    pid = "p_hobelwerk_haus_d_oberwinterthur"
    bwr = "bw_hobelwerk_haus_d_winterthur"
    bg1 = "bg_hobelwerk_d_fenster_ausbau"
    lines = []

    lines.append(n(q, "Quelle", name="Hobelwerk_Haus_D_Oberwinterthur.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_winterthur", "Winterthur", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid, "Hobelwerk Haus D Oberwinterthur", bwr,
                               bewertung=2,
                               projektstatus_text="gebaut Ende 2023"))

    bw_r, bwr_rels = bauwerk(bwr, "Hobelwerk Haus D – Genossenschaftswohnbau",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_winterthur", "land_schweiz",
                              "status_gebaut", ["nut_wohnen"], q,
                              note="Eines von mehreren Wohnhäusern im Hobelwerk-Areal; Reuse-Detaildaten begrenzt")
    lines.append(bw_r)

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Fenster + Ausbauteile (Reuse, Detaildaten begrenzt)", True,
        None, bwr, pid, q,
        types=["bt_fenster", "bt_ausbau"], mats=["mat_holz", "mat_glas"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_ausbau_von_bauteilen"],
        huerde=["h_datenluecke"],
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_mehr_als_wohnen",  "Baugenossenschaft mehr als wohnen", ["ar_bauherr_auftraggeber"], "at_organisation"),
        ("a_zirkular_cirkla",  "Zirkular / Cirkla",                 ["ar_reuse_beratung"],       "at_unternehmen"),
        ("a_bauburo_in_situ",  "baubüro in situ",                   ["ar_architektur"],          "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_winterthur"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_digitale_plattform"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "HAT_HUERDE", "h_datenluecke"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg_rels
    return lines


# ══════════════════════════════════════════════════════════════════════════════
# BATCH 017
# Cases: Lysbuechel_Parkhaus, Da_Vinci, ReUseBox_Heilbronn, BOELL_LAB, CRCLR_Overview
# ══════════════════════════════════════════════════════════════════════════════

def case_lysbuechel_parkhaus():
    q   = "q_lysbuechel_parkhaus_basel_md"
    pid = "p_lysbuechel_parkhaus_basel"
    bw1 = "bw_lysbuechel_parkhaus_basel"
    bg1 = "bg_lysbuechel_parkhaus_betonteile"
    lines = []

    lines.append(n(q, "Quelle", name="Lysbuechel_Parkhaus.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_basel", "Basel", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid, "Lysbuechel Parkhaus Basel (Spendergebäude)", bw1,
                               bewertung=3,
                               projektstatus_text="rückgebaut (Spender für ELEMENTA)"))

    bw_d, bwd_rels = bauwerk(bw1, "Lysbuechel Parkhaus Basel",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_rueckgebaut", ["nut_infrastruktur"], q,
                              note="Selektiver Rückbau; Betonfertigteile → ELEMENTA/Walkeweg")
    lines.append(bw_d)

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Betonfertigteile: Stützen, Träger, Deckenplatten, Rampenplatten", True,
        bw1, None, pid, q,
        types=["bt_decke", "bt_traeger", "bt_stuetze"], mats=["mat_stahlbeton"],
        wvas=["wva_direkte_wiederverwendung", "wva_urban_mining"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_materialpruefung", "pr_zustandsbewertung"],
        la=["la_tragfaehigkeit"],
        bauweise=["bauw_fertigteilbauweise"],
        status="status_rueckgebaut",
    )
    lines.append(bg_nd)

    nd_a, rl_a = akteur("a_immobilien_basel_stadt", "Immobilien Basel-Stadt",
                         ["ar_oeffentliche_hand", "ar_bauherr_auftraggeber"],
                         "at_oeffentliche_institution", pid, q)
    lines.append(nd_a)

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_basel"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_rueckgebaut"),
        r(pid, "HAT_INTERVENTION", "bai_rueckbau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_pre_deconstruction_audit"),
        r(pid, "HAT_METHODE", "meth_materialinventur"),
        r(pid, "HAT_RUECKBAUVERFAHREN", "rv_selektiver_rueckbau"),
        r(pid, "NUTZT_BAUWERK", bw1),
    ]
    lines += bwd_rels + bg_rels + rl_a
    return lines


def case_da_vinci():
    q   = "q_da_vinci_business_district_evere_md"
    pid = "p_da_vinci_business_district_evere"
    bwr = "bw_da_vinci_business_district_evere"
    lines = []

    lines.append(n(q, "Quelle", name="Da_Vinci_Business_District.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_evere", "Evere (Brüssel)", "land_belgien", "Belgien", q)
    lines += on

    lines.append(projekt_base(pid, "Da Vinci Business District – Rotor DC ReUse Centre", bwr,
                               bewertung=2,
                               projektstatus_text="in Bau seit 2022",
                               flaeche_m2=14000))

    bw_r, bwr_rels = bauwerk(bwr, "Da Vinci Business District Evere – ReUse Centre",
                              "bok_reuse_centre", "bor_empfaengerobjekt",
                              "stadt_evere", "land_belgien",
                              "status_in_bau", ["nut_gewerbe"], q,
                              note="~14.000m² Industriegebäude aus 1980er Jahren; Transformation zu Rotor DC ReUse-Zentrum")
    lines.append(bw_r)

    akteure_data = [
        ("a_rotor_deconstruction", "Rotor Deconstruction / RotorDC",
         ["ar_betreiber_nutzer", "ar_bauherr_auftraggeber"], "at_unternehmen"),
        ("a_citydev_brussels",     "citydev.brussels",
         ["ar_oeffentliche_hand"], "at_oeffentliche_institution"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_evere"),
        r(pid, "LIEGT_IN_LAND", "land_belgien"),
        r(pid, "HAT_STATUS", "status_in_bau"),
        r(pid, "HAT_INTERVENTION", "bai_umbau"),
        r(pid, "HAT_INTERVENTION", "bai_umnutzung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_adaptives_reuse"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_bestandserhalt"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_reusebox_heilbronn():
    q   = "q_reusebox_heilbronn_md"
    pid = "p_reusebox_heilbronn"
    bwr = "bw_reusebox_heilbronn"
    lines = []

    lines.append(n(q, "Quelle", name="ReUseBox_Heilbronn.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_heilbronn", "Heilbronn", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "ReUseBox Heilbronn (Wettbewerbsbeitrag 2025)", bwr,
                               bewertung=2,
                               projektstatus_text="Wettbewerb 2025; Realisierung ungesichert"))

    bw_r, bwr_rels = bauwerk(bwr, "ReUseBox Heilbronn – Demonstratorbau",
                              "bok_gebaeude", "bor_empfaengerobjekt",
                              "stadt_heilbronn", "land_deutschland",
                              "status_wettbewerb", ["nut_kultur"], q,
                              note="Wettbewerbsentwurf; Lern- und Erlebnisort Kreislaufwirtschaft")
    lines.append(bw_r)

    bg1_nd, bg1_rels = bauteilgruppe(
        "bg_reusebox_stahltraeger", "Wiedergewonnene Stahlträger (Tragwerk)", True,
        None, bwr, pid, q,
        types=["bt_traeger"], mats=["mat_stahl"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau"],
        tp=["tp_skeletttragwerk"],
        bauweise=["bauw_stahlbauweise"],
        fw=["fw_gleiche_funktion"],
        status="status_geplant",
    )
    bg2_nd, bg2_rels = bauteilgruppe(
        "bg_reusebox_altholz", "Altholz (Ausbau + Fassade)", True,
        None, bwr, pid, q,
        types=["bt_ausbau", "bt_fassade"], mats=["mat_holz"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung", "av_holzaufbereitung"],
        rueckbau=["rv_demontage"],
        fw=["fw_neue_funktion"],
        status="status_geplant",
    )
    lines += [bg1_nd, bg2_nd]

    akteure_data = [
        ("a_lxsy_architektur",  "LXSY Architektur",  ["ar_architektur"],         "at_unternehmen"),
        ("a_stadt_heilbronn",   "Stadt Heilbronn",   ["ar_bauherr_auftraggeber"], "at_oeffentliche_institution"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_heilbronn"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_wettbewerb"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_design_for_disassembly"),
        r(pid, "HAT_METHODE", "meth_design_for_disassembly"),
        r(pid, "HAT_METHODE", "meth_form_follows_availability"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_wettbewerb"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg1_rels + bg2_rels
    return lines


def case_boell_lab():
    q   = "q_boell_lab_berlin_md"
    pid = "p_boell_lab_berlin"
    bwr = "bw_boell_lab_berlin_konzept"
    lines = []

    lines.append(n(q, "Quelle", name="BOELL_LAB_Berlin.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "BOELL.LAB Berlin (Projekt eingestellt)", bwr,
                               bewertung=1,
                               projektstatus_text="verworfen/eingestellt"))

    bw_r, bwr_rels = bauwerk(bwr, "BOELL.LAB Berlin (Konzept, nicht realisiert)",
                              "bok_pavillon", "bor_empfaengerobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_verworfen", ["nut_kultur"], q,
                              note="Geplanter Pavillon Karl-Marx-Allee; Design for Disassembly + ReUse Bauteile; eingestellt laut LXSY")
    lines.append(bw_r)

    akteure_data = [
        ("a_lxsy_architektur",       "LXSY Architektur",        ["ar_architektur"],          "at_unternehmen"),
        ("a_heinrich_boell_stiftung","Heinrich-Böll-Stiftung",  ["ar_bauherr_auftraggeber"], "at_organisation"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_verworfen"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_design_for_disassembly"),
        r(pid, "HAT_METHODE", "meth_design_for_disassembly"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_crclr_overview():
    q   = "q_crclr_house_berlin_overview_md"
    pid = "p_crclr_house_berlin_overview"
    bwr = "bw_crclr_house_berlin"
    bg1 = "bg_crclr_overview_stahl_treppenwangen"
    lines = []

    lines.append(n(q, "Quelle", name="CRCLR_House.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "CRCLR House Berlin – Überblicksfallstudie", bwr,
                               bewertung=3,
                               projektstatus_text="gebaut",
                               note="Überblicksfallstudie; Kindl-Areal; Industrie-Bestandshalle + Holzaufstockung"))

    bw_r, bwr_rels = bauwerk(bwr, "CRCLR House Berlin Neukölln (ehem. Industriehalle)",
                              "bok_gebaeude", "bor_bestandsobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_gebaut", ["nut_gewerbe", "nut_kultur"], q,
                              note="Industriehalle 1872, Kindl-Areal; Umbau + Holzaufstockung")
    lines.append(bw_r)

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Stahlbauteile Hallendach als Treppenwangen (tragend)", True,
        bwr, bwr, pid, q,
        types=["bt_treppe", "bt_traeger"], mats=["mat_stahl"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung"],
        fw=["fw_neue_funktion"],
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_trnsfrm_eg",      "TRNSFRM eG",                ["ar_bauherr_auftraggeber"], "at_organisation"),
        ("a_lxsy_architektur","LXSY Architektur",           ["ar_architektur"],          "at_unternehmen"),
        ("a_zrs_architekten", "ZRS Architekten Ingenieure", ["ar_tragwerksplanung"],     "at_unternehmen"),
        ("a_concular",        "Concular",                   ["ar_reuse_beratung"],       "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_umbau"),
        r(pid, "HAT_INTERVENTION", "bai_aufstockung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_weiterbauen_im_bestand"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg_rels
    return lines


# ══════════════════════════════════════════════════════════════════════════════
# BATCH 018
# Cases: Kindl_Areal, BIZH_Reallabor, Be_Ware, Opalis_Plattformfall
# ══════════════════════════════════════════════════════════════════════════════

def case_kindl_areal():
    q   = "q_kindl_areal_berlin_md"
    pid = "p_kindl_areal_berlin"
    bwr = "bw_kindl_areal_berlin"
    lines = []

    lines.append(n(q, "Quelle", name="Kindl_Areal.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Kindl Areal Berlin-Neukölln – Arealtransformation", bwr,
                               bewertung=2,
                               projektstatus_text="gebaut / laufend",
                               note="Ehemaliges Brauereigelände; Adaptive Reuse; Gemeinschaftsprojekt"))

    bw_r, bwr_rels = bauwerk(bwr, "Kindl Areal Berlin-Neukölln",
                              "bok_quartier_areal", "bor_bestandsobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_gebaut", ["nut_gewerbe", "nut_kultur", "nut_wohnen"], q,
                              note="Ehem. Schultheiß-Brauerei; Bestandserhalt + Adaptive Reuse; CRCLR House, Vollgut, KINDL Kunst")
    lines.append(bw_r)

    akteure_data = [
        ("a_trnsfrm_eg",        "TRNSFRM eG",              ["ar_betreiber_nutzer"],    "at_organisation"),
        ("a_edith_maryon_stift","Stiftung Edith Maryon",   ["ar_oeffentliche_hand"],   "at_organisation"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_umbau"),
        r(pid, "HAT_INTERVENTION", "bai_umnutzung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_bestandserhalt"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_adaptives_reuse"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_bizh_reallabor():
    q   = "q_bizh_reallabor_berlin_md"
    pid = "p_bizh_reallabor_berlin"
    bwr = "bw_halle_2_ringberlin"
    bg1 = "bg_bizh_drahtglas_zweischeiben"
    lines = []

    lines.append(n(q, "Quelle", name="BIZH_Reallabor.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "BIZH Reallabor – Drahtglas Zweischeiben-Isolierverglasung", bwr,
                               bewertung=2,
                               projektstatus_text="in Bau / Reallabor laufend"))

    bw_r, bwr_rels = bauwerk(bwr, "Halle 2 ringberlin – Sheddach 1938",
                              "bok_gebaeude", "bor_bestandsobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_in_bau", ["nut_gewerbe"], q,
                              note="Halle 2 mit Sheddach von 1938; Drahtglasscheiben als Donor für Reallabor-Prototyp")
    lines.append(bw_r)

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Drahtglasscheiben aus Sheddach → Zweischeiben-Isolierverglasung (Prototyp)", False,
        bwr, bwr, pid, q,
        types=["bt_fenster", "bt_fassade"], mats=["mat_glas"],
        wvas=["wva_remanufacturing"],
        aufbereitung=["av_remanufacturing", "av_drahtglasschneiden"],
        pruefung=["pr_sichtpruefung", "pr_materialpruefung"],
        la=["la_waermeschutz", "la_brandschutz"],
        huerde=["h_technische_freigabe", "h_bauproduktstatus"],
        status="status_in_bau",
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_bizh",                "BIZH (Berliner Institut für Zirkuläres Handwerk)", ["ar_forschung_dokumentation"],    "at_forschung_lehre"),
        ("a_koimo_development",   "KOIMO Development GmbH",                            ["ar_bauherr_auftraggeber"],       "at_unternehmen"),
        ("a_concular",            "Concular",                                          ["ar_reuse_beratung"],             "at_unternehmen"),
        ("a_glasfischer_glastec", "Glasfischer Glastechnik",                           ["ar_aufbereitung_refurbishment"], "at_unternehmen"),
        ("a_gibbins_architekten", "Gibbins Architekten",                               ["ar_architektur"],                "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_in_bau"),
        r(pid, "HAT_INTERVENTION", "bai_sanierung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_remanufacturing"),
        r(pid, "HAT_METHODE", "meth_reuse_assessment"),
        r(pid, "HAT_HUERDE", "h_technische_freigabe"),
        r(pid, "HAT_HUERDE", "h_bauproduktstatus"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_reallabor"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg_rels
    return lines


def case_be_ware():
    q   = "q_be_ware_reallabor_berlin_md"
    pid = "p_be_ware_reallabor_berlin"
    bwr = "bw_be_ware_hub_spandau"
    bg1 = "bg_be_ware_altholz_tragwerk"
    lines = []

    lines.append(n(q, "Quelle", name="Be_Ware.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Be_Ware Reallabor Berlin – Tragwerke aus Sekundärmaterialien", bwr,
                               bewertung=3,
                               projektstatus_text="in Bau / Reallabor laufend",
                               note="Teilprojekte: TULIUM, Wasserrettungsstation, Jugendbauhuette"))

    bw_r, bwr_rels = bauwerk(bwr, "Be_Ware ReUse-Hub Berlin Spandau",
                              "bok_reuse_centre", "bor_empfaengerobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_in_bau", ["nut_gewerbe"], q)
    lines.append(bw_r)

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Altholz / Sekundärmaterialien als Tragwerk (mehrere Teilprojekte)", True,
        None, bwr, pid, q,
        types=["bt_traeger", "bt_wand", "bt_decke"], mats=["mat_holz"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_holzaufbereitung", "av_qualitaetssicherung"],
        rueckbau=["rv_selektiver_rueckbau", "rv_demontage"],
        pruefung=["pr_materialpruefung", "pr_statische_nachweisfuehrung"],
        la=["la_tragfaehigkeit", "la_brandschutz"],
        tp=["tp_skeletttragwerk"],
        bauweise=["bauw_holzbauweise"],
        status="status_in_bau",
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_natural_building_lab","Natural Building Lab TU Berlin", ["ar_forschung_dokumentation"], "at_forschung_lehre"),
        ("a_zrs_architekten",     "ZRS Architekten Ingenieure",     ["ar_architektur"],             "at_unternehmen"),
        ("a_dare_gmbh",           "DARE GmbH",                      ["ar_rueckbau_demontage"],      "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_in_bau"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_materialinventur"),
        r(pid, "HAT_METHODE", "meth_reuse_assessment"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_donorgebaeude"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_reallabor_be_ware"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg_rels
    return lines


def case_opalis():
    q   = "q_opalis_plattformfall_md"
    pid = "p_opalis_plattformfall"
    bwr = "bw_opalis_platform_brussels"
    lines = []

    lines.append(n(q, "Quelle", name="Opalis_Plattformfall.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_brussel", "Brüssel", "land_belgien", "Belgien", q)
    lines += on

    lines.append(projekt_base(pid, "Opalis – Digitale Plattform für wiedergewonnene Bauteile", bwr,
                               bewertung=2,
                               projektstatus_text="laufend seit ~2016"))

    bw_r, bwr_rels = bauwerk(bwr, "Opalis Online-Plattform",
                              "bok_reuse_centre", "bor_bestandsobjekt",
                              "stadt_brussel", "land_belgien",
                              "status_gebaut", ["nut_gewerbe"], q,
                              note="Digitale Plattform für Lieferanten und Käufer von wiedergewonnenen Baumaterialien")
    lines.append(bw_r)

    akteure_data = [
        ("a_rotor_vzw",    "Rotor vzw",    ["ar_forschung_dokumentation"], "at_ngo_netzwerk"),
        ("a_bellastock",   "Bellastock",   ["ar_forschung_dokumentation"], "at_ngo_netzwerk"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_brussel"),
        r(pid, "LIEGT_IN_LAND", "land_belgien"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_fcrbe"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_preuse"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


# ══════════════════════════════════════════════════════════════════════════════
# BATCH 019
# Cases: PREUSE, Haus_der_Materialisierung, Kunst_Stoffe_Berlin, Areal_Walkeweg_Nord
# Delta: prog_interreg_nwe
# ══════════════════════════════════════════════════════════════════════════════

def case_preuse():
    q   = "q_preuse_interreg_nwe_md"
    pid = "p_preuse_interreg_nwe"
    bwr = "bw_preuse_programme_context"
    lines = []

    lines.append(n(q, "Quelle", name="PREUSE.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_brussel", "Brüssel", "land_belgien", "Belgien", q)
    lines += on

    lines.append(projekt_base(pid, "PREUSE – EU Interreg NWE Reuse Centre Programme", bwr,
                               bewertung=2,
                               projektstatus_text="laufend 2024–2028",
                               budget_total_eur=6770000,
                               budget_eu_eur=4060000,
                               partner_anzahl=9))

    bw_r, bwr_rels = bauwerk(bwr, "PREUSE Programmkontext (Interreg NWE)",
                              "bok_reuse_centre", "bor_bestandsobjekt",
                              "stadt_brussel", "land_belgien",
                              "status_in_bau", ["nut_gewerbe"], q,
                              note="EU Interreg NWE; 9 Partner; 3 Pilot-ReUse-Centre-Formate; Belgien/Frankreich/NL/Luxemburg")
    lines.append(bw_r)

    akteure_data = [
        ("a_rotor_vzw",   "Rotor vzw",   ["ar_forschung_dokumentation"],             "at_ngo_netzwerk"),
        ("a_bellastock",  "Bellastock",  ["ar_forschung_dokumentation"],             "at_ngo_netzwerk"),
        ("a_interreg_nwe","Interreg NWE",["ar_oeffentliche_hand"],                   "at_foerdergeber_programmtraeger"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_brussel"),
        r(pid, "LIEGT_IN_LAND", "land_belgien"),
        r(pid, "HAT_STATUS", "status_in_bau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_preuse"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_interreg_nwe"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_haus_der_materialisierung():
    q   = "q_haus_der_materialisierung_berlin_md"
    pid = "p_haus_der_materialisierung_berlin"
    bwr = "bw_haus_der_materialisierung"
    lines = []

    lines.append(n(q, "Quelle", name="Haus_der_Materialisierung.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Haus der Materialisierung Berlin", bwr,
                               bewertung=2,
                               projektstatus_text="gebaut / laufend; ab Ende 2024 Otto-Braun-Str. 72",
                               note="Lokale Reuse-Infrastruktur / Materialdrehscheibe; Kunst-Stoffe + ZUsammenKUNFT"))

    bw_r, bwr_rels = bauwerk(bwr, "Haus der Materialisierung Berlin",
                              "bok_reuse_centre", "bor_bestandsobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_gebaut", ["nut_gewerbe", "nut_kultur"], q)
    lines.append(bw_r)

    akteure_data = [
        ("a_kunst_stoffe_ev",    "Kunst-Stoffe e.V.",     ["ar_materialhub_bauteilboerse"],  "at_ngo_netzwerk"),
        ("a_zusammenkunft_berlin","ZUsammenKUNFT Berlin eG",["ar_betreiber_nutzer"],          "at_organisation"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels
    return lines


def case_kunst_stoffe():
    q   = "q_kunst_stoffe_berlin_md"
    pid = "p_kunst_stoffe_berlin"
    bwr = "bw_kunst_stoffe_berlin"
    lines = []

    lines.append(n(q, "Quelle", name="Kunst_Stoffe_Berlin.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Kunst-Stoffe e.V. Berlin – Materialdrehscheibe", bwr,
                               bewertung=2,
                               projektstatus_text="laufend seit 2006"))

    bw_r, bwr_rels = bauwerk(bwr, "Kunst-Stoffe e.V. Berlin",
                              "bok_reuse_centre", "bor_bestandsobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_gebaut", ["nut_gewerbe"], q,
                              note="Materialaustauschzentrum seit 2006; vermittelt Materialien zwischen Firmen und Privat")
    lines.append(bw_r)

    nd_a, rl_a = akteur("a_kunst_stoffe_ev", "Kunst-Stoffe e.V.",
                         ["ar_materialhub_bauteilboerse"], "at_ngo_netzwerk", pid, q)
    lines.append(nd_a)

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + rl_a
    return lines


def case_areal_walkeweg_nord():
    q   = "q_areal_walkeweg_nord_basel_md"
    pid = "p_areal_walkeweg_nord_basel"
    bwr = "bw_areal_walkeweg_nord"
    bwd = "bw_lysbuechel_parkhaus_basel"
    bg1 = "bg_walkeweg_nord_betonfertigteile"
    lines = []

    lines.append(n(q, "Quelle", name="Areal_Walkeweg_Nord.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_basel", "Basel", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid, "Areal Walkeweg Nord Basel – Wohnungsbau Neubau", bwr,
                               bewertung=3,
                               projektstatus_text="geplant; Wettbewerb gewonnen",
                               co2_saving_t_erwartet=1000))

    bw_r, bwr_rels = bauwerk(bwr, "Areal Walkeweg Nord Basel",
                              "bok_quartier_areal", "bor_empfaengerobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_geplant", ["nut_wohnen"], q,
                              note="Neubau mit Betonfertigteil-Reuse; Lysbuechel-Parkhaus als Spender")
    bw_d, bwd_rels = bauwerk(bwd, "Lysbuechel Parkhaus Basel (Spender)",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_basel", "land_schweiz",
                              "status_rueckgebaut", ["nut_infrastruktur"], q)
    lines += [bw_r, bw_d]

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Betonfertigteile aus Lysbuechel Parkhaus (geplant)", True,
        bwd, bwr, pid, q,
        types=["bt_decke", "bt_traeger"], mats=["mat_stahlbeton"],
        wvas=["wva_direkte_wiederverwendung", "wva_urban_mining"],
        aufbereitung=["av_reinigung"],
        rueckbau=["rv_selektiver_rueckbau"],
        pruefung=["pr_materialpruefung"],
        bauweise=["bauw_fertigteilbauweise"],
        status="status_geplant",
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_parabase",               "PARABASE Architekten",   ["ar_architektur"],          "at_unternehmen"),
        ("a_immobilien_basel_stadt", "Immobilien Basel-Stadt", ["ar_bauherr_auftraggeber"], "at_oeffentliche_institution"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_basel"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_geplant"),
        r(pid, "HAT_INTERVENTION", "bai_neubau"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_urban_mining"),
        r(pid, "HAT_METHODE", "meth_bauteilkatalogisierung"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_ausschreibung"),
        r(pid, "TEIL_VON_PROGRAMM", "prog_wettbewerb"),
        r(pid, "NUTZT_BAUWERK", bwr),
        r(pid, "NUTZT_BAUWERK", bwd),
    ]
    lines += bwr_rels + bwd_rels + bg_rels
    return lines


# ══════════════════════════════════════════════════════════════════════════════
# BATCH 020
# Cases: Permanently_Temporary_Pavilion (stub), Rotor_DC_Brussels_Model (stub),
#        Halle_2, Altes_Hobelwerk_Winterthur
# ══════════════════════════════════════════════════════════════════════════════

def case_permanently_temporary():
    q   = "q_permanently_temporary_pavilion_md"
    pid = "p_permanently_temporary_pavilion"
    lines = []

    lines.append(n(q, "Quelle", name="Permanently_Temporary_Pavilion.md", quelltyp="case_markdown"))
    lines.append(projekt_base(pid, "Permanently Temporary Pavilion (Stub)", None,
                               bewertung=0,
                               projektstatus_text="unklar",
                               note="Leerer Stub; keine Fachinhalts-Daten vorhanden"))
    lines += [
        belegt(pid, q),
        r(pid, "HAT_STATUS", "status_unklar"),
    ]
    return lines


def case_rotor_dc_model():
    q   = "q_rotor_dc_brussels_model_md"
    pid = "p_rotor_dc_brussels_model"
    lines = []

    lines.append(n(q, "Quelle", name="Rotor_DC_Brussels_Model.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_brussel", "Brüssel", "land_belgien", "Belgien", q)
    lines += on

    lines.append(projekt_base(pid, "Rotor DC Brussels Model (Stub)", None,
                               bewertung=0,
                               projektstatus_text="unklar",
                               note="Leerer Stub; keine Fachinhalts-Daten vorhanden"))

    nd_a, rl_a = akteur("a_rotor_deconstruction", "Rotor Deconstruction / RotorDC",
                         ["ar_betreiber_nutzer"], "at_unternehmen", pid, q)
    lines.append(nd_a)

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_brussel"),
        r(pid, "LIEGT_IN_LAND", "land_belgien"),
        r(pid, "HAT_STATUS", "status_unklar"),
    ]
    lines += rl_a
    return lines


def case_halle_2():
    q   = "q_halle_2_ringberlin_berlin_md"
    pid = "p_halle_2_ringberlin_berlin"
    bwr = "bw_halle_2_ringberlin"
    bg1 = "bg_halle_2_drahtglas_donor"
    lines = []

    lines.append(n(q, "Quelle", name="Halle_2.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_berlin", "Berlin", "land_deutschland", "Deutschland", q)
    lines += on

    lines.append(projekt_base(pid, "Halle 2 ringberlin – Kontext Sheddach Drahtglas", bwr,
                               bewertung=1,
                               projektstatus_text="gebaut / Donorperspektive BIZH",
                               note="Kontext-Fallstudie; Halle 2 als Donorgebäude für BIZH Reallabor Drahtglas"))

    bw_r, bwr_rels = bauwerk(bwr, "Halle 2 ringberlin – Sheddach 1938",
                              "bok_gebaeude", "bor_donorobjekt",
                              "stadt_berlin", "land_deutschland",
                              "status_gebaut", ["nut_gewerbe"], q,
                              note="Sheddach-Industriehalle 1938; Drahtglasscheiben als Donor für BIZH Reallabor")
    lines.append(bw_r)

    bg_nd, bg_rels = bauteilgruppe(
        bg1, "Drahtglasscheiben aus Sheddach (Donorperspektive)", False,
        bwr, None, pid, q,
        types=["bt_fenster"], mats=["mat_glas"],
        wvas=["wva_remanufacturing"],
        aufbereitung=["av_drahtglasschneiden"],
        rueckbau=["rv_ausbau_von_bauteilen"],
        huerde=["h_technische_freigabe", "h_bauproduktstatus"],
        status="status_in_bau",
    )
    lines.append(bg_nd)

    akteure_data = [
        ("a_koimo_development",   "KOIMO Development GmbH", ["ar_bauherr_auftraggeber"], "at_unternehmen"),
        ("a_gibbins_architekten", "Gibbins Architekten",    ["ar_architektur"],          "at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_berlin"),
        r(pid, "LIEGT_IN_LAND", "land_deutschland"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_sanierung"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg_rels
    return lines


def case_altes_hobelwerk():
    q   = "q_altes_hobelwerk_winterthur_md"
    pid = "p_altes_hobelwerk_winterthur"
    bwr = "bw_altes_hobelwerk_winterthur"
    bg1 = "bg_altes_hobelwerk_mauerwerk_bruestung"
    bg2 = "bg_altes_hobelwerk_laminatplatten"
    lines = []

    lines.append(n(q, "Quelle", name="Altes_Hobelwerk_Winterthur.md", quelltyp="case_markdown"))
    on, or_ = ort_nodes("stadt_winterthur", "Winterthur", "land_schweiz", "Schweiz", q)
    lines += on

    lines.append(projekt_base(pid, "Altes Hobelwerk Winterthur – Minimalinvasive Bestandsaktivierung", bwr,
                               bewertung=3,
                               projektstatus_text="gebaut",
                               note="Ehemalige Hobelfabrik; reversible Aktivierung als Quartiersraum; unbeheizt"))

    bw_r, bwr_rels = bauwerk(bwr, "Altes Hobelwerk Winterthur (ehemalige Hobelfabrikhalle)",
                              "bok_gebaeude", "bor_bestandsobjekt",
                              "stadt_winterthur", "land_schweiz",
                              "status_gebaut", ["nut_gewerbe", "nut_kultur"], q,
                              note="Backsteinstruktur; sichtbare Stützen; weitgehend original; freistehender Boxeinbau für Sanitär+Teeküche")
    lines.append(bw_r)

    bg1_nd, bg1_rels = bauteilgruppe(
        bg1, "Mauerwerksbrüstung aus Abbruchmaterial (arealeigener Rückbau)", True,
        bwr, bwr, pid, q,
        types=["bt_wand", "bt_gelaender"], mats=["mat_ziegel", "mat_naturstein"],
        wvas=["wva_direkte_wiederverwendung", "wva_same_site_reuse"],
        aufbereitung=["av_reinigung", "av_reparatur"],
        rueckbau=["rv_selektiver_rueckbau"],
        fw=["fw_neue_funktion"],
    )
    bg2_nd, bg2_rels = bauteilgruppe(
        bg2, "Kasten aus recycelten Laminatfurnierplatten (Cirkla)", True,
        None, bwr, pid, q,
        types=["bt_ausbau"], mats=["mat_mdf"],
        wvas=["wva_direkte_wiederverwendung"],
        aufbereitung=["av_reinigung", "av_zuschnitt"],
        rueckbau=["rv_ausbau_von_bauteilen"],
        fw=["fw_neue_funktion"],
        note="Freistehender Einbau; reversibel; enthält Sanitär+Teeküche+Garderobe",
    )
    lines += [bg1_nd, bg2_nd]

    akteure_data = [
        ("a_bauburo_in_situ",    "baubüro in situ",                 ["ar_architektur"],         "at_unternehmen"),
        ("a_mehr_als_wohnen",    "Baugenossenschaft mehr als wohnen",["ar_bauherr_auftraggeber"],"at_organisation"),
        ("a_zirkular_cirkla",    "Zirkular / Cirkla",               ["ar_reuse_beratung"],      "at_unternehmen"),
        ("a_denkstatt",          "Denkstatt",                       ["ar_nachhaltigkeitsberatung"],"at_unternehmen"),
    ]
    for a_id, name, rollen, typ in akteure_data:
        nd, rl = akteur(a_id, name, rollen, typ, pid, q)
        lines.append(nd)
        lines += rl

    lines += or_
    lines += [
        belegt(pid, q),
        r(pid, "LIEGT_IN_STADT", "stadt_winterthur"),
        r(pid, "LIEGT_IN_LAND", "land_schweiz"),
        r(pid, "HAT_STATUS", "status_gebaut"),
        r(pid, "HAT_INTERVENTION", "bai_umbau"),
        r(pid, "HAT_INTERVENTION", "bai_umnutzung"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_bestandserhalt"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_same_site_reuse"),
        r(pid, "HAT_WIEDERVERWENDUNGSART", "wva_direkte_wiederverwendung"),
        r(pid, "HAT_METHODE", "meth_design_for_disassembly"),
        r(pid, "HAT_BESCHAFFUNGSWEG", "bweg_rueckbauprojekt"),
        r(pid, "HAT_RESSOURCENQUELLE", "rq_baustelle"),
        r(pid, "HAT_HUERDE", "h_datenluecke"),
        r(pid, "NUTZT_BAUWERK", bwr),
    ]
    lines += bwr_rels + bg1_rels + bg2_rels
    return lines


# ══════════════════════════════════════════════════════════════════════════════
# MAIN
# ══════════════════════════════════════════════════════════════════════════════

def main():
    print("Generating batches 015–020 …")

    # BATCH 015  ─────────────────────────────────────────────────────────────
    delta_015 = [
        n("bsys_iw73", "Bausystem", name="IW73/6_Plattenbausystem"),
    ]
    write_batch(15, {
        "controlled_terms.delta.jsonl": delta_015,
        "p_55_great_suffolk_street_london.kg.jsonl":  case_55_great_suffolk_street(),
        "p_association_house_groeditz.kg.jsonl":       case_association_groeditz(),
        "p_association_house_plauen.kg.jsonl":         case_association_plauen(),
        "p_bedzed_london_hackbridge.kg.jsonl":         case_bedzed(),
        "p_awm_muenster_circular_office.kg.jsonl":     case_awm_muenster(),
    })

    # BATCH 016  ─────────────────────────────────────────────────────────────
    write_batch(16, {
        "p_lysp8_basel_lysbuechelareal.kg.jsonl":                          case_lysp8_basel(),
        "p_elys_kultur_und_gewerbehaus_basel_lysbuechelareal.kg.jsonl":    case_elys_lysbuechelareal(),
        "p_elementa_walkeweg_basel.kg.jsonl":                              case_elementa(),
        "p_bestandshalle_crclr_house.kg.jsonl":                            case_bestandshalle_crclr(),
        "p_hobelwerk_haus_d_oberwinterthur.kg.jsonl":                      case_hobelwerk_haus_d(),
    })

    # BATCH 017  ─────────────────────────────────────────────────────────────
    write_batch(17, {
        "p_lysbuechel_parkhaus_basel.kg.jsonl":    case_lysbuechel_parkhaus(),
        "p_da_vinci_business_district_evere.kg.jsonl": case_da_vinci(),
        "p_reusebox_heilbronn.kg.jsonl":           case_reusebox_heilbronn(),
        "p_boell_lab_berlin.kg.jsonl":             case_boell_lab(),
        "p_crclr_house_berlin_overview.kg.jsonl":  case_crclr_overview(),
    })

    # BATCH 018  ─────────────────────────────────────────────────────────────
    write_batch(18, {
        "p_kindl_areal_berlin.kg.jsonl":           case_kindl_areal(),
        "p_bizh_reallabor_berlin.kg.jsonl":        case_bizh_reallabor(),
        "p_be_ware_reallabor_berlin.kg.jsonl":     case_be_ware(),
        "p_opalis_plattformfall.kg.jsonl":         case_opalis(),
    })

    # BATCH 019  ─────────────────────────────────────────────────────────────
    delta_019 = [
        n("prog_interreg_nwe", "Programm", name="Interreg_North_West_Europe"),
    ]
    write_batch(19, {
        "controlled_terms.delta.jsonl":                delta_019,
        "p_preuse_interreg_nwe.kg.jsonl":              case_preuse(),
        "p_haus_der_materialisierung_berlin.kg.jsonl": case_haus_der_materialisierung(),
        "p_kunst_stoffe_berlin.kg.jsonl":              case_kunst_stoffe(),
        "p_areal_walkeweg_nord_basel.kg.jsonl":        case_areal_walkeweg_nord(),
    })

    # BATCH 020  ─────────────────────────────────────────────────────────────
    write_batch(20, {
        "p_permanently_temporary_pavilion.kg.jsonl":   case_permanently_temporary(),
        "p_rotor_dc_brussels_model.kg.jsonl":          case_rotor_dc_model(),
        "p_halle_2_ringberlin_berlin.kg.jsonl":        case_halle_2(),
        "p_altes_hobelwerk_winterthur.kg.jsonl":       case_altes_hobelwerk(),
    })

    print("Done.")


if __name__ == "__main__":
    main()
