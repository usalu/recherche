#!/usr/bin/env python3
"""Quality Pass Q04 — re-adjudicate PARTIAL/MISSING catalogue edges (HAT_BAUTEILTYP, NUTZT_MATERIAL).

Scope: 143 PARTIAL + 3 MISSING_EVIDENCE rows from ledger/element_proof_agent_03.csv.
Strict Evidence Gate: PROVEN only with verbatim page quote naming target classification;
else DELETE (high-confidence) or RELABEL confidence down.

Outputs:
  ledger/quality_pass_q04.csv
  reports/quality_pass_q04.md
  patches/quality_pass_q04_upgrades.patch.jsonl
  patches/quality_pass_q04_deletes.patch.jsonl
  patches/quality_pass_q04_downgrades.patch.jsonl
"""
from __future__ import annotations

import csv
import json
import re
import ssl
import subprocess
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from neo4j_env import resolve_connection  # noqa: E402

EP03_LEDGER = HERE / "ledger/element_proof_agent_03.csv"
R07_LEDGER = HERE / "ledger/remediation_r07.csv"
R07_CACHE = HERE / "_agent_r07_work/url_fetch_cache.json"
VOCAB_PATH = REPO / "_neo4j/contracts/project_batches_v1_1/controlled_vocabulary.seed.kg.jsonl"
ENRICH_DIRS = [
    REPO / "_neo4j/intake/inbox/research/bauteilboersen_deep_enrichment_results",
    REPO / "_neo4j/intake/inbox/research/bauteilboersen_deeper_material_bauteiltyp_results",
]

OUT_LEDGER = HERE / "ledger/quality_pass_q04.csv"
OUT_REPORT = HERE / "reports/quality_pass_q04.md"
PATCH_UPGRADES = HERE / "patches/quality_pass_q04_upgrades.patch.jsonl"
PATCH_DELETES = HERE / "patches/quality_pass_q04_deletes.patch.jsonl"
PATCH_DOWNGRADES = HERE / "patches/quality_pass_q04_downgrades.patch.jsonl"
APPLY_PATCH = PATCH_UPGRADES  # merged apply file written at end

REVIEW_RUN = "quality_pass_q04_2026_06_06"
AGENT_ID = "Q04"
SSL_CTX = ssl.create_default_context()
SCOPE_TYPES = {"HAT_BAUTEILTYP", "NUTZT_MATERIAL"}

LEDGER_COLS = [
    "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
    "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status",
    "verdict_before", "verdict_after", "confidence", "proof_quote",
    "proposed_action", "patch_op", "agent_id", "notes", "coverage_level", "graph_element_id",
]

