"""
Richness + Re-supply audit.

Answers two questions the user raised:

1. Are the live :Projekt and :Bauteilgruppe nodes actually richer than what the
   batches give us? -> sample full property bags; surface properties that
   batches won't regenerate.

2. Do the batches REALLY re-supply enough evidence to replace the old vocab
   edges per :Bauteilgruppe and per :Projekt? -> per-project density compare,
   per-BG edge-fate count, flag the gaps.

Read-only.
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

OLD_VOCAB_RELS = {
    "HAT_METHODE", "HAT_AUFBEREITUNG", "HAT_RESSOURCENQUELLE",
    "HAT_WIEDERVERWENDUNGSART", "HAT_RUECKBAUVERFAHREN",
}
NEW_VOCAB_RELS = {
    "HAT_METHODE", "HAT_AUFBEREITUNG", "HAT_RESSOURCENQUELLE",
    "HAT_ERGEBNIS", "HAT_WIEDERVERWENDUNGSORT", "HAT_RUECKBAUVERFAHREN",
}


def load_graph():
    g = json.loads(NET.read_text(encoding="utf-8"))
    nodes = []
    for n in g["nodes"]:
        props = n.get("properties") or {}
        nodes.append({
            "elementId": n["elementId"],
            "id": props.get("id", n["elementId"]),
            "name": props.get("name", ""),
            "labels": n.get("labels", []),
            "properties": props,
        })
    by_eid = {n["elementId"]: n for n in nodes}
    by_label = defaultdict(list)
    for n in nodes:
        for lbl in n.get("labels", []):
            by_label[lbl].append(n)
    edges = []
    for e in g["edges"]:
        edges.append({"type": e["type"], "start": e["source"], "end": e["target"]})
    return by_eid, by_label, edges


def parse_batches() -> dict:
    """Return {project_id: list of {batch, rel, bg, target, conf}}.

    Headers vary across batches (an extra `source_label` column was added at index 4
    in batches 05+, shifting `relationship` from index 4 to 5). Parse the header row
    dynamically to find column indices.
    """
    rows_by_project: dict[str, list] = defaultdict(list)
    for md in sorted(BATCH_DIR.glob("reuse_taxonomy_v9_connection_expansion_batch_*.md")):
        if "open_questions" in md.name:
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")

        # Find the data table by walking lines: a markdown table is a header row
        # followed by a "|---|---|..." separator, then data rows.
        lines = text.splitlines()
        col_idx: dict[str, int] | None = None  # current header indices
        for line in lines:
            if not line.lstrip().startswith("|"):
                col_idx = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            # Separator row
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                continue
            # Header row detection — contains "project_id" and either "edge_id" or "id"
            if "project_id" in cells and ("edge_id" in cells or "id" in cells):
                col_idx = {name: i for i, name in enumerate(cells)}
                # Normalize: accept either `edge_id` or `id` as the edge identifier column
                if "edge_id" not in col_idx and "id" in col_idx:
                    col_idx["edge_id"] = col_idx["id"]
                continue
            # Data row — must have a valid edge_id and we must already know columns
            if not col_idx:
                continue
            if len(cells) <= max(col_idx.values()):
                continue
            edge_id = cells[col_idx["edge_id"]]
            if not re.fullmatch(r"v10[A-Z]?-\d+", edge_id):
                continue
            try:
                project_id = cells[col_idx["project_id"]]
                rel_type   = cells[col_idx.get("relationship", -1)]
                target     = cells[col_idx.get("target_node",  -1)]
                bg_id      = cells[col_idx.get("bauteilgruppe", -1)]
                conf       = cells[col_idx.get("confidence",    -1)]
                rows_by_project[project_id].append({
                    "batch": md.name,
                    "rel": rel_type,
                    "bg": bg_id,
                    "target": target,
                    "conf": conf,
                })
            except (IndexError, ValueError):
                continue
    return rows_by_project


def main() -> int:
    by_eid, by_label, edges = load_graph()
    batch_rows = parse_batches()

    print("=" * 78)
    print("1. PROPERTY-BAG RICHNESS — what carries info that batches won't regenerate")
    print("=" * 78)

    # 1a. :Projekt — sample richest nodes (most properties)
    print("\n--- :Projekt — property keys observed across all 86 nodes ---")
    projekt_prop_freq = Counter()
    for p in by_label["Projekt"]:
        projekt_prop_freq.update(p["properties"].keys())
    for prop, n in projekt_prop_freq.most_common():
        print(f"    {prop:<40} appears on {n:>3}/86 nodes")

    print("\n--- :Projekt — sample full property bag (densest 3) ---")
    projekts_sorted = sorted(by_label["Projekt"], key=lambda n: -len(n["properties"]))
    for p in projekts_sorted[:3]:
        print(f"\n  * {p['id']}  ({len(p['properties'])} properties)")
        for k, v in p["properties"].items():
            v_str = str(v)
            if len(v_str) > 100:
                v_str = v_str[:97] + "..."
            print(f"      {k:<32} = {v_str}")

    # 1b. :Bauteilgruppe — sample
    print("\n--- :Bauteilgruppe — property keys observed across all 356 nodes ---")
    bg_prop_freq = Counter()
    for b in by_label["Bauteilgruppe"]:
        bg_prop_freq.update(b["properties"].keys())
    for prop, n in bg_prop_freq.most_common():
        print(f"    {prop:<40} appears on {n:>3}/356 nodes")

    print("\n--- :Bauteilgruppe — sample 3 densest ---")
    bgs_sorted = sorted(by_label["Bauteilgruppe"], key=lambda n: -len(n["properties"]))
    for b in bgs_sorted[:3]:
        print(f"\n  * {b['id']}  ({len(b['properties'])} properties)")
        for k, v in b["properties"].items():
            v_str = str(v)
            if len(v_str) > 100:
                v_str = v_str[:97] + "..."
            print(f"      {k:<32} = {v_str}")

    # 1c. Bauteilgruppe — neighbouring labels (what else is attached besides old vocab)
    print("\n--- :Bauteilgruppe — outgoing edges by target label (top 15) ---")
    bg_eids = {b["elementId"] for b in by_label["Bauteilgruppe"]}
    bg_out_by_target_label = Counter()
    for e in edges:
        if e["start"] in bg_eids:
            tgt = by_eid.get(e["end"])
            if not tgt:
                continue
            for lbl in tgt["labels"]:
                bg_out_by_target_label[(lbl, e["type"])] += 1
    for (lbl, rel), n in sorted(bg_out_by_target_label.items(), key=lambda kv: -kv[1])[:15]:
        marker = "  [IN SCOPE]" if rel in OLD_VOCAB_RELS else ""
        print(f"    -[:{rel:<28}]->(:{lbl:<24}) {n:>5}{marker}")

    # ---------------------------------------------------------------
    print("\n" + "=" * 78)
    print("2. PER-PROJECT RE-SUPPLY DENSITY — old edges vs new batch rows")
    print("=" * 78)

    # Build proj_eid → proj_id, bg_eid → proj_id
    proj_eid_to_id = {p["elementId"]: p["id"] for p in by_label["Projekt"]}
    proj_id_to_name = {p["id"]: p["name"] for p in by_label["Projekt"]}
    bg_to_proj: dict[str, str] = {}  # bg_eid -> proj_id
    for e in edges:
        if e["type"] == "HAT_BAUTEILGRUPPE":
            if e["end"] in bg_eids and e["start"] in proj_eid_to_id:
                bg_to_proj[e["end"]] = proj_eid_to_id[e["start"]]

    # Per-project: count old edges per vocab type + count batch rows per new vocab type
    old_by_proj_vocab: dict[tuple[str, str], int] = Counter()
    for e in edges:
        if e["type"] not in OLD_VOCAB_RELS:
            continue
        # source could be :Projekt or :Bauteilgruppe
        if e["start"] in proj_eid_to_id:
            pid = proj_eid_to_id[e["start"]]
        elif e["start"] in bg_to_proj:
            pid = bg_to_proj[e["start"]]
        else:
            continue
        old_by_proj_vocab[(pid, e["type"])] += 1

    # Batch rows already grouped by project
    batch_by_proj_vocab: dict[tuple[str, str], int] = Counter()
    for pid, rows in batch_rows.items():
        for r in rows:
            rel = r["rel"]
            if rel in ("HAT_QUELLE", "HAS_SOURCE"):
                rel = "HAT_RESSOURCENQUELLE"
            elif rel in ("NUTZT_METHODE", "HAS_METHOD"):
                rel = "HAT_METHODE"
            elif rel in ("HAS_REUSE_RESULT",):
                rel = "HAT_ERGEBNIS"
            elif rel in ("HAS_LOCATION",):
                rel = "HAT_WIEDERVERWENDUNGSORT"
            elif rel in ("HAS_PROCESSING",):
                rel = "HAT_AUFBEREITUNG"
            elif rel in ("HAS_DISMANTLING", "HAS_DECONSTRUCTION"):
                rel = "HAT_RUECKBAUVERFAHREN"
            if rel in NEW_VOCAB_RELS:
                batch_by_proj_vocab[(pid, rel)] += 1

    # Header
    cols = [
        ("HAT_METHODE", "Method"),
        ("HAT_AUFBEREITUNG", "Aufber"),
        ("HAT_RESSOURCENQUELLE", "Quelle"),
        ("HAT_RUECKBAUVERFAHREN", "Rueckb"),
        ("HAT_WIEDERVERWENDUNGSART", "WVA"),
        ("HAT_ERGEBNIS", "Ergebn"),
        ("HAT_WIEDERVERWENDUNGSORT", "Ort"),
    ]
    all_projects = sorted(set(proj_id_to_name))

    print(f"\nFormat:  old / new  per axis. Projects where batch supply < old detail are flagged.\n")
    print(f"  {'project_id':<48}", end="")
    for rel, short in cols:
        print(f" {short:>8}", end="")
    print("   FLAG")

    flagged = []
    for pid in all_projects:
        line = f"  {pid:<48}"
        is_flagged = False
        flag_reason = []
        for rel, short in cols:
            old = old_by_proj_vocab.get((pid, rel), 0)
            new = batch_by_proj_vocab.get((pid, rel), 0)
            # For axes that the batches REPLACE 1:1 (HAT_METHODE, HAT_AUFBEREITUNG,
            # HAT_RESSOURCENQUELLE, HAT_RUECKBAUVERFAHREN) - we want new >= old (or close).
            # HAT_WIEDERVERWENDUNGSART is retired; new = 0 expected. Old indicates how much
            # detail is "lost" (it's not really lost; it's distributed across HAT_ERGEBNIS + HAT_WIEDERVERWENDUNGSORT + HAT_METHODE).
            # For new-only axes (HAT_ERGEBNIS, HAT_WIEDERVERWENDUNGSORT) - new comes from batches only.
            line += f" {old:>3}/{new:<3}"
            if rel in OLD_VOCAB_RELS and rel != "HAT_WIEDERVERWENDUNGSART":
                if old >= 3 and new < max(1, old // 3):
                    is_flagged = True
                    flag_reason.append(f"{short}-thin({old}→{new})")
        if is_flagged:
            line += f"   THIN: {','.join(flag_reason)}"
            flagged.append(pid)
        print(line)

    # ---------------------------------------------------------------
    print("\n" + "=" * 78)
    print("3. PER-BAUTEILGRUPPE EVIDENCE COVERAGE")
    print("=" * 78)
    print("For each live BG with old vocab edges, check if its project has batch coverage.")

    # Count old vocab edges per BG
    old_edges_per_bg: dict[str, Counter] = defaultdict(Counter)
    for e in edges:
        if e["type"] in OLD_VOCAB_RELS and e["start"] in bg_eids:
            old_edges_per_bg[e["start"]][e["type"]] += 1

    # Stats: how many BGs have N old edges
    bg_old_total = Counter()
    for bg_eid, ct in old_edges_per_bg.items():
        total = sum(ct.values())
        bg_old_total[total] += 1
    print("\nDistribution: how many BGs have N old-vocab edges?")
    for n_edges in sorted(bg_old_total):
        print(f"    BGs with {n_edges:>2} old-vocab edges: {bg_old_total[n_edges]}")

    # BGs that are EVIDENCE-HEAVY (>=5 old edges) — these are at highest risk if batches don't re-supply
    print("\nEvidence-heavy BGs (>=5 old vocab edges) — top 20 by old-edge count:")
    heavy = sorted(old_edges_per_bg.items(), key=lambda kv: -sum(kv[1].values()))[:20]
    for bg_eid, ct in heavy:
        bg = by_eid[bg_eid]
        pid = bg_to_proj.get(bg_eid, "?")
        batch_row_count = len(batch_rows.get(pid, []))
        total = sum(ct.values())
        breakdown = " ".join(f"{r[8:11]}:{n}" for r, n in ct.most_common())
        print(f"    {bg['id']:<55} proj={pid:<32} old={total:>2} ({breakdown})  batch_rows={batch_row_count}")

    # BGs whose PROJECT has zero batch coverage — gap candidates
    print("\nBGs whose project has zero or very few batch rows (<= 3):")
    gap_bgs = []
    for bg_eid, ct in old_edges_per_bg.items():
        pid = bg_to_proj.get(bg_eid, "?")
        batch_row_count = len(batch_rows.get(pid, []))
        if batch_row_count <= 3:
            gap_bgs.append((bg_eid, pid, sum(ct.values()), batch_row_count))
    print(f"    Count: {len(gap_bgs)}")
    for bg_eid, pid, old_count, batch_count in sorted(gap_bgs, key=lambda x: -x[2])[:20]:
        bg = by_eid[bg_eid]
        print(f"    {bg['id']:<55} proj={pid:<32} old={old_count:>2}  batch={batch_count}")

    # ---------------------------------------------------------------
    print("\n" + "=" * 78)
    print("4. SUMMARY")
    print("=" * 78)
    total_old = sum(old_by_proj_vocab.values())
    total_new = sum(batch_by_proj_vocab.values())
    print(f"\n  Total old vocab edges (5 rels) across all projects:  {total_old}")
    print(f"  Total new batch rows (6 rels) across all projects :  {total_new}")
    print(f"  Net density change:                                 {total_new - total_old:+d}")
    print(f"\n  Projects flagged (batch supply < old detail on ≥1 axis): {len(flagged)}")
    if flagged:
        print(f"  Flagged project ids:")
        for pid in flagged:
            print(f"    - {pid}  ({proj_id_to_name.get(pid,'?')})")
    print(f"\n  BGs whose project has near-zero batch rows: {len(gap_bgs)}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
