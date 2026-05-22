# Source Referencing: Three Examples Per Node Type

Generated from live Neo4j database `mit-bestand` on 2026-05-26.

This is a concrete walkthrough of the minimal source rule:

```text
Nodes identify things.
Relationships state facts.
Claims state complex/value facts.
The source goes on the exact fact, not broadly on the node.
```

Important correction:

```text
Markdown/document edges are not source truth.
Dossiers, research files, Bauteilboerse files, and akteursliste_master.md contain URLs.
Those concrete URLs are the source truth.
If an example points to a Dossier/ResearchDocument/registry .md file, read that as lineage/context only until a concrete URL is copied onto the fact.
```

For each node label below, there are three live examples from the graph.

## `DataIssue`

Type meaning: a review/problem marker. Current count: 29061.

### Example 1

Node: `id=di_actor_stub__CITYFOERSTER__p_recyclinghaus_hannover; status=open; severity=medium; ref_id=r_CITYFOERSTER__ASSOZIIERT_MIT_PROJEKT__p_recyclinghaus_hannover`

- This `DataIssue` node is a review/problem marker.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

### Example 2

Node: `id=di_actor_stub__Lendager__p_resource_rows_copenhagen; status=open; severity=medium; ref_id=r_Lendager__ASSOZIIERT_MIT_PROJEKT__p_resource_rows_copenhagen`

- This `DataIssue` node is a review/problem marker.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

### Example 3

Node: `id=di_actor_stub__Lendager__p_upcycle_studios_copenhagen; status=open; severity=medium; ref_id=r_Lendager__ASSOZIIERT_MIT_PROJEKT__p_upcycle_studios_copenhagen`

- This `DataIssue` node is a review/problem marker.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

## `Quelle`

Type meaning: a source or URL metadata node. Current count: 5343.

### Example 1

Node: `id=q_55_great_suffolk_street_london_md; name=55_Great_Suffolk_Street_…; text_content_retry_result=resolved; source_count=6`

- This `Quelle` node is a source or URL metadata node.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 2

Node: `id=q_55_great_suffolk_street_london_s1; name=ASBP — 55 Great Suffolk Street case study; url=https://asbp.org.uk/case-studies/55-great-suffolk-street; url_status=reachable_2xx`

- This `Quelle` node is a source or URL metadata node. It stores `https://asbp.org.uk/case-studies/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 3

Node: `id=q_55_great_suffolk_street_london_s2; name=New London Architecture — 55 Great Suffolk Street; url=https://www.nla.london/projects/55-great-suffolk-street; url_status=reachable_2xx`

- This `Quelle` node is a source or URL metadata node. It stores `https://www.nla.london/projects/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

## `ExternalLink`

Type meaning: a URL metadata node. Current count: 5026.

### Example 1

Node: `id=q_55_great_suffolk_street_london_s1; name=ASBP — 55 Great Suffolk Street case study; url=https://asbp.org.uk/case-studies/55-great-suffolk-street; url_status=reachable_2xx`

- This `ExternalLink` node is a URL metadata node. It stores `https://asbp.org.uk/case-studies/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 2

Node: `id=q_55_great_suffolk_street_london_s2; name=New London Architecture — 55 Great Suffolk Street; url=https://www.nla.london/projects/55-great-suffolk-street; url_status=reachable_2xx`

- This `ExternalLink` node is a URL metadata node. It stores `https://www.nla.london/projects/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 3

Node: `id=q_55_great_suffolk_street_london_s3; name=Hawkins\Brown — 55 Great Suffolk Street; url=https://www.hawkinsbrown.com/projects/55-great-suffolk-street; url_status=reachable_2xx`

- This `ExternalLink` node is a URL metadata node. It stores `https://www.hawkinsbrown.com/projects/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

## `DossierEntityTarget`

Type meaning: a value or row extracted from a dossier. Current count: 2591.

### Example 1

Node: `id=det_0020ded6015328ef18e11bbf; name=Fläche Gesamtprojekt; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.340742+00:00`

- This `DossierEntityTarget` node is a value or row extracted from a dossier: `Fläche Gesamtprojekt`.
- The dossier row is only context.
- The source truth is the concrete URL from that dossier row/source field, copied onto the fact or Claim as `source_status: exact`.

### Example 2

Node: `id=det_004186f92418ba6ed0c60186; name=Betonblöcke Surplus; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.304667+00:00`

- This `DossierEntityTarget` node is a value or row extracted from a dossier: `Betonblöcke Surplus`.
- The dossier row is only context.
- The source truth is the concrete URL from that dossier row/source field, copied onto the fact or Claim as `source_status: exact`.

### Example 3

Node: `id=det_0041ac8f71cf7115117459c5; name=22 Wandplatten, 27 Deckenplatten; unfolding_kind=dossier_row; created_at_utc=2026-05-22T15:56:47.416125+00:00`

- This `DossierEntityTarget` node is a value or row extracted from a dossier: `22 Wandplatten, 27 Deckenplatten`.
- The dossier row is only context.
- The source truth is the concrete URL from that dossier row/source field, copied onto the fact or Claim as `source_status: exact`.

## `Akteur`

Type meaning: an actor such as an office, person, company, institution, or group. Current count: 648.

### Example 1

Node: `id=2emain_be; name=2emain.be; migration_origin= | mig_s5_visibility | mig_qext_b_source_urls | mig_qext_c_primary_sourc...; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00`

- This `Akteur` node is an actor such as an office, person, company, institution, or group. Keep identity like name/id on the node.
- The fact is represented by this relationship: `Akteur ->[:BELEGT_IN] Quelle:Dossier Maison_Vignette_Auderghe…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=2hs; name=2hs; actor_registry_loader_seen=agent10; migration_origin= | mig_s5_visibility | mig_qext_b_source_urls`

- This `Akteur` node is an actor such as an office, person, company, institution, or group. Keep identity like name/id on the node.
- This relationship, `Akteur ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that actor row is copied onto the actor fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=3xn; name=3XN; actor_registry_loader_seen=agent10; migration_origin= | mig_s5_visibility | mig_qext_b_source_urls`

- This `Akteur` node is an actor such as an office, person, company, institution, or group. Keep identity like name/id on the node.
- This relationship, `Akteur ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that actor row is copied onto the actor fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `SectionRef`

Type meaning: a pointer to a section inside a source/document. Current count: 641.

### Example 1

Node: `id=q_55_great_suffolk_street_london_s1; name=ASBP — 55 Great Suffolk Street case study; url=https://asbp.org.uk/case-studies/55-great-suffolk-street; url_status=reachable_2xx`

- This `SectionRef` node is a pointer to a section inside a source/document. It stores `https://asbp.org.uk/case-studies/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 2

Node: `id=q_55_great_suffolk_street_london_s2; name=New London Architecture — 55 Great Suffolk Street; url=https://www.nla.london/projects/55-great-suffolk-street; url_status=reachable_2xx`

- This `SectionRef` node is a pointer to a section inside a source/document. It stores `https://www.nla.london/projects/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 3

Node: `id=q_55_great_suffolk_street_london_s3; name=Hawkins\Brown — 55 Great Suffolk Street; url=https://www.hawkinsbrown.com/projects/55-great-suffolk-street; url_status=reachable_2xx`

- This `SectionRef` node is a pointer to a section inside a source/document. It stores `https://www.hawkinsbrown.com/projects/55-great-suffolk-street`.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

## `ResearchDocument`

Type meaning: a research/import document record. Current count: 403.

### Example 1

Node: `id=q_aufbereitungsverfahren_reused_building_elements_md; name=aufbereitungsverfahren_reused_building_elements.md; title=Aufbereitungsverfahren for Reused Building Elements; last_seen_by=agent10_phase4b_2`

- This `ResearchDocument` node is a research/import document record.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 2

Node: `id=q_bauteilreuse_legal_regime_matrix_md; name=bauteilreuse_legal_regime_matrix.md; title=Legal and regulatory conditions affecting Bauteilreuse; last_seen_by=agent10_phase4b_2`

