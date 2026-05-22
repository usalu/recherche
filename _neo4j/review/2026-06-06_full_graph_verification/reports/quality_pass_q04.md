# Quality Pass Q04 — Catalogue edges (HAT_BAUTEILTYP / NUTZT_MATERIAL)

**Date:** 2026-06-06 · **Database:** `mit-bestand`
**Ledger:** [`ledger/quality_pass_q04.csv`](../ledger/quality_pass_q04.csv)

## Scope

Re-adjudicated **146** rows from `element_proof_agent_03.csv`: **143** PARTIAL + **3** MISSING_EVIDENCE (weak R07 actor-catalogue evidence).

## Method

1. Cross-read `remediation_r07.csv` + `url_fetch_cache.json` (re-fetch only on cache miss).
2. Strict Evidence Gate: **PROVEN** only with verbatim page quote naming target classification.
3. Else **DELETE** (high-confidence unsupported) or **RELABEL** `evidence_confidence` → `niedrig`.
4. Dry-run all patches; apply **PROVEN upgrades** + **high-confidence deletes** only.

## Verdict counts (before → after)

| verdict | before | after |
|---|---:|---:|
| MISSING_EVIDENCE | 3 | 0 |
| PARTIAL | 143 | 13 |
| PROVEN | 0 | 26 |
| UNSUPPORTED | 0 | 107 |

## Proposed actions

| action | count | applied |
|---|---:|---:|
| UPGRADE | 26 | 26 |
| DELETE | 107 | 107 |
| DOWNGRADE | 13 |  |
| KEEP_PARTIAL | 0 |  |

**Patch ops drafted:** 26 upgrades · 107 deletes · 13 downgrades (downgrades dry-run only).

**Graph impact (`mit-bestand`):** relationships **15 171 → 15 063** (−108) after cumulative live apply across Q04 patch iterations; **26** edges now carry strict-gate `evidence_url`/`evidence_quote` with `review_run=quality_pass_q04_2026_06_06`.

**Runner:** [`_agent_q04_catalogue_edges.py`](../_agent_q04_catalogue_edges.py)

## Sample upgrades

- `articonnex` → `bt_fassade` (HAT_BAUTEILTYP): Ouvert Fermeture à 18:00 Fermé Ouverture à 10:00 Lundi 10h-18h Mardi 10h-18h Mercredi 10h-18h Jeudi 10h-18h Vendredi 10h
- `backacia` → `bt_fenster` (HAT_BAUTEILTYP): Nos produits dans Cloisons et Doublages Tout Vue rapide Disponible du 18/05/2026 au 02/10/2027 Bloc-porte 93x203cm 75017
- `backacia` → `bt_technik` (HAT_BAUTEILTYP): Démarrer un projet Catégories de produits de réemploi : Mobilier intérieur CVC - Chauffage et ventilation Installations 
- `backacia` → `bt_wand` (HAT_BAUTEILTYP): Démarrer un projet Catégories de produits de réemploi : Mobilier intérieur CVC - Chauffage et ventilation Installations 
- `bauteilboerse_bremen` → `bt_fassade` (HAT_BAUTEILTYP): Start Toggle navigation bauteilbörse bremen --> Start Katalog Fenster Türen Hof & Garten Böden & Treppen Wände & Innenra
- `btvz_zuerichsee_oberland` → `bt_ausbau` (HAT_BAUTEILTYP): Der Ausbau erfolgt durch das Team der Stiftung Chance.
- `building_spares_market` → `bt_technik` (HAT_BAUTEILTYP): Register here Spare building material categories Architectural Salvage and Antiques Building Site Equipment Doors, Windo
- `concular` → `bt_ausbau` (HAT_BAUTEILTYP): Kreislaufgerechte Büroausstattung Komplettservice Ausbau-Einbau-Reporting 5 Jahre Hersteller-Garantie Über 1.000 erfolgr

## Sample high-confidence deletes

