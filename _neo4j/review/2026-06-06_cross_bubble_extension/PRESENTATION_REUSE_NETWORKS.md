# Reuse Infrastructure as a Network

### A spoken presentation, with the graph as the slide deck

> **How to use this document.** Every section has two parts: what you *say*
> (the narration), and what you *show* (a Cypher query you paste into Neo4j
> Browser). The query renders the slide live. Each slide is built only from
> data that is actually in `mit-bestand` — **66 directed** evidence-tagged reuse
> connections (**132** undirected endpoints with `review_run`; **114** fully
> evidenced as `belegt`) across ten research runs / six country bubbles. Live graph
> **2,263 nodes / 15,060 rels** (read-cypher 2026-06-06). Nothing here is
> decorative; if a node is on screen, it has a source URL hanging off the
> relationship that put it there.

---

## Act 0 — Cold open: the problem nobody can see

**Say this:**

> "Every year, construction and demolition waste is the single largest waste
> stream in Europe — by mass, bigger than household waste. And the strange
> thing is that most of it isn't *broken*. A steel beam, a hardwood door, a
> sanitary fixture: these don't wear out the way we throw them out. We
> demolish working materials because we have no idea who, three kilometres
> away, needs exactly that beam next month.
>
> Reuse isn't fundamentally a *materials* problem. It's a *coordination*
> problem. The beam exists. The demand exists. The missing thing is the
> connective tissue — the catalogues, the platforms, the trade associations,
> the research labs — that lets supply find demand before the excavator
> arrives.
>
> So the question I want to answer tonight is not 'is reuse good?' Everyone
> agrees it is. The question is: **what does the coordination infrastructure
> actually look like, and is it connected enough to work?**
>
> To answer that, we stopped reading reports and built a graph."

**The thesis in one line:** *Reuse scales at the speed of its network, not its
material supply.*

---

## Act 1 — The big idea: model the infrastructure, not the material

**Say this:**

> "Here is the shift in perspective. Instead of cataloguing *materials*, we
> catalogued the *organisations* that move materials, and the *relationships*
> between them. Marketplaces, deconstruction firms, material passports,
> trade networks, universities, municipalities.
>
> Then we asked a deliberately naive question of each region: *who is
> connected to whom, and can you prove it?* The 'can you prove it' part is the
> whole discipline. Every single edge in this graph carries a source URL. No
> URL, no edge. We'll come back to why that rule matters."

**Slide 1 — The whole reuse-network layer at a glance.**

```cypher
// Every evidence-backed reuse connection we built, all six bubbles at once.
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run IS NOT NULL
RETURN a, r, b;
```

**What the audience sees:** a constellation — several dense local clusters,
joined by a few long edges. Point at it and say: *"Those dense clumps are the
bubbles. Those long edges between them are the bridges. The rest of the talk is
just zooming into each."*

**Slide 2 — Prove the discipline: count the connections per bubble.**

```cypher
// 66 directed tagged connections, partitioned by review_run.
MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
WHERE r.review_run IS NOT NULL
RETURN r.review_run AS bubble, count(r) AS connections
ORDER BY connections DESC;
```

| bubble | connections |
|---|---|
| `swiss_reuse_bubble_2026_06_05` | 14 |
| `germany_reuse_bubble_2026_06_05` | 13 |
| `cross_bubble_extension_2026_06_06` | 9 |
| `agent_06b_non_bubble_actor_networks_2026_06_06` | 9 |
| `post_quality_p06_02_2026_06_06` | 9 |
| `france_reuse_bubble_2026_06_05` | 6 |
| `rotor_dc_reuse_bubble_2026_06_05` | 3 |
| `netherlands_reuse_bubble_2026_06_05` | 1 |
| `quality_pass_q05_2026_06_06` | 1 |
| `remediation_wave2_r04_2026_06_06` | 1 |

**Say this:** *"Notice the cross-bubble block — nine directed edges — plus two
post-quality runs that added another eighteen. After the evidence audit removed
unsupported mesh edges, the Dutch bubble shrank to one surviving link; the
backbone is now Swiss + German density plus sourced bridges. Hold the bridge
count in mind; it's the punchline."*

---

## Act 2 — The method: bubbles, evidence, and one hard rule

**Say this:**

