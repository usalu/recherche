"""Read-only audit of relationship properties on the live graph.

Mirrors the node minimal-property audit, but for relationships. For every
relationship type it reports, per property key: coverage (count + %), distinct
value count, and a few sample values. A heuristic verdict (KEEP / DROP / REVIEW)
is attached so the keep-list matrix can be built and reviewed.

Outputs (under --out-dir):
  rel_property_minimization.csv   one row per (rel_type, property)
  PER_REL_DIGEST.txt              human-readable per-type digest
  rel_property_audit.json         machine-readable full payload

Read-only: issues no writes.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
from collections import defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import repo_root, resolve_connection  # noqa: E402


# Heuristic classification. These mirror the round-2 plan defaults; the real
# decision is the reviewed matrix, this only pre-fills a suggestion column.
DROP_EXACT = {
    "evidence_basis", "evidence_origin", "evidence_excerpt", "evidence_quality",
    "evidence_note", "evidence_cleanup_run", "evidence_confidence_status",
    "previous_evidence_confidence", "evidence_source_id",
    "source_resolution_status", "source_scope", "source_role",
    "derivation_note", "review_status", "review_run", "needs_verification",
    "archive_source_id", "is_bookkeeping",
    "invalid_candidate_source_urls", "invalid_source_url", "invalid_source_url_node_id",
}
DROP_PREFIXES = (
    "source_status", "source_review_status", "source_resolution_status_correction",
    "source_url", "verification_", "strict_", "cleanup_", "invalid_",
)
KEEP_EXACT = {
    "id", "datenqualitaet", "evidence_confidence", "evidence_quote", "evidence_url",
    "original_source_excerpt", "rolle", "role", "pollutant_basis",
    "connection_kind", "association_basis", "reversibility", "property_name",
    "inference_basis", "individual_project_lead_uncertain",
    "not_confirmed_project_participation",
}


def classify(key: str) -> str:
    if key in KEEP_EXACT:
        return "KEEP"
    if key in DROP_EXACT:
        return "DROP"
    if any(key.startswith(p) for p in DROP_PREFIXES):
        return "DROP"
    return "REVIEW"


def short(value: Any, limit: int = 80) -> str:
    s = "" if value is None else str(value)
    s = s.replace("\n", " ").replace("\r", " ")
    return s if len(s) <= limit else s[: limit - 1] + "\u2026"


def run(out_dir: Path) -> dict:
    try:
        from neo4j import GraphDatabase
    except ImportError as exc:
        raise SystemExit("Install: pip install -r requirements-neo4j.txt") from exc

    uri, user, password, database = resolve_connection()
    if not uri or not user or not password:
        raise SystemExit("Missing Neo4j connection settings.")

    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        driver.verify_connectivity()
        with driver.session(database=database) as session:
            type_counts = {
                row["t"]: int(row["c"])
                for row in session.run(
                    "MATCH ()-[r]->() RETURN type(r) AS t, count(r) AS c"
                )
            }
            # Per (type, key): coverage, distinct values, sample values.
            pair_rows = list(
                session.run(
                    "MATCH ()-[r]->() "
                    "UNWIND keys(r) AS k "
                    "WITH type(r) AS t, k, r[k] AS val "
                    "RETURN t AS t, k AS k, count(*) AS cov, "
                    "count(DISTINCT val) AS distinct_vals, "
                    "collect(DISTINCT val)[0..4] AS samples "
                    "ORDER BY t, cov DESC"
                )
            )
            totals = session.run(
                "MATCH ()-[r]->() RETURN count(r) AS rels, sum(size(keys(r))) AS occ"
            ).single()
    finally:
        driver.close()

    by_type: dict[str, list[dict]] = defaultdict(list)
    rows_out: list[dict] = []
    for row in pair_rows:
        t = row["t"]
        k = row["k"]
        cov = int(row["cov"])
        total = type_counts.get(t, 0) or 1
        verdict = classify(k)
        entry = {
            "rel_type": t,
            "property": k,
            "rel_count": type_counts.get(t, 0),
            "coverage": cov,
            "coverage_pct": round(100.0 * cov / total, 1),
            "distinct_values": int(row["distinct_vals"]),
            "samples": " | ".join(short(v) for v in (row["samples"] or [])),
            "suggested_verdict": verdict,
        }
        by_type[t].append(entry)
        rows_out.append(entry)

    out_dir.mkdir(parents=True, exist_ok=True)
    csv_path = out_dir / "rel_property_minimization.csv"
    with csv_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "rel_type", "property", "rel_count", "coverage", "coverage_pct",
                "distinct_values", "suggested_verdict", "samples",
            ],
        )
        w.writeheader()
        for r in rows_out:
            w.writerow(r)

    digest_lines: list[str] = []
    drop_occ = keep_occ = review_occ = 0
    for t in sorted(by_type, key=lambda x: -type_counts.get(x, 0)):
        entries = by_type[t]
        digest_lines.append(
            f"\n=== {t}  ({type_counts.get(t, 0)} rels, "
            f"{len(entries)} distinct prop keys) ==="
        )
        for e in entries:
            if e["suggested_verdict"] == "DROP":
                drop_occ += e["coverage"]
            elif e["suggested_verdict"] == "KEEP":
                keep_occ += e["coverage"]
            else:
                review_occ += e["coverage"]
            digest_lines.append(
                f"  [{e['suggested_verdict']:<6}] {e['property']:<42} "
                f"cov={e['coverage']:>6} ({e['coverage_pct']:>5}%) "
                f"distinct={e['distinct_values']:>5}  e.g. {e['samples']}"
            )
    (out_dir / "PER_REL_DIGEST.txt").write_text(
        "\n".join(digest_lines) + "\n", encoding="utf-8"
    )

    payload = {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "database": database,
        "totals": {
            "relationships": int(totals["rels"]),
            "property_occurrences": int(totals["occ"]),
            "rel_types": len(type_counts),
            "drop_occurrences_suggested": drop_occ,
            "keep_occurrences_suggested": keep_occ,
            "review_occurrences_suggested": review_occ,
        },
        "rows": rows_out,
    }
    (out_dir / "rel_property_audit.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return payload


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out-dir", type=Path, default=None)
    args = ap.parse_args()
    out_dir = args.out_dir or (
        repo_root() / "_neo4j" / "review"
        / "2026-06-01_relationship_property_audit_mit-bestand"
    )
    payload = run(out_dir)
    print(json.dumps(payload["totals"], indent=2))
    print(f"\nWrote audit to: {out_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
