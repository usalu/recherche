"""
Remap Akteurtyp + Akteurrolle to compact controlled vocabulary.

Idempotent: safe to run multiple times.
"""

from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from _scripts.neo4j_env import resolve_connection
from neo4j import GraphDatabase

# ---------------------------------------------------------------------------
# Canonical vocabulary
# ---------------------------------------------------------------------------

AKTEURTYP_CANONICAL: dict[str, str] = {
    "at_person":                      "Person",
    "at_unternehmen":                 "Unternehmen",
    "at_organisation":                "Organisation",
    "at_oeffentliche_institution":    "Oeffentliche_Institution",
    "at_forschung_lehre":             "Forschung_Lehre",
    "at_ngo_verband_netzwerk":        "NGO_Verband_Netzwerk",
    "at_materialhub_bauteilboerse":   "Materialhub_Bauteilboerse",
    "at_software_tool_anbieter":      "Software_Tool_Anbieter",
    "at_foerdergeber_programmtraeger":"Foerdergeber_Programmtraeger",
    "at_unbekannt":                   "Unbekannt",
}

AKTEURROLLE_CANONICAL: dict[str, str] = {
    "ar_bauherr_auftraggeber":              "Bauherr_Auftraggeber",
    "ar_entwurf_planung":                   "Entwurf_Planung",
    "ar_fachplanung_nachweis":              "Fachplanung_Nachweis",
    "ar_bauausfuehrung_fertigung":          "Bauausfuehrung_Fertigung",
    "ar_rueckbau_bauteilernte_logistik":    "Rueckbau_Bauteilernte_Logistik",
    "ar_materiallieferung_markt":           "Materiallieferung_Markt",
    "ar_aufbereitung_refurbishment":        "Aufbereitung_Refurbishment",
    "ar_reuse_zirkularitaetsberatung":      "Reuse_Zirkularitaetsberatung",
    "ar_forschung_dokumentation":           "Forschung_Dokumentation",
    "ar_oeffentliche_hand_foerderung":      "Oeffentliche_Hand_Foerderung",
    "ar_betrieb_nutzung":                   "Betrieb_Nutzung",
    "ar_bildung_wissenstransfer":           "Bildung_Wissenstransfer",
    "ar_software_digitalisierung":          "Software_Digitalisierung",
    "ar_projektmanagement_koordination":    "Projektmanagement_Koordination",
    "ar_unbestimmt":                        "Unbestimmt",
}

AKTEURTYP_REMAP: dict[str, str] = {
    "at_person":                         "at_person",
    "at_organisation":                   "at_organisation",
    "at_unternehmen":                    "at_unternehmen",
    "at_oeffentliche_institution":       "at_oeffentliche_institution",
    "at_forschung_lehre":                "at_forschung_lehre",
    "at_ngo_verband_netzwerk":           "at_ngo_verband_netzwerk",
    "at_materialhub_bauteilboerse":      "at_materialhub_bauteilboerse",
    "at_foerdergeber_programmtraeger":   "at_foerdergeber_programmtraeger",
    "at_software_tool_anbieter":         "at_software_tool_anbieter",
    "at_unbekannt":                      "at_unbekannt",
    # remaps
    "at_ngo_netzwerk":                   "at_ngo_verband_netzwerk",
    "at_verband_kammer":                 "at_ngo_verband_netzwerk",
    "at_architekturburo":                "at_unternehmen",
    "at_ingenieurburo":                  "at_unternehmen",
    "at_bauunternehmen":                 "at_unternehmen",
    "at_rueckbauunternehmen":            "at_unternehmen",
    "at_materiallieferant_hersteller":   "at_unternehmen",
    "at_reuse_consultancy_zirkularitaet":"at_unternehmen",
    "at_developer_immobilien":           "at_unternehmen",
    "at_wohnungsbau_genossenschaft":     "at_organisation",
    "at_universitaet_forschungsinstitut":"at_forschung_lehre",
    "at_kultur_bildung_ausstellung":     "at_organisation",
    "at_betreiber_nutzerorganisation":   "at_organisation",
    "at_zertifizierer_pruefstelle":      "at_organisation",
}

