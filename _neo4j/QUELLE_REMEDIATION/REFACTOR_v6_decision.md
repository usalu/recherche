# Q-EXT v6 — kill `:ZITIERT_QUELLE`, attach URLs directly, trace every node to its unfolding

**Date:** 2026-05-22 r4 · **Author:** orchestrator
**Trigger:** user instruction: *"Zirierte Quelle shouldn't exist, it should grab the url directly. all the input files… were unfolded in some way to the current nodes and edges so we need to trace it and map everything to its origin."*

> **TL;DR.** Looked at four representative input-file types. Each *unfolded* into the graph with a different rule. The current model wraps every URL in a `:Quelle :ExternalLink` node and inserts a `:ZITIERT_QUELLE` hop. That's needless indirection. v6 deletes `:ZITIERT_QUELLE`, attaches the concrete URL directly to the fact relationship or Claim, keeps `:Dossier`/`:ResearchDocument`/registry file nodes only as lineage containers, and tags every node + every edge with a precise `unfolding_kind`.

> **Correction:** no `.md` file is source truth. `Stuttgart_210.md`, `rotordc.md`, `akteursliste_master.md`, and research `.md` files are containers. The links inside the relevant row/section are the source truth.

---

## §1 What I read on disk (concrete)

I sampled four file types to understand actual unfolding patterns:

### §1.1 Building dossiers (`_archive/research/gebaeude/*.md`, batch dossiers)

Stuttgart_210.md — a multi-table .md, ~30 KB. Sections: Identification, Bauwerk, Akteure (table), Bauteilgruppen (table), Component technical properties (table), Quality + compliance (table), Building-level graph categories (table), Relationships (table), Funding & program, Economy.

**Unfolding rule:** one `:Projekt` per file; each *table row* describes 1+ entities (BG, Akteur, …). The URL lives in a `Source` column (`[S1](url)`) and applies to the **row** (i.e., to every entity in that row). Currently only the `:Projekt` gets a `:BELEGT_IN` to the dossier; the row-level entities don't.

### §1.2 Bauteilbörse files (`_archive/research/bauteilboerse/rotordc.md`)

YAML frontmatter + structured H2 sections (Kurzbeschreibung, Land/Region, Betreiber, Plattformtyp, Bauteilkategorien, Art der Wiederverwendung, Funktionen, Daten je Bauteil, Qualität, Logistik, Geschäftsmodell, Ökologische Bewertung, Stärken, Schwächen, Relevanz, **Quellen und Links**).

**Unfolding rule:** entire file → one `:Materialdepot` node. URLs at the bottom in `## Quellen und Links` are bare URLs (no markdown link syntax). The file is only a container; those concrete URLs can back whole-node/material-depot facts only when the file-level scope is clear.

### §1.3 Actor master file (`_archive/research/person/akteursliste_master.md`)

One big table per H2 section (Designer:innen, Technik / Forschung, …). Columns: Name | Sterne | Land | Akteur/Kontext | Warum relevant | Links. Each row is one actor; the Links column carries `[label](url)` markdown links (often 3–5 per row).

**Unfolding rule:** each row → one `:Akteur` (or `:Akteur:Person`) node. `akteursliste_master.md` itself is not evidence. URLs in that row's Links column back that specific actor/fact. Star ratings convert to a relevance score. The "Akteur/Kontext" cell often references organisations + projects (TODO: link the actor to those nodes too).

### §1.4 Research files (`_neo4j/intake/inbox/research/*.md`)

Mix of tables + prose. URLs appear as `[label](url)` in prose, as bare URLs in tables' Source columns, or in `<https://…>` angle-brackets.

**Unfolding rule:** entire file → one `:ResearchDocument` container. The research `.md` file is not evidence by itself. URLs back the **rules/standards/claims** in the immediate paragraph or table row, not the whole file.

---

## §2 What the current graph does wrong

For each (node, citation, url) triple, the graph today stores:

```
(:Projekt)-[:BELEGT_IN]->(:Quelle :Dossier {id:'q_stuttgart_210_md'})
(:Quelle :Dossier)-[:ZITIERT_QUELLE {locator:'S1'}]->(:Quelle :ExternalLink {url:'https://...'})
```

