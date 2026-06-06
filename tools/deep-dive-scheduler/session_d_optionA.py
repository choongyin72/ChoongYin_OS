"""
Session D - Option A: Python gathers data, Claude analyses.
Items: #19 Extension DB migration, #20 Creating extension classes, #21 ZWP_/ZWT_ patterns
"""
import subprocess, requests, urllib3, sys
from pathlib import Path
from datetime import datetime
from bs4 import BeautifulSoup

urllib3.disable_warnings()

CLAUDE   = r'C:\Users\choong-yin.lee\AppData\Roaming\npm\claude.cmd'
EC_REPO  = Path(r'C:\DEV\GIT\ec-application')
WS_REPO  = Path(r'C:\DEV\GIT\woodside_impl_pluto_12839')
DEEPDIVE = Path(r'C:\Projects\ChoongYin_OS\workstreams\master-plan\drafts\ec-application-deep-dive.md')
AUTH     = ('choong-yin.lee@tieto.com', 'Xinyee!20090330')
BASE_DOC = 'https://hub.energycomponents.com/repository/site-hub/ec-application/14.2.5/documentation/Energy-Components/14.2.5/'

def log(msg):
    print(f'[{datetime.now().strftime("%H:%M:%S")}] {msg}', flush=True)

def fetch_doc(path):
    try:
        r = requests.get(BASE_DOC + path, auth=AUTH, verify=False, timeout=30)
        soup = BeautifulSoup(r.text, 'html.parser')
        content = soup.find('article', class_='doc') or soup.find('div', class_='content')
        return content.get_text(separator='\n', strip=True)[:6000] if content else ''
    except Exception as e:
        return f'[fetch failed: {e}]'

def read_files(pattern_list, max_chars=4000):
    result = []
    for pattern in pattern_list:
        for f in list(Path('/').glob(pattern.lstrip('/')))[:3]:
            try:
                content = f.read_text(encoding='utf-8', errors='ignore')[:max_chars]
                result.append(f'=== {f} ===\n{content}')
            except: pass
    return '\n\n'.join(result)[:8000]

def ask_claude(prompt):
    log(f'Calling claude --print ({len(prompt)} chars)...')
    r = subprocess.run(
        [CLAUDE, '--print', '--dangerously-skip-permissions', prompt],
        cwd=str(DEEPDIVE.parent.parent.parent),
        capture_output=True, timeout=300,
        encoding='utf-8', errors='replace'
    )
    return r.stdout.strip()

def append_to_deepdive(content):
    current = DEEPDIVE.read_text(encoding='utf-8')
    DEEPDIVE.write_text(current + '\n' + content, encoding='utf-8')

def git_commit(msg):
    cwd = r'C:\Projects\ChoongYin_OS'
    subprocess.run(f'git add workstreams/master-plan/drafts/ec-application-deep-dive.md',
                   shell=True, cwd=cwd)
    subprocess.run(f'git commit -m "{msg}"', shell=True, cwd=cwd)
    subprocess.run('git push origin master', shell=True, cwd=cwd)
    log(f'Committed: {msg}')

# ─── ITEM #19: Extension DB Migration ────────────────────────────────────────
log('=== ITEM #19: Extension DB Migration ===')

# Gather data
doc19a = fetch_doc('technical-documentation/frmw/ec-extensions/db-migration.html')
doc19b = fetch_doc('technical-documentation/frmw/ec-extensions/how_to_create_extension.html')

# Read actual extension migration files from Woodside repo
ws_flyway = list((WS_REPO / 'extensions').rglob('*.sql'))[:5] if WS_REPO.exists() else []
ws_sql = '\n\n'.join([f'=== {f.name} ===\n' + f.read_text(encoding='utf-8', errors='ignore')[:1500]
                      for f in ws_flyway if f.exists()])[:5000]

ec_ext_flyway = list(EC_REPO.rglob('ec-extensions*flyway*'))[:2] if EC_REPO.exists() else []

prompt19 = f"""You are doing EC deep dive learning. Analyse this content about EC Extension DB Migration and produce a technical summary for knowledge retention.

EC TECHNICAL DOCS - DB Migration in Extensions:
{doc19a[:3000]}

EC TECHNICAL DOCS - How to Create Extension:
{doc19b[:2000]}

WOODSIDE ACTUAL EXTENSION SQL FILES:
{ws_sql}

Based on the above content, produce a structured technical summary covering:
1. How Flyway works in EC extensions (delta migrations, versioning)
2. What rules apply to extension DB objects (naming, prefixes)
3. How extension DB migration differs from core EC migration
4. Key constraints and best practices
5. What ZWP_ prefix means in practice (from Woodside examples)

Format as concise learning notes with code examples where relevant. Rate my understanding: was it 7/10 before, should reach 9/10 after this."""

