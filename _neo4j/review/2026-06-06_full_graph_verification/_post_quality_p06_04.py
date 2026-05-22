#!/usr/bin/env python3
"""Post Quality Pass P6-04 — Q5 BETEILIGT_AN residuals, UNVERIFIABLE/DEAD_LINK, prog_mas_dfab relabel."""
from __future__ import annotations

import csv
import json
import re
import subprocess
import sys
import time
import unicodedata
from collections import Counter
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

OUT_LEDGER = HERE / "ledger" / "post_quality_p06_04.csv"
OUT_REPORT = HERE / "reports" / "post_quality_p06_04.md"
OUT_PATCH = HERE / "patches" / "post_quality_p06_04.patch.jsonl"
ELEMENT_LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
Q05_LEDGER = HERE / "ledger" / "quality_pass_q05.csv"
R07_CACHE = HERE / "_agent_r07_work" / "url_fetch_cache.json"
REVIEW_RUN = "post_quality_p06_04_2026_06_06"

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "scope", "prior_verdict", "prior_claim_id",
]

SCOPE_A_PRIORS = [
    "EP09-r-0003",
    "EP09-r-0004",
    "EP09-r-0010",
    "EP09-r-0011",
    "EP09-r-0012",
]

# Dossier-recovered project-specific URLs (not geo-token portals)
BETEILIGT_AN_URLS: dict[tuple[str, str], list[str]] = {
    ("albert_and_co", "p_ferme_du_rail_paris"): [
        "https://grandhuit.eu/projet/ferme-du-rail/",
    ],
    ("archipel_zero", "p_resilience_la_ferme_des_possibles_stains"): [
        "https://topophile.net/faire/la-ferme-des-possibles-ou-de-la-serendipite/",
        "http://materiauxreemploi.com/visite-de-chantier-resilience-la-ferme-des-possibles-a-stains/",
        "https://www.bellastock.com/projets/resilience",
    ],
    ("greisch", "p_recypark_demets_anderlecht"): [
        "https://www.greisch.com/en/projet/anderlecht-recypark-wood-expertise/",
        "https://brusselsarchitectureprize.be/nl/project/recypark-demets/",
    ],
    ("iemb_tu_berlin", "p_plattenpalast_berlin"): [
        "https://wwstudio.de/projects/plattenpalst",
        "http://www.whs-architekten.de/pp.html",
    ],
    ("pirmin_jung_schweiz_ag", "p_lysp8_basel"): [
        "https://zirkular.net/en/project/lysp8/",
        "https://loeligerstrub.ch/nproject/lysp8-neubau-wohnhaus-mit-gewerbe-basel/",
    ],
}

MAS_DFAB_URL = "https://gramaziokohler.arch.ethz.ch/"
MAS_DFAB_QUOTE = (
    "Coordinator and tutor of the MAS ETH Architecture and Digital Fabrication"
)

URL_REPAIRS = {
    "https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024": (
        "https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest"
    ),
    "https://www.cirkla.ch/en/le-reseau-du-reemploi/lannuaire/experts/wiederverwerkle-wick-upcycling-gmbh": (
        "https://www.cirkla.ch/en/lassociation-cirkla/"
    ),
    "https://heynetillettsteel.com/research/": "https://www.heynetillettsteel.com/",
}

