"""
Build the Phase 3.2 Bauteilgruppe resolver CSV.

Reads:
  - 2026-06-02 full network export (live BG nodes with full property bag)
  - all 10 batch markdown files (every row that mentions a bg_*)

For each (project, live_bg) pair, emits the best match against the project's
batch BGs, scored by:

  - Exact slug ID match            -> 1.00, action=auto_confirm
  - Token-set similarity with German<->English aliasing, enriched with
    descriptive properties (alte_funktion, neue_funktion, name on live;
    detail, evidence_phrase, canonical_target on batch)
  - Material-family compatibility bonus (stahl<->metall, etc.)
  - Bauteiltyp-family compatibility bonus (gelaender<->balustrade etc.)
  - Project must match (we never cross-project)

Output CSV columns:
  project_id, live_bg_id, batch_bg_id, score, action, reason,
  live_alte_funktion, live_neue_funktion, batch_detail

Actions:
  auto_confirm       — slug exact OR rich-token score >= 0.65
  needs_review       — score 0.35-0.65 (best guess; user must confirm)
  no_batch_equiv     — live BG with no plausible batch match (score < 0.35 against any)
  new_candidate      — batch BG with no plausible live match (the other side)

Read-only on the graph. Writes only:
  bauteilgruppe_id_map.csv
  bauteilgruppe_resolver_review.md  (human-readable review queue)
"""

from __future__ import annotations
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(r"E:/recherche")
NET  = ROOT / "_neo4j/review/2026-06-02_projekt_programm_full_network_export_mit-bestand/topology.json"
BATCH_DIR = ROOT / "_neo4j/intake/inbox/research/new taxonomy edit"
PLAN_DIR  = ROOT / "_neo4j/review/2026-06-03_taxonomy_integration_plan"

OUT_CSV = PLAN_DIR / "bauteilgruppe_id_map.csv"
OUT_REVIEW = PLAN_DIR / "bauteilgruppe_resolver_review.md"


# ---------------------------------------------------------------------------
# Bilingual alias dictionary — token-level normalization for BG slug matching.
# Each set lists tokens treated as identical. The canonical form is the
# alphabetically-first member of the set.
# ---------------------------------------------------------------------------

EQUIVALENT_TOKENS: list[set[str]] = [
    # --- material families ---
    {"beton", "concrete", "betonbloecke"},
    {"stahlbeton", "reinforced"},
    {"holz", "wood", "timber", "lumber", "cedar", "fir", "pine", "spruce"},
    {"stahl", "steel", "iron"},
    {"metall", "metal", "metallic"},
    {"glas", "glass", "verglasung", "verglaste", "glazing", "glazed"},
    {"ziegel", "brick", "bricks", "mauerwerk", "masonry"},
    {"naturstein", "stone", "granite", "granit", "blaustein", "bluestone",
     "limestone", "kalkstein"},
    {"keramik", "ceramic", "ceramics", "fliese", "fliesen", "tile", "tiles", "tiled"},
    {"aluminium", "aluminum", "alu"},
    {"kupfer", "copper"},
    {"messing", "brass"},
    {"kunststoff", "plastic"},
    {"daemmstoff", "insulation"},
    {"textil", "textile", "felt", "fabric"},
    {"asphalt", "bitumen"},
    {"papier", "paper", "fibre", "fiber"},
    {"lehm", "clay", "earth"},
    {"mdf"},

    # --- component slot / Bauteiltyp ---
    {"wand", "wall", "trennwand", "trennwaende", "partition", "partitions"},
    {"innenwand", "interior", "innenraum"},
    {"aussenwand", "exterior"},
    {"fassade", "facade", "cladding"},
    {"decke", "ceiling", "deck", "decks", "soffit"},
    {"hohlkoerperdecke", "hollow", "core"},
    {"boden", "floor", "flooring", "floors", "belag", "belaege", "beläge"},
    {"dach", "roof", "rooftop", "dachterrasse"},
    {"fenster", "window", "windows", "fensterrahmen", "fensterrahmenrahmen",
     "windowframe", "fensterelemente", "fensterelement"},
    {"tuer", "door", "doors", "tuerrahmen"},
    {"treppe", "stair", "stairs", "staircase", "stairway", "treppen",
     "aussentreppe", "innentreppe", "fluchttreppe"},
    {"fundament", "foundation"},
    {"stuetze", "column", "columns"},
    {"traeger", "beam", "beams", "girder", "binder", "dachbinder", "purlin", "purlins"},
    {"gelaender", "balustrade", "balustrades", "balustraden", "balustradenbauteil",
     "railing", "railings", "handlauf", "handrail"},
    {"daemmung", "insulating"},
    {"ausbau", "fitout", "fitting", "fittings", "interior", "moebel", "furniture",
     "cupboard", "cupboards", "fixed"},
    {"tragwerk", "structure", "structural", "frame", "framework"},
    {"sanitaer", "sanitary", "wc", "toilet", "bathroom"},
    {"technik", "technical", "tech", "mep", "hvac", "elevator", "elevators",
     "aufzug", "aufzuege", "lift", "lifts"},
    {"erschliessung", "circulation", "stairwell"},

    # --- function / origin ---
    {"existing", "bestand", "bestands", "retained"},
    {"reused", "wiederverwendet"},
    {"original", "originale"},
    {"recycled", "recycling", "recyclingbeton"},
    {"reclaimed", "reclaim"},
    {"donor", "spenderbau", "donorgebaeude"},
    {"site", "baustelle"},
    {"surplus", "ueberschuss", "leftover", "offcut", "offcuts"},
    {"insulation", "daemmung"},
    {"pier", "deck"},
    {"oil", "oel", "oelplattform", "platform", "offshore"},

    # --- common descriptors ---
    {"bauteilboerse", "marketplace", "market"},
    {"haendler", "dealer"},
    {"lager", "warehouse", "storage", "stockpile"},
]

