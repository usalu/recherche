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

function Write-RoleNode {
    param(
        [string]$Id,
        [string]$Title,
        [string]$Definition,
        [string[]]$Aliases = @()
    )

    $targetDir = Join-Path (Join-Path $TargetRoot "akteurrolle") $Id
    $filesDir = Join-Path $targetDir "DATEIEN"
    $targetIndex = Join-Path $targetDir "index.md"
    New-Item -ItemType Directory -Force -Path $filesDir | Out-Null

    if (Test-Path -LiteralPath $targetIndex) {
        return [pscustomobject]@{
            role_id = $Id
            target = "akteurrolle/$Id"
            status = "already_exists"
        }
    }

    $frontmatter = New-Object System.Collections.Generic.List[string]
    $frontmatter.Add("---")
    $frontmatter.Add("id: $(Escape-YamlScalar $Id)")
    $frontmatter.Add("entity: `"akteurrolle`"")
    $frontmatter.Add("node_kind: `"knot`"")
    $frontmatter.Add("migration_status: `"migrated_phase9_actor_role_knot`"")
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
        "- Promoted as a controlled actor role for `akteur_beteiligung` edges."
        ""
    ) -join "`n"

    [System.IO.File]::WriteAllText($targetIndex, (($frontmatter -join "`n") + $body), $Utf8NoBom)

    return [pscustomobject]@{
        role_id = $Id
        target = "akteurrolle/$Id"
        status = "created"
    }
}

New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "akteurrolle") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null

$roles = @(
    @{ id="Bauherr_Auftraggeber"; title="Bauherr / Auftraggeber"; definition="Akteur mit Auftraggeber-, Bauherrschafts-, Client-, Developer- oder Eigentuemerrolle im Projekt."; aliases=@("Bauherr","Auftraggeber","Client","Developer","Eigentuemer","Bauherrin","Nutzerin","Owner") },
    @{ id="Architektur"; title="Architektur"; definition="Akteur mit architektonischer Entwurfs-, Planungs- oder Designverantwortung."; aliases=@("Architekt","Architektur","Architekturbüro","Architektin","Architect","Design team","Entwurf") },
    @{ id="Tragwerksplanung"; title="Tragwerksplanung"; definition="Akteur mit Tragwerks-, Bauingenieur-, Statik- oder Structural-Engineering-Rolle."; aliases=@("Tragwerksplanung","Structural engineer","Bauingenieur","Civil engineer","Statik","Engineering") },
    @{ id="Bauausfuehrung"; title="Bauausfuehrung"; definition="Akteur mit Bauunternehmen-, Contractor-, Builder-, General-Contractor- oder Hauptauftragnehmerrolle."; aliases=@("Bauunternehmen","Contractor","main contractor","Builder","General Contractor","Hauptauftragnehmer","Bauausführung") },
    @{ id="Rueckbau_Demontage"; title="Rueckbau / Demontage"; definition="Akteur mit Rueckbau-, Demontage-, Abbruch- oder Donor-Harvesting-Rolle."; aliases=@("Rückbau","Demolition contractor","Rückbaupartner","Demontage","Donor deconstruction") },
    @{ id="Materiallieferant"; title="Materiallieferant"; definition="Akteur, der Reuse-Bauteile, Material, reclaimed stock oder Komponenten liefert."; aliases=@("Supplier","Stockholder","Materiallieferant","Reclaimed steel stockholder","Materiallieferant","Rückbauunternehmen / Materiallieferant") },
    @{ id="Reuse_Beratung"; title="Reuse-Beratung"; definition="Akteur mit Reuse-, Circular-Design-, Urban-Mining-, Bauteilwiederverwendungs- oder Materialstrategie-Rolle."; aliases=@("Reuse-Beratung","Reuse-Expertise","urban mining advice","Circular Design","Materialstrategie","AMO Reuse") },
    @{ id="Pruefung_Qualitaetssicherung"; title="Pruefung / Qualitaetssicherung"; definition="Akteur mit Test-, Zertifizierungs-, QA-, Zulassungs- oder technischer Kontrollrolle."; aliases=@("Prüfung","QA","Qualitätssicherung","technischer Kontrolleur","Zulassung","Testing") },
    @{ id="Aufbereitung_Refurbishment"; title="Aufbereitung / Refurbishment"; definition="Akteur, der Bauteile reinigt, prueft, repariert, refabriziert, redesigned oder montagefertig macht."; aliases=@("Aufbereitung","Refurbishment","Produkt-Redesign","Rekonditionierung","Joinery") },
    @{ id="Forschung_Dokumentation"; title="Forschung / Dokumentation"; definition="Akteur mit Forschungs-, Dokumentations-, Autorenschafts-, Hochschul- oder Monitoringrolle."; aliases=@("Forschung","Dokumentation","Autor:innen","Projektteam im Forschungskontext","University") },
    @{ id="Nachhaltigkeitsberatung"; title="Nachhaltigkeitsberatung"; definition="Akteur mit Nachhaltigkeits-, LCA-, Materialpass-, ESG- oder Circularity-Reporting-Rolle."; aliases=@("Nachhaltigkeitsberatung","Material passporting","LCA","Sustainability consultant","Materialpass") },
    @{ id="Projektmanagement_Koordination"; title="Projektmanagement / Koordination"; definition="Akteur mit Projektmanagement-, Koordinations-, Partner- oder Kollaborationsrolle."; aliases=@("Projektmanagement","Koordination","Projektpartner","Partner","Kollaborateur","Project manager") },
    @{ id="Landschaftsplanung"; title="Landschaftsplanung"; definition="Akteur mit Landschaftsarchitektur, Aussenraumplanung oder Freiraumrolle."; aliases=@("Landschaftsplanung","Landscape","VIA Landscape") },
    @{ id="TGA_Gebaeudetechnik"; title="TGA / Gebaeudetechnik"; definition="Akteur mit Gebäudetechnik-, TGA-, Energie-, Installations- oder Services-Planungsrolle."; aliases=@("TGA","Gebäudetechnik","Installationsberatung","Technik/Energie","Services") },
    @{ id="Brandschutz_Barrierefreiheit"; title="Brandschutz / Barrierefreiheit"; definition="Akteur mit Brandschutz-, Sicherheits-, Barrierefreiheits- oder Sicherheitskoordination-Rolle."; aliases=@("Brandschutz","Barrierefreiheit","Sicherheitskoordination") },
    @{ id="Stahlbau_Fertigung"; title="Stahlbau / Fertigung"; definition="Akteur mit Stahlbau-, Holzbau-, Fabricator-, Erector-, Konstrukteur- oder spezifischer Fertigungsrolle."; aliases=@("Stahlbau","Holzbauingenieur","fabricator","erector","Konstrukteur","steel structure designer") },
    @{ id="Fassade"; title="Fassade"; definition="Akteur mit Fassadenplanung, Fassadenbau oder Huelle-Rolle."; aliases=@("Fassade","Fassaden","facade") },
    @{ id="Kunst_Gestaltung"; title="Kunst / Gestaltung"; definition="Akteur mit Kunst-, Grafik-, Illustration-, Szenografie- oder Skatepark-Design-Rolle."; aliases=@("Künstler","Grafik","Illustration","Szenografie","Skatepark-Design") },
    @{ id="Betreiber_Nutzer"; title="Betreiber / Nutzer"; definition="Akteur mit Betreiber-, Nutzer-, Schultraeger-, sozialer Integrations- oder Nutzungskontextrolle."; aliases=@("Betreiber","Nutzer","Schulträger","soziale Integration","heutiger Betreiber") },
    @{ id="Oeffentliche_Hand"; title="Oeffentliche Hand"; definition="Kommunale, staatliche oder oeffentliche Projektrolle als Bauherr, Verwaltung, Amt oder Gemeinde."; aliases=@("Kommune","Ville","Municipality","Amt","öffentlicher Auftraggeber","Administration") },
    @{ id="Projektbeteiligte_Unbestimmt"; title="Projektbeteiligte, unbestimmt"; definition="Unspezifische Sammelrolle, wenn Quellen nur allgemeine Beteiligung, Projektteam oder Akteurskreis nennen."; aliases=@("Akteure","Beteiligte","Projektakteure","Projektteam","Mitwirkende","Quellenbezug") }
)

$result = New-Object System.Collections.Generic.List[object]
foreach ($role in $roles) {
    $result.Add((Write-RoleNode -Id $role.id -Title $role.title -Definition $role.definition -Aliases $role.aliases)) | Out-Null
}

$result | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase9_actor_roles.csv"

$summary = @(
    "# Phase 9 Actor Roles"
    ""
    "- Role knots created or confirmed: $($result.Count)"
    "- Created roles: $(@($result | Where-Object { $_.status -eq 'created' }).Count)"
    "- CSV: _migration/phase9_actor_roles.csv"
    ""
    "These knots normalize akteur_beteiligung.beziehung labels into graph roles."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase9_actor_roles_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    roles = $result.Count
    created = @($result | Where-Object { $_.status -eq "created" }).Count
    already_exists = @($result | Where-Object { $_.status -eq "already_exists" }).Count
}
