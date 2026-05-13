"""Shared Neo4j connection settings (MCP file + env overrides)."""

from __future__ import annotations

import json
import os
from pathlib import Path


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def load_mcp_neo4j_env() -> dict[str, str]:
    path = repo_root() / ".cursor" / "mcp.json"
    if not path.is_file():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    servers = data.get("mcpServers") or {}
    neo = servers.get("Neo4j-Official") or servers.get("neo4j-official")
    if not neo:
        return {}
    env = neo.get("env") or {}
    return {str(k): str(v) for k, v in env.items() if isinstance(v, str)}


def resolve_connection() -> tuple[str, str, str, str]:
    mcp = load_mcp_neo4j_env()
    uri = os.environ.get("NEO4J_URI", mcp.get("NEO4J_URI", "")).strip()
    user = (
        os.environ.get("NEO4J_USERNAME")
        or os.environ.get("NEO4J_USER")
        or mcp.get("NEO4J_USERNAME", "")
    ).strip()
    password = os.environ.get("NEO4J_PASSWORD", mcp.get("NEO4J_PASSWORD", "")).strip()
    database = (
        os.environ.get("NEO4J_DATABASE") or mcp.get("NEO4J_DATABASE") or "neo4j"
    ).strip()
    return uri, user, password, database
