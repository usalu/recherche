"""Quick Figma bridge connectivity test."""
from __future__ import annotations

import asyncio
import json
import sys
import time
import uuid

try:
    import websockets
except ImportError:
    import subprocess

    subprocess.check_call([sys.executable, "-m", "pip", "install", "websockets", "-q"])
    import websockets

BRIDGES = ["ws://127.0.0.1:9223", "ws://[::1]:9223"]
FILE_KEY = "NlkhCdjuc4ZtS21rqVJFcw"


async def main() -> int:
    code = "return { ok: true, file: figma.root.name, page: figma.currentPage.name };"
    for bridge in BRIDGES:
        try:
            async with websockets.connect(bridge, max_size=8 * 1024 * 1024, open_timeout=5) as ws:
                deadline = time.time() + 8
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
                req_id = f"ping_{uuid.uuid4().hex[:8]}"
                await ws.send(
                    json.dumps(
                        {
                            "id": req_id,
                            "method": "EXECUTE_CODE",
                            "params": {"code": code, "timeout": 10000},
                        }
                    )
                )
                deadline = time.time() + 15
                while time.time() < deadline:
                    raw = await asyncio.wait_for(ws.recv(), timeout=3)
                    data = json.loads(raw)
                    if data.get("id") == req_id:
                        print(json.dumps({"bridge": bridge, "response": data}, default=str))
                        return 0
        except Exception as exc:
            print(json.dumps({"bridge": bridge, "error": str(exc)}))
    return 1


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
