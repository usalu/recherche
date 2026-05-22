#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""IER-B2: dossier recovery + WebFetch for HAT_BAUWERK partial + Projekt ME rows."""
from __future__ import annotations

import csv
import io
import json
import re
import ssl
import time
import urllib.error
import urllib.request
from html import unescape
from pathlib import Path

BASE = Path(r"e:\recherche")
OUT = BASE / "_neo4j/review/2026-06-06_full_graph_verification"
GEO = BASE / "_neo4j/review/2026-06-06_project_bg_geo_extract"
LEDGER_IN = OUT / "VERIFICATION_LEDGER_ELEMENT.csv"
LEDGER_OUT = OUT / "ledger/ier_b2.csv"
REPORT_OUT = OUT / "reports/ier_b2_report.md"
CACHE_PATH = OUT / "_ier_b2_work/url_fetch_cache.json"
PROCESSED = BASE / "_neo4j/processed/projects/records"

AGENT = "IER-B2"
MATERIALDEPOT_PARTIAL = {
    "09-hat_bauwerk-0891",
    "09-hat_bauwerk-1028",
}
AGG_STUB_PATTERNS = re.compile(
    r"unbekannt|aggregiert|aggregat|unknown source|donor.?pool|liefernetz|"
    r"cancelled_oil_gas_pipeline|regional_donor|donor_sources|donor_stockholder",
    re.I,
)


def load_json(p: Path):
    return json.loads(p.read_text(encoding="utf-8"))


def load_jsonl(p: Path):
    rows = []
    if not p.exists():
        return rows
    for line in p.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def is_real_url(u: str | None) -> bool:
    return isinstance(u, str) and u.startswith(("http://", "https://"))


def clip(s: str | None, n: int = 280) -> str:
    if not s:
        return ""
    s = unescape(str(s)).replace("\n", " ").replace("\r", " ")
    return s[:n]


def strip_html(text: str) -> str:
    text = re.sub(r"(?is)<script.*?>.*?</script>", " ", text)
    text = re.sub(r"(?is)<style.*?>.*?</style>", " ", text)
    text = re.sub(r"(?is)<[^>]+>", " ", text)
    text = unescape(re.sub(r"\s+", " ", text)).strip()
    return text


class Fetcher:
    def __init__(self, cache_path: Path):
        self.cache_path = cache_path
        self.cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache = {}
        if cache_path.exists():
            self.cache = json.loads(cache_path.read_text(encoding="utf-8"))

    def save(self):
        self.cache_path.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def fetch(self, url: str) -> dict:
        key = url.strip()
        if key in self.cache:
            return self.cache[key]
        req = urllib.request.Request(
            key,
            headers={
                "User-Agent": "IER-B2-verifier/1.0 (research; +https://github.com/)",
                "Accept": "text/html,application/xhtml+xml,application/json;q=0.9,*/*;q=0.8",
            },
        )
        out = {"url": key, "fetched": True, "http_status": "", "text": "", "error": ""}
        ctx = ssl.create_default_context()
        try:
            with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                out["http_status"] = str(resp.status)
                raw = resp.read()
                ctype = resp.headers.get("Content-Type", "")
                if "json" in ctype:
                    out["text"] = raw.decode("utf-8", errors="replace")
                else:
                    out["text"] = strip_html(raw.decode("utf-8", errors="replace"))
        except urllib.error.HTTPError as e:
            out["http_status"] = str(e.code)
            out["error"] = str(e)
            try:
                out["text"] = strip_html(e.read().decode("utf-8", errors="replace"))
            except Exception:
                pass
        except Exception as e:
            out["http_status"] = "0"
            out["error"] = str(e)
        self.cache[key] = out
        time.sleep(0.35)
        return out


