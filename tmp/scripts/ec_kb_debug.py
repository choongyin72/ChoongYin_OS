"""Debug KB file contents."""
import json, os

KB_PATH = r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_v3.json'
LOG_PATHS = [
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_v3.txt',
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_search.txt',
]

print('=== KB FILE ===')
with open(KB_PATH, 'r', encoding='utf-8') as f:
    db = json.load(f)
found = [v for v in db.values() if v.get('found')]
not_found = [v for v in db.values() if not v.get('found')]
print(f'Total: {len(db)} | Found: {len(found)} | Not found: {len(not_found)}')
print(f'Progress: {len(found)}/670 = {len(found)/670*100:.1f}%')

# Show all found screens
print(f'\nAll found screens ({len(found)}):')
for v in found:
    iud = ('S' if v.get('save_enabled') else '-') + ('+' if v.get('insert_enabled') else '-')
    nav = [la for g in v.get('nav_labels',[]) for la in g[:2]]
    cols= [c for dt in v.get('datatables',[]) for c in dt.get('cols',[])[:2]]
    print(f'  {iud} [{v.get("section","")[:12]:<12}] {v.get("name",""):<30} '
          f'{v.get("screen_type",""):<18} nav={nav[:1]} cols={cols[:1]}')

for logpath in LOG_PATHS:
    if os.path.exists(logpath):
        print(f'\n=== LOG: {os.path.basename(logpath)} ===')
        with open(logpath, 'rb') as f:
            lines = f.read().decode('utf-8','replace').splitlines()
        # Show first few + last few non-empty lines
        non_empty = [l for l in lines if l.strip() and not l.strip() == ' '*len(l.strip())]
        print(f'Total lines: {len(lines)} | Non-empty: {len(non_empty)}')
        print('First 3:', non_empty[:3])
        print('Last 3:', non_empty[-3:])
