import json, sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    outer = json.load(f)

for i, item in enumerate(outer):
    text = item.get("text", "")
    try:
        data = json.loads(text)
    except Exception:
        print(f"--- entry {i}: not JSON, first 200 chars ---")
        print(text[:200])
        continue
    if isinstance(data, dict) and "values" in data:
        vals = data["values"]
        print(f"--- entry {i}: total={data.get('total')} isLast={data.get('isLast')} returned={len(vals)} ---")
        for p in vals:
            print(f"{p.get('key'):<12} {str(p.get('name')):<55} {p.get('projectTypeKey','')}")
    else:
        print(f"--- entry {i}: JSON of type {type(data).__name__}, keys={list(data)[:10] if isinstance(data, dict) else 'n/a'} ---")
