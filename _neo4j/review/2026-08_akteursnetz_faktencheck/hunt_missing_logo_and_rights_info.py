#!/usr/bin/env python3
"""Research-only crawl for missing logo and permission information.

The script never changes review decisions, assets, rendering, opacity, Neo4j,
or publication clearance.  Every discovered image remains an unreviewed lead.
"""

from __future__ import annotations

import concurrent.futures
import csv
import html
import json
import re
import ssl
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "bilder_full"
IDENTITY = DATA / "CURRENT_LOGO_IDENTITY_AUDIT.json"
RIGHTS = DATA / "CURRENT_IMAGE_RIGHTS_AUDIT.json"
OUT_ALL = DATA / "MISSING_RIGHTS_INFO_HUNT.json"
OUT_RIGHTS_CSV = DATA / "MISSING_RIGHTS_INFO_HUNT.csv"
OUT_NONE = DATA / "MISSING_LOGO_INFO_HUNT.json"
OUT_NONE_CSV = DATA / "MISSING_LOGO_INFO_HUNT.csv"
OUT_REPORT = DATA / "MISSING_INFO_HUNT_REPORT.md"

USER_AGENT = "Mozilla/5.0 (compatible; AkteursnetzResearch/1.0; read-only)"
MAX_BYTES = 1_500_000
TIMEOUT = 6

CONTACT_WORDS = (
    "contact", "kontakt", "contactez", "contatti", "contacto", "yhteys",
    "nous-contacter", "ansprechpartner", "team", "about", "ueber-uns", "over-ons",
)
LEGAL_WORDS = (
    "impressum", "legal", "mentions-legales", "mentions_légales", "copyright",
    "terms", "conditions", "voorwaarden", "privacy", "datenschutz", "cookies",
)
BRAND_WORDS = (
    "brand", "branding", "logo", "press", "presse", "media", "medien", "newsroom",
    "design-guide", "designmanual", "grafisk-profil", "visuel-identitet", "downloads",
)
IMAGE_WORDS = ("logo", "brand", "wordmark", "logotype", "identite", "identity")
POLICY_RE = re.compile(
    r".{0,180}(?:logo|logotype|trademark|trade mark|marque|marke|brand|copyright|"
    r"urheberrecht|licen[cs]e|nutzungsrecht|bildrecht).{0,280}", re.I | re.S
)
EMAIL_RE = re.compile(r"[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}", re.I)


