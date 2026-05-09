$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$decisionCsvPath = Join-Path $root "_migration/31_bauteiltyp_bauwerksteil_edge_review_decisions.csv"
$reportPath = Join-Path $root "_migration/31_Bauteiltyp_Bauwerksteil_Review_Decision.md"

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$reviewRows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $_.target -eq "bauteiltyp/Bauwerksteil" })

$decisions = foreach ($row in $reviewRows) {
    $existingEdges = @($cleanEdges |
        Where-Object {
            $_.source -eq $row.source -and
            $_.relation -in @("has_bauteiltyp", "has_tragwerkstyp", "has_tragwerksprinzip", "installed_in_bauobjekt", "uses_material")
        } |
        ForEach-Object { "$($_.relation)->$($_.target)" } |
        Select-Object -Unique |
        Sort-Object)

    $raw = Normalize-Text $row.raw_label
    $decision = "keep_review_resolve_scale"
    $suggestedTargets = ""
    $suggestedRelations = ""
    $rationale = "Bauwerksteil is too broad; decide whether this is object scale, structural system, or precise component."

    if ($raw -match "garagentor") {
        $decision = "candidate_precise_component"
        $suggestedTargets = "bauteiltyp/Tuer"
        $suggestedRelations = "has_bauteiltyp"
        $rationale = "Garagentor is a door/gate component, not a whole Bauwerksteil."
    }
    elseif ($raw -match "betonrahmen|concrete frame|betonstruktur|bestands.*betonstruktur") {
        $decision = "candidate_structural_system"
        $suggestedTargets = "tragwerkstyp/Ortbetontragwerk; tragwerksprinzip/Skeletttragwerk"
        $suggestedRelations = "has_tragwerkstyp; has_tragwerksprinzip"
        $rationale = "Concrete frame/structure is structural-system scale."
    }
    elseif ($raw -match "strohbau|holz-/stroh|holz-\/stroh") {
        $decision = "case_context_required"
        $suggestedTargets = "bauweise/*; material/Holz; material/Stroh"
        $suggestedRelations = "has_bauweise; uses_material"
        $rationale = "Holz-/Strohbau is construction/material context, not a component type."
    }
    elseif ($raw -match "\brohbau\b") {
        $decision = "candidate_structural_system"
        $suggestedTargets = "tragwerkstyp/*"
        $suggestedRelations = "has_tragwerkstyp"
        $rationale = "Rohbau is object/system scale; exact structure must be checked."
    }
    elseif ($raw -match "gebäude|gebaeude|pavillon|garage|schuppen|lagerhaus|bestand|block|residence|ensemble|krypta|kreuzgang|observatorium|kuppel|gewächshaus|gewaechshaus|glasgang|glaskubus|würfel|wuerfel") {
        $decision = "object_scale_not_component"
        $suggestedTargets = "bauobjekt/* or bauobjekt_beteiligung/*"
        $suggestedRelations = "relates_to_bauobjekt"
        $rationale = "The raw label points to a building, object, or object part; do not model as bauteiltyp."
    }
    elseif ($raw -match "galerie|innenausbau|box|wohnungsteile|units|ramp|pier|wasserbecken|kolonnade") {
        $decision = "case_context_required"
        $suggestedTargets = "bauobjekt/* or precise bauteiltyp/*"
        $suggestedRelations = "relates_to_bauobjekt or has_bauteiltyp"
        $rationale = "Could be object-scale or component-scale depending on source context."
    }

    [PSCustomObject]@{
        source = $row.source
        old_relation = $row.relation
        old_target = $row.target
        raw_label = $row.raw_label
        existing_clean_edges = ($existingEdges -join "; ")
        bauwerksteil_decision = $decision
        suggested_target = $suggestedTargets
        suggested_relation = $suggestedRelations
        database_change = "none"
        rationale = $rationale
        legacy_path = $row.legacy_path
    }
}

$decisions |
    Sort-Object bauwerksteil_decision, raw_label, source |
    Export-Csv -LiteralPath $decisionCsvPath -NoTypeInformation -Encoding UTF8

$byDecision = $decisions |
    Group-Object bauwerksteil_decision |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$examples = $decisions |
    Sort-Object bauwerksteil_decision, raw_label, source |
    Select-Object -First 12 |
    ForEach-Object { "| $($_.raw_label) | $($_.existing_clean_edges) | $($_.bauwerksteil_decision) | $($_.suggested_target) |" }

$report = @()
$report += "# Phase 31 Bauteiltyp Bauwerksteil Review Decision"
$report += ""
$report += "## Decision"
$report += ""
$report += "Keep bauteiltyp/Bauwerksteil out of the clean database."
$report += ""
$report += "Reason: Bauwerksteil is usually object scale or system scale, not a reusable component family."
$report += ""
$report += "## Database Change"
$report += ""
$report += "No database nodes or clean edges were added. The held edges need case-level decisions."
$report += ""
$report += "## Counts"
$report += ""
$report += "- Held bauteiltyp/Bauwerksteil edges reviewed: $($decisions.Count)"
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
$report += "- _migration/31_bauteiltyp_bauwerksteil_edge_review_decisions.csv"

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $decisionCsvPath"
Write-Output "Wrote $reportPath"