TOKEN_ALIAS: dict[str, str] = {}
for grp in EQUIVALENT_TOKENS:
    canon = sorted(grp)[0]
    for t in grp:
        TOKEN_ALIAS[t] = canon

# Material families (broader than the alias groups above) for compatibility bonus.
MATERIAL_FAMILIES: list[set[str]] = [
    {"beton", "stahlbeton", "recyclingbeton", "concrete"},
    {"holz", "wood", "timber", "cedar", "mdf", "papier", "fibre"},
    {"stahl", "metall", "metal", "aluminium", "kupfer", "messing", "steel", "iron"},
    {"glas", "glass"},
    {"ziegel", "naturstein", "keramik", "stone", "brick", "ceramic", "mauerwerk"},
    {"kunststoff", "plastic"},
    {"daemmstoff", "insulation"},
    {"textil", "textile"},
    {"asphalt", "bitumen"},
    {"lehm", "clay"},
    {"mehrere"},  # explicit "multiple" marker — soft-match across families
]

# Map token -> material family index
MATERIAL_FAMILY_OF: dict[str, int] = {}
for i, fam in enumerate(MATERIAL_FAMILIES):
    for t in fam:
        canon = TOKEN_ALIAS.get(t, t)
        MATERIAL_FAMILY_OF[canon] = i

# Bauteiltyp families
BAUTEILTYP_FAMILIES: list[set[str]] = [
    {"wand", "fassade", "innenwand", "aussenwand"},
    {"decke", "boden", "dach", "hohlkoerperdecke"},
    {"fenster", "tuer", "verglasung"},
    {"treppe", "fundament"},
    {"stuetze", "traeger", "tragwerk"},
    {"gelaender"},
    {"daemmung"},
    {"ausbau"},
    {"sanitaer"},
    {"technik", "erschliessung"},
    {"mehrere"},
]

BAUTEILTYP_FAMILY_OF: dict[str, int] = {}
for i, fam in enumerate(BAUTEILTYP_FAMILIES):
    for t in fam:
        canon = TOKEN_ALIAS.get(t, t)
        BAUTEILTYP_FAMILY_OF[canon] = i


STOPWORDS = {
    "reuse", "retained", "planned", "dismantled", "candidate",
    "und", "the", "mit", "von", "and", "of", "to", "in", "for", "fuer",
    "der", "die", "das", "des", "auf", "im", "am", "an", "als",
    "nicht", "neu", "alt", "unbekannt", "unklar",
}


