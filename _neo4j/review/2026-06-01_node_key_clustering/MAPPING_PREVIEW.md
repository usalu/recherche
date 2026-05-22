# Phase L mapping preview (review before apply)


## pollutant_risks -> HAS_RISK_POLLUTANT  (43 tokens mapped, 6 residual)

- `Asbestos` -> s_asbest
- `Asbestos adhesives` -> s_asbest
- `Asbestos backing/mastic` -> s_asbest
- `Asbestos coatings/tiles` -> s_asbest
- `Asbestos contamination` -> s_asbest
- `Asbestos dust` -> s_asbest
- `Asbestos dust from mixed demolition` -> s_asbest
- `Asbestos fireproofing` -> s_asbest
- `Asbestos spacers/coatings` -> s_asbest
- `Asbestos-containing mortars/adhesives` -> s_asbest, s_pak
- `CCA` -> s_holzschutzmittel
- `Cadmium/galvanic coatings` -> s_schwermetalle
- `Chlorides` -> s_chlorid
- `Coatings with lead/chromate/PAH` -> s_bleifarbe, s_pak, s_schwermetalle
- `Creosote` -> s_holzschutzmittel
- `Formaldehyde` -> s_formaldehyd
- `Heavy metals` -> s_schwermetalle
- `Lead paint` -> s_bleifarbe
- `Lead paint/glaze` -> s_bleifarbe
- `Lead/chromate coatings` -> s_bleifarbe, s_schwermetalle
- `Lead/chromate paint` -> s_bleifarbe, s_schwermetalle
- `Lead/chromate/PAH coatings` -> s_bleifarbe, s_pak, s_schwermetalle
- `Lindane` -> s_holzschutzmittel
- `Mineral oil contamination` -> s_mineraloel
- `Mold` -> s_schimmel
- `Mold/moisture` -> s_schimmel
- `Oil contamination` -> s_mineraloel
- `Oil/heavy metals` -> s_mineraloel, s_schwermetalle
- `Oils` -> s_mineraloel
- `PAH` -> s_pak
- `PAH coatings` -> s_pak
- `PAH membranes` -> s_pak
- `PAH waterproofing` -> s_pak
- `PAH/tar` -> s_pak
- `PAH/tar adhesives` -> s_pak
- `PAH/tar membranes` -> s_pak
- `PCB` -> s_pcb
- `PCB joints` -> s_pcb
- `PCB sealants` -> s_pcb
- `PCP` -> s_holzschutzmittel
- `PCP/lindane` -> s_holzschutzmittel
- `Salts` -> s_salze
- `Wood preservatives` -> s_holzschutzmittel

**Residual (kept as-is, no edge):** Chemical coatings; Insulation contamination; Old fireproofing; Old paints; Organic contamination; Soot

## required_tests -> HAT_PRUEFUNG  (79 tokens mapped, 29 residual)

