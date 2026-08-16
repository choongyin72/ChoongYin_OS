"""Quality pass over the full Assets scan: break down ERROR rows and the OTHER
bucket by evidence + URL pattern, to find OV-variants vs genuinely-new patterns."""
import json
import re
from collections import Counter
from pathlib import Path

J = Path(r"c:/Projects/ChoongYin_OS/tmp/screen_scan/assets_scan.json")
data = json.loads(J.read_text(encoding="utf-8"))

errors = [(k, r.get("why", "")) for k, r in data.items() if r.get("status") != "ok"]
print("=== ERROR rows ===")
for k, why in errors:
    print(f"  {k}: {why[:120]}")

others = {k: r for k, r in data.items() if r.get("status") == "ok" and r["type"] == "OTHER"}
print(f"\n=== OTHER bucket: {len(others)} ===")
print("\n-- by evidence (why) --")
for why, n in Counter(r["why"] for r in others.values()).most_common():
    print(f"  {n:4d}  {why}")

print("\n-- by URL screen-path (first 2 segments after host) --")
def path2(u):
    m = re.match(r"https://[^/]+/([^/]+)/([^/?]+)", u or "")
    return f"{m.group(1)}/{m.group(2)}" if m else "?"
for p, n in Counter(path2(r.get("url")) for r in others.values()).most_common(40):
    print(f"  {n:4d}  {p}")

print("\n-- OTHER screens with marker combos (sample per evidence group) --")
seen = set()
for k, r in others.items():
    why = r["why"]
    if why in seen:
        continue
    seen.add(why)
    m = r["markers"]
    print(f"  e.g. {k}")
    print(f"       url={r['url'][:100]}")
    print(f"       tabs={m['tabs']} nav={m['navApplyBtn']} tables={m['dataTables'][:3]} insert={m['insertMenu']} treeTable={m['treeTable']} editCells={m['editableCells']}")