def normalize_token(t: str) -> str:
    return TOKEN_ALIAS.get(t, t)


def tokenize(text: str) -> set[str]:
    """Lowercase, split on non-word, drop stopwords/short, normalize via alias map."""
    text = text.lower()
    # Map umlauts to ASCII consistent with project schema
    text = (text.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue")
                .replace("ß", "ss"))
    parts = re.split(r"[^a-z0-9]+", text)
    return {normalize_token(p) for p in parts if len(p) >= 3 and p not in STOPWORDS}


def bg_id_tokens(bg_id: str) -> set[str]:
    s = bg_id
    if s.startswith("bg_"):
        s = s[3:]
    return tokenize(s)


def material_family(tokens: set[str]) -> int | None:
    for t in tokens:
        if t in MATERIAL_FAMILY_OF:
            return MATERIAL_FAMILY_OF[t]
    return None


def bauteiltyp_family(tokens: set[str]) -> int | None:
    for t in tokens:
        if t in BAUTEILTYP_FAMILY_OF:
            return BAUTEILTYP_FAMILY_OF[t]
    return None


# ---------------------------------------------------------------------------

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
    """Return:
      bg_by_project   = {project_id: set(bg_id)}
      bg_descriptors  = {bg_id: {"detail": [...], "evidence_phrase": [...], "canonical": [...]}}

    Reads all batch markdown files, handles both column-layout variants.
    """
    bg_by_project: dict[str, set[str]] = defaultdict(set)
    bg_descriptors: dict[str, dict[str, list[str]]] = defaultdict(
        lambda: {"detail": [], "evidence_phrase": [], "canonical": [], "summary": []}
    )

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
                rel = cells[col_idx.get("relationship", -1)] if "relationship" in col_idx else ""
                target = cells[col_idx.get("target_node", -1)] if "target_node" in col_idx else ""
                bg = cells[col_idx.get("bauteilgruppe", -1)] if "bauteilgruppe" in col_idx else ""
                # detail / evidence_phrase / canonical / evidence_summary — fall back across
                # both column-layout variants
                def get(name: str) -> str:
                    i = col_idx.get(name, -1)
                    return cells[i] if 0 <= i < len(cells) else ""

                detail  = get("detail") or get("evidence_summary")
                phrase  = get("evidence_phrase") or get("evidence_summary")
                summary = get("evidence_summary")
                canon   = get("canonical_taxonomy_target") or get("canonical_target")

                def record(bg_id: str):
                    bg_by_project[pid].add(bg_id)
                    for key, val in (("detail", detail), ("evidence_phrase", phrase),
                                      ("canonical", canon), ("summary", summary)):
                        if val and val not in bg_descriptors[bg_id].setdefault(key, []):
                            bg_descriptors[bg_id][key].append(val)

                if rel == "HAT_BAUTEILGRUPPE" and target.startswith("bg_"):
                    record(target)
                if bg.startswith("bg_"):
                    record(bg)
            except (IndexError, ValueError):
                continue
    return bg_by_project, bg_descriptors


def live_bg_token_bag(bg_node: dict) -> set[str]:
    """Rich token bag for a live BG: id + name + alte_funktion + neue_funktion."""
    props = bg_node.get("properties", {})
    text = " ".join([
        bg_node.get("id", ""),
        bg_node.get("name", ""),
        props.get("alte_funktion", "") or "",
        props.get("neue_funktion", "") or "",
    ])
    return tokenize(text)


def batch_bg_token_bag(bg_id: str, descriptors: dict) -> set[str]:
    """Rich token bag for a batch BG: id + all row descriptors."""
    bag = bg_id_tokens(bg_id)
    desc = descriptors.get(bg_id, {})
    for key in ("detail", "evidence_phrase", "canonical", "summary"):
        for s in desc.get(key, [])[:3]:  # cap to avoid drowning the signal
            bag |= tokenize(s)
    return bag


