"""Sub-analyze the frmw (167-page) module to plan sessions. Read-only."""
from pathlib import Path
import json
from collections import defaultdict


def _repo_root() -> Path:
    here = Path(__file__).resolve()
    for p in [here, *here.parents]:
        if (p / '.git').exists():
            return p
    return here.parents[3]


data = json.loads((_repo_root() / 'DeepDiveLearnings' / 'ec-docs' / 'ec_doc_index_bucketed.json').read_text(encoding='utf-8'))
tech = data.get('technical-documentation', [])
frmw = [e for e in tech if '/technical-documentation/frmw/' in e['abs']]
print(f'frmw pages: {len(frmw)}\n')

groups = defaultdict(list)
for e in frmw:
    tail = e['abs'].split('/technical-documentation/frmw/', 1)[1]
    seg = tail.split('/')
    sub = seg[0] if len(seg) > 1 else '(direct)'
    groups[sub].append(e['text'] or seg[-1])

print('=== frmw sub-groups (by path) ===')
for sub in sorted(groups, key=lambda k: -len(groups[k])):
    print(f'\n## frmw/{sub}  ({len(groups[sub])})')
    for t in groups[sub][:16]:
        print(f'   - {t[:62]}')
    if len(groups[sub]) > 16:
        print(f'   ... +{len(groups[sub]) - 16} more')
