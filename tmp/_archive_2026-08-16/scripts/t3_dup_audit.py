"""T3 duplication audit: parse every page object, extract keyword names + bodies,
group identical/near-identical bodies across files, and flag fat keywords.

Near-identical = same body after normalizing the screen-specific tokens
(variable names like ${BANK_...} -> ${X}, literal screen names -> <NAME>).
"""
import re
from collections import defaultdict
from pathlib import Path

PO = Path(r"c:/Projects/ChoongYin_OS/workstreams/master-plan/ec-automation/pageobjects")

def parse_keywords(text):
    """Return dict name -> list of body lines (stripped, no [Documentation])."""
    kws = {}
    in_kw_section = False
    name = None
    for line in text.splitlines():
        if line.startswith("*** "):
            in_kw_section = line.strip().lower().startswith("*** keywords")
            name = None
            continue
        if not in_kw_section:
            continue
        if line and not line[0].isspace():
            name = line.strip()
            kws[name] = []
        elif name is not None and line.strip():
            s = line.strip()
            if s.startswith("...") and kws[name] and kws[name][-1].startswith("[Documentation]"):
                continue
            if s.startswith("[Documentation]"):
                kws[name].append("[Documentation]")
                continue
            kws[name].append(s)
    return {k: [l for l in v if l != "[Documentation]"] for k, v in kws.items()}

def normalize(body):
    out = []
    for l in body:
        l = re.sub(r"\$\{[A-Z][A-Z0-9_]*\}", "${X}", l)   # screen-specific consts
        l = re.sub(r"\s{2,}", "  ", l)
        out.append(l)
    return "\n".join(out)

files = sorted(PO.rglob("*.resource"))
by_norm = defaultdict(list)   # normalized body -> [(file, kw_name, n_lines)]
fat = []                      # keywords > 8 lines (should be thin delegations)
all_kw_names = defaultdict(list)

for f in files:
    rel = str(f.relative_to(PO))
    kws = parse_keywords(f.read_text(encoding="utf-8"))
    for name, body in kws.items():
        if not body:
            continue
        all_kw_names[name].append(rel)
        if len(body) >= 3:    # only multi-line logic is interesting
            by_norm[normalize(body)].append((rel, name, len(body)))
        if len(body) > 8:
            fat.append((rel, name, len(body)))

print("== DUPLICATE MULTI-LINE BODIES (same normalized body in 2+ files) ==")
n_dup = 0
for body, locs in sorted(by_norm.items(), key=lambda kv: -len(kv[1])):
    file_set = {l[0] for l in locs}
    if len(file_set) >= 2:
        n_dup += 1
        print(f"\n--- cluster {n_dup}: {len(locs)} keywords / {len(file_set)} files, {locs[0][2]} lines ---")
        for rel, name, n in locs[:6]:
            print(f"    {name}    [{rel}]")
        if len(locs) > 6:
            print(f"    ... +{len(locs)-6} more")
        print("    body preview: " + " | ".join(body.splitlines()[:3]))
print(f"\ntotal duplicate clusters: {n_dup}")

print("\n== FAT KEYWORDS (>8 logic lines — candidates to push down to T2) ==")
for rel, name, n in sorted(fat, key=lambda x: -x[2])[:25]:
    print(f"  {n:3d}  {name}    [{rel}]")

print("\n== SAME KEYWORD NAME DEFINED IN MANY FILES (naming convention check) ==")
for name, rels in sorted(all_kw_names.items(), key=lambda kv: -len(kv[1])):
    if len(rels) >= 3:
        print(f"  {len(rels):2d}x  {name}")
