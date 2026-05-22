"""Shared Bauteilgruppe evidence hunting utilities for BG-01..BG-06."""

from __future__ import annotations

import csv
import json
import re
import ssl
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
import urllib.parse

HERE = Path(__file__).resolve().parent
REVIEW = HERE.parent
REPO = REVIEW.parents[2]
SCRIPTS = REPO / "_scripts"
WORK = HERE
GEO_DIR = REVIEW.parent / "2026-06-06_project_bg_geo_extract"

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

from bg_slug_decompose import decompose_bg_id, project_aliases_from_geo  # noqa: E402
from quote_scorer import extract_best_sentence, is_valid_quote, norm_text, score_quote, token_hit  # noqa: E402

V6 = REVIEW / "VERIFICATION_LEDGER_ELEMENT_v6.csv"
V8 = REVIEW / "VERIFICATION_LEDGER_ELEMENT_v8.csv"
VOCAB_PATH = REPO / "_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl"
AKTEUR_GEO = GEO_DIR / "akteur_typ_projekt_geo.json"
REUSE_GEO = GEO_DIR / "reuse_geo_graph.json"
ENRICH_DIRS = [
    REPO / "_neo4j/intake/inbox/research/bauteilboersen_deep_enrichment_results",
    REPO / "_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results",
]
DOSSIER_ROOTS = [
    REPO / "_neo4j/processed/projects/records",
    REPO / "_neo4j/intake/archive",
    REPO / "_neo4j/intake/inbox",
]

SSL_CTX = ssl.create_default_context()
REVIEW_RUN = "bg_hunt_rework_2026_06_07"

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status",
    "verdict_before", "verdict_after", "confidence", "proof_quote",
    "proposed_action", "patch_op", "agent_id", "notes", "coverage_level",
    "graph_element_id", "evidence_basis", "matched_aliases", "alias_score",
    "project_anchor_hit", "component_family_hit", "search_tier", "queries_tried",
]

EXTRA_TOKENS: dict[str, list[str]] = {
    "bt_boden": ["boden", "floor", "flooring", "sol", "carrelage", "terrasse", "fliesen", "tiles"],
    "bt_wand": ["wand", "wall", "mur", "cloison", "wandelement", "wandelemente", "grossplatte", "großplatte"],
    "bt_fassade": ["fassade", "facade", "façade", "bardage", "cladding", "schindel", "schindeln", "shingle", "verkleidung", "parement"],
    "bt_gelaender": ["gelaender", "geländer", "railing", "garde-corps", "rambarde", "balustrade"],
    "bt_decke": ["decke", "ceiling", "plafond", "dalle", "plancher", "slab", "deckenelement", "deckenelemente", "hohldiele", "hollow core"],
    "bt_dach": ["dach", "roof", "toiture", "couverture"],
    "bt_fenster": ["fenster", "window", "fenêtre", "châssis", "rahmen", "fensterrahmen", "fensterrahmen"],
    "bt_tuer": ["tuer", "tür", "door", "porte", "türen"],
    "bt_traeger": ["traeger", "träger", "balken", "beam", "glulam", "profile"],
    "bt_fundament": ["fundament", "foundation", "fondation"],
    "bt_technik": ["technik", "sanitaire", "plomberie", "mep", "elevator", "aufzug", "motors"],
    "mat_keramik": ["keramik", "ceramic", "céramique", "carrelage", "tile", "terracotta", "terre cuite", "zellige"],
    "mat_ziegel": ["ziegel", "brick", "brique", "terracotta", "facing brick", "parement"],
    "mat_stahl": ["stahl", "steel", "acier", "metall", "metal"],
    "mat_holz": ["holz", "wood", "bois", "timber", "softwood"],
    "mat_glas": ["glas", "glass", "verre", "glazing", "partitions"],
    "mat_stahlbeton": ["stahlbeton", "reinforced concrete", "béton armé", "wbs70", "betonplatte"],
    "mat_beton": ["beton", "béton", "concrete"],
    "mat_naturstein": ["naturstein", "natural stone", "pierre", "granite", "granit", "bluestein"],
    "mat_kunststoff": ["kunststoff", "plastic", "plastique", "pvc", "polymer"],
    "mat_daemmstoff": ["daemmstoff", "dämmstoff", "insulation", "isolant"],
    "mat_metall": ["metall", "metal", "aluminium", "aluminum"],
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_v6_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    with V6.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
            if geid:
                idx[geid] = row
            cid = row.get("claim_id", "")
            if cid:
                idx[f"claim:{cid}"] = row
    return idx


def load_v8_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    path = V8 if V8.is_file() else V6
    with path.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh):
            geid = (row.get("graph_element_id") or row.get("element_id") or "").strip()
            if geid:
                idx[geid] = row
            cid = row.get("claim_id", "")
            if cid:
                idx[f"claim:{cid}"] = row
    return idx


def load_vocab_names() -> dict[str, str]:
    names: dict[str, str] = {}
    if not VOCAB_PATH.is_file():
        return names
    with VOCAB_PATH.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("record_type") == "node":
                names[rec["id"]] = rec.get("properties", {}).get("name", rec["id"])
    return names


