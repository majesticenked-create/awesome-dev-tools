// Footprint designs 16-23. Foot model: toes point to -y, heel at +y.
import * as L from './lib.mjs';
import { W, PAINT, footPt, batWing } from './helpers.mjs';
const { INK, os, line, isBW, pal } = L;

const ovalEyes = (x, y, gap = 16, rx = 8, ry = 12) => `<ellipse cx="${x - gap}" cy="${y}" rx="${rx}" ry="${ry}" fill="${INK}"/><ellipse cx="${x + gap}" cy="${y}" rx="${rx}" ry="${ry}" fill="${INK}"/>`;
const wing = (x, y, side, h = 240, c = 'dark') => // folded scalloped wing hugging the sole
  `<path transform="translate(${x} ${y}) scale(${side} 1)" d="M0,0 C40,-10 78,10 86,50 C70,60 66,80 74,100 C56,104 50,124 58,146 C40,148 30,168 34,${h - 50} C22,${h - 40} 10,${h - 20} 0,${h} Z" ${os(c)}/>`;
const spreadWing = (x, y, side, c = 'dark') =>
  `<path transform="translate(${x} ${y}) scale(${side} 1)" d="M0,-50 C40,-96 140,-104 196,-60 C176,-40 172,-6 178,28 C150,8 118,14 104,44 C90,16 60,14 46,42 C38,16 18,6 0,14 Z M30,-58 C70,-40 100,-10 104,44 M30,-58 C40,-20 44,10 46,42" ${os(c)}/>`;
const arm = (x, y, side, c = 'green') => `<g transform="translate(${x} ${y}) scale(${side} 1)">
  <path d="M0,0 C30,-6 60,-30 74,-62 L90,-56 C76,-20 44,10 0,20 Z" ${os(c)}/>
  <path d="M74,-62 l-8,-22 M82,-60 l2,-24 M88,-56 l14,-16" ${line(5)}/></g>`;

