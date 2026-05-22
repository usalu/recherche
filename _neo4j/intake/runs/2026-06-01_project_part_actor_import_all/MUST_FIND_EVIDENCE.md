# Must Find Evidence Later

Imported for now:

- all 91 edges from `project_part_actor_edge_enrichment_existing_node_types_2026_06_01`
- all imported edges are tagged with `review_run = project_part_actor_import_all_2026_06_01`
- all imported edges are currently normalized to `evidence_confidence = abgeleitet`
- the source-side JSON confidence is preserved as `import_original_evidence_confidence`
- all imported edges are marked `review_status = needs_source_url_review`

Deliver later:

1. Bind one exact supporting source URL, quote, or page-level proof per imported edge.
2. Confirm whether `planning_actor_component_involvement` edges should stay as `BETEILIGT_AN` or be remodeled more precisely.
3. Review the highest-risk overlap-derived candidates before treating them as signed-off graph facts.

First review packet:

- `Chiro d'Itterbeek / Sanitary block, Dilbeek` -> `Gebruiktebouwmaterialen` (`11` derived-only edges, all overlap-based candidates, all on components that also attach to another actor)
- `UMAR Unit` -> `RotorDC` for `UMAR Magna Glas` and `UMAR Desso-Teppich`
- `ELEMENTA Walkeweg Basel` -> `Bauteilboerse Basel` for `ELEMENTA Baufeld D` and `ELEMENTA Lehm`
- `House of Fraser -> Cleveland Steel & Tubes -> Handrails` because the component naming looks semantically weak
- `Timber Square -> Heyne Tillett Steel / HTS` planning-involvement edges, especially `Demontierbare TGA-/Plant...`

Suggested later query:

```cypher
MATCH (:Akteur)-[r:BETEILIGT_AN {review_run:'project_part_actor_import_all_2026_06_01'}]->(:Bauteilgruppe)
WHERE r.review_status = 'needs_source_url_review'
RETURN r.source_project_name,
       r.actor_name,
       r.bauteilgruppe_name,
       r.evidence_confidence,
       r.connection_kind,
       r.candidate_source_urls
ORDER BY r.source_project_name, r.actor_name, r.bauteilgruppe_name;
```