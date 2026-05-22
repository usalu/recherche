"""Per-node source linking test — concrete data validation.

For each test node, this script:
  1. Reads the dossier .md file that describes/mentions the node.
  2. Finds URLs cited near the node (parses Markdown links + bare URLs).
  3. Resolves each URL to its cached HTML/PDF body from S2's cache.
  4. Extracts text from the page body.
  5. Tests THREE evidence types per (node, URL) pair:
       D — Dossier-mention: node name appears in dossier text near the URL.
       P — Page-mention:    node name (or synonym) appears in the page body.
       B — Both:            D AND P → CONFIRMED LINK.
  6. Reports a matrix per node type.

This is the ground truth that should drive C4 (page-content match) in v4
of the migration. Read-only against disk; no graph access needed.

Run:  python test_node_link.py
"""

from __future__ import annotations

import gzip
import hashlib
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

CACHE_DIR = REPO_ROOT / "_neo4j" / "intake" / "runs" / "2026-05-21_quelle_remediation" / "shared" / "url_bodies"
SYNONYMS_PATH = REPO_ROOT / "_neo4j" / "contracts" / "synonyms.json"

UTM_PARAMS = {"utm_source","utm_medium","utm_campaign","utm_term","utm_content",
              "fbclid","gclid","mc_cid","mc_eid","_ga"}


def load_synonym_map() -> dict[str, list[str]]:
    """Read the canonical synonyms.json. Filter out _comment_* keys."""
    if not SYNONYMS_PATH.exists():
        return {}
    data = json.loads(SYNONYMS_PATH.read_text(encoding="utf-8"))
    syns = data.get("synonyms", {})
    return {k: v for k, v in syns.items()
            if not k.startswith("_") and isinstance(v, list)}


SYNONYM_MAP = load_synonym_map()
# Add the test-only fixtures that aren't general vocabulary
SYNONYM_MAP.update({
    "rotordc":             ["rotor dc", "rotor deconstruction"],
    "htwg konstanz":       ["htwg", "hochschule konstanz"],
    "klingelhöfer krötsch": ["klingelhoefer-kroetsch", "klingelhoefer kroetsch"],
    "akt ii":              ["akt-uk", "alan baxter"],
    "stuttgart 210":       ["stuttgart 21", "s21", "stuttgart210"],
})

# --------------------------------------------------------------------------- #
# URL normalization (same as S1/S2)
# --------------------------------------------------------------------------- #

def normalise_url(raw: str) -> str:
    raw = raw.strip().rstrip(".,;:!?")
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


