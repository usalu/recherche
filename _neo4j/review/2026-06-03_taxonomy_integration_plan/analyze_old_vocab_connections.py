"""
Coverage gap and connection-type analysis for the taxonomy integration.

Goal: prove (or disprove) that the new evidence batches replace the old
:Methode, :Aufbereitungsverfahren, :Ressourcenquelle data entirely, so the
plan can switch from migrate-then-archive to delete-with-prejudice.

Read-only. No graph writes.

Reads:
  - the 2026-06-02 full network export (full property bag on nodes, topology on edges)
  - the new-taxonomy-edit batch markdown for project coverage
"""

from __future__ import annotations
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"E:/recherche")
NET = ROOT / "_neo4j/review/2026-06-02_projekt_programm_full_network_export_mit-bestand/topology.json"
BATCH_DIR = ROOT / "_neo4j/intake/inbox/research/new taxonomy edit"
TARGET_LABELS = ("Methode", "Aufbereitungsverfahren", "Ressourcenquelle",
                  "WiederverwendungsArt", "Rueckbauverfahren")


def load_graph() -> tuple[dict, dict, list]:
    """Return (nodes_by_eid, nodes_by_label_index, edges).
    Schema: nodes have {elementId, labels, properties}; edges have {elementId, type, source, target}.
    Node business id lives in properties.id when present.
    """
    g = json.loads(NET.read_text(encoding="utf-8"))
    raw_nodes = g["nodes"]
    raw_edges = g["edges"]

    nodes = []
    for n in raw_nodes:
        props = n.get("properties") or {}
        nodes.append({
            "elementId": n["elementId"],
            "id": props.get("id", n["elementId"]),
            "name": props.get("name", ""),
            "labels": n.get("labels", []),
            "properties": props,
        })
    by_eid = {n["elementId"]: n for n in nodes}

    # Re-shape edges to use source/target consistently
    edges = []
    for e in raw_edges:
        edges.append({
            "elementId": e["elementId"],
            "type": e["type"],
            "start": e["source"],
            "end": e["target"],
        })

    by_label = defaultdict(list)
    for n in nodes:
        for lbl in n.get("labels", []):
            by_label[lbl].append(n)
    return by_eid, by_label, edges


def batch_project_slugs() -> set[str]:
    """Extract every batch project_id (`p_*`) appearing in batch markdown files."""
    seen: set[str] = set()
    for md in BATCH_DIR.glob("reuse_taxonomy_v9_connection_expansion_batch_*.md"):
        text = md.read_text(encoding="utf-8", errors="ignore")
        # batch IDs use snake_case p_* slugs in the project_id column
        for m in re.finditer(r"\b(p_[a-z0-9_]+)\b", text):
            seen.add(m.group(1))
    return seen


