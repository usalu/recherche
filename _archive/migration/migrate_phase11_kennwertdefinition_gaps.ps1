param(
    [string]$TargetRoot = "_graph"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Escape-YamlScalar {
    param([string]$Value)
    if ($null -eq $Value) { return '""' }
    $escaped = $Value.Replace('\', '\\').Replace('"', '\"')
    return '"' + $escaped + '"'
}

function Write-KennwertNode {
    param(
        [string]$Id,
        [string]$Title,
        [string]$Definition,
        [string[]]$Aliases = @()
    )

    $targetDir = Join-Path (Join-Path $TargetRoot "kennwertdefinition") $Id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"
    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    if (Test-Path -LiteralPath $targetIndex) {
        return [pscustomobject]@{
            id = $Id
            target = "kennwertdefinition/$Id"
            status = "already_exists"
        }
    }

    $frontmatter = New-Object System.Collections.Generic.List[string]
    $frontmatter.Add("---")
    $frontmatter.Add("id: $(Escape-YamlScalar $Id)")
    $frontmatter.Add("entity: `"kennwertdefinition`"")
    $frontmatter.Add("node_kind: `"knot`"")
    $frontmatter.Add("migration_status: `"migrated_phase11_kennwertdefinition_gap`"")
    $frontmatter.Add("title: $(Escape-YamlScalar $Title)")
    $frontmatter.Add("aliases:")
    foreach ($alias in $Aliases) {
        $frontmatter.Add("  - $(Escape-YamlScalar $alias)")
    }
    $frontmatter.Add("---")
    $frontmatter.Add("")

    $body = @(
        "# $Title"
        ""
        "## Definition"
        ""
        $Definition
        ""
        "## Migration"
        ""
        "- Promoted from recurring phase-6 metric review labels."
        "- Keep raw metric label on the edge for case-specific nuance."
        ""
    ) -join "`n"

    [System.IO.File]::WriteAllText($targetIndex, (($frontmatter -join "`n") + $body), $Utf8NoBom)

    return [pscustomobject]@{
        id = $Id
        target = "kennwertdefinition/$Id"
        status = "created"
    }
}

New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "kennwertdefinition") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null

$nodes = @(
    @{ id="Bauteilanzahl"; title="Bauteilanzahl"; definition="Anzahl von Bauteilen, Komponenten, Produkten oder Elementen."; aliases=@("Anzahl","Türen","Radiatoren","Leuchten","Sanitär","Fenster","Paneele","Platten","Betonblöcke") },
    @{ id="Abmessung"; title="Abmessung"; definition="Geometrische Groesse wie Laenge, Breite, Spannweite, Stich, Winkel oder Einzelabmessung."; aliases=@("Abmessung","Spannweite","Breite","Länge","Stich","Öffnungswinkel","HCS-Abmessung") },
    @{ id="Materialherkunft"; title="Materialherkunft"; definition="Anzahl oder Art von Herkunftsquellen, Donor Buildings, Materialquellen oder Harvesting-Kontexten."; aliases=@("Herkunftsquellen","Bauteilherkünfte","donor buildings","Donor-Umfang") },
    @{ id="Zertifizierung_Auszeichnung"; title="Zertifizierung / Auszeichnung"; definition="Projektbezogene Zertifizierung, Auszeichnung, Rating oder Award."; aliases=@("DGNB","EPC","Auszeichnung","Metropolis Next Generation Prize") },
    @{ id="Nutzungsumfang"; title="Nutzungsumfang"; definition="Nutzungsbezogene Mengen wie Wohneinheiten, Betten, Unterrichtsgruppen, Workspace oder geplante Nutzung."; aliases=@("Wohneinheiten","Betten","Unterrichtsgruppen","Workspace","geplante Nutzung") },
    @{ id="Primaermaterial_Einsparung"; title="Primaermaterial-Einsparung"; definition="Eingesparte Primaermaterialien, Ressourcen oder vermiedener Primaerressourceneinsatz."; aliases=@("Primärmaterial eingespart","Primärmaterial","Ressourcen eingespart") },
    @{ id="Wasserkennwert"; title="Wasserkennwert"; definition="Wasserbezogene Kennwerte wie Wassereinsparung, Regenwasserspeicher oder wasserbezogene Umweltwirkung."; aliases=@("Wassereinsparung","Regenwasserspeicher","Wasser") },
    @{ id="Recyclingquote"; title="Recyclingquote"; definition="Anteil von Recyclingmaterial, Upcycling/Recycling-Anteil oder Recyclingrate."; aliases=@("Recyclingrate","Upcycled/recycled Anteil","recycled materials","Anteil Altmaterial im Recyclingbeton") },
    @{ id="Energieerzeugung"; title="Energieerzeugung"; definition="Erzeugungsbezogene Energiewerte wie PV-Stromanteil oder Erdwärmesonden."; aliases=@("PV-Stromanteil","PV-Anlage","Erdwärmesonden") },
    @{ id="U_Wert"; title="U-Wert"; definition="Waermedurchgangskoeffizient von Bauteilen, Fenstern oder Huellenelementen."; aliases=@("U-Wert","U-Wert KRONE upcycled windows") },
    @{ id="Gebaeudemasse"; title="Gebaeudemasse"; definition="Erhaltene, gebundene oder bilanzierte Gebaeudemasse."; aliases=@("Gebäudemasse","erhaltene Gebäudemasse","gebundener CO₂-Anteil") },
    @{ id="Planungsaufwand"; title="Planungsaufwand"; definition="Planungszeit, Mehrhonorar, Zusatzaufwand oder sonstiger Aufwand zur Reuse-Integration."; aliases=@("Planungszeit","Mehrhonorar Planung","Zusatzaufwand","Sourcing/Prüfung") }
)

$result = New-Object System.Collections.Generic.List[object]
foreach ($node in $nodes) {
    $result.Add((Write-KennwertNode -Id $node.id -Title $node.title -Definition $node.definition -Aliases $node.aliases)) | Out-Null
}

$result | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase11_kennwertdefinition_gaps.csv"

$summary = @(
    "# Phase 11 Kennwertdefinition Gaps"
    ""
    "- Nodes created or confirmed: $($result.Count)"
    "- Created nodes: $(@($result | Where-Object { $_.status -eq 'created' }).Count)"
    "- CSV: _migration/phase11_kennwertdefinition_gaps.csv"
    ""
    "These metric families were promoted from recurring case-data labels."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase11_kennwertdefinition_gaps_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    nodes = $result.Count
    created = @($result | Where-Object { $_.status -eq "created" }).Count
    already_exists = @($result | Where-Object { $_.status -eq "already_exists" }).Count
}
