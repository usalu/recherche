"""Agent 11 — Phase 3.1 + 3.2 + 3.3 runner.

Executes the three Phase 3 migrations against the live mit-bestand
graph and writes phase done-flags + a structured result JSON.

The cypher files under migrations/ are the source of truth for intent;
this runner reads them, strips comments, splits on ';', and runs each
statement with the relevant parameters.

The 20 :ReuseRule rows are encoded below in REUSE_RULE_ROWS following
the canonical structure of
  _knowledge/themes/circular_construction_reuse_graph_gaps.md.

Usage:
    python agent11_runner.py
"""
from __future__ import annotations

import json
import re
import sys
import traceback
import unicodedata
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

REPO_ROOT = Path(r"E:/recherche")
RUN_ROOT = REPO_ROOT / "_neo4j/intake/runs/2026-05-20_radical_quality_reset"
MIG_DIR = RUN_ROOT / "migrations"
LOGS_DIR = RUN_ROOT / "logs"
RESULT = LOGS_DIR / "agent11_result.json"
PROG = LOGS_DIR / "agent11_progress.log"

MIG_3_1 = MIG_DIR / "mig_3_1_built_in_era.cypher"
MIG_3_2 = MIG_DIR / "mig_3_2_pollutant_inference.cypher"
MIG_3_3 = MIG_DIR / "mig_3_3_reuse_rules.cypher"


# ---------------------------------------------------------------------------
#  20 canonical :ReuseRule rows (mirroring
#  circular_construction_reuse_graph_gaps.md rows 1..20)
# ---------------------------------------------------------------------------


