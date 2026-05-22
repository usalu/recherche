"""Agent S2 - URL prober.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s2_url_prober/logs/agent_s2_runner.py

The runner probes each distinct due URL once, then writes the same probe result
to every due :ExternalLink node that carries that URL.
"""
from __future__ import annotations

import gzip
import hashlib
import json
import socket
import ssl
import sys
import time
from collections import Counter, defaultdict, deque
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import quote, urljoin, urlparse, urlunparse
from urllib.robotparser import RobotFileParser

import httpx
from neo4j import GraphDatabase

REPO_ROOT = Path(__file__).resolve().parents[6]
if str(REPO_ROOT / "_scripts") not in sys.path:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402

RUN_ROOT = Path(__file__).resolve().parents[1]
PHASE_ROOT = RUN_ROOT.parent
LOG_DIR = RUN_ROOT / "logs"
REPORT_DIR = RUN_ROOT / "reports"
MIG_DIR = RUN_ROOT / "migrations"
BODY_DIR = PHASE_ROOT / "shared" / "url_bodies"
PROBE_LOG = LOG_DIR / "url_probe_results.jsonl"
PROGRESS_LOG = LOG_DIR / "agent_s2_progress.log"
REPORT_FILE = REPORT_DIR / "agent_s2_report.md"
FLAG_FILE = RUN_ROOT / "PHASE_S2_DONE.flag"

DATABASE = "mit-bestand"
USER_AGENT = (
    "mit-bestand-source-prober/1.0 (research-graph; "
    "contact: kinan.sarak@gmail.com)"
)
ACCEPT = "text/html,application/xhtml+xml,text/plain,application/pdf,*/*;q=0.8"
MAX_REDIRECTS = 5
MAX_BODY_BYTES = 5 * 1024 * 1024
GZIP_THRESHOLD_BYTES = 100 * 1024
TOTAL_CACHE_BUDGET_BYTES = 2 * 1024 * 1024 * 1024
ALLOWED_BODY_TYPES = ("text/", "application/pdf", "application/xhtml+xml")

S2_A: str
S2_B: str


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def today_local_iso() -> str:
    return datetime.now().date().isoformat()


def md5_hex(value: str | bytes) -> str:
    data = value if isinstance(value, bytes) else value.encode("utf-8")
    return hashlib.md5(data).hexdigest()


def log(message: str) -> None:
    line = f"[{utc_now()}] {message}"
    print(line, flush=True)
    with PROGRESS_LOG.open("a", encoding="utf-8") as fp:
        fp.write(line + "\n")


def load_migration_statements() -> tuple[str, str]:
    text = (MIG_DIR / "mig_s2_url_probe.cypher").read_text(encoding="utf-8")
    statements: list[str] = []
    current: list[str] = []
    for raw_line in text.splitlines():
        line = raw_line.rstrip()
        current.append(line)
        if line.strip().endswith(";"):
            stmt = "\n".join(
                ln for ln in current if not ln.strip().startswith("//")
            ).strip()
            if stmt.endswith(";"):
                stmt = stmt[:-1].rstrip()
            if stmt:
                statements.append(stmt)
            current = []
    if len(statements) != 2:
        raise RuntimeError(f"Expected two S2 migration statements, got {len(statements)}")
    return statements[0], statements[1]


class RateLimiter:
    def __init__(self, host_interval: float = 1.0, global_rpm: int = 30) -> None:
        self.host_interval = host_interval
        self.global_window = 60.0
        self.global_max = global_rpm
        self.host_last: dict[str, float] = {}
        self.global_hits: deque[float] = deque()

    def wait(self, host: str) -> None:
        while True:
            now = time.monotonic()
            while self.global_hits and now - self.global_hits[0] >= self.global_window:
                self.global_hits.popleft()
            host_wait = 0.0
            if host in self.host_last:
                host_wait = max(0.0, self.host_interval - (now - self.host_last[host]))
            global_wait = 0.0
            if len(self.global_hits) >= self.global_max:
                global_wait = max(0.0, self.global_window - (now - self.global_hits[0]))
            wait_for = max(host_wait, global_wait)
            if wait_for <= 0.0:
                self.host_last[host] = now
                self.global_hits.append(now)
                return
            time.sleep(min(wait_for, 5.0))


