"""test_all_labels.py — full v4 rule validation across every user-facing label.

For each non-denylisted node label in the live graph:
  1. Sample N nodes (default 5; configurable via --samples).
  2. For each sample node, pull its source_urls + the dossier(s) it cites.
  3. For each (node, URL) candidate, run the v4 cross-confirmation test:
       D = node terms appear in dossier text near the URL
       P = node terms appear in cached HTML body
       BOTH = D AND P (the v4 gold standard)
  4. Aggregate per label, emit:
       - console matrix
       - logs/v4_test_all_labels.jsonl (per-edge detail)
       - logs/v4_test_all_labels_summary.json (per-label stats)

Read-only against the graph + disk.

Run:  python test_all_labels.py [--samples 5] [--label-only Material]
"""

from __future__ import annotations

import argparse
import gzip
import hashlib
import json
import re
import sys
from collections import defaultdict
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATABASE = "mit-bestand"
CACHE_DIR = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-21_quelle_remediation" / "shared" / "url_bodies"
SYNONYMS_PATH = REPO_ROOT / "_neo4j" / "contracts" / "synonyms.json"
LOG_DIR = THIS_FILE.parent
DETAIL_JSONL = LOG_DIR / "v4_test_all_labels.jsonl"
SUMMARY_JSON = LOG_DIR / "v4_test_all_labels_summary.json"

DENYLIST_LABELS = {
    "Quelle", "Dossier", "ExternalLink", "ResearchDocument", "SectionRef",
    "OntologyAnchor", "DataIssue", "DeprecatedType", "GraphVersion",
    "Land", "Stadt",
}

UTM_PARAMS = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content",
              "fbclid","gclid","mc_cid","mc_eid","_ga"}

TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
SCRIPT_RE = re.compile(r"<(script|style|nav|footer)\b[^>]*>.*?</\1>",
                       re.IGNORECASE | re.DOTALL)
WHITESPACE_RE = re.compile(r"\s+")


# --------------------------------------------------------------------------- #
# Common helpers (shared shape with test_node_link.py + qext_runner)
# --------------------------------------------------------------------------- #

def normalise_url(raw: str) -> str:
    raw = (raw or "").strip().rstrip(".,;:!?")
    try:
        parsed = urlparse(raw)
    except Exception:
        return raw
    scheme = (parsed.scheme or "https").lower()
    netloc = parsed.netloc.lower()
    if (scheme == "https" and netloc.endswith(":443")) or (scheme == "http" and netloc.endswith(":80")):
        netloc = netloc.rsplit(":", 1)[0]
    path = parsed.path.rstrip("/") or "/"
    query_pairs = [(k, v) for k, v in parse_qsl(parsed.query) if k.lower() not in UTM_PARAMS]
    query = urlencode(sorted(query_pairs))
    return urlunparse((scheme, netloc, path, parsed.params, query, ""))


def load_synonym_map() -> dict[str, list[str]]:
    if not SYNONYMS_PATH.exists():
        return {}
    data = json.loads(SYNONYMS_PATH.read_text(encoding="utf-8"))
    syns = data.get("synonyms", {})
    return {k: v for k, v in syns.items()
            if not k.startswith("_") and isinstance(v, list)}


def norm_token_for(name: str) -> str | None:
    m = re.search(r"(\d{3,5}(?:[-:]\d{1,4})?)", name or "")
    return m.group(1) if m else None


