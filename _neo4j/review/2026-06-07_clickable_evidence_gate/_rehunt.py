"""Phase 2b — gate-validated re-hunt for the bad-link claims.

For every claim flagged QUOTE_MISMATCH / HOMEPAGE_ONLY / LINK_DEAD (non-bot-blocked),
discover candidate deep links from:
  1. the claim endpoints' own source_urls / primary_source_url,
  2. source_urls of Projekt nodes within 2 hops,
  3. DuckDuckGo HTML search (quote nouns + subject name).
Each candidate is validated with the SAME gate (quote-on-page). A new evidence_url is
proposed ONLY when the quote is verbatim/strong on that page. Nothing is applied; no deletes.
"""

from __future__ import annotations

import csv
import json
import re
import sys
import time
import urllib.parse
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
SCRIPTS = REPO / "_scripts"
sys.path.insert(0, str(SCRIPTS))
from neo4j_env import resolve_connection  # noqa: E402
import verify_clickable_evidence as ceg  # noqa: E402

csv.field_size_limit(10_000_000)
BASELINE = HERE / "CLICKABLE_EVIDENCE_BASELINE.csv"
OUT_LEDGER = HERE / "REHUNT_LEDGER.csv"
OUT_PATCH = HERE / "patches" / "ceg_rehunt_recovered_links.patch.jsonl"
BOT_BLOCKED = {"403", "401", "503", "429"}
BAD = {"QUOTE_MISMATCH", "HOMEPAGE_ONLY", "LINK_DEAD"}
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
STOPWORDS = ceg.STOP | {"reused", "neue", "alte", "funktion", "anzahl"}


def quote_terms(quote: str, n: int = 6) -> list[str]:
    words = [w for w in re.findall(r"[a-zaeoeue0-9]{5,}", ceg.norm(quote)) if w not in STOPWORDS]
    seen, out = set(), []
    for w in words:
        if w not in seen:
            seen.add(w); out.append(w)
        if len(out) >= n:
            break
    return out


def ddg_results(query: str, cache: dict, limit: int = 6) -> list[str]:
    url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
    ent = ceg.fetch(url, cache)
    if not ent.get("ok"):
        # DDG html page is normalized; fall back to raw norm search for uddg
        pass
    text = ent.get("norm", "")
    out = []
    for m in re.finditer(r"uddg=([^&\"]+)", text):
        try:
            cand = urllib.parse.unquote(m.group(1))
        except Exception:  # noqa: BLE001
            continue
        if cand.startswith("http") and cand not in out:
            out.append(cand)
        if len(out) >= limit:
            break
    return out


