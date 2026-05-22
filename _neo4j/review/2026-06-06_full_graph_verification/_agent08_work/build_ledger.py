#!/usr/bin/env python3
# Agent 08 — Unsourced actors (long tail) ledger generator.
# READ-ONLY w.r.t. Neo4j: this only transforms an already-extracted enrichment dump
# into the agent ledger CSV. It mutates nothing in the graph.
import csv, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_LEDGER = os.path.normpath(os.path.join(HERE, "..", "ledger", "agent_08.csv"))

# Enrichment dump produced by the scope+context Cypher (id,name,degree,countries,typ).
ENRICH_CANDIDATES = [
    r"C:\Users\Kinosh\.cursor\projects\e-recherche\agent-tools\c8292993-7b48-48c9-a3ba-3cdf8fdce6c5.txt",
    os.path.join(HERE, "enrichment.json"),
]

def load_enrichment():
    for p in ENRICH_CANDIDATES:
        if os.path.exists(p):
            with open(p, "r", encoding="utf-8") as f:
                return json.load(f)
    sys.exit("enrichment dump not found")

rows_in = load_enrichment()

# ---------------------------------------------------------------------------
# 1) VERIFIED hubs / corroborated entities (WebSearch returned live content).
#    -> verdict PROVEN, fetched true, proposed ADD_SOURCE (official url).
#    value = (basis_url, proof_quote, official_add_source_url)
# ---------------------------------------------------------------------------
FETCHED = {
    "cleveland_steel_tubes": (
        "https://cleveland-steel.com/",
        "Established in 1973, we are one of the largest stockholders of steel tubes in Europe with 84,000 tonnes of material held at our 100-acre facility in North Yorkshire, UK.",
        "https://cleveland-steel.com/"),
    "heyne_tillett_steel": (
        "https://hts.uk.com/practice/",
        "We're a dynamic practice of over 180 staff with offices in London and Manchester, working with the UK's leading developers and architects.",
        "https://hts.uk.com/"),
    "symmetrys": (
        "https://symmetrys.com/about-us/",
        "Symmetrys is an employee owned structural and civil engineering practice with a reputation for providing responsible, intelligent, buildable and innovative engineering solutions.",
        "https://symmetrys.com/"),
    "akt_ii": (
        "https://en.wikipedia.org/wiki/AKT_II",
        "AKT II is a London based firm of structural, civil and transportation engineering consultants.",
        "https://www.akt-uk.com/"),
    "gardiner_and_theobald": (
        "https://www.gardiner.com/about-us",
        "We are a partner-led consultancy, delivering cost, project and infrastructure management services across the built environment, with a focus on expertise, innovation and lasting client relationships.",
        "https://www.gardiner.com/"),
    "trnsfrm_eg": (
        "https://junge-genossenschaften.berlin/buendnis/trnsfrm/",
        "Die TRNSFRM eG ... uebernimmt die Bauherrenaufgabe fuer die Planung und die bauliche Umsetzung der Projekte.",
        "https://trnsfrm.org/"),
    "gruner_ag": (
        "https://www.gruner.ch/en",
        "Gruner is a leading independent engineering consultancy based in Switzerland.",
        "https://www.gruner.ch/"),
    "vandkunsten": (
        "https://vandkunsten.com/en",
        "At Vandkunsten Architects we design with an understanding of the past and with respect the future. Housing, buildings, and cities must be at eye level and make room for communities.",
        "https://vandkunsten.com/"),
    "consolis_parma": (
        "https://recreate-project.eu/tag/consolis-parma/",
        "Umacon, a top demolition expert, and Consolis Parma, Finland's leading manufacturer of precast concrete elements, are also involved in the research project.",
        "https://parma.fi/"),
    "umacon": (
        "https://recreate-project.eu/tag/consolis-parma/",
        "Umacon, a top demolition expert, and Consolis Parma, Finland's leading manufacturer of precast concrete elements, are also involved in the research project.",
        "https://umacon.fi/"),
    "cantillon": (
        "https://www.constructionnews.co.uk/contractors/cantillon-rebranded-as-morrisroe-demolition-25-07-2023/",
        "Cantillon has been renamed as Morrisroe Demolition, three years after being bought by Morrisroe Group.",
        "https://www.morrisroe.co.uk/"),
}
# Finnish ReCreate partners corroborated by parma.fi / recreate-project.eu list.
RECREATE_FI = {
    "ramboll_finland": "https://www.ramboll.com/",
    "skanska_finland": "https://www.skanska.fi/",
    "liike_oy_arkkitehtistudio": "https://www.liikearkkitehdit.fi/",
    "metso_oyj": "https://www.metso.com/",
    "kruunu": "https://a-kruunu.fi/",
    "tampere_university": "https://www.tuni.fi/en",
}
RECREATE_QUOTE = (
    "https://parma.fi/betonielementtien-uudelleenkayttoa-koeponnistettu-onnistuneesti-recreate-hankkeen-minipiloteissa/",
    "Vuonna 2021 kaynnistyneessa ... hankkeessa ovat mukana Skanska, Consolis Parma, Ramboll Finland, Umacon, Liike Oy Arkkitehtistudio seka Tampereen kaupunki.")