def _slug(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    text = text.lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    return text.strip("_")


def _norm_id(name: str) -> str:
    return "norm_" + _slug(name)


REUSE_RULE_ROWS: list[dict[str, Any]] = [
    {
        "rank": 1,
        "country_iso": "GB",
        "country_name": "Vereinigtes Königreich",
        "land_id": "land_vereinigtes_koenigreich",
        "material": "Stahl",
        "material_id": "mat_stahl",
        "priority": "P1_Critical",
        "project_cluster": "Steel-dominant structural reuse",
        "key_norms": [
            "PD CEN/TS 1090-201",
            "EN 1090-2",
            "Eurocode 3",
            "SCI protocol",
            "UKCA/CE interface",
        ],
        "legal_conditions": [
            "Building Regulations Part A",
            "CDM 2015",
            "waste duty-of-care",
            "CE/UKCA status for placed-on-market reclaimed members",
        ],
        "required_tests": [
            "Provenance",
            "visual inspection",
            "section geometry",
            "tensile/yield/elongation",
            "Charpy where relevant",
            "weldability/CEV",
            "NDT of welds",
            "corrosion loss",
            "fire-protection evidence",
        ],
        "pollutant_risks": [
            "Lead/chromate paint",
            "PAH coatings",
            "Asbestos fireproofing",
            "PCB sealants",
            "Cadmium/galvanic coatings",
        ],
        "processing_methods": [
            "Dismantle by unbolting",
            "Cut out damaged ends",
            "Shotblast",
            "Decoat",
            "Redrill",
            "Recoat",
            "Recertify",
        ],
        "source_url": "https://standards.iteh.ai/catalog/standards/cen/31a1835a-d97d-4bf7-8319-62d76609fe39/cen-ts-1090-201-2024",
        "suggested_graph_action": "Create `ReusableStructuralSteelMember` template with edges to CEN_TS_1090_201, SCI_Protocol, TestProtocol, PollutantScreening, BoltedSpliceConnection, FireResistanceRequirement, CorrosionProtectionRequirement.",
    },
    {
        "rank": 2,
        "country_iso": "BE",
        "country_name": "Belgien",
        "land_id": "land_belgien",
        "material": "Stahl",
        "material_id": "mat_stahl",
        "priority": "P1_Critical",
        "project_cluster": "High-count Belgian steel reuse",
        "key_norms": [
            "CEN/TS 1090-201",
            "EN 1090-2",
            "Eurocode 3",
            "NBN national annexes",
        ],
        "legal_conditions": [
            "Regional waste/product boundary",
            "Tracimat traceability",
            "CPR/CE/DoP/DPP",
            "Liability split between salvager, engineer, contractor",
        ],
        "required_tests": [
            "Same steel test package as UK",
            "Batch grouping by provenance and execution class",
        ],
        "pollutant_risks": [
            "Coatings with lead/chromate/PAH",
            "Asbestos fireproofing",
            "PCB sealants",
        ],
        "processing_methods": [
            "Selective deconstruction",
            "Traceable batch labelling",
            "Blasting/decoating",
            "Re-fabrication",
        ],
        "source_url": "https://www.fir-recycling.com/wp-content/uploads/2023/02/FPRGErkenning_Tracimatversie_Engels.pdf",
        "suggested_graph_action": "Add Belgium-specific TraceabilityProcedure = Tracimat and require ProvenanceEvidence before assigning steel strength class.",
    },
    {
        "rank": 3,
        "country_iso": "DE",
        "country_name": "Deutschland",
        "land_id": "land_deutschland",
        "material": "Stahl",
        "material_id": "mat_stahl",
        "priority": "P1_Critical",
        "project_cluster": "High-count German structural steel",
        "key_norms": [
            "CEN/TS 1090-201",
            "DIN EN 1090-2",
            "DIN EN 1993",
            "MVV TB/DIBt pathway",
        ],
        "legal_conditions": [
            "CE-marked product status",
            "Non-harmonised Ü/ZiE/vBG route",
            "Project-specific approval",
        ],
        "required_tests": [
            "Mechanical tests",
            "Chemical tests",
            "Weldability tests",
            "Geometry",
            "Corrosion",
            "Existing weld NDT",
            "Coating/fire proofing records",
        ],
        "pollutant_risks": [
            "Lead/chromate coatings",
            "PAH",
            "Asbestos",
            "PCB",
            "Old fireproofing",
        ],
        "processing_methods": [
            "Careful deconstruction",
            "Coating removal",
            "Trimming",
            "New bolted connections",
            "DIBt/project documentation",
        ],
        "source_url": "https://www.dibt.de/en/service/faqs/the-german-regulatory-system-for-construction-products-and-construction-techniques",
        "suggested_graph_action": "Add GermanyApprovalPath decision node: CE_hEN, Ü_Zeichen, abZ/aBG, ZiE/vBG, ProjectSpecificEngineerAssessment.",
    },
    {
        "rank": 4,
        "country_iso": "NL",
        "country_name": "Niederlande",
        "land_id": "land_niederlande",
        "material": "Stahl",
        "material_id": "mat_stahl",
        "priority": "P1_Critical",
        "project_cluster": "Dutch circular steel / material-passport projects",
        "key_norms": [
            "CEN/TS 1090-201",
            "NEN EN 1090-2",
            "Eurocode 3",
            "Bbl/NEN links",
        ],
        "legal_conditions": [
            "Bbl compliance",
            "CE/DoP if placed on market",
            "CB'23 quality-assurance",
            "Material passport decision trees",
        ],
        "required_tests": [
            "Provenance grouping",
            "Mechanical testing",
            "Geometry/tolerances",
            "Weldability",
            "Corrosion",
            "Weld NDT",
        ],
        "pollutant_risks": [
            "Lead/chromate/PAH coatings",
            "Asbestos",
            "PCB",
            "Heavy metals",
        ],
        "processing_methods": [
            "Passport creation",
            "Selective dismantling",
            "Reconditioning",
            "Bolted design-for-disassembly",
        ],
        "source_url": "https://www.government.nl/themes/building-and-housing/construction-products/ce-marking-for-construction-products-supervision-and-control",
        "suggested_graph_action": "Create DutchReuseQualityAssessment node linked to MaterialPassport, BblPerformanceRequirement, and CEN_TS_1090_201_TestProtocol.",
    },
    {
        "rank": 5,
        "country_iso": "CH",
        "country_name": "Schweiz",
        "land_id": "land_schweiz",
        "material": "Stahl",
        "material_id": "mat_stahl",
        "priority": "P1_Critical",
        "project_cluster": "Swiss steel-bearing reused components",
        "key_norms": [
            "CEN/TS 1090-201",
            "SIA 263",
            "SIA fire/durability rules",
            "Swiss BauPG",
        ],
        "legal_conditions": [
            "BauPG/market-placement status",
            "Canton permit practice",
            "Declaration of performance responsibility",
        ],
        "required_tests": [
            "Strength/weldability",
            "Geometry",
            "Corrosion",
            "Coatings",
            "Connection history",
            "Fire performance",
        ],
        "pollutant_risks": [
            "Asbestos",
            "PCB",
            "PAH",
            "Heavy metals",
            "Chemical coatings",
        ],
        "processing_methods": [
            "Dismantling",
            "Cutting",
            "Surface preparation",
            "New bolted/clamped connections",
            "Coating renewal",
        ],
        "source_url": "https://openbim-knowledgebase.org/en/docs/chapter-5-swiss-climate-strategy-and-legislation/chapter-5-6-federal-act-on-construction-products-construction-products-act-baupg/",
        "suggested_graph_action": "Add Swiss BauPGLegalStatus and SIA263PerformanceRequirement; separate ReusableSteel from WasteMetalScrap.",
    },
    {
        "rank": 6,
        "country_iso": "BE",
        "country_name": "Belgien",
        "land_id": "land_belgien",
        "material": "Beton",
        "material_id": "mat_beton",
        "priority": "P1_Critical",
        "project_cluster": "High-count concrete reuse and precast reuse",
        "key_norms": [
            "Eurocode 2",
            "EN 206",
            "EN 13369",
            "EN 1168",
            "EN 13224",
            "EN 13747",
        ],
        "legal_conditions": [
            "Product-vs-waste status",
            "Regional demolition inventory",
            "CPR/CE gap for reused elements",
        ],
        "required_tests": [
            "Drawings/provenance",
            "Cover scan",
            "Reinforcement scan",
            "Cores/rebound/UPV",
            "Carbonation",
            "Chloride",
            "Sulfate",
            "Cracks",
            "Fire exposure",
            "Load test where needed",
        ],
        "pollutant_risks": [
            "Asbestos coatings/tiles",
            "PCB joints",
            "PAH/tar membranes",
            "Oil contamination",
            "Chlorides",
            "Heavy metals",
        ],
        "processing_methods": [
            "Saw-cut",
            "Clean",
            "Remove screed/topping",
            "Repair edges",
            "Expose anchors",
            "Recast pockets",
            "Surface protection",
        ],
        "source_url": "https://ec.europa.eu/environment/pdf/waste/studies/deliverables/CDW_Belgium_Factsheet_Final.pdf",
        "suggested_graph_action": "Create ReclaimedConcreteElement template with ConditionAssessment, DurabilityAssessment, BearingZoneCheck, HazardousSubstanceInventory.",
    },
    {
        "rank": 7,
        "country_iso": "NL",
        "country_name": "Niederlande",
        "land_id": "land_niederlande",
        "material": "Beton",
        "material_id": "mat_beton",
        "priority": "P1_Critical",
        "project_cluster": "Dutch precast/concrete reuse pilots",
        "key_norms": [
            "Eurocode 2",
            "EN 206",
            "EN 13369",
            "EN 1168",
            "Bbl/NEN",
        ],
        "legal_conditions": [
            "Bbl compliance",
            "Demolition notification/permit trigger",
            "CE status",
            "CB'23 quality decision tree",
        ],
        "required_tests": [
            "Concrete strength",
            "Reinforcement/prestress detection",
            "Cracks after each handling stage",
            "Carbonation/chloride",
            "Fire history",
            "Load testing",
        ],
        "pollutant_risks": [
            "Asbestos",
            "PCB sealants",
            "PAH membranes",
            "Chlorides",
            "Oil/heavy metals",
        ],
        "processing_methods": [
            "Deconstruction-as-production-process",
            "Storage QA",
            "Repair",
            "Shortening",
            "Cleaning",
            "Traceable passporting",
        ],
        "source_url": "https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment-and-assurance-when-reusing-products-from-existing-structures_June2023.pdf",
        "suggested_graph_action": "Add lifecycle stage nodes: PreDeconstructionAudit → DismantlingInspection → StorageInspection → RefurbishmentQA → ReassemblyAcceptance.",
    },
    {
        "rank": 8,
        "country_iso": "DE",
        "country_name": "Deutschland",
        "land_id": "land_deutschland",
        "material": "Beton",
        "material_id": "mat_beton",
        "priority": "P1_Critical",
        "project_cluster": "German concrete/precast reuse",
        "key_norms": [
            "Eurocode 2",
            "DIN EN 206",
            "DIN EN 13369",
            "DIN EN 1168",
            "DIBt/MVV TB",
        ],
        "legal_conditions": [
            "State building-code route",
            "DIBt approval if no standard route",
            "Mineral-waste EBV if element becomes waste",
        ],
        "required_tests": [
            "Strength",
            "Cover",
            "Reinforcement",
            "Carbonation/chloride",
            "Crack mapping",
            "Bearing zones",
            "Anchorage",
            "Fire damage",
            "Load test",
        ],
        "pollutant_risks": [
            "Asbestos spacers/coatings",
            "PCB joints",
            "PAH waterproofing",
            "Chlorides",
            "Heavy metals",
        ],
        "processing_methods": [
            "Selective dismantling",
            "Cutting",
            "Cleaning",
            "Edge repair",
            "New bearing pads",
            "Grouted/mechanical connections",
        ],
        "source_url": "https://www.dibt.de/en/service/faqs/the-german-regulatory-system-for-construction-products-and-construction-techniques",
        "suggested_graph_action": "Add GermanyConcreteReuseApprovalRoute and EBV_NotApplicableUnlessCrushedOrWaste rule.",
    },
    {
        "rank": 9,
        "country_iso": "CH",
        "country_name": "Schweiz",
        "land_id": "land_schweiz",
        "material": "Beton",
        "material_id": "mat_beton",
        "priority": "P1_Critical",
        "project_cluster": "Swiss concrete structural reuse",
        "key_norms": [
            "SIA 262",
            "SIA 269",
            "EN/SIA product references",
        ],
        "legal_conditions": [
            "VVEA waste status",
            "Canton demolition/pollutant rules",
            "BauPG market-placement issue",
        ],
        "required_tests": [
            "Cover/rebar scan",
            "Cores",
            "Carbonation/chloride",
            "Crack/damage",
            "Fire",
            "Remaining service life",
            "Load path",
        ],
        "pollutant_risks": [
            "Asbestos",
            "PCB",
            "PAH",
            "Heavy metals",
            "Mineral oil contamination",
        ],
        "processing_methods": [
            "Selective saw-cut",
            "Cleaning",
            "Surface repair",
            "New supports",
            "Dry/mechanical connections",
        ],
        "source_url": "https://www.fedlex.admin.ch/eli/cc/2015/891/en",
        "suggested_graph_action": "Add RemainingServiceLifeRequirement and VVEAWasteStatus nodes to concrete elements.",
    },
    {
        "rank": 10,
        "country_iso": "FI",
        "country_name": "Finnland",
        "land_id": "land_finnland",
        "material": "Beton / hollow-core slabs",
        "material_id": "mat_beton",
        "priority": "P1_Critical",
        "project_cluster": "Finnish ReCreate HCS/precast cluster",
        "key_norms": [
            "EN 1168",
            "Eurocode 2",
            "Finnish national annexes",
            "ReCreate QA procedure",
        ],
        "legal_conditions": [
            "Finnish demolition permitting acknowledges reuse",
            "CE marking not required if reused without substantial modification",
        ],
        "required_tests": [
            "HCS dimensions",
            "Strand location",
            "End damage",
            "Bending/shear load tests",
            "Cracking after handling",
            "Carbonation/chloride",
            "Fire exposure",
            "Bearing length",
        ],
        "pollutant_risks": [
            "Asbestos",
            "PCB",
            "PAH",
            "Chlorides",
            "Insulation contamination",
            "Mold/moisture",
        ],
        "processing_methods": [
            "Careful deconstruction",
            "Lifting plan",
            "End repair",
            "Shortening with specialist equipment",
            "Storage QA",
            "Grouted joints",
        ],
        "source_url": "https://recreate-project.eu/2025/05/27/which-regulation-pertains-to-deconstruction-and-reuse-of-precast-concrete/",
        "suggested_graph_action": "Build HollowCoreSlabReuseProtocol with explicit StrandIntegrity, BearingZone, LoadTest, HandlingDamage properties.",
    },
    {
        "rank": 11,
        "country_iso": "NO",
        "country_name": "Norwegen",
        "land_id": "land_norwegen",
        "material": "Beton / hollow-core slabs",
        "material_id": "mat_beton",
        "priority": "P1_Critical",
        "project_cluster": "Norwegian HCS reuse, low count but high transfer value",
        "key_norms": [
            "NS 3682:2022",
            "EN 1168",
            "Eurocode 2",
            "TEK17",
        ],
        "legal_conditions": [
            "NS 3682 documentation route",
            "Waste-plan/demolition obligations",
            "Legal status of reused product",
        ],
        "required_tests": [
            "Minimum full-scale testing rule",
            "Remaining service life",
            "Carbonation threshold",
            "Strand/bearing condition",
            "Shear/bending capacity",
            "Fire exposure",
        ],
        "pollutant_risks": [
            "Asbestos",
            "PCB",
            "PAH",
            "Chlorides",
            "Heavy metals",
        ],
        "processing_methods": [
            "Dismantle",
            "Inspect",
            "Classify",
            "Repair edges",
            "Document like new HCS",
            "New grouted/shear-pocket connections",
        ],
        "source_url": "https://standard.no/en/sectors/byggevarer/norwegian-standard-for-hollow-core-slabs-for-reuse--ns-3682/",
        "suggested_graph_action": "Treat NS 3682 as the reference ontology pattern for all HCS rows; add FullScaleTestRate and CarbonationDepthTrigger.",
    },
    {
        "rank": 12,
        "country_iso": "DE",
        "country_name": "Deutschland",
        "land_id": "land_deutschland",
        "material": "Holz",
        "material_id": "mat_holz",
        "priority": "P2_High",
        "project_cluster": "High-count timber reuse",
        "key_norms": [
            "Eurocode 5",
            "DIN EN 14081",
            "DIN EN 338",
            "DIN 4074",
            "DIN 68800",
        ],
        "legal_conditions": [
            "CE/DoP gap for reclaimed graded timber",
            "German waste-wood restrictions if contaminated",
            "Proof of fitness for structural use",
        ],
        "required_tests": [
            "Species",
            "Grade",
            "Dimensions",
            "Moisture",
            "Density/stiffness NDT",
            "Biological attack",
            "Holes/notches",
            "Fastener damage",
            "Fire/charring",
        ],
        "pollutant_risks": [
            "PCP",
            "Lindane",
            "Creosote",
            "CCA",
            "Lead paint",
            "Formaldehyde",
            "Mold",
            "Asbestos dust",
        ],
        "processing_methods": [
            "De-nailing",
            "Trimming",
            "Planing",
            "Kiln drying",
            "Sorting",
            "Regrading",
            "Surface treatment",
            "Traceable storage",
        ],
        "source_url": "https://www.iom3.org/asset/E62529EE-C75E-47E8-BE09F55791407110/",
        "suggested_graph_action": "Create ReclaimedStructuralTimber class with mandatory StrengthGradingEvidence and WoodPreservativeScreening.",
    },
    {
        "rank": 13,
        "country_iso": "NL",
        "country_name": "Niederlande",
        "land_id": "land_niederlande",
        "material": "Holz",
        "material_id": "mat_holz",
        "priority": "P2_High",
        "project_cluster": "Dutch timber reuse / circular building",
        "key_norms": [
            "Eurocode 5",
            "NEN EN 14081",
            "NEN EN 338",
            "NEN fire/moisture rules",
            "CB'23 passports",
        ],
        "legal_conditions": [
            "Bbl compliance",
            "CE status if re-marketed",
            "CB'23 quality passport",
        ],
        "required_tests": [
            "Visual/NDT grading",
            "Moisture",
            "Stiffness",
            "Species",
            "Decay/insect attack",
            "Connection-hole damage",
        ],
        "pollutant_risks": [
            "Wood preservatives",
            "Lead paint",
            "Mold",
            "Formaldehyde",
            "Asbestos dust",
        ],
        "processing_methods": [
            "De-nail",
            "Trim",
            "Plane",
            "Dry",
            "Regrade",
            "Passport",
            "Reversible screw/bolt detailing",
        ],
        "source_url": "https://platformcb23.nl/wp-content/uploads/PlatformCB23_guide_Quality-assessment-and-assurance-when-reusing-products-from-existing-structures_June2023.pdf",
        "suggested_graph_action": "Link MaterialPassport to TimberStrengthGrade, MoistureClass, ServiceClass, BiologicalDurability.",
    },
    {
        "rank": 14,
        "country_iso": "BE",
        "country_name": "Belgien",
        "land_id": "land_belgien",
        "material": "Holz",
        "material_id": "mat_holz",
        "priority": "P2_High",
        "project_cluster": "Belgian reclaimed timber / FCRBE market",
        "key_norms": [
            "Eurocode 5",
            "NBN EN 14081",
            "NBN EN 338",
            "Fire/durability rules",
        ],
        "legal_conditions": [
            "Product-vs-waste boundary",
            "Tracimat inventory",
            "CPR/CE ambiguity",
        ],
        "required_tests": [
            "Strength grading",
            "Moisture",
            "Decay",
            "Species",
            "Previous load/damage",
            "Connection defects",
        ],
        "pollutant_risks": [
            "PCP/lindane",
            "Creosote",
            "Lead paint",
            "Asbestos contamination",
            "Mold",
        ],
        "processing_methods": [
            "Careful salvage",
            "De-nailing",
            "Trimming",
            "Planing",
            "Drying",
            "Batch sorting",
        ],
        "source_url": "https://opalis.eu/sites/default/files/2023-10/en_id2023_fcrbe_finition_web.pdf",
        "suggested_graph_action": "Add BelgianReclamationAudit edge to timber components before ReusePotential = structural.",
    },
    {
        "rank": 15,
        "country_iso": "CH",
        "country_name": "Schweiz",
        "land_id": "land_schweiz",
        "material": "Holz",
        "material_id": "mat_holz",
        "priority": "P2_High",
        "project_cluster": "Swiss timber reuse",
        "key_norms": [
            "SIA 265",
            "Eurocode-related timber product standards",
            "Fire/moisture/durability requirements",
        ],
        "legal_conditions": [
            "BauPG status",
            "Cantonal approval",
            "Contractual allocation of reuse liability",
        ],
        "required_tests": [
            "Species",
            "Moisture",
            "Strength grading/NDT",
            "Decay",
            "Insect attack",
            "Dimensional stability",
            "Connection-hole damage",
        ],
        "pollutant_risks": [
            "PCP",
            "Lindane",
            "Creosote",
            "Formaldehyde",
            "Mold",
            "Asbestos dust",
            "Lead paint",
        ],
        "processing_methods": [
            "De-nailing",
            "Trimming",
            "Planing",
            "Drying",
            "Regrading",
            "Reversible dry joints",
        ],
        "source_url": "https://www.cirkla.ch/en/publications-outils/projet-innosuisse/",
        "suggested_graph_action": "Add SIA265PerformanceRequirement and ContractualWarrantyAllocation properties.",
    },
    {
        "rank": 16,
        "country_iso": "BE",
        "country_name": "Belgien",
        "land_id": "land_belgien",
        "material": "Naturstein",
        "material_id": "mat_naturstein",
        "priority": "P2_High",
        "project_cluster": "Belgian stone floors, stairs, façade elements",
        "key_norms": [
            "EN 12058",
            "EN 1469",
            "EN 1341",
            "EN 12371",
            "EN 12372",
            "EN 14231",
            "EN 1936",
            "EN 13755",
        ],
        "legal_conditions": [
            "CPR/CE if placed on market",
            "Product-vs-waste",
            "Tracimat/predemolition inventory",
        ],
        "required_tests": [
            "Petrography",
            "Flexural strength",
            "Slip resistance",
            "Frost resistance",
            "Water absorption",
            "Dimensions",
            "Anchor-pullout for cladding",
        ],
        "pollutant_risks": [
            "Asbestos backing/mastic",
            "PAH/tar adhesives",
            "Salts",
            "Oils",
            "Heavy metals",
        ],
        "processing_methods": [
            "Careful dismantling",
            "Cleaning",
            "Cut-to-size",
            "Surface refinish",
            "Redrilling anchors",
            "Batch grading",
        ],
        "source_url": "https://opalis.eu/sites/default/files/2022-01/4.10_en_-_natural_stone_flooring_slab_v01_0.pdf",
        "suggested_graph_action": "Create ReclaimedNaturalStoneSlab with application-specific tests: floor = slip/abrasion; exterior = frost; façade = anchor/flexural.",
    },
    {
        "rank": 17,
        "country_iso": "CH",
        "country_name": "Schweiz",
        "land_id": "land_schweiz",
        "material": "Naturstein",
        "material_id": "mat_naturstein",
        "priority": "P2_High",
        "project_cluster": "Swiss stone façades/floors",
        "key_norms": [
            "EN/SN 12058",
            "EN/SN 1469",
            "SIA façade/anchorage rules",
        ],
        "legal_conditions": [
            "BauPG",
            "Canton permitting",
            "VVEA if waste",
            "Pollutant-remediation duties",
        ],
        "required_tests": [
            "Petrography",
            "Flexural",
            "Frost",
            "Slip",
            "Water absorption",
            "Anchor condition",
            "Cracks/delamination",
        ],
        "pollutant_risks": [
            "Asbestos adhesives",
            "PAH",
            "Salts",
            "Oils",
            "Heavy metals",
        ],
        "processing_methods": [
            "Dismantle",
            "Clean",
            "Saw",
            "Refinish",
            "Redrill",
            "Mechanical anchors/clips",
        ],
        "source_url": "https://cdn.standards.iteh.ai/samples/11505/3673463ce1514a2ebf23dd8d24690556/SIST-EN-12058-2004.pdf",
        "suggested_graph_action": "Add StoneApplicationContext node so the graph does not reuse floor-slab data for façade anchorage without extra proof.",
    },
    {
        "rank": 18,
        "country_iso": "GB",
        "country_name": "Vereinigtes Königreich",
        "land_id": "land_vereinigtes_koenigreich",
        "material": "Holz",
        "material_id": "mat_holz",
        "priority": "P2_High",
        "project_cluster": "Secondary UK timber reuse cluster",
        "key_norms": [
            "Eurocode 5 / UK NA",
            "BS 4978",
            "EN 14081",
            "EN 338",
            "Fire/moisture rules",
        ],
        "legal_conditions": [
            "Building Control Part A",
            "CDM/waste duty",
            "UKCA/CE if re-marketed",
        ],
        "required_tests": [
            "Visual/NDT grading",
            "Moisture",
            "Species",
            "Stiffness",
            "Decay",
            "Fastener-hole damage",
            "Fire performance",
        ],
        "pollutant_risks": [
            "Lead paint",
            "Creosote",
            "PCP/lindane",
            "Mold",
            "Asbestos contamination",
        ],
        "processing_methods": [
            "De-nail",
            "Trim",
            "Plane",
            "Dry",
            "Regrade",
            "New bolted/screwed reversible joints",
        ],
        "source_url": "https://www.gov.uk/government/publications/structure-approved-document-a",
        "suggested_graph_action": "Add UK BuildingControlEvidence edge from timber element to structural calculations and inspection records.",
    },
    {
        "rank": 19,
        "country_iso": "DE",
        "country_name": "Deutschland",
        "land_id": "land_deutschland",
        "material": "Ziegel",
        "material_id": "mat_ziegel",
        "priority": "P2_High",
        "project_cluster": "German brick/masonry reuse",
        "key_norms": [
            "EN 771-1",
            "EN 772",
            "Eurocode 6",
            "DIN EN 1996",
            "EN 998",
            "Frost rules",
        ],
        "legal_conditions": [
            "Product-vs-waste",
            "CE if marketed as masonry unit",
            "Heritage vs new-build use",
            "Landfill/waste if contaminated",
        ],
        "required_tests": [
            "Compressive strength",
            "Dimensions",
            "Water absorption",
            "Frost resistance",
            "Soluble salts",
            "Bond strength with new mortar",
        ],
        "pollutant_risks": [
            "Soot",
            "Salts",
            "Lead paint/glaze",
            "PAH/tar",
            "Asbestos-containing mortars/adhesives",
        ],
        "processing_methods": [
            "Mortar removal",
            "Cleaning",
            "Sorting",
            "Grading",
            "Palletising",
            "Lime-mortar reuse detailing",
        ],
        "source_url": "https://opalis.eu/sites/default/files/2022-01/2.40_en_-_reclaimed_solid_terracotta_brick_v01_0.pdf",
        "suggested_graph_action": "Add ReclaimedBrickBatch with MortarTypeRemoved, SaltRisk, FrostExposureClass, MasonryDesignStrength.",
    },
    {
        "rank": 20,
        "country_iso": "DE",
        "country_name": "Deutschland",
        "land_id": "land_deutschland",
        "material": "Lehm",
        "material_id": "mat_lehm",
        "priority": "P2_High",
        "project_cluster": "German earth/clay reuse",
        "key_norms": [
            "DIN 18940",
            "DIN 18945",
            "DIN 18946",
            "DIN 18947",
            "Eurocode-adjacent structural verification",
            "Fire/moisture rules",
        ],
        "legal_conditions": [
            "Non-harmonised product status",
            "Project-specific approval",
            "Indoor-air/moisture responsibility",
        ],
        "required_tests": [
            "Clay content",
            "Grain size",
            "Compressive strength",
            "Shrinkage",
            "Erosion/water sensitivity",
            "Moisture sorption",
            "Microbial contamination",
        ],
        "pollutant_risks": [
            "Mold",
            "Salts",
            "Organic contamination",
            "Old paints",
            "Asbestos dust from mixed demolition",
        ],
        "processing_methods": [
            "Crush",
            "Sieve",
            "Rehydrate",
            "Reform blocks/plasters",
            "Dry",
            "Stabilize only where reversible/permitted",
        ],
        "source_url": "https://www.dibt.de/en/service/faqs/the-german-regulatory-system-for-construction-products-and-construction-techniques",
        "suggested_graph_action": "Create EarthenMaterialReuse branch distinct from brick/concrete; add MoistureSensitivityRequirement and ReversibleStabilisation properties.",
    },
]


def _enrich_rule_rows() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]
]:
    """Compute id, name, and the derived norm tables from REUSE_RULE_ROWS."""

    rule_rows: list[dict[str, Any]] = []
    norm_rows_idx: dict[str, str] = {}
    referenziert_rows: list[dict[str, Any]] = []

    for row in REUSE_RULE_ROWS:
        material_slug = _slug(row["material"])
        rid = f"rr_{row['country_iso'].lower()}_{material_slug}"
        name = f"{row['country_name']} × {row['material']} reuse rule"
        rule = {
            "id": rid,
            "name": name,
            "rank": row["rank"],
            "country_iso": row["country_iso"],
            "country_name": row["country_name"],
            "land_id": row["land_id"],
            "material": row["material"],
            "material_id": row["material_id"],
            "priority": row["priority"],
            "project_cluster": row["project_cluster"],
            "key_norms": row["key_norms"],
            "legal_conditions": row["legal_conditions"],
            "required_tests": row["required_tests"],
            "pollutant_risks": row["pollutant_risks"],
            "processing_methods": row["processing_methods"],
            "source_url": row["source_url"],
            "suggested_graph_action": row["suggested_graph_action"],
        }
        rule_rows.append(rule)
        for norm_name in row["key_norms"]:
            nid = _norm_id(norm_name)
            norm_rows_idx[nid] = norm_name
            referenziert_rows.append({"rule_id": rid, "norm_id": nid})

    norm_rows = [
        {"norm_id": nid, "norm_name": name} for nid, name in sorted(norm_rows_idx.items())
    ]
    return rule_rows, norm_rows, referenziert_rows


