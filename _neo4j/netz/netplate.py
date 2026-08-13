"""
Mechanism: country force-graph plates.

Stages (each pure, each checkable):
  1 MODEL    JSON -> actors, projects, edges
  2 RESOLVE  country per actor (Rule A only, validated 100%)
  3 PARTITION per-country subgraph, actors+projects
  4 NUMBER   per-country ids == table row order  (bijection invariant)
  5 LAYOUT   per component: spring -> overlap relaxation; isolates gridded; shelf-pack
  6 CHECK    invariants: no overlap, in-bounds, edge/node conservation
  7 EMIT     TikZ (only if CHECK passes)

`dry_run()` runs 1-6 and reports geometry. No TeX is written.
"""
import collections, io, re, math
import networkx as nx
import numpy as np
from net_lib import Net, TYPE_LETTER

# ---------- geometry constants (mm) ----------
PANEL_W = 181.0
PANEL_H = 232.0
NODE_R = 1.75       # circle radius (uniform)
NODE_H = 2 * NODE_R
GAP = 0.9           # min clear space between circles
RING = 6.2          # base radial ring step (uniform edge length)
RING_DECAY = 0.82   # outer rings step closer, so deep trees stay compact
ISO_GAP = 1.2

# Only DACH + established reuse-pioneer countries are drawn.
WHITELIST = {"CH", "DE", "AT", "BE", "NL", "FR", "GB", "DK", "SE", "NO", "FI"}

CC_TEXT = {"UK": "GB", "United Kingdom": "GB", "England": "GB", "London": "GB",
           "Schweiz": "CH", "Switzerland": "CH", "Suisse": "CH",
           "Deutschland": "DE", "Germany": "DE", "Belgium": "BE", "Belgique": "BE",
           "België": "BE", "Belgien": "BE", "Netherlands": "NL", "Nederland": "NL",
           "Niederlande": "NL", "France": "FR", "Frankreich": "FR", "Austria": "AT",
           "Österreich": "AT", "Denmark": "DK", "Danmark": "DK", "Dänemark": "DK",
           "Finland": "FI", "Finnland": "FI", "Norway": "NO", "Norwegen": "NO",
           "USA": "US", "United States": "US", "Japan": "JP", "Luxembourg": "LU",
           "Italia": "IT", "Italy": "IT", "Spain": "ES"}
CC_CITY = {"Zürich": "CH", "Basel": "CH", "Winterthur": "CH", "Genève": "CH", "Lausanne": "CH",
           "Bern": "CH", "Berlin": "DE", "Hannover": "DE", "Bremen": "DE", "Kassel": "DE",
           "München": "DE", "Brussel": "BE", "Bruxelles": "BE", "Dilbeek": "BE",
           "Anderlecht": "BE", "Gent": "BE", "Amsterdam": "NL", "Utrecht": "NL",
           "Rotterdam": "NL", "Leiden": "NL", "Eindhoven": "NL", "Maassluis": "NL",
           "Oegstgeest": "NL", "Colombelles": "FR", "Stains": "FR", "Paris": "FR",
           "Wien": "AT", "Copenhagen": "DK", "København": "DK", "Tampere": "FI",
           "Kamikatsu": "JP"}


def cc_from_text(t):
    if not t:
        return None
    for k, v in CC_TEXT.items():
        if re.search(r"\b" + re.escape(k) + r"\b", t, re.I):
            return v
    for k, v in CC_CITY.items():
        if re.search(re.escape(k), t, re.I):
            return v
    return None


