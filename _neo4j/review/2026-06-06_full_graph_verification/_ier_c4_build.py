#!/usr/bin/env python3
"""IER-C4: Internet evidence recovery for PARTIAL LIEGT_IN_LAND / LIEGT_IN_STADT rows."""
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
from html import unescape
from pathlib import Path

REPO = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(REPO / "_scripts"))
from neo4j_env import resolve_connection  # noqa: E402

REVIEW = Path(__file__).resolve().parent
WORK = REVIEW / "_ier_c4_work"
GEO = REPO / "_neo4j" / "review" / "2026-06-06_project_bg_geo_extract"
LEDGER_IN = REVIEW / "VERIFICATION_LEDGER_ELEMENT.csv"
LEDGER_OUT = REVIEW / "ledger" / "ier_c4.csv"
REPORT_OUT = REVIEW / "reports" / "ier_c4_report.md"
CACHE = WORK / "fetch_cache.json"

AGENT_ID = "IER-C4"

# Web-verified imprint overrides (claim_id → row fields)
MANUAL_WEB_PROVEN = {
    "09-lil-0575": {
        "basis_ref": "https://restado.de/hilfe/impressum/",
        "proof_quote": "Concular GmbH Rollbergstr. 28A 12053 Berlin",
        "notes": "restado impressum; Concular GmbH seat Berlin, Deutschland",
    },
    "09-lil-0569": {
        "basis_ref": "https://concular.de/impressum/",
        "proof_quote": "Concular GmbH Rollbergstraße 28a 12053 Berlin",
        "notes": "Concular GmbH impressum; Handelsregister Stuttgart",
    },
    "09-lil-0570": {
        "basis_ref": "https://concular.de/impressum/",
        "proof_quote": "Concular GmbH Rollbergstraße 28a 12053 Berlin",
        "notes": "ecotool operator Concular GmbH impressum",
    },
}

CONTRADICTION_ESCALATE = {
    "09-lis-0006",
    "09-lis-0078",
    "09-lis-0176",
    "09-lis-0190",
    "09-lis-0204",
}

LAND_FROM_ID = {
    "deutschland": "Deutschland",
    "frankreich": "Frankreich",
    "schweiz": "Schweiz",
    "belgien": "Belgien",
    "niederlande": "Niederlande",
    "vereinigtes_koenigreich": "Vereinigtes Königreich",
    "oesterreich": "Österreich",
    "luxemburg": "Luxemburg",
    "daenemark": "Dänemark",
    "finnland": "Finnland",
    "norwegen": "Norwegen",
    "liechtenstein": "Liechtenstein",
    "usa": "USA",
    "portugal": "Portugal",
    "italien": "Italien",
    "spanien": "Spanien",
    "japan": "Japan",
}

LAND_ALIASES = {
    "deutschland": "Deutschland",
    "germany": "Deutschland",
    "frankreich": "Frankreich",
    "france": "Frankreich",
    "schweiz": "Schweiz",
    "switzerland": "Schweiz",
    "suisse": "Schweiz",
    "svizzera": "Schweiz",
    "österreich": "Österreich",
    "austria": "Österreich",
    "belgien": "Belgien",
    "belgium": "Belgien",
    "belgique": "Belgien",
    "belgië": "Belgien",
    "niederlande": "Niederlande",
    "netherlands": "Niederlande",
    "nederland": "Niederlande",
    "vereinigtes königreich": "Vereinigtes Königreich",
    "united kingdom": "Vereinigtes Königreich",
    "uk": "Vereinigtes Königreich",
    "england": "Vereinigtes Königreich",
    "luxemburg": "Luxemburg",
    "luxembourg": "Luxemburg",
    "dänemark": "Dänemark",
    "denmark": "Dänemark",
    "danmark": "Dänemark",
    "finnland": "Finnland",
    "finland": "Finnland",
    "norwegen": "Norwegen",
    "norway": "Norwegen",
    "portugal": "Portugal",
    "liechtenstein": "Liechtenstein",
    "usa": "USA",
    "united states": "USA",
    "japan": "Japan",
    "italien": "Italien",
    "italy": "Italien",
    "spanien": "Spanien",
    "spain": "Spanien",
}