def target_aliases(to_id: str, vocab_names: dict[str, str]) -> list[str]:
    aliases: list[str] = []
    name = vocab_names.get(to_id, to_id)
    if name:
        aliases.append(name)
        for part in re.split(r"[\s_/()-]+", name):
            if len(part) >= 3:
                aliases.append(part)
    aliases.extend(EXTRA_TOKENS.get(to_id, []))
    if "_" in to_id:
        aliases.append(to_id.split("_", 1)[1])
    return list(dict.fromkeys(norm_text(a) for a in aliases if a))


def load_geo_index() -> tuple[dict[str, dict], dict[str, list[str]]]:
    """Return projekt_id -> geo record, bg_id -> project URLs."""
    proj_index: dict[str, dict] = defaultdict(lambda: {"locations": [], "projekt_name": ""})
    bg_urls: dict[str, list[str]] = defaultdict(list)

    if AKTEUR_GEO.is_file():
        data = json.loads(AKTEUR_GEO.read_text(encoding="utf-8"))
        for akteur in data.get("akteure", []):
            for loc in akteur.get("locations", []):
                pid = loc.get("linked_projekt_id", "")
                if not pid:
                    continue
                proj_index[pid]["locations"].append(loc)
                proj_index[pid]["projekt_name"] = loc.get("linked_projekt_name", "") or proj_index[pid]["projekt_name"]
                url = loc.get("source_url", "")
                if url and url.startswith("http"):
                    if url not in proj_index[pid].get("urls", []):
                        proj_index[pid].setdefault("urls", []).append(url)
            for proj in akteur.get("projekte", []):
                pid = proj.get("id", "")
                if pid:
                    proj_index[pid]["projekt_name"] = proj.get("name", "") or proj_index[pid]["projekt_name"]

    if REUSE_GEO.is_file():
        reuse = json.loads(REUSE_GEO.read_text(encoding="utf-8"))
        for edge in reuse.get("edges", []) + reuse.get("links", []):
            url = edge.get("source_url") or edge.get("url") or ""
            pid = edge.get("projekt_id") or edge.get("project_id") or ""
            bg = edge.get("bg_id") or edge.get("bauteilgruppe_id") or ""
            if pid and url.startswith("http"):
                if url not in proj_index[pid].setdefault("urls", []):
                    proj_index[pid]["urls"].append(url)
            if bg and url.startswith("http") and url not in bg_urls[bg]:
                bg_urls[bg].append(url)

    return dict(proj_index), dict(bg_urls)


def load_dossier_index() -> tuple[dict[str, dict], dict[str, list[dict]]]:
    """bg_id -> properties; projekt_id -> list of dossier bg records."""
    idx: dict[str, dict] = {}
    by_projekt: dict[str, list[dict]] = defaultdict(list)
    for root in DOSSIER_ROOTS:
        if not root.is_dir():
            continue
        for path in root.rglob("*.kg.jsonl"):
            projekt_id = ""
            m = re.search(r"(p_[a-z0-9_]+)\.kg\.jsonl$", path.name, re.I)
            if m:
                projekt_id = m.group(1)
            try:
                for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    if rec.get("record_type") != "node":
                        continue
                    labels = rec.get("labels") or []
                    if "Bauteilgruppe" not in labels:
                        continue
                    bg_id = rec.get("id", "")
                    props = {**rec.get("properties", {}), "_source_file": str(path), "_legacy_id": bg_id}
                    if projekt_id:
                        props["_projekt_id"] = projekt_id
                    if bg_id:
                        idx[bg_id] = props
                    if projekt_id:
                        by_projekt[projekt_id].append(props)
            except (json.JSONDecodeError, OSError):
                pass
    return idx, dict(by_projekt)


def resolve_dossier(
    bg_id: str,
    bg_name: str,
    projekt_id: str,
    dossier_index: dict[str, dict],
    by_projekt: dict[str, list[dict]],
    decomp: dict,
) -> dict | None:
    if bg_id in dossier_index:
        return dossier_index[bg_id]
    if not projekt_id or projekt_id not in by_projekt:
        return None
    candidates = by_projekt[projekt_id]
    if not candidates:
        return None
    bg_tokens = set(norm_text(bg_name).split()) if bg_name else set()
    bg_tokens |= {norm_text(t) for t in decomp.get("component_tokens", []) + decomp.get("detail_tokens", []) if len(t) >= 4}
    bg_tokens |= {norm_text(decomp.get("material_token", ""))}
    best = None
    best_score = 0
    for cand in candidates:
        text = " ".join(str(cand.get(k, "")) for k in ("name", "raw_name", "neue_funktion", "alte_funktion"))
        ctoks = set(norm_text(text).split())
        overlap = len(bg_tokens & ctoks)
        if overlap > best_score:
            best_score = overlap
            best = cand
    return best if best_score >= 2 else (candidates[0] if len(candidates) == 1 else None)


def load_bg_projekt_map() -> dict[str, str]:
    uri, user, password, _ = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    mapping: dict[str, str] = {}
    with driver.session(database="mit-bestand") as session:
        for rec in session.run(
            "MATCH (p:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg:Bauteilgruppe) "
            "RETURN bg.id AS bg_id, p.id AS projekt_id, p.name AS projekt_name, bg.name AS bg_name"
        ):
            mapping[rec["bg_id"]] = {"projekt_id": rec["projekt_id"], "projekt_name": rec["projekt_name"], "bg_name": rec["bg_name"]}
    driver.close()
    return mapping


def load_live_bg_names() -> dict[str, str]:
    uri, user, password, _ = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    names: dict[str, str] = {}
    with driver.session(database="mit-bestand") as session:
        for rec in session.run("MATCH (bg:Bauteilgruppe) RETURN bg.id AS id, bg.name AS name"):
            names[rec["id"]] = rec["name"] or ""
    driver.close()
    return names


