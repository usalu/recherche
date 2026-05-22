# BAUTEILBÖRSEN RESEARCH — Interface-Archetypen und Datenmuster

**Stand:** 2026-06-04

**Zweck:** finale, bereinigte Bauteilbörsen-Recherche mit Fokus auf Interface-Archetypen, Datenqualität und vergleichbare Screenshot-Erfassung. Diese Fassung priorisiert die Frage: *Welche Art von Interface macht konkrete Bauteile beschaffbar, und welche Daten müssen je Plattform wirklich erfasst werden?*

**Kernregel:** Jede Plattform wird über konkrete Angebotslogik gelesen, nicht über Selbstbeschreibung oder Organisationsrolle. Zentrale Bewertungseinheit ist deshalb nicht die Homepage, sondern die Kombination aus Suche/Kategorie, Listingkarte, Detailseite, Standort-/Logistikinformation und Transaktionsweg.

## 1. Executive Summary

- Der bereinigte Korpus enthält **51 Bauteilbörsen-relevante Plattformen und Angebotskanäle**.
- Die Recherche wird auf **fünf minimale Interface-Archetypen** reduziert: Depot-Shop, Marketplace, Project/Harvest Catalogue, Brokered Catalogue und External/App Channel.
- Die wichtigste Datenerkenntnis: Gute Bauteilbörsen verbinden mindestens **Bauteilkategorie + Maße/Menge + Standort + Zustand + Transaktionsweg**. Für professionelle Wiederverwendung kommen **Herkunft/Projekt + Verfügbarkeit + Nachweis/Prüfung** dazu.
- Ein Produktbild allein ist kein Beschaffungsbeweis. Ein Angebot ist erst vergleichbar, wenn ersichtlich ist, *was* es ist, *wie viel* vorhanden ist, *wo* es liegt, *in welchem Zustand* es ist und *wie* man es bekommt.
- Große/tragende Elemente tauchen am ehesten in Projekt-/Harvest-Katalogen, B2B-Marktplätzen oder spezialisierten Chargen auf; kleine Ausbau-/Sanitär-/Möbel-/Oberflächenbauteile passen besser in Depot-Shop- und Marketplace-Karten.
- Diese Fassung vermeidet Inventar-Prozentwerte. Kategorien und Mengen gelten nur als screenshotfähige Momentaufnahme, nicht als dauerhafte Statistik.

### 1.1 Minimaler Archetypen-Split

| Archetyp | Anzahl | Kurzinterpretation |
| --- | ---: | --- |
| Depot-Shop | 11 | Ein Betreiber kontrolliert Bestand oder Laden/Depot. Die Oberfläche zeigt Sortiment, Produktkarten, Shop-/Reservierungs- oder Kontaktlogik. |
| Marketplace | 21 | Mehrere Anbieter oder Verkäufer stellen Angebote ein. Die Plattform normalisiert Suche, Kategorie, Ort und Kontakt/Transaktion. |
| Project/Harvest Catalogue | 9 | Bauteile sind an Rückbau, Quellgebäude, Ressourcendossier, Projektort oder Zeitfenster gekoppelt. |
| Brokered Catalogue | 6 | Konkrete Bauteile oder Materiallisten sind sichtbar, aber die Beschaffung läuft über Kontakt, Vermittlung, Besuch oder individuelle Anfrage. |
| External/App Channel | 4 | Die Website ist nur Einstieg; echte Angebotsdaten liegen in App, App-Store, Ricardo oder anderem externen Kanal. |

### 1.2 Datenreife-Split

| Datenreife | Anzahl | Bedeutung |
| --- | ---: | --- |
| 3 | 19 | 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren. |
| 2 | 25 | 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden. |
| 1 | 7 | 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten. |

## 2. Fünf Interface-Archetypen

Diese fünf Kategorien sind absichtlich minimal. Sie reichen aus, um alle 51 Plattformen sauber einzuordnen, ohne die Recherche wieder mit Software-, Verzeichnis-, Beratungs- oder Materialpasslogiken zu vermischen.

| Archetyp | Interface-Signale | Typische Datenstärke | Primäres Risiko | Beispiele |
| --- | --- | --- | --- | --- |
| **Depot-Shop** | Kategorien, Produktkarten, Preis/Anfrage, Laden/Depot, Abholung, teils Warenkorb. | Produkt- und Lagerdaten sind vergleichsweise konsistent; Herkunft und technische Nachweise fehlen oft. | Website ist oft nur eine Auswahl des realen Lagers; kein Inventaranteil ohne Zählung. | BatiTerre, Cornermat / Retrival, Bauteilbörse Bremen, Genbyg, Articonnex, Gebruiktebouwmaterialen, Bauteilbörse Basel |
| **Marketplace** | Suche, Filter, Verkäuferprofil, Standort/Radius, Listingkarte, Kontakt/Checkout. | Ort, Verkäufer, Menge und Transaktionsweg sind zentral; Datenqualität schwankt je Anbieter. | Einzelne Listings dürfen nicht als Plattforminventar gelesen werden. | Materialrest24, Restado, Backacia, Bâticycle, Cycle Up, R-Place, Réempro |
| **Project/Harvest Catalogue** | Projekt-/Quellseite, Chargen, Verfügbarkeit ab/bis, Anfrage/Interesse, teils professionelle Klassifikation. | Herkunft und Zeit sind wichtiger als Warenkorb; große Bauteile sind hier am ehesten sichtbar. | Zeitfenster und Projektstatus können schnell veralten. | RotorDC, Concular Shop, RAEDIFICARE, REFAIR Bordeaux, Archipel Sion Ressourcerie, Matériuum Genève Ressourcerie, Ressourcerie Lausanne / Matériuum / R-UUL |
| **Brokered Catalogue** | Angebotsliste, Materialkarte, Kontaktweg, regionale/lokale Logik, oft wenig Automatisierung. | Beschaffbarkeit ist plausibel, muss aber über Kontakt-/Detailfelder bewiesen werden. | Nicht mit Shop oder vollständiger Inventardatenbank verwechseln. | Materialenbank Leuven / Atelier Circuler, bauteilnetz Deutschland, Bauteilvermittlung Zürichsee-Oberland, Bauteilverwertung Köppel & Klein, La Ressourcerie Fribourg, Stiftung Chance BauTeile Zürich / Glattbrugg |
| **External/App Channel** | CTA zur App oder externer Shop/Profil; echte Listingebene außerhalb der Hauptseite. | Nur ein externes oder App-Listing zählt als Angebotsbeweis. | Landingpage ist kein Inventarnachweis. | BatRecup, Cycle Zéro, ReSource Marktplaats, Wick ReUse / ROTO Baumarkt |

## 3. Datenmodell: was wirklich erfasst werden muss

