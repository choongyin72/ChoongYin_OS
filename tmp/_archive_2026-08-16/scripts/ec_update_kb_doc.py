"""Generate updated EC screen knowledge base from captured data."""
import json, os

KB_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_final.json'
DOC_PATH = r'c:\Projects\ChoongYin_OS\workstreams\master-plan\drafts\ec-screen-knowledge-base.md'

with open(KB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)

found = [v for v in db.values() if v.get('found')]
not_found_count = sum(1 for v in db.values() if not v.get('found'))

print(f'Total found: {len(found)} / 670 ({len(found)/670*100:.1f}%)')

# Group by section
sections = {}
for v in found:
    s = v.get('section', '?')
    if s not in sections: sections[s] = []
    sections[s].append(v)

# Print comprehensive summary for each section
print('\n' + '='*80)
print('COMPLETE SCREEN INVENTORY')
print('='*80)

for sec, screens in sorted(sections.items(), key=lambda x: -len(x[1])):
    print(f'\n=== {sec} ({len(screens)} screens) ===')

    nav_table = [s for s in screens if s.get('screen_type')=='NAVIGATOR+TABLE']
    nav_only  = [s for s in screens if s.get('screen_type')=='NAVIGATOR-ONLY']
    table_only= [s for s in screens if s.get('screen_type')=='TABLE-ONLY']
    action    = [s for s in screens if s.get('screen_type')=='ACTION/EMPTY']

    for category, items in [('NAVIGATOR+TABLE', nav_table), ('NAVIGATOR-ONLY', nav_only),
                              ('TABLE-ONLY', table_only), ('ACTION/EMPTY', action)]:
        if not items: continue
        print(f'\n  [{category}] ({len(items)}):')
        for s in items:
            iud = ('S' if s.get('save_enabled') else '-') + \
                  ('+' if s.get('insert_enabled') else '-') + \
                  ('D' if s.get('delete_enabled') else '-')
            nav = [la for g in s.get('nav_labels',[]) for la in g[:2]]
            cols= [c for dt in s.get('datatables',[]) for c in dt.get('cols',[])[:2]]
            btns= s.get('action_buttons',[])[:2]
            print(f'    {iud} {s.get("name",""):<32} nav={nav[:2]} cols={cols[:2]}{"  btns="+str(btns) if btns else ""}')

print(f'\n\nNot navigated: {not_found_count} screens (not accessible in local EC sandbox)')
print('These screens exist in the tree but could not be navigated via search/label.')
print('They are likely accessible in Woodside Pluto COPS DEV with proper roles.')
