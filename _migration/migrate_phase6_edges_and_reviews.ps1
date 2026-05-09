param(
    [string]$TargetRoot = "_graph"
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function Normalize-Key {
    param([string]$Value)
    if ($null -eq $Value) { return "" }
    $s = $Value.ToLowerInvariant()
    $s = $s.Replace(([string][char]0x00E4), 'ae')
    $s = $s.Replace(([string][char]0x00F6), 'oe')
    $s = $s.Replace(([string][char]0x00FC), 'ue')
    $s = $s.Replace(([string][char]0x00DF), 'ss')
    $s = $s -replace '[^a-z0-9]+', '_'
    return $s.Trim('_')
}

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
    $lines = [System.IO.File]::ReadAllLines($Path, $Utf8NoBom)
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

function Get-FmFirst {
    param([hashtable]$Frontmatter, [string]$Key)
    if (-not $Frontmatter.ContainsKey($Key)) { return "" }
    $value = $Frontmatter[$Key]
    if ($value -is [System.Collections.IList]) {
        if ($value.Count -gt 0) { return [string]$value[0] }
        return ""
    }
    return [string]$value
}

function Get-FmList {
    param([hashtable]$Frontmatter, [string]$Key)
    if (-not $Frontmatter.ContainsKey($Key)) { return @() }
    $value = $Frontmatter[$Key]
    if ($value -is [System.Collections.IList]) { return @($value) }
    if ([string]::IsNullOrWhiteSpace([string]$value)) { return @() }
    return @([string]$value)
}

function Is-IgnorableLabel {
    param([string]$Label)
    if ([string]::IsNullOrWhiteSpace($Label)) { return $true }
    $k = Normalize-Key -Value $Label
    if ([string]::IsNullOrWhiteSpace($k)) { return $true }
    if ($k -match '^(unbekannt|unklar|keine|kein|nicht_belegt|nicht_gesichert|n_a|na|none|offen|diverse|verschiedene|gemischt)$') { return $true }
    return $false
}

function Split-LabelPieces {
    param([string]$Label)
    if ([string]::IsNullOrWhiteSpace($Label)) { return @() }
    $clean = $Label -replace '\bu\.?\s*a\.?\b', ''
    $clean = $clean -replace '\bvermutlich\b', ''
    $clean = $clean -replace '\bgenaue Art unbekannt\b', ''
    $clean = $clean -replace '\bSpezifikation unbekannt\b', ''
    $parts = @($clean -split '\s*(;|,|\+|/|\bund\b|\bmit\b|\bteilweise\b)\s*' |
        Where-Object { $_ -notmatch '^(;|,|\+|/|und|mit|teilweise)$' } |
        ForEach-Object { $_.Trim() } |
        Where-Object { -not (Is-IgnorableLabel -Label $_) })
    return @($parts | Sort-Object -Unique)
}

function New-Resolution {
    param([string]$Target, [string]$Confidence, [string]$Rule)
    return [pscustomobject]@{
        target = $Target
        confidence = $Confidence
        rule = $Rule
    }
}

function Add-Edge {
    param(
        [System.Collections.Generic.List[object]]$Edges,
        [string]$Source,
        [string]$Relation,
        [string]$Target,
        [string]$Field = "",
        [string]$RawLabel = "",
        [string]$Confidence = "structural",
        [string]$Rule = "",
        [string]$LegacyPath = ""
    )
    if ([string]::IsNullOrWhiteSpace($Source) -or [string]::IsNullOrWhiteSpace($Target)) { return }
    $sourceParts = $Source -split '/', 2
    $targetParts = $Target -split '/', 2
    if ($sourceParts.Count -ne 2 -or $targetParts.Count -ne 2) { return }
    $Edges.Add([pscustomobject]@{
        source = $Source
        source_entity = $sourceParts[0]
        source_id = $sourceParts[1]
        relation = $Relation
        target = $Target
        target_entity = $targetParts[0]
        target_id = $targetParts[1]
        field = $Field
        raw_label = $RawLabel
        confidence = $Confidence
        resolution_rule = $Rule
        legacy_path = $LegacyPath
    })
}

function Add-Review {
    param(
        [System.Collections.Generic.List[object]]$Reviews,
        [string]$Source,
        [string]$Field,
        [string]$RawLabel,
        [string]$SuggestedEntity,
        [string]$Reason,
        [string]$LegacyPath = ""
    )
    if (Is-IgnorableLabel -Label $RawLabel) { return }
    $parts = $Source -split '/', 2
    $Reviews.Add([pscustomobject]@{
        source = $Source
        source_entity = if ($parts.Count -eq 2) { $parts[0] } else { "" }
        source_id = if ($parts.Count -eq 2) { $parts[1] } else { "" }
        field = $Field
        raw_label = $RawLabel
        suggested_entity = $SuggestedEntity
        reason = $Reason
        legacy_path = $LegacyPath
    })
}

function Build-NodeLookup {
    param([string[]]$Entities)
    $lookup = @{}
    foreach ($entity in $Entities) {
        $lookup[$entity] = @{}
        $entityDir = Join-Path $TargetRoot $entity
        if (-not (Test-Path -LiteralPath $entityDir)) { continue }
        foreach ($dir in (Get-ChildItem -LiteralPath $entityDir -Directory)) {
            $id = $dir.Name
            $lookup[$entity][(Normalize-Key -Value $id)] = $id
            $index = Join-Path $dir.FullName "index.md"
            if (Test-Path -LiteralPath $index) {
                $fm = Read-Frontmatter -Path $index
                $title = Get-FmFirst -Frontmatter $fm -Key "title"
                if (-not [string]::IsNullOrWhiteSpace($title)) {
                    $lookup[$entity][(Normalize-Key -Value $title)] = $id
                }
                foreach ($alias in (Get-FmList -Frontmatter $fm -Key "aliases")) {
                    if (-not [string]::IsNullOrWhiteSpace($alias)) {
                        $lookup[$entity][(Normalize-Key -Value $alias)] = $id
                    }
                }
            }
        }
    }
    return $lookup
}

function Resolve-Exact {
    param([hashtable]$Lookup, [string]$Entity, [string]$Label)
    $key = Normalize-Key -Value $Label
    if ($Lookup.ContainsKey($Entity) -and $Lookup[$Entity].ContainsKey($key)) {
        return @(New-Resolution -Target "$Entity/$($Lookup[$Entity][$key])" -Confidence "exact" -Rule "exact_id_or_title")
    }
    return @()
}

function Resolve-Material {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    foreach ($piece in (Split-LabelPieces -Label $Label)) {
        $k = Normalize-Key -Value $piece
        if ($k -match 'sekundaer_stahl|reclaimed_steel|reused_steel') { $out.Add((New-Resolution "material/Sekundaerstahl" "rule_high" "material_secondary_steel")) | Out-Null; continue }
        if ($k -match 'stahlbeton|spannbeton|fertigbeton') {
            $out.Add((New-Resolution "material/Beton" "rule_medium" "material_reinforced_concrete_contains_beton")) | Out-Null
            $out.Add((New-Resolution "material/Stahl" "rule_low" "material_reinforced_concrete_contains_stahl")) | Out-Null
            continue
        }
        if ($k -match 'betonfertig') { $out.Add((New-Resolution "material/Beton_Fertigteile" "rule_high" "material_betonfertigteil")) | Out-Null; continue }
        if ($k -match 'baustahl|stahlblech|stahlrohr|stahlfenster|^stahl$|_stahl|stahl_') { $out.Add((New-Resolution "material/Stahl" "rule_high" "material_contains_stahl")) | Out-Null; continue }
        if ($k -match 'brettschichtholz|glulam') { $out.Add((New-Resolution "material/Brettschichtholz" "rule_high" "material_brettschichtholz")) | Out-Null; continue }
        if ($k -match 'brettsperrholz|cross_laminated_timber|clt') { $out.Add((New-Resolution "material/Brettsperrholz" "rule_high" "material_brettsperrholz")) | Out-Null; continue }
        if ($k -match 'holzwerkstoff|mdf|holz') { $out.Add((New-Resolution "material/Holz" "rule_high" "material_contains_holz")) | Out-Null; continue }
        if ($k -match 'glas') { $out.Add((New-Resolution "material/Glas" "rule_high" "material_contains_glas")) | Out-Null; continue }
        if ($k -match 'sanitaerkeramik') { $out.Add((New-Resolution "material/Sanitarkeramik" "rule_high" "material_sanitaerkeramik")) | Out-Null; continue }
        if ($k -match 'keramik|fliese|ziegel|klinker') { $out.Add((New-Resolution "material/Keramik" "rule_medium" "material_ceramic_family")) | Out-Null; continue }
        if ($k -match 'recyclingbeton') { $out.Add((New-Resolution "material/Recyclingbeton" "rule_high" "material_recyclingbeton")) | Out-Null; continue }
        if ($k -match 'beton') { $out.Add((New-Resolution "material/Beton" "rule_high" "material_contains_beton")) | Out-Null; continue }
        if ($k -match '^metall$|^metal$') { $out.Add((New-Resolution "material/Metall" "rule_high" "material_generic_metall")) | Out-Null; continue }
        if ($k -match 'aluminium|aluminum') { $out.Add((New-Resolution "material/Aluminium" "rule_high" "material_aluminium")) | Out-Null; continue }
        if ($k -match 'granit|granite') { $out.Add((New-Resolution "material/Granit" "rule_high" "material_granit")) | Out-Null; continue }
        if ($k -match 'marmor|marble') { $out.Add((New-Resolution "material/Marmor" "rule_high" "material_marmor")) | Out-Null; continue }
        if ($k -match 'naturstein|blaustein|stein$|^stein|stone') { $out.Add((New-Resolution "material/Naturstein" "rule_medium" "material_naturstein_family")) | Out-Null; continue }
        if ($k -match 'kunststoff|plastic|pet') { $out.Add((New-Resolution "material/Kunststoff" "rule_high" "material_kunststoff")) | Out-Null; continue }
        if ($k -match 'mineralwolle|steinwolle') { $out.Add((New-Resolution "material/Mineralwolle" "rule_high" "material_mineralwolle")) | Out-Null; continue }
        if ($k -match 'daemmstoff|daemmmaterial|d_mmstoff|d_mmmaterial') { $out.Add((New-Resolution "material/Daemmstoff" "rule_high" "material_daemmstoff")) | Out-Null; continue }
        if ($k -match 'polystyrol|eps') { $out.Add((New-Resolution "material/Polystyrol" "rule_high" "material_polystyrol")) | Out-Null; continue }
        if ($k -match 'textil|textile') { $out.Add((New-Resolution "material/Textil" "rule_high" "material_textil")) | Out-Null; continue }
        if ($k -match 'faserzement') { $out.Add((New-Resolution "material/Faserzement" "rule_high" "material_faserzement")) | Out-Null; continue }
        if ($k -match 'gusseisen|guss|cast_iron') { $out.Add((New-Resolution "material/Guss" "rule_medium" "material_guss")) | Out-Null; continue }
        if ($k -match '^erde$|gepresste_erde|earth') { $out.Add((New-Resolution "material/Erde" "rule_medium" "material_erde")) | Out-Null; continue }
        if ($k -match 'lehm') { $out.Add((New-Resolution "material/Lehm" "rule_high" "material_contains_lehm")) | Out-Null; continue }
        if ($k -match 'stroh') { $out.Add((New-Resolution "material/Stroh" "rule_high" "material_contains_stroh")) | Out-Null; continue }
        if ($k -match 'composite|verbund') { $out.Add((New-Resolution "material/Composite" "rule_medium" "material_composite")) | Out-Null; continue }
    }
    return @($out | Sort-Object target -Unique)
}

function Resolve-Bauteiltyp {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    $k = Normalize-Key -Value $Label
    if ($k -match 'betonfertig|fertigbeton|fertigteil|precast_concrete|plattenbauteil|prefabriqu|prefabricated|betonunit|betonunits|sichtbetonteile|betonteile|wbs70|p2') { $out.Add((New-Resolution "bauteiltyp/Betonfertigteil" "rule_high" "bauteil_concrete_prefab")) | Out-Null }
    if ($k -match 'fenster') { $out.Add((New-Resolution "bauteiltyp/Fenster" "rule_high" "bauteil_contains_fenster")) | Out-Null }
    if ($k -match 'feuerschutztuer|brandschutztuer') { $out.Add((New-Resolution "bauteiltyp/Feuerschutztuer" "rule_high" "bauteil_fire_door")) | Out-Null }
    elseif ($k -match 'tuer|tueren|door|doors|(^|_)t_ren($|_)|^t_r$|^t_re$|bauernhaustuer') { $out.Add((New-Resolution "bauteiltyp/Tuer" "rule_high" "bauteil_tuer")) | Out-Null }
    if ($k -match 'tga|technik|technische_komponenten|technical_components|aufzug|lift|aufzugsmotor|pv_anlage|photovoltaik|solarzell|elektrotechnische|elektroinstallation|major_plant|kabeltrasse|waermepumpe|lueftung|duct|pipe|rohr|kanal') {
        if ($k -match 'pv_anlage|photovoltaik|solarzell') { $out.Add((New-Resolution "bauteiltyp/PV_Anlage" "rule_high" "bauteil_pv")) | Out-Null }
        else { $out.Add((New-Resolution "bauteiltyp/TGA_Element" "rule_medium" "bauteil_tga")) | Out-Null }
    }
    if ($k -match 'daemmung|d_mmung|innendaemmung|insulation') { $out.Add((New-Resolution "bauteiltyp/Daemmung" "rule_high" "bauteil_daemmung")) | Out-Null }
    if ($k -match 'akustik|baffle|troldtekt') { $out.Add((New-Resolution "bauteiltyp/Akustikelement" "rule_high" "bauteil_akustik")) | Out-Null }
    if ($k -match 'dachziegel|roof_tile|roof_tiles') { $out.Add((New-Resolution "bauteiltyp/Dachziegel" "rule_high" "bauteil_dachziegel")) | Out-Null }
    if ($k -match '^dach$|dach_satteldach|satteldach|glasdach|flachdach|flaches_dach|pv_dach|dach_mit|dachgarten|dachaufbau|dachbegruenung|dachelement|holzdach|roof') { $out.Add((New-Resolution "bauteiltyp/Dach" "rule_medium" "bauteil_dach")) | Out-Null }
    if ($k -match 'innenwand|innenwaende|innenw_nde|interior_wall|binnenbladen') { $out.Add((New-Resolution "bauteiltyp/Innenwand" "rule_high" "bauteil_innenwand")) | Out-Null }
    if ($k -match 'bruestung|br_stung|balustrad|parapet') { $out.Add((New-Resolution "bauteiltyp/Bruestung" "rule_high" "bauteil_bruestung")) | Out-Null }
    if ($k -match 'gelaender|gel_nder|bruestungsgelaender|br_stungsgel_nder|railing|handrail') { $out.Add((New-Resolution "bauteiltyp/Gelaender" "rule_high" "bauteil_gelaender")) | Out-Null }
    if ($k -match 'heizkoerper|heizk_rper|radiator') { $out.Add((New-Resolution "bauteiltyp/Heizkoerper" "rule_high" "bauteil_heizkoerper")) | Out-Null }
    if ($k -match 'moebel|m_bel|mobiliar|furniture|regal|bank|baenke|benches|stuhl|stuehle|sofa|betten|vorhang|vorhaenge|schrank|schraenke') { $out.Add((New-Resolution "bauteiltyp/Moebel" "rule_medium" "bauteil_moebel")) | Out-Null }
    if ($k -match 'feste_einbauten|feste_ausstattung|built_in') { $out.Add((New-Resolution "bauteiltyp/Festes_Einbauteil" "rule_medium" "bauteil_festes_einbauteil")) | Out-Null }
    if ($k -match 'kueche|kuechen|arbeitsplatte|arbeitsflaeche|kuechenflaeche|countertop|counter') { $out.Add((New-Resolution "bauteiltyp/Kueche" "rule_high" "bauteil_kueche")) | Out-Null }
    if ($k -match 'innenausbau|innenoberflaeche|innenausstattung|sideboard|garderobe|holzeinbauten|einbauten') { $out.Add((New-Resolution "bauteiltyp/Innenausbau_Element" "rule_medium" "bauteil_innenausbau")) | Out-Null }
    if ($k -match 'bodenfliese') { $out.Add((New-Resolution "bauteiltyp/Bodenfliese" "rule_high" "bauteil_bodenfliese")) | Out-Null }
    elseif ($k -match 'fliese|fayence|tile') { $out.Add((New-Resolution "bauteiltyp/Fliese" "rule_high" "bauteil_fliese")) | Out-Null }
    if ($k -match 'betonblock|betonbloecke|betonbl_cke|concrete_block') { $out.Add((New-Resolution "bauteiltyp/Betonblock" "rule_high" "bauteil_betonblock")) | Out-Null }
    if ($k -match 'hanfkalk|hanf_kalk|lehmstein|mauerstein|blockelement|baublock') { $out.Add((New-Resolution "bauteiltyp/Mauerstein_Block" "rule_medium" "bauteil_mauerstein_block")) | Out-Null }
    if ($k -match 'tragstruktur|tragwerk|primaertragwerk|prim_rtragwerk|primaerstruktur|primary_structure|holzstruktur|stahlstruktur|stahlkonstruktion|stahlbauteile|infill_struktur|bracing|aussteifung|framing|tragunterbau|retained_.*structure') { $out.Add((New-Resolution "bauteiltyp/Tragstruktur" "rule_medium" "bauteil_tragstruktur")) | Out-Null }
    if ($k -match 'treppe|stiege') { $out.Add((New-Resolution "bauteiltyp/Treppe" "rule_high" "bauteil_contains_treppe")) | Out-Null }
    if ($k -match 'wand|waende|wandteile|innenwand|innenwaende|aussenwand|aussenwaende|aussenmauer|lehmbauwaende|mauer|fassadenwand|binnenbladen') {
        if ($k -match 'tragend') { $out.Add((New-Resolution "bauteiltyp/Tragende_Wand" "rule_high" "bauteil_tragende_wand")) | Out-Null }
        else { $out.Add((New-Resolution "bauteiltyp/Wand" "rule_medium" "bauteil_contains_wand")) | Out-Null }
    }
    if ($k -match 'fassade|cladding|bekleidung|facade|profilbauglas|substation_screen|fassadenscreen|office_front|innenverglasung') { $out.Add((New-Resolution "bauteiltyp/Fassade" "rule_high" "bauteil_contains_fassade")) | Out-Null }
    if ($k -match 'leuchte|beleuchtung|luminaire|lamp|led|lichttube') { $out.Add((New-Resolution "bauteiltyp/Leuchte" "rule_high" "bauteil_lighting")) | Out-Null }
    if ($k -match 'sanitaer|sanitary|waschbecken|toilette|wc|urinal') { $out.Add((New-Resolution "bauteiltyp/Sanitaerobjekt" "rule_high" "bauteil_sanitary")) | Out-Null }
    if ($k -match 'decke|deckenplatte|deckenelement|hohlkoerperdecke|floor_slab|floor_panel|floor_panels|clt_floor|bodenpaneel|bodenpaneele') { $out.Add((New-Resolution "bauteiltyp/Deckenplatte" "rule_medium" "bauteil_decke_family")) | Out-Null }
    if ($k -match 'stuetze|stutze|st_tze|st_tzen|column|columns') { $out.Add((New-Resolution "bauteiltyp/Stuetze" "rule_high" "bauteil_stuetze")) | Out-Null }
    if ($k -match 'traeger|trager|tr_ger|beam|balken|stahlprofil|profilstahl|profile|steel_sections|support_members|curved_steel_sections|sturz|stuerz|bogen|boegen|arch|joist|solivage') { $out.Add((New-Resolution "bauteiltyp/Traeger" "rule_high" "bauteil_traeger")) | Out-Null }
    if ($k -match 'pfette|purlin|purlins') { $out.Add((New-Resolution "bauteiltyp/Pfette" "rule_high" "bauteil_pfette")) | Out-Null }
    if ($k -match 'fachwerk|truss|trusses|dachbinder') { $out.Add((New-Resolution "bauteiltyp/Fachwerktraeger" "rule_high" "bauteil_fachwerk")) | Out-Null }
    if ($k -match 'kern|core') { $out.Add((New-Resolution "bauteiltyp/Kern" "rule_medium" "bauteil_core")) | Out-Null }
    if ($k -match 'dachtragwerk|dachspant|kniespant|dachbinder|timber_truss|roof_truss|rafter|rafters|traespaer') { $out.Add((New-Resolution "bauteiltyp/Dachtragwerk" "rule_high" "bauteil_dachtragwerk")) | Out-Null }
    if ($k -match 'auflager|widerlager|plattenauflager') { $out.Add((New-Resolution "bauteiltyp/Auflager_Widerlager" "rule_high" "bauteil_auflager_widerlager")) | Out-Null }
    if ($k -match 'ziegel|brick|bricks|klinker|backstein') { $out.Add((New-Resolution "bauteiltyp/Ziegel" "rule_high" "bauteil_ziegel")) | Out-Null }
    if ($k -match 'pflaster|paving|flagstone|blaustein|granitplatten_terrasse|granitboden|natursteinplatten|bordstein|strassen|rampenelement|gehwegplatten|blockstufen') { $out.Add((New-Resolution "bauteiltyp/Pflaster_Bodenplatte" "rule_medium" "bauteil_pflaster_bodenplatte")) | Out-Null }
    if ($k -match 'bodenbelag|bodenaufbau|bodenaufbauten|parkett|dielen|terrassendielen|flooring|bodenbretter|fussboden|fussboeden|vloerdelen|caillebotis|moertelboden|mosaikboden|terrazzo') { $out.Add((New-Resolution "bauteiltyp/Bodenbelag" "rule_high" "bauteil_bodenbelag")) | Out-Null }
    if ($k -match 'gitterrost|stahlrost') { $out.Add((New-Resolution "bauteiltyp/Gitterrost" "rule_high" "bauteil_gitterrost")) | Out-Null }
    if ($k -match 'sonnenschutz|beschattung|awning|awnings') { $out.Add((New-Resolution "bauteiltyp/Beschattung_Sonnenschutz" "rule_high" "bauteil_beschattung_sonnenschutz")) | Out-Null }
    if ($k -match 'vordach|vordaecher|luifel|luifels|pergola|ueberdachung|atriumhuelle|atriumhulle|atrium') { $out.Add((New-Resolution "bauteiltyp/Vordach_Ueberdachung" "rule_medium" "bauteil_vordach_ueberdachung")) | Out-Null }
    if ($k -match 'fundament|bodenplatte|betonpfaehle|betonpfahl|pfahl|pfaehle') { $out.Add((New-Resolution "bauteiltyp/Fundament_Bodenplatte" "rule_medium" "bauteil_fundament_bodenplatte")) | Out-Null }
    if ($k -match 'blech|wellblech|trapezblech|metal_deck|metall_deckenpaneel') { $out.Add((New-Resolution "bauteiltyp/Blechpaneel" "rule_high" "bauteil_blechpaneel")) | Out-Null }
    if ($k -match 'schacht|schaechte') { $out.Add((New-Resolution "bauteiltyp/Schacht" "rule_high" "bauteil_schacht")) | Out-Null }
    if ($k -match 'landscape|aussenraum|park|pflanztrog|pflanztroege|pflanzenfilter|baeume|fahrradstaender') { $out.Add((New-Resolution "bauteiltyp/Landschaftselement" "rule_medium" "bauteil_landschaftselement")) | Out-Null }
    if ($k -match 'bestandsgebaeude|bestandslagerhaus|betriebsgebaeude|garage|schuppen|pavillon|pavillonensemble|hauptstruktur|rohbau|kreuzgang|observatoriumskuppel|krypta|kolonnade|glasgang|block_6000|bestand_block|print_building_structure|ramp_pier_components|wohnungsteile|residence_palace|industriegewaechshaus|gewaechshaus|glas_stahlwuerfel|betonstruktur|betonrahmen|concrete_frame|innere_box|holzgalerie|galerie') { $out.Add((New-Resolution "bauteiltyp/Bauwerksteil" "rule_medium" "bauteil_bauwerksteil")) | Out-Null }
    if ($k -notmatch 'bodenplatte|deckenplatte|floor_slab' -and $k -match 'paneel|panel|panels|platte|platten|sheet|sheets|board|boards|profilbauglas|faserzement|eternit|filzpaneel|sockel_plinthenplatten|plinthenplatten|dallet|dallettes|shingle|shingles|schindel') { $out.Add((New-Resolution "bauteiltyp/Platte_Paneel" "rule_medium" "bauteil_platte_paneel")) | Out-Null }
    return @($out | Sort-Object target -Unique)
}

function Resolve-Pruefung {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    $k = Normalize-Key -Value $Label
    if (Is-IgnorableLabel -Label $Label) { return @() }
    if ($k -match 'zug|tensile') { $out.Add((New-Resolution "pruefung_nachweis/Zugversuch" "rule_high" "pruefung_zugversuch")) | Out-Null }
    if ($k -match 'schweiss|weld') { $out.Add((New-Resolution "pruefung_nachweis/Schweissbarkeitspruefung" "rule_high" "pruefung_schweissbarkeit")) | Out-Null }
    if ($k -match 'statik|statisch|structural|engineer_sign_off|tragfaeh') { $out.Add((New-Resolution "pruefung_nachweis/Statische_Nachweisfuehrung" "rule_high" "pruefung_statik")) | Out-Null }
    if ($k -match 'vermess|geometr|scan|mass') { $out.Add((New-Resolution "pruefung_nachweis/Geometrische_Vermessung" "rule_medium" "pruefung_geometrie")) | Out-Null }
    if ($k -match 'sicht|visual') { $out.Add((New-Resolution "pruefung_nachweis/Sichtpruefung" "rule_medium" "pruefung_sicht")) | Out-Null }
    if ($k -match 'zustand|condition') { $out.Add((New-Resolution "pruefung_nachweis/Zustandsbewertung" "rule_medium" "pruefung_zustand")) | Out-Null }
    if ($k -match 'schadstoff|asbest|pcb|lead|blei') { $out.Add((New-Resolution "pruefung_nachweis/Schadstoffscreening" "rule_high" "pruefung_schadstoff")) | Out-Null }
    if ($k -match 'brand|fire') { $out.Add((New-Resolution "pruefung_nachweis/Brandnachweis" "rule_medium" "pruefung_brand")) | Out-Null }
    if ($k -match 'material|chemisch|chemical|metallographic|ce|zertifiz|testing|test') { $out.Add((New-Resolution "pruefung_nachweis/Materialpruefung" "rule_medium" "pruefung_material")) | Out-Null }
    return @($out | Sort-Object target -Unique)
}

function Resolve-Huerde {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    $k = Normalize-Key -Value $Label
    if (Is-IgnorableLabel -Label $Label) { return @() }

    if ($k -match 'nicht_direct_reuse|kein_direct_reuse|keine_reuse|kein_reuse|nicht_reuse|nicht_als_reuse|reuse_nicht|nicht_wiederverwendet|not_direct_reuse|nicht_fuer_diesen_fall') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Kein_Direct_Reuse_Nachweis" "rule_high" "abgrenzung_no_direct_reuse_evidence")) | Out-Null
    }
    if ($k -match 'bestandserhalt|retention') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Bestandserhalt_Nicht_Direct_Reuse" "rule_high" "abgrenzung_bestandserhalt")) | Out-Null
    }
    if ($k -match 'recycling|recycled|reststrom|reuse_recycled|materialreuse_vs_recycling') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Recycling_Nicht_Direct_Reuse" "rule_high" "abgrenzung_recycling")) | Out-Null
    }
    if ($k -match 'moebel|m_bel|dekoration|lose|fest_eingebaut|feste_einbauten') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Moebel_Dekoration_Nicht_Direct_Reuse" "rule_medium" "abgrenzung_moebel_dekoration")) | Out-Null
    }
    if ($k -match 'ungebaut|nicht_geplant|presseabsicht|nicht_als_gebaut|geplant') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Ungebaut_Nicht_Realisierte_Wiederverwendung" "rule_medium" "abgrenzung_ungebaut")) | Out-Null
    }
    if ($k -match 'dfd|future|spaetere_austausch|sp_tere_austausch') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Zukunftsfaehigkeit_Nicht_Aktuelle_Wiederverwendung" "rule_medium" "abgrenzung_future_dfd")) | Out-Null
    }
    if ($k -match 'reuse_anteil|teilweise_belegt|mengenkonflikt|nicht_aufgeschluesselt|nicht_aufgeschl_sselt|menge_nicht|unklare_herkunft') {
        $out.Add((New-Resolution "bewertungslogik_abgrenzung/Reuse_Anteil_Unklar" "rule_medium" "abgrenzung_reuse_anteil_unclear")) | Out-Null
    }

    if ($k -match 'brand|fire') { $out.Add((New-Resolution "huerde/Brandschutzkonflikt" "rule_medium" "huerde_brand")) | Out-Null }
    if ($k -match 'schadstoff|asbest|pcb') { $out.Add((New-Resolution "huerde/Schadstoffbelastung" "rule_high" "huerde_schadstoff")) | Out-Null }
    if ($k -match 'lager|storage|platz') { $out.Add((New-Resolution "huerde/Fehlende_Lagerflaeche" "rule_medium" "huerde_lager")) | Out-Null }
    if ($k -match 'transport|logistik|liefer|jit|site_constraints') { $out.Add((New-Resolution "huerde/Logistikproblem" "rule_medium" "huerde_logistik")) | Out-Null }
    if ($k -match 'toleranz|mass|geometr|profil|fit') { $out.Add((New-Resolution "huerde/Toleranzen" "rule_medium" "huerde_toleranzen")) | Out-Null }
    if ($k -match 'anschluss|schnittstelle|fuge|fugen|integration|alt_neu|montage') { $out.Add((New-Resolution "huerde/Anschlussproblem" "rule_high" "huerde_anschluss")) | Out-Null }
    if ($k -match 'kompatibilitaet|kompatibilit_t|passung|passgenau|systemmix|format|hoehen|h_hen|raster|grundriss') { $out.Add((New-Resolution "huerde/Kompatibilitaetsproblem" "rule_medium" "huerde_kompatibilitaet")) | Out-Null }
    if ($k -match 'freigabe|bauaufsichtlich|zulassung|technische_pruefung|technische_pr_fung') { $out.Add((New-Resolution "huerde/Technische_Freigabe" "rule_medium" "huerde_technische_freigabe")) | Out-Null }
    if ($k -match 'materialqualitaet|materialqualit_t|qualitaet|qualit_t|herkunft|zusammensetzung|materialdetails') { $out.Add((New-Resolution "huerde/Materialqualitaet_Unklar" "rule_medium" "huerde_materialqualitaet")) | Out-Null }
    if ($k -match '^zustand$|glaszustand|alter_leistung|zustand_passung|verschleiss') { $out.Add((New-Resolution "huerde/Zustand_Unklar" "rule_medium" "huerde_zustand")) | Out-Null }
    if ($k -match 'heterogen|charge|chargen|homogen|sortierung|unterschiedliche') { $out.Add((New-Resolution "huerde/Heterogenitaet_Chargen" "rule_medium" "huerde_heterogenitaet")) | Out-Null }
    if ($k -match 'aufbereitung|zuschnitt|bearbeitung|refurbishment|rekonditionierung|reinigung') { $out.Add((New-Resolution "huerde/Aufbereitungsaufwand" "rule_medium" "huerde_aufbereitungsaufwand")) | Out-Null }
    if ($k -match 'witterung|feuchte|abdichtung|waermebruecke|w_rmebr_cke|waermebrucken|w_rmebr_cken|d_mmk|daemmkonzept|d_mmkonzept|innenfeuchte') { $out.Add((New-Resolution "huerde/Witterung_Feuchte" "rule_medium" "huerde_witterung_feuchte")) | Out-Null }
    if ($k -match 'dauerhaft|restlebensdauer|robustheit|lebensdauer') { $out.Add((New-Resolution "huerde/Dauerhaftigkeit_Restlebensdauer" "rule_medium" "huerde_dauerhaftigkeit")) | Out-Null }
    if ($k -match 'hygiene') { $out.Add((New-Resolution "huerde/Hygieneanforderung" "rule_high" "huerde_hygiene")) | Out-Null }
    if ($k -match 'bauprodukt|ce\b|ce_|produktnachweis') { $out.Add((New-Resolution "huerde/Bauproduktstatus" "rule_medium" "huerde_bauproduktstatus")) | Out-Null }
    if ($k -match 'menge|mengen|aufschluessel|aufschl_ssel') { $out.Add((New-Resolution "huerde/Mengenunsicherheit" "rule_medium" "huerde_mengenunsicherheit")) | Out-Null }
    if ($k -match 'entwurf|lastannah|lastfunktion|dimensionen|hoehen|h_hen|grundrissbindung|bestimmen') { $out.Add((New-Resolution "huerde/Entwurfsbindung" "rule_medium" "huerde_entwurfsbindung")) | Out-Null }
    if ($k -match 'akzeptanz|wollte') { $out.Add((New-Resolution "huerde/Akzeptanzproblem" "rule_medium" "huerde_akzeptanz")) | Out-Null }
    if ($k -match 'bruch|beschaedigung|besch_digung') { $out.Add((New-Resolution "huerde/Bruch_Beschaedigungsrisiko" "rule_medium" "huerde_bruch_beschaedigung")) | Out-Null }
    if ($k -match 'unkonventionell|ungewoehnlich|ungew_hnlich|experimentell|materialexperiment') { $out.Add((New-Resolution "huerde/Unkonventionelles_Material" "rule_medium" "huerde_unkonventionelles_material")) | Out-Null }
    if ($k -match 'performance|stabilitaet|stabilit_t|dichtheit|eignung|werte|leistung|energieanforderung') { $out.Add((New-Resolution "huerde/Performance_Nachweis" "rule_medium" "huerde_performance_nachweis")) | Out-Null }
    if ($k -match 'verfuegbarkeit|availability|marktliquiditaet|timing|termin') {
        $out.Add((New-Resolution "huerde/Verfuegbarkeitsproblem" "rule_medium" "huerde_verfuegbarkeit")) | Out-Null
        if ($k -match 'timing|termin') { $out.Add((New-Resolution "huerde/Terminunsicherheit" "rule_medium" "huerde_termin")) | Out-Null }
    }
    if ($k -match 'daten|dokument|traceability|nachweis') { $out.Add((New-Resolution "huerde/Datenluecke" "rule_medium" "huerde_daten")) | Out-Null }
    if ($k -match 'haftung|liability') { $out.Add((New-Resolution "huerde/Haftung" "rule_high" "huerde_haftung")) | Out-Null }
    if ($k -match 'gewaehr|warranty') { $out.Add((New-Resolution "huerde/Gewaehrleistung" "rule_high" "huerde_gewaehrleistung")) | Out-Null }
    if ($k -match 'standard|norm|zulassung') { $out.Add((New-Resolution "huerde/Fehlende_Standardisierung" "rule_medium" "huerde_standardisierung")) | Out-Null }
    if ($k -match 'ausschreib') { $out.Add((New-Resolution "huerde/Ausschreibungsproblem" "rule_high" "huerde_ausschreibung")) | Out-Null }
    return @($out | Sort-Object target -Unique)
}

