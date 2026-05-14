param(
    [string]$TargetRoot = "_graph",
    [string]$MapPath = "_migration/legacy_to_new_map.csv"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

$graphEntities = @(
    "fallstudie",
    "projekt",
    "bauobjekt",
    "reuse_einsatz",
    "reuse_kette",
    "reuse_kettenstation",
    "akteur_beteiligung",
    "bauobjekt_beteiligung",
    "datenpunkt",
    "beleg"
)

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

function New-SafeId {
    param([string]$Value, [int]$MaxLength = 90)
    if ([string]::IsNullOrWhiteSpace($Value)) { return "Unbenannt" }
    $safe = $Value -replace '[^A-Za-z0-9]+', '_'
    $safe = $safe.Trim('_')
    if ([string]::IsNullOrWhiteSpace($safe)) { $safe = "Unbenannt" }
    if ($safe.Length -gt $MaxLength) { $safe = $safe.Substring(0, $MaxLength).Trim('_') }
    return $safe
}

function Split-Targets {
    param([string]$Value)
    $targets = New-Object System.Collections.Generic.List[string]
    if ([string]::IsNullOrWhiteSpace($Value)) { return $targets }
    foreach ($part in ($Value -split ';')) {
        $clean = $part.Trim()
        if (-not [string]::IsNullOrWhiteSpace($clean)) { $targets.Add($clean) }
    }
    return $targets
}

function Get-TargetId {
    param([string]$Target, [string]$Entity)
    if ([string]::IsNullOrWhiteSpace($Target)) { return $null }
    if ($Target -match '<|>') { return $null }
    if ($Target -match "^$([regex]::Escape($Entity))/(.+)$") {
        return $Matches[1]
    }
    return $null
}

function Get-FirstTargetId {
    param([object]$Row, [string]$Entity)
    foreach ($target in (Split-Targets -Value $Row.target_primary)) {
        $id = Get-TargetId -Target $target -Entity $Entity
        if ($null -ne $id) { return $id }
    }
    foreach ($target in (Split-Targets -Value $Row.target_secondary)) {
        $id = Get-TargetId -Target $target -Entity $Entity
        if ($null -ne $id) { return $id }
    }
    return $null
}

function Get-TitleFromMarkdown {
    param([string]$Content, [string]$Fallback)
    foreach ($line in ($Content -split "`r?`n")) {
        if ($line -match '^#\s+(.+)$') { return $Matches[1].Trim() }
    }
    return $Fallback
}

function Get-SectionByKeyword {
    param([string]$Content, [string]$Keyword)
    $lines = $Content -split "`r?`n"
    $start = -1
    for ($i = 0; $i -lt $lines.Count; $i++) {
        if ($lines[$i] -match '^#{2,6}\s+' -and $lines[$i] -match [regex]::Escape($Keyword)) {
            $start = $i
            break
        }
    }
    if ($start -lt 0) { return "" }
    $end = $lines.Count
    for ($j = $start + 1; $j -lt $lines.Count; $j++) {
        if ($lines[$j] -match '^#{2,6}\s+') {
            $end = $j
            break
        }
    }
    return ($lines[$start..($end - 1)] -join "`n")
}

function Split-MarkdownTableLine {
    param([string]$Line)
    $trimmed = $Line.Trim()
    if ($trimmed.StartsWith('|')) { $trimmed = $trimmed.Substring(1) }
    if ($trimmed.EndsWith('|')) { $trimmed = $trimmed.Substring(0, $trimmed.Length - 1) }
    return @($trimmed -split '\|' | ForEach-Object { $_.Trim() })
}

function ConvertFrom-MarkdownTable {
    param([string]$Markdown)
    $tableLines = @($Markdown -split "`r?`n" | Where-Object { $_.Trim().StartsWith('|') })
    if ($tableLines.Count -lt 2) { return @() }

    $headers = Split-MarkdownTableLine -Line $tableLines[0]
    $rows = New-Object System.Collections.Generic.List[object]

    for ($i = 1; $i -lt $tableLines.Count; $i++) {
        $cells = Split-MarkdownTableLine -Line $tableLines[$i]
        $isSeparator = $true
        foreach ($cell in $cells) {
            if ($cell -notmatch '^:?-{2,}:?$') { $isSeparator = $false; break }
        }
        if ($isSeparator) { continue }

        $obj = [ordered]@{}
        for ($c = 0; $c -lt $headers.Count; $c++) {
            $header = if ([string]::IsNullOrWhiteSpace($headers[$c])) { "Spalte_$c" } else { $headers[$c] }
            if ($obj.Contains($header)) { $header = "${header}_$c" }
            $value = if ($c -lt $cells.Count) { $cells[$c] } else { "" }
            $obj[$header] = $value
        }
        $rows.Add([pscustomobject]$obj)
    }

    return $rows.ToArray()
}

function Get-TableValue {
    param([object]$Row, [string[]]$Patterns)
    foreach ($pattern in $Patterns) {
        foreach ($prop in $Row.PSObject.Properties) {
            if ($prop.Name -match $pattern) {
                return [string]$prop.Value
            }
        }
    }
    return ""
}

function Format-TableRowAsMarkdown {
    param([object]$Row)
    $lines = New-Object System.Collections.Generic.List[string]
    foreach ($prop in $Row.PSObject.Properties) {
        $lines.Add("- **$($prop.Name):** $($prop.Value)")
    }
    return ($lines -join "`n")
}

function Copy-LegacySources {
    param([array]$Sources, [string]$FilesDir)
    New-Item -ItemType Directory -Force -Path $FilesDir | Out-Null
    foreach ($source in $Sources) {
        $copyName = "legacy_" + (New-SafeFileName -Path $source.legacy_path)
        Copy-Item -LiteralPath $source.full_path -Destination (Join-Path $FilesDir $copyName) -Force
    }
}

function Write-GraphNode {
    param(
        [string]$Entity,
        [string]$Id,
        [string]$Title,
        [string]$NodeKind,
        [hashtable]$Fields,
        [string]$Body,
        [array]$CopySources = @()
    )

    $targetDir = Join-Path (Join-Path $TargetRoot $Entity) $Id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"
    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    if ($CopySources.Count -gt 0) {
        Copy-LegacySources -Sources $CopySources -FilesDir $filesDir
    }

    $frontmatter = New-Object System.Collections.Generic.List[string]
    $frontmatter.Add("---")
    $frontmatter.Add("id: $(Escape-YamlScalar $Id)")
    $frontmatter.Add("entity: $(Escape-YamlScalar $Entity)")
    $frontmatter.Add("node_kind: $(Escape-YamlScalar $NodeKind)")
    $frontmatter.Add("migration_status: `"migrated_phase4_case_graph`"")
    $frontmatter.Add("title: $(Escape-YamlScalar $Title)")
    foreach ($key in ($Fields.Keys | Sort-Object)) {
        $value = $Fields[$key]
        if ($value -is [array]) {
            $frontmatter.Add("${key}:")
            foreach ($item in $value) { $frontmatter.Add("  - $(Escape-YamlScalar ([string]$item))") }
        }
        else {
            $frontmatter.Add("${key}: $(Escape-YamlScalar ([string]$value))")
        }
    }
    $frontmatter.Add("---")
    $frontmatter.Add("")

    [System.IO.File]::WriteAllText($targetIndex, (($frontmatter -join "`n") + $Body), $Utf8NoBom)

    return [pscustomobject]@{
        entity = $Entity
        id = $Id
        title = $Title
        target = "$Entity/$Id"
        target_index = $targetIndex
    }
}

if (-not (Test-Path -LiteralPath $MapPath)) {
    throw "Migration map not found: $MapPath"
}

New-Item -ItemType Directory -Force -Path $TargetRoot | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null
foreach ($entity in $graphEntities) {
    New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot $entity) | Out-Null
}

$rows = Import-Csv -LiteralPath $MapPath
$caseSources = New-Object System.Collections.Generic.List[object]
$sourceLog = New-Object System.Collections.Generic.List[object]

foreach ($row in $rows) {
    $legacyFolder = ($row.legacy_path -split '[\\/]')[0]
    $isCaseAction = $row.action -in @("split_into_case_graph", "keep_or_split_case")
    $hasCaseTarget = $false
    foreach ($target in @((Split-Targets -Value $row.target_primary) + (Split-Targets -Value $row.target_secondary))) {
        if ($target -match '^(fallstudie|projekt)/') { $hasCaseTarget = $true }
    }
    if (-not ($isCaseAction -or ($legacyFolder -eq "fallstudie" -and $hasCaseTarget))) { continue }
    if (-not (Test-Path -LiteralPath $row.legacy_path)) { continue }

    $content = [System.IO.File]::ReadAllText((Resolve-Path -LiteralPath $row.legacy_path).Path, $Utf8NoBom)
    $fallbackId = New-SafeId -Value ([System.IO.Path]::GetFileNameWithoutExtension($row.legacy_path))
    $fallstudieId = Get-FirstTargetId -Row $row -Entity "fallstudie"
    if ($null -eq $fallstudieId -and $legacyFolder -eq "fallstudie") { $fallstudieId = $fallbackId }
    if ($null -eq $fallstudieId) { $fallstudieId = $fallbackId }

    $projectId = Get-FirstTargetId -Row $row -Entity "projekt"
    if ($null -eq $projectId -and ($legacyFolder -eq "gebaeude" -or $legacyFolder -like "Geb*")) { $projectId = $fallstudieId }
    if ($null -eq $projectId -and $row.action -eq "split_into_case_graph") { $projectId = $fallstudieId }

    $bauobjektId = if ($legacyFolder -eq "gebaeude" -or $legacyFolder -like "Geb*") { $fallstudieId } else { $null }

    $titleFallback = if (-not [string]::IsNullOrWhiteSpace($row.title)) { $row.title } else { ($fallstudieId -replace '_', ' ') }
    $title = Get-TitleFromMarkdown -Content $content -Fallback $titleFallback

    $source = [pscustomobject]@{
        legacy_path = $row.legacy_path
        full_path = (Resolve-Path -LiteralPath $row.legacy_path).Path
        action = $row.action
        risk_flags = $row.risk_flags
        legacy_type = $row.legacy_type
        target_primary = $row.target_primary
        target_secondary = $row.target_secondary
        fallstudie_id = $fallstudieId
        projekt_id = $projectId
        bauobjekt_id = $bauobjektId
        title = $title
        content = $content
    }

    $caseSources.Add($source)
    $sourceLog.Add([pscustomobject]@{
        legacy_path = $row.legacy_path
        fallstudie_id = $fallstudieId
        projekt_id = $projectId
        bauobjekt_id = $bauobjektId
        action = $row.action
        target_primary = $row.target_primary
        target_secondary = $row.target_secondary
    })
}

$nodeLog = New-Object System.Collections.Generic.List[object]
$reuseRowsLog = New-Object System.Collections.Generic.List[object]
$datenpunktRowsLog = New-Object System.Collections.Generic.List[object]
$actorRowsLog = New-Object System.Collections.Generic.List[object]

foreach ($caseGroup in ($caseSources | Group-Object fallstudie_id | Sort-Object Name)) {
    $caseId = $caseGroup.Name
    $sources = @($caseGroup.Group | Sort-Object legacy_path)
    $primarySource = $sources | Select-Object -First 1
    $title = $primarySource.title
    $legacyPaths = @($sources | ForEach-Object { $_.legacy_path })
    $projectId = @($sources | Where-Object { -not [string]::IsNullOrWhiteSpace($_.projekt_id) } | Select-Object -First 1 -ExpandProperty projekt_id)
    $bauobjektId = @($sources | Where-Object { -not [string]::IsNullOrWhiteSpace($_.bauobjekt_id) } | Select-Object -First 1 -ExpandProperty bauobjekt_id)

    $allInventoryRows = New-Object System.Collections.Generic.List[object]
    $allKennwertRows = New-Object System.Collections.Generic.List[object]
    $allEntityRows = New-Object System.Collections.Generic.List[object]
    $legacyBlocks = New-Object System.Collections.Generic.List[string]
    $projectContextBlocks = New-Object System.Collections.Generic.List[string]
    $isReuseChain = $false

    foreach ($source in $sources) {
        $inventorySection = Get-SectionByKeyword -Content $source.content -Keyword "BAUTEIL-INVENTAR"
        foreach ($row in (ConvertFrom-MarkdownTable -Markdown $inventorySection)) {
            $allInventoryRows.Add([pscustomobject]@{ source = $source; row = $row })
        }

        $kennwertSection = Get-SectionByKeyword -Content $source.content -Keyword "KENNWERTE"
        foreach ($row in (ConvertFrom-MarkdownTable -Markdown $kennwertSection)) {
            $allKennwertRows.Add([pscustomobject]@{ source = $source; row = $row })
        }

        $entitySection = Get-SectionByKeyword -Content $source.content -Keyword "ENTIT"
        foreach ($row in (ConvertFrom-MarkdownTable -Markdown $entitySection)) {
            $allEntityRows.Add([pscustomobject]@{ source = $source; row = $row })
        }

        $projectContext = Get-SectionByKeyword -Content $source.content -Keyword "FALLSTUDIE"
        if (-not [string]::IsNullOrWhiteSpace($projectContext)) {
            $projectContextBlocks.Add("### $($source.legacy_path)`n`n$projectContext")
        }

        if ($source.content -match 'Reuse-Kette|Donor|Receiver|->') { $isReuseChain = $true }

        $legacyBlocks.Add((@(
            "### Legacy Source: $($source.legacy_path)"
            ""
            "- Map action: $($source.action)"
            "- Primary target: $($source.target_primary)"
            "- Secondary targets: $($source.target_secondary)"
            "- Risk flags: $($source.risk_flags)"
            ""
            $source.content.TrimEnd()
            ""
        ) -join "`n"))
    }

    $fallstudieBody = @(
        "# $title"
        ""
        "## Migration"
        ""
        "- Fallstudie ID: $caseId"
        "- Legacy source count: $($sources.Count)"
        "- Generated project: $projectId"
        "- Generated bauobjekt: $bauobjektId"
        "- Extracted reuse_einsatz rows: $($allInventoryRows.Count)"
        "- Extracted datenpunkt rows: $($allKennwertRows.Count)"
        "- Extracted entity mapping rows: $($allEntityRows.Count)"
        "- Reuse chain detected: $isReuseChain"
        ""
        "## Legacy Content"
        ""
        ($legacyBlocks -join "`n")
    ) -join "`n"

    $nodeLog.Add((Write-GraphNode -Entity "fallstudie" -Id $caseId -Title $title -NodeKind "core" -CopySources $sources -Fields @{
        legacy_paths = $legacyPaths
        projekt = $projectId
        bauobjekt = $bauobjektId
        reuse_chain_detected = [string]$isReuseChain
    } -Body $fallstudieBody))

    if (-not [string]::IsNullOrWhiteSpace($projectId)) {
        $projectBody = @(
            "# $title"
            ""
            "## Migration"
            ""
            "- Generated from fallstudie: fallstudie/$caseId"
            "- Legacy source count: $($sources.Count)"
            "- Bauobjekt: $bauobjektId"
            ""
            "## Extracted Project Context"
            ""
            if ($projectContextBlocks.Count -gt 0) { ($projectContextBlocks -join "`n`n") } else { "Kein eigener Projektabschnitt automatisch erkannt. Vollstaendige Quelle liegt in DATEIEN und in der Fallstudie." }
            ""
        ) -join "`n"

        $nodeLog.Add((Write-GraphNode -Entity "projekt" -Id $projectId -Title $title -NodeKind "core" -CopySources $sources -Fields @{
            fallstudie = "fallstudie/$caseId"
            bauobjekt = $bauobjektId
            legacy_paths = $legacyPaths
        } -Body $projectBody))
    }

    if (-not [string]::IsNullOrWhiteSpace($bauobjektId)) {
        $bauobjektBody = @(
            "# $title"
            ""
            "## Migration"
            ""
            "- Generated from fallstudie: fallstudie/$caseId"
            "- Project: projekt/$projectId"
            "- Role: Hauptbauobjekt / receiver object unless the legacy content states otherwise."
            ""
            "## Extracted Object Context"
            ""
            if ($projectContextBlocks.Count -gt 0) { ($projectContextBlocks -join "`n`n") } else { "Kein eigener Bauobjektabschnitt automatisch erkannt. Vollstaendige Quelle liegt in DATEIEN und in der Fallstudie." }
            ""
        ) -join "`n"

        $nodeLog.Add((Write-GraphNode -Entity "bauobjekt" -Id $bauobjektId -Title $title -NodeKind "core" -CopySources $sources -Fields @{
            fallstudie = "fallstudie/$caseId"
            projekt = $projectId
            legacy_paths = $legacyPaths
        } -Body $bauobjektBody))
    }

    $rowIndex = 0
    foreach ($entry in $allInventoryRows) {
        $rowIndex++
        $component = Get-TableValue -Row $entry.row -Patterns @('^Bauteil$', 'Bauteil')
        if ([string]::IsNullOrWhiteSpace($component) -or $component -match '^-+$') { continue }
        $material = Get-TableValue -Row $entry.row -Patterns @('^Material$')
        $herkunft = Get-TableValue -Row $entry.row -Patterns @('Herkunft')
        $oldFunction = Get-TableValue -Row $entry.row -Patterns @('alte Funktion')
        $newFunction = Get-TableValue -Row $entry.row -Patterns @('neue Funktion')
        $quantity = Get-TableValue -Row $entry.row -Patterns @('Menge|Umfang')
        $pruefung = Get-TableValue -Row $entry.row -Patterns @('Pr.fung')
        $normRecht = Get-TableValue -Row $entry.row -Patterns @('Norm|Recht')
        $huerde = Get-TableValue -Row $entry.row -Patterns @('H.rde')
        $quelle = Get-TableValue -Row $entry.row -Patterns @('Quelle')
        $reuseId = "$caseId`__$($rowIndex.ToString('000'))__$((New-SafeId -Value $component -MaxLength 48))"
        $reuseTitle = "$component - $title"
        $reuseBody = @(
            "# $reuseTitle"
            ""
            "## Migration"
            ""
            "- Generated from fallstudie: fallstudie/$caseId"
            "- Source legacy file: $($entry.source.legacy_path)"
            "- Source table: BAUTEIL-INVENTAR"
            ""
            "## Extracted Row"
            ""
            (Format-TableRowAsMarkdown -Row $entry.row)
            ""
        ) -join "`n"

        $nodeLog.Add((Write-GraphNode -Entity "reuse_einsatz" -Id $reuseId -Title $reuseTitle -NodeKind "core" -Fields @{
            fallstudie = "fallstudie/$caseId"
            projekt = $projectId
            bauobjekt = $bauobjektId
            bauteil_label = $component
            material_label = $material
            herkunft_label = $herkunft
            alte_funktion = $oldFunction
            neue_funktion = $newFunction
            menge_umfang = $quantity
            pruefung_label = $pruefung
            norm_recht_label = $normRecht
            huerde_label = $huerde
            quelle_label = $quelle
            legacy_path = $entry.source.legacy_path
        } -Body $reuseBody))

        $reuseRowsLog.Add([pscustomobject]@{
            fallstudie = $caseId
            reuse_einsatz = $reuseId
            legacy_path = $entry.source.legacy_path
            bauteil = $component
            material = $material
            herkunft = $herkunft
            menge_umfang = $quantity
        })
    }

    $kennwertIndex = 0
    foreach ($entry in $allKennwertRows) {
        $kennwertIndex++
        $kennwert = Get-TableValue -Row $entry.row -Patterns @('^Kennwert$', 'Kennwert')
        $wert = Get-TableValue -Row $entry.row -Patterns @('^Wert$', 'Wert')
        if ([string]::IsNullOrWhiteSpace($kennwert) -or [string]::IsNullOrWhiteSpace($wert) -or $wert -match '^(unbekannt|-+)$') { continue }
        $einheit = Get-TableValue -Row $entry.row -Patterns @('Einheit')
        $methode = Get-TableValue -Row $entry.row -Patterns @('Methode|Datenmodell|Software')
        $bilanzgrenze = Get-TableValue -Row $entry.row -Patterns @('Bilanzgrenze')
        $quelle = Get-TableValue -Row $entry.row -Patterns @('Quelle')
        $vertrauen = Get-TableValue -Row $entry.row -Patterns @('Vertrauensgrad')
        $datenpunktId = "$caseId`__$($kennwertIndex.ToString('000'))__$((New-SafeId -Value $kennwert -MaxLength 48))"
        $datenpunktTitle = "$kennwert - $title"
        $datenpunktBody = @(
            "# $datenpunktTitle"
            ""
            "## Migration"
            ""
            "- Generated from fallstudie: fallstudie/$caseId"
            "- Source legacy file: $($entry.source.legacy_path)"
            "- Source table: KENNWERTE"
            ""
            "## Extracted Row"
            ""
            (Format-TableRowAsMarkdown -Row $entry.row)
            ""
        ) -join "`n"

        $nodeLog.Add((Write-GraphNode -Entity "datenpunkt" -Id $datenpunktId -Title $datenpunktTitle -NodeKind "core" -Fields @{
            fallstudie = "fallstudie/$caseId"
            projekt = $projectId
            bauobjekt = $bauobjektId
            kennwert_label = $kennwert
            wert = $wert
            einheit = $einheit
            methode_label = $methode
            bilanzgrenze = $bilanzgrenze
            quelle_label = $quelle
            vertrauensgrad = $vertrauen
            legacy_path = $entry.source.legacy_path
        } -Body $datenpunktBody))

        $datenpunktRowsLog.Add([pscustomobject]@{
            fallstudie = $caseId
            datenpunkt = $datenpunktId
            legacy_path = $entry.source.legacy_path
            kennwert = $kennwert
            wert = $wert
            einheit = $einheit
        })
    }

    $actorIndex = 0
    foreach ($entry in $allEntityRows) {
        $entityLabel = Get-TableValue -Row $entry.row -Patterns @('Entit')
        $value = Get-TableValue -Row $entry.row -Patterns @('^Wert$', 'Wert')
        if ($entityLabel -notmatch 'People|Akteur|Person' -or [string]::IsNullOrWhiteSpace($value)) { continue }
        $actorIndex++
        $relationId = "$caseId`__$($actorIndex.ToString('000'))__$((New-SafeId -Value $value -MaxLength 48))"
        $relationship = Get-TableValue -Row $entry.row -Patterns @('Beziehung')
        $quelle = Get-TableValue -Row $entry.row -Patterns @('Quelle|Beleg')
        $confidence = Get-TableValue -Row $entry.row -Patterns @('Vertrauensgrad')
        $relationBody = @(
            "# $value - $title"
            ""
            "## Migration"
            ""
            "- Generated from fallstudie: fallstudie/$caseId"
            "- Source legacy file: $($entry.source.legacy_path)"
            "- Source table: ENTITAETEN-MAPPING"
            "- Akteur is stored as a candidate label here; canonical actor merging can happen in a later review pass."
            ""
            "## Extracted Row"
            ""
            (Format-TableRowAsMarkdown -Row $entry.row)
            ""
        ) -join "`n"

        $nodeLog.Add((Write-GraphNode -Entity "akteur_beteiligung" -Id $relationId -Title "$value - $title" -NodeKind "relation" -Fields @{
            fallstudie = "fallstudie/$caseId"
            projekt = $projectId
            bauobjekt = $bauobjektId
            akteur_candidate = $value
            beziehung = $relationship
            quelle_label = $quelle
            vertrauensgrad = $confidence
            legacy_path = $entry.source.legacy_path
        } -Body $relationBody))

        $actorRowsLog.Add([pscustomobject]@{
            fallstudie = $caseId
            relation = $relationId
            legacy_path = $entry.source.legacy_path
            akteur_candidate = $value
            beziehung = $relationship
            vertrauensgrad = $confidence
        })
    }

    if ($isReuseChain) {
        $chainId = $caseId
        $chainBody = @(
            "# Reuse-Kette - $title"
            ""
            "## Migration"
            ""
            "- Generated from fallstudie: fallstudie/$caseId"
            "- This node was created because the legacy content contains Reuse-Kette, donor/receiver wording, or an arrow transfer notation."
            ""
        ) -join "`n"
        $nodeLog.Add((Write-GraphNode -Entity "reuse_kette" -Id $chainId -Title "Reuse-Kette - $title" -NodeKind "core" -Fields @{
            fallstudie = "fallstudie/$caseId"
            projekt = $projectId
            legacy_paths = $legacyPaths
        } -Body $chainBody))

        foreach ($stationKind in @("Donor", "Receiver")) {
            $stationLines = New-Object System.Collections.Generic.List[string]
            foreach ($source in $sources) {
                foreach ($line in ($source.content -split "`r?`n")) {
                    if ($line -match $stationKind) { $stationLines.Add("$($source.legacy_path): $line") }
                }
            }
            $stationId = "$chainId`__$stationKind"
            $stationBody = @(
                "# $stationKind - $title"
                ""
                "## Migration"
                ""
                "- Generated from reuse_kette: reuse_kette/$chainId"
                "- Station type: $stationKind"
                ""
                "## Extracted Clues"
                ""
                if ($stationLines.Count -gt 0) { ($stationLines -join "`n") } else { "Keine explizite $stationKind-Zeile gefunden; Station wurde wegen erkannter Reuse-Kette als Strukturplatzhalter angelegt." }
                ""
            ) -join "`n"
            $nodeLog.Add((Write-GraphNode -Entity "reuse_kettenstation" -Id $stationId -Title "$stationKind - $title" -NodeKind "core" -Fields @{
                reuse_kette = "reuse_kette/$chainId"
                fallstudie = "fallstudie/$caseId"
                stationstyp = $stationKind
                legacy_paths = $legacyPaths
            } -Body $stationBody))
        }
    }
}

$sourceLog | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase4_case_graph_sources.csv"
$nodeLog | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase4_case_graph_nodes.csv"
$reuseRowsLog | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase4_reuse_einsatz_rows.csv"
$datenpunktRowsLog | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase4_datenpunkt_rows.csv"
$actorRowsLog | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase4_akteur_beteiligung_rows.csv"

$summary = @(
    "# Phase 4 Migration Manifest"
    ""
    "- Target root: $TargetRoot"
    "- Case legacy sources: $($sourceLog.Count)"
    "- Graph nodes generated: $($nodeLog.Count)"
    "- Reuse-einsatz rows extracted: $($reuseRowsLog.Count)"
    "- Datenpunkt rows extracted: $($datenpunktRowsLog.Count)"
    "- Akteur-beteiligung rows extracted: $($actorRowsLog.Count)"
    ""
    "This phase is non-destructive. Legacy case files were copied into fallstudie, projekt, and bauobjekt nodes; structured tables were converted into graph-ready child nodes."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase4_case_graph_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    case_sources = $sourceLog.Count
    nodes = $nodeLog.Count
    reuse_einsatz_rows = $reuseRowsLog.Count
    datenpunkt_rows = $datenpunktRowsLog.Count
    akteur_beteiligung_rows = $actorRowsLog.Count
}