# ---------------- stage 1-4 ----------------
class Model:
    def __init__(self, overlay=None, extra_peers=None, exclude=None):
        n = Net(overlay=overlay, extra_peers=extra_peers)
        self.n = n
        exclude = exclude or set()
        self.aset = {a["eid"] for a in n.actors if a["eid"] not in exclude}
        self.proj_cc = {e: cc_from_text(n.by[e]["properties"].get("adresse", "")) for e in n.projects}
        for e, cc in getattr(n, "new_proj_cc", {}).items():   # harvested new projects
            self.proj_cc[e] = cc
        # stage 2: Rule A only (new overlay nodes already carry a researched country in n.land)
        self.cc = {e: n.iso(e) for e in self.aset if e in n.land}
        self.inferred = set()
        for a in n.actors:
            e = a["eid"]
            if e not in self.aset or e in self.cc:
                continue
            cs = {self.proj_cc[x] for x in n.part[e] if self.proj_cc.get(x)}
            if len(cs) == 1:
                self.cc[e] = next(iter(cs))
                self.inferred.add(e)
        self.unplaced = sorted(self.aset - set(self.cc))
        # stage 3: partition — only DACH + reuse-pioneer countries
        # secondary key `c` breaks ties deterministically -- the generator
        # iterates a set union (hash-random per process), so without a
        # tiebreak, equal-count countries swap order in a hash-random way.
        self.countries = sorted((c for c in ({c for c in self.cc.values()}
                                             | {c for c in self.proj_cc.values() if c})
                                 if c in WHITELIST),
                                key=lambda c: (-sum(1 for v in self.cc.values() if v == c), c))
        # Persons are excluded from the DRAWN graph (they stay in the tables).
        self.is_person = lambda e: n.types.get(e) == "Person"
        self.panels = {}
        drawn = set()
        for c in self.countries:
            A = sorted(e for e, v in self.cc.items() if v == c and not self.is_person(e))
            P = sorted(e for e, v in self.proj_cc.items() if v == c)
            inside = set(A) | set(P)
            E = []
            for e in A:
                for q in sorted(n.peers[e]):
                    if q in inside and q in self.aset:
                        k = (min(e, q), max(e, q))
                        if k not in drawn:
                            drawn.add(k); E.append(k)
                for x in sorted(n.part[e]):
                    if x in inside:
                        k = (e, x)
                        if k not in drawn:
                            drawn.add(k); E.append(k)
            self.panels[c] = {"A": A, "P": P, "E": E}
        self.drawn = drawn
        # cross-border / out-of-panel edges (listed once, never drawn)
        self.cross = []
        for e in self.aset:
            for q in self.n.peers[e]:
                if q in self.aset:
                    k = (min(e, q), max(e, q))
                    if k not in drawn:
                        self.cross.append(("peer",) + k)
            for x in self.n.part[e]:
                if x in self.proj_cc and (e, x) not in drawn:
                    self.cross.append(("proj", e, x))
        self.cross = sorted(set(self.cross))
        # stage 4: numbering (row order == id); placeholder order = alphabetical
        # self.num: plain per-country running int -- kept ONLY for internal layout
        # tie-breaking (deterministic sort keys), never shown to the reader.
        self.num = {}
        for c, pan in self.panels.items():
            for i, e in enumerate(sorted(pan["A"], key=lambda x: n.name(x).lower()), start=1):
                self.num[e] = i
            for i, e in enumerate(sorted(pan["P"], key=lambda x: n.name(x).lower()), start=1):
                self.num[e] = i
        # self.tid: the ONE id shown everywhere (graph circles + tables) --
        # single-letter Typ code + per-country per-type running number, so it
        # fits the 3.5mm node circles and doubles as the table's sort key.
        # Projects keep "P%d"; a person (excluded from the drawn graph) still
        # gets an id here so the table can reference it consistently.
        self.tid = {}
        for c, pan in self.panels.items():
            by_typ = collections.defaultdict(list)
            for e in pan["A"]:
                by_typ[n.types.get(e, "Unbekannt")].append(e)
            for typ, es in by_typ.items():
                letter = TYPE_LETTER.get(typ, "X")
                for i, e in enumerate(sorted(es, key=lambda x: n.name(x).lower()), start=1):
                    self.tid[e] = "%s%02d" % (letter, i)
            for i, e in enumerate(sorted(pan["P"], key=lambda x: n.name(x).lower()), start=1):
                self.tid[e] = "P%d" % i
        # persons: not in any panel["A"] (excluded from the drawn graph), but
        # still need a stable per-country id for the table.
        by_cc_person = collections.defaultdict(list)
        for a in n.actors:
            e = a["eid"]
            if self.is_person(e) and self.cc.get(e) in self.panels:
                by_cc_person[self.cc[e]].append(e)
        letter = TYPE_LETTER["Person"]
        for c, es in by_cc_person.items():
            for i, e in enumerate(sorted(es, key=lambda x: n.name(x).lower()), start=1):
                self.tid[e] = "%s%02d" % (letter, i)

    def label(self, e):
        return self.tid[e]

    def box(self, e):
        return (2 * NODE_R, 2 * NODE_R)


# ---------------- stage 5: layout ----------------
def _relax(P, W, H, iters=600):
    keys = list(P)
    for _ in range(iters):
        moved = 0
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                a, b = keys[i], keys[j]
                dx = P[b][0] - P[a][0]; dy = P[b][1] - P[a][1]
                mx = (W[a] + W[b]) / 2 + GAP; my = (H[a] + H[b]) / 2 + GAP
                ox = mx - abs(dx); oy = my - abs(dy)
                if ox > 0 and oy > 0:
                    moved += 1
                    if ox / mx <= oy / my:
                        s = ox / 2 + 0.02
                        if dx >= 0: P[a][0] -= s; P[b][0] += s
                        else: P[a][0] += s; P[b][0] -= s
                    else:
                        s = oy / 2 + 0.02
                        if dy >= 0: P[a][1] -= s; P[b][1] += s
                        else: P[a][1] += s; P[b][1] -= s
        if moved == 0:
            break
    return P


