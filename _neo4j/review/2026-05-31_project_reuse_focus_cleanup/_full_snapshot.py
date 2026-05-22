"""Pre-apply snapshot: full properties + all rels for every id in
final_delete_targets.txt and projects.phaseB.merge_targets.txt. Writes one
JSON file with everything needed to manually reconstruct on rollback.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
from neo4j import GraphDatabase  # type: ignore


def _safe(obj):
    if obj is None or isinstance(obj, (str, int, float, bool)):
        return obj
    if isinstance(obj, dict):
        return {str(k): _safe(v) for k, v in obj.items()}
    if isinstance(obj, (list, tuple)):
        return [_safe(v) for v in obj]
    return str(obj)  # Neo4j Date, DateTime, Duration, Point, etc.

HERE = Path(__file__).resolve().parent
PASSWORD = Path(".neo4j_password").read_text(encoding="utf-8").strip().splitlines()[0]
URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687")
DB = os.environ.get("NEO4J_DATABASE", "mit-bestand")

delete_ids = [l.strip() for l in (HERE / "final_delete_targets.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
merge_ids = [l.strip() for l in (HERE / "projects.phaseB.merge_targets.txt").read_text(encoding="utf-8").splitlines() if l.strip()]
all_ids = list(dict.fromkeys(delete_ids + merge_ids))  # dedupe preserving order

print(f"Snapshotting {len(delete_ids)} delete targets + {len(merge_ids)} merge targets = {len(all_ids)} unique ids...")

driver = GraphDatabase.driver(URI, auth=("neo4j", PASSWORD))
out: list[dict] = []
with driver.session(database=DB, default_access_mode="READ") as sess:
    for nid in all_ids:
        rec = sess.run(
            "MATCH (n {id:$id}) RETURN labels(n) AS labels, properties(n) AS props",
            id=nid,
        ).single()
        if not rec:
            out.append({"id": nid, "found": False})
            continue
        rels = list(sess.run(
            """MATCH (n {id:$id})-[r]->(m)
               RETURN type(r) AS rt, properties(r) AS rprops, 'OUT' AS dir, m.id AS nid, m.name AS nname, labels(m) AS nlabels
               UNION ALL
               MATCH (n {id:$id})<-[r]-(m)
               RETURN type(r) AS rt, properties(r) AS rprops, 'IN' AS dir, m.id AS nid, m.name AS nname, labels(m) AS nlabels""",
            id=nid,
        ))
        out.append({
            "id": nid, "found": True,
            "labels": list(rec["labels"]),
            "properties": _safe(dict(rec["props"])),
            "rels": [{"type": r["rt"], "dir": r["dir"], "neighbour_id": r["nid"], "neighbour_name": r["nname"],
                      "neighbour_labels": list(r["nlabels"]), "properties": _safe(dict(r["rprops"]))} for r in rels],
        })
driver.close()

backup_dir = HERE.parents[1] / "backups" / "2026-05-31_project_reuse_focus_cleanup_pre_apply"
backup_dir.mkdir(parents=True, exist_ok=True)
backup_path = backup_dir / "snapshot.json"
backup_path.write_text(json.dumps({
    "snapshot_at": datetime.now(timezone.utc).isoformat(),
    "database": DB,
    "delete_target_count": len(delete_ids),
    "merge_target_count": len(merge_ids),
    "total_unique_ids": len(all_ids),
    "nodes": out,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"Wrote {backup_path}")
print(f"Found: {sum(1 for o in out if o.get('found'))}/{len(out)}")