def md5_hex(s: str) -> str:
    return hashlib.md5(s.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------- #
# URL cache index (URL → cache_path)
# --------------------------------------------------------------------------- #

def build_url_cache_index() -> dict[str, dict]:
    """Read every .meta.json under CACHE_DIR; return URL → {cache_path, content_type, http_code}."""
    index: dict[str, dict] = {}
    for meta_path in CACHE_DIR.glob("*.meta.json"):
        try:
            meta = json.loads(meta_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        url = meta.get("url")
        if not url:
            continue
        # Cache file: same stem as meta.json, with .html / .html.gz / .pdf / .pdf.gz
        stem = meta_path.stem  # filename without .json — but full name is "<md5>.meta"
        # Actually .meta.json strips .json, leaving "<md5>.meta"; we want <md5>
        body_id = stem.replace(".meta", "")
        body_candidates = [
            CACHE_DIR / f"{body_id}.html",
            CACHE_DIR / f"{body_id}.html.gz",
            CACHE_DIR / f"{body_id}.pdf",
            CACHE_DIR / f"{body_id}.pdf.gz",
        ]
        body_path = next((p for p in body_candidates if p.exists()), None)
        if not body_path:
            continue
        norm = normalise_url(url)
        index[norm] = {
            "url_raw": url,
            "cache_path": str(body_path),
            "content_type": meta.get("content_type", ""),
            "http_code": meta.get("http_code"),
        }
    return index


# --------------------------------------------------------------------------- #
# Page-text extraction (simple — no BeautifulSoup dependency)
# --------------------------------------------------------------------------- #

TAG_RE = re.compile(r"<[^>]+>", re.DOTALL)
SCRIPT_RE = re.compile(r"<(script|style|nav|footer)\b[^>]*>.*?</\1>",
                       re.IGNORECASE | re.DOTALL)
WHITESPACE_RE = re.compile(r"\s+")


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


def extract_page_text(cache_path: str) -> str:
    if cache_path.endswith((".pdf", ".pdf.gz")):
        return ""    # we don't depend on pdfplumber; PDFs reported but not parsed in this test
    body = read_body(cache_path)
    return html_to_text(body)


# --------------------------------------------------------------------------- #
# Dossier parsing — find URLs and the surrounding row
# --------------------------------------------------------------------------- #

MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
ANGLE_URL_RE = re.compile(r"<(https?://[^>]+)>")
BARE_URL_RE = re.compile(r"(?<![\(\[\w])(https?://[^\s<>\"'\)]+)")


def extract_urls_with_context(text: str, radius: int = 400):
    """Yield {url_norm, url_raw, sref, context} for every URL form."""
    for pattern, name in [(MD_LINK_RE, "md"), (ANGLE_URL_RE, "angle"), (BARE_URL_RE, "bare")]:
        for m in pattern.finditer(text):
            if name == "md":
                label, url_raw = m.group(1), m.group(2)
            else:
                label, url_raw = "", m.group(1)
            url_norm = normalise_url(url_raw)
            pos = m.start()
            # row or paragraph
            line_start = text.rfind("\n", 0, pos) + 1
            line_end = text.find("\n", m.end())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end]
            if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
                context = line
            else:
                start = max(0, pos - radius)
                end = min(len(text), m.end() + radius)
                blank_before = text.rfind("\n\n", start, pos)
                if blank_before > -1:
                    start = blank_before + 2
                blank_after = text.find("\n\n", m.end(), end)
                if blank_after > -1:
                    end = blank_after
                context = text[start:end]
            yield {"url_norm": url_norm, "url_raw": url_raw, "sref": label,
                   "context": context.replace("\n", " ").strip()}


# --------------------------------------------------------------------------- #
# Node-term mention check (D or P)
# --------------------------------------------------------------------------- #

def expand_node_terms(name: str) -> list[str]:
    terms = {name.lower()}
    for syn in SYNONYM_MAP.get(name.lower(), []):
        terms.add(syn.lower())
    return [t for t in terms if len(t) >= 3]


def text_mentions(text: str, terms: list[str]) -> tuple[bool, list[str]]:
    text_lower = text.lower()
    hits: list[str] = []
    for t in terms:
        pattern = rf"\b{re.escape(t)}\b"
        if re.search(pattern, text_lower):
            hits.append(t)
    return len(hits) > 0, hits


# --------------------------------------------------------------------------- #
# Test fixtures — 2 to 5 nodes per type
# --------------------------------------------------------------------------- #

DOSSIERS = {
    "stuttgart_210": REPO_ROOT / "_neo4j" / "intake" / "archive" /
                     "2026-05-20_inbox_batch2_import" / "raw_tree" /
                     "DE_AT_CH_graph_ready_dossiers" / "Stuttgart_210.md",
    "holbein": REPO_ROOT / "_archive" / "research" / "gebaeude" /
               "Holbein_Gardens_London.md",
    "k118": REPO_ROOT / "_archive" / "research" / "gebaeude" /
            "K118_Kopfbau_Halle_118_Winterthur.md",
    "circl_pavilion": REPO_ROOT / "_neo4j" / "intake" / "archive" /
                      "2026-05-20_inbox_batch2_import" / "raw_tree" /
                      "BE_NL_graph_ready_dossiers" / "Circl_Pavilion_Amsterdam.md",
}

# (label, node_name, dossier_key)
TEST_NODES = [
    # Material
    ("Material", "Holz",       "stuttgart_210"),
    ("Material", "Beton",      "stuttgart_210"),
    ("Material", "Stahl",      "holbein"),
    ("Material", "Stahl",      "k118"),
    # Norm
    ("Norm",     "CEN/TS 1090-201", "holbein"),
    ("Norm",     "EN 1090",         "holbein"),
    # Bauteilgruppe (use the descriptive name from the dossier)
    ("Bauteilgruppe", "Schalungselement", "stuttgart_210"),
    ("Bauteilgruppe", "formwork",         "stuttgart_210"),  # English variant
    # Akteur
    ("Akteur", "HTWG Konstanz",        "stuttgart_210"),
    ("Akteur", "Klingelhöfer Krötsch", "stuttgart_210"),
    ("Akteur", "AKT II",                "holbein"),
    ("Akteur", "Baubüro in situ",       "k118"),
    # Schadstoff
    ("Schadstoff", "Asbest", "holbein"),
    # Projekt (top-level sanity)
    ("Projekt", "Stuttgart 210", "stuttgart_210"),
    ("Projekt", "Holbein Gardens", "holbein"),
    ("Projekt", "K118",            "k118"),
]


# --------------------------------------------------------------------------- #
# Test loop
# --------------------------------------------------------------------------- #

def run_test(url_index: dict[str, dict]):
    print(f"\n{'=' * 84}")
    print(f"  URL cache index: {len(url_index)} URLs")
    print(f"  Test nodes:       {len(TEST_NODES)}")
    print(f"{'=' * 84}")

    by_type: dict[str, list] = {}

    for label, node_name, dossier_key in TEST_NODES:
        dossier_path = DOSSIERS[dossier_key]
        if not dossier_path.exists():
            print(f"  SKIP missing dossier: {dossier_path}")
            continue

        text = dossier_path.read_text(encoding="utf-8")
        terms = expand_node_terms(node_name)
        urls_in_dossier = list(extract_urls_with_context(text))

        # Per-URL evidence
        per_url = []
        for u in urls_in_dossier:
            d_hit, d_terms = text_mentions(u["context"], terms)
            cache_entry = url_index.get(u["url_norm"])
            if cache_entry:
                page_text = extract_page_text(cache_entry["cache_path"])
                p_hit, p_terms = text_mentions(page_text[:80_000], terms)  # cap for perf
            else:
                p_hit, p_terms = False, []
            per_url.append({
                "url": u["url_norm"],
                "sref": u["sref"],
                "d_hit": d_hit,
                "d_terms": d_terms,
                "p_hit": p_hit,
                "p_terms": p_terms,
                "cached": cache_entry is not None,
            })

        # Summary per node
        d_only = sum(1 for r in per_url if r["d_hit"] and not r["p_hit"])
        p_only = sum(1 for r in per_url if r["p_hit"] and not r["d_hit"])
        both   = sum(1 for r in per_url if r["d_hit"] and r["p_hit"])
        neither = sum(1 for r in per_url if not r["d_hit"] and not r["p_hit"])
        cached_count = sum(1 for r in per_url if r["cached"])

        result = {
            "label": label,
            "node_name": node_name,
            "dossier": dossier_key,
            "terms": terms,
            "urls_total": len(per_url),
            "urls_cached": cached_count,
            "D_only": d_only,
            "P_only": p_only,
            "BOTH": both,
            "neither": neither,
            "examples_both": [
                {"url": r["url"], "sref": r["sref"],
                 "d_terms": r["d_terms"], "p_terms": r["p_terms"]}
                for r in per_url if r["d_hit"] and r["p_hit"]
            ][:3],
            "examples_d_only": [
                {"url": r["url"], "sref": r["sref"], "d_terms": r["d_terms"]}
                for r in per_url if r["d_hit"] and not r["p_hit"]
            ][:3],
            "examples_p_only": [
                {"url": r["url"], "p_terms": r["p_terms"], "cached": r["cached"]}
                for r in per_url if r["p_hit"] and not r["d_hit"]
            ][:3],
        }
        by_type.setdefault(label, []).append(result)

    # Print report
    for label, results in by_type.items():
        print(f"\n--- {label} -------------------------------------------------")
        for r in results:
            print(f"\n  {r['node_name']:25} (in {r['dossier']})")
            print(f"    terms tested:    {r['terms']}")
            print(f"    URLs in dossier: {r['urls_total']} ({r['urls_cached']} cached for page check)")
            print(f"    BOTH  (D+P) — CONFIRMED LINK: {r['BOTH']}")
            print(f"    D only (dossier claim, page does NOT confirm): {r['D_only']}")
            print(f"    P only (page mentions, but dossier did not cite here): {r['P_only']}")
            print(f"    neither: {r['neither']}")
            for ex in r["examples_both"]:
                print(f"      ✓ CONFIRMED: {ex['url']}  [sref={ex['sref']}]")
                print(f"          d_terms={ex['d_terms']}   p_terms={ex['p_terms']}")
            for ex in r["examples_d_only"]:
                print(f"      ~ DOSSIER-ONLY: {ex['url']}  [sref={ex['sref']}]")
                print(f"          d_terms={ex['d_terms']}")

    # Aggregate
    total = sum(len(rs) for rs in by_type.values())
    print(f"\n{'=' * 84}")
    print(f"  Aggregate: {total} test nodes processed")
    print(f"{'=' * 84}")


def main():
    print("Building URL cache index from S2's shared/url_bodies/...")
    idx = build_url_cache_index()
    print(f"  Indexed {len(idx)} URLs (raw → cached body path)")
    run_test(idx)


if __name__ == "__main__":
    main()
