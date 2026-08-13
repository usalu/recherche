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
import io
import json

from ...mechanisms.countries import is_person
from .escape import esc
from .vocab import CC_NAME, ROLE_GROUP, GROUP_LABEL

PITCH = 3.35
# 📐 Column origins in mm across the 181 mm text block. Budget measured, not
# guessed: at 0.2294 mm/char/pt the spelled-out role plus the 90-char Relevanz
# needs ~316 mm and cannot share a line at any size down to the 5.4 pt floor.
# The role therefore prints as its taxonomy group letter (see _rolegroups),
# which frees ~70 mm and puts Relevanz back on the same line as its actor.
#
# Name at 44 chars/6.4 pt = 64.6 mm (was 34/7 pt = 54.6 mm, hard-cutting 82 of
# 620 names mid-word -- fixed by switching to _clip(), the width increase
# roughly halves how many still get shortened at all, 82 -> 38). 6.4 pt also
# matches the header/code size, so node rows stop reading heavier than edge
# rows (they shared no font size before this).
X_IMG, X_NR, X_NAME, X_CODE, X_REL, X_Q = 0.0, 5.5, 14.0, 80.5, 91.5, 176.0
NAME_MAX = 44
REL_MAX = 60
ROWS_PER_PAGE = 66
# 3.0, nicht 3.6: bei PITCH 3.35 stossen zwei Logos in aufeinanderfolgenden
# Zeilen sonst aneinander (gemessen an SOCOTEC/Soprema auf der FR-Seite).
IMG_MM = 3.0
# Versatz der optischen Zeilenmitte gegen die Grundlinie. NEGATIV, weil y in
# diesem Raster nach unten waechst: die Versalhoehe von 6,4 pt liegt rund
# 0,8 mm ueber der Grundlinie, also bei y - 0,8. Beide Vorzeichen wurden im
# gebauten PDF nachgemessen (Bildmitte gegen Textgrundlinie derselben Zeile),
# nicht hergeleitet -- +0.8 setzte das Logo sichtbar in die naechste Zeile.
IMG_MID = -0.8

# 🔗 Beziehungsband je Land. Von/Nach sind dieselben IDs wie in der
# Knotentabelle und im Diagramm -- die Kante wird ueber die Endknoten
# gelesen, nicht ueber einen eigenen Schluessel. X_BESCH == X_REL: beide
# Baender teilen sich dieselbe Spaltengrenze, damit sie als ein System lesen.
X_VON, X_ART, X_BESCH, X_QK = 5.5, 34.0, X_REL, 176.0
BESCH_MAX = REL_MAX


def role_frequency(net) -> collections.Counter:
    rf = collections.Counter()
    for a in net.raw.actors:
        rf.update(net.raw.roles.get(a["eid"], ()))
    return rf


def load_klassifikation(path):
    """eid -> {rolle, rollen[], relevanz, beleg_url}. The strict review's
    actor/project file is the authority for what a node *does*; net.raw.roles
    is the superseded 31-category export scheme and is no longer printed."""
    with io.open(path, encoding="utf-8") as f:
        return json.load(f)


def _code(rec) -> str:
    """Taxonomy group letters, deduplicated and ordered -- a node with three
    roles from one group prints one letter, not three.

    The separator must terminate itself (`\\,` here): a bare
    `\\textperiodcentered` directly followed by the next letter is read as the
    control sequence `\\textperiodcenteredI` and stops the build."""
    letters = sorted({ROLE_GROUP.get(r) for r in (rec.get("rollen") or []) if ROLE_GROUP.get(r)})
    return r"\,\textperiodcentered\,".join(letters) if letters else "--"


def _clip(s: str, maxlen: int) -> str:
    """Truncate on a word boundary, never mid-word -- a hard character cut
    prints fragments like 'fuer neue Pro' and has already shipped once."""
    s = (s or "").strip()
    if len(s) <= maxlen:
        return esc(s)
    cut = s[:maxlen].rsplit(" ", 1)[0].rstrip(" ,;:")
    return esc(cut) + r"\,\textellipsis{}"


