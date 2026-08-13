"""Table renderer: one \\SemioTableLong per whitelisted country, replacing
the legacy hand-drawn TikZ table + manual ROWS=62 pagination with the
existing auto-paginating longtable mechanism (semio-table.sty). This is a
DELIBERATE visual change (Stage 8, user-gated): native table chrome and
automatic page breaks replace the manual "Seite N/M" titles, and automatic
register numbering replaces the cross-reference-free plain heading.

Column layout is three named columns (ID, Name, Rollen), not TikZ pixel
offsets. Section rows (P -- Projekte, U -- Unternehmen, ..., E -- Personen)
are plain full-width \\multicolumn rows passed through \\SemioTableRow --
the SAME primitive \\SemioTableBandRow already uses inside the project
catalogue (semio-table.sty) -- so no new LaTeX mechanism is needed for this.

Marks (deg/dagger) reuse model.variants.node_role -- the SAME classification
the graph circles use -- instead of re-deriving new_eids/inferred membership
a second time.
"""
import collections

from ...data._identity import TYPE_LETTER
from ...mechanisms.countries import is_person
from ...model.variants import node_role, ATTESTED, HYPO
from .escape import esc, esct
from .vocab import CC_NAME, ROLE_SHORT, TYP_NAME_DE, TYP_ORDER

FRACS = "0.07,0.46,0.47"
NAME_MAX, ROLE_MAX = 62, 68

_MARK = {ATTESTED: r"\,\textdegree", HYPO: r"\,\textdagger"}

TABLE_LEGEND = (
    r"{\SemioSans\fontsize{7.6pt}{9.5pt}\selectfont ID = Typ-Buchstabe + laufende Nummer je Land "
    r"(z.\,B. \textbf{M07}) \textendash\ identisch mit der Kreis-Beschriftung im zugeh\"origen "
    r"Netzdiagramm (Kap. Akteursnetze). "
    r"\textdegree\ = neu erforscht \textperiodcentered\ \textdagger\ = Land erschlossen.\\[2mm]}")


def role_frequency(net) -> collections.Counter:
    """Global role frequency across ALL actors (not per-country) -- the sort
    key for a row's own roles, exactly matching the legacy `RF` scope."""
    rf = collections.Counter()
    for a in net.raw.actors:
        rf.update(net.raw.roles.get(a["eid"], ()))
    return rf


def _roles_cell(net, e, rf: collections.Counter) -> str:
    # secondary key `r` breaks ties deterministically -- net.raw.roles[e] is a
    # set, so without a tiebreak, equal-frequency roles sort in hash-random
    # per-process order (Stage 0 finding, same root cause as the legacy fix).
    rs = sorted(net.raw.roles.get(e, []), key=lambda r: (-rf.get(r, 0), r))
    if not rs:
        return r"\textcolor{semio-chrome-border-normal}{ohne}"
    parts, budget = [], ROLE_MAX
    for r in rs[:5]:
        label = ROLE_SHORT.get(r, r[:12]).replace("_", " ")
        if len(label) > budget:
            break
        parts.append(esc(label))
        budget -= len(label) + 3
    return r" \textperiodcentered\ ".join(parts) if parts else r"\textcolor{semio-chrome-border-normal}{ohne}"


def _entity_row(net, e, rf: collections.Counter, dim: bool = False) -> str:
    mark = _MARK.get(node_role(net, e), "")
    name_col = "semio-chrome-border-normal" if dim else "semio-chrome-foreground"
    id_cell = r"{\SemioMono %s}" % esc(net.tid[e])
    name_cell = r"\textcolor{%s}{%s%s}" % (name_col, esct(net.raw.name(e), NAME_MAX), mark)
    role_cell = _roles_cell(net, e, rf)
    return r"\SemioTableRow{%s & %s & %s}" % (id_cell, name_cell, role_cell)


def _section_row(label: str) -> str:
    # \multicolumn inside a \SemioTableLong body row throws "Misplaced \omit"
    # -- reproduced with a minimal probe down to a single lone multicolumn
    # row, so it is not a row-transition or column-count issue. The working
    # multicolumn precedent (\SemioTableBandRow, semio-table.sty's
    # ProjectCatalogue region) goes through a DIFFERENT render call
    # (\semio@project@long@render@call), not \semio@table@long@render, which
    # is what \SemioTableLong uses -- so that precedent doesn't transfer.
    # A plain N-column row with the label in the wide Name cell (not the
    # narrow ID cell -- a long label like "Materialhub / Bauteilbörse" wraps
    # to four lines in the ~7%-width ID column, confirmed by rendering) and
    # the rest blank stays inside the machinery every other
    # \SemioTableLong body row already uses.
    return r"\SemioTableRow{\cellcolor{semio-chrome-canvas}{} & \cellcolor{semio-chrome-canvas}\textbf{%s} & \cellcolor{semio-chrome-canvas}{}}" % esc(label)


def country_table(net, cc: str, rf: collections.Counter):
    pan = net.panels[cc]
    projs = sorted(pan.projects, key=lambda e: net.num[e])
    persons = sorted(
        (a["eid"] for a in net.raw.actors
         if net.res.cc.get(a["eid"]) == cc and is_person(net.raw, a["eid"])),
        key=lambda e: net.raw.name(e).lower(),
    )
    if not (pan.actors or projs or persons):
        return None

    rows = []
    if projs:
        rows.append(_section_row("P — Projekte"))
        for e in projs:
            rows.append(_entity_row(net, e, rf))

    by_typ = collections.defaultdict(list)
    for e in pan.actors:
        by_typ[net.raw.types.get(e, "Unbekannt")].append(e)
    for typ in TYP_ORDER:
        es = sorted(by_typ.get(typ, []), key=lambda e: net.raw.name(e).lower())
        if not es:
            continue
        rows.append(_section_row("%s — %s" % (TYPE_LETTER.get(typ, "X"), TYP_NAME_DE[typ])))
        for e in es:
            rows.append(_entity_row(net, e, rf))

    if persons:
        rows.append(_section_row("E — Personen (Einzelpersonen)"))
        for e in persons:
            rows.append(_entity_row(net, e, rf, dim=True))

    title = (r"%s \textperiodcentered\ %d Organisationen \textperiodcentered\ "
             r"%d Projekte \textperiodcentered\ %d Personen"
             % (CC_NAME.get(cc, cc), len(pan.actors), len(projs), len(persons)))
    return r"\SemioTableLong[text-size=7.2pt]{%s}{%s}{ID & Name & Rollen}{%s}" % (
        title, FRACS, "\n".join(rows))
