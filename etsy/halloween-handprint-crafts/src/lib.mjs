// Drawing library for the Halloween handprint printables.
// Units: 1 unit = 0.01 inch. Portrait pages are 850 x 1100 (US Letter).
// Every function returns an SVG string. Colors go through `fill()` so the
// same artwork renders in full color or as an ink-saving coloring page.

export const INK = '#2B2530';
export const SW = 4; // default outline width

const PALETTE = {
  orange: '#F5893A', orangeDk: '#DE6A1F', yellow: '#FFD24A', cream: '#FFF3D1',
  purple: '#8B68C8', purpleDk: '#5B4296', lavender: '#CDB9EE', green: '#86C34A',
  greenDk: '#4E8C2E', lime: '#B6E07A', night: '#2F2B52', nightLt: '#46407A',
  moon: '#FFE8A3', brown: '#9A6740', brownLt: '#C9915F', tan: '#E9C891',
  pink: '#F6A5B9', red: '#E2453C', gray: '#9C98A3', grayLt: '#DAD6DE',
  white: '#FFFFFF', black: '#2B2530', dark: '#353040', bone: '#F4EFE6', teal: '#6CC3B5',
};

let MODE = 'color';
export function setMode(m) { MODE = m; }
export function getMode() { return MODE; }
export const isBW = () => MODE === 'bw';

// Fill for a colorable shape. In BW mode everything colorable turns white.
export function fill(name) {
  if (isBW()) return name === 'ink' ? INK : '#FFFFFF';
  if (name === 'ink') return INK;
  return PALETTE[name] || name;
}
export const pal = (n) => PALETTE[n] || n;

// Attributes for an outlined (kawaii) shape.
export function os(color, w = SW) {
  return `fill="${fill(color)}" stroke="${INK}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="round"`;
}
// Attributes for a small decoration: flat color in color mode, outlined in BW.
export function deco(color, w = 2.5) {
  if (isBW()) return color === 'ink'
    ? `fill="${INK}"`
    : `fill="#fff" stroke="${INK}" stroke-width="${w}" stroke-linejoin="round"`;
  return `fill="${fill(color)}"`;
}
export const line = (w = SW, color = INK) =>
  `fill="none" stroke="${color}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"`;

let UID = 0;
export const uid = (p = 'u') => `${p}${++UID}`;

export const g = (t, c) => `<g transform="${t}">${c}</g>`;
export const at = (x, y, s = 1, r = 0) =>
  `translate(${x} ${y})${r ? ` rotate(${r})` : ''}${s !== 1 ? ` scale(${s})` : ''}`;

// ---------- text ----------
export const FONTS = {
  title: "'Grandstander', sans-serif",
  hand: "'Patrick Hand', sans-serif",
  spooky: "'Creepster', cursive",
  round: "'Fredoka', sans-serif",
};
export function text(x, y, str, { size = 40, font = 'hand', weight = 400, color = 'ink', anchor = 'middle', ls = 0, outline = false, extra = '' } = {}) {
  const f = FONTS[font] || font;
  let paint;
  if (outline && isBW()) paint = `fill="#fff" stroke="${INK}" stroke-width="${Math.max(2, size / 22)}" paint-order="stroke"`;
  else paint = `fill="${color === 'ink' ? INK : (isBW() ? INK : pal(color))}"`;
  return `<text x="${x}" y="${y}" font-family="${f}" font-size="${size}" font-weight="${weight}" text-anchor="${anchor}" letter-spacing="${ls}" ${paint} ${extra}>${esc(str)}</text>`;
}
export const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

// Rich title: array of [string, color] segments laid out as one centered line.
export function title(x, y, segs, { size = 72, font = 'title', weight = 900, ls = 0 } = {}) {
  if (typeof segs === 'string') segs = [[segs, 'ink']];
  const f = FONTS[font] || font;
  const spans = segs.map(([s, c]) => {
    const colored = c !== 'ink';
    const paint = colored && isBW()
      ? `fill="#fff" stroke="${INK}" stroke-width="${size / 20}" paint-order="stroke"`
      : `fill="${c === 'ink' ? INK : pal(c)}"`;
    return `<tspan ${paint}>${esc(s)}</tspan>`;
  }).join('');
  return `<text x="${x}" y="${y}" font-family="${f}" font-size="${size}" font-weight="${weight}" text-anchor="middle" letter-spacing="${ls}">${spans}</text>`;
}

