"""Export public pages for GitHub Pages without publishing the database."""
import os
import re
import shutil
import sys
from html import unescape
from pathlib import Path
from urllib.parse import urlsplit, unquote

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
import django
django.setup()
from django.conf import settings
from django.test import Client, override_settings
from django.contrib.staticfiles import finders
from blog.models import Post
from portfolio.models import Proyecto

PREFIX = '/blog-tp-repo'
OUT = ROOT / 'docs'
OUT.mkdir(exist_ok=True)
paths = ['/', '/description/', '/cv/', '/blog/']
paths += [p.get_absolute_url() for p in Post.objects.publicados()]
paths += [p.get_absolute_url() for p in Proyecto.objects.filter(visible=True)]
count = Post.objects.publicados().count()
paths += [f'/blog/?page={n}' for n in range(2, (count + 4) // 5 + 1)]
assets = set()
rendered = []

def rewrite(match):
    attr, quote, value = match.groups()
    value = unescape(value)
    if value.startswith('/') and not value.startswith('//'):
        if value.startswith(('/static/', '/media/')):
            assets.add(urlsplit(value).path)
        value = PREFIX + value
    return f'{attr}={quote}{value}{quote}'

with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'], MIDDLEWARE=[m for m in settings.MIDDLEWARE if not m.startswith('debug_toolbar')]):
    client = Client()
    for path in paths:
        response = client.get(path)
        if response.status_code != 200:
            raise RuntimeError(f'{path}: HTTP {response.status_code}')
        text = response.content.decode('utf-8')
        text = re.sub(r'<a\b[^>]*href=[\"\"]/cuentas/[^>]*>.*?</a>', '', text, flags=re.S)
        text = re.sub(r'<section\b[^>]*id="comentarios"[^>]*>.*?</section>', '<section class="card-descripcion" id="comentarios"><p class="texto-card">Esta es la version estatica del blog. Los comentarios y las cuentas necesitan el sitio Django.</p></section>', text, flags=re.S)
        text = re.sub(r'(href|src|poster)=([\"\"])(.*?)\2', rewrite, text)
        url = urlsplit(path)
        dest = OUT / url.path.lstrip('/') / 'index.html'
        if url.query:
            dest = OUT / 'blog' / 'page' / url.query.split('=')[1] / 'index.html'
        text = re.sub(r'href="\?page=(\d+)"', lambda m: f'href="{PREFIX}/blog/' + ('' if m[1]=='1' else f'page/{m[1]}/') + '"', text)
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(text, encoding='utf-8')
        rendered.append(dest)

# Copy only public assets referenced in exported pages (never db.sqlite3).
for url in sorted(assets):
    relative = unquote(url).lstrip('/')
    if url.startswith('/static/'):
        source = finders.find(unquote(url)[len('/static/'):])
    else:
        source = settings.MEDIA_ROOT / unquote(url)[len('/media/'):]
    if not source or not Path(source).is_file():
        raise RuntimeError(f'Missing asset: {url}')
    dest = OUT / relative
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, dest)
# CSS files can reference additional images, fonts or videos.
for folder in [ROOT/'portfolio'/'static', ROOT/'blog'/'static']:
    if folder.is_dir():
        shutil.copytree(folder, OUT/'static', dirs_exist_ok=True)
(OUT/'.nojekyll').touch()
errors = []
for file in rendered:
    for value in re.findall(r'(?:href|src|poster)=[\"\"]([^\"\"]+)', file.read_text(encoding='utf-8')):
        if not value.startswith(PREFIX+'/'):
            continue
        target = OUT / unquote(urlsplit(value).path[len(PREFIX)+1:])
        if not target.is_file() and not (target/'index.html').is_file():
            errors.append(f'{file.relative_to(OUT)}: {value}')
if errors:
    raise RuntimeError('\n'.join(errors))
print(f'Exported {len(rendered)} pages; all internal links and referenced assets verified.')
