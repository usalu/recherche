# -*- coding: utf-8 -*-
"""Fail-closed validator for strict-review lane decisions."""
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
HERE = Path(__file__).resolve().parent
FALLBACKS = {
    "Keine direkte Reuse-Rolle belegt",
    "Reuse-Bezug belegt, Rolle unklar",
    "Unzureichende Informationen",
    "Referenzprojekt, Reuse-Umfang unklar",
}
ALLOWED_DECISIONS = {"keep", "prune", "merge"}
ALLOWED_SCOPES = {"actual_reuse", "direct_enabler", "none", "future_design_only"}
ALLOWED_STATUS = {"active", "historical", "project"}
PROJECT_ROLE = "Referenzprojekt"
LANES = {"A": {"AT", "CH", "DE", "FI", "NO"}, "B": {"BE", "DK", "FR"}, "C": {"GB", "NL", "SE"}}


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def records_from_lane(data):
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("records"), list):
        return data["records"]
    raise ValueError("lane JSON must be a list or an object with records[]")


def main() -> int:
    errors = []
    manifest = load(HERE / "input_manifest.json")
    current = {
        rel: digest(BASE / rel)
        for rel in manifest["inputs"]
        if (BASE / rel).exists()
    }
    for rel, expected in manifest["inputs"].items():
        if rel not in current:
            errors.append(f"frozen input missing: {rel}")
        elif current[rel] != expected:
            errors.append(f"frozen input changed: {rel}")

    classification = load(BASE / "klassifikation.json")
    taxonomy = (BASE / "KLASSIFIKATION_TAXONOMIE.md").read_text(encoding="utf-8")
    vocabulary = set(re.findall(r"^###\s+`([^`]+)`\s*$", taxonomy, re.M))
    vocabulary -= FALLBACKS
    expected_eids = set(classification)
    all_records = []
    for lane, countries in LANES.items():
        path = HERE / f"lane_{lane}.json"
        if not path.exists():
            errors.append(f"missing lane file: {path.name}")
            continue
        try:
            lane_records = records_from_lane(load(path))
        except Exception as exc:
            errors.append(f"invalid {path.name}: {exc}")
            continue
        for rec in lane_records:
            if not isinstance(rec, dict):
                errors.append(f"{path.name}: every records[] item must be an object")
                continue
            eid = rec.get("eid")
            base = classification.get(eid)
            if base and base["cc"] not in countries:
                errors.append(f'{rec.get("audit_id")}: wrong lane {lane}')
            if rec.get("primary_reviewer") != lane:
                errors.append(f'{rec.get("audit_id")}: primary_reviewer must be {lane}')
        all_records.extend(rec for rec in lane_records if isinstance(rec, dict))

    by_eid = {}
    for rec in all_records:
        eid = rec.get("eid")
        aid = rec.get("audit_id", eid or "<missing>")
        if not eid:
            errors.append(f"{aid}: missing eid")
            continue
        if eid in by_eid:
            errors.append(f"{aid}: duplicate eid {eid}")
            continue
        by_eid[eid] = rec
        if eid not in expected_eids:
            errors.append(f"{aid}: unknown eid")
            continue
        if aid != classification[eid]["id"]:
            errors.append(f"{aid}: audit_id does not match frozen EID mapping")

        decision = rec.get("decision")
        roles = rec.get("roles") or []
        evidence = rec.get("evidence") or []
        scope = rec.get("reuse_scope")
        status = rec.get("current_status")
        if decision not in ALLOWED_DECISIONS:
            errors.append(f"{aid}: invalid decision {decision!r}")
        if scope not in ALLOWED_SCOPES:
            errors.append(f"{aid}: invalid reuse_scope {scope!r}")
        if status not in ALLOWED_STATUS:
            errors.append(f"{aid}: invalid current_status {status!r}")
        if any(role in FALLBACKS for role in roles):
            errors.append(f"{aid}: fallback role remains")
        unknown_roles = sorted(set(roles) - vocabulary)
        if unknown_roles:
            errors.append(f"{aid}: roles outside controlled vocabulary: {unknown_roles}")
        if len(roles) > 3:
            errors.append(f"{aid}: more than three roles")
        name = rec.get("corrected_name") or rec.get("current_name") or ""
        if decision == "keep" and ("…" in name or name.rstrip().endswith("...")):
            errors.append(f"{aid}: truncated name remains")
        relevance = rec.get("relevance") or ""
        if decision == "keep" and (not relevance or len(relevance) > 90):
            errors.append(f"{aid}: relevance missing or >90 characters")
        if decision == "keep":
            if status == "historical":
                errors.append(f"{aid}: historical organization kept")
            if scope == "future_design_only":
                errors.append(f"{aid}: future-only project kept")
            if not roles:
                errors.append(f"{aid}: kept without roles")
            if not evidence:
                errors.append(f"{aid}: kept without evidence")
            supported = {role for ev in evidence for role in (ev.get("supports_roles") or [])}
            missing = sorted(set(roles) - supported)
            if missing:
                errors.append(f"{aid}: roles lack evidence: {missing}")
            for ev in evidence:
                if not ev.get("url") or not ev.get("quote") or not ev.get("accessed_at"):
                    errors.append(f"{aid}: incomplete evidence item")
            if status == "project":
                if scope != "actual_reuse" or not rec.get("reuse_objects"):
                    errors.append(f"{aid}: project lacks actual reused objects")
                if roles != [PROJECT_ROLE]:
                    errors.append(f"{aid}: project must have exactly the role {PROJECT_ROLE!r}")
            elif scope not in {"actual_reuse", "direct_enabler"}:
                errors.append(f"{aid}: kept organization lacks qualifying reuse scope")
            elif PROJECT_ROLE in roles:
                errors.append(f"{aid}: organization has project role")
        elif decision == "merge":
            target = rec.get("merge_target_eid")
            if not target or target == eid:
                errors.append(f"{aid}: invalid merge target")
        elif rec.get("merge_target_eid"):
            errors.append(f"{aid}: merge target present for non-merge decision")

    missing = expected_eids - set(by_eid)
    extra = set(by_eid) - expected_eids
    if missing:
        errors.append(f"missing EIDs: {len(missing)}")
    if extra:
        errors.append(f"unknown EIDs: {len(extra)}")
    if len(by_eid) != 859:
        errors.append(f"expected 859 unique decisions, got {len(by_eid)}")

    for eid, rec in by_eid.items():
        if rec.get("decision") != "merge":
            continue
        target = rec.get("merge_target_eid")
        target_rec = by_eid.get(target)
        if not target_rec:
            errors.append(f'{rec.get("audit_id")}: merge target absent')
        elif target_rec.get("decision") != "keep":
            errors.append(f'{rec.get("audit_id")}: merge target is not kept')

    review_complete = all(
        rec.get("review_status") == "cross_review_complete" and rec.get("verified_by")
        for rec in by_eid.values()
    ) if len(by_eid) == 859 else False
    if manifest.get("approved_for_render_prune") and not review_complete:
        errors.append("render approval set before cross-review completion")

    print(f"records={len(by_eid)} errors={len(errors)} cross_review_complete={review_complete}")
    for error in errors[:100]:
        print(f"ERROR: {error}")
    if len(errors) > 100:
        print(f"... {len(errors) - 100} more errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
