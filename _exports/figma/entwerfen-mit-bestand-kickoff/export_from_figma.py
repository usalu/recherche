#!/usr/bin/env python3
"""Export Kickoff Presentation slides from Figma Desktop as PNG (one file per slide)."""
from __future__ import annotations

import asyncio
import base64
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen

try:
    import websockets
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "-q"])
    import websockets

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "slides.json"
BRIDGES = ["ws://127.0.0.1:9223", "ws://[::1]:9223", "ws://localhost:9223"]
FILE_KEY = "NlkhCdjuc4ZtS21rqVJFcw"
PNG_SCALE = 2

EXPORT_ONE_JS = """
function bytesToBase64(bytes) {
  let binary = '';
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {
    binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  }
  return btoa(binary);
}

const slide = __SLIDE_JSON__;
const node = await figma.getNodeByIdAsync(slide.id);
if (!node || !('exportAsync' in node)) {
  return { number: slide.number, id: slide.id, name: slide.name, error: 'node not found or not exportable' };
}
const bytes = await node.exportAsync({
  format: 'PNG',
  constraint: { type: 'SCALE', value: __PNG_SCALE__ },
});
return {
  number: slide.number,
  id: slide.id,
  name: slide.name,
  width: node.width,
  height: node.height,
  pngBase64: bytesToBase64(bytes),
};
"""


def slide_slug(slide: dict) -> str:
    number = slide["number"]
    slug = re.sub(r"[^a-z0-9]+", "-", slide["name"].lower()).strip("-")
    slug = re.sub(r"^slide-\d+-?", "", slug) or "slide"
    return f"slide-{number:02d}-{slug}"


def figma_token() -> str | None:
    return os.environ.get("FIGMA_ACCESS_TOKEN") or os.environ.get("FIGMA_TOKEN")


def http_get(url: str, headers: dict | None = None) -> bytes:
    req = Request(url, headers=headers or {})
    with urlopen(req, timeout=120) as resp:
        return resp.read()


async def wait_for_bridge(max_wait_s: float = 90.0):
    deadline = time.time() + max_wait_s
    last_err = None
    while time.time() < deadline:
        for bridge in BRIDGES:
            try:
                ws = await websockets.connect(
                    bridge, max_size=64 * 1024 * 1024, open_timeout=5
                )
                hello_deadline = time.time() + 8
                while time.time() < hello_deadline:
                    try:
                        raw = await asyncio.wait_for(ws.recv(), timeout=2.0)
                    except asyncio.TimeoutError:
                        continue
                    data = json.loads(raw)
                    if data.get("type") == "SERVER_HELLO":
                        await ws.send(
                            json.dumps(
                                {
                                    "type": "FILE_INFO",
                                    "data": {
                                        "fileKey": FILE_KEY,
                                        "fileName": "Entwerfen mit Bestand",
                                        "editorType": "figma",
                                    },
                                }
                            )
                        )
                        print(f"Connected ({bridge})", flush=True)
                        return ws, bridge
            except Exception as exc:
                last_err = f"{bridge}: {type(exc).__name__}: {exc}"
        print("Waiting for Figma Desktop Bridge…", flush=True)
        await asyncio.sleep(2.0)
    raise RuntimeError(last_err or "Figma Desktop bridge unavailable")


async def execute_code(ws, code: str, timeout_ms: int = 120000) -> dict:
    req_id = f"png_{uuid.uuid4().hex[:8]}"
    await ws.send(
        json.dumps(
            {
                "id": req_id,
                "method": "EXECUTE_CODE",
                "params": {"code": code, "timeout": timeout_ms},
            }
        )
    )
    deadline = time.time() + (timeout_ms / 1000) + 15
    while time.time() < deadline:
        try:
            raw = await asyncio.wait_for(ws.recv(), timeout=5.0)
        except asyncio.TimeoutError:
            continue
        data = json.loads(raw)
        if data.get("id") != req_id:
            continue
        if data.get("error"):
            raise RuntimeError(data["error"])
        result = data.get("result", data)
        if isinstance(result, dict) and "result" in result:
            return result["result"]
        return result
    raise RuntimeError("no response from Figma bridge")