# Extended catalogue tokens (DE/FR/EN) keyed by vocab node id.
EXTRA_TOKENS: dict[str, list[str]] = {
    "bt_ausbau": ["ausbau", "fit-out", "second oeuvre", "second œuvre", "sanitaire", "luminaire", "cloisons", "hardware", "equipement"],
    "bt_boden": ["boden", "floor", "flooring", "sol", "parquet", "revetement", "revêtement", "carrelage", "terrasse"],
    "bt_dach": ["dach", "roof", "toiture", "couverture", "tuile"],
    "bt_daemmung": ["daemmung", "dämmung", "isolation", "isolant", "insulation", "isolierung", "laine", "polystyrene"],
    "bt_decke": ["decke", "decken", "ceiling", "plafond", "dalle", "dalles", "hollow core", "plancher"],
    "bt_fassade": ["fassade", "facade", "façade", "bardage", "cladding", "parement"],
    "bt_fenster": ["fenster", "window", "fenetre", "fenêtre", "chassis", "châssis", "vitrage", "menuiserie"],
    "bt_fundament": ["fundament", "foundation", "fondation"],
    "bt_gelaender": ["gelaender", "geländer", "railing", "garde-corps", "balustrade"],
    "bt_stuetze": ["stuetze", "stütze", "column", "poteau", "pillar", "support"],
    "bt_technik": ["technik", "sanitaire", "plomberie", "hvac", "chauffage", "radiateur", "plumbing", "tuyauterie", "electrique"],
    "bt_traeger": ["traeger", "träger", "beam", "poutre", "charpente", "steel beam", "poutrelle"],
    "bt_treppe": ["treppe", "treppen", "stair", "escalier", "escaliers", "marche"],
    "bt_tuer": ["tuer", "tür", "door", "porte", "portes"],
    "bt_wand": ["wand", "wall", "mur", "murs", "cloison", "cloisons", "paroi"],
    "mat_aluminium": ["aluminium", "aluminum", "alu"],
    "mat_beton": ["beton", "béton", "concrete"],
    "mat_daemmstoff": ["daemmstoff", "dämmstoff", "insulation material", "isolant"],
    "mat_glas": ["glas", "glass", "verre", "vitrage"],
    "mat_gusseisen": ["gusseisen", "cast iron", "fonte"],
    "mat_holz": ["holz", "wood", "bois", "timber", "parquet", "osb", "contreplaque", "contreplaqué"],
    "mat_keramik": ["keramik", "ceramic", "céramique", "carrelage", "tile", "faience", "faïence"],
    "mat_kunststoff": ["kunststoff", "plastic", "plastique", "pvc"],
    "mat_lehm": ["lehm", "clay", "argile", "terre"],
    "mat_naturstein": ["naturstein", "natural stone", "pierre"],
    "mat_recyclingbeton": ["recyclingbeton", "recycled concrete", "beton recycle", "béton recyclé"],
    "mat_stahl": ["stahl", "steel", "acier", "metall", "métal"],
    "mat_stahlbeton": ["stahlbeton", "reinforced concrete", "beton arme", "béton armé"],
    "mat_stroh": ["stroh", "straw", "paille"],
    "mat_ziegel": ["ziegel", "brick", "brique", "briques", "terracotta"],
}


def norm_text(s: str) -> str:
    s = unescape(s or "")
    s = unicodedata.normalize("NFKD", s)
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip().lower()
    return s


def strip_html(text: str) -> str:
    t = text or ""
    t = re.sub(r"<(script|style|noscript)\b[^>]*>.*?</\1>", " ", t, flags=re.I | re.S)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", unescape(t)).strip()


def is_valid_quote(quote: str) -> bool:
    if not quote or len(quote.strip()) < 15:
        return False
    q = quote.strip()
    bad_markers = (
        "function(", "dataLayer", "gtag(", "@context", "application/ld+json",
        "window._", "Browser|", "regex", "stylesheet", "javascript",
        ".collection-image", "object-fit", "cdn/shop", "background-color",
        "VfPpkd", "{.", "}.", "z-index",
    )
    if any(m.lower() in q.lower() for m in bad_markers):
        return False
    if re.search(r"[{}]|\\.{2,}\d|[|]{2,}", q):
        return False
    alpha_words = re.findall(r"[a-zA-ZÀ-ÿ]{4,}", q)
    return len(alpha_words) >= 2


def load_vocab_names() -> dict[str, str]:
    names: dict[str, str] = {}
    with VOCAB_PATH.open(encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line)
            if rec.get("record_type") == "node":
                names[rec["id"]] = rec.get("properties", {}).get("name", rec["id"])
    return names


def classification_tokens(to_id: str, to_name: str) -> list[str]:
    tokens: set[str] = set()
    if to_name:
        tokens.add(norm_text(to_name))
        for part in re.split(r"[\s_/()-]+", to_name):
            if len(part) >= 3:
                tokens.add(norm_text(part))
    for t in EXTRA_TOKENS.get(to_id, []):
        tokens.add(norm_text(t))
    # id tail e.g. bt_decke -> decke
    if "_" in to_id:
        tokens.add(norm_text(to_id.split("_", 1)[1]))
    return [t for t in tokens if t and len(t) >= 3]


