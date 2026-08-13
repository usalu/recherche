import io, sys, os

SP = r"E:/recherche/_neo4j/netz"

def read(p):
    return io.open(p, encoding="utf-8").read()

def build(out_name, frags, extra_preamble=None):
    head = read(SP + "/head.tex")
    if extra_preamble:
        marker = chr(92) + "begin{document}"
        head = head.replace(marker, read(SP + "/" + extra_preamble) + marker, 1)
    body = "".join(read(SP + "/figs/" + f) for f in frags)
    tail = read(SP + "/tail.tex")
    dest = SP + "/figs/" + out_name
    io.open(dest, "w", encoding="utf-8", newline="\n").write(head + body + tail)
    print("wrote", dest)

if __name__ == "__main__":
    out = sys.argv[1]
    extra = None
    frags = []
    for a in sys.argv[2:]:
        if a.startswith("+"):
            extra = a[1:]
        else:
            frags.append(a)
    build(out, frags, extra)
