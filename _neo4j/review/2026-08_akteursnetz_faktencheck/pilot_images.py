# -*- coding: utf-8 -*-
"""Reproducible 48-node image pilot for the printed actor network.

The script never writes to Neo4j.  Its final ``patch`` command emits a
reviewable property patch and can optionally validate its match keys against
the live ``mit-bestand`` database in read-only mode.
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import gzip
import hashlib
import html.parser
import io
import json
import math
import mimetypes
import os
import re
import time
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

from PIL import Image, ImageChops, ImageDraw, ImageFont
import numpy as np


BASE = Path(__file__).resolve().parent
REPO = BASE.parents[2]
NETZ_ROOT = REPO / "_neo4j" / "netz"
PILOT = BASE / "bilder_pilot"
RAW = PILOT / "kandidaten"
FINAL = PILOT / "bilder"
SELECTION = PILOT / "selection.json"
DOMAINS = PILOT / "domains_review.json"
DOMAIN_DECISIONS = BASE / "pilot_domain_decisions.json"
REVIEW = PILOT / "asset_review.json"
ASSET_DECISIONS = BASE / "pilot_asset_decisions.json"
MANIFEST = PILOT / "pilot_transport_manifest.json"
PATCH = PILOT / "pilot_image_property_patch.json"
PATCH_REPORT = PILOT / "pilot_image_property_patch_report.md"
RENDER_CONTAINMENT_REPORT = PILOT / "render_containment_report.json"
WORKLIST = BASE / "worklist.json"
VERDICTS = BASE / "verdicts.json"
EXPORT = REPO / "actors_network.json"

COUNTRY_TARGETS = {
    "GB": {"graph": 12, "overlay": 4},
    "NL": {"graph": 12, "overlay": 4},
    "AT": {"graph": 11, "overlay": 5},
}
TYPE_ORDER = (
    "Software_Tool_Anbieter",
    "Oeffentliche_Institution",
    "Forschung_Lehre",
    "NGO_Verband_Netzwerk",
    "Materialhub_Bauteilboerse",
    "Unternehmen",
    "Foerdergeber_Programmtraeger",
    "Organisation",
    "Unbekannt",
)
BLOCKED_SUGGESTION_HOSTS = {
    "wikipedia.org", "wikimedia.org", "linkedin.com", "facebook.com",
    "instagram.com", "youtube.com", "vimeo.com", "researchgate.net",
    "archdaily.com", "dezeen.com", "springer.com", "mdpi.com",
}
# A number of official public-sector sites reject non-browser tokens before
# serving even their public HTML and logo files. Keep the project identifier
# while using a browser-compatible prefix so the reproducible collector sees
# the same public page as the human reviewer.
USER_AGENT = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
              "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0 Safari/537.36 "
              "Semio-actor-network-image-review/1.0")
MAX_DOWNLOAD = 12 * 1024 * 1024
FINAL_SIZE = 256
SAFE_RADIUS = 119.0  # 93% of the 128px node radius
SEMIO_DARK = (0, 17, 23)
SEMIO_LIGHT = (247, 243, 227)
NODE_RADIUS_MM = 2.275
IMAGE_DIAMETER_FRACTION = 1.00
PILOT_PDFS = {
    "light": NETZ_ROOT / "figs" / "_abb_pilot_light_fitted.pdf",
    "dark": NETZ_ROOT / "figs" / "_abb_pilot_dark_fitted.pdf",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def today():
    return dt.date.today().isoformat()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())


def stable_key(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def normalized_type(value) -> str:
    return value if value in TYPE_ORDER else "Unbekannt"


def node_key(cc: str, tid: str) -> str:
    return f"{cc}:{tid}"


def host_of(url: str) -> str:
    try:
        host = (urllib.parse.urlsplit(url).hostname or "").lower()
    except ValueError:
        return ""
    return host[4:] if host.startswith("www.") else host


def host_is_blocked(host: str) -> bool:
    return any(host == h or host.endswith("." + h) for h in BLOCKED_SUGGESTION_HOSTS)


def final_network():
    sys.path.insert(0, str(NETZ_ROOT))
    from netz.sources import DEFAULT
    from netz.data.prune import load_prune, load_edge_exclude
    from netz.model.concepts import build_network

    exclude = load_prune(DEFAULT.prune_path) | load_prune(DEFAULT.prune_faktencheck_path)
    edge_exclude = load_edge_exclude(DEFAULT.unklar_edges_path)
    return build_network(DEFAULT, exclude=exclude, edge_exclude=edge_exclude)


def round_robin(rows: list[dict], count: int) -> list[dict]:
    """Rotate types and alternate URL-present/URL-missing inside each type."""
    buckets = {}
    for typ in TYPE_ORDER:
        typed = [r for r in rows if normalized_type(r.get("typ")) == typ]
        if not typed:
            continue
        buckets[typ] = {
            True: collections.deque(sorted(
                (r for r in typed if r["url_present"]),
                key=lambda r: stable_key(r["key"]),
            )),
            False: collections.deque(sorted(
                (r for r in typed if not r["url_present"]),
                key=lambda r: stable_key(r["key"]),
            )),
            "prefer": True,
        }

    chosen = []
    while len(chosen) < count:
        progressed = False
        for typ in TYPE_ORDER:
            if typ not in buckets or len(chosen) >= count:
                continue
            b = buckets[typ]
            pref = b["prefer"]
            queue = b[pref] if b[pref] else b[not pref]
            if queue:
                chosen.append(queue.popleft())
                b["prefer"] = not pref
                progressed = True
        if not progressed:
            break
    if len(chosen) != count:
        raise RuntimeError(f"selection requested {count}, only {len(chosen)} available")
    return chosen


def command_select(_args):
    net = final_network()
    total = sum(len(p.actors) + len(p.projects) for p in net.panels.values())
    if total != 859:
        raise RuntimeError(f"final network drift: expected 859 drawn nodes, got {total}")

    work = load_json(WORKLIST)
    by_eid = {}
    for packet in work["packets"]:
        for row in packet.get("nodes", []):
            by_eid[row["eid"]] = row
    verdict_by_eid = {r["eid"]: r for r in load_json(VERDICTS)["nodes"] if r.get("eid")}

    selected = []
    for cc, targets in COUNTRY_TARGETS.items():
        rows = []
        for eid in net.panels[cc].actors:
            w = by_eid.get(eid, {})
            raw = net.raw.by.get(eid, {})
            props = raw.get("properties", {})
            sources = [u for u in ([w.get("primary_source_url")] + list(w.get("source_urls") or [])) if u]
            graph_backed = eid not in net.new_eids
            rows.append({
                "key": node_key(cc, net.tid[eid]),
                "cc": cc,
                "tid": net.tid[eid],
                "eid": eid,
                "graph_id": props.get("id") if graph_backed else None,
                "graph_backed": graph_backed,
                "name": net.raw.name(eid),
                "typ": normalized_type(w.get("typ")),
                "url_present": bool(sources),
                "source_urls": sources,
                "evidence_url": verdict_by_eid.get(eid, {}).get("beleg_url", ""),
            })
        graph_rows = [r for r in rows if r["graph_backed"]]
        overlay_rows = [r for r in rows if not r["graph_backed"]]
        if cc == "AT" and len(graph_rows) != 11:
            raise RuntimeError(f"AT graph-backed drift: expected 11, got {len(graph_rows)}")
        chosen = round_robin(graph_rows, targets["graph"])
        chosen += round_robin(overlay_rows, targets["overlay"])
        for r in chosen:
            r["selection_stratum"] = "graph" if r["graph_backed"] else "overlay"
        selected.extend(chosen)

    selected.sort(key=lambda r: (r["cc"], r["tid"]))
    if len(selected) != 48:
        raise AssertionError(len(selected))
    data = {
        "schema_version": 1,
        "created_at": today(),
        "graph_export": str(EXPORT.relative_to(REPO)).replace("\\", "/"),
        "graph_export_sha256": sha256_file(EXPORT),
        "drawn_network_nodes": total,
        "selection_policy": "GB/NL 12 graph + 4 overlay; AT 11 graph + 5 overlay; type round-robin; URL alternating; SHA-256 stable order",
        "nodes": selected,
    }
    write_json(SELECTION, data)
    print(f"wrote {SELECTION}: {len(selected)} nodes")


def suggested_official_url(row: dict) -> tuple[str, str]:
    for url in row.get("source_urls", []):
        host = host_of(url)
        if host and not host_is_blocked(host):
            root = urllib.parse.urlunsplit((urllib.parse.urlsplit(url).scheme or "https", host, "/", "", ""))
            return root, "worklist_source_candidate"
    return "", "manual_research_required"


def command_domains(_args):
    selection = load_json(SELECTION)
    existing = {}
    if DOMAINS.exists():
        existing = {r["key"]: r for r in load_json(DOMAINS).get("nodes", [])}
    decisions = load_json(DOMAIN_DECISIONS) if DOMAIN_DECISIONS.exists() else {}
    rows = []
    for node in selection["nodes"]:
        url, basis = suggested_official_url(node)
        row = existing.get(node["key"], {
            "key": node["key"],
            "name": node["name"],
            "official_url": url,
            "status": "needs_review",
            "basis": basis,
            "notes": "",
        })
        if node["key"] in decisions:
            row.update(decisions[node["key"]])
            row["key"] = node["key"]
            row["name"] = node["name"]
        rows.append(row)
    write_json(DOMAINS, {"schema_version": 1, "nodes": rows})
    print(f"wrote {DOMAINS}: {len(rows)} domain rows")


class IconParser(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.base = ""
        self.candidates = []
        self.stylesheets = []
        self.manifests = []
        self.header_depth = 0
        self.nav_depth = 0
        self.json_ld_depth = 0
        self.json_ld_parts = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        tag = tag.lower()
        if tag == "base" and a.get("href"):
            self.base = a["href"]
        if tag == "header":
            self.header_depth += 1
        if tag == "nav":
            self.nav_depth += 1
        if tag == "link" and a.get("href"):
            rel = set(a.get("rel", "").lower().split())
            if "stylesheet" in rel:
                self.stylesheets.append(a["href"])
            if "manifest" in rel:
                self.manifests.append(a["href"])
            if "apple-touch-icon" in rel or "apple-touch-icon-precomposed" in rel:
                self.candidates.append((1, "apple_touch", a["href"]))
            elif "icon" in rel or "shortcut" in rel or "mask-icon" in rel:
                self.candidates.append((2, "declared_icon", a["href"]))
        if tag == "meta" and a.get("content"):
            prop = (a.get("property") or a.get("name") or "").lower()
            if prop == "og:image":
                self.candidates.append((4, "og_image", a["content"]))
            if prop in {"twitter:image", "twitter:image:src", "msapplication-tileimage"}:
                self.candidates.append((4, "declared_icon", a["content"]))
        if tag in {"img", "source", "object", "embed"}:
            urls = [a.get(key, "") for key in ("src", "data-src", "data-lazy-src", "data-original", "data")]
            for srcset in (a.get("srcset", ""), a.get("data-srcset", "")):
                urls.extend(part.strip().split()[0] for part in srcset.split(",") if part.strip())
            marker = " ".join(a.values()).lower()
            identified = any(word in marker for word in ("logo", "brand", "wordmark", "logotype", "identity"))
            if identified or ((self.header_depth or self.nav_depth) and tag == "img"):
                self.candidates.extend((5, "header_logo", url) for url in urls if url)
        if tag == "script" and "ld+json" in a.get("type", "").lower():
            self.json_ld_depth = 1
            self.json_ld_parts = []

    def handle_data(self, data):
        if self.json_ld_depth:
            self.json_ld_parts.append(data)

    def handle_endtag(self, tag):
        if tag.lower() == "header" and self.header_depth:
            self.header_depth -= 1
        if tag.lower() == "nav" and self.nav_depth:
            self.nav_depth -= 1
        if tag.lower() == "script" and self.json_ld_depth:
            self.json_ld_depth = 0
            try:
                value = json.loads("".join(self.json_ld_parts))
            except (TypeError, ValueError):
                return
            for logo in structured_organisation_logos(value):
                self.candidates.append((4, "structured_logo", logo))


def structured_organisation_logos(value):
    """Return logo URLs only from JSON-LD organisation records."""
    output = []

    def visit(item):
        if isinstance(item, list):
            for child in item:
                visit(child)
            return
        if not isinstance(item, dict):
            return
        kind = item.get("@type", "")
        kinds = kind if isinstance(kind, list) else [kind]
        if any(str(entry).lower() in {"organization", "corporation", "governmentorganization"}
               for entry in kinds):
            logo = item.get("logo")
            if isinstance(logo, str):
                output.append(logo)
            elif isinstance(logo, dict):
                for key in ("url", "contentUrl"):
                    if isinstance(logo.get(key), str):
                        output.append(logo[key])
        for child in item.values():
            if isinstance(child, (dict, list)):
                visit(child)

    visit(value)
    return output


def css_header_logo_candidates(css_text: str, stylesheet_url: str):
    """Find image URLs used by header/navigation logo CSS rules."""
    output = []
    # Parse one flat rule at a time. The former unbounded selector regex could
    # backtrack quadratically on multi-megabyte minified bundles.
    for match in re.finditer(r"([^{}]{0,4096})\{([^{}]{0,131072})\}", css_text):
        selector, declarations = match.groups()
        if not re.search(r"logo|wordmark|brandmark", selector, re.I):
            continue
        for url_match in re.finditer(r"url\(\s*['\"]?([^)'\"]+)", declarations, re.I):
            output.append(urllib.parse.urljoin(stylesheet_url, html.unescape(url_match.group(1).strip())))
    return output


def request_bytes(url: str) -> tuple[bytes, str, str]:
    split = urllib.parse.urlsplit(url)
    referer = urllib.parse.urlunsplit((split.scheme or "https", split.netloc, "/", "", ""))
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT,
                                               "Accept": "image/*,text/html;q=0.9,*/*;q=0.5",
                                               "Accept-Encoding": "gzip",
                                               "Referer": referer})
    with urllib.request.urlopen(req, timeout=20) as response:
        content_type = response.headers.get_content_type()
        final_url = response.geturl()
        data = response.read(MAX_DOWNLOAD + 1)
        content_encoding = response.headers.get("Content-Encoding", "").lower()
    if len(data) > MAX_DOWNLOAD:
        raise ValueError("download exceeds 12 MiB")
    if content_encoding == "gzip" or data.startswith(b"\x1f\x8b"):
        data = gzip.decompress(data)
        if len(data) > MAX_DOWNLOAD:
            raise ValueError("decompressed download exceeds 12 MiB")
    return data, content_type, final_url


def discover_candidates(official_url: str):
    split = urllib.parse.urlsplit(official_url)
    root = urllib.parse.urlunsplit((split.scheme or "https", split.netloc, "/", "", ""))
    candidates = [
        (1, "apple_touch", urllib.parse.urljoin(root, "/apple-touch-icon.png")),
        (1, "apple_touch", urllib.parse.urljoin(root, "/apple-touch-icon-precomposed.png")),
        (2, "declared_icon", urllib.parse.urljoin(root, "/logo.svg")),
        (2, "declared_icon", urllib.parse.urljoin(root, "/logo.png")),
        (3, "favicon", urllib.parse.urljoin(root, "/favicon.ico")),
    ]
    page_error = ""
    try:
        data, content_type, final_url = request_bytes(official_url)
        if content_type == "text/html" or b"<html" in data[:1000].lower():
            parser = IconParser()
            # Headers, declared icons and manifests live at the beginning of
            # the document. Bounding parser input prevents modern sites with
            # multi-megabyte hydration payloads from stalling a batch.
            parser.feed(data[:3_000_000].decode("utf-8", errors="replace"))
            base = urllib.parse.urljoin(final_url, parser.base) if parser.base else final_url
            candidates.extend((p, k, urllib.parse.urljoin(base, u)) for p, k, u in parser.candidates)
            manifests = list(parser.manifests) + ["/site.webmanifest", "/manifest.json"]
            for manifest in manifests:
                try:
                    manifest_data, _, manifest_final = request_bytes(urllib.parse.urljoin(base, manifest))
                    manifest_value = json.loads(manifest_data.decode("utf-8", errors="replace"))
                    for icon in manifest_value.get("icons", []):
                        if isinstance(icon, dict) and icon.get("src"):
                            candidates.append((2, "declared_icon", urllib.parse.urljoin(manifest_final, icon["src"])))
                except Exception:
                    continue
            for stylesheet in parser.stylesheets[:6]:
                stylesheet_url = urllib.parse.urljoin(base, stylesheet)
                try:
                    css_data, css_type, css_final = request_bytes(stylesheet_url)
                    if css_type in {"text/css", "text/plain", "application/octet-stream"} or stylesheet_url.lower().split("?", 1)[0].endswith(".css"):
                        # Logo rules are normally in the primary application
                        # bundle. A deterministic bound keeps minified vendor
                        # CSS from dominating collection time and memory.
                        css_text = css_data[:2_000_000].decode("utf-8", errors="replace")
                        candidates.extend((5, "header_logo", url)
                                          for url in css_header_logo_candidates(css_text, css_final))
                except Exception:
                    continue
    except Exception as exc:
        page_error = f"{type(exc).__name__}: {exc}"
    seen, result = set(), []
    for priority, kind, url in sorted(candidates, key=lambda x: x[0]):
        clean = urllib.parse.urldefrag(url)[0]
        if clean and clean not in seen:
            seen.add(clean)
            result.append((priority, kind, clean))
    return result, page_error


def rasterize(data: bytes, content_type: str, source_url: str) -> tuple[Image.Image, str]:
    is_svg = content_type == "image/svg+xml" or source_url.lower().endswith(".svg") or data.lstrip().startswith(b"<svg")
    if is_svg:
        try:
            import cairosvg
        except ImportError as exc:
            raise RuntimeError("SVG candidate requires cairosvg") from exc
        # Supplying both dimensions would stretch non-square wordmarks.  One
        # target dimension keeps the SVG's intrinsic aspect ratio intact.
        data = cairosvg.svg2png(bytestring=data, output_width=512)
        return Image.open(io.BytesIO(data)).convert("RGBA"), "svg"
    im = Image.open(io.BytesIO(data))
    best = None
    for i in range(getattr(im, "n_frames", 1)):
        im.seek(i)
        frame = im.convert("RGBA")
        if best is None or frame.width * frame.height > best.width * best.height:
            best = frame.copy()
    return best, (im.format or mimetypes.guess_type(source_url)[0] or "raster").lower()


def safe_slug(key: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "_", key)


def command_harvest(args):
    selection = {r["key"]: r for r in load_json(SELECTION)["nodes"]}
    domains = {r["key"]: r for r in load_json(DOMAINS)["nodes"]}
    keys = sorted(selection)
    if args.key:
        keys = [args.key]
    for pos, key in enumerate(keys, 1):
        domain = domains[key]
        node_dir = RAW / selection[key]["cc"] / selection[key]["tid"]
        node_dir.mkdir(parents=True, exist_ok=True)
        meta = {"key": key, "official_url": domain.get("official_url", ""), "page_error": "", "candidates": []}
        if domain.get("status") != "accepted" or not domain.get("official_url"):
            meta["page_error"] = "domain not accepted"
            write_json(node_dir / "candidates.json", meta)
            print(f"[{pos}/{len(keys)}] {key}: no accepted domain")
            continue
        candidates, page_error = discover_candidates(domain["official_url"])
        meta["page_error"] = page_error
        for idx, (priority, kind, url) in enumerate(candidates, 1):
            record = {"id": f"c{idx:02d}", "priority": priority, "kind": kind, "url": url, "status": "rejected", "reason": ""}
            try:
                data, content_type, final_url = request_bytes(url)
                im, fmt = rasterize(data, content_type, final_url)
                record.update({"final_url": final_url, "content_type": content_type, "format": fmt,
                               "width": im.width, "height": im.height})
                if fmt != "svg" and min(im.size) < 128:
                    record["reason"] = "short edge below 128px"
                else:
                    preview = node_dir / f"{record['id']}_{kind}.png"
                    im.save(preview, "PNG")
                    record["preview_path"] = str(preview.relative_to(PILOT)).replace("\\", "/")
                    record["status"] = "candidate"
                    record["reason"] = ""
            except Exception as exc:
                record["reason"] = f"{type(exc).__name__}: {exc}"
            meta["candidates"].append(record)
        write_json(node_dir / "candidates.json", meta)
        good = sum(r["status"] == "candidate" for r in meta["candidates"])
        print(f"[{pos}/{len(keys)}] {key}: {good}/{len(meta['candidates'])} usable candidates")


def font(size=18):
    for path in (Path("C:/Windows/Fonts/arial.ttf"), Path("C:/Windows/Fonts/segoeui.ttf")):
        if path.exists():
            return ImageFont.truetype(str(path), size)
    return ImageFont.load_default()


def command_contact(_args):
    selection = load_json(SELECTION)["nodes"]
    review_rows = []
    sheets = []
    for page_no, start in enumerate(range(0, len(selection), 12), 1):
        page = Image.new("RGB", (4 * 260, 12 * 190), "#f7f3e3")
        draw = ImageDraw.Draw(page)
        for row_no, node in enumerate(selection[start:start + 12]):
            meta_path = RAW / node["cc"] / node["tid"] / "candidates.json"
            meta = load_json(meta_path) if meta_path.exists() else {"candidates": []}
            candidates = [c for c in meta["candidates"] if c.get("status") == "candidate"][:4]
            review_rows.append({"key": node["key"], "result": "pending", "candidate_id": "", "notes": ""})
            y = row_no * 190
            draw.text((4, y + 4), f"{node['key']}  {node['name'][:31]}", fill="#001117", font=font(16))
            for col in range(4):
                x = col * 260
                if col >= len(candidates):
                    draw.rectangle((x + 55, y + 34, x + 205, y + 184), outline="#7b827d")
                    continue
                c = candidates[col]
                path = PILOT / c["preview_path"]
                im = Image.open(path).convert("RGBA")
                im.thumbnail((140, 120), Image.Resampling.LANCZOS)
                tile = Image.new("RGBA", (150, 125), "white")
                tile.alpha_composite(im, ((150 - im.width) // 2, (125 - im.height) // 2))
                page.paste(tile.convert("RGB"), (x + 55, y + 34))
                draw.text((x + 58, y + 160), f"{c['id']} {c['kind']}", fill="#001117", font=font(14))
        out = PILOT / f"contact_sheet_{page_no}.png"
        page.save(out)
        sheets.append(out)
    existing = {}
    if REVIEW.exists():
        existing = {r["key"]: r for r in load_json(REVIEW).get("nodes", [])}
    decisions = load_json(ASSET_DECISIONS) if ASSET_DECISIONS.exists() else {}
    for row in review_rows:
        if row["key"] in existing:
            row.update(existing[row["key"]])
        if row["key"] in decisions:
            row.update(decisions[row["key"]])
    write_json(REVIEW, {"schema_version": 1, "nodes": review_rows})
    print("wrote contact sheets: " + ", ".join(str(p) for p in sheets))
    print(f"wrote {REVIEW}")


def remove_edge_background(im: Image.Image) -> Image.Image:
    im = im.convert("RGBA")
    if im.getbbox() is None:
        return im
    corners = [im.getpixel((0, 0)), im.getpixel((im.width - 1, 0)),
               im.getpixel((0, im.height - 1)), im.getpixel((im.width - 1, im.height - 1))]
    if any(a < 250 for _, _, _, a in corners):
        return im
    bg = tuple(sum(p[i] for p in corners) // 4 for i in range(3))
    pix = im.load()
    queue = collections.deque()
    seen = set()
    for x in range(im.width):
        queue.append((x, 0)); queue.append((x, im.height - 1))
    for y in range(im.height):
        queue.append((0, y)); queue.append((im.width - 1, y))
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x, y))
        r, g, b, a = pix[x, y]
        if a < 8 or max(abs(r - bg[0]), abs(g - bg[1]), abs(b - bg[2])) <= 8:
            pix[x, y] = (r, g, b, 0)
            if x: queue.append((x - 1, y))
            if y: queue.append((x, y - 1))
            if x + 1 < im.width: queue.append((x + 1, y))
            if y + 1 < im.height: queue.append((x, y + 1))
    return im


# Tuned against the real 2026-08 circle_cover set (56 assets), not guessed.
# Each value is named because the classification moves under small changes to
# any of them -- two assets sit within 1% of the tolerance-14 boundary alone.
EXTEND_FLOOD_TOLERANCE = 14     # Chebyshev RGB step, LOCAL per BFS hop
EXTEND_WORKING_SIZE = 256       # long edge of the downsampled copy the flood
                                # runs on; mirrors neutral_edge_backdrop's own
                                # 128px sample, both for speed (a Python BFS
                                # over BOBI Réemploi's 2314x1000 source took
                                # 5.7s; this pipeline calls the same
                                # computation once per browser request in the
                                # review server) and to blur past JPEG noise
EXTEND_MARGIN = 0.96            # target radius = 128 * this; leaves ~5px so
                                # an antialiased mark edge doesn't graze the
                                # circle's own antialiasing
EXTEND_MAX_FOREGROUND = 0.85    # above this fraction the flood never
                                # travelled -- it did not find a backdrop, it
                                # found almost the whole tile (measured:
                                # Allibert Matériaux Anciens reaches 0.966)
EXTEND_CLEAN_ALPHA = 250        # what counts as "opaque" when hunting for a
                                # replicable edge pixel, matching the alpha
                                # threshold has_flat_opaque_backdrop already
                                # uses for its four-corner test


def _flood_background_mask(im: Image.Image, tolerance: int = EXTEND_FLOOD_TOLERANCE,
                            working_size: int = EXTEND_WORKING_SIZE) -> "np.ndarray":
    """Boolean mask, `im`-sized, of pixels reachable from the border by LOCAL
    colour similarity -- the actual background, not just "far from one fixed
    reference colour".

    A neighbour joins the background if it is transparent (alpha<24) or its
    RGB is within `tolerance` of the ALREADY-background pixel it was reached
    from, not of a single global reference. That local chaining is what lets
    a two-tone tile (one colour band over a second, e.g. Van der Wal
    Sloopwerken's red-over-yellow) register as background end to end --
    `remove_edge_background` above compares every pixel against one fixed
    corner-mean colour with tolerance 8 and would only ever knock out ONE of
    the two bands.

    Vectorised as a fixed-point iteration (repeated one-pixel shifts, ORed
    in) rather than a Python queue: a pure-Python BFS is the actual bottleneck
    on a multi-megapixel source and this function also runs live from the
    review server's HTTP handler. Runs on a downsampled working copy (long
    edge `working_size`) and the mask is upsampled back with nearest-neighbour
    so it stays a hard boolean, then resized to the input's exact size.
    """
    original_size = im.size
    scale = min(1.0, working_size / max(original_size))
    work = im.resize((max(1, round(original_size[0] * scale)),
                      max(1, round(original_size[1] * scale))),
                     Image.Resampling.LANCZOS) if scale < 1.0 else im
    array = np.asarray(work.convert("RGBA"))
    height, width = array.shape[:2]
    rgb = array[:, :, :3].astype(np.int16)
    transparent = array[:, :, 3] < 24
    background = transparent.copy()
    background[0, :] = True
    background[-1, :] = True
    background[:, 0] = True
    background[:, -1] = True

    for _ in range(height + width):  # worst case: a single-pixel-wide chain
        grew = False
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            src = np.roll(background, (dy, dx), axis=(0, 1))
            base = np.roll(rgb, (dy, dx), axis=(0, 1))
            close = (np.abs(rgb - base).max(axis=2) <= tolerance) & src & ~background
            close |= transparent & ~background
            if close.any():
                background |= close
                grew = True
        if not grew:
            break

    if work is not im:
        mask_image = Image.fromarray(background.astype(np.uint8) * 255, "L")
        mask_image = mask_image.resize(original_size, Image.Resampling.NEAREST)
        background = np.asarray(mask_image) > 0
    return background


def _extend_geometry(im: Image.Image, background: "np.ndarray",
                      margin: float = EXTEND_MARGIN) -> float | None:
    """Fit-scale for `im` given its background mask, or None if extending is
    not safe -- callers keep the historical cover crop in every None case.

    None covers every way the flood mask fails to mean "the mark": no
    foreground at all (the mark touches the frame and floods away with it --
    e.g. Provincie Gelderland), or near-total foreground (the flood never
    left the border -- e.g. Allibert Matériaux Anciens at 96.6%, which is a
    "no real backdrop found" result, not a "the whole tile is the mark"
    result). Measured against the mark's own bounding radius from the image
    centre, never against the tile's background -- a square brand tile must
    not shrink by root two just to tuck its own coloured CORNERS inside the
    circle, only as far as its lettering actually demands.
    """
    foreground = ~background
    total = foreground.size
    if total == 0:
        return None
    coverage = float(foreground.sum()) / total
    if coverage <= 0.0 or coverage > EXTEND_MAX_FOREGROUND:
        return None
    ys, xs = np.nonzero(foreground)
    cy, cx = (im.height - 1) / 2.0, (im.width - 1) / 2.0
    radius = float(np.hypot(xs - cx, ys - cy).max())
    if radius <= 0:
        return None
    return (FINAL_SIZE / 2.0 * margin) / radius


def _clean_edge_line(background: "np.ndarray", alpha: "np.ndarray", axis: int,
                      from_start: bool) -> "np.ndarray | None":
    """Per row (axis=0) or column (axis=1), the first pixel INDEX walking
    inward from that edge that is both background-classified and opaque
    (alpha >= EXTEND_CLEAN_ALPHA) -- or None if any row/column has no such
    pixel at all.

    `_opaque_bounds` only guarantees ONE opaque pixel per boundary line, not
    the whole line: measured on the real set, 14 of 56 circle_cover sources
    still carry a partly transparent outer ring after that crop, five of them
    (including Allibert and DRZ) fully transparent along an entire edge.
    Replicating that literal edge with `np.pad(mode="edge")` was the first
    version of this function and it produced exactly the artefact this whole
    change exists to prevent: a 72-column alpha-11 wedge on one asset, a
    translucent alpha 179-217 ring on another -- the report's node fill
    showing through what should be a solid disc. Walking inward to a genuinely
    opaque background pixel is what "replicated" is allowed to mean.
    """
    h, w = background.shape
    length = h if axis == 1 else w
    depth = w if axis == 1 else h
    opaque = alpha >= EXTEND_CLEAN_ALPHA
    clean = background & opaque
    order = clean if from_start else np.flip(clean, axis=axis)
    first = np.argmax(order, axis=axis)
    found = np.take_along_axis(order, np.expand_dims(first, axis), axis=axis).squeeze(axis)
    if not bool(found.all()):
        return None
    if not from_start:
        first = depth - 1 - first
    return first


def _running_median(values: "np.ndarray", window: int = 9) -> "np.ndarray":
    """Odd-window running median along a 1-D (or last-axis) array, edges held
    by clamped padding. Kills single-pixel JPEG/dither outliers in a
    replicated edge line without smearing an intentional gradient -- BOBI
    Réemploi's backdrop is one, and a median (unlike a mean) does not blur it."""
    pad = window // 2
    padded = np.pad(values, [(0, 0)] * (values.ndim - 1) + [(pad, pad)], mode="edge")
    stack = np.stack([padded[..., i:i + values.shape[-1]] for i in range(window)], axis=-1)
    return np.median(stack, axis=-1)