- This `ResearchDocument` node is a research/import document record.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 3

Node: `id=q_circular_construction_economics_kg_md; name=circular_construction_economics_kg.md; title=Economic Dimension of a Circular Construction Knowledge Graph; last_seen_by=agent10_phase4b_2`

- This `ResearchDocument` node is a research/import document record.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

## `Bauteilgruppe`

Type meaning: a reusable group of building components. Current count: 369.

### Example 1

Node: `id=bg_dismantled_glas_technik_medunicampus_fluorescent; name=MedUni Leuchtstoffr.; name_full=MedUni Mariannengasse — Fluorescent tubes (hazardous removal, not reuse); primary_material_id=mat_glas`

- This `Bauteilgruppe` node is a reusable group of building components. The node names the concept/category/value.
- The fact is represented by this relationship: `Bauteilgruppe ->[:BELEGT_IN] Quelle:Dossier MedUni Campus Mariannengasse Wien`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bg_dismantled_holz_mehrere_circl_larch_structure; name=Circl Lärchentragwerk; name_full=Circl — Fully demountable locally-sourced larch timber support structure...; primary_material_id=mat_holz`

- This `Bauteilgruppe` node is a reusable group of building components. The node names the concept/category/value.
- The fact is represented by this relationship: `Bauteilgruppe ->[:BELEGT_IN] Quelle:Dossier Circl Pavilion Amsterdam`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bg_dismantled_holz_mehrere_stuttgart21_donor_stock; name=S21 CLT-Lager; name_full=Stuttgart 21 Hauptbahnhof — 78 CLT formwork elements secured in depot fo...; primary_material_id=mat_holz`

- This `Bauteilgruppe` node is a reusable group of building components. The node names the concept/category/value.
- The fact is represented by this relationship: `Bauteilgruppe ->[:BELEGT_IN] Quelle:Dossier Stuttgart 210`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: missing`; do not invent a URL.

## `Kennwert`

Type meaning: a measured or calculated value. Current count: 258.

### Example 1

Node: `id=kw_p_55_great_suffolk_street_london_co2_saving_0; kennwert=co2_einsparung_t; wert=50.0; loader=unknown`

- This `Kennwert` node is a measured or calculated value. Keep identity like name/id on the node.
- The source belongs on this relationship: `Kennwert <-[:HAT_KENNWERT] Projekt 55 Great Suffolk Street`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=kw_p_55_great_suffolk_street_london_cost_0; kennwert=CO₂-Einsparung Stahlreuse; wert=50.0; method=Vergleich zu A1-A3 2.5 kgCO₂e/kg steel`

- This `Kennwert` node is a measured or calculated value. Keep identity like name/id on the node.
- The source belongs on this relationship: `Kennwert <-[:HAT_KENNWERT] Projekt 55 Great Suffolk Street`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=kw_p_55_great_suffolk_street_london_cost_1; kennwert=Kosten; method=—; loader=agent9_phase4b1`

- This `Kennwert` node is a measured or calculated value. Keep identity like name/id on the node.
- The source belongs on this relationship: `Kennwert <-[:HAT_KENNWERT] Projekt 55 Great Suffolk Street`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Bauwerk`

Type meaning: a building or built object. Current count: 186.

### Example 1

Node: `id=bw_1_broadgate_1_2_broadgate_donor_stahl; name=1 Broadgate; name_full=1 Broadgate / 1–2 Broadgate Donor-Stahl; migration_origin= | mig_s5_visibility | mig_qext_b_source_urls | mig_qext_c_primary_sourc...`

- This `Bauwerk` node is a building or built object. Keep identity like name/id on the node.
- The fact is represented by this relationship: `Bauwerk ->[:BELEGT_IN] Quelle:Dossier Roots_in_the_Sky_Blackfr…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=bw_1_broadgate_london; name=1 Broadgate, London; migration_origin= | mig_s5_visibility | mig_qext_b_source_urls | mig_qext_c_primary_sourc...; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00`

- This `Bauwerk` node is a building or built object. Keep identity like name/id on the node.
- The fact is represented by this relationship: `Bauwerk ->[:BELEGT_IN] Quelle:Dossier 55_Great_Suffolk_Street_…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=bw_318_oxford_street_house_of_fraser; name=318 Oxford Street; name_full=318 Oxford Street / former House of Fraser / The Elephant; nutzung_text=ehemaliges Department Store, Donor und Self-Reuse-Projekt`

- This `Bauwerk` node is a building or built object. Keep identity like name/id on the node.
- The fact is represented by this relationship: `Bauwerk ->[:BELEGT_IN] Quelle:Dossier House_of_Fraser_318_Oxfo…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `PruefungNachweis`

Type meaning: a test, proof, verification, or evidence type. Current count: 120.

### Example 1

Node: `id=pn_ankerpruefung; name=pn_ankerpruefung; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `PruefungNachweis` node is a test, proof, verification, or evidence type. The node names the concept/category/value.
- This relationship, `PruefungNachweis ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the proof fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=pn_anwendungsbeschraenkung; name=pn_anwendungsbeschraenkung; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `PruefungNachweis` node is a test, proof, verification, or evidence type. The node names the concept/category/value.
- This relationship, `PruefungNachweis ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the proof fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=pn_approval_process; name=pn_approval_process; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `PruefungNachweis` node is a test, proof, verification, or evidence type. The node names the concept/category/value.
- This relationship, `PruefungNachweis ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the proof fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Norm`

Type meaning: a standard or regulation. Current count: 103.

### Example 1

Node: `id=norm_bbl_nen; name=Bbl/NEN; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls`

- This `Norm` node is a standard or regulation. The node names the concept/category/value.
- The source belongs on this relationship: `Norm <-[:REFERENZIERT_NORM] ReuseRule Niederlande × Beton reuse rule`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=norm_bbl_nen_links; name=Bbl/NEN links; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls`

- This `Norm` node is a standard or regulation. The node names the concept/category/value.
- The source belongs on this relationship: `Norm <-[:REFERENZIERT_NORM] ReuseRule Niederlande × Stahl reuse rule`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=norm_bs_4978; name=BS 4978; evidence_basis=reuse_rule_key_norm; migration_origin=mig_qext_b_source_urls`

- This `Norm` node is a standard or regulation. The node names the concept/category/value.
- The source belongs on this relationship: `Norm <-[:REFERENZIERT_NORM] ReuseRule Vereinigtes Königreich × Holz reuse rule`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Projekt`

Type meaning: a project or case study. Current count: 101.

### Example 1

Node: `id=p_55_great_suffolk_street_london; name=55 Great Suffolk Street; name_full=55 Great Suffolk Street, London; year_completed=2024`

- This `Projekt` node is a project or case study. Keep identity like name/id on the node.
- The fact is represented by this relationship: `Projekt ->[:BELEGT_IN] Quelle:Dossier 55_Great_Suffolk_Street_…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=p_association_house_groeditz; name=Vereinshaus Gröditz; name_full=Association house, Gröditz; year_completed=2007`

- This `Projekt` node is a project or case study. Keep identity like name/id on the node.
- The source belongs on this relationship: `Projekt ->[:BELEGT_IN] Quelle:ExternalLink Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): Reuse...`, because that is the actual fact.
- `source_status: exact`, `source_url: https://doi.org/10.1016/j.jclepro.2022.135235`.

### Example 3

Node: `id=p_association_house_plauen; name=Vereinshaus Plauen; name_full=Association house, Plauen; year_completed=2007`

- This `Projekt` node is a project or case study. Keep identity like name/id on the node.
- The source belongs on this relationship: `Projekt ->[:BELEGT_IN] Quelle:ExternalLink Küpfer, C.; Bastien-Masse, M.; Fivet, C. (2023): Reuse...`, because that is the actual fact.
- `source_status: exact`, `source_url: https://doi.org/10.1016/j.jclepro.2022.135235`.

## `Dossier`

Type meaning: a source dossier or source package. Current count: 100.

### Example 1

Node: `id=q_55_great_suffolk_street_london_md; name=55_Great_Suffolk_Street_…; text_content_retry_result=resolved; source_count=6`