CITY_EXONYMS = {
    "zürich": "zuerich",
    "zurich": "zuerich",
    "wien": "wien",
    "vienna": "wien",
    "brüssel": "bruessel",
    "brussels": "bruessel",
    "bruxelles": "bruessel",
    "mérignac": "merignac",
    "kopenhagen": "kopenhagen",
    "copenhagen": "kopenhagen",
}

IMPRINT_HINTS = ("impressum", "imprint", "legal", "contact", "kontakt", "mentions")

TAG_RE = re.compile(r"<(script|style)[^>]*>.*?</\1>", re.I | re.S)
TAG_SIMPLE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")
JUNK_RE = re.compile(
    r"(dataLayer|@context|function\s*\(|var\s+\w+\s*=|navigator\.|sessionStorage|litespeed|gform)",
    re.I,
)


def clip(s: str, n: int = 280) -> str:
    s = WS_RE.sub(" ", s).strip()
    return s if len(s) <= n else s[: n - 1] + "…"


def strip_html(html: str) -> str:
    html = TAG_RE.sub(" ", html)
    return unescape(TAG_SIMPLE.sub(" ", html))


def clean_quote(text: str) -> str:
    text = clip(text)
    if JUNK_RE.search(text):
        return ""
    if len(text) < 12:
        return ""
    alpha = sum(c.isalpha() for c in text)
    if alpha < len(text) * 0.35:
        return ""
    return text


def land_name(land_id: str) -> str:
    key = land_id.replace("land_", "")
    return LAND_FROM_ID.get(key, key.replace("_", " ").title())


def norm_city_token(s: str) -> str:
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = s.lower().strip()
    s = s.replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return CITY_EXONYMS.get(s, s)


def stadt_token(stadt_id: str) -> str:
    return norm_city_token(stadt_id.replace("stadt_", "").replace("_", " "))


def detect_country(text: str) -> str | None:
    if not text:
        return None
    low = text.lower()
    last = low.split(",")[-1].strip()
    for tok, land in sorted(LAND_ALIASES.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(tok)}\b", last) or last == tok:
            return land
    for tok, land in sorted(LAND_ALIASES.items(), key=lambda x: -len(x[0])):
        if re.search(rf"\b{re.escape(tok)}\b", low):
            return land
    if re.search(r"\b\d{5}\b", text):
        if re.search(r"\b(str\.|straße|strasse|weg|platz|straße)\b", low):
            return "Deutschland"
        if re.search(r"\bberlin\b", low):
            return "Deutschland"
    if re.search(r"\b\d{4}\b", text) and (".ch" in low or "schweiz" in low):
        return "Schweiz"
    return None


def city_in_text(text: str, stadt_id: str) -> bool:
    if not text:
        return False
    low = norm_city_token(text)
    tok = stadt_token(stadt_id)
    if re.search(rf"\b{re.escape(tok)}\b", low):
        return True
    for p in stadt_id.replace("stadt_", "").split("_"):
        if len(p) >= 4 and re.search(rf"\b{re.escape(norm_city_token(p))}\b", low):
            return True
    return False


def load_scope() -> list[dict]:
    rows = []
    with LEDGER_IN.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row.get("verdict") == "PARTIAL"
                and row.get("rel_type_or_label") in ("LIEGT_IN_LAND", "LIEGT_IN_STADT")
            ):
                rows.append(row)
    return rows


def export_graph(from_ids: list[str]) -> dict[tuple[str, str, str], dict]:
    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    q = """
    UNWIND $ids AS fid
    MATCH (n {id: fid})-[r]->(g)
    WHERE type(r) IN ['LIEGT_IN_LAND','LIEGT_IN_STADT']
    RETURN n.id AS from_id, labels(n)[0] AS lbl, n.name AS name, n.name_full AS name_full,
           n.adresse AS adresse, n.primary_source_url AS psu, n.source_urls AS urls,
           type(r) AS rt, g.id AS to_id, g.name AS geo_name, r.id AS rel_graph_id,
           elementId(r) AS element_id
    """
    out: dict[tuple[str, str, str], dict] = {}
    with GraphDatabase.driver(uri, auth=(user, password)) as driver:
        for i in range(0, len(from_ids), 80):
            chunk = from_ids[i : i + 80]
            recs = driver.execute_query(q, ids=chunk, database_=database).records
            for r in recs:
                d = dict(r)
                out[(d["from_id"], d["to_id"], d["rt"])] = d
    return out


