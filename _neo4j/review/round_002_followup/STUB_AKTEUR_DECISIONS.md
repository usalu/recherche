# Stub Akteur decisions

**Status:** decisions written, **no execution yet** — per your instruction, removals/merges happen later via prompt.

Each entry has my chosen decision and a verification Cypher you can run before executing. The 16 stub Akteure are the degree-0 and degree-1 nodes carrying `Akteur` label.

---

## DELETE (2)

These are cryptic short slugs with no source-scope, no degree, no identifiable real entity. Recommend `DETACH DELETE`.

| id | decision | reason |
|---|---|---|
| `bizh` | DELETE | Unknown abbreviation; degree 0; no source_scope; no plausible expansion found |
| `dare_gmbh` | DELETE | Generic "GmbH" stub; degree 1; cannot disambiguate which DARE firm; no source_scope |

**Verify before delete:**
```cypher
MATCH (a:Akteur {id: 'bizh'}) OPTIONAL MATCH (a)-[r]-(x)
RETURN a.name, a.source_scope, type(r), x.id, x.name;

MATCH (a:Akteur {id: 'dare_gmbh'}) OPTIONAL MATCH (a)-[r]-(x)
RETURN a.name, a.source_scope, type(r), x.id, x.name;
```

If the result row count is what you expect (≤ 1 rel each), delete:
```cypher
MATCH (a:Akteur) WHERE a.id IN ['bizh', 'dare_gmbh'] DETACH DELETE a;
```

---

## MERGE (3)

These are name-variant duplicates of canonical Akteure already in the graph. Recommend `canonicalize_node` (redirect all rels onto the canonical id, then delete the duplicate).

| duplicate id | canonical id | reason |
|---|---|---|
| `rotor_vzw` | `rotor_asbl_vzw` | Both are the Rotor cooperative. Canonical is the bilingual full form already in the graph. Alternatives `rotor_dc` / `rotordc` are the **deconstruction company arm** — keep those separate. |
| `zirkular_cirkla` | `zirkular_gmbh` | Both refer to Zirkular GmbH (Basel reuse-planning company). Canonical = the legal entity form. `cirkla` is a typo variant. |
| `zusammenkunft_berlin` | (keep — not a duplicate) | I initially flagged it as a merge candidate but discovery showed no other `zusammenkunft*` node in the graph. **Decision reverted to KEEP.** |

**Verify before merge:**
```cypher
// Show all rels carried by the duplicates:
MATCH (dup:Akteur) WHERE dup.id IN ['rotor_vzw', 'zirkular_cirkla']
OPTIONAL MATCH (dup)-[r]-(x)
RETURN dup.id AS duplicate, type(r) AS rel, x.id AS endpoint, x.name AS endpoint_name
ORDER BY dup.id;

// Show what the canonicals already have:
MATCH (canon:Akteur) WHERE canon.id IN ['rotor_asbl_vzw', 'zirkular_gmbh']
OPTIONAL MATCH (canon)-[r]-(x)
RETURN canon.id AS canonical, type(r) AS rel, count(*) AS n
ORDER BY canonical, rel;
```

Then merge via the apply tool's `merge_node` op (it handles rel redirection + alias absorption automatically):
```jsonl
{"op": "merge_node", "from": "rotor_vzw",        "to": "rotor_asbl_vzw", "reason": "Akteur dedup", "severity": "LOW"}
{"op": "merge_node", "from": "zirkular_cirkla",  "to": "zirkular_gmbh",  "reason": "Akteur dedup", "severity": "LOW"}
```

---

## KEEP (11)

All real entities, sparsely connected but worth keeping. Will gain edges naturally as round 003 archive files reference them.

| id | degree | reason to keep |
|---|---:|---|
| `glasfischer_glastec` | 0 | Real Swiss/German glass-tech company |
| `heinrich_boell_stiftung` | 0 | Real Heinrich-Böll-Stiftung — frequently relevant to reuse-policy discussions |
| `koimo_development` | 0 | Real Berlin developer |
| `mehr_als_wohnen` | 0 | Genossenschaft "Mehr als wohnen" Zürich — real, well-known Bauherr |
| `stiftung_habitat` | 0 | Stiftung Habitat Basel — real housing foundation |
| `citydev_brussels` | 1 | Brussels public developer |
| `denkstatt` | 1 | Austrian sustainability consultancy |
| `edith_maryon_stift` | 1 | Stiftung Edith Maryon (CH) — well-known land-trust + reuse foundation |
| `eitel_partner` | 1 | Real architecture firm |
| `gibbins_architekten` | 1 | Swiss architecture firm |
| `kunst_stoffe_ev` | 1 | Kunst-Stoffe e.V. Berlin — known reuse association |
| `zusammenkunft_berlin` | 1 | ZUsammenKUNFT Berlin eG — real cooperative; reverted from merge to keep |

**Verify still in graph:**
```cypher
MATCH (a:Akteur) WHERE a.id IN [
  'glasfischer_glastec','heinrich_boell_stiftung','koimo_development',
  'mehr_als_wohnen','stiftung_habitat','citydev_brussels','denkstatt',
  'edith_maryon_stift','eitel_partner','gibbins_architekten',
  'kunst_stoffe_ev','zusammenkunft_berlin'
]
OPTIONAL MATCH (a)-[r]-()
RETURN a.id, a.name, count(r) AS degree
ORDER BY degree, a.id;
```

---

## Combined verification — current state of all 16

Run this to see the full picture of stub Akteure before any removal:
```cypher
MATCH (a:Akteur)
OPTIONAL MATCH (a)-[r]-()
WITH a, count(r) AS deg
WHERE deg <= 1
RETURN a.id AS id, a.name AS name, deg AS degree,
       coalesce(a.source_scope, '<null>') AS scope
ORDER BY deg, a.id;
```

Expected output: 16 rows. If the count drops below 16 in the future, something has changed — re-audit.
