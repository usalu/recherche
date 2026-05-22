"""Generate a Quelle dedup plan: one canonical node per normalized URL.

Round 2, Phase H. 994+ URLs are duplicated across thousands of Quelle nodes
(no uniqueness on url). This groups every Quelle by normalized URL and emits
`merge_node` records (handled by apply_neo4j_review_patch.py, which redirects all
relationships onto the survivor, unions labels/props, then deletes the duplicate)
so no link is lost. After the merge, raw `url` values are unique and a uniqueness
constraint can be added.

Survivor selection per URL group:
  1. richest quelltyp (case/actor/research markdown beats bare external links)
  2. highest degree (keep the well-connected node id)
  3. lexicographically smallest id (deterministic)

Read-only: writes only the patch file.
"""

from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from build_url_entity_index import normalize_url  # noqa: E402
from neo4j_env import repo_root, resolve_connection  # noqa: E402

# Lower rank = preferred survivor.
TYPE_RANK = {
    "case_markdown": 0,
    "actor_registry_markdown": 0,
    "research_markdown": 1,
    "external_reference": 3,
    "external_link": 4,
    "external_link_from_actor_registry": 4,
}


def rank(quelltyp: str | None) -> int:
    return TYPE_RANK.get(quelltyp or "", 2)


def run(out_dir: Path) -> dict:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            rows = list(
                session.run(
                    "MATCH (q:Quelle) WHERE q.url IS NOT NULL "
                    "RETURN q.id AS id, q.url AS url, q.quelltyp AS quelltyp, "
                    "COUNT { (q)--() } AS degree"
                )
            )
    finally:
        driver.close()

    groups: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        nurl = normalize_url(r["url"])
        if nurl:
            groups[nurl].append(
                {"id": r["id"], "url": r["url"], "quelltyp": r["quelltyp"], "degree": int(r["degree"])}
            )

    merges: list[dict] = []
    dup_groups = 0
    nodes_removed = 0
    for nurl, members in groups.items():
        if len(members) < 2:
            continue
        dup_groups += 1
        survivor = sorted(
            members, key=lambda m: (rank(m["quelltyp"]), -m["degree"], m["id"])
        )[0]
        for m in members:
            if m["id"] == survivor["id"]:
                continue
            merges.append({"op": "merge_node", "from": m["id"], "to": survivor["id"]})
            nodes_removed += 1

    out_dir.mkdir(parents=True, exist_ok=True)
    patch_path = out_dir / "quelle_dedup.patch.jsonl"
    with patch_path.open("w", encoding="utf-8", newline="\n") as f:
        for m in merges:
            f.write(json.dumps(m, ensure_ascii=False) + "\n")

    summary = {
        "quelle_with_url": len(rows),
        "distinct_normalized_urls": len(groups),
        "duplicate_groups": dup_groups,
        "merge_records": len(merges),
        "nodes_removed_after_merge": nodes_removed,
        "patch": str(patch_path),
    }
    (out_dir / "DEDUP_SUMMARY.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return summary


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or (
        repo_root() / "_neo4j" / "review" / "2026-06-01_quelle_dedup"
    )
    summary = run(out_dir)
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
