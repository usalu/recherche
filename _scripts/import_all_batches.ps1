Set-Location e:\recherche
$base = "_neo4j\neo4j batch"
foreach ($n in 15,16,17,18,19,20) {
    $num = "{0:D3}" -f $n
    $dir = "$base\neo4j_batch_${num}_exports\neo4j_exports\batches\batch_${num}"
    Write-Host "=== Batch $num ===" -ForegroundColor Cyan
    $delta = "$dir\controlled_terms.delta.jsonl"
    if (Test-Path $delta) {
        Write-Host "  Importing delta..."
        python _scripts\import_jsonl_to_neo4j.py $delta
    }
    foreach ($f in Get-ChildItem "$dir\p_*.jsonl") {
        Write-Host "  Importing $($f.Name)..."
        python _scripts\import_jsonl_to_neo4j.py $f.FullName
    }
}
Write-Host "ALL DONE" -ForegroundColor Green
