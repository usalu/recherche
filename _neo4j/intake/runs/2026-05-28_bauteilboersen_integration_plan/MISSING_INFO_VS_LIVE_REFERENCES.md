# Missing Info vs Live References

Date: 2026-05-28

Compared the target Bauteilbörsen preview against richer live nodes:

- `bauteilboerse_bremen`
- `concular`
- supporting checks: `baukarussell`, `rotordc`, `software_restado`

## Reference Pattern

`bauteilboerse_bremen` currently has:

- `HAT_AKTEURTYP`
- `HAT_AKTEURROLLE`
- `LIEGT_IN_LAND`
- `GEHÖRT_ZU`
- `VERBUNDEN_MIT_AKTEUR`
- `ANCHORED_BY`
- `HAS_DATA_ISSUE`
- inbound `CONCERNS`

`concular` currently has:

- `HAT_AKTEURTYP`
- `HAT_AKTEURROLLE`
- `LIEGT_IN_LAND`
- `GEHÖRT_ZU`
- `BELEGT_IN`
- `BETEILIGT_AN`
- `NUTZT_SOFTWARE`
- `VERBUNDEN_MIT_AKTEUR`
- `ANCHORED_BY`
- inbound `CONCERNS`

## Missing From The Current Preview / Plan

1. `GEHÖRT_ZU` country links

The preview uses only `LIEGT_IN_LAND`. Live reference nodes often have both `LIEGT_IN_LAND` and `GEHÖRT_ZU` to the country. Decide whether to keep both for parity or standardize to one relation. If parity is desired, add `GEHÖRT_ZU` to concrete country nodes.

2. Direct source URL graph links

The preview shows `BELEGT_IN` to `q_research_*_md` containers. Concular-style evidence also uses direct `BELEGT_IN`/source links to external `Quelle` / `ExternalLink` nodes. Because the source containers already carry `source_url_node_ids`, the patch should explicitly link graph facts or anchors to those URL nodes where accepted.

3. `HAS_DATA_ISSUE` / `CONCERNS` for unresolved imported facts

The plan says to use `DataIssue` only when uncertainty affects an accepted graph fact, but the preview does not show these. Add them for accepted facts with unclear operator, unclear country, questionable source URL binding, or uncertain semantic match. Do not create DataIssues for prose that is dropped.

4. Additional actor types

The preview mostly shows only `at_materialhub_bauteilboerse`. Concular also has `at_unternehmen` and `at_software_tool_anbieter`. Add additional `HAT_AKTEURTYP` links where the archive and URL evidence clearly support them, especially for digital/software marketplace operators.

5. More precise roles

The current role preview uses six broad roles. Concular and RotorDC also use `ar_materialbroker`, `ar_fachplanung_nachweis`, `ar_nachhaltigkeitsberatung`, and `ar_betrieb_nutzung`. Add these only where explicitly evidenced. At minimum, consider `ar_materialbroker` for brokerage/marketplace actors.

6. Operator / network actor links beyond the three highlighted examples

The preview shows only:

- `software_restado -> concular`
- `salvoweb -> salvo_ltd`
- `re_store_harvestmap_vienna -> materialnomaden`

But Bremen-style graph context also uses `VERBUNDEN_MIT_AKTEUR` for network/person/related-actor links. Existing Bremen already links to `bauteilnetz_deutschland` and `ute_dechantsreiter`. The patch should preserve existing such links and add new ones only when the operator/network actor is explicit and not just a prose hint.

7. `BETEILIGT_AN` project/material links

Concular has project and material-group participation. The archive Bauteilbörse files mostly describe platforms, not projects. Do not invent `BETEILIGT_AN` links unless a profile explicitly names a concrete project, program, or material group that already exists or is accepted for creation.

8. `NUTZT_SOFTWARE` / software-tool modeling

Concular uses software/tool relations. Restado already exists as `Software`. For digital marketplaces, decide case by case whether to create a separate `Software`/`Tool` node or keep the platform as an `Akteur`. Avoid creating duplicate actor/software pairs unless the distinction is explicit.

9. `ANCHORED_BY`

Actor-registry nodes often have `ANCHORED_BY -> q_akteursliste_master_md`. New archive-derived platform nodes should not point to the actor registry anchor unless they actually come from that registry. If needed, use the research source container via `BELEGT_IN` instead.

## Import Recommendation

Before applying the patch, extend the dry-run generation with these checks:

- Add `GEHÖRT_ZU` country links if we choose parity with current actor nodes.
- Link accepted anchors/facts to external URL nodes, not only to the Markdown source container.
- Add `DataIssue` nodes only for uncertainties on imported graph facts.
- Add secondary actor types and precise roles where evidence is explicit.
- Preserve existing `VERBUNDEN_MIT_AKTEUR`, `BETEILIGT_AN`, and `NUTZT_SOFTWARE` relationships; add new ones only when unambiguous.

The current preview is therefore a good minimum graph, but not yet a full parity graph compared with Bremen/Concular.
