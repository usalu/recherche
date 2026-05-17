# Batch 4 — UK + unidentified

**Decision after research:** promote `p_granby_workshop` to full Projekt. For `p_obk_27`: identify or delete.
**Project count:** 2.
**Common reference:** see [README.md](README.md). Comparable UK case: [`55_Great_Suffolk_Street_London.md`](../../../../_archive/research/gebaeude/55_Great_Suffolk_Street_London.md), [`Holbein_Gardens_London.md`](../../../../_archive/research/gebaeude/Holbein_Gardens_London.md).

---

### 1. `p_granby_workshop` — Granby Workshop (Liverpool)

**Existing actor links:** Lewis Jones.

**Likely identity:** **Granby Workshop** — a social-enterprise design studio in Liverpool's Granby Four Streets, spun out of the **Assemble** collective's Turner Prize-winning 2015 community-led housing-restoration project. Lewis Jones = one of the Granby Workshop founders. The Workshop makes ceramics + door handles from salvaged materials.

**To research:**
- [ ] Disambiguate: is the stub about **Granby Workshop** the studio, or the broader **Granby Four Streets** housing project?
- [ ] Most likely: the Workshop's craft-from-salvage activity (mantelpieces, door handles, ceramics) **and** the Granby Four Streets reuse-led housing restoration (the Turner Prize project)
- [ ] Address (Cairns Street, Liverpool L8 area)
- [ ] Founding year (Workshop: 2015; Four Streets restoration: 2013–2017+)
- [ ] Materials reused: bricks from demolition, tile/marble fragments, doors, fireplace surrounds
- [ ] Architects: Assemble (London-based collective)
- [ ] Bauherr: Granby Four Streets Community Land Trust (CLT)
- [ ] Sources: assemblestudio.co.uk/projects/granby-four-streets, granbyworkshop.co.uk, Turner Prize 2015 press

---

### 2. `p_obk_27` — OBK 27

**Existing actor links:** Cyril Pressacco, Thibaut Barrault.

**Likely identity:** Both actors are French architects — Cyril Pressacco + Thibaut Barrault = **Barrault Pressacco** Paris architecture firm (known for reuse + raw materials, e.g. their Saint-Denis pierre-de-taille housing). "OBK 27" plausibly = a building or address — possibly **Olympus Building Kapital 27** / **Oberkampf 27** (Paris 11e: 27 rue Oberkampf) / similar.

**To research:**
- [ ] Decode "OBK 27" — most likely **27 rue Oberkampf** (Paris 11e), since that's the standard French architectural shorthand and matches Barrault Pressacco's geography
- [ ] If confirmed: building type, reuse strategy, dates
- [ ] If NOT identifiable from any source: **delete** the stub (rec: keep as last resort)
- [ ] Sources: barrault-pressacco.com, archdaily.com search "Barrault Pressacco", AMC magazine

**Fallback decision:** if the project cannot be confidently identified after a reasonable research effort, document the negative finding and the stub can be deleted via a follow-up prompt. Do not invent details.

---

## Output

For Granby Workshop: one archive + one JSONL.
For OBK 27: only emit files if identification is confident. Otherwise produce a `_neo4j/intake/inbox/stub_promotion/p_obk_27.NEGATIVE_FINDING.md` documenting what was checked, and the stub can be DETACH DELETE'd later.