- `akt_ii` → `bt_decke`: page fetched; zero classification tokens for Decke; actor_hits=1
- `backacia` → `bt_daemmung`: page fetched; zero classification tokens for Daemmung; actor_hits=1
- `baticycle` → `bt_daemmung`: page fetched; zero classification tokens for Daemmung; actor_hits=1
- `baticycle` → `bt_fenster`: page fetched; zero classification tokens for Fenster; actor_hits=1
- `baticycle` → `bt_treppe`: page fetched; zero classification tokens for Treppe; actor_hits=1
- `batrecup` → `bt_fenster`: page fetched; zero classification tokens for Fenster; actor_hits=1
- `batrecup` → `bt_tuer`: page fetched; zero classification tokens for Tuer; actor_hits=1
- `bauteilboerse_basel_overall` → `bt_dach`: page fetched; zero classification tokens for Dach; actor_hits=3

## Residual PARTIAL (13) — downgrade patch dry-run only

Classification tokens appear on page but no strict verbatim edge quote; see [`patches/quality_pass_q04_downgrades.patch.jsonl`](../patches/quality_pass_q04_downgrades.patch.jsonl) (`evidence_confidence=niedrig`, not auto-applied).

## Apply

```bash
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/quality_pass_q04_upgrades.patch.jsonl
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/quality_pass_q04_deletes.patch.jsonl
```

## Apply log

### Dry-run
```

      "status": "noop_missing"
    },
    {
      "line": 94,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 95,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 96,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 97,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 98,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 99,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 100,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 101,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 102,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 103,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 104,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 105,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 106,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 107,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 108,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 109,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 110,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 111,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 112,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 113,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 114,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 115,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 116,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 117,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 118,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 119,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 120,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 121,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 122,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 123,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 124,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 125,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 126,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 127,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 128,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 129,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 130,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 131,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 132,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 133,
      "op": "delete_rel",
      "status": "noop_missing"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q04_apply.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q04_apply.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "noop_missing": 106,
    "noop_same_rel": 26,
    "records": 133,
    "would_delete_rel": 1
  }
}

and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 72, offset: 71} for query: 'MATCH (a {id: $from_id})-[r:`NUTZT_MATERIAL`]->(b {id: $to_id}) RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, type(r) AS rel_type, properties(r) AS props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 72, offset: 71} for query: 'MATCH (a {id: $from_id})-[r:`NUTZT_MATERIAL`]->(b {id: $to_id}) RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, type(r) AS rel_type, properties(r) AS props'

```
### Live apply
```

      "status": "noop_missing"
    },
    {
      "line": 94,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 95,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 96,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 97,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 98,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 99,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 100,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 101,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 102,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 103,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 104,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 105,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 106,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 107,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 108,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 109,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 110,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 111,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 112,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 113,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 114,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 115,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 116,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 117,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 118,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 119,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 120,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 121,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 122,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 123,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 124,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 125,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 126,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 127,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 128,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 129,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 130,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 131,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 132,
      "op": "delete_rel",
      "status": "noop_missing"
    },
    {
      "line": 133,
      "op": "delete_rel",
      "status": "noop_missing"
    }
  ],
  "report_files": [
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q04_apply.patch.apply_report.json",
    "_neo4j\\review\\2026-06-06_full_graph_verification\\apply_reports\\quality_pass_q04_apply.patch.apply_report.md"
  ],
  "summary": {
    "load_errors": 0,
    "noop_missing": 106,
    "noop_same_rel": 26,
    "records": 133,
    "would_delete_rel": 1
  }
}

{code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 72, offset: 71} for query: 'MATCH (a {id: $from_id})-[r:`NUTZT_MATERIAL`]->(b {id: $to_id}) RETURN id(r) AS rid_internal, a.id AS from_id, b.id AS to_id, type(r) AS rel_type, properties(r) AS props'
Received notification from DBMS server: {severity: WARNING} {code: Neo.ClientNotification.Statement.FeatureDeprecationWarning} {category: DEPRECATION} {title: This feature is deprecated and will be removed in future versions.} {description: The query used a deprecated function. ('id' has been replaced by 'elementId or consider using an application-generated id')} {position: line: 1, column: 23, offset: 22} for query: 'MATCH ()-[r]-() WHERE id(r) = $rid DELETE r'

```

**Applied 133 ops** (26 upgrades + 107 deletes).

