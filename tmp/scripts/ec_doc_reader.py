"""
READ-ONLY EC doc page fetcher for a deep-dive session.
Usage: py ec_doc_reader.py LABEL module1,module2,...
Selects technical-documentation pages in the given modules, fetches each page's content text,
saves to DeepDiveLearnings/ec-docs/_raw/LABEL_raw.md for synthesis.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, sys


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]


EC_BASE = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
KB = _repo_root() / 'DeepDiveLearnings' / 'ec-docs'
RAW = KB / '_raw'; RAW.mkdir(parents=True, exist_ok=True)

LABEL = sys.argv[1] if len(sys.argv) > 1 else 'DOC-01'
MODULES = (sys.argv[2].split(',') if len(sys.argv) > 2 else ['product_concept', 'user_guide', '(top)'])

idx = json.loads((KB / 'ec_doc_index_bucketed.json').read_text(encoding='utf-8'))
tech = idx.get('technical-documentation', [])


def module_of(abs_url):
    m = '/technical-documentation/'
    if m not in abs_url:
        return '(other)'
    tail = abs_url.split(m, 1)[1]
    seg = tail.split('/')
    return seg[0] if len(seg) > 1 else '(top)'


pages = [e for e in tech if module_of(e['abs']) in MODULES]
# dedupe + keep order
seen = set(); sel = []
for e in pages:
    if e['abs'] not in seen:
        seen.add(e['abs']); sel.append(e)
print(f'{LABEL}: {len(sel)} pages from modules {MODULES}')

out = [f'# Raw content — {LABEL}\nModules: {MODULES}\nPages: {len(sel)}\n']

with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()
    page.goto(EC_BASE, wait_until='domcontentloaded', timeout=30000)
    if page.locator('#username').count() > 0:
        page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
        page.wait_for_load_state('networkidle', timeout=40000)
    print('logged in')

    for i, e in enumerate(sel, 1):
        url = e['abs']
        try:
            page.goto(url, wait_until='domcontentloaded', timeout=40000)
            page.wait_for_timeout(700)
            data = page.evaluate("""() => {
                const pick = document.querySelector('article.doc') || document.querySelector('article')
                          || document.querySelector('.doc') || document.querySelector('main') || document.body;
                const title = (document.querySelector('h1') || {}).textContent || document.title || '';
                return {title: title.trim(), text: (pick.innerText||'').trim()};
            }""")
            txt = data['text']
            if len(txt) > 9000:
                txt = txt[:9000] + '\n…[truncated]'
            out.append(f'\n\n{"="*90}\n## [{i}/{len(sel)}] {data["title"] or e["text"]}\nURL: {url}\n{"="*90}\n{txt}')
            print(f'  [{i}/{len(sel)}] {data["title"][:55]}  ({len(txt)} chars)')
        except Exception as ex:
            out.append(f'\n\n## [{i}] {e["text"]} — FETCH ERROR: {ex}\nURL: {url}')
            print(f'  [{i}] ERROR {e["text"][:40]}: {ex}')

    ctx.close(); b.close()

(RAW / f'{LABEL}_raw.md').write_text('\n'.join(out), encoding='utf-8')
print(f'\nSaved raw to {RAW / (LABEL + "_raw.md")}')