function Resolve-NormRechtLeistung {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    $k = Normalize-Key -Value $Label
    if (Is-IgnorableLabel -Label $Label) { return @() }
    if ($k -match 'f90') { $out.Add((New-Resolution "leistungsanforderung/F90" "rule_high" "leistung_f90")) | Out-Null }
    if ($k -match 'rei90') { $out.Add((New-Resolution "leistungsanforderung/REI90" "rule_high" "leistung_rei90")) | Out-Null }
    elseif ($k -match 'r90') { $out.Add((New-Resolution "leistungsanforderung/R90" "rule_high" "leistung_r90")) | Out-Null }
    if ($k -match 'brand|fire') { $out.Add((New-Resolution "leistungsanforderung/Brandschutz" "rule_medium" "leistung_brand")) | Out-Null }
    if ($k -match 'tragfaeh|structural|last') { $out.Add((New-Resolution "leistungsanforderung/Tragfaehigkeit" "rule_medium" "leistung_tragfaehigkeit")) | Out-Null }
    if ($k -match 'schall') { $out.Add((New-Resolution "leistungsanforderung/Schallschutz" "rule_medium" "leistung_schall")) | Out-Null }
    if ($k -match 'waerme|u_wert|thermal') { $out.Add((New-Resolution "leistungsanforderung/Waermeschutz" "rule_medium" "leistung_waerme")) | Out-Null }
    if ($k -match 'din_?en_?15804|en_?15804') { $out.Add((New-Resolution "norm/EN_15804" "rule_high" "norm_en_15804")) | Out-Null }
    if ($k -match 'en_?1090|ce_marking|ce') { $out.Add((New-Resolution "norm/EN_1090" "rule_medium" "norm_en_1090_or_ce_marking")) | Out-Null }
    if ($k -match 'iso_?14040') { $out.Add((New-Resolution "norm/ISO_14040" "rule_high" "norm_iso_14040")) | Out-Null }
    if ($k -match 'iso_?14044') { $out.Add((New-Resolution "norm/ISO_14044" "rule_high" "norm_iso_14044")) | Out-Null }
    if ($k -match 'iso_?20887') { $out.Add((New-Resolution "norm/ISO_20887" "rule_high" "norm_iso_20887")) | Out-Null }
    return @($out | Sort-Object target -Unique)
}

