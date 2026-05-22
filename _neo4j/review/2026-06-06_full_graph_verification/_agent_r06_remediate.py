#!/usr/bin/env python3
"""Remediation Wave 2 — Agent R06: dead regulation source_url fixes (Agent 07 scope)."""
from __future__ import annotations

import csv
import json
import re
import ssl
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER_IN = ROOT / "ledger" / "agent_07.csv"
LEDGER_OUT = ROOT / "ledger" / "remediation_r06.csv"
REPORT_OUT = ROOT / "reports" / "remediation_r06.md"
PATCH_OUT = ROOT / "patches" / "remediation_r06_regulation_urls.patch.jsonl"

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
)
CTX = ssl.create_default_context()
RUN_DATE = "2026-06-06"

# Candidate alternates per dead/unverifiable URL (from Agent 07 notes + fresh search).
URL_FIXES: dict[str, dict] = {
    "https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/neue-gefahrstoffverordnung-2024": {
        "candidates": [
            "https://bauportal.bgbau.de/bauportal-12025/rund-um-die-bg-bau/novellierung-gefahrstoffverordnung-umgang-mit-asbest",
            "https://www.bgbau.de/themen/sicherheit-und-gesundheit/asbest/",
            "https://www.bgbau.de/fileadmin/Medien-Objekte/Medien/Sonstige_Medien/Infoblatt_neue_Gefahrstoffverordnung_2024_bf.pdf",
        ],
        "needles": ["31. Oktober 1993", "31.10.1993", "Asbest", "Informations", "Mitwirkung"],
        "min_hits": 3,
    },
    "https://www.endk.ch/de/energiepolitik/muken": {
        "candidates": [
            "https://www.endk.ch/energiepolitik/",
            "https://www.endk.ch/de/energiepolitik/",
        ],
        "needles": ["MuKEn", "Mustervorschriften", "Energie"],
        "min_hits": 2,
    },
    "https://www.vdi.de/richtlinien/details/vdi-3492-messen-von-innenraumluftverunreinigungen-messen-von-immissionen-messen-anorganischer-faserfoermiger-partikel-rasterelektronenmikroskopisches-verfahren": {
        "candidates": [
            "https://www.vdi.de/mitgliedschaft/vdi-richtlinien/details/vdi-3492-innenraumluft-aussenluft-messen-anorganischer-faserfoermiger-partikel-rasterelektronenmikroskopisches-verfahren",
            "https://www.vdi.de/news/detail/faserbelastung-in-der-luft-richtlinie-zur-messung-anorganischer-fasern",
        ],
        "needles": ["3492", "faser", "Chrysotil", "REM", "Amphibol"],
        "min_hits": 3,
    },
    "https://www.fib-international.org/publications/fib-bulletins/special-design-considerations-for-precast-prestress-pdf-detail.html": {
        "candidates": [
            "https://shop.fib-international.org/publications/fib-bulletins/228-special-design-considerations-for-precast-prestress-hollow-core-floors-pdf",
            "https://www.fib-international.org/tags-search/productslist/tg6_1.html",
        ],
        "needles": ["hollow core", "prestressed", "Bulletin", "006", "Special design"],
        "min_hits": 2,
    },
    "https://vito.be/en/news/demolition-guide-recognizes-building-materials-recycling-or-reuse": {
        "candidates": [
            "https://ovam.vlaanderen.be/bouw-sloopopvolging",
            "https://www.tauw.be/vakgebieden/sloopopvolging/tracimat.html",
            "https://www.hiserproject.eu/index_php/pozycja-1/80-news/172-tracimat-recognised-as-a-cdw-management-organisation/",
        ],
        "needles": [
            "Tracimat",
            "enige erkende",
            "only",
            "sloopbeheerorganisatie",
            "demolition management",
        ],
        "min_hits": 2,
        "claim_needles": ["Tracimat", "enige erkende", "only recognised", "only recognized"],
    },
}


def fetch(url: str, timeout: int = 30) -> tuple[int | None, str, str]:
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=timeout, context=CTX) as resp:
            body = resp.read(800_000).decode("utf-8", errors="replace")
            return resp.status, resp.geturl(), body
    except urllib.error.HTTPError as exc:
        try:
            body = exc.read(200_000).decode("utf-8", errors="replace")
        except Exception:
            body = ""
        return exc.code, url, body
    except Exception as exc:
        return None, url, str(exc)


def needle_hits(body: str, needles: list[str]) -> list[str]:
    low = body.lower()
    return [n for n in needles if n.lower() in low]


