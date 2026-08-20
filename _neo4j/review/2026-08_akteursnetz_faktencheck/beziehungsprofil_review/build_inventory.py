"""Build the review-only inventory for normalized relationship profiles.

This script never writes canonical graph or LaTeX inputs.  In particular,
``beschreibung`` and every former ``dauer*`` field are deliberately excluded
from profile classification inputs.
"""

from __future__ import annotations

import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path

from rapidfuzz.fuzz import ratio, token_set_ratio


HERE = Path(__file__).resolve().parent
FACTCHECK = HERE.parent
EXPANSION = Path(
    r"E:\semio\mit-bestand\bericht\forschungsbericht\anhang\akteursnetz-erweiterung-kandidaten.md"
)

BASE_DURATION = FACTCHECK / "kanten_dauer_final.json"
BASE_CLASSIFICATION = FACTCHECK / "kanten_klassifikation.json"

OUT_JSON = HERE / "relationship_inventory.json"
OUT_CSV = HERE / "relationship_inventory.csv"
OUT_DUPLICATES = HERE / "duplicate_actor_candidates.json"
OUT_SUMMARY = HERE / "INVENTORY_SUMMARY.md"

PROFILE_SINGLE_PROJECT = "Einzelfall / Vorhaben"
PROFILE_PENDING = "needs_profile_review"

# Four retained baseline edges use renamed/shortened endpoints in the Semio
# draft, so exact normalized-name matching cannot recover their canonical IDs.
BASE_EDGE_ALIASES = {
    "base-edge:CH:016": "CH:K044",
    "base-edge:DE:024": "BE:K075",
    "base-edge:BE:002": "BE:K012",
    "base-edge:DK:005": "DK:K019",
}

META_QUOTE_PATTERNS = (
    "url erreichbar",
    "beide urls erreichbar",
    "laut zitat",
    "wird namentlich",
    "verifikation",
    "quelle nennt",
    "im stakeholder-verzeichnis",
    "geführt und laut",
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_expansion() -> dict:
    text = EXPANSION.read_text(encoding="utf-8")
    match = re.search(
        r"<!-- FINAL-DATA:START -->\s*```json\s*(.*?)\s*```\s*<!-- FINAL-DATA:END -->",
        text,
        re.S,
    )
    if not match:
        raise RuntimeError("FINAL-DATA block not found in expansion report")
    return json.loads(match.group(1))


def normalized(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch))
    return re.sub(r"[^a-z0-9]+", "", value.lower())


def fuzzy_name(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "")
    value = "".join(ch for ch in value if not unicodedata.combining(ch)).lower()
    value = re.sub(
        r"\b(gmbh|ag|ab|as|aps|bv|b\.?v\.?|sa|sas|oy|ltd|limited|ev|e\.?v\.?)\b",
        " ",
        value,
    )
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def unordered_pair(country: str, left: str, right: str) -> str:
    return country + ":" + "|".join(sorted((normalized(left), normalized(right))))


def quote_flags(quote: str, project_name: str = "") -> list[str]:
    flags: list[str] = []
    q = (quote or "").strip()
    q_lower = q.lower()
    if not q:
        return ["missing_quote"]
    if len(q) < 25:
        flags.append("quote_too_short")
    if project_name and normalized(q) == normalized(project_name):
        flags.append("quote_is_only_project_name")
    if any(pattern in q_lower for pattern in META_QUOTE_PATTERNS):
        flags.append("quote_contains_review_meta_language")
    if q_lower.endswith((" der", " die", " das", " und", " von", " im")):
        flags.append("quote_looks_truncated")
    return flags


def classify(kind: str) -> tuple[str, str, str]:
    """Classify only from endpoint kind.

    Actor-to-project edges are necessarily evidence about one named project.
    Actor-to-actor edges require source-scope review and are intentionally not
    inferred from their current type, description, or duration.
    """
    if kind == "AKTEUR-BAUVORHABEN":
        return PROFILE_SINGLE_PROJECT, "actor_project_edge", "ready"
    return PROFILE_PENDING, "actor_actor_requires_scope_evidence", "needs_source_scope_review"