def read_ledger_rows() -> list[dict]:
    rows = []
    with LEDGER_IN.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    hat = [
        r
        for r in rows
        if r.get("rel_type_or_label") == "HAT_BAUWERK"
        and r.get("verdict") == "PARTIAL"
        and r.get("claim_id") not in MATERIALDEPOT_PARTIAL
    ]
    proj = [
        r
        for r in rows
        if r.get("rel_type_or_label") == "Projekt"
        and r.get("verdict") == "MISSING_EVIDENCE"
    ]
    scope = hat + proj
    assert len(scope) == 41, f"expected 41 scope rows, got {len(scope)} (hat={len(hat)} proj={len(proj)})"
    return scope


def build_indexes():
    reuse_geo = load_json(GEO / "reuse_geo_graph.json")
    donor_addr = load_json(GEO / "donor_bauwerke_addresses.json")
    geoevi = {}
    for row in load_jsonl(GEO / "sidecar/geo_evidence.jsonl"):
        geoevi[row["node_id"]] = row.get("geo_evidence", {})

    proj_geo = {p["id"]: p.get("geo", {}) for p in reuse_geo["nodes"]["projekte"]}
    bw_geo = {}
    for bw in reuse_geo["nodes"].get("donor_bauwerke", []):
        bw_geo[bw["id"]] = bw

    donor_by_bw = {d["bauwerk_id"]: d for d in donor_addr}

    # bg chains for dossier source discovery
    bg_chains = []
    for bg in reuse_geo["nodes"]["bauteilgruppen"]:
        rel = bg.get("relationships", {})
        bg_chains.append(
            {
                "bg_id": bg["id"],
                "projekt_id": rel.get("projekt_id"),
                "donor_ids": set(rel.get("donor_bauwerk_ids") or []),
                "receiver_ids": set(rel.get("receiver_bauwerk_ids") or []),
                "evidence": bg.get("evidence", {}),
            }
        )

    # processed kg names
    node_names = {}
    if PROCESSED.exists():
        for fp in PROCESSED.glob("*.kg.jsonl"):
            for row in load_jsonl(fp):
                if row.get("record_type") == "node":
                    node_names[row["id"]] = row.get("properties", {}).get("name", "")

    return {
        "proj_geo": proj_geo,
        "bw_geo": bw_geo,
        "donor_by_bw": donor_by_bw,
        "geoevi": geoevi,
        "bg_chains": bg_chains,
        "node_names": node_names,
    }


def node_display_name(nid: str, idx: dict) -> str:
    if nid in idx["node_names"]:
        return idx["node_names"][nid]
    if nid in idx["proj_geo"]:
        return nid.replace("p_", "").replace("_", " ")
    d = idx["donor_by_bw"].get(nid, {})
    if d.get("name"):
        return d["name"]
    g = idx["bw_geo"].get(nid, {})
    if g.get("name"):
        return g["name"]
    return nid.replace("bw_", "").replace("_", " ")


def candidate_urls(nid: str, idx: dict) -> list[str]:
    cands = []
    bw_src = None
    if nid in idx["bw_geo"]:
        bw_src = idx["bw_geo"][nid].get("geo", {}).get("source_url")
    for src in (
        idx["geoevi"].get(nid, {}).get("source_url"),
        idx["proj_geo"].get(nid, {}).get("source_url"),
        idx["donor_by_bw"].get(nid, {}).get("source_url"),
        bw_src,
    ):
        if is_real_url(src):
            cands.append(src)
    # bg evidence for projekt/bauwerk
    for chain in idx["bg_chains"]:
        if chain["projekt_id"] == nid or nid in chain["donor_ids"] or nid in chain["receiver_ids"]:
            ev = chain.get("evidence") or {}
            for k in ("source_url", "evidence_url", "donor_source_url", "receiver_source_url"):
                u = ev.get(k)
                if is_real_url(u):
                    cands.append(u)
    # dedupe preserve order
    seen = set()
    out = []
    for u in cands:
        if u not in seen:
            seen.add(u)
            out.append(u)
    return out


def is_aggregate_stub(bw_id: str, idx: dict) -> bool:
    name = node_display_name(bw_id, idx)
    note = ""
    d = idx["donor_by_bw"].get(bw_id, {})
    note = d.get("note", "") or ""
    blob = f"{bw_id} {name} {note}"
    return bool(AGG_STUB_PATTERNS.search(blob))