def main() -> None:
    rows = [r for r in csv.DictReader(BASELINE.open(encoding="utf-8")) if r["evidence_status"] in BAD]
    # skip bot-blocked dead (likely fine for humans)
    rows = [r for r in rows if not (r["evidence_status"] == "LINK_DEAD" and r["http_status"] in BOT_BLOCKED)]
    rel_rows = [r for r in rows if r["kind"] == "rel"]
    node_rows = [r for r in rows if r["kind"] == "node"]
    print(f"re-hunt scope: {len(rows)} bad claims ({len(rel_rows)} rel / {len(node_rows)} node)")

    from neo4j import GraphDatabase

    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    ctx: dict[str, dict] = {}  # eid -> {from,to,type,rid,cands:set}
    try:
        with driver.session(database=database) as s:
            for r in rel_rows:
                rec = s.run(
                    "MATCH (a)-[rel]->(b) WHERE elementId(rel)=$eid "
                    "OPTIONAL MATCH (a)-[*1..2]-(p:Projekt) "
                    "WITH a,b,rel, collect(DISTINCT p) AS ps "
                    "RETURN a.id AS fid, b.id AS tid, type(rel) AS t, rel.id AS rid, "
                    "a.source_urls AS asu, a.primary_source_url AS apu, "
                    "b.source_urls AS bsu, "
                    "[x IN ps | x.source_urls] AS psu, [x IN ps | x.primary_source_url] AS ppu",
                    eid=r["eid"],
                ).single()
                if not rec:
                    continue
                cands: list[str] = []
                for v in [rec["apu"]] + (rec["ppu"] or []):
                    if v and v.startswith("http"):
                        cands.append(v)
                for lst in [rec["asu"], rec["bsu"]] + (rec["psu"] or []):
                    for v in (lst or []):
                        if v and v.startswith("http"):
                            cands.append(v)
                ctx[r["eid"]] = {"from": rec["fid"], "to": rec["tid"], "type": rec["t"],
                                 "rid": rec["rid"], "cands": list(dict.fromkeys(cands))}
            for r in node_rows:
                rec = s.run(
                    "MATCH (n) WHERE elementId(n)=$eid "
                    "RETURN n.id AS nid, n.source_urls AS su, n.primary_source_url AS pu",
                    eid=r["eid"],
                ).single()
                if not rec:
                    continue
                cands = [v for v in ([rec["pu"]] + (rec["su"] or [])) if v and v.startswith("http")]
                ctx[r["eid"]] = {"nid": rec["nid"], "cands": list(dict.fromkeys(cands))}
    finally:
        driver.close()

    cache: dict[str, dict] = {}
    if ceg.CACHE_PATH.is_file():
        cache = json.loads(ceg.CACHE_PATH.read_text(encoding="utf-8"))
        print(f"loaded fetch cache: {len(cache)} urls")

    out_rows, patch_ops = [], []
    recovered = 0
    for i, r in enumerate(rows, 1):
        c = ctx.get(r["eid"])
        if not c:
            continue
        quote = r["quote"]
        anchors = [r["subject"], r["object"]]
        failed_url = r["url"]
        candidates = [u for u in c["cands"] if u != failed_url and not ceg.is_homepage(u)]
        # add web search candidates
        terms = quote_terms(quote)
        subj = re.sub(r"[^a-zA-Z0-9\s]", " ", r["subject"])[:40]
        if terms:
            q = subj + " " + " ".join(terms[:4])
            try:
                candidates += [u for u in ddg_results(q, cache) if u != failed_url and not ceg.is_homepage(u)]
            except Exception:  # noqa: BLE001
                pass
        candidates = list(dict.fromkeys(candidates))[:8]

        best = None
        for u in candidates:
            ent = ceg.fetch(u, cache)
            if not ent.get("ok"):
                continue
            mk, ratio, hits = ceg.quote_on_page(quote, anchors, ent.get("norm", ""))
            if mk in {"VERBATIM", "STRONG"}:
                best = (u, mk, ratio)
                break
        if best:
            recovered += 1
            u = best[0]
            if r["kind"] == "rel":
                sel = {"id": c["rid"]} if c.get("rid") else {"from": c["from"], "type": c["type"], "to": c["to"]}
                patch_ops.append({"op": "set_rel_properties", **sel,
                                  "properties": {"evidence_url": u, "evidence_status": "CLICKABLE_VERIFIED",
                                                 "evidence_checked_at": NOW},
                                  "reason": f"CEG re-hunt recovered ({best[1]} {best[2]:.2f})"})
            else:
                patch_ops.append({"op": "set_node_properties", "id": c["nid"],
                                  "properties": {"primary_source_url": u, "evidence_status": "CLICKABLE_VERIFIED",
                                                 "evidence_checked_at": NOW},
                                  "reason": f"CEG re-hunt recovered ({best[1]} {best[2]:.2f})"})
        out_rows.append({
            "kind": r["kind"], "type": r["type"], "subject": r["subject"][:60],
            "old_status": r["evidence_status"], "old_url": failed_url,
            "result": "RECOVERED" if best else "STILL_UNVERIFIED",
            "new_url": best[0] if best else "", "match": best[1] if best else "",
            "candidates_tried": len(candidates), "quote": quote[:120],
        })
        if i % 10 == 0:
            print(f"  {i}/{len(rows)} processed, recovered {recovered}")
            ceg.CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
            time.sleep(0.2)

    ceg.CACHE_PATH.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
    with OUT_LEDGER.open("w", encoding="utf-8", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(out_rows[0].keys()))
        w.writeheader(); w.writerows(out_rows)
    OUT_PATCH.parent.mkdir(parents=True, exist_ok=True)
    with OUT_PATCH.open("w", encoding="utf-8") as fh:
        for op in patch_ops:
            fh.write(json.dumps(op, ensure_ascii=False) + "\n")

    print(f"\n=== re-hunt done ===\nrecovered: {recovered}/{len(rows)}")
    print(f"ledger: {OUT_LEDGER}\npatch:  {OUT_PATCH} ({len(patch_ops)} ops)")


if __name__ == "__main__":
    main()
