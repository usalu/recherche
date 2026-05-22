// Run via figma-console MCP figma_execute after sync_slide11_from_markdown apply.
// Roboto Mono YAML syntax highlighting for Slide 11 pipeline cells.

const slide = await figma.getNodeByIdAsync('378:2208');
if (!slide) return { error: 'slide 378:2208 missing' };

function hex(h) {
  const c = h.replace('#', '');
  return {
    r: parseInt(c.slice(0, 2), 16) / 255,
    g: parseInt(c.slice(2, 4), 16) / 255,
    b: parseInt(c.slice(4, 6), 16) / 255,
  };
}

const PAL = {
  header: hex('2dd4bf'),
  key: hex('79c0ff'),
  keyTop: hex('56d4dd'),
  string: hex('a8ff60'),
  number: hex('f2cc60'),
  bool: hex('ff7b72'),
  punct: hex('6e7681'),
  indent: hex('484f58'),
  text: hex('e6edf3'),
  muted: hex('9fb3c8'),
  list: hex('d2a8ff'),
};

let mono = { family: 'Roboto Mono', style: 'Regular' };
let monoMed = { family: 'Roboto Mono', style: 'Medium' };
let monoBold = { family: 'Roboto Mono', style: 'Bold' };
try {
  await figma.loadFontAsync(mono);
  await figma.loadFontAsync(monoMed);
  await figma.loadFontAsync(monoBold);
} catch {
  mono = { family: 'Inter', style: 'Regular' };
  monoMed = { family: 'Inter', style: 'Semi Bold' };
  monoBold = { family: 'Inter', style: 'Bold' };
  await figma.loadFontAsync(mono);
  await figma.loadFontAsync(monoMed);
  await figma.loadFontAsync(monoBold);
}

function paint(textNode, start, end, color, font, size) {
  if (end <= start) return;
  textNode.setRangeFills(start, end, [{ type: 'SOLID', color }]);
  textNode.setRangeFontName(start, end, font);
  if (size) textNode.setRangeFontSize(start, end, size);
}

function classifyValue(raw) {
  const v = raw.trim();
  if (!v) return 'empty';
  if ((v.startsWith('"') && v.endsWith('"')) || (v.startsWith("'") && v.endsWith("'")))
    return 'string';
  if (/^-?\d+(\.\d+)?$/.test(v)) return 'number';
  if (/^-?\d+(\.\d+)?-/.test(v) && v.includes('-')) return 'range';
  if (['true', 'false', 'null'].includes(v)) return 'bool';
  if (/^[a-z0-9_]+$/.test(v)) return 'token';
  return 'text';
}

function styleYamlText(textNode) {
  const chars = textNode.characters;
  textNode.fontName = mono;
  textNode.fontSize = 11;
  textNode.lineHeight = { unit: 'PIXELS', value: 17 };
  textNode.fills = [{ type: 'SOLID', color: PAL.text }];

  const lines = chars.split('\n');
  let off = 0;
  for (const line of lines) {
    const start = off;
    const end = start + line.length;

    if (line.startsWith('## ')) {
      paint(textNode, start, end, PAL.header, monoBold, 14);
    } else if (/^\s*-\s/.test(line)) {
      const m = line.match(/^(\s*)(-\s)(.*)$/);
      if (m) {
        const i0 = start;
        const iDash = i0 + m[1].length;
        const iVal = iDash + m[2].length;
        if (m[1]) paint(textNode, i0, iDash, PAL.indent, mono);
        paint(textNode, iDash, iVal, PAL.punct, mono);
        const val = m[3];
        const kind = classifyValue(val);
        const col =
          kind === 'token' ? PAL.keyTop : kind === 'number' ? PAL.number : kind === 'string' ? PAL.string : PAL.list;
        paint(textNode, iVal, end, col, mono);
      }
    } else if (line.includes(':')) {
      const m = line.match(/^(\s*)([A-Za-z0-9_]+)(\s*:\s*)(.*)$/);
      if (m) {
        const i0 = start;
        const iKey = i0 + m[1].length;
        const iColon = iKey + m[2].length;
        const iVal = iColon + m[3].length;
        if (m[1]) paint(textNode, i0, iKey, PAL.indent, mono);
        paint(textNode, iKey, iColon, PAL.key, monoMed);
        paint(textNode, iColon, iVal, PAL.punct, mono);
        const val = m[4];
        if (val.length) {
          const kind = classifyValue(val);
          let col = PAL.text;
          if (kind === 'number' || kind === 'range') col = PAL.number;
          else if (kind === 'string') col = PAL.string;
          else if (kind === 'bool') col = PAL.bool;
          else if (kind === 'token') col = PAL.keyTop;
          else col = PAL.muted;
          paint(textNode, iVal, end, col, mono);
        }
      } else {
        paint(textNode, start, end, PAL.muted, mono);
      }
    } else if (line.trim()) {
      paint(textNode, start, end, PAL.muted, mono);
    }

    off = end + 1;
  }
}

const panel = hex('0d1117');
const panelBorder = hex('30363d');
let count = 0;
for (const frame of slide.children.filter((n) => n.name.startsWith('Cell_'))) {
  frame.fills = [{ type: 'SOLID', color: panel }];
  frame.strokes = [{ type: 'SOLID', color: panelBorder }];
  frame.strokeWeight = 1;
  frame.cornerRadius = 6;
  const text = frame.findOne((n) => n.type === 'TEXT');
  if (!text) continue;
  styleYamlText(text);
  const pad = 14;
  text.resize(frame.width - pad * 2, text.height);
  frame.resize(frame.width, Math.max(frame.height, text.height + pad * 2));
  count++;
}

return { styledCells: count, font: mono.family };
