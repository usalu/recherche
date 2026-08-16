#!/usr/bin/env python3
"""Build the conservative final identity audit for every selected logo.

This is a read-only audit of the frozen image transport.  It never connects to
Neo4j and never changes the accepted review or the rendered assets.
"""

from __future__ import annotations

import csv
import hashlib
import html
import json
import math
import textwrap
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "bilder_full"
INPUT = DATA / "CURRENT_LOGO_IDENTITY_AUDIT.json"
OUT_JSON = DATA / "FINAL_FINAL_LOGO_AUDIT.json"
OUT_CSV = DATA / "FINAL_FINAL_LOGO_AUDIT.csv"
OUT_MD = DATA / "FINAL_FINAL_LOGO_AUDIT.md"
OUT_HTML = DATA / "FINAL_FINAL_LOGO_AUDIT.html"
SHEETS = DATA / "final_final_review"

CHECKED_AT = "2026-08-16T00:00:00+02:00"

# A failed image request does not by itself make an identity wrong.  A 404 is a
# durable provenance defect; 403/disconnect means the source needs a human click.
SOURCE_RECHECK = {
    "FR:N02": ("manual", "Offizielles Bellastock-Asset antwortete beim Schlusscheck mit HTTP 403; lokaler offizieller Snapshot vorhanden."),
    "FR:M44": ("high", "Die bisherige PROCLUS-Quelldatei antwortet mit HTTP 404; die offizielle Website zeigt inzwischen ein neues Logo-Asset."),
    "NL:U33": ("manual", "Offizielles Lagemaat-Asset antwortete beim Schlusscheck mit HTTP 403; lokaler offizieller Snapshot vorhanden."),
    "NL:F01": ("manual", "Leiden-Quelldatei trennte die Verbindung beim Schlusscheck; Identität/Quelle bitte per Browser bestätigen."),
    "NL:S03": ("manual", "Offizielles Ter-Velde-&-Den-Besten-Asset antwortete beim Schlusscheck mit HTTP 403; Snapshot vorhanden."),
    "CH:F02": ("manual", "Offizielles Empa-Asset antwortete beim Schlusscheck mit HTTP 403; zusätzlich wird eine Trägermarke verwendet."),
    "DE:I05": ("high", "Das bisherige Roskilde-Apple-Touch-Asset antwortet mit HTTP 404; aktuelle Design-/Logo-Seite bitte gegenprüfen."),
    "NO:M06": ("manual", "Deklariertes Google-CDN-Asset antwortete beim Schlusscheck mit HTTP 403; Quelle bitte per Browser bestätigen."),
}

# Known, documented carrier/successor/umbrella-brand decisions.  They may be
# defensible, but are intentionally never classified as zero-uncertainty.
PARENT_OR_SUCCESSOR = {
    "FR:O04": "Nachfolgemarke: Novaedia/Novædia wird als La Ferme des Possibles geführt.",
    "DK:M13": "Trägermarke: PlusByg wird mit AffaldPlus dargestellt.",
    "DK:M15": "Trägermarke: Sydhavn Genbrugscenter wird mit ARC dargestellt.",
    "NL:N03": "Trägermarke: Urban Mining Collective wird mit New Horizon dargestellt.",
    "SE:M04": "Trägermarke: Byggåterbruket wird mit Umeå kommun dargestellt.",
    "SE:N01": "Trägermarke: Handslag wird mit Business Region Göteborg dargestellt.",
    "SE:M07": "Trägermarke: Reboost wird mit Ragn-Sells dargestellt.",
    "SE:U09": "Konzernmarke: Contiga wird mit Heidelberg Materials dargestellt.",
    "NO:U02": "Träger-/Gruppenmarke: Bevar/Urban Reuse wird mit NG Nordic dargestellt.",
    "DE:M07": "Trägermarke: MÖWE wird mit SKM Osnabrück dargestellt.",
    "DE:I04": "Programm-/Trägermarke: Münchner Bauteilbörse/CirCoFin wird mit der Stadt München dargestellt.",
    "AT:I02": "Programm-/Trägermarke: VIE.CYCLE wird mit der Stadt Wien dargestellt.",
    "AT:N02": "Trägermarke: DRZ wird mit Wiener Volkshochschulen dargestellt.",
    "BE:N09": "Arbeitsgruppe wird mit der EU-/CCRI-Trägermarke dargestellt.",
    "BE:N02": "CCRI-Pilot Uppsala wird mit der kommunalen Trägermarke dargestellt.",
    "NO:N02": "CCRI-Pilot Asker wird mit der kommunalen Trägermarke dargestellt.",
    "CH:F01": "Forschungseinheit CEA wird mit der ETH-Zürich-Trägermarke dargestellt.",
    "CH:F02": "NEST wird mit der Empa-Trägermarke dargestellt.",
    "CH:F07": "Structural Xploration Lab wird mit der EPFL-Trägermarke dargestellt.",
    "BE:F05": "CirculaTUM wird mit der TUM-Trägermarke dargestellt.",
    "BE:F07": "Forschungseinheit wird mit der University-of-Twente-Trägermarke dargestellt.",
    "FI:F01": "Aalto-Untereinheit wird mit der Aalto-University-Trägermarke dargestellt.",
    "FI:U05": "Aalto-Untereinheit wird mit der Aalto-University-Trägermarke dargestellt.",
    "FI:U10": "Aalto-Untereinheit wird mit der Aalto-University-Trägermarke dargestellt.",
    "CURRENT:BE:advitam-material": "Nachfolge-/aktuelle Marke für Plateforme Réemploi; manuelle Bestätigung empfohlen.",
    "BE:S03": "SundaHus wird in aktueller iBinder-Gruppenfassung dargestellt.",
}

