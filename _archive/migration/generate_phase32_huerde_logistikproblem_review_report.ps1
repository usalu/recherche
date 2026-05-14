$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$decisionCsvPath = Join-Path $root "_migration/32_huerde_logistikproblem_edge_review_decisions.csv"
$reportPath = Join-Path $root "_migration/32_Huerde_Logistikproblem_Review_Decision.md"

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$reviewRows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $_.target -eq "huerde/Logistikproblem" })

$decisions = foreach ($row in $reviewRows) {
    $existingHuerden = @($cleanEdges |
        Where-Object { $_.source -eq $row.source -and $_.relation -eq "has_huerde" } |
        Select-Object -ExpandProperty target -Unique |
        Sort-Object)

    $raw = Normalize-Text $row.raw_label
    $decision = "keep_review_logistics_too_broad"
    $suggestedTargets = ""
    $suggestedRelations = ""
    $rationale = "Raw label is too broad or needs source context."

    if ($existingHuerden.Count -gt 0) {
        $decision = "covered_by_existing_concrete_huerden"
        $rationale = "Concrete hurdle edges already exist; do not also import broad Logistikproblem."
    }
    elseif ($raw -match "lager") {
        $decision = "candidate_precise_huerde"
        $suggestedTargets = "huerde/Fehlende_Lagerflaeche"
        $suggestedRelations = "has_huerde"
        $rationale = "Storage/logistics issue can map to missing storage capacity."
    }
    elseif ($raw -match "liefer|lieferkette|supply") {
        $decision = "candidate_precise_huerde"
        $suggestedTargets = "huerde/Verfuegbarkeitsproblem"
        $suggestedRelations = "has_huerde"
        $rationale = "Supply-chain issue is more precise than generic logistics."
    }
    elseif ($raw -match "bruch|risse|beschädigung|beschaedigung") {
        $decision = "candidate_precise_huerde"
        $suggestedTargets = "huerde/Bruch_Beschaedigungsrisiko"
        $suggestedRelations = "has_huerde"
        $rationale = "Transport damage risk is the concrete barrier."
    }
    elseif ($raw -match "gewicht|heavy|transportgewicht|kran|trailer") {
        $decision = "candidate_review_split"
        $suggestedTargets = "huerde/Kompatibilitaetsproblem or huerde/Toleranzen"
        $suggestedRelations = "has_huerde"
        $rationale = "Weight/handling can be compatibility, tolerance, or process issue; verify source."
    }
    elseif ($raw -match "transport|montage|montagefolge|fügung|fuegung|passung") {
        $decision = "candidate_review_split"
        $suggestedTargets = "huerde/Kompatibilitaetsproblem or huerde/Anschlussproblem"
        $suggestedRelations = "has_huerde"
        $rationale = "Transport/mounting can be fit, connection, or sequencing issue; verify source."
    }

    [PSCustomObject]@{
        source = $row.source
        old_relation = $row.relation
        old_target = $row.target
        raw_label = $row.raw_label
        existing_clean_huerde_edges = ($existingHuerden -join "; ")
        logistikproblem_decision = $decision
        suggested_target = $suggestedTargets
        suggested_relation = $suggestedRelations
        database_change = "none"
        rationale = $rationale
        legacy_path = $row.legacy_path
    }
}

$decisions |
    Sort-Object logistikproblem_decision, raw_label, source |
    Export-Csv -LiteralPath $decisionCsvPath -NoTypeInformation -Encoding UTF8

$byDecision = $decisions |
    Group-Object logistikproblem_decision |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$examples = $decisions |
    Sort-Object logistikproblem_decision, raw_label, source |
    Select-Object -First 12 |
    ForEach-Object { "| $($_.raw_label) | $($_.existing_clean_huerde_edges) | $($_.logistikproblem_decision) | $($_.suggested_target) |" }

$report = @()
$report += "# Phase 32 Huerde Logistikproblem Review Decision"
$report += ""
$report += "## Decision"
$report += ""
$report += "Keep huerde/Logistikproblem out of the clean database."
$report += ""
$report += "Reason: Logistikproblem is too broad. The clean graph needs the concrete barrier behind the logistics issue."
$report += ""
$report += "## Database Change"
$report += ""
$report += "No database nodes or clean edges were added. Existing concrete hurdle edges remain the clean representation where already present."
$report += ""
$report += "## Counts"
$report += ""
$report += "- Held huerde/Logistikproblem edges reviewed: $($decisions.Count)"
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
$report += "- _migration/32_huerde_logistikproblem_edge_review_decisions.csv"

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $decisionCsvPath"
Write-Output "Wrote $reportPath"
