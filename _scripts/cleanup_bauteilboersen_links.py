"""Clean reciprocal Bauteilboersen/materialhub actor links in live Neo4j.

This is intentionally narrow:
- only VERBUNDEN_MIT_AKTEUR reciprocal pairs touching a Materialhub/Bauteilboerse
  actor or bauteilnetz_deutschland are considered;
- one direction is kept and annotated;
- the removed inverse relationship is archived to a JSONL ledger before delete;
- high-risk duplicate BELEGT_IN/CITED_* relationships are not touched.

Usage:
  python _scripts/cleanup_bauteilboersen_links.py --dry-run
  python _scripts/cleanup_bauteilboersen_links.py --apply
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


RUN_ID = "2026-05-28_bauteilboersen_cleanup"
RUN_DIR = repo_root() / "_neo4j" / "intake" / "runs" / RUN_ID


def json_safe(value: Any) -> Any:
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    if isinstance(value, dict):
        return {str(k): json_safe(v) for k, v in value.items()}
    if isinstance(value, (list, tuple)):
        return [json_safe(v) for v in value]
    return str(value)


CANDIDATES = """
MATCH (a:Akteur)-[r_ab:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
MATCH (b)-[r_ba:VERBUNDEN_MIT_AKTEUR]->(a)
WHERE elementId(a) < elementId(b)
WITH a, b, r_ab, r_ba,
     EXISTS {
       MATCH (a)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     } AS a_is_hub,
     EXISTS {
       MATCH (b)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     } AS b_is_hub
WHERE a_is_hub OR b_is_hub
   OR a.id = "bauteilnetz_deutschland"
   OR b.id = "bauteilnetz_deutschland"
WITH a, b, r_ab, r_ba, a_is_hub, b_is_hub,
     CASE
       WHEN a_is_hub AND NOT b_is_hub THEN "a"
       WHEN b_is_hub AND NOT a_is_hub THEN "b"
       WHEN a.id = "bauteilnetz_deutschland" AND NOT b_is_hub THEN "a"
       WHEN b.id = "bauteilnetz_deutschland" AND NOT a_is_hub THEN "b"
       WHEN coalesce(a.id, "") <= coalesce(b.id, "") THEN "a"
       ELSE "b"
     END AS keep_side
RETURN
  a.id AS a_id,
  a.name AS a_name,
  b.id AS b_id,
  b.name AS b_name,
  a_is_hub,
  b_is_hub,
  CASE keep_side WHEN "a" THEN elementId(r_ab) ELSE elementId(r_ba) END AS keep_rel_element_id,
  CASE keep_side WHEN "a" THEN elementId(r_ba) ELSE elementId(r_ab) END AS drop_rel_element_id,
  CASE keep_side WHEN "a" THEN a.id ELSE b.id END AS keep_from_id,
  CASE keep_side WHEN "a" THEN b.id ELSE a.id END AS keep_to_id,
  CASE keep_side WHEN "a" THEN properties(r_ab) ELSE properties(r_ba) END AS keep_props,
  CASE keep_side WHEN "a" THEN properties(r_ba) ELSE properties(r_ab) END AS drop_props
ORDER BY keep_from_id, keep_to_id
"""


APPLY_ONE = """
MATCH ()-[keep:VERBUNDEN_MIT_AKTEUR]->()
WHERE elementId(keep) = $keep_rel_element_id
MATCH ()-[drop:VERBUNDEN_MIT_AKTEUR]->()
WHERE elementId(drop) = $drop_rel_element_id
SET keep.cleanup_bauteilboersen_bidirectional_dedup_run = $run_id,
    keep.cleanup_bauteilboersen_bidirectional_dedup_at = $applied_at,
    keep.cleanup_bauteilboersen_removed_inverse_rel_ids =
      coalesce(keep.cleanup_bauteilboersen_removed_inverse_rel_ids, []) + [$drop_rel_element_id],
    keep.cleanup_bauteilboersen_inverse_ledger = $ledger_path
DELETE drop
RETURN count(*) AS deleted
"""


POST_COUNTS = """
MATCH (a:Akteur)-[r_ab:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)
MATCH (b)-[r_ba:VERBUNDEN_MIT_AKTEUR]->(a)
WHERE elementId(a) < elementId(b)
WITH a, b,
     EXISTS {
       MATCH (a)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     } AS a_is_hub,
     EXISTS {
       MATCH (b)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: "at_materialhub_bauteilboerse"})
     } AS b_is_hub
WHERE a_is_hub OR b_is_hub
   OR a.id = "bauteilnetz_deutschland"
   OR b.id = "bauteilnetz_deutschland"
RETURN count(*) AS reciprocal_pairs_remaining
"""


def load_candidates(session) -> list[dict[str, Any]]:
    return [json_safe(dict(record)) for record in session.run(CANDIDATES)]


def write_json(path: Path, payload: Any) -> None:
    path.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--dry-run", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    RUN_DIR.mkdir(parents=True, exist_ok=True)
    mode_name = "apply" if args.apply else "dry_run"
    candidates_path = RUN_DIR / f"{mode_name}_reciprocal_candidates.json"
    ledger_path = RUN_DIR / "removed_inverse_relationships.jsonl"
    report_path = RUN_DIR / f"{mode_name}_report.json"
    applied_at = datetime.now(timezone.utc).isoformat()

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            candidates = load_candidates(session)
            write_json(candidates_path, candidates)

            deleted = 0
            if args.apply:
                with ledger_path.open("w", encoding="utf-8", newline="\n") as f:
                    for candidate in candidates:
                        f.write(
                            json.dumps(
                                {
                                    "run_id": RUN_ID,
                                    "archived_at": applied_at,
                                    "deleted_relationship": {
                                        "element_id": candidate["drop_rel_element_id"],
                                        "type": "VERBUNDEN_MIT_AKTEUR",
                                        "from_id": candidate["keep_to_id"],
                                        "to_id": candidate["keep_from_id"],
                                        "properties": candidate["drop_props"],
                                    },
                                    "kept_relationship": {
                                        "element_id": candidate["keep_rel_element_id"],
                                        "type": "VERBUNDEN_MIT_AKTEUR",
                                        "from_id": candidate["keep_from_id"],
                                        "to_id": candidate["keep_to_id"],
                                        "properties_before": candidate["keep_props"],
                                    },
                                },
                                ensure_ascii=False,
                                sort_keys=True,
                            )
                            + "\n"
                        )
                        result = session.run(
                            APPLY_ONE,
                            keep_rel_element_id=candidate["keep_rel_element_id"],
                            drop_rel_element_id=candidate["drop_rel_element_id"],
                            run_id=RUN_ID,
                            applied_at=applied_at,
                            ledger_path=str(ledger_path).replace("\\", "/"),
                        ).single()
                        deleted += int(result["deleted"] if result else 0)

            remaining = session.run(POST_COUNTS).single()["reciprocal_pairs_remaining"]

    finally:
        driver.close()

    report = {
        "run_id": RUN_ID,
        "mode": mode_name,
        "database": database,
        "candidate_count": len(candidates),
        "deleted_inverse_relationships": deleted,
        "reciprocal_pairs_remaining": remaining,
        "candidates": str(candidates_path),
        "ledger": str(ledger_path) if args.apply else None,
        "applied_at": applied_at if args.apply else None,
        "backup_required": "_neo4j/review/backups/2026-05-28_pre_bauteilboersen_cleanup",
    }
    write_json(report_path, report)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