> "Three design decisions, and each one is a lesson.
>
> **First: we worked in bubbles.** We didn't try to draw the whole European
> reuse map in one sitting — that's how you get a hairball nobody trusts.
> Instead, each 'bubble' is one bounded research session: one country or one
> tight network, researched and sourced as a unit, tagged with its own
> `review_run`. Bubbles are *transport units*, not permanent truths. You can
> audit one, redo one, or delete one without touching the others.
>
> **Second: evidence lives on the relationship, not in a footnote.** When we
> say Backácia is listed in Opalis, the edge between them literally carries
> `evidence_url`, `evidence_quote`, and a confidence rating. The proof travels
> *with* the claim.
>
> **Third — and this is the one that bit us — direction is not duplication.**"

**Slide 3 — The confidence and connection vocabulary.**

```cypher
// What KINDS of connection exist, and how well each is evidenced?
MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
WHERE r.review_run IS NOT NULL
RETURN r.connection_kind AS connection_kind,
       r.evidence_confidence AS confidence,
       count(*) AS n
ORDER BY n DESC;
```

**Say this:** *"This is the semantic heart of the project. We didn't just say
'these two are connected'. We typed every connection: a `directory` listing is
a weak claim — 'they appear in the same catalogue'. A `formal_partnership` or a
`research_consortium` is a strong claim — 'they signed something, they
co-authored something'. The graph distinguishes a handshake from a hyperlink.*

*And confidence is explicit: `belegt` means we have a primary source making the
exact claim; `teilweise_belegt` means the source supports a weaker version and
we're being honest about the gap."*

**Slide 4 — The de-duplication story (the war wound).**

```cypher
// A connection should appear ONCE per pair, not twice.
// This proves we collapsed every bidirectional duplicate.
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]-(b)
WHERE r.review_run IS NOT NULL AND a.id < b.id
WITH a, b, count(r) AS edges_between
RETURN edges_between, count(*) AS pairs
ORDER BY edges_between;
```

**Say this:**

> "Early on, the graph looked twice as dense as it should. Restado seemed to
> have a thick double-line to Concular, to Cirkla, to Opalis — to everyone.
> The instinct is to panic: 'we've got dirty data'.
>
> We hadn't. The import had honestly written A→B *and* B→A for every
> partnership, because a partnership is symmetric. But Neo4j's undirected view
> drew both, so every real relationship looked like two. The fix wasn't to
> delete information — it was to pick one canonical direction per pair and
> *merge* the two evidence trails onto the survivor, so we kept every source
> URL. The lesson: **a duplicated drawing is not duplicated knowledge.** Today
> this query returns a single row: `edges_between = 1`."

---

## Act 3 — A tour of the bubbles

> Now we zoom in. Each bubble gets one slide and one story. I'll go in order of
> how *legible* the structure is — start with the cleanest, end with the
> sparsest — because each one teaches a different shape of network.

### 3.1 — Switzerland: the star (one association holds the field together)

**Slide 5:**

```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

**Say this:**

> "Switzerland is the cleanest shape in the whole dataset: a **star**. One
> node, **Cirkla**, sits in the middle and touches almost everyone — eleven
> partners, the single most-connected node in the project.
>
> Why? Because Cirkla *is* the directory. It publishes a national reuse
> register — `cirkla.ch/.../l'annuaire/experts/...` — and that register is
> doing the coordination work I described at the start. Bauteilladen
> Winterthur, Materiuum, Salza, Gruner's reuse platform, useagain: they're not
> connected to each other through handshakes, they're connected *because they
> all appear in the same trustworthy catalogue.*
>
> But look closer and you see the network has texture beyond the listings.
> There's a `committee_co_chair_affiliation` — a *person*, Benjamin Poignon,
> co-chairing across organisations. There's a `published_tool` edge to
> Cirkla-Scan and Swiss-Inv: the association doesn't just list members, it
> ships software. And there's an `ecosystem_practice_triangle` linking Cirkla
> to Zirkular, whose flagship is the K.118 building — Switzerland's most-cited
> reuse project. The star has a research arm and a software arm, not just a
> phone book."

**The pattern to name out loud:** *a star network is cheap to grow but fragile
— remove the centre and the field shatters. Switzerland's reuse coordination
has a single point of failure, and its name is Cirkla.*

### 3.2 — Germany: the institutional braid

**Slide 6:**

