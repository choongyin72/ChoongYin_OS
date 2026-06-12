"""Backup helper for shared keyword files - run BEFORE any change to a common
RF resource / library / shared engine file.

Usage: py backup_keyword_file.py <file> [<file>...]
Copies each file to ec-automation/.keyword_backups/<name>.<YYYYMMDD_HHMMSS>.bak
"""
import shutil
import sys
import time
from pathlib import Path

BACKUPS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/.keyword_backups")
BACKUPS.mkdir(exist_ok=True)

if len(sys.argv) < 2:
    raise SystemExit("usage: py backup_keyword_file.py <file> [<file>...]")

stamp = time.strftime("%Y%m%d_%H%M%S")
for arg in sys.argv[1:]:
    src = Path(arg)
    if not src.exists():
        print(f"!! not found: {src}")
        continue
    dst = BACKUPS / f"{src.name}.{stamp}.bak"
    shutil.copy2(src, dst)
    print(f"backed up: {src.name} -> {dst.name}")
