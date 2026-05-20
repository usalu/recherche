"""Phase 13: ~55 additional Akteure (orgs + persons) from dossiers not yet patched.

Each entry: id, name, label-class, role-shorthand, dossier evidence, project link.
Generator emits add_node + HAT_AKTEURROLLE + HAT_AKTEURTYP + BETEILIGT_AN
(and Land where evidenced).
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

SRC = 'batch2_v2_followup_2026-05-20'

# Role shorthand → (ar_*, at_*)
ROLES = {
    'arch':       ('ar_entwurf_planung',                'at_unternehmen'),
    'struct':     ('ar_tragwerksplanung',               'at_unternehmen'),
    'engineer':   ('ar_fachplanung_nachweis',           'at_unternehmen'),
    'tga':        ('ar_tga_gebaeudetechnik',            'at_unternehmen'),
    'landscape':  ('ar_landschaftsplanung',             'at_unternehmen'),
    'client':     ('ar_bauherr_auftraggeber',           'at_unternehmen'),
    'client_pub': ('ar_bauherr_auftraggeber',           'at_oeffentliche_institution'),
    'funder':     ('ar_oeffentliche_hand_foerderung',   'at_oeffentliche_institution'),
    'research':   ('ar_forschung_dokumentation',        'at_forschung_lehre'),
    'reuse_consult': ('ar_reuse_zirkularitaetsberatung','at_unternehmen'),
    'broker':     ('ar_materialbroker',                 'at_materialhub_bauteilboerse'),
    'decon':      ('ar_rueckbau_bauteilernte_logistik', 'at_unternehmen'),
    'contract':   ('ar_bauausfuehrung_fertigung',       'at_unternehmen'),
    'supplier':   ('ar_materiallieferung_markt',        'at_unternehmen'),
    'software':   ('ar_software_digitalisierung',       'at_software_tool_anbieter'),
    'ngo':        ('ar_forschung_dokumentation',        'at_ngo_verband_netzwerk'),
    'fassade':    ('ar_fassade',                        'at_unternehmen'),
    'p_arch':     ('ar_entwurf_planung',                'at_person'),
    'p_struct':   ('ar_tragwerksplanung',               'at_person'),
    'p_research': ('ar_forschung_dokumentation',        'at_person'),
    'p_landscape':('ar_landschaftsplanung',             'at_person'),
    'p_manage':   ('ar_projektmanagement_koordination', 'at_person'),
    'p_curate':   ('ar_kunst_gestaltung',               'at_person'),
}

# (id, name, name_full, role, land, [(rel, target, rolle_text)...])
ACTORS = [
    # UMAR suppliers
    ('kaufmann_zimmerei', 'kaufmann zimmerei', 'kaufmann zimmerei und tischlerei GmbH', 'contract', 'CH', [('BETEILIGT_AN','p_umar_unit','timber contractor')]),
    ('amstein_walthert', 'Amstein+Walthert AG', 'Amstein+Walthert AG — building services engineer', 'tga', 'CH', [('BETEILIGT_AN','p_umar_unit','building services engineer')]),
    ('balzer_ingenieure', 'Balzer Ingenieure AG', 'Balzer Ingenieure AG — structural engineer', 'struct', 'CH', [('BETEILIGT_AN','p_umar_unit','structural engineer')]),
    ('weber_energie_bauphysik', 'Weber Energie+Bauphysik', 'Weber Energie und Bauphysik — building physics', 'engineer', 'CH', [('BETEILIGT_AN','p_umar_unit','building physics')]),
    ('lindner_se', 'Lindner SE', 'Lindner SE — Plafotherm ceiling panel supplier (product-as-service)', 'supplier', 'DE', [('BETEILIGT_AN','p_umar_unit','ceiling panel supplier')]),
    ('nimbus', 'Nimbus', 'Nimbus — lighting designer (UMAR)', 'supplier', 'DE', [('BETEILIGT_AN','p_umar_unit','lighting designer')]),
    ('magna_glaskeramik', 'Magna Glaskeramik', 'Magna Glaskeramik — sintered recycled-glass panel manufacturer', 'supplier', 'DE', [('BETEILIGT_AN','p_umar_unit','recycled-glass panel manufacturer')]),
    ('ecovative', 'Ecovative', 'Ecovative — mycelium insulation manufacturer', 'supplier', 'US', [('BETEILIGT_AN','p_umar_unit','mycelium insulation manufacturer')]),
    ('desso_tarkett', 'Desso / Tarkett', 'Desso / Tarkett — carpet supplier (take-back service)', 'supplier', 'NL', [('BETEILIGT_AN','p_umar_unit','carpet supplier (take-back)')]),
    # ELEMENTA team
    ('monotti_ingegneri', 'Monotti Ingegneri', 'Monotti Ingegneri Consulenti SA — structural engineer (ELEMENTA)', 'struct', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','structural engineer')]),
    ('mario_monotti', 'Mario Monotti', 'Mario Monotti — structural engineer at Monotti Ingegneri', 'p_struct', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','structural engineer (person)')]),
    ('usus_la', 'USUS Landschaftsarch.', 'USUS Landschaftsarchitektur — landscape architect (ELEMENTA)', 'landscape', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','landscape architect')]),
    ('roger_keller', 'Roger Keller', 'Roger Keller — landscape architect at USUS', 'p_landscape', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','landscape architect (person)')]),
    ('ana_olalquiaga', 'Ana Olalquiaga', 'Ana Olalquiaga — architect at PARABASE', 'p_arch', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','architect (person)')]),
    ('caretta_weidmann', 'Caretta+Weidmann', 'Caretta+Weidmann — façade engineering', 'fassade', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','façade engineering')]),
    ('gti_engineering', 'GTI Engineering', 'GTI Engineering — MEP / building services (ELEMENTA)', 'tga', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','MEP / building services')]),
    ('afc_basel', 'AFC Basel', 'AFC — cost management / quantity surveying', 'engineer', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','cost management')]),
    ('senn_technology', 'Senn Technology AG', 'Senn Technology AG — specialist engineering', 'engineer', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','specialist engineering')]),
    ('anima_engineering', 'Anima Engineering AG', 'Anima Engineering AG — specialist engineering', 'engineer', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','specialist engineering')]),
    ('bauteilboerse_basel', 'Bauteilbörse Basel', 'Bauteilbörse Basel — component exchange platform', 'broker', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','component exchange platform')]),
    ('digvis_gmbh', 'Digvis GmbH', 'Digvis GmbH — digital visualisation (ELEMENTA)', 'software', 'CH', [('BETEILIGT_AN','p_elementa_walkeweg','digital visualisation')]),
    # SMS Zürich team
    ('perez_schmidlin_bauingenieure', 'Pérez Schmidlin', 'Pérez Schmidlin Bauingenieure GmbH — structural engineer', 'struct', 'CH', [('BETEILIGT_AN','p_schaerenmoosstrasse_zuerich','structural engineer')]),
    ('andreas_geser_landschaftsarchitekten', 'AG Landschaftsarch.', 'Andreas Geser Landschaftsarchitekten AG', 'landscape', 'CH', [('BETEILIGT_AN','p_schaerenmoosstrasse_zuerich','landscape architect')]),
    ('stefan_perez', 'Stefan Pérez', 'Stefan Pérez — Bauingenieur Mitarbeit at Pérez Schmidlin', 'p_struct', 'CH', [('BETEILIGT_AN','p_schaerenmoosstrasse_zuerich','structural engineer (person)')]),
    ('michael_schmidlin', 'Michael Schmidlin', 'Michael Schmidlin — Bauingenieur Mitarbeit at Pérez Schmidlin', 'p_struct', 'CH', [('BETEILIGT_AN','p_schaerenmoosstrasse_zuerich','structural engineer (person)')]),
    ('andreas_geser', 'Andreas Geser', 'Andreas Geser — landscape architecture lead at AG Landschaftsarch.', 'p_landscape', 'CH', [('BETEILIGT_AN','p_schaerenmoosstrasse_zuerich','landscape architect (person)')]),
    ('martin_zeller', 'Martin Zeller', 'Martin Zeller — credits at Loeliger Strub Architektur (LysP8 visuals)', 'p_curate', 'CH', [('BETEILIGT_AN','p_lysp8_basel','credits / visuals')]),
    # LysP8 Zirkular team + suppliers
    ('repoxit_ag', 'Repoxit AG', 'Repoxit AG — construction / floor execution (Oxacrete)', 'contract', 'CH', [('BETEILIGT_AN','p_lysp8_basel','floor construction (Oxacrete)')]),
    ('kibag', 'KIBAG', 'KIBAG — Oxacrete material production', 'supplier', 'CH', [('BETEILIGT_AN','p_lysp8_basel','Oxacrete material production')]),
    ('pascal_hentschel', 'Pascal Hentschel', 'Pascal Hentschel — project team at Zirkular GmbH', 'p_research', 'CH', [('BETEILIGT_AN','p_lysp8_basel','project team (Zirkular)')]),
    ('rebecca_brandmayer', 'Rebecca Brandmayer', 'Rebecca Brandmayer — component hunting at Zirkular', 'p_research', 'CH', [('BETEILIGT_AN','p_lysp8_basel','component hunting (Zirkular)')]),
    ('laia_meier', 'Laia Meier', 'Laia Meier — component hunting at Zirkular', 'p_research', 'CH', [('BETEILIGT_AN','p_lysp8_basel','component hunting (Zirkular)')]),
    # MedUni Persons
    ('markus_meissner', 'Markus Meissner', 'Markus Meissner — Ressourcenmanager / Leiter at BauKarussell', 'p_manage', 'AT', [('BETEILIGT_AN','p_meduni_campus_mariannengasse','resource manager (BauKarussell)')]),
    ('thomas_romm', 'Thomas Romm', 'Thomas Romm — architect / founder of BauKarussell', 'p_arch', 'AT', [('BETEILIGT_AN','p_meduni_campus_mariannengasse','architect / founder of BauKarussell')]),
    # Stuttgart 210 orgs
    ('ed_zueblin_ag', 'Ed. Züblin AG', 'Ed. Züblin AG — Praxispartner (Stuttgart 210; parent of ZÜBLIN Timber)', 'contract', 'DE', [('BETEILIGT_AN','prog_stuttgart_210','Praxispartner')]),
    ('faltlhauser_krapf', 'Faltlhauser Krapf', 'Faltlhauser Krapf — structural engineer (Jugendtreff Ingersheim)', 'struct', 'DE', [('BETEILIGT_AN','p_jugendtreff_ingersheim','Tragwerksplanung')]),
    ('mlr_bw', 'MLR BW', 'Ministerium für Ernährung, Ländlichen Raum und Verbraucherschutz Baden-Württemberg — funder', 'funder', 'DE', [('BETEILIGT_AN','prog_stuttgart_210','funder ministry')]),
    # Granby Workshop
    ('will_shannon', 'Will Shannon', 'Will Shannon — collaborator on Granby Rock terrazzo development', 'p_arch', 'GB', [('BETEILIGT_AN','p_granby_workshop','Granby Rock collaborator (2015)')]),
    ('granby_workshop_cic', 'Granby Workshop CIC', 'Granby Workshop CIC — operator / manufacturer', 'supplier', 'GB', [('BETEILIGT_AN','p_granby_workshop','operator / CIC')]),
    ('granby_4_streets_clt', 'Granby 4 Streets CLT', 'Granby 4 Streets CLT — community land trust collaborator', 'ngo', 'GB', [('BETEILIGT_AN','p_granby_workshop','community land trust')]),
    # Circl additional
    ('traject', 'TRAJECT', 'TRAJECT — Circl construction-team coordinator', 'engineer', 'NL', [('BETEILIGT_AN','p_circl_abn_amro','construction-team coordinator')]),
    ('vermaat', 'Vermaat', 'Vermaat — Circl circular catering operator', 'supplier', 'NL', [('BETEILIGT_AN','p_circl_abn_amro','circular catering operator')]),
    ('exasun', 'Exasun', 'Exasun — Circl solar panel supplier', 'supplier', 'NL', [('BETEILIGT_AN','p_circl_abn_amro','solar panel supplier')]),
    ('fagerhult', 'Fagerhult', 'Fagerhult — Circl DC lighting supplier (leased)', 'supplier', 'SE', [('BETEILIGT_AN','p_circl_abn_amro','DC lighting supplier')]),
    ('de_groot_en_visser', 'De Groot & Visser', 'De Groot & Visser — Circl façade / solar boiler', 'supplier', 'NL', [('BETEILIGT_AN','p_circl_abn_amro','façade + Fasolar solar boiler')]),
    ('victory_group', 'Victory Group', 'Victory Group — owner of ABN AMRO complex including Circl post-2024', 'client', 'NL', [('BETEILIGT_AN','p_circl_abn_amro','post-dismantling owner')]),
    ('ter_velde_den_besten', 'Ter Velde & Den Besten', 'Ter Velde & Den Besten — 3D laser scanning provider (Circl digital twin)', 'software', 'NL', [('BETEILIGT_AN','p_circl_abn_amro','3D laser scanning / digital twin')]),
    # RE_USE Höfe Persons
    ('michelle_schneider_zhaw', 'Michelle Schneider', 'Michelle Schneider — author / concept / graphics at ZHAW IKE', 'p_research', 'CH', [('BETEILIGT_AN','prog_re_use_hoefe','author / concept')]),
    ('felix_dillmann', 'Félix Dillmann', 'Félix Dillmann — author / concept / graphics at Verein RE-WIN', 'p_research', 'CH', [('BETEILIGT_AN','prog_re_use_hoefe','author / concept')]),
    # Reuse Logistics (Urban Bricolage core)
    ('elena_sischarenco', 'Elena Sischarenco', 'Elena Sischarenco — Urban Bricolage core team', 'p_research', 'CH', [('BETEILIGT_AN','prog_urban_bricolage','core team')]),
    ('vanessa_feri', 'Vanessa Feri', 'Vanessa Feri — Urban Bricolage core team', 'p_research', 'CH', [('BETEILIGT_AN','prog_urban_bricolage','core team')]),
    ('adam_przywara', 'Adam Przywara', 'Adam Przywara — Urban Bricolage core team', 'p_research', 'CH', [('BETEILIGT_AN','prog_urban_bricolage','core team')]),
    ('rahel_jud', 'Rahel Jud', 'Rahel Jud — Urban Bricolage core team', 'p_research', 'CH', [('BETEILIGT_AN','prog_urban_bricolage','core team')]),
    # REFAIR additional Persons + Collectif
    ('valerie_jamet', 'Valérie Jamet', 'Valérie Jamet — DGD de La Fab', 'p_manage', 'FR', [('BETEILIGT_AN','la_fabrique_de_bordeaux_metropole','DGD')]),
    ('aurelie_heraut', 'Aurélie Héraut', 'Aurélie Héraut — directrice de projet, REFAIR pilot at La Fab', 'p_manage', 'FR', [('BETEILIGT_AN','la_fabrique_de_bordeaux_metropole','REFAIR pilot lead')]),
    ('jerome_goze', 'Jérôme Goze', 'Jérôme Goze — Directeur Général Délégué La Fab', 'p_manage', 'FR', [('BETEILIGT_AN','la_fabrique_de_bordeaux_metropole','DGD')]),
    ('collectif_cancan', 'Collectif CANCAN', 'Collectif CANCAN — architect maîtrise d\'œuvre for Base du Réemploi', 'arch', 'FR', [('BETEILIGT_AN','la_fabrique_de_bordeaux_metropole','architect maîtrise d\'œuvre')]),
    # RCMI additional Persons
    ('julius_schaeufele', 'Julius Schäufele', 'Julius Schäufele — Geschäftsführer Concular GmbH', 'p_manage', 'DE', [('BETEILIGT_AN','concular','Geschäftsführer')]),
    ('lenard_da_costa_kurek', 'Lenard da Costa Kurek', 'Lenard da Costa Kurek — RCMI article co-author at Concular', 'p_research', 'DE', [('BETEILIGT_AN','concular','RCMI co-author')]),
    # FCRBE partner orgs
    ('salvo_ltd', 'Salvo Ltd', 'Salvo Ltd — UK reclamation directory and marketplace (FCRBE partner)', 'broker', 'GB', [('BETEILIGT_AN','prog_fcrbe','UK partner')]),
    ('embuild', 'Embuild', 'Embuild — Belgian construction federation (FCRBE partner)', 'ngo', 'BE', [('BETEILIGT_AN','prog_fcrbe','BE partner federation')]),
    ('buildwise', 'Buildwise', 'Buildwise — Belgian Building Research Institute partner (FCRBE)', 'research', 'BE', [('BETEILIGT_AN','prog_fcrbe','BE research partner')]),
    ('cstb', 'CSTB', 'CSTB — Centre Scientifique et Technique du Bâtiment (France, FCRBE)', 'research', 'FR', [('BETEILIGT_AN','prog_fcrbe','FR research partner')]),
    ('brussels_environment', 'Brussels Environment', 'Brussels Environment (Bruxelles Environnement) — FCRBE partner', 'funder', 'BE', [('BETEILIGT_AN','prog_fcrbe','BE public-authority partner')]),
    ('university_of_brighton', 'Univ. of Brighton', 'University of Brighton — UK academic partner (FCRBE)', 'research', 'GB', [('BETEILIGT_AN','prog_fcrbe','UK academic partner')]),
    ('city_of_utrecht', 'City of Utrecht', 'City of Utrecht — NL public-authority partner (FCRBE)', 'client_pub', 'NL', [('BETEILIGT_AN','prog_fcrbe','NL public-authority partner')]),
    ('bellastock', 'Bellastock', 'Bellastock — French reuse architecture/research collective (FCRBE partner)', 'arch', 'FR', [('BETEILIGT_AN','prog_fcrbe','FR partner; reuse architecture/research')]),
]


def emit_adds() -> list[dict]:
    adds: list[dict] = []
    for actor in ACTORS:
        aid, name, name_full, role, land, _ = actor
        props = {'id': aid, 'name': name, 'name_full': name_full, 'source_scope': 'case_markdown'}
        if land:
            props['land'] = land
        adds.append({
            'op': 'add_node',
            'id': aid,
            'labels': ['Akteur'],
            'properties': props,
            'reason': 'Phase 13: new dossier-evidenced Akteur (org or person).',
            'severity': 'LOW',
        })
    return adds


def emit_rels() -> list[dict]:
    rels: list[dict] = []
    for actor in ACTORS:
        aid, _, _, role, _, rel_list = actor
        ar, at = ROLES[role]
        # HAT_AKTEURROLLE
        rels.append({
            'op': 'add_rel', 'from': aid, 'type': 'HAT_AKTEURROLLE', 'to': ar,
            'properties': {'id': f'r_{aid}__HAT_AKTEURROLLE__{ar}', 'source': SRC},
            'reason': 'Phase 13: typed role.', 'severity': 'LOW',
        })
        # HAT_AKTEURTYP
        rels.append({
            'op': 'add_rel', 'from': aid, 'type': 'HAT_AKTEURTYP', 'to': at,
            'properties': {'id': f'r_{aid}__HAT_AKTEURTYP__{at}', 'source': SRC},
            'reason': 'Phase 13: typed actor category.', 'severity': 'LOW',
        })
        # Project links + BELEGT_IN to default Quelle (we'll attach via project's Quelle later)
        for (rel_type, target, rolle_text) in rel_list:
            props = {'id': f'r_{aid}__{rel_type}__{target}', 'source': SRC, 'evidence': 'BELEGT'}
            if rolle_text:
                props['rolle_text'] = rolle_text
            rels.append({
                'op': 'add_rel', 'from': aid, 'type': rel_type, 'to': target,
                'properties': props,
                'reason': 'Phase 13: actor project link.',
                'severity': 'LOW',
            })
    return rels


def main() -> int:
    adds = emit_adds()
    rels = emit_rels()
    out_dir = Path('e:/recherche/_neo4j/review/round_002_followup/patches/batch2')
    a = out_dir / 'phase_batch2_v2_13a_more_actors_addnodes.patch.jsonl'
    r = out_dir / 'phase_batch2_v2_13b_more_actors_rels.patch.jsonl'
    with a.open('w', encoding='utf-8') as f:
        for x in adds:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    with r.open('w', encoding='utf-8') as f:
        for x in rels:
            f.write(json.dumps(x, ensure_ascii=False) + '\n')
    print(f'Wrote {len(adds)} actor add_nodes to {a}')
    print(f'Wrote {len(rels)} typed-rel ops to {r}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
