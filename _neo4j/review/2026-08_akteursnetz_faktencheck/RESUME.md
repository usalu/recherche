# Resume: Akteursnetz fact-check

Plan: `C:\Users\Kinosh\.claude\plans\idempotent-drifting-river.md`

## State (2026-08-13)

**GRADING COMPLETE — 955/955 nodes, all 11 panels, zero gaps, zero unrecovered
agent failures.** 127/127 packets returned.

    kern 493 | bezug 380 | ohne_beleg 82        (nodes)
    belegt 406 | teilweise_belegt 46 | unklar 88 (540 graded edges)

`prune_faktencheck.json` is written: **88 removal candidates** (82 × R2, 6 × R1).

Coverage prints on every `merge_verdicts.py` run.

## How to run a remaining packet

The pre-split arg batches already exist and cover exactly the remaining packets:

| group | batches | packets |
|---|---|---|
| CH | `args_CH-b1/b2/b3.json` | 13 |
| DK+SE | `args_DK-SE-b1/b2/b3.json` | 15 |
| FI+NO | `args_FI-NO-b1/b2/b3.json` | 13 |

1. Read the batch file.
2. `Workflow({scriptPath: "…\shard_<GROUP>.js", args: <the file's contents inline>})`
   — args must be passed inline; workflow scripts have no filesystem access.
   Keep batches at their existing size: one batch ≈ 1–7 agents, which is what
   fits under the concurrency cap without tripping session rate limits.
3. Save the task output: `cp <task output path> raw/shard_<GROUP>-<batch>.json`
4. Re-run `merge_verdicts.py` (auto-picks up everything in `raw/`).

**Note on earlier "missing" packets:** the DE/NL packets that were open before
2026-08-13 were not unattempted — their agents died on a session rate limit
(`You've hit your session limit`). Retrying them worked unchanged. If a batch
comes back with `ausgefallen`, it is almost certainly rate limiting, not data.

## merge_verdicts.py — current behaviour

Rules are R1–R3 only (the plan defines three computed removal rules; there is no
R4–R6):
- R1 `duplikat` flag → candidate
- R2 `ohne_beleg` AND (no drawn edge OR every incident edge `unklar`) → candidate
- R3 `falsches_land` AND the correct country is not itself a drawn panel → candidate

Never candidates on their own: `nicht_pruefbar`, `kern`, `bezug`, `defunkt`.

Outputs every run: `prune_candidates_preview.json`, `verdicts.json`,
`coverage_log.json`.

**`prune_faktencheck.json` is written only when all 11 panels are fully graded.**
A partial prune list would be exactly the silent country-drop the plan warns
about, so the script refuses and prints which panels are still short.

Country is taken from each packet's own `cc`, never from the filename — the
grouped shards (`shard_DK-SE-*`, `shard_FI-NO-*`) put two countries in one file.

## Decisions taken

- **Sweden: RESOLVED, no removal question arises.** SE graded 47/47 →
  **32 kern, 15 bezug, 0 ohne_beleg, 0 removal candidates.** The plan's worry
  (SE drops out of the figures) was wrong: "47/47 overlay with 0 URLs"
  described a gap in the *export*, not absent organisations. Every SE entry has
  a live page (CCBuild, Vasakronan, Bjerking, Palats, Stockholms stad,
  Återbygget …). Nothing to decide — the rules nominate nothing in SE.

## ALL DONE (2026-08-13)

1. **Grading: 955/955, complete.**
2. **Verify pass: 899/899 claims checked** (493 kern nodes + 406 belegt edges).
   Raw batch outputs in `verify_raw/`, merged in `verify_all_checks.json`.
   Result: 788 confirmed verbatim, 83 paraphrased-but-supported, **4 fabricated
   quotes (0.44%)**, 24 pages currently unreachable. All 4 misses are on the
   node side; edges came back 100% clean. Findings + demotions in
   `verify_findings.md`.
3. **Review file written:** `E:\semio\mit-bestand\bericht\zwischenbericht\anhang\akteursnetz-faktencheck.md`
   (via `emit_review.py`, in this folder). Sent to the user.

## Known open item — R3 rule field bug (flagged, NOT auto-fixed)

`merge_verdicts.py`'s R3 rule checks `land_soll`, but the grading agents
consistently wrote `land_ist` = the actor's actual correct country and
`land_soll` = the (wrong) panel it's drawn in — i.e. R3 checks the field that
by definition is always a drawn panel, so **R3 can never fire** (0/88
candidates are R3). This was caught while writing the review file, not before.

Do NOT blindly flip the field to `land_ist` — of the 7 `falsches_land`-flagged
nodes, only 5 are genuine country errors (4 DE→DK, 1 NL→LU/SXB-EDGE); the other
2 (NL: BlueCity, Workspot) carry `land_ist=CN/US` because of a **stored-URL
mix-up** with an unrelated foreign company of the same name — the actors
themselves are correctly Dutch. A naive field-swap would wrongly nominate two
real, correctly-panelled actors for removal. This is worked out and explained
per-row in the review file's "Falsches Land" section (with a recommendation:
EDGE/SXB — Luxembourg-registered, not a drawn panel — is the one case where an
R3 candidate would be legitimate once the rule is fixed properly).

## Data defects already found (for the review file)

- Four nodes drawn in the **DE** panel are Danish: Roskilde Universitet,
  Roskilde Kommune, Høje-Taastrup Kommune, Region Hovedstaden (`falsches_land`).
  DK is itself a drawn panel, so R3 correctly does *not* nominate them — they
  are mis-panelled, not removable.
- Nine `bauteilbörse <city>` entries came back `defunkt` but graded `bezug`, so
  they are kept, not pruned.

## Separately: akteursnetz report integration

Already done and compiling clean:
- Pipeline rescued to `E:\recherche\_neo4j\netz\` (git-tracked)
- Appendix **Anlage AN** in the zwischenbericht (`anhang/akteursnetz.tex`
  + `-figuren.tex` + `-tabellen.tex`)
- Table style reverted to the dense v1 grid (`netz/render/latex/table_grid.py`),
  escaping bug in the original generator fixed

Nothing committed to git in either repo yet. The plan requires every producing
script to be committed to `E:\recherche` — that is still outstanding.
