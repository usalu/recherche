"""Phase 11: per-BG optional vocab rels (the ~10 rel types Phase 6b skipped).

Maps each BG to its dossier-evidenced vocab targets across:
  HAT_BESCHAFFUNGSWEG, HAT_VERBINDUNGSTECHNIK, HAT_RUECKBAUVERFAHREN,
  HAT_AUFBEREITUNG, HAT_LOGISTIK, HAT_PRUEFUNG, HAT_DEFEKT,
  HAT_ZUSTANDSKLASSE (NEW rel type), HAT_BAUPRODUKTSTATUS,
  HAT_LEISTUNGSANFORDERUNG, HAT_SCHADSTOFF, HAT_MARKTMODELL,
  NUTZT_MATERIAL.

Only emits edges with BELEGT evidence in dossier. Generic patterns:
  - all 'reuse' BGs → HAT_BESCHAFFUNGSWEG (per dossier 'Beschaffungsweg' column)
  - dismantled BGs → HAT_RUECKBAUVERFAHREN
  - cleaned/refurbished BGs → HAT_AUFBEREITUNG
  - BGs from donor → HAT_AUFBEREITUNG (cleaning step)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

SRC = 'batch2_v2_followup_2026-05-20'

# Per-BG vocab spec
# Keys: bweg, vt, rv, av, log, pr, def, zk, bps, la, schadstoff, mm, mat
BG_VOCAB = {
    # ============ SMS Zürich ============
    'bg_retained_mehrere_mehrere_sms_zuerich_existing_bldgs': {
        'bweg': ['bweg_eigenbestand'], 'la': ['la_tragfaehigkeit','la_waermeschutz'],
        'pr': ['pr_dokumentenpruefung_bestand'], 'def': ['def_keine_befunde'],
        'zk': ['zk_unbekannt_pruefung_offen'], 'bps': ['bps_bestand_no_status'],
        'log': ['log_transport'],
    },
    'bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall': {
        'bweg': ['bweg_rueckbauprojekt'], 'rv': ['rv_selektiver_rueckbau'],
        'av': ['av_beton_anhaftungen_entfernen'], 'la': ['la_tragfaehigkeit','la_waermeschutz'],
        'pr': ['pr_statische_nachweisfuehrung','pr_dokumentenpruefung_bestand'],
        'def': ['def_oberflaechenmangel'], 'zk': ['zk_unbekannt_pruefung_offen'],
        'bps': ['bps_baupg_ch'], 'log': ['log_transport','log_zwischenlagerung'],
    },
    'bg_planned_stahl_fassade_sms_zuerich_arcade': {
        'vt': ['vt_verschraubung','vt_bolzenverbindung'], 'la': ['la_tragfaehigkeit'],
        'pr': ['pr_korrosionspruefung'], 'zk': ['zk_unbekannt_pruefung_offen'],
        'bps': ['bps_baupg_ch'],
    },
    'bg_retained_stahlbeton_treppe_sms_zuerich_existing_stairs': {
        'bweg': ['bweg_eigenbestand'], 'la': ['la_tragfaehigkeit'],
        'pr': ['pr_dokumentenpruefung_bestand'], 'def': ['def_keine_befunde'],
        'bps': ['bps_bestand_no_status'],
    },
    'bg_planned_mehrere_technik_sms_zuerich_pv_roof': {
        'la': ['la_dauerhaftigkeit'], 'bps': ['bps_ce_hen'],
    },
    # ============ UMAR ============
    'bg_reuse_holz_wand_umar_timber_facade': {
        'bweg': ['bweg_ausschreibung'], 'vt': ['vt_verschraubung','vt_steckverbindung'],
        'rv': ['rv_selektiver_rueckbau'], 'av': ['av_hobeln_schleifen_holz','av_holz_zuschnitt_reparatur'],
        'pr': ['pr_festigkeitssortierung_holz'], 'la': ['la_rueckbaubarkeit','la_waermeschutz'],
        'zk': ['zk_neuwertig'], 'def': ['def_keine_befunde'], 'bps': ['bps_baupg_ch'],
        'log': ['log_transport'], 'mat': ['mat_holz'],
    },
    'bg_reuse_metall_fassade_umar_alu_copper': {
        'vt': ['vt_verschraubung'], 'rv': ['rv_demontage'],
        'av': ['av_entrosten_korrosionsbehandlung','av_korrosionsschutz_beschichten'],
        'la': ['la_rueckbaubarkeit'], 'zk': ['zk_neuwertig'], 'bps': ['bps_baupg_ch'],
        'mat': ['mat_aluminium'],
    },
    'bg_reuse_metall_tuer_umar_wabbes_handles': {
        'bweg': ['bweg_direktvermittlung'], 'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_reinigung','av_rekonditionierung'], 'la': ['la_rueckbaubarkeit'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'def': ['def_keine_befunde'],
        'pr': ['pr_dokumentenpruefung_bestand'], 'bps': ['bps_project_specific'],
        'log': ['log_lagerung','log_transport'], 'mm': ['mm_leasing'],
        # mat_messing doesn't exist in live graph; suggested new node — see NEW_NODE_SUGGESTIONS.md
    },
    'bg_reuse_glas_keramik_fassade_umar_magna_glass': {
        'bweg': ['bweg_direktvermittlung'], 'av': ['av_remanufacturing','av_glas_pruefung_sortierung'],
        'la': ['la_rueckbaubarkeit'], 'zk': ['zk_neuwertig'], 'bps': ['bps_baupg_ch'],
        'mat': ['mat_glas'],  # "recycled" aspect already captured by wva_recycling/wva_upcycling
    },
    'bg_reuse_daemmstoff_daemmung_umar_mycelium': {
        'vt': ['vt_reversible_fuegung'], 'rv': ['rv_demontage'],
        'la': ['la_rueckbaubarkeit','la_waermeschutz'], 'zk': ['zk_neuwertig'],
        'bps': ['bps_project_specific'],
    },
    'bg_reuse_kunststoff_boden_umar_carpets': {
        'bweg': ['bweg_leihmodell'], 'rv': ['rv_ausbau_von_bauteilen'],
        'av': ['av_remanufacturing'], 'la': ['la_rueckbaubarkeit'], 'zk': ['zk_neuwertig'],
        'bps': ['bps_baupg_ch'], 'log': ['log_transport'], 'mm': ['mm_take_back_service'],
    },
    'bg_reuse_verbundstoff_decke_umar_lindner_ceiling': {
        'bweg': ['bweg_leihmodell'], 'vt': ['vt_verschraubung','vt_klemmverbindung'],
        'rv': ['rv_demontage'], 'la': ['la_rueckbaubarkeit'], 'zk': ['zk_neuwertig'],
        'bps': ['bps_baupg_ch'], 'log': ['log_transport'], 'mm': ['mm_take_back_service'],
    },
    'bg_reuse_mineralisch_wand_umar_recycled_bricks': {
        'bweg': ['bweg_lager'], 'rv': ['rv_ausbau_von_bauteilen'],
        'av': ['av_moertelentfernung_ziegel'], 'zk': ['zk_gebrauchsspuren_funktional'],
        'bps': ['bps_project_specific'],
    },
    # ============ ELEMENTA ============
    'bg_reuse_mineralisch_stuetze_elementa_baufeld_c': {
        'bweg': ['bweg_bauteilboerse','bweg_digitale_plattform','bweg_rueckbauprojekt'],
        'vt': ['vt_bolzenverbindung','vt_verschraubung'], 'rv': ['rv_selektiver_rueckbau'],
        'av': ['av_beton_anhaftungen_entfernen','av_betonfertigteil_tagging_sortierung','av_betonfertigteil_saegen'],
        'pr': ['pr_bohrkernpruefung_beton','pr_dokumentenpruefung_bestand','pr_statische_nachweisfuehrung','pr_schadstoffpruefung'],
        'la': ['la_tragfaehigkeit','la_dauerhaftigkeit'], 'def': ['def_oberflaechenmangel','def_karbonatisierung'],
        'zk': ['zk_unbekannt_pruefung_offen'], 'bps': ['bps_project_specific','bps_baupg_ch'],
        'schadstoff': ['s_pak','s_asbest'],
        'log': ['log_just_in_time','log_materialmatching','log_lokale_wiederverwendung','log_zwischenlagerung','log_bauteiltracking'],
    },
    'bg_reuse_mineralisch_wand_elementa_baufeld_d': {
        'bweg': ['bweg_bauteilboerse','bweg_rueckbauprojekt'], 'vt': ['vt_verschraubung'],
        'rv': ['rv_selektiver_rueckbau'], 'av': ['av_beton_anhaftungen_entfernen','av_betonfertigteil_tagging_sortierung'],
        'pr': ['pr_bohrkernpruefung_beton','pr_statische_nachweisfuehrung'],
        'la': ['la_tragfaehigkeit','la_dauerhaftigkeit'], 'zk': ['zk_unbekannt_pruefung_offen'],
        'bps': ['bps_project_specific','bps_baupg_ch'], 'schadstoff': ['s_pak','s_asbest'],
        'log': ['log_just_in_time','log_materialmatching','log_zwischenlagerung'],
    },
    'bg_planned_holz_decke_elementa_brettstapel': {
        'vt': ['vt_steckverbindung'], 'zk': ['zk_neuwertig'], 'bps': ['bps_baupg_ch'],
        'la': ['la_waermeschutz','la_schallschutz'],
    },
    'bg_planned_lehm_erde_wand_elementa_clay': {
        'av': ['av_lehm_sieben_mischen'], 'zk': ['zk_neuwertig'],
        'la': ['la_waermeschutz','la_feuchteschutz'],
    },
    # ============ Careno tiles ============
    'bg_reuse_glas_keramik_boden_careno_historic_tiles': {
        'bweg': ['bweg_rueckbauprojekt'], 'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_entmoertelung_von_fliesen','av_reinigung','av_materialsortierung_chargenbildung'],
        'pr': ['pr_dokumentenpruefung_bestand'], 'def': ['def_riss','def_oberflaechenmangel'],
        'zk': ['zk_unbekannt_pruefung_offen'], 'bps': ['bps_project_specific'],
        'log': ['log_lagerung','log_materialverfuegbarkeit'], 'schadstoff': ['s_bleifarbe'],
    },
    'bg_reuse_glas_keramik_boden_careno_retile_cleaned': {
        'bweg': ['bweg_digitale_plattform','bweg_lager'],
        'av': ['av_entmoertelung_von_fliesen','av_qualitaetssicherung'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'def': ['def_keine_befunde'],
        'bps': ['bps_project_specific'], 'log': ['log_bauteiltracking'],
        'mm': ['mm_plattform_vermittelt'],
    },
    'bg_reuse_glas_keramik_boden_careno_rotor_stock': {
        'bweg': ['bweg_lager','bweg_digitale_plattform'], 'av': ['av_qualitaetssicherung'],
        'log': ['log_bauteiltracking','log_materialverfuegbarkeit'],
        'mm': ['mm_plattform_vermittelt'],
    },
    # ============ Circl ============
    'bg_reuse_holz_boden_circl_window_frame_floor': {
        'bweg': ['bweg_rueckbauprojekt'], 'av': ['av_holz_zuschnitt_reparatur','av_hobeln_schleifen_holz'],
        'la': ['la_rueckbaubarkeit'], 'zk': ['zk_gebrauchsspuren_funktional'],
        'mat': ['mat_holz'],
    },
    'bg_dismantled_holz_mehrere_circl_larch_structure': {
        'bweg': ['bweg_direktvermittlung'], 'vt': ['vt_reversible_fuegung','vt_verschraubung'],
        'rv': ['rv_selektiver_rueckbau','rv_demontage'],
        'av': ['av_holz_festigkeitssortierung','av_holz_trocknung_feuchtekonditionierung'],
        'pr': ['pr_festigkeitssortierung_holz','pr_dokumentenpruefung_bestand'],
        'la': ['la_rueckbaubarkeit','la_tragfaehigkeit'], 'zk': ['zk_gebrauchsspuren_funktional'],
        'bps': ['bps_nta_8713'], 'log': ['log_bauteiltracking','log_lagerung','log_lokale_wiederverwendung'],
        'mat': ['mat_holz_larche'] if False else ['mat_holz'],  # mat_holz_larche may not exist; fallback to mat_holz
    },
    'bg_reuse_daemmstoff_daemmung_circl_jeans_insulation': {
        'bweg': ['bweg_spende','bweg_informelles_netzwerk'], 'la': ['la_waermeschutz','la_schallschutz'],
        'zk': ['zk_neuwertig'], 'bps': ['bps_project_specific'], 'mm': ['mm_spende'],
    },
    'bg_reuse_mehrere_fenster_circl_conference_windows': {
        'bweg': ['bweg_rueckbauprojekt'], 'rv': ['rv_zerstoerungsarme_bergung','rv_ausbau_von_bauteilen'],
        'av': ['av_fenster_refurbishment'], 'zk': ['zk_gebrauchsspuren_funktional'],
        'bps': ['bps_nta_8713'], 'log': ['log_transport'],
    },
    'bg_reuse_metall_technik_circl_fire_hose_cabinets': {
        'bweg': ['bweg_direktvermittlung','bweg_digitale_plattform'],
        'rv': ['rv_ausbau_von_bauteilen'], 'av': ['av_reinigung','av_entrosten_korrosionsbehandlung'],
        'pr': ['pr_korrosionspruefung'], 'def': ['def_korrosion'], 'zk': ['zk_gebrauchsspuren_funktional'],
        'bps': ['bps_nta_8713'], 'mm': ['mm_plattform_vermittelt'],
    },
    'bg_reuse_textil_wand_circl_clothing_felt': {
        'bweg': ['bweg_eigenbestand','bweg_spende'], 'zk': ['zk_neuwertig'],
        'la': ['la_schallschutz'], 'bps': ['bps_project_specific'], 'mm': ['mm_intra_konzern'],
    },
    'bg_dismantled_mehrere_technik_circl_solar_panels': {
        'rv': ['rv_demontage'], 'def': ['def_oberflaechenmangel'],
        'zk': ['zk_eingeschraenkt_nutzungsklasse_reduzieren'],
        'pr': ['pr_dokumentenpruefung_bestand'], 'la': ['la_dauerhaftigkeit'],
    },
    # ============ LysP8 ============
    'bg_reuse_mehrere_fassade_lysp8_external_mix': {
        'bweg': ['bweg_rueckbauprojekt','bweg_bauteilboerse'],
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_reinigung'], 'la': ['la_waermeschutz','la_dauerhaftigkeit'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'bps': ['bps_baupg_ch'],
        'log': ['log_lagerung','log_transport','log_bauteiltracking'],
        'mm': ['mm_kauf_gebraucht'],
    },
    'bg_reuse_holz_ausbau_lysp8_kitchens': {
        'bweg': ['bweg_rueckbauprojekt','bweg_direktvermittlung'],
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_reinigung','av_holz_zuschnitt_reparatur'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'def': ['def_oberflaechenmangel'],
        'log': ['log_lagerung','log_transport'], 'mm': ['mm_kauf_gebraucht'],
        'mat': ['mat_holz'],
    },
    'bg_reuse_metall_boden_lysp8_grating_steps': {
        'bweg': ['bweg_rueckbauprojekt'], 'rv': ['rv_ausbau_von_bauteilen'],
        'av': ['av_entrosten_korrosionsbehandlung'], 'pr': ['pr_korrosionspruefung'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'def': ['def_korrosion'],
        'mat': ['mat_stahl'],
    },
    'bg_reuse_mehrere_ausbau_lysp8_doors_tiles': {
        'bweg': ['bweg_rueckbauprojekt','bweg_bauteilboerse'],
        'av': ['av_reinigung'], 'zk': ['zk_gebrauchsspuren_funktional'],
        'mm': ['mm_kauf_gebraucht'],
    },
    'bg_planned_holz_mehrere_lysp8_dfd_frame': {
        'vt': ['vt_verschraubung','vt_steckverbindung','vt_reversible_fuegung'],
        'la': ['la_rueckbaubarkeit','la_tragfaehigkeit'], 'zk': ['zk_neuwertig'],
        'bps': ['bps_baupg_ch'], 'mat': ['mat_holz'],
    },
    'bg_planned_lehm_erde_boden_lysp8_oxacrete': {
        'av': ['av_lehm_sieben_mischen'], 'zk': ['zk_neuwertig'],
        'la': ['la_feuchteschutz','la_waermeschutz'], 'bps': ['bps_project_specific'],
    },
    # ============ MedUni ============
    'bg_reuse_mehrere_technik_medunicampus_paternoster': {
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_reinigung'], 'log': ['log_transport','log_lagerung'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'mm': ['mm_spende'],  # to museum
    },
    'bg_reuse_holz_wand_medunicampus_doors_as_cladding': {
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_reinigung','av_hobeln_schleifen_holz'],
        'zk': ['zk_gebrauchsspuren_funktional'], 'log': ['log_lagerung'],
        'mat': ['mat_holz'],
    },
    'bg_retained_mehrere_decke_medunicampus_glasdecke': {
        'bweg': ['bweg_eigenbestand'], 'pr': ['pr_dokumentenpruefung_bestand'],
        'zk': ['zk_unbekannt_pruefung_offen'], 'bps': ['bps_bestand_no_status'],
    },
    # ============ Stuttgart 210 / Ingersheim ============
    'bg_reuse_holz_mehrere_ingersheim_clt_structure': {
        'bweg': ['bweg_rueckbauprojekt','bweg_direktvermittlung'],
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_hobeln_schleifen_holz','av_holz_zuschnitt_reparatur','av_holz_festigkeitssortierung'],
        'pr': ['pr_festigkeitssortierung_holz','pr_dokumentenpruefung_bestand','pr_statische_nachweisfuehrung'],
        'la': ['la_tragfaehigkeit','la_dauerhaftigkeit'],
        'zk': ['zk_gebrauchsspuren_funktional'],
        'bps': ['bps_zie_vbg'],  # ZiE/vBG approval needed for non-standard reuse
        'log': ['log_transport','log_just_in_time'], 'mm': ['mm_forschungsprojekt_zuteilung'],
        'mat': ['mat_holz'],
    },
    'bg_dismantled_holz_mehrere_stuttgart21_donor_stock': {
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'log': ['log_lagerung','log_bauteiltracking','log_zwischenlagerung'],
        'zk': ['zk_unbekannt_pruefung_offen'],
        'mat': ['mat_holz'],
    },
    # ============ Granby ============
    'bg_reuse_mehrere_boden_granby_rock_terrazzo': {
        'bweg': ['bweg_informelles_netzwerk','bweg_lager'],
        'av': ['av_naturstein_reinigung_schleifen_zuschnitt'],  # crushing+grinding+polishing
        'la': ['la_dauerhaftigkeit'], 'mm': ['mm_kauf_gebraucht'],
    },
    'bg_reuse_ziegel_boden_granby_brick_slate_terrazzo': {
        'bweg': ['bweg_informelles_netzwerk','bweg_lager'],
        'av': ['av_moertelentfernung_ziegel','av_naturstein_reinigung_schleifen_zuschnitt'],
        'la': ['la_dauerhaftigkeit'], 'mm': ['mm_kauf_gebraucht'],
    },
    # ============ ETH ============
    'bg_reuse_mehrere_mehrere_eggshell_recycled_structure': {
        'vt': ['vt_reversible_fuegung'], 'la': ['la_rueckbaubarkeit'],
        'zk': ['zk_neuwertig'],
    },
    'bg_reuse_holz_mehrere_upsticks_timber_frame': {
        'vt': ['vt_steckverbindung','vt_reversible_fuegung'],
        'la': ['la_rueckbaubarkeit','la_tragfaehigkeit'], 'zk': ['zk_neuwertig'],
        'mat': ['mat_holz'],
    },
}

# Rel type per slot key
SLOT_TO_REL = {
    'bweg': 'HAT_BESCHAFFUNGSWEG',
    'vt': 'HAT_VERBINDUNGSTECHNIK',
    'rv': 'HAT_RUECKBAUVERFAHREN',
    'av': 'HAT_AUFBEREITUNG',
    'log': 'HAT_LOGISTIK',
    'pr': 'HAT_PRUEFUNG',
    'def': 'HAT_DEFEKT',
    'zk': 'HAT_ZUSTANDSKLASSE',  # NEW REL TYPE — first use
    'bps': 'HAT_BAUPRODUKTSTATUS',
    'la': 'HAT_LEISTUNGSANFORDERUNG',
    'schadstoff': 'HAT_SCHADSTOFF',
    'mm': 'HAT_MARKTMODELL',
    'mat': 'NUTZT_MATERIAL',
}


def emit_rels() -> list[dict]:
    rels: list[dict] = []
    for bg_id, slots in BG_VOCAB.items():
        for slot_key, targets in slots.items():
            rel_type = SLOT_TO_REL[slot_key]
            for target in targets:
                rid = f'r_{bg_id}__{rel_type}__{target}'
                rels.append({
                    'op': 'add_rel',
                    'from': bg_id,
                    'type': rel_type,
                    'to': target,
                    'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                    'reason': f'Phase 11: per-BG vocab rel ({rel_type}); dossier-evidenced.',
                    'severity': 'LOW',
                })
    return rels


def main() -> int:
    rels = emit_rels()
    out = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_11_bg_vocab.patch.jsonl')
    with out.open('w', encoding='utf-8') as f:
        for r in rels:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Wrote {len(rels)} BG-level vocab rel ops to {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
