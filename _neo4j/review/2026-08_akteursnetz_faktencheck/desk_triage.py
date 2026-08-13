"""Phase 0 of the actor-network fact-check: deterministic desk triage.

No web access, no agents. Builds the SAME drawn-node/drawn-edge set the
country figures use (by calling the actual netz pipeline functions, not a
re-derivation of them), attaches whatever evidence already exists per node
and per edge, pre-resolves directory-only ties to `unklar` at zero web cost,
and packs everything into evidence-clustered work packets for the shard
agent runs.

Committed to E:\\recherche (git) on purpose -- the sibling prune_eids.json
scoring script was lost by living only in a Claude scratchpad, and its
criterion is now unrecoverable. This script, and everything downstream of
it (merge_verdicts.py, emit_review.py), must not repeat that mistake.

Usage: python desk_triage.py   (writes worklist.json next to this file)
"""
import sys, os, json, io, collections, hashlib

NETZ_SRC = r"C:/Users/Kinosh/AppData/Local/Temp/claude/E--semio/85df4902-0865-445b-a166-a39acf157738/scratchpad"
if NETZ_SRC not in sys.path:
    sys.path.insert(0, NETZ_SRC)

from netz.sources import DEFAULT
from netz.data.prune import load_prune
from netz.model.concepts import build_network
from netz.mechanisms.connectivity import drawn_edge_nodes, FAN_THRESH
from netz.mechanisms.layout import force_layout, DEFAULT_FRAME
from netz.mechanisms.countries import is_person

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "worklist.json")

# region DirectoryNames
# 🗂 The second audit's exact bar, verbatim: "Directory-only ties (Opalis,
# bauteilnetz.de, Cirkla, Insert Marktplaats, Artisans du Patrimoine, generic
# SalvoWEB listings) are EXCLUDED -- same bar we used to remove the
# fan-boxes." Insert Marktplaats / Artisans du Patrimoine do not appear as
# named nodes anywhere in the export or the three overlays (checked
# directly) -- nothing to match, which is consistent, not a gap. The other
# four are matched by exact node display name (case-insensitive), confirmed
# against the live data rather than guessed.
DIRECTORY_NAMES = {"opalis", "salvoweb", "cirkla", "cirkla-scan", "bauteilnetz deutschland"}
# endregion DirectoryNames

# region RelationshipEvidence
# 🔍 RawGraph (netz.data.neo4j_export) intentionally does not carry
# relationship properties through -- it only keeps roles/types/land/part/peers
# as name-or-eid indices. Evidence (evidence_url, evidence_quote, confidence,
# connection_kind) lives on the ORIGINAL relationship objects, so this reads
# the export a second time, directly, to recover it and key it by the
# unordered (start, end) eid pair.
EVIDENCE_REL_TYPES = {"VERBUNDEN_MIT_AKTEUR", "BETRIEBEN_VON", "BETEILIGT_AN"}


def load_relationship_evidence(export_path):
    d = json.load(io.open(export_path, encoding="utf-8"))
    ev = {}
    for r in d["relationships"]:
        if r["type"] not in EVIDENCE_REL_TYPES:
            continue
        props = r.get("properties", {})
        key = frozenset((r["start"], r["end"]))
        # last-write-wins is fine here: BETEILIGT_AN/VERBUNDEN_MIT_AKTEUR never
        # share the same endpoint pair in this export (checked: 0 collisions).
        ev[key] = {"rel_type": r["type"], **{k: props[k] for k in
                   ("evidence_url", "evidence_quote", "evidence_confidence",
                    "connection_kind", "confidence", "basis_project_edge_id")
                   if k in props}}
    return ev
# endregion RelationshipEvidence


def load_audit2_pairs(path):
    d = json.load(io.open(path, encoding="utf-8"))
    return {frozenset((e["a"], e["b"])) for e in d["edges"]}


def is_markup_quote(q):
    """The exact defect that ruined 93 of 159 VERBUNDEN_MIT_AKTEUR quotes in
    the source data: JSON-LD / CSS / nav markup masquerading as a quote."""
    if not q:
        return False
    return any(tok in q for tok in ("{\"", "</", "@type", "px;", "font-", "@context"))


