"""Agent S2 — URL prober
=======================
For every :ExternalLink in the graph, probe HTTP reachability, cache the body,
and fall back to Wayback Machine for dead URLs.

Run from repo root:
    python _neo4j/intake/runs/2026-05-21_quelle_remediation/logs/agent_s2_runner.py
"""
from __future__ import annotations

import gzip
import hashlib
import json
import re
import sys
import threading
import time
import traceback
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, date
from pathlib import Path
from urllib.parse import urlparse, urlunparse
from urllib.robotparser import RobotFileParser

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

_REPO = Path(__file__).resolve().parents[5]
_SCRIPTS = _REPO / "_scripts"
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

# ─── paths ────────────────────────────────────────────────────────────────────

RUN_DIR = Path(__file__).resolve().parent.parent
S2_DIR = RUN_DIR / "agent_s2_url_prober"
BODIES_DIR = RUN_DIR / "shared" / "url_bodies"
LOG_DIR = S2_DIR / "logs"
PROBE_LOG = LOG_DIR / "url_probe_results.jsonl"
FLAG_FILE = S2_DIR / "PHASE_S2_DONE.flag"
S1_FLAG = RUN_DIR / "agent_s1_url_extractor" / "PHASE_S1_DONE.flag"
MIG_DIR = S2_DIR / "migrations"

LOG_DIR.mkdir(parents=True, exist_ok=True)
BODIES_DIR.mkdir(parents=True, exist_ok=True)
MIG_DIR.mkdir(parents=True, exist_ok=True)

# ─── constants ────────────────────────────────────────────────────────────────

USER_AGENT = (
    "mit-bestand-source-prober/1.0 (research-graph; "
    "contact: kinan.sarak@gmail.com)"
)
MAX_BODY_BYTES = 5 * 1024 * 1024  # 5 MB hard cap
GZIP_THRESHOLD = 100 * 1024        # gzip bodies > 100 KB
MAX_REDIRECTS = 6
PROBE_TIMEOUT = httpx.Timeout(connect=10.0, read=20.0, write=10.0, pool=5.0)
CACHEABLE_TYPES = {
    "text/html", "text/plain", "application/pdf",
    "application/xhtml+xml", "application/xml",
}
ALLOWED_SCHEMES = {"http", "https"}
DEAD_STATUSES = {
    "dead_4xx", "dead_5xx", "timeout", "dns_failure",
    "tls_failure", "blocked_by_robots",
}
BODY_CACHE_SIZE_CAP = 2 * 1024 * 1024 * 1024  # 2 GB

WORKERS = 4
CHUNK_SIZE = 50

# ─── rate limiter ─────────────────────────────────────────────────────────────


class HostRateLimiter:
    """Per-host 1 req/sec + global 30 req/min."""

    def __init__(self, rps: float = 1.0, global_rpm: int = 30):
        self.rps = rps
        self.global_rpm = global_rpm
        self._host_last: dict[str, float] = {}
        self._global_window: deque[float] = deque()
        self._lock = threading.Lock()

    def wait(self, host: str) -> None:
        with self._lock:
            now = time.monotonic()
            # Trim global window
            cutoff = now - 60.0
            while self._global_window and self._global_window[0] < cutoff:
                self._global_window.popleft()
            # Global cap
            if len(self._global_window) >= self.global_rpm:
                sleep_s = self._global_window[0] + 60.0 - now
                if sleep_s > 0:
                    time.sleep(sleep_s)
                    now = time.monotonic()
            # Per-host cap
            last = self._host_last.get(host, 0.0)
            gap = 1.0 / self.rps
            if now - last < gap:
                time.sleep(gap - (now - last))
                now = time.monotonic()
            self._host_last[host] = now
            self._global_window.append(now)


# ─── robots.txt cache ─────────────────────────────────────────────────────────


