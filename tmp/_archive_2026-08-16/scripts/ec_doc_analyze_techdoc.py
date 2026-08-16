"""Analyze technical-documentation structure to plan deep-dive sessions. Read-only (local JSON)."""
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
print(f'technical-documentation pages: {len(tech)}\n')

# group by the path segment after technical-documentation/
groups = defaultdict(list)
for e in tech:
    abs_url = e['abs']
    marker = '/technical-documentation/'
    tail = abs_url.split(marker, 1)[1] if marker in abs_url else abs_url
    seg = tail.split('/')
    module = seg[0] if len(seg) > 1 else '(top)'
    groups[module].append(e['text'] or seg[-1])

print('=== Modules under technical-documentation (page count) ===')
for mod in sorted(groups, key=lambda k: -len(groups[k])):
    print(f'\n## {mod}  ({len(groups[mod])} pages)')
    for t in groups[mod][:12]:
        print(f'   - {t[:64]}')
    if len(groups[mod]) > 12:
        print(f'   ... +{len(groups[mod]) - 12} more')
