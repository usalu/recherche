# Residual orphaned sources (after reconnect + dedup)

After Phase F (rel cleanup), source reconnection (+580 `HAS_SOURCE_LINK`), and
the dedup merge (-2,442 duplicate nodes), the orphan source count fell from
~4,492 to **2,096** disconnected `Quelle`/`ExternalLink` nodes (plus 16 non-source
stray nodes handled in hygiene).

## What remains

| quelltyp | orphans |
| --- | --- |
| external_link | 1,565 |
| external_reference | 365 |
| research_markdown | 164 |
| external_link_from_actor_registry | 2 |
| **total** | **2,096** |

## Where they came from

These were a harvested URL pool attached to the now-deleted `DataIssue` /
`DossierEntityTarget` meta-layers (round 1) or to candidate-URL arrays. Their
specific claim linkage was never modeled as `BELEGT_IN`, and the authoritative
`_neo4j/processed/` records only document 457 distinct URLs (the 580 we could
reconnect). The rest are not present in the canonical processed source-of-truth.

## What they refer to (top domains)

Legitimate, high-value references - they are not junk:

- Standards: `iso.org`, `standards.iteh.ai`, `dibt.de`, `dgnb.de`
- Regulation: `gesetze-im-internet.de`, `eur-lex.europa.eu`, `berlin.de`, `bbsr.bund.de`, `baua.de`, `umweltbundesamt.de`
- Reuse platforms / tools: `rotordb.org`, `opalis.eu`, `concular.de`, `madaster.com`, `cirkla.ch`, `oneclicklca.com`, `zirkular.net`
- Research / institutions: `sciencedirect.com`, `zrs.berlin`, `bellastock.com`, `bamb2020.eu`, `hausdermaterialisierung.org`

## Decision taken: research in-graph linkage and reconnect

Per your instruction, no orphan was deleted. Instead the orphans were
reconnected using the strongest available **in-graph** signal - the node id
provenance, where ids of the form `q_<case>_s<N>` directly encode the case
markdown Quelle (`q_<case>_md`) they were extracted from.

- **+194 reconnected** to 43 parent cases via `HAS_SOURCE_LINK` (id signal).
- Combined with the earlier 580 url-index reconnections and 2,442 dedup merges,
  the orphan pool fell from ~4,492 to **1,902**.

## Remaining 1,902 - why they can't be safely linked from the graph alone

| id kind | count | why unlinkable in-graph |
| --- | --- | --- |
| `q_url_<hash>` opaque | 1,563 | id is a hash of the URL; carries no case/entity reference |
| other (`q_ext_*`, research_markdown, ...) | 330 | no case-encoding id; domain is generic |
| `q_<case>_s<N>` (parent case not connected) | 7 | parent case itself is not in the connected graph |
| `q_ext_<domain>_<slug>` | 2 | domain only |

No entity node carries a `url`/`website` property (removed in round 1), so the
only remaining signal is **domain overlap** with connected sources - which is
unsafe for the dominant generic domains here (`sciencedirect.com`, `iso.org`,
`gesetze-im-internet.de`, ...): a shared domain does **not** mean the same claim.
Linking by domain would fabricate evidence links, violating the
"never lose / never fake an evidence link" principle.

**These 1,902 need data-driven reconnection**, not graph-topology guessing: the
authoritative "which entity/claim each URL backs" lives in the source deliveries
(actor/bauteilbörse enrichment under `intake/`, archived research dossiers), and
should be re-attached through the normal intake->processed->import workflow rather
than this cleanup. They are kept intact (no data lost) pending that import.
