# Reuse, Read as a Network

### A short, spoken deck — 7 slides, one argument

> **The argument in one line:** every national reuse scene is building the *same*
> coordination machine — but each one **leads with a different part of it**, and
> you can see which part straight from the graph.
>
> Each slide = one thing to **say** + one Cypher query to **show**. Built from
> **66 directed** evidence-tagged reuse connections (**132** in undirected view;
> **114** with `evidence_confidence='belegt'`) across 5 countries in `mit-bestand`
> (live **2,263 nodes / 15,060 rels**, read-cypher 2026-06-06). Every edge
> carries its source.

---

## Slide 1 — Open on the whole thing

**Say:**
> "Construction is Europe's biggest waste stream by mass — and most of what we
> demolish still works. Reuse isn't a *materials* problem, it's a *coordination*
> problem: the beam exists, the demand exists, the connective tissue doesn't.
> So we mapped the connective tissue — the platforms, directories, labs and
> deconstruction firms — across five countries. Here is all of it at once."

**Show:**
```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run IS NOT NULL
RETURN a, r, b;
```

> *Point:* "Dense national clumps, joined by a few long edges. The rest of this
> talk is one idea about those clumps, and one idea about those edges."

---

## Slide 2 — The one idea: a shared value chain

**Say:**
> "Strip away the logos and every country is assembling the same seven-step
> chain. A donor building is **audited**, its parts get a **passport**, they're
> **stored**, **listed**, **matched** to a new project, **reused**, and the data
> **feeds back**. Nobody is missing steps. What differs is the **centre of
> gravity** — which step a country leads with. That single choice explains the
> whole shape of each network."

**Show (the chain, as the slide):**
```text
donor building → audit/screening → material passport → storage/brokerage
   → marketplace listing → match supply&demand → reuse → data feeds back
```

> *Semantic point:* "We didn't draw one generic 'connected to' line. We typed
> every link — a catalogue listing is a weak claim; a signed consortium is a
> strong one. The typing is what lets the graph *argue*, not just *display*."

---

## Slide 3 — Portrait A: Switzerland, the **star** (centralised)

**Say:**
> "Switzerland is the cleanest shape in the data: a star. One node — **Cirkla**,
> 'the Swiss re-use network' — touches almost everyone. Eleven partners, the most
> connected node in the whole project. It's centralised on purpose: Cirkla *is*
> the national directory, publicly backed by the federal environment office.
> The risk is written into the shape — remove the centre and the field
> shatters. Switzerland's reuse coordination has a single point of failure, and
> its name is Cirkla."

**Show:**
```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run = 'swiss_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

> *One detail to land it:* "Notice the edge to a *tool*, Cirkla-Scan, and to
> Zirkular's K.118 project. The hub doesn't just list members — it ships
> software and owns the field's flagship building. A directory that became
> infrastructure."

---

## Slide 4 — Portrait B: Netherlands, the **language** (distributed)

**Say:**
> "Now the opposite pole. The Netherlands has no Cirkla — no single umbrella.
> It's distributed and densely meshed. What holds it together isn't an
> organisation, it's a **shared vocabulary**: 'harvesting', 'donor buildings',
> 'urban mining', 'material passport'. When everyone names the problem the same
> way, clients, demolishers and architects can coordinate without a central hub.
> The Netherlands proves you can centralise on *concepts* instead of on an
> institution."

**Show — and zoom into the single most beautiful edge:**
```cypher
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]-(b)
WHERE r.review_run = 'netherlands_reuse_bubble_2026_06_05'
RETURN a, r, b;
```

> *The killer example (point at this edge):* "Superuse Studios invented the
> *Oogstkaart* — the 'harvest map' — in 2012, then sold it to New Horizon in
> 2019. We typed that link `oogstkaart_lineage`. It's not a partnership; it's
> **inheritance** — one firm invented a method, another scaled it. The graph
> can carry the genealogy of an *idea*, not just a contract. That's what typed
> edges buy you."

---

## Slide 5 — The semantic payoff: typing catches truth

**Say:**
> "Two quick cases where the typing forced us to be honest. First: Restado and
> Concular kept colliding in Germany. The source settles it — 'restado ist eine
> Marke der Concular GmbH'. They're not peers; one is a company, the other its
> brand. We typed it `marketplace_brand_operator`, not 'partnership'. Second:
> France's whole scene hangs off a *regulation* — the PEMD pre-demolition
> diagnostic — which turns a building from 'future waste' into a documented
> inventory *before* the excavator arrives. Different countries, different
> leading layer; same chain."

**Show — the vocabulary, collapsed to the mechanisms that matter:**
```cypher
MATCH ()-[r:VERBUNDEN_MIT_AKTEUR]->()
WHERE r.review_run IS NOT NULL
RETURN
  CASE
    WHEN r.connection_kind CONTAINS 'director' OR r.connection_kind CONTAINS 'listing'
         OR r.connection_kind CONTAINS 'supplier' OR r.connection_kind CONTAINS 'mesh'
         OR r.connection_kind CONTAINS 'peer'      THEN 'DISCOVERY  (weak tie: find each other)'
    WHEN r.connection_kind CONTAINS 'research' OR r.connection_kind CONTAINS 'consortium'
         OR r.connection_kind CONTAINS 'programme' OR r.connection_kind CONTAINS 'partnership'
         OR r.connection_kind CONTAINS 'operator' OR r.connection_kind CONTAINS 'commissioner'
                                                   THEN 'COMMITMENT (strong tie: build/move material)'
    ELSE 'OTHER / lineage'
  END AS tie_type,
  count(*) AS links
