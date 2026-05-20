"""Phase 12: 19 deferred Bauteilgruppen (per NEXT_STEPS §B3).

For each: add_node + mandatory 7 rels (HAT_BAUTEILEBENE, HAT_STATUS,
HAT_RESSOURCENQUELLE, HAT_BAUTEILTYP, HAT_MATERIALGRUPPE,
HAT_WIEDERVERWENDUNGSART, BELEGT_IN) + Project + Bauwerk links + optional vocab.

Splits into two files:
  - phase_batch2_v2_12a_deferred_bg_addnodes.patch.jsonl (add_node)
  - phase_batch2_v2_12b_deferred_bg_rels.patch.jsonl (all rels)
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

SRC = 'batch2_v2_followup_2026-05-20'

# 19 deferred BGs with full spec
BGS = [
    # === Circl extended (8 BGs) ===
    {
        'id': 'bg_reuse_mineralisch_boden_circl_pcm_tiles', 'name': 'Circl PCM-Fliesen',
        'name_full': 'Circl — Tile floors from reused concrete with PCM',
        'reuse_status': 'reuse', 'mat_primary': 'mat_recyclingbeton', 'bt_primary': 'bt_boden',
        'mg': 'mg_mineralisch', 'wva': 'wva_recycling', 'status': 'status_rueckgebaut',
        'rq': 'rq_baustelle', 'be': 'be_bauteilgruppe',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'mat': ['mat_recyclingbeton'],
    },
    {
        'id': 'bg_reuse_mehrere_ausbau_circl_restored_furniture', 'name': 'Circl ABN-Möbel',
        'name_full': 'Circl — Restored ABN AMRO furniture (intra-konzern reuse)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_ausbau',
        'mg': 'mg_mehrere', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_rueckgebaut',
        'rq': 'rq_baustelle', 'be': 'be_einzelbauteil',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'mm': ['mm_intra_konzern'], 'av': ['av_reinigung','av_holz_zuschnitt_reparatur'],
        'zk': ['zk_gebrauchsspuren_funktional'],
    },
    {
        'id': 'bg_planned_mehrere_technik_circl_leased_lifts', 'name': 'Circl Mietaufzüge',
        'name_full': 'Circl — Leased lifts (product-service system, supplier ownership, 10-year return)',
        'reuse_status': 'planned', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_technik',
        'mg': 'mg_mehrere', 'wva': 'wva_design_for_disassembly', 'status': 'status_rueckgebaut',
        'rq': 'rq_lager', 'be': 'be_system',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'mm': ['mm_leasing'], 'bweg': ['bweg_leihmodell'],
        'la': ['la_rueckbaubarkeit'],
    },
    {
        'id': 'bg_planned_mehrere_technik_circl_leased_lighting', 'name': 'Circl Mietbeleuchtung',
        'name_full': 'Circl — Leased Fagerhult DC lighting (product-service system)',
        'reuse_status': 'planned', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_technik',
        'mg': 'mg_mehrere', 'wva': 'wva_design_for_disassembly', 'status': 'status_rueckgebaut',
        'rq': 'rq_lager', 'be': 'be_system',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'mm': ['mm_leasing'], 'bweg': ['bweg_leihmodell'],
    },
    {
        'id': 'bg_planned_kunststoff_boden_circl_c2c_tarkett', 'name': 'Circl Tarkett C2C',
        'name_full': 'Circl — C2C-certified Tarkett iQ One flooring',
        'reuse_status': 'planned', 'mat_primary': 'mat_kunststoff', 'bt_primary': 'bt_boden',
        'mg': 'mg_kunststoff', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_rueckgebaut',
        'rq': 'rq_lager', 'be': 'be_oberflaechenschicht',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'mm': ['mm_take_back_service'], 'la': ['la_rueckbaubarkeit','la_dauerhaftigkeit'],
    },
    {
        'id': 'bg_planned_mehrere_fassade_circl_remountable_facade', 'name': 'Circl Remont. Fass.',
        'name_full': 'Circl — Remountable façade with C2C-certified plant modules (De Groot & Visser + Donkergroen)',
        'reuse_status': 'planned', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_fassade',
        'mg': 'mg_mehrere', 'wva': 'wva_design_for_disassembly', 'status': 'status_rueckgebaut',
        'rq': 'rq_baustelle', 'be': 'be_system',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'la': ['la_rueckbaubarkeit'],
    },
    {
        'id': 'bg_dismantled_mehrere_boden_circl_floor_structure', 'name': 'Circl Bodenaufbau',
        'name_full': 'Circl — Floor structure (less suitable for reuse than anticipated per Icon dismantling progress)',
        'reuse_status': 'dismantled', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_boden',
        'mg': 'mg_mehrere', 'wva': 'wva_recycling', 'status': 'status_rueckgebaut',
        'rq': 'rq_baustelle', 'be': 'be_bauteilgruppe',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'zk': ['zk_eingeschraenkt_nachbearbeitung'],
        'rv': ['rv_demontage'], 'pr': ['pr_dokumentenpruefung_bestand'],
    },
    {
        'id': 'bg_reuse_mehrere_ausbau_circl_greenery_harvest', 'name': 'Circl Bepflanzung',
        'name_full': 'Circl — Roof terrace + garden planting harvested by local residents (Stichting Struikroven)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_dach',
        'mg': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_rueckgebaut',
        'rq': 'rq_baustelle', 'be': 'be_einzelbauteil',
        'quelle': 'qu_circl_pavilion_dossier', 'projekt': 'p_circl_abn_amro',
        'eingebaut_in': 'bw_circl_pavilion_amsterdam',
        'mm': ['mm_spende'], 'bweg': ['bweg_informelles_netzwerk'],
    },
    # === MedUni extended (3 BGs) ===
    {
        'id': 'bg_reuse_metall_ausbau_medunicampus_bike_workshop', 'name': 'MedUni Fahrradwerkst.',
        'name_full': 'MedUni Mariannengasse — Bike workshop equipment (donor batch)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_stahl', 'bt_primary': 'bt_ausbau',
        'mg': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_realisiert',
        'rq': 'rq_donorgebaeude', 'be': 'be_einzelbauteil',
        'quelle': 'qu_meduni_mariannengasse_dossier', 'projekt': 'p_meduni_campus_mariannengasse',
        'aus_bauwerk': 'bw_meduni_campus_mariannengasse',
        'rv': ['rv_ausbau_von_bauteilen'], 'mm': ['mm_kauf_gebraucht'],
        'mat': ['mat_stahl'],
    },
    {
        'id': 'bg_reuse_metall_ausbau_medunicampus_heavy_shelves', 'name': 'MedUni Schwerlastreg.',
        'name_full': 'MedUni Mariannengasse — Heavy-duty shelves (donor batch)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_stahl', 'bt_primary': 'bt_ausbau',
        'mg': 'mg_metall', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_realisiert',
        'rq': 'rq_donorgebaeude', 'be': 'be_einzelbauteil',
        'quelle': 'qu_meduni_mariannengasse_dossier', 'projekt': 'p_meduni_campus_mariannengasse',
        'aus_bauwerk': 'bw_meduni_campus_mariannengasse',
        'rv': ['rv_ausbau_von_bauteilen'], 'mm': ['mm_kauf_gebraucht'],
        'mat': ['mat_stahl'],
    },
    {
        'id': 'bg_dismantled_glas_technik_medunicampus_fluorescent', 'name': 'MedUni Leuchtstoffr.',
        'name_full': 'MedUni Mariannengasse — Fluorescent tubes (hazardous removal, not reuse)',
        'reuse_status': 'dismantled', 'mat_primary': 'mat_glas', 'bt_primary': 'bt_technik',
        'mg': 'mg_glas_keramik', 'wva': 'wva_recycling', 'status': 'status_realisiert',
        'rq': 'rq_baustelle', 'be': 'be_einzelbauteil',
        'quelle': 'qu_meduni_mariannengasse_dossier', 'projekt': 'p_meduni_campus_mariannengasse',
        'aus_bauwerk': 'bw_meduni_campus_mariannengasse',
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'schadstoff': ['s_schwermetalle'],  # mercury
        'zk': ['zk_nicht_wiederverwendbar'],
    },
    # === BE-WARE TULIUM (3 BGs) ===
    {
        'id': 'bg_reuse_holz_mehrere_beware_local_timber', 'name': 'BE-WARE Altholz',
        'name_full': 'Reallabor B(e) Ware Berlin — Local secondary timber for structural systems (central storage Spandau)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_holz', 'bt_primary': 'bt_traeger',
        'mg': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_geplant',
        'rq': 'rq_lager', 'be': 'be_materialcharge',
        'quelle': 'qu_beware_dossier', 'projekt': 'prog_reallabor_be_ware',
        'av': ['av_holz_festigkeitssortierung','av_holz_trocknung_feuchtekonditionierung'],
        'log': ['log_lagerung','log_zwischenlagerung','log_bauteiltracking'],
        'pr': ['pr_festigkeitssortierung_holz'],
        'mat': ['mat_holz'],
    },
    {
        'id': 'bg_reuse_holz_mehrere_beware_tulium_trusses', 'name': 'TULIUM Altholz-Träger',
        'name_full': 'TULIUM museum pavilion (BE-WARE) — Wide-span lattice beams from old timber (reversible steel-poor system)',
        'reuse_status': 'planned', 'mat_primary': 'mat_holz', 'bt_primary': 'bt_traeger',
        'mg': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_geplant',
        'rq': 'rq_donorgebaeude', 'be': 'be_bauteilgruppe',
        'quelle': 'qu_beware_dossier', 'projekt': 'prog_reallabor_be_ware',
        'vt': ['vt_reversible_fuegung','vt_steckverbindung'],
        'la': ['la_tragfaehigkeit','la_rueckbaubarkeit'],
        'mat': ['mat_holz'],
    },
    {
        'id': 'bg_planned_mehrere_fundament_beware_flying_foundation', 'name': 'BE-WARE Flugfundam.',
        'name_full': 'TULIUM (BE-WARE) — Flying foundation with recycled RC elements (low-concrete, no slab sealing)',
        'reuse_status': 'planned', 'mat_primary': 'mat_recyclingbeton', 'bt_primary': 'bt_fundament',
        'mg': 'mg_mineralisch', 'wva': 'wva_recycling', 'status': 'status_geplant',
        'rq': 'rq_donorgebaeude', 'be': 'be_bauteilgruppe',
        'quelle': 'qu_beware_dossier', 'projekt': 'prog_reallabor_be_ware',
        'la': ['la_tragfaehigkeit'],
        'mat': ['mat_recyclingbeton'],
    },
    # === RE_USE Höfe (2 BGs, modest) ===
    {
        'id': 'bg_reuse_holz_fenster_reusehoefe_ukraine_windows', 'name': 'RE-WIN Ukraine-Fenster',
        'name_full': 'RE-USE Höfe — Windows for Ukraine: salvaged window frames from CH demolitions → humanitarian reuse Ukraine',
        'reuse_status': 'reuse', 'mat_primary': 'mat_holz', 'bt_primary': 'bt_fenster',
        'mg': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_realisiert',
        'rq': 'rq_donorgebaeude', 'be': 'be_bauteilgruppe',
        'quelle': 'qu_reusehoefe_dossier', 'projekt': 'prog_re_use_hoefe',
        'rv': ['rv_ausbau_von_bauteilen','rv_zerstoerungsarme_bergung'],
        'av': ['av_fenster_refurbishment'],
        'log': ['log_lagerung','log_transport','log_transportdistanz'],
        'mm': ['mm_spende'], 'bweg': ['bweg_spende','bweg_informelles_netzwerk'],
        'mat': ['mat_holz'],
    },
    {
        'id': 'bg_reuse_mehrere_mehrere_reusehoefe_yard_logistics', 'name': 'RE-USE Höfe Logistik',
        'name_full': 'RE-USE Höfe — yard logistics / supply-chain model (collection, storage, distribution)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_mehrere',
        'mg': 'mg_mehrere', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_realisiert',
        'rq': 'rq_lager', 'be': 'be_system',
        'quelle': 'qu_reusehoefe_dossier', 'projekt': 'prog_re_use_hoefe',
        'log': ['log_lagerung','log_zwischenlagerung','log_bauteiltracking','log_materialmatching','log_lagerflaeche'],
        'bweg': ['bweg_digitale_plattform','bweg_informelles_netzwerk'],
    },
    # === Stuttgart 210 / Ingersheim secondary (1) ===
    {
        'id': 'bg_reuse_holz_ausbau_ingersheim_clt_secondary', 'name': 'Ingersheim CLT-Ausbau',
        'name_full': 'Jugendtreff Ingersheim — CLT offcuts used for secondary fit-out elements',
        'reuse_status': 'reuse', 'mat_primary': 'mat_holz', 'bt_primary': 'bt_ausbau',
        'mg': 'mg_holz_biobasiert', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_realisiert',
        'rq': 'rq_donorgebaeude', 'be': 'be_einzelbauteil',
        'quelle': 'qu_stuttgart210_dossier', 'projekt': 'p_jugendtreff_ingersheim',
        'eingebaut_in': 'bw_jugendtreff_ingersheim', 'aus_bauwerk': 'bw_stuttgart21_hauptbahnhof',
        'av': ['av_holz_zuschnitt_reparatur','av_hobeln_schleifen_holz'],
        'mat': ['mat_holz'],
    },
    # === Granby bespoke (1) ===
    {
        'id': 'bg_reuse_mehrere_boden_granby_bespoke_waste', 'name': 'Granby Abfallmix',
        'name_full': 'Granby Workshop — bespoke waste-stream terrazzo mixes (client-supplied materials or workshop materials)',
        'reuse_status': 'reuse', 'mat_primary': 'mat_mehrere', 'bt_primary': 'bt_boden',
        'mg': 'mg_mehrere', 'wva': 'wva_recycling', 'status': 'status_realisiert',
        'rq': 'rq_lager', 'be': 'be_materialcharge',
        'quelle': 'qu_granby_workshop_dossier', 'projekt': 'p_granby_workshop',
        'av': ['av_materialsortierung_chargenbildung','av_naturstein_reinigung_schleifen_zuschnitt'],
        'mm': ['mm_kauf_gebraucht'], 'bweg': ['bweg_direktvermittlung'],
        'la': ['la_dauerhaftigkeit'],
    },
    # === Granby first house products (1) ===
    {
        'id': 'bg_reuse_glas_keramik_ausbau_granby_first_house_products', 'name': 'Granby Ersthausprod.',
        'name_full': 'Granby Workshop — first products (bathroom tiles, door handles, fireplaces) made in Granby for renovated houses',
        'reuse_status': 'reuse', 'mat_primary': 'mat_keramik', 'bt_primary': 'bt_ausbau',
        'mg': 'mg_glas_keramik', 'wva': 'wva_direkte_wiederverwendung', 'status': 'status_realisiert',
        'rq': 'rq_baustelle', 'be': 'be_einzelbauteil',
        'quelle': 'qu_granby_workshop_dossier', 'projekt': 'p_granby_workshop',
        'mm': ['mm_kauf_gebraucht'], 'la': ['la_dauerhaftigkeit'],
        'mat': ['mat_keramik'],
    },
]


SLOT_TO_REL = {
    'bweg': 'HAT_BESCHAFFUNGSWEG',
    'vt': 'HAT_VERBINDUNGSTECHNIK',
    'rv': 'HAT_RUECKBAUVERFAHREN',
    'av': 'HAT_AUFBEREITUNG',
    'log': 'HAT_LOGISTIK',
    'pr': 'HAT_PRUEFUNG',
    'def': 'HAT_DEFEKT',
    'zk': 'HAT_ZUSTANDSKLASSE',
    'bps': 'HAT_BAUPRODUKTSTATUS',
    'la': 'HAT_LEISTUNGSANFORDERUNG',
    'schadstoff': 'HAT_SCHADSTOFF',
    'mm': 'HAT_MARKTMODELL',
    'mat': 'NUTZT_MATERIAL',
}


def emit_adds() -> list[dict]:
    """Emit add_node ops for the 19 deferred BGs."""
    adds: list[dict] = []
    for bg in BGS:
        props = {
            'id': bg['id'],
            'name': bg['name'],
            'name_full': bg['name_full'],
            'reuse_status': bg['reuse_status'],
            'primary_material_id': bg['mat_primary'],
            'primary_bauteiltyp_id': bg['bt_primary'],
            'source_scope': 'case_markdown',
        }
        adds.append({
            'op': 'add_node',
            'id': bg['id'],
            'labels': ['Bauteilgruppe'],
            'properties': props,
            'reason': 'Phase 12: deferred BG from NEXT_STEPS §B3.',
            'severity': 'LOW',
        })
    return adds


def emit_rels() -> list[dict]:
    """Emit all rels for the 19 deferred BGs (mandatory 7 + optional vocab + Projekt/Bauwerk + FW)."""
    rels: list[dict] = []
    for bg in BGS:
        bid = bg['id']
        # Mandatory 7 rels
        for slot, rel_type in [
            ('be', 'HAT_BAUTEILEBENE'),
            ('status', 'HAT_STATUS'),
            ('rq', 'HAT_RESSOURCENQUELLE'),
            ('bt_primary', 'HAT_BAUTEILTYP'),
            ('mg', 'HAT_MATERIALGRUPPE'),
            ('wva', 'HAT_WIEDERVERWENDUNGSART'),
            ('quelle', 'BELEGT_IN'),
        ]:
            target = bg[slot]
            rid = f'r_{bid}__{rel_type}__{target}'
            rels.append({
                'op': 'add_rel', 'from': bid, 'type': rel_type, 'to': target,
                'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                'reason': 'Phase 12: deferred BG mandatory rel.', 'severity': 'LOW',
            })
        # Projekt link
        if 'projekt' in bg:
            p = bg['projekt']
            rid = f'r_{p}__HAT_BAUTEILGRUPPE__{bid}'
            rels.append({
                'op': 'add_rel', 'from': p, 'type': 'HAT_BAUTEILGRUPPE', 'to': bid,
                'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                'reason': 'Phase 12: Projekt to BG.', 'severity': 'LOW',
            })
        # Bauwerk links
        if 'eingebaut_in' in bg:
            t = bg['eingebaut_in']
            rid = f'r_{bid}__EINGEBAUT_IN__{t}'
            rels.append({
                'op': 'add_rel', 'from': bid, 'type': 'EINGEBAUT_IN', 'to': t,
                'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                'reason': 'Phase 12.', 'severity': 'LOW',
            })
        if 'aus_bauwerk' in bg:
            t = bg['aus_bauwerk']
            rid = f'r_{bid}__AUS_BAUWERK__{t}'
            rels.append({
                'op': 'add_rel', 'from': bid, 'type': 'AUS_BAUWERK', 'to': t,
                'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                'reason': 'Phase 12.', 'severity': 'LOW',
            })
        # Optional vocab
        for slot_key, rel_type in SLOT_TO_REL.items():
            if slot_key in bg:
                for target in bg[slot_key]:
                    rid = f'r_{bid}__{rel_type}__{target}'
                    rels.append({
                        'op': 'add_rel', 'from': bid, 'type': rel_type, 'to': target,
                        'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                        'reason': 'Phase 12: deferred BG optional vocab.', 'severity': 'LOW',
                    })
    return rels


def main() -> int:
    adds = emit_adds()
    rels = emit_rels()
    out_dir = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2')
    a = out_dir / 'phase_batch2_v2_12a_deferred_bg_addnodes.patch.jsonl'
    r = out_dir / 'phase_batch2_v2_12b_deferred_bg_rels.patch.jsonl'
    with a.open('w', encoding='utf-8') as f:
        for x in adds:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    with r.open('w', encoding='utf-8') as f:
        for x in rels:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    print(f'Wrote {len(adds)} add_nodes to {a}')
    print(f'Wrote {len(rels)} rel ops to {r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