def _radial(nodes, edges, model):
    """Pure radial-tree positions, centred, no de-overlap wrapper."""
    if len(nodes) == 1:
        return {nodes[0]: (0.0, 0.0)}
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(edges)
    root = max(nodes, key=lambda v: (g.degree(v), -model.num[v]))
    parent = {root: None}; depth = {root: 0}; order = [root]
    children = collections.defaultdict(list)
    dq = [root]
    while dq:
        u = dq.pop(0)
        for w in sorted(g.neighbors(u), key=lambda z: (-g.degree(z), model.num[z])):
            if w not in parent:
                parent[w] = u; depth[w] = depth[u] + 1
                children[u].append(w); order.append(w); dq.append(w)
    weight = {}
    for v in reversed(order):
        weight[v] = sum(weight[c] for c in children[v]) if children[v] else 1
    center = {}
    def assign(v, a0, a1):
        center[v] = (a0 + a1) / 2.0
        cs = children[v]
        if not cs:
            return
        tw = sum(weight[c] for c in cs)
        a = a0
        # pad each side so leaves don't sit exactly on the wedge boundary
        for c in cs:
            span = (a1 - a0) * weight[c] / tw
            assign(c, a, a + span); a += span
    # a 2-leaf star drawn full-circle is a straight line through the hub; fan it
    # into a V instead. 3+ leaves form a proper star (not a line) so keep the ring.
    if len(children[root]) == 2:
        a0 = math.pi / 2 - 0.62
        assign(root, a0, a0 + 1.24)
    else:
        assign(root, 0.0, 2 * math.pi)
    # choose ring step so same-depth circles never touch
    diam = 2 * NODE_R + GAP
    bydepth = collections.defaultdict(list)
    for v in nodes:
        bydepth[depth[v]].append(v)
    ring = RING
    maxd = max(depth.values())
    for d, vs in bydepth.items():
        if d == 0 or len(vs) < 2:
            continue
        angs = sorted(center[v] for v in vs)
        gaps = [angs[i + 1] - angs[i] for i in range(len(angs) - 1)] + [2 * math.pi - angs[-1] + angs[0]]
        mg = min(x for x in gaps if x > 1e-6)
        # radius at depth d from decaying ring steps: R_d = ring * sum_{i<d} decay^i
        rd = sum(RING_DECAY ** i for i in range(d))
        ring = max(ring, (diam / mg) / max(rd, 1e-6))
    radius = {d: ring * sum(RING_DECAY ** i for i in range(d)) for d in range(maxd + 1)}
    pos = {}
    for v in nodes:
        r = radius[depth[v]]
        pos[v] = (r * math.cos(center[v]), r * math.sin(center[v]))
    return pos


def _compact(P, iters=16, pull=0.12):
    """Pull every node toward the component centroid, de-overlapping after each
    step. Converges to a tight, round blob so degree-1 satellites hug their hub
    instead of radiating — no topology change, circles never touch."""
    keys = list(P)
    if len(keys) < 3:
        return P
    Q = {v: [P[v][0], P[v][1]] for v in keys}
    W = {v: 2 * NODE_R for v in keys}
    for _ in range(iters):
        cx = sum(Q[v][0] for v in keys) / len(keys)
        cy = sum(Q[v][1] for v in keys) / len(keys)
        for v in keys:
            Q[v][0] += (cx - Q[v][0]) * pull
            Q[v][1] += (cy - Q[v][1]) * pull
        Q = _relax(Q, W, W, iters=70)
    return {v: tuple(Q[v]) for v in keys}


def _bbox_r(pos):
    xs = [p[0] for p in pos.values()]; ys = [p[1] for p in pos.values()]
    cx = (max(xs) + min(xs)) / 2; cy = (max(ys) + min(ys)) / 2
    r = max(math.hypot(p[0] - cx, p[1] - cy) for p in pos.values()) + NODE_R
    return cx, cy, r


def _uniform_edge(nodes, edges, model, seed=11):
    """Force model with UNIFORM target edge length + LOCAL repulsion only.
    Local (not global) repulsion lets bridge/chain edges fold back toward the
    cluster instead of stretching into long lines; every edge relaxes to L0."""
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(edges)
    p0 = nx.spring_layout(g, seed=seed, iterations=250, k=1.1 / math.sqrt(len(nodes)))
    lens = [math.hypot(p0[a][0] - p0[b][0], p0[a][1] - p0[b][1]) for a, b in edges] or [1.0]
    mean = sum(lens) / len(lens) or 1e-6
    L0 = RING
    P = {v: [p0[v][0] * L0 / mean, p0[v][1] * L0 / mean] for v in nodes}
    keys = list(nodes)
    R = 1.5 * L0
    GRAV = 0.014            # weak pull to centroid -> chains curl into the cluster
    for it in range(420):
        disp = {v: [0.0, 0.0] for v in nodes}
        cx = sum(P[v][0] for v in nodes) / len(nodes)
        cy = sum(P[v][1] for v in nodes) / len(nodes)
        for v in nodes:
            disp[v][0] += GRAV * (cx - P[v][0]); disp[v][1] += GRAV * (cy - P[v][1])
        for a, b in edges:
            dx = P[b][0] - P[a][0]; dy = P[b][1] - P[a][1]
            d = math.hypot(dx, dy) or 1e-6
            f = 0.5 * (d - L0) / d                     # >0 too long -> attract
            disp[a][0] += f * dx; disp[a][1] += f * dy
            disp[b][0] -= f * dx; disp[b][1] -= f * dy
        for i in range(len(keys)):
            ax, ay = P[keys[i]]
            for j in range(i + 1, len(keys)):
                bx, by = P[keys[j]]
                dx = bx - ax; dy = by - ay
                d2 = dx * dx + dy * dy
                if d2 < R * R:
                    d = math.sqrt(d2) or 1e-6
                    f = 0.11 * (R - d) / d              # local push apart
                    disp[keys[i]][0] -= f * dx; disp[keys[i]][1] -= f * dy
                    disp[keys[j]][0] += f * dx; disp[keys[j]][1] += f * dy
        damp = 0.12 if it < 60 else 0.07
        for v in nodes:
            mx = max(-1.8, min(1.8, disp[v][0] * damp))
            my = max(-1.8, min(1.8, disp[v][1] * damp))
            P[v][0] += mx; P[v][1] += my
    return P


