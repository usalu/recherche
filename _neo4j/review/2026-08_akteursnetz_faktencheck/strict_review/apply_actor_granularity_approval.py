# -*- coding: utf-8 -*-
"""Apply the user-approved actor-granularity and programme-category decisions."""
from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TODAY = "2026-08-13"
REVIEWER = "root-actor-granularity-approved"


RENAME = {
    "BE:F05": "CirculaTUM – TUM Mission Network Circular Economy",
    "BE:F07": "Construction Management and Engineering / University of Twente",
    "CH:F03": "NEST Research and Innovation Platform / Empa–Eawag",
    "CH:I03": "Amt für Hochbauten und Immobilien Stadt Zürich",
    "DE:F01": "Arbeitsgebiet Bauliches Recycling / BTU Cottbus-Senftenberg",
    "DE:F04": "Forschungsteam Stuttgart 210 / HFT Stuttgart",
    "DE:F05": "Forschungsteam Stuttgart 210 / HTWG Konstanz",
    "DE:F07": "Professur Nachhaltiges Bauen / KIT",
    "DE:F14": "Lehrstuhl TEAMhillebrandt / Bergische Universität Wuppertal",
    "DK:F01": "DTU Byg – Sektion Materialer og Holdbarhed",
    "FI:F01": "Housing Design / Department of Architecture / Aalto University",
    "FI:F02": "KIELO-Projektteam / Xamk",
    "FI:F04": "ReCreate-Koordination / Faculty of Built Environment / Tampere University",
    "FI:I02": "Urban Environment Division / City of Helsinki",
    "NL:F01": "Leiden University",
    "NL:F03": "Circular Built Environment Hub / TU Delft",
    "SE:F01": "ReCreate Sweden / KTH Architecture, Technique and Theory",
    "SE:I02": "Serviceförvaltningen und Miljöförvaltningen / Stockholms stad",
}


PROGRAMMES = {
    "BE:F01",
    "CH:F10",
    "DE:F02",
    "DE:F10",
    "DE:P4",
    "FI:F03",
    "FR:F02",
}


# These kept records became disconnected from the legacy country inference
# after strict pruning.  Their frozen audit IDs provide the reviewed country;
# persist it explicitly so report rendering does not depend on removed peers.
COUNTRY_CORRECTIONS = {
    "BE:S01": "BE",
    "GB:U64": "GB",
    "NL:I03": "NL",
    "NL:U35": "NL",
    "NL:U48": "NL",
    "SE:I01": "SE",
}


MERGES = {
    "CH:F04": "CH:F08",
    "CH:F11": "CH:F12",
}


def append_reason(rec: dict, reason: str) -> None:
    reasons = list(rec.get("reason_codes") or [])
    if reason not in reasons:
        reasons.append(reason)
    rec["reason_codes"] = reasons


def merged_evidence(*groups: list[dict]) -> list[dict]:
    """Combine evidence idempotently when this approval is rerun."""
    result = []
    seen = set()
    for group in groups:
        for evidence in group or []:
            key = (evidence.get("url"), evidence.get("quote"))
            if key not in seen:
                seen.add(key)
                result.append(evidence)
    return result


def consolidate_epfl(target: dict, source: dict) -> None:
    target.update({
        "corrected_name": "Structural Xploration Lab (SXL) / EPFL",
        "roles": ["Technologieentwicklung", "Pilotierung", "Angewandte Forschung"],
        "relevance": "Entwickelt und erprobt zerlegbare Tragwerksysteme für wiederholte Nutzung.",
        "verified_by": REVIEWER,
        "review_status": "cross_review_complete",
    })
    target["evidence"] = merged_evidence(target.get("evidence"), source.get("evidence"))
    append_reason(target, "APPROVED_DUPLICATE_EVIDENCE_CONSOLIDATED")


def consolidate_zhaw(target: dict, source: dict) -> None:
    target.update({
        "corrected_name": "Institut Konstruktives Entwerfen (IKE) / ZHAW",
        "roles": ["Methodenentwicklung", "Angewandte Forschung", "Lehre"],
        "relevance": "Entwickelt, erforscht und lehrt Verfahren zur Wiederverwendung von Bauteilen.",
        "verified_by": REVIEWER,
        "review_status": "cross_review_complete",
    })
    target["evidence"] = merged_evidence(target.get("evidence"), source.get("evidence"))
    append_reason(target, "APPROVED_DUPLICATE_EVIDENCE_CONSOLIDATED")