AKTEURROLLE_REMAP: dict[str, str] = {
    "ar_architektur":                           "ar_entwurf_planung",
    "ar_fassade":                               "ar_entwurf_planung",
    "ar_kunst_gestaltung":                      "ar_entwurf_planung",
    "ar_landschaftsplanung":                    "ar_entwurf_planung",
    "ar_entwurf_bauende_praxis":                "ar_entwurf_planung",
    "ar_tragwerksplanung":                      "ar_fachplanung_nachweis",
    "ar_pruefung_qualitaetssicherung":          "ar_fachplanung_nachweis",
    "ar_brandschutz_barrierefreiheit":          "ar_fachplanung_nachweis",
    "ar_tga_gebaeudetechnik":                   "ar_fachplanung_nachweis",
    "ar_bauausfuehrung":                        "ar_bauausfuehrung_fertigung",
    "ar_stahlbau_fertigung":                    "ar_bauausfuehrung_fertigung",
    "ar_produkt_bausystementwicklung":          "ar_bauausfuehrung_fertigung",
    "ar_rueckbau_demontage":                    "ar_rueckbau_bauteilernte_logistik",
    "ar_bauteilernte_materialakquise":          "ar_rueckbau_bauteilernte_logistik",
    "ar_logistik_transport":                    "ar_rueckbau_bauteilernte_logistik",
    "ar_materiallieferant":                     "ar_materiallieferung_markt",
    "ar_vermittlung_marktplatz":                "ar_materiallieferung_markt",
    "ar_materialhub_bauteilboerse":             "ar_materiallieferung_markt",
    "ar_bauteilboerse_bauteilernte_markt":      "ar_materiallieferung_markt",
    "ar_aufbereitung_refurbishment":            "ar_aufbereitung_refurbishment",
    "ar_reuse_beratung":                        "ar_reuse_zirkularitaetsberatung",
    "ar_nachhaltigkeitsberatung":               "ar_reuse_zirkularitaetsberatung",
    "ar_zertifizierung_bewertung":              "ar_reuse_zirkularitaetsberatung",
    "ar_konzept_future_reuse_system":           "ar_reuse_zirkularitaetsberatung",
    "ar_forschung_dokumentation":               "ar_forschung_dokumentation",
    "ar_technik_forschung_nachweis":            "ar_forschung_dokumentation",
    "ar_materialpass_digitalisierung":          "ar_software_digitalisierung",
    "ar_software_tool":                         "ar_software_digitalisierung",
    "ar_bauherr_auftraggeber":                  "ar_bauherr_auftraggeber",
    "ar_betreiber_nutzer":                      "ar_betrieb_nutzung",
    "ar_oeffentliche_hand":                     "ar_oeffentliche_hand_foerderung",
    "ar_foerderung_programmsteuerung":          "ar_oeffentliche_hand_foerderung",
    "ar_bildung_wissenstransfer":               "ar_bildung_wissenstransfer",
    "ar_organisation_bildung_wissenstransfer":  "ar_bildung_wissenstransfer",
    "ar_ausstellung_kuration":                  "ar_bildung_wissenstransfer",
    "ar_projektmanagement_koordination":        "ar_projektmanagement_koordination",
    "ar_projektbeteiligte_unbestimmt":          "ar_unbestimmt",
    "ar_entwurf_planung":                       "ar_entwurf_planung",
    "ar_fachplanung_nachweis":                  "ar_fachplanung_nachweis",
    "ar_bauausfuehrung_fertigung":              "ar_bauausfuehrung_fertigung",
    "ar_rueckbau_bauteilernte_logistik":        "ar_rueckbau_bauteilernte_logistik",
    "ar_materiallieferung_markt":               "ar_materiallieferung_markt",
    "ar_reuse_zirkularitaetsberatung":          "ar_reuse_zirkularitaetsberatung",
    "ar_oeffentliche_hand_foerderung":          "ar_oeffentliche_hand_foerderung",
    "ar_betrieb_nutzung":                       "ar_betrieb_nutzung",
    "ar_software_digitalisierung":              "ar_software_digitalisierung",
    "ar_unbestimmt":                            "ar_unbestimmt",
}


def run(tx, query, **params):
    result = tx.run(query, **params)
    return result.consume()