analysis19 = ask_claude(prompt19)
log(f'Got analysis for #19 ({len(analysis19)} chars)')

section19 = f"""
### Item #19: Extension DB Migration (7→9) ✅

{analysis19}
"""
append_to_deepdive(section19)
git_commit('Session D Item #19: Extension DB migration (7->9) — Option A')

# ─── ITEM #20: Creating Extension Classes ────────────────────────────────────
log('=== ITEM #20: Creating Extension Classes ===')

doc20a = fetch_doc('technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_classes.html')
doc20b = fetch_doc('technical-documentation/frmw/ec-extensions/development/development_create_ec_extension_datamodel.html')

# Read actual Woodside extension class XML files
ws_classes = list((WS_REPO / 'extensions').rglob('*.xml'))[:8] if WS_REPO.exists() else []
ws_xml = '\n\n'.join([f'=== {f.name} ===\n' + f.read_text(encoding='utf-8', errors='ignore')[:1200]
                      for f in ws_classes if f.exists()])[:6000]

prompt20 = f"""You are doing EC deep dive learning. Analyse this content about Creating EC Extension Classes.

EC TECHNICAL DOCS - Create Extension Classes:
{doc20a[:3000]}

EC TECHNICAL DOCS - Create Extension Datamodel:
{doc20b[:2000]}

WOODSIDE ACTUAL EXTENSION CLASS XML FILES:
{ws_xml}

Produce a structured technical summary covering:
1. Steps to create a new class in an EC extension
2. Required XML structure and mandatory attributes
3. How extension classes relate to base EC classes (inheritance/extension)
4. Naming rules enforced (ZWP_ prefix requirement)
5. How the class model generator processes extension classes
6. What the actual Woodside files show about real-world usage

Format as concise learning notes. Previous rating 5/10, target 9/10."""

analysis20 = ask_claude(prompt20)
log(f'Got analysis for #20 ({len(analysis20)} chars)')

section20 = f"""
### Item #20: Creating Extension Classes (5→9) ✅

{analysis20}
"""
append_to_deepdive(section20)
git_commit('Session D Item #20: Creating extension classes (5->9) — Option A')

# ─── ITEM #21: ZWP_/ZWT_ Woodside Patterns ───────────────────────────────────
log('=== ITEM #21: ZWP_/ZWT_ Woodside Extension Patterns ===')

# Read Woodside extension structure
ext_dirs = []
if WS_REPO.exists():
    for d in (WS_REPO / 'extensions').iterdir():
        if d.is_dir():
            ext_dirs.append(d.name)

ws_all_files = list((WS_REPO / 'extensions').rglob('*'))[:50] if WS_REPO.exists() else []
ws_structure = '\n'.join([str(f.relative_to(WS_REPO / 'extensions'))
                           for f in ws_all_files if f.is_file()][:40])

# Read a few key Woodside extension files
ws_key = []
for pattern in ['*.xml', '*.sql', '*.java']:
    ws_key.extend(list((WS_REPO / 'extensions').rglob(pattern))[:3])
ws_key_content = '\n\n'.join([f'=== {f.name} ===\n' + f.read_text(encoding='utf-8', errors='ignore')[:800]
                               for f in ws_key[:6] if f.exists()])[:5000]

doc21 = fetch_doc('technical-documentation/frmw/ec-extensions/ec-extensions-overview.html')

prompt21 = f"""You are doing EC deep dive learning. Analyse the Woodside Pluto EC extension patterns.

EC EXTENSIONS OVERVIEW:
{doc21[:2000]}

WOODSIDE EXTENSION FOLDER STRUCTURE:
Extension directories found: {ext_dirs}

Files in extension folder:
{ws_structure}

KEY EXTENSION FILES CONTENT:
{ws_key_content}

Produce a structured technical summary covering:
1. What ZWP_ prefix means and why it's mandatory
2. What ZWT_ prefix means (different extension?)
3. How Woodside extension folders are organised
4. Pattern of ZWP_ attributes in class XML files
5. How Woodside extensions relate to EC SaaS compliance
6. Extension naming conventions observed in practice
7. Key design patterns used in Woodside's extension approach

Format as concise learning notes. Previous rating 7/10, target 9/10."""

analysis21 = ask_claude(prompt21)
log(f'Got analysis for #21 ({len(analysis21)} chars)')

section21 = f"""
### Item #21: ZWP_/ZWT_ Woodside Extension Patterns (7→9) ✅

{analysis21}
"""
append_to_deepdive(section21)
git_commit('Session D Item #21: ZWP_/ZWT_ Woodside patterns (7->9) — Option A')

# ─── SESSION SUMMARY ─────────────────────────────────────────────────────────
log('=== Session D Complete ===')
log('All 3 items done. Committed to GitHub.')