```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run = 'germany_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

**Say this:**

> "Germany is not a star. It's a **braid of three strands** that happen to meet.
>
> Strand one is *physical*: the Bauteilbörsen — the salvage depots. Bremen and
> Hannover are tied together as `bauteilnetz_peer_exchange`, both members of
> the **bauteilnetz Deutschland** network. This is the oldest, most analog
> layer — literal warehouses of saved components.
>
> Strand two is *digital*: **Concular** and **Restado**, the marketplaces, plus
> Madaster the material-passport platform. Watch how the physical and digital
> strands touch: Bauteilbörse Hannover has a `marketplace_listing` edge into
> Restado. The warehouse put its stock online. That single edge is the whole
> circular-economy transition in miniature.
>
> Strand three is *academic*: the **Haus der Materialisierung** in Berlin — a
> shared building where Kunst-Stoffe, Material Mafia, TU Berlin and Circular
> Berlin literally co-locate as a `research_consortium`. Reuse research and
> reuse practice under one roof.
>
> Germany's strength is exactly this institutional thickness. Its weakness:
> the three strands are only lightly stitched to each other."

**Slide 6b — the insight hidden in a brand name:**

```cypher
// Why did Restado and Concular look like the same organisation?
MATCH (a {id:'concular'})-[r:VERBUNDEN_MIT_AKTEUR]->(b {id:'software_restado'})
RETURN a.id, r.connection_kind, r.evidence_quote, r.evidence_url, r.evidence_confidence;
```

**Say this:** *"Here's a semantic catch the graph forced us to get right.
Restado and Concular kept colliding. The reason, straight from the source:
'restado ist eine Marke der Concular GmbH' — Restado is a **brand operated by**
Concular. They're not two peers; they're a company and its marketplace. We
typed that edge `marketplace_brand_operator` instead of a generic partnership.
The graph made us distinguish a corporate fact from a collaboration."*

### 3.3 — France: the catalogue-as-glue, plus a research spine

**Slide 7:**

```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run = 'france_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

**Say this:**

> "France rhymes with Switzerland — there's a directory holding it together —
> but the directory is **Opalis**, and France adds a second, very different
> kind of glue.
>
> The first glue is the listing mesh: Backácia, Cycle Up, Mineka, Association
> Réavie — they're all `supplier_listing` entries in Opalis, and we also drew
> `opalis_directory_peer` edges between them because being in the same curated
> catalogue *is* a relationship. That's the same logic as Cirkla.
>
> The second glue is research. **Bellastock** and **CSTB** — the national
> building-science centre — are tied through the **REPAR** and **SPIROU**
> programmes (`research_programme`, `spirou_consortium`). This is the layer
> that turns reuse from craft into standard: testing protocols, technical
> guidance, the paperwork that lets an insurer accept a reclaimed beam.
>
> So France shows two coordination mechanisms side by side: a *marketplace*
> catalogue and a *standards* consortium. Different tools, same job — reducing
> the friction of trust."

### 3.4 — Netherlands: urban mining and the lineage of an idea

**Slide 8:**

```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run = 'netherlands_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

**Say this:**

> "The Netherlands is the most *meshed* of the bubbles — fewer nodes, but
> they're nearly all interconnected, because the Dutch scene is small, mature
> and densely collaborative. New Horizon (urban mining), Insert (marketplace),
> Repurpose, Superuse Studios, Madaster, and the City of Utrecht form an almost
> complete little graph: a `dutch_reuse_marketplace_mesh` crossed with a
> `dutch_reuse_data_mesh`.
>
> But the edge I love most here is a single one: `oogstkaart_lineage`, from
> Superuse Studios to New Horizon. The **Oogstkaart** — the 'harvest map' — was
> a pioneering Dutch reuse mapping tool invented by Superuse, and the source
> records that it was *adopted by* New Horizon. That's not a partnership; it's
> **intellectual inheritance**. One organisation invented a method, another
> scaled it. The graph can hold the genealogy of an idea, not just a contract.
>
> And the city is in the picture deliberately: Utrecht is wired in via a
> `dutch_reuse_policy_mesh` edge. Demand-side public procurement is a coordinating
> force too."

### 3.5 — Rotor DC / Belgium: small, but the keystone

**Slide 9:**

```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run = 'rotor_dc_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

**Say this:**

> "Only three connections — the smallest bubble. So why does it matter? Because
> of *who* it connects. **Rotor DC** is the Brussels deconstruction company that
> the whole European reuse field treats as proof-of-concept: reuse done at
> commercial scale. The three edges are tiny but load-bearing:
> Rotor DC is a `directory_dealer` inside Opalis; Bellastock is Opalis's
> `programme_maintenance_partner`; and Rotor DC `colocation_evere` with its
> sister design practice Rotor.
>
> The point of this slide is methodological honesty: **a bubble's importance is
> not its edge count.** Three well-chosen, fully-evidenced edges put the single
> most influential reuse operator in Europe onto the map and, crucially, *onto
> Opalis* — which is about to become our main bridge."