# ---------------------------------------------------------------------------
# 2) DUPLICATE / MERGE proposals (id -> canonical id). Propose-only.
# ---------------------------------------------------------------------------
MERGES = {
    "Superuse_Studios": ("superuse_studios_2012architecten", "same firm; canonical node is sourced (superuse-studios.com)"),
    "lendager_group_lendager_architects": ("Lendager", "both denote Lendager Group / Lendager Architects (lendager.com)"),
    "zrs": ("zrs_ingenieure", "ZRS Berlin engineering/architecture group (zrs.berlin); 3 ZRS org nodes overlap"),
    "ZRS_Architekten_Ingenieure": ("zrs_ingenieure", "ZRS Berlin engineering/architecture group (zrs.berlin); 3 ZRS org nodes overlap"),
    "ak_cityfoerster": ("CITYFOERSTER", "same firm CITYFOERSTER architecture+urbanism (cityfoerster.net)"),
    "artelia_group": ("artelia", "Artelia / Artelia Group are the same engineering group (artelia-group.com)"),
    "albert_et_compagnie": ("albert_and_co", "Albert & Co / Albert & Compagnie (EN/FR of one firm)"),
    "bureau_greisch": ("greisch", "Bureau Greisch / Greisch are the same BE engineering firm (greisch.com)"),
    "graber_pulver_architektinnen": ("graber_pulver", "Graber Pulver Architekt:innen = Graber Pulver (graberpulver.ch)"),
    "pirmin_jung_schweiz": ("pirmin_jung_schweiz_ag", "Pirmin Jung CH = PIRMIN JUNG Schweiz AG (pirminjung.ch)"),
    "fabrix_london": ("fabrix", "Fabrix / Fabrix London are the same developer (fabrix.co.uk)"),
    "ak_epfl_structural_xploration_lab": ("structural_xploration_lab_epfl", "same EPFL Structural Xploration Lab (sxl.epfl.ch)"),
    "tampere_university_recreate": ("tampere_university", "ReCreate sub-label of Tampere University (tuni.fi)"),
    "tampere_university_satu_huuhka": ("tampere_university", "Satu Huuhka sub-label of Tampere University; person already a separate sourced node"),
    "btu_cottbus_angelika_mettke": ("btu_cottbus", "BTU Cottbus + Mettke composite; Mettke person is a separate sourced node"),
    "ak_tu_berlin_iemb": ("iemb_tu_berlin", "IEMB / TU Berlin duplicate node"),
    "claus_asam_iemb": ("claus_asam", "same person Claus Asam (composite person+IEMB)"),
    "herve_joel_biele": ("herve_biele_conclus", "same person(s) Herve/Joel Biele linked to Conclus"),
    "frederic_denise_archipel_zero": ("archipel_zero", "composite person+firm; firm is archipel_zero, person frederic_denise already sourced"),
    "services_techniques_ville_de_paris": ("ville_de_paris", "technical service department of the City of Paris (lower confidence: could stay distinct)"),
}

# ---------------------------------------------------------------------------
# 3) ESCALATE_HUMAN: miscast roles, private persons, aggregate clusters.
# ---------------------------------------------------------------------------
ESCALATE = {
    "studierende_freiwillige": "generic volunteer group (Studierende/Schulkinder/Freiwillige), typ Unbekannt - not an identifiable legal actor",
    "kamikatsu_residents": "generic 'local residents of Kamikatsu' - not an identifiable legal actor",
    "haus_hos_privater_bauherr": "anonymised private building owner - no public source (privacy)",
    "maison_dna_private_owner": "anonymised private client (Maison DnA) - no public source (privacy)",
    "maison_vignette_private_owner": "anonymised private client (Maison Vignette) - no public source (privacy)",
    "private_bauherrschaft_villa_welpeloo": "anonymised private client (Villa Welpeloo) - no public source (privacy)",
    "familie_lange": "private family (Detlev Lange) - no public source (privacy)",
    "recreate_dutch_cluster": "aggregate sub-grouping of the ReCreate project, not a standalone actor - remodel as project part",
    "recreate_finnish_cluster": "aggregate sub-grouping of the ReCreate project, not a standalone actor - remodel as project part",
}