def _extend_backdrop_to_canvas(im: Image.Image, background: "np.ndarray",
                                scale: float) -> Image.Image | None:
    """Scale `im` by `scale`, then bring it to exactly FINAL_SIZE x FINAL_SIZE
    by replicating a CLEAN (opaque, background-classified, median-smoothed)
    edge line outward on any side that still falls short -- never a foreign
    fill colour, never the raw possibly-translucent border. Centre-crops any
    side that already exceeds FINAL_SIZE (`_extend_geometry` guarantees only
    background can still overhang there, never the mark). Returns None if any
    side needing extension has no clean edge at all -- caller falls back to
    the historical cover crop for that source.
    """
    new_size = (max(1, round(im.width * scale)), max(1, round(im.height * scale)))
    resized = im.resize(new_size, Image.Resampling.LANCZOS)
    mask = _flood_background_mask(resized)
    array = np.asarray(resized.convert("RGBA")).astype(np.int32)

    def extend_rows(a, m, depth, at_top):
        """Add `depth` replicated rows at the top or bottom of `a`."""
        row = _clean_edge_line(m, a[:, :, 3], axis=0, from_start=at_top)  # one index per COLUMN
        if row is None:
            return None, None
        cols = np.arange(a.shape[1])
        edge = _running_median(a[row, cols, :].astype(np.float64).T).T
        edge[:, 3] = 255  # a translucent ring is worse than none
        band = np.broadcast_to(edge.astype(np.int32)[None, :, :], (depth, a.shape[1], 4)).copy()
        mask_band = np.ones((depth, a.shape[1]), dtype=bool)  # replicated pixels ARE background
        return ((np.concatenate([band, a], axis=0), np.concatenate([mask_band, m], axis=0)) if at_top
                else (np.concatenate([a, band], axis=0), np.concatenate([m, mask_band], axis=0)))

    def extend_cols(a, m, depth, at_left):
        """Add `depth` replicated columns at the left or right of `a`."""
        col = _clean_edge_line(m, a[:, :, 3], axis=1, from_start=at_left)  # one index per ROW
        if col is None:
            return None, None
        rows = np.arange(a.shape[0])
        edge = _running_median(a[rows, col, :].astype(np.float64).T).T
        edge[:, 3] = 255
        band = np.broadcast_to(edge.astype(np.int32)[:, None, :], (a.shape[0], depth, 4)).copy()
        mask_band = np.ones((a.shape[0], depth), dtype=bool)
        return ((np.concatenate([band, a], axis=1), np.concatenate([mask_band, m], axis=1)) if at_left
                else (np.concatenate([a, band], axis=1), np.concatenate([m, mask_band], axis=1)))

    def fit(a, m, axis, extend_before, extend_after):
        current = a.shape[axis]
        if current > FINAL_SIZE:
            start = (current - FINAL_SIZE) // 2
            index = [slice(None)] * a.ndim
            index[axis] = slice(start, start + FINAL_SIZE)
            return a[tuple(index)], m[tuple(index[:2])]
        if current == FINAL_SIZE:
            return a, m
        before = (FINAL_SIZE - current) // 2
        after = FINAL_SIZE - current - before
        if before:
            a, m = extend_before(a, m, before)
            if a is None:
                return None, None
        if after:
            a, m = extend_after(a, m, after)
            if a is None:
                return None, None
        return a, m

    array, mask = fit(array, mask, 0, lambda a, m, d: extend_rows(a, m, d, True),
                      lambda a, m, d: extend_rows(a, m, d, False))
    if array is None:
        return None
    array, mask = fit(array, mask, 1, lambda a, m, d: extend_cols(a, m, d, True),
                      lambda a, m, d: extend_cols(a, m, d, False))
    if array is None:
        return None
    return Image.fromarray(array.astype(np.uint8), "RGBA")