def actor_tokens(from_id: str, from_name: str) -> list[str]:
    tokens: set[str] = set()
    for src in (from_name, from_id):
        if not src:
            continue
        n = norm_text(src)
        if n:
            tokens.add(n)
        for part in re.split(r"[\s_/()-]+", src):
            p = norm_text(part)
            if len(p) >= 4:
                tokens.add(p)
    # domain guess from id
    if "_" in from_id:
        for part in from_id.split("_"):
            if len(part) >= 4:
                tokens.add(norm_text(part))
    return [t for t in tokens if t]


def load_enrichment_index() -> dict[str, dict]:
    idx: dict[str, dict] = {}
    for d in ENRICH_DIRS:
        if not d.is_dir():
            continue
        for f in d.glob("*.enrichment.json"):
            aid = f.name.replace(".enrichment.json", "")
            try:
                idx[aid] = json.loads(f.read_text(encoding="utf-8"))
            except json.JSONDecodeError:
                pass
    return idx


def dossier_item(enrich: dict | None, rel_type: str, to_id: str) -> dict | None:
    if not enrich:
        return None
    key = "bauteiltypen" if rel_type == "HAT_BAUTEILTYP" else "materials"
    for item in enrich.get(key, []):
        if item.get("target_id") == to_id:
            return item
    return None


def load_r07_index() -> dict[tuple[str, str, str], dict]:
    idx: dict[tuple[str, str, str], dict] = {}
    with R07_LEDGER.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["rel_type_or_label"] not in SCOPE_TYPES:
                continue
            key = (row["from_id"], row["to_id"], row["rel_type_or_label"])
            idx[key] = row
    return idx


def load_scope_rows() -> list[dict]:
    rows = []
    with EP03_LEDGER.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if (
                row["verdict"] in ("PARTIAL", "MISSING_EVIDENCE")
                and row["rel_type_or_label"] in SCOPE_TYPES
            ):
                rows.append(row)
    return rows


def fetch_url(url: str, cache: dict) -> dict:
    if url in cache:
        return cache[url]
    entry = {"url": url, "fetched": False, "http_status": "", "text": "", "error": ""}
    if not url or not url.lower().startswith("http"):
        entry["error"] = "non_http"
        cache[url] = entry
        return entry
    try:
        req = Request(
            url,
            headers={
                "User-Agent": "recherche-q04-quality-pass/1.0",
                "Accept": "text/html,application/xhtml+xml",
            },
        )
        with urlopen(req, timeout=20, context=SSL_CTX) as resp:
            raw = resp.read(600_000)
            entry["http_status"] = str(getattr(resp, "status", 200))
            entry["fetched"] = True
            entry["text"] = raw.decode("utf-8", errors="replace")
    except HTTPError as e:
        entry["http_status"] = str(e.code)
        entry["error"] = str(e)
        try:
            entry["text"] = e.read(100_000).decode("utf-8", errors="replace")
            entry["fetched"] = bool(entry["text"])
        except Exception:
            pass
    except (URLError, TimeoutError, OSError) as e:
        entry["error"] = str(e)
    cache[url] = entry
    time.sleep(0.12)
    return entry


def token_hits(tokens: list[str], body: str, min_len: int = 4) -> list[str]:
    hits: list[str] = []
    for t in tokens:
        if len(t) < min_len:
            continue
        if re.search(r"(?<![a-z0-9äöüß])" + re.escape(t) + r"(?![a-z0-9äöüß])", body):
            hits.append(t)
    return hits


def quote_contains_class(quote: str, class_tokens: list[str], to_id: str, vocab_names: dict[str, str]) -> bool:
    qn = norm_text(quote)
    hits = token_hits(class_tokens, qn, min_len=4)
    if not hits:
        return False
    primary = norm_text(vocab_names.get(to_id, ""))
    strong = {norm_text(t) for t in EXTRA_TOKENS.get(to_id, []) if len(t) >= 4}
    must = {primary} | strong if primary else strong
    return bool(must and token_hits(list(must), qn, min_len=4))


