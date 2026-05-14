$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$proposalCsvPath = Join-Path $root "_migration/36_third_manual_batch_edge_proposals.csv"
$reportPath = Join-Path $root "_migration/36_Third_Manual_Batch_Proposals.md"

$batchNodes = @(
    "datenpunkt/Timber_Square_London__001__Wiederverwendete_Stahltr_ger",
    "datenpunkt/ELYS_Kultur_Gewerbehaus_Basel__003__Fenster",
    "material/Guss",
    "material/Erde",
    "bauteiltyp/Auflager_Widerlager",
    "material/Recyclingbeton"
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
    param([object]$Edge, [array]$ExistingEdges)

    $source = $Edge.source
    $target = $Edge.target
    $raw = Normalize-Text $Edge.raw_label

    if ($source -like "datenpunkt/*") {
        return New-Proposal "keep_review_convert_datapoint" "" "" "REVIEW_REQUIRED" "This source is not a clean datapoint yet. Create a real datenpunkt only if the source provides value, unit, metric, and scope; then reconnect fallstudie/projekt/bauobjekt/kennwertdefinition."
    }

    if ($target -eq "material/Guss") {
        if ($raw -match "gusseisen") {
            return New-Proposal "candidate_new_material" "material/Gusseisen" "uses_material" "REVIEW" "Gusseisen is an exact material candidate, but the clean material knot does not exist yet."
        }
        if ($raw -match "stahl") {
            return New-Proposal "candidate_split" "material/Stahl; material/Gusseisen" "uses_material" "REVIEW" "Stahl is already clean; Guss likely means cast iron/metal and needs exact material decision."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Guss alone is a process/form label, not a clean material without cast iron/cast steel context."
    }

    if ($target -eq "material/Erde") {
        if ($raw -match "stroh") {
            return New-Proposal "candidate_split" "material/Stroh; material/Lehm" "uses_material" "REVIEW" "Stroh is known; Erde may mean Lehm/earth plaster, but source must confirm."
        }
        if ($raw -match "gepresste|btc|ziegel") {
            return New-Proposal "candidate_move" "material/Lehm" "uses_material" "REVIEW" "Compressed earth/block context likely maps to Lehm, but verify source terminology."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Erde may be excavated soil/resource rather than a clean construction material."
    }

    if ($target -eq "bauteiltyp/Auflager_Widerlager") {
        if ($raw -match "plattenauflager") {
            return New-Proposal "candidate_review_component_or_connection" "bauteiltyp/Fundament or fuegung_verbindung/*" "has_bauteiltyp or has_fuegung_verbindung" "REVIEW" "Plate support may be support detail, foundation/support component, or connection context."
        }
        if ($raw -match "widerlager|auflager") {
            return New-Proposal "keep_review_infrastructure_support" "" "" "REVIEW_REQUIRED" "Abutment/support is infrastructure/foundation scale; current clean bauteiltyp may not cover it."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Support/abutment context needs source review."
    }

    if ($target -eq "material/Recyclingbeton") {
        return New-Proposal "candidate_boundary_split" "material/Beton; bewertungslogik_abgrenzung/Recycling_Nicht_Direct_Reuse" "uses_material; has_bewertungslogik_abgrenzung" "REVIEW" "Recyclingbeton is material plus recycling boundary; do not count as direct reuse."
    }

    return New-Proposal "not_in_third_batch" "" "" "REVIEW_REQUIRED" "Row is outside third batch."
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$rows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { ($batchNodes -contains $_.target) -or ($batchNodes -contains $_.source) })

$proposals = foreach ($row in $rows) {
    $existing = @($cleanEdges |
        Where-Object { $_.source -eq $row.source } |
        ForEach-Object { "$($_.relation)->$($_.target)" } |
        Select-Object -Unique |
        Sort-Object)
    $proposal = Suggest-EdgeDecision -Edge $row -ExistingEdges $existing
    [PSCustomObject]@{
        source = $row.source
        relation = $row.relation
        target = $row.target
        raw_label = $row.raw_label
        review_reason = $row.review_reason
        existing_clean_edges = ($existing -join "; ")
        legacy_path = $row.legacy_path
        proposed_action = $proposal.proposed_action
        proposed_target = $proposal.proposed_target
        proposed_relation = $proposal.proposed_relation
        proposal_confidence = $proposal.proposal_confidence
        reviewer_note = $proposal.reviewer_note
    }
}

$proposals |
    Sort-Object target, source, relation |
    Export-Csv -LiteralPath $proposalCsvPath -NoTypeInformation -Encoding UTF8

$summaryByNode = $proposals |
    ForEach-Object {
        $node = if ($batchNodes -contains $_.source) { $_.source } else { $_.target }
        [PSCustomObject]@{ node = $node; action = $_.proposed_action; confidence = $_.proposal_confidence }
    }

$byNode = $summaryByNode |
    Group-Object node |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$byAction = $proposals |
    Group-Object proposed_action |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$report = @()
$report += "# Phase 36 Third Manual Batch Proposals"
$report += ""
$report += "## Scope"
$report += ""
$report += "Proposal-only pass for the remaining six manual-review nodes with held edges. No manual decisions were written."
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/36_third_manual_batch_edge_proposals.csv"
$report += ""
$report += "## Counts"
$report += ""
$report += "- Proposed edge rows: $($proposals.Count)"
$report += ""
$report += "## By Node"
$report += ""
$report += "| node | rows |"
$report += "|---|---:|"
$report += $byNode
$report += ""
$report += "## By Proposed Action"
$report += ""
$report += "| action | rows |"
$report += "|---|---:|"
$report += $byAction
$report += ""
$report += "## Rule"
$report += ""
$report += "Keep manual decisions deferred until the content-only review package is also prepared."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $proposalCsvPath"
Write-Output "Wrote $reportPath"