def fetch_url(url: str, cache: dict) -> dict:
    if url in cache:
        return cache[url]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    if not url or not str(url).lower().startswith("http"):
        entry["error"] = "non_http"
        cache[url] = entry
        return entry
    try:
        req = Request(
            url,
            headers={"User-Agent": "recherche-bg-hunt/1.0", "Accept": "text/html,application/xhtml+xml"},
        )
        with urlopen(req, timeout=20, context=SSL_CTX) as resp:
            raw = resp.read(600_000)
            entry["http_status"] = str(getattr(resp, "status", 200))
            entry["fetched"] = True
            entry["text"] = raw.decode("utf-8", errors="replace")
    except HTTPError as e:
        entry["http_status"] = str(e.code)
        entry["error"] = str(e)
        try:
            entry["text"] = e.read(100_000).decode("utf-8", errors="replace")
            entry["fetched"] = bool(entry["text"])
        except Exception:
            pass
    except (URLError, TimeoutError, OSError) as e:
        entry["error"] = str(e)
    cache[url] = entry
    time.sleep(0.35)
    return entry


BOILERPLATE_RE = re.compile(
    r"(thank you for getting in touch|submit|cookie|menu toggle|newsletter|"
    r"project pilots finland sweden|home - recreate home|dataLayer|wp-block)",
    re.I,
)


def is_boilerplate_quote(quote: str) -> bool:
    return bool(BOILERPLATE_RE.search(quote or ""))


def dossier_quote(dossier: dict | None) -> str:
    if not dossier:
        return ""
    for key in ("name", "raw_name", "neue_funktion", "alte_funktion"):
        val = dossier.get(key, "")
        if val and len(str(val)) >= 15:
            return str(val)[:300]
    return ""


_DOSSIER_BUNDLE_CACHE: dict[str, dict] = {}


def load_full_dossier_bundle(projekt_id: str) -> dict | None:
    """Load full project dossier text: Projekt note, all Bauteilgruppe lines, Quelle citations."""
    if not projekt_id:
        return None
    if projekt_id in _DOSSIER_BUNDLE_CACHE:
        return _DOSSIER_BUNDLE_CACHE[projekt_id]

    bundle: dict = {
        "projekt_id": projekt_id,
        "source_file": "",
        "projekt_name": "",
        "projekt_note": "",
        "bg_lines": [],
        "external_sources": [],
        "sentences": [],
        "full_text": "",
    }
    for root in DOSSIER_ROOTS:
        if not root.is_dir():
            continue
        for path in root.rglob(f"{projekt_id}.kg.jsonl"):
            bundle["source_file"] = str(path)
            parts: list[str] = []
            try:
                for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
                    if not line.strip():
                        continue
                    rec = json.loads(line)
                    if rec.get("record_type") != "node":
                        continue
                    labels = rec.get("labels") or []
                    props = rec.get("properties") or {}
                    if "Projekt" in labels:
                        bundle["projekt_name"] = props.get("name", "") or bundle["projekt_name"]
                        note = props.get("note", "")
                        if note:
                            bundle["projekt_note"] = str(note)
                            parts.append(str(note))
                        for k, v in props.items():
                            if k.startswith("wiederverwendete") and v:
                                parts.append(f"{k.replace('_', ' ')}: {v}")
                    elif "Bauteilgruppe" in labels:
                        bg_line = " ".join(
                            str(props.get(k, "")) for k in ("name", "raw_name", "neue_funktion", "alte_funktion", "menge", "flaeche_m2")
                            if props.get(k)
                        )
                        if bg_line.strip():
                            bundle["bg_lines"].append(bg_line.strip())
                            parts.append(bg_line.strip())
                    elif "Quelle" in labels:
                        for src in props.get("external_sources") or []:
                            if src and src not in bundle["external_sources"]:
                                bundle["external_sources"].append(str(src))
                                parts.append(str(src))
            except (json.JSONDecodeError, OSError):
                pass
            break
        if bundle["source_file"]:
            break

    if not bundle["source_file"]:
        _DOSSIER_BUNDLE_CACHE[projekt_id] = None
        return None

    bundle["full_text"] = " ".join(parts)
    bundle["sentences"] = [
        s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", bundle["full_text"]) if len(s.strip()) >= 12
    ]
    _DOSSIER_BUNDLE_CACHE[projekt_id] = bundle
    return bundle


def catalogue_family_hit(
    rel_type: str,
    quote: str,
    tgt_aliases: list[str],
    component_aliases: list[str],
    material_aliases: list[str],
) -> bool:
    """Relaxed catalogue gate: target lemma OR component/material family synonym."""
    q = norm_text(quote)
    if any(token_hit(t, q) for t in tgt_aliases if len(t) >= 3):
        return True
    if rel_type == "NUTZT_MATERIAL":
        return any(token_hit(t, q) for t in material_aliases if len(t) >= 3)
    if rel_type == "HAT_BAUTEILTYP":
        return any(token_hit(t, q) for t in component_aliases if len(t) >= 3)
    return False


def is_bundle_bg(bg_id: str, decomp: dict | None = None) -> bool:
    tokens = bg_id.replace("bg_", "").split("_")
    if "mehrere" in tokens:
        return True
    if any(x in bg_id for x in ("borrowed_elements", "doors_windows", "mixed_", "_multi_")):
        return True
    if decomp and decomp.get("material_token") == "mehrere":
        return True
    return False


