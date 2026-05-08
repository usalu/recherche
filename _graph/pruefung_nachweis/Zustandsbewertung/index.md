---
id: "Zustandsbewertung"
entity: "pruefung_nachweis"
node_kind: "knot"
migration_status: "migrated_phase1_stable_knots"
migration_action: "move_as_knot"
title: "Zustandsbewertung"
legacy_type: "PrÃ¼fung"
legacy_paths:
  - "pruefung\Zustandsbewertung.md"
target_primary: "pruefung_nachweis/Zustandsbewertung"
target_secondary: ""
risk_flags: ""
---
# Zustandsbewertung

## Migration

- Target: pruefung_nachweis/Zustandsbewertung
- Legacy source count: 1
- Legacy types: PrÃ¼fung
- Migration actions: move_as_knot
- Secondary targets: 
- Risk flags: 

## Legacy Content: pruefung\Zustandsbewertung.md

---
type: Prüfung
bauteil: ["[[bauteil/Betonfertigteil]]", "[[bauteil/Deckenplatte]]", "[[bauteil/Wand]]"]
verwandt: ["[[pruefung/Geometrische_Vermessung]]", "[[pruefung/Materialpruefung]]", "[[pruefung/Schadstoffscreening]]", "[[pruefung/Sichtpruefung]]"]
---

## Verknüpfungen

- **Übergeordnete Themen:** Wiederverwendungsentscheidung, Risikobewertung, Restnutzungsdauer, Bauwerksdiagnostik, Bauteilfreigabe, Nachweisführung, zirkuläre Planung, Rückbau- und Wiedereinbaukonzept.
- **Verwandte Dateien / Dateigruppen:** `pruefung/Sichtpruefung.md`, `pruefung/Materialpruefung.md`, `pruefung/Geometrische_Vermessung.md`, `pruefung/Schadstoffscreening.md`; außerdem `material/`, `bauteil/`, `schadstoff/`, `logistik/` und `leistungsanforderung/`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** Bauherrschaft, Architekt:innen, Tragwerksplaner:innen, Prüfingenieur:innen, Sachverständige, Materialprüfanstalten, Schadstoffgutachter:innen, Behörden, Versicherer, Rückbauunternehmen, Bauteilbörsen; DIN SPEC 91484, VDI 6200, DIN 1076, Eurocodes, DGNB Rückbau, BNB, Bauteilpass, Prüfmatrix, Risikoanalyse, Zustandsklassen, Restnutzungsdauerbewertung.

## Kurzdefinition

Zustandsbewertung ist die fachliche Gesamtbeurteilung eines Bauteils oder Bauteilkollektivs im Hinblick auf seine Eignung für eine definierte Anschlussnutzung. Sie integriert Sichtprüfung, geometrische Vermessung, Materialprüfung, Schadstoffscreening, Dokumentenlage, Rückbaurisiken, Logistik und Leistungsanforderungen. Ergebnis ist eine nachvollziehbare Entscheidung: direkte Wiederverwendung, Wiederverwendung nach Aufbereitung, Wiederverwendung mit Einschränkungen, andere Nutzung, Recycling oder Entsorgung.

Abgrenzung:

- **Sichtprüfung:** liefert sichtbare Befunde und Verdachtsmomente.
- **Materialprüfung:** liefert Werkstoffkennwerte und technische Labor-/Messdaten.
- **Geometrische Vermessung:** liefert Maße, Verformungen und Passfähigkeit.
- **Schadstoffscreening:** liefert Gesundheits-, Arbeitsschutz- und Freigabestatus.
- **Zustandsbewertung:** fasst alle diese Daten in Relation zur geplanten zweiten Nutzung zusammen.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung erfordert eine belastbare Entscheidung unter Unsicherheit. Anders als beim Recycling, bei dem Material in einen neuen Rohstoffstrom übergeht, bleibt beim Re-Use die Bauteilidentität mit ihrer Nutzungsgeschichte erhalten. Deshalb ist die Zustandsbewertung der zentrale Gatekeeper zwischen Potenzial und tatsächlicher Verwendung.