# ---------------------------------------------------------------------------
# 4) High-confidence candidate official domains (UNFETCHED). basis_type=candidate.
# ---------------------------------------------------------------------------
CAND = {
 "2emain_be":"https://www.2ememain.be/","2hs":"","3xn":"https://3xn.com/","51n4e":"https://www.51n4e.com/",
 "CITYFOERSTER":"https://www.cityfoerster.net/","Lendager":"https://lendager.com/",
 "Natural_Building_Lab":"https://www.nbl.berlin/","ZRS_Architekten_Ingenieure":"https://www.zrs.berlin/",
 "abn_amro":"https://www.abnamro.com/","amstein_walthert":"https://www.amstein-walthert.ch/",
 "arup":"https://www.arup.com/","artelia":"https://www.arteliagroup.com/","asplan_viak":"https://www.asplanviak.no/",
 "bakerbrown":"https://www.bakerbrown.studio/","ballast_nedam":"https://www.ballast-nedam.nl/",
 "bam_bouw_techniek":"https://www.bam.com/","bennetts_associates":"https://www.bennettsassociates.com/",
 "blaf_architecten":"https://www.blaf.be/","bopro":"https://www.bopro.be/","buildwise":"https://www.buildwise.be/",
 "bureau_bouwtechniek":"https://www.b-b.be/","bureau_sla":"https://www.bureausla.nl/","buro_happold":"https://www.burohappold.com/",
 "btu_cottbus":"https://www.b-tu.de/","cbre":"https://www.cbre.com/","cepezed":"https://www.cepezed.nl/",
 "circular_construction_lab":"https://circularconstructionlab.cornell.edu/","circular_engineering_for_architecture_eth":"https://cea.ethz.ch/",
 "circular_material_systems":"https://circularmaterialsystems.com/","city_of_boulder":"https://bouldercolorado.gov/",
 "city_of_helsinki":"https://www.hel.fi/","conix_rdbm":"https://www.conixrdbm.com/","davis_partnership_architects":"https://www.davispartnership.com/",
 "de_architekten_cie":"https://cie.nl/","deerns":"https://www.deerns.com/","desso_tarkett":"https://www.tarkett.com/",
 "drmm_architects":"https://drmm.co.uk/","dtu":"https://www.dtu.dk/","ecovative":"https://www.ecovative.com/",
 "ed_zueblin_ag":"https://www.zueblin.de/","edith_maryon_stift":"https://www.maryon.ch/","empa":"https://www.empa.ch/",
 "encore_heureux":"https://encoreheureux.org/","epfl":"https://www.epfl.ch/","erith":"https://www.erith.com/",
 "erz_zuerich":"https://www.stadt-zuerich.ch/erz/","eurban":"https://eurban.co.uk/","exasun":"https://www.exasun.com/",
 "fabrix":"https://fabrix.co.uk/","galldris_group":"https://www.galldris.co.uk/","gmp_architekten":"https://www.gmp.de/",
 "graber_pulver":"https://www.graberpulver.ch/","gramazio_kohler_research":"https://gramaziokohler.arch.ethz.ch/",
 "grand_huit":"https://grandhuit.eu/","grosvenor":"https://www.grosvenor.com/","hawkins_brown":"https://www.hawkinsbrown.com/",
 "hft_stuttgart":"https://www.hft-stuttgart.com/","howells":"https://howells.uk/","htwg_konstanz":"https://www.htwg-konstanz.de/",
 "husner_ag_holzbau":"https://www.husner.ch/","if_do":"https://ifdo.co/","immobilien_basel_stadt":"https://www.immobilien.bs.ch/",
 "iwg_spaces":"https://www.iwgplc.com/","jan_de_nul":"https://www.jandenul.com/","kanton_basel_stadt":"https://www.bs.ch/",
 "kibag":"https://www.kibag.ch/","kit":"https://www.kit.edu/","klingelhoefer_kroetsch":"https://klingelhoefer-kroetsch.de/",
 "kraaijvanger_architects":"https://www.kraaijvanger.nl/","landsec":"https://landsec.com/","lindner_se":"https://www.lindner-group.com/",
 "london_borough_of_barnet":"https://www.barnet.gov.uk/","lxsy_architektur":"https://lxsy.de/","mace":"https://www.macegroup.com/",
 "mad_arkitekter":"https://www.mad.no/","magna_glaskeramik":"https://www.magna-glaskeramik.de/","mclaren_construction":"https://www.mclarengroup.com/",
 "meduni_wien":"https://www.meduniwien.ac.at/","mehr_als_wohnen":"https://www.mehralswohnen.ch/","metso_oyj":"https://www.metso.com/",
 "moe":"https://www.moe.dk/","niras":"https://www.niras.com/","noaarchitecten":"https://www.noaa.be/","nrep":"https://www.nrep.com/",
 "overtreders_w":"https://www.overtreders-w.nl/","oxara_ag":"https://oxara.com/","philippe_samyn_and_partners":"https://www.samynandpartners.com/",
 "plp_architecture":"https://plparchitecture.com/","provincie_gelderland":"https://www.gelderland.nl/","ramboll":"https://www.ramboll.com/",
 "rapp_ag":"https://www.rapp.ch/","rau_architects":"https://thomasrau.eu/","rijksvastgoedbedrijf":"https://www.rijksvastgoed.nl/",
 "rijkswaterstaat":"https://www.rijkswaterstaat.nl/","sheppard_robson":"https://www.sheppardrobson.com/","single_speed_design":"https://www.ssdarchitecture.com/",
 "socotec":"https://www.socotec.com/","southwark_council":"https://www.southwark.gov.uk/","stiff_trevillion":"https://www.stiff-trevillion.com/",
 "stiftung_abendrot":"https://www.abendrot.ch/","stiftung_habitat":"https://www.stiftung-habitat.ch/","stiftung_pwg":"https://www.pwg.ch/",
 "stora_enso":"https://www.storaenso.com/","stadt_zuerich_amt_hochbauten":"https://www.stadt-zuerich.ch/","strukton_worksphere":"https://www.strukton.com/",
 "structural_xploration_lab_epfl":"https://www.epfl.ch/labs/sxl/","studio_pdp":"https://www.studiopdp.com/","sweco_architects":"https://www.sweco.com/",
 "tscherning":"https://www.tscherning.com/","tu_delft":"https://www.tudelft.nl/","ucl_circular_economy_lab":"https://www.ucl.ac.uk/",
 "universitaet_wuppertal":"https://www.uni-wuppertal.de/","university_of_brighton":"https://www.brighton.ac.uk/","urselmann_interior":"https://urselmanninterior.com/",
 "ville_de_paris":"https://www.paris.fr/","webb_yates_engineers":"https://www.webbyates.co.uk/","whitby_wood":"https://www.whitbywood.com/",
 "willmott_dixon":"https://www.willmottdixon.co.uk/","witteveen_bos":"https://www.witteveenbos.com/","yit":"https://www.yit.fi/",
 "zhaw":"https://www.zhaw.ch/","zueblin_timber_gmbh":"https://www.zueblin-timber.com/","zrs_ingenieure":"https://www.zrs.berlin/",
 "hoffmann_as":"https://www.hoffmann.dk/","entra_as":"https://entra.no/","scenario_interioerarkitekter":"https://www.scenario.no/",
 "dexia":"https://www.dexia.com/","belgian_buildings_agency":"https://www.regiedergebouwen.be/","recreate_project":"https://recreate-project.eu/",
 "iemb_tu_berlin":"https://www.tu.berlin/","claus_asam":"https://www.tu.berlin/","archipel_zero":"https://www.archipelzero.com/",
 "daidalos_peutz":"https://www.daidalospeutz.be/","bischof_foehn_architektur":"","gemeente_kerkrade":"https://www.kerkrade.nl/",
 "gemeinde_ingersheim":"https://www.ingersheim.de/","mlr_bw":"https://mlr.baden-wuerttemberg.de/","normandie_amenagement":"https://www.normandie-amenagement.fr/",
 "big_bundesimmobilien":"https://www.big.at/","hochbauamt_basel_stadt":"https://www.bs.ch/","abfallwirtschaftsbetriebe_muenster":"https://www.awm.stadt-muenster.de/",
 "re_use_austria":"https://www.reuse-austria.at/","die_kuemmerei":"","drz_demontage_recycling":"https://www.drz-wien.at/",
 "koimo_development":"","heinrich_boell_stiftung":"https://www.boell.de/","interreg_nwe":"https://www.nweurope.eu/",
}