- This `Dossier` node is a source dossier or source package.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 2

Node: `id=q_architecture_of_reuse_brussels_md; name=Architecture of Reuse Brussels; migration_origin= | r7_d_text_content | mig_s4_a_secondary_labels | mig_s4_b_text_strip; text_content_chars_pre_strip=14698`

- This `Dossier` node is a source dossier or source package.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

### Example 3

Node: `id=q_association_house_groeditz_md; name=Association_house_Groedi…; text_content_retry_result=resolved; source_count=4`

- This `Dossier` node is a source dossier or source package.
- Use it as source inventory/metadata only.
- A real project/material/actor fact still needs its own `source_url` on the exact relationship or Claim.

## `Stadt`

Type meaning: a city. Current count: 76.

### Example 1

Node: `id=stadt_aarhus; name=Aarhus; source_scope=controlled_vocab_seed`

- This `Stadt` node is a city. The node names the concept/category/value.
- The fact is represented by this relationship: `Stadt ->[:BELEGT_IN] Quelle:Dossier TRAE_High_Rise_Aarhus.md`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=stadt_amsterdam; name=Amsterdam; source_scope=case_markdown`

- This `Stadt` node is a city. The node names the concept/category/value.
- The fact is represented by this relationship: `Stadt ->[:BELEGT_IN] Quelle:Dossier Circl Pavilion Amsterdam`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=stadt_arnhem; name=Arnhem; source_scope=controlled_vocab_seed`

- This `Stadt` node is a city. The node names the concept/category/value.
- The fact is represented by this relationship: `Stadt ->[:BELEGT_IN] Quelle:Dossier Circular_Centre_Netherla…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Aufbereitungsverfahren`

Type meaning: a preparation or processing method. Current count: 62.

### Example 1

Node: `id=av_aluminium_oberflaechenbehandlung; name=av_aluminium_oberflaechenbehandlung; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Aufbereitungsverfahren` node is a preparation or processing method. The node names the concept/category/value.
- This relationship, `Aufbereitungsverfahren ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the method fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=av_aluminium_reinigung_entdichtung; name=Aluminium-Reinigung + Entdichtung; last_seen_by=agent10_phase4b_2; scope_note=Cleaning of aluminium profiles + removal of old gaskets, glue, hardware.`

- This `Aufbereitungsverfahren` node is a preparation or processing method. The node names the concept/category/value.
- This relationship, `Aufbereitungsverfahren ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the method fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=av_aluminium_zuschnitt_bohrung; name=Aluminium-Zuschnitt + Bohrung + Profilanpassung; last_seen_by=agent10_phase4b_2; scope_note=Cutting + drilling + dimensional adaptation of aluminium profiles for re...`

- This `Aufbereitungsverfahren` node is a preparation or processing method. The node names the concept/category/value.
- This relationship, `Aufbereitungsverfahren ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the method fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Leistungsanforderung`

Type meaning: a performance requirement. Current count: 46.

### Example 1

Node: `id=la_aesthetik; name=la_aesthetik; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Leistungsanforderung` node is a performance requirement. The node names the concept/category/value.
- This relationship, `Leistungsanforderung ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the requirement fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=la_angemessene_anwendung; name=la_angemessene_anwendung; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Leistungsanforderung` node is a performance requirement. The node names the concept/category/value.
- This relationship, `Leistungsanforderung ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the requirement fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=la_arbeitsschutz; name=la_arbeitsschutz; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Leistungsanforderung` node is a performance requirement. The node names the concept/category/value.
- This relationship, `Leistungsanforderung ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the requirement fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Programm`

Type meaning: a program or initiative. Current count: 29.

### Example 1

Node: `id=p_architecture_of_reuse_brussels; name=Architecture of Reuse…; name_full=Architecture of Reuse Brussels; migration_origin=5_3_relabel_to_programm | mig_qext_b_source_urls | mig_qext_c_primary_so...`

- This `Programm` node is a program or initiative. The node names the concept/category/value.
- This relationship, `Programm ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that registry row is copied onto the program fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=p_eth_circular_construction_programme; name=ETH Circular Construction Programme; evidence_basis=dossier_anchored; migration_origin=mig_r7_b_resolve_orphans | mig_qext_b_source_urls | mig_qext_c_primary_s...`

- This `Programm` node is a program or initiative. The node names the concept/category/value.
- The fact is represented by this relationship: `Programm ->[:BELEGT_IN] Quelle:Dossier ETH Circular Construction Programme`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=p_reuse_in_construction_zhaw; name=Reuse in Construction; name_full=Reuse in Construction / ZHAW; migration_origin=5_3_relabel_to_programm | mig_qext_b_source_urls | mig_qext_c_primary_so...`

- This `Programm` node is a program or initiative. The node names the concept/category/value.
- This relationship, `Programm ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that registry row is copied onto the program fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Huerde`

Type meaning: a barrier or obstacle. Current count: 28.

### Example 1

Node: `id=h_akzeptanzproblem; name=Akzeptanzproblem; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Huerde` node is a barrier or obstacle. The node names the concept/category/value.
- The source belongs on this relationship: `Huerde ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=h_anschlussproblem; name=Anschlussproblem; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Huerde` node is a barrier or obstacle. The node names the concept/category/value.
- The source belongs on this relationship: `Huerde ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=h_aufbereitungsaufwand; name=Aufbereitungsaufwand; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Huerde` node is a barrier or obstacle. The node names the concept/category/value.
- The source belongs on this relationship: `Huerde ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Material`

Type meaning: a material. Current count: 26.

### Example 1

Node: `id=mat_aluminium; name=Aluminium; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Material` node is a material. The node names the concept/category/value.
- This relationship, `Material ->[:BELEGT_IN] Quelle:ResearchDocument aufbereitungsverfahren_reused_building_elements.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the material fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=mat_beton; name=Beton; migration_origin=mig_qext_b_source_urls; strict_source_url_cleanup_at=2026-05-23T11:01:59.122927+00:00`

- This `Material` node is a material. The node names the concept/category/value.
- The source belongs on this relationship: `Material <-[:APPLIES_TO] ReuseRule Belgien × Beton reuse rule`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=mat_bitumen; name=Bitumen; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Material` node is a material. The node names the concept/category/value.
- The source belongs on this relationship: `Material ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Akteurrolle`

Type meaning: a role an actor can have. Current count: 24.

### Example 1

Node: `id=ar_aufbereitung_refurbishment; name=Aufbereitung_Refurbishment; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Akteurrolle` node is a role an actor can have. The node names the concept/category/value.
- The source belongs on this relationship: `Akteurrolle <-[:HAT_AKTEURROLLE] Akteur Granby Workshop`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=ar_bauausfuehrung_fertigung; name=Bauausfuehrung_Fertigung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Akteurrolle` node is a role an actor can have. The node names the concept/category/value.
- The source belongs on this relationship: `Akteurrolle <-[:HAT_AKTEURROLLE] Akteur HFT Stuttgart`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=ar_bauherr_auftraggeber; name=Bauherr_Auftraggeber; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Akteurrolle` node is a role an actor can have. The node names the concept/category/value.
- The source belongs on this relationship: `Akteurrolle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bauteiltyp`

Type meaning: a component type. Current count: 23.

### Example 1

Node: `id=bt_ausbau; name=Ausbau; source_resolution_status=needs_source_url_review; brand_layer=space_plan`

- This `Bauteiltyp` node is a component type. The node names the concept/category/value.
- The source belongs on this relationship: `Bauteiltyp ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bt_boden; name=Boden; source_resolution_status=needs_source_url_review; brand_layer=space_plan`

- This `Bauteiltyp` node is a component type. The node names the concept/category/value.
- The source belongs on this relationship: `Bauteiltyp ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bt_dach; name=Dach; source_resolution_status=needs_source_url_review; brand_layer=skin`

- This `Bauteiltyp` node is a component type. The node names the concept/category/value.
- The source belongs on this relationship: `Bauteiltyp ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Materialdepot`

