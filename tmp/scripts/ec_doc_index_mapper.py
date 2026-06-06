"""
READ-ONLY: map the local EC documentation tree (/doc/Energy-Components/current/ecindex.html).
Logs in, opens the doc, enumerates frames + all links, and dumps a structured index so we
can split the deep dive into sessions. Saves to DeepDiveLearnings/ec-docs/.
"""
from playwright.sync_api import sync_playwright
from pathlib import Path
import json, os
from collections import defaultdict


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]


EC_BASE = 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/'
DOC_URL = EC_BASE + 'doc/Energy-Components/current/ecindex.html'
OUT = _repo_root() / 'DeepDiveLearnings' / 'ec-docs'
OUT.mkdir(parents=True, exist_ok=True)


with sync_playwright() as p:
    b = p.chromium.launch(headless=True, args=['--ignore-certificate-errors'])
    ctx = b.new_context(ignore_https_errors=True, viewport={'width': 1680, 'height': 1050})
    page = ctx.new_page()

    # login
    page.goto(EC_BASE, wait_until='domcontentloaded', timeout=30000)
    if page.locator('#username').count() > 0:
        page.fill('#username', 'sysadmin'); page.fill('#password', 'sysadmin'); page.click('#kc-login')
        page.wait_for_load_state('networkidle', timeout=40000)
    print('logged in')

    # open the doc
    page.goto(DOC_URL, wait_until='domcontentloaded', timeout=40000)
    page.wait_for_timeout(3000)
    print(f'doc title: {page.title()}')
    print(f'frames: {len(page.frames)}')
    for fr in page.frames:
        print(f'  frame: name="{fr.name}" url={fr.url[-70:] if fr.url else ""}')

    # collect links from every frame
    all_links = []
    for fr in page.frames:
        try:
            links = fr.evaluate("""() => {
                const out=[];
                document.querySelectorAll('a[href]').forEach(a=>{
                    const t=(a.textContent||'').trim();
                    out.push({text:t.substring(0,80), href:a.getAttribute('href')||'', abs:a.href||''});
                });
                return out;
            }""")
            for l in links:
                l['frame'] = fr.name or '(main)'
            all_links += links
        except Exception as e:
            print(f'  frame read error: {e}')

    # dedupe by abs url
    seen = set(); uniq = []
    for l in all_links:
        key = l['abs'] or l['href']
        if key and key not in seen:
            seen.add(key); uniq.append(l)
    print(f'\nTotal links: {len(all_links)}  unique: {len(uniq)}')

    # categorize by first path segment after .../current/
    def section(href_abs):
        h = href_abs
        marker = '/current/'
        if marker in h:
            tail = h.split(marker, 1)[1]
            seg = tail.split('/')
            return seg[0] if len(seg) > 1 else '(root)'
        return '(other)'

    buckets = defaultdict(list)
    for l in uniq:
        buckets[section(l['abs'])].append(l)

    print('\n=== Top-level sections (by path) ===')
    for sec in sorted(buckets, key=lambda k: -len(buckets[k])):
        print(f'  {sec:<32} {len(buckets[sec]):>4} pages')

    # save raw + bucketed
    (OUT / 'ec_doc_index_raw.json').write_text(json.dumps(uniq, indent=1), encoding='utf-8')
    bsumm = {sec: [{'text': l['text'], 'abs': l['abs']} for l in ls] for sec, ls in buckets.items()}
    (OUT / 'ec_doc_index_bucketed.json').write_text(json.dumps(bsumm, indent=1), encoding='utf-8')
    page.screenshot(path=str(OUT / 'ec_doc_index.png'), full_page=True)

    # also try to capture the TOC tree text (often a nav frame)
    print('\n=== Sample top-of-tree entries ===')
    for l in uniq[:40]:
        if l['text']:
            print(f'  [{l["frame"]}] {l["text"][:50]:<50} -> {l["href"][:50]}')

    ctx.close(); b.close()

print(f'\nIndex saved to {OUT}')
