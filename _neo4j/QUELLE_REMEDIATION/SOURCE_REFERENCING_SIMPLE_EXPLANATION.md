# Simple Explanation Of The Source Examples

This explains the node samples in `SOURCE_REFERENCING_MINIMAL_NODE_SAMPLES.md` in plain language.

The main idea is:

```text
Nodes say what a thing is.
Relationships say facts about things.
Sources belong on the fact, not broadly on the thing.
```

So a project node can have a name, but the source for "this project uses reused steel" belongs on the relationship that says that fact.

Markdown files are only containers:

```text
Stuttgart_210.md is not the source truth.
akteursliste_master.md is not the source truth.
research/*.md files are not the source truth.
Bauteilboerse/*.md files are not the source truth.

The links inside the relevant row or section are the source truth.
```

## The Four Source States

Use only these simple meanings:

| State | Meaning |
|---|---|
| `exact` | This URL directly proves this exact fact. |
| `candidate` | This URL may be relevant, but it has not been checked for this exact fact. |
| `derived` | This fact was produced from other facts or a rule. It should point to the source facts or rule, not to a guessed URL. |
| `missing` | No source is known yet. |

Only `exact` facts get `source_url`.

Candidate URLs are leads for review. They are not proof.

## How To Read The Sample Rows

Each sample row shows one node. The important column is `attach source how`.

When it says:

| Text in sample | Simple meaning |
|---|---|
| `identity on node; facts on relationships/Claim` | Keep only stable identity on the node. Put sources on the relationships or on a Claim node. |
| `metadata node; do not use as proof alone` | This node stores source metadata, but it does not prove a graph fact by itself. |
| markdown row/section or document lineage edge | This is only row/context lineage. The actual source is the concrete URL from that row/section, copied onto the fact or Claim. |
| `relationship fact or Claim if attribute-like` | If the fact is a relationship, source the relationship. If it is more like a value/attribute, use a Claim. |
| `review/audit node, no fact source required` | This is about graph quality review, not evidence for a domain fact. |

## Concrete Label Explanation

