"""Build the SPECIES editorial pages from reviewed, source-linked project content.

Run with the bundled Python runtime. Existing homepage animation and header remain.
"""
from pathlib import Path
import html
import json
import math
import re

ROOT = Path(__file__).resolve().parent
DIST = ROOT / 'dist'
DATA = json.loads((ROOT / 'data/species.json').read_text(encoding='utf-8'))
CASES = {c['id']: c for c in DATA['cases']}
PEOPLE = {p['id']: p for p in DATA['people']}
STORIES = {s['id']: s for s in DATA['stories']}
ASSETS = './assets/species/'

def e(value):
    return html.escape(str(value), quote=True)

def write(name, content):
    (DIST / name).write_text(content, encoding='utf-8')

def header(active=''):
    links = [('cases.html','Case Studies'), ('team.html','The Team'),
             ('multimedia.html','Multimedia'), ('field-notes.html','Field Notes')]
    def link(file, label):
        current = ' aria-current="page"' if active == file else ''
        return f'<a href="./{file}"{current}>{label}</a>'
    return f'''<header class="site-header">
      <a class="brand-placeholder header-brand" href="./index.html" aria-label="SPECIES home"><span class="brand-placeholder-mark" aria-hidden="true">S</span><span>SPECIES</span></a>
      <nav class="header-links" aria-label="Main navigation">{''.join(link(*l) for l in links)}</nav>
      <button class="header-menu-toggle" type="button" aria-label="Open navigation menu" aria-expanded="false" aria-controls="header-menu"><span aria-hidden="true"></span><span aria-hidden="true"></span><span aria-hidden="true"></span></button>
      <nav class="header-menu" id="header-menu" aria-label="All navigation" hidden><span class="header-menu-title">Explore</span>{link('index.html','Home')}{link('about.html','About the project')}{''.join(link(*l) for l in links)}<a href="./index.html#partners">Research institutions</a></nav>
    </header>'''

def footer():
    return '''<footer class="team-page-footer"><span>SPECIES · Sustainable Species in the Arctic</span><div><a href="./about.html">About the project</a> · <a href="#top">Back to top ↑</a></div></footer>'''

