#!/usr/bin/env python3
"""Verify the strongest research-only logo leads for current `none` rows."""

from __future__ import annotations

import csv
import io
import json
import ssl
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

from PIL import Image


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "bilder_full"
OUT_JSON = DATA / "MISSING_LOGO_CURATED_LEADS.json"
OUT_CSV = DATA / "MISSING_LOGO_CURATED_LEADS.csv"
OUT_MD = DATA / "MISSING_LOGO_CURATED_LEADS.md"

# These are not accepted assets.  They are the strongest exact-name/header
# leads found by the crawl and still require visual identity and rights review.
LEADS = [
    ("BE:G01", "https://feder.brussels/wp-content/uploads/2024/09/BI-FR-LOGO-WHITE.png", "high", "Current first-party FEDER Brussels wordmark."),
    ("BE:I04", "https://ovam.vlaanderen.be/o/ovam-website-theme/assets/images/logo_be.png", "manual_parent", "Official OVAM page header asset; verify whether it is OVAM or the Flemish-government umbrella mark."),
    ("BE:M28", "http://www.recupan.be/wp-content/uploads/2012/12/logo.gif", "high", "Exact first-party Recupan logo-named image."),
    ("BE:M32", "http://www.vanhuele.be/wp-content/uploads/2015/08/VanHuele_Logo.png", "high", "Exact first-party Van Huele logo-named image."),
    ("CH:M07", "https://www.bauteilverwertung.ch/img/logo2.png", "high", "Exact first-party Bauteilverwertung logo-named image."),
    ("CH:U20", "https://www.pascalflammer.com/static/favicon/apple-touch-icon.891ee2c70a35.png", "manual_icon", "First-party Apple Touch icon; verify against full Pascal Flammer identity."),
    ("DE:N02", "http://www.bauteilnetz.de/bauteilnetz/bilder/btn/logos/logo_schrift_384_weiss.png", "high", "Exact first-party bauteilnetz wordmark."),
    ("DE:U14", "https://zusammenarbeiter.de/img/dza_logo.png", "high", "Exact first-party Die Zusammenarbeiter logo-named image."),
    ("DK:M02", "https://www.xn--byggebrsen-5cb.dk/icons/apple-touch-icon.png", "manual_icon", "Current exact first-party Byggebørsen site icon."),
    ("FI:U04", "https://durat.fi/cdn/shop/files/Durat_logo_1200_x_3390_px_3.png?v=1731570759", "high", "Exact current first-party Durat logo; visually checked at its native 1200 x 3390 px resolution."),
    ("FR:M05", "https://bathestia.fr/img_fixes/logo_blanc_100px.webp", "low_resolution", "Exact first-party Bathestia wordmark, likely below the 128 px minimum."),
    ("FR:M09", "https://brocantique.pro/wp-content/uploads/2021/04/Logo-le-BrocAntique-site.png", "ambiguous_identity", "Exact logo on a same-name site; graph-to-business identity still unconfirmed."),
    ("FR:M53", "https://cdn-ilcaikb.nitrocdn.com/OViQksRGSgJCzcTfExhRTmXbgKDmkOSO/assets/images/optimized/rev-9acf7ef/pierredetaille-gironde.fr/wp-content/uploads/2025/08/cropped-logo-saint-emilion-materiaux-negoce-vente-pierre-naturelle-neuf-ancien-192x192.png", "high", "Exact first-party Saint Emilion Matériaux icon."),
    ("FR:S02", "https://cyclezero.fr/src/img/logo.png", "high", "Exact first-party Cycle Zéro logo."),
    ("GB:U30", "https://www.grantsint.com/wp-content/uploads/2023/01/grants-logo.png", "high", "Exact first-party Grants wordmark."),
    ("GB:X03", "https://www.warp-it.co.uk/images/login/logo.png", "high", "Exact first-party Warp It login/header logo."),
    ("NL:M09", "https://woodfarm.nl/wp-content/uploads/Naamloos.png", "manual_identity", "First-party header image; verify that it represents Handelsonderneming Klepper/Woodfarm."),
    ("NL:M13", "https://www.antieketegel.nl/wp-content/uploads/2016/09/logoregtsantieketegels.png", "high", "Exact first-party Regts Antieke Tegels logo."),
    ("SE:U20", "https://teknikbyggarna.se/gfx/logo.png", "high", "Exact first-party Teknikbyggarna header logo."),
]

