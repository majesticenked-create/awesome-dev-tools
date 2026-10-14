// START HERE guide + bonus pages (cover, how-to, visual index, cut & glue
// pieces, mini cards, terms). All portrait 850 x 1100.
import * as L from './lib.mjs';
import { DESIGNS } from './designs.mjs';
import { renderDesign } from './page.mjs';
import { batWing } from './helpers.mjs';
const { INK, os, line, isBW, pal, text, title } = L;

export const PRODUCT = 'Halloween Handprint Art';
const N = DESIGNS.length;

// Embed a full-page SVG as a thumbnail.
export function nest(svg, x, y, w, h) {
  return svg.replace(/^<svg xmlns="http:\/\/www.w3.org\/2000\/svg" viewBox="([^"]+)" width="\d+" height="\d+">/, `<svg x="${x}" y="${y}" width="${w}" height="${h}" viewBox="$1">`);
}
const card = (x, y, w, h, r = 18, c = '#fff') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" fill="${c}" stroke="${INK}" stroke-width="2.5"/>`;
const para = (x, y, lines, { size = 25, lh = 1.32, anchor = 'start', color = 'ink', font = 'round', weight = 400 } = {}) =>
  lines.map((l, i) => text(x, y + i * size * lh, l, { size, anchor, color, font, weight })).join('');
const wrap = (svgBody) => `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 850 1100" width="850" height="1100"><defs>${L.paintDefs()}</defs><rect width="850" height="1100" fill="#fff"/>${svgBody}</svg>`;
const footer = (n) => text(425, 1062, `${PRODUCT}  ·  Start Here guide  ·  page ${n}`, { size: 16, font: 'round', color: 'gray' });

function cover() {
  L.setMode('color');
  let b = L.nightPanel(40, 40, 770, 1020, { r: 40, seed: 12 }) + L.moon(690, 160, 70) + L.bat(150, 150, 2, -8) + L.bat(230, 200, 1.3, 10);
  b += title(425, 300, [['Halloween', 'orange']], { size: 96 });
  b += `<text x="425" y="390" font-family="${L.FONTS.title}" font-size="66" font-weight="900" text-anchor="middle" fill="#fff">Handprint Art</text>`;
  b += `<text x="425" y="450" font-family="${L.FONTS.round}" font-size="30" text-anchor="middle" fill="${pal('moon')}">${N} keepsake crafts · handprint · footprint · fingerprint</text>`;
  const picks = ['ghost-hand', 'monster-hand', 'pumpkin-hand', 'vampire-hand', 'ghost-feet', 'eyes-hand'];
  picks.forEach((id, i) => {
    const d = DESIGNS.find((x) => x.id === id);
    const x = 95 + (i % 3) * 225, y = 500 + Math.floor(i / 3) * 265;
    b += `<rect x="${x - 6}" y="${y - 6}" width="${192}" height="${248}" rx="10" fill="#fff" opacity="0.15"/>`;
    b += nest(renderDesign(d, { mode: 'color', sample: true }).svg, x, y, 180, 233);
    L.setMode('color');
  });
  b += `<text x="425" y="1040" font-family="${L.FONTS.title}" font-size="34" font-weight="700" text-anchor="middle" fill="#fff">START HERE ✦ guide &amp; bonus pages</text>`;
  return wrap(b);
}

function howTo() {
  L.setMode('color');
  let b = title(425, 110, [['How to Make a ', 'ink'], ['Perfect Print', 'orange']], { size: 52 });
  const steps = [
    ['1', 'Print', ['Print on white cardstock (65–110 lb) at “Actual size”.', 'Type names into the name / age / year boxes', 'first. Printing on A4 paper? Use the A4 files.']],
    ['2', 'Paint', ['Use washable kids’ paint (tempera or finger', 'paint). Brush a thin, even coat onto the hand', 'or foot. Don’t dip – thick paint smudges.']],
    ['3', 'Press', ['Line up with the faint corner guides. Press', 'down, gently push each finger / toe, then lift', 'straight up. The guides are hidden by paint.']],
    ['4', 'Finish', ['Let it dry 15–30 minutes. Add faces with a', 'marker, googly eyes, or the cut & glue face', 'pieces included in this guide.']],
  ];
  steps.forEach(([n, h, lines], i) => {
    const y = 165 + i * 158;
    b += card(60, y, 730, 140, 22, i % 2 ? '#FFF7EC' : '#F4EEFB');
    b += `<circle cx="120" cy="${y + 70}" r="38" fill="${pal(i % 2 ? 'orange' : 'purple')}"/>` + text(120, y + 86, n, { size: 46, font: 'title', weight: 900, color: '#fff' });
    b += text(185, y + 46, h, { size: 34, font: 'title', weight: 900, anchor: 'start' });
    b += para(185, y + 80, lines, { size: 21 });
  });
  b += title(425, 820, [['Little ', 'ink'], ['Tips', 'purple']], { size: 40 });
  b += para(85, 862, [
    '•  Babies: do footprints while they’re sleepy or feeding – one foot at a time.',
    '•  Practice once on scrap paper first. Keep baby wipes close by!',
    '•  Prints look best when the hand is relaxed and fingers are spread.',
    '•  Ghosts on the night sky: use white paint. Coloring version: color the sky first.',
    '•  Every page fits an 8.5×11 frame, or an 11×14 frame with a mat.',
  ], { size: 21, lh: 1.45 });
  return wrap(b + footer(2));
}

