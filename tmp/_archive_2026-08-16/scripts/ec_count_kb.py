"""Quick count of KB results."""
import json, os

KB_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_final.json'
with open(KB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)

found    = [v for v in db.values() if v.get('found')]
not_found= [v for v in db.values() if not v.get('found')]
print(f'Total entries: {len(db)}')
print(f'Found (navigated): {len(found)}')
print(f'Not found (skipped): {len(not_found)}')
print(f'Progress: {len(found)}/670 = {len(found)/670*100:.1f}%')

# Count by type
types = {}
for v in found:
    t = v.get('screen_type','?')
    types[t] = types.get(t, 0) + 1
print(f'\nScreen types:')
for t, n in sorted(types.items()):
    print(f'  {t}: {n}')

# Count by section
sections = {}
for v in found:
    s = v.get('section','?')[:20]
    sections[s] = sections.get(s, 0) + 1
print(f'\nBy section:')
for s, n in sorted(sections.items(), key=lambda x:-x[1]):
    print(f'  {s:<22}: {n}')