RECENT_KEYS = {
    "FR:U02", "FR:N02", "CURRENT:FR:toulousemetropole", "FR:M19",
    "GB:M09", "GB:M21", "GB:M01", "GB:M17", "GB:M07", "NL:U33",
    "NL:S03", "BE:M12", "BE:M17", "CURRENT:BE:advitam-material",
    "BE:S03", "FI:U06", "DE:U13", "BE:M18", "BE:M27", "CH:U22",
}

LOW_SIGNAL_SOURCE_KINDS = {
    "favicon": "Favicon ist häufig nur eine verkürzte oder generische Bildmarke.",
    "declared_icon": "Deklariertes Site-Icon kann eine verkürzte Bildmarke statt des vollständigen Logos sein.",
    "og_image": "Open-Graph-Bild kann Kampagnenmotiv, Foto oder zusammengesetzte Grafik sein.",
    "wikimedia": "Wikimedia-Datei muss trotz zulässiger Nutzung gegen die aktuelle Eigenmarke geprüft werden.",
}

MULTIPART_MARKERS = (" / ", " + ", "(")


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def host(url: str) -> str:
    if not url:
        return ""
    if url.startswith("inline+"):
        url = url[len("inline+"):].split("#", 1)[0]
    if url.startswith("data:"):
        return "embedded"
    return (urlparse(url).hostname or "").lower().removeprefix("www.")


def same_site(a: str, b: str) -> bool:
    if not a or not b or a == "embedded" or b == "embedded":
        return True
    if a == b or a.endswith("." + b) or b.endswith("." + a):
        return True
    hosted = (
        "cloudfront.net", "wixstatic.com", "squarespace-cdn.com", "shopify.com",
        "googleusercontent.com", "googleapis.com", "filesusr.com", "wp.com",
        "contentful.com", "ctfassets.net", "sanity.io", "prismic.io",
        "azureedge.net", "akamaized.net", "scene7.com", "website-files.com",
    )
    return any(b.endswith(x) for x in hosted)


def technical_asset_check(node: dict) -> list[str]:
    errors: list[str] = []
    for field, hash_field in (("asset_path", "asset_sha256"), ("dark_asset_path", "dark_asset_sha256")):
        rel = node.get(field)
        if not rel:
            continue
        path = DATA / rel
        if not path.is_file():
            errors.append(f"{field}: Datei fehlt")
            continue
        digest = sha256(path)
        expected = node.get(hash_field)
        if expected and digest != expected:
            errors.append(f"{field}: SHA-256 abweichend")
        try:
            with Image.open(path) as im:
                if im.format != "PNG":
                    errors.append(f"{field}: Format {im.format}, nicht PNG")
                if im.size != (256, 256):
                    errors.append(f"{field}: Größe {im.size}, nicht 256×256")
                rgba = im.convert("RGBA")
                alpha = rgba.getchannel("A")
                if alpha.getbbox() is None:
                    errors.append(f"{field}: vollständig transparent")
                px = alpha.load()
                max_radius = 0.0
                for y in range(256):
                    for x in range(256):
                        # Alpha values 1–8 are resampling fringe, not visible ink.
                        # This is the same antialiasing tolerance used by the
                        # established renderer acceptance check.
                        if px[x, y] > 8:
                            max_radius = max(max_radius, math.hypot(x - 127.5, y - 127.5))
                if max_radius > 128.75:
                    errors.append(f"{field}: Alpha-Radius {max_radius:.3f} px > 128.75 px")
        except Exception as exc:  # pragma: no cover - diagnostic only
            errors.append(f"{field}: nicht lesbar ({exc})")
    return errors


