$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$graphRoot = Join-Path $root "_graph"
$databaseRoot = Join-Path $root "_database"
$manualRoot = Join-Path $root "_manual_review"
$manifestPath = Join-Path $root "_migration/19_clean_build_dry_run_manifest.csv"
$buildManifestPath = Join-Path $root "_migration/20_clean_database_build_manifest.csv"
$validationPath = Join-Path $root "_migration/20_clean_database_validation.md"

if (Test-Path -LiteralPath $databaseRoot) {
    throw "_database already exists. Stop to avoid mixing build runs."
}

if (Test-Path -LiteralPath $manualRoot) {
    throw "_manual_review already exists. Stop to avoid mixing build runs."
}

function Ensure-Dir {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
    }
}

function Normalize-RepoPath {
    param([string]$Path)
    return ($Path -replace "\\", "/")
}

function Resolve-RepoPath {
    param([string]$RepoPath)
    $normalized = Normalize-RepoPath $RepoPath
    return Join-Path $root ($normalized -replace "/", [IO.Path]::DirectorySeparatorChar)
}

function Convert-TargetToLocalPath {
    param([string]$TargetPath)
    $normalized = Normalize-RepoPath $TargetPath
    if ($normalized.StartsWith("_database/")) {
        return Join-Path $root ($normalized -replace "/", [IO.Path]::DirectorySeparatorChar)
    }
    if ($normalized.StartsWith("_manual_review/")) {
        return Join-Path $root ($normalized -replace "/", [IO.Path]::DirectorySeparatorChar)
    }
    return Join-Path $root ($normalized -replace "/", [IO.Path]::DirectorySeparatorChar)
}

