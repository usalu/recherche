# Pollutant × era × component — sourced matrix (rescues the Schadstoff layer)

Deep web research turning the 754 unsourced `HAS_RISK_POLLUTANT` (`evidence_confidence='inferiert'`)
edges into **evidenced era→pollutant rules**. Each row = real time-window + typical components +
authoritative source. Mapped to the graph's existing `:BauwerkEra` nodes — which means the graph's
`Schadstoff-[:TYPISCH_BEI_ERA]->BauwerkEra` edges are **correct and now citable**, and per-component
risk can be *derived* (via Bauwerk era / material) instead of sprayed on as inference.

| Schadstoff | Use window | Typical components | Maps to era nodes | Source |
|---|---|---|---|---|
| **Asbest** (`s_asbest`) | 1950–1995 (DE-Verbot 1993) | Spritzasbest, Asbestzement (Dach/Fassade), Putze/Spachtel/Fliesenkleber, Fugendichtmassen, Leichtbauplatten, Floor-Flex | nachkrieg_1945_1970, 1970_1990, 1990_2000 | GefStoffV/TRGS 519; [schadstoff-kompass](https://www.schadstoff-kompass.de/sanierung/schadstoffe-bei-der-sanierung-erkennen/); LfU Arbeitshilfe |
| **KMF / alte Mineralwolle** (`s_kmf`) | vor 1996/2000 | Dämmung (Glas-/Steinwolle) | 1970_1990, 1990_2000 | TRGS 521; schadstoff-kompass |
| **PCB** (`s_pcb`) | 1955–1975 (Peak 1964–72); Fugen-Verbot 1978, generell 1989 | Fugendichtmassen ("Thiokol") in Skelett-/Plattenbau, Wandfarben, Kondensatoren/Leuchten | nachkrieg_1945_1970, 1970_1990 | [LfU Bayern](https://www.lfu.bayern.de/abfall/schadstoffratgeber_gebaeuderueckbau/arbeitshilfe/index.htm); [polludoc.ch](https://polludoc.ch/de/material/pcb-fugendichtungsmassen); allum.de |
| **PAK / Teer** (`s_pak`) | bis ~1970er (Parkettkleber bis ~1960er) | Teerpappe/Dachabdichtung, Parkett-Schwarzkleber, Gussasphalt, Schlacke-Schüttung | vor_1900, 1900_1945, nachkrieg_1945_1970, (früh) 1970_1990 | [arguk.de](https://www.arguk.de/leistung/innenraum/Sanierung-von-teerpechhaltigen-Parkettklebern.htm); polludoc.ch; ifmu.de |
| **Holzschutzmittel** (PCP/Lindan) (`s_holzschutzmittel`) | bis 1989 (PCP-Verbot DE) | behandeltes Bau-/Konstruktionsholz, Dachstühle | nachkrieg_1945_1970, 1970_1990 | AltholzV / DIN 68800 |
| **Bleifarbe** (`s_bleifarbe`) | überw. vor ~1960 | Anstriche, Beschichtungen | vor_1900, 1900_1945, nachkrieg_1945_1970 | schadstoff-kompass; REACH |
| **Formaldehyd** (`s_formaldehyd`) | ab 1960er, laufend | Spanplatten, MDF, Leime | nachkrieg_1945_1970, 1970_1990, post_2000 | REACH Anh. XVII; AgBB |
| **Schwermetalle** (`s_schwermetalle`) | material-/nutzungsabhängig | Beschichtungen, Laborbauten, Metallteile | (material-getrieben, nicht era) | REACH |
| **Radon** (`s_radon`) | **nicht era-, sondern geologieabhängig** | Kontakt zum Baugrund (Keller/EG) | (Standort, alle Era) | StrlSchG / BfS |
| **Schimmel** (`s_schimmel`) | feuchteabhängig, nicht era | feuchtegeschädigte Bauteile | (Zustand, nicht era) | UBA-Schimmelleitfaden |

## How this rescues the layer (no information lost)
1. **Keep** all 13 `Schadstoff` nodes (real substances).
2. **Keep** `TYPISCH_BEI_ERA` / `TYPISCH_BEI_MATERIAL` — now **cited** with the sources above + the new
   `rw_lfu_schadstoff_arbeitshilfe` Regelwerk. These become the *evidenced* basis.
3. **Replace** the 754 `HAS_RISK_POLLUTANT` (`inferiert`) + 331 `material_only`
   `REQUIRES_VERIFICATION_FOR` edges with the derived, sourced spine:
   `Bauwerk(era) → Schadstoff → Nachweisforderung(AsbestCheck…) → Regelwerk(GefStoffV/TRGS/LfU)`.
4. Net: the *same* "this 1960s concrete building likely has PCB in its joint sealants" conclusion —
   but now traceable to LfU/TRGS, not a bare `inferiert` tag.

> Caveat kept honest: era→pollutant is a **screening likelihood** (what to test for), not proof of
> presence. The evidenced edge says exactly that ("typical for era per LfU"), which is what a
> pre-demolition pollutant survey (GefStoffV/LfU/VDI 6202) actually mandates.
