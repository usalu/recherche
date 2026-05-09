$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$databaseRoot = Join-Path $root "_database"
$manifestPath = Join-Path $root "_migration/19_clean_build_dry_run_manifest.csv"
$edgePath = Join-Path $databaseRoot "_edges/phase6_graph_edges.csv"

$nodeInventoryPath = Join-Path $databaseRoot "_system/node_inventory.csv"
$nodeInventoryMigrationPath = Join-Path $root "_migration/22_database_node_inventory.csv"
$cleanEdgesPath = Join-Path $databaseRoot "_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $databaseRoot "_edges/clean_edge_review_queue.csv"
$edgeReviewMigrationPath = Join-Path $root "_migration/22_clean_edge_review_queue.csv"
$reportPath = Join-Path $root "_migration/22_Clean_Import_Readiness_Report.md"
$sqliteSchemaPath = Join-Path $databaseRoot "_system/sqlite_schema.sql"

function Normalize-RepoPath {
    param([string]$Path)
    return ($Path -replace "\\", "/")
}

function Split-TypedPath {
    param([string]$TypedPath)
    $normalized = Normalize-RepoPath $TypedPath
    $parts = $normalized -split "/", 2
    if ($parts.Length -ne 2) {
        return $null
    }
    return [PSCustomObject]@{
        entity = $parts[0]
        id = $parts[1]
    }
}

function Get-DatabaseTypedPath {
    param([string]$TargetPath)
    $normalized = Normalize-RepoPath $TargetPath
    if ($normalized -notmatch "^_database/([^/]+)/(.+)$") {
        return ""
    }
    $entity = $matches[1]
    $id = $matches[2]
    if ([string]::IsNullOrWhiteSpace($entity) -or [string]::IsNullOrWhiteSpace($id)) {
        return ""
    }
    if ($id.Contains("/")) {
        return ""
    }
    return "$entity/$id"
}

function Read-NodeTitle {
    param([string]$IndexPath, [string]$Fallback)

    if (-not (Test-Path -LiteralPath $IndexPath)) {
        return $Fallback
    }

    $lines = Get-Content -LiteralPath $IndexPath -TotalCount 80
    foreach ($line in $lines) {
        if ($line -match '^title:\s*"?([^"]+)"?\s*$') {
            return $matches[1]
        }
    }
    foreach ($line in $lines) {
        if ($line -match '^#\s+(.+)$') {
            return $matches[1]
        }
    }
    return $Fallback
}

function Get-NodeBuildStatus {
    param([string]$IndexPath)

    if (-not (Test-Path -LiteralPath $IndexPath)) {
        return ""
    }

    foreach ($line in Get-Content -LiteralPath $IndexPath -TotalCount 40) {
        if ($line -match '^build_status:\s*"?([^"]+)"?\s*$') {
            return $matches[1]
        }
    }
    return ""
}

function Rewrite-Relation {
    param(
        [string]$Relation,
        [string]$TargetTypedPath
    )

    $target = Split-TypedPath $TargetTypedPath
    if ($null -eq $target) {
        return $Relation
    }

    if ($Relation -eq "has_bauteiltyp" -and $target.entity -eq "material") {
        return "uses_material"
    }
    if ($Relation -eq "uses_material" -and $target.entity -eq "bauteiltyp") {
        return "has_bauteiltyp"
    }
    if ($Relation -eq "has_bauteiltyp" -and $target.entity -eq "tragwerkstyp") {
        return "has_tragwerkstyp"
    }
    if ($target.entity -eq "bewertungslogik_abgrenzung") {
        return "has_bewertungslogik_abgrenzung"
    }
    if ($Relation -eq "references_norm" -and $target.entity -eq "leistungsanforderung") {
        return "has_leistungsanforderung"
    }
    return $Relation
}

if (-not (Test-Path -LiteralPath $databaseRoot)) {
    throw "_database does not exist. Run phase 20 first."
}