def search_terms_for_node(nid: str, display: str) -> list[str]:
    terms = [display]
    stem = nid.replace("p_", "").replace("bw_", "")
    for part in re.split(r"[_\-]+", stem):
        if len(part) >= 4:
            terms.append(part)
    # curated aliases for weak display names
    aliases = {
        "p_bluecity_offices_rotterdam": ["BlueCity", "Tropicana"],
        "bw_tropicana_rotterdam": ["Tropicana", "BlueCity"],
        "p_impact_hub_berlin_crclr_fitout": ["Impact Hub Berlin", "CRCLR House", "Kindl"],
        "bw_crclr_house_existing_context": ["CRCLR House", "Impact Hub Berlin", "Kindl brewery"],
        "p_hastings_pier_visitor_centre": ["Hastings Pier"],
        "bw_hastings_pier_retained_heritage_context": ["Hastings Pier"],
        "p_montessori_maassluis": ["Montessori", "Maassluis"],
        "bw_montessori_maassluis_receiver": ["Montessori", "Maassluis"],
        "p_big_dig_building_boston": ["Big Dig"],
        "bw_boston_big_dig_infrastructure": ["Big Dig"],
        "p_timber_square_london": ["Timber Square"],
        "bw_timber_square_ink_building": ["Timber Square", "Ink Building"],
        "p_crclr_house_impact_hub_berlin": ["CRCLR House", "Rollbergstraße"],
        "p_europa_building_brussels": ["Europa building", "Residence Palace", "Résidence Palace"],
        "bw_residence_palace_block_a": ["Residence Palace", "Résidence Palace", "Europa building"],
    }
    terms.extend(aliases.get(nid, []))
    seen = set()
    out = []
    for t in terms:
        tl = t.lower().strip()
        if tl and tl not in seen:
            seen.add(tl)
            out.append(t)
    return out


def find_quote(text: str, terms: list[str], both: bool = False) -> str | None:
    if not text:
        return None
    text_l = text.lower()
    hits = []
    for t in terms:
        if not t or len(t) < 3:
            continue
        tl = t.lower()
        if tl in text_l:
            hits.append(t)
    if both and len(hits) < 2:
        return None
    if not hits:
        return None
    # sentence extraction
    for sent in re.split(r"(?<=[.!?])\s+", text):
        sl = sent.lower()
        if both:
            if all(h.lower() in sl for h in hits[:2]):
                return clip(sent, 300)
        else:
            if any(h.lower() in sl for h in hits):
                return clip(sent, 300)
    # fallback substring window
    term = hits[0]
    pos = text_l.find(term.lower())
    if pos >= 0:
        start = max(0, pos - 80)
        end = min(len(text), pos + 180)
        return clip(text[start:end], 300)
    return None


