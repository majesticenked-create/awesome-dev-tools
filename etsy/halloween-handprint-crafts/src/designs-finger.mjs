// Fingerprint designs 24-30.
import * as L from './lib.mjs';
import { W, PAINT, batWing, hauntedHouse } from './helpers.mjs';
const { INK, os, line, isBW, pal, text } = L;

const fz = (pts, r, color) => pts.map(([x, y, c]) => ({ type: 'finger', x, y, r, color: c || color }));
const tinyFace = (x, y, s = 1, kind = 'smile') => `<circle cx="${x - 7 * s}" cy="${y - 3 * s}" r="${3 * s}" fill="${INK}"/><circle cx="${x + 7 * s}" cy="${y - 3 * s}" r="${3 * s}" fill="${INK}"/>` +
  (kind === 'o' ? `<ellipse cx="${x}" cy="${y + 8 * s}" rx="${3 * s}" ry="${4 * s}" fill="${INK}"/>` : `<path d="M${x - 5 * s},${y + 4 * s} q${5 * s},${5 * s} ${10 * s},0" ${line(2.2 * s)}/>`);
const ggEyes = (x, y, r = 9) => L.googly(x - r * 0.95, y - 4, r, [0.2, 0.2]) + L.googly(x + r * 0.95, y - 4, r, [0.2, 0.2]);

const PATCH = [[150, 450], [262, 395], [374, 450], [486, 395], [598, 450], [710, 395], [200, 700], [312, 645], [424, 700], [536, 645], [648, 700]];
const JAR = [[330, 470, PAINT.purple], [425, 450, PAINT.orange], [520, 475, PAINT.green], [300, 560, PAINT.red], [550, 565, PAINT.teal], [330, 720, PAINT.pink], [425, 745, PAINT.yellow], [520, 720, PAINT.purple], [375, 800, PAINT.orange], [480, 805, PAINT.green]];
const CREW = [[200, 330], [330, 290], [520, 290], [650, 330], [205, 520], [645, 520]];
const WEBSP = [[425, 560], [300, 420], [560, 400], [270, 650], [580, 690], [425, 330]];
const BATS = [[230, 330], [610, 300], [425, 430], [295, 575], [565, 590], [190, 760], [660, 760]];
const BUBBLES = [[340, 600, PAINT.lime], [500, 570, PAINT.purple], [410, 470, PAINT.lime], [540, 400, PAINT.lime], [300, 420, PAINT.purple], [430, 300, PAINT.lime]];
const SQUAD = [[205, 430, PAINT.green], [425, 430, PAINT.purple], [645, 430, PAINT.orange], [205, 730, PAINT.teal], [425, 730, PAINT.pink], [645, 730, PAINT.lime]];