Das Datenmodell ist kompakt gehalten. Für jedes Screenshot-Set sollen dieselben acht Datenblöcke geprüft werden. Fehlende Felder werden als fehlend dokumentiert, nicht geschätzt.

| Datenblock | Pflichtfrage | Minimaler Nachweis | Warum wichtig |
| --- | --- | --- | --- |
| 1. Identität | Welches konkrete Angebot wird belegt? | Plattform, URL, Datum, Titel, Listing-/Artikel-ID falls vorhanden | verhindert spätere Verwechslung dynamischer Angebote |
| 2. Bauteilkategorie | Welche Art Bauteil ist es? | Kategoriepfad oder Suchbegriff, Bauteilfamilie | macht Plattformen vergleichbar |
| 3. Technische Daten | Passt das Bauteil technisch? | Maße, Menge, Einheit, Material, Marke/Modell falls relevant | zentral für Wiederverwendung |
| 4. Zustand | Kann man dem Angebot vertrauen? | Zustand, sichtbare Schäden, geprüft/gereinigt/garantiert falls sichtbar | trennt brauchbare Bauteile von nur schönen Bildern |
| 5. Standort/Logistik | Wo liegt es und wie kommt man daran? | Depot, Verkäuferort, PLZ/Radius, Projektort, Lieferung/Abholung, Gewicht falls sichtbar | entscheidet über reale Beschaffbarkeit |
| 6. Zeit/Verfügbarkeit | Ist es jetzt oder nur in einem Projektfenster verfügbar? | verfügbar/reserviert/verkauft, verfügbar ab/bis, Deadline, Listingdatum | besonders wichtig bei Rückbau und Projektchargen |
| 7. Transaktion | Was kann der Nutzer tun? | Kaufen, reservieren, anfragen, merken, chatten, App öffnen, extern kaufen | unterscheidet Shop, Marktplatz, Vermittlung und Projektkoordination |
| 8. Herkunft/Nachweis | Woher stammt das Bauteil und gibt es Belege? | Quelle/Projekt/Verkäufer, CO₂/Abfall, Attestation, Prüf-/Gewährleistungshinweis | wichtig für B2B, Ausschreibung und tragende/technische Bauteile |

### 3.1 Datenfelder nach Archetyp

| Archetyp | Must-have Felder | Nice-to-have Felder | Wichtigster Screenshot |
| --- | --- | --- | --- |
| Depot-Shop | Kategorie, Produktkarte, Maße, Preis/Anfrage, Zustand, Depot/Abholung | Lagerort, Artikelnummer, Gewicht, Warenkorb, Öffnungszeiten | Detailseite eines konkreten Artikels plus Depotbezug |
| Marketplace | Verkäufer, Ort/Radius, Kategorie, Menge, Preis/Anfrage, Kontakt/Checkout | Verkäuferprofil, Listingdatum, Bewertung, Lieferoption | Such-/Filteransicht plus Listing mit Verkäufer/Ort |
| Project/Harvest Catalogue | Projekt/Quelle, Bauteil/Charge, Menge, Verfügbarkeit, Anfrage/Interesse | Ressourcendossier, Nachweis, Demontagefenster, CO₂ | Projekt-/Quellseite plus konkrete Ressource |
| Brokered Catalogue | Angebotsliste, Kontaktweg, Ort, Kategorie, Maße/Menge falls sichtbar | Besichtigung, Reservierung, Zustandsnotiz, Vermittlungsregeln | konkrete Angebotskarte plus Kontakt-/Abholprozess |
| External/App Channel | externer Kanal, echtes Listing, Ort, Aktion | App-Screens, Verkäuferprofil, Aktualität | Hauptseite plus App-/externes Listing, nicht nur Landingpage |

## 4. Gesamtkorpus: klare Zuordnung aller 51 Plattformen

