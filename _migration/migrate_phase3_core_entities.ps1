param(
    [string]$TargetRoot = "_graph",
    [string]$MapPath = "_migration/legacy_to_new_map.csv"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$coreEntities = @(
    "akteur",
    "software_digitaltool",
    "foerderprogramm"
)

$aliasByTarget = @{
    "akteur/Architects_For_Future_Deutschland" = "akteur/Architects_for_Future_Deutschland"

    "software_digitaltool/bauteilboerse_bremen" = "software_digitaltool/Bauteilboerse_Bremen"
    "software_digitaltool/bauteilnetz_deutschland" = "software_digitaltool/Bauteilnetz_Deutschland"
    "software_digitaltool/restado" = "software_digitaltool/Restado"
    "software_digitaltool/rotordc" = "software_digitaltool/RotorDC"
    "software_digitaltool/Rotor_DC" = "software_digitaltool/RotorDC"
    "software_digitaltool/salvoweb" = "software_digitaltool/SalvoWEB"
    "software_digitaltool/cycle_up" = "software_digitaltool/Cycle_Up"
    "software_digitaltool/globechain" = "software_digitaltool/Globechain"
    "software_digitaltool/loopfront" = "software_digitaltool/Loopfront"
    "software_digitaltool/material_index" = "software_digitaltool/Material_Index"
    "software_digitaltool/material_reuse_portal" = "software_digitaltool/Material_Reuse_Portal"
    "software_digitaltool/one_click_lca" = "software_digitaltool/One_Click_LCA"
    "software_digitaltool/klimaschutz_konfigurator" = "software_digitaltool/Klimaschutz_Konfigurator"
    "software_digitaltool/Madaster_Plattform" = "software_digitaltool/Madaster"
    "software_digitaltool/Opalis_Plattform" = "software_digitaltool/Opalis"
}

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

function Get-TitleFromMarkdown {
    param([string]$Content, [string]$Fallback)
    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match '^#\s+(.+)$') {
            return $Matches[1].Trim()
        }
    }
    return $Fallback
}

function Split-Targets {
    param([string]$Value)
    $targets = New-Object System.Collections.Generic.List[string]
    if ([string]::IsNullOrWhiteSpace($Value)) { return $targets }
    foreach ($part in ($Value -split ';')) {
        $clean = $part.Trim()
        if (-not [string]::IsNullOrWhiteSpace($clean)) {
            $targets.Add($clean)
        }
    }
    return $targets
}

function Get-CanonicalTarget {
    param([string]$Target)
    if ([string]::IsNullOrWhiteSpace($Target)) { return $null }
    $clean = $Target.Trim()
    if ($clean -match '<|>' -or $clean -notmatch '^[^/]+/[^/]+$') { return $null }
    if ($aliasByTarget.ContainsKey($clean)) { return $aliasByTarget[$clean] }
    return $clean
}

function Get-EntityFromTarget {
    param([string]$Target)
    if ($Target -notmatch '^([^/]+)/(.+)$') { return $null }
    return $Matches[1]
}

function Get-IdFromTarget {
    param([string]$Target)
    if ($Target -notmatch '^([^/]+)/(.+)$') { return $null }
    return $Matches[2]
}

function Get-NormalizedKey {
    param([string]$Value)
    if ($null -eq $Value) { return "" }
    return (($Value -replace '[^A-Za-z0-9]+', '_').Trim('_')).ToLowerInvariant()
}

function Get-ReferenceTitleScore {
    param([object]$Ref, [string]$CanonicalTarget)
    $entity = Get-EntityFromTarget -Target $CanonicalTarget
    $id = Get-IdFromTarget -Target $CanonicalTarget
    $idKey = Get-NormalizedKey -Value $id
    $rawId = Get-IdFromTarget -Target $Ref.raw_target
    $rawIdKey = Get-NormalizedKey -Value $rawId
    $fileBase = [System.IO.Path]::GetFileNameWithoutExtension($Ref.legacy_path)
    $fileKey = Get-NormalizedKey -Value $fileBase
    $score = 0

    if ($Ref.target_role -eq "primary") { $score += 100 }
    if ($fileKey -eq $idKey) { $score += 80 }
    if ($rawIdKey -eq $idKey) { $score += 50 }
    if (-not [string]::IsNullOrWhiteSpace($Ref.map_title)) { $score += 10 }
    if ($entity -eq "software_digitaltool" -and $Ref.legacy_path -match '^bauteilboerse[\\/]') { $score += 30 }
    if ($entity -eq "akteur" -and $Ref.legacy_path -match '^akteur[\\/]') { $score += 30 }
    if ($entity -eq "foerderprogramm" -and $Ref.legacy_path -match '^foerderprogramm[\\/]') { $score += 30 }
    if ($Ref.action -eq "split_platform_profile") { $score += 20 }
    return $score
}