$nodeRows = New-Object System.Collections.Generic.List[object]
foreach ($entityDir in Get-ChildItem -LiteralPath $databaseRoot -Directory | Where-Object { $_.Name -notlike "_*" }) {
    foreach ($nodeDir in Get-ChildItem -LiteralPath $entityDir.FullName -Directory -ErrorAction SilentlyContinue) {
        $indexPath = Join-Path $nodeDir.FullName "index.md"
        if (-not (Test-Path -LiteralPath $indexPath)) {
            continue
        }
        $dateienDir = Join-Path $nodeDir.FullName "DATEIEN"
        $dateienCount = if (Test-Path -LiteralPath $dateienDir) {
            @(Get-ChildItem -LiteralPath $dateienDir -File -Recurse -ErrorAction SilentlyContinue).Count
        } else { 0 }
        $sourceCount = @(Select-String -LiteralPath $indexPath -Pattern "^- Source:" -ErrorAction SilentlyContinue).Count
        $entity = $entityDir.Name
        $id = $nodeDir.Name
        $nodeRows.Add([PSCustomObject]@{
            entity = $entity
            id = $id
            typed_path = "$entity/$id"
            title = Read-NodeTitle -IndexPath $indexPath -Fallback $id
            build_status = Get-NodeBuildStatus -IndexPath $indexPath
            markdown_path = Normalize-RepoPath ($indexPath.Substring($root.Length + 1))
            dateien_file_count = $dateienCount
            imported_source_count = $sourceCount
        })
    }
}

$nodeRows |
    Sort-Object entity, id |
    Export-Csv -LiteralPath $nodeInventoryPath -NoTypeInformation -Encoding UTF8

Copy-Item -LiteralPath $nodeInventoryPath -Destination $nodeInventoryMigrationPath -Force

$nodeSet = New-Object 'System.Collections.Generic.HashSet[string]'
foreach ($node in $nodeRows) {
    [void]$nodeSet.Add($node.typed_path)
}

$redirects = @{}
$manualReview = @{}
$ambiguousRedirects = @{}
$notImported = @{}

foreach ($row in Import-Csv -LiteralPath $manifestPath) {
    $oldPath = Normalize-RepoPath $row.old_path
    if ($oldPath -notmatch "^_graph/([^/]+)/(.+)$") {
        continue
    }
    $oldTyped = "$($matches[1])/$($matches[2])"

    if ($row.status -eq "REVIEW_REQUIRED") {
        $manualReview[$oldTyped] = $row.reason
        continue
    }

    if ($row.action -eq "delete_from_final" -or $row.action -eq "hold_out_of_final") {
        $notImported[$oldTyped] = $row.reason
        continue
    }

    if ($row.status -ne "CONFIDENT") {
        continue
    }

    $targets = @($row.target_path -split ";\s*" | ForEach-Object { Get-DatabaseTypedPath $_ } | Where-Object { -not [string]::IsNullOrWhiteSpace($_) })
    if ($targets.Count -eq 1 -and $nodeSet.Contains($targets[0])) {
        $redirects[$oldTyped] = $targets[0]
    }
    elseif ($targets.Count -gt 1) {
        $ambiguousRedirects[$oldTyped] = ($targets -join "; ")
    }
}

function Resolve-CleanTypedPath {
    param([string]$TypedPath)
    $normalized = Normalize-RepoPath $TypedPath
    if ($redirects.ContainsKey($normalized)) {
        return $redirects[$normalized]
    }
    if ($nodeSet.Contains($normalized)) {
        return $normalized
    }
    return ""
}

$cleanEdges = New-Object System.Collections.Generic.List[object]
$edgeReview = New-Object System.Collections.Generic.List[object]