def classify_edge(a, b, net, evidence, audit2):
    """Returns (edge_class, evidence_dict, pre_verdict_or_None). A pre_verdict
    is only ever `unklar` (directory) -- never a positive degree; positive
    degrees are always agent-assigned, per the plan's D11 rule that agents
    decide degrees and only a script derives removal candidacy from them."""
    name_a, name_b = net.raw.name(a).strip().lower(), net.raw.name(b).strip().lower()
    if name_a in DIRECTORY_NAMES or name_b in DIRECTORY_NAMES:
        return "directory", {}, {"edge_degree": "unklar", "unklar_grund": "verzeichnis_only",
                                   "vorentschieden": True}

    key = frozenset((a, b))
    if key in evidence:
        e = evidence[key]
        if e.get("basis_project_edge_id"):
            return "E1_derived", e, None  # the 61 *_candidate hypotheses -- not pre-verdicted, but flagged
        q = e.get("evidence_quote", "")
        if is_markup_quote(q):
            return "E1_markup", e, {"edge_degree": "unklar", "unklar_grund": "markup_zitat",
                                      "vorentschieden": False}  # agent may still overturn with a fresh fetch
        if e.get("evidence_url"):
            return "E1", e, None
        return "E1_bare", e, None
    if key in audit2:
        return "E3_second_audit", {"source": "second_audit_report.md (prose, not machine-evidenced)"}, None
    if a.startswith("NEW:") or b.startswith("NEW:"):
        return "E4_overlay", {}, None
    return "E2_bare", {}, None


def node_kind_rank(net, e, is_proj):
    """(kind_rank, name, eid) ordering -- matches the actors+projects
    concatenation order the layout/renderer already depend on, so packet
    order is stable and reproducible run to run."""
    return (1 if is_proj else 0, net.raw.name(e).lower(), e)