HOMEPAGE_BLOCKLIST = re.compile(
    r"(multibrussels\.eu|about (the )?building|lobby office|workplace for over|google maps chapter)",
    re.I,
)


def generate_search_queries(
    projekt_name: str,
    project_aliases: list[str],
    component_aliases: list[str],
    material_aliases: list[str],
    external_sources: list[str],
    dossier_bundle: dict | None,
) -> list[str]:
    """Build 5–10 search query strings (for URL discovery / manual ladder)."""
    queries: list[str] = []
    anchor = projekt_name or (project_aliases[0] if project_aliases else "")
    comp = component_aliases[0] if component_aliases else ""
    mat = material_aliases[0] if material_aliases else ""
    if anchor and comp:
        queries.append(f"{anchor} {comp} wiederverwendet")
    if anchor and mat:
        queries.append(f"{anchor} {mat} reuse")
    if dossier_bundle and dossier_bundle.get("projekt_note"):
        note_words = dossier_bundle["projekt_note"][:80]
        queries.append(f"{anchor} {note_words}")
    for src in external_sources[:3]:
        if ":" in src:
            queries.append(src.split(":", 1)[-1].strip())
        else:
            queries.append(src)
    if anchor:
        queries.append(f'"{anchor}" reclaimed building components')
        queries.append(f"{anchor} filetype:pdf material reuse")
    return list(dict.fromkeys(q for q in queries if q and len(q) >= 8))[:10]


def _apply_hunt_result(
    out: dict,
    *,
    verdict_after: str,
    basis_ref: str,
    proof_quote: str,
    meta: dict,
    queries_tried: int,
    search_tier: str,
    source_note: dict,
    dossier_only: bool = False,
) -> dict:
    if verdict_after == "PROVEN":
        out.update(
            verdict_after="PROVEN",
            basis_ref=basis_ref,
            fetched="true",
            http_status="local" if dossier_only else out.get("http_status", "200"),
            proof_quote=proof_quote[:300],
            confidence="belegt",
            proposed_action="UPGRADE",
            patch_op="set_rel_properties",
            evidence_basis="bg_hunt_alias_match",
            matched_aliases=";".join(meta.get("matched_aliases", [])),
            alias_score=str(meta.get("score", "")),
            project_anchor_hit=str(meta.get("project_hit", False)).lower(),
            component_family_hit=str(
                meta.get("component_hit") or meta.get("material_hit") or meta.get("target_hit")
            ).lower(),
            search_tier=search_tier,
            queries_tried=str(queries_tried),
            notes=json.dumps(source_note),
        )
    elif verdict_after == "PARTIAL":
        out.update(
            verdict_after="PARTIAL",
            basis_ref=basis_ref,
            fetched="true",
            http_status="local" if dossier_only else out.get("http_status", ""),
            proof_quote=proof_quote[:300],
            confidence="niedrig",
            proposed_action="KEEP",
            evidence_basis="dossier" if dossier_only else "bg_hunt_alias_match",
            matched_aliases=";".join(meta.get("matched_aliases", [])),
            alias_score=str(meta.get("score", "")),
            project_anchor_hit=str(meta.get("project_hit", False)).lower(),
            component_family_hit=str(
                meta.get("component_hit") or meta.get("material_hit") or meta.get("target_hit")
            ).lower(),
            search_tier=search_tier,
            queries_tried=str(queries_tried),
            notes=json.dumps(source_note),
        )
    return out


