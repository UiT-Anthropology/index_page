"""Build the complete source library and the local Drive-to-website record."""
from pathlib import Path
from importlib.util import spec_from_file_location, module_from_spec
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
spec = spec_from_file_location('species_site', ROOT / 'build-species.py')
site = module_from_spec(spec)
spec.loader.exec_module(site)
manifest = json.loads((ROOT / 'data/drive-library.json').read_text(encoding='utf-8'))
entries = manifest['entries']
by_key = {entry['key']: entry for entry in entries}
e = site.e

def inherited_url(entry):
    return entry.get('drive_url') or inherited_url(by_key[entry['parent']])

def preview(entry):
    key = entry['key']
    if key == 'diagram':
        return 'assets/species/muskox-model.png'
    aliases = {'heidi': 'heidi-winter', 'skins': 'seal-skins', 'benjamin': 'benjamin-dupuis', 'floris': 'floris-van-beest'}
    return 'assets/species/' + aliases.get(key, key) + '.webp'

def image_card(entry):
    original = e('./' + entry['file'])
    return f'<figure class="library-image"><a href="{original}"><img src="./{e(preview(entry))}" alt="{e(entry["alt"])}" loading="lazy"/></a><figcaption><strong>{e(entry["title"])}</strong><span>{e(entry["credit"])}</span><a href="{original}" download>Download original image ↓</a></figcaption></figure>'

def actions(entry):
    text = f'<a href="./{e(entry["file"])}" download>Download {e(Path(entry["file"]).suffix[1:].upper())} ↓</a>'
    text += f'<a href="{e(inherited_url(entry))}">View Drive source ↗</a>'
    return '<div class="library-actions">' + text + '</div>'

for entry in entries:
    path = ROOT / 'dist' / entry['file']
    assert path.is_file(), path
    assert hashlib.sha256(path.read_bytes()).hexdigest() == entry['sha256'], f'Changed source: {path}'
    if not entry.get('page'):
        continue
    paragraphs = json.loads((ROOT / 'data' / entry['text']).read_text(encoding='utf-8'))
    body = '<nav class="breadcrumb" aria-label="Breadcrumb"><a href="./resources.html">Research materials</a> / Source document</nav>'
    body += site.intro('SOURCE DOCUMENT', e(entry['title']), 'Complete source text from the project’s supplied research materials.')
    body += '<article class="reading-column source-document">' + actions(entry)
    if entry['key'] == 'florian':
        body += '<p class="source-context">Original spring–summer 2026 fieldwork account by Florian Stammler. Interpretations and statements are presented in the author’s own words; references to photographs remain as supplied.</p>'
    if entry['key'] == 'luke':
        body += '<p class="source-context">September 2026 update. Page breaks are retained in this text transcription; the original PDF preserves the full layout and photographs.</p>'
    if entry['key'] == 'test':
        body += '<p class="source-context">A short test document supplied in the project folder.</p>'
    for paragraph in paragraphs:
        if not paragraph.strip():
            continue
        body += '<p class="source-paragraph">' + e(paragraph) + '</p>'
    related = [item for item in entries if item['kind'] == 'image' and (item.get('parent') == entry['key'] or (entry['key'] == 'profiles' and item['key'] in ['benjamin', 'floris']) or (entry['key'] == 'update' and item['key'] == 'diagram'))]
    body += '</article>'
    if related:
        body += '<section class="editorial-section"><h2>Images from this source</h2><div class="library-gallery">' + ''.join(image_card(item) for item in related) + '</div></section>'
    body += '<section class="related-links"><a href="./resources.html">← All research materials</a>' + ''.join(f'<a href="./{e(url)}">{e(url.split("#")[0].replace(".html", "").replace("-", " ").title())} ↗</a>' for url in entry['uses'][:3]) + '</section>'
    site.write(entry['page'], site.page(entry['title'], 'Complete supplied source document: ' + entry['title'], body, 'resources.html'))

body = site.intro('PROJECT COLLECTION', 'Research materials.', 'Project documents, fieldwork accounts, photographs and working diagrams.')
body += '<section class="editorial-section library-documents"><h2>Documents and source files</h2><div class="library-file-grid">'
for entry in entries:
    if entry['kind'] == 'image':
        continue
    heading = f'<a href="./{e(entry["page"])}">{e(entry["title"])} ↗</a>' if entry.get('page') else e(entry['title'])
    body += f'<article class="library-file" id="file-{e(entry["key"])}"><span class="team-page-kicker">{e(entry["folder"])}</span><h3>{heading}</h3><p>{e(entry["description"])}</p>'
    if entry.get('page'):
        body += f'<a class="text-link" href="./{e(entry["page"])}">Read complete text →</a>'
    body += actions(entry) + '</article>'
body += '</div></section><section class="editorial-section"><h2>Photographs and diagrams</h2><div class="library-gallery">'
body += ''.join(image_card(entry) for entry in entries if entry['kind'] == 'image')
body += '</div></section>'
site.write('resources.html', site.page('Research materials', 'Complete SPECIES source documents, original photographs and research diagrams.', body, 'resources.html'))

# Keep all generated pages discoverable even when the library is rebuilt on its own.
for path in (ROOT / 'dist').glob('*.html'):
    text = path.read_text(encoding='utf-8')
    if 'href="./resources.html">Research materials</a>' not in text and path.name != 'resources.html':
        text = text.replace('<a href="./index.html#partners">', '<a href="./resources.html">Research materials</a><a href="./index.html#partners">')
    path.write_text(text, encoding='utf-8')

