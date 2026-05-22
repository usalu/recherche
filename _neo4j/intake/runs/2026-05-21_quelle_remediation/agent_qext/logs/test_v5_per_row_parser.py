"""test_v5_per_row_parser.py — prove the per-row parser idea works.

Reads one dossier .md, builds a node-index from the live graph, walks every
table row + prose section, and reports per-label how many new :BELEGT_IN
triples would emerge.

Read-only against the graph; no mutations.

Run:  python test_v5_per_row_parser.py [--dossier Stuttgart_210.md]
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

from neo4j import GraphDatabase

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]
sys.path.insert(0, str(REPO_ROOT / "_scripts"))
# noinspection PyUnresolvedReferences
from neo4j_env import resolve_connection  # type: ignore

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

DATABASE = "mit-bestand"
SYNONYMS_PATH = REPO_ROOT / "_neo4j" / "contracts" / "synonyms.json"

DENYLIST_LABELS = {
    "Quelle", "Dossier", "ExternalLink", "ResearchDocument", "SectionRef",
    "OntologyAnchor", "DataIssue", "DeprecatedType", "GraphVersion",
    "Land", "Stadt",
}


# --------------------------------------------------------------------------- #
# Markdown parsing
# --------------------------------------------------------------------------- #

SECTION_RE = re.compile(r"^##+\s+(.+?)\s*$", re.MULTILINE)
URL_RE = re.compile(r"https?://[^\s<>\"'\)\]]+")


def split_into_sections(text: str) -> list[dict]:
    """Return list of {title, content_start, content}."""
    positions = [(m.start(), m.group(1).strip()) for m in SECTION_RE.finditer(text)]
    if not positions:
        return [{"title": "(root)", "content": text}]
    sections = []
    for i, (pos, title) in enumerate(positions):
        start = text.find("\n", pos) + 1
        end = positions[i + 1][0] if i + 1 < len(positions) else len(text)
        sections.append({"title": title, "content": text[start:end]})
    return sections


def is_table(content: str) -> bool:
    """Quick check: does this section contain a Markdown table?"""
    lines = content.strip().split("\n")
    table_lines = sum(1 for ln in lines
                      if ln.strip().startswith("|") and ln.strip().endswith("|"))
    return table_lines >= 3   # header + separator + at least one data row


def parse_table(content: str) -> tuple[list[str], list[list[str]]]:
    """Return (headers, rows). Each row is a list of cell strings."""
    lines = [ln for ln in content.strip().split("\n")
             if ln.strip().startswith("|") and ln.strip().endswith("|")]
    if len(lines) < 2:
        return ([], [])
    headers = [c.strip() for c in lines[0].strip("|").split("|")]
    rows: list[list[str]] = []
    # Skip the separator row (---|---|---)
    for ln in lines[2:]:
        cells = [c.strip() for c in ln.strip("|").split("|")]
        rows.append(cells)
    return headers, rows


# --------------------------------------------------------------------------- #
# Node index
# --------------------------------------------------------------------------- #

def load_synonyms() -> dict[str, list[str]]:
    if not SYNONYMS_PATH.exists():
        return {}
    data = json.loads(SYNONYMS_PATH.read_text(encoding="utf-8"))
    return {k: v for k, v in data.get("synonyms", {}).items()
            if not k.startswith("_") and isinstance(v, list)}


def get_driver():
    uri, user, password, _db = resolve_connection()
    return GraphDatabase.driver(uri, auth=(user, password))


def build_node_index(s, synonyms: dict[str, list[str]]) -> dict[str, dict]:
    """For every non-denylisted node: id → {label, name, terms}."""
    index: dict[str, dict] = {}
    rows = list(s.run(
        "MATCH (n) WHERE n.id IS NOT NULL "
        "WITH n, [l IN labels(n) WHERE NOT l IN $deny] AS keep "
        "WHERE size(keep) > 0 "
        "RETURN n.id AS id, keep[0] AS label, "
        "       coalesce(n.name, n.id) AS name, "
        "       coalesce(n.aliases, []) AS aliases",
        deny=list(DENYLIST_LABELS),
    ))
    for r in rows:
        terms: set[str] = set()
        for src in [r["name"], *r["aliases"]]:
            if src and isinstance(src, str):
                t = src.lower().strip()
                if len(t) >= 4:
                    terms.add(t)
        # Add curated synonyms keyed on the lowercased name
        name_key = (r["name"] or "").lower().strip()
        for syn in synonyms.get(name_key, []):
            if isinstance(syn, str) and len(syn) >= 4:
                terms.add(syn.lower())
        # Stem (e.g., mat_stahl → 'stahl')
        stem = re.sub(r"^(mat|norm|bg|bt|p|q|s|huerde|akt|akr|cert|lcm|prog|rb|rr|wva|wvk|zbs|av|prn|la|md|rsq|vt|bps|hk|lo|pp|mq|mm|nz|bsy|btb|bw|bwe|bzk|de|fw|me|nw|gw|pz|sof|stat|tw|tp|zk)_", "",
                      (r["id"] or "").lower())
        if stem and stem != (r["id"] or "").lower():
            t = stem.replace("_", " ")
            if len(t) >= 4:
                terms.add(t)
        if terms:
            index[r["id"]] = {
                "label": r["label"],
                "name": r["name"],
                "terms": list(terms),
            }
    return index


# --------------------------------------------------------------------------- #
# Per-row matching
# --------------------------------------------------------------------------- #

def find_mentioned_nodes(text: str, node_index: dict[str, dict],
                         label_filter: set[str] | None = None) -> list[tuple[str, str]]:
    """Return list of (node_id, matched_term) for nodes whose terms appear in text."""
    tl = text.lower()
    hits: list[tuple[str, str]] = []
    for node_id, info in node_index.items():
        if label_filter and info["label"] not in label_filter:
            continue
        for term in info["terms"]:
            if re.search(rf"\b{re.escape(term)}\b", tl):
                hits.append((node_id, term))
                break  # one match per node is enough
    return hits


# --------------------------------------------------------------------------- #
# Test driver
# --------------------------------------------------------------------------- #

def test_dossier(s, dossier_path: Path, node_index: dict[str, dict]):
    print(f"\n{'=' * 84}")
    print(f"Dossier: {dossier_path.name}")
    print(f"  Node-index size: {len(node_index)} candidate terms")
    print(f"{'=' * 84}")

    text = dossier_path.read_text(encoding="utf-8")
    sections = split_into_sections(text)
    print(f"  Sections found: {len(sections)}")

    # Tally per (label, section)
    label_section_hits: dict[tuple[str, str], list[dict]] = defaultdict(list)
    row_url_count = 0
    total_belegt_in = 0

    for section in sections:
        title = section["title"][:50]
        if is_table(section["content"]):
            headers, rows = parse_table(section["content"])
            for row_idx, cells in enumerate(rows):
                row_text = " ".join(cells)
                hits = find_mentioned_nodes(row_text, node_index)
                urls_in_row = URL_RE.findall(row_text)
                row_url_count += len(urls_in_row)
                for node_id, term in hits:
                    label = node_index[node_id]["label"]
                    label_section_hits[(label, title)].append({
                        "node_id": node_id,
                        "term": term,
                        "row_idx": row_idx,
                        "headers": headers[:3],
                        "urls_in_row": urls_in_row[:3],
                    })
                    total_belegt_in += 1
        else:
            # Prose section
            hits = find_mentioned_nodes(section["content"], node_index)
            urls = URL_RE.findall(section["content"])
            row_url_count += len(urls)
            for node_id, term in hits:
                label = node_index[node_id]["label"]
                label_section_hits[(label, title)].append({
                    "node_id": node_id,
                    "term": term,
                    "section": title,
                    "urls_in_section": urls[:3],
                })
                total_belegt_in += 1

    print(f"\n  Total URLs in dossier: {row_url_count}")
    print(f"  Total :BELEGT_IN edges that would be emitted: {total_belegt_in}")
    print(f"  Distinct (label, section) pairs hit: {len(label_section_hits)}\n")

    # Aggregate by label
    by_label: dict[str, dict] = defaultdict(
        lambda: {"hits": 0, "distinct_nodes": set(), "sections": set()})
    for (label, section), records in label_section_hits.items():
        by_label[label]["hits"] += len(records)
        by_label[label]["distinct_nodes"].update(r["node_id"] for r in records)
        by_label[label]["sections"].add(section)

    print(f"  {'label':30}  {'hits':>6} {'distinct_nodes':>14} {'sections':>10}")
    print(f"  {'-' * 28:30}  {'-' * 6:>6} {'-' * 14:>14} {'-' * 10:>10}")
    for label, stats in sorted(by_label.items(), key=lambda kv: -kv[1]["hits"]):
        print(f"  {label:30}  {stats['hits']:>6} "
              f"{len(stats['distinct_nodes']):>14} {len(stats['sections']):>10}")

    # Spot examples per label (3 max)
    print(f"\n  --- Example matches per label ---")
    for label in sorted({k[0] for k in label_section_hits}):
        examples = []
        for (lbl, section), records in label_section_hits.items():
            if lbl != label:
                continue
            for r in records[:1]:
                examples.append((section, r))
            if len(examples) >= 3:
                break
        if not examples:
            continue
        print(f"\n  {label}:")
        for section, r in examples[:3]:
            term = r.get("term", "?")
            urls = r.get("urls_in_row") or r.get("urls_in_section") or []
            node_id = r.get("node_id", "")
            row = r.get("row_idx")
            print(f"    {node_id:35}  term='{term}'  section='{section[:30]}'  "
                  f"row={row if row is not None else '-'}  urls_in_context={len(urls)}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dossier", default="Stuttgart_210.md",
                        help="Dossier filename to test (default: Stuttgart_210.md)")
    args = parser.parse_args()

    candidates = list((REPO_ROOT / "_neo4j" / "intake" / "archive" /
                       "2026-05-20_inbox_batch2_import" / "raw_tree").rglob(args.dossier))
    if not candidates:
        candidates = list((REPO_ROOT / "_archive" / "research" / "gebaeude").rglob(args.dossier))
    if not candidates:
        sys.exit(f"Dossier {args.dossier} not found.")

    print(f"Testing dossier: {candidates[0]}")

    synonyms = load_synonyms()
    print(f"Loaded {len(synonyms)} synonym entries.")

    driver = get_driver()
    try:
        with driver.session(database=DATABASE, default_access_mode="READ") as s:
            node_index = build_node_index(s, synonyms)
            test_dossier(s, candidates[0], node_index)
    finally:
        driver.close()


if __name__ == "__main__":
    main()