// ---------- name / age / year line with fillable-field rects ----------
// fields: array of [label, widthOfBlank]; returns svg, pushes field rects to ctx.
export function fillLine(ctx, cx, y, fields = [['name', 230], ['age', 70], ['year', 90]], { size = 24, gap = 26 } = {}) {
  const lw = (s) => s.length * size * 0.42 + 8; // approx Patrick Hand label width
  const total = fields.reduce((a, [l, w]) => a + lw(l) + w, 0) + gap * (fields.length - 1);
  let x = cx - total / 2;
  let out = '';
  for (const [label, w] of fields) {
    out += text(x, y, label, { size, anchor: 'start', color: 'ink', extra: 'opacity="0.85"' });
    x += lw(label);
    out += `<line x1="${x}" y1="${y + 4}" x2="${x + w}" y2="${y + 4}" stroke="${INK}" stroke-width="1.6" stroke-linecap="round" opacity="0.8"/>`;
    ctx.fields.push({ name: label, x: x + 2, y: y - size * 0.95, w: w - 4, h: size * 1.15 });
    x += w + gap;
  }
  return out;
}
// Single labelled line (for keepsake questionnaires).
export function labelLine(ctx, x, y, label, w, { size = 26 } = {}) {
  const lw = label.length * size * 0.42 + 10;
  ctx.fields.push({ name: label, x: x + lw + 2, y: y - size * 0.95, w: w - lw - 4, h: size * 1.15 });
  return text(x, y, label, { size, anchor: 'start' }) +
    `<line x1="${x + lw}" y1="${y + 4}" x2="${x + w}" y2="${y + 4}" stroke="${INK}" stroke-width="1.6" stroke-linecap="round" opacity="0.8"/>`;
}

// ---------- small decorations ----------
export function starPath(r, inner = 0.45) {
  let d = '';
  for (let i = 0; i < 10; i++) {
    const a = (Math.PI / 5) * i - Math.PI / 2;
    const rr = i % 2 ? r * inner : r;
    d += `${i ? 'L' : 'M'}${(Math.cos(a) * rr).toFixed(2)},${(Math.sin(a) * rr).toFixed(2)}`;
  }
  return d + 'Z';
}
export const star = (x, y, r, c = 'orange', rot = 0) =>
  `<path transform="${at(x, y, 1, rot)}" d="${starPath(r)}" ${deco(c)} stroke-linejoin="round"/>`;
export const sparkle = (x, y, r, c = 'yellow') =>
  `<path transform="${at(x, y)}" d="M0,${-r} Q${r * 0.15},${-r * 0.15} ${r},0 Q${r * 0.15},${r * 0.15} 0,${r} Q${-r * 0.15},${r * 0.15} ${-r},0 Q${-r * 0.15},${-r * 0.15} 0,${-r}Z" ${deco(c, 2)}/>`;
export const dot = (x, y, r, c = 'purple') => `<circle cx="${x}" cy="${y}" r="${r}" ${deco(c, 2)}/>`;

// Scatter helper: list of [x,y,r,color,kind]
export function scatter(items) {
  return items.map(([x, y, r, c = 'orange', k = 'star']) =>
    k === 'star' ? star(x, y, r, c, (x * 7 + y) % 30 - 15)
      : k === 'dot' ? dot(x, y, r, c) : sparkle(x, y, r, c)).join('');
}

export function bat(x, y, s = 1, rot = 0) {
  const d = 'M0,-7 C3,-7 5,-4 5.5,-1 L9,-5 C14,-10 23,-10 29,-5 C25,-3 24,1 25,5 C21,2.5 16,3 13.5,6.5 C11.5,3.5 8,3 5.5,5 C4.5,8 2.5,9.5 0,9.5 C-2.5,9.5 -4.5,8 -5.5,5 C-8,3 -11.5,3.5 -13.5,6.5 C-16,3 -21,2.5 -25,5 C-24,1 -25,-3 -29,-5 C-23,-10 -14,-10 -9,-5 L-5.5,-1 C-5,-4 -3,-7 0,-7 Z M-4.5,-5.5 L-5.5,-11 L-1.5,-6.5 Z M4.5,-5.5 L5.5,-11 L1.5,-6.5 Z';
  return `<path transform="${at(x, y, s, rot)}" d="${d}" fill="${INK}"/>`;
}

export function moon(x, y, r, { craters = true, crescent = false } = {}) {
  let out = '';
  if (crescent) {
    out = `<path transform="${at(x, y)}" d="M${r * 0.2},${-r} A${r},${r} 0 1 0 ${r * 0.2},${r} A${r * 0.78},${r * 0.78} 0 1 1 ${r * 0.2},${-r} Z" ${isBW() ? `fill="#fff" stroke="${INK}" stroke-width="3"` : `fill="${pal('moon')}"`}/>`;
    return out;
  }
  out += `<circle cx="${x}" cy="${y}" r="${r}" ${isBW() ? `fill="#fff" stroke="${INK}" stroke-width="3"` : `fill="${pal('moon')}"`}/>`;
  if (craters) {
    const c = isBW() ? `fill="none" stroke="${INK}" stroke-width="2"` : `fill="#F3D78A"`;
    out += `<circle cx="${x - r * 0.35}" cy="${y - r * 0.2}" r="${r * 0.16}" ${c}/><circle cx="${x + r * 0.3}" cy="${y + r * 0.3}" r="${r * 0.12}" ${c}/><circle cx="${x + r * 0.15}" cy="${y - r * 0.45}" r="${r * 0.08}" ${c}/>`;
  }
  return out;
}