---

## Act 4 — The bridges: where the magic (and the fragility) lives

**Say this:**

> "Five national clusters. On their own they're five islands. The most valuable
> work we did wasn't inside any bubble — it was the nine cross-bubble connections
> (plus follow-on quality-pass edges) *between* them. Let me show you the nodes
> that do double duty."

**Slide 10 — The bridge nodes (a node that lives in more than one bubble).**

```cypher
// Which actors appear across multiple research runs? Those are the bridges.
MATCH (n)-[r:VERBUNDEN_MIT_AKTEUR]-()
WHERE r.review_run IS NOT NULL
WITH n, collect(DISTINCT r.review_run) AS bubbles
WHERE size(bubbles) > 1
RETURN n.id AS bridge_node, size(bubbles) AS spans, bubbles
ORDER BY spans DESC, bridge_node;
```

**Say this, pointing at the top rows:**

> "Two nodes span *three* bubbles each, and they are the load-bearing walls of
> European reuse:
>
> - **Opalis** bridges France, Belgium (Rotor) and the cross-layer. It started
>   as a Belgian reclaimed-materials catalogue and became the de-facto
>   directory for the whole Franco-Belgian field. It is funded by Brussels
>   Environment — we have that as a `programme_funder_platform` edge — which
>   tells you something profound: *the connective tissue is publicly financed.*
>   The market didn't build the bridge; a government did.
>
> - **Madaster** bridges the Netherlands, Germany and the cross-layer. Where
>   Opalis catalogues *physical dealers*, Madaster catalogues *data* — material
>   passports. It links to EPEA as a `platform_family` and to Insert via a
>   `formal_partnership`. It's the data backbone the way Opalis is the physical
>   backbone.
>
> And **Cirkla** — the Swiss star — turns out to also reach outward, linking
> Sumami and useagain into the European frame. The strongest *national* hub is
> also a *continental* connector."

**Slide 11 — Degree ranking: who actually runs this network?**

```cypher
// Rank actors by how many distinct reuse partners they touch.
MATCH (n)-[r:VERBUNDEN_MIT_AKTEUR]-(m)
WHERE r.review_run IS NOT NULL
RETURN n.id AS actor, labels(n)[0] AS type, count(DISTINCT m) AS partners
ORDER BY partners DESC
LIMIT 10;
```

| actor | partners |
|---|---|
| cirkla | 11 |
| opalis | 7 |
| zrs_ingenieure | 4 |
| superuse_studios_2012architecten | 4 |
| bauteilboerse_hannover | 4 |
| useagain_bauteilclick | 4 |
| sumami | 4 |
| rotordc | 4 |
| haus_der_materialisierung | 4 |

**Say this:** *"This is a classic power-law — a few hyper-connected hubs, a long
tail of specialists. That's good news and bad news. Good: you can reach most of
the field through a handful of organisations. Bad: knock out Cirkla, Opalis or
Madaster and the continent fragments back into islands. **The European reuse
network is held together by maybe five organisations, two of which are
publicly funded.** That's the single most important sentence in this talk."*

**Slide 12 — Trace an actual path across borders.**

```cypher
// Can a Swiss component-shop reach a French research centre through the network?
MATCH p = shortestPath(
  (:Akteur {id:'useagain_bauteilclick'})-[:VERBUNDEN_MIT_AKTEUR*..8]-(:Akteur {id:'cstb'})
)
RETURN [n IN nodes(p) | n.id] AS hops, length(p) AS distance;
```

**The path this actually returns (4 hops):**
`useagain → restado → opalis → bellastock → cstb`

**Say this:** *"This is the 'so what'. A reclaimed-parts shop in Switzerland and
France's national building-science institute are not in the same bubble, were
researched weeks apart — and yet the graph connects them in four hops. And look
at the route: it leaves Switzerland through Restado, crosses the
**Restado→Opalis bridge** we built in the cross-bubble run, and lands in France
via Bellastock. The two hubs from the last slide, Opalis and Restado, are
literally the stepping stones. That path did not exist before the cross-bubble
work. We didn't just describe the network; by adding sourced cross-bubble edges
(and pruning unsupported ones), **we made the honest backbone traversable.**"*

