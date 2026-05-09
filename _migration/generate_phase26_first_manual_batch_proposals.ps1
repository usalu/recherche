$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$proposalCsvPath = Join-Path $root "_migration/26_first_manual_batch_edge_proposals.csv"
$reportPath = Join-Path $root "_migration/26_First_Manual_Batch_Proposals.md"

$batchTargets = @(
    "material/Metall",
    "huerde/Performance_Nachweis",
    "bauteiltyp/Tragstruktur",
    "bauteiltyp/Bauwerksteil",
    "huerde/Logistikproblem"
)

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

function New-Proposal {
    param(
        [string]$Action,
        [string]$Target,
        [string]$Relation,
        [string]$Confidence,
        [string]$Note
    )
    return [PSCustomObject]@{
        proposed_action = $Action
        proposed_target = $Target
        proposed_relation = $Relation
        proposal_confidence = $Confidence
        reviewer_note = $Note
    }
}

function Suggest-EdgeDecision {
    param([object]$Edge)

    $target = $Edge.target
    $raw = Normalize-Text $Edge.raw_label

    if ($target -eq "material/Metall") {
        if ($raw -match "aluminium" -and $raw -match "stahl") {
            return New-Proposal "approve_split" "material/Aluminium; material/Stahl" "uses_material" "REVIEW" "Exact metals appear, but the source is mixed/uncertain; verify whether both should be linked."
        }
        if ($raw -match "aluminium") {
            return New-Proposal "approve_move" "material/Aluminium" "uses_material" "CONFIDENT_IF_SOURCE_CLEAR" "Use Aluminium only when the raw source names aluminium as the actual reused material."
        }
        if ($raw -match "stahl") {
            return New-Proposal "approve_move" "material/Stahl" "uses_material" "CONFIDENT_IF_SOURCE_CLEAR" "Use Stahl when the raw source names steel; keep Metall only if steel is merely an example."
        }
        if ($raw -match "unbekannt|gemischt|sonstige|elektro|technik|photovoltaik|kunststoff|holz|glas|keramik|metall / unbekannt") {
            return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Mixed or unknown material bundle; do not create broad material/Metall edge automatically."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Raw label says only Metall; approve only if you accept Metall as a deliberate fallback."
    }

    if ($target -eq "huerde/Performance_Nachweis") {
        if ($raw -match "gewährleistung|gewaehrleistung") {
            if ($raw -match "hygiene") {
                return New-Proposal "approve_split" "huerde/Gewaehrleistung; huerde/Hygieneanforderung" "has_huerde" "CONFIDENT_IF_SOURCE_CLEAR" "This is a warranty/hygiene barrier, not a proof type."
            }
            return New-Proposal "approve_move" "huerde/Gewaehrleistung" "has_huerde" "CONFIDENT_IF_SOURCE_CLEAR" "This is a warranty barrier, not Performance_Nachweis."
        }
        if ($raw -match "hygiene") {
            return New-Proposal "approve_move" "huerde/Hygieneanforderung" "has_huerde" "CONFIDENT_IF_SOURCE_CLEAR" "Hygiene is an explicit requirement/barrier."
        }
        if ($raw -match "brandschutz|feuer") {
            return New-Proposal "approve_split" "huerde/Brandschutzkonflikt; leistungsanforderung/Brandschutz" "has_huerde; has_leistungsanforderung" "REVIEW" "Separate the barrier from the performance requirement."
        }
        if ($raw -match "leistungsnachweis|werkszeugnis|leistung nicht belegt|herkunft und leistung|unbekannte werte") {
            return New-Proposal "approve_move" "huerde/Technische_Freigabe" "has_huerde" "CONFIDENT_IF_SOURCE_CLEAR" "The barrier is missing/uncertain proof or approval."
        }
        if ($raw -match "dichtheit|feuchte|korrosion|dauerhaft") {
            return New-Proposal "approve_split" "huerde/Dauerhaftigkeit_Restlebensdauer; leistungsanforderung/Feuchteschutz" "has_huerde; has_leistungsanforderung" "REVIEW" "Potential durability/fitness issue; check exact source context."
        }
        if ($raw -match "test|stabilität|stabilitaet|eignung|performance|maße|masse") {
            return New-Proposal "approve_move" "huerde/Technische_Freigabe" "has_huerde" "REVIEW" "Likely technical approval/proof barrier, but verify whether a pruefung_nachweis edge is better."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Unclear proof/performance barrier; review manually."
    }

    if ($target -eq "bauteiltyp/Tragstruktur") {
        if ($raw -match "dachtragwerk") {
            return New-Proposal "approve_move" "tragwerkstyp/Dachtragwerk" "has_tragwerkstyp" "CONFIDENT_IF_SOURCE_CLEAR" "Dachtragwerk is a structural type, not bauteiltyp."
        }
        if ($raw -match "holz") {
            return New-Proposal "approve_move" "tragwerkstyp/Holztragwerk" "has_tragwerkstyp" "REVIEW" "Material-derived structural system; verify whether Holz-Skeletttragwerk is more exact."
        }
        if ($raw -match "stahl") {
            return New-Proposal "create_or_review" "tragwerkstyp/Stahltragwerk" "has_tragwerkstyp" "REVIEW" "A generic Stahltragwerk node may be needed; current clean ontology only has Stahl_Skeletttragwerk."
        }
        if ($raw -match "beton|concrete") {
            return New-Proposal "approve_move" "tragwerkstyp/Ortbetontragwerk" "has_tragwerkstyp" "REVIEW" "Concrete structure; verify whether it is in-situ, frame, or slab system."
        }
        if ($raw -match "aussteifung|bracing|kern") {
            return New-Proposal "approve_move" "tragwerksprinzip/Wand_Kern_Tragwerk" "has_tragwerksprinzip" "REVIEW" "Likely bracing/core structural principle; source context required."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Tragstruktur is too broad; derive system/principle/component from source."
    }

    if ($target -eq "bauteiltyp/Bauwerksteil") {
        if ($raw -match "garagentor|\btor\b|tür|tuer") {
            return New-Proposal "approve_move" "bauteiltyp/Tuer" "has_bauteiltyp" "REVIEW" "Door/gate-like component; verify if it is actually a whole facade/object."
        }
        if ($raw -match "strohbau|holz-/stroh|holz-\/stroh") {
            return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Bauweise/material bundle, not a component type; decide whether to model as material, bauweise, or bauobjekt context."
        }
        if ($raw -match "betonrahmen|concrete frame|betonstruktur|\brohbau\b") {
            return New-Proposal "approve_split" "tragwerkstyp/Ortbetontragwerk; tragwerksprinzip/Skeletttragwerk" "has_tragwerkstyp; has_tragwerksprinzip" "REVIEW" "This is structural object/system scale, not a reusable component family."
        }
        if ($raw -match "gebäude|gebaeude|pavillon|garage|bestand|block|residence|lagerhaus|ensemble|hall|krypta|kreuzgang") {
            return New-Proposal "delete_or_object_relation" "bauobjekt/*" "relates_to_bauobjekt" "REVIEW" "Whole object/building-part scale; model as bauobjekt or bauobjekt_beteiligung, not bauteiltyp."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Bauwerksteil is too broad; decide object scale vs component scale from source."
    }

    if ($target -eq "huerde/Logistikproblem") {
        if ($raw -match "lager|zwischenlager|lagerfläche|lagerflaeche") {
            return New-Proposal "approve_move" "huerde/Fehlende_Lagerflaeche" "has_huerde" "CONFIDENT_IF_SOURCE_CLEAR" "Storage issue is a concrete logistics barrier."
        }
        if ($raw -match "transport") {
            return New-Proposal "approve_move" "huerde/Terminunsicherheit" "has_huerde" "REVIEW" "Transport may be schedule/logistics or just process phase; verify exact barrier."
        }
        if ($raw -match "liefer|verfügbar|verfuegbar|supply") {
            return New-Proposal "approve_move" "huerde/Verfuegbarkeitsproblem" "has_huerde" "CONFIDENT_IF_SOURCE_CLEAR" "Availability/supply problem is more precise than Logistikproblem."
        }
        if ($raw -match "passung|maß|masse|toleranz") {
            return New-Proposal "approve_move" "huerde/Toleranzen" "has_huerde" "REVIEW" "Fit/tolerance issue; verify if compatibility is more exact."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Logistikproblem is broad; map only if a concrete logistics barrier is visible."
    }

    return New-Proposal "not_in_first_batch" "" "" "REVIEW_REQUIRED" "Target is outside first manual batch."
}

$rows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $batchTargets -contains $_.target })

$proposals = foreach ($row in $rows) {
    $proposal = Suggest-EdgeDecision $row
    [PSCustomObject]@{
        source = $row.source
        relation = $row.relation
        target = $row.target
        raw_label = $row.raw_label
        legacy_path = $row.legacy_path
        proposed_action = $proposal.proposed_action
        proposed_target = $proposal.proposed_target
        proposed_relation = $proposal.proposed_relation
        proposal_confidence = $proposal.proposal_confidence
        reviewer_note = $proposal.reviewer_note
    }
}

$proposals |
    Sort-Object target, proposed_action, raw_label, source |
    Export-Csv -LiteralPath $proposalCsvPath -NoTypeInformation -Encoding UTF8

$summaryByTarget = $proposals |
    Group-Object target |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$summaryByAction = $proposals |
    Group-Object proposed_action |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$highConfidence = @($proposals | Where-Object { $_.proposal_confidence -like "CONFIDENT*" }).Count
$review = @($proposals | Where-Object { $_.proposal_confidence -eq "REVIEW" -or $_.proposal_confidence -eq "REVIEW_REQUIRED" }).Count

$report = @()
$report += "# Phase 26 First Manual Batch Proposals"
$report += ""
$report += "## Scope"
$report += ""
$report += "Proposal-only pass for the five highest-impact review targets. No nodes or edges were migrated."
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/26_first_manual_batch_edge_proposals.csv"
$report += ""
$report += "## Counts"
$report += ""
$report += "- Proposed edge decisions: $($proposals.Count)"
$report += "- High-confidence-if-source-clear proposals: $highConfidence"
$report += "- Still review-required proposals: $review"
$report += ""
$report += "## By Target"
$report += ""
$report += "| target | rows |"
$report += "|---|---:|"
$report += $summaryByTarget
$report += ""
$report += "## By Proposed Action"
$report += ""
$report += "| action | rows |"
$report += "|---|---:|"
$report += $summaryByAction
$report += ""
$report += "## How To Use"
$report += ""
$report += "1. Open the CSV."
$report += "2. Filter by `proposal_confidence = CONFIDENT_IF_SOURCE_CLEAR` first."
$report += "3. Check the source file before approving."
$report += "4. Keep anything mixed, broad, or uncertain in review."
$report += ""
$report += "## Important"
$report += ""
$report += "These are not automatic migration rules. They are a review aid."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $proposalCsvPath"
Write-Output "Wrote $reportPath"