def _rose(nodes, edges, model, seed=11):
    """'Clusters within clusters' force layout. Every leaf (degree-1 satellite) is
    sprung SHORT and hard to its hub, so it hugs the hub as a tight rose petal;
    hub<->hub edges rest LONGER, so the roses sit apart and only inter-hub lines
    run long. Local repulsion pushes each hub's petals outward, away from the core."""
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(edges)
    if len(nodes) == 1:
        return {nodes[0]: [0.0, 0.0]}
    deg = dict(g.degree())
    L_leaf = 2 * NODE_R + GAP + 0.7        # short petal spoke (~5.0 mm)
    L_core = RING * 1.08                   # hubs sit close -> tight bouquet (~6.7 mm)

    def rest(a, b):
        return L_leaf if (deg[a] == 1 or deg[b] == 1) else L_core

    def kcoef(a, b):                       # petals bind harder than hub links
        return 0.85 if (deg[a] == 1 or deg[b] == 1) else 0.50

    p0 = nx.spring_layout(g, seed=seed, iterations=220, k=1.0 / math.sqrt(len(nodes)))
    lens = [math.hypot(p0[a][0] - p0[b][0], p0[a][1] - p0[b][1]) for a, b in edges] or [1.0]
    mean = sum(lens) / len(lens) or 1e-6
    P = {v: [p0[v][0] * L_core / mean, p0[v][1] * L_core / mean] for v in nodes}
    keys = list(nodes)
    R = L_core * 1.05
    # denser cores need stronger pull to stay compact; scale gravity with hub count
    nhub = sum(1 for v in nodes if deg[v] > 1)
    GRAV = min(0.030, 0.014 + 0.0009 * nhub)
    for it in range(460):
        disp = {v: [0.0, 0.0] for v in nodes}
        cx = sum(P[v][0] for v in nodes) / len(nodes)
        cy = sum(P[v][1] for v in nodes) / len(nodes)
        for v in nodes:
            if deg[v] != 1:                # gravity acts on hubs only; petals follow hub
                disp[v][0] += GRAV * (cx - P[v][0]); disp[v][1] += GRAV * (cy - P[v][1])
        for a, b in edges:
            dx = P[b][0] - P[a][0]; dy = P[b][1] - P[a][1]
            d = math.hypot(dx, dy) or 1e-6
            L0 = rest(a, b); f = kcoef(a, b) * (d - L0) / d
            disp[a][0] += f * dx; disp[a][1] += f * dy
            disp[b][0] -= f * dx; disp[b][1] -= f * dy
        for i in range(len(keys)):
            ax, ay = P[keys[i]]
            for j in range(i + 1, len(keys)):
                bx, by = P[keys[j]]
                dx = bx - ax; dy = by - ay
                d2 = dx * dx + dy * dy
                if d2 < R * R:
                    d = math.sqrt(d2) or 1e-6
                    f = 0.10 * (R - d) / d
                    disp[keys[i]][0] -= f * dx; disp[keys[i]][1] -= f * dy
                    disp[keys[j]][0] += f * dx; disp[keys[j]][1] += f * dy
        damp = 0.11 if it < 70 else 0.06
        for v in nodes:
            P[v][0] += max(-1.8, min(1.8, disp[v][0] * damp))
            P[v][1] += max(-1.8, min(1.8, disp[v][1] * damp))
    return P


def _star_disc(nodes, hub, model):
    """Pack a big hub's leaves into concentric rings (a compact disc) rather than
    one oversized single ring. Alternate rings are angularly staggered so most
    hub->leaf edges pass through the gaps of the inner ring."""
    leaves = sorted((v for v in nodes if v != hub), key=lambda v: model.num[v])
    diam = 2 * NODE_R + GAP
    pos = {hub: (0.0, 0.0)}
    r = diam * 1.15
    idx = 0; ring = 0
    while idx < len(leaves):
        cap = max(1, int(2 * math.pi * r / diam))
        k = min(cap, len(leaves) - idx)
        off = (math.pi / k) if (ring % 2) else 0.0
        for j in range(k):
            a = 2 * math.pi * j / k + off
            pos[leaves[idx]] = (r * math.cos(a), r * math.sin(a)); idx += 1
        r += diam * 0.98; ring += 1
    return pos