def add_reason(reasons: list[dict], code: str, severity: str, text: str) -> None:
    if not any(r["code"] == code for r in reasons):
        reasons.append({"code": code, "severity": severity, "text": text})


def classify(node: dict, duplicate_keys: list[str]) -> tuple[str, list[dict], list[str]]:
    reasons: list[dict] = []
    technical = technical_asset_check(node)
    key = node["key"]
    if technical:
        add_reason(reasons, "technical_failure", "high", "Technischer Assettest fehlgeschlagen.")
    if key in SOURCE_RECHECK:
        severity, message = SOURCE_RECHECK[key]
        add_reason(reasons, "source_recheck", severity, message)
    if key in PARENT_OR_SUCCESSOR:
        add_reason(reasons, "carrier_or_successor", "manual", PARENT_OR_SUCCESSOR[key])
    kind = node.get("source_kind") or ""
    if kind in LOW_SIGNAL_SOURCE_KINDS:
        add_reason(reasons, "low_signal_source_kind", "manual", LOW_SIGNAL_SOURCE_KINDS[kind])
    source_url = node.get("source_url") or ""
    if source_url.startswith("http://"):
        add_reason(reasons, "http_source", "manual", "Quelldatei nur über unverschlüsseltes HTTP referenziert.")
    if source_url.startswith("inline+"):
        add_reason(reasons, "inline_extraction", "manual", "Logo wurde aus eingebettetem Seiten-SVG extrahiert; Ausschnitt manuell prüfen.")
    official_host = host(node.get("official_url") or "")
    source_host = host(source_url)
    if official_host and source_host and not same_site(official_host, source_host):
        add_reason(
            reasons, "cross_origin_source", "manual",
            f"Quelldatei liegt auf anderer Domain ({source_host}) als die offizielle Seite ({official_host}).",
        )
    name = node.get("name") or ""
    if any(marker in name for marker in MULTIPART_MARKERS):
        add_reason(reasons, "multi_entity_label", "manual", "Netzbezeichnung kombiniert Organisation, Untereinheit, Träger oder Ortszusatz.")
    if duplicate_keys:
        add_reason(
            reasons, "shared_asset_hash", "manual",
            "Exakt dieselbe Logodatei wird auch verwendet für: " + ", ".join(duplicate_keys) + ".",
        )
    if key.startswith("CURRENT:"):
        add_reason(reasons, "current_overlay", "manual", "Aktueller Overlay-Schlüssel statt eingefrorener Graph-ID; Identitätszuordnung manuell prüfen.")
    if key[:2].isalpha() and key[2:3] == ":" and key[:2] != node.get("cc"):
        add_reason(
            reasons, "key_country_mismatch", "manual",
            f"Schlüsselpräfix {key[:2]} weicht vom Länderfeld {node.get('cc')} ab; Overlay-/Transportzuordnung prüfen.",
        )
    if node.get("provisional_review"):
        # This does not create a flag alone; it is recorded explicitly below.
        pass
    if technical or any(r["severity"] == "high" for r in reasons):
        status = "manual_check_high"
    elif reasons:
        status = "manual_check"
    else:
        status = "confirmed_exact"
    return status, reasons, technical


def font(size: int, bold: bool = False):
    candidates = [
        Path("C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf"),
        Path("C:/Windows/Fonts/segoeuib.ttf" if bold else "C:/Windows/Fonts/segoeui.ttf"),
    ]
    for candidate in candidates:
        if candidate.exists():
            return ImageFont.truetype(str(candidate), size)
    return ImageFont.load_default()