def baseline_rows(expansion: dict) -> tuple[list[dict], set[str]]:
    duration = load_json(BASE_DURATION)["relationships"]
    canonical = load_json(BASE_CLASSIFICATION)
    by_pair: dict[str, list[str]] = {}
    for row in duration:
        key = unordered_pair(row["cc"], row["von"], row["nach"])
        by_pair.setdefault(key, []).append(row["id"])

    nodes = {node["key"]: node for node in expansion["nodes"]}
    retained: set[str] = set()
    unresolved: list[str] = []
    for edge in expansion["edges"]:
        if not edge["key"].startswith("base-edge:"):
            continue
        if edge["key"] in BASE_EDGE_ALIASES:
            retained.add(BASE_EDGE_ALIASES[edge["key"]])
            continue
        source = nodes[edge["source"]]
        target = nodes[edge["target"]]
        key = unordered_pair(source["country"], source["name"], target["name"])
        matches = by_pair.get(key, [])
        if len(matches) == 1:
            retained.add(matches[0])
        else:
            unresolved.append(edge["key"])
    if unresolved:
        raise RuntimeError(f"Unresolved baseline expansion edges: {unresolved}")
    if len(retained) != 254:
        raise RuntimeError(f"Expected 254 retained baseline edges, got {len(retained)}")

    rows: list[dict] = []
    for old in duration:
        record = canonical[old["id"]]
        profile, reason, status = classify(record["kind"])
        rows.append(
            {
                "review_id": old["id"],
                "origin": "baseline_264",
                "expansion_state": "retained" if old["id"] in retained else "proposed_removed",
                "country": old["cc"],
                "relationship_kind": record["kind"],
                "source": old["von"],
                "target": old["nach"],
                "relationship_type": old["beziehungsart"],
                "description_for_display_only": old["beschreibung"],
                "profile_proposal": profile,
                "profile_reason_code": reason,
                "profile_review_status": status,
                "evidence_quote": old["evidence_quote"],
                "evidence_url": old["evidence_url"],
                "evidence_flags": quote_flags(old["evidence_quote"]),
            }
        )
    return rows, retained


def new_rows(expansion: dict) -> list[dict]:
    nodes = {node["key"]: node for node in expansion["nodes"]}
    rows: list[dict] = []
    for edge in expansion["edges"]:
        if not edge["key"].startswith("candidate-edge:"):
            continue
        source = nodes[edge["source"]]
        target = nodes[edge["target"]]
        profile, reason, status = classify("AKTEUR-BAUVORHABEN")
        flags = quote_flags(edge.get("evidenceQuote", ""), target["name"])
        if len(edge.get("description", "")) > 60:
            flags.append("description_over_60")
        rows.append(
            {
                "review_id": edge["key"],
                "origin": "expansion_candidate",
                "expansion_state": "proposed_addition",
                "country": source["country"],
                "relationship_kind": "AKTEUR-BAUVORHABEN",
                "source": source["name"],
                "target": target["name"],
                "relationship_type": edge["type"],
                "description_for_display_only": edge.get("description", ""),
                "profile_proposal": profile,
                "profile_reason_code": reason,
                "profile_review_status": status,
                "evidence_quote": edge.get("evidenceQuote", ""),
                "evidence_url": edge.get("evidenceUrl", ""),
                "evidence_flags": flags,
            }
        )
    if len(rows) != 193:
        raise RuntimeError(f"Expected 193 expansion edges, got {len(rows)}")
    return rows