Problems:
1. **Three nodes** and **two edges** to express "Projekt P is described in dossier D which cites URL U".
2. **`:ExternalLink` wraps every URL** — adds 2,640 nodes whose only job is to hold a string property.
3. **`:ZITIERT_QUELLE`** is documentation, not data — it describes the dossier→URL relationship, which is a fact ABOUT the source document, not a fact about the domain.
4. **The user has to traverse two hops** to get from a fact to its URL. Even worse, the URL is detached from the row context.

---

## §3 v6 target model

### §3.1 Fact carrier — URL on the fact

```
(:Bauteilgruppe {id:'bg_stuttgart_210_clt_formwork'})-[:NUTZT_MATERIAL {
   source_container_id: 'q_stuttgart_210_md',
   locator:           'row:Bauteilgruppen:2:Material',
   source_url:        'https://www.holzbauoffensivebw.de/.../productId=38',
   source_url_status: 'reachable_2xx',
   source_url_verified: true,
   provenance_kind:   'dossier_row + external_url',
   row_excerpt:       'Stuttgart 21 CLT formwork elements | Schalungselement | Brettsperrholz | …'
}]->(:Material {id:'mat_brettsperrholz'})
```

One edge per (node, locator, URL) when the edge itself is the fact carrier, or one Claim with citation fields when the fact is complex. The URL is **on the fact/Claim**. The dossier/research/registry file id may be kept as lineage context, but it is not the source truth. No `:ZITIERT_QUELLE`. No `:ExternalLink` on the citation path.

For nodes cited in multiple rows of the same dossier → multiple edges (each with its own locator). For URLs that appear in many dossiers → URL is duplicated across edges. That duplication is intentional (each citation context is independent) and the storage cost is trivial.

### §3.2 What stays

- **`:Dossier`** — document container / lineage context. Stays as node, but not as evidence.
- **`:ResearchDocument`** — document container / lineage context. Stays, but not as evidence.
- **`:Bauteilbörse / :Materialdepot`** — already exists; each file → one such node.

### §3.3 What gets removed

- **`:ZITIERT_QUELLE`** — gone. URLs live on `:CITED_FROM_*` edges.
- **`:Quelle :ExternalLink` as a node-on-the-path** — gone. URLs are strings on edges.

### §3.4 What might persist as side-lookup (decision V6-1)

The 2,640 existing `:Quelle :ExternalLink` nodes carry useful metadata (`url_status`, `url_http_code`, redirect chain, body cache reference, Wayback fallback, …). Two options:

**Option A:** Drop them entirely. Duplicate `url_status` etc. on every `:CITED_FROM_*` edge that uses the URL. Simpler model.
**Option B:** Keep them as a **side-lookup** node (`:UrlMetadata` rename?) NOT on the citation path. Edges store the URL string; a query joining to `:UrlMetadata` by URL gives full reachability/verification metadata.

Recommendation: **Option B**. Rename `:Quelle :ExternalLink` → `:UrlMetadata`. Keep the rich properties. But the citation chain doesn't traverse through it. The user gets directness while we keep S2's hard-won reachability/probe results.

---

## §4 The provenance taxonomy — refined for v6

Every node and every edge gets two stable properties:

```
unfolding_kind ∈ {
  dossier_row,              // extracted from a row in a building/project dossier
  dossier_section,          // extracted from a prose section of a dossier
  bauteilboerse_file,       // whole-file → :Materialdepot
  registry_row,             // row in actor/master registry file
  research_section,         // research file prose section
  research_table_row,       // research file table row
  inference_rule,           // produced by an inference rule (era×material)
  controlled_vocabulary,    // graph-internal vocab seed
  topology_synthesized,     // Repair D / mig_*
  user_curated              // explicit manual annotation
}

unfolding_origin             // string — the specific origin reference
   // for dossier_row:        'q_stuttgart_210_md/Bauteilgruppen/row:2'
   // for bauteilboerse_file: 'archive/research/bauteilboerse/rotordc.md'
   // for inference_rule:     'mig_3_2_pollutant_inference/rule_b_era_and_material'
   // for controlled_vocabulary: 'q_controlled_vocab_seed'
   // for topology_synthesized: 'mig_repair_4_1_q1'
   // for user_curated:       'user:kinan/2026-05-22'
```