def _hdr(y, cols):
    # Column labels are project-owned constants, already print-ready -- never
    # esc() them. esc() is for DATA fields only; running it over a label that
    # already carries a LaTeX macro or an intentional separator corrupts the
    # macro (the exact roles_str trap the module docstring warns about --
    # here it turned "Von -> Nach" into a broken \textbackslash{}-strewn
    # mess). If a label ever needs a literal &, %, _ etc., escape it by hand
    # at the point it's written into NODE_COLS/EDGE_COLS, not here.
    s = []
    for x, t in cols:
        s.append(r"\node[anchor=base west, font=\SemioMono\fontsize{6.4pt}{6.6pt}\selectfont, "
                  r"text=semio-chrome-foreground, inner sep=0] at (%.1f,%.2f) {%s};" % (x, y, t))
    s.append(r"\draw[draw=semio-chrome-border-emphasized, line width=0.75pt] (0,%.2f) -- (181,%.2f);"
              % (y + 1.3, y + 1.3))
    return s


NODE_COLS = [(X_NR, "ID"), (X_NAME, "Name"), (X_CODE, "Rolle"),
             (X_REL, "Relevanz für Wiederverwendung"), (X_Q, "Q")]
# ASCII arrow, not \textrightarrow{}: ShareTechMono (SemioMono, the font this
# header and the Von/Nach data cells are set in) has no U+2192 glyph -- the
# build fails with "could not represent character" once the macro itself
# renders correctly. Plain "->"/"--" need no glyph and match the mono ID font.
EDGE_COLS = [(X_VON, "Von -> Nach"), (X_ART, "Art"),
             (X_BESCH, "Beschreibung"), (X_QK, "Q")]


def _row(net, e, y, kl, qnum, images, dim: bool = False):
    rec = kl.get(e) or {}
    name_col = "semio-chrome-border-normal" if dim else "semio-chrome-foreground"
    q = qnum.get(rec.get("beleg_url") or "", "")
    s = []
    img = (images or {}).get(e)
    if img:
        # \SemioLogoFit statt \includegraphics: derselbe Resolver wie bei jedem
        # anderen Logo im Bericht, also -dark-Variante im Dark-Build und ein
        # leerer Platzhalter statt eines TeX-Fehlers, wenn die Datei fehlt.
        s.append(r"\node[anchor=west, inner sep=0] at (%.1f,%.2f) "
                 r"{\SemioLogoFit{%.2fmm}{%.2fmm}{%s}};"
                 % (X_IMG, y + IMG_MID, IMG_MM, IMG_MM, img))
    s += [
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, text=%s, "
        r"inner sep=0] at (%.1f,%.2f) {%s};" % (name_col, X_NR, y, esc(net.tid[e])),
        r"\node[anchor=base west, font=\SemioSans\fontsize{6.4pt}{6.6pt}\selectfont, text=%s, "
        r"inner sep=0] at (%.1f,%.2f) {%s};" % (name_col, X_NAME, y, _clip(net.raw.name(e), NAME_MAX)),
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};" % (X_CODE, y, _code(rec)),
        r"\node[anchor=base west, font=\SemioSans\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};"
        % (X_REL, y, _clip(rec.get("relevanz") or "", REL_MAX)),
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-border-normal, inner sep=0] at (%.1f,%.2f) {%s};" % (X_Q, y, q),
    ]
    return s


def _edge_row(net, kante, y, qnum):
    """One relationship, always with its description. A prior version
    suppressed it for actor-to-building edges on the theory that the shared
    thing IS the other endpoint (`U04 -> P1, Entwurf`) -- true for most, but
    not all: 22 of 312 name the specific discipline/component/project that
    Art and the endpoint alone do not ("Cleveland lieferte wiederverwendeten
    Stahl für Holbein Gardens"), and those were lost along with the rest.
    Every one of the 268 drawn edges has a description in the data; print it."""
    a, b = kante["pair"]
    if kante.get("richtung") == "B→A":
        a, b = b, a
    # ASCII, same reason as EDGE_COLS above: \textrightarrow{} has no glyph
    # in SemioMono. "--"/"->" are plain text, safe unescaped.
    pfeil = "--" if kante.get("richtung") == "—" else "->"
    paar = "%s %s %s" % (esc(net.tid.get(a, "?")), pfeil, esc(net.tid.get(b, "?")))
    besch = kante.get("beschreibung") or ""
    q = qnum.get(kante.get("evidence_url") or "", "")
    return [
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-foreground, inner sep=0] at (%.1f,%.2f) {%s};" % (X_VON, y, paar),
        r"\node[anchor=base west, font=\SemioSans\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};"
        % (X_ART, y, esc(kante.get("beziehungsart") or "")),
        r"\node[anchor=base west, font=\SemioSans\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-text-normal, inner sep=0] at (%.1f,%.2f) {%s};"
        % (X_BESCH, y, _clip(besch, BESCH_MAX)),
        r"\node[anchor=base west, font=\SemioMono\fontsize{5.8pt}{6pt}\selectfont, "
        r"text=semio-chrome-border-normal, inner sep=0] at (%.1f,%.2f) {%s};" % (X_QK, y, q),
    ]


