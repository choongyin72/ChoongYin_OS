"""
ChoongYin_OS health snapshot — read-only repo review to ground improvement priorities.
Reports: per-area file counts + staleness, root clutter, tmp sprawl, code duplication,
STATUS freshness. Single py script (no compound shell).
"""
from pathlib import Path
from datetime import datetime
import subprocess

ROOT = Path(r'c:\Projects\ChoongYin_OS')
now = datetime.now()


def git_tracked():
    out = subprocess.run(['git', '-C', str(ROOT), 'ls-files'], capture_output=True, text=True).stdout
    return [l for l in out.splitlines() if l]


def days_old(path: Path):
    try:
        return (now - datetime.fromtimestamp(path.stat().st_mtime)).days
    except Exception:
        return None


print(f'=== ChoongYin_OS health snapshot @ {now:%Y-%m-%d %H:%M} ===\n')

tracked = git_tracked()
print(f'Total tracked files: {len(tracked)}\n')

# per top-level area: count + newest file age
print('=== Top-level areas: file count | newest-file age (days) ===')
areas = {}
for f in tracked:
    top = f.split('/')[0]
    areas.setdefault(top, []).append(f)
for top in sorted(areas, key=lambda k: -len(areas[k])):
    files = areas[top]
    newest = None
    for f in files:
        d = days_old(ROOT / f)
        if d is not None and (newest is None or d < newest):
            newest = d
    tag = 'DIR ' if (ROOT / top).is_dir() else 'file'
    print(f'  {tag} {top:<28} {len(files):>5} files   newest={newest}d ago')

# root clutter
print('\n=== Root clutter (loose files directly at repo root) ===')
root_loose = [f for f in tracked if '/' not in f]
exts = {}
for f in root_loose:
    e = Path(f).suffix.lower() or '(none)'
    exts[e] = exts.get(e, 0) + 1
print(f'  {len(root_loose)} loose files at root: {exts}')
print('  examples:', root_loose[:8])

# workstreams breakdown
print('\n=== workstreams/ subfolders ===')
ws = ROOT / 'workstreams'
if ws.is_dir():
    for sub in sorted(ws.iterdir()):
        if sub.is_dir():
            fs = [p for p in sub.rglob('*') if p.is_file()]
            newest = min((days_old(p) for p in fs), default=None) if fs else None
            print(f'  {sub.name:<26} {len(fs):>4} files   newest={newest}d ago')

# tmp sprawl
print('\n=== tmp/ sprawl ===')
for sub in ['scripts', 'logs']:
    d = ROOT / 'tmp' / sub
    if d.is_dir():
        n = len([p for p in d.iterdir() if p.is_file()])
        print(f'  tmp/{sub}: {n} files')

# code duplication signal (how many scripts repeat the same EC helpers)
print('\n=== Code duplication signal (EC helper repetition) ===')
py_files = [ROOT / f for f in tracked if f.endswith('.py')]
patterns = {
    "login (page.fill('#username'": "#username",
    "ignore_https_errors": "ignore_https_errors",
    "navigate-to-screen (searchTxt)": "menu:searchForm:searchTxt",
    "set nav dropdown (dd_button)": "dd_button",
    "do_save / Save toolbar": "Save [Ctrl+s]",
    "oracledb connect": "oracledb.connect",
}
for label, needle in patterns.items():
    c = 0
    for p in py_files:
        try:
            if needle in p.read_text(encoding='utf-8', errors='ignore'):
                c += 1
        except Exception:
            pass
    print(f'  {label:<36} appears in {c} scripts')
print(f'  (total .py tracked: {len(py_files)})')

# STATUS freshness
print('\n=== Freshness ===')
for key in ['STATUS.md', 'CLAUDE.MD', 'DATA_SOURCES.MD']:
    p = ROOT / key
    if p.exists():
        print(f'  {key:<18} last modified {days_old(p)}d ago')

print('\n=== done ===')