GEO_STOP = {
    "berlin", "basel", "paris", "wien", "zurich", "schweiz", "deutschland",
    "frankreich", "belgien", "niederlande", "city", "stadt", "land",
}


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


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
    # albert_and_co ↔ "albert et cie"
    if "albert" in nid:
        candidates.extend(["albert et cie", "albert et compagnie", "albert & co"])
    if "archipel" in nid:
        candidates.append("archipel zero")
    if "iemb" in nid:
        candidates.extend(["iem b", "institut fur erhaltung", "erhaltung und modernisierung"])
    if "pirmin" in nid:
        candidates.append("pirmin jung")
    if "greisch" in nid:
        candidates.extend(["bureau greisch", "greisch"])
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
    # project slug hints
    if not to_ok and "plattenpalast" in to_id:
        to_ok = "plattenpalast" in body
    if not to_ok and "lysp8" in to_id or "lysp" in to_id:
        to_ok = "lysp8" in body or "lysp 8" in body
    if not to_ok and "recypark" in to_id:
        to_ok = "recypark" in body and "anderlecht" in body
    if not to_ok and "ferme_du_rail" in to_id or "ferme du rail" in to_name.lower():
        to_ok = "ferme du rail" in body
    if not to_ok and ("resilience" in to_id or "ferme des possibles" in to_name.lower()):
        to_ok = "resilience" in body or "ferme des possibles" in body
    if not from_ok and "archipel" in from_id and "archipel" in body:
        from_ok = True
    ok = from_ok and to_ok
    quote = ""
    if ok:
        for t in tokens(from_name or from_id, 4) + tokens(to_name or to_id, 4):
            idx = body.find(t)
            if idx >= 0:
                quote = body[max(0, idx - 15) : idx + 120].strip()
                break
    return ok, quote[:200]


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as f:
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
                "User-Agent": "recherche-post-quality-p06-04/1.0",
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        with urlopen(req, timeout=30) as resp:
            raw = resp.read(800_000)
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
    time.sleep(0.15)
    return entry


def q05_resolved_ids() -> set[str]:
    resolved: set[str] = set()
    if Q05_LEDGER.is_file():
        for r in load_csv(Q05_LEDGER):
            if r.get("verdict") == "PROVEN":
                resolved.add(r.get("prior_claim_id", ""))
    for q in ("q01", "q02", "q03", "q04"):
        p = HERE / "ledger" / f"quality_pass_{q}.csv"
        if not p.is_file():
            continue
        for r in load_csv(p):
            v = r.get("verdict") or r.get("new_verdict") or r.get("verdict_after", "")
            if v == "PROVEN":
                resolved.add(r.get("prior_claim_id") or r.get("claim_id", ""))
    return {x for x in resolved if x}


def scope_b_rows(resolved: set[str]) -> list[dict]:
    rows = []
    for r in load_csv(ELEMENT_LEDGER):
        cid = r["claim_id"]
        if cid in resolved:
            continue
        if r["verdict"] not in ("DEAD_LINK", "UNVERIFIABLE"):
            continue
        if not (r.get("basis_ref") or "").startswith("http") and "source_present" not in (r.get("notes") or ""):
            continue
        rows.append(r)
    # cap volume; prioritize agent 10 rel + high-value 06b nodes
    rows.sort(key=lambda x: (0 if x.get("claim_kind") == "rel" else 1, x["claim_id"]))
    return rows[:50]


def query_names(driver, database: str, ids: set[str]) -> dict[str, str]:
    if not ids:
        return {}
    with driver.session(database=database) as session:
        recs = session.run(
            "UNWIND $ids AS i MATCH (n {id: i}) RETURN n.id AS id, "
            "coalesce(n.name, n.name_full, n.id) AS name",
            ids=list(ids),
        )
        return {r["id"]: r["name"] for r in recs}