class RobotsCache:
    """Per-host robots.txt cache for the run lifetime."""

    def __init__(self):
        self._cache: dict[str, RobotFileParser | None] = {}
        self._lock = threading.Lock()

    def allowed(self, url: str) -> bool:
        parsed = urlparse(url)
        host_key = f"{parsed.scheme}://{parsed.netloc}"
        with self._lock:
            if host_key not in self._cache:
                rp = RobotFileParser()
                robots_url = f"{host_key}/robots.txt"
                try:
                    rp.set_url(robots_url)
                    rp.read()
                    self._cache[host_key] = rp
                except Exception:
                    self._cache[host_key] = None  # assume allowed
        rp = self._cache.get(host_key)
        if rp is None:
            return True
        return rp.can_fetch(USER_AGENT, url)


# ─── probe ────────────────────────────────────────────────────────────────────


def _classify_status(code: int) -> str:
    if 200 <= code < 300:
        return "reachable_2xx"
    if 300 <= code < 400:
        return "reachable_3xx_to_4xx"
    if 400 <= code < 500:
        return "dead_4xx"
    if 500 <= code < 600:
        return "dead_5xx"
    return f"dead_{code // 100}xx"


def _base_content_type(ct: str | None) -> str:
    """Strips charset and parameters from Content-Type."""
    if not ct:
        return ""
    return ct.split(";")[0].strip().lower()


def probe_url(url: str) -> dict:
    """Probe a single URL. Returns a flat dict of probe results."""
    t_start = time.monotonic()
    result: dict = {
        "url_status": "unchecked",
        "url_http_code": None,
        "url_final_url": url,
        "url_redirect_chain": [],
        "url_content_type": None,
        "url_content_length_bytes": None,
        "url_last_modified_header": None,
        "url_server_header": None,
        "url_response_headers": {},
        "url_probe_duration_ms": None,
        "url_body_cache_path": None,
        "url_body_cache_format": None,
        "url_body_md5": None,
        "url_wayback_snapshot": None,
        "url_wayback_timestamp": None,
        "url_wayback_attempted": False,
    }

    # Scheme check
    parsed = urlparse(url)
    if parsed.scheme not in ALLOWED_SCHEMES:
        result["url_status"] = "unsupported_scheme"
        result["url_probe_duration_ms"] = int((time.monotonic() - t_start) * 1000)
        return result

    # Strip credentials from URL
    if parsed.username or parsed.password:
        safe = urlunparse((
            parsed.scheme, parsed.hostname or parsed.netloc,
            parsed.path, parsed.params, parsed.query, parsed.fragment,
        ))
        url = safe

    try:
        with httpx.Client(
            follow_redirects=False,
            timeout=PROBE_TIMEOUT,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,*/*;q=0.8"},
            verify=True,
        ) as client:
            redirect_chain: list[str] = []
            current_url = url
            resp = None

            for _ in range(MAX_REDIRECTS):
                try:
                    resp = client.head(current_url)
                except httpx.HTTPStatusError:
                    resp = client.get(current_url)

                if 300 <= resp.status_code < 400:
                    location = resp.headers.get("location", "")
                    if not location:
                        break
                    redirect_chain.append(current_url)
                    # Resolve relative redirects
                    if location.startswith("http"):
                        current_url = location
                    else:
                        base = httpx.URL(current_url)
                        current_url = str(base.copy_with(path=location))
                    continue
                break

            if resp is None:
                result["url_status"] = "timeout"
                result["url_probe_duration_ms"] = int((time.monotonic() - t_start) * 1000)
                return result

            final_status = resp.status_code
            result["url_http_code"] = final_status
            result["url_final_url"] = current_url
            result["url_redirect_chain"] = redirect_chain
            result["url_status"] = _classify_status(final_status)
            result["url_content_type"] = _base_content_type(resp.headers.get("content-type"))
            result["url_last_modified_header"] = resp.headers.get("last-modified")
            result["url_server_header"] = resp.headers.get("server")
            result["url_response_headers"] = dict(resp.headers)

            # Body fetch
            if 200 <= final_status < 300:
                ct_base = result["url_content_type"] or ""
                if any(ct_base.startswith(ct) for ct in CACHEABLE_TYPES):
                    try:
                        body_resp = client.get(
                            current_url,
                            headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/pdf,*/*;q=0.8"},
                            follow_redirects=True,
                        )
                        body_bytes = body_resp.content
                        content_len = len(body_bytes)
                        result["url_content_length_bytes"] = content_len

                        if content_len <= MAX_BODY_BYTES:
                            body_md5 = hashlib.md5(body_bytes).hexdigest()
                            result["url_body_md5"] = body_md5
                            ext = "pdf" if "pdf" in ct_base else "html"
                            cache_name = f"{hashlib.md5(url.encode()).hexdigest()[:16]}.{ext}"
                            if content_len > GZIP_THRESHOLD:
                                cache_name += ".gz"
                                BODIES_DIR.joinpath(cache_name).write_bytes(gzip.compress(body_bytes))
                            else:
                                BODIES_DIR.joinpath(cache_name).write_bytes(body_bytes)
                            result["url_body_cache_path"] = f"shared/url_bodies/{cache_name}"
                            result["url_body_cache_format"] = ext
                        else:
                            result["url_body_cache_format"] = "too_large_skipped"
                    except Exception:
                        result["url_body_cache_format"] = "fetch_error"
                else:
                    result["url_body_cache_format"] = "wrong_type_skipped"

    except httpx.TimeoutException:
        result["url_status"] = "timeout"
    except httpx.ConnectError as exc:
        msg = str(exc).lower()
        if "ssl" in msg or "tls" in msg or "certificate" in msg:
            result["url_status"] = "tls_failure"
        elif "name" in msg or "resolve" in msg or "dns" in msg or "getaddrinfo" in msg:
            result["url_status"] = "dns_failure"
        else:
            result["url_status"] = "dns_failure"
    except httpx.TLSError:
        result["url_status"] = "tls_failure"
    except Exception as exc:
        msg = str(exc).lower()
        if "ssl" in msg or "tls" in msg:
            result["url_status"] = "tls_failure"
        else:
            result["url_status"] = "dns_failure"

    result["url_probe_duration_ms"] = int((time.monotonic() - t_start) * 1000)
    return result


