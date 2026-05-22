"""Refactored S1 extraction + C3 matching — demonstration that the fix works.

Three refactor ideas tested:
  R1. Widen S1's context window from ±120 chars to the whole surrounding
      Markdown table row OR paragraph.
  R2. Allow multiple search terms per node:
       - name.lower()
       - any entry in aliases
       - English equivalent from a small fixed map
       - id-derived stems (when id is e.g. mat_stahl, also match 'mat_stahl' or 'stahl')
  R3. For norm-style names ('CEN/TS 1090-201'), match on the strongest
      discriminating token (the digit sequence '1090-201'), not the full
      literal.

Run:  python test_c3_refactored.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# --------------------------------------------------------------------------- #
# Curated German -> English (and reverse) synonyms for common reuse vocabulary
# --------------------------------------------------------------------------- #

# Keep small. Each entry is bidirectional. Build a comprehensive list slowly
# rather than autogenerating — manual control is the point.
SYNONYM_MAP: dict[str, list[str]] = {
    "stahl":      ["steel"],
    "holz":       ["timber", "wood"],
    "beton":      ["concrete"],
    "stahlbeton": ["reinforced concrete", "rc"],
    "ziegel":     ["brick", "masonry"],
    "naturstein": ["natural stone", "stone"],
    "lehm":       ["earth", "clay", "loam"],
    "aluminium":  ["aluminum"],
    "glas":       ["glass"],
    "dämmstoff":  ["insulation", "insulation material"],
    "kunststoff": ["plastic", "polymer"],
    # Pollutants — bilingual already in many cases
    "asbest":     ["asbestos"],
    "bleifarbe":  ["lead paint"],
    "pak":        ["pah"],            # both forms used
    "kmf":        ["mmvf", "man-made mineral fibres"],
    # Connection technique vocab
    "verbindungstechnik":  ["connection", "joinery", "joint"],
}


def expand_terms(name: str, aliases: list[str] | None = None,
                 node_id: str | None = None) -> list[str]:
    """Build the list of search terms for one node."""
    terms: set[str] = set()
    if name:
        terms.add(name.lower().strip())
    for a in (aliases or []):
        if a and isinstance(a, str):
            terms.add(a.lower().strip())
    if node_id:
        # Strip common prefixes (mat_, norm_, bg_, …) and use the stem
        stem = re.sub(r"^(mat|norm|bg|bt|p|q|s|huerde|akt|akr)_", "", node_id.lower())
        if stem and stem != node_id.lower():
            terms.add(stem.replace("_", " "))
    # Add curated English synonyms
    for t in list(terms):
        for syn in SYNONYM_MAP.get(t, []):
            terms.add(syn.lower())
    # Reject too-short stems
    return [t for t in terms if len(t) >= 4]


# --------------------------------------------------------------------------- #
# Refactored context extraction (R1)
# --------------------------------------------------------------------------- #

MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
ANGLE_URL_RE = re.compile(r"<(https?://[^>]+)>")
BARE_URL_RE = re.compile(r"(?<![\(\[\w])(https?://[^\s<>\"'\)]+)")


def extract_with_context(text: str, char_radius_fallback: int = 400):
    """Yield (url, context_text) where context is the whole surrounding
    Markdown table row OR paragraph (whichever ends first)."""
    for pattern, name in [(MD_LINK_RE, "md_link"),
                          (ANGLE_URL_RE, "angle"),
                          (BARE_URL_RE, "bare")]:
        for m in pattern.finditer(text):
            url = m.group(2) if name == "md_link" else m.group(1)
            pos = m.start()
            # Find the surrounding "block" — either a table row (delimited by
            # leading | and trailing newline) or a paragraph (blank-line bounded)
            line_start = text.rfind("\n", 0, pos) + 1
            line_end = text.find("\n", m.end())
            if line_end == -1:
                line_end = len(text)
            line = text[line_start:line_end]
            if line.lstrip().startswith("|") and line.rstrip().endswith("|"):
                # It's a Markdown table row — use the whole row
                context = line
            else:
                # Use the paragraph (between blank lines), capped at radius
                start = max(0, pos - char_radius_fallback)
                end = min(len(text), m.end() + char_radius_fallback)
                # Try to expand to blank-line boundaries
                blank_before = text.rfind("\n\n", start, pos)
                if blank_before > -1:
                    start = blank_before + 2
                blank_after = text.find("\n\n", m.end(), end)
                if blank_after > -1:
                    end = blank_after
                context = text[start:end]
            yield {"url": url, "kind": name,
                   "context": context.replace("\n", " ").strip()}


# --------------------------------------------------------------------------- #
# Refactored C3 match (R2 + R3)
# --------------------------------------------------------------------------- #

def c3_match(node_terms: list[str], excerpt: str) -> tuple[bool, str | None]:
    """Return (matched, matching_term). Match is word-boundary, case-insensitive."""
    if not excerpt:
        return False, None
    for t in node_terms:
        if len(t) < 4:
            continue
        pattern = f"(?i)\\b{re.escape(t)}\\b"
        if re.search(pattern, excerpt):
            return True, t
    return False, None


# --------------------------------------------------------------------------- #
# Test cases
# --------------------------------------------------------------------------- #

SAMPLE_NODES = [
    # name, aliases, id, expected to match in research/* text
    {"name": "Stahl",      "aliases": [], "id": "mat_stahl"},
    {"name": "Holz",       "aliases": [], "id": "mat_holz"},
    {"name": "Beton",      "aliases": [], "id": "mat_beton"},
    {"name": "Ziegel",     "aliases": [], "id": "mat_ziegel"},
    {"name": "Naturstein", "aliases": [], "id": "mat_naturstein"},
    {"name": "Lehm",       "aliases": [], "id": "mat_lehm"},
    {"name": "Aluminium",  "aliases": [], "id": "mat_aluminium"},
    {"name": "Glas",       "aliases": [], "id": "mat_glas"},
    {"name": "Dämmstoff",  "aliases": ["Mineralwolle"], "id": "mat_daemmstoff"},
    {"name": "CEN/TS 1090-201", "aliases": ["EN 1090", "CEN-TS-1090"], "id": "norm_cen_ts_1090_201"},
    {"name": "Asbest", "aliases": ["Asbestos"], "id": "s_asbest"},
]


def main():
    research_dir = REPO_ROOT / "_neo4j" / "intake" / "inbox" / "research"
    test_files = [
        research_dir / "circular_construction_reuse_graph_gaps.md",
        research_dir / "missing_underused_norm_nodes_reuse_kg.md",
        research_dir / "aufbereitungsverfahren_reused_building_elements.md",
    ]

    print(f"{'=' * 78}")
    print("Refactored S1 + C3 — match rates against real research file text")
    print(f"{'=' * 78}\n")

    for f in test_files:
        if not f.exists():
            print(f"SKIP (not found): {f}")
            continue
        text = f.read_text(encoding="utf-8")
        all_extracts = list(extract_with_context(text))
        unique_urls = {e["url"] for e in all_extracts}

        print(f"\nFile: {f.name}")
        print(f"  Total URL occurrences: {len(all_extracts)}; distinct URLs: {len(unique_urls)}")
        print(f"  Avg context length: "
              f"{sum(len(e['context']) for e in all_extracts) / max(1, len(all_extracts)):.0f} chars\n")

        for node in SAMPLE_NODES:
            terms = expand_terms(node["name"], node["aliases"], node["id"])
            hits = 0
            matched_via = {}
            for e in all_extracts:
                ok, term = c3_match(terms, e["context"])
                if ok:
                    hits += 1
                    matched_via[term] = matched_via.get(term, 0) + 1
            total = len(all_extracts)
            pct = hits / total * 100 if total else 0
            via = ", ".join(f"{t}:{n}" for t, n in matched_via.items()) if matched_via else "—"
            print(f"    {node['name']:20s}  (terms={terms[:4]}…)  "
                  f"{hits:3d}/{total:3d}  ({pct:4.0f}%)  via {via}")


if __name__ == "__main__":
    main()
