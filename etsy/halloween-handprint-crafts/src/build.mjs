// Renders every page to its own PDF (so portrait and landscape pages can mix)
// and writes build/pages/manifest.json for assemble.py, which merges the
// pages, adds fillable name/age/year fields and writes the final files.
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { mkdirSync, writeFileSync, rmSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DESIGNS } from './designs.mjs';
import { renderDesign, FONT_CSS } from './page.mjs';
import { guidePages } from './bonus.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = `${ROOT}/build/pages`;
rmSync(OUT, { recursive: true, force: true });
mkdirSync(OUT, { recursive: true });

// Paper sizes in points.
const PAPER = { letter: [612, 792], a4: [595.28, 841.89] };

// Fit a W x H (units of 1/100 in) design onto paper, centred.
function placement(W, H, paper) {
  const landscape = W > H;
  let [pw, ph] = PAPER[paper];
  if (landscape) [pw, ph] = [ph, pw];
  const s = Math.min(pw / (W * 0.72), ph / (H * 0.72));
  const w = W * 0.72 * s, h = H * 0.72 * s;
  return { pw, ph, s: 0.72 * s, ox: (pw - w) / 2, oy: (ph - h) / 2, w, h };
}

const browser = await chromium.launch();
const page = await browser.newPage();
const manifest = {};

async function renderPdf(svg, pl, file) {
  const html = `<html><head><style>${FONT_CSS('../../fonts')}
    @page{size:${pl.pw}pt ${pl.ph}pt;margin:0} html,body{margin:0;padding:0}
    .p{position:relative;width:${pl.pw}pt;height:${pl.ph}pt;overflow:hidden}
    .p svg{position:absolute;left:${pl.ox}pt;top:${pl.oy}pt;width:${pl.w}pt;height:${pl.h}pt}</style></head>
    <body><div class="p">${svg}</div></body></html>`;
  writeFileSync(`${OUT}/_page.html`, html);
  await page.goto(`file://${OUT}/_page.html`);
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: file, width: `${pl.pw / 72}in`, height: `${pl.ph / 72}in`, printBackground: true, margin: { top: 0, right: 0, bottom: 0, left: 0 }, preferCSSPageSize: true });
}

for (const mode of ['color', 'bw']) {
  for (const paper of ['letter', 'a4']) {
    const key = `${mode}-${paper}`;
    manifest[key] = [];
    for (const [i, d] of DESIGNS.entries()) {
      const { svg, fields, W, H } = renderDesign(d, { mode });
      const pl = placement(W, H, paper);
      const file = `${OUT}/${key}-${String(i + 1).padStart(2, '0')}.pdf`;
      await renderPdf(svg, pl, file);
      manifest[key].push({ file, id: d.id, fields, pl });
    }
    console.log('rendered', key);
  }
}
manifest.guide = [];
for (const [i, g] of guidePages().entries()) {
  const pl = placement(850, 1100, 'letter');
  const file = `${OUT}/guide-${String(i + 1).padStart(2, '0')}.pdf`;
  await renderPdf(g.svg, pl, file);
  manifest.guide.push({ file, id: `guide-${i + 1}`, fields: g.fields, pl });
}
console.log('rendered guide');
writeFileSync(`${OUT}/manifest.json`, JSON.stringify(manifest, null, 1));
await browser.close();
