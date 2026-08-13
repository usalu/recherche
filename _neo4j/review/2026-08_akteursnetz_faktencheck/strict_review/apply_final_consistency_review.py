# -*- coding: utf-8 -*-
"""Apply the final user-requested consistency review before approval."""
from __future__ import annotations

import json
from pathlib import Path


HERE = Path(__file__).resolve().parent
TODAY = "2026-08-13"

PRUNE = {
    "AT:U01": "Membership statement does not prove technical planning or certification.",
    "CH:U16": "Building-services project credit does not prove a reuse-specific task.",
    "CH:U24": "Construction-management credit does not prove a reuse-specific task.",
    "DE:U19": "Structural-engineering credit does not prove a reuse-specific task.",
    "DE:U33": "Execution-planning credit does not prove reuse planning or coordination.",
    "DE:F11": "Circular collaboration statement does not prove a concrete reuse task.",
    "FI:I01": "Partner list does not prove the city's assigned ownership/inventory roles.",
    "FI:I03": "Collaboration listing does not prove the city's assigned reuse roles.",
    "FI:F04": "Project description does not identify Tampere University's concrete task.",
    "FI:F05": "General resource-bank statement does not prove VTT's assigned roles.",
    "DK:U11": "General circular-economy statement does not prove method development.",
}


def keep_umar(rec):
    rec.update({
        "decision": "keep",
        "merge_target_eid": None,
        "reason_codes": ["final_consistency_actual_reuse_evidence_recovered"],
        "current_status": "project",
        "reuse_scope": "actual_reuse",
        "roles": ["Referenzprojekt"],
        "relevance": "Verbaut umgenutzte Dämmstoffe in einem trennbaren Forschungsmodul.",
        "reuse_objects": ["umgenutzte Dämmstoffe"],
        "evidence": [{
            "url": "https://nest-umar.net/portfolio/umar/",
            "quote": "Among the technologies used here are ... repurposed insulation materials.",
            "supports_roles": ["Referenzprojekt"],
            "accessed_at": TODAY,
        }],
        "verified_by": "root-final",
        "review_status": "cross_review_complete",
    })


def keep_asam(rec):
    rec.update({
        "decision": "keep",
        "merge_target_eid": None,
        "reason_codes": ["final_consistency_actor_specific_evidence_recovered"],
        "current_status": "active",
        "reuse_scope": "direct_enabler",
        "roles": ["Projektentwicklung", "Pilotierung"],
        "relevance": "Leitete Reuse-Piloten und erprobte den Wiedereinsatz rückgebauter Betonplatten.",
        "reuse_objects": [],
        "evidence": [
            {
                "url": "https://www.baulinks.de/webplugin/2005/1177.php4",
                "quote": "Claus Asam vom IEMB, der das Projekt leitete und maßgeblich mitinitiierte.",
                "supports_roles": ["Projektentwicklung"],
                "accessed_at": TODAY,
            },
            {
                "url": "https://taz.de/Die-Wiedergeburt-der-Platte/!493469/",
                "quote": "Gemeinsam mit Claus Asam vom IEMB ... drei Testbauten errichtet.",
                "supports_roles": ["Pilotierung"],
                "accessed_at": TODAY,
            },
        ],
        "verified_by": "root-final",
        "review_status": "cross_review_complete",
    })


def strengthen_tu_chair(rec):
    rec.update({
        "reason_codes": ["final_consistency_specific_chair_evidence"],
        "roles": ["Angewandte Forschung", "Lehre"],
        "relevance": "Entwickelte das Reuse-Gebäude mit und band Studierende in Lehrbaustellen ein.",
        "evidence": [{
            "url": "https://www.tu.berlin/en/bauphysik/research/past-projects/projekt-plattenvereinigung",
            "quote": (
                "The building was developed in partnership with the Chair of Building Physics and "
                "Building Constructions at TU Berlin. Trainees and students were also included in "
                "the process to help design experimental teaching sites within the construction."
            ),
            "supports_roles": ["Angewandte Forschung", "Lehre"],
            "accessed_at": TODAY,
        }],
        "verified_by": "root-final",
        "review_status": "cross_review_complete",
    })


def main():
    lanes = {}
    records = []
    for lane in "ABC":
        path = HERE / f"lane_{lane}.json"
        lanes[lane] = json.loads(path.read_text(encoding="utf-8"))
        records.extend(lanes[lane]["records"])
    if len(records) != 859:
        raise SystemExit("Expected 859 records")
    by_id = {r["audit_id"]: r for r in records}
    if len(by_id) != 859:
        raise SystemExit("Audit IDs are not unique")

    snapshot = HERE / "cross_review_complete_snapshot.json"
    if not snapshot.exists():
        snapshot.write_text(json.dumps(lanes, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    changes = []
    for aid, rationale in PRUNE.items():
        rec = by_id[aid]
        before = rec["decision"]
        rec.update({
            "decision": "prune",
            "merge_target_eid": None,
            "reason_codes": ["final_consistency_generic_or_credit_only"],
            "reuse_scope": "none",
            "roles": [],
            "relevance": "",
            "reuse_objects": [],
            "evidence": [],
            "verified_by": "root-final",
            "review_status": "cross_review_complete",
        })
        changes.append({"audit_id": aid, "from": before, "to": "prune", "rationale": rationale})

    keep_umar(by_id["CH:P10"])
    changes.append({"audit_id": "CH:P10", "from": "prune", "to": "keep", "rationale": "Official UMAR page names repurposed insulation materials."})
    keep_asam(by_id["DE:F03"])
    changes.append({"audit_id": "DE:F03", "from": "prune", "to": "keep", "rationale": "Sources name Asam as initiator/leader and document three test buildings."})
    strengthen_tu_chair(by_id["DE:F13"])
    changes.append({"audit_id": "DE:F13", "from": "keep", "to": "keep", "rationale": "Specific chair and student teaching sites are explicitly named."})

    for lane, data in lanes.items():
        (HERE / f"lane_{lane}.json").write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
        )
    report = {
        "schema_version": 1,
        "reviewer": "root-final",
        "policy": "specific actor + concrete reuse activity + role-specific evidence",
        "changes": changes,
    }
    (HERE / "final_consistency_review.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"Applied {len(changes)} final consistency decisions")


if __name__ == "__main__":
    main()
