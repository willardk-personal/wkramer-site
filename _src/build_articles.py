"""Builds articles/from-amiga-to-m6.html from _src/articles/from-amiga-to-m6.src.html.
The source is the standalone page (no doctype); this adds the site masthead, fonts and footer.
Run from anywhere: python3 _src/build_articles.py"""
import pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
src = (ROOT / "_src/articles/from-amiga-to-m6.src.html").read_text()
out = ROOT / "articles/from-amiga-to-m6.html"

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>\n'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@100..125,500..800&family=IBM+Plex+Sans:wght@400;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">')

def swap(s, a, b):
    assert s.count(a) == 1, a[:70]
    return s.replace(a, b)

s = src
s = swap(s, '<meta name="claude:viewport-fit-sides" content="cover">\n', '')
# fonts: use the site's families
start = s.index('<link rel="preconnect" href="https://fonts.googleapis.com">')
end = s.index('<style>')
s = s[:start] + FONTS + '\n' + s[end:]
s = swap(s, '--font-display: "Chakra Petch", "Segoe UI", system-ui, sans-serif;',
            '--font-display: "Archivo", "Helvetica Neue", Arial, sans-serif;')
s = s.replace('"Chakra Petch, sans-serif"', '"Archivo, Helvetica Neue, Arial, sans-serif"')
s = s.replace('disp = "Chakra Petch, sans-serif"', 'disp = "Archivo, Helvetica Neue, Arial, sans-serif"')
# base reset the artifact host used to provide, plus the site masthead
extra_css = '''
/* page basics (the artifact host supplied these) */
html { -webkit-text-size-adjust: 100%; }
body { margin: 0; }
img { max-width: 100%; }
[hidden] { display: none !important; }
h1, h2, nav.tabs a { font-stretch: 110%; }
/* site masthead, matching wkramer.com */
:root { --ink: #0d1226; --ink-fg: #eef0fb; --ink-muted: #a4add0; --ink-line: #2a3360; }
.site-mast { background: var(--ink); color: var(--ink-fg); border-bottom: 6px solid var(--accent); }
.site-mast .wrap { display: flex; flex-wrap: wrap; gap: 6px 22px; align-items: baseline; padding-block: 18px; }
.site-mast a { font-size: 15px; color: var(--ink-muted); text-decoration: none; }
.site-mast a:hover { color: var(--ink-fg); }
.site-mast .brand { font: 700 18px var(--font-display); font-stretch: 112%; margin-right: auto; color: var(--ink-fg); letter-spacing: .01em; }
.site-mast a[aria-current="page"] { color: var(--ink-fg); font-weight: 600; box-shadow: 0 2px 0 var(--accent); }
.byline { font-family: var(--font-mono); font-size: 0.82rem; color: var(--muted); }
footer a { color: inherit; }
</style>'''
s = swap(s, '</style>', extra_css)
nav = ('<div class="site-mast gutter"><div class="wrap">'
       '<a class="brand" href="../index.html">Willard Kramer</a>'
       '<a href="../index.html">About</a><a href="../mac-mini.html">Mac mini setup</a>'
       '<a href="../macbook-pro.html">Mac Work Book Pro</a><a href="../dev-env.html">Dev environment</a>'
       '<a href="../articles.html" aria-current="page">Articles</a></div></div>\n')
s = swap(s, '<header class="top gutter">', nav + '<header class="top gutter">')
s = swap(s, '    <span class="eyebrow">1987 → 2026</span>\n    <h1>From Amiga to M6</h1>\n',
            '    <span class="eyebrow">Article · 1987 → 2026</span>\n    <h1>From Amiga to M6</h1>\n'
            '    <span class="byline">Willard Kramer · November 16, 2026</span>\n')
s = swap(s, '<p>In 1987 the Amiga 2000 spread its computer',
            '<p>I owned an Amiga 2000 with an A2088 XT Bridgeboard. In 1987 that machine spread its computer')
s = swap(s, '<footer class="gutter"><div class="wrap">Compiled Nov 16, 2026. Prices change daily; check the store before buying.</div></footer>',
            '<footer class="gutter"><div class="wrap">Compiled November 16, 2026. Prices change daily; check the store before buying.<br>'
            'Willard Kramer &middot; New York, NY &middot; <a href="mailto:willardk@gmail.com">willardk@gmail.com</a></div></footer>')
desc = ("How the Amiga 2000's board of separate chips and its A2088 PC-on-a-card became one Apple M6 die, "
        "with side-by-side comparisons of the M6 and M5 MacBooks and the iPad Pro.")
title_end = s.index('</title>') + len('</title>')
head = s[:title_end].replace('<title>From Amiga to M6</title>', '<title>From Amiga to M6 · Willard Kramer</title>')
s = ('<!doctype html>\n<html lang="en"><head><meta charset="utf-8">'
     '<meta name="viewport" content="width=device-width,initial-scale=1">\n'
     + head + f'<meta name="description" content="{desc}">\n'
     + s[title_end:])
# close head before the masthead
s = s.replace('</style>\n\n<div class="site-mast', '</style>\n</head><body>\n<div class="site-mast', 1)
s = s.rstrip() + '\n</body></html>\n'
assert s.count('<body>') == 1, s.count('<body>')
out.parent.mkdir(exist_ok=True)
out.write_text(s)
print("wrote", out, len(s))
