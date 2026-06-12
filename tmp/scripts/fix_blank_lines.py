"""Repair: restore the 2 blank lines between the Variables section and the next
section header that suite_data_refactor.py's greedy \\s*$ accidentally consumed."""
import re
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/tests")
pat = re.compile(r"(\$\{TEST_START_DATE(?:_REFDD)?\})\n(\*\*\* )")
fixed = 0
for f in sorted(TESTS.rglob("*.robot")):
    text = f.read_text(encoding="utf-8")
    new, n = pat.subn(r"\1\n\n\n\2", text)
    if n:
        f.write_text(new, encoding="utf-8")
        fixed += 1
print(f"fixed {fixed} files")
