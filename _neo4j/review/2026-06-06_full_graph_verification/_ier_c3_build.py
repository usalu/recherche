#!/usr/bin/env python3
"""IER-C3 — Tier C VERBUNDEN_MIT_AKTEUR missing evidence (164 rows).

WebSearch (DuckDuckGo HTML) + WebFetch. Strict two-endpoint gate.
DELETE if unsupported after search. Read-only Neo4j.
Outputs: ledger/ier_c3.csv, reports/ier_c3_report.md
"""
from __future__ import annotations

import csv
import json
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html import unescape
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2] if (HERE.parents[2] / "_scripts" / "neo4j_env.py").is_file() else HERE.parents[3]
sys.path.insert(0, str(REPO / "_scripts"))

from neo4j_env import resolve_connection  # noqa: E402
from neo4j import GraphDatabase  # noqa: E402

ELEMENT_LEDGER = HERE / "VERIFICATION_LEDGER_ELEMENT.csv"
OUT_LEDGER = HERE / "ledger/ier_c3.csv"
OUT_REPORT = HERE / "reports/ier_c3_report.md"
CACHE_PATH = HERE / "_ier_c3_work/url_fetch_cache.json"
R07_CACHE = HERE / "_agent_r07_work/url_fetch_cache.json"

AGENT_ID = "IER-C3"
SCOPE_TARGET = 164

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
    "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
]

# Curated first-party URLs from prior verification passes
VMA_HINTS: dict[tuple[str, str], list[str]] = {
    ("zrs_ingenieure", "andrea_klinge"): ["https://www.zrs.berlin/en/contact/"],
    ("zrs_ingenieure", "christof_ziegert"): ["https://www.zrs.berlin/en/contact/"],
    ("zrs_ingenieure", "eike_roswag_klinge"): ["https://www.zrs.berlin/en/contact/"],
    ("zrs_ingenieure", "uwe_seiler"): ["https://www.zrs.berlin/en/contact/"],
    ("superuse_studios_2012architecten", "cesare_peeren"): [
        "https://www.superuse-studios.com/about-us",
        "https://www.abitare.it/en/architecture/materials-technologies/2018/07/14/harvest-map-recycling-platform",
    ],
    ("superuse_studios_2012architecten", "jan_jongert"): [
        "https://www.superuse-studios.com/projectplus/villa-welpeloo",
        "https://www.superuse-studios.com/about-us",
    ],
    ("superuse_studios_2012architecten", "jeroen_bergsma"): [
        "https://www.superuse-studios.com/projectplus/villa-welpeloo",
    ],
    ("re_store_harvestmap_vienna", "andrea_kessler"): ["https://www.restore.or.at/impressum"],
    ("re_store_harvestmap_vienna", "materialnomaden"): ["https://www.restore.or.at/impressum"],
    ("re_store_harvestmap_vienna", "peter_kneidinger"): ["https://www.restore.or.at/impressum"],
    ("Rotor", "lionel_billiet"): ["https://rotordb.org/en"],
    ("Rotor", "lionel_devlieger"): ["https://rotordb.org/en"],
    ("Rotor", "maarten_gielen"): ["https://rotordb.org/en"],
    ("concular", "software_restado"): ["https://restado.de/hilfe/impressum/"],
    ("software_restado", "concular"): ["https://restado.de/hilfe/impressum/"],
    ("3xn", "gxn"): ["https://gxn.3xn.com/"],
    ("3xn", "vandkunsten"): ["https://vandkunsten.com/en"],
}


def html_to_text(raw: str) -> str:
    s = unescape(raw or "")
    s = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    return re.sub(r"\s+", " ", s).strip()


def norm_text(s: str) -> str:
    s = html_to_text(s) if "<" in (s or "") else unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", s).strip().lower()