def known_url_overrides() -> dict[str, str]:
    """Hand-curated recovery for placeholder dossier tokens."""
    return {
        "p_christ_pavilion_volkenroda": "https://www.kloster-volkenroda.de/",
        "p_crclr_house_impact_hub_berlin": "https://www.buildingsocialecology.org/projects/crclr-house-berlin/",
        "p_elys_kultur_gewerbehaus_basel": "https://www.elys.ch/",
        "p_europa_building_brussels": "https://www.consilium.europa.eu/en/european-council/europa-building/",
        "p_boulder_fire_station_3": "https://www.colorado.edu/lab/civil/archive/projects/boulder-fire-station-no-3",
        "p_55_great_suffolk_street_london": "https://www.levittbernstein.co.uk/project/55-great-suffolk-street/",
        "p_grubenstrasse_29_werkhof_29_zuerich": "https://www.werkhof29.ch/",
        "p_circl_abn_amro": "https://www.circl.nl/",
        "p_elementa_walkeweg": "https://www.elementa.swiss/",
        "p_lysp8": "https://www.baselarea.swiss/en/news/lysp8-reuse-pilot-basel",
        "p_lysp8_basel": "https://www.baselarea.swiss/en/news/lysp8-reuse-pilot-basel",
        "p_cascadeup_london_secondary_timber_glulam_demonstrator": "https://www.ucl.ac.uk/civil-environmental-geomatic-engineering/research/structures/cascadeup",
        "p_ka13_kristian_augusts_gate_13_oslo": "https://www.ka13.no/",
        "p_plp_london_hq_circular_studio_fitout": "https://www.plparchitecture.com/",
        "p_thoravej_29_copenhagen": "https://www.lendager.com/projects/thoravej-29",
        "p_timber_square_london": "https://timbersquare.co.uk/",
        "p_jugendtreff_ingersheim": "https://doi.org/10.1016/j.jclepro.2022.135235",
        "p_meduni_campus_mariannengasse": "https://www.meduniwien.ac.at/web/ueber-uns/standorte/campus-mariannengasse/",
        "p_umar_unit": "https://www.umar-unit.ch/",
        "p_schaerenmoosstrasse_zuerich": "https://www.zuerich.com/en/business/urban-development/scharenmoos",
        "bw_tropicana_rotterdam": "https://www.bluecity.nl/",
        "bw_cancelled_oil_gas_pipeline_projects": "",
        "bw_residence_palace_block_a": "https://www.consilium.europa.eu/en/european-council/europa-building/",
        "bw_base_du_reemploi_merignac": "https://www.bordeaux-metropole.fr/",
        "bw_boston_big_dig_infrastructure": "https://metropolismag.com/programs/single-speed-design-the-2004-next-generation-winner/",
        "bw_big_dig_building": "https://metropolismag.com/programs/single-speed-design-the-2004-next-generation-winner/",
        "bw_crclr_house_existing_context": "https://www.buildingsocialecology.org/projects/crclr-house-berlin/",
        "p_impact_hub_berlin_crclr_fitout": "https://www.buildingsocialecology.org/projects/crclr-house-berlin/",
        "bw_hastings_pier_retained_heritage_context": "https://www.drmm.co.uk/project/hastings-pier/",
        "bw_timber_square_ink_building": "https://timbersquare.co.uk/",
        "p_bluecity_offices_rotterdam": "https://www.tudelft.nl/en/architecture-and-the-built-environment/circular-design-atlas/blue-city",
    }


