# Agent S4 — schema cleanup

> **Read [ORCHESTRATION.md](ORCHESTRATION.md) first.**

You are agent S4 of 6. Your job: **clean up the `:Quelle` model into clear secondary labels, strip the markdown-text bloat, and resolve the 5 dossier-path-resolution failures from FU-8.**

You run in parallel with S2 and S3 — you don't touch any property they care about.

---

## §1 Cold-start context

- `:Quelle` (~1,570 nodes) uses `.quelltyp` as a discriminator for 5+ kinds. We want first-class secondary labels.
- ~95 `:Quelle {quelltyp:'case_markdown'}` carry `text_content` (full dossier markdown). This is the R7.d mistake the user asked us to fix.
- 5 `:Quelle {quelltyp:'case_markdown'}` are missing `text_content` (FU-8) — their dossier files are unfindable by the previous path resolver. S4 retries with a smarter resolver.
- 16 dossiers have parallel `qu_*_dossier` and `q_<slug>_md` aliases from R7.a; they were merged but the surviving node's aliases need to be sanity-checked.

---

## §2 Mission

1. **Promote `quelltyp` to secondary labels** — `:Dossier`, `:ExternalLink`, `:ResearchDocument`, `:SectionRef`.
2. **Strip `Quelle.text_content`** from every `:Dossier` (gated on S1 — every dossier must have at least one outgoing `:ZITIERT_QUELLE`).
3. **Resolve FU-8** — for the 5 dossiers without `text_content`, try harder path-resolution; if found, populate text and re-trigger S1 on those dossiers. If not, emit `:DataIssue {kind:'dossier_path_unresolvable'}`.
4. **Sanity-check the 16 dual-naming aliases** — confirm each surviving `q_<slug>_md` has the `qu_<slug>_dossier` form in `.aliases`.

