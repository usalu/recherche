"""Final verifier 1/12: Phase 1.1 read-only checks against mit-bestand."""
import json
from neo4j import GraphDatabase

URI = "bolt://localhost:7687"
AUTH = ("neo4j", "ENTWERFENMITBESTAND")
DB = "mit-bestand"

driver = GraphDatabase.driver(URI, auth=AUTH)

def run(tx_query, **params):
    with driver.session(database=DB, default_access_mode="READ") as s:
        return list(s.run(tx_query, **params))

results = {}

# Check 5
r = run("MATCH (k:Wiederverwendungskette) RETURN count(k) AS c")
results["chain_count"] = r[0]["c"]

# Check 6
r = run(
    "MATCH (k:Wiederverwendungskette) "
    "WHERE NOT (exists{(k)-[:FROM_DONOR]->()} AND exists{(k)-[:INTO_RECEIVER]->()}) "
    "RETURN count(k) AS c"
)
results["unwired_chains"] = r[0]["c"]

# Check 7
r = run(
    "MATCH ()-[r]->() WHERE r.migration_origin='mig_1_1_demote_chains' RETURN count(r) AS c"
)
results["migrated_edges_count"] = r[0]["c"]

# Check 8: sample 5 demoted edges
r = run(
    "MATCH ()-[r]->() WHERE r.migration_origin='mig_1_1_demote_chains' "
    "RETURN type(r) AS reltype, r.evidence_source_id AS esid, r.evidence_basis AS eb, "
    "r.derivation_note AS dn LIMIT 5"
)
samples = []
for row in r:
    samples.append({
        "reltype": row["reltype"],
        "evidence_source_id": row["esid"],
        "evidence_basis": row["eb"],
        "derivation_note": row["dn"],
    })
results["sampled_edges"] = samples

print(json.dumps(results, indent=2, ensure_ascii=False))
driver.close()
