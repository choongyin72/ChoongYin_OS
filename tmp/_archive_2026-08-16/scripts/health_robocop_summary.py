"""Health pass step 1b: robocop summary grouped by file + rule."""
import re
import subprocess
from collections import Counter

ROOT = r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation"
r = subprocess.run(["robocop", "check", ROOT], capture_output=True, text=True,
                   timeout=300, shell=True)
out = (r.stdout or "") + (r.stderr or "")

pat = re.compile(r"^(workstreams\S+?):(\d+):\d+ (\w+) (.*)$", re.M)
by_file = Counter()
by_rule = Counter()
rows = []
for m in pat.finditer(out):
    f, line, rule, msg = m.groups()
    short = f.replace("workstreams\\master-plan\\ec-automation\\", "")
    by_file[short] += 1
    by_rule[rule] += 1
    rows.append((short, line, rule, msg[:80]))

print("== BY RULE ==")
for k, v in by_rule.most_common():
    print(f"  {k:8s} {v}")
print("\n== BY FILE ==")
for k, v in by_file.most_common():
    print(f"  {v:3d}  {k}")
print("\n== NON-DOC ISSUES (everything except DOC01/DOC02) ==")
for f, line, rule, msg in rows:
    if rule not in ("DOC01", "DOC02"):
        print(f"  {f}:{line} {rule} {msg}")
