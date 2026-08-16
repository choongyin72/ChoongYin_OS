"""Read and summarize EC screen knowledge base — run this instead of inline py -c."""
import json, sys, os

# Auto-detect latest KB file
LOG_PATHS = [
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_v3.txt',
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_final.txt',
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_explore_log.txt',
]
KB_PATHS = [
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb_v3.json',
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_screen_kb.json',
    r'c:\Projects\ChoongYin_OS\tmp\logs\ec_full_screen_kb.json',
]

LOG_PATH = next((p for p in LOG_PATHS if os.path.exists(p)), LOG_PATHS[0])
KB_PATH  = next((p for p in KB_PATHS if os.path.exists(p)), KB_PATHS[0])

# Show last 50 lines of log
print('=== LAST LOG LINES ===')
try:
    with open(LOG_PATH, 'rb') as f:
        content = f.read().decode('utf-8', errors='replace')
    lines = content.splitlines()
    for line in lines[-60:]:
        print(line)
except Exception as e:
    print(f'Log error: {e}')

print('\n=== KNOWLEDGE BASE SUMMARY ===')
try:
    with open(KB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)

    found    = [v for v in db.values() if v.get('found')]
    not_found= [v for v in db.values() if not v.get('found')]
    print(f'Total: {len(db)} | Found: {len(found)} | Not found: {len(not_found)}')

    types = {}
    for v in found:
        t = v.get('screen_type','?')
        if t not in types: types[t] = []
        types[t].append(v)

    for t, screens in sorted(types.items()):
        print(f'\n--- {t} ({len(screens)}) ---')
        for s in screens[:8]:
            iud = ('S' if s.get('save_enabled') else '-') + \
                  ('+' if s.get('insert_enabled') else '-') + \
                  ('D' if s.get('delete_enabled') else '-')
            nav = [la for g in s.get('nav_labels',[]) for la in g[:2]]
            cols= [c for dt in s.get('datatables',[]) for c in dt.get('cols',[])[:2]]
            print(f'  {iud} [{s.get("section","")[:12]:<12}] {s.get("name",""):<30}'
                  f' nav={nav[:2]} cols={cols[:2]}')
        if len(screens) > 8:
            print(f'  ... and {len(screens)-8} more')
except Exception as e:
    print(f'KB error: {e}')
