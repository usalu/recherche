param(
    [string]$TargetRoot = "_graph",
    [string]$MapPath = "_migration/legacy_to_new_map.csv"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Escape-YamlScalar {
    param([string]$Value)
    if ($null -eq $Value) { return '""' }
    $escaped = $Value.Replace('\', '\\').Replace('"', '\"')
    return '"' + $escaped + '"'
}

function New-SafeFileName {
    param([string]$Path)
    $safe = $Path -replace '[^A-Za-z0-9_.-]+', '_'
    return $safe.Trim('_')
}

function Get-ShortHash {
    param([string]$Value)
    $md5 = [System.Security.Cryptography.MD5]::Create()
    try {
        $bytes = [System.Text.Encoding]::UTF8.GetBytes($Value)
        $hashBytes = $md5.ComputeHash($bytes)
        return (($hashBytes | ForEach-Object { $_.ToString("x2") }) -join "").Substring(0, 8)
    }
    finally {
        $md5.Dispose()
    }
}

function New-LegacySourceId {
    param([string]$LegacyPath)
    $safe = New-SafeFileName -Path $LegacyPath
    $safe = [System.IO.Path]::ChangeExtension($safe, $null)
    if ($safe.Length -gt 82) {
        $safe = $safe.Substring(0, 82).Trim('_') + "_" + (Get-ShortHash -Value $LegacyPath)
    }
    return "Legacy_$safe"
}

function Get-TitleFromMarkdown {
    param([string]$Content, [string]$Fallback)
    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match '^#\s+(.+)$') { return $Matches[1].Trim() }
    }
    return $Fallback
}

function Add-CoveredPaths {
    param([hashtable]$Covered, [string]$CsvPath)
    if (-not (Test-Path -LiteralPath $CsvPath)) { return }
    foreach ($row in (Import-Csv -LiteralPath $CsvPath)) {
        if ($row.PSObject.Properties.Name -contains "legacy_path" -and -not [string]::IsNullOrWhiteSpace($row.legacy_path)) {
            $Covered[$row.legacy_path] = $true
        }
    }
}

if (-not (Test-Path -LiteralPath $MapPath)) {
    throw "Migration map not found: $MapPath"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "quelle") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "meta") | Out-Null

$covered = @{}
Add-CoveredPaths -Covered $covered -CsvPath "_migration/phase1_stable_knots_migrated.csv"
Add-CoveredPaths -Covered $covered -CsvPath "_migration/phase2_semantic_corrections_sources.csv"
Add-CoveredPaths -Covered $covered -CsvPath "_migration/phase3_core_entities_sources.csv"
Add-CoveredPaths -Covered $covered -CsvPath "_migration/phase4_case_graph_sources.csv"

$rows = Import-Csv -LiteralPath $MapPath
$phase5Nodes = New-Object System.Collections.Generic.List[object]
$coverageRows = New-Object System.Collections.Generic.List[object]
$missingAfterPhase5 = New-Object System.Collections.Generic.List[object]