Type meaning: a material depot or storage/source place. Current count: 23.

### Example 1

Node: `id=bw_bellastock_ville_des_terres_l_ile_saint_denis_lager; name=Bellastock Ville des…; name_full=Bellastock Ville des Terres / L’Île-Saint-Denis Lager; is_material_depot=True`

- This `Materialdepot` node is a material depot or storage/source place. The node names the concept/category/value.
- The fact is represented by this relationship: `Materialdepot ->[:BELEGT_IN] Quelle:Dossier Resilience_La_Ferme_des_…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=bw_berlin_fitout_donor_sources; name=Berlin donors; name_full=Aggregierte Donorquellen: Boros/Berghain-Ausstellung, andere Baustellen,...; nutzung_text=Donorquellen für Interior-Reuse`

- This `Materialdepot` node is a material depot or storage/source place. The node names the concept/category/value.
- The fact is represented by this relationship: `Materialdepot ->[:BELEGT_IN] Quelle:Dossier Impact_Hub_Berlin_CRCLR_…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=bw_chiro_itterbeek_reuse_supply_network; name=Reuse-/Surplus-Liefernet…; name_full=Reuse-/Surplus-Liefernetz Chiro d’Itterbeek; is_material_depot=True`

- This `Materialdepot` node is a material depot or storage/source place. The node names the concept/category/value.
- The fact is represented by this relationship: `Materialdepot ->[:BELEGT_IN] Quelle:Dossier Chiro_d_Itterbeek_Dilbee…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `ReuseRule`

Type meaning: a reuse rule. Current count: 20.

### Example 1

Node: `id=rr_be_beton; name=Belgien × Beton reuse rule; evidence_basis=research_file_row; source_count=1`

- This `ReuseRule` node is a reuse rule. The node names the concept/category/value.
- The source belongs on this relationship: `ReuseRule ->[:HAS_SOURCE_LINK] Quelle:ExternalLink f/waste/studies/deliverables/CDW_Belgium_Factsheet_Fin...`, because that is the actual fact.
- `source_status: exact`, `source_url: https://ec.europa.eu/environment/pdf/waste/studies/deliverables/CDW_Belgium_Factsheet_Fina...`.

### Example 2

Node: `id=rr_be_holz; name=Belgien × Holz reuse rule; evidence_basis=research_file_row; source_count=1`

- This `ReuseRule` node is a reuse rule. The node names the concept/category/value.
- The source belongs on this relationship: `ReuseRule ->[:HAS_SOURCE_LINK] Quelle:ExternalLink sites/default/files/2023-10/en_id2023_fcrbe_finition_w...`, because that is the actual fact.
- `source_status: exact`, `source_url: https://opalis.eu/sites/default/files/2023-10/en_id2023_fcrbe_finition_web.pdf`.

### Example 3

Node: `id=rr_be_naturstein; name=Belgien × Naturstein reuse rule; evidence_basis=research_file_row; source_count=1`

- This `ReuseRule` node is a reuse rule. The node names the concept/category/value.
- The source belongs on this relationship: `ReuseRule ->[:HAS_SOURCE_LINK] Quelle:ExternalLink iles/2022-01/4.10_en_-_natural_stone_flooring_slab_v01...`, because that is the actual fact.
- `source_status: exact`, `source_url: https://opalis.eu/sites/default/files/2022-01/4.10_en_-_natural_stone_flooring_slab_v01_0....`.

## `Land`

Type meaning: a country. Current count: 19.

### Example 1

Node: `id=land_belgien; name=Belgien; actor_registry_loader_seen=agent10; pcb_verbot_jahr=1986`

- This `Land` node is a country. The node names the concept/category/value.
- This relationship, `Land ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that registry row is copied onto the country/location fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=land_daenemark; name=Dänemark; actor_registry_loader_seen=agent10; pcb_verbot_jahr=1986`

- This `Land` node is a country. The node names the concept/category/value.
- This relationship, `Land ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that registry row is copied onto the country/location fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=land_deutschland; name=Deutschland; actor_registry_loader_seen=agent10; kmf_grenzwert_jahr=1996`

- This `Land` node is a country. The node names the concept/category/value.
- This relationship, `Land ->[:ANCHORED_BY] OntologyAnchor akteursliste_master.md`, is only registry lineage. It becomes evidence only when the concrete link from that registry row is copied onto the country/location fact or Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Software`

Type meaning: a software tool. Current count: 19.

### Example 1

Node: `id=software_bim; name=Building Information Modeling / BIM; source_resolution_status=needs_source_url_review; kind=software`

- This `Software` node is a software tool. The node names the concept/category/value.
- The source belongs on this relationship: `Software ->[:NUTZT_SOFTWARE] Software:Tool BIM / digitaler Bauteilkatalog`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=software_concular; name=Concular; kind=software; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Software` node is a software tool. The node names the concept/category/value.
- The fact is represented by this relationship: `Software ->[:BELEGT_IN] Quelle:Dossier Impact_Hub_Berlin_CRCLR_…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=software_ecotool; name=EcoTool; name_full=EcoTool — ökologische Bilanz (Pflichtnachweis Wettbewerb Lysbüchel); source_resolution_status=needs_source_url_review`

- This `Software` node is a software tool. The node names the concept/category/value.
- The source belongs on this relationship: `Software <-[:NUTZT_SOFTWARE] Projekt ELEMENTA Walkeweg`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Ressourcenquelle`

Type meaning: a resource source. Current count: 16.

### Example 1

Node: `id=rq_baustelle; name=Baustelle; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Ressourcenquelle` node is a resource source. The node names the concept/category/value.
- The source belongs on this relationship: `Ressourcenquelle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=rq_bauteilboerse; name=Bauteilboerse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Ressourcenquelle` node is a resource source. The node names the concept/category/value.
- The source belongs on this relationship: `Ressourcenquelle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=rq_borrowed_material_pool; name=Borrowed_Material_Pool; datenqualitaet=Belegt; migration_origin=mig_qext_b_source_urls`

- This `Ressourcenquelle` node is a resource source. The node names the concept/category/value.
- The source belongs on this relationship: `Ressourcenquelle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bauproduktstatus`

Type meaning: a product/status category. Current count: 15.

### Example 1

Node: `id=bps_abz_abg; name=abZ / aBG (DE); name_full=abZ / aBG (DE, allgemeine bauaufsichtliche Zulassung); scope_note=DIBt allgemeine Zulassung for non-standard German construction products.`

- This `Bauproduktstatus` node is a product/status category. The node names the concept/category/value.
- The source belongs on this relationship: `Bauproduktstatus ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bps_baupg_ch; name=BauPG (CH); name_full=BauPG-Status (CH, Schweizer Bauprodukteverordnung); scope_note=Swiss construction-products regime under BauPG.`

- This `Bauproduktstatus` node is a product/status category. The node names the concept/category/value.
- The source belongs on this relationship: `Bauproduktstatus ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bps_bestand_no_status; name=Bestand vor Ort; name_full=Bestand vor Ort weiterverwendet (kein neues Inverkehrbringen); scope_note=On-site reuse without placing the element on the market — no Bauprodukts...`

- This `Bauproduktstatus` node is a product/status category. The node names the concept/category/value.
- The source belongs on this relationship: `Bauproduktstatus ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `RechtlicheBedingung`

Type meaning: a legal condition. Current count: 15.

### Example 1

Node: `id=rb_bauordnungsrecht; name=Bauordnungsrecht; evidence_basis=controlled_vocab; scope_note=Building approval law applies in every corpus country; specific instrume...`

- This `RechtlicheBedingung` node is a legal condition. The node names the concept/category/value.
- This relationship, `RechtlicheBedingung ->[:BELEGT_IN] Quelle:ResearchDocument bauteilreuse_legal_regime_matrix.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the legal-condition fact or Claim.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=rb_bauproduktenverordnung_cpr; name=Bauproduktenverordnung (CPR); evidence_basis=registry_stub; migration_origin=mig_r2_c_restore_legal | mig_qext_b_source_urls | mig_qext_c_primary_sou...`