You do NOT touch `url_*` properties (S2's), `verification_*` properties (S3's), or `source_*` properties (S5's).

---

## §3 Schema delta

Already covered in [QUELLE_REMEDIATION_PLAN.md §3.1](../QUELLE_REMEDIATION_PLAN.md) — secondary labels and the strip. No new properties introduced.

---

## §4 Conflict avoidance

You write:
- Secondary labels (`:Dossier`, `:ExternalLink`, `:ResearchDocument`, `:SectionRef`).
- `:Dossier.text_content_chars_pre_strip`, `:Dossier.text_content_stripped_at`.
- Remove `:Dossier.text_content`.
- `:Dossier.text_content_retry_attempted_at`, `:Dossier.text_content_retry_result` (FU-8 resolution).
- New `:DataIssue {kind:'dossier_path_unresolvable'}` if FU-8 retries fail.

You DO NOT touch:
- `url_*` properties — S2.
- `verification_*` properties — S3.
- `source_*` properties — S5.
- `:ZITIERT_QUELLE` or `:BELEGT_IN` edges (just READ them to confirm strip safety).

---

## §5 Pre-flight

```bash
# 1. S1 done flag
ls _neo4j/intake/runs/2026-05-21_quelle_remediation/agent_s1_url_extractor/PHASE_S1_DONE.flag

# 2. Branch
git switch -c agent_s4/schema-cleanup

# 3. Expected starting counts
# MATCH (q:Quelle {quelltyp:'case_markdown'}) WHERE q.text_content IS NOT NULL RETURN count(q);  -- 95
# MATCH (q:Quelle {quelltyp:'case_markdown'}) WHERE q.text_content IS NULL     RETURN count(q);  -- 5
# MATCH (q:Quelle) WHERE q.quelltyp = 'case_markdown' RETURN count(q);                            -- 100
```

---

## §6 Migrations

### §6.1 Secondary labels

Adopt the [legacy mig_q2_secondary_labels.cypher](../intake/runs/2026-05-21_quelle_remediation/migrations/mig_q2_secondary_labels.cypher) as the starting point. Rename to `mig_s4_a_secondary_labels.cypher`. No changes to logic.

### §6.2 Strip text_content (gated)

```cypher
// S4.B.1 — Pre-gate: every Dossier with text_content must have ≥ 1
// ZITIERT_QUELLE → ExternalLink (proving S1 extracted its links).
// Runner aborts strip if violations > 0.
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
  AND NOT exists{(d)-[:ZITIERT_QUELLE]->(:ExternalLink)}
RETURN 's4_b1_pre_strip_gate' AS rule, count(d) AS violations;

// S4.B.2 — Capture pre-strip stats
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
WITH d, size(d.text_content) AS char_count
SET d.text_content_chars_pre_strip = char_count,
    d.text_content_stripped_at = date(),
    d.migration_origin = coalesce(d.migration_origin, '') + ' | mig_s4_b_text_strip';

// S4.B.3 — Strip
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
REMOVE d.text_content;

// S4.B.4 — Audit
MATCH (d:Dossier) WHERE d.text_content IS NOT NULL
RETURN 's4_b4_dossiers_with_text_remaining' AS rule, count(d) AS violations;

MATCH (d:Dossier) WHERE d.text_content_chars_pre_strip IS NOT NULL
RETURN 's4_b4_dossiers_stripped' AS check, count(d) AS c,
       sum(d.text_content_chars_pre_strip) AS total_chars_removed;
```

### §6.3 FU-8 dossier path retry

Driver-side Python — the original R7.d resolver matched on `q.id`-slug; FU-8 dossiers fail this match because their dossier files live under non-standard paths or have casing variations.

```python
def retry_resolve_dossier_path(dossier_id):
    """Three-tier fallback for finding the .md file matching a dossier id."""
    slug = dossier_id.removeprefix('q_').removesuffix('_md')

    # Tier 1: exact path match (original R7.d logic)
    canonical_paths = [
        REPO_ROOT / '_neo4j' / 'intake' / 'archive' / '2026-05-20_inbox_batch2_import' / 'raw_tree',
        REPO_ROOT / '_archive' / 'research' / 'gebaeude',
    ]
    for base in canonical_paths:
        for ext in ['.md', '.MD']:
            candidate = base / (slug + ext)
            if candidate.exists():
                return candidate

    # Tier 2: case-insensitive search within canonical paths
    for base in canonical_paths:
        for f in base.rglob('*.md'):
            if f.stem.lower() == slug.lower():
                return f

    # Tier 3: fuzzy match on stem with rapidfuzz
    from rapidfuzz import process
    all_md = []
    for base in canonical_paths:
        all_md.extend(base.rglob('*.md'))
    if all_md:
        match, score, _ = process.extractOne(
            slug, [f.stem for f in all_md], score_cutoff=85
        )
        if match:
            return next(f for f in all_md if f.stem == match)

    return None
```

If resolved → repopulate `Quelle.text_content`, then re-invoke S1 logic on just that dossier (extract URLs), then strip text_content again via §6.2.

If unresolved → emit `:DataIssue`:

```cypher
MATCH (d:Dossier {id: $dossier_id})
MERGE (i:DataIssue {id: 'di_dossier_path_unresolvable__' + d.id})
ON CREATE SET
  i.kind = 'dossier_path_unresolvable',
  i.severity = 'medium',
  i.ref_label = 'Dossier',
  i.ref_id = d.id,
  i.found_at = date(),
  i.found_by = 's4_dossier_path_retry',
  i.status = 'open',
  i.resolution_note = 'Dossier .md file could not be resolved with exact, '
                      'case-insensitive, or fuzzy (85) matching. Provide explicit path.'
MERGE (i)-[:CONCERNS]->(d);
```

### §6.4 Dual-naming alias sanity check

```cypher
// Every q_<slug>_md that resulted from a R7.a merge should have its old
// qu_<slug>_dossier id preserved in .aliases.
MATCH (d:Dossier)
WHERE d.id =~ 'q_.+_md'
WITH d, replace(replace(d.id, 'q_', 'qu_'), '_md', '_dossier') AS expected_alias
WHERE d.aliases IS NULL OR NOT (expected_alias IN d.aliases)
// This is informational — the alias may genuinely not be needed if there
// was never a qu_*_dossier counterpart. Emit DataIssue only if we know
// the counterpart existed pre-R7.a (check R7.a journal).
RETURN d.id, expected_alias LIMIT 20;
```

If any rows return, cross-reference with R7.a's audit log; if the expected_alias really existed pre-merge, set:

```cypher
MATCH (d:Dossier {id: $dossier_id})
SET d.aliases = apoc.coll.toSet(coalesce(d.aliases, []) + [$expected_alias]),
    d.migration_origin = coalesce(d.migration_origin, '') + ' | mig_s4_d_alias_sanity';
```

---

## §7 Runner outline

```python
def run_s4():
    # 6.1 — Secondary labels (pure Cypher)
    run_cypher_file('mig_s4_a_secondary_labels.cypher')

    # 6.3 — FU-8 retry FIRST (before strip — so newly-resolved dossiers
    # get their URLs extracted into ExternalLink via S1 logic)
    unresolved = session.run(
        "MATCH (d:Dossier) WHERE d.text_content IS NULL RETURN d.id"
    )
    for d in unresolved:
        path = retry_resolve_dossier_path(d['id'])
        if path:
            text = path.read_text(encoding='utf-8')
            session.run(
                "MATCH (d:Dossier {id: $id}) "
                "SET d.text_content = $text, "
                "    d.text_content_retry_attempted_at = date(), "
                "    d.text_content_retry_result = 'resolved', "
                "    d.text_content_resolved_path = $path",
                id=d['id'], text=text, path=str(path)
            )
            # Re-extract URLs for this dossier (mini S1 re-run)
            from agent_s1_url_extractor.logs.agent_s1_runner import extract_for_dossier
            extract_for_dossier(d['id'])
        else:
            # Emit DataIssue
            session.run(s4_data_issue_cypher, dossier_id=d['id'])

    # 6.2 — Pre-gate then strip
    gate = session.run(s4_b1_gate_cypher).single()
    if gate['violations'] > 0:
        raise RuntimeError(f"Strip aborted: {gate['violations']} dossiers have text but no extracted URLs")
    run_cypher_file('mig_s4_b_text_strip.cypher')

    # 6.4 — Alias sanity (informational)
    run_cypher_file('mig_s4_d_alias_sanity.cypher')

    # Audits
    ...
```

---

## §8 Acceptance gates

| Gate | Cypher | Expected |
|---|---|---|
| `:Dossier` label count | `MATCH (d:Dossier) RETURN count(d)` | 100 |
| `:ExternalLink` label count | `MATCH (e:ExternalLink) RETURN count(e)` | ≥ post-S1 count |
| Untyped `:Quelle` after S4 (excluding OntologyAnchor) | `MATCH (q:Quelle) WHERE NOT (q:Dossier OR q:ExternalLink OR q:ResearchDocument OR q:SectionRef OR q:OntologyAnchor) RETURN count(q)` | ≤ 5 (residual) |
| `:Dossier` with `text_content` | `MATCH (d:Dossier) WHERE d.text_content IS NOT NULL RETURN count(d)` | 0 |
| `:Dossier` with `text_content_chars_pre_strip` set | `MATCH (d:Dossier) WHERE d.text_content_chars_pre_strip IS NOT NULL RETURN count(d)` | ≥ 95 (may be 100 if FU-8 fully resolved) |
| Total chars stripped | `MATCH (d:Dossier) WHERE d.text_content_chars_pre_strip IS NOT NULL RETURN sum(d.text_content_chars_pre_strip)` | ≥ 2,000,000 (~2 MB) |
| FU-8 unresolved emitted as DataIssue | `MATCH (i:DataIssue {kind:'dossier_path_unresolvable'}) RETURN count(i)` | ≤ 5 (decreases as resolver improves) |

---

## §9 Rollback

```cypher
// Drop secondary labels
MATCH (q:Quelle:Dossier) REMOVE q:Dossier;
MATCH (q:Quelle:ExternalLink) REMOVE q:ExternalLink;
MATCH (q:Quelle:ResearchDocument) REMOVE q:ResearchDocument;
MATCH (q:Quelle:SectionRef) REMOVE q:SectionRef;

// Repopulate text_content from disk (driver-side; iterate journals)
// Each :Dossier with text_content_chars_pre_strip > 0 → re-read the .md file
// (the file is the source of truth; rollback is lossless).
// See runner's rollback function.

// Drop S4-issued DataIssue
MATCH (i:DataIssue) WHERE i.found_by = 's4_dossier_path_retry' DETACH DELETE i;
```

---

## §10 Risks specific to S4

| Risk | Mitigation |
|---|---|
| The strip gate fails — some dossier has text_content but no extracted URLs | Investigate: was the dossier markdown empty of URLs? Tag manually; don't strip until S1 retried. |
| FU-8 retries find a .md file but the content is for a different project (slug collision) | The fuzzy match score (≥ 85) reduces but doesn't eliminate this. Sample-check 2–3 resolved cases manually. |
| The OntologyAnchor nodes get secondary labels by mistake | Exclude `:OntologyAnchor` from S4.A explicitly. |
| Some `:Quelle` has `quelltyp = NULL` (legacy) | Match by id pattern fallback: `q_<slug>_md` → `:Dossier`, URLs in `.url` → `:ExternalLink`. |

---

## §11 Handoff

When S4 completes:

1. Write `agent_s4_schema_cleanup/PHASE_S4_DONE.flag`.
2. Push branch + open PR.
3. HANDOFF_LOG row: Dossier=X, ExternalLink=Y, FU-8 resolved=Z, unresolved=W, chars_stripped=N.

S4 unblocks no agent (it runs parallel with S2/S3); S5 reads the secondary labels for its surfacing logic.

---

**End of AGENT_S4_schema_cleanup.md.**