// Spider web anchored in a corner. quad: 'tl','tr','bl','br'
export function web(cx, cy, R, quad = 'tr', w = 2.4) {
  const [sx, sy] = { tl: [1, 1], tr: [-1, 1], bl: [1, -1], br: [-1, -1] }[quad];
  const spokes = 6;
  const angs = Array.from({ length: spokes }, (_, i) => (Math.PI / 2) * (i / (spokes - 1)));
  const P = (a, r) => [cx + sx * Math.cos(a) * r, cy + sy * Math.sin(a) * r];
  let d = '';
  for (const a of angs) { const [x, y] = P(a, R); d += `M${cx},${cy}L${x.toFixed(1)},${y.toFixed(1)}`; }
  for (const f of [0.28, 0.5, 0.72, 0.93]) {
    for (let i = 0; i < spokes - 1; i++) {
      const [x1, y1] = P(angs[i], R * f), [x2, y2] = P(angs[i + 1], R * f);
      const [mx, my] = P((angs[i] + angs[i + 1]) / 2, R * f * 0.86);
      d += `M${x1.toFixed(1)},${y1.toFixed(1)}Q${mx.toFixed(1)},${my.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)}`;
    }
  }
  return `<path d="${d}" ${line(w)}/>`;
}
// Free-standing round web centred at (cx,cy)
export function roundWeb(cx, cy, R, w = 2.4, spokes = 10) {
  let d = '';
  const P = (a, r) => [cx + Math.cos(a) * r, cy + Math.sin(a) * r];
  for (let i = 0; i < spokes; i++) { const [x, y] = P((2 * Math.PI * i) / spokes, R); d += `M${cx},${cy}L${x.toFixed(1)},${y.toFixed(1)}`; }
  for (const f of [0.2, 0.4, 0.6, 0.8, 1.0]) {
    for (let i = 0; i < spokes; i++) {
      const a1 = (2 * Math.PI * i) / spokes, a2 = (2 * Math.PI * (i + 1)) / spokes;
      const [x1, y1] = P(a1, R * f), [x2, y2] = P(a2, R * f), [mx, my] = P((a1 + a2) / 2, R * f * 0.88);
      d += `M${x1.toFixed(1)},${y1.toFixed(1)}Q${mx.toFixed(1)},${my.toFixed(1)} ${x2.toFixed(1)},${y2.toFixed(1)}`;
    }
  }
  return `<path d="${d}" ${line(w)}/>`;
}

export function spider(x, y, s = 1, { thread = 0 } = {}) {
  let out = '';
  if (thread) out += `<line x1="${x}" y1="${y - thread}" x2="${x}" y2="${y - 10 * s}" ${line(2)}/>`;
  const legs = [[-1, -1], [-1, -0.3], [-1, 0.4], [-1, 1]].flatMap(([a, b]) => [[a, b], [-a, b]]);
  let d = '';
  for (const [a, b] of legs) d += `M${x},${y}q${a * 10 * s},${(b * 6 - 6) * s} ${a * 16 * s},${(b * 10 + 2) * s}`;
  out += `<path d="${d}" ${line(2.6 * Math.min(1.2, s))}/>`;
  out += `<circle cx="${x}" cy="${y}" r="${9 * s}" fill="${INK}"/>`;
  out += `<circle cx="${x - 3 * s}" cy="${y - 2 * s}" r="${2.6 * s}" fill="#fff"/><circle cx="${x + 3 * s}" cy="${y - 2 * s}" r="${2.6 * s}" fill="#fff"/>`;
  out += `<circle cx="${x - 3 * s}" cy="${y - 1.5 * s}" r="${1.2 * s}" fill="${INK}"/><circle cx="${x + 3 * s}" cy="${y - 1.5 * s}" r="${1.2 * s}" fill="${INK}"/>`;
  return out;
}