Every node has these two properties. Every edge has them too. They are **independent of `source_url`** — a node can have BOTH (e.g., unfolding_kind=dossier_row AND a source_url on its citation edge).

Combined with v6's `:CITED_FROM_*` edges (which carry the URL when one exists), the graph answers:

> "Where does this node come from? And if there's a clickable URL, what is it?"

…in **one hop** for URL-backed nodes, and **one node property** for non-URL-backed nodes.

---

## §5 The per-file-type unfolders

Each input file type needs its own unfolder. v6.A authoring plan:

| Input file | Output | Unfolder ID |
|---|---|---|
| Building dossier `.md` (gebäude, batches) | `:Projekt` + per-row facts/Claims carrying the concrete row URL; dossier id as lineage only | `unfolder_building_dossier` |
| Bauteilbörse `.md` | `:Materialdepot` + concrete `Quellen und Links` URLs on scoped facts/Claims; file id as lineage only | `unfolder_bauteilboerse_file` |
| Actor master file `.md` | per-row `:Akteur` + concrete row links on actor/fact Claims; `akteursliste_master.md` as lineage only | `unfolder_registry` |
| Research file `.md` | `:ResearchDocument` container + concrete row/section URLs on facts/Claims | `unfolder_research` |

Each unfolder is a function from `(file_path, node_index) → list of (node_id, container_id, locator, source_url, unfolding_kind)` tuples. `file_path` / `container_id` are lineage; `source_url` is the evidence. The shared driver then writes the facts idempotently.

---

## §6 What v6.B does to existing edges/nodes

For every existing node and edge in the graph, set `unfolding_kind` + `unfolding_origin` by inferring from current properties:

| Current `evidence_origin` | Mapped to v6 `unfolding_kind` |
|---|---|
| `source_curated` + linked to a `:Dossier` | `dossier_row` (when locator can be derived) OR `dossier_section` |
| `source_curated` + linked to a `:ResearchDocument` | `research_section` |
| `source_curated` + linked to a Materialdepot file | `bauteilboerse_file` |
| `source_curated` + linked to a registry master file | `registry_row` |
| `registry_derived` | `registry_row` |
| `inferred` | `inference_rule` |
| `topology_synthesized` | `topology_synthesized` |
| `external_unfolded` | `external_url` (this becomes a `source_url` on the edge, not a separate origin) |
| (no `evidence_origin`) + controlled-vocab-style label | `controlled_vocabulary` |

After v6.B every node + every edge declares `unfolding_kind`. The legacy `evidence_origin` stays for back-compat for one cycle, then gets dropped.

---

## §7 The kill of `:ZITIERT_QUELLE` — migration steps

The older sketch below used `:CITED_FROM_DOSSIER` as the replacement edge. That is superseded by the current rule: the concrete URL must land on the actual fact relationship or Claim. A document/registry edge may remain as lineage context only.

```cypher
// v6.C.1 — promote each :ZITIERT_QUELLE URL to the actual fact carrier

MATCH (n)-[bel:BELEGT_IN]->(d:Dossier)-[zq:ZITIERT_QUELLE]->(ext:ExternalLink)
// For each (n, d, ext.url) triple, copy ext.url onto bel only if
// bel is the exact fact being sourced. Otherwise create/reuse a Claim.
SET bel.source_url = ext.url,
    bel.source_status = 'exact',
    bel.source_url_status = ext.url_status,
    bel.source_container_id = d.id,
    bel.source_locator = coalesce(zq.locator, 'bare'),
    bel.source_note = zq.evidence_excerpt,
    bel.unfolding_kind = coalesce(bel.unfolding_kind, 'dossier_row'),
    bel.unfolding_origin = d.id + '/' + coalesce(zq.locator, 'bare'),
    bel.migration_origin = coalesce(bel.migration_origin, '') + '|mig_qext_v6_kill_zitiert_quelle';

// v6.C.2 — delete the :ZITIERT_QUELLE edges
MATCH ()-[r:ZITIERT_QUELLE]->() DELETE r;

// v6.C.3 — rename :Quelle:ExternalLink → :UrlMetadata (side-lookup only)
MATCH (e:ExternalLink) SET e:UrlMetadata REMOVE e:ExternalLink, e:Quelle;
// Now :UrlMetadata is the metadata store; not on the citation path.

// v6.C.4 — verify no :ZITIERT_QUELLE remaining
MATCH ()-[r:ZITIERT_QUELLE]->() RETURN 'should_be_zero' AS check, count(r);
```

