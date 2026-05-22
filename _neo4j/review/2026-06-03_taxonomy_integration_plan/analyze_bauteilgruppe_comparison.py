"""
Bauteilgruppe-level coverage comparison.

For each :Projekt, list:
  - the live BG slugs currently attached
  - the BG slugs that appear in the batch markdowns
  - the match between them (exact / fuzzy / live-only / batch-only)

User's question: would deleting old BGs lose components that are actually
connected to projects? Important context: the integration plan DOES NOT delete
any :Bauteilgruppe nodes. It only deletes vocab nodes (meth_/av_/rq_/wva_).

But: the Phase 3.2 resolver will MERGE batch rows onto existing BGs by id-match
or fuzzy match. This script measures how well the match works and what's at
risk if a fuzzy-match falls through.

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


def parse_batch_bgs() -> tuple[dict, dict]:
    """Return ({project_id: set of batch BG ids}, {bg_id: descriptor sample}).

    A batch BG id appears in either:
    - the `target_node` column when relationship=HAT_BAUTEILGRUPPE
    - the `bauteilgruppe` column of every other row
    """
    bg_by_project: dict[str, set[str]] = defaultdict(set)
    bg_descriptor: dict[str, str] = {}  # bg_id -> short descriptor from row

    for md in sorted(BATCH_DIR.glob("reuse_taxonomy_v9_connection_expansion_batch_*.md")):
        if "open_questions" in md.name:
            continue
        text = md.read_text(encoding="utf-8", errors="ignore")
        col_idx: dict[str, int] | None = None
        for line in text.splitlines():
            if not line.lstrip().startswith("|"):
                col_idx = None
                continue
            cells = [c.strip() for c in line.strip().strip("|").split("|")]
            if all(re.fullmatch(r":?-+:?", c) for c in cells if c):
                continue
            if "project_id" in cells and ("edge_id" in cells or "id" in cells):
                col_idx = {name: i for i, name in enumerate(cells)}
                if "edge_id" not in col_idx and "id" in col_idx:
                    col_idx["edge_id"] = col_idx["id"]
                continue
            if not col_idx:
                continue
            if len(cells) <= max(col_idx.values()):
                continue
            edge_id = cells[col_idx["edge_id"]]
            if not re.fullmatch(r"v10[A-Z]?-\d+", edge_id):
                continue
            try:
                pid = cells[col_idx["project_id"]]
                bg = cells[col_idx.get("bauteilgruppe", -1)] if "bauteilgruppe" in col_idx else ""
                target = cells[col_idx.get("target_node", -1)] if "target_node" in col_idx else ""
                rel = cells[col_idx.get("relationship", -1)] if "relationship" in col_idx else ""
                detail = cells[col_idx.get("detail", -1)] if "detail" in col_idx else ""
                # If it's a HAT_BAUTEILGRUPPE row, target_node is the bg id (canonical)
                # Otherwise the bauteilgruppe column holds it
                if rel == "HAT_BAUTEILGRUPPE" and target.startswith("bg_"):
                    bg_by_project[pid].add(target)
                    if target not in bg_descriptor and detail:
                        bg_descriptor[target] = detail[:60]
                if bg and bg.startswith("bg_"):
                    bg_by_project[pid].add(bg)
                    if bg not in bg_descriptor and detail:
                        bg_descriptor[bg] = detail[:60]
            except (IndexError, ValueError):
                continue
    return bg_by_project, bg_descriptor


# German<->English equivalent tokens for BG slug matching.
# Many live BG slugs use German tokens; many batch BG slugs use English. Same component.
# Each set lists tokens that should be treated as identical for matching purposes.
EQUIVALENT_TOKENS: list[set[str]] = [
    {"beton", "concrete"},
    {"holz", "wood", "timber"},
    {"stahl", "steel"},
    {"glas", "glass"},
    {"ziegel", "brick", "bricks"},
    {"naturstein", "stone"},
    {"keramik", "ceramic", "tile", "tiles", "tiled"},
    {"aluminium", "aluminum", "alu"},
    {"kunststoff", "plastic"},
    {"daemmstoff", "daemmung", "insulation"},
    {"textil", "textile", "felt", "fabric"},
    {"metall", "metal"},
    {"asphalt", "bitumen"},
    {"wand", "wall", "innenwand", "trennwand", "partition", "partitions", "trennwaende"},
    {"fassade", "facade", "cladding"},
    {"decke", "ceiling", "deck", "decks"},
    {"boden", "floor", "flooring", "floors"},
    {"dach", "roof", "rooftop"},
    {"fenster", "window", "windows", "verglasung", "glazing", "verglaste"},
    {"tuer", "door", "doors"},
    {"treppe", "stair", "stairs", "staircase", "treppen"},
    {"fundament", "foundation"},
    {"stuetze", "column", "columns"},
    {"traeger", "beam", "beams", "girder"},
    {"gelaender", "balustrade", "balustrades", "railing", "railings"},
    {"daemmung", "insulation"},
    {"ausbau", "fitout", "interior", "finishes"},
    {"tragwerk", "structure", "structural", "frame"},
    {"existing", "bestand", "retained"},
    {"reused", "wiederverwendet"},
    {"original", "originale"},
]

# Build alias map: token -> canonical (first item in its set)
TOKEN_ALIAS: dict[str, str] = {}
for grp in EQUIVALENT_TOKENS:
    canon = sorted(grp)[0]
    for t in grp:
        TOKEN_ALIAS[t] = canon


STOPWORDS = {
    "reuse", "retained", "planned", "dismantled", "candidate",
    "mehrere", "und", "the", "mit", "von", "and", "of", "to", "in", "for",
}


def normalize_token(t: str) -> str:
    return TOKEN_ALIAS.get(t, t)


def tokenize_bg_id(bg_id: str) -> tuple[str, set[str]]:
    """Return (slug_without_bg_prefix, set of normalized significant tokens)."""
    s = bg_id.lower()
    if s.startswith("bg_"):
        s = s[3:]
    parts = s.split("_")
    tokens = {normalize_token(t) for t in parts if len(t) >= 3 and t not in STOPWORDS}
    return s, tokens


def best_fuzzy_match(target_bg: str, candidates: set[str]) -> tuple[str | None, float]:
    """Best Jaccard-similarity match with a weighted bonus for shared material+bauteiltyp+project tokens."""
    _, t_tokens = tokenize_bg_id(target_bg)
    if not t_tokens:
        return None, 0.0
    best_id, best_score = None, 0.0
    for c in candidates:
        _, c_tokens = tokenize_bg_id(c)
        if not c_tokens:
            continue
        inter = t_tokens & c_tokens
        union = t_tokens | c_tokens
        score = len(inter) / len(union) if union else 0.0
        if score > best_score:
            best_id, best_score = c, score
    return best_id, best_score


def main() -> int:
    by_eid, by_label, edges = load_graph()
    batch_bgs_per_proj, batch_descriptors = parse_batch_bgs()

    # Build per-project live BG inventory
    proj_eid_to_id = {p["elementId"]: p["id"] for p in by_label["Projekt"]}
    proj_id_to_name = {p["id"]: p["name"] for p in by_label["Projekt"]}
    bg_eids = {b["elementId"]: b for b in by_label["Bauteilgruppe"]}

    live_bgs_per_proj: dict[str, dict] = defaultdict(dict)  # proj_id -> {bg_id: bg_node}
    for e in edges:
        if e["type"] != "HAT_BAUTEILGRUPPE":
            continue
        if e["start"] not in proj_eid_to_id or e["end"] not in bg_eids:
            continue
        pid = proj_eid_to_id[e["start"]]
        bg = bg_eids[e["end"]]
        live_bgs_per_proj[pid][bg["id"]] = bg

    # Now compare per project
    print("=" * 78)
    print("BAUTEILGRUPPE COMPARISON: live graph vs batch markdowns")
    print("=" * 78)
    print()
    print("Match rules:")
    print("  EXACT      = identical bg_* slug appears in both live and batches")
    print("  FUZZY      = different slug, but ≥0.5 Jaccard similarity on tokens")
    print("  LIVE-ONLY  = bg exists in live graph but not referenced by any batch row")
    print("  BATCH-ONLY = bg appears in batches but no live equivalent (NEW candidate)")
    print()

    # Per-project counts
    exact_total = fuzzy_total = live_only_total = batch_only_total = 0
    risky_projects = []
    project_rows = []

    for pid in sorted(set(proj_id_to_name) | set(batch_bgs_per_proj)):
        live = live_bgs_per_proj.get(pid, {})
        batch = batch_bgs_per_proj.get(pid, set())

        live_ids = set(live.keys())

        # Exact matches
        exact = live_ids & batch
        # For non-exact, try fuzzy match
        live_only = live_ids - exact
        batch_only = batch - exact

        fuzzy_pairs = []  # (live_id, batch_id, score)
        used_batch = set()
        # Two-pass: first take high-confidence matches (>=0.5), then permissive (>=0.35)
        for threshold in (0.5, 0.35):
            for lid in sorted(live_only - {p[0] for p in fuzzy_pairs}):
                best, score = best_fuzzy_match(lid, batch_only - used_batch)
                if best and score >= threshold:
                    fuzzy_pairs.append((lid, best, score))
                    used_batch.add(best)

        fuzzy_live = {lp[0] for lp in fuzzy_pairs}
        fuzzy_batch = {lp[1] for lp in fuzzy_pairs}
        live_unmatched = live_only - fuzzy_live
        batch_unmatched = batch_only - fuzzy_batch

        n_exact = len(exact)
        n_fuzzy = len(fuzzy_pairs)
        n_live_only = len(live_unmatched)
        n_batch_only = len(batch_unmatched)

        exact_total += n_exact
        fuzzy_total += n_fuzzy
        live_only_total += n_live_only
        batch_only_total += n_batch_only

        project_rows.append((pid, len(live_ids), len(batch),
                             n_exact, n_fuzzy, n_live_only, n_batch_only,
                             live_unmatched, batch_unmatched, fuzzy_pairs))

        if n_live_only > 0:
            risky_projects.append((pid, n_live_only, n_fuzzy, len(live_ids)))

    # Print summary table
    print(f"{'project_id':<48} {'live':>4} {'batch':>5} {'EXACT':>6} {'FUZZY':>6} {'LIVE-ONLY':>9} {'BATCH-ONLY':>10}")
    print("-" * 96)
    for (pid, n_live, n_batch, n_e, n_f, n_lo, n_bo, _, _, _) in project_rows:
        flag = " *" if n_lo > 0 else ""
        print(f"{pid:<48} {n_live:>4} {n_batch:>5} {n_e:>6} {n_f:>6} {n_lo:>9} {n_bo:>10}{flag}")

    print()
    print("=" * 78)
    print("SUMMARY TOTALS")
    print("=" * 78)
    print(f"  Total live BGs covered:       {sum(p[1] for p in project_rows)}")
    print(f"  Total batch BGs referenced:   {sum(p[2] for p in project_rows)}")
    print(f"  EXACT matches:                {exact_total}")
    print(f"  FUZZY matches (resolver auto-folds): {fuzzy_total}")
    print(f"  LIVE-ONLY (no batch evidence): {live_only_total}")
    print(f"  BATCH-ONLY (new candidates to add): {batch_only_total}")
    print()
    print(f"  Live BGs at risk if resolver fails to fuzzy-match: {fuzzy_total}")
    print(f"  Live BGs that will keep zero batch evidence:        {live_only_total}")
    print()

    # Show the risky projects with details
    print("=" * 78)
    print("PROJECTS WITH LIVE-ONLY BGs (not referenced by any batch row)")
    print("=" * 78)
    risky_projects.sort(key=lambda r: -r[1])
    for pid, n_lo, n_f, total in risky_projects[:25]:
        print(f"\n  {pid}  (live total: {total}, live-only: {n_lo}, fuzzy folded: {n_f})")
        # find the row
        row = next(r for r in project_rows if r[0] == pid)
        _, _, _, _, _, _, _, live_unmatched, batch_unmatched, fuzzy_pairs = row
        if live_unmatched:
            print(f"    LIVE-ONLY (will lack batch evidence on new axes):")
            for bg_id in sorted(live_unmatched)[:12]:
                bg = live_bgs_per_proj[pid][bg_id]
                old_func = bg["properties"].get("alte_funktion", "")[:50]
                print(f"      - {bg_id:<70} alte_funktion={old_func!r}")
            if len(live_unmatched) > 12:
                print(f"      ... + {len(live_unmatched)-12} more")

    # Show fuzzy-match examples so user can spot-check
    print()
    print("=" * 78)
    print("FUZZY MATCH SAMPLES — resolver should fold these")
    print("=" * 78)
    fuzzy_count = 0
    for row in project_rows:
        pid, _, _, _, n_f, _, _, _, _, fuzzy_pairs = row
        if n_f == 0:
            continue
        for live_id, batch_id, score in fuzzy_pairs[:2]:
            print(f"\n  Project: {pid}")
            print(f"    LIVE : {live_id}")
            print(f"    BATCH: {batch_id}    (jaccard={score:.2f})")
            descr = batch_descriptors.get(batch_id, "")
            if descr:
                print(f"    batch detail: {descr}")
            fuzzy_count += 1
            if fuzzy_count >= 12:
                break
        if fuzzy_count >= 12:
            break

    # Show batch-only samples
    print()
    print("=" * 78)
    print("BATCH-ONLY samples (new candidates batches want to add)")
    print("=" * 78)
    batch_only_count = 0
    for row in project_rows:
        pid, _, _, _, _, _, n_bo, _, batch_unmatched, _ = row
        if n_bo == 0:
            continue
        for bg_id in sorted(batch_unmatched)[:2]:
            print(f"  {pid:<48} NEW: {bg_id}")
            batch_only_count += 1
            if batch_only_count >= 12:
                break
        if batch_only_count >= 12:
            break

    return 0


if __name__ == "__main__":
    sys.exit(main())