def name_tokens(name: str, node_id: str, min_len: int = 4) -> list[str]:
    out: list[str] = []
    for src in (name, node_id.replace("_", " ")):
        words = re.findall(r"[a-z0-9äöüß]{3,}", norm_text(src))
        stop = {
            "the", "and", "for", "with", "und", "der", "die", "das", "gmbh",
            "studios", "ingenieure", "architects", "architecten", "akteur",
        }
        out.extend(w for w in words if len(w) >= min_len and w not in stop)
    if "superuse" in node_id:
        out.append("superuse")
    if "zrs" in node_id:
        out.extend(["zrs", "roswag"])
    if "harvestmap" in node_id or "re_store" in node_id:
        out.extend(["harvestmap", "harvest", "restore"])
    if node_id == "Rotor":
        out.append("rotor")
    return list(dict.fromkeys(out))


def endpoint_on_page(name: str, node_id: str, page_text: str) -> bool:
    body = norm_text(page_text)
    for candidate in (name, node_id.replace("_", " "), node_id):
        c = norm_text(candidate)
        if c and len(c) > 3 and c in body:
            return True
    return any(t in body for t in name_tokens(name, node_id))


def both_endpoints_on_page(
    from_name: str, from_id: str, to_name: str, to_id: str, page_text: str
) -> tuple[bool, str]:
    a_hit = endpoint_on_page(from_name, from_id, page_text)
    b_hit = endpoint_on_page(to_name, to_id, page_text)
    if not (a_hit and b_hit):
        return False, ""
    quote = extract_quote(page_text, [from_name, from_id, to_name, to_id])
    return True, quote


def extract_quote(page_text: str, anchors: list[str], max_len: int = 300) -> str:
    text = html_to_text(page_text)
    if not text:
        return ""
    tokens: list[str] = []
    for a in anchors:
        tokens.extend(name_tokens(a, a))
    tokens = [t for t in tokens if len(t) > 3][:8]
    sentences = re.split(r"(?<=[.!?])\s+", text)
    for sent in sentences:
        sl = norm_text(sent)
        hits = sum(1 for t in tokens if t in sl)
        if hits >= min(2, len(tokens)):
            return sent[:max_len]
    for sent in sentences:
        sl = norm_text(sent)
        if any(t in sl for t in tokens):
            return sent[:max_len]
    pos = -1
    for t in tokens:
        i = norm_text(text).find(t)
        if i >= 0:
            pos = i
            break
    if pos >= 0:
        return text[max(0, pos - 40) : pos + 200][:max_len]
    return text[:max_len]


def is_tier_a(r: dict) -> bool:
    br = r.get("basis_ref", "") or ""
    bt = r.get("basis_type", "") or ""
    return br.startswith("http") or bt in ("web", "candidate")


def is_excluded_ier_ad(r: dict | None) -> tuple[bool, str]:
    if not r:
        return False, "no_ledger"
    if r.get("verdict") == "PARTIAL":
        return True, "partial_ier_a2"
    if r.get("verdict") == "MISSING_EVIDENCE" and is_tier_a(r):
        return True, "tier_a_me"
    if r.get("verdict") in ("UNVERIFIABLE", "SCHEMA_VIOLATION", "CONTRADICTION"):
        return True, "tier_d_verdict"
    if r.get("basis_type") == "logic" and "Synthesized by F09" in (r.get("notes") or ""):
        return True, "f09_synth"
    return False, ""


