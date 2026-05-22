# Agent S6 — audit & sign-off

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.**

You are agent S6 of 6 — the final agent. Your job: **prove the work happened, surface every residual, and produce the canonical end-state report.**

You run LAST. Every other agent's done flag must exist before you start. You do not mutate the graph except to MERGE `:DataIssue` nodes summarising findings, and you write the `STAGE_S6_AUDIT_DONE.flag`.

---

## §1 Mission

1. **Run the cross-cutting invariant check** — every QV1–QV10 from [QUELLE_REMEDIATION_PLAN.md §8](../QUELLE_REMEDIATION_PLAN.md).
2. **Roll up `:DataIssue` counts** — by kind, severity, top-N nodes by issue density.
3. **Compute the comparative metrics** — `source_curated` edges before vs. after, verification distribution, trust-score distribution.
4. **Identify residuals** — every category of unfinished work, with concrete projects/edges named.
5. **Produce `_neo4j/FINAL_QUELLE_AUDIT.md`** with the full breakdown.
6. **Install the CI gate** at `_scripts/validate_no_text_content.py` so future ingestion can never re-introduce the bug.
7. **Sign off** by writing `STAGE_S6_AUDIT_DONE.flag`.

---

## §2 Schema delta

You write only:
- New `:DataIssue` nodes with `found_by='s6_audit'` for any cross-cutting finding that isn't already covered by S2/S3's kinds (e.g., `node_with_no_source`).
- `STAGE_S6_AUDIT_DONE.flag`.
- `_neo4j/FINAL_QUELLE_AUDIT.md`.
- `_scripts/validate_no_text_content.py`.

You do NOT touch any other node or edge property.

---

## §3 Pre-flight (mandatory; abort if any fails)

```bash
# Required done flags
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s1_url_extractor/PHASE_S1_DONE.flag
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s2_url_prober/PHASE_S2_DONE.flag
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s3_content_verifier/PHASE_S3_DONE.flag
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s4_schema_cleanup/PHASE_S4_DONE.flag
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s5_visibility/PHASE_S5_DONE.flag
```

If any is missing → abort with a clear error pointing at the missing prereq.

---

## §4 Audit queries (`migrations/stage_s6_audit_queries.cypher`)

The runner runs each in read-only mode and captures results.

