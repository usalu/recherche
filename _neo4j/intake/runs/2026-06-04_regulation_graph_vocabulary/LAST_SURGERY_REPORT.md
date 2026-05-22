# LAST SURGERY REPORT — finishing pass after the migration (2026-06-05)

Follows `FINAL_AUDIT_REPORT.md` (the migration, Phases 0–8 + Variant‑B, @14:48). This pass (S1–S5,
@15:22+) closed the residual gaps a full re-analysis found. **Every connection made was web-researched;
nothing fabricated.** Rollback point: backup `_neo4j/review/backups/20260605T152248Z-mit-bestand`
(pre-surgery, 2 273 nodes).

## Final state
**2 255 nodes · 15 235 relationships · 51 labels · 48 relationship types.**

## What this pass did
- **S1 — Schadstoff evidence:** sourced all **137** previously-unsourced pollutant edges
  (`HAT_SCHADSTOFFRISIKO` 100 + `ERFORDERT_SCHADSTOFFPRUEFUNG` 37) + `TYPISCH_BEI_MATERIAL`, each to a
  freshly web-researched authority: TRGS 519/521, PCB-Richtlinie, POP/PAK (arguk), REACH,
  AgBB, AltholzV, UBA-Schimmelleitfaden, **WTA 4‑5** (salts/chlorides), **LABO MKW** (oil),
  **BfS/StrlSchG** (radon). `s_radon` given a source.
- **S2 — connect orphaned components:** 30 material-bearing groups with no regulation link → **125**
  evidence-backed edges (universal reuse proofs KrWG/CPR/DIN SPEC 91484 + material test only where a
  standard exists; plastic/textile correctly got no fabricated test). Coverage 254 → **284**/364.
- **S3 — orphans & duplicates:** merged duplicate actors (Werner Sobek, Gruner ReUse); deleted 5 empty
  project/programme stubs + 11 unused vocab values (18 low-info nodes). Kept `p_lysp8` (real project).
- **S4:** no-op — folding `ERFORDERT_SCHADSTOFFPRUEFUNG` would be lossy (different target); the typed
  `…recht` labels already give one node per law.

## Acceptance — all PASS
| Gate | Result |
|---|---|
| `evidence_status` but no `source_url` | **0** |
| categorical `evidence_confidence` | **0** (all numeric, 0–1) |
| `HAT_SCHADSTOFFRISIKO` unsourced | **0** (was 100) |
| source nodes (Quelle/ExternalLink/SectionRef/Dossier/ResearchDocument) | **0** |
| parallel duplicate edges / duplicate actor names | **0 / 0** |
| spine intact (HAT_BAUTEILGRUPPE 360 · NUTZT_MATERIAL 390 · HAT_BAUWERK 192) | ✅ |
| Bauteilgruppen reaching regulation layer | **284/364** (every material-bearing group; 80 w/o material excluded) |
| Schadstoff reachable by a **sourced** path | **13/13** |
| mojibake (`�`) | **0** |
| orphan nodes | **1** (`p_lysp8`, kept intentionally) |

## Residual / optional
- `p_lysp8` — empty real-project stub; populate when data exists, else delete.
- Typed law layer = 11 `…recht` labels (51 total). Optional stylistic unify → one `Regelwerk` + `domain`
  property (~41 labels) if you ever prefer it.
- `AGENTS.md` "Aktueller Stand: 2 580 nodes" is stale → should read **2 255**.

## Reversible artifacts (this run folder)
`phase_s1_schadstoff_source.py` · `phase_s2_connect.py` · `phase_s3_orphans.py`
(all dry-run→commit, tagged `review_run='regulation_graph_vocab_2026_06_04'`). Rollback: restore the
pre-surgery backup, or delete tagged edges.
