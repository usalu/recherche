$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$graphRoot = Join-Path $root "_graph"
$decisionsPath = Join-Path $root "_migration/17_Semantic_Normalization_Decisions.md"
$schemaPath = Join-Path $root "_migration/final_schema_folder_decisions.csv"
$legacyMapPath = Join-Path $root "_migration/legacy_to_new_map.csv"

$manifestPath = Join-Path $root "_migration/19_clean_build_dry_run_manifest.csv"
$manualQueuePath = Join-Path $root "_migration/19_manual_review_queue.csv"
$summaryPath = Join-Path $root "_migration/19_clean_build_dry_run_summary.md"

function Normalize-RepoPath {
    param([string]$Path)
    return ($Path -replace "\\", "/")
}

function Get-TargetFromDecision {
    param([string]$Decision)

    if ($Decision -notmatch "->") {
        return ""
    }

    $rhs = ($Decision -split "->", 2)[1].Trim()
    $rhs = $rhs -replace "\s+\+\s+", "; "
    return $rhs
}

function Get-ActionFromDecision {
    param([string]$Decision)

    $prefix = $Decision
    if ($Decision -match "->") {
        $prefix = ($Decision -split "->", 2)[0].Trim()
    }

    switch -Regex ($prefix) {
        "^delete" { return "delete_from_final" }
        "^create" { return "create_node" }
        "^keep" { return "keep_or_merge" }
        "^move/split" { return "split_to_clean_targets" }
        "^move/merge" { return "merge_to_clean_target" }
        "^move" { return "move_to_clean_target" }
        "^split" { return "split_to_clean_targets" }
        "^review" { return "manual_review" }
        default { return $prefix }
    }
}

function New-SourceId {
    param(
        [string]$LegacyPath,
        [hashtable]$Seen
    )

    $id = Normalize-RepoPath $LegacyPath
    $id = $id -replace "^_+", ""
    $id = $id -replace "[/\\\.]", "_"
    $id = $id -replace "[^A-Za-z0-9_]+", "_"
    $id = $id -replace "_+", "_"
    $id = $id.Trim("_")

    if ([string]::IsNullOrWhiteSpace($id)) {
        $id = "source"
    }

    $base = $id
    $i = 2
    while ($Seen.ContainsKey($id)) {
        $id = "${base}_${i}"
        $i++
    }
    $Seen[$id] = $true
    return $id
}

$decisionRows = foreach ($line in Get-Content -Path $decisionsPath) {
    if ($line -match '^\| `([^`]+)` \| `([^`]+)` \| (.*?) \| (CONFIDENT|REVIEW_REQUIRED) \|$') {
        [PSCustomObject]@{
            old_path = Normalize-RepoPath $matches[1]
            decision = $matches[2]
            reason = $matches[3]
            status = $matches[4]
        }
    }
}

$decisionByPath = @{}
foreach ($row in $decisionRows) {
    if (-not $decisionByPath.ContainsKey($row.old_path)) {
        $decisionByPath[$row.old_path] = $row
    }
}

$schemaRows = Import-Csv -Path $schemaPath
$schemaByFolder = @{}
foreach ($row in $schemaRows) {
    $schemaByFolder[$row.folder] = $row
}

$manifest = New-Object System.Collections.Generic.List[object]

foreach ($schema in $schemaRows) {
    $action = if ($schema.decision -eq "include") { "create_schema_folder" } else { "exclude_schema_folder" }
    $target = if ($schema.decision -eq "include") { "_database/$($schema.folder)" } else { "_manual_review/excluded_schema/$($schema.folder)" }
    $status = if ($schema.decision -eq "include") { "CONFIDENT" } else { "EXCLUDED" }

    $manifest.Add([PSCustomObject]@{
        old_path = "schema:$($schema.folder)"
        target_path = $target
        action = $action
        status = $status
        reason = $schema.note
    })
}

$nodeDirs = Get-ChildItem -Path $graphRoot -Directory |
    Where-Object { $_.Name -notlike "_*" } |
    ForEach-Object {
        $entity = $_.Name
        Get-ChildItem -Path $_.FullName -Directory -ErrorAction SilentlyContinue |
            Where-Object { Test-Path (Join-Path $_.FullName "index.md") } |
            ForEach-Object {
                [PSCustomObject]@{
                    entity = $entity
                    id = $_.Name
                    old_path = "_graph/$entity/$($_.Name)"
                }
            }
    }

