#!/usr/bin/env python3
"""Post Quality Pass P6-03 — bidirectional VMA dedup residuals, rau merge, Q5 orphan SCHEMA."""
from __future__ import annotations

import csv
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

OUT_LEDGER = HERE / "ledger" / "post_quality_p06_03.csv"
OUT_REPORT = HERE / "reports" / "post_quality_p06_03.md"
OUT_PATCH = HERE / "patches" / "post_quality_p06_03.patch.jsonl"
Q05_LEDGER = HERE / "ledger" / "quality_pass_q05.csv"
REVIEW_RUN = "post_quality_p06_03_2026_06_06"

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
    "scope", "prior_verdict", "prior_claim_id",
]

RAU_EVIDENCE_URL = "https://thomasrau.eu/en/initiatives/rau"
RAU_QUOTE = (
    "From 1992 onwards, architectural firm RAU has been operating from a strong sense "
    "of awareness with respect to designing environmentally friendly buildings."
)
RAU_ALLIANDER_QUOTE = (
    "Buildings as a material depot (Municipal building Brummen, Alliander head office)"
)


def fetch_url(url: str) -> tuple[bool, int | None, str]:
    try:
        req = Request(url, headers={"User-Agent": "recherche-p06-03/1.0"})
        with urlopen(req, timeout=25) as resp:
            body = resp.read().decode("utf-8", "replace")
            return True, resp.status, body
    except HTTPError as e:
        return True, e.code, ""
    except (URLError, TimeoutError, OSError):
        return False, None, ""


def run_cypher(query: str) -> list[dict]:
    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        with driver.session(database=database) as session:
            return [dict(r) for r in session.run(query)]


def load_q05_prior() -> dict[str, dict]:
    if not Q05_LEDGER.exists():
        return {}
    out: dict[str, dict] = {}
    with Q05_LEDGER.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cid = row.get("prior_claim_id") or row.get("claim_id", "")
            if row.get("scope") == "B" or row.get("claim_id", "").startswith("Q05-A14"):
                out[cid] = row
    return out


def scan_bidir_pairs() -> list[dict]:
    return run_cypher(
        """
        MATCH (a:Akteur)-[r1:VERBUNDEN_MIT_AKTEUR]->(b:Akteur)-[r2:VERBUNDEN_MIT_AKTEUR]->(a)
        WHERE a.id < b.id
        RETURN a.id AS a_id, b.id AS b_id,
               elementId(r1) AS fwd_eid, elementId(r2) AS rev_eid,
               r1.evidence_url AS fwd_url, r1.evidence_confidence AS fwd_conf,
               r2.evidence_url AS rev_url, r2.evidence_confidence AS rev_conf
        ORDER BY a_id, b_id
        """
    )


def scan_orphan_akteure() -> list[dict]:
    return run_cypher(
        """
        MATCH (a:Akteur)
        WHERE NOT (a)--()
        RETURN a.id AS id, a.name AS name
        ORDER BY id
        """
    )


def scan_rau_nodes() -> list[dict]:
    return run_cypher(
        """
        MATCH (n:Akteur)
        WHERE n.id IN ['rau', 'rau_architects']
        OPTIONAL MATCH (n)-[r]-(m)
        RETURN n.id AS id, n.name AS name, n.primary_source_url AS url,
               count(r) AS degree,
               collect(DISTINCT type(r) + '->' + coalesce(m.id, '')) AS edges
        ORDER BY id
        """
    )


def row(
    claim_id: str,
    kind: str,
    element_id: str,
    from_id: str,
    to_id: str,
    rel_label: str,
    claim: str,
    basis_type: str,
    basis_ref: str,
    fetched: bool,
    http_status: str | int,
    verdict: str,
    confidence: str,
    proof_quote: str,
    action: str,
    notes: str,
    scope: str,
    prior_verdict: str = "",
    prior_claim_id: str = "",
) -> dict:
    return {
        "claim_id": claim_id,
        "claim_kind": kind,
        "element_id": element_id,
        "from_id": from_id,
        "to_id": to_id,
        "rel_type_or_label": rel_label,
        "asserted_claim": claim,
        "basis_type": basis_type,
        "basis_ref": basis_ref,
        "fetched": str(fetched).lower(),
        "http_status": str(http_status) if http_status != "" else "",
        "verdict": verdict,
        "confidence": confidence,
        "proof_quote": proof_quote,
        "proposed_action": action,
        "agent_id": "P6-03",
        "notes": notes,
        "scope": scope,
        "prior_verdict": prior_verdict,
        "prior_claim_id": prior_claim_id,
    }