def hunt_edge_rework(
    edge: dict,
    ledger_row: dict | None,
    *,
    vocab_names: dict[str, str],
    geo_index: dict,
    bg_urls: dict[str, list[str]],
    dossier_index: dict,
    by_projekt: dict[str, list[dict]],
    bg_projekt: dict,
    live_names: dict[str, str],
    cache: dict,
    agent_id: str,
    enable_web: bool = True,
    bundle_escalate: bool = True,
) -> dict:
    """Reworked hunt: full dossier mining, relaxed catalogue gate, optional web ladder."""
    from_id = edge.get("from_id", "")
    to_id = edge.get("to_id", "")
    rel_type = edge.get("rel_type", edge.get("rel_type_or_label", ""))
    bg_id = from_id if from_id.startswith("bg_") else to_id
    target_id = to_id if from_id.startswith("bg_") else from_id

    bg_name = live_names.get(bg_id) or edge.get("bg_name") or ""
    decomp = decompose_bg_id(bg_id, bg_name)
    proj_info = bg_projekt.get(bg_id, {})
    projekt_id = proj_info.get("projekt_id") or decomp.get("projekt_id_guess", "")
    projekt_name = proj_info.get("projekt_name", "")

    dossier = resolve_dossier(bg_id, bg_name, projekt_id, dossier_index, by_projekt, decomp)
    dossier_bundle = load_full_dossier_bundle(projekt_id) if projekt_id else None

    geo = geo_index.get(projekt_id, {})
    project_aliases = project_aliases_from_geo(projekt_id, projekt_name or geo.get("projekt_name", ""), geo)
    if projekt_name:
        project_aliases.insert(0, projekt_name)
    if projekt_id:
        for part in projekt_id.replace("p_", "").split("_"):
            if len(part) >= 4:
                project_aliases.append(part)
    if bg_name:
        project_aliases.append(bg_name)
        for part in re.split(r"[\s_/()-]+", bg_name):
            if len(part) >= 4:
                project_aliases.append(part)
    if dossier_bundle and dossier_bundle.get("projekt_note"):
        for part in re.split(r"[\s,;]+", dossier_bundle["projekt_note"]):
            if len(part) >= 5:
                project_aliases.append(part)
    project_aliases = list(dict.fromkeys(a for a in project_aliases if a))

    component_aliases = [norm_text(a) for a in decomp["component_aliases"] if a]
    material_aliases = [norm_text(a) for a in decomp["material_aliases"] if a]
    tgt_aliases = target_aliases(target_id, vocab_names)

    verdict_before = (ledger_row or {}).get("verdict", edge.get("verdict_before", "UNSUPPORTED"))
    geid = edge.get("element_id") or edge.get("graph_element_id") or (ledger_row or {}).get("graph_element_id", "")

    out = {
        "claim_id": (ledger_row or {}).get("claim_id", f"{agent_id}-{geid[-8:]}"),
        "claim_kind": "rel",
        "element_id": geid,
        "from_id": from_id,
        "to_id": to_id,
        "rel_type_or_label": rel_type,
        "asserted_claim": (ledger_row or {}).get("asserted_claim", f"{bg_id} {rel_type} {target_id}"),
        "basis_type": "web",
        "basis_ref": "",
        "fetched": "false",
        "http_status": "",
        "verdict_before": verdict_before,
        "verdict_after": verdict_before,
        "confidence": (ledger_row or {}).get("confidence", "teilweise_belegt"),
        "proof_quote": "",
        "proposed_action": "KEEP_DEFERRED" if verdict_before == "UNSUPPORTED" else "KEEP",
        "patch_op": "",
        "agent_id": agent_id,
        "notes": "",
        "coverage_level": "bg_hunt_rework",
        "graph_element_id": geid,
        "evidence_basis": "",
        "matched_aliases": "",
        "alias_score": "",
        "project_anchor_hit": "false",
        "component_family_hit": "false",
        "search_tier": "",
        "queries_tried": "0",
    }

    if rel_type not in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}:
        out["notes"] = "non_catalogue_skip"
        return out

    queries_tried = 0
    external_sources = (dossier_bundle or {}).get("external_sources", [])

    def finalize_catalogue(meta: dict, quote: str) -> dict:
        if rel_type in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}:
            fam = catalogue_family_hit(rel_type, quote, tgt_aliases, component_aliases, material_aliases)
            if meta.get("proven_eligible") and not fam:
                meta["proven_eligible"] = False
                meta["verdict_hint"] = "PARTIAL" if meta.get("score", 0) >= 5 else "UNSUPPORTED"
            elif fam and meta.get("project_hit") and meta.get("score", 0) >= 8:
                meta["proven_eligible"] = True
                meta["verdict_hint"] = "PROVEN"
        return meta

    # Phase A: full dossier bundle sentences
    if dossier_bundle and dossier_bundle.get("sentences"):
        dossier_projects = list(project_aliases)
        if projekt_id and dossier_bundle.get("source_file"):
            dossier_projects.insert(0, projekt_name or projekt_id.replace("p_", ""))
        best_quote, best_meta = "", {"score": -1, "verdict_hint": "UNSUPPORTED", "matched_aliases": []}
        for sent in dossier_bundle["sentences"]:
            meta = score_quote(
                sent, dossier_projects, component_aliases, material_aliases, target_aliases=tgt_aliases,
                require_project=bool(projekt_name),
            )
            meta = finalize_catalogue(meta, sent)
            if meta["score"] > best_meta.get("score", -1) and is_valid_quote(sent):
                best_quote, best_meta = sent.strip(), meta
        queries_tried += 1
        if best_meta.get("proven_eligible"):
            evidence_url = (geo.get("urls") or [None])[0] if geo.get("urls") else dossier_bundle.get("source_file", "dossier")
            return _apply_hunt_result(
                out,
                verdict_after="PROVEN",
                basis_ref=evidence_url or dossier_bundle["source_file"],
                proof_quote=best_quote,
                meta=best_meta,
                queries_tried=queries_tried,
                search_tier="primary",
                source_note={"tier": "primary", "source": "dossier_full", "matched_aliases": best_meta.get("matched_aliases"), "score": best_meta.get("score")},
                dossier_only=True,
            )
        if best_meta.get("verdict_hint") == "PARTIAL" and best_meta.get("score", 0) >= 5:
            return _apply_hunt_result(
                out,
                verdict_after="PARTIAL",
                basis_ref=dossier_bundle["source_file"],
                proof_quote=best_quote,
                meta=best_meta,
                queries_tried=queries_tried,
                search_tier="primary",
                source_note={"tier": "primary", "source": "dossier_partial", "matched_aliases": best_meta.get("matched_aliases"), "score": best_meta.get("score")},
                dossier_only=True,
            )

    # Phase A fallback: single matched bg dossier record
    dq = dossier_quote(dossier)
    if dq:
        queries_tried += 1
        meta = score_quote(dq, project_aliases, component_aliases, material_aliases, target_aliases=tgt_aliases)
        meta = finalize_catalogue(meta, dq)
        if projekt_id and dossier and dossier.get("_projekt_id") == projekt_id:
            if meta.get("component_hit") or meta.get("material_hit"):
                if meta.get("score", 0) >= 8 and catalogue_family_hit(rel_type, dq, tgt_aliases, component_aliases, material_aliases):
                    meta["proven_eligible"] = True
                    meta["project_hit"] = True
                    meta["verdict_hint"] = "PROVEN"
        if meta.get("proven_eligible"):
            evidence_url = (geo.get("urls") or [None])[0] if geo.get("urls") else (dossier or {}).get("_source_file", "dossier")
            return _apply_hunt_result(
                out, verdict_after="PROVEN", basis_ref=evidence_url, proof_quote=dq, meta=meta,
                queries_tried=queries_tried, search_tier="primary",
                source_note={"source": "dossier", "matched_aliases": meta.get("matched_aliases"), "score": meta.get("score")},
                dossier_only=True,
            )
        if meta.get("verdict_hint") == "PARTIAL" and meta.get("score", 0) >= 5:
            return _apply_hunt_result(
                out, verdict_after="PARTIAL", basis_ref=(dossier or {}).get("_source_file", "dossier"), proof_quote=dq, meta=meta,
                queries_tried=queries_tried, search_tier="primary",
                source_note={"source": "dossier_partial", "matched_aliases": meta.get("matched_aliases"), "score": meta.get("score")},
                dossier_only=True,
            )

    if not enable_web:
        out["queries_tried"] = str(queries_tried)
        out["notes"] = json.dumps({"reason": "no_dossier_match", "queries_tried": queries_tried})
        return out

    # Phase B: web discovery — prioritize non-homepage URLs
    urls: list[str] = []
    for u in bg_urls.get(bg_id, []):
        if u.startswith("http") and u not in urls:
            urls.append(u)
    for loc in geo.get("locations", []):
        u = loc.get("source_url", "")
        if u.startswith("http") and u not in urls:
            urls.append(u)
    for src in external_sources:
        if src.startswith("http") and src not in urls:
            urls.append(src)

    search_queries = generate_search_queries(
        projekt_name, project_aliases, component_aliases, material_aliases, external_sources, dossier_bundle,
    )
    for q in search_queries[:5]:
        queries_tried += 1
        ddg = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(q)}"
        fe = fetch_url(ddg, cache)
        if fe.get("fetched"):
            for m in re.finditer(r'uddg=([^&"]+)', fe.get("text", "")):
                try:
                    cand = urllib.parse.unquote(m.group(1))
                    if cand.startswith("http") and cand not in urls:
                        urls.append(cand)
                except Exception:
                    pass

    for url in urls[:8]:
        if HOMEPAGE_BLOCKLIST.search(url):
            continue
        queries_tried += 1
        fe = fetch_url(url, cache)
        if not fe.get("fetched"):
            continue
        quote, meta = extract_best_sentence(
            fe.get("text", ""), project_aliases, component_aliases, material_aliases, target_aliases=tgt_aliases,
        )
        if not quote or is_boilerplate_quote(quote) or HOMEPAGE_BLOCKLIST.search(quote):
            continue
        meta = finalize_catalogue(meta, quote)
        out["http_status"] = fe.get("http_status", "")
        if meta.get("proven_eligible"):
            return _apply_hunt_result(
                out, verdict_after="PROVEN", basis_ref=url, proof_quote=quote, meta=meta,
                queries_tried=queries_tried, search_tier="secondary",
                source_note={"tier": "secondary", "url": url, "matched_aliases": meta.get("matched_aliases"), "score": meta.get("score")},
            )
        if meta.get("verdict_hint") == "PARTIAL" and meta.get("score", 0) >= 5:
            return _apply_hunt_result(
                out, verdict_after="PARTIAL", basis_ref=url, proof_quote=quote, meta=meta,
                queries_tried=queries_tried, search_tier="secondary",
                source_note={"tier": "secondary", "url": url, "matched_aliases": meta.get("matched_aliases"), "score": meta.get("score")},
            )

    # Phase C: bundle escalation
    if bundle_escalate and is_bundle_bg(bg_id, decomp):
        out.update(
            verdict_after="PARTIAL",
            proposed_action="ESCALATE_HUMAN",
            confidence="niedrig",
            notes=json.dumps({"reason": "bundle_bg", "policy": "ESCALATE_HUMAN", "queries_tried": queries_tried}),
            queries_tried=str(queries_tried),
        )
        return out

    out["queries_tried"] = str(queries_tried)
    out["notes"] = json.dumps({"queries_tried": queries_tried, "urls_tried": urls[:5], "reason": "no_qualifying_quote"})
    if verdict_before == "UNSUPPORTED":
        out["proposed_action"] = "KEEP_DEFERRED"
    return out