function visualIndex(part) {
  L.setMode('color');
  const list = DESIGNS.slice(part * 15, part * 15 + 15);
  let b = title(425, 95, [['Design ', 'ink'], ['Index', 'orange'], [` ${part + 1}/2`, 'ink']], { size: 48 });
  b += text(425, 132, 'Finished examples with the paint colors we suggest. Page numbers match every PDF.', { size: 20, font: 'round', color: 'gray' });
  list.forEach((d, i) => {
    const n = part * 15 + i + 1;
    const col = i % 3, row = Math.floor(i / 3);
    const x = 55 + col * 255, y = 160 + row * 178;
    b += card(x, y, 240, 168, 12, '#FBF9F6');
    const r = renderDesign(d, { mode: 'color', sample: true });
    const tw = r.W > r.H ? 120 : 98, th = r.W > r.H ? 93 : 127;
    b += nest(r.svg, x + 8, y + (168 - th) / 2, tw, th);
    L.setMode('color');
    const tx = x + 8 + tw + 10;
    b += text(tx, y + 30, `p.${n}`, { size: 18, font: 'round', weight: 700, anchor: 'start', color: 'orange' });
    const words = d.name.split(' '); let lines = [''];
    for (const w of words) { if ((lines.at(-1) + ' ' + w).trim().length > 13) lines.push(w); else lines[lines.length - 1] = (lines.at(-1) + ' ' + w).trim(); }
    b += para(tx, y + 54, lines.slice(0, 3), { size: 17, weight: 600, lh: 1.15 });
    const kind = { hand: '✋ handprint', foot: '👣 footprint', finger: '☝ fingerprints' }[d.kind];
    b += text(tx, y + 54 + Math.min(3, lines.length) * 19.5 + 6, kind.replace(/^\S+ /, ''), { size: 15, font: 'round', anchor: 'start', color: 'purple' });
    const pw = d.paint.split(' '); let pl = [''];
    for (const w of pw) { if ((pl.at(-1) + ' ' + w).trim().length > 15) pl.push(w); else pl[pl.length - 1] = (pl.at(-1) + ' ' + w).trim(); }
    b += para(tx, y + 54 + Math.min(3, lines.length) * 19.5 + 28, pl.slice(0, 3), { size: 13.5, lh: 1.2, color: 'gray' });
  });
  return wrap(b + footer(3 + part));
}

