# Vollständiger Hürden-Baum (DE, alle Ebenen)

8 Bereiche (A–H) · ~55 Kategorien · ~330 Blätter · ~400 Knoten.
`◀ LIVE` = natürlicher Anker einer der 11 aktuellen Hürden (Ebene, wo sie wirklich passt — nicht erzwungen).
Zwei Live-Hürden (`Ausschreibungsproblem`, `Entwurfsbindung`) haben **keinen** natürlichen Treffer → nicht im Baum.

```
DIGITALES WIEDERVERWENDUNGS-HÜRDENSYSTEM
│
├─ A · Informationsgrundlage
│  ├─ A1 Informationsverfügbarkeit
│  │  ├─ A1.1 Fehlende Bestandsdaten
│  │  │  ├─ A1.1.1 Fehlende As-built-Informationen
│  │  │  ├─ A1.1.2 Fehlendes BIM-/digitales Gebäudemodell
│  │  │  └─ A1.1.3 Fehlende Sanierungshistorie
│  │  ├─ A1.2 Fehlende Bauteildaten
│  │  │  ├─ A1.2.1 Fehlende Herstellerinformation
│  │  │  ├─ A1.2.2 Fehlende Produktmodell-Information
│  │  │  ├─ A1.2.3 Fehlende Bauteilkennung
│  │  │  └─ A1.2.4 Fehlendes Einbaudatum
│  │  ├─ A1.3 Fehlende technische Nachweise
│  │  │  ├─ A1.3.1 Fehlende Leistungsdaten
│  │  │  ├─ A1.3.2 Fehlende Wartungsprotokolle
│  │  │  ├─ A1.3.3 Fehlende Prüfdokumentation
│  │  │  └─ A1.3.4 Fehlende Originalzertifizierung
│  │  └─ A1.4 Unzureichende Sekundärprodukt-Inventare
│  │     ├─ A1.4.1 Begrenzte Inventarabdeckung
│  │     ├─ A1.4.2 Unzugängliche Listungen
│  │     └─ A1.4.3 Lückenhafte geografische Abdeckung
│  ├─ A2 Informationsspezifikation
│  │  ├─ A2.1 Undefinierter Mindest-Bauteildatensatz
│  │  ├─ A2.2 Übermäßige Pflichtinformationen
│  │  ├─ A2.3 Inkonsistente Pflichtfelder
│  │  ├─ A2.4 Stakeholder-spezifische Informationskonflikte
│  │  ├─ A2.5 Produktkategorie-spezifische Informationsunterschiede
│  │  └─ A2.6 Unklare Informationsgranularität
│  │     ├─ A2.6.1 Produktmodell-Ebene
│  │     ├─ A2.6.2 Chargen-Ebene
│  │     ├─ A2.6.3 Einzelbauteil-Ebene
│  │     └─ A2.6.4 Baugruppen-Ebene
│  ├─ A3 Informationsqualität
│  │  ├─ A3.1 Unvollständige Daten
│  │  ├─ A3.2 Fehlerhafte Daten
│  │  ├─ A3.3 Veraltete Daten
│  │  ├─ A3.4 Inkonsistente Daten
│  │  ├─ A3.5 Ungültige Daten
│  │  ├─ A3.6 Ungeprüfte Daten
│  │  ├─ A3.7 Fehlende Provenienz
│  │  ├─ A3.8 Unklares Konfidenzniveau
│  │  └─ A3.9 Unklare Messmethode
│  └─ A4 Informations-Lebenszyklus-Management
│     ├─ A4.1 Erschwerte Datenerfassung
│     ├─ A4.2 Erschwerte Datentransformation
│     ├─ A4.3 Duplikat-Datensätze
│     ├─ A4.4 Schwache Versionskontrolle
│     ├─ A4.5 Schwache Änderungsverfolgung
│     ├─ A4.6 Fehlende Lebenszyklus-Aktualisierungen
│     ├─ A4.7 Erschwerte Archivierung
│     └─ A4.8 Langzeit-Erhaltungsrisiko
│        ├─ A4.8.1 Obsolete Formate
│        ├─ A4.8.2 Defekte Dokumentverweise
│        ├─ A4.8.3 Plattformbetreiber-Schließung
│        └─ A4.8.4 Verlust bei Datenmigration
│
├─ B · Digitale Interoperabilität & Plattformarchitektur
│  ├─ B1 Technische Interoperabilität
│  │  ├─ B1.1 Inkompatible Softwaresysteme
│  │  ├─ B1.2 Fehlende APIs
│  │  ├─ B1.3 Proprietäre Schnittstellen
│  │  ├─ B1.4 Proprietäre Dateiformate
│  │  ├─ B1.5 Geschlossene digitale Silos
│  │  ├─ B1.6 Begrenzter Import/Export
│  │  └─ B1.7 Instabile Systemintegrationen
│  ├─ B2 Strukturelle Interoperabilität
│  │  ├─ B2.1 Inkompatible Schemata
│  │  ├─ B2.2 Inkompatible Feldstrukturen
│  │  ├─ B2.3 Inkompatible Dateiformate
│  │  ├─ B2.4 Inkonsistente Einheiten
│  │  ├─ B2.5 Inkonsistente Property-Strukturen
│  │  └─ B2.6 Inkonsistente Validierungsregeln
│  ├─ B3 Semantische Interoperabilität
│  │  ├─ B3.1 Inkonsistente Terminologie
│  │  ├─ B3.2 Klassifikations-Mismatch
│  │  ├─ B3.3 Bauteilkategorie-Mismatch
│  │  ├─ B3.4 Property-Definitions-Mismatch
│  │  ├─ B3.5 Unterschiedliche Zustandsvokabulare
│  │  ├─ B3.6 Unterschiedliche Leistungsdefinitionen
│  │  └─ B3.7 Unterschiedliche Lebenszyklus-Status-Definitionen
│  ├─ B4 Identitäts-Interoperabilität
│  │  ├─ B4.1 Fehlende persistente Identifikatoren
│  │  ├─ B4.2 Doppelte Bauteil-Identitäten
│  │  ├─ B4.3 Identifikator-Änderungen zwischen Systemen
│  │  ├─ B4.4 Gebrochene physisch-digitale Verknüpfung
│  │  ├─ B4.5 Unklare Identifikator-Granularität
│  │  └─ B4.6 Fehlende Chargen-zu-Bauteil-Beziehungen
│  ├─ B5 Workflow-Interoperabilität
│  │  ├─ B5.1 Audit von Entwurf entkoppelt
│  │  ├─ B5.2 Entwurf von Marktplatz entkoppelt
│  │  ├─ B5.3 Marktplatz von Zertifizierung entkoppelt
│  │  ├─ B5.4 Matching von Beschaffung entkoppelt
│  │  ├─ B5.5 Beschaffung von Logistik entkoppelt
│  │  ├─ B5.6 Einbau von Lebenszyklus-Daten entkoppelt
│  │  ├─ B5.7 Wiederholte manuelle Dateneingabe
│  │  └─ B5.8 Informationsverlust bei Übergabe
│  ├─ B6 Plattform-Funktionsgrenzen
│  │  ├─ B6.1 Unzureichende Inventar-Werkzeuge
│  │  ├─ B6.2 Unzureichende Zustandsbewertungs-Werkzeuge
│  │  ├─ B6.3 Unzureichendes technisches Matching
│  │  ├─ B6.4 Unzureichendes toleranzbasiertes Matching
│  │  ├─ B6.5 Unzureichende Rückgewinnungsplanung
│  │  ├─ B6.6 Unzureichende Dokumentenprüfung
│  │  ├─ B6.7 Unzureichendes Reservierungsmanagement
│  │  ├─ B6.8 Unzureichende Logistik-Integration
│  │  ├─ B6.9 Unzureichende Lebenszyklus-Verfolgung
│  │  └─ B6.10 Unzureichendes Wirkungs-Reporting
│  └─ B7 Technologie-Nachhaltigkeit
│     ├─ B7.1 Abhängigkeit von Pilotförderung
│     ├─ B7.2 Unklare Wartungs-Verantwortung
│     ├─ B7.3 Instabile Plattform-Einnahmen
│     ├─ B7.4 Software-Obsoleszenz
│     ├─ B7.5 Sinkende Nutzerbeteiligung
│     ├─ B7.6 Integrations-Degradation
│     ├─ B7.7 Digitaler Energieverbrauch
│     └─ B7.8 Digitalgeräte-Entsorgungswirkungen
│
├─ C · Datenverwaltung & Vertrauensinfrastruktur
│  ├─ C1 Dateneigentum
│  │  ├─ C1.1 Unklarer Bauteildatensatz-Eigentümer
│  │  ├─ C1.2 Unklares Eigentum nach Transfer
│  │  ├─ C1.3 Unklare Lieferant-Plattform-Datengrenze
│  │  ├─ C1.4 Unklares Eigentum abgeleiteter Daten
│  │  └─ C1.5 Unklares Eigentum von Inspektionsergebnissen
│  ├─ C2 Datenverantwortung
│  │  ├─ C2.1 Kein zugewiesener Data Steward
│  │  ├─ C2.2 Unklare Datensatz-Erstellungsverantwortung
│  │  ├─ C2.3 Unklare Prüfverantwortung
│  │  ├─ C2.4 Unklare Korrekturverantwortung
│  │  ├─ C2.5 Unklare Zustands-Aktualisierungsverantwortung
│  │  ├─ C2.6 Unklare Zertifizierungs-Aktualisierungsverantwortung
│  │  └─ C2.7 Unklare Verantwortung nach Einbau
│  ├─ C3 Zugriffs-Governance
│  │  ├─ C3.1 Fehlende rollenbasierte Zugriffskontrolle
│  │  ├─ C3.2 Übermäßige öffentliche Offenlegung
│  │  ├─ C3.3 Eingeschränkter Zugriff auf nötige Nachweise
│  │  ├─ C3.4 Unklare Zugriffsrechte nach Eigentumsübergang
│  │  └─ C3.5 Inkonsistente Berechtigungen über Systeme
│  ├─ C4 Datensicherheit
│  │  ├─ C4.1 Unautorisierte Änderung
│  │  ├─ C4.2 Gefälschte Bauteil-Identität
│  │  ├─ C4.3 Gefälschte Zertifikate
│  │  ├─ C4.4 Schwache Nutzer-Authentifizierung
│  │  ├─ C4.5 Schwache API-Sicherheit
│  │  ├─ C4.6 Unzureichendes Audit-Logging
│  │  └─ C4.7 Unzureichende Wiederherstellung nach Datenverlust
│  ├─ C5 Vertraulichkeit & Datenschutz
│  │  ├─ C5.1 Kommerzielle Vertraulichkeit
│  │  ├─ C5.2 Schutz geistigen Eigentums
│  │  ├─ C5.3 Hersteller-Geschäftsgeheimnisse
│  │  ├─ C5.4 Personendatenschutz-Bedenken
│  │  ├─ C5.5 Betriebssicherheits-Bedenken
│  │  └─ C5.6 Eingeschränkte Zusammensetzungs-/Lieferantendaten
│  └─ C6 Evidenz-Autorität
│     ├─ C6.1 Selbstauskunft ohne Prüfung
│     ├─ C6.2 Unklare Autorität der Prüfer
│     ├─ C6.3 Widersprüchliche Evidenzquellen
│     ├─ C6.4 Abgelaufene Evidenz
│     ├─ C6.5 Evidenz nur für vorherige Nutzung gültig
│     └─ C6.6 Keine Unterscheidung geschätzt/geprüft
│
├─ D · Organisatorische & Kapazitätsbedingungen
│  ├─ D1 Organisatorische Fragmentierung
│  │  ├─ D1.1 Temporäre Projektteams
│  │  ├─ D1.2 Getrennte Vertragspakete
│  │  ├─ D1.3 Fragmentierte Lebenszyklus-Verantwortlichkeiten
│  │  ├─ D1.4 Entkoppelte Lieferkettenakteure
│  │  ├─ D1.5 Schwache Zusammenarbeit Quell-/Empfangsprojekt
│  │  └─ D1.6 Informationsverlust bei organisatorischen Übergaben
│  ├─ D2 Prozess-Governance
│  │  ├─ D2.1 Keine harmonisierten Audit-Verfahren
│  │  ├─ D2.2 Keine harmonisierten Prüfverfahren
│  │  ├─ D2.3 Keine harmonisierten Aktualisierungsverfahren
│  │  ├─ D2.4 Keine harmonisierten Streitbeilegungsverfahren
│  │  └─ D2.5 Keine gemeinsamen Data-Governance-Protokolle
│  ├─ D3 Fehlende organisatorische Rollen
│  │  ├─ D3.1 Fehlender Reuse-Koordinator
│  │  ├─ D3.2 Fehlender Material-Auditor
│  │  ├─ D3.3 Fehlender Data Steward
│  │  ├─ D3.4 Fehlender Bauteil-Bewerter
│  │  ├─ D3.5 Fehlender Passport-Manager
│  │  ├─ D3.6 Fehlender Reuse-Beschaffungsspezialist
│  │  └─ D3.7 Fehlender Rückbauplaner
│  ├─ D4 Kompetenzen & Personal
│  │  ├─ D4.1 Unzureichende digitale Kompetenzen
│  │  │  ├─ D4.1.1 BIM/openBIM-Kompetenzlücken
│  │  │  ├─ D4.1.2 Datenbank-Kompetenzlücken
│  │  │  ├─ D4.1.3 API-Kompetenzlücken
│  │  │  └─ D4.1.4 Data-Governance-Kompetenzlücken
│  │  ├─ D4.2 Unzureichende Reuse-Kompetenzen
│  │  │  ├─ D4.2.1 Materialidentifikations-Lücken
│  │  │  ├─ D4.2.2 Zustandsbewertungs-Lücken
│  │  │  ├─ D4.2.3 Rückbauplanungs-Lücken
│  │  │  ├─ D4.2.4 Reuse-Beschaffungs-Lücken
│  │  │  └─ D4.2.5 Regulatorisches-Wissen-Lücken
│  │  └─ D4.3 Unzureichende Personalkapazität
│  │     ├─ D4.3.1 Zu wenige qualifizierte Auditoren
│  │     ├─ D4.3.2 Zu wenige Rückbauspezialisten
│  │     ├─ D4.3.3 Zu wenige technische Bewerter
│  │     └─ D4.3.4 Zu wenig Datenmanagement-Personal
│  ├─ D5 Bewusstsein & Commitment
│  │  ├─ D5.1 Begrenztes Bewusstsein für Reuse-Chancen
│  │  ├─ D5.2 Begrenztes Bewusstsein für digitale Systeme
│  │  ├─ D5.3 Begrenztes Bewusstsein für verfügbare Inventare
│  │  ├─ D5.4 Begrenztes Bewusstsein für rechtliche Anforderungen
│  │  ├─ D5.5 Schwaches Stakeholder-Commitment
│  │  ├─ D5.6 Schwache Langzeit-Beteiligung
│  │  └─ D5.7 Geringe Bereitschaft zur Datenteilung
│  └─ D6 Adoptionswiderstand            ◀ LIVE: Akzeptanzproblem
│     ├─ D6.1 Widerstand gegen Prozessänderung
│     ├─ D6.2 Zurückhaltung bei digitaler Technologie
│     ├─ D6.3 Präferenz für etablierte Beschaffung
│     ├─ D6.4 Kulturelle Präferenz für Neuprodukte
│     ├─ D6.5 Geringer wahrgenommener digitaler Wert
│     ├─ D6.6 Ungleiche Verteilung digitaler Vorteile
│     └─ D6.7 Wahrgenommene Last ohne direkten Ertrag
│
├─ E · Wirtschaftlichkeit & Marktreife
│  ├─ E1 Digitale Implementierungskosten
│  │  ├─ E1.1 Vermessungskosten          ├─ E1.7 Datenbereinigungskosten
│  │  ├─ E1.2 Scan-Kosten                 ├─ E1.8 Prüfkosten
│  │  ├─ E1.3 BIM-Modellierungskosten     ├─ E1.9 Cybersicherheitskosten
│  │  ├─ E1.4 Softwareentwicklungskosten  ├─ E1.10 Schulungskosten
│  │  ├─ E1.5 Softwarelizenzkosten        └─ E1.11 Hosting-/Wartungskosten
│  │  └─ E1.6 Integrationskosten
│  ├─ E2 Begrenzte Finanzkraft
│  │  ├─ E2.1 KMU-Finanzierungsengpässe
│  │  ├─ E2.2 Kommunale Finanzierungsengpässe
│  │  ├─ E2.3 Engpässe kleiner Reuse-Händler
│  │  ├─ E2.4 Begrenzte Eigentümer-Investition
│  │  └─ E2.5 Ökonomie geringwertiger Bauteile
│  ├─ E3 Schwache Anreize
│  │  ├─ E3.1 Billige Entsorgung
│  │  ├─ E3.2 Billige Neuprodukte
│  │  ├─ E3.3 Umweltkosten nicht eingepreist
│  │  ├─ E3.4 Keine Belohnung für Produktdaten-Erstellung
│  │  ├─ E3.5 Keine Belohnung für Lebenszyklus-Aktualisierung
│  │  └─ E3.6 Keine Wiederverwendungs-Beschaffungspflicht
│  ├─ E4 Unsichere Plattform-Rendite
│  │  ├─ E4.1 Unklares Erlösmodell
│  │  ├─ E4.2 Unsichere Transaktionsprovision
│  │  ├─ E4.3 Unsichere Abonnement-Nachfrage
│  │  ├─ E4.4 Unsicherer Wert des Wirkungs-Reportings
│  │  ├─ E4.5 Unsichere vermiedene-Kosten-Vorteile
│  │  └─ E4.6 Plattformwert auf verschiedene Akteure verteilt
│  ├─ E5 Unreife Reuse-Märkte            ◐ LIVE: Heterogenitaet_Chargen
│  │  ├─ E5.1 Begrenzte Käufernachfrage
│  │  ├─ E5.2 Unregelmäßiges Angebot
│  │  ├─ E5.3 Begrenzter geografischer Marktzugang
│  │  ├─ E5.4 Geringes Transaktionsvolumen
│  │  ├─ E5.5 Schwache Preistransparenz
│  │  ├─ E5.6 Inkonsistente Produktqualität
│  │  └─ E5.7 Schwache Gewährleistungsverfügbarkeit
│  └─ E6 Netzwerkdichte-Grenzen
│     ├─ E6.1 Zu wenige aktive Anbieter    ├─ E6.4 Zu wenige erfolgreiche Matches
│     ├─ E6.2 Zu wenige aktive Käufer      ├─ E6.5 Zu wenige Wiederholungstransaktionen
│     └─ E6.3 Zu wenige vollständige Listungen └─ E6.6 Unzureichende regionale Dichte
│
├─ F · Regulierung, Konformität & Risiko
│  ├─ F1 Regulatorische Unsicherheit
│  │  ├─ F1.1 Unzureichende reuse-spezifische Regulierung
│  │  ├─ F1.2 Inkonsistente nationale/regionale Regeln
│  │  ├─ F1.3 Unklarer Produkt-vs-Abfall-Status
│  │  ├─ F1.4 Unklare Regeln für Second-Life-Produkte
│  │  ├─ F1.5 Sich entwickelnde Digital-Product-Passport-Regeln
│  │  └─ F1.6 Produktkategorie-spezifische regulatorische Unterschiede
│  ├─ F2 Dokumentations-Konformität
│  │  ├─ F2.1 Fehlende Originalerklärung
│  │  ├─ F2.2 Fehlende Konformitätsdokumentation
│  │  ├─ F2.3 Fehlende technische Unterlage
│  │  ├─ F2.4 Fehlende Produkthistorie
│  │  ├─ F2.5 Fehlende Verwendungszweck-Information
│  │  └─ F2.6 Fehlende Gefahrstoff-Information
│  ├─ F3 Zertifizierungs-Unsicherheit
│  │  ├─ F3.1 Unklare Zertifikatsgültigkeit nach Ausbau
│  │  ├─ F3.2 Unklare Nachprüfungspflicht
│  │  ├─ F3.3 Unklarer Konformitätsbewertungs-Weg
│  │  ├─ F3.4 Unklare zuständige Bewertungsstelle
│  │  ├─ F3.5 Unklare Anerkennung historischer Prüfergebnisse
│  │  └─ F3.6 Andere Anforderungen bei geänderter Nutzung
│  ├─ F4 Haftungs-Unsicherheit
│  │  ├─ F4.1 Unklare Vorbesitzer-Haftung
│  │  ├─ F4.2 Unklare Hersteller-Haftung
│  │  ├─ F4.3 Unklare Plattform-Haftung
│  │  ├─ F4.4 Unklare Auditor-Haftung
│  │  ├─ F4.5 Unklare Labor-Haftung
│  │  ├─ F4.6 Unklare Planer-/Ingenieur-Haftung
│  │  └─ F4.7 Unklare Auftragnehmer-/Einbau-Haftung
│  ├─ F5 Gewährleistungs-Unsicherheit
│  │  ├─ F5.1 Keine Standard-Reuse-Produktgewährleistung
│  │  ├─ F5.2 Unklarer Gewährleistungsgeber
│  │  ├─ F5.3 Unklare Gewährleistungsdauer
│  │  ├─ F5.4 Unklare Gewährleistungsausschlüsse
│  │  └─ F5.5 Produktspezifische Gewährleistungsunterschiede
│  └─ F6 Technisches Risiko              ◐ LIVE: Unkonventionelles_Material
│     ├─ F6.1 Unsichere Leistung
│     ├─ F6.2 Unsicherer Zustand
│     ├─ F6.3 Unsichere Restnutzungsdauer
│     ├─ F6.4 Unsichere Sicherheit
│     ├─ F6.5 Unsichere Kompatibilität mit neuer Nutzung
│     └─ F6.6 Unsichere künftige Wartungsanforderungen
│
├─ G · Angebot, Matching & Transaktionskoordination
│  ├─ G1 Angebotssichtbarkeit           ◀ LIVE: Mengenunsicherheit
│  │  ├─ G1.1 Produkte nicht inventarisiert
│  │  ├─ G1.2 Listungen zu spät veröffentlicht
│  │  ├─ G1.3 Künftige Verfügbarkeit nicht erfasst
│  │  ├─ G1.4 Standort nicht erfasst
│  │  ├─ G1.5 Menge nicht bestätigt
│  │  └─ G1.6 Verfügbarkeitsstatus nicht aktualisiert
│  ├─ G2 Nachfragesichtbarkeit
│  │  ├─ G2.1 Projektanforderungen nicht veröffentlicht
│  │  ├─ G2.2 Benötigte Mengen nicht spezifiziert
│  │  ├─ G2.3 Maßtoleranzen nicht spezifiziert
│  │  ├─ G2.4 Technische Kriterien nicht spezifiziert
│  │  ├─ G2.5 Benötigte Termine nicht spezifiziert
│  │  └─ G2.6 Entwurfsflexibilität nicht abgebildet
│  ├─ G3 Kompatibilitäts-Mismatch
│  │  ├─ G3.1 Produkttyp-Mismatch      ├─ G3.6 Zustands-Mismatch
│  │  ├─ G3.2 Mengen-Mismatch          ├─ G3.7 Zertifizierungs-Mismatch
│  │  ├─ G3.3 Maß-Mismatch             ├─ G3.8 Standort-Mismatch
│  │  ├─ G3.4 Material-Mismatch        └─ G3.9 Preis-Mismatch
│  │  └─ G3.5 Leistungs-Mismatch
│  ├─ G4 Verfügbarkeitsunsicherheit     ◀ LIVE: Verfuegbarkeitsproblem
│  │  ├─ G4.1 Geschätzter aber unbestätigter Bestand
│  │  ├─ G4.2 Unsichere Rückgewinnungsausbeute
│  │  ├─ G4.3 Abbruchverzögerung
│  │  ├─ G4.4 Eigentumswechsel
│  │  ├─ G4.5 Projektabsage
│  │  ├─ G4.6 Beschädigung vor Rückgewinnung
│  │  ├─ G4.7 Kontamination entdeckt
│  │  └─ G4.8 Konkurrierende Reservierung
│  ├─ G5 Zeitliche Diskrepanz           ◀ LIVE: Terminunsicherheit
│  │  ├─ G5.1 Angebot vor Nachfrage verfügbar
│  │  ├─ G5.2 Angebot nach Beschaffungsfrist verfügbar
│  │  ├─ G5.3 Freigabe zu spät abgeschlossen
│  │  ├─ G5.4 Reservierungszeitraum zu kurz
│  │  └─ G5.5 Bauprogramm inkompatibel mit Rückgewinnung
│  ├─ G6 Transaktionsvertrauen
│  │  ├─ G6.1 Misstrauen gegenüber Verkäufer
│  │  ├─ G6.2 Misstrauen gegenüber Plattform
│  │  ├─ G6.3 Misstrauen gegenüber Zustandsangabe
│  │  ├─ G6.4 Misstrauen gegenüber Leistungsdaten
│  │  ├─ G6.5 Misstrauen gegenüber Zertifizierung
│  │  └─ G6.6 Misstrauen gegenüber künftiger Verfügbarkeit
│  └─ G7 Transaktionsmanagement-Grenzen
│     ├─ G7.1 Kein Reservierungsmechanismus
│     ├─ G7.2 Keine bedingte Reservierung
│     ├─ G7.3 Kein Freigabestatus
│     ├─ G7.4 Kein Substitutionsprozess
│     ├─ G7.5 Kein Eigentumsübergangs-Workflow
│     ├─ G7.6 Kein Streitbeilegungsprozess
│     └─ G7.7 Keine Erfassung fehlgeschlagener Transaktionen
│
└─ H · Physische Rückgewinnung & Ausführung
   ├─ H1 Rückgewinnbarkeit durch Konstruktion
   │  ├─ H1.1 Irreversible Klebeverbindungen
   │  ├─ H1.2 Unzugängliche Befestigungsmittel
   │  ├─ H1.3 Verbundbauteile
   │  ├─ H1.4 Verdeckte Bauteile
   │  ├─ H1.5 Zerstörende Verbindungen
   │  └─ H1.6 Nichtstandardisierte Fügungen
   ├─ H2 Demontierbarkeit
   │  ├─ H2.1 Hoher Arbeitsaufwand
   │  ├─ H2.2 Lange Demontagedauer
   │  ├─ H2.3 Spezialgerätebedarf
   │  ├─ H2.4 Eingeschränkte Baustellenzugänglichkeit
   │  ├─ H2.5 Sicherheitsrestriktionen
   │  └─ H2.6 Unvollständige Demontageanleitung
   ├─ H3 Rückgewinnungsausbeute
   │  ├─ H3.1 Beschädigung bei Ausbau
   │  ├─ H3.2 Geringere Menge als geschätzt
   │  ├─ H3.3 Kontamination
   │  ├─ H3.4 Verformung
   │  ├─ H3.5 Verdeckte Mängel
   │  └─ H3.6 Verlust ergänzender Bauteile
   ├─ H4 Prüf- & Aufbereitungskapazität  ◐ LIVE: Aufbereitungsaufwand
   │  ├─ H4.1 Unzureichende Inspektionskapazität
   │  ├─ H4.2 Unzureichende Laborkapazität
   │  ├─ H4.3 Unzureichende Prüfkapazität
   │  ├─ H4.4 Unzureichende Reinigungskapazität
   │  ├─ H4.5 Unzureichende Reparaturkapazität
   │  └─ H4.6 Unzureichende Aufarbeitungskapazität
   ├─ H5 Lagerfähigkeit                  ◀ LIVE: Witterung_Feuchte (Familie)
   │  ├─ H5.1 Keine Lagerkapazität       ◀ LIVE: Fehlende_Lagerflaeche (exaktes Blatt)
   │  ├─ H5.2 Hohe Lagerkosten
   │  ├─ H5.3 Ungeeignete Lagerbedingungen
   │  ├─ H5.4 Lange Lagerdauer
   │  ├─ H5.5 Erschwerte Bestandskontrolle
   │  └─ H5.6 Handhabungsschäden im Lager
   ├─ H6 Transport & Handhabung
   │  ├─ H6.1 Lange Transportdistanz
   │  ├─ H6.2 Hohe Transportkosten
   │  ├─ H6.3 Überdimensionierte Bauteile
   │  ├─ H6.4 Spezialtransportbedarf
   │  ├─ H6.5 Schutzverpackungsbedarf
   │  ├─ H6.6 Handhabungsschäden
   │  └─ H6.7 Erschwerte Baustellenanlieferung
   └─ H7 Einbau & Weiternutzung
      ├─ H7.1 Entwurfsanpassungsbedarf
      ├─ H7.2 Erschwerter Einbau
      ├─ H7.3 Fehlende Einbauanleitung
      ├─ H7.4 Inkompatible Schnittstellen
      ├─ H7.5 Fehlender Inbetriebnahmenachweis
      └─ H7.6 Keine Lebenszyklus-Aktualisierung nach Einbau
```

## Ohne natürlichen Treffer (nicht im Baum)
- `Ausschreibungsproblem` — kein Vergabe/Ausschreibung-Knoten.
- `Entwurfsbindung` — kein „Entwurf an Verfügbarkeit gebunden"-Knoten.
