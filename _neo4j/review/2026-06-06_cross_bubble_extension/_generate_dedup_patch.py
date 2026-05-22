"""Generate patch to dedupe bubble actor mesh edges (parallel + bidirectional)."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[3] / "_scripts"))
from neo4j import GraphDatabase
from neo4j_env import resolve_connection

OUT = Path(__file__).resolve().parent
CONF_RANK = {"belegt": 3, "teilweise_belegt": 2, "unsicher": 1}
RUN_RANK = {
    "cross_bubble_extension_2026_06_06": 6,
    "germany_reuse_bubble_2026_06_05": 5,
    "netherlands_reuse_bubble_2026_06_05": 4,
    "swiss_reuse_bubble_2026_06_05": 3,
    "france_reuse_bubble_2026_06_05": 2,
    "rotor_dc_reuse_bubble_2026_06_05": 1,
}


def pick_conf(a: str | None, b: str | None) -> str | None:
    if CONF_RANK.get(a or "", 0) >= CONF_RANK.get(b or "", 0):
        return a or b
    return b or a


def merge_props(keep: dict, drop: dict) -> dict:
    out = dict(keep)
    if drop.get("evidence_url") and drop["evidence_url"] != keep.get("evidence_url"):
        q1 = keep.get("evidence_quote") or ""
        q2 = drop.get("evidence_quote") or ""
        alt = f"alt_url: {drop['evidence_url']}"
        if q2 and q2 not in q1:
            extra = q2
        else:
            extra = alt
        out["evidence_quote"] = (q1 + " | " + extra).strip(" |") if q1 else extra
        if not out.get("evidence_url"):
            out["evidence_url"] = drop["evidence_url"]
    out["evidence_confidence"] = pick_conf(keep.get("evidence_confidence"), drop.get("evidence_confidence"))
    kr = RUN_RANK.get(keep.get("review_run") or "", 0)
    dr = RUN_RANK.get(drop.get("review_run") or "", 0)
    if dr > kr:
        out["review_run"] = drop.get("review_run")
        out["review_status"] = drop.get("review_status") or "evidence_on_properties"
    if not out.get("evidence_basis") and drop.get("evidence_basis"):
        out["evidence_basis"] = drop["evidence_basis"]
    if not out.get("connection_kind") and drop.get("connection_kind"):
        out["connection_kind"] = drop["connection_kind"]
    out["dedup_run"] = "cross_bubble_dedup_2026_06_06"
    return out


uri, u, pw, db = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(u, pw))
patch: list[dict] = []
report: dict = {"parallel_betrieben": [], "bidirectional_collapses": [], "missing_evidence_fixes": []}

with driver.session(database=db) as s:
    # A) BETRIEBEN_VON parallel to VERBUNDEN with evidence
    for row in s.run(
        """
        MATCH (a)-[r1:BETRIEBEN_VON]->(b)
        MATCH (a)-[r2:VERBUNDEN_MIT_AKTEUR]->(b)
        WHERE r2.evidence_url IS NOT NULL
        RETURN r1.id AS drop_id, a.id AS from_id, b.id AS to_id, r2.id AS keep_id
        """
    ):
        d = dict(row)
        report["parallel_betrieben"].append(d)
        patch.append({"op": "delete_rel", "id": d["drop_id"], "reason": "parallel_betrieben_von_superseded_by_verbunden"})

    # B) Bidirectional VERBUNDEN between Akteur pairs (bubble-tagged at least one side)
    pairs = s.run(
        """
        MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]-(b)
        WHERE r.review_run IS NOT NULL AND a.id < b.id
        WITH a, b, collect(r) AS rels
        WHERE size(rels) = 2
        RETURN a.id AS a_id, b.id AS b_id,
               [x IN rels | {
                 id: x.id,
                 from_id: startNode(x).id,
                 to_id: endNode(x).id,
                 evidence_url: x.evidence_url,
                 evidence_quote: x.evidence_quote,
                 evidence_confidence: x.evidence_confidence,
                 evidence_basis: x.evidence_basis,
                 review_run: x.review_run,
                 review_status: x.review_status,
                 connection_kind: x.connection_kind
               }] AS props
        """
    )
    for row in pairs:
        a_id, b_id = row["a_id"], row["b_id"]
        props = list(row["props"])
        canon_from, canon_to = (a_id, b_id) if a_id < b_id else (b_id, a_id)
        keep = next((p for p in props if p["from_id"] == canon_from and p["to_id"] == canon_to), None)
        drop = next((p for p in props if p is not keep), None)
        if not keep or not drop:
            continue
        merged = merge_props(keep, drop)
        report["bidirectional_collapses"].append(
            {"pair": f"{a_id}↔{b_id}", "keep": keep["id"], "drop": drop["id"]}
        )
        patch.append(
            {
                "op": "set_rel_properties",
                "id": keep["id"],
                "properties": {
                    k: v
                    for k, v in merged.items()
                    if k in {
                        "evidence_basis",
                        "evidence_confidence",
                        "evidence_url",
                        "evidence_quote",
                        "review_run",
                        "review_status",
                        "connection_kind",
                        "dedup_run",
                    }
                    and v is not None
                },
            }
        )
        patch.append({"op": "delete_rel", "id": drop["id"], "reason": "bidirectional_verbunden_collapse"})

    # C) Bubble-tagged VERBUNDEN/BETEILIGT_AN missing evidence fields — backfill from patch backups not done here;
    # only flag rels that have url but no confidence
    for row in s.run(
        """
        MATCH ()-[r]->()
        WHERE (r.review_run CONTAINS 'reuse_bubble' OR r.review_run CONTAINS 'cross_bubble')
          AND r.evidence_url IS NOT NULL AND r.evidence_confidence IS NULL
        RETURN r.id AS id LIMIT 100
        """
    ):
        rid = row["id"]
        report["missing_evidence_fixes"].append(rid)
        patch.append(
            {
                "op": "set_rel_properties",
                "id": rid,
                "properties": {
                    "evidence_confidence": "teilweise_belegt",
                    "review_status": "evidence_on_properties",
                    "dedup_run": "cross_bubble_dedup_2026_06_06",
                },
            }
        )

driver.close()

patch_path = OUT / "patches" / "bubble_edge_dedup_phase2.patch.jsonl"
patch_path.parent.mkdir(parents=True, exist_ok=True)
patch_path.write_text(
    "\n".join(json.dumps(r, ensure_ascii=False) for r in patch) + ("\n" if patch else ""),
    encoding="utf-8",
)
report_path = OUT / "dedup_plan.json"
report_path.write_text(json.dumps({**report, "patch_ops": len(patch)}, indent=2), encoding="utf-8")
print(json.dumps({"patch_ops": len(patch), "parallel": len(report["parallel_betrieben"]), "collapses": len(report["bidirectional_collapses"])}, indent=2))
