"""Clickable Evidence Gate (CEG) validator — Phase 1 baseline.

For every claim in the graph that carries an evidence URL (relationships with
`evidence_url`, nodes with `primary_source_url` / `source_urls`), this script:

  1. fetches the URL **live** (no archive.org fallback — per user decision),
  2. checks whether the stored quote (or the claim's distinctive anchor tokens)
     is actually present on the fetched page,
  3. detects bare homepages / unrelated aggregators,
  4. assigns one honest `evidence_status` per claim.

It is READ-ONLY against Neo4j and writes a baseline CSV. Nothing is mutated.

Usage:
    python _scripts/verify_clickable_evidence.py [--limit N] [--out PATH]

Status taxonomy:
    CLICKABLE_VERIFIED  url 200 + quote/anchors present on page, deep link
    HOMEPAGE_ONLY       url 200 but bare homepage / no quote match on a root page
    QUOTE_MISMATCH      url 200 but neither quote nor anchors found on page
    LINK_DEAD           url did not return 200 (or fetch error)
    NO_URL              claim has no http evidence url at all (Tier-1 gap marker)
"""

from __future__ import annotations

import argparse
import csv
import re
import ssl
import sys
import time
import unicodedata
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
from neo4j_env import resolve_connection  # noqa: E402

CEG_DIR = REPO / "_neo4j/review/2026-06-07_clickable_evidence_gate"
OUT_DEFAULT = CEG_DIR / "CLICKABLE_EVIDENCE_BASELINE.csv"
CACHE_PATH = CEG_DIR / "_fetch_cache.json"
SSL_CTX = ssl.create_default_context()
SSL_CTX.check_hostname = False
SSL_CTX.verify_mode = ssl.CERT_NONE

STOP = {
    "reused", "reuse", "reclaimed", "project", "house", "building", "components",
    "component", "material", "materials", "wiederverwendete", "wiederverwendet",
    "fertigteile", "anzahl", "prozent", "with", "from", "and", "the", "der", "die",
    "das", "und", "von", "fuer", "structure", "walls", "wall", "used", "neue",
    "alte", "funktion",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def is_homepage(url: str) -> bool:
    m = re.match(r"https?://[^/]+(/.*)?$", url.strip())
    if not m:
        return False
    path = (m.group(1) or "").strip("/")
    return path == "" or path in {"en", "de", "fr", "nl", "index.html", "home"}


def fetch(url: str, cache: dict) -> dict:
    """Fetch + normalize. Cache stores {ok,status,err,norm} (norm = normalized page text)."""
    if url in cache:
        return cache[url]
    e = {"url": url, "ok": False, "status": "", "norm": "", "err": ""}
    if not url.lower().startswith("http"):
        e["err"] = "non_http"
        cache[url] = e
        return e
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (recherche-ceg-validator/1.0)",
                "Accept": "text/html,application/xhtml+xml,application/pdf;q=0.8,*/*;q=0.5",
                "Accept-Language": "de,en;q=0.8,fr;q=0.6",
            },
        )
        with urlopen(req, timeout=25, context=SSL_CTX) as resp:
            raw = resp.read(1_200_000)
            e["status"] = str(getattr(resp, "status", 200))
            e["ok"] = e["status"].startswith("2")
            e["norm"] = norm(raw.decode("utf-8", errors="replace"))[:200_000]
    except HTTPError as ex:
        e["status"] = str(ex.code)
        e["err"] = f"http {ex.code}"
    except (URLError, TimeoutError, ssl.SSLError) as ex:
        e["err"] = f"{type(ex).__name__}: {ex}"
    except Exception as ex:  # noqa: BLE001
        e["err"] = f"{type(ex).__name__}: {ex}"
    cache[url] = e
    return e


def quote_on_page(quote: str, anchors: list[str], pn: str) -> tuple[str, float, int]:
    """Return (match_kind, ratio, hits). pn = already-normalized page text.

    match_kind: VERBATIM / STRONG / WEAK / NONE. Ground-truthed thresholds:
    a deep page that contains a verbatim fragment, or >=60% of the quote's
    distinctive words (>=3 absolute), genuinely shows the fact.
    """
    qn = norm(quote)
    if not pn:
        return "NONE", 0.0, 0
    if qn:
        frag = qn[:90].strip()
        if len(frag) >= 25 and frag in pn:
            return "VERBATIM", 1.0, 99
    words = [w for w in re.findall(r"[a-zaeoeue0-9]{5,}", qn) if w not in STOP]
    anchor_toks = [norm(a) for a in anchors if a]
    anchor_toks = [a for a in anchor_toks if len(a) >= 4 and a not in STOP]
    cand = list(dict.fromkeys(words + anchor_toks))[:14]
    if not cand:
        return "NONE", 0.0, 0
    page_tokens = set(re.findall(r"[a-zaeoeue0-9]{4,}", pn))

    def hit(tok: str) -> bool:
        if tok in pn:
            return True
        return any(pt.startswith(tok) or tok.startswith(pt)
                   for pt in page_tokens if abs(len(pt) - len(tok)) <= 3)

    hits = sum(1 for t in cand if hit(t))
    ratio = hits / len(cand)
    if (ratio >= 0.6 and hits >= 3) or (ratio >= 0.75 and hits >= 2):
        return "STRONG", ratio, hits
    if ratio >= 0.33 and hits >= 2:
        return "WEAK", ratio, hits
    return "NONE", ratio, hits


