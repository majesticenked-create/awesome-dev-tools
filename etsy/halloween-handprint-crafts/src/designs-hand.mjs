// Handprint designs 5-15.
import * as L from './lib.mjs';
import { W, PAINT, tip, batWing, crow, cornStalk } from './helpers.mjs';
const { INK, os, line, isBW, pal, text } = L;

const bandage = (d, w = 24) =>
  `<path d="${d}" fill="none" stroke="${INK}" stroke-width="${w + 7}" stroke-linecap="round" stroke-linejoin="round"/>` +
  `<path d="${d}" fill="none" stroke="${isBW() ? '#fff' : pal('bone')}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`;
const mummyWraps = (pts) => pts.map(([x1, y1, x2, y2]) => `<path d="M${x1},${y1} L${x2},${y2}" ${line(3)}/>`).join('');

export const HAND_B = [
  {
    id: 'vampire-hand', kind: 'hand', name: 'Vampire', paint: 'purple or lavender',
    title: [['Fang', 'purple'], ['-tastic!', 'ink']],
    caption: 'I want to suck your... juice box!',
    zones: [{ type: 'hand', x: 410, y: 590, color: PAINT.purple }],
    back: () => L.moon(665, 300, 58) + L.bat(640, 400, 1.3, -8) + L.bat(700, 440, 0.9, 10) +
      L.scatter([[170, 300, 14, 'orange'], [150, 470, 9, 'purple'], [230, 220, 7, 'ink'], [690, 560, 10, 'orange']]),
    front: () => `<path d="M205,850 C222,770 270,722 334,704 L486,704 C550,722 598,770 615,850 Z" ${os('dark')}/>` +
      `<path d="M330,708 L258,616 C294,628 326,660 352,698 Z" ${os('red')}/><path d="M490,708 L562,616 C526,628 494,660 468,698 Z" ${os('red')}/>` +
      `<path d="M372,706 L410,782 L448,706 Z" ${os('white')}/>` +
      `<path d="M386,738 L410,750 L434,738 L434,770 L410,758 L386,770 Z" ${os('red', 3)}/><circle cx="410" cy="754" r="7" ${os('red', 3)}/>`,
    finish: () => L.googly(388, 572, 17) + L.googly(436, 572, 17) +
      `<path d="M378,628 q34,22 68,0" ${line(4.5)}/><path d="M386,634 l6,18 l6,-14 Z M426,638 l6,14 l6,-18 Z" fill="#fff" stroke="${INK}" stroke-width="2.5" stroke-linejoin="round"/>`,
  },
  {
    id: 'mummy-hand', kind: 'hand', name: 'Mummy', paint: 'white or light gray',
    title: [['Unwrap ', 'ink'], ['the Fun!', 'purple']],
    caption: "Happy Halloween from mummy's little monster",
    zones: [{ type: 'hand', x: 400, y: 590, color: '#DCD8D0' }],
    back: () => L.web(60, 200, 230, 'tl') + L.web(790, 200, 230, 'tr') +
      L.spider(150, 470, 1.1, { thread: 130 }) + L.spider(700, 450, 1, { thread: 110 }) +
      L.scatter([[160, 620, 12, 'orange'], [690, 620, 13, 'purple'], [720, 700, 7, 'orange', 'dot'], [130, 700, 8, 'ink']]),
    front: () => L.pumpkin(170, 790, 1.4) + L.ghost(680, 785, 1.25) + L.candyCorn(250, 815, 1.2, -15) + L.candyCorn(600, 815, 1.2, 15),
    finish: () => {
      const z = { type: 'hand', x: 400, y: 590 };
      let wraps = mummyWraps([[300, 520, 498, 492], [296, 570, 500, 548], [306, 640, 494, 610], [320, 686, 470, 676]]);
      for (let i = 0; i < 5; i++) { const [x, y] = tip(z, i, 2.2); const [x2, y2] = tip(z, i, 3.2); wraps += `<path d="M${x - 20},${y + 4} L${x + 20},${y - 4} M${x2 - 20},${y2 + 6} L${x2 + 20},${y2 - 2}" ${line(3)}/>`; }
      return wraps + `<rect x="345" y="532" width="110" height="34" rx="16" fill="${INK}"/>` +
        `<circle cx="378" cy="549" r="11" fill="${pal('yellow')}"/><circle cx="422" cy="549" r="11" fill="${pal('yellow')}"/><circle cx="380" cy="551" r="5" fill="${INK}"/><circle cx="424" cy="551" r="5" fill="${INK}"/>`;
    },
  },
  {
    id: 'cat-hand', kind: 'hand', name: 'Black Cat', paint: 'black',
    title: [['Purr', 'purple'], ['-fectly Spooky', 'ink']],
    caption: 'Feline fine this Halloween!',
    zones: [{ type: 'hand', x: 350, y: 525, rot: 180, color: PAINT.black }],
    back: () => L.moon(650, 290, 62) + L.bat(220, 260, 1.3, -6) + L.bat(280, 300, 0.9, 10) +
      `<path d="M110,820 Q425,790 740,820" ${line(4)}/>` + L.grassTufts(120, 740, 818) +
      L.scatter([[150, 400, 10, 'orange'], [720, 450, 12, 'purple'], [760, 600, 8, 'orange']]),
    front: () => `<g transform="translate(565 430)">
        <path d="M-58,-30 L-66,-92 L-18,-58 Z M58,-30 L66,-92 L18,-58 Z" ${os('dark')}/>
        <path d="M-50,-44 L-55,-76 L-30,-56 Z M50,-44 L55,-76 L30,-56 Z" fill="${isBW() ? '#fff' : pal('pink')}"/>
        <ellipse cx="0" cy="0" rx="74" ry="64" ${os('dark')}/>
        <ellipse cx="-26" cy="-6" rx="15" ry="18" ${os('yellow', 3)}/><ellipse cx="26" cy="-6" rx="15" ry="18" ${os('yellow', 3)}/>
        <ellipse cx="-26" cy="-4" rx="5" ry="12" fill="${INK}"/><ellipse cx="26" cy="-4" rx="5" ry="12" fill="${INK}"/>
        <path d="M-6,16 L6,16 L0,23 Z" fill="${isBW() ? INK : pal('pink')}"/>
        <path d="M0,23 q-8,10 -16,4 M0,23 q8,10 16,4" fill="none" stroke="${isBW() ? INK : '#fff'}" stroke-width="3" stroke-linecap="round"/>
        <path d="M-40,18 L-92,8 M-40,26 L-90,32 M40,18 L92,8 M40,26 L90,32" fill="none" stroke="${isBW() ? INK : '#fff'}" stroke-width="2.5" stroke-linecap="round"/>
      </g>` + L.pumpkin(670, 780, 1.1),
  },
  {
    id: 'witch-hand', kind: 'hand', name: 'Witch', paint: 'green palm + purple or orange fingers',
    title: [['Cutest ', 'ink'], ['Witch', 'purple'], [' in Town', 'ink']], titleSize: 66,
    caption: 'Brewing up some Halloween fun',
    zones: [{ type: 'hand', x: 455, y: 545, rot: 180, color: PAINT.green, fingerColor: PAINT.purple, thumbColor: PAINT.purple }],
    back: () => L.moon(690, 290, 50) + L.scatter([[160, 280, 13, 'orange'], [740, 420, 10, 'purple'], [130, 480, 9, 'ink'], [700, 760, 12, 'orange']]) +
      L.bat(170, 380, 1.1, -10),
    front: () => L.witchHat(445, 412, 1.55) + L.cauldron(165, 770, 0.95) +
      `<circle cx="145" cy="690" r="9" ${os('lime', 3)}/><circle cx="175" cy="665" r="6" ${os('lime', 3)}/>`,
    finish: () => L.face(445, 520, 2.6) + `<circle cx="485" cy="548" r="4" fill="${INK}" opacity="0.7"/>`,
  },
  {
    id: 'bat-hands', kind: 'hand', name: 'Bat (two hands)', paint: 'black or gray', orient: 'landscape',
    title: [['Going ', 'ink'], ['Batty', 'purple'], [' for Halloween!', 'ink']], titleSize: 68,
    caption: 'Hang out with me anytime', captionY: 680, nameY: 785,
    zones: [{ type: 'hand', x: 372, y: 440, rot: -90, color: PAINT.black }, { type: 'hand', x: 728, y: 440, rot: 90, mirror: true, color: PAINT.black }],
    back: () => L.moon(960, 170, 44) + L.scatter([[130, 170, 13, 'orange'], [90, 600, 10, 'purple'], [1000, 600, 12, 'orange'], [560, 610, 8, 'ink'], [200, 640, 7, 'orange', 'dot'], [900, 650, 7, 'purple', 'dot']]),
    front: () => `<g transform="translate(550 440)">
        <path d="M-36,-58 L-44,-104 L-10,-72 Z M36,-58 L44,-104 L10,-72 Z" ${os('dark')}/>
        <ellipse cx="0" cy="0" rx="58" ry="80" ${os('dark')}/>
        <ellipse cx="0" cy="22" rx="34" ry="44" fill="${isBW() ? '#fff' : pal('nightLt')}" stroke="${isBW() ? INK : 'none'}" stroke-width="2.5"/>
        <circle cx="-18" cy="-28" r="13" fill="#fff" stroke="${INK}" stroke-width="2.5"/><circle cx="18" cy="-28" r="13" fill="#fff" stroke="${INK}" stroke-width="2.5"/>
        <circle cx="-16" cy="-25" r="6" fill="${INK}"/><circle cx="20" cy="-25" r="6" fill="${INK}"/>
        <path d="M-12,-6 q12,10 24,0" fill="none" stroke="${isBW() ? INK : '#fff'}" stroke-width="3" stroke-linecap="round"/>
        <path d="M-7,-3 l3,8 l3,-6 M4,-3 l3,6 l3,-8" fill="#fff" stroke="${INK}" stroke-width="1.5"/>
        ${isBW() ? '' : `<ellipse cx="-30" cy="-8" rx="7" ry="4" fill="${pal('pink')}" opacity="0.8"/><ellipse cx="30" cy="-8" rx="7" ry="4" fill="${pal('pink')}" opacity="0.8"/>`}
        <path d="M-20,78 l-6,14 M-14,80 l0,14 M14,80 l0,14 M20,78 l6,14" ${line(4)}/>
      </g>`,
  },
  {
    id: 'skeleton-hand', kind: 'hand', name: 'Skeleton', paint: 'white (on the black panel)',
    title: [['Bone', 'orange'], ['-afide Cutie!', 'ink']],
    caption: 'Happy Hallo-scream!',
    zones: [{ type: 'hand', x: 400, y: 590, color: W }],
    back: () => L.nightPanel(150, 225, 550, 590, { color: 'dark', seed: 7 }) +
      [[205, 285, 20], [645, 285, -20], [210, 760, -15], [640, 760, 15]].map(([x, y, r]) =>
        `<g transform="translate(${x} ${y}) rotate(${r})"><path d="M-22,0 H22" stroke="${isBW() ? INK : '#fff'}" stroke-width="7" stroke-linecap="round"/><circle cx="-24" cy="-4" r="5" fill="${isBW() ? '#fff' : '#fff'}" stroke="${INK}" stroke-width="${isBW() ? 2 : 0}"/><circle cx="-24" cy="4" r="5" fill="#fff" stroke="${INK}" stroke-width="${isBW() ? 2 : 0}"/><circle cx="24" cy="-4" r="5" fill="#fff" stroke="${INK}" stroke-width="${isBW() ? 2 : 0}"/><circle cx="24" cy="4" r="5" fill="#fff" stroke="${INK}" stroke-width="${isBW() ? 2 : 0}"/></g>`).join(''),
    finish: () => {
      const z = { type: 'hand', x: 400, y: 590 };
      let bones = '';
      for (let i = 0; i < 4; i++) {
        const [x1, y1] = tip(z, i, 0.6), [x2, y2] = tip(z, i, 3.6);
        bones += `<path d="M${x1},${y1} L${x2},${y2}" stroke="${INK}" stroke-width="5" stroke-linecap="round" stroke-dasharray="26 12"/>`;
      }
      return bones + `<ellipse cx="370" cy="575" rx="22" ry="25" fill="${INK}"/><ellipse cx="430" cy="575" rx="22" ry="25" fill="${INK}"/><path d="M400,598 l-9,16 h18 z" fill="${INK}"/>` +
        `<path d="M362,640 h76 M372,630 v20 M386,630 v20 M400,630 v20 M414,630 v20 M428,630 v20" ${line(3.5)}/>`;
    },
  },
  {
    id: 'eyes-hand', kind: 'hand', name: 'Many-Eyed Monster', paint: 'purple, green or blue',
    title: [['Eye ', 'ink'], ['Love', 'purple'], [' You!', 'ink']],
    caption: '...a monster-sized amount',
    zones: [{ type: 'hand', x: 395, y: 600, color: PAINT.purple }],
    back: () => L.heart(170, 300, 1.6, 'red') + L.heart(690, 260, 1.2, 'pink') + L.heart(720, 640, 1.5, 'red') + L.heart(140, 680, 1.1, 'pink') +
      L.eyeball(200, 480, 16, [0.3, 0]) + L.eyeball(700, 450, 20, [-0.3, 0.1]) + L.eyeball(640, 800, 13) +
      L.scatter([[260, 230, 9, 'orange'], [600, 220, 11, 'orange'], [180, 800, 12, 'purple']]),
    finish: () => {
      const z = { type: 'hand', x: 395, y: 600 };
      let out = '';
      [0, 1, 2, 3, 4].forEach((i) => { const [x, y] = tip(z, i, 0.7); out += L.googly(x, y, i === 2 ? 22 : 18, [i < 2 ? -0.2 : 0.2, 0.2]); });
      return out + `<path d="M345,620 q50,50 100,0 z" fill="${INK}"/><path d="M360,626 l8,14 l8,-12 Z M414,628 l8,12 l8,-14 Z" fill="#fff"/>`;
    },
  },
  {
    id: 'scarecrow-hand', kind: 'hand', name: 'Scarecrow', paint: 'tan or peach palm + yellow fingers',
    title: [['Scare', 'orange'], ['-ly Adorable', 'ink']],
    caption: 'Happy Harvest & Happy Halloween',
    zones: [{ type: 'hand', x: 455, y: 545, rot: 180, color: '#F2C994', fingerColor: PAINT.yellow, thumbColor: PAINT.yellow }],
    back: () => cornStalk(150, 830, 420, 1) + cornStalk(720, 830, 380, -1) + crow(220, 290, 1.4) + crow(660, 260, 1.2, -1) +
      L.scatter([[330, 240, 9, 'orange'], [560, 230, 11, 'orange']]),
    front: () => `<g transform="translate(450 410)">
        <path d="M-118,4 C-90,-18 90,-18 118,4 C96,22 -96,22 -118,4 Z" ${os('tan')}/>
        <path d="M-66,-2 C-70,-60 -40,-104 4,-104 C48,-104 70,-60 66,-2 Z" ${os('tan')}/>
        <path d="M-68,-20 C-30,-10 30,-10 68,-20 L66,-2 C30,8 -30,8 -66,-2 Z" ${os('red', 3.5)}/>
        <rect x="16" y="-80" width="30" height="28" rx="3" ${os('purple', 3)}/><path d="M20,-74 h22 M20,-66 h22 M20,-58 h22" stroke="${INK}" stroke-width="1.5" stroke-dasharray="3 3"/>
        <path d="M-100,6 l-14,16 M-80,12 l-6,18 M80,12 l6,18 M100,6 l14,16" ${line(3.5, isBW() ? INK : pal('yellow'))}/>
      </g>`,
    finish: () => `<circle cx="420" cy="500" r="11" fill="${INK}"/><circle cx="470" cy="500" r="11" fill="${INK}"/><circle cx="417" cy="497" r="3" fill="#fff"/><circle cx="467" cy="497" r="3" fill="#fff"/>` +
      `<path d="M445,515 l-12,22 h24 z" fill="${pal('orange')}" stroke="${INK}" stroke-width="2"/>` +
      `<path d="M408,556 q37,26 74,0" ${line(4)}/><path d="M418,552 l-4,12 M434,560 l-2,12 M450,562 l0,12 M466,560 l2,12 M476,552 l4,12" ${line(2.5)}/>` +
      `<ellipse cx="398" cy="530" rx="11" ry="7" fill="${pal('pink')}"/><ellipse cx="492" cy="530" rx="11" ry="7" fill="${pal('pink')}"/>`,
  },
  {
    id: 'candycorn-hand', kind: 'hand', name: 'Candy Corn', paint: 'yellow palm, orange fingers, white fingertips',
    title: [['Sweet as ', 'ink'], ['Candy Corn', 'orange']], titleSize: 68,
    caption: 'A sweet little treat for you!',
    zones: [{ type: 'hand', x: 395, y: 610, color: PAINT.yellow, fingerColor: PAINT.orange, thumbColor: PAINT.orange, tipColor: '#FFF6DF' }],
    back: () => L.candyCornGarland(110, 740, 205, 22) +
      L.candyCorn(160, 420, 1.6, -20) + L.candyCorn(700, 380, 1.4, 18) + L.candyCorn(150, 640, 1.2, 15) +
      L.wrappedCandy(690, 560, 1.4, 'purple', -20) + L.lollipop(190, 790, 1.2, 'red', -12) +
      L.scatter([[260, 330, 9, 'purple'], [640, 300, 8, 'orange', 'dot'], [720, 470, 7, 'purple', 'dot']]),
    front: () => L.treatBucket(680, 770, 1.15) + L.wrappedCandy(600, 812, 1, 'green', 10),
  },
  {
    id: 'tree-hand', kind: 'hand', name: 'Spooky Tree + Bats', paint: 'brown (hand) + black (fingerprints)',
    title: [['Spooky ', 'ink'], ['Season', 'orange']],
    caption: 'Spooky, sweet & one of a kind',
    zones: [
      { type: 'hand', x: 395, y: 560, color: PAINT.brown },
      { type: 'finger', x: 190, y: 330, r: 32, color: PAINT.black }, { type: 'finger', x: 165, y: 520, r: 32, color: PAINT.black },
      { type: 'finger', x: 680, y: 470, r: 32, color: PAINT.black }, { type: 'finger', x: 560, y: 245, r: 32, color: PAINT.black },
    ],
    back: () => L.moon(690, 300, 56) +
      `<path d="M120,830 C220,760 630,760 730,830 Z" ${os('dark')}/>` +
      `<path d="M352,672 C352,720 344,760 318,800 L478,800 C450,760 440,720 440,672 Z" ${os('brown')}/>` +
      `<path d="M378,700 q6,30 -4,70 M414,700 q-4,40 8,80" ${line(3)}/>`,
    front: () => [[190, 330], [165, 520], [680, 470], [560, 245]].map(([x, y]) => batWing(x, y, 32, -1) + batWing(x, y, 32, 1)).join('') +
      L.tombstone(210, 780, 1.3, 'BOO') + L.pumpkin(620, 790, 1.1) + L.pumpkin(680, 805, 0.8, { faceKind: 'none' }),
    finish: () => [[190, 330], [165, 520], [680, 470], [560, 245]].map(([x, y]) => `<circle cx="${x - 8}" cy="${y - 4}" r="5" fill="#fff"/><circle cx="${x + 8}" cy="${y - 4}" r="5" fill="#fff"/><circle cx="${x - 7}" cy="${y - 3}" r="2.2" fill="${INK}"/><circle cx="${x + 9}" cy="${y - 3}" r="2.2" fill="${INK}"/>`).join(''),
  },
  {
    id: 'keepsake-hand', kind: 'hand', name: 'All About My Halloween (keepsake)', paint: 'any color',
    title: [['My ', 'ink'], ['Halloween', 'orange'], [' Handprint', 'ink']], titleSize: 60,
    caption: 'Little hands, big Halloween memories', captionY: 935,
    zones: [{ type: 'hand', x: 290, y: 600, color: PAINT.orange }],
    back: () => L.scatter([[110, 240, 10, 'purple'], [740, 230, 12, 'orange'], [480, 250, 8, 'ink']]),
    front: () => L.pumpkin(170, 820, 1.4) + L.ghost(420, 815, 1.15) + L.candyCorn(545, 830, 1.4, 15) + L.pumpkin(660, 830, 1.05) +
      L.bat(640, 245, 1.2, -6) + L.bat(330, 790, 0.9, 6),
    extra: (ctx) => {
      const qs = ['I am ___ years old', 'My costume:', 'Favorite candy:', 'Trick-or-treating with:', 'Best part of Halloween:'];
      let out = '', y = 360;
      for (const q of qs) {
        if (q.includes('___')) {
          out += text(540, y, 'I am', { size: 28, anchor: 'start' }) + `<line x1="600" y1="${y + 4}" x2="650" y2="${y + 4}" stroke="${INK}" stroke-width="1.6"/>` + text(660, y, 'years old', { size: 28, anchor: 'start' });
          ctx.fields.push({ name: 'age_q', x: 602, y: y - 26, w: 46, h: 30 });
          y += 84; continue;
        }
        out += text(540, y, q, { size: 28, anchor: 'start', color: isBW() ? 'ink' : 'purpleDk' });
        out += `<line x1="540" y1="${y + 44}" x2="790" y2="${y + 44}" stroke="${INK}" stroke-width="1.6"/>`;
        ctx.fields.push({ name: q, x: 542, y: y + 14, w: 246, h: 30 });
        y += 98;
      }
      return out;
    },
  },
];
