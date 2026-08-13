# -*- coding: utf-8 -*-
"""Collect official image candidates for all 762 organisations in the final net.

This is a transport/review workflow only. It never writes to Neo4j and never
turns evidence URLs into accepted organisation domains without an explicit
identity check.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures
import datetime as dt
import html
import hashlib
import http.server
import io
import json
import os
import re
import subprocess
import sys
import threading
import time
import unicodedata
import urllib.parse
import urllib.request
import webbrowser
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path

from PIL import Image, ImageDraw

import pilot_images as pilot


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
FULL = BASE / "bilder_full"
RAW = FULL / "kandidaten"
SELECTION = FULL / "selection.json"
DOMAINS = FULL / "domains_review.json"
MANIFEST = FULL / "collection_manifest.json"
REPORT = FULL / "COLLECTION_REPORT.md"
CONTACT = FULL / "contact_sheets"
SUGGESTIONS = FULL / "suggestions.json"
REVIEW = FULL / "full_asset_review.json"
FINAL = FULL / "bilder"
FINAL_MANIFEST = FULL / "final_image_manifest.json"
FINAL_REPORT = FULL / "FINAL_IMAGE_REPORT.md"
PATCH = FULL / "full_image_property_patch.json"
PATCH_REPORT = FULL / "full_image_property_patch_report.md"
RENDER = FULL / "render"
REVIEW_HTML = BASE / "full_image_review.html"
PILOT_DECISIONS = BASE / "pilot_domain_decisions.json"
NETZ = REPO / "_neo4j" / "netz"
EXPORT = pilot.EXPORT
TECTONIC = Path(r"E:\semio\.repo\cache\tectonic\0.16.9\tectonic.exe")

COUNTRY_ORDER = ("GB", "DE", "NL", "CH", "FR", "BE", "DK", "SE", "FI", "NO", "AT")
LEGAL = {
    "ag", "as", "asa", "ab", "bv", "gmbh", "oy", "oyj", "sa", "sas", "sarl",
    "ltd", "limited", "inc", "association", "foundation", "stiftung", "verein",
    "group", "holding", "the", "and", "und", "pour", "for", "of", "de", "der",
    "des", "die", "la", "le", "les", "en", "et", "organisation", "organization",
}
THIRD_PARTY_HOSTS = {
    "ots.at", "taz.de", "archdaily.com", "dezeen.com", "wikipedia.org",
    "architectsjournal.co.uk", "researchgate.net", "linkedin.com", "facebook.com",
    "instagram.com", "youtube.com", "springer.com", "mdpi.com", "corren.se",
}
SEARCH_BLOCKED_HOSTS = THIRD_PARTY_HOSTS | {
    "opalis.eu", "baunetzwissen.de", "dbz.de", "baublatt.ch", "ekopolis.fr",
    "mynewsdesk.com", "sttinfo.fi", "businessregiongoteborg.se", "futurebuilt.no",
    "superlocal.eu", "steelconstruction.info", "constructionnews.co.uk",
}
SOCIAL_MARKERS = ("facebook", "instagram", "youtube", "linkedin", "pinterest", "twitter", "tiktok")
_write_lock = threading.Lock()


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, ensure_ascii=False, indent=2) + "\n"
    tmp = path.with_suffix(path.suffix + ".tmp")
    with _write_lock:
        tmp.write_text(payload, encoding="utf-8")
        os.replace(tmp, path)


def norm(value: str) -> str:
    value = unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode()
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def tokens(value: str):
    return [t for t in norm(value).split() if len(t) >= 3 and t not in LEGAL]


def root_url(url: str) -> str:
    p = urllib.parse.urlsplit(url)
    if not p.netloc:
        return ""
    return urllib.parse.urlunsplit((p.scheme or "https", p.netloc, "/", "", ""))


def blocked_host(host: str) -> bool:
    host = (host or "").lower().removeprefix("www.")
    return pilot.host_is_blocked(host) or any(host == h or host.endswith("." + h) for h in THIRD_PARTY_HOSTS)


def select_all(_args):
    net = pilot.final_network()
    total = sum(len(p.actors) + len(p.projects) for p in net.panels.values())
    if total != 859:
        raise RuntimeError(f"final network drift: expected 859, got {total}")
    work = pilot.load_json(pilot.WORKLIST)
    by_eid = {r["eid"]: r for packet in work["packets"] for r in packet.get("nodes", [])}
    verdicts = {r["eid"]: r for r in pilot.load_json(pilot.VERDICTS)["nodes"] if r.get("eid")}
    rows = []
    for cc in COUNTRY_ORDER:
        for eid in net.panels[cc].actors:
            w = by_eid.get(eid, {})
            raw = net.raw.by.get(eid, {})
            props = raw.get("properties", {})
            primary = w.get("primary_source_url") or ""
            source_urls = [u for u in w.get("source_urls") or [] if u]
            rows.append({
                "key": pilot.node_key(cc, net.tid[eid]), "cc": cc, "tid": net.tid[eid],
                "eid": eid, "graph_backed": eid not in net.new_eids,
                "graph_id": props.get("id") if eid not in net.new_eids else None,
                "name": net.raw.name(eid), "typ": pilot.normalized_type(w.get("typ")),
                "primary_source_url": primary, "source_urls": source_urls,
                "evidence_url": verdicts.get(eid, {}).get("beleg_url", ""),
            })
    rows.sort(key=lambda r: (COUNTRY_ORDER.index(r["cc"]), r["tid"]))
    if len(rows) != 762:
        raise RuntimeError(f"expected 762 organisations, got {len(rows)}")
    write_json(SELECTION, {
        "schema_version": 1, "created_at": pilot.today(), "drawn_network_nodes": total,
        "organisation_nodes": len(rows), "project_nodes_excluded": 97,
        "graph_export_sha256": pilot.sha256_file(pilot.EXPORT), "nodes": rows,
    })
    print(f"wrote {SELECTION}: {len(rows)} organisations")


def initial_domain_row(node, manual):
    decision = manual.get(node["key"])
    if decision and decision.get("status") == "accepted" and decision.get("official_url"):
        return {"key": node["key"], "name": node["name"], "official_url": decision["official_url"],
                "status": "accepted", "basis": "pilot_manual", "notes": decision.get("notes", "")}
    if node.get("primary_source_url"):
        return {"key": node["key"], "name": node["name"],
                "official_url": "", "candidate_url": node["primary_source_url"],
                "status": "needs_review", "basis": "graph_primary_source_url_candidate",
                "notes": "Graph property is a research entry; identity check still required."}
    candidates = list(node.get("source_urls") or []) + [node.get("evidence_url", "")]
    candidate = next((u for u in candidates if u and not blocked_host(pilot.host_of(u))), "")
    return {"key": node["key"], "name": node["name"], "official_url": "",
            "candidate_url": candidate, "status": "needs_review" if candidate else "no_candidate",
            "basis": "research_entry_only" if candidate else "no_domain_candidate", "notes": ""}


def build_domains(_args):
    selection = pilot.load_json(SELECTION)["nodes"]
    manual = pilot.load_json(PILOT_DECISIONS) if PILOT_DECISIONS.exists() else {}
    existing = {r["key"]: r for r in pilot.load_json(DOMAINS).get("nodes", [])} if DOMAINS.exists() else {}
    rows = []
    for node in selection:
        fresh = initial_domain_row(node, manual)
        old = existing.get(node["key"])
        if old and old.get("status") == "accepted" and old.get("basis") in {
            "manual", "pilot_manual", "individual_identity_check"
        }:
            fresh = old
        rows.append(fresh)
    write_json(DOMAINS, {"schema_version": 1, "nodes": rows})
    print(f"wrote {DOMAINS}: {collections.Counter(r['status'] for r in rows)}")


class TitleParser(pilot.html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.title = []
        self.site_name = ""
    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag.lower() == "title":
            self.in_title = True
        if tag.lower() == "meta" and (a.get("property") or a.get("name", "")).lower() == "og:site_name":
            self.site_name = a.get("content", "")
    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False
    def handle_data(self, data):
        if self.in_title:
            self.title.append(data)


def confirm_one(node, row):
    if row["status"] != "needs_review" or not row.get("candidate_url"):
        return row
    candidate = row["candidate_url"]
    try:
        data, content_type, final_url = pilot.request_bytes(candidate)
        if content_type != "text/html" and b"<html" not in data[:1500].lower():
            data, content_type, final_url = pilot.request_bytes(root_url(candidate))
        text = data.decode("utf-8", errors="replace")[:500000]
        parser = TitleParser(); parser.feed(text)
        title = html.unescape(" ".join(parser.title)).strip()
        landing = root_url(final_url)
        host = pilot.host_of(landing)
        host_compact = norm(host).replace(" ", "")
        nt = tokens(node["name"])
        distinctive = [t for t in nt if len(t) >= 4]
        page_compact = norm(title + " " + parser.site_name + " " + re.sub(r"<[^>]+>", " ", text[:80000]))
        host_hits = [t for t in distinctive if t in host_compact]
        page_hits = [t for t in distinctive if t in page_compact]
        compact_name = "".join(distinctive[:3])
        similarity = SequenceMatcher(None, compact_name, host_compact.split(" ")[0]).ratio() if compact_name else 0.0
        accepted = bool(host_hits and page_hits) or (similarity >= 0.72 and bool(page_hits))
        result = dict(row)
        result.update({"checked_url": final_url, "checked_at": pilot.today(), "page_title": title[:300],
                       "host_hits": host_hits, "page_hits": page_hits[:8], "host_similarity": round(similarity, 3)})
        if accepted and not blocked_host(host):
            result.update({"official_url": landing, "status": "accepted", "basis": "individual_identity_check"})
        else:
            result.update({"status": "needs_review", "basis": "identity_check_inconclusive"})
        return result
    except Exception as exc:
        result = dict(row)
        result.update({"status": "needs_review", "basis": "identity_check_failed",
                       "check_error": f"{type(exc).__name__}: {exc}", "checked_at": pilot.today()})
        return result


def confirm_domains(args):
    nodes = {r["key"]: r for r in pilot.load_json(SELECTION)["nodes"]}
    rows = pilot.load_json(DOMAINS)["nodes"]
    todo = [r for r in rows if r["status"] == "needs_review" and r.get("candidate_url")]
    if args.limit:
        todo = todo[:args.limit]
    updates = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(confirm_one, nodes[r["key"]], r): r["key"] for r in todo}
        for n, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result(); updates[result["key"]] = result
            print(f"[{n}/{len(todo)}] {result['key']}: {result['status']} ({result['basis']})")
    merged = [updates.get(r["key"], r) for r in rows]
    write_json(DOMAINS, {"schema_version": 1, "nodes": merged})
    print("domain status:", collections.Counter(r["status"] for r in merged))


def name_aliases(name: str):
    """Return normalized names, abbreviations and parent-name fragments."""
    raw_parts = [name] + re.split(r"\s*(?:/|–|—|\(|\))\s*", name)
    aliases = set()
    for part in raw_parts:
        part = norm(part)
        if not part:
            continue
        aliases.add(part)
        ts = tokens(part)
        if ts:
            aliases.add(" ".join(ts))
            if len(ts) >= 2:
                aliases.add("".join(t[0] for t in ts))
    for token in re.findall(r"\b[A-ZÄÖÜ][A-ZÄÖÜ0-9+&.-]{1,7}\b", name):
        aliases.add(norm(token).replace(" ", ""))
    return sorted((a for a in aliases if len(a.replace(" ", "")) >= 3), key=len, reverse=True)


def identity_score(name: str, host: str, page_text: str):
    host_compact = norm(host).replace(" ", "").removeprefix("www")
    page = norm(page_text[:160000])
    hits, score = [], 0.0
    for alias in name_aliases(name):
        compact = alias.replace(" ", "")
        if compact in host_compact:
            score = max(score, 8.0 + min(len(compact), 12) / 10)
            hits.append("host:" + alias)
        if len(alias) >= 4 and alias in page:
            score += min(3.0, len(alias) / 12)
            hits.append("page:" + alias)
    token_hits = sorted({t for t in tokens(name) if len(t) >= 4 and t in page})
    score += min(4.0, len(token_hits) * 1.2)
    hits += ["token:" + t for t in token_hits[:6]]
    return score, hits


def fetch_identity(url: str):
    data, content_type, final_url = pilot.request_bytes(url)
    if content_type != "text/html" and b"<html" not in data[:1500].lower():
        raise ValueError("identity URL is not HTML")
    text = data.decode("utf-8", errors="replace")
    parser = TitleParser(); parser.feed(text)
    title = html.unescape(" ".join(parser.title)).strip()
    visible = re.sub(r"<script\b[^>]*>.*?</script>|<style\b[^>]*>.*?</style>", " ", text, flags=re.I | re.S)
    visible = html.unescape(re.sub(r"<[^>]+>", " ", visible))
    return final_url, title, parser.site_name, visible


def bing_results(query: str, limit: int = 8):
    url = "https://www.bing.com/search?format=rss&q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": pilot.USER_AGENT})
    with urllib.request.urlopen(req, timeout=20) as response:
        root = ET.fromstring(response.read(2_000_000))
    return [{"title": item.findtext("title") or "", "url": item.findtext("link") or "",
             "snippet": item.findtext("description") or ""}
            for item in root.findall("./channel/item")[:limit]]


def research_one(node, row):
    if row.get("status") == "accepted":
        return row
    attempts, candidates = [], []
    current = row.get("candidate_url") or ""
    if current and not blocked_host(pilot.host_of(current)):
        candidates.append({"url": current, "origin": "existing_research_entry", "search_text": ""})
    for query in (f'"{node["name"]}" official {node["cc"]}', f'{node["name"]} logo official'):
        try:
            results = bing_results(query)
            attempts.append({"query": query, "result_count": len(results)})
            for found in results:
                if found["url"] and not blocked_host(pilot.host_of(found["url"])):
                    candidates.append({"url": found["url"], "origin": "web_search",
                                       "search_text": found["title"] + " " + found["snippet"]})
        except Exception as exc:
            attempts.append({"query": query, "error": f"{type(exc).__name__}: {exc}"})
    seen, evaluated = set(), []
    for candidate in candidates:
        root = root_url(candidate["url"])
        host = pilot.host_of(root)
        if not root or host in seen or blocked_host(host):
            continue
        seen.add(host)
        try:
            final_url, title, site_name, body = fetch_identity(candidate["url"])
            final_root = root_url(final_url); final_host = pilot.host_of(final_root)
            if blocked_host(final_host):
                continue
            score, hits = identity_score(node["name"], final_host,
                                         title + " " + site_name + " " + candidate["search_text"] + " " + body)
            evaluated.append({"url": final_root, "page_title": title[:300], "score": round(score, 2),
                              "hits": hits[:10], "origin": candidate["origin"]})
        except Exception as exc:
            evaluated.append({"url": root, "score": 0, "origin": candidate["origin"],
                              "error": f"{type(exc).__name__}: {exc}"})
    evaluated.sort(key=lambda x: (-x.get("score", 0), x["url"]))
    result = dict(row)
    result.update({"research_checked_at": pilot.today(), "research_attempts": attempts,
                   "research_candidates": evaluated[:12]})
    best = next((x for x in evaluated if x.get("score", 0) >= 7.5), None)
    if best:
        result.update({"official_url": best["url"], "status": "accepted",
                       "basis": "individual_official_web_research",
                       "notes": "Official or parent mark candidate verified by host and page identity."})
    else:
        result.update({"official_url": "", "status": "resolved_none",
                       "basis": "no_verified_official_domain_after_research",
                       "notes": "Two official-domain searches and available entries produced no verified organisation or parent domain."})
    return result


def research_domains(args):
    nodes = {r["key"]: r for r in pilot.load_json(SELECTION)["nodes"]}
    rows = pilot.load_json(DOMAINS)["nodes"]
    todo = [r for r in rows if r.get("status") != "accepted"]
    if args.limit:
        todo = todo[:args.limit]
    updates = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(research_one, nodes[r["key"]], r): r["key"] for r in todo}
        for pos, future in enumerate(concurrent.futures.as_completed(futures), 1):
            result = future.result(); updates[result["key"]] = result
            print(f"[{pos}/{len(todo)}] {result['key']}: {result['status']}")
    merged = [updates.get(r["key"], r) for r in rows]
    write_json(DOMAINS, {"schema_version": 2, "nodes": merged})
    print("research status:", collections.Counter(r["status"] for r in merged))


def harvest_one(node, domain):
    node_dir = RAW / node["cc"] / node["tid"]
    node_dir.mkdir(parents=True, exist_ok=True)
    meta = {"key": node["key"], "official_url": domain.get("official_url", ""),
            "domain_basis": domain.get("basis", ""), "page_error": "", "candidates": []}
    if domain.get("status") != "accepted" or not domain.get("official_url"):
        meta["page_error"] = "domain not accepted"
        write_json(node_dir / "candidates.json", meta)
        return node["key"], 0, 0
    candidates, page_error = pilot.discover_candidates(domain["official_url"])
    candidates.extend(discover_media_candidates(domain["official_url"], candidates))
    meta["page_error"] = page_error
    for idx, (priority, kind, url) in enumerate(candidates[:20], 1):
        record = {"id": f"c{idx:02d}", "priority": priority, "kind": kind,
                  "url": url, "status": "rejected", "review_status": "pending",
                  "retrieved_at": "", "license_note": "Official-site candidate; usage rights require final review.",
                  "source_sha256": "", "preview_sha256": "", "reason": ""}
        try:
            data, content_type, final_url = pilot.request_bytes(url)
            im, fmt = pilot.rasterize(data, content_type, final_url)
            record.update({"final_url": final_url, "content_type": content_type,
                           "format": fmt, "width": im.width, "height": im.height,
                           "retrieved_at": pilot.today(), "source_sha256": pilot.sha256_bytes(data)})
            if fmt != "svg" and min(im.size) < 128:
                record["reason"] = "short edge below 128px"
            else:
                preview = node_dir / f"{record['id']}_{kind}.png"
                im.save(preview, "PNG")
                record.update({"preview_path": str(preview.relative_to(FULL)).replace("\\", "/"),
                               "preview_sha256": pilot.sha256_file(preview), "status": "candidate"})
        except Exception as exc:
            record["reason"] = f"{type(exc).__name__}: {exc}"
        meta["candidates"].append(record)
    write_json(node_dir / "candidates.json", meta)
    good = sum(c["status"] == "candidate" for c in meta["candidates"])
    return node["key"], good, len(meta["candidates"])


def discover_media_candidates(official_url, existing):
    """Search a small set of official brand/media/about pages for a mark."""
    existing_urls = {urllib.parse.urldefrag(row[2])[0] for row in existing}
    root_host = pilot.host_of(official_url)
    page_links = []
    try:
        data, content_type, final_url = pilot.request_bytes(official_url)
        if content_type != "text/html" and b"<html" not in data[:1500].lower():
            return []
        text = data.decode("utf-8", errors="replace")
        for match in re.finditer(r"<a\b[^>]*href=[\"']([^\"']+)[\"'][^>]*>(.*?)</a>", text, re.I | re.S):
            href = urllib.parse.urljoin(final_url, html.unescape(match.group(1)))
            label = norm(re.sub(r"<[^>]+>", " ", match.group(2)) + " " + href)
            if pilot.host_of(href) == root_host and any(word in label for word in (
                "brand", "branding", "logo", "media", "press", "presse", "download",
                "about", "uber uns", "over ons", "om oss", "a propos")):
                page_links.append(href)
    except Exception:
        return []
    output, seen_pages = [], set()
    for page_url in page_links:
        clean_page = urllib.parse.urldefrag(page_url)[0]
        if clean_page in seen_pages or len(seen_pages) >= 5:
            continue
        seen_pages.add(clean_page)
        try:
            data, content_type, final_url = pilot.request_bytes(clean_page)
            if content_type != "text/html" and b"<html" not in data[:1500].lower():
                continue
            parser = pilot.IconParser(); parser.feed(data.decode("utf-8", errors="replace"))
            base = urllib.parse.urljoin(final_url, parser.base) if parser.base else final_url
            for _priority, kind, url in parser.candidates:
                absolute = urllib.parse.urldefrag(urllib.parse.urljoin(base, url))[0]
                if absolute not in existing_urls:
                    output.append((6, "media_logo" if kind == "header_logo" else kind, absolute))
                    existing_urls.add(absolute)
            for match in re.finditer(r"<(?:img|source)\b[^>]*(?:src|srcset)=[\"']([^\"' ,]+)",
                                     data.decode("utf-8", errors="replace"), re.I):
                absolute = urllib.parse.urldefrag(urllib.parse.urljoin(final_url, html.unescape(match.group(1))))[0]
                if absolute not in existing_urls and any(word in absolute.lower() for word in ("logo", "brand", "wordmark")):
                    output.append((6, "media_logo", absolute)); existing_urls.add(absolute)
        except Exception:
            continue
    return output


def harvest_all(args):
    nodes = {r["key"]: r for r in pilot.load_json(SELECTION)["nodes"]}
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    todo = [nodes[k] for k in sorted(nodes) if domains[k]["status"] == "accepted"]
    if args.limit:
        todo = todo[:args.limit]
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = [pool.submit(harvest_one, n, domains[n["key"]]) for n in todo]
        for pos, future in enumerate(concurrent.futures.as_completed(futures), 1):
            key, good, total = future.result()
            print(f"[{pos}/{len(todo)}] {key}: {good}/{total} usable")


def build_manifest(_args):
    nodes = pilot.load_json(SELECTION)["nodes"]
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    rows = []
    for node in nodes:
        d = domains[node["key"]]
        path = RAW / node["cc"] / node["tid"] / "candidates.json"
        meta = pilot.load_json(path) if path.exists() else {"candidates": []}
        usable = [c for c in meta.get("candidates", []) if c.get("status") == "candidate"]
        result = ("candidates_collected" if usable else
                  ("no_usable_candidate" if d["status"] == "accepted" else "resolved_none"))
        candidate_transport = [{k: c.get(k) for k in (
            "id", "kind", "url", "final_url", "retrieved_at", "license_note", "review_status",
            "source_sha256", "preview_sha256", "preview_path", "format", "width", "height"
        )} for c in usable]
        rows.append({**{k: node[k] for k in ("key", "cc", "tid", "eid", "graph_id", "name", "typ")},
                     "domain_status": d["status"], "official_url": d.get("official_url", ""),
                     "domain_basis": d.get("basis", ""), "collection_result": result,
                     "candidate_count": len(usable),
                     "candidates": candidate_transport,
                     "candidate_metadata": str(path.relative_to(FULL)).replace("\\", "/") if path.exists() else None})
    counts = collections.Counter(r["collection_result"] for r in rows)
    domain_counts = collections.Counter(r["domain_status"] for r in rows)
    candidate_total = sum(r["candidate_count"] for r in rows)
    graph_backed = sum(r["graph_id"] is not None for r in rows)
    country_counts = collections.Counter((r["cc"], r["collection_result"]) for r in rows)
    write_json(MANIFEST, {"schema_version": 1, "transport_only": True,
                          "created_at": pilot.today(), "nodes": rows, "counts": counts})
    lines = ["# Full image candidate collection", "", "- Organisations: **762**",
             "- Projects excluded: **97**", f"- Graph-backed organisations: **{graph_backed}**",
             f"- Overlay organisations: **{762 - graph_backed}**", "- Neo4j writes: **0**",
             f"- Collected candidate files: **{candidate_total}**", "", "## Results", ""]
    lines += [f"- {k}: **{v}**" for k, v in sorted(counts.items())]
    lines += ["", "## Domain review", ""] + [f"- {k}: **{v}**" for k, v in sorted(domain_counts.items())]
    lines += ["", "## Countries", "", "| Country | candidates collected | no usable candidate | resolved none |", "|---|---:|---:|---:|"]
    for cc in COUNTRY_ORDER:
        lines.append(f"| {cc} | {country_counts[(cc, 'candidates_collected')]} | {country_counts[(cc, 'no_usable_candidate')]} | {country_counts[(cc, 'resolved_none')]} |")
    lines += ["", "`resolved_none` and `no_usable_candidate` are research/suggestion states; your explicit review is still required.",
              "Every candidate remains `review_status: pending` until visual and licence review."]
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote {MANIFEST} and {REPORT}: {dict(counts)}")


def contact_sheets(_args):
    nodes = pilot.load_json(SELECTION)["nodes"]
    visible = []
    for node in nodes:
        path = RAW / node["cc"] / node["tid"] / "candidates.json"
        meta = pilot.load_json(path) if path.exists() else {"candidates": []}
        usable = [c for c in meta.get("candidates", []) if c.get("status") == "candidate"][:4]
        if usable:
            visible.append((node, usable))
    CONTACT.mkdir(parents=True, exist_ok=True)
    for old_sheet in CONTACT.glob("contact_*.png"):
        old_sheet.unlink()
    for page_no, start in enumerate(range(0, len(visible), 12), 1):
        sheet = Image.new("RGB", (1040, 2280), "#f7f3e3"); draw = ImageDraw.Draw(sheet)
        for row_no, (node, candidates) in enumerate(visible[start:start + 12]):
            y = row_no * 190
            draw.text((4, y + 4), f"{node['key']}  {node['name'][:34]}", fill="#001117", font=pilot.font(16))
            for col, candidate in enumerate(candidates):
                x = col * 260; im = Image.open(FULL / candidate["preview_path"]).convert("RGBA")
                im.thumbnail((140, 120), Image.Resampling.LANCZOS)
                tile = Image.new("RGBA", (150, 125), "white")
                tile.alpha_composite(im, ((150 - im.width) // 2, (125 - im.height) // 2))
                sheet.paste(tile.convert("RGB"), (x + 55, y + 34))
                draw.text((x + 58, y + 160), f"{candidate['id']} {candidate['kind']}", fill="#001117", font=pilot.font(14))
        sheet.save(CONTACT / f"contact_{page_no:03d}.png")
    print(f"wrote {len(list(CONTACT.glob('contact_*.png')))} contact sheets for {len(visible)} organisations")


def usable_candidates(node):
    path = RAW / node["cc"] / node["tid"] / "candidates.json"
    if not path.exists():
        return []
    return [c for c in pilot.load_json(path).get("candidates", []) if c.get("status") == "candidate"]


def candidate_rank(candidate):
    weights = {"apple_touch": 100, "declared_icon": 95, "favicon": 90,
               "header_logo": 85, "media_logo": 75, "wikimedia": 70, "og_image": 45}
    url = (candidate.get("final_url") or candidate.get("url") or "").lower()
    penalty = 200 if any(marker in url for marker in SOCIAL_MARKERS) else 0
    if any(marker in url for marker in ("no-image", "placeholder", "default-image", "spacer")):
        penalty += 200
    w, h = candidate.get("width", 1), candidate.get("height", 1)
    shape_bonus = 8 if 0.65 <= w / max(h, 1) <= 1.55 else 0
    size_bonus = min(8, min(w, h) / 128)
    return weights.get(candidate.get("kind"), 0) + shape_bonus + size_bonus - penalty


def command_suggest(_args):
    nodes = pilot.load_json(SELECTION)["nodes"]
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    rows = []
    for node in nodes:
        candidates = usable_candidates(node)
        ranked = sorted(candidates, key=lambda c: (-candidate_rank(c), c["id"]))
        best = ranked[0] if ranked and candidate_rank(ranked[0]) > 0 else None
        if best:
            result, candidate_id = "logo", best["id"]
            reason = f"Highest-ranked official candidate: {best['kind']}; review is still required."
        else:
            result, candidate_id = "none", ""
            reason = ("No technically usable official candidate was collected."
                      if domains[node["key"]].get("status") == "accepted"
                      else "No verified organisation or parent domain/mark after research.")
        rows.append({"key": node["key"], "suggested_result": result,
                     "suggested_candidate_id": candidate_id, "reason": reason,
                     "confirmed": False})
    write_json(SUGGESTIONS, {"schema_version": 1, "created_at": pilot.today(), "nodes": rows})
    print(f"wrote {SUGGESTIONS}: {collections.Counter(r['suggested_result'] for r in rows)}")


def prepared_canvas(source: Path):
    im = pilot.remove_edge_background(Image.open(source))
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("candidate has no visible pixels")
    im = im.crop(bbox)
    scale = min((pilot.SAFE_RADIUS * 2) / im.width, (pilot.SAFE_RADIUS * 2) / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))), Image.Resampling.LANCZOS)
    canvas = Image.new("RGBA", (pilot.FINAL_SIZE, pilot.FINAL_SIZE), (0, 0, 0, 0))
    canvas.alpha_composite(im, ((pilot.FINAL_SIZE - im.width) // 2, (pilot.FINAL_SIZE - im.height) // 2))
    max_r = pilot.alpha_max_radius(canvas)
    if max_r > pilot.SAFE_RADIUS:
        ratio = (pilot.SAFE_RADIUS - 1.0) / max_r
        im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))), Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (pilot.FINAL_SIZE, pilot.FINAL_SIZE), (0, 0, 0, 0))
        canvas.alpha_composite(im, ((pilot.FINAL_SIZE - im.width) // 2, (pilot.FINAL_SIZE - im.height) // 2))
    return canvas


def review_document():
    existing = pilot.load_json(REVIEW) if REVIEW.exists() else {"schema_version": 1, "nodes": []}
    existing.setdefault("nodes", [])
    return existing


def candidate_for(node, candidate_id):
    matches = [c for c in usable_candidates(node) if c.get("id") == candidate_id]
    if len(matches) != 1:
        raise ValueError(f"{node['key']}: candidate {candidate_id!r} not found")
    return matches[0]


def review_state():
    nodes = pilot.load_json(SELECTION)["nodes"]
    domains = {r["key"]: r for r in pilot.load_json(DOMAINS)["nodes"]}
    suggestions = ({r["key"]: r for r in pilot.load_json(SUGGESTIONS)["nodes"]}
                   if SUGGESTIONS.exists() else {})
    decisions = {r["key"]: r for r in review_document()["nodes"]}
    output = []
    for node in nodes:
        candidates = []
        for candidate in sorted(usable_candidates(node), key=lambda c: (-candidate_rank(c), c["id"])):
            candidates.append({k: candidate.get(k) for k in (
                "id", "kind", "url", "final_url", "width", "height", "format",
                "preview_path", "preview_sha256", "license_note", "retrieved_at")})
        output.append({**{k: node.get(k) for k in ("key", "cc", "tid", "eid", "name", "typ", "graph_id")},
                       "domain": domains[node["key"]], "suggestion": suggestions.get(node["key"], {}),
                       "decision": decisions.get(node["key"]), "candidates": candidates})
    return {"schema_version": 1, "total": len(output), "confirmed": len(decisions), "nodes": output}


class ReviewHandler(http.server.BaseHTTPRequestHandler):
    server_version = "AkteursnetzImageReview/1.0"

    def log_message(self, fmt, *args):
        print("review:", fmt % args)

    def send_bytes(self, data, content_type, status=200):
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers(); self.wfile.write(data)

    def send_json(self, value, status=200):
        data = json.dumps(value, ensure_ascii=False).encode("utf-8")
        self.send_bytes(data, "application/json; charset=utf-8", status)

    def do_GET(self):
        parsed = urllib.parse.urlsplit(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        try:
            if parsed.path == "/":
                self.send_bytes(REVIEW_HTML.read_bytes(), "text/html; charset=utf-8")
            elif parsed.path == "/api/state":
                self.send_json(review_state())
            elif parsed.path == "/asset":
                rel = query.get("path", [""])[0]
                target = (FULL / rel).resolve()
                if FULL.resolve() not in target.parents or not target.is_file():
                    raise FileNotFoundError(rel)
                self.send_bytes(target.read_bytes(), "image/png")
            elif parsed.path == "/prepared":
                key = query.get("key", [""])[0]
                candidate_id = query.get("candidate", [""])[0]
                node = next(n for n in pilot.load_json(SELECTION)["nodes"] if n["key"] == key)
                candidate = candidate_for(node, candidate_id)
                image = prepared_canvas(FULL / candidate["preview_path"])
                buf = io.BytesIO(); image.save(buf, "PNG", optimize=True)
                self.send_bytes(buf.getvalue(), "image/png")
            else:
                self.send_json({"error": "not found"}, 404)
        except Exception as exc:
            self.send_json({"error": f"{type(exc).__name__}: {exc}"}, 400)

    def do_POST(self):
        if urllib.parse.urlsplit(self.path).path != "/api/decision":
            self.send_json({"error": "not found"}, 404); return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length <= 0 or length > 100_000:
                raise ValueError("invalid request size")
            value = json.loads(self.rfile.read(length))
            nodes = pilot.load_json(SELECTION)["nodes"]
            by_key = {n["key"]: n for n in nodes}
            key, result = value.get("key"), value.get("result")
            if key not in by_key or result not in {"logo", "none"}:
                raise ValueError("invalid key or result")
            candidate_id, candidate_hash = "", None
            if result == "logo":
                candidate_id = value.get("candidate_id") or ""
                candidate = candidate_for(by_key[key], candidate_id)
                candidate_hash = candidate.get("preview_sha256") or pilot.sha256_file(FULL / candidate["preview_path"])
            decisions = {r["key"]: r for r in review_document()["nodes"]}
            decisions[key] = {"key": key, "result": result, "candidate_id": candidate_id,
                              "candidate_sha256": candidate_hash,
                              "confirmed_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
                              "reviewer": (value.get("reviewer") or "user").strip()[:100],
                              "notes": (value.get("notes") or "").strip()[:2000]}
            ordered = [decisions[n["key"]] for n in nodes if n["key"] in decisions]
            write_json(REVIEW, {"schema_version": 1, "required": 762, "nodes": ordered})
            self.send_json({"ok": True, "confirmed": len(ordered), "total": len(nodes),
                            "decision": decisions[key]})
        except Exception as exc:
            self.send_json({"error": f"{type(exc).__name__}: {exc}"}, 400)


def command_review_server(args):
    if not REVIEW_HTML.is_file():
        raise FileNotFoundError(REVIEW_HTML)
    if not SUGGESTIONS.exists():
        command_suggest(args)
    server = http.server.ThreadingHTTPServer((args.host, args.port), ReviewHandler)
    url = f"http://{args.host}:{args.port}/"
    print(f"Review gallery: {url}")
    if not args.no_open:
        threading.Timer(0.5, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


def complete_review():
    nodes = pilot.load_json(SELECTION)["nodes"]
    decisions = {r["key"]: r for r in review_document()["nodes"]}
    expected = {n["key"] for n in nodes}
    missing = sorted(expected - set(decisions))
    extra = sorted(set(decisions) - expected)
    if missing or extra or len(decisions) != 762:
        raise ValueError(f"review incomplete: {len(decisions)}/762 confirmed; missing={len(missing)} extra={len(extra)}")
    return nodes, decisions


def command_finalize(_args):
    nodes, decisions = complete_review()
    rows = []
    for node in nodes:
        decision = decisions[node["key"]]
        result = decision.get("result")
        if result not in {"logo", "none"}:
            raise ValueError(f"{node['key']}: invalid result")
        row = {**{k: node.get(k) for k in ("key", "cc", "tid", "eid", "graph_id", "name", "typ")},
               "result": result, "review_status": "accepted", "asset_path": None,
               "dark_asset_path": None, "source_url": None, "source_kind": None,
               "retrieved_at": pilot.today(), "license_note": "", "sha256": None,
               "reviewer": decision.get("reviewer", "user"),
               "confirmed_at": decision.get("confirmed_at"), "review_notes": decision.get("notes", "")}
        if result == "logo":
            candidate = candidate_for(node, decision.get("candidate_id") or "")
            source = FULL / candidate["preview_path"]
            current_hash = candidate.get("preview_sha256") or pilot.sha256_file(source)
            if decision.get("candidate_sha256") != current_hash:
                raise ValueError(f"{node['key']}: confirmed candidate changed after review")
            dest = FINAL / node["cc"] / f"{node['tid']}.png"
            dest.parent.mkdir(parents=True, exist_ok=True)
            prepared_canvas(source).save(dest, "PNG", optimize=True)
            row.update({"asset_path": str(dest.relative_to(FULL)).replace("\\", "/"),
                        "source_url": candidate.get("final_url") or candidate.get("url"),
                        "source_kind": candidate.get("kind"),
                        "retrieved_at": candidate.get("retrieved_at") or pilot.today(),
                        "license_note": candidate.get("license_note") or "Official-site mark used for identification; no affiliation implied.",
                        "sha256": pilot.sha256_file(dest)})
        rows.append(row)
    manifest = {"schema_version": 1, "transport_only": True,
                "canonical_target": "Neo4j node properties after separate approval",
                "database": "mit-bestand", "created_at": pilot.today(),
                "graph_export_sha256": pilot.load_json(SELECTION)["graph_export_sha256"],
                "nodes": rows}
    write_json(FINAL_MANIFEST, manifest)
    counts = collections.Counter(r["result"] for r in rows)
    FINAL_REPORT.write_text("# Final image manifest\n\n" +
                            f"- Confirmed nodes: **{len(rows)}**\n- Logos: **{counts['logo']}**\n- None: **{counts['none']}**\n- Neo4j writes: **0**\n",
                            encoding="utf-8")
    print(f"wrote {FINAL_MANIFEST}: {dict(counts)}")


def validate_final_manifest(manifest):
    errors, rows = [], manifest.get("nodes", [])
    selection = pilot.load_json(SELECTION)["nodes"]
    if len(rows) != 762:
        errors.append(f"expected 762 rows, got {len(rows)}")
    if {r.get("key") for r in rows} != {r["key"] for r in selection}:
        errors.append("manifest keys differ from frozen selection")
    if sum(r.get("graph_id") is not None for r in rows) != 412:
        errors.append("graph-backed count is not 412")
    for row in rows:
        key = row.get("key", "?")
        if row.get("review_status") != "accepted" or row.get("result") not in {"logo", "none"}:
            errors.append(f"{key}: unresolved result"); continue
        if not row.get("confirmed_at") or not row.get("reviewer"):
            errors.append(f"{key}: missing explicit reviewer confirmation")
        if row["result"] == "none":
            if row.get("asset_path"):
                errors.append(f"{key}: none row has asset")
            continue
        path = FULL / (row.get("asset_path") or "")
        if not path.is_file():
            errors.append(f"{key}: missing final asset"); continue
        with Image.open(path) as image:
            if image.size != (256, 256) or image.mode != "RGBA" or image.format != "PNG":
                errors.append(f"{key}: expected 256x256 RGBA PNG")
            if pilot.alpha_max_radius(image.convert("RGBA")) > pilot.SAFE_RADIUS + 0.75:
                errors.append(f"{key}: visible pixels exceed 93% radial safety zone")
        if pilot.sha256_file(path) != row.get("sha256"):
            errors.append(f"{key}: final checksum mismatch")
        if not row.get("source_url") or not row.get("source_kind") or not row.get("license_note"):
            errors.append(f"{key}: incomplete provenance")
    return errors


def command_validate(_args):
    if not FINAL_MANIFEST.exists():
        raise FileNotFoundError("final manifest does not exist; complete review and run finalize")
    errors = validate_final_manifest(pilot.load_json(FINAL_MANIFEST))
    if errors:
        print("FAIL\n" + "\n".join(" - " + e for e in errors)); raise SystemExit(1)
    print("PASS: 762/762 explicitly confirmed; assets and provenance valid")


def command_patch(args):
    manifest = pilot.load_json(FINAL_MANIFEST)
    errors = validate_final_manifest(manifest)
    if errors:
        raise ValueError("final manifest invalid; run validate first")
    export = pilot.load_json(EXPORT)
    by_id = collections.Counter(n.get("properties", {}).get("id") for n in export["nodes"]
                                if n.get("properties", {}).get("id"))
    patch_rows, overlays, match_errors = [], [], []
    for row in manifest["nodes"]:
        if not row.get("graph_id"):
            overlays.append({"key": row["key"], "eid": row["eid"],
                             "reason": "overlay node has no canonical graph id"})
            continue
        graph_id = row["graph_id"]
        if by_id[graph_id] != 1:
            match_errors.append(f"{row['key']}: id {graph_id!r} matches {by_id[graph_id]} export nodes")
            continue
        props = {"image_result": row["result"], "image_review_status": "full_accepted",
                 "image_retrieved_at": row["retrieved_at"]}
        if row["result"] == "logo":
            props.update({"image_asset_path": str((FULL / row["asset_path"]).relative_to(REPO)).replace("\\", "/"),
                          "image_source_url": row["source_url"], "image_source_kind": row["source_kind"],
                          "image_license_note": row["license_note"], "image_sha256": row["sha256"]})
        patch_rows.append({"match": {"id": graph_id}, "set": props,
                           "audit": {"key": row["key"], "eid": row["eid"]}})
    live = None
    if args.live:
        counts = pilot.live_counts([r["match"]["id"] for r in patch_rows])
        live = {"database": "mit-bestand", "read_only": True, "counts": counts}
        match_errors += [f"live {gid!r}: {count} matches" for gid, count in counts.items() if count != 1]
    if len(patch_rows) != 412 or len(overlays) != 350:
        match_errors.append(f"partition mismatch: patch={len(patch_rows)} overlay={len(overlays)}")
    value = {"schema_version": 1, "database": "mit-bestand", "dry_run_only": True,
             "match_property": "id",
             "forbidden_side_effects": ["create :Quelle nodes", "create BELEGT_IN relationships",
                                        "write metadata_sidecar_key"],
             "rows": patch_rows, "blocked_overlay_nodes": overlays,
             "validation": {"export": str(EXPORT), "live": live, "errors": match_errors}}
    write_json(PATCH, value)
    lines = ["# Full image property patch report", "", f"- Patch rows: **{len(patch_rows)}**",
             f"- Overlay-only: **{len(overlays)}**", f"- Match errors: **{len(match_errors)}**",
             f"- Live read-only validation: **{'run' if args.live else 'not run'}**", "",
             "No write was performed against Neo4j."]
    PATCH_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"wrote dry-run patch: {len(patch_rows)} rows, {len(overlays)} overlays")
    if match_errors:
        raise SystemExit(1)


def assemble_render_tex(fragment: Path, theme: str, destination: Path):
    head = (NETZ / "head.tex").read_text(encoding="utf-8")
    if theme == "dark":
        head = head.replace(r"\documentclass[type=zwischenbericht]{zukunftbau}",
                            r"\documentclass[type=zwischenbericht,theme=dark]{zukunftbau}", 1)
    body = fragment.read_text(encoding="utf-8")
    tail = (NETZ / "tail.tex").read_text(encoding="utf-8")
    destination.write_text(head + body + tail, encoding="utf-8", newline="\n")


def compile_tex(tex_path: Path):
    report_dir = Path(r"E:\semio\mit-bestand\bericht\zwischenbericht")
    command = [str(TECTONIC), "--keep-logs", "-Z", "search-path=E:/semio/print/tex",
               "--outdir", str(RENDER), str(tex_path)]
    result = subprocess.run(command, cwd=report_dir, capture_output=True, text=True)
    pdf = RENDER / (tex_path.stem + ".pdf")
    if result.returncode != 0 or not pdf.is_file():
        raise RuntimeError((result.stdout + result.stderr)[-3000:])
    return pdf


def command_render(_args):
    manifest = pilot.load_json(FINAL_MANIFEST)
    errors = validate_final_manifest(manifest)
    if errors:
        raise ValueError("final manifest invalid; render blocked")
    RENDER.mkdir(parents=True, exist_ok=True)
    image_fragment = RENDER / "frag_images.tex"
    control_fragment = RENDER / "frag_control.tex"
    base_cmd = [sys.executable, "-m", "netz.cli", "abb"]
    for out, extra in ((image_fragment, ["--images-manifest", str(FINAL_MANIFEST)]),
                       (control_fragment, [])):
        result = subprocess.run(base_cmd + ["--out", str(out)] + extra, cwd=NETZ, capture_output=True, text=True)
        if result.returncode:
            raise RuntimeError((result.stdout + result.stderr)[-3000:])
    logo_count = sum(r["result"] == "logo" for r in manifest["nodes"])
    source = image_fragment.read_text(encoding="utf-8")
    if source.count("image={") != logo_count:
        raise ValueError(f"render fragment has {source.count('image={')} images, expected {logo_count}")
    pdfs = {}
    for theme in ("light", "dark"):
        for label, fragment in (("images", image_fragment), ("control", control_fragment)):
            tex = RENDER / f"akteursnetz_{label}_{theme}.tex"
            assemble_render_tex(fragment, theme, tex)
            pdfs[f"{label}_{theme}"] = compile_tex(tex)
    import fitz
    raster_root = RENDER / "600dpi"
    render_info = {}
    for label, pdf in pdfs.items():
        doc = fitz.open(pdf); target = raster_root / label; target.mkdir(parents=True, exist_ok=True)
        pages = []
        for page_no, page in enumerate(doc):
            out = target / f"page_{page_no + 1:02d}.png"
            page.get_pixmap(matrix=fitz.Matrix(600 / 72, 600 / 72), alpha=False).save(out)
            pages.append({"page": page_no + 1, "png": str(out.relative_to(FULL)).replace("\\", "/"),
                          "sha256": pilot.sha256_file(out)})
        render_info[label] = {"pdf": str(pdf.relative_to(FULL)).replace("\\", "/"),
                              "page_count": len(doc), "pages": pages}
        doc.close()
    write_json(RENDER / "render_report.json", {"schema_version": 1, "logo_count": logo_count,
                                                "countries": list(COUNTRY_ORDER), "renders": render_info,
                                                "result": "PASS"})
    print(f"PASS: rendered {logo_count} logos in light/dark plus controls at 600 dpi")


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("select").set_defaults(func=select_all)
    sub.add_parser("domains").set_defaults(func=build_domains)
    confirm = sub.add_parser("confirm-domains"); confirm.add_argument("--workers", type=int, default=12); confirm.add_argument("--limit", type=int)
    confirm.set_defaults(func=confirm_domains)
    research = sub.add_parser("research"); research.add_argument("--workers", type=int, default=8); research.add_argument("--limit", type=int)
    research.set_defaults(func=research_domains)
    harvest = sub.add_parser("harvest"); harvest.add_argument("--workers", type=int, default=10); harvest.add_argument("--limit", type=int)
    harvest.set_defaults(func=harvest_all)
    sub.add_parser("manifest").set_defaults(func=build_manifest)
    sub.add_parser("contact").set_defaults(func=contact_sheets)
    sub.add_parser("suggest").set_defaults(func=command_suggest)
    review = sub.add_parser("review-server"); review.add_argument("--host", default="127.0.0.1"); review.add_argument("--port", type=int, default=8765); review.add_argument("--no-open", action="store_true")
    review.set_defaults(func=command_review_server)
    sub.add_parser("finalize").set_defaults(func=command_finalize)
    sub.add_parser("validate").set_defaults(func=command_validate)
    sub.add_parser("render").set_defaults(func=command_render)
    patch = sub.add_parser("patch"); patch.add_argument("--live", action="store_true", help="read-only exact-id validation against mit-bestand")
    patch.set_defaults(func=command_patch)
    args = ap.parse_args(); args.func(args)


if __name__ == "__main__":
    main()