FAN_THRESH = 8   # a hub with more degree-1 leaves is drawn as a boxed grid, not spokes


def layout_component(nodes, edges, model, seed=11):
    """Returns (pos, fans). A hub with many degree-1 leaves ('fan') is pulled out
    of the node-link layout and its leaves are placed in a compact grid inside a
    containment box (drawn by the emitter) — no radiating spokes. The remaining
    core is laid out with radial (pure star) or uniform-edge force (everything
    else) so edges stay short and clusters stay tight."""
    if len(nodes) == 1:
        return {nodes[0]: (0.0, 0.0)}, []
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(edges)
    deg = dict(g.degree())
    # detect fans
    fans = []; fan_leaf = set()
    for hub in nodes:
        leaves = [w for w in g.neighbors(hub) if deg[w] == 1]
        if len(leaves) > FAN_THRESH:
            fans.append([hub, sorted(leaves, key=lambda v: model.num[v])])
            fan_leaf.update(leaves)
    core = [v for v in nodes if v not in fan_leaf]
    cset = set(core)
    core_edges = [e for e in edges if e[0] in cset and e[1] in cset]
    W = {v: 2 * NODE_R for v in nodes}; H = W

    # ---- core layout ----
    if len(core) == 1:
        pos = {core[0]: [0.0, 0.0]}
    else:
        cg = nx.Graph(); cg.add_nodes_from(core); cg.add_edges_from(core_edges)
        cdeg = dict(cg.degree()); cmax = max(cdeg.values())
        if cmax == len(core) - 1:
            pos = {v: list(p) for v, p in _radial(core, core_edges, model).items()}
        else:
            pos = _uniform_edge(core, core_edges, model, seed=seed)
        pos = _relax(pos, {v: W[v] for v in core}, {v: H[v] for v in core}, iters=140)
        pos = _edge_repair(pos, W, H, core_edges, core, rounds=8)

    # ---- attach each fan as a grid box, pushed away from the core centroid ----
    diam = 2 * NODE_R + GAP
    fan_boxes = []
    cx = sum(pos[v][0] for v in core) / len(core)
    cy = sum(pos[v][1] for v in core) / len(core)
    for hub, leaves in fans:
        hx, hy = pos[hub]
        nlv = len(leaves)
        cols = max(1, int(round(math.sqrt(nlv * 1.5))))
        rows = (nlv + cols - 1) // cols
        gw = cols * diam; gh = rows * diam
        dx, dy = hx - cx, hy - cy
        dlen = math.hypot(dx, dy) or 1.0
        ux, uy = dx / dlen, dy / dlen
        if len(core) == 1: ux, uy = 0.0, 1.0        # lone hub: grid straight below
        gx = hx + ux * (gh / 2 + diam * 1.4) - gw / 2 + diam / 2
        gy = hy + uy * (gh / 2 + diam * 1.4) - gh / 2 + diam / 2
        for i, l in enumerate(leaves):
            r_, c_ = divmod(i, cols)
            pos[l] = [gx + c_ * diam, gy + r_ * diam]
        bx0 = gx - diam / 2 - 0.8; by0 = gy - diam / 2 - 0.8
        bx1 = gx + (cols - 1) * diam + diam / 2 + 0.8
        by1 = gy + (rows - 1) * diam + diam / 2 + 0.8
        fan_boxes.append(dict(hub=hub, leaves=set(leaves), box=[bx0, by0, bx1, by1]))

    # keep fan GRIDS rigid; push whole fans off the core so nothing overlaps them
    leafset = set().union(*[f["leaves"] for f in fan_boxes]) if fan_boxes else set()
    for f in fan_boxes:
        for _ in range(200):
            b = f["box"]; hit = False
            for v in core:
                vx, vy = pos[v]
                if b[0] - NODE_R < vx < b[2] + NODE_R and b[1] - NODE_R < vy < b[3] + NODE_R:
                    hit = True; break
            if not hit:
                break
            # shift fan away from core centroid
            fcx = (b[0] + b[2]) / 2; fcy = (b[1] + b[3]) / 2
            dx, dy = fcx - cx, fcy - cy
            dl = math.hypot(dx, dy) or 1.0
            sx, sy = dx / dl * 2.0, dy / dl * 2.0
            for l in f["leaves"]:
                pos[l][0] += sx; pos[l][1] += sy
            f["box"] = [b[0] + sx, b[1] + sy, b[2] + sx, b[3] + sy]

    xs = [p[0] for p in pos.values()]
    span = (max(xs) - min(xs)) + 2 * NODE_R
    limit = PANEL_W - 2 * NODE_R
    if span > limit:
        s = limit / span
        pos = {v: [p[0] * s, p[1] * s] for v, p in pos.items()}
        for f in fan_boxes:
            f["box"] = [c * s for c in f["box"]]
    return {v: tuple(p) for v, p in pos.items()}, [dict(hub=f["hub"], leaves=f["leaves"], box=tuple(f["box"])) for f in fan_boxes]


