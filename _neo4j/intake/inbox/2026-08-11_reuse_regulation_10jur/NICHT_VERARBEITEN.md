# Nicht verarbeitet

Was erhoben, aber bewusst nicht in die Plattform-Ableitung (semio `temp/regulierung-*.md`) übernommen wurde, was nie erhoben wurde, und was noch offen ist. Diese Datei ist die Gegenprobe zu `README.md` — sie macht die Grenzen dieses Intakes explizit, statt sie stillschweigend zu lassen.

---

## Erhoben, aber bewusst nicht ausgewertet

| Was | Begründung |
|---|---|
| Achse D (Rechtsform-Ordinalrang) | Projektkonvention der formellen Verbindlichkeit, **keine Rechtshierarchie** (`schema/taxonomie-final.md` Abschnitt 4 stellt das selbst klar) — als Auswahlfeld im Wizard würde die Ordinalstellung als Verbindlichkeitsrangfolge missverstanden. |
| A-Ursprung, Downstream-Verifikationsstatus | Kodier-Feingliederung der Erhebung selbst (trennt Erarbeitungs- von Bindungsebene), keine Bauteil- oder Dokumenteigenschaft — für die Plattform nicht direkt nutzbar. |
| Konfidenz (gesichert/abgeleitet/unklar) | Redundant zu Beleg-Quelle B0–B4 — beide Felder bewerten dieselbe Belastbarkeit aus unterschiedlichem Blickwinkel; für die Plattform-Ableitung wurde durchgängig nur Beleg-Quelle/Zugänglichkeit geführt. |
| Feld 5b Anreize/Förderung | Veraltet zu schnell (Förderprogramme, Zuschüsse) für eine als Auswahlliste gedachte Ableitung — ein Wizard-Feld, das auf ein bereits ausgelaufenes Förderprogramm verweist, ist irreführender als ein fehlendes Feld. |
| Versicherung | Nur verstreute Erwähnungen ohne eigene Primärquelle im Korpus (z. B. `REG-FR-7-002` Code des assurances Art. L241-1 als Einzelfund) — zu dünn für eine belastbare Achse oder ein eigenes Artefakt. |

---

## Nie erhoben (gestrichen 2026-08-14)

**Arbeitspaket W3b komplett** (6 Agenten: Haftung, Versicherung, Vergabe, grenzüberschreitend, Denkmal-/Bestandsschutz, Steuer) — **ersatzlos gestrichen**, nicht nachgeholt.

Begründung: Der F1-3/F4-7-Split der Länderextraktion (W2) deckt die dort vorgesehenen Regelungsfelder 5a, 5b, 6 und 7 bereits ab, sodass ein eigenes Querschnitts-Arbeitspaket redundant gewesen wäre. Belege dafür im vorliegenden Korpus:

- **51 Feld-7-Objekte** (Haftung/Gewährleistung) über alle 10 Länder + EU verteilt, u. a. `REG-EU-7-101` (Produkthaftungs-RL 2024/2853, Refurbisher-Herstellerfiktion) in `eu-haftung-vergabe.md`.
- **58 Feld-5-Objekte** (Vergabe/Anreize) über alle 10 Länder + EU verteilt.
- **Denkmal-/Bestandsschutz**: 77 Fundstellen, u. a. in `DE-LBO.md` (Bestandsschutz-/Umbauordnungs-Objekte der 16-Länder-Stichprobe).
- **Grenzüberschreitend**: `REG-EU-3-007` (Abfallverbringung) bereits im regulären W2-Abfallrecht-Zweig erfasst.

Diese Lücken sind absichtlich — kein Erhebungsversäumnis, sondern eine bewusste Entscheidung gegen doppelte Struktur.

---

## Gestoppte Auswertung

Die folgenden, ursprünglich in W4 vorgesehenen Syntheseschritte wurden **nicht** durchgeführt:

- W4 Konfliktanalyse/Relationen-Synthese (über die Arbeitsmenge hinaus — für die 35er-Arbeitsmenge liegt eine Teilauswertung in `regulierung-belege.md`/`regulierung-plattformbezug.md` vor, für den Gesamtkorpus nicht)
- Lückenmatrix (Gesamtkorpus)
- Diagrammdaten — **7 von 8 geplanten Diagrammen fehlen**; nur die Nachweis-Matrix E×G wurde gezogen (`regulierung-achsen.md`, Abschnitt „Nachweis-Matrix E × G", Basis 470 Objekte)
- Quellenregister (Gesamtkorpus-Fassung; ein Auszug für die 35er-Arbeitsmenge liegt implizit in den Prüfvermerken von `regulierung-belege.md` vor)
- Schlussredaktion (Gesamtkorpus)
- CH-Quellen-Retry (der ursprünglich per Safety-Classifier blockierte `quellen:CH`-Lauf wurde nicht erneut versucht — CH-Extraktion und -Prüfung liefen unabhängig davon erfolgreich)
- Vault-Seeding in `mit-bestand/recherche/` (die semio-eigene Wissensbasis außerhalb dieses Intakes)
- **Phase B** (LaTeX-Anlage „RG" + TikZ-Diagramme im Zwischenbericht) — **keine Anlage RG im Zwischenbericht.** Kein `.tex`, kein Eintrag in `zwischenbericht.tex`.

---

## Offener Punkt

**Vier kostenpflichtige Normen sind für die Materialzeiger (`regulierung-material-zeiger.md`) ungelesen:**

- **SIA 269/2** (Beton, Schweiz)
- **CROW-CUR 4:2023** (Beton, Niederlande)
- **DS 11990:2024** (Beton, Dänemark)
- **NEN 8700** (Stahlbeton, Niederlande)

Bis zur Beschaffung bleiben die materialbezogenen Nachweisarten für diese vier Fälle **E3** (Projektzuordnung aus Titel/Anwendungsbereich, nicht aus dem Normtext). Das ist ausdrücklich **eine Beschaffungsentscheidung, keine Recherchelücke** — die Fundstellen sind bekannt und benannt, nur der Zugang fehlt.
