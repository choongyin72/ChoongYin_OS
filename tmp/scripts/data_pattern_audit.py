"""Data/variable handling audit across test suites: how is test data defined today?
Reports: per-suite *** Variables *** blocks, repeated literal values across suites,
AUTOTEST code conventions, date conventions.
"""
import re
from collections import Counter, defaultdict
from pathlib import Path

TESTS = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/tests")

var_line = re.compile(r"^(\$\{[A-Z0-9_]+\})\s{2,}(.+)$")
value_locs = defaultdict(list)
suite_vars = {}

for f in sorted(TESTS.rglob("*.robot")):
    rel = str(f.relative_to(TESTS))
    in_vars = False
    rows = []
    for line in f.read_text(encoding="utf-8").splitlines():
        if line.startswith("*** "):
            in_vars = line.strip().lower().startswith("*** variables")
            continue
        if in_vars:
            m = var_line.match(line.strip()) or var_line.match(line)
            if line and not line.startswith("#") and "    " in line and line.strip().startswith("${"):
                parts = re.split(r"\s{2,}", line.strip(), maxsplit=1)
                if len(parts) == 2:
                    rows.append((parts[0], parts[1]))
                    value_locs[parts[1]].append(rel)
    suite_vars[rel] = rows

print("== VALUES REPEATED ACROSS 3+ SUITES ==")
for val, locs in sorted(value_locs.items(), key=lambda kv: -len(kv[1])):
    uniq = sorted(set(locs))
    if len(uniq) >= 3:
        print(f"  {len(uniq):2d} suites: {val!r}")

print("\n== AUTOTEST CODE VALUES (uniqueness check) ==")
codes = Counter()
for val, locs in value_locs.items():
    if "AUTOTEST" in val.upper() or val.upper().startswith("AT_"):
        codes[val] += len(set(locs))
for val, n in codes.most_common(40):
    print(f"  {n:2d}x  {val}")

print("\n== SAMPLE VARIABLE BLOCKS (one per section) ==")
for sample in [
    "Configuration\\Assets\\Basic_Objects\\country_iud.robot",
    "Configuration\\Assets\\Financial_Objects\\bank_iud.robot",
    "Configuration\\Assets\\Commercial_Objects\\vendor_iud.robot",
]:
    print(f"\n--- {sample} ---")
    for k, v in suite_vars.get(sample, []):
        print(f"    {k:24s} {v}")