def host_of(url: str) -> str:
    return (urlparse(url).hostname or "").lower()


def host_is_plausibly_resolvable(host: str) -> bool:
    if not host:
        return False
    if host in {"localhost"}:
        return True
    if host.startswith("www.") and host.count(".") == 1:
        return False
    if "." in host:
        return True
    if ":" in host:
        return True
    return False


def strip_credentials(url: str) -> tuple[str, bool]:
    parsed = urlparse(url)
    if "@" not in parsed.netloc:
        return url, False
    hostname = parsed.hostname or ""
    port = f":{parsed.port}" if parsed.port else ""
    cleaned = urlunparse((
        parsed.scheme,
        hostname + port,
        parsed.path,
        parsed.params,
        parsed.query,
        parsed.fragment,
    ))
    return cleaned, True


def base_content_type(headers: dict[str, str]) -> str | None:
    raw = headers.get("content-type") or headers.get("Content-Type")
    if not raw:
        return None
    return raw.split(";", 1)[0].strip().lower()


def content_type_allowed(content_type: str | None) -> bool:
    if not content_type:
        return False
    return content_type.startswith("text/") or content_type in {
        "application/pdf",
        "application/xhtml+xml",
    }


def safe_headers(headers: httpx.Headers | dict[str, str]) -> dict[str, str]:
    return {str(k).lower(): str(v)[:2000] for k, v in dict(headers).items()}


def classify_status(status_code: int, redirected: bool) -> str:
    if 200 <= status_code < 300:
        return "reachable_2xx"
    if 300 <= status_code < 400:
        return "reachable_2xx"
    if 400 <= status_code < 500:
        return "reachable_3xx_to_4xx" if redirected else "dead_4xx"
    if status_code >= 500:
        return "dead_5xx"
    return "unchecked"


def classify_exception(exc: Exception) -> str:
    if isinstance(exc, (httpx.TimeoutException, TimeoutError, socket.timeout)):
        return "timeout"
    if isinstance(exc, httpx.UnsupportedProtocol):
        return "unsupported_scheme"
    message = str(exc).lower()
    if isinstance(exc, httpx.ConnectError):
        if "ssl" in message or "tls" in message or isinstance(exc.__cause__, ssl.SSLError):
            return "tls_failure"
        if "name or service not known" in message or "getaddrinfo" in message:
            return "dns_failure"
        if "nodename nor servname" in message or "temporary failure in name resolution" in message:
            return "dns_failure"
        if "11001" in message:
            return "dns_failure"
    return "timeout"


@dataclass
class ProbeResult:
    original_url: str
    probe_url: str
    url_status: str
    url_http_code: int | None = None
    url_final_url: str | None = None
    url_redirect_chain: list[str] | None = None
    url_content_type: str | None = None
    url_content_length_bytes: int | None = None
    url_last_modified_header: str | None = None
    url_server_header: str | None = None
    url_response_headers: dict[str, str] | None = None
    url_probe_duration_ms: int = 0
    url_wayback_snapshot: str | None = None
    url_wayback_timestamp: str | None = None
    url_wayback_attempted: bool = False
    url_body_cache_path: str | None = None
    url_body_cache_format: str | None = None
    url_body_md5: str | None = None
    credential_stripped: bool = False
    error: str | None = None

    def params_for(self, external_link_id: str) -> dict[str, Any]:
        headers_json = json.dumps(self.url_response_headers or {}, sort_keys=True)
        return {
            "external_link_id": external_link_id,
            "url": self.original_url,
            "url_status": self.url_status,
            "url_http_code": self.url_http_code,
            "url_final_url": self.url_final_url,
            "url_redirect_chain": self.url_redirect_chain or [],
            "url_content_type": self.url_content_type,
            "url_content_length_bytes": self.url_content_length_bytes,
            "url_last_modified_header": self.url_last_modified_header,
            "url_server_header": self.url_server_header,
            "url_response_headers": headers_json,
            "url_probe_duration_ms": self.url_probe_duration_ms,
            "url_user_agent": USER_AGENT,
            "url_body_cache_path": self.url_body_cache_path,
            "url_body_cache_format": self.url_body_cache_format,
            "url_body_md5": self.url_body_md5,
            "url_wayback_snapshot": self.url_wayback_snapshot,
            "url_wayback_timestamp": self.url_wayback_timestamp,
            "url_wayback_attempted": self.url_wayback_attempted,
        }


