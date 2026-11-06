from pathlib import Path
import html
import re
import yaml
from PIL import Image

ROOT = Path(__file__).resolve().parent
data = yaml.safe_load((ROOT / 'content.yaml').read_text())
esc = lambda value: html.escape(str(value), quote=True)

def value(path):
    result = data
    for key in path.split('.'):
        result = result[key]
    return esc(result)

for name in ['hero', 'lookbook', 'detail']:
    image = Image.open(ROOT / 'img' / f'{name}.png').convert('RGB')
    image.thumbnail((1920, 1600))
    image.save(ROOT / 'img' / f'{name}.webp', quality=88)

sheet = Image.open(ROOT / 'img/products.png').convert('RGB')
w, h = sheet.size
for index, name in enumerate(['hoodie', 'shell', 'tee', 'cap']):
    x, y = index % 2, index // 2
    sheet.crop((x*w//2, y*h//2, (x+1)*w//2, (y+1)*h//2)).save(ROOT / 'img' / f'{name}.webp', quality=90)

cards = []
for index, product in enumerate(data['products'], 1):
    cards.append(f'''<article class="product reveal"><div class="product-image"><span class="product-index">0{index}</span><img src="./img/{esc(product['image'])}" alt="{esc(product['alt'])}" loading="lazy" width="768" height="768"><span class="product-concept">CONCEPT IA</span></div><div class="product-title"><h3>{esc(product['name'])}</h3><span aria-hidden="true">↗</span></div><p class="product-description">{esc(product['description'])}</p><p class="micro product-status">{esc(data['collection']['status'])}</p></article>''')
items = []
for index, item in enumerate(data['construction']['items'], 1):
    items.append(f'<div class="construction-item"><span class="micro">0{index}</span><div><h3>{esc(item["title"])}</h3><p>{esc(item["text"])}</p></div></div>')
page = (ROOT / 'template.html').read_text()
page = page.replace('{{products_html}}', ''.join(cards)).replace('{{construction_html}}', ''.join(items))
page = re.sub(r'\{\{([a-zA-Z_.]+)\}\}', lambda match: value(match.group(1)), page)
(ROOT / 'index.html').write_text(page)
print('Prototype generated from content.yaml — 9 sections, 4 products.')
