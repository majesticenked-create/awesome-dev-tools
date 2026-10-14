// Shared bits for the design modules.
import * as L from './lib.mjs';
const { INK, line, HAND, FOOT, zp } = L;

export const W = '#F4F1EA';      // white paint (sample)
export const PAINT = {
  orange: '#F5893A', black: '#2E2A33', green: '#79D14F', purple: '#A585DB', white: W,
  gray: '#B9B5BE', yellow: '#FFD23F', brown: '#8A5A36', red: '#E2453C', cream: '#F7E7C4',
  teal: '#4FC1B0', pink: '#F59BB6', lime: '#A6E05A',
};

export const jackFace = (x, y, s = 1) => `<g transform="translate(${x} ${y}) scale(${s})">
  <path d="M-38,-14 l14,-22 l14,22z M10,-14 l14,-22 l14,22z M-6,4 l6,-10 l6,10z" fill="${INK}"/>
  <path d="M-44,18 q44,44 88,0 l-12,5 l-8,-9 l-10,9 l-10,-9 l-10,9 l-10,-9 l-10,9 l-8,-9 z" fill="${INK}"/></g>`;
export const markerSmile = (x, y, w = 40, sw = 5) => `<path d="M${x - w / 2},${y} q${w / 2},${w * 0.45} ${w},0" ${line(sw)}/>`;

// Page position of a fingertip (0=pinky..3=index, 4=thumb) for a hand zone.
export function tip(z, i, inset = 0.5) {
  const [bx, by, len, w, a] = i === 4 ? HAND.thumb : HAND.fingers[i];
  const r = (a * Math.PI) / 180, d = len - w * inset;
  return zp(z, bx + Math.sin(r) * d, by - Math.cos(r) * d);
}
// Page position of a toe (0=big toe..4) or the heel for a foot zone.
export const toe = (z, i) => zp(z, FOOT.toes[i][0], FOOT.toes[i][1]);
export const footPt = (z, x, y) => zp(z, x, y);

// Bat wing for fingerprint bats. side: -1 left, 1 right. r = body radius
export function batWing(x, y, r = 30, side = 1, c = 'dark') {
  const s = r / 30;
  return `<path transform="translate(${x + side * r * 0.72} ${y - 4 * s}) scale(${side * s} ${s})" d="M0,-6 C14,-22 40,-30 58,-22 C52,-14 52,-6 56,2 C46,-2 40,2 38,10 C30,4 22,6 18,14 C12,6 6,6 0,10 Z" ${L.os(c, 3 / s)}/>` +
    `<path transform="translate(${x + side * r * 0.5} ${y - r * 0.95}) scale(${side * s} ${s})" d="M-6,6 L4,-14 L10,8 Z" ${L.os(c, 3 / s)}/>`;
}
export function hauntedHouse(x, y, s = 1) {
  const sw = 4 / s;
  return `<g transform="translate(${x} ${y}) scale(${s})">
    <path d="M-70,90 L-70,-10 L-90,-10 L-40,-70 L-10,-34 L-10,-60 L-20,-60 L10,-110 L40,-60 L30,-60 L30,-20 L80,-20 L60,10 L60,90 Z" ${L.os('purpleDk', sw)}/>
    <rect x="-52" y="10" width="22" height="26" rx="3" ${L.os('yellow', sw * 0.8)}/><rect x="16" y="20" width="22" height="26" rx="3" ${L.os('yellow', sw * 0.8)}/>
    <path d="M-2,-62 a12,12 0 0 1 24,0 v18 h-24z" ${L.os('yellow', sw * 0.8)}/>
    <path d="M-20,90 v-40 a14,14 0 0 1 28,0 v40" ${L.os('dark', sw * 0.8)}/>
    <path d="M-52,23 h22 M-41,10 v26 M16,33 h22 M27,20 v26" ${line(sw * 0.6)}/>
  </g>`;
}
export function crow(x, y, s = 1, flip = 1) {
  return `<g transform="translate(${x} ${y}) scale(${flip * s} ${s})"><path d="M-20,4 C-14,-12 6,-14 14,-6 L24,-8 L16,0 C14,10 0,16 -12,12 L-26,18 Z" fill="${INK}"/><circle cx="8" cy="-6" r="2" fill="#fff"/></g>`;
}
export function cornStalk(x, y, h = 300, flip = 1) {
  let out = `<path d="M${x},${y} C${x + flip * 6},${y - h * 0.5} ${x - flip * 4},${y - h * 0.8} ${x + flip * 10},${y - h}" ${line(6, L.isBW() ? INK : L.pal('greenDk'))}/>`;
  for (let i = 1; i <= 4; i++) {
    const yy = y - (h * i) / 5, side = i % 2 ? 1 : -1;
    out += L.leaf(x, yy, 1.6, side > 0 ? -30 : -150, 'green');
  }
  return out;
}
