# Deferred — insufficient first-party evidence for graph facts

Items from `swiss_reuse_bubble_v2.md` that stay **off-graph** until per-item URL verification.

## Interpretive / analytical (never import as facts)

Sidecar claim ids (graph edges may be `teilweise_belegt` but claims stay off-graph as facts):
- `claim_cirkla_zirkular_ecosystem_overlap`
- `claim_coordination_actors_shared_field`


| Item | Reason |
|---|---|
| §11 matrix scores (reuse intensity, infrastructural potential) | Analytical ratings, not sourced measurements |
| §12 "most important entry point" | Explicitly qualified as interpretation in dossier |
| §12 "clearest in Europe" | Needs comparative European evidence |
| §13 "infrastructural reclaimed-material reuse" label | Synthesis conclusion; keep in ResearchDocument only |
| "Reuse bubble / ecology" framing (§1) | Interpretive conclusion with supporting facts listed separately |

## Actor / node deferrals

| Proposed import | Why deferred | What would unblock |
|---|---|---|
| `roto_reuse` separate from `wick_reuse_roto_baumarkt` | Committee lists ROTO-Reuse affiliation; no dedicated ROTO-Reuse first-party marketplace URL verified | roto-reuse.ch or equivalent operational profile |
| `innosuisse` as `:Akteur` | Mentioned as funder on project pages, not as reuse actor | Innosuisse project page naming SWIRCULAR/legal framework as grantee context only |
| `bfh` as `:Akteur` | SWIRCULAR partner list on ethz page is JS-rendered; partner names not extracted | BFH first-party SWIRCULAR partner statement |
| `overall_stiftung` as `:Akteur` | Overall appears via library-of-reuse (useagain owner) and Cirkla directory | overall.ch / library-of-reuse dedicated profile with operational role |
| Full SWIRCULAR 24-partner roster | Bulk partner list not individually verified | Per-partner first-party URL + role statement |
| SWIRCULAR demonstrator leads (Halter, Roche, Eberhard AG) | Named in ETH news but not per-building reuse participation proof | Demonstrator case-study URLs |

## Edge deferrals

| Edge | Why deferred |
|---|---|
| Planular → specific projects (Grubenstrasse, ELYS, Lysbüchel, KSSU) | planular.net portfolio pages not yet fetched per project |
| Cirkla c/o address → `VERBUNDEN` merge with baubuero | Institutional address ≠ organizational merge; use committee edge instead |
| reMATERIAL® as `:Software` or shop node | No standalone first-party URL in source register (only via Zirkular services page) |
| Öbu, Losinger Marazzi, SUPSI, EPFL committee members → graph | Committee listed but those actors not in Swiss reuse bubble scope / no directory import batch |

## Phase 5 optional

| Item | Status |
|---|---|
| Meta `:Wiederverwendungskette` for 9-step loop (§10) | Deferred — loop is dossier synthesis; step-to-actor mapping needs per-step URL, not summary table |
