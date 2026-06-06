"""List screens that could not be accessed."""
import json

KB_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_final.json'

with open(KB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)

missing = [(k, v) for k, v in db.items() if not v.get('found')]
print(f'Missing screens: {len(missing)}\n')

# Group by section
sections = {}
for k, v in missing:
    s = v.get('section', '?')
    if s not in sections: sections[s] = []
    sections[s].append(v.get('name', k.split('::')[-1]))

for sec, names in sorted(sections.items(), key=lambda x: -len(x[1])):
    print(f'[{sec}] — {len(names)} screens:')
    for n in sorted(names):
        print(f'  - {n}')
    print()