if (-not (Test-Path -LiteralPath $MapPath)) {
    throw "Migration map not found: $MapPath"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null
foreach ($entity in $coreEntities) {
    New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot $entity) | Out-Null
}

$rows = Import-Csv -LiteralPath $MapPath
$sourceRefs = New-Object System.Collections.Generic.List[object]
$canonicalization = New-Object System.Collections.Generic.List[object]

foreach ($row in $rows) {
    $targetsWithRole = New-Object System.Collections.Generic.List[object]
    foreach ($target in (Split-Targets -Value $row.target_primary)) {
        $targetsWithRole.Add([pscustomobject]@{ raw_target = $target; role = "primary" })
    }
    foreach ($target in (Split-Targets -Value $row.target_secondary)) {
        $targetsWithRole.Add([pscustomobject]@{ raw_target = $target; role = "secondary" })
    }

    foreach ($item in $targetsWithRole) {
        $canonical = Get-CanonicalTarget -Target $item.raw_target
        if ($null -eq $canonical) { continue }
        $entity = Get-EntityFromTarget -Target $canonical
        if ($coreEntities -notcontains $entity) { continue }

        if (-not (Test-Path -LiteralPath $row.legacy_path)) { continue }

        if ($canonical -cne $item.raw_target) {
            $canonicalization.Add([pscustomobject]@{
                raw_target = $item.raw_target
                canonical_target = $canonical
                legacy_path = $row.legacy_path
            })
        }

        $sourceRefs.Add([pscustomobject]@{
            legacy_path = $row.legacy_path
            action = $row.action
            risk_flags = $row.risk_flags
            legacy_type = $row.legacy_type
            map_title = $row.title
            raw_target = $item.raw_target
            canonical_target = $canonical
            target_role = $item.role
            target_primary = $row.target_primary
            target_secondary = $row.target_secondary
        })
    }
}

$nodes = New-Object System.Collections.Generic.List[object]
$copyErrors = New-Object System.Collections.Generic.List[object]