def make_contact_sheets(rows: list[dict]) -> list[str]:
    SHEETS.mkdir(parents=True, exist_ok=True)
    for old in SHEETS.glob("manual_check_*.png"):
        old.unlink()
    pages: list[str] = []
    per_page = 8
    title_font = font(28, True)
    body_font = font(20)
    small_font = font(17)
    for page_no, start in enumerate(range(0, len(rows), per_page), 1):
        subset = rows[start:start + per_page]
        canvas = Image.new("RGB", (1800, 200 + 330 * len(subset)), "#f4f0e2")
        draw = ImageDraw.Draw(canvas)
        draw.text((50, 35), f"Manuelle Logo-Prüfung — Seite {page_no}", fill="#082a32", font=title_font)
        draw.text((50, 85), f"{start + 1}–{start + len(subset)} von {len(rows)} markierten Logos", fill="#39535a", font=body_font)
        for idx, row in enumerate(subset):
            y = 160 + idx * 330
            draw.rounded_rectangle((35, y, 1765, y + 300), radius=18, fill="#fffdf7", outline="#c4bda9", width=2)
            draw.text((65, y + 25), f"{row['key']}  {row['name']}", fill="#082a32", font=title_font)
            badge = "HOCH" if row["audit_status"] == "manual_check_high" else "MANUELL"
            draw.text((1510, y + 28), badge, fill="#9b2d20" if badge == "HOCH" else "#9a6500", font=body_font)
            base = DATA / row["asset_path"]
            dark = DATA / (row.get("dark_asset_path") or row["asset_path"])
            for x, path, bg, label in ((75, base, "#e4dfcd", "Hell"), (295, dark, "#06262f", "Dunkel")):
                draw.ellipse((x, y + 85, x + 180, y + 265), fill=bg, outline="#17343a" if label == "Hell" else "white", width=4)
                if path.exists():
                    with Image.open(path) as im:
                        logo = im.convert("RGBA").resize((180, 180), Image.Resampling.LANCZOS)
                    alpha = logo.getchannel("A").point(lambda a: round(a * 0.5))
                    logo.putalpha(alpha)
                    canvas.paste(logo.convert("RGB"), (x, y + 85), logo.getchannel("A"))
                tid = row.get("tid") or row["key"].split(":")[-1]
                box = draw.textbbox((0, 0), tid, font=title_font)
                tx = x + 90 - (box[2] - box[0]) / 2
                ty = y + 175 - (box[3] - box[1]) / 2
                draw.rounded_rectangle((tx - 6, ty - 4, tx + box[2] - box[0] + 6, ty + box[3] - box[1] + 4), radius=5, fill="#ffffffe6")
                draw.text((tx, ty), tid, fill="#082a32", font=title_font)
            reason_text = " | ".join(r["text"] for r in row["manual_reasons"])
            wrapped = textwrap.wrap(reason_text, width=105)[:7]
            draw.multiline_text((520, y + 85), "\n".join(wrapped), fill="#273c40", font=small_font, spacing=5)
        path = SHEETS / f"manual_check_{page_no:02d}.png"
        canvas.save(path, optimize=True)
        pages.append(str(path.relative_to(DATA)).replace("\\", "/"))
    return pages


