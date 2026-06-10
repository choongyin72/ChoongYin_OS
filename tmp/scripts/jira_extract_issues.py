import json, sys

path = sys.argv[1]
with open(path, encoding="utf-8") as f:
    raw = f.read()

# file may be a JSON array of {type,text} or plain JSON
try:
    outer = json.loads(raw)
except Exception:
    print("cannot parse file as JSON"); sys.exit(1)

candidates = []
if isinstance(outer, list):
    for item in outer:
        t = item.get("text", "")
        try:
            candidates.append(json.loads(t))
        except Exception:
            pass
else:
    candidates.append(outer)

def field(node, *names):
    fields = node.get("fields", node)
    for n in names:
        v = fields.get(n)
        if v is None:
            continue
        if isinstance(v, dict):
            return v.get("name") or v.get("displayName") or v.get("key") or str(v)[:30]
        return v
    return ""

for data in candidates:
    issues = data.get("issues", {})
    nodes = issues.get("nodes", []) if isinstance(issues, dict) else issues
    print(f"=== {len(nodes)} issues ===")
    for n in nodes:
        key = n.get("key", "?")
        print(f"{key:<12} [{field(n,'issuetype','issueType'):<12}] {field(n,'status'):<22} upd={str(field(n,'updated'))[:10]} asg={field(n,'assignee'):<22} {str(field(n,'summary'))[:80]}")