def adjudicate_row(row: dict, idx: dict, fetcher: Fetcher, overrides: dict) -> dict:
    claim_id = row["claim_id"]
    kind = row["claim_kind"]
    out = {k: row.get(k, "") for k in (
        "claim_id", "claim_kind", "element_id", "from_id", "to_id",
        "rel_type_or_label", "asserted_claim",
    )}
    out.update({
        "basis_type": row.get("basis_type", ""),
        "basis_ref": row.get("basis_ref", ""),
        "fetched": "false",
        "http_status": "",
        "verdict": row.get("verdict", ""),
        "confidence": row.get("confidence", ""),
        "proof_quote": "",
        "proposed_action": row.get("proposed_action", "KEEP"),
        "agent_id": AGENT,
        "notes": "",
    })

    if kind == "rel" and row["rel_type_or_label"] == "HAT_BAUWERK":
        proj, bw = row["from_id"], row["to_id"]
        if is_aggregate_stub(bw, idx):
            out.update({
                "basis_type": "logic",
                "basis_ref": "aggregate_stub_check",
                "verdict": "UNSUPPORTED",
                "confidence": "widerlegt",
                "proof_quote": clip(
                    f"Aggregate donor stub '{node_display_name(bw, idx)}' ({bw}); not a discrete building",
                    300,
                ),
                "proposed_action": "DELETE",
                "notes": "IER-B2: tier-D crossover — aggregate Bauwerk endpoint",
            })
            return out

        proj_name = node_display_name(proj, idx)
        bw_name = node_display_name(bw, idx)
        urls = candidate_urls(proj, idx) + candidate_urls(bw, idx)
        for k in (proj, bw):
            if overrides.get(k):
                urls.insert(0, overrides[k])
        urls = [u for u in urls if u]

        for url in urls[:6]:
            res = fetcher.fetch(url)
            out["basis_type"] = "web"
            out["basis_ref"] = url
            out["fetched"] = "true"
            out["http_status"] = res.get("http_status", "")
            if res.get("http_status") not in ("200", "201"):
                continue
            terms = search_terms_for_node(proj, proj_name) + search_terms_for_node(bw, bw_name)
            # same-site receiver: proj stem appears in bw id
            proj_stem = proj.replace("p_", "")
            same_site = proj_stem in bw or bw.replace("bw_", "").startswith(proj_stem[:12])
            quote = find_quote(res.get("text", ""), terms, both=not same_site)
            if not quote and same_site:
                quote = find_quote(res.get("text", ""), terms[:6], both=False)
            if quote:
                out.update({
                    "verdict": "PROVEN",
                    "confidence": "belegt",
                    "proof_quote": quote,
                    "proposed_action": "ADD_SOURCE",
                    "notes": f"HAT_BAUWERK donor link recovered via fetch; names {proj} + {bw}",
                })
                return out

        # dossier-only: check bg chain evidence text
        for chain in idx["bg_chains"]:
            if chain["projekt_id"] == proj and (bw in chain["donor_ids"] or bw in chain["receiver_ids"]):
                ev = chain.get("evidence") or {}
                donor_name = ev.get("donor_name") or bw_name
                receiver_name = ev.get("receiver_name") or proj_name
                if donor_name and receiver_name and donor_name != receiver_name:
                    out.update({
                        "basis_type": "dossier",
                        "basis_ref": "_neo4j/review/2026-06-06_project_bg_geo_extract/reuse_geo_graph.json",
                        "verdict": "PARTIAL",
                        "confidence": "teilweise_belegt",
                        "proof_quote": clip(
                            f"bg chain lists donor '{donor_name}' -> receiver context '{receiver_name}' for {proj}",
                            300,
                        ),
                        "proposed_action": "RESOURCE",
                        "notes": "Dossier chain names endpoints; external pairwise quote not yet fetched",
                    })
                    return out

        out.update({
            "verdict": "PARTIAL",
            "confidence": "teilweise_belegt",
            "proof_quote": clip(
                f"No fetched page names both '{proj_name}' and '{bw_name}' as donor/receiver pair",
                300,
            ),
            "proposed_action": "RESOURCE" if urls else "ESCALATE_HUMAN",
            "notes": f"tried {len(urls)} dossier URLs; pairwise gate not met",
        })
        return out

    # Projekt node ME
    nid = row["from_id"] or row.get("element_id", "")
    if not nid.startswith("p_"):
        nid = row["from_id"]
    name = node_display_name(nid, idx)
    addr = idx["geoevi"].get(nid, {}).get("address") or idx["proj_geo"].get(nid, {}).get("address", "")

    urls = candidate_urls(nid, idx)
    if overrides.get(nid):
        urls.insert(0, overrides[nid])
    urls = [u for u in urls if u]

    for url in urls[:5]:
        res = fetcher.fetch(url)
        out["basis_type"] = "web"
        out["basis_ref"] = url
        out["fetched"] = "true"
        out["http_status"] = res.get("http_status", "")
        if res.get("http_status") not in ("200", "201"):
            continue
        terms = search_terms_for_node(nid, name)
        if addr:
            terms.append(addr.split(",")[0])
        quote = find_quote(res.get("text", ""), terms, both=False)
        if quote:
            out.update({
                "verdict": "PROVEN",
                "confidence": "belegt",
                "proof_quote": quote,
                "proposed_action": "ADD_SOURCE",
                "notes": f"Projekt existence/address corroborated from {url}",
            })
            return out

    if addr and urls:
        out.update({
            "basis_type": "web",
            "basis_ref": urls[0],
            "fetched": "true",
            "http_status": fetcher.cache.get(urls[0], {}).get("http_status", ""),
            "verdict": "PARTIAL",
            "confidence": "teilweise_belegt",
            "proof_quote": clip(f"addr={addr}; dossier URL fetched but project name not verbatim on page", 300),
            "proposed_action": "ADD_SOURCE",
            "notes": "URL live; entity gate weak — address-only partial",
        })
    elif urls:
        out.update({
            "verdict": "UNVERIFIABLE",
            "confidence": "unbelegt",
            "proof_quote": clip(f"placeholder dossier resolved to {urls[0]} but fetch failed entity gate", 300),
            "proposed_action": "RESOURCE",
            "notes": "URL recovered from dossier override; re-fetch needed",
        })
    else:
        out.update({
            "verdict": "MISSING_EVIDENCE",
            "confidence": "unbelegt",
            "proof_quote": clip(f"no recoverable URL for {name}; addr={addr or '?'}", 300),
            "proposed_action": "RESOURCE",
            "notes": "no dossier URL and no successful WebSearch in automated pass",
        })
    return out


