# -*- coding: utf-8 -*-
"""Audit the approved report-only cleanup and document graph deltas."""
from __future__ import annotations

import json
import os
import sys
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
NETZ_ROOT = BASE.parents[1] / "netz"
sys.path.insert(0, str(NETZ_ROOT))

from netz.cli import load_network  # noqa: E402


BASELINE = {
    "organizations": 762,
    "projects": 97,
    "nodes": 859,
    "edges": 570,
}
FORBIDDEN = {
    "Keine direkte Reuse-Rolle belegt",
    "Reuse-Bezug belegt, Rolle unklar",
    "Unzureichende Informationen",
    "Referenzprojekt, Reuse-Umfang unklar",
}


def main() -> int:
    manifest = json.loads((HERE / "input_manifest.json").read_text(encoding="utf-8"))
    if not manifest.get("approved_for_render_prune"):
        print("REFUSED: strict review is not approved")
        return 2
    final_path = BASE / "klassifikation_final.json"
    if not final_path.exists():
        print("REFUSED: run finalize_strict_review.py first")
        return 2
    classification = json.loads(final_path.read_text(encoding="utf-8"))
    net = load_network()
    per_country = {}
    actors = projects = edges = 0
    drawn_eids = set()
    for cc, panel in net.panels.items():
        a, p, e = len(panel.actors), len(panel.projects), len(panel.edges)
        if a or p:
            per_country[cc] = {"organizations": a, "projects": p, "nodes": a + p, "edges": e}
        actors += a; projects += p; edges += e
        drawn_eids.update(panel.actors); drawn_eids.update(panel.projects)

    errors = []
    if drawn_eids != set(classification):
        errors.append(
            f"drawn/classification EID mismatch: drawn={len(drawn_eids)} "
            f"classification={len(classification)}"
        )
    for eid, row in classification.items():
        if set(row.get("rollen") or []) & FORBIDDEN:
            errors.append(f"{eid}: forbidden fallback remains")
        if "…" in row.get("name", "") or row.get("name", "").rstrip().endswith("..."):
            errors.append(f"{eid}: truncated name remains")

    final_counts = {
        "organizations": actors,
        "projects": projects,
        "nodes": actors + projects,
        "edges": edges,
    }
    audit = {
        "baseline": BASELINE,
        "final": final_counts,
        "delta": {key: final_counts[key] - BASELINE[key] for key in BASELINE},
        "per_country": per_country,
        "unplaced": list(net.res.unplaced),
        "errors": errors,
    }
    (BASE / "strict_cleanup_network_audit.json").write_text(
        json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    lines = [
        "# Strict-Cleanup-Netzprüfung", "",
        "| Kennzahl | Vorher | Nachher | Delta |", "|---|---:|---:|---:|",
    ]
    for key in ("organizations", "projects", "nodes", "edges"):
        lines.append(f"| {key} | {BASELINE[key]} | {final_counts[key]} | {audit['delta'][key]:+d} |")
    lines.extend(["", "## Länder", "", "| Land | Organisationen | Projekte | Knoten | Kanten |", "|---|---:|---:|---:|---:|"])
    for cc, counts in sorted(per_country.items()):
        lines.append(
            f"| {cc} | {counts['organizations']} | {counts['projects']} | "
            f"{counts['nodes']} | {counts['edges']} |"
        )
    lines.extend(["", f"Unplatzierte EIDs: {len(net.res.unplaced)}", f"Fehler: {len(errors)}", ""])
    (BASE / "STRICT_CLEANUP_NETWORK_AUDIT.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"nodes={final_counts['nodes']} edges={edges} errors={len(errors)}")
    for error in errors[:20]:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
