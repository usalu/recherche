"""Per-country actor tables, sectioned by Actor-Typ (Option 2).

ID scheme is now UNIFIED with the graph: single-letter Typ code + per-country
per-type running number (e.g. M07, U46, F03), computed once in Model.tid and
used verbatim as both the table's primary key and the node label burned into
the compiled Abbildung circles. No more separate "Graph-Nr." cross-reference
column -- the ID you read on a circle IS the row you look up.
"""
import io, json, collections
import gen_abb as G           # reuses the already-integrated overlay+audit+prune Model
from net_lib import esc, esct, ISO, ROLE_DE, TYPE_LETTER

SP = r"E:/recherche/_neo4j/netz"
m = G.m
n = m.n
CC_NAME = {v: k for k, v in ISO.items()}
ROLE_SHORT = {k: v.split("/")[0][:14] for k, v in ROLE_DE.items()}
RF = collections.Counter(r for a in n.actors for r in n.roles[a["eid"]])

TYP_ORDER = ["Unternehmen", "Materialhub_Bauteilboerse", "Forschung_Lehre",
             "NGO_Verband_Netzwerk", "Oeffentliche_Institution", "Software_Tool_Anbieter",
             "Organisation", "Foerdergeber_Programmtraeger", "Unbekannt"]
TYP_NAME_DE = {
    "Unternehmen": "Unternehmen", "Materialhub_Bauteilboerse": "Materialhub / Bauteilbörse",
    "Forschung_Lehre": "Forschung / Lehre", "NGO_Verband_Netzwerk": "NGO / Verband / Netzwerk",
    "Oeffentliche_Institution": "Öffentliche Institution", "Software_Tool_Anbieter": "Software / Tool-Anbieter",
    "Organisation": "Organisation", "Foerdergeber_Programmtraeger": "Förderträger", "Unbekannt": "Unbekannt"}

PITCH = 3.35
X_ID, X_NAME, X_ROLE = 0.0, 9.0, 95.0
NAME_MAX, ROLE_MAX = 62, 68
ROWS = 62


def roles_str(e):
    # escape each role label BEFORE joining with the LaTeX dot-separator macro
    # -- esc()/esct() escape backslashes, so a macro must never be inserted
    # into the string ahead of an esc() call.
    # secondary key `r` breaks ties deterministically -- n.roles[e] is a set, so
    # without a tiebreak, equal-frequency roles sort in hash-random per-process order.
    rs = sorted(n.roles.get(e, []), key=lambda r: (-RF.get(r, 0), r))
    if not rs:
        return r"\textcolor{semio-chrome-border-normal}{ohne}"
    parts, budget = [], ROLE_MAX
    for r in rs[:5]:
        label = ROLE_SHORT.get(r, r[:12]).replace("_", " ")
        if len(label) > budget:
            break
        parts.append(esc(label)); budget -= len(label) + 3
    return r" \textperiodcentered\ ".join(parts) if parts else r"\textcolor{semio-chrome-border-normal}{ohne}"


def hdr(y):
    s = []
    for x, t in [(X_ID, "ID"), (X_NAME, "Name"), (X_ROLE, "Rollen")]:
        s.append(r"\node[anchor=base west, font=\SemioMono\fontsize{6.4pt}{6.6pt}\selectfont, text=semio-chrome-foreground, inner sep=0] at (%.1f,%.2f) {%s};" % (x, y, t))
    s.append(r"\draw[draw=semio-chrome-border-emphasized, line width=0.75pt] (0,%.2f) -- (181,%.2f);" % (y + 1.3, y + 1.3))
    return s


def row(idc, e, y, dim=False):
    col = "semio-chrome-border-normal" if dim else "semio-chrome-foreground"
    marks = ""
    if e in n.new_eids:
        marks += r"\,\textdegree"
    if e in m.inferred and e not in n.new_eids:
        marks += r"\,\textdagger"
    s = [
        r"\node[anchor=base west, font=\SemioMono\fontsize{6.2pt}{6.4pt}\selectfont, text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};" % (X_ID, y, idc),
        r"\node[anchor=base west, font=\SemioSans\fontsize{7pt}{7.2pt}\selectfont, text=%s, inner sep=0] at (%.1f,%.2f) {%s%s};" % (col, X_NAME, y, esct(n.name(e), NAME_MAX), marks),
        r"\node[anchor=base west, font=\SemioSans\fontsize{6.2pt}{6.4pt}\selectfont, text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};" % (X_ROLE, y, roles_str(e)),
    ]
    return s