def hunt_edge(
    edge: dict,
    v6_row: dict | None,
    *,
    vocab_names: dict[str, str],
    geo_index: dict,
    bg_urls: dict[str, list[str]],
    dossier_index: dict,
    by_projekt: dict[str, list[dict]],
    bg_projekt: dict,
    live_names: dict[str, str],
    cache: dict,
    agent_id: str,
) -> dict:
    from_id = edge.get("from_id", "")
    to_id = edge.get("to_id", "")
    rel_type = edge.get("rel_type", edge.get("rel_type_or_label", ""))
    bg_id = from_id if from_id.startswith("bg_") else to_id
    target_id = to_id if from_id.startswith("bg_") else from_id

    bg_name = live_names.get(bg_id) or edge.get("bg_name") or ""
    decomp = decompose_bg_id(bg_id, bg_name)
    proj_info = bg_projekt.get(bg_id, {})
    projekt_id = proj_info.get("projekt_id") or decomp.get("projekt_id_guess", "")
    projekt_name = proj_info.get("projekt_name", "")

    dossier = resolve_dossier(bg_id, bg_name, projekt_id, dossier_index, by_projekt, decomp)
    if dossier and not bg_name:
        bg_name = dossier.get("name", "")

    geo = geo_index.get(projekt_id, {})
    project_aliases = project_aliases_from_geo(projekt_id, projekt_name or geo.get("projekt_name", ""), geo)
    if projekt_name:
        project_aliases.insert(0, projekt_name)
    if projekt_id:
        for part in projekt_id.replace("p_", "").split("_"):
            if len(part) >= 4:
                project_aliases.append(part)
    if bg_name:
        project_aliases.append(bg_name)
        for part in re.split(r"[\s_/()-]+", bg_name):
            if len(part) >= 4:
                project_aliases.append(part)
    project_aliases = list(dict.fromkeys(a for a in project_aliases if a))

    component_aliases = [norm_text(a) for a in decomp["component_aliases"] if a]
    material_aliases = [norm_text(a) for a in decomp["material_aliases"] if a]
    tgt_aliases = target_aliases(target_id, vocab_names)

    verdict_before = (v6_row or {}).get("verdict", edge.get("verdict_before", "UNSUPPORTED"))
    geid = edge.get("element_id") or edge.get("graph_element_id") or (v6_row or {}).get("graph_element_id", "")

    out = {
        "claim_id": (v6_row or {}).get("claim_id", f"{agent_id}-{geid[-8:]}"),
        "claim_kind": "rel",
        "element_id": geid,
        "from_id": from_id,
        "to_id": to_id,
        "rel_type_or_label": rel_type,
        "asserted_claim": (v6_row or {}).get("asserted_claim", f"{bg_id} {rel_type} {target_id}"),
        "basis_type": "web",
        "basis_ref": "",
        "fetched": "false",
        "http_status": "",
        "verdict_before": verdict_before,
        "verdict_after": verdict_before,
        "confidence": (v6_row or {}).get("confidence", "teilweise_belegt"),
        "proof_quote": "",
        "proposed_action": "KEEP_DEFERRED" if verdict_before == "UNSUPPORTED" else "KEEP",
        "patch_op": "",
        "agent_id": agent_id,
        "notes": "",
        "coverage_level": "bg_hunt",
        "graph_element_id": geid,
        "evidence_basis": "",
        "matched_aliases": "",
        "alias_score": "",
        "project_anchor_hit": "false",
        "component_family_hit": "false",
        "search_tier": "",
        "queries_tried": "0",
    }

    if verdict_before != "UNSUPPORTED" and rel_type not in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}:
        out["notes"] = "no_unsupported_in_v6; logic_proven_pass_through"
        out["evidence_basis"] = "logic"
        return out

    # candidate URLs
    urls: list[str] = []
    for src in (
        geo.get("urls") or [],
        bg_urls.get(bg_id, []),
        [(v6_row or {}).get("basis_ref", "")],
    ):
        if isinstance(src, list):
            for u in src:
                if u and str(u).startswith("http") and u not in urls:
                    urls.append(str(u))
        elif src and str(src).startswith("http") and src not in urls:
            urls.append(str(src))

    dq = dossier_quote(dossier)
    queries_tried = 0

    # Tier 1: dossier text scoring (primary)
    if dq:
        queries_tried += 1
        # dossier on matched project: projekt_name counts as anchor when file projekt matches
        dossier_projects = project_aliases[:]
        if projekt_name:
            dossier_projects.insert(0, projekt_name)
        meta = score_quote(dq, dossier_projects, component_aliases, material_aliases, target_aliases=tgt_aliases)
        if rel_type in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}:
            tgt_hit = any(token_hit(norm_text(t), norm_text(dq)) for t in tgt_aliases if len(t) >= 3)
            if meta["proven_eligible"] and not tgt_hit:
                meta["proven_eligible"] = False
                meta["verdict_hint"] = "PARTIAL" if meta["score"] >= 5 else "UNSUPPORTED"
        # accept dossier PROVEN when project-linked file + component + (target for catalogue)
        if projekt_id and dossier and dossier.get("_projekt_id") == projekt_id:
            if meta["component_hit"] and meta["score"] >= 7:
                if rel_type not in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"} or meta.get("target_hit"):
                    if meta["score"] >= 8 and meta["component_hit"]:
                        meta["proven_eligible"] = True
                        meta["project_hit"] = True
                        meta["verdict_hint"] = "PROVEN"
        if meta["proven_eligible"]:
            evidence_url = (geo.get("urls") or [None])[0] if geo.get("urls") else (dossier or {}).get("_source_file", "dossier")
            out.update(
                verdict_after="PROVEN",
                basis_ref=evidence_url,
                fetched="true",
                http_status="local",
                proof_quote=dq[:300],
                confidence="belegt",
                proposed_action="UPGRADE",
                patch_op="set_rel_properties",
                evidence_basis="bg_hunt_alias_match",
                matched_aliases=";".join(meta["matched_aliases"]),
                alias_score=str(meta["score"]),
                project_anchor_hit=str(meta["project_hit"]).lower(),
                component_family_hit=str(meta["component_hit"]).lower(),
                search_tier="primary",
                queries_tried=str(queries_tried),
                notes=json.dumps({"matched_aliases": meta["matched_aliases"], "score": meta["score"], "tier": "primary", "source": "dossier"}),
            )
            return out
        if meta["verdict_hint"] == "PARTIAL" and meta["score"] >= 5:
            out.update(
                verdict_after="PARTIAL",
                basis_ref=(dossier or {}).get("_source_file", "dossier"),
                fetched="true",
                http_status="local",
                proof_quote=dq[:300],
                confidence="niedrig",
                proposed_action="KEEP",
                evidence_basis="dossier",
                matched_aliases=";".join(meta["matched_aliases"]),
                alias_score=str(meta["score"]),
                project_anchor_hit=str(meta["project_hit"]).lower(),
                component_family_hit=str(meta["component_hit"]).lower(),
                search_tier="primary",
                queries_tried=str(queries_tried),
                notes=json.dumps({"matched_aliases": meta["matched_aliases"], "score": meta["score"], "tier": "primary", "source": "dossier_partial"}),
            )
            return out

    # Tier 1/2: fetch project URLs
    for url in urls[:5]:
        queries_tried += 1
        fe = fetch_url(url, cache)
        if not fe.get("fetched"):
            continue
        quote, meta = extract_best_sentence(
            fe.get("text", ""),
            project_aliases,
            component_aliases,
            material_aliases,
            target_aliases=tgt_aliases,
        )
        if not quote or is_boilerplate_quote(quote):
            continue
        # catalogue edges require target vocab in quote for PROVEN
        if rel_type in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}:
            tgt_hit = any(token_hit(norm_text(t), norm_text(quote)) for t in tgt_aliases if len(t) >= 3)
            if meta["proven_eligible"] and not tgt_hit:
                meta["proven_eligible"] = False
                meta["verdict_hint"] = "PARTIAL" if meta["score"] >= 5 else "UNSUPPORTED"

        if meta["proven_eligible"]:
            out.update(
                verdict_after="PROVEN",
                basis_ref=url,
                fetched="true",
                http_status=fe.get("http_status", ""),
                proof_quote=quote[:300],
                confidence="belegt",
                proposed_action="UPGRADE",
                patch_op="set_rel_properties",
                evidence_basis="bg_hunt_alias_match",
                matched_aliases=";".join(meta["matched_aliases"]),
                alias_score=str(meta["score"]),
                project_anchor_hit=str(meta["project_hit"]).lower(),
                component_family_hit=str(meta["component_hit"]).lower(),
                search_tier="primary" if queries_tried <= 2 else "secondary",
                queries_tried=str(queries_tried),
                notes=json.dumps({"matched_aliases": meta["matched_aliases"], "score": meta["score"], "tier": out["search_tier"]}),
            )
            return out
        if meta["verdict_hint"] == "PARTIAL" and int(meta["score"]) >= 5:
            out.update(
                verdict_after="PARTIAL",
                basis_ref=url,
                fetched="true",
                http_status=fe.get("http_status", ""),
                proof_quote=quote[:300],
                confidence="niedrig",
                proposed_action="KEEP",
                evidence_basis="bg_hunt_alias_match",
                matched_aliases=";".join(meta["matched_aliases"]),
                alias_score=str(meta["score"]),
                project_anchor_hit=str(meta["project_hit"]).lower(),
                component_family_hit=str(meta["component_hit"]).lower(),
                search_tier="secondary",
                queries_tried=str(queries_tried),
                notes=json.dumps({"matched_aliases": meta["matched_aliases"], "score": meta["score"], "tier": "secondary"}),
            )
            return out

    out["queries_tried"] = str(queries_tried)
    out["notes"] = json.dumps({"queries_tried": queries_tried, "urls": urls[:3], "reason": "no_qualifying_quote"})
    if verdict_before == "UNSUPPORTED":
        out["proposed_action"] = "KEEP_DEFERRED"
    return out


