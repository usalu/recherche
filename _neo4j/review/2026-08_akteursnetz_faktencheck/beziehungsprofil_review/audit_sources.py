"""Re-open every stored relationship source and audit the stored quotation.

The audit is review-only. It stores response metadata and text hashes, never
copies full third-party page text into the repository.
"""

from __future__ import annotations

import hashlib
import json
import re
import threading
import unicodedata
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import BytesIO
from pathlib import Path

import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader
from rapidfuzz.fuzz import partial_ratio


HERE = Path(__file__).resolve().parent
INVENTORY = HERE / "relationship_inventory.json"
OUT_JSON = HERE / "source_access_audit.json"
OUT_SUMMARY = HERE / "SOURCE_AUDIT_SUMMARY.md"

MAX_BYTES = 18 * 1024 * 1024
TIMEOUT = (10, 25)
WORKERS = 16
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 Chrome/127 Safari/537.36 relationship-evidence-review/1.0"
)

_thread_local = threading.local()


def session() -> requests.Session:
    if not hasattr(_thread_local, "session"):
        value = requests.Session()
        value.headers.update({"User-Agent": USER_AGENT, "Accept-Language": "de,en;q=0.8"})
        _thread_local.session = value
    return _thread_local.session


def normalized_text(value: str) -> str:
    value = unicodedata.normalize("NFKC", value or "")
    value = value.replace("\u00ad", "")
    value = re.sub(r"\s+", " ", value)
    return value.strip().casefold()


def search_needles(value: str) -> list[str]:
    value = normalized_text(value)
    words = re.findall(r"[\wÀ-ÿ'-]+", value)
    stop = {
        "gmbh", "ag", "ab", "as", "aps", "bv", "sa", "sas", "oy", "ltd", "limited",
        "group", "project", "building", "architects", "architecten", "ingenieurs", "stadt",
    }
    useful = [word for word in words if len(word) >= 5 and word not in stop]
    return sorted(set(useful), key=len, reverse=True)[:5]


def evidence_snippet(text: str, quote: str, source_name: str, target_name: str) -> str:
    if not text:
        return ""
    needles = []
    if quote and quote in text:
        needles.append(quote)
    needles.extend(search_needles(source_name))
    needles.extend(search_needles(target_name))
    positions = [text.find(needle) for needle in needles if needle and text.find(needle) >= 0]
    if not positions:
        return text[:900]
    position = min(positions)
    start = max(0, position - 220)
    end = min(len(text), position + 680)
    return text[start:end]


def extract_text(content: bytes, content_type: str, url: str) -> tuple[str, str]:
    is_pdf = "application/pdf" in content_type.lower() or url.lower().split("?", 1)[0].endswith(".pdf")
    if is_pdf:
        try:
            reader = PdfReader(BytesIO(content))
            text = "\n".join((page.extract_text() or "") for page in reader.pages)
            return text, "pdf"
        except Exception as exc:  # noqa: BLE001 - audit must record parser failures
            return "", f"pdf_parse_error:{type(exc).__name__}"
    try:
        soup = BeautifulSoup(content, "html.parser")
        for element in soup(["script", "style", "noscript", "svg"]):
            element.decompose()
        return soup.get_text(" ", strip=True), "html"
    except Exception as exc:  # noqa: BLE001
        return "", f"html_parse_error:{type(exc).__name__}"


