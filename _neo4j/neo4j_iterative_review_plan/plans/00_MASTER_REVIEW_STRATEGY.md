# 00 Master Review Strategy

## Goal

Optimize the already generated Neo4j JSONL exports by auditing and patching them iteratively.

The goal is **not** to regenerate every project from scratch. The goal is to improve:
- consistency,
- graph connectivity,
- controlled vocabulary quality,
- import safety,
- research-query usefulness.

## Frozen model assumptions

```text
No Fallbeispiel nodes.
No Kennwert nodes.
Projekt is the central case/intervention node.
Bauteilgruppe is the component-group / reuse-occurrence node.
Bauwerk is the physical building/infrastructure/object node.
Quelle is the source-of-truth node.
Datenqualitaet is only a property on BELEGT_IN and defaults to "Belegt".
City/country/roles/classes/materials/hurdles/types are nodes, not properties.
Metrics are scalar properties on the scoped node.
```

## Review rounds

### Round 1 — Technical baseline

Run global mechanical checks on all exported batches.

Output:
```text
review/round_001/global_audit_report.md
review/round_001/patches/global_technical.patch.jsonl
review/round_001/patch_manifest.json
```

### Round 2 — Controlled vocabulary cleanup

Review one controlled vocabulary family at a time.

Recommended order:
```text
1. Material + Materialgruppe
2. Bauteiltyp + Bauteilebene
3. Huerde + HuerdeKategorie
4. Akteurrolle + Akteurtyp
5. Bauobjektrolle + Bauobjektklasse
6. Status + WiederverwendungsArt
7. Stadt + Land
8. Norm + PruefungNachweis + Leistungsanforderung
```

### Round 3 — Project content review

Review project chunks of 5 projects.

For each chunk:
- verify project root,
- verify donor/receiver Bauwerk,
- verify Bauteilgruppen,
- verify metrics placement,
- verify direct reuse vs Bestandserhalt,
- verify actors and roles,
- verify source links.

### Round 4 — Query-driven consistency review

Run graph queries and patch inconsistencies found in cross-project comparisons.

Recommended query themes:
```text
1. direct structural reuse
2. concrete / precast reuse
3. steel reuse
4. timber reuse
5. facade reuse
6. certification / testing hurdles
7. planned vs realized reuse
8. donor-receiver chains
9. Bestandserhalt vs direct reuse
10. uncertain/conflicting metrics
```

### Round 5 — Freeze

After patches are reviewed:
- merge accepted controlled vocabulary deltas,
- freeze canonical registry,
- run final validation,
- produce release manifest.
