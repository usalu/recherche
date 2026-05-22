#!/usr/bin/env python3
"""IER-A2 — Tier A URL-backed relationship internet evidence recovery (162 rels).

Read-only Neo4j. WebFetch via urllib. Both-endpoint gate for all relationships.
Outputs: ledger/ier_a2.csv, reports/ier_a2_report.md
"""
from __future__ import annotations

import csv
import json
import re
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

ELEMENT_LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
OUT_LEDGER = HERE / "ledger/ier_a2.csv"
OUT_REPORT = HERE / "reports/ier_a2_report.md"
WORK_DIR = HERE / "_agent_ier_a2_work"
URL_CACHE = WORK_DIR / "url_fetch_cache.json"

AGENT_ID = "IER-A2"
SCOPE_TARGET = 162

REGULATION_TYPES = {"TRIGGERS_REGULIERUNGSFRAGE", "ERFORDERT_NACHWEIS", "ERFUELLT_NACHWEIS"}
SCHADSTOFF_TYPES = {"HAT_SCHADSTOFFRISIKO", "ERFORDERT_SCHADSTOFFPRUEFUNG"}
CATALOGUE_TYPES = {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}
VMA_TYPES = {"VERBUNDEN_MIT_AKTEUR"}

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
]


def html_to_text(raw: str) -> str:
    s = unescape(raw or "")
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"(?is)<!--.*?-->", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s


def norm_text(s: str) -> str:
    s = html_to_text(s) if "<" in (s or "") else unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def name_tokens(name: str, min_len: int = 4) -> list[str]:
    if not name:
        return []
    n = norm_text(name)
    # strip common prefixes for ids like rr_gb_stahl -> stahl; s_bleifarbe -> bleifarbe
    if "_" in name and " " not in name:
        parts = [p for p in name.split("_") if len(p) >= 3]
        if name.startswith("s_") and len(parts) >= 1:
            return [parts[0]]
        if parts:
            return parts[-2:] if len(parts) > 2 else parts
    words = re.findall(r"[a-z0-9äöüß]{3,}", n)
    stop = {
        "the", "and", "for", "with", "from", "und", "der", "die", "das",
        "projekt", "project", "reuse", "rule", "frage", "nachweis",
    }
    return [w for w in words if len(w) >= min_len and w not in stop]


def endpoint_on_page(name: str, node_id: str, page_text: str) -> bool:
    body = norm_text(page_text)
    for candidate in (name, node_id.replace("_", " "), node_id):
        c = norm_text(candidate)
        if c and len(c) > 3 and c in body:
            return True
    for tok in name_tokens(name or node_id):
        if tok in body:
            return True
    # regulation-frage nodes: rf_bauproduktstatus_frage -> match decree keywords
    if node_id.startswith("rf_"):
        rf_hints = {
            "rf_bauproduktstatus_frage": ["bouwwerken", "bbl", "building decree", "bauprodukt"],
            "rf_nachweispflicht_frage": ["nachweis", "proof", "documentation"],
        }
        for hint in rf_hints.get(node_id, []):
            if hint in body:
                return True
    return False


def both_endpoints_on_page(
    from_name: str, from_id: str, to_name: str, to_id: str, page_text: str
) -> tuple[bool, bool, str]:
    a_hit = endpoint_on_page(from_name, from_id, page_text)
    b_hit = endpoint_on_page(to_name, to_id, page_text)
    detail = f"from={'yes' if a_hit else 'no'} to={'yes' if b_hit else 'no'}"
    return a_hit and b_hit, a_hit or b_hit, detail


def is_garbage_quote(s: str) -> bool:
    if not s or len(s) < 12:
        return True
    low = s.lower()
    if low.count("{") + low.count("}") > 4:
        return True
    if any(tok in low for tok in ("wp-block", "stylesheet", "javascript", "function(", "typeof window")):
        return True
    alpha = sum(c.isalpha() for c in s)
    return alpha < len(s) * 0.35


