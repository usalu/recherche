"""Export one Figma slide node to PNG via Desktop Bridge websocket."""
from __future__ import annotations

import argparse
import asyncio
import base64
import json
import sys
import time
import uuid
from pathlib import Path

try:
    import websockets
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "-q"])
    import websockets

BRIDGES = [
    "ws://127.0.0.1:9223",
    "ws://[::1]:9223",
    "ws://127.0.0.1:9224",
    "ws://[::1]:9224",
]
FILE_KEY = "NlkhCdjuc4ZtS21rqVJFcw"


def build_code(node_id: str, scale: float) -> str:
    return f"""
function bytesToBase64(bytes) {{
  let binary = '';
  const chunk = 0x8000;
  for (let i = 0; i < bytes.length; i += chunk) {{
    binary += String.fromCharCode(...bytes.subarray(i, i + chunk));
  }}
  return btoa(binary);
}}
const node = await figma.getNodeByIdAsync('{node_id}');
if (!node || !('exportAsync' in node)) return {{ error: 'not exportable', nodeId: '{node_id}' }};
const bytes = await node.exportAsync({{
  format: 'PNG',
  constraint: {{ type: 'SCALE', value: {scale} }},
}});
return {{ nodeId: '{node_id}', byteLength: bytes.length, pngBase64: bytesToBase64(bytes) }};
"""


async def run(node_id: str, out_path: Path, scale: float, timeout_ms: int) -> int:
    code = build_code(node_id, scale)
    last_err = None
    for bridge in BRIDGES:
        ws = None
        try:
            ws = await websockets.connect(bridge, max_size=64 * 1024 * 1024, open_timeout=8)
            deadline = time.time() + 10
            while time.time() < deadline:
                raw = await asyncio.wait_for(ws.recv(), timeout=2)
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
                    break

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
            recv_deadline = time.time() + (timeout_ms / 1000) + 20
            while time.time() < recv_deadline:
                raw = await asyncio.wait_for(ws.recv(), timeout=5)
                data = json.loads(raw)
                if data.get("id") != req_id:
                    continue
                if data.get("error"):
                    raise RuntimeError(data["error"])
                result = data.get("result", data)
                if isinstance(result, dict) and "result" in result:
                    result = result["result"]
                if result.get("error"):
                    raise RuntimeError(result["error"])
                png = base64.b64decode(result["pngBase64"])
                out_path.parent.mkdir(parents=True, exist_ok=True)
                out_path.write_bytes(png)
                print(f"OK {out_path} ({len(png):,} bytes)")
                return 0
            raise RuntimeError("timeout waiting for export")
        except Exception as exc:
            last_err = f"{bridge}: {exc}"
        finally:
            if ws is not None:
                try:
                    await ws.close()
                except Exception:
                    pass
    print(f"FAIL {node_id}: {last_err}", file=sys.stderr)
    return 1


def main() -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--node-id", required=True)
    p.add_argument("--out", required=True)
    p.add_argument("--scale", type=float, default=1.0)
    p.add_argument("--timeout-ms", type=int, default=180000)
    args = p.parse_args()
    return asyncio.run(run(args.node_id, Path(args.out), args.scale, args.timeout_ms))


if __name__ == "__main__":
    raise SystemExit(main())