```cypher
// =================== QV1–QV10 (invariants) ===================

// QV1 — Every :Quelle is one of the secondary kinds
MATCH (q:Quelle)
WHERE NOT (q:Dossier OR q:ExternalLink OR q:ResearchDocument
        OR q:SectionRef OR q:OntologyAnchor)
RETURN 'QV1' AS gate, count(q) AS violations,
       collect(q.id)[..10] AS sample;

// QV2 — Every :ExternalLink has non-null .url
MATCH (e:ExternalLink) WHERE e.url IS NULL
RETURN 'QV2' AS gate, count(e) AS violations;

// QV3 — Every :ExternalLink has url_status (S2 done)
MATCH (e:ExternalLink) WHERE e.url_status IS NULL OR e.url_status = 'unchecked'
RETURN 'QV3' AS gate, count(e) AS violations;

// QV4 — Every source_curated citation edge has verification_status
MATCH ()-[r]->()
WHERE r.evidence_origin = 'source_curated'
  AND r.evidence_excerpt IS NOT NULL AND r.evidence_excerpt <> ''
  AND (r.verification_status IS NULL OR r.verification_status = 'unchecked')
RETURN 'QV4' AS gate, count(r) AS violations;

// QV5 — No :Dossier carries text_content
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
RETURN 'QV5' AS gate, count(d) AS violations;

// QV6 — Every Projekt/Bauwerk/Akteur has source_urls
MATCH (n) WHERE (n:Projekt OR n:Bauwerk OR n:Akteur) AND n.source_urls IS NULL
RETURN 'QV6' AS gate, count(n) AS violations;

// QV7 — same nodes have source_quality_summary
MATCH (n) WHERE (n:Projekt OR n:Bauwerk OR n:Akteur)
  AND n.source_quality_summary IS NULL
RETURN 'QV7' AS gate, count(n) AS violations;

// QV8 — Every source_curated edge resolved by S3
MATCH ()-[r]->()
WHERE r.evidence_origin = 'source_curated'
  AND (r.verification_status = 'unchecked' OR r.verification_status IS NULL)
RETURN 'QV8' AS gate, count(r) AS violations;

// QV9 — No url contains 'utm_' or trailing slash
MATCH (e:ExternalLink)
WHERE e.url CONTAINS 'utm_' OR (e.url ENDS WITH '/' AND size(e.url) > 12)
RETURN 'QV9' AS gate, count(e) AS violations;

// QV10 — Every S2/S3/S6 DataIssue has a :CONCERNS edge
MATCH (i:DataIssue)
WHERE i.found_by IN ['s2_url_probe','s3_content_verify','s4_dossier_path_retry',
                     's5_visibility','s6_audit']
  AND NOT exists{(i)-[:CONCERNS]->()}
RETURN 'QV10' AS gate, count(i) AS violations;

// =================== Distributions ===================

// D1 — URL reachability distribution
MATCH (e:ExternalLink)
RETURN e.url_status AS status, count(e) AS c
ORDER BY c DESC;

// D2 — Verification status distribution
MATCH ()-[r]->()
WHERE r.verification_status IS NOT NULL
RETURN r.verification_status AS status, count(r) AS c
ORDER BY c DESC;

// D3 — Trust-score distribution (binned)
MATCH (p:Projekt) WHERE p.source_trust_score IS NOT NULL
WITH CASE
       WHEN p.source_trust_score >= 0.9 THEN '0.9-1.0'
       WHEN p.source_trust_score >= 0.7 THEN '0.7-0.9'
       WHEN p.source_trust_score >= 0.5 THEN '0.5-0.7'
       WHEN p.source_trust_score >= 0.3 THEN '0.3-0.5'
       ELSE '0.0-0.3'
     END AS bin, p
RETURN bin, count(p) AS c
ORDER BY bin DESC;

// D4 — DataIssue by kind
MATCH (i:DataIssue) RETURN i.kind AS kind, count(i) AS c
ORDER BY c DESC;

// D5 — DataIssue by severity
MATCH (i:DataIssue) RETURN i.severity AS sev, count(i) AS c;

// D6 — Tier-1 projects with verified sources
MATCH (p:Projekt {quality_tier:'tier_1_decision_grade'})
RETURN p.id AS projekt, p.source_count AS n, p.source_trust_score AS trust
ORDER BY trust DESC NULLS LAST;

// D7 — Top-10 projects by no_text_match citations
MATCH (p:Projekt)-[bel:BELEGT_IN]->(:Dossier)-[z:ZITIERT_QUELLE]->(:ExternalLink)
WHERE z.verification_status = 'no_text_match'
WITH p, count(z) AS no_match_count
RETURN p.id, no_match_count
ORDER BY no_match_count DESC LIMIT 10;

// D8 — Top-10 ExternalLinks by no_text_match incoming
MATCH (e:ExternalLink)<-[z:ZITIERT_QUELLE]-(:Dossier)
WHERE z.verification_status = 'no_text_match'
WITH e, count(z) AS no_match_count
RETURN e.url AS url, no_match_count
ORDER BY no_match_count DESC LIMIT 10;

// =================== node_with_no_source seed ===================
// Find :Projekt without any source_urls — likely an ingestion gap
MATCH (p:Projekt) WHERE p.source_count = 0 OR p.source_count IS NULL
MERGE (i:DataIssue {id: 'di_node_no_source__' + p.id})
ON CREATE SET
  i.kind = 'node_with_no_source',
  i.severity = 'medium',
  i.ref_label = 'Projekt',
  i.ref_id = p.id,
  i.found_at = date(),
  i.found_by = 's6_audit',
  i.status = 'open',
  i.resolution_note = 'Projekt has zero source URLs. Likely an ingestion gap.'
MERGE (i)-[:CONCERNS]->(p);
```

---

## §5 The `FINAL_QUELLE_AUDIT.md` report

Generated by the runner using the JSON from §4. Template structure:

```markdown
# FINAL — Quelle remediation audit

- **Audit run:** <ISO timestamp>
- **Database:** mit-bestand
- **Plan:** _neo4j/QUELLE_REMEDIATION_PLAN.md
- **Supersedes:** the legacy Q1–Q5 outcome
- **Verdict:** PASS | PASS WITH RESIDUALS | FAIL

## 0. Headline

| Metric | Pre-S1 | Post-S6 |
|---|---:|---:|
| `:Quelle` total | ~1,570 | ... |
| `:ExternalLink` distinct URLs | ~580 | ... |
| `:Dossier` with text_content | ~95 | **0** |
| `source_curated` citation edges | 3,074 | ... |
| Verified citations (verbatim+paraphrase+token) | 0 | ... |
| `:DataIssue` count | 1,454 | ... |
| Tier-1 projects with trust ≥ 0.7 | n/a | ... |

## 1. Invariants (QV1–QV10)

[table of each invariant + violations count]

## 2. URL reachability distribution (S2)

[D1 results]

## 3. Verification distribution (S3)

[D2 results]

## 4. Trust-score distribution (S5)

[D3 binned results]

## 5. DataIssue rollup (S2 / S3 / S4 / S5 / S6)

[D4 + D5]

## 6. Tier-1 projects — source quality

[D6 table]

## 7. Most-problematic citations (for re-curation)

### 7.1 Top-10 projects by `no_text_match` count
[D7]

### 7.2 Top-10 URLs returning `no_text_match`
[D8]

## 8. Residuals + recommended follow-ups

- N projects with `source_count = 0` → ingestion gap
- N URLs with `url_status = blocked_by_robots` → consider per-host exception or skip
- N dossiers still without text_content (FU-8 unresolved) → manual path entry needed
- N citations marked `language_mismatch` → cross-lingual matching out of scope

## 9. CI gate

The script `_scripts/validate_no_text_content.py` is now installed and referenced from `_neo4j/intake/README.md`. Every future ingestion MUST pass it.

## 10. Sign-off

This audit was generated automatically against the live `mit-bestand`. Every invariant green = pass. Yellow = pass with residuals (still acceptable). Red = block; investigate.
```

---

## §6 The CI gate (`_scripts/validate_no_text_content.py`)

```python
"""validate_no_text_content.py — fail if any :Dossier carries text_content.

Run after every ingestion. Add to pre-flight in _neo4j/intake/README.md.
"""
import sys
from pathlib import Path
from neo4j import GraphDatabase
sys.path.insert(0, str(Path(__file__).resolve().parent))
from neo4j_env import resolve_connection

uri, user, password, _db = resolve_connection()
with GraphDatabase.driver(uri, auth=(user, password)) as driver:
    with driver.session(database='mit-bestand', default_access_mode='READ') as s:
        result = s.run(
            "MATCH (d:Dossier) WHERE d.text_content IS NOT NULL RETURN count(d) AS c"
        ).single()
        n = result['c']
        if n > 0:
            print(f"FAIL: {n} :Dossier nodes carry text_content. "
                  f"Strip via Q3 / mig_s4_b_text_strip before merging.")
            sys.exit(2)
        print("OK: no :Dossier carries text_content.")
```

Add to [_neo4j/intake/README.md](../intake/README.md) Pre-flight section:

```
- `python _scripts/validate_no_text_content.py` MUST exit 0 before any new ingestion.
```

---

## §7 Acceptance gates (S6 itself)

| Gate | Expected |
|---|---|
| All 10 QV invariants return 0 violations OR explicit yellow-flag note | yes |
| `FINAL_QUELLE_AUDIT.md` written at repo root | yes |
| `STAGE_S6_AUDIT_DONE.flag` written | yes |
| `_scripts/validate_no_text_content.py` exists and exits 0 | yes |
| Runner has 0 errors | yes |

---

## §8 Rollback

```cypher
MATCH (i:DataIssue) WHERE i.found_by = 's6_audit' DETACH DELETE i;
// Delete _neo4j/FINAL_QUELLE_AUDIT.md and STAGE_S6_AUDIT_DONE.flag manually if needed.
```

---

## §9 Handoff

When S6 completes:

1. Verdict in `STAGE_S6_AUDIT_DONE.flag`: PASS / PASS_WITH_RESIDUALS / FAIL.
2. HANDOFF_LOG row: full summary line.
3. PR body: top 3 metrics that matter — overall verification rate, count of `no_text_match`, count of dead URLs.
4. After PR merge, fast-forward `wip/kinan2`.

---

## §10 What "done" means for the entire effort

After S6 PASS:

- `python _scripts/find_sources.py p_stuttgart_210 --verify` works and shows per-URL verification.
- Browser-click on any Projekt/Bauwerk/Akteur shows source_urls + quality + trust in the property panel.
- `MATCH (i:DataIssue {status:'open'}) RETURN i.kind, count(i)` is the user's prioritised backlog.
- The user can finally say: **"for this fact in the graph, here's the URL it came from, and here's whether the URL is live, and here's whether the URL actually contains the claim."**

That's the full chase-and-double-check loop.

---

**End of AGENT_S6_audit_signoff.md.**