def sec(y, label):
    return [
        r"\node[anchor=base west, font=\SemioSans\fontsize{6.6pt}{6.8pt}\selectfont, text=semio-chrome-foreground, inner sep=0] at (0,%.2f) {%s};" % (y, label),
        r"\draw[draw=semio-chrome-border-normal, line width=0.4pt] (0,%.2f) -- (181,%.2f);" % (y + 0.9, y + 0.9),
    ]


# ---- build item stream: head(country) / sec(typ) / row ----
items = []
tot_rows = tot_persons = 0
for cc in m.countries:
    pan = m.panels.get(cc, {"A": [], "P": []})
    projs = sorted(pan["P"], key=lambda e: m.num[e])
    persons = sorted([a["eid"] for a in n.actors if m.cc.get(a["eid"]) == cc and m.is_person(a["eid"])],
                     key=lambda e: n.name(e).lower())
    if not (pan["A"] or projs or persons):
        continue
    items.append(("head", "%s \\textperiodcentered\\ %d Organisationen \\textperiodcentered\\ %d Projekte \\textperiodcentered\\ %d Personen"
                  % (CC_NAME.get(cc, cc), len(pan["A"]), len(projs), len(persons))))
    if projs:
        items.append(("sec", "P — Projekte"))
        for e in projs:
            items.append(("row", m.tid[e], e, False))
            tot_rows += 1
    by_typ = collections.defaultdict(list)
    for e in pan["A"]:
        by_typ[n.types.get(e, "Unbekannt")].append(e)
    for typ in TYP_ORDER:
        es = sorted(by_typ.get(typ, []), key=lambda e: n.name(e).lower())
        if not es:
            continue
        items.append(("sec", "%s — %s" % (TYPE_LETTER.get(typ, "X"), TYP_NAME_DE[typ])))
        for e in es:
            items.append(("row", m.tid[e], e, False))
            tot_rows += 1
    if persons:
        items.append(("sec", "E — Personen (Einzelpersonen)"))
        for e in persons:
            items.append(("row", m.tid[e], e, True))
            tot_rows += 1; tot_persons += 1

# ---- paginate ----
out = [r"\section{Akteurstabellen nach Land}",
       r"{\SemioSans\fontsize{7.6pt}{9.5pt}\selectfont ID = Typ-Buchstabe + laufende Nummer je Land (z.\,B. \textbf{M07}) "
       r"-- identisch mit der Kreis-Beschriftung im zugehörigen Netzdiagramm (Kap. Akteursnetze). "
       r"\textdegree\ = neu erforscht \textperiodcentered\ \textdagger\ = Land erschlossen.\\[2mm]}",
       r"\clearpage", r"\newgeometry{left=1.2cm, right=1.2cm, top=1.5cm, bottom=1.5cm}"]
page = []; pages = []; count = 0
for it in items:
    if it[0] != "row" and count >= ROWS - 2:   # keep a section header from being orphaned at page bottom
        pages.append(page); page = []; count = 0
    if count >= ROWS:
        pages.append(page); page = []; count = 0
    page.append(it); count += 1
if page:
    pages.append(page)

for pi, chunk in enumerate(pages):
    s = [r"\begin{Figure}[title={Akteurstabellen \textperiodcentered\ Seite %d\,/\,%d}, break=false]" % (pi + 1, len(pages)),
         r"\begin{tikzpicture}[semio, x=1mm, y=-1mm]"]
    s += hdr(0.0)
    y = 5.0
    for it in chunk:
        if it[0] == "head":
            s.append(r"\node[anchor=base west, font=\SemioSans\fontsize{7.6pt}{7.8pt}\selectfont, text=semio-chrome-foreground, inner sep=0] at (0,%.2f) {%s};" % (y, it[1]))
            s.append(r"\draw[draw=semio-chrome-border-emphasized, line width=0.5pt] (0,%.2f) -- (181,%.2f);" % (y + 1.0, y + 1.0))
            y += PITCH + 1.4
        elif it[0] == "sec":
            s += sec(y, it[1]); y += PITCH + 0.6
        else:
            s += row(it[1], it[2], y, it[3]); y += PITCH
    s.append(r"\end{tikzpicture}"); s.append(r"\end{Figure}")
    out.append("\n".join(s)); out.append("")
out += [r"\clearpage", r"\restoregeometry"]
io.open(SP + "/figs/frag_tables2.tex", "w", encoding="utf-8", newline="\n").write("\n".join(out))
print(f"rows={tot_rows} (persons={tot_persons})  pages={len(pages)}")
