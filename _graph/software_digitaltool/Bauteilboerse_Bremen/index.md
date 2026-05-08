---
id: "Bauteilboerse_Bremen"
entity: "software_digitaltool"
node_kind: "core"
migration_status: "migrated_phase3_core_entities"
title: "Bauteilbörse Bremen"
source_count: 2
legacy_paths:
  - "akteur\\06_bauteilboersen_marktplaetze_handel\\Bauteilboerse_Bremen.md"
  - "bauteilboerse\\bauteilboerse-bremen.md"
raw_targets:
  - "software_digitaltool/Bauteilboerse_Bremen"
migration_actions:
  - "semantic_split"
  - "split_platform_profile"
risk_flags:
  - "duplicate_with_akteur_or_werkzeug"
  - "market_actor_platform_overlap;check_against_bauteilboerse_and_werkzeug_duplicates"
---
# Bauteilbörse Bremen

## Migration

- Canonical target: software_digitaltool/Bauteilboerse_Bremen
- Legacy source count: 2
- Semantic note: Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet.

## Legacy Content

### Legacy Source: bauteilboerse\bauteilboerse-bremen.md

- Map action: split_platform_profile
- Target role in map: primary
- Raw mapped target: software_digitaltool/bauteilboerse_bremen
- Original primary target: software_digitaltool/bauteilboerse_bremen
- Original secondary targets: akteur/<operator_if_named>; beschaffungsweg/Digitale_Plattform; ressourcenquelle/Bauteilboerse; plattformfunktion/Material_Matching

---
type: Bauteilbörse
---

# Bauteilbörse Bremen

## Kurzbeschreibung
Bauteilbörse Bremen ist ein(e) regionale Bauteilbörse mit physischem Lager und Online-Katalog mit Bezug zu Deutschland; Bremen und Umgebung. Im Reuse-Kontext liegt der Schwerpunkt auf: Bergung, Ausbau, Transport, Lagerung, Registrierung und Verkauf gebrauchter Bauteile aus Abbruch oder Umbau.

## Land / Region
Deutschland; Bremen und Umgebung

## Betreiber
bauteilbörse bremen; Kooperationsbezug zur Bremer Stadtreinigung; genaue Rechtsform auf den verwendeten Quellen nicht durchgängig angegeben

## Zielgruppe
Privatpersonen, Handwerk, Planende, Denkmalpflege, Sanierung, Upcycling-Projekte

## Plattformtyp
regionale Bauteilbörse mit physischem Lager und Online-Katalog

## Bauteilkategorien
Fenster, Türen, Hof/Garten, Böden/Treppen, Wände/Innenraum, Sanitär, Elektro/Leuchten, Beschläge, Heizkörper, Handläufe, historische und moderne Einzelstücke

## Art der Wiederverwendung
Bergung, Ausbau, Transport, Lagerung, Registrierung und Verkauf gebrauchter Bauteile aus Abbruch oder Umbau

## Funktionen
Online-Katalog und Suche; Beratung; Annahmeprüfung per Fotos; Ausbau/Abtransport bei passenden Bauteilen; Verkauf vor Ort

## Daten je Bauteil
Katalogeinträge enthalten mindestens Artikelnummer, Preis, Kategorie, Fotos und häufig Maße/Material/Eigenschaften; genaue Detailtiefe variiert

## Qualität / Prüfung
funktionstüchtige Bauteile werden ausgewählt; Elektroartikel werden laut Quelle nicht als geprüfte Elektrogeräte verkauft und sollten professionell geprüft werden

## Logistik / Lagerung
physisches Lager in Bremen; Ausbau, Abtransport und Lagerung durch die Börse nach Eignungsprüfung; Abholung vor Ort üblich

## Geschäftsmodell
Verkauf gebrauchter Bauteile; konkrete Gebühren/Provisionen nicht angegeben

## Ökologische Bewertung
Verringert Bauabfall und spart Rohstoffe und Energie, die bei Neuproduktion anfallen würden; quantitative Ökobilanz je Bauteil nicht angegeben

## Stärken
sehr praxisnah; großes regionales Lager; Online-Bestand; Beratung und Ausbaukompetenz

## Schwächen / Hemmnisse
regional begrenzt; Verfügbarkeit stark abhängig von Abbruch-/Umbauprojekten; technische Normnachweise je Bauteil prüfen

## Relevanz für zirkuläres Bauen
hoch für zirkuläres Bauen im Bestand, insbesondere bei Sanierung, Denkmalpflege und Ersatzteilen.

## Quellen und Links
- https://www.bauteilboerse-bremen.de/start
- https://www.bauteilboerse-bremen.de/katalog
- https://www.bauteilboerse-bremen.de/katalog/suche
- https://www.bauteilboerse-bremen.de/die-idee
- https://www.bauteilboerse-bremen.de/katalog/tueren

---
Hinweis: Verfügbarkeit, Zustand, Maße, Normen- und Brandschutzanforderungen müssen vor Spezifikation oder Kauf direkt mit Anbieter/Betreiber geprüft werden.

### Legacy Source: akteur\06_bauteilboersen_marktplaetze_handel\Bauteilboerse_Bremen.md

- Map action: semantic_split
- Target role in map: secondary
- Raw mapped target: software_digitaltool/Bauteilboerse_Bremen
- Original primary target: akteur/Bauteilboerse_Bremen
- Original secondary targets: software_digitaltool/Bauteilboerse_Bremen; tooltyp/Bauteilboerse; beschaffungsweg/Bauteilboerse; ressourcenquelle/Bauteilboerse

## Verknüpfungen

**Übergeordnete Themen**
- Bauteilbergung und Wiederverkauf
- regionale Lager- und Beratungsinfrastruktur
- praktische Erfahrung mit gebrauchten Bauteilen

