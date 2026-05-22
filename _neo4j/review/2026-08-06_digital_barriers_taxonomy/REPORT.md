# Hürden-Taxonomie — Report (knoten- & kantenbasiert)

**2026-08-06 · keine DB-Writes bisher** · Details: [PLAN.md](PLAN.md) · [DROPOUT_REPORT.md](DROPOUT_REPORT.md) · [TAXONOMY_DE.md](TAXONOMY_DE.md)

---

## Prinzip
Alles als **Knoten + Beziehung**, nichts Wichtiges in Properties. Für jede Guide-Dimension zuerst einen **bestehenden** Knotentyp nutzen; neu nur, wo keiner existiert. Der Graph hatte das Muster schon: `(:Huerde)-[:HAT_HUERDEKATEGORIE]->(:HuerdeKategorie)` — heute flach; wird reaktiviert und vertieft.

## Hierarchie (2 vorhandene Labels, 1 vorhandene Kante)
```
(:Huerde h_*)  ──HAT_HUERDEKATEGORIE──▶  (:HuerdeKategorie huek_*)  ──HAT_HUERDEKATEGORIE──▶  (:HuerdeKategorie …A–H)
   Blatt ~330                                Familie/Gruppe ~55                       Bereich (kein Elternteil) 8
```
Ebene = Baumposition, keine Property. Kein neues Label/Kante für die Struktur.

## Wiederverwendung statt Properties
| Guide | Vorhandener Knoten | Kante |
|---|---|---|
| hat Hürde | :Projekt / :Bauteilgruppe | HAT_HUERDE *(bestehend, 237 bleiben)* |
| Quelle | :Quelle | (:Huerde)-[:BELEGT_IN]->(:Quelle) |
| Reuse-Phase | :Prozessphase (10) | (:Huerde)-[:BETRIFFT_PHASE]-> |
| Stakeholder | :Akteurrolle (22) | (:Huerde)-[:BETRIFFT_ROLLE]-> |
| Standard | :Norm (103) | (:Norm)-[:ADRESSIERT]->(:Huerde) |
| Rechtsfrage | :Regulierungsfrage (11) | (:Huerde)-[:TRIGGERS_REGULIERUNGSFRAGE]-> *(Kante bestehend)* |
| Hürde→Hürde | :Huerde | VERURSACHT / VERSTAERKT / ERMOEGLICHT / MINDERT *(nur ~40 belegte)* |

## Genuin neu (nichts Passendes im Graph)
| Neu | Anzahl | Kante | warum |
|---|---:|---|---|
| :Plattformfunktion `pf_*` | ~23 | (:Huerde)-[:BEEINTRAECHTIGT]-> | Bauteilportal-Kern, kein Äquivalent |
| :Massnahme `mn_*` *(opt.)* | ~12 | (:Massnahme)-[:MINDERT]->(:Huerde) | Gegenmaßnahmen §5 |
| :Evidenzstatus / :Digitalbezug *(oder Property)* | 3 / 3 | HAT_EVIDENZSTATUS / HAT_DIGITALBEZUG | analog :Status, :ZustandsKlasse |

## Konsistenz-Garantie
Keine 400×N erfundenen Kanten. Gesetzt werden nur: volle Hierarchie · ~40 Querverweise · Quellen-Belege · benannte Plattformfunktions-Kanten · 237 umgehängte HAT_HUERDE. Phase/Rolle/Norm-Kanten nur bei Quellenbeleg, sonst als spätere Anreicherung markiert.

## Wegfall — 0 Datenverlust
11 flache :Huerde (nach Umhängen gelöscht) · `category`-Strings (ersetzt durch Bereiche A–H) · `HAT_HUERDEKATEGORIE` als 0-Instanz-Müll (reaktiviert mit echten Knoten) · **237 Kanten: 0 verloren**.

## Offene Freigaben
1. Terminologie am Muster **Bereich H** (Umlaut-Regel, Bereich-C-Name).
2. `:Evidenzstatus`/`:Digitalbezug` als **Knoten** (Repo-konsequent) oder Property (schlanker)?
3. `:Massnahme` in **Phase 1** mit rein oder als Phase 2?
4. Die 5 unscharfen Anker aus [DROPOUT_REPORT.md](DROPOUT_REPORT.md) bestätigen.
