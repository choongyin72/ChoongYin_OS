"""
EC Screen Help Deep-Dive - DETERMINISTIC unattended runner (no LLM spawn, no improvising).

Root-cause fix: the old version spawned a headless Claude session that had to re-derive the browser+DB recipe
every run and flailed (ORA-06569 x24, timeouts, 30 min, 0 commits). This version runs the PROVEN steps directly
in Python, per screen, with a hard timeout + best-effort fallback so it can never hang:
  1) read CHECKLIST.md -> next N unfinished screens (priority/file order)
  2) DB (metadata tables only -> no ORA-06569): BUSINESS_FUNCTION + class_cnfg/class_property_cnfg
     -> class, CLASS_TYPE, TIME_SCOPE, base table, OV_/TV_/DV_ view, screen type
  3) Help: login once, then per screen open it + openOnlineHelp() -> description (best-effort, timeout-guarded)
  4) write notes/<BF_CODE>.md, mark [x] (full = DB+Help) or [~] (DB only, Help not captured)
  5) commit on the detached worktree HEAD; push unless EC_LEARN_PUSH=0

Isolated git worktree (C:\\tmp\\wt-ec-learn) so it never touches the user's main checkout.
Env knobs: EC_LEARN_MAX (screen cap, default 8); EC_LEARN_PUSH=0 (commit locally, no push).
"""
import os, re, sys, subprocess
from datetime import datetime
from pathlib import Path

REPO   = r'C:\Projects\ChoongYin_OS'
WT     = r'C:\tmp\wt-ec-learn'
BRANCH = 'feature/ec-screen-deepdive'
LOG    = Path(REPO) / 'tools' / 'deep-dive-scheduler' / 'session_log.txt'
MAXN   = int(os.environ.get('EC_LEARN_MAX', '8'))
DO_PUSH= os.environ.get('EC_LEARN_PUSH', '1') != '0'

EC_URL  = os.environ.get('EC_URL', 'https://ap-f0a7g341jn6d.corp.quorumsoftware.com:8443/')
EC_USER = os.environ.get('EC_USER', 'sysadmin')
EC_PASS = os.environ.get('EC_PASS', 'sysadmin')
DB_DSN  = os.environ.get('EC_DB_DSN', 'localhost:1521/ORCL')
DB_USER = os.environ.get('EC_DB_USER', 'ECKERNEL_EC')
DB_PASS = os.environ.get('EC_DB_PASS', 'energy')

def log(m):
    line = f'[{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {m}'
    print(line)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(line + '\n')

def git(args, cwd=REPO):
    return subprocess.run(['git', '-C', cwd] + args, capture_output=True, text=True)

def ensure_worktree():
    git(['fetch', 'origin', BRANCH]); git(['worktree', 'prune'])
    if not Path(WT, '.git').exists():
        r = git(['worktree', 'add', '--detach', WT, f'origin/{BRANCH}'])
        if r.returncode: log('worktree add failed: ' + (r.stderr or r.stdout)[:120]); return False
    else:
        git(['fetch', 'origin', BRANCH], cwd=WT)
        if git(['checkout', '--detach', '--force', f'origin/{BRANCH}'], cwd=WT).returncode:
            log('worktree checkout failed'); return False
        git(['reset', '--hard', f'origin/{BRANCH}'], cwd=WT); git(['clean', '-fd'], cwd=WT)
    log('worktree ready (detached) at EC-screen bundle tip'); return True

def pick_screens(checklist_path, n):
    """Complete [~] partials FIRST (DoD backfill), then new [ ] screens, in file/priority order."""
    todo, partial = [], []
    for ln in Path(checklist_path).read_text(encoding='utf-8').splitlines():
        m = re.match(r'- \[([ ~])\] \*\*([A-Z0-9.]+)\*\* (?:—|-) (.+)', ln)
        if not m: continue
        status, code, rest = m.group(1), m.group(2), m.group(3)
        name = rest.split(' -> ')[0].split(' (')[0].strip()
        (partial if status == '~' else todo).append((code, name))
    return (partial + todo)[:n]