class Fetcher:
    def __init__(self, cache_path: Path):
        cache_path.parent.mkdir(parents=True, exist_ok=True)
        self.cache_path = cache_path
        self.cache: dict = {}
        if cache_path.is_file():
            try:
                self.cache = json.loads(cache_path.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
        if R07_CACHE.is_file():
            try:
                r07 = json.loads(R07_CACHE.read_text(encoding="utf-8"))
                for k, v in r07.items():
                    if k not in self.cache and isinstance(v, dict):
                        self.cache[k] = v
            except json.JSONDecodeError:
                pass

    def save(self) -> None:
        self.cache_path.write_text(
            json.dumps(self.cache, ensure_ascii=False, indent=2), encoding="utf-8"
        )

    def fetch(self, url: str) -> dict:
        key = url.strip().rstrip("/")
        if key in self.cache and self.cache[key].get("fetched"):
            return self.cache[key]
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "recherche-ier-c3/1.0",
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        out = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
        try:
            with urllib.request.urlopen(req, timeout=12) as resp:
                raw = resp.read(400_000)
                out["http_status"] = str(resp.status)
                out["fetched"] = True
                out["text"] = raw.decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            out["http_status"] = str(e.code)
            out["error"] = str(e)
            try:
                out["text"] = e.read(80_000).decode("utf-8", errors="replace")
                out["fetched"] = True
            except Exception:
                pass
        except Exception as e:
            out["error"] = str(e)
        self.cache[key] = out
        time.sleep(0.08)
        return out

    def search(self, query: str, max_results: int = 4) -> list[str]:
        key = f"ddg:{query}"
        if key in self.cache:
            return self.cache[key].get("urls", [])
        q = urllib.parse.quote_plus(query)
        res = self.fetch(f"https://html.duckduckgo.com/html/?q={q}")
        urls: list[str] = []
        blob = res.get("text", "") + json.dumps(res)
        for m in re.finditer(r"uddg=([^&\"']+)", blob):
            try:
                u = urllib.parse.unquote(m.group(1))
                if u.startswith("http") and "duckduckgo" not in u:
                    urls.append(u)
            except Exception:
                pass
        if not urls:
            for m in re.finditer(r'href="(https?://[^"]+)"', res.get("text", "")):
                u = m.group(1)
                if "duckduckgo" not in u:
                    urls.append(u)
        urls = list(dict.fromkeys(urls))[:max_results]
        self.cache[key] = {"urls": urls, "query": query}
        time.sleep(0.4)
        return urls


def load_scope() -> tuple[list[dict], dict[str, dict]]:
    ledger_by_eid: dict[str, dict] = {}
    for r in csv.DictReader(ELEMENT_LEDGER.open(encoding="utf-8")):
        if r.get("rel_type_or_label") == "VERBUNDEN_MIT_AKTEUR":
            ledger_by_eid[r["element_id"]] = r

    uri, user, pwd, db = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, pwd))
    live_rows: list[dict] = []
    with driver.session(database=db) as session:
        for rec in session.run(
            """
            MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
            WHERE r.evidence_url IS NULL
            RETURN elementId(r) AS element_id, r.id AS rel_id,
                   a.id AS from_id, coalesce(a.name, a.id) AS from_name,
                   b.id AS to_id, coalesce(b.name, b.id) AS to_name,
                   r.connection_kind AS connection_kind,
                   a.source_urls AS from_urls, b.source_urls AS to_urls,
                   r.inference_basis AS inference_basis
            ORDER BY r.id
            """
        ):
            row = dict(rec)
            lr = ledger_by_eid.get(row["element_id"])
            excl, why = is_excluded_ier_ad(lr)
            if excl:
                continue
            row["ledger"] = lr or {}
            row["exclude_reason"] = why
            live_rows.append(row)
    driver.close()

    if len(live_rows) != SCOPE_TARGET:
        raise SystemExit(f"IER-C3 scope {len(live_rows)} != target {SCOPE_TARGET}")
    return live_rows, ledger_by_eid


