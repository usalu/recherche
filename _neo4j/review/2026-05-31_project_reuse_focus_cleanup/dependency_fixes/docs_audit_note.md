# Docs audit — advisory diffs for `_neo4j/REVIEW_BASED_PLAN.md` and `_neo4j/FINAL_REVIEW_PLAN_AUDIT.md`

After the 2026-05-31 cleanup is applied, the following readings in the two
plan/audit docs go silently wrong if they assume a single `:Projekt` label.
Apply these advisories AFTER Phase C is merged.

## REVIEW_BASED_PLAN.md
Add a top-banner note (under the version line):

> **2026-05-31 advisory:** project-level entities are now split across `:Projekt`
> (built reuse projects), `:Programm` (research / funded programmes), `:Tool` /
> `:Software` (reclamation tools and software platforms), and `:Marktmodell`
> (component-exchange marketplaces / Baubörsen). Counts and gap-audits below
> that refer to "projects" are scoped to `:Projekt` ONLY. To get a holistic
> count, add a sibling check across `:Programm`.

## FINAL_REVIEW_PLAN_AUDIT.md
Same banner. Then for each audit gate that uses `MATCH (p:Projekt)`:

- If the gate is about *built reuse* (donor → receiver, components, intervention,
  city/land): leave as `:Projekt`.
- If the gate is about *coverage* (source-density, status modelling, methode
  attachment): add a sibling `:Programm` check or change to label union
  `MATCH (p) WHERE 'Projekt' IN labels(p) OR 'Programm' IN labels(p)`.

The detailed line-by-line rewrites live in
`dependency_fixes/hard_coded_projekt_query_audit.csv`.
