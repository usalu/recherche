"""Programme block: the strict review split 8 entries out of the actor
network because they are programmes (BAMB, ReCreate, FCRBE, ...), not
organisations -- they take no role in the reuse process, they coordinate or
fund it. Rendered as its own \\SemioTableLong, never mixed into the actor
figures/tables (table_grid.py, graph_tikz.py never see these eids at all,
since they are pruned from `aset` upstream of both).

Reads only the essence four fields (cc, name, rolle, relevanz) out of
sources.programme_path -- the full record also carries per-programme
evidence quotes and URLs, which belong to the review trail, not the print.
"""
import json

from .escape import esc

FRACS = "0.08,0.27,0.27,0.38"

LEGEND = (
    r"Programme sind länder- oder themenübergreifende Forschungs- und "
    r"Förderprogramme, keine Organisationen -- sie erhöhen weder die "
    r"Akteurszahl noch die Länder-Akteursrollen der vorangehenden Abschnitte."
)


def _row(rec: dict) -> str:
    # \SemioTableLong is a wrapping longtable (Stage 8), not a fixed TikZ
    # grid -- with only 8 rows there is no page-budget reason to truncate,
    # and cutting mid-word (confirmed on "FCRBE (Facilitating ... Building
    # El") produces the exact garbled-cell defect this project has hit and
    # fixed twice before. Escape only, no length cap.
    cc = esc(rec["cc"])
    name = esc(rec["name"])
    rolle = esc(rec["rolle"])
    relevanz = esc(rec["relevanz"])
    return r"\SemioTableRow{%s & %s & %s & %s}" % (cc, name, rolle, relevanz)


def build_programme_fragment(sources, out_path: str) -> int:
    with open(sources.programme_path, encoding="utf-8") as f:
        programmes = json.load(f)

    rows = sorted(programmes.values(), key=lambda r: (r["cc"], r["name"]))

    lines = [
        r"\section{Programme}",
        r"\label{anlage:akteursnetz-programme}",
        "",
        LEGEND,
        "",
        r"\SemioTableLong[text-size=7.6pt]{Programme}{%s}{Land & Programm & Rolle(n) & "
        r"Relevanz für Wiederverwendung}{%%" % FRACS,
    ]
    lines += ["  " + _row(r) for r in rows]
    lines += ["}", ""]

    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(lines))
    return len(rows)