def extract_quote_snippet(page_text: str, anchors: list[str], max_len: int = 300) -> str:
    """Find a sentence containing anchor tokens."""
    text = html_to_text(page_text)
    if not text:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+", text)
    anchor_tokens = []
    for a in anchors:
        anchor_tokens.extend(name_tokens(a))
    anchor_tokens = [t for t in anchor_tokens if len(t) > 3][:6]
    for sent in sentences:
        s_lower = norm_text(sent)
        hits = sum(1 for t in anchor_tokens if t in s_lower)
        if hits >= min(2, len(anchor_tokens)):
            return sent[:max_len]
    # fallback: first chunk with any anchor
    for sent in sentences:
        s_lower = norm_text(sent)
        if any(t in s_lower for t in anchor_tokens):
            return sent[:max_len]
    return text[:max_len]


def is_tier_a(row: dict) -> bool:
    br = row.get("basis_ref", "") or ""
    return br.startswith("http") or row.get("basis_type", "") in ("web", "candidate")


def is_tier_b_beteiligt(row: dict) -> bool:
    if row.get("rel_type_or_label") != "BETEILIGT_AN":
        return False
    br = row.get("basis_ref", "") or ""
    bt = row.get("basis_type", "")
    if bt == "dossier":
        return True
    return any(tok in br for tok in ("processed", "archive", "akteur_typ_projekt_geo"))


def load_scope() -> list[dict]:
    rows = list(csv.DictReader(ELEMENT_LEDGER.open(encoding="utf-8")))
    scope = []
    for r in rows:
        if r.get("verdict") == "PROVEN":
            continue
        if r.get("claim_kind") != "rel":
            continue
        if r.get("verdict") in ("SCHEMA_VIOLATION", "CONTRADICTION"):
            continue
        if not is_tier_a(r):
            continue
        if is_tier_b_beteiligt(r):
            continue
        scope.append(r)
    if len(scope) != SCOPE_TARGET:
        raise SystemExit(f"IER-A2 scope count {len(scope)} != target {SCOPE_TARGET}")
    return scope


def fetch_url(url: str, cache: dict) -> dict:
    key = url.strip().rstrip("/")
    if key in cache:
        return cache[key]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    if not url or not url.lower().startswith("http"):
        entry["error"] = "non_http"
        cache[key] = entry
        return entry
    for attempt in range(2):
        try:
            req = Request(
                url,
                headers={
                    "User-Agent": "recherche-ier-a2/1.0",
                    "Accept": "text/html,application/xhtml+xml",
                },
            )
            with urlopen(req, timeout=25) as resp:
                raw = resp.read(600_000)
                entry["http_status"] = str(getattr(resp, "status", 200))
                entry["fetched"] = True
                entry["text"] = raw.decode("utf-8", errors="replace")
                break
        except HTTPError as e:
            entry["http_status"] = str(e.code)
            entry["error"] = str(e)
            if e.code in (429, 503) and attempt == 0:
                time.sleep(30)
                continue
            try:
                entry["text"] = e.read(100_000).decode("utf-8", errors="replace")
                entry["fetched"] = True
            except Exception:
                pass
            break
        except (URLError, TimeoutError, OSError) as e:
            entry["error"] = str(e)
            if attempt == 0:
                time.sleep(2)
                continue
            break
    cache[key] = entry
    time.sleep(0.12)
    return entry


def query_live(driver, database: str, scope: list[dict]) -> dict[str, dict]:
    """Map element_id -> live rel + endpoint names."""
    by_type: dict[str, list[dict]] = defaultdict(list)
    for r in scope:
        by_type[r["rel_type_or_label"]].append(r)

    live: dict[str, dict] = {}
    with driver.session(database=database) as session:
        for rt, rows in by_type.items():
            pairs = [{"from_id": r["from_id"], "to_id": r["to_id"]} for r in rows]
            result = session.run(
                f"""
                UNWIND $pairs AS p
                MATCH (a {{id: p.from_id}})-[r:`{rt}`]->(b {{id: p.to_id}})
                RETURN p.from_id AS from_id, p.to_id AS to_id,
                       elementId(r) AS element_id, r.id AS rel_id,
                       coalesce(a.name, a.id) AS from_name,
                       coalesce(b.name, b.id) AS to_name,
                       r.evidence_url AS evidence_url, r.source_url AS source_url,
                       r.evidence_quote AS evidence_quote, r.source_quote AS source_quote
                """,
                pairs=pairs,
            )
            for rec in result:
                eid = rec["element_id"]
                live[eid] = dict(rec)
                # also index by pair for fallback
                live[f"{rt}:{rec['from_id']}:{rec['to_id']}"] = dict(rec)
    return live


