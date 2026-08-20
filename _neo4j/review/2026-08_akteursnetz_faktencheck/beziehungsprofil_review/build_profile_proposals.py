"""Build evidence-scope profile proposals for every inventoried relationship.

Actor-to-project routing is structural. Actor-to-actor decisions below were
reviewed from endpoint identity, relationship type, stored evidence quotation,
and reopened source context. Current descriptions and former duration fields
are not classification inputs.
"""

from __future__ import annotations

import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
INVENTORY = HERE / "relationship_inventory.json"
OUT_JSON = HERE / "profile_proposals.json"
OUT_SUMMARY = HERE / "PROFILE_PROPOSAL_SUMMARY.md"


P_INSTITUTIONAL = "Übergreifend / institutionell"
P_STRATEGIC = "Übergreifend / strategisch"
P_OPERATIONAL = "Übergreifend / operativ"
P_PROJECT = "Einzelfall / Vorhaben"
P_SERVICE = "Einzelfall / Leistung"
P_EVENT = "Einzelfall / Ereignis"


INSTITUTIONAL = {
    "AT:K001", "AT:K009", "AT:K013", "AT:K014",
    "BE:K043", "BE:K086",
    "CH:K001",
    "DE:K034", "DE:K048", "DE:K049",
    "DK:K030", "DK:K031",
    "FI:K040",
    "FR:K010", "FR:K024", "FR:K032", "FR:K041",
    "GB:K026", "GB:K047", "GB:K061", "GB:K063", "GB:K095",
    "NL:K007", "NL:K010",
    "NO:K001", "NO:K011", "NO:K015", "NO:K018", "NO:K019", "NO:K027",
    "SE:K001", "SE:K003", "SE:K011", "SE:K014", "SE:K015", "SE:K019", "SE:K022", "SE:K026",
}

STRATEGIC = {
    "CH:K011", "FI:K031", "FI:K032",
    "FR:K006", "FR:K008", "SE:K005", "SE:K029",
}

OPERATIONAL = {"CH:K004", "CH:K006", "DK:K010", "DK:K024", "GB:K046"}

SINGLE_SERVICE = {
    "AT:K002", "CH:K003", "CH:K046", "FI:K039",
    "FR:K031", "FR:K034", "GB:K051", "GB:K075",
}

SINGLE_EVENT = {"CH:K041", "NL:K069"}

SINGLE_PROJECT = {
    # One cooperation, commission, pilot, or named programme.
    "AT:K003",
    "BE:K046", "BE:K072", "BE:K073", "BE:K075",
    "CH:K002", "CH:K012", "CH:K040", "CH:K042", "CH:K044",
    "DE:K031", "DE:K033", "DE:K035", "DE:K036",
    "FI:K007", "FI:K009", "FI:K011", "FI:K013", "FI:K016", "FI:K017",
    "FI:K024", "FI:K029", "FI:K030", "FI:K036", "FI:K038",
    "FR:K033", "FR:K035", "FR:K038", "FR:K039", "FR:K044",
    "GB:K062", "GB:K072",
    "NO:K012", "NO:K013", "NO:K021",
    "SE:K002", "SE:K006", "SE:K007", "SE:K016", "SE:K017", "SE:K018",
    "SE:K023", "SE:K024", "SE:K025", "SE:K027", "SE:K028",
    "SE:K030", "SE:K033",
}

# Reopened sources now support the scope profile for all 108 actor-actor
# relationships. Some rows still need a relationship-type correction; those
# are tracked in RESEARCH_REVIEW_REPORT.md and are not profile uncertainty.
WARNINGS = {}


def actor_actor_profiles() -> dict[str, str]:
    groups = {
        P_INSTITUTIONAL: INSTITUTIONAL,
        P_STRATEGIC: STRATEGIC,
        P_OPERATIONAL: OPERATIONAL,
        P_PROJECT: SINGLE_PROJECT,
        P_SERVICE: SINGLE_SERVICE,
        P_EVENT: SINGLE_EVENT,
    }
    result: dict[str, str] = {}
    for profile, identifiers in groups.items():
        for identifier in identifiers:
            if identifier in result:
                raise RuntimeError(f"duplicate profile decision for {identifier}")
            result[identifier] = profile
    return result


def main() -> None:
    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    profiles = actor_actor_profiles()
    actor_actor_ids = {
        row["review_id"]
        for row in inventory["relationships"]
        if row["relationship_kind"] == "AKTEUR-AKTEUR"
    }
    missing = sorted(actor_actor_ids - profiles.keys())
    extra = sorted(profiles.keys() - actor_actor_ids)
    if missing or extra:
        raise RuntimeError(f"actor-actor coverage failure; missing={missing}; extra={extra}")

    proposals = []
    for row in inventory["relationships"]:
        if row["relationship_kind"] == "AKTEUR-BAUVORHABEN":
            profile = P_PROJECT
            reason = "one named project endpoint"
        else:
            profile = profiles[row["review_id"]]
            reason = "actor-actor source-scope review"
        warning = WARNINGS.get(row["review_id"], "")
        proposals.append(
            {
                "review_id": row["review_id"],
                "origin": row["origin"],
                "expansion_state": row["expansion_state"],
                "source": row["source"],
                "target": row["target"],
                "relationship_type": row["relationship_type"],
                "profile_proposal": profile,
                "reason": reason,
                "review_status": "needs_source_scope_review" if warning else "profile_ready",
                "warning": warning,
                "evidence_url": row["evidence_url"],
            }
        )

    payload = {
        "review_run": "2026-08-20_beziehungsprofil_proposals",
        "review_only": True,
        "approved_for_apply": False,
        "canonical_outputs_changed": False,
        "classification_excludes": ["beschreibung", "dauer", "dauer_*"],
        "relationships": proposals,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    counts_all = Counter(row["profile_proposal"] for row in proposals)
    target = [row for row in proposals if row["expansion_state"] != "proposed_removed"]
    counts_target = Counter(row["profile_proposal"] for row in target)
    lines = [
        "# Beziehungsprofil proposal summary",
        "",
        "Review only; not approved for application.",
        "",
        "| Profile | All 457 reviewed | Proposed 447-edge expansion |",
        "|---|---:|---:|",
    ]
    for profile in (P_INSTITUTIONAL, P_STRATEGIC, P_OPERATIONAL, P_PROJECT, P_SERVICE, P_EVENT):
        lines.append(f"| {profile} | {counts_all[profile]} | {counts_target[profile]} |")
    lines.extend(
        [
            "",
            f"Relationships with unresolved scope/evidence warnings: **{len(WARNINGS)}**.",
            "",
            "The candidate expansion still requires evidence repair and identity review before these counts can become final.",
        ]
    )
    OUT_SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"proposals": len(proposals), "warnings": len(WARNINGS)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
