$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$decisionCsvPath = Join-Path $root "_migration/29_huerde_performance_nachweis_edge_review_decisions.csv"
$reportPath = Join-Path $root "_migration/29_Huerde_Performance_Nachweis_Review_Decision.md"

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$reviewRows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $_.target -eq "huerde/Performance_Nachweis" })

$decisions = foreach ($row in $reviewRows) {
    $existingHuerden = @($cleanEdges |
        Where-Object { $_.source -eq $row.source -and $_.relation -eq "has_huerde" } |
        Select-Object -ExpandProperty target -Unique |
        Sort-Object)

    $raw = Normalize-Text $row.raw_label
    $decision = "keep_review_split_needed"
    $suggestedTargets = ""
    $suggestedRelations = ""
    $rationale = "Performance_Nachweis mixes barrier, proof, and requirement levels; review source before importing."

    if ($existingHuerden.Count -gt 0) {
        $decision = "covered_by_existing_concrete_huerden"
        $rationale = "Concrete hurdle edges already exist; do not also import broad huerde/Performance_Nachweis."
    }
    elseif ($raw -match "gewährleistung|gewaehrleistung") {
        $decision = "candidate_precise_huerde"
        $suggestedTargets = "huerde/Gewaehrleistung"
        $suggestedRelations = "has_huerde"
        $rationale = "Raw label points to warranty/liability barrier."
    }
    elseif ($raw -match "hygiene") {
        $decision = "candidate_precise_huerde"
        $suggestedTargets = "huerde/Hygieneanforderung"
        $suggestedRelations = "has_huerde"
        $rationale = "Raw label points to hygiene requirement/barrier."
    }
    elseif ($raw -match "leistungsnachweis|werkszeugnis|unbekannte werte|herkunft und leistung|eignung|performance|test|stabilität|stabilitaet") {
        $decision = "candidate_precise_huerde"
        $suggestedTargets = "huerde/Technische_Freigabe"
        $suggestedRelations = "has_huerde"
        $rationale = "Raw label points to missing technical proof/approval."
    }
    elseif ($raw -match "dichtheit|korrosion|alter|dauerhaft") {
        $decision = "candidate_review_split"
        $suggestedTargets = "huerde/Dauerhaftigkeit_Restlebensdauer"
        $suggestedRelations = "has_huerde"
        $rationale = "Durability/rest-life issue likely, but source context should decide exact target."
    }
    elseif ($raw -match "energie") {
        $decision = "candidate_non_huerde_requirement"
        $suggestedTargets = "leistungsanforderung/Waermeschutz"
        $suggestedRelations = "has_leistungsanforderung"
        $rationale = "Energy requirement is likely a performance requirement, not a hurdle node."
    }

    [PSCustomObject]@{
        source = $row.source
        old_relation = $row.relation
        old_target = $row.target
        raw_label = $row.raw_label
        existing_clean_huerde_edges = ($existingHuerden -join "; ")
        performance_nachweis_decision = $decision
        suggested_target = $suggestedTargets
        suggested_relation = $suggestedRelations
        database_change = "none"
        rationale = $rationale
        legacy_path = $row.legacy_path
    }
}

$decisions |
    Sort-Object performance_nachweis_decision, raw_label, source |
    Export-Csv -LiteralPath $decisionCsvPath -NoTypeInformation -Encoding UTF8

$byDecision = $decisions |
    Group-Object performance_nachweis_decision |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$examples = $decisions |
    Sort-Object performance_nachweis_decision, raw_label, source |
    Select-Object -First 12 |
    ForEach-Object { "| $($_.raw_label) | $($_.existing_clean_huerde_edges) | $($_.performance_nachweis_decision) | $($_.suggested_target) |" }

$report = @()
$report += "# Phase 29 Huerde Performance Nachweis Review Decision"
$report += ""
$report += "## Decision"
$report += ""
$report += "Keep huerde/Performance_Nachweis out of the clean database."
$report += ""
$report += "Reason: the label mixes three levels: a barrier, a proof/check, and a performance requirement. Clean import needs concrete targets."
$report += ""
$report += "## Database Change"
$report += ""
$report += "No database nodes or clean edges were added. Existing concrete hurdle edges remain the clean representation where already present."
$report += ""
$report += "## Counts"
$report += ""
$report += "- Held huerde/Performance_Nachweis edges reviewed: $($decisions.Count)"
$report += ""
$report += "| decision | rows |"
$report += "|---|---:|"
$report += $byDecision
$report += ""
$report += "## Sample Rows"
$report += ""
$report += "| raw label | existing clean hurdle edges | decision | suggested target |"
$report += "|---|---|---|---|"
$report += $examples
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/29_huerde_performance_nachweis_edge_review_decisions.csv"

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $decisionCsvPath"
Write-Output "Wrote $reportPath"
