import json
import sys
from pathlib import Path

import pdfplumber
from pypdf import PdfReader


pdf_path = Path(sys.argv[1])
out_dir = Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

reader = PdfReader(str(pdf_path))
meta = {str(k): str(v) for k, v in (reader.metadata or {}).items()}

outline = []
try:
    for item in reader.outline:
        if isinstance(item, list):
            outline.append({"children": len(item)})
        else:
            outline.append(
                {
                    "title": getattr(item, "title", str(item)),
                    "page": reader.get_destination_page_number(item) + 1,
                }
            )
except Exception as exc:
    outline = [{"error": repr(exc)}]

pages = []
full_text = []
tables = []
with pdfplumber.open(str(pdf_path)) as pdf:
    for idx, page in enumerate(pdf.pages, start=1):
        text = page.extract_text(x_tolerance=2, y_tolerance=3, layout=False) or ""
        layout_text = page.extract_text(x_tolerance=2, y_tolerance=3, layout=True) or ""
        words = page.extract_words(x_tolerance=2, y_tolerance=3, use_text_flow=False)
        detected = []
        try:
            for table_idx, table in enumerate(page.extract_tables() or [], start=1):
                detected.append({"table": table_idx, "rows": table})
                tables.append({"page": idx, "table": table_idx, "rows": table})
        except Exception as exc:
            detected.append({"error": repr(exc)})
        pages.append(
            {
                "page": idx,
                "width": page.width,
                "height": page.height,
                "rotation": page.rotation,
                "chars": len(page.chars),
                "words": len(words),
                "images": len(page.images),
                "lines": len(page.lines),
                "rects": len(page.rects),
                "curves": len(page.curves),
                "tables": len(detected),
                "text_chars": len(text),
                "text": text,
                "layout_text": layout_text,
            }
        )
        full_text.append(f"\n===== PAGE {idx} =====\n{text}\n")

payload = {
    "file": str(pdf_path),
    "metadata": meta,
    "encrypted": reader.is_encrypted,
    "pages": len(reader.pages),
    "outline": outline,
    "page_stats": [{k: v for k, v in p.items() if k not in ("text", "layout_text")} for p in pages],
}

(out_dir / "document.json").write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
(out_dir / "pages.json").write_text(json.dumps(pages, ensure_ascii=False, indent=2), encoding="utf-8")
(out_dir / "tables.json").write_text(json.dumps(tables, ensure_ascii=False, indent=2), encoding="utf-8")
(out_dir / "text-flow.txt").write_text("".join(full_text), encoding="utf-8")

print(json.dumps(payload, ensure_ascii=False, indent=2))
