# Taxonomie DE — Modell + Muster-Bereich H

Muster zur **Terminologie-Freigabe**. Nach OK generiere ich A–G im selben Stil als `taxonomy_de.jsonl`.
`name` = deutsch, TitleCase, Umlaute transliteriert (ae/oe/ue) wie im Repo (`Witterung_Feuchte`). `barriere_code` bleibt.

---

## Bereich H — Physische_Rueckgewinnung_und_Ausfuehrung (`hb_physische_rueckgewinnung`, Ebene 2)

### H1 — Rueckgewinnbarkeit_durch_Konstruktion · `Recoverability by design` (Kategorie, Ebene 3)
| Code | name (DE) | name_en |
|---|---|---|
| H1.1 | Irreversible_Klebeverbindungen | Irreversible adhesives |
| H1.2 | Unzugaengliche_Befestigungsmittel | Inaccessible fasteners |
| H1.3 | Verbundbauteile | Composite assemblies |
| H1.4 | Verdeckte_Bauteile | Concealed components |
| H1.5 | Zerstoerende_Verbindungen | Destructive connections |
| H1.6 | Nichtstandardisierte_Fuegungen | Nonstandard assemblies |

### H2 — Demontierbarkeit · `Deconstruction feasibility`
| Code | name (DE) | name_en |
|---|---|---|
| H2.1 | Hoher_Arbeitsaufwand | High labor requirement |
| H2.2 | Lange_Demontagedauer | Long dismantling duration |
| H2.3 | Spezialgeraetebedarf | Specialist-equipment requirement |
| H2.4 | Eingeschraenkte_Baustellenzugaenglichkeit | Site-access limitations |
| H2.5 | Sicherheitsrestriktionen | Safety constraints |
| H2.6 | Unvollstaendige_Demontageanleitung | Incomplete dismantling instructions |

### H3 — Rueckgewinnungsausbeute · `Recovery yield`
| Code | name (DE) | name_en |
|---|---|---|
| H3.1 | Beschaedigung_bei_Ausbau | Damage during removal |
| H3.2 | Geringere_Menge_als_geschaetzt | Lower-than-estimated recoverable quantity |
| H3.3 | Kontamination | Contamination |
| H3.4 | Verformung | Deformation |
| H3.5 | Verdeckte_Maengel | Hidden defects |
| H3.6 | Verlust_ergaenzender_Bauteile | Loss of supporting components |

### H4 — Pruef_und_Aufbereitungskapazitaet · `Assessment and preparation capacity`
| Code | name (DE) | name_en |
|---|---|---|
| H4.1 | Unzureichende_Inspektionskapazitaet | Insufficient inspection capacity |
| H4.2 | Unzureichende_Laborkapazitaet | Insufficient laboratory capacity |
| H4.3 | Unzureichende_Pruefkapazitaet | Insufficient testing capacity |
| H4.4 | Unzureichende_Reinigungskapazitaet | Insufficient cleaning capacity |
| H4.5 | Unzureichende_Reparaturkapazitaet | Insufficient repair capacity |
| H4.6 | Unzureichende_Aufarbeitungskapazitaet | Insufficient refurbishment capacity |

### H5 — Lagerfaehigkeit · `Storage capability`
| Code | name (DE) | name_en |
|---|---|---|
| H5.1 | Keine_Lagerkapazitaet | No warehouse capacity |
| H5.2 | Hohe_Lagerkosten | High storage cost |
| H5.3 | Ungeeignete_Lagerbedingungen | Unsuitable storage conditions |
| H5.4 | Lange_Lagerdauer | Long storage duration |
| H5.5 | Erschwerte_Bestandskontrolle | Difficult inventory control |
| H5.6 | Handhabungsschaeden_im_Lager | Handling damage in storage |

### H6 — Transport_und_Handhabung · `Transport and handling`
| Code | name (DE) | name_en |
|---|---|---|
| H6.1 | Lange_Transportdistanz | Long transport distance |
| H6.2 | Hohe_Transportkosten | High transport cost |
| H6.3 | Ueberdimensionierte_Bauteile | Oversized components |
| H6.4 | Spezialtransportbedarf | Specialist transport requirements |
| H6.5 | Schutzverpackungsbedarf | Protective-packaging requirements |
| H6.6 | Handhabungsschaeden | Handling damage |
| H6.7 | Erschwerte_Baustellenanlieferung | Difficult site delivery |

### H7 — Einbau_und_Weiternutzung · `Installation and continued use`
| Code | name (DE) | name_en |
|---|---|---|
| H7.1 | Entwurfsanpassungsbedarf | Design adaptation requirement |
| H7.2 | Erschwerter_Einbau | Difficult installation |
| H7.3 | Fehlende_Einbauanleitung | Missing installation guidance |
| H7.4 | Inkompatible_Schnittstellen | Incompatible interfaces |
| H7.5 | Fehlender_Inbetriebnahmenachweis | Missing commissioning evidence |
| H7.6 | Keine_Lebenszyklus_Aktualisierung_nach_Einbau | No lifecycle-record update after installation |

---

## Zu bestätigende Terminologie-Entscheidungen (gelten dann für A–G)

1. **Umlaut-Transliteration im `name`** (ae/oe/ue) — konsistent mit `Witterung_Feuchte`, `Fehlende_Lagerflaeche`. Lesbares Deutsch mit echten Umlauten steht in `definition_de`.
2. **`interoperability` → `Interoperabilitaet`**, **`matching` → `Matching`** (etablierter Fachbegriff, bleibt), **`Digital Product Passport` → `Digitaler_Produktpass`**.
3. **`governance` → `Verwaltung`/`Governance`?** Vorschlag: Bereich C = `Datenverwaltung_und_Vertrauensinfrastruktur`, aber „Daten-Governance" ist im Fachdeutsch üblich — Alternative `Daten_Governance_und_Vertrauensinfrastruktur`.
4. **`stakeholder` → `Akteur`** (Repo nutzt bereits `:Akteur`).
