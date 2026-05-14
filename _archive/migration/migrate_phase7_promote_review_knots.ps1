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

function Write-KnotNode {
    param(
        [string]$Entity,
        [string]$Id,
        [string]$Title,
        [string]$Reason,
        [string[]]$Aliases = @()
    )
    $targetDir = Join-Path (Join-Path $TargetRoot $Entity) $Id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"
    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    if (Test-Path -LiteralPath $targetIndex) {
        return [pscustomobject]@{
            entity = $Entity
            id = $Id
            target = "$Entity/$Id"
            status = "already_exists"
        }
    }

    $frontmatter = New-Object System.Collections.Generic.List[string]
    $frontmatter.Add("---")
    $frontmatter.Add("id: $(Escape-YamlScalar $Id)")
    $frontmatter.Add("entity: $(Escape-YamlScalar $Entity)")
    $frontmatter.Add("node_kind: `"knot`"")
    $frontmatter.Add("migration_status: `"migrated_phase7_promoted_review_knot`"")
    $frontmatter.Add("title: $(Escape-YamlScalar $Title)")
    $frontmatter.Add("promotion_reason: $(Escape-YamlScalar $Reason)")
    if ($Aliases.Count -gt 0) {
        $frontmatter.Add("aliases:")
        foreach ($alias in $Aliases) {
            $frontmatter.Add("  - $(Escape-YamlScalar $alias)")
        }
    }
    $frontmatter.Add("---")
    $frontmatter.Add("")

    $body = @(
        "# $Title"
        ""
        "## Migration"
        ""
        "- Promoted from repeated phase-6 label-resolution gaps."
        "- Reason: $Reason"
        "- Review before using for final analysis if a narrower domain-specific node is needed."
        ""
    ) -join "`n"

    [System.IO.File]::WriteAllText($targetIndex, (($frontmatter -join "`n") + $body), $Utf8NoBom)

    return [pscustomobject]@{
        entity = $Entity
        id = $Id
        target = "$Entity/$Id"
        status = "created"
    }
}

$knots = @(
    @{ entity="bauteiltyp"; id="Tuer"; title="Tuer"; reason="Recurring generic door labels should not be forced into Feuerschutztuer."; aliases=@("Tuer","Tuer/en","Door","Tueren") },
    @{ entity="bauteiltyp"; id="TGA_Element"; title="TGA-Element"; reason="Recurring fixed building-services components need a neutral component type."; aliases=@("TGA","Technische Gebaeudeausruestung","Building services") },
    @{ entity="bauteiltyp"; id="Daemmung"; title="Daemmung"; reason="Recurring insulation elements appear across reuse inventories."; aliases=@("Daemmung","Innendaemmung","Insulation") },
    @{ entity="bauteiltyp"; id="Dach"; title="Dach"; reason="Recurring roof labels are not always structural Dachtragwerk."; aliases=@("Dach","Roof") },
    @{ entity="bauteiltyp"; id="Innenwand"; title="Innenwand"; reason="Recurring non-loadbearing interior wall labels should be separate from generic Wand."; aliases=@("Innenwand","Innenwaende","Interior wall") },
    @{ entity="bauteiltyp"; id="Gelaender"; title="Gelaender"; reason="Recurring railing and balustrade labels."; aliases=@("Gelaender","Bruestungsgelaender","Railing") },
    @{ entity="bauteiltyp"; id="Heizkoerper"; title="Heizkoerper"; reason="Recurring radiator/heating component labels."; aliases=@("Heizkoerper","Radiator","Radiatoren") },
    @{ entity="bauteiltyp"; id="Moebel"; title="Moebel"; reason="Furniture appears repeatedly; keep as component type but review scoring relevance."; aliases=@("Moebel","Furniture") },
    @{ entity="bauteiltyp"; id="Festes_Einbauteil"; title="Festes Einbauteil"; reason="Recurring built-in fixtures are relevant when permanently installed."; aliases=@("feste Einbauten","Built-in fixture") },
    @{ entity="bauteiltyp"; id="Fliese"; title="Fliese"; reason="Recurring tile/fayence labels."; aliases=@("Fliese","Fliesen","Fayence","Tile") },
    @{ entity="bauteiltyp"; id="Bodenfliese"; title="Bodenfliese"; reason="Recurring floor tile labels deserve a narrower child knot."; aliases=@("Bodenfliese","Bodenfliesen","Floor tile") },
    @{ entity="bauteiltyp"; id="Betonblock"; title="Betonblock"; reason="Recurring concrete block labels are not the same as Betonfertigteil."; aliases=@("Betonblock","Betonbloecke","Concrete block") },
    @{ entity="bauteiltyp"; id="Tragstruktur"; title="Tragstruktur"; reason="Some cases name a structural assembly without a precise component."; aliases=@("Tragstruktur","Tragwerk","Primary structure") },
    @{ entity="bauteiltyp"; id="PV_Anlage"; title="PV-Anlage"; reason="PV systems appear as fixed technical components."; aliases=@("PV-Anlage","Photovoltaik") },

    @{ entity="material"; id="Metall"; title="Metall"; reason="Recurring unknown-metal labels should not be forced to Stahl."; aliases=@("Metall","Metal") },
    @{ entity="material"; id="Aluminium"; title="Aluminium"; reason="Recurring aluminium labels."; aliases=@("Aluminium","Aluminum") },
    @{ entity="material"; id="Naturstein"; title="Naturstein"; reason="Recurring natural stone labels, including stone/marble/granite families."; aliases=@("Naturstein","Stein","Stone") },
    @{ entity="material"; id="Granit"; title="Granit"; reason="Recurring granite labels."; aliases=@("Granit","Granite") },
    @{ entity="material"; id="Marmor"; title="Marmor"; reason="Marble labels appear in reuse inventories."; aliases=@("Marmor","Marble") },
    @{ entity="material"; id="Kunststoff"; title="Kunststoff"; reason="Recurring plastic labels."; aliases=@("Kunststoff","Plastic") },
    @{ entity="material"; id="Mineralwolle"; title="Mineralwolle"; reason="Recurring mineral wool insulation labels."; aliases=@("Mineralwolle","Steinwolle","Mineral wool") },
    @{ entity="material"; id="Daemmstoff"; title="Daemmstoff"; reason="Generic insulation-material labels should not be lost."; aliases=@("Daemmstoff","Daemmmaterial","Insulation material") },
    @{ entity="material"; id="Textil"; title="Textil"; reason="Recurring textile labels."; aliases=@("Textil","Textile") },
    @{ entity="material"; id="Faserzement"; title="Faserzement"; reason="Fibre cement appears as a material label."; aliases=@("Faserzement","Fibre cement") },
    @{ entity="material"; id="Polystyrol"; title="Polystyrol"; reason="Recurring EPS/polystyrene material labels."; aliases=@("Polystyrol","EPS") },
    @{ entity="material"; id="Guss"; title="Guss"; reason="Cast metal/cast iron labels need a material placeholder."; aliases=@("Guss","Gusseisen","Cast iron") },
    @{ entity="material"; id="Erde"; title="Erde"; reason="Earth/pressed earth appears in circular construction material labels."; aliases=@("Erde","gepresste Erde","Earth") },

    @{ entity="kennwertdefinition"; id="Flaeche"; title="Flaeche"; reason="Most frequent unmatched metric label."; aliases=@("Flaeche","Projektflaeche","Gebaeudeflaeche","Gesamtflaeche","Nutzflaeche","BGF","GIA") },
    @{ entity="kennwertdefinition"; id="Bauzeit"; title="Bauzeit"; reason="Recurring project-time metric."; aliases=@("Bauzeit","Projektzeitraum","Zeitraum") },
    @{ entity="kennwertdefinition"; id="Fertigstellung"; title="Fertigstellung"; reason="Recurring completion/opening metric."; aliases=@("Fertigstellung","Eroeffnung","Projektjahr","Jahr") },
    @{ entity="kennwertdefinition"; id="Baukosten"; title="Baukosten"; reason="Recurring cost metric."; aliases=@("Baukosten","Kosten","Kosten/m2") },
    @{ entity="kennwertdefinition"; id="Transportdistanz"; title="Transportdistanz"; reason="Recurring logistics-distance metric."; aliases=@("Transportdistanz","Distanz Spender-Empfaenger","Donor-Receiver distance") },
    @{ entity="kennwertdefinition"; id="Lebensdauer"; title="Lebensdauer"; reason="Recurring lifetime metric."; aliases=@("Lebensdauer","geplante Lebensdauer") },
    @{ entity="kennwertdefinition"; id="Kostenwirkung"; title="Kostenwirkung"; reason="Recurring qualitative or comparative cost-impact metric."; aliases=@("Kostenwirkung","Kostenreduktion") },
    @{ entity="kennwertdefinition"; id="Abfallvermeidung"; title="Abfallvermeidung"; reason="Recurring waste-avoidance metric."; aliases=@("Abfallvermeidung","Abfall vermieden","Waste avoided") },
    @{ entity="kennwertdefinition"; id="Bauteilalter"; title="Bauteilalter"; reason="Recurring age-of-component metric."; aliases=@("Bauteilalter","Alter") },
    @{ entity="kennwertdefinition"; id="Hoehe"; title="Hoehe"; reason="Recurring object-height metric."; aliases=@("Hoehe","Height") },
    @{ entity="kennwertdefinition"; id="Geschosse"; title="Geschosse"; reason="Recurring storey-count metric."; aliases=@("Geschosse","Storeys") },
    @{ entity="kennwertdefinition"; id="Energiebedarf"; title="Energiebedarf"; reason="Recurring energy metric."; aliases=@("Energie","Energiebedarf") },
    @{ entity="kennwertdefinition"; id="Arbeitsplaetze"; title="Arbeitsplaetze"; reason="Recurring workplace-count metric."; aliases=@("Arbeitsplaetze","Workplaces") },
    @{ entity="kennwertdefinition"; id="Materialmenge"; title="Materialmenge"; reason="Recurring quantity of reused component/material metric."; aliases=@("wiederverwendeter Stahl","wiederverwendete Masse","Betonvolumen","Tonnen") },

    @{ entity="norm"; id="EN_1090"; title="EN 1090"; reason="Recurring steel execution / CE marking reference in structural steel reuse cases."; aliases=@("EN 1090","CE marking steel") }
)

$created = New-Object System.Collections.Generic.List[object]
foreach ($knot in $knots) {
    $created.Add((Write-KnotNode -Entity $knot.entity -Id $knot.id -Title $knot.title -Reason $knot.reason -Aliases $knot.aliases)) | Out-Null
}

$created | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase7_promoted_review_knots.csv"

$summary = @(
    "# Phase 7 Promoted Review Knots"
    ""
    "- Created or confirmed knots: $($created.Count)"
    "- CSV: _migration/phase7_promoted_review_knots.csv"
    ""
    "These are controlled knots promoted from repeated phase-6 review gaps. They are conservative vocabulary additions, not extracted case facts."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase7_promoted_review_knots_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    promoted = $created.Count
    created = @($created | Where-Object { $_.status -eq "created" }).Count
    already_exists = @($created | Where-Object { $_.status -eq "already_exists" }).Count
}
