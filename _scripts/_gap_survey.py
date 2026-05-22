"""Exhaustive gap survey of the live mit-bestand graph.

Reports counts that should be 0 (consistency); flags any remaining work.
"""
from __future__ import annotations
import sys
from pathlib import Path

_SCRIPTS = Path(__file__).resolve().parent
if str(_SCRIPTS) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS))

from neo4j_env import resolve_connection


CHECKS = [
    # Core
    ('Total nodes', 'MATCH (n) RETURN count(n) AS c', None),
    ('Total rels', 'MATCH ()-[r]->() RETURN count(r) AS c', None),
    ('Distinct labels', 'CALL db.labels() YIELD label RETURN count(label) AS c', None),
    ('Distinct rel types', 'CALL db.relationshipTypes() YIELD relationshipType RETURN count(relationshipType) AS c', None),
    # Hygiene (should be 0)
    # NOTE: the former 'Nodes missing source_scope' check was retired on 2026-06-01.
    # source_scope was intentionally dropped from every label during the minimal-
    # property cleanup (provenance now lives on Quelle nodes + BELEGT_IN edges).
    ('r.id NULL', 'MATCH ()-[r]->() WHERE r.id IS NULL RETURN count(r) AS c', 0),
    ('Case-specific nodes missing BELEGT_IN',
     'MATCH (n) WHERE any(l IN labels(n) WHERE l IN ["Projekt","Bauteilgruppe","Bauwerk","Wiederverwendungskette","Stadt"]) AND NOT EXISTS { (n)-[:BELEGT_IN]->(:Quelle) } RETURN count(n) AS c', 0),
    # BG mandatory rels (should be 0)
    ('BG missing HAT_BAUTEILEBENE', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUTEILEBENE]->() } RETURN count(bg) AS c', 0),
    ('BG missing HAT_STATUS', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_STATUS]->() } RETURN count(bg) AS c', 0),
    ('BG missing HAT_RESSOURCENQUELLE', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_RESSOURCENQUELLE]->() } RETURN count(bg) AS c', 0),
    ('BG missing HAT_BAUTEILTYP', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUTEILTYP]->() } RETURN count(bg) AS c', 0),
    ('BG missing HAT_MATERIALGRUPPE', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_MATERIALGRUPPE]->() } RETURN count(bg) AS c', 0),
    ('BG missing HAT_WIEDERVERWENDUNGSART', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_WIEDERVERWENDUNGSART]->() } RETURN count(bg) AS c', 0),
    # BG optional vocab (informational; not 0)
    ('BG without HAT_BESCHAFFUNGSWEG', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BESCHAFFUNGSWEG]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_VERBINDUNGSTECHNIK', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_VERBINDUNGSTECHNIK]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_PRUEFUNG', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_PRUEFUNG]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_LEISTUNGSANFORDERUNG', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_LEISTUNGSANFORDERUNG]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_MARKTMODELL', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_MARKTMODELL]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_LOGISTIK', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_LOGISTIK]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_AUFBEREITUNG', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_AUFBEREITUNG]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_RUECKBAUVERFAHREN', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_RUECKBAUVERFAHREN]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_ZUSTANDSKLASSE', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_ZUSTANDSKLASSE]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_BAUPRODUKTSTATUS', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_BAUPRODUKTSTATUS]->() } RETURN count(bg) AS c', None),
    ('BG without NUTZT_MATERIAL', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:NUTZT_MATERIAL]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_DEFEKT', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_DEFEKT]->() } RETURN count(bg) AS c', None),
    ('BG without HAT_SCHADSTOFF', 'MATCH (bg:Bauteilgruppe) WHERE NOT EXISTS { (bg)-[:HAT_SCHADSTOFF]->() } RETURN count(bg) AS c', None),
    # Bauwerk
    ('Bauwerk missing HAT_STATUS', 'MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_STATUS]->() } RETURN count(bw) AS c', 0),
    ('Bauwerk missing HAT_BAUOBJEKTROLLE', 'MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_BAUOBJEKTROLLE]->() } RETURN count(bw) AS c', None),
    ('Bauwerk missing HAT_BAUOBJEKTKLASSE', 'MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:HAT_BAUOBJEKTKLASSE]->() } RETURN count(bw) AS c', None),
    ('Bauwerk missing LIEGT_IN_STADT', 'MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:LIEGT_IN_STADT]->() } RETURN count(bw) AS c', None),
    ('Bauwerk missing LIEGT_IN_LAND', 'MATCH (bw:Bauwerk) WHERE NOT EXISTS { (bw)-[:LIEGT_IN_LAND]->() } RETURN count(bw) AS c', None),
    # Projekt
    ('Projekt missing LIEGT_IN_STADT', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:LIEGT_IN_STADT]->() } RETURN count(p) AS c', None),
    ('Projekt missing LIEGT_IN_LAND', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:LIEGT_IN_LAND]->() } RETURN count(p) AS c', None),
    ('Projekt missing HAT_INTERVENTION', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:HAT_INTERVENTION]->() } RETURN count(p) AS c', None),
    ('Projekt missing HAT_NUTZUNG', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:HAT_NUTZUNG]->() } RETURN count(p) AS c', None),
    ('Projekt missing HAT_METHODE', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:HAT_METHODE]->() } RETURN count(p) AS c', None),
    ('Programm missing HAT_METHODE', 'MATCH (p:Programm) WHERE NOT EXISTS { (p)-[:HAT_METHODE]->() } RETURN count(p) AS c', None),
    ('Projekt missing HAS_BAUWERK', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:HAS_BAUWERK]->(:Bauwerk) } RETURN count(p) AS c', None),
    ('Projekt missing TEIL_VON_PROGRAMM', 'MATCH (p:Projekt) WHERE NOT EXISTS { (p)-[:TEIL_VON_PROGRAMM]->() } RETURN count(p) AS c', None),
    # Akteur
    ('Akteur missing HAT_AKTEURROLLE', 'MATCH (a:Akteur) WHERE NOT EXISTS { (a)-[:HAT_AKTEURROLLE]->() } RETURN count(a) AS c', None),
    ('Akteur missing HAT_AKTEURTYP', 'MATCH (a:Akteur) WHERE NOT EXISTS { (a)-[:HAT_AKTEURTYP]->() } RETURN count(a) AS c', None),
    ('Akteur 0-degree (true orphans)', 'MATCH (a:Akteur) WHERE NOT EXISTS { (a)-[]-() } RETURN count(a) AS c', None),
    ('Akteur deg=1', 'MATCH (a:Akteur) WITH a, size([(a)-[r]-()|r]) AS d WHERE d = 1 RETURN count(a) AS c', None),
    # Quelle
    ('Quelle missing url', 'MATCH (q:Quelle) WHERE q.url IS NULL RETURN count(q) AS c', None),
    ('Quelle missing quelltyp', 'MATCH (q:Quelle) WHERE q.quelltyp IS NULL RETURN count(q) AS c', None),
    # Programm
    ('Programm missing properties (type)', 'MATCH (p:Programm) WHERE p.type IS NULL RETURN count(p) AS c', None),
    # Naming
    ('Projekt name > 25 chars', 'MATCH (p:Projekt) WHERE size(p.name) > 25 RETURN count(p) AS c', None),
    ('Programm name > 25 chars', 'MATCH (p:Programm) WHERE size(p.name) > 25 RETURN count(p) AS c', None),
    ('Bauwerk name > 25 chars', 'MATCH (bw:Bauwerk) WHERE size(bw.name) > 25 RETURN count(bw) AS c', None),
    ('Bauteilgruppe name > 25 chars', 'MATCH (bg:Bauteilgruppe) WHERE size(bg.name) > 25 RETURN count(bg) AS c', None),
    ('Wiederverwendungskette name > 25 chars', 'MATCH (k:Wiederverwendungskette) WHERE size(k.name) > 25 RETURN count(k) AS c', None),
]


def main() -> int:
    sys.stdout.reconfigure(encoding='utf-8')
    from neo4j import GraphDatabase
    uri, user, password, database = resolve_connection()
    driver = GraphDatabase.driver(uri, auth=(user, password))
    try:
        with driver.session(database=database) as session:
            for label, q, expected_zero in CHECKS:
                try:
                    v = session.run(q).single()['c']
                except Exception as e:
                    print(f'  {label:<55}  ERROR {e}')
                    continue
                marker = ''
                if expected_zero == 0:
                    marker = 'OK' if v == 0 else 'FAIL'
                print(f'  {label:<55}  {v:>6}  {marker}')
    finally:
        driver.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