# ---------------------------------------------------------------------------
#  Cypher loader: strip comments, split on ';', drop empties.
# ---------------------------------------------------------------------------


def _load_statements(path: Path) -> list[str]:
    raw = path.read_text(encoding="utf-8")
    stripped: list[str] = []
    for line in raw.splitlines():
        if line.lstrip().startswith("//"):
            continue
        idx = line.find("//")
        if idx >= 0:
            line = line[:idx].rstrip()
        stripped.append(line)
    body = "\n".join(stripped)
    parts = [s.strip() for s in body.split(";")]
    return [s for s in parts if s]


# ---------------------------------------------------------------------------
#  Counts / probes shared by all three phases
# ---------------------------------------------------------------------------


def _now() -> str:
    return datetime.now(tz=timezone.utc).isoformat(timespec="seconds")


def _log(progress: list[str], msg: str) -> None:
    line = f"{_now()}  {msg}"
    progress.append(line)
    print(line, flush=True)


def _counts(session) -> dict[str, Any]:
    def s_one(q: str, **params: Any) -> Any:
        rec = session.run(q, **params).single()
        return rec.value() if rec is not None else 0

    out = {
        "total_nodes": s_one("MATCH (n) RETURN count(n)"),
        "total_rels": s_one("MATCH ()-[r]->() RETURN count(r)"),
        "bauwerk_total": s_one("MATCH (b:Bauwerk) RETURN count(b)"),
        "materialdepot_total": s_one("MATCH (m:Materialdepot) RETURN count(m)"),
        "bauwerk_era_total": s_one("MATCH (e:BauwerkEra) RETURN count(e)"),
        "built_in_era_total": s_one(
            "MATCH ()-[r:BUILT_IN_ERA]->() RETURN count(r)"
        ),
        "built_in_era_from_bauwerk": s_one(
            "MATCH (:Bauwerk)-[r:BUILT_IN_ERA]->(:BauwerkEra) RETURN count(r)"
        ),
        "built_in_era_from_materialdepot": s_one(
            "MATCH (:Materialdepot)-[r:BUILT_IN_ERA]->(:BauwerkEra) RETURN count(r)"
        ),
        "bauwerk_era_unknown": s_one(
            "MATCH (b:Bauwerk) WHERE b.era_unknown = true RETURN count(b)"
        ),
        "materialdepot_era_unknown": s_one(
            "MATCH (m:Materialdepot) WHERE m.era_unknown = true RETURN count(m)"
        ),
        "hat_schadstoff_total": s_one(
            "MATCH ()-[r:HAT_SCHADSTOFF]->() RETURN count(r)"
        ),
        "has_risk_pollutant_total": s_one(
            "MATCH ()-[r:HAS_RISK_POLLUTANT]->() RETURN count(r)"
        ),
        "requires_verification_for_total": s_one(
            "MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() RETURN count(r)"
        ),
        "reuse_rule_total": s_one("MATCH (r:ReuseRule) RETURN count(r)"),
        "applies_in_total": s_one(
            "MATCH (:ReuseRule)-[r:APPLIES_IN]->(:Land) RETURN count(r)"
        ),
        "applies_to_total": s_one(
            "MATCH (:ReuseRule)-[r:APPLIES_TO]->(:Material) RETURN count(r)"
        ),
        "referenziert_norm_from_rule": s_one(
            "MATCH (:ReuseRule)-[r:REFERENZIERT_NORM]->(:Norm) RETURN count(r)"
        ),
        "norm_total": s_one("MATCH (n:Norm) RETURN count(n)"),
        "land_with_iso": s_one(
            "MATCH (l:Land) WHERE l.country_iso IS NOT NULL RETURN count(l)"
        ),
        "has_risk_pollutant_by_basis": {
            r["basis"]: r["c"]
            for r in session.run(
                "MATCH ()-[r:HAS_RISK_POLLUTANT]->() "
                "RETURN r.evidence_basis AS basis, count(r) AS c"
            )
        },
        "requires_verification_for_by_basis": {
            r["basis"]: r["c"]
            for r in session.run(
                "MATCH ()-[r:REQUIRES_VERIFICATION_FOR]->() "
                "RETURN r.pollutant_basis AS basis, count(r) AS c"
            )
        },
    }
    return out


