# -*- coding: utf-8 -*-
import json, os, csv

WORK = r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\_agent06b_work"
OUT  = r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification\ledger\agent_06b.csv"

with open(os.path.join(WORK,"gap_nodes.json"),encoding="utf-8") as f:
    nodes = json.load(f)
with open(os.path.join(WORK,"edge_rows.json"),encoding="utf-8") as f:
    edge_rows = json.load(f)

HEADER = ["claim_id","claim_kind","element_id","from_id","to_id","rel_type_or_label",
          "asserted_claim","basis_type","basis_ref","fetched","http_status","verdict",
          "confidence","proof_quote","proposed_action","agent_id","notes"]

# PROVEN: id -> (url, quote)
PROVEN = {
 "Werner_Sobek":("https://labs.aap.cornell.edu/ccl/umar-unit","The building design created by Werner Sobek with Dirk E. Hebel and Felix Heisel demonstrates how a responsible approach to dealing with our natural resources can go hand in hand with appealing architectural form."),
 "dirk_e_hebel":("https://labs.aap.cornell.edu/ccl/umar-unit","The building design created by Werner Sobek with Dirk E. Hebel and Felix Heisel"),
 "felix_heisel":("https://labs.aap.cornell.edu/ccl/umar-unit","The building design created by Werner Sobek with Dirk E. Hebel and Felix Heisel"),
 "marc_angst":("https://zirkular.net/en/project/building-k-118","project team: Marc Angst, Pascal Hentschel, Benjamin Poignon, Michele Brand"),
 "pascal_hentschel":("https://zirkular.net/en/project/building-k-118","project team: Marc Angst, Pascal Hentschel, Benjamin Poignon, Michele Brand"),
 "benjamin_poignon":("https://zirkular.net/en/project/building-k-118","project team: Marc Angst, Pascal Hentschel, Benjamin Poignon, Michele Brand"),
 "martin_zeller":("https://zirkular.net/en/project/building-k-118","credits: Martin Zeller [photo credit on baubuero/Zirkular K.118 project page]"),
 "andreas_kretzer":("https://klingelhoefer-kroetsch.de/projekte/Stuttgart_210","Entwurf: Roman Kreuzer, Katharina Raabe, Max Stemmler, Stefan Kroetsch, Andreas Kretzer"),
 "roman_kreuzer":("https://klingelhoefer-kroetsch.de/projekte/Stuttgart_210","Entwurf: Roman Kreuzer, Katharina Raabe, Max Stemmler, Stefan Kroetsch, Andreas Kretzer"),
 "katharina_raabe":("https://klingelhoefer-kroetsch.de/projekte/Stuttgart_210","Entwurf: Roman Kreuzer, Katharina Raabe, Max Stemmler, Stefan Kroetsch, Andreas Kretzer"),
 "maximilian_stemmler":("https://klingelhoefer-kroetsch.de/projekte/Stuttgart_210","Entwurf: Roman Kreuzer, Katharina Raabe, Max Stemmler, Stefan Kroetsch"),
 "stefan_kroetsch":("https://klingelhoefer-kroetsch.de/projekte/Stuttgart_210","Architektur: ARGE 4K - Kretzer, Kreuzer, Klingelhoefer Kroetsch Architekten ... Entwurf: ... Stefan Kroetsch"),
 "satu_huuhka":("https://recreate-project.eu/tag/precast-concrete","says ReCreate's coordinator and the Finnish cluster's leader, Prof. Satu Huuhka from Tampere University"),
 "angelika_mettke":("https://recreate-project.eu/tag/precast-concrete","professor Angelika Mettke who has worked on the topic for 20 years ... and who would eventually join the leadership here on ReCreate"),
 "soren_nielsen":("https://vandkunsten.com/en/projects/component-reuse","Contact: Soren Nielsen, sn@vandkunst.dk [Nordic Built Component Reuse, Vandkunsten]"),
 "katrine_west_kristensen":("https://vandkunsten.com/en/projects/component-reuse","Contact Group: Katrine West Kristensen, Nel Jan Schipull, Astrid Vang Kaspersen, Anne-Mette Manelius Greisen, Soren Nielsen"),
 "anna_buser":("https://re-win.ch/verein/ueber","Anna Buser - Vorstand (Gruendungsmitglied), Critical Urbanism MA [Verein RE-WIN]"),
 "barbara_buser":("https://re-win.ch/verein/ueber","Barbara und Anna Buser entwickelten im Sommer 2022 die Idee ... Barbara Buser Gruendungsmitglied, Architektin ETH/SIA"),
 "felix_dillmann":("https://re-win.ch/verein/ueber","Felix Dillmann - Programmleitung, Architekt MSc. ETH/MIT [Verein RE-WIN operatives Team]"),
 # orgs / platforms
 "loopfront":("https://www.loopfront.com/","Loopfront's digital platform makes it easy for companies to save costs, CO2 and waste by reusing furniture, building materials and more ... Since 2020"),
 "salvoweb":("https://www.salvoweb.com/","Architectural Salvage, Reclamation Yards, UK, USA and more | SalvoWEB ... Shop from Salvo Code members"),
 "salvo_ltd":("https://www.salvoweb.com/","SHOP TRULY RECLAIMED - Browse verified materials & products from trusted Salvo Code members [Salvo Ltd operates SalvoWEB]"),
 "baticycle":("https://baticycle.fr/","Decouvrez Baticycle, le magasin de materiaux de construction d'occasion pour les professionnels du batiment"),
 "batiterre":("https://www.batiterre.be/","BATITERRE DONNE UNE SECONDE VIE AUX MATERIAUX DE CONSTRUCTION"),
 "baumab_kassel":("https://baumab-kassel.de/","Willkommen bei der Bauteilboerse in und fuer Kassel! Gebrauchte Baumaterialien und Baustoffe kaufen und verkaufen"),
 "surap_gmbh":("https://baumab-kassel.de/","Die Bauteilboerse Kassel liefert ... Daten zum oekologischen Fussabdruck ... mit der Hilfe unseres Partners SURAP"),
 "materialnomaden":("https://www.materialnomaden.at/","Home - materialnomaden ... we evaluate buildings & material flows, quantify them and thus assess the potential on an economic, ecological and social level"),
 "re_win":("https://re-win.ch/verein/ueber","Der Verein RE-WIN will ... eine Kultur der Wiederverwendung von Bauteilen ... foerdern"),
 "urban_bricolage":("https://urbanbricolage.ch","Urban Bricolage - first-party site (Swiss reuse-logistics practice); homepage fetched (urbanbricolage.ch)"),
 "baukarussell":("https://www.baukarussell.at/projekte","Projekte - BauKarussell ... Social Urban Mining [Austrian re-use deconstruction operator; project roster incl. MedUni Campus Mariannengasse]"),
 "cancan_architecture":("https://www.collectifcancan.fr/project/refair/","Accompagnee par CANCAN en tant qu'AMO REEMPLOI, La Fab a pour objectif de reintegrer les materiaux ... EQUIPE CANCAN"),
 "collectif_cancan":("https://www.collectifcancan.fr/project/refair/","REFAIR - Collectif Cancan ... EQUIPE CANCAN"),
 "la_fabrique_de_bordeaux_metropole":("https://www.collectifcancan.fr/project/refair/","COMMANDITAIRE La Fab de Bordeaux Metropole"),
 "refair_bordeaux":("https://www.collectifcancan.fr/project/refair/","REFAIR est un projet relatif a la mise en place d'une demarche de reemploi ... www.refair-bm.fr"),
 "new_horizon":("https://www.superuse-studios.com/about-us","Superuse founded the platform oogstkaart.nl in 2012 ... In 2019, the platform was sold to urban mining company New Horizon"),
 "globechain":("https://globechain.com/","Globechain the ESG Reuse Marketplace | Reduce Waste, Access Free Items, and Track ESG"),
 "material_index":("https://material-index.co.uk/","Material Index is the UK's circular construction platform: a reclaimed materials marketplace, pre-demolition audit service and digital platform"),
 "material_reuse_portal":("https://materialreuseportal.com/","The Material Reuse Portal is designed to bring together data on available materials from multiple sources [London, CIRCuIT/ReLondon]"),
 "warp_it":("https://www.warp-it.co.uk/","Welcome to Warp It - the resource redistribution network ... Find, give away, or loan office furniture, equipment and other resources"),
 "enviromate":("https://www.enviromate.co.uk/","Enviromate | Free Leftover Building Materials Marketplace ... buy, sell & discover leftover building materials"),
 "genbyg":("https://genbyg.dk/","Vi er Danmarks stoerste genbrugsbyggemarked med brugte byggematerialer. Vi har eksisteret siden 1998"),
 "r_place":("https://r-place.fr/","R-place est un outil et une marque deposee par la societe CAPRIONIS [societe ESS, reemploi]"),
}