ORDER BY links DESC;
```

> *Point:* "The field is rich in **discovery** ties and thin in **commitment**
> ties. Lots of ways to find a partner; few formalised, money-moving deals.
> That ratio *is* the maturity gap — and it tells you the next decade's job:
> convert weak ties into strong ones."

---

## Slide 6 — The bridges: two organisations hold the continent

**Say:**
> "Now the long edges. Five national scenes are five islands until something
> spans them. Two nodes do the spanning. **Opalis** — the Belgian-French
> directory of physical dealers — and **Madaster** — the cross-border *data*
> registry. One bridges the physical world, one bridges the data world. And the
> tell: both are publicly funded. The market didn't build the bridges; the
> public sector did."

**Show — who spans more than one bubble:**
```cypher
MATCH (n)-[r:VERBUNDEN_MIT_AKTEUR]-()
WHERE r.review_run IS NOT NULL
WITH n, collect(DISTINCT r.review_run) AS bubbles
WHERE size(bubbles) > 1
RETURN n.id AS bridge, size(bubbles) AS spans
ORDER BY spans DESC, bridge
LIMIT 8;
```

> *Proof it's traversable now:* a Swiss parts-shop reaches France's building-
> science institute in 4 hops — `useagain → restado → opalis → bellastock →
> cstb` — a path that did **not exist** before we added the bridge edges.
> ```cypher
> MATCH p = shortestPath(
>   (:Akteur {id:'useagain_bauteilclick'})-[:VERBUNDEN_MIT_AKTEUR*..8]-(:Akteur {id:'cstb'}))
> RETURN [n IN nodes(p) | n.id] AS hops;
> ```

---

## Slide 7 — Synthesis & close

**Say:**
> "So here's the whole talk in one table. Same chain everywhere; different
> centre of gravity."

| Country | Leads with | Network shape |
|---|---|---|
| **Switzerland** | a **network/directory** (Cirkla) | centralised **star** |
| **Netherlands** | a **shared language** (harvesting, donor buildings) | distributed **mesh** |
| **Germany** | **standards & data** (DIN SPECs, passports) | layered, marketplace-led |
| **France** | **regulation & trust** (PEMD, insurance) | polycentric |
| **Belgium / Rotor** | **proof of practice** (commercial deconstruction) | small, keystone |

**Close:**
> "Three findings. **One:** reuse coordination has a shape — hubs and bridges —
> and it's efficient *and* fragile. **Two:** the scarce resource isn't
> marketplaces, it's the *bridges between* them — and the most important ones
> are public. Fund the bridges. **Three:** because every edge is *typed* and
> *sourced*, this isn't a picture — it's an argument you can click through, link
> by link. The deliverable was never the diagram. It's a queryable model of how
> reuse coordinates itself — and the news is: it works, but it's balanced on a
> handful of bridges. Protect them. Thank you."

---

### Backup — three Q&A probes

```cypher
-- "What breaks if Opalis disappears?"
MATCH (:Akteur {id:'opalis'})-[r:VERBUNDEN_MIT_AKTEUR]-(m)
RETURN m.id AS would_lose_link, r.connection_kind AS via;
```
```cypher
-- "Show only the strongly-proven backbone."
MATCH (a)-[r:VERBUNDEN_MIT_AKTEUR]->(b)
WHERE r.review_run IS NOT NULL AND r.evidence_confidence = 'belegt'
RETURN a, r, b;
```
```cypher
-- "Who are the real hubs?"
MATCH (n)-[r:VERBUNDEN_MIT_AKTEUR]-(m)
WHERE r.review_run IS NOT NULL
RETURN n.id AS actor, count(DISTINCT m) AS partners
ORDER BY partners DESC LIMIT 6;
```

> Full long-form version with all six bubbles: `PRESENTATION_REUSE_NETWORKS.md`.
