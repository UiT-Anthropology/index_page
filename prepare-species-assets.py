"""Extract supplied PDF images and produce web-sized copies; retain source files."""
from pathlib import Path
from io import BytesIO
from PIL import Image, ImageOps
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
ASSETS = ROOT / 'assets/species'
pdf = PdfReader(ASSETS / 'luke-research-update.pdf')
# Images follow the biographies across page breaks in the original six-page PDF.
mapping = {
    (1, 'Image30.jpg'): 'juha-kantanen',
    (1, 'Image31.jpg'): 'kisun-pokharel',
    (2, 'Image34.jpg'): 'rodney-okwasiimire',
    (2, 'Image35.jpg'): 'melak-weldenegodguad',
    (3, 'Image43.jp2'): 'jonne-pohjankukka',
    (4, 'Image47.jpg'): 'finncattle-pasture',
    (5, 'Image50.jpg'): 'finncattle-woodland',
    (5, 'Image51.jpg'): 'finncattle-archive',
}
for (number, filename), name in mapping.items():
    image = next(i for i in pdf.pages[number].images if i.name == filename)
    im = ImageOps.exif_transpose(Image.open(BytesIO(image.data))).convert('RGB')
    im.thumbnail((1600, 1600))
    im.save(ASSETS / (name + '.webp'), quality=86)
for filename in ['benjamin-dupuis.jpg', 'floris-van-beest.jpg', 'heidi-winter.jpg', 'seal-skins.jpg']:
    im = ImageOps.exif_transpose(Image.open(ASSETS / filename)).convert('RGB')
    im.thumbnail((1800, 1800) if filename == 'seal-skins.jpg' else (900, 1100))
    im.save(ASSETS / (Path(filename).stem + '.webp'), quality=86)
print('Prepared 12 web images from supplied originals.')