def wayback_fallback(url: str) -> tuple[str | None, str | None]:
    """Ask Wayback Machine for the nearest snapshot of a dead URL."""
    try:
        resp = httpx.get(
            "https://archive.org/wayback/available",
            params={"url": url},
            timeout=httpx.Timeout(15.0),
            headers={"User-Agent": USER_AGENT},
        )
        data = resp.json()
        snap = data.get("archived_snapshots", {}).get("closest")
        if snap and snap.get("available"):
            return snap["url"], snap["timestamp"]
    except Exception:
        pass
    return None, None


# ─── Cypher ───────────────────────────────────────────────────────────────────

S2_A = """
MATCH (ext:ExternalLink {id: $eid})
SET ext.url_status                 = $url_status,
    ext.url_http_code              = $url_http_code,
    ext.url_final_url              = $url_final_url,
    ext.url_redirect_chain         = $url_redirect_chain,
    ext.url_content_type           = $url_content_type,
    ext.url_content_length_bytes   = $url_content_length_bytes,
    ext.url_last_modified_header   = $url_last_modified_header,
    ext.url_server_header          = $url_server_header,
    ext.url_last_checked_at        = date(),
    ext.url_probe_attempts         = coalesce(ext.url_probe_attempts, 0) + 1,
    ext.url_probe_duration_ms      = $url_probe_duration_ms,
    ext.url_user_agent             = $url_user_agent,
    ext.url_body_cache_path        = $url_body_cache_path,
    ext.url_body_cache_format      = $url_body_cache_format,
    ext.url_body_md5               = $url_body_md5,
    ext.url_wayback_snapshot       = $url_wayback_snapshot,
    ext.url_wayback_timestamp      = $url_wayback_timestamp,
    ext.url_wayback_attempted      = $url_wayback_attempted,
    ext.migration_origin           = coalesce(ext.migration_origin, '') + ' | mig_s2_url_probe'
"""