def main() -> None:
    lanes = {}
    records = []
    for lane in "ABC":
        path = HERE / f"lane_{lane}.json"
        lanes[lane] = json.loads(path.read_text(encoding="utf-8"))
        records.extend(lanes[lane]["records"])
    if len(records) != 859:
        raise SystemExit(f"Expected 859 records, got {len(records)}")
    by_id = {record["audit_id"]: record for record in records}
    if len(by_id) != 859:
        raise SystemExit("Audit IDs are not unique")

    required = (set(RENAME) | PROGRAMMES | set(MERGES) | set(MERGES.values()) |
                set(COUNTRY_CORRECTIONS) | {"NO:F02"})
    missing = sorted(required - set(by_id))
    if missing:
        raise SystemExit(f"Missing approved records: {missing}")

    changes = []
    for aid, corrected_name in RENAME.items():
        rec = by_id[aid]
        old_name = rec.get("corrected_name") or rec["current_name"]
        rec["corrected_name"] = corrected_name
        rec["verified_by"] = REVIEWER
        rec["review_status"] = "cross_review_complete"
        append_reason(rec, "APPROVED_SPECIFIC_ACTOR_GRANULARITY")
        changes.append({"audit_id": aid, "action": "rename", "from": old_name, "to": corrected_name})

    for aid in sorted(PROGRAMMES):
        rec = by_id[aid]
        old_type = rec.get("corrected_type")
        rec["corrected_type"] = "Programm"
        rec["verified_by"] = REVIEWER
        rec["review_status"] = "cross_review_complete"
        append_reason(rec, "APPROVED_PROGRAMME_NOT_ACTOR")
        changes.append({"audit_id": aid, "action": "retype", "from": old_type, "to": "Programm"})

    for aid, country in COUNTRY_CORRECTIONS.items():
        rec = by_id[aid]
        old_country = rec.get("corrected_country")
        rec["corrected_country"] = country
        rec["verified_by"] = REVIEWER
        rec["review_status"] = "cross_review_complete"
        append_reason(rec, "APPROVED_EXPLICIT_REPORT_COUNTRY")
        changes.append({"audit_id": aid, "action": "country", "from": old_country, "to": country})

    for source_id, target_id in MERGES.items():
        source = by_id[source_id]
        target = by_id[target_id]
        source.update({
            "decision": "merge",
            "merge_target_eid": target["eid"],
            "reuse_scope": "none",
            "roles": [],
            "relevance": "",
            "reuse_objects": [],
            "verified_by": REVIEWER,
            "review_status": "cross_review_complete",
        })
        append_reason(source, "APPROVED_GENERIC_PARENT_DUPLICATE_MERGE")
        if source_id == "CH:F04":
            consolidate_epfl(target, source)
        else:
            consolidate_zhaw(target, source)
        changes.append({
            "audit_id": source_id,
            "action": "merge",
            "target_audit_id": target_id,
            "target_eid": target["eid"],
        })

    ntnu = by_id["NO:F02"]
    ntnu.update({
        "decision": "prune",
        "merge_target_eid": None,
        "reuse_scope": "none",
        "roles": [],
        "relevance": "",
        "reuse_objects": [],
        "verified_by": REVIEWER,
        "review_status": "cross_review_complete",
    })
    append_reason(ntnu, "APPROVED_GENERIC_PARTNER_ONLY_PRUNE")
    changes.append({
        "audit_id": "NO:F02",
        "action": "prune",
        "rationale": "Only a project-partner listing; no specific NTNU unit or task is evidenced.",
    })

    for lane, data in lanes.items():
        (HERE / f"lane_{lane}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )

    manifest_path = HERE / "input_manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest["approved_for_render_prune"] = True
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    report = {
        "schema_version": 1,
        "approved": True,
        "approved_at": TODAY,
        "reviewer": REVIEWER,
        "policy": "specific actor unit; programmes excluded from actor category",
        "changes": changes,
    }
    (HERE / "actor_granularity_approval.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Applied {len(changes)} approved actor-granularity decisions")


if __name__ == "__main__":
    main()
