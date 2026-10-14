// Etsy listing images (2400 x 2400). All artwork is drawn here — no stock photos.
//   node src/mockups.mjs  ->  dist/listing-images/*.jpg (via PIL convert step)
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { mkdirSync, writeFileSync } from 'node:fs';
import { resolve, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';
import * as L from './lib.mjs';
import { DESIGNS, byId } from './designs.mjs';
import { renderDesign, FONT_CSS } from './page.mjs';
import { guidePages } from './bonus.mjs';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const OUT = `${ROOT}/build/listing`;
mkdirSync(OUT, { recursive: true });
const N = DESIGNS.length;

const C = { ink: '#2B2530', orange: '#F5893A', purple: '#8B68C8', cream: '#FBF4EA', night: '#2F2B52', green: '#86C34A' };
const sample = (id) => renderDesign(byId[id], { sample: true }).svg;
const blank = (id, mode = 'color') => renderDesign(byId[id], { mode }).svg;
// A "sheet of paper" holding an svg page. w in px, rot in deg.
const sheet = (svg, { x, y, w, rot = 0, shadow = true, landscape = false, z = 1 }) => {
  const h = landscape ? w * (850 / 1100) : w * (1100 / 850);
  return `<div style="position:absolute;left:${x}px;top:${y}px;width:${w}px;height:${h}px;transform:rotate(${rot}deg);z-index:${z};background:#fff;${shadow ? 'box-shadow:0 18px 40px rgba(40,30,50,.22),0 3px 8px rgba(40,30,50,.12);' : ''}">${svg.replace(/width="\d+" height="\d+"/, 'width="100%" height="100%"')}</div>`;
};
const confetti = (seed = 1, n = 40) => {
  let r = seed * 9301 + 49297; const R = () => ((r = (r * 9301 + 49297) % 233280) / 233280);
  L.setMode('color');
  let s = '';
  for (let i = 0; i < n; i++) {
    const x = R() * 2400, y = R() * 2400, sz = 10 + R() * 22, c = ['orange', 'purple', 'yellow', 'green'][i % 4];
    s += i % 3 ? L.star(x, y, sz, c, R() * 40) : `<circle cx="${x}" cy="${y}" r="${sz * 0.45}" fill="${L.pal(c)}"/>`;
  }
  return `<svg style="position:absolute;inset:0;opacity:.55" width="2400" height="2400" viewBox="0 0 2400 2400">${s}</svg>`;
};
const H = (txt, { x = 1200, y, size = 150, color = C.ink, font = 'Grandstander', weight = 900, align = 'center', stroke = 0, w = 2200 } = {}) =>
  `<div style="position:absolute;left:${x - w / 2}px;top:${y}px;width:${w}px;text-align:${align};font-family:'${font}';font-weight:${weight};font-size:${size}px;line-height:1.05;color:${color};${stroke ? `-webkit-text-stroke:${stroke}px #fff;paint-order:stroke fill;` : ''}">${txt}</div>`;
const pill = (txt, { x, y, bg = C.orange, color = '#fff', size = 54, w }) =>
  `<div style="position:absolute;left:${x}px;top:${y}px;${w ? `width:${w}px;` : ''}padding:22px 46px;border-radius:999px;background:${bg};color:${color};font-family:'Fredoka';font-weight:700;font-size:${size}px;text-align:center;white-space:nowrap">${txt}</div>`;
const badge = (big, small, { x, y, bg = C.purple, r = 170 }) =>
  `<div style="position:absolute;left:${x - r}px;top:${y - r}px;width:${2 * r}px;height:${2 * r}px;border-radius:50%;background:${bg};color:#fff;display:flex;flex-direction:column;align-items:center;justify-content:center;font-family:'Grandstander';font-weight:900;box-shadow:0 10px 24px rgba(0,0,0,.18);border:8px solid #fff">
    <div style="font-size:${r * 0.62}px;line-height:1">${big}</div><div style="font-family:'Fredoka';font-weight:600;font-size:${r * 0.2}px;line-height:1.1;text-align:center;padding:0 20px">${small}</div></div>`;
const page = (body, bg = C.cream) => `<html><head><style>${FONT_CSS('../../fonts')}
  body{margin:0;width:2400px;height:2400px;position:relative;overflow:hidden;background:${bg}}</style></head><body>${body}</body></html>`;

// Drawn interior scene pieces for the framed mockups.
function wallScene(inner) {
  L.setMode('color');
  const deco = `<svg style="position:absolute;inset:0" width="2400" height="2400" viewBox="0 0 2400 2400">
    <defs><linearGradient id="wall" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#EFE7DE"/><stop offset="1" stop-color="#E6DBCF"/></linearGradient>
    <linearGradient id="shelf" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#D9B98F"/><stop offset="1" stop-color="#C49C6C"/></linearGradient>
    <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="#FFD58A" stop-opacity=".55"/><stop offset="1" stop-color="#FFD58A" stop-opacity="0"/></radialGradient></defs>
    <rect width="2400" height="2400" fill="url(#wall)"/>
    <rect y="1960" width="2400" height="440" fill="url(#shelf)"/><rect y="1960" width="2400" height="16" fill="#B88F60"/>
    <path d="M0,2060 C600,2050 1200,2080 2400,2050 M0,2200 C700,2190 1500,2220 2400,2200" stroke="#B68A5A" stroke-width="5" fill="none" opacity=".5"/>
    <circle cx="2030" cy="1700" r="360" fill="url(#glow)"/>
    <g transform="translate(2030 1830) scale(7.2)">${L.pumpkin(0, 0, 1, { faceKind: 'jack' })}</g>
    <g transform="translate(380 1890)"><rect x="-60" y="-200" width="120" height="270" rx="14" fill="#F8F2E8" stroke="#D8CCBC" stroke-width="5"/>
      <path d="M0,-200 v-30" stroke="${C.ink}" stroke-width="6"/><path d="M0,-300 C26,-262 16,-236 0,-228 C-16,-236 -26,-262 0,-300 Z" fill="#FFC14D"/></g>
    <g transform="translate(270 1925) scale(3.4)">${L.pumpkin(0, 0, 1, { faceKind: 'none', color: 'cream' })}</g>
  </svg>`;
  return deco + inner;
}
function frame(svg, { x, y, w, landscape = false, mat = 60 }) {
  const ih = landscape ? w * (850 / 1100) : w * (1100 / 850);
  const b = 54;
  return `<div style="position:absolute;left:${x - b - mat}px;top:${y - b - mat}px;width:${w + 2 * mat}px;height:${ih + 2 * mat}px;border:${b}px solid #C9A274;border-color:#D6B184 #BC9263 #B08657 #CBA577;background:#FDFBF8;box-shadow:0 30px 50px rgba(60,40,20,.28), inset 0 0 0 3px rgba(0,0,0,.06)">
    <div style="position:absolute;left:${mat}px;top:${mat}px;width:${w}px;height:${ih};box-shadow:inset 0 2px 6px rgba(0,0,0,.12)">${svg.replace(/width="\d+" height="\d+"/, `width="${w}" height="${ih}"`)}</div></div>`;
}

const IMAGES = {
  '01-hero': () => {
    let b = confetti(3);
    b += H('HALLOWEEN', { y: 90, size: 250, stroke: 0 });
    b += `<div style="position:absolute;left:250px;top:375px;width:1900px;padding:26px 0;background:${C.orange};color:#fff;text-align:center;font-family:'Grandstander';font-weight:900;font-size:96px;letter-spacing:2px;border-radius:24px">HANDPRINT &amp; FOOTPRINT ART</div>`;
    const picks = [['ghost-hand', 40, 650, -7], ['vampire-hand', 480, 600, -3], ['monster-hand', 920, 580, 0], ['owl-foot', 1360, 600, 3], ['pumpkin-hand', 1800, 650, 7]];
    picks.forEach(([id, x, y, r], i) => { b += sheet(sample(id), { x, y, w: 560, rot: r, z: i === 2 ? 5 : i % 2 ? 4 : 3 }); });
    b += `<div style="position:absolute;z-index:9;inset:0">` + badge(String(N), 'crafts included', { x: 290, y: 1440, bg: C.purple }) +
      badge('A4', '+ US Letter', { x: 2110, y: 1440, bg: C.orange, r: 160 }) + '</div>';
    b += H('hand · foot · fingerprint keepsakes', { y: 1700, size: 104, font: 'Fredoka', weight: 600, color: C.ink });
    b += pill('INSTANT DOWNLOAD · PRINT AT HOME', { x: 470, y: 1910, w: 1460, bg: C.night, size: 66 });
    b += H('color + ink-saver coloring versions · type-in names', { y: 2140, size: 62, font: 'Fredoka', weight: 400, color: '#6b6170' });
    return page(b);
  },
  '02-all-designs': () => {
    let b = H(`${N} Halloween Crafts Included`, { y: 70, size: 128 });
    b += H('15 handprint · 8 footprint · 7 fingerprint designs', { y: 225, size: 64, font: 'Fredoka', weight: 600, color: C.orange });
    const cols = 6, cw = 360, ch = 410, gx = 25, ox = (2400 - (cols * cw + (cols - 1) * gx)) / 2;
    DESIGNS.forEach((d, i) => {
      const c = i % cols, r = Math.floor(i / cols);
      const x = ox + c * (cw + gx), y = 345 + r * (ch + 3);
      const land = d.orient === 'landscape';
      const w = land ? cw - 10 : 300;
      const hh = land ? w * 850 / 1100 : w * 1100 / 850;
      b += sheet(sample(d.id), { x: x + (cw - w) / 2, y: y + (ch - 22 - hh) / 2, w, landscape: land });
    });
    return page(b, '#FFFBF5');
  },
  '03-framed-ghost': () => {
    let b = frame(sample('ghost-hand'), { x: 760, y: 300, w: 880 });
    b += pill('frame-ready keepsake', { x: 140, y: 140, bg: C.night, size: 58 });
    return page(wallScene(b));
  },
  '04-framed-pair': () => {
    let b = frame(sample('vampire-hand'), { x: 290, y: 520, w: 640 }) + frame(sample('trickortreat-feet'), { x: 1460, y: 520, w: 640 });
    L.setMode('color');
    b = `<svg style="position:absolute;left:0;top:0" width="2400" height="400" viewBox="0 0 850 140">${L.bunting(20, 830, 30, ['orange', 'purple', 'green', 'ink'], 30)}</svg>` + b;
    return page(wallScene(b));
  },
  '05-whats-included': () => {
    let b = confetti(8, 24) + H("What's Included", { y: 90, size: 150 });
    b += H('5 instant-download PDF files', { y: 270, size: 70, font: 'Fredoka', weight: 600, color: C.orange });
    const files = [
      ['START HERE', 'guide + bonus pages', guidePages()[0].svg, C.night],
      ['COLOR', 'US Letter · 30 pages', sample('monster-hand'), C.orange],
      ['COLOR', 'A4 · 30 pages', sample('cat-hand'), C.orange],
      ['INK-SAVER', 'coloring · US Letter', blank('witch-hand', 'bw'), C.purple],
      ['INK-SAVER', 'coloring · A4', blank('spiders-finger', 'bw'), C.purple],
    ];
    files.forEach(([a, s, svg, col], i) => {
      const x = 110 + i * 445, y = 470;
      b += sheet(svg, { x: x + 18, y: y + 26, w: 330, rot: 3 }) + sheet(svg, { x, y, w: 370, z: 2 });
      b += `<div style="position:absolute;left:${x - 20}px;top:${y + 530}px;width:410px;text-align:center"><div style="display:inline-block;background:${col};color:#fff;font-family:'Grandstander';font-weight:900;font-size:50px;padding:10px 30px;border-radius:16px">${a}</div><div style="font-family:'Fredoka';font-weight:600;font-size:44px;color:${C.ink};margin-top:16px">${s}</div></div>`;
    });
    const bullets = ['30 designs: handprint, footprint &amp; fingerprint', 'type-in name · age · year fields', 'cut &amp; glue face pieces + 4 mini cards', 'how-to tips + visual design index'];
    b += `<div style="position:absolute;left:300px;top:1330px;width:1800px;background:#fff;border-radius:40px;padding:60px 80px;box-shadow:0 12px 30px rgba(0,0,0,.08);font-family:'Fredoka';font-size:66px;line-height:1.75;color:${C.ink}">${bullets.map((t) => `<div><span style="color:${C.orange}">✔</span>&nbsp; ${t}</div>`).join('')}</div>`;
    b += H('no physical item will be shipped', { y: 2220, size: 50, font: 'Fredoka', weight: 400, color: '#7a7080' });
    return page(b);
  },
  '06-two-versions': () => {
    let b = H('2 Versions of Every Design', { y: 90, size: 130 });
    b += sheet(blank('pumpkin-hand'), { x: 170, y: 420, w: 960, rot: -2 }) + sheet(blank('pumpkin-hand', 'bw'), { x: 1270, y: 420, w: 960, rot: 2 });
    b += pill('FULL COLOR', { x: 380, y: 1740, bg: C.orange, size: 72, w: 540 }) + pill('INK-SAVER + COLORING', { x: 1290, y: 1740, bg: C.purple, size: 72, w: 920 });
    b += H('Low on ink? Print the outline version and let kids color it in.', { y: 1960, size: 66, font: 'Fredoka', weight: 600 });
    b += H('Both come in US Letter (8.5×11 in) and A4.', { y: 2080, size: 60, font: 'Fredoka', weight: 400, color: '#6b6170' });
    return page(b, '#FFFBF5');
  },
  '07-features': () => {
    let b = confetti(5, 20) + H('Designed to Make It Easy', { y: 80, size: 128 });
    b += sheet(blank('ghost-hand'), { x: 160, y: 330, w: 1250 });
    // callouts pointing at the page
    const call = (n, t, s, x, y, ax, ay) => `<svg style="position:absolute;inset:0;z-index:4" width="2400" height="2400"><path d="M${x},${y + 70} C${(x + ax) / 2},${y + 70} ${(x + ax) / 2},${ay} ${ax},${ay}" stroke="${C.ink}" stroke-width="7" fill="none" stroke-dasharray="18 12"/><circle cx="${ax}" cy="${ay}" r="16" fill="${C.orange}"/></svg>` +
      `<div style="position:absolute;left:${x}px;top:${y}px;width:860px;z-index:5;background:#fff;border-radius:34px;padding:34px 44px;box-shadow:0 10px 30px rgba(0,0,0,.12);font-family:'Fredoka'"><div style="font-family:'Grandstander';font-weight:900;font-size:62px;color:${C.purple}">${n}. ${t}</div><div style="font-size:46px;color:${C.ink};line-height:1.3;margin-top:8px">${s}</div></div>`;
    b += call(1, 'Placement guides', 'Faint corner marks show exactly where the hand goes – hidden by the paint.', 1440, 560, 1130, 720);
    b += call(2, 'Type-in names', 'Fillable name, age &amp; year boxes. Or write them by hand.', 1440, 1130, 920, 1880);
    b += call(3, 'Night-sky designs', 'White paint pops on the dark panels. Color the sky in on the coloring version.', 1440, 1620, 1250, 1500);
    return page(b);
  },
  '08-how-it-works': () => {
    let b = H('How It Works', { y: 150, size: 150 });
    const steps = [['1', 'Print', 'at home on cardstock', blank('eyes-hand')], ['2', 'Paint', 'a hand, foot or finger', null], ['3', 'Press', 'inside the corner guides', null], ['4', 'Decorate', 'eyes, faces &amp; names', sample('eyes-hand')]];
    steps.forEach(([n, t, s, svg], i) => {
      const x = 90 + i * 565, y = 520;
      b += `<div style="position:absolute;left:${x}px;top:${y}px;width:520px;height:1300px;background:#fff;border-radius:44px;box-shadow:0 12px 30px rgba(0,0,0,.08)"></div>`;
      b += `<div style="position:absolute;left:${x + 190}px;top:${y + 50}px;width:140px;height:140px;border-radius:50%;background:${i % 2 ? C.orange : C.purple};color:#fff;font-family:'Grandstander';font-weight:900;font-size:92px;text-align:center;line-height:140px">${n}</div>`;
      b += H(t, { x: x + 260, y: y + 230, size: 96, w: 520 });
      b += H(s, { x: x + 260, y: y + 360, size: 48, w: 460, font: 'Fredoka', weight: 400, color: '#6b6170' });
      if (svg) b += sheet(svg, { x: x + 60, y: y + 560, w: 400 });
      else {
        L.setMode('color');
        const z = { type: i === 1 ? 'hand' : 'hand', x: 0, y: 0, color: i === 1 ? '#A585DB' : '#A585DB' };
        const art = i === 1
          ? `<svg width="420" height="700" viewBox="-250 -330 500 720"><defs>${L.paintDefs()}</defs>${L.samplePrint(z)}<g transform="translate(150 -170) rotate(35)"><rect x="-18" y="-10" width="36" height="300" rx="14" fill="#E2B672" stroke="${C.ink}" stroke-width="6"/><rect x="-22" y="-60" width="44" height="60" fill="#C8C3CC" stroke="${C.ink}" stroke-width="6"/><path d="M-22,-60 C-24,-110 24,-110 22,-60 Z" fill="#A585DB" stroke="${C.ink}" stroke-width="6"/></g></svg>`
          : `<svg width="420" height="700" viewBox="-260 -320 520 720"><defs>${L.paintDefs()}</defs>${L.samplePrint(z)}<g stroke="${C.ink}" stroke-width="6" fill="none" stroke-dasharray="4 14" stroke-linecap="round"><path d="M-180,-150 a40,40 0 0 1 0,-60 M190,-150 a40,40 0 0 0 0,-60"/></g></svg>`;
        b += `<div style="position:absolute;left:${x + 50}px;top:${y + 560}px">${art}</div>`;
      }
    });
    b += H('Takes about 10 minutes – then it’s a keepsake forever.', { y: 1980, size: 64, font: 'Fredoka', weight: 600, color: C.purple });
    return page(b, '#FFFBF5');
  },
  '09-bonus': () => {
    const g = guidePages();
    let b = confetti(11, 22) + H('Bonus Pages Included', { y: 140, size: 140 });
    b += sheet(g[4].svg, { x: 90, y: 470, w: 740, rot: -4 }) + sheet(g[6].svg, { x: 830, y: 430, w: 740, rot: 0, z: 2 }) + sheet(g[2].svg, { x: 1570, y: 470, w: 740, rot: 4 });
    b += H('cut &amp; glue<br>face pieces', { x: 460, y: 1540, size: 70, w: 700, font: 'Fredoka', weight: 600 });
    b += H('4 fingerprint<br>mini cards', { x: 1200, y: 1540, size: 70, w: 700, font: 'Fredoka', weight: 600 });
    b += H('visual index<br>+ paint guide', { x: 1940, y: 1540, size: 70, w: 700, font: 'Fredoka', weight: 600 });
    b += pill('PLUS: how-to tips for a perfect print', { x: 470, y: 1960, bg: C.night, size: 64, w: 1460 });
    return page(b);
  },
  '10-every-age': () => {
    let b = H('Babies to Big Kids', { y: 150, size: 150 });
    b += H('and classrooms too!', { y: 320, size: 76, font: 'Fredoka', weight: 600, color: C.orange });
    const cols = [['ghost-feet', 'Footprints', 'perfect for babies'], ['monster-hand', 'Handprints', 'toddlers &amp; preschool'], ['boocrew-finger', 'Fingerprints', 'families &amp; classes']];
    cols.forEach(([id, t, s], i) => {
      const x = 120 + i * 740;
      b += sheet(sample(id), { x: x, y: 540, w: 660, rot: (i - 1) * 2 });
      b += H(t, { x: x + 330, y: 1460, size: 92, w: 700 }) + H(s, { x: x + 330, y: 1575, size: 56, w: 700, font: 'Fredoka', weight: 400, color: '#6b6170' });
    });
    b += pill('Teachers: one download prints for your whole class', { x: 300, y: 1900, bg: C.purple, size: 62, w: 1800 });
    return page(b, '#FFFBF5');
  },
};

const browser = await chromium.launch();
const pg = await browser.newPage({ viewport: { width: 2400, height: 2400 } });
const only = process.argv.slice(2);
for (const [name, fn] of Object.entries(IMAGES)) {
  if (only.length && !only.includes(name)) continue;
  writeFileSync(`${OUT}/_tmp.html`, fn());
  await pg.goto(`file://${OUT}/_tmp.html`);
  await pg.evaluate(() => document.fonts.ready);
  await pg.waitForTimeout(150);
  await pg.screenshot({ path: `${OUT}/${name}.png` });
  console.log('ok', name);
}
await browser.close();
