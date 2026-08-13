"""Rebuild the standalone harness head from the live report preamble.

Keeps the scratchpad harness in sync with zwischenbericht.tex so fragments are
tested against the same styles the report actually has.
"""
import io

SP = r"E:/recherche/_neo4j/netz"
REPORT = r"E:/semio/mit-bestand/bericht/zwischenbericht/zwischenbericht.tex"

MARKER = chr(92) + "begin{document}"

src = io.open(REPORT, encoding="utf-8").read()
pre = src.split(MARKER)[0]
io.open(SP + "/preamble.inc", "w", encoding="utf-8", newline="\n").write(pre)

B = chr(92)

# Harness shims: \SemioCellList/\SemioCellListInline are defined in the report
# *body* (just before \appendixinput), so a standalone fragment build has to
# supply them. \ProvideDocumentCommand means the report's own definitions win.
SHIM = (B + "ExplSyntaxOn\n"
        + B + "ProvideDocumentCommand " + B + "SemioCellList { O{;} m }\n"
        "  {\n"
        "    " + B + "seq_set_split:Nnn " + B + "l_tmpa_seq {#1} {#2}\n"
        "    " + B + "int_zero:N " + B + "l_tmpa_int\n"
        "    " + B + "seq_map_inline:Nn " + B + "l_tmpa_seq\n"
        "      {\n"
        "        " + B + "int_incr:N " + B + "l_tmpa_int\n"
        "        " + B + "int_compare:nNnT " + B + "l_tmpa_int > 1 { " + B + "par " + B + "noindent }\n"
        "        " + B + "hangindent=0.8em " + B + "hangafter=1\n"
        "        " + B + "textcolor{semio-chrome-border-normal}{" + B + "textendash}~%\n"
        "        " + B + "tl_trim_spaces:n {##1}%\n"
        "      }\n"
        "  }\n"
        + B + "ProvideDocumentCommand " + B + "SemioCellListInline { O{;} m }\n"
        "  {\n"
        "    " + B + "seq_set_split:Nnn " + B + "l_tmpa_seq {#1} {#2}\n"
        "    " + B + "int_zero:N " + B + "l_tmpa_int\n"
        "    " + B + "seq_map_inline:Nn " + B + "l_tmpa_seq\n"
        "      {\n"
        "        " + B + "int_incr:N " + B + "l_tmpa_int\n"
        "        " + B + "int_compare:nNnT " + B + "l_tmpa_int > 1\n"
        "          { " + B + "textcolor{semio-chrome-border-normal}{~" + B + "textperiodcentered}~ }\n"
        "        " + B + "tl_trim_spaces:n {##1}%\n"
        "      }\n"
        "  }\n"
        + B + "ExplSyntaxOff\n")

opener = (MARKER + "\n" + SHIM
          + B + "makemainmatter\n"
          + B + "part{Anlage BT}\n")
io.open(SP + "/head.tex", "w", encoding="utf-8", newline="\n").write(pre + opener)
print("head.tex rebuilt, %d chars; 'semio tree' occurrences: %d"
      % (len(pre) + len(opener), pre.count("semio tree")))