def main() -> int:
    by_eid, by_label, edges = load_graph()
    # Quick alias for downstream code that used `by_id`
    by_id = by_eid

    # --- 1. Node sets per target label (elementIds for edge lookup) ---
    target_node_ids: dict[str, set[str]] = {
        lbl: {n["elementId"] for n in by_label.get(lbl, [])} for lbl in TARGET_LABELS
    }
    print("=" * 78)
    print("1. NODE COUNTS PER TARGET LABEL (from 2026-06-02 network export)")
    print("=" * 78)
    for lbl, ids in target_node_ids.items():
        print(f"  {lbl:<24} {len(ids):>4}")
    print()

    # --- 2. List node names per label so we can eyeball semantic match ---
    print("=" * 78)
    print("2. NODES BY LABEL (id | name | inbound count from this export)")
    print("=" * 78)

    inbound_count: dict[str, int] = Counter()
    for e in edges:
        inbound_count[e["end"]] += 1

    for lbl in TARGET_LABELS:
        print(f"\n  --- :{lbl} ---")
        rows = []
        for n in by_label.get(lbl, []):
            rows.append((n["id"], n.get("name", ""), inbound_count.get(n["elementId"], 0)))
        rows.sort(key=lambda r: -r[2])
        for nid, name, inb in rows:
            print(f"    {nid:<48} {name:<48} {inb:>4}")
    print()

    # --- 3. Incoming-edge analysis per target label ---
    # For each target node, group inbound edges by (source label, rel type) so
    # we can see which upstreams would be orphaned by deletion.
    print("=" * 78)
    print("3. INBOUND EDGES TO EACH TARGET LABEL")
    print("    aggregated by (source_label, rel_type)")
    print("=" * 78)

    for lbl in TARGET_LABELS:
        target_ids = target_node_ids[lbl]
        upstream: Counter = Counter()
        for e in edges:
            if e["end"] in target_ids:
                src_node = by_id.get(e["start"])
                if not src_node:
                    continue
                src_labels = tuple(sorted(src_node.get("labels", [])))
                upstream[(src_labels, e["type"])] += 1
        print(f"\n  --- :{lbl} inbound ---")
        for (src_labels, rel), n in sorted(upstream.items(), key=lambda kv: -kv[1]):
            label_str = ":" + ":".join(src_labels)
            print(f"    ({label_str:<40})-[:{rel}]->  {n:>5}")
    print()

    # --- 4. Outgoing edges (each target label → ?) ---
    # If a target node has outbound edges, deleting the node breaks them too.
    print("=" * 78)
    print("4. OUTBOUND EDGES FROM EACH TARGET LABEL")
    print("=" * 78)

    for lbl in TARGET_LABELS:
        target_ids = target_node_ids[lbl]
        downstream: Counter = Counter()
        for e in edges:
            if e["start"] in target_ids:
                tgt_node = by_id.get(e["end"])
                if not tgt_node:
                    continue
                tgt_labels = tuple(sorted(tgt_node.get("labels", [])))
                downstream[(tgt_labels, e["type"])] += 1
        print(f"\n  --- :{lbl} outbound ---")
        if not downstream:
            print("    (none)")
            continue
        for (tgt_labels, rel), n in sorted(downstream.items(), key=lambda kv: -kv[1]):
            label_str = ":" + ":".join(tgt_labels)
            print(f"    -[:{rel}]-> ({label_str:<40}) {n:>5}")
    print()

    # --- 5. Project coverage gap ---
    # For each project that has at least one HAT_METHODE/HAT_AUFBEREITUNG/HAT_RESSOURCENQUELLE
    # edge anchored on its Bauteilgruppe, check whether that project is in batches.
    print("=" * 78)
    print("5. PROJECT COVERAGE GAP")
    print("=" * 78)

    # Build proj → bauteilgruppe set (keyed by elementId)
    proj_of_bg: dict[str, str] = {}
    for e in edges:
        if e["type"] == "HAT_BAUTEILGRUPPE":
            bg = by_id.get(e["end"])
            proj = by_id.get(e["start"])
            if bg and proj and "Bauteilgruppe" in bg.get("labels", []):
                proj_of_bg[bg["elementId"]] = proj["id"]

    # Build map: vocab-edge → project
    vocab_rels = {
        "Methode": "HAT_METHODE",
        "Aufbereitungsverfahren": "HAT_AUFBEREITUNG",
        "Ressourcenquelle": "HAT_RESSOURCENQUELLE",
        "WiederverwendungsArt": "HAT_WIEDERVERWENDUNGSART",
        "Rueckbauverfahren": "HAT_RUECKBAUVERFAHREN",
    }
    projects_with_old_edge: dict[str, set[str]] = {lbl: set() for lbl in TARGET_LABELS}
    for e in edges:
        for lbl, rel in vocab_rels.items():
            if e["type"] == rel:
                src = by_id.get(e["start"])
                tgt = by_id.get(e["end"])
                if not src or not tgt or lbl not in tgt.get("labels", []):
                    continue
                # source could be Bauteilgruppe or Projekt
                if "Bauteilgruppe" in src.get("labels", []):
                    proj = proj_of_bg.get(src["elementId"])
                    if proj:
                        projects_with_old_edge[lbl].add(proj)
                elif "Projekt" in src.get("labels", []):
                    projects_with_old_edge[lbl].add(src["id"])

    batch_pids = batch_project_slugs()
    # Build name-based match because batch ids are `p_<name>` and live ids are bare slug.
    live_projects = {n["id"]: n.get("name", "") for n in by_label.get("Projekt", [])}

    # Heuristic mapping: batch p_<x> → live id <x> by:
    #   1. exact match on stripped p_ prefix
    #   2. live id is a token substring of stripped batch id
    #   3. name-based: shared significant token between batch_pid (after p_) and live name (slug-ified)
    def slug(s: str) -> str:
        s = re.sub(r"[^\w]+", "_", s.lower())
        return re.sub(r"_+", "_", s).strip("_")

    def shared_tokens(a: str, b: str, min_len: int = 5) -> set[str]:
        ta = {t for t in a.split("_") if len(t) >= min_len}
        tb = {t for t in b.split("_") if len(t) >= min_len}
        return ta & tb

    def batch_to_live_candidates(batch_pid: str, live_ids: dict[str, str]) -> list[str]:
        stub = batch_pid[2:]  # drop p_
        hits: list[tuple[str, int]] = []
        for lid, lname in live_ids.items():
            score = 0
            if lid == stub:
                score = 100
            elif stub.startswith(lid + "_") and len(lid) >= 4:
                score = 90
            else:
                lname_slug = slug(lname)
                shared = shared_tokens(stub, lname_slug)
                shared |= shared_tokens(stub, lid)
                if shared:
                    score = 50 + len(shared) * 10
            if score > 0:
                hits.append((lid, score))
        if not hits:
            return []
        # Keep best-scoring; break ties
        hits.sort(key=lambda x: -x[1])
        best = hits[0][1]
        return [lid for lid, sc in hits if sc == best]

    batch_to_live: dict[str, list[str]] = {bp: batch_to_live_candidates(bp, live_projects)
                                             for bp in batch_pids}
    covered_live_ids: set[str] = set()
    for bp, hits in batch_to_live.items():
        covered_live_ids.update(hits)

    for lbl in TARGET_LABELS:
        old_projects = projects_with_old_edge[lbl]
        uncovered = old_projects - covered_live_ids
        print(f"\n  --- :{lbl} project coverage ---")
        print(f"    live projects total                : {len(live_projects)}")
        print(f"    projects appearing in batch ids    : {len(batch_pids)} (batch p_* slugs)")
        print(f"    live ids matched by batch ids      : {len(covered_live_ids)}")
        print(f"    live projects WITH old edges       : {len(old_projects)}")
        print(f"    live projects WITH old, NOT in batches: {len(uncovered)}")
        if uncovered:
            print(f"    uncovered project ids (first 20):")
            for pid in sorted(uncovered)[:20]:
                print(f"      - {pid} ({live_projects.get(pid,'?')})")
    print()

    # --- 6. Semantic-equivalence check for :Ressourcenquelle ---
    # The batch's six canonical Quelle buckets vs the live rq_* nodes.
    print("=" * 78)
    print("6. :Ressourcenquelle SEMANTIC EQUIVALENCE CHECK")
    print("=" * 78)
    print("    live rq_* nodes (id | name | inbound):")
    rq_nodes = sorted(
        ((n["id"], n.get("name", ""), inbound_count.get(n["id"], 0))
         for n in by_label.get("Ressourcenquelle", [])),
        key=lambda r: -r[2],
    )
    for nid, name, inb in rq_nodes:
        print(f"      {nid:<40} {name:<40} {inb:>4}")
    print()
    print("    batch's 6 canonical Quelle buckets:")
    for q in [
        "Externer_Spenderbau (190)",
        "Eigener_Bestand (55)",
        "Gleicher_Standort (17)",
        "Bauteilmarkt_oder_Lager (19)",
        "Leihgabe_oder_Service (4)",
        "Restposten_Abfall_Unbekannt (65)",
    ]:
        print(f"      {q}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