function piecesPage(mode) {
  L.setMode(mode);
  const cut = (x, y, w, h) => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="14" fill="none" stroke="#B9B4BF" stroke-width="1.6" stroke-dasharray="7 6"/>`;
  let b = title(425, 95, [['Cut & Glue ', 'ink'], ['Face Pieces', 'purple']], { size: 50 });
  b += text(425, 132, mode === 'bw' ? 'Color them in, cut on the dotted lines and glue onto the dry print.' : 'Cut on the dotted lines and glue onto the dry print. Print extra copies for classes!', { size: 20, font: 'round', color: 'gray' });
  // googly eyes, 3 sizes
  b += cut(45, 160, 760, 120);
  [14, 14, 18, 18, 22, 22, 26, 26, 30, 30].forEach((r, i) => { b += L.googly(85 + i * 72, 220, r, [i % 2 ? 0.2 : -0.2, 0.2]); });
  // ghost eyes + jack faces
  b += cut(45, 295, 370, 150) + cut(435, 295, 370, 150);
  for (let i = 0; i < 3; i++) { const x = 105 + i * 110; b += `<ellipse cx="${x - 16}" cy="350" rx="10" ry="15" fill="${INK}"/><ellipse cx="${x + 16}" cy="350" rx="10" ry="15" fill="${INK}"/><ellipse cx="${x}" cy="400" rx="11" ry="16" fill="${INK}"/>`; }
  for (let i = 0; i < 2; i++) {
    const x = 530 + i * 180;
    b += `<g transform="translate(${x} 370) scale(0.9)"><path d="M-38,-14 l14,-22 l14,22z M10,-14 l14,-22 l14,22z M-6,4 l6,-10 l6,10z" ${os('yellow', 3)}/><path d="M-44,18 q44,44 88,0 l-12,5 l-8,-9 l-10,9 l-10,-9 l-10,9 l-10,-9 l-10,9 l-8,-9 z" ${os('yellow', 3)}/></g>`;
  }
  // fangs + smiles + stitched smiles
  b += cut(45, 460, 760, 120);
  for (let i = 0; i < 3; i++) { const x = 110 + i * 120; b += `<path d="M${x - 34},510 q34,30 68,0" ${line(5)}/><path d="M${x - 24},514 l7,22 l7,-17 Z M${x + 10},517 l7,17 l7,-22 Z" fill="#fff" stroke="${INK}" stroke-width="2.5" stroke-linejoin="round"/>`; }
  for (let i = 0; i < 3; i++) { const x = 475 + i * 115; b += `<path d="M${x - 36},510 q36,34 72,0" ${line(5)}/><path d="M${x - 26},512 l-4,14 M${x - 10},521 l-2,14 M${x + 6},523 l0,14 M${x + 22},518 l2,14" ${line(3)}/>`; }
  // bow ties, bolts, hearts
  b += cut(45, 595, 370, 140) + cut(435, 595, 370, 140);
  for (let i = 0; i < 3; i++) { const x = 110 + i * 110, c = ['red', 'purple', 'orange'][i]; b += `<path d="M${x - 40},648 L${x},668 L${x + 40},648 L${x + 40},698 L${x},678 L${x - 40},698 Z" ${os(c, 3.5)}/><circle cx="${x}" cy="673" r="10" ${os(c, 3.5)}/>`; }
  b += L.bolt(500, 640, 1.4, -1) + L.bolt(560, 640, 1.4, 1) + L.bolt(500, 700, 1.4, -1) + L.bolt(560, 700, 1.4, 1);
  b += L.heart(670, 650, 1.6, 'red') + L.heart(740, 650, 1.6, 'pink') + L.heart(670, 705, 1.3, 'pink') + L.heart(740, 705, 1.3, 'red');
  // hats, mummy eye bands, owl eyes, bat wings
  b += cut(45, 750, 370, 165) + cut(435, 750, 370, 165);
  b += L.witchHat(140, 880, 0.95) + L.witchHat(320, 880, 0.95, 0, 'green');
  for (let i = 0; i < 2; i++) { const y = 795 + i * 70; b += `<rect x="470" y="${y}" width="110" height="34" rx="16" fill="${INK}"/><circle cx="503" cy="${y + 17}" r="11" fill="${isBW() ? '#fff' : pal('yellow')}"/><circle cx="547" cy="${y + 17}" r="11" fill="${isBW() ? '#fff' : pal('yellow')}"/><circle cx="505" cy="${y + 19}" r="5" fill="${INK}"/><circle cx="549" cy="${y + 19}" r="5" fill="${INK}"/>`; }
  b += `<circle cx="660" cy="830" r="34" fill="#fff" stroke="${isBW() ? INK : pal('orange')}" stroke-width="7"/><circle cx="740" cy="830" r="34" fill="#fff" stroke="${isBW() ? INK : pal('orange')}" stroke-width="7"/><circle cx="664" cy="834" r="14" fill="${INK}"/><circle cx="736" cy="834" r="14" fill="${INK}"/><path d="M690,872 l10,22 l10,-22 z" ${os('orange', 2.5)}/>`;
  // wings row
  b += cut(45, 930, 760, 110);
  for (let i = 0; i < 4; i++) { const x = 140 + i * 190; b += batWing(x, 990, 44, -1) + batWing(x, 990, 44, 1); }
  return wrap(b);
}

function miniCards(page) {
  L.setMode('color');
  const ctx = { fields: [] };
  let b = `<line x1="30" y1="550" x2="820" y2="550" stroke="#B9B4BF" stroke-width="2" stroke-dasharray="10 8"/>` +
    text(425, 543, '✂  cut here', { size: 16, font: 'round', color: 'gray' });
  const cards = page === 0
    ? [{ t: [['Have a ', 'ink'], ['Fang-tastic', 'purple']], t2: 'Halloween!', kind: 'bats' }, { t: [['Love You, ', 'ink'], ['Pumpkin!', 'orange']], t2: '', kind: 'pumpkins' }]
    : [{ t: [["You're ", 'ink'], ['Spook-tacular!', 'purple']], t2: '', kind: 'spiders' }, { t: [['Sending ', 'ink'], ['Monster', 'green']], t2: 'Hugs!', kind: 'monsters' }];
  const zones = [];
  cards.forEach((c, i) => {
    const oy = i * 550;
    b += `<rect x="40" y="${oy + 40}" width="770" height="470" rx="26" fill="none" stroke="${pal(i ? 'orange' : 'purple')}" stroke-width="5"/>`;
    b += title(425, oy + 125, c.t, { size: 54 });
    if (c.t2) b += title(425, oy + 182, [[c.t2, 'ink']], { size: 46 });
    const yy = oy + 320;
    const pts = [[270, yy], [425, yy - 20], [580, yy]];
    if (c.kind === 'bats') pts.forEach(([x, y]) => { zones.push({ type: 'finger', x, y, r: 36 }); b += batWing(x, y, 36, -1) + batWing(x, y, 36, 1); });
    if (c.kind === 'pumpkins') { b += `<path d="M160,${yy + 30} C260,${yy + 70} 330,${yy - 10} 425,${yy + 20} C520,${yy + 50} 590,${yy - 10} 690,${yy + 30}" ${line(4, pal('greenDk'))}/>`; pts.forEach(([x, y]) => { zones.push({ type: 'finger', x, y, r: 40 }); b += `<path d="M${x - 3},${y - 42} q-2,-16 7,-23 l6,5 q-7,4 -5,18 z" ${os('greenDk', 2.5)}/>` + L.leaf(x + 5, y - 52, 0.8, -150); }); }
    if (c.kind === 'spiders') { b += L.web(810, oy + 40, 120, 'tr') + L.web(40, oy + 40, 120, 'tl'); pts.forEach(([x, y]) => { zones.push({ type: 'finger', x, y, r: 34 }); let d = ''; for (const s of [-1, 1]) for (const [a, bb] of [[-0.6, -1.1], [-0.2, -0.3], [0.2, 0.4], [0.5, 1.1]]) d += `M${x + s * 24},${y + a * 24} q${s * 18},${-14 + a * 10} ${s * 32},${bb * 24}`; b += `<path d="${d}" ${line(4)}/>`; }); }
    if (c.kind === 'monsters') [[300, yy], [550, yy]].forEach(([x, y], k) => { zones.push({ type: 'finger', x, y, r: 55 }); b += `<path d="M${x - 30},${y - 56} l-12,-30 l24,16 M${x + 30},${y - 56} l12,-30 l-24,16" ${os(k ? 'purple' : 'yellow', 3)}/><path d="M${x - 58},${y} q-30,-8 -36,-34 M${x + 58},${y} q30,-8 36,-34 M${x - 18},${y + 62} v24 h-12 M${x + 18},${y + 62} v24 h12" ${line(4.5)}/>`; });
    b += L.scatter([[90, oy + 100, 14, 'orange'], [760, oy + 100, 14, 'purple'], [100, oy + 440, 10, 'purple'], [750, oy + 440, 10, 'orange']]);
    b += L.fillLine(ctx, 425, oy + 470, [['to', 220], ['from', 220]], { size: 26 });
  });
  b += zones.map(L.zoneGuide).join('');
  return { svg: wrap(b), fields: ctx.fields };
}

function terms() {
  L.setMode('color');
  let b = L.ghost(425, 190, 2.4) + L.pumpkin(330, 250, 1.4) + L.candyCorn(530, 260, 1.6, 15);
  b += title(425, 360, [['Thank ', 'ink'], ['You!', 'orange']], { size: 70 });
  b += para(425, 420, ['Thank you for supporting a small shop. If you love your prints,', 'a review (with a photo of your little one’s art!) means the world.'], { size: 23, anchor: 'middle' });
  b += card(70, 500, 710, 430, 24, '#FBF9F6');
  b += title(425, 560, [['Terms of ', 'ink'], ['Use', 'purple']], { size: 40 });
  b += para(110, 610, [
    '✓  Print as many copies as you like for your family.',
    '✓  Teachers, daycares and homeschool groups: print for your',
    '     class or group – one purchase per teacher, please.',
    '✓  Gift, frame or sell the finished, hand-made artwork.',
    '✗  Please don’t share, resell, or redistribute the digital files,',
    '     or sell printed blank templates.',
    '',
    'This is a digital download – no physical item will be shipped.',
    'Colors may vary slightly between screens and printers.',
  ], { size: 22, lh: 1.5 });
  b += text(425, 980, 'Questions? Send us a message on Etsy – we’re happy to help.', { size: 22, font: 'round', color: 'purpleDk' });
  return wrap(b + footer(9));
}

// Returns [{svg, fields}] in order.
export function guidePages() {
  const pages = [cover(), howTo(), visualIndex(0), visualIndex(1), piecesPage('color'), piecesPage('bw')].map((svg) => ({ svg, fields: [] }));
  pages.push(miniCards(0), miniCards(1));
  pages.push({ svg: terms(), fields: [] });
  return pages;
}