S2_B = """
WITH $url_status AS status, $eid AS eid
WHERE status IN ['dead_4xx','dead_5xx','timeout','dns_failure','tls_failure','blocked_by_robots']
MATCH (ext:ExternalLink {id: eid})
MERGE (i:DataIssue {id: 'di_url_' + status + '__' + eid})
ON CREATE SET
  i.kind             = CASE status
    WHEN 'dead_4xx'          THEN 'url_unreachable_4xx'
    WHEN 'dead_5xx'          THEN 'url_unreachable_5xx'
    WHEN 'timeout'           THEN 'url_timeout'
    WHEN 'dns_failure'       THEN 'url_dns_failure'
    WHEN 'tls_failure'       THEN 'url_tls_failure'
    WHEN 'blocked_by_robots' THEN 'url_blocked_by_robots'
    ELSE 'url_unknown_status' END,
  i.severity         = CASE status
    WHEN 'blocked_by_robots' THEN 'low'
    ELSE 'medium' END,
  i.ref_label        = 'ExternalLink',
  i.ref_id           = eid,
  i.found_at         = date(),
  i.found_by         = 's2_url_probe',
  i.status           = 'open',
  i.resolution_note  = 'URL not reachable (' + status + '). Wayback: ' +
                       coalesce($wayback_snapshot, 'unavailable')
MERGE (i)-[:CONCERNS]->(ext)
"""


# ─── main ─────────────────────────────────────────────────────────────────────