function Resolve-Kennwert {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    $k = Normalize-Key -Value $Label
    if (Is-IgnorableLabel -Label $Label) { return @() }
    if ($k -match '(^|_)co($|_)|co2|co_e|carbon|emission|embodied|thg|treibhausgas|gwp|global_warming|footprint|umweltschaeden|umweltsch_den') {
        if ($k -match 'saving|einspar|reduktion|saved|vermieden|diverted') { $out.Add((New-Resolution "kennwertdefinition/CO2_Einsparung" "rule_high" "kennwert_co2_saving")) | Out-Null }
        else { $out.Add((New-Resolution "kennwertdefinition/Graue_Energie" "rule_medium" "kennwert_embodied_carbon")) | Out-Null }
    }
    if ($k -match 'flaeche|fl_che|projektflaeche|geb_udefl_che|gesamtfl_che|nutzfl_che|bgf|gia|built_surface|area|extension|basement|umfang|park$') { $out.Add((New-Resolution "kennwertdefinition/Flaeche" "rule_high" "kennwert_flaeche")) | Out-Null }
    if ($k -match 'bauzeit|projektzeitraum|zeitraum|renovation|standzeit|montagezeit|einbau$|planungszeit|entwurfsbeginn') { $out.Add((New-Resolution "kennwertdefinition/Bauzeit" "rule_medium" "kennwert_bauzeit")) | Out-Null }
    if ($k -match 'fertigstellung|er_ffnung|eroeffnung|projektjahr|fallstudienstart|jahr') { $out.Add((New-Resolution "kennwertdefinition/Fertigstellung" "rule_medium" "kennwert_fertigstellung")) | Out-Null }
    if ($k -match 'baukosten|kosten_m|^kosten$|cost|budget|kredit|bausumme|mehrhonorar|honorar|ausgaben|preis|bauvertrag|vertrag') { $out.Add((New-Resolution "kennwertdefinition/Baukosten" "rule_medium" "kennwert_baukosten")) | Out-Null }
    if ($k -match 'kostenwirkung|kostenreduktion') { $out.Add((New-Resolution "kennwertdefinition/Kostenwirkung" "rule_medium" "kennwert_kostenwirkung")) | Out-Null }
    if ($k -match 'transportdistanz|distanz_spender|donor_receiver') { $out.Add((New-Resolution "kennwertdefinition/Transportdistanz" "rule_high" "kennwert_transportdistanz")) | Out-Null }
    if ($k -match 'lebensdauer|standortnutzungsdauer') { $out.Add((New-Resolution "kennwertdefinition/Lebensdauer" "rule_high" "kennwert_lebensdauer")) | Out-Null }
    if ($k -match 'abfallvermeidung|abfall_vermieden|waste_avoided|landfill|deponieren|abfallmaximum|abfallreduktion') { $out.Add((New-Resolution "kennwertdefinition/Abfallvermeidung" "rule_high" "kennwert_abfallvermeidung")) | Out-Null }
    if ($k -match 'bauteilalter') { $out.Add((New-Resolution "kennwertdefinition/Bauteilalter" "rule_high" "kennwert_bauteilalter")) | Out-Null }
    if ($k -match '^hoehe$|^h_he$|height') { $out.Add((New-Resolution "kennwertdefinition/Hoehe" "rule_high" "kennwert_hoehe")) | Out-Null }
    if ($k -match 'geschosse|storey|storeys') { $out.Add((New-Resolution "kennwertdefinition/Geschosse" "rule_high" "kennwert_geschosse")) | Out-Null }
    if ($k -match '^energie$|energiebedarf|primaerenergie|prim_renergie') { $out.Add((New-Resolution "kennwertdefinition/Energiebedarf" "rule_medium" "kennwert_energiebedarf")) | Out-Null }
    if ($k -match 'pv|erdwaermesonden|erdw_rmesonden|energieerzeugung|stromanteil') { $out.Add((New-Resolution "kennwertdefinition/Energieerzeugung" "rule_medium" "kennwert_energieerzeugung")) | Out-Null }
    if ($k -match 'arbeitsplaetze|arbeitspl_tze|workplace') { $out.Add((New-Resolution "kennwertdefinition/Arbeitsplaetze" "rule_high" "kennwert_arbeitsplaetze")) | Out-Null }
    if ($k -match 'wiederverwendeter_stahl|wiederverwendete_stahl|wiederverwendete_masse|betonvolumen|reused_steel|steel_reused|tonnage|gesamtstahl|stahl_aus|stock|materialien|materialmenge|beton_aus|ziegelflaeche|ziegelfl_che|ziegelvolumen|aluminiumprofile|profile|hohlkoerperdecken|hcs|masse|geerntete_materialien|sekundaere_materialien|sekund_re_materialien') { $out.Add((New-Resolution "kennwertdefinition/Materialmenge" "rule_medium" "kennwert_materialmenge")) | Out-Null }
    if ($k -match 'reuse|re_use|wiederverwend|wiederverwendungs|reuse_anteil|anteil_reused|quote|rate|second_hand|altmaterial|borrowed_materials|materialwiederverwendung|ziel_reuse|erreichter_reuse') { $out.Add((New-Resolution "kennwertdefinition/Wiederverwendungsquote" "rule_medium" "kennwert_reuse_quote")) | Out-Null }
    if ($k -match 'recyclingrate|recycled_materials|upcycled_recycled|recyclingbeton|rc_zuschlag') { $out.Add((New-Resolution "kennwertdefinition/Recyclingquote" "rule_medium" "kennwert_recyclingquote")) | Out-Null }
    if ($k -match 'anzahl|ursprungs|tueren|t_ren|fenster|platten|paneele|bloecke|bl_cke|radiatoren|heizkoerper|leuchten|sanit_r|sanitaer|mobile_trennwand|glastueren|glast_ren|produkte|sortierkategorien|a_gain_produkte') { $out.Add((New-Resolution "kennwertdefinition/Bauteilanzahl" "rule_medium" "kennwert_bauteilanzahl")) | Out-Null }
    if ($k -match 'abmessung|spannweite|breite|laenge|l_nge|stich|rise|oeffnungswinkel|ffnungswinkel|capacity|einzelgewicht|gewicht') { $out.Add((New-Resolution "kennwertdefinition/Abmessung" "rule_medium" "kennwert_abmessung")) | Out-Null }
    if ($k -match 'herkunft|donor|quellen|urspruengliche|urspr_ngliche|originalgebaeude|originalgeb_ude') { $out.Add((New-Resolution "kennwertdefinition/Materialherkunft" "rule_medium" "kennwert_materialherkunft")) | Out-Null }
    if ($k -match 'dgnb|epc|auszeichnung|prize|zertifiz') { $out.Add((New-Resolution "kennwertdefinition/Zertifizierung_Auszeichnung" "rule_medium" "kennwert_zertifizierung")) | Out-Null }
    if ($k -match 'wohneinheiten|betten|unterrichtsgruppen|workspace|geplante_nutzung') { $out.Add((New-Resolution "kennwertdefinition/Nutzungsumfang" "rule_medium" "kennwert_nutzungsumfang")) | Out-Null }
    if ($k -match 'primaermaterial|prim_rmaterial|ressourcen') { $out.Add((New-Resolution "kennwertdefinition/Primaermaterial_Einsparung" "rule_medium" "kennwert_primaermaterial")) | Out-Null }
    if ($k -match 'wasser|regenwasserspeicher') { $out.Add((New-Resolution "kennwertdefinition/Wasserkennwert" "rule_medium" "kennwert_wasser")) | Out-Null }
    if ($k -match 'u_wert') { $out.Add((New-Resolution "kennwertdefinition/U_Wert" "rule_high" "kennwert_u_wert")) | Out-Null }
    if ($k -match 'gebaeudemasse|geb_udemasse|betonerhalt|print_building_structure') { $out.Add((New-Resolution "kennwertdefinition/Gebaeudemasse" "rule_medium" "kennwert_gebaeudemasse")) | Out-Null }
    if ($k -match 'planungsaufwand|zusatzaufwand|sourcing_pr_fung|sourcing_pruefung|mehrhonorar') { $out.Add((New-Resolution "kennwertdefinition/Planungsaufwand" "rule_medium" "kennwert_planungsaufwand")) | Out-Null }
    if ($k -match 'demontagegrad|demontier') { $out.Add((New-Resolution "kennwertdefinition/Demontagegrad" "rule_high" "kennwert_demontagegrad")) | Out-Null }
    if ($k -match 'materialwert|restwert') { $out.Add((New-Resolution "kennwertdefinition/Materialwert" "rule_high" "kennwert_materialwert")) | Out-Null }
    return @($out | Sort-Object target -Unique)
}