def get_driver():
    uri, user, password, database = resolve_connection()
    db = database or DATABASE
    return GraphDatabase.driver(
        uri,
        auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    ), db


def get_targets(session) -> list[dict[str, Any]]:
    rows = session.run(
        """
        MATCH (e:ExternalLink)
        WHERE e.url IS NOT NULL
          AND (
            e.url_status IS NULL OR e.url_status = 'unchecked'
            OR e.url_last_checked_at IS NULL
            OR duration.inDays(date(e.url_last_checked_at), date()).days > 30
          )
          AND (e.url_last_checked_at IS NULL OR date(e.url_last_checked_at) <> date())
        RETURN e.url AS url, collect(e.id) AS ids, count(e) AS node_count
        ORDER BY url
        """
    )
    return [dict(row) for row in rows]


def get_counts(session) -> dict[str, Any]:
    status_rows = session.run(
        "MATCH (e:ExternalLink) RETURN coalesce(e.url_status, '<null>') AS status, count(e) AS c ORDER BY c DESC"
    ).data()
    total = session.run("MATCH (e:ExternalLink) RETURN count(e) AS c").single()["c"]
    unchecked = session.run(
        "MATCH (e:ExternalLink) WHERE e.url_status IS NULL OR e.url_status='unchecked' RETURN count(e) AS c"
    ).single()["c"]
    distinct_urls = session.run(
        "MATCH (e:ExternalLink) RETURN count(DISTINCT e.url) AS c"
    ).single()["c"]
    return {
        "total_external_links": total,
        "distinct_urls": distinct_urls,
        "unchecked_external_links": unchecked,
        "status_distribution": status_rows,
    }


def fetch_robots(
    client: httpx.Client,
    limiter: RateLimiter,
    url: str,
    robots_cache: dict[str, RobotFileParser | None],
) -> RobotFileParser | None:
    parsed = urlparse(url)
    host = parsed.hostname or ""
    if not host:
        return None
    cache_key = host.lower()
    if cache_key in robots_cache:
        return robots_cache[cache_key]

    robots_url = f"https://{host}/robots.txt"
    try:
        limiter.wait(host)
        resp = client.get(robots_url, timeout=10.0)
        if resp.status_code >= 400:
            robots_cache[cache_key] = None
            return None
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.parse(resp.text.splitlines())
        robots_cache[cache_key] = rp
        return rp
    except Exception:
        robots_cache[cache_key] = None
        return None


def allowed_by_robots(
    client: httpx.Client,
    limiter: RateLimiter,
    url: str,
    robots_cache: dict[str, RobotFileParser | None],
) -> bool:
    rp = fetch_robots(client, limiter, url, robots_cache)
    if rp is None:
        return True
    try:
        return rp.can_fetch(USER_AGENT, url)
    except Exception:
        return True


def request_with_retry(
    client: httpx.Client,
    limiter: RateLimiter,
    method: str,
    url: str,
    *,
    max_attempts: int = 3,
) -> httpx.Response:
    last_exc: Exception | None = None
    for attempt in range(max_attempts):
        limiter.wait(host_of(url))
        try:
            resp = client.request(method, url)
            if resp.status_code in {429, 503}:
                retry_after = resp.headers.get("retry-after")
                if retry_after:
                    try:
                        sleep_for = min(float(retry_after), 120.0)
                    except ValueError:
                        sleep_for = min(10.0 * (attempt + 1), 120.0)
                else:
                    sleep_for = min(2.0 ** attempt, 30.0)
                time.sleep(sleep_for)
                continue
            return resp
        except (httpx.TimeoutException, httpx.ConnectError) as exc:
            last_exc = exc
            time.sleep(min(2.0 ** attempt, 10.0))
    if last_exc:
        raise last_exc
    return resp


