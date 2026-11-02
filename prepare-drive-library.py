"""Prepare an offline, traceable copy of the supplied SPECIES Drive materials.

Run with the bundled Python runtime (pypdf and Pillow). No network access is used.
"""
from pathlib import Path
import hashlib
import json
import shutil
import zipfile
import xml.etree.ElementTree as ET
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets/drive'
DATA = ROOT / 'data/drive-text'
ASSETS.mkdir(parents=True, exist_ok=True)
DATA.mkdir(parents=True, exist_ok=True)
for source, target in [('main.docx', 'main-content.docx'), ('florian.docx', 'finland-fieldwork.docx'), ('wp3.zip', 'wp3-materials.zip')]:
    shutil.copy2(ROOT / 'audit' / source, ASSETS / target)

inventory = json.loads((ROOT / 'audit/drive-inventory.json').read_text(encoding='utf-8'))
originals = {item['id']: item for item in inventory if item['file_or_folder'] == 'file'}
entries = []

def record(key, file, title, folder, uses, drive_id=None, parent=None, kind='document', page=None, credit=None, alt=None):
    path = ASSETS / file
    entry = dict(key=key, title=title, folder=folder, file='assets/drive/' + file,
                 kind=kind, uses=uses, bytes=path.stat().st_size,
                 sha256=hashlib.sha256(path.read_bytes()).hexdigest())
    if drive_id:
        entry.update(drive_id=drive_id, drive_url=originals[drive_id]['url'], modified=originals[drive_id]['modified_time'])
    if parent:
        entry['parent'] = parent
    if page:
        entry['page'] = page
    if credit:
        entry['credit'] = credit
    if alt:
        entry['alt'] = alt
    entries.append(entry)
    return entry

record('main', 'main-content.docx', 'SPECIES Website Main Content.docx', 'SPECIES', ['index.html', 'about.html', 'cases.html', 'team.html'], '1Om3zUqRkrsxlwTJbpANQggBx7gRJ66hZ', page='source-main.html')
record('test', 'test.txt', 'test', 'SPECIES', ['resources.html'], '16VWSxvU1IKMYzcxI2hnPPQQ49UpGHd8C-PKTkLnsAAI', page='source-test.html')
record('wp3', 'wp3-overview.docx', 'SPECIES_WP3_May_2026_aoa_fvb_aoa.docx', 'SPECIES/Website/Muskoxen', ['case-muskoxen.html', 'team.html'], '1AvBaNC2l7R4oWGuRP61jTrS5i55SUX_7', page='source-wp3.html')
record('wp3zip', 'wp3-materials.zip', 'SPECIES WP 3 information for website.zip', 'SPECIES/Website/Muskoxen', ['resources.html', 'team.html', 'note-muskox-model.html', 'multimedia.html'], '1f3shr4tSJWoDranq8eIsIftezQwEaAGN', kind='archive')
record('florian', 'finland-fieldwork.docx', 'website_update_2026Sep_Florian.docx', 'SPECIES/Website/Seals', ['case-seals.html', 'note-ajos.html', 'note-seal-practices.html', 'team.html'], '1G8KmD5L9oyJVKoaWdYUqAlma00_3R8RL', page='source-florian.html')
record('luke', 'luke-update.pdf', 'website_update_LUKE_202609.pdf', 'SPECIES/Website/Seals', ['case-lapland-cattle.html', 'note-genomics.html', 'note-bovine-symposium.html', 'note-multiomics-workshop.html', 'team.html', 'multimedia.html'], '16QZjXwQQk58BObldWfPQ58Sv14c0U7Kt', page='source-luke.html')
record('heidi', 'heidi-winter.jpeg', 'Heidi_winter_bigger.jpeg', 'SPECIES/Website/Seals', ['team.html#heidi-konttinen', 'index.html', 'multimedia.html'], '1H6m2fbSGEXc6Fp27RopFngwTv2_LoRp8', kind='image', credit='Supplied with the Finland fieldwork materials; photographer not specified.', alt='Portrait of Heidi Konttinen in winter clothing')
record('skins', 'seal-skins.JPG', 'Seal skins.JPG', 'SPECIES/Website/Seals', ['case-seals.html', 'note-seal-practices.html', 'multimedia.html'], '1LPEb6Te2Kcw24ex85cl2GIN8vlIKoE1D', kind='image', credit='Supplied with the Finland fieldwork materials; photographer and location not specified.', alt='Seal skins stacked beside larger animal hides')

zip_mapping = [
    ('SPECIES WP 3 profiles.docx', 'wp3-profiles.docx', 'profiles', 'document', 'source-profiles.html', ['team.html']),
    ('SPECIES WP 3 project update.docx', 'wp3-project-update.docx', 'update', 'document', 'source-update.html', ['note-muskox-model.html']),
    ('conceptual_diagram.png', 'conceptual-diagram.png', 'diagram', 'image', None, ['case-muskoxen.html', 'note-muskox-model.html', 'multimedia.html']),
    ('Benjamin Dupuis.jpg', 'benjamin-dupuis.jpg', 'benjamin', 'image', None, ['team.html#benjamin-dupuis', 'index.html', 'multimedia.html']),
    ('Profile picture Floris.jpg', 'floris-van-beest.jpg', 'floris', 'image', None, ['team.html#floris-van-beest', 'index.html', 'multimedia.html']),
]
with zipfile.ZipFile(ASSETS / 'wp3-materials.zip') as archive:
    for original, filename, key, kind, page, uses in zip_mapping:
        (ASSETS / filename).write_bytes(archive.read(original))
        entry = record(key, filename, original, 'WP3 ZIP', uses, parent='wp3zip', kind=kind, page=page)
        entry['member'] = original
        if kind == 'image':
            entry['credit'] = 'Supplied by the SPECIES WP3 team.'
            entry['alt'] = {'diagram': 'Working diagram linking muskox foraging, movement, energy and reproduction', 'benjamin': 'Portrait of Benjamin Dupuis', 'floris': 'Portrait of Floris M. van Beest'}[key]