# Manual domain findings for the 12 current rows without an accepted domain.
# Evidence can be a registry or project page, but only an exact first-party site
# is marked as an official-domain lead.
MANUAL_DOMAIN_FINDINGS = {
    "FR:U12": {
        "domain_lead": "",
        "status": "no_exact_first_party_domain_found",
        "evidence_url": "https://www.fapil.fr/adherents-ile-de-france/name/rehabail",
        "note": "Réhabail is documented as the carrier of Ferme du Rail, but no exact first-party brand/domain was found.",
        "recommended_outcome": "none_unless_parent_brand_is_manually_approved",
    },
    "FR:M09": {
        "domain_lead": "https://brocantique.pro/",
        "status": "ambiguous_same_name_business",
        "evidence_url": "https://brocantique.pro/",
        "note": "A same-name antiques site exists, but the graph identity cannot yet be tied to it exactly.",
        "recommended_outcome": "none_pending_exact_identity_match",
    },
    "GB:X02": {
        "domain_lead": "",
        "status": "not_an_organisation",
        "evidence_url": "",
        "note": "Students, schoolchildren and volunteers are a participant group, not a stable organisation/brand.",
        "recommended_outcome": "none",
    },
    "CH:U15": {
        "domain_lead": "http://www.modissa.ch/",
        "status": "registry_domain_lead_not_first_party_verified",
        "evidence_url": "https://ch.kompass.com/c/modissa-immobilien-ag/ch750511/",
        "note": "Business listing names modissa.ch; the current first-party site and exact property-company brand still need confirmation.",
        "recommended_outcome": "none_pending_first_party_verification",
    },
    "CH:U18": {
        "domain_lead": "",
        "status": "no_exact_first_party_domain_found",
        "evidence_url": "https://www.archdaily.com/professional/oberli-ingenieurbau-ag",
        "note": "Oberli Ingenieurbau AG is documented in project sources, but no current exact first-party website was found.",
        "recommended_outcome": "none",
    },
    "CH:U01": {
        "domain_lead": "",
        "status": "no_exact_first_party_domain_found",
        "evidence_url": "https://2025.prixbeton.ch/de/hochbau-projekte/1433/Erweiterung-Schreinerei-MZU-Uitikon-Zurich",
        "note": "AIK is documented as a project consultant, but no exact current first-party site was found.",
        "recommended_outcome": "none",
    },
    "DE:F03": {
        "domain_lead": "",
        "status": "person_historical_affiliation",
        "evidence_url": "https://d-nb.info/995034567/34",
        "note": "Claus Asam is a person historically affiliated with IEMB/TU/BBSR, not a standalone organisation brand.",
        "recommended_outcome": "none",
    },
    "DE:U41": {
        "domain_lead": "https://www.annahopp.com/",
        "status": "historical_office_successor_not_exact",
        "evidence_url": "https://www.annahopp.com/info",
        "note": "Wiewiorra Hopp is documented as a historical office; Anna Hopp's current practice is not an exact identity replacement.",
        "recommended_outcome": "none_unless_historical_logo_is_officially_sourced",
    },
    "DE:U32": {
        "domain_lead": "https://www.jablonicka.com/",
        "status": "exact_personal_site_but_person",
        "evidence_url": "https://www.jablonicka.com/impressum",
        "note": "Exact personal portfolio found; the row is a person, so the no-monogram/person rule still yields none.",
        "recommended_outcome": "none",
    },
    "DE:U27": {
        "domain_lead": "",
        "status": "ambiguous_common_business_name",
        "evidence_url": "",
        "note": "No domain could be tied uniquely to the intended Ingenieurbüro Fechner.",
        "recommended_outcome": "none_pending_exact_identity_match",
    },
    "DK:M02": {
        "domain_lead": "https://www.xn--byggebrsen-5cb.dk/",
        "status": "exact_current_first_party_domain_found",
        "evidence_url": "https://www.xn--byggebrsen-5cb.dk/",
        "note": "Current first-party Byggebørsen marketplace found.",
        "recommended_outcome": "research_logo_on_official_site",
    },
    "NO:N06": {
        "domain_lead": "",
        "status": "project_network_not_standalone_brand",
        "evidence_url": "https://ncce.no/en/kategori/avfallsrett/",
        "note": "Regionalt ombruksnettverk is documented as a project/network, not a stable standalone organisation brand.",
        "recommended_outcome": "none_unless_project_owner_brand_is_manually_approved",
    },
}


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.links = []
        self.images = []
        self.metas = []
        self._href = None
        self._anchor_text = []
        self.text = []

    def handle_starttag(self, tag, attrs):
        a = {k.lower(): (v or "") for k, v in attrs}
        if tag == "a":
            self._href = a.get("href", "")
            self._anchor_text = []
        elif tag == "img":
            self.images.append(a)
        elif tag == "link":
            self.images.append(a)
        elif tag == "meta":
            self.metas.append(a)

    def handle_endtag(self, tag):
        if tag == "a" and self._href is not None:
            self.links.append((self._href, " ".join(self._anchor_text).strip()))
            self._href = None
            self._anchor_text = []

    def handle_data(self, data):
        clean = " ".join(data.split())
        if clean:
            self.text.append(clean)
            if self._href is not None:
                self._anchor_text.append(clean)