- `Anchor condition` -> pn_ankerpruefung
- `Anchor-pullout for cladding` -> pn_ankerpruefung
- `Anchorage` -> pn_ankerpruefung
- `Batch grouping by provenance and execution class` -> pr_dokumentenpruefung_bestand
- `Bending/shear load tests` -> pr_statische_nachweisfuehrung
- `Biological attack` -> pn_faeulnis_sichtpruefung
- `Carbonation` -> pn_karbonatisierung
- `Carbonation threshold` -> pn_karbonatisierung
- `Carbonation/chloride` -> pn_chlorid, pn_karbonatisierung
- `Charpy where relevant` -> pn_kerbschlag
- `Chloride` -> pn_chlorid
- `Coating/fire proofing records` -> pr_brandschutznachweis
- `Compressive strength` -> pn_druckfestigkeit
- `Cores` -> pn_bohrkern_druckfestigkeit
- `Cores/rebound/UPV` -> pn_bohrkern_druckfestigkeit, pn_rueckprallhammer, pn_ultraschall
- `Corrosion` -> pn_rostgrad
- `Cover` -> pn_bewehrungsscan
- `Cover scan` -> pn_bewehrungsscan
- `Cover/rebar scan` -> pn_bewehrungsscan
- `Crack mapping` -> pn_risskartierung
- `Crack/damage` -> pn_risskartierung
- `Cracking after handling` -> pn_risskartierung
- `Cracks` -> pn_risskartierung
- `Cracks after each handling stage` -> pn_risskartierung
- `Cracks/delamination` -> pn_risskartierung
- `Decay` -> pn_faeulnis_sichtpruefung
- `Decay/insect attack` -> pn_faeulnis_sichtpruefung
- `Density/stiffness NDT` -> pn_dichte, pr_zerstoerungsfreie_pruefung
- `Dimensional stability` -> pr_geometrische_vermessung
- `Dimensions` -> pr_geometrische_vermessung
- `Drawings/provenance` -> pr_dokumentenpruefung_bestand
- `Existing weld NDT` -> pr_zerstoerungsfreie_pruefung
- `Fire` -> pr_brandschutznachweis
- `Fire damage` -> pr_brandschutznachweis
- `Fire exposure` -> pr_brandschutznachweis
- `Fire history` -> pr_brandschutznachweis
- `Fire performance` -> pr_brandschutznachweis
- `Fire/charring` -> pr_brandschutznachweis
- `Flexural` -> pn_biegezug
- `Flexural strength` -> pn_biegezug
- `Geometry` -> pr_geometrische_vermessung
- `Geometry/tolerances` -> pr_geometrische_vermessung
- `Grade` -> pr_festigkeitssortierung_holz
- `HCS dimensions` -> pr_geometrische_vermessung
- `Insect attack` -> pn_faeulnis_sichtpruefung
- `Load path` -> pr_statische_nachweisfuehrung
- `Load test` -> pr_statische_nachweisfuehrung
- `Load test where needed` -> pr_statische_nachweisfuehrung
- `Load testing` -> pr_statische_nachweisfuehrung
- `Mechanical testing` -> pr_materialpruefung
- `Mechanical tests` -> pr_materialpruefung
- `Moisture` -> pn_feuchtemessung
- `Moisture sorption` -> pn_feuchtemessung
- `NDT of welds` -> pr_zerstoerungsfreie_pruefung
- `Petrography` -> pn_petrografie
- `Provenance` -> pr_dokumentenpruefung_bestand
- `Provenance grouping` -> pr_dokumentenpruefung_bestand
- `Reinforcement` -> pn_bewehrungsscan
- `Reinforcement scan` -> pn_bewehrungsscan
- `Reinforcement/prestress detection` -> pn_bewehrungsscan
- `Shear/bending capacity` -> pr_statische_nachweisfuehrung
- `Slip` -> pn_rutschhemmung
- `Slip resistance` -> pn_rutschhemmung
- `Strand location` -> pn_spannlitzenlage
- `Strand/bearing condition` -> pn_spannlitzenlage
- `Strength grading` -> pr_festigkeitssortierung_holz
- `Strength grading/NDT` -> pr_festigkeitssortierung_holz, pr_zerstoerungsfreie_pruefung
- `Strength/weldability` -> pn_schweissbarkeit
- `Visual/NDT grading` -> pn_sichtpruefung, pr_zerstoerungsfreie_pruefung
- `Water absorption` -> pn_wasseraufnahme
- `Weld NDT` -> pr_zerstoerungsfreie_pruefung
- `Weldability` -> pn_schweissbarkeit
- `Weldability tests` -> pn_schweissbarkeit
- `corrosion loss` -> pn_rostgrad
- `fire-protection evidence` -> pr_brandschutznachweis
- `section geometry` -> pr_geometrische_vermessung
- `tensile/yield/elongation` -> pn_zugversuch
- `visual inspection` -> pn_sichtpruefung
- `weldability/CEV` -> pn_schweissbarkeit

