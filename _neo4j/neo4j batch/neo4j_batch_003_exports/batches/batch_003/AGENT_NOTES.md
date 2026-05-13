# AGENT NOTES — batch_003

Purpose: repo-ready JSONL import chunks for Neo4j/MCP ingestion.

Import order:
1. `controlled_vocabulary.seed.kg.jsonl` from the contract root.
2. `batches/batch_003/controlled_terms.delta.jsonl`.
3. The five `p_*.kg.jsonl` project files in this batch.
4. Optional: run the validation report checks again after import.

Modeling choices:
- `Projekt` is the only central case node; no separate Fallbeispiel node is emitted.
- `bewertung` is the only reuse score scalar retained from the old case ranking fields.
- All source-of-truth links go through one case-markdown `Quelle` node per source file; the original web URLs are stored in `Quelle.external_sources` arrays.
- Every `BELEGT_IN` relationship carries `datenqualitaet="Belegt"`.
- `Stadt`, `Land`, `Bauwerk`, `Bauobjektrolle`, `Bauobjektklasse`, `Akteurrolle`, `Akteurtyp`, `Bauteiltyp`, `Materialgruppe`, `Huerde` and `HuerdeKategorie` are graph nodes, not scalar properties.
- Numeric project/component facts are properties on the node they describe, e.g. `flaeche_m2`, `anzahl`, `co2_einsparung_kg`, `transportdistanz_km`.
- Components that are documented but not Direct Reuse are retained with `counts_as_direct_reuse=false` and linked to the appropriate strategy/source category, e.g. Bestandserhalt in Charles Malis and Surplus in Chiro.
- Unknown actors are not emitted as `Akteur` nodes, to avoid low-information entities.