def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": "text/html,application/xhtml+xml"})
    ctx = ssl.create_default_context()
    with urllib.request.urlopen(req, timeout=TIMEOUT, context=ctx) as response:
        raw = response.read(MAX_BYTES)
        final_url = response.geturl()
        content_type = response.headers.get_content_type()
        charset = response.headers.get_content_charset() or "utf-8"
    if "html" not in content_type and not raw.lstrip().startswith(b"<"):
        raise ValueError(f"not HTML ({content_type})")
    try:
        text = raw.decode(charset, "replace")
    except LookupError:
        text = raw.decode("utf-8", "replace")
    parser = PageParser()
    parser.feed(text)
    return final_url, text, parser


def absolute(base, href):
    if not href or href.startswith(("javascript:", "tel:", "#")):
        return ""
    return urllib.parse.urldefrag(urllib.parse.urljoin(base, html.unescape(href)))[0]


def site_host(url):
    return (urllib.parse.urlparse(url).hostname or "").lower().removeprefix("www.")


def is_internal(base, url):
    a, b = site_host(base), site_host(url)
    return bool(a and b and (a == b or a.endswith("." + b) or b.endswith("." + a)))


def page_leads(base, parser):
    buckets = {"contact": [], "legal": [], "brand_media": []}
    for href, label in parser.links:
        url = absolute(base, href)
        if not url or not is_internal(base, url):
            continue
        hay = (url + " " + label).lower()
        for bucket, words in (("contact", CONTACT_WORDS), ("legal", LEGAL_WORDS), ("brand_media", BRAND_WORDS)):
            score = sum(1 for word in words if word in hay)
            if score:
                buckets[bucket].append((score, url))
    return {k: [u for _, u in sorted(set(v), key=lambda x: (-x[0], len(x[1])))[:2]] for k, v in buckets.items()}


def emails_from(text, parser):
    found = set(EMAIL_RE.findall(text))
    for href, _ in parser.links:
        if href.lower().startswith("mailto:"):
            found.add(href.split(":", 1)[1].split("?", 1)[0])
    blocked = ("example.com", "sentry.io", "wixpress.com", "wordpress.org")
    return sorted(e for e in found if not any(x in e.lower() for x in blocked))


def candidate_images(base, parser):
    out = []
    for attrs in parser.images:
        rel = (attrs.get("rel") or "").lower()
        src = attrs.get("src") or attrs.get("href") or attrs.get("data-src") or ""
        descriptor = " ".join([src, attrs.get("alt", ""), attrs.get("class", ""), attrs.get("id", ""), rel]).lower()
        if not src or not (any(w in descriptor for w in IMAGE_WORDS) or "apple-touch-icon" in rel):
            continue
        url = absolute(base, src)
        if url and not any(x in url.lower() for x in ("facebook", "instagram", "linkedin", "youtube", "twitter", "x.com/")):
            kind = "declared_icon" if "icon" in rel else "logo_named_image"
            out.append({"url": url, "kind": kind, "basis": descriptor[:260]})
    for meta in parser.metas:
        prop = (meta.get("property") or meta.get("name") or "").lower()
        if prop in ("og:image", "twitter:image") and meta.get("content"):
            out.append({"url": absolute(base, meta["content"]), "kind": "og_image", "basis": prop})
    unique = []
    seen = set()
    for row in out:
        if row["url"] and row["url"] not in seen:
            seen.add(row["url"]); unique.append(row)
    return unique[:20]


def preferred_email(emails):
    ranks = ("brand", "press", "media", "kommunikation", "communication", "marketing", "legal", "info", "contact", "kontakt")
    return sorted(emails, key=lambda e: (next((i for i, word in enumerate(ranks) if word in e.lower()), 99), e))[0] if emails else ""


