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

const svg = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" aria-hidden="true">
<defs><clipPath id="disc"><circle cx="500" cy="500" r="${radius.toFixed(1)}"/></clipPath></defs>
<circle cx="500" cy="500" r="${radius.toFixed(1)}" fill="#0b2c3a" stroke="#749ca0" stroke-width="1.5"/>
<g clip-path="url(#disc)">
  <path d="${land}" fill="#bfd2ca" fill-rule="evenodd" stroke="#dce8dd" stroke-width="1.5" stroke-linejoin="round"/>
</g>
</svg>`;

writeFileSync(new URL('./dist/assets/arctic-polar-map.svg', import.meta.url), svg);
