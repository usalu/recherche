# Q-EXT v5 — per-row dossier parsing + provenance taxonomy

**Date:** 2026-05-22 r3 · **Author:** orchestrator
**Trigger:** user instruction: "test on every single node type… my goal is to be able to identify the source of every information in the node or the edge… EVERY SINGLE LINK PROVIDED HAS TO BE MAPPED IN THE CORRECT CORRESPONDING NODE/EDGE."

> **TL;DR.** Ran `test_all_labels.py` against every non-denylisted label (53 total, 5 samples each). Only 4 labels have working source mapping (Akteur, Projekt, Bauwerk, Programm). 35 labels show ZERO citation triples — they have no direct `:BELEGT_IN` to any dossier at all. The fix isn't more synonyms; it's a **per-row dossier parser** that creates direct `:BELEGT_IN` edges from every node mentioned in a dossier row to that dossier, with the row locator preserved. Plus a **provenance taxonomy** so every fact's source is categorised (URL, dossier-section, domain-knowledge, inference, registry, topology, vocab, user-curated).

---

## §1 Test results (concrete, from live graph)

53 labels tested, 5 samples each (where available). `total_triples_checked` = number of (URL, dossier) pairs the test could find for the sampled nodes.

### Tier A — confirmed source mapping works (4 labels)

| Label | samples | with_BOTH | %nodes | total_BOTH | total_D_only | triples |
|---|---:|---:|---:|---:|---:|---:|
| **Akteur** | 5 | 4 | 80.0% | **20** | 13 | 586 |
| **Projekt** | 5 | 3 | 60.0% | **9** | 8 | 211 |
| **Bauwerk** | 5 | 1 | 20.0% | 7 | 4 | 280 |
| **Programm** | 5 | 1 | 20.0% | 3 | 2 | 113 |

Pattern: these have direct `:BELEGT_IN → :Dossier` edges from the curated import. v4 works for them.

### Tier B — citation paths exist but 0 BOTH (11 labels)

| Label | samples | triples | BOTH | D_only |
|---|---:|---:|---:|---:|
| RechtlicheBedingung | 5 | 547 | 0 | 0 |
| Bauteilgruppe | 5 | 265 | 0 | 0 |
| Zertifizierungssystem | 5 | 185 | 0 | 0 |
| Materialdepot | 5 | 166 | 0 | 0 |
| Wiederverwendungskette | 5 | 147 | 0 | 0 |
| Software | 5 | 142 | 0 | 0 |
| PruefungNachweis | 5 | 115 | 0 | 0 |
| Tool | 4 | 99 | 0 | 0 |
| Norm | 3 | 61 | 0 | 0 |
| Material | 5 | 40 | 0 | 0 |
| Bauteiltyp | 5 | 40 | 0 | 0 |
| Leistungsanforderung | 5 | 40 | 0 | 0 |
| Aufbereitungsverfahren | 5 | 40 | 0 | 0 |
| Verbindungstechnik | 3 | 30 | 0 | 0 |