def build_worklist():
    exclude = load_prune(DEFAULT.prune_path)
    net = build_network(DEFAULT, exclude=exclude)
    evidence = load_relationship_evidence(DEFAULT.export_path)
    audit2 = load_audit2_pairs(DEFAULT.audit_edges_path)

    countries = [cc for cc in net.countries
                 if cc in net.panels and (net.panels[cc].actors or net.panels[cc].projects)]

    all_nodes, all_edges = [], []
    per_country = {}
    for cc in countries:
        pan = net.panels[cc]
        keep = drawn_edge_nodes(pan)
        _, kept_edges = force_layout(pan, keep, DEFAULT_FRAME)

        nodes = []
        for e in pan.actors:
            nodes.append({"tid": net.tid.get(e, "?"), "eid": e, "cc": cc, "name": net.raw.name(e),
                          "is_project": False, "is_person": is_person(net.raw, e),
                          "is_overlay": e.startswith("NEW:"), "is_isolated": e not in keep,
                          "typ": net.raw.types.get(e), "rollen": sorted(net.raw.roles.get(e, [])),
                          "source_urls": net.raw.by[e]["properties"].get("source_urls", []),
                          "primary_source_url": net.raw.by[e]["properties"].get("primary_source_url", "")})
        for e in pan.projects:
            nodes.append({"tid": net.tid.get(e, "?"), "eid": e, "cc": cc, "name": net.raw.name(e),
                          "is_project": True, "is_person": False,
                          "is_overlay": e.startswith("NEW:"), "is_isolated": e not in keep,
                          "typ": None, "rollen": [],
                          "source_urls": net.raw.by[e]["properties"].get("source_urls", []),
                          "primary_source_url": net.raw.by[e]["properties"].get("primary_source_url", "")})
        nodes.sort(key=lambda n: node_kind_rank(net, n["eid"], n["is_project"]))

        edges = []
        for a, b in kept_edges:
            cls, ev, pre = classify_edge(a, b, net, evidence, audit2)
            edges.append({"edge_id": "%s:%s|%s" % (cc, a, b), "cc": cc,
                          "a_tid": net.tid.get(a, "?"), "b_tid": net.tid.get(b, "?"),
                          "a_eid": a, "b_eid": b, "a_name": net.raw.name(a), "b_name": net.raw.name(b),
                          "edge_class": cls, "stored_evidence": ev, "vorentscheidung": pre})

        all_nodes.extend(nodes)
        all_edges.extend(edges)
        per_country[cc] = {"nodes": len(nodes), "edges": len(edges),
                            "isolated": sum(1 for n in nodes if n["is_isolated"]),
                            "overlay": sum(1 for n in nodes if n["is_overlay"]),
                            "has_url": sum(1 for n in nodes if n["source_urls"] or n["primary_source_url"])}

    # region Packeting
    # 📦 Evidence-clustered, not alphabetical: pack a connected component
    # together so one project page can settle several verdicts in one fetch.
    # Components are derived from the DRAWN edge set only (isolated nodes have
    # no component to join and are packed separately, grouped by shared URL
    # domain so a shared-source packet still saves fetches where possible).
    def domain_of(url):
        if not url:
            return ""
        u = url.split("//", 1)[-1].split("/", 1)[0]
        return u[4:] if u.startswith("www.") else u

    EGO_SPLIT_THRESHOLD = 12
    EGO_NEIGHBOURS = 8

    def split_large_component(members, comp_edges):
        """Large components (a country's giant cluster) are too much work for
        one agent. Split into ego-packets, processing nodes highest-degree
        first: a node with an already-grouped neighbour joins that neighbour's
        group (if it has room) rather than starting a new singleton group --
        this is the fix for the first version of this function, which made a
        new hub-only group for every node whose neighbours had already been
        claimed by a bigger hub, producing dozens of 1-node packets that threw
        away a real, drawn edge for no reason. A genuinely unreachable node
        (no already-grouped neighbour, no room in any) starts its own group
        and greedily claims up to EGO_NEIGHBOURS of its own unassigned
        neighbours. Every node lands in exactly one ego-packet; an edge is
        kept in a sub-packet only when BOTH endpoints landed in it -- a
        bridging edge whose ends fall in different ego-packets is dropped
        from both (still counted in `all_edges`/`dropped_bridge_edges` for
        the report, just not handed to a single agent without the context of
        the far side)."""
        adj = collections.defaultdict(set)
        for e in comp_edges:
            adj[e["a_eid"]].add(e["b_eid"])
            adj[e["b_eid"]].add(e["a_eid"])
        cap = EGO_NEIGHBOURS + 1
        order = sorted(members, key=lambda n: -len(adj[n]))
        assigned = {}
        groups = []
        for n in order:
            if n in assigned:
                continue
            placed = False
            for nb in sorted(adj[n]):
                gi = assigned.get(nb)
                if gi is not None and len(groups[gi]) < cap:
                    groups[gi].add(n)
                    assigned[n] = gi
                    placed = True
                    break
            if not placed:
                gi = len(groups)
                groups.append({n})
                assigned[n] = gi
                for nb in sorted(adj[n]):
                    if len(groups[gi]) >= cap:
                        break
                    if nb not in assigned:
                        groups[gi].add(nb)
                        assigned[nb] = gi

        # Absorption pass: a leftover singleton whose only neighbour's group
        # was already at cap when it was processed still has a real drawn
        # edge to that neighbour. Merge it in anyway, cap or not -- a 9-10
        # node packet beats a 1-node packet that silently discards an edge.
        for gi, g in enumerate(groups):
            if len(g) != 1:
                continue
            (only,) = tuple(g)
            for nb in sorted(adj[only]):
                tgi = assigned.get(nb)
                if tgi is not None and tgi != gi:
                    groups[tgi].add(only)
                    assigned[only] = tgi
                    groups[gi] = set()
                    break
        return [g for g in groups if g]

    packets = []
    by_cc_isolated = collections.defaultdict(list)
    dropped_bridge_edges = []
    for cc in countries:
        cc_nodes = [n for n in all_nodes if n["cc"] == cc]
        cc_edges = [e for e in all_edges if e["cc"] == cc]
        eid_to_node = {n["eid"]: n for n in cc_nodes}

        par = {n["eid"]: n["eid"] for n in cc_nodes}

        def find(x):
            while par[x] != x:
                par[x] = par[par[x]]
                x = par[x]
            return x

        for e in cc_edges:
            par[find(e["a_eid"])] = find(e["b_eid"])
        comps = collections.defaultdict(list)
        for n in cc_nodes:
            comps[find(n["eid"])].append(n["eid"])

        comp_id = 0
        for root, members in comps.items():
            if len(members) < 2:
                by_cc_isolated[cc].append(eid_to_node[members[0]])
                continue
            mset = set(members)
            comp_edges = [e for e in cc_edges if e["a_eid"] in mset and e["b_eid"] in mset]
            if len(members) <= EGO_SPLIT_THRESHOLD:
                comp_id += 1
                packets.append({
                    "packet_id": "%s-c%02d" % (cc, comp_id), "cc": cc, "kind": "component",
                    "nodes": sorted((eid_to_node[m] for m in mset), key=lambda n: n["tid"]),
                    "edges": comp_edges,
                })
            else:
                groups = split_large_component(members, comp_edges)
                for group in groups:
                    comp_id += 1
                    group_edges = [e for e in comp_edges if e["a_eid"] in group and e["b_eid"] in group]
                    packets.append({
                        "packet_id": "%s-c%02d" % (cc, comp_id), "cc": cc, "kind": "ego",
                        "nodes": sorted((eid_to_node[m] for m in group), key=lambda n: n["tid"]),
                        "edges": group_edges,
                    })
                assigned_edge_ids = {e["edge_id"] for grp_pkts in
                                      [p for p in packets if p["cc"] == cc and p["kind"] == "ego"]
                                      for e in grp_pkts["edges"]}
                dropped_bridge_edges.extend(e["edge_id"] for e in comp_edges
                                             if e["edge_id"] not in assigned_edge_ids)

        iso = sorted(by_cc_isolated[cc], key=lambda n: (domain_of(n["primary_source_url"] or
                     (n["source_urls"][0] if n["source_urls"] else "")), n["name"]))
        for i in range(0, len(iso), 8):
            chunk = iso[i:i + 8]
            packets.append({"packet_id": "%s-s%02d" % (cc, i // 8 + 1), "cc": cc, "kind": "isolated",
                            "nodes": chunk, "edges": []})
    # endregion Packeting

    # region ControlSet
    # 🎯 12 blind control nodes, stratified: 4 with URL, 4 without, 2 projects,
    # 2 known-flag cases. Injected unlabelled into every shard run so
    # cross-run agreement is measurable (see plan, verification step 1).
    with_url = [n for n in all_nodes if not n["is_project"] and (n["source_urls"] or n["primary_source_url"])]
    without_url = [n for n in all_nodes if not n["is_project"] and not (n["source_urls"] or n["primary_source_url"])]
    projects = [n for n in all_nodes if n["is_project"]]
    known_flag_tids = {("DE", "M04"), ("FI", "P1")}  # Brita Marx dup; Antti Lehto mistyped
    known_flags = [n for n in all_nodes if (n["cc"], n["tid"]) in known_flag_tids]

    def stable_pick(pool, k, seed):
        pool = sorted(pool, key=lambda n: n["eid"])
        h = hashlib.sha256(seed.encode()).hexdigest()
        idx = int(h, 16)
        picked, seen = [], set()
        i = 0
        while len(picked) < k and pool:
            j = (idx + i) % len(pool)
            if j not in seen:
                seen.add(j)
                picked.append(pool[j])
            i += 1
        return picked

    control = (stable_pick(with_url, 4, "control-url") + stable_pick(without_url, 4, "control-nourl") +
               stable_pick(projects, 2, "control-proj") + known_flags[:2])
    # endregion ControlSet

    worklist = {
        "meta": {"drawn_nodes": len(all_nodes), "drawn_edges": len(all_edges),
                 "countries": countries, "per_country": per_country,
                 "isolated_total": sum(1 for n in all_nodes if n["is_isolated"]),
                 "overlay_total": sum(1 for n in all_nodes if n["is_overlay"]),
                 "directory_preresolved": sum(1 for e in all_edges if e["edge_class"] == "directory"),
                 "packets": len(packets), "control_set": [n["tid"] + ":" + n["cc"] for n in control],
                 "dropped_bridge_edges": sorted(set(dropped_bridge_edges))},
        "packets": packets,
        "control_set": control,
        "panel_index": {cc: sorted([n["tid"] + " " + n["name"] for n in all_nodes if n["cc"] == cc])
                        for cc in countries},
    }
    return worklist, net


if __name__ == "__main__":
    wl, net = build_worklist()
    io.open(OUT, "w", encoding="utf-8", newline="\n").write(
        json.dumps(wl, ensure_ascii=False, indent=1, sort_keys=False))
    m = wl["meta"]
    print("drawn: %d nodes (%d isolated, %d overlay), %d edges (%d directory-preresolved)"
          % (m["drawn_nodes"], m["isolated_total"], m["overlay_total"], m["drawn_edges"], m["directory_preresolved"]))
    print("packets: %d, control set: %d" % (m["packets"], len(m["control_set"])))
    for cc in m["countries"]:
        pc = m["per_country"][cc]
        print("  %-2s nodes=%-3d edges=%-3d isolated=%-3d overlay=%-3d has_url=%-3d"
              % (cc, pc["nodes"], pc["edges"], pc["isolated"], pc["overlay"], pc["has_url"]))
    print("wrote", OUT)