| # | Plattform | Land/Region | Interface-Archetyp | Datenprofil | Datenreife | Wichtigster Datenbeweis |
| ---: | --- | --- | --- | --- | ---: | --- |
| 1 | BatiTerre | Belgien | **Depot-Shop** | Produktkarte + Standortkategorie | 3 | Shop-Kategorie, Produktkarte, Detailseite mit Preis/Maß/Standort |
| 2 | Cornermat / Retrival | Belgien | **Depot-Shop** | Produktkarte + Materialfilter + Depot | 3 | Kategoriebaum, Par MATIÈRE, Standortblock, Detailseite |
| 3 | Materialenbank Leuven / Atelier Circuler | Belgien | **Brokered Catalogue** | Katalogkarte + Kontaktlogik | 2 | Katalogübersicht, konkrete Karte, Kontakt-/Abholhinweis |
| 4 | RotorDC | Belgien | **Project/Harvest Catalogue** | Produktkarte + Per-Building-Quelle | 3 | Per-Building-Menü, Listing, Detail mit Herkunft |
| 5 | Bauteilbörse Bremen | Deutschland | **Depot-Shop** | Katalogkarte + Lagerort | 3 | Kategorie-/Filterseite und Detailseite mit Lagerort/Artikeldaten |
| 6 | bauteilnetz Deutschland | Deutschland | **Brokered Catalogue** | Verbundkatalog + Anbieter | 2 | Such-/Katalogseite, Anbieterhinweis, Detailangebot |
| 7 | Concular Shop | Deutschland | **Project/Harvest Catalogue** | Projektlisting + KG/Kategorie + B2B-Daten | 3 | Projektseite, Filter/KG, Listing mit Verfügbarkeits-/B2B-Hinweis |
| 8 | Materialrest24 | Deutschland | **Marketplace** | Seller listing + Restposten | 2 | Suchseite, Listingkarte, Anbieter-/Standorthinweis |
| 9 | Restado | Deutschland | **Marketplace** | Seller listing + Stadt/Kategorie + Restposten/Rückbau | 3 | Kategorie- oder Stadt-Suche, Listing, Verkäufer-/Abholinfo |
| 10 | Genbyg | Dänemark | **Depot-Shop** | Produktkarte + Bestand + Quelle-Story | 3 | Mega-Menü, Produktkarte, Detailseite, Quelle-Story falls vorhanden |
| 11 | Articonnex | Frankreich | **Depot-Shop** | Shopkollektion + Reuse-Hinweis | 2 | Collection-Seite, Produktkarte, Detail mit Abholung/Status |
| 12 | Backacia | Frankreich | **Marketplace** | Professional listing + availability window | 2 | Such-/Kategorieansicht, Listing mit Stadt/Menge/Datum |
| 13 | BatRecup | Frankreich | **External/App Channel** | App-/Marktplatzkanal | 1 | Landingpage + echtes App/Marketplace-Listing |
| 14 | Bâticycle | Frankreich | **Marketplace** | Seller/profile listing within Skop | 2 | Profilseite und mindestens ein konkretes Listing |
| 15 | Cycle Up | Frankreich | **Marketplace** | Marketplace + diagnostic/reconditioning context | 3 | Marketplace-Einstieg, Listing, Herkunft/Nachweisfeld |
| 16 | Cycle Zéro | Frankreich | **External/App Channel** | App-first local listing | 1 | Website-Einstieg + App-Screen mit konkretem Angebot |
| 17 | R-Place | Frankreich | **Marketplace** | B2B listing | 2 | Marketplace-Suche, Listingkarte, Detailseite |
| 18 | RAEDIFICARE | Frankreich | **Project/Harvest Catalogue** | B2B procurement + lot/specification | 2 | Marketplace/Buyer-Interface, Filter, Anfrage-/Bedarfsfunktion |
| 19 | REFAIR Bordeaux | Frankreich | **Project/Harvest Catalogue** | Resource dossier + interest list | 2 | Ressourcendossier, Materialkarte, List-/Interessensfunktion |
| 20 | Réempro | Frankreich | **Marketplace** | Professional listing | 2 | Marketplace-Übersicht, Listing, Verkäufer-/Kontaktfeld |
| 21 | Skop Marketplace | Frankreich | **Marketplace** | Seller listing + around-me/all-France | 3 | Suchseite mit Standorttoggle, Listing, Verkäuferprofil |
| 22 | Gebruiktebouwmaterialen | Niederlande | **Depot-Shop** | Assortment catalogue | 2 | Assortiment, Produktkarte, Kontakt-/Abholhinweis |
| 23 | Insert Marketplace | Niederlande | **Marketplace** | Reuse marketplace listing | 2 | Marktplatzseite, Such-/Filteransicht, Detaillisting |
| 24 | ReSource Marktplaats | Niederlande | **External/App Channel** | App-store/app listing | 1 | App-Store-Seite + In-App-Angebot |
| 25 | Archipel Sion Ressourcerie | Schweiz | **Project/Harvest Catalogue** | Resource inventory + project/location context | 2 | Inventarseite, Objektkarte, Detail/Kontakt |
| 26 | Baumatpool.ch | Schweiz | **Marketplace** | Seller listing + category/location | 2 | Suche/Filter, Listingkarte, Anbieter/Ort |
| 27 | Bauteilbörse Basel | Schweiz | **Depot-Shop** | Regional depot catalogue | 2 | Bauteile-Übersicht, Produktdetail, Standort/Öffnungszeiten |
| 28 | Bauteilladen Winterthur | Schweiz | **Depot-Shop** | Shop catalogue | 2 | Shopkategorie, Produktkarte, Detailseite |
| 29 | Bauteilvermittlung Zürichsee-Oberland | Schweiz | **Brokered Catalogue** | Offer list + mediation | 2 | Angebotsliste, Detailangebot, Kontakt-/Vermittlungshinweis |
| 30 | Bauteilverwertung Köppel & Klein | Schweiz | **Brokered Catalogue** | Sales list/page + contact | 2 | Verkaufsseite, einzelnes Angebot, Abholung/Kontakt |
| 31 | GGZ@WORK Laden 2 Bauteile Zug | Schweiz | **Depot-Shop** | Physical store visibility | 2 | Ladenseite + konkreter Angebots-/Sortimentsbeleg |
| 32 | Gruner ReUse | Schweiz | **Marketplace** | Structured product platform + technical fields | 2 | Produktübersicht, Filter, Detail mit Spezifikationen |
| 33 | La Ressourcerie Fribourg | Schweiz | **Brokered Catalogue** | Selective materials catalogue | 2 | Materialienseite, konkrete Materialkarte, Kontaktweg |
| 34 | Matériuum | Schweiz | **Depot-Shop** | Shop + classification/category | 3 | Boutique-Filter, Produktkarte, Detailseite |
| 35 | Matériuum Genève Ressourcerie | Schweiz | **Project/Harvest Catalogue** | Project/channel within Matériuum | 1 | Projekt-/Genève-Hinweis + konkretes Ressourcerie-Angebot |
| 36 | Ressourcerie Lausanne / Matériuum / R-UUL | Schweiz | **Project/Harvest Catalogue** | Project/channel within Matériuum/R-UUL | 1 | Lausanne/R-UUL-Kontext + konkretes Angebot |
| 37 | ReUse Recycling Center Riedtwil / wiederverwendung.ch | Schweiz | **Depot-Shop** | Shop category + used components | 2 | Kategorie gebrauchte Bauteile, Produktkarte, Detailseite |
| 38 | REUZI | Schweiz | **Marketplace** | Agora listing + project/seller context | 2 | Agora-Übersicht, Angebot, Anbieter/Ort |
| 39 | Salza | Schweiz | **Marketplace** | Search/radius + admin-reviewed listing + chat/handover | 3 | Suche/Radius, Angebotsworkflow, Listing/Chat-/Übergabehinweis |
| 40 | Stiftung Chance BauTeile Zürich / Glattbrugg | Schweiz | **Brokered Catalogue** | Physical social-enterprise offer + contact | 1 | Dienstleistungsseite + konkreter Verkaufs-/Sortimentsnachweis |
| 41 | useagain / Bauteilclick | Schweiz | **Marketplace** | Listing + PLZ/Umkreis + delivery mode | 3 | Kaufen-Seite mit Radiusfilter, Listing, Detailseite |
| 42 | Wick ReUse / ROTO Baumarkt | Schweiz | **External/App Channel** | External shop/channel listing | 1 | ROTO/Wick-Kontext + Ricardo-Angebot |
| 43 | Building Spares Market | Vereinigtes Königreich | **Marketplace** | Classified listing + category/location | 2 | Kategorieansicht, Anzeige, Kontakt/Ort |
| 44 | Enviromate | Vereinigtes Königreich | **Marketplace** | Classified listing + distance radius | 3 | Marketplace-Suche mit Radius, Listingkarte, Detailseite |
| 45 | Globechain | Vereinigtes Königreich | **Marketplace** | Business marketplace listing | 2 | Construction-Kategorie, Listing, Anbieter/Logistik |
| 46 | Material Index | Vereinigtes Königreich | **Marketplace** | Marketplace + audit/brokerage overlay | 3 | Marketplace-Einstieg, Listing, Daten-/Brokeragehinweis |
| 47 | SalvoWEB | Vereinigtes Königreich | **Marketplace** | Salvage search + dealer/profile hybrid | 3 | Search nach area/category, Listing, Dealerprofil |
| 48 | Surplus Building & Plumbing Materials | Vereinigtes Königreich | **Marketplace** | E-commerce listing + collect-from-postcode | 3 | Produktliste, collect-from-Hinweis, Detail/Checkoutdaten |
| 49 | Sustainability Yard | Vereinigtes Königreich | **Marketplace** | Seller listing + modern marketplace UX | 3 | Homepage/Marketplace, Listing, Verkäufer-/Standorthinweis |
| 50 | BauKarussell | Österreich | **Project/Harvest Catalogue** | Project/resource catalogue | 3 | Katalogstart, Projekt/Ressource, Interessen-/Kontaktweg |
| 51 | re:Laden / HarvestMAP Vienna | Österreich | **Project/Harvest Catalogue** | List/map + project/source listing | 3 | Liste/Karte-Toggle, Filter, Projekt-/Quelleintrag |