---

## Act 5 — Reading the semantics: what the typing reveals

**Say this:**

> "Step back from the map and look at the *grammar*. We could have drawn one
> generic 'is connected to' edge everywhere. We didn't, and the typing now tells
> a story the topology alone can't."

**Slide 13 — Group the connection vocabulary into its underlying mechanisms.**

```cypher
// Collapse 40+ specific connection_kinds into the handful of real mechanisms.
MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
WHERE r.review_run IS NOT NULL
WITH r.connection_kind AS k, count(*) AS n
RETURN
  CASE
    WHEN k CONTAINS 'director' OR k CONTAINS 'listing' OR k CONTAINS 'supplier'
      THEN '1. Catalogue / directory (weak tie, high reach)'
    WHEN k CONTAINS 'research' OR k CONTAINS 'consortium' OR k CONTAINS 'programme' OR k CONTAINS 'lab'
      THEN '2. Research / standards (strong tie, makes reuse legitimate)'
    WHEN k CONTAINS 'partnership' OR k CONTAINS 'commissioner' OR k CONTAINS 'operator' OR k CONTAINS 'family'
      THEN '3. Formal / commercial (strong tie, moves real material)'
    WHEN k CONTAINS 'mesh' OR k CONTAINS 'ecosystem' OR k CONTAINS 'network' OR k CONTAINS 'peer'
      THEN '4. Ecosystem peer (medium tie, same scene)'
    ELSE '5. Other / lineage'
  END AS mechanism,
  sum(n) AS connections
ORDER BY connections DESC;
```

**What the query returns:**

| mechanism | connections |
|---|---|
| 5. Other / lineage | 21 |
| 2. Research / standards (strong tie) | 19 |
| 1. Catalogue / directory (weak tie, high reach) | 14 |
| 3. Formal / commercial (strong tie) | 7 |
| 4. Ecosystem peer (medium tie, same scene) | 5 |

**Say this:**

> "Look at the distribution and a clear story falls out.
>
> After the evidence audit, the mix shifted: **research/standards** (19) and
> **other/lineage** (21) lead — still a blend of discovery and commitment.
> **Catalogue** listings (14) and **ecosystem-peer** ties (5) remain the weak
> ties that help strangers *find* each other.
>
> The strong commercial layer — **formal/commercial** (7) — is still the
> smallest bucket: signed consortia, brand operators, project commissioners.
> These make reuse *legitimate* and move *real material and money*.
>
> That ratio is the diagnostic. The European reuse field is **rich in discovery
> infrastructure and thin in binding commitment**. Lots of ways to find a
> partner; comparatively few formalised, money-moving relationships. That's not
> a flaw to hide — it's precisely the maturity gap the next decade has to close,
> and the graph shows you exactly where: convert weak ties into strong ones."

**Slide 14 — The honesty audit (this is what makes it trustworthy).**

```cypher
// Every reuse connection, with its proof. No row should have a null URL.
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run IS NOT NULL
RETURN a.id AS from, b.id AS to,
       r.connection_kind AS kind,
       r.evidence_confidence AS confidence,
       r.evidence_url AS source
ORDER BY confidence, from;
```

**Say this:** *"This is the slide I'd defend in front of a skeptic. Sixty-six
directed tagged connections — every one with a source URL, every one rated
`belegt` or `teilweise_belegt` (57 fully evidenced, 9 partial). We don't hide
the weak ones — we *label* them. A reuse network you can't audit is just a nice
drawing. This one you can click through, link by link."*

---

## Act 6 — Closing: the network is the product

**Say this:**

> "Let me bring it home.
>
> We started with a coordination problem: working materials thrown away because
> supply can't find demand in time. We modelled the *coordinators* — 66 directed
> sourced connections (114 fully `belegt`) across Switzerland, Germany, France,
> the Netherlands and Belgium — and three findings fell out:
>
> **One. Reuse coordination has a shape, and the shape is hubs-and-bridges.** A
> handful of organisations — Cirkla, Opalis, Madaster — carry the whole field.
> That's efficient and dangerous in equal measure.
>
> **Two. The bridges are the scarce resource.** Inside each country, the network
> is decent. *Between* countries, it hangs on a few nodes, and two of the most
> important — Opalis and Madaster's public-facing layers — are publicly funded.
> If you want to accelerate European reuse, you don't fund more marketplaces.
> You fund the *bridges*.
>
> **Three. Typed, sourced relationships turn a map into an argument.** Because
> every edge knows *what kind* of tie it is and *where the proof lives*, the
> graph can answer questions a flat directory can't: where is this country
> weak, which idea came from where, can these two strangers reach each other.
>
> The deliverable was never the diagram. The deliverable is a *queryable,
> auditable model of how reuse actually coordinates itself* — and the news it
> delivers is that the system works, but it's balanced on a handful of bridges.
> Protect the bridges."

