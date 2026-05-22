"""Agent S3 — Content verifier
==============================
For each citation edge whose evidence_origin='source_curated' and
evidence_excerpt is non-empty, verify whether the excerpt (or a
paraphrase) appears in the cached body of the cited URL.

3-tier match:
  Tier A — verbatim_match    (exact substring, score 1.0)
  Tier B — paraphrase_match  (fuzz.partial_ratio ≥ 0.85)
  Tier C — token_match       (token-set overlap ≥ 0.80)
  Fallback — no_text_match   (score 0.0)

Skips:
  - evidence_origin IN ['topology_synthesized','inferred','registry_derived']
  - null / empty evidence_excerpt
  - already verified (verification_status not NULL and not 'unchecked')
  - dead URL (url_status starts with 'dead_') → tag target_page_dead
  - no body cache → tag fetch_error
  - unsupported content type → tag unsupported_content_type

Writes verification_status / score / method / notes on the citation edge.
Emits :DataIssue nodes for no_text_match.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/logs/agent_s3_runner.py
"""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import sys
import unicodedata
from datetime import date, datetime, timezone
from pathlib import Path

import pdfplumber
from bs4 import BeautifulSoup
from langdetect import detect as langdetect_detect, LangDetectException
from rapidfuzz import fuzz

_REPO = Path(__file__).resolve().parents[5]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

# ─── paths ────────────────────────────────────────────────────────────────────

RUN_DIR = Path(__file__).resolve().parent.parent
S2_DIR = RUN_DIR / "agent_s2_url_prober"
S3_DIR = RUN_DIR / "agent_s3_content_verifier"
BODIES_DIR = RUN_DIR / "shared" / "url_bodies"
LOG_DIR = S3_DIR / "logs"
VERIFY_LOG = LOG_DIR / "verification_results.jsonl"
FLAG_FILE = S3_DIR / "PHASE_S3_DONE.flag"
S2_FLAG = S2_DIR / "PHASE_S2_DONE.flag"
MIG_DIR = S3_DIR / "migrations"

LOG_DIR.mkdir(parents=True, exist_ok=True)
MIG_DIR.mkdir(parents=True, exist_ok=True)

# ─── constants ────────────────────────────────────────────────────────────────

PARAPHRASE_THRESHOLD = 0.85
TOKEN_THRESHOLD = 0.80

# Evidence basis values that are structured metadata (not verbatim page quotes)
# S3 still runs on them — it will mostly produce no_text_match, which is honest.
STRUCTURED_BASES = {
    "cell_citation",
    "edge_excerpt_extraction",
    "bare_url_extraction",
    "markdown_link_extraction",
    "documented",
}

SKIP_ORIGINS = {"topology_synthesized", "inferred", "registry_derived"}

# Cookie wall indicators (present in small pages with consent walls)
COOKIE_WALL_PHRASES = [
    "cookie", "consent", "accept all", "akzeptieren", "datenschutz",
    "privacy", "gdpr", "dsgvo", "zustimmung", "einwilligung",
]
JS_ONLY_INDICATORS = [
    "javascript", "enable javascript", "javascript required",
    "please enable", "bitte aktivieren",
]


# ─── text helpers ─────────────────────────────────────────────────────────────