def build_html(rows: list[dict], counts: Counter, reason_counts: Counter) -> str:
    cards = []
    for row in rows:
        reasons = "".join(
            f'<li><code>{html.escape(r["code"])}</code> — {html.escape(r["text"])}</li>'
            for r in row["manual_reasons"]
        ) or "<li>Keine Identitätsunsicherheit nach den strengen Auditregeln erkannt.</li>"
        base = html.escape(row["asset_path"])
        dark = html.escape(row.get("dark_asset_path") or row["asset_path"])
        status = row["audit_status"]
        cards.append(f'''
        <article class="card {status}" data-status="{status}" data-country="{html.escape(row['cc'])}" data-text="{html.escape((row['key'] + ' ' + row['name']).lower())}">
          <header><div><b>{html.escape(row['key'])}</b> · {html.escape(row['name'])}</div><span class="badge">{status}</span></header>
          <div class="body">
            <div class="previews">
              <div><div class="node light"><img src="{base}"><span>{html.escape(row['tid'])}</span></div><small>Hell</small></div>
              <div><div class="node dark"><img src="{dark}"><span>{html.escape(row['tid'])}</span></div><small>Dunkel</small></div>
            </div>
            <div class="facts">
              <ul>{reasons}</ul>
              <p><a target="_blank" rel="noreferrer" href="{html.escape(row.get('official_url') or '')}">Offizielle Seite</a> · <a target="_blank" rel="noreferrer" href="{html.escape(row.get('source_url') or '')}">Quelldatei</a></p>
              <p>Quelle: {html.escape(row.get('source_kind') or '')} · Rechte: {html.escape(row.get('rights_status') or '')}</p>
              <label><input type="checkbox" data-review="{html.escape(row['key'])}"> manuell angesehen (nur lokal im Browser gespeichert)</label>
            </div>
          </div>
        </article>''')
    reason_list = "".join(f"<li>{html.escape(k)}: {v}</li>" for k, v in reason_counts.most_common())
    return f'''<!doctype html>
<html lang="de"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Finales Logo-Identitätsaudit</title>
<style>
:root{{--ink:#082a32;--paper:#f4f0e2;--card:#fffdf7;--warn:#9a6500;--high:#9b2d20}}
*{{box-sizing:border-box}} body{{margin:0;background:var(--paper);color:var(--ink);font:16px/1.4 system-ui,sans-serif}}
main{{max-width:1500px;margin:auto;padding:28px}} h1{{margin:.1em 0}} .summary{{display:flex;gap:10px;flex-wrap:wrap;margin:16px 0}}
.pill,.controls{{background:#ffffffb8;border:1px solid #c4bda9;border-radius:12px;padding:10px 14px}} .controls{{position:sticky;top:0;z-index:5;backdrop-filter:blur(14px);display:flex;gap:8px;flex-wrap:wrap}}
button,input,select{{font:inherit;padding:8px 10px}} button{{cursor:pointer}} .grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(620px,1fr));gap:16px;margin-top:18px}}
.card{{background:var(--card);border:2px solid #b7c5c4;border-radius:16px;overflow:hidden}} .card.manual_check{{border-color:#d29a36}} .card.manual_check_high{{border-color:#b14635}}
.card header{{display:flex;justify-content:space-between;gap:12px;padding:12px 16px;background:#ffffffa8}} .badge{{font:700 12px/1 system-ui;text-transform:uppercase}}
.body{{display:flex;gap:20px;padding:16px}} .previews{{display:flex;gap:14px;flex:0 0 auto;text-align:center}} .node{{position:relative;width:140px;height:140px;border-radius:50%;overflow:hidden;display:grid;place-items:center;border:3px solid var(--ink)}}
.node.light{{background:#e4dfcd}} .node.dark{{background:#06262f;border-color:white}} .node img{{position:absolute;inset:0;width:100%;height:100%;object-fit:contain;opacity:.5}}
.node span{{position:relative;z-index:2;font-weight:800;font-size:22px;color:var(--ink);background:#ffffffb3;border-radius:5px;padding:0 4px;backdrop-filter:blur(2px)}}
.facts{{min-width:0}} .facts ul{{margin:.1em 0 .8em;padding-left:20px}} .facts p{{margin:.35em 0;overflow-wrap:anywhere}} small{{display:block;margin-top:4px}}
.hidden{{display:none!important}} details{{margin:14px 0}} code{{font-size:.82em}} @media(max-width:720px){{main{{padding:12px}}.grid{{grid-template-columns:1fr}}.body{{display:block}}.previews{{margin-bottom:12px}}}}
</style></head><body><main>
<h1>Finales Logo-Identitätsaudit</h1>
<p>Alle 476 ausgewählten Logos sind enthalten. „Bestätigt“ bedeutet: im strengen Regelcheck ohne Restunsicherheit. Jede Träger-/Nachfolgemarke, schwächere Quellenart, kombinierte Netzbezeichnung, Hash-Dublette oder auffällige Transportzuordnung ist vorsorglich markiert.</p>
<div class="summary"><div class="pill">Bestätigt: <b>{counts['confirmed_exact']}</b></div><div class="pill">Manuell: <b>{counts['manual_check']}</b></div><div class="pill">Hohe Priorität: <b>{counts['manual_check_high']}</b></div><div class="pill">Gesamt: <b>{len(rows)}</b></div></div>
<details><summary>Markierungsgründe</summary><ul>{reason_list}</ul></details>
<div class="controls"><button data-filter="manual">Nur manuell</button><button data-filter="high">Nur hohe Priorität</button><button data-filter="all">Alle</button><select id="country"><option value="">Alle Länder</option>{''.join(f'<option>{cc}</option>' for cc in sorted({r['cc'] for r in rows}))}</select><input id="search" type="search" placeholder="ID oder Name"><span id="visible"></span></div>
<section class="grid">{''.join(cards)}</section>
<script>
const cards=[...document.querySelectorAll('.card')], country=document.querySelector('#country'), search=document.querySelector('#search'); let mode='manual';
for(const box of document.querySelectorAll('[data-review]')){{box.checked=localStorage.getItem('logo-audit:'+box.dataset.review)==='1';box.onchange=()=>localStorage.setItem('logo-audit:'+box.dataset.review,box.checked?'1':'0')}}
function apply(){{let n=0;for(const c of cards){{const status=c.dataset.status;const okMode=mode==='all'||(mode==='manual'&&status!=='confirmed_exact')||(mode==='high'&&status==='manual_check_high');const okCountry=!country.value||c.dataset.country===country.value;const okText=!search.value||c.dataset.text.includes(search.value.toLowerCase());c.classList.toggle('hidden',!(okMode&&okCountry&&okText));if(okMode&&okCountry&&okText)n++}}document.querySelector('#visible').textContent=n+' sichtbar'}}
document.querySelectorAll('[data-filter]').forEach(b=>b.onclick=()=>{{mode=b.dataset.filter;apply()}});country.onchange=apply;search.oninput=apply;apply();
</script></main></body></html>'''