## 5. Länder- und Archetypenmatrix

| Land/Region | Depot-Shop | Marketplace | Project/Harvest Catalogue | Brokered Catalogue | External/App Channel | Gesamt |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Belgien | 2 | 0 | 1 | 1 | 0 | 4 |
| Deutschland | 1 | 2 | 1 | 1 | 0 | 5 |
| Dänemark | 1 | 0 | 0 | 0 | 0 | 1 |
| Frankreich | 1 | 6 | 2 | 0 | 2 | 11 |
| Niederlande | 1 | 1 | 0 | 0 | 1 | 3 |
| Schweiz | 5 | 5 | 3 | 4 | 1 | 18 |
| Vereinigtes Königreich | 0 | 7 | 0 | 0 | 0 | 7 |
| Österreich | 0 | 0 | 2 | 0 | 0 | 2 |
| **Gesamt** | 11 | 21 | 9 | 6 | 4 | 51 |

## 6. Muster aus allen Plattformen

### 6.1 Der stärkste Unterschied ist nicht Shop vs. kein Shop

Die entscheidende Trennung verläuft zwischen **bestandskontrollierten Oberflächen** und **angebotsvermittelnden Oberflächen**. Depot-Shops können konsistente Produktdaten zeigen, weil ein Betreiber Lager, Foto, Preis und Abholung kontrolliert. Marketplaces skalieren besser, aber ihre Datenqualität hängt am Verkäufer. Project/Harvest-Kataloge sind für große Bauteile stärker, weil Herkunft und Zeitfenster sichtbar werden. Brokered Catalogues sind lokal oft relevant, aber brauchen mehr manuelle Erfassung. External/App Channels sind erst nutzbar, wenn das tatsächliche externe Listing dokumentiert ist.

### 6.2 Die fünf wiederkehrenden Datenmuster

| Datenmuster | Wo es dominiert | Was es gut zeigt | Was häufig fehlt |
| --- | --- | --- | --- |
| **Produktkarte** | Depot-Shops | Bild, Titel, Kategorie, Preis, Maße, Warenkorb/Kontakt | Herkunft, Prüfung, vollständiger Lagerbestand |
| **Seller Listing** | Marketplaces | Verkäufer, Standort, Menge, Preis, Kontakt, Radius | konsistente technische Daten und Zustandsprüfung |
| **Projekt-/Quellkarte** | Project/Harvest | Herkunft, Chargen, Zeitfenster, Rückbaukontext | schneller generischer Produktvergleich |
| **Kontakt-/Vermittlungskarte** | Brokered Catalogues | lokale Beschaffbarkeit, menschliche Vermittlung | Checkout, Standardschema, Aktualität |
| **Externer/App-Beleg** | External/App Channels | echte Angebote außerhalb der Website | öffentlich zitierbare Webdaten ohne App-/Kanalprüfung |

### 6.3 Welche Datenfelder am häufigsten entscheidend sind

1. **Standort ist wichtiger als Land.** Ein nationaler Marktplatz hilft nur, wenn das konkrete Listing Ort, PLZ, Radius, Abholung oder Lieferung zeigt.
2. **Menge und Einheit entscheiden über Projektfähigkeit.** Stück, Set, m², Laufmeter, Palette oder Charge müssen sichtbar sein.
3. **Maße sind Pflicht bei Türen, Fenstern, Platten, Böden, Trägern und Küchen.** Ohne Maße ist ein Angebot nur Inspiration.
4. **Zustand muss als Feld, Text oder Detailfoto belegbar sein.** Besonders Sanitär, Elektro, HVAC und Oberflächen brauchen Zustands-/Prüfhinweise.
5. **Herkunft ist das Unterscheidungsmerkmal guter Reuse-Interfaces.** Project/Harvest-Kataloge und einige Shops zeigen Quelle/Per Building/Projekt; normale Marketplaces oft nicht.
6. **Transaktionsweg muss sichtbar sein.** Kaufen, Anfrage, Reservierung, Merkliste, Chat, App oder externer Kauf sind unterschiedliche Interface-Logiken.

### 6.4 Minimaler Vergleichssatz für spätere Screenshots

Für eine schlanke, aber vollständige Screenshot-Reihe sollten je Archetyp mindestens diese Plattformen aufgenommen werden:

| Archetyp | Prioritätsbeispiele | Warum |
| --- | --- | --- |
| Depot-Shop | Cornermat, Genbyg, Bauteilbörse Bremen, Matériuum | Produktdaten, Kategorien, Abholung, Maße/Preis vergleichbar |
| Marketplace | useagain, Salza, Skop, Enviromate, Restado | Verkäufer/Ort/Radius/Suche und Listingqualität sichtbar |
| Project/Harvest Catalogue | Concular, RotorDC, BauKarussell, re:Laden, REFAIR | Herkunft, Projekt, Zeitfenster und Chargenlogik |
| Brokered Catalogue | Materialenbank Leuven, Bauteilvermittlung Zürichsee-Oberland, La Ressourcerie Fribourg | zeigt kontaktbasierte Bauteilvermittlung |
| External/App Channel | Cycle Zéro, BatRecup, ReSource Marktplaats, Wick ReUse/ROTO | zeigt, wie externe Kanäle korrekt belegt werden müssen |

## 7. Platform-by-platform Interface/Data Cards

### Belgien

#### 1. BatiTerre
- **Link:** https://www.batiterre.be/shop
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Produktkarte + Standortkategorie
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** kontrollierter Lagerbestand wird wie ein Shop vorselektierbar.
- **Zu erfassende Kernfelder:** Kategorie, Maße, Preis, Warenkorb/Anfrage, Standort Liège/Bruxelles, Zustand.
- **Pflicht-Screenshot:** Shop-Kategorie, Produktkarte, Detailseite mit Preis/Maß/Standort.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 2. Cornermat / Retrival
- **Link:** https://www.cornermat.be/shop
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Produktkarte + Materialfilter + Depot
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** Depot-Shop mit starker Materialnavigation.
- **Zu erfassende Kernfelder:** Kategorie, Material, Maße, Preis, Zustand, Gewicht/Origin wo sichtbar, Standort Charleroi/Namur.
- **Pflicht-Screenshot:** Kategoriebaum, Par MATIÈRE, Standortblock, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 3. Materialenbank Leuven / Atelier Circuler
- **Link:** https://ateliercirculer.be/materialenbank/catalogus
- **Interface-Archetyp:** Brokered Catalogue
- **Datenprofil:** Katalogkarte + Kontaktlogik
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** regionale Materialbank ohne zwingenden Checkout.
- **Zu erfassende Kernfelder:** Kategorie, Menge, Maße, Zustand, Kontakt-/Reservierungsweg, Lager-/Projektort.
- **Pflicht-Screenshot:** Katalogübersicht, konkrete Karte, Kontakt-/Abholhinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 4. RotorDC
- **Link:** https://rotordc.com/shop
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Produktkarte + Per-Building-Quelle
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** Shop und Quellgebäude-Navigation sind kombiniert.
- **Zu erfassende Kernfelder:** Kategorie, Preis, Maße/Menge, Quelle/Per Building, Zustand, Abholung/Versand.
- **Pflicht-Screenshot:** Per-Building-Menü, Listing, Detail mit Herkunft.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Deutschland

