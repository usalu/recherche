$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$decisionCsvPath = Join-Path $root "_migration/28_material_metall_edge_review_decisions.csv"
$reportPath = Join-Path $root "_migration/28_Material_Metall_Review_Decision.md"

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$reviewRows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $_.target -eq "material/Metall" })

$decisions = foreach ($row in $reviewRows) {
    $existingMaterials = @($cleanEdges |
        Where-Object { $_.source -eq $row.source -and $_.relation -eq "uses_material" } |
        Select-Object -ExpandProperty target -Unique |
        Sort-Object)

    $raw = Normalize-Text $row.raw_label
    $decision = "keep_review_exact_metal_unknown"
    $rationale = "No exact metal is known from the current clean edge set; do not import broad material/Metall."

    if (($raw -match "stahl" -and $existingMaterials -contains "material/Stahl") -or
        ($raw -match "aluminium" -and $existingMaterials -contains "material/Aluminium")) {
        $decision = "resolved_by_existing_exact_material"
        $rationale = "Exact metal mentioned in raw label is already represented by a clean material edge."
    }
    elseif ($existingMaterials.Count -gt 0 -and $raw -ne "metall") {
        $decision = "partial_exact_materials_already_imported_keep_metal_unknown"
        $rationale = "Other exact material parts are already imported; the metal part remains too broad."
    }

    [PSCustomObject]@{
        source = $row.source
        old_relation = $row.relation
        old_target = $row.target
        raw_label = $row.raw_label
        existing_clean_material_edges = ($existingMaterials -join "; ")
        material_metall_decision = $decision
        database_change = "none"
        rationale = $rationale
        legacy_path = $row.legacy_path
    }
}

$decisions |
    Sort-Object material_metall_decision, raw_label, source |
    Export-Csv -LiteralPath $decisionCsvPath -NoTypeInformation -Encoding UTF8

$byDecision = $decisions |
    Group-Object material_metall_decision |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$examples = $decisions |
    Sort-Object material_metall_decision, raw_label, source |
    Select-Object -First 12 |
    ForEach-Object { "| $($_.raw_label) | $($_.existing_clean_material_edges) | $($_.material_metall_decision) |" }

$report = @()
$report += "# Phase 28 Material Metall Review Decision"
$report += ""
$report += "## Decision"
$report += ""
$report += "Keep material/Metall out of the clean database."
$report += ""
$report += "Reason: Metall is a broad fallback label, not a clean material knot. Use exact material nodes such as material/Stahl, material/Aluminium, material/Glas, material/Holz, material/Keramik, or material/Kunststoff when known."
$report += ""
$report += "## Database Change"
$report += ""
$report += "No database nodes or clean edges were added. The decision is recorded in the manual decision template and in the edge decision CSV."
$report += ""
$report += "## Counts"
$report += ""
$report += "- Held material/Metall edges reviewed: $($decisions.Count)"
$report += ""
$report += "| decision | rows |"
$report += "|---|---:|"
$report += $byDecision
$report += ""
$report += "## Sample Rows"
$report += ""
$report += "| raw label | existing clean material edges | decision |"
$report += "|---|---|---|"
$report += $examples
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/28_material_metall_edge_review_decisions.csv"

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $decisionCsvPath"
Write-Output "Wrote $reportPath"