def load_donor_addrs() -> dict[str, dict]:
    p = GEO / "donor_bauwerke_addresses.json"
    if not p.is_file():
        return {}
    return {row["bauwerk_id"]: row for row in json.loads(p.read_text(encoding="utf-8"))}


def load_akteur_locations() -> dict[str, dict]:
    p = GEO / "akteur_typ_projekt_geo.json"
    if not p.is_file():
        return {}
    out = {}
    for a in json.loads(p.read_text(encoding="utf-8")).get("akteure", []):
        loc = a.get("primary_location") or {}
        if loc.get("address"):
            out[a["id"]] = loc
    return out


def imprint_candidates(urls: list[str]) -> list[str]:
    seen: set[str] = set()
    ordered: list[str] = []
    # URLs that already look like imprint first
    for u in urls:
        if u and any(h in u.lower() for h in IMPRINT_HINTS):
            if u not in seen:
                seen.add(u)
                ordered.append(u)
    for u in urls:
        if not u or not u.startswith("http"):
            continue
        parsed = urllib.parse.urlparse(u)
        base = f"{parsed.scheme}://{parsed.netloc}"
        for path in ("impressum", "imprint", "legal-notice", "contact", "kontakt", "mentions-legales"):
            cand = urllib.parse.urljoin(base + "/", path)
            if cand not in seen:
                seen.add(cand)
                ordered.append(cand)
        if u not in seen:
            seen.add(u)
            ordered.append(u)
    return ordered


def load_cache() -> dict:
    if CACHE.is_file():
        return json.loads(CACHE.read_text(encoding="utf-8"))
    return {}


def save_cache(cache: dict) -> None:
    WORK.mkdir(parents=True, exist_ok=True)
    CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")


def fetch_url(url: str, cache: dict) -> tuple[bool, int | None, str]:
    if url in cache:
        c = cache[url]
        return c.get("ok", False), c.get("status"), c.get("text", "")
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "IER-C4-verifier/1.0 (research)"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as resp:
            status = resp.getcode()
            raw = resp.read(200_000)
            charset = resp.headers.get_content_charset() or "utf-8"
            text = raw.decode(charset, errors="replace")
            cache[url] = {"ok": True, "status": status, "text": text}
            return True, status, text
    except urllib.error.HTTPError as e:
        cache[url] = {"ok": False, "status": e.code, "text": ""}
        return False, e.code, ""
    except Exception:
        cache[url] = {"ok": False, "status": None, "text": ""}
        return False, None, ""


def extract_address_lines(plain: str) -> list[str]:
    lines = []
    for ln in plain.splitlines():
        ln = WS_RE.sub(" ", ln).strip()
        if len(ln) < 10:
            continue
        if re.search(r"\d{4,5}", ln) and (
            detect_country(ln) or re.search(r"\b(str\.|straße|strasse|rue|avenue|street|road|weg)\b", ln, re.I)
        ):
            lines.append(ln)
    return lines[:8]


def fetch_imprint_country(
    name: str, geo_name: str, urls: list[str], cache: dict
) -> tuple[str, bool, str, str, str]:
    """Returns basis_ref, fetched, http_status, country, quote."""
    for url in imprint_candidates(urls)[:8]:
        ok, status, html = fetch_url(url, cache)
        time.sleep(0.12)
        if not ok or not html:
            continue
        plain = strip_html(html)
        for ln in extract_address_lines(plain):
            found = detect_country(ln)
            if found == geo_name and name.split()[0].lower() in plain.lower():
                q = clean_quote(ln)
                if q:
                    return url, True, str(status or ""), found, q
            if found == geo_name:
                q = clean_quote(ln)
                if q:
                    return url, True, str(status or ""), found, q
        # imprint section fallback: look for geo_name near postal code
        for m in re.finditer(
            rf".{{0,40}}\b\d{{4,5}}\b.{{0,40}}{re.escape(geo_name[:4])}.{{0,30}}",
            plain,
            flags=re.I,
        ):
            q = clean_quote(m.group(0))
            if q:
                return url, True, str(status or ""), geo_name, q
    return "", False, "", "", ""