function Resolve-Akteur {
    param([hashtable]$Lookup, [string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    if (Is-IgnorableLabel -Label $Label) { return @() }
    $labelsToTry = New-Object System.Collections.Generic.List[string]
    $labelsToTry.Add($Label) | Out-Null
    if ($Label -match '[,;/]') {
        foreach ($piece in ($Label -split '\s*(;|,|/)\s*')) {
            if ($piece -notmatch '^(;|,|/)$' -and -not [string]::IsNullOrWhiteSpace($piece)) {
                $labelsToTry.Add($piece.Trim()) | Out-Null
            }
        }
    }
    $manual = @{
        "baubuero_in_situ" = "akteur/baubuero_in_situ_zirkular"
        "bauburo_in_situ" = "akteur/baubuero_in_situ_zirkular"
        "zirkular" = "akteur/Zirkular_GmbH"
        "zirkular_gmbh" = "akteur/Zirkular_GmbH"
        "rotor_dc" = "akteur/Rotor_DC"
        "rotordc" = "akteur/Rotor_DC"
        "rotor" = "akteur/Rotor"
        "concular" = "akteur/Concular"
        "madaster" = "akteur/Madaster"
        "bellastock" = "akteur/Bellastock"
        "lendager" = "akteur/Lendager"
        "dgnb" = "akteur/DGNB"
        "epea" = "akteur/EPEA"
        "superuse_studios" = "akteur/Superuse_Studios"
        "cityfoerster" = "akteur/CITYFOERSTER"
        "arup" = "akteur/Arup"
        "cepezed" = "akteur/cepezed"
        "cleveland_steel_and_tubes" = "akteur/Cleveland_Steel_and_Tubes"
        "consolis_parma" = "akteur/Consolis_Parma"
        "imd_raadgevende_ingenieurs" = "akteur/IMd_Raadgevende_Ingenieurs"
        "ramboll_finland" = "akteur/Ramboll_Finland"
        "skanska_finland" = "akteur/Skanska_Finland"
        "umacon" = "akteur/Umacon"
        "blaf_architecten" = "akteur/BLAF_Architecten"
    }
    foreach ($candidateLabel in ($labelsToTry | Sort-Object -Unique)) {
        $exact = Resolve-Exact -Lookup $Lookup -Entity "akteur" -Label $candidateLabel
        foreach ($r in $exact) { $out.Add($r) | Out-Null }
        $k = Normalize-Key -Value $candidateLabel
        if ($manual.ContainsKey($k)) {
            $confidence = if ($candidateLabel -eq $Label) { "manual_high" } else { "manual_split" }
            $out.Add((New-Resolution $manual[$k] $confidence "akteur_manual_alias")) | Out-Null
        }
    }
    return @($out | Sort-Object target -Unique)
}

function Resolve-Akteurrolle {
    param([string]$Label)
    $out = New-Object System.Collections.Generic.List[object]
    if (Is-IgnorableLabel -Label $Label) { return @() }
    $k = Normalize-Key -Value $Label

    if ($k -match 'bauherr|auftraggeber|client|developer|eigentuemer|eigentumer|bauherrin|nutz|owner|joint_venture|schultraeger|prim_rer_auftraggeber|primaerer_auftraggeber') {
        $out.Add((New-Resolution "akteurrolle/Bauherr_Auftraggeber" "rule_high" "role_client_owner")) | Out-Null
    }
    if ($k -match 'architekt|architecture|architektur|entwurf|designteam|design_team|design_build|circular_design') {
        $out.Add((New-Resolution "akteurrolle/Architektur" "rule_high" "role_architecture")) | Out-Null
    }
    if ($k -match 'tragwerk|structural|bauingenieur|civil_engineer|engineering|ingenieur|statik|konstrukteur|engineer_reused') {
        $out.Add((New-Resolution "akteurrolle/Tragwerksplanung" "rule_high" "role_structural_engineering")) | Out-Null
    }
    if ($k -match 'contractor|bauunternehmen|builder|hauptauftragnehmer|general_contractor|bauausfuehrung|bauausf_hrung|main_builder|ausfuehrung|ausf_hrung') {
        $out.Add((New-Resolution "akteurrolle/Bauausfuehrung" "rule_high" "role_construction")) | Out-Null
    }
    if ($k -match 'rueckbau|r_ckbau|demolition|demontage|donor|abbruch') {
        $out.Add((New-Resolution "akteurrolle/Rueckbau_Demontage" "rule_high" "role_deconstruction")) | Out-Null
    }
    if ($k -match 'supplier|stockholder|materiallieferant|material_lieferant|materialliefer|reclaimed_steel|lieferkette') {
        $out.Add((New-Resolution "akteurrolle/Materiallieferant" "rule_high" "role_supplier")) | Out-Null
    }
    if ($k -match 'reuse|re_use|urban_mining|circular|materialstrategie|amo_reuse|bauteilwiederverwendung|bauteiljagd|bim_katalog') {
        $out.Add((New-Resolution "akteurrolle/Reuse_Beratung" "rule_high" "role_reuse_consulting")) | Out-Null
    }
    if ($k -match 'pruefung|pr_fung|qa|qualitaet|qualit_t|zulassung|kontrolleur|testing|certification') {
        $out.Add((New-Resolution "akteurrolle/Pruefung_Qualitaetssicherung" "rule_high" "role_quality_testing")) | Out-Null
    }
    if ($k -match 'aufbereitung|refurbishment|redesign|joinery|furniture|rekonditionierung') {
        $out.Add((New-Resolution "akteurrolle/Aufbereitung_Refurbishment" "rule_high" "role_refurbishment")) | Out-Null
    }
    if ($k -match 'forschung|dokumentation|autor|university|hochschule|research|monitoring') {
        $out.Add((New-Resolution "akteurrolle/Forschung_Dokumentation" "rule_high" "role_research_documentation")) | Out-Null
    }
    if ($k -match 'nachhaltigkeit|sustainability|lca|materialpass|passport|esg|hqe|umweltberatung') {
        $out.Add((New-Resolution "akteurrolle/Nachhaltigkeitsberatung" "rule_high" "role_sustainability")) | Out-Null
    }
    if ($k -match 'projektmanagement|project_manager|koordination|koordinator|partner|kollaborateur|projektpartner|prozess|planung_entwicklung_beratung') {
        $out.Add((New-Resolution "akteurrolle/Projektmanagement_Koordination" "rule_medium" "role_project_coordination")) | Out-Null
    }
    if ($k -match 'landschaft|landscape|aussenraum|freiraum') {
        $out.Add((New-Resolution "akteurrolle/Landschaftsplanung" "rule_high" "role_landscape")) | Out-Null
    }
    if ($k -match 'tga|gebaeudetechnik|geb_udetechnik|installation|energie|services|thermik|epb|be_tce') {
        $out.Add((New-Resolution "akteurrolle/TGA_Gebaeudetechnik" "rule_high" "role_building_services")) | Out-Null
    }
    if ($k -match 'brandschutz|barrierefreiheit|sicherheit') {
        $out.Add((New-Resolution "akteurrolle/Brandschutz_Barrierefreiheit" "rule_high" "role_fire_access_safety")) | Out-Null
    }
    if ($k -match 'stahlbau|holzbau|fabricator|erector|fertigung|steel_structure|wrap_contractor') {
        $out.Add((New-Resolution "akteurrolle/Stahlbau_Fertigung" "rule_high" "role_fabrication")) | Out-Null
    }
    if ($k -match 'fassade|facade') {
        $out.Add((New-Resolution "akteurrolle/Fassade" "rule_high" "role_facade")) | Out-Null
    }
    if ($k -match 'kuenstler|k_nstler|kunst|grafik|illustration|szenografie|skatepark') {
        $out.Add((New-Resolution "akteurrolle/Kunst_Gestaltung" "rule_high" "role_art_design")) | Out-Null
    }
    if ($k -match 'betreiber|nutzer|soziale_integration') {
        $out.Add((New-Resolution "akteurrolle/Betreiber_Nutzer" "rule_medium" "role_operator_user")) | Out-Null
    }
    if ($k -match 'kommune|municipality|ville|amt|oeffentlich|offentlich|administration|government') {
        $out.Add((New-Resolution "akteurrolle/Oeffentliche_Hand" "rule_medium" "role_public_sector")) | Out-Null
    }
    if ($k -match '^(akteure|beteiligte|projektakteure|beteiligte_akteure|akteure_im_projektumfeld)$|projektteam|mitwirkend|quellenbezug') {
        $out.Add((New-Resolution "akteurrolle/Projektbeteiligte_Unbestimmt" "rule_medium" "role_unspecified_project_participant")) | Out-Null
    }

    return @($out | Sort-Object target -Unique)
}

$lookup = Build-NodeLookup -Entities @(
    "material", "bauteiltyp", "huerde", "pruefung_nachweis", "norm",
    "leistungsanforderung", "kennwertdefinition", "akteur", "fallstudie",
    "projekt", "bauobjekt", "reuse_kette", "reuse_kettenstation", "akteurrolle"
)

$edges = New-Object System.Collections.Generic.List[object]
$reviews = New-Object System.Collections.Generic.List[object]

foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $TargetRoot "reuse_einsatz") -Directory)) {
    $index = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path -LiteralPath $index)) { continue }
    $fm = Read-Frontmatter -Path $index
    $source = "reuse_einsatz/$($dir.Name)"
    $legacyPath = Get-FmFirst -Frontmatter $fm -Key "legacy_path"

    foreach ($fallstudie in (Get-FmList -Frontmatter $fm -Key "fallstudie")) {
        Add-Edge $edges $source "belongs_to_fallstudie" $fallstudie "fallstudie" $fallstudie "structural" "frontmatter" $legacyPath
    }
    foreach ($projekt in (Get-FmList -Frontmatter $fm -Key "projekt")) {
        Add-Edge $edges $source "belongs_to_projekt" "projekt/$projekt" "projekt" $projekt "structural" "frontmatter" $legacyPath
    }
    foreach ($bauobjekt in (Get-FmList -Frontmatter $fm -Key "bauobjekt")) {
        Add-Edge $edges $source "installed_in_bauobjekt" "bauobjekt/$bauobjekt" "bauobjekt" $bauobjekt "structural" "frontmatter" $legacyPath
    }

    $materialLabel = Get-FmFirst -Frontmatter $fm -Key "material_label"
    $materialResolved = Resolve-Material -Label $materialLabel
    foreach ($r in $materialResolved) { Add-Edge $edges $source "uses_material" $r.target "material_label" $materialLabel $r.confidence $r.rule $legacyPath }
    if ($materialResolved.Count -eq 0) { Add-Review $reviews $source "material_label" $materialLabel "material" "no_confident_material_match" $legacyPath }

    $bauteilLabel = Get-FmFirst -Frontmatter $fm -Key "bauteil_label"
    $bauteilResolved = Resolve-Bauteiltyp -Label $bauteilLabel
    foreach ($r in $bauteilResolved) { Add-Edge $edges $source "has_bauteiltyp" $r.target "bauteil_label" $bauteilLabel $r.confidence $r.rule $legacyPath }
    if ($bauteilResolved.Count -eq 0) { Add-Review $reviews $source "bauteil_label" $bauteilLabel "bauteiltyp" "no_confident_bauteiltyp_match" $legacyPath }

    $pruefungLabel = Get-FmFirst -Frontmatter $fm -Key "pruefung_label"
    $pruefungResolved = Resolve-Pruefung -Label $pruefungLabel
    foreach ($r in $pruefungResolved) { Add-Edge $edges $source "has_pruefung_nachweis" $r.target "pruefung_label" $pruefungLabel $r.confidence $r.rule $legacyPath }
    if ($pruefungResolved.Count -eq 0) { Add-Review $reviews $source "pruefung_label" $pruefungLabel "pruefung_nachweis" "no_confident_pruefung_match" $legacyPath }

    $huerdeLabel = Get-FmFirst -Frontmatter $fm -Key "huerde_label"
    $huerdeResolved = Resolve-Huerde -Label $huerdeLabel
    foreach ($r in $huerdeResolved) {
        $relation = if ($r.target -match '^bewertungslogik_abgrenzung/') { "has_bewertungslogik_abgrenzung" } else { "has_huerde" }
        Add-Edge $edges $source $relation $r.target "huerde_label" $huerdeLabel $r.confidence $r.rule $legacyPath
    }
    if ($huerdeResolved.Count -eq 0) { Add-Review $reviews $source "huerde_label" $huerdeLabel "huerde" "no_confident_huerde_match" $legacyPath }

    $normLabel = Get-FmFirst -Frontmatter $fm -Key "norm_recht_label"
    $normResolved = Resolve-NormRechtLeistung -Label $normLabel
    foreach ($r in $normResolved) {
        $relation = if ($r.target -match '^norm/') { "references_norm" } else { "has_leistungsanforderung" }
        Add-Edge $edges $source $relation $r.target "norm_recht_label" $normLabel $r.confidence $r.rule $legacyPath
    }
    if ($normResolved.Count -eq 0) { Add-Review $reviews $source "norm_recht_label" $normLabel "norm_or_leistungsanforderung" "no_confident_norm_or_requirement_match" $legacyPath }
}

foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $TargetRoot "datenpunkt") -Directory)) {
    $index = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path -LiteralPath $index)) { continue }
    $fm = Read-Frontmatter -Path $index
    $source = "datenpunkt/$($dir.Name)"
    $legacyPath = Get-FmFirst -Frontmatter $fm -Key "legacy_path"

    foreach ($fallstudie in (Get-FmList -Frontmatter $fm -Key "fallstudie")) {
        Add-Edge $edges $source "belongs_to_fallstudie" $fallstudie "fallstudie" $fallstudie "structural" "frontmatter" $legacyPath
    }
    foreach ($projekt in (Get-FmList -Frontmatter $fm -Key "projekt")) {
        Add-Edge $edges $source "belongs_to_projekt" "projekt/$projekt" "projekt" $projekt "structural" "frontmatter" $legacyPath
    }
    foreach ($bauobjekt in (Get-FmList -Frontmatter $fm -Key "bauobjekt")) {
        Add-Edge $edges $source "measured_on_bauobjekt" "bauobjekt/$bauobjekt" "bauobjekt" $bauobjekt "structural" "frontmatter" $legacyPath
    }

    $kennwertLabel = Get-FmFirst -Frontmatter $fm -Key "kennwert_label"
    $resolved = Resolve-Kennwert -Label $kennwertLabel
    foreach ($r in $resolved) { Add-Edge $edges $source "measures_kennwertdefinition" $r.target "kennwert_label" $kennwertLabel $r.confidence $r.rule $legacyPath }
    if ($resolved.Count -eq 0) { Add-Review $reviews $source "kennwert_label" $kennwertLabel "kennwertdefinition" "no_confident_kennwertdefinition_match" $legacyPath }
}

foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $TargetRoot "akteur_beteiligung") -Directory)) {
    $index = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path -LiteralPath $index)) { continue }
    $fm = Read-Frontmatter -Path $index
    $source = "akteur_beteiligung/$($dir.Name)"
    $legacyPath = Get-FmFirst -Frontmatter $fm -Key "legacy_path"

    foreach ($fallstudie in (Get-FmList -Frontmatter $fm -Key "fallstudie")) {
        Add-Edge $edges $source "belongs_to_fallstudie" $fallstudie "fallstudie" $fallstudie "structural" "frontmatter" $legacyPath
    }
    foreach ($projekt in (Get-FmList -Frontmatter $fm -Key "projekt")) {
        Add-Edge $edges $source "belongs_to_projekt" "projekt/$projekt" "projekt" $projekt "structural" "frontmatter" $legacyPath
    }
    foreach ($bauobjekt in (Get-FmList -Frontmatter $fm -Key "bauobjekt")) {
        Add-Edge $edges $source "relates_to_bauobjekt" "bauobjekt/$bauobjekt" "bauobjekt" $bauobjekt "structural" "frontmatter" $legacyPath
    }

    $actorLabel = Get-FmFirst -Frontmatter $fm -Key "akteur_candidate"
    $actorResolved = Resolve-Akteur -Lookup $lookup -Label $actorLabel
    foreach ($r in $actorResolved) { Add-Edge $edges $source "involves_akteur" $r.target "akteur_candidate" $actorLabel $r.confidence $r.rule $legacyPath }
    if ($actorResolved.Count -eq 0) {
        $reason = if ($actorLabel -match '[,;/]') { "multi_actor_or_unmerged_candidate" } else { "no_existing_actor_match" }
        Add-Review $reviews $source "akteur_candidate" $actorLabel "akteur" $reason $legacyPath
    }
    elseif ($actorLabel -match '[,;/]') {
        Add-Review $reviews $source "akteur_candidate" $actorLabel "akteur" "partially_resolved_multi_actor_label" $legacyPath
    }

    $roleLabel = Get-FmFirst -Frontmatter $fm -Key "beziehung"
    $roleResolved = Resolve-Akteurrolle -Label $roleLabel
    foreach ($r in $roleResolved) { Add-Edge $edges $source "has_akteurrolle" $r.target "beziehung" $roleLabel $r.confidence $r.rule $legacyPath }
    if ($roleResolved.Count -eq 0) {
        Add-Review $reviews $source "beziehung" $roleLabel "akteurrolle" "no_confident_akteurrolle_match" $legacyPath
    }
}

foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $TargetRoot "fallstudie") -Directory)) {
    $index = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path -LiteralPath $index)) { continue }
    $fm = Read-Frontmatter -Path $index
    $source = "fallstudie/$($dir.Name)"
    foreach ($projekt in (Get-FmList -Frontmatter $fm -Key "projekt")) {
        Add-Edge $edges $source "has_projekt" "projekt/$projekt" "projekt" $projekt "structural" "frontmatter" ""
    }
    foreach ($bauobjekt in (Get-FmList -Frontmatter $fm -Key "bauobjekt")) {
        Add-Edge $edges $source "has_bauobjekt" "bauobjekt/$bauobjekt" "bauobjekt" $bauobjekt "structural" "frontmatter" ""
    }
}

foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $TargetRoot "reuse_kette") -Directory -ErrorAction SilentlyContinue)) {
    $index = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path -LiteralPath $index)) { continue }
    $fm = Read-Frontmatter -Path $index
    $source = "reuse_kette/$($dir.Name)"
    foreach ($fallstudie in (Get-FmList -Frontmatter $fm -Key "fallstudie")) {
        Add-Edge $edges $source "belongs_to_fallstudie" $fallstudie "fallstudie" $fallstudie "structural" "frontmatter" ""
    }
}

foreach ($dir in (Get-ChildItem -LiteralPath (Join-Path $TargetRoot "reuse_kettenstation") -Directory -ErrorAction SilentlyContinue)) {
    $index = Join-Path $dir.FullName "index.md"
    if (-not (Test-Path -LiteralPath $index)) { continue }
    $fm = Read-Frontmatter -Path $index
    $source = "reuse_kettenstation/$($dir.Name)"
    $chain = Get-FmFirst -Frontmatter $fm -Key "reuse_kette"
    if (-not [string]::IsNullOrWhiteSpace($chain)) {
        Add-Edge $edges $source "part_of_reuse_kette" $chain "reuse_kette" $chain "structural" "frontmatter" ""
    }
    foreach ($fallstudie in (Get-FmList -Frontmatter $fm -Key "fallstudie")) {
        Add-Edge $edges $source "belongs_to_fallstudie" $fallstudie "fallstudie" $fallstudie "structural" "frontmatter" ""
    }
}