def duplicate_candidates(expansion: dict) -> list[dict]:
    actors = [node for node in expansion["nodes"] if node["kind"] == "actor"]
    candidates = [node for node in actors if node["key"].startswith("candidate:")]
    rows: list[dict] = []
    for index, left in enumerate(actors):
        for right in actors[index + 1 :]:
            if left["country"] != right["country"]:
                continue
            if not (left in candidates or right in candidates):
                continue
            a = fuzzy_name(left["name"])
            b = fuzzy_name(right["name"])
            if not a or not b:
                continue
            score = max(ratio(a, b), token_set_ratio(a, b))
            exact = normalized(left["name"]) == normalized(right["name"])
            if exact or score >= 91:
                rows.append(
                    {
                        "country": left["country"],
                        "left_key": left["key"],
                        "left_name": left["name"],
                        "right_key": right["key"],
                        "right_name": right["name"],
                        "score": round(score, 1),
                        "exact_normalized_match": exact,
                        "status": "needs_identity_review",
                    }
                )
    return sorted(rows, key=lambda row: (-row["score"], row["country"], row["left_name"]))


def write_outputs(rows: list[dict], duplicates: list[dict], retained: set[str]) -> None:
    payload = {
        "review_run": "2026-08-20_beziehungsprofil_review",
        "review_only": True,
        "canonical_outputs_changed": False,
        "classification_inputs": [
            "endpoint_kind",
            "relationship_type_for_manual_routing_only",
            "evidence_quote",
            "evidence_url",
            "source_context",
        ],
        "excluded_classification_inputs": ["beschreibung", "dauer", "dauer_*"],
        "published_profiles_under_review": [
            "Übergreifend / institutionell",
            "Übergreifend / strategisch",
            "Übergreifend / operativ",
            "Einzelfall / Vorhaben",
            "Einzelfall / Leistung",
            "Einzelfall / Ereignis",
        ],
        "relationships": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fieldnames = list(rows[0])
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            printable = dict(row)
            printable["evidence_flags"] = ";".join(row["evidence_flags"])
            writer.writerow(printable)
    OUT_DUPLICATES.write_text(
        json.dumps(duplicates, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    counts = Counter(row["origin"] for row in rows)
    profile_counts = Counter(row["profile_proposal"] for row in rows)
    flagged_new = [
        row for row in rows if row["origin"] == "expansion_candidate" and row["evidence_flags"]
    ]
    actor_actor = [row for row in rows if row["relationship_kind"] == "AKTEUR-AKTEUR"]
    removed = [row for row in rows if row["expansion_state"] == "proposed_removed"]
    summary = f"""# Beziehungsprofil inventory summary

Review-only inventory. No canonical graph or LaTeX output was changed.

## Coverage

- Current visible baseline: **{counts['baseline_264']}** relationships.
- Retained by the uncommitted expansion draft: **{len(retained)}** baseline relationships.
- Proposed baseline removals in that draft: **{len(removed)}** relationships.
- New expansion relationships: **{counts['expansion_candidate']}**.
- Total reviewed inventory: **{len(rows)}** relationship records.

## Initial profile routing

- `{PROFILE_SINGLE_PROJECT}`: **{profile_counts[PROFILE_SINGLE_PROJECT]}** actor-to-project relationships.
- Actor-to-actor scope review still required: **{len(actor_actor)}**.

The routing function does not read the current description or former duration.

## Immediate QA flags

- New relationships with at least one quotation/length flag: **{len(flagged_new)}**.
- Suspected actor identity duplicates: **{len(duplicates)}**.

These are review flags, not deletion or merge decisions.
"""
    OUT_SUMMARY.write_text(summary, encoding="utf-8")


def main() -> None:
    expansion = load_expansion()
    baseline, retained = baseline_rows(expansion)
    additions = new_rows(expansion)
    rows = baseline + additions
    duplicates = duplicate_candidates(expansion)
    write_outputs(rows, duplicates, retained)
    print(
        json.dumps(
            {
                "relationships": len(rows),
                "baseline": len(baseline),
                "retained_baseline": len(retained),
                "new": len(additions),
                "duplicate_flags": len(duplicates),
            },
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