def expand_terms(name: str, aliases: list, node_id: str,
                 label: str, synonyms: dict) -> list[str]:
    terms: set[str] = set()
    if name and isinstance(name, str):
        terms.add(name.lower().strip())
    for a in (aliases or []):
        if a and isinstance(a, str):
            terms.add(a.lower().strip())
    if node_id:
        stem = re.sub(r"^(mat|norm|bg|bt|p|q|s|huerde|akt|akr|cert|lcm|prog|rb|rr|wva|wvk|zbs|av|prn|la|md|rsq|vt|bps|bg|hk|lo|pp|mq|mm|nz|bsy|btb|bw|bwe|bzk|de|fw|me|nw|gw|pz|sof|stat|tw|tp|zk)_", "", node_id.lower())
        if stem and stem != node_id.lower():
            terms.add(stem.replace("_", " "))
    for t in list(terms):
        for syn in synonyms.get(t, []):
            if isinstance(syn, str):
                terms.add(syn.lower())
    if label == "Norm" and name:
        tok = norm_token_for(name)
        if tok:
            terms.add(tok.lower())
    return [t for t in terms if len(t) >= 4]


def text_mentions(text: str, terms: list[str]) -> list[str]:
    if not text or not terms:
        return []
    tl = text.lower()
    return [t for t in terms if re.search(rf"\b{re.escape(t)}\b", tl)]


# --------------------------------------------------------------------------- #
# Cache index + page-text extraction
# --------------------------------------------------------------------------- #