def _edge_repair(P, W, H, edges, nodes, rounds=6):
    """Nudge any node that a non-endpoint edge passes through, perpendicular to that edge."""
    for _ in range(rounds):
        fixed = 0
        for a, b in edges:
            if a not in P or b not in P: continue
            ax, ay = P[a]; bx, by = P[b]
            dx, dy = bx - ax, by - ay
            L2 = dx * dx + dy * dy
            if L2 < 1e-6: continue
            for v in nodes:
                if v in (a, b): continue
                vx, vy = P[v]
                t = ((vx - ax) * dx + (vy - ay) * dy) / L2
                if not (0.05 < t < 0.95): continue
                px, py = ax + t * dx, ay + t * dy
                offx, offy = vx - px, vy - py
                if abs(offx) < W[v] / 2 + 0.4 and abs(offy) < H[v] / 2 + 0.4:
                    nx_, ny_ = -dy, dx
                    nlen = math.sqrt(nx_ * nx_ + ny_ * ny_)
                    push = (H[v] / 2 + 0.8)
                    sign = 1 if (offx * nx_ + offy * ny_) >= 0 else -1
                    P[v] = [vx + sign * push * nx_ / nlen, vy + sign * push * ny_ / nlen]
                    fixed += 1
        if fixed:
            P = _relax(P, W, H, iters=120)
        else:
            break
    return P


def pack_blocks(blocks, maxw, bign=14):
    """Skyline/shelf pack ALL components (tallest first) left-to-right across the
    full width, wrapping to a new shelf when the row is full. A narrow-tall cluster
    and the small stars share a row, so the space beside the cluster gets filled."""
    items = sorted(blocks, key=lambda b: -b[1])
    GAPB = 4.0
    out = []; x = y = 0.0; shelf_h = 0.0; tw = 0.0
    for w, h, nc, pay in items:
        if x > 0 and x + w > maxw:
            x = 0.0; y += shelf_h + GAPB; shelf_h = 0.0
        out.append((x, y, pay)); x += w + GAPB
        shelf_h = max(shelf_h, h); tw = max(tw, x - GAPB)
    return out, min(tw, maxw), y + shelf_h


def _rows_into(items, region_w, gap, nrows):
    """Distribute boxes into nrows rows, adding each (widest first) to the row that
    is currently shortest -> balanced row widths. Returns list-of-rows."""
    rows = [[] for _ in range(nrows)]
    rw = [0.0] * nrows
    for it in sorted(items, key=lambda b: -b[0]):
        r = min(range(nrows), key=lambda i: rw[i])
        rows[r].append(it); rw[r] += it[0] + gap
    return [r for r in rows if r]


def _place_rows(rows, x0, region_w, y0, gap, justify=False):
    """Place already-grouped rows left->right, centred (or justified) within
    region_w, stacked top->down from y0. Returns (placements, used_w, used_h)."""
    out = []; y = y0; used_w = 0.0
    for rl in rows:
        roww = sum(b[0] for b in rl) + gap * (len(rl) - 1)
        rh = max(b[1] for b in rl)
        if justify and len(rl) > 1:
            extra = max(0.0, (region_w - roww)) / (len(rl) - 1)
            g = gap + extra; x = x0
        else:
            g = gap; x = x0 + max(0.0, (region_w - roww) / 2)
        for w, h, nc, pay in rl:
            out.append((x, y + (rh - h) / 2, pay)); x += w + g
        used_w = max(used_w, roww); y += rh + gap
    return out, used_w, (y - gap - y0 if rows else 0.0)


def _fill_row(rl, x_left, width, y, row_h):
    """Distribute a row of boxes over `width` with EVEN COLUMN CENTRES: box i is
    centred at x_left + (i+0.5)*width/n. Fills the width edge-to-edge with uniform,
    balanced spacing regardless of individual box widths (no edge-flinging, no
    centred-narrow gap). Vertically centred within row_h."""
    n = len(rl); col = width / n
    res = []
    for i, (w, h, nc, pay) in enumerate(rl):
        cx = x_left + (i + 0.5) * col
        res.append((cx - w / 2, y + (row_h - h) / 2, pay))
    return res


def _fits(rl, width):
    """True if every box gets a column at least as wide as itself (no overlap)."""
    col = width / max(1, len(rl))
    return all(b[0] <= col - 1.0 for b in rl)


