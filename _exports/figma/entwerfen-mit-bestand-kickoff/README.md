# PNG export — Entwerfen mit Bestand slides

**Folder:** `E:\recherche\_exports\figma\entwerfen-mit-bestand-kickoff\`

Target files:

- `slide-08-bauteilerfassung-eingabe-vs-import.png`
- `slide-09-bauteilkatalog-datenstruktur.png`
- `slide-10-backup-pre-redesign.png`
- `slide-11-typology-view.png`
- `slide-12-filter-sidebar-spec.png`
- `slide-13-typology-view-working-copy.png`

---

## Fastest: one-click Figma plugin (no MCP bridge)

1. Open **Entwerfen mit Bestand** in **Figma Desktop**.
2. **Plugins → Development → Import plugin from manifest…**
3. Select:
   `E:\recherche\_exports\figma\entwerfen-mit-bestand-kickoff\figma-plugin-export-pngs\manifest.json`
4. **Plugins → Development → Export Kickoff Slides PNG**
5. Allow **6 PNG downloads** in the browser/Figma save dialog.
6. Move/copy the PNGs into this folder (`entwerfen-mit-bestand-kickoff\`).

---

## Automated: Cursor MCP bridge

1. Open **Entwerfen mit Bestand** in Figma Desktop.
2. **Plugins → Development → Figma Desktop Bridge** (leave it open).
3. Ask Cursor to run:

```bash
python _exports/figma/entwerfen-mit-bestand-kickoff/export_pngs_mcp.py
```

Uses the **existing** Cursor `figma-console` MCP on port **9223** (do not spawn a second MCP server).

---

## Iframe embed

```html
<img src="_exports/figma/entwerfen-mit-bestand-kickoff/slide-12-filter-sidebar-spec.png" alt="Slide 12" style="width:100%;height:auto">
```

Or wrap in HTML:

```html
<iframe src="slide-12-filter-sidebar-spec.html" width="100%" height="720" style="border:0"></iframe>
```

(`slide-*.html` files reference the matching `.png`.)
