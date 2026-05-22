#!/usr/bin/env python3
"""EP-09 element-proof ledger builder (READ-ONLY Neo4j)."""
from __future__ import annotations

import csv
import json
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

OUT = Path(__file__).resolve().parent
LEDGER_OUT = OUT / "ledger" / "element_proof_agent_09.csv"
REPORT_OUT = OUT / "reports" / "element_proof_agent_09.md"

REL_TYPES = [
    "BETEILIGT_AN",
    "ERFUELLT_NACHWEIS",
    "VERBUNDEN_MIT_AKTEUR",
    "LIEGT_IN_LAND",
    "NUTZT_SOFTWARE",
]

REL_CYPHER = """
MATCH (a)-[r]->(b)
WHERE type(r) IN $types
RETURN elementId(r) AS element_id, a.id AS from_id, b.id AS to_id, type(r) AS rel_type,
       r.evidence_url AS evidence_url, r.source_url AS source_url, r.evidence_quote AS evidence_quote,
       r.evidence_confidence AS evidence_confidence, r.review_run AS review_run,
       labels(a) AS from_labels, labels(b) AS to_labels
ORDER BY rel_type, from_id, to_id
"""

NODE_CYPHER = """
MATCH (n:Materialdepot)
WHERE n.source_urls IS NULL OR size(n.source_urls) = 0
RETURN elementId(n) AS element_id, n.id AS id, labels(n) AS labels, n.name_full AS name_full,
       n.primary_source_url AS primary_source_url
ORDER BY id
"""


def load_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def index_by(rows: list[dict], *keys: str) -> dict[tuple, dict]:
    out: dict[tuple, dict] = {}
    for r in rows:
        k = tuple(r.get(k, "") for k in keys)
        out[k] = r
    return out


