# Actor registry chunk 091_100

This folder exports actors 91–100 from `akteursliste_master.md` into the existing Neo4j graph contract.

Rules applied:

- `Sterne` column ignored.
- `Akteurrolle` is used for broad expertise-profile classification.
- No `AkteurFokus` label is introduced.
- `VERBUNDEN_MIT_AKTEUR` connects people to organisations/platforms mentioned in the registry.
- `ASSOZIIERT_MIT_PROJEKT` is used only as a weak registry-derived project relation with `needs_verification:true`.
- No `BETEILIGT_AN` relations are invented from this registry.
- Every source link becomes a `Quelle`; every `BELEGT_IN` has `datenqualitaet:"Belegt"`.
- `mailto:` links are ignored.