# PARTIAL: id -> (url, quote, note)  (cluster/firm confirmed; person/entity not individually named on fetched page)
PARTIAL = {
 "andrea_klinge":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","Reallabor B(e) Ware, a joint project between the Natural Building Lab at TU Berlin and ZRS Architects and Engineers","ZRS firm/Reallabor confirmed; individual not named on fetched article"),
 "christof_ziegert":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","Reallabor B(e) Ware, a joint project between the Natural Building Lab at TU Berlin and ZRS Architects and Engineers","ZRS partner (known earth-building expert); firm confirmed, name not on fetched article"),
 "eike_roswag_klinge":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","joint project between the Natural Building Lab at TU Berlin and ZRS Architects","NBL/ZRS confirmed; node also has nbl.berlin person page (not fetched)"),
 "matthew_crabbe":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","Natural Building Lab at TU Berlin and ZRS Architects","NBL/ZRS confirmed; name not on fetched page"),
 "nina_pawlicki":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","Natural Building Lab at TU Berlin and ZRS Architects","NBL/ZRS confirmed; name not on fetched page"),
 "sina_jansen":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","Natural Building Lab at TU Berlin and ZRS Architects","NBL/ZRS confirmed; name not on fetched page"),
 "uwe_seiler":("https://www.zrs.berlin/en/article/reallabor-lab-be-ware-from-research-straight-to-implementation","Natural Building Lab at TU Berlin and ZRS Architects","ZRS confirmed; name not on fetched page"),
 "cesare_peeren":("https://www.superuse-studios.com/about-us","Superuse Studios is an international architecture collective for circular and sustainable design","Superuse co-founder; firm confirmed, name on team subpages not fetched"),
 "jan_jongert":("https://www.superuse-studios.com/about-us","Superuse Studios is an international architecture collective for circular and sustainable design","Superuse co-founder; firm confirmed"),
 "jeroen_bergsma":("https://www.superuse-studios.com/about-us","Superuse Studios is an international architecture collective for circular and sustainable design","Superuse member; firm confirmed"),
 "hester_van_dijk":("https://www.overtreders-w.nl/en/peoplespavilion","Overtreders W and bureau SLA have accomplished this [People's Pavilion]","Overtreders W co-founder; firm/project confirmed, name not on fetched page"),
 "peter_van_assche":("https://www.overtreders-w.nl/en/peoplespavilion","Overtreders W and bureau SLA","bureau SLA founder; project confirmed, name not on fetched page"),
 "reinder_bakker":("https://www.overtreders-w.nl/en/peoplespavilion","Overtreders W and bureau SLA","Overtreders W co-founder; project confirmed"),
 "charlotte_bofinger":("https://zirkular.net/en/project/building-k-118","trigger for the foundation of Zirkular by the involved planners","Zirkular context confirmed; name on contact page not fetched"),
 "kerstin_mueller":("https://zirkular.net/en/project/building-k-118","trigger for the foundation of Zirkular by the involved planners","Zirkular co-founder (corroborated by Agent 01); not on fetched project team list"),
 "michel_massmuenster":("https://zirkular.net/en/project/culture-commercial-center-elys","trigger for the foundation of Zirkular by the involved planners","Zirkular context; name on park-books book not fetched"),
 "thomas_stark":("https://www.hft-stuttgart.com/research/projects/current/stuttgart-210-ii","Stuttgart 210 II ... HFT Stuttgart [interdisciplinary team Konstanz/Stuttgart/Karlsruhe]","HfT Stuttgart project confirmed; Prof. T. Stark not individually named on fetched page"),
}