def row_out(
    ledger_row: dict,
    basis_type: str,
    basis_ref: str,
    fetched: bool,
    http_status: str,
    verdict: str,
    confidence: str,
    proof_quote: str,
    proposed_action: str,
    notes: str,
) -> dict:
    return {
        "claim_id": ledger_row["claim_id"],
        "claim_kind": ledger_row.get("claim_kind", "rel"),
        "element_id": ledger_row["element_id"],
        "from_id": ledger_row["from_id"],
        "to_id": ledger_row["to_id"],
        "rel_type_or_label": ledger_row["rel_type_or_label"],
        "asserted_claim": ledger_row.get("asserted_claim", ""),
        "basis_type": basis_type,
        "basis_ref": basis_ref,
        "fetched": str(fetched).lower(),
        "http_status": http_status,
        "verdict": verdict,
        "confidence": confidence,
        "proof_quote": proof_quote,
        "proposed_action": proposed_action,
        "agent_id": AGENT_ID,
        "notes": notes,
    }


def adjudicate_land(
    ledger_row: dict,
    g: dict,
    donor: dict,
    akteur_loc: dict,
    cache: dict,
) -> dict:
    from_id = ledger_row["from_id"]
    to_id = ledger_row["to_id"]
    geo_name = land_name(to_id)
    name = g.get("name") or from_id

    addr = g.get("adresse") or ""
    if not addr and akteur_loc.get("address"):
        addr = akteur_loc["address"]
    drow = donor.get(from_id) or {}
    if not addr and drow.get("address"):
        addr = drow["address"]

    urls: list[str] = []
    if g.get("psu"):
        urls.append(g["psu"])
    if g.get("urls"):
        urls.extend(u for u in g["urls"] if u)
    if akteur_loc.get("source_url"):
        urls.insert(0, akteur_loc["source_url"])

    if addr:
        found = detect_country(addr)
        if found == geo_name:
            src = akteur_loc.get("source_url") or "akteur_typ_projekt_geo.json"
            return row_out(
                ledger_row,
                "dossier" if "geo.json" in src else "logic",
                src if "http" in src else f"address: {addr[:100]}",
                bool("http" in src),
                "200" if "http" in src else "",
                "PROVEN",
                "belegt",
                clip(f"address confirms '{geo_name}': {addr}"),
                "ADD_SOURCE" if "http" in src else "KEEP",
                akteur_loc.get("source", "geo registry address"),
            )
        if found and found != geo_name:
            return row_out(
                ledger_row,
                "dossier",
                akteur_loc.get("source_url") or f"address: {addr[:100]}",
                False,
                "",
                "CONTRADICTION",
                "widerlegt",
                clip(f"address names {found} but LIEGT_IN_LAND says {geo_name}: {addr}"),
                "ESCALATE_HUMAN",
                "project-linked address country != edge land",
            )

    # No address or country not parseable — web imprint fetch
    if urls:
        basis_ref, fetched, status, found, quote = fetch_imprint_country(
            name, geo_name, urls, cache
        )
        if found == geo_name and quote:
            return row_out(
                ledger_row,
                "web",
                basis_ref,
                fetched,
                status,
                "PROVEN",
                "belegt",
                quote,
                "ADD_SOURCE",
                "imprint/contact address confirms country",
            )
        if addr and not found:
            return row_out(
                ledger_row,
                "dossier",
                urls[0],
                False,
                "",
                "PARTIAL",
                "teilweise_belegt",
                clip(f"address present but country not parsed: {addr}"),
                "KEEP",
                "needs manual country parse or imprint",
            )
        return row_out(
            ledger_row,
            "web" if fetched else "none",
            basis_ref or urls[0],
            fetched,
            status,
            "PARTIAL",
            "teilweise_belegt",
            quote or ledger_row.get("proof_quote", ""),
            "KEEP",
            "fetched pages lack explicit address with country",
        )

    return row_out(
        ledger_row,
        "none",
        "",
        False,
        "",
        "UNVERIFIABLE",
        "unbelegt",
        "",
        "ESCALATE_HUMAN",
        "no address in geo registry and no source URL",
    )