def probe_http(client: httpx.Client, limiter: RateLimiter, url: str) -> tuple[ProbeResult, bytes | None]:
    start = time.perf_counter()
    current = url
    redirect_chain: list[str] = []
    response_body: bytes | None = None
    final_resp: httpx.Response | None = None

    try:
        for _hop in range(MAX_REDIRECTS + 1):
            try:
                resp = request_with_retry(client, limiter, "HEAD", current)
                if resp.status_code in {405, 403}:
                    resp = request_with_retry(client, limiter, "GET", current)
                    response_body = resp.content
            except httpx.HTTPError:
                resp = request_with_retry(client, limiter, "GET", current)
                response_body = resp.content

            final_resp = resp
            if 300 <= resp.status_code < 400 and resp.headers.get("location"):
                redirect_chain.append(current)
                current = urljoin(current, resp.headers["location"])
                response_body = None
                continue
            break

        assert final_resp is not None
        headers = safe_headers(final_resp.headers)
        content_type = base_content_type(headers)
        duration_ms = int((time.perf_counter() - start) * 1000)
        status = classify_status(final_resp.status_code, redirected=bool(redirect_chain))
        result = ProbeResult(
            original_url=url,
            probe_url=url,
            url_status=status,
            url_http_code=final_resp.status_code,
            url_final_url=str(final_resp.url) if final_resp.url else current,
            url_redirect_chain=redirect_chain,
            url_content_type=content_type,
            url_content_length_bytes=int(headers["content-length"]) if headers.get("content-length", "").isdigit() else None,
            url_last_modified_header=headers.get("last-modified"),
            url_server_header=headers.get("server"),
            url_response_headers=headers,
            url_probe_duration_ms=duration_ms,
        )
        return result, response_body
    except Exception as exc:
        duration_ms = int((time.perf_counter() - start) * 1000)
        return ProbeResult(
            original_url=url,
            probe_url=url,
            url_status=classify_exception(exc),
            url_final_url=url,
            url_redirect_chain=redirect_chain,
            url_probe_duration_ms=duration_ms,
            error=str(exc)[:500],
        ), None