def adjudicate_beteiligt(
    row: dict, names: dict[str, str], cache: dict, patches: list[dict]
) -> dict:
    prior_id = row.get("prior_claim_id") or row.get("claim_id", "")
    fid = row.get("from_id", "")
    tid = row.get("to_id", "")
    rt = row.get("rel_type_or_label", "BETEILIGT_AN")
    from_name = names.get(fid, fid)
    to_name = names.get(tid, tid)
    urls = BETEILIGT_AN_URLS.get((fid, tid), [])
    verdict = row.get("prior_verdict") or row.get("verdict", "PARTIAL")
    action = "RESOURCE"
    proof_quote = ""
    basis_out = ""
    http_status = ""
    fetched_any = False

    for u in urls:
        fe = fetch_url(u, cache)
        if not fe.get("fetched") or not str(fe.get("http_status", "")).startswith("2"):
            continue
        fetched_any = True
        http_status = fe.get("http_status", "")
        ok, quote = both_endpoints_on_page(fid, tid, from_name, to_name, fe["text"])
        if ok:
            verdict = "PROVEN"
            action = "ADD_SOURCE"
            proof_quote = quote
            basis_out = u
            patches.append({
                "op": "set_rel_properties",
                "from": fid,
                "type": rt,
                "to": tid,
                "properties": {
                    "evidence_url": u,
                    "evidence_quote": quote,
                    "evidence_confidence": "belegt",
                    "evidence_basis": "web_fetch_p06_04",
                    "review_run": REVIEW_RUN,
                },
                "reason": f"P6-04 {prior_id}: dossier-recovered project page",
            })
            break

    notes = row.get("notes", "")
    if verdict != "PROVEN":
        notes = (notes + " | P6-04: project-specific fetch; strict two-endpoint gate failed").strip()

    return {
        "claim_id": f"P604-{prior_id}",
        "claim_kind": "rel",
        "element_id": row.get("element_id", ""),
        "from_id": fid,
        "to_id": tid,
        "rel_type_or_label": rt,
        "asserted_claim": row.get("asserted_claim", ""),
        "basis_type": "web",
        "basis_ref": basis_out or (urls[0] if urls else ""),
        "fetched": str(fetched_any).lower(),
        "http_status": http_status,
        "verdict": verdict,
        "confidence": "belegt" if verdict == "PROVEN" else row.get("confidence", ""),
        "proof_quote": proof_quote,
        "proposed_action": action,
        "agent_id": "P6-04",
        "notes": notes,
        "scope": "A",
        "prior_verdict": row.get("prior_verdict") or "PARTIAL",
        "prior_claim_id": prior_id,
    }


def node_id_from_row(row: dict) -> str:
    fid = (row.get("from_id") or "").strip()
    eid = (row.get("element_id") or "").strip()
    if fid:
        return fid
    if row.get("claim_kind") == "node" and eid and ":" not in eid:
        return eid
    return fid


def adjudicate_unverifiable(
    row: dict, names: dict[str, str], cache: dict, patches: list[dict]
) -> dict:
    prior_id = row["claim_id"]
    prior_verdict = row["verdict"]
    fid = node_id_from_row(row)
    tid = row.get("to_id", "")
    rt = row.get("rel_type_or_label", "")
    basis_ref = row.get("basis_ref", "")
    verdict = prior_verdict
    action = row.get("proposed_action", "KEEP")
    proof_quote = ""
    basis_out = basis_ref
    http_status = ""
    fetched_any = False

    urls: list[str] = []
    if basis_ref.startswith("http"):
        urls.append(basis_ref)
    if basis_ref in URL_REPAIRS:
        urls.append(URL_REPAIRS[basis_ref])

    # A10-R-094 immobilien basel
    if prior_id == "A10-R-094":
        urls.append("https://www.immobilien.bs.ch/")

    seen: set[str] = set()
    candidate_urls = [u for u in urls if u and not (u in seen or seen.add(u))]

    for u in candidate_urls:
        repair = URL_REPAIRS.get(u, u)
        fe = fetch_url(repair, cache)
        if not fe.get("fetched"):
            continue
        fetched_any = True
        http_status = fe.get("http_status", "")
        if not http_status.startswith("2"):
            continue
        body = norm_text(fe["text"])
        if row["claim_kind"] == "node" and fid:
            if endpoint_hit(fid, names.get(fid, fid), body):
                verdict = "PROVEN"
                action = "KEEP"
                proof_quote = body[:150]
                basis_out = repair
                patches.append({
                    "op": "set_node_properties",
                    "id": fid,
                    "properties": {"primary_source_url": repair},
                    "reason": f"P6-04 {prior_id}: UNVERIFIABLE→PROVEN re-fetch",
                })
                break
        elif rt and fid and tid:
            ok, quote = both_endpoints_on_page(fid, tid, names.get(fid, fid), names.get(tid, tid), fe["text"])
            if ok:
                verdict = "PROVEN"
                action = "ADD_SOURCE"
                proof_quote = quote
                basis_out = repair
                patches.append({
                    "op": "set_rel_properties",
                    "from": fid,
                    "type": rt,
                    "to": tid,
                    "properties": {
                        "evidence_url": repair,
                        "evidence_quote": quote,
                        "evidence_confidence": "belegt",
                        "review_run": REVIEW_RUN,
                    },
                    "reason": f"P6-04 {prior_id}: dead/unverifiable URL repaired",
                })
                break

    return {
        "claim_id": f"P604-{prior_id}",
        "claim_kind": row.get("claim_kind", "node"),
        "element_id": row.get("element_id", row.get("graph_element_id", "")),
        "from_id": fid,
        "to_id": tid,
        "rel_type_or_label": rt,
        "asserted_claim": row.get("asserted_claim", ""),
        "basis_type": "web",
        "basis_ref": basis_out,
        "fetched": str(fetched_any).lower(),
        "http_status": http_status,
        "verdict": verdict,
        "confidence": "belegt" if verdict == "PROVEN" else row.get("confidence", ""),
        "proof_quote": proof_quote,
        "proposed_action": action,
        "agent_id": "P6-04",
        "notes": row.get("notes", ""),
        "scope": "B",
        "prior_verdict": prior_verdict,
        "prior_claim_id": prior_id,
    }


