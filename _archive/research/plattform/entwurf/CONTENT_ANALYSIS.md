# Content Analysis

This file analyzes the content after splitting the restored original `entwurf` file into clustered Markdown files.

## Executive Finding

No original prose section is missing according to `CONTENT_SPLIT_AUDIT.md`, but the split is not yet semantically clean.

The main issue is not loss. The main issue is placement: several important orientation, role, diagram, example, and trust sections are preserved under `Review-Hinweis` even though some of them are core content for parent modules or specific child nodes.

## Confirmed Safe Points

- Original file `entwurf` is preserved unchanged.
- The clustered files contain the original direct prose sections exactly once.
- Leaf-only files were removed from the top level and their content was copied into cluster files.
- The numbered tree is readable and stable as a clustering pattern.
- No file-level encoding corruption was detected in the actual UTF-8 text. Any mojibake-like display artifacts seen in PowerShell output appear to be console rendering, not stored file corruption.

## Main Content Risks

### 1. Parent overview files are structurally correct but content-light

Affected files:

- `1.1 - Bauteil-Seed.md`
- `1.2 - Generator.md`
- `2.1 - Bauteilkatalog.md`
- `2.2 - Playground.md`

These files show the subtree only. That matches the requested structure-only parent rule, but it weakens them as navigation documents.

Content impact:

- A reader opening `1.1 - Bauteil-Seed.md` does not see the role of the Bauteil-Seed.
- A reader opening `1.2 - Generator.md` does not see the generator overview diagram.
- A reader opening `2.1 - Bauteilkatalog.md` does not see the Katalog role or transition from Generator.
- A reader opening `2.2 - Playground.md` does not see the Playground role.

Recommendation:

Keep parent files structure-only if the folder is meant as a pure clustering index. If these files are meant to be read as documents, move the corresponding role and overview diagram sections into the parent files.

### 2. Some `Review-Hinweis` sections are actually core orientation content

Affected placements:

- `1.1.4 - Output Bauteil-Seed.md` contains:
  - `Original: Rolle des Bauteil-Seeds`
  - `Original: Einspeiseplattform: Vom realen Stahlbetonbauteil zum generatorfähigen Input`
  - `Original: Kernaussage`
- `2.1.1 - Bauteilkarte.md` contains:
  - `Original: Rolle des Bauteilkatalogs`
  - `Original: Übergang vom Generator in den Katalog`
- `2.2.1 - Idee Komposition.md` contains:
  - `Original: Rolle des Playgrounds`

Content impact:

These are not weak extras. They define the purpose of their parent modules. Putting them under a review marker makes them look uncertain, although they are conceptually foundational.

Recommendation:

Either keep them as reviewed-but-unmapped notes, or promote them into explicit intro sections in the parent overview files. The second option is better for reader comprehension.

### 3. Ports and Connectoren are not extras; they belong to the semantic model

Affected file:

- `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md`

Current placement:

- `Original: Ports`
- `Original: Connectoren`

Content impact:

These sections are under `Review-Hinweis`, but they are directly part of `1.2.3.4 Semantisches Modell`. The current tree names "Ports, Connectoren, erlaubte Rollen" as the semantic model content, so Ports and Connectoren should not be treated as unmapped.

Recommendation:

Move `Ports` and `Connectoren` under `1.2.3.4 Semantisches Modell` as subsections, for example:

- `### 1.2.3.4.1 Ports`
- `### 1.2.3.4.2 Connectoren`

### 4. Datenvertrauen belongs with Evidence Link, not generic review

Affected file:

- `1.2.3 - Bauteil-Seed generiertes Bauteilobjekt.md`

Current placement:

- `Original: Datenvertrauen und fehlende Nachweise`

Content impact:

This section directly explains evidence confidence and missing proof logic. It is strongly tied to `1.2.3.5 Evidence Link` and also echoes `1.1.2.4 Nachweis-Panel`.

Recommendation:

Move it under `1.2.3.5 Evidence Link`, or keep it as a sibling section immediately after Evidence Link without the review wrapper.

### 5. Standardisierung is a bridge concept, not merely an unmapped leftover

Affected file:

- `1.2.2 - Klassifikationslogik.md`

Current placement:

- `Original: Standardisierung und Typisierung von Stahlbeton-Bauteilen`
- `Fertigteile`
- `Zuschnitt-Elemente`

