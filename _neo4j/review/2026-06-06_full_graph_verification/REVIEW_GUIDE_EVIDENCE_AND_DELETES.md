# Review Guide — IER Evidence Patch & DELETE Batch

Plain-language explainer for **checklist sections 1 and 2** of the Internet Evidence Recovery (IER) campaign.
Nothing here has been applied to Neo4j yet.

**Context:** [IER Campaign Report](reports/IER_CAMPAIGN_REPORT.md) — campaign goal was to recover missing source URLs and quotes from the public web, then mark what is truly proven vs. what should be removed.

---

## Section 1 — Evidence patch (184 operations)

**Patch file:** [`patches/ier_evidence_recovery.patch.jsonl`](patches/ier_evidence_recovery.patch.jsonl)  
**Dry-run report:** [`apply_reports/ier_evidence_recovery.patch.apply_report.md`](apply_reports/ier_evidence_recovery.patch.apply_report.md)

### What it does

This patch **adds or fixes evidence on existing nodes and relationships**. It does **not** delete anything, merge nodes, or create new graph elements.

Think of it as attaching footnotes: “here is the web page, and here is the exact quote that supports this claim.”

### What gets updated

| Operation | Count | What changes |
|---|---:|---|
| `set_node_properties` | 172 | **Actor nodes** (`:Akteur`) gain `primary_source_url`, `source_quote`, and `review_run` |
| `set_rel_properties` | 12 | **Relationships** (all `ERFUELLT_NACHWEIS` — “fulfills proof/requirement”) gain `evidence_url`, `evidence_quote`, `evidence_confidence`, `evidence_basis`, and `review_run` |

**Sources merged into this patch:** IER-P0 (proof-type links), IER-A1 (actor homepages), IER-C12 (actor domain recovery). See the campaign report for shard detail.

**Graph size after apply:** unchanged — **2,263 nodes / 15,060 relationships** (same as today).

### Dry-run status

Dry-run **passed** (2026-06-07):

- 184 records loaded, 0 errors
- 172 nodes would update, 12 relationships would update
- Nothing rejected or flagged for review

### How to apply (when ready)

From the repo root:

```bash
# 1. Dry-run (safe preview — default)
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/ier_evidence_recovery.patch.jsonl

# 2. Live apply (only after you are satisfied with the dry-run)
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/ier_evidence_recovery.patch.jsonl --confirm "APPLY ier_evidence_recovery.patch.jsonl TO mit-bestand"
```

The `--confirm` phrase must match exactly (patch filename + database name).

### What to check before approving

Sample a handful of lines from the patch file (start, middle, end):

- **URLs look legitimate** — real organisation sites, norm pages, or project pages; not pipeline tokens like `processed` or `archive`.
- **Quotes are verbatim** — text copied from the fetched page, not paraphrased.
- **The quote supports the claim** — for actors, the entity name appears on the page; for relationships, the quote connects the two endpoints (proof type ↔ requirement, etc.).
- **Spot-check odd cases** — e.g. a `source_quote` that is mostly HTML junk (see line 13 in the patch: `3xn`) may need a manual fix before apply.

This batch is **non-destructive** and lower risk than deletes, but bad URLs or quotes will pollute the graph’s evidence layer.

---

## Section 2 — DELETE batch (214 edges)

**Patch file:** [`patches/ier_evidence_recovery_deletes.patch.jsonl`](patches/ier_evidence_recovery_deletes.patch.jsonl)

### What it does

This patch **removes 214 relationships** that IER agents could not prove with internet evidence. Each line is a `delete_rel` operation.

### Why these edges are proposed for deletion

Common pattern across agents: **no real pairwise proof**.

An edge is kept only when a fetched web page names **both** endpoints (e.g. both the actor and the project, or both actors in a connection). If the page mentions only one side, or the link was inferred from import metadata / placeholder tokens / generic compendia, the edge is marked **UNSUPPORTED** and proposed for deletion.