def cache_body_if_allowed(
    client: httpx.Client,
    limiter: RateLimiter,
    result: ProbeResult,
    initial_body: bytes | None,
) -> None:
    content_type = result.url_content_type
    if result.url_status != "reachable_2xx":
        result.url_body_cache_format = None
        return
    if not content_type_allowed(content_type):
        result.url_body_cache_format = "wrong_type_skipped"
        return
    if result.url_http_code == 204:
        result.url_body_cache_format = "html" if content_type and content_type.startswith("text/") else "binary"
        return

    body = initial_body
    if body is None:
        try:
            resp = request_with_retry(client, limiter, "GET", result.url_final_url or result.probe_url)
            body = resp.content
            headers = safe_headers(resp.headers)
            result.url_response_headers = headers
            result.url_content_type = base_content_type(headers) or result.url_content_type
            result.url_last_modified_header = headers.get("last-modified") or result.url_last_modified_header
            result.url_server_header = headers.get("server") or result.url_server_header
        except Exception as exc:
            result.url_body_cache_format = "fetch_failed_skipped"
            result.error = f"body fetch failed: {exc}"[:500]
            return

    result.url_content_length_bytes = len(body)
    if len(body) > MAX_BODY_BYTES:
        result.url_body_cache_format = "too_large_skipped"
        return

    body_hash = md5_hex(body)
    url_hash = md5_hex(result.original_url)
    ctype = result.url_content_type or content_type or ""
    ext = "pdf" if "pdf" in ctype else "html" if ctype.startswith("text/") or ctype == "application/xhtml+xml" else "bin"
    cache_path = BODY_DIR / f"{url_hash}.{ext}"
    rel_path = f"shared/url_bodies/{cache_path.name}"
    payload = body
    if len(body) > GZIP_THRESHOLD_BYTES:
        cache_path = Path(str(cache_path) + ".gz")
        rel_path = f"{rel_path}.gz"
        payload = gzip.compress(body)

    cache_path.write_bytes(payload)
    meta = {
        "url": result.original_url,
        "fetched_at": utc_now(),
        "http_code": result.url_http_code,
        "content_type": result.url_content_type,
        "content_length": len(body),
        "content_encoding": result.url_response_headers.get("content-encoding") if result.url_response_headers else None,
        "redirect_chain": result.url_redirect_chain or [],
        "final_url": result.url_final_url,
        "body_md5": body_hash,
    }
    (BODY_DIR / f"{url_hash}.meta.json").write_text(
        json.dumps(meta, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    result.url_body_cache_path = rel_path
    result.url_body_cache_format = "pdf" if ext == "pdf" else "html" if ext == "html" else "binary"
    result.url_body_md5 = body_hash


def wayback_fallback_if_dead(client: httpx.Client, limiter: RateLimiter, result: ProbeResult) -> None:
    if result.url_status not in {"dead_4xx", "dead_5xx", "timeout", "dns_failure", "tls_failure"}:
        result.url_wayback_attempted = False
        return
    result.url_wayback_attempted = True
    try:
        api_url = "https://archive.org/wayback/available"
        limiter.wait("archive.org")
        resp = client.get(api_url, params={"url": result.original_url}, timeout=15.0)
        data = resp.json()
        snap = data.get("archived_snapshots", {}).get("closest")
        if snap and snap.get("available"):
            result.url_wayback_snapshot = snap.get("url")
            result.url_wayback_timestamp = snap.get("timestamp")
    except Exception as exc:
        result.error = f"{result.error or ''} wayback failed: {exc}"[:500]


def maybe_archive_live(client: httpx.Client, limiter: RateLimiter, url: str, enabled: bool) -> bool:
    if not enabled:
        return False
    try:
        save_url = f"https://web.archive.org/save/{quote(url, safe='')}"
        limiter.wait("web.archive.org")
        client.get(save_url, timeout=30.0)
        return True
    except Exception:
        return False


def enforce_cache_budget() -> tuple[int, int]:
    files = [p for p in BODY_DIR.iterdir() if p.is_file()]
    total = sum(p.stat().st_size for p in files)
    evicted = 0
    if total <= TOTAL_CACHE_BUDGET_BYTES:
        return total, evicted
    files.sort(key=lambda p: p.stat().st_mtime)
    for path in files:
        if total <= TOTAL_CACHE_BUDGET_BYTES:
            break
        size = path.stat().st_size
        path.unlink(missing_ok=True)
        total -= size
        evicted += 1
    return total, evicted


def append_probe_log(result: ProbeResult, node_ids: list[str], archived_live: bool) -> None:
    row = {
        "url": result.original_url,
        "normalised_url": result.probe_url,
        "external_link_ids": node_ids,
        "probed_at": utc_now(),
        "url_status": result.url_status,
        "http_code": result.url_http_code,
        "content_type": result.url_content_type,
        "final_url": result.url_final_url,
        "redirect_chain": result.url_redirect_chain or [],
        "user_agent": USER_AGENT,
        "duration_ms": result.url_probe_duration_ms,
        "body_cache_path": result.url_body_cache_path,
        "body_md5": result.url_body_md5,
        "wayback_attempted": result.url_wayback_attempted,
        "wayback_snapshot_url": result.url_wayback_snapshot,
        "wayback_timestamp": result.url_wayback_timestamp,
        "credential_stripped": result.credential_stripped,
        "archived_live": archived_live,
        "error": result.error,
    }
    with PROBE_LOG.open("a", encoding="utf-8") as fp:
        fp.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_credential_issue(session, eid: str, url: str) -> None:
    session.run(
        """
        MATCH (ext:ExternalLink {id: $eid})
        MERGE (i:DataIssue {id: 'di_url_with_credentials__' + $eid})
        ON CREATE SET
          i.kind = 'url_with_credentials',
          i.severity = 'medium',
          i.ref_label = 'ExternalLink',
          i.ref_id = $eid,
          i.url = $url,
          i.found_at = date(),
          i.found_by = 's2_url_probe',
          i.status = 'open',
          i.resolution_note = 'URL contained credentials; probe stripped credentials before request.',
          i.migration_origin = 'mig_s2_url_probe'
        MERGE (i)-[:CONCERNS]->(ext)
        """,
        eid=eid,
        url=url,
    ).consume()


def persist_result(session, result: ProbeResult, node_ids: list[str]) -> None:
    for eid in node_ids:
        params = result.params_for(eid)
        session.run(S2_A, **params).consume()
        session.run(S2_B, **params).consume()
        if result.credential_stripped:
            write_credential_issue(session, eid, result.original_url)


def audit_gates(session) -> dict[str, Any]:
    gates = {}
    gates["unchecked_external_links"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.url_status IS NULL OR e.url_status='unchecked' RETURN count(e) AS c"
    ).single()["c"]
    gates["reachable_2xx"] = session.run(
        "MATCH (e:ExternalLink {url_status:'reachable_2xx'}) RETURN count(e) AS c"
    ).single()["c"]
    gates["dead_with_wayback"] = session.run(
        "MATCH (e:ExternalLink) WHERE e.url_status STARTS WITH 'dead_' AND e.url_wayback_snapshot IS NOT NULL RETURN count(e) AS c"
    ).single()["c"]
    gates["reachable_html_without_cache"] = session.run(
        """
        MATCH (e:ExternalLink)
        WHERE e.url_status='reachable_2xx'
          AND e.url_content_type STARTS WITH 'text/html'
          AND e.url_body_cache_path IS NULL
        RETURN count(e) AS c
        """
    ).single()["c"]
    gates["data_issue_counts"] = session.run(
        "MATCH (i:DataIssue) WHERE i.found_by='s2_url_probe' RETURN i.kind AS kind, count(i) AS c ORDER BY c DESC"
    ).data()
    gates["status_distribution"] = session.run(
        "MATCH (e:ExternalLink) RETURN e.url_status AS status, count(e) AS c ORDER BY c DESC"
    ).data()
    return gates


def top_problematic_hosts(results: list[ProbeResult], limit: int = 10) -> list[dict[str, Any]]:
    counts: Counter[str] = Counter()
    by_status: dict[str, Counter[str]] = defaultdict(Counter)
    for result in results:
        if result.url_status in {"dead_4xx", "dead_5xx", "reachable_3xx_to_4xx", "timeout", "dns_failure", "tls_failure"}:
            host = host_of(result.original_url) or "<no-host>"
            counts[host] += 1
            by_status[host][result.url_status] += 1
    return [
        {"host": host, "issues": count, "statuses": dict(by_status[host])}
        for host, count in counts.most_common(limit)
    ]


def write_report(
    start_counts: dict[str, Any],
    end_counts: dict[str, Any],
    gates: dict[str, Any],
    results: list[ProbeResult],
    cache_bytes: int,
    evicted_files: int,
    archive_live_enabled: bool,
) -> None:
    status_counter = Counter(r.url_status for r in results)
    wayback_count = sum(1 for r in results if r.url_wayback_snapshot)
    body_cached = sum(1 for r in results if r.url_body_cache_path)
    top_hosts = top_problematic_hosts(results)

    lines = [
        "# Agent S2 URL probe report",
        "",
        f"- Completed at UTC: `{utc_now()}`",
        f"- Distinct URLs probed this run: `{len(results)}`",
        f"- ExternalLink nodes at start: `{start_counts['total_external_links']}`",
        f"- Distinct URLs in graph: `{start_counts['distinct_urls']}`",
        f"- Body cache size: `{cache_bytes}` bytes",
        f"- Cache evicted files: `{evicted_files}`",
        f"- Proactive Wayback archive enabled: `{archive_live_enabled}`",
        f"- Body cache entries written: `{body_cached}`",
        f"- Wayback fallbacks found: `{wayback_count}`",
        "",
        "## Status Distribution This Run",
        "",
    ]
    for status, count in status_counter.most_common():
        lines.append(f"- `{status}`: {count}")
    lines.extend(["", "## Graph Gates", ""])
    lines.append(f"- Unchecked ExternalLinks: `{gates['unchecked_external_links']}`")
    lines.append(f"- Reachable 2xx ExternalLinks: `{gates['reachable_2xx']}`")
    lines.append(f"- Dead URLs with Wayback snapshot: `{gates['dead_with_wayback']}`")
    lines.append(f"- Reachable HTML without cache: `{gates['reachable_html_without_cache']}`")
    lines.extend(["", "## DataIssues", ""])
    if gates["data_issue_counts"]:
        for row in gates["data_issue_counts"]:
            lines.append(f"- `{row['kind']}`: {row['c']}")
    else:
        lines.append("- None")
    lines.extend(["", "## Top Problematic Hosts", ""])
    if top_hosts:
        for item in top_hosts:
            lines.append(f"- `{item['host']}`: {item['issues']} ({item['statuses']})")
    else:
        lines.append("- None")
    lines.extend(["", "## End Counts", ""])
    for row in end_counts["status_distribution"]:
        lines.append(f"- `{row['status']}`: {row['c']}")

    REPORT_FILE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_flag(
    gates: dict[str, Any],
    results: list[ProbeResult],
    cache_bytes: int,
    archive_live_enabled: bool,
) -> None:
    status_counter = Counter(r.url_status for r in results)
    payload = {
        "phase": "S2",
        "agent": "agent_s2_url_prober",
        "completed_at_utc": utc_now(),
        "verified": gates["unchecked_external_links"] == 0 and gates["reachable_html_without_cache"] == 0,
        "distinct_urls_probed": len(results),
        "status_counts_this_run": dict(status_counter),
        "wayback_fallbacks": sum(1 for r in results if r.url_wayback_snapshot),
        "body_cache_size_bytes": cache_bytes,
        "body_cache_files": len([p for p in BODY_DIR.iterdir() if p.is_file()]),
        "proactive_wayback_archive_enabled": archive_live_enabled,
        "acceptance_gates": gates,
    }
    FLAG_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False, default=str), encoding="utf-8")


