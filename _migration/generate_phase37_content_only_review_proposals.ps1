$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$manualRoot = Join-Path $root "_manual_review/nodes"
$proposalCsvPath = Join-Path $root "_migration/37_content_only_review_proposals.csv"
$reportPath = Join-Path $root "_migration/37_Content_Only_Review_Proposals.md"

$nodes = @(
    "bauteiltyp/Holzrahmenelement",
    "bauteiltyp/Treppenwange",
    "datenmodell/Gebaeuderessourcenpass",
    "dokumenttyp/Gebaeuderessourcenpass",
    "fuegung_verbindung/Beton_Fertigteile_Verbindungen",
    "fuegung_verbindung/Composite_Verbindungen",
    "fuegung_verbindung/Holz_Verbindungen",
    "fuegung_verbindung/Stahl_Verbindungen",
    "fuegung_verbindung/Stahlseil",
    "reuse_strategie/Temporaerer_Wiedereinbau",
    "zertifizierung_bewertungssystem/DGNB"
)

function Get-ManualIndexPath {
    param([string]$TypedPath)
    $parts = $TypedPath -split "/", 2
    return Join-Path $manualRoot (Join-Path $parts[0] (Join-Path $parts[1] "index.md"))
}

function Read-Title {
    param([string]$Path, [string]$Fallback)
    if (-not (Test-Path -LiteralPath $Path)) {
        return $Fallback
    }
    foreach ($line in Get-Content -LiteralPath $Path -TotalCount 40) {
        if ($line -match '^title:\s*"?([^"]+)"?\s*$') {
            return $matches[1]
        }
    }
    foreach ($line in Get-Content -LiteralPath $Path -TotalCount 80) {
        if ($line -match '^#\s+(.+)$') {
            return $matches[1]
        }
    }
    return $Fallback
}

function New-Proposal {
    param(
        [string]$TypedPath,
        [string]$ProposalClass,
        [string]$RecommendedHandling,
        [string]$PossibleTargets,
        [string]$Reason
    )

    $indexPath = Get-ManualIndexPath $TypedPath
    [PSCustomObject]@{
        typed_path = $TypedPath
        title = Read-Title -Path $indexPath -Fallback (($TypedPath -split "/", 2)[1])
        proposal_class = $ProposalClass
        recommended_handling = $RecommendedHandling
        possible_final_targets = $PossibleTargets
        reason = $Reason
        source_index = if (Test-Path -LiteralPath $indexPath) { $indexPath.Substring($root.Length + 1) -replace "\\", "/" } else { "" }
    }
}

$proposals = foreach ($node in $nodes) {
    switch ($node) {
        "bauteiltyp/Holzrahmenelement" {
            New-Proposal $node "system_vs_component" "defer_until_source_context" "bausystem/Holzrahmenbau or bauteiltyp/Wand or bauteiltyp/Platte_Paneel" "Can mean timber-frame building system or an individual wall/panel element."
        }
        "bauteiltyp/Treppenwange" {
            New-Proposal $node "component_subtype" "merge_or_exact_component_after_context" "bauteiltyp/Treppe or bauteiltyp/Traeger" "Could be stair component or load-bearing stringer; function decides target."
        }
        "datenmodell/Gebaeuderessourcenpass" {
            New-Proposal $node "model_document_tool_mixed" "clean_and_split_later" "datenmodell/Gebaeuderessourcenpass_Schema; software_digitaltool/Concular; akteur/Concular" "Type can be valid, but current content is a Concular profile, not a clean data model node."
        }
        "dokumenttyp/Gebaeuderessourcenpass" {
            New-Proposal $node "document_model_tool_mixed" "clean_and_split_later" "dokumenttyp/Gebaeuderessourcenpass; datenmodell/Gebaeuderessourcenpass_Schema; software_digitaltool/Madaster" "Document type is valid, but current content mixes Madaster/DGNB/source profiles."
        }
        "fuegung_verbindung/Beton_Fertigteile_Verbindungen" {
            New-Proposal $node "connection_overview" "do_not_import_as_atomic_connection" "methode/Verbindungen_im_Betonfertigteilbau or atomic fuegung_verbindung/*" "Material/system-specific overview, not one connection principle."
        }
        "fuegung_verbindung/Composite_Verbindungen" {
            New-Proposal $node "connection_overview" "do_not_import_as_atomic_connection" "methode/Verbindungen_im_Verbundbau or atomic fuegung_verbindung/*" "Composite connection overview belongs to method/how unless split into atomic connection types."
        }
        "fuegung_verbindung/Holz_Verbindungen" {
            New-Proposal $node "connection_overview" "do_not_import_as_atomic_connection" "methode/Verbindungen_im_Holzbau or atomic fuegung_verbindung/*" "Timber connection overview belongs to method/how unless split into screws, plugs, glue, etc."
        }
        "fuegung_verbindung/Stahl_Verbindungen" {
            New-Proposal $node "connection_overview" "do_not_import_as_atomic_connection" "methode/Verbindungen_im_Stahlbau or atomic fuegung_verbindung/*" "Steel connection overview belongs to method/how unless split into welds, bolts, clamps, etc."
        }
        "fuegung_verbindung/Stahlseil" {
            New-Proposal $node "wrong_entity_component_material" "defer_until_component_knot_decision" "bauteiltyp/Zugglied_Seil or material/Stahl" "A steel cable is usually a tension component/material fact, not a connection principle."
        }
        "reuse_strategie/Temporaerer_Wiedereinbau" {
            New-Proposal $node "strategy_status_overlap" "defer_until_strategy_status_rule" "reuse_einsatzstatus/Temporaer plus reuse_strategie/Direkte_Wiederverwendung if applicable" "Temporary reuse is status-like and may also be a strategy pattern; avoid double counting."
        }
        "zertifizierung_bewertungssystem/DGNB" {
            New-Proposal $node "valid_system_mixed_content" "clean_content_then_possible_import" "zertifizierung_bewertungssystem/DGNB" "DGNB is a valid rating system, but mixed resource-pass content must be stripped before import."
        }
    }
}

$proposals |
    Sort-Object typed_path |
    Export-Csv -LiteralPath $proposalCsvPath -NoTypeInformation -Encoding UTF8

$byClass = $proposals |
    Group-Object proposal_class |
    Sort-Object Name |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$rows = $proposals |
    Sort-Object typed_path |
    ForEach-Object { "| $($_.typed_path) | $($_.recommended_handling) | $($_.possible_final_targets) |" }

$report = @()
$report += "# Phase 37 Content-Only Review Proposals"
$report += ""
$report += "## Scope"
$report += ""
$report += "Proposal-only pass for the 11 manual-review nodes with no held clean-edge rows. No manual decisions were written."
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/37_content_only_review_proposals.csv"
$report += ""
$report += "## By Proposal Class"
$report += ""
$report += "| class | nodes |"
$report += "|---|---:|"
$report += $byClass
$report += ""
$report += "## Node Proposals"
$report += ""
$report += "| node | recommended handling | possible final targets |"
$report += "|---|---|---|"
$report += $rows
$report += ""
$report += "## Rule"
$report += ""
$report += "These rows should stay out of _database until the final manual decision pass."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $proposalCsvPath"
Write-Output "Wrote $reportPath"