def main() -> None:
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))

    with driver.session(database=database) as s:

        # ------------------------------------------------------------------
        # 1. Ensure canonical Akteurtyp nodes exist
        # ------------------------------------------------------------------
        print("=== 1. Ensuring canonical Akteurtyp nodes ===")
        for id_, name in AKTEURTYP_CANONICAL.items():
            info = s.execute_write(
                lambda tx, i=id_, n=name: run(
                    tx,
                    "MERGE (t:Akteurtyp {id: $id}) SET t.name = $name RETURN t",
                    id=i, name=n
                )
            )
            print(f"  MERGE Akteurtyp {id_}")

        # ------------------------------------------------------------------
        # 2. Ensure canonical Akteurrolle nodes exist
        # ------------------------------------------------------------------
        print("=== 2. Ensuring canonical Akteurrolle nodes ===")
        for id_, name in AKTEURROLLE_CANONICAL.items():
            s.execute_write(
                lambda tx, i=id_, n=name: run(
                    tx,
                    "MERGE (r:Akteurrolle {id: $id}) SET r.name = $name RETURN r",
                    id=i, name=n
                )
            )
            print(f"  MERGE Akteurrolle {id_}")

        # ------------------------------------------------------------------
        # 3. Remap HAT_AKTEURTYP: retarget to canonical node
        # ------------------------------------------------------------------
        print("=== 3. Remapping HAT_AKTEURTYP ===")
        for old_id, new_id in AKTEURTYP_REMAP.items():
            if old_id == new_id:
                continue
            summary = s.execute_write(
                lambda tx, oid=old_id, nid=new_id: run(
                    tx,
                    """
                    MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(old:Akteurtyp {id: $old_id})
                    MATCH (new:Akteurtyp {id: $new_id})
                    WHERE NOT (a)-[:HAT_AKTEURTYP]->(new)
                    MERGE (a)-[:HAT_AKTEURTYP]->(new)
                    DELETE r
                    """,
                    old_id=oid, new_id=nid
                )
            )
            # Also handle duplicates where both old and new exist
            s.execute_write(
                lambda tx, oid=old_id, nid=new_id: run(
                    tx,
                    """
                    MATCH (a:Akteur)-[r:HAT_AKTEURTYP]->(old:Akteurtyp {id: $old_id})
                    MATCH (a)-[:HAT_AKTEURTYP]->(:Akteurtyp {id: $new_id})
                    DELETE r
                    """,
                    old_id=oid, new_id=nid
                )
            )
            print(f"  {old_id} -> {new_id}")

        # ------------------------------------------------------------------
        # 4. Remap HAT_AKTEURROLLE: retarget + set scope
        # ------------------------------------------------------------------
        print("=== 4. Remapping HAT_AKTEURROLLE ===")
        for old_id, new_id in AKTEURROLLE_REMAP.items():
            if old_id == new_id:
                # Just ensure scope is set on already-canonical relationships
                s.execute_write(
                    lambda tx, oid=old_id: run(
                        tx,
                        """
                        MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(ar:Akteurrolle {id: $role_id})
                        WHERE r.scope IS NULL
                        SET r.scope = 'expertise_profile'
                        """,
                        role_id=oid
                    )
                )
            else:
                # Retarget: create new rel to canonical, delete old
                s.execute_write(
                    lambda tx, oid=old_id, nid=new_id: run(
                        tx,
                        """
                        MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(old:Akteurrolle {id: $old_id})
                        MATCH (new:Akteurrolle {id: $new_id})
                        WHERE NOT (a)-[:HAT_AKTEURROLLE {scope: coalesce(r.scope, 'expertise_profile')}]->(new)
                        CREATE (a)-[:HAT_AKTEURROLLE {
                            id: 'r_' + a.id + '__HAT_AKTEURROLLE__' + $new_id,
                            scope: coalesce(r.scope, 'expertise_profile')
                        }]->(new)
                        DELETE r
                        """,
                        old_id=oid, new_id=nid
                    )
                )
                # Clean up any remaining old->old dups (actor already had canonical)
                s.execute_write(
                    lambda tx, oid=old_id, nid=new_id: run(
                        tx,
                        """
                        MATCH (a:Akteur)-[r:HAT_AKTEURROLLE]->(old:Akteurrolle {id: $old_id})
                        WHERE (a)-[:HAT_AKTEURROLLE]->(:Akteurrolle {id: $new_id})
                        DELETE r
                        """,
                        old_id=oid, new_id=nid
                    )
                )
            print(f"  {old_id} -> {new_id}")

        # ------------------------------------------------------------------
        # 5. Set scope on any remaining HAT_AKTEURROLLE without scope
        # ------------------------------------------------------------------
        print("=== 5. Setting missing scope on HAT_AKTEURROLLE ===")
        s.execute_write(
            lambda tx: run(
                tx,
                """
                MATCH ()-[r:HAT_AKTEURROLLE]->()
                WHERE r.scope IS NULL
                SET r.scope = 'expertise_profile'
                """
            )
        )

        # ------------------------------------------------------------------
        # 6. Delete obsolete Akteurtyp nodes (not in canonical set)
        # ------------------------------------------------------------------
        print("=== 6. Deleting obsolete Akteurtyp nodes ===")
        canonical_at_ids = list(AKTEURTYP_CANONICAL.keys())
        s.execute_write(
            lambda tx, ids=canonical_at_ids: run(
                tx,
                """
                MATCH (t:Akteurtyp)
                WHERE NOT t.id IN $ids
                DETACH DELETE t
                """,
                ids=ids
            )
        )

        # ------------------------------------------------------------------
        # 7. Delete obsolete Akteurrolle nodes (not in canonical set)
        # ------------------------------------------------------------------
        print("=== 7. Deleting obsolete Akteurrolle nodes ===")
        canonical_ar_ids = list(AKTEURROLLE_CANONICAL.keys())
        s.execute_write(
            lambda tx, ids=canonical_ar_ids: run(
                tx,
                """
                MATCH (r:Akteurrolle)
                WHERE NOT r.id IN $ids
                DETACH DELETE r
                """,
                ids=ids
            )
        )

        # ------------------------------------------------------------------
        # 8. Remove AkteurFokus nodes (safety)
        # ------------------------------------------------------------------
        print("=== 8. Removing AkteurFokus nodes ===")
        s.execute_write(
            lambda tx: run(tx, "MATCH (n:AkteurFokus) DETACH DELETE n")
        )

        # ------------------------------------------------------------------
        # 9. Remove IST_UNTERROLLE_VON / IST_UNTERTYP_VON (safety)
        # ------------------------------------------------------------------
        print("=== 9. Removing IST_UNTERROLLE_VON / IST_UNTERTYP_VON ===")
        s.execute_write(
            lambda tx: run(
                tx,
                "MATCH ()-[r:IST_UNTERROLLE_VON|IST_UNTERTYP_VON]->() DELETE r"
            )
        )

        # ------------------------------------------------------------------
        # 10. ASSOZIIERT_MIT_PROJEKT: ensure needs_verification = true
        # ------------------------------------------------------------------
        print("=== 10. Patching ASSOZIIERT_MIT_PROJEKT ===")
        s.execute_write(
            lambda tx: run(
                tx,
                """
                MATCH ()-[r:ASSOZIIERT_MIT_PROJEKT]->()
                WHERE r.needs_verification IS NULL OR r.needs_verification <> true
                SET r.needs_verification = true, r.source_scope = 'actor_registry'
                """
            )
        )

        # ------------------------------------------------------------------
        # Validation report
        # ------------------------------------------------------------------
        print("\n=== VALIDATION REPORT ===")

        result = s.run("MATCH (n:Akteurtyp) RETURN n.id AS id, n.name AS name ORDER BY n.id")
        rows = result.data()
        print(f"\nAkteurtyp nodes ({len(rows)}):")
        for r in rows:
            print(f"  {r['id']} -> {r['name']}")

        result = s.run("MATCH (n:Akteurrolle) RETURN n.id AS id, n.name AS name ORDER BY n.id")
        rows = result.data()
        print(f"\nAkteurrolle nodes ({len(rows)}):")
        for r in rows:
            print(f"  {r['id']} -> {r['name']}")

        result = s.run(
            "MATCH ()-[r:HAT_AKTEURROLLE]->() "
            "RETURN count(r) AS total, count(r.scope) AS with_scope"
        )
        row = result.single()
        print(f"\nHAT_AKTEURROLLE: total={row['total']}, with_scope={row['with_scope']}")

        result = s.run("MATCH (n:AkteurFokus) RETURN count(n) AS cnt")
        print(f"AkteurFokus nodes: {result.single()['cnt']} (expect 0)")

        result = s.run(
            "MATCH ()-[r:IST_UNTERROLLE_VON|IST_UNTERTYP_VON]->() RETURN count(r) AS cnt"
        )
        print(f"IST_UNTERROLLE/TYP_VON rels: {result.single()['cnt']} (expect 0)")

        # Check for invalid Akteurtyp/Akteurrolle
        canonical_at = set(AKTEURTYP_CANONICAL.keys())
        result = s.run("MATCH (n:Akteurtyp) RETURN collect(n.id) AS ids")
        actual_at = set(result.single()["ids"])
        invalid_at = actual_at - canonical_at
        print(f"Invalid Akteurtyp: {invalid_at or 'none'}")

        canonical_ar = set(AKTEURROLLE_CANONICAL.keys())
        result = s.run("MATCH (n:Akteurrolle) RETURN collect(n.id) AS ids")
        actual_ar = set(result.single()["ids"])
        invalid_ar = actual_ar - canonical_ar
        print(f"Invalid Akteurrolle: {invalid_ar or 'none'}")

        # Scope coverage
        result = s.run(
            "MATCH ()-[r:HAT_AKTEURROLLE]->() WHERE r.scope IS NULL RETURN count(r) AS cnt"
        )
        print(f"HAT_AKTEURROLLE without scope: {result.single()['cnt']} (expect 0)")

        result = s.run(
            "MATCH ()-[r:HAT_AKTEURTYP]->(:Akteurtyp) RETURN count(r) AS cnt"
        )
        print(f"HAT_AKTEURTYP relationships: {result.single()['cnt']}")

    driver.close()
    print("\nDone.")


if __name__ == "__main__":
    main()