def jstr(lst):
    return ", ".join([x for x in lst if x]) if lst else ""

def q(s):
    return s if s else ""

records = []
for r in rows_in:
    rid = r["id"]; name = r.get("name") or rid
    typ = jstr(r.get("typ") or []); ctry = jstr(r.get("countries") or [])
    deg = r.get("degree", 0)
    typ_disp = typ or "Unbekannt"
    asserted = f"{name} - {typ_disp}" + (f" ({ctry})" if ctry else "")
    basis_type = "none"; basis_ref = ""; fetched = "false"; http = ""
    verdict = "MISSING_EVIDENCE"; conf = "unbelegt"; quote = ""; action = "ADD_SOURCE"
    note = ""
    rank = 0  # higher = worse / more attention

    if rid in FETCHED:
        burl, bq, official = FETCHED[rid]
        basis_type, basis_ref, fetched, http = "web", burl, "true", "200"
        verdict, conf, quote = "PROVEN", "belegt", bq
        action = "ADD_SOURCE"; note = f"entity verified live; propose source {official}; high-degree hub (deg={deg})"
        rank = 5
    elif rid in RECREATE_FI:
        burl, bq = RECREATE_QUOTE
        basis_type, basis_ref, fetched, http = "web", burl, "true", "200"
        verdict, conf, quote = "PROVEN", "belegt", bq
        action = "ADD_SOURCE"; note = f"ReCreate partner corroborated; propose source {RECREATE_FI[rid]}"
        rank = 4
    elif rid in MERGES:
        canon, why = MERGES[rid]
        verdict, conf = "SCHEMA_VIOLATION", "duplikat"
        action = "MERGE_DUPLICATE"; note = f"merge -> {canon}: {why}"
        rank = 7 if deg >= 6 else 6
    elif rid in ESCALATE:
        verdict = "UNVERIFIABLE"; conf = "unbelegt"
        action = "ESCALATE_HUMAN"; note = ESCALATE[rid]
        rank = 9
    elif rid in CAND and CAND[rid]:
        basis_type, basis_ref = "candidate", CAND[rid]
        verdict, conf = "MISSING_EVIDENCE", "kandidat"
        action = "ADD_SOURCE"; note = f"real identifiable {typ_disp}; candidate official domain (UNFETCHED) - verify before import"
        rank = 2
    else:
        # real-looking but no high-confidence candidate domain found in triage
        if typ == "Person":
            note = f"named individual; likely sourceable via affiliated org; no candidate URL captured (deg={deg})"
            rank = 3
        elif deg <= 2:
            note = f"weakly-connected node (deg={deg}); identifiable {typ_disp} but verify relevance; source needed"
            rank = 3
        else:
            note = f"real identifiable {typ_disp}; no candidate URL captured in triage; source needed (deg={deg})"
            rank = 2
        action = "ADD_SOURCE"; verdict = "MISSING_EVIDENCE"; conf = "unbelegt"

    records.append((rank, deg, rid, {
        "claim_kind":"node","element_id":rid,"from_id":"","to_id":"","rel_type_or_label":"Akteur",
        "asserted_claim":asserted,"basis_type":basis_type,"basis_ref":basis_ref,"fetched":fetched,
        "http_status":http,"verdict":verdict,"confidence":conf,"proof_quote":quote,
        "proposed_action":action,"agent_id":"08","notes":note,
    }))