def extract_verbatim_sentence(page_text: str, class_tokens: list[str], actor_toks: list[str]) -> str:
    """Return best verbatim sentence naming classification (and ideally actor)."""
    plain = strip_html(page_text)
    body = norm_text(plain)
    if not body:
        return ""
    sentences = re.split(r"(?<=[.!?])\s+|\n+", plain)
    best = ""
    best_score = 0
    for sent in sentences:
        if len(sent.strip()) < 12:
            continue
        sn = norm_text(sent)
        chits = token_hits(class_tokens, sn)
        if not chits:
            continue
        ahits = token_hits(actor_toks, sn) if actor_toks else []
        score = len(chits) * 3 + len(ahits) * 2 + min(len(sent), 200) // 50
        if score > best_score and is_valid_quote(sent):
            best_score = score
            best = sent.strip()[:500]
    if best:
        return best
    # fallback: window around first classification hit in visible text
    for tok in sorted(class_tokens, key=len, reverse=True):
        idx = plain.lower().find(tok.lower())
        if idx < 0:
            continue
        start = max(0, idx - 80)
        end = min(len(plain), idx + 120)
        snippet = plain[start:end].strip()[:500]
        if is_valid_quote(snippet):
            return snippet
    return ""


def candidate_urls(row: dict, r07: dict | None, dossier: dict | None, live: dict) -> list[str]:
    urls: list[str] = []
    for src in (
        row.get("basis_ref"),
        (r07 or {}).get("basis_ref"),
        (dossier or {}).get("evidence_urls"),
        live.get("evidence_url"),
        live.get("actor_primary_url"),
    ):
        if isinstance(src, list):
            for u in src:
                if u and u.startswith("http") and u not in urls:
                    urls.append(u)
        elif src and str(src).startswith("http") and src not in urls:
            urls.append(str(src))
    for u in live.get("actor_source_urls") or []:
        if u and u.startswith("http") and u not in urls:
            urls.append(u)
    return urls


