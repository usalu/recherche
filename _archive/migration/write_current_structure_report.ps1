param(
    [string]$GraphRoot = "_graph",
    [string]$OutReport = "_migration/09_Current_Graph_Structure_Report.md",
    [string]$OutInventory = "_migration/current_graph_node_inventory.csv",
    [string]$OutFiles = "_migration/current_graph_file_inventory.csv"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Unquote-Value {
    param([string]$Value)
    if ($null -eq $Value) { return "" }
    $v = $Value.Trim()
    if ($v.StartsWith('"') -and $v.EndsWith('"') -and $v.Length -ge 2) {
        $v = $v.Substring(1, $v.Length - 2)
    }
    return $v.Replace('\"', '"').Replace('\\', '\')
}

function Read-Frontmatter {
    param([string]$Path)
    $result = @{}
    $lines = [System.IO.File]::ReadAllLines($Path, [System.Text.Encoding]::UTF8)
    if ($lines.Count -eq 0 -or $lines[0].Trim() -ne "---") { return $result }
    $currentKey = $null
    for ($i = 1; $i -lt $lines.Count; $i++) {
        $line = $lines[$i]
        if ($line.Trim() -eq "---") { break }
        if ($line -match '^\s+-\s*(.+)$' -and $null -ne $currentKey) {
            if (-not ($result[$currentKey] -is [System.Collections.IList])) {
                $result[$currentKey] = New-Object System.Collections.Generic.List[string]
            }
            $result[$currentKey].Add((Unquote-Value -Value $Matches[1])) | Out-Null
            continue
        }
        if ($line -match '^([^:]+):\s*(.*)$') {
            $currentKey = $Matches[1].Trim()
            $value = $Matches[2].Trim()
            if ([string]::IsNullOrWhiteSpace($value)) {
                $result[$currentKey] = New-Object System.Collections.Generic.List[string]
            }
            else {
                $result[$currentKey] = Unquote-Value -Value $value
            }
        }
    }
    return $result
}

function Get-FmValue {
    param([hashtable]$Frontmatter, [string]$Key)
    if (-not $Frontmatter.ContainsKey($Key)) { return "" }
    $value = $Frontmatter[$Key]
    if ($value -is [System.Collections.IEnumerable] -and -not ($value -is [string])) {
        return (@($value) -join "; ")
    }
    return [string]$value
}

function Get-ActionSummary {
    param([string]$Status, [string]$Entity)
    switch -Regex ($Status) {
        "migrated_phase4_case_graph" { return "Generated from a rich case file into case graph nodes: fallstudie/projekt/bauobjekt/reuse_einsatz/datenpunkt/akteur_beteiligung." }
        "migrated_phase5" { return "Preserved as source/meta coverage so no legacy file is lost." }
        "migrated_phase7" { return "Promoted from repeated review labels into a controlled vocabulary knot." }
        "migrated_phase8" { return "Promoted repeated actor label into a canonical akteur node." }
        "migrated_phase9" { return "Generated actor role knot for akteur_beteiligung role normalization." }
        "migrated_phase10" { return "Generated hurdle or boundary-logic knot from repeated review labels." }
        "migrated_phase11" { return "Generated metric/kennwert knot from repeated review labels." }
        "migrated_phase12" { return "Generated component-type/bauteiltyp knot from repeated inventory labels." }
        "migrated_phase3" { return "Migrated or canonicalized a core entity/platform/actor from old files." }
        "migrated_phase2" { return "Semantically corrected from old folder/entity into the new entity structure." }
        "migrated_phase1" { return "Copied stable old knowledge file as a controlled knot in the new structure." }
        default {
            if ($Entity -eq "quelle") { return "Source preservation node." }
            if ([string]::IsNullOrWhiteSpace($Status)) { return "No migration status found; needs inspection." }
            return "Migrated/generated node; inspect migration_status for exact phase."
        }
    }
}

if (-not (Test-Path -LiteralPath $GraphRoot)) {
    throw "Graph root not found: $GraphRoot"
}

$entityDirs = @(Get-ChildItem -LiteralPath $GraphRoot -Directory | Sort-Object Name)
$nodeRows = New-Object System.Collections.Generic.List[object]
$fileRows = New-Object System.Collections.Generic.List[object]
$entityRows = New-Object System.Collections.Generic.List[object]

foreach ($entityDir in $entityDirs) {
    $entity = $entityDir.Name
    $indexFiles = @(Get-ChildItem -LiteralPath $entityDir.FullName -Recurse -File -Filter "index.md")
    $allFiles = @(Get-ChildItem -LiteralPath $entityDir.FullName -Recurse -File)
    $dateienFiles = @($allFiles | Where-Object { $_.FullName -match '\\DATEIEN\\' })
    $nodeDirs = @(Get-ChildItem -LiteralPath $entityDir.FullName -Directory -ErrorAction SilentlyContinue)

    $entityRows.Add([pscustomobject]@{
        entity = $entity
        node_directories = $nodeDirs.Count
        index_files = $indexFiles.Count
        dateien_files = $dateienFiles.Count
        total_files = $allFiles.Count
    }) | Out-Null

    foreach ($file in $allFiles) {
        $rel = Resolve-Path -LiteralPath $file.FullName -Relative
        $fileRows.Add([pscustomobject]@{
            path = $rel
            entity = $entity
            kind = if ($file.Name -eq "index.md") { "index" } elseif ($file.FullName -match '\\DATEIEN\\') { "DATEIEN" } else { "other" }
            size_bytes = $file.Length
        }) | Out-Null
    }

    foreach ($index in $indexFiles) {
        $fm = Read-Frontmatter -Path $index.FullName
        $rel = Resolve-Path -LiteralPath $index.FullName -Relative
        $nodeId = Split-Path (Split-Path $index.FullName -Parent) -Leaf
        $status = Get-FmValue $fm "migration_status"
        $legacy = Get-FmValue $fm "legacy_path"
        $legacyPlural = Get-FmValue $fm "legacy_paths"
        if ([string]::IsNullOrWhiteSpace($legacy)) { $legacy = $legacyPlural }
        $nodeRows.Add([pscustomobject]@{
            entity_folder = $entity
            id_folder = $nodeId
            frontmatter_entity = Get-FmValue $fm "entity"
            title = Get-FmValue $fm "title"
            node_kind = Get-FmValue $fm "node_kind"
            migration_status = $status
            came_from = $legacy
            action_done = Get-ActionSummary -Status $status -Entity $entity
            path = $rel
        }) | Out-Null
    }
}

$nodeRows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $OutInventory
$fileRows | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $OutFiles

$gebaeudeFolder = "Geb" + ([string][char]0x00E4) + "ude"
$legacyExists = @($gebaeudeFolder, "tragwerkssystem", "bauteilboerse", "material", "huerde", "prozessphase") | ForEach-Object {
    [pscustomobject]@{ folder = $_; exists = Test-Path -LiteralPath $_ }
}

$createdStatuses = $nodeRows |
    Group-Object migration_status |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$entityTable = $entityRows |
    Sort-Object entity |
    ForEach-Object { "| $($_.entity) | $($_.node_directories) | $($_.index_files) | $($_.dateien_files) | $($_.total_files) |" }

$report = New-Object System.Collections.Generic.List[string]
$report.Add("# Current Graph Structure Report") | Out-Null
$report.Add("") | Out-Null
$report.Add("## Short Answer") | Out-Null
$report.Add("") | Out-Null
$report.Add("- No final move was done.") | Out-Null
$report.Add("- The old knowledge base folders still exist.") | Out-Null
$report.Add('- The new structure is a staging graph under `_graph`. It is not yet the cleaned final database.') | Out-Null
$report.Add("- The migration copied/generated new nodes and edges; it did not replace the old repo.") | Out-Null
$report.Add("") | Out-Null
$report.Add("## Folder Pattern") | Out-Null
$report.Add("") | Out-Null
$report.Add('```text') | Out-Null
$report.Add("_graph/") | Out-Null
$report.Add("  ENTITAET/") | Out-Null
$report.Add("    ID/") | Out-Null
$report.Add("      index.md") | Out-Null
$report.Add("      DATEIEN/") | Out-Null
$report.Add('```') | Out-Null
$report.Add("") | Out-Null
$report.Add('Each `index.md` is a node candidate for Tolaria/SQLite. `DATEIEN` contains copied or supporting source files when available.') | Out-Null
$report.Add("") | Out-Null
$report.Add("## Old Folders Still Present") | Out-Null
$report.Add("") | Out-Null
foreach ($row in $legacyExists) {
    $report.Add(("- `{0}`: {1}" -f $row.folder, $row.exists)) | Out-Null
}
$report.Add("") | Out-Null
$report.Add("## Current Entity Folders") | Out-Null
$report.Add("") | Out-Null
$report.Add("| entity | node directories | index.md files | DATEIEN files | total files |") | Out-Null
$report.Add("|---|---:|---:|---:|---:|") | Out-Null
foreach ($line in $entityTable) { $report.Add($line) | Out-Null }
$report.Add("") | Out-Null
$report.Add("## Migration Status Summary") | Out-Null
$report.Add("") | Out-Null
$report.Add("| migration_status | node count |") | Out-Null
$report.Add("|---|---:|") | Out-Null
foreach ($line in $createdStatuses) { $report.Add($line) | Out-Null }
$report.Add("") | Out-Null
$report.Add("## Complete Per-Node Inventory") | Out-Null
$report.Add("") | Out-Null
$report.Add('The complete per-node inventory is here: `_migration/current_graph_node_inventory.csv`.') | Out-Null
$report.Add("") | Out-Null
$report.Add("Columns:") | Out-Null
$report.Add('- `entity_folder`: folder under `_graph`.') | Out-Null
$report.Add('- `id_folder`: node ID folder.') | Out-Null
$report.Add('- `title`: node title from frontmatter.') | Out-Null
$report.Add('- `migration_status`: which migration phase created or changed it.') | Out-Null
$report.Add('- `came_from`: legacy path when the node records one.') | Out-Null
$report.Add('- `action_done`: human-readable description of what was done.') | Out-Null
$report.Add('- `path`: exact generated node file.') | Out-Null
$report.Add("") | Out-Null
$report.Add('The complete physical file inventory is here: `_migration/current_graph_file_inventory.csv`.') | Out-Null
$report.Add("") | Out-Null
$report.Add("## Important Warning") | Out-Null
$report.Add("") | Out-Null
$report.Add('There are expected duplicates in this staging graph because one legacy file can become several semantic nodes. Example: a building case can become `fallstudie`, `projekt`, `bauobjekt`, many `reuse_einsatz`, many `datenpunkt`, and `akteur_beteiligung` nodes. That is not a final deduplicated database yet.') | Out-Null
$report.Add("") | Out-Null
$report.Add("The real possible mistake is semantic over-linking: some generated edges classify one raw label into several knots. Those need a QA pass before final import.") | Out-Null

[System.IO.File]::WriteAllText($OutReport, ($report -join "`n"), $Utf8NoBom)

[pscustomobject]@{
    report = $OutReport
    node_inventory = $OutInventory
    file_inventory = $OutFiles
    node_rows = $nodeRows.Count
    file_rows = $fileRows.Count
    entity_rows = $entityRows.Count
}