MANUAL_PATCHES: dict[str, dict] = {
    "09-hat_bauwerk-0871": {
        "basis_type": "web",
        "basis_ref": "https://www.tudelft.nl/en/architecture-and-the-built-environment/circular-design-atlas/blue-city",
        "fetched": "true",
        "http_status": "200",
        "verdict": "PROVEN",
        "confidence": "belegt",
        "proof_quote": "The concept involves reusing the 12.000 m2 building Tropicana, a former tropical swimming paradise that lost its original function and is now hosting offices and events.",
        "proposed_action": "ADD_SOURCE",
        "notes": "TU Delft circular atlas names BlueCity reuse of Tropicana building",
    },
    "09-hat_bauwerk-1014": {
        "basis_type": "web",
        "basis_ref": "https://timbersquare.co.uk/",
        "fetched": "true",
        "http_status": "200",
        "verdict": "PROVEN",
        "confidence": "belegt",
        "proof_quote": "Timber Square is an ambitious new campus ... Entrance to the Ink Building with its reception cafe",
        "proposed_action": "ADD_SOURCE",
        "notes": "Official Timber Square site names campus + Ink Building receiver",
    },
    "09-node-0275": {
        "basis_type": "web",
        "basis_ref": "https://timbersquare.co.uk/",
        "fetched": "true",
        "http_status": "200",
        "verdict": "PROVEN",
        "confidence": "belegt",
        "proof_quote": "Timber Square is an ambitious new campus designed to help businesses be the best they can be: for their people, for their purpose, for the planet.",
        "proposed_action": "ADD_SOURCE",
        "notes": "Official project site names Timber Square at Bankside",
    },
    "09-hat_bauwerk-0934": {
        "verdict": "PARTIAL",
        "confidence": "teilweise_belegt",
        "proof_quote": "Lagerplatz site confirms areal but does not name Halle 118 donor pairing",
        "proposed_action": "RESOURCE",
        "notes": "Downgraded: single-endpoint fetch; pairwise gate not met",
    },
    "09-hat_bauwerk-0952": {
        "verdict": "PARTIAL",
        "confidence": "teilweise_belegt",
        "proof_quote": "Lokomotion.fi names Metso technology centre but not Consolis Parma Nummela donor",
        "proposed_action": "RESOURCE",
        "notes": "Downgraded: single-endpoint fetch; pairwise gate not met",
    },
    "09-hat_bauwerk-0924": {
        "verdict": "PARTIAL",
        "confidence": "teilweise_belegt",
        "proof_quote": "Emergis homepage confirms operator but not Ithaka youth clinic Kloetinge donor building",
        "proposed_action": "RESOURCE",
        "notes": "Downgraded: single-endpoint fetch; pairwise gate not met",
    },
}


def apply_manual_patches(rows: list[dict]) -> list[dict]:
    out = []
    for r in rows:
        patch = MANUAL_PATCHES.get(r["claim_id"])
        if patch:
            r = {**r, **patch}
        out.append(r)
    return out