$dedupEdges = $edges |
    Sort-Object source, relation, target, field, raw_label -Unique
$dedupReviews = $reviews |
    Sort-Object source, field, raw_label, suggested_entity, reason -Unique

$dedupEdges | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase6_graph_edges.csv"
$dedupReviews | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase6_label_resolution_review.csv"

$edgeSummary = $dedupEdges |
    Group-Object relation, target_entity |
    Sort-Object Name |
    ForEach-Object {
        [pscustomobject]@{
            count = $_.Count
            relation_target = $_.Name
        }
    }
$edgeSummary | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase6_edge_summary.csv"

$reviewSummary = $dedupReviews |
    Group-Object suggested_entity, field, reason |
    Sort-Object Count -Descending |
    ForEach-Object {
        [pscustomobject]@{
            count = $_.Count
            bucket = $_.Name
        }
    }
$reviewSummary | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase6_review_summary.csv"

$manifest = @(
    "# Phase 6 Edge and Review Manifest"
    ""
    "- Edge CSV: _migration/phase6_graph_edges.csv"
    "- Label review CSV: _migration/phase6_label_resolution_review.csv"
    "- Edge summary CSV: _migration/phase6_edge_summary.csv"
    "- Review summary CSV: _migration/phase6_review_summary.csv"
    "- Edges generated: $(@($dedupEdges).Count)"
    "- Review items generated: $(@($dedupReviews).Count)"
    ""
    "This phase does not edit graph nodes. It creates import-ready relationship rows and separates uncertain label normalization into review queues."
    ""
) -join "`n"
[System.IO.File]::WriteAllText((Join-Path $TargetRoot "_system/phase6_edges_and_reviews_manifest.md"), $manifest, $Utf8NoBom)

[pscustomobject]@{
    target_root = $TargetRoot
    edges = @($dedupEdges).Count
    review_items = @($dedupReviews).Count
    edge_csv = "_migration/phase6_graph_edges.csv"
    review_csv = "_migration/phase6_label_resolution_review.csv"
}
