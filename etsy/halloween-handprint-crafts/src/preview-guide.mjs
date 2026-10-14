import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { writeFileSync, mkdirSync } from 'node:fs';
import { guidePages } from './bonus.mjs';
import { FONT_CSS } from './page.mjs';
const OUT = new URL('../build/preview', import.meta.url).pathname; mkdirSync(OUT, { recursive: true });
const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 850, height: 1100 } });
const pages = guidePages();
for (const [i, pg] of pages.entries()) {
  writeFileSync(`${OUT}/_g.html`, `<html><head><style>${FONT_CSS('../../fonts')} body{margin:0}</style></head><body>${pg.svg}</body></html>`);
  await p.goto(`file://${OUT}/_g.html`); await p.evaluate(() => document.fonts.ready);
  await p.screenshot({ path: `${OUT}/guide-${i + 1}.png` });
}
await b.close(); console.log(pages.length, 'pages');
