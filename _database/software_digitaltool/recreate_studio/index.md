---
entity: "software_digitaltool"
id: "recreate_studio"
title: "ReCreate Studio"
build_status: "promoted_phase42"
legacy_paths:
  - "tools\\recreate_studio.md"
node_kind: "core"
---

# ReCreate Studio

## Legacy Content

### Legacy Source: tools\recreate_studio.md

- Map action: move_as_core
- Target role in map: primary
- Raw mapped target: software_digitaltool/recreate_studio
- Original primary target: software_digitaltool/recreate_studio
- Original secondary targets: 

# ReCreate Studio

## Research positioning

**ReCreate Studio** is a BIM-based digital design tool developed in the context of the European **ReCreate** project. Its relevance to reuse lies in a very specific problem: how to design new buildings when the available structural components are **not newly manufactured to order**, but are taken from existing precast concrete buildings.

In reuse-oriented construction, design has to respond to existing component stock. Precast slabs, beams, columns, and wall panels have fixed geometry, known or partly known structural capacity, a donor-building history, and practical constraints around dismantling, transport, repair, and reassembly. ReCreate Studio addresses this by connecting BIM design with a database of reusable precast concrete elements.

## Main reuse problem addressed

Conventional BIM workflows usually assume that components can be specified and procured after the design is defined. Reuse reverses that logic. The designer first needs to know which components exist, whether they can be dismantled without damage, what their properties are, and how they can fit into a new design.

ReCreate Studio supports this shift from:

- **design-then-procure**: design the building first, then order new components;
- to **design-by-availability**: design with the dimensions, capacities, and quantities of available reused components.

## How it supports reuse

ReCreate Studio is relevant to reuse because it can make reclaimed precast elements behave like designable digital objects. Instead of treating reused components as irregular leftovers, the tool allows them to become part of a structured BIM-based design workflow.

Key reuse-supporting functions include:

- importing reusable concrete components into a BIM environment;
- linking each element to data on geometry, origin, structural capacity, and condition;
- supporting layout options based on available stock;
- helping designers check whether reused elements satisfy structural requirements;
- comparing design options with regard to embodied carbon and reuse potential;
- supporting earlier decisions about whether reuse is technically and environmentally worthwhile.

## Typical data inputs

A useful ReCreate Studio workflow depends on high-quality information from the donor building and from pre-deconstruction assessment. Typical data includes:

- component type, such as slab, wall, beam, column, or façade element;
- dimensions and geometry;
- connection type and dismantling constraints;
- reinforcement information;
- concrete properties and structural capacity;
- damage, contamination, or repair needs;
- original location and donor-building context;
- quantity and availability date;
- transport distance and storage assumptions;
- regulatory or quality-assurance status.

## Typical outputs

Outputs are useful for design, engineering, and project decision-making:

- BIM layout options using reused precast components;
- lists of selected reusable elements;
- identification of components that do or do not match design requirements;
- structural suitability feedback;
- preliminary carbon or environmental comparison;
- documentation for further quality assurance and approval discussions.

## Place in a reuse workflow

ReCreate Studio is most relevant between the **pre-deconstruction audit** and the **new-building design phase**.

A typical workflow is:

1. inspect and document the donor building;
2. create a verified component database;
3. import candidate components into the design tool;
4. test layouts and structural feasibility;
5. decide which elements should be dismantled, stored, transported, and reused;
6. feed the design decision back into logistics and deconstruction planning.

## Relevance to circular construction research

ReCreate Studio is important as a research case because it shows how digital design tools can operationalise structural reuse. Many circular-economy discussions remain at the material-flow level, but structural reuse requires element-level compatibility, engineering evidence, and design integration. The tool therefore connects circular economy goals with practical BIM, structural engineering, and procurement workflows.

It is especially relevant for research on:

- reuse of load-bearing components;
- design-by-availability;
- digital twins and material inventories;
- BIM-based circular design;
- reuse logistics and donor-recipient building matching;
- embodied-carbon reduction through high-value reuse.

## Strengths for reuse

- Focuses on high-value structural reuse rather than low-value recycling.
- Connects available component stock directly to design decisions.
- Helps overcome the mismatch between existing component dimensions and new design requirements.
- Can make reuse visible early enough to influence project feasibility.
- Supports integration of technical and environmental evaluation.

## Limitations and research gaps

- It is closely linked to precast concrete; it is not a universal reuse tool for all materials.
- It depends on accurate donor-building data and verified component properties.
- Reuse of structural elements still requires regulatory acceptance, liability clarity, quality assurance, and logistics planning.
- The tool is associated with research and pilot development; market maturity and interoperability may vary by context.
- It does not remove the need for engineering judgement.

## Key references

- ReCreate project homepage: https://recreate-project.eu/
- ReCreate, "BIM software for designing with reused concrete building components": https://recreate-project.eu/2023/09/14/bim-software-for-designing-with-reused-concrete-building-components/
- CORDIS project record, ReCreate: https://cordis.europa.eu/project/id/958200

Access date: 2026-05-04.