#### 5. Bauteilbörse Bremen
- **Link:** https://www.bauteilboerse-bremen.de/katalog
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Katalogkarte + Lagerort
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** klassischer lokaler Bauteilkatalog mit sehr konkreten Depotdaten.
- **Zu erfassende Kernfelder:** Kategorie, Artikelnummer, Maße, Material, Preis, Menge, Lagerort, Gewicht wo sichtbar.
- **Pflicht-Screenshot:** Kategorie-/Filterseite und Detailseite mit Lagerort/Artikeldaten.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 6. bauteilnetz Deutschland
- **Link:** https://bauteilnetz-bauteilkatalog.bauteillager.de/
- **Interface-Archetyp:** Brokered Catalogue
- **Datenprofil:** Verbundkatalog + Anbieter
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Verbundoberfläche; wichtiger als Einzelshop ist Anbieterzuordnung.
- **Zu erfassende Kernfelder:** Anbieter, Kategorie, Maße, Preis/Anfrage, Standort, Kontaktweg.
- **Pflicht-Screenshot:** Such-/Katalogseite, Anbieterhinweis, Detailangebot.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 7. Concular Shop
- **Link:** https://concular.shop/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Projektlisting + KG/Kategorie + B2B-Daten
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** B2B-Rückbaukatalog mit professioneller Klassifikation.
- **Zu erfassende Kernfelder:** Rückbauprojekt, Kategorie/KG, Maße, Menge, Preis/Anfrage, Verfügbarkeit, Gewährleistung/Dokumentation.
- **Pflicht-Screenshot:** Projektseite, Filter/KG, Listing mit Verfügbarkeits-/B2B-Hinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 8. Materialrest24
- **Link:** https://www.materialrest24.de/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Seller listing + Restposten
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Restmengen-Marktplatz: Angebot ist sellerabhängig.
- **Zu erfassende Kernfelder:** Verkäufer, Standort, Kategorie, Menge/Einheit, Preis, Zustand/neu-restposten, Kontakt/Checkout.
- **Pflicht-Screenshot:** Suchseite, Listingkarte, Anbieter-/Standorthinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 9. Restado
- **Link:** https://restado.de/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Seller listing + Stadt/Kategorie + Restposten/Rückbau
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** nationaler Bau-/Reststoffmarktplatz mit geografischer Suche.
- **Zu erfassende Kernfelder:** Kategorie, Stadt/Standort, Verkäufer, Menge, Preis/Anfrage, Zustand, Lieferung/Abholung.
- **Pflicht-Screenshot:** Kategorie- oder Stadt-Suche, Listing, Verkäufer-/Abholinfo.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Dänemark

#### 10. Genbyg
- **Link:** https://genbyg.dk/
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Produktkarte + Bestand + Quelle-Story
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** großer kontrollierter Lager-Webshop mit hoher Datenreife.
- **Zu erfassende Kernfelder:** Produktnummer, Kategorie, Maße, Preis, Bestand, Zustand, Abholung/Lieferung, Quelle wo sichtbar.
- **Pflicht-Screenshot:** Mega-Menü, Produktkarte, Detailseite, Quelle-Story falls vorhanden.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Frankreich

#### 11. Articonnex
- **Link:** https://articonnex.com/collections/reemploi
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Shopkollektion + Reuse-Hinweis
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Reuse-/Surplus-Shop; genaue Itemdaten live prüfen.
- **Zu erfassende Kernfelder:** Kategorie, Preis, Menge/Einheit, Zustand, Lager/Abholung, Reuse/anti-waste Status.
- **Pflicht-Screenshot:** Collection-Seite, Produktkarte, Detail mit Abholung/Status.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 12. Backacia
- **Link:** https://backacia.com/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Professional listing + availability window
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** B2B-Marktplatz mit Projekt-/Zeitdaten innerhalb sellerbasierter Angebote.
- **Zu erfassende Kernfelder:** Kategorie, Menge/Einheit, Preis HT/Anfrage, Stadt, Verfügbarkeitsfenster, Verkäufer/Projekt.
- **Pflicht-Screenshot:** Such-/Kategorieansicht, Listing mit Stadt/Menge/Datum.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 13. BatRecup
- **Link:** https://www.batrecup.com/marketplace-3/
- **Interface-Archetyp:** External/App Channel
- **Datenprofil:** App-/Marktplatzkanal
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** Hauptwebsite ist nur Kanalnachweis; Angebotsdaten müssen im Zielkanal belegt werden.
- **Zu erfassende Kernfelder:** echtes App-/Marketplace-Listing, Kategorie, Ort, Menge, Kontaktaktion.
- **Pflicht-Screenshot:** Landingpage + echtes App/Marketplace-Listing.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 14. Bâticycle
- **Link:** https://marketplace.skop.app/baticycle
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Seller/profile listing within Skop
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Anbieterprofil innerhalb einer Marktplatzlogik.
- **Zu erfassende Kernfelder:** Verkäuferprofil, konkrete Listings, Standort, Menge, Preis/Anfrage, Herkunft.
- **Pflicht-Screenshot:** Profilseite und mindestens ein konkretes Listing.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 15. Cycle Up
- **Link:** https://www.cycle-up.fr/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Marketplace + diagnostic/reconditioning context
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** Marktplatz plus professioneller Kontext; Listing muss vom Service-Text getrennt werden.
- **Zu erfassende Kernfelder:** Kategorie, Menge, Standort, Preis/Anfrage, Herkunft, CO₂/Abfall wo sichtbar, Verkäufer/Projekt.
- **Pflicht-Screenshot:** Marketplace-Einstieg, Listing, Herkunft/Nachweisfeld.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 16. Cycle Zéro
- **Link:** https://cyclezero.fr/particulier.html
- **Interface-Archetyp:** External/App Channel
- **Datenprofil:** App-first local listing
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** lokale Reuse-Vermittlung; Website reicht nicht als Inventarbeleg.
- **Zu erfassende Kernfelder:** App-Listing, Ort, Kategorie, Menge, Abgabe-/Anfrageaktion.
- **Pflicht-Screenshot:** Website-Einstieg + App-Screen mit konkretem Angebot.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 17. R-Place
- **Link:** https://r-place.fr/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** B2B listing
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** B2B-Marktplatz mit feldgetriebener Beschaffung.
- **Zu erfassende Kernfelder:** Kategorie, Anbieter, Standort, Menge, Preis/Anfrage, Zustand, technische Spezifikation.
- **Pflicht-Screenshot:** Marketplace-Suche, Listingkarte, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 18. RAEDIFICARE
- **Link:** https://raedificare.com/marketplace/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** B2B procurement + lot/specification
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** professioneller Projekt-/Beschaffungsworkflow statt einfacher Konsumentenshop.
- **Zu erfassende Kernfelder:** technisches Los, Gebäudetyp, Standort, Spezifikation, Verfügbarkeit, Anfrage, Attestation/Nachweis.
- **Pflicht-Screenshot:** Marketplace/Buyer-Interface, Filter, Anfrage-/Bedarfsfunktion.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 19. REFAIR Bordeaux
- **Link:** https://refair-bm.fr/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Resource dossier + interest list
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Projektressourcen werden als Dossier/Interesse koordiniert.
- **Zu erfassende Kernfelder:** Ressourcendossier, Projektquelle, Kategorie, Menge, Verfügbarkeit, Interessenliste/Kontakt.
- **Pflicht-Screenshot:** Ressourcendossier, Materialkarte, List-/Interessensfunktion.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 20. Réempro
- **Link:** https://www.reempro.com/marketplace
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Professional listing
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** professioneller Reuse-Marktplatz; Datenqualität listingabhängig.
- **Zu erfassende Kernfelder:** Kategorie, Verkäufer, Standort, Menge, Preis/Anfrage, Zustand, Verfügbarkeit.
- **Pflicht-Screenshot:** Marketplace-Übersicht, Listing, Verkäufer-/Kontaktfeld.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 21. Skop Marketplace
- **Link:** https://marketplace.skop.app/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Seller listing + around-me/all-France
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** starke Orts- und Verkäuferlogik in einem professionellen Marktplatz.
- **Zu erfassende Kernfelder:** Kategorie, Ort, Seller, Menge, Einheitspreis, Herkunft, Suchradius/All-France Toggle.
- **Pflicht-Screenshot:** Suchseite mit Standorttoggle, Listing, Verkäuferprofil.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Niederlande

