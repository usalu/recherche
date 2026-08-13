# -*- coding: utf-8 -*-
"""Apply complete cross-review proposals to lane files after review.

The script preserves primary reviewer attribution, records the verifier and
marks every resulting record cross_review_complete. It refuses partial review
files and writes an audit snapshot before replacing a lane file.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
ROUTES = {"A": "C", "B": "A", "C": "B"}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def main(argv: list[str]) -> int:
    targets = argv[1:] or list("ABC")
    for target in targets:
        reviewer = ROUTES.get(target)
        if not reviewer:
            raise SystemExit(f"unknown target lane: {target}")
        lane_path = HERE / f"lane_{target}.json"
        review_path = HERE / f"cross_{reviewer}_reviews_{target}.json"
        if not lane_path.exists() or not review_path.exists():
            raise SystemExit(f"missing lane or cross-review for {target}")
        lane = load(lane_path)
        review = load(review_path)
        reviews = review.get("reviews") or []
        by_eid = {r["eid"]: r for r in reviews}
        records = lane["records"]
        expected = {r["eid"] for r in records}
        if len(by_eid) != len(reviews) or set(by_eid) != expected:
            raise SystemExit(
                f"cross-review {review_path.name} must cover all {len(expected)} EIDs exactly once"
            )
        updated = []
        for original in records:
            finding = by_eid[original["eid"]]
            status = finding.get("status")
            if status == "accept":
                result = dict(original)
            elif status == "change":
                proposed = finding.get("proposed_record")
                if not isinstance(proposed, dict) or proposed.get("eid") != original["eid"]:
                    raise SystemExit(f"invalid proposed record for {original['audit_id']}")
                result = proposed
            else:
                raise SystemExit(f"invalid cross-review status for {original['audit_id']}")
            result["primary_reviewer"] = target
            result["verified_by"] = reviewer
            result["review_status"] = "cross_review_complete"
            updated.append(result)
        audit_path = HERE / f"lane_{target}_primary_snapshot.json"
        if not audit_path.exists():
            audit_path.write_text(
                json.dumps(lane, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
            )
        lane["records"] = updated
        lane_path.write_text(json.dumps(lane, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        changes = sum(1 for r in reviews if r.get("status") == "change")
        print(f"lane {target}: {len(updated)} cross-reviewed, {changes} changed")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
