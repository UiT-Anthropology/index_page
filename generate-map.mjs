import { readFileSync, writeFileSync } from 'node:fs';

// Natural Earth 1:110m land, public domain: naturalearthdata.com.
// A north-polar azimuthal equidistant projection keeps the Arctic Ocean centered.
const source = JSON.parse(readFileSync(new URL('./data/ne_110m_land.geojson', import.meta.url)));
const center = 500;
const degreesToPixels = 9.15;
const limit = 45;
const radius = (90 - limit) * degreesToPixels;

function project([longitude, latitude]) {
  const theta = longitude * Math.PI / 180;
  const distance = (90 - latitude) * degreesToPixels;
  return [center + distance * Math.sin(theta), center - distance * Math.cos(theta)];
}

function ringPath(ring) {
  if (ring.length < 3) return '';
  return ring.map((point, index) => {
    const [x, y] = project(point);
    return `${index ? 'L' : 'M'}${x.toFixed(1)},${y.toFixed(1)}`;
  }).join('') + 'Z';
}

const land = source.features.filter((feature) => feature.bbox?.[3] >= limit).flatMap(({ geometry }) => {
  if (geometry.type === 'Polygon') return [geometry.coordinates];
  if (geometry.type === 'MultiPolygon') return geometry.coordinates;
  return [];
}).map((polygon) => polygon.map(ringPath).join('')).filter(Boolean).join('');

const rings = [50, 60, 70, 80].map((latitude) =>
  `<circle cx="500" cy="500" r="${((90 - latitude) * degreesToPixels).toFixed(1)}" />`
).join('');
const meridians = Array.from({ length: 12 }, (_, i) => {
  const [x, y] = project([i * 30, limit]);
  return `<path d="M500,500L${x.toFixed(1)},${y.toFixed(1)}" />`;
}).join('');

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" aria-hidden="true">
<defs><clipPath id="disc"><circle cx="500" cy="500" r="${radius.toFixed(1)}"/></clipPath></defs>
<circle cx="500" cy="500" r="${radius.toFixed(1)}" fill="#0b2c3a" stroke="#749ca0" stroke-width="1.5"/>
<g clip-path="url(#disc)">
  <g fill="none" stroke="#72939a" stroke-width="1" opacity=".35">${rings}${meridians}</g>
  <path d="${land}" fill="#bfd2ca" fill-rule="evenodd" stroke="#dce8dd" stroke-width="1.5" stroke-linejoin="round"/>
  <g fill="none" stroke="#b4d6d5" stroke-width="1.2" opacity=".78">${rings}</g>
</g>
<circle cx="500" cy="500" r="5" fill="#b9e8e3"/>
<path d="M500 476v-15M500 524v15M476 500h-15M524 500h15" stroke="#b9e8e3" stroke-width="1.4"/>
<g font-family="Arial,sans-serif" fill="#cce2df" letter-spacing="3" text-anchor="middle">
  <text x="500" y="440" font-size="13">NORTH POLE</text>
  <text x="500" y="580" font-size="20" letter-spacing="5">ARCTIC OCEAN</text>
</g>
<g font-family="Arial,sans-serif" fill="#c8d8d1" font-size="13" font-weight="600" letter-spacing="2">
  <text x="216" y="650" transform="rotate(-18 216 650)">CANADA</text>
  <text x="640" y="220" transform="rotate(17 640 220)">RUSSIA</text>
  <text x="350" y="240" transform="rotate(-22 350 240)">GREENLAND</text>
  <text x="680" y="655">NORWAY</text>
</g>
<g font-family="Arial,sans-serif" fill="#a8c7c8" font-size="12" letter-spacing="2">
  <text x="512" y="405">80° N</text><text x="512" y="310">70° N</text><text x="512" y="220">60° N</text>
</g>
</svg>`;

writeFileSync(new URL('./dist/assets/arctic-polar-map.svg', import.meta.url), svg);