#### 22. Gebruiktebouwmaterialen
- **Link:** https://gebruiktebouwmaterialen.com/assortiment.html
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Assortment catalogue
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** sortimentsorientierter Shop/Katalog für gebrauchte Baumaterialien.
- **Zu erfassende Kernfelder:** Kategorie, Produkt, Maße, Preis/Anfrage, Zustand, Abholung/Kontakt.
- **Pflicht-Screenshot:** Assortiment, Produktkarte, Kontakt-/Abholhinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 23. Insert Marketplace
- **Link:** https://www.insert.nl/producten/insert-marktplaats/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Reuse marketplace listing
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** strukturierter Marktplatz; Live-Produktansicht ist entscheidend.
- **Zu erfassende Kernfelder:** Kategorie, Anbieter/Projekt, Standort, Menge, Verfügbarkeit, Anfrageaktion, Spezifikation.
- **Pflicht-Screenshot:** Marktplatzseite, Such-/Filteransicht, Detaillisting.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 24. ReSource Marktplaats
- **Link:** https://play.google.com/store/apps/details?id=com.pss.resource
- **Interface-Archetyp:** External/App Channel
- **Datenprofil:** App-store/app listing
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** App-Store ist kein Inventar; tatsächliche App-Oberfläche prüfen.
- **Zu erfassende Kernfelder:** App-Listing, Kategorie, Ort, Menge, Aktion, Aktualität.
- **Pflicht-Screenshot:** App-Store-Seite + In-App-Angebot.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Schweiz