def batch_descriptor_display(bg_id: str, descriptors: dict) -> str:
    """Best human-readable descriptor for a batch BG (for review queue)."""
    desc = descriptors.get(bg_id, {})
    for key in ("detail", "evidence_phrase", "summary", "canonical"):
        vals = desc.get(key) or []
        if vals:
            return vals[0][:120]
    return ""


REUSE_STATUS_PREFIXES = ("bg_reuse_", "bg_retained_", "bg_planned_", "bg_dismantled_")


def reuse_status_of(bg_id: str) -> str:
    for p in REUSE_STATUS_PREFIXES:
        if bg_id.startswith(p):
            return p
    return ""


def score_pair(live_tokens: set[str], batch_tokens: set[str],
                live_id: str = "", batch_id: str = "") -> float:
    if not live_tokens or not batch_tokens:
        return 0.0
    inter = live_tokens & batch_tokens
    union = live_tokens | batch_tokens
    jaccard = len(inter) / len(union) if union else 0.0

    bonus = 0.0
    lm = material_family(live_tokens)
    bm = material_family(batch_tokens)
    if lm is not None and bm is not None and lm == bm:
        bonus += 0.10
    elif lm is not None and bm is not None:
        bonus -= 0.05

    lb = bauteiltyp_family(live_tokens)
    bb = bauteiltyp_family(batch_tokens)
    if lb is not None and bb is not None and lb == bb:
        bonus += 0.10
    elif lb is not None and bb is not None:
        bonus -= 0.05

    # Cross-reuse-status penalty: bg_retained_* (existing/preserved) is semantically
    # very different from bg_reuse_* (newly reused), bg_planned_* (designed-in), or
    # bg_dismantled_* (removed). Penalize mismatched prefixes to prevent the greedy
    # matcher from mis-pairing structurally different BGs that happen to share
    # surface tokens (same project + same material).
    l_status = reuse_status_of(live_id)
    b_status = reuse_status_of(batch_id)
    if l_status and b_status and l_status != b_status:
        bonus -= 0.20

    return max(0.0, min(1.0, jaccard + bonus))


def assign_greedy(live: dict[str, set[str]], batch: dict[str, set[str]]) -> list[tuple]:
    """Greedy assignment: highest-score pair first; mark used; repeat."""
    pairs = []
    for lid, l_tokens in live.items():
        for bid, b_tokens in batch.items():
            pairs.append((score_pair(l_tokens, b_tokens, lid, bid), lid, bid))
    pairs.sort(reverse=True)

    used_live, used_batch = set(), set()
    assignments = []
    for score, lid, bid in pairs:
        if score <= 0:
            break
        if lid in used_live or bid in used_batch:
            continue
        used_live.add(lid)
        used_batch.add(bid)
        assignments.append((lid, bid, score))
    return assignments


# ---------------------------------------------------------------------------