export const FEET = [
  {
    id: 'ghost-feet', kind: 'foot', name: 'Ghost Toes (two feet)', paint: 'white (on the night sky) or light gray',
    title: [['Little ', 'ink'], ['Ghost', 'purple'], [' Toes', 'ink']],
    caption: 'Two little ghosts came out to play',
    zones: [{ type: 'foot', x: 315, y: 530, rot: 180, s: 0.95, color: W }, { type: 'foot', x: 535, y: 530, rot: 180, s: 0.95, mirror: true, color: W }],
    back: () => L.nightPanel(115, 220, 620, 600, { seed: 5 }) + L.moon(425, 276, 34) + L.bat(200, 280, 1.2, -8) + L.bat(660, 290, 1.1, 8),
    finish: () => ovalEyes(315, 410) + `<ellipse cx="315" cy="456" rx="9" ry="13" fill="${INK}"/>` + ovalEyes(535, 410) + `<path d="M520,450 q15,14 30,0" ${line(4)}/>`,
  },
  {
    id: 'bat-foot', kind: 'foot', name: 'Upside-Down Bat', paint: 'black or gray',
    title: [['Hang in ', 'ink'], ['There!', 'purple']],
    caption: 'Happy Halloween from your little bat',
    zones: [{ type: 'foot', x: 425, y: 545, color: PAINT.black }],
    back: () => L.moon(660, 790, 52) + `<path d="M100,300 C260,320 560,300 750,316 L750,334 C560,320 260,340 100,320 Z" ${os('brown')}/>` +
      L.leaf(160, 318, 1.4, -160) + L.leaf(700, 330, 1.3, 30) + L.leaf(560, 322, 1.1, 150) +
      L.scatter([[180, 690, 12, 'orange'], [150, 400, 9, 'purple'], [700, 690, 11, 'orange'], [230, 790, 8, 'ink'], [700, 400, 9, 'purple']]),
    front: () => spreadWing(352, 520, -1) + spreadWing(498, 520, 1) +
      `<path d="M395,712 L388,766 L414,728 Z M455,712 L462,766 L436,728 Z" ${os('dark')}/>`,
    finish: () => `<circle cx="408" cy="650" r="10" fill="#fff"/><circle cx="442" cy="650" r="10" fill="#fff"/><circle cx="408" cy="652" r="5" fill="${INK}"/><circle cx="442" cy="652" r="5" fill="${INK}"/>` +
      `<path d="M410,624 q15,-12 30,0" fill="none" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/><path d="M414,621 l3,-9 l3,8 M430,621 l3,-8 l3,9" fill="#fff" stroke="#fff" stroke-width="1"/>`,
  },
  {
    id: 'broom-foot', kind: 'foot', name: "Witch's Broom", paint: 'yellow, orange or brown',
    title: [['Broom, ', 'ink'], ['Broom!', 'purple']],
    caption: 'Watch this little witch zoom!',
    zones: [{ type: 'foot', x: 420, y: 650, rot: 200, color: PAINT.yellow }],
    back: () => L.moon(190, 280, 54) + L.bat(290, 250, 1.1, -6) + L.bat(250, 320, 0.8, 8) +
      L.scatter([[300, 820, 13, 'orange'], [230, 760, 9, 'yellow', 'sparkle'], [180, 860, 11, 'purple'], [340, 880, 7, 'orange', 'dot'], [140, 700, 8, 'yellow', 'sparkle']]),
    front: () => {
      const [hx, hy] = footPt({ x: 420, y: 650, rot: 200 }, 0, 186);
      const dx = 0.342, dy = -0.94, ex = hx + dx * 170, ey = hy + dy * 170;
      return `<path d="M${hx + dx * 6},${hy + dy * 6} L${ex},${ey}" stroke="${INK}" stroke-width="22" stroke-linecap="round"/><path d="M${hx + dx * 6},${hy + dy * 6} L${ex},${ey}" stroke="${isBW() ? '#fff' : pal('brown')}" stroke-width="15" stroke-linecap="round"/>` +
        `<g transform="translate(${hx + dx * 18} ${hy + dy * 18}) rotate(20)"><rect x="-26" y="-9" width="52" height="18" rx="6" ${os('purple', 3.5)}/></g>` +
        L.star(ex + 50, ey + 10, 14, 'yellow') + L.sparkle(ex - 40, ey + 30, 12, 'yellow');
    },
  },
  {
    id: 'monster-foot', kind: 'foot', name: 'Big Foot Monster', paint: 'green, blue or purple',
    title: [['Big Feet, ', 'ink'], ['Little Monster', 'green']], titleSize: 64,
    caption: 'Stomping into Halloween!',
    zones: [{ type: 'foot', x: 425, y: 565, color: PAINT.lime }],
    back: () => L.scatter([[160, 280, 13, 'purple'], [700, 260, 12, 'orange'], [140, 700, 10, 'orange'], [720, 720, 14, 'purple'], [230, 820, 7, 'green', 'dot'], [630, 830, 7, 'green', 'dot']]) +
      L.eyeball(180, 470, 18, [0.3, 0]) + L.eyeball(690, 460, 15, [-0.3, 0]),
    front: () => arm(345, 560, -1) + arm(505, 560, 1) +
      `<path d="M370,760 l-10,22 M392,764 l-4,24 M458,764 l4,24 M480,760 l10,22" ${line(5)}/>`,
    finish: () => L.googly(408, 470, 22) + L.googly(452, 480, 16) + `<path d="M380,560 q45,50 90,0 z" fill="${INK}"/><path d="M392,566 l7,12 l7,-11 Z M440,567 l7,11 l7,-12 Z" fill="#fff"/>`,
  },
  {
    id: 'candycorn-foot', kind: 'foot', name: 'Candy Corn Foot', paint: 'white heel, orange middle, yellow toes',
    title: [['Sweet ', 'ink'], ['Feet', 'orange']], titleSize: 80,
    caption: "Trick or treat, I'm extra sweet!",
    zones: [{ type: 'foot', x: 425, y: 545, rot: 180, color: PAINT.yellow, bands: [['#FFF6DF', 95, 200], [PAINT.orange, -15, 95], [PAINT.yellow, -220, -15]], toeColor: PAINT.yellow }],
    back: () => L.candyCorn(170, 300, 2, -20) + L.candyCorn(690, 330, 1.7, 22) + L.candyCorn(150, 620, 1.4, 10) + L.candyCorn(700, 640, 1.9, -12) +
      L.wrappedCandy(240, 800, 1.4, 'purple', -15) + L.wrappedCandy(610, 810, 1.3, 'green', 15) + L.lollipop(700, 470, 1.1, 'red', 12) +
      L.scatter([[260, 450, 9, 'purple'], [600, 240, 8, 'orange', 'dot'], [300, 240, 7, 'purple', 'dot']]),
  },
  {
    id: 'owl-foot', kind: 'foot', name: 'Owl', paint: 'brown, purple or gray',
    title: [['Whooo', 'purple'], ["'s Ready for", 'ink']], title2: [['Halloween?', 'orange']], titleSize: 62, titleY: 125,
    caption: 'Hoot hoot, happy Halloween!',
    zones: [{ type: 'foot', x: 425, y: 545, color: '#9A6740' }],
    back: () => L.moon(660, 330, 56) + L.bat(200, 300, 1.2, -6) +
      `<path d="M150,750 C300,742 560,748 720,762 L720,780 C560,768 300,764 150,770 Z" ${os('brown')}/>` + L.leaf(690, 770, 1.3, 20) + L.leaf(190, 760, 1.2, -170),
    front: () => `<path transform="translate(347 470)" d="M0,0 C-50,20 -66,110 -40,200 C-30,170 -14,150 0,140 Z" ${os('purple')}/><path transform="translate(503 470) scale(-1 1)" d="M0,0 C-50,20 -66,110 -40,200 C-30,170 -14,150 0,140 Z" ${os('purple')}/>` +
      `<path d="M395,742 l-6,18 M405,744 l0,18 M445,744 l0,18 M455,742 l6,18" ${line(5, isBW() ? INK : pal('orange'))}/>`,
    finish: () => `<circle cx="398" cy="470" r="34" fill="#fff" stroke="${pal('orange')}" stroke-width="7"/><circle cx="456" cy="470" r="34" fill="#fff" stroke="${pal('orange')}" stroke-width="7"/>` +
      `<circle cx="404" cy="474" r="14" fill="${INK}"/><circle cx="450" cy="474" r="14" fill="${INK}"/><circle cx="400" cy="469" r="4" fill="#fff"/><circle cx="446" cy="469" r="4" fill="#fff"/>` +
      `<path d="M417,505 l10,22 l10,-22 z" fill="${pal('orange')}" stroke="${INK}" stroke-width="2"/>` +
      `<path d="M395,580 l10,10 l10,-10 M435,580 l10,10 l10,-10 M415,620 l10,10 l10,-10" fill="none" stroke="#F3E3C8" stroke-width="3.5" stroke-linecap="round"/>`,
  },
  {
    id: 'mummy-foot', kind: 'foot', name: 'Mummy', paint: 'white or light gray',
    title: [['Mummy', 'purple'], ["'s Little Treasure", 'ink']], titleSize: 62,
    caption: 'Loved to pieces (and bandages!)',
    zones: [{ type: 'foot', x: 425, y: 545, rot: 180, color: '#DCD8D0' }],
    back: () => L.spider(680, 300, 1.2, { thread: 110 }) + L.web(60, 200, 210, 'tl') +
      L.scatter([[700, 520, 12, 'orange'], [140, 560, 10, 'purple'], [700, 780, 13, 'purple'], [160, 790, 11, 'orange']]),
    front: () => `<g transform="translate(362 500)"><rect x="-110" y="-22" width="112" height="44" rx="20" ${os('bone')}/><path d="M-90,-22 l-8,44 M-66,-22 l-10,44 M-40,-22 l-8,44 M-16,-22 l-6,44" ${line(2.5)}/></g>` +
      `<g transform="translate(488 500)"><rect x="-2" y="-22" width="112" height="44" rx="20" ${os('bone')}/><path d="M20,-22 l8,44 M44,-22 l10,44 M70,-22 l8,44 M94,-22 l6,44" ${line(2.5)}/></g>`,
    finish: () => `<path d="M352,560 L498,540 M350,610 L500,590 M356,660 L494,640 M362,700 L480,694 M372,470 L478,450" ${line(3)}/>` +
      `<rect x="370" y="408" width="110" height="34" rx="16" fill="${INK}"/><circle cx="403" cy="425" r="11" fill="${pal('yellow')}"/><circle cx="447" cy="425" r="11" fill="${pal('yellow')}"/><circle cx="405" cy="427" r="5" fill="${INK}"/><circle cx="449" cy="427" r="5" fill="${INK}"/>`,
  },
  {
    id: 'trickortreat-feet', kind: 'foot', name: 'Smell My Feet (two feet)', paint: 'orange + black (or any two colors)',
    title: [['Trick or Treat,', 'ink']], title2: [['Smell My Feet!', 'orange']], titleSize: 70, titleY: 130,
    caption: 'Give me something good to eat!', captionY: 945,
    zones: [{ type: 'foot', x: 285, y: 520, color: PAINT.orange }, { type: 'foot', x: 565, y: 520, mirror: true, color: PAINT.black }],
    back: () => L.scatter([[120, 330, 12, 'purple'], [740, 330, 12, 'purple'], [130, 640, 9, 'orange'], [720, 620, 10, 'orange']]),
    front: () => L.treatBucket(425, 800, 1.15) + L.wrappedCandy(310, 800, 1.2, 'purple', -20) + L.lollipop(545, 770, 1, 'red', 18) +
      L.candyCorn(230, 790, 1.2, -15) + L.candyCorn(620, 810, 1.1, 20) + L.wrappedCandy(425, 690, 1, 'green', 0),
  },
];
