$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$cleanEdgesPath = Join-Path $root "_database/_edges/clean_confirmed_edges.csv"
$edgeReviewPath = Join-Path $root "_database/_edges/clean_edge_review_queue.csv"
$proposalCsvPath = Join-Path $root "_migration/34_second_manual_batch_edge_proposals.csv"
$reportPath = Join-Path $root "_migration/34_Second_Manual_Batch_Proposals.md"

$batchTargets = @(
    "bauteiltyp/Fliese",
    "bauteiltyp/Kueche",
    "bauteiltyp/Landschaftselement",
    "bauteiltyp/Bruestung",
    "bauteiltyp/Kern"
)

function Normalize-Text {
    param([string]$Value)
    if ([string]::IsNullOrWhiteSpace($Value)) {
        return ""
    }
    return $Value.ToLowerInvariant()
}

function New-Proposal {
    param(
        [string]$Action,
        [string]$Target,
        [string]$Relation,
        [string]$Confidence,
        [string]$Note
    )
    return [PSCustomObject]@{
        proposed_action = $Action
        proposed_target = $Target
        proposed_relation = $Relation
        proposal_confidence = $Confidence
        reviewer_note = $Note
    }
}

function Suggest-EdgeDecision {
    param([object]$Edge, [array]$ExistingEdges)

    $target = $Edge.target
    $raw = Normalize-Text $Edge.raw_label
    $existing = ($ExistingEdges -join "; ")

    if ($target -eq "bauteiltyp/Fliese") {
        if ($raw -match "austern") {
            return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Oyster shell tile is unusual material/product; source context needed before creating a material or component knot."
        }
        if ($raw -match "wand") {
            return New-Proposal "candidate_split" "bauteiltyp/Wand; material/Keramik" "has_bauteiltyp; uses_material" "REVIEW" "Wall tile context; verify whether material is ceramic/fayence or another surface material."
        }
        if ($raw -match "teppich|textile|faser") {
            return New-Proposal "candidate_split" "bauteiltyp/Boden; material/Textil" "has_bauteiltyp; uses_material" "REVIEW" "Carpet/textile tile is floor finish plus textile material, not generic Fliese."
        }
        if ($raw -match "dachziegel|roof tiles|dachfliesen") {
            return New-Proposal "candidate_split" "bauteiltyp/Dach; material/Ziegel" "has_bauteiltyp; uses_material" "REVIEW" "Roof tile belongs to roof context and brick/clay material; not generic tile."
        }
        if ($raw -match "boden|terrassen|pflaster|terrazzo") {
            return New-Proposal "candidate_move_or_split" "bauteiltyp/Boden" "has_bauteiltyp" "REVIEW" "Floor/terrace/paving context; material must be checked from source."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Fliese is too broad without wall/floor/roof/material context."
    }

    if ($target -eq "bauteiltyp/Kueche") {
        if ($raw -match "arbeitsplatte|arbeitsflächen|arbeitsflaechen|counter|schalter") {
            return New-Proposal "candidate_move" "bauteiltyp/Festes_Einbauteil" "has_bauteiltyp" "REVIEW" "Countertop/counter is fixed fit-out rather than the category Kueche."
        }
        if ($raw -match "küche|kueche|küchen|kuechen") {
            return New-Proposal "candidate_move" "bauteiltyp/Festes_Einbauteil" "has_bauteiltyp" "REVIEW" "Kitchen unit is fixed fit-out unless source treats it as loose furniture or non-direct reuse."
        }
        if ($raw -match "tga|solar") {
            return New-Proposal "candidate_split" "bauteiltyp/Technik_TGA; bauteiltyp/Festes_Einbauteil; bauteiltyp/PV_Anlage" "has_bauteiltyp" "REVIEW" "Mixed kitchen/TGA/solar label; split only after source check."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Kitchen-like label needs fit-out vs furniture vs equipment decision."
    }

    if ($target -eq "bauteiltyp/Landschaftselement") {
        if ($raw -match "parkett") {
            return New-Proposal "candidate_split" "bauteiltyp/Boden; material/Holz" "has_bauteiltyp; uses_material" "REVIEW" "Parkett is floor component plus wood material, not landscape element."
        }
        if ($raw -match "boden|decken") {
            return New-Proposal "candidate_move_or_split" "bauteiltyp/Boden; bauteiltyp/Decke" "has_bauteiltyp" "REVIEW" "Raw label points to floor/slab components; source must decide actual object."
        }
        if ($raw -match "fahrrad|pflanz|baum|bäume|baeume|park|außenraum|aussenraum|skate|landscape") {
            return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Outdoor/landscape object is outside the current clean component scope; consider future outdoor/infrastructure ontology."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Landscape element needs object/context decision."
    }

    if ($target -eq "bauteiltyp/Bruestung") {
        if ($raw -match "geländer|gelaender|balustrad") {
            return New-Proposal "candidate_move" "bauteiltyp/Gelaender" "has_bauteiltyp" "CONFIDENT_IF_SOURCE_CLEAR" "Guardrail/balustrade should normalize to Gelaender."
        }
        if ($raw -match "gitterrost") {
            return New-Proposal "candidate_split" "bauteiltyp/Gitterrost; bauteiltyp/Gelaender" "has_bauteiltyp" "REVIEW" "Could be grating used as guardrail; verify component function."
        }
        if ($raw -match "parapet|brüstung|bruestung") {
            return New-Proposal "candidate_move_or_review" "bauteiltyp/Gelaender or bauteiltyp/Fassade" "has_bauteiltyp" "REVIEW" "Brüstung/parapet can be guardrail, facade edge, or wall element."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Brüstung needs functional context."
    }

    if ($target -eq "bauteiltyp/Kern") {
        if ($raw -match "hohlkörperdecken|hohlkoerperdecken|hollow") {
            return New-Proposal "candidate_move" "bauteiltyp/Decke" "has_bauteiltyp" "CONFIDENT_IF_SOURCE_CLEAR" "Hollow-core slabs are deck/slab elements, not Kern."
        }
        if ($raw -match "fassadenbekleidung") {
            return New-Proposal "candidate_move" "bauteiltyp/Fassade" "has_bauteiltyp" "CONFIDENT_IF_SOURCE_CLEAR" "Facade cladding of a core is facade component, not core component."
        }
        if ($raw -match "ckenlinks") {
            return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Bridge links to core are connection/object-context, not a clean Kern component."
        }
        if ($raw -match "stahlprofile") {
            return New-Proposal "candidate_split" "tragwerksprinzip/Wand_Kern_Tragwerk; bauteiltyp/Traeger" "has_tragwerksprinzip; has_bauteiltyp" "REVIEW" "Core context plus steel profiles; derive structural principle and precise member only after source check."
        }
        if ($raw -match "kern") {
            return New-Proposal "candidate_move_or_review" "tragwerksprinzip/Wand_Kern_Tragwerk" "has_tragwerksprinzip" "REVIEW" "Core context is structural principle/object context, not a component type."
        }
        return New-Proposal "keep_review" "" "" "REVIEW_REQUIRED" "Kern is usually structural/object-scale, not bauteiltyp."
    }

    return New-Proposal "not_in_second_batch" "" "" "REVIEW_REQUIRED" "Target is outside second manual batch."
}

$cleanEdges = @(Import-Csv -LiteralPath $cleanEdgesPath)
$rows = @(Import-Csv -LiteralPath $edgeReviewPath | Where-Object { $batchTargets -contains $_.target })

$proposals = foreach ($row in $rows) {
    $existing = @($cleanEdges |
        Where-Object { $_.source -eq $row.source } |
        ForEach-Object { "$($_.relation)->$($_.target)" } |
        Select-Object -Unique |
        Sort-Object)
    $proposal = Suggest-EdgeDecision -Edge $row -ExistingEdges $existing
    [PSCustomObject]@{
        source = $row.source
        relation = $row.relation
        target = $row.target
        raw_label = $row.raw_label
        existing_clean_edges = ($existing -join "; ")
        legacy_path = $row.legacy_path
        proposed_action = $proposal.proposed_action
        proposed_target = $proposal.proposed_target
        proposed_relation = $proposal.proposed_relation
        proposal_confidence = $proposal.proposal_confidence
        reviewer_note = $proposal.reviewer_note
    }
}

$proposals |
    Sort-Object target, proposed_action, raw_label, source |
    Export-Csv -LiteralPath $proposalCsvPath -NoTypeInformation -Encoding UTF8

$summaryByTarget = $proposals |
    Group-Object target |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$summaryByAction = $proposals |
    Group-Object proposed_action |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$summaryByConfidence = $proposals |
    Group-Object proposal_confidence |
    Sort-Object Count -Descending |
    ForEach-Object { "| $($_.Name) | $($_.Count) |" }

$report = @()
$report += "# Phase 34 Second Manual Batch Proposals"
$report += ""
$report += "## Scope"
$report += ""
$report += "Proposal-only pass for the next five review targets. No manual decisions were written."
$report += ""
$report += "## Output"
$report += ""
$report += "- _migration/34_second_manual_batch_edge_proposals.csv"
$report += ""
$report += "## Counts"
$report += ""
$report += "- Proposed edge rows: $($proposals.Count)"
$report += ""
$report += "## By Target"
$report += ""
$report += "| target | rows |"
$report += "|---|---:|"
$report += $summaryByTarget
$report += ""
$report += "## By Proposed Action"
$report += ""
$report += "| action | rows |"
$report += "|---|---:|"
$report += $summaryByAction
$report += ""
$report += "## By Confidence"
$report += ""
$report += "| confidence | rows |"
$report += "|---|---:|"
$report += $summaryByConfidence
$report += ""
$report += "## Rule"
$report += ""
$report += "Do not write final decisions until the full manual-review package is prepared."

$report | Set-Content -LiteralPath $reportPath -Encoding UTF8

Write-Output "Wrote $proposalCsvPath"
Write-Output "Wrote $reportPath"