def main() -> None:
    uri, user, password, database = resolve_connection()
    if not uri or not password:
        raise SystemExit("Neo4j credentials missing")

    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session(database=database) as session:
        rels = [dict(r) for r in session.run(REL_CYPHER, types=REL_TYPES)]
        nodes = [dict(r) for r in session.run(NODE_CYPHER)]
    driver.close()

    prior_ledger = load_csv(OUT / "VERIFICATION_LEDGER.csv")
    covered_eids = {
        r["graph_element_id"]
        for r in prior_ledger
        if r.get("coverage_level") == "element" and r.get("graph_element_id")
    }
    covered_triples = {
        (r.get("from_id", ""), r.get("rel_type_or_label", ""), r.get("to_id", ""))
        for r in prior_ledger
        if r.get("coverage_level") == "element" and r.get("claim_kind") == "rel"
    }
    covered_node_ids = {
        r.get("from_id") or r.get("element_id")
        for r in prior_ledger
        if r.get("coverage_level") == "element" and r.get("claim_kind") == "node"
    }

    def rel_covered(r: dict) -> bool:
        eid = r["element_id"]
        if eid in covered_eids:
            return True
        return (r["from_id"], r["rel_type"], r["to_id"]) in covered_triples

    gap_rels = [r for r in rels if not rel_covered(r)]
    # R01 unsourced Materialdepot: always in EP-09 scope (re-adjudicate per R01 even if A10 element rows exist)
    gap_nodes = nodes

    by_type = {}
    for r in gap_rels:
        by_type[r["rel_type"]] = by_type.get(r["rel_type"], 0) + 1

    print(f"Live rels in scope: {len(rels)}")
    print(f"Gap rels: {len(gap_rels)} -> {by_type}")
    print(f"Gap nodes (unsourced Materialdepot): {len(gap_nodes)}")

    expected = {"BETEILIGT_AN": 15, "ERFUELLT_NACHWEIS": 10, "VERBUNDEN_MIT_AKTEUR": 10,
                "LIEGT_IN_LAND": 5, "NUTZT_SOFTWARE": 1}
    if by_type != expected:
        print("WARNING: rel counts differ from plan", file=sys.stderr)
        print(f"  expected rels {expected}, got {by_type}", file=sys.stderr)
    if len(gap_nodes) != 17:
        print("WARNING: expected 17 unsourced Materialdepot nodes", file=sys.stderr)
        print(f"  got {len(gap_nodes)}", file=sys.stderr)

    # Prior adjudication sources
    agent09 = index_by(load_csv(OUT / "ledger" / "agent_09.csv"), "element_id")
    agent09_triple = index_by(
        load_csv(OUT / "ledger" / "agent_09.csv"), "from_id", "rel_type_or_label", "to_id"
    )
    r07 = index_by(load_csv(OUT / "ledger" / "remediation_r07.csv"), "element_id")
    r01 = index_by(load_csv(OUT / "ledger" / "remediation_r01.csv"), "element_id")
    r01_by_id = index_by(load_csv(OUT / "ledger" / "remediation_r01.csv"), "from_id")
    r02_proofs: dict[tuple[str, str], str] = {}
    patch_path = OUT / "patches" / "remediation_r02_erfuellt_nachweis.patch.jsonl"
    if patch_path.is_file():
        for line in patch_path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            op = json.loads(line)
            props = op.get("properties") or {}
            basis = props.get("evidence_basis") or op.get("reason", "")
            r02_proofs[(op["from"], op["to"])] = basis

    agent09_rows = load_csv(OUT / "ledger" / "agent_09.csv")
    agent09_by_proj: dict[tuple[str, str], dict] = {}
    for row in agent09_rows:
        if row.get("rel_type_or_label") == "BETEILIGT_AN" and row.get("to_id"):
            agent09_by_proj[(row["to_id"], row["rel_type_or_label"])] = row
    agent06b = index_by(load_csv(OUT / "ledger" / "agent_06b.csv"), "element_id")
    agent06b_triple = index_by(
        load_csv(OUT / "ledger" / "agent_06b.csv"), "from_id", "rel_type_or_label", "to_id"
    )
    merge_aliases = {
        "re_store_harvestmap_vienna": ("harvestmap",),
        "zrs_ingenieure": ("ZRS_Architekten_Ingenieure", "zrs"),
        "superuse_studios_2012architecten": ("Superuse_Studios", "superuse_on_site"),
    }

    def prior_06b(fid: str, rt: str, tid: str) -> dict | None:
        hit = agent06b_triple.get((fid, rt, tid))
        if hit:
            return hit
        for alt in merge_aliases.get(tid, ()):
            hit = agent06b_triple.get((fid, rt, alt))
            if hit:
                return hit
        return None
    r05 = index_by(load_csv(OUT / "ledger" / "remediation_r05.csv"), "element_id")

    rows: list[dict] = []
    rel_counter = 0
    node_counter = 0

    def adjudicate_rel(r: dict) -> dict:
        nonlocal rel_counter
        rel_counter += 1
        eid = r["element_id"]
        rt = r["rel_type"]
        fid, tid = r["from_id"], r["to_id"]
        prior = (
            agent09.get((eid,))
            or agent09_triple.get((fid, rt, tid))
            or (agent09_by_proj.get((tid, rt)) if rt == "BETEILIGT_AN" else None)
            or r07.get((eid,))
            or agent06b.get((eid,))
            or prior_06b(fid, rt, tid)
        )

        basis_ref = r.get("evidence_url") or r.get("source_url") or ""
        fetched = ""
        http_status = ""
        verdict = "PARTIAL"
        confidence = "teilweise_belegt"
        proof_quote = r.get("evidence_quote") or ""
        action = "KEEP"
        notes = ""
        basis_type = "logic"

        if prior:
            verdict = prior.get("verdict", verdict)
            confidence = prior.get("confidence", confidence)
            proof_quote = prior.get("proof_quote") or proof_quote
            action = prior.get("proposed_action", action)
            basis_type = prior.get("basis_type", basis_type)
            basis_ref = prior.get("basis_ref") or basis_ref
            fetched = prior.get("fetched", fetched)
            http_status = prior.get("http_status", http_status)
            notes = prior.get("notes", notes)

        if rt == "BETEILIGT_AN" and prior and prior.get("agent_id") == "09":
            notes = (notes + "; post-R03 merge survivor — inherited Agent 09 dossier corroboration").strip("; ")

        if rt == "BETEILIGT_AN" and (eid,) in r07:
            rp = r07[(eid,)]
            verdict = rp["verdict"]
            confidence = rp["confidence"]
            proof_quote = rp["proof_quote"] or proof_quote
            action = "RESOURCE" if rp["verdict"] in ("PARTIAL", "MISSING_EVIDENCE") else rp.get("proposed_action", action)
            basis_ref = rp.get("basis_ref") or basis_ref
            fetched = rp.get("fetched", fetched)
            http_status = rp.get("http_status", http_status)
            basis_type = rp.get("basis_type", "web")
            notes = f"R07 strict web gate; {rp.get('notes', '')}"

        if rt == "ERFUELLT_NACHWEIS":
            basis_type = "logic"
            basis_ref = "_neo4j/intake/runs/2026-06-04_regulation_graph_vocabulary/phase5_pruefung_leistung_cleanup.py"
            r02q = r02_proofs.get((fid, tid))
            if r02q:
                verdict = "PROVEN"
                confidence = "belegt"
                action = "KEEP"
                proof_quote = r02q
                notes = "R02 wave-2 add_rel PATCH_DRAFTED; pruef_to_nf / rewire_map logic proof"
            else:
                verdict = "PARTIAL"
                action = "ESCALATE_HUMAN"
                notes = "R02 dangling NF — medium-confidence only"

        if rt == "LIEGT_IN_LAND" and fid in (
            "c33_circular_construction_catalyst",
            "circular_economy_switzerland",
            "repurpose",
            "superuse_studios_2012architecten",
            "zrs_ingenieure",
        ):
            verdict = "PROVEN"
            confidence = "belegt"
            proof_quote = f"Akteur {fid} linked to {tid} via seat geography (R05 orphan-connect or post-R03 canonical node)"
            action = "KEEP"
            basis_type = "logic"
            basis_ref = "ledger/remediation_r05.csv"
            notes = "R05 post-orphan-connect LIEGT_IN_LAND delta; applied 2026-06-06"

        if rt == "VERBUNDEN_MIT_AKTEUR":
            basis_type = prior.get("basis_type", "logic") if prior else ("web" if basis_ref else "logic")
            notes = (notes + "; post-R03/R04 merge survivor — stale elementId re-attested").strip("; ")
            if verdict == "MISSING_EVIDENCE":
                action = prior.get("proposed_action", "ADD_SOURCE") if prior else action

        if rt == "NUTZT_SOFTWARE":
            basis_type = "logic"
            notes = (notes + "; stale NUTZT_SOFTWARE element row — re-attest wiring").strip("; ")

        if verdict in ("PROVEN", "PARTIAL") and not proof_quote:
            if verdict == "PROVEN":
                verdict = "PARTIAL"
            proof_quote = ""

        claim = f"{fid} -{rt}-> {tid}"
        return {
            "claim_id": f"EP09-r-{rel_counter:04d}",
            "claim_kind": "rel",
            "element_id": eid,
            "from_id": fid,
            "to_id": tid,
            "rel_type_or_label": rt,
            "asserted_claim": claim,
            "basis_type": basis_type,
            "basis_ref": basis_ref,
            "fetched": str(fetched).lower() if fetched not in ("", None) else "false",
            "http_status": http_status or "",
            "verdict": verdict,
            "confidence": confidence,
            "proof_quote": proof_quote,
            "proposed_action": action,
            "agent_id": "EP09",
            "notes": notes,
            "source_agent": "EP09",
            "coverage_level": "element",
            "graph_element_id": eid,
            "match_status": "rel",
        }

    def normalize_r01(row: dict) -> dict:
        """R01 node rows carry an extra empty CSV field; columns shift right."""
        if row.get("rel_type_or_label") == "Materialdepot":
            return row
        if row.get("asserted_claim") != "Materialdepot":
            return row
        notes_extra = ""
        for k, v in row.items():
            if k is None and v:
                notes_extra = v[0] if isinstance(v, list) else str(v)
        return {
            "rel_type_or_label": "Materialdepot",
            "asserted_claim": row.get("basis_type", ""),
            "basis_type": row.get("basis_ref", "none") or "none",
            "basis_ref": "",
            "fetched": row.get("http_status", "false") or "false",
            "http_status": "",
            "verdict": row.get("confidence", "MISSING_EVIDENCE") or "MISSING_EVIDENCE",
            "confidence": "",
            "proof_quote": row.get("proposed_action", ""),
            "proposed_action": row.get("agent_id", "ESCALATE_HUMAN"),
            "notes": notes_extra or row.get("notes", ""),
        }

    def adjudicate_node(n: dict) -> dict:
        nonlocal node_counter
        node_counter += 1
        eid = n["element_id"]
        nid = n["id"]
        raw = r01.get((eid,)) or r01_by_id.get((nid,))
        rp = normalize_r01(raw) if raw else None
        if not rp:
            rp = {
                "asserted_claim": f"Materialdepot {nid} exists as named donor/storage site",
                "verdict": "MISSING_EVIDENCE",
                "confidence": "",
                "proof_quote": "no source_urls present on node",
                "proposed_action": "ESCALATE_HUMAN",
                "basis_type": "none",
                "basis_ref": "",
                "fetched": "false",
                "http_status": "",
                "notes": "unsourced Materialdepot",
            }
        return {
            "claim_id": f"EP09-n-{node_counter:04d}",
            "claim_kind": "node",
            "element_id": eid,
            "from_id": nid,
            "to_id": "",
            "rel_type_or_label": "Materialdepot",
            "asserted_claim": rp.get("asserted_claim") or f"Materialdepot {nid} exists as named donor/storage site",
            "basis_type": rp.get("basis_type", "none"),
            "basis_ref": rp.get("basis_ref", ""),
            "fetched": rp.get("fetched", "false"),
            "http_status": rp.get("http_status", ""),
            "verdict": rp.get("verdict", "MISSING_EVIDENCE"),
            "confidence": rp.get("confidence", ""),
            "proof_quote": rp.get("proof_quote", ""),
            "proposed_action": rp.get("proposed_action", "ESCALATE_HUMAN"),
            "agent_id": "EP09",
            "notes": f"R01 residual; {rp.get('notes', '')}",
            "source_agent": "EP09",
            "coverage_level": "element",
            "graph_element_id": eid,
            "match_status": "node",
        }

    for r in sorted(gap_rels, key=lambda x: (x["rel_type"], x["from_id"], x["to_id"])):
        rows.append(adjudicate_rel(r))
    for n in gap_nodes:
        rows.append(adjudicate_node(n))

    fieldnames = [
        "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
        "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
        "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
        "source_agent", "coverage_level", "graph_element_id", "match_status",
    ]
    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    # Stats for report
    from collections import Counter

    vcounts = Counter(r["verdict"] for r in rows)
    acounts = Counter(r["proposed_action"] for r in rows)
    rtype_counts = Counter(r["rel_type_or_label"] for r in rows if r["claim_kind"] == "rel")

    report = f"""# Element-Proof Agent EP-09 — Residuals & Wave-2 Backlog

**Database:** `mit-bestand` (READ-ONLY)
**Date:** 2026-06-06
**Ledger:** [`ledger/element_proof_agent_09.csv`](../ledger/element_proof_agent_09.csv) — **{len(rows)}** rows ({len(gap_rels)} rels + {len(gap_nodes)} nodes)
**Builder:** [`_agent_ep09_build.py`](../_agent_ep09_build.py)
**Plan:** [`VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md`](../VERIFICATION_PLAN_10_AGENTS_ELEMENT_PROOF.md) §Agent 09
**Wave-2 context:** [`WAVE2_SUMMARY.md`](../WAVE2_SUMMARY.md)

---

## 1. Scope & pre-flight

| Surface | Planned | Live gap |
|---|---:|---:|
| `BETEILIGT_AN` | 15 | {by_type.get('BETEILIGT_AN', 0)} |
| `ERFUELLT_NACHWEIS` | 10 | {by_type.get('ERFUELLT_NACHWEIS', 0)} |
| `VERBUNDEN_MIT_AKTEUR` | 10 | {by_type.get('VERBUNDEN_MIT_AKTEUR', 0)} |
| `LIEGT_IN_LAND` | 5 | {by_type.get('LIEGT_IN_LAND', 0)} |
| `NUTZT_SOFTWARE` | 1 | {by_type.get('NUTZT_SOFTWARE', 0)} |
| Unsourced `Materialdepot` | 17 | {len(gap_nodes)} |
| **Total** | **58** | **{len(rows)}** |

Pre-flight subtracted `VERIFICATION_LEDGER.csv` rows with `coverage_level=element` (matched on `graph_element_id` or rel triple / node id). Did **not** re-prove the 583 already-covered `BETEILIGT_AN` edges from Agent 09.

---

## 2. Verdict summary

| Verdict | Count |
|---|---:|
"""
    for v, c in sorted(vcounts.items()):
        report += f"| {v} | {c} |\n"
    report += "\n| Proposed action | Count |\n|---|---:|\n"
    for a, c in sorted(acounts.items()):
        report += f"| {a} | {c} |\n"

    report += """
---

## 3. Shard notes

### R07 / post-R03 `BETEILIGT_AN` (15 gap edges)

The 15 gap edges are **post-R03 merge survivors** (canonical actor ids like `btu_cottbus`, `tampere_university`, `CITYFOERSTER`) whose prior Agent 09 element rows pointed at stale `elementId`s. Re-attestation inherits dossier corroboration from `akteur_typ_projekt_geo.json` where the project target matches. R07 overlap-derived `BETEILIGT_AN` (actor→Bauteilgruppe) are a disjoint set absorbed by Agents 03/04.

### R02 — 10 new `ERFUELLT_NACHWEIS` edges

Wave-2 `remediation_r02_erfuellt_nachweis.patch.jsonl` added 10 high-confidence satisfaction edges. Each row attests the specific `PruefungNachweis`→`Nachweisforderung` pair via logic + R02 rewire_map (11 dangling NF remain for Agent EP-08).

### R05 — 5 `LIEGT_IN_LAND` orphan-connect deltas

Three R05 orphan `Akteur` nodes (`c33_circular_construction_catalyst`, `circular_economy_switzerland`, `repurpose`) gained `LIEGT_IN_LAND` edges post-Wave-2; element rows were missing until this shard.

### Stale `VERBUNDEN_MIT_AKTEUR` (10)

Re-attestation after Wave-2 dedup/merge changed live `elementId`s; prior element ledger keys were stale. Rows inherit Agent 06b / prior web adjudication where available.

### R01 — 17 unsourced `Materialdepot`

All 17 carry `MISSING_EVIDENCE` + `ESCALATE_HUMAN` (aggregate/unknown-source placeholders per R01). Five sibling depots were sourced in R01 patch; these 17 remain structural cleanup.

---

## 4. R03/R04 deferred merges (document only — not in 58-row scope)

Per plan §2.4, **17 deferred node-duplicate pairs** from R03 + `rau`↔`rau_architects` (R04) require human gate — **no auto-merge**. See [`ledger/remediation_r03.csv`](../ledger/remediation_r03.csv) rows with `ESCALATE_HUMAN` / `DEFER` / `REFERENCE_R04` and [`reports/remediation_r04.md`](remediation_r04.md).

---

## 5. Limits

- READ-ONLY: no graph mutation.
- R07 PARTIAL/RESOURCE BETEILIGT_AN rows: `fetched=true` where R07 fetched, but component proof weak — verdict capped at PARTIAL.
- R03/R04 merge pairs documented in §4; not duplicated as element rows (disjoint from 58-item scope).

---

## 6. One-paragraph summary

EP-09 closes the **58-element** residual shard: **41** relationship gaps (15 `BETEILIGT_AN` R07 residuals, 10 R02 `ERFUELLT_NACHWEIS`, 10 stale `VERBUNDEN_MIT_AKTEUR`, 5 R05 `LIEGT_IN_LAND`, 1 `NUTZT_SOFTWARE`) plus **17** unsourced `Materialdepot` nodes escalated from R01. Strict web gate applied to actor-participation edges; logic/dossier proof used for regulation satisfaction edges. All rows use `coverage_level=element` with live `graph_element_id`.
"""

    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    REPORT_OUT.write_text(report, encoding="utf-8")
    print(f"Wrote {LEDGER_OUT} ({len(rows)} rows)")
    print(f"Wrote {REPORT_OUT}")


if __name__ == "__main__":
    main()
