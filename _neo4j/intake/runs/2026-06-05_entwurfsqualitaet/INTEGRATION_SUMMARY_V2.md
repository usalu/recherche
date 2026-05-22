# Entwurfsqualitaet v2 — Apply Summary

- Run: `entwurfsqualitaet_v2_2026_06_05`
- Vocabulary: literature-backed 8+8 (Brütting, CBA-AR, Plevoets, Frontiers 2025, BAMB, D5/FCRBE)

## Artefakte (bereit)

| Datei | Inhalt |
|---|---|
| `_neo4j/contracts/entwurfsqualitaet_vokabular_v2.seed.kg.jsonl` | 16 Knoten mit `name`, `name_de`, **`beschreibung`**, `literature_ref` |
| `_neo4j/contracts/entwurfsqualitaet_v2_legacy_map.json` | v1→v2 Mapping + deprecated IDs |
| `_neo4j/intake/runs/2026-06-05_entwurfsqualitaet/projekt_begriff_zuordnungen_v2.csv` | 79 aktive + 3 skip (DoNotExtract) |
| `_neo4j/intake/runs/2026-06-05_entwurfsqualitaet/apply_entwurfsqualitaet_v2.py` | Apply-Script |

## V2 Begriffe

**EM:** Design_with_Stock, Building_Transformation, Component_Matchmaking, Design_for_Disassembly, Spolia_Design, Typology_Adaptation, Material_Bank_Building, Circularity_Demonstrator

**AE:** Exposed_Reuse_Structure, Patchwork_Envelope, Modular_Grid_Form, Reversible_Tectonics, Cultural_Continuity_Spolia, Interior_Reuse_Atmosphere, Didactic_Circularity, Infrastructural_Spolia

## Graph-Apply

```powershell
python _neo4j/intake/runs/2026-06-05_entwurfsqualitaet/apply_entwurfsqualitaet_v2.py --commit
```

**Status:** Applied 2026-06-05. Backup: `_neo4j/review/backups/20260605T_entwurfsqualitaet_pre_v2/`. Reports: `apply_v2_report.json`, `verify_v2_report.json`.

## Post-apply (mit-bestand)

| Check | Result |
|---|---|
| Active EM / AE nodes | 8 / 8 (all with `beschreibung`) |
| EM / AE edges | 79 / 79 |
| Deprecated v1 orphans | 8 EM + 8 AE |
| Projects with `entwurfsbeschreibung` | 82 |
| Skip projects (no edges) | 3 |
| Graph totals | 2287 nodes / 15393 rels |
| Max term share | EM 35.4% / AE 34.2% |

## Kanten-Properties (neu)

- `integration_phase`: early | midway | late
- `integration_layer`: structure | envelope | interior
- `zuordnung_quelle`: manual_v2
- `vokabular_version`: v2

## Skip (Kanten entfernt, entwurfsbeschreibung bleibt)

- p_maison_dna_asse
- p_schaerenmoosstrasse_zuerich
- p_maison_des_canaux_paris
