# Final Cleanup F08 — Synthetic PROVEN/PARTIAL audit

**Date:** 2026-06-06T18:19:14.411604+00:00 · **Database:** `mit-bestand`
**Mode:** READ-ONLY Neo4j + ledger scan (no graph writes)
**Input:** [`VERIFICATION_LEDGER_ELEMENT.csv`](../VERIFICATION_LEDGER_ELEMENT.csv)
**Output:** [`ledger/final_cleanup_f08.csv`](../ledger/final_cleanup_f08.csv)

## Scope

PROVEN/PARTIAL rows where **external claims** violate the Evidence Gate:

- empty `proof_quote`, and/or
- `basis_type=logic` (synthetic inherit) on claims that require external attestation

External = P6-new synthetic rows, ledger `basis_type` ∈ {web, dossier}, `basis_ref` URL, live graph evidence URL/quote on element, or actor edges (`VERBUNDEN_MIT_AKTEUR` / `BETEILIGT_AN`). Structural-only `logic` rows (taxonomy/regulation contract) are out of scope.

## Counts

| Metric | Value |
|---|---:|
| Ledger rows scanned | 17,327 |
| External issue rows found | **158** |
| Synthetic rows found (`P6-new` / P6-06 logic) | **36** |
| Synthetic rows fixed from graph | **18** |
| Total rows fixed from graph | **114** |
| Unfixed (no graph quote/URL) | **44** |

## Fix status breakdown

| fix_status | Count |
|---|---:|
| FIXED_NODE_URL | 61 |
| FIXED_REL_QUOTE | 53 |
| UNFIXED | 44 |

## Issue type breakdown

| issue_type | Count |
|---|---:|
| logic_basis | 118 |
| empty_proof_quote+logic_basis | 36 |
| empty_proof_quote | 4 |

## Method

1. Loaded canonical element ledger (`VERIFICATION_LEDGER_ELEMENT.csv`).
2. Exported live graph evidence properties via read-only Cypher (`mit-bestand`).
3. Flagged PROVEN/PARTIAL external rows with empty quote or `logic` basis.
4. Patched rows where graph exposes `evidence_quote`, `source_quote`, `evidence_url`, `source_url`, or node source URLs.
5. Did **not** mutate Neo4j; fixes are ledger-side overrides for F4 merge.

## Residual

Rows with `fix_status=UNFIXED*` still need F2 (19 merge-redirect rels) or F3 (actor/VMA externals) re-proof via WebFetch.
P6-new node rows (5 PruefungNachweis catalog nodes) may remain logic-basis structural existence — downgrade or contract-cite in F4 if no URL on graph.
