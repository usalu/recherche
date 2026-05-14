$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$impactPath = Join-Path $root "_migration/25_manual_review_node_impact.csv"
$decisionPath = Join-Path $root "_migration/25_manual_review_decision_template.csv"
$statusCsvPath = Join-Path $root "_migration/35_manual_review_preparation_status.csv"
$reportPath = Join-Path $root "_migration/35_Manual_Review_Preparation_Status.md"

$firstBatch = @(
    "material/Metall",
    "huerde/Performance_Nachweis",
    "bauteiltyp/Tragstruktur",
    "bauteiltyp/Bauwerksteil",
    "huerde/Logistikproblem"
)

$secondBatch = @(
    "bauteiltyp/Fliese",
    "bauteiltyp/Kueche",
    "bauteiltyp/Landschaftselement",
    "bauteiltyp/Bruestung",
    "bauteiltyp/Kern"
)

$thirdBatch = @(
    "datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger",
    "datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster",
    "material/Guss",
    "material/Erde",
    "bauteiltyp/Auflager_Widerlager",
    "material/Recyclingbeton"
)

$contentBatch = @(
    "bauteiltyp/Holzrahmenelement",
    "bauteiltyp/Treppenwange",
    "datenmodell/Gebaeuderessourcenpass",
    "dokumenttyp/Gebaeuderessourcenpass",
    "fuegung_verbindung/Beton_Fertigteile_Verbindungen",
    "fuegung_verbindung/Composite_Verbindungen",
    "fuegung_verbindung/Holz_Verbindungen",
    "fuegung_verbindung/Stahl_Verbindungen",
    "fuegung_verbindung/Stahlseil",
    "reuse_strategie/Temporaerer_Wiedereinbau",
    "zertifizierung_bewertungssystem/DGNB"
)

function Get-PreparationStatus {
    param([string]$TypedPath, [int]$EdgeCount)

    if ($firstBatch -contains $TypedPath) {
        return "proposal_ready_first_batch"
    }
    if ($secondBatch -contains $TypedPath) {
        return "proposal_ready_second_batch"
    }
    if ($thirdBatch -contains $TypedPath) {
        return "proposal_ready_third_batch"
    }
    if ($contentBatch -contains $TypedPath) {
        return "proposal_ready_content_only"
    }
    if ($EdgeCount -gt 0) {
        return "needs_edge_proposal"
    }
    return "needs_content_only_review"
}

function Get-NextAction {
    param([string]$TypedPath, [int]$EdgeCount, [string]$Status)

    switch ($Status) {
        "proposal_ready_first_batch" { return "Use phase 28-32 proposal files during final decision pass." }
        "proposal_ready_second_batch" { return "Use phase 34 proposal CSV during final decision pass." }
        "proposal_ready_third_batch" { return "Use phase 36 proposal CSV during final decision pass." }
        "proposal_ready_content_only" { return "Use phase 37 content-only proposal CSV during final decision pass." }
        "needs_edge_proposal" { return "Generate edge-level proposal before final decision." }
        "needs_content_only_review" { return "Review node content only; no held edges currently depend on it." }
        default { return "Review manually." }
    }
}

$decisionByPath = @{}
foreach ($row in Import-Csv -LiteralPath $decisionPath) {
    $decisionByPath[$row.typed_path] = $row
}

$rows = foreach ($impact in Import-Csv -LiteralPath $impactPath) {
    $edgeCount = [int]$impact.total_edge_review_count
    $status = Get-PreparationStatus -TypedPath $impact.typed_path -EdgeCount $edgeCount
    $decision = if ($decisionByPath.ContainsKey($impact.typed_path)) { $decisionByPath[$impact.typed_path].decision } else { "" }

    [PSCustomObject]@{
        typed_path = $impact.typed_path
        review_class = $impact.review_class
        held_edge_count = $edgeCount
        preparation_status = $status
        manual_decision_state = $decision
        next_action = Get-NextAction -TypedPath $impact.typed_path -EdgeCount $edgeCount -Status $status
    }
}

$rows |
    Sort-Object @{Expression = "held_edge_count"; Descending = $true}, typed_path |
    Export-Csv -LiteralPath $statusCsvPath -NoTypeInformation -Encoding UTF8

$byStatus = $rows |
    Group-Object preparation_status |
    Sort-Object Name |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$byDecision = $rows |
    Group-Object manual_decision_state |
    Sort-Object Name |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$needsProposal = $rows |
    Where-Object { $_.preparation_status -eq "needs_edge_proposal" } |
    Sort-Object @{Expression = "held_edge_count"; Descending = $true}, typed_path |
    ForEach-Object { "| $($_.typed_path) | $($_.held_edge_count) | $($_.review_class) |" }

$contentOnly = $rows |
    Where-Object { $_.preparation_status -eq "needs_content_only_review" } |
    Sort-Object typed_path |
    ForEach-Object { "| $($_.typed_path) | $($_.review_class) |" }

$report = @()
$report += "# Phase 35 Manual Review Preparation Status"
$report += ""
$report += "## Purpose"
$report += ""
$report += "Track preparation work before final manual decisions. This file does not approve or migrate nodes."
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/35_manual_review_preparation_status.csv"
$report += ""
$report += "## Preparation Status"
$report += ""
$report += "| status | nodes |"
$report += "|---|---:|"
$report += $byStatus
$report += ""
$report += "## Manual Decision State"
$report += ""
$report += "| decision state | nodes |"
$report += "|---|---:|"
$report += $byDecision
$report += ""
$report += "## Remaining Edge-Proposal Work"
$report += ""
$report += "| node | held edges | class |"
$report += "|---|---:|---|"
$report += $needsProposal
$report += ""
$report += "## Content-Only Review Later"
$report += ""
$report += "| node | class |"
$report += "|---|---|"
$report += $contentOnly
$report += ""
$report += "## Final Decision Rule"
$report += ""
$report += "Keep _migration/25_manual_review_decision_template.csv as TODO until every needed proposal package is prepared."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $statusCsvPath"
Write-Output "Wrote $reportPath"