def arrange_clusters(blocks, maxw, gap=4.0):
    """Tidy per-figure arrangement of island clusters (each a bounding box), spread
    to fill the whole figure width so nothing floats with empty margins:
      - 1 cluster            -> centred (a lone box can't be spread).
      - similar sizes         -> one row justified edge-to-edge (wraps if too wide).
      - one dominant cluster  -> big flush LEFT; the smaller ones in two storeys on
                                 the right, each row justified across the remaining
                                 width and aligned to the big one's height.
    """
    if not blocks:
        return [], 0.0, 0.0
    B = sorted(blocks, key=lambda b: -(b[0] * b[1]))
    if len(B) == 1:
        w, h, nc, pay = B[0]
        return [(0.0, 0.0, pay)], w, h

    big = B[0]; rest = sorted(B[1:], key=lambda b: -(b[0] * b[1]))
    dominant = big[0] * big[1] >= 2.0 * rest[0][0] * rest[0][1]
    # a big cluster is "tall" if it wants vertical company (two storeys beside it)
    tall_big = dominant and big[1] >= big[0] * 0.9

    # big cluster + many/tall -> big flush left, small in two even-column storeys
    if dominant and (len(rest) >= 4 or tall_big) and len(rest) >= 2:
        bw, bh, bnc, bpay = big
        region_x = bw + gap
        region_w = maxw - region_x
        rows = _rows_into(rest, region_w, gap, 2)
        rh0 = max(b[1] for b in rows[0]); rh1 = max(b[1] for b in rows[1])
        out = [(0.0, 0.0, bpay)]
        out += _fill_row(rows[0], region_x, region_w, 0.0, rh0)
        out += _fill_row(rows[1], region_x, region_w, max(rh0 + gap, bh - rh1), rh1)
        return out, maxw, max(bh, rh0 + gap + rh1)

    # dominant + few short small ones -> big flush left, rest even across the region
    if dominant and len(rest) >= 1:
        bw, bh, bnc, bpay = big
        region_x = bw + gap
        region_w = maxw - region_x
        rh = max(b[1] for b in rest)
        out = [(0.0, 0.0, bpay)]
        out += _fill_row(rest, region_x, region_w, max(0.0, (bh - rh) / 2), rh)
        return out, maxw, bh

    # similar sizes -> even columns across the full width (wrap to 2 rows if cramped)
    row = sorted(B, key=lambda b: -b[1])
    if _fits(row, maxw):
        rh = max(b[1] for b in row)
        return _fill_row(row, 0.0, maxw, 0.0, rh), maxw, rh
    for nrows in (2, 3):
        rows = _rows_into(B, maxw, gap, nrows)
        if all(_fits(rl, maxw) for rl in rows):
            break
    out = []; y = 0.0
    for rl in rows:
        rh = max(b[1] for b in rl)
        out += _fill_row(rl, 0.0, maxw, y, rh)
        y += rh + gap
    return out, maxw, y - gap


def drawn_nodes(cc, model, min_comp=3, drop_fans=True):
    """Node set actually drawn for a country: optionally strip directory fan
    leaves (the boxed members) and always drop <min_comp fragments / floaters."""
    pan = model.panels[cc]
    nodes = set(pan["A"]) | set(pan["P"])
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(pan["E"])
    if drop_fans:
        deg = dict(g.degree())
        leaves = set()
        for hub in nodes:
            lv = [w for w in g.neighbors(hub) if deg[w] == 1]
            if len(lv) > FAN_THRESH:
                leaves.update(lv)
        nodes -= leaves
        g = g.subgraph(nodes)
    keep = set().union(*[c for c in nx.connected_components(g) if len(c) >= min_comp]) if nodes else set()
    return keep


def layout_panel(cc, model, min_comp=3, maxw=PANEL_W - 4.0, drop_fans=True):
    pan = model.panels[cc]
    keep = drawn_nodes(cc, model, min_comp=min_comp, drop_fans=drop_fans)
    nodes = [v for v in (list(pan["A"]) + list(pan["P"])) if v in keep]
    edges = [(a, b) for a, b in pan["E"] if a in keep and b in keep]
    g = nx.Graph(); g.add_nodes_from(nodes); g.add_edges_from(edges)
    comps = [sorted(c) for c in nx.connected_components(g)]
    core = [c for c in comps if len(c) >= min_comp]     # keep only real networks
    iso = [v for c in comps if len(c) < min_comp for v in c]
    core.sort(key=len, reverse=True)
    blocks = []
    fanb = []
    for c in core:
        sub = [e for e in pan["E"] if e[0] in set(c) and e[1] in set(c)]
        Wd = {v: 2 * NODE_R for v in c}
        P = _rose(c, sub, model)                                # clusters-within-clusters
        P = _relax(P, Wd, Wd, iters=140)                        # de-overlap petals
        P = _edge_repair(P, Wd, Wd, sub, c, rounds=8)           # clear through-edges
        P = {v: tuple(p) for v, p in P.items()}
        pts = list(P.values()) + [(f["box"][0], f["box"][1]) for f in fanb] + [(f["box"][2], f["box"][3]) for f in fanb]
        ox = min(x for x, y in pts) - NODE_R; oy = min(y for x, y in pts) - NODE_R
        P = {v: (P[v][0] - ox, P[v][1] - oy) for v in c}
        fanb = [dict(f, box=(f["box"][0] - ox, f["box"][1] - oy, f["box"][2] - ox, f["box"][3] - oy)) for f in fanb]
        bw = max(x for x, y in pts) - ox + NODE_R
        bh = max(y for x, y in pts) - oy + NODE_R
        blocks.append((bw, bh, len(c), ("g", c, P, fanb)))
    # isolates are NOT drawn — they carry no network info and stay in the tables.
    # tidy arrangement: similar -> centred row; one dominant -> big left + 2 stories right
    placed, tw, th = arrange_clusters(blocks, maxw)
    pos = {}; fans = []
    for bx, by, (kind, members, P, fanb) in placed:
        for v in members:
            pos[v] = (bx + P[v][0], by + P[v][1])
        for f in fanb:
            x0, y0, x1, y1 = f["box"]
            fans.append(dict(hub=f["hub"], leaves=f["leaves"], box=(bx + x0, by + y0, bx + x1, by + y1)))
    return pos, tw, th, len(core), len(iso), fans