**Residual (kept as-is, no edge):** Bearing length; Bearing zones; Bond strength with new mortar; Chemical tests; Clay content; Coatings; Concrete strength; Connection defects; Connection history; Connection-hole damage; End damage; Erosion/water sensitivity; Fastener damage; Fastener-hole damage; Frost; Frost resistance; Grain size; Holes/notches; Microbial contamination; Minimum full-scale testing rule; Previous load/damage; Remaining service life; Same steel test package as UK; Shrinkage; Soluble salts; Species; Stiffness; Strength; Sulfate

## processing_methods -> HAT_AUFBEREITUNG  (54 tokens mapped, 36 residual)

- `Batch grading` -> av_materialsortierung_chargenbildung
- `Batch sorting` -> av_materialsortierung_chargenbildung
- `Blasting/decoating` -> av_beschichtung_entfernen, av_sandstrahlen
- `Careful deconstruction` -> av_zerlegung_vereinzelung
- `Careful dismantling` -> av_zerlegung_vereinzelung
- `Careful salvage` -> av_zerlegung_vereinzelung
- `Classify` -> av_materialsortierung_chargenbildung
- `Clean` -> av_reinigung
- `Cleaning` -> av_reinigung
- `Coating removal` -> av_beschichtung_entfernen
- `Coating renewal` -> av_korrosionsschutz_beschichten
- `Crush` -> av_lehm_sieben_mischen
- `Cut out damaged ends` -> av_zuschnitt
- `Cut-to-size` -> av_zuschnitt
- `Cutting` -> av_zuschnitt
- `De-nail` -> av_entnageln
- `De-nailing` -> av_entnageln
- `Decoat` -> av_beschichtung_entfernen
- `Deconstruction-as-production-process` -> av_zerlegung_vereinzelung
- `Dismantle` -> av_zerlegung_vereinzelung
- `Dismantle by unbolting` -> av_zerlegung_vereinzelung
- `Dismantling` -> av_zerlegung_vereinzelung
- `Drying` -> av_holz_trocknung_feuchtekonditionierung
- `Edge repair` -> av_reparatur
- `End repair` -> av_reparatur
- `Kiln drying` -> av_holz_trocknung_feuchtekonditionierung
- `Mortar removal` -> av_moertelentfernung_ziegel
- `Plane` -> av_hobeln
- `Planing` -> av_hobeln
- `Re-fabrication` -> av_remanufacturing
- `Recoat` -> av_korrosionsschutz_beschichten
- `Reconditioning` -> av_rekonditionierung
- `Refinish` -> av_oberflaechenbehandlung
- `Reform blocks/plasters` -> av_lehm_sieben_mischen
- `Regrade` -> av_holz_festigkeitssortierung
- `Regrading` -> av_holz_festigkeitssortierung
- `Rehydrate` -> av_lehm_sieben_mischen
- `Repair` -> av_reparatur
- `Repair edges` -> av_reparatur
- `Saw` -> av_zuschnitt
- `Saw-cut` -> av_zuschnitt
- `Selective deconstruction` -> av_zerlegung_vereinzelung
- `Selective dismantling` -> av_zerlegung_vereinzelung
- `Selective saw-cut` -> av_zuschnitt
- `Shotblast` -> av_sandstrahlen
- `Sieve` -> av_lehm_sieben_mischen
- `Sorting` -> av_materialsortierung_chargenbildung
- `Surface preparation` -> av_oberflaechenbehandlung
- `Surface protection` -> av_oberflaechenbehandlung
- `Surface refinish` -> av_oberflaechenbehandlung
- `Surface repair` -> av_reparatur
- `Traceable batch labelling` -> av_materialsortierung_chargenbildung
- `Trim` -> av_zuschnitt
- `Trimming` -> av_zuschnitt