export function candyCorn(x, y, s = 1, rot = 0) {
  const id = uid('cc');
  const d = 'M-15,10 Q-16.5,16 -10,16 L10,16 Q16.5,16 15,10 L3.5,-15 Q0,-21 -3.5,-15 Z';
  return `<g transform="${at(x, y, s, rot)}"><clipPath id="${id}"><path d="${d}"/></clipPath>
    <g clip-path="url(#${id})"><rect x="-20" y="-25" width="40" height="45" fill="${fill('cream')}"/>
    <rect x="-20" y="-6" width="40" height="12" fill="${fill('orange')}"/><rect x="-20" y="6" width="40" height="14" fill="${fill('yellow')}"/></g>
    ${isBW() ? `<path d="M-20,-6H20M-20,6H20" ${line(2)} clip-path="url(#${id})"/>` : ''}
    <path d="${d}" fill="none" stroke="${INK}" stroke-width="${2.6 / s}" stroke-linejoin="round"/></g>`;
}

export function face(x, y, s = 1, { cheeks = true, mouth = 'smile', eyes = 'dot' } = {}) {
  let out = '';
  if (eyes === 'dot') out += `<circle cx="${x - 9 * s}" cy="${y}" r="${3.4 * s}" fill="${INK}"/><circle cx="${x + 9 * s}" cy="${y}" r="${3.4 * s}" fill="${INK}"/>`;
  if (eyes === 'happy') out += `<path d="M${x - 13 * s},${y + 1 * s}q${4 * s},${-6 * s} ${8 * s},0M${x + 5 * s},${y + 1 * s}q${4 * s},${-6 * s} ${8 * s},0" ${line(2.6 * s)}/>`;
  if (mouth === 'smile') out += `<path d="M${x - 4 * s},${y + 6 * s}q${4 * s},${4 * s} ${8 * s},0" ${line(2.4 * s)}/>`;
  if (mouth === 'o') out += `<ellipse cx="${x}" cy="${y + 9 * s}" rx="${3 * s}" ry="${4 * s}" fill="${INK}"/>`;
  if (cheeks && !isBW()) out += `<ellipse cx="${x - 15 * s}" cy="${y + 6 * s}" rx="${4.5 * s}" ry="${3 * s}" fill="${pal('pink')}" opacity="0.8"/><ellipse cx="${x + 15 * s}" cy="${y + 6 * s}" rx="${4.5 * s}" ry="${3 * s}" fill="${pal('pink')}" opacity="0.8"/>`;
  return out;
}

export function pumpkin(x, y, s = 1, { faceKind = 'kawaii', color = 'orange' } = {}) {
  const sw = SW / s;
  let out = `<g transform="${at(x, y, s)}">`;
  out += `<path d="M-2,-26 Q-4,-38 4,-42 L9,-38 Q3,-34 5,-25 Z" fill="${fill('greenDk')}" stroke="${INK}" stroke-width="${sw}" stroke-linejoin="round"/>`;
  out += `<ellipse cx="-17" cy="0" rx="22" ry="27" ${os(color, sw)}/><ellipse cx="17" cy="0" rx="22" ry="27" ${os(color, sw)}/>`;
  out += `<ellipse cx="0" cy="0" rx="18" ry="28" ${os(color, sw)}/>`;
  out += `<path d="M8,-33 q10,-8 14,0 q-6,4 -14,0" fill="${fill('green')}" stroke="${INK}" stroke-width="${sw * 0.8}" stroke-linejoin="round"/>`;
  if (faceKind === 'kawaii') out += face(0, 2, 0.9);
  if (faceKind === 'jack') out += `<path d="M-14,-6 l6,-9 l6,9z M2,-6 l6,-9 l6,9z" fill="${INK}"/><path d="M-15,6 q15,16 30,0 l-5,2 l-3,-3 l-4,3 l-4,-3 l-4,3 l-3,-3 z" fill="${INK}"/>`;
  out += '</g>';
  return out;
}

export function ghost(x, y, s = 1, { faceKind = 'kawaii', rot = 0 } = {}) {
  const d = 'M-30,8 C-30,-26 -16,-42 0,-42 C16,-42 30,-26 30,8 L31,36 Q26,46 19,38 Q13,46 6,38 Q0,46 -6,38 Q-13,46 -19,38 Q-26,46 -31,36 Z';
  let out = `<g transform="${at(x, y, s, rot)}"><path d="${d}" fill="#fff" stroke="${INK}" stroke-width="${SW / s}" stroke-linejoin="round"/>`;
  if (faceKind === 'kawaii') out += face(0, -10, 0.95);
  if (faceKind === 'boo') out += `<ellipse cx="-9" cy="-14" rx="4.5" ry="6.5" fill="${INK}"/><ellipse cx="9" cy="-14" rx="4.5" ry="6.5" fill="${INK}"/><ellipse cx="0" cy="4" rx="5" ry="7" fill="${INK}"/>`;
  return out + '</g>';
}

