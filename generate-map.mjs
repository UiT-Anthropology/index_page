import { readFileSync, writeFileSync } from 'node:fs';
// Natural Earth 1:50m Admin 0, public domain. North-polar azimuthal equidistant.
// Magnify the Greenland–Fennoscandia research sector 2.15× inside the same disc.
const zoom = 2.15, focus = [450, 360];
const mapTransform = `translate(${500-focus[0]*zoom} ${500-focus[1]*zoom}) scale(${zoom})`;
const source = JSON.parse(readFileSync(new URL('./data/ne_50m_admin_0_countries.geojson', import.meta.url)));
function project([lon,lat]) {
  const a=lon*Math.PI/180, r=(90-lat)*9.15;
  return [500+r*Math.sin(a),500-r*Math.cos(a)];
}
const esc = v => String(v).replaceAll('&','&amp;').replaceAll('"','&quot;').replaceAll('<','&lt;');
const ring = points => points.map((p,i)=>`${i?'L':'M'}${project(p).map(n=>n.toFixed(1)).join(',')}`).join('')+'Z';
const countries=source.features.flatMap(({properties:p,geometry:g})=>{
  const polygons=(g.type==='Polygon'?[g.coordinates]:g.coordinates).filter(poly=>poly[0].some(point=>{
    if (point[1] < 45) return false;
    const [x,y]=project(point);
    return Math.hypot((x-focus[0])*zoom,(y-focus[1])*zoom) <= 460;
  }));
  if (!polygons.length) return [];
  const name=p.ADMIN==='Greenland'?'Greenland · Kingdom of Denmark':p.ADMIN;
  return [`<path class="map-country" data-country="${esc(name)}" tabindex="0" role="button" aria-label="${esc(name)}" fill="${['#bfd2ca','#b3c9c2','#c8d8cf'][p.MAPCOLOR7%3]}" d="${polygons.map(poly=>poly.map(ring).join('')).join('')}"><title>${esc(name)}</title></path>`];
}).join('\n');
const grid=[60,66.562,75].map(lat=>`<circle cx="500" cy="500" r="${(90-lat)*9.15}"/>`).join('')+Array.from({length:12},(_,i)=>{const [x,y]=project([i*30,45]);return `<path d="M500,500L${x},${y}"/>`;}).join('');
const svg=`<svg class="polar-basemap" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000" role="group" aria-label="Interactive map focused on Greenland and northern Europe, magnified north-polar azimuthal equidistant projection">
<defs><clipPath id="arctic-disc"><circle cx="500" cy="500" r="455"/></clipPath><radialGradient id="arctic-sea"><stop stop-color="#153d49"/><stop offset="1" stop-color="#0b2c3a"/></radialGradient></defs>
<circle cx="500" cy="500" r="455" fill="url(#arctic-sea)" stroke="#749ca0" stroke-width="1.5"/>
<g clip-path="url(#arctic-disc)"><g transform="${mapTransform}"><g fill="none" stroke="#a0c4c3" stroke-opacity=".16" stroke-width=".65">${grid}</g><g fill-rule="evenodd" stroke="#355b60" stroke-width=".9" stroke-linejoin="round">${countries}</g></g></g>
<g fill="#a6c4c3" font-family="Outfit,Arial,sans-serif" font-size="13" letter-spacing="3" text-anchor="middle" pointer-events="none"><text x="607.5" y="770">ARCTIC OCEAN</text><text x="607.5" y="825" font-size="10" letter-spacing="2">90° N</text></g><path d="M600.5 801h14m-7-7v14" stroke="#a6c4c3" stroke-width="1" pointer-events="none"/></svg>`;
writeFileSync(new URL('./assets/arctic-polar-map.svg',import.meta.url),svg);
console.log(`Generated map with ${countries.split('data-country=').length-1} countries and territories.`);
