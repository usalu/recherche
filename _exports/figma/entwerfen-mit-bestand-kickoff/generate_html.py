#!/usr/bin/env python3
"""Regenerate iframe HTML wrappers pointing at PNG files."""
from __future__ import annotations

import html
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "slides.json"


def slide_slug(slide: dict) -> str:
    number = slide["number"]
    slug = re.sub(r"[^a-z0-9]+", "-", slide["name"].lower()).strip("-")
    slug = re.sub(r"^slide-\d+-?", "", slug) or "slide"
    return f"slide-{number:02d}-{slug}"


def render_html(slide: dict, png_name: str) -> str:
    title = f"Entwerfen mit Bestand — {slide['name']}"
    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)}</title>
  <style>
    html, body {{
      margin: 0;
      width: 100%;
      height: 100%;
      overflow: hidden;
      background: #001117;
    }}
    .slide-root {{
      width: 100%;
      height: 100%;
      display: flex;
      align-items: center;
      justify-content: center;
    }}
    .slide-root img {{
      display: block;
      width: 100%;
      height: 100%;
      object-fit: contain;
      object-position: center;
    }}
  </style>
</head>
<body>
  <div class="slide-root">
    <img src="{html.escape(png_name)}" alt="{html.escape(slide['name'])}" width="{slide['width']}" height="{slide['height']}">
  </div>
</body>
</html>
"""


def main() -> None:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    for slide in manifest["slides"]:
        base = slide_slug(slide)
        png_name = f"{base}.png"
        html_name = f"{base}.html"
        (ROOT / html_name).write_text(render_html(slide, png_name), encoding="utf-8")
        status = "ok" if (ROOT / png_name).exists() else "png missing"
        print(f"  {html_name} ({status})")


if __name__ == "__main__":
    main()