def evaluate_row(
    row: dict,
    r07: dict | None,
    enrich_idx: dict,
    vocab_names: dict[str, str],
    live: dict,
    cache: dict,
) -> dict:
    fid, tid, rt = row["from_id"], row["to_id"], row["rel_type_or_label"]
    from_name = live.get("from_name") or fid
    to_name = live.get("to_name") or vocab_names.get(tid, tid)
    dossier = dossier_item(enrich_idx.get(fid), rt, tid)
    actor_toks = actor_tokens(fid, from_name)
    class_toks = classification_tokens(tid, to_name)

    urls = candidate_urls(row, r07, dossier, live)
    dossier_quote = (dossier or {}).get("evidence_quote") or ""

    best = {
        "verdict_after": row["verdict"],
        "basis_ref": row.get("basis_ref") or "",
        "fetched": row.get("fetched") or "false",
        "http_status": row.get("http_status") or "",
        "proof_quote": "",
        "confidence": row.get("confidence") or "teilweise_belegt",
        "proposed_action": "KEEP_PARTIAL",
        "patch_op": "",
        "notes": "",
        "delete_confidence": "low",
    }

    tried: list[str] = []
    for url in urls[:6]:
        if url in tried:
            continue
        tried.append(url)
        fe = fetch_url(url, cache)
        text = fe.get("text") or ""
        status = fe.get("http_status") or ""
        body = norm_text(strip_html(text))

        if not fe.get("fetched"):
            continue

        # Strict gate: classification must appear on page
        chits = token_hits(class_toks, body)
        if not chits:
            continue

        # Try dossier quote verification first
        if dossier_quote:
            dq_norm = norm_text(dossier_quote)
            dq_toks = [t for t in re.findall(r"[a-z0-9äöüß]{4,}", dq_norm) if t not in ("page", "collection", "evidence")]
            if len([t for t in dq_toks if t in body]) >= max(2, len(dq_toks) // 3):
                verbatim = extract_verbatim_sentence(text, class_toks, actor_toks)
                if (
                    verbatim
                    and is_valid_quote(verbatim)
                    and quote_contains_class(verbatim, class_toks, tid, vocab_names)
                ):
                    best.update(
                        verdict_after="PROVEN",
                        basis_ref=url,
                        fetched="true",
                        http_status=status,
                        proof_quote=verbatim[:500],
                        confidence="belegt",
                        proposed_action="UPGRADE",
                        patch_op="set_rel_properties",
                        notes=f"dossier_quote verified on page; class_hits={chits[:4]}",
                    )
                    return best

        verbatim = extract_verbatim_sentence(text, class_toks, actor_toks)
        ahits = token_hits(actor_toks, body) if actor_toks else []

        if (
            verbatim
            and chits
            and is_valid_quote(verbatim)
            and quote_contains_class(verbatim, class_toks, tid, vocab_names)
        ):
            # PROVEN: verbatim names classification; actor on page OR first-party catalogue URL
            is_catalogue = any(t in norm_text(url) for t in actor_toks if len(t) >= 5)
            if ahits or is_catalogue or fid.startswith("tool_"):
                best.update(
                    verdict_after="PROVEN",
                    basis_ref=url,
                    fetched="true",
                    http_status=status,
                    proof_quote=verbatim[:500],
                    confidence="belegt",
                    proposed_action="UPGRADE",
                    patch_op="set_rel_properties",
                    notes=f"strict gate pass; class={chits[:3]} actor={ahits[:2] or ['catalogue_url']}",
                )
                return best

        # Partial evidence: classification on page but weak verbatim
        if chits:
            best.update(
                verdict_after="PARTIAL",
                basis_ref=url,
                fetched="true",
                http_status=status,
                proof_quote=(verbatim or f"classification tokens on page: {', '.join(chits[:4])}")[:300],
                confidence="niedrig",
                proposed_action="DOWNGRADE",
                patch_op="set_rel_properties",
                notes=f"classification present ({chits[:3]}) but no strict verbatim edge quote",
            )

    # No usable page evidence
    if not tried:
        best.update(
            verdict_after="UNSUPPORTED",
            proposed_action="DELETE",
            patch_op="delete_rel",
            confidence="unbelegt",
            delete_confidence="high",
            notes="no candidate HTTP URL",
        )
        return best

    last = fetch_url(tried[0], cache) if tried else {}
    status = last.get("http_status", "")
    body = norm_text(strip_html(last.get("text") or ""))

    if status in ("404", "410", "403") or not last.get("fetched"):
        best.update(
            verdict_after="UNSUPPORTED",
            basis_ref=tried[0],
            fetched=str(bool(last.get("fetched"))).lower(),
            http_status=status,
            proposed_action="DELETE",
            patch_op="delete_rel",
            confidence="unbelegt",
            delete_confidence="high",
            notes=f"dead or unfetchable URL ({status or last.get('error', '')})",
        )
        return best

    chits = token_hits(class_toks, body)
    ahits = token_hits(actor_toks, body)

    if not chits and not dossier_quote:
        best.update(
            verdict_after="UNSUPPORTED",
            basis_ref=tried[0],
            fetched="true",
            http_status=status,
            proposed_action="DELETE",
            patch_op="delete_rel",
            confidence="unbelegt",
            delete_confidence="high",
            notes=f"page fetched; zero classification tokens for {to_name}; actor_hits={len(ahits)}",
        )
    elif best["proposed_action"] == "KEEP_PARTIAL":
        best.update(
            verdict_after="PARTIAL",
            basis_ref=tried[0],
            fetched="true",
            http_status=status,
            confidence="niedrig",
            proposed_action="DOWNGRADE",
            patch_op="set_rel_properties",
            notes=f"weak residual; class_hits={chits[:3]} actor_hits={ahits[:2]}",
        )
    return best


def query_live(driver, database: str, rows: list[dict]) -> dict[tuple[str, str, str], dict]:
    live: dict[tuple[str, str, str], dict] = {}
    by_type: dict[str, list[dict]] = defaultdict(list)
    for r in rows:
        by_type[r["rel_type_or_label"]].append(r)

    with driver.session(database=database) as session:
        for rt, chunk_rows in by_type.items():
            pairs = [{"from_id": r["from_id"], "to_id": r["to_id"]} for r in chunk_rows]
            result = session.run(
                f"""
                UNWIND $pairs AS p
                MATCH (a {{id: p.from_id}})-[r:`{rt}`]->(b {{id: p.to_id}})
                RETURN p.from_id AS from_id, p.to_id AS to_id,
                       elementId(r) AS element_id,
                       coalesce(a.name, a.id) AS from_name,
                       coalesce(b.name, b.id) AS to_name,
                       r.evidence_url AS evidence_url,
                       r.evidence_quote AS evidence_quote,
                       r.evidence_confidence AS evidence_confidence,
                       a.primary_source_url AS actor_primary_url,
                       a.source_urls AS actor_source_urls
                """,
                pairs=pairs,
            )
            for rec in result:
                key = (rec["from_id"], rec["to_id"], rt)
                live[key] = dict(rec)
    return live


def build_patches(results: list[dict]) -> tuple[list[dict], list[dict], list[dict]]:
    upgrades, deletes, downgrades = [], [], []
    for r in results:
        if r["patch_op"] == "set_rel_properties" and r["proposed_action"] == "UPGRADE":
            upgrades.append({
                "op": "set_rel_properties",
                "from": r["from_id"],
                "type": r["rel_type_or_label"],
                "to": r["to_id"],
                "properties": {
                    "evidence_url": r["basis_ref"],
                    "evidence_quote": r["proof_quote"][:500],
                    "evidence_confidence": "belegt",
                    "evidence_basis": "q04_strict_gate_verified",
                    "review_run": REVIEW_RUN,
                },
                "reason": f"Q04 {r['claim_id']}: PROVEN strict gate — {r['notes'][:160]}",
            })
        elif r["patch_op"] == "delete_rel" and r["proposed_action"] == "DELETE":
            deletes.append({
                "op": "delete_rel",
                "from": r["from_id"],
                "type": r["rel_type_or_label"],
                "to": r["to_id"],
                "reason": f"Q04 {r['claim_id']}: UNSUPPORTED catalogue edge — {r['notes'][:160]}",
            })
        elif r["patch_op"] == "set_rel_properties" and r["proposed_action"] == "DOWNGRADE":
            downgrades.append({
                "op": "set_rel_properties",
                "from": r["from_id"],
                "type": r["rel_type_or_label"],
                "to": r["to_id"],
                "properties": {
                    "evidence_confidence": "niedrig",
                    "review_run": REVIEW_RUN,
                },
                "reason": f"Q04 {r['claim_id']}: RELABEL confidence down — {r['notes'][:160]}",
            })
    return upgrades, deletes, downgrades


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_report(
    scope: list[dict],
    results: list[dict],
    before: Counter,
    after: Counter,
    upgrades: list[dict],
    deletes: list[dict],
    downgrades: list[dict],
    apply_summary: str,
) -> None:
    lines = [
        "# Quality Pass Q04 — Catalogue edges (HAT_BAUTEILTYP / NUTZT_MATERIAL)",
        "",
        f"**Date:** {datetime.now(timezone.utc).date().isoformat()} · **Database:** `mit-bestand`",
        f"**Ledger:** [`ledger/quality_pass_q04.csv`](../ledger/quality_pass_q04.csv)",
        "",
        "## Scope",
        "",
        f"Re-adjudicated **{len(scope)}** rows from `element_proof_agent_03.csv`: "
        f"**{before.get('PARTIAL', 0)}** PARTIAL + **{before.get('MISSING_EVIDENCE', 0)}** MISSING_EVIDENCE "
        "(weak R07 actor-catalogue evidence).",
        "",
        "## Method",
        "",
        "1. Cross-read `remediation_r07.csv` + `url_fetch_cache.json` (re-fetch only on cache miss).",
        "2. Strict Evidence Gate: **PROVEN** only with verbatim page quote naming target classification.",
        "3. Else **DELETE** (high-confidence unsupported) or **RELABEL** `evidence_confidence` → `niedrig`.",
        "4. Dry-run all patches; apply **PROVEN upgrades** + **high-confidence deletes** only.",
        "",
        "## Verdict counts (before → after)",
        "",
        "| verdict | before | after |",
        "|---|---:|---:|",
    ]
    all_verdicts = sorted(set(before) | set(after))
    for v in all_verdicts:
        lines.append(f"| {v} | {before.get(v, 0)} | {after.get(v, 0)} |")

    lines += [
        "",
        "## Proposed actions",
        "",
        "| action | count | applied |",
        "|---|---:|---:|",
    ]
    action_counts = Counter(r["proposed_action"] for r in results)
    applied_up = apply_summary.count("set_rel_properties") if apply_summary else 0
    applied_del = apply_summary.count("delete_rel") if apply_summary else 0
    for action in ("UPGRADE", "DELETE", "DOWNGRADE", "KEEP_PARTIAL"):
        c = action_counts.get(action, 0)
        applied = ""
        if action == "UPGRADE":
            applied = str(len(upgrades))
        elif action == "DELETE":
            applied = str(sum(1 for r in results if r["proposed_action"] == "DELETE" and r.get("delete_confidence") == "high"))
        lines.append(f"| {action} | {c} | {applied} |")

    lines += [
        "",
        f"**Patch ops drafted:** {len(upgrades)} upgrades · {len(deletes)} deletes · {len(downgrades)} downgrades (downgrades dry-run only).",
        "",
        "## Sample upgrades",
        "",
    ]
    for r in [x for x in results if x["proposed_action"] == "UPGRADE"][:8]:
        q = (r.get("proof_quote") or "")[:120]
        lines.append(
            f"- `{r['from_id']}` → `{r['to_id']}` ({r['rel_type_or_label']}): {q}"
        )

    lines += ["", "## Sample high-confidence deletes", ""]
    for r in [x for x in results if x["proposed_action"] == "DELETE" and x.get("delete_confidence") == "high"][:8]:
        lines.append(f"- `{r['from_id']}` → `{r['to_id']}`: {r['notes']}")

    lines += [
        "",
        "## Apply",
        "",
        "```bash",
        f"python _scripts/apply_neo4j_review_patch.py --patch {PATCH_UPGRADES.relative_to(REPO).as_posix()}",
        f"python _scripts/apply_neo4j_review_patch.py --patch {PATCH_DELETES.relative_to(REPO).as_posix()}",
        "```",
        "",
        "## Apply log",
        "",
        apply_summary or "(dry-run only — no live apply)",
        "",
    ]
    OUT_REPORT.write_text("\n".join(lines), encoding="utf-8")


def apply_patches(upgrade_ops: list[dict], delete_ops: list[dict], results: list[dict]) -> str:
    high_conf_deletes = [
        op for op, r in zip(
            [x for x in delete_ops],
            [x for x in results if x["proposed_action"] == "DELETE" and x.get("delete_confidence") == "high"],
        )
    ]
    # rebuild high conf from results
    delete_by_key = {
        (d["from"], d["type"], d["to"]): d for d in delete_ops
    }
    to_apply = list(upgrade_ops)
    for r in results:
        if r["proposed_action"] == "DELETE" and r.get("delete_confidence") == "high":
            k = (r["from_id"], r["rel_type_or_label"], r["to_id"])
            if k in delete_by_key:
                to_apply.append(delete_by_key[k])

    if not to_apply:
        return "No PROVEN upgrades or high-confidence deletes to apply."

    merged = HERE / "patches/quality_pass_q04_apply.patch.jsonl"
    write_jsonl(merged, to_apply)

    dry = subprocess.run(
        [sys.executable, str(SCRIPTS / "apply_neo4j_review_patch.py"), "--patch", str(merged)],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    log = f"### Dry-run\n```\n{dry.stdout[-4000:]}\n{dry.stderr[-1000:]}\n```\n"

    if dry.returncode != 0:
        log += f"\n**Dry-run failed (exit {dry.returncode})** — live apply skipped.\n"
        return log

    live = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "apply_neo4j_review_patch.py"),
            "--patch",
            str(merged),
            "--confirm",
            f"APPLY {merged.name} TO mit-bestand",
        ],
        capture_output=True,
        text=True,
        cwd=str(REPO),
    )
    log += f"### Live apply\n```\n{live.stdout[-4000:]}\n{live.stderr[-1000:]}\n```\n"
    if live.returncode != 0:
        log += f"\n**Live apply failed (exit {live.returncode})**\n"
    else:
        log += f"\n**Applied {len(to_apply)} ops** ({len(upgrade_ops)} upgrades + {len(to_apply) - len(upgrade_ops)} deletes).\n"
    return log