def fetch(url: str) -> dict:
    try:
        response = session().get(url, timeout=TIMEOUT, allow_redirects=True, stream=True)
        chunks: list[bytes] = []
        size = 0
        truncated = False
        for chunk in response.iter_content(128 * 1024):
            if not chunk:
                continue
            if size + len(chunk) > MAX_BYTES:
                chunks.append(chunk[: MAX_BYTES - size])
                truncated = True
                break
            chunks.append(chunk)
            size += len(chunk)
        content = b"".join(chunks)
        text, parser = extract_text(content, response.headers.get("Content-Type", ""), response.url)
        return {
            "requested_url": url,
            "final_url": response.url,
            "http_status": response.status_code,
            "reachable": 200 <= response.status_code < 400,
            "content_type": response.headers.get("Content-Type", ""),
            "bytes_read": len(content),
            "truncated_at_limit": truncated,
            "parser": parser,
            "text_length": len(text),
            "text_sha256": hashlib.sha256(text.encode("utf-8", errors="replace")).hexdigest(),
            "text": normalized_text(text),
            "error": "",
        }
    except Exception as exc:  # noqa: BLE001
        return {
            "requested_url": url,
            "final_url": "",
            "http_status": None,
            "reachable": False,
            "content_type": "",
            "bytes_read": 0,
            "truncated_at_limit": False,
            "parser": "",
            "text_length": 0,
            "text_sha256": "",
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    relationships = inventory["relationships"]
    urls = sorted({row["evidence_url"] for row in relationships if row["evidence_url"]})

    fetched: dict[str, dict] = {}
    with ThreadPoolExecutor(max_workers=WORKERS) as pool:
        future_urls = {pool.submit(fetch, url): url for url in urls}
        for future in as_completed(future_urls):
            result = future.result()
            fetched[result["requested_url"]] = result

    relationship_results: list[dict] = []
    for row in relationships:
        source = fetched.get(row["evidence_url"], {})
        quote = normalized_text(row["evidence_quote"])
        text = source.get("text", "")
        exact = bool(quote and text and quote in text)
        fuzzy = 0.0
        if quote and text and not exact:
            fuzzy = round(float(partial_ratio(quote, text)), 1)
        relationship_results.append(
            {
                "review_id": row["review_id"],
                "origin": row["origin"],
                "evidence_url": row["evidence_url"],
                "http_status": source.get("http_status"),
                "reachable": source.get("reachable", False),
                "parser": source.get("parser", ""),
                "extracted_text_length": source.get("text_length", 0),
                "quote_exact_match": exact,
                "quote_fuzzy_match": fuzzy,
                "source_snippet": evidence_snippet(
                    text,
                    quote,
                    row.get("source", ""),
                    row.get("target", ""),
                ),
                "requires_manual_source_review": (
                    not source.get("reachable", False)
                    or source.get("text_length", 0) < 80
                    or (not exact and fuzzy < 92)
                ),
            }
        )

    public_sources = []
    for url in urls:
        item = dict(fetched[url])
        item.pop("text", None)
        public_sources.append(item)
    payload = {
        "review_run": "2026-08-20_beziehungsprofil_source_audit",
        "review_only": True,
        "unique_urls": len(urls),
        "sources": public_sources,
        "relationships": relationship_results,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    reachable = sum(source["reachable"] for source in public_sources)
    exact = sum(row["quote_exact_match"] for row in relationship_results)
    manual = sum(row["requires_manual_source_review"] for row in relationship_results)
    base_manual = sum(
        row["requires_manual_source_review"] and row["origin"] == "baseline_264"
        for row in relationship_results
    )
    new_manual = sum(
        row["requires_manual_source_review"] and row["origin"] == "expansion_candidate"
        for row in relationship_results
    )
    OUT_SUMMARY.write_text(
        f"""# Relationship source access audit

Review-only source audit. No canonical graph or LaTeX output was changed.

- Unique stored URLs reopened: **{len(urls)}**
- Reachable in this automated pass: **{reachable}**
- Relationship quotations found verbatim: **{exact} / {len(relationship_results)}**
- Relationships requiring manual browser/source review: **{manual}**
  - baseline: **{base_manual}**
  - expansion: **{new_manual}**

Automated non-matches are flags, not rejection decisions. JavaScript pages,
access blocks, PDF layout, translations, and shortened quotations can prevent
a literal match even when a source is valid.
""",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "unique_urls": len(urls),
                "reachable": reachable,
                "quote_exact": exact,
                "manual_relationships": manual,
            }
        )
    )


if __name__ == "__main__":
    main()
