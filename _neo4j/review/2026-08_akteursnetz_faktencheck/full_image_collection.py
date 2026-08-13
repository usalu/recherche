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
import html
import json
import re
import threading
import unicodedata
import urllib.parse
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
PILOT_DECISIONS = BASE / "pilot_domain_decisions.json"

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
_write_lock = threading.Lock()


def write_json(path: Path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


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
    meta["page_error"] = page_error
    for idx, (priority, kind, url) in enumerate(candidates[:12], 1):
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
        result = "candidates_collected" if usable else ("no_usable_candidate" if d["status"] == "accepted" else "pending_domain")
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
    lines += ["", "## Countries", "", "| Country | candidates collected | no usable candidate | pending domain |", "|---|---:|---:|---:|"]
    for cc in COUNTRY_ORDER:
        lines.append(f"| {cc} | {country_counts[(cc, 'candidates_collected')]} | {country_counts[(cc, 'no_usable_candidate')]} | {country_counts[(cc, 'pending_domain')]} |")
    lines += ["", "`pending_domain` and `no_usable_candidate` are collection states, not final `none` decisions.",
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


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("select").set_defaults(func=select_all)
    sub.add_parser("domains").set_defaults(func=build_domains)
    confirm = sub.add_parser("confirm-domains"); confirm.add_argument("--workers", type=int, default=12); confirm.add_argument("--limit", type=int)
    confirm.set_defaults(func=confirm_domains)
    harvest = sub.add_parser("harvest"); harvest.add_argument("--workers", type=int, default=10); harvest.add_argument("--limit", type=int)
    harvest.set_defaults(func=harvest_all)
    sub.add_parser("manifest").set_defaults(func=build_manifest)
    sub.add_parser("contact").set_defaults(func=contact_sheets)
    args = ap.parse_args(); args.func(args)


if __name__ == "__main__":
    main()