function Safe-FileName {
    param([string]$Value)
    $safe = Normalize-RepoPath $Value
    $safe = $safe -replace "^_graph/", ""
    $safe = $safe -replace "/", "__"
    $safe = $safe -replace "[^A-Za-z0-9_.-]+", "_"
    $safe = $safe -replace "_+", "_"
    $safe = $safe.Trim("_")
    if ([string]::IsNullOrWhiteSpace($safe)) {
        return "source"
    }
    return $safe
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

function Write-CleanIndex {
    param(
        [string]$TargetDir,
        [string]$TargetPath,
        [string]$OldPath,
        [string]$Action,
        [string]$Status,
        [string]$Reason,
        [string]$Title,
        [string]$SourceIndexPath
    )

    Ensure-Dir $TargetDir
    $indexPath = Join-Path $TargetDir "index.md"
    $targetNormalized = Normalize-RepoPath $TargetPath
    $parts = $targetNormalized -split "/"
    $entity = if ($parts.Length -ge 2) { $parts[-2] } else { "" }
    $id = if ($parts.Length -ge 1) { $parts[-1] } else { "" }

    if (-not (Test-Path -LiteralPath $indexPath)) {
        $content = @(
            "---",
            "id: ""$id""",
            "entity: ""$entity""",
            "build_status: ""clean_phase20""",
            "title: ""$Title""",
            "---",
            "# $Title",
            "",
            "## Clean Node",
            "",
            "- Final path: $targetNormalized",
            "- Build rule: typed path IDs only.",
            "",
            "## Imported Staging Nodes",
            ""
        )
        $content | Set-Content -LiteralPath $indexPath -Encoding UTF8
    }

    $safe = Safe-FileName $OldPath
    $dateien = Join-Path $TargetDir "DATEIEN"
    Ensure-Dir $dateien

    if ($SourceIndexPath -and (Test-Path -LiteralPath $SourceIndexPath)) {
        $copyTarget = Join-Path $dateien "$safe.staging_index.md"
        if (-not (Test-Path -LiteralPath $copyTarget)) {
            Copy-Item -LiteralPath $SourceIndexPath -Destination $copyTarget
        }
    }

    $entry = @(
        "- Source: $OldPath",
        "  - Action: $Action",
        "  - Status: $Status",
        "  - Reason: $Reason",
        ""
    )
    Add-Content -LiteralPath $indexPath -Value $entry -Encoding UTF8
}

function Write-SourceArchive {
    param(
        [string]$OldPath,
        [string]$TargetPath,
        [string]$Reason
    )

    $targetDir = Convert-TargetToLocalPath $TargetPath
    Ensure-Dir $targetDir
    $dateien = Join-Path $targetDir "DATEIEN"
    Ensure-Dir $dateien

    $sourcePath = Resolve-RepoPath $OldPath
    $exists = Test-Path -LiteralPath $sourcePath
    $leaf = Split-Path -Leaf $sourcePath
    if ([string]::IsNullOrWhiteSpace($leaf)) {
        $leaf = "source.md"
    }

    if ($exists) {
        Copy-Item -LiteralPath $sourcePath -Destination (Join-Path $dateien $leaf) -Force
    }

    $id = Split-Path -Leaf $targetDir
    $content = @(
        "---",
        "id: ""$id""",
        "entity: ""quelle""",
        "build_status: ""clean_phase20_source_archive""",
        "source_path: ""$(Normalize-RepoPath $OldPath)""",
        "source_exists: ""$exists""",
        "---",
        "# $id",
        "",
        "## Source Archive",
        "",
        "- Original path: $(Normalize-RepoPath $OldPath)",
        "- Archive action: archive_source_once",
        "- Source copied: $exists",
        "- Reason: $Reason"
    )
    $content | Set-Content -LiteralPath (Join-Path $targetDir "index.md") -Encoding UTF8
}

function Copy-NodeToTarget {
    param(
        [string]$OldPath,
        [string]$TargetPath,
        [string]$Action,
        [string]$Status,
        [string]$Reason
    )

    $sourceDir = Resolve-RepoPath $OldPath
    $sourceIndex = Join-Path $sourceDir "index.md"
    $targetDir = Convert-TargetToLocalPath $TargetPath
    $targetLeaf = Split-Path -Leaf $targetDir
    $title = Read-NodeTitle -IndexPath $sourceIndex -Fallback $targetLeaf

    Write-CleanIndex -TargetDir $targetDir -TargetPath $TargetPath -OldPath $OldPath -Action $Action -Status $Status -Reason $Reason -Title $title -SourceIndexPath $sourceIndex
}

function Copy-ManualNode {
    param(
        [string]$OldPath,
        [string]$TargetPath,
        [string]$Action,
        [string]$Status,
        [string]$Reason
    )

    $sourceDir = Resolve-RepoPath $OldPath
    $sourceIndex = Join-Path $sourceDir "index.md"
    $targetDir = Convert-TargetToLocalPath $TargetPath
    $targetLeaf = Split-Path -Leaf $targetDir
    $title = Read-NodeTitle -IndexPath $sourceIndex -Fallback $targetLeaf

    Write-CleanIndex -TargetDir $targetDir -TargetPath $TargetPath -OldPath $OldPath -Action $Action -Status $Status -Reason $Reason -Title $title -SourceIndexPath $sourceIndex
}

function Write-ManualSchemaNote {
    param([string]$TargetPath, [string]$Action, [string]$Status, [string]$Reason)
    $targetDir = Convert-TargetToLocalPath $TargetPath
    Ensure-Dir $targetDir
    $id = Split-Path -Leaf $targetDir
    @(
        "---",
        "id: ""$id""",
        "build_status: ""manual_review_schema_hold""",
        "---",
        "# $id",
        "",
        "- Action: $Action",
        "- Status: $Status",
        "- Reason: $Reason"
    ) | Set-Content -LiteralPath (Join-Path $targetDir "index.md") -Encoding UTF8
}

function Copy-Edges {
    $edgesDir = Join-Path $databaseRoot "_edges"
    Ensure-Dir $edgesDir
    $edgeSources = @(
        "_migration/phase6_graph_edges.csv",
        "_migration/phase6_label_resolution_review.csv",
        "_migration/phase6_edge_summary.csv",
        "_migration/phase6_review_summary.csv"
    )
    foreach ($rel in $edgeSources) {
        $src = Resolve-RepoPath $rel
        if (Test-Path -LiteralPath $src) {
            Copy-Item -LiteralPath $src -Destination (Join-Path $edgesDir (Split-Path -Leaf $src)) -Force
        }
    }
    @(
        "# Edges",
        "",
        "Copied from phase-6 migration outputs.",
        "",
        "- These are support files for graph import.",
        "- Final relation import should use typed path IDs: entity/id."
    ) | Set-Content -LiteralPath (Join-Path $edgesDir "index.md") -Encoding UTF8
}

Ensure-Dir $databaseRoot
Ensure-Dir $manualRoot
Ensure-Dir (Join-Path $databaseRoot "_system")
Ensure-Dir (Join-Path $databaseRoot "_edges")

$results = New-Object System.Collections.Generic.List[object]
$manifestRows = Import-Csv -LiteralPath $manifestPath

foreach ($row in $manifestRows) {
    $oldPath = Normalize-RepoPath $row.old_path
    $targetPath = Normalize-RepoPath $row.target_path
    $action = $row.action
    $status = $row.status
    $reason = $row.reason

    $result = "done"
    $note = ""

    try {
        switch ($action) {
            "create_schema_folder" {
                Ensure-Dir (Convert-TargetToLocalPath $targetPath)
            }
            "exclude_schema_folder" {
                Write-ManualSchemaNote -TargetPath $targetPath -Action $action -Status $status -Reason $reason
            }
            "hold_out_of_final" {
                Copy-ManualNode -OldPath $oldPath -TargetPath $targetPath -Action $action -Status $status -Reason $reason
            }
            "manual_review" {
                Copy-ManualNode -OldPath $oldPath -TargetPath $targetPath -Action $action -Status $status -Reason $reason
            }
            "archive_source_once" {
                Write-SourceArchive -OldPath $oldPath -TargetPath $targetPath -Reason $reason
            }
            "delete_from_final" {
                $result = "not_imported"
                $note = "Approved non-import/delete-from-final row."
            }
            "create_node" {
                foreach ($target in ($targetPath -split ";\s*")) {
                    if ([string]::IsNullOrWhiteSpace($target)) { continue }
                    Write-CleanIndex -TargetDir (Convert-TargetToLocalPath $target) -TargetPath $target -OldPath $oldPath -Action $action -Status $status -Reason $reason -Title (Split-Path -Leaf $target) -SourceIndexPath ""
                }
            }
            "keep_default" {
                Copy-NodeToTarget -OldPath $oldPath -TargetPath $targetPath -Action $action -Status $status -Reason $reason
            }
            "keep_or_merge" {
                if ($oldPath -eq "_graph/_edges/*") {
                    Copy-Edges
                }
                elseif ($oldPath.Contains("*") -or $targetPath.Contains("*")) {
                    $result = "validation_rule_only"
                    $note = "Wildcard rule; no concrete node to copy."
                }
                elseif ($oldPath -like "* same slug *") {
                    $result = "validation_rule_only"
                    $note = "Pseudo rule; no concrete node to copy."
                }
                else {
                    Copy-NodeToTarget -OldPath $oldPath -TargetPath $targetPath -Action $action -Status $status -Reason $reason
                }
            }
            "move_to_clean_target" {
                Copy-NodeToTarget -OldPath $oldPath -TargetPath $targetPath -Action $action -Status $status -Reason $reason
            }
            "merge_to_clean_target" {
                Copy-NodeToTarget -OldPath $oldPath -TargetPath $targetPath -Action $action -Status $status -Reason $reason
            }
            "split_to_clean_targets" {
                foreach ($target in ($targetPath -split ";\s*")) {
                    if ([string]::IsNullOrWhiteSpace($target)) { continue }
                    Copy-NodeToTarget -OldPath $oldPath -TargetPath $target -Action $action -Status $status -Reason $reason
                }
            }
            default {
                $result = "skipped_unknown_action"
                $note = "Unknown action: $action"
            }
        }
    }
    catch {
        $result = "error"
        $note = $_.Exception.Message
    }

    $results.Add([PSCustomObject]@{
        old_path = $oldPath
        target_path = $targetPath
        action = $action
        status = $status
        result = $result
        note = $note
    })
}

$results | Export-Csv -LiteralPath $buildManifestPath -NoTypeInformation -Encoding UTF8

Copy-Item -LiteralPath $manifestPath -Destination (Join-Path $databaseRoot "_system/import_manifest_phase19.csv") -Force
Copy-Item -LiteralPath $buildManifestPath -Destination (Join-Path $databaseRoot "_system/build_manifest_phase20.csv") -Force
Copy-Item -LiteralPath (Join-Path $root "_migration/18_Clean_Ontology_Database_Build_Plan.md") -Destination (Join-Path $databaseRoot "_system/migration_notes.md") -Force

$dbEntities = Get-ChildItem -LiteralPath $databaseRoot -Directory | Select-Object -ExpandProperty Name | Sort-Object
$manualNodes = if (Test-Path -LiteralPath (Join-Path $manualRoot "nodes")) {
    Get-ChildItem -LiteralPath (Join-Path $manualRoot "nodes") -Recurse -Filter "index.md" | Measure-Object | Select-Object -ExpandProperty Count
} else { 0 }
$sourceArchives = if (Test-Path -LiteralPath (Join-Path $databaseRoot "quelle")) {
    Get-ChildItem -LiteralPath (Join-Path $databaseRoot "quelle") -Directory | Where-Object { Test-Path (Join-Path $_.FullName "index.md") } | Measure-Object | Select-Object -ExpandProperty Count
} else { 0 }
$dbNodeIndexes = Get-ChildItem -LiteralPath $databaseRoot -Recurse -Filter "index.md" | Measure-Object | Select-Object -ExpandProperty Count
$manualIndexes = Get-ChildItem -LiteralPath $manualRoot -Recurse -Filter "index.md" | Measure-Object | Select-Object -ExpandProperty Count
$errors = @($results | Where-Object { $_.result -eq "error" })
$reviewInDb = @(Get-ChildItem -LiteralPath $databaseRoot -Recurse -Filter "index.md" | Select-String -Pattern "REVIEW_REQUIRED" -List -ErrorAction SilentlyContinue)

$validation = @()
$validation += "# Phase 20 Clean Database Validation"
$validation += ""
$validation += "## Build Result"
$validation += ""
$validation += "- _database created: $(Test-Path -LiteralPath $databaseRoot)"
$validation += "- _manual_review created: $(Test-Path -LiteralPath $manualRoot)"
$validation += "- Database index files: $dbNodeIndexes"
$validation += "- Manual-review index files: $manualIndexes"
$validation += "- Source archive nodes in _database/quelle: $sourceArchives"
$validation += "- Manual review node index files: $manualNodes"
$validation += "- Build errors: $($errors.Count)"
$validation += "- REVIEW_REQUIRED markers inside _database: $($reviewInDb.Count)"
$validation += ""
$validation += "## Database Top-Level Folders"
$validation += ""
$validation += '```text'
$validation += $dbEntities
$validation += '```'
$validation += ""
$validation += "## Notes"
$validation += ""
$validation += "- _graph was not modified."
$validation += "- Original staging node indexes were copied into node DATEIEN/*.staging_index.md for provenance."
$validation += "- Clean node index.md files contain typed path identity and import provenance."
$validation += "- REVIEW_REQUIRED nodes were routed to _manual_review."

if ($errors.Count -gt 0) {
    $validation += ""
    $validation += "## Errors"
    $validation += ""
    foreach ($err in $errors | Select-Object -First 20) {
        $validation += "- $($err.old_path) -> $($err.target_path): $($err.note)"
    }
}

$validation | Set-Content -LiteralPath $validationPath -Encoding UTF8
Copy-Item -LiteralPath $validationPath -Destination (Join-Path $databaseRoot "_system/validation_report.md") -Force

Write-Output "Created _database"
Write-Output "Created _manual_review"
Write-Output "Wrote $buildManifestPath"
Write-Output "Wrote $validationPath"