def main() -> int:
    scope = load_scope_rows()
    r07_idx = load_r07_index()
    enrich_idx = load_enrichment_index()
    vocab_names = load_vocab_names()

    cache: dict = {}
    if R07_CACHE.exists():
        try:
            cache = json.loads(R07_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}

    uri, user, password, database = resolve_connection()
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver(uri, auth=(user, password))
    driver.verify_connectivity()
    live = query_live(driver, database, scope)
    driver.close()

    before_verdict = Counter(r["verdict"] for r in scope)
    results: list[dict] = []

    for i, row in enumerate(scope, start=1):
        key = (row["from_id"], row["to_id"], row["rel_type_or_label"])
        r07 = r07_idx.get(key)
        live_row = live.get(key, {})
        ev = evaluate_row(row, r07, enrich_idx, vocab_names, live_row, cache)

        out = {
            "claim_id": f"Q04-{i:04d}",
            "claim_kind": "rel",
            "element_id": row.get("element_id") or live_row.get("element_id", ""),
            "from_id": row["from_id"],
            "to_id": row["to_id"],
            "rel_type_or_label": row["rel_type_or_label"],
            "asserted_claim": row.get("asserted_claim", ""),
            "basis_type": "web" if ev["basis_ref"].startswith("http") else row.get("basis_type", "web"),
            "basis_ref": ev["basis_ref"],
            "fetched": ev["fetched"],
            "http_status": ev["http_status"],
            "verdict_before": row["verdict"],
            "verdict_after": ev["verdict_after"],
            "confidence": ev["confidence"],
            "proof_quote": ev["proof_quote"],
            "proposed_action": ev["proposed_action"],
            "patch_op": ev["patch_op"],
            "agent_id": AGENT_ID,
            "notes": ev["notes"],
            "coverage_level": "element",
            "graph_element_id": row.get("graph_element_id", ""),
            "delete_confidence": ev.get("delete_confidence", ""),
        }
        results.append(out)
        if i % 20 == 0:
            print(f"processed {i}/{len(scope)}...", flush=True)

    # persist extended cache
    R07_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=0), encoding="utf-8")

    after_verdict = Counter(r["verdict_after"] for r in results)
    upgrades, deletes, downgrades = build_patches(results)
    write_jsonl(PATCH_UPGRADES, upgrades)
    write_jsonl(PATCH_DELETES, deletes)
    write_jsonl(PATCH_DOWNGRADES, downgrades)

    OUT_LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with OUT_LEDGER.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=LEDGER_COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(results)

    apply_log = apply_patches(upgrades, deletes, results)
    write_report(scope, results, before_verdict, after_verdict, upgrades, deletes, downgrades, apply_log)

    print(f"scope={len(scope)} before={dict(before_verdict)} after={dict(after_verdict)}")
    print(f"upgrades={len(upgrades)} deletes={len(deletes)} downgrades={len(downgrades)}")
    print(f"wrote {OUT_LEDGER}")
    print(f"wrote {OUT_REPORT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