#### 25. Archipel Sion Ressourcerie
- **Link:** https://archipelsion.ch/ressourcerie/inventaire/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Resource inventory + project/location context
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Ressourcerie-Inventar mit Projekt-/Standortlogik.
- **Zu erfassende Kernfelder:** Inventarobjekt, Kategorie, Maße, Menge, Ort, Verfügbarkeit, Kontakt/Reservierung.
- **Pflicht-Screenshot:** Inventarseite, Objektkarte, Detail/Kontakt.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 26. Baumatpool.ch
- **Link:** https://www.baumatpool.ch/de/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Seller listing + category/location
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** klassische baunahe Marktplatzlogik.
- **Zu erfassende Kernfelder:** Kategorie, Verkäufer, Standort, Menge, Preis, Zustand, Abholung/Lieferung.
- **Pflicht-Screenshot:** Suche/Filter, Listingkarte, Anbieter/Ort.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 27. Bauteilbörse Basel
- **Link:** https://bauteilboerse-basel.ch/bauteile/
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Regional depot catalogue
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** regionaler Bauteilladen/Katalog.
- **Zu erfassende Kernfelder:** Kategorie, Maße, Preis/Anfrage, Zustand, Lager/Abholung, Kontakt.
- **Pflicht-Screenshot:** Bauteile-Übersicht, Produktdetail, Standort/Öffnungszeiten.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 28. Bauteilladen Winterthur
- **Link:** https://bauteilladen.ch/shop
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Shop catalogue
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** lokaler Bauteilladen mit Shoplogik.
- **Zu erfassende Kernfelder:** Kategorie, Maße, Preis, Zustand, Lager/Abholung, Warenkorb/Kontakt.
- **Pflicht-Screenshot:** Shopkategorie, Produktkarte, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 29. Bauteilvermittlung Zürichsee-Oberland
- **Link:** https://www.btvz.ch/angebote/
- **Interface-Archetyp:** Brokered Catalogue
- **Datenprofil:** Offer list + mediation
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Vermittlung statt automatischer Shop; Kontaktweg ist Kernfunktion.
- **Zu erfassende Kernfelder:** Angebot, Kategorie, Maße, Ort, Kontakt, Verfügbarkeit.
- **Pflicht-Screenshot:** Angebotsliste, Detailangebot, Kontakt-/Vermittlungshinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 30. Bauteilverwertung Köppel & Klein
- **Link:** https://www.bauteilverwertung.ch/verkauf.html
- **Interface-Archetyp:** Brokered Catalogue
- **Datenprofil:** Sales list/page + contact
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Verkaufsseite eines Verwertungsakteurs; Daten je Angebot prüfen.
- **Zu erfassende Kernfelder:** Kategorie, Maße, Zustand, Preis/Anfrage, Abholort, Kontakt.
- **Pflicht-Screenshot:** Verkaufsseite, einzelnes Angebot, Abholung/Kontakt.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 31. GGZ@WORK Laden 2 Bauteile Zug
- **Link:** https://ggzatwork.ch/gaeste/laden2/laden-2-bauteile
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Physical store visibility
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** sozialer physischer Bauteilladen; Website kann stärker als Ladenbeleg als Listingbeleg wirken.
- **Zu erfassende Kernfelder:** Sortiment/Kategorie, Ladenstandort, Öffnungszeiten, konkrete Artikel falls sichtbar, Kontakt.
- **Pflicht-Screenshot:** Ladenseite + konkreter Angebots-/Sortimentsbeleg.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 32. Gruner ReUse
- **Link:** https://www.gruner-reuse.ch/produkte
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Structured product platform + technical fields
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** strukturierte ReUse-Oberfläche mit professioneller Datenlogik.
- **Zu erfassende Kernfelder:** Kategorie, technische Daten, Standort, Verfügbarkeit/Jahr, Zustand, Anbieter/Projekt.
- **Pflicht-Screenshot:** Produktübersicht, Filter, Detail mit Spezifikationen.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 33. La Ressourcerie Fribourg
- **Link:** https://www.la-ressourcerie.ch/les-mat%C3%A9riaux
- **Interface-Archetyp:** Brokered Catalogue
- **Datenprofil:** Selective materials catalogue
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** selektive Ressourcerie-Liste; nicht als Gesamtinventar lesen.
- **Zu erfassende Kernfelder:** Material, Kategorie, Menge, Zustand, Ort, Kontakt/Reservierung.
- **Pflicht-Screenshot:** Materialienseite, konkrete Materialkarte, Kontaktweg.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 34. Matériuum
- **Link:** https://materiuum.ch/boutique/
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Shop + classification/category
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** Ressourcerie-Shop mit vergleichsweise strukturierter Klassifikation.
- **Zu erfassende Kernfelder:** Kategorie, eCCC/classification wo sichtbar, Maße, Preis, Zustand, Menge, Standort/Abholung.
- **Pflicht-Screenshot:** Boutique-Filter, Produktkarte, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 35. Matériuum Genève Ressourcerie
- **Link:** https://materiuum.ch/boutique/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Project/channel within Matériuum
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** nicht automatisch identisch mit der allgemeinen Matériuum-Boutique; Kanal sauber trennen.
- **Zu erfassende Kernfelder:** Kanal/Projekt, konkrete Ressource, Ort, Verfügbarkeit, Kontakt.
- **Pflicht-Screenshot:** Projekt-/Genève-Hinweis + konkretes Ressourcerie-Angebot.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 36. Ressourcerie Lausanne / Matériuum / R-UUL
- **Link:** https://materiuum.ch/boutique/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Project/channel within Matériuum/R-UUL
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** nicht automatisch identisch mit der allgemeinen Matériuum-Boutique; Kanal sauber trennen.
- **Zu erfassende Kernfelder:** Kanal/Projekt, konkrete Ressource, Ort, Verfügbarkeit, Kontakt.
- **Pflicht-Screenshot:** Lausanne/R-UUL-Kontext + konkretes Angebot.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 37. ReUse Recycling Center Riedtwil / wiederverwendung.ch
- **Link:** https://shop.wiederverwendung.ch/de/434/gebrauchte-bauteile-occasion-bauteile
- **Interface-Archetyp:** Depot-Shop
- **Datenprofil:** Shop category + used components
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** physischer ReUse-Shop/Katalog mit konkretem Bauteilbereich.
- **Zu erfassende Kernfelder:** Kategorie, Preis, Maße, Zustand, Menge, Abholung/Versand, Warenkorb.
- **Pflicht-Screenshot:** Kategorie gebrauchte Bauteile, Produktkarte, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 38. REUZI
- **Link:** https://reuzi.ch/agora/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Agora listing + project/seller context
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Agora-/Marktplatzlogik; Beschaffbarkeit je Beitrag prüfen.
- **Zu erfassende Kernfelder:** Kategorie, Anbieter, Ort, Menge, Verfügbarkeit, Kontakt/Anfrage, Zustand.
- **Pflicht-Screenshot:** Agora-Übersicht, Angebot, Anbieter/Ort.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 39. Salza
- **Link:** https://salza.ch/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Search/radius + admin-reviewed listing + chat/handover
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** starkes Plattformmodell mit Koordinationsworkflow.
- **Zu erfassende Kernfelder:** Kategorie, Suchradius/Ort, Anbieter, Maße, Menge, Zustand, Chat/Übergabe, Freigabeprozess.
- **Pflicht-Screenshot:** Suche/Radius, Angebotsworkflow, Listing/Chat-/Übergabehinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 40. Stiftung Chance BauTeile Zürich / Glattbrugg
- **Link:** https://www.chance.ch/dienstleistungen/bauteile
- **Interface-Archetyp:** Brokered Catalogue
- **Datenprofil:** Physical social-enterprise offer + contact
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** Bauteilangebot ist real, aber Website muss mit konkretem Listing ergänzt werden.
- **Zu erfassende Kernfelder:** Standort, Sortiment, Öffnungszeiten/Kontakt, konkrete Angebotsebene falls vorhanden.
- **Pflicht-Screenshot:** Dienstleistungsseite + konkreter Verkaufs-/Sortimentsnachweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 41. useagain / Bauteilclick
- **Link:** https://www.useagain.ch/de/kaufen
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Listing + PLZ/Umkreis + delivery mode
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** sehr starkes geografisches und logistisches Filtermodell.
- **Zu erfassende Kernfelder:** Kategorie, Händler/Ort, PLZ+Umkreis, Material/Farbe/Zustand, Versandart, Preis, Menge.
- **Pflicht-Screenshot:** Kaufen-Seite mit Radiusfilter, Listing, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 42. Wick ReUse / ROTO Baumarkt
- **Link:** https://www.ricardo.ch/de/shop/ReUse_Baumarkt/offers/
- **Interface-Archetyp:** External/App Channel
- **Datenprofil:** External shop/channel listing
- **Datenreife:** 1 — kanalabhängig: ohne App-/externes/konkretes Listing nur Rollen- oder Einstiegshinweis, nicht als Inventar auswerten.
- **Pattern-Bedeutung:** sichtbares Inventar liegt im externen Kanal.
- **Zu erfassende Kernfelder:** Ricardo-/externe Angebotskarte, Preis, Ort, Zustand, Verkäufer, Abholung/Versand.
- **Pflicht-Screenshot:** ROTO/Wick-Kontext + Ricardo-Angebot.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Vereinigtes Königreich