def _legend() -> str:
    parts = [r"\textbf{%s}~%s" % (k, esc(GROUP_LABEL[k])) for k in sorted(GROUP_LABEL)]
    return r" \textperiodcentered\ ".join(parts)


def load_kanten(path, net, redirects_path=None):
    """cc -> [relationship], only those whose BOTH endpoints are actually
    DRAWN -- not just known to the pipeline.

    Two ways a "known" edge can still not be drawn, both found by counting
    net.drawn against this function's own output on the same run and getting
    268 != 268 despite matching totals:

      1. Cross-border. partition() only draws an edge whose two endpoints
         share a panel; an edge between e.g. a BE actor and an SE project is
         a real classified relationship but is never drawn anywhere. Checking
         against `set(net.tid)` (every node the pipeline knows) missed this --
         it has to be `net.drawn`.
      2. Merge redirects. The strict review merged duplicate eids
         (merge_redirects_strict.json); a classification written against the
         PRE-merge eid otherwise joins against nothing once the drawn graph
         only knows the canonical one.

    Fixing both together: canonicalize eids through the redirect map BEFORE
    membership-testing against net.drawn, whose keys are already canonical.
    """
    if not path:
        return {}
    with io.open(path, encoding="utf-8") as f:
        data = json.load(f)
    redirects = {}
    if redirects_path:
        with io.open(redirects_path, encoding="utf-8") as f:
            redirects = json.load(f)

    def canon(eid):
        return redirects.get(eid, eid)

    drawn_pairs = {tuple(sorted(pair)) for pair in net.drawn}
    by_cc = collections.defaultdict(list)
    for k in data.values():
        if k.get("entfernen"):
            continue
        a, b = k.get("pair", (None, None))
        a, b = canon(a), canon(b)
        if tuple(sorted((a, b))) in drawn_pairs:
            k = dict(k, pair=[a, b])
            by_cc[k["cc"]].append(k)
    for cc in by_cc:
        by_cc[cc].sort(key=lambda k: (net.tid.get(k["pair"][0], ""), net.tid.get(k["pair"][1], "")))
    return by_cc


