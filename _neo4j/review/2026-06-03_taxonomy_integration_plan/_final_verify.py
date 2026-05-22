"""Final verification of the taxonomy integration."""
import sys
sys.path.insert(0, r"_scripts")
from neo4j_env import resolve_connection
from neo4j import GraphDatabase

passes = 0
fails = 0

def check(label, ok, detail=""):
    global passes, fails
    if ok:
        passes += 1
        print(f"  [PASS] {label}")
    else:
        fails += 1
        print(f"  [FAIL] {label}  {detail}")

uri, user, password, database = resolve_connection()
driver = GraphDatabase.driver(uri, auth=(user, password))

try:
    with driver.session(database=database) as s:
        print("=" * 60)
        print("FINAL VERIFICATION — TAXONOMY INTEGRATION")
        print("=" * 60)
        print()
        print("Section 1. Vocab axis sizes")
        targets = {
            "Methode": 6, "Aufbereitungsverfahren": 6, "Ressourcenquelle": 6,
            "Rueckbauverfahren": 6, "Wiederverwendungsergebnis": 6,
            "Wiederverwendungsort": 6, "WiederverwendungsArt": 0,
        }
        for lbl, n in targets.items():
            r = s.run(f"MATCH (x:`{lbl}`) RETURN count(x) AS n").single()
            check(f":{lbl} = {n}", r["n"] == n, f"got {r['n']}")

        print()
        print("Section 2. Canonical ids correct")
        meth_ids = ["meth_urban_mining_und_scouting", "meth_bestands_und_reuse_assessment",
                    "meth_verfuegbarkeitsbasiertes_design", "meth_reversibles_design",
                    "meth_zirkulaere_beschaffung", "meth_dokumentation_und_monitoring"]
        av_ids = ["av_reinigung_und_oberflaeche", "av_zuschnitt_und_vereinzelung",
                  "av_pruefung_sortierung_qs", "av_reparatur_und_refurbishment",
                  "av_remanufacturing_und_upcycling", "av_verstaerkung_und_schutz"]
        rq_ids = ["rq_externer_spenderbau", "rq_eigener_bestand", "rq_gleicher_standort",
                  "rq_bauteilmarkt_oder_lager", "rq_leihgabe_oder_service",
                  "rq_restposten_abfall_unbekannt"]
        rv_ids = ["rv_selektiver_rueckbau", "rv_ausbau_von_bauteilen", "rv_demontage",
                  "rv_zerstoerungsarme_bergung", "rv_schneidender_rueckbau",
                  "rv_integrierter_rueckbau_und_lagerung"]
        wver_ids = ["wver_bestandserhalt", "wver_wv_gleiche_funktion", "wver_wv_neue_funktion",
                    "wver_modul_oder_abschnittswv", "wver_material_reprocessing",
                    "wver_geplant_oder_gelagert"]
        wvo_ids = ["wvo_in_situ", "wvo_im_selben_gebaeude_versetzt",
                   "wvo_auf_demselben_standort_versetzt", "wvo_extern_importiert",
                   "wvo_temporaer_oder_zurueckgegeben", "wvo_gelagert_oder_unbekannt"]
        for lbl, expected in [("Methode", meth_ids), ("Aufbereitungsverfahren", av_ids),
                              ("Ressourcenquelle", rq_ids), ("Rueckbauverfahren", rv_ids),
                              ("Wiederverwendungsergebnis", wver_ids),
                              ("Wiederverwendungsort", wvo_ids)]:
            r = s.run(f"MATCH (x:`{lbl}`) RETURN collect(x.id) AS ids").single()
            actual = sorted(r["ids"])
            exp = sorted(expected)
            check(f":{lbl} canonical ids match", actual == exp,
                  f"diff={set(actual) ^ set(exp)}")

        print()
        print("Section 3. Edge axes — no edges left pointing at non-canonical")
        for rel, ids in [("HAT_METHODE", meth_ids), ("HAT_AUFBEREITUNG", av_ids),
                         ("HAT_RESSOURCENQUELLE", rq_ids), ("HAT_RUECKBAUVERFAHREN", rv_ids),
                         ("HAT_ERGEBNIS", wver_ids), ("HAT_WIEDERVERWENDUNGSORT", wvo_ids)]:
            q = f"MATCH ()-[r:`{rel}`]->(t) WHERE NOT t.id IN $ids RETURN count(r) AS n"
            r = s.run(q, ids=ids).single()
            check(f"{rel} all-targets-canonical", r["n"] == 0,
                  f"{r['n']} edges to non-canonical")

        print()
        print("Section 4. Retired structures gone")
        n = s.run("MATCH ()-[r:HAT_WIEDERVERWENDUNGSART]->() RETURN count(r) AS n").single()["n"]
        check("HAT_WIEDERVERWENDUNGSART rel: 0", n == 0)
        n = s.run("MATCH (n:WiederverwendungsArt) RETURN count(n) AS n").single()["n"]
        check(":WiederverwendungsArt nodes: 0", n == 0)
        n = s.run("SHOW CONSTRAINTS YIELD name WHERE name = 'wiederverwendungsart_id' RETURN count(*) AS n").single()["n"]
        check("wiederverwendungsart_id constraint dropped", n == 0)

        print()
        print("Section 5. Bauteilgruppe state")
        n = s.run("MATCH (bg:Bauteilgruppe) RETURN count(bg) AS n").single()["n"]
        check("Total Bauteilgruppe = 364", n == 364, f"got {n}")
        bad_prefixes = ["bg_reuse_", "bg_retained_", "bg_planned_", "bg_dismantled_", "bg_candidate_"]
        n = s.run(
            "MATCH (bg:Bauteilgruppe) "
            "WHERE any(p IN $pfx WHERE bg.id STARTS WITH p) "
            "RETURN count(bg) AS n",
            pfx=bad_prefixes,
        ).single()["n"]
        check("No legacy BG prefix remains", n == 0, f"{n} with old prefix")
        n = s.run('MATCH (bg:Bauteilgruppe) WHERE NOT bg.id STARTS WITH "bg_" RETURN count(bg) AS n').single()["n"]
        check("All BGs keep bg_ prefix", n == 0)

        print()
        print("Section 6. New constraints in place")
        n = s.run(
            "SHOW CONSTRAINTS YIELD name WHERE name IN "
            "['wiederverwendungsergebnis_id','wiederverwendungsort_id',"
            "'rel_hat_ergebnis_id','rel_hat_wiederverwendungsort_id',"
            "'rel_angewendet_auf_id'] RETURN count(*) AS n"
        ).single()["n"]
        check("5 new constraints active", n == 5, f"got {n}")

        print()
        print("Section 7. Provenance preserved on migrated edges")
        n1 = s.run("MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03_phase6_1'}]->() "
                   "WHERE r.legacy_methode_id IS NOT NULL OR r.legacy_aufbereitung_id IS NOT NULL "
                   "OR r.legacy_ressourcenquelle_id IS NOT NULL RETURN count(r) AS n").single()["n"]
        n2 = s.run("MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03_phase6_1'}]->() RETURN count(r) AS n").single()["n"]
        check("All P6.1 edges have legacy_*_id", n1 == n2, f"{n1}/{n2} with provenance")
        n1 = s.run("MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03_phase6_2'}]->() "
                   "WHERE r.legacy_aufbereitung_id IS NOT NULL RETURN count(r) AS n").single()["n"]
        n2 = s.run("MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03_phase6_2'}]->() RETURN count(r) AS n").single()["n"]
        check("All P6.2 edges have legacy_aufbereitung_id", n1 == n2, f"{n1}/{n2}")

        print()
        print("Section 8. Evidence quality shift")
        rows = s.run("MATCH ()-[r {review_run: 'taxonomy_integration_2026_06_03'}]-() "
                     "RETURN r.evidence_confidence AS conf, count(*) AS n").data()
        total = sum(row["n"] for row in rows)
        belegt = sum(row["n"] for row in rows if row["conf"] == "belegt")
        check(f">= 70% edges at belegt ({belegt}/{total} = {100*belegt//max(1,total)}%)",
              belegt * 10 >= total * 7)

        print()
        print("Section 9. Total graph health")
        n = s.run("MATCH (di:DataIssue) RETURN count(di) AS n").single()["n"]
        check("DataIssue still 0", n == 0)
        n = s.run("MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS "
                  "{ MATCH (:Projekt)-[:HAT_BAUTEILGRUPPE]->(bg) } RETURN count(bg) AS n").single()["n"]
        check(f"No orphan Bauteilgruppen (got {n})", n == 0)
        n = s.run("MATCH ()-[r:HAT_METHODE|HAT_AUFBEREITUNG|HAT_RESSOURCENQUELLE"
                  "|HAT_RUECKBAUVERFAHREN]->(t) WHERE labels(t) = [] "
                  "RETURN count(r) AS n").single()["n"]
        check("No dangling vocab edges", n == 0)

        print()
        print("=" * 60)
        print(f"  TOTAL: {passes} pass / {fails} fail")
        print("=" * 60)
finally:
    driver.close()
