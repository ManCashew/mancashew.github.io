#!/usr/bin/env python3
"""Build ericreier.com from content.toml + template.html into _site/.

Run it yourself to preview (see README), or just push to GitHub and it runs there.
No installs needed, only Python 3.11 or newer.
"""
import json, os, shutil, sys, tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_site')

try:
    c = tomllib.load(open(os.path.join(HERE, 'content.toml'), 'rb'))
except tomllib.TOMLDecodeError as e:
    sys.exit(f'content.toml has a typo: {e}\n(Usually a missing quote or bracket near that line.)')

problems = []
projects = []
for p in c['projects']:
    for k in ['key', 'slug', 'title', 'credit_line', 'description', 'vimeo_link', 'player_url']:
        if not p.get(k):
            problems.append(f'project "{p.get("title", p.get("key", "?"))}" is missing {k}')
    p['thumbnail'] = (p.get('thumbnail') or f'img/{p.get("key")}.jpg').lstrip('/')
    if not os.path.exists(os.path.join(HERE, p['thumbnail'])):
        problems.append(f'project "{p.get("title")}" thumbnail {p["thumbnail"]} isn\'t in the img folder')
    q = {k: p.get(k, '') for k in ['key', 'slug', 'title', 'credit_line', 'description', 'vimeo_link', 'player_url']}
    q['thumb'] = p['thumbnail']
    q['listing'] = {'label': p['listing_label'], 'url': p['listing_url']} if p.get('listing_label') else None
    projects.append(q)
slugs = [p['slug'] for p in projects]
for s in set(slugs):
    if slugs.count(s) > 1:
        problems.append(f'two projects use the slug "{s}"')
if problems:
    sys.exit('Fix these in content.toml:\n  ' + '\n  '.join(problems))

r = c['resume']
resume_text = [r['headline'], 'EXPERIENCE']
for j in r['jobs']:
    resume_text += [j['title'], j['dates'], j['text']]
resume_text += ['SKILLS'] + r['skills'] + ['EDUCATION'] + r['education']

a = c['about']
data = {
    'projects': projects,
    'reel': {'text': c['reel']['text'], 'link': c['reel']['vimeo_link'], 'player_url': c['reel']['player_url'], 'still': c['reel'].get('still', 'img/reel.jpg').lstrip('/')},
    'about': {'paragraphs': a['paragraphs'], 'tools': a['tools'], 'clients': a['clients'], 'based': a['based']},
    'resume': {'text': resume_text, 'link': r['pdf_link']},
    'email': c['site']['email'], 'linkedin': c['site']['linkedin'],
}
D = json.dumps(data, ensure_ascii=False).replace('</', '<\\/')  # so text can never close the script tag
tpl = open(os.path.join(HERE, 'template.html')).read().replace('__PHOTO__', a.get('photo', 'img/headshot.jpg').lstrip('/'))
esc = lambda s: s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')
cname = os.path.join(HERE, 'CNAME')
SITE = 'https://' + (open(cname).read().strip() if os.path.exists(cname) else 'ericreier.com')
ICONS = ['favicon.png', 'apple-touch-icon.png']

def page(view, title, desc=None, image=None, canonical=None):
    """desc and image feed the preview card shown when a link is pasted into LinkedIn, Slack, iMessage, etc."""
    desc, image = esc((desc or c['site']['description']).strip()), SITE + '/' + (image or data['reel']['still'])
    body = tpl.replace('__TITLE__', esc(title)).replace('/*DATA*/', 'const CONFIG=' + json.dumps({'mode': 'local', 'view': view}) + ';\nconst DATA=' + D + ';')
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + desc + '">'
            '<meta name="theme-color" content="#000000">'
            '<link rel="icon" type="image/png" href="/favicon.png">'
            '<link rel="apple-touch-icon" href="/apple-touch-icon.png">')
    if canonical is None:
        head += '<meta name="robots" content="noindex">'
    else:
        url = SITE + '/' + (canonical + '/' if canonical else '')
        head += ('<link rel="canonical" href="' + url + '">'
                 '<meta property="og:type" content="website">'
                 '<meta property="og:site_name" content="Eric Reier">'
                 '<meta property="og:url" content="' + url + '">'
                 '<meta property="og:title" content="' + esc(title) + '">'
                 '<meta property="og:description" content="' + desc + '">'
                 '<meta property="og:image" content="' + esc(image) + '">'
                 '<meta name="twitter:card" content="summary_large_image">')
    return head + '</head><body>\n' + body + '\n</body></html>\n'

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
shutil.copytree(os.path.join(HERE, 'img'), os.path.join(OUT, 'img'))
for f in ['CNAME'] + ICONS:
    if os.path.exists(os.path.join(HERE, f)):
        shutil.copy(os.path.join(HERE, f), OUT)
open(os.path.join(OUT, '.nojekyll'), 'w').close()

# path -> (view, tab title, preview text, preview image, canonical path)
title = c['site']['title']
routes = {'': ('reel', title, None, None, '')}
for v in ['reel', 'home', 'home-page']:  # old links from the Adobe Portfolio site
    routes[v] = ('reel', title, None, None, '')
for v in ['work', 'about', 'resume', 'contact']:
    routes[v] = (v, v.capitalize() + ' · Eric Reier', None, None, v)
routes['about'] = routes['about'][:3] + (a.get('photo', 'img/headshot.jpg').lstrip('/'), 'about')
for p in projects:
    routes[p['slug']] = (p['slug'], p['title'] + ' · Eric Reier', p['description'], p['thumb'], p['slug'])
if 'spectrum-reach-tarta-wheels' in slugs:  # old link
    routes['spectrum-reach'] = routes['spectrum-reach-tarta-wheels']
for path, r in routes.items():
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(*r))
open(os.path.join(OUT, '404.html'), 'w').write(page('notfound', 'Page not found · Eric Reier'))

pages = sorted({r[4] for r in routes.values()})
open(os.path.join(OUT, 'sitemap.xml'), 'w').write(
    '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'  <url><loc>{SITE}/{p + "/" if p else ""}</loc></url>\n' for p in pages) + '</urlset>\n')
open(os.path.join(OUT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n')
print(f'Built {len(routes)} pages into _site/')