#### 43. Building Spares Market
- **Link:** https://buildingsparesmarket.co.uk/advert-category/general-building-materials
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Classified listing + category/location
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** klassischer Kleinanzeigenmarkt für Baureste.
- **Zu erfassende Kernfelder:** Kategorie, Verkäufer, Ort/Postcode, Preis, Menge, Zustand, Kontakt.
- **Pflicht-Screenshot:** Kategorieansicht, Anzeige, Kontakt/Ort.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 44. Enviromate
- **Link:** https://www.enviromate.co.uk/marketplace
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Classified listing + distance radius
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** gutes Beispiel für explizite Radiuslogik.
- **Zu erfassende Kernfelder:** Kategorie, Standort, Distanzradius, Preis, Menge, Verkäufer, Kontakt.
- **Pflicht-Screenshot:** Marketplace-Suche mit Radius, Listingkarte, Detailseite.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 45. Globechain
- **Link:** https://marketplace.globechain.com/business/construction
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Business marketplace listing
- **Datenreife:** 2 — verwendbar nach Live-Screenshot: Plattform passt in den Korpus, aber konkrete Datenfelder müssen pro Listing geprüft werden.
- **Pattern-Bedeutung:** Ressourcenmarktplatz mit construction-Kategorie; konkrete Listingtiefe prüfen.
- **Zu erfassende Kernfelder:** Kategorie, Anbieter, Ort, Menge, Preis/Free/Anfrage, Abholung/Lieferung, Zustand.
- **Pflicht-Screenshot:** Construction-Kategorie, Listing, Anbieter/Logistik.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 46. Material Index
- **Link:** https://material-index.co.uk/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Marketplace + audit/brokerage overlay
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** öffentliches Marktplatz-/Beschaffungsziel mit zusätzlichem Audit-Kontext.
- **Zu erfassende Kernfelder:** Kategorie, Anbieter/Projekt, Standort, Maße/Menge, Preis/Anfrage, Nachweis/Brokerage-Kontext.
- **Pflicht-Screenshot:** Marketplace-Einstieg, Listing, Daten-/Brokeragehinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 47. SalvoWEB
- **Link:** https://www.salvoweb.com/antique-reclaimed
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Salvage search + dealer/profile hybrid
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** Marketplace/Verzeichnis-Hybrid; Listing- und Händlerdaten trennen.
- **Zu erfassende Kernfelder:** Kategorie, Gebiet/Area, Händler/Verkäufer, Preis/Anfrage, Beschreibung, Kontakt.
- **Pflicht-Screenshot:** Search nach area/category, Listing, Dealerprofil.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 48. Surplus Building & Plumbing Materials
- **Link:** https://surplusbuildingsupplies.co.uk/building-materials.html
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** E-commerce listing + collect-from-postcode
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** merchant-artiger Surplus-Marktplatz mit starker Abholortlogik.
- **Zu erfassende Kernfelder:** Kategorie, Preis inkl. VAT, Menge, Verkäufer, collect-from/Postcode, Abholung/Lieferung, Zustand/Surplus.
- **Pflicht-Screenshot:** Produktliste, collect-from-Hinweis, Detail/Checkoutdaten.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 49. Sustainability Yard
- **Link:** https://sustainabilityyard.com/
- **Interface-Archetyp:** Marketplace
- **Datenprofil:** Seller listing + modern marketplace UX
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** moderner Multi-Seller-Marktplatz für Bau-/Surplusmaterial.
- **Zu erfassende Kernfelder:** Kategorie, Verkäufer, Standort, Preis/VAT, Menge, Zustand, Sell/Buy workflow.
- **Pflicht-Screenshot:** Homepage/Marketplace, Listing, Verkäufer-/Standorthinweis.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

### Österreich

#### 50. BauKarussell
- **Link:** https://katalog.baukarussell.at/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** Project/resource catalogue
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** Social-Urban-Mining-Katalog mit starker Projektquelle.
- **Zu erfassende Kernfelder:** Projekt, Bauteil/Ressource, Menge, Maße, Verfügbarkeit, Kontakt/Interesse, Herkunft.
- **Pflicht-Screenshot:** Katalogstart, Projekt/Ressource, Interessen-/Kontaktweg.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

#### 51. re:Laden / HarvestMAP Vienna
- **Link:** https://www.restore.or.at/
- **Interface-Archetyp:** Project/Harvest Catalogue
- **Datenprofil:** List/map + project/source listing
- **Datenreife:** 3 — direkt vergleichbar: öffentliche Listing-/Filter-/Detaildaten sind für Screenshot-Vergleich stark genug, dynamische Daten trotzdem datieren.
- **Pattern-Bedeutung:** HarvestMAP-Logik: Karte/Liste und Quelle sind zentrale Interfaceelemente.
- **Zu erfassende Kernfelder:** Liste/Karte, Projektquelle, Kategorie, Menge, Verfügbarkeit, Kontakt/Reservierung, Ort.
- **Pflicht-Screenshot:** Liste/Karte-Toggle, Filter, Projekt-/Quelleintrag.
- **Interpretationsregel:** Dieses Angebot nur auf Listing-/Screenshot-Ebene auswerten; keine Plattform-Inventarquote ableiten.

## 8. Screenshot-Protokoll nach Archetyp

| Archetyp | Screenshot 1 | Screenshot 2 | Screenshot 3 | Screenshot 4 |
| --- | --- | --- | --- | --- |
| Depot-Shop | Shop-/Kategorieeinstieg | Produktkarte | Detailseite mit Daten | Standort/Abholung/Warenkorb |
| Marketplace | Suche/Filter mit Ort | Listingkarte | Verkäufer/Standort | Kontakt/Checkout/Radius |
| Project/Harvest Catalogue | Projekt-/Quellübersicht | Ressource/Charge | Verfügbarkeitsfenster | Anfrage/Interesse/Nachweis |
| Brokered Catalogue | Angebots-/Materialliste | konkrete Karte | Kontakt/Vermittlung | Standort/Abholung |
| External/App Channel | offizielle Einstiegsseite | externer/App-Kanal | echtes Listing | Aktion/Ort/Verkäufer |

### 8.1 Dateinamen

`YYYY-MM-DD_land_plattform_archetyp_ebene_kurzbeschreibung.png`

Beispiele:
- `2026-06-04_be_cornermat_depot-shop_materialfilter_detail.png`
- `2026-06-04_ch_useagain_marketplace_radius_listing.png`
- `2026-06-04_at_baukarussell_harvest_project-resource.png`

## 9. Saubere Forschungslogik

Diese Recherche bleibt Bauteilbörse-only, indem sie nur Oberflächen behandelt, die konkrete physische Bauteile, Baustoffreste, Rückbauressourcen oder Reuse-Materialien sichtbar und beschaffbar machen. Die relevanten Plattformen werden nicht danach bewertet, ob sie modern aussehen, sondern danach, ob sie genügend Daten zeigen, um ein Bauteil real zu finden, zu prüfen und zu beschaffen.

Der wichtigste Designschluss lautet: Eine gute Bauteilbörse braucht nicht viele Interface-Kategorien, sondern eine klare Kombination aus **Bauteilsuche, Datenqualität, Ort/Logistik, Verfügbarkeit und Handlung**. Alles andere ist sekundär.