def is_opaque_tile(im: Image.Image) -> bool:
    """Return whether the artwork is a solid square tile, corners aside.

    The corner test in `has_flat_opaque_backdrop` misses two very common tile
    shapes: a rounded-corner app icon (its four corners are transparent, so the
    alpha check rejects it) and a tile whose corners carry different colours
    (so the tolerance check rejects it).  Both then went through `safe_contain`,
    which shrinks the artwork inside the node circle -- and a shrunk tile reads
    as a rectangular plate floating in the node, which is exactly what a node
    logo must never look like.  Measured on the 2026-08 set: 14 of 343.

    Deliberately narrow.  A freestanding wordmark or emblem never fills 92 % of
    a bounding box that itself covers 90 % of the frame; those keep the contain
    treatment so their artwork is never cut.  This test is reached only after
    `neutral_edge_backdrop`, so a white/black backdrop still goes through the
    knockout branch and keeps its light/dark tokenisation.

    Aspect ratio is deliberately NOT part of the test.  A wide banner of solid
    brand colour is the same defect as a square one -- 7 further sources are
    exactly that, and requiring a near-square box left them contained.  A banner
    cover-cropped to the circle loses the ends of its wordmark, but a wordmark is
    unreadable at 4.55 mm either way, and a clean brand-coloured disc is what the
    node is meant to show.
    """
    im = im.convert("RGBA")
    if im.width < 2 or im.height < 2:
        return False
    alpha = np.asarray(im.getchannel("A"))
    ys, xs = np.nonzero(alpha > 24)
    if xs.size == 0:
        return False
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    width, height = x1 - x0 + 1, y1 - y0 + 1
    # 0.88, not 0.92: a squircle app icon fills about 0.90 of its box, and at
    # 0.92 the one squircle in this set stayed contained.  A true circle fills
    # 0.785 and needs no cover treatment, so the band between is empty --
    # measured: 0.900, then 0.842, 0.803, then a cluster at 0.785.
    covers_frame = (width * height) / (im.width * im.height) >= 0.90
    fills_box = float((alpha[y0:y1 + 1, x0:x1 + 1] > 24).mean()) >= 0.88
    return bool(covers_frame and fills_box)


