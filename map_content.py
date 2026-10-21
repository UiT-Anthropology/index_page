"""Homepage map content; geographic anchors are representative research areas, not animal ranges."""
from pathlib import Path
from html import escape
import math

# lon, lat, button x/y. Leader lines preserve geography when buttons are separated.
SITES = {
    'reindeer': (25.51,69.47,58,19),
    'king-crabs': (29.7,70.2,78,30),
    'wild-ducks': (25.5,69.5,85,51),
    'seals': (24.52,65.68,74,73),
    'lapland-cattle': (25.7,67.5,54,58),
    'polar-bears': (-21.97,70.49,34,27),
    'muskoxen': (-50.69,67.01,20,57),
}
ICONS = {
    'reindeer': 'M17 37l3-13 11-2 8 7-4 8M20 35v13m13-13 3 13M29 23l-1-9m-1 3-7-5m7 2 4-7m-2 10 8-4M38 28l8-8 6 3-3 6-10 1',
    'king-crabs': 'M22 29q10-10 20 0l1 9q-11 9-22 0ZM22 30l-9-8-4 3m33 5 9-8 4 3M22 35 10 33l-3 6m35-4 12-2 3 6M24 40l-9 7m25-7 9 7M18 25l-4-10-7-2 2 8 5-6m32 10 4-10 7-2-2 8-5-6',
    'wild-ducks': 'M12 36q10 2 16-7l7-5v-9q0-7 7-6 8 1 5 10l8 3-10 2-3 10q-6 14-22 10ZM24 35q9 5 15-3m-15 12-3 6m15-7 2 7',
    'seals': 'M9 39q6-15 24-10 6-2 8-8 7-10 13-2 4 7-3 11l-5 5q-11 12-28 10l-9 5 1-9ZM26 36l9 8m13-22h1m1 5 7 2',
    'lapland-cattle': 'M13 27h25l6 7-5 9H18l-5-6ZM18 41v9m18-9v9M39 31l3-12 9-1 4 9-6 9-7-3M43 20l-5-8m13 7 6-7M13 29 8 22v15m38-10h1m4 0h1',
    'polar-bears': 'M10 34l4-10 21-1 8-6 10 4 3 10-8 4-6-3-5 12h-7l-1-10-6 1-5 9h-7l1-10ZM44 19q-3-8 3-7 5 0 4 7m0 7h1',
    'muskoxen': 'M10 31q1-17 19-14l10 3 9 8-4 15-9-2-5 3-6-3-7 2-6-3ZM16 40v9m17-8v8M40 25q-7-1-8-8-5 13 6 14m8-5q8-3 9-9 5 13-6 15M40 32l3 7 6-2 2-6',
}
def project(lon, lat):
    r=(90-lat)*9.15; a=math.radians(lon)
    # Match the research-sector magnification in generate-map.mjs.
    return 500+(500+r*math.sin(a)-450)*2.15, 500+(500-r*math.cos(a)-360)*2.15

def build_map(cases):
    base=Path('dist/assets/arctic-polar-map.svg').read_text(encoding='utf-8')
    callouts=[]; pins=[]; legend=[]
    for i,c in enumerate(cases,1):
        key=c['id']; lon,lat,px,py=SITES[key]
        x,y=project(lon,lat)
        callouts.append(f'<line x1="{x:.1f}" y1="{y:.1f}" x2="{px*10}" y2="{py*10}"/><circle cx="{x:.1f}" cy="{y:.1f}" r="4"/>')
        # Muskox modelling also draws on a second, distinct site in NE Greenland.
        if key=='muskoxen':
            zx,zy=project(-20.57,74.47)
            callouts.append(f'<line x1="{zx:.1f}" y1="{zy:.1f}" x2="{px*10}" y2="{py*10}"/><circle cx="{zx:.1f}" cy="{zy:.1f}" r="4"/>')
        icon=f'<svg viewBox="0 0 64 64" aria-hidden="true"><path d="{ICONS[key]}"/></svg>'
        name=escape(c['name']); place=escape(c['place']); region=escape(c['region'])
        pins.append(f'<button class="animal-pin species-pin" type="button" data-pin="{key}" style="--pin-x:{px}%;--pin-y:{py}%" aria-label="Explore {name} · {region}" aria-controls="{key}-project" aria-expanded="false">{icon}<span class="species-pin-name">{name}</span></button><section class="pin-popup" id="{key}-project" role="dialog" aria-modal="false" aria-labelledby="{key}-map-title" hidden><button class="pin-popup-close" type="button" aria-label="Close {name}">×</button><span class="pin-popup-kicker">{region}</span><h3 id="{key}-map-title">{name}</h3><p class="map-place">{place}</p><p>{escape(c["summary"])}</p><a class="pin-link" href="./case-{key}.html">Explore the case →</a></section>')
        legend.append(f'<button type="button" data-map-target="{key}"><span>{i:02}</span>{name}</button>')
    body=base+'<svg class="map-callouts" viewBox="0 0 1000 1000" aria-hidden="true">'+''.join(callouts)+'</svg>'+''.join(pins)+'<span class="map-country-label" role="status" aria-live="polite"></span>'
    legend='<div class="map-legend"><p class="map-instruction">Seven species. One shared Arctic.<br/>Hover over a country. Select a species.</p><nav class="map-species-list" aria-label="Explore all seven species">'+''.join(legend)+'</nav><p class="map-source">Research locations, not species ranges.<br/>North-polar projection · <a href="https://www.naturalearthdata.com/downloads/50m-cultural-vectors/">Natural Earth</a></p></div><!-- /map-legend -->'
    return body,legend
