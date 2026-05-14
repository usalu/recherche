$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$databaseRoot = Join-Path $root "_database"
$decisionPath = Join-Path $root "_migration/25_manual_review_decision_template.csv"
$reportPath = Join-Path $root "_migration/27_Manual_Decision_Validation_Report.md"

function Normalize-RepoPath {
    param([string]$Path)
    return ($Path -replace "\\", "/")
}

function Test-TypedPath {
    param([string]$Path)
    $normalized = Normalize-RepoPath $Path
    return ($normalized -match "^[a-z0-9_]+/[^/]+$")
}

function Test-DatabaseNode {
    param([string]$TypedPath)
    $normalized = Normalize-RepoPath $TypedPath
    if (-not (Test-TypedPath $normalized)) {
        return $false
    }
    $parts = $normalized -split "/", 2
    $index = Join-Path $databaseRoot (Join-Path $parts[0] (Join-Path $parts[1] "index.md"))
    return (Test-Path -LiteralPath $index)
}

$rows = @(Import-Csv -LiteralPath $decisionPath)
$issues = New-Object System.Collections.Generic.List[object]

foreach ($row in $rows) {
    $decision = $row.decision
    $target = Normalize-RepoPath $row.final_target_path

    if ($decision -eq "TODO") {
        continue
    }

    if ($decision -notin @("approve_move", "approve_split", "merge_into_existing", "keep_review", "delete_from_final")) {
        $issues.Add([PSCustomObject]@{
            typed_path = $row.typed_path
            issue = "unknown_decision"
            detail = "Decision must be approve_move, approve_split, merge_into_existing, keep_review, or delete_from_final."
        })
        continue
    }

    if ($decision -in @("keep_review", "delete_from_final")) {
        continue
    }

    if ([string]::IsNullOrWhiteSpace($target)) {
        $issues.Add([PSCustomObject]@{
            typed_path = $row.typed_path
            issue = "missing_target"
            detail = "Approved decisions need final_target_path."
        })
        continue
    }

    foreach ($oneTarget in ($target -split ";\s*")) {
        if ([string]::IsNullOrWhiteSpace($oneTarget)) {
            continue
        }
        if (-not (Test-TypedPath $oneTarget)) {
            $issues.Add([PSCustomObject]@{
                typed_path = $row.typed_path
                issue = "invalid_typed_path"
                detail = "Target is not entity/id: $oneTarget"
            })
            continue
        }
        if ($oneTarget -match "\*|TODO|REVIEW") {
            $issues.Add([PSCustomObject]@{
                typed_path = $row.typed_path
                issue = "placeholder_target"
                detail = "Target contains wildcard or placeholder: $oneTarget"
            })
        }
        if ($decision -eq "merge_into_existing" -and -not (Test-DatabaseNode $oneTarget)) {
            $issues.Add([PSCustomObject]@{
                typed_path = $row.typed_path
                issue = "merge_target_missing"
                detail = "merge_into_existing target does not exist in _database: $oneTarget"
            })
        }
    }
}

$decisionsByState = $rows |
    Group-Object decision |
    Sort-Object Name |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$report = @()
$report += "# Phase 27 Manual Decision Validation Report"
$report += ""
$report += "## Input"
$report += ""
$report += "- _migration/25_manual_review_decision_template.csv"
$report += ""
$report += "## Decision Counts"
$report += ""
$report += "| decision | rows |"
$report += "|---|---:|"
$report += $decisionsByState
$report += ""
$report += "## Issues"
$report += ""
$report += "- Issues found: $($issues.Count)"

if ($issues.Count -gt 0) {
    $report += ""
    $report += "| typed_path | issue | detail |"
    $report += "|---|---|---|"
    foreach ($issue in $issues) {
        $report += "| $($issue.typed_path) | $($issue.issue) | $($issue.detail) |"
    }
}
else {
    $report += ""
    $report += "No blocking issues in non-TODO manual decisions."
}

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $reportPath"
