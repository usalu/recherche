"""Reconnect orphan sources using in-graph signals (node-id provenance).

Many orphan external_reference nodes carry ids of the form `q_<case>_s<N>` which
directly encode the case markdown Quelle (`q_<case>_md`) they were extracted
from. That is a precise, in-graph link (no fuzzy domain guessing). For every such
orphan whose parent case exists and is connected, emit a
(case)-[:HAS_SOURCE_LINK]->(orphan) edge.

Opaque orphans (`q_url_<hash>`, `q_ext_<domain>_<slug>`) carry no reliable
in-graph case signal and are reported as needing data-driven reconnection.

Writes only the patch + report; apply via apply_neo4j_review_patch.py.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402

SREF_RE = re.compile(r"^(q_.+)_s\d+$")


def run(out_dir: Path) -> dict:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            orphans = [
                {"id": r["id"], "url": r["url"]}
                for r in session.run(
                    "MATCH (o) WHERE NOT (o)--() AND (o:Quelle OR o:ExternalLink) "
                    "RETURN o.id AS id, o.url AS url"
                )
            ]
            connected_ids = {
                r["id"]
                for r in session.run(
                    "MATCH (q:Quelle) WHERE EXISTS { (q)--() } RETURN q.id AS id"
                )
            }
    finally:
        driver.close()

    patch: list[dict] = []
    reasons: Counter = Counter()
    linked_cases: Counter = Counter()
    for o in orphans:
        m = SREF_RE.match(o["id"])
        if not m:
            reasons["no_sref_id_signal"] += 1
            continue
        case_id = m.group(1) + "_md"
        if case_id not in connected_ids:
            reasons["parent_case_not_connected"] += 1
            continue
        reasons["linked_via_case_id"] += 1
        linked_cases[case_id] += 1
        patch.append({
            "op": "add_rel",
            "from": case_id,
            "type": "HAS_SOURCE_LINK",
            "to": o["id"],
            "properties": {"id": f"r_{case_id}__HAS_SOURCE_LINK__{o['id']}"},
        })

    out_dir.mkdir(parents=True, exist_ok=True)
    patch_path = out_dir / "orphan_ingraph_link.patch.jsonl"
    with patch_path.open("w", encoding="utf-8", newline="\n") as f:
        for line in patch:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")

    summary = {
        "orphans_total": len(orphans),
        "linked_via_case_id": reasons["linked_via_case_id"],
        "distinct_parent_cases": len(linked_cases),
        "parent_case_not_connected": reasons["parent_case_not_connected"],
        "no_sref_id_signal": reasons["no_sref_id_signal"],
        "patch_lines": len(patch),
    }
    (out_dir / "INGRAPH_LINK_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or (
        repo_root() / "_neo4j" / "review" / "2026-06-01_orphan_ingraph_link"
    )
    summary = run(out_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