def crawl(row, need_logo):
    official = row.get("official_url") or ""
    result = {
        "key": row["key"], "cc": row["cc"], "tid": row["tid"], "name": row["name"],
        "result": row["result"], "official_url": official, "access_status": "not_attempted",
        "final_url": "", "contact_pages": [], "legal_pages": [], "brand_media_pages": [],
        "emails": [], "preferred_permission_email": "", "policy_snippets": [],
        "logo_leads": [], "research_status": "no_official_domain",
        "publication_clearance": "blocked_no_permission_requested" if row["result"] == "logo" else "not_applicable_no_logo",
    }
    manual = MANUAL_DOMAIN_FINDINGS.get(row["key"])
    if not official and manual:
        result["manual_domain_finding"] = manual
        official = manual.get("domain_lead") or ""
        result["official_url"] = official
    if not official:
        return result
    try:
        final_url, root_text, root_parser = fetch(official)
        result["access_status"] = "ok"
        result["final_url"] = final_url
        leads = page_leads(final_url, root_parser)
        result["contact_pages"] = leads["contact"]
        result["legal_pages"] = leads["legal"]
        result["brand_media_pages"] = leads["brand_media"]
        emails = set(emails_from(root_text, root_parser))
        snippets = [" ".join(m.group(0).split())[:500] for m in POLICY_RE.finditer(" ".join(root_parser.text))][:4]
        logo_leads = candidate_images(final_url, root_parser) if need_logo else []
        # Relevant secondary pages are recorded as leads but deliberately not
        # bulk-fetched.  Several legacy sites keep sockets open indefinitely;
        # each promising media/legal page must be checked manually anyway.
        result["emails"] = sorted(emails)
        result["preferred_permission_email"] = preferred_email(result["emails"])
        result["policy_snippets"] = list(dict.fromkeys(snippets))[:8]
        seen = set(); clean_leads = []
        for lead in logo_leads:
            if lead["url"] not in seen:
                seen.add(lead["url"]); clean_leads.append(lead)
        result["logo_leads"] = clean_leads[:20]
        if result["policy_snippets"]:
            result["research_status"] = "explicit_rights_or_brand_text_found_manual_legal_review_required"
        elif result["preferred_permission_email"] or result["contact_pages"]:
            result["research_status"] = "contact_route_found_permission_not_requested"
        else:
            result["research_status"] = "official_site_found_no_permission_route"
    except Exception as exc:
        result["access_status"] = f"error:{type(exc).__name__}:{str(exc)[:180]}"
        result["research_status"] = "official_site_unreachable_manual_research_required"
    if manual:
        result["manual_domain_finding"] = manual
    return result