| Agent | Deletes | Rationale (short) | Full report |
|---:|---:|---|---|
| **B1** | 97 | Geo-import `BETEILIGT_AN` (actor ↔ project): dossier URLs often confirm the **project** but not the specific **actor** on that project | [ier_b1_report.md](reports/ier_b1_report.md) |
| **C3** | 60 | `VERBUNDEN_MIT_AKTEUR` (actor ↔ actor): had no evidence URL; web search + fetch could not pass strict two-endpoint gate | [ier_c3_report.md](reports/ier_c3_report.md) |
| **A2** | 49 | Tier-A URL-backed rels: existing `basis_ref` fetched, but quote does not name both endpoints (e.g. generic schadstoff compendia, regulation pages that never mention the project) | [ier_a2_report.md](reports/ier_a2_report.md) |
| **C5** | 7 | Software / participation residual: no page names both the project/component **and** the software tool | [ier_c5_report.md](reports/ier_c5_report.md) |
| **B2** | 1 | `HAT_BAUWERK`: link to an **aggregate donor stub** (not a discrete building) | [ier_b2_report.md](reports/ier_b2_report.md) |
| **Total** | **214** | | |

### Relationship types affected

| Type | Deletes | Meaning (plain) |
|---:|---|---|
| `BETEILIGT_AN` | 99 | Actor participated in project |
| `VERBUNDEN_MIT_AKTEUR` | 60 | Actor connected to another actor |
| `ERFORDERT_NACHWEIS` | 19 | Project requires a proof document |
| `TRIGGERS_REGULIERUNGSFRAGE` | 12 | Project triggers a regulation question |
| `HAT_SCHADSTOFFRISIKO` | 8 | Material/component has contaminant risk |
| `ERFORDERT_SCHADSTOFFPRUEFUNG` | 8 | Project requires contaminant testing |
| `NUTZT_SOFTWARE` | 7 | Entity uses a software tool |
| `HAT_BAUWERK` | 1 | Project linked to donor/receiver building |

After apply (if approved): **2,263 nodes / 14,846 relationships** (−214 edges).

### Human-gated — do NOT auto-apply

Unlike the evidence patch, **deletes are irreversible** (unless you re-import the edge from scratch with new evidence). The campaign explicitly marks this file as **human-gated**. Review first; apply only after explicit approval.

### What to check before approving

- **Known-good edges** — Do you personally know any of these connections are real? If yes, do not delete; instead find a source URL and add an evidence patch.
- **Too aggressive?** — B1 deletes are the largest group (97). Many are “project on page, actor not named.” That may be correct (inferred link) or too harsh (consortium page that implies participation). Spot-check projects you care about.
- **Regulation / schadstoff cluster (A2)** — 49 deletes include edges where a generic reference page was stored as evidence but never names the specific project or contaminant link. Confirm you are OK losing those weak links.
- **VMA network (C3)** — 60 actor–actor deletes. Check whether any removed tie is structurally important for reuse-network analysis.
- **Sample the `reason` field** — Each delete line cites the agent ID (e.g. `IER-B1 … UNSUPPORTED — DELETE`) so you can trace back to the ledger row.

### How to apply IF approved

Same tool, **separate file**:

```bash
# 1. Dry-run first
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/ier_evidence_recovery_deletes.patch.jsonl

# 2. Live apply (only after human approval)
python _scripts/apply_neo4j_review_patch.py --patch _neo4j/review/2026-06-06_full_graph_verification/patches/ier_evidence_recovery_deletes.patch.jsonl --confirm "APPLY ier_evidence_recovery_deletes.patch.jsonl TO mit-bestand"
```

Recommended order: apply **Section 1 (evidence)** first, then review deletes again with the improved graph. Deletes do not depend on the evidence patch, but separating the steps makes rollback easier to reason about.

---

## Quick reference

| Item | Evidence patch | DELETE batch |
|---|---|---|
| Ops | 184 | 214 |
| Destructive? | No | Yes |
| Auto-apply? | Ready after your review | **No — human-gated** |
| Expected PROVEN lift | +539 element rows → **93.74%** (see campaign report) | −214 element rows (pruned unsupported) |

**Campaign summary:** [IER_CAMPAIGN_REPORT.md](reports/IER_CAMPAIGN_REPORT.md)