def write_ledger(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        for row in rows:
            w.writerow(row)


def write_report(path: Path, agent_id: str, mission: str, rows: list[dict], scope_count: int, blockers: list[str]) -> None:
    vc = Counter(r.get("verdict_after", "") for r in rows)
    vb = Counter(r.get("verdict_before", "") for r in rows)
    upgrades = sum(1 for r in rows if r.get("proposed_action") == "UPGRADE")
    partial = vc.get("PARTIAL", 0)
    proven = vc.get("PROVEN", 0)
    unsupported = vc.get("UNSUPPORTED", 0)
    lines = [
        f"# {agent_id} Report — {mission}",
        "",
        f"**Generated:** {utc_now()}",
        "",
        "## Scope",
        f"- Scope edges exported: **{scope_count}**",
        f"- Processed this run: **{len(rows)}**",
        "",
        "## Verdict deltas",
        f"| verdict_before | count |",
        f"|---|---:|",
    ]
    for k, v in vb.most_common():
        lines.append(f"| {k} | {v} |")
    lines += ["", "| verdict_after | count |", "|---|---:|"]
    for k, v in vc.most_common():
        lines.append(f"| {k} | {v} |")
    lines += [
        "",
        "## Summary",
        f"- PROVEN upgrades: **{proven}** (new external: **{upgrades}**)",
        f"- PARTIAL: **{partial}**",
        f"- UNSUPPORTED kept: **{unsupported}**",
        "",
    ]
    if blockers:
        lines += ["## Blockers", ""] + [f"- {b}" for b in blockers]
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
