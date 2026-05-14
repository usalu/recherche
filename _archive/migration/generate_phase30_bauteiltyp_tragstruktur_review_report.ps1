$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$decisionCsvPath = Join-Path $root "_migration/30_bauteiltyp_tragstruktur_edge_review_decisions.csv"
$reportPath = Join-Path $root "_migration/30_Bauteiltyp_Tragstruktur_Review_Decision.md"

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$reviewRows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $_.target -eq "bauteiltyp/Tragstruktur" })

$decisions = foreach ($row in $reviewRows) {
    $existingEdges = @($cleanEdges |
        Where-Object {
            $_.source -eq $row.source -and
            $_.relation -in @("has_bauteiltyp", "has_tragwerkstyp", "has_tragwerksprinzip", "uses_material")
        } |
        ForEach-Object { "$($_.relation)->$($_.target)" } |
        Select-Object -Unique |
        Sort-Object)

    $raw = Normalize-Text $row.raw_label
    $decision = "keep_review_derive_structure"
    $suggestedTargets = ""
    $suggestedRelations = ""
    $rationale = "Tragstruktur is too broad as bauteiltyp; derive a real structural entity from source context."

    if ($existingEdges -match "has_tragwerkstyp->tragwerkstyp/Dachtragwerk") {
        $decision = "covered_by_existing_tragwerkstyp"
        $rationale = "A precise Dachtragwerk edge already exists."
    }
    elseif ($raw -match "dachtragwerk") {
        $decision = "candidate_existing_tragwerkstyp"
        $suggestedTargets = "tragwerkstyp/Dachtragwerk"
        $suggestedRelations = "has_tragwerkstyp"
        $rationale = "Dachtragwerk is a structural type, not bauteiltyp."
    }
    elseif ($raw -match "stahl|bracing|aussteifung") {
        $decision = "candidate_new_or_existing_tragwerk"
        $suggestedTargets = "tragwerkstyp/Stahltragwerk or tragwerksprinzip/Skeletttragwerk"
        $suggestedRelations = "has_tragwerkstyp or has_tragwerksprinzip"
        $rationale = "Likely steel/material structure or bracing principle; current ontology may need a generic Stahltragwerk knot."
    }
    elseif ($raw -match "\bholz|holzstruktur|holzrahmen|holztragwerk|holz-/") {
        $decision = "candidate_existing_tragwerkstyp"
        $suggestedTargets = "tragwerkstyp/Holztragwerk"
        $suggestedRelations = "has_tragwerkstyp"
        $rationale = "Material-derived timber structure; verify whether Holz_Skeletttragwerk is more exact."
    }
    elseif ($raw -match "beton|concrete") {
        $decision = "candidate_existing_tragwerkstyp"
        $suggestedTargets = "tragwerkstyp/Ortbetontragwerk"
        $suggestedRelations = "has_tragwerkstyp"
        $rationale = "Concrete structural system; verify whether in-situ, precast, frame, or slab system."
    }
    elseif ($raw -match "rahmen|balken|stützen|stuetzen") {
        $decision = "covered_or_candidate_components"
        $suggestedTargets = "bauteiltyp/Traeger; bauteiltyp/Stuetze; tragwerksprinzip/Skeletttragwerk"
        $suggestedRelations = "has_bauteiltyp; has_tragwerksprinzip"
        $rationale = "The raw label names structural components/principle rather than a generic component type."
    }

    [PSCustomObject]@{
        source = $row.source
        old_relation = $row.relation
        old_target = $row.target
        raw_label = $row.raw_label
        existing_clean_edges = ($existingEdges -join "; ")
        tragstruktur_decision = $decision
        suggested_target = $suggestedTargets
        suggested_relation = $suggestedRelations
        database_change = "none"
        rationale = $rationale
        legacy_path = $row.legacy_path
    }
}

$decisions |
    Sort-Object tragstruktur_decision, raw_label, source |
    Export-Csv -LiteralPath $decisionCsvPath -NoTypeInformation -Encoding UTF8

$byDecision = $decisions |
    Group-Object tragstruktur_decision |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$examples = $decisions |
    Sort-Object tragstruktur_decision, raw_label, source |
    Select-Object -First 12 |
    ForEach-Object { "| $($_.raw_label) | $($_.existing_clean_edges) | $($_.tragstruktur_decision) | $($_.suggested_target) |" }

$report = @()
$report += "# Phase 30 Bauteiltyp Tragstruktur Review Decision"
$report += ""
$report += "## Decision"
$report += ""
$report += "Keep bauteiltyp/Tragstruktur out of the clean database."
$report += ""
$report += "Reason: Tragstruktur is not a true component type. Each case should become a structural type, structural principle, material-specific structure, or concrete component."
$report += ""
$report += "## Database Change"
$report += ""
$report += "No database nodes or clean edges were added. Some rows reveal possible future ontology knots, especially tragwerkstyp/Stahltragwerk."
$report += ""
$report += "## Counts"
$report += ""
$report += "- Held bauteiltyp/Tragstruktur edges reviewed: $($decisions.Count)"
$report += ""
$report += "| decision | rows |"
$report += "|---|---:|"
$report += $byDecision
$report += ""
$report += "## Sample Rows"
$report += ""
$report += "| raw label | existing clean edges | decision | suggested target |"
$report += "|---|---|---|---|"
$report += $examples
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/30_bauteiltyp_tragstruktur_edge_review_decisions.csv"

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $decisionCsvPath"
Write-Output "Wrote $reportPath"