- This `RechtlicheBedingung` node is a legal condition. The node names the concept/category/value.
- This relationship, `RechtlicheBedingung ->[:BELEGT_IN] Quelle:ResearchDocument bauteilreuse_legal_regime_matrix.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the legal-condition fact or Claim.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=rb_boulder_deconstruction_ordinance_8366; name=Boulder Deconstruction Ordinance 8366 / 2020; evidence_basis=controlled_vocab; is_universal=False`

- This `RechtlicheBedingung` node is a legal condition. The node names the concept/category/value.
- This relationship, `RechtlicheBedingung ->[:BELEGT_IN] Quelle:ResearchDocument bauteilreuse_legal_regime_matrix.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the legal-condition fact or Claim.
- `source_status: missing`; do not invent a URL.

## `Verbindungstechnik`

Type meaning: a connection or joining technique. Current count: 15.

### Example 1

Node: `id=vt_bolzenverbindung; name=Bolzenverbindung; last_seen_by=agent10_phase4b_2; source_resolution_status=needs_source_url_review`

- This `Verbindungstechnik` node is a connection or joining technique. The node names the concept/category/value.
- The source belongs on this relationship: `Verbindungstechnik ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=vt_demontierbarer_schwerlastanker; name=Demontierbarer Schwerlastanker; last_seen_by=agent10_phase4b_2; source_resolution_status=needs_source_url_review`

- This `Verbindungstechnik` node is a connection or joining technique. The node names the concept/category/value.
- The source belongs on this relationship: `Verbindungstechnik ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=vt_holzduebel; name=vt_holzduebel; last_seen_by=agent10_phase4b_2; source_resolution_status=needs_source_url_review`

- This `Verbindungstechnik` node is a connection or joining technique. The node names the concept/category/value.
- This relationship, `Verbindungstechnik ->[:BELEGT_IN] Quelle:ResearchDocument connection_techniques_bauteilreuse.md`, is research-document lineage. It becomes evidence only when the concrete URL from the relevant row/section is copied onto the connection-technique fact or Claim.
- `source_status: missing`; do not invent a URL.

## `Wiederverwendungskette`

Type meaning: a reuse chain. Current count: 14.

### Example 1

Node: `id=k_bestandserhalt_blackfriars_tragstruktur; name=Bestandserhalt Blackfria…; name_full=Bestandserhalt Blackfriars Tragstruktur; methodische_abgrenzung=Bestandserhalt nicht als Direct Reuse werten`

- This `Wiederverwendungskette` node is a reuse chain. The node names the concept/category/value.
- The fact is represented by this relationship: `Wiederverwendungskette ->[:BELEGT_IN] Quelle:Dossier Roots_in_the_Sky_Blackfr…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 2

Node: `id=k_geplante_reuse_kette_broadgate_stahl_nach_blackfriars; name=Geplante Reuse-Kette…; name_full=Geplante Reuse-Kette Broadgate-Stahl nach Blackfriars; status=geplant / nicht gebaut bestätigt`

- This `Wiederverwendungskette` node is a reuse chain. The node names the concept/category/value.
- The fact is represented by this relationship: `Wiederverwendungskette ->[:BELEGT_IN] Quelle:Dossier Roots_in_the_Sky_Blackfr…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=k_reuse_kette_brettschichtholzbogen_liege_bierset_nach_anderlecht; name=Reuse-Kette Brettschicht…; name_full=Reuse-Kette Brettschichtholzbögen Liège/Bierset nach Anderlecht; migration_origin=mig_qext_b_source_urls | mig_qext_c_primary_source_url`

- This `Wiederverwendungskette` node is a reuse chain. The node names the concept/category/value.
- The fact is represented by this relationship: `Wiederverwendungskette ->[:BELEGT_IN] Quelle:Dossier Recypark_Demets_Anderlec…`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `DeprecatedType`

Type meaning: an old/superseded type. Current count: 13.

### Example 1

Node: `id=dep_label__GraphVersion; reason=Experimental versioning label — never populated.; evidence_basis=audit_record; old_name=GraphVersion`

- This `DeprecatedType` node is an old/superseded type.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

### Example 2

Node: `id=dep_label__LebenszyklusModul; reason=Renamed in R2.b — original IDs (lz_*) preserved on new nodes.; evidence_basis=audit_record; old_name=LebenszyklusModul`

- This `DeprecatedType` node is an old/superseded type.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

### Example 3

Node: `id=dep_label__ZertifizierungBewertungssystem; reason=Renamed in R2.d for brevity — old name preserved as alias on new nodes.; evidence_basis=audit_record; old_name=ZertifizierungBewertungssystem`

- This `DeprecatedType` node is an old/superseded type.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

## `Methode`

Type meaning: a method. Current count: 13.

### Example 1

Node: `id=meth_abrissmonitoring; name=Abrissmonitoring; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Methode` node is a method. The node names the concept/category/value.
- The source belongs on this relationship: `Methode ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=meth_bauteilkatalogisierung; name=Bauteilkatalogisierung; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Methode` node is a method. The node names the concept/category/value.
- The source belongs on this relationship: `Methode ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=meth_building_material_scouting; name=Building_Material_Scouting; source_resolution_status=needs_source_url_review; source_trace_migration=mig_trace_zitiert_quelle_to_urls_2026_05_23`

- This `Methode` node is a method. The node names the concept/category/value.
- The source belongs on this relationship: `Methode ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Wirtschaft`

Type meaning: an economic/business concept. Current count: 12.

### Example 1

Node: `id=wi_capex_hoeher_marketing_payback; name=CapEx höher, Marketing-/Branding-Payback; scope_note=Reuse-Mehrkosten amortisieren über PR/Positionierung/Marktdifferenzierun...; migration_origin=mig_qext_b_source_urls`

- This `Wirtschaft` node is an economic/business concept. The node names the concept/category/value.
- The source belongs on this relationship: `Wirtschaft ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=wi_capex_hoeher_opex_payback; name=CapEx höher, Payback über OpEx / LCA; scope_note=Upfront-Mehrkosten amortisieren über Lebenszyklusvorteile (Wartung, Ener...; migration_origin=mig_qext_b_source_urls`

- This `Wirtschaft` node is an economic/business concept. The node names the concept/category/value.
- The source belongs on this relationship: `Wirtschaft ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=wi_capex_hoeher_subvention; name=CapEx höher, Subvention/Förderung deckt Mehrkosten; scope_note=Reuse-Mehrkosten durch öffentliche Förderung oder Forschungsfinanzierung...; migration_origin=mig_qext_b_source_urls`

- This `Wirtschaft` node is an economic/business concept. The node names the concept/category/value.
- The source belongs on this relationship: `Wirtschaft ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Marktmodell`

Type meaning: a market model. Current count: 11.

### Example 1

Node: `id=mm_forschungsprojekt_zuteilung; name=Forschungs-Zuteilung; name_full=Forschungsprojekt-Zuteilung; scope_note=Allocation via research project (UMAR, ReCreate pilots, etc.).`

- This `Marktmodell` node is a market model. The node names the concept/category/value.
- The source belongs on this relationship: `Marktmodell ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=mm_intra_konzern; name=Intra-Konzern; name_full=Intra-Konzern-Transfer; scope_note=Material transferred within the same legal entity / corporate group; no ...`

- This `Marktmodell` node is a market model. The node names the concept/category/value.
- The source belongs on this relationship: `Marktmodell ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=mm_kauf_gebraucht; name=Kauf gebraucht; name_full=Kauf als Gebrauchtware; scope_note=Sale acknowledged as used material; reduced product-status expectations.`

- This `Marktmodell` node is a market model. The node names the concept/category/value.
- The source belongs on this relationship: `Marktmodell ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Materialgruppe`

Type meaning: a material group/category. Current count: 11.

### Example 1

