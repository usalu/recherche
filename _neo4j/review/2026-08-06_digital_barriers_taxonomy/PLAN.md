# Hürden-Taxonomie — Integrationsplan (knoten- & kantenbasiert)

**Datum:** 2026-08-06 · **Branch:** agent_s4/schema-cleanup · **DB-Writes bisher:** keine
**Vorbild:** [`../2026-06-03_taxonomy_integration_plan/FINAL_PLAN.md`](../2026-06-03_taxonomy_integration_plan/FINAL_PLAN.md)
**Schema-Referenz:** [`../2026-06-01_current_schema_guide/CURRENT_SCHEMA_GUIDE.md`](../2026-06-01_current_schema_guide/CURRENT_SCHEMA_GUIDE.md)

---

## 0. Leitprinzip

**Alles wird als Knoten und Beziehung modelliert — nichts Wichtiges in Properties.** Wir folgen exakt dem bestehenden Graphen: für jede Dimension des Import-Guides zuerst prüfen, ob es dafür schon einen Knotentyp gibt. Nur wo nachweislich keiner existiert, kommt ein neuer typisierter Knotensatz dazu. Properties tragen nur Identität (`id`, `name`, `barriere_code`) und, an Kanten, die Standard-Evidenzfelder des Repos.

Der ursprüngliche Graph hatte das Muster bereits: `(:Huerde)-[:HAT_HUERDEKATEGORIE]->(:HuerdeKategorie)`. Es wurde auf 11 flache Knoten mit englischem String-`category` reduziert. Wir **reaktivieren** es (Constraints + Indizes für `:HuerdeKategorie` und `HAT_HUERDEKATEGORIE` sind noch aktiv) und **vertiefen** es.

---

## 1. Hierarchie — nur zwei Labels, eine Kante (beide existieren bereits)

```
(:Huerde)            = Blatt-Hürde        id h_*      ~330
   └─[:HAT_HUERDEKATEGORIE]→
(:HuerdeKategorie)   = jede Gruppierungs-Ebene (Bereich A–H, Familie, Gruppe)   id huek_*   ~64
   └─[:HAT_HUERDEKATEGORIE]→   (verkettet nach oben, Richtung Kind→Eltern wie bisher)
(:HuerdeKategorie)   = Elternebene …
```

- **Kein neues Label, kein neuer Kantentyp für die Hierarchie.** `HAT_HUERDEKATEGORIE` wird von Kind zu Eltern verkettet; die 8 Bereiche A–H sind schlicht die `:HuerdeKategorie`-Knoten ohne Elternteil.
- Ebene ergibt sich aus der **Baumposition**, nicht aus einer Property. (`ebene`/`barriere_code` dürfen als Identitätsattribut mitlaufen, sind aber nicht der Träger der Struktur.)
- Regel Blatt vs. Kategorie: hat der Knoten Kinder → `:HuerdeKategorie`; ist er ein Blatt → `:Huerde`.

## 2. Wiederverwendung bestehender Knoten (kein neuer Typ nötig)

| Guide-Konzept | Bestehender Knoten | Beziehung (Richtung) | neu? |
|---|---|---|---|
| Projekt/BG **hat** Hürde | `:Projekt` / `:Bauteilgruppe` | `-[:HAT_HUERDE]->(:Huerde)` | **bestehend** — alle 237 Kanten bleiben |
| Beleg / Quelle | `:Quelle` (`:ResearchDocument`/`:ExternalLink`) | `(:Huerde)-[:BELEGT_IN]->(:Quelle)` | **bestehend** |
| Prozess-/Reuse-Phase | `:Prozessphase` (10) | `(:Huerde)-[:BETRIFFT_PHASE]->(:Prozessphase)` | Kante neu, Ziel-Knoten bestehend |
| Stakeholder | `:Akteurrolle` (22) | `(:Huerde)-[:BETRIFFT_ROLLE]->(:Akteurrolle)` | Kante neu, Ziel-Knoten bestehend |
| Standard | `:Norm` (103) | `(:Norm)-[:ADRESSIERT]->(:Huerde)` | Kante neu, Ziel-Knoten bestehend |
| Regulierung/Rechtsfrage | `:Regulierungsfrage` (11) | `(:Huerde)-[:TRIGGERS_REGULIERUNGSFRAGE]->(:Regulierungsfrage)` | **Kante bestehend** (heute BG→Regfrage) |
| Hürde verstärkt/verursacht Hürde | `:Huerde` → `:Huerde` | `VERURSACHT` / `VERSTAERKT` / `ERMOEGLICHT` / `MINDERT` | Kanten neu (nur die ~40 aus §5) |

## 3. Genuin neue Knotentypen (im Live-Graph gibt es nichts Passendes)

