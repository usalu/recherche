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

function Write-BauteiltypNode {
    param(
        [string]$Id,
        [string]$Title,
        [string]$Definition,
        [string[]]$Aliases = @()
    )

    $targetDir = Join-Path (Join-Path $TargetRoot "bauteiltyp") $Id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"
    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    if (Test-Path -LiteralPath $targetIndex) {
        return [pscustomobject]@{
            id = $Id
            target = "bauteiltyp/$Id"
            status = "already_exists"
        }
    }

    $frontmatter = New-Object System.Collections.Generic.List[string]
    $frontmatter.Add("---")
    $frontmatter.Add("id: $(Escape-YamlScalar $Id)")
    $frontmatter.Add("entity: `"bauteiltyp`"")
    $frontmatter.Add("node_kind: `"knot`"")
    $frontmatter.Add("migration_status: `"migrated_phase12_bauteiltyp_gap`"")
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
        "- Promoted from recurring phase-6 component-type review labels."
        "- Keep raw component wording on the edge for case-specific detail."
        ""
    ) -join "`n"

    [System.IO.File]::WriteAllText($targetIndex, (($frontmatter -join "`n") + $body), $Utf8NoBom)

    return [pscustomobject]@{
        id = $Id
        target = "bauteiltyp/$Id"
        status = "created"
    }
}

New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "bauteiltyp") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null

$nodes = @(
    @{ id="Platte_Paneel"; title="Platte / Paneel"; definition="Platten-, Paneel- oder Sheet-Elemente, wenn keine spezifischere Bauteilart sicher ist."; aliases=@("Paneel","Platte","Messebauplatten","Filzpaneele","Faserzementplatten","Sperrholz / ply sheets") },
    @{ id="Ziegel"; title="Ziegel"; definition="Ziegel, Backstein, Klinker oder Brick-Elemente als wiederverwendeter Bauteiltyp."; aliases=@("Ziegel","Fassadenziegel","Abbruchziegel","BTC-Ziegel","bricks") },
    @{ id="Mauerstein_Block"; title="Mauerstein / Block"; definition="Mauersteine, Bau- oder Blockelemente, wenn sie keine spezifische Betonblock- oder Ziegelklassifikation haben."; aliases=@("Hanfkalkstein","Hanf-Kalk-Block","Lehmstein","Mauerstein","Blockelement") },
    @{ id="Dachziegel"; title="Dachziegel"; definition="Dachziegel oder roof tiles als eigene Bauteilgruppe."; aliases=@("Dachziegel","Roof tiles") },
    @{ id="Pflaster_Bodenplatte"; title="Pflaster / Bodenplatte"; definition="Pflasterplatten, Flagstones, paving slabs, Aussenbodenplatten oder aehnliche feste Bodenplatten."; aliases=@("Pflaster","Strassenpflasterplatten","Blaustein-Flagstones","Granitpflaster","Pflaster / Bodenplatten aussen") },
    @{ id="Bodenbelag"; title="Bodenbelag"; definition="Bodenbelag, Parkett, Dielen, Terrassen- oder Bodenaufbauten, wenn nicht als Fliese klassifiziert."; aliases=@("Bodenbelag","Eichenparkett","Azobe-Dielen","Bodenaufbau","Terrassendielen") },
    @{ id="Akustikelement"; title="Akustikelement"; definition="Akustikpaneele, Baffles, Flaechen oder absorbierende Bauteile."; aliases=@("Akustikpaneele","Akustik-Baffles","Akustikflaechen") },
    @{ id="Innenausbau_Element"; title="Innenausbau-Element"; definition="Wiederverwendete Innenausbau-, Ausstattungs- oder Oberflaechenelemente, wenn fest eingebaut."; aliases=@("Innenausbau","Innenoberflaechen","wiederverwendete Innenausbau-Elemente","feste Innenausbauten") },
    @{ id="Kueche"; title="Kueche / Kuechenelement"; definition="Kuechen, Kuechenbloecke, Kuechenunits oder Arbeitsplatten als feste Einbauten."; aliases=@("Kueche","Kuechenbloecke","Kuechenunit","Arbeitsplatte") },
    @{ id="Bruestung"; title="Bruestung"; definition="Bruestungen, Balustraden, Parapets oder Handrails als bauliche Sicherungs-/Randelemente."; aliases=@("Bruestung","Balustraden","parapets","Handrails") },
    @{ id="Gitterrost"; title="Gitterrost"; definition="Gitterroste, Stahlroste oder vergleichbare begehbare Rostelemente."; aliases=@("Gitterrost","Gitterroste","Stahlroste") },
    @{ id="Beschattung_Sonnenschutz"; title="Beschattung / Sonnenschutz"; definition="Sonnenschutz, Awnings, Screens, Beschattungskonstruktionen oder Fassadenscreens."; aliases=@("Sonnenschutz","Beschattung","awnings","Screen") },
    @{ id="Vordach_Ueberdachung"; title="Vordach / Ueberdachung"; definition="Vordaecher, Pergolen, Atriumhuellen, Ueberdachungen oder Dachrand-Ueberdeckungen."; aliases=@("Vordach","Pergola","Ueberdachung","Atriumhuelle") },
    @{ id="Fundament_Bodenplatte"; title="Fundament / Bodenplatte"; definition="Fundamente, Bodenplatten, erste Geschosse oder grundungsnahe massive Bauteile."; aliases=@("Fundament","Bodenplatte","Fundamente / erste Geschosse") },
    @{ id="Auflager_Widerlager"; title="Auflager / Widerlager"; definition="Auflager, Widerlager, Plattenauflager oder tragende Lagerpunkte."; aliases=@("Auflager","Widerlager","Plattenauflager") },
    @{ id="Blechpaneel"; title="Blechpaneel"; definition="Blech-, Wellblech-, Trapezblech- oder Metallpaneel-Elemente."; aliases=@("Wellblech","Trapezblech","Dachbleche","Blech aus Boeden","Metall-Deckenpaneele") },
    @{ id="Schacht"; title="Schacht"; definition="Technische Schaechte, Installationsschaechte oder vertikale Service-Zonen."; aliases=@("Schacht","technische Schaechte") },
    @{ id="Landschaftselement"; title="Landschafts- / Aussenraumelement"; definition="Aussenraum-, Park-, Pflanz- oder Landschaftselemente, wenn als baulicher Reuse-Einsatz gefuehrt."; aliases=@("Park / Aussenraum","Pflanztroege","Landscape elements") },
    @{ id="Bauwerksteil"; title="Bauwerksteil"; definition="Ganze Gebaeudeteile, Pavillons, Bestandsgebaeude oder Hauptstrukturen, wenn eine feinere Bauteilklasse nicht passt."; aliases=@("Bestandsgebaeude","Pavillonensemble","Hauptstruktur","Rohbau","Kreuzgang") }
)

$result = New-Object System.Collections.Generic.List[object]
foreach ($node in $nodes) {
    $result.Add((Write-BauteiltypNode -Id $node.id -Title $node.title -Definition $node.definition -Aliases $node.aliases)) | Out-Null
}

$result | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase12_bauteiltyp_gaps.csv"

$summary = @(
    "# Phase 12 Bauteiltyp Gaps"
    ""
    "- Nodes created or confirmed: $($result.Count)"
    "- Created nodes: $(@($result | Where-Object { $_.status -eq 'created' }).Count)"
    "- CSV: _migration/phase12_bauteiltyp_gaps.csv"
    ""
    "These component families were promoted from recurring case inventory labels."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase12_bauteiltyp_gaps_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    nodes = $result.Count
    created = @($result | Where-Object { $_.status -eq "created" }).Count
    already_exists = @($result | Where-Object { $_.status -eq "already_exists" }).Count
}
