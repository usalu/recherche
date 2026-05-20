"""Phase 10: project-level HAT_HUERDE, HAT_WIRTSCHAFT, HAT_DOMINANT_AKZEPTANZ.

Maps each promoted Projekt's dossier "Building-level graph categories" Huerde +
Wirtschaft + Akzeptanz text to live vocab IDs. Only emits where dossier evidence
is BELEGT (i.e., explicitly named in source).

Live vocab IDs verified 2026-05-20 via pre_flight_validation.cypher (S sections).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

SRC = 'batch2_v2_followup_2026-05-20'

# Per-project mapping: Projekt id → {rel_type: [vocab_id, ...]}
PROJEKT_RELS = {
    # Schärenmoosstrasse Zürich (batch 1.md §1; jury report)
    'p_schaerenmoosstrasse_zuerich': {
        'HAT_HUERDE': ['h_technische_freigabe', 'h_entwurfsbindung', 'h_zustand_unklar', 'h_dauerhaftigkeit_restlebensdauer', 'h_toleranzen'],
        'HAT_WIRTSCHAFT': ['wi_capex_hoeher_subvention', 'wi_capex_hoeher_opex_payback'],
    },
    # UMAR Unit (batch 1.md §2)
    'p_umar_unit': {
        'HAT_HUERDE': ['h_fehlende_standardisierung', 'h_fehlende_datenstandards', 'h_datenluecke', 'h_dauerhaftigkeit_restlebensdauer'],
        'HAT_WIRTSCHAFT': ['wi_capex_hoeher_opex_payback', 'wi_hidden_costs_lagerung_pruefung', 'wi_geschaeftsmodell', 'wi_lebenszykluskosten'],
    },
    # ELEMENTA Walkeweg (batch 1.md §3)
    'p_elementa_walkeweg': {
        'HAT_HUERDE': ['h_entwurfsbindung', 'h_verfuegbarkeitsproblem', 'h_heterogenitaet_chargen', 'h_terminunsicherheit', 'h_toleranzen', 'h_zustand_unklar'],
        'HAT_WIRTSCHAFT': ['wi_capex_niedriger_direkter_ersparnis', 'wi_capex_hoeher_subvention', 'wi_hidden_costs_lagerung_pruefung', 'wi_lebenszykluskosten'],
    },
    # Careno Be.Circular
    'p_careno_becircular': {
        'HAT_HUERDE': ['h_aufbereitungsaufwand', 'h_materialqualitaet_unklar', 'h_fehlende_standardisierung', 'h_bruch_beschaedigungsrisiko', 'h_gewaehrleistung'],
        'HAT_WIRTSCHAFT': ['wi_capex_hoeher_subvention', 'wi_preisbildung', 'wi_geschaeftsmodell'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_aesthetik_patinakultur'],  # historic 1900-1960 tiles aesthetic
    },
    # Circl Pavilion
    'p_circl_abn_amro': {
        'HAT_HUERDE': ['h_zustand_unklar', 'h_materialqualitaet_unklar', 'h_dauerhaftigkeit_restlebensdauer', 'h_anschlussproblem'],  # Icon dismantling sources; some BGs less suitable
        'HAT_WIRTSCHAFT': ['wi_geschaeftsmodell', 'wi_restwert', 'wi_capex_hoeher_marketing_payback', 'wi_lebenszykluskosten'],
    },
    # LysP8 Basel
    'p_lysp8_basel': {
        'HAT_HUERDE': ['h_verfuegbarkeitsproblem', 'h_fehlende_lagerflaeche', 'h_aufbereitungsaufwand', 'h_toleranzen', 'h_terminunsicherheit'],
        'HAT_WIRTSCHAFT': ['wi_capex_neutral', 'wi_kostenvergleich', 'wi_lebenszykluskosten'],  # "Material cost new = ceiling for reuse"; 132t CO2 LCA
    },
    # MedUni Campus Mariannengasse
    'p_meduni_campus_mariannengasse': {
        'HAT_HUERDE': ['h_terminunsicherheit', 'h_ausschreibungsproblem', 'h_akzeptanzproblem'],  # Thomas Romm quote: lead time + client engagement
        'HAT_WIRTSCHAFT': ['wi_geschaeftsmodell', 'wi_preisbildung'],  # proceeds from sales fund BauKarussell
    },
    # Stuttgart 210 (the parent Programm; will reach via merged dual-label :Projekt)
    'prog_stuttgart_210': {
        'HAT_HUERDE': ['h_bauproduktstatus', 'h_technische_freigabe', 'h_gewaehrleistung'],
        'HAT_WIRTSCHAFT': ['wi_capex_niedriger_direkter_ersparnis', 'wi_restwert'],
    },
    # Jugendtreff Ingersheim
    'p_jugendtreff_ingersheim': {
        'HAT_HUERDE': ['h_bauproduktstatus', 'h_technische_freigabe', 'h_unkonventionelles_material'],
        'HAT_DOMINANT_AKZEPTANZ': ['ak_oeffentlicher_bauherr_pilot'],
    },
    # Granby Workshop
    'p_granby_workshop': {
        'HAT_HUERDE': ['h_heterogenitaet_chargen', 'h_mengenunsicherheit'],
        'HAT_WIRTSCHAFT': ['wi_geschaeftsmodell', 'wi_preisbildung'],  # CIC business model + bespoke pricing
    },
    # Eggshell Pavilion / Up Sticks Dundee — research demonstrators
    'p_eggshell_pavilion': {
        'HAT_HUERDE': ['h_unkonventionelles_material', 'h_bauproduktstatus'],
    },
    'p_up_sticks_dundee': {
        'HAT_HUERDE': ['h_unkonventionelles_material', 'h_bauproduktstatus'],
    },
}


def emit_rels() -> list[dict]:
    rels: list[dict] = []
    for projekt_id, rel_map in PROJEKT_RELS.items():
        for rel_type, targets in rel_map.items():
            for target in targets:
                rels.append({
                    'op': 'add_rel',
                    'from': projekt_id,
                    'type': rel_type,
                    'to': target,
                    'properties': {
                        'id': f'r_{projekt_id}__{rel_type}__{target}',
                        'source': SRC,
                        'evidence': 'BELEGT',
                    },
                    'reason': 'Phase 10: project-level Huerde + Wirtschaft + Akzeptanz from dossier Building-level graph categories.',
                    'severity': 'LOW',
                })
    return rels


def main() -> int:
    rels = emit_rels()
    out = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2/phase_batch2_v2_10_huerde_wirtschaft.patch.jsonl')
    with out.open('w', encoding='utf-8') as f:
        for r in rels:
            f.write(json.dumps(r, ensure_ascii=False) + '\n')
    print(f'Wrote {len(rels)} ops to {out}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
