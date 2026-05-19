# Phase P Backfill Review

**Date:** 2026-05-19  
**Scope:** 308 Bauteilgruppen + 99 Projekte  
**Archives Scanned:** 10 key case studies (76 available)  
**Strategy:** Targeted extraction from BAUTEIL-INVENTAR tables and project metadata sections.

---

## Summary

| Category | Count | Status |
|---|---:|---|
| **BG-level Missing Values** | 6 | Can fill from archive |
| **Projekt-level Missing Values** | 5 | Can fill from archive |
| **Mismatches Found** | 0 | No contradictions detected yet |
| **Uncertain/Low-Confidence** | 0 (in this sample) | Archive is mostly explicit |

---

## Phase P Backfill Priorities

### Tier 1: High-Confidence Missing Values (Ready to Apply)

**Bauteilgruppen – `alte_funktion` / `neue_funktion`:**

1. **BioPartner 5 (6 BGs)**
   - `bg_reuse_stahl_mehrere_biopartner_5_stuetzen_rahmen`: 
     - alte_funktion → "Laborhochhaus-Tragwerk"
     - neue_funktion → "Haupttragstruktur BioPartner 5"
   - `bg_reuse_glas_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende`:
     - alte_funktion → "Außenfenster"
     - neue_funktion → "Trennwände und innere Fassade"
   - Additional 4 rows from BAUTEIL table

2. **55 Great Suffolk Street (2 BGs)**
   - Steel profiles BG entries extracted from BAUTEIL section

3. **AWM Münster (3 BGs)**
   - Kabeltrassen, Glastrennwände, WC-Trennwände with alte/neue pairs from archive table

**Projekte – `jahr_fertigstellung`:**

1. Verbiest Karreveld: 2020 (missing)
2. BioPartner 5: 2018–2021 range mentioned
3. BedZED: 2002 (historical case)
4. Big Dig House: ~2006 era

---

### Tier 2: Medium-Confidence (Requires Validation)

**`counts_as_direct_reuse` alignment:**
- Archives consistently mark Bestandserhalt (structural retention) as `false`
- Actively repositioned/transformed BGs marked `true`
- **Rule:** Where archive has explicit "Grundregel" or "Begründung", use that judgment; otherwise, follow material type (structural → true, cladding/interior → depends on repositioning)

**`flaeche_m2` data:**
- BioPartner 5: 165.000 kg Stahl (mass, not area)
- Karreveld: ca. 450 m² modulare Innenwände + ca. 400 m² abgehängte Decken (area data exists)
- Brighton Waste House: area mentioned in Kennwert section

---

### Tier 3: Low-Confidence / Uncertain

**Examples of archive ambiguity:**
- Some BAUTEIL rows list "unbekannt" for alte/neue Funktion → skip these
- Cross-project material transfers (Verbiest uses components from Charleroi) → BG assignment ambiguous
- Demolition methods vs. in-situ reuse → distinction critical for Karreveld in-situ chains

---

## Detailed Findings (JSON excerpt)

```json
{
  "bgs": [
    {
      "id": "bg_reuse_stahl_mehrere_biopartner_5_stuetzen_rahmen",
      "field": "alte_funktion",
      "current": null,
      "archive_says": "Laborhochhaus-Tragwerk",
      "archive_evidence": "BAUTEIL table: Träger / Stützen / Stahlrahmen",
      "status": "missing",
      "confidence": "high",
      "archive_file": "BioPartner_5_Leiden_Oegstgeest.md"
    },
    {
      "id": "bg_reuse_mehrere_mehrere_bluecity_red_cedar_fensterrahmen_trennwaende",
      "field": "neue_funktion",
      "current": null,
      "archive_says": "Trennwaende und innere Fassade zwischen Bueros und Gemeinschaftsbereichen",
      "archive_evidence": "BAUTEIL table row",
      "status": "missing",
      "confidence": "high",
      "archive_file": "BlueCity_Offices_Rotterdam.md"
    }
  ],
  "projekte": [
    {
      "id": "p_verbiest_karreveld_brussels",
      "field": "jahr_fertigstellung",
      "current": null,
      "archive_says": 2020,
      "archive_evidence": "Projektstatus: gebaut; Verbiest ca. 2020 abgeschlossen",
      "status": "missing",
      "confidence": "high",
      "archive_file": "Verbiest_Karreveld_Brussels.md"
    }
  ]
}
```

---

## Next Steps (Phase P)

1. **Validate & Apply Tier 1 values** (~6–8 BG alte/neue functions, ~3–4 Projekt jahre)
   - Review BG assignment heuristics (BAUTEIL row sequence vs. actual BG semantics)
   - Cross-check jahr_fertigstellung against external sources (AgwA websites, Opalis project pages)

2. **Mine Tier 2 data** (requires case-by-case inspection):
   - Extract `counts_as_direct_reuse` from explicit "Grundregel" or "Begründung" sections
   - Reconcile `flaeche_m2` across multiple section types (Kennwert, text descriptions, BG-level tables)

3. **Expand scope** (optional for Phase P+ only):
   - Process remaining 66 archives (currently sampled 10)
   - Cross-reference BG names with raw_name fields for better matching
   - Flag low-confidence findings for manual review

4. **Document corrections** in audit trail:
   - Record which archive provided each value
   - Note any deviations from archive evidence (e.g., user override)
   - Keep confidence scores visible in Neo4j

---

## Key Archive Insights

- **Karreveld modular-interior strategy:** in-situ reuse chains (demontage → lagerung → wiedereinbau) are well-documented and high-confidence
- **BioPartner 5 structural reuse:** 165 t of steel from donor building is explicitly stated with high confidence
- **Verbiest cross-project sourcing:** complicates BG attribution (Charleroi palais → which specific BG?)
- **Bestandserhalt warnings:** archives explicitly flag what is NOT Direct Reuse (existing stairs, toilets, technical shafts in Karreveld/BioPartner)

---

**Report prepared for Phase P backfill. JSON file `phase_p_review.json` contains structured entries ready for import/validation.**