**Verwandte Dateien**
- `akteur/Bauteilnetz_Deutschland.md`
- `werkzeug/Bauteilboerse.md`
- `methode/Selektiver_Rueckbau.md`
- `methode/Bauteilernte.md`
- `material/Historische_Bauteile.md`

**Akteurstyp**
- Regionale physische Bauteilbörse

## Kurzüberblick zur Kategorie

**Bauteilbörse Bremen** ist im Kontext „Entwerfen mit Bestand“ / Wiederverwendung in der Architektur ein Regionale physische Bauteilbörse. Die Bauteilbörse Bremen ist eine regionale Infrastruktur für gebrauchte Bauteile. Sie steht exemplarisch für physische Bauteilbörsen in Deutschland, die Bauteile aus Rückbau, Umbau oder Sanierung sichern und für neue Nutzungen anbieten.

Für das Repo ist dieser Akteur besonders wichtig, weil die Wiederverwendung von Bauteilen nicht nur durch einzelne Produkte entsteht, sondern durch ein Zusammenspiel aus politischem Rahmen, Planungskultur, Daten, Materiallogistik, Rückbau, Qualitätssicherung und Nachfrage. Die Datei ist als Akteursprofil zu lesen: Sie beschreibt Rolle, Nutzen, Grenzen und sinnvolle Querverbindungen, ersetzt aber keine projektspezifische Prüfung von Recht, Technik, Schadstoffen, Kosten oder Verfügbarkeit.

## Zentrale Unterthemen

- Türen, Fenster, Treppen, Geländer, Sanitärkeramik, Ziegel und Beschläge
- Annahme und Verkauf gebrauchter Bauteile
- Beratung zu Ausbau und Wiedereinbau
- regionale Nachfrage und kurze Wege
- Grenzen bei bauaufsichtlich relevanten Produkten

## Wichtige Dateien dieser Kategorie mit je 1–3 Sätzen Einordnung

- methode/Selektiver_Rueckbau.md — beschreibt den schonenden Ausbau als Voraussetzung für die Börse.
- material/Historische_Bauteile.md — sammelt wertvolle robuste und gestalterisch gefragte Produktgruppen.
- wirtschaft/Lagerkosten.md — erklärt die Geschäftsmodell-Hürde physischer Börsen.

Weitere Anschlussdateien sollten den Akteur nicht nur erwähnen, sondern prüfen, welche konkrete Funktion er im ReUse-Prozess übernimmt: politischer Druck, technische Bewertung, Marktplatz, physisches Lager, Planungskompetenz, Forschung, Zertifizierung oder kommunale Infrastruktur.

## Relevanz für Wiederverwendung / Entwerfen mit Bestand

- Ermöglicht reale Inspektion, Lagerung und Abholung von Bauteilen.
- Ist besonders geeignet für robuste, sichtbare, historische oder gut demontierbare Bauteile.
- Liefert praktische Hinweise zu Nachfrage, Preisen, Lagerproblemen und Produktgruppen.

Die Einordnung ist bewusst nicht auf „Bauteile kaufen“ reduziert. Gerade in Deutschland entstehen ReUse-Potenziale häufig vor dem eigentlichen Materialhandel: durch Erhaltungsentscheidungen, frühe Zielvereinbarungen, selektiven Rückbau, Gebäuderessourcenpässe, kommunale Beschaffung, lokale Materialorte und eine Planungskultur, die mit Verfügbarkeit, Patina und Unregelmäßigkeit umgehen kann.

## Querverbindungen zu anderen Kategorien

- Zu Bauteilnetz Deutschland: Bremen ist ein konkreter Standort innerhalb der deutschen Bauteilbörsenlogik.
- Zu restado: Bremen steht für physische Lagerlogik, restado für Online-Vermittlung.
- Zu Denkmalpflege: historische Bauteile können kulturell und handwerklich besonders wertvoll sein.

Für die Arbeit im Repo sollte der Akteur mit Methoden-, Werkzeug-, Material-, Rechts- und Wirtschaftlichkeitsdateien verknüpft werden. Besonders wichtig ist die Unterscheidung zwischen:
- **Diskurs / Policy**: schafft Legitimation und politische Forderungen.
- **Daten / Bewertung**: macht Ressourcen sichtbar und vergleichbar.
- **Markt / Logistik**: bringt Angebot und Nachfrage zusammen.
- **Planung / Entwurf**: integriert verfügbare Bauteile in Räume, Tragwerke und Details.
- **Nachweis / Recht**: entscheidet, ob ein Bauteil genehmigungs- und haftungsfähig wiederverwendet werden kann.

## Offene Lücken / Ausbaufelder

- Bauteile sind oft Einzelstücke; größere Projekte brauchen Mengen und Planungssicherheit.
- Qualität, Herkunft, Schadstofffreiheit und Zulassung sind nicht immer vollständig dokumentiert.
- Neuware ist häufig billiger, schneller verfügbar und normativ einfacher.

Zusätzlich sollte bei jeder späteren Vertiefung geprüft werden, ob die Angaben auf offiziellen Quellen, unabhängigen Evaluationen, Projektpublikationen oder Eigenkommunikation beruhen. Eigenangaben von Plattformen, Büros und Herstellern sind nützlich, müssen aber bei CO₂-Einsparungen, Wiederverwendungsquoten, Preisen und Skalierbarkeit kritisch markiert werden.

## Quellen / Bezugslogik

- https://www.bauteilboerse-bremen.de/
- https://www.bauteilnetz.de/
- https://www.ressource-deutschland.de/themen/bauwesen/kreislaufgerechtes-bauen/
- https://www.umweltbundesamt.de/themen/abfall-ressourcen/abfallwirtschaft/abfallarten/bauabfaelle