async def export_one_slide(slide: dict, retries: int = 3) -> Path:
    code = (
        EXPORT_ONE_JS.replace("__SLIDE_JSON__", json.dumps(slide, ensure_ascii=False))
        .replace("__PNG_SCALE__", str(PNG_SCALE))
    )
    last_err: Exception | None = None
    png_path = ROOT / f"{slide_slug(slide)}.png"

    for attempt in range(1, retries + 1):
        ws = None
        try:
            ws, _bridge = await wait_for_bridge(max_wait_s=30.0)
            result = await execute_code(ws, code)
            if result.get("error"):
                raise RuntimeError(result["error"])
            png_bytes = base64.b64decode(result["pngBase64"])
            png_path.write_bytes(png_bytes)
            print(f"  {png_path.name} ({len(png_bytes):,} bytes)", flush=True)
            return png_path
        except Exception as exc:
            last_err = exc
            print(f"    slide {slide['number']:02d} attempt {attempt}/{retries}: {exc}", flush=True)
            await asyncio.sleep(1.5)
        finally:
            if ws is not None:
                try:
                    await ws.close()
                except Exception:
                    pass

    raise RuntimeError(f"slide {slide['number']:02d}: {last_err}")


def export_via_rest(slides: list[dict], file_key: str) -> list[dict]:
    token = figma_token()
    if not token:
        raise RuntimeError("Set FIGMA_ACCESS_TOKEN or open Figma Desktop Bridge.")

    ids = ",".join(slide["id"] for slide in slides)
    query = urlencode({"ids": ids, "format": "png", "scale": str(PNG_SCALE)})
    images_url = f"https://api.figma.com/v1/images/{file_key}?{query}"
    payload = json.loads(http_get(images_url, {"X-Figma-Token": token}).decode("utf-8"))
    if payload.get("err"):
        raise RuntimeError(payload["err"])

    written = []
    for slide in slides:
        url = (payload.get("images") or {}).get(slide["id"])
        if not url:
            raise RuntimeError(f"No PNG URL for {slide['name']}")
        png_path = ROOT / f"{slide_slug(slide)}.png"
        png_path.write_bytes(http_get(url))
        print(f"  {png_path.name} ({png_path.stat().st_size:,} bytes)", flush=True)
        written.append({"number": slide["number"], "name": slide["name"], "png": png_path.name})
    return written


async def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    slides = sorted(manifest["slides"], key=lambda s: s["width"] * s["height"])
    print(f"Exporting {len(slides)} slides as PNG @ {PNG_SCALE}x…", flush=True)

    written = []
    try:
        for slide in slides:
            print(f"slide {slide['number']:02d} — {slide['name']}", flush=True)
            path = await export_one_slide(slide)
            written.append(
                {
                    "number": slide["number"],
                    "name": slide["name"],
                    "id": slide["id"],
                    "png": path.name,
                }
            )
        source = "figma-desktop-bridge"
    except Exception as bridge_err:
        print(f"Bridge failed ({bridge_err}); trying REST API…", flush=True)
        try:
            written = export_via_rest(manifest["slides"], manifest["fileKey"])
            source = "figma-rest-api"
        except (RuntimeError, HTTPError, URLError) as rest_err:
            print(
                "\nExport failed.\n"
                "Open Figma Desktop → Plugins → Development → Figma Desktop Bridge,\n"
                "or set FIGMA_ACCESS_TOKEN and rerun.\n",
                file=sys.stderr,
            )
            raise SystemExit(1) from rest_err

    (ROOT / "manifest.json").write_text(
        json.dumps(
            {
                "fileKey": manifest["fileKey"],
                "fileName": manifest["fileName"],
                "format": "png",
                "scale": PNG_SCALE,
                "source": source,
                "slides": written,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"Done — {len(written)} PNGs in {ROOT}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
