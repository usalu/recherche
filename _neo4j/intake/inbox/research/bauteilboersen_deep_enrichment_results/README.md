# Bauteilbörsen deep enrichment results

Generated: 2026-05-31

Contents:
- `INDEX.json` — run metadata and per-anchor counts
- `<anchor_id>.enrichment.json` — one enrichment JSON per anchor, 39 total
- `NEW_VOCAB_PROPOSALS.md` — vocabulary proposals only when a closed-set target did not fit
- `REVIEW_QUEUE.json` — anchors requiring human/graph review before import
- `SUMMARY.csv` — compact count summary

Important constraints followed:
- Country, Akteurtyp, Akteurrolle and base URLs were not re-created.
- Closed-set Material and Bauteiltyp IDs were used exactly where applicable.
- PruefungNachweis, Aufbereitungsverfahren and Rueckbauverfahren IDs were not invented because the live graph was unavailable in this environment. Each such claim carries `target_id: null`, `lookup_keyword`, and `requires_cypher_lookup: true`.
- `http_status: 200` means the URL was successfully opened/read via the browser tool or supplied as a visited secondary source in this pass; product/listing pages still require import-time validation.

Coverage summary:
- Anchors processed: 39
- Core Material claims: 81
- Core Bauteiltyp claims: 130
- Pruefung lookup candidates: 19
- Aufbereitung lookup candidates: 8
- Rueckbau lookup candidates: 5
