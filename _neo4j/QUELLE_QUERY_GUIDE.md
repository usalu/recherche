# How to find where a fact in `mit-bestand` came from

> One page. Five queries. That's all you need.
> Authoritative guide for source traceability after the Quelle remediation (2026-05-21). See [QUELLE_REMEDIATION_PLAN.md](QUELLE_REMEDIATION_PLAN.md) for design rationale.

---

## 30-second mental model

```
Any fact node ─[:BELEGT_IN]→ :Dossier ─[:ZITIERT_QUELLE]→ :ExternalLink {url}
```

- **`:Dossier`** — an internal markdown file describing one project (`q_holbein_gardens_london_md`, `q_stuttgart_210_md`, …). 100 of them.
- **`:ExternalLink`** — a clickable URL (`https://www.baunetzwissen.de/…`). ~1,000–2,000 of them after Q1.
- **`:BELEGT_IN`** — "this fact is documented in that dossier". Carries `evidence_excerpt` (the cell text).
- **`:ZITIERT_QUELLE`** — "this dossier cites that URL". Carries `locator` (`S1`, `S7`, `P1`, `bare`).

If you want the URLs immediately without writing a query: every `:Projekt`, `:Bauwerk`, `:Akteur` has a denormalised `source_urls` array. Click the node in Browser, see the list.

---

## Query 1 — "Just give me the URLs for this thing" (the 90 % query)

```cypher
MATCH (n {id: 'p_holbein_gardens_london'})
RETURN n.source_urls AS urls, n.source_count AS n;
```

Works on `:Projekt`, `:Bauwerk`, `:Akteur`. Instant. No traversal.

---

## Query 2 — "Where does this fact come from, with full context?"

```cypher
MATCH (n {id: 'p_holbein_gardens_london'})
OPTIONAL MATCH (n)-[bel:BELEGT_IN]->(d:Dossier)-[z:ZITIERT_QUELLE]->(ext:ExternalLink)
RETURN ext.url       AS url,
       ext.title     AS title,
       d.id          AS dossier,
       z.locator     AS sref,
       bel.evidence_excerpt AS excerpt
ORDER BY dossier, sref;
```

Returns one row per (dossier, URL) pair with the dossier reference label (`S1` …) and the verbatim excerpt that grounded the claim.

---

## Query 3 — "Which dossiers cite this URL?"

```cypher
MATCH (ext:ExternalLink {url: 'https://www.baunetzwissen.de/...'})
<-[:ZITIERT_QUELLE]-(d:Dossier)
RETURN d.id AS dossier;
```

Use to find every project whose dossier mentions a specific URL.

---

## Query 4 — "Which projects share this source?"

```cypher
MATCH (ext:ExternalLink {url: 'https://standards.iteh.ai/...'})
<-[:ZITIERT_QUELLE]-(:Dossier)<-[:BELEGT_IN]-(p:Projekt)
RETURN p.id AS projekt, p.name AS name
ORDER BY p.id;
```

Reveals projects citing the same standard / paper / report.

---

## Query 5 — "Give me one row per project with all sources packed in"

```cypher
MATCH (p:Projekt {id: 'p_stuttgart_210'})
OPTIONAL MATCH (p)-[:BELEGT_IN]->(d:Dossier)
RETURN p.name AS project,
       p.source_urls AS urls,
       p.source_count AS n_sources,
       collect(DISTINCT d.id) AS dossiers;
```

Quick one-liner for a CSV export or a UI card.

---

## What's where (so you stop guessing)

| If you want… | Look at… |
|---|---|
| The clickable URLs for a project | `Projekt.source_urls` (array) — Query 1 |
| The dossier that mentions a project | `:Dossier`-labelled `:Quelle` reachable via `:BELEGT_IN` |
| The verbatim cell text behind a fact | `BELEGT_IN.evidence_excerpt` on the edge |
| The S-ref label (`S1`, `S7`) for a URL | `ZITIERT_QUELLE.locator` on the edge |
| The dossier file on disk | `<dossier.id>.md` under `_neo4j/intake/archive/` or `_archive/research/` |
| The trust grade of a citation | `BELEGT_IN.evidence_origin` ∈ `{source_curated, topology_synthesized, registry_derived, inferred, external_unfolded}` |

---

## Helper script

```bash
python _scripts/find_sources.py p_holbein_gardens_london
```

Prints the project's source URLs to stdout. Wraps Query 2.

Add `--full` to also dump the excerpts:

```bash
python _scripts/find_sources.py p_holbein_gardens_london --full
```

---

## What does NOT exist anymore

- `:Quelle.text_content` — the full dossier markdown is no longer dumped on the node. Read the `.md` file from disk if you need full text.
- `quelltyp='case_markdown'` filter — still works for back-compat, but prefer `MATCH (d:Dossier)`.
- "Where is the URL?" — it's on `:ExternalLink.url`. Always. No exceptions.

---

## Edge cases

| Situation | Behaviour |
|---|---|
| A project with `source_count = 0` | The dossier exists but cited no URLs (rare; flagged as `:DataIssue {kind:'dossier_section8_missing'}` by R8 audit). |
| A URL appears in two dossiers | One `:ExternalLink` node, two incoming `:ZITIERT_QUELLE` edges. `ext.also_in_dossier` lists all citers. |
| A URL has tracking params (utm, fbclid, …) | Normalised away before MERGE. So `https://x.com/y?utm_source=a` and `https://x.com/y` are one node. |
| A URL appears as both `[label](url)` and bare in same dossier | Single edge, label-version wins (Q1 dedupes per dossier). |
| The dossier `.md` file is missing from disk | The `:Dossier` node still exists but `text_content_chars_pre_strip` may be 0; URLs would be missing. Flag via R8. |

---

## When to update the denormalised `source_urls`

`Projekt.source_urls` / `Bauwerk.source_urls` / `Akteur.source_urls` are denormalised for visibility. The graph traversal is source of truth.

**Re-run `mig_q4_surface_urls.cypher`** after any of:
- New dossier ingested
- A `:ZITIERT_QUELLE` edge added or removed
- A new `:Projekt`, `:Bauwerk`, or `:Akteur` introduced

The migration is idempotent. Safe to re-run anytime.

---

## How this evolved (one paragraph)

The pre-2026-05-21 `:Quelle` model used a `.quelltyp` property to discriminate 5+ kinds of source nodes; users had to remember to filter. The review-based remediation's R7.d added `Quelle.text_content` dumping full dossier markdown onto nodes — a mistake, since the disk file was already authoritative. The 2026-05-21 Quelle remediation (Q1–Q5): extracted every URL from `text_content` into `:Quelle :ExternalLink` nodes (Q1), promoted the discriminator to secondary labels `:Dossier` / `:ExternalLink` / `:ResearchDocument` / `:SectionRef` (Q2), stripped the markdown bloat (Q3), denormalised `source_urls` arrays onto `:Projekt`, `:Bauwerk`, `:Akteur` (Q4), and wrote this guide (Q5).

The historic `quelltyp` property is preserved for back-compat but new queries should use the secondary labels.

---

**End of QUELLE_QUERY_GUIDE.md.**