After v6.C: user-facing traversal reads the fact relationship or Claim directly. The URL is on that fact carrier.

---

## §8 What "fully traced" means in v6

A node is **fully traced** iff:
- It has `unfolding_kind` set AND
- It has `unfolding_origin` set AND
- Either (a) the fact relationship or Claim has non-null `source_url`, OR (b) `unfolding_kind ∈ {controlled_vocabulary, inference_rule, topology_synthesized, user_curated}` and points to source facts/rules rather than a guessed URL.

For an edge: same rule.

The audit query becomes:
```cypher
MATCH (n) WHERE n.unfolding_kind IS NULL OR n.unfolding_origin IS NULL
RETURN labels(n)[0] AS label, count(n) AS untraced_count;
```

Target: **0 untraced** post-v6.

---

## §9 What ships in v6

Five migrations + one parser + one audit:

| Order | Artefact | Purpose |
|---|---|---|
| v6.A.1 | `unfolder_building_dossier.py` | Walks every `.md` in gebäude / batch dirs; attaches concrete row URLs to facts/Claims |
| v6.A.2 | `unfolder_bauteilboerse_file.py` | Walks Bauteilbörse files; attaches concrete file/section URLs to scoped facts/Claims |
| v6.A.3 | `unfolder_registry.py` | Walks `akteursliste_master.md` + similar; attaches concrete actor-row links to facts/Claims |
| v6.A.4 | `unfolder_research.py` | Walks research files; attaches concrete section/row URLs to facts/Claims |
| v6.B | `mig_qext_v6_b_unfolding_taxonomy.cypher` | Sets `unfolding_kind` + `unfolding_origin` on existing nodes/edges |
| v6.C | `mig_qext_v6_c_kill_zitiert_quelle.cypher` | Promotes :ZITIERT_QUELLE to edge properties; drops the type; renames ExternalLink → UrlMetadata |
| v6.D | `audit_full_tracing.py` | Per-label table of `fully_traced` % + sample untraced nodes |

---

## §10 Open decisions

| ID | Question | Default |
|---|---|---|
| V6-1 | Drop `:Quelle :ExternalLink` entirely OR keep as `:UrlMetadata` side-lookup? | **Keep as `:UrlMetadata`** — preserves S2's reachability + Wayback metadata |
| V6-2 | When a fact is cited in multiple rows of the same container, write multiple citations OR aggregate to one? | **Multiple citations** — each (fact, container, locator, URL) tuple is its own citation context |
| V6-3 | What if a dossier row has multiple URLs in the Source column? | One edge per URL × the row's matched nodes |
| V6-4 | Should source truth live on document edges or fact carriers? | **Fact carriers**. Document edges are lineage only. |
| V6-5 | The legacy `evidence_origin` property — drop or keep? | Keep one cycle, drop in v7 |
| V6-6 | Reverse direction for lineage edges? | Secondary question only; source truth is the concrete URL on the fact/Claim. |
| V6-7 | For research files with hundreds of URLs, cap edges per (node, dossier) at N? | NO cap; storage is cheap |
| V6-8 | Should `:UrlMetadata` retain the `:Quelle` label for back-compat? | NO — clean break |

---

## §11 The minimum viable v6 — what to ship first

Don't ship everything at once. Two waves:

