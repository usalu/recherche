"""Collect the set of nodes to cascade-delete for each delete-target project.

Cascade rule (auto-delete only):
  - Bauteilgruppe whose ONLY incoming reuse-entity edge is from this project (EXCLUSIVE)
  - DataIssue whose ONLY incoming/outgoing reuse-entity edge is from this project (EXCLUSIVE)
  - Kennwert whose ONLY connection is from this project
  - Quelle/Dossier whose id is name-scoped to this project AND has no other reuse-entity user

Surface-for-review (NOT auto-deleted):
  - Akteur / Bauwerk / Stadt / Tool / Methode — real-world entities even if exclusive
"""
from __future__ import annotations
import json, os
from pathlib import Path
from neo4j import GraphDatabase  # type: ignore

PASSWORD = Path(".neo4j_password").read_text(encoding="utf-8").strip().splitlines()[0]
URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687")
DB = os.environ.get("NEO4J_DATABASE", "mit-bestand")

DELETE_IDS = ["p_circle_house", "p_obk_27", "p_careno_becircular", "p_eggshell_pavilion", "p_granby_workshop"]

# OWNER set: entities that "own" auxiliary nodes (bauteilgruppen, dataissues, kennwerte, dossiers).
# Tool/Software can theoretically own a bauteilgruppe; Methode/Marktmodell are pure vocab (do not own).
OWNER_LABELS = ("Projekt", "Programm", "Tool", "Software")
REUSE_ENTITY_LABELS = OWNER_LABELS  # kept name for compatibility

# Labels we will cascade-delete (project-specific bookkeeping nodes)
CASCADE_LABELS = ("Bauteilgruppe", "DataIssue", "Kennwert")
# Labels we will cascade-delete ONLY if id is name-scoped to the project
DOSSIER_LABELS = ("Dossier",)


def collect_for(sess, pid: str) -> dict:
    """Return cascade + surface lists for one project id."""
    # All neighbours of pid with neighbour-side label sets + degree from OTHER reuse entities
    rows = list(sess.run(
        """
        MATCH (p {id:$pid})-[r]-(n)
        WITH p, n, collect(DISTINCT type(r)) AS rel_types, labels(n) AS n_labels
        OPTIONAL MATCH (other)-[r2]-(n)
          WHERE other.id <> $pid AND any(l IN $reuse_labels WHERE l IN labels(other))
        RETURN n.id AS id, n_labels AS labels, coalesce(n.name,'') AS name,
               rel_types, count(DISTINCT other) AS others
        """,
        pid=pid, reuse_labels=list(REUSE_ENTITY_LABELS),
    ))

    cascade_ids: list[dict] = []
    surface_ids: list[dict] = []
    project_slug = pid[2:] if pid.startswith("p_") else pid

    for r in rows:
        nid = r["id"]
        labs = list(r["labels"])
        others = r["others"]
        if others > 0:
            continue  # shared with at least one other reuse-entity — never cascade
        # Exclusive — categorise
        if any(l in CASCADE_LABELS for l in labs):
            cascade_ids.append({"id": nid, "labels": labs, "name": r["name"], "reason": f"exclusive {'/'.join(labs)}"})
        elif "Dossier" in labs and project_slug in nid:
            cascade_ids.append({"id": nid, "labels": labs, "name": r["name"], "reason": "exclusive project-scoped Dossier (id contains project slug)"})
        else:
            surface_ids.append({"id": nid, "labels": labs, "name": r["name"], "rel_types": r["rel_types"], "reason": "exclusive real-world entity — surface for review"})
    return {"project_id": pid, "cascade": cascade_ids, "surface": surface_ids}


driver = GraphDatabase.driver(URI, auth=("neo4j", PASSWORD))
out: list[dict] = []
with driver.session(database=DB, default_access_mode="READ") as sess:
    for pid in DELETE_IDS:
        out.append(collect_for(sess, pid))
driver.close()

HERE = Path(__file__).resolve().parent
target = HERE / "cascade_targets.json"
target.write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Summary
for entry in out:
    print(f"\n== {entry['project_id']} ==")
    print(f"  cascade ({len(entry['cascade'])}):")
    for c in entry["cascade"]:
        print(f"    [{'+'.join(sorted(c['labels']))}] {c['id']}  ::  {c['name']}")
    print(f"  surface ({len(entry['surface'])}):")
    for s in entry["surface"]:
        print(f"    [{'+'.join(sorted(s['labels']))}] {s['id']}  ::  {s['name']}  rels={s['rel_types']}")
print(f"\nWrote {target}")
