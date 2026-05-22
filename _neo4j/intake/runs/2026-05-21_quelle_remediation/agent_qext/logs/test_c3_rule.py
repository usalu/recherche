"""Local test harness for Q-EXT.C v2 confirmation rules.

Tests C1/C2/C3 logic against ACTUAL extracted text from the research files
and dossiers. Reports false positives and false negatives so we can refactor
the migration before running it against the live db.

This is read-only. Doesn't touch the graph.

Run:  python test_c3_rule.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]   # repo root is 'recherche', 6 levels up

# Force stdout to UTF-8 on Windows so check/cross marks render
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Mirror S1's extraction: capture ~120 chars around each URL.
MD_LINK_RE = re.compile(r"\[([^\]]+)\]\((https?://[^\s)]+)\)")
BARE_URL_RE = re.compile(r"(?<![\(\[\w])(https?://[^\s<>\"'\)]+)")
ANGLE_URL_RE = re.compile(r"<(https?://[^>]+)>")  # research files use this form a lot

# Mirror C3: word-boundary case-insensitive match
def c3_match(needle: str, excerpt: str) -> tuple[bool, str]:
    """Return (matched, regex_used)."""
    if not needle or len(needle) < 4:
        return False, f"needle too short ({len(needle)} chars)"
    # Escape regex metachars in the needle (current migration does NOT do this — BUG)
    pattern_naive = f"(?i)\\b{needle}\\b"
    pattern_escaped = f"(?i)\\b{re.escape(needle)}\\b"
    try:
        m_naive = re.search(pattern_naive, excerpt) is not None
    except re.error:
        m_naive = "regex_error"
    m_escaped = re.search(pattern_escaped, excerpt) is not None
    return m_escaped, pattern_escaped


def extract_urls_and_context(text: str, context_chars: int = 120):
    """Yield (url, surrounding_text) for every URL form."""
    for pattern, name in [(MD_LINK_RE, "md_link"),
                          (ANGLE_URL_RE, "angle"),
                          (BARE_URL_RE, "bare")]:
        for m in pattern.finditer(text):
            url = m.group(2) if name == "md_link" else m.group(1)
            start = max(0, m.start() - context_chars)
            end = min(len(text), m.end() + context_chars)
            yield {
                "url": url,
                "kind": name,
                "surrounding": text[start:end].replace("\n", " ").strip(),
            }


def test_against_research_file(filepath: Path, sample_names: list[str], context_chars: int = 120):
    """Extract URLs from a research file, test C3 match for each sample name."""
    text = filepath.read_text(encoding="utf-8")
    results = []
    for record in extract_urls_and_context(text, context_chars=context_chars):
        for name in sample_names:
            matched, regex = c3_match(name.lower(), record["surrounding"])
            results.append({
                "node_name": name,
                "url": record["url"],
                "kind": record["kind"],
                "matched": matched,
                "surrounding_preview": record["surrounding"][:200],
            })
    return results


def summarise(file_label: str, results: list[dict], sample_names: list[str]):
    print(f"\n{'=' * 78}")
    print(f"File: {file_label}")
    print(f"URLs extracted: {len({r['url'] for r in results})}")
    print(f"Sample node names tested: {sample_names}")
    print(f"{'=' * 78}")

    by_name: dict[str, dict] = {n: {"hits": 0, "misses": 0, "example_hit": None, "example_miss": None}
                                 for n in sample_names}
    for r in results:
        n = r["node_name"]
        if r["matched"]:
            by_name[n]["hits"] += 1
            if not by_name[n]["example_hit"]:
                by_name[n]["example_hit"] = (r["url"], r["surrounding_preview"])
        else:
            by_name[n]["misses"] += 1
            if not by_name[n]["example_miss"]:
                by_name[n]["example_miss"] = (r["url"], r["surrounding_preview"])

    for name, stats in by_name.items():
        total = stats["hits"] + stats["misses"]
        if total == 0:
            continue
        pct = stats["hits"] / total * 100 if total > 0 else 0
        print(f"\n  '{name}': {stats['hits']}/{total} matched ({pct:.0f} %)")
        if stats["example_hit"]:
            u, s = stats["example_hit"]
            print(f"    ✓ {u}")
            print(f"      …{s[:180]}…")
        if stats["example_miss"]:
            u, s = stats["example_miss"]
            print(f"    ✗ {u}")
            print(f"      …{s[:180]}…")


SAMPLE_MATERIAL_NAMES = ["Stahl", "Holz", "Beton", "Ziegel", "Naturstein", "Lehm",
                         "Aluminium", "Glas", "Dämmstoff", "Stahlbeton"]

# Names that intentionally contain regex special chars — to expose the
# escaping bug in the current C3 migration.
SAMPLE_NORM_NAMES = ["CEN/TS 1090-201", "DIN EN 1090-2", "EN 1168", "SIA 263",
                     "NS 3682:2022", "Eurocode 5"]

# Short names that should be REJECTED (< 4 chars) per the migration's filter.
SAMPLE_TOO_SHORT = ["AT", "EU", "Pb", "PCB", "PAH"]


def test_word_boundary_false_positives():
    """German compound words must NOT match a short stem."""
    cases = [
        # (needle, text, expected_match)
        ("holz", "Holzbauoffensive", False),       # compound — should NOT match
        ("holz", "Verkleidung aus Holz", True),    # standalone — should match
        ("stahl", "Stahltragwerk", False),         # compound — should NOT match
        ("stahl", "reused Stahl from donor", True),
        ("stahl", "STAHL", True),                  # case insensitive
        ("beton", "Stahlbeton", False),            # SUBSTRING — \b should reject
        ("beton", "Recycling-Beton", True),        # dash IS word boundary
        ("aluminium", "Aluminium-Profil", True),
    ]
    print(f"\n{'=' * 78}")
    print("Word-boundary false-positive sanity tests")
    print(f"{'=' * 78}")
    for needle, text, expected in cases:
        matched, _ = c3_match(needle, text)
        verdict = "✓" if matched == expected else "✗ BUG"
        print(f"  {verdict} needle={needle!r} text={text!r} → matched={matched}, expected={expected}")


def test_special_char_names():
    """Names with /, -, :, spaces — current migration's apoc.text.regexGroups
    truncates to first \\w\\s+ run. Test the FIX (re.escape) behaviour."""
    test_excerpt = (
        "CEN/TS defines reuse assessment and declared mechanical/geometrical "
        "properties and weldability; SCI protocol covers data, inspection and "
        "testing. Source: <https://standards.iteh.ai/.../cen-ts-1090-201-2024>"
    )
    print(f"\n{'=' * 78}")
    print("Special-character name tests")
    print(f"  Excerpt: {test_excerpt[:120]}…")
    print(f"{'=' * 78}")
    for name in SAMPLE_NORM_NAMES:
        matched, regex = c3_match(name.lower(), test_excerpt)
        print(f"  needle={name!r:25} matched={matched}  regex={regex}")


def main():
    research_dir = REPO_ROOT / "_neo4j" / "intake" / "inbox" / "research"
    test_files = [
        research_dir / "circular_construction_reuse_graph_gaps.md",
        research_dir / "missing_underused_norm_nodes_reuse_kg.md",
        research_dir / "aufbereitungsverfahren_reused_building_elements.md",
    ]
    for f in test_files:
        if not f.exists():
            print(f"SKIP (not found): {f}")
            continue
        results = test_against_research_file(f, SAMPLE_MATERIAL_NAMES)
        summarise(f.name, results, SAMPLE_MATERIAL_NAMES)

    test_word_boundary_false_positives()
    test_special_char_names()

    # Also test the rejection of too-short names
    print(f"\n{'=' * 78}")
    print("Short-name rejection (must reject all of: AT, EU, Pb, PCB, PAH)")
    print(f"{'=' * 78}")
    for name in SAMPLE_TOO_SHORT:
        matched, regex = c3_match(name.lower(), "Reuse in AT and EU with PCB and PAH contamination")
        verdict = "✓ correctly skipped" if not matched else "✗ FALSE POSITIVE"
        print(f"  {verdict}: needle={name!r} → matched={matched}, regex={regex}")


if __name__ == "__main__":
    main()