def normalise_text(text: str) -> str:
    """NFKC normalise + collapse whitespace + lowercase."""
    text = unicodedata.normalize("NFKC", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text.lower()


def extract_visible_text(html_bytes: bytes) -> str:
    """Extract human-readable text from HTML, stripping nav/footer/scripts."""
    try:
        soup = BeautifulSoup(html_bytes, "lxml")
    except Exception:
        soup = BeautifulSoup(html_bytes, "html.parser")
    # Remove boilerplate
    for tag in soup(["script", "style", "nav", "footer", "header",
                     "aside", "noscript", "form", "button"]):
        tag.decompose()
    return soup.get_text(separator=" ", strip=True)


def extract_pdf_text(pdf_bytes: bytes) -> str:
    """Extract text from PDF bytes using pdfplumber."""
    parts: list[str] = []
    try:
        import io
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                t = page.extract_text()
                if t:
                    parts.append(t)
    except Exception:
        pass
    return "\n".join(parts)


def read_cached_body(cache_path: str) -> bytes | None:
    """Read body from cache, decompressing .gz files."""
    full_path = RUN_DIR / cache_path
    if not full_path.exists():
        return None
    try:
        raw = full_path.read_bytes()
        if cache_path.endswith(".gz"):
            return gzip.decompress(raw)
        return raw
    except Exception:
        return None


def is_cookie_wall(text: str, body_len: int) -> bool:
    """Heuristic: short page + multiple cookie-wall phrases → consent wall."""
    if body_len > 50_000:
        return False
    text_lower = text.lower()
    hits = sum(1 for phrase in COOKIE_WALL_PHRASES if phrase in text_lower)
    return hits >= 3


def is_js_only(html_bytes: bytes, visible_text: str) -> bool:
    """Heuristic: very short visible text in an HTML page."""
    if len(visible_text.split()) < 20:
        text_lower = visible_text.lower()
        return any(ind in text_lower for ind in JS_ONLY_INDICATORS)
    return False


def detect_language(text: str) -> str | None:
    """Detect language; returns ISO 639-1 code or None."""
    try:
        sample = text[:3000].strip()
        if len(sample) < 50:
            return None
        return langdetect_detect(sample)
    except LangDetectException:
        return None
    except Exception:
        return None


def token_overlap(a: str, b: str) -> float:
    """Fraction of tokens in `a` that appear in `b`."""
    tokens_a = set(a.lower().split())
    tokens_b = set(b.lower().split())
    if not tokens_a:
        return 0.0
    return len(tokens_a & tokens_b) / len(tokens_a)


# ─── 3-tier matching ──────────────────────────────────────────────────────────


def three_tier_match(
    excerpt: str, page_text: str
) -> tuple[str, float, str, str]:
    """
    Returns (status, score, method, notes).
    status in: verbatim_match, paraphrase_match, token_match, no_text_match
    """
    norm_excerpt = normalise_text(excerpt)
    norm_page = normalise_text(page_text)

    # Tier A — verbatim substring
    if norm_excerpt and norm_excerpt in norm_page:
        return "verbatim_match", 1.0, "substring", ""

    # For very short excerpts (< 15 chars), skip fuzzy to avoid false positives
    if len(norm_excerpt) < 15:
        return "no_text_match", 0.0, "excerpt_too_short", "excerpt < 15 chars"

    # Tier B — fuzzy partial match
    # Use partial_ratio on the first 2000 chars of excerpt for performance
    excerpt_sample = norm_excerpt[:2000]
    # Slide over page in windows to find the best partial match
    page_sample = norm_page[:50000]  # limit page text for performance
    ratio = fuzz.partial_ratio(excerpt_sample, page_sample) / 100.0
    if ratio >= PARAPHRASE_THRESHOLD:
        return "paraphrase_match", round(ratio, 4), "fuzz_partial_ratio", \
               f"score={ratio:.3f}"

    # Tier C — token-set overlap
    overlap = token_overlap(norm_excerpt, norm_page)
    if overlap >= TOKEN_THRESHOLD:
        return "token_match", round(overlap, 4), "token_overlap", \
               f"overlap={overlap:.3f}"

    return "no_text_match", round(max(ratio, overlap), 4), "none", \
           f"best_fuzz={ratio:.3f} best_token={overlap:.3f}"


# ─── MD5 helper ───────────────────────────────────────────────────────────────


def md5_of(data: bytes) -> str:
    return hashlib.md5(data).hexdigest()


# ─── Cypher ───────────────────────────────────────────────────────────────────

S3_A = """
MATCH ()-[r]->()
WHERE id(r) = $edge_id
SET r.verification_status   = $verification_status,
    r.verification_score    = $verification_score,
    r.verification_method   = $verification_method,
    r.verified_at           = date(),
    r.verification_attempts = coalesce(r.verification_attempts, 0) + 1,
    r.verification_notes    = $verification_notes,
    r.verification_body_md5 = $verification_body_md5,
    r.migration_origin      = coalesce(r.migration_origin, '') + ' | mig_s3_content_verify'
"""

S3_B = """
WITH $edge_id AS eid, $verification_status AS vstatus, $excerpt AS exc
WHERE vstatus = 'no_text_match'
MATCH (src)-[r]->(tgt)
WHERE id(r) = eid
MERGE (i:DataIssue {id: 'di_no_match__' + toString(eid)})
ON CREATE SET
  i.kind             = 'citation_no_text_match',
  i.severity         = 'low',
  i.ref_label        = 'edge',
  i.ref_id           = toString(eid),
  i.found_at         = date(),
  i.found_by         = 's3_content_verify',
  i.status           = 'open',
  i.resolution_note  = 'Excerpt not found in source page body',
  i.evidence_excerpt_preview = left(exc, 200)
MERGE (i)-[:CONCERNS]->(tgt)
"""


# ─── main ─────────────────────────────────────────────────────────────────────


def run_s3() -> None:
    print("=" * 70)
    print("Agent S3 — Content verifier")
    print("=" * 70)

    # Pre-flight: S2 flag
    if not S2_FLAG.exists():
        print(f"[ABORT] S2 flag not found: {S2_FLAG}")
        print("       Run agent_s2_runner.py first.")
        sys.exit(1)
    print(f"[OK] S2 flag present")

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )
    print(f"[INFO] Connecting to {uri} / db={database}")

    # Fetch all verifiable citation edges
    with driver.session(database=database) as session:
        rows = list(session.run("""
            MATCH (src)-[r]->(target)
            WHERE r.evidence_origin = 'source_curated'
              AND r.evidence_excerpt IS NOT NULL
              AND r.evidence_excerpt <> ''
              AND (r.verification_status IS NULL OR r.verification_status = 'unchecked')
              AND NOT (r.evidence_origin IN $skip_origins)
            OPTIONAL MATCH (target)-[:ZITIERT_QUELLE]->(ext1:ExternalLink)
            WITH src, r, target,
                 CASE
                   WHEN target:ExternalLink THEN target
                   WHEN ext1 IS NOT NULL THEN ext1
                   ELSE NULL END AS url_node
            RETURN
              id(r)                       AS edge_id,
              type(r)                     AS edge_type,
              r.evidence_excerpt          AS excerpt,
              r.evidence_basis            AS basis,
              url_node.id                 AS ext_id,
              url_node.url                AS url,
              url_node.url_status         AS url_status,
              url_node.url_body_cache_path AS cache_path,
              url_node.url_content_type   AS content_type,
              url_node.url_wayback_snapshot AS wayback_url,
              url_node.url_body_md5       AS body_md5
        """, skip_origins=list(SKIP_ORIGINS)))

    targets = [dict(r) for r in rows]
    total = len(targets)
    print(f"[INFO] {total} citation edges to verify")

    # Stats
    stats = {k: 0 for k in [
        "verbatim_match", "paraphrase_match", "token_match", "no_text_match",
        "target_page_dead", "fetch_error", "cookie_wall_detected",
        "unsupported_javascript_required", "unsupported_content_type",
        "unsupported_pdf_scanned", "language_mismatch",
        "no_url_node", "errors", "total",
    ]}
    stats["total"] = total

    def _write_edge(session, edge_id, status, score, method, notes, body_md5=None):
        session.run(S3_A,
                    edge_id=edge_id,
                    verification_status=status,
                    verification_score=score,
                    verification_method=method,
                    verification_notes=notes,
                    verification_body_md5=body_md5)

    def _write_data_issue(session, edge_id, excerpt):
        session.run(S3_B, edge_id=edge_id,
                    verification_status="no_text_match",
                    excerpt=excerpt)

    print(f"\n[Stage 1] Verifying {total} edges...")
    done = 0

    with driver.session(database=database) as session:
        for t in targets:
            edge_id = t["edge_id"]
            excerpt = t["excerpt"] or ""
            cache_path = t["cache_path"]
            url_status = t["url_status"]
            content_type = (t["content_type"] or "").lower()
            basis = t["basis"] or ""

            try:
                # No URL node found
                if t["ext_id"] is None:
                    _write_edge(session, edge_id,
                                "no_url_node", 0.0, "skipped",
                                "No ExternalLink reachable from this citation")
                    stats["no_url_node"] += 1
                    done += 1
                    continue

                # Dead URL
                if url_status and (url_status.startswith("dead_") or
                                   url_status in {"timeout", "dns_failure",
                                                  "tls_failure", "blocked_by_robots"}):
                    _write_edge(session, edge_id,
                                "target_page_dead", 0.0, "skipped",
                                f"url_status={url_status}")
                    stats["target_page_dead"] += 1
                    done += 1
                    continue

                # No body cache
                if not cache_path:
                    reason = "no_cache_path"
                    if url_status is None or url_status == "unchecked":
                        reason = "url_not_probed"
                    _write_edge(session, edge_id,
                                "fetch_error", 0.0, "skipped", reason)
                    stats["fetch_error"] += 1
                    done += 1
                    continue

                # Read body
                body_bytes = read_cached_body(cache_path)
                if body_bytes is None:
                    _write_edge(session, edge_id,
                                "fetch_error", 0.0, "skipped",
                                f"cache_file_missing: {cache_path}")
                    stats["fetch_error"] += 1
                    done += 1
                    continue

                # Extract text by content type
                if "pdf" in content_type:
                    page_text = extract_pdf_text(body_bytes)
                    if not page_text.strip():
                        _write_edge(session, edge_id,
                                    "unsupported_pdf_scanned", 0.0, "skipped",
                                    "PDF extraction returned no text")
                        stats["unsupported_pdf_scanned"] += 1
                        done += 1
                        continue
                elif any(ct in content_type for ct in
                         ["html", "xhtml", "xml", "text"]):
                    page_text = extract_visible_text(body_bytes)
                else:
                    _write_edge(session, edge_id,
                                "unsupported_content_type", 0.0, "skipped",
                                f"content_type={content_type}")
                    stats["unsupported_content_type"] += 1
                    done += 1
                    continue

                # Cookie wall / JS-only detection
                if is_cookie_wall(page_text, len(body_bytes)):
                    _write_edge(session, edge_id,
                                "cookie_wall_detected", 0.0, "skipped",
                                "Cookie consent wall detected")
                    stats["cookie_wall_detected"] += 1
                    done += 1
                    continue

                if "html" in content_type and is_js_only(body_bytes, page_text):
                    _write_edge(session, edge_id,
                                "unsupported_javascript_required", 0.0, "skipped",
                                "Page appears JavaScript-only")
                    stats["unsupported_javascript_required"] += 1
                    done += 1
                    continue

                # Language check (only for non-structured basis excerpts)
                if basis not in STRUCTURED_BASES:
                    ex_lang = detect_language(excerpt)
                    pg_lang = detect_language(page_text[:5000])
                    if ex_lang and pg_lang and ex_lang != pg_lang:
                        _write_edge(session, edge_id,
                                    "language_mismatch", 0.0, "skipped",
                                    f"excerpt_lang={ex_lang}; page_lang={pg_lang}")
                        stats["language_mismatch"] += 1
                        done += 1
                        continue

                # Three-tier match
                status, score, method, notes = three_tier_match(excerpt, page_text)
                body_md5 = md5_of(body_bytes)

                _write_edge(session, edge_id,
                            status, score, method, notes, body_md5)
                if status == "no_text_match":
                    _write_data_issue(session, edge_id, excerpt)

                stats[status] += 1

                # Log
                log_entry = {
                    "ts": datetime.now(timezone.utc).isoformat(),
                    "edge_id": edge_id,
                    "edge_type": t["edge_type"],
                    "url": t["url"],
                    "basis": basis,
                    "verification_status": status,
                    "verification_score": score,
                    "method": method,
                }
                with VERIFY_LOG.open("a", encoding="utf-8") as fh:
                    fh.write(json.dumps(log_entry, default=str) + "\n")

            except Exception as exc:
                stats["errors"] += 1
                print(f"  [ERROR] edge_id={edge_id}: {exc}")
                try:
                    _write_edge(session, edge_id,
                                "fetch_error", 0.0, "error", str(exc)[:200])
                except Exception:
                    pass

            done += 1
            if done % 200 == 0 or done == total:
                pct = 100 * done / total if total else 0
                print(
                    f"  [{done}/{total} {pct:.0f}%] "
                    f"verbatim={stats['verbatim_match']} "
                    f"paraphrase={stats['paraphrase_match']} "
                    f"token={stats['token_match']} "
                    f"no_match={stats['no_text_match']} "
                    f"dead={stats['target_page_dead']} "
                    f"skip={stats['fetch_error']}"
                )

    driver.close()

    # Acceptance gates
    print("\n[Acceptance gates]")
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )
    with driver.session(database=database) as sess:
        g1 = sess.run(
            "MATCH ()-[r]->() WHERE r.evidence_origin='source_curated' "
            "AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> '' "
            "AND (r.verification_status IS NULL OR r.verification_status='unchecked') "
            "RETURN count(r) AS n"
        ).single()["n"]
        g3 = sess.run(
            "MATCH ()-[r]->() WHERE r.verification_score IS NOT NULL "
            "AND (r.verification_score < 0 OR r.verification_score > 1) "
            "RETURN count(r) AS n"
        ).single()["n"]
        g4 = sess.run(
            "MATCH (i:DataIssue {kind:'citation_no_text_match'}) RETURN count(i) AS n"
        ).single()["n"]
        g5 = sess.run(
            "MATCH ()-[r]->() WHERE r.verification_method IS NOT NULL "
            "RETURN r.verification_status, count(r) AS n ORDER BY n DESC"
        ).data()
        g6 = sess.run(
            "MATCH (:Projekt {id:'p_stuttgart_210'})-[bel:BELEGT_IN]->(d:Dossier)"
            "-[z:ZITIERT_QUELLE]->(e:ExternalLink) "
            "WHERE z.verification_status='verbatim_match' RETURN count(z) AS n"
        ).single()["n"]
    driver.close()

    print(f"  unchecked edges remaining:   {g1}  (expected 0)")
    print(f"  score out of [0,1]:          {g3}  (expected 0)")
    print(f"  DataIssue no_text_match:     {g4}  (expected ≥0)")
    print(f"  Stuttgart 210 verbatim:      {g6}  (expected ≥1, aspirational)")
    print(f"  Status distribution:")
    for row in g5[:10]:
        print(f"    {row['r.verification_status']:40s} {row['n']}")

    # Compute match rate
    attempted = stats["verbatim_match"] + stats["paraphrase_match"] + \
                stats["token_match"] + stats["no_text_match"]
    match_rate = 0.0
    if attempted > 0:
        match_rate = (stats["verbatim_match"] + stats["paraphrase_match"] +
                      stats["token_match"]) / attempted

    print(f"\n  Match rate (verbatim+para+token / attempted): {match_rate:.1%}")

    gate_pass = (g1 == 0 and g3 == 0)
    if not gate_pass:
        print("\n[WARNING] Not all acceptance gates pass.")
    else:
        print("\n[OK] Core acceptance gates pass.")

    # Write flag
    FLAG_FILE.write_text(
        f"PHASE_S3_DONE\n"
        f"verified_at: {date.today()}\n"
        f"total_edges: {total}\n"
        f"verbatim_match: {stats['verbatim_match']}\n"
        f"paraphrase_match: {stats['paraphrase_match']}\n"
        f"token_match: {stats['token_match']}\n"
        f"no_text_match: {stats['no_text_match']}\n"
        f"target_page_dead: {stats['target_page_dead']}\n"
        f"fetch_error: {stats['fetch_error']}\n"
        f"cookie_wall_detected: {stats['cookie_wall_detected']}\n"
        f"language_mismatch: {stats['language_mismatch']}\n"
        f"no_url_node: {stats['no_url_node']}\n"
        f"errors: {stats['errors']}\n"
        f"match_rate_of_attempted: {match_rate:.3f}\n",
        encoding="utf-8",
    )
    print(f"\n[DONE] PHASE_S3_DONE.flag written → {FLAG_FILE}")
    print(f"[STATS] {stats}")


if __name__ == "__main__":
    run_s3()
