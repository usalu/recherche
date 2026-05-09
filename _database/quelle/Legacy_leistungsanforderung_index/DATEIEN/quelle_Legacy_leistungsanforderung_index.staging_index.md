---
id: "Legacy_leistungsanforderung_index."
entity: "quelle"
node_kind: "source"
migration_status: "migrated_phase5_legacy_source"
title: "Leistungsanforderungen – Index"
legacy_path: "leistungsanforderung\\index.md"
migration_action: "merge_into_index"
legacy_type: "Leistungsanforderung"
target_primary: "leistungsanforderung/index"
target_secondary: ""
risk_flags: "index_content_may_contain_unique_gaps_or_cluster_lists"
---
# Leistungsanforderungen – Index

## Migration

- Legacy path: leistungsanforderung\index.md
- Action in migration map: merge_into_index
- Reason: not already consumed by phase 1-4, so preserved as source/meta node.
- Original primary target: leistungsanforderung/index
- Original secondary targets: 

## Legacy Content

---
type: Leistungsanforderung
pruefung: ["[[pruefung/Statische_Nachweisfuehrung]]"]
verwandt: ["[[leistungsanforderung/Schadstofffreiheit]]"]
---

# Leistungsanforderungen – Index

## Verknüpfungen

- [pruefung/](../pruefung/) – Leistungsanforderungen werden durch Prüfungen nachgewiesen: Tragfähigkeit durch statische Nachweisführung und Zugversuch, Brandschutz durch Brandnachweis, Schadstofffreiheit durch Schadstoffscreening.
- [standard/](../standard/) – Leistungsanforderungen sind in Normen definiert: DIN EN 1990–1999 für Tragfähigkeit, DIN 4109 für Schallschutz, GEG/DIN 4108 für Wärmeschutz, DIN EN 13501 für Brandschutz.
- [recht/](../recht/) – Leistungsanforderungen sind bauordnungsrechtlich verbindlich; ihre Erfüllung ist Voraussetzung für Baugenehmigung und Verwendbarkeitsnachweis.
- [material/](../material/) — Leistungsanforderungen sind materialabhängig: Holz hat andere Brandschutz- und Tragfähigkeitscharakteristika als Stahl oder Beton; gebrauchte Materialien können gealtert, vorgeschädigt oder unbekannt sortiert sein.
- [bauteil/](../bauteil/) — Leistungsanforderungen gelten auf Bauteilebene: Fenster müssen Wärmeschutzwerte erfüllen, Stützen Tragfähigkeit, Feuerschutztüren Feuerwiderstand.
- [schadstoff/](../schadstoff/) — Schadstofffreiheit als Leistungsanforderung ist eng mit der Schadstoffkategorie verknüpft: Asbest, PCB, PAK, Holzschutzmittel und andere Gefahrstoffe können Wiederverwendung ausschließen.

---

## Kurzüberblick zur Kategorie

Diese Kategorie dokumentiert die technischen und bauordnungsrechtlichen Leistungsanforderungen, die an Bauteile im Kontext der Wiederverwendung gestellt werden. Leistungsanforderungen sind nicht optional: Sie gelten unabhängig davon, ob ein Bauteil neu ist oder gebraucht. Im Reuse-Kontext verschiebt sich das Problem: Bei neuen Produkten werden Anforderungen durch Normung, CE-Kennzeichnung und Herstellerdokumentation abgedeckt. Bei gebrauchten Bauteilen müssen sie oft durch Prüfung, Gutachten oder Einzelfallzulassung neu nachgewiesen werden.

---

## Zentrale Unterthemen

- **Sicherheitsrelevante Anforderungen:** Tragfähigkeit und Brandschutz als bauordnungsrechtlich zwingende Schutzziele; bei tragenden und raumabschließenden Bauteilen besonders hoch.
- **Gesundheitsbezogene Anforderungen:** Schadstofffreiheit und Feuchteschutz schützen Nutzerinnen und Nutzer; bei Bestandsbauteilen aus früheren Bauphasen besonders kritisch.
- **Komfort- und Energieanforderungen:** Schallschutz und Wärmeschutz; beeinflussen Nutzungsqualität und Energiebilanz; häufig Konfliktfeld zwischen Bestandserhalt und heutigen Mindeststandards.
- **Dauerhaftigkeit:** Restlebensdauer und Nutzungsdauer als übergreifende Anforderung; bei gebrauchten Bauteilen ist ein Teil der Lebensdauer bereits verbraucht.
- **Rückbaubarkeit:** Als spezifische ReUse-Anforderung, die nicht nur den aktuellen Einbau betrifft, sondern die spätere Demontierbarkeit für einen weiteren Nutzungszyklus.

---

## Wichtige Dateien dieser Kategorie

- [Tragfaehigkeit.md](Tragfaehigkeit.md) — Nachweis, dass ein Bauteil unter neuen statischen Einwirkungen und für eine weitere Nutzungsdauer ausreichend sicher ist. Bei gebrauchten tragenden Bauteilen erfordert das Materialprüfungen, Zustandsbewertung und oft Einzelfallzulassung. Hohes CO₂-Einsparpotenzial rechtfertigt den Prüfaufwand.

