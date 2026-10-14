// Turns a design definition into a full-page SVG.
import { setMode, isBW, zoneGuide, samplePrint, paintDefs, title, text, fillLine, INK } from './lib.mjs';

export const SIZE = { portrait: [850, 1100], landscape: [1100, 850] };

// design: { id, orient, title, titleSize, titleY, caption, captionY, nameY,
//           zones:[], back(ctx), front(ctx), finish(ctx) (sample only) }
export function renderDesign(d, { mode = 'color', sample = false } = {}) {
  setMode(mode);
  const [W, H] = SIZE[d.orient || 'portrait'];
  const ctx = { W, H, cx: W / 2, fields: [], sample, d };
  const zones = (d.zones || []).map((z) => ({ ...z }));
  ctx.zones = zones;
  let body = '';
  if (d.back) body += d.back(ctx);
  if (sample) body += zones.map((z) => samplePrint(z)).join('');
  else body += zones.map(zoneGuide).join('');
  if (d.front) body += d.front(ctx);
  if (sample && d.finish) body += d.finish(ctx);
  if (d.title) {
    const ty = d.titleY ?? (d.orient === 'landscape' ? 120 : 150);
    const opt = { size: d.titleSize || 72, font: d.titleFont || 'title', weight: d.titleFont ? 400 : 900 };
    body += title(ctx.cx, ty, d.title, opt);
    if (d.title2) body += title(ctx.cx, ty + opt.size * 1.02, d.title2, opt);
  }
  if (d.caption) {
    const cy = d.captionY ?? (H - 165);
    const lines = Array.isArray(d.caption) ? d.caption : [d.caption];
    lines.forEach((l, i) => { body += text(ctx.cx, cy + i * (d.captionSize || 40) * 1.15, l, { size: d.captionSize || 40, font: 'hand' }); });
  }
  if (d.nameLine !== false) body += fillLine(ctx, ctx.cx, d.nameY ?? (H - 68), d.nameFields);
  if (d.extra) body += d.extra(ctx);
  const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${W} ${H}" width="${W}" height="${H}">
<defs>${sample ? paintDefs() : ''}</defs><rect width="${W}" height="${H}" fill="#fff"/>${body}</svg>`;
  return { svg, fields: ctx.fields, W, H };
}

export const FONT_CSS = (base) => `
@font-face{font-family:'Grandstander';font-weight:500;src:url(${base}/Grandstander-500.ttf)}
@font-face{font-family:'Grandstander';font-weight:700;src:url(${base}/Grandstander-700.ttf)}
@font-face{font-family:'Grandstander';font-weight:900;src:url(${base}/Grandstander-900.ttf)}
@font-face{font-family:'Patrick Hand';font-weight:400;src:url(${base}/PatrickHand-400.ttf)}
@font-face{font-family:'Creepster';font-weight:400;src:url(${base}/Creepster-400.ttf)}
@font-face{font-family:'Fredoka';font-weight:400;src:url(${base}/Fredoka-400.ttf)}
@font-face{font-family:'Fredoka';font-weight:600;src:url(${base}/Fredoka-600.ttf)}
@font-face{font-family:'Fredoka';font-weight:700;src:url(${base}/Fredoka-700.ttf)}
`;