Sie ist relevant für:

- **technische Sicherheit:** Tragfähigkeit, Gebrauchstauglichkeit, Dauerhaftigkeit, Brandschutz, Hygiene, Dichtheit;
- **rechtliche Nachweisführung:** Bauordnungsrecht, Verwendbarkeitsnachweise, Genehmigungsfähigkeit, Haftung;
- **wirtschaftliche Entscheidung:** Prüf-, Ausbau-, Reparatur-, Lager- und Anpassungskosten;
- **ökologische Entscheidung:** Re-Use nur dort, wo ökologische Vorteile nicht durch Sanierung, Transport oder Ausschuss aufgehoben werden;
- **Planungssicherheit:** frühzeitige Entscheidung, welche Bauteile in Entwurf, Ausschreibung und Terminplan eingehen können;
- **Kommunikation:** einheitliche Sprache zwischen Bestandseigentümer, Planenden, Rückbau, Prüflabor, Marktplatz und neuer Baustelle.

## Fachinhalt

### Ziel

Die Zustandsbewertung beantwortet:

- Kann das Bauteil in der vorgesehenen zweiten Nutzung die geforderten Leistungen erfüllen?
- Welche Nachweise sind vorhanden, welche fehlen?
- Welche Schäden, Verformungen, Kontaminationen oder Unsicherheiten sind relevant?
- Welche Maßnahmen sind nötig: Reinigung, Reparatur, Verstärkung, Zuschnitt, Herabstufung, Beschränkung, Monitoring?
- Welche Risiken bleiben und wer trägt sie?
- Ist die Wiederverwendung gegenüber Ersatz, Recycling oder Entsorgung sinnvoll?

### Typischer Ablauf

1. **Zielnutzung und Leistungsanforderungen definieren**
   - Tragend/nicht tragend, Innen/Außen, temporär/dauerhaft, sichtbar/nicht sichtbar, feucht/trocken, öffentlich/privat.
   - Leistungsanforderungen festlegen: Tragfähigkeit, Brandschutz, Schallschutz, Wärmeschutz, Hygiene, Emissionen, Dauerhaftigkeit, Ästhetik, Wartung.

2. **Bauteilakte aufbauen**
   - Herkunft, Baujahr, Lage, Funktion, Fotos, Pläne, Herstellerdaten, Prüfzeugnisse, Umbauten, Nutzungsgeschichte.
   - Bauteil-ID und Dokumentationsstruktur festlegen.
   - Fehlende Daten und Unsicherheiten markieren.

3. **Prüfdaten integrieren**
   - Sichtbefunde: Schäden, Demontagerisiken, Oberflächenzustand.
   - Geometrie: Maße, Toleranzen, Verformung, Anschlussdetails.
   - Materialdaten: Festigkeit, Dauerhaftigkeit, Korrosion, Feuchte, Alterung.
   - Schadstoffe: Befunde, Freigabe, Sanierungsbedarf, Nutzungseinschränkungen.
   - Logistik: Ausbau, Transport, Lagerung, Rückverfolgbarkeit.

4. **Schadens- und Degradationsmechanismen bewerten**
   - Ursache, Fortschritt und Relevanz: z. B. Korrosion, Karbonatisierung, Chloride, Fäule, Ermüdung, Frost, Feuchte, UV, Brand, chemischer Angriff.
   - Akute Schäden von tolerierbarer Patina unterscheiden.
   - Einmalige Vorschäden und fortschreitende Schädigung getrennt bewerten.

5. **Abgleich mit Zielanforderungen**
   - Prüfdaten in Bemessungs-, Bauphysik-, Hygiene- und Nutzungskontext übersetzen.
   - Bei fehlenden Nachweisen konservative Ansätze, Zusatzprüfungen oder Nutzungseinschränkungen festlegen.
   - Anschluss- und Montagekonzept berücksichtigen.