- [Brandschutz.md](Brandschutz.md) — Bauordnungsrechtliche Anforderung für Verhalten von Bauteilen im Brandfall: Feuerwiderstand, Nichtbrennbarkeit oder definierte Brennbarkeit, Rauchdichtheit. Bei gebrauchten Bauteilen fehlen häufig Klassifizierungsberichte und Prüfzeugnisse; gutachterliche Stellungnahmen oder neue Brandprüfungen werden notwendig.

- [Schadstofffreiheit.md](Schadstofffreiheit.md) — Nachgewiesene Abwesenheit oder kontrollierte Unterschreitung gesundheits-, arbeits- und umweltrelevanter Schadstoffe. Kritischste Anforderung bei Bestandsbauteilen aus dem 20. Jahrhundert: Asbest, PCB, PAK, Holzschutzmittel und weitere Altlasten können Wiederverwendung vollständig ausschließen.

- [Dauerhaftigkeit.md](Dauerhaftigkeit.md) — Fähigkeit eines Bauteils, die geforderten Leistungen während einer definierten Restnutzungsdauer zu erfüllen. Nicht „alt gleich haltbar", sondern belastbare Restlebensdaueranalyse mit Prüfung, ISO 15686, Instandhaltungskonzept und materialspezifischer Expositionsbewertung.

- [Feuchteschutz.md](Feuchteschutz.md) — Schutz vor Wasser, Feuchte, Dampf und Kondensation über Einbau und Nutzung hinweg. Gebrauchte Bauteile bringen eine Feuchtegeschichte mit: Versalzung, mikrobielle Belastung, frühere Beschichtungen können im neuen Einbau problematisch werden.

- [Schallschutz.md](Schallschutz.md) — Anforderung an die Dämmwirkung von Bauteilen gegen Luft- und Trittschall. Besonders systemabhängig: Ein Bauteil mit guten Laborwerten kann im neuen Gebäude durch ungünstige Anschlüsse und Flankenwege versagen. Prüfung im eingebauten Zustand oft notwendig.

- [Waermeschutz.md](Waermeschutz.md) — Begrenzung von Wärmeverlusten und sommerlicher Überhitzung. Gebrauchte Bauteile erfüllen heutige energetische Anforderungen oft nicht ohne Ergänzung; gleichzeitig ist der Ersatz alter Bauteile durch neue Hochleistungsprodukte ökologisch nicht immer sinnvoll.

- [Rueckbaubarkeit.md](Rueckbaubarkeit.md) — Planbare Eigenschaft von Entwurf, Bauteil und Verbindung, die selektive, wirtschaftliche Demontage ermöglicht. Anforderung, die bereits beim ersten Einbau gestellt wird, um spätere Wiederverwendung zu ermöglichen. Verknüpft mit ISO 20887 und DfD-Entwurfsprinzipien.

---

## Querverbindungen zu anderen Kategorien

- **Prüfung:** Jede Leistungsanforderung hat eine zugehörige Prüfkategorie; Tragfähigkeit → statische Nachweisführung und Zugversuch; Brandschutz → Brandnachweis und Abbrandbemessung; Schadstofffreiheit → Schadstoffscreening.
- **Standard:** Normen definieren den Zahlenwert der Anforderung und das Verfahren zum Nachweis; ohne Norm ist die Anforderung nicht operationalisierbar.
- **Recht:** Leistungsanforderungen sind öffentlich-rechtlich verbindlich; ihre Nichterfüllung führt zur Verweigerung der Baugenehmigung oder zu bauaufsichtlichen Maßnahmen.
- **Material:** Materialspezifische Charakteristika bestimmen, wie eine Leistungsanforderung nachzuweisen ist; Holz, Stahl, Beton und Lehm haben grundlegend unterschiedliche Prüf- und Nachweislogiken.
- **Bauteil:** Leistungsanforderungen werden auf Bauteilebene spezifiziert und geprüft; Fenster, Stütze, Fassade und Decke haben je eigene Anforderungskombinationen.
- **Hürde:** Unerfüllte oder nur mit hohem Aufwand erfüllbare Leistungsanforderungen sind strukturelle Hürden für Wiederverwendung; besonders Brandschutz und Schadstofffreiheit führen häufig zum Ausschluss wertvoller Bauteile.

---

## Offene Lücken / Ausbaufelder

- **Gebrauchstauglichkeit:** Als eigenständige Leistungsanforderung (Verformung, Schwingung, Rissbreite) ist sie bisher nicht dokumentiert; sie ist für tragende Bauteile neben der Tragfähigkeit ebenso relevant.
- **Barrierefreiheit:** Nutzungsqualitätsbezogene Anforderung bei Umnutzung und Bestandsumbau; nicht als Leistungsanforderungsdatei vorhanden.
- **Luftdichtheit:** Als bauphysikalische Anforderung bei Aufstockungen und Fassadenertüchtigungen relevant; im Wärmeschutz erwähnt, aber nicht als eigenständiges Thema dokumentiert.
- **Robustheit:** Anforderung an außergewöhnliche Einwirkungen (Anprall, Explosionsdruck); in `pruefung/Statische_Nachweisfuehrung.md` erwähnt, fehlt als Leistungsanforderungsdatei.
- **Innenraumhygiene:** Emissionsanforderungen an Bauteile und Oberflächen im Innenraum; in `leistungsanforderung/Schadstofffreiheit.md` erwähnt, aber nicht separat ausgearbeitet.
