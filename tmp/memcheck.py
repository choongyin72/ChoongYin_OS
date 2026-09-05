"""Every memory file must be reachable from MEMORY.md, and every link must resolve.

    py tmp/memcheck.py

Run after compacting the index - the whole risk of merging entries onto shared lines is a
pointer silently disappearing, which would make a memory unreachable without any error.
"""
import os
import re

M = (r"C:\Users\choong-yin.lee\.claude\projects"
     r"\c--Projects-ChoongYin-OS\memory")
idx = open(os.path.join(M, "MEMORY.md"), encoding="utf-8").read()
linked = set(re.findall(r'\(([a-z0-9_]+\.md)\)', idx))
files = {f for f in os.listdir(M) if f.endswith(".md") and f != "MEMORY.md"}

print("MEMORY.md: %d lines, %d link(s)" % (len(idx.splitlines()), len(linked)))
print("memory dir: %d file(s)" % len(files))
missing = sorted(linked - files)
orphan = sorted(files - linked)
print("\nbroken links (linked but no file): %d" % len(missing))
for f in missing:
    print("   %s" % f)
print("\nunreachable (file but not linked): %d" % len(orphan))
for f in orphan:
    print("   %s" % f)
print("\n%s" % ("OK" if not missing and not orphan else "NEEDS ATTENTION"))
