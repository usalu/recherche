"""Create compact review batches for relationships flagged by source audit."""

from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
BATCH_DIR = HERE / "manual_batches"


def compact(value: str, limit: int) -> str:
    value = " ".join((value or "").split())
    if len(value) <= limit:
        return value
    return value[: limit - 1].rstrip() + "…"


def main() -> None:
    inventory = json.loads((HERE / "relationship_inventory.json").read_text(encoding="utf-8"))
    audit = json.loads((HERE / "source_access_audit.json").read_text(encoding="utf-8"))
    by_id = {row["review_id"]: row for row in inventory["relationships"]}
    flagged = [row for row in audit["relationships"] if row["requires_manual_source_review"]]
    BATCH_DIR.mkdir(exist_ok=True)
    for old in BATCH_DIR.glob("batch_*.md"):
        old.unlink()
    for index in range(0, len(flagged), 20):
        group = flagged[index : index + 20]
        number = index // 20 + 1
        lines = [
            f"# Manual source review batch {number}",
            "",
            "Review only. Description is display context and must not determine the profile.",
            "",
        ]
        for audited in group:
            row = by_id[audited["review_id"]]
            lines.extend(
                [
                    f"## {row['review_id']}",
                    "",
                    f"- Origin: `{row['origin']}`",
                    f"- Endpoints: {row['source']} → {row['target']}",
                    f"- Kind/type: `{row['relationship_kind']}` / `{row['relationship_type']}`",
                    f"- Proposed profile: `{row['profile_proposal']}`",
                    f"- Stored quote: {compact(row['evidence_quote'], 420)}",
                    f"- Reopened: `{audited['http_status']}`; exact `{audited['quote_exact_match']}`; fuzzy `{audited['quote_fuzzy_match']}`",
                    f"- Source passage: {compact(audited.get('source_snippet', ''), 1100)}",
                    f"- URL: {row['evidence_url']}",
                    "- Decision: `pending`",
                    "",
                ]
            )
        (BATCH_DIR / f"batch_{number:02d}.md").write_text("\n".join(lines), encoding="utf-8")
    print(json.dumps({"flagged": len(flagged), "batches": (len(flagged) + 19) // 20}))


if __name__ == "__main__":
    main()