foreach ($edge in Import-Csv -LiteralPath $edgePath) {
    $sourceOld = Normalize-RepoPath $edge.source
    $targetOld = Normalize-RepoPath $edge.target
    $sourceNew = Resolve-CleanTypedPath $sourceOld
    $targetNew = Resolve-CleanTypedPath $targetOld
    $relationNew = if ($targetNew) { Rewrite-Relation -Relation $edge.relation -TargetTypedPath $targetNew } else { $edge.relation }

    if ($sourceNew -and $targetNew -and $nodeSet.Contains($sourceNew) -and $nodeSet.Contains($targetNew)) {
        $sourceParts = Split-TypedPath $sourceNew
        $targetParts = Split-TypedPath $targetNew
        $edgeCleaning = if ($sourceOld -eq $sourceNew -and $targetOld -eq $targetNew -and $edge.relation -eq $relationNew) {
            "unchanged"
        } else {
            "normalized"
        }
        $cleanEdges.Add([PSCustomObject]@{
            source = $sourceNew
            source_entity = $sourceParts.entity
            source_id = $sourceParts.id
            relation = $relationNew
            target = $targetNew
            target_entity = $targetParts.entity
            target_id = $targetParts.id
            field = $edge.field
            raw_label = $edge.raw_label
            confidence = $edge.confidence
            resolution_rule = $edge.resolution_rule
            legacy_path = $edge.legacy_path
            original_source = $sourceOld
            original_relation = $edge.relation
            original_target = $targetOld
            edge_cleaning = $edgeCleaning
        })
        continue
    }

    $reasons = New-Object System.Collections.Generic.List[string]
    if (-not $sourceNew) {
        if ($manualReview.ContainsKey($sourceOld)) {
            $reasons.Add("source_manual_review")
        }
        elseif ($ambiguousRedirects.ContainsKey($sourceOld)) {
            $reasons.Add("source_ambiguous_split")
        }
        elseif ($notImported.ContainsKey($sourceOld)) {
            $reasons.Add("source_not_imported")
        }
        else {
            $reasons.Add("source_missing_in_database")
        }
    }
    if (-not $targetNew) {
        if ($manualReview.ContainsKey($targetOld)) {
            $reasons.Add("target_manual_review")
        }
        elseif ($ambiguousRedirects.ContainsKey($targetOld)) {
            $reasons.Add("target_ambiguous_split")
        }
        elseif ($notImported.ContainsKey($targetOld)) {
            $reasons.Add("target_not_imported")
        }
        else {
            $reasons.Add("target_missing_in_database")
        }
    }

    $edgeReview.Add([PSCustomObject]@{
        source = $sourceOld
        relation = $edge.relation
        target = $targetOld
        review_reason = ($reasons -join "; ")
        suggested_source = $sourceNew
        suggested_relation = $relationNew
        suggested_target = $targetNew
        field = $edge.field
        raw_label = $edge.raw_label
        confidence = $edge.confidence
        resolution_rule = $edge.resolution_rule
        legacy_path = $edge.legacy_path
    })
}

$cleanEdges |
    Sort-Object source, relation, target, field, raw_label |
    Export-Csv -LiteralPath $cleanEdgesPath -NoTypeInformation -Encoding UTF8

$edgeReview |
    Sort-Object review_reason, target, source |
    Export-Csv -LiteralPath $edgeReviewPath -NoTypeInformation -Encoding UTF8

Copy-Item -LiteralPath $edgeReviewPath -Destination $edgeReviewMigrationPath -Force

$schema = @'
CREATE TABLE nodes (
  entity TEXT NOT NULL,
  id TEXT NOT NULL,
  typed_path TEXT NOT NULL UNIQUE,
  title TEXT,
  build_status TEXT,
  markdown_path TEXT NOT NULL,
  dateien_file_count INTEGER DEFAULT 0,
  imported_source_count INTEGER DEFAULT 0,
  PRIMARY KEY (entity, id)
);

