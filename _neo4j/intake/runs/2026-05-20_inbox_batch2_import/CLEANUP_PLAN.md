# CLEANUP_PLAN — repo housekeeping after batch2 v2

**Audience:** Whoever (agent or human) is closing out the batch2 v2 work.
**When to execute:** After verifying everything in [HANDOFF.md](HANDOFF.md) is understood and the graph state is satisfactory.
**Risk profile:** All actions below are reversible (git tracks them; backups exist). None modify the live database.

This document specifies WHAT to clean up, WHY each action makes sense, and HOW to execute it precisely. Order matters where indicated.

---

## §1 — Archive the processed inbox dossiers (PRIMARY cleanup task)

### Why

`_neo4j/intake/README.md` says:

> After processing, move the untouched raw package into `archive/<run-id>/` and keep the generated reports in `runs/<run-id>/`.

All 21 dossier files in `_neo4j/intake/inbox/projects/` were ingested into the graph during batch2 v2. They are no longer "incoming raw drops" — they're processed input. Leaving them in `inbox/` would falsely signal "new work waiting" to a future agent.

### What to move

Create the archive directory:

```
_neo4j/intake/archive/2026-05-20_inbox_batch2_import/
└── raw_tree/
    ├── BE_NL_graph_ready_dossiers/
    │   ├── Careno_Be_Circular_Brussels.md
    │   ├── Circl_ABN_AMRO_Urban_Mining.md
    │   └── Circl_Pavilion_Amsterdam.md
    ├── BE_NL_graph_ready_dossiers.zip
    ├── DE_AT_CH_graph_ready_dossiers/
    │   ├── LYSP8_Basel.md
    │   ├── MedUni_Campus_Mariannengasse_Wien.md
    │   ├── RE_USE_Hoefe_Wien.md
    │   ├── Reallabor_Be_Ware.md
    │   └── Stuttgart_210.md
    ├── DE_AT_CH_graph_ready_dossiers.zip
    ├── EU_consortia_graph_ready_dossiers/
    │   ├── FCRBE_Facilitating_Circulation_Reclaimed_Building_Elements.md
    │   ├── Interreg_NWE_FCRBE.md
    │   ├── REBRIDGE_Structural_Reuse.md
    │   └── Reuse_Logistics.md
    ├── EU_consortia_graph_ready_dossiers.zip
    ├── batch 1.md                            # 3 sub-dossiers (SMS Zürich, UMAR, ELEMENTA)
    ├── reuse_platform_graph_ready_dossiers/
    │   ├── RCMI_Concular.md
    │   └── REFAIR_Bordeaux.md
    ├── teaching_programme_graph_ready_dossiers/
    │   ├── Architecture_of_Reuse_Brussels.md
    │   ├── ETH_Circular_Construction_Programme.md
    │   ├── Vandkunsten_Component_Reuse_Programme.md
    │   └── ZHAW_Reuse_in_Construction.md
    ├── teaching_programme_graph_ready_dossiers.zip
    ├── uk_unclear_graph_ready_dossiers/
    │   ├── Granby_Workshop_Liverpool.md
    │   └── OBK_27.md
    └── uk_unclear_graph_ready_dossiers.zip
```

### How to execute

```bash
# Create archive dir
mkdir -p _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree

# Move all dossier folders + zips + batch 1.md
git mv _neo4j/intake/inbox/projects/BE_NL_graph_ready_dossiers/ _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/BE_NL_graph_ready_dossiers.zip _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/DE_AT_CH_graph_ready_dossiers/ _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/DE_AT_CH_graph_ready_dossiers.zip _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/EU_consortia_graph_ready_dossiers/ _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/EU_consortia_graph_ready_dossiers.zip _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv "_neo4j/intake/inbox/projects/batch 1.md" _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/reuse_platform_graph_ready_dossiers/ _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/teaching_programme_graph_ready_dossiers/ _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/teaching_programme_graph_ready_dossiers.zip _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/uk_unclear_graph_ready_dossiers/ _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
git mv _neo4j/intake/inbox/projects/uk_unclear_graph_ready_dossiers.zip _neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/
```

After move:
- `_neo4j/intake/inbox/projects/` should contain only `.gitkeep`.
- `_neo4j/intake/archive/2026-05-20_inbox_batch2_import/raw_tree/` should contain all 21 dossiers.

