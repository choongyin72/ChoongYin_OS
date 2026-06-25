"""
EC Screen Help Deep-Dive - DETERMINISTIC unattended runner (no LLM spawn, no improvising).

Root-cause fix: the old version spawned a headless Claude session that had to re-derive the browser+DB recipe
every run and flailed (ORA-06569 x24, timeouts, 30 min, 0 commits). This version runs the PROVEN steps directly
in Python, per screen, with a hard timeout + best-effort fallback so it can never hang:
  1) read CHECKLIST.md -> next N unfinished screens (priority/file order)
  2) DB (metadata tables only -> no ORA-06569): BUSINESS_FUNCTION + class_cnfg/class_property_cnfg
     -> class, CLASS_TYPE, TIME_SCOPE, base table, OV_/TV_/DV_ view, screen type
  3) Help: login once, then per screen open it + openOnlineHelp() -> description text AND a full-page
     screenshot of the Help popup saved to notes/<BF_CODE>_help.png (both best-effort, timeout-guarded)
  4) write notes/<BF_CODE>.md (incl. the screenshot reference), mark [x] (full = DB+Help text) or
     [~] (DB only, Help not captured); the screenshot is a bonus and does not change the full/partial threshold
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
    rf = git(['fetch', 'origin', BRANCH])
    if rf.returncode:
        log(f'WARNING: git fetch failed ({(rf.stderr or rf.stdout)[:80].strip()}) -- using cached refs')
    git(['worktree', 'prune'])
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
        m = re.match(r'- \[([ ~])\] \*\*([A-Z0-9.]+)\*\* (?:' + chr(0x2014) + r'|-) (.+)', ln)
        if not m: continue
        status, code, rest = m.group(1), m.group(2), m.group(3)
        name = rest.split(' -> ')[0].split(' (')[0].strip()
        (partial if status == '~' else todo).append((code, name))
    return (partial + todo)[:n]

def _class_exists(cur, cn):
    cur.execute("SELECT 1 FROM class_cnfg WHERE class_name=:c", [cn])
    return cur.fetchone() is not None

def db_resolve(cur, bf_code, name):
    """Resolve the screen's data class via layered HIGH-CONFIDENCE strategies (metadata tables only -> safe).
    Order: (1) explicit CLASS_NAME tokens in the URL; (2) the URL's last path-segment as a class token,
    verb-prefix stripped, only if it IS a real class (e.g. maintain_equity_share -> EQUITY_SHARE);
    (3) a case-insensitive EXACT label match, only when UNIQUE. Ambiguous/none -> left unresolved
    (honest [~] partial; never guess a binding)."""
    info = {'url': None, 'classes': [], 'resolved_by': None}
    cur.execute("SELECT url FROM business_function WHERE bf_code=:c", [bf_code])
    r = cur.fetchone(); info['url'] = r[0] if r else None
    url = info['url'] or ''
    classes = re.findall(r'CLASS_NAME[^/]*/([A-Z0-9_]+)', url)
    if classes:
        info['resolved_by'] = 'url CLASS_NAME'
    else:  # (2) URL last path-segment token
        tok = url.rstrip('/').split('/')[-1].upper()
        for cand in dict.fromkeys([tok, re.sub(r'^(MAINTAIN|MANAGE|EDIT|VIEW|CREATE)_', '', tok)]):
            if cand and _class_exists(cur, cand):
                classes = [cand]; info['resolved_by'] = 'url path token'; break
    if not classes:  # (3) case-insensitive EXACT label, only if unambiguous
        cur.execute("""SELECT DISTINCT class_name FROM class_property_cnfg
                       WHERE property_code='LABEL' AND UPPER(property_value)=UPPER(:n)""", [name])
        labs = [row[0] for row in cur.fetchall()]
        if len(labs) == 1:
            classes = labs; info['resolved_by'] = 'label (exact, unique)'
        elif len(labs) > 1:
            info['resolved_by'] = f'ambiguous label ({len(labs)} candidates) - left unresolved'
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

def _clip(s, limit=2400):
    """Trim to <=limit chars but cut on a sentence/paragraph boundary so text never ends mid-word."""
    s = (s or '').strip()
    if len(s) <= limit:
        return s or None
    cut = s[:limit]
    for sep in ('\n\n', '. ', '.\n', '\n'):
        i = cut.rfind(sep)
        if i > limit * 0.6:
            return cut[:i + 1].strip() + ' [...]'
    return cut.rstrip() + ' [...]'

def help_text(page, name, shot_path=None, timeout_ms=45000):
    """Open the screen, trigger in-session openOnlineHelp(); return (description_text, screenshot_saved).
    Both best-effort + timeout-guarded. If shot_path is given, save a full-page PNG of the Help popup
    (which itself includes the screen's own Screenshots section) so the note carries a visual reference."""
    try:
        box = page.locator('[id="menu:searchForm:searchTxt"]'); box.fill(''); box.type(name, delay=25)
        page.wait_for_timeout(1200)
        q = "'" if '"' in name else '"'
        link = page.locator(f"xpath=//*[self::label or self::span][contains(@class,'tv-link') and normalize-space(text())={q}{name}{q}]")
        if not link.count(): return None, False
        link.first.click(); page.wait_for_load_state('networkidle', timeout=timeout_ms); page.wait_for_timeout(1500)
        ctx = page.context
        with ctx.expect_page(timeout=10000) as np:
            page.evaluate('openOnlineHelp()')
        h = np.value; h.wait_for_load_state('domcontentloaded', timeout=15000); h.wait_for_timeout(1500)
        body = h.inner_text('body')
        shot_ok = False
        if shot_path:
            try:
                h.screenshot(path=shot_path, full_page=True); shot_ok = True
            except Exception:
                shot_ok = False  # screenshot is a bonus; never fail the screen on it
        h.close()
        m = re.search(r'Description\s*(.+?)(?:Business Function|Screenshots|$)', body, re.S)
        text = _clip(m.group(1), 2400) if m else _clip(body, 600)
        return text, shot_ok
    except Exception:
        return None, False

def _ascii(s):
    """Force ASCII (R18/R20) - EC help text often has smart quotes / dashes."""
    if not s: return s
    repl = {0x2019: "'", 0x2018: "'", 0x201c: '"', 0x201d: '"',
            0x2014: '-', 0x2013: '-', 0x2026: '...', 0x00a0: ' '}
    for cp, v in repl.items():
        s = s.replace(chr(cp), v)
    return s.encode('ascii', 'ignore').decode('ascii')

def write_note(wt, bf_code, name, info, help_desc, help_shot=False):
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

_Resolved by: {info.get('resolved_by') or 'not resolved'}_

## Screen type
{screen_type(info)}

## Help (description)
{help_desc if help_desc else '_(not captured this run - DB binding above is verified; Help to backfill)_'}

## Help (screenshot)
{f'![{bf_code} Help screenshot]({bf_code}_help.png)' if help_shot else '_(no Help screenshot captured this run)_'}
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
    newline = f'- {mark} **{bf_code}** - {_ascii(name)} -> notes/{bf_code}.md{suffix}'
    orig = s
    s = re.sub(r'(?m)^- \[[ x~\-]\] \*\*' + re.escape(bf_code) + r'\*\* .*$', newline, s, count=1)
    if s == orig:
        log(f'  WARNING: {bf_code} not found in CHECKLIST.md -- mark skipped')
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
    try:
        con = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN, tcp_connect_timeout=15)
        cur = con.cursor()
    except Exception as e:
        log(f'ABORTED: DB connect failed ({str(e)[:120]})'); return 1
    done_full = done_partial = 0
    with sync_playwright() as p:
        br = None
        try:
            br = p.chromium.launch(headless=True)
            page = br.new_context(ignore_https_errors=True, viewport={'width': 1500, 'height': 1000}).new_page()
            page.goto(EC_URL, wait_until='domcontentloaded', timeout=60000)
            page.fill('#username', EC_USER); page.fill('#password', EC_PASS); page.click('#kc-login')
            page.wait_for_selector('[id="menu:searchForm:searchTxt"]', timeout=60000); page.wait_for_timeout(1200)
        except Exception as e:
            log(f'ABORTED: browser/login failed ({str(e)[:120]})')
            if br: br.close()
            con.close(); return 1
        for bf_code, name in screens:
            try:
                info = db_resolve(cur, bf_code, name)
                notes_dir = Path(WT) / 'DeepDiveLearnings' / 'ec-screens' / 'notes'
                notes_dir.mkdir(parents=True, exist_ok=True)
                shot_path = str(notes_dir / f'{bf_code}_help.png')
                hd, shot_ok = help_text(page, name, shot_path)
                full, missing = write_note(WT, bf_code, name, info, hd, shot_ok)
                mark_checklist(WT, bf_code, name, full, missing)
                done_full += int(full); done_partial += int(not full)
                log(f'  {bf_code}: {"FULL" if full else "PARTIAL["+missing+"]"} ({len(info["classes"])} class{", +shot" if shot_ok else ""})')
            except Exception as e:
                log(f'  {bf_code}: skipped ({str(e)[:60]})')
        br.close()
    con.close()
    git(['add', 'DeepDiveLearnings/ec-screens/'], cwd=WT)
    if done_full + done_partial == 0:
        log('nothing committed (all screens skipped -- no notes written)')
    else:
        msg = f'learn(ec-screens): {", ".join(c for c,_ in screens)} ({done_full} full, {done_partial} partial)'
        git(['commit', '-m', msg], cwd=WT)
        if DO_PUSH:
            r = git(['push', 'origin', 'HEAD:' + BRANCH], cwd=WT)
            if r.returncode:
                log('push failed (non-fast-forward?), retrying after rebase: ' + (r.stderr or r.stdout)[:80].strip())
                git(['fetch', 'origin', BRANCH], cwd=WT)
                rb = git(['rebase', f'origin/{BRANCH}'], cwd=WT)
                if rb.returncode:
                    log('rebase failed -- committed notes NOT pushed (will retry next run): ' + (rb.stderr or rb.stdout)[:80].strip())
                else:
                    r2 = git(['push', 'origin', 'HEAD:' + BRANCH], cwd=WT)
                    log('pushed after rebase' if r2.returncode == 0 else 'push still failed: ' + (r2.stderr or r2.stdout)[:80].strip())
            else:
                log('pushed')
        else:
            log('TEST MODE: committed locally, not pushed')
    log(f'EC-screen learn (deterministic): done - {done_full} full + {done_partial} partial')
    return 0

if __name__ == '__main__':
    sys.exit(main())