def classify(kind: str, url: str, fetched: dict, match_kind: str) -> str:
    """Honest per-claim status.

    LINK_DEAD            url did not load (200)
    CLICKABLE_VERIFIED   verbatim/strong quote match on the page
    ENTITY_HOMEPAGE      node link to its own org homepage (acceptable for entities)
    HOMEPAGE_ONLY        rel link to a bare homepage, fact not shown
    LIKELY_REVIEW        deep page, partial (weak) match — keep, human review
    QUOTE_MISMATCH       deep page, fact not found
    """
    if not fetched.get("ok"):
        return "LINK_DEAD"
    if match_kind in {"VERBATIM", "STRONG"}:
        return "CLICKABLE_VERIFIED"
    if is_homepage(url):
        return "ENTITY_HOMEPAGE" if kind == "node" else "HOMEPAGE_ONLY"
    if match_kind == "WEAK":
        return "LIKELY_REVIEW"
    return "QUOTE_MISMATCH"


REL_QUERY = """
MATCH (a)-[r]->(b)
WHERE r.evidence_url STARTS WITH 'http'
RETURN elementId(r) AS eid, type(r) AS rtype,
       coalesce(a.name, a.id, '') AS from_name,
       coalesce(b.name, b.id, '') AS to_name,
       r.evidence_url AS url, coalesce(r.evidence_quote,'') AS quote
"""

NODE_QUERY = """
MATCH (n)
WHERE n.primary_source_url STARTS WITH 'http'
RETURN elementId(n) AS eid, labels(n) AS labels,
       coalesce(n.name, n.id, '') AS name,
       n.primary_source_url AS url, coalesce(n.name,'') AS quote
"""


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=0, help="cap claims (0 = all)")
    ap.add_argument("--out", type=Path, default=OUT_DEFAULT)
    args = ap.parse_args()

    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    claims: list[dict] = []
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as s:
            for rec in s.run(REL_QUERY):
                claims.append({
                    "kind": "rel", "eid": rec["eid"], "type": rec["rtype"],
                    "subject": rec["from_name"], "object": rec["to_name"],
                    "url": rec["url"], "quote": rec["quote"],
                })
            for rec in s.run(NODE_QUERY):
                claims.append({
                    "kind": "node", "eid": rec["eid"],
                    "type": "+".join(rec["labels"]),
                    "subject": rec["name"], "object": "",
                    "url": rec["url"], "quote": rec["quote"],
                })
    finally:
        driver.close()

    if args.limit:
        claims = claims[: args.limit]
    print(f"Loaded {len(claims)} URL-bearing claims from {database}")

    import json as _json

    cache: dict[str, dict] = {}
    if CACHE_PATH.is_file():
        try:
            cache = _json.loads(CACHE_PATH.read_text(encoding="utf-8"))
            print(f"loaded fetch cache: {len(cache)} urls")
        except Exception:  # noqa: BLE001
            cache = {}
    uniq = sorted({c["url"] for c in claims})
    todo = [u for u in uniq if u not in cache]
    print(f"Fetching {len(todo)}/{len(uniq)} unique URLs (live; rest cached)...")
    for i, u in enumerate(todo, 1):
        fetch(u, cache)
        if i % 20 == 0:
            print(f"  fetched {i}/{len(todo)}")
            CACHE_PATH.write_text(_json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.2)
    CACHE_PATH.write_text(_json.dumps(cache, ensure_ascii=False), encoding="utf-8")

    args.out.parent.mkdir(parents=True, exist_ok=True)
    cols = [
        "kind", "type", "subject", "object", "url", "http_status",
        "match_kind", "match_score", "evidence_status", "is_homepage",
        "quote", "eid", "checked_at",
    ]
    from collections import Counter

    status_counts: Counter = Counter()
    type_status: dict[str, Counter] = {}
    with args.out.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for c in claims:
            ent = cache.get(c["url"], {})
            anchors = [c["subject"], c["object"]]
            mk, score, hits = quote_on_page(c["quote"], anchors, ent.get("norm", ""))
            status = classify(c["kind"], c["url"], ent, mk)
            status_counts[status] += 1
            type_status.setdefault(c["type"], Counter())[status] += 1
            w.writerow({
                "kind": c["kind"], "type": c["type"], "subject": c["subject"][:80],
                "object": c["object"][:80], "url": c["url"],
                "http_status": ent.get("status", ""), "match_kind": mk,
                "match_score": f"{score:.2f}", "evidence_status": status,
                "is_homepage": is_homepage(c["url"]),
                "quote": c["quote"][:160], "eid": c["eid"], "checked_at": utc_now(),
            })

    print("\n=== Phase 1 baseline — evidence_status ===")
    total = len(claims)
    for st, n in status_counts.most_common():
        print(f"  {st:20} {n:5}  ({100*n/total:.1f}%)")
    verified = status_counts.get("CLICKABLE_VERIFIED", 0)
    print(f"\n  CLICKABLE_VERIFIED: {verified}/{total} = {100*verified/total:.1f}%")
    print(f"\nBaseline CSV: {args.out}")


if __name__ == "__main__":
    main()