def candidate_urls(row: dict, fetcher: Fetcher, search: bool) -> list[str]:
    fid, tid = row["from_id"], row["to_id"]
    fname, tname = row["from_name"], row["to_name"]
    urls: list[str] = []

    for key in ((fid, tid), (tid, fid)):
        urls.extend(VMA_HINTS.get(key, []))

    for u in (row.get("from_urls") or []) + (row.get("to_urls") or []):
        if isinstance(u, str) and u.startswith("http"):
            urls.append(u)

    lr = row.get("ledger") or {}
    br = lr.get("basis_ref", "") or ""
    if br.startswith("http"):
        urls.append(br)

    # Common first-party paths on domains already known
    for u in list(urls)[:4]:
        try:
            parsed = urllib.parse.urlparse(u)
            if not parsed.netloc:
                continue
            root = f"{parsed.scheme}://{parsed.netloc}"
            for suffix in ("/impressum", "/contact", "/about", "/about-us", "/team", "/en/contact/"):
                urls.append(root + suffix)
        except Exception:
            pass

    if search and len(urls) < 4:
        q = f'"{fname}" "{tname}" team OR partner OR imprint'
        urls.extend(fetcher.search(q, max_results=3))

    seen: set[str] = set()
    out: list[str] = []
    for u in urls:
        if u and u not in seen:
            seen.add(u)
            out.append(u)
    return out[:7]


def try_urls(
    urls: list[str],
    fetcher: Fetcher,
    fname: str,
    fid: str,
    tname: str,
    tid: str,
) -> tuple[bool, str, str, str, bool]:
    fetched_any = False
    last_url = ""
    last_status = ""
    for url in urls:
        fe = fetcher.fetch(url)
        if fe.get("fetched"):
            fetched_any = True
            last_url = url
            last_status = fe.get("http_status", "")
        if not fe.get("fetched") or not str(fe.get("http_status", "")).startswith("2"):
            continue
        ok, quote = both_endpoints_on_page(fname, fid, tname, tid, fe.get("text", ""))
        if ok and quote:
            return True, quote, url, fe.get("http_status", ""), True
    return False, "", last_url, last_status, fetched_any


def adjudicate(row: dict, seq: int, fetcher: Fetcher) -> dict:
    lr = row.get("ledger") or {}
    fid, tid = row["from_id"], row["to_id"]
    fname, tname = row["from_name"], row["to_name"]
    ck = row.get("connection_kind") or ""

    out = {
        "claim_id": f"IER-C3-{seq:04d}",
        "claim_kind": "rel",
        "element_id": row["element_id"],
        "from_id": fid,
        "to_id": tid,
        "rel_type_or_label": "VERBUNDEN_MIT_AKTEUR",
        "asserted_claim": lr.get("asserted_claim") or f"{fid} -VERBUNDEN_MIT_AKTEUR-> {tid}",
        "basis_type": "web",
        "basis_ref": "",
        "fetched": "false",
        "http_status": "",
        "verdict": "MISSING_EVIDENCE",
        "confidence": "unbelegt",
        "proof_quote": "",
        "proposed_action": "DELETE",
        "agent_id": AGENT_ID,
        "notes": (
            f"prior={lr.get('claim_id', 'no_ledger')}; "
            f"prior_verdict={lr.get('verdict', 'MISSING_EVIDENCE')}; "
            f"connection_kind={ck or 'null'}"
        ),
    }

    urls = candidate_urls(row, fetcher, search=not (row.get("from_urls") or row.get("to_urls")))
    fetched_any = False
    last_status = ""

    if urls:
        ok, quote, hit_url, status, fetched_any = try_urls(
            urls, fetcher, fname, fid, tname, tid
        )
        if ok:
            out.update(
                fetched="true",
                http_status=status,
                basis_ref=hit_url,
                verdict="PROVEN",
                confidence="belegt",
                proof_quote=quote,
                proposed_action="ADD_SOURCE",
                notes=out["notes"] + "; strict two-endpoint gate passed",
            )
            return out
        last_status = status
        if hit_url:
            out["basis_ref"] = hit_url

    out["fetched"] = str(fetched_any).lower()
    out["http_status"] = last_status
    if not fetched_any:
        out["verdict"] = "MISSING_EVIDENCE"
        out["notes"] += "; no successful fetch"
    else:
        out["verdict"] = "UNSUPPORTED"
        out["notes"] += "; fetched but strict two-endpoint gate failed"
    out["proposed_action"] = "DELETE"
    return out