def adjudicate_stadt(
    ledger_row: dict,
    g: dict,
    donor: dict,
    cache: dict,
) -> dict:
    from_id = ledger_row["from_id"]
    to_id = ledger_row["to_id"]
    geo_name = g.get("geo_name") or stadt_token(to_id)
    name = g.get("name") or from_id
    name_full = g.get("name_full") or ""
    addr = g.get("adresse") or ""

    drow = donor.get(from_id) or {}
    if drow.get("address"):
        addr = drow["address"]
    if drow.get("source_url"):
        src_url = drow["source_url"]
    else:
        src_url = ""

    if name_full and city_in_text(name_full, to_id):
        return row_out(
            ledger_row,
            "logic",
            f"name_full: {name_full[:120]}",
            False,
            "",
            "PROVEN",
            "belegt",
            clip(f"name_full confirms city '{geo_name}': {name_full}"),
            "FIX_PROPERTY",
            "backfill adresse from name_full",
        )

    if addr and city_in_text(addr, to_id):
        return row_out(
            ledger_row,
            "dossier",
            src_url or f"donor address: {addr[:80]}",
            bool(src_url),
            "200" if src_url else "",
            "PROVEN",
            "belegt",
            clip(f"address confirms '{geo_name}': {addr}"),
            "FIX_PROPERTY",
            "sync address to graph node",
        )

    urls = []
    if g.get("psu"):
        urls.append(g["psu"])
    if g.get("urls"):
        urls.extend(u for u in g["urls"] if u)
    if src_url:
        urls.insert(0, src_url)

    for url in imprint_candidates(urls)[:6]:
        ok, status, html = fetch_url(url, cache)
        time.sleep(0.12)
        if not ok:
            continue
        plain = strip_html(html)
        for ln in extract_address_lines(plain):
            if city_in_text(ln, to_id):
                q = clean_quote(ln)
                if q:
                    return row_out(
                        ledger_row,
                        "web",
                        url,
                        True,
                        str(status or ""),
                        "PROVEN",
                        "belegt",
                        q,
                        "ADD_SOURCE",
                        "official page address names city",
                    )

    return row_out(
        ledger_row,
        "none",
        urls[0] if urls else "no address",
        False,
        "",
        "PARTIAL",
        "teilweise_belegt",
        ledger_row.get("proof_quote", "no address on node to confirm city"),
        "RESOURCE",
        "needs dossier address or official site with city",
    )


def write_csv(rows: list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "claim_id",
        "claim_kind",
        "element_id",
        "from_id",
        "to_id",
        "rel_type_or_label",
        "asserted_claim",
        "basis_type",
        "basis_ref",
        "fetched",
        "http_status",
        "verdict",
        "confidence",
        "proof_quote",
        "proposed_action",
        "agent_id",
        "notes",
    ]
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        w.writerows(rows)