foreach ($row in ($rows | Sort-Object legacy_path -Unique)) {
    $legacyPath = $row.legacy_path
    $wasCovered = $covered.ContainsKey($legacyPath)
    $exists = Test-Path -LiteralPath $legacyPath

    if (-not $wasCovered -and $exists) {
        $legacyFolder = ($legacyPath -split '[\\/]')[0]
        $entity = if ($row.action -eq "keep_meta" -or $legacyFolder -eq "meta" -or $legacyPath -eq "AGENTS.md") { "meta" } else { "quelle" }
        $id = New-LegacySourceId -LegacyPath $legacyPath
        $targetDir = Join-Path (Join-Path $TargetRoot $entity) $id
        $filesDir = Join-Path $targetDir "DATEIEN"
        $targetIndex = Join-Path $targetDir "index.md"
        New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

        $fullPath = (Resolve-Path -LiteralPath $legacyPath).Path
        $content = [System.IO.File]::ReadAllText($fullPath, $Utf8NoBom)
        $titleFallback = if (-not [string]::IsNullOrWhiteSpace($row.title)) { $row.title } else { $legacyPath }
        $title = Get-TitleFromMarkdown -Content $content -Fallback $titleFallback
        $copyName = "legacy_" + (New-SafeFileName -Path $legacyPath)
        Copy-Item -LiteralPath $fullPath -Destination (Join-Path $filesDir $copyName) -Force

        $frontmatter = @(
            "---"
            "id: $(Escape-YamlScalar $id)"
            "entity: $(Escape-YamlScalar $entity)"
            "node_kind: `"source`""
            "migration_status: `"migrated_phase5_legacy_source`""
            "title: $(Escape-YamlScalar $title)"
            "legacy_path: $(Escape-YamlScalar $legacyPath)"
            "migration_action: $(Escape-YamlScalar $row.action)"
            "legacy_type: $(Escape-YamlScalar $row.legacy_type)"
            "target_primary: $(Escape-YamlScalar $row.target_primary)"
            "target_secondary: $(Escape-YamlScalar $row.target_secondary)"
            "risk_flags: $(Escape-YamlScalar $row.risk_flags)"
            "---"
            ""
        ) -join "`n"

        $body = @(
            "# $title"
            ""
            "## Migration"
            ""
            "- Legacy path: $legacyPath"
            "- Action in migration map: $($row.action)"
            "- Reason: not already consumed by phase 1-4, so preserved as source/meta node."
            "- Original primary target: $($row.target_primary)"
            "- Original secondary targets: $($row.target_secondary)"
            ""
            "## Legacy Content"
            ""
            $content.TrimEnd()
            ""
        ) -join "`n"

        [System.IO.File]::WriteAllText($targetIndex, $frontmatter + $body, $Utf8NoBom)
        $covered[$legacyPath] = $true

        $phase5Nodes.Add([pscustomobject]@{
            legacy_path = $legacyPath
            entity = $entity
            id = $id
            target = "$entity/$id"
            target_index = $targetIndex
            action = $row.action
        })
    }

    $coverageRows.Add([pscustomobject]@{
        legacy_path = $legacyPath
        exists = $exists
        covered_after_phase5 = $covered.ContainsKey($legacyPath)
        action = $row.action
        target_primary = $row.target_primary
        target_secondary = $row.target_secondary
    })
}

foreach ($coverage in $coverageRows) {
    if (-not $coverage.covered_after_phase5) { $missingAfterPhase5.Add($coverage) }
}

$phase5Nodes | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase5_legacy_source_nodes.csv"
$coverageRows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/final_legacy_coverage.csv"
$missingAfterPhase5 | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/final_legacy_missing.csv"

$entityCounts = Get-ChildItem -LiteralPath $TargetRoot -Directory |
    Where-Object { $_.Name -ne "_system" } |
    ForEach-Object {
        [pscustomobject]@{
            entity = $_.Name
            node_count = @(Get-ChildItem -LiteralPath $_.FullName -Directory -ErrorAction SilentlyContinue).Count
        }
    } |
    Sort-Object entity
$entityCounts | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/final_graph_entity_counts.csv"

$summaryLines = New-Object System.Collections.Generic.List[string]
$summaryLines.Add("# Final Legacy Coverage Report")
$summaryLines.Add("")
$summaryLines.Add("- Source map: $MapPath")
$summaryLines.Add("- Unique mapped legacy paths: $($coverageRows.Count)")
$summaryLines.Add("- Phase 5 source/meta nodes created: $($phase5Nodes.Count)")
$summaryLines.Add("- Missing after phase 5: $($missingAfterPhase5.Count)")
$summaryLines.Add("")
$summaryLines.Add("## Entity Counts")
$summaryLines.Add("")
foreach ($count in $entityCounts) {
    $summaryLines.Add("- $($count.entity): $($count.node_count)")
}
$summaryLines.Add("")
$summaryLines.Add("## Notes")
$summaryLines.Add("")
$summaryLines.Add("- The migration is staged in _graph; legacy files were copied, not moved.")
$summaryLines.Add("- quelle and meta nodes are preservation nodes for indexes, reports, archive material, and system notes that did not belong cleanly in a semantic entity.")
$summaryLines.Add("- Detailed extraction from case tables is in reuse_einsatz, datenpunkt, and akteur_beteiligung.")
$summaryLines.Add("")

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/final_legacy_coverage_report.md"), ($summaryLines -join "`n"), $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    unique_legacy_paths = $coverageRows.Count
    phase5_nodes = $phase5Nodes.Count
    missing_after_phase5 = $missingAfterPhase5.Count
    entity_count_rows = $entityCounts.Count
}
