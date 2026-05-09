param(
    [string[]]$Roots = @("_graph", "_migration")
)

$ErrorActionPreference = "Stop"
$Utf8NoBom = New-Object System.Text.UTF8Encoding($false)

function New-CodepointString {
    param([Parameter(ValueFromRemainingArguments=$true)][int[]]$Codepoints)
    return -join ($Codepoints | ForEach-Object { [string][char]$_ })
}

$replacements = @(
    @((New-CodepointString 0x00C3 0x00A4), (New-CodepointString 0x00E4)), # ae
    @((New-CodepointString 0x00C3 0x00B6), (New-CodepointString 0x00F6)), # oe
    @((New-CodepointString 0x00C3 0x00BC), (New-CodepointString 0x00FC)), # ue
    @((New-CodepointString 0x00C3 0x201E), (New-CodepointString 0x00C4)), # Ae
    @((New-CodepointString 0x00C3 0x2013), (New-CodepointString 0x00D6)), # Oe
    @((New-CodepointString 0x00C3 0x0153), (New-CodepointString 0x00DC)), # Ue
    @((New-CodepointString 0x00C3 0x0178), (New-CodepointString 0x00DF)), # ss
    @((New-CodepointString 0x00C3 0x00A9), (New-CodepointString 0x00E9)), # e acute
    @((New-CodepointString 0x00C3 0x00A8), (New-CodepointString 0x00E8)), # e grave
    @((New-CodepointString 0x00C3 0x00A1), (New-CodepointString 0x00E1)), # a acute
    @((New-CodepointString 0x00C3 0x00A0), (New-CodepointString 0x00E0)), # a grave
    @((New-CodepointString 0x00C3 0x00A2), (New-CodepointString 0x00E2)), # a circumflex
    @((New-CodepointString 0x00C3 0x00AA), (New-CodepointString 0x00EA)), # e circumflex
    @((New-CodepointString 0x00C3 0x00AF), (New-CodepointString 0x00EF)), # i diaeresis
    @((New-CodepointString 0x00C3 0x00B4), (New-CodepointString 0x00F4)), # o circumflex
    @((New-CodepointString 0x00C3 0x00A7), (New-CodepointString 0x00E7)), # c cedilla
    @((New-CodepointString 0x00C3 0x00B1), (New-CodepointString 0x00F1)), # n tilde
    @((New-CodepointString 0x00C3 0x00B8), (New-CodepointString 0x00F8)), # o slash
    @((New-CodepointString 0x00C3 0x00A6), (New-CodepointString 0x00E6)), # ae ligature
    @((New-CodepointString 0x00C3 0x2020), (New-CodepointString 0x00C6)), # AE ligature
    @((New-CodepointString 0x00C2 0x00AE), (New-CodepointString 0x00AE)), # registered sign
    @((New-CodepointString 0x00E2 0x201A 0x201A), (New-CodepointString 0x2082)), # subscript 2
    @((New-CodepointString 0x00E2 0x20AC 0x201D), (New-CodepointString 0x2014)), # em dash
    @((New-CodepointString 0x00E2 0x20AC 0x201C), (New-CodepointString 0x2013)), # en dash
    @((New-CodepointString 0x00E2 0x20AC 0x2122), (New-CodepointString 0x2019)), # right single quote
    @((New-CodepointString 0x00E2 0x20AC 0x02DC), (New-CodepointString 0x2018)), # left single quote
    @((New-CodepointString 0x00E2 0x20AC 0x0153), (New-CodepointString 0x201C)), # left double quote
    @((New-CodepointString 0x00E2 0x20AC 0x017E), (New-CodepointString 0x201E))  # low double quote
)

$files = New-Object System.Collections.Generic.List[string]
foreach ($root in $Roots) {
    if (-not (Test-Path -LiteralPath $root)) { continue }
    & rg --files $root -g "*.md" -g "*.csv" | ForEach-Object {
        $files.Add($_) | Out-Null
    }
}

$log = New-Object System.Collections.Generic.List[object]
foreach ($file in ($files | Sort-Object -Unique)) {
    $path = (Resolve-Path -LiteralPath $file).Path
    $text = [System.IO.File]::ReadAllText($path, [System.Text.Encoding]::UTF8)
    $updated = $text
    $count = 0
    foreach ($pair in $replacements) {
        $bad = $pair[0]
        $good = $pair[1]
        if ($updated.Contains($bad)) {
            $before = $updated
            $updated = $updated.Replace($bad, $good)
            $count += ([regex]::Matches($before, [regex]::Escape($bad))).Count
        }
    }
    if ($updated -ne $text) {
        [System.IO.File]::WriteAllText($path, $updated, $Utf8NoBom)
        $log.Add([pscustomobject]@{
            path = $file
            replacement_count = $count
        }) | Out-Null
    }
}

$log | Export-Csv -NoTypeInformation -Encoding UTF8 -Path "_migration/phase13_encoding_repair.csv"

$summary = @(
    "# Phase 13 Encoding Repair"
    ""
    "- Files scanned: $($files.Count)"
    "- Files repaired: $($log.Count)"
    "- CSV: _migration/phase13_encoding_repair.csv"
    ""
    "This pass repairs UTF-8 text that had been interpreted as Windows-1252 during earlier generated vocabulary phases."
    ""
) -join "`n"

New-Item -ItemType Directory -Force -Path "_graph/_system" | Out-Null
[System.IO.File]::WriteAllText("_graph/_system/phase13_encoding_repair_manifest.md", $summary, $Utf8NoBom)

[pscustomobject]@{
    files_scanned = $files.Count
    files_repaired = $log.Count
    csv = "_migration/phase13_encoding_repair.csv"
}
