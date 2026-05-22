"""unfold_all_gebaeude.py — run the unfolder over ALL 76 gebäude dossiers.

Imports unfold_dossier from test_gebaeude_unfolder.py. Writes a full triple
log + per-dossier summary so the v6 plan can be refactored with concrete
extraction numbers.

Read-only. Does not touch the graph.

Output:
  - unfold_all_gebaeude_triples.jsonl   (one triple per line)
  - unfold_all_gebaeude_summary.json    (per-dossier + global stats)

Run:  python unfold_all_gebaeude.py
"""

from __future__ import annotations

import json
import sys
from collections import defaultdict
from pathlib import Path

THIS_FILE = Path(__file__).resolve()
REPO_ROOT = THIS_FILE.parents[6]
sys.path.insert(0, str(THIS_FILE.parent))

# noinspection PyUnresolvedReferences
from test_gebaeude_unfolder import unfold_dossier, GEBAEUDE_DIR  # type: ignore

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def main():
    dossiers = sorted(GEBAEUDE_DIR.glob("*.md"))
    print(f"Unfolding {len(dossiers)} gebäude dossiers...\n")

    triples_path = THIS_FILE.parent / "unfold_all_gebaeude_triples.jsonl"
    summary_path = THIS_FILE.parent / "unfold_all_gebaeude_summary.json"

    all_summaries = []
    global_per_section = defaultdict(int)
    global_per_kind = defaultdict(int)
    global_per_entity_type = defaultdict(int)
    global_distinct_urls = set()
    global_distinct_entities = set()
    grand_total = 0
    dossiers_with_zero_triples = []
    dossiers_with_zero_quellen = []
    total_rows_no_quelle = 0
    total_rows_unresolved = 0

    with triples_path.open("w", encoding="utf-8") as tf:
        for p in dossiers:
            result = unfold_dossier(p)
            triples = result.get("triples", [])

            for tr in triples:
                tf.write(json.dumps(tr, ensure_ascii=False) + "\n")
                global_distinct_urls.add(tr["url"])
                global_distinct_entities.add(
                    (tr["entity_type"], tr["entity_value"].lower())
                )

            grand_total += len(triples)
            total_rows_no_quelle += result["rows_with_no_quelle"]
            total_rows_unresolved += result["rows_with_quelle_but_no_resolved_url"]
            for sec, n in result["per_section"].items():
                global_per_section[sec] += n
            for k, n in result["per_kind"].items():
                global_per_kind[k] += n
            for et, n in result["per_entity_type"].items():
                global_per_entity_type[et] += n
            if len(triples) == 0:
                dossiers_with_zero_triples.append(p.name)
            if result["s_refs_in_quellen_list"] == 0:
                dossiers_with_zero_quellen.append(p.name)

            all_summaries.append({
                "dossier_file": p.name,
                "dossier_id": p.stem.lower(),
                "quellen_entries_resolved": result["s_refs_in_quellen_list"],
                "triples": len(triples),
                "per_section": result["per_section"],
                "rows_no_quelle": result["rows_with_no_quelle"],
                "rows_unresolved": result["rows_with_quelle_but_no_resolved_url"],
            })

    summary = {
        "n_dossiers": len(dossiers),
        "grand_total_triples": grand_total,
        "distinct_urls": len(global_distinct_urls),
        "distinct_entities": len(global_distinct_entities),
        "dossiers_with_zero_triples_count": len(dossiers_with_zero_triples),
        "dossiers_with_zero_triples": dossiers_with_zero_triples,
        "dossiers_with_zero_quellen": dossiers_with_zero_quellen,
        "global_per_section": dict(sorted(global_per_section.items(),
                                          key=lambda kv: -kv[1])),
        "global_per_kind": dict(sorted(global_per_kind.items(),
                                       key=lambda kv: -kv[1])),
        "global_per_entity_type": dict(sorted(global_per_entity_type.items(),
                                              key=lambda kv: -kv[1])),
        "total_rows_no_quelle": total_rows_no_quelle,
        "total_rows_unresolved": total_rows_unresolved,
        "per_dossier": all_summaries,
    }
    summary_path.write_text(json.dumps(summary, indent=2, ensure_ascii=False),
                            encoding="utf-8")

    print(f"{'=' * 84}")
    print(f"  GLOBAL SUMMARY — {len(dossiers)} gebäude dossiers")
    print(f"{'=' * 84}")
    print(f"  Total triples extracted:        {grand_total}")
    print(f"  Distinct URLs:                  {len(global_distinct_urls)}")
    print(f"  Distinct (entity_type, value):  {len(global_distinct_entities)}")
    print(f"  Dossiers with ZERO triples:     {len(dossiers_with_zero_triples)}")
    print(f"  Dossiers with ZERO Quellen:     {len(dossiers_with_zero_quellen)}")
    print(f"  Rows skipped (no Quelle col):   {total_rows_no_quelle}")
    print(f"  Rows skipped (unresolved sref): {total_rows_unresolved}")
    print()
    print(f"  Per-section totals:")
    for sec, n in sorted(global_per_section.items(), key=lambda kv: -kv[1]):
        print(f"    {sec:40} {n:>5}")
    print()
    print(f"  Per-kind totals:")
    for kind, n in sorted(global_per_kind.items(), key=lambda kv: -kv[1]):
        print(f"    {kind:25} {n:>5}")
    print()
    print(f"  Top 20 entity types in §2:")
    for et, n in list(sorted(global_per_entity_type.items(),
                             key=lambda kv: -kv[1]))[:20]:
        print(f"    {et:35} {n:>5}")
    print()
    if dossiers_with_zero_triples:
        print(f"  Still-zero dossiers ({len(dossiers_with_zero_triples)}):")
        for name in dossiers_with_zero_triples:
            print(f"    - {name}")
    print()
    print(f"Triple log:  {triples_path.relative_to(REPO_ROOT)}")
    print(f"Summary:     {summary_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