Content impact:

This is a useful bridge explaining why both prefabricated parts and cut-out concrete segments can enter the same generator logic. It supports `Typologie`, `Generatorgrammatik`, and `Piece`.

Recommendation:

Keep it near `1.2.2`, but rename the wrapper from `Review-Hinweis` to something less uncertain, such as `## Brückenlogik: Standardisierung und Typisierung`, if the content is accepted.

### 6. Example cards are currently attached to actions, but they explain Bauteilkarte

Affected file:

- `2.1.3 - Katalog-Aktionen.md`

Current placement:

- `Original: Beispielkarte A — Hohlkörperdecke`
- `Original: Beispielkarte B — Stahlbeton-Wandplatte`
- `Original: Beispielkarte C — ColumnBeamSlabAssembly`
- `Original: Kernaussage`

Content impact:

The examples are catalog cards, not catalog actions. Their current location after `Auswählen / Vergleichen`, `Platzieren`, and `Reservieren` can make them feel like action examples.

Recommendation:

Move the example cards to `2.1.1 - Bauteilkarte.md` after `2.1.1.4 Prüfstatus`. Move the Katalog `Kernaussage` to `2.1 - Bauteilkatalog.md` if parent files are allowed to carry intro/summary content.

### 7. The content is more Stahlbeton-specific than the abstract tree

Affected across:

- Most content cluster files

Content impact:

The current tree reads like a general reusable-component platform architecture. The restored original content is much more specifically about Stahlbeton, with examples such as Hohlkörperdecken, Stützen, Träger, Wandplatten, ColumnBeamSlabAssembly, Bewehrung, Betondruckfestigkeit, and Auflager.

This is not a bug if the intended prototype is Stahlbeton-first. It is a conceptual constraint if the platform should describe all material families equally.

Recommendation:

Decide whether this folder is:

- a Stahlbeton-specific implementation of the architecture, or
- the general platform concept.

If general, mark Stahlbeton examples explicitly as examples, not as the universal model.

### 8. Reifegrad has a mismatch between tree and original content

Affected file:

- `2.1.1 - Bauteilkarte.md`

Tree phrasing:

- `Idee → entwurfsfähig → prüfbedürftig → ausschreibungsnah`

Original content:

- `Idee`
- `Entwurfsfähig`
- `Prüfbedürftig`
- `Ausschreibungsnah`
- `Einbaufähig`

Content impact:

The original adds `Einbaufähig`, which is a meaningful fifth maturity stage. This is not missing, but it diverges from the current tree summary.

Recommendation:

Either update the tree summary to include `Einbaufähig`, or add a note that `Einbaufähig` is an optional later-stage extension beyond the first catalog view.

### 9. Some file titles are bilingual or normalized differently from content

Examples:

- `UI Concept` vs `UI-Konzept`
- `Evidence Link` vs German surrounding terminology
- filenames use `CO2`, `Pruefstatus`, `Kompatibilitaetspruefung`, while content uses `CO₂`, `Prüfstatus`, `Kompatibilitätsprüfung`

Content impact:

This does not change meaning, but it weakens recognition if the folder is used to identify clustering patterns visually.

Recommendation:

Accept ASCII filenames if filesystem/search stability matters. Inside files, prefer the proper display title with German spelling and special characters.

## Recommended Next Cleanup

Priority 1:

- Move `Ports` and `Connectoren` out of `Review-Hinweis` and under `1.2.3.4 Semantisches Modell`.
- Move `Datenvertrauen und fehlende Nachweise` out of `Review-Hinweis` and under `1.2.3.5 Evidence Link`.
- Move example cards from `2.1.3` to `2.1.1`.

Priority 2:

- Decide whether parent overview files should remain structure-only or become readable intro documents.
- If readable intro documents are allowed, move role/overview/kernaussage sections into `1.1`, `1.2`, `2.1`, and `2.2`.

Priority 3:

- Resolve whether the architecture is Stahlbeton-first or material-general.
- Resolve whether `Einbaufähig` belongs in the official Reifegrad structure.

## Bottom Line

The split preserved the text, but it did not fully preserve the conceptual hierarchy. The current structure is usable as a first clustering pass, but several sections are parked as review leftovers even though they carry core system meaning.
