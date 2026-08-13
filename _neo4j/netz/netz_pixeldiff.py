"""PDF pixel-diff helper (Stage 0 harness component).

Usage: python netz_pixeldiff.py <pdf_a> <pdf_b> [--dpi 150] [--out prefix]
Renders each page of both PDFs at the same DPI and reports per-page
mean-absolute-difference and max-difference. Exits nonzero if any page
exceeds the tolerance (small tolerance absorbs anti-aliasing / font-hinting
jitter from re-rendering the same content, NOT real layout differences).
"""
import sys, io
import fitz


def render_pages(path, dpi):
    d = fitz.open(path)
    pages = []
    for p in d:
        pix = p.get_pixmap(dpi=dpi)
        pages.append((pix.width, pix.height, pix.samples))
    return pages


def diff(path_a, path_b, dpi=150, tol=2.0):
    pa = render_pages(path_a, dpi)
    pb = render_pages(path_b, dpi)
    if len(pa) != len(pb):
        print(f"PAGE COUNT MISMATCH: {path_a}={len(pa)}  {path_b}={len(pb)}")
        return False
    ok = True
    for i, ((wa, ha, sa), (wb, hb, sb)) in enumerate(zip(pa, pb)):
        if (wa, ha) != (wb, hb):
            print(f"page {i+1}: SIZE MISMATCH {wa}x{ha} vs {wb}x{hb}")
            ok = False
            continue
        n = min(len(sa), len(sb))
        diffs = [abs(sa[j] - sb[j]) for j in range(n)]
        mean_d = sum(diffs) / n
        max_d = max(diffs) if diffs else 0
        status = "OK" if mean_d <= tol else "DIFFERS"
        if mean_d > tol:
            ok = False
        print(f"page {i+1}: mean_abs_diff={mean_d:.4f} max_diff={max_d}  [{status}]")
    return ok


if __name__ == "__main__":
    a, b = sys.argv[1], sys.argv[2]
    dpi = 150
    if "--dpi" in sys.argv:
        dpi = int(sys.argv[sys.argv.index("--dpi") + 1])
    result = diff(a, b, dpi=dpi)
    print("RESULT:", "PASS" if result else "FAIL")
    sys.exit(0 if result else 1)