Node: `id=mg_daemmstoff; name=Daemmstoff; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Materialgruppe` node is a material group/category. The node names the concept/category/value.
- The source belongs on this relationship: `Materialgruppe ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=mg_glas_keramik; name=Glas_Keramik; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Materialgruppe` node is a material group/category. The node names the concept/category/value.
- The source belongs on this relationship: `Materialgruppe ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=mg_holz_biobasiert; name=Holz_Biobasiert; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Materialgruppe` node is a material group/category. The node names the concept/category/value.
- The source belongs on this relationship: `Materialgruppe ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `WiederverwendungsArt`

Type meaning: a reuse type/category. Current count: 11.

### Example 1

Node: `id=wva_adaptives_reuse; name=Adaptives_ReUse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `WiederverwendungsArt` node is a reuse type/category. The node names the concept/category/value.
- The source belongs on this relationship: `WiederverwendungsArt ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=wva_bestandserhalt; name=Bestandserhalt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `WiederverwendungsArt` node is a reuse type/category. The node names the concept/category/value.
- The source belongs on this relationship: `WiederverwendungsArt ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=wva_design_for_disassembly; name=Design_for_Disassembly; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `WiederverwendungsArt` node is a reuse type/category. The node names the concept/category/value.
- The source belongs on this relationship: `WiederverwendungsArt ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Akteurtyp`

Type meaning: an actor type/category. Current count: 10.

### Example 1

Node: `id=at_foerdergeber_programmtraeger; name=Foerdergeber_Programmtraeger; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Akteurtyp` node is an actor type/category. The node names the concept/category/value.
- The source belongs on this relationship: `Akteurtyp ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=at_forschung_lehre; name=Forschung_Lehre; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Akteurtyp` node is an actor type/category. The node names the concept/category/value.
- The source belongs on this relationship: `Akteurtyp <-[:HAT_AKTEURTYP] Akteur HFT Stuttgart`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

### Example 3

Node: `id=at_materialhub_bauteilboerse; name=Materialhub_Bauteilboerse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Akteurtyp` node is an actor type/category. The node names the concept/category/value.
- The source belongs on this relationship: `Akteurtyp <-[:HAT_AKTEURTYP] Akteur RotorDC`, because that is the actual fact.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `BauaufgabeIntervention`

Type meaning: a building task/intervention type. Current count: 10.

### Example 1

Node: `id=bai_aufstockung; name=Aufstockung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `BauaufgabeIntervention` node is a building task/intervention type. The node names the concept/category/value.
- The source belongs on this relationship: `BauaufgabeIntervention ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bai_erweiterung; name=Erweiterung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `BauaufgabeIntervention` node is a building task/intervention type. The node names the concept/category/value.
- The source belongs on this relationship: `BauaufgabeIntervention ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bai_fit_out; name=Fit_out; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `BauaufgabeIntervention` node is a building task/intervention type. The node names the concept/category/value.
- The source belongs on this relationship: `BauaufgabeIntervention ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Beschaffungsweg`

Type meaning: a procurement path. Current count: 10.

### Example 1

Node: `id=bweg_ausschreibung; name=Ausschreibung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Beschaffungsweg` node is a procurement path. The node names the concept/category/value.
- The source belongs on this relationship: `Beschaffungsweg ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bweg_bauteilboerse; name=Bauteilboerse; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Beschaffungsweg` node is a procurement path. The node names the concept/category/value.
- The source belongs on this relationship: `Beschaffungsweg ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bweg_digitale_plattform; name=Digitale_Plattform; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Beschaffungsweg` node is a procurement path. The node names the concept/category/value.
- The source belongs on this relationship: `Beschaffungsweg ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Defekt`

Type meaning: a defect/damage type. Current count: 10.

### Example 1

Node: `id=def_brandschaden; name=Brandschaden; scope_note=Fire damage: SCI P427 excludes fire-exposed members from steel reuse.; migration_origin=mig_qext_b_source_urls`

- This `Defekt` node is a defect/damage type. The node names the concept/category/value.
- The source belongs on this relationship: `Defekt ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=def_chemische_belastung; name=Chemisch belastet; name_full=Chemische Belastung (Salze, Säuren, Öle); scope_note=Salt efflorescence, acid attack, oil contamination.`

- This `Defekt` node is a defect/damage type. The node names the concept/category/value.
- The source belongs on this relationship: `Defekt ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=def_hohlraum_delamination; name=Delamination; name_full=Hohlraum / Delamination; scope_note=Voids, debonding, layer separation in composite/laminated elements.`

- This `Defekt` node is a defect/damage type. The node names the concept/category/value.
- The source belongs on this relationship: `Defekt ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `HuerdeKategorie`

Type meaning: a barrier category. Current count: 10.

### Example 1

Node: `id=hk_beschaffung_markt; name=Beschaffung_Markt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `HuerdeKategorie` node is a barrier category. The node names the concept/category/value.
- The source belongs on this relationship: `HuerdeKategorie ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=hk_daten_evidenz; name=Daten_Evidenz; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `HuerdeKategorie` node is a barrier category. The node names the concept/category/value.
- The source belongs on this relationship: `HuerdeKategorie ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=hk_logistisch; name=Logistisch; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `HuerdeKategorie` node is a barrier category. The node names the concept/category/value.
- The source belongs on this relationship: `HuerdeKategorie ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Logistik`

Type meaning: a logistics concept/process. Current count: 10.

### Example 1

Node: `id=log_bauteiltracking; name=Bauteiltracking; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Logistik` node is a logistics concept/process. The node names the concept/category/value.
- The source belongs on this relationship: `Logistik ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=log_just_in_time; name=Just_in_Time; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Logistik` node is a logistics concept/process. The node names the concept/category/value.
- The source belongs on this relationship: `Logistik ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=log_lagerflaeche; name=Lagerflaeche; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Logistik` node is a logistics concept/process. The node names the concept/category/value.
- The source belongs on this relationship: `Logistik ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Prozessphase`

Type meaning: a process phase. Current count: 10.

### Example 1

Node: `id=phase_aufbereitung; name=Aufbereitung; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Prozessphase` node is a process phase. The node names the concept/category/value.
- The source belongs on this relationship: `Prozessphase ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=phase_betrieb; name=Betrieb; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Prozessphase` node is a process phase. The node names the concept/category/value.
- The source belongs on this relationship: `Prozessphase ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=phase_dokumentation; name=Dokumentation; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Prozessphase` node is a process phase. The node names the concept/category/value.
- The source belongs on this relationship: `Prozessphase ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bausystem`

Type meaning: a building system. Current count: 9.

### Example 1

Node: `id=bsys_betonfertigteil_system; name=Betonfertigteil_System; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bausystem` node is a building system. The node names the concept/category/value.
- The source belongs on this relationship: `Bausystem ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bsys_cross_laminated_secondary_timber_clst; name=CLST_cross_laminated_secondary_timber; migration_origin=mig_qext_b_source_urls; definition=Cross-laminated secondary timber from reclaimed solid wood; remanufactur...`

- This `Bausystem` node is a building system. The node names the concept/category/value.
- The source belongs on this relationship: `Bausystem ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bsys_holz_skelettbau; name=Holz_Skelettbau; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bausystem` node is a building system. The node names the concept/category/value.
- The source belongs on this relationship: `Bausystem ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `MatchingQualitaet`

Type meaning: a matching quality category. Current count: 9.

### Example 1

Node: `id=mq_geographic_intl; name=Geo: international; name_full=International / interkontinental; scope_note=Cross-border or transcontinental sourcing; high transport burden.`

- This `MatchingQualitaet` node is a matching quality category. The node names the concept/category/value.
- The source belongs on this relationship: `MatchingQualitaet ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=mq_geographic_local; name=Geo: lokal (<50 km); name_full=Lokales geografisches Matching (<50 km); scope_note=Donor + receiver within ~50 km; lowest transport emissions.`

- This `MatchingQualitaet` node is a matching quality category. The node names the concept/category/value.
- The source belongs on this relationship: `MatchingQualitaet ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=mq_geographic_regional; name=Geo: regional; name_full=Regional geografisches Matching (50–500 km); scope_note=Regional supply chain.`

