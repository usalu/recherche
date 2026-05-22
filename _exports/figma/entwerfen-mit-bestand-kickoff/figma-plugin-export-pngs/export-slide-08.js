// Export only Slide 08 (often skipped when browsers block rapid multi-downloads)
const SLIDE = {
  number: 8,
  id: "281:41724",
  file: "slide-08-bauteilerfassung-eingabe-vs-import.png",
};

figma.showUI(
  `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body><p id="s">Exporting…</p><script>
onmessage=(e)=>{const m=e.data.pluginMessage;if(m&&m.type==='save'){const b=new Blob([new Uint8Array(m.bytes)],{type:'image/png'});const a=document.createElement('a');a.href=URL.createObjectURL(b);a.download=m.name;a.click();document.getElementById('s').textContent='Saved '+m.name;}}
</script></body></html>`,
  { width: 360, height: 100 }
);

(async () => {
  const node = await figma.getNodeByIdAsync(SLIDE.id);
  if (!node || !("exportAsync" in node)) {
    figma.notify("Slide 08 node not found: " + SLIDE.id);
    figma.closePlugin();
    return;
  }
  const bytes = await node.exportAsync({
    format: "PNG",
    constraint: { type: "SCALE", value: 2 },
  });
  figma.ui.postMessage({ type: "save", name: SLIDE.file, bytes: Array.from(bytes) });
  figma.notify("Downloaded " + SLIDE.file);
})();