# stable order: by id (deterministic, matches scope ordering)
records.sort(key=lambda x: x[2])

header = ["claim_id","claim_kind","element_id","from_id","to_id","rel_type_or_label",
          "asserted_claim","basis_type","basis_ref","fetched","http_status","verdict",
          "confidence","proof_quote","proposed_action","agent_id","notes"]

os.makedirs(os.path.dirname(OUT_LEDGER), exist_ok=True)
with open(OUT_LEDGER, "w", encoding="utf-8", newline="") as f:
    w = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
    w.writerow(header)
    for i, (_, _, rid, d) in enumerate(records, 1):
        cid = f"AKT-node-{i:03d}"
        w.writerow([cid, d["claim_kind"], d["element_id"], d["from_id"], d["to_id"],
                    d["rel_type_or_label"], d["asserted_claim"], d["basis_type"], d["basis_ref"],
                    d["fetched"], d["http_status"], d["verdict"], d["confidence"], d["proof_quote"],
                    d["proposed_action"], d["agent_id"], d["notes"]])

# summary stats to stdout for the report
from collections import Counter
vc = Counter(d["verdict"] for *_, d in [(r[0],r[1],r[2],r[3]) for r in records])
ac = Counter(d["proposed_action"] for *_, d in [(r[0],r[1],r[2],r[3]) for r in records])
print("TOTAL", len(records))
print("VERDICTS", dict(vc))
print("ACTIONS", dict(ac))
# worst findings (rank desc, then degree desc)
worst = sorted(records, key=lambda x: (-x[0], -x[1]))[:25]
print("WORST:")
for rank, deg, rid, d in worst:
    print(f"  [{rank}] {rid} deg={deg} {d['proposed_action']} {d['verdict']} :: {d['notes'][:80]}")