lines = [
    '# Google Drive 文件与网站本地收录记录', '',
    '记录日期：2026-11-02（Europe/Paris）。本文件说明本地源资料、资源文件和网站页面的对应关系。', '',
    '## 收录范围', '',
    '- 来源：[SPECIES 项目文件夹](' + manifest['root_url'] + ')，包含根目录、Website 及其四个子文件夹，共六个目录。',
    '- 八个 Drive 原始文件全部收录；WP3 ZIP 的五个有效条目单独提取；Luke PDF 的八张内嵌图片单独提取。',
    '- 共 21 条资源记录、13 张图片、七个完整文本阅读页面。所有原件与文本均随本地网站提供，不依赖访客的 Drive 登录。',
    '- 原生 Google 文档 test 导出为 UTF-8 文本；内容为 Hey。其余 Drive 原件保留原始文件格式。',
    '- ZIP 中的五项 __MACOSX 元数据保留在原 ZIP 内，不另作图片或文档展示。',
    '- Reindeer 与 King Crab 文件夹为空，记录为空目录，不制作虚构内容。', '',
    '## 文件对应表', '',
    '下列路径均相对于仓库根目录；网站链接以 dist 为根。完整资料入口：[Research materials](dist/resources.html)。', '',
    '| 来源文件或条目 | 内容介绍 | 来源目录 | 本地原件 | 全文阅读 | 内容使用页面 |',
    '|---|---|---|---|---|---|',
]
for entry in entries:
    file = entry['file']
    reading = f'[完整文本](dist/{entry["page"]})' if entry.get('page') else ('图片展示于资料库和 Multimedia' if entry['kind'] == 'image' else 'ZIP 可下载；内部文档和图片单独列出')
    uses = '、'.join(f'[{url}](dist/{url})' for url in entry['uses'])
    lines.append(f'| [{entry["title"]}]({inherited_url(entry)}) | {entry["description"]} | {entry["folder"]} | [原件](dist/{file}) | {reading} | {uses} |')
lines += ['', '## 图片与署名', '', '| 图片 | 原件 | 网页预览 | 来源及署名 |', '|---|---|---|---|']
for entry in entries:
    if entry['kind'] == 'image':
        lines.append(f'| {entry["title"]} | [下载](dist/{entry["file"]}) | [预览](dist/{preview(entry)}) | {entry["credit"]} |')
lines += [
    '', '## 内容整理方式', '',
    '- 原始 Word 全文转换为可阅读 HTML，保留段落顺序与文字；表格单元格按原始顺序展开为段落。原始 Word 下载保留版式。',
    '- PDF 全文按页转录，原始 PDF 下载保留版式；其五张头像和三张牛照片可单独下载。',
    '- 项目总稿用于首页、About、案例与成员资料；三工作包组织结构补入 About。',
    '- 补充麝牛引入历史、北极熊与麝牛关系、牛的保种场/冷冻库/种群记录、研究联盟合作与具体研究方向。',
    '- 芬兰田野札记补充 ajopuu、文化遗产申请经历、捕鱼设备设计、鱼卵加工与季节实践；完整源稿保留作者对法律、健康与价格等问题的原始说法。',
    '- 文本阅读页明确作者及资料时间，完整保留源材料与其编辑后案例/札记的区别。',
    '- 已有八张成员头像、三张牛照片、皮张照片和模型图全部在资料库及 Multimedia 汇总。',
    '- 此次增加内容沿用网站已有英语；浏览器语言不受支持时显示英语。', '',
    '## 资料尚未提供的内容', '',
    '- Florian 原文中的捕鱼、鱼体标记、冰上狩猎、工具和加工等具名照片，当前 Drive 目录及原 Word 内均无对应图片。原文保留文件名引用，网页不伪造照片。',
    '- 主文档提到 Nordforsk - Sustainable Species.pdf，但当前项目目录没有该文件，也没有附件链接。',
    '- 野鸭目前仅有总稿中的物种与贡献者信息，无独立详细案例稿。', '',
    '## 文件核对', '',
    '每条记录保存字节数和 SHA-256，用于确认本地原件与收录清单一致。PDF 图片为 pypdf 提取后的图片文件。', '',
    '| 资源编号 | 字节数 | SHA-256 |', '|---|---:|---|',
]
for entry in entries:
    lines.append(f'| {entry["key"]} | {entry["bytes"]} | {entry["sha256"]} |')
lines += ['', '## 后续维护', '',
          '- 结构化清单：data/drive-library.json；正文快照：data/drive-text/；原件：dist/assets/drive/。',
          '- 修改案例、成员和札记：data/species.json。页面生成器：build-species.py，末尾自动调用 build-drive-library.py。',
          '- 仅重建资料库和本记录：python build-drive-library.py。',
          '- 更新原始资料后，可用包含 pypdf/Pillow 的 Python 运行 prepare-drive-library.py，再运行 python build-species.py。',
          '- 原件准备脚本从 audit/main.docx、audit/florian.docx、audit/wp3.zip 与 dist/assets/drive/ 的其余文件重建清单；更新时同步替换相应输入。',
          '- 检查：python check-species.py。资料库构建还会逐一核验清单中的文件 SHA-256。', '']
(ROOT / 'DRIVE-CONTENT-RECORD.md').write_text('\n'.join(lines), encoding='utf-8')
print('Built research library, 7 complete-text source pages and DRIVE-CONTENT-RECORD.md.')