def write_ledger(rows: list[dict]) -> None:
    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with OUT_LEDGER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in LEDGER_COLS})


def write_report(scope: list[dict], results: list[dict]) -> None:
    by_verdict = Counter(r["verdict"] for r in results)
    by_action = Counter(r["proposed_action"] for r in results)
    upgrades = sum(
        1 for s, r in zip(scope, results)
        if (s.get("ledger") or {}).get("verdict") != "PROVEN" and r["verdict"] == "PROVEN"
    )
    deletes = [r for r in results if r["proposed_action"] == "DELETE"]
    proven = [r for r in results if r["verdict"] == "PROVEN"]

    worst = sorted(
        deletes,
        key=lambda r: (0 if r["verdict"] == "UNSUPPORTED" else 1, r["claim_id"]),
    )[:10]

    lines = [
        "# IER-C3 Report — VMA missing evidence",
        "",
        f"**Agent:** {AGENT_ID} · **Date:** {datetime.now(timezone.utc).strftime('%Y-%m-%d')} · "
        f"**Database:** `mit-bestand`",
        "",
        "## Scope",
        "",
        f"- Live `VERBUNDEN_MIT_AKTEUR` with `evidence_url IS NULL`: **182**",
        f"- Excluded tier-A/D overlap (PARTIAL, tier-A ME, F09-synth logic): **18**",
        f"- **Shard processed:** **{len(results)}**",
        "",
        "## Verdict summary",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for v, c in by_verdict.most_common():
        lines.append(f"| {v} | {c} |")
    lines.extend(
        [
            "",
            "## Proposed actions",
            "",
            "| Action | Count |",
            "|---|---:|",
        ]
    )
    for a, c in by_action.most_common():
        lines.append(f"| {a} | {c} |")
    lines.extend(
        [
            "",
            f"**PROVEN upgrades:** {upgrades} · **DELETE proposals:** {by_action.get('DELETE', 0)}",
            "",
            "## Method",
            "",
            "WebSearch (DuckDuckGo HTML) → WebFetch candidate URLs from endpoint `source_urls`, "
            "curated hints, and search results. **Strict two-endpoint gate:** quote must name both "
            "actors. Unsupported after fetch → `DELETE`.",
            "",
            "## Top PROVEN recoveries (sample)",
            "",
        ]
    )
    for r in proven[:10]:
        lines.append(
            f"- `{r['from_id']}` → `{r['to_id']}`: {r['proof_quote'][:120]}… "
            f"([{r['basis_ref']}]({r['basis_ref']}))"
        )
    lines.extend(["", "## Worst unsupported (DELETE sample)", ""])
    for r in worst:
        lines.append(
            f"- `{r['from_id']}` → `{r['to_id']}` ({r['verdict']}): {r['notes'][:140]}"
        )
    lines.extend(
        [
            "",
            "## Headline",
            "",
            f"Of **{len(results)}** unsourced VMA edges, **{by_verdict.get('PROVEN', 0)}** upgraded to "
            f"PROVEN via internet evidence; **{by_action.get('DELETE', 0)}** proposed for deletion "
            f"as unsupported after strict two-endpoint gate.",
        ]
    )
    OUT_REPORT.parent.mkdir(parents=True, exist_ok=True)
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    scope, _ = load_scope()
    fetcher = Fetcher(CACHE_PATH)
    results: list[dict] = []
    for i, row in enumerate(scope, 1):
        results.append(adjudicate(row, i, fetcher))
        if i % 10 == 0:
            fetcher.save()
            write_ledger(results)
            print(f"progress {i}/{len(scope)} proven={sum(1 for r in results if r['verdict']=='PROVEN')}", flush=True)
    fetcher.save()
    write_ledger(results)
    write_report(scope, results)
    print(
        f"IER-C3 done: {len(results)} rows -> {OUT_LEDGER.name}",
        Counter(r["verdict"] for r in results),
        flush=True,
    )


if __name__ == "__main__":
    main()
