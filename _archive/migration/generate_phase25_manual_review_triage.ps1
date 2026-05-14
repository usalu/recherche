$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$manualRoot = Join-Path $root "_manual_review/nodes"
$manualQueuePath = Join-Path $root "_migration/19_manual_review_queue.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"

$impactPath = Join-Path $root "_migration/25_manual_review_node_impact.csv"
$decisionTemplatePath = Join-Path $root "_migration/25_manual_review_decision_template.csv"
$edgeBucketPath = Join-Path $root "_migration/25_manual_review_edge_buckets.csv"
$reportPath = Join-Path $root "_migration/25_Manual_Review_Triage_Report.md"
$playbookPath = Join-Path $root "_manual_review/review_playbook.md"

function Normalize-RepoPath {
    param([string]$Path)
    return ($Path -replace "\\", "/")
}

function Get-TypedPathFromGraphPath {
    param([string]$Path)
    $normalized = Normalize-RepoPath $Path
    if ($normalized -match "^_graph/([^/]+)/(.+)$") {
        return "$($matches[1])/$($matches[2])"
    }
    return ""
}

function Get-ReviewClass {
    param([string]$TypedPath)

    switch -Regex ($TypedPath) {
        "^material/Metall$" { return "broad_material_fallback" }
        "^material/(Erde|Guss|Recyclingbeton)$" { return "ambiguous_material_or_boundary" }
        "^bauteiltyp/(Tragstruktur|Bauwerksteil|Kern)$" { return "wrong_scale_or_structural_system" }
        "^bauteiltyp/(Fliese|Kueche|Bruestung|Treppenwange|Auflager_Widerlager|Holzrahmenelement|Landschaftselement)$" { return "component_scope_unclear" }
        "^huerde/(Logistikproblem|Performance_Nachweis)$" { return "broad_barrier_fallback" }
        "^datenpunkt/" { return "datapoint_conflicts_with_reuse_item" }
        "^fuegung_verbindung/" { return "connection_overview_not_atomic_connection" }
        "^datenmodell/|^dokumenttyp/|^zertifizierung_bewertungssystem/" { return "model_document_system_mixed_content" }
        "^reuse_strategie/Temporaerer_Wiedereinbau$" { return "strategy_status_overlap" }
        default { return "manual_semantic_review" }
    }
}

function Get-RecommendedDecision {
    param([string]$TypedPath)

    switch -Regex ($TypedPath) {
        "^material/Metall$" { return "Do not approve as clean material unless exact metal is unknown and source truly says only Metall. Prefer Stahl, Aluminium, Sekundaerstahl, or keep edge in review." }
        "^material/Recyclingbeton$" { return "Treat as material only with recycling boundary; link to reuse_strategy/Recycling and do not count as Direct Reuse." }
        "^material/Guss$" { return "Resolve to Gusseisen, Stahlguss, or another exact material; otherwise keep in review." }
        "^material/Erde$" { return "Resolve to Lehm when construction-earth context is clear; otherwise keep source label only." }
        "^bauteiltyp/Tragstruktur$" { return "Resolve to specific bauteiltyp, tragwerkstyp, or tragwerksprinzip; avoid generic component import." }
        "^bauteiltyp/Bauwerksteil$" { return "Resolve to bauobjekt, bauobjektrolle, or a precise bauteiltyp depending on source scale." }
        "^bauteiltyp/Kern$" { return "Usually structural core: prefer tragwerkstyp/tragwerksprinzip or precise component if source is concrete." }
        "^bauteiltyp/Kueche$" { return "Usually fit-out: prefer bauteiltyp/Festes_Einbauteil or boundary logic if furniture/non-direct-reuse." }
        "^bauteiltyp/Fliese$" { return "Resolve as bauteiltyp/Boden or bauteiltyp/Wand plus material/Keramik if context is clear." }
        "^bauteiltyp/Bruestung$" { return "Resolve to bauteiltyp/Gelaender, Fassade, or parapet-like component based on case context." }
        "^bauteiltyp/Holzrahmenelement$" { return "Resolve to bausystem/Holzrahmenbau or bauteiltyp/Wand/Platte_Paneel depending on reuse object." }
        "^huerde/Logistikproblem$" { return "Resolve to concrete hurdle such as Terminunsicherheit, Fehlende_Lagerflaeche, Verfuegbarkeitsproblem, or keep review." }
        "^huerde/Performance_Nachweis$" { return "Separate barrier from proof: use huerde/Technische_Freigabe or pruefung_nachweis/leistungsanforderung node." }
        "^datenpunkt/" { return "Do not import as datenpunkt until it is converted to a measured value with unit/scope." }
        "^fuegung_verbindung/" { return "Split into atomic connection types or move overview content into method/source notes." }
        "^datenmodell/Gebaeuderessourcenpass$" { return "Clean content first; separate data model from tool/vendor/project profile." }
        "^dokumenttyp/Gebaeuderessourcenpass$" { return "Clean content first; keep as document type only, not software or certification system." }
        "^zertifizierung_bewertungssystem/DGNB$" { return "Valid system, but strip resource-pass mixed content before import." }
        "^reuse_strategie/Temporaerer_Wiedereinbau$" { return "Decide whether strategy, status, or both; likely pair with reuse_einsatzstatus/Temporaer." }
        default { return "Review source text and map to strongest real-world type before import." }
    }
}