# Rights findings are research notes only.  None of them is converted into a
# publication clearance by this script.
RIGHTS_RESEARCH = {
    "BE:G01": {
        "rights_research_status": "official_communications_kit_scope_review_required",
        "rights_source_url": "https://feder.brussels/wp-content/uploads/2024/03/FEDER_KIT-COM-2021-2027.zip",
        "rights_research_note": "Official 2021-2027 communications kit contains PNG, EPS and AI logo variants plus guidance; intended-use scope still requires manual review.",
    },
    "FI:U04": {
        "rights_research_status": "official_marketing_contact_found_permission_not_requested",
        "rights_source_url": "https://durat.fi/pages/yhteystiedot",
        "rights_research_note": "Official contact page identifies marketing and communications contacts; no permission request has been sent.",
    },
    "FR:M05": {
        "rights_research_status": "official_site_restricts_reproduction_permission_required",
        "rights_source_url": "https://bathestia.fr/mentions-legales.html",
        "rights_research_note": "Official legal notice restricts reproduction of site illustrations without prior agreement; the logo must not be treated as cleared.",
    },
    "FR:S02": {
        "rights_research_status": "official_press_contact_found_permission_not_requested",
        "rights_source_url": "https://cyclezero.fr/presse.html",
        "rights_research_note": "Official press page gives a communications contact; no permission request has been sent.",
    },
    "GB:X03": {
        "rights_research_status": "official_press_communications_use_statement_scope_review_required",
        "rights_source_url": "https://www.warp-it.co.uk/App_Pages/downloads/Content/logos.aspx",
        "rights_research_note": "Official page says its logo package may be used for the user's own press releases or communications; the linked ZIP currently returns 404 and scope still needs manual review.",
    },
}


def probe(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 AkteursnetzResearch/1.0"})
    ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, timeout=12, context=ctx) as response:
            data = response.read(8_000_000)
            content_type = response.headers.get_content_type()
            final_url = response.geturl()
        width = height = None
        fmt = ""
        try:
            with Image.open(io.BytesIO(data)) as im:
                width, height = im.size
                fmt = (im.format or "").lower()
        except Exception:
            if data.lstrip().startswith(b"<svg") or b"<svg" in data[:1000]:
                fmt = "svg"
        minimum_ok = fmt == "svg" or (width is not None and min(width, height) >= 128)
        return {"access": "ok", "final_url": final_url, "content_type": content_type, "format": fmt, "width": width, "height": height, "minimum_128_ok": minimum_ok}
    except Exception as exc:
        return {"access": f"error:{type(exc).__name__}:{str(exc)[:180]}", "final_url": "", "content_type": "", "format": "", "width": None, "height": None, "minimum_128_ok": False}


def main():
    identity = json.loads((DATA / "CURRENT_LOGO_IDENTITY_AUDIT.json").read_text(encoding="utf-8"))
    by_key = {r["key"]: r for r in identity["nodes"]}
    rows = []
    for key, url, confidence, note in LEADS:
        node = by_key[key]
        rows.append({
            "key": key, "cc": node["cc"], "tid": node["tid"], "name": node["name"],
            "official_url": node.get("official_url") or "", "candidate_url": url,
            "research_confidence": confidence, "research_note": note,
            **probe(url), "decision": "unreviewed_research_lead",
            "publication_clearance": "not_cleared",
            **RIGHTS_RESEARCH.get(key, {
                "rights_research_status": "no_explicit_logo_permission_found",
                "rights_source_url": "",
                "rights_research_note": "",
            }),
        })
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    payload = {
        "schema_version": "curated-missing-logo-leads-v1", "created_at": now,
        "boundary": "Research only: no review, asset, style, opacity, render, rights or Neo4j state changed.",
        "counts": {
            "curated_leads": len(rows), "accessible": sum(r["access"] == "ok" for r in rows),
            "minimum_128_ok": sum(r["minimum_128_ok"] for r in rows),
            "high_identity_confidence": sum(r["research_confidence"] == "high" for r in rows),
        }, "nodes": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        fields = list(rows[0]); w = csv.DictWriter(f, fieldnames=fields); w.writeheader(); w.writerows(rows)
    lines = ["# Kuratierte Logo-Leads für aktuelle `none`-Organisationen", "",
             "Nur Recherche; keine Auswahl, kein Assetbau und keine Freigabe.", "",
             f"- Kuratierte Leads: **{len(rows)}**",
             f"- Erreichbar: **{payload['counts']['accessible']}**",
             f"- Technische Mindestkante/SVG bestanden: **{payload['counts']['minimum_128_ok']}**",
             f"- Hohe vorläufige Identitätskonfidenz: **{payload['counts']['high_identity_confidence']}**", "",
             "| Key | Organisation | Identität | Technik | Quelle |", "|---|---|---|---|---|"]
    for r in rows:
        tech = f"{r['format']} {r['width']}×{r['height']}" if r["access"] == "ok" else r["access"]
        lines.append(f"| `{r['key']}` | {r['name']} | {r['research_confidence']} | {tech} | [Bild]({r['candidate_url']}) |")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(payload["counts"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
