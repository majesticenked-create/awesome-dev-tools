// Quick PNG previews: node src/preview.mjs [id ...] -> build/preview/<id>-{color,bw,sample}.png
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import { DESIGNS } from './designs.mjs';
import { renderDesign, FONT_CSS } from './page.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = `${ROOT}/build/preview`;
mkdirSync(OUT, { recursive: true });
const ids = process.argv.slice(2);
const list = ids.length ? DESIGNS.filter((d) => ids.includes(d.id)) : DESIGNS;
const browser = await chromium.launch();
const page = await browser.newPage({ deviceScaleFactor: 1 });
for (const d of list) {
  for (const [mode, sample] of [['color', true], ['color', false], ['bw', false]]) {
    const { svg, W, H } = renderDesign(d, { mode, sample });
    await page.setViewportSize({ width: W, height: H });
    writeFileSync(`${OUT}/_tmp.html`, `<html><head><style>${FONT_CSS('../../fonts')} body{margin:0}</style></head><body>${svg}</body></html>`);
    await page.goto(`file://${OUT}/_tmp.html`);
    await page.evaluate(() => document.fonts.ready);
    const tag = sample ? 'sample' : mode;
    await page.screenshot({ path: `${OUT}/${d.id}-${tag}.png` });
  }
  console.log('ok', d.id);
}
await browser.close();
