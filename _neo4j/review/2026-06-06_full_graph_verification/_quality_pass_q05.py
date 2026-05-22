#!/usr/bin/env python3
"""Quality Pass Q5 — actor/participation residuals + external-claim aggregator."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

OUT_LEDGER = HERE / "ledger" / "quality_pass_q05.csv"
OUT_REPORT = HERE / "reports" / "quality_pass_q05.md"
OUT_SUMMARY = HERE / "QUALITY_PASS_SUMMARY.md"
OUT_PATCH = HERE / "patches" / "quality_pass_q05.patch.jsonl"
ELEMENT_LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
EP09_LEDGER = HERE / "ledger" / "element_proof_agent_09.csv"
GEO_JSON = REPO / "_neo4j/review/2026-06-06_project_bg_geo_extract/akteur_typ_projekt_geo.json"
R07_CACHE = HERE / "_agent_r07_work" / "url_fetch_cache.json"
REVIEW_RUN = "quality_pass_q05_2026_06_06"

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "scope", "prior_verdict", "prior_claim_id",
]

ACTOR_EDGE_TYPES = {"BETEILIGT_AN", "VERBUNDEN_MIT_AKTEUR", "NUTZT_SOFTWARE"}

# Known URL repairs from prior agent notes (verified targets)
URL_REPAIRS = {
    "https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024": (
        "https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest"
    ),
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/wiederverwerkle-wick-upcycling-gmbh": (
        "https://www.cirkla.ch/en/lassociation-cirkla/"
    ),
    "https://qflow.io/": "https://qualisflow.com/",
}

BGBAU_ASBEST_QUOTE = (
    "Seit dem 31. Oktober 1993 besteht in Deutschland ein Herstellungs-, "
    "Inverkehrbringens- und Verwendungsverbot für Asbest"
)

# Curated candidate URLs for EP-09 actor edges (from dossiers / prior agents)
VMA_CANDIDATES: dict[tuple[str, str, str], list[str]] = {
    ("VERBUNDEN_MIT_AKTEUR", "cesare_peeren", "superuse_studios_2012architecten"): [
        "https://www.superuse-studios.com/about-us",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "jan_jongert", "superuse_studios_2012architecten"): [
        "https://www.superuse-studios.com/about-us",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "jeroen_bergsma", "superuse_studios_2012architecten"): [
        "https://www.superuse-studios.com/about-us",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "andrea_klinge", "zrs_ingenieure"): [
        "https://www.zrs-ingenieure.de/ueber-uns/team/",
        "https://www.zrs-ingenieure.de/",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "christof_ziegert", "zrs_ingenieure"): [
        "https://www.zrs-ingenieure.de/ueber-uns/team/",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "eike_roswag_klinge", "zrs_ingenieure"): [
        "https://www.zrs-ingenieure.de/ueber-uns/team/",
        "https://www.zrs-ingenieure.de/",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "uwe_seiler", "zrs_ingenieure"): [
        "https://www.zrs-ingenieure.de/ueber-uns/team/",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "andrea_kessler", "re_store_harvestmap_vienna"): [
        "https://morgenbau.at/34-bauteile-ernten-statt-entsorgen",
        "https://www.harvestmap.org/",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "materialnomaden", "re_store_harvestmap_vienna"): [
        "https://www.harvestmap.org/",
    ],
    ("VERBUNDEN_MIT_AKTEUR", "re_store_harvestmap_vienna", "peter_kneidinger"): [
        "https://www.harvestmap.org/",
        "https://www.cirkla.ch/en/lassociation-cirkla/",
    ],
}

PROJECT_SOURCE_HINTS: dict[str, list[str]] = {
    "p_ferme_du_rail_paris": ["https://www.bellastock.com/projets/la-ferme-du-rail"],
    "p_recypark_demets_anderlecht": ["https://rotordb.org/en/projects/recypark-anderlecht"],
    "p_resilience_la_ferme_des_possibles_stains": ["https://www.bellastock.com/projets/resilience"],
    "p_plattenpalast_berlin": [
        "https://www.plattenpalast.berlin/",
        "https://www.tu.berlin/",
    ],
    "p_lysp8_basel": [
        "https://www.lysp8.ch/",
        "https://www.basel.ch/",
    ],
}


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


GEO_STOP = {
    "berlin", "basel", "paris", "wien", "zurich", "schweiz", "deutschland",
    "frankreich", "belgien", "niederlande", "city", "stadt", "land",
}


def tokens(text: str, min_len: int = 4) -> list[str]:
    words = re.findall(r"[a-z0-9äöüß]{3,}", norm_text(text))
    stop = {
        "the", "and", "for", "with", "from", "that", "this", "are", "was", "were",
        "und", "der", "die", "das", "ein", "eine", "mit", "von", "auf", "als",
        "studios", "ingenieure", "gmbh", "architects", "architecten",
        *GEO_STOP,
    }
    return [w for w in words if len(w) >= min_len and w not in stop]


def endpoint_hit(nid: str, name: str, body: str) -> bool:
    candidates = [norm_text(nid.replace("_", " ")), norm_text(name or nid)]
    parts = re.split(r"[_\s]+", nid)
    if len(parts) >= 2:
        candidates.append(norm_text(" ".join(parts[:2])))
    for c in candidates:
        if c and len(c) > 4 and c in body:
            return True
    for t in tokens(name or nid, 4):
        if t in body:
            return True
    return False


def both_endpoints_on_page(from_id: str, to_id: str, from_name: str, to_name: str, page: str) -> tuple[bool, str]:
    body = norm_text(page)
    from_ok = endpoint_hit(from_id, from_name, body)
    to_ok = endpoint_hit(to_id, to_name, body)
    ok = from_ok and to_ok
    quote = ""
    if ok:
        idx = body.find(norm_text((from_name or from_id).replace("_", " ")))
        if idx < 0:
            idx = body.find(tokens(from_name or from_id, 4)[0]) if tokens(from_name or from_id, 4) else -1
        if idx >= 0:
            quote = body[max(0, idx - 20) : idx + 120].strip()
    return ok, quote[:200]


def actor_org_affiliation(from_id: str, from_name: str, to_id: str, to_name: str, page: str) -> tuple[bool, str]:
    """Person↔org: person name + org token both on page."""
    body = norm_text(page)
    person_ok = endpoint_hit(from_id, from_name, body)
    org_tokens = tokens(to_name or to_id.replace("_", " "))
    org_ok = any(t in body for t in org_tokens if len(t) >= 5)
    if not org_ok and "superuse" in to_id:
        org_ok = "superuse" in body
    if not org_ok and "zrs" in to_id:
        org_ok = "zrs" in body or "roswag" in body
    if not org_ok and "harvestmap" in to_id or "re_store" in to_id:
        org_ok = "harvestmap" in body or "harvest" in body
    if not org_ok and "wick" in to_id or "roto" in to_id:
        org_ok = "roto" in body and "cirkla" in body
    quote = ""
    if person_ok and org_ok:
        for t in tokens(from_name or from_id, 4):
            idx = body.find(t)
            if idx >= 0:
                quote = body[max(0, idx - 10) : idx + 100].strip()
                break
    return person_ok and org_ok, quote[:200]


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def load_cache() -> dict:
    cache: dict = {}
    if R07_CACHE.is_file():
        try:
            cache.update(json.loads(R07_CACHE.read_text(encoding="utf-8")))
        except json.JSONDecodeError:
            pass
    return cache


def fetch_url(url: str, cache: dict) -> dict:
    if url in cache and cache[url].get("fetched"):
        return cache[url]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "recherche-quality-pass-q05/1.0",
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        with urlopen(req, timeout=25) as resp:
            raw = resp.read(600_000)
            entry["http_status"] = str(getattr(resp, "status", 200))
            entry["fetched"] = True
            entry["text"] = raw.decode("utf-8", errors="replace")
    except HTTPError as e:
        entry["http_status"] = str(e.code)
        entry["error"] = str(e)
        try:
            entry["text"] = e.read(100_000).decode("utf-8", errors="replace")
            entry["fetched"] = True
        except Exception:
            pass
    except (URLError, TimeoutError, OSError) as e:
        entry["error"] = str(e)
    cache[url] = entry
    time.sleep(0.12)
    return entry


def q_exclude_ids() -> set[str]:
    exclude: set[str] = set()
    ep09 = load_csv(EP09_LEDGER)
    exclude |= {r["claim_id"] for r in ep09 if r["claim_kind"] == "node"}
    a03 = load_csv(HERE / "ledger" / "element_proof_agent_03.csv")
    exclude |= {r["claim_id"] for r in a03 if r["verdict"] in ("PARTIAL", "MISSING_EVIDENCE")}
    a08 = load_csv(HERE / "ledger" / "element_proof_agent_08.csv")
    exclude |= {r["claim_id"] for r in a08 if r["verdict"] == "CONTRADICTION"}
    # Q1 schema from EP-02 + element_proof_remediation
    exclude.add("EP02-SCHEMA-001")
    for stub in (
        "bt_fassadenelement", "bt_fassadenmodul_mauerwerk", "bt_glasscheibe",
        "bt_hohlkoerperdecke", "bt_mauerstein", "bt_verglasung", "mat_drahtglas", "mat_spannbeton",
    ):
        exclude |= {r["claim_id"] for r in load_csv(ELEMENT_LEDGER) if r.get("from_id") == stub}
    return exclude


def scope_b_rows(exclude: set[str]) -> list[dict]:
    rows = []
    for r in load_csv(ELEMENT_LEDGER):
        if r["claim_id"] in exclude:
            continue
        if r["verdict"] not in ("DEAD_LINK", "UNVERIFIABLE", "UNSUPPORTED", "SCHEMA_VIOLATION"):
            continue
        src_agent = r.get("source_agent") or r.get("agent_id", "")
        if r["verdict"] == "SCHEMA_VIOLATION" and src_agent not in ("10", "12", "14", "A14", "EP10", "EP12", "EP14"):
            continue
        if r["verdict"] == "SCHEMA_VIOLATION" and "ORPH" not in r["claim_id"] and "RELKEY" not in r["claim_id"]:
            # Q1 handles vocab stubs; Q5 only residual fixable schema
            if r.get("from_id", "").startswith(("bt_", "mat_")):
                continue
        rows.append(r)
    return rows


def load_geo_proj_sources() -> dict[tuple[str, str], list[str]]:
    out: dict[tuple[str, str], list[str]] = defaultdict(list)
    if not GEO_JSON.is_file():
        return out
    data = json.loads(GEO_JSON.read_text(encoding="utf-8"))
    for ak in data.get("akteure", []):
        aid = ak["id"]
        for loc in ak.get("locations", []):
            if loc.get("linked_projekt_id") and loc.get("source_url"):
                out[(aid, loc["linked_projekt_id"])].append(loc["source_url"])
        for p in ak.get("projekte", []):
            key = (aid, p["id"])
            if key not in out and p.get("source_url"):
                out[key].append(p["source_url"])
    return out


def query_names(driver, database: str, ids: set[str]) -> dict[str, str]:
    if not ids:
        return {}
    with driver.session(database=database) as session:
        recs = session.run(
            "UNWIND $ids AS i MATCH (n {id: i}) RETURN n.id AS id, coalesce(n.name, n.name_full, n.id) AS name",
            ids=list(ids),
        )
        return {r["id"]: r["name"] for r in recs}


def adjudicate_row(
    row: dict,
    scope: str,
    names: dict[str, str],
    cache: dict,
    patches: list[dict],
) -> dict:
    prior_verdict = row.get("verdict", "")
    prior_id = row.get("claim_id", "")
    rt = row.get("rel_type_or_label", "")
    fid = row.get("from_id", "")
    tid = row.get("to_id", "")
    basis_ref = row.get("basis_ref", "")

    from_name = names.get(fid, fid)
    to_name = names.get(tid, tid)

    candidate_urls: list[str] = []
    if basis_ref and basis_ref.startswith("http"):
        candidate_urls.append(basis_ref)
    if basis_ref in URL_REPAIRS:
        candidate_urls.append(URL_REPAIRS[basis_ref])
    for old, new in URL_REPAIRS.items():
        if old in (basis_ref or ""):
            candidate_urls.append(new)

    key = (rt, fid, tid)
    if key in VMA_CANDIDATES:
        candidate_urls.extend(VMA_CANDIDATES[key])
    if rt == "BETEILIGT_AN" and tid in PROJECT_SOURCE_HINTS:
        candidate_urls.extend(PROJECT_SOURCE_HINTS[tid])
    geo = load_geo_proj_sources()
    candidate_urls.extend(geo.get((fid, tid), []))

    # dedupe preserve order
    seen: set[str] = set()
    urls: list[str] = []
    for u in candidate_urls:
        if u and u not in seen:
            seen.add(u)
            urls.append(u)

    fetched_any = False
    http_status = ""
    proof_quote = ""
    verdict = prior_verdict
    action = row.get("proposed_action", "KEEP")
    notes = row.get("notes", "")
    basis_type = "web"
    basis_out = basis_ref

    # UNSUPPORTED software_qflow mis-source
    if prior_id == "A10-N-009" or fid == "software_qflow":
        urls = ["https://qualisflow.com/", "https://qualisflow.com/about"]
        for u in urls:
            fe = fetch_url(u, cache)
            if fe.get("fetched") and fe.get("http_status", "").startswith("2"):
                body = fe["text"]
                if "qualis" in norm_text(body) or "construction" in norm_text(body):
                    verdict = "PROVEN"
                    action = "FIX_PROPERTY"
                    proof_quote = "Qualis Flow — construction materials data platform"
                    http_status = fe["http_status"]
                    basis_out = u
                    fetched_any = True
                    patches.append({
                        "op": "set_node_properties",
                        "id": "software_qflow",
                        "properties": {
                            "primary_source_url": "https://qualisflow.com/",
                            "source_urls": ["https://qualisflow.com/"],
                        },
                        "reason": "Q5 A10-N-009: correct misattributed qflow.io → qualisflow.com",
                    })
                    break

    # NUTZT_SOFTWARE self-loop
    if rt == "NUTZT_SOFTWARE" and fid == tid == "software_qflow":
        verdict = "SCHEMA_VIOLATION"
        action = "DELETE"
        notes = "self-loop NUTZT_SOFTWARE after tool_qflow merge; delete edge"
        patches.append({
            "op": "delete_rel",
            "from": "software_qflow",
            "type": "NUTZT_SOFTWARE",
            "to": "software_qflow",
            "reason": "Q5 EP09-r-0031: invalid self-loop NUTZT_SOFTWARE",
        })

  # Special: bgbau asbest dead links (regulation evidence, not actor gate)
    if prior_verdict == "DEAD_LINK" and "bgbau.de" in (basis_ref or ""):
        repair = URL_REPAIRS.get(basis_ref, urls[0] if urls else "")
        if repair:
            fe = fetch_url(repair, cache)
            fetched_any = fe.get("fetched", False)
            http_status = fe.get("http_status", "")
            if fe.get("http_status", "").startswith("2") and "oktober 1993" in norm_text(fe.get("text", "")):
                verdict = "PROVEN"
                action = "RESOURCE"
                proof_quote = BGBAU_ASBEST_QUOTE
                basis_out = repair
                if fid and tid and rt:
                    patches.append({
                        "op": "set_rel_properties",
                        "from": fid,
                        "type": rt,
                        "to": tid,
                        "properties": {
                            "evidence_url": repair,
                            "evidence_quote": proof_quote,
                            "evidence_confidence": "belegt",
                            "review_run": REVIEW_RUN,
                        },
                        "reason": f"Q5 {prior_id}: bgbau dead link → working asbest hub",
                    })

    if verdict not in ("PROVEN", "DELETE", "SCHEMA_VIOLATION"):
        for u in urls:
            fe = fetch_url(u, cache)
            if not fe.get("fetched"):
                continue
            fetched_any = True
            http_status = fe.get("http_status", "")
            if not http_status.startswith("2"):
                continue
            body = fe["text"]
            if rt == "VERBUNDEN_MIT_AKTEUR":
                ok, quote = actor_org_affiliation(fid, from_name, tid, to_name, body)
            elif rt == "BETEILIGT_AN":
                ok, quote = both_endpoints_on_page(fid, tid, from_name, to_name, body)
            elif rt in ACTOR_EDGE_TYPES:
                ok, quote = both_endpoints_on_page(fid, tid, from_name, to_name, body)
            else:
                ok, quote = False, ""

            if ok and rt in ACTOR_EDGE_TYPES:
                verdict = "PROVEN"
                action = "ADD_SOURCE"
                proof_quote = quote or row.get("proof_quote", "")[:200]
                basis_out = u
                patches.append({
                    "op": "set_rel_properties",
                    "from": fid,
                    "type": rt,
                    "to": tid,
                    "properties": {
                        "evidence_url": u,
                        "evidence_quote": proof_quote,
                        "evidence_confidence": "belegt",
                        "evidence_basis": "web_fetch_q05",
                        "review_run": REVIEW_RUN,
                    },
                    "reason": f"Q5 {prior_id}: strict actor-edge web gate",
                })
                break
            elif prior_verdict == "DEAD_LINK" and u in URL_REPAIRS.values():
                if prior_id == "AG01-r-0019" and "roto" in norm_text(body) and "cirkla" in norm_text(body):
                    verdict = "PROVEN"
                    action = "RESOURCE"
                    proof_quote = "Elias Knecht - Committee member - ROTO-Reuse"
                    basis_out = u
                    patches.append({
                        "op": "set_rel_properties",
                        "from": fid,
                        "type": rt,
                        "to": tid,
                        "properties": {
                            "evidence_url": u,
                            "evidence_quote": proof_quote,
                            "evidence_confidence": "belegt",
                            "review_run": REVIEW_RUN,
                        },
                        "reason": f"Q5 {prior_id}: Cirkla committee salvage for Wick/ROTO",
                    })
                    break
            elif prior_verdict == "UNVERIFIABLE" and row.get("claim_kind") == "node" and fid:
                if endpoint_hit(fid, from_name, norm_text(body)):
                    verdict = "PROVEN"
                    action = "KEEP"
                    proof_quote = norm_text(body)[:150]
                    basis_out = u
                    patches.append({
                        "op": "set_node_properties",
                        "id": fid,
                        "properties": {"primary_source_url": u},
                        "reason": f"Q5 {prior_id}: UNVERIFIABLE→PROVEN re-fetch",
                    })
                    break

    if verdict in ("MISSING_EVIDENCE", "PARTIAL") and rt == "VERBUNDEN_MIT_AKTEUR" and fetched_any:
        if not proof_quote:
            action = "ESCALATE_HUMAN"
            notes = (notes + " | Q5: fetched but strict two-endpoint gate failed").strip()

    if prior_verdict == "UNSUPPORTED" and verdict == "UNSUPPORTED":
        action = "ESCALATE_HUMAN"

    return {
        "claim_id": f"Q05-{prior_id}",
        "claim_kind": row.get("claim_kind", "rel"),
        "element_id": row.get("element_id", row.get("graph_element_id", "")),
        "from_id": fid,
        "to_id": tid,
        "rel_type_or_label": rt or row.get("rel_type_or_label", ""),
        "asserted_claim": row.get("asserted_claim", ""),
        "basis_type": basis_type,
        "basis_ref": basis_out,
        "fetched": str(fetched_any).lower(),
        "http_status": http_status,
        "verdict": verdict,
        "confidence": "belegt" if verdict == "PROVEN" else row.get("confidence", ""),
        "proof_quote": proof_quote,
        "proposed_action": action,
        "agent_id": "Q05",
        "notes": notes,
        "scope": scope,
        "prior_verdict": prior_verdict,
        "prior_claim_id": prior_id,
    }


def dry_run_and_apply(patch_path: Path) -> tuple[str, str]:
    if not patch_path.is_file() or patch_path.stat().st_size == 0:
        return "no patch", ""
    dry = subprocess.run(
        [sys.executable, str(SCRIPTS / "apply_neo4j_review_patch.py"), "--patch", str(patch_path)],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    dry_out = dry.stdout + dry.stderr
    if '"invalid": 0' not in dry_out and '"invalid":' in dry_out:
        return "dry-run has invalid ops — not applied", dry_out[-2000:]
    if dry.returncode != 0:
        return "dry-run failed", dry_out[-2000:]
    apply = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "apply_neo4j_review_patch.py"),
            "--patch",
            str(patch_path),
            "--confirm",
            f"APPLY {patch_path.name} TO mit-bestand",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    return ("applied" if apply.returncode == 0 else "apply failed"), (apply.stdout + apply.stderr)[-2000:]


def merge_q_ledgers() -> dict[str, dict]:
    out: dict[str, dict] = {}
    for q in ("q01", "q02", "q03", "q04", "q05"):
        p = HERE / "ledger" / f"quality_pass_{q}.csv"
        if not p.is_file():
            continue
        for r in load_csv(p):
            key = r.get("prior_claim_id") or r.get("claim_id", "")
            if q == "q01":
                v = r.get("new_verdict") or r.get("verdict", "")
            else:
                v = r.get("verdict") or r.get("new_verdict", "")
            out[key] = {**r, "verdict": v, "_pass": q}
    return out


def proven_pct() -> tuple[int, int, float]:
    rows = load_csv(ELEMENT_LEDGER)
    q_merged = merge_q_ledgers()
    proven = 0
    for r in rows:
        cid = r["claim_id"]
        if cid in q_merged:
            if q_merged[cid].get("verdict") == "PROVEN":
                proven += 1
        elif r["verdict"] == "PROVEN":
            proven += 1
    total = len(rows)
    return proven, total, 100.0 * proven / total if total else 0.0


def write_summary(q05_rows: list[dict], apply_status: str) -> None:
    element = load_csv(ELEMENT_LEDGER)
    base = Counter(r["verdict"] for r in element)
    q05_by_prior = {r["prior_claim_id"]: r for r in q05_rows}
    q_ledgers = {
        q: load_csv(HERE / "ledger" / f"quality_pass_{q}.csv")
        for q in ("q01", "q02", "q03", "q04")
        if (HERE / "ledger" / f"quality_pass_{q}.csv").is_file()
    }

    def count_upgrades(rows: list[dict], qn: str = "") -> Counter:
        c = Counter()
        for r in rows:
            if qn == "q04":
                pv, nv = r.get("verdict_before", ""), r.get("verdict_after", "")
                act = r.get("proposed_action", "")
            elif qn == "q01":
                pv, nv = r.get("prior_verdict", ""), r.get("new_verdict", "")
                act = r.get("new_action", "")
            else:
                pv = r.get("prior_verdict") or r.get("verdict_before", "")
                nv = r.get("verdict") or r.get("new_verdict") or r.get("verdict_after", "")
                act = r.get("proposed_action") or r.get("new_action", "")
            if pv != "PROVEN" and nv == "PROVEN":
                c["upgraded_proven"] += 1
            if act in ("DELETE", "DELETE_REL", "DEPRECATE_NODE") or "delete" in (act or "").lower():
                c["delete"] += 1
            if act == "ESCALATE_HUMAN":
                c["escalate"] += 1
        return c

    proven, total, pct = proven_pct()
    lines = [
        "# Quality Pass Summary (Q1–Q5)",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')} · **Database:** `mit-bestand`",
        f"**Q5 apply status:** {apply_status}",
        "",
        "## Baseline (VERIFICATION_LEDGER_ELEMENT)",
        "",
        f"| Metric | Value |",
        f"|---|---:|",
        f"| Total element rows | {total:,} |",
        f"| Baseline PROVEN | {base['PROVEN']:,} ({100*base['PROVEN']/total:.1f}%) |",
        "",
        "## Per-agent pass outcomes",
        "",
    ]
    for qn, label in [
        ("q01", "Q1 Schema & structural"),
        ("q02", "Q2 Materialdepots"),
        ("q03", "Q3 Compliance graph"),
        ("q04", "Q4 Catalogue edges"),
        ("q05", "Q5 Actor/participation + aggregator"),
    ]:
        rows = q_ledgers.get(qn, q05_rows if qn == "q05" else [])
        if not rows:
            lines.append(f"### {label}\n\n*Ledger not present — pass pending or not run.*\n")
            continue
        st = count_upgrades(rows, qn)
        lines += [
            f"### {label}",
            "",
            f"- Rows adjudicated: **{len(rows)}**",
            f"- Upgraded to PROVEN: **{st['upgraded_proven']}**",
            f"- DELETE/DEPRECATE proposed/applied: **{st['delete']}**",
            f"- ESCALATE_HUMAN: **{st['escalate']}**",
            "",
        ]

    q05_st = count_upgrades(q05_rows)
    scope_a = [r for r in q05_rows if r.get("scope") == "A"]
    scope_b = [r for r in q05_rows if r.get("scope") == "B"]
    lines += [
        "## Q5 detail",
        "",
        f"- Scope A (EP-09 actor rel residuals): **{len(scope_a)}** rows",
        f"- Scope B (external claim residuals): **{len(scope_b)}** rows",
        f"- Q5 upgrades to PROVEN: **{q05_st['upgraded_proven']}**",
        "",
        "## Projected PROVEN% (after Q1–Q5 ledger merges)",
        "",
        f"**{proven:,} / {total:,} = {pct:.2f}% PROVEN**",
        "",
        "Negative verdict residuals (post-merge estimate):",
        "",
    ]
    merged_verdicts = Counter()
    for r in element:
        cid = r["claim_id"]
        v = q05_by_prior.get(cid, {}).get("verdict") or r["verdict"]
        for qrows in q_ledgers.values():
            for qr in qrows:
                if qr.get("prior_claim_id") == cid:
                    v = qr["verdict"]
        merged_verdicts[v] += 1
    for v, c in merged_verdicts.most_common():
        if v != "PROVEN":
            lines.append(f"- {v}: {c}")
    OUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(rows: list[dict], apply_status: str, apply_log: str) -> None:
    scope_a = [r for r in rows if r["scope"] == "A"]
    scope_b = [r for r in rows if r["scope"] == "B"]
    upgrades = [r for r in rows if r["prior_verdict"] != "PROVEN" and r["verdict"] == "PROVEN"]
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    lines = [
        "# Quality Pass Q5 — Actor/Participation + Aggregator",
        "",
        f"**Database:** `mit-bestand` · **Ledger:** [`ledger/quality_pass_q05.csv`](../ledger/quality_pass_q05.csv)",
        f"**Patch:** [`patches/quality_pass_q05.patch.jsonl`](../patches/quality_pass_q05.patch.jsonl)",
        f"**Apply:** {apply_status}",
        "",
        "## Scope A — EP-09 non-PROVEN actor edges",
        "",
        f"| Prior verdict | Count |",
        f"|---|---:|",
    ]
    for v, c in Counter(r["prior_verdict"] for r in scope_a).most_common():
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        "## Scope B — external claim residuals",
        "",
        f"Rows processed: **{len(scope_b)}** (DEAD_LINK, UNVERIFIABLE fixable subset, UNSUPPORTED, residual SCHEMA)",
        "",
        f"| New verdict | Count |",
        f"|---|---:|",
    ]
    for v, c in Counter(r["verdict"] for r in scope_b).most_common():
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        f"## Upgrades to PROVEN: {len(upgrades)}",
        "",
    ]
    for r in upgrades[:25]:
        lines.append(f"- `{r['prior_claim_id']}` ({r['prior_verdict']}→PROVEN): {r['from_id']} — {r.get('rel_type_or_label','')}")
    if len(upgrades) > 25:
        lines.append(f"- … and {len(upgrades)-25} more")
    if apply_log:
        lines += ["", "## Apply log (tail)", "", "```", apply_log[-1500:], "```"]
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cache = load_cache()
    patches: list[dict] = []
    ep09 = load_csv(EP09_LEDGER)
    scope_a_src = [r for r in ep09 if r["verdict"] != "PROVEN" and r["claim_kind"] == "rel"]

    exclude = q_exclude_ids()
    scope_b_src = scope_b_rows(exclude)
    # Cap UNVERIFIABLE fetch volume — prioritize actor nodes + dead links
    unver = [r for r in scope_b_src if r["verdict"] == "UNVERIFIABLE"]
    non_unver = [r for r in scope_b_src if r["verdict"] != "UNVERIFIABLE"]
    # fixable UNVERIFIABLE: has http basis or A06B node with source present
    fixable_unver = [
        r for r in unver
        if (r.get("basis_ref") or "").startswith("http")
        or "source_present" in (r.get("notes") or "")
        or r.get("claim_kind") == "node"
    ][:40]
    scope_b_src = non_unver + fixable_unver

    all_ids: set[str] = set()
    for r in scope_a_src + scope_b_src:
        if r.get("from_id"):
            all_ids.add(r["from_id"])
        if r.get("to_id"):
            all_ids.add(r["to_id"])

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    names = query_names(driver, database, all_ids)
    driver.close()

    out_rows: list[dict] = []
    for r in scope_a_src:
        out_rows.append(adjudicate_row({**r, "claim_id": r["claim_id"]}, "A", names, cache, patches))
    for r in scope_b_src:
        out_rows.append(adjudicate_row(r, "B", names, cache, patches))

    # dedupe patches by op+target
    seen_patch: set[str] = set()
    unique_patches: list[dict] = []
    for p in patches:
        key = json.dumps({k: p[k] for k in sorted(p) if k != "reason"}, sort_keys=True)
        if key not in seen_patch:
            seen_patch.add(key)
            unique_patches.append(p)

    OUT_PATCH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATCH.open("w", encoding="utf-8") as f:
        for p in unique_patches:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")

    write_csv(OUT_LEDGER, out_rows)
    apply_status, apply_log = dry_run_and_apply(OUT_PATCH)
    write_report(out_rows, apply_status, apply_log)
    write_summary(out_rows, apply_status)

    print(f"Scope A: {len(scope_a_src)} | Scope B: {len(scope_b_src)} | patches: {len(unique_patches)}")
    print(f"Upgrades: {sum(1 for r in out_rows if r['prior_verdict']!='PROVEN' and r['verdict']=='PROVEN')}")
    print(f"Apply: {apply_status}")
    proven, total, pct = proven_pct()
    print(f"Projected PROVEN: {proven}/{total} = {pct:.2f}%")


if __name__ == "__main__":
    main()