foreach ($group in ($sourceRefs | Sort-Object canonical_target, legacy_path -Unique | Group-Object canonical_target)) {
    $target = $group.Name
    $entity = Get-EntityFromTarget -Target $target
    $id = Get-IdFromTarget -Target $target
    if ($id -eq "index") { continue }

    $targetDir = Join-Path (Join-Path $TargetRoot $entity) $id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"
    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    $sourceBlocks = New-Object System.Collections.Generic.List[string]
    $legacyPaths = New-Object System.Collections.Generic.List[string]
    $rawTargets = New-Object System.Collections.Generic.List[string]
    $actions = New-Object System.Collections.Generic.List[string]
    $riskFlags = New-Object System.Collections.Generic.List[string]
    $title = $null

    $orderedRefs = $group.Group |
        Sort-Object @{ Expression = { Get-ReferenceTitleScore -Ref $_ -CanonicalTarget $target }; Descending = $true }, legacy_path, target_role -Unique

    foreach ($ref in $orderedRefs) {
        $legacyPaths.Add($ref.legacy_path)
        $rawTargets.Add($ref.raw_target)
        $actions.Add($ref.action)
        if (-not [string]::IsNullOrWhiteSpace($ref.risk_flags)) { $riskFlags.Add($ref.risk_flags) }

        try {
            $legacyFullPath = (Resolve-Path -LiteralPath $ref.legacy_path).Path
            $legacyContent = [System.IO.File]::ReadAllText($legacyFullPath, $Utf8NoBom)
            if ([string]::IsNullOrWhiteSpace($title)) {
                $titleFallback = if (-not [string]::IsNullOrWhiteSpace($ref.map_title)) { $ref.map_title } else { ($id -replace '_', ' ') }
                $title = Get-TitleFromMarkdown -Content $legacyContent -Fallback $titleFallback
            }

            $legacyCopyName = "legacy_" + (New-SafeFileName -Path $ref.legacy_path)
            $legacyCopyPath = Join-Path $filesDir $legacyCopyName
            Copy-Item -LiteralPath $legacyFullPath -Destination $legacyCopyPath -Force

            $sourceBlocks.Add((@(
                "### Legacy Source: $($ref.legacy_path)"
                ""
                "- Map action: $($ref.action)"
                "- Target role in map: $($ref.target_role)"
                "- Raw mapped target: $($ref.raw_target)"
                "- Original primary target: $($ref.target_primary)"
                "- Original secondary targets: $($ref.target_secondary)"
                ""
                $legacyContent.TrimEnd()
                ""
            ) -join "`n"))
        }
        catch {
            $copyErrors.Add([pscustomobject]@{
                legacy_path = $ref.legacy_path
                canonical_target = $target
                error = $_.Exception.Message
            })
        }
    }

    if ([string]::IsNullOrWhiteSpace($title)) {
        $title = ($id -replace '_', ' ')
    }

    $frontmatter = @(
        "---"
        "id: $(Escape-YamlScalar $id)"
        "entity: $(Escape-YamlScalar $entity)"
        "node_kind: `"core`""
        "migration_status: `"migrated_phase3_core_entities`""
        "title: $(Escape-YamlScalar $title)"
        "source_count: $($legacyPaths.Count)"
        "legacy_paths:"
    )
    foreach ($path in ($legacyPaths | Sort-Object -Unique)) {
        $frontmatter += "  - $(Escape-YamlScalar $path)"
    }
    $frontmatter += "raw_targets:"
    foreach ($raw in ($rawTargets | Sort-Object -Unique)) {
        $frontmatter += "  - $(Escape-YamlScalar $raw)"
    }
    $frontmatter += "migration_actions:"
    foreach ($action in ($actions | Sort-Object -Unique)) {
        $frontmatter += "  - $(Escape-YamlScalar $action)"
    }
    $frontmatter += "risk_flags:"
    foreach ($risk in ($riskFlags | Sort-Object -Unique)) {
        $frontmatter += "  - $(Escape-YamlScalar $risk)"
    }
    $frontmatter += "---"
    $frontmatter += ""

    $semanticNote = switch ($entity) {
        "akteur" { "Akteurprofil. Kann spaeter mit Rollen, Beteiligungen, Orten und Plattformbetreiberschaft verknuepft werden." }
        "software_digitaltool" { "Digitales Werkzeug oder Plattform. Bauteilboersen werden hier als Plattformprofile gefuehrt, nicht als eigene Entitaet." }
        "foerderprogramm" { "Programm- oder Foerderkontext. Kann mit Projekten, Akteuren und Fallstudien verbunden werden." }
        default { "Kernentitaet." }
    }

    $body = @(
        "# $title"
        ""
        "## Migration"
        ""
        "- Canonical target: $target"
        "- Legacy source count: $($legacyPaths.Count)"
        "- Semantic note: $semanticNote"
        ""
        "## Legacy Content"
        ""
        ($sourceBlocks -join "`n")
    ) -join "`n"

    [System.IO.File]::WriteAllText($targetIndex, (($frontmatter -join "`n") + $body), $Utf8NoBom)

    $nodes.Add([pscustomobject]@{
        canonical_target = $target
        entity = $entity
        id = $id
        title = $title
        legacy_source_count = $legacyPaths.Count
        target_index = $targetIndex
    })
}

$sourceRefs | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase3_core_entities_sources.csv"
$nodes | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase3_core_entities_nodes.csv"
$copyErrors | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase3_core_entities_copy_errors.csv"
$canonicalization | Sort-Object raw_target, canonical_target, legacy_path -Unique |
    Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/platform_actor_canonicalization.csv"

$summary = @(
    "# Phase 3 Migration Manifest"
    ""
    "- Target root: $TargetRoot"
    "- Core source references: $($sourceRefs.Count)"
    "- Core nodes generated: $($nodes.Count)"
    "- Canonicalized target references: $($canonicalization.Count)"
    "- Copy errors: $($copyErrors.Count)"
    ""
    "This phase is non-destructive. Legacy actor, platform, tool, and programme files were copied into canonical core nodes."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase3_core_entities_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    source_refs = $sourceRefs.Count
    nodes = $nodes.Count
    canonicalized_refs = $canonicalization.Count
    copy_errors = $copyErrors.Count
}
