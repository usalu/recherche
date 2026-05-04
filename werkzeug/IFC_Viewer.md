## Verknüpfungen

- **Übergeordnete Themen:** openBIM; IFC; Modellprüfung; Bestandsmodell; Datenqualität; Materialpass; Kollaboration.
- **Verwandte Dateien:** `werkzeug/BIM.md`; `werkzeug/Madaster_Plattform.md`; `werkzeug/Rhino.md`; `datenmodell/IFC.md`; `datenmodell/IDS.md`; `datenmodell/BCF.md`; `werkzeug/Materialdatenbank.md`; `methode/BIM_Modellpruefung.md`; `methode/Bauteilkatalogisierung.md`.
- **Relevante Akteure / Fallstudien / Materialien / Standards / Methoden:** buildingSMART; IFC2x3; IFC4; IFC4.3; BCF; IDS; bSDD; BIMcollab ZOOM; Solibri; BlenderBIM / Bonsai; xBIM; web-ifc / IFC.js; Madaster Smart Views; BIM-Koordination; Model Checking.

## Kurzdefinition

Ein IFC-Viewer ist ein Werkzeug zur Anzeige, Navigation, Auswertung und teilweise Prüfung von IFC-Dateien. IFC steht für Industry Foundation Classes und ist ein offener Standard für den Austausch von BIM-Daten. Ein IFC-Viewer ist kein vollwertiges BIM-Autorensystem: Er dient primär dazu, Modelle softwareunabhängig sichtbar, kontrollierbar, filterbar und kommentierbar zu machen.

Für Wiederverwendung ist der IFC-Viewer ein Prüf- und Übersetzungswerkzeug zwischen BIM-Modell, Materialpass, Audit, LCA, Plattform und Planung. Er zeigt, ob ein Modell die notwendigen Bauteile, Mengen, Materialinformationen, Klassifikationen und Property-Sets tatsächlich enthält.

## Relevanz für Wiederverwendung im Bauwesen

Wiederverwendung verlangt belastbare Informationen über Bauteile. IFC-Viewer helfen, diese Informationen aus Modellen zu prüfen, ohne an die Autorensoftware gebunden zu sein. Sie sind besonders relevant, wenn Bestandsmodelle, Scan-to-BIM-Modelle oder Neubauplanungen an Materialpassplattformen, Rückbauplaner oder Auftraggeber übergeben werden.

Wichtige Funktionen:

- Sichtprüfung, ob Bauteile korrekt modelliert und räumlich auffindbar sind.
- Kontrolle von Mengen, Base Quantities, Materialien und Klassifikationen.
- Filterung nach Materialgruppen, Geschossen, Bauteilarten oder Property-Sets.
- Prüfung, ob zirkuläre Datenfelder vorhanden sind.
- Export von Listen für Audits, Materialpässe oder Plattformimporte.
- BCF-Kommunikation zu fehlenden oder fehlerhaften Angaben.
- Vorbereitung von IFC-Dateien für Madaster, LCA, Ressourcenpass oder Koordination.

## Fachinhalt

### Abgrenzung der Ebenen

- **IFC:** Datenstandard und Dateiinhalt.
- **IFC-Viewer:** Werkzeug zur Darstellung, Navigation und Prüfung.
- **BIM-Autorensoftware:** erzeugt und bearbeitet Modelle, z. B. Revit, Archicad, Vectorworks, Tekla, Rhino/VisualARQ.
- **Model Checker:** spezialisierte Prüfung von Regeln, Normen, Kollisionen, Informationsanforderungen und Klassifikationen. Manche Viewer enthalten Checker-Funktionen.
- **Materialpassplattform:** verarbeitet Modellinformationen weiter, ergänzt Datenbanken und erstellt Auswertungen.

Diese Unterscheidung ist wichtig, weil ein Modell in einem Viewer sichtbar sein kann, aber dennoch für Wiederverwendung unbrauchbar bleibt, wenn Material-, Mengen- oder Demontagedaten fehlen.

### IFC-Daten, die für Wiederverwendung relevant sind

