# Finding: projects_no_component_or_work Discrepancy

**Check**: projects_no_component_or_work  
**Export scan result**: 2  
**Live DB result**: 9  
**Date**: 2026-05-14

## Explanation

The export-scan check counts Projekt nodes in the 97 `.kg.jsonl` batch files that have
**no outgoing `HAT_BAUTEILGRUPPE` or `NUTZT_BAUWERK` edge** in those same files. It found 2.

The live-DB check runs the same logic but against all nodes currently in Neo4j, including
nodes added via direct patches (round 004) that were never part of any batch JSONL file.
It found 9.

The 7 extra projects in the live DB are programme-, platform-, hub-, or stub-type entries
added through the round 004 donor/receiver research patch. They intentionally have no
component or building links because they are:

| Project id | Type | Reason for no components |
| --- | --- | --- |
| p_boell_lab_berlin | cancelled project | Cancelled before construction; no reuse documented |
| p_da_vinci_business_district_evere | stub | Preliminary entry; components to be researched |
| p_kindl_areal_berlin | stub | Preliminary entry; components to be researched |
| p_opalis_plattformfall | platform/tool | Platform node, not a reuse project |
| p_haus_der_materialisierung_berlin | hub | Material hub, not a reuse project |
| p_kunst_stoffe_berlin | hub | Material hub, not a reuse project |
| p_preuse_interreg_nwe | programme | EU programme node, not a reuse project |
| p_permanently_temporary_pavilion | stub | Preliminary entry; Round 005 deferred |
| p_rotor_dc_brussels_model | stub | Preliminary entry; Round 005 deferred |

*(Note: the 2 matching export-scan entries are p_permanently_temporary_pavilion and
p_rotor_dc_brussels_model — present in batch JSONL without component links.)*

## Resolution

- The 7 programme/hub/platform/cancelled projects will be classified in **Round 006**
  (stub/programme project classification).
- The 2 stub projects (p_permanently_temporary_pavilion, p_rotor_dc_brussels_model) are
  deferred to **Round 005** (unknown-donor Bauteilgruppen research).
- **No immediate patch action required.** The discrepancy is fully explained and tracked.