# ---------------------------------------------------------------------------
#  Driver glue
# ---------------------------------------------------------------------------


def _resolve() -> tuple[str, str, str, str]:
    sys.path.insert(0, str(REPO_ROOT / "_scripts"))
    from neo4j_env import resolve_connection  # type: ignore

    uri, user, pw, db = resolve_connection()
    if db != "mit-bestand":
        db = "mit-bestand"
    return uri, user, pw, db


def _exec_file(session, path: Path, params: dict[str, Any] | None, progress: list[str]) -> list[dict[str, Any]]:
    audits: list[dict[str, Any]] = []
    params = params or {}
    statements = _load_statements(path)
    _log(progress, f"running {path.name}: {len(statements)} statements")
    for i, stmt in enumerate(statements, start=1):
        try:
            result = session.run(stmt, **params)
            keys = result.keys()
            if keys and (keys[0] == "check"):
                for rec in result:
                    audits.append({"file": path.name, "stmt": i, "audit": dict(rec)})
            else:
                result.consume()
        except Exception as exc:
            snippet = stmt[:280].replace("\n", " ")
            _log(progress, f"  stmt {i} FAILED: {snippet} -> {exc}")
            raise
    return audits


def main() -> int:
    from neo4j import GraphDatabase  # type: ignore

    progress: list[str] = []
    result: dict[str, Any] = {
        "agent": 11,
        "phases": ["3.1", "3.2", "3.3"],
        "started_at": _now(),
    }
    try:
        uri, user, pw, db = _resolve()
        drv = GraphDatabase.driver(uri, auth=(user, pw))
        rule_rows, norm_rows, referenziert_norm_rows = _enrich_rule_rows()
        _log(
            progress,
            f"connect uri={uri} db={db} rules={len(rule_rows)} norm_anchors={len(norm_rows)} "
            f"referenziert={len(referenziert_norm_rows)}",
        )
        with drv.session(database=db) as session:
            result["before"] = _counts(session)
            _log(progress, f"before counts: {json.dumps(result['before'])}")

            audits: dict[str, list[dict[str, Any]]] = {}

            _log(progress, "------- Phase 3.1 -------")
            audits["3.1"] = _exec_file(session, MIG_3_1, None, progress)
            result["after_3_1"] = _counts(session)
            _log(progress, f"after 3.1: {json.dumps(result['after_3_1'])}")

            _log(progress, "------- Phase 3.2 -------")
            audits["3.2"] = _exec_file(session, MIG_3_2, None, progress)
            result["after_3_2"] = _counts(session)
            _log(progress, f"after 3.2: {json.dumps(result['after_3_2'])}")

            _log(progress, "------- Phase 3.3 -------")
            audits["3.3"] = _exec_file(
                session,
                MIG_3_3,
                {
                    "rule_rows": rule_rows,
                    "norm_rows": norm_rows,
                    "referenziert_norm_rows": referenziert_norm_rows,
                },
                progress,
            )
            result["after_3_3"] = _counts(session)
            _log(progress, f"after 3.3: {json.dumps(result['after_3_3'])}")

            result["audits"] = audits
        drv.close()
        result["completed_at"] = _now()
        result["status"] = "ok"
    except Exception:
        result["status"] = "error"
        result["error"] = traceback.format_exc()
        _log(progress, "FAILED")
        _log(progress, result["error"])
    finally:
        LOGS_DIR.mkdir(parents=True, exist_ok=True)
        RESULT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
        PROG.write_text("\n".join(progress) + "\n", encoding="utf-8")
        print(f"wrote {RESULT}")
        print(f"wrote {PROG}")
    return 0 if result.get("status") == "ok" else 1


if __name__ == "__main__":
    sys.exit(main())