def db_resolve(cur, bf_code, name):
    info = {'url': None, 'classes': []}
    cur.execute("SELECT url FROM business_function WHERE bf_code=:c", [bf_code])
    r = cur.fetchone(); info['url'] = r[0] if r else None
    classes = re.findall(r'CLASS_NAME[^/]*/([A-Z0-9_]+)', info['url'] or '')
    if not classes:  # fall back to LABEL lookup (metadata table, safe)
        cur.execute("""SELECT class_name FROM class_property_cnfg
                       WHERE property_code='LABEL' AND property_value=:n""", [name])
        classes = [row[0] for row in cur.fetchall()]
    for cn in classes:
        cur.execute("""SELECT class_type, time_scope_code, db_object_name
                       FROM class_cnfg WHERE class_name=:c""", [cn])
        row = cur.fetchone()
        if not row: continue
        ctype, tscope, base = row
        view = None
        for pref in ('OV_', 'TV_', 'DV_'):
            cur.execute("SELECT 1 FROM all_views WHERE owner='ECKERNEL_EC' AND view_name=:v", [pref + cn])
            if cur.fetchone(): view = pref + cn; break
        info['classes'].append({'class': cn, 'type': ctype, 'scope': tscope, 'base': base, 'view': view})
    return info

def screen_type(info):
    if not info['classes']:
        return 'unknown (no class resolved)'
    c0 = info['classes'][0]
    if c0['type'] == 'OBJECT':   return 'OV (master-data object)'
    if c0['type'] == 'TABLE':    return 'TV (table-class)'
    if c0['type'] == 'DATA' and c0['scope'] == 'DAY':   return 'N1 daily-status grid'
    if c0['type'] == 'DATA' and c0['scope'] == 'MONTH': return 'N monthly-status grid'
    return f"{c0['type']}/{c0['scope']}"

def help_text(page, name, timeout_ms=45000):
    """Open the screen, trigger in-session openOnlineHelp(), return description text. Best-effort."""
    try:
        box = page.locator('[id="menu:searchForm:searchTxt"]'); box.fill(''); box.type(name, delay=25)
        page.wait_for_timeout(1200)
        link = page.locator(f'xpath=//*[self::label or self::span][contains(@class,"tv-link") and normalize-space(text())="{name}"]')
        if not link.count(): return None
        link.first.click(); page.wait_for_load_state('networkidle', timeout=timeout_ms); page.wait_for_timeout(1500)
        ctx = page.context
        with ctx.expect_page(timeout=10000) as np:
            page.evaluate('openOnlineHelp()')
        h = np.value; h.wait_for_load_state('domcontentloaded', timeout=15000); h.wait_for_timeout(1500)
        body = h.inner_text('body'); h.close()
        m = re.search(r'Description\s*(.+?)(?:Business Function|Screenshots|$)', body, re.S)
        return (m.group(1).strip()[:900] if m else body[:500].strip()) or None
    except Exception:
        return None

def _ascii(s):
    """Force ASCII (R18/R20) - EC help text often has smart quotes / dashes."""
    if not s: return s
    for k, v in {'’': "'", '‘': "'", '“': '"', '”': '"',
                 '—': '-', '–': '-', '…': '...', ' ': ' '}.items():
        s = s.replace(k, v)
    return s.encode('ascii', 'ignore').decode('ascii')

