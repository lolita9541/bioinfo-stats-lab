from pathlib import Path
from datetime import datetime
import json, re, html

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content" / "tutorials"
OUT = ROOT / "tutorials"
INDEX = CONTENT / "index.json"
OUT.mkdir(parents=True, exist_ok=True)


def parse_frontmatter(text):
    if not text.startswith('---'):
        return {}, text
    parts = text.split('---', 2)
    if len(parts) < 3:
        return {}, text
    raw, body = parts[1], parts[2].lstrip()
    data = {}
    for line in raw.splitlines():
        if ':' not in line:
            continue
        k, v = line.split(':', 1)
        k, v = k.strip(), v.strip()
        if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
            v = v[1:-1]
        data[k] = v
    return data, body


def markdown_to_html(md):
    lines = md.splitlines()
    out = []
    in_code = False
    code = []
    for line in lines:
        if line.startswith('```'):
            if not in_code:
                in_code = True; code = []
            else:
                out.append('<pre><code>' + html.escape('\n'.join(code)) + '</code></pre>')
                in_code = False
            continue
        if in_code:
            code.append(line); continue
        s = line.strip()
        if not s:
            continue
        if s.startswith('### '):
            out.append(f'<h3>{inline_md(s[4:])}</h3>')
        elif s.startswith('## '):
            out.append(f'<h2>{inline_md(s[3:])}</h2>')
        elif s.startswith('# '):
            out.append(f'<h1>{inline_md(s[2:])}</h1>')
        elif s.startswith('- '):
            if not out or not out[-1].startswith('<ul'):
                out.append('<ul>')
            out.append(f'<li>{inline_md(s[2:])}</li>')
        else:
            if out and out[-1] == '</ul>':
                pass
            out.append(f'<p>{inline_md(s)}</p>')
    # normalize UL blocks
    normalized=[]; ul_open=False
    for item in out:
        if item=='<ul>':
            if not ul_open: normalized.append(item); ul_open=True
            continue
        if ul_open and not item.startswith('<li>'):
            normalized.append('</ul>'); ul_open=False
        normalized.append(item)
    if ul_open: normalized.append('</ul>')
    return '\n'.join(normalized)


def inline_md(s):
    s = html.escape(s)
    s = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', s)
    return s


def page_html(meta, body_html, slug):
    zh = html.escape(meta.get('title_zh', slug))
    en = html.escape(meta.get('title_en', zh))
    cat = html.escape(meta.get('category', 'Tutorial'))
    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{zh} | Bioinfo & Stats Lab</title>
<link rel="stylesheet" href="/style.css">
<style>
.article-wrap{{width:min(860px,calc(100% - 36px));margin:70px auto 100px}}
.article-top{{display:flex;justify-content:space-between;gap:18px;align-items:center}}
.article-wrap h1{{font-size:clamp(2rem,5vw,3.5rem);line-height:1.15}}
.article-meta{{font-size:.75rem;letter-spacing:.1em;color:#7854dc;font-weight:800}}
.article-body{{margin-top:28px;padding:32px;border:1px solid #e9e6f3;border-radius:20px;box-shadow:0 16px 45px rgba(88,71,126,.08)}}
.article-body pre{{overflow:auto;background:#171a24;color:#f5f5f5;padding:16px;border-radius:12px}}
.lang-mini button{{border:1px solid #d8d1ee;background:white;padding:7px 10px;border-radius:999px;cursor:pointer}}
</style>
</head><body>
<main class="article-wrap">
<div class="article-top"><a href="/">← Home</a><div class="lang-mini"><button onclick="document.documentElement.lang='zh-Hant';document.querySelectorAll('[data-enblock]').forEach(x=>x.hidden=true);document.querySelectorAll('[data-zhblock]').forEach(x=>x.hidden=false)">中文</button> <button onclick="document.documentElement.lang='en';document.querySelectorAll('[data-zhblock]').forEach(x=>x.hidden=true);document.querySelectorAll('[data-enblock]').forEach(x=>x.hidden=false)">EN</button></div></div>
<p class="article-meta">{cat.upper()} · TUTORIAL</p>
<div data-zhblock><h1>{zh}</h1></div><div data-enblock hidden><h1>{en}</h1></div>
<div class="article-body" data-zhblock>{body_html}</div>
<div class="article-body" data-enblock hidden><p>English version can be added from the CMS field “English Content”.</p></div>
</main></body></html>'''

items=[]
for mdfile in sorted(CONTENT.glob('*.md'), reverse=True):
    text = mdfile.read_text(encoding='utf-8')
    meta, body = parse_frontmatter(text)
    slug = mdfile.stem
    out_file = OUT / f'{slug}.html'
    out_file.write_text(page_html(meta, markdown_to_html(body), slug), encoding='utf-8')
    items.append({
        'category': meta.get('category','Tutorial'),
        'title_zh': meta.get('title_zh', slug),
        'title_en': meta.get('title_en', meta.get('title_zh',slug)),
        'summary_zh': meta.get('summary_zh',''),
        'summary_en': meta.get('summary_en', meta.get('summary_zh','')),
        'date': meta.get('date',''),
        'url': f'/tutorials/{slug}.html'
    })

INDEX.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Built {len(items)} tutorial(s).')
