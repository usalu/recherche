"""Shared utilities for CEG 4-agent re-hunt."""

from __future__ import annotations

import csv
import json
import re
import sys
import urllib.parse
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
BG_WORK = REPO / "_neo4j/review/2026-06-06_full_graph_verification/_bg_hunt_work"
DOSSIER_ROOT = REPO / "_neo4j/processed/projects/records"

sys.path.insert(0, str(SCRIPTS))
import verify_clickable_evidence as ceg  # noqa: E402

csv.field_size_limit(10_000_000)
BASELINE = HERE / "CLICKABLE_EVIDENCE_BASELINE.csv"
BOT_BLOCKED = {"403", "401", "503", "429"}
BAD = {"QUOTE_MISMATCH", "HOMEPAGE_ONLY", "LINK_DEAD"}
REVIEW = {"LIKELY_REVIEW"}
STOP = ceg.STOP | {"reused", "neue", "alte", "funktion", "anzahl", "page", "accueil"}

AGENT_FILTERS: dict[str, callable] = {
    "CEG-R1": lambda r: r["kind"] == "rel" and r["type"] in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"},
    "CEG-R2": lambda r: r["kind"] == "rel" and r["type"] not in {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"},
    "CEG-R3": lambda r: r["kind"] == "node" and r["type"] == "Akteur",
    "CEG-R4": lambda r: r["kind"] == "node" and r["type"] != "Akteur",
}


def in_scope(row: dict) -> bool:
    st = row.get("evidence_status", "")
    if st in REVIEW:
        return True
    if st not in BAD:
        return False
    if st == "LINK_DEAD" and row.get("http_status", "") in BOT_BLOCKED:
        return False
    return True


def load_scope(agent_id: str) -> list[dict]:
    filt = AGENT_FILTERS[agent_id]
    return [r for r in csv.DictReader(BASELINE.open(encoding="utf-8")) if in_scope(r) and filt(r)]


def quote_terms(quote: str, n: int = 8) -> list[str]:
    words = [w for w in re.findall(r"[a-zaeoeue0-9]{5,}", ceg.norm(quote)) if w not in STOP]
    seen, out = set(), []
    for w in words:
        if w not in seen:
            seen.add(w)
            out.append(w)
        if len(out) >= n:
            break
    return out


def ddg_results(query: str, cache: dict, limit: int = 8) -> list[str]:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    ent = ceg.fetch(url, cache)
    text = ent.get("norm", "")
    out: list[str] = []
    for m in re.finditer(r"uddg=([^&\"]+)", text):
        try:
            cand = urllib.parse.unquote(m.group(1))
        except Exception:  # noqa: BLE001
            continue
        if cand.startswith("http") and cand not in out:
            out.append(cand)
        if len(out) >= limit:
            break
    return out


def split_sentences(norm_text: str) -> list[str]:
    if not norm_text:
        return []
    parts = re.split(r"(?<=[.!?])\s+|\s*\|\s*|\s{2,}", norm_text)
    return [p.strip() for p in parts if len(p.strip()) >= 20]


def extract_on_page_quote(pn: str, anchors: list[str], terms: list[str]) -> tuple[str, float]:
    """Pick best verbatim sentence from normalized page text."""
    anchor_toks = [ceg.norm(a) for a in anchors if a and len(ceg.norm(a)) >= 4]
    anchor_toks = [a for a in anchor_toks if a not in STOP]
    cand_terms = list(dict.fromkeys(anchor_toks + terms))[:12]
    if not cand_terms:
        return "", 0.0
    best_sent, best_score = "", 0.0
    for sent in split_sentences(pn):
        if len(sent) > 400:
            continue
        alpha = re.findall(r"[a-zaeoeue]{4,}", sent)
        if len(alpha) < 3:
            continue
        hits = sum(1 for t in cand_terms if t in sent)
        ratio = hits / len(cand_terms)
        if ratio > best_score and hits >= 2:
            best_score, best_sent = ratio, sent[:300]
    if best_score >= 0.33 and len(best_sent) >= 25:
        return best_sent, best_score
    return "", 0.0


def load_dossier_urls(projekt_ids: list[str]) -> list[str]:
    urls: list[str] = []
    for pid in projekt_ids:
        if not pid:
            continue
        path = DOSSIER_ROOT / f"{pid}.kg.jsonl"
        if not path.is_file():
            continue
        try:
            for line in path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                rec = json.loads(line)
                props = rec.get("properties") or {}
                for k in ("primary_source_url", "evidence_url"):
                    v = props.get(k, "")
                    if isinstance(v, str) and v.startswith("http"):
                        urls.append(v)
                for v in props.get("source_urls") or []:
                    if isinstance(v, str) and v.startswith("http"):
                        urls.append(v)
                for v in props.get("external_sources") or []:
                    if isinstance(v, str) and v.startswith("http"):
                        urls.append(v)
        except Exception:  # noqa: BLE001
            continue
    return list(dict.fromkeys(urls))


def build_queries(row: dict, terms: list[str]) -> list[str]:
    subj = re.sub(r"[^a-zA-Z0-9À-ÿ\s]", " ", row.get("subject", ""))[:50].strip()
    obj = re.sub(r"[^a-zA-Z0-9À-ÿ\s]", " ", row.get("object", ""))[:40].strip()
    qs: list[str] = []
    if subj and terms:
        qs.append(f"{subj} {' '.join(terms[:3])} reuse")
        qs.append(f"{subj} {' '.join(terms[:2])}")
    if subj and obj:
        qs.append(f"{subj} {obj} wiederverwendung")
    if subj:
        qs.append(f'"{subj}" site:opalis.eu OR site:rotordb.org')
    return qs[:4]


def validate_url(
    url: str,
    quote: str,
    anchors: list[str],
    cache: dict,
    *,
    allow_repair: bool,
) -> dict | None:
    ent = ceg.fetch(url, cache)
    if not ent.get("ok"):
        return None
    pn = ent.get("norm", "")
    mk, ratio, _ = ceg.quote_on_page(quote, anchors, pn)
    if mk in {"VERBATIM", "STRONG"}:
        return {"url": url, "mode": "STRICT", "match": mk, "score": ratio, "quote": quote[:300]}
    if not allow_repair:
        return None
    terms = quote_terms(quote)
    repaired, rs = extract_on_page_quote(pn, anchors, terms)
    if not repaired:
        return None
    rmk, rr, _ = ceg.quote_on_page(repaired, anchors, pn)
    if rmk in {"VERBATIM", "STRONG"} or (rmk == "STRONG" and rs >= 0.4):
        return {"url": url, "mode": "QUOTE_REPAIR", "match": rmk or "REPAIR", "score": max(rs, rr),
                "quote": repaired}
    if rs >= 0.45 and len(repaired) >= 30:
        return {"url": url, "mode": "QUOTE_REPAIR", "match": "REPAIR", "score": rs, "quote": repaired}
    return None


def hunt_claim(row: dict, ctx: dict, cache: dict) -> dict:
    quote = row.get("quote", "")
    anchors = [row.get("subject", ""), row.get("object", "")]
    failed = row.get("url", "")
    terms = quote_terms(quote)
    allow_repair = row.get("evidence_status") in BAD | REVIEW

    candidates: list[str] = []
    for u in ctx.get("cands", []):
        if u.startswith("http"):
            candidates.append(u)
    for u in ctx.get("dossier_urls", []):
        candidates.append(u)
    if failed.startswith("http") and not ceg.is_homepage(failed):
        candidates.insert(0, failed)
    for q in build_queries(row, terms):
        try:
            candidates.extend(ddg_results(q, cache))
        except Exception:  # noqa: BLE001
            pass
    candidates = [u for u in dict.fromkeys(candidates) if u.startswith("http")][:12]

    best = None
    for u in candidates:
        hit = validate_url(u, quote, anchors, cache, allow_repair=allow_repair)
        if hit and (best is None or hit["score"] > best["score"]):
            best = hit

    return {
        "eid": row["eid"],
        "kind": row["kind"],
        "type": row["type"],
        "subject": row.get("subject", "")[:80],
        "object": row.get("object", "")[:80],
        "old_status": row.get("evidence_status", ""),
        "old_url": failed,
        "result": "RECOVERED" if best else "STILL_UNVERIFIED",
        "new_url": best["url"] if best else "",
        "new_quote": best["quote"] if best else "",
        "mode": best["mode"] if best else "",
        "match": best["match"] if best else "",
        "score": f"{best['score']:.2f}" if best else "",
        "candidates_tried": len(candidates),
    }