export function witchHat(x, y, s = 1, rot = 0, color = 'purpleDk') {
  const sw = SW / s;
  return `<g transform="${at(x, y, s, rot)}">
    <ellipse cx="0" cy="0" rx="62" ry="14" ${os(color, sw)}/>
    <path d="M-36,-2 C-30,-40 -14,-70 4,-96 C10,-104 22,-104 28,-96 C18,-92 12,-80 14,-64 C18,-40 30,-18 36,-2 Z" ${os(color, sw)}/>
    <path d="M-34,-8 C-12,-2 14,-2 35,-8 L33,-22 C12,-16 -12,-16 -31,-22 Z" ${os('orange', sw)}/>
    <rect x="-8" y="-24" width="16" height="16" rx="3" fill="none" stroke="${INK}" stroke-width="${sw * 0.9}"/>
  </g>`;
}

export function leaf(x, y, s = 1, rot = 0, color = 'green') {
  return `<path transform="${at(x, y, s, rot)}" d="M0,0 C6,-10 18,-14 28,-12 C26,-2 18,8 4,8 C2,6 1,3 0,0 Z M0,0 Q12,-3 22,-9" ${os(color, SW / s * 0.8)}/>`;
}
export function curl(x, y, s = 1, flip = 1) {
  return `<path transform="${at(x, y)} scale(${flip * s} ${s})" d="M0,0 C10,-6 22,-4 22,6 C22,14 12,16 9,9 C7,4 13,1 15,5" ${line(3 / s, isBW() ? INK : pal('greenDk'))}/>`;
}

export function bolt(x, y, s = 1, flip = 1) {
  // shaft starts at the head edge (x=0) and points outward (+x, or -x when flip=-1)
  return `<g transform="${at(x, y)} scale(${flip * s} ${s})"><rect x="-4" y="-7" width="26" height="14" rx="3" ${os('gray', 3)}/><rect x="20" y="-13" width="12" height="26" rx="3" ${os('grayLt', 3)}/></g>`;
}

// Dark rounded panel (night sky). In BW becomes an outlined frame to colour in.
export function nightPanel(x, y, w, h, { r = 50, color = 'night', starsOn = true, seed = 1 } = {}) {
  let out = `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${r}" ${isBW() ? `fill="#fff" stroke="${INK}" stroke-width="4"` : `fill="${pal(color)}"`}/>`;
  if (starsOn) {
    let rnd = seed * 9301 + 49297;
    const R = () => ((rnd = (rnd * 9301 + 49297) % 233280) / 233280);
    for (let i = 0; i < 22; i++) {
      const sx = x + 30 + R() * (w - 60), sy = y + 30 + R() * (h - 60), rr = 3 + R() * 6;
      out += isBW() ? `<path transform="${at(sx, sy)}" d="${starPath(rr * 0.9)}" fill="#fff" stroke="${INK}" stroke-width="1.6"/>`
        : (i % 3 ? `<circle cx="${sx}" cy="${sy}" r="${rr * 0.35}" fill="#fff" opacity="0.8"/>` : `<path transform="${at(sx, sy)}" d="${starPath(rr)}" fill="${pal('moon')}"/>`);
    }
  }
  return out;
}

export function heart(x, y, s = 1, c = 'red') {
  return `<path transform="${at(x, y, s)}" d="M0,10 C-14,0 -20,-8 -14,-15 C-9,-20 -2,-18 0,-12 C2,-18 9,-20 14,-15 C20,-8 14,0 0,10 Z" ${deco(c, 2.4 / s)}/>`;
}

export function grassTufts(x1, x2, y, c = 'green') {
  let d = '';
  for (let x = x1 + 10; x < x2 - 10; x += 78) d += `M${x},${y}q2,-14 -4,-22M${x + 6},${y}q2,-18 6,-26M${x + 12},${y}q4,-10 12,-14`;
  return `<path d="${d}" ${line(3, isBW() ? INK : pal(c))}/>`;
}

export function tombstone(x, y, s = 1, label = 'BOO') {
  return `<g transform="${at(x, y, s)}"><path d="M-30,30 L-30,-10 C-30,-34 30,-34 30,-10 L30,30 Z" ${os('grayLt', SW / s)}/>
  ${text(0, 4, label, { size: 16, font: 'title', weight: 900, color: 'gray' })}</g>`;
}