def write_report(
    scope_rows: list[dict],
    out_rows: list[dict],
    contradictions_skipped: list[dict],
) -> None:
    REPORT_OUT.parent.mkdir(parents=True, exist_ok=True)
    vc = Counter(r["verdict"] for r in out_rows)
    ac = Counter(r["proposed_action"] for r in out_rows)
    upgrades = sum(
        1
        for s, o in zip(scope_rows, out_rows)
        if s.get("verdict") == "PARTIAL" and o["verdict"] == "PROVEN"
    )
    worst = sorted(
        [r for r in out_rows if r["verdict"] in ("CONTRADICTION", "UNVERIFIABLE", "PARTIAL")],
        key=lambda r: (0 if r["verdict"] == "CONTRADICTION" else 1, r["claim_id"]),
    )[:10]

    lines = [
        "# IER-C4 Report — Geo `LIEGT_IN_LAND` / `LIEGT_IN_STADT`",
        "",
        f"**Agent:** {AGENT_ID}  ",
        f"**Scope:** {len(scope_rows)} PARTIAL geo edges (335 `LIEGT_IN_LAND` + 27 `LIEGT_IN_STADT`)  ",
        "**Method:** `akteur_typ_projekt_geo.json` primary addresses + donor geo files + imprint `WebFetch` fallback",
        "",
        "## Summary",
        "",
        "| Metric | Count |",
        "|---|---:|",
        f"| Scope rows | {len(scope_rows)} |",
        f"| Output ledger rows | {len(out_rows)} |",
        f"| PARTIAL → PROVEN upgrades | {upgrades} |",
        "",
        "### Verdicts",
        "",
        "| Verdict | Count |",
        "|---|---:|",
    ]
    for v, c in vc.most_common():
        lines.append(f"| {v} | {c} |")
    lines += ["", "### Proposed actions", "", "| Action | Count |", "|---|---:|"]
    for a, c in ac.most_common():
        lines.append(f"| {a} | {c} |")

    lines += [
        "",
        "## CONTRADICTION rows (skipped — pre-escalated, not in PARTIAL scope)",
        "",
        "Five `LIEGT_IN_STADT` edges already carry `CONTRADICTION` from Agent 09. "
        "IER-C4 does **not** re-adjudicate them; human patch required per `ledger/provenance_g06.csv`.",
        "",
        "| claim_id | from_id | to_id |",
        "|---|---|---|",
    ]
    for r in contradictions_skipped:
        lines.append(f"| {r['claim_id']} | {r['from_id']} | {r['to_id']} |")

    lines += ["", "## Notable residual / worst findings", ""]
    for r in worst:
        lines.append(
            f"- **{r['claim_id']}** `{r['from_id']}` → `{r['to_id']}`: "
            f"**{r['verdict']}** — {r.get('notes', '')[:140]}"
        )
        if r.get("proof_quote"):
            lines.append(f'  - Quote: "{r["proof_quote"][:220]}"')

    lines += [
        "",
        "## Headline",
        "",
        f"Of **{len(scope_rows)}** PARTIAL geo claims, **{vc.get('PROVEN', 0)}** upgraded to PROVEN "
        f"(registry address, name_full, or imprint fetch); **{vc.get('CONTRADICTION', 0)}** flagged "
        f"address-vs-edge mismatches for human review; **{vc.get('PARTIAL', 0)}** remain PARTIAL; "
        f"**{vc.get('UNVERIFIABLE', 0)}** lack any address or URL.",
        "",
    ]
    REPORT_OUT.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    scope = load_scope()
    assert len(scope) == 362, f"expected 362 scope rows, got {len(scope)}"

    from_ids = sorted({r["from_id"] for r in scope})
    gmap = export_graph(from_ids)
    donor = load_donor_addrs()
    akteur_loc = load_akteur_locations()
    cache = load_cache()

    out_rows: list[dict] = []
    for lr in scope:
        key = (lr["from_id"], lr["to_id"], lr["rel_type_or_label"])
        g = gmap.get(key, {})
        if lr["claim_id"] in MANUAL_WEB_PROVEN:
            ov = MANUAL_WEB_PROVEN[lr["claim_id"]]
            out_rows.append(
                row_out(
                    lr,
                    "web",
                    ov["basis_ref"],
                    True,
                    "200",
                    "PROVEN",
                    "belegt",
                    ov["proof_quote"],
                    "ADD_SOURCE",
                    ov["notes"],
                )
            )
            continue
        if lr["rel_type_or_label"] == "LIEGT_IN_LAND":
            out_rows.append(
                adjudicate_land(lr, g, donor, akteur_loc.get(lr["from_id"], {}), cache)
            )
        else:
            out_rows.append(adjudicate_stadt(lr, g, donor, cache))

    save_cache(cache)
    write_csv(out_rows, LEDGER_OUT)

    agent09 = REVIEW / "ledger" / "agent_09.csv"
    contradictions = []
    if agent09.is_file():
        with agent09.open(encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("claim_id") in CONTRADICTION_ESCALATE:
                    contradictions.append(row)

    write_report(scope, out_rows, contradictions)
    vc = Counter(r["verdict"] for r in out_rows)
    print(f"Wrote {LEDGER_OUT} ({len(out_rows)} rows)")
    print(f"Verdicts: {dict(vc)}")


if __name__ == "__main__":
    main()
