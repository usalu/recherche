# Resume: Akteursnetz fact-check — remaining packets

Everything below is already built and working. This is the last stretch — no new design decisions needed, just execution.

## What's left

**DE** (script: `shard_DE.js`): packets `DE-c01`, `DE-c07`, `DE-c08`, `DE-s01`, `DE-s02`, `DE-s03`, `DE-s04`, `DE-s06`, `DE-s08`

**NL** (script: `shard_NL.js`): packets `NL-c07`, `NL-c11`, `NL-s01`, `NL-s02`, `NL-s05`

Everything else (AT, GB, FR, BE fully; the rest of DE and NL) is done and saved in `raw/`.

## How to run each packet

1. Read `worklist.json` in this folder, find the packet by `packet_id` under `packets[]` (filter by `cc` first — `"DE"` or `"NL"`).
2. Launch `Workflow({scriptPath: "E:\\recherche\\_neo4j\\review\\2026-08_akteursnetz_faktencheck\\shard_DE.js"` (or `shard_NL.js`), `args: {"packets": [<that packet's JSON object>]}})`. One or a few packets per call is fine — that's how it was run throughout.
3. When the task notification lands, save the raw output:
   `cp <task output path> raw/shard_<packet_id>.json`
4. Repeat for each remaining packet.

## After all packets are done

1. Re-run `merge_verdicts.py` in this folder — it auto-picks up everything in `raw/` and regenerates `prune_candidates_preview.json` (the removal-candidate list).
2. Still open from the original plan (`C:\Users\Kinosh\.claude\plans\idempotent-drifting-river.md`):
   - The **Sweden decision** — SE hasn't been fact-checked yet at all (47/47 overlay nodes, 0 URLs) and will likely come back almost entirely `ohne_beleg`. Needs a deliberate call before removal, not a silent script outcome. **CH, DK, SE, FI, NO haven't been started at all yet either** — only AT/GB/FR/BE/DE/NL have been run.
   - Adversarial verify pass (`verify.js`, already generated, never run) — re-checks every `kern` node and `belegt` edge.
   - `merge_verdicts.py` / `emit_review.py` need the eid-reattachment + R1–R6 removal-rule logic finished (partially done in the current `merge_verdicts.py` — check it still matches the plan before trusting it fully).
   - Final human-readable file `E:\semio\mit-bestand\bericht\zwischenbericht\anhang\akteursnetz-faktencheck.md` — not started.

## Separately: the akteursnetz report integration

Already done and compiling clean in the real report:
- Pipeline rescued to `E:\recherche\_neo4j\netz\` (git-tracked, was only in a temp scratchpad before)
- New appendix **Anlage AN** in the real zwischenbericht (`anhang/akteursnetz.tex` + `-figuren.tex` + `-tabellen.tex`)
- Table style reverted to the original dense v1 grid layout (`netz/render/latex/table_grid.py`) per request, escaping bug from the original generator fixed along the way

Nothing has been committed to git in either repo yet.
