"""Full-width figure-page framing.

Stage 6: uses the GraphSpread environment from print/tex/semio-graph.sty --
a first-class package, registered in semio.cls -- instead of the Stage 4
spliced-preamble macro pair. GraphSpread wraps the exact same
\\clearpage/\\newgeometry/\\restoregeometry values every legacy generator
duplicated; the bare \\newgeometry still drops the class's
includehead/includefoot chrome-band reservation, exactly as before
(preserved, not introduced -- see semio-graph.sty's Spread region for the
opt-in `chrome=keep` fix).

GRAPH_LEGEND is still hand-written German prose describing the state model,
not yet the .sty's \\SemioGraphLegend (which draws real style swatches). That
adoption is a deliberate visual change and belongs with Stage 8's table
migration, which is user-gated.
"""

# Stage 8: adopts \SemioGraphLegend, which draws the actual state circles
# instead of describing them in prose that rots when a token changes. The
# framing sentences either side (which cluster gets drawn, what the number
# means) are not part of the state vocabulary, so they stay hand-written.
GRAPH_LEGEND = (r"{\SemioSans\fontsize{7.6pt}{9.5pt}\selectfont Ein Netz je Land \textendash\ "
                r"alle belegten Verbindungen. "
                r"\SemioGraphLegend{focal=Projekt, attested=neu recherchiert, hypo=Land erschlossen}. "
                r"Kr\"aftige Linie = Projektbeteiligung, blasse Linie = Organisationsbindung "
                r"(Konsortialpartner, Gr\"undung, Konzernbindung u.\,\"a.). "
                r"Zahl = Zeilennummer der zugeh\"origen Tabelle.\\[2mm]}")


def assemble_spread_fragment(section_title: str, legend: str, blocks: list) -> str:
    """Generic \\section + legend + full-width GraphSpread wrapper. Shared by
    the graph and table renderers -- GraphSpread has nothing graph-specific
    in its own definition (print/tex/semio-graph.sty is just a full-width-page
    geometry mechanism), so the table renderer reuses it instead of
    duplicating a second wide-page macro."""
    out = [r"\section{%s}" % section_title, legend, r"\begin{GraphSpread}"]
    for b in blocks:
        out.append(b)
        out.append("")
    out.append(r"\end{GraphSpread}")
    return "\n".join(out)


def assemble_graph_fragment(section_title: str, legend: str, figures: list) -> str:
    return assemble_spread_fragment(section_title, legend, figures)
