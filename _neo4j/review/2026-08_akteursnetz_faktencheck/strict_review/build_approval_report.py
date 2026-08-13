# -*- coding: utf-8 -*-
"""Build the user-facing approval report from cross-reviewed lane records."""
from __future__ import annotations

import json
from collections import Counter, defaultdict
from pathlib import Path


HERE = Path(__file__).resolve().parent


def load_records(lane: str):
    data = json.loads((HERE / f"lane_{lane}.json").read_text(encoding="utf-8"))
    return data["records"]


def esc(value) -> str:
    return str(value or "").replace("|", "\\|").replace("\n", " ")


def main() -> None:
    records = [r for lane in "ABC" for r in load_records(lane)]
    if len(records) != 859 or len({r["eid"] for r in records}) != 859:
        raise SystemExit("Expected 859 unique records")
    if any(r.get("review_status") != "cross_review_complete" for r in records):
        raise SystemExit("Cross-review is incomplete")

    counts = Counter(r["decision"] for r in records)
    by_country = defaultdict(Counter)
    for r in records:
        country = r.get("corrected_country") or r["audit_id"].split(":", 1)[0]
        by_country[country][r["decision"]] += 1

    lines = [
        "# Freigabeliste: Harter Research-only-Cleanup", "",
        "**Status: geprüft, aber nicht für Semio aktiviert.**", "",
        f"- Behalten: {counts['keep']}",
        f"- Entfernen: {counts['prune']}",
        f"- Zusammenführen: {counts['merge']}",
        f"- Erwarteter finaler Bestand nach Freigabe: {counts['keep']}", "",
        "## Ergebnis nach Land", "",
        "| Land | Behalten | Entfernen | Zusammenführen |", "|---|---:|---:|---:|",
    ]
    for cc, c in sorted(by_country.items()):
        lines.append(f"| {cc} | {c['keep']} | {c['prune']} | {c['merge']} |")

    lines.extend([
        "", "## Behalten", "",
        "| ID | Name | Rolle(n) | Relevanz |", "|---|---|---|---|",
    ])
    for r in sorted((x for x in records if x["decision"] == "keep"), key=lambda x: x["audit_id"]):
        lines.append(
            f"| {esc(r['audit_id'])} | {esc(r.get('corrected_name') or r['current_name'])} | "
            f"{esc(' / '.join(r.get('roles') or []))} | {esc(r.get('relevance'))} |"
        )

    lines.extend([
        "", "## Entfernen", "",
        "| ID | Name | Begründung |", "|---|---|---|",
    ])
    for r in sorted((x for x in records if x["decision"] == "prune"), key=lambda x: x["audit_id"]):
        lines.append(
            f"| {esc(r['audit_id'])} | {esc(r.get('corrected_name') or r['current_name'])} | "
            f"{esc(', '.join(r.get('reason_codes') or []))} |"
        )

    lines.extend([
        "", "## Zusammenführen", "",
        "| ID | Name | Ziel-EID | Begründung |", "|---|---|---|---|",
    ])
    for r in sorted((x for x in records if x["decision"] == "merge"), key=lambda x: x["audit_id"]):
        lines.append(
            f"| {esc(r['audit_id'])} | {esc(r['current_name'])} | {esc(r['merge_target_eid'])} | "
            f"{esc(', '.join(r.get('reason_codes') or []))} |"
        )

    corrected = [
        r for r in records if r["decision"] == "keep" and any(
            r.get(k) for k in ("corrected_name", "corrected_type", "corrected_country")
        )
    ]
    lines.extend([
        "", "## Behalten mit Identitätskorrektur", "",
        "| ID | Name | Neuer Name | Typ | Land |", "|---|---|---|---|---|",
    ])
    for r in sorted(corrected, key=lambda x: x["audit_id"]):
        lines.append(
            f"| {esc(r['audit_id'])} | {esc(r['current_name'])} | {esc(r.get('corrected_name'))} | "
            f"{esc(r.get('corrected_type'))} | {esc(r.get('corrected_country'))} |"
        )

    lines.extend([
        "", "## Freigaberegel", "",
        "Erst nach ausdrücklicher Freigabe wird `approved_for_render_prune` aktiviert. ",
        "Danach erzeugt der Finalizer die report-spezifische Prune-Liste, finale Klassifikation, ",
        "Merge-Weiterleitungen und Semio-Overrides. Neo4j bleibt unverändert.", "",
    ])
    (HERE / "APPROVAL_REVIEW.md").write_text("\n".join(lines), encoding="utf-8")
    summary = {
        "approved_for_render_prune": False,
        "records": len(records),
        "decisions": dict(counts),
        "expected_final_nodes": counts["keep"],
        "countries": {cc: dict(c) for cc, c in sorted(by_country.items())},
    }
    (HERE / "approval_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(summary, ensure_ascii=False))


if __name__ == "__main__":
    main()