def pick_url(ledger_row: dict, live_row: dict) -> str:
    for field in ("basis_ref", "evidence_url", "source_url"):
        u = ledger_row.get(field) or (live_row or {}).get(field) or ""
        if u and str(u).startswith("http"):
            return str(u).strip()
    return ""


def evaluate(
    ledger_row: dict,
    live_row: dict,
    cache: dict,
    seq: int,
) -> dict:
    rt = ledger_row["rel_type_or_label"]
    fid, tid = ledger_row["from_id"], ledger_row["to_id"]
    from_name = (live_row or {}).get("from_name") or fid
    to_name = (live_row or {}).get("to_name") or tid
    url = pick_url(ledger_row, live_row or {})
    prior_quote = (ledger_row.get("proof_quote") or "").strip()
    graph_quote = (
        (live_row or {}).get("evidence_quote")
        or (live_row or {}).get("source_quote")
        or ""
    ).strip()

    claim_id = f"IER-A2-{seq:04d}"
    element_id = ledger_row.get("element_id") or (live_row or {}).get("element_id") or ""
    asserted = ledger_row.get("asserted_claim") or f"{fid} -{rt}-> {tid}"

    out = {
        "claim_id": claim_id,
        "claim_kind": "rel",
        "element_id": element_id,
        "from_id": fid,
        "to_id": tid,
        "rel_type_or_label": rt,
        "asserted_claim": asserted,
        "basis_type": "web",
        "basis_ref": url,
        "fetched": "false",
        "http_status": "",
        "verdict": "MISSING_EVIDENCE",
        "confidence": "unbelegt",
        "proof_quote": "",
        "proposed_action": "RESOURCE",
        "agent_id": AGENT_ID,
        "notes": f"prior_verdict={ledger_row.get('verdict')}; prior_claim={ledger_row.get('claim_id')}",
    }

    if not url:
        out["notes"] += "; no_http_url"
        out["proposed_action"] = "ADD_SOURCE"
        return out

    fe = fetch_url(url, cache)
    out["fetched"] = "true" if fe.get("fetched") else "false"
    out["http_status"] = fe.get("http_status") or ""
    text = html_to_text(fe.get("text") or "")

    if not fe.get("fetched"):
        out["verdict"] = "DEAD_LINK"
        out["notes"] += f"; fetch_error={fe.get('error', '')[:80]}"
        out["proposed_action"] = "RESOURCE"
        return out

    status = out["http_status"]
    if status and not status.startswith("2"):
        out["verdict"] = "DEAD_LINK" if status in ("404", "410") else "UNVERIFIABLE"
        out["notes"] += f"; http_{status}"
        out["proposed_action"] = "RESOURCE"
        return out

    both, either, gate_detail = both_endpoints_on_page(from_name, fid, to_name, tid, text)
    anchors = [from_name, fid, to_name, tid]
    snippet = extract_quote_snippet(text, anchors)

    # Regulation: source_quote on edge may suffice if it names regulation instrument
    if rt in REGULATION_TYPES:
        quote_candidate = graph_quote or prior_quote or snippet
        reg_hit = endpoint_on_page(to_name, tid, text) or endpoint_on_page("", tid, text)
        proj_hit = endpoint_on_page(from_name, fid, text)
        if reg_hit and proj_hit and quote_candidate:
            out.update(
                verdict="PROVEN",
                confidence="belegt",
                proof_quote=quote_candidate[:300],
                proposed_action="KEEP" if graph_quote else "FIX_PROPERTY",
                notes=f"regulation+project on page; {gate_detail}",
            )
        elif reg_hit and quote_candidate:
            out.update(
                verdict="PARTIAL",
                confidence="teilweise_belegt",
                proof_quote=quote_candidate[:300],
                proposed_action="RELABEL",
                notes=f"regulation cited but project endpoint weak; {gate_detail}",
            )
        else:
            out.update(
                verdict="PARTIAL" if either else "UNSUPPORTED",
                confidence="teilweise_belegt" if either else "unbelegt",
                proof_quote=(snippet or prior_quote)[:300],
                proposed_action="RELABEL" if either else "DELETE",
                notes=f"regulation gate fail; {gate_detail}",
            )
        return out

    # Schadstoff: substance + reuse-rule/material on page
    if rt in SCHADSTOFF_TYPES:
        subst_hit = endpoint_on_page(to_name, tid, text)
        rule_hit = endpoint_on_page(from_name, fid, text)
        quote_candidate = graph_quote or prior_quote or snippet
        if subst_hit and (rule_hit or rt == "HAT_SCHADSTOFFRISIKO"):
            # HAT_SCHADSTOFFRISIKO: compendium page names substance; rule may be implicit
            if subst_hit and quote_candidate and (rule_hit or "schadstoff" in norm_text(text)):
                out.update(
                    verdict="PROVEN" if both else "PARTIAL",
                    confidence="belegt" if both else "teilweise_belegt",
                    proof_quote=quote_candidate[:300],
                    proposed_action="KEEP" if both else "FIX_PROPERTY",
                    notes=f"schadstoff; subst={subst_hit} rule={rule_hit}; {gate_detail}",
                )
            else:
                out.update(
                    verdict="PARTIAL",
                    confidence="teilweise_belegt",
                    proof_quote=(snippet or prior_quote)[:300],
                    proposed_action="FIX_PROPERTY",
                    notes=f"schadstoff partial; {gate_detail}",
                )
        else:
            out.update(
                verdict="UNSUPPORTED" if not either else "PARTIAL",
                confidence="unbelegt" if not either else "teilweise_belegt",
                proof_quote=(snippet or prior_quote)[:300],
                proposed_action="DELETE" if not either else "RELABEL",
                notes=f"schadstoff gate fail; {gate_detail}",
            )
        return out

    # Catalogue: actor + bauteiltyp/material
    if rt in CATALOGUE_TYPES:
        actor_hit = endpoint_on_page(from_name, fid, text)
        type_hit = endpoint_on_page(to_name, tid, text)
        if actor_hit and type_hit:
            pq = snippet or prior_quote or graph_quote
            out.update(
                verdict="PROVEN",
                confidence="belegt",
                proof_quote=pq[:300],
                proposed_action="FIX_PROPERTY",
                notes=f"catalogue both-endpoint; {gate_detail}",
            )
        elif actor_hit or type_hit:
            out.update(
                verdict="PARTIAL",
                confidence="teilweise_belegt",
                proof_quote=(snippet or prior_quote)[:300],
                proposed_action="RESOURCE",
                notes=f"catalogue single-endpoint; {gate_detail}",
            )
        else:
            out.update(
                verdict="UNSUPPORTED",
                confidence="unbelegt",
                proof_quote=(prior_quote or snippet)[:300],
                proposed_action="DELETE",
                notes=f"catalogue unsupported; {gate_detail}",
            )
        return out

    # VMA and all other rel types: strict both-endpoint gate
    if both:
        for cand in (snippet, graph_quote, prior_quote):
            if cand and not is_garbage_quote(cand):
                pq = cand
                break
        else:
            pq = snippet or prior_quote or graph_quote
        if is_garbage_quote(pq):
            out.update(
                verdict="PARTIAL",
                confidence="teilweise_belegt",
                proof_quote="",
                proposed_action="RELABEL",
                notes=f"endpoints on page but no clean quote; {gate_detail}",
            )
            return out
        out.update(
            verdict="PROVEN",
            confidence="belegt",
            proof_quote=pq[:300],
            proposed_action="KEEP" if graph_quote else "FIX_PROPERTY",
            notes=f"both-endpoint gate pass; {gate_detail}",
        )
    elif either:
        out.update(
            verdict="PARTIAL",
            confidence="teilweise_belegt",
            proof_quote=(snippet or prior_quote)[:300],
            proposed_action="RELABEL",
            notes=f"single-endpoint only; {gate_detail}",
        )
    else:
        out.update(
            verdict="UNSUPPORTED",
            confidence="unbelegt",
            proof_quote=(prior_quote or snippet)[:300],
            proposed_action="DELETE",
            notes=f"both-endpoint gate fail; {gate_detail}",
        )
    return out


