import csv, json, os

BASE = r"e:\recherche\_neo4j\review\2026-06-06_full_graph_verification"
WORK = os.path.join(BASE, "_agent06b_work")
LEDGER = os.path.join(BASE, "ledger")

# 2026-06 review runs (bubble-tagged)
TAGGED_RUNS = {
    "swiss_reuse_bubble_2026_06_05",
    "rotor_dc_reuse_bubble_2026_06_05",
    "germany_reuse_bubble_2026_06_05",
    "france_reuse_bubble_2026_06_05",
    "netherlands_reuse_bubble_2026_06_05",
    "cross_bubble_extension_2026_06_06",
}

# --- Load graph dumps ---
with open(os.path.join(WORK, "all_verbunden_edges.json"), encoding="utf-8") as f:
    edges = json.load(f)
with open(os.path.join(WORK, "sourced_akteur_nodes.json"), encoding="utf-8") as f:
    nodes = json.load(f)

print("graph VERBUNDEN edges:", len(edges))
print("graph sourced Akteur nodes:", len(nodes))

# --- Parse coverage from agents 01-06 ledgers ---
covered_pairs = set()      # (from_id, to_id) for VERBUNDEN rows
covered_nodes = set()      # node ids covered (any label) by agents 01-06
for n in range(1, 7):
    path = os.path.join(LEDGER, f"agent_{n:02d}.csv")
    with open(path, encoding="utf-8") as f:
        rdr = csv.DictReader(f)
        for row in rdr:
            kind = (row.get("claim_kind") or "").strip()
            rel = (row.get("rel_type_or_label") or "").strip()
            frm = (row.get("from_id") or "").strip()
            to = (row.get("to_id") or "").strip()
            eid = (row.get("element_id") or "").strip()
            if kind == "rel" and rel.upper() == "VERBUNDEN_MIT_AKTEUR":
                if frm and to:
                    covered_pairs.add((frm, to))
            if kind == "node":
                if eid:
                    covered_nodes.add(eid)

print("covered VERBUNDEN pairs (01-06):", len(covered_pairs))
print("covered node ids (01-06):", len(covered_nodes))

# --- Compute gap edges ---
# scope: review_run NOT a 2026-06 tagged run AND (from,to) not covered by 01-06
gap_edges = []
tagged_uncovered = []
for e in edges:
    rr = e.get("review_run")
    pair = (e.get("from_id"), e.get("to_id"))
    is_tagged = rr in TAGGED_RUNS
    is_covered = pair in covered_pairs
    if is_tagged:
        if not is_covered:
            tagged_uncovered.append(e)
        continue
    # untagged
    if not is_covered:
        gap_edges.append(e)

print("\nGAP EDGES (untagged, uncovered):", len(gap_edges))
print("tagged-but-uncovered (out of scope, sanity):", len(tagged_uncovered))
for e in tagged_uncovered:
    print("  TAGGED-UNCOV:", e["from_id"], "->", e["to_id"], e.get("review_run"))

# how many gap edges carry an evidence_url / source_url
with_url = [e for e in gap_edges if e.get("evidence_url") or e.get("source_url")]
print("gap edges WITH evidence/source url:", len(with_url))
for e in with_url:
    print("  URL-EDGE:", e["from_id"], "->", e["to_id"], "|", e.get("connection_kind"), "|", e.get("evidence_url") or e.get("source_url"))

# --- Compute gap nodes ---
# sourced Akteur not covered (by id) in agents 01-06
gap_nodes = []
for nd in nodes:
    if nd["id"] not in covered_nodes:
        gap_nodes.append(nd)

print("\nGAP NODES (sourced Akteur, uncovered):", len(gap_nodes))

# --- Save work-set ---
with open(os.path.join(WORK, "gap_edges.json"), "w", encoding="utf-8") as f:
    json.dump(gap_edges, f, ensure_ascii=False, indent=2)
with open(os.path.join(WORK, "gap_nodes.json"), "w", encoding="utf-8") as f:
    json.dump(gap_nodes, f, ensure_ascii=False, indent=2)

# Summary of gap edge endpoint nodes that are NOT sourced (persons/stubs)
print("\nSample gap edges (first 30):")
for e in gap_edges[:30]:
    print(" ", e["from_id"], "->", e["to_id"], "| rr=", e.get("review_run"), "| ck=", e.get("connection_kind"))
