"""Resolve Disposition Type's treeview breadcrumb from the flat depth-ordered inventory."""
import json
d = json.load(open(r"C:\Projects\ChoongYin_OS\docs\EC\ec_full_tree_inventory.json"))
# find Disposition Type index
idx = next(i for i, r in enumerate(d) if r.get("text") == "Disposition Type")
target = d[idx]
print("target:", target)
# walk backwards collecting nearest lower-depth ancestors
chain = [target]
need = target["depth"] - 1
i = idx - 1
while i >= 0 and need >= 0:
    if d[i].get("depth") == need:
        chain.append(d[i])
        need -= 1
    i -= 1
chain.reverse()
print("\nBREADCRUMB:")
print("  " + " > ".join(r.get("text", "?") for r in chain))