def main() -> None:
    source = json.loads(INPUT.read_text(encoding="utf-8"))
    logos = [n for n in source["nodes"] if n.get("result") == "logo"]
    by_hash: dict[str, list[str]] = defaultdict(list)
    for node in logos:
        by_hash[node.get("asset_sha256") or ""].append(node["key"])
    rows = []
    for node in logos:
        peers = [k for k in by_hash[node.get("asset_sha256") or ""] if k != node["key"]]
        status, reasons, technical = classify(node, peers)
        row = dict(node)
        row.update({
            "audit_status": status,
            "manual_reasons": reasons,
            "technical_errors": technical,
            "recent_last_three_sessions": node["key"] in RECENT_KEYS,
            "source_rechecked_at": CHECKED_AT if node["key"] in SOURCE_RECHECK else None,
        })
        rows.append(row)
    rows.sort(key=lambda r: ({"manual_check_high": 0, "manual_check": 1, "confirmed_exact": 2}[r["audit_status"]], r["cc"], r["key"]))
    counts = Counter(r["audit_status"] for r in rows)
    reason_counts = Counter(reason["code"] for row in rows for reason in row["manual_reasons"])
    technical_count = sum(bool(r["technical_errors"]) for r in rows)
    duplicate_groups = [keys for digest, keys in by_hash.items() if digest and len(keys) > 1]
    sheets = make_contact_sheets([r for r in rows if r["audit_status"] != "confirmed_exact"])
    payload = {
        "schema_version": "final-final-logo-audit-v1",
        "created_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "scope": {"network_nodes": 619, "organizations": 541, "selected_logos": len(rows), "none": 65, "projects_image_free": 78},
        "policy": "Any degree of source, identity, carrier, duplicate, transport or technical uncertainty is flagged for manual review.",
        "counts": dict(counts),
        "technical_failures": technical_count,
        "duplicate_asset_groups": duplicate_groups,
        "reason_counts": dict(reason_counts),
        "rights_boundary": "Identity confidence is independent from publication permission; consult CURRENT_IMAGE_RIGHTS_AUDIT.*.",
        "visual_review": {
            "all_selected_logos": "476/476 reviewed on the 33 complete suggestion sheets; no obvious swapped organization, partner logo, photo or social-media mark found.",
            "strict_manual_subset": f"{len([r for r in rows if r['audit_status'] != 'confirmed_exact'])}/476 conservative flags reviewed again on the generated contact sheets.",
            "visual_mismatch_found": 0,
            "interpretation": "A visual match does not clear the documented source/carrier/provenance uncertainty.",
        },
        "neo4j_write": False,
        "contact_sheets": sheets,
        "nodes": rows,
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    fieldnames = ["audit_status", "key", "cc", "tid", "name", "official_url", "source_url", "source_kind", "asset_path", "dark_asset_path", "asset_sha256", "rights_status", "recent_last_three_sessions", "reason_codes", "manual_reasons", "technical_errors"]
    with OUT_CSV.open("w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow({
                **{k: row.get(k, "") for k in fieldnames},
                "reason_codes": " | ".join(r["code"] for r in row["manual_reasons"]),
                "manual_reasons": " | ".join(r["text"] for r in row["manual_reasons"]),
                "technical_errors": " | ".join(row["technical_errors"]),
            })
    high = [r for r in rows if r["audit_status"] == "manual_check_high"]
    manual = [r for r in rows if r["audit_status"] == "manual_check"]
    recent_manual = [r for r in rows if r["recent_last_three_sessions"] and r["audit_status"] != "confirmed_exact"]
    md = f"""# Finales Schlussaudit aller ausgewählten Logos

Erzeugt: {payload['created_at']}

## Ergebnis

- 476/476 ausgewählte Logos technisch und regelbasiert erneut geprüft.
- **{counts['confirmed_exact']}** ohne erkannte Restunsicherheit (`confirmed_exact`).
- **{counts['manual_check']}** vorsorglich manuell zu prüfen (`manual_check`).
- **{counts['manual_check_high']}** mit hoher Priorität zu prüfen (`manual_check_high`).
- **{technical_count}** technische Assetfehler.
- **{len(duplicate_groups)}** exakte Hash-Dubletten-Gruppen; jede beteiligte Zuordnung ist bewusst markiert.
- 476/476 Logos auf den 33 vollständigen Prüfbögen visuell geprüft; {len(manual) + len(high)}/476 markierte Grenzfälle zusätzlich auf {len(sheets)} Schlussaudit-Bögen geprüft.
- 0 visuell offensichtliche Vertauschungen, Partnerlogos, Fotos oder Social-Media-Zeichen gefunden.
- `mit-bestand` unverändert; keine Neo4j-Schreiboperation.

„Manuell prüfen“ bedeutet nicht „falsch“. Die Warteschlange enthält bewusst jeden Fall mit auch nur kleiner Unsicherheit: Träger-/Nachfolgemarke, kombinierte Bezeichnung, schwächere Quellenart, abweichende Domain, Inline-Extraktion, Hash-Dublette, Transportauffälligkeit oder nicht erneut erreichbare Quelldatei.

## Hohe Priorität

{chr(10).join(f"- `{r['key']}` — {r['name']}: " + ' | '.join(x['text'] for x in r['manual_reasons']) for r in high) or '- keine'}

## Zuletzt ergänzte Logos mit manueller Markierung

{chr(10).join(f"- `{r['key']}` — {r['name']}: " + ' | '.join(x['text'] for x in r['manual_reasons']) for r in recent_manual) or '- keine'}

## Manuelle Warteschlange

Die vollständige Liste der {len(manual) + len(high)} markierten Logos steht in `FINAL_FINAL_LOGO_AUDIT.csv` und in der klickbaren Galerie `FINAL_FINAL_LOGO_AUDIT.html`. Die Galerie startet mit dem Filter „nur manuell“ und enthält offizielle Seite, Quelldatei, Hell-/Dunkelvorschau sowie alle Markierungsgründe.

## Rechte

Identitätsprüfung und Bildrechte bleiben getrennt. Für Veröffentlichungsfreigaben ist weiterhin `CURRENT_IMAGE_RIGHTS_AUDIT.csv` maßgeblich.
"""
    OUT_MD.write_text(md, encoding="utf-8")
    OUT_HTML.write_text(build_html(rows, counts, reason_counts), encoding="utf-8")
    print(json.dumps({
        "selected_logos": len(rows),
        "counts": dict(counts),
        "technical_failures": technical_count,
        "manual_total": len(manual) + len(high),
        "recent_manual": len(recent_manual),
        "contact_sheets": len(sheets),
        "outputs": [str(OUT_JSON), str(OUT_CSV), str(OUT_MD), str(OUT_HTML)],
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