**Wave 1 (the user's stated demand): kill `:ZITIERT_QUELLE`**
- v6.C — promote `:ZITIERT_QUELLE` URLs to `source_url` on fact relationships or Claims.
- Rename `:ExternalLink` to `:UrlMetadata`.
- After this wave: URL is on the fact carrier directly. User can stop traversing `:ZITIERT_QUELLE`.

**Wave 2 (the deeper goal: full tracing): per-file unfolders + taxonomy**
- v6.A.* unfolders write the missing fact/Claim citations (one per row/section × concrete URL).
- v6.B sets `unfolding_kind` + `unfolding_origin` on every node.
- v6.D audit reports `fully_traced` per label.

Each wave is independently committable and independently rollbackable.

---

## §12 What the user sees post-v6

Browser, clicking `mat_stahl`:

```
:Material
  id:                       mat_stahl
  name:                     Stahl
  unfolding_kind:           controlled_vocabulary
  unfolding_origin:         q_controlled_vocab_seed
  source_urls:              [12 URLs — denormalised from exact fact/Claim citations]
  confirmed_source_count:   8
  primary_source_url:       https://standards.iteh.ai/.../cen-ts-1090-201-2024
```

And one exact fact relationship/Claim:
```
(project_or_component)-[:NUTZT_MATERIAL {
   source_container_id:'q_holbein_gardens_london_md',
   locator:'row:Bauteilgruppen:1:Material',
   source_url:'https://www.akt-uk.com/...',
   source_url_status:'reachable_2xx',
   source_url_verified:true,
   row_excerpt:'Steel beams from donor → Holbein reuse | Steel | direct reuse | …'
}]->(mat_stahl)
```

The URL is right on the fact. Locator says **which row** of which container supplied the URL. The chain is honest.

For nodes that have NO URL (`Akteurrolle`, `Status`, `Layer`):
```
:Status {id:'status_realisiert', name:'Realisiert'}
  unfolding_kind:    controlled_vocabulary
  unfolding_origin:  q_controlled_vocab_seed
  source_urls:       []           # honest — vocab doesn't have URLs
  primary_source_url: null
```

That's the honest answer.

---

## §13 Long-term-plan adjustment

[LONG_TERM_PLAN.md §4.1](../LONG_TERM_PLAN.md) (Ingestion contract) becomes:

> Every PR adding a new dossier must:
> 1. Specify which **unfolder** applies (`building_dossier`, `bauteilboerse_file`, `registry`, `research`).
> 2. Pass CI validators: schema check + per-row URL extraction smoke test.
> 3. After merge, the per-row parser writes concrete URLs onto fact relationships or Claims automatically — no manual triple insertion.

The graph stops accumulating manually-edited triples. Every fact has a clear origin file + locator from the moment it lands.

---

## §14 Why v6 is the right ending shape

The user's stated goals, by line:

| User said | v6 answers it via |
|---|---|
| "Zirierte Quelle shouldn't exist" | `:ZITIERT_QUELLE` dropped in v6.C |
| "grab the url directly" | `source_url` property on the fact relationship or Claim |
| "all the input files… were unfolded" | Per-file-type unfolders (v6.A) document the unfolding rule |
| "trace it and map everything to its origin" | `unfolding_kind` + `unfolding_origin` on every node + edge (v6.B) |
| "when its a direct link or any other way" | Taxonomy of 10 unfolding kinds; URL is one kind, others are explicit |
| "EVERY SINGLE LINK PROVIDED HAS TO BE MAPPED IN THE CORRECT CORRESPONDING NODE/EDGE" | Per-row unfolders + per-(node, dossier, locator) edges |

---

## §15 Run order

```bash
# Wave 1 (minimum viable):
python qext_runner.py kill_zitiert_quelle    # v6.C — drop :ZITIERT_QUELLE, attach URL to edges

# Wave 2 (full tracing):
python qext_runner.py unfold_building_dossiers   # v6.A.1
python qext_runner.py unfold_bauteilboerse       # v6.A.2
python qext_runner.py unfold_registry            # v6.A.3
python qext_runner.py unfold_research            # v6.A.4
python qext_runner.py taxonomy                   # v6.B
python qext_runner.py audit_tracing              # v6.D
```

Each subcommand idempotent. Wave 1 ships the user's immediate ask (URL on edge). Wave 2 reaches full tracing.

---

**End of REFACTOR_v6_decision.md.**