export function cauldron(x, y, s = 1) {
  return `<g transform="${at(x, y, s)}">
   <path d="M-34,40 l-8,14 M34,40 l8,14" ${line(5 / s)}/>
   <path d="M-56,-10 C-62,30 -36,52 0,52 C36,52 62,30 56,-10 Z" ${os('dark', SW / s)}/>
   ${isBW() ? '' : `<path d="M-42,10 C-40,30 -26,40 -10,42" fill="none" stroke="#fff" stroke-opacity="0.25" stroke-width="${6 / s}" stroke-linecap="round"/>`}
   <rect x="-64" y="-20" width="128" height="16" rx="8" ${os('dark', SW / s)}/>
   <path d="M-56,-20 C-50,-36 -30,-30 -24,-38 C-16,-48 -4,-34 4,-40 C14,-48 26,-32 34,-38 C44,-44 56,-32 56,-20 Z" ${os('lime', SW / s)}/>
  </g>`;
}

export function treatBucket(x, y, s = 1) {
  return `<g transform="${at(x, y, s)}">
   <path d="M-40,-30 C-40,-80 40,-80 40,-30" ${line(4 / s)}/>
   <path d="M-46,-30 L-38,36 C-36,46 36,46 38,36 L46,-30 Z" ${os('orange', SW / s)}/>
   <ellipse cx="0" cy="-30" rx="46" ry="10" ${os('orangeDk', SW / s)}/>
   <path d="M-22,-8 l9,-12 l9,12z M4,-8 l9,-12 l9,12z" fill="${INK}"/>
   <path d="M-24,10 q24,22 48,0 l-7,3 l-5,-5 l-6,5 l-6,-5 l-6,5 l-5,-5 z" fill="${INK}"/>
  </g>`;
}

export function wrappedCandy(x, y, s = 1, c = 'purple', rot = 0) {
  return `<g transform="${at(x, y, s, rot)}"><path d="M-12,0 L-24,-9 L-22,9 Z M12,0 L24,-9 L22,9 Z" ${os(c, 2.6 / s)}/><ellipse cx="0" cy="0" rx="13" ry="10" ${os(c, 2.6 / s)}/></g>`;
}

export function lollipop(x, y, s = 1, c = 'red', rot = 0) {
  return `<g transform="${at(x, y, s, rot)}"><path d="M0,10 L0,46" ${line(4 / s)}/><circle cx="0" cy="0" r="16" ${os(c, 2.6 / s)}/><path d="M-8,0 a8,8 0 1 1 8,8" ${line(2.4 / s, isBW() ? INK : '#fff')}/></g>`;
}

export function bunting(x1, x2, y, colors = ['orange', 'purple', 'green', 'ink'], sag = 30) {
  let out = `<path d="M${x1},${y} Q${(x1 + x2) / 2},${y + sag * 2} ${x2},${y}" ${line(2)}/>`;
  const n = Math.round((x2 - x1) / 52);
  for (let i = 0; i < n; i++) {
    const t = (i + 0.5) / n;
    const px = x1 + (x2 - x1) * t, py = y + sag * 2 * 2 * t * (1 - t) * 1.0;
    const c = colors[i % colors.length];
    out += `<path transform="${at(px, py)}" d="M-17,0 L17,0 L0,30 Z" ${c === 'ink' && !isBW() ? `fill="${INK}"` : os(c, 2.4)}/>`;
  }
  return out;
}

export function candyCornGarland(x1, x2, y, sag = 26) {
  let out = `<path d="M${x1},${y} Q${(x1 + x2) / 2},${y + sag * 2} ${x2},${y}" ${line(2)}/>`;
  const n = Math.round((x2 - x1) / 44);
  for (let i = 0; i < n; i++) {
    const t = (i + 0.5) / n;
    const px = x1 + (x2 - x1) * t, py = y + sag * 2 * 2 * t * (1 - t);
    out += candyCorn(px, py + 14, 0.85, 180);
  }
  return out;
}

export function eyeball(x, y, r = 14, look = [0.2, 0.1]) {
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${Math.max(2, r / 6)}"/>` +
    `<circle cx="${x + look[0] * r}" cy="${y + look[1] * r}" r="${r * 0.5}" fill="${isBW() ? '#fff' : pal('teal')}" stroke="${INK}" stroke-width="${isBW() ? 2 : 0}"/>` +
    `<circle cx="${x + look[0] * r * 1.2}" cy="${y + look[1] * r * 1.2}" r="${r * 0.25}" fill="${INK}"/>`;
}
export function googly(x, y, r = 16, look = [0.25, 0.25]) {
  return `<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${INK}" stroke-width="${Math.max(1.5, r / 7)}"/>` +
    `<circle cx="${x + look[0] * r}" cy="${y + look[1] * r}" r="${r * 0.55}" fill="${INK}"/>` +
    `<circle cx="${x + look[0] * r - r * 0.15}" cy="${y + look[1] * r - r * 0.18}" r="${r * 0.14}" fill="#fff"/>`;
}