| Label | What it is | Simple source rule |
|---|---|---|
| `DataIssue` | A problem marker or review note. | It does not need a source URL. It should point to the thing that needs review. |
| `Quelle` | A source or URL-like metadata node. | Do not treat it as proof by itself. A fact still needs its own exact `source_url`. |
| `ExternalLink` | A URL metadata node. | Useful for URL inventory, not enough to prove a fact alone. |
| `DossierEntityTarget` | A value or row extracted from a dossier. | Use the dossier row only as context. The source truth is the concrete URL from that row/source field, copied onto the fact or Claim. |
| `Akteur` | A person, office, company, institution, or other actor. | Keep name/id on the node. If it came from `akteursliste_master.md`, source it with the concrete link from that actor row, not with the `.md` file. |
| `SectionRef` | A section reference inside a source/document. | Treat as source location metadata, not as a domain fact. |
| `ResearchDocument` | A research document or imported document record. | Document metadata only. Facts taken from it need the concrete URL from the relevant row/section attached to the fact. |
| `Bauteilgruppe` | A group of building components. | Source facts like material, status, reuse type, and component type on relationships. |
| `Kennwert` | A measured or calculated value. | Usually use a Claim or source the `HAT_KENNWERT` relationship exactly. |
| `Bauwerk` | A building or built object. | Keep identity on the node. Source status, location, role, material, and links on relationships. |
| `PruefungNachweis` | A test, proof, verification, or evidence type. | Source the relationship saying a project/component has this proof. |
| `Norm` | A standard or regulation. | Source the relationship saying something follows or uses the norm. |
| `Projekt` | A project/case study. | Keep id/name/year on node. Source every project fact on relationships or Claims. |
| `Dossier` | A dossier/source package. | Keep as source container and URL inventory. Facts from it still need the concrete URL attached directly. |
| `Stadt` | A city. | Identity node. Source location claims on relationships if needed. |
| `Aufbereitungsverfahren` | A preparation or processing method. | Source the relationship saying a component/project uses this method. |
| `Leistungsanforderung` | A performance requirement. | Source the relationship that attaches the requirement to a component/project. |
| `Programm` | A program, initiative, or research/project program. | Source membership or participation relationships. |
| `Huerde` | A barrier or obstacle. | Source the relationship saying a project/component has this barrier. |
| `Material` | A material. | Identity node. Source material use on `NUTZT_MATERIAL` or similar relationships. |
| `Akteurrolle` | A role an actor can have. | Source the actor-role relationship, not the role vocabulary node. |
| `Bauteiltyp` | A component type. | Source the relationship from component group to type. |
| `Materialdepot` | A material depot/storage/source place. | Source relationships that connect it to projects, materials, or components. |
| `ReuseRule` | A reuse rule. | If it is a rule from a document, source the rule Claim or rule relationship. |
| `Land` | A country. | Identity node. Source country/location relationships if they are imported facts. |
| `Software` | A software tool. | Source relationships saying an actor/project uses or provides it. |
| `Ressourcenquelle` | A resource source. | Source the relationship saying where a reused resource came from. |
| `Bauproduktstatus` | A product/status category. | Source the relationship assigning the status. |
| `RechtlicheBedingung` | A legal condition. | Source the relationship linking the condition to a project/component. |
| `Verbindungstechnik` | A connection/joining technique. | Source the relationship saying it was used. |
| `Wiederverwendungskette` | A reuse chain. | Source the chain facts or create Claims for complex chain steps. |
| `DeprecatedType` | An old/superseded type. | Review metadata. Do not use as source proof. |
| `Methode` | A method. | Source the relationship saying the method was used. |
| `Wirtschaft` | An economic/business concept. | Source relationships or Claims about economic facts. |
| `Marktmodell` | A market model. | Source the relationship assigning the market model. |
| `Materialgruppe` | A material group/category. | Vocabulary-like node. Source the classification relationship. |
| `WiederverwendungsArt` | A reuse type/category. | Source the relationship assigning the reuse type. |
| `Akteurtyp` | Actor type/category. | Source the relationship assigning the actor type. |
| `BauaufgabeIntervention` | Building task/intervention type. | Source the relationship assigning the intervention. |
| `Beschaffungsweg` | Procurement path. | Source the relationship saying how something was procured. |
| `Defekt` | Defect/damage type. | Source the relationship saying a defect exists. |
| `HuerdeKategorie` | Barrier category. | Source the classification relationship if it is factual. |
| `Logistik` | Logistics concept/process. | Source the relationship saying it applies. |
| `Prozessphase` | Process phase. | Source the relationship assigning a phase. |
| `Bausystem` | Building system. | Source the relationship saying a building/component uses it. |
| `MatchingQualitaet` | Matching quality category. | Source the relationship/Claim where this quality is asserted. |
| `Nutzung` | Use/function. | Source the relationship saying a building/project has this use. |
| `Schadstoff` | Pollutant. | Source the relationship saying a pollutant risk exists. |
| `Status` | Status category. | Source the relationship assigning the status. |
| `Bauobjektklasse` | Built-object class. | Source the classification relationship. |
| `Tool` | Tool category or named tool. | Source the relationship saying it is used or relevant. |
| `Zertifizierungssystem` | Certification system. | Source the relationship linking it to a project/building. |
| `Akzeptanz` | Acceptance/social acceptance concept. | Source the Claim or relationship where acceptance is asserted. |
| `Bauobjektrolle` | Role of a building object, such as donor/recipient. | Source the relationship assigning the role. |
| `Bauteilebene` | Component level/layer. | Source the relationship assigning the level. |
| `Bauweise` | Construction method. | Source the relationship saying this method applies. |
| `BauwerkEra` | Era/period of a building. | Source the relationship or Claim assigning the era. |
| `Funktionswechsel` | Change of function. | Source the relationship or Claim describing the change. |
| `Layer` | Building layer. | Source the relationship assigning the layer. |
| `ZustandsKlasse` | Condition class. | Source the relationship assigning the condition. |
| `LCAModule` | Life-cycle assessment module. | Source the LCA/Kennwert Claim or relationship using the module. |
| `Rueckbauverfahren` | Deconstruction method. | Source the relationship saying the method was used. |
| `Tragwerksprinzip` | Structural principle. | Source the relationship assigning the structural principle. |
| `OntologyAnchor` | Ontology helper/anchor node. | Schema helper, not evidence. No fact source needed unless used as a claim. |

## The Simplest Practical Rule

For every imported piece of information, ask one question:

```text
What exact fact is being stated?
```

Then put the source on that exact fact.

Examples:

```text
Project name:
  keep on Projekt node as identity

Project has status "completed":
  source the Projekt - HAT_STATUS - Status relationship

Project has CO2 saving value:
  source the Projekt - HAT_KENNWERT - Kennwert relationship
  or use a Claim if the value has method/unit/context

Actor worked on project:
  source the Akteur - BETEILIGT_AN - Projekt relationship

Component group uses material:
  source the Bauteilgruppe - NUTZT_MATERIAL - Material relationship

URL node exists:
  this is only URL inventory
  it does not prove a fact unless a fact points to that exact URL
```

## Minimal Fields

Use these on the relationship or Claim:

```text
source_status
source_url
source_note
```

Meaning:

```text
source_status: exact      source_url is allowed
source_status: candidate  source_url stays empty; candidate_source_urls may exist
source_status: derived    point to source facts/rule
source_status: missing    no source known yet
```