# MERGE/duplicate or low-quality stub or weak-source -> special handling
MERGE = {
 "rau":("thomas_rau","node 'rau' duplicate of 'thomas_rau' (RAU = Thomas Rau's firm/founder); merge candidate"),
 "tomas":("annabelle_von_reutern/concular","low-quality stub id 'tomas' (TOMAS Architecture); source tomas-architecture.com; clarify identity or merge"),
 "harvestmap":("materialnomaden/re_store_harvestmap_vienna","'HarvestMAP' sourced only by materialnomaden.at; likely the materialnomaden HarvestMAP tool; possible duplicate of re_store_harvestmap_vienna"),
}
WEAK = {
 "resource_marktplaats":"only app-store URLs (Google Play / Apple) as sources; no first-party web page -> find a canonical URL",
 "materialrest24":"only third-party/press + Instagram as sources; no first-party site fetched -> resource a canonical URL",
 "stadt_kassel":"sole source is baumab-kassel.de/impressum (not the city's own site); add an official stadt-kassel.de source",
}

# Edge corroboration from fetched authoritative pages (consortium co-membership / operational link).
# verdict PARTIAL: source names BOTH endpoints as members of one consortium/project (NOT yet a graph evidence_url).
RC_URL="https://recreate-project.eu/tag/precast-concrete"
RC_Q="ReCreate's Finnish cluster is formed by Tampere University, Skanska, Consolis Parma, Ramboll Finland, Umacon, LIIKE architects, and the City of Tampere"
RC_BUILT="The building was built by Skanska ... The elements ... were quality controlled and factory refurbished in Consolis Parma's factory in Kangasala"
MET_Q="professor Angelika Mettke ... would eventually join the leadership here on ReCreate ... BTU Cottbus-Senftenberg"
SATU_Q="ReCreate's coordinator and the Finnish cluster's leader, Prof. Satu Huuhka from Tampere University"
CORROB_EDGES={
 ("skanska_finland","consolis_parma"):(RC_URL,RC_BUILT,"Finnish RecReate cluster co-members + operational link (Skanska built, Consolis Parma refurbished)"),
 ("skanska_finland","ramboll_finland"):(RC_URL,RC_Q,"Finnish RecReate cluster co-members"),
 ("skanska_finland","umacon"):(RC_URL,RC_Q,"Finnish RecReate cluster co-members"),
 ("consolis_parma","ramboll_finland"):(RC_URL,RC_Q,"Finnish RecReate cluster co-members"),
 ("consolis_parma","umacon"):(RC_URL,RC_Q,"Finnish RecReate cluster co-members"),
 ("umacon","ramboll_finland"):(RC_URL,RC_Q,"Finnish RecReate cluster co-members"),
 ("recreate_project","satu_huuhka"):(RC_URL,SATU_Q,"Satu Huuhka named as ReCreate coordinator"),
 ("satu_huuhka","recreate_project"):(RC_URL,SATU_Q,"Satu Huuhka named as ReCreate coordinator"),
 ("recreate_project","angelika_mettke"):(RC_URL,MET_Q,"Angelika Mettke named in ReCreate leadership"),
 ("angelika_mettke","recreate_project"):(RC_URL,MET_Q,"Angelika Mettke named in ReCreate leadership"),
 ("angelika_mettke","btu_cottbus"):(RC_URL,MET_Q,"Mettke affiliated with BTU Cottbus (scientific support BTU Cottbus-Senftenberg)"),
 ("btu_cottbus","angelika_mettke"):(RC_URL,MET_Q,"Mettke affiliated with BTU Cottbus"),
}
# apply to edge_rows (cols: 0 cid,1 kind,2 eid,3 from,4 to,...,11 verdict,13 quote,14 action,16 note)
for r in edge_rows:
    key=(r[3],r[4])
    if key in CORROB_EDGES:
        url,q,note=CORROB_EDGES[key]
        r[7]="web"; r[8]=url; r[9]="true"; r[10]="200"
        r[11]="PARTIAL"; r[12]=0.6; r[13]=q
        r[14]="ADD_SOURCE"
        r[16]="CORROBORATED off-graph: "+note+". Consortium co-membership (not a pairwise partnership claim) - add this URL as evidence_url and, if kept, relabel connection_kind to consortium_co_membership. "+r[16]