def build_url_cache_index() -> dict[str, str]:
    index: dict[str, str] = {}
    for meta_path in CACHE_DIR.glob("*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        url = meta.get("url")
        if not url:
            continue
        body_id = meta_path.stem.replace(".meta", "")
        for ext in (".html", ".html.gz", ".pdf", ".pdf.gz"):
            p = CACHE_DIR / f"{body_id}{ext}"
            if p.exists():
                index[normalise_url(url)] = str(p)
                break
    return index


def read_body(cache_path: str) -> bytes:
    p = Path(cache_path)
    if p.suffix == ".gz":
        with gzip.open(p, "rb") as f:
            return f.read()
    return p.read_bytes()


def html_to_text(html_bytes: bytes) -> str:
    try:
        html = html_bytes.decode("utf-8", errors="replace")
    except Exception:
        html = html_bytes.decode("latin-1", errors="replace")
    html = SCRIPT_RE.sub("", html)
    text = TAG_RE.sub(" ", html)
    text = WHITESPACE_RE.sub(" ", text)
    return text.strip()


def page_text_for(cache_path: str, cache: dict[str, str]) -> str:
    if cache_path in cache:
        return cache[cache_path]
    if cache_path.endswith((".pdf", ".pdf.gz")):
        cache[cache_path] = ""
        return ""
    try:
        text = html_to_text(read_body(cache_path))[:80_000]
    except Exception:
        text = ""
    cache[cache_path] = text
    return text


# --------------------------------------------------------------------------- #
# Per-label sampling + per-node test
# --------------------------------------------------------------------------- #

def get_driver():
    uri, user, password, _db = resolve_connection()
    if not uri:
        sys.exit("Missing Neo4j connection. Check .cursor/mcp.json.")
    return GraphDatabase.driver(uri, auth=(user, password))


def discover_target_labels(s) -> list[str]:
    rows = list(s.run(
        "CALL db.labels() YIELD label "
        "WHERE NOT label IN $deny RETURN label ORDER BY label",
        deny=list(DENYLIST_LABELS),
    ))
    return [r["label"] for r in rows]


def sample_nodes(s, label: str, n: int) -> list[dict]:
    """Sample up to N nodes from the label, preferring those that HAVE source_urls."""
    rows = list(s.run(
        f"MATCH (n:`{label}`) "
        "WHERE n.source_urls IS NOT NULL AND size(coalesce(n.source_urls, [])) > 0 "
        "RETURN n.id AS id, n.name AS name, n.aliases AS aliases, "
        "       n.source_urls AS source_urls "
        "ORDER BY n.source_count DESC, n.id ASC "
        f"LIMIT {n}"
    ))
    if rows:
        return [dict(r) for r in rows]
    # Fallback: if no node in this label has source_urls, sample anyway
    rows = list(s.run(
        f"MATCH (n:`{label}`) "
        "RETURN n.id AS id, n.name AS name, n.aliases AS aliases, "
        "       coalesce(n.source_urls, []) AS source_urls "
        "ORDER BY n.id ASC "
        f"LIMIT {n}"
    ))
    return [dict(r) for r in rows]


def fetch_node_dossier_evidence(s, node_id: str, urls: list[str]) -> list[dict]:
    """For one node, return every (dossier_id, url, locator, d_text) triple."""
    return [dict(r) for r in s.run(
        "MATCH (n {id: $id})-[:BELEGT_IN|HAS_SOURCE_LINK]->(d) "
        "WHERE (d:Dossier OR d:ResearchDocument) "
        "MATCH (d)-[zq:ZITIERT_QUELLE]->(ext:ExternalLink) "
        "WHERE ext.url IN $urls "
        "RETURN ext.url AS url, d.id AS dossier_id, "
        "       zq.locator AS sref, "
        "       coalesce(zq.evidence_excerpt, '') AS d_text",
        id=node_id, urls=urls
    )]


# --------------------------------------------------------------------------- #
# Per-label test
# --------------------------------------------------------------------------- #

def test_one_node(node: dict, label: str, synonyms: dict,
                  url_cache: dict[str, str], page_cache: dict[str, str],
                  triples: list[dict]) -> dict:
    terms = expand_terms(node["name"], node["aliases"], node["id"],
                          label, synonyms)
    if not terms:
        return {
            "node_id": node["id"], "name": node["name"], "label": label,
            "terms": [], "broad_urls": len(node["source_urls"]),
            "BOTH": 0, "D_only": 0, "P_only": 0, "neither": 0,
            "skipped_reason": "no_search_terms",
        }

    BOTH = D_only = P_only = neither = 0
    examples_BOTH: list[dict] = []
    examples_D_only: list[dict] = []

    # Per (URL, dossier) pair — only counts D/P from the dossier-text & page-body
    seen: set[tuple] = set()
    for t in triples:
        key = (t["url"], t["dossier_id"])
        if key in seen:
            continue
        seen.add(key)
        d_hits = text_mentions(t["d_text"], terms)
        cache_path = url_cache.get(normalise_url(t["url"]))
        if cache_path:
            p_text = page_text_for(cache_path, page_cache)
            p_hits = text_mentions(p_text, terms)
        else:
            p_hits = []
        if d_hits and p_hits:
            BOTH += 1
            if len(examples_BOTH) < 2:
                examples_BOTH.append({
                    "url": t["url"], "dossier": t["dossier_id"],
                    "d_terms": d_hits[:3], "p_terms": p_hits[:3]
                })
        elif d_hits and not p_hits:
            D_only += 1
            if len(examples_D_only) < 2:
                examples_D_only.append({
                    "url": t["url"], "dossier": t["dossier_id"],
                    "d_terms": d_hits[:3]
                })
        elif p_hits and not d_hits:
            P_only += 1
        else:
            neither += 1

    return {
        "node_id": node["id"], "name": node["name"], "label": label,
        "terms": terms[:6],
        "broad_urls": len(node["source_urls"]),
        "triples_checked": len(triples),
        "BOTH": BOTH, "D_only": D_only, "P_only": P_only, "neither": neither,
        "examples_BOTH": examples_BOTH,
        "examples_D_only": examples_D_only,
    }


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--samples", type=int, default=5,
                        help="Samples per label (default 5; max 10 recommended)")
    parser.add_argument("--label-only", type=str,
                        help="Restrict to a single label (debug)")
    args = parser.parse_args()

    print(f"Building URL cache index from {CACHE_DIR}...")
    url_cache = build_url_cache_index()
    print(f"  Indexed {len(url_cache)} URLs.")

    synonyms = load_synonym_map()
    print(f"  Loaded {len(synonyms)} synonym entries.")

    page_cache: dict[str, str] = {}

    driver = get_driver()
    per_label: dict[str, list[dict]] = defaultdict(list)
    label_summary: dict[str, dict] = {}

    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as s:
            labels = discover_target_labels(s)
            if args.label_only:
                labels = [args.label_only] if args.label_only in labels else []
            print(f"\nTesting {len(labels)} labels at {args.samples} samples each...\n")

            with DETAIL_JSONL.open("w", encoding="utf-8") as detail_fp:
                for label in labels:
                    samples = sample_nodes(s, label, args.samples)
                    if not samples:
                        per_label[label] = []
                        continue

                    for node in samples:
                        if not node["source_urls"]:
                            per_label[label].append({
                                "node_id": node["id"], "name": node["name"],
                                "label": label, "terms": [],
                                "broad_urls": 0,
                                "BOTH": 0, "D_only": 0, "P_only": 0, "neither": 0,
                                "skipped_reason": "no_source_urls"
                            })
                            continue
                        triples = fetch_node_dossier_evidence(s, node["id"], node["source_urls"])
                        result = test_one_node(node, label, synonyms,
                                                url_cache, page_cache, triples)
                        per_label[label].append(result)
                        detail_fp.write(json.dumps(result, default=str) + "\n")

                    # Per-label summary
                    n_samples = len(samples)
                    n_with_any_BOTH = sum(1 for r in per_label[label] if r["BOTH"] > 0)
                    n_skipped = sum(1 for r in per_label[label]
                                     if r.get("skipped_reason"))
                    total_BOTH = sum(r["BOTH"] for r in per_label[label])
                    total_D_only = sum(r["D_only"] for r in per_label[label])
                    total_triples = sum(r.get("triples_checked", 0) for r in per_label[label])
                    label_summary[label] = {
                        "samples": n_samples,
                        "skipped": n_skipped,
                        "nodes_with_BOTH": n_with_any_BOTH,
                        "total_BOTH": total_BOTH,
                        "total_D_only": total_D_only,
                        "total_triples_checked": total_triples,
                        "pct_nodes_with_BOTH": (
                            round(100 * n_with_any_BOTH / n_samples, 1)
                            if n_samples else 0
                        ),
                    }
                    print(f"  {label:30}  samples={n_samples:>2}  "
                          f"with_BOTH={n_with_any_BOTH:>2}  "
                          f"total_BOTH={total_BOTH:>3}  "
                          f"D_only={total_D_only:>3}  "
                          f"triples={total_triples:>4}")
    finally:
        driver.close()

    # Sort label summary by total BOTH and print final table
    print(f"\n{'=' * 90}")
    print("FINAL TABLE — per-label coverage (sorted by total BOTH desc)")
    print(f"{'=' * 90}")
    print(f"  {'label':30} {'samples':>7} {'with_BOTH':>10} {'%nodes':>7} "
          f"{'tot_BOTH':>9} {'tot_D_only':>11} {'triples':>8}")
    sorted_labels = sorted(label_summary.items(),
                           key=lambda kv: -kv[1]["total_BOTH"])
    for label, stats in sorted_labels:
        print(f"  {label:30} {stats['samples']:>7} "
              f"{stats['nodes_with_BOTH']:>10} {stats['pct_nodes_with_BOTH']:>6}% "
              f"{stats['total_BOTH']:>9} {stats['total_D_only']:>11} "
              f"{stats['total_triples_checked']:>8}")

    # Persist summary
    SUMMARY_JSON.write_text(json.dumps({
        "samples_per_label": args.samples,
        "labels_tested": len(label_summary),
        "url_cache_size": len(url_cache),
        "synonym_entries": len(synonyms),
        "per_label": label_summary,
    }, indent=2, default=str), encoding="utf-8")
    print(f"\nWrote detail: {DETAIL_JSONL.relative_to(REPO_ROOT)}")
    print(f"Wrote summary: {SUMMARY_JSON.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