6. **Klassifizierung**
   - Beispielhafte Re-Use-Klassen:
     - **R0 Ausschluss:** Gefahrstoff, gravierender Schaden, fehlende Sicherheit, nicht demontierbar oder wirtschaftlich/ökologisch unsinnig.
     - **R1 Direkte Wiederverwendung:** ausreichend dokumentiert, schadstofffrei/freigegeben, geringe Schäden, Anforderungen erfüllt.
     - **R2 Wiederverwendung nach Aufbereitung:** Reinigung, Reparatur, Entschichtung, Zuschnitt, neue Verbindungsmittel oder Ersatzteile erforderlich.
     - **R3 Eingeschränkte Wiederverwendung:** nur in niedrigerer Belastung, nichttragend, Innenraum statt Außenraum, temporär oder mit Monitoring.
     - **R4 Alternative Anschlussnutzung:** gestalterisch, Landschaftsbau, Möbel, nicht sicherheitsrelevante Nutzung.
   - Klassen müssen projektspezifisch definiert und im Prüfbericht erklärt werden.

7. **Entscheidung und Freigabe**
   - Verantwortliche Fachpersonen benennen.
   - Prüfbefund, Bewertungslogik, Auflagen, Restunsicherheiten und Gültigkeitsbereich dokumentieren.
   - Freigabe an konkrete Zielnutzung binden, nicht pauschal an das Bauteil.

8. **Kontrolle im Prozess**
   - Zustand nach Ausbau, Transport, Lagerung und vor Wiedereinbau erneut kontrollieren.
   - Abweichungen nachbewerten und Bauteilakte aktualisieren.

### Bewertungsdimensionen

#### Technischer Zustand

- Schäden, Verformungen, Restquerschnitt, Tragreserven, Steifigkeit, Ermüdung, Verbindungen, Brandschäden, Feuchte, Alterung.
- Frage: Kann das Bauteil die geforderte technische Leistung sicher und dauerhaft erfüllen?

#### Schadstoff- und Gesundheitszustand

- Asbest, PCB, PAK, KMF, Holzschutzmittel, Schwermetalle, Schimmel, Nutzungschemikalien, Emissionen.
- Frage: Ist die geplante Nutzung gesundheitlich und rechtlich zulässig?

#### Geometrische und konstruktive Eignung

- Maße, Toleranzen, Passfähigkeit, Anschlussmöglichkeiten, Reparatur- und Adapterbedarf, Demontierbarkeit.
- Frage: Kann das Bauteil ohne unverhältnismäßige Anpassung integriert werden?

#### Dokumentationszustand

- Pläne, Herstellerdaten, Prüfzeugnisse, Materialnachweise, Fotos, Proben, Prüfberichte, Rückbauprotokolle.
- Frage: Reicht die Nachweisführung für Planung, Bauaufsicht, Versicherung und spätere Betreiber?

#### Logistischer Zustand

- Ausbauzustand, Verpackung, Lagerung, Feuchteschutz, Kennzeichnung, Transportfähigkeit.
- Frage: Bleibt die Qualität bis zum Wiedereinbau erhalten?

#### Wirtschaftlich-ökologische Eignung

- Prüfkosten, Rückbaukosten, Sanierung, Transport, Lagerung, Anpassung, Ersatzteilbedarf, CO₂- und Ressourcenersparnis.
- Frage: Ist Wiederverwendung gegenüber Neuprodukt oder Recycling plausibel vorteilhaft?

### Aussagekraft

Eine gute Zustandsbewertung liefert:

- eine nachvollziehbare Re-Use-Entscheidung;
- Prüf- und Maßnahmenplan;
- Bauteilklassen und Prioritäten;
- Auflagen für Rückbau, Lagerung und Wiedereinbau;
- Nachweispaket für Entwurf, Genehmigung und Ausschreibung;
- Restunsicherheiten und Verantwortlichkeiten.

Sie ersetzt nicht:

- detaillierte statische Berechnung;
- bauaufsichtliche Zustimmung, wenn erforderlich;
- vollständiges Schadstoffgutachten;
- produktspezifische Leistungserklärungen;
- laufende Qualitätssicherung während Demontage, Transport und Montage.

### Grenzen

- Bewertungsmaßstäbe für wiederverwendete Bauprodukte sind noch uneinheitlich.
- Bestehende Normen beziehen sich oft auf Neubauprodukte, Instandhaltung oder Bauwerksprüfung, nicht direkt auf Re-Use.
- Zielnutzung verändert die Bewertung: Ein Bauteil kann für Innenausbau geeignet und für tragende Außenanwendung ungeeignet sein.
- Restnutzungsdauer ist probabilistisch und hängt von zukünftiger Exposition und Wartung ab.
- Dokumentationslücken können durch Prüfung reduziert, aber nicht immer geschlossen werden.
- Haftung, Gewährleistung und Versicherung müssen projektspezifisch vertraglich und fachlich geklärt werden.
- Eine positive Bewertung vor Rückbau kann durch Demontageschäden entfallen.

### Schnittstellen

- **Zu Sichtprüfung:** Sichtprüfung liefert die erste Schadens- und Potenzialeinschätzung; Zustandsbewertung gewichtet sie.
- **Zu Materialprüfung:** Kennwerte werden in Bemessung, Dauerhaftigkeit und Restnutzung übersetzt.
- **Zu geometrischer Vermessung:** Passfähigkeit und Toleranzmanagement fließen in Wiederverwendungskonzept und Detailplanung ein.
- **Zu Schadstoffscreening:** Ohne Freigabe oder Sanierung ist technische Eignung allein nicht ausreichend.
- **Zu Logistik:** Bewertung muss Lager- und Transportzustand berücksichtigen; falsche Lagerung kann eine Freigabe entwerten.
- **Zu Leistungsanforderungen:** Die Bewertung ist nur in Bezug auf konkrete Anforderungen sinnvoll.
- **Zu Bauteilpass / Materialkataster:** Zustandsbewertung bildet die qualifizierte Entscheidungsebene über Rohdaten.

## Praxisbezug / Beispiele

- **Stahlträger aus Industriehalle:** Sichtprüfung zeigt geringe Korrosion, Materialanalyse bestätigt geeignete Stahlgüte, Geometrie passt in ein neues Raster, Beschichtung enthält jedoch Schwermetalle. Zustandsbewertung: Wiederverwendung nach fachgerechter Entschichtung und neuer Beschichtung; keine erneute Ermüdungsbeanspruchung; Anschlussdetails neu bemessen.
- **Betonstützen aus Parkhaus:** Geometrisch geeignet, aber Chloridbelastung und Bewehrungskorrosion sind lokal hoch. Zustandsbewertung: tragende Wiederverwendung nur mit vertiefter Prüfung und Instandsetzung; alternativ nichttragende oder landschaftsbauliche Nutzung prüfen.
- **Holzbalken aus Gründerzeitgebäude:** Sichtbar gut erhalten, aber Holzschutzmittel nachgewiesen. Zustandsbewertung: keine Wiederverwendung in Aufenthaltsräumen; eventuell Außen-/Technikbereich nach Sanierung und Emissionsbewertung oder Ausschluss.
- **Natursteinplatten:** Viele Platten haben Kantenabbrüche, aber ausreichende Dicke. Zustandsbewertung: direkte Fassadenwiederverwendung nur für intakte Platten; beschädigte Platten als Bodenbelag oder Zuschnitt in kleinere Formate.
- **Türen aus Verwaltungsbau:** gute Sichtqualität, aber fehlende Brandschutz- und Schallschutznachweise. Zustandsbewertung: Nutzung als normale Innentüren möglich, nicht als Brandschutzabschlüsse ohne gültigen Nachweis.

## Herausforderungen / offene Fragen

