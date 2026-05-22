# Bauteilboerse archive vs graph gap report

Date: 2026-05-28

Scope: `_archive/research/bauteilboerse/*.md` compared to live Neo4j `mit-bestand`.

Important: the archive is legacy-only. This report identifies candidates for review/import; it does not promote archive claims to truth.

## Summary

- Archive Bauteilboerse profiles checked: 39
- OK: materialhub actor exists: 5
- PARTIAL: semantic node exists, missing materialhub/platform modeling: 2
- MISSING: only source container exists: 32

All 39 files have live source/container representation as `Quelle`/`ResearchDocument`; the gap is semantic modeling as `Akteur`, `Software`, `Tool`, `Materialdepot`, country, operator, platform type, and URLs-on-facts.

## OK / already modeled as materialhub actor

| Archive profile | Live semantic match | Country/region from archive |
|---|---|---|
| BauKarussell | baukarussell (Akteur) | Österreich |
| Bauteilbörse Bremen | bauteilboerse_bremen (Akteur) | Deutschland; Bremen und Umgebung |
| Bauteilladen Winterthur | bauteilladen_winterthur (Akteur) | Schweiz; Winterthur |
| Oogstkaart / New Horizon | new_horizon (Akteur) | Niederlande |
| RotorDC | rotordc (Akteur) | Belgien; Brüssel |

## Partial semantic matches

| Archive profile | What exists | What is missing / needs review |
|---|---|---|
| Bauteilnetz Deutschland | bauteilnetz_deutschland (bauteilnetz Deutschland; Akteur) | Exists as network actor, but not typed as materialhub; decide whether to keep as network only or add Bauteilboerse/network platform role. |
| Restado | software_restado (Restado; Software) | Exists as Software only; missing operator/brand relation to Concular and materialhub/marketplace role if accepted. |

## Missing semantic platform/actor nodes

