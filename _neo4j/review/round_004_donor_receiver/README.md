# Neo4j Donor/Receiver Research Round 004

This package is the researched follow-up to `round_003_query_donor_receiver`.

## Apply order

1. Import `controlled_terms/controlled_terms.delta.jsonl`.
2. Import/apply `patches/donor_receiver_source_research.patch.jsonl`.
3. Run `cypher/post_patch_donor_receiver_review.cypher`.
4. Inspect `reviews/donor_receiver_research_results.jsonl` for each candidate decision.

## Important rule

Do not create a fake `Bauwerk` donor just to make the graph look complete. When the source only says supplier stock, borrowed pool, construction waste, rest stock, demolition stream, or unknown origin, resolve the Bauteilgruppe with `HAT_RESSOURCENQUELLE` and `donor_resolution_status`.

## Summary

- Candidates reviewed: 49
- Patch operations: 131
- Controlled vocabulary additions: 8
- Source files missing/deferred: 15