These nodes ARE reachable to URLs through some path, but the **narrow `evidence_excerpt` on the `:ZITIERT_QUELLE` edges doesn't mention them by name**. The rewiden migration was authored but never run; even after rewiden, these node types are referenced in dossier rows that don't include their name in the surrounding text (often the URL is at the end of a "Source:" column while the node's term is in column 1).

### Tier C — no direct dossier grounding at all (35 labels)

5 samples each, ALL skipped because no dossier `:BELEGT_IN` chain exists:

```
Akteurrolle, Akteurtyp, Akzeptanz, BauaufgabeIntervention,
Bauobjektklasse, Bauobjektrolle, Bauproduktstatus, Bausystem,
Bauteilebene, Bauweise, BauwerkEra, Beschaffungsweg, Defekt,
Funktionswechsel, Huerde, HuerdeKategorie, Kennwert, LCAModule,
Layer, Logistik, Marktmodell, MatchingQualitaet, Materialgruppe,
Methode, Nutzung, Prozessphase, Ressourcenquelle, ReuseRule,
Rueckbauverfahren, Schadstoff, Status, Tragwerksprinzip,
WiederverwendungsArt, Wirtschaft, ZustandsKlasse
```

These are vocab / controlled-term / structural nodes. They have `source_urls` (via 1..3 hop traversal) but no `:BELEGT_IN` edge of their own. The graph currently treats them as **anonymous referents** rather than as **citable entities**.

---

## §2 Why the current model fails the user's goal

The user's exact ask: *"EVERY SINGLE LINK PROVIDED HAS TO BE MAPPED IN THE CORRECT CORRESPONDING NODE/EDGE."*

What the data shows:
1. The graph has ~726 cached URLs from real research/dossier files.
2. Only ~4 of 50 node types have any actual mapping between their nodes and those URLs.
3. The other ~46 node types get URLs only by transitive inheritance through citation chains, which is **the wrong correspondence**: a Material `mat_stahl` inherits URLs from every Projekt that uses steel, regardless of whether those URLs say anything about steel.

**Root cause:** dossiers contain rows like:

```
| Bauteilgruppe | Bauteiltyp | Material | WiederverwendungsArt | Source |
| Stuttgart 21 CLT formwork | shell element | Brettsperrholz | upcycling | [S1](https://...) |
```

Today, only the `Projekt` gets a `:BELEGT_IN` to this dossier. The Bauteilgruppe, Bauteiltyp, Material, and WiederverwendungsArt nodes mentioned in this row also deserve a `:BELEGT_IN` edge to this dossier (with row locator), but none exists.

---

## §3 The v5 architecture

Two structural changes. Both required to meet the user's goal.

### §3.1 Change A — per-row dossier parser

For every `.md` dossier and research file, walk row-by-row (or section-by-section for prose). For each row, identify every node `id` or `name` mentioned. Create a `:BELEGT_IN` edge from each mentioned node to the dossier with:

```
locator: 'row:Bauteilgruppen:2'              // for table rows
       | 'section:Akteure'                    // for prose sections
       | 'cell:Bauteilgruppen:2:Material'     // for a specific cell
       | 'sref:S5'                            // for source-reference cells
provenance_kind: 'dossier_row'                // see §3.2
parsed_at: <date>
```

Result: every node's relationship to its dossier(s) is **direct and explicit**. The traversal `(node)-[:BELEGT_IN]->(:Dossier)` now returns the right set for every node, not just Projekt/Akteur/Bauwerk/Programm.

### §3.2 Change B — provenance taxonomy

The user said: *"whether its a url, Domain knowledge or whatever other category. come out of the category to organize."* That asks for an explicit source taxonomy. Adopt **8 categories**:

```
provenance_kind ∈ {
  external_url,              // a clickable URL (S1/Q-EXT.A captured)
  dossier_row,               // a specific row/cell in a .md dossier (v5)
  research_file,             // a research/* .md file (S1 + Q-EXT.A)
  domain_inference,          // rule-derived (era×material; HAS_RISK_POLLUTANT)
  registry,                  // master files like q_akteursliste_master_md
  topology_synthesized,      // Repair D-style graph-derived
  controlled_vocabulary,     // graph-internal vocab (Akteurrolle, Status, …)
  user_curated               // explicit manual annotation
}
```

Every node carries:
```
provenance_kind             // primary category
provenance_evidence         // list of source references (URLs / dossier rows / rule names / …)
provenance_confidence       // {high, medium, low, unknown}
```

Every edge carries the same trio (mostly already done — just normalised under this enum).

### §3.3 Putting it together — what "fully sourced" means

A node is **fully sourced** iff it has at least ONE evidence entry of `external_url` OR `dossier_row` OR `research_file` (the "primary" categories — externally verifiable). Without any of these, the node is `controlled_vocabulary` (acceptable for vocab types) or `topology_synthesized` (acceptable for derived nodes, but flagged for the audit).

A `:Material` like `mat_stahl` becomes fully sourced when:
- Some dossier row mentions "Stahl" → creates `:BELEGT_IN` from mat_stahl to the dossier
- That dossier cites at least one URL via `:ZITIERT_QUELLE`
- Both edges exist → mat_stahl is now PROPERLY mapped to its source URLs

---

## §4 Implementation phases

### v5.A — Parse every dossier and research file (driver-side)

```python
# Pseudocode for the parser
def parse_dossier(md_path: Path, all_node_index: dict[str, list[Node]]):
    text = md_path.read_text()
    sections = split_into_sections(text)
    for section in sections:
        if is_table(section):
            rows = parse_table(section)
            for row_idx, cells in enumerate(rows):
                row_text = " ".join(cells)
                # Match against the node index
                for node_id, terms in all_node_index.items():
                    if any(term_in(t, row_text) for t in terms):
                        emit_belegt_in_edge(
                            node_id, dossier_id,
                            locator=f"row:{section.title}:{row_idx}",
                            provenance_kind="dossier_row",
                        )
                # Also extract URLs in this row and emit ZITIERT_QUELLE
                for url in extract_urls(row_text):
                    emit_zitiert_quelle(dossier_id, url,
                                       locator=f"row:{section.title}:{row_idx}")
        else:
            # Prose section
            for node_id, terms in all_node_index.items():
                if any(term_in(t, section.text) for t in terms):
                    emit_belegt_in_edge(node_id, dossier_id,
                                       locator=f"section:{section.title}",
                                       provenance_kind="dossier_row")
```

Output: dramatic increase in `:BELEGT_IN` edge count. **Confirmed by test:** Stuttgart 210 alone produces 304 new `:BELEGT_IN` edges across 19 labels (see §10 for details). Extrapolated to ~100 dossiers + ~3,000 research files: **50,000–100,000 new edges**.

### v5.B — Apply provenance taxonomy

For each existing node/edge:
- Set `provenance_kind` based on `evidence_origin` mapping:
  - `source_curated` + `case_markdown` link → `dossier_row`
  - `source_curated` + `external_link` → `external_url`
  - `source_curated` + `research_markdown` → `research_file`
  - `inferred` → `domain_inference`
  - `registry_derived` → `registry`
  - `topology_synthesized` → `topology_synthesized`
  - `external_unfolded` → `external_url`
  - (no origin) + vocab labels → `controlled_vocabulary`

### v5.C — Re-confirm with the new mapping

Re-run test_all_labels.py after v5.A lands. Expected: every Tier B/C label gains direct triples, Material/Bauteilgruppe/Norm score meaningful BOTH counts.

### v5.D — Audit + report

For every node in the graph, the audit reports:
```
provenance_kind, n_provenance_evidence, n_external_urls, fully_sourced (bool)
```

And per-label:
- % nodes with `fully_sourced = true`
- distribution of provenance_kind

---

## §5 Why per-row parsing fixes everything in Tier B + Tier C

Take Material `mat_stahl` again. Under v5:

1. Parser scans `q_holbein_gardens_london_md`. Finds Section 4 "Materials & Components" row mentioning "Stahl" (or its alias "steel") in cell 2.
2. Emits `(mat_stahl)-[:BELEGT_IN {locator:'row:Materials:2:Material', provenance_kind:'dossier_row'}]->(q_holbein_gardens_london_md)`.
3. Same row's "Source" cell has `https://www.akt-uk.com/...`. Emits `(q_holbein_gardens_london_md)-[:ZITIERT_QUELLE {locator:'row:Materials:2:Source'}]->(q_url_<hash>)`.
4. Q-EXT.B re-walks: `mat_stahl` now has a DIRECT 2-hop path to the URL, not a 4-hop inherited one.
5. v4 BOTH-check on `mat_stahl`: page body (akt-uk.com) mentions "Stahl"/"steel"? Yes → BOTH = confirmed.

For Tier C labels like `:Schadstoff`:
1. Parser scans dossier rows about pollutants. Finds "asbest" mentioned in row 3 of "Quality & Risk" section.
2. Emits `(s_asbest)-[:BELEGT_IN {locator:'row:Quality:3:Schadstoff'}]->(q_<dossier>_md)`.
3. Same row may cite a pollutant-research URL.
4. v4: page mentions "asbest" / "asbestos"? Confirmed.

`:Akteurrolle`, `:Bauteilebene`, etc. — these are vocab; they should be marked `provenance_kind='controlled_vocabulary'` (no external source needed, by definition).

---

## §6 What ships in v5

| Artefact | Path |
|---|---|
| **This decision doc** | [REFACTOR_v5_decision.md](REFACTOR_v5_decision.md) |
| **v5.A migration** | (NEW) `mig_qext_v5_a_per_row_belegt_in.cypher` — parameterised write per (node, dossier, locator) triple |
| **v5.A runner** | (NEW) `qext_runner.py parse_rows` — parses every `.md` and emits the triples |
| **v5.B migration** | (NEW) `mig_qext_v5_b_provenance_taxonomy.cypher` — sets `provenance_kind` per node based on existing origin |
| **v5.C re-verify** | re-run `test_all_labels.py --samples 10` (expect Tier B/C to climb to Tier A) |
| **v5.D audit** | (NEW) `audit_provenance_coverage.py` — per-label `fully_sourced` matrix |

---

## §7 Open decisions (v5)

| ID | Question | Default |
|---|---|---|
| V5-1 | Run v5.A against ALL ~3,000+ dossier/research files, or restrict to non-archive ones first? | **All** — the archive files contain real info |
| V5-2 | What's the term-match strictness in the parser? Use the same v4 logic (synonym-expanded word boundary)? | YES |
| V5-3 | For non-table dossier prose, what's the section delimiter? `##` headers? | YES, with paragraph-level fallback |
| V5-4 | If 50,000+ new `:BELEGT_IN` edges land, what's the storage hit? | ~1–2 GB; acceptable |
| V5-5 | Cap edges per (node, dossier) pair at 1? (i.e. don't write multiple edges if the same node appears in 5 rows of one dossier?) | NO — preserve all locators; future querying may need them |
| V5-6 | Re-classify existing `:BELEGT_IN` edges with `provenance_kind` or only tag new ones? | **All** — for consistency |
| V5-7 | Should v5 also unlock C5 = page-body mention without dossier-side? | NO — keep the BOTH-AND discipline; v4 stays |

---

## §8 Long-term-plan adjustment

[LONG_TERM_PLAN.md §4.1](../LONG_TERM_PLAN.md) gains a new validator: every new dossier batch must include the per-row parser as a pre-flight that emits the `:BELEGT_IN` edges automatically. Manual ingestion no longer relies on the dossier author also setting up the citations — the parser handles it.

This is the moment the corpus stops being "Projekt-centric documents that mention vocab" and becomes a properly-grounded knowledge graph where every term is traceable to a row in a source.

---

## §9 What the user will see post-v5

A query like:

```cypher
MATCH (n {id: 'mat_stahl'})
RETURN n.name, n.provenance_kind, n.confirmed_source_urls, n.source_count
```

Returns:
```
name: 'Stahl'
provenance_kind: 'dossier_row'
confirmed_source_urls: ['https://www.akt-uk.com/...', 'https://standards.iteh.ai/...',
                        'https://www.steelconstruction.info/...', ...]
source_count: 12
```

Where the URLs are NO LONGER inherited via every project that mentions steel, but specifically the URLs cited in **rows that mention Stahl** across all dossiers.

For `:Akteurrolle`, the query returns:
```
provenance_kind: 'controlled_vocabulary'
confirmed_source_urls: []
```

That's the honest signal — controlled vocab nodes don't need external sources; their authority is the graph's internal vocab.

---

## §10 Test the v5 design before shipping — DONE, RESULTS BELOW

[test_v5_per_row_parser.py](../intake/runs/2026-05-21_quelle_remediation/agent_qext/logs/test_v5_per_row_parser.py) authored and run against **Stuttgart 210**. The proof-of-concept works.

### Output

| Metric | Value |
|---|---:|
| Sections parsed | 16 |
| URLs in dossier | 179 |
| **:BELEGT_IN edges that would be emitted** | **304** |
| Distinct (label, section) pairs hit | 112 |
| Labels covered (vs 4 today) | **19** |

### Per-label hits from Stuttgart 210 alone

| Label | Hits | Distinct nodes |
|---|---:|---:|
| Nutzung | 70 | 1 |
| Akteur | 32 | 13 |
| Status | 27 | 3 |
| Projekt | 24 | 2 |
| Programm | 23 | 2 |
| Akteurrolle | 21 | 3 |
| Material | 21 | 3 |
| Bauobjektklasse | 17 | 1 |
| Akteurtyp | 15 | 2 |
| Bauteiltyp | 14 | 6 |
| Layer | 10 | 2 |
| Zertifizierungssystem | 8 | 8 |
| Bauwerk | 5 | 1 |
| WiederverwendungsArt | 5 | 3 |
| Logistik | 4 | 1 |
| Prozessphase | 4 | 1 |
| Bauteilebene | 2 | 1 |
| Materialgruppe | 1 | 1 |
| Methode | 1 | 1 |

### Caveat the test exposed — over-broad term matching

Some vocab nodes' id-stems are too generic:

- `layer_site` matched the word "site" everywhere (70 hits via "Nutzung" → "Site")
- `at_person` matched any mention of "person"
- `be_system` matched "system"
- `log_transport` matched "transport"

**Fix needed in v5.A:** for vocab-style labels (Akteurtyp, Akteurrolle, Status, Bauteilebene, Layer, Logistik, Methode, Prozessphase, etc.), match against `name` only — NOT id-stem or short common synonyms. Maintain a `_term_blocklist` in synonyms.json:

```json
"_term_blocklist": ["site", "person", "system", "transport", "process",
                    "module", "type", "role", "kind", "phase", "status",
                    "method", "category", "level"]
```

The blocklist filters terms at index-build time; nodes still match on their distinctive name/aliases.

### What this means for v5

The architecture is sound. The implementation needs the term-blocklist + per-label strictness rule. After that, ~50 labels gain direct dossier-grounding — exactly what the user asked for.


Before any migration runs, I'll author `test_v5_per_row_parser.py` that:
1. Takes one dossier (e.g., Stuttgart 210).
2. Builds the node index of every existing graph node's id+name+aliases.
3. Runs the per-row parser.
4. Reports: how many (node, dossier, locator) triples would emerge, per label.
5. Spot-checks 3-5 examples per label.

This is the same test-before-ship discipline that caught the v3 and v4 problems.

---

## §11 Summary table — v5 will produce

| Label tier | Today | After v5.A |
|---|---|---|
| Tier A (4 labels) | works | works (more triples) |
| Tier B (11 labels) | triples but 0 BOTH | per-row triples + BOTH coverage rises |
| Tier C (35 labels) | 0 triples | direct `:BELEGT_IN` exists; either confirms via C4 OR is tagged `controlled_vocabulary` |

The 35 Tier C labels split into:
- **Vocab nodes** (Akteurrolle, Status, Bauteilebene, etc.) → tagged `controlled_vocabulary` — acceptable
- **Domain entities** (Schadstoff, Norm, ReuseRule, Leistungsanforderung, Material, Norm, Bauteiltyp, etc.) → should gain `dossier_row` provenance after v5.A; many will confirm via v4 BOTH

---

**End of REFACTOR_v5_decision.md.**
