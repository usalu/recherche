# Entwurfsqualitaet — Apply Summary

- Run: `entwurfsqualitaet_2026_06_05`
- Backup: `_neo4j/review/backups/20260605T_entwurfsqualitaet_pre/`

## Ergebnis

| Metrik | Vorher | Nachher |
|---|---|---|
| Knoten | 2255 | 2271 (+16 Begriffe) |
| Kanten | 15235 | 15399 (+164) |
| Projekte mit `entwurfsbeschreibung` | 0 | **82** |
| `HAT_ENTWURFSMETHODIK` | 0 | **82** |
| `HAT_ARCHITEKTURERGEBNIS` | 0 | **82** |

## Begriffsknoten

Jeder `:Entwurfsmethodik`- und `:Architekturergebnis`-Knoten hat:
- `id`, `name`, **`beschreibung`** (Definition des Begriffs)

## Zuordnung pruefen

- `projekt_begriff_zuordnungen.csv` — 82 matched + 14 unmatched
- `em_zuordnung_pruefung`: 43 Faelle
- `ae_zuordnung_pruefung`: 52 Faelle

## Artefakte

- `_neo4j/contracts/entwurfsqualitaet_vokabular.seed.kg.jsonl`
- `_neo4j/contracts/entwurfsqualitaet_phrase_zuordnung.json`
- `_neo4j/intake/archive/2026-06-05_entwurfsqualitaet/designQuality.md`
- `_neo4j/intake/runs/2026-06-05_entwurfsqualitaet/apply_entwurfsqualitaet.py`