export function branch(x1, y1, x2, y2, c = 'brown') {
  return `<path d="M${x1},${y1} Q${(x1 + x2) / 2},${(y1 + y2) / 2 - 18} ${x2},${y2} L${x2},${y2 + 16} Q${(x1 + x2) / 2},${(y1 + y2) / 2} ${x1},${y1 + 18} Z" ${os(c)}/>`;
}

// ---------- print zones ----------
// Hand model (fingers point to -y, thumb on +x), origin = palm centre.
export const HAND = {
  palm: 'M-84,-104 C-60,-118 60,-120 84,-102 C96,-70 98,-10 94,40 C90,92 60,116 10,118 C-40,120 -84,100 -92,50 C-98,0 -98,-70 -84,-104 Z',
  fingers: [ // [baseX, baseY, length, width, angleDeg]
    [-70, -86, 122, 33, -21], [-30, -100, 158, 36, -8], [12, -104, 174, 37, 3], [52, -96, 156, 35, 14],
  ],
  thumb: [74, 26, 132, 40, 60],
  bbox: [-125, -280, 205, 122], // x1,y1,x2,y2 local
};
export const FOOT = {
  sole: 'M2,-138 C58,-140 76,-96 72,-44 C68,4 50,40 48,92 C46,150 32,184 0,184 C-36,184 -52,150 -52,100 C-52,48 -66,2 -68,-50 C-72,-112 -50,-136 2,-138 Z',
  toes: [[-40, -168, 27], [6, -180, 18], [38, -172, 15.5], [62, -153, 13.5], [77, -128, 11.5]],
  bbox: [-80, -205, 100, 192],
};
export function zoneBBox(z) {
  if (z.type === 'finger') { const r = z.r || 34; return [z.x - r, z.y - r * 1.15, z.x + r, z.y + r * 1.15]; }
  const s = z.s || 1, b = (z.type === 'hand' ? HAND : FOOT).bbox;
  const pts = [[b[0], b[1]], [b[2], b[1]], [b[0], b[3]], [b[2], b[3]]].map(([x, y]) => {
    if (z.mirror) x = -x;
    const a = ((z.rot || 0) * Math.PI) / 180;
    return [z.x + s * (x * Math.cos(a) - y * Math.sin(a)), z.y + s * (x * Math.sin(a) + y * Math.cos(a))];
  });
  const xs = pts.map((p) => p[0]), ys = pts.map((p) => p[1]);
  return [Math.min(...xs), Math.min(...ys), Math.max(...xs), Math.max(...ys)];
}

// Faint placement guide: corner brackets + label (covered by paint).
export function zoneGuide(z) {
  const GC = '#C9C4CE';
  if (z.type === 'finger') {
    const r = z.r || 34;
    return `<ellipse cx="${z.x}" cy="${z.y}" rx="${r * 0.82}" ry="${r}" fill="none" stroke="${GC}" stroke-width="2" stroke-dasharray="3 7" stroke-linecap="round"/>`;
  }
  const [x1, y1, x2, y2] = zoneBBox(z);
  const L = 26;
  const d = `M${x1},${y1 + L}V${y1}H${x1 + L}M${x2 - L},${y1}H${x2}V${y1 + L}M${x2},${y2 - L}V${y2}H${x2 - L}M${x1 + L},${y2}H${x1}V${y2 - L}`;
  const label = z.type === 'hand' ? 'handprint here' : 'footprint here';
  return `<path d="${d}" fill="none" stroke="${GC}" stroke-width="2.5" stroke-linecap="round"/>` +
    `<text x="${z.x}" y="${z.y + 6}" font-family="${FONTS.hand}" font-size="20" fill="${GC}" text-anchor="middle">${label}</text>`;
}

// Paint-texture filter for realistic sample prints (mockups only).
export function paintDefs() {
  return `<filter id="paint" x="-15%" y="-15%" width="130%" height="130%" color-interpolation-filters="sRGB">
    <feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="3" seed="4" result="n1"/>
    <feDisplacementMap in="SourceGraphic" in2="n1" scale="12" xChannelSelector="R" yChannelSelector="G" result="d"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.07" numOctaves="4" seed="21" result="nb"/>
    <feColorMatrix in="nb" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -18 0 0 0 13.1" result="blot"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.7" numOctaves="1" seed="11" result="np"/>
    <feColorMatrix in="np" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -16 0 0 0 11.9" result="pore"/>
    <feComposite in="d" in2="blot" operator="in" result="d2"/>
    <feComposite in="d2" in2="pore" operator="in" result="d3"/>
    <feTurbulence type="fractalNoise" baseFrequency="0.015" numOctaves="2" seed="2" result="n3"/>
    <feColorMatrix in="n3" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -1.4 0 0 0 1.68" result="mott"/>
    <feComposite in="d3" in2="mott" operator="in"/>
  </filter>`;
}

