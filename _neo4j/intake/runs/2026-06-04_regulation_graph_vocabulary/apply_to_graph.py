"""Apply the regulation vocabulary + anchor connections to mit-bestand.

DRY-RUN BY DEFAULT: validates that every referenced node exists and reports counts,
WITHOUT writing. Pass --commit to actually MERGE nodes and edges.

Creates (all tagged review_run = regulation_graph_vocab_2026_06_04, source_scope on new nodes):
  - new vocab nodes from vocab_nodes.jsonl  (Regulierungsfrage / Nachweisforderung / Regelwerk)
  - vocab backbone edges from vocab_edges.csv
      GILT_IN_LAND, GESTUETZT_AUF_REGELWERK, ERFORDERT_NACHWEIS  -> rf/nf/rw merged
      BETRIFFT_MATERIAL, GILT_IN_LAND                            -> Land/Material MATCHed (not created)
  - anchor edges from anchor_edges.csv
      (Projekt|Bauteilgruppe|Bauteiltyp|Material|Bauwerk)-[:TRIGGERS_REGULIERUNGSFRAGE]->(rf)
      anchors MATCHed (never created); rf merged.

Rollback:
  MATCH ()-[r {review_run:'regulation_graph_vocab_2026_06_04'}]->() DELETE r;
  MATCH (n {source_scope:'regulation_graph_vocab_2026_06_04'}) DETACH DELETE n;

Usage:
  python apply_to_graph.py            # dry-run (validate + count)
  python apply_to_graph.py --commit   # write
"""

from __future__ import annotations

import csv
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from neo4j import GraphDatabase

from build_vocabulary_graph import RUN

OUT = Path(__file__).resolve().parent
URI, USER, PWD, DB = "bolt://localhost:7687", "neo4j", "ENTWERFENMITBESTAND", "mit-bestand"
NOW = datetime.now(timezone.utc).isoformat()

VOCAB_LABELS = {"Regulierungsfrage", "Nachweisforderung", "Regelwerk"}
# edge target/source that must already exist in the live graph (we MATCH, never create):
EXISTING_TARGET_TYPES = {"GILT_IN_LAND", "BETRIFFT_MATERIAL", "BETRIFFT_BAUTEILTYP"}


def load():
    nodes = [json.loads(l) for l in (OUT / "vocab_nodes.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
    vocab_edges = list(csv.DictReader((OUT / "vocab_edges.csv").open(encoding="utf-8")))
    anchor_edges = list(csv.DictReader((OUT / "anchor_edges.csv").open(encoding="utf-8")))
    return nodes, vocab_edges, anchor_edges


def validate(s, nodes, vocab_edges, anchor_edges):
    """Check every node that must pre-exist is present. Returns list of problems."""
    problems = []
    new_ids = {n["id"] for n in nodes}
    # targets that must exist (Land, Material) in vocab_edges
    need_existing = set()
    for e in vocab_edges:
        if e["edge_type"] in EXISTING_TARGET_TYPES:
            need_existing.add(e["to_node_id"])
    # anchor sources must exist
    anchor_ids = {e["from_node_id"] for e in anchor_edges}
    for ids, what in [(need_existing, "Land/Material target"), (anchor_ids, "anchor source")]:
        if not ids:
            continue
        found = {r["id"] for r in s.run("MATCH (n) WHERE n.id IN $ids RETURN n.id AS id", ids=list(ids))}
        for missing in sorted(ids - found):
            problems.append(f"MISSING {what}: {missing}")
    # anchor rf targets must be among new vocab nodes
    for e in anchor_edges:
        if e["to_node_id"] not in new_ids:
            problems.append(f"anchor edge -> unknown rf: {e['to_node_id']}")
    return problems


def commit(s, nodes, vocab_edges, anchor_edges):
    # 1. new vocab nodes
    for n in nodes:
        s.run(f"MERGE (x:`{n['label']}` {{id:$id}}) "
              "SET x.name=$name, x.source_scope=$scope, x.source_url=$url, x.review_run=$run",
              id=n["id"], name=n.get("name"), scope=RUN, url=n.get("source_url"), run=RUN)
    # 2. vocab backbone edges
    for e in vocab_edges:
        merge_edge(s, e["from_node_id"], e["to_node_id"], e["edge_type"], e)
    # 3. anchor edges
    for e in anchor_edges:
        merge_edge(s, e["from_node_id"], e["to_node_id"], e["edge_type"], e)


def merge_edge(s, a, b, etype, e):
    s.run(
        f"MATCH (x {{id:$a}}) MATCH (y {{id:$b}}) "
        f"MERGE (x)-[r:`{etype}`]->(y) "
        "SET r.review_run=$run, r.evidence_status=$st, r.source_url=$url, "
        "r.source_quote=$q, r.applicability_reason=$reason, r.confidence=$conf, r.created_at_utc=$now",
        a=a, b=b, run=RUN, st=e.get("evidence_status"), url=e.get("source_url"),
        q=e.get("source_quote"), reason=e.get("applicability_reason", ""),
        conf=float(e["confidence"]) if e.get("confidence") else None, now=NOW)


def main():
    do_commit = "--commit" in sys.argv
    nodes, vocab_edges, anchor_edges = load()
    drv = GraphDatabase.driver(URI, auth=(USER, PWD))
    with drv.session(database=DB) as s:
        problems = validate(s, nodes, vocab_edges, anchor_edges)
        print(f"nodes={len(nodes)}  vocab_edges={len(vocab_edges)}  anchor_edges={len(anchor_edges)}")
        if problems:
            print(f"\n!! {len(problems)} validation problems:")
            for p in problems[:40]:
                print("  ", p)
            print("\nAborting (fix references before --commit).")
            drv.close()
            return
        print("validation: OK — all pre-existing targets/anchors found.")
        if not do_commit:
            print("\nDRY-RUN (no writes). Re-run with --commit to apply.")
            drv.close()
            return
        commit(s, nodes, vocab_edges, anchor_edges)
        n = s.run("MATCH (n {source_scope:$r}) RETURN count(n) AS c", r=RUN).single()["c"]
        rels = s.run("MATCH ()-[r {review_run:$r}]->() RETURN count(r) AS c", r=RUN).single()["c"]
        print(f"\nCOMMITTED: {n} nodes, {rels} edges tagged review_run={RUN}")
    drv.close()


if __name__ == "__main__":
    main()
