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
        [string]$Definition,
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
    $frontmatter.Add("migration_status: `"migrated_phase10_huerde_abgrenzung`"")
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
        "- Promoted from repeated phase-6 hurdle review labels."
        "- Use as a controlled knot; keep the original case wording on the edge as `raw_label`."
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

New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "huerde") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "bewertungslogik_abgrenzung") | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $TargetRoot "_system") | Out-Null

$nodes = @(
    @{
        entity="bewertungslogik_abgrenzung"; id="Kein_Direct_Reuse_Nachweis"; title="Kein Direct-Reuse-Nachweis";
        definition="Abgrenzung fuer Bauteile oder Angaben, bei denen keine belastbare Wiederverwendung belegt ist.";
        aliases=@("nicht Direct Reuse","kein Reuse-Beleg","keine Reuse-Belege","nicht als Reuse belegt","Reuse nicht gesichert","nicht wiederverwendet","not direct reuse")
    },
    @{
        entity="bewertungslogik_abgrenzung"; id="Bestandserhalt_Nicht_Direct_Reuse"; title="Bestandserhalt ist nicht automatisch Direct Reuse";
        definition="Abgrenzung fuer Bestandserhalt, Weiterbetrieb oder Retention, der nicht als transferierte Bauteilwiederverwendung gezaehlt wird.";
        aliases=@("Bestandserhalt nicht Reuse","Bestandserhalt darf nicht als Direct Reuse gezählt werden","zählt als Bestandserhalt, nicht Direct Reuse")
    },
    @{
        entity="bewertungslogik_abgrenzung"; id="Recycling_Nicht_Direct_Reuse"; title="Recycling ist nicht Direct Reuse";
        definition="Abgrenzung fuer Recycling, Reststoffnutzung oder stoffliche Verwertung, die keine direkte Bauteilwiederverwendung ist.";
        aliases=@("Recycling, nicht Direct Reuse","eher Recycling","Reststrom statt direct reuse","reuse/recycled")
    },
    @{
        entity="bewertungslogik_abgrenzung"; id="Moebel_Dekoration_Nicht_Direct_Reuse"; title="Moebel und Dekoration zaehlen nur bei fester baulicher Integration";
        definition="Abgrenzung fuer lose Moebel, Dekoration oder nicht fest eingebaute Ausstattung.";
        aliases=@("Möbel nicht zählen","Möbel/Dekoration","lose Möbel","nur fest eingebaute Elemente zählen")
    },
    @{
        entity="bewertungslogik_abgrenzung"; id="Ungebaut_Nicht_Realisierte_Wiederverwendung"; title="Ungebaut oder nicht realisiert";
        definition="Abgrenzung fuer geplante, spekulative oder nicht realisierte Wiederverwendung.";
        aliases=@("ungebaut","nicht geplant","Presseabsicht","nicht als gebaut verifiziert")
    },
    @{
        entity="bewertungslogik_abgrenzung"; id="Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung"; title="Design for Disassembly ist nicht automatisch aktuelle Wiederverwendung";
        definition="Abgrenzung fuer future DfD, Demontierbarkeit oder spaetere Austauschplanung ohne aktuell belegten Reuse-Einsatz.";
        aliases=@("DfD, nicht Direct Reuse","Future DfD, kein aktueller Direct Reuse","spätere Austauschplanung")
    },
    @{
        entity="bewertungslogik_abgrenzung"; id="Reuse_Anteil_Unklar"; title="Reuse-Anteil unklar";
        definition="Abgrenzung fuer Angaben, bei denen der wiederverwendete Anteil, Umfang oder die relevante Bauteilkategorie nicht klar ist.";
        aliases=@("Reuse-Anteil unklar","nicht nach Bauteilkategorien aufgeschlüsselt","Mengenkonflikt","nur teilweise belegt")
    },

    @{ entity="huerde"; id="Anschlussproblem"; title="Anschlussproblem"; definition="Probleme bei Anschluessen, Schnittstellen, Fugen, Integration oder Alt-Neu-Verbindungen."; aliases=@("Anschluss","Anschlussdetails","Schnittstelle Alt/Neu","technische Anschlüsse","Montage und Anschlüsse") },
    @{ entity="huerde"; id="Kompatibilitaetsproblem"; title="Kompatibilitaetsproblem"; definition="Probleme der Passung, Systemkompatibilitaet, Formate, Hoehen, Raster oder Schnittstellen zwischen gefundenen Bauteilen und neuem Entwurf."; aliases=@("Kompatibilität","Passung","Passgenauigkeit","Systemmix","Maße/Höhen","Format/Verfügbarkeit") },
    @{ entity="huerde"; id="Technische_Freigabe"; title="Technische Freigabe"; definition="Projektbezogene technische Freigabe, Zulassung oder bauaufsichtliche Akzeptanz als Huerde."; aliases=@("technische Freigabe","bauaufsichtliche Akzeptanz","technische Prüfung nicht öffentlich") },
    @{ entity="huerde"; id="Materialqualitaet_Unklar"; title="Materialqualitaet unklar"; definition="Unklare oder schwankende Materialqualitaet, Herkunft, Zusammensetzung oder Materialdetails."; aliases=@("Materialqualität","Herkunft/Materialdetails","Qualität/Herkunft","Zusammensetzung") },
    @{ entity="huerde"; id="Zustand_Unklar"; title="Zustand unklar"; definition="Unklarer Zustand, Alter, Restzustand, Glaszustand oder Verschleiss eines gebrauchten Bauteils."; aliases=@("Zustand","Glaszustand","Alter, Leistung, Dichtheit") },
    @{ entity="huerde"; id="Heterogenitaet_Chargen"; title="Heterogenitaet / Chargenvarianz"; definition="Heterogene Chargen, unterschiedliche Staerken, Masse, Zustaende oder fehlende Homogenitaet."; aliases=@("heterogene Chargen","heterogene Bauteile","Chargen-/Maßvarianz","Aufbereitung und Homogenität") },
    @{ entity="huerde"; id="Aufbereitungsaufwand"; title="Aufbereitungsaufwand"; definition="Zusaetzlicher Aufwand durch Reinigung, Zuschnitt, Bearbeitung, Refurbishment, Sortierung oder Rekonditionierung."; aliases=@("Aufbereitung","Zuschnitt","Bearbeitung","Sortierung","Refurbishment") },
    @{ entity="huerde"; id="Witterung_Feuchte"; title="Witterung / Feuchte"; definition="Probleme mit Witterung, Feuchte, Abdichtung, Waermebruecken oder bauphysikalischer Integration."; aliases=@("Witterung","Feuchteschutz","Innenfeuchte","Abdichtung","Wärmebrücken") },
    @{ entity="huerde"; id="Dauerhaftigkeit_Restlebensdauer"; title="Dauerhaftigkeit / Restlebensdauer"; definition="Unklare Dauerhaftigkeit, Restlebensdauer, Feuer-/Witterungsbestaendigkeit oder langfristige Robustheit."; aliases=@("Dauerhaftigkeit","Restlebensdauer","Feuer / Restlebensdauer") },
    @{ entity="huerde"; id="Hygieneanforderung"; title="Hygieneanforderung"; definition="Hygiene, Sauberkeit oder Nutzungssicherheit als Huerde fuer gebrauchte Bauteile."; aliases=@("Hygiene","Hygiene/Gewährleistung") },
    @{ entity="huerde"; id="Bauproduktstatus"; title="Bauproduktstatus"; definition="Huerde, wenn Material durch Nachweis, Dokumentation oder Konformitaet wieder als Bauprodukt verwendbar werden muss."; aliases=@("aus Material wird Bauprodukt","Bauprodukt","CE") },
    @{ entity="huerde"; id="Mengenunsicherheit"; title="Mengenunsicherheit"; definition="Unklare, widerspruechliche oder nicht passende Mengen fuer den Wiedereinsatz."; aliases=@("Menge","Mengen","Mengenkonflikt","passende Menge") },
    @{ entity="huerde"; id="Entwurfsbindung"; title="Entwurfsbindung durch vorhandene Bauteile"; definition="Gefundene Bauteile bestimmen Entwurf, Raster, Hoehen, Grundriss oder Lastannahmen."; aliases=@("Maße bestimmen Entwurf","Grundrissbindung","neue Lastannahmen","Dimensionen des Hausentwurfs") },
    @{ entity="huerde"; id="Akzeptanzproblem"; title="Akzeptanzproblem"; definition="Akzeptanz durch Bauherrschaft, Installateur, Ausfuehrende, Behoerden oder Markt als Huerde."; aliases=@("Akzeptanz Installateur","Akzeptanz","wollte reclaimed steel nicht") },
    @{ entity="huerde"; id="Bruch_Beschaedigungsrisiko"; title="Bruch- und Beschaedigungsrisiko"; definition="Risiko von Bruch, Beschaedigung oder Verlust beim Ausbau, Transport, Bearbeiten oder Leihen."; aliases=@("Bruchrisiko","ohne Beschädigung","Beschädigung") },
    @{ entity="huerde"; id="Unkonventionelles_Material"; title="Unkonventionelles Material"; definition="Experimentelle, ungewoehnliche oder nicht standardisierte Materialanwendungen als Huerde."; aliases=@("unkonventioneller Baustoff","ungewöhnliches Material","experimentelle Eignung","neues Materialexperiment") },
    @{ entity="huerde"; id="Performance_Nachweis"; title="Performance-Nachweis"; definition="Nachweis von Leistung, Dichtheit, Stabilitaet, Energie, Eignung oder Gebrauchstauglichkeit."; aliases=@("Performance","unbekannte Werte","Energieanforderungen","Stabilitätsaufwand","Dichtheit") }
)

$result = New-Object System.Collections.Generic.List[object]
foreach ($node in $nodes) {
    $result.Add((Write-KnotNode -Entity $node.entity -Id $node.id -Title $node.title -Definition $node.definition -Aliases $node.aliases)) | Out-Null
}

$result | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase10_huerde_abgrenzung_nodes.csv"

$summary = @(
    "# Phase 10 Huerde And Abgrenzung"
    ""
    "- Nodes created or confirmed: $($result.Count)"
    "- Created nodes: $(@($result | Where-Object { $_.status -eq 'created' }).Count)"
    "- CSV: _migration/phase10_huerde_abgrenzung_nodes.csv"
    ""
    "This phase splits methodological evaluation boundaries from true project hurdles."
    ""
) -join "`n"

[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase10_huerde_abgrenzung_manifest.md"), $summary, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    nodes = $result.Count
    created = @($result | Where-Object { $_.status -eq "created" }).Count
    already_exists = @($result | Where-Object { $_.status -eq "already_exists" }).Count
}
