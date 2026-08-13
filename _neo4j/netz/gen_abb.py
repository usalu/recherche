import io, json, random, math
from netplate import Model, layout_panel, check_panel, NODE_R, PANEL_W
from net_lib import ISO

PAGE_MAX_H = 232.0     # a single country figure never taller than the text block
SMARGIN = 3.0          # keep scattered dots off the box edge
SP_TARGET = 6.2        # preferred spacing between scattered dots (repulsion range)
MIN_D = 2 * NODE_R + 0.8   # hard minimum centre distance (no overlaps)

SP = r"E:/recherche/_neo4j/netz"
ov = [json.load(io.open(SP + f"/overlay{s}.json", encoding="utf-8")) for s in ["", "2", "3"]]
# second-audit: 175 verified known<->known connections + FR/BE prune (60/27, least
# reuse-relevant unconnected actors; newly-connected ones from the audit are spared)
_audit_edges = json.load(io.open(SP + "/audit2_peer_edges.json", encoding="utf-8"))["edges"]
_extra_peers = [(e["a"], e["b"]) for e in _audit_edges]
_prune_eids = set(json.load(io.open(SP + "/prune_eids.json", encoding="utf-8")))
m = Model(overlay=ov, extra_peers=_extra_peers, exclude=_prune_eids)
CC_NAME = {v: k for k, v in ISO.items()}


def node_tikz(e, x, y, label=True):
    is_proj = e in m.proj_cc
    is_new = e in m.n.new_eids
    is_inf = e in m.inferred and not is_new
    if is_proj:
        style = "fill=semio-chrome-panel, draw=semio-chrome-border-emphasized, line width=1.5pt"; txt = "semio-chrome-foreground"
    elif is_new:
        style = "fill=semio-chrome-window, draw=semio-chrome-border-emphasized, line width=0.75pt"; txt = "semio-chrome-foreground"
    elif is_inf:
        style = "fill=semio-chrome-canvas, draw=semio-chrome-border-normal, line width=0.75pt, dash pattern=on 2.25pt off 1.5pt"; txt = "semio-chrome-text-normal"
    else:
        style = "fill=semio-chrome-canvas, draw=semio-chrome-border-normal, line width=0.75pt"; txt = "semio-chrome-text-normal"
    r = NODE_R + (0.3 if is_proj else 0.0)
    out = r"\draw[%s] (%.2f,%.2f) circle (%.2fmm);" % (style, x, y, r)
    if label:
        out += r"\node[font=\SemioMono\fontsize{5.2pt}{5.4pt}\selectfont, text=%s, inner sep=0] at (%.2f,%.2f) {%s};" % (txt, x, y, m.label(e))
    return out


from netplate import drawn_nodes

BOX_W = PANEL_W          # every Abbildung the same size
BOX_H = 50.0             # fixed height -> four equal Abbildungen per page
IM = SMARGIN
L_LEAF = MIN_D + 1.0     # short spring: satellite hugs its hub
L_CORE = 7.6             # longer spring between hubs
R_REP = 8.2              # local repulsion range (spreads everything evenly)


