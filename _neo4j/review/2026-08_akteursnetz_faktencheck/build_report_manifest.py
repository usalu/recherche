"""Rendermanifest fuer den Bericht aus dem aktuellen Identitaetsaudit.

Warum es das braucht: der Bericht zeichnet das AKTUELLE 619-Knoten-Netz,
`final_image_manifest.json` beschreibt dagegen die eingefrorene 762er
Transportauswahl. Beides deckt sich fast, aber nicht ganz -- Knoten, die es
im aktuellen Netz gibt und in der Auswahl nicht, liegen nur unter
`current_only_final/` und fehlten deshalb im Bericht, obwohl ihr Logo geprueft
und freigegeben ist (Toulouse Metropole und AD VITAM MATERIAL, beide im Netz
gezeichnet, beide ohne Bild gerendert).

`CURRENT_LOGO_IDENTITY_AUDIT.json` ist die Instanz, die genau die Menge
beschreibt, die der Bericht zeichnet: 541 Organisationen des aktuellen Netzes.
Diese Datei giesst sie in das Schema, das netz.render.latex.graph_tikz
erwartet -- unveraenderte Pfade und Pruefsummen, nur `review_status` von
`accepted_provisional` auf `accepted` normalisiert, weil `manifest_rows()`
darauf filtert.

Der Reviewstand bleibt dabei ausdruecklich vorlaeufig; `accepted` ist hier die
technische Freigabe fuer den Satz, keine Rechtefreigabe. Aufrufen nach jedem
`current-finalize`, dann `netz.cli sync-images/abb/tables-grid` mit
`--images-manifest` auf die erzeugte Datei zeigen lassen.
"""
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
FULL = BASE / "bilder_full"
AUDIT = FULL / "CURRENT_LOGO_IDENTITY_AUDIT.json"
OUT = FULL / "report_image_manifest.json"

audit = json.loads(AUDIT.read_text(encoding="utf-8"))
rows, missing = [], []
for row in audit["nodes"]:
    if row.get("result") != "logo":
        continue
    asset = row.get("asset_path")
    if not asset or not (FULL / asset).is_file():
        missing.append(row.get("key"))
        continue
    rows.append({
        "key": row["key"], "cc": row["cc"], "tid": row["tid"], "eid": row["eid"],
        "name": row.get("name"), "result": "logo",
        # manifest_rows() filtert auf genau diesen Wert; die inhaltliche
        # Vorlaeufigkeit steht unveraendert in review_status_source.
        "review_status": "accepted",
        "review_status_source": row.get("review_status"),
        "asset_path": asset, "dark_asset_path": row.get("dark_asset_path"),
        "sha256": row.get("asset_sha256"), "dark_sha256": row.get("dark_asset_sha256"),
        "crop_mode": row.get("crop_mode"),
        "source_url": row.get("source_url"), "source_kind": row.get("source_kind"),
        "license_note": row.get("license_note", ""),
        "logo_opacity_percent": row.get("logo_opacity_percent"),
        "identity_review_status": row.get("identity_review_status"),
    })

if missing:
    raise SystemExit("Asset fehlt fuer: " + ", ".join(missing[:10]))

collisions = {}
for row in rows:
    collisions.setdefault((row["cc"], row["tid"]), []).append(row["key"])
clashing = {k: v for k, v in collisions.items() if len(v) > 1}
if clashing:
    # cc/tid ist der Dateiname im Bericht; zwei Knoten darauf waeren ein
    # stiller Ueberschreibfehler, kein Schoenheitsfehler.
    raise SystemExit(f"cc/tid-Kollision: {clashing}")

OUT.write_text(json.dumps({
    "schema_version": 1, "transport_only": True,
    "scope": "aktuelles 619-Knoten-Netz, 541 Organisationen",
    "derived_from": AUDIT.name, "created_at": audit.get("created_at"),
    "nodes": rows,
}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(f"{OUT.name}: {len(rows)} Logos "
      f"({sum(1 for r in rows if r['asset_path'].startswith('current_only_final'))} davon nur im aktuellen Netz)")
