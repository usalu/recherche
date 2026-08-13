"""Table renderer: the ORIGINAL dense TikZ-grid layout (predates Stage 8's
switch to \\SemioTableLong), restored on request and re-pointed at the
CURRENT data model so it stays consistent with the graph figures (same
`net.tid`, same 955-node/3-overlay panel).

Ported from the legacy `gen_tables.py` (2026-08-10), fixing the one real bug
found there: `roles_str()` built a string containing an intentional LaTeX
separator macro (`\\textperiodcentered\\ `) and then ran the WHOLE joined
string through `esc()`, which escapes `\\` and braces -- corrupting its own
separator (rendered as a literal backslash-brace pair before every role,
confirmed visually). The fix here escapes each role label individually,
BEFORE joining with the raw (never-escaped) separator macro.

Deliberately un-grouped (flat, alphabetical per country, no P/U/M/... section
bands) and denser (~66 rows/page, small monospace grid) than the Stage 8
table -- this is the visual difference the restore was for.
"""
import collections

from ...mechanisms.countries import is_person
from .escape import esc, esct
from .vocab import CC_NAME, ROLE_SHORT

PITCH = 3.35
X_NR, X_NAME, X_TYP, X_ROLE = 0.0, 8.5, 92.0, 104.0
NAME_MAX = 52
ROWS_PER_PAGE = 66

TYPE_ABBR_GRID = {
    "Unternehmen": "UN", "Materialhub_Bauteilboerse": "MH", "Forschung_Lehre": "FL",
    "NGO_Verband_Netzwerk": "NG", "Oeffentliche_Institution": "OI",
    "Software_Tool_Anbieter": "ST", "Organisation": "OR", "Foerdergeber_Programmtraeger": "GE",
}


def role_frequency(net) -> collections.Counter:
    rf = collections.Counter()
    for a in net.raw.actors:
        rf.update(net.raw.roles.get(a["eid"], ()))
    return rf


def _roles_str(net, e, rf: collections.Counter) -> str:
    rs = sorted(net.raw.roles.get(e, []), key=lambda r: (-rf.get(r, 0), r))
    if not rs:
        return r"\textcolor{semio-chrome-border-normal}{ohne}"
    # escape each label BEFORE joining -- never run the already-valid
    # separator macro back through esc() a second time.
    labels = [esc(ROLE_SHORT.get(r, r[:12]).replace("_", " ")) for r in rs[:4]]
    return r" \textperiodcentered\ ".join(labels)


def _hdr(y):
    s = []
    for x, t in [(X_NR, "ID"), (X_NAME, "Name"), (X_TYP, "Typ"), (X_ROLE, "Rollen")]:
        s.append(r"\node[anchor=base west, font=\SemioMono\fontsize{6.4pt}{6.6pt}\selectfont, "
                  r"text=semio-chrome-foreground, inner sep=0] at (%.1f,%.2f) {%s};" % (x, y, t))
    s.append(r"\draw[draw=semio-chrome-border-emphasized, line width=0.75pt] (0,%.2f) -- (181,%.2f);"
              % (y + 1.3, y + 1.3))
    return s


def _row(net, e, y, rf: collections.Counter, dim: bool = False):
    tid = net.tid[e]
    typ_abbr = TYPE_ABBR_GRID.get(net.raw.types.get(e), "--")
    name_col = "semio-chrome-border-normal" if dim else "semio-chrome-foreground"
    nr_col = "semio-chrome-border-normal" if dim else "semio-chrome-foreground"
    return [
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, text=%s, "
        r"inner sep=0] at (%.1f,%.2f) {%s};" % (nr_col, X_NR, y, esc(tid)),
        r"\node[anchor=base west, font=\SemioSans\fontsize{7pt}{7.2pt}\selectfont, text=%s, "
        r"inner sep=0] at (%.1f,%.2f) {%s};" % (name_col, X_NAME, y, esct(net.raw.name(e), NAME_MAX)),
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-border-normal, inner sep=0] at (%.1f,%.2f) {%s};" % (X_TYP, y, typ_abbr),
        r"\node[anchor=base west, font=\SemioSans\fontsize{6.2pt}{6.4pt}\selectfont, "
        r"text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};"
        % (X_ROLE, y, _roles_str(net, e, rf)),
    ]


def build_grid_fragment(net, out_path):
    rf = role_frequency(net)
    items = []  # ("head", label) | ("row", eid, is_person)
    for cc in net.countries:
        pan = net.panels.get(cc)
        if pan is None:
            continue
        orgs = sorted(pan.actors, key=lambda e: net.num[e])
        projs = sorted(pan.projects, key=lambda e: net.num[e])
        persons = sorted(
            (a["eid"] for a in net.raw.actors
             if net.res.cc.get(a["eid"]) == cc and is_person(net.raw, a["eid"])),
            key=lambda e: net.raw.name(e).lower(),
        )
        if not (orgs or projs or persons):
            continue
        items.append(("head", "%s \\textperiodcentered\\ %d Organisationen \\textperiodcentered\\ "
                               "%d Projekte \\textperiodcentered\\ %d Personen"
                       % (CC_NAME.get(cc, cc), len(orgs), len(projs), len(persons))))
        for e in sorted(orgs + projs, key=lambda e: net.raw.name(e).lower()):
            items.append(("row", e, False))
        for e in persons:
            items.append(("row", e, True))

    out = [r"\section{Akteurstabellen nach Land}", "",
           r"{\SemioSans\fontsize{7.6pt}{9.5pt}\selectfont ID = Typ-Buchstabe + laufende Nummer je Land "
           r"(z.\,B. \textbf{M07}) \textendash\ identisch mit der Kreis-Beschriftung im zugeh\"origen "
           r"Netzdiagramm (Kap. Akteursnetze).\\[2mm]}",
           r"\clearpage", r"\newgeometry{left=1.2cm, right=1.2cm, top=1.5cm, bottom=1.5cm}"]

    pages, page, count = [], [], 0
    for it in items:
        if count >= ROWS_PER_PAGE:
            pages.append(page); page = []; count = 0
        page.append(it)
        count += 1
    if page:
        pages.append(page)

    for pi, chunk in enumerate(pages):
        s = [r"\begin{Figure}[title={Tabelle %d\,/\,%d}, break=false]" % (pi + 1, len(pages)),
             r"\begin{tikzpicture}[semio, x=1mm, y=-1mm]"]
        s += _hdr(0.0)
        y = 5.0
        for it in chunk:
            if it[0] == "head":
                s.append(r"\node[anchor=base west, font=\SemioSans\fontsize{7.6pt}{7.8pt}\selectfont, "
                          r"text=semio-chrome-foreground, inner sep=0] at (0,%.2f) {%s};" % (y, it[1]))
                s.append(r"\draw[draw=semio-chrome-border-normal, line width=0.5pt] "
                          r"(0,%.2f) -- (181,%.2f);" % (y + 1.0, y + 1.0))
                y += PITCH + 1.2
            else:
                s += _row(net, it[1], y, rf, dim=it[2])
                y += PITCH
        s.append(r"\end{tikzpicture}")
        s.append(r"\end{Figure}")
        out.append("\n".join(s))
        out.append("")
    out += [r"\clearpage", r"\restoregeometry"]

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    return len(items), len(pages)
