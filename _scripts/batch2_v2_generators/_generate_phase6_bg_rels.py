"""Generate Phase 6b/6c/6d BG rels JSONL from compact spec table.

For each BG, emits the mandatory rels:
  HAT_BAUTEILEBENE, HAT_STATUS, HAT_RESSOURCENQUELLE,
  HAT_BAUTEILTYP, HAT_MATERIALGRUPPE, HAT_WIEDERVERWENDUNGSART,
  BELEGT_IN.

Plus Project + Bauwerk links and Funktionswechsel (HAT_MATCHINGQUALITAET).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

SRC = 'batch2_v2_import_2026-05-20'

# Spec table: each entry is a dict per BG with mandatory + optional rel targets.
# Format (compact): list of dicts with keys:
#   id, bauteilebene (default be_bauteilgruppe), status, ressourcenquelle,
#   bauteiltyp (mandatory id), materialgruppe, wiederverwendungsart,
#   quelle (BELEGT_IN target), projekt (HAT_BAUTEILGRUPPE source),
#   eingebaut_in (Bauwerk receiver), aus_bauwerk (Bauwerk donor, optional),
#   funktionswechsel (True if HAT_MATCHINGQUALITAET → mq_spec_zweckaenderung)

BGS = [
  # SMS Zürich
  {'id': 'bg_retained_mehrere_mehrere_sms_zuerich_existing_bldgs', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_bestandserhalt', 'quelle': 'qu_batch1_schaerenmoosstrasse_dossier', 'projekt': 'p_schaerenmoosstrasse_zuerich', 'eingebaut_in': 'bw_schaerenmoosstrasse_zuerich'},
  {'id': 'bg_reuse_mehrere_mehrere_sms_zuerich_ubs_hall', 'status': 'status_geplant', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_decke', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_schaerenmoosstrasse_dossier', 'projekt': 'p_schaerenmoosstrasse_zuerich', 'eingebaut_in': 'bw_schaerenmoosstrasse_zuerich', 'aus_bauwerk': 'bw_ubs_altstetten'},
  {'id': 'bg_planned_stahl_fassade_sms_zuerich_arcade', 'status': 'status_geplant', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_traeger', 'materialgruppe': 'mg_metall', 'wva': 'wva_design_for_disassembly', 'quelle': 'qu_batch1_schaerenmoosstrasse_dossier', 'projekt': 'p_schaerenmoosstrasse_zuerich', 'eingebaut_in': 'bw_schaerenmoosstrasse_zuerich'},
  {'id': 'bg_retained_stahlbeton_treppe_sms_zuerich_existing_stairs', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_treppe', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_bestandserhalt', 'quelle': 'qu_batch1_schaerenmoosstrasse_dossier', 'projekt': 'p_schaerenmoosstrasse_zuerich', 'eingebaut_in': 'bw_schaerenmoosstrasse_zuerich'},
  {'id': 'bg_planned_mehrere_technik_sms_zuerich_pv_roof', 'status': 'status_geplant', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_technik', 'materialgruppe': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_schaerenmoosstrasse_dossier', 'projekt': 'p_schaerenmoosstrasse_zuerich', 'eingebaut_in': 'bw_schaerenmoosstrasse_zuerich'},
  # UMAR
  {'id': 'bg_reuse_holz_wand_umar_timber_facade', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_design_for_disassembly', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  {'id': 'bg_reuse_metall_fassade_umar_alu_copper', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_fassade', 'materialgruppe': 'mg_metall', 'wva': 'wva_recycling', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  {'id': 'bg_reuse_metall_tuer_umar_wabbes_handles', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_tuer', 'materialgruppe': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf', 'aus_bauwerk': 'bw_generale_de_banque_brussels', 'funktionswechsel': True},
  {'id': 'bg_reuse_glas_keramik_fassade_umar_magna_glass', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_fassade', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_upcycling', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  {'id': 'bg_reuse_daemmstoff_daemmung_umar_mycelium', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_daemmung', 'materialgruppe': 'mg_daemmstoff', 'wva': 'wva_recycling', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  {'id': 'bg_reuse_kunststoff_boden_umar_carpets', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_kunststoff', 'wva': 'wva_recycling', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  {'id': 'bg_reuse_verbundstoff_decke_umar_lindner_ceiling', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_decke', 'materialgruppe': 'mg_verbundstoff', 'wva': 'wva_design_for_disassembly', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  {'id': 'bg_reuse_mineralisch_wand_umar_recycled_bricks', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_umar_dossier', 'projekt': 'p_umar_unit', 'eingebaut_in': 'bw_umar_unit_duebendorf'},
  # ELEMENTA
  {'id': 'bg_reuse_mineralisch_stuetze_elementa_baufeld_c', 'status': 'status_geplant', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_stuetze', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_elementa_dossier', 'projekt': 'p_elementa_walkeweg', 'eingebaut_in': 'bw_elementa_walkeweg_basel', 'aus_bauwerk': 'bw_lysbueechel_garage_basel'},
  {'id': 'bg_reuse_mineralisch_wand_elementa_baufeld_d', 'status': 'status_geplant', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_elementa_dossier', 'projekt': 'p_elementa_walkeweg', 'eingebaut_in': 'bw_elementa_walkeweg_basel', 'aus_bauwerk': 'bw_lysbueechel_garage_basel'},
  {'id': 'bg_planned_holz_decke_elementa_brettstapel', 'status': 'status_geplant', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_decke', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_weiterbauen_im_bestand', 'quelle': 'qu_batch1_elementa_dossier', 'projekt': 'p_elementa_walkeweg', 'eingebaut_in': 'bw_elementa_walkeweg_basel'},
  {'id': 'bg_planned_lehm_erde_wand_elementa_clay', 'status': 'status_geplant', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_lehm_erde', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_batch1_elementa_dossier', 'projekt': 'p_elementa_walkeweg', 'eingebaut_in': 'bw_elementa_walkeweg_basel'},
  # Careno (material charge — be_materialcharge; no EINGEBAUT_IN)
  {'id': 'bg_reuse_glas_keramik_boden_careno_historic_tiles', 'bauteilebene': 'be_materialcharge', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_careno_becircular_dossier', 'projekt': 'p_careno_becircular'},
  {'id': 'bg_reuse_glas_keramik_boden_careno_retile_cleaned', 'bauteilebene': 'be_materialcharge', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_careno_becircular_dossier', 'projekt': 'p_careno_becircular'},
  {'id': 'bg_reuse_glas_keramik_boden_careno_rotor_stock', 'bauteilebene': 'be_materialcharge', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_careno_becircular_dossier', 'projekt': 'p_careno_becircular'},
  # Circl
  {'id': 'bg_reuse_holz_boden_circl_window_frame_floor', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_upcycling', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam', 'funktionswechsel': True},
  {'id': 'bg_dismantled_holz_mehrere_circl_larch_structure', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_traeger', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_design_for_disassembly', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam'},
  {'id': 'bg_reuse_daemmstoff_daemmung_circl_jeans_insulation', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_daemmung', 'materialgruppe': 'mg_daemmstoff', 'wva': 'wva_upcycling', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam', 'funktionswechsel': True},
  {'id': 'bg_reuse_mehrere_fenster_circl_conference_windows', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_fenster', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam'},
  {'id': 'bg_reuse_metall_technik_circl_fire_hose_cabinets', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_technik', 'materialgruppe': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam'},
  {'id': 'bg_reuse_textil_wand_circl_clothing_felt', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_kunststoff', 'wva': 'wva_upcycling', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam', 'funktionswechsel': True},
  {'id': 'bg_dismantled_mehrere_technik_circl_solar_panels', 'status': 'status_rueckgebaut', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_technik', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro', 'eingebaut_in': 'bw_circl_pavilion_amsterdam'},
  # LysP8
  {'id': 'bg_reuse_mehrere_fassade_lysp8_external_mix', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_fassade', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_lysp8_basel_dossier', 'projekt': 'p_lysp8_basel', 'eingebaut_in': 'bw_lysp8_basel'},
  {'id': 'bg_reuse_holz_ausbau_lysp8_kitchens', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_ausbau', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_lysp8_basel_dossier', 'projekt': 'p_lysp8_basel', 'eingebaut_in': 'bw_lysp8_basel'},
  {'id': 'bg_reuse_metall_boden_lysp8_grating_steps', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_lysp8_basel_dossier', 'projekt': 'p_lysp8_basel', 'eingebaut_in': 'bw_lysp8_basel'},
  {'id': 'bg_reuse_mehrere_ausbau_lysp8_doors_tiles', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_ausbau', 'materialgruppe': 'mg_mehrere', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_lysp8_basel_dossier', 'projekt': 'p_lysp8_basel', 'eingebaut_in': 'bw_lysp8_basel'},
  {'id': 'bg_planned_holz_mehrere_lysp8_dfd_frame', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_traeger', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_design_for_disassembly', 'quelle': 'qu_lysp8_basel_dossier', 'projekt': 'p_lysp8_basel', 'eingebaut_in': 'bw_lysp8_basel'},
  {'id': 'bg_planned_lehm_erde_boden_lysp8_oxacrete', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_lehm_erde', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_lysp8_basel_dossier', 'projekt': 'p_lysp8_basel', 'eingebaut_in': 'bw_lysp8_basel'},
  # MedUni (donor batches, no EINGEBAUT_IN — components go to external receivers)
  {'id': 'bg_reuse_mehrere_technik_medunicampus_paternoster', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_technik', 'materialgruppe': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_meduni_mariannengasse_dossier', 'projekt': 'p_meduni_campus_mariannengasse', 'aus_bauwerk': 'bw_meduni_campus_mariannengasse'},
  {'id': 'bg_reuse_holz_wand_medunicampus_doors_as_cladding', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_wand', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_upcycling', 'quelle': 'qu_meduni_mariannengasse_dossier', 'projekt': 'p_meduni_campus_mariannengasse', 'aus_bauwerk': 'bw_meduni_campus_mariannengasse', 'funktionswechsel': True},
  {'id': 'bg_retained_mehrere_decke_medunicampus_glasdecke', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_decke', 'materialgruppe': 'mg_glas_keramik', 'wva': 'wva_bestandserhalt', 'quelle': 'qu_meduni_mariannengasse_dossier', 'projekt': 'p_meduni_campus_mariannengasse', 'eingebaut_in': 'bw_meduni_campus_mariannengasse'},
  # Stuttgart 210 / Jugendtreff Ingersheim
  {'id': 'bg_reuse_holz_mehrere_ingersheim_clt_structure', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_donorgebaeude', 'bauteiltyp': 'bt_traeger', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'quelle': 'qu_stuttgart210_dossier', 'projekt': 'p_jugendtreff_ingersheim', 'eingebaut_in': 'bw_jugendtreff_ingersheim', 'aus_bauwerk': 'bw_stuttgart21_hauptbahnhof', 'funktionswechsel': True},
  {'id': 'bg_dismantled_holz_mehrere_stuttgart21_donor_stock', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_mehrere', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_urban_mining', 'quelle': 'qu_stuttgart210_dossier', 'projekt': 'prog_stuttgart_210', 'aus_bauwerk': 'bw_stuttgart21_hauptbahnhof'},
  # Granby (no specific EINGEBAUT_IN — products go to external markets)
  {'id': 'bg_reuse_mehrere_boden_granby_rock_terrazzo', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_mehrere', 'wva': 'wva_recycling', 'quelle': 'qu_granby_workshop_dossier', 'projekt': 'p_granby_workshop', 'funktionswechsel': True},
  {'id': 'bg_reuse_ziegel_boden_granby_brick_slate_terrazzo', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_lager', 'bauteiltyp': 'bt_boden', 'materialgruppe': 'mg_mineralisch', 'wva': 'wva_recycling', 'quelle': 'qu_granby_workshop_dossier', 'projekt': 'p_granby_workshop', 'funktionswechsel': True},
  # ETH
  {'id': 'bg_reuse_mehrere_mehrere_eggshell_recycled_structure', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_traeger', 'materialgruppe': 'mg_mehrere', 'wva': 'wva_recycling', 'quelle': 'qu_eth_mas_dfab_dossier', 'projekt': 'p_eggshell_pavilion'},
  {'id': 'bg_reuse_holz_mehrere_upsticks_timber_frame', 'status': 'status_realisiert', 'ressourcenquelle': 'rq_baustelle', 'bauteiltyp': 'bt_traeger', 'materialgruppe': 'mg_holz_biobasiert', 'wva': 'wva_design_for_disassembly', 'quelle': 'qu_eth_mas_dfab_dossier', 'projekt': 'p_up_sticks_dundee'},
]


def emit_rels() -> list[dict]:
    rels: list[dict] = []
    src = SRC
    for bg in BGS:
        bid = bg['id']
        be = bg.get('bauteilebene', 'be_bauteilgruppe')
        # 1. HAT_BAUTEILEBENE
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_BAUTEILEBENE', 'to': be,
                     'properties': {'id': f'r_{bid}__HAT_BAUTEILEBENE__{be}', 'source': src},
                     'reason': 'Phase 6b + O1.', 'severity': 'LOW'})
        # 2. HAT_STATUS
        st = bg['status']
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_STATUS', 'to': st,
                     'properties': {'id': f'r_{bid}__HAT_STATUS__{st}', 'source': src},
                     'reason': 'Phase 6b + O2.', 'severity': 'LOW'})
        # 3. HAT_RESSOURCENQUELLE
        rq = bg['ressourcenquelle']
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_RESSOURCENQUELLE', 'to': rq,
                     'properties': {'id': f'r_{bid}__HAT_RESSOURCENQUELLE__{rq}', 'source': src},
                     'reason': 'Phase 6b + O3.', 'severity': 'LOW'})
        # 4. HAT_BAUTEILTYP
        bt = bg['bauteiltyp']
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_BAUTEILTYP', 'to': bt,
                     'properties': {'id': f'r_{bid}__HAT_BAUTEILTYP__{bt}', 'source': src},
                     'reason': 'Phase 6b.', 'severity': 'LOW'})
        # 5. HAT_MATERIALGRUPPE
        mg = bg['materialgruppe']
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_MATERIALGRUPPE', 'to': mg,
                     'properties': {'id': f'r_{bid}__HAT_MATERIALGRUPPE__{mg}', 'source': src},
                     'reason': 'Phase 6b.', 'severity': 'LOW'})
        # 6. HAT_WIEDERVERWENDUNGSART
        wva = bg['wva']
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_WIEDERVERWENDUNGSART', 'to': wva,
                     'properties': {'id': f'r_{bid}__HAT_WIEDERVERWENDUNGSART__{wva}', 'source': src},
                     'reason': 'Phase 6b.', 'severity': 'LOW'})
        # 7. BELEGT_IN
        q = bg['quelle']
        rels.append({'op': 'add_rel', 'from': bid, 'type': 'BELEGT_IN', 'to': q,
                     'properties': {'id': f'r_{bid}__BELEGT_IN__{q}', 'source': src},
                     'reason': 'Phase 6b.', 'severity': 'LOW'})
        # Bauwerk + Project links
        if 'eingebaut_in' in bg:
            bw = bg['eingebaut_in']
            rels.append({'op': 'add_rel', 'from': bid, 'type': 'EINGEBAUT_IN', 'to': bw,
                         'properties': {'id': f'r_{bid}__EINGEBAUT_IN__{bw}', 'source': src},
                         'reason': 'Phase 6c + C7: BG to receiving Bauwerk.', 'severity': 'LOW'})
        if 'aus_bauwerk' in bg:
            bw = bg['aus_bauwerk']
            rels.append({'op': 'add_rel', 'from': bid, 'type': 'AUS_BAUWERK', 'to': bw,
                         'properties': {'id': f'r_{bid}__AUS_BAUWERK__{bw}', 'source': src},
                         'reason': 'Phase 6c + C4: BG to donor Bauwerk.', 'severity': 'LOW'})
        if 'projekt' in bg:
            p = bg['projekt']
            rels.append({'op': 'add_rel', 'from': p, 'type': 'HAT_BAUTEILGRUPPE', 'to': bid,
                         'properties': {'id': f'r_{p}__HAT_BAUTEILGRUPPE__{bid}', 'source': src},
                         'reason': 'Phase 6c: Projekt to BG.', 'severity': 'LOW'})
        # Funktionswechsel
        if bg.get('funktionswechsel'):
            rels.append({'op': 'add_rel', 'from': bid, 'type': 'HAT_MATCHINGQUALITAET', 'to': 'mq_spec_zweckaenderung',
                         'properties': {'id': f'r_{bid}__HAT_MATCHINGQUALITAET__mq_spec_zweckaenderung', 'source': src, 'evidence': 'BELEGT'},
                         'reason': 'Phase 6d + O9: Funktionswechsel (Zweckänderung).', 'severity': 'LOW'})
    return rels


def main() -> int:
    rels = emit_rels()
    out = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_6b_bg_rels.patch.jsonl')
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as f:
        for r in rels:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Wrote {len(rels)} rel ops to {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