def country_layout(cc, seed=7):
    """One Fruchterman-Reingold force graph per country in a fixed BOX_W x BOX_H
    frame. Natural distance k = sqrt(area/n) sets the even spacing so nodes fill
    the frame without piling on the walls; inverse-square repulsion (soft-capped
    at short range so it can't blow a cluster apart) spreads everything, while
    stiff SHORT springs keep each network's rose tight. Connected components are
    seeded together so clusters form cleanly. A hard pass removes any overlap."""
    pan = m.panels[cc]
    keep = drawn_nodes(cc, m)
    nodes = list(pan["A"]) + list(pan["P"])
    edges = [(a, b) for a, b in pan["E"] if a in keep and b in keep]
    deg = {}
    for a, b in edges:
        deg[a] = deg.get(a, 0) + 1; deg[b] = deg.get(b, 0) + 1
    n = len(nodes)
    rng = random.Random(seed + n)
    hix, hiy = BOX_W - IM, BOX_H - IM
    cx, cy = BOX_W / 2, BOX_H / 2

    # connected components -> seed each together so its rose forms cleanly
    par = {e: e for e in nodes}
    def find(x):
        while par[x] != x:
            par[x] = par[par[x]]; x = par[x]
        return x
    for a, b in edges:
        par[find(a)] = find(b)
    comps = {}
    for e in nodes:
        comps.setdefault(find(e), []).append(e)
    P = {}
    for members in comps.values():
        gxc = rng.uniform(IM + 8, hix - 8); gyc = rng.uniform(IM + 5, hiy - 5)
        for e in members:
            P[e] = [gxc + rng.uniform(-4, 4), gyc + rng.uniform(-4, 4)]

    k = max(6.0, min(15.0, 0.92 * math.sqrt((BOX_W - 2 * IM) * (BOX_H - 2 * IM) / n)))
    cutoff = 2.7 * k
    softmin = MIN_D * 0.9
    L_leaf = MIN_D + 0.6
    L_core = 7.0

    def rest(a, b): return L_leaf if deg.get(a, 0) == 1 or deg.get(b, 0) == 1 else L_core
    def kco(a, b): return 0.95 if deg.get(a, 0) == 1 or deg.get(b, 0) == 1 else 0.55

    def hashgrid(cell):
        g = {}
        for e in nodes:
            x, y = P[e]; g.setdefault((int(x // cell), int(y // cell)), []).append(e)
        return g

    for it in range(380):
        cool = max(0.22, 1.0 - it / 380.0)
        grid = hashgrid(cutoff)
        disp = {e: [0.0, 0.0] for e in nodes}
        for e in nodes:
            ex, ey = P[e]; gx = int(ex // cutoff); gy = int(ey // cutoff)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for f in grid.get((gx + dx, gy + dy), ()):
                        if f == e:
                            continue
                        fx, fy = P[f]; ddx = ex - fx; ddy = ey - fy
                        d = math.hypot(ddx, ddy) or 1e-6
                        if d < cutoff:
                            deff = d if d > softmin else softmin      # cap short-range blow-up
                            fr = 1.15 * k * k / (deff * deff)
                            disp[e][0] += fr * ddx / d; disp[e][1] += fr * ddy / d
            # network nodes are held further inside the frame (a bigger keep-out
            # margin + stronger centre pull) so clusters never touch the border;
            # individual dots may reach the edges.
            netnode = deg.get(e, 0) > 0
            grav = 0.020 if netnode else 0.004
            disp[e][0] += (cx - ex) * grav; disp[e][1] += (cy - ey) * grav
            mx = 11.0 if netnode else IM
            my = 8.0 if netnode else IM
            if ex < mx: disp[e][0] += (mx - ex) * 0.9
            if ex > BOX_W - mx: disp[e][0] += (BOX_W - mx - ex) * 0.9
            if ey < my: disp[e][1] += (my - ey) * 0.9
            if ey > BOX_H - my: disp[e][1] += (BOX_H - my - ey) * 0.9
        for a, b in edges:
            ax, ay = P[a]; bx, by = P[b]
            dx = bx - ax; dy = by - ay; d = math.hypot(dx, dy) or 1e-6
            L0 = rest(a, b); f = kco(a, b) * (d - L0) / d
            disp[a][0] += f * dx; disp[a][1] += f * dy
            disp[b][0] -= f * dx; disp[b][1] -= f * dy
        maxstep = k * 0.55 * cool
        for e in nodes:
            mag = math.hypot(disp[e][0], disp[e][1]) or 1e-6
            s = min(mag, maxstep) / mag
            P[e][0] = min(hix, max(IM, P[e][0] + disp[e][0] * s))
            P[e][1] = min(hiy, max(IM, P[e][1] + disp[e][1] * s))

    # hard de-overlap (both nodes of a colliding pair move apart)
    for _ in range(400):
        grid = hashgrid(MIN_D)
        moved = 0
        for e in nodes:
            ex, ey = P[e]; gx = int(ex // MIN_D); gy = int(ey // MIN_D)
            for dx in (-1, 0, 1):
                for dy in (-1, 0, 1):
                    for f in grid.get((gx + dx, gy + dy), ()):
                        if f == e:
                            continue
                        fx, fy = P[f]; ddx = ex - fx; ddy = ey - fy
                        d = math.hypot(ddx, ddy) or 1e-6
                        if d < MIN_D:
                            s = 0.5 * (MIN_D - d) / d
                            P[e][0] = ex = min(hix, max(IM, ex + s * ddx))
                            P[e][1] = ey = min(hiy, max(IM, ey + s * ddy))
                            P[f][0] = min(hix, max(IM, fx - s * ddx))
                            P[f][1] = min(hiy, max(IM, fy - s * ddy))
                            moved += 1
        if not moved:
            break
    return {e: (P[e][0], P[e][1]) for e in nodes}, edges


def country_figure(cc):
    pan = m.panels[cc]
    nodes = list(pan["A"]) + list(pan["P"])
    if not nodes:
        return None
    P, edges = country_layout(cc)
    nA = sum(1 for e in pan["A"])
    nP = sum(1 for e in pan["P"])
    s = [r"\begin{Figure}[title={%s \textperiodcentered\ %d Organisationen \textperiodcentered\ %d Projekte}, break=false]" % (CC_NAME.get(cc, cc), nA, nP),
         r"\begin{tikzpicture}[semio, x=1mm, y=-1mm]",
         r"\useasboundingbox (0,0) rectangle (%.2f,%.2f);" % (BOX_W, BOX_H)]
    for a, b in edges:
        ax, ay = P[a]; bx, by = P[b]
        s.append(r"\draw[draw=semio-chrome-border-emphasized, line width=0.75pt] (%.2f,%.2f) -- (%.2f,%.2f);" % (ax, ay, bx, by))
    for e in nodes:
        px, py = P[e]
        s.append(node_tikz(e, px, py, label=True))
    s.append(r"\end{tikzpicture}")
    s.append(r"\end{Figure}")
    return "\n".join(s), nA, nP, len(nodes), 0


order = [cc for cc in m.countries if cc in m.panels and (m.panels[cc]["A"] or m.panels[cc]["P"])]
out = [r"\section{Akteursnetze nach Land}",
       r"{\SemioSans\fontsize{7.6pt}{9.5pt}\selectfont Ein Netz je Land \textendash\ nur zusammenh\"angende Cluster ab drei Knoten. Kreis mit dicker Kontur = Projekt, gef\"ullter Kreis = neu recherchiert, gestrichelt = Land erschlossen. Zahl = Zeilennummer der zugeh\"origen Tabelle.\\[2mm]}",
       r"\clearpage", r"\newgeometry{left=1.2cm, right=1.2cm, top=1.5cm, bottom=1.5cm}"]
tot = 0
for cc in order:
    r = country_figure(cc)
    if not r:
        continue
    frag, nA, nP, nd, nfill = r
    out.append(frag); out.append("")
    tot += nd
    print(f"  {cc}: {nd} clustered + {nfill} scattered = {nd + nfill}")
out += [r"\clearpage", r"\restoregeometry"]
io.open(SP + "/figs/frag_abb.tex", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"total drawn: {tot} nodes across {len(order)} country figures")