- **IfcElement / IfcBuildingElement:** Wände, Decken, Stützen, Träger, Fenster, Türen, Dächer, Platten, Treppen, Geländer.
- **IfcMaterial / IfcMaterialLayerSet / IfcMaterialProfileSet:** Material- und Schichtinformationen.
- **Base Quantities:** Länge, Fläche, Volumen, Masse soweit vorhanden oder ableitbar.
- **Psets:** Eigenschaftssätze, z. B. Brandschutz, Schallschutz, Tragfähigkeit, Herstellerdaten, eigene Re-Use-Property-Sets.
- **Classification References:** DIN 276, Uniclass, Omniclass, eBKP, NL/SfB oder projektspezifische Klassifikationen.
- **Spatial Structure:** Projekt, Standort, Gebäude, Geschoss, Raum; wichtig für Ausbauort und Logistik.
- **Relationships:** Aggregationen, Typzuordnung, Materialzuordnung, Verbindungen teilweise begrenzt.
- **GUIDs:** eindeutige Objektkennungen; wichtig für Nachverfolgung, aber nur stabil, wenn sauber modelliert und nicht ständig neu exportiert.

### Prüffragen im IFC-Viewer

Für Wiederverwendung sollte ein IFC-Viewer u. a. folgende Fragen beantworten:

- Sind potenziell wiederverwendbare Bauteile als eigene Objekte modelliert oder nur als generische Massen?
- Gibt es Materialinformationen auf Bauteil- oder Schichtebene?
- Sind Mengen vollständig und plausibel?
- Ist das Bauteil einem Geschoss, Raum oder Gebäudeteil zugeordnet?
- Gibt es eine eindeutige Klassifikation?
- Sind Hersteller, Typ, Baujahr, Produktdaten oder Nachweise enthalten?
- Sind Demontierbarkeit, Verbindungstyp, Wiederverwendungsstatus oder Schadstoffhinweise vorhanden?
- Werden IFC-Property-Sets beim Export korrekt übertragen?
- Können Listen nach Material, Bauteiltyp oder Geschoss exportiert werden?
- Gibt es Abweichungen zwischen Modellgeometrie und Auditdaten?

### Typische Viewer- und Prüfwerkzeuge

- **BIMcollab ZOOM:** IFC-Viewer mit Smart Views, Modellprüfung, BCF-Kommunikation; in Madaster-Workflows für IFC-Vorprüfung relevant.
- **Solibri:** umfangreiche Modellprüfung, Informationsprüfung, Klassifikations- und Kollisionskontrolle.
- **Bonsai / BlenderBIM:** open-source openBIM-Werkzeug mit IFC-orientierter Modellierung und Prüfung.
- **xBIM:** .NET-basierte Bibliothek und Viewer-Ökosystem für IFC-Verarbeitung.
- **web-ifc / IFC.js:** Web-Technologien zur Anzeige und Verarbeitung von IFC im Browser.
- **Open IFC Viewer / andere Desktop-Viewer:** einfache Sichtprüfung und Navigation.

Die Auswahl hängt davon ab, ob nur visualisiert, regelbasiert geprüft, Daten exportiert oder in eigene Web-Workflows integriert werden soll.

### Schnittstellen und Formate

- **IFC2x3 / IFC4 / IFC4.3:** Version und MVD müssen mit Zielplattformen abgestimmt werden.
- **BCF:** Modellkommentare und Issues zwischen Viewer, Autorensoftware und Koordination.
- **IDS:** maschinenlesbare Informationsanforderungen; perspektivisch zentral für Prüfung von Wiederverwendungsdaten.
- **CSV / Excel:** Export von Objektlisten und Mengen; wichtig für Audits und Plattformimporte.
- **JSON / API:** bei Web-Viewern und eigenen Datenpipelines.
- **bSDD:** Verknüpfung von Eigenschaften und Begriffen mit standardisierten Dictionaries.

### Einsatzszenarien

- **Vorprüfung für Madaster:** IFC-Datei auf Klassifikation, Material, Base Quantities und Modellstruktur prüfen.
- **Bestandsaudit:** IFC aus Bestandsmodell mit vor Ort erhobenen Bauteildaten abgleichen.
- **Re-Use-Planung:** verfügbare Bauteile im Modell lokalisieren, Mengenlisten erzeugen und Planungsvarianten prüfen.
- **Rückbau:** Ausbauabschnitte, Geschosse, Bauteilgruppen und Logistikmengen auswerten.
- **Qualitätssicherung:** fehlende Materialangaben oder falsche Klassifikationen als BCF-Issues zurück an Modellautoren geben.
- **Forschung:** Modellqualität verschiedener Projekte vergleichbar bewerten.