def main() -> int:
    by_eid, by_label, edges = load_graph()
    batch_bgs_per_proj, batch_descriptors = parse_batch_bgs()

    proj_eid_to_id = {p["elementId"]: p["id"] for p in by_label["Projekt"]}
    proj_id_to_name = {p["id"]: p["name"] for p in by_label["Projekt"]}
    bg_eid_to_node = {b["elementId"]: b for b in by_label["Bauteilgruppe"]}

    live_bgs_per_proj: dict[str, dict[str, dict]] = defaultdict(dict)
    for e in edges:
        if e["type"] != "HAT_BAUTEILGRUPPE":
            continue
        if e["start"] not in proj_eid_to_id or e["end"] not in bg_eid_to_node:
            continue
        pid = proj_eid_to_id[e["start"]]
        bg = bg_eid_to_node[e["end"]]
        live_bgs_per_proj[pid][bg["id"]] = bg

    rows = []          # CSV rows
    review_blocks = [] # markdown review queue
    stats = Counter()

    for pid in sorted(set(proj_id_to_name) | set(batch_bgs_per_proj)):
        live_nodes = live_bgs_per_proj.get(pid, {})
        batch_ids = batch_bgs_per_proj.get(pid, set())
        if not live_nodes and not batch_ids:
            continue

        # 1) Exact id matches first
        exact = set(live_nodes.keys()) & batch_ids
        for lid in sorted(exact):
            rows.append([pid, lid, lid, 1.00, "auto_confirm", "exact_slug_match",
                         (live_nodes[lid]["properties"].get("alte_funktion") or "")[:80],
                         (live_nodes[lid]["properties"].get("neue_funktion") or "")[:80],
                         ""])
            stats["auto_confirm_exact"] += 1

        # 2) For the remainder, rich-token assignment
        live_remaining = {lid: live_bg_token_bag(node) for lid, node in live_nodes.items() if lid not in exact}
        batch_remaining = {bid: batch_bg_token_bag(bid, batch_descriptors) for bid in batch_ids - exact}
        assignments = assign_greedy(live_remaining, batch_remaining)

        proj_review = []
        # Sort assignments by score so the highest-confidence comes first
        assignments_sorted = sorted(assignments, key=lambda a: -a[2])
        for lid, bid, score in assignments_sorted:
            live_node = live_nodes[lid]
            af = (live_node["properties"].get("alte_funktion") or "")[:80]
            nf = (live_node["properties"].get("neue_funktion") or "")[:80]
            detail = batch_descriptor_display(bid, batch_descriptors)

            if score >= 0.65:
                action = "auto_confirm"
                reason = f"high_token_match_{score:.2f}"
                stats["auto_confirm_fuzzy"] += 1
                rows.append([pid, lid, bid, round(score, 3), action, reason, af, nf, detail])
            elif score >= 0.35:
                action = "needs_review"
                reason = f"medium_token_match_{score:.2f}"
                stats["needs_review"] += 1
                rows.append([pid, lid, bid, round(score, 3), action, reason, af, nf, detail])
                proj_review.append(("needs_review", lid, bid, score, af, nf, detail))
            # weak (<0.35) assignments are NOT auto-paired in the CSV; both sides
            # become unmatched and get a "weak-guess" suggestion in the review block below.

        # 3) Live unmatched -> no_batch_equiv, with a weak-guess suggestion if any batch BG is also unmatched
        matched_live = exact | {a[0] for a in assignments if a[2] >= 0.35}
        matched_batch = exact | {a[1] for a in assignments if a[2] >= 0.35}
        unmatched_live = sorted(set(live_nodes.keys()) - matched_live)
        unmatched_batch = sorted(batch_ids - matched_batch)

        # Build weak-guess pairs: for each unmatched live, find best unmatched batch (any score)
        used_batch_weak: set[str] = set()
        weak_suggestions: dict[str, tuple[str, float]] = {}
        for lid in unmatched_live:
            l_tokens = live_bg_token_bag(live_nodes[lid])
            best, best_score = None, -1.0
            for bid in unmatched_batch:
                if bid in used_batch_weak:
                    continue
                b_tokens = batch_bg_token_bag(bid, batch_descriptors)
                s = score_pair(l_tokens, b_tokens, lid, bid)
                if s > best_score:
                    best, best_score = bid, s
            # Only keep weak guesses with at least some signal; below 0.10 there is
            # nothing useful and the suggestion becomes pure noise.
            if best is not None and best_score >= 0.10:
                weak_suggestions[lid] = (best, best_score)
                used_batch_weak.add(best)

        for lid in unmatched_live:
            af = (live_nodes[lid]["properties"].get("alte_funktion") or "")[:80]
            nf = (live_nodes[lid]["properties"].get("neue_funktion") or "")[:80]
            suggested_bid, suggested_score = weak_suggestions.get(lid, (None, 0.0))
            detail = batch_descriptor_display(suggested_bid, batch_descriptors) if suggested_bid else ""
            if suggested_bid:
                # Weak-guess row: lives goes into CSV as needs_review with low-confidence suggestion
                rows.append([pid, lid, suggested_bid, round(suggested_score, 3),
                             "needs_review", f"weak_guess_{suggested_score:.2f}",
                             af, nf, detail])
                stats["needs_review"] += 1
                proj_review.append(("weak_guess", lid, suggested_bid, suggested_score,
                                     af, nf, detail))
            else:
                rows.append([pid, lid, "", 0.0, "no_batch_equiv",
                             "no_plausible_batch_match", af, nf, ""])
                stats["no_batch_equiv"] += 1
                proj_review.append(("no_batch_equiv", lid, None, 0.0, af, nf, ""))

        # 4) Batch unmatched that weren't picked up as weak guess -> new_candidate
        unmatched_batch_after_weak = set(unmatched_batch) - used_batch_weak
        for bid in sorted(unmatched_batch_after_weak):
            detail = batch_descriptor_display(bid, batch_descriptors)
            rows.append([pid, "", bid, 0.0, "new_candidate",
                         "batch_introduces_new_bg", "", "", detail])
            stats["new_candidate"] += 1
            proj_review.append(("new_candidate", None, bid, 0.0, "", "", detail))

        if proj_review:
            review_blocks.append((pid, proj_review))

    # ---------------- write CSV ----------------
    OUT_CSV.write_text("", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["project_id", "live_bg_id", "batch_bg_id", "score", "action",
                    "reason", "live_alte_funktion", "live_neue_funktion", "batch_detail"])
        w.writerows(rows)

    # ---------------- write markdown review queue ----------------
    md_lines = [
        "# Bauteilgruppe Resolver — manual review queue",
        "",
        f"Generated {len(rows)} entries.",
        "",
        f"- **auto_confirm** (exact slug): {stats['auto_confirm_exact']}",
        f"- **auto_confirm** (high token match >=0.65): {stats['auto_confirm_fuzzy']}",
        f"- **needs_review** (0.35-0.65): {stats['needs_review']}",
        f"- **no_batch_equiv** (live BG unmatched): {stats['no_batch_equiv']}",
        f"- **new_candidate** (batch BG unmatched): {stats['new_candidate']}",
        "",
        "Decision keys (edit the CSV directly):",
        "- `auto_confirm` -> resolver merges batch rows onto live BG",
        "- `confirm`      -> human approves the proposed match",
        "- `reject`       -> human says these aren't the same BG; mark live as no_batch_equiv and batch as new_candidate",
        "- `merge_to:bg_X` -> assign to a different live or batch BG than the suggested one",
        "",
        "## Per-project review",
        "",
    ]
    for pid, proj_review in review_blocks:
        md_lines.append(f"### {pid}")
        md_lines.append("")
        md_lines.append("| kind | live | batch | score | live alte_funktion | live neue_funktion | batch detail |")
        md_lines.append("|---|---|---|---:|---|---|---|")
        # Sort: needs_review first (highest confidence pairs), then weak_guess, then no_batch_equiv, then new_candidate
        sort_order = {"needs_review": 0, "weak_guess": 1, "no_batch_equiv": 2, "new_candidate": 3}
        proj_review.sort(key=lambda r: (sort_order.get(r[0], 9), -(r[3] or 0)))
        for kind, lid, bid, score, af, nf, detail in proj_review:
            l = lid or "_(none)_"
            b = bid or "_(none)_"
            s = f"{score:.2f}" if score else "-"
            md_lines.append(f"| **{kind}** | `{l}` | `{b}` | {s} | {af} | {nf} | {detail} |")
        md_lines.append("")
    OUT_REVIEW.write_text("\n".join(md_lines), encoding="utf-8")

    # ---------------- console summary ----------------
    print("Resolver build complete.")
    print(f"  -> {OUT_CSV.name}")
    print(f"  -> {OUT_REVIEW.name}")
    print()
    print("Stats:")
    for k, v in stats.most_common():
        print(f"  {k:<28} {v:>4}")
    total_live = sum(len(by) for by in live_bgs_per_proj.values())
    total_batch = sum(len(bs) for bs in batch_bgs_per_proj.values())
    auto_confirmed = stats["auto_confirm_exact"] + stats["auto_confirm_fuzzy"]
    print()
    print(f"  Live BGs total          : {total_live}")
    print(f"  Batch BGs total         : {total_batch}")
    print(f"  Auto-confirmed coverage : {auto_confirmed}/{total_live} "
          f"({100*auto_confirmed/total_live:.1f}%)")
    print(f"  Needs human review      : {stats['needs_review']}")
    print(f"  Live BG unmatched (evidence-cold candidates): {stats['no_batch_equiv']}")
    print(f"  Batch BG unmatched (new candidates to add)  : {stats['new_candidate']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