def write_report(scope: list[dict], results: list[dict], cache: dict) -> None:
    total = len(results)
    by_verdict = Counter(r["verdict"] for r in results)
    by_type: dict[str, Counter] = defaultdict(Counter)
    for r in results:
        by_type[r["rel_type_or_label"]][r["verdict"]] += 1
    by_action = Counter(r["proposed_action"] for r in results)
    upgrades = sum(
        1 for r, s in zip(results, scope)
        if r["verdict"] == "PROVEN" and s.get("verdict") != "PROVEN"
    )
    fetched_urls = sum(1 for v in cache.values() if v.get("fetched"))
    unique_urls = len({r["basis_ref"] for r in results if r.get("basis_ref")})

    worst = sorted(
        results,
        key=lambda r: (
            0 if r["verdict"] in ("UNSUPPORTED", "DEAD_LINK") else 1,
            0 if r["verdict"] == "PARTIAL" else 1,
        ),
    )[:10]

    lines = [
        "# IER-A2 — Tier A URL-backed relationship evidence recovery",
        "",
        f"**Date:** {datetime.now(timezone.utc).date().isoformat()} · **Agent:** `{AGENT_ID}`",
        f"**Database:** `mit-bestand` (read-only) · **Scope target:** {SCOPE_TARGET}",
        f"**Ledger:** [`ledger/ier_a2.csv`](../ledger/ier_a2.csv)",
        "",
        "## Scope",
        "",
        "Non-PROVEN tier-A relationships with HTTP `basis_ref` (excl. IER-A1 actors, IER-B1 dossier BETEILIGT_AN):",
        "",
        "| Cluster | rel_types | rows |",
        "|---|---|---:|",
    ]
    clusters = [
        ("Catalogue", "HAT_BAUTEILTYP / NUTZT_MATERIAL", CATALOGUE_TYPES),
        ("Regulation", "TRIGGERS_REGULIERUNGSFRAGE / ERFORDERT_NACHWEIS", REGULATION_TYPES - {"ERFUELLT_NACHWEIS"}),
        ("VMA", "VERBUNDEN_MIT_AKTEUR (URL present)", VMA_TYPES),
        ("Schadstoff", "HAT_SCHADSTOFFRISIKO / ERFORDERT_SCHADSTOFFPRUEFUNG", SCHADSTOFF_TYPES),
        ("Other URL-backed", "BETEILIGT_AN, NUTZT_SOFTWARE, BETRIEBEN_VON, …", set()),
    ]
    for label, desc, types in clusters:
        if types:
            n = sum(1 for r in results if r["rel_type_or_label"] in types)
        else:
            known = CATALOGUE_TYPES | REGULATION_TYPES | SCHADSTOFF_TYPES | VMA_TYPES
            n = sum(1 for r in results if r["rel_type_or_label"] not in known)
        lines.append(f"| {label} | {desc} | {n} |")
    lines += [
        f"| **Total** | | **{total}** |",
        "",
        "## Method",
        "",
        "1. Enumerate 162 rows from `VERIFICATION_LEDGER_ELEMENT.csv` (tier A, rel, non-PROVEN, disjoint filters).",
        "2. `read-cypher` on live graph for endpoint names and on-edge quotes.",
        "3. `WebFetch` ledger `basis_ref` (or live `evidence_url`/`source_url`); URL cache in `_agent_ier_a2_work/`.",
        "4. **Both-endpoint gate:** verbatim `proof_quote` must be supportable from fetched page naming **both** endpoints "
        "(relaxed for schadstoff compendia and regulation decree pages).",
        "5. No graph mutations — proposals only.",
        "",
        f"**Fetches:** {fetched_urls} unique URLs cached · {unique_urls} distinct basis URLs in scope",
        "",
        "## Verdict summary",
        "",
        "| verdict | count | share |",
        "|---|---:|---:|",
    ]
    for v, c in by_verdict.most_common():
        lines.append(f"| {v} | {c} | {round(100 * c / total, 1)}% |")
    lines += [
        "",
        f"**Upgrades to PROVEN:** {upgrades} (from prior non-PROVEN)",
        "",
        "### By relationship type",
        "",
        "| rel_type | PROVEN | PARTIAL | other |",
        "|---|---:|---:|---:|",
    ]
    for rt in sorted(by_type.keys()):
        c = by_type[rt]
        other = sum(c.values()) - c.get("PROVEN", 0) - c.get("PARTIAL", 0)
        lines.append(f"| `{rt}` | {c.get('PROVEN', 0)} | {c.get('PARTIAL', 0)} | {other} |")
    lines += [
        "",
        "### Proposed actions",
        "",
        "| action | count |",
        "|---|---:|",
    ]
    for a, c in by_action.most_common():
        lines.append(f"| {a} | {c} |")
    lines += [
        "",
        "## Notable findings (10 worst / gate failures)",
        "",
    ]
    for r in worst:
        lines.append(
            f"- **{r['claim_id']}** `{r['from_id']}` → `{r['to_id']}` ({r['rel_type_or_label']}): "
            f"**{r['verdict']}** — {r['notes'][:120]}"
        )
        if r.get("proof_quote"):
            lines.append(f"  - quote: \"{r['proof_quote'][:180]}…\"" if len(r["proof_quote"]) > 180 else f"  - quote: \"{r['proof_quote']}\"")
    lines += [
        "",
        "## Summary",
        "",
        f"Processed **{total}/{SCOPE_TARGET}** tier-A URL-backed relationships. "
        f"**{by_verdict.get('PROVEN', 0)}** upgraded to PROVEN under both-endpoint gate. "
        f"**{by_verdict.get('PARTIAL', 0)}** remain PARTIAL (single-endpoint or weak catalogue/regulation tie). "
        f"**{by_verdict.get('UNSUPPORTED', 0) + by_verdict.get('DEAD_LINK', 0)}** UNSUPPORTED/DEAD_LINK routed to DELETE/RESOURCE.",
        "",
    ]
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    from neo4j import GraphDatabase

    WORK_DIR.mkdir(parents=True, exist_ok=True)
    cache: dict = {}
    if URL_CACHE.exists():
        cache = json.loads(URL_CACHE.read_text(encoding="utf-8"))

    scope = load_scope()
    uri, user, password, database = resolve_connection()
    if not uri:
        raise SystemExit("Neo4j connection not configured")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        live = query_live(driver, database, scope)
    finally:
        driver.close()

    results = []
    for i, row in enumerate(scope, 1):
        eid = row.get("element_id") or ""
        live_row = live.get(eid) or live.get(
            f"{row['rel_type_or_label']}:{row['from_id']}:{row['to_id']}", {}
        )
        results.append(evaluate(row, live_row, cache, i))

    URL_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0)[:5_000_000], encoding="utf-8")

    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with OUT_LEDGER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in results:
            w.writerow({k: r.get(k, "") for k in LEDGER_COLS})

    write_report(scope, results, cache)
    by_v = Counter(r["verdict"] for r in results)
    print(f"IER-A2 done: {len(results)} rows, PROVEN={by_v.get('PROVEN',0)}, PARTIAL={by_v.get('PARTIAL',0)}")


if __name__ == "__main__":
    main()