def append_handoff_row(gates: dict[str, Any], results: list[ProbeResult], cache_bytes: int) -> None:
    handoff = REPO_ROOT / "_neo4j" / "QUELLE_REMEDIATION" / "HANDOFF_LOG.md"
    if not handoff.is_file():
        return
    status_counter = Counter(r.url_status for r in results)
    wayback_count = sum(1 for r in results if r.url_wayback_snapshot)
    mb = cache_bytes / (1024 * 1024)
    row = (
        f"| {datetime.now().astimezone().strftime('%Y-%m-%d %H:%M %z')[:-2]}:"
        f"{datetime.now().astimezone().strftime('%z')[-2:]} | agent_s2 | "
        f"{'PASS' if gates['unchecked_external_links'] == 0 else 'FAIL'} | "
        f"Probed {len(results)} distinct URLs; "
        f"reachable_2xx={status_counter.get('reachable_2xx', 0)}, "
        f"reachable_3xx_to_4xx={status_counter.get('reachable_3xx_to_4xx', 0)}, "
        f"dead_4xx={status_counter.get('dead_4xx', 0)}, "
        f"dead_5xx={status_counter.get('dead_5xx', 0)}, "
        f"timeout={status_counter.get('timeout', 0)}, "
        f"dns_failure={status_counter.get('dns_failure', 0)}, "
        f"blocked_by_robots={status_counter.get('blocked_by_robots', 0)}; "
        f"Wayback fallbacks={wayback_count}; body cache size={mb:.1f} MB |"
    )
    text = handoff.read_text(encoding="utf-8")
    placeholder = "| _<fill>_ | agent_s2 | _<…>_ | Probed <n> URLs;"
    if placeholder in text:
        text = text.replace(
            "| _<fill>_ | agent_s2 | _<…>_ | Probed <n> URLs; reachable_2xx=<n>, reachable_3xx_to_4xx=<n>, dead_4xx=<n>, dead_5xx=<n>, timeout=<n>, dns_failure=<n>, blocked_by_robots=<n>; Wayback fallbacks=<n>; body cache size=<n> MB |",
            row,
        )
    elif row not in text:
        marker = "## §4 S3"
        text = text.replace(marker, row + "\n\n" + marker)
    handoff.write_text(text, encoding="utf-8")