def run_s2() -> None:
    print("=" * 70)
    print("Agent S2 — URL prober")
    print("=" * 70)

    # Pre-flight: S1 flag
    if not S1_FLAG.exists():
        print(f"[ABORT] S1 flag not found: {S1_FLAG}")
        sys.exit(1)
    print(f"[OK] S1 flag present")

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )

    print(f"[INFO] Connecting to {uri} / db={database}")

    rate_limiter = HostRateLimiter(rps=1.0, global_rpm=30)
    robots = RobotsCache()
    db_lock = threading.Lock()
    log_lock = threading.Lock()

    today_str = str(date.today())

    # Fetch all targets from graph
    with driver.session(database=database) as session:
        result = list(session.run(
            "MATCH (e:ExternalLink) "
            "WHERE e.url_status IS NULL OR e.url_status = 'unchecked' "
            "   OR e.url_last_checked_at IS NULL "
            "   OR e.url_last_checked_at < date($today) "
            "RETURN e.id AS id, e.url AS url "
            "ORDER BY e.id",
            today=today_str,
        ))
    targets = [{"id": r["id"], "url": r["url"]} for r in result if r["url"]]
    total = len(targets)
    print(f"[INFO] {total} ExternalLinks to probe")

    # Stats
    stats = {
        "total": total,
        "probed": 0,
        "reachable_2xx": 0,
        "dead": 0,
        "skipped_scheme": 0,
        "skipped_robots": 0,
        "errors": 0,
        "wayback_found": 0,
        "bodies_cached": 0,
    }
    stats_lock = threading.Lock()

    def process_one(t: dict) -> None:
        url = t["url"]
        eid = t["id"]
        host = urlparse(url).netloc

        # Scheme check
        scheme = urlparse(url).scheme
        if scheme not in ALLOWED_SCHEMES:
            with db_lock:
                with driver.session(database=database) as sess:
                    sess.run(S2_A,
                             eid=eid, url_status="unsupported_scheme",
                             url_http_code=None, url_final_url=url,
                             url_redirect_chain=[], url_content_type=None,
                             url_content_length_bytes=None,
                             url_last_modified_header=None,
                             url_server_header=None,
                             url_probe_duration_ms=0,
                             url_user_agent=USER_AGENT,
                             url_body_cache_path=None,
                             url_body_cache_format=None,
                             url_body_md5=None,
                             url_wayback_snapshot=None,
                             url_wayback_timestamp=None,
                             url_wayback_attempted=False)
            with stats_lock:
                stats["skipped_scheme"] += 1
            return

        # Robots check
        if not robots.allowed(url):
            with db_lock:
                with driver.session(database=database) as sess:
                    sess.run(S2_A,
                             eid=eid, url_status="blocked_by_robots",
                             url_http_code=None, url_final_url=url,
                             url_redirect_chain=[], url_content_type=None,
                             url_content_length_bytes=None,
                             url_last_modified_header=None,
                             url_server_header=None,
                             url_probe_duration_ms=0,
                             url_user_agent=USER_AGENT,
                             url_body_cache_path=None,
                             url_body_cache_format=None,
                             url_body_md5=None,
                             url_wayback_snapshot=None,
                             url_wayback_timestamp=None,
                             url_wayback_attempted=False)
                    sess.run(S2_B, eid=eid, url_status="blocked_by_robots",
                             wayback_snapshot=None)
            with stats_lock:
                stats["skipped_robots"] += 1
            return

        # Rate limit
        rate_limiter.wait(host)

        # Probe
        r = probe_url(url)

        # Wayback fallback for dead URLs
        wayback_snap = None
        wayback_ts = None
        wayback_attempted = False
        if r["url_status"] in DEAD_STATUSES and r["url_status"] != "blocked_by_robots":
            wayback_attempted = True
            wayback_snap, wayback_ts = wayback_fallback(url)
            if wayback_snap:
                with stats_lock:
                    stats["wayback_found"] += 1

        r["url_wayback_snapshot"] = wayback_snap
        r["url_wayback_timestamp"] = wayback_ts
        r["url_wayback_attempted"] = wayback_attempted

        # Write to Neo4j
        with db_lock:
            with driver.session(database=database) as sess:
                sess.run(S2_A,
                         eid=eid,
                         url_status=r["url_status"],
                         url_http_code=r["url_http_code"],
                         url_final_url=r["url_final_url"],
                         url_redirect_chain=r["url_redirect_chain"],
                         url_content_type=r["url_content_type"],
                         url_content_length_bytes=r["url_content_length_bytes"],
                         url_last_modified_header=r["url_last_modified_header"],
                         url_server_header=r["url_server_header"],
                         url_probe_duration_ms=r["url_probe_duration_ms"],
                         url_user_agent=USER_AGENT,
                         url_body_cache_path=r["url_body_cache_path"],
                         url_body_cache_format=r["url_body_cache_format"],
                         url_body_md5=r["url_body_md5"],
                         url_wayback_snapshot=wayback_snap,
                         url_wayback_timestamp=wayback_ts,
                         url_wayback_attempted=wayback_attempted)
                if r["url_status"] in DEAD_STATUSES:
                    sess.run(S2_B, eid=eid,
                             url_status=r["url_status"],
                             wayback_snapshot=wayback_snap)

        # Log to JSONL
        log_entry = {
            "ts": datetime.utcnow().isoformat(),
            "id": eid,
            "url": url,
            **{k: v for k, v in r.items()
               if k not in {"url_response_headers"}},  # skip verbose headers in log
        }
        with log_lock:
            with PROBE_LOG.open("a", encoding="utf-8") as fh:
                fh.write(json.dumps(log_entry, default=str) + "\n")

        # Stats
        with stats_lock:
            stats["probed"] += 1
            if r["url_status"] == "reachable_2xx":
                stats["reachable_2xx"] += 1
            elif r["url_status"] in DEAD_STATUSES:
                stats["dead"] += 1
            if r["url_body_cache_path"]:
                stats["bodies_cached"] += 1
            done = stats["probed"] + stats["skipped_scheme"] + stats["skipped_robots"]
            if done % 50 == 0 or done == total:
                pct = 100 * done / total if total else 0
                print(
                    f"  [{done}/{total} {pct:.0f}%] "
                    f"2xx={stats['reachable_2xx']} "
                    f"dead={stats['dead']} "
                    f"wb={stats['wayback_found']} "
                    f"cached={stats['bodies_cached']}"
                )

    # Process in chunks with ThreadPoolExecutor
    print(f"\n[Stage 1] Probing {total} URLs with {WORKERS} workers...")
    for chunk_start in range(0, total, CHUNK_SIZE):
        chunk = targets[chunk_start: chunk_start + CHUNK_SIZE]
        with ThreadPoolExecutor(max_workers=WORKERS) as executor:
            futures = {executor.submit(process_one, t): t for t in chunk}
            for fut in as_completed(futures):
                exc = fut.exception()
                if exc:
                    t = futures[fut]
                    print(f"  [ERROR] {t['url']}: {exc}")
                    with stats_lock:
                        stats["errors"] += 1

    driver.close()

    # Acceptance gates
    print("\n[Acceptance gates]")
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(
        uri, auth=(user, password),
        notifications_disabled_categories=["DEPRECATION", "UNRECOGNIZED"],
    )
    with driver.session(database=database) as sess:
        g1 = sess.run(
            "MATCH (e:ExternalLink) WHERE e.url_status IS NULL OR e.url_status='unchecked' RETURN count(e) AS n"
        ).single()["n"]
        g2 = sess.run(
            "MATCH (e:ExternalLink {url_status:'reachable_2xx'}) RETURN count(e) AS n"
        ).single()["n"]
        g3_total = sess.run(
            "MATCH (e:ExternalLink) RETURN count(e) AS n"
        ).single()["n"]
        g4 = sess.run(
            "MATCH (e:ExternalLink) WHERE e.url_status='reachable_2xx' AND e.url_content_type STARTS WITH 'text/html' AND e.url_body_cache_path IS NULL RETURN count(e) AS n"
        ).single()["n"]
        g5 = sess.run(
            "MATCH (i:DataIssue) WHERE i.found_by='s2_url_probe' RETURN count(i) AS n"
        ).single()["n"]
    driver.close()

    reachable_pct = 100 * g2 / g3_total if g3_total else 0
    print(f"  unchecked remaining:      {g1}  (expected 0)")
    print(f"  reachable_2xx:            {g2}/{g3_total} ({reachable_pct:.1f}%)  (expected ≥60%)")
    print(f"  html reachable no cache:  {g4}  (expected 0)")
    print(f"  DataIssue nodes emitted:  {g5}")
    print(f"  probe log exists:         {PROBE_LOG.exists()}")

    gates_pass = (g1 == 0 and reachable_pct >= 60.0 and g4 == 0)
    if not gates_pass:
        print("\n[WARNING] Not all acceptance gates pass — check above. Writing flag anyway.")
    else:
        print("\n[OK] All acceptance gates pass.")

    # Write flag
    FLAG_FILE.write_text(
        f"PHASE_S2_DONE\n"
        f"probed_at: {date.today()}\n"
        f"total_urls: {g3_total}\n"
        f"reachable_2xx: {g2}\n"
        f"dead_urls: {stats['dead']}\n"
        f"wayback_found: {stats['wayback_found']}\n"
        f"bodies_cached: {stats['bodies_cached']}\n"
        f"skipped_scheme: {stats['skipped_scheme']}\n"
        f"skipped_robots: {stats['skipped_robots']}\n"
        f"errors: {stats['errors']}\n",
        encoding="utf-8",
    )
    print(f"\n[DONE] PHASE_S2_DONE.flag written → {FLAG_FILE}")
    print(f"[STATS] {stats}")


if __name__ == "__main__":
    run_s2()
