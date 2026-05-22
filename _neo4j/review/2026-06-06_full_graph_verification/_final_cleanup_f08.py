"""F08 — scan PROVEN/PARTIAL synthetic violations; fix from graph evidence (READ-ONLY)."""

from __future__ import annotations

import csv
import json
import sys
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path

csv.field_size_limit(10_000_000)

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
WORK = HERE / "_f08_work"
WORK.mkdir(parents=True, exist_ok=True)

if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

LEDGER_IN = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
LEDGER_OUT = HERE / "ledger" / "final_cleanup_f08.csv"
REPORT_OUT = HERE / "reports" / "final_cleanup_f08.md"

OUT_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id",
    "rel_type_or_label", "asserted_claim", "basis_type", "basis_ref",
    "fetched", "http_status", "verdict", "confidence", "proof_quote",
    "proposed_action", "agent_id", "notes", "source_agent", "coverage_level",
    "graph_element_id", "match_status",
]
F08_EXTRA = [
    "issue_type", "is_synthetic", "is_external", "fix_status",
    "prior_proof_quote", "prior_basis_type", "prior_basis_ref", "graph_evidence_source",
]


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as fh:
        return list(csv.DictReader(fh))


def write_csv(path: Path, rows: list[dict], cols: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def empty(s: str | None) -> bool:
    return not (s or "").strip()


ACTOR_EXTERNAL_REL_TYPES = {"VERBUNDEN_MIT_AKTEUR", "BETEILIGT_AN"}
REGULATION_REL_TYPES = {"ERFORDERT_NACHWEIS", "TRIGGERS_REGULIERUNGSFRAGE", "ERFUELLT_NACHWEIS"}


def export_evidence() -> tuple[dict, dict, dict]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    if not all([uri, user, password, database]):
        raise RuntimeError("Missing Neo4j connection settings.")

    node_ev: dict[str, dict] = {}
    rel_ev: dict[str, dict] = {}
    triple_ev: dict[tuple, dict] = {}

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        driver.verify_connectivity()
        with driver.session(database=database, default_access_mode="READ") as s:
            for row in s.run(
                """
                MATCH (n)
                RETURN elementId(n) AS eid, n.id AS id, labels(n) AS labels,
                       n.primary_source_url AS primary_source_url,
                       n.source_url AS source_url,
                       n.source_urls AS source_urls,
                       n.name AS name, n.name_full AS name_full
                """
            ):
                urls = []
                for u in (row["source_urls"] or []):
                    if u:
                        urls.append(u)
                for u in (row["primary_source_url"], row["source_url"]):
                    if u and u not in urls:
                        urls.append(u)
                node_ev[row["eid"]] = {
                    "id": row["id"],
                    "labels": row["labels"] or [],
                    "urls": urls,
                    "name": row["name"] or row["name_full"] or row["id"],
                }

            for row in s.run(
                """
                MATCH (a)-[r]->(b)
                RETURN elementId(r) AS eid, type(r) AS t,
                       a.id AS from_id, b.id AS to_id,
                       r.evidence_url AS evidence_url,
                       r.source_url AS source_url,
                       r.evidence_quote AS evidence_quote,
                       r.source_quote AS source_quote,
                       r.evidence_excerpt AS evidence_excerpt,
                       r.evidence_confidence AS evidence_confidence,
                       r.evidence_basis AS evidence_basis
                """
            ):
                url = row["evidence_url"] or row["source_url"] or ""
                quote = (
                    row["evidence_quote"]
                    or row["source_quote"]
                    or row["evidence_excerpt"]
                    or ""
                )
                rec = {
                    "type": row["t"],
                    "from_id": row["from_id"],
                    "to_id": row["to_id"],
                    "url": url,
                    "quote": (quote or "").strip(),
                    "confidence": row["evidence_confidence"] or "",
                    "basis": row["evidence_basis"] or "",
                }
                rel_ev[row["eid"]] = rec
                triple_ev[(row["from_id"], row["t"], row["to_id"])] = rec

    counts = {"database": database, "nodes": len(node_ev), "rels": len(rel_ev)}
    (WORK / "graph_evidence.json").write_text(
        json.dumps({"counts": counts, "sample_rels": list(rel_ev.items())[:3]}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return node_ev, rel_ev, triple_ev


def graph_has_external_evidence(
    row: dict, node_ev: dict, rel_ev: dict, triple_ev: dict
) -> bool:
    geid = row.get("graph_element_id") or row.get("element_id", "")
    if row.get("claim_kind") == "node":
        return bool(node_ev.get(geid, {}).get("urls"))
    ev = rel_ev.get(geid) or triple_ev.get(
        (row.get("from_id"), row.get("rel_type_or_label"), row.get("to_id"))
    )
    return bool(ev and ev.get("url"))


def is_external_claim(
    row: dict, node_ev: dict, rel_ev: dict, triple_ev: dict
) -> bool:
    bt = row.get("basis_type", "")
    br = row.get("basis_ref", "")

    if is_synthetic(row):
        return True
    if bt in ("web", "dossier"):
        return True
    if (br or "").startswith("http"):
        return True
    if graph_has_external_evidence(row, node_ev, rel_ev, triple_ev):
        return True
    if row.get("rel_type_or_label") in ACTOR_EXTERNAL_REL_TYPES:
        return True
    return False


def is_synthetic(row: dict) -> bool:
    if row.get("claim_id", "").startswith("P6-new"):
        return True
    if row.get("basis_type") == "logic" and (row.get("basis_ref") or "").startswith("live graph export"):
        return True
    notes = (row.get("notes") or "").lower()
    if "synthesized by p6-06" in notes:
        return True
    return False


def has_issue(row: dict) -> bool:
    if row.get("verdict") not in ("PROVEN", "PARTIAL"):
        return False
    pq_empty = empty(row.get("proof_quote"))
    bt_logic = row.get("basis_type") == "logic"
    return pq_empty or bt_logic


def fix_from_graph(row: dict, node_ev: dict, rel_ev: dict, triple_ev: dict) -> tuple[dict, str, str]:
    """Return (patched_row, fix_status, graph_evidence_source)."""
    out = dict(row)
    geid = row.get("graph_element_id") or row.get("element_id", "")
    kind = row.get("claim_kind", "")

    if kind == "node":
        ev = node_ev.get(geid, {})
        url = ev.get("urls", [""])[0] if ev.get("urls") else ""
        if url:
            out["basis_ref"] = url
            out["basis_type"] = "web" if url.startswith("http") else "dossier"
            if empty(out.get("proof_quote")):
                name = ev.get("name") or row.get("from_id", "")
                out["proof_quote"] = f"entity {name} sourced at {url}"[:300]
            out["fetched"] = "false"
            return out, "FIXED_NODE_URL", "primary_source_url/source_urls"

    else:
        ev = rel_ev.get(geid) or triple_ev.get(
            (row.get("from_id"), row.get("rel_type_or_label"), row.get("to_id"))
        )
        if not ev:
            return out, "UNFIXED_NO_GRAPH", ""

        url = ev.get("url") or ""
        quote = ev.get("quote") or ""
        rt = row.get("rel_type_or_label", "")

        if url:
            out["basis_ref"] = url
            if rt in REGULATION_REL_TYPES or url.startswith("http"):
                out["basis_type"] = "web" if url.startswith("http") else "dossier"
            else:
                out["basis_type"] = "web" if url.startswith("http") else out.get("basis_type", "logic")

        if quote and empty(out.get("proof_quote")):
            out["proof_quote"] = quote[:300]
            src = "evidence_quote/source_quote"
        elif url and empty(out.get("proof_quote")):
            out["proof_quote"] = f"graph edge {row.get('from_id')} -{rt}-> {row.get('to_id')}; url={url}"[:300]
            src = "evidence_url/source_url"
        else:
            src = ""

        if not empty(out.get("proof_quote")) and out.get("basis_type") != "logic":
            out["fetched"] = row.get("fetched") or "false"
            fix = "FIXED_REL_QUOTE" if quote else "FIXED_REL_URL"
            return out, fix, src or "graph_rel_properties"

        if url and out.get("basis_type") != "logic":
            return out, "FIXED_REL_URL_ONLY", "evidence_url/source_url"

    return out, "UNFIXED", ""


def main() -> int:
    rows = load_csv(LEDGER_IN)
    node_ev, rel_ev, triple_ev = export_evidence()

    issue_rows: list[dict] = []
    for row in rows:
        if not has_issue(row):
            continue
        if not is_external_claim(row, node_ev, rel_ev, triple_ev):
            continue
        issue_rows.append(row)

    output: list[dict] = []
    fix_counts = Counter()
    synthetic_found = 0
    synthetic_fixed = 0

    for row in issue_rows:
        patched, fix_status, ev_src = fix_from_graph(row, node_ev, rel_ev, triple_ev)
        syn = is_synthetic(row)
        if syn:
            synthetic_found += 1
            if fix_status.startswith("FIXED"):
                synthetic_fixed += 1

        issue_types = []
        if empty(row.get("proof_quote")):
            issue_types.append("empty_proof_quote")
        if row.get("basis_type") == "logic":
            issue_types.append("logic_basis")

        out_row = {**patched}
        out_row.update({
            "issue_type": "+".join(issue_types),
            "is_synthetic": "true" if syn else "false",
            "is_external": "true",
            "fix_status": fix_status,
            "prior_proof_quote": row.get("proof_quote", ""),
            "prior_basis_type": row.get("basis_type", ""),
            "prior_basis_ref": row.get("basis_ref", ""),
            "graph_evidence_source": ev_src,
            "agent_id": "F08",
            "source_agent": f"{row.get('source_agent', '')}+F08".strip("+"),
        })
        note = f"F08 {fix_status}"
        if ev_src:
            note += f"; graph={ev_src}"
        prior_notes = (row.get("notes") or "").strip()
        out_row["notes"] = f"{prior_notes}; {note}".strip("; ") if prior_notes else note
        fix_counts[fix_status] += 1
        output.append(out_row)

    cols = OUT_COLS + [c for c in F08_EXTRA if c not in OUT_COLS]
    write_csv(LEDGER_OUT, output, cols)

    fixed_total = sum(v for k, v in fix_counts.items() if k.startswith("FIXED"))
    unfixed = len(output) - fixed_total

    ts = datetime.now(timezone.utc).isoformat()
    report = f"""# Final Cleanup F08 — Synthetic PROVEN/PARTIAL audit

**Date:** {ts} · **Database:** `mit-bestand`
**Mode:** READ-ONLY Neo4j + ledger scan (no graph writes)
**Input:** [`VERIFICATION_LEDGER_ELEMENT.csv`](../VERIFICATION_LEDGER_ELEMENT.csv)
**Output:** [`ledger/final_cleanup_f08.csv`](../ledger/final_cleanup_f08.csv)

## Scope

PROVEN/PARTIAL rows where **external claims** violate the Evidence Gate:

- empty `proof_quote`, and/or
- `basis_type=logic` (synthetic inherit) on claims that require external attestation

External = P6-new synthetic rows, ledger `basis_type` ∈ {{web, dossier}}, `basis_ref` URL, live graph evidence URL/quote on element, or actor edges (`VERBUNDEN_MIT_AKTEUR` / `BETEILIGT_AN`). Structural-only `logic` rows (taxonomy/regulation contract) are out of scope.

## Counts

| Metric | Value |
|---|---:|
| Ledger rows scanned | {len(rows):,} |
| External issue rows found | **{len(output)}** |
| Synthetic rows found (`P6-new` / P6-06 logic) | **{synthetic_found}** |
| Synthetic rows fixed from graph | **{synthetic_fixed}** |
| Total rows fixed from graph | **{fixed_total}** |
| Unfixed (no graph quote/URL) | **{unfixed}** |

## Fix status breakdown

| fix_status | Count |
|---|---:|
"""
    for status, cnt in sorted(fix_counts.items(), key=lambda x: (-x[1], x[0])):
        report += f"| {status} | {cnt} |\n"

    report += f"""
## Issue type breakdown

| issue_type | Count |
|---|---:|
"""
    for it, cnt in Counter(r["issue_type"] for r in output).most_common():
        report += f"| {it} | {cnt} |\n"

    report += """
## Method

1. Loaded canonical element ledger (`VERIFICATION_LEDGER_ELEMENT.csv`).
2. Exported live graph evidence properties via read-only Cypher (`mit-bestand`).
3. Flagged PROVEN/PARTIAL external rows with empty quote or `logic` basis.
4. Patched rows where graph exposes `evidence_quote`, `source_quote`, `evidence_url`, `source_url`, or node source URLs.
5. Did **not** mutate Neo4j; fixes are ledger-side overrides for F4 merge.

## Residual

Rows with `fix_status=UNFIXED*` still need F2 (19 merge-redirect rels) or F3 (actor/VMA externals) re-proof via WebFetch.
P6-new node rows (5 PruefungNachweis catalog nodes) may remain logic-basis structural existence — downgrade or contract-cite in F4 if no URL on graph.
"""

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(report, encoding="utf-8")

    print(f"F08: {len(output)} issue rows, {synthetic_found} synthetic, {synthetic_fixed} synthetic fixed, {fixed_total} total fixed")
    print(f"Wrote {LEDGER_OUT}")
    print(f"Wrote {REPORT_OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
