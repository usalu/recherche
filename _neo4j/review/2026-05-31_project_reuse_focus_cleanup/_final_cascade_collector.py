"""Final cascade collector: produces the full delete list for the live apply.

Inputs (hard-coded):
  - 6 project ids (5 originals + Up Sticks Dundee)
  - 12 surface entity ids the user explicitly authorized for delete
  - 1 surface entity SKIPPED (`meth_wiederverwendungskriterien` — referenced by
    bg_planned_stahlbeton_decke_montessori_maassluis_hollow_core_slabs which is
    NOT being deleted; would corrupt unrelated project)

Outputs:
  - final_cascade.json — categorized list (projects, surface, project-aux, actor-aux)
  - final_delete_targets.txt — flat newline-delimited id list for snapshot + cypher
"""
from __future__ import annotations
import json, os
from pathlib import Path
from neo4j import GraphDatabase  # type: ignore

PASSWORD = Path(".neo4j_password").read_text(encoding="utf-8").strip().splitlines()[0]
URI = os.environ.get("NEO4J_URI", "neo4j://127.0.0.1:7687")
DB = os.environ.get("NEO4J_DATABASE", "mit-bestand")

PROJECTS_TO_DELETE = [
    "p_circle_house", "p_obk_27", "p_careno_becircular", "p_eggshell_pavilion",
    "p_granby_workshop", "p_up_sticks_dundee",
]

SURFACE_TO_DELETE = [
    # Per user 2026-05-31 "1. yes delete 2. yes 3.yes 4. delet"
    "tool_retile",                                 # Careno tool
    "bw_granby_workshop_liverpool",                 # Granby donor Bauwerk
    "brussels_capital_region", "bbri",              # Careno Akteure
    "stadt_weil_am_rhein",                          # Eggshell Stadt
    "stadt_liverpool",                              # Granby Stadt
    "assemble", "granby_4_streets_clt",
    "granby_workshop_cic", "will_shannon", "lewis_jones",  # Granby Akteure
    "kasper_guldager_jensen",                       # Circle House Akteur
    "cyril_pressacco", "thibaut_barrault",          # OBK 27 Akteure
]

# Explicitly NOT deleted (the user said "delete" surface, but this one is referenced
# by an unrelated project's Bauteilgruppe — would corrupt Montessori Maassluis):
SKIPPED_SURFACE = [
    "meth_wiederverwendungskriterien",  # see CONFLICT_ANALYSIS update
]

ALL_OWNERS = PROJECTS_TO_DELETE + SURFACE_TO_DELETE
OWNER_LABELS = ("Projekt", "Programm", "Tool", "Software")
CASCADE_AUX_LABELS = ("Bauteilgruppe", "DataIssue", "Kennwert")
DOSSIER_LABELS = ("Dossier",)


def collect_for(sess, pid: str, all_deleted: set[str]) -> dict:
    """Per-owner: find aux neighbours where the ONLY owner-side connection that
    will SURVIVE this run is this entity (i.e., other owners are all in the delete set)."""
    rows = list(sess.run(
        """
        MATCH (p {id:$pid})-[r]-(n)
        WITH p, n, collect(DISTINCT type(r)) AS rel_types, labels(n) AS n_labels
        OPTIONAL MATCH (other)-[r2]-(n)
          WHERE other.id <> $pid AND any(l IN $owner_labels WHERE l IN labels(other))
        RETURN n.id AS id, n_labels AS labels, coalesce(n.name,'') AS name,
               rel_types, collect(DISTINCT other.id) AS other_owners
        """,
        pid=pid, owner_labels=list(OWNER_LABELS),
    ))

    cascade: list[dict] = []
    surface: list[dict] = []
    for r in rows:
        nid = r["id"]
        labs = list(r["labels"])
        other_owners = [o for o in r["other_owners"] if o]
        # Surviving owners = owners that won't be deleted in this run
        surviving = [o for o in other_owners if o not in all_deleted]
        if surviving:
            # Other live entity uses this neighbour — never cascade
            continue
        slug_match = pid[2:] if pid.startswith("p_") else pid
        if any(l in CASCADE_AUX_LABELS for l in labs):
            cascade.append({"id": nid, "labels": labs, "name": r["name"], "reason": f"exclusive-after-run {'/'.join(labs)}"})
        elif "Dossier" in labs and slug_match in nid:
            cascade.append({"id": nid, "labels": labs, "name": r["name"], "reason": "project-scoped Dossier (id contains owner slug)"})
        else:
            # Real-world entity (Akteur/Bauwerk/Stadt/Methode/Tool/...) — surface
            surface.append({"id": nid, "labels": labs, "name": r["name"], "rel_types": r["rel_types"], "reason": "real-world entity, not auto-cascaded"})
    return {"owner_id": pid, "cascade": cascade, "surface": surface}