| Neuer Knoten | id | Anzahl | Beziehung | Begründung |
|---|---|---:|---|---|
| `:Plattformfunktion` | `pf_*` | ~23 | `(:Huerde)-[:BEEINTRAECHTIGT]->(:Plattformfunktion)` | Plattform-Fähigkeiten (Matching, Inventar, Passport …) — Kern der Bauteilportal-Forschung, kein Äquivalent vorhanden |
| `:Massnahme` *(optional, Phase 2)* | `mn_*` | ~12 | `(:Massnahme)-[:MINDERT]->(:Huerde)` | Gegenmaßnahmen aus §5 (Controlled Vocab, Persistent ID, Rollen-Zugriff …) |
| `:Evidenzstatus` *(oder Property)* | `evs_*` | 3 | `(:Huerde)-[:HAT_EVIDENZSTATUS]->` | etabliert / kontextabhaengig / hypothese — analog zu `:ZustandsKlasse`, `:Status` |
| `:Digitalbezug` *(oder Property)* | `db_*` | 3 | `(:Huerde)-[:HAT_DIGITALBEZUG]->` | direkt / ermoeglichender_kontext / physische_restriktion |

> `:Evidenzstatus`/`:Digitalbezug` als 3-Knoten-Vokabular ist konsistent mit dem Graphstil (auch `:Status`, `:ZustandsKlasse` sind Mini-Vokabulare). Wer schlanker will, macht sie zur Property — **eine** Entscheidung, dann konsequent.

## 4. Keine erfundenen Kanten

Die ~400 Blätter bekommen **nicht** automatisch je N Querkanten. Wir setzen nur:
- die **volle Hierarchie** (Knoten + `HAT_HUERDEKATEGORIE`),
- die **~40 belegten Querverweise** aus §5 des Guides,
- die **Quellen-Belege** (`BELEGT_IN`) aus dem Quellenregister,
- die **`:Plattformfunktion`-Kanten**, soweit im Guide benannt,
- die **237 bestehenden `HAT_HUERDE`** (umgehängt).

`BETRIFFT_PHASE` / `BETRIFFT_ROLLE` / `ADRESSIERT` nur dort, wo eine Quelle es hergibt — sonst als spätere Anreicherung markiert, nicht fabriziert.

## 5. Identität & Namen (Repo-Konvention)

- `id`: `h_<code>_<slug>` bzw. `huek_<code>_<slug>`, ASCII, snake_case, Umlaute → ae/oe/ue. Beispiel: `h_h5_3_ungeeignete_lagerbedingungen`, `huek_h5_lagerfaehigkeit`.
- `name`: deutsch, TitleCase (Umlaute im `name` erlaubt laut Schema-Guide §1 — echte Umlaute ok, nur `id` transliteriert).
- `barriere_code`: `H5.3` — stabiler externer Schlüssel als Identitätsattribut.
- `name_en`, `definition_de`: als Attribut (kein Strukturträger).
- Kanten tragen: `evidence_basis`, `evidence_confidence` (`belegt`/`wahrscheinlich`/`unsicher`), `evidence_url`, `evidence_quote`, `review_run='digital_barriers_2026_08_06'`, `created_at`.

## 6. Was reaktiviert / bereinigt wird

- **Reaktiviert:** Label `:HuerdeKategorie` + Kante `HAT_HUERDEKATEGORIE` (aktuell 0 Instanzen, aber Constraint `huerdekategorie_id` + `rel_hat_huerdekategorie_id` sind ONLINE) — bekommen echte Knoten statt Schema-Müll zu bleiben.
- **Umgeschrieben:** die 11 flachen `:Huerde` → siehe [`DROPOUT_REPORT.md`](DROPOUT_REPORT.md); 237 `HAT_HUERDE` umgehängt, dann Altknoten gelöscht.
- **Entfernt:** englische `category`-Property (ersetzt durch Bereichs-Knoten A–H).

## 7. Phasen

| Phase | Was | Graph? |
|---|---|---|
| 0 | Voll-Backup (JSONL) + Pre-Scan der 11 `:Huerde` + 237 Kanten | Lesen + Dump |
| 1 | Modell (dieses Dok) — bestätigt | Nein |
| 2 | Terminologie-Freigabe am Muster Bereich H ([`TAXONOMY_DE.md`](TAXONOMY_DE.md)) | Nein |
| 3 | Volle DE-Taxonomie A–H als `taxonomy_de.jsonl` (Knoten + Eltern-Kante) + `crosslinks.jsonl` (~40) + `plattformfunktion.jsonl` + `quellen.jsonl` | Nein (Dateien) |
| 4 | Seed: Constraints prüfen → alle `:HuerdeKategorie`/`:Huerde`/`:Plattformfunktion`/`:Quelle`-Knoten + `HAT_HUERDEKATEGORIE`-Hierarchie | Nur Hinzufügen |
| 5 | Querkanten (~40) + `BELEGT_IN` + `BEEINTRAECHTIGT` mit Evidenzfeldern | Nur Hinzufügen |
| 6 | `huerde_id_map.csv` → 237 `HAT_HUERDE` umhängen (`legacy_huerde_*`), 11 Altknoten löschen, `category` entfernen | Reroute + Delete |
| 7 | `verify_integration.cypher` — Konsistenz-Checks grün | Lesen |

## 8. Rollback

- Phase 4/5 additiv: `MATCH ()-[r {review_run:'digital_barriers_2026_08_06'}]-() DELETE r` + Seed-Knoten löschen.
- Phase 6 destruktiv: nur über Phase-0-Voll-Backup. Start erst wenn Phase 5 grün **und** Backup auf Klon verifiziert.