### Grenzen

- IFC-Viewer sehen nur, was im IFC enthalten ist; fehlende Informationen können nicht verlässlich rekonstruiert werden.
- Material- und Mengenangaben können durch Exportfehler, Modellierungsfehler oder Software-Mapping verfälscht sein.
- Demontierbarkeit, Verbindungstypen und Schadstoffe sind in gewöhnlichen IFC-Modellen selten ausreichend abgebildet.
- Bauteilzustand und Restlebensdauer müssen meist extern erhoben werden.
- Große IFC-Dateien können Performanceprobleme verursachen.
- Unterschiedliche Viewer interpretieren IFC teils verschieden.
- Viewer ersetzen keine bauaufsichtliche, statische, brandschutztechnische oder schadstoffbezogene Prüfung.

## Praxisbezug / Beispiele

- **Madaster-Smart-View-Prüfung:** Vor Upload einer IFC-Datei kann mit BIMcollab ZOOM und Smart Views kontrolliert werden, ob Klassifikationscodes, Mengen und Materialien ausreichend vorhanden sind.
- **Türen- und Fensterinventar:** Ein Viewer filtert alle `IfcDoor`- und `IfcWindow`-Objekte nach Geschoss, Typ und Material. Für Re-Use müssen anschließend Zustand, Beschläge, Brandschutzklassifizierung, Maße und Ausbauaufwand ergänzt werden.
- **Stahltragwerk:** `IfcBeam` und `IfcColumn` können nach Profiltyp und Länge ausgewertet werden. Für Wiederverwendung bleiben Stahlgüte, Korrosion, Bohrungen, Schweißnähte und Prüfzeugnisse kritisch.
- **Innenausbau:** Doppelböden, Systemtrennwände und Leuchten sind oft als Familien/Objekte erfassbar. Für Marktfähigkeit sind Stückzahl, Serie, Oberflächenzustand und Ersatzteilverfügbarkeit wichtig.
- **Rückbauphasen:** Über Geschoss- und Zonenfilter lassen sich Ausbaupakete vorbereiten; genaue Demontagereihenfolgen müssen aber meist außerhalb des IFC-Viewers geplant werden.

## Herausforderungen / offene Fragen

- Wie werden Re-Use-spezifische Properties standardisiert und zuverlässig exportiert?
- Können IDS-Regeln Mindestdaten für Wiederverwendung projektübergreifend prüfbar machen?
- Wie werden Qualität, Unsicherheit und Prüfstatus im IFC-Viewer sichtbar?
- Wie lassen sich Fotos, Prüfberichte, QR-Codes und physische Bauteilkennzeichnungen stabil mit IFC-Objekten verbinden?
- Welche IFC-Version und welche Property-Sets sind für Materialpassplattformen langfristig am robustesten?
- Wie können Viewer von reiner Sichtprüfung zu belastbarer zirkulärer Modellprüfung weiterentwickelt werden?
- Wie wird verhindert, dass geometrische Modellqualität mit Wiederverwendungsfähigkeit verwechselt wird?

## Quellen

- buildingSMART International: Industry Foundation Classes / IFC, https://www.buildingsmart.org/standards/bsi-standards/industry-foundation-classes/
- buildingSMART International: BIM Collaboration Format / BCF, https://www.buildingsmart.org/standards/bsi-standards/bcf/
- buildingSMART International: Information Delivery Specification / IDS, https://www.buildingsmart.org/standards/bsi-standards/information-delivery-specification-ids/
- buildingSMART Data Dictionary / bSDD, https://www.buildingsmart.org/users/services/buildingsmart-data-dictionary/
- Madaster Documentation: Preparing BIM IFC source files, https://docs.madaster.com/us/en/knowledge-base/preparing-bim-ifc-source-files
- BIMcollab ZOOM, https://www.bimcollab.com/en/products/bimcollab-zoom/
- Solibri Office / Model Checking, https://www.solibri.com/
- Bonsai / BlenderBIM, https://bonsaibim.org/
- xBIM Toolkit, https://docs.xbim.net/
- web-ifc / IFC.js, https://ifcjs.github.io/info/
