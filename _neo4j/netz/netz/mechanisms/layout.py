"""Force layout: one Fruchterman-Reingold simulation per country panel,
producing abstract mm positions for a fixed W x H frame.

VERBATIM PORT of gen_abb.country_layout -- same loop structure, arithmetic
expression order, clamp sequence, `random.Random(seed + n)`. Byte-parity
with the legacy fragment depends on ALL of:
  - node order = panel.actors (sorted by name) + panel.projects (sorted by name)
  - component dict insertion order = first-seen node in the above node order
  - edge list order = panel.edges (canonical, from mechanisms.countries.partition)
  - float summation order in the two force loops (unchanged below)
Do not vectorize, do not "clean up" the union-find or hash-grid, do not
reorder any loop. If you need to change the physics, change it in a NEW
function and keep this one as the parity reference.

LAYOUT IS MECHANISM, NOT RENDERER: this module owns the POLICY (component
seeding, hub/leaf spring lengths, "networked nodes stay inset from the wall
while individuals may reach the edge", the no-overlap guarantee). The
renderer supplies the Frame it wants filled and consumes the returned
abstract mm coordinates -- it does not know HOW they were produced.
"""
import random, math
from dataclasses import dataclass

NODE_R = 1.75 * 1.3
MIN_D = 2 * NODE_R + 0.8   # hard minimum centre distance (no overlaps)


@dataclass(frozen=True)
class Frame:
    w: float
    h: float
    margin: float


DEFAULT_FRAME = Frame(w=181.0, h=50.0, margin=3.0)   # PANEL_W x (4-per-page height) x SMARGIN


def force_layout(panel, keep: set, frame: Frame = DEFAULT_FRAME, seed: int = 7):
    """Returns (positions: {eid: (x, y)}, edges: [(a, b), ...]) -- edges is the
    keep-filtered list actually used by the simulation (and by the renderer
    for drawing lines), in the same order as panel.edges."""
    BOX_W, BOX_H, IM = frame.w, frame.h, frame.margin
    nodes = list(panel.actors) + list(panel.projects)
    edges = [(a, b) for a, b in panel.edges if a in keep and b in keep]
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
            # networked nodes are held further inside the frame (a bigger keep-out
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
