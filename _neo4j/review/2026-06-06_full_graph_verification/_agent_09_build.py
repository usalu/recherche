#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Agent 09 ledger builder (READ-ONLY analysis; no Neo4j writes).

Consumes the read-cypher exports (agent-tools JSON dumps) plus the
2026-06-06_project_bg_geo_extract geo files, runs structural / geo
consistency checks, and emits ledger/agent_09.csv + a stats summary.
"""
import json, csv, os, io, sys

BASE = r"e:\recherche"
ATOOLS = r"C:\Users\Kinosh\.cursor\projects\e-recherche\agent-tools"
GEO = os.path.join(BASE, r"_neo4j\review\2026-06-06_project_bg_geo_extract")
OUTDIR = os.path.join(BASE, r"_neo4j\review\2026-06-06_full_graph_verification")
LEDGER = os.path.join(OUTDIR, "ledger", "agent_09.csv")

NODES_F = os.path.join(ATOOLS, "ecf3879d-6fe4-4b48-97ec-97bbdc042902.txt")
RELS_F  = os.path.join(ATOOLS, "e1dab0df-18f5-470e-9524-0a0850155fc6.txt")
LIL_F   = os.path.join(ATOOLS, "287700c8-9f14-4f14-a04e-91fd8e7105f1.txt")
LIS_F   = os.path.join(ATOOLS, "999dc048-d3ed-45f9-b741-41365ccbb3a5.txt")

def loadj(p):
    with io.open(p, "r", encoding="utf-8") as f:
        return json.load(f)

def loadjsonl(p):
    out=[]
    with io.open(p,"r",encoding="utf-8") as f:
        for line in f:
            line=line.strip()
            if line:
                out.append(json.loads(line))
    return out

nodes = loadj(NODES_F)
rels  = loadj(RELS_F)
lil   = loadj(LIL_F)
lis   = loadj(LIS_F)

donor_addr = loadj(os.path.join(GEO,"donor_bauwerke_addresses.json"))
reuse_geo  = loadj(os.path.join(GEO,"reuse_geo_graph.json"))
akteur_geo = loadj(os.path.join(GEO,"akteur_typ_projekt_geo.json"))
geo_evi    = loadjsonl(os.path.join(GEO,"sidecar","geo_evidence.jsonl"))

# ---- Stadt -> Land (from graph) ----
STADT_LAND = {
 "stadt_aarhus":"Dänemark","stadt_amsterdam":"Niederlande","stadt_arnhem":"Niederlande",
 "stadt_asse":"Belgien","stadt_auderghem_brussels":"Belgien","stadt_basel":"Schweiz",
 "stadt_berlin":"Deutschland","stadt_berlin_marzahn":"Deutschland",
 "stadt_bleijerheide_kerkrade":"Niederlande","stadt_bordeaux":"Frankreich","stadt_boston":"USA",
 "stadt_boulder_colorado":"USA","stadt_brighton":"Vereinigtes Königreich","stadt_bruessel":"Belgien",
 "stadt_brussel_anderlecht":"Belgien","stadt_cambridge_ma":"USA","stadt_canterbury":"Vereinigtes Königreich",
 "stadt_coimbra":"Portugal","stadt_colombelles":"Frankreich","stadt_dilbeek":"Belgien",
 "stadt_duiven":"Niederlande","stadt_dundee":"Vereinigtes Königreich","stadt_duebendorf":"Schweiz",
 "stadt_duesseldorf":"Deutschland","stadt_eindhoven":"Niederlande","stadt_enschede":"Niederlande",
 "stadt_esch_sur_alzette":"Luxemburg","stadt_frankfurt_oder":"Deutschland","stadt_fribourg":"Schweiz",
 "stadt_gentbrugge":"Belgien","stadt_gladsaxe":"Dänemark","stadt_groeditz":"Deutschland",
 "stadt_hannover":"Deutschland","stadt_hastings":"Vereinigtes Königreich","stadt_heerde":"Niederlande",
 "stadt_helsinki":"Finnland","stadt_hoyerswerda":"Deutschland","stadt_ingersheim":"Deutschland",
 "stadt_kamikatsu":"Japan","stadt_kloetinge":"Niederlande","stadt_kopenhagen":"Dänemark",
 "stadt_leiden":"Niederlande","stadt_leinefelde":"Deutschland","stadt_lexington_ma":"USA",
 "stadt_liege":"Belgien","stadt_lo_reninge":"Belgien","stadt_london":"Vereinigtes Königreich",
 "stadt_luxembourg_limpertsberg":"Luxemburg","stadt_maassluis":"Niederlande","stadt_mehrow":"Deutschland",
 "stadt_molenbeek_saint_jean":"Belgien","stadt_mouscron":"Belgien","stadt_merignac":"Frankreich",
 "stadt_muehlhausen_thueringen":"Deutschland","stadt_muenchen":"Deutschland","stadt_muenster":"Deutschland",
 "stadt_oegstgeest":"Niederlande","stadt_oslo":"Norwegen","stadt_paris":"Frankreich",
 "stadt_paso_robles_templeton_gap":"USA","stadt_plauen":"Deutschland","stadt_rotterdam":"Niederlande",
 "stadt_ruemlang":"Schweiz","stadt_schildow":"Deutschland","stadt_stains":"Frankreich",
 "stadt_stuttgart":"Deutschland","stadt_tampere":"Finnland","stadt_terneuzen":"Niederlande",
 "stadt_utrecht":"Niederlande","stadt_volkenroda_koerner":"Deutschland","stadt_wien":"Österreich",
 "stadt_winterthur":"Schweiz","stadt_zuerich":"Schweiz","stadt_s_hertogenbosch":"Niederlande",
}

# ---- country detection from address strings ----
COUNTRY_TOKENS = [
 ("united kingdom","Vereinigtes Königreich"),("vereinigtes königreich","Vereinigtes Königreich"),
 ("england","Vereinigtes Königreich"),("scotland","Vereinigtes Königreich"),
 ("germany","Deutschland"),("deutschland","Deutschland"),
 ("france","Frankreich"),("frankreich","Frankreich"),
 ("belgium","Belgien"),("belgien","Belgien"),("belgique","Belgien"),("belgië","Belgien"),
 ("netherlands","Niederlande"),("niederlande","Niederlande"),("nederland","Niederlande"),
 ("switzerland","Schweiz"),("schweiz","Schweiz"),("suisse","Schweiz"),("svizzera","Schweiz"),
 ("luxembourg","Luxemburg"),("luxemburg","Luxemburg"),
 ("austria","Österreich"),("österreich","Österreich"),
 ("denmark","Dänemark"),("dänemark","Dänemark"),("danmark","Dänemark"),
 ("finland","Finnland"),("finnland","Finnland"),
 ("norway","Norwegen"),("norwegen","Norwegen"),
 ("portugal","Portugal"),
 ("japan","Japan"),
 ("united states","USA"),("usa","USA"),
]

def detect_country(addr):
    if not addr: return None
    a = addr.lower()
    # prefer last comma segment for trailing-country match
    last = a.split(",")[-1].strip()
    for tok,land in COUNTRY_TOKENS:
        if tok==last or last.endswith(" "+tok) or last==tok:
            return land
    for tok,land in COUNTRY_TOKENS:
        if tok in a:
            return land
    # Luxembourg postal "L-xxxx"
    if " l-" in (" "+a) and "luxemb" in a:
        return "Luxemburg"
    return None

LAND_ALIAS = {
 "deutschland":"Deutschland","germany":"Deutschland","de":"Deutschland",
 "schweiz":"Schweiz","switzerland":"Schweiz","ch":"Schweiz",
 "belgien":"Belgien","belgium":"Belgien","be":"Belgien",
 "niederlande":"Niederlande","netherlands":"Niederlande","nl":"Niederlande",
 "frankreich":"Frankreich","france":"Frankreich","fr":"Frankreich",
 "vereinigtes königreich":"Vereinigtes Königreich","vereinigtes koenigreich":"Vereinigtes Königreich",
 "united kingdom":"Vereinigtes Königreich","uk":"Vereinigtes Königreich","gb":"Vereinigtes Königreich",
 "luxemburg":"Luxemburg","luxembourg":"Luxemburg","lu":"Luxemburg",
 "österreich":"Österreich","oesterreich":"Österreich","austria":"Österreich","at":"Österreich",
 "dänemark":"Dänemark","daenemark":"Dänemark","denmark":"Dänemark","dk":"Dänemark",
 "finnland":"Finnland","finland":"Finnland","fi":"Finnland",
 "norwegen":"Norwegen","norway":"Norwegen","no":"Norwegen",
 "portugal":"Portugal","pt":"Portugal","usa":"USA","us":"USA","japan":"Japan","jp":"Japan",
 "liechtenstein":"Liechtenstein",
}
def norm_land(v):
    if not v: return None
    return LAND_ALIAS.get(v.strip().lower())

def is_real_url(u):
    return isinstance(u,str) and (u.startswith("http://") or u.startswith("https://"))

PLACEHOLDER_HINTS = {"processed","archive","processed+archive","processed+web","web","","none"}
def url_quality(u):
    """return ('real',u) | ('placeholder',u) | ('none','')"""
    if u is None: return ("none","")
    if is_real_url(u): return ("real",u)
    return ("placeholder",str(u))

# ---- build node maps ----
node_by_id = {}
for n in nodes:
    nid = n["id"]; node_by_id[nid]=n

# geo_evidence by node_id
geoevi_by_id = {}
for row in geo_evi:
    geoevi_by_id[row.get("node_id")] = row.get("geo_evidence",{})

# donor addresses by bauwerk_id
donor_by_bw = {}
for d in donor_addr:
    donor_by_bw[d["bauwerk_id"]] = d

# reuse_geo: bauteilgruppe chains
bg_chain = {}   # bg_id -> {projekt_id, donor_ids:set, receiver_ids:set}
for bg in reuse_geo.get("nodes",{}).get("bauteilgruppen",[]):
    relp = bg.get("relationships",{})
    bg_chain[bg["id"]] = {
        "projekt_id": relp.get("projekt_id"),
        "donor_ids": set(relp.get("donor_bauwerk_ids") or []),
        "receiver_ids": set(relp.get("receiver_bauwerk_ids") or []),
    }
# projekt->bauwerk pairs from chains (donor & receiver)
proj_bw_donor=set(); proj_bw_recv=set()
for bg_id,c in bg_chain.items():
    p=c["projekt_id"]
    for b in c["donor_ids"]: proj_bw_donor.add((p,b))
    for b in c["receiver_ids"]: proj_bw_recv.add((p,b))

# reuse_geo projekt source urls
proj_geo = {}
for p in reuse_geo.get("nodes",{}).get("projekte",[]):
    proj_geo[p["id"]] = p.get("geo",{})

# donor linked projekte: bauwerk_id -> set(projekt ids)
bw_linked_proj={}
for d in donor_addr:
    lp=d.get("linked_projekte") or ""
    s=set([x for x in str(lp).replace(";",",").split(",") if x.strip()])
    bw_linked_proj[d["bauwerk_id"]]=s

# akteur file: (actor_id, projekt_id) -> source_url ; actor_id -> set(projekt ids)
akteur_link_src={}
akteur_proj={}
for a in akteur_geo.get("akteure",[]):
    aid=a["id"]
    pids=set()
    for loc in a.get("locations",[]):
        if loc.get("role")=="linked_projekt" and loc.get("linked_projekt_id"):
            pid=loc["linked_projekt_id"]
            akteur_link_src[(aid,pid)]=loc.get("source_url")
            pids.add(pid)
    for pr in a.get("projekte",[]):
        pids.add(pr["id"])
    akteur_proj[aid]=pids

def best_node_url(nid):
    """union real url from graph node + geo_evidence + donor file."""
    n=node_by_id.get(nid,{})
    cands=[]
    su=n.get("source_urls")
    if isinstance(su,list): cands+=su
    if n.get("primary_source_url"): cands.append(n["primary_source_url"])
    ge=geoevi_by_id.get(nid,{})
    if ge.get("source_url"): cands.append(ge["source_url"])
    d=donor_by_bw.get(nid,{})
    if d.get("source_url"): cands.append(d["source_url"])
    pg=proj_geo.get(nid,{})
    if pg.get("source_url"): cands.append(pg["source_url"])
    real=[c for c in cands if is_real_url(c)]
    if real: return ("real",real[0])
    ph=[c for c in cands if c]  # non-empty placeholders
    if ph: return ("placeholder",ph[0])
    return ("none","")

def node_address(nid):
    n=node_by_id.get(nid,{})
    if n.get("adresse"): return n["adresse"]
    ge=geoevi_by_id.get(nid,{})
    if ge.get("address"): return ge["address"]
    d=donor_by_bw.get(nid,{})
    if d.get("address"): return d["address"]
    pg=proj_geo.get(nid,{})
    if pg.get("address"): return pg["address"]
    return None

# ---------- ledger rows ----------
rows=[]
def add(claim_id,kind,eid,frm,to,typ,claim,basis,ref,fetched,http,verdict,conf,quote,action,notes):
    rows.append({
        "claim_id":claim_id,"claim_kind":kind,"element_id":eid,"from_id":frm,"to_id":to,
        "rel_type_or_label":typ,"asserted_claim":claim,"basis_type":basis,"basis_ref":ref,
        "fetched":str(fetched).lower(),"http_status":http,"verdict":verdict,"confidence":conf,
        "proof_quote":quote,"proposed_action":action,"agent_id":"09","notes":notes})

def clip(s,n=280):
    if s is None: return ""
    s=str(s).replace("\n"," ").replace("\r"," ")
    return s[:n]

stats={"verdict":{},"by_type":{}}
def bump(v,t):
    stats["verdict"][v]=stats["verdict"].get(v,0)+1
    stats["by_type"].setdefault(t,{}); stats["by_type"][t][v]=stats["by_type"][t].get(v,0)+1

nc=0
# ===== NODES =====
for n in nodes:
    lab=n["labels"][0]; nid=n["id"]; nm=n.get("name")
    nc+=1; cid=f"09-node-{nc:04d}"
    if lab=="Land":
        iso=n.get("iso2")
        if iso:
            add(cid,"node",nid,"","","Land",f"country {nm} ({iso})","logic","ISO-3166 / graph Land node",
                False,"","PROVEN","belegt",f"{nm}={iso}","KEEP","real-world sovereign country")
            bump("PROVEN","Land")
        else:
            add(cid,"node",nid,"","","Land",f"country {nm} (iso2 missing)","logic","graph Land node",
                False,"","PROVEN","teilweise_belegt",f"{nm}; country_iso2=null","FIX_PROPERTY","real country but country_iso2 property missing")
            bump("PROVEN","Land")
    elif lab=="Stadt":
        lat=n.get("lat"); lng=n.get("lng")
        land=STADT_LAND.get(nid)
        if lat is not None and lng is not None:
            add(cid,"node",nid,"","","Stadt",f"city {nm} ({land})","logic","graph geocode + stadt_geocode_cache",
                False,"","PROVEN","belegt",f"{nm} lat={lat},lng={lng}","KEEP","geocoded city centroid present")
            bump("PROVEN","Stadt")
        else:
            add(cid,"node",nid,"","","Stadt",f"city {nm}","logic","graph Stadt node",
                False,"","PARTIAL","teilweise_belegt",f"{nm}; coords missing","FIX_PROPERTY","city node lacks lat/lng")
            bump("PARTIAL","Stadt")
    else:  # Projekt or Bauwerk
        addr=node_address(nid)
        q,u=best_node_url(nid)
        if q=="real":
            add(cid,"node",nid,"","",lab,f"{lab} '{nm}' at {clip(addr,120)}","dossier",u,
                False,"",("PROVEN" if addr else "PARTIAL"),"belegt",clip((addr or "")+" | src "+u,260),"KEEP",
                "address+real source on file (geo extract); existence corroborated, source not re-fetched")
            bump("PROVEN" if addr else "PARTIAL",lab)
        elif q=="placeholder":
            add(cid,"node",nid,"","",lab,f"{lab} '{nm}' at {clip(addr,120)}","dossier",u,
                False,"","MISSING_EVIDENCE","unbelegt",clip("addr="+(addr or "?")+" | source placeholder='"+u+"'",260),"RESOURCE",
                "geo address rests on placeholder source (processed/archive/etc.), not a real URL")
            bump("MISSING_EVIDENCE",lab)
        else:
            add(cid,"node",nid,"","",lab,f"{lab} '{nm}'","dossier","",
                False,"","MISSING_EVIDENCE","unbelegt",clip("addr="+(addr or "none")+"; no source url",260),"RESOURCE",
                "no real or placeholder source url found for node/address")
            bump("MISSING_EVIDENCE",lab)

# ===== build per-from_id city/country sets from LIEGT rels for cross-check =====
from collections import defaultdict
node_land_targets=defaultdict(set)   # from_id -> set(land_name)
for r in lil:
    node_land_targets[r["from_id"]].add(r["land_name"])
node_city_targets=defaultdict(set)
for r in lis:
    node_city_targets[r["from_id"]].add(r["stadt_id"])

# ===== LIEGT_IN_LAND =====
rc=0
for r in lil:
    rc+=1; cid=f"09-lil-{rc:04d}"
    frm=r["from_id"]; land=r["land_name"]; eid=r["eid"]; flab=r["from_label"]
    addr=r.get("from_adresse") or node_address(frm)
    detected=None; basis_note=""
    if flab=="Stadt":
        detected=STADT_LAND.get(frm); basis_note="city geography"
    if not detected and addr:
        detected=detect_country(addr); 
        if detected: basis_note="address country"
    # fallback via city -> land (node has LIEGT_IN_STADT)
    if not detected:
        for sid in node_city_targets.get(frm,()):
            cl=STADT_LAND.get(sid)
            if cl: detected=cl; basis_note="linked city geography"; break
    # fallback via akteur.land
    if not detected:
        nl=norm_land(r.get("from_land"))
        if nl: detected=nl; basis_note="node.land property"
    claim=f"{flab} {frm} liegt in {land}"
    if detected and detected==land:
        add(cid,"rel",eid,frm,r["land_id"],"LIEGT_IN_LAND",claim,"logic",
            basis_note,False,"","PROVEN","belegt",clip(basis_note+" => "+land+" | "+(addr or frm),260),"KEEP","")
        bump("PROVEN","LIEGT_IN_LAND")
    elif detected and detected!=land:
        add(cid,"rel",eid,frm,r["land_id"],"LIEGT_IN_LAND",claim,"logic",
            "country mismatch",False,"","CONTRADICTION","widerlegt",clip(basis_note+" implies "+detected+" but edge says "+land+" | addr="+(addr or '?'),260),"ESCALATE_HUMAN","geo country contradiction")
        bump("CONTRADICTION","LIEGT_IN_LAND")
    else:
        note=("Akteur/org node has no address or land property; home country not confirmable from geo files" if flab in ("Akteur","Software","Programm","Materialdepot")
              else "node has address but country token not parsed: "+(addr or 'none'))
        add(cid,"rel",eid,frm,r["land_id"],"LIEGT_IN_LAND",claim,"logic",
            "unconfirmed",False,"","PARTIAL","teilweise_belegt",clip("country unconfirmed; addr="+(addr or 'none'),260),"KEEP",note)
        bump("PARTIAL","LIEGT_IN_LAND")

# ===== LIEGT_IN_STADT =====
def city_tokens(name):
    out=set()
    for part in str(name).replace("/",",").split(","):
        p=part.strip()
        if p: out.add(p.lower())
    return out
# benign exonym/native-name acceptances per stadt_id (address substrings that DO confirm the city)
EXONYM_ACCEPT = {
 "stadt_bruessel":["brussels","bruxelles","brussel"],
 "stadt_kopenhagen":["københavn","kobenhavn","copenhagen"],
 "stadt_gladsaxe":["søborg","soborg","gladsaxe"],
 "stadt_wien":["vienna"],
 "stadt_s_hertogenbosch":["den bosch","'s-hertogenbosch","hertogenbosch"],
 "stadt_luxembourg_limpertsberg":["luxembourg","limpertsberg","l-2311"],
 "stadt_liege":["liège","liege","lüttich","luttich"],
}
# primary distinctive token per stadt (for "address names a DIFFERENT known city" detection)
STADT_PRIMARY_TOKEN = {}
# resolve stadt names from graph nodes
stadt_name_by_id={n["id"]:n.get("name") for n in nodes if n["labels"][0]=="Stadt"}
for sid_,nm_ in stadt_name_by_id.items():
    first=str(nm_).replace("/",",").split(",")[0].strip().lower()
    if len(first)>3:
        STADT_PRIMARY_TOKEN[first]=sid_
# explicit confirmed wrong-city overrides (address city is a distinct place not modelled as its own Stadt token)
CONTRA_OVERRIDE = {
 "bw_alte_kade_tiel":"address is in Tiel (Gelderland), not Utrecht",
 "bw_kerenzerbergtunnel":"address is Kerenzerberg/Glarus, not Zürich",
}
rc=0
for r in lis:
    rc+=1; cid=f"09-lis-{rc:04d}"
    frm=r["from_id"]; sid=r["stadt_id"]; sname=r["stadt_name"]; eid=r["eid"]
    addr=r.get("from_adresse") or node_address(frm)
    al=(addr or "").lower()
    toks=[t for t in city_tokens(sname) if len(t)>2]
    matched=any(t in al for t in toks)
    if not matched and sid in EXONYM_ACCEPT:
        matched=any(x in al for x in EXONYM_ACCEPT[sid])
    city_land=STADT_LAND.get(sid)
    node_lands=node_land_targets.get(frm,set())
    land_conflict = city_land and node_lands and (city_land not in node_lands)
    # does address name a DIFFERENT known Stadt?
    other_city=None
    if addr and not matched:
        for tok,osid in STADT_PRIMARY_TOKEN.items():
            if osid!=sid and tok in al:
                other_city=(tok,osid); break
    claim=f"{r['from_label']} {frm} liegt in Stadt {sname}"
    if land_conflict:
        add(cid,"rel",eid,frm,sid,"LIEGT_IN_STADT",claim,"logic","city-country vs node-country mismatch",
            False,"","CONTRADICTION","widerlegt",clip("city "+sname+" is in "+city_land+" but node LIEGT_IN_LAND="+",".join(node_lands),260),"ESCALATE_HUMAN","city/country inconsistency")
        bump("CONTRADICTION","LIEGT_IN_STADT")
    elif matched:
        add(cid,"rel",eid,frm,sid,"LIEGT_IN_STADT",claim,"logic","address names city",
            False,"","PROVEN","belegt",clip("address confirms '"+sname+"': "+(addr or ''),260),"KEEP","")
        bump("PROVEN","LIEGT_IN_STADT")
    elif other_city:
        add(cid,"rel",eid,frm,sid,"LIEGT_IN_STADT",claim,"logic","address names a different known city",
            False,"","CONTRADICTION","widerlegt",clip("edge says "+sname+" but address names '"+other_city[0]+"' ("+other_city[1]+"): "+addr,260),"ESCALATE_HUMAN","address city != linked Stadt; a more correct Stadt node exists")
        bump("CONTRADICTION","LIEGT_IN_STADT")
    elif frm in CONTRA_OVERRIDE:
        add(cid,"rel",eid,frm,sid,"LIEGT_IN_STADT",claim,"logic","manual geo check",
            False,"","CONTRADICTION","widerlegt",clip(CONTRA_OVERRIDE[frm]+" | addr: "+(addr or ''),260),"ESCALATE_HUMAN","address city != linked Stadt")
        bump("CONTRADICTION","LIEGT_IN_STADT")
    elif addr:
        add(cid,"rel",eid,frm,sid,"LIEGT_IN_STADT",claim,"logic","address present, city token not found",
            False,"","PARTIAL","teilweise_belegt",clip("city '"+sname+"' not literally in addr: "+addr,260),"KEEP","city name variant/district; benign")
        bump("PARTIAL","LIEGT_IN_STADT")
    else:
        add(cid,"rel",eid,frm,sid,"LIEGT_IN_STADT",claim,"logic","no address",
            False,"","PARTIAL","teilweise_belegt","no address on node to confirm city","KEEP","")
        bump("PARTIAL","LIEGT_IN_STADT")

# ===== general rels: BETEILIGT_AN, AUS_SPENDER, IN_EMPFANGSOBJEKT, HAT_BAUWERK, NUTZT_BAUWERK =====
rc=0
for r in rels:
    t=r["t"]
    if t in ("LIEGT_IN_LAND","LIEGT_IN_STADT"): continue
    rc+=1; cid=f"09-{t.lower()}-{rc:04d}"
    eid=r["eid"]; frm=r["from_id"]; to=r["to_id"]
    fl=(r["fl"] or [""])[0]; tl=(r["tl"] or [""])[0]
    evurl=r.get("evidence_url"); evq=r.get("evidence_quote"); ck=r.get("connection_kind")
    rr=r.get("review_run"); role=r.get("role")
    if t=="BETEILIGT_AN":
        if tl=="Projekt":
            src=evurl if is_real_url(evurl) else akteur_link_src.get((frm,to))
            claim=f"Akteur {frm} beteiligt an Projekt {to}"
            if is_real_url(src):
                add(cid,"rel",eid,frm,to,t,claim,"dossier",src,False,"","PROVEN","belegt",
                    clip("akteur_typ_projekt_geo links "+frm+"->"+to+" src="+src,260),"KEEP","corroborated by project source on file; not re-fetched")
                bump("PROVEN",t)
            elif (frm,to) in akteur_link_src or to in akteur_proj.get(frm,set()):
                add(cid,"rel",eid,frm,to,t,claim,"dossier","akteur_typ_projekt_geo.json",False,"","PARTIAL","teilweise_belegt",
                    clip("link present in dossier but source placeholder/empty='"+str(akteur_link_src.get((frm,to)))+"'",260),"RESOURCE","participation link present but unsourced")
                bump("PARTIAL",t)
            else:
                add(cid,"rel",eid,frm,to,t,claim,"dossier","",False,"","MISSING_EVIDENCE","unbelegt","actor-project link not in geo dossier and no evidence_url","RESOURCE","")
                bump("MISSING_EVIDENCE",t)
        elif tl=="Bauteilgruppe":
            claim=f"Akteur {frm} beteiligt an Bauteilgruppe {to} (ck={ck})"
            if ck in ("reuse_supply_or_material_hub_candidate","planning_actor_component_involvement"):
                add(cid,"rel",eid,frm,to,t,claim,"logic","connection_kind inference",False,"","PARTIAL","teilweise_belegt",
                    clip("inferred participation via "+str(ck)+"; shared-material/candidate, no evidence_url",260),"RELABEL","candidate/inferred edge - downgrade or keep as candidate, not proven participation")
                bump("PARTIAL",t)
            elif is_real_url(evurl):
                add(cid,"rel",eid,frm,to,t,claim,"web",evurl,False,"","PROVEN","belegt",clip(evq or "",260),"KEEP","")
                bump("PROVEN",t)
            else:
                add(cid,"rel",eid,frm,to,t,claim,"logic","none",False,"","MISSING_EVIDENCE","unbelegt","actor-bauteilgruppe edge without connection_kind or evidence","RESOURCE","")
                bump("MISSING_EVIDENCE",t)
        elif tl=="Programm":
            claim=f"Akteur {frm} beteiligt an Programm {to}"
            if is_real_url(evurl):
                add(cid,"rel",eid,frm,to,t,claim,"web",evurl,False,"","PROVEN","belegt",clip(evq or "",260),"KEEP","evidence_url on edge; not re-fetched")
                bump("PROVEN",t)
            else:
                add(cid,"rel",eid,frm,to,t,claim,"logic","none",False,"","MISSING_EVIDENCE","unbelegt","program participation without evidence_url","RESOURCE","")
                bump("MISSING_EVIDENCE",t)
        elif tl=="Stadt" or fl=="Stadt":
            # Stadt -> Projekt geographic participation
            paddr=node_address(to)
            claim=f"Stadt {frm} beteiligt an Projekt {to}"
            add(cid,"rel",eid,frm,to,t,claim,"logic","geographic",False,"","PARTIAL","teilweise_belegt",
                clip("city-as-participant edge; project addr="+(paddr or '?'),260),"ESCALATE_HUMAN","Stadt as BETEILIGT_AN actor is unusual modelling")
            bump("PARTIAL",t)
        else:  # Akteur->Akteur / Akteur->Software
            claim=f"{fl} {frm} beteiligt an {tl} {to}"
            if is_real_url(evurl):
                add(cid,"rel",eid,frm,to,t,claim,"web",evurl,False,"","PROVEN","belegt",clip(evq or "",260),"KEEP","")
                bump("PROVEN",t)
            else:
                add(cid,"rel",eid,frm,to,t,claim,"logic","none",False,"","MISSING_EVIDENCE","unbelegt",clip(tl+"-target BETEILIGT_AN without evidence",200),"ESCALATE_HUMAN","unusual BETEILIGT_AN target; verify modelling")
                bump("MISSING_EVIDENCE",t)
    elif t=="HAT_BAUWERK":
        claim=f"Projekt {frm} HAT_BAUWERK {to} (role={role})"
        if is_real_url(evurl):
            add(cid,"rel",eid,frm,to,t,claim,"web",evurl,False,"","PROVEN","belegt",clip(evq or "",260),"KEEP","web-evidenced donor link; not re-fetched")
            bump("PROVEN",t)
        elif tl=="Materialdepot":
            add(cid,"rel",eid,frm,to,t,claim,"logic","materialdepot target",False,"","PARTIAL","teilweise_belegt",
                "projekt->Materialdepot; depot has 0 sources (see Agent 10)","ESCALATE_HUMAN","unsourced Materialdepot endpoint")
            bump("PARTIAL",t)
        else:
            in_chain = ((frm,to) in proj_bw_donor) or ((frm,to) in proj_bw_recv) or (frm in bw_linked_proj.get(to,set()))
            if in_chain:
                add(cid,"rel",eid,frm,to,t,claim,"dossier","reuse_geo_graph donor/receiver chain",False,"","PROVEN","belegt",
                    clip("projekt-bauwerk pair present in geo donor/receiver chain ("+(role or 'n/a')+")",260),"KEEP","")
                bump("PROVEN",t)
            else:
                add(cid,"rel",eid,frm,to,t,claim,"dossier","reuse_geo_graph",False,"","PARTIAL","teilweise_belegt",
                    "projekt-bauwerk link not found in geo donor/receiver chain","KEEP","structurally valid; not corroborated in geo chain export")
                bump("PARTIAL",t)
    elif t=="AUS_SPENDER":
        claim=f"Bauteilgruppe {frm} AUS_SPENDER {to}"
        c=bg_chain.get(frm,{})
        if tl=="Materialdepot":
            add(cid,"rel",eid,frm,to,t,claim,"logic","materialdepot donor",False,"","PARTIAL","teilweise_belegt",
                "donor is Materialdepot (0 sources, see Agent 10)","ESCALATE_HUMAN","unsourced depot donor")
            bump("PARTIAL",t)
        elif to in c.get("donor_ids",set()):
            add(cid,"rel",eid,frm,to,t,claim,"dossier","reuse_geo_graph donor chain",False,"","PROVEN","belegt",
                clip("bg donor_bauwerk_ids contains "+to,260),"KEEP","")
            bump("PROVEN",t)
        else:
            add(cid,"rel",eid,frm,to,t,claim,"dossier","reuse_geo_graph",False,"","PARTIAL","teilweise_belegt",
                "donor bauwerk not in bg donor chain export","KEEP","structurally valid; not in geo chain")
            bump("PARTIAL",t)
    elif t=="IN_EMPFANGSOBJEKT":
        claim=f"Bauteilgruppe {frm} IN_EMPFANGSOBJEKT {to}"
        c=bg_chain.get(frm,{})
        if tl=="Materialdepot":
            add(cid,"rel",eid,frm,to,t,claim,"logic","materialdepot receiver",False,"","PARTIAL","teilweise_belegt",
                "receiver is Materialdepot (0 sources, see Agent 10)","ESCALATE_HUMAN","unsourced depot receiver")
            bump("PARTIAL",t)
        elif to in c.get("receiver_ids",set()):
            add(cid,"rel",eid,frm,to,t,claim,"dossier","reuse_geo_graph receiver chain",False,"","PROVEN","belegt",
                clip("bg receiver_bauwerk_ids contains "+to,260),"KEEP","")
            bump("PROVEN",t)
        else:
            add(cid,"rel",eid,frm,to,t,claim,"dossier","reuse_geo_graph",False,"","PARTIAL","teilweise_belegt",
                "receiver bauwerk not in bg receiver chain export","KEEP","structurally valid; not in geo chain")
            bump("PARTIAL",t)
    elif t=="NUTZT_BAUWERK":
        claim=f"{fl} {frm} NUTZT_BAUWERK {to}"
        if is_real_url(evurl):
            add(cid,"rel",eid,frm,to,t,claim,"web",evurl,False,"","PROVEN","belegt",clip(evq or "",260),"KEEP","rotor_dc bubble; web evidence_url, fetch to confirm")
            bump("PROVEN",t)
        else:
            add(cid,"rel",eid,frm,to,t,claim,"logic","none",False,"","MISSING_EVIDENCE","unbelegt","no evidence","RESOURCE","")
            bump("MISSING_EVIDENCE",t)

# ---- apply live WebFetch confirmations (2026-06-06, all HTTP 200) ----
WEB_CONFIRMED = {
 ("NUTZT_BAUWERK","rotordc","bw_generale_de_banque_brussels"):(
   "https://rotordc.com/blog/salvaging-by-rotordc-3/generale-banks-hq-brussels-72",
   "over 230 tonnes of finishing materials were salvaged, including ceilings, granite floors, doors, hardware, decorations and more besides. This project kick-started Rotor DC"),
 ("BETEILIGT_AN","baubuero_in_situ","p_k118_kopfbau_halle_118_winterthur"):(
   "https://zirkular.net/en/project/building-k-118/",
   "the projects K.118 in Winterthur and ELYS in Basel, proved to be pioneering projects of circular building ... architecture: baubüro in situ"),
 ("BETEILIGT_AN","zirkular","p_k118_kopfbau_halle_118_winterthur"):(
   "https://zirkular.net/en/project/building-k-118/",
   "They received a lot of attention and were the trigger for the foundation of Zirkular by the involved planners (K.118 Winterthur)"),
 ("BETEILIGT_AN","immobel","p_oxy_centre_monnaie"):(
   "https://rotordb.org/en/projects/oxy-centre-monnaie",
   "the Centre Monnaie, which was acquired by property developers Whitewood and Immobel. The duo planned a €150 million renovation"),
 ("BETEILIGT_AN","whitewood","p_oxy_centre_monnaie"):(
   "https://rotordb.org/en/projects/oxy-centre-monnaie",
   "the Centre Monnaie, which was acquired by property developers Whitewood and Immobel. The duo planned a €150 million renovation"),
 ("BETEILIGT_AN","Rotor","p_oxy_centre_monnaie"):(
   "https://rotordb.org/en/projects/oxy-centre-monnaie",
   "Rotor was asked to join the project team to help define a circular approach to the project, integrate reuse principles into the design"),
 ("BETEILIGT_AN","opalis","prog_preuse"):(
   "https://opalis.eu/en/about",
   "Between 2024 and 2027, Opalis is maintained and updated by Rotor and Bellastock as part of the Interreg NWE programme for the PREUSE-project"),
 ("BETEILIGT_AN","brussels_environment","prog_preuse"):(
   "https://opalis.eu/en/about",
   "Opalis is maintained and updated by Rotor and Bellastock ... for the PREUSE-project. ... Rotor by Brussels Environment as part of the Renolution strategy"),
}
wc=0
for r in rows:
    key=(r["rel_type_or_label"],r["from_id"],r["to_id"])
    if key in WEB_CONFIRMED:
        url,quote=WEB_CONFIRMED[key]
        r["fetched"]="true"; r["http_status"]="200"; r["basis_type"]="web"; r["basis_ref"]=url
        r["verdict"]="PROVEN"; r["confidence"]="belegt"; r["proof_quote"]=clip(quote,300)
        r["notes"]="live-fetched 2026-06-06; both endpoints named on page"
        wc+=1
print("WEB_CONFIRMED applied:",wc)

# ---- write ledger ----
os.makedirs(os.path.dirname(LEDGER),exist_ok=True)
cols=["claim_id","claim_kind","element_id","from_id","to_id","rel_type_or_label","asserted_claim",
      "basis_type","basis_ref","fetched","http_status","verdict","confidence","proof_quote",
      "proposed_action","agent_id","notes"]
with io.open(LEDGER,"w",encoding="utf-8",newline="") as f:
    w=csv.DictWriter(f,fieldnames=cols,quoting=csv.QUOTE_MINIMAL)
    w.writeheader()
    for r in rows: w.writerow(r)

print("TOTAL ROWS:",len(rows))
print("VERDICTS:",json.dumps(stats["verdict"],ensure_ascii=False,indent=0))
print("BY TYPE:")
for t,d in sorted(stats["by_type"].items()):
    print(" ",t,json.dumps(d,ensure_ascii=False))
# dump contradictions & missing for report
def sel(pred,lim=60):
    return [ (r["claim_id"],r["rel_type_or_label"],r["from_id"],r["to_id"],r["verdict"],r["proof_quote"],r["notes"]) for r in rows if pred(r)][:lim]
import pprint
con=sel(lambda r:r["verdict"]=="CONTRADICTION")
print("CONTRADICTIONS:",len(con))
for c in con: print("  C:",c)
print("STADT_NO_COORDS:",[r["from_id"] for r in rows if r["rel_type_or_label"]=="Stadt" and r["verdict"]=="PARTIAL"])
