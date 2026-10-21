"""Check the generated static site's local destinations, assets and basic markup."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from collections import Counter

ROOT = Path(__file__).resolve().parent / 'dist'
class Document(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.ids, self.links, self.headings, self.images = [], [], 0, []
        self.feed(text)
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs: self.ids.append(attrs['id'])
        if tag == 'h1': self.headings += 1
        for key in ['src','href']:
            if attrs.get(key): self.links.append(attrs[key])
        if tag == 'img': self.images.append(attrs)

docs = {p:Document(p.read_text(encoding='utf-8')) for p in ROOT.glob('*.html')}
errors = []
links = 0
for path, doc in docs.items():
    if doc.headings != 1: errors.append(f'{path.name}: expected one h1, got {doc.headings}')
    if len(doc.ids) != len(set(doc.ids)): errors.append(f'{path.name}: duplicate id')
    for im in doc.images:
        if 'alt' not in im: errors.append(f'{path.name}: image missing alt')
    for href in doc.links:
        url = urlsplit(href)
        if url.scheme or url.netloc: continue
        dest = (path.parent / unquote(url.path)).resolve() if url.path else path
        if not dest.is_file(): errors.append(f'{path.name}: missing {href}')
        if url.fragment and dest.suffix == '.html' and dest in docs and unquote(url.fragment) not in docs[dest].ids:
            errors.append(f'{path.name}: missing fragment {href}')
        links += 1
for path in ROOT.glob('*.html'):
    text = path.read_text(encoding='utf-8')
    for phrase in ['Your project title','five countries','Team member 02','DEMONSTRATION PROJECT','PROJECT LOGO','To be added']:
        if phrase in text: errors.append(f'{path.name}: leftover placeholder {phrase}')
if errors:
    raise SystemExit('\n'.join(errors))
print(f'PASS: {len(docs)} HTML pages, {links} local references, unique IDs, one h1 per page, image alt text and placeholder checks.')