def verify_url(url: str, spec: dict) -> dict:
    status, final_url, body = fetch(url)
    hits = needle_hits(body, spec["needles"])
    claim_hits = (
        needle_hits(body, spec["claim_needles"])
        if "claim_needles" in spec
        else hits
    )
    ok = status == 200 and len(hits) >= spec["min_hits"]
    # For Tracimat claim we need explicit Tracimat + recognition language.
    if "claim_needles" in spec and ok:
        ok = len(claim_hits) >= 2
    snippet = ""
    if body and not body.startswith("HTTP"):
        text = re.sub(r"<[^>]+>", " ", body)
        text = re.sub(r"\s+", " ", text).strip()
        for needle in spec.get("claim_needles") or spec["needles"]:
            idx = text.lower().find(needle.lower())
            if idx >= 0:
                snippet = text[max(0, idx - 40) : idx + 120].strip()
                break
        if not snippet and len(text) > 80:
            snippet = text[:200]
    return {
        "url": url,
        "http_status": status,
        "final_url": final_url,
        "hits": hits,
        "claim_hits": claim_hits,
        "ok": ok,
        "snippet": snippet[:300],
        "paywalled": status == 200 and len(body) < 500 and "login" in body.lower(),
    }


def pick_fix(old_url: str, spec: dict) -> dict:
    old_check = verify_url(old_url, spec)
    result = {
        "old_url": old_url,
        "old_status": old_check["http_status"],
        "old_ok": old_check["ok"],
        "new_url": None,
        "new_status": None,
        "new_ok": False,
        "proof_quote": "",
        "verdict": "UNVERIFIABLE",
        "note": "",
    }
    if old_check["ok"]:
        result["new_url"] = old_url
        result["new_status"] = old_check["http_status"]
        result["new_ok"] = True
        result["proof_quote"] = old_check["snippet"]
        result["verdict"] = "PROVEN"
        result["note"] = "Original URL now resolves; no patch needed."
        return result

    for cand in spec["candidates"]:
        check = verify_url(cand, spec)
        if check["paywalled"]:
            result["note"] = f"Paywalled/login gate at {cand}"
            continue
        if check["ok"]:
            result["new_url"] = check["final_url"]
            result["new_status"] = check["http_status"]
            result["new_ok"] = True
            result["proof_quote"] = check["snippet"]
            result["verdict"] = "PROVEN"
            result["note"] = f"Moved/dead link; confirmed alternate at {check['final_url']}"
            return result

    result["note"] = "No working alternate confirmed from candidate list."
    return result


