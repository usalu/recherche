"""Generate Phase 8 project-level vocabulary edges JSONL.

For each Projekt, emit HAT_INTERVENTION / HAT_NUTZUNG / HAT_METHODE / HAT_HUERDE /
HAT_WIRTSCHAFT / HAT_DOMINANT_MARKTMODELL / HAT_DOMINANT_AKZEPTANZ /
NUTZT_SOFTWARE / NUTZT_TOOL / HAT_ZERTIFIZIERUNG / REFERENZIERT_NORM rels
per dossier evidence.

Source IDs verified live (S2-S25). Only emit edges where dossier evidence is BELEGT.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

SRC = 'batch2_v2_import_2026-05-20'

# Project-level rels per project (dossier-evidenced)
PROJEKT_RELS = {
    'p_schaerenmoosstrasse_zuerich': {
        'HAT_INTERVENTION': ['bai_umnutzung', 'bai_umbau'],
        'HAT_NUTZUNG': ['nut_wohnen', 'nut_gewerbe'],
        'HAT_METHODE': ['meth_form_follows_availability', 'meth_reuse_assessment'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_oeffentlicher_bauherr_pilot'],
        'REFERENZIERT_NORM': ['norm_sia_500', 'norm_sia_261'],
    },
    'p_umar_unit': {
        'HAT_INTERVENTION': ['bai_neubau'],
        'HAT_NUTZUNG': ['nut_wohnen'],
        'HAT_METHODE': ['meth_design_for_disassembly', 'meth_reversibilitaet', 'meth_urban_mining', 'meth_bauteilkatalogisierung'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_take_back_service'],
        'NUTZT_TOOL': ['tool_bim_bauteilkatalog'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_oeffentlicher_bauherr_pilot'],
        'REFERENZIERT_NORM': ['norm_sia_269'],
    },
    'p_elementa_walkeweg': {
        'HAT_INTERVENTION': ['bai_neubau'],
        'HAT_NUTZUNG': ['nut_wohnen'],
        'HAT_METHODE': ['meth_pre_deconstruction_audit', 'meth_bauteilkatalogisierung', 'meth_materialinventur', 'meth_form_follows_availability'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_plattform_vermittelt'],
        'NUTZT_SOFTWARE': ['software_ecotool'],
        'NUTZT_TOOL': ['tool_bauteilkatalog'],
        'HAT_ZERTIFIZIERUNG': ['zbs_ecotool'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_oeffentlicher_bauherr_pilot'],
        'REFERENZIERT_NORM': ['norm_sia_269'],
    },
    'p_careno_becircular': {
        'HAT_METHODE': ['meth_wiederverwendungskriterien', 'meth_building_material_scouting'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_plattform_vermittelt'],
        'NUTZT_TOOL': ['tool_retile'],
    },
    'p_circl_abn_amro': {
        'HAT_INTERVENTION': ['bai_neubau', 'bai_rueckbau'],
        'HAT_NUTZUNG': ['nut_buero', 'nut_mischnutzung'],
        'HAT_METHODE': ['meth_design_for_disassembly', 'meth_zirkulaere_ausschreibung', 'meth_urban_mining', 'meth_abrissmonitoring'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_intra_konzern'],
        'NUTZT_SOFTWARE': ['software_llmnt'],
    },
    'p_lysp8_basel': {
        'HAT_INTERVENTION': ['bai_neubau'],
        'HAT_NUTZUNG': ['nut_wohnen', 'nut_gewerbe'],
        'HAT_METHODE': ['meth_design_for_disassembly', 'meth_reuse_assessment', 'meth_building_material_scouting'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_oeffentlicher_bauherr_pilot'],
        'REFERENZIERT_NORM': ['norm_sia_269'],
    },
    'p_meduni_campus_mariannengasse': {
        'HAT_INTERVENTION': ['bai_rueckbau', 'bai_neubau'],
        'HAT_NUTZUNG': ['nut_schule_bildung'],
        'HAT_METHODE': ['meth_pre_deconstruction_audit', 'meth_bauteilkatalogisierung', 'meth_materialinventur'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_spende'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_oeffentlicher_bauherr_pilot'],
    },
    'p_granby_workshop': {
        'HAT_METHODE': ['meth_form_follows_availability'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_kauf_gebraucht'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_aesthetik_patinakultur'],
    },
    'p_jugendtreff_ingersheim': {
        'HAT_INTERVENTION': ['bai_neubau'],
        'HAT_NUTZUNG': ['nut_kultur'],
        'HAT_METHODE': ['meth_form_follows_availability', 'meth_urban_mining'],
        'HAT_DOMINANT_MARKTMODELL': ['mm_forschungsprojekt_zuteilung'],
    },
    'p_eggshell_pavilion': {
        'HAT_INTERVENTION': ['bai_neubau'],
        'HAT_METHODE': ['meth_design_for_disassembly'],
    },
    'p_up_sticks_dundee': {
        'HAT_INTERVENTION': ['bai_neubau'],
        'HAT_METHODE': ['meth_design_for_disassembly'],
    },
}


def emit_rels() -> list[dict]:
    rels: list[dict] = []
    for projekt_id, rel_map in PROJEKT_RELS.items():
        for rel_type, targets in rel_map.items():
            for target in targets:
                rid = f'r_{projekt_id}__{rel_type}__{target}'
                rels.append({
                    'op': 'add_rel',
                    'from': projekt_id,
                    'type': rel_type,
                    'to': target,
                    'properties': {'id': rid, 'source': SRC, 'evidence': 'BELEGT'},
                    'reason': 'Phase 8 + O7 (project-level vocab; Plan 1 Phase 8 restored).',
                    'severity': 'LOW',
                })
    return rels


def main() -> int:
    rels = emit_rels()
    out = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_8_project_vocab.patch.jsonl')
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open('w', encoding='utf-8') as f:
        for r in rels:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Wrote {len(rels)} project-level vocab rel ops to {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
