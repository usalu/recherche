#!/usr/bin/env python3
"""Fetch PNG base64 chunks from Figma clientStorage via figma-console MCP."""
from __future__ import annotations

import asyncio
import base64
import json
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent


def tool_json(result) -> dict:
    text = ""
    if result.content:
        for block in result.content:
            if hasattr(block, "text"):
                text += block.text
    return json.loads(text) if text else {}


async def main(prefix: str, chunks: int, out: Path) -> int:
    params = StdioServerParameters(
        command="C:\\Program Files\\nodejs\\npx.cmd",
        args=["-y", "figma-console-mcp@latest"],
        env={"ENABLE_MCP_APPS": "true"},
    )
    parts: list[str] = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for i in range(chunks):
                code = f"""
const data = await figma.clientStorage.getAsync('{prefix}{i}');
return {{ index: {i}, data: data || '' }};
"""
                result = await session.call_tool(
                    "figma_execute", {"code": code, "timeout": 30000}
                )
                payload = tool_json(result)
                inner = payload.get("result", payload)
                if isinstance(inner, dict) and "result" in inner:
                    inner = inner["result"]
                data = inner.get("data", "")
                if not data:
                    print(f"missing chunk {i}", file=sys.stderr)
                    return 1
                parts.append(data)
                print(f"chunk {i}: {len(data)} chars")

            cleanup = f"""
const prefix = '{prefix}';
for (let i = 0; i < {chunks}; i++) {{
  await figma.clientStorage.deleteAsync(prefix + i);
}}
return {{ ok: true }};
"""
            await session.call_tool("figma_execute", {"code": cleanup, "timeout": 15000})

    b64 = "".join(parts)
    png = base64.b64decode(b64)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(png)
    print(f"Wrote {out} ({len(png):,} bytes)")
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("usage: _fetch_png_chunks_mcp.py <prefix> <chunks> <out.png>", file=sys.stderr)
        raise SystemExit(2)
    raise SystemExit(asyncio.run(main(sys.argv[1], int(sys.argv[2]), Path(sys.argv[3]))))