pdf = PdfReader(ASSETS / 'luke-update.pdf')
images = [
    (1, 'Image30.jpg', 'juha-kantanen', 'Portrait of Juha Kantanen', 'Luke team portrait; photographer not specified.', ['team.html#juha-kantanen', 'index.html']),
    (1, 'Image31.jpg', 'kisun-pokharel', 'Portrait of Kisun Pokharel', 'Luke team portrait; photographer not specified.', ['team.html#kisun-pokharel']),
    (2, 'Image34.jpg', 'rodney-okwasiimire', 'Portrait of Rodney Okwasiimire', 'Luke team portrait; photographer not specified.', ['team.html#rodney-okwasiimire']),
    (2, 'Image35.jpg', 'melak-weldenegodguad', 'Portrait of Melak Weldenegodguad', 'Luke team portrait; photographer not specified.', ['team.html#melak-weldenegodguad']),
    (3, 'Image43.jp2', 'jonne-pohjankukka', 'Portrait of Jonne Pohjankukka', 'Luke team portrait; photographer not specified.', ['team.html#jonne-pohjankukka']),
    (4, 'Image47.jpg', 'finncattle-pasture', 'Northern Finncattle grazing in pasture', 'Photo: Annu Puurunen.', ['case-lapland-cattle.html', 'multimedia.html']),
    (5, 'Image50.jpg', 'finncattle-woodland', 'Northern Finncattle in a wooded landscape', 'Photo: Juha Kantanen.', ['note-genomics.html', 'multimedia.html']),
    (5, 'Image51.jpg', 'finncattle-archive', 'Northern Finncattle in an archive photograph', 'Photo: Luke Archive.', ['multimedia.html']),
]
for number, name, key, alt, credit, uses in images:
    image = next(item for item in pdf.pages[number].images if item.name == name)
    filename = key + Path(name).suffix
    (ASSETS / filename).write_bytes(image.data)
    entry = record(key, filename, alt, f'Luke PDF / page {number+1}', uses, parent='luke', kind='image', credit=credit, alt=alt)
    entry.update(pdf_page=number+1, member=name)

ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
for entry in entries:
    if not entry.get('page'):
        continue
    file = ROOT / entry['file']
    if file.suffix == '.docx':
        with zipfile.ZipFile(file) as archive:
            root = ET.fromstring(archive.read('word/document.xml'))
        paragraphs = [''.join(node.text or '' for node in p.findall('.//w:t', ns)) for p in root.findall('.//w:p', ns)]
    elif file.suffix == '.pdf':
        paragraphs = ['Page ' + str(i+1) + '\n' + page.extract_text() for i, page in enumerate(pdf.pages)]
    else:
        paragraphs = [file.read_text(encoding='utf-8-sig')]
    entry['text'] = 'drive-text/' + entry['key'] + '.json'
    (ROOT / 'data' / entry['text']).write_text(json.dumps(paragraphs, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

descriptions = {
    'main': 'Project identity, vision, research questions, methods, case studies, work packages and collaborators.',
    'test': 'A short test document containing Hey.',
    'wp3': 'Ecological modelling, co-creation, Greenland field settings and WP3 collaborators.',
    'wp3zip': 'Two researcher profiles, a Winnipeg research update, two portraits and a working model diagram.',
    'florian': 'Spring–summer 2026 fieldwork in Ajos: fishing, seals, hunting, material practices and cultural knowledge.',
    'luke': 'Northern livestock genomics, five team biographies, two activities and cattle conservation photographs.',
    'profiles': 'Research profiles of Benjamin Dupuis and Floris M. van Beest.',
    'update': 'A research visit to Winnipeg and development of muskox movement and energy-budget modelling.',
}
for entry in entries:
    entry['description'] = descriptions.get(entry['key'], entry.get('alt', entry['title']))
    if entry['kind'] == 'image' and 'multimedia.html' not in entry['uses']:
        entry['uses'].append('multimedia.html')
entries[0]['uses'].extend('case-' + key + '.html' for key in ['reindeer', 'king-crabs', 'wild-ducks', 'seals', 'lapland-cattle', 'polar-bears', 'muskoxen'])
manifest = dict(date='2026-11-02', root_url='https://drive.google.com/drive/folders/1cs_RIrYgbEW6Op_M-F44fQF9WWnDtU6Z', entries=entries,
                empty_folders=['SPECIES/Website/Reindeer', 'SPECIES/Website/King Crab'])
(ROOT / 'data/drive-library.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'Prepared {len(entries)} entries: 8 Drive files, 5 ZIP members and 8 PDF images.')
