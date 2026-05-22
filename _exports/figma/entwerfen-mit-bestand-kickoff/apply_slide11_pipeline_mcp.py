#!/usr/bin/env python3
"""Apply slide11_pipeline_cells.json to Figma via figma-console MCP execute (chunked)."""
from __future__ import annotations

import asyncio
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CELLS = ROOT / "slide11_pipeline_cells.json"

APPLY_JS = r"""
const cells = __CELLS_JSON__;
await figma.loadFontAsync({ family: 'Inter', style: 'Regular' });

function hex(h) {
  const c = h.replace('#','');
  return {
    r: parseInt(c.slice(0,2),16)/255,
    g: parseInt(c.slice(2,4),16)/255,
    b: parseInt(c.slice(4,6),16)/255,
  };
}

const results = [];
for (const cell of cells) {
  const old = await figma.getNodeByIdAsync(cell.nodeId);
  if (!old || !('width' in old)) {
    results.push({ nodeId: cell.nodeId, error: 'node missing' });
    continue;
  }
  const parent = old.parent;
  if (!parent || !('appendChild' in parent)) {
    results.push({ nodeId: cell.nodeId, error: 'no parent' });
    continue;
  }

  const pad = 12;
  const frame = figma.createFrame();
  frame.name = `Cell_${cell.row}_${cell.col}`;
  frame.x = old.x;
  frame.y = old.y;
  frame.resize(old.width, old.height);
  frame.fills = [{ type: 'SOLID', color: hex('1e1e1e') }];
  frame.strokes = [{ type: 'SOLID', color: hex('333333') }];
  frame.strokeWeight = 1;
  frame.cornerRadius = 6;
  frame.clipsContent = true;

  const text = figma.createText();
  text.fontName = { family: 'Inter', style: 'Regular' };
  text.fontSize = 11;
  text.lineHeight = { unit: 'PIXELS', value: 14 };
  text.fills = [{ type: 'SOLID', color: hex('e6e6e6') }];
  text.characters = cell.yaml;
  text.textAutoResize = 'HEIGHT';
  text.resize(old.width - pad * 2, 10);
  text.x = pad;
  text.y = pad;
  frame.appendChild(text);

  const neededH = Math.max(old.height, text.height + pad * 2);
  frame.resize(old.width, neededH);
  parent.appendChild(frame);
  old.remove();
  results.push({
    nodeId: cell.nodeId,
    newId: frame.id,
    row: cell.row,
    col: cell.col,
    h: Math.round(frame.height),
    chars: cell.yaml.length,
  });
}
return results;
"""


async def apply_chunk(cells: list[dict]) -> list[dict]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    code = APPLY_JS.replace("__CELLS_JSON__", json.dumps(cells, ensure_ascii=False))
    params = StdioServerParameters(
        command="C:\\Program Files\\nodejs\\npx.cmd",
        args=["-y", "figma-console-mcp@latest"],
        env={"ENABLE_MCP_APPS": "true"},
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(
                "figma_execute",
                {"code": code, "timeout": 60000},
            )
            content = result.content[0].text if result.content else "{}"
            return json.loads(content)


def main() -> int:
    cells = json.loads(CELLS.read_text(encoding="utf-8"))
    chunk_size = 6
    all_results = []
    for i in range(0, len(cells), chunk_size):
        chunk = cells[i : i + chunk_size]
        print(f"Applying cells {i}-{i + len(chunk) - 1}...", flush=True)
        try:
            res = asyncio.run(apply_chunk(chunk))
            all_results.extend(res if isinstance(res, list) else [res])
            print(json.dumps(res, ensure_ascii=False, indent=2))
        except Exception as exc:
            print(f"Chunk failed: {exc}", file=sys.stderr)
            return 1
    out = ROOT / "slide11_pipeline_apply_report.json"
    out.write_text(json.dumps(all_results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Done -> {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