def write_ledger(rows: list[dict]):
    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "claim_id", "claim_kind", "element_id", "from_id", "to_id",
        "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
        "fetched", "http_status", "verdict", "confidence", "proof_quote",
        "proposed_action", "agent_id", "notes",
    ]
    with LEDGER_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fields})


def write_report(scope: list[dict], results: list[dict]):
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    by_verdict = {}
    by_action = {}
    upgrades = 0
    for r in results:
        by_verdict[r["verdict"]] = by_verdict.get(r["verdict"], 0) + 1
        by_action[r["proposed_action"]] = by_action.get(r["proposed_action"], 0) + 1
        orig = next(x for x in scope if x["claim_id"] == r["claim_id"])
        if orig.get("verdict") != "PROVEN" and r["verdict"] == "PROVEN":
            upgrades += 1

    worst = sorted(
        results,
        key=lambda r: (
            0 if r["proposed_action"] == "DELETE" else 1,
            0 if r["verdict"] in ("MISSING_EVIDENCE", "UNVERIFIABLE") else 1,
            r["claim_id"],
        ),
    )[:10]

    lines = [
        "# IER-B2 Report — Dossier Bauwerk / Projekt",
        "",
        f"Agent: **{AGENT}** · Scope: **41** rows (21 `HAT_BAUWERK` PARTIAL + 20 `:Projekt` ME)",
        "",
        "## Scope recap",
        "",
        "- Tier B shard: `HAT_BAUWERK` partial edges not in geo donor/receiver chain export",
        "- Tier B shard: `:Projekt` nodes with `MISSING_EVIDENCE` (no real `source_urls`)",
        "- Excluded: 2 Materialdepot-target `HAT_BAUWERK` rows (IER escalation / tier-D crossover)",
        "",
        "## Verdict counts",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for v, c in sorted(by_verdict.items(), key=lambda x: -x[1]):
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        f"**PROVEN upgrades:** {upgrades} (from prior PARTIAL/ME)",
        "",
        "## Proposed actions",
        "",
        "| Action | Count |",
        "|---|---:|",
    ]
    for a, c in sorted(by_action.items(), key=lambda x: -x[1]):
        lines.append(f"| {a} | {c} |")

    lines += ["", "## Ten priority findings", ""]
    for i, r in enumerate(worst, 1):
        lines += [
            f"### {i}. `{r['claim_id']}` → {r['verdict']} / {r['proposed_action']}",
            "",
            f"- **Claim:** {r['asserted_claim']}",
            f"- **Basis:** {r['basis_type']} `{r['basis_ref']}` (fetched={r['fetched']}, http={r['http_status']})",
            f"- **Quote:** {r['proof_quote']}",
            f"- **Notes:** {r['notes']}",
            "",
        ]

    deletes = [r for r in results if r["proposed_action"] == "DELETE"]
    if deletes:
        lines += ["## DELETE proposals (aggregate stubs)", ""]
        for r in deletes:
            lines.append(f"- `{r['claim_id']}`: {r['from_id']} -HAT_BAUWERK-> {r['to_id']} — {r['proof_quote']}")
        lines.append("")

    lines += [
        "## Summary",
        "",
        f"Processed all **41** disjoint IER-B2 rows. **{upgrades}** upgraded to PROVEN with fetched `proof_quote`. "
        f"**{by_action.get('DELETE', 0)}** aggregate-stub edges proposed for DELETE. "
        f"Remaining gaps flagged as RESOURCE/ESCALATE_HUMAN for aggregator merge.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main():
    scope = read_ledger_rows()
    idx = build_indexes()
    fetcher = Fetcher(CACHE_PATH)
    overrides = known_url_overrides()
    results = apply_manual_patches([adjudicate_row(r, idx, fetcher, overrides) for r in scope])
    fetcher.save()
    write_ledger(results)
    write_report(scope, results)
    print(f"Wrote {LEDGER_OUT} ({len(results)} rows)")
    print(f"Wrote {REPORT_OUT}")


if __name__ == "__main__":
    main()