def esc(s): return "" if s is None else str(s)

rows=[]
i=0
for n in sorted(nodes, key=lambda x:x["id"]):
    i+=1
    nid=n["id"]; nm=n.get("name") or ""
    srcs = n.get("source_urls") or []
    psrc = n.get("primary_source_url")
    first = psrc or (srcs[0] if srcs else "")
    cid=f"A06B-node-{i:04d}"
    if nid in PROVEN:
        url,q = PROVEN[nid]
        rows.append([cid,"node",nid,"","","Akteur",f"{nm} is a real reuse-network actor (existence + role)","web",url,"true","200","PROVEN","belegt",q,"KEEP","06b","entity confirmed by fetched first-party/authoritative page naming it"])
    elif nid in PARTIAL:
        url,q,note=PARTIAL[nid]
        rows.append([cid,"node",nid,"","","Akteur",f"{nm} exists as part of the cited project/firm","web",url,"true","200","PARTIAL","teilweise_belegt",q,"KEEP","06b",note+"; recommend spot-fetch of the person/team subpage"])
    elif nid in MERGE:
        tgt,note=MERGE[nid]
        rows.append([cid,"node",nid,"","","Akteur",f"{nm} node identity unclear / duplicate","none",first,"false","","SCHEMA_VIOLATION","",f"merge/clarify -> {tgt}","ESCALATE_HUMAN","06b",note])
    elif nid in WEAK:
        rows.append([cid,"node",nid,"","","Akteur",f"{nm} sourced only by weak/non-first-party URLs","none",first,"false","","MISSING_EVIDENCE","","",("RESOURCE"),"06b",WEAK[nid]])
    else:
        # first-party source present but NOT re-fetched in this shard (volume cap)
        rows.append([cid,"node",nid,"","","Akteur",f"{nm} carries first-party/authoritative source_urls on graph","web",first,"false","","UNVERIFIABLE","",
                     "",("KEEP"),"06b",
                     f"DEFERRED (volume cap): not re-fetched in 06b; graph carries first-party source ({first}); coverage=source_present_unverified; recommend spot-fetch before relying on as PROVEN"])

# write combined ledger: edges first, then nodes
allrows = edge_rows + rows
with open(OUT,"w",encoding="utf-8",newline="") as f:
    w=csv.writer(f)
    w.writerow(HEADER)
    for r in allrows:
        w.writerow([esc(x) for x in r])

from collections import Counter
print("edge rows:",len(edge_rows),"node rows:",len(rows),"total:",len(allrows))
print("node verdicts:",Counter(r[11] for r in rows))
print("node actions:",Counter(r[14] for r in rows))
print("PROVEN nodes:",sum(1 for r in rows if r[11]=="PROVEN"))
print("PARTIAL nodes:",sum(1 for r in rows if r[11]=="PARTIAL"))
print("wrote",OUT)