- This `MatchingQualitaet` node is a matching quality category. The node names the concept/category/value.
- The source belongs on this relationship: `MatchingQualitaet ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Nutzung`

Type meaning: a use/function. Current count: 9.

### Example 1

Node: `id=nut_buero; name=Buero; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Nutzung` node is a use/function. The node names the concept/category/value.
- The source belongs on this relationship: `Nutzung ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=nut_gewerbe; name=Gewerbe; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Nutzung` node is a use/function. The node names the concept/category/value.
- The source belongs on this relationship: `Nutzung ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=nut_infrastruktur; name=Infrastruktur; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Nutzung` node is a use/function. The node names the concept/category/value.
- The source belongs on this relationship: `Nutzung ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Schadstoff`

Type meaning: a pollutant. Current count: 9.

### Example 1

Node: `id=s_asbest; name=Asbest; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls`

- This `Schadstoff` node is a pollutant. The node names the concept/category/value.
- The source belongs on this relationship: `Schadstoff ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=s_bleifarbe; name=Bleifarbe; last_seen_by=agent10_phase4b_2; migration_origin=mig_qext_b_source_urls`

- This `Schadstoff` node is a pollutant. The node names the concept/category/value.
- The source belongs on this relationship: `Schadstoff ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=s_formaldehyd; name=Formaldehyd (MDF / Spanplatten); last_seen_by=agent10_phase4b_2; standards_body=EU REACH`

- This `Schadstoff` node is a pollutant. The node names the concept/category/value.
- The source belongs on this relationship: `Schadstoff ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Status`

Type meaning: a status category. Current count: 9.

### Example 1

Node: `id=status_geplant; name=Geplant; kind=lifecycle; migration_origin=mig_qext_b_source_urls`

- This `Status` node is a status category. The node names the concept/category/value.
- The source belongs on this relationship: `Status ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=status_in_bau; name=In_Bau; kind=lifecycle; migration_origin=mig_qext_b_source_urls`

- This `Status` node is a status category. The node names the concept/category/value.
- The source belongs on this relationship: `Status ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=status_prototyp; name=Prototyp; kind=maturity; migration_origin=mig_qext_b_source_urls`

- This `Status` node is a status category. The node names the concept/category/value.
- The source belongs on this relationship: `Status ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bauobjektklasse`

Type meaning: a built-object class. Current count: 8.

### Example 1

Node: `id=bok_depot_lager; name=Depot_Lager; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauobjektklasse` node is a built-object class. The node names the concept/category/value.
- The source belongs on this relationship: `Bauobjektklasse ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bok_gebaeude; name=Gebaeude; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauobjektklasse` node is a built-object class. The node names the concept/category/value.
- The source belongs on this relationship: `Bauobjektklasse ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bok_gebaeudeteil; name=Gebaeudeteil; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauobjektklasse` node is a built-object class. The node names the concept/category/value.
- The source belongs on this relationship: `Bauobjektklasse ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Tool`

Type meaning: a tool category or named tool. Current count: 8.

### Example 1

Node: `id=tool_bauteilkatalog; name=Bauteilkatalog / Bauteilpass; source_resolution_status=needs_source_url_review; kind=tool`

- This `Tool` node is a tool category or named tool. The node names the concept/category/value.
- The source belongs on this relationship: `Tool ->[:NUTZT_SOFTWARE] Software Building Information Modeling / BIM`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=tool_bim_bauteilkatalog; name=BIM / digitaler Bauteilkatalog; source_resolution_status=needs_source_url_review; kind=tool`

- This `Tool` node is a tool category or named tool. The node names the concept/category/value.
- The source belongs on this relationship: `Tool ->[:NUTZT_SOFTWARE] Software Building Information Modeling / BIM`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=tool_hts_stockmatcher; name=HTS Reused Steel Stockmatcher; funktion=Abgleich von stock list und design list für wiederverwendete Stahlträger; kind=tool`

- This `Tool` node is a tool category or named tool. The node names the concept/category/value.
- The fact is represented by this relationship: `Tool ->[:BELEGT_IN] Quelle:Dossier Timber_Square_London.md`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: candidate`; keep URLs in `candidate_source_urls`, not in `source_url`.

## `Zertifizierungssystem`

Type meaning: a certification system. Current count: 8.

### Example 1

Node: `id=zbs_breeam; name=BREEAM; evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications | mig_qext_b_source_urls | mig_qext_c_pr...`

- This `Zertifizierungssystem` node is a certification system. The node names the concept/category/value.
- The fact is represented by this relationship: `Zertifizierungssystem ->[:BELEGT_IN] Quelle:Dossier Timber_Square_London.md`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=zbs_dgnb; name=DGNB; evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications | mig_qext_b_source_urls | mig_qext_c_pr...`

- This `Zertifizierungssystem` node is a certification system. The node names the concept/category/value.
- The fact is represented by this relationship: `Zertifizierungssystem ->[:BELEGT_IN] Quelle:Dossier Thoravej_29_Copenhagen.md`. Because it points only to a Dossier, it becomes exact only after the concrete dossier URL is copied onto this relationship or a Claim.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=zbs_ecotool; name=EcoTool (ZBS); evidence_basis=controlled_vocab; migration_origin=mig_r2_d_restore_certifications | mig_qext_b_source_urls`

- This `Zertifizierungssystem` node is a certification system. The node names the concept/category/value.
- The source belongs on this relationship: `Zertifizierungssystem <-[:HAT_ZERTIFIZIERUNG] Projekt ELEMENTA Walkeweg`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Akzeptanz`

Type meaning: an acceptance/social acceptance concept. Current count: 7.

### Example 1

Node: `id=ak_aesthetik_patinakultur; name=Patina-Ästhetik; name_full=Ästhetik-/Patinakultur akzeptiert; scope_note=Sichtbare Reuse-Ästhetik (Patina, Materialgeschichte) als gestalterische...`

- This `Akzeptanz` node is an acceptance/social acceptance concept. The node names the concept/category/value.
- The source belongs on this relationship: `Akzeptanz ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=ak_breeam_zertifizierung; name=BREEAM; name_full=BREEAM-Zertifizierung akzeptiert Reuse; scope_note=UK-basiertes Nachhaltigkeitszertifikat; Mat-Credits für Reuse.`

- This `Akzeptanz` node is an acceptance/social acceptance concept. The node names the concept/category/value.
- The source belongs on this relationship: `Akzeptanz ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=ak_dgnb_zertifizierung; name=DGNB; name_full=DGNB-Zertifizierung akzeptiert Reuse; scope_note=Deutsches Nachhaltigkeitszertifikat (DGNB) gewährt Bonuspunkte für Baute...`

- This `Akzeptanz` node is an acceptance/social acceptance concept. The node names the concept/category/value.
- The source belongs on this relationship: `Akzeptanz ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bauobjektrolle`

Type meaning: the role of a building object, such as donor or recipient. Current count: 6.

### Example 1

Node: `id=bor_bestandsobjekt; name=Bestandsobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauobjektrolle` node is the role of a building object, such as donor or recipient. The node names the concept/category/value.
- The source belongs on this relationship: `Bauobjektrolle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bor_donorobjekt; name=Donorobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauobjektrolle` node is the role of a building object, such as donor or recipient. The node names the concept/category/value.
- The source belongs on this relationship: `Bauobjektrolle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bor_empfaengerobjekt; name=Empfaengerobjekt; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauobjektrolle` node is the role of a building object, such as donor or recipient. The node names the concept/category/value.
- The source belongs on this relationship: `Bauobjektrolle ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bauteilebene`

Type meaning: a component level/layer. Current count: 6.

### Example 1

Node: `id=be_bauteilgruppe; name=Bauteilgruppe; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauteilebene` node is a component level/layer. The node names the concept/category/value.
- The source belongs on this relationship: `Bauteilebene ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=be_einzelbauteil; name=Einzelbauteil; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauteilebene` node is a component level/layer. The node names the concept/category/value.
- The source belongs on this relationship: `Bauteilebene ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=be_gebaeudeteil; name=Gebaeudeteil; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauteilebene` node is a component level/layer. The node names the concept/category/value.
- The source belongs on this relationship: `Bauteilebene ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Bauweise`

