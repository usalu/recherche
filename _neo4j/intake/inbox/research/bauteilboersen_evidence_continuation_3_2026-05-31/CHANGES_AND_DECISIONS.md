# Changes and decisions in continuation 3

## Promoted / strengthened with line-level first-party evidence

- `batiterre`: added/strengthened direct material and Bauteiltyp evidence from BatiTerre shop and reuse-preparation pages, including `mat_holz`, `mat_gusseisen`, `mat_glas`, `mat_kunststoff`, and many component categories. Added a reconditioning candidate, but exact graph ID still needs lookup.
- `baticycle`: strengthened Bauteiltyp coverage from the first-party “Matériaux second oeuvre” page. Reconditioning recorded as lookup-required.
- `genbyg`: added first-party category evidence for doors, windows, glass, and electrical/lighting.
- `reempro`: added first-party marketplace/service evidence for materials (`mat_ziegel`, `mat_keramik`), component types, selective deconstruction, and concrete reconditioning processes.
- `raedificare`: did not invent material IDs; added process/proof candidates for Diagnostic PEMD/Ressource, environmental/carbon balance, and second-life attestation.
- `salza`: kept as broad `bt_mehrere` only; added administrative-final-check candidate. Rejected dismantling link because the page says buyer/seller coordinate demontage, not that Salza performs it.
- `resandes`: added a new high-quality first-party evidence set for historical materials and components.

## Kept as manual-review only

- `cycle_zero`, `cornermat_retrival`, and `materialrest24` include useful evidence but depend partly on third-party or search-extract evidence; they are marked `import_safe_without_manual_review=no` where appropriate.
- `materialenbank_leuven_atelier_circuler` has strong first-party search-extract category evidence, but a fetched line-level catalog page was not available through the tool; verify before automated import if you require only line-level source text.

## Rejections / corrections

- `mat_stahl` was rejected wherever the source only says iron (`Jern`), wrought iron, or generic metal.
- `mat_keramik` was rejected where the source only says `carrelage`, `Fliesen`, or `tiles` without ceramic wording.
- `mat_beton` was rejected for Articonnex “imitation béton” flooring because it describes appearance, not material.
- `Salza` Rueckbauverfahren was rejected from the platform page because it only supports coordination of demontage between buyer and seller.