def collect_actor_scoped_data_issues(sess, actor_id: str) -> list[dict]:
    """For an Akteur about to be deleted, collect DataIssue nodes whose id
    encodes this actor (di_no_src_<actor>, di_node_source_url_review__<actor>,
    di_actor_stub__<actor>__*). These would orphan if we leave them."""
    rows = list(sess.run(
        """
        MATCH (di:DataIssue)
        WHERE di.id STARTS WITH 'di_no_src_' + $aid
           OR di.id = 'di_node_source_url_review__' + $aid
           OR di.id STARTS WITH 'di_actor_stub__' + $aid + '__'
        RETURN di.id AS id, labels(di) AS labels, coalesce(di.name,'') AS name
        """,
        aid=actor_id,
    ))
    return [{"id": r["id"], "labels": list(r["labels"]), "name": r["name"], "reason": f"actor-scoped DataIssue for {actor_id}"} for r in rows]


driver = GraphDatabase.driver(URI, auth=("neo4j", PASSWORD))
result: list[dict] = []
all_deleted = set(ALL_OWNERS)

with driver.session(database=DB, default_access_mode="READ") as sess:
    # First pass: cascade per owner (using all_deleted as the "future state" filter)
    for owner in ALL_OWNERS:
        entry = collect_for(sess, owner, all_deleted)
        # If this owner is an Akteur (or Tool/Bauwerk/Stadt), also collect its scoped DataIssue
        info = sess.run("MATCH (n {id:$id}) RETURN labels(n) AS l", id=owner).single()
        owner_labels = list(info["l"]) if info else []
        if any(l in ("Akteur",) for l in owner_labels):
            entry["actor_data_issues"] = collect_actor_scoped_data_issues(sess, owner)
        else:
            entry["actor_data_issues"] = []
        entry["owner_labels"] = owner_labels
        result.append(entry)

driver.close()

HERE = Path(__file__).resolve().parent
(HERE / "final_cascade.json").write_text(json.dumps({"skipped_surface": SKIPPED_SURFACE, "owners": result}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Build flat delete list, dedupe, preserve aux-before-owner order
all_ids: list[str] = []
seen: set[str] = set()
for entry in result:
    for sub in entry["cascade"]:
        if sub["id"] not in seen:
            all_ids.append(sub["id"])
            seen.add(sub["id"])
    for sub in entry["actor_data_issues"]:
        if sub["id"] not in seen:
            all_ids.append(sub["id"])
            seen.add(sub["id"])
# Owners (projects + surface) last
for entry in result:
    if entry["owner_id"] not in seen:
        all_ids.append(entry["owner_id"])
        seen.add(entry["owner_id"])

(HERE / "final_delete_targets.txt").write_text("\n".join(all_ids) + "\n", encoding="utf-8")

# Summary
for entry in result:
    print(f"\n== {entry['owner_id']} [{'+'.join(sorted(entry['owner_labels']))}] ==")
    print(f"  cascade aux: {len(entry['cascade'])}")
    for c in entry["cascade"]:
        print(f"    [{'+'.join(sorted(c['labels']))}] {c['id']}")
    if entry["actor_data_issues"]:
        print(f"  actor-scoped DataIssue: {len(entry['actor_data_issues'])}")
        for d in entry["actor_data_issues"]:
            print(f"    {d['id']}")
    if entry["surface"]:
        print(f"  surface (NOT cascaded — would survive run): {len(entry['surface'])}")
        for s in entry["surface"]:
            print(f"    [{'+'.join(sorted(s['labels']))}] {s['id']}  rels={s['rel_types']}")

print(f"\nSkipped surface (would corrupt unrelated data): {SKIPPED_SURFACE}")
print(f"\nTOTAL distinct nodes to delete: {len(all_ids)}")
print(f"Wrote {HERE / 'final_cascade.json'}")
print(f"Wrote {HERE / 'final_delete_targets.txt'}")