**Closing slide — the one-query summary of the whole thesis.**

```cypher
// The story in one screen: bubbles as clusters, bridges as the nodes that span them.
MATCH (n)-[r:VERBUNDEN_MIT_AKTEUR]-()
WHERE r.review_run IS NOT NULL
WITH n, collect(DISTINCT r.review_run) AS bubbles, count(DISTINCT r) AS deg
RETURN n.id AS actor,
       deg AS connections,
       size(bubbles) AS bubbles_spanned,
       CASE WHEN size(bubbles) > 1 THEN '🌉 BRIDGE' ELSE 'local' END AS role
ORDER BY bubbles_spanned DESC, connections DESC
LIMIT 20;
```

> *"Twenty rows. The ones marked BRIDGE are the load-bearing walls of European
> reuse. Everything else depends on them. Thank you."*

---

## Appendix A — Speaker's cheat-sheet (numbers to have ready)

- **Scope:** 66 directed / 132 undirected tagged reuse connections, 10
  `review_run` tags, 5 countries (CH · DE · NL · FR · BE).
- **Graph (live):** 2,263 nodes / 15,060 rels · 17,323 elements.
- **VMA evidence:** 114 `belegt` · 18 `teilweise_belegt` (undirected) · 0 missing URL.
- **Top hubs by partners:** Cirkla 11 · Opalis 7 · ZRS/Superuse/Bauteilbörse Hannover/useagain/Sumami/RotorDC/HdM 4 each.
- **Bridge nodes (span ≥2 bubbles):** Opalis & Madaster span 3; Cirkla,
  Bellastock, Concular, Restado, Insert, useagain, Sumami, RotorDC,
  Circular Berlin, City of Utrecht, Kunst-Stoffe, Material Mafia,
  Madaster/EPEA, Circular Hub Zürich span 2.
- **Evidence rule:** every tagged edge carries `evidence_url` +
  `evidence_confidence` (`belegt` / `teilweise_belegt`); 0 tagged edges missing URL.
- **Dedup / audit:** bidirectional pairs collapsed where sourced; Tier-1/Tier-2
  unsupported mesh edges removed per `EVIDENCE_AUDIT.md`; graph **2,263 nodes /
  15,060 relationships** (post-F1 rau merge, read-cypher 2026-06-06).

## Appendix B — Bubble → `review_run` tag map (for live filtering)

| Bubble (say) | `review_run` value (paste) |
|---|---|
| Switzerland | `swiss_reuse_bubble_2026_06_05` |
| Germany | `germany_reuse_bubble_2026_06_05` |
| France | `france_reuse_bubble_2026_06_05` |
| Netherlands | `netherlands_reuse_bubble_2026_06_05` |
| Rotor DC / Belgium | `rotor_dc_reuse_bubble_2026_06_05` |
| Cross-bubble bridges | `cross_bubble_extension_2026_06_06` |
| Agent-06b actor networks | `agent_06b_non_bubble_actor_networks_2026_06_06` |
| Post-quality actor upgrades | `post_quality_p06_02_2026_06_06` |
| Quality pass Q05 | `quality_pass_q05_2026_06_06` |
| Remediation wave-2 R04 | `remediation_wave2_r04_2026_06_06` |

## Appendix C — Three "what-if" probes for live Q&A

```cypher
-- Q: "What breaks if Opalis disappears?" (count its connections)
MATCH (:Akteur {id:'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(m)
RETURN m.id AS would_lose_a_link, r.connection_kind AS via;
```

```cypher
-- Q: "Show me only the strongly-proven (belegt) backbone."
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run IS NOT NULL AND r.evidence_confidence = 'belegt'
RETURN a, r, b;
```

```cypher
-- Q: "Which connections are still only partially evidenced (our to-do list)?"
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run IS NOT NULL AND r.evidence_confidence = 'teilweise_belegt'
RETURN a.id AS from, b.id AS to, r.connection_kind AS kind, r.evidence_url AS source
ORDER BY from;
```