def run_s2(archive_live: bool = False) -> int:
    global S2_A, S2_B
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    BODY_DIR.mkdir(parents=True, exist_ok=True)
    S2_A, S2_B = load_migration_statements()

    s1_flag = PHASE_ROOT / "agent_s1_url_extractor" / "PHASE_S1_DONE.flag"
    if not s1_flag.is_file():
        raise SystemExit(f"S1 done flag missing: {s1_flag}")

    log("S2 starting - URL reachability probe")
    driver, database = get_driver()
    results: list[ProbeResult] = []
    limiter = RateLimiter(host_interval=1.0, global_rpm=30)
    robots_cache: dict[str, RobotFileParser | None] = {}
    headers = {"User-Agent": USER_AGENT, "Accept": ACCEPT}

    with driver.session(database=database) as session:
        start_counts = get_counts(session)
        targets = get_targets(session)
    log(
        "S2 target set: "
        f"{len(targets)} distinct due URLs across "
        f"{sum(t['node_count'] for t in targets)} ExternalLink nodes"
    )

    with httpx.Client(
        follow_redirects=False,
        timeout=httpx.Timeout(connect=10.0, read=20.0, write=20.0, pool=10.0),
        headers=headers,
        verify=True,
    ) as client:
        for index, target in enumerate(targets, start=1):
            original_url = target["url"]
            node_ids = list(target["ids"])
            parsed = urlparse(original_url)
            if parsed.scheme.lower() not in {"http", "https"}:
                result = ProbeResult(
                    original_url=original_url,
                    probe_url=original_url,
                    url_status="unsupported_scheme",
                    url_final_url=original_url,
                )
            else:
                probe_url, stripped = strip_credentials(original_url)
                probe_host = host_of(probe_url)
                if not host_is_plausibly_resolvable(probe_host):
                    result = ProbeResult(
                        original_url=original_url,
                        probe_url=probe_url,
                        url_status="dns_failure",
                        url_final_url=probe_url,
                        credential_stripped=stripped,
                        error=f"implausible host for public DNS: {probe_host}",
                    )
                    wayback_fallback_if_dead(client, limiter, result)
                elif not allowed_by_robots(client, limiter, probe_url, robots_cache):
                    result = ProbeResult(
                        original_url=original_url,
                        probe_url=probe_url,
                        url_status="blocked_by_robots",
                        url_final_url=probe_url,
                        credential_stripped=stripped,
                    )
                else:
                    result, initial_body = probe_http(client, limiter, probe_url)
                    result.original_url = original_url
                    result.probe_url = probe_url
                    result.credential_stripped = stripped
                    cache_body_if_allowed(client, limiter, result, initial_body)
                    wayback_fallback_if_dead(client, limiter, result)

            archived_live = maybe_archive_live(
                client,
                limiter,
                original_url,
                archive_live and result.url_status == "reachable_2xx",
            )
            with driver.session(database=database) as session:
                persist_result(session, result, node_ids)
            append_probe_log(result, node_ids, archived_live)
            results.append(result)

            if index == 1 or index % 25 == 0 or index == len(targets):
                log(
                    f"S2 progress {index}/{len(targets)} - "
                    f"{result.url_status} - {host_of(original_url)}"
                )

    cache_bytes, evicted_files = enforce_cache_budget()
    with driver.session(database=database) as session:
        gates = audit_gates(session)
        end_counts = get_counts(session)
    driver.close()

    write_report(
        start_counts,
        end_counts,
        gates,
        results,
        cache_bytes,
        evicted_files,
        archive_live,
    )
    write_flag(gates, results, cache_bytes, archive_live)
    append_handoff_row(gates, results, cache_bytes)

    log(f"S2 report written: {REPORT_FILE}")
    log(f"S2 flag written: {FLAG_FILE}")
    log(f"S2 complete - unchecked ExternalLinks: {gates['unchecked_external_links']}")
    return 0 if gates["unchecked_external_links"] == 0 else 1


def main() -> int:
    archive_live = "--archive-live" in sys.argv
    return run_s2(archive_live=archive_live)


if __name__ == "__main__":
    raise SystemExit(main())