def page(title, description, body, active=''):
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"/><meta name="viewport" content="width=device-width, initial-scale=1"/>
<meta name="theme-color" content="#071724"/><meta name="description" content="{e(description)}"/>
<title>{e(title)} · SPECIES</title>
<link rel="stylesheet" href="./styles.css"/><link rel="stylesheet" href="./story.css"/><link rel="stylesheet" href="./team-page.css"/><link rel="stylesheet" href="./header.css"/><link rel="stylesheet" href="./species.css"/>
<script src="./header.js" defer></script><script src="./species.js" defer></script></head>
<body><a class="skip-link" href="#main">Skip to main content</a><div class="site-shell species-shell" id="top">{header(active)}<main id="main">{body}</main>{footer()}</div></body></html>'''

def intro(kicker, title, description):
    return f'<section class="editorial-intro"><span class="team-page-kicker">{e(kicker)}</span><h1>{title}</h1><p>{e(description)}</p></section>'

def source_note(source):
    item = DATA['sources'][source]
    return f'<p class="source-note">Source material: <a href="{e(item["url"])}">{e(item["title"])}</a>.</p>'

def tags(items):
    return '<div class="tags">' + ''.join(f'<span>{e(t)}</span>' for t in items) + '</div>'

def photo(name, alt, credit, cls=''):
    return f'<figure class="editorial-figure {cls}"><a href="{ASSETS}{e(name)}"><img src="{ASSETS}{e(name)}" alt="{e(alt)}" loading="lazy"/></a><figcaption>{e(credit)} <a href="{ASSETS}{e(name)}">View full image ↗</a></figcaption></figure>'

def person_visual(p):
    if p.get('image'):
        return f'<img class="person-image" src="{ASSETS}{p["image"]}" alt="{e(p["name"])}" loading="lazy"/>'
    initials = ''.join(n[0] for n in p['name'].split()[:2])
    return f'<div class="person-monogram" aria-hidden="true">{e(initials)}</div>'

def case_card(c, n=1):
    visual = f'<img src="{ASSETS}{c["image"]}" alt="{e(c["imageAlt"])}" loading="lazy"/>' if c.get('image') else f'<span class="case-number" aria-hidden="true">{n:02d}</span><span class="case-art-name" aria-hidden="true">{e(c["name"])}</span>'
    group = 'norway' if c['region'].startswith('Norway') else c['region'].lower()
    return f'''<article class="case-tile" data-region="{group}" data-filter-item>
      <a class="case-art {'is-diagram' if c['id']=='muskoxen' else ''}" href="./case-{c['id']}.html" tabindex="-1" aria-hidden="true">{visual}</a>
      <div class="case-copy"><span class="team-page-kicker">{e(c['region'])}</span><h2><a href="./case-{c['id']}.html">{e(c['name'])} <span aria-hidden="true">↗</span></a></h2><h3>{e(c['title'])}</h3><p>{e(c['summary'])}</p>{tags(c['themes'])}</div></article>'''

def story_card(s):
    return f'''<article class="story-card" data-filter-item data-region="{e(s['case'])}"><span class="team-page-kicker">{e(s['category'])} · {e(s['region'])}</span><p class="story-period">{e(s['period'])}</p><h2><a href="./note-{s['id']}.html">{e(s['title'])} <span aria-hidden="true">↗</span></a></h2><p>{e(s['summary'])}</p><a class="text-link" href="./case-{s['case']}.html">{e(CASES[s['case']]['name'])} case →</a></article>'''

def filters(options, label):
    return f'<div class="filter-bar" role="group" aria-label="{e(label)}">' + ''.join(f'<button type="button" data-filter="{key}" aria-pressed="{str(i==0).lower()}">{e(name)}</button>' for i,(key,name) in enumerate(options)) + '</div><p class="filter-count" aria-live="polite" aria-atomic="true"></p>'

def build_cases():
    body = '<h1 class="sr-only">Case studies</h1><section class="editorial-section directory-section" aria-label="Case studies" data-filter-group>'
    body += filters([('all','All regions'),('norway','Norway · Sápmi'),('finland','Finland'),('greenland','Greenland')], 'Filter case studies by region')
    body += '<div class="case-directory">' + ''.join(case_card(c,n) for n,c in enumerate(DATA['cases'],1)) + '</div></section>'
    write('cases.html', page('Case studies','Seven species and three Arctic research regions.',body,'cases.html'))
    for c in DATA['cases']:
        body = f'<div class="breadcrumb"><a href="./cases.html">Case studies</a><span>/</span>{e(c["name"])}</div>'
        body += intro(c['region'], e(c['name']) + '.', c['title'])
        body += '<div class="article-layout"><article class="article-body">'
        body += f'<p class="article-lead">{e(c["summary"])}</p>'
        body += ''.join(f'<p>{e(t)}</p>' for t in c['body'])
        if c.get('image'):
            body += photo(c['image'],c['imageAlt'],c['credit'],'diagram' if c['id']=='muskoxen' else '')
        body += '<h2>How we work</h2><p>' + e(c['methods']) + '</p>'
        body += source_note(c['source']) + '</article>'
        body += f'<aside class="case-aside"><span class="team-page-kicker">IN FOCUS</span><h2>Place &amp; perspectives</h2><p>{e(c["place"])}</p>{tags(c["themes"])}<h3>People connected to this case</h3>'
        body += '<ul class="people-links">' + ''.join(f'<li><a href="./team.html#{pid}">{e(PEOPLE[pid]["name"])}</a><small>{e(PEOPLE[pid]["institution"])}</small></li>' for pid in c['people']) + '</ul></aside></div>'
        if c.get('stories'):
            body += '<section class="editorial-section"><div class="editorial-heading"><span class="team-page-kicker">RESEARCH IN PRACTICE</span><h2>Stories from this case.</h2></div><div class="story-grid">' + ''.join(story_card(STORIES[s]) for s in c['stories']) + '</div></section>'
        body += '<section class="related-links"><a href="./cases.html">← All case studies</a><a href="./multimedia.html">Explore the media collection ↗</a></section>'
        write(f'case-{c["id"]}.html',page(c['name'],c['summary'],body,'cases.html'))

def build_team():
    body = '<h1 class="sr-only">The team</h1><section class="editorial-section directory-section" data-filter-group aria-label="Project contributors">'
    body += filters([('all','All contributors'),('reindeer','Reindeer'),('king-crabs','King crabs'),('wild-ducks','Wild ducks'),('seals','Seals'),('lapland-cattle','Lapland cattle'),('polar-bears','Polar bears'),('muskoxen','Muskoxen')],'Filter contributors by case')
    body += '<div class="people-grid">'
    for p in DATA['people']:
        body += f'<article class="person-card" id="{p["id"]}" data-filter-item data-region="{" ".join(p["cases"])}">{person_visual(p)}<div class="person-copy"><span class="team-page-kicker">{e(p["institution"])}</span><h2>{e(p["name"])}</h2><p class="person-role">{e(p["role"])}</p><p>{e(p["bio"])}</p><div class="person-cases">' + ''.join(f'<a href="./case-{cid}.html">{e(CASES[cid]["name"])}</a>' for cid in p['cases']) + '</div>'
        if p.get('orcid'):
            body += f'<a class="text-link" href="https://orcid.org/{p["orcid"]}">ORCID profile ↗</a>'
        body += '</div></article>'
    body += '</div></section>'
    write('team.html',page('The team','Meet the researchers and artists contributing to SPECIES.',body,'team.html'))

def build_stories():
    body = '<h1 class="sr-only">Field notes</h1><section class="editorial-section directory-section" data-filter-group aria-label="Field notes and activities">' + filters([('all','All notes'),('seals','Baltic seals'),('muskoxen','Muskoxen'),('lapland-cattle','Lapland cattle')],'Filter notes by case')
    body += '<div class="story-grid">' + ''.join(story_card(s) for s in DATA['stories']) + '</div></section>'
    write('field-notes.html',page('Field notes','Field stories, research updates and activities from SPECIES.',body,'field-notes.html'))
    for s in DATA['stories']:
        body = '<div class="breadcrumb"><a href="./field-notes.html">Field notes</a><span>/</span>' + e(s['category']) + '</div>'
        body += intro(s['category']+' · '+s['region'],e(s['title']),s['summary'])
        body += '<article class="reading-column"><div class="article-meta"><span>'+e(s['period'])+'</span><span>'+e(s['byline'])+'</span></div>'
        if s.get('image'):
            body += photo(s['image'],s['imageAlt'],s['credit'],'diagram' if s['id']=='muskox-model' else '')
        for section in s['body']:
            body += '<h2>'+e(section[0])+'</h2>'+''.join('<p>'+e(t)+'</p>' for t in section[1:])
        body += source_note(s['source']) + '</article>'
        body += f'<section class="related-links"><a href="./field-notes.html">← All field notes</a><a href="./case-{s["case"]}.html">Explore the {e(CASES[s["case"]]["name"])} case ↗</a></section>'
        write('note-'+s['id']+'.html',page(s['title'],s['summary'],body,'field-notes.html'))

def build_media():
    media = [
      ('lapland-cattle','finncattle-pasture.webp','Northern Finncattle in pasture','White Northern Finncattle grazing in a green pasture','Photo: Annu Puurunen.'),
      ('lapland-cattle','finncattle-woodland.webp','Cattle in a northern landscape','Northern Finncattle standing in a wooded landscape','Photo: Juha Kantanen.'),
      ('lapland-cattle','finncattle-archive.webp','Northern Finncattle archive','A white Northern Finncattle cow in a wooded pasture','Photo: Luke Archive.'),
      ('muskoxen','muskox-model.png','Inside a developing model','Working diagram of muskox foraging, energy budgets, movement and reproduction','SPECIES WP3 working conceptual diagram; model development, not simulation results.'),
      ('seals','seal-skins.webp','Skins and material practices','Stacks of seal skins beside larger hides in a workshop','Supplied with the Finland fieldwork materials. Photographer and location not specified.')]
    body = '<h1 class="sr-only">Multimedia</h1><section class="editorial-section directory-section" data-filter-group aria-label="Media collection">' + filters([('all','All media'),('lapland-cattle','Lapland cattle'),('muskoxen','Muskoxen'),('seals','Seals')],'Filter media by case') + '<div class="media-grid">'
    for cid,filename,title,alt,credit in media:
        body += f'<article class="media-tile" data-filter-item data-region="{cid}">{photo(filename,alt,credit,"diagram" if cid=="muskoxen" else "")}<h2>{e(title)}</h2><a class="text-link" href="./case-{cid}.html">{e(CASES[cid]["name"])} case →</a></article>'
    body += '</div></section><section class="editorial-section download-panel"><div><span class="team-page-kicker">FURTHER READING</span><h2>The Luke research update.</h2><p>Read the complete September 2026 contribution, including research descriptions, team biographies, activities and photographs.</p></div><a class="outline-link" href="./assets/species/luke-research-update.pdf" download>Download PDF · 938 KB ↓</a></section>'
    write('multimedia.html',page('Multimedia','Photography and research diagrams from SPECIES.',body,'multimedia.html'))

def build_about():
    body = intro('SUSTAINABLE SPECIES IN THE ARCTIC','Shared worlds.<br/>Different perspectives.', 'How can we create sustainable futures for humans and other species in a rapidly changing Arctic?')
    body += '''<article class="reading-column"><p class="article-lead">SPECIES explores environmental conflicts involving humans and other species across Norway, Finland and Greenland.</p>
    <p>Climate change, conservation policies, infrastructure and competing demands on resources are reshaping Arctic relationships. These changes raise questions about sustainability, Indigenous rights, traditional livelihoods and how different species can continue to live together.</p>
    <h2>Different ways of understanding a shared world</h2><p>Environmental conflicts concern more than wildlife or resources. They involve cultural practices, relationships between beings and the authority to decide how environments should be managed.</p>
    <p>Through the concept of multispecies ontologies, the project explores different understandings of animals, humans and landscapes. It brings scientific, local and Indigenous perspectives into dialogue without assuming they should be reduced to a single framework.</p>
    <h2>How we work</h2><p>Anthropology, biology, ecology, genetics, technology studies and audio-visual art contribute methods suited to each case. Depending on the setting, these include participant observation, interviews, scientific data collection, genetic analysis, drone testing and ecological modelling.</p>
    <p>Collaborative fieldwork and participatory workshops create opportunities to exchange knowledge, identify shared goals and connect research with local priorities. Local and Indigenous partners participate in framing questions as well as developing knowledge.</p>
    <h2>Questions guiding the research</h2><ul class="research-questions"><li>How can environmental conflicts be co-researched through different multispecies ontologies?</li><li>How can local and Indigenous knowledge work alongside research to question approaches to development, management and conservation?</li><li>How can participatory fieldwork and Indigenous methodologies challenge reductive understandings of traditional knowledge?</li><li>How can co-producing knowledge advance sustainable multispecies relations?</li></ul>
    <h2>Towards sustainable multispecies futures</h2><p>The project seeks to strengthen collaboration, identify shared priorities and explore culturally sensitive approaches to environmental management. Its ambition is to build alliances that recognise local aspirations, Indigenous sovereignty and the value of different knowledge traditions.</p>'''
    body += source_note('main') + '</article><section class="related-links"><a href="./cases.html">Explore the seven cases ↗</a><a href="./team.html">Meet the contributors ↗</a></section>'
    write('about.html',page('About the project','The vision, questions and collaborative approach behind SPECIES.',body))

def build_home():
    home = (DIST/'index.html').read_text(encoding='utf-8')
    # Replace the generated homepage sections cleanly on subsequent builds.
    home = re.sub(r'<section class="home-about section-wrap".*?</section>', '', home, flags=re.S)
    home = re.sub(r'<section class="editorial-section home-notes".*?</section>', '', home, flags=re.S)
    home = re.sub(r'<title>.*?</title>','<title>SPECIES · Sustainable Species in the Arctic</title>',home)
    home = re.sub(r'<meta name="description"[^>]+>', '<meta name="description" content="Exploring environmental conflicts and sustainable multispecies futures with researchers, local and Indigenous communities, and artists across Norway, Finland and Greenland." />',home)
    if 'href="./species.css"' not in home:
        home = home.replace('</head>','<link rel="stylesheet" href="./species.css" />\n</head>')
    home = re.sub(r'<header class="site-header">.*?</header>',header(),home,flags=re.S)
    home = home.replace('Your project title.','Sustainable Species<br/>in the Arctic.')
    home = home.replace('aria-label="An Arctic glacier at night with a meteor streaking across the sky"', 'aria-label="Conceptual illustration of an Arctic glacier at night with a meteor in the sky"')
    old = 'A polar research project spanning five countries, organized by <strong>Richard Fraser</strong> and supported by our research partners.'
    home = home.replace(old,'Exploring environmental conflicts with researchers, local and Indigenous communities, and artists across Norway, Finland and Greenland.',1)
    home = home.replace(old,'We bring anthropology, ecology, genetics, technology and art into dialogue to co-create knowledge for more sustainable multispecies futures.')
    home = home.replace('Research beyond<br /><em>borders.</em>','Towards shared<br /><em>Arctic futures.</em>')
    home = re.sub(r'<div class="story-facts".*?</div>\s*</div>\s*</div>', '<div class="story-facts" aria-label="Project at a glance"><div><span>3</span><small>RESEARCH REGIONS</small></div><div><span>7</span><small>SPECIES</small></div><div><span>1</span><small>SHARED ARCTIC</small></div></div>\n</div>',home, count=1,flags=re.S)
    home = home.replace('Click the pin<br /><em>to discover<br />with the team.</em>','Three regions.<br/><em>Connected lives.</em>')
    # Generated geometry and species share the same projection and viewBox.
    from map_content import build_map
    map_body, map_legend = build_map(DATA['cases'])
    home = re.sub(r'(<div class="polar-map-wrap">).*?(</div>\s*</figure>)', lambda m:m[1]+map_body+m[2], home, count=1, flags=re.S)
    home = re.sub(r'<div class="map-legend">.*?</div><!-- /map-legend -->', '', home, flags=re.S)
    home = home.replace('<h2 id="polar-title">Three regions.<br/><em>Connected lives.</em></h2>', '<h2 id="polar-title">Three regions.<br/><em>Connected lives.</em></h2>'+map_legend)
    # Use a representative selection of real contributors in the existing scroll scene.
    selection = ['richard-fraser','floris-van-beest','benjamin-dupuis','heidi-konttinen','juha-kantanen']
    cards = ''.join(f'<article class="team-card"><a class="team-photo" href="./team.html#{pid}" aria-label="Read about {e(PEOPLE[pid]["name"])}">{person_visual(PEOPLE[pid])}</a><h2><a href="./team.html#{pid}">{e(PEOPLE[pid]["name"])}</a></h2><p>{e(PEOPLE[pid]["role"])}</p></article>' for pid in selection)
    home = re.sub(r'(<div class="team-viewport"><div class="team-row">).*?(</div></div>)',lambda m:m[1]+cards+m[2],home,count=1,flags=re.S)
    content = '''<section class="home-about section-wrap" aria-labelledby="vision-title"><div><span class="team-page-kicker">THE PROJECT</span><h2 id="vision-title">How do we<br/><em>live together?</em></h2></div><div><p>Across the Arctic, relationships between people, animals and landscapes are changing. SPECIES brings different forms of knowledge into dialogue to explore environmental conflict, cultural practices and more sustainable shared futures.</p><a class="text-link" href="./about.html">Our questions and approach ↗</a></div></section>'''
    content += '<section class="projects section-wrap" id="projects" aria-labelledby="projects-title"><div class="section-heading"><div><div class="section-meta"><span>CASE STUDIES</span></div><h2 id="projects-title">Seven species.<br/>Many ways of knowing.</h2></div><a class="text-link" href="./cases.html">Explore every case ↗</a></div><div class="home-case-grid">' + ''.join(case_card(c,n) for n,c in enumerate(DATA['cases'],1)) + '</div></section>'
    content += '<section class="editorial-section home-notes"><div class="editorial-heading"><span class="team-page-kicker">FROM THE FIELD</span><h2>Research taking shape.</h2></div><div class="story-grid">'+''.join(story_card(STORIES[s]) for s in ['ajos','muskox-model','genomics'])+'</div><a class="text-link" href="./field-notes.html">All field notes ↗</a></section>'
    home = re.sub(r'<section class="projects section-wrap".*?</section>',lambda m:content,home,count=1,flags=re.S)
    partners = [('uit.png', 'UiT The Arctic University of Norway', 'uit'), ('lapland.svg', 'University of Lapland', 'lapland'), ('luke.svg', 'Natural Resources Institute Finland (Luke)', 'luke'), ('aarhus.png', 'Aarhus University', 'aarhus'), ('aalborg.svg', 'Aalborg University', 'aalborg'), ('cambridge.svg', 'University of Cambridge', 'cambridge'), ('niva.svg', 'Norwegian Institute for Water Research (NIVA)', 'niva')]
    partner_html = '<section class="partners-section section-wrap" id="partners" aria-label="Research institutions"><div class="partner-logo-grid">'+''.join(f'<div class="partner-logo partner-logo--{slug}"><img src="./assets/partners/{file}" alt="{e(name)}" loading="lazy" decoding="async"/></div>' for file,name,slug in partners)+'</div></section>'
    home = re.sub(r'<section class="partners-section section-wrap".*?</section>',lambda m:partner_html,home,count=1,flags=re.S)
    home = home.replace('Between Ice and Light · Arctic Research','SPECIES · Sustainable Species in the Arctic')
    write('index.html',home)

if __name__ == '__main__':
    build_cases()
    build_team()
    build_stories()
    build_media()
    build_about()
    build_home()
    print(f'Built homepage, 7 cases, {len(PEOPLE)} contributor profiles, {len(STORIES)} notes, about and media pages.')