# ---------------- stage 6: checks ----------------
def check_panel(cc, model, pos, tw, th, fans=()):
    pan = model.panels[cc]
    nodes = list(pos)          # only drawn nodes (isolates excluded)
    issues = []
    ov = 0
    items = [(v, pos[v][0], pos[v][1], *model.box(v)) for v in nodes]
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            _, x1, y1, w1, h1 = items[i]; _, x2, y2, w2, h2 = items[j]
            if abs(x1 - x2) < (w1 + w2) / 2 - 0.01 and abs(y1 - y2) < (h1 + h2) / 2 - 0.01:
                ov += 1
    if ov: issues.append(f"{ov} overlaps")
    if tw > PANEL_W + 0.01: issues.append(f"width {tw:.0f}>{PANEL_W:.0f}")
    # suppressed fan edges are not drawn, so exclude from the through-edge check
    supp = set()
    for f in fans:
        for l in f["leaves"]:
            supp.add((min(f["hub"], l), max(f["hub"], l)))
    thr = 0
    for a, b in pan["E"]:
        if a not in pos or b not in pos:      # endpoint in a dropped <3 fragment
            continue
        if (min(a, b), max(a, b)) in supp:
            continue
        ax, ay = pos[a]; bx, by = pos[b]
        for v in nodes:
            if v in (a, b): continue
            vx, vy = pos[v]; w, h = model.box(v)
            t = ((vx - ax) * (bx - ax) + (vy - ay) * (by - ay)) / max((bx - ax) ** 2 + (by - ay) ** 2, 1e-9)
            if 0 < t < 1:
                px, py = ax + t * (bx - ax), ay + t * (by - ay)
                if abs(px - vx) < w / 2 and abs(py - vy) < h / 2:
                    thr += 1; break
    return issues, ov, thr


def dry_run(overlay=None):
    m = Model(overlay=overlay)
    print(f"actors placed {len(m.cc)} (stated {len(m.cc)-len(m.inferred)}, inferred {len(m.inferred)}) "
          f"| unplaced {len(m.unplaced)} | projects {len(m.proj_cc)}")
    tot_e = sum(len(p['E']) for p in m.panels.values())
    print(f"edges drawn in panels {tot_e} | listed cross-border {len(m.cross)} | total {tot_e+len(m.cross)}")
    print()
    print(f"{'CC':<4}{'Akt':>5}{'Prj':>5}{'Kant':>6}{'Komp':>6}{'Iso':>5}{'W':>7}{'H':>7}{'Pg':>5}{'thru':>6}  issues")
    tot_h = 0
    for cc in m.countries:
        pan = m.panels[cc]
        if not pan["A"] and not pan["P"]:
            continue
        pos, tw, th, ncore, niso, fans = layout_panel(cc, m)
        issues, ov, thr = check_panel(cc, m, pos, tw, th, fans)
        pg = th / PANEL_H
        tot_h += th
        print(f"{cc:<4}{len(pan['A']):>5}{len(pan['P']):>5}{len(pan['E']):>6}{ncore:>6}{niso:>5}"
              f"{tw:>7.0f}{th:>7.0f}{pg:>5.2f}{thr:>6}  {'; '.join(issues) if issues else 'ok'}")
    print(f"\ntotal stacked height {tot_h:.0f} mm  ->  {tot_h/PANEL_H:.1f} panel-pages")
    return m


if __name__ == "__main__":
    import json as _j
    ov = [_j.load(io.open(r"E:/recherche/_neo4j/netz/overlay.json", encoding="utf-8")), _j.load(io.open(r"E:/recherche/_neo4j/netz/overlay2.json", encoding="utf-8")),
          _j.load(io.open(r"E:/recherche/_neo4j/netz/overlay3.json", encoding="utf-8"))]
    dry_run(overlay=ov)
