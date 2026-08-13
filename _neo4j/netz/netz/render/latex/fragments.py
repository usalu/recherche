"""Fragment file writer -- the one place that touches disk on the renderer
side. utf-8 + explicit newline="\\n" preserved (Windows default would write
\\r\\n, breaking the byte-diff goldens)."""
import io


def write_fragment(path: str, text: str):
    io.open(path, "w", encoding="utf-8", newline="\n").write(text)
