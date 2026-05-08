param(
    [string]$TargetRoot = "_graph",
    [string]$MapPath = "_migration/legacy_to_new_map.csv"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$stableEntities = @(
    "material",
    "bauteiltyp",
    "bauteilebene",
    "bauteilzustand",
    "schadstoff",
    "bauweise",
    "bausystem",
    "tragwerksprinzip",
    "tragwerkstyp",
    "fuegung_verbindung",
    "reuse_strategie",
    "reuse_einsatzstatus",
    "bewertungslogik_abgrenzung",
    "ressourcenquelle",
    "beschaffungsweg",
    "funktionswechsel",
    "prozessphase",
    "rueckbauverfahren",
    "aufbereitungsverfahren",
    "methode",
    "logistik",
    "leistungsanforderung",
    "pruefung_nachweis",
    "norm",
    "rechtliche_bedingung",
    "zertifizierung_bewertungssystem",
    "huerde",
    "kennwertdefinition",
    "datenqualitaet",
    "datenmodell",
    "dokumenttyp",
    "tooltyp",
    "plattformfunktion",
    "plattformzugang",
    "wirtschaft",
    "foerderprogramm",
    "programm_kontext",
    "bauobjektklasse",
    "bauobjektrolle",
    "bauobjektstatus",
    "bauaufgabe_intervention",
    "gebaeudetypologie",
    "nutzung",
    "ort",
    "akteurtyp",
    "akteurrolle",
    "akteurleistung",
    "kontextmerkmal"
)

function New-SafeFileName {
    param([string]$Path)
    $safe = $Path -replace '[\\/:*?"<>| ]+', '_'
    $safe = $safe -replace 'ä','ae' -replace 'ö','oe' -replace 'ü','ue'
    $safe = $safe -replace 'Ä','Ae' -replace 'Ö','Oe' -replace 'Ü','Ue'
    $safe = $safe -replace 'ß','ss'
    return $safe.Trim('_')
}

function Escape-YamlScalar {
    param([string]$Value)
    if ($null -eq $Value) { return '""' }
    $escaped = $Value.Replace('\', '\\').Replace('"', '\"')
    return '"' + $escaped + '"'
}

function Get-TitleFromMarkdown {
    param([string]$Content, [string]$Fallback)
    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match '^#\s+(.+)$') {
            return $Matches[1].Trim()
        }
    }
    return $Fallback
}

if (-not (Test-Path -LiteralPath $MapPath)) {
    throw "Migration map not found: $MapPath"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null

foreach ($entity in $stableEntities) {
    New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot $entity) | Out-Null
}

$rows = Import-Csv -LiteralPath $MapPath
$migrated = New-Object System.Collections.Generic.List[object]
$skipped = New-Object System.Collections.Generic.List[object]

foreach ($row in $rows) {
    if ($row.action -ne "move_as_knot") { continue }
    if (-not $row.target_primary -or $row.target_primary -notmatch '^[^/]+/[^/]+$') { continue }

    $entity, $id = $row.target_primary -split '/', 2
    if ($stableEntities -notcontains $entity) { continue }
    if ($id -eq "index") { continue }
    if ($row.target_primary -match '<|>') { continue }

    $legacyPath = $row.legacy_path
    if (-not (Test-Path -LiteralPath $legacyPath)) {
        $skipped.Add([pscustomobject]@{
            legacy_path = $legacyPath
            target_primary = $row.target_primary
            reason = "legacy file missing"
        })
        continue
    }

    $targetDir = Join-Path (Join-Path $TargetRoot $entity) $id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"

    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    $legacyFullPath = (Resolve-Path -LiteralPath $legacyPath).Path
    $legacyContent = [System.IO.File]::ReadAllText($legacyFullPath, $Utf8NoBom)
    $titleFallback = ($id -replace '_', ' ')
    $title = Get-TitleFromMarkdown -Content $legacyContent -Fallback $titleFallback
    $legacyCopyName = "legacy_" + (New-SafeFileName -Path $legacyPath)
    $legacyCopyPath = Join-Path $filesDir $legacyCopyName

    Copy-Item -LiteralPath $legacyFullPath -Destination $legacyCopyPath -Force

    $frontmatter = @(
        "---"
        "id: $(Escape-YamlScalar $id)"
        "entity: $(Escape-YamlScalar $entity)"
        "node_kind: `"knot`""
        "migration_status: `"migrated_phase1_stable_knots`""
        "migration_action: $(Escape-YamlScalar $row.action)"
        "title: $(Escape-YamlScalar $title)"
        "legacy_type: $(Escape-YamlScalar $row.legacy_type)"
        "legacy_paths:"
        "  - $(Escape-YamlScalar $legacyPath)"
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
        "- Legacy type: $($row.legacy_type)"
        "- Migration action: $($row.action)"
        "- Target: $($row.target_primary)"
        "- Secondary targets: $($row.target_secondary)"
        "- Risk flags: $($row.risk_flags)"
        ""
        "## Legacy Content"
        ""
        $legacyContent.TrimEnd()
        ""
    ) -join "`n"

    [System.IO.File]::WriteAllText($targetIndex, $frontmatter + $body, $Utf8NoBom)

    $migrated.Add([pscustomobject]@{
        legacy_path = $legacyPath
        target_primary = $row.target_primary
        target_index = $targetIndex
        legacy_copy = $legacyCopyPath
    })
}

$manifestPath = "_migration/phase1_stable_knots_migrated.csv"
$skippedPath = "_migration/phase1_stable_knots_skipped.csv"
$migrated | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $manifestPath
$skipped | Export-Csv -NoTypeInformation -Encoding UTF8 -Path $skippedPath

$summary = @(
    "# Phase 1 Migration Manifest"
    ""
    "- Target root: $TargetRoot"
    "- Migrated stable knot files: $($migrated.Count)"
    "- Skipped files: $($skipped.Count)"
    "- Source map: $MapPath"
    "- Manifest CSV: $manifestPath"
    "- Skipped CSV: $skippedPath"
    ""
    "This phase is non-destructive. Legacy files were copied, not moved."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase1_migration_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    migrated = $migrated.Count
    skipped = $skipped.Count
    manifest = $manifestPath
    skipped_manifest = $skippedPath
}
