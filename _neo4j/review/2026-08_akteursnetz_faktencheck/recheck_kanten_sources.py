# -*- coding: utf-8 -*-
"""Re-open every distinct stored edge-evidence URL and verify saved quotations.

This is a transport/accessibility audit only.  It does not decide that a
relationship exists; the per-edge classification remains responsible for
checking what the quotation actually proves.

Output: kanten_source_recheck.json
"""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from html import unescape
import json
import os
import re
import tempfile

import requests


BASE = os.path.dirname(os.path.abspath(__file__))
INDEX = os.path.join(BASE, "kanten_batches", "_index.json")
OUTPUT = os.path.join(BASE, "kanten_source_recheck.json")
TIMEOUT = 20
WORKERS = 12


def normalize(value):
    value = unescape(value or "")
    value = re.sub(r"<script\b[^>]*>.*?</script>", " ", value,
                   flags=re.I | re.S)
    value = re.sub(r"<style\b[^>]*>.*?</style>", " ", value,
                   flags=re.I | re.S)
    value = re.sub(r"<[^>]+>", " ", value)
    value = value.replace("\u00ad", "").replace("\xa0", " ")
    return re.sub(r"\s+", " ", value).strip().casefold()


def fetch(url, quotes):
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; AkteursnetzEvidenceAudit/1.0)"
    }
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT,
                                allow_redirects=True)
        content_type = response.headers.get("content-type", "").lower()
        result = {
            "requested_url": url,
            "final_url": response.url,
            "status_code": response.status_code,
            "content_type": content_type,
            "reachable": 200 <= response.status_code < 400,
            "quote_checks": {},
        }
        if result["reachable"] and ("html" in content_type or
                                      "text" in content_type or
                                      not content_type):
            page = normalize(response.text)
            for quote in quotes:
                q = normalize(quote)
                result["quote_checks"][quote] = bool(q and q in page)
            result["text_checked"] = True
        else:
            result["text_checked"] = False
        return result
    except requests.RequestException as exc:
        return {
            "requested_url": url,
            "final_url": None,
            "status_code": None,
            "content_type": None,
            "reachable": False,
            "text_checked": False,
            "quote_checks": {},
            "error": f"{type(exc).__name__}: {exc}",
        }


def write_atomic(path, value):
    fd, tmp = tempfile.mkstemp(prefix=os.path.basename(path) + ".",
                               suffix=".tmp", dir=os.path.dirname(path))
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            json.dump(value, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
        os.replace(tmp, path)
    except Exception:
        if os.path.exists(tmp):
            os.unlink(tmp)
        raise


def main():
    with open(INDEX, encoding="utf-8") as handle:
        index = json.load(handle)
    edges = [edge for batch in index["batches"] for edge in batch["edges"]]
    by_url = {}
    for edge in edges:
        if edge["status"] != "GEPRUEFT":
            continue
        by_url.setdefault(edge["evidence_url"], set()).add(edge["evidence_quote"])

    pages = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        futures = {
            pool.submit(fetch, url, sorted(quotes)): url
            for url, quotes in by_url.items()
        }
        for future in as_completed(futures):
            pages[futures[future]] = future.result()

    edge_checks = {}
    for edge in edges:
        if edge["status"] != "GEPRUEFT":
            continue
        page = pages[edge["evidence_url"]]
        quote_found = page["quote_checks"].get(edge["evidence_quote"])
        edge_checks[edge["id"]] = {
            "url": edge["evidence_url"],
            "reachable": page["reachable"],
            "text_checked": page["text_checked"],
            "quote_found": quote_found,
        }

    payload = {
        "review_run": index.get("review_run"),
        "checked_at": datetime.now(timezone.utc).isoformat(),
        "distinct_urls": len(pages),
        "checked_edges": len(edge_checks),
        "pages": dict(sorted(pages.items())),
        "edges": dict(sorted(edge_checks.items())),
    }
    write_atomic(OUTPUT, payload)

    reachable = sum(page["reachable"] for page in pages.values())
    quote_found = sum(check["quote_found"] is True for check in edge_checks.values())
    quote_missing = sum(check["quote_found"] is False for check in edge_checks.values())
    text_unchecked = sum(check["quote_found"] is None for check in edge_checks.values())
    print(f"URLs: {len(pages)} | reachable: {reachable} | unreachable: {len(pages)-reachable}")
    print(f"Edges: {len(edge_checks)} | quote found: {quote_found} | "
          f"quote missing: {quote_missing} | text unchecked: {text_unchecked}")
    print(f"written: {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