**Residual (kept as-is, no edge):** Bolted design-for-disassembly; DIBt/project documentation; Document like new HCS; Dry; Dry/mechanical connections; Expose anchors; Grading; Grouted joints; Grouted/mechanical connections; Inspect; Lifting plan; Lime-mortar reuse detailing; Mechanical anchors/clips; New bearing pads; New bolted connections; New bolted/clamped connections; New bolted/screwed reversible joints; New grouted/shear-pocket connections; New supports; Palletising; Passport; Passport creation; Recast pockets; Recertify; Redrill; Redrilling anchors; Remove screed/topping; Reversible dry joints; Reversible screw/bolt detailing; Shortening; Shortening with specialist equipment; Stabilize only where reversible/permitted; Storage QA; Surface treatment; Traceable passporting; Traceable storage

## legal_conditions -> HAT_RECHTLICHE_BEDINGUNG  (15 tokens mapped, 46 residual)

- `BauPG` -> rb_schweizer_bauproduktegesetz
- `BauPG market-placement issue` -> rb_schweizer_bauproduktegesetz
- `BauPG status` -> rb_schweizer_bauproduktegesetz
- `BauPG/market-placement status` -> rb_schweizer_bauproduktegesetz
- `CB'23 quality passport` -> rb_materialpass
- `CE marking not required if reused without substantial modification` -> rb_ce_marking_reused_steel
- `CE/UKCA status for placed-on-market reclaimed members` -> rb_ukca_marking_reused_steel
- `CPR/CE ambiguity` -> rb_bauproduktenverordnung_cpr
- `CPR/CE gap for reused elements` -> rb_bauproduktenverordnung_cpr
- `CPR/CE if placed on market` -> rb_bauproduktenverordnung_cpr
- `CPR/CE/DoP/DPP` -> rb_bauproduktenverordnung_cpr
- `DIBt approval if no standard route` -> rb_dibt_zustimmung
- `Heritage vs new-build use` -> rb_denkmalschutz
- `Material passport decision trees` -> rb_materialpass
- `UKCA/CE if re-marketed` -> rb_ukca_marking_reused_steel

**Residual (kept as-is, no edge):** Bbl compliance; Building Control Part A; Building Regulations Part A; CB'23 quality decision tree; CB'23 quality-assurance; CDM 2015; CDM/waste duty; CE if marketed as masonry unit; CE status; CE status if re-marketed; CE-marked product status; CE/DoP gap for reclaimed graded timber; CE/DoP if placed on market; Canton demolition/pollutant rules; Canton permit practice; Canton permitting; Cantonal approval; Contractual allocation of reuse liability; Declaration of performance responsibility; Demolition notification/permit trigger; Finnish demolition permitting acknowledges reuse; German waste-wood restrictions if contaminated; Indoor-air/moisture responsibility; Landfill/waste if contaminated; Legal status of reused product; Liability split between salvager, engineer, contractor; Mineral-waste EBV if element becomes waste; NS 3682 documentation route; Non-harmonised product status; Non-harmonised Ü/ZiE/vBG route; Pollutant-remediation duties; Product-vs-waste; Product-vs-waste boundary; Product-vs-waste status; Project-specific approval; Proof of fitness for structural use; Regional demolition inventory; Regional waste/product boundary; State building-code route; Tracimat inventory; Tracimat traceability; Tracimat/predemolition inventory; VVEA if waste; VVEA waste status; Waste-plan/demolition obligations; waste duty-of-care

## Edge totals to MERGE

- HAS_RISK_POLLUTANT: 96
- HAT_PRUEFUNG: 108
- HAT_AUFBEREITUNG: 76
- HAT_RECHTLICHE_BEDINGUNG: 15
- REFERENZIERT_NORM: 1
- REGULIERT (Land->Schadstoff): 25

## New Schadstoff nodes: s_schimmel, s_chlorid, s_mineraloel, s_salze