- Einheitliche Re-Use-Zustandsklassen fehlen für viele Bauteilgruppen.
- Genehmigungsbehörden, Prüfingenieur:innen und Versicherer akzeptieren Nachweiskonzepte unterschiedlich.
- Für gebrauchte Produkte ist unklar, wann sie rechtlich wieder zum Bauprodukt werden und welche Pflichten ausgelöst werden.
- Digitale Bauteilpässe müssen Prüfstatus, Auflagen und Gültigkeitsbereich maschinenlesbar abbilden.
- Restnutzungsdauer und Wartungsbedarf sollten stärker in Ausschreibung und Betreiberpflichten integriert werden.
- Bewertungsaufwand muss zum Bauteilwert passen; sonst werden nur hochwertige Bauteile wiederverwendet.
- Zielkonflikt: robuste Sicherheit versus Ressourcenschutz. Konservative Ausschlüsse können Wiederverwendung verhindern, zu optimistische Bewertungen können Risiken verlagern.
- Ein zweiter Lebenszyklus braucht Monitoring: Wiederverwendung endet nicht mit Einbau, sondern mit Betrieb, Wartung und späterem erneuten Rückbau.

## Quellen

- VDI 6200: Standsicherheit von Bauwerken — regelmäßige Überprüfung; Bewertungs- und Handlungsanleitungen für Bestands- und Neubauten. https://www.vdi.de/en/home/vdi-standards/details/vdi-6200-standsicherheit-von-bauwerken-regelmaessige-ueberpruefung
- DIN 1076: Ingenieurbauwerke im Zuge von Straßen und Wegen — Überwachung und Prüfung.
- DIN SPEC 91484:2023-09: Verfahren zur Erfassung von Bauprodukten als Grundlage für Bewertungen des hochwertigen Anschlussnutzungspotenzials vor Abbruch- und Renovierungsarbeiten.
- Senatsverwaltung Berlin: *Leitfaden: Hilfestellung zur Wiederverwendung von Bauprodukten durch öffentliche Akteure im Land Berlin*. https://www.berlin.de/sen/uvk/_assets/umwelt/kreislaufwirtschaft/projekte/re-use-von-bauteilen/leitfaden-wiederverwendung-bauprodukte.pdf
- Ministerium für Landesentwicklung und Wohnen Baden-Württemberg / KIT / TUM: *Leitfaden zur Wiederverwendung tragender Bauteile*, 2025. https://mlw.baden-wuerttemberg.de/fileadmin/redaktion/m-mlw/intern/Dateien/06_Service/Publikationen/Bauen_und_Wohnen/2025-04-30-MLW_Broschuere_TragendeBauteile-BF_LNF.pdf
- DGNB: *Das DGNB System für den Gebäuderückbau*. https://www.dgnb.de/de/zertifizierung/gebaeude/rueckbau
- DGNB: *Rückbau- und Recyclingfreundlichkeit*, TEC1.6. https://www.dgnb.de/filestorages/Downloads_unprotected/dokumente/kriterien/dgnb-kriterium-tec1-6-innenraeume-version-2018.pdf
- UBA: *Instrumente zur Wiederverwendung von Bauteilen und hochwertigen Verwertung von Baustoffen*, Texte 93/2015. https://www.umweltbundesamt.de/sites/default/files/medien/378/publikationen/texte_93_2015_wiederverwertung_von_bauteilen_0.pdf
- BAM: *Neues Leben für alten Beton: Forschung zur Wiederverwendung von Betonbauteilen gestartet*, 2025. https://www.bam.de/Content/DE/Pressemitteilungen/2025/Umwelt/2025-06-11-sfb-wiederverwendung-bestandsbauwerke.html
- Eurocode-Grundlagen: DIN EN 1990; materialbezogene Eurocodes DIN EN 1992, DIN EN 1993, DIN EN 1995, DIN EN 1996.
- Bewertungssystem Nachhaltiges Bauen (BNB), Modul Komplettmodernisierung, insbesondere Risiken für lokale Umwelt und Bestandsbewertung.

