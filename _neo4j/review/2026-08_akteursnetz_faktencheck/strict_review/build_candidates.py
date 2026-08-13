# -*- coding: utf-8 -*-
"""Build the immutable input manifest and the strict-review candidate register.

This script never changes the original classification or fact-check artifacts.
It only writes generated files below strict_review/.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


BASE = Path(__file__).resolve().parent.parent
OUT = BASE / "strict_review"

FALLBACKS = {
    "Keine direkte Reuse-Rolle belegt",
    "Reuse-Bezug belegt, Rolle unklar",
    "Unzureichende Informationen",
    "Referenzprojekt, Reuse-Umfang unklar",
}

FINAL_SEARCH = set("""
AT:U02 AT:U10 AT:U12 BE:F06 BE:U19 BE:U28 BE:U35 CH:I02 DE:F11
DK:U01 FI:U20 FR:M22 FR:M24 FR:N06 FR:U19 GB:F04 GB:M04 GB:N02
GB:U01 GB:U04 GB:U18 GB:U49 GB:U59 GB:U64 NL:I05 NL:U16 NL:U24
NL:U31 SE:F01 SE:U19
""".split())

IDENTITY_TYPE = set("""
AT:U03 BE:P12 DE:P1 DE:P4 DE:P5 DE:P9 DE:P18 DK:M07 FI:P1 FR:O03 SE:I01
""".split())

FUTURE_ONLY = {"DK:P1", "FI:P2", "GB:P6"}
HISTORICAL_ORGS = {"DE:U05", "DE:U08", "DE:U09", "DE:U11", "DK:M12"}
TRUNCATED_NAMES = set("""
BE:P6 BE:P10 CH:P2 CH:P4 CH:P7 DE:P2 FI:P5 FI:P6 FR:P3 GB:P8 GB:P11
NL:P3 NL:P6 NL:P11 NL:P16
""".split())
COUNTRY_DRIFT = {"DE:N03", "DE:N04", "DE:U24", "DE:I03", "DE:U39", "DE:I06", "DE:F11"}
RETYPE = {"FR:P6"}
FORCE_PRUNE = FUTURE_ONLY | HISTORICAL_ORGS | {"DE:O01"}
MERGE_SOURCE = {"DK:P3": "DK:P2", "NL:P5": "NL:P4"}
COLLISION_RENAME = {"DE:P10"}


def load(name: str):
    return json.loads((BASE / name).read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def input_files() -> list[Path]:
    paths = [
        BASE / "KLASSIFIKATION_TAXONOMIE.md",
        BASE / "batches" / "_index.json",
        BASE / "verdicts.json",
        BASE / "klassifikation.json",
        BASE / "prune_faktencheck_final.json",
    ]
    paths.extend(sorted((BASE / "results").glob("klass_*.md")))
    return paths


def main() -> None:
    OUT.mkdir(exist_ok=True)
    classification = load("klassifikation.json")
    by_id = {row["id"]: (eid, row) for eid, row in classification.items()}
    if len(classification) != 859 or len(by_id) != 859:
        raise SystemExit("Expected 859 unique classification records")

    all_special = (
        FINAL_SEARCH | IDENTITY_TYPE | FUTURE_ONLY | HISTORICAL_ORGS |
        TRUNCATED_NAMES | COUNTRY_DRIFT | RETYPE | set(MERGE_SOURCE) |
        set(MERGE_SOURCE.values()) | COLLISION_RENAME | {"DE:O01"}
    )
    missing_special = sorted(all_special - set(by_id))
    if missing_special:
        raise SystemExit(f"Unknown planned audit IDs: {missing_special}")

    candidates = []
    weak_count = 0
    known_count = 0
    for eid, row in sorted(classification.items(), key=lambda item: item[1]["id"]):
        audit_id = row["id"]
        roles = row.get("rollen") or [x.strip() for x in row["rolle"].split("/")]
        flags = []
        weak = any(r in FALLBACKS for r in roles)
        if weak:
            flags.append("weak_classification")
            weak_count += 1
        if audit_id in FINAL_SEARCH:
            flags.append("final_source_search")
        if audit_id in IDENTITY_TYPE:
            flags.append("identity_or_type_review")
        if audit_id in FUTURE_ONLY:
            flags.append("future_design_only")
        if audit_id in HISTORICAL_ORGS:
            flags.append("historical_or_closed_org")
        if audit_id in TRUNCATED_NAMES:
            flags.append("truncated_name")
        if audit_id in COUNTRY_DRIFT:
            flags.append("country_drift")
        if audit_id in RETYPE:
            flags.append("retype_required")
        if audit_id in MERGE_SOURCE:
            flags.append("duplicate_merge_source")
        if audit_id in MERGE_SOURCE.values():
            flags.append("duplicate_canonical_target")
        if audit_id in COLLISION_RENAME:
            flags.append("name_collision")
        if audit_id == "DE:O01":
            flags.append("known_prune")

        if flags:
            known_count += 1
        if audit_id in MERGE_SOURCE:
            recommendation = "merge"
        elif audit_id in FORCE_PRUNE or (weak and audit_id not in FINAL_SEARCH | IDENTITY_TYPE):
            recommendation = "prune"
        else:
            recommendation = "review"

        candidates.append({
            "eid": eid,
            "audit_id": audit_id,
            "name": row["name"],
            "cc": row["cc"],
            "current_roles": roles,
            "current_relevance": row["relevanz"],
            "primary_url": row["beleg_url"],
            "flags": flags,
            "initial_recommendation": recommendation,
            "merge_target_audit_id": MERGE_SOURCE.get(audit_id),
        })

    if weak_count != 99:
        raise SystemExit(f"Expected 99 weak classifications, found {weak_count}")
    if known_count != 131:
        raise SystemExit(f"Expected 131 unique known review candidates, found {known_count}")

    manifest = {
        "schema_version": 1,
        "expected_records": 859,
        "known_review_candidates": known_count,
        "weak_classifications": weak_count,
        "approved_for_render_prune": False,
        "inputs": {
            str(p.relative_to(BASE)).replace("\\", "/"): sha256(p)
            for p in input_files()
        },
    }
    (OUT / "input_manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    (OUT / "strict_review_candidates.json").write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    rows = [
        "# Strict-Review-Kandidaten",
        "",
        "Noch nicht für Rendering freigegeben.",
        "",
        "| ID | Name | Flags | Empfehlung |",
        "|---|---|---|---|",
    ]
    for c in candidates:
        if not c["flags"]:
            continue
        rows.append(
            f'| {c["audit_id"]} | {c["name"].replace("|", "\\|")} | '
            f'{", ".join(c["flags"])} | {c["initial_recommendation"]} |'
        )
    (OUT / "STRICT_REVIEW.md").write_text("\n".join(rows) + "\n", encoding="utf-8")
    print(f"Wrote 859 records; {known_count} known candidates; approval=false")


if __name__ == "__main__":
    main()