### Add a README to the archive

```bash
cat > _neo4j/intake/archive/2026-05-20_inbox_batch2_import/README.md <<'EOF'
# Archive — 2026-05-20 inbox batch2 import

**Raw drop preserved for provenance.** Do not edit files under `raw_tree/`.

These 21 dossier files were processed via the multi-phase batch2 v2 import. See:
- [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md`](../../runs/2026-05-20_inbox_batch2_import/HANDOFF.md) — overview
- [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/PLAN_v2.md`](../../runs/2026-05-20_inbox_batch2_import/PLAN_v2.md) — plan
- [`_neo4j/review/round_002_followup/rollback.md`](../../../review/round_002_followup/rollback.md) — apply ledger

Apply outcome: +282 nodes / +2 954 relationships against the `mit-bestand` Neo4j database.
EOF
```

---

## §2 — Mark superseded documents (don't delete; just label)

### Why

The `runs/2026-05-20_inbox_batch2_import/` folder currently has multiple revisions of the same docs (PLAN, NEXT_STEPS). A future agent can't tell which is current without reading internals. Adding a prefix banner to superseded docs solves this without losing history.

### Files to mark as superseded

| File | Status | Action |
|---|---|---|
| `PLAN.md` | Superseded by PLAN_v2.md | Add banner |
| `NEXT_STEPS.md` | Superseded by NEXT_STEPS_v2.md and REMAINING_GAPS.md | Add banner |
| `NEXT_STEPS_v2.md` | Superseded by REMAINING_GAPS.md | Add banner |
| `predelete_snapshot.json` | Pre-Phase-1 snapshot — archival only | Leave as-is (low risk; small) |
| `predelete_snapshot_round2.json` | Pre-Phase-4c snapshot | Leave as-is |
| `predelete_snapshot_round3.json` | Pre-Phase-17 snapshot | Leave as-is |
| `apply_log.jsonl` | Per-patch apply log — historic | Leave as-is |
| `pre_flight_results.json` | Pre-flight survey output | Leave as-is |
| `pre_flight_validation.cypher` | Pre-flight validation source | Leave as-is — reusable for batch3 |

### How to execute (banner header)

For each superseded markdown file, prepend a short banner. Example for `PLAN.md`:

```markdown
> ⚠️ **SUPERSEDED** by [PLAN_v2.md](PLAN_v2.md) (incorporates all corrections from [CORRECTIONS_2026-05-20.md](CORRECTIONS_2026-05-20.md) and the user decisions documented in [HANDOFF.md §7](HANDOFF.md#7-decisions-log-d1-d16--b1-b4-from-batch2-v2)). Keep for diff/historic reference.

---

[original content below]
```

Same pattern for `NEXT_STEPS.md` (point at NEXT_STEPS_v2.md + REMAINING_GAPS.md) and `NEXT_STEPS_v2.md` (point at REMAINING_GAPS.md).

---

## §3 — Decide on per-patch apply reports retention

### Status

`_neo4j/review/round_002_followup/apply_reports/` is **3.7 MB total**, with ~70 batch2 v2 reports. Each patch produced a `.json` + `.md` apply report.

### Recommendation: KEEP

These are the audit trail. If anyone ever asks "did this op succeed? what did it touch?", the apply reports are the answer. 3.7 MB is small. Don't delete.

### What to confirm

If `.gitignore` excludes `apply_reports/`, ensure it's in the repo via `git add -f` or remove the ignore rule. Check:

```bash
git check-ignore _neo4j/review/round_002_followup/apply_reports/phase_batch2_v2_2_shared_nodes.patch.apply_report.json
```

If the file IS ignored: decide whether to keep apply_reports gitignored (saves repo size, fine since they're regenerable on re-apply) OR commit them (full audit trail).

---

## §4 — Backups

### Status

`_neo4j/review/backups/batch2_v2_pre_apply/` is **6.4 MB** (full JSONL dump of pre-batch2 graph). Still valid as rollback target.

### Recommendation

**Keep until at least one new substantial batch lands** that supersedes the rollback need. After that, can be deleted IF a fresh backup is taken.

If `.gitignore` excludes backups (likely — backups are regenerable), confirm via:

```bash
cat .gitignore | grep backup
```

Backups should typically be gitignored.

---

## §5 — `_scripts/` cleanup

### Durable scripts (KEEP in repo, document)

| Script | Why durable |
|---|---|
| `apply_neo4j_review_patch.py` | Canonical applier — modified during batch2 v2 (Unicode rel-type fix) |
| `backup_neo4j_graph.py` | Generic backup tool |
| `restore_neo4j_graph_backup.py` | Generic restore tool |
| `neo4j_env.py` | Shared connection settings |
| `_apply_batch2_v2_all.py` | Reusable orchestrator pattern |
| `_run_cypher_file.py` | Reusable Cypher runner |
| `_snapshot_predelete.py` | Reusable safety tool |
| `_gap_survey.py` | Reusable diagnostic |
| `run_preflight_validation.py` | Reusable pre-flight runner |
| `_probe_schema.py` | Reusable diagnostic |
| `_test_graph_queries.py` | Reusable test runner |

### Phase-specific generators (KEEP for historic reproducibility)

These scripts ARE one-shot but they encode the LOGIC of how each phase's patch was built. If batch2 v2 needs to be partially reproduced or audited line-by-line, they're the receipt:

| Script | Generated patch |
|---|---|
| `_generate_phase6_bg_rels.py` | phase_batch2_v2_6b_bg_rels.patch.jsonl |
| `_generate_phase8_project_vocab.py` | phase_batch2_v2_8_project_vocab.patch.jsonl |
| `_generate_phase10_huerde_wirtschaft.py` | phase_batch2_v2_10_huerde_wirtschaft.patch.jsonl |
| `_generate_phase11_bg_vocab.py` | phase_batch2_v2_11_bg_vocab.patch.jsonl |
| `_generate_phase12_deferred_bgs.py` | phase_batch2_v2_12a + 12b |
| `_generate_phase13_more_actors.py` | phase_batch2_v2_13a + 13b |
| `_generate_phase19_counts_as.py` | phase_batch2_v2_19_counts_as.patch.jsonl |
| `_generate_phase20_ketten.py` | phase_batch2_v2_20a + 20b |
| `_generate_phase24_autodiscovery.py` | phase_batch2_v2_24_autodiscovery.patch.jsonl |

### Recommendation

**Move all `_generate_phase*.py` into a subfolder** `_scripts/batch2_v2_generators/` (or similar) — so they don't clutter top-level `_scripts/` but remain available. Add a brief README in that subfolder linking back to the run folder.

```bash
mkdir -p _scripts/batch2_v2_generators
git mv _scripts/_generate_phase*.py _scripts/batch2_v2_generators/

cat > _scripts/batch2_v2_generators/README.md <<'EOF'
# Batch2 v2 phase generator scripts

One-shot generators that produced the JSONL patches for the 2026-05-20 batch2 v2 import.

**Don't delete.** They're the receipt for how each phase was built. If you need to:
- Re-derive a patch from spec → run the matching generator
- Audit a phase's logic → read the script
- Build a similar phase for a future batch → fork the script

See [_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md §6](../../_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md) for the full tooling guide.
EOF
```

### Scripts to consider deleting after handoff is signed off

| Script | Why removable |
|---|---|
| (none yet — all currently in repo serve a documented purpose) | — |

---

## §6 — Patches folder

### Status

`_neo4j/review/round_002_followup/patches/batch2/` has **50 patches (~963 KB)**. All applied.

### Recommendation

**Keep all of them**. They're the apply units; rollback or partial re-apply needs them. The `patches/batch2/` subfolder convention is appropriate.

### Optional: add a README inside `patches/batch2/`

```bash
cat > _neo4j/review/round_002_followup/patches/batch2/README.md <<'EOF'
# patches/batch2/ — batch2 v2 (2026-05-20) apply units

50 patches applied to `mit-bestand`. Order documented in [`../../intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md`](../../../intake/runs/2026-05-20_inbox_batch2_import/APPLY_ORDER.md).

Each `phase_batch2_v2_N_*.patch.jsonl` has a corresponding `.apply_report.json` and `.apply_report.md` in `../apply_reports/`.

For rollback procedure see [`../rollback.md` § Phase batch2 v2](../rollback.md).

DO NOT MOVE THESE FILES. They are referenced from rollback.md, HANDOFF.md, and APPLY_ORDER.md by name.
EOF
```

---

## §7 — `inbox/projects/` becomes empty: keep the directory

After §1, `_neo4j/intake/inbox/projects/` will be empty except for `.gitkeep`. **Do not delete `.gitkeep`** — it preserves the directory for the next intake.

---

## §8 — Update `AGENTS.md` (root) to reference batch2 v2

### Current state

`AGENTS.md` (German) sets the rules for future agents but doesn't reference batch2 v2 specifically.

### Recommendation

Add a 2-3 line addendum at the bottom of `AGENTS.md`:

```markdown
## Aktueller Stand (2026-05-20)

Batch2 v2 ist vollständig importiert. Aktueller Graph-Stand: ~2 580 Knoten / ~19 990 Relationen.
Übergabe-Dokument für nächste Agenten: [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md`](_neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md).
Offene Lücken und Batch3-Kandidaten: [`_neo4j/intake/runs/2026-05-20_inbox_batch2_import/REMAINING_GAPS.md`](_neo4j/intake/runs/2026-05-20_inbox_batch2_import/REMAINING_GAPS.md).
```

---

## §9 — Verify nothing's broken before final commit

After steps 1-8, run:

```bash
# 1. Live graph still healthy
python _scripts/_gap_survey.py

# 2. All patch files still parseable
for f in _neo4j/review/round_002_followup/patches/batch2/*.jsonl; do
  python -c "import json,sys; [json.loads(l) for l in open('$f',encoding='utf-8')]" || echo "BAD: $f"
done

# 3. All referenced paths in HANDOFF.md resolve
grep -oE '\[.+\]\([^)]+\)' _neo4j/intake/runs/2026-05-20_inbox_batch2_import/HANDOFF.md | grep -oE '\([^)]+\)' | tr -d '()' | while read p; do
  [[ "$p" =~ ^http ]] && continue  # skip URLs
  fullpath="_neo4j/intake/runs/2026-05-20_inbox_batch2_import/$p"
  [[ "$p" =~ ^\.\.\/ ]] && fullpath="_neo4j/intake/runs/2026-05-20_inbox_batch2_import/$p"
  [[ -f "$fullpath" ]] || echo "MISSING: $p"
done
```

---

## §10 — Commit strategy

### Recommendation

**One commit per coherent unit**, in this order:

1. **Commit A: "Archive batch2 v2 raw inbox"** — covers §1 (the `git mv` operations + archive README).
2. **Commit B: "Add batch2 v2 handoff + cleanup + gaps docs"** — covers HANDOFF.md, CLEANUP_PLAN.md, REMAINING_GAPS.md.
3. **Commit C: "Mark superseded batch2 v2 plan docs"** — covers §2 banner additions.
4. **Commit D: "Move batch2 v2 generators to subfolder"** — covers §5 (if executed).
5. **Commit E: "Update AGENTS.md with batch2 v2 status"** — covers §8.
6. **Commit F: "Add README to patches/batch2/ + archive/2026-05-20_*"** — covers §6 + §1's README.

Each commit message: 3-word imperative subject, no AI co-author trailers, no `--no-verify`.

### What NOT to commit

- Backups (gitignored by convention)
- Apply reports if `.gitignore` excludes them
- Cursor / MCP configuration with secrets

---

## §11 — Final state checklist

Before declaring batch2 v2 closed:

- [ ] §1 done: 21 dossiers in `archive/2026-05-20_inbox_batch2_import/raw_tree/`, `inbox/projects/` empty except `.gitkeep`
- [ ] §1 done: archive README written
- [ ] §2 done: PLAN.md, NEXT_STEPS.md, NEXT_STEPS_v2.md have superseded banners
- [ ] §5 done (optional): `_generate_phase*.py` moved to `_scripts/batch2_v2_generators/` with README
- [ ] §6 done (optional): patches/batch2/ README written
- [ ] §8 done: AGENTS.md addendum added
- [ ] §9 done: gap survey returns clean; patch parseability check passes
- [ ] §10 done: commits A-F created and pushed (or staged for review)
- [ ] HANDOFF.md, CLEANUP_PLAN.md, REMAINING_GAPS.md committed and pushed
- [ ] Backups still in place at `_neo4j/review/backups/batch2_v2_pre_apply/`
- [ ] Live graph still passes `_gap_survey.py`

---

**End of CLEANUP_PLAN.md.** Updated 2026-05-20.
