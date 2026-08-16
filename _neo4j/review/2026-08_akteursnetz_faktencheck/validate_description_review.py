# -*- coding: utf-8 -*-
"""Fail-closed validation for the 570-row description review package."""
from __future__ import annotations

import hashlib
import json
from collections import Counter
from pathlib import Path


BASE = Path(__file__).resolve().parent
REVIEW = BASE / "relationship_description_review"
PROPOSALS = REVIEW / "proposals.json"
MANIFEST = REVIEW / "approval_manifest.json"
MAX_DESCRIPTION = 60
BANNED = (
    "die quelle belegt", "der akteur", "beide sind als", "die kante",
    "die zusammenarbeit ist", "in einem benannten", "auftragsleistung",
)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    errors: list[str] = []
    doc = json.loads(PROPOSALS.read_text(encoding="utf-8"))
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    rows = doc.get("records") or []
    ids = [row.get("id") for row in rows]

    if len(rows) != 570 or len(set(ids)) != 570:
        errors.append(f"coverage is not 570 unique IDs: rows={len(rows)} unique={len(set(ids))}")
    if manifest.get("proposal_sha256") != digest(PROPOSALS):
        errors.append("proposal hash does not match approval manifest")
    if doc.get("approved_for_apply") is not False:
        errors.append("proposal document is not locked for review")
    if manifest.get("approved_for_apply") is not False:
        errors.append("approval manifest is not locked for review")

    for relative, expected in manifest.get("source_hashes", {}).items():
        path = BASE / relative
        if not path.is_file() or digest(path) != expected:
            errors.append(f"source hash mismatch: {path}")
    for filename, expected in manifest.get("protected_output_hashes", {}).items():
        path = Path(filename)
        if not path.is_file() or digest(path) != expected:
            errors.append(f"protected canonical output changed: {path}")

    batch_files = sorted((REVIEW / "batches").glob("kanten_*.md"))
    if len(batch_files) != 34:
        errors.append(f"expected 34 review batches, found {len(batch_files)}")
    batch_counts = Counter(row.get("batch") for row in rows)
    if any(count > 20 for count in batch_counts.values()) or len(batch_counts) != 34:
        errors.append("batch partition is not 34 batches of at most 20 rows")

    allowed_status = {"ready", "needs_source", "type_conflict", "removal"}
    for row in rows:
        rid = row.get("id", "<missing>")
        text = row.get("proposed_description") or ""
        if row.get("character_count") != len(text):
            errors.append(f"{rid}: stored character count is wrong")
        if not text or len(text) > MAX_DESCRIPTION:
            errors.append(f"{rid}: invalid description length {len(text)}")
        if text and text[-1] not in ".!?":
            errors.append(f"{rid}: missing terminal punctuation")
        if any(term in text.casefold() for term in BANNED):
            errors.append(f"{rid}: banned or non-concrete wording")
        if "\n" in text or "|" in text or chr(0x2026) in text:
            errors.append(f"{rid}: unsafe or clipped description text")
        status = row.get("review_status")
        if status not in allowed_status:
            errors.append(f"{rid}: invalid review status {status!r}")
        if status == "needs_source" and not row.get("source_recheck"):
            errors.append(f"{rid}: needs_source lacks documented source recheck")
        if status == "type_conflict":
            unchanged = (
                row.get("type") == row.get("proposed_type") and
                row.get("direction") == row.get("proposed_direction") and
                row.get("current_remove") == row.get("proposed_remove")
            )
            if unchanged:
                errors.append(f"{rid}: type_conflict proposes no classification change")
        if row.get("approved") is not False:
            errors.append(f"{rid}: row was approved outside the approval gate")

    visible = [row for row in rows if row.get("currently_visible")]
    if len(visible) != 268:
        errors.append(f"expected 268 currently visible rows, found {len(visible)}")

    status = Counter(row.get("review_status") for row in rows)
    print(
        f"description-review rows={len(rows)} batches={len(batch_files)} "
        f"visible={len(visible)} maxlen={max(map(lambda row: len(row['proposed_description']), rows))} "
        f"ready={status['ready']} needs_source={status['needs_source']} "
        f"type_conflict={status['type_conflict']} removal={status['removal']} "
        f"errors={len(errors)}"
    )
    for error in errors:
        print(f"ERROR: {error}")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
