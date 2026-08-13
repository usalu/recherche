"""LaTeX text escaping. Verbatim port of net_lib.esc/esct -- byte-for-byte,
including the backslash-first replacement order and the \\SemioSlash{} macro
for slashes (a semio-core.sty break-opportunity helper, not general escaping;
LaTeX provides no general-purpose escaping macro, so this stays a renderer
concern -- see the Stage-2 architecture review)."""


def esc(s):
    s = s.replace("\\", r"\textbackslash{}").replace("&", r"\&").replace("%", r"\%")
    s = s.replace("_", r"\_").replace("#", r"\#").replace("$", r"\$").replace("~", r"\textasciitilde{}")
    s = s.replace("^", r"\textasciicircum{}").replace("{", r"\{").replace("}", r"\}")
    return s.replace("/", r"\SemioSlash{}")


def esct(s, maxlen):
    """Truncate the RAW string first, then escape -- never cut a LaTeX macro in half."""
    return esc(s[:maxlen])