$manualRows = @()
foreach ($row in Import-Csv -LiteralPath $manualQueuePath) {
    $typed = Get-TypedPathFromGraphPath $row.old_path
    if ([string]::IsNullOrWhiteSpace($typed)) {
        continue
    }
    $parts = $typed -split "/", 2
    $manualRows += [PSCustomObject]@{
        typed_path = $typed
        entity = $parts[0]
        id = $parts[1]
        old_path = Normalize-RepoPath $row.old_path
        suggested_target = $row.suggested_target
        reason = $row.reason
        review_class = Get-ReviewClass $typed
        recommended_decision = Get-RecommendedDecision $typed
    }
}

$edgeRows = @(Import-Csv -LiteralPath $edgeReviewPath)

$existingDecisionByPath = @{}
if (Test-Path -LiteralPath $decisionTemplatePath) {
    foreach ($existing in Import-Csv -LiteralPath $decisionTemplatePath) {
        if (-not [string]::IsNullOrWhiteSpace($existing.typed_path) -and -not $existingDecisionByPath.ContainsKey($existing.typed_path)) {
            $existingDecisionByPath[$existing.typed_path] = $existing
        }
    }
}

$impactRows = foreach ($manual in $manualRows) {
    $incoming = @($edgeRows | Where-Object { (Normalize-RepoPath $_.target) -eq $manual.typed_path })
    $outgoing = @($edgeRows | Where-Object { (Normalize-RepoPath $_.source) -eq $manual.typed_path })
    $labels = @($incoming + $outgoing |
        Where-Object { -not [string]::IsNullOrWhiteSpace($_.raw_label) } |
        Select-Object -ExpandProperty raw_label -Unique |
        Select-Object -First 8)

    [PSCustomObject]@{
        typed_path = $manual.typed_path
        entity = $manual.entity
        id = $manual.id
        review_class = $manual.review_class
        incoming_edge_review_count = $incoming.Count
        outgoing_edge_review_count = $outgoing.Count
        total_edge_review_count = $incoming.Count + $outgoing.Count
        top_raw_labels = ($labels -join " | ")
        reason = $manual.reason
        recommended_decision = $manual.recommended_decision
    }
}

$edgeBuckets = $edgeRows |
    Group-Object review_reason, target |
    Sort-Object Count -Descending |
    ForEach-Object {
        $sample = $_.Group | Select-Object -First 1
        [PSCustomObject]@{
            review_reason = $sample.review_reason
            target = $sample.target
            relation = ($_.Group | Select-Object -ExpandProperty relation -Unique) -join "; "
            count = $_.Count
            sample_raw_label = $sample.raw_label
            sample_legacy_path = $sample.legacy_path
        }
    }

$decisionRows = foreach ($manual in $manualRows) {
    $existing = $null
    if ($existingDecisionByPath.ContainsKey($manual.typed_path)) {
        $existing = $existingDecisionByPath[$manual.typed_path]
    }

    [PSCustomObject]@{
        typed_path = $manual.typed_path
        old_path = $manual.old_path
        decision = if ($existing) { $existing.decision } else { "TODO" }
        final_target_path = if ($existing) { $existing.final_target_path } else { "" }
        edge_relation_rule = if ($existing) { $existing.edge_relation_rule } else { "" }
        import_now = if ($existing) { $existing.import_now } else { "no" }
        reviewer_note = if ($existing -and -not [string]::IsNullOrWhiteSpace($existing.reviewer_note)) { $existing.reviewer_note } else { $manual.recommended_decision }
    }
}

