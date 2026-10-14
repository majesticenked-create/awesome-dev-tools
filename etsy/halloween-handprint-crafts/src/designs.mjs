// The 30 craft designs. Each zone is where paint goes; `color` is only used
// for the sample (mockup) print. finish() draws what parents add afterwards
// (googly eyes, marker faces) and only appears in mockups.
import * as L from './lib.mjs';
const { INK, os, deco, line, fill, isBW, pal, text } = L;

import { W, PAINT, jackFace, markerSmile } from './helpers.mjs';
import { HAND_B } from './designs-hand.mjs';
import { FEET } from './designs-foot.mjs';
import { FINGERS } from './designs-finger.mjs';

const HAND_A = [
  // ---------------- HANDPRINTS ----------------
  {
    id: 'ghost-hand', kind: 'hand', name: 'Ghost', paint: 'white (on the night sky) or light gray',
    title: [['Hey there, ', 'ink'], ['Boo!', 'orange']],
    caption: 'Hands down, the cutest ghost around',
    zones: [{ type: 'hand', x: 425, y: 470, rot: 180, color: W }],
    back: () => L.nightPanel(110, 215, 630, 650, { seed: 3 }) + L.moon(640, 320, 48) +
      L.bat(200, 300, 1.4, -10) + L.bat(250, 345, 1, 8) + L.bat(620, 780, 1.2, 6),
    finish: () => `<ellipse cx="398" cy="430" rx="12" ry="18" fill="${INK}"/><ellipse cx="452" cy="430" rx="12" ry="18" fill="${INK}"/><ellipse cx="425" cy="490" rx="14" ry="20" fill="${INK}"/>`,
  },
  {
    id: 'spider-hand', kind: 'hand', name: 'Spider', paint: 'black',
    title: [['Spinning Up ', 'ink'], ['Some Fun', 'purple']], titleY: 870,
    caption: 'on the spookiest night of the year', captionY: 940,
    zones: [{ type: 'hand', x: 410, y: 455, rot: 180, color: PAINT.black }],
    back: () => L.web(800, 50, 340, 'tr') +
      `<path d="M640,228 C600,260 470,250 420,345" ${line(2.2)}/>` +
      L.spider(150, 330, 1.3, { thread: 280 }) + L.spider(700, 520, 1, { thread: 0 }) +
      L.scatter([[180, 520, 14, 'orange'], [140, 640, 9, 'purple'], [650, 640, 13, 'orange'], [705, 420, 8, 'purple'], [250, 220, 10, 'ink'], [600, 760, 9, 'ink'], [160, 760, 12, 'orange']]),
    finish: () => L.googly(392, 420, 20, [0.2, 0.3]) + L.googly(440, 420, 20, [0.2, 0.3]) + markerSmile(416, 470, 34, 4) .replace(INK, '#fff'),
  },
  {
    id: 'monster-hand', kind: 'hand', name: 'Monster', paint: 'green',
    title: [["It's ", 'ink'], ['Alive!', 'green']], titleFont: 'spooky', titleSize: 92,
    caption: '...and it wants candy!',
    zones: [{ type: 'hand', x: 425, y: 500, rot: 180, color: PAINT.green }],
    back: () => L.scatter([[160, 300, 14, 'purple'], [700, 280, 12, 'orange'], [170, 640, 10, 'orange'], [690, 650, 15, 'purple'], [140, 470, 7, 'green', 'dot'], [720, 470, 7, 'green', 'dot']]),
    front: () => `<path d="M322,382 L322,332 Q322,312 345,312 L505,312 Q528,312 528,332 L528,382 L512,374 L500,392 L486,374 L468,390 L454,372 L438,394 L422,374 L406,388 L390,372 L374,392 L360,374 L342,390 Z" ${os('dark')}/>` +
      L.bolt(332, 452, 1.25, -1) + L.bolt(518, 452, 1.25, 1),
    finish: () => L.googly(400, 455, 20) + L.googly(452, 455, 20) +
      `<path d="M392,510 q34,24 66,0" ${line(5)}/><path d="M400,420 L450,415 M410,410 l2,16 M424,408 l2,16 M438,406 l2,16" ${line(3)}/>`,
  },
  {
    id: 'pumpkin-hand', kind: 'hand', name: 'Pumpkin', paint: 'orange',
    title: [['Pick of the ', 'ink'], ['Patch', 'orange']],
    caption: 'our sweetest little pumpkin', captionY: 900,
    zones: [{ type: 'hand', x: 425, y: 590, rot: 0, color: PAINT.orange }],
    back: () => `<path d="M120,790 C160,700 300,688 425,694 C560,688 690,700 730,790 Z" ${os('brown')}/>` +
      `<path d="M190,760 q30,-8 60,0 M560,770 q40,-10 80,0 M380,770 q30,-6 60,0" ${line(3, isBW() ? INK : pal('brownLt'))}/>` +
      L.scatter([[180, 260, 14, 'orange'], [680, 250, 12, 'purple'], [160, 420, 9, 'ink'], [700, 400, 15, 'orange'], [250, 330, 7, 'purple', 'dot'], [620, 330, 7, 'orange', 'dot']]),
    front: () => `<path d="M150,700 C120,640 170,600 210,630 M700,700 C730,640 690,600 650,625" ${line(4, isBW() ? INK : pal('greenDk'))}/>` +
      L.curl(205, 628, 1.3, 1) + L.curl(655, 622, 1.3, -1) + L.leaf(150, 660, 1.5, -110) + L.leaf(175, 640, 1.2, -30) +
      L.leaf(700, 660, 1.5, -70) + L.leaf(675, 640, 1.2, -150) +
      L.pumpkin(200, 728, 1.5) + L.pumpkin(655, 735, 1.15) + L.pumpkin(310, 760, 0.8, { faceKind: 'none' }) +
      L.grassTufts(140, 230, 790) + L.grassTufts(610, 720, 790),
    finish: () => jackFace(425, 600, 1.05),
  },
];

export const DESIGNS = [...HAND_A, ...HAND_B, ...FEET, ...FINGERS];
export const byId = Object.fromEntries(DESIGNS.map((d) => [d.id, d]));
