# -*- coding: utf-8 -*-
"""Create report-only strict-cleanup artifacts after explicit approval."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def lane_records(path: Path):
    data = load(path)
    return data if isinstance(data, list) else data["records"]


def main() -> int:
    check = subprocess.run([sys.executable, str(HERE / "validate_strict_review.py")])
    if check.returncode:
        return check.returncode
    manifest = load(HERE / "input_manifest.json")
    if not manifest.get("approved_for_render_prune"):
        print("REFUSED: approved_for_render_prune is false; review artifacts remain inactive")
        return 2

    records = []
    for lane in "ABC":
        records.extend(lane_records(HERE / f"lane_{lane}.json"))
    by_eid = {r["eid"]: r for r in records}
    source = load(BASE / "klassifikation.json")

    pruned = sorted(eid for eid, r in by_eid.items() if r["decision"] in {"prune", "merge"})
    redirects = {
        eid: r["merge_target_eid"] for eid, r in by_eid.items() if r["decision"] == "merge"
    }
    overrides = {}
    final = {}
    programmes = {}
    actor_project = {}
    provenance = []
    for eid, rec in by_eid.items():
        provenance.append(rec)
        if rec["decision"] != "keep":
            continue
        old = source[eid]
        roles = rec["roles"]
        final[eid] = {
            **old,
            "name": rec.get("corrected_name") or rec["current_name"],
            "rolle": " / ".join(roles),
            "rollen": roles,
            "relevanz": rec["relevance"],
            "evidence": rec["evidence"],
            "reuse_objects": rec.get("reuse_objects") or [],
            "strict_review": True,
        }
        if rec.get("corrected_type"):
            final[eid]["report_entity_type"] = rec["corrected_type"]
        if rec.get("corrected_type") == "Programm":
            programmes[eid] = final[eid]
        else:
            actor_project[eid] = final[eid]
        override = {
            key: rec.get(key) for key in ("corrected_name", "corrected_type", "corrected_country")
            if rec.get(key)
        }
        if override:
            overrides[eid] = override

    outputs = {
        "prune_strict_final.json": pruned,
        "merge_redirects_strict.json": redirects,
        "report_overrides_strict.json": overrides,
        "klassifikation_final.json": final,
        "programme_strict_final.json": programmes,
        "klassifikation_actor_project_final.json": actor_project,
        "prune_strict_provenance.json": {
            "schema_version": 1,
            "approved": True,
            "records": provenance,
        },
    }
    for name, data in outputs.items():
        (BASE / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(
        f"final kept={len(final)} programmes={len(programmes)} "
        f"actor_or_project={len(final) - len(programmes)} removed_or_merged={len(pruned)}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