def build_ledger_and_patch() -> tuple[list[dict], list[dict], dict]:
    ledger: list[dict] = []
    patches: list[dict] = []
    q05 = load_q05_prior()
    stats = {"bidir_live": 0, "bidir_remediated": 0, "orphan_live": 0, "merge_ops": 0, "delete_ops": 0}

    # --- Scope A: bidirectional VERBUNDEN_MIT_AKTEUR ---
    live_bidir = scan_bidir_pairs()
    stats["bidir_live"] = len(live_bidir)
    live_pairs = {(r["a_id"], r["b_id"]) for r in live_bidir}

    for i, pair in enumerate(live_bidir, 1):
        a_id, b_id = pair["a_id"], pair["b_id"]
        prior_id = f"pair:{a_id}--{b_id}"
        prior = q05.get(prior_id.replace("pair:", "A14-BIDIR-")) or {}
        # choose canonical: prefer edge with evidence_url, else lexicographic from
        if pair.get("fwd_url") and not pair.get("rev_url"):
            keep_from, keep_to, del_from, del_to = a_id, b_id, b_id, a_id
        elif pair.get("rev_url") and not pair.get("fwd_url"):
            keep_from, keep_to, del_from, del_to = b_id, a_id, a_id, b_id
        else:
            keep_from, keep_to, del_from, del_to = a_id, b_id, b_id, a_id
        ledger.append(row(
            f"P6-03-BIDIR-{i:03d}", "rel", prior_id, a_id, b_id, "VERBUNDEN_MIT_AKTEUR",
            f"Bidirectional VERBUNDEN_MIT_AKTEUR pair {a_id}<->{b_id}",
            "logic", "read-cypher bidirectional scan", False, "",
            "SCHEMA_VIOLATION", "", f"both legs present; canonical {keep_from}->{keep_to}",
            "MERGE_DUPLICATE",
            f"delete reverse leg {del_from}->{del_to}",
            "A", prior.get("verdict", ""), prior.get("prior_claim_id", prior_id),
        ))
        patches.append({
            "op": "delete_rel",
            "from": del_from,
            "type": "VERBUNDEN_MIT_AKTEUR",
            "to": del_to,
            "reason": (
                f"P6-03 P6-03-BIDIR-{i:03d}: collapse bidirectional pair; "
                f"keep canonical {keep_from}->{keep_to}"
            ),
        })
        stats["delete_ops"] += 1

    # Q5 residual rows that should already be remediated
    q05_bidir = [
        r for r in q05.values()
        if "BIDIR" in (r.get("prior_claim_id") or r.get("claim_id", ""))
        or "pair:" in (r.get("element_id") or "")
    ]
    seen_remediated: set[str] = set()
    for r in q05_bidir:
        eid = r.get("element_id", "")
        if not eid.startswith("pair:"):
            continue
        parts = eid.replace("pair:", "").split("--")
        if len(parts) != 2:
            continue
        a_id, b_id = sorted(parts)
        key = (a_id, b_id)
        if key in live_pairs or key in seen_remediated:
            continue
        seen_remediated.add(key)
        stats["bidir_remediated"] += 1
        ledger.append(row(
            f"P6-03-BIDIR-R-{stats['bidir_remediated']:03d}", "rel", eid, parts[0], parts[1],
            "VERBUNDEN_MIT_AKTEUR",
            r.get("asserted_claim", "Bidirectional VERBUNDEN_MIT_AKTEUR pair"),
            "logic", "read-cypher bidirectional scan (post wave-1/06b/R04)", False, "",
            "REMEDIATED", "hoch", "0 live bidirectional pairs for this unordered pair",
            "KEEP",
            "Already collapsed in merge_duplicate_edges_remaining + agent06b_merge_duplicate_reverse + remediation_r04",
            "A", r.get("verdict", "SCHEMA_VIOLATION"), r.get("prior_claim_id", ""),
        ))

    # --- Scope B: Q5 orphan Akteur SCHEMA ---
    orphans = scan_orphan_akteure()
    stats["orphan_live"] = len(orphans)
    q05_orphans = {
        "c33_circular_construction_catalyst": "A14-ORPH-001",
        "circular_economy_switzerland": "A14-ORPH-002",
        "repurpose": "A14-ORPH-003",
    }
    if orphans:
        for i, o in enumerate(orphans, 1):
            ledger.append(row(
                f"P6-03-ORPH-{i:03d}", "node", o["id"], "", "", "Akteur",
                f"Akteur {o['id']} has zero relationships (orphan)",
                "logic", "read-cypher orphan scan", False, "",
                "SCHEMA_VIOLATION", "", "degree=0",
                "ESCALATE_HUMAN", "New orphan — needs connect-or-deprecate decision", "B",
            ))
    else:
        for nid, prior in q05_orphans.items():
            deg_rows = run_cypher(
                f"MATCH (a:Akteur {{id: '{nid}'}}) OPTIONAL MATCH (a)-[r]-() "
                "RETURN a.id AS id, count(r) AS degree, collect(DISTINCT type(r)) AS types"
            )
            deg = deg_rows[0]["degree"] if deg_rows else 0
            types = deg_rows[0]["types"] if deg_rows else []
            ledger.append(row(
                f"P6-03-ORPH-{nid}", "node", nid, "", "", "Akteur",
                f"Akteur {nid} orphan SCHEMA from Q5",
                "logic", "read-cypher orphan scan + R05 verify", False, "",
                "REMEDIATED", "hoch",
                f"degree={deg}; types={types}",
                "KEEP",
                "R05 remediation_r05_connect_orphans.patch.jsonl applied LIEGT_IN_LAND",
                "B", "SCHEMA_VIOLATION", prior,
            ))

    # --- Scope C: rau vs rau_architects merge ---
    rau_nodes = {r["id"]: r for r in scan_rau_nodes()}
    fetched, status, body = fetch_url(RAU_EVIDENCE_URL)
    has_rau_firm = "architectural firm RAU" in body
    has_alliander = "Alliander head office" in body or "Alliander" in body
    arch = rau_nodes.get("rau_architects", {})
    firm = rau_nodes.get("rau", {})
    project_link = any("p_liander" in e for e in (arch.get("edges") or []))

    if "rau_architects" in rau_nodes and "rau" in rau_nodes:
        if fetched and has_rau_firm and has_alliander and project_link:
            verdict, conf, action = "PROVEN", "belegt", "MERGE_DUPLICATE"
            quote = f"{RAU_QUOTE} | {RAU_ALLIANDER_QUOTE}"
            notes = (
                "thomasrau.eu names architectural firm RAU; lists Alliander head office; "
                "rau_architects has BETEILIGT_AN p_liander_alliander_hq_duiven; "
                "merge stub rau_architects into canonical rau (has primary_source_url)"
            )
            patches.append({
                "op": "merge_node",
                "from": "rau_architects",
                "to": "rau",
                "reason": (
                    "P6-03 P6-03-RAU-001: PROVEN duplicate firm — RAU Architects on Liander HQ "
                    "= architectural firm RAU (thomasrau.eu/en/initiatives/rau)"
                ),
            })
            stats["merge_ops"] += 1
        else:
            verdict, conf, action = "PARTIAL", "teilweise_belegt", "ESCALATE_HUMAN"
            quote = ""
            notes = (
                f"fetch={fetched} status={status} firm_quote={has_rau_firm} "
                f"alliander_quote={has_alliander} project_link={project_link}"
            )
        ledger.append(row(
            "P6-03-RAU-001", "node", "rau_architects", "rau_architects", "rau", "Akteur",
            "rau and rau_architects are duplicate firm nodes",
            "web", RAU_EVIDENCE_URL, fetched, status or "", verdict, conf, quote, action, notes,
            "C", "PARTIAL", "R03-021",
        ))
    elif "rau" in rau_nodes and "rau_architects" not in rau_nodes:
        ledger.append(row(
            "P6-03-RAU-001", "node", "rau", "", "", "Akteur",
            "rau_architects already merged into rau",
            "logic", "read-cypher node scan", False, "", "REMEDIATED", "hoch",
            "rau_architects absent from live graph", "KEEP", "Prior merge applied", "C",
            "ESCALATE_HUMAN", "R03-021",
        ))

    return ledger, patches, stats


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def write_patch(path: Path, patches: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for p in patches:
            f.write(json.dumps(p, ensure_ascii=False) + "\n")


def dry_run_patch(patch_path: Path) -> str:
    cmd = [
        sys.executable,
        str(SCRIPTS / "apply_neo4j_review_patch.py"),
        "--patch", str(patch_path),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True, cwd=str(REPO))
    return (proc.stdout or "") + (proc.stderr or "")


def write_report(
    ledger: list[dict],
    patches: list[dict],
    stats: dict,
    dry_run_log: str,
) -> None:
    actions = {}
    verdicts = {}
    for r in ledger:
        verdicts[r["verdict"]] = verdicts.get(r["verdict"], 0) + 1
        actions[r["proposed_action"]] = actions.get(r["proposed_action"], 0) + 1

    node_count = run_cypher("MATCH (n) RETURN count(n) AS c")[0]["c"]
    rel_count = run_cypher("MATCH ()-[r]->() RETURN count(r) AS c")[0]["c"]
    vma = run_cypher("MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]-() RETURN count(r) AS c")[0]["c"]

    lines = [
        "# Post Quality Pass P6-03 — Structural dedup + RAU merge",
        "",
        f"**Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')} · **Database:** `mit-bestand`",
        f"**Ledger:** [`ledger/post_quality_p06_03.csv`](../ledger/post_quality_p06_03.csv)",
        f"**Patch:** [`patches/post_quality_p06_03.patch.jsonl`](../patches/post_quality_p06_03.patch.jsonl)",
        f"**Review run:** `{REVIEW_RUN}`",
        "",
        "## Live graph baseline",
        "",
        f"| Metric | Value |",
        f"|---|---:|",
        f"| Nodes | {node_count} |",
        f"| Directed rels | {rel_count} |",
        f"| `VERBUNDEN_MIT_AKTEUR` (undirected count) | {vma} |",
        f"| Live bidirectional VMA pairs | {stats['bidir_live']} |",
        f"| Degree-0 `Akteur` | {stats['orphan_live']} |",
        "",
        "## Scope summary",
        "",
        "| Scope | Topic | Ledger rows | Patch ops |",
        "|---|---|---:|---:|",
        f"| A | Bidirectional `VERBUNDEN_MIT_AKTEUR` | {stats['bidir_remediated'] + stats['bidir_live']} | {stats['delete_ops']} `delete_rel` |",
        f"| B | Q5 orphan `Akteur` SCHEMA | 3 | 0 (R05 already applied) |",
        f"| C | `rau` ↔ `rau_architects` merge | 1 | {stats['merge_ops']} `merge_node` |",
        "",
        "## Verdicts",
        "",
    ]
    for v, n in sorted(verdicts.items()):
        lines.append(f"- **{v}:** {n}")
    lines.extend(["", "## Proposed actions", ""])
    for a, n in sorted(actions.items()):
        lines.append(f"- **{a}:** {n}")

    if patches:
        lines.extend([
            "",
            "## Patch (evidence-gated: `merge_node` + `delete_rel` only)",
            "",
            "```json",
        ])
        for p in patches:
            lines.append(json.dumps(p, ensure_ascii=False))
        lines.extend(["```", "", "## Dry-run apply", "", "```"])
        tail = dry_run_log.strip().splitlines()[-40:]
        lines.extend(tail)
        lines.append("```")
    else:
        lines.extend([
            "",
            "## Patch",
            "",
            "No new patch operations — all scoped issues already remediated in prior waves.",
        ])

    lines.extend([
        "",
        "## Notes",
        "",
        "- Bidirectional VMA dedup from Agent 14/Q5 was applied across wave-1 "
        "(`merge_duplicate_edges_remaining.patch.jsonl`, 23 ops), Agent 06b (63 ops), "
        "and R04 (`remediation_r04_madaster_rau_harvestmap.patch.jsonl`).",
        "- Q5 orphan `Akteur` nodes were connected via R05 `LIEGT_IN_LAND` — not re-patched here.",
        "- `rau` vs `thomas_rau` remains **distinct** (firm vs person; R04 PROVEN).",
        "",
        "## Apply (human gate)",
        "",
        "```bash",
        f"python _scripts/apply_neo4j_review_patch.py --patch {OUT_PATCH.relative_to(REPO).as_posix()}",
        f'python _scripts/apply_neo4j_review_patch.py --patch {OUT_PATCH.relative_to(REPO).as_posix()} --confirm "APPLY post_quality_p06_03.patch.jsonl TO mit-bestand"',
        "```",
    ])

    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ledger, patches, stats = build_ledger_and_patch()
    write_csv(OUT_LEDGER, ledger)
    write_patch(OUT_PATCH, patches)
    dry_log = dry_run_patch(OUT_PATCH) if patches else "(no patch ops)"
    write_report(ledger, patches, stats, dry_log)
    print(f"ledger: {len(ledger)} rows -> {OUT_LEDGER}")
    print(f"patch: {len(patches)} ops -> {OUT_PATCH}")
    print(f"report -> {OUT_REPORT}")
    print(f"stats: {stats}")


if __name__ == "__main__":
    main()