def load_scope_rows() -> list[dict]:
    rows = []
    with LEDGER_IN.open(encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["verdict"] in ("DEAD_LINK", "UNVERIFIABLE") and row["proposed_action"] == "RESOURCE":
                rows.append(row)
    return rows


def main() -> None:
    scope = load_scope_rows()
    url_groups: dict[str, list[dict]] = defaultdict(list)
    for row in scope:
        url_groups[row["basis_ref"]].append(row)

    fixes: dict[str, dict] = {}
    for old_url in url_groups:
        spec = URL_FIXES.get(old_url)
        if not spec:
            fixes[old_url] = {
                "old_url": old_url,
                "verdict": "UNVERIFIABLE",
                "note": "No candidate list configured.",
            }
            continue
        fixes[old_url] = pick_fix(old_url, spec)

    # Build remediation ledger rows.
    rem_cols = [
        "claim_id", "claim_kind", "element_id", "from_id", "to_id", "rel_type_or_label",
        "asserted_claim", "basis_type", "basis_ref", "fetched", "http_status", "verdict",
        "confidence", "proof_quote", "proposed_action", "agent_id", "notes",
        "remediation_status", "new_source_url", "r06_verdict", "r06_fetched", "r06_http_status",
    ]
    rem_rows: list[dict] = []
    patch_ops: list[dict] = []

    status_counts: Counter = Counter()
    verdict_counts: Counter = Counter()

    for row in scope:
        old_url = row["basis_ref"]
        fix = fixes[old_url]
        new_url = fix.get("new_url")
        r06_verdict = fix.get("verdict", "UNVERIFIABLE")
        if new_url and fix.get("new_ok"):
            remediation_status = "FIXED"
            proposed = "KEEP"
            confidence = "belegt"
            status_counts["fixed"] += 1
            patch_ops.append({
                "op": "set_rel_properties",
                "from": row["from_id"],
                "type": row["rel_type_or_label"],
                "to": row["to_id"],
                "properties": {"source_url": new_url},
                "reason": (
                    f"R06 {row['claim_id']}: replace dead/unverifiable regulation source_url "
                    f"({old_url[:60]}... -> {new_url[:60]}...)"
                ),
            })
        else:
            remediation_status = "DEFERRED"
            proposed = "RESOURCE"
            confidence = row["confidence"]
            status_counts["deferred"] += 1

        verdict_counts[r06_verdict] += 1
        rem_rows.append({
            **row,
            "proposed_action": proposed,
            "confidence": confidence,
            "remediation_status": remediation_status,
            "new_source_url": new_url or "",
            "r06_verdict": r06_verdict,
            "r06_fetched": "true",
            "r06_http_status": str(fix.get("new_status") or fix.get("old_status") or ""),
            "notes": f"R06: {fix.get('note', '')}; agent07: {row.get('notes', '')}",
            "proof_quote": fix.get("proof_quote") or row.get("proof_quote", ""),
        })

    LEDGER_OUT.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER_OUT.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=rem_cols, quoting=csv.QUOTE_ALL)
        w.writeheader()
        w.writerows(rem_rows)

    PATCH_OUT.parent.mkdir(parents=True, exist_ok=True)
    with PATCH_OUT.open("w", encoding="utf-8") as f:
        for op in patch_ops:
            f.write(json.dumps(op, ensure_ascii=False) + "\n")

    # Markdown report.
    lines = [
        "# Remediation R06 — Dead Regulation URLs (Agent 07)",
        "",
        f"**Agent:** R06 · **Date:** {RUN_DATE} · **Scope:** Agent 07 `DEAD_LINK` + `UNVERIFIABLE` / `RESOURCE`",
        f"**Input:** [`ledger/agent_07.csv`](../ledger/agent_07.csv) · **Output ledger:** [`ledger/remediation_r06.csv`](../ledger/remediation_r06.csv)",
        f"**Patch:** [`patches/remediation_r06_regulation_urls.patch.jsonl`](../patches/remediation_r06_regulation_urls.patch.jsonl)",
        "",
        "## Summary",
        "",
        f"| Metric | Count |",
        f"|---|---:|",
        f"| Scope relationships | {len(scope)} |",
        f"| Distinct dead/unverifiable URLs | {len(url_groups)} |",
        f"| Fixed (confirmed alternate) | {status_counts['fixed']} |",
        f"| Deferred (no confirmed fix) | {status_counts['deferred']} |",
        f"| Patch ops (`set_rel_properties`) | {len(patch_ops)} |",
        "",
        "### URL-level fixes",
        "",
        "| rels | agent07 verdict | old URL | new URL | R06 verdict | note |",
        "|---:|---|---|---|---|---|",
    ]
    for old_url, group in sorted(url_groups.items(), key=lambda x: -len(x[1])):
        fix = fixes[old_url]
        new = fix.get("new_url") or "—"
        lines.append(
            f"| {len(group)} | {group[0]['verdict']} | `{old_url[:70]}…` | "
            f"`{new[:70]}{'…' if len(str(new)) > 70 else ''}` | {fix.get('verdict')} | {fix.get('note', '')} |"
        )

    lines.extend([
        "",
        "## Method",
        "",
        "- Re-fetched each stored `source_url` and candidate alternates from Agent 07 notes.",
        "- Confirmed fix only when HTTP 200 and page body contains claim-specific needles.",
        "- Paywalled/login-gated pages marked **UNVERIFIABLE**, never **PROVEN**.",
        "- Patch uses `set_rel_properties` with `source_url` only (non-destructive).",
        "",
        "## Apply",
        "",
        "```bash",
        "python _scripts/apply_neo4j_review_patch.py \\",
        "  --patch _neo4j/review/2026-06-06_full_graph_verification/patches/remediation_r06_regulation_urls.patch.jsonl",
        "```",
        "",
        f"Generated {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}.",
    ])
    REPORT_OUT.write_text("\n".join(lines) + "\n", encoding="utf-8")

    print(f"scope_rows={len(scope)} url_groups={len(url_groups)}")
    print(f"fixed={status_counts['fixed']} deferred={status_counts['deferred']} patch_ops={len(patch_ops)}")
    print(f"wrote {LEDGER_OUT}")
    print(f"wrote {REPORT_OUT}")
    print(f"wrote {PATCH_OUT}")
    for old, fix in fixes.items():
        print(f"  {old[:55]}... -> {fix.get('new_url', 'NONE')} [{fix.get('verdict')}]")


if __name__ == "__main__":
    main()