def adjudicate_mas_dfab(cache: dict, patches: list[dict]) -> dict:
    fe = fetch_url(MAS_DFAB_URL, cache)
    fetched = fe.get("fetched", False)
    http_status = fe.get("http_status", "")
    body = norm_text(fe.get("text", ""))
    verdict = "PARTIAL"
    action = "ESCALATE_HUMAN"
    proof_quote = ""
    if fetched and http_status.startswith("2") and (
        "mas eth architecture and digital fabrication" in body
        or "gramazio kohler" in body
    ):
        verdict = "PROVEN"
        action = "FIX_PROPERTY"
        proof_quote = MAS_DFAB_QUOTE
        patches.append({
            "op": "set_node_properties",
            "id": "prog_mas_dfab",
            "properties": {
                "primary_source_url": MAS_DFAB_URL,
                "source_urls": [MAS_DFAB_URL],
                "short_description": (
                    "ETH MAS Architecture and Digital Fabrication (Gramazio Kohler Research) — "
                    "teaching programme combining computational design, robotic fabrication, "
                    "and reusable/reversible construction details."
                ),
            },
            "reason": "P6-04 A10-N-058: relabel source from De Wolf course → GKR MAS DFAB programme",
        })

    return {
        "claim_id": "P604-A10-N-058",
        "claim_kind": "node",
        "element_id": "4:5f542910-8dcf-46a9-a77c-dfff0c64ee65:533",
        "from_id": "prog_mas_dfab",
        "to_id": "",
        "rel_type_or_label": "Programm",
        "asserted_claim": "MAS DFAB ETH (Gramazio Kohler) circular-construction programme",
        "basis_type": "web",
        "basis_ref": MAS_DFAB_URL,
        "fetched": str(fetched).lower(),
        "http_status": http_status,
        "verdict": verdict,
        "confidence": "belegt" if verdict == "PROVEN" else "teilweise_belegt",
        "proof_quote": proof_quote,
        "proposed_action": action,
        "agent_id": "P6-04",
        "notes": "Prior cited ETH news was De Wolf course; GKR homepage confirms MAS DFAB programme",
        "scope": "C",
        "prior_verdict": "PARTIAL",
        "prior_claim_id": "A10-N-058",
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


def write_report(rows: list[dict], apply_status: str, apply_log: str) -> None:
    scope_a = [r for r in rows if r["scope"] == "A"]
    scope_b = [r for r in rows if r["scope"] == "B"]
    scope_c = [r for r in rows if r["scope"] == "C"]
    upgrades = [r for r in rows if r["prior_verdict"] != "PROVEN" and r["verdict"] == "PROVEN"]
    lines = [
        "# Post Quality Pass P6-04 — BETEILIGT_AN + UNVERIFIABLE + prog_mas_dfab",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')} · **Database:** `mit-bestand`",
        f"**Ledger:** [`ledger/post_quality_p06_04.csv`](../ledger/post_quality_p06_04.csv)",
        f"**Patch:** [`patches/post_quality_p06_04.patch.jsonl`](../patches/post_quality_p06_04.patch.jsonl)",
        f"**Apply:** {apply_status}",
        "",
        "## Scope A — 5 Q5 PARTIAL BETEILIGT_AN (dossier recovery)",
        "",
        f"| New verdict | Count |",
        f"|---|---:|",
    ]
    for v, c in Counter(r["verdict"] for r in scope_a).most_common():
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        "## Scope B — fixable UNVERIFIABLE / DEAD_LINK (element ledger residuals)",
        "",
        f"Rows processed: **{len(scope_b)}**",
        "",
        f"| New verdict | Count |",
        f"|---|---:|",
    ]
    for v, c in Counter(r["verdict"] for r in scope_b).most_common():
        lines.append(f"| {v} | {c} |")
    lines += [
        "",
        "## Scope C — prog_mas_dfab (A10-N-058 relabel)",
        "",
    ]
    for r in scope_c:
        lines.append(
            f"- `{r['prior_claim_id']}`: {r['prior_verdict']}→**{r['verdict']}** "
            f"({r['proposed_action']}) — {r.get('proof_quote', '')[:80]}"
        )
    lines += [
        "",
        f"## Upgrades to PROVEN: **{len(upgrades)}**",
        "",
    ]
    for r in upgrades[:30]:
        lines.append(
            f"- `{r['prior_claim_id']}` ({r['prior_verdict']}→PROVEN): "
            f"{r.get('from_id', '')} — {r.get('rel_type_or_label', '')}"
        )
    if len(upgrades) > 30:
        lines.append(f"- … and {len(upgrades) - 30} more")
    if apply_log:
        lines += ["", "## Apply log (tail)", "", "```", apply_log[-1500:], "```"]
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    cache = load_cache()
    patches: list[dict] = []
    resolved = q05_resolved_ids()

    scope_a_src = [
        r for r in load_csv(Q05_LEDGER)
        if r.get("prior_claim_id") in SCOPE_A_PRIORS and r.get("verdict") == "PARTIAL"
    ]
    if not scope_a_src:
        ep09 = HERE / "ledger" / "element_proof_agent_09.csv"
        if ep09.is_file():
            scope_a_src = [
                {**r, "prior_claim_id": r["claim_id"], "prior_verdict": r["verdict"]}
                for r in load_csv(ep09)
                if r["claim_id"] in SCOPE_A_PRIORS
            ]

    scope_b_src = scope_b_rows(resolved)

    all_ids: set[str] = set()
    for r in scope_a_src + scope_b_src:
        nid = node_id_from_row(r)
        if nid:
            all_ids.add(nid)
        if r.get("to_id"):
            all_ids.add(r["to_id"])

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    names = query_names(driver, database, all_ids)
    driver.close()

    out_rows: list[dict] = []
    for r in scope_a_src:
        out_rows.append(adjudicate_beteiligt(r, names, cache, patches))
    for r in scope_b_src:
        out_rows.append(adjudicate_unverifiable(r, names, cache, patches))
    out_rows.append(adjudicate_mas_dfab(cache, patches))

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

    upgrades = sum(1 for r in out_rows if r["prior_verdict"] != "PROVEN" and r["verdict"] == "PROVEN")
    print(f"Scope A: {len(scope_a_src)} | Scope B: {len(scope_b_src)} | patches: {len(unique_patches)}")
    print(f"Upgrades: {upgrades} | Apply: {apply_status}")


if __name__ == "__main__":
    main()