foreach ($node in $nodeDirs) {
    $oldPath = Normalize-RepoPath $node.old_path

    if ($decisionByPath.ContainsKey($oldPath)) {
        $decision = $decisionByPath[$oldPath]

        if ($decision.status -eq "REVIEW_REQUIRED") {
            $manifest.Add([PSCustomObject]@{
                old_path = $oldPath
                target_path = "_manual_review/nodes/$($node.entity)/$($node.id)"
                action = "manual_review"
                status = "REVIEW_REQUIRED"
                reason = $decision.reason
            })
            continue
        }

        $target = Get-TargetFromDecision $decision.decision
        $action = Get-ActionFromDecision $decision.decision
        if ([string]::IsNullOrWhiteSpace($target) -and $action -ne "delete_from_final") {
            $target = "_database/$($node.entity)/$($node.id)"
        }

        $manifest.Add([PSCustomObject]@{
            old_path = $oldPath
            target_path = $target
            action = $action
            status = $decision.status
            reason = $decision.reason
        })
        continue
    }

    if ($schemaByFolder.ContainsKey($node.entity)) {
        $schema = $schemaByFolder[$node.entity]
        if ($schema.decision -eq "include") {
            $manifest.Add([PSCustomObject]@{
                old_path = $oldPath
                target_path = "_database/$($node.entity)/$($node.id)"
                action = "keep_default"
                status = "CONFIDENT"
                reason = "Folder is included in clean ontology and node has no conflict-specific normalization rule."
            })
        }
        else {
            $manifest.Add([PSCustomObject]@{
                old_path = $oldPath
                target_path = "_manual_review/excluded/$($node.entity)/$($node.id)"
                action = "hold_out_of_final"
                status = "EXCLUDED"
                reason = $schema.note
            })
        }
    }
    else {
        $manifest.Add([PSCustomObject]@{
            old_path = $oldPath
            target_path = "_manual_review/unknown_folder/$($node.entity)/$($node.id)"
            action = "manual_review_unknown_folder"
            status = "REVIEW_REQUIRED"
            reason = "Folder is not present in final schema decision table."
        })
    }
}

$realOldPaths = @{}
foreach ($node in $nodeDirs) {
    $realOldPaths[(Normalize-RepoPath $node.old_path)] = $true
}

foreach ($decision in $decisionRows) {
    if ($realOldPaths.ContainsKey($decision.old_path)) {
        continue
    }

    $target = Get-TargetFromDecision $decision.decision
    $action = Get-ActionFromDecision $decision.decision
    if ($decision.status -eq "REVIEW_REQUIRED") {
        $target = "_manual_review/pseudo_decisions"
        $action = "manual_review_pseudo_rule"
    }

    $manifest.Add([PSCustomObject]@{
        old_path = $decision.old_path
        target_path = $target
        action = $action
        status = $decision.status
        reason = $decision.reason
    })
}

$sourceIds = @{}
foreach ($legacy in Import-Csv -Path $legacyMapPath) {
    $sourceId = New-SourceId -LegacyPath $legacy.legacy_path -Seen $sourceIds
    $manifest.Add([PSCustomObject]@{
        old_path = Normalize-RepoPath $legacy.legacy_path
        target_path = "_database/quelle/$sourceId"
        action = "archive_source_once"
        status = "CONFIDENT"
        reason = "Archive original old knowledge file once as source evidence; old action: $($legacy.action); old target: $($legacy.target_primary)"
    })
}

$manualQueue = $decisionRows |
    Where-Object { $_.status -eq "REVIEW_REQUIRED" } |
    ForEach-Object {
        [PSCustomObject]@{
            old_path = $_.old_path
            suggested_target = Get-TargetFromDecision $_.decision
            reason = $_.reason
            status = $_.status
        }
    }

$manifest |
    Sort-Object old_path, action, target_path |
    Export-Csv -Path $manifestPath -NoTypeInformation -Encoding UTF8

$manualQueue |
    Sort-Object old_path |
    Export-Csv -Path $manualQueuePath -NoTypeInformation -Encoding UTF8

$summaryByAction = $manifest |
    Group-Object action |
    Sort-Object Name |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$summaryByStatus = $manifest |
    Group-Object status |
    Sort-Object Name |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$summary = @()
$summary += "# Phase 19 Clean Build Dry Run Summary"
$summary += ""
$summary += "No files were moved, copied, or deleted."
$summary += ""
$summary += "## Outputs"
$summary += ""
$summary += '- `_migration/19_clean_build_dry_run_manifest.csv`'
$summary += '- `_migration/19_manual_review_queue.csv`'
$summary += ""
$summary += "## Counts By Status"
$summary += ""
$summary += "| status | rows |"
$summary += "|---|---:|"
$summary += $summaryByStatus
$summary += ""
$summary += "## Counts By Action"
$summary += ""
$summary += "| action | rows |"
$summary += "|---|---:|"
$summary += $summaryByAction
$summary += ""
$summary += "## Meaning"
$summary += ""
$summary += '- `CONFIDENT` rows are approved decisions; rows with `delete_from_final` are approved non-imports.'
$summary += '- `REVIEW_REQUIRED` rows must stay in `_manual_review` until manually migrated.'
$summary += '- `EXCLUDED` rows are not part of the first clean database.'
$summary += '- `delete_from_final` rows are staging artifacts or forbidden pseudo-nodes and should not be imported.'

$summary | Set-Content -Path $summaryPath -Encoding UTF8

Write-Output "Wrote $manifestPath"
Write-Output "Wrote $manualQueuePath"
Write-Output "Wrote $summaryPath"
