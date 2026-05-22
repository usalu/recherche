#!/usr/bin/env python3
"""Export slide PNGs via figma-console MCP (chunked to avoid payload timeouts)."""
from __future__ import annotations

import asyncio
import base64
import json
import re
import sys
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent
MANIFEST = ROOT / "slides.json"

STORE_JS = """
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
if (!node || !('exportAsync' in node)) return { error: 'not exportable', id: slide.id };
const bytes = await node.exportAsync({
  format: 'PNG',
  constraint: { type: 'SCALE', value: 1 },
});
const b64 = bytesToBase64(bytes);
const CHUNK = 350000;
const prefix = 'png_' + slide.id.replace(':', '_') + '_';
const chunks = Math.ceil(b64.length / CHUNK) || 1;
for (let i = 0; i < chunks; i++) {
  await figma.clientStorage.setAsync(prefix + i, b64.slice(i * CHUNK, (i + 1) * CHUNK));
}
return {
  id: slide.id,
  number: slide.number,
  name: slide.name,
  width: node.width,
  height: node.height,
  chunks,
  byteLength: bytes.length,
  prefix,
};
"""

FETCH_JS = """
const prefix = '__PREFIX__';
const index = __INDEX__;
const data = await figma.clientStorage.getAsync(prefix + index);
return { index, data: data || '' };
"""

CLEANUP_JS = """
const prefix = '__PREFIX__';
const chunks = __CHUNKS__;
for (let i = 0; i < chunks; i++) {
  await figma.clientStorage.deleteAsync(prefix + i);
}
return { ok: true };
"""


def slide_slug(slide: dict) -> str:
    number = slide["number"]
    slug = re.sub(r"[^a-z0-9]+", "-", slide["name"].lower()).strip("-")
    slug = re.sub(r"^slide-\d+-?", "", slug) or "slide"
    return f"slide-{number:02d}-{slug}"


def tool_json(result) -> dict:
    text = ""
    if result.content:
        text = getattr(result.content[0], "text", str(result.content[0]))
    if result.isError:
        raise RuntimeError(text or "MCP tool error")
    data = json.loads(text) if text.startswith("{") else json.loads(text)
    if isinstance(data, dict) and data.get("_mcp") == "figma-console-mcp":
        if data.get("error"):
            raise RuntimeError(data["error"])
        return data.get("result", data)
    return data


async def wait_bridge(session: ClientSession, seconds: int = 120) -> None:
    deadline = time.time() + seconds
    while time.time() < deadline:
        result = await session.call_tool("figma_diagnose", {"verbose": False})
        text = getattr(result.content[0], "text", "") if result.content else ""
        if "Desktop Bridge plugin connected" in text:
            print("Bridge connected.", flush=True)
            return
        print("Waiting for Figma Desktop Bridge…", flush=True)
        await asyncio.sleep(2)
    raise RuntimeError("Figma Desktop Bridge not connected after wait")


async def export_slide(session: ClientSession, slide: dict) -> Path:
    store_code = STORE_JS.replace("__SLIDE_JSON__", json.dumps(slide, ensure_ascii=False))
    meta = tool_json(
        await session.call_tool("figma_execute", {"code": store_code, "timeout": 180000})
    )
    if meta.get("error"):
        raise RuntimeError(meta["error"])

    prefix = meta["prefix"]
    parts: list[str] = []
    for i in range(int(meta["chunks"])):
        fetch_code = FETCH_JS.replace("__PREFIX__", prefix).replace("__INDEX__", str(i))
        chunk = tool_json(
            await session.call_tool("figma_execute", {"code": fetch_code, "timeout": 30000})
        )
        parts.append(chunk.get("data") or "")

    cleanup_code = CLEANUP_JS.replace("__PREFIX__", prefix).replace("__CHUNKS__", str(meta["chunks"]))
    await session.call_tool("figma_execute", {"code": cleanup_code, "timeout": 15000})

    png = base64.b64decode("".join(parts))
    out = ROOT / f"{slide_slug(slide)}.png"
    out.write_bytes(png)
    print(f"  {out.name} ({len(png):,} bytes)", flush=True)
    return out


async def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    slides = sorted(manifest["slides"], key=lambda s: s["width"] * s["height"])

    server_params = StdioServerParameters(
        command=r"C:\Program Files\nodejs\npx.cmd",
        args=["-y", "figma-console-mcp@latest"],
        env={"ENABLE_MCP_APPS": "true", "FIGMA_BRIDGE_PORT": "9223", "FIGMA_WS_PORT": "9223"},
    )

    written = []
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            await wait_bridge(session, 120)
            for slide in slides:
                print(f"slide {slide['number']:02d} — {slide['name']}", flush=True)
                path = await export_slide(session, slide)
                written.append(
                    {
                        "number": slide["number"],
                        "name": slide["name"],
                        "id": slide["id"],
                        "png": path.name,
                    }
                )

    (ROOT / "manifest.json").write_text(
        json.dumps(
            {
                "fileKey": manifest["fileKey"],
                "fileName": manifest["fileName"],
                "format": "png",
                "scale": 1,
                "source": "figma-console-mcp-chunked",
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
    try:
        raise SystemExit(asyncio.run(main()))
    except KeyboardInterrupt:
        raise SystemExit(130)