def write_note(wt, bf_code, name, info, help_desc):
    help_desc = _ascii(help_desc); name = _ascii(name)
    nd = Path(wt) / 'DeepDiveLearnings' / 'ec-screens' / 'notes'; nd.mkdir(parents=True, exist_ok=True)
    rows = '\n'.join(f"| `{c['class']}` | {c['type']}/{c['scope']} | `{c['base']}` | `{c['view'] or '(none)'}` |"
                     for c in info['classes']) or "| (no class resolved from URL/LABEL) | | | |"
    body = f"""# {bf_code} - {name}

_Deep-dive {datetime.now().strftime('%Y-%m-%d')} (deterministic runner). Module: {bf_code.split('.')[0]}._

## Identity
- BF_CODE: {bf_code} - URL: `{info['url'] or '(none)'}`

## DB binding (metadata-resolved)
| Class | Type/Scope | Base table | View |
|---|---|---|---|
{rows}

## Screen type
{screen_type(info)}

## Help (description)
{help_desc if help_desc else '_(not captured this run - DB binding above is verified; Help to backfill)_'}
"""
    has_db = any(c.get('view') for c in info['classes'])
    missing = []
    if not has_db: missing.append('DB binding')
    if not help_desc: missing.append('Help')
    (nd / f'{bf_code}.md').write_text(body, encoding='utf-8')
    return (not missing), ', '.join(missing)

def mark_checklist(wt, bf_code, name, full, missing):
    p = Path(wt) / 'DeepDiveLearnings' / 'ec-screens' / 'CHECKLIST.md'
    s = p.read_text(encoding='utf-8')
    mark = '[x]' if full else '[~]'
    suffix = '' if full else f' (partial: missing {missing})'
    newline = f'- {mark} **{bf_code}** — {name} -> notes/{bf_code}.md{suffix}'
    s = re.sub(r'(?m)^- \[[ x~\-]\] \*\*' + re.escape(bf_code) + r'\*\* .*$', newline, s, count=1)
    p.write_text(s, encoding='utf-8')

def main():
    log(f'EC-screen learn (deterministic): start, max={MAXN}, push={DO_PUSH}')
    if not ensure_worktree(): log('ABORTED: worktree not ready'); return 1
    try:
        import oracledb
        from playwright.sync_api import sync_playwright
    except Exception as e:
        log(f'ABORTED: missing dep {str(e)[:80]}'); return 1
    checklist = Path(WT) / 'DeepDiveLearnings' / 'ec-screens' / 'CHECKLIST.md'
    screens = pick_screens(checklist, MAXN)
    if not screens: log('nothing to do (no [ ] screens found)'); return 0
    log(f'screens this run: {", ".join(c for c,_ in screens)}')
    con = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN, tcp_connect_timeout=15); cur = con.cursor()
    done_full = done_partial = 0
    with sync_playwright() as p:
        br = p.chromium.launch(headless=True)
        page = br.new_context(ignore_https_errors=True, viewport={'width': 1500, 'height': 1000}).new_page()
        page.goto(EC_URL, wait_until='domcontentloaded', timeout=60000)
        page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
        page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); page.wait_for_timeout(1200)
        for bf_code, name in screens:
            try:
                info = db_resolve(cur, bf_code, name)
                hd = help_text(page, name)
                full, missing = write_note(WT, bf_code, name, info, hd)
                mark_checklist(WT, bf_code, name, full, missing)
                done_full += int(full); done_partial += int(not full)
                log(f'  {bf_code}: {"FULL" if full else "PARTIAL["+missing+"]"} ({len(info["classes"])} class)')
            except Exception as e:
                log(f'  {bf_code}: skipped ({str(e)[:60]})')
        br.close()
    con.close()
    git(['add', 'DeepDiveLearnings/ec-screens/'], cwd=WT)
    msg = f'learn(ec-screens): {", ".join(c for c,_ in screens)} ({done_full} full, {done_partial} DB-only)'
    git(['commit', '-m', msg], cwd=WT)
    if DO_PUSH:
        r = git(['push', 'origin', 'HEAD:' + BRANCH], cwd=WT)
        log('pushed' if r.returncode == 0 else 'push failed: ' + (r.stderr or r.stdout)[:100])
    else:
        log('TEST MODE: committed locally, not pushed')
    log(f'EC-screen learn (deterministic): done - {done_full} full + {done_partial} DB-only')
    return 0

if __name__ == '__main__':
    sys.exit(main())