export const FINGERS = [
  {
    id: 'pumpkinpatch-finger', kind: 'finger', name: 'Fingerprint Pumpkin Patch', paint: 'orange',
    title: [['My Little ', 'ink'], ['Pumpkin Patch', 'orange']], titleSize: 60,
    caption: 'Count them all, then give each one a face!',
    zones: fz(PATCH, 40, PAINT.orange),
    back: () => `<path d="M90,470 C180,510 230,420 320,460 C410,500 460,410 540,460 C630,500 680,410 770,440" ${line(4, isBW() ? INK : pal('greenDk'))}/>` +
      `<path d="M120,720 C220,760 280,660 380,710 C470,750 520,660 600,710 C660,740 700,690 750,700" ${line(4, isBW() ? INK : pal('greenDk'))}/>` +
      `<path d="M110,860 C300,830 550,830 740,860" ${line(4)}/>` + L.grassTufts(130, 730, 857) + L.pumpkin(200, 822, 1.1) + L.pumpkin(650, 826, 0.9),
    front: (ctx) => ctx.zones.map((z, i) => `<path d="M${z.x - 3},${z.y - 40} q-2,-16 7,-23 l6,5 q-7,4 -5,18 z" ${os('greenDk', 2.5)}/>` + L.leaf(z.x + 5, z.y - 50, 0.8, i % 2 ? -30 : -150) +
      text(z.x + 52, z.y + 40, String(i + 1), { size: 26, font: 'round', weight: 600, color: 'orangeDk' })).join('') +
      L.scatter([[120, 260, 12, 'purple'], [740, 270, 12, 'orange'], [425, 250, 8, 'ink']]),
    finish: (ctx) => ctx.zones.map((z) => tinyFace(z.x, z.y + 2, 1.15)).join(''),
  },
  {
    id: 'candyjar-finger', kind: 'finger', name: 'Fingerprint Candy Jar', paint: 'any bright colors',
    title: [['Sweet ', 'ink'], ['Treat', 'purple'], [' Jar', 'ink']],
    caption: 'Fill the jar with fingerprint candy!',
    zones: fz(JAR, 32),
    back: () => `<path d="M260,320 L590,320 C610,320 620,340 610,360 C650,400 660,460 660,520 L660,800 C660,850 630,870 580,870 L270,870 C220,870 190,850 190,800 L190,520 C190,460 200,400 240,360 C230,340 240,320 260,320 Z" fill="${isBW() ? '#fff' : '#EEF6FB'}" stroke="${INK}" stroke-width="5" stroke-linejoin="round"/>` +
      `<rect x="245" y="270" width="360" height="56" rx="16" ${os('orange')}/><path d="M275,270 v56 M315,270 v56 M355,270 v56 M395,270 v56 M435,270 v56 M475,270 v56 M515,270 v56 M555,270 v56" ${line(2.5)}/>` +
      (isBW() ? '' : `<path d="M220,520 C220,470 230,430 255,400" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round"/>`) +
      `<rect x="285" y="605" width="280" height="76" rx="14" ${os('cream', 3.5)}/>` + text(425, 657, 'TREATS', { size: 44, font: 'title', weight: 900, color: 'purple', outline: true }) +
      L.scatter([[130, 330, 12, 'orange'], [720, 330, 12, 'purple'], [120, 620, 9, 'purple'], [730, 640, 10, 'orange']]),
    front: (ctx) => ctx.zones.map((z) => `<path d="M${z.x - 28},${z.y} l-18,-12 l2,24 z M${z.x + 28},${z.y} l18,-12 l-2,24 z" ${os('white', 2.5)}/>`).join(''),
  },
  {
    id: 'boocrew-finger', kind: 'finger', name: 'Our Boo Crew (family / class)', paint: 'white (on the night sky)',
    title: [['Our ', 'ink'], ['Boo', 'purple'], [' Crew', 'ink']], titleSize: 80,
    nameFields: [['Halloween', 110]], nameY: 1040,
    zones: fz(CREW, 36, W),
    back: () => L.nightPanel(110, 205, 630, 575, { seed: 9 }) + L.moon(425, 300, 44) + hauntedHouse(425, 640, 1.5) +
      `<path d="M140,780 C300,740 550,740 710,780 Z" ${isBW() ? `fill="#fff" stroke="${INK}" stroke-width="3"` : `fill="${pal('nightLt')}"`}/>`,
    front: (ctx) => ctx.zones.map((z, i) => text(z.x + 46, z.y + 40, String(i + 1), { size: 24, font: 'round', weight: 700, color: isBW() ? 'ink' : 'moon' })).join(''),
    finish: (ctx) => ctx.zones.map((z) => `<ellipse cx="${z.x - 8}" cy="${z.y - 4}" rx="4" ry="6" fill="${INK}"/><ellipse cx="${z.x + 8}" cy="${z.y - 4}" rx="4" ry="6" fill="${INK}"/><ellipse cx="${z.x}" cy="${z.y + 12}" rx="4" ry="5" fill="${INK}"/>`).join(''),
    extra: (ctx) => {
      let out = '';
      for (let i = 0; i < 6; i++) {
        const x = i < 3 ? 140 : 455, y = 835 + (i % 3) * 52;
        out += text(x, y, `${i + 1}.`, { size: 26, font: 'round', weight: 600, anchor: 'start' }) + `<line x1="${x + 30}" y1="${y + 4}" x2="${x + 260}" y2="${y + 4}" stroke="${INK}" stroke-width="1.6"/>`;
        ctx.fields.push({ name: `boo${i + 1}`, x: x + 32, y: y - 24, w: 226, h: 30 });
      }
      return out;
    },
  },
  {
    id: 'spiders-finger', kind: 'finger', name: 'Fingerprint Spiders', paint: 'black or purple',
    title: [['Itsy Bitsy ', 'ink'], ['Halloween', 'purple']], titleSize: 66,
    caption: 'Give every little spider a pair of eyes',
    zones: fz(WEBSP, 30, PAINT.black),
    back: () => L.roundWeb(425, 540, 320, 2.2, 12) + `<line x1="425" y1="190" x2="425" y2="220" ${line(2)}/>`,
    front: (ctx) => ctx.zones.map((z) => {
      let d = '';
      for (const s of [-1, 1]) for (const [a, b] of [[-0.6, -1.1], [-0.2, -0.3], [0.2, 0.4], [0.5, 1.1]]) {
        const x0 = z.x + s * 22, y0 = z.y + a * 22;
        d += `M${x0},${y0} q${s * 18},${-14 + a * 10} ${s * 30},${b * 22}`;
      }
      return `<path d="${d}" ${line(4)}/>`;
    }).join('') + L.scatter([[130, 260, 12, 'orange'], [720, 260, 12, 'orange'], [140, 840, 10, 'purple'], [710, 850, 10, 'purple']]),
    finish: (ctx) => ctx.zones.map((z) => ggEyes(z.x, z.y, 9)).join(''),
  },
  {
    id: 'bats-finger', kind: 'finger', name: 'Fingerprint Bats & Moon', paint: 'black or gray',
    title: [['Bats ', 'ink'], ['About', 'purple'], [' You!', 'ink']], titleSize: 76,
    caption: 'A whole night full of Halloween love',
    zones: fz(BATS, 32, PAINT.black),
    back: () => L.moon(425, 530, 215) + `<path d="M120,610 q30,-30 70,-10 q30,-26 66,0 q30,-4 30,22 H120 Z M570,360 q30,-30 70,-10 q30,-26 66,0 q30,-4 30,22 H570 Z" ${os('white', 3)}/>`,
    front: (ctx) => ctx.zones.map((z) => batWing(z.x, z.y, 32, -1) + batWing(z.x, z.y, 32, 1)).join('') +
      L.scatter([[130, 270, 12, 'orange'], [730, 470, 12, 'orange'], [130, 470, 8, 'purple'], [720, 860, 9, 'purple'], [425, 860, 8, 'orange']]),
    finish: (ctx) => ctx.zones.map((z) => `<circle cx="${z.x - 8}" cy="${z.y - 4}" r="5.5" fill="#fff"/><circle cx="${z.x + 8}" cy="${z.y - 4}" r="5.5" fill="#fff"/><circle cx="${z.x - 7}" cy="${z.y - 3}" r="2.4" fill="${INK}"/><circle cx="${z.x + 9}" cy="${z.y - 3}" r="2.4" fill="${INK}"/>`).join(''),
  },
  {
    id: 'cauldron-finger', kind: 'finger', name: 'Bubbling Cauldron', paint: 'green + purple',
    title: [['Bubble, Bubble,', 'ink']], title2: [['Here Comes Trouble!', 'green']], titleSize: 64, titleY: 125,
    caption: 'Happy Halloween!', captionY: 950,
    zones: fz(BUBBLES, 38),
    back: () => `<path d="M300,700 C260,640 360,620 330,560 M520,690 C580,630 480,600 530,540" ${line(3, isBW() ? INK : pal('lime'))}/>` +
      L.spider(150, 400, 1.2, { thread: 180 }) + L.bat(700, 320, 1.4, 8) + L.bat(650, 280, 0.9, -8),
    front: () => L.cauldron(425, 760, 2.4) +
      `<path d="M300,880 l30,-20 l30,20 l30,-22 l30,22 l30,-20 l30,20 l30,-22 l30,22" ${line(5, isBW() ? INK : pal('orange'))}/>` +
      L.scatter([[160, 620, 10, 'orange'], [700, 600, 12, 'purple'], [690, 820, 9, 'orange']]),
    finish: (ctx) => ctx.zones.map((z, i) => i % 2 ? L.googly(z.x, z.y, 14) : ggEyes(z.x, z.y, 9)).join(''),
  },
  {
    id: 'monsters-finger', kind: 'finger', name: 'Mini Monster Squad', paint: 'any bright colors (thumbprints work great)',
    title: [['Mini ', 'ink'], ['Monster', 'green'], [' Squad', 'ink']], titleSize: 72,
    caption: 'Give every monster a silly face!',
    zones: fz(SQUAD, 60),
    front: (ctx) => ctx.zones.map((z, i) => {
      const { x, y } = z;
      const top = [
        `<path d="M${x - 22},${y - 44} l-10,-26 l20,14 M${x + 22},${y - 44} l10,-26 l-20,14" ${os('yellow', 3)}/>`,
        `<path d="M${x - 14},${y - 50} q-10,-26 -24,-30 M${x + 14},${y - 50} q10,-26 24,-30" ${line(3.5)}/><circle cx="${x - 38}" cy="${y - 80}" r="8" ${os('pink', 3)}/><circle cx="${x + 38}" cy="${y - 80}" r="8" ${os('pink', 3)}/>`,
        `<path d="M${x - 30},${y - 40} l8,-24 l10,18 l12,-24 l12,24 l10,-18 l8,24" ${os('purple', 3)}/>`,
        `<path d="M${x},${y - 52} q4,-28 -12,-36" ${line(3.5)}/><circle cx="${x - 12}" cy="${y - 90}" r="9" ${os('yellow', 3)}/>`,
        `<path d="M${x - 26},${y - 42} q-14,-24 -2,-34 q6,14 14,22 M${x + 26},${y - 42} q14,-24 2,-34 q-6,14 -14,22" ${os('teal', 3)}/>`,
        `<path d="M${x - 36},${y - 30} q-6,-30 14,-34 q-2,18 6,24 M${x + 36},${y - 30} q6,-30 -14,-34 q2,18 -6,24" ${os('orange', 3)}/>`,
      ][i];
      const legs = `<path d="M${x - 14},${y + 50} v20 h-10 M${x + 14},${y + 50} v20 h10" ${line(4)}/>` +
        `<path d="M${x - 44},${y + 4} q-22,-6 -28,-26 M${x + 44},${y + 4} q22,-6 28,-26" ${line(4)}/>`;
      return `<g transform="translate(${x} ${y}) scale(1.3) translate(${-x} ${-y})">${top + legs}</g>`;
    }).join('') + L.scatter([[110, 260, 12, 'orange'], [740, 250, 12, 'purple'], [425, 590, 9, 'ink'], [110, 590, 8, 'purple', 'dot'], [740, 590, 8, 'orange', 'dot']]),
    finish: (ctx) => ctx.zones.map((z, i) => `<g transform="translate(${z.x} ${z.y}) scale(1.3) translate(${-z.x} ${-z.y})">` + [
      ggEyes(z.x, z.y - 6, 11) + `<path d="M${z.x - 12},${z.y + 18} q12,10 24,0" ${line(3)}/>`,
      L.googly(z.x, z.y - 8, 18) + `<path d="M${z.x - 14},${z.y + 18} h28" ${line(3)}/>`,
      ggEyes(z.x, z.y - 8, 10) + `<path d="M${z.x - 16},${z.y + 12} q16,22 32,0 z" fill="${INK}"/><path d="M${z.x - 9},${z.y + 13} l3,6 l3,-5 Z" fill="#fff"/>`,
      L.googly(z.x - 14, z.y - 12, 9) + L.googly(z.x + 10, z.y - 16, 11) + L.googly(z.x, z.y + 4, 8),
      ggEyes(z.x, z.y - 6, 10) + `<ellipse cx="${z.x}" cy="${z.y + 18}" rx="6" ry="8" fill="${INK}"/>`,
      ggEyes(z.x, z.y - 6, 12) + `<path d="M${z.x - 14},${z.y + 14} q14,14 28,0" ${line(3)}/><path d="M${z.x - 2},${z.y + 20} q2,10 6,0" fill="${pal('pink')}"/>`,
    ][i] + '</g>').join(''),
  },
];