CREATE TABLE edges (
  source_entity TEXT NOT NULL,
  source_id TEXT NOT NULL,
  relation TEXT NOT NULL,
  target_entity TEXT NOT NULL,
  target_id TEXT NOT NULL,
  field TEXT,
  raw_label TEXT,
  confidence TEXT,
  resolution_rule TEXT,
  legacy_path TEXT,
  original_source TEXT,
  original_relation TEXT,
  original_target TEXT,
  edge_cleaning TEXT,
  FOREIGN KEY (source_entity, source_id) REFERENCES nodes(entity, id),
  FOREIGN KEY (target_entity, target_id) REFERENCES nodes(entity, id)
);

CREATE TABLE edge_review (
  source TEXT,
  relation TEXT,
  target TEXT,
  review_reason TEXT,
  suggested_source TEXT,
  suggested_relation TEXT,
  suggested_target TEXT,
  field TEXT,
  raw_label TEXT,
  confidence TEXT,
  resolution_rule TEXT,
  legacy_path TEXT
);
'@
$schema | Set-Content -LiteralPath $sqliteSchemaPath -Encoding UTF8

$nodeCount = $nodeRows.Count
$edgeCount = @(Import-Csv -LiteralPath $edgePath).Count
$cleanEdgeCount = $cleanEdges.Count
$edgeReviewCount = $edgeReview.Count
$normalizedEdges = @($cleanEdges | Where-Object { $_.edge_cleaning -eq "normalized" }).Count
$reviewByReason = $edgeReview |
    Group-Object review_reason |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }
$cleanByRelation = $cleanEdges |
    Group-Object relation |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$expectedTargetEntity = @{
    has_bauteiltyp = "bauteiltyp"
    uses_material = "material"
    has_huerde = "huerde"
    has_bewertungslogik_abgrenzung = "bewertungslogik_abgrenzung"
    has_pruefung_nachweis = "pruefung_nachweis"
    references_norm = "norm"
    has_leistungsanforderung = "leistungsanforderung"
    measures_kennwertdefinition = "kennwertdefinition"
    involves_akteur = "akteur"
    has_akteurrolle = "akteurrolle"
    has_tragwerkstyp = "tragwerkstyp"
}
$relationTargetMismatches = @($cleanEdges | Where-Object {
    $expectedTargetEntity.ContainsKey($_.relation) -and $_.target_entity -ne $expectedTargetEntity[$_.relation]
})

$report = @()
$report += "# Phase 22 Clean Import Readiness Report"
$report += ""
$report += "## Outputs"
$report += ""
$report += "- _database/_system/node_inventory.csv"
$report += "- _database/_edges/clean_confirmed_edges.csv"
$report += "- _database/_edges/clean_edge_review_queue.csv"
$report += "- _database/_system/sqlite_schema.sql"
$report += ""
$report += "## Counts"
$report += ""
$report += "- Clean database nodes: $nodeCount"
$report += "- Original phase-6 confirmed edges: $edgeCount"
$report += "- Clean importable edges: $cleanEdgeCount"
$report += "- Clean edges with normalized endpoint/relation: $normalizedEdges"
$report += "- Edges held for review: $edgeReviewCount"
$report += "- Relation-target mismatches: $($relationTargetMismatches.Count)"
$report += ""
$report += "## Clean Edges By Relation"
$report += ""
$report += "| relation | rows |"
$report += "|---|---:|"
$report += $cleanByRelation
$report += ""
$report += "## Edge Review Reasons"
$report += ""
$report += "| reason | rows |"
$report += "|---|---:|"
$report += $reviewByReason
$report += ""
$report += "## Import Rule"
$report += ""
$report += "Import only clean_confirmed_edges.csv automatically. Keep clean_edge_review_queue.csv out of the graph until each row is manually approved."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8
Copy-Item -LiteralPath $reportPath -Destination (Join-Path $databaseRoot "_system/clean_import_readiness_report.md") -Force

Write-Output "Wrote $nodeInventoryPath"
Write-Output "Wrote $cleanEdgesPath"
Write-Output "Wrote $edgeReviewPath"
Write-Output "Wrote $reportPath"