def main():
    identity = json.loads(IDENTITY.read_text(encoding="utf-8"))
    rights = json.loads(RIGHTS.read_text(encoding="utf-8"))
    rights_by_key = {r["key"]: r for r in rights["nodes"]}
    nodes = identity["nodes"]
    with concurrent.futures.ThreadPoolExecutor(max_workers=40) as pool:
        futures = {pool.submit(crawl, row, row["result"] == "none"): row["key"] for row in nodes}
        rows = []
        for pos, future in enumerate(concurrent.futures.as_completed(futures), 1):
            row = future.result()
            old = rights_by_key.get(row["key"], {})
            row["prior_rights_status"] = old.get("rights_status", "")
            row["prior_print_clearance"] = old.get("print_clearance", "")
            rows.append(row)
            if pos % 50 == 0:
                print(f"[{pos}/{len(nodes)}] researched", flush=True)
    rows.sort(key=lambda r: (r["cc"], r["key"]))
    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    counts = Counter(r["research_status"] for r in rows)
    payload = {
        "schema_version": "missing-rights-info-hunt-v1", "created_at": now,
        "scope": {"organisations": len(rows), "existing_logos": 476, "none": 65},
        "boundary": "Research only. No permission request sent; no publication clearance changed; no asset/render/Neo4j mutation.",
        "counts": dict(counts), "nodes": rows,
    }
    OUT_ALL.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fields = ["key", "cc", "tid", "name", "result", "official_url", "access_status", "research_status", "preferred_permission_email", "contact_pages", "legal_pages", "brand_media_pages", "policy_snippets", "prior_rights_status", "prior_print_clearance", "publication_clearance"]
    with OUT_RIGHTS_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields); w.writeheader()
        for row in rows:
            flat = {k: row.get(k, "") for k in fields}
            for k in ("contact_pages", "legal_pages", "brand_media_pages", "policy_snippets"):
                flat[k] = " | ".join(row[k])
            w.writerow(flat)
    none_rows = [r for r in rows if r["result"] == "none"]
    none_payload = {
        "schema_version": "missing-logo-info-hunt-v1", "created_at": now,
        "boundary": "Every image URL is an unreviewed research lead, not an accepted logo.",
        "counts": {
            "none_total": len(none_rows),
            "with_logo_leads": sum(bool(r["logo_leads"]) for r in none_rows),
            "without_logo_leads": sum(not r["logo_leads"] for r in none_rows),
            "manual_domain_findings": sum("manual_domain_finding" in r for r in none_rows),
        },
        "nodes": none_rows,
    }
    OUT_NONE.write_text(json.dumps(none_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    none_fields = ["key", "cc", "tid", "name", "official_url", "access_status", "research_status", "logo_lead_count", "logo_leads", "brand_media_pages", "contact_pages", "preferred_permission_email", "domain_finding_status", "domain_finding_note", "recommended_outcome"]
    with OUT_NONE_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=none_fields); w.writeheader()
        for row in none_rows:
            manual = row.get("manual_domain_finding", {})
            w.writerow({
                "key": row["key"], "cc": row["cc"], "tid": row["tid"], "name": row["name"],
                "official_url": row["official_url"], "access_status": row["access_status"], "research_status": row["research_status"],
                "logo_lead_count": len(row["logo_leads"]), "logo_leads": " | ".join(x["url"] for x in row["logo_leads"]),
                "brand_media_pages": " | ".join(row["brand_media_pages"]), "contact_pages": " | ".join(row["contact_pages"]),
                "preferred_permission_email": row["preferred_permission_email"], "domain_finding_status": manual.get("status", ""),
                "domain_finding_note": manual.get("note", ""), "recommended_outcome": manual.get("recommended_outcome", "manual_candidate_review" if row["logo_leads"] else "none_no_lead"),
            })
    report = f"""# Recherche der fehlenden Logo- und Rechteinformationen

Erzeugt: {now}

## Feste Grenze

- Nur Informationsrecherche; keine Änderung an Stil, Deckkraft, Assets, Reviews, Rendering oder Neo4j.
- Keine Erlaubnisanfrage versendet und keine Publikationsfreigabe behauptet.
- Alle gefundenen Bild-URLs sind unbestätigte Recherchehinweise und müssen einzeln auf Identität, Mindestauflösung und Rechte geprüft werden.

## Umfang

- Organisationen geprüft: **{len(rows)}**
- Bereits ausgewählte Logos: **476**
- Aktuelle `none`-Organisationen: **{len(none_rows)}**
- `none` mit mindestens einem technischen Bildhinweis: **{none_payload['counts']['with_logo_leads']}**
- `none` ohne Bildhinweis: **{none_payload['counts']['without_logo_leads']}**
- Manuell recherchierte zuvor fehlende Domainfälle: **{none_payload['counts']['manual_domain_findings']}**

## Rechte

Gefundene Kontakt-, Presse-, Marken- und Rechteseiten erleichtern die spätere Rechteklärung, ändern aber keinen Status. Bis eine ausdrückliche Erlaubnis oder belastbare Lizenz dokumentiert ist, bleibt jedes bisher blockierte Logo blockiert.

## Dateien

- `MISSING_LOGO_INFO_HUNT.csv` — 65 `none`-Fälle, neue Domain- und Bildhinweise
- `MISSING_LOGO_INFO_HUNT.json` — vollständige maschinenlesbare Logo-Recherche
- `MISSING_RIGHTS_INFO_HUNT.csv` — Kontakt-/Rechtewege aller 541 Organisationen
- `MISSING_RIGHTS_INFO_HUNT.json` — vollständige maschinenlesbare Rechte-Recherche
"""
    OUT_REPORT.write_text(report, encoding="utf-8")
    print(json.dumps({"rights_counts": dict(counts), "none_counts": none_payload["counts"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