function capsule(bx, by, len, w, ang) {
  return `<g transform="translate(${bx} ${by}) rotate(${ang})"><rect x="${-w / 2}" y="${-len}" width="${w}" height="${len + 24}" rx="${w / 2}"/></g>`;
}
function creases(bx, by, len, w, ang, gaps) {
  return `<g transform="translate(${bx} ${by}) rotate(${ang})">${gaps.map((t) => `<path d="M${-w / 2 - 3},${-len * t + 2} q${w / 2},${-6} ${w + 6},${-1}" fill="none" stroke="#000" stroke-width="4.5"/>`).join('')}</g>`;
}
// Realistic sample print (for mockups). colors: {main, fingers}
export function samplePrint(z, paper = '#ffffff') {
  const c = z.color || '#F5893A';
  const s = z.s || 1;
  const T = `translate(${z.x} ${z.y}) rotate(${z.rot || 0}) scale(${(z.mirror ? -1 : 1) * s} ${s})`;
  if (z.type === 'finger') {
    const r = (z.r || 34) * 0.8;
    return `<g filter="url(#paint)"><ellipse cx="${z.x}" cy="${z.y}" rx="${r * 0.85}" ry="${r}" fill="${c}"/>
      <path d="M${z.x - r * 0.5},${z.y}a${r * 0.5},${r * 0.6} 0 1 1 ${r},0 M${z.x - r * 0.3},${z.y + 2}a${r * 0.3},${r * 0.36} 0 1 1 ${r * 0.6},0" fill="none" stroke="${paper}" stroke-opacity="0.45" stroke-width="2.5"/></g>`;
  }
  if (z.type === 'hand') {
    const fc = z.fingerColor || c;
    const m = uid('hm');
    let out = `<mask id="${m}" maskUnits="userSpaceOnUse" x="-400" y="-400" width="800" height="800"><rect x="-400" y="-400" width="800" height="800" fill="#fff"/>` +
      HAND.fingers.map(([x, y, l, w, a]) => creases(x, y, l, w, a, [0.3, 0.58])).join('') + creases(...HAND.thumb, [0.45]) +
      `<path d="M-70,-30 q60,14 150,-24 M-58,30 q50,-14 92,-70 M-14,104 q8,-60 66,-124" fill="none" stroke="#000" stroke-opacity="0.6" stroke-width="4"/></mask>`;
    out += `<g filter="url(#paint)"><g transform="${T}"><g mask="url(#${m})">`;
    out += `<g fill="${fc}">${HAND.fingers.map(([x, y, l, w, a]) => capsule(x, y, l, w, a)).join('')}</g>`;
    out += `<g fill="${z.thumbColor || fc}">${capsule(...HAND.thumb)}</g>`;
    if (z.tipColor) out += `<g fill="${z.tipColor}">${HAND.fingers.map(([x, y, l, w, a]) => `<g transform="translate(${x} ${y}) rotate(${a})"><rect x="${-w / 2}" y="${-l}" width="${w}" height="${l * 0.3}" rx="${w / 2}"/></g>`).join('')}</g>`;
    out += `<path d="${HAND.palm}" fill="${c}"/>`;
    return out + '</g></g></g>';
  }
  // foot
  const tc = z.toeColor || c;
  let out = `<g filter="url(#paint)"><g transform="${T}">`;
  if (z.bands) { // [[color, fromY, toY]] colour bands across the sole
    const id = uid('fb');
    out += `<clipPath id="${id}"><path d="${FOOT.sole}"/></clipPath><g clip-path="url(#${id})">${z.bands.map(([bc, a, b]) => `<rect x="-90" y="${a}" width="180" height="${b - a}" fill="${bc}"/>`).join('')}</g>`;
  } else out += `<path d="${FOOT.sole}" fill="${c}"/>`;
  out += FOOT.toes.map(([x, y, r]) => `<ellipse cx="${x}" cy="${y}" rx="${r}" ry="${r * 1.12}" fill="${tc}"/>`).join('');
  out += `<path d="M-30,-60 q30,20 70,0 M-20,60 q20,10 40,0" fill="none" stroke="${paper}" stroke-opacity="0.45" stroke-width="5"/>`;
  return out + '</g></g>';
}

// Map a point in zone-local coords (hand/foot model space) to page coords.
export function zp(z, lx, ly) {
  const s = z.s || 1, a = ((z.rot || 0) * Math.PI) / 180;
  const x = (z.mirror ? -lx : lx) * s, y = ly * s;
  return [z.x + x * Math.cos(a) - y * Math.sin(a), z.y + x * Math.sin(a) + y * Math.cos(a)];
}