def has_flat_opaque_backdrop(im: Image.Image, tolerance: int = 18) -> bool:
    """Return whether the source has a real, approximately solid rectangular backdrop.

    Such a backdrop is source material, not a synthesized fill.  It should be
    scaled as a cover image and cropped by the node circle so coloured logo
    tiles can occupy the complete node.  Transparent/freestanding marks keep
    the historical contain treatment so their actual artwork is never cut.

    Two acceptance paths: the historical four-corner test, and `is_opaque_tile`
    for the rounded/multi-coloured tiles that test cannot see.
    """
    im = im.convert("RGBA")
    if im.width < 2 or im.height < 2:
        return False
    corners = [im.getpixel((0, 0)), im.getpixel((im.width - 1, 0)),
               im.getpixel((0, im.height - 1)), im.getpixel((im.width - 1, im.height - 1))]
    if all(pixel[3] >= 250 for pixel in corners) and all(
            max(pixel[channel] for pixel in corners) - min(pixel[channel] for pixel in corners) <= tolerance
            for channel in range(3)):
        return True
    return is_opaque_tile(im)


def neutral_edge_backdrop(im: Image.Image) -> tuple[str, int] | None:
    """Detect a dominant light/dark neutral backdrop touching the source edge.

    Border clustering is used instead of corner equality because wide
    wordmarks may touch two corners, as in the English Salvage source.
    Coloured tiles are deliberately excluded and continue through circle-cover.
    """
    im = im.convert("RGBA")
    if im.width < 2 or im.height < 2:
        return None
    border = ([im.getpixel((x, 0)) for x in range(im.width)] +
              [im.getpixel((x, im.height - 1)) for x in range(im.width)] +
              [im.getpixel((0, y)) for y in range(1, im.height - 1)] +
              [im.getpixel((im.width - 1, y)) for y in range(1, im.height - 1)])
    neutral_luminances = []
    buckets = collections.Counter()
    for r, g, b, a in border:
        if a < 250 or max(r, g, b) - min(r, g, b) > 20:
            continue
        luminance = round((299 * r + 587 * g + 114 * b) / 1000)
        neutral_luminances.append(luminance)
        buckets[luminance // 16] += 1
    if not buckets:
        return None
    bucket, count = buckets.most_common(1)[0]
    if count < max(8, round(len(border) * 0.12)):
        return None
    cluster = sorted(value for value in neutral_luminances if abs(value // 16 - bucket) <= 1)
    backdrop = cluster[len(cluster) // 2]
    appearance = "light" if backdrop >= 184 else "dark" if backdrop <= 72 else None
    if appearance is None:
        return None

    # Require the neutral backdrop to be a material part of the rectangle;
    # this prevents a pale strip around a photograph from flattening the photo.
    sample = im.resize((min(128, im.width), min(128, im.height)), Image.Resampling.BILINEAR)
    sample_pixels = np.asarray(sample, dtype=np.int32)
    sample_rgb = sample_pixels[:, :, :3]
    sample_luminance = ((299 * sample_rgb[:, :, 0] + 587 * sample_rgb[:, :, 1] +
                         114 * sample_rgb[:, :, 2] + 500) // 1000)
    opaque_mask = sample_pixels[:, :, 3] >= 220
    neutral_mask = (sample_rgb.max(axis=2) - sample_rgb.min(axis=2) <= 24) & opaque_mask
    near_mask = neutral_mask & (np.abs(sample_luminance - backdrop) <= 24)
    total = sample.width * sample.height
    if int(opaque_mask.sum()) / total < 0.95:
        return None
    neutral = int(neutral_mask.sum())
    near_backdrop = int(near_mask.sum())
    if neutral / total < 0.55 or near_backdrop / total < 0.18:
        return None
    return appearance, backdrop


def neutral_backdrop_to_transparency(im: Image.Image, theme: str, backdrop: tuple[str, int]) -> Image.Image:
    """Knock out a neutral rectangle and tokenise its neutral foreground."""
    if theme not in {"light", "dark"}:
        raise ValueError(f"unsupported theme: {theme}")
    im = im.convert("RGBA")
    appearance, backdrop_luminance = backdrop
    pixels = np.array(im, dtype=np.uint8)
    rgb = pixels[:, :, :3].astype(np.int32)
    luminance = ((299 * rgb[:, :, 0] + 587 * rgb[:, :, 1] + 114 * rgb[:, :, 2] + 500) // 1000)
    neutral_mask = ((rgb.max(axis=2) - rgb.min(axis=2)) <= 32) & (pixels[:, :, 3] >= 8)
    neutral_values = luminance[neutral_mask]
    if neutral_values.size == 0:
        raise ValueError("neutral backdrop has no foreground")
    if appearance == "light":
        foreground_luminance = int(np.quantile(neutral_values, 0.04, method="nearest"))
        span = max(48, backdrop_luminance - foreground_luminance)
    else:
        foreground_luminance = int(np.quantile(neutral_values, 0.96, method="nearest"))
        span = max(48, foreground_luminance - backdrop_luminance)
    token = SEMIO_DARK if theme == "light" else SEMIO_LIGHT
    output = np.zeros_like(pixels)
    coloured_mask = (~neutral_mask) & (pixels[:, :, 3] >= 8)
    output[coloured_mask] = pixels[coloured_mask]
    output[neutral_mask, :3] = token
    delta = (backdrop_luminance - luminance if appearance == "light"
             else luminance - backdrop_luminance)
    coverage = np.clip(delta.astype(np.float32) / span, 0.0, 1.0)
    output[:, :, 3][neutral_mask] = np.rint(pixels[:, :, 3][neutral_mask] * coverage[neutral_mask]).astype(np.uint8)
    return Image.fromarray(output, "RGBA")


def tokenise_transparent_neutral_mark(im: Image.Image, theme: str) -> Image.Image:
    """Theme-tokenise a predominantly neutral mark on transparency."""
    if theme not in {"light", "dark"}:
        raise ValueError(f"unsupported theme: {theme}")
    pixels = np.array(im.convert("RGBA"), dtype=np.uint8)
    visible = pixels[:, :, 3] >= 8
    if not visible.any():
        return im.convert("RGBA")
    rgb = pixels[:, :, :3].astype(np.int32)
    neutral = visible & ((rgb.max(axis=2) - rgb.min(axis=2)) <= 32)
    if int(neutral.sum()) / int(visible.sum()) < 0.85:
        return im.convert("RGBA")
    token = SEMIO_DARK if theme == "light" else SEMIO_LIGHT
    output = pixels.copy()
    output[neutral, :3] = token
    return Image.fromarray(output, "RGBA")


def blacken_to_ink(im: Image.Image, ink: tuple[int, int, int] = SEMIO_DARK,
                    luminance_max: int = 70, chroma_max: int = 40) -> Image.Image:
    """Recolour only near-black pixels to `ink`; every other pixel is untouched.

    Unlike `tokenise_transparent_neutral_mark`, this is unconditional and
    per-pixel -- it does not require 85% of the mark to be neutral before it
    acts.  That gate exists so a genuinely coloured logo is never recoloured
    wholesale; this function is for the opposite case, where a logo is MOSTLY
    saturated brand colour but carries a thin black tagline or icon stroke
    that the 85% rule correctly leaves alone.  Only used together with a baked
    light backdrop (see `prepare_light_backdrop_canvas`): once the backdrop no
    longer depends on the report's theme, black elements just need to read as
    ink, not be inverted per theme the way `tokenise_transparent_neutral_mark`
    inverts a fully neutral mark.
    """
    pixels = np.array(im.convert("RGBA"), dtype=np.uint8)
    visible = pixels[:, :, 3] >= 8
    rgb = pixels[:, :, :3].astype(np.int32)
    luminance = 0.299 * rgb[:, :, 0] + 0.587 * rgb[:, :, 1] + 0.114 * rgb[:, :, 2]
    chroma = rgb.max(axis=2) - rgb.min(axis=2)
    near_black = visible & (luminance <= luminance_max) & (chroma <= chroma_max)
    output = pixels.copy()
    output[near_black, :3] = ink
    return Image.fromarray(output, "RGBA")


def apply_circle_crop(im: Image.Image) -> Image.Image:
    """Mask a 256px node asset to its final circle with antialiased edges."""
    im = im.convert("RGBA")
    if im.size != (FINAL_SIZE, FINAL_SIZE):
        raise ValueError(f"circle crop expects {FINAL_SIZE}x{FINAL_SIZE}, got {im.size}")
    supersample = 4
    mask_size = FINAL_SIZE * supersample
    mask = Image.new("L", (mask_size, mask_size), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, mask_size - 1, mask_size - 1), fill=255)
    mask = mask.resize((FINAL_SIZE, FINAL_SIZE), Image.Resampling.LANCZOS)
    im.putalpha(ImageChops.multiply(im.getchannel("A"), mask))
    return im


def contain_node_artwork(im: Image.Image, mode: str,
                          backdrop: tuple[int, int, int] | None = None) -> tuple[Image.Image, str]:
    """Trim and contain already-separated artwork within the radial safety area.

    `backdrop`, when given, fills the canvas opaquely before the artwork is
    composited on top -- used by `prepare_light_backdrop_canvas` so the disc
    is opaque light in both light and dark builds, rather than transparent
    and dependent on whatever the node fill happens to be.  `apply_circle_crop`
    still clears everything outside the circle to alpha 0 regardless, since it
    multiplies the existing alpha by the mask rather than assuming it.
    """
    bbox = im.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("candidate has no visible pixels")
    im = im.crop(bbox)
    scale = min((SAFE_RADIUS * 2) / im.width, (SAFE_RADIUS * 2) / im.height)
    im = im.resize((max(1, round(im.width * scale)), max(1, round(im.height * scale))),
                   Image.Resampling.LANCZOS)
    fill = (backdrop + (255,)) if backdrop else (0, 0, 0, 0)
    canvas = Image.new("RGBA", (FINAL_SIZE, FINAL_SIZE), fill)
    canvas.alpha_composite(im, ((FINAL_SIZE - im.width) // 2, (FINAL_SIZE - im.height) // 2))
    max_r = alpha_max_radius(canvas)
    if max_r > SAFE_RADIUS:
        ratio = (SAFE_RADIUS - 1.0) / max_r
        im = im.resize((max(1, int(im.width * ratio)), max(1, int(im.height * ratio))),
                      Image.Resampling.LANCZOS)
        canvas = Image.new("RGBA", (FINAL_SIZE, FINAL_SIZE), fill)
        canvas.alpha_composite(im, ((FINAL_SIZE - im.width) // 2, (FINAL_SIZE - im.height) // 2))
    return apply_circle_crop(canvas), mode


def save_png(canvas: Image.Image, dest: Path, attempts: int = 6):
    """Write a PNG, tolerating a transient lock on the destination.

    finalize writes ~420 files back to back; on this Windows box a real-time
    scanner intermittently still holds the file it just saw, and the next
    `open(..., "w+b")` fails with EINVAL.  The failing name moved from run to
    run, which is what rules out a bad image and rules in the scanner.  Writing
    to a sibling temp file and renaming keeps the destination valid at every
    moment, and the short backoff covers the scan window.
    """
    dest.parent.mkdir(parents=True, exist_ok=True)
    tmp = dest.with_name(dest.name + ".part")
    last = None
    for attempt in range(attempts):
        try:
            canvas.save(tmp, "PNG", optimize=True)
            os.replace(tmp, dest)
            return
        except OSError as error:
            last = error
            time.sleep(0.05 * (attempt + 1))
    tmp.unlink(missing_ok=True)
    raise OSError(f"{dest}: still unwritable after {attempts} attempts ({last})")


def _opaque_bounds(im: Image.Image) -> tuple[int, int, int, int]:
    """(left, upper, right, lower) of the visibly opaque artwork, PIL-crop style."""
    alpha = np.asarray(im.convert("RGBA"))[:, :, 3]
    ys, xs = np.nonzero(alpha > 24)
    if xs.size == 0:
        return (0, 0, im.width, im.height)
    return (int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1)


def is_solid_colour_block(im: Image.Image) -> bool:
    """Return whether the opaque artwork is one solid, saturated square block.

    Used to tell a coloured brand tile that merely sits on a white page margin
    from a wordmark that sits on a white background.  Once the neutral margin is
    knocked out, the tile leaves a filled square and the wordmark leaves
    letterforms, so the fill ratio of the bounding box separates them cleanly:
    measured on the 2026-08 set, the one tile scores 0.99 fill / 1.00 chroma and
    the next candidate 0.75 fill / 0.00 chroma.  Nothing sits in between.
    """
    im = im.convert("RGBA")
    array = np.asarray(im)
    alpha = array[:, :, 3]
    ys, xs = np.nonzero(alpha > 24)
    if xs.size == 0:
        return False
    x0, x1, y0, y1 = int(xs.min()), int(xs.max()), int(ys.min()), int(ys.max())
    width, height = x1 - x0 + 1, y1 - y0 + 1
    if max(width, height) / min(width, height) > 1.15:
        return False
    if float((alpha[y0:y1 + 1, x0:x1 + 1] > 24).mean()) < 0.92:
        return False
    rgb = array[:, :, :3][alpha > 24].astype(np.int32)
    saturation = rgb.max(axis=1) - rgb.min(axis=1)
    return bool(float(np.mean(saturation > 40)) >= 0.5)


def prepare_light_backdrop_canvas(source: Path) -> Image.Image:
    """Bake a permanent light backdrop behind a mark that reads poorly on the
    report's dark-theme node canvas, and recolour only its near-black pixels.

    Used exclusively for the fixed override list in `dark_backdrop_overrides
    .json`: marks whose own colours are dark enough that neither automatic
    path gets them right. `safe_contain` never generates a dark variant at
    all -- the light file is reused unchanged in the dark build, so a dark
    logo simply disappears against the near-black canvas. `neutral_knockout`
    does generate one, but `neutral_backdrop_to_transparency` only recolours
    the neutral (grayscale) part of a mark; any dark SATURATED brand colour
    is passed through unchanged in `coloured_mask` and is just as invisible.

    Baking a light disc sidesteps the theme dependency entirely instead of
    trying to out-guess it per mark: the resulting file is correct in both
    builds, so `command_finalize` does not generate a `-dark` sibling for it.
    """
    original = Image.open(source).convert("RGBA")
    neutral_backdrop = neutral_edge_backdrop(original)
    if neutral_backdrop is not None:
        separated = neutral_backdrop_to_transparency(original, "light", neutral_backdrop)
        if is_solid_colour_block(separated):
            original = original.crop(_opaque_bounds(separated))
            separated = remove_edge_background(original)
    else:
        separated = remove_edge_background(original)
    separated = blacken_to_ink(separated)
    canvas, _ = contain_node_artwork(separated, "light_backdrop", backdrop=SEMIO_LIGHT)
    return canvas


def prepare_node_canvas(source: Path, theme: str = "light") -> tuple[Image.Image, str]:
    """Prepare a node asset using circle-cover or safe contain as appropriate."""
    original = Image.open(source).convert("RGBA")
    neutral_backdrop = neutral_edge_backdrop(original)
    if neutral_backdrop is not None:
        # The solid-colour-block DECISION and its crop bounds are always taken
        # against the light rendering, regardless of which theme was actually
        # requested: light and dark calls must land on the same branch here or
        # `command_finalize` raises "theme crop modes differ" mid-run, having
        # already written some of 343 files. R-Place is currently the one
        # asset that reaches this sub-path at all; its light/dark separations
        # happen to already agree, which is luck, not a guarantee -- this
        # makes the agreement structural instead.
        reference = neutral_backdrop_to_transparency(original, "light", neutral_backdrop)
        # A coloured tile on a white page margin is NOT a neutral-backdrop mark.
        # Knocking it out contains the tile inside the circle (a rectangular
        # plate) and runs the brand colours through the light/dark tokeniser,
        # which recolours them -- R-Place shipped indigo/orange as
        # periwinkle/salmon in light and navy/brown in dark.  Fall through to
        # circle-cover instead: the colours stay exactly as the source has them
        # and both themes show the same tile.
        if not is_solid_colour_block(reference):
            separated = (reference if theme == "light"
                        else neutral_backdrop_to_transparency(original, theme, neutral_backdrop))
            return contain_node_artwork(separated, "neutral_knockout")
        # Cover the circle with the TILE, not with the page it sits on. The
        # knockout has already found the tile's edge, so reuse that bounding box
        # -- covering the untrimmed source would just centre the plate on a
        # white disc, which is the same defect one step later.
        original = original.crop(_opaque_bounds(reference))
    if has_flat_opaque_backdrop(original):
        cover_scale = max(FINAL_SIZE / original.width, FINAL_SIZE / original.height)
        # Do not cut the MARK (text/icon) to cover the frame -- shrink just
        # far enough that the mark itself fits, and replicate the tile's own
        # background outward to refill the disc. Measured against the mark
        # alone, never the background: a square tile must not shrink by root
        # two just to tuck its own coloured corners inside the circle.
        background = _flood_background_mask(original)
        fit_scale = _extend_geometry(original, background)
        if fit_scale is not None and cover_scale > fit_scale:
            extended = _extend_backdrop_to_canvas(original, background, fit_scale)
            if extended is not None:
                return apply_circle_crop(extended), "circle_extend"
        # Historical cover crop -- unreachable geometry, or `_extend_geometry`
        # found no plausible mark (touches the frame, or the flood never left
        # the border), or extending would need a clean edge line that doesn't
        # exist (a still-transparent ring after `_opaque_bounds`). Every one
        # of those keeps the tile exactly as it always rendered.
        scale = cover_scale
        resized = original.resize((max(FINAL_SIZE, round(original.width * scale)),
                                   max(FINAL_SIZE, round(original.height * scale))),
                                  Image.Resampling.LANCZOS)
        left = (resized.width - FINAL_SIZE) // 2
        top = (resized.height - FINAL_SIZE) // 2
        canvas = resized.crop((left, top, left + FINAL_SIZE, top + FINAL_SIZE))
        return apply_circle_crop(canvas), "circle_cover"

    separated = tokenise_transparent_neutral_mark(remove_edge_background(original), theme)
    return contain_node_artwork(separated, "safe_contain")


def alpha_max_radius(im: Image.Image) -> float:
    alpha = np.asarray(im.getchannel("A"))
    ys, xs = np.nonzero(alpha > 8)
    if xs.size == 0:
        return 0.0
    cx = (im.width - 1) / 2
    cy = (im.height - 1) / 2
    max_r2 = np.max((xs - cx) ** 2 + (ys - cy) ** 2)
    return math.sqrt(float(max_r2))


def inner_disc_min_alpha(im: Image.Image, radius: float = 110.0) -> int:
    """Lowest alpha value found within `radius` of a 256x256 canvas's centre.

    The permanent guard for the exact defect the first version of
    `_extend_backdrop_to_canvas` produced: `np.pad(mode="edge")` on a still-
    partly-transparent border replicated a wedge of alpha 11 into one asset
    and a translucent alpha 179-217 ring into another -- the node's own fill
    colour showing through what must be a solid disc. A well-formed
    `circle_cover`/`circle_extend`/`light_backdrop` asset is fully opaque
    everywhere well inside the outer contour; 110 leaves clearance before the
    antialiased circle edge itself starts falling off.
    """
    alpha = np.asarray(im.convert("RGBA"))[:, :, 3]
    yy, xx = np.mgrid[0:im.height, 0:im.width]
    cx, cy = (im.width - 1) / 2.0, (im.height - 1) / 2.0
    inside = ((xx - cx) ** 2 + (yy - cy) ** 2) <= radius ** 2
    if not inside.any():
        return 255
    return int(alpha[inside].min())


def prepare_final(source: Path, dest: Path):
    canvas, _crop_mode = prepare_node_canvas(source)
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "PNG", optimize=True)


def command_finalize(_args):
    selection = {r["key"]: r for r in load_json(SELECTION)["nodes"]}
    domains = {r["key"]: r for r in load_json(DOMAINS)["nodes"]}
    decisions = {r["key"]: r for r in load_json(REVIEW)["nodes"]}
    if ASSET_DECISIONS.exists():
        for key, decision in load_json(ASSET_DECISIONS).items():
            decisions[key].update(decision)
    rows = []
    for key in sorted(selection):
        node = selection[key]
        decision = decisions[key]
        if decision.get("result") not in {"logo", "none"}:
            raise ValueError(f"{key}: unresolved review result {decision.get('result')!r}")
        row = {
            "key": key, "cc": node["cc"], "tid": node["tid"], "eid": node["eid"],
            "graph_id": node.get("graph_id"), "name": node["name"],
            "result": decision["result"], "review_status": "accepted",
            "asset_path": None, "source_url": None, "source_kind": None,
            "retrieved_at": today(), "license_note": decision.get("license_note", ""),
            "sha256": None, "review_notes": decision.get("notes", ""),
        }
        if decision["result"] == "logo":
            candidate_id = decision.get("candidate_id")
            meta = load_json(RAW / node["cc"] / node["tid"] / "candidates.json")
            matches = [c for c in meta["candidates"] if c["id"] == candidate_id and c.get("status") == "candidate"]
            if len(matches) != 1:
                raise ValueError(f"{key}: accepted candidate {candidate_id!r} not found")
            candidate = matches[0]
            source = PILOT / candidate["preview_path"]
            dest = FINAL / node["cc"] / f"{node['tid']}.png"
            prepare_final(source, dest)
            row.update({
                "asset_path": str(dest.relative_to(PILOT)).replace("\\", "/"),
                "source_url": candidate.get("final_url") or candidate["url"],
                "source_kind": candidate["kind"],
                "sha256": sha256_file(dest),
                "license_note": decision.get("license_note") or "official-site mark; identification in research figure; no affiliation implied",
            })
        rows.append(row)
    manifest = {
        "schema_version": 1,
        "transport_only": True,
        "canonical_target": "Neo4j node properties after separate approval",
        "database": "mit-bestand",
        "created_at": today(),
        "graph_export_sha256": load_json(SELECTION)["graph_export_sha256"],
        "nodes": rows,
    }
    write_json(MANIFEST, manifest)
    print(f"wrote {MANIFEST}: {len(rows)} reviewed nodes")


def validate_manifest(manifest):
    errors = []
    rows = manifest.get("nodes", [])
    if len(rows) != 48:
        errors.append(f"expected 48 rows, got {len(rows)}")
    counts = collections.Counter(r.get("cc") for r in rows)
    if counts != collections.Counter({"GB": 16, "NL": 16, "AT": 16}):
        errors.append(f"country counts wrong: {dict(counts)}")
    for row in rows:
        key = row.get("key", "?")
        if row.get("review_status") != "accepted" or row.get("result") not in {"logo", "none"}:
            errors.append(f"{key}: unresolved outcome")
            continue
        if row["result"] == "none":
            if row.get("asset_path"):
                errors.append(f"{key}: none row has asset")
            continue
        path = PILOT / row["asset_path"]
        if not path.is_file():
            errors.append(f"{key}: missing {path}")
            continue
        im = Image.open(path)
        if im.size != (FINAL_SIZE, FINAL_SIZE) or im.mode != "RGBA":
            errors.append(f"{key}: expected 256x256 RGBA, got {im.size} {im.mode}")
        if alpha_max_radius(im) > SAFE_RADIUS + 0.75:
            errors.append(f"{key}: visible pixels exceed radial safe zone")
        if sha256_file(path) != row.get("sha256"):
            errors.append(f"{key}: checksum mismatch")
        if not row.get("source_url") or not row.get("source_kind"):
            errors.append(f"{key}: missing source provenance")
    return errors


def command_validate(_args):
    manifest = load_json(MANIFEST)
    errors = validate_manifest(manifest)
    if errors:
        print("FAIL")
        for error in errors:
            print(" - " + error)
        raise SystemExit(1)
    logos = sum(r["result"] == "logo" for r in manifest["nodes"])
    print(f"PASS: 48 reviewed nodes; {logos} logos; {48 - logos} unchanged ID-only nodes")


def validate_rendered_pdfs(manifest):
    """Measure embedded PDF image squares and visible alpha against the node."""
    import fitz

    logos = [r for r in manifest["nodes"] if r["result"] == "logo"]
    alpha_r = max(
        alpha_max_radius(Image.open(PILOT / r["asset_path"]).convert("RGBA"))
        for r in logos
    )
    node_r = NODE_RADIUS_MM * 72.0 / 25.4
    expected_side = 2.0 * node_r * IMAGE_DIAMETER_FRACTION
    errors, themes = [], {}
    for theme, path in PILOT_PDFS.items():
        if not path.is_file():
            errors.append(f"{theme}: missing PDF")
            continue
        doc = fitz.open(path)
        infos = [i for i in doc[1].get_image_info(xrefs=True) if i.get("has-mask")]
        if len(infos) != len(logos):
            errors.append(f"{theme}: expected {len(logos)} images, got {len(infos)}")
        measured = []
        for n, info in enumerate(infos):
            x0, y0, x1, y1 = info["bbox"]
            w, h = x1 - x0, y1 - y0
            corner_r = math.hypot(w, h) / 2.0
            visible_r = alpha_r * max(w, h) / FINAL_SIZE
            measured.append({"index": n, "width_pt": round(w, 5),
                             "height_pt": round(h, 5),
                             "square_corner_radius_pt": round(corner_r, 5),
                             "visible_radius_pt": round(visible_r, 5)})
            if abs(w - h) > 0.02 or abs(w - expected_side) > 0.08:
                errors.append(f"{theme} image {n}: wrong PDF dimensions {w:.3f}x{h:.3f}pt")
            if visible_r > node_r * 0.94:
                errors.append(f"{theme} image {n}: visible logo reaches circle clip")
        themes[theme] = measured
        doc.close()
    return {"schema_version": 1, "node_radius_mm": NODE_RADIUS_MM,
            "image_diameter_fraction": IMAGE_DIAMETER_FRACTION,
            "logo_count": len(logos), "circle_radius_pt": round(node_r, 5),
            "inscribed_square_side_pt": round(node_r * math.sqrt(2), 5),
            "expected_image_side_pt": round(expected_side, 5),
            "max_source_alpha_radius_px": round(alpha_r, 5),
            "themes": themes, "errors": errors,
            "result": "PASS" if not errors else "FAIL"}


def command_validate_render(_args):
    report = validate_rendered_pdfs(load_json(MANIFEST))
    write_json(RENDER_CONTAINMENT_REPORT, report)
    print(f"{report['result']}: {report['logo_count']} logos, light + dark")
    if report["errors"]:
        print("\n".join(" - " + e for e in report["errors"]))
        raise SystemExit(1)


def live_counts(graph_ids: list[str]):
    scripts = REPO / "_scripts"
    sys.path.insert(0, str(scripts))
    from neo4j_env import resolve_connection
    from neo4j import GraphDatabase, READ_ACCESS
    uri, user, password, _database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database="mit-bestand", default_access_mode=READ_ACCESS) as session:
            rows = session.run(
                "UNWIND $ids AS id OPTIONAL MATCH (n {id:id}) RETURN id, count(n) AS matches",
                ids=graph_ids,
            )
            return {r["id"]: r["matches"] for r in rows}
    finally:
        driver.close()


def command_patch(args):
    manifest = load_json(MANIFEST)
    errors = validate_manifest(manifest)
    if errors:
        raise ValueError("manifest invalid; run validate first")
    export = load_json(EXPORT)
    by_id = collections.Counter(
        n.get("properties", {}).get("id") for n in export["nodes"] if n.get("properties", {}).get("id")
    )
    patch_rows, blocked, match_errors = [], [], []
    for row in manifest["nodes"]:
        if not row.get("graph_id"):
            blocked.append({"key": row["key"], "eid": row["eid"], "reason": "overlay node has no canonical graph id"})
            continue
        if by_id[row["graph_id"]] != 1:
            match_errors.append(f"{row['key']}: graph id {row['graph_id']!r} matches {by_id[row['graph_id']]} export nodes")
            continue
        props = {
            "image_result": row["result"],
            "image_review_status": "pilot_accepted",
            "image_retrieved_at": row["retrieved_at"],
        }
        if row["result"] == "logo":
            props.update({
                "image_asset_path": str((PILOT / row["asset_path"]).relative_to(REPO)).replace("\\", "/"),
                "image_source_url": row["source_url"],
                "image_source_kind": row["source_kind"],
                "image_license_note": row["license_note"],
                "image_sha256": row["sha256"],
            })
        patch_rows.append({"match": {"id": row["graph_id"]}, "set": props, "audit": {"key": row["key"], "eid": row["eid"]}})
    live = None
    if args.live:
        counts = live_counts([r["match"]["id"] for r in patch_rows])
        live = {"database": "mit-bestand", "read_only": True, "counts": counts}
        match_errors.extend(f"live {gid!r}: {count} matches" for gid, count in counts.items() if count != 1)
    patch = {
        "schema_version": 1,
        "database": "mit-bestand",
        "dry_run_only": True,
        "match_property": "id",
        "forbidden_side_effects": ["create :Quelle nodes", "create BELEGT_IN relationships", "write metadata_sidecar_key"],
        "rows": patch_rows,
        "blocked_overlay_nodes": blocked,
        "validation": {"export": str(EXPORT), "live": live, "errors": match_errors},
    }
    write_json(PATCH, patch)
    report = [
        "# Pilot image property patch report", "",
        f"- Patch rows: **{len(patch_rows)}**", f"- Overlay-only, not importable: **{len(blocked)}**",
        f"- Export match errors: **{len(match_errors)}**", f"- Live validation: **{'run' if args.live else 'not run'}**", "",
        "No write was performed against Neo4j.", "",
    ]
    if blocked:
        report += ["## Overlay-only nodes", ""] + [f"- `{r['key']}` — {r['reason']}" for r in blocked] + [""]
    if match_errors:
        report += ["## Match errors", ""] + [f"- {e}" for e in match_errors] + [""]
    PATCH_REPORT.write_text("\n".join(report), encoding="utf-8")
    print(f"wrote {PATCH} and {PATCH_REPORT}")
    if match_errors:
        raise SystemExit(1)


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest="command", required=True)
    sub.add_parser("select").set_defaults(func=command_select)
    sub.add_parser("domains").set_defaults(func=command_domains)
    harvest = sub.add_parser("harvest")
    harvest.add_argument("--key", help="harvest one LAND:tid row")
    harvest.set_defaults(func=command_harvest)
    sub.add_parser("contact").set_defaults(func=command_contact)
    sub.add_parser("finalize").set_defaults(func=command_finalize)
    sub.add_parser("validate").set_defaults(func=command_validate)
    sub.add_parser("validate-render").set_defaults(func=command_validate_render)
    patch = sub.add_parser("patch")
    patch.add_argument("--live", action="store_true", help="read-only match validation against mit-bestand")
    patch.set_defaults(func=command_patch)
    args = ap.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