def build_grid_fragment(net, out_path, klassifikation_path=None,
                        kanten_path=None, images=None, merge_redirects_path=None):
    kl = load_klassifikation(klassifikation_path) if klassifikation_path else {}
    kanten = load_kanten(kanten_path, net, merge_redirects_path)
    items = []   # ("head"|"band", label, cc) | ("row", eid, is_person) | ("kante", k)
    quellen = []  # (cc, [urls in print order])
    qnum = {}     # url -> number, restarted per country
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
                       % (CC_NAME.get(cc, cc), len(orgs), len(projs), len(persons)), cc))
        ordered = sorted(orgs + projs, key=lambda e: net.raw.name(e).lower())
        # 🔢 Quellennummern laufen je Land neu und folgen der Druckreihenfolge,
        # damit die Nummer in der Zeile ohne Suchen in der Landesliste steht.
        seen = {}
        for e in ordered:
            url = (kl.get(e) or {}).get("beleg_url") or ""
            if url and url not in seen:
                seen[url] = len(seen) + 1
        for k in kanten.get(cc, []):
            url = k.get("evidence_url") or ""
            if url and url not in seen:
                seen[url] = len(seen) + 1
        qnum.update(seen)
        quellen.append((cc, sorted(seen, key=seen.get)))
        for e in ordered:
            items.append(("row", e, False))
        for e in persons:
            items.append(("row", e, True))
        ks = kanten.get(cc, [])
        if ks:
            items.append(("band", "Beziehungen \\textperiodcentered\\ %d" % len(ks), cc))
            for k in ks:
                items.append(("kante", k, cc))

    out = [r"\section{Akteurstabellen nach Land}", "",
           r"{\SemioSans\fontsize{7.6pt}{9.5pt}\selectfont ID = Typ-Buchstabe + laufende Nummer je Land "
           r"(z.\,B. \textbf{M07}) \textendash\ identisch mit der Kreis-Beschriftung im zugeh\"origen "
           r"Netzdiagramm (Kap. Akteursnetze). "
           r"\textbf{Q} = Quellennummer, Liste am Ende des jeweiligen Landes.\\[1mm]"
           r"Rolle nach Gruppen der Klassifikation: " + _legend() + r"\\[2mm]}",
           r"\clearpage", r"\newgeometry{left=1.2cm, right=1.2cm, top=1.5cm, bottom=1.5cm}"]

    pages, page, count = [], [], 0
    for it in items:
        if count >= ROWS_PER_PAGE:
            pages.append(page); page = []; count = 0
        page.append(it)
        count += 1
    if page:
        pages.append(page)

    # 🧭 Laufender Kolumnentitel: welche Laender auf dieser Seite stehen. Der
    # bisherige Titel "Tabelle 3/10" half beim Nachschlagen nicht -- der Weg
    # ist immer Panel -> ID -> Land, also muss das Land oben stehen.
    cur_cc = None
    page_ccs = []
    for chunk in pages:
        ccs = []
        for it in chunk:
            if it[0] == "head":
                cur_cc = it[2]
            if cur_cc and cur_cc not in ccs:
                ccs.append(cur_cc)
        page_ccs.append(ccs)

    # 🧷 Ob eine Seite im Knoten- oder im Beziehungsband beginnt, entscheidet,
    # welcher Spaltenkopf oben stehen muss. Ohne das traegt eine Seite, die
    # mitten im Band anfaengt, die falschen Ueberschriften.
    starts_in_band = []
    in_band = False
    for chunk in pages:
        starts_in_band.append(in_band)
        for it in chunk:
            if it[0] == "band":
                in_band = True
            elif it[0] == "head":
                in_band = False

    for pi, chunk in enumerate(pages):
        title = r" \textendash\ ".join(esc(CC_NAME.get(c, c)) for c in page_ccs[pi]) or "Akteurstabelle"
        s = [r"\begin{Figure}[title={%s}, break=false]" % title,
             r"\begin{tikzpicture}[semio, x=1mm, y=-1mm]"]
        s += _hdr(0.0, EDGE_COLS if starts_in_band[pi] else NODE_COLS)
        y = 5.0
        for it in chunk:
            if it[0] in ("head", "band"):
                # Ueberschriften auf X_NR gesetzt, nicht auf 0 -- jede
                # Datenspalte beginnt bei X_NR (5.5), eine Ueberschrift bei 0
                # haengt 5.5 mm links aus dem Raster.
                s.append(r"\node[anchor=base west, font=\SemioSans\fontsize{7.6pt}{7.8pt}\selectfont, "
                          r"text=semio-chrome-foreground, inner sep=0] at (%.1f,%.2f) {%s};" % (X_NR, y, it[1]))
                s.append(r"\draw[draw=semio-chrome-border-normal, line width=0.5pt] "
                          r"(0,%.2f) -- (181,%.2f);" % (y + 1.0, y + 1.0))
                y += PITCH + 1.2
                # Jeder Block bekommt seinen eigenen Spaltenkopf. Vorher nur
                # nach "band" gesetzt -- eine Seite, die im Kantenband beginnt
                # und dann per "head" in ein neues Land wechselt, druckte den
                # folgenden Knotenblock nie mit Kopf (Seiten 6, 9, 14).
                s += _hdr(y, EDGE_COLS if it[0] == "band" else NODE_COLS)
                y += PITCH + 0.6
            elif it[0] == "kante":
                s += _edge_row(net, it[1], y, qnum)
                y += PITCH
            else:
                s += _row(net, it[1], y, kl, qnum, images, dim=it[2])
                y += PITCH
        s.append(r"\end{tikzpicture}")
        s.append(r"\end{Figure}")
        out.append("\n".join(s))
        out.append("")

    out.append(r"\clearpage")
    out.append(r"{\SemioSans\fontsize{6.4pt}{7.6pt}\selectfont")
    for cc, urls in quellen:
        if not urls:
            continue
        out.append(r"\textbf{%s}\\[0.5mm]" % esc(CC_NAME.get(cc, cc)))
        # \url handles its own escaping -- never run a URL through esc(),
        # which would rewrite every "/" as \SemioSlash{}.
        out.append(r" \textperiodcentered\ ".join(
            r"%d~\url{%s}" % (i + 1, u) for i, u in enumerate(urls)))
        out.append(r"\\[1.5mm]")
    out.append(r"}")
    out += [r"\clearpage", r"\restoregeometry"]

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out))
    return len(items), len(pages)
