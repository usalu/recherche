const SLIDES = [
  { number: 8, id: "281:41724", file: "slide-08-bauteilerfassung-eingabe-vs-import.png" },
  { number: 9, id: "38:7551", file: "slide-09-bauteilkatalog-datenstruktur.png" },
  { number: 10, id: "288:43374", file: "slide-10-backup-pre-redesign.png" },
  { number: 11, id: "196:17007", file: "slide-11-typology-view.png" },
  { number: 12, id: "192:16039", file: "slide-12-filter-sidebar-spec.png" },
  { number: 13, id: "199:24517", file: "slide-13-typology-view-working-copy.png" },
];

figma.showUI(
  `<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
body{font:13px/1.4 Segoe UI,sans-serif;margin:16px;color:#111}
#log{white-space:pre-wrap;margin-top:12px;color:#444;max-height:140px;overflow:auto}
button{margin:8px 8px 0 0;padding:8px 12px}
</style>
</head><body>
<strong>Export Kickoff slides</strong>
<div id="log">Preparing…</div>
<button id="all" hidden>Download all again</button>
<button id="missing" hidden>Download missing only</button>
<script>
const log=document.getElementById('log');
const allBtn=document.getElementById('all');
const missingBtn=document.getElementById('missing');
let lastItems=[];

function sleep(ms){return new Promise(r=>setTimeout(r,ms));}

async function downloadItems(items, label){
  log.textContent += '\\n' + label + '\\n';
  for (const item of items) {
    const blob=new Blob([new Uint8Array(item.bytes)],{type:'image/png'});
    const a=document.createElement('a');
    a.href=URL.createObjectURL(blob);
    a.download=item.name;
    a.click();
    URL.revokeObjectURL(a.href);
    log.textContent += '  saved ' + item.name + '\\n';
    await sleep(700);
  }
}

allBtn.onclick=()=>downloadItems(lastItems,'Re-download all:');
missingBtn.onclick=()=>{
  const only=lastItems.filter(i=>i.missing);
  if(!only.length){log.textContent+='\\nNo missing slides reported.\\n';return;}
  downloadItems(only,'Missing slides:');
};

onmessage=async(event)=>{
  const msg=event.data.pluginMessage;
  if(!msg)return;
  if(msg.type==='log')log.textContent+=msg.text+'\\n';
  if(msg.type==='exports'){
    lastItems=msg.items;
    const missing=msg.items.filter(i=>i.missing);
    await downloadItems(msg.items.filter(i=>!i.missing),'Downloaded:');
    if(missing.length){
      log.textContent+='\\nSkipped (node not found): '+missing.map(m=>m.name).join(', ')+'\\n';
      missingBtn.hidden=false;
    }
    allBtn.hidden=false;
  }
  if(msg.type==='done'){
    log.textContent+='\\nDone: '+msg.exported+'/'+msg.total+' exported.\\n';
    if(msg.exported<msg.total)log.textContent+='Use "Download missing only" or re-run for failed slides.\\n';
  }
};
</script></body></html>`,
  { width: 460, height: 280 }
);

(async () => {
  const items = [];
  let exported = 0;
  for (const slide of SLIDES) {
    const node = await figma.getNodeByIdAsync(slide.id);
    if (!node || !("exportAsync" in node)) {
      figma.ui.postMessage({
        type: "log",
        text: "MISSING NODE: " + slide.file + " (" + slide.id + ")",
      });
      items.push({ name: slide.file, bytes: [], missing: true, number: slide.number });
      continue;
    }
    figma.ui.postMessage({ type: "log", text: "Exporting slide " + slide.number + "…" });
    const bytes = await node.exportAsync({
      format: "PNG",
      constraint: { type: "SCALE", value: 2 },
    });
    items.push({ name: slide.file, bytes: Array.from(bytes), missing: false, number: slide.number });
    exported += 1;
    figma.ui.postMessage({ type: "log", text: "Ready: " + slide.file + " (" + bytes.length + " bytes)" });
  }
  figma.ui.postMessage({ type: "exports", items });
  figma.ui.postMessage({ type: "done", exported, total: SLIDES.length });
})();