Type meaning: a construction method. Current count: 6.

### Example 1

Node: `id=bauw_fertigteilbauweise; name=Fertigteilbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauweise` node is a construction method. The node names the concept/category/value.
- The source belongs on this relationship: `Bauweise ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=bauw_holzbauweise; name=Holzbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauweise` node is a construction method. The node names the concept/category/value.
- The source belongs on this relationship: `Bauweise ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=bauw_hybridbauweise; name=Hybridbauweise; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Bauweise` node is a construction method. The node names the concept/category/value.
- The source belongs on this relationship: `Bauweise ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `BauwerkEra`

Type meaning: an era/period of a building. Current count: 6.

### Example 1

Node: `id=era_1900_1945; name=1900–1945; year_from=1900; notes=Industrialisation; reinforced concrete commercialised; PAK still high; s...`

- This `BauwerkEra` node is an era/period of a building. The node names the concept/category/value.
- The source belongs on this relationship: `BauwerkEra ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=era_1970_1990; name=1970–1990; year_from=1970; notes=Still high asbestos / PCB / KMF; energy crisis drives insulation upgrade...`

- This `BauwerkEra` node is an era/period of a building. The node names the concept/category/value.
- The source belongs on this relationship: `BauwerkEra ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=era_1990_2000; name=1990–2000; year_from=1990; notes=Country-specific asbestos bans (DE 1993, NL 1994, FR 1997, BE 1998, UK 2...`

- This `BauwerkEra` node is an era/period of a building. The node names the concept/category/value.
- The source belongs on this relationship: `BauwerkEra ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Funktionswechsel`

Type meaning: a change of function. Current count: 6.

### Example 1

Node: `id=fw_dekorative_funktion; name=Dekorative_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Funktionswechsel` node is a change of function. The node names the concept/category/value.
- The source belongs on this relationship: `Funktionswechsel ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=fw_gleiche_funktion; name=Gleiche_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Funktionswechsel` node is a change of function. The node names the concept/category/value.
- The source belongs on this relationship: `Funktionswechsel ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=fw_konstruktive_funktion; name=Konstruktive_Funktion; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Funktionswechsel` node is a change of function. The node names the concept/category/value.
- The source belongs on this relationship: `Funktionswechsel ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Layer`

Type meaning: a building layer. Current count: 6.

### Example 1

Node: `id=layer_services; name=Services; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab`

- This `Layer` node is a building layer. The node names the concept/category/value.
- The source belongs on this relationship: `Layer <-[:TEILT_LAYER] Bauteiltyp Technik`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=layer_site; name=Site; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab`

- This `Layer` node is a building layer. The node names the concept/category/value.
- The source belongs on this relationship: `Layer ->[:HAS_DATA_ISSUE] DataIssue di_no_src_layer_site`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=layer_skin; name=Skin; evidence_source_id=q_brand_how_buildings_learn; evidence_basis=controlled_vocab`

- This `Layer` node is a building layer. The node names the concept/category/value.
- The source belongs on this relationship: `Layer <-[:TEILT_LAYER] Bauteiltyp Dach`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `ZustandsKlasse`

Type meaning: a condition class. Current count: 6.

### Example 1

Node: `id=zk_eingeschraenkt_nachbearbeitung; name=Eingeschränkt: Nacharbeit; name_full=Eingeschränkt, Nachbearbeitung nötig; scope_note=Wiederverwendbar nach Aufbereitung (Zuschnitt, Schliff, Beschichtung, Re...`

- This `ZustandsKlasse` node is a condition class. The node names the concept/category/value.
- The source belongs on this relationship: `ZustandsKlasse ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=zk_eingeschraenkt_nutzungsklasse_reduzieren; name=Eingeschränkt: downgrade; name_full=Eingeschränkt, Nutzungsklasse reduzieren; scope_note=Wiederverwendbar nur in geringerer Beanspruchungsklasse (downgrade, z.B....`

- This `ZustandsKlasse` node is a condition class. The node names the concept/category/value.
- The source belongs on this relationship: `ZustandsKlasse ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=zk_gebrauchsspuren_funktional; name=Gebraucht, funktional; name_full=Gebrauchsspuren, funktional unbeeinträchtigt; scope_note=Sichtbare Patina/Verschleiß ohne funktionalen Einfluss; weiterhin im gle...`

- This `ZustandsKlasse` node is a condition class. The node names the concept/category/value.
- The source belongs on this relationship: `ZustandsKlasse ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `LCAModule`

Type meaning: a life-cycle assessment module. Current count: 5.

### Example 1

Node: `id=lz_a1_a3; name=A1-A3 Produkt; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab`

- This `LCAModule` node is a life-cycle assessment module. The node names the concept/category/value.
- The source belongs on this relationship: `LCAModule <-[:BERECHNET_NACH_MODUL] Projekt 55 Great Suffolk Street`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=lz_a4_a5; name=A4-A5 Errichtung; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab`

- This `LCAModule` node is a life-cycle assessment module. The node names the concept/category/value.
- The source belongs on this relationship: `LCAModule <-[:BERECHNET_NACH_MODUL] Projekt 55 Great Suffolk Street`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=lz_b; name=B1-B7 Nutzung; evidence_source_id=q_en_15978_lifecycle_modules; evidence_basis=controlled_vocab`

- This `LCAModule` node is a life-cycle assessment module. The node names the concept/category/value.
- The source belongs on this relationship: `LCAModule <-[:BERECHNET_NACH_MODUL] Projekt Resource Rows`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Rueckbauverfahren`

Type meaning: a deconstruction method. Current count: 5.

### Example 1

Node: `id=rv_ausbau_von_bauteilen; name=Ausbau_von_Bauteilen; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Rueckbauverfahren` node is a deconstruction method. The node names the concept/category/value.
- The source belongs on this relationship: `Rueckbauverfahren ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=rv_betonfraesen; name=Betonfraesen; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Rueckbauverfahren` node is a deconstruction method. The node names the concept/category/value.
- The source belongs on this relationship: `Rueckbauverfahren ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=rv_demontage; name=Demontage; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Rueckbauverfahren` node is a deconstruction method. The node names the concept/category/value.
- The source belongs on this relationship: `Rueckbauverfahren ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `Tragwerksprinzip`

Type meaning: a structural principle. Current count: 4.

### Example 1

Node: `id=tp_fachwerk; name=Fachwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Tragwerksprinzip` node is a structural principle. The node names the concept/category/value.
- The source belongs on this relationship: `Tragwerksprinzip ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 2

Node: `id=tp_skeletttragwerk; name=Skeletttragwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Tragwerksprinzip` node is a structural principle. The node names the concept/category/value.
- The source belongs on this relationship: `Tragwerksprinzip ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

### Example 3

Node: `id=tp_wand_kern_tragwerk; name=Wand_Kern_Tragwerk; migration_origin=mig_qext_b_source_urls; source_scope=controlled_vocab_seed`

- This `Tragwerksprinzip` node is a structural principle. The node names the concept/category/value.
- The source belongs on this relationship: `Tragwerksprinzip ->[:ANCHORED_BY] OntologyAnchor Controlled-vocab seed`, because that is the actual fact.
- `source_status: missing`; do not invent a URL.

## `OntologyAnchor`

Type meaning: an ontology helper/anchor node. Current count: 2.

### Example 1

Node: `id=q_akteursliste_master_md; name=akteursliste_master.md; actor_registry_loader_seen=agent10; source_count=163`

- This `OntologyAnchor` node is an ontology helper/anchor node.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

### Example 2

Node: `id=q_controlled_vocab_seed; name=Controlled-vocab seed; name_full=Controlled vocabulary seed source — definitional taxonomy file (controll...; quelltyp=controlled_vocab_seed`

- This `OntologyAnchor` node is an ontology helper/anchor node.
- It is not a domain fact that needs a source URL.
- It should point to the affected node/relationship and carry review status.

