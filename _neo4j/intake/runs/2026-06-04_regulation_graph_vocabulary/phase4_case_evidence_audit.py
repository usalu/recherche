"""Phase 4 pre-audit: find case-documented pollutant evidence candidates.

This is read-only. It searches live Projekt/Bauwerk/Bauteilgruppe properties for
explicit pollutant keywords and writes a coverage report. The result determines
which Phase 4 edges can honestly be marked `case_documented`; all others need
taxonomy/era/material-derived treatment or an explicit keep/drop decision.

Usage:
  python phase4_case_evidence_audit.py
"""

from __future__ import annotations

import json
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from neo4j import GraphDatabase

REPO = Path(__file__).resolve().parents[4]
if str(REPO / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent

KEYWORDS = {
    "s_asbest": [r"\basbest\b", r"asbestos"],
    "s_kmf": [r"\bkmf\b", r"künstliche mineralfas", r"kuenstliche mineralfas", r"mineralwolle", r"glass wool", r"glaswolle", r"steinwolle"],
    "s_pcb": [r"\bpcb\b"],
    "s_pak": [r"\bpak\b", r"\bteer\b", r"teerpech", r"schwarzkleber"],
    "s_holzschutzmittel": [r"holzschutzmittel", r"\bpcp\b", r"lindan"],
    "s_bleifarbe": [r"bleifarbe", r"lead paint"],
    "s_formaldehyd": [r"formaldehyd", r"formaldehyde"],
    "s_schwermetalle": [r"schwermetall", r"heavy metal"],
    "s_radon": [r"radon"],
    "s_schimmel": [r"schimmel", r"mould", r"mold"],
    "s_chlorid": [r"chlorid", r"chloride"],
    "s_salze": [r"\bsalze\b", r"\bsalt\b"],
    "s_mineraloel": [r"mineralöl", r"mineraloel", r"mineral oil"],
}

LABELS = ["Projekt", "Bauwerk", "Bauteilgruppe"]
TEXT_PROPS_TO_IGNORE = {
    "id",
    "source_urls",
    "source_titles",
    "legacy_internal_provenance_docs",
    "legacy_rechtsgrundlagen",
    "legacy_rechtsgrundlagen_urls",
}


def text_values(props: dict[str, Any]) -> list[tuple[str, str]]:
    values: list[tuple[str, str]] = []
    for key, value in props.items():
        if key in TEXT_PROPS_TO_IGNORE:
            continue
        if isinstance(value, str):
            values.append((key, value))
        elif isinstance(value, list):
            text = " | ".join(str(v) for v in value if v is not None)
            if text:
                values.append((key, text))
    return values


def snippet(text: str, pattern: str) -> str:
    match = re.search(pattern, text, flags=re.IGNORECASE)
    if not match:
        return text[:220]
    start = max(0, match.start() - 90)
    end = min(len(text), match.end() + 120)
    return text[start:end].strip()


def pollutant_hits(props: dict[str, Any]) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for key, value in text_values(props):
        for pollutant_id, patterns in KEYWORDS.items():
            for pattern in patterns:
                if re.search(pattern, value, flags=re.IGNORECASE):
                    hits.append(
                        {
                            "pollutant_id": pollutant_id,
                            "property": key,
                            "matched_pattern": pattern,
                            "snippet": snippet(value, pattern),
                        }
                    )
                    break
    return hits


def run() -> dict[str, Any]:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    candidates: list[dict[str, Any]] = []
    with driver.session(database=database) as session:
        rows = session.run(
            """
            MATCH (n)
            WHERE any(label IN labels(n) WHERE label IN $labels)
            RETURN n.id AS id, labels(n) AS labels, properties(n) AS props
            ORDER BY n.id
            """,
            labels=LABELS,
        )
        for row in rows:
            hits = pollutant_hits(row["props"])
            if not hits:
                continue
            candidates.append(
                {
                    "node_id": row["id"],
                    "labels": row["labels"],
                    "name": row["props"].get("name"),
                    "source_urls": row["props"].get("source_urls", []),
                    "legacy_internal_provenance_docs": row["props"].get("legacy_internal_provenance_docs", []),
                    "hits": hits,
                }
            )
        rel_counts = {
            reltype: session.run(f"MATCH ()-[r:`{reltype}`]->() RETURN count(r) AS c").single()["c"]
            for reltype in [
                "HAS_RISK_POLLUTANT",
                "REQUIRES_VERIFICATION_FOR",
                "TYPISCH_BEI_ERA",
                "TYPISCH_BEI_MATERIAL",
                "TYPISCH_BEI_BAUTEILTYP",
            ]
        }
    driver.close()

    by_pollutant = Counter()
    by_label = Counter()
    nodes_by_pollutant: dict[str, set[str]] = defaultdict(set)
    for candidate in candidates:
        for label in candidate["labels"]:
            if label in LABELS:
                by_label[label] += 1
                break
        for hit in candidate["hits"]:
            by_pollutant[hit["pollutant_id"]] += 1
            nodes_by_pollutant[hit["pollutant_id"]].add(candidate["node_id"])

    report = {
        "phase": "phase4_case_evidence_audit",
        "database": database,
        "created_at_utc": datetime.now(timezone.utc).isoformat(),
        "rel_counts": rel_counts,
        "candidate_nodes": len(candidates),
        "candidate_hits": sum(len(c["hits"]) for c in candidates),
        "candidate_nodes_by_label": dict(by_label),
        "candidate_hits_by_pollutant": dict(by_pollutant),
        "candidate_nodes_by_pollutant": {k: len(v) for k, v in sorted(nodes_by_pollutant.items())},
        "candidates": candidates,
    }
    (OUT / "phase4_case_evidence_audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str) + "\n",
        encoding="utf-8",
    )
    return report


def main() -> int:
    report = run()
    print(json.dumps({k: v for k, v in report.items() if k != "candidates"}, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
