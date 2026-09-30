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
resume_text = [r['headline'], r['lede'], 'EXPERIENCE']
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
D = json.dumps(data, ensure_ascii=False)
tpl = open(os.path.join(HERE, 'template.html')).read().replace('__PHOTO__', a.get('photo', 'img/headshot.jpg').lstrip('/'))
esc = lambda s: s.replace('&', '&amp;').replace('"', '&quot;').replace('<', '&lt;')

def page(view, title):
    body = tpl.replace('__TITLE__', esc(title)).replace('/*DATA*/', 'const CONFIG=' + json.dumps({'mode': 'local', 'view': view}) + ';\nconst DATA=' + D + ';')
    head = ('<!doctype html><html lang="en"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<meta name="description" content="' + esc(c['site']['description']) + '"></head><body>\n')
    return head + body + '\n</body></html>\n'

shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT)
shutil.copytree(os.path.join(HERE, 'img'), os.path.join(OUT, 'img'))
for f in ['CNAME']:
    if os.path.exists(os.path.join(HERE, f)):
        shutil.copy(os.path.join(HERE, f), OUT)
open(os.path.join(OUT, '.nojekyll'), 'w').close()

title = c['site']['title']
routes = {'': ('reel', title)}
for v in ['reel', 'home', 'home-page']:  # old links from the Adobe Portfolio site
    routes[v] = ('reel', title)
for v in ['work', 'about', 'resume', 'contact']:
    routes[v] = (v, v.capitalize() + ' · Eric Reier')
for p in projects:
    routes[p['slug']] = (p['slug'], p['title'] + ' · Eric Reier')
if 'spectrum-reach-tarta-wheels' in slugs:  # old link
    routes['spectrum-reach'] = ('spectrum-reach-tarta-wheels', 'Spectrum Reach / TARTA Wheels · Eric Reier')
for path, (view, t) in routes.items():
    d = os.path.join(OUT, path)
    os.makedirs(d, exist_ok=True)
    open(os.path.join(d, 'index.html'), 'w').write(page(view, t))
open(os.path.join(OUT, '404.html'), 'w').write(page('notfound', 'Page not found · Eric Reier'))
print(f'Built {len(routes)} pages into _site/')