| Archive profile | Country/region | Operator from archive | Platform type from archive |
|---|---|---|---|
| Articonnex | Frankreich | Articonnex | Online-Shop / Anti-Gaspillage-Marktplatz für Bau- und Renovierungsmaterial |
| Backacia | Frankreich | Backacia | B2B-Marktplatz und Beratungs-/Begleitplattform für wiederverwendbare Baustoffe |
| Bâticycle | Frankreich; Großraum Paris / Île-de-France | Bâticycle | Shop/Plattform für second œuvre und wiederaufbereitete Materialien |
| BatiTerre | Belgien; Brüssel und Lüttich | BatiTerre | Online-Shop plus Reuse-Läden und Dienstleistungen für Demontage, Aufbereitung und Wiedereinbau |
| BatRecup | Frankreich; Ursprung Baskenland, digitale Reichweite darüber hinaus | BatRecup | Community-Plattform / App für gebrauchte Bau- und Renovierungsmaterialien |
| Building Spares Market | Vereinigtes Königreich | Building Spares Market; genaue Rechtsform nicht angegeben | kostenlose Kleinanzeigenplattform für spare and second-hand building supplies |
| Cornermat / Retrival | Belgien; Wallonie/Charleroi | Retrival / Cornermat | Online-Shop/Materialbörse für wiederverwendbare Baustoffe |
| Cycle Up | Frankreich | Cycle Up | professioneller Marktplatz für Wiederverwendung plus Beratungs-/Auditdienstleistungen |
| Cycle Zéro | Frankreich; Schwerpunkt Île-de-France laut Quellen/App-Kontext | Cycle Zéro | mobile App / Plattform zur kostenlosen Bergung von Baustellenmaterialien |
| Enviromate | Vereinigtes Königreich | Enviromate Reuse Ltd laut Website-Footer | Marketplace für leftover building materials; Kauf, Verkauf und Spende |
| Gebruiktebouwmaterialen.com / GBM | Niederlande | Gebruiktebouwmaterialen.com / GBM | Online-Shop für gebrauchte und zirkuläre Baumaterialien |
| Genbyg | Dänemark | Genbyg A/S | Webshop und Markt für gebrauchte Baumaterialien mit physischem Lager |
| Globechain | Vereinigtes Königreich; international | Globechain | ESG-Reuse-Marketplace mit interner/externer Wiederverwendung und Construction-Vertical |
| Insert Marketplace | Niederlande | Insert; genaue Betreiberstruktur nicht angegeben | Online-Marktplatz für wiederverwendbare Materialien aus Bau und öffentlichem Raum |
| Loopfront | Norwegen; Nordics und international/Europa-facing | Loopfront | digitale Reuse-Plattform mit Inventar, Material Tracking und Marketplace-Funktionen |
| Material Index | Vereinigtes Königreich | Material Index | professionelle Reuse-Plattform mit Audits, Inventar, Materialpässen, Brokerage und B2B-Marketplace |
| Material Reuse Portal | Vereinigtes Königreich; London-/UK-Fokus | CIRCuIT-/ReLondon-Kontext; konkreter laufender Betreiber nicht vollständig angegeben | Aggregator/Portal für wiederverwendbare Bau- und Abbruchmaterialien |
| Materialenbank Leuven / Atelier Circuler | Belgien; Leuven/Herent | Atelier Circuler vzw; auf Initiative und mit Unterstützung der Stadt Leuven; Zusammenarbeit mit Wonen en Werken | Materialbank mit Online-Katalog und physischem Lager |
| Materialrest24 | Deutschland / DACH | materialrest24.de; Gründung laut Medienberichten durch Simon Schlögl; aktuelle Rechtsform nicht angegeben | Online-Marktplatz für Materialreste, Restbestände und Bauartikel |
| R-Place | Frankreich; Occitanie und B2B-Reichweite | R-Place | B2B-Plattform für Wiederverwendung von Baumaterialien |
| RAEDIFICARE | Frankreich | RAEDIFICARE | Marketplace für Materialien aus Bau, öffentlichem Bauwesen und Landschaftsbau |
| re:store / HarvestMAP Vienna | Österreich; Wien | materialnomaden / HarvestMAP-Bezug laut Quellen; genaue Betreiberangaben über Impressum prüfen | Online-Store / urban-mining-orientierte Wiederverkaufsplattform mit physischer Materialbasis |
| Réempro | Frankreich; Hauts-de-France/Île-de-France und Benelux-Bezug laut Quellen | Réempro | Marketplace für Wiederverwendungsmaterialien |
| ReSource Marktplaats | Niederlande | nicht angegeben; App-Store/Google-Play-Quellen nennen die App, Betreiber nicht eindeutig im Quellenstand | App/Marktplatz für zirkuläre Baumaterialien |
| ReUse and Trade | Deutschland | nicht angegeben | digitale Reuse-Börse / Online-Listings für wiederverwendbare Produkte |
| SalvoWEB | Vereinigtes Königreich; international | Salvo | Marktplatz und Händlerverzeichnis für Architectural Salvage und reclaimed building materials |
| Salza | Schweiz; Zürich/Schweiz | Salza; genaue Rechtsform nicht angegeben | Bauteildatenbank/Plattform plus Beratung und Rückbau-/Bauteil-Sourcing |
| Skop Marketplace | Frankreich | Skop | Marketplace für Reuse- und Reconditioned-Baustoffe |
| Surplus Building & Plumbing Materials | Vereinigtes Königreich | Surplus Building & Plumbing Materials / surplusbuildingsupplies.co.uk | Marketplace für surplus building and plumbing supplies |
| Sustainability Yard | Vereinigtes Königreich | Sustainability Yard | App-/Web-Marktplatz für überschüssige, reclaimed und nachhaltige Baumaterialien |
| useagain / Bauteilclick | Schweiz | useagain; genaue Rechtsform nicht angegeben | digitale Vermittlungs- und Austauschplattform für gebrauchte Bauteile, Materialien und Möbel |
| Warp It | Vereinigtes Königreich; Organisationsnetzwerke auch darüber hinaus | Warp It | Ressourcen-Redistribution-Netzwerk / Organisationsplattform |

## Recommended next graph work

1. Promote only reviewed profiles into semantic nodes. Do not import from `_archive/research/bauteilboerse/` blindly.
2. For each accepted profile, create/update an `Akteur` for the operator or organization and a `Software`/`Tool`/`Materialdepot` node for the platform where those are distinct.
3. Attach country via `GEHÖRT_ZU`/`LIEGT_IN_LAND`, actor type `at_materialhub_bauteilboerse` where semantically correct, and platform/source URLs directly on fact relationships per Q-EXT v6 logic.
4. Prioritize partials first: Bauteilnetz Deutschland and Restado, because they already have semantic nodes.
