from pathlib import Path
import json, html
import yaml
import markdown

ROOT = Path(__file__).resolve().parents[1]
CONTENT = ROOT / "content"
TUTORIAL_DIR = CONTENT / "tutorials"
RESEARCH_DIR = CONTENT / "research"
SERVICE_DIR = CONTENT / "services"
SITE_DIR = CONTENT / "site"
TUTORIAL_OUT = ROOT / "tutorials"
TUTORIAL_OUT.mkdir(parents=True, exist_ok=True)


def read_markdown(path):
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return meta, parts[2].lstrip()


def as_text(value):
    if value is None:
        return ""
    return str(value)


def json_dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2, default=str), encoding="utf-8")


def article_page(meta, body_zh, slug):
    title_zh = html.escape(as_text(meta.get("title_zh") or slug))
    title_en = html.escape(as_text(meta.get("title_en") or meta.get("title_zh") or slug))
    category = html.escape(as_text(meta.get("category") or "Tutorial"))
    date = html.escape(as_text(meta.get("date") or ""))
    image = as_text(meta.get("image") or "")
    image_html = f'<img class="article-cover" src="{html.escape(image)}" alt="{title_zh}">' if image else ""
    body_en_raw = as_text(meta.get("body_en") or "")
    body_en = markdown.markdown(body_en_raw, extensions=["fenced_code", "tables"]) if body_en_raw else '<p>English version will be available soon.</p>'
    body_zh_html = markdown.markdown(body_zh, extensions=["fenced_code", "tables"])

    return f'''<!doctype html>
<html lang="zh-Hant">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="description" content="{html.escape(as_text(meta.get('summary_zh') or 'Bioinfo & Stats Lab tutorial'))}">
<title>{title_zh} | Bioinfo & Stats Lab</title>
<link rel="stylesheet" href="/style.css">
<style>
.article-wrap{{width:min(900px,calc(100% - 36px));margin:62px auto 100px}}
.article-nav{{display:flex;justify-content:space-between;align-items:center;gap:16px;margin-bottom:42px}}
.article-nav a{{color:#6048bd;font-weight:700}}
.article-lang button{{border:1px solid #d8d1ee;background:white;padding:7px 11px;border-radius:999px;cursor:pointer}}
.article-meta{{font-size:.75rem;letter-spacing:.1em;color:#7854dc;font-weight:800}}
.article-wrap h1{{font-size:clamp(2.2rem,5vw,3.8rem);line-height:1.12;letter-spacing:-.035em;margin:10px 0}}
.article-subtitle{{color:#747a8f;margin-bottom:28px}}
.article-cover{{max-height:420px;object-fit:cover;border-radius:20px;margin:26px 0}}
.article-body{{margin-top:26px;padding:38px;background:white;border:1px solid #e9e6f3;border-radius:22px;box-shadow:0 16px 45px rgba(88,71,126,.08)}}
.article-body h2,.article-body h3{{margin-top:1.7em}}
.article-body p,.article-body li{{color:#39415a}}
.article-body pre{{overflow:auto;background:#171a24;color:#f5f5f5;padding:18px;border-radius:12px}}
.article-body code{{font-family:ui-monospace,SFMono-Regular,Menlo,monospace}}
.article-body table{{border-collapse:collapse;width:100%}} .article-body th,.article-body td{{border:1px solid #ddd;padding:8px}}
@media(max-width:650px){{.article-body{{padding:24px}}}}
</style>
</head><body>
<main class="article-wrap">
<div class="article-nav"><a href="/#tutorials">← Tutorials</a><div class="article-lang"><button onclick="setArticleLang('zh')">中文</button> <button onclick="setArticleLang('en')">EN</button></div></div>
<p class="article-meta">{category.upper()} · {date}</p>
<section data-article-zh><h1>{title_zh}</h1><p class="article-subtitle">{title_en}</p>{image_html}<div class="article-body">{body_zh_html}</div></section>
<section data-article-en hidden><h1>{title_en}</h1><p class="article-subtitle">{title_zh}</p>{image_html}<div class="article-body">{body_en}</div></section>
</main>
<script>function setArticleLang(l){{document.documentElement.lang=l==='zh'?'zh-Hant':'en';document.querySelector('[data-article-zh]').hidden=l!=='zh';document.querySelector('[data-article-en]').hidden=l!=='en';}}</script>
</body></html>'''


def build_tutorials():
    items = []
    for path in TUTORIAL_DIR.glob("*.md"):
        meta, body = read_markdown(path)
        slug = path.stem
        (TUTORIAL_OUT / f"{slug}.html").write_text(article_page(meta, body, slug), encoding="utf-8")
        items.append({
            "category": meta.get("category", "Tutorial"),
            "title_zh": meta.get("title_zh", slug),
            "title_en": meta.get("title_en") or meta.get("title_zh", slug),
            "summary_zh": meta.get("summary_zh", ""),
            "summary_en": meta.get("summary_en") or meta.get("summary_zh", ""),
            "date": meta.get("date", ""),
            "image": meta.get("image", ""),
            "url": f"/tutorials/{slug}.html"
        })
    items.sort(key=lambda x: as_text(x.get("date")), reverse=True)
    json_dump(TUTORIAL_DIR / "index.json", items)
    return len(items)


def build_collection(folder, output_name, fields):
    items = []
    for path in folder.glob("*.md"):
        meta, _ = read_markdown(path)
        item = {k: meta.get(k, default) for k, default in fields.items()}
        item["slug"] = path.stem
        items.append(item)
    items.sort(key=lambda x: int(x.get("order") or 99))
    json_dump(folder / output_name, items)
    return len(items)


def build_about():
    src = SITE_DIR / "about.yml"
    if not src.exists():
        return 0
    data = yaml.safe_load(src.read_text(encoding="utf-8")) or {}
    json_dump(SITE_DIR / "about.json", data)
    return 1


t = build_tutorials()
r = build_collection(RESEARCH_DIR, "index.json", {
    "title_zh": "", "title_en": "", "description_zh": "", "description_en": "",
    "image": "", "order": 99
})
s = build_collection(SERVICE_DIR, "index.json", {
    "title_zh": "", "title_en": "", "description_zh": "", "description_en": "",
    "color": "purple", "icon": "✦", "items_zh": [], "items_en": [], "order": 99
})
a = build_about()
print(f"Built {t} tutorial(s), {r} research item(s), {s} service(s), about={a}.")