$impactRows |
    Sort-Object @{Expression = "total_edge_review_count"; Descending = $true}, typed_path |
    Export-Csv -LiteralPath $impactPath -NoTypeInformation -Encoding UTF8

$edgeBuckets |
    Export-Csv -LiteralPath $edgeBucketPath -NoTypeInformation -Encoding UTF8

$decisionRows |
    Sort-Object typed_path |
    Export-Csv -LiteralPath $decisionTemplatePath -NoTypeInformation -Encoding UTF8

$topImpact = $impactRows |
    Sort-Object @{Expression = "total_edge_review_count"; Descending = $true}, typed_path |
    Select-Object -First 15 |
    ForEach-Object { "| $($_.typed_path) | $($_.total_edge_review_count) | $($_.review_class) | $($_.recommended_decision) |" }

$zeroImpact = @($impactRows | Where-Object { $_.total_edge_review_count -eq 0 }).Count
$totalReviewEdges = $edgeRows.Count
$totalManualNodes = $manualRows.Count

$report = @()
$report += "# Phase 25 Manual Review Triage Report"
$report += ""
$report += "## Purpose"
$report += ""
$report += "This does not migrate any review node. It only sorts the manual work so conflict-prone content stays out of the clean database until approved."
$report += ""
$report += "## Outputs"
$report += ""
$report += "- _migration/25_manual_review_node_impact.csv"
$report += "- _migration/25_manual_review_edge_buckets.csv"
$report += "- _migration/25_manual_review_decision_template.csv"
$report += "- _manual_review/review_playbook.md"
$report += ""
$report += "## Counts"
$report += ""
$report += "- Manual-review nodes: $totalManualNodes"
$report += "- Edge-review rows: $totalReviewEdges"
$report += "- Manual-review nodes with no held edges: $zeroImpact"
$report += ""
$report += "## Highest Impact Review Nodes"
$report += ""
$report += "| node | held edges | class | recommended decision logic |"
$report += "|---|---:|---|---|"
$report += $topImpact
$report += ""
$report += "## Review Method"
$report += ""
$report += "1. Start with the highest held-edge count."
$report += "2. Open the source node in _manual_review/nodes and compare the raw labels in _database/_edges/clean_edge_review_queue.csv."
$report += "3. Decide the strongest real-world type before moving anything."
$report += "4. Approve only exact mappings; keep broad fallback nodes in review."
$report += "5. After each approved node, regenerate clean edges and rebuild SQLite."
$report += ""
$report += "## Hard Rule"
$report += ""
$report += "Do not import broad fallback nodes just to reduce the queue. Cleanliness is more important than edge count."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

$playbook = @()
$playbook += "# Manual Review Playbook"
$playbook += ""
$playbook += "Work one node at a time. Nothing in this folder is imported automatically."
$playbook += ""
$playbook += "## Decision Options"
$playbook += ""
$playbook += "- approve_move: move to one clean typed path."
$playbook += "- approve_split: split into multiple exact typed paths."
$playbook += "- merge_into_existing: merge evidence into an existing clean node."
$playbook += "- keep_review: leave unresolved."
$playbook += "- delete_from_final: do not import as semantic node."
$playbook += ""
$playbook += "## Files"
$playbook += ""
$playbook += "- Node impact: _migration/25_manual_review_node_impact.csv"
$playbook += "- Decision template: _migration/25_manual_review_decision_template.csv"
$playbook += "- Held edges: _database/_edges/clean_edge_review_queue.csv"
$playbook += ""
$playbook += "## First Nodes To Review"
$playbook += ""
$playbook += "| node | held edges | class | recommended decision logic |"
$playbook += "|---|---:|---|---|"
$playbook += $topImpact
$playbook += ""
$playbook += "## Rule"
$playbook += ""
$playbook += "A node may enter _database only when its entity type is unambiguous and the target path follows entity/id."

$playbook | Set-Content -LiteralPath $playbookPath -Encoding UTF8

Write-Output "Wrote $impactPath"
Write-Output "Wrote $edgeBucketPath"
Write-Output "Wrote $decisionTemplatePath"
Write-Output "Wrote $reportPath"
Write-Output "Wrote $playbookPath"
